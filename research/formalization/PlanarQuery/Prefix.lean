import PlanarQuery.Model

namespace PlanarQuery
namespace Tree

variable {H Q : Type*} [DecidableEq H]

def prefixCost (M : QuerySystem H Q) (weight : H → ℚ)
    (S : Finset H) (T : Tree H Q) (k : ℕ) : ℚ :=
  ∑ h ∈ S, weight h * (min k (depth M T h) : ℕ)

def suffixCost (M : QuerySystem H Q) (weight : H → ℚ)
    (S : Finset H) (T : Tree H Q) (k : ℕ) : ℚ :=
  ∑ h ∈ S, weight h * (depth M T h - k : ℕ)

def frontier (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (k : ℕ) : Finset H :=
  S.filter (fun h => k ≤ depth M T h)

/-- This is an identity on actual per-hypothesis tree depths, including
    leaves reached before the lookahead horizon. -/
theorem prefix_suffix_decomposition (M : QuerySystem H Q) (weight : H → ℚ)
    (S : Finset H) (T : Tree H Q) (k : ℕ) :
    prefixCost M weight S T k + suffixCost M weight S T k =
      rawExpected M weight S T := by
  unfold prefixCost suffixCost rawExpected
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro h hh
  have hsplit : min k (depth M T h) + (depth M T h - k) = depth M T h := by omega
  rw [← mul_add, ← Nat.cast_add, hsplit]

/-- The prefix pays k times the entire surviving mass, for arbitrary
    nonnegative rational weights. No minimum-prior premise occurs. -/
theorem prefix_pays_frontier (M : QuerySystem H Q) (weight : H → ℚ)
    (hw : ∀ h, 0 ≤ weight h) (S : Finset H) (T : Tree H Q) (k : ℕ) :
    (k : ℚ) * mass weight (frontier M S T k) ≤ prefixCost M weight S T k := by
  unfold mass frontier prefixCost
  rw [Finset.sum_filter, Finset.mul_sum]
  apply Finset.sum_le_sum
  intro h hh
  by_cases hk : k ≤ depth M T h
  · simp only [hk, if_true, Nat.min_eq_left hk]
    exact le_of_eq (mul_comm _ _)
  · simp only [hk, if_false, mul_zero]
    exact mul_nonneg (hw h) (Nat.cast_nonneg _)

end Tree
end PlanarQuery
