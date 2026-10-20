import Mathlib

/-! Finite accounting for the interior split in the weighted interval-greedy
argument.  A run starts at a selected natural position whose predecessor is
not selected.  Cutting a finite candidate set on either side of a pivot can
create at most one extra run, and that extra run occurs only when the pivot
itself was selected. -/

namespace PlanarQuery.GreedyRunAccounting

/-- The first positions of the maximal consecutive runs in `S`. -/
def runStarts (S : Finset Nat) : Finset Nat :=
  S.filter fun x => x = 0 ∨ x - 1 ∉ S

/-- Number of maximal consecutive runs in a finite set of positions. -/
def runCount (S : Finset Nat) : Nat := (runStarts S).card

private theorem left_starts_subset (P : Finset Nat) (v : Nat) :
    runStarts (P.filter fun x => x < v) ⊆ runStarts P := by
  intro x hx
  rcases Finset.mem_filter.mp hx with ⟨hxP, hxStart⟩
  apply Finset.mem_filter.mpr
  refine ⟨(Finset.mem_filter.mp hxP).1, ?_⟩
  rcases hxStart with hzero | hprev
  · exact Or.inl hzero
  · apply Or.inr
    intro hprevP
    have hxv := (Finset.mem_filter.mp hxP).2
    have hprevv : x - 1 < v := by omega
    have hleft : x - 1 ∈ P.filter (fun y => y < v) :=
      Finset.mem_filter.mpr ⟨hprevP, hprevv⟩
    exact hprev hleft

private theorem right_starts_subset (P : Finset Nat) (v : Nat) :
    runStarts (P.filter fun x => v < x) ⊆
      runStarts P ∪ (if v ∈ P then {v + 1} else ∅) := by
  intro x hx
  rcases Finset.mem_filter.mp hx with ⟨hxP, hxStart⟩
  have hvx := (Finset.mem_filter.mp hxP).2
  rcases hxStart with hzero | hprev
  · omega
  · by_cases hvP : v ∈ P
    · by_cases hnext : x = v + 1
      · apply Finset.mem_union.mpr
        right
        simp [hvP, hnext]
      · apply Finset.mem_union.mpr
        left
        apply Finset.mem_filter.mpr
        refine ⟨(Finset.mem_filter.mp hxP).1, Or.inr ?_⟩
        intro hprevP
        have hprevRight : v < x - 1 := by omega
        exact hprev (Finset.mem_filter.mpr ⟨hprevP, hprevRight⟩)
    · apply Finset.mem_union.mpr
      left
      apply Finset.mem_filter.mpr
      refine ⟨(Finset.mem_filter.mp hxP).1, Or.inr ?_⟩
      intro hprevP
      have hne : x - 1 ≠ v := by
        intro heq
        have hvP' : v ∈ P := by simpa [heq] using hprevP
        exact hvP hvP'
      have hprevRight : v < x - 1 := by omega
      exact hprev (Finset.mem_filter.mpr ⟨hprevP, hprevRight⟩)

private theorem left_right_starts_disjoint (P : Finset Nat) (v : Nat) :
    Disjoint (runStarts (P.filter fun x => x < v))
      (runStarts (P.filter fun x => v < x)) := by
  refine Finset.disjoint_left.mpr ?_
  intro x hxL hxR
  have hL := (Finset.mem_filter.mp (Finset.mem_filter.mp hxL).1).2
  have hR := (Finset.mem_filter.mp (Finset.mem_filter.mp hxR).1).2
  omega

private theorem split_size_bound (P : Finset Nat) (v : Nat) :
    (P.filter fun x => x < v).card + (P.filter fun x => v < x).card +
      (if v ∈ P then 1 else 0) ≤ P.card := by
  let L := P.filter fun x => x < v
  let R := P.filter fun x => v < x
  have hdisj : Disjoint L R := by
    refine Finset.disjoint_left.mpr ?_
    intro x hxL hxR
    have hL := (Finset.mem_filter.mp hxL).2
    have hR := (Finset.mem_filter.mp hxR).2
    omega
  have hunionCard : L.card + R.card = (L ∪ R).card :=
    (Finset.card_union_of_disjoint hdisj).symm
  have hsub : L ∪ R ⊆ P := by
    intro x hx
    rcases Finset.mem_union.mp hx with hx | hx
    · exact (Finset.mem_filter.mp hx).1
    · exact (Finset.mem_filter.mp hx).1
  by_cases hvP : v ∈ P
  · have hsubErase : L ∪ R ⊆ P.erase v := by
      intro x hx
      have hxP := hsub hx
      have hxne : x ≠ v := by
        rcases Finset.mem_union.mp hx with hx | hx
        · have hlt := (Finset.mem_filter.mp hx).2
          omega
        · have hgt := (Finset.mem_filter.mp hx).2
          omega
      exact Finset.mem_erase.mpr ⟨hxne, hxP⟩
    have herase := Finset.card_le_card hsubErase
    have hcard : (P.erase v).card + 1 = P.card := Finset.card_erase_add_one hvP
    simp only [if_pos hvP]
    rw [hunionCard]
    omega
  · have hcard := Finset.card_le_card hsub
    simp only [if_neg hvP]
    rw [hunionCard]
    omega

/-- Splitting the run starts at `v` creates at most one additional start;
the extra start can occur only when `v` belonged to the original set. -/
theorem split_run_count_bound (P : Finset Nat) (v : Nat) :
    runCount (P.filter fun x => x < v) + runCount (P.filter fun x => v < x) ≤
      runCount P + (if v ∈ P then 1 else 0) := by
  let L := runStarts (P.filter fun x => x < v)
  let R := runStarts (P.filter fun x => v < x)
  let B := runStarts P
  have hdisj : Disjoint L R := left_right_starts_disjoint P v
  have hsub : L ∪ R ⊆ B ∪ (if v ∈ P then {v + 1} else ∅) := by
    intro x hx
    rcases Finset.mem_union.mp hx with hx | hx
    · exact Finset.mem_union.mpr (Or.inl (left_starts_subset P v hx))
    · exact right_starts_subset P v hx
  have hunionCard : L.card + R.card = (L ∪ R).card :=
    (Finset.card_union_of_disjoint hdisj).symm
  have hbound : (B ∪ (if v ∈ P then {v + 1} else ∅)).card ≤
      B.card + (if v ∈ P then 1 else 0) := by
    by_cases hvP : v ∈ P
    · simpa [hvP] using (Finset.card_union_le B {v + 1})
    · simp [hvP]
  change L.card + R.card ≤ B.card + (if v ∈ P then 1 else 0)
  calc
    L.card + R.card = (L ∪ R).card := hunionCard
    _ ≤ (B ∪ (if v ∈ P then {v + 1} else ∅)).card :=
      Finset.card_le_card hsub
    _ ≤ B.card + (if v ∈ P then 1 else 0) := hbound

/-- The main interior-cut accounting inequality: the sum of the two
subproblem size-plus-run charges is at most the original charge. -/
theorem split_size_run_charge (P : Finset Nat) (v : Nat) :
    ((P.filter fun x => x < v).card + runCount (P.filter fun x => x < v)) +
      ((P.filter fun x => v < x).card + runCount (P.filter fun x => v < x)) ≤
        P.card + runCount P := by
  have hsize := split_size_bound P v
  have hruns := split_run_count_bound P v
  by_cases hvP : v ∈ P
  · simp only [if_pos hvP] at hsize hruns
    omega
  · simp only [if_neg hvP] at hsize hruns
    omega

end PlanarQuery.GreedyRunAccounting
