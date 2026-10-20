import PlanarQuery.EntropyInequalities
import PlanarQuery.Randomized

/-! The uniform-prior lower bound is obtained from the entropy of actual
identifying trees. It then passes to finite legal mixtures, allowing trees
with zero mixture probability to be arbitrary. -/

namespace PlanarQuery.Entropy

variable {H Q : Type*} [DecidableEq H]

noncomputable def uniformWeight (S : Finset H) (_h : H) : ℝ :=
  1 / (S.card : ℝ)

omit [DecidableEq H] in
theorem uniformWeight_nonneg (S : Finset H) (h : H) :
    0 ≤ uniformWeight S h := by
  unfold uniformWeight
  positivity

omit [DecidableEq H] in
theorem uniformWeight_mass (S : Finset H) (hS : S.Nonempty) :
    mass (uniformWeight S) S = 1 := by
  have hc : (S.card : ℝ) ≠ 0 := ne_of_gt
    (Nat.cast_pos.mpr (Finset.card_pos.mpr hS))
  simp [mass, uniformWeight, hc]

omit [DecidableEq H] in
/-- Uniform entropy is exactly the natural logarithm of the live state size. -/
theorem uniformWeight_entropy (S : Finset H) (hS : S.Nonempty) :
    weighted (uniformWeight S) S = Real.log (S.card : ℝ) := by
  rw [weighted_eq_log_ratio _ S (fun h _ => uniformWeight_nonneg S h),
    uniformWeight_mass S hS]
  simp only [uniformWeight, one_div_one_div]
  rw [← Finset.sum_mul]
  have hc : (S.card : ℝ) ≠ 0 := ne_of_gt
    (Nat.cast_pos.mpr (Finset.card_pos.mpr hS))
  simp [hc]

omit [DecidableEq H] in
theorem uniformWeight_expected_eq_average (M : QuerySystem H Q)
    (S : Finset H) (T : Tree H Q) :
    expected M (uniformWeight S) S T =
      (∑ h ∈ S, (Tree.depth M T h : ℝ)) / (S.card : ℝ) := by
  unfold expected uniformWeight
  simp_rw [one_div, inv_mul_eq_div]
  exact (Finset.sum_div S (fun h => (Tree.depth M T h : ℝ)) (S.card : ℝ)).symm

/-- This invokes the proved Kraft/log-sum bound on the identifying tree's
actual transcripts, rather than assuming an information lower bound. -/
theorem uniform_identifying_tree_entropy_lower_bound (M : QuerySystem H Q)
    (S : Finset H) (T : Tree H Q) (hS : S.Nonempty)
    (hId : Tree.Identifies M S T) :
    Real.log (S.card : ℝ) / Real.log 2 ≤ expected M (uniformWeight S) S T := by
  have h := identifying_tree_entropy_lower_bound_via_kraft M (uniformWeight S) S T
    (fun h _ => uniformWeight_nonneg S h) (uniformWeight_mass S hS) hId
  simpa only [uniformWeight_entropy S hS] using h

theorem uniform_identifying_tree_average_lower_bound (M : QuerySystem H Q)
    (S : Finset H) (T : Tree H Q) (hS : S.Nonempty)
    (hId : Tree.Identifies M S T) :
    Real.log (S.card : ℝ) / Real.log 2 ≤
      (∑ h ∈ S, (Tree.depth M T h : ℝ)) / (S.card : ℝ) := by
  rw [← uniformWeight_expected_eq_average M S T]
  exact uniform_identifying_tree_entropy_lower_bound M S T hS hId

end PlanarQuery.Entropy

namespace PlanarQuery

open Entropy

/-- The uniform average of every finite legal mixture is at least log₂ n.
Only positive-probability trees are required to identify the state. -/
theorem legal_mixture_uniform_average_lower_bound {H Q I : Type*}
    [Fintype H] [Fintype I] [DecidableEq H]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ)
    (hcard : 0 < Fintype.card H)
    (hmix : LegalMixture M Finset.univ trees probability) :
    Real.log (Fintype.card H : ℝ) / Real.log 2 ≤
      ∑ i, probability i * expected M (uniformWeight Finset.univ) Finset.univ (trees i) := by
  classical
  have hS : (Finset.univ : Finset H).Nonempty :=
    Finset.card_pos.mp (by simpa only [Finset.card_univ] using hcard)
  calc
    _ = ∑ i, probability i * (Real.log (Fintype.card H : ℝ) / Real.log 2) := by
      rw [← Finset.sum_mul, hmix.2.1, one_mul]
    _ ≤ _ := by
      apply Finset.sum_le_sum
      intro i hi
      by_cases hp : 0 < probability i
      · have h := uniform_identifying_tree_entropy_lower_bound M Finset.univ (trees i)
          hS (hmix.2.2 i hp)
        simp only [Finset.card_univ] at h
        exact mul_le_mul_of_nonneg_left h (hmix.1 i)
      · have hz : probability i = 0 := le_antisymm (le_of_not_gt hp) (hmix.1 i)
        simp only [hz, zero_mul, le_refl]

