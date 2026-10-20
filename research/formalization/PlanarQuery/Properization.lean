import PlanarQuery.FiniteSearch

namespace PlanarQuery
namespace Tree

variable {H Q : Type*}

/-- Count leaf occurrences, including any repeated leaf labels. -/
def leafCount : Tree H Q → ℕ
  | .leaf _ => 1
  | .node _ miss hit => leafCount miss + leafCount hit

theorem leafCount_le_pow_height (T : Tree H Q) : leafCount T ≤ 2 ^ height T := by
  induction T with
  | leaf label => simp [leafCount, height]
  | node q miss hit ihm ihh =>
    calc
      leafCount (.node q miss hit) = leafCount miss + leafCount hit := rfl
      _ ≤ 2 ^ height miss + 2 ^ height hit := Nat.add_le_add ihm ihh
      _ ≤ 2 ^ max (height miss) (height hit) + 2 ^ max (height miss) (height hit) :=
        Nat.add_le_add
          (Nat.pow_le_pow_right (by omega) (Nat.le_max_left _ _))
          (Nat.pow_le_pow_right (by omega) (Nat.le_max_right _ _))
      _ = 2 ^ height (.node q miss hit) := by
        simp [height, Nat.add_comm 1, pow_succ, Nat.mul_two]

variable [DecidableEq H]

/-- Contracting constant queries produces a tree of height at most the
    number of live hypotheses minus one. This needs no geometric assumption
    and in fact does not need the input tree to identify the live set. -/
theorem restricted_height_le_card_pred (M : QuerySystem H Q)
    (T : Tree H Q) (S : Finset H) (hS : S.Nonempty) :
    height (restrict M T S) ≤ S.card - 1 := by
  induction T generalizing S with
  | leaf label => simp [restrict, height]
  | node q miss hit ihm ihh =>
    have hcard : (branch M S q false).card + (branch M S q true).card = S.card := by
      rw [← Finset.card_union_of_disjoint (branches_disjoint M S q),
        branches_union M S q]
    have hpos : 0 < S.card := Finset.card_pos.mpr hS
    simp only [restrict]
    split_ifs with hm hh
    · have hp : 0 < (branch M S q true).card := by
        rw [hm, Finset.card_empty] at hcard
        omega
      have hi := ihh (branch M S q true) (Finset.card_pos.mp hp)
      rw [hm, Finset.card_empty] at hcard
      omega
    · have hp : 0 < (branch M S q false).card := by
        rw [hh, Finset.card_empty] at hcard
        omega
      have hi := ihm (branch M S q false) (Finset.card_pos.mp hp)
      rw [hh, Finset.card_empty] at hcard
      omega
    · have hp := Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hm)
      have hq := Finset.card_pos.mpr (Finset.nonempty_iff_ne_empty.mpr hh)
      have hi := ihm (branch M S q false) (Finset.card_pos.mp hp)
      have hj := ihh (branch M S q true) (Finset.card_pos.mp hq)
      simp only [height]
      omega

/-- The original weights make disjoint subproblem invoices additive.
    Restriction can only reduce each invoice, so even a partial partition
    is paid by the original identifying tree. -/
theorem disjoint_restriction_expected {I : Type*} [DecidableEq I]
    (M : QuerySystem H Q) (weight : H → ℚ) (hw : ∀ h, 0 ≤ weight h)
    (S : Finset H) (T : Tree H Q) (family : Finset I) (part : I → Finset H)
    (hdisj : (family : Set I).PairwiseDisjoint part) (hsub : ∀ i ∈ family, part i ⊆ S) :
    (∑ i ∈ family, rawExpected M weight (part i) (restrict M T (part i))) ≤
      rawExpected M weight S T := by
  have hjoin : family.biUnion part ⊆ S := by
    intro h hh
    obtain ⟨i, hi, hp⟩ := Finset.mem_biUnion.mp hh
    exact hsub i hi hp
  calc
    (∑ i ∈ family, rawExpected M weight (part i) (restrict M T (part i)))
        ≤ ∑ i ∈ family, rawExpected M weight (part i) T := by
      exact Finset.sum_le_sum fun i _ => restriction_expected_nonincrease M weight hw (part i) T
    _ = rawExpected M weight (family.biUnion part) T := by
      unfold rawExpected
      symm
      exact Finset.sum_biUnion hdisj
    _ ≤ rawExpected M weight S T := by
      apply Finset.sum_le_sum_of_subset_of_nonneg hjoin
      intro h _ _
      exact mul_nonneg (hw h) (Nat.cast_nonneg _)

/-- Complete expected-optimum restriction inequality. The supplied
    minimizers may be any globally optimal legal trees for their states;
    no geometric or finite-search premise is used in this inequality. -/
