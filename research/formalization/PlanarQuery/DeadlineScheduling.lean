import PlanarQuery.IntervalCover
import Mathlib.Data.Finset.Max

/-! Actual finite first-hit scheduling and graded-prefix checks.
The exhaustive executable solver is sound and complete for distinct
candidate schedules and arbitrary simultaneous integer deadlines.
The last-position/count update lemmas establish the state invariants
used by the graded spatial scan. This module does not yet prove the
manuscript's memoized rank-subset or graded-DP running-time bounds.
The final theorems construct real supplied-query trees with checked
exit codes and include the all-negative route. -/

namespace PlanarQuery.DeadlineScheduling
open IntervalCover

structure Job where
  interval : Interval
  deadline : Nat
  deriving DecidableEq

def Meets (jobs : List Job) (schedule : List Nat) : Prop :=
  ∀ J ∈ jobs, ∃ p ∈ schedule.take J.deadline, J.interval.Hits p

def passes (jobs : List Job) (schedule : List Nat) : Bool :=
  jobs.all (fun J => (schedule.take J.deadline).any
    (fun p => decide (J.interval.Hits p)))

def catalog (candidates : List Nat) : Nat → List (List Nat)
  | 0 => [[]]
  | fuel + 1 => [] :: candidates.flatMap
      (fun p => (catalog candidates fuel).map (List.cons p))

def Feasible (candidates : List Nat) (jobs : List Job) (cap : Nat)
    (schedule : List Nat) : Prop :=
  schedule.length ≤ cap ∧ (∀ p ∈ schedule, p ∈ candidates) ∧
    schedule.Nodup ∧ Meets jobs schedule

def solve (candidates : List Nat) (jobs : List Job) (cap : Nat) :
    Option (List Nat) :=
  (catalog candidates cap).find? (fun schedule =>
    passes jobs schedule && decide schedule.Nodup)

theorem passes_iff (jobs : List Job) (schedule : List Nat) :
    passes jobs schedule = true ↔ Meets jobs schedule := by
  simp [passes, Meets, List.all_eq_true, List.any_eq_true]

theorem mem_catalog_iff (candidates : List Nat) (cap : Nat) (schedule : List Nat) :
    schedule ∈ catalog candidates cap ↔
      schedule.length ≤ cap ∧ ∀ p ∈ schedule, p ∈ candidates := by
  induction cap generalizing schedule with
  | zero =>
      cases schedule <;> simp [catalog]
  | succ cap ih =>
      cases schedule with
      | nil => simp [catalog]
      | cons p rest =>
          constructor
          · intro hmem
            have hflat : p :: rest ∈ candidates.flatMap
                (fun p => (catalog candidates cap).map (List.cons p)) := by
              simpa [catalog] using hmem
            obtain ⟨p', hp', hmap⟩ := List.mem_flatMap.mp hflat
            obtain ⟨rest', hr', heq⟩ := List.mem_map.mp hmap
            have hpEq := (List.cons.inj heq).1
            have hrEq := (List.cons.inj heq).2
            subst p'
            subst rest'
            obtain ⟨hlen, hsub⟩ := (ih rest).mp hr'
            refine ⟨by simp; omega, ?_⟩
            intro x hx
            rcases List.mem_cons.mp hx with rfl | hx
            · exact hp'
            · exact hsub x hx
          · rintro ⟨hlen, hsub⟩
            have hlenRest : rest.length ≤ cap := by simp only [List.length_cons] at hlen; omega
            have hmemRest : rest ∈ catalog candidates cap := (ih rest).mpr
              ⟨hlenRest, fun x hx => hsub x (List.mem_cons_of_mem p hx)⟩
            apply List.mem_cons_of_mem []
            exact List.mem_flatMap.mpr ⟨p, hsub p (by simp),
              List.mem_map.mpr ⟨rest, hmemRest, rfl⟩⟩

