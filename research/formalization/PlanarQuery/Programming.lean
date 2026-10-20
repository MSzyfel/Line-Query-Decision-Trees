import Mathlib.Data.Real.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic.Ring

namespace PlanarQuery

/-- Finite LP weak duality, with every sign and feasibility assumption
    present in the statement. This verifies the general certificate rule;
    it does not claim that a particular algorithmic relaxation is integral. -/
theorem linear_program_weak_duality {I J : Type*} [Fintype I] [Fintype J]
    (matrix : I → J → ℝ) (rhs : I → ℝ) (cost : J → ℝ)
    (primal : J → ℝ) (dual : I → ℝ)
    (hprimal : ∀ j, 0 ≤ primal j) (hdual : ∀ i, 0 ≤ dual i)
    (hcover : ∀ i, rhs i ≤ ∑ j, matrix i j * primal j)
    (hbudget : ∀ j, (∑ i, dual i * matrix i j) ≤ cost j) :
    (∑ i, dual i * rhs i) ≤ ∑ j, cost j * primal j := by
  calc
    (∑ i, dual i * rhs i)
        ≤ ∑ i, dual i * (∑ j, matrix i j * primal j) := by
      exact Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (hcover i) (hdual i)
    _ = ∑ j, (∑ i, dual i * matrix i j) * primal j := by
      simp only [Finset.mul_sum, Finset.sum_mul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro j hj
      apply Finset.sum_congr rfl
      intro i hi
      ring
    _ ≤ ∑ j, cost j * primal j := by
      exact Finset.sum_le_sum fun j _ =>
        mul_le_mul_of_nonneg_right (hbudget j) (hprimal j)

/-- Averaging any finite family of certified schedules preserves the
    bound. It is legitimate to select the cheapest actual schedule after
    using this mixture only in the proof. -/
theorem finite_mixture_bound {I : Type*} [Fintype I]
    (probability cost : I → ℝ) (bound : ℝ)
    (hp : ∀ i, 0 ≤ probability i) (hsum : ∑ i, probability i = 1)
    (hcost : ∀ i, cost i ≤ bound) :
    (∑ i, probability i * cost i) ≤ bound := by
  calc
    (∑ i, probability i * cost i) ≤ ∑ i, probability i * bound := by
      exact Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (hcost i) (hp i)
    _ = bound := by rw [← Finset.sum_mul, hsum, one_mul]

theorem minimum_below_mixture {I : Type*} [Fintype I]
    (probability cost : I → ℝ) (chosen : I)
    (hp : ∀ i, 0 ≤ probability i) (hsum : ∑ i, probability i = 1)
    (hmin : ∀ i, cost chosen ≤ cost i) :
    cost chosen ≤ ∑ i, probability i * cost i := by
  calc
    cost chosen = ∑ i, probability i * cost chosen := by
      rw [← Finset.sum_mul, hsum, one_mul]
    _ ≤ ∑ i, probability i * cost i := by
      exact Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (hmin i) (hp i)

end PlanarQuery
