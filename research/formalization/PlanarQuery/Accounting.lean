import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Ring

namespace PlanarQuery

/-! Exact algebra used by the expected-depth proof. The construction
    parameters are inputs; no decimal certificate is assumed here. -/

def deficit (threshold coefficient : ℝ) : ℝ :=
  max (threshold - coefficient) 0

theorem deficit_nonneg (threshold coefficient : ℝ) :
    0 ≤ deficit threshold coefficient := le_max_right _ _

theorem coefficient_from_deficit (threshold coefficient : ℝ) :
    threshold - deficit threshold coefficient ≤ coefficient := by
  have h := le_max_left (threshold - coefficient) (0 : ℝ)
  unfold deficit
  linarith

theorem capped_coefficient (m coefficient threshold cap : ℝ)
    (hm : 0 ≤ m) (hcap : m ≤ cap) :
    threshold * m - cap * deficit threshold coefficient ≤ m * coefficient := by
  have ha := mul_le_mul_of_nonneg_left
    (coefficient_from_deficit threshold coefficient) hm
  have hc := mul_le_mul_of_nonneg_right hcap
    (deficit_nonneg threshold coefficient)
  nlinarith

/-- Individual coefficient deficits are charged at their individual mass
    cap. This proves the paper's conversion, including arbitrary zero mass. -/
theorem capped_rank_credit {ι : Type*} [Fintype ι]
    (m coefficient : ι → ℝ) (b zeroMass w δ μ τ ζ χ : ℝ)
    (hm : ∀ i, 0 ≤ m i) (hcap : ∀ i, m i ≤ 2 * δ * w)
    (hsum : ∑ i, m i = b) (hw : w = b + zeroMass)
    (hzero : 0 ≤ zeroMass)
    (hχ : χ = τ - 2 * δ * (∑ i, deficit τ (coefficient i)) - δ * μ)
    (hroute : τ ≤ χ + ζ) :
    χ * b ≤ (∑ i, m i * coefficient i) - δ * w * μ + ζ * zeroMass := by
  have hlocal := Finset.sum_le_sum fun i (_ : i ∈ Finset.univ) =>
    capped_coefficient (m i) (coefficient i) τ (2 * δ * w) (hm i) (hcap i)
  simp only [Finset.sum_sub_distrib, ← Finset.mul_sum, hsum] at hlocal
  have hz : 0 ≤ zeroMass * (χ + ζ - τ) :=
    mul_nonneg hzero (by linarith)
  rw [hw] at hlocal ⊢
  have halgebra :
      τ * b - 2 * δ * (b + zeroMass) * (∑ i, deficit τ (coefficient i)) -
        δ * (b + zeroMass) * μ + ζ * zeroMass =
      χ * b + zeroMass * (χ + ζ - τ) := by
    rw [hχ]
    ring
  nlinarith [halgebra]

/-- Absorb endpoint information and the capped positive mass into one
    information charge. The geometric and entropy inputs are explicit. -/
theorem flat_stage_absorption
    (W A Δ B b I J c inverseLog σ : ℝ)
    (hb : 0 ≤ b) (hc : 0 ≤ c) (hJI : J ≤ I)
    (hJ : b * σ ≤ J) (hB : B ≤ c * σ)
    (hk : inverseLog ≤ c)
    (hstage : W ≤ A * Δ + B * b + inverseLog * (I - J)) :
    W ≤ A * Δ + c * I := by
  have hmass := mul_le_mul_of_nonneg_right hB hb
  have hentropy := mul_le_mul_of_nonneg_left hJ hc
  have hremaining := mul_le_mul_of_nonneg_right hk (sub_nonneg.mpr hJI)
  nlinarith

/-! A recursive partition can have arbitrary arity. Its cancellation is
    represented as a finite ledger of internal nodes. The equation hcancel
    is a genuine input here; the binary-tree theorem below proves cancellation
    independently rather than assuming it. -/