theorem solve_sound (candidates : List Nat) (jobs : List Job) (cap : Nat)
    (schedule : List Nat) (hsolve : solve candidates jobs cap = some schedule) :
    Feasible candidates jobs cap schedule := by
  have hmem := List.mem_of_find?_eq_some hsolve
  have hpass := List.find?_some hsolve
  have hbase := (mem_catalog_iff candidates cap schedule).mp hmem
  have htest : passes jobs schedule = true ∧ decide schedule.Nodup = true := by
    simpa only [Bool.and_eq_true] using hpass
  exact ⟨hbase.1, hbase.2, of_decide_eq_true htest.2,
    (passes_iff jobs schedule).mp htest.1⟩

theorem solve_complete (candidates : List Nat) (jobs : List Job) (cap : Nat)
    (schedule : List Nat) (hfeasible : Feasible candidates jobs cap schedule) :
    (solve candidates jobs cap).isSome = true := by
  apply List.find?_isSome.mpr
  refine ⟨schedule, (mem_catalog_iff candidates cap schedule).mpr
    ⟨hfeasible.1, hfeasible.2.1⟩, ?_⟩
  simp only [Bool.and_eq_true, decide_eq_true_eq]
  exact ⟨(passes_iff jobs schedule).mpr hfeasible.2.2.2, hfeasible.2.2.1⟩

theorem solve_feasible_iff (candidates : List Nat) (jobs : List Job) (cap : Nat) :
    (solve candidates jobs cap).isSome = true ↔
      ∃ schedule, Feasible candidates jobs cap schedule := by
  constructor
  · intro h
    cases hs : solve candidates jobs cap with
    | none => simp [hs] at h
    | some schedule => exact ⟨schedule, solve_sound candidates jobs cap schedule hs⟩
  · rintro ⟨schedule, hfeasible⟩
    exact solve_complete candidates jobs cap schedule hfeasible

/-- A zero deadline cannot cover a nonempty demand, even if later
queries hit it. The solver therefore rejects this actual obstruction. -/
theorem zero_deadline_infeasible (jobs : List Job) (J : Job)
    (hJ : J ∈ jobs) (hzero : J.deadline = 0) (schedule : List Nat) :
    ¬ Meets jobs schedule := by
  intro h
  obtain ⟨p, hp, _⟩ := h J hJ
  simp [hzero] at hp

structure GradedJob where
  interval : Interval
  grade : Nat
  deriving DecidableEq

def translateGrades (capacity : Nat → Nat) (jobs : List GradedJob) : List Job :=
  jobs.map (fun J => ⟨J.interval, capacity J.grade⟩)

def MeetsGrades (capacity : Nat → Nat) (jobs : List GradedJob)
    (schedule : List Nat) : Prop :=
  ∀ J ∈ jobs, ∃ p ∈ schedule.take (capacity J.grade), J.interval.Hits p

theorem translated_grades_iff (capacity : Nat → Nat) (jobs : List GradedJob)
    (schedule : List Nat) :
    Meets (translateGrades capacity jobs) schedule ↔ MeetsGrades capacity jobs schedule := by
  constructor
  · intro h J hJ
    exact h _ (List.mem_map.mpr ⟨J, hJ, rfl⟩)
  · intro h J hJ
    obtain ⟨G, hG, rfl⟩ := List.mem_map.mp hJ
    exact h G hG

/-- Simultaneous grade feasibility is a real finite decision problem,
not independent per-prefix covers. All grades share one output order. -/
theorem graded_solver_complete (candidates : List Nat) (capacity : Nat → Nat)
    (jobs : List GradedJob) (cap : Nat) :
    (solve candidates (translateGrades capacity jobs) cap).isSome = true ↔
      ∃ schedule, schedule.length ≤ cap ∧ (∀ p ∈ schedule, p ∈ candidates) ∧
        schedule.Nodup ∧ MeetsGrades capacity jobs schedule := by
  rw [solve_feasible_iff]
  simp only [Feasible, translated_grades_iff]

/-- Zero is the sentinel for no point seen; positive left endpoints
make the last-position test exact even on an empty selected prefix. -/
def lastBefore (points : Finset Nat) (right : Nat) : Nat :=
  (points.filter (fun p => p ≤ right)).sup id

