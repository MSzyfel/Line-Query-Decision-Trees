import PlanarQuery.PlanarSemantics
import Mathlib.Analysis.Convex.Radon
import Mathlib.LinearAlgebra.Dimension.Constructions

/-! Helly is applied over the rational field itself. Consequently the
common witness has rational coordinates without a density argument.
This module proves geometric existence, separately from the polynomial
bit complexity and running time of a linear-programming implementation. -/

namespace PlanarQuery

/-- The finite planar Helly theorem, including empty families. -/
theorem planar_helly {𝕜 : Type*} [Field 𝕜] [LinearOrder 𝕜]
    [IsStrictOrderedRing 𝕜] {ι : Type*} [DecidableEq ι]
    (F : ι → Set (𝕜 × 𝕜)) (s : Finset ι)
    (hc : ∀ i ∈ s, Convex 𝕜 (F i))
    (hi : ∀ t ⊆ s, t.card ≤ 3 → (⋂ i ∈ t, F i).Nonempty) :
    (⋂ i ∈ s, F i).Nonempty := by
  apply Convex.helly_theorem' hc
  intro t ht hn
  apply hi t ht
  simpa only [Module.finrank_prod, Module.finrank_self] using hn

/-- A rational line's homogeneous part is an actual linear map. -/
def RationalLine.linearPart (line : RationalLine) : (ℚ × ℚ) →ₗ[ℚ] ℚ where
  toFun p := line.a * p.1 + line.b * p.2
  map_add' x y := by simp only [Prod.fst_add, Prod.snd_add]; ring
  map_smul' a x := by
    simp only [Prod.smul_fst, Prod.smul_snd, smul_eq_mul, RingHom.id_apply]
    ring

/-- Both strict answer sides of every supplied rational line are convex. -/
theorem RationalLine.strictSide_convex (line : RationalLine) (b : Bool) :
    Convex ℚ {p | line.strictSide p b} := by
  cases b
  · exact convex_halfSpace_lt line.linearPart.isLinear line.c
  · exact convex_halfSpace_gt line.linearPart.isLinear line.c

/-- All majority sides, rather than only triples, share a strict rational
point. This is the geometric preprocessing guarantee in the actual model. -/
theorem PlanarInstance.majority_strict_point {n m : ℕ}
    (I : PlanarInstance n m) (S : Finset (Fin n)) (hS : S.Nonempty)
    (F : Finset (Fin m)) (majority : Fin m → Bool)
    (delta : ℚ) (hdelta : delta < (1 : ℚ) / 3)
    (hminor : ∀ q ∈ F,
      Tree.mass I.weight (Tree.branch I.querySystem S q (!majority q)) <
        delta * Tree.mass I.weight S) :
    ∃ point : ℚ × ℚ, ∀ q ∈ F, (I.line q).strictSide point (majority q) := by
  let sides : Fin m → Set (ℚ × ℚ) := fun q =>
    {p | (I.line q).strictSide p (majority q)}
  have hex : (⋂ q ∈ F, sides q).Nonempty := by
    apply planar_helly sides F
    · intro q _
      exact (I.line q).strictSide_convex (majority q)
    · intro t ht hcard
      obtain ⟨p, hp⟩ := I.small_majority_family_intersects S hS t majority
        hcard delta hdelta (fun q hq => hminor q (ht hq))
      exact ⟨p, Set.mem_iInter.mpr (fun q =>
        Set.mem_iInter.mpr (fun hq => hp q hq))⟩
  obtain ⟨p, hp⟩ := hex
  exact ⟨p, fun q hq => Set.mem_iInter.mp (Set.mem_iInter.mp hp q) hq⟩

end PlanarQuery
