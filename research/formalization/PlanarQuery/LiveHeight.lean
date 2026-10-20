import PlanarQuery.Properization
import PlanarQuery.TreePotentials
import Mathlib.Data.Finset.Lattice.Fold

namespace PlanarQuery
namespace Tree

variable {H Q : Type*}

/-- Maximum depth of an actual live hypothesis, including the empty-state
    convention zero. Irrelevant branches of an unproper tree are ignored. -/
def liveHeight (M : QuerySystem H Q) (S : Finset H) (T : Tree H Q) : ℕ :=
  S.sup (depth M T)

theorem liveHeight_le_height (M : QuerySystem H Q) (S : Finset H) (T : Tree H Q) :
    liveHeight M S T ≤ height T :=
  Finset.sup_le fun h _ => depth_le_height M T h

variable [DecidableEq H]

/-- After contraction every deepest leaf is reached by a live hypothesis. -/
theorem restricted_height_realized (M : QuerySystem H Q) (T : Tree H Q)
    (S : Finset H) (hS : S.Nonempty) :
    ∃ h ∈ S, depth M (restrict M T S) h = height (restrict M T S) := by
  induction T generalizing S with
  | leaf label =>
    obtain ⟨h, hh⟩ := hS
    exact ⟨h, hh, by simp [restrict, depth, height]⟩
  | node q miss hit ihm ihh =>
    have hcard : (branch M S q false).card + (branch M S q true).card = S.card := by
      rw [← Finset.card_union_of_disjoint (branches_disjoint M S q), branches_union M S q]
    have hpos := Finset.card_pos.mpr hS
    by_cases hm : branch M S q false = ∅
    · have hp : 0 < (branch M S q true).card := by rw [hm, Finset.card_empty] at hcard; omega
      obtain ⟨h, hh, hd⟩ := ihh _ (Finset.card_pos.mp hp)
      exact ⟨h, ((mem_branch _ _ _ _ _).mp hh).1, by simpa [restrict, hm] using hd⟩
    by_cases hh : branch M S q true = ∅
    · have hp : 0 < (branch M S q false).card := by rw [hh, Finset.card_empty] at hcard; omega
      obtain ⟨h, hs, hd⟩ := ihm _ (Finset.card_pos.mp hp)
      exact ⟨h, ((mem_branch _ _ _ _ _).mp hs).1, by simpa [restrict, hm, hh] using hd⟩
    have hp := Finset.nonempty_iff_ne_empty.mpr hm
    have ht := Finset.nonempty_iff_ne_empty.mpr hh
    by_cases hc : height (restrict M miss (branch M S q false)) ≤
        height (restrict M hit (branch M S q true))
    · obtain ⟨h, hs, hd⟩ := ihh _ ht
      have hb := (mem_branch _ _ _ _ _).mp hs
      exact ⟨h, hb.1, by simp [restrict, hm, hh, depth, height, hb.2, max_eq_right hc, hd]⟩
    · obtain ⟨h, hs, hd⟩ := ihm _ hp
      have hb := (mem_branch _ _ _ _ _).mp hs
      have hreverse := le_of_not_ge hc
      exact ⟨h, hb.1, by simp [restrict, hm, hh, depth, height, hb.2, max_eq_left hreverse, hd]⟩

theorem restricted_height_le_liveHeight (M : QuerySystem H Q) (T : Tree H Q)
    (S : Finset H) (hS : S.Nonempty) : height (restrict M T S) ≤ liveHeight M S T := by
  obtain ⟨h, hh, hd⟩ := restricted_height_realized M T S hS
  rw [← hd]
  exact le_trans (restriction_preserves M T S h hh).2 (Finset.le_sup hh)

/-- The binary information bound concerns live paths even when the original
    identifying tree has unused branches of arbitrarily large height. -/
theorem identification_log_liveHeight (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (hId : Identifies M S T) (hne : S.Nonempty) :
    Real.log (S.card : ℝ) / Real.log 2 ≤ (liveHeight M S T : ℝ) := by
  have hrestricted := restriction_identifies M T S S (by intro h hh; exact hh) hId
  exact le_trans (identification_log_height M S (restrict M T S) hrestricted hne)
    (Nat.cast_le.mpr (restricted_height_le_liveHeight M T S hne))

theorem restricted_liveHeight_eq_height (M : QuerySystem H Q) (T : Tree H Q)
    (S : Finset H) (hS : S.Nonempty) :
    liveHeight M S (restrict M T S) = height (restrict M T S) := by
  apply Nat.le_antisymm (liveHeight_le_height _ _ _)
  obtain ⟨h, hh, hd⟩ := restricted_height_realized M T S hS
  rw [← hd]
  exact Finset.le_sup hh

/-- Restricting an optimal competitor proves the precise per-hypothesis
    maximum-depth optimum inequality, even for an unproper competitor. -/
theorem subset_live_height_optimum_le (M : QuerySystem H Q)
    (S U : Finset H) (hsub : U ⊆ S) (T V : Tree H Q)
    (hT : Identifies M S T)
    (hmin : ∀ A, Identifies M U A → liveHeight M U V ≤ liveHeight M U A) :
    liveHeight M U V ≤ liveHeight M S T := by
  apply le_trans (hmin _ (restriction_identifies M T S U hsub hT))
  apply Finset.sup_le
  intro h hh
  exact le_trans (restriction_preserves M T U h hh).2 (Finset.le_sup (hsub hh))

variable [Fintype H] [Fintype Q] [DecidableEq Q]

/-- The true maximum live depth, not the syntactic height of irrelevant
    branches, attains its global optimum in the finite proper catalogue. -/
theorem global_live_height_minimum (M : QuerySystem H Q) (S : Finset H)
    (hS : S.Nonempty) (hfeasible : ∃ T, Identifies M S T) :
    ∃ T, Identifies M S T ∧ height T ≤ S.card - 1 ∧
      ∀ U, Identifies M S U → liveHeight M S T ≤ liveHeight M S U := by
  obtain ⟨T, hT, hcap, hmin⟩ := global_height_minimum M S hS hfeasible
  refine ⟨T, hT, hcap, ?_⟩
  intro U hU
  exact le_trans (liveHeight_le_height M S T)
    (le_trans (hmin _ (restriction_identifies M U S S (by intro h hh; exact hh) hU))
      (restricted_height_le_liveHeight M U S hS))

end Tree
end PlanarQuery