theorem last_position_hit_iff (points : Finset Nat) (I : Interval)
    (hlo : 0 < I.lo) :
    I.lo ≤ lastBefore points I.hi ↔ ∃ p ∈ points, I.Hits p := by
  rw [lastBefore, Finset.le_sup_iff hlo]
  simp only [Finset.mem_filter, id_eq, Interval.Hits]
  constructor
  · rintro ⟨p, ⟨hp, hhi⟩, hlow⟩
    exact ⟨p, hp, hlow, hhi⟩
  · rintro ⟨p, hp, hlow, hhi⟩
    exact ⟨p, ⟨hp, hhi⟩, hlow⟩

def gradePrefix (selected : Finset (Nat × Nat)) (grade : Nat) : Finset Nat :=
  (selected.filter (fun pg => pg.2 ≤ grade)).image Prod.fst

theorem grade_prefix_insert (selected : Finset (Nat × Nat)) (point grade prefixGrade : Nat) :
    gradePrefix (insert (point, grade) selected) prefixGrade =
      if grade ≤ prefixGrade then insert point (gradePrefix selected prefixGrade)
      else gradePrefix selected prefixGrade := by
  by_cases h : grade ≤ prefixGrade <;> simp [gradePrefix, Finset.filter_insert, h]

theorem grade_count_insert (selected : Finset (Nat × Nat)) (point grade prefixGrade : Nat)
    (hgrade : grade ≤ prefixGrade) (hfresh : point ∉ gradePrefix selected prefixGrade) :
    (gradePrefix (insert (point, grade) selected) prefixGrade).card =
      (gradePrefix selected prefixGrade).card + 1 := by
  rw [grade_prefix_insert, if_pos hgrade, Finset.card_insert_of_not_mem hfresh]

theorem last_position_insert (points : Finset Nat) (point right : Nat)
    (hpoint : point ≤ right) :
    lastBefore (insert point points) right = max point (lastBefore points right) := by
  simp [lastBefore, Finset.filter_insert, hpoint, Finset.sup_insert]

section SuppliedTrees
variable {H Q : Type*} [DecidableEq H]

/-- Every internal node is an actual supplied query q : Q. -/
def querySpine (queries : List Q) (children : Q → Tree H Q) (witness : H) : Tree H Q :=
  match queries with
  | [] => .leaf witness
  | q :: rest => .node q (querySpine rest children witness) (children q)

def ExitCodes (M : QuerySystem H Q) (S : Finset H) :
    List Q → (Q → Tree H Q) → Prop
  | [], _ => True
  | q :: rest, children =>
      Tree.Identifies M (Tree.branch M S q true) (children q) ∧
        ExitCodes M (Tree.branch M S q false) rest children

def ExitDepthBound (M : QuerySystem H Q) (S : Finset H) :
    List Q → (Q → Tree H Q) → (H → Nat) → Prop
  | [], _, _ => True
  | q :: rest, children, continuation =>
      (∀ h ∈ Tree.branch M S q true, Tree.depth M (children q) h ≤ continuation h) ∧
        ExitDepthBound M (Tree.branch M S q false) rest children continuation

