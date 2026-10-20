import PlanarQuery.Model
import Mathlib.Algebra.Order.GroupWithZero.Unbundled.Basic

/-! Integer separation of priority levels in a finite greedy schedule.
Higher-priority score differences cannot be reversed by a bounded sum
of lower-priority scores. The scheduling data must still establish the
stated divisibility and suffix bounds. -/

namespace PlanarQuery.PriorityPrefix

/-- With base one larger than the number of classes, all lower levels
    together have score strictly smaller than one unit at the next level. -/
theorem lower_priority_geometric_budget (s k : Nat) :
    s * (s + 1) ^ k < (s + 1) ^ (k + 1) := by
  have hb : 0 < s + 1 := by omega
  have hp : 0 < (s + 1) ^ k := Nat.pow_pos hb
  have hmul := Nat.mul_lt_mul_of_pos_right (Nat.lt_succ_self s) hp
  have hmul' : s * (s + 1) ^ k < (s + 1) * (s + 1) ^ k := by
    exact hmul
  calc
    s * (s + 1) ^ k < (s + 1) * (s + 1) ^ k := hmul'
    _ = (s + 1) ^ k * (s + 1) := Nat.mul_comm _ _
    _ = (s + 1) ^ (k + 1) := by rw [Nat.pow_succ]

/-- At most `s` lower-priority classes, each with score at most `B^k`,
    have total score strictly below the next level `B^(k+1)` when
    `B = s + 1`. -/
theorem finite_suffix_sum_below_level (classes : Finset β) (weight : β → Nat)
    (s k : Nat) (hcard : classes.card ≤ s)
    (hweight : ∀ a ∈ classes, weight a ≤ (s + 1) ^ k) :
    (∑ a ∈ classes, weight a) < (s + 1) ^ (k + 1) := by
  have hsum : (∑ a ∈ classes, weight a) ≤ s * (s + 1) ^ k := by
    calc
      (∑ a ∈ classes, weight a) ≤ ∑ _a ∈ classes, (s + 1) ^ k :=
        Finset.sum_le_sum fun a ha => hweight a ha
      _ = classes.card * (s + 1) ^ k := by simp [nsmul_eq_mul]
      _ ≤ s * (s + 1) ^ k := Nat.mul_le_mul_right _ hcard
  exact lt_of_le_of_lt hsum (lower_priority_geometric_budget s k)

/-- Sums of priority weights at or above one rank are exact multiples
    of that rank's unit. -/
theorem priority_level_sum_divisible (classes : Finset β) (base k : Nat)
    (offset : β → Nat) :
    base ^ k ∣ ∑ a ∈ classes, base ^ (k + offset a) := by
  refine ⟨∑ a ∈ classes, base ^ offset a, ?_⟩
  calc
    (∑ a ∈ classes, base ^ (k + offset a)) =
        ∑ a ∈ classes, base ^ k * base ^ offset a := by
          apply Finset.sum_congr rfl
          intro a ha
          rw [Nat.pow_add]
    _ = base ^ k * ∑ a ∈ classes, base ^ offset a := by
      rw [← Finset.mul_sum]

/-- A score difference that is a positive multiple of `unit` is larger
    than any lower-priority contribution bounded strictly below `unit`.
    The nonnegative suffix of the winning candidate can only strengthen
    the conclusion. -/
theorem priority_score_dominates_suffix
    (prefixScore suffixScore : α → Nat) (unit : Nat)
    (x y : α) (hdivx : unit ∣ prefixScore x) (hdivy : unit ∣ prefixScore y)
    (hsuffix : suffixScore y < unit) (hprefix : prefixScore y < prefixScore x) :
    prefixScore y + suffixScore y < prefixScore x + suffixScore x := by
  obtain ⟨qx, hx⟩ := hdivx
  obtain ⟨qy, hy⟩ := hdivy
  have hquot : qy < qx := by
    by_contra hnot
    have hle : qx ≤ qy := Nat.le_of_not_gt hnot
    have hmul := Nat.mul_le_mul_left unit hle
    have hcontra : prefixScore x ≤ prefixScore y := by
      calc
        prefixScore x = unit * qx := hx
        _ ≤ unit * qy := hmul
        _ = prefixScore y := hy.symm
    omega
  have hstep := Nat.mul_le_mul_left unit (Nat.succ_le_of_lt hquot)
  have hgap : prefixScore y + unit ≤ prefixScore x := by
    calc
      prefixScore y + unit = unit * (qy + 1) := by rw [hy, Nat.mul_succ]
      _ ≤ unit * qx := hstep
      _ = prefixScore x := hx.symm
  omega

