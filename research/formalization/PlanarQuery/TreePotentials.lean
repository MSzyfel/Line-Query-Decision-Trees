import PlanarQuery.Model
import PlanarQuery.Accounting
import Mathlib.Analysis.SpecialFunctions.Log.Basic

namespace PlanarQuery
namespace Tree

variable {H Q : Type*} [DecidableEq H]

theorem identification_log_height (M : QuerySystem H Q) (S : Finset H)
    (T : Tree H Q) (hId : Identifies M S T) (hne : S.Nonempty) :
    Real.log (S.card : ℝ) / Real.log 2 ≤ (height T : ℝ) := by
  have hcardPos : 0 < (S.card : ℝ) := Nat.cast_pos.mpr (Finset.card_pos.mpr hne)
  have hcap : (S.card : ℝ) ≤ (2 : ℝ) ^ height T := by
    have hcast : (S.card : ℝ) ≤ ((2 ^ height T : ℕ) : ℝ) :=
      Nat.cast_le.mpr (identification_capacity M S T hId)
    simpa only [Nat.cast_pow, Nat.cast_ofNat] using
      hcast
  have hlog := Real.log_le_log hcardPos hcap
  rw [Real.log_pow] at hlog
  exact (div_le_iff₀ (Real.log_pos (by norm_num : (1 : ℝ) < 2))).mpr hlog

def potentialDecreaseSum (M : QuerySystem H Q) (potential : Finset H → ℝ) :
    Tree H Q → Finset H → ℝ
  | .leaf _, _ => 0
  | .node q miss hit, S =>
      potential S - potential (branch M S q false) - potential (branch M S q true) +
      potentialDecreaseSum M potential miss (branch M S q false) +
      potentialDecreaseSum M potential hit (branch M S q true)

def leafPotentialSum (M : QuerySystem H Q) (potential : Finset H → ℝ) :
    Tree H Q → Finset H → ℝ
  | .leaf _, S => potential S
  | .node q miss hit, S =>
      leafPotentialSum M potential miss (branch M S q false) +
      leafPotentialSum M potential hit (branch M S q true)

/-- Potential cancellation follows the actual executable query branches. -/
theorem executable_potential_cancellation (M : QuerySystem H Q)
    (potential : Finset H → ℝ) (T : Tree H Q) (S : Finset H) :
    potentialDecreaseSum M potential T S =
      potential S - leafPotentialSum M potential T S := by
  induction T generalizing S with
  | leaf label => simp [potentialDecreaseSum, leafPotentialSum]
  | node q miss hit ihm ihh =>
    simp only [potentialDecreaseSum, leafPotentialSum, ihm, ihh]
    ring

theorem identifies_children (M : QuerySystem H Q) (S : Finset H)
    (q : Q) (miss hit : Tree H Q)
    (hId : Identifies M S (.node q miss hit)) :
    Identifies M (branch M S q false) miss ∧
      Identifies M (branch M S q true) hit := by
  constructor
  · intro h hh
    have hm := (mem_branch M S q false h).mp hh
    have hx := hId h hm.1
    simpa only [eval, hm.2, Bool.false_eq_true, if_false] using hx
  · intro h hh
    have hm := (mem_branch M S q true h).mp hh
    have hx := hId h hm.1
    simpa only [eval, hm.2, if_true] using hx

theorem terminal_potentials_zero (M : QuerySystem H Q)
    (potential : Finset H → ℝ) (T : Tree H Q) (S : Finset H)
    (hId : Identifies M S T) (hbase : ∀ U, U.card ≤ 1 → potential U = 0) :
    leafPotentialSum M potential T S = 0 := by
  induction T generalizing S with
  | leaf label =>
    have hcard := identification_capacity M S (.leaf label) hId
    simp only [height, pow_zero] at hcard
    exact hbase S hcard
  | node q miss hit ihm ihh =>
    have hc := identifies_children M S q miss hit hId
    simp only [leafPotentialSum, ihm _ hc.1, ihh _ hc.2, add_zero]

/-- Every potential vanishing on singleton/empty states telescopes to its
    root value on an actual identifying supplied-query tree. -/
theorem executable_potential_telescope (M : QuerySystem H Q)
    (potential : Finset H → ℝ) (T : Tree H Q) (S : Finset H)
    (hId : Identifies M S T) (hbase : ∀ U, U.card ≤ 1 → potential U = 0) :
    potentialDecreaseSum M potential T S = potential S := by
  rw [executable_potential_cancellation,
    terminal_potentials_zero M potential T S hId hbase, sub_zero]

end Tree
end PlanarQuery
