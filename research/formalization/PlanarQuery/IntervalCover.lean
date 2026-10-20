import PlanarQuery.Model
import Mathlib.Data.List.Sort

/-! Executable minimum hitting sets for finite ordinary intervals.
The proof checks the actual earliest-right-endpoint algorithm. Its
lower bound removes a point of an arbitrary competing hitting set;
no optimality or correctness oracle is assumed. Positions are naturals,
so a finite supplied candidate order is represented by a bound M.
Circular cutting and the weighted greedy run bound are separate claims. -/

namespace PlanarQuery.IntervalCover

structure Interval where
  lo : Nat
  hi : Nat
  deriving DecidableEq

def Interval.Hits (I : Interval) (p : Nat) : Prop := I.lo ≤ p ∧ p ≤ I.hi
instance (I : Interval) (p : Nat) : Decidable (I.Hits p) := inferInstanceAs
  (Decidable (I.lo ≤ p ∧ p ≤ I.hi))

def Valid (intervals : List Interval) : Prop :=
  ∀ I ∈ intervals, I.lo ≤ I.hi

def Covers (intervals : List Interval) (points : List Nat) : Prop :=
  ∀ I ∈ intervals, ∃ p ∈ points, I.Hits p

def CoversSet (intervals : List Interval) (points : Finset Nat) : Prop :=
  ∀ I ∈ intervals, ∃ p ∈ points, I.Hits p

/-- Fuel is initially the number of intervals. Each iteration takes the
first (earliest-ending) interval and discards every interval it hits. -/
def greedyFuel : Nat → List Interval → List Nat
  | 0, _ => []
  | _ + 1, [] => []
  | fuel + 1, I :: rest =>
      I.hi :: greedyFuel fuel (rest.filter (fun J => decide (I.hi < J.lo)))

def sortIntervals (intervals : List Interval) : List Interval :=
  intervals.mergeSort (fun I J => decide (I.hi ≤ J.hi))

def minimumCover (intervals : List Interval) : List Nat :=
  greedyFuel (sortIntervals intervals).length (sortIntervals intervals)

/-- Unlike minimumCover, the public solver checks empty demands. -/
def solve (intervals : List Interval) : Option (List Nat) :=
  if intervals.all (fun I => decide (I.lo ≤ I.hi)) then
    some (minimumCover intervals)
  else none

theorem sorted_intervals (intervals : List Interval) :
    (sortIntervals intervals).Pairwise (fun I J => I.hi ≤ J.hi) := by
  have htrans : ∀ I J K : Interval,
      decide (I.hi ≤ J.hi) = true → decide (J.hi ≤ K.hi) = true →
      decide (I.hi ≤ K.hi) = true := by
    intro I J K hIJ hJK
    simpa using Nat.le_trans (of_decide_eq_true hIJ) (of_decide_eq_true hJK)
  have htotal : ∀ I J : Interval,
      (decide (I.hi ≤ J.hi) || decide (J.hi ≤ I.hi)) = true := by
    intro I J
    simp only [Bool.or_eq_true, decide_eq_true_eq]
    exact le_total _ _
  simpa [sortIntervals] using List.sorted_mergeSort htrans htotal intervals

theorem sort_mem_iff (intervals : List Interval) (I : Interval) :
    I ∈ sortIntervals intervals ↔ I ∈ intervals :=
  (List.mergeSort_perm intervals _).mem_iff

