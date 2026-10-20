import PlanarQuery.DeadlineScheduling
import Mathlib.Data.Fintype.Pi
import Mathlib.Data.Fintype.Option
import Mathlib.Data.Finset.NAry
import Mathlib.Data.Fintype.BigOperators

/-! The actual compressed spatial graded DP. A state stores only one
count and last position per grade; traces occur only in its correctness
proof and are not retained by the algorithm. Candidates are 1,...,M.
A trace assigns either no grade or exactly one grade to each candidate.
The final endpoint checks are equivalent to interval coverage, and the
count checks enforce all nested capacities simultaneously. -/

namespace PlanarQuery.GradedDP
open IntervalCover

structure Job (r : Nat) where
  interval : Interval
  grade : Fin r
  deriving DecidableEq

structure State (r : Nat) where
  count : Fin r → Nat
  last : Fin r → Nat
  deriving DecidableEq

def initial (r : Nat) : State r := ⟨fun _ => 0, fun _ => 0⟩

def advance {r : Nat} (S : State r) (point : Nat) (choice : Option (Fin r)) : State r :=
  match choice with
  | none => S
  | some i => ⟨fun j => if i ≤ j then S.count j + 1 else S.count j,
      fun j => if i ≤ j then point else S.last j⟩

def CountOK {r : Nat} (capacity : Fin r → Nat) (S : State r) : Prop :=
  ∀ j, S.count j ≤ capacity j

def EndOK {r : Nat} (jobs : List (Job r)) (point : Nat) (S : State r) : Prop :=
  ∀ J ∈ jobs, J.interval.hi = point → J.interval.lo ≤ S.last J.grade

instance {r : Nat} (capacity : Fin r → Nat) (S : State r) :
    Decidable (CountOK capacity S) := inferInstanceAs (Decidable (∀ j, S.count j ≤ capacity j))
instance {r : Nat} (jobs : List (Job r)) (point : Nat) (S : State r) :
    Decidable (EndOK jobs point S) := inferInstanceAs
      (Decidable (∀ J ∈ jobs, J.interval.hi = point → J.interval.lo ≤ S.last J.grade))

def next {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (point : Nat) (S : State r) : Finset (State r) :=
  (Finset.univ.image (fun choice : Option (Fin r) => advance S point choice)).filter
    (fun R => CountOK capacity R ∧ EndOK jobs point R)

def run {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r)) : Nat → Finset (State r)
  | 0 => {initial r}
  | point + 1 => (run capacity jobs point).biUnion (next capacity jobs (point + 1))

/-- Newest scanned candidate first, so the position of a head choice
is one plus the length of its already scanned tail. -/
def traceState {r : Nat} : List (Option (Fin r)) → State r
  | [] => initial r
  | choice :: rest => advance (traceState rest) (rest.length + 1) choice

def pointsAt {r : Nat} : List (Option (Fin r)) → Fin r → List Nat
  | [], _ => []
  | none :: rest, j => pointsAt rest j
  | some i :: rest, j =>
      if i ≤ j then (rest.length + 1) :: pointsAt rest j else pointsAt rest j

def TraceOK {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r)) :
    List (Option (Fin r)) → Prop
  | [] => True
  | choice :: rest => TraceOK capacity jobs rest ∧
      CountOK capacity (traceState (choice :: rest)) ∧
      EndOK jobs (rest.length + 1) (traceState (choice :: rest))