/-- Every global score maximizer also maximizes the selected priority
    prefix. Thus lower-deadline classes cannot change the greedy choice
    for that prefix, provided each prefix score is a multiple of one unit
    and every lower-priority suffix stays below that unit. -/
theorem global_maximizer_maximizes_prefix
    [DecidableEq α] (candidates : Finset α)
    (prefixScore suffixScore : α → Nat) (unit : Nat)
    (hdiv : ∀ a ∈ candidates, unit ∣ prefixScore a)
    (hsuffix : ∀ a ∈ candidates, suffixScore a < unit)
    (x : α) (hx : x ∈ candidates)
    (hglobal : ∀ y ∈ candidates,
      prefixScore y + suffixScore y ≤ prefixScore x + suffixScore x) :
    ∀ y ∈ candidates, prefixScore y ≤ prefixScore x := by
  intro y hy
  by_contra hnot
  have hprefix : prefixScore x < prefixScore y := Nat.lt_of_not_ge hnot
  have hstrict := priority_score_dominates_suffix prefixScore suffixScore unit y x
    (hdiv y hy) (hdiv x hx) (hsuffix x hx) hprefix
  have hmax := hglobal y hy
  omega

/-! A deadline instance has one finite class per remaining demand.
Each candidate's weight is the sum of the weights of the classes it hits.
The following results instantiate the abstract score hypotheses above. -/

def remainingHitClasses [DecidableEq α] (remaining : Finset α) (hits : β → Finset α)
    (candidate : β) : Finset α := remaining ∩ hits candidate

def earlierDeadlineClasses (rank : α → Fin r) (j : Fin r)
    (classes : Finset α) : Finset α := classes.filter fun a => rank a ≤ j

def laterDeadlineClasses (rank : α → Fin r) (j : Fin r)
    (classes : Finset α) : Finset α := classes.filter fun a => ¬ rank a ≤ j

def earlierPriorityScore [DecidableEq α] (s r : Nat) (rank : α → Fin r) (j : Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β) : Nat :=
  ∑ a ∈ earlierDeadlineClasses rank j (remainingHitClasses remaining hits candidate),
    (s + 1) ^ (r - (rank a).val)

def laterPriorityScore [DecidableEq α] (s r : Nat) (rank : α → Fin r) (j : Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β) : Nat :=
  ∑ a ∈ laterDeadlineClasses rank j (remainingHitClasses remaining hits candidate),
    (s + 1) ^ (r - (rank a).val)

def fullPriorityScore [DecidableEq α] (s r : Nat) (rank : α → Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β) : Nat :=
  ∑ a ∈ remainingHitClasses remaining hits candidate,
    (s + 1) ^ (r - (rank a).val)

/-- Splitting hit classes at a deadline partitions the score exactly. -/
theorem full_priority_score_split [DecidableEq α] (s r : Nat) (rank : α → Fin r) (j : Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β) :
    fullPriorityScore s r rank remaining hits candidate =
      earlierPriorityScore s r rank j remaining hits candidate +
        laterPriorityScore s r rank j remaining hits candidate := by
  unfold fullPriorityScore earlierPriorityScore laterPriorityScore
    earlierDeadlineClasses laterDeadlineClasses
  rw [← Finset.sum_filter_add_sum_filter_not
    (s := remainingHitClasses remaining hits candidate) (p := fun a => rank a ≤ j)]

/-- The score of all classes due by `j` is a multiple of their smallest
    priority weight `(s+1)^(r-j)`. -/