theorem greedyFuel_covers (fuel : Nat) (intervals : List Interval)
    (hlen : intervals.length ≤ fuel)
    (hsorted : intervals.Pairwise (fun I J => I.hi ≤ J.hi))
    (hvalid : Valid intervals) : Covers intervals (greedyFuel fuel intervals) := by
  induction fuel generalizing intervals with
  | zero =>
      have he : intervals = [] := List.length_eq_zero_iff.mp (by omega)
      simp [he, Covers]
  | succ fuel ih =>
      cases intervals with
      | nil => simp [Covers]
      | cons I rest =>
          have hpair := List.pairwise_cons.mp hsorted
          have hlenRest : rest.length ≤ fuel := by simpa using hlen
          let residual := rest.filter (fun J => decide (I.hi < J.lo))
          have hlenResidual : residual.length ≤ fuel :=
            le_trans (List.length_filter_le _ rest) hlenRest
          have hsortResidual : residual.Pairwise (fun I J => I.hi ≤ J.hi) :=
            hpair.2.filter _
          have hvalidResidual : Valid residual := by
            intro J hJ
            exact hvalid J (List.mem_cons_of_mem I (List.mem_filter.mp hJ).1)
          have hrec := ih residual hlenResidual hsortResidual hvalidResidual
          intro J hJ
          simp only [greedyFuel]
          rcases List.mem_cons.mp hJ with hJI | hJ
          · subst J
            exact ⟨I.hi, by simp, hvalid I (by simp), le_rfl⟩
          · by_cases hlate : I.hi < J.lo
            · have hJres : J ∈ residual := by simp [residual, hJ, hlate]
              obtain ⟨p, hp, hhit⟩ := hrec J hJres
              exact ⟨p, List.mem_cons_of_mem I.hi hp, hhit⟩
            · exact ⟨I.hi, by simp, by omega, hpair.1 J hJ⟩

/-- This exchange lower bound compares with every finite hitting set,
not a assumed minimum one. It even holds when fuel is insufficient. -/
theorem greedyFuel_length_le (fuel : Nat) (intervals : List Interval)
    (P : Finset Nat) (hcover : CoversSet intervals P) :
    (greedyFuel fuel intervals).length ≤ P.card := by
  induction fuel generalizing intervals P with
  | zero => simp [greedyFuel]
  | succ fuel ih =>
      cases intervals with
      | nil => simp [greedyFuel]
      | cons I rest =>
          obtain ⟨x, hx, hIx⟩ := hcover I (by simp)
          have herase : CoversSet
              (rest.filter (fun J => decide (I.hi < J.lo))) (P.erase x) := by
            intro J hJ
            have hmem := List.mem_filter.mp hJ
            have hlate : I.hi < J.lo := of_decide_eq_true hmem.2
            obtain ⟨y, hy, hJy⟩ := hcover J (by simp [hmem.1])
            have hne : y ≠ x := by
              unfold Interval.Hits at hIx hJy
              omega
            exact ⟨y, by simp [hy, hne], hJy⟩
          have hrec := ih _ (P.erase x) herase
          have hcard := Finset.card_erase_add_one hx
          simp only [greedyFuel, List.length_cons]
          omega

theorem greedyFuel_endpoint (fuel : Nat) (intervals : List Interval)
    (p : Nat) (hp : p ∈ greedyFuel fuel intervals) :
    ∃ I ∈ intervals, p = I.hi := by
  induction fuel generalizing intervals with
  | zero => simp [greedyFuel] at hp
  | succ fuel ih =>
      cases intervals with
      | nil => simp [greedyFuel] at hp
      | cons I rest =>
          simp only [greedyFuel, List.mem_cons] at hp
          rcases hp with hp | hp
          · exact ⟨I, by simp, hp⟩
          · obtain ⟨J, hJ, heq⟩ := ih _ hp
            exact ⟨J, by simp [(List.mem_filter.mp hJ).1], heq⟩

theorem minimumCover_covers (intervals : List Interval) (hvalid : Valid intervals) :
    Covers intervals (minimumCover intervals) := by
  have hv : Valid (sortIntervals intervals) := by
    intro I hI
    exact hvalid I ((sort_mem_iff intervals I).mp hI)
  have hc := greedyFuel_covers _ _ (le_refl _) (sorted_intervals intervals) hv
  intro I hI
  exact hc I ((sort_mem_iff intervals I).mpr hI)

