import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

/-! Concrete natural-number estimates for the expected-depth reduction's
scale calibration.  These lemmas derive the scale comparisons from the
chosen value of `V`; they do not assume the resulting bounds. -/

namespace PlanarQuery

open Finset

/-- The accumulated error term used in the expected-depth construction. -/
def expectedDepthEminus (m q r : ℕ) : ℕ :=
  ∑ i ∈ Finset.range m, (q + r + m - i - 2)

/-- Dividing the calibrated scale by `2000` recovers its basic product. -/
theorem expected_depth_scale_div
    {m q r V : ℕ}
    (hV : V = 2000 * m * (r + q + m + 1)) :
    m * (r + q + m + 1) = V / 2000 := by
  rw [hV, Nat.mul_assoc]
  symm
  exact Nat.mul_div_cancel_left _ (by norm_num)

/-- The calibrated product is large enough to dominate the number of bins
plus one.  The factor `r + q + m + 1` is at least `m + 1`, and the positive
integer `m` is at least one, so multiplying by `m` can only increase it. -/
theorem expected_depth_scale_dominates_bins
    {m q r V : ℕ} (hm : 0 < m) (hq : 0 < q) (hr : 0 < r)
    (hV : V = 2000 * m * (r + q + m + 1)) :
    m + 1 ≤ V / 2000 := by
  rw [← expected_depth_scale_div hV]
  have hm1 : 1 ≤ m := by omega
  have hfactor : m + 1 ≤ r + q + m + 1 := by omega
  have hfactor_le_product : r + q + m + 1 ≤ m * (r + q + m + 1) := by
    calc
      r + q + m + 1 = 1 * (r + q + m + 1) := by simp
      _ ≤ m * (r + q + m + 1) := Nat.mul_le_mul_right _ hm1
  exact hfactor.trans hfactor_le_product

/-- The total accumulated error is strictly below `V / 2000`.  Each of the
`m` summands is at most `q + r + m`; summing gives at most
`m * (q + r + m)`.  Since `m > 0`, adding one to the second factor makes
`m * (r + q + m + 1)` strictly larger. -/
theorem expected_depth_eminus_lt_scale_div
    {m q r V : ℕ} (hm : 0 < m) (hq : 0 < q) (hr : 0 < r)
    (hV : V = 2000 * m * (r + q + m + 1)) :
    expectedDepthEminus m q r < V / 2000 := by
  rw [← expected_depth_scale_div hV]
  unfold expectedDepthEminus
  have hsum :
      (∑ i ∈ Finset.range m, (q + r + m - i - 2)) ≤
        ∑ _i ∈ Finset.range m, (q + r + m) := by
    apply Finset.sum_le_sum
    intro i hi
    have hi_lt : i < m := Finset.mem_range.mp hi
    omega
  have hconstant_sum :
      (∑ _i ∈ Finset.range m, (q + r + m)) = m * (q + r + m) := by
    simp [nsmul_eq_mul]
  have hstrict :
      m * (q + r + m) < m * (r + q + m + 1) := by
    apply Nat.mul_lt_mul_of_pos_left
    · omega
    · exact hm
  exact lt_of_le_of_lt (hsum.trans_eq hconstant_sum) hstrict

end PlanarQuery
