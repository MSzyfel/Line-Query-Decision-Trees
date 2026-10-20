import PlanarQuery.AverageInvoice
import Mathlib.Tactic

/-! A rank-sum upper bound for the weighted completion cost. -/

namespace PlanarQuery

/-- The sum of the ranks `1, ..., q` is the `q`th triangular number. -/
theorem fin_rank_sum (q : ℕ) :
    (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ)) =
      (q : ℝ) * ((q : ℝ) + 1) / 2 := by
  induction q with
  | zero => simp
  | succ q ih =>
      rw [Fin.sum_univ_castSucc]
      simp only [Fin.coe_castSucc, Fin.val_last]
      rw [ih]
      push_cast
      ring

/-- If every coordinate is bounded above by `M`, then the
minimum weighted completion cost is at most the cost of assigning ranks
`1, ..., q` in the identity order, and that cost is at most the triangular
rank sum times `M`. -/
theorem pair_completion_cost_le_triangular_bound {q : ℕ}
    (z : Fin q → ℝ) (M : ℝ)
    (hz : ∀ j, z j ≤ M) :
    pairCompletionCost z ≤ M * (q : ℝ) * ((q : ℝ) + 1) / 2 := by
  classical
  let costs := Finset.univ.image (pairOrderCost z)
  have hcosts : costs.Nonempty :=
    Finset.image_nonempty.mpr ⟨Equiv.refl (Fin q), Finset.mem_univ _⟩
  have hidentity_mem : pairOrderCost z (Equiv.refl (Fin q)) ∈ costs := by
    exact Finset.mem_image.mpr
      ⟨Equiv.refl (Fin q), Finset.mem_univ _, rfl⟩
  have hminimum_le_identity :
      pairCompletionCost z ≤ pairOrderCost z (Equiv.refl (Fin q)) := by
    unfold pairCompletionCost
    exact Finset.min'_le costs (pairOrderCost z (Equiv.refl (Fin q)))
      hidentity_mem
  have hidentity_bound :
      pairOrderCost z (Equiv.refl (Fin q)) ≤
        M * (q : ℝ) * ((q : ℝ) + 1) / 2 := by
    unfold pairOrderCost
    calc
      (∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * z (Equiv.refl (Fin q) j))
          ≤ ∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) * M := by
              apply Finset.sum_le_sum
              intro j hj
              apply mul_le_mul_of_nonneg_left (hz j)
              positivity
      _ = ∑ j : Fin q, M * ((j.val + 1 : ℕ) : ℝ) := by
            apply Finset.sum_congr rfl
            intro j hj
            ring
      _ = M * ∑ j : Fin q, ((j.val + 1 : ℕ) : ℝ) := by
            rw [Finset.mul_sum]
      _ = M * (q : ℝ) * ((q : ℝ) + 1) / 2 := by
            rw [fin_rank_sum]
            ring
  exact hminimum_le_identity.trans hidentity_bound

end PlanarQuery
