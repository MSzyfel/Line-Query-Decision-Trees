import PlanarQuery.Model
import Mathlib.Tactic.Linarith

/-! Exact integer-parabola geometry used by the hardness reductions.
The lines are actual `RationalLine` values from the supplied-query model;
`parabolaLineValue` is their left-hand side minus their constant.
Negative values therefore describe the manuscript's membership cap.
The model's Boolean answer is its positive affine sign, so this cap is
its false answer on the off-line hypotheses proved below.
This file proves scalar and line semantics, not a complete reduction,
a finite construction-size bound, or the separate cloud interval formula. -/

namespace PlanarQuery

/-- Integer-indexed points with exact rational coordinates. -/
def integerParabola (t : ℤ) : ℚ × ℚ := ((t : ℚ), (t : ℚ) ^ 2)

/-- Signed evaluation of the actual supplied line equation a*x + b*y = c. -/
def parabolaLineValue (line : RationalLine) (point : ℚ × ℚ) : ℚ :=
  line.a * point.1 + line.b * point.2 - line.c

/-- I_ab: 4*y - 4*(a+b)*x + (2*a-1)*(2*b+1) = 0. -/
def intervalEncoding (a b : ℤ) : RationalLine where
  a := -4 * ((a : ℚ) + (b : ℚ))
  b := 4
  c := -((2 * (a : ℚ) - 1) * (2 * (b : ℚ) + 1))
  nonzero := Or.inr (by norm_num)

/-- P_t: 2*y - 4*t*x + 2*t^2 - 1 = 0. -/
def privateEncoding (t : ℤ) : RationalLine where
  a := -4 * (t : ℚ)
  b := 2
  c := 1 - 2 * (t : ℚ) ^ 2
  nonzero := Or.inr (by norm_num)

/-- The tangent y = 2*t*x - t^2. -/
def tangentEncoding (t : ℤ) : RationalLine where
  a := -2 * (t : ℚ)
  b := 1
  c := -(t : ℚ) ^ 2
  nonzero := Or.inr (by norm_num)

theorem interval_encoding_factor (a b t : ℤ) :
    parabolaLineValue (intervalEncoding a b) (integerParabola t) =
      4 * ((t : ℚ) - (a : ℚ) + 1 / 2) *
        ((t : ℚ) - (b : ℚ) - 1 / 2) := by
  unfold parabolaLineValue intervalEncoding integerParabola
  ring

/-- Integer discreteness excludes half-integer intersections. -/
theorem integer_add_half_nonzero (z : ℤ) : (z : ℚ) + 1 / 2 ≠ 0 := by
  by_cases hz : 0 ≤ z
  · have hr : (0 : ℚ) ≤ (z : ℚ) := by exact_mod_cast hz
    linarith
  · have hi : z ≤ -1 := by omega
    have hr : (z : ℚ) ≤ -1 := by exact_mod_cast hi
    linarith

/-- No integer parabola point lies on I_ab, even without a <= b. -/
theorem interval_encoding_nonzero (a b t : ℤ) :
    parabolaLineValue (intervalEncoding a b) (integerParabola t) ≠ 0 := by
  rw [interval_encoding_factor]
  have hleft : (t : ℚ) - (a : ℚ) + 1 / 2 ≠ 0 := by
    simpa only [Int.cast_sub] using integer_add_half_nonzero (t - a)
  have heq : (t : ℚ) - (b : ℚ) - 1 / 2 =
      ((t - b - 1 : ℤ) : ℚ) + 1 / 2 := by
    simp only [Int.cast_sub, Int.cast_one]
    ring
  have hright : (t : ℚ) - (b : ℚ) - 1 / 2 ≠ 0 := by
    rw [heq]
    exact integer_add_half_nonzero (t - b - 1)
  exact mul_ne_zero (mul_ne_zero (by norm_num) hleft) hright

/-- The supplied negative membership answer selects exactly [a,b]. -/
theorem interval_encoding_negative_iff (a b t : ℤ) (hab : a ≤ b) :
    parabolaLineValue (intervalEncoding a b) (integerParabola t) < 0 ↔
      a ≤ t ∧ t ≤ b := by
  rw [interval_encoding_factor]
  have habq : (a : ℚ) ≤ (b : ℚ) := by exact_mod_cast hab
  constructor
  · intro hnegative
    have hat : a ≤ t := by
      by_contra hnot
      have hi : t + 1 ≤ a := by omega
      have hr : (t : ℚ) + 1 ≤ (a : ℚ) := by exact_mod_cast hi
      have hx : (t : ℚ) - (a : ℚ) + 1 / 2 < 0 := by linarith
      have hy : (t : ℚ) - (b : ℚ) - 1 / 2 < 0 := by linarith
      have hp := mul_pos_of_neg_of_neg hx hy
      nlinarith
    have htb : t ≤ b := by
      by_contra hnot
      have hi : b + 1 ≤ t := by omega
      have hr : (b : ℚ) + 1 ≤ (t : ℚ) := by exact_mod_cast hi
      have hx : 0 < (t : ℚ) - (a : ℚ) + 1 / 2 := by linarith
      have hy : 0 < (t : ℚ) - (b : ℚ) - 1 / 2 := by linarith
      have hp := mul_pos hx hy
      nlinarith
    exact ⟨hat, htb⟩
  · rintro ⟨hat, htb⟩
    have haq : (a : ℚ) ≤ (t : ℚ) := by exact_mod_cast hat
    have htq : (t : ℚ) ≤ (b : ℚ) := by exact_mod_cast htb
    have hx : 0 < (t : ℚ) - (a : ℚ) + 1 / 2 := by linarith
    have hy : (t : ℚ) - (b : ℚ) - 1 / 2 < 0 := by linarith
    have hp := mul_neg_of_pos_of_neg hx hy
    nlinarith

