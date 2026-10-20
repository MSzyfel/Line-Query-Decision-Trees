import Mathlib.Tactic

/-! Arithmetic behind the quadratic contribution to the calibrated
expected-depth threshold.  The first theorem records the exact source of the
factor `p(p-1)B^2`; the second turns it into a parameterized fourth-degree
bound. -/

namespace PlanarQuery

/-- If the source total is `s = pB`, then the square of the total decomposes
into the reference square `p B^2` and the imbalance coefficient
`p(p-1)B^2`.  This is the natural-number form of
`s^2 - p B^2 = p(p-1)B^2`, avoiding subtraction until its nonnegativity
has been established. -/
theorem three_partition_square_decomposition
    (p B s : ℕ) (hp : 1 ≤ p) (h : p * B = s) :
    s ^ 2 = p * B ^ 2 + p * (p - 1) * B ^ 2 := by
  let k := p - 1
  have hk : k + 1 = p := by
    dsimp [k]
    omega
  have hkm : p - 1 = k := by
    dsimp [k]
  rw [← h]
  rw [hkm]
  rw [← hk]
  ring

/-- The quadratic coefficient is at most `s^2`.  This is precisely the
nonnegative magnitude of the difference between the two reference terms. -/
theorem three_partition_quadratic_coefficient_le
    (p B s : ℕ) (hp : 1 ≤ p) (h : p * B = s) :
    p * (p - 1) * B ^ 2 ≤ s ^ 2 := by
  have hdecomp := three_partition_square_decomposition p B s hp h
  omega

/-- Parameterized `O(n^4)` estimate for the absolute quadratic threshold
term. If `pB=s<n` and `V≤c n²`, then
`(V * p(p-1)B²)/2 ≤ c n⁴`. The division by two can only decrease the
nonnegative numerator; the coefficient bound supplies the two remaining
factors of `n`. -/
theorem three_partition_quadratic_threshold_le_fourth
    (p B s n c V : ℕ)
    (hpB : p * B = s) (hp : 2 ≤ p) (hs : s < n)
    (hV : V ≤ c * n ^ 2) :
    (V * (p * (p - 1) * B ^ 2)) / 2 ≤ c * n ^ 4 := by
  have hcoef : p * (p - 1) * B ^ 2 ≤ s ^ 2 :=
    three_partition_quadratic_coefficient_le p B s (by omega) hpB
  have hsq : s ^ 2 ≤ n ^ 2 := by
    exact Nat.pow_le_pow_left (Nat.le_of_lt hs) 2
  have hnum : V * (p * (p - 1) * B ^ 2) ≤ (c * n ^ 2) * n ^ 2 := by
    calc
      V * (p * (p - 1) * B ^ 2) ≤ (c * n ^ 2) * (s ^ 2) :=
        Nat.mul_le_mul hV hcoef
      _ ≤ (c * n ^ 2) * n ^ 2 :=
        Nat.mul_le_mul_left (c * n ^ 2) hsq
  calc
    (V * (p * (p - 1) * B ^ 2)) / 2
        ≤ V * (p * (p - 1) * B ^ 2) := Nat.div_le_self _ _
    _ ≤ (c * n ^ 2) * n ^ 2 := hnum
    _ = c * n ^ 4 := by ring

/-- The `p≥2` hypothesis used by the manuscript also makes the difference
between `s²` and `pB²` an ordinary nonnegative natural number. -/
theorem three_partition_reference_term_le_total
    (p B s : ℕ) (hp : 2 ≤ p) (h : p * B = s) :
    p * B ^ 2 ≤ s ^ 2 := by
  have hdecomp := three_partition_square_decomposition p B s (by omega) h
  omega

end PlanarQuery
