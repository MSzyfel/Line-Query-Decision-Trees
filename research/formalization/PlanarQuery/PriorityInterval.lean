import PlanarQuery.IntervalCover

/-! Exact interval facts used by the extremal step in the
maximum-remaining-weight greedy cover argument. -/

namespace PlanarQuery.PriorityInterval

open PlanarQuery.IntervalCover

/-- An active demand is hit when the selected position belongs to its
closed interval. -/
def HitsAt {D : Type*} (lo hi : D → Nat) (d : D) (q : Nat) : Prop :=
  lo d ≤ q ∧ q ≤ hi d

instance hitsAtDecidable {D : Type*} (lo hi : D → Nat) (d : D) (q : Nat) :
    Decidable (HitsAt lo hi d q) := inferInstanceAs (Decidable (lo d ≤ q ∧ q ≤ hi d))

/-- If a candidate is strictly to the left of a comparison cover, every
interval containing that candidate also contains the cover's leftmost
point, provided the interval is covered by the comparison set. -/
theorem extreme_hit_subset {D : Type*}
    (active : Finset D) (lo hi : D → Nat) (P : Finset Nat)
    (u : Nat) (hu : u ∈ P) (hleast : ∀ p ∈ P, u ≤ p)
    (v : Nat) (hv : v < u)
    (hcover : ∀ d ∈ active, ∃ p ∈ P, HitsAt lo hi d p)
    (d : D) (hd : d ∈ active) (hvit : HitsAt lo hi d v) :
    HitsAt lo hi d u := by
  obtain ⟨p, hpP, hpit⟩ := hcover d hd
  have hself : u ≤ u := hleast u hu
  have hleastp : u ≤ p := le_trans hself (hleast p hpP)
  exact ⟨le_trans hvit.1 (le_of_lt hv), le_trans hleastp hpit.2⟩

/-- The total remaining weight hit at an available position. Positive
weights are represented as natural numbers; only the coverage comparison
is needed here. -/
def hitWeight {D : Type*}
    (active : Finset D) (lo hi weight : D → Nat) (q : Nat) : Nat :=
  ∑ d ∈ active, if HitsAt lo hi d q then weight d else 0

/-- Moving an extreme candidate leftward cannot decrease the weight of
the demands it hits, when the comparison set covers every active demand. -/
theorem extreme_hitWeight_le {D : Type*}
    (active : Finset D) (lo hi weight : D → Nat) (P : Finset Nat)
    (u : Nat) (hu : u ∈ P) (hleast : ∀ p ∈ P, u ≤ p)
    (v : Nat) (hv : v < u)
    (hcover : ∀ d ∈ active, ∃ p ∈ P, HitsAt lo hi d p) :
    hitWeight active lo hi weight v ≤ hitWeight active lo hi weight u := by
  unfold hitWeight
  apply Finset.sum_le_sum
  intro d hd
  by_cases hhit : HitsAt lo hi d v
  · have huHit : HitsAt lo hi d u := extreme_hit_subset active lo hi P u hu hleast v hv hcover d hd hhit
    simp [hhit, huHit]
  · simp [hhit]

/-- If the extreme candidate and the greedy candidate both maximize
remaining hit weight, their scores are equal. This is the score part of
the exchange argument; equality of the hit demand sets additionally uses
strict positivity of every demand weight. -/
theorem extreme_maximizer_score_eq {D : Type*}
    (active : Finset D) (lo hi weight : D → Nat) (P : Finset Nat)
    (u : Nat) (hu : u ∈ P) (hleast : ∀ p ∈ P, u ≤ p)
    (v : Nat) (hv : v < u)
    (hcover : ∀ d ∈ active, ∃ p ∈ P, HitsAt lo hi d p)
    (hmax : ∀ q, hitWeight active lo hi weight q ≤ hitWeight active lo hi weight v) :
    hitWeight active lo hi weight u = hitWeight active lo hi weight v := by
  apply Nat.le_antisymm
  · exact hmax _
  · exact extreme_hitWeight_le active lo hi weight P u hu hleast v hv hcover

end PlanarQuery.PriorityInterval
