import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

/-! Finite-sum arithmetic for the expected-depth pair-perturbation error.

The geometric construction supplies a uniform bound on each correction.
This module isolates the arithmetic that turns that pointwise estimate into
the aggregate estimate used in the threshold gap. -/

namespace PlanarQuery

open Finset

/-- The aggregate pair-perturbation allowance, with `m` items and `p` bins. -/
def expectedDepthEplus (m p q : ℕ) (δ : ℕ → ℕ → ℕ) : ℕ :=
  q * (∑ i ∈ Finset.range m, ∑ b ∈ Finset.range p, δ i b)

/-- A uniform bound on every correction bounds their finite sum by the number
of item-bin pairs times that bound. The factor `q` is then the rank multiplier
in the pair-completion perturbation estimate. -/
theorem expected_depth_Eplus_le_of_pointwise
    (m p q D : ℕ) (δ : ℕ → ℕ → ℕ)
    (hδ : ∀ i < m, ∀ b < p, δ i b ≤ D) :
    expectedDepthEplus m p q δ ≤ (q * m * p) * D := by
  have hbin : ∀ i ∈ Finset.range m,
      (∑ b ∈ Finset.range p, δ i b) ≤ p * D := by
    intro i hi
    calc
      (∑ b ∈ Finset.range p, δ i b)
          ≤ ∑ _b ∈ Finset.range p, D := by
              apply Finset.sum_le_sum
              intro b hb
              exact hδ i (Finset.mem_range.mp hi) b (Finset.mem_range.mp hb)
      _ = p * D := by simp
  have hsum :
      (∑ i ∈ Finset.range m, ∑ b ∈ Finset.range p, δ i b)
        ≤ m * (p * D) := by
    calc
      (∑ i ∈ Finset.range m, ∑ b ∈ Finset.range p, δ i b)
          ≤ ∑ _i ∈ Finset.range m, (p * D) := by
              apply Finset.sum_le_sum
              intro i hi
              exact hbin i hi
      _ = m * (p * D) := by simp
  unfold expectedDepthEplus
  have hmul := Nat.mul_le_mul_left q hsum
  calc
    q * (∑ i ∈ Finset.range m, ∑ b ∈ Finset.range p, δ i b)
        ≤ q * (m * (p * D)) := hmul
    _ = (q * m * p) * D := by ring

/-- If every correction is at most the floor scale `V*C/r`, and the chosen
`r` dominates `1000(qmp+2m+1)C`, then the full pair-perturbation allowance is
strictly below `V/1000` (stated without fractions as `1000 Eplus < V`).

The pointwise premise is the per-correction estimate supplied by the
construction; this theorem proves the subsequent finite-sum and scale
arithmetic. -/
theorem expected_depth_Eplus_lt_scale
    (m p q V C r : ℕ) (δ : ℕ → ℕ → ℕ)
    (hm : 0 < m) (hV : 0 < V) (hC : 0 < C)
    (hδ : ∀ i < m, ∀ b < p, δ i b ≤ (V * C) / r)
    (hscale : 1000 * (q * m * p + 2 * m + 1) * C < r) :
    1000 * expectedDepthEplus m p q δ < V := by
  let D : ℕ := (V * C) / r
  let K : ℕ := q * m * p
  have hsum := expected_depth_Eplus_le_of_pointwise m p q D δ (by
    intro i hi b hb
    exact hδ i hi b hb)
  have hE : expectedDepthEplus m p q δ ≤ K * D := by
    simpa [K, D] using hsum
  have hK : K ≤ q * m * p + 2 * m + 1 := by
    dsimp [K]
    omega
  have hKscale : 1000 * K * C < r := by
    have hmul : 1000 * K * C ≤ 1000 * (q * m * p + 2 * m + 1) * C := by
      have hleft : 1000 * K ≤ 1000 * (q * m * p + 2 * m + 1) :=
        Nat.mul_le_mul_left 1000 hK
      have hright := Nat.mul_le_mul_right C hleft
      simpa [Nat.mul_assoc] using hright
    exact lt_of_le_of_lt hmul hscale
  have hquotient : D * r ≤ V * C := by
    dsimp [D]
    exact Nat.div_mul_le_self (V * C) r
  have hscaleD : 1000 * K * D < V := by
    by_cases hD : D = 0
    · simpa [hD] using hV
    · have hDpos : 0 < D := Nat.pos_of_ne_zero hD
      have hmul := Nat.mul_lt_mul_of_pos_right hKscale hDpos
      have hcommon : (1000 * K * D) * C < V * C := by
        calc
          (1000 * K * D) * C = (1000 * K * C) * D := by ring
          _ < r * D := by simpa [Nat.mul_comm] using hmul
          _ = D * r := Nat.mul_comm r D
          _ ≤ V * C := hquotient
      exact (mul_lt_mul_right hC).mp hcommon
  have hfinal : 1000 * expectedDepthEplus m p q δ ≤ 1000 * (K * D) :=
    Nat.mul_le_mul_left 1000 hE
  calc
    1000 * expectedDepthEplus m p q δ ≤ 1000 * (K * D) := hfinal
    _ = 1000 * K * D := by ring
    _ < V := hscaleD

end PlanarQuery
