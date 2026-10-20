import PlanarQuery.Reduction
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

/-! Exact finite-sum algebra used in the expected-depth reduction.

These theorems formalize the load-deviation calculation and its integral
gap. They do not assume or prove the geometric histogram identity, the
invoice representation, or the scale bounds used by the manuscript. -/

namespace PlanarQuery

/-- If the total load is `|I| * B`, then the deviations from `B` sum to zero. -/
theorem load_deviations_sum_zero {I : Type*} [Fintype I] [DecidableEq I]
    (load : I → ℤ) (B : ℤ)
    (htotal : ∑ i, load i = (Fintype.card I : ℤ) * B) :
    ∑ i, (load i - B) = 0 := by
  classical
  have hconst : (∑ _i : I, B) = (Fintype.card I : ℤ) * B := by
    simp [nsmul_eq_mul]
  rw [Finset.sum_sub_distrib, htotal, hconst]
  ring

/-- Expanding the squared deviations exposes the load-square term.

The hypothesis supplies the total-load identity; the theorem records every
algebraic contribution, including the constant term from all `|I|` bins. -/
theorem load_deviation_square_identity {I : Type*} [Fintype I] [DecidableEq I]
    (load : I → ℤ) (B : ℤ)
    (htotal : ∑ i, load i = (Fintype.card I : ℤ) * B) :
    (∑ i, (load i - B) ^ 2) =
      (∑ i, (load i) ^ 2) - (Fintype.card I : ℤ) * B ^ 2 := by
  classical
  have hconst : (∑ _i : I, B ^ 2) = (Fintype.card I : ℤ) * B ^ 2 := by
    simp [nsmul_eq_mul]
  calc
    (∑ i, (load i - B) ^ 2)
        = (∑ i, ((load i) ^ 2 - 2 * B * load i + B ^ 2)) := by
            apply Finset.sum_congr rfl
            intro i hi
            ring
    _ = (∑ i, (load i) ^ 2) -
          (2 * B) * (∑ i, load i) + (∑ _i : I, B ^ 2) := by
            simp only [Finset.sum_sub_distrib, Finset.sum_add_distrib,
              ← Finset.mul_sum]
    _ = (∑ i, (load i) ^ 2) -
          (2 * B) * ((Fintype.card I : ℤ) * B) +
          (Fintype.card I : ℤ) * B ^ 2 := by rw [htotal, hconst]
    _ = (∑ i, (load i) ^ 2) - (Fintype.card I : ℤ) * B ^ 2 := by ring

/-- Any non-balanced integral load vector has squared deviation at least two.

This is the load-level arithmetic gap used before the manuscript's separate
error-budget comparison. -/
theorem unbalanced_load_square_gap {I : Type*} [Fintype I] [DecidableEq I]
    (load : I → ℤ) (B : ℤ)
    (htotal : ∑ i, load i = (Fintype.card I : ℤ) * B)
    (hunbalanced : ∃ i, load i ≠ B) :
    2 ≤ ∑ i, (load i - B) ^ 2 := by
  apply integer_zero_sum_gap (fun i ↦ load i - B)
  · exact load_deviations_sum_zero load B htotal
  · obtain ⟨i, hi⟩ := hunbalanced
    exact ⟨i, by omega⟩

/-- Zero quadratic deviation forces every integral load to equal the baseline. -/
theorem zero_load_deviation_iff_balanced {I : Type*} [Fintype I] [DecidableEq I]
    (load : I → ℤ) (B : ℤ) :
    (∑ i, (load i - B) ^ 2 = 0) ↔ (∀ i, load i = B) := by
  constructor
  · intro hzero i
    have hnonneg : ∀ j, 0 ≤ (load j - B) ^ 2 := fun j => sq_nonneg _
    have hsingle : (load i - B) ^ 2 ≤ ∑ j, (load j - B) ^ 2 :=
      Finset.single_le_sum (fun j _ => hnonneg j) (Finset.mem_univ i)
    rw [hzero] at hsingle
    have hdiff : load i - B = 0 := by nlinarith
    omega
  · intro hbalanced
    simp [hbalanced]

/-- The manuscript's two scale bounds separate the imbalance penalty from
the accumulated error: `V - Eminus` exceeds `Eplus`. -/
theorem load_gap_exceeds_error_budget
    (V Eminus Eplus baseline : ℚ)
    (hV : 0 < V) (hminus : Eminus < V / 2000)
    (hplus : Eplus ≤ V / 1000) :
    baseline + V - Eminus > baseline + Eplus := by
  have hremaining : (1999 : ℚ) / 2000 * V < V - Eminus := by
    nlinarith
  have hseparation : (V / 1000 : ℚ) < (1999 : ℚ) / 2000 * V := by
    nlinarith
  linarith