theorem private_encoding_factor (t s : ℤ) :
    parabolaLineValue (privateEncoding t) (integerParabola s) =
      2 * ((s : ℚ) - (t : ℚ)) ^ 2 - 1 := by
  unfold parabolaLineValue privateEncoding integerParabola
  ring

/-- Distinct integer indices have squared rational distance at least one. -/
theorem integer_difference_sq_ge_one (s t : ℤ) (hne : s ≠ t) :
    1 ≤ ((s : ℚ) - (t : ℚ)) ^ 2 := by
  rcases lt_or_gt_of_ne hne with hlt | hgt
  · have hi : s + 1 ≤ t := by omega
    have hr : (s : ℚ) + 1 ≤ (t : ℚ) := by exact_mod_cast hi
    nlinarith [sq_nonneg ((s : ℚ) - (t : ℚ) + 1)]
  · have hi : t + 1 ≤ s := by omega
    have hr : (t : ℚ) + 1 ≤ (s : ℚ) := by exact_mod_cast hi
    nlinarith [sq_nonneg ((s : ℚ) - (t : ℚ) - 1)]

theorem private_encoding_positive_of_ne (t s : ℤ) (hne : s ≠ t) :
    0 < parabolaLineValue (privateEncoding t) (integerParabola s) := by
  rw [private_encoding_factor]
  have hsq := integer_difference_sq_ge_one s t hne
  linarith

/-- A private query's negative answer is exactly its designated point. -/
theorem private_encoding_negative_iff (t s : ℤ) :
    parabolaLineValue (privateEncoding t) (integerParabola s) < 0 ↔ s = t := by
  constructor
  · intro hn
    by_contra hne
    have hp := private_encoding_positive_of_ne t s hne
    linarith
  · intro he
    subst s
    rw [private_encoding_factor]
    norm_num

theorem private_encoding_nonzero (t s : ℤ) :
    parabolaLineValue (privateEncoding t) (integerParabola s) ≠ 0 := by
  by_cases he : s = t
  · subst s
    rw [private_encoding_factor]
    norm_num
  · exact ne_of_gt (private_encoding_positive_of_ne t s he)

theorem tangent_encoding_factor (t s : ℤ) :
    parabolaLineValue (tangentEncoding t) (integerParabola s) =
      ((s : ℚ) - (t : ℚ)) ^ 2 := by
  unfold parabolaLineValue tangentEncoding integerParabola
  ring

/-- The tangent contains its point, and every other integer parabola point
lies strictly on its positive side. This is the exposure certificate. -/
theorem tangent_encoding_exposes (t : ℤ) :
    parabolaLineValue (tangentEncoding t) (integerParabola t) = 0 ∧
      ∀ s : ℤ, s ≠ t →
        0 < parabolaLineValue (tangentEncoding t) (integerParabola s) := by
  constructor
  · rw [tangent_encoding_factor]
    simp
  · intro s hne
    rw [tangent_encoding_factor]
    exact lt_of_lt_of_le (by norm_num : (0 : ℚ) < 1)
      (integer_difference_sq_ge_one s t hne)

/-- The exact off-line condition required by `PlanarInstance.offLine`. -/
theorem interval_encoding_offLine (a b t : ℤ) :
    (intervalEncoding a b).a * (integerParabola t).1 +
      (intervalEncoding a b).b * (integerParabola t).2 ≠
        (intervalEncoding a b).c := by
  intro he
  apply interval_encoding_nonzero a b t
  unfold parabolaLineValue
  rw [he]
  ring

/-- Private singleton lines also satisfy the actual model's off-line condition. -/
theorem private_encoding_offLine (t s : ℤ) :
    (privateEncoding t).a * (integerParabola s).1 +
      (privateEncoding t).b * (integerParabola s).2 ≠
        (privateEncoding t).c := by
  intro he
  apply private_encoding_nonzero t s
  unfold parabolaLineValue
  rw [he]
  ring

end PlanarQuery