import PlanarQuery.CodingConverse
import Mathlib.Data.Real.Basic
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Data.Rat.BigOperators

/-! The transcript-to-code bridge uses the actual supplied query answers and
stopping leaves. It does not assume that an arbitrary code can be implemented
by the query family. -/

namespace PlanarQuery.Coding

variable {H Q : Type*}

def transcript (M : QuerySystem H Q) : Tree H Q → H → List Bool
  | .leaf _, _ => []
  | .node q miss hit, h =>
      if M.answer q h then true :: transcript M hit h else false :: transcript M miss h

theorem transcript_length (M : QuerySystem H Q) (T : Tree H Q) (h : H) :
    (transcript M T h).length = Tree.depth M T h := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh =>
    cases he : M.answer q h <;> simp [transcript, Tree.depth, he, ihm, ihh, Nat.add_comm]

theorem transcript_prefix_eval_eq (M : QuerySystem H Q) (T : Tree H Q) (h k : H)
    (hp : transcript M T h <+: transcript M T k) : Tree.eval M T h = Tree.eval M T k := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh =>
    cases he : M.answer q h <;> cases ke : M.answer q k
    · simp only [transcript, he, ke, Bool.false_eq_true, if_false, List.cons_prefix_cons] at hp
      simpa [Tree.eval, he, ke] using ihm hp.2
    · simp [transcript, he, ke] at hp
    · simp [transcript, he, ke] at hp
    · simp only [transcript, he, ke, if_true, List.cons_prefix_cons] at hp
      simpa [Tree.eval, he, ke] using ihh hp.2

theorem identifying_transcripts_prefix_free (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (hId : Tree.Identifies M S T) : PrefixFree S (transcript M T) := by
  intro h hh k hk hne hp
  have he := transcript_prefix_eval_eq M T h k hp
  rw [hId h hh, hId k hk] at he
  exact hne he

theorem identifying_tree_kraft (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (hId : Tree.Identifies M S T) :
    ∑ h ∈ S, ((2 : ℚ)⁻¹) ^ Tree.depth M T h ≤ 1 := by
  have hk := kraft S (transcript M T) (identifying_transcripts_prefix_free M S T hId)
  simpa only [transcript_length] using hk

theorem identifying_tree_kraft_real (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (hId : Tree.Identifies M S T) :
    ∑ h ∈ S, ((2 : ℝ)⁻¹) ^ Tree.depth M T h ≤ 1 := by
  have hk := (Rat.cast_le (K := ℝ)).mpr (identifying_tree_kraft M S T hId)
  simpa only [Rat.cast_sum, Rat.cast_pow, Rat.cast_inv, Rat.cast_ofNat,
    Rat.cast_one] using hk

end PlanarQuery.Coding