/-- Once the integral variance is at least two, the paper's error bounds
force the unbalanced invoice strictly above the balanced threshold. -/
theorem unbalanced_invoice_exceeds_threshold
    (V Eminus Eplus baseline variance error : ℚ)
    (hV : 0 < V) (hminus : Eminus < V / 2000)
    (hplus : Eplus ≤ V / 1000) (hvariance : 2 ≤ variance)
    (herror : -Eminus ≤ error) :
    baseline + (V / 2) * variance + error > baseline + Eplus := by
  have hgap := load_gap_exceeds_error_budget V Eminus Eplus baseline hV hminus hplus
  have hpenalty : V ≤ (V / 2) * variance := by nlinarith
  linarith

/-- A balanced load profile stays within the threshold when its residual
invoice error is at most the positive error allowance. -/
theorem balanced_invoice_within_threshold
    (V Eplus baseline error : ℚ) (herror : error ≤ Eplus) :
    baseline + (V / 2) * 0 + error ≤ baseline + Eplus := by
  linarith

/-- The weighted completion cost associated with a fixed ordering of the
pair coordinates.  Coordinate `j` has rank `j.val + 1`. -/
def pairOrderCost {q : ℕ} (z : Fin q → ℝ) (σ : Equiv.Perm (Fin q)) : ℝ :=
  ∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * z (σ j)

/-- The optimal weighted completion cost, obtained by minimizing over all
orders of the pair coordinates. -/
noncomputable def pairCompletionCost {q : ℕ} (z : Fin q → ℝ) : ℝ :=
  (Finset.univ.image (pairOrderCost z)).min'
    (Finset.image_nonempty.mpr ⟨Equiv.refl (Fin q), Finset.mem_univ _⟩)

/-- Coordinatewise nonnegative changes cannot lower the minimum weighted
ordering cost, and their increase is bounded by assigning every added mass
the largest possible rank `q`.

This abstract finite statement is the algebraic core of
Claim `clm:average-pair-perturbation`; no geometric assumptions are needed. -/
theorem average_pair_perturbation_bound {q : ℕ}
    (z d : Fin q → ℝ) (hd : ∀ j, 0 ≤ d j) :
    pairCompletionCost z ≤ pairCompletionCost (fun j => z j + d j) ∧
      pairCompletionCost (fun j => z j + d j) ≤
        pairCompletionCost z + (q : ℝ) * ∑ j : Fin q, d j := by
  classical
  let oldCosts := Finset.univ.image (pairOrderCost z)
  let newCosts := Finset.univ.image (pairOrderCost (fun j => z j + d j))
  have hold : oldCosts.Nonempty :=
    Finset.image_nonempty.mpr ⟨Equiv.refl (Fin q), Finset.mem_univ _⟩
  have hnew : newCosts.Nonempty :=
    Finset.image_nonempty.mpr ⟨Equiv.refl (Fin q), Finset.mem_univ _⟩
  have hcost_mono (σ : Equiv.Perm (Fin q)) :
      pairOrderCost z σ ≤ pairOrderCost (fun j => z j + d j) σ := by
    unfold pairOrderCost
    apply Finset.sum_le_sum
    intro j hj
    have hv : z (σ j) ≤ z (σ j) + d (σ j) := le_add_of_nonneg_right (hd (σ j))
    exact mul_le_mul_of_nonneg_left hv (by positivity)
  have hcost_add (σ : Equiv.Perm (Fin q)) :
      pairOrderCost (fun j => z j + d j) σ ≤
        pairOrderCost z σ + (q : ℝ) * ∑ j : Fin q, d j := by
    unfold pairOrderCost
    calc
      (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * (z (σ j) + d (σ j)))
          = (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * z (σ j)) +
              ∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * d (σ j) := by
                simp_rw [mul_add, Finset.sum_add_distrib]
      _ ≤ (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * z (σ j)) +
              ∑ j : Fin q, (q : ℝ) * d (σ j) := by
                gcongr with j
                · exact hd (σ j)
                · exact_mod_cast Nat.succ_le_iff.mpr j.isLt
      _ = (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * z (σ j)) +
              (q : ℝ) * ∑ j : Fin q, d j := by
                congr 1
                rw [← Finset.mul_sum]
                rw [Equiv.sum_comp σ (fun j => d j)]

  constructor
  · have hminnew := Finset.min'_mem newCosts hnew
    rcases Finset.mem_image.mp hminnew with ⟨σ, hσ, hσval⟩
    have holdle : oldCosts.min' hold ≤ pairOrderCost z σ := by
      apply Finset.min'_le
      exact Finset.mem_image.mpr ⟨σ, Finset.mem_univ _, rfl⟩
    have hmono := hcost_mono σ
    rw [hσval] at hmono
    exact holdle.trans hmono
  · have hminold := Finset.min'_mem oldCosts hold
    rcases Finset.mem_image.mp hminold with ⟨σ, hσ, hσval⟩
    have hnewle : newCosts.min' hnew ≤ pairOrderCost (fun j => z j + d j) σ := by
      apply Finset.min'_le
      exact Finset.mem_image.mpr ⟨σ, Finset.mem_univ _, rfl⟩
    have hadd := hcost_add σ
    rw [hσval] at hadd
    exact hnewle.trans hadd

end PlanarQuery
