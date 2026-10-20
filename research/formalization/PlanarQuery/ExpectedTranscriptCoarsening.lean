import PlanarQuery.EntropyPartitions

/-!
Finite-label transcript coarsening.  The first theorem proves the exact
entropy loss when two labels are merged and all other labels retain their
masses.  The second realizes those mass premises for actual fibers of a
transcript function.  The hypotheses state explicitly that the two labels
are distinct and that the coarse map has no additional preimages.
-/

namespace PlanarQuery.ExpectedTranscriptCoarsening

open PlanarQuery.Entropy

private def otherLabels {Y : Type*} [Fintype Y] [DecidableEq Y]
    (a b : Y) : Finset Y :=
  Finset.univ.filter (fun y => Not (y = a) ∧ Not (y = b))

private theorem sum_negMulLog_split {Y : Type*} [Fintype Y] [DecidableEq Y]
    (m : Y -> Real) (a b : Y) (hab : Not (a = b)) :
    (Finset.univ.sum fun y => Real.negMulLog (m y)) =
      Real.negMulLog (m a) + Real.negMulLog (m b) +
        ((otherLabels a b).sum fun y => Real.negMulLog (m y)) := by
  let O := otherLabels a b
  have hparts : (Finset.univ : Finset Y) = ({a, b} : Finset Y) ∪ O := by
    ext y
    by_cases hya : y = a
    · subst y
      simp [O, otherLabels, hab]
    · by_cases hyb : y = b
      · subst y
        simp [O, otherLabels, hab]
      · simp [O, otherLabels, hya, hyb]
  have hd : Disjoint ({a, b} : Finset Y) O := by
    apply Finset.disjoint_left.mpr
    intro y hy hyo
    have hmem : Not (y = a) ∧ Not (y = b) := by
      simpa [O, otherLabels] using hyo
    simp only [Finset.mem_insert, Finset.mem_singleton] at hy
    rcases hy with hya | hyb
    · subst y
      exact hmem.1 rfl
    · subst y
      exact hmem.2 rfl
  rw [hparts, Finset.sum_union hd]
  simp [O, otherLabels, Finset.sum_pair, hab, add_assoc]

private noncomputable def labelEntropy {Y : Type*} [Fintype Y]
    [DecidableEq Y] (m : Y -> Real) (total : Real) : Real :=
  (Finset.univ.sum fun y => Real.negMulLog (m y)) - Real.negMulLog total

/-- Exact finite-label entropy loss under a single merge.  The coarse mass at
`a` is the sum of the two original masses, `b` becomes empty, and every other
label keeps its mass. -/
theorem finite_label_merge_entropy_loss {Y : Type*} [Fintype Y]
    [DecidableEq Y] (m coarse : Y -> Real) (total : Real) (a b : Y)
    (hab : Not (a = b))
    (hmerge : coarse a = m a + m b)
    (hempty : coarse b = 0)
    (hother : forall y, Not (y = a) -> Not (y = b) -> coarse y = m y) :
    labelEntropy m total = labelEntropy coarse total +
      binaryInformation (m a) (m b) := by
  have hrest : (otherLabels a b).sum (fun y => Real.negMulLog (m y)) =
      (otherLabels a b).sum (fun y => Real.negMulLog (coarse y)) := by
    apply Finset.sum_congr rfl
    intro y hy
    have hy' : Not (y = a) ∧ Not (y = b) := by
      simpa [otherLabels] using hy
    have hm := hother y hy'.1 hy'.2
    rw [hm]
  rw [labelEntropy, labelEntropy,
    sum_negMulLog_split m a b hab,
    sum_negMulLog_split coarse a b hab, hmerge, hempty, hrest]
  simp only [Real.negMulLog_zero, binaryInformation]
  ring

private def mergeLabel {Y : Type*} [DecidableEq Y]
    (a b : Y) (y : Y) : Y :=
  if y = b then a else y

private theorem mergeLabel_eq_a_iff {Y : Type*} [DecidableEq Y]
    (a b x : Y) :
    mergeLabel a b x = a <-> x = a ∨ x = b := by
  by_cases hxb : x = b
  · subst x
    simp [mergeLabel]
  · simp [mergeLabel, hxb]