theorem disjoint_expected_optima_le {I : Type*} [DecidableEq I]
    (M : QuerySystem H Q) (weight : H → ℚ) (hw : ∀ h, 0 ≤ weight h)
    (S : Finset H) (T : Tree H Q) (hT : Identifies M S T)
    (family : Finset I) (part : I → Finset H) (chosen : I → Tree H Q)
    (hdisj : (family : Set I).PairwiseDisjoint part) (hsub : ∀ i ∈ family, part i ⊆ S)
    (hmin : ∀ i ∈ family, ∀ U, Identifies M (part i) U →
      rawExpected M weight (part i) (chosen i) ≤ rawExpected M weight (part i) U) :
    (∑ i ∈ family, rawExpected M weight (part i) (chosen i)) ≤ rawExpected M weight S T := by
  calc
    (∑ i ∈ family, rawExpected M weight (part i) (chosen i))
        ≤ ∑ i ∈ family, rawExpected M weight (part i) (restrict M T (part i)) := by
      apply Finset.sum_le_sum
      intro i hi
      exact hmin i hi _ (restriction_identifies M T S (part i) (hsub i hi) hT)
    _ ≤ rawExpected M weight S T := disjoint_restriction_expected M weight hw S T family part hdisj hsub

/-- Complete maximum-depth optimum restriction inequality. -/
theorem subset_height_optimum_le (M : QuerySystem H Q)
    (S U : Finset H) (hsub : U ⊆ S) (T V : Tree H Q)
    (hT : Identifies M S T)
    (hmin : ∀ A, Identifies M U A → height V ≤ height A) :
    height V ≤ height T :=
  le_trans (hmin _ (restriction_identifies M T S U hsub hT))
    (restriction_height_nonincrease M T U)

variable [Fintype H] [Fintype Q] [DecidableEq Q]

/-- A global minimum over all legal identifying trees, rather than merely
    over a depth-bounded search space. Properization proves that the finite
    catalogue contains a tree no more expensive than every competitor. -/
theorem global_expected_minimum (M : QuerySystem H Q) (weight : H → ℚ)
    (hw : ∀ h, 0 ≤ weight h) (S : Finset H) (hS : S.Nonempty)
    (hfeasible : ∃ T, Identifies M S T) :
    ∃ T, Identifies M S T ∧ height T ≤ S.card - 1 ∧
      ∀ U, Identifies M S U →
        rawExpected M weight S T ≤ rawExpected M weight S U := by
  obtain ⟨U, hU⟩ := hfeasible
  have hbounded : ∃ T, Identifies M S T ∧ height T ≤ S.card - 1 :=
    ⟨restrict M U S, restriction_identifies M U S S (by intro h hh; exact hh) hU,
      restricted_height_le_card_pred M U S hS⟩
  obtain ⟨T, hcat, hId, hmin⟩ := finite_expected_minimum M weight S (S.card - 1) hbounded
  refine ⟨T, hId, catalog_sound T (S.card - 1) hcat, ?_⟩
  intro V hV
  have hrId := restriction_identifies M V S S (by intro h hh; exact hh) hV
  have hrCat := catalog_complete (restrict M V S) (S.card - 1)
    (restricted_height_le_card_pred M V S hS)
  exact le_trans (hmin _ hrCat hrId) (restriction_expected_nonincrease M weight hw S V)

/-- The worst-case optimum is also attained by a finite, properized tree. -/
theorem global_height_minimum (M : QuerySystem H Q) (S : Finset H)
    (hS : S.Nonempty) (hfeasible : ∃ T, Identifies M S T) :
    ∃ T, Identifies M S T ∧ height T ≤ S.card - 1 ∧
      ∀ U, Identifies M S U → height T ≤ height U := by
  classical
  let valid := (catalog (S.card - 1)).filter (Identifies M S)
  have hnonempty : valid.Nonempty := by
    obtain ⟨U, hU⟩ := hfeasible
    exact ⟨restrict M U S, Finset.mem_filter.mpr
      ⟨catalog_complete _ _ (restricted_height_le_card_pred M U S hS),
        restriction_identifies M U S S (by intro h hh; exact hh) hU⟩⟩
  obtain ⟨T, hT, hmin⟩ := valid.exists_min_image height hnonempty
  have hm := Finset.mem_filter.mp hT
  refine ⟨T, hm.2, catalog_sound _ _ hm.1, ?_⟩
  intro U hU
  have hr := Finset.mem_filter.mpr
    ⟨catalog_complete _ _ (restricted_height_le_card_pred M U S hS),
      restriction_identifies M U S S (by intro h hh; exact hh) hU⟩
  exact le_trans (hmin (restrict M U S) hr) (restriction_height_nonincrease M U S)

end Tree
end PlanarQuery
