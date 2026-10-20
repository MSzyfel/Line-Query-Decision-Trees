import PlanarQuery.Model
import Mathlib.Data.Finset.Image
import Mathlib.Data.Finset.NAry
import Mathlib.Data.Finset.Max

namespace PlanarQuery
namespace Tree

variable {H Q : Type*} [Fintype H] [Fintype Q] [DecidableEq H] [DecidableEq Q]

/-- Exhaustive finite depth-bounded search. This deliberately formalizes
    completeness, not the paper's polynomial/quasipolynomial complexity. -/
def catalog : ℕ → Finset (Tree H Q)
  | 0 => Finset.univ.image Tree.leaf
  | k + 1 => Finset.univ.image Tree.leaf ∪
      Finset.univ.biUnion (fun q =>
        Finset.image₂ (Tree.node q) (catalog k) (catalog k))

theorem catalog_complete (T : Tree H Q) (k : ℕ) (hk : height T ≤ k) :
    T ∈ catalog k := by
  induction k generalizing T with
  | zero =>
    cases T with
    | leaf h => simp [catalog]
    | node q miss hit => simp [height] at hk
  | succ k ih =>
    cases T with
    | leaf h => simp [catalog]
    | node q miss hit =>
      have hm : height miss ≤ k := by simp only [height] at hk; omega
      have hh : height hit ≤ k := by simp only [height] at hk; omega
      apply Finset.mem_union_right
      apply Finset.mem_biUnion.mpr
      refine ⟨q, Finset.mem_univ q, ?_⟩
      exact Finset.mem_image₂.mpr ⟨miss, ih miss hm, hit, ih hit hh, rfl⟩

theorem catalog_sound (T : Tree H Q) (k : ℕ) (hk : T ∈ catalog k) :
    height T ≤ k := by
  induction k generalizing T with
  | zero =>
    obtain ⟨h, _, rfl⟩ := Finset.mem_image.mp hk
    simp [height]
  | succ k ih =>
    rcases Finset.mem_union.mp hk with hleaf | hnode
    · obtain ⟨h, _, rfl⟩ := Finset.mem_image.mp hleaf
      simp [height]
    · obtain ⟨q, _, hpair⟩ := Finset.mem_biUnion.mp hnode
      obtain ⟨miss, hm, hit, hh, rfl⟩ := Finset.mem_image₂.mp hpair
      have ihm := ih miss hm
      have ihh := ih hit hh
      simp only [height]
      omega

theorem mem_catalog_iff (T : Tree H Q) (k : ℕ) :
    T ∈ catalog k ↔ height T ≤ k :=
  ⟨catalog_sound T k, catalog_complete T k⟩

/-- A genuine finite minimum over a nonempty set of depth-bounded legal
    identifying trees. Its rational objective is the actual weighted cost. -/
theorem finite_expected_minimum (M : QuerySystem H Q) (weight : H → ℚ)
    (S : Finset H) (k : ℕ)
    (hfeasible : ∃ T, Identifies M S T ∧ height T ≤ k) :
    ∃ T ∈ catalog k, Identifies M S T ∧
      ∀ U ∈ catalog k, Identifies M S U →
        rawExpected M weight S T ≤ rawExpected M weight S U := by
  classical
  let valid := (catalog k).filter (Identifies M S)
  have hnonempty : valid.Nonempty := by
    obtain ⟨T, hId, hk⟩ := hfeasible
    exact ⟨T, Finset.mem_filter.mpr ⟨catalog_complete T k hk, hId⟩⟩
  obtain ⟨T, hT, hmin⟩ := valid.exists_min_image (rawExpected M weight S) hnonempty
  have hm := Finset.mem_filter.mp hT
  refine ⟨T, hm.1, hm.2, ?_⟩
  intro U hU hId
  exact hmin U (Finset.mem_filter.mpr ⟨hU, hId⟩)

end Tree
end PlanarQuery
