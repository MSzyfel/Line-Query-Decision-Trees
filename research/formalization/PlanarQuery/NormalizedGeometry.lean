import PlanarQuery.Helly

namespace PlanarQuery

/-- Translation relative to the common witness. -/
def translatePoint (p x : ℚ × ℚ) : ℚ × ℚ := (x.1 - p.1, x.2 - p.2)

/-- The denominator is signed: division reverses the cap orientation
exactly when the witness lies on the positive side. -/
def RationalLine.normalizedAt (line : RationalLine) (p : ℚ × ℚ) : ℚ × ℚ :=
  (line.a / (line.c - line.linearPart p), line.b / (line.c - line.linearPart p))

theorem RationalLine.normalized_dot (line : RationalLine) (p x : ℚ × ℚ) :
    rationalDot (line.normalizedAt p) (translatePoint p x) =
      (line.linearPart x - line.linearPart p) / (line.c - line.linearPart p) := by
  simp only [rationalDot, normalizedAt, translatePoint, linearPart, LinearMap.coe_mk,
    AddHom.coe_mk]
  ring

/-- Actual original-line minority answers are exactly normalized caps.
The premise is strictness of the witness, not a cap-cover assumption. -/
theorem RationalLine.normalized_cap_iff (line : RationalLine) (p x : ℚ × ℚ)
    (b : Bool) (hp : line.strictSide p b) :
    1 < rationalDot (line.normalizedAt p) (translatePoint p x) ↔
      line.strictSide x (!b) := by
  rw [normalized_dot]
  cases b
  · change line.linearPart p < line.c at hp
    have hd : 0 < line.c - line.linearPart p := sub_pos.mpr hp
    rw [one_lt_div hd]
    change line.c - line.linearPart p < line.linearPart x - line.linearPart p ↔
      line.c < line.linearPart x
    exact sub_lt_sub_iff_right _
  · change line.c < line.linearPart p at hp
    have hd : line.c - line.linearPart p < 0 := sub_neg.mpr hp
    rw [one_lt_div_of_neg hd]
    change line.linearPart x - line.linearPart p < line.c - line.linearPart p ↔
      line.linearPart x < line.c
    exact sub_lt_sub_iff_right _

/-- Cap domination follows directly from convex-hull containment. This
also works with many supports, with the origin treated as a free support. -/
theorem convexHull_cap_domination (V : Finset (ℚ × ℚ)) (u x : ℚ × ℚ)
    (hu : u ∈ convexHull ℚ (insert 0 (V : Set (ℚ × ℚ))))
    (hV : ∀ v ∈ V, rationalDot v x ≤ 1) : rationalDot u x ≤ 1 := by
  let f : (ℚ × ℚ) →ₗ[ℚ] ℚ :=
    { toFun := fun v => rationalDot v x
      map_add' := by intro v w; simp [rationalDot]; ring
      map_smul' := by intro a v; simp [rationalDot]; ring }
  apply convexHull_min (t := {v | rationalDot v x ≤ 1}) ?_
    (convex_halfSpace_le f.isLinear 1) hu
  intro v hv
  rcases hv with rfl | hv
  · simp [rationalDot]
  · exact hV v hv

/-- With a separating query family, at most one hypothesis has the
common witness's complete answer vector. -/
theorem QuerySystem.same_answers_unique {H Q : Type*} (M : QuerySystem H Q)
    (separates : ∀ a b : H, a ≠ b → ∃ q, M.answer q a ≠ M.answer q b)
    (bits : Q → Bool) (a b : H) (ha : ∀ q, M.answer q a = bits q)
    (hb : ∀ q, M.answer q b = bits q) : a = b := by
  by_contra hn
  obtain ⟨q, hq⟩ := separates a b hn
  exact hq ((ha q).trans (hb q).symm)

/-- The all-zero hull pattern forces all original majority answers.
Hull containment is explicit; no two-support expression is assumed. -/
theorem PlanarInstance.zero_pattern_forces_majority {n m : ℕ}
    (I : PlanarInstance n m) (p : ℚ × ℚ) (majority : Fin m → Bool)
    (hp : ∀ q, (I.line q).strictSide p (majority q))
    (V : Finset (Fin m))
    (hhull : ∀ q, (I.line q).normalizedAt p ∈
      convexHull ℚ (insert 0 ((fun v => (I.line v).normalizedAt p) '' (V : Set (Fin m)))))
    (h : Fin n) (hzero : ∀ v ∈ V,
      rationalDot ((I.line v).normalizedAt p) (translatePoint p (I.point h)) ≤ 1) :
    ∀ q, I.querySystem.answer q h = majority q := by
  intro q
  have hbound := convexHull_cap_domination
    (V.image (fun v => (I.line v).normalizedAt p)) ((I.line q).normalizedAt p)
    (translatePoint p (I.point h)) (by simpa using hhull q) (by
      intro u hu
      obtain ⟨v, hv, rfl⟩ := Finset.mem_image.mp hu
      exact hzero v hv)
  have hn : ¬ (I.line q).strictSide (I.point h) (!majority q) := by
    intro hm
    have hc := ((I.line q).normalized_cap_iff p (I.point h) (majority q) (hp q)).mpr hm
    exact not_lt_of_ge hbound hc
  have hb : I.querySystem.answer q h ≠ !majority q := by
    intro he
    exact hn ((I.strict_query_semantics q h (!majority q)).mp he)
  cases hm : majority q <;> cases ha : I.querySystem.answer q h <;> simp_all

end PlanarQuery