theorem minimumCover_minimal (intervals : List Interval) (P : Finset Nat)
    (hcover : CoversSet intervals P) : (minimumCover intervals).length ≤ P.card := by
  apply greedyFuel_length_le
  intro I hI
  exact hcover I ((sort_mem_iff intervals I).mp hI)

theorem minimumCover_endpoints (intervals : List Interval) (p : Nat)
    (hp : p ∈ minimumCover intervals) : ∃ I ∈ intervals, p = I.hi := by
  obtain ⟨I, hI, heq⟩ := greedyFuel_endpoint _ _ p hp
  exact ⟨I, (sort_mem_iff intervals I).mp hI, heq⟩

/-- For a finite candidate order 0,...,M-1, the actual output uses only
available candidates. No new query or arbitrary test is introduced. -/
theorem minimumCover_available (intervals : List Interval) (M : Nat)
    (hbound : ∀ I ∈ intervals, I.hi < M) :
    ∀ p ∈ minimumCover intervals, p < M := by
  intro p hp
  obtain ⟨I, hI, rfl⟩ := minimumCover_endpoints intervals p hp
  exact hbound I hI

theorem solve_eq_some_iff (intervals : List Interval) (points : List Nat) :
    solve intervals = some points ↔ Valid intervals ∧ minimumCover intervals = points := by
  simp [solve, Valid, List.all_eq_true]

theorem invalid_infeasible (intervals : List Interval) (I : Interval)
    (hI : I ∈ intervals) (hempty : I.hi < I.lo) (P : Finset Nat) :
    ¬ CoversSet intervals P := by
  intro hcover
  obtain ⟨p, _, hp⟩ := hcover I hI
  unfold Interval.Hits at hp
  omega

@[simp] theorem minimumCover_nil : minimumCover [] = [] := by
  simp [minimumCover, sortIntervals, greedyFuel]


/-- The executable greedy output contains no repetitions: its list
length equals the cardinality of the represented hitting set. -/
theorem minimumCover_card_eq_length (intervals : List Interval)
    (hvalid : Valid intervals) :
    (minimumCover intervals).toFinset.card = (minimumCover intervals).length := by
  have hcover : CoversSet intervals (minimumCover intervals).toFinset := by
    intro I hI
    obtain ⟨p, hp, hhit⟩ := minimumCover_covers intervals hvalid I hI
    exact ⟨p, List.mem_toFinset.mpr hp, hhit⟩
  exact Nat.le_antisymm (List.toFinset_card_le _)
    (minimumCover_minimal intervals _ hcover)

theorem minimumCover_optimal (intervals : List Interval) (hvalid : Valid intervals) :
    CoversSet intervals (minimumCover intervals).toFinset ∧
      ∀ P, CoversSet intervals P → (minimumCover intervals).toFinset.card ≤ P.card := by
  constructor
  · intro I hI
    obtain ⟨p, hp, hhit⟩ := minimumCover_covers intervals hvalid I hI
    exact ⟨p, List.mem_toFinset.mpr hp, hhit⟩
  · intro P hP
    rw [minimumCover_card_eq_length intervals hvalid]
    exact minimumCover_minimal intervals P hP

theorem solve_sound (intervals : List Interval) (points : List Nat)
    (hsolve : solve intervals = some points) :
    CoversSet intervals points.toFinset ∧
      ∀ P, CoversSet intervals P → points.length ≤ P.card := by
  obtain ⟨hvalid, heq⟩ := (solve_eq_some_iff intervals points).mp hsolve
  rw [← heq]
  exact ⟨(minimumCover_optimal intervals hvalid).1,
    fun P hP => minimumCover_minimal intervals P hP⟩

theorem solve_complete (intervals : List Interval) (P : Finset Nat)
    (hcover : CoversSet intervals P) :
    solve intervals = some (minimumCover intervals) := by
  apply (solve_eq_some_iff intervals _).mpr
  refine ⟨?_, rfl⟩
  intro I hI
  obtain ⟨p, _, hhit⟩ := hcover I hI
  exact Nat.le_trans hhit.1 hhit.2