theorem finite_ledger_bound {ι : Type*} [Fintype ι]
    (cost Δ information : ι → ℝ) (A c optimum entropy : ℝ)
    (hcost : ∀ i, cost i ≤ A * Δ i + c * information i)
    (hopt : ∑ i, Δ i = optimum)
    (hent : ∑ i, information i = entropy) :
    (∑ i, cost i) ≤ A * optimum + c * entropy := by
  have hsum := Finset.sum_le_sum fun i (_ : i ∈ Finset.univ) => hcost i
  simpa [Finset.sum_add_distrib, ← Finset.mul_sum, hopt, hent] using hsum

inductive Ledger where
  | leaf (potential entropy : ℝ)
  | fork (potential entropy localCost : ℝ) (left right : Ledger)

namespace Ledger

def potential : Ledger → ℝ
  | .leaf p _ => p
  | .fork p _ _ _ _ => p

def entropy : Ledger → ℝ
  | .leaf _ e => e
  | .fork _ e _ _ _ => e

def cost : Ledger → ℝ
  | .leaf _ _ => 0
  | .fork _ _ c l r => c + cost l + cost r

def decrementSum : Ledger → ℝ
  | .leaf _ _ => 0
  | .fork p _ _ l r =>
      (p - potential l - potential r) + decrementSum l + decrementSum r

def leafPotential : Ledger → ℝ
  | .leaf p _ => p
  | .fork _ _ _ l r => leafPotential l + leafPotential r

def entropyDecrementSum : Ledger → ℝ
  | .leaf _ _ => 0
  | .fork _ e _ l r =>
      (e - entropy l - entropy r) + entropyDecrementSum l + entropyDecrementSum r

def leafEntropy : Ledger → ℝ
  | .leaf _ e => e
  | .fork _ _ _ l r => leafEntropy l + leafEntropy r

theorem potential_cancels (T : Ledger) :
    decrementSum T = potential T - leafPotential T := by
  induction T with
  | leaf p e => simp [decrementSum, potential, leafPotential]
  | fork p e c l r ihl ihr =>
    simp only [decrementSum, potential, leafPotential, ihl, ihr]
    ring

theorem entropy_cancels (T : Ledger) :
    entropyDecrementSum T = entropy T - leafEntropy T := by
  induction T with
  | leaf p e => simp [entropyDecrementSum, entropy, leafEntropy]
  | fork p e c l r ihl ihr =>
    simp only [entropyDecrementSum, entropy, leafEntropy, ihl, ihr]
    ring

def LocalBound (A c : ℝ) : Ledger → Prop
  | .leaf p e => p = 0 ∧ e = 0
  | .fork p e stageCost l r =>
      stageCost ≤ A * (p - potential l - potential r) +
        c * (e - entropy l - entropy r) ∧
      LocalBound A c l ∧ LocalBound A c r

/-- The main proof pattern: local decrements pay for the whole recursion.
    This is a proved induction over an arbitrary actual ledger tree. -/
theorem local_to_global (T : Ledger) (A c : ℝ) (h : LocalBound A c T) :
    cost T ≤ A * potential T + c * entropy T := by
  induction T with
  | leaf p e =>
    simp only [LocalBound] at h
    simp [cost, potential, entropy, h.1, h.2]
  | fork p e stageCost l r ihl ihr =>
    simp only [LocalBound] at h
    have hl := ihl h.2.1
    have hr := ihr h.2.2
    simp only [cost, potential, entropy]
    nlinarith [h.1]

end Ledger

theorem entropy_to_ratio (cost A c optimum entropy logTwo : ℝ)
    (hc : 0 ≤ c) (hlower : entropy ≤ logTwo * optimum)
    (hcost : cost ≤ A * optimum + c * entropy) :
    cost ≤ (A + c * logTwo) * optimum := by
  have h := mul_le_mul_of_nonneg_left hlower hc
  nlinarith

end PlanarQuery