/-- Interchanging two genuinely finite sums links mixture expected cost to
the uniform average of its actual hypothesiswise randomized depths. -/
theorem mixture_uniform_average_eq {H Q I : Type*}
    [Fintype H] [Fintype I] [DecidableEq H]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ) :
    (∑ i, probability i * expected M (uniformWeight Finset.univ) Finset.univ (trees i)) =
      ∑ h, uniformWeight Finset.univ h * randomizedDepth M trees probability h := by
  classical
  unfold expected randomizedDepth
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro h hh
  apply Finset.sum_congr rfl
  intro i hi
  ring

/-- Every feasible randomized height of an actual finite legal mixture is
at least log₂ n, with no assumed lower-bound certificate. -/
theorem legal_mixture_log_two_lower_bound {H Q I : Type*}
    [Fintype H] [Fintype I] [DecidableEq H]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ)
    (bound : ℝ) (hcard : 0 < Fintype.card H)
    (hmix : LegalMixture M Finset.univ trees probability)
    (hbound : RandomizedHeightAtMost M trees probability bound) :
    Real.log (Fintype.card H : ℝ) / Real.log 2 ≤ bound := by
  classical
  have hS : (Finset.univ : Finset H).Nonempty :=
    Finset.card_pos.mp (by simpa only [Finset.card_univ] using hcard)
  have hsum : (∑ h : H, uniformWeight Finset.univ h) = 1 :=
    uniformWeight_mass Finset.univ hS
  calc
    _ ≤ ∑ i, probability i * expected M (uniformWeight Finset.univ) Finset.univ (trees i) :=
      legal_mixture_uniform_average_lower_bound M trees probability hcard hmix
    _ = ∑ h, uniformWeight Finset.univ h * randomizedDepth M trees probability h :=
      mixture_uniform_average_eq M trees probability
    _ ≤ bound := finite_mixture_bound (uniformWeight Finset.univ)
      (randomizedDepth M trees probability) bound (uniformWeight_nonneg Finset.univ)
      hsum hbound

/-- For n≥2 the natural-log inequality is strict because 0 < ln 2 < 1. -/
theorem legal_mixture_log_strict_lower_bound {H Q I : Type*}
    [Fintype H] [Fintype I] [DecidableEq H]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ)
    (bound : ℝ) (hcard : 2 ≤ Fintype.card H)
    (hmix : LegalMixture M Finset.univ trees probability)
    (hbound : RandomizedHeightAtMost M trees probability bound) :
    Real.log (Fintype.card H : ℝ) < bound := by
  have hc : 0 < Fintype.card H := by omega
  have hn : 1 < (Fintype.card H : ℝ) := by
    exact_mod_cast (show 1 < Fintype.card H by omega)
  have hlog : 0 < Real.log (Fintype.card H : ℝ) := Real.log_pos hn
  have htwo : 0 < Real.log 2 := Real.log_pos (by norm_num : (1 : ℝ) < 2)
  have htwo_lt : Real.log 2 < 1 := by
    have h := Real.log_lt_sub_one_of_pos (by norm_num : (0 : ℝ) < 2)
      (by norm_num : (2 : ℝ) ≠ 1)
    norm_num at h
    exact h
  have hstrict : Real.log (Fintype.card H : ℝ) <
      Real.log (Fintype.card H : ℝ) / Real.log 2 := by
    apply (lt_div_iff₀ htwo).mpr
    simpa only [mul_one] using mul_lt_mul_of_pos_left htwo_lt hlog
  exact lt_of_lt_of_le hstrict
    (legal_mixture_log_two_lower_bound M trees probability bound hc hmix hbound)

end PlanarQuery