theorem solve_none_iff (intervals : List Interval) :
    solve intervals = none ↔ ¬ ∃ P, CoversSet intervals P := by
  constructor
  · intro hnone ⟨P, hP⟩
    have hsome := solve_complete intervals P hP
    rw [hnone] at hsome
    cases hsome
  · intro hno
    cases hs : solve intervals with
    | none => rfl
    | some points =>
        exact False.elim (hno ⟨points.toFinset, (solve_sound intervals points hs).1⟩)

/-- The number of demand examinations in the greedy filtering loop.
Sorting is separate from this executable cost counter. -/
def greedyFilterWork : Nat → List Interval → Nat
  | 0, _ => 0
  | _ + 1, [] => 0
  | fuel + 1, I :: rest => rest.length +
      greedyFilterWork fuel (rest.filter (fun J => decide (I.hi < J.lo)))

theorem greedyFilterWork_bound (fuel : Nat) (intervals : List Interval) :
    greedyFilterWork fuel intervals ≤ fuel * intervals.length := by
  induction fuel generalizing intervals with
  | zero => simp [greedyFilterWork]
  | succ fuel ih =>
      cases intervals with
      | nil => simp [greedyFilterWork]
      | cons I rest =>
          have hrec := ih (rest.filter (fun J => decide (I.hi < J.lo)))
          have hlen := List.length_filter_le (fun J => decide (I.hi < J.lo)) rest
          have hmul := Nat.mul_le_mul_left fuel hlen
          simp only [greedyFilterWork, List.length_cons]
          calc
            rest.length + greedyFilterWork fuel _ ≤ rest.length + fuel * rest.length :=
              Nat.add_le_add_left (le_trans hrec hmul) _
            _ ≤ (fuel + 1) * (rest.length + 1) := by
              calc
                rest.length + fuel * rest.length = (fuel + 1) * rest.length := by ring
                _ ≤ (fuel + 1) * (rest.length + 1) := Nat.mul_le_mul_left _ (Nat.le_succ _)

theorem minimumCover_filter_work (intervals : List Interval) :
    greedyFilterWork (sortIntervals intervals).length (sortIntervals intervals) ≤
      intervals.length * intervals.length := by
  have h := greedyFilterWork_bound (sortIntervals intervals).length (sortIntervals intervals)
  have hlen : (sortIntervals intervals).length = intervals.length :=
    (List.mergeSort_perm intervals _).length_eq
  simpa only [hlen] using h

/-- Link the actual returned candidates to supplied queries. The finite
incidence representation is explicit; this statement assumes no tree
algorithm or cover oracle is correct. -/
theorem minimumCover_supplied_discovery {H Q : Type*} [DecidableEq H]
    (M : QuerySystem H Q) (S : Finset H) (intervals : List Interval)
    (job : H → Interval) (query : Nat → Q) (candidateCount : Nat)
    (hvalid : Valid intervals)
    (hbound : ∀ I ∈ intervals, I.hi < candidateCount)
    (hjob : ∀ h ∈ S, job h ∈ intervals)
    (hsem : ∀ h ∈ S, ∀ p < candidateCount,
      M.answer (query p) h = true ↔ (job h).Hits p) :
    ∀ h ∈ S, ∃ q ∈ (minimumCover intervals).map query, M.answer q h = true := by
  intro h hh
  obtain ⟨p, hp, hhit⟩ := minimumCover_covers intervals hvalid (job h) (hjob h hh)
  have havailable := minimumCover_available intervals candidateCount hbound p hp
  exact ⟨query p, List.mem_map.mpr ⟨p, hp, rfl⟩,
    (hsem h hh p havailable).mpr hhit⟩
end PlanarQuery.IntervalCover