theorem querySpine_identifies (M : QuerySystem H Q) (S : Finset H)
    (queries : List Q) (children : Q → Tree H Q) (witness : H)
    (hcodes : ExitCodes M S queries children)
    (hcover : ∀ h ∈ S, h ≠ witness → ∃ q ∈ queries, M.answer q h = true) :
    Tree.Identifies M S (querySpine queries children witness) := by
  induction queries generalizing S with
  | nil =>
      intro h hh
      have heq : h = witness := by
        by_contra hne
        obtain ⟨q, hq, _⟩ := hcover h hh hne
        simp at hq
      simp [querySpine, Tree.eval, heq]
  | cons q rest ih =>
      intro h hh
      cases hq : M.answer q h with
      | true =>
          have hm : h ∈ Tree.branch M S q true := by simp [hh, hq]
          simpa [querySpine, Tree.eval, hq] using hcodes.1 h hm
      | false =>
          have hm : h ∈ Tree.branch M S q false := by simp [hh, hq]
          have hc : ∀ x ∈ Tree.branch M S q false, x ≠ witness →
              ∃ r ∈ rest, M.answer r x = true := by
            intro x hx hne
            have hx' := (Tree.mem_branch M S q false x).mp hx
            obtain ⟨r, hr, ha⟩ := hcover x hx'.1 hne
            rcases List.mem_cons.mp hr with hr | hr
            · subst r; rw [hx'.2] at ha; cases ha
            · exact ⟨r, hr, ha⟩
          simpa [querySpine, Tree.eval, hq] using ih _ hcodes.2 hc h hm

omit [DecidableEq H] in
theorem querySpine_negative_depth (M : QuerySystem H Q) (queries : List Q)
    (children : Q → Tree H Q) (witness h : H)
    (hnegative : ∀ q ∈ queries, M.answer q h = false) :
    Tree.depth M (querySpine queries children witness) h = queries.length := by
  induction queries with
  | nil => simp [querySpine, Tree.depth]
  | cons q rest ih =>
      have hq := hnegative q (by simp)
      have hr : ∀ r ∈ rest, M.answer r h = false :=
        fun r hr => hnegative r (List.mem_cons_of_mem q hr)
      simp [querySpine, Tree.depth, hq, ih hr, Nat.add_comm]

theorem querySpine_hit_depth (M : QuerySystem H Q) (S : Finset H)
    (queries : List Q) (children : Q → Tree H Q) (witness h : H)
    (continuation : H → Nat) (k : Nat) (hh : h ∈ S)
    (hbound : ExitDepthBound M S queries children continuation)
    (hhit : ∃ q ∈ queries.take k, M.answer q h = true) :
    Tree.depth M (querySpine queries children witness) h ≤ k + continuation h := by
  induction queries generalizing S k with
  | nil => simp at hhit
  | cons q rest ih =>
      cases k with
      | zero => simp at hhit
      | succ k =>
          cases hq : M.answer q h with
          | true =>
              have hm : h ∈ Tree.branch M S q true := by simp [hh, hq]
              have hc := hbound.1 h hm
              simp only [querySpine, Tree.depth, hq, if_true]
              omega
          | false =>
              have hm : h ∈ Tree.branch M S q false := by simp [hh, hq]
              obtain ⟨r, hr, ha⟩ := hhit
              simp only [List.take_succ_cons, List.mem_cons] at hr
              have hr' : r ∈ rest.take k := by
                rcases hr with hr | hr
                · subst r; rw [hq] at ha; cases ha
                · exact hr
              have hc := ih _ k hm hbound.2 ⟨r, hr', ha⟩
              simp only [querySpine, Tree.depth, hq, Bool.false_eq_true, if_false]
              omega

/-- This is an actual route-height certificate for the constructed
supplied-query tree, including the zero/witness route. -/
theorem querySpine_route_certificate (M : QuerySystem H Q) (S : Finset H)
    (queries : List Q) (children : Q → Tree H Q) (witness : H)
    (deadline continuation : H → Nat) (heightBudget : Nat)
    (hcodes : ExitCodes M S queries children)
    (hbound : ExitDepthBound M S queries children continuation)
    (hnegative : ∀ q ∈ queries, M.answer q witness = false)
    (hlength : queries.length ≤ heightBudget)
    (hdeadline : ∀ h ∈ S, h ≠ witness →
      ∃ q ∈ queries.take (deadline h), M.answer q h = true)
    (hallowance : ∀ h ∈ S, h ≠ witness → deadline h + continuation h ≤ heightBudget) :
    Tree.Identifies M S (querySpine queries children witness) ∧
      ∀ h ∈ S, Tree.depth M (querySpine queries children witness) h ≤ heightBudget := by
  constructor
  · apply querySpine_identifies M S queries children witness hcodes
    intro h hh hne
    obtain ⟨q, hq, ha⟩ := hdeadline h hh hne
    exact ⟨q, (List.take_sublist _ _).subset hq, ha⟩
  · intro h hh
    by_cases heq : h = witness
    · subst h
      rw [querySpine_negative_depth M queries children witness witness hnegative]
      exact hlength
    · exact le_trans (querySpine_hit_depth M S queries children witness h
        continuation (deadline h) hh hbound (hdeadline h hh heq))
        (hallowance h hh heq)

end SuppliedTrees
end PlanarQuery.DeadlineScheduling