theorem earlier_priority_score_divisible [DecidableEq α]
    (s r : Nat) (rank : α → Fin r) (j : Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β) :
    (s + 1) ^ (r - j.val) ∣ earlierPriorityScore s r rank j remaining hits candidate := by
  let classes := earlierDeadlineClasses rank j (remainingHitClasses remaining hits candidate)
  have hdiv : (s + 1) ^ (r - j.val) ∣
      ∑ a ∈ classes, (s + 1) ^ ((r - j.val) + (j.val - (rank a).val)) := by
    exact priority_level_sum_divisible classes (s + 1) (r - j.val)
      (fun a => j.val - (rank a).val)
  have hsum : earlierPriorityScore s r rank j remaining hits candidate =
      ∑ a ∈ classes, (s + 1) ^ ((r - j.val) + (j.val - (rank a).val)) := by
    unfold earlierPriorityScore
    dsimp [classes]
    apply Finset.sum_congr rfl
    intro a ha
    have hrank : (rank a).val ≤ j.val := (Finset.mem_filter.mp ha).2
    have hexp : r - (rank a).val = (r - j.val) + (j.val - (rank a).val) := by omega
    rw [hexp]
  rw [hsum]
  exact hdiv

/-- Every later-deadline suffix has score less than one unit at the
    current deadline. Its hit classes are a subset of the at most `s`
    remaining classes, and each later weight is at most this bound. -/
theorem later_priority_score_lt_unit [DecidableEq α]
    (s r : Nat) (rank : α → Fin r) (j : Fin r)
    (remaining : Finset α) (hits : β → Finset α) (candidate : β)
    (hcard : remaining.card ≤ s) :
    laterPriorityScore s r rank j remaining hits candidate < (s + 1) ^ (r - j.val) := by
  let classes := laterDeadlineClasses rank j (remainingHitClasses remaining hits candidate)
  have hsub : classes ⊆ remaining := by
    intro a ha
    have hmem := Finset.mem_filter.mp ha
    have hclass : a ∈ remaining ∩ hits candidate := by
      simpa only [remainingHitClasses] using hmem.1
    exact (Finset.mem_inter.mp hclass).1
  have hcard' : classes.card ≤ s := le_trans (Finset.card_le_card hsub) hcard
  have hweight : ∀ a ∈ classes, (s + 1) ^ (r - (rank a).val) ≤
      (s + 1) ^ (r - j.val - 1) := by
    intro a ha
    have hj : j.val < (rank a).val := by
      have hnot := (Finset.mem_filter.mp ha).2
      exact Nat.lt_of_not_ge hnot
    have hrank := (rank a).is_lt
    have hexp : r - (rank a).val ≤ r - j.val - 1 := by omega
    exact pow_le_pow_right₀ (by omega) hexp
  have hsum := finite_suffix_sum_below_level classes
    (fun a => (s + 1) ^ (r - (rank a).val)) s (r - j.val - 1) hcard' hweight
  have hexp : r - j.val - 1 + 1 = r - j.val := by omega
  simpa [laterPriorityScore, classes, hexp] using hsum

/-- For actual finite ranked classes, every global maximum-weight
    candidate is a maximum-weight choice for each deadline prefix. -/
theorem ranked_global_maximizer_maximizes_prefix
    [DecidableEq α] [DecidableEq β]
    (candidates : Finset β) (s r : Nat) (rank : α → Fin r)
    (remaining : Finset α) (hits : β → Finset α)
    (hcard : remaining.card ≤ s) (candidate : β) (hcandidate : candidate ∈ candidates)
    (hglobal : ∀ other ∈ candidates,
      fullPriorityScore s r rank remaining hits other ≤
        fullPriorityScore s r rank remaining hits candidate) :
    ∀ j : Fin r, ∀ other ∈ candidates,
      earlierPriorityScore s r rank j remaining hits other ≤
        earlierPriorityScore s r rank j remaining hits candidate := by
  intro j other hother
  apply global_maximizer_maximizes_prefix candidates
    (earlierPriorityScore s r rank j remaining hits)
    (laterPriorityScore s r rank j remaining hits) ((s + 1) ^ (r - j.val))
    (fun x hx => earlier_priority_score_divisible s r rank j remaining hits x)
    (fun x hx => later_priority_score_lt_unit s r rank j remaining hits x hcard)
    candidate hcandidate ?_ other hother
  · intro x hx
    rw [← full_priority_score_split s r rank j remaining hits x,
      ← full_priority_score_split s r rank j remaining hits candidate]
    exact hglobal x hx

end PlanarQuery.PriorityPrefix
