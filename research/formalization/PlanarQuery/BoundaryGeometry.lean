import PlanarQuery.Boundary
import PlanarQuery.PlanarSemantics

namespace PlanarQuery

/-- Every finite rational value family has a positive rational margin
below every nonzero absolute value, including the all-zero case. -/
theorem finite_rational_margin {H : Type*} [DecidableEq H]
    (S : Finset H) (value : H → ℚ) :
    ∃ e : ℚ, 0 < e ∧ ∀ h ∈ S, value h ≠ 0 → e < |value h| := by
  induction S using Finset.induction_on with
  | empty => exact ⟨1, by norm_num, by simp⟩
  | @insert a S ha ih =>
    obtain ⟨e, he, hgap⟩ := ih
    by_cases hz : value a = 0
    · refine ⟨e, he, ?_⟩
      intro h hh hn
      rcases Finset.mem_insert.mp hh with rfl | hh
      · exact False.elim (hn hz)
      · exact hgap h hh hn
    · have hv : 0 < |value a| := abs_pos.mpr hz
      refine ⟨min e (|value a| / 2), lt_min he (div_pos hv (by norm_num)), ?_⟩
      intro h hh hn
      rcases Finset.mem_insert.mp hh with rfl | hh
      · exact (min_le_right _ _).trans_lt (by linarith)
      · exact (min_le_left _ _).trans_lt (hgap h hh hn)

/-- A strict rational margin realizes both virtual predicates and keeps
both shifted boundaries off every hypothesis. -/
theorem shifted_virtual_predicates (v e : ℚ) (he : 0 < e)
    (hgap : v ≠ 0 → e < |v|) :
    (v < -e ↔ v < 0) ∧ (v < e ↔ v ≤ 0) ∧ v ≠ -e ∧ v ≠ e := by
  by_cases hn : v < 0
  · have hz : v ≠ 0 := ne_of_lt hn
    have hg := hgap hz
    rw [abs_of_neg hn] at hg
    constructor
    · constructor <;> intro h <;> linarith
    constructor
    · constructor <;> intro h <;> linarith
    constructor <;> intro h <;> linarith
  · have hv : 0 ≤ v := le_of_not_gt hn
    by_cases hz : v = 0
    · subst v
      constructor
      · constructor <;> intro h <;> linarith
      constructor
      · constructor <;> intro h <;> linarith
      constructor <;> intro h <;> linarith
    · have hg := hgap hz
      rw [abs_of_nonneg hv] at hg
      constructor
      · constructor <;> intro h <;> linarith
      constructor
      · constructor <;> intro h <;> linarith
      constructor <;> intro h <;> linarith

def RationalLine.affineValue (line : RationalLine) (p : ℚ × ℚ) :=
  line.a * p.1 + line.b * p.2 - line.c

/-- Sign-reversal makes Model's positive Boolean answer the requested
negative predicate. False requests f<0, true requests f<=0. -/
def RationalLine.virtualShift (line : RationalLine) (e : ℚ) (bit : Bool) : RationalLine where
  a := -line.a
  b := -line.b
  c := -line.c + (if bit then -e else e)
  nonzero := by
    rcases line.nonzero with ha | hb
    · exact Or.inl (neg_ne_zero.mpr ha)
    · exact Or.inr (neg_ne_zero.mpr hb)

theorem RationalLine.virtualShift_semantics (line : RationalLine) (p : ℚ × ℚ)
    (e : ℚ) (he : 0 < e) (hgap : line.affineValue p ≠ 0 → e < |line.affineValue p|)
    (bit : Bool) :
    ((line.virtualShift e bit).c <
      (line.virtualShift e bit).a * p.1 + (line.virtualShift e bit).b * p.2) ↔
    (if bit then line.affineValue p ≤ 0 else line.affineValue p < 0) := by
  have hs := shifted_virtual_predicates (line.affineValue p) e he hgap
  cases bit
  · simp only [virtualShift, Bool.false_eq_true, if_false]
    have heq : (-line.c + e < -line.a * p.1 + -line.b * p.2) ↔
        line.affineValue p < -e := by unfold affineValue; constructor <;> intro h <;> linarith
    exact heq.trans hs.1
  · simp only [virtualShift, if_true]
    have heq : (-line.c + -e < -line.a * p.1 + -line.b * p.2) ↔
        line.affineValue p < e := by unfold affineValue; constructor <;> intro h <;> linarith
    exact heq.trans hs.2.1

theorem RationalLine.virtualShift_offLine (line : RationalLine) (p : ℚ × ℚ)
    (e : ℚ) (he : 0 < e) (hgap : line.affineValue p ≠ 0 → e < |line.affineValue p|)
    (bit : Bool) :
    (line.virtualShift e bit).a * p.1 + (line.virtualShift e bit).b * p.2 ≠
      (line.virtualShift e bit).c := by
  have hs := shifted_virtual_predicates (line.affineValue p) e he hgap
  cases bit
  · intro h
    apply hs.2.2.1
    simp only [virtualShift, Bool.false_eq_true, if_false] at h
    unfold affineValue
    linarith
  · intro h
    apply hs.2.2.2
    simp only [virtualShift, if_true] at h
    unfold affineValue
    linarith

end PlanarQuery
