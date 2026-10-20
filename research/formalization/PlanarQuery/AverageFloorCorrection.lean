import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

/-! Floor-division error bounds used in the expected-depth reduction.

For a nonnegative integer `n` and a positive integer `t`, the quotient
`n / t` rounds down.  The difference between `t * (n / t)` and `n` is the
negative remainder, so its magnitude is at most `t - 1`.  The finite-sum
version records the corresponding accumulated correction term. -/

namespace PlanarQuery

open Finset

/-- The error from replacing `n` by the largest multiple of `t` below it is
exactly the negative remainder.  This identity makes the floor correction
explicit before we use its bounds. -/
theorem nat_floor_multiple_error_eq_neg_remainder
    (n t : ℕ) :
    (t : ℤ) * ((n / t : ℕ) : ℤ) - (n : ℤ) = -((n % t : ℕ) : ℤ) := by
  have hcast : n % t + t * (n / t) = n := Nat.mod_add_div n t
  have hcastInt : ((n % t : ℕ) : ℤ) +
      (t : ℤ) * ((n / t : ℕ) : ℤ) = (n : ℤ) := by
    exact_mod_cast hcast
  rw [← hcastInt]
  ring

/-- For positive `t`, the floor-multiple error lies between `-(t - 1)` and
zero.  The lower bound follows from the remainder being smaller than `t`;
the upper bound follows because the quotient rounds down. -/
theorem nat_floor_multiple_error_bounds
    (n t : ℕ) (ht : 0 < t) :
    -((t - 1 : ℕ) : ℤ) ≤
        (t : ℤ) * ((n / t : ℕ) : ℤ) - (n : ℤ) ∧
      (t : ℤ) * ((n / t : ℕ) : ℤ) - (n : ℤ) ≤ 0 := by
  rw [nat_floor_multiple_error_eq_neg_remainder n t]
  constructor
  · have hrem : n % t < t := Nat.mod_lt n ht
    have hrem' : n % t ≤ t - 1 := by omega
    exact neg_le_neg (by exact_mod_cast hrem')
  · exact neg_nonpos.mpr (by exact_mod_cast (Nat.zero_le (n % t)))

/-- Summing floor-multiple errors over a finite family adds the individual
`tᵢ - 1` bounds.  Each summand is controlled by
`nat_floor_multiple_error_bounds`, and finite-sum monotonicity preserves both
inequalities. -/
theorem sum_nat_floor_multiple_error_bounds
    {ι : Type*} (s : Finset ι) (n t : ι → ℕ)
    (ht : ∀ i ∈ s, 0 < t i) :
    - (∑ i ∈ s, ((t i - 1 : ℕ) : ℤ)) ≤
        (∑ i ∈ s,
          ((t i : ℤ) * ((n i / t i : ℕ) : ℤ) - (n i : ℤ))) ∧
      (∑ i ∈ s,
        ((t i : ℤ) * ((n i / t i : ℕ) : ℤ) - (n i : ℤ))) ≤ 0 := by
  constructor
  · have hpoint : ∀ i ∈ s,
        -((t i - 1 : ℕ) : ℤ) ≤
          (t i : ℤ) * ((n i / t i : ℕ) : ℤ) - (n i : ℤ) := by
      intro i hi
      exact (nat_floor_multiple_error_bounds (n i) (t i) (ht i hi)).1
    have hsum := Finset.sum_le_sum hpoint
    simpa only [Finset.sum_neg_distrib] using hsum
  · have hpoint : ∀ i ∈ s,
        (t i : ℤ) * ((n i / t i : ℕ) : ℤ) - (n i : ℤ) ≤ 0 := by
      intro i hi
      exact (nat_floor_multiple_error_bounds (n i) (t i) (ht i hi)).2
    have hsum := Finset.sum_le_sum hpoint
    simpa using hsum

end PlanarQuery
