import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Lean.Elab.Tactic.Omega

namespace PlanarQuery

/-! Reduction transfer is kept distinct from proving a reduction or
    NP-hardness. These theorems validate only the stated exact identities. -/

theorem exact_additive_threshold (source target overhead threshold : ℝ)
    (hidentity : target = source + overhead) :
    target ≤ threshold + overhead ↔ source ≤ threshold := by
  rw [hidentity]
  exact add_le_add_iff_right overhead

theorem uniform_cloud_threshold (n weightedOpt uniformOpt overhead threshold : ℝ)
    (hn : 0 < n) (hidentity : n * uniformOpt = weightedOpt + overhead) :
    uniformOpt ≤ (threshold + overhead) / n ↔ weightedOpt ≤ threshold := by
  rw [le_div_iff₀ hn]
  rw [mul_comm uniformOpt n, hidentity]
  exact add_le_add_iff_right overhead

/-- Adding the same nonnegative local invoice preserves an approximation
    factor. This explains why the exact cloud lift alone creates no gap. -/
theorem additive_lift_preserves_ratio (cost optimum overhead factor : ℝ)
    (hfactor : 1 ≤ factor) (hoverhead : 0 ≤ overhead)
    (hcost : cost ≤ factor * optimum) :
    cost + overhead ≤ factor * (optimum + overhead) := by
  have h := mul_nonneg (sub_nonneg.mpr hfactor) hoverhead
  nlinarith

def singletonCloudCost (n : ℕ) : ℕ := n * (n + 1) / 2 - 1

theorem singletonCloudCost_one : singletonCloudCost 1 = 0 := by decide

theorem singletonCloudCost_two : singletonCloudCost 2 = 2 := by decide

/-- A nonzero integral zero-sum load deviation has quadratic cost at least
    two. The histogram reduction and its error budget are separate inputs. -/
theorem integer_zero_sum_gap {I : Type*} [Fintype I] [DecidableEq I]
    (deviation : I → ℤ) (hsum : ∑ i, deviation i = 0)
    (hne : ∃ i, deviation i ≠ 0) :
    2 ≤ ∑ i, (deviation i) ^ 2 := by
  classical
  have hpos : ∃ i, 0 < deviation i := by
    apply Classical.byContradiction
    intro hn
    have hall : ∀ i, deviation i ≤ 0 := fun i =>
      le_of_not_gt ((not_exists.mp hn) i)
    obtain ⟨j, hj⟩ := hne
    have hsingle : -deviation j ≤ ∑ i, -deviation i :=
      Finset.single_le_sum (fun i _ => neg_nonneg.mpr (hall i)) (Finset.mem_univ j)
    rw [Finset.sum_neg_distrib, hsum, neg_zero] at hsingle
    have hjnonpos := hall j
    omega
  obtain ⟨i, hi⟩ := hpos
  have hneg : ∃ j, deviation j < 0 := by
    apply Classical.byContradiction
    intro hn
    have hall : ∀ j, 0 ≤ deviation j := fun j =>
      le_of_not_gt ((not_exists.mp hn) j)
    have hsingle : deviation i ≤ ∑ j, deviation j :=
      Finset.single_le_sum (fun j _ => hall j) (Finset.mem_univ i)
    rw [hsum] at hsingle
    omega
  obtain ⟨j, hj⟩ := hneg
  have hij : i ≠ j := by intro h; subst j; omega
  have hsquareI : 1 ≤ (deviation i) ^ 2 := by
    have : 1 ≤ deviation i := by omega
    nlinarith
  have hsquareJ : 1 ≤ (deviation j) ^ 2 := by
    have : deviation j ≤ -1 := by omega
    nlinarith
  have hsub : ({i, j} : Finset I) ⊆ Finset.univ := fun _ _ => Finset.mem_univ _
  have hpair : (deviation i) ^ 2 + (deviation j) ^ 2 ≤ ∑ k, (deviation k) ^ 2 := by
    have h := Finset.sum_le_sum_of_subset_of_nonneg hsub
      (fun k _ _ => sq_nonneg (deviation k))
    simpa [Finset.sum_pair hij] using h
  omega

end PlanarQuery