theorem mem_next_iff {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (point : Nat) (S R : State r) :
    R ∈ next capacity jobs point S ↔
      ∃ choice, R = advance S point choice ∧ CountOK capacity R ∧ EndOK jobs point R := by
  simp only [next, Finset.mem_filter, Finset.mem_image, Finset.mem_univ, true_and]
  constructor
  · rintro ⟨⟨choice, heq⟩, hc, he⟩
    exact ⟨choice, heq.symm, hc, he⟩
  · rintro ⟨choice, heq, hc, he⟩
    exact ⟨⟨choice, heq.symm⟩, hc, he⟩

/-- This proves state merging sound and complete: two histories with
identical counts and last positions have exactly the same next moves. -/
theorem mem_run_iff {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (point : Nat) (S : State r) :
    S ∈ run capacity jobs point ↔
      ∃ trace, trace.length = point ∧ TraceOK capacity jobs trace ∧ traceState trace = S := by
  induction point generalizing S with
  | zero =>
      simp only [run, Finset.mem_singleton]
      constructor
      · intro heq
        exact ⟨[], rfl, trivial, heq.symm⟩
      · rintro ⟨trace, hlen, _, heq⟩
        have ht : trace = [] := List.length_eq_zero_iff.mp hlen
        simpa [ht, traceState] using heq.symm
  | succ point ih =>
      simp only [run, Finset.mem_biUnion]
      constructor
      · rintro ⟨R, hR, hstep⟩
        obtain ⟨trace, hlen, htrace, heq⟩ := (ih R).mp hR
        obtain ⟨choice, hS, hc, he⟩ := (mem_next_iff capacity jobs (point + 1) R S).mp hstep
        refine ⟨choice :: trace, by simp [hlen], ?_, ?_⟩
        · simp only [TraceOK]
          refine ⟨htrace, ?_, ?_⟩ <;> simpa [traceState, hlen, heq, ← hS]
        · simpa [traceState, hlen, heq] using hS.symm
      · rintro ⟨trace, hlen, htrace, heq⟩
        cases trace with
        | nil => simp at hlen
        | cons choice rest =>
            have hrest : rest.length = point := by simp only [List.length_cons] at hlen; omega
            refine ⟨traceState rest, (ih _).mpr ⟨rest, hrest, htrace.1, rfl⟩, ?_⟩
            apply (mem_next_iff capacity jobs (point + 1) _ _).mpr
            refine ⟨choice, ?_, ?_, ?_⟩
            · simpa [traceState, hrest] using heq.symm
            · simpa [heq] using htrace.2.1
            · simpa [hrest, heq] using htrace.2.2

theorem trace_count {r : Nat} (trace : List (Option (Fin r))) (j : Fin r) :
    (traceState trace).count j = (pointsAt trace j).length := by
  induction trace with
  | nil => rfl
  | cons choice rest ih =>
      cases choice with
      | none => simpa [traceState, advance, pointsAt] using ih
      | some i =>
          by_cases hi : i ≤ j <;> simp [traceState, advance, pointsAt, hi, ih]

theorem trace_points_bounds {r : Nat} (trace : List (Option (Fin r)))
    (j : Fin r) (p : Nat) (hp : p ∈ pointsAt trace j) :
    0 < p ∧ p ≤ trace.length := by
  induction trace with
  | nil => simp [pointsAt] at hp
  | cons choice rest ih =>
      cases choice with
      | none =>
          have h := ih (by simpa [pointsAt] using hp)
          simp only [List.length_cons]
          omega
      | some i =>
          by_cases hi : i ≤ j
          · simp only [pointsAt, if_pos hi, List.mem_cons] at hp
            rcases hp with rfl | hp
            · simp
            · have h := ih hp; simp only [List.length_cons]; omega
          · have h := ih (by simpa [pointsAt, hi] using hp)
            simp only [List.length_cons]
            omega

theorem trace_last {r : Nat} (trace : List (Option (Fin r))) (j : Fin r) :
    (traceState trace).last j = (pointsAt trace j).toFinset.sup id := by
  induction trace with
  | nil => simp [traceState, initial, pointsAt]
  | cons choice rest ih =>
      cases choice with
      | none => simpa [traceState, advance, pointsAt] using ih
      | some i =>
          by_cases hi : i ≤ j
          · simp only [traceState, advance, hi, if_true, pointsAt,
              List.toFinset_cons, Finset.sup_insert, id_eq]
            have hlast : (pointsAt rest j).toFinset.sup id ≤ rest.length + 1 := by
              apply Finset.sup_le
              intro p hp
              exact le_trans (trace_points_bounds rest j p (List.mem_toFinset.mp hp)).2
                (Nat.le_succ _)
            exact (max_eq_left hlast).symm
          · simpa [traceState, advance, pointsAt, hi] using ih

theorem trace_last_hit_iff {r : Nat} (trace : List (Option (Fin r)))
    (j : Fin r) (I : Interval) (hlo : 0 < I.lo) (hhi : I.hi = trace.length) :
    I.lo ≤ (traceState trace).last j ↔ ∃ p ∈ pointsAt trace j, I.Hits p := by
  rw [trace_last, Finset.le_sup_iff hlo]
  simp only [List.mem_toFinset, id_eq]
  constructor
  · rintro ⟨p, hp, hl⟩
    exact ⟨p, hp, hl, by rw [hhi]; exact (trace_points_bounds trace j p hp).2⟩
  · rintro ⟨p, hp, hl, _⟩
    exact ⟨p, hp, hl⟩


/-- Adding a candidate can only increase each cumulative count. -/
theorem trace_count_mono {r : Nat} (rest : List (Option (Fin r)))
    (choice : Option (Fin r)) (j : Fin r) :
    (traceState rest).count j ≤ (traceState (choice :: rest)).count j := by
  cases choice with
  | none => simp [traceState, advance]
  | some i => by_cases hi : i ≤ j <;> simp [traceState, advance, hi]

theorem trace_points_mono {r : Nat} (rest : List (Option (Fin r)))
    (choice : Option (Fin r)) (j : Fin r) (p : Nat)
    (hp : p ∈ pointsAt rest j) : p ∈ pointsAt (choice :: rest) j := by
  cases choice with
  | none => simpa [pointsAt] using hp
  | some i => by_cases hi : i ≤ j <;> simp [pointsAt, hi, hp]

/-- A later candidate cannot repair an earlier interval deadline. -/
theorem trace_old_hit {r : Nat} (rest : List (Option (Fin r)))
    (choice : Option (Fin r)) (j : Fin r) (I : Interval)
    (hhi : I.hi ≤ rest.length)
    (hhit : ∃ p ∈ pointsAt (choice :: rest) j, I.Hits p) :
    ∃ p ∈ pointsAt rest j, I.Hits p := by
  obtain ⟨p, hp, hI⟩ := hhit
  cases choice with
  | none => exact ⟨p, by simpa [pointsAt] using hp, hI⟩
  | some i =>
      by_cases hi : i ≤ j
      · simp only [pointsAt, if_pos hi, List.mem_cons] at hp
        rcases hp with hp | hp
        · unfold Interval.Hits at hI; omega
        · exact ⟨p, hp, hI⟩
      · exact ⟨p, by simpa [pointsAt, hi] using hp, hI⟩

def WellFormed {r : Nat} (jobs : List (Job r)) : Prop :=
  ∀ J ∈ jobs, 0 < J.interval.lo ∧ J.interval.lo ≤ J.interval.hi

def PrefixFeasible {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (trace : List (Option (Fin r))) : Prop :=
  CountOK capacity (traceState trace) ∧
    ∀ J ∈ jobs, J.interval.hi ≤ trace.length →
      ∃ p ∈ pointsAt trace J.grade, J.interval.Hits p

/-- Every intermediate endpoint check is equivalent to actual coverage
of all intervals whose right endpoints have already been scanned.
In particular this checks the substantive last-position DP invariant. -/
theorem traceOK_iff_prefixFeasible {r : Nat} (capacity : Fin r → Nat)
    (jobs : List (Job r)) (hwell : WellFormed jobs)
    (trace : List (Option (Fin r))) :
    TraceOK capacity jobs trace ↔ PrefixFeasible capacity jobs trace := by
  induction trace with
  | nil =>
      constructor
      · intro _
        refine ⟨fun _ => Nat.zero_le _, ?_⟩
        intro J hJ hhi
        have hw := hwell J hJ
        simp only [List.length_nil] at hhi
        omega
      · intro _; trivial
  | cons choice rest ih =>
      constructor
      · rintro ⟨hrest, hc, he⟩
        have hprefix := ih.mp hrest
        refine ⟨hc, ?_⟩
        intro J hJ hhi
        by_cases hold : J.interval.hi ≤ rest.length
        · obtain ⟨p, hp, hhit⟩ := hprefix.2 J hJ hold
          exact ⟨p, trace_points_mono rest choice J.grade p hp, hhit⟩
        · have hend : J.interval.hi = (choice :: rest).length := by
            simp only [List.length_cons] at hhi ⊢
            omega
          apply (trace_last_hit_iff (choice :: rest) J.grade J.interval
            (hwell J hJ).1 hend).mp
          exact he J hJ (by simpa only [List.length_cons] using hend)
      · rintro ⟨hc, hcovered⟩
        refine ⟨ih.mpr ⟨?_, ?_⟩, hc, ?_⟩
        · intro j
          exact le_trans (trace_count_mono rest choice j) (hc j)
        · intro J hJ hhi
          apply trace_old_hit rest choice J.grade J.interval hhi
          exact hcovered J hJ (by simp only [List.length_cons]; omega)
        · intro J hJ hend
          apply (trace_last_hit_iff (choice :: rest) J.grade J.interval
            (hwell J hJ).1 (by simpa only [List.length_cons] using hend)).mpr
          exact hcovered J hJ (by simp only [List.length_cons]; omega)

/-- This is correctness of the actual compressed finite DP, not an
oracle assumption. All grades share the same candidate assignments. -/
theorem run_feasible_iff {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (hwell : WellFormed jobs) (M : Nat) (hbound : ∀ J ∈ jobs, J.interval.hi ≤ M) :
    (run capacity jobs M).Nonempty ↔
      ∃ trace : List (Option (Fin r)), trace.length = M ∧
        (∀ j, (pointsAt trace j).length ≤ capacity j) ∧
        ∀ J ∈ jobs, ∃ p ∈ pointsAt trace J.grade, J.interval.Hits p := by
  constructor
  · rintro ⟨S, hS⟩
    obtain ⟨trace, hlen, ht, _⟩ := (mem_run_iff capacity jobs M S).mp hS
    have hp := (traceOK_iff_prefixFeasible capacity jobs hwell trace).mp ht
    refine ⟨trace, hlen, ?_, ?_⟩
    · intro j
      rw [← trace_count]
      exact hp.1 j
    · intro J hJ
      exact hp.2 J hJ (by rw [hlen]; exact hbound J hJ)
  · rintro ⟨trace, hlen, hc, hhit⟩
    refine ⟨traceState trace, (mem_run_iff capacity jobs M _).mpr
      ⟨trace, hlen, ?_, rfl⟩⟩
    apply (traceOK_iff_prefixFeasible capacity jobs hwell trace).mpr
    refine ⟨?_, fun J hJ _ => hhit J hJ⟩
    intro j
    rw [trace_count]
    exact hc j

/-- Stored last positions are bounded by the scan position; the empty
prefix is represented by the zero sentinel. -/
theorem run_state_bounds {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (point : Nat) (S : State r) (hS : S ∈ run capacity jobs point) :
    CountOK capacity S ∧ ∀ j, S.last j ≤ point := by
  obtain ⟨trace, hlen, ht, heq⟩ := (mem_run_iff capacity jobs point S).mp hS
  constructor
  · cases trace with
    | nil =>
        rw [← heq]
        intro j
        exact Nat.zero_le _
    | cons choice rest => simpa [heq] using ht.2.1
  · intro j
    rw [← heq, trace_last]
    apply Finset.sup_le
    intro p hp
    rw [← hlen]
    exact (trace_points_bounds trace j p (List.mem_toFinset.mp hp)).2

/-- Each spatial candidate has one assignment, so reconstruction cannot
repeat a candidate even if it belongs to many grade prefixes. -/
def assignments {r : Nat} : List (Option (Fin r)) → List (Nat × Fin r)
  | [] => []
  | none :: rest => assignments rest
  | some i :: rest => (rest.length + 1, i) :: assignments rest

theorem pointsAt_assignments {r : Nat} (trace : List (Option (Fin r))) (j : Fin r) :
    pointsAt trace j = ((assignments trace).filter (fun pg => decide (pg.2 ≤ j))).map Prod.fst := by
  induction trace with
  | nil => rfl
  | cons choice rest ih =>
      cases choice with
      | none => simpa [pointsAt, assignments] using ih
      | some i => by_cases hi : i ≤ j <;> simp [pointsAt, assignments, hi, ih]

theorem assignment_bounds {r : Nat} (trace : List (Option (Fin r)))
    (pg : Nat × Fin r) (hpg : pg ∈ assignments trace) :
    0 < pg.1 ∧ pg.1 ≤ trace.length := by
  induction trace with
  | nil => simp [assignments] at hpg
  | cons choice rest ih =>
      cases choice with
      | none =>
          have h := ih (by simpa [assignments] using hpg)
          simp only [List.length_cons]; omega
      | some i =>
          simp only [assignments, List.mem_cons] at hpg
          rcases hpg with rfl | hpg
          · simp
          · have h := ih hpg; simp only [List.length_cons]; omega

theorem assignments_nodup {r : Nat} (trace : List (Option (Fin r))) :
    ((assignments trace).map Prod.fst).Nodup := by
  induction trace with
  | nil => simp [assignments]
  | cons choice rest ih =>
      cases choice with
      | none => simpa [assignments] using ih
      | some i =>
          simp only [assignments, List.map_cons, List.nodup_cons]
          refine ⟨?_, ih⟩
          intro hmem
          obtain ⟨pg, hpg, heq⟩ := List.mem_map.mp hmem
          have hb := assignment_bounds rest pg hpg
          omega

def orderedAssignments {r : Nat} (trace : List (Option (Fin r))) : List (Nat × Fin r) :=
  (assignments trace).mergeSort (fun a b => decide (a.2 ≤ b.2))

def output {r : Nat} (trace : List (Option (Fin r))) : List Nat :=
  (orderedAssignments trace).map Prod.fst

theorem ordered_sorted {r : Nat} (trace : List (Option (Fin r))) :
    (orderedAssignments trace).Pairwise (fun a b => a.2 ≤ b.2) := by
  have ht : ∀ a b c : Nat × Fin r,
      decide (a.2 ≤ b.2) = true → decide (b.2 ≤ c.2) = true → decide (a.2 ≤ c.2) = true := by
    intro a b c hab hbc
    simpa using le_trans (of_decide_eq_true hab) (of_decide_eq_true hbc)
  have htotal : ∀ a b : Nat × Fin r,
      (decide (a.2 ≤ b.2) || decide (b.2 ≤ a.2)) = true := by
    intro a b
    simp only [Bool.or_eq_true, decide_eq_true_eq]
    exact le_total _ _
  simpa [orderedAssignments] using List.sorted_mergeSort ht htotal (assignments trace)

theorem ordered_perm {r : Nat} (trace : List (Option (Fin r))) :
    (orderedAssignments trace).Perm (assignments trace) :=
  List.mergeSort_perm _ _

theorem ordered_filter_length {r : Nat} (trace : List (Option (Fin r))) (j : Fin r) :
    ((orderedAssignments trace).filter (fun pg => decide (pg.2 ≤ j))).length =
      (pointsAt trace j).length := by
  rw [pointsAt_assignments, List.length_map]
  exact ((ordered_perm trace).filter _).length_eq

/-- In a grade-sorted list, every member of a grade prefix occurs in
its first count-many positions. This is the rank-versus-count step. -/
theorem sorted_grade_early {r : Nat} (pairs : List (Nat × Fin r)) (j : Fin r)
    (hsorted : pairs.Pairwise (fun a b => a.2 ≤ b.2))
    (pg : Nat × Fin r) (hpg : pg ∈ pairs) (hgrade : pg.2 ≤ j) :
    pg ∈ pairs.take ((pairs.filter (fun a => decide (a.2 ≤ j))).length) := by
  induction pairs with
  | nil => simp at hpg
  | cons head rest ih =>
      have hp := List.pairwise_cons.mp hsorted
      rcases List.mem_cons.mp hpg with rfl | hpg
      · simp [List.filter_cons, hgrade]
      · have hhead : head.2 ≤ j := le_trans (hp.1 pg hpg) hgrade
        have hr := ih hp.2 hpg
        simpa [List.filter_cons, hhead, List.take_succ_cons] using
          List.mem_cons_of_mem head hr

theorem output_nodup {r : Nat} (trace : List (Option (Fin r))) :
    (output trace).Nodup :=
  ((ordered_perm trace).map Prod.fst).nodup_iff.mpr (assignments_nodup trace)

theorem output_bounds {r : Nat} (trace : List (Option (Fin r)))
    (p : Nat) (hp : p ∈ output trace) : 0 < p ∧ p ≤ trace.length := by
  obtain ⟨pg, hpg, rfl⟩ := List.mem_map.mp hp
  exact assignment_bounds trace pg ((ordered_perm trace).mem_iff.mp hpg)

theorem output_grade_early {r : Nat} (trace : List (Option (Fin r)))
    (capacity : Fin r → Nat) (j : Fin r)
    (hc : (pointsAt trace j).length ≤ capacity j) (p : Nat)
    (hp : p ∈ pointsAt trace j) : p ∈ (output trace).take (capacity j) := by
  rw [pointsAt_assignments] at hp
  obtain ⟨pg, hpg, rfl⟩ := List.mem_map.mp hp
  have hpfilter := List.mem_filter.mp hpg
  have hsortedmem := (ordered_perm trace).mem_iff.mpr hpfilter.1
  have hearly := sorted_grade_early (orderedAssignments trace) j (ordered_sorted trace)
    pg hsortedmem (of_decide_eq_true hpfilter.2)
  have hcount : ((orderedAssignments trace).filter
      (fun a => decide (a.2 ≤ j))).length ≤ capacity j := by
    rw [ordered_filter_length]; exact hc
  have htake := List.take_subset_take_left (orderedAssignments trace) hcount hearly
  simpa only [output, List.map_take] using
    (List.mem_map.mpr ⟨pg, htake, rfl⟩ :
      pg.1 ∈ ((orderedAssignments trace).take (capacity j)).map Prod.fst)

/-- A passing compressed DP state reconstructs an actual distinct
candidate schedule satisfying every original first-hit capacity. -/
theorem run_reconstructs {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (hwell : WellFormed jobs) (M : Nat) (hbound : ∀ J ∈ jobs, J.interval.hi ≤ M)
    (hrun : (run capacity jobs M).Nonempty) :
    ∃ schedule : List Nat, schedule.Nodup ∧
      (∀ p ∈ schedule, 0 < p ∧ p ≤ M) ∧
      ∀ J ∈ jobs, ∃ p ∈ schedule.take (capacity J.grade), J.interval.Hits p := by
  obtain ⟨trace, hlen, hc, hhit⟩ :=
    (run_feasible_iff capacity jobs hwell M hbound).mp hrun
  refine ⟨output trace, output_nodup trace, ?_, ?_⟩
  · intro p hp
    simpa only [hlen] using output_bounds trace p hp
  · intro J hJ
    obtain ⟨p, hp, hI⟩ := hhit J hJ
    exact ⟨p, output_grade_early trace capacity J.grade (hc J.grade) p hp, hI⟩

/-- The compressed state space has the manuscript's product bound.
There are B+1 possible counts and M+1 possible last positions per grade;
histories do not occur in this bound. -/
theorem run_card_bound {r : Nat} (capacity : Fin r → Nat) (jobs : List (Job r))
    (M B : Nat) (hcapacity : ∀ j, capacity j ≤ B) :
    (run capacity jobs M).card ≤ (B + 1) ^ r * (M + 1) ^ r := by
  let encodeState : ((Fin r → Fin (B + 1)) × (Fin r → Fin (M + 1))) → State r :=
    fun x => ⟨fun j => x.1 j, fun j => x.2 j⟩
  let box := Finset.univ.image encodeState
  have hsub : run capacity jobs M ⊆ box := by
    intro S hS
    obtain ⟨hc, hl⟩ := run_state_bounds capacity jobs M S hS
    let counts : Fin r → Fin (B + 1) := fun j => ⟨S.count j,
      Nat.lt_succ_of_le ((hc j).trans (hcapacity j))⟩
    let lasts : Fin r → Fin (M + 1) := fun j => ⟨S.last j, Nat.lt_succ_of_le (hl j)⟩
    exact Finset.mem_image.mpr ⟨(counts, lasts), Finset.mem_univ _, rfl⟩
  calc
    (run capacity jobs M).card ≤ box.card := Finset.card_le_card hsub
    _ ≤ Fintype.card ((Fin r → Fin (B + 1)) × (Fin r → Fin (M + 1))) :=
      (Finset.card_image_le).trans_eq (Finset.card_univ)
    _ = (B + 1) ^ r * (M + 1) ^ r := by
      simp only [Fintype.card_prod, Fintype.card_fun, Fintype.card_fin]
end PlanarQuery.GradedDP
