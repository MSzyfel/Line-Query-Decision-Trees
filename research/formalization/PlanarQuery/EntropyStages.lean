import PlanarQuery.Entropy

/-! Entropy charging for the balanced nodes of an actual executable tree.
Unbalanced nodes are retained in the tree and have zero balanced-cost invoice;
their nonnegative information is what permits the global bound. -/

namespace PlanarQuery.Entropy

variable {H Q : Type*} [DecidableEq H]

def BalancedAt (M : QuerySystem H Q) (w : H → ℝ) (δ : ℝ)
    (S : Finset H) (q : Q) : Prop :=
  δ ≤ mass w (Tree.branch M S q false) / mass w S ∧
    mass w (Tree.branch M S q false) / mass w S ≤ 1 - δ

noncomputable def balancedCost (M : QuerySystem H Q) (w : H → ℝ) (δ : ℝ) :
    Tree H Q → Finset H → ℝ
  | .leaf _, _ => 0
  | .node q miss hit, S => by
      classical
      exact (if BalancedAt M w δ S q then mass w S else 0) +
        balancedCost M w δ miss (Tree.branch M S q false) +
        balancedCost M w δ hit (Tree.branch M S q true)

theorem node_information_nonneg (M : QuerySystem H Q) (w : H → ℝ)
    (S : Finset H) (q : Q) (hw : ∀ h ∈ S, 0 ≤ w h) :
    0 ≤ weighted w S - weighted w (Tree.branch M S q false) -
      weighted w (Tree.branch M S q true) := by
  rw [weighted_branches M w S q]
  have hm := mass_nonneg w (Tree.branch M S q false)
    (fun h hh => hw h ((Tree.mem_branch M S q false h).mp hh).1)
  have hh := mass_nonneg w (Tree.branch M S q true)
    (fun h hh => hw h ((Tree.mem_branch M S q true h).mp hh).1)
  have hi := binaryInformation_nonneg _ _ hm hh
  linarith

theorem balanced_node_information (M : QuerySystem H Q) (w : H → ℝ)
    (δ : ℝ) (S : Finset H) (q : Q) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hδ0 : 0 ≤ δ) (hδhalf : δ ≤ 2⁻¹) (hb : BalancedAt M w δ S q) :
    mass w S * Real.binEntropy δ ≤ weighted w S -
      weighted w (Tree.branch M S q false) - weighted w (Tree.branch M S q true) := by
  have hm := mass_nonneg w (Tree.branch M S q false)
    (fun h hh => hw h ((Tree.mem_branch M S q false h).mp hh).1)
  have hh := mass_nonneg w (Tree.branch M S q true)
    (fun h hh => hw h ((Tree.mem_branch M S q true h).mp hh).1)
  have hi := binaryInformation_balanced_lower _ _ δ hm hh hδ0 hδhalf
    (by rw [← mass_branches M w S q]; exact hb.1)
    (by rw [← mass_branches M w S q]; exact hb.2)
  rw [← mass_branches M w S q] at hi
  rw [weighted_branches M w S q]
  linarith

/-- Every balanced query's live mass is charged to the actual entropy loss.
This assertion is valid for partial stages, without assuming identification. -/
theorem balanced_cost_information (M : QuerySystem H Q) (w : H → ℝ)
    (δ : ℝ) (T : Tree H Q) (S : Finset H) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hδ0 : 0 ≤ δ) (hδhalf : δ ≤ 2⁻¹) :
    balancedCost M w δ T S * Real.binEntropy δ ≤
      Tree.potentialDecreaseSum M (weighted w) T S := by
  classical
  induction T generalizing S with
  | leaf label => simp [balancedCost, Tree.potentialDecreaseSum]
  | node q miss hit ihm ihh =>
    have hm := ihm (Tree.branch M S q false)
      (fun h hh => hw h ((Tree.mem_branch M S q false h).mp hh).1)
    have hh := ihh (Tree.branch M S q true)
      (fun h hh => hw h ((Tree.mem_branch M S q true h).mp hh).1)
    simp only [balancedCost, Tree.potentialDecreaseSum]
    by_cases hb : BalancedAt M w δ S q
    · rw [if_pos hb]
      have hi := balanced_node_information M w δ S q hw hδ0 hδhalf hb
      nlinarith
    · rw [if_neg hb]
      have hi := node_information_nonneg M w S q hw
      nlinarith

theorem balanced_cost_partial_stage (M : QuerySystem H Q) (w : H → ℝ)
    (δ : ℝ) (T : Tree H Q) (S : Finset H) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hδ0 : 0 ≤ δ) (hδhalf : δ ≤ 2⁻¹) :
    balancedCost M w δ T S * Real.binEntropy δ ≤
      weighted w S - Tree.leafPotentialSum M (weighted w) T S := by
  rw [← Tree.executable_potential_cancellation]
  exact balanced_cost_information M w δ T S hw hδ0 hδhalf

theorem balanced_cost_identifying (M : QuerySystem H Q) (w : H → ℝ)
    (δ : ℝ) (T : Tree H Q) (S : Finset H) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hδ0 : 0 < δ) (hδhalf : δ ≤ 2⁻¹) (hId : Tree.Identifies M S T) :
    balancedCost M w δ T S ≤ weighted w S / Real.binEntropy δ := by
  have hh : δ < 1 := by norm_num at hδhalf; linarith
  have hp := Real.binEntropy_pos hδ0 hh
  apply (le_div_iff₀ hp).mpr
  rw [← executable_information_telescope M w S T hId]
  exact balanced_cost_information M w δ T S hw (le_of_lt hδ0) hδhalf

end PlanarQuery.Entropy