private theorem mergeLabel_ne_b {Y : Type*} [DecidableEq Y]
    (a b x : Y) (hab : Not (a = b)) : Not (mergeLabel a b x = b) := by
  by_cases hxb : x = b
  · subst x
    simp [mergeLabel, hab]
  · simp [mergeLabel, hxb]

private theorem fiber_merge_target {H Y : Type*} [DecidableEq Y]
    [DecidableEq H] (S : Finset H) (f : H -> Y) (a b : Y) :
    fiber S (fun h => mergeLabel a b (f h)) a =
      fiber S f a ∪ fiber S f b := by
  ext h
  simp [fiber, mergeLabel_eq_a_iff, Finset.mem_union, or_comm, or_left_comm, or_assoc]
  tauto

private theorem fiber_merge_empty {H Y : Type*} [DecidableEq Y]
    [DecidableEq H] (S : Finset H) (f : H -> Y) (a b : Y)
    (hab : Not (a = b)) :
    fiber S (fun h => mergeLabel a b (f h)) b = ∅ := by
  ext h
  simp [fiber, mergeLabel_ne_b, hab]

private theorem fiber_merge_other {H Y : Type*} [DecidableEq Y]
    [DecidableEq H] (S : Finset H) (f : H -> Y) (a b y : Y)
    (hya : Not (y = a)) (hyb : Not (y = b)) :
    fiber S (fun h => mergeLabel a b (f h)) y = fiber S f y := by
  have hpoint : forall x : Y, mergeLabel a b x = y <-> x = y := by
    intro x
    by_cases hxb : x = b
    · subst x
      simp only [mergeLabel, if_pos, reduceIte]
      constructor
      · intro h
        exact (hya h.symm).elim
      · intro h
        exact (hyb h.symm).elim
    · simp [mergeLabel, hxb]
  ext h
  simp only [fiber, Finset.mem_filter]
  constructor
  · rintro ⟨hh, hlabel⟩
    exact ⟨hh, (hpoint (f h)).mp hlabel⟩
  · rintro ⟨hh, hlabel⟩
    exact ⟨hh, (hpoint (f h)).mpr hlabel⟩

private theorem fiber_pair_disjoint {H Y : Type*} [DecidableEq Y]
    [DecidableEq H] (S : Finset H) (f : H -> Y) (a b : Y)
    (hab : Not (a = b)) : Disjoint (fiber S f a) (fiber S f b) := by
  apply Finset.disjoint_left.mpr
  intro h ha hb
  have hfa : f h = a := (Finset.mem_filter.mp ha).2
  have hfb : f h = b := (Finset.mem_filter.mp hb).2
  exact hab (hfa.symm.trans hfb)

/-- For a transcript function, merging exactly the two fibers labelled `a`
and `b` loses their binary information.  Every other label is required to
remain unchanged by `mergeLabel`, so its fiber contributes no loss. -/
theorem transcript_fiber_merge_information_loss {H Y : Type*}
    [Fintype Y] [DecidableEq Y] [DecidableEq H]
    (w : H -> Real) (S : Finset H) (f : H -> Y) (a b : Y)
    (hab : Not (a = b)) :
    information w S f =
      information w S (fun h => mergeLabel a b (f h)) +
        binaryInformation (mass w (fiber S f a))
          (mass w (fiber S f b)) := by
  let m : Y -> Real := fun y => mass w (fiber S f y)
  let coarse : Y -> Real := fun y =>
    mass w (fiber S (fun h => mergeLabel a b (f h)) y)
  have hmerge : coarse a = m a + m b := by
    dsimp [coarse, m]
    rw [fiber_merge_target S f a b,
      mass_union w _ _ (fiber_pair_disjoint S f a b hab)]
  have hempty : coarse b = 0 := by
    dsimp [coarse]
    rw [fiber_merge_empty S f a b hab]
    simp [mass]
  have hmassOther : forall y, Not (y = a) -> Not (y = b) -> coarse y = m y := by
    intro y hya hyb
    dsimp [coarse, m]
    rw [fiber_merge_other S f a b y hya hyb]
  have hlabels := finite_label_merge_entropy_loss m coarse
    (mass w S) a b hab hmerge hempty hmassOther
  rw [information_eq, information_eq]
  exact hlabels

end PlanarQuery.ExpectedTranscriptCoarsening
