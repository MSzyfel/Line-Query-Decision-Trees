import PlanarQuery.Majority

namespace PlanarQuery

/-- Strict geometric answer side. Off-line hypotheses make both Boolean
    outcomes open half-planes, rather than one open and one closed side. -/
def RationalLine.strictSide (line : RationalLine) (point : ℚ × ℚ) (b : Bool) : Prop :=
  if b then line.c < line.a * point.1 + line.b * point.2
  else line.a * point.1 + line.b * point.2 < line.c

theorem PlanarInstance.strict_query_semantics {n m : ℕ} (I : PlanarInstance n m)
    (q : Fin m) (h : Fin n) (b : Bool) :
    I.querySystem.answer q h = b ↔ (I.line q).strictSide (I.point h) b := by
  cases b
  · change decide ((I.line q).c < (I.line q).a * (I.point h).1 +
        (I.line q).b * (I.point h).2) = false ↔
        (I.line q).a * (I.point h).1 + (I.line q).b * (I.point h).2 < (I.line q).c
    simp only [decide_eq_false_iff_not]
    constructor
    · intro hn
      exact lt_of_le_of_ne (le_of_not_gt hn) (I.offLine q h)
    · intro hl
      exact not_lt_of_ge hl.le
  · exact I.query_semantics q h

/-- A common majority answer is an actual strict rational planar witness
    for all three supplied half-planes. Duplicate queries are permitted,
    so this also handles one- and two-element nonempty subfamilies. -/
theorem PlanarInstance.three_majority_strict_point {n m : ℕ} (I : PlanarInstance n m)
    (S : Finset (Fin n)) (hS : S.Nonempty)
    (q₁ q₂ q₃ : Fin m) (minor₁ minor₂ minor₃ : Bool)
    (delta : ℚ) (hdelta : delta < (1 : ℚ) / 3)
    (h₁ : Tree.mass I.weight (Tree.branch I.querySystem S q₁ minor₁) < delta * Tree.mass I.weight S)
    (h₂ : Tree.mass I.weight (Tree.branch I.querySystem S q₂ minor₂) < delta * Tree.mass I.weight S)
    (h₃ : Tree.mass I.weight (Tree.branch I.querySystem S q₃ minor₃) < delta * Tree.mass I.weight S) :
    ∃ point : ℚ × ℚ, (I.line q₁).strictSide point (!minor₁) ∧
      (I.line q₂).strictSide point (!minor₂) ∧ (I.line q₃).strictSide point (!minor₃) := by
  obtain ⟨h, hh⟩ := three_minority_branches_intersect I.querySystem I.weight S
    q₁ q₂ q₃ minor₁ minor₂ minor₃ hS (fun h _ => I.positive h) delta hdelta h₁ h₂ h₃
  have hp := Finset.mem_inter.mp hh
  have hp₁ := (Tree.mem_branch _ _ _ _ _).mp (Finset.mem_inter.mp hp.1).1
  have hp₂ := (Tree.mem_branch _ _ _ _ _).mp (Finset.mem_inter.mp hp.1).2
  have hp₃ := (Tree.mem_branch _ _ _ _ _).mp hp.2
  exact ⟨I.point h, (I.strict_query_semantics _ _ _).mp hp₁.2,
    (I.strict_query_semantics _ _ _).mp hp₂.2, (I.strict_query_semantics _ _ _).mp hp₃.2⟩

theorem nonempty_card_le_three_cover {Q : Type*} [DecidableEq Q]
    (F : Finset Q) (hF : F.Nonempty) (hc : F.card ≤ 3) :
    ∃ q₁ q₂ q₃, q₁ ∈ F ∧ q₂ ∈ F ∧ q₃ ∈ F ∧ F ⊆ {q₁, q₂, q₃} := by
  have hp := Finset.card_pos.mpr hF
  have hcases : F.card = 1 ∨ F.card = 2 ∨ F.card = 3 := by omega
  rcases hcases with h | h | h
  · obtain ⟨q, rfl⟩ := Finset.card_eq_one.mp h
    exact ⟨q, q, q, by simp, by simp, by simp, by simp⟩
  · obtain ⟨q₁, q₂, _, rfl⟩ := Finset.card_eq_two.mp h
    exact ⟨q₁, q₂, q₂, by simp, by simp, by simp, by simp⟩
  · obtain ⟨q₁, q₂, q₃, _, _, _, rfl⟩ := Finset.card_eq_three.mp h
    exact ⟨q₁, q₂, q₃, by simp, by simp, by simp, by simp⟩

/-- Every subfamily of at most three majority half-planes intersects.
    This includes the empty subfamily, and the witness is rational. -/
theorem PlanarInstance.small_majority_family_intersects {n m : ℕ}
    (I : PlanarInstance n m) (S : Finset (Fin n)) (hS : S.Nonempty)
    (F : Finset (Fin m)) (majority : Fin m → Bool) (hcard : F.card ≤ 3)
    (delta : ℚ) (hdelta : delta < (1 : ℚ) / 3)
    (hminor : ∀ q ∈ F, Tree.mass I.weight (Tree.branch I.querySystem S q (!majority q)) <
      delta * Tree.mass I.weight S) :
    ∃ point : ℚ × ℚ, ∀ q ∈ F, (I.line q).strictSide point (majority q) := by
  by_cases hF : F.Nonempty
  · obtain ⟨q₁, q₂, q₃, h₁, h₂, h₃, hcover⟩ := nonempty_card_le_three_cover F hF hcard
    obtain ⟨point, hp₁, hp₂, hp₃⟩ := I.three_majority_strict_point S hS q₁ q₂ q₃
      (!majority q₁) (!majority q₂) (!majority q₃) delta hdelta
      (hminor q₁ h₁) (hminor q₂ h₂) (hminor q₃ h₃)
    simp only [Bool.not_not] at hp₁ hp₂ hp₃
    refine ⟨point, ?_⟩
    intro q hq
    have hmem := hcover hq
    simp only [Finset.mem_insert, Finset.mem_singleton] at hmem
    rcases hmem with rfl | rfl | rfl
    · exact hp₁
    · exact hp₂
    · exact hp₃
  · have he : F = ∅ := Finset.not_nonempty_iff_eq_empty.mp hF
    exact ⟨(0, 0), by simp [he]⟩

end PlanarQuery
