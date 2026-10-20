import PlanarQuery.TreePotentials
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-! Weighted Shannon entropy on finite live hypothesis states.  The definition
uses `negMulLog`, whose value at zero is zero, so empty states and zero weights
are treated by the same formulas as positive distributions. -/

namespace PlanarQuery.Entropy

variable {H Q : Type*} [DecidableEq H]

noncomputable def mass (w : H → ℝ) (S : Finset H) : ℝ := ∑ h ∈ S, w h

noncomputable def weighted (w : H → ℝ) (S : Finset H) : ℝ :=
  (∑ h ∈ S, Real.negMulLog (w h)) - Real.negMulLog (mass w S)

noncomputable def expected (M : QuerySystem H Q) (w : H → ℝ)
    (S : Finset H) (T : Tree H Q) : ℝ :=
  ∑ h ∈ S, w h * (Tree.depth M T h : ℝ)

noncomputable def binaryInformation (a b : ℝ) : ℝ :=
  Real.negMulLog a + Real.negMulLog b - Real.negMulLog (a + b)

omit [DecidableEq H] in
theorem mass_nonneg (w : H → ℝ) (S : Finset H)
    (hw : ∀ h ∈ S, 0 ≤ w h) : 0 ≤ mass w S := Finset.sum_nonneg hw

omit [DecidableEq H] in
theorem weight_le_mass (w : H → ℝ) (S : Finset H)
    (hw : ∀ h ∈ S, 0 ≤ w h) (h : H) (hh : h ∈ S) : w h ≤ mass w S :=
  Finset.single_le_sum hw hh

omit [DecidableEq H] in
@[simp] theorem weighted_empty (w : H → ℝ) : weighted w ∅ = 0 := by
  simp [weighted, mass]

omit [DecidableEq H] in
@[simp] theorem weighted_singleton (w : H → ℝ) (h : H) :
    weighted w {h} = 0 := by simp [weighted, mass]

omit [DecidableEq H] in
theorem weighted_card_le_one (w : H → ℝ) (S : Finset H)
    (hc : S.card ≤ 1) : weighted w S = 0 := by
  by_cases hn : S.Nonempty
  · obtain ⟨h, hh⟩ := hn
    have he : S = {h} := by
      ext x
      constructor
      · intro hx
        exact Finset.mem_singleton.mpr (Finset.card_le_one.mp hc x hx h hh)
      · intro hx
        exact (Finset.mem_singleton.mp hx) ▸ hh
    rw [he]; exact weighted_singleton w h
  · rw [Finset.not_nonempty_iff_eq_empty.mp hn]; exact weighted_empty w

theorem mass_union (w : H → ℝ) (A B : Finset H) (hd : Disjoint A B) :
    mass w (A ∪ B) = mass w A + mass w B := Finset.sum_union hd

theorem weighted_union (w : H → ℝ) (A B : Finset H) (hd : Disjoint A B) :
    weighted w (A ∪ B) = weighted w A + weighted w B +
      binaryInformation (mass w A) (mass w B) := by
  unfold weighted binaryInformation
  rw [mass_union w A B hd, Finset.sum_union hd]
  ring

theorem binaryInformation_eq (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    binaryInformation a b = (a + b) * Real.binEntropy (a / (a + b)) := by
  by_cases hz : a + b = 0
  · have ha0 : a = 0 := by linarith
    have hb0 : b = 0 := by linarith
    simp [ha0, hb0, binaryInformation]
  · have hratio : 1 - a / (a + b) = b / (a + b) := by field_simp
    have haa : a / (a + b) * (a + b) = a := div_mul_cancel₀ a hz
    have hbb : b / (a + b) * (a + b) = b := div_mul_cancel₀ b hz
    have hsum : a / (a + b) + b / (a + b) = 1 := by
      rw [← add_div, div_self hz]
    have ea := Real.negMulLog_mul (a / (a + b)) (a + b)
    have eb := Real.negMulLog_mul (b / (a + b)) (a + b)
    rw [haa] at ea
    rw [hbb] at eb
    rw [Real.binEntropy_eq_negMulLog_add_negMulLog_one_sub, hratio]
    unfold binaryInformation
    rw [ea, eb]
    calc
      _ = (a + b) * (Real.negMulLog (a / (a + b)) +
        Real.negMulLog (b / (a + b))) +
        (a / (a + b) + b / (a + b) - 1) * Real.negMulLog (a + b) := by ring
      _ = _ := by rw [hsum]; ring

theorem binaryInformation_nonneg (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    0 ≤ binaryInformation a b := by
  rw [binaryInformation_eq a b ha hb]
  by_cases hz : a + b = 0
  · simp [hz]
  · have hp : 0 < a + b := lt_of_le_of_ne (add_nonneg ha hb) (Ne.symm hz)
    exact mul_nonneg (le_of_lt hp) (Real.binEntropy_nonneg
      (div_nonneg ha (le_of_lt hp)) ((div_le_one hp).mpr (by linarith)))

theorem binaryInformation_le (a b : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b) :
    binaryInformation a b ≤ (a + b) * Real.log 2 := by
  rw [binaryInformation_eq a b ha hb]
  exact mul_le_mul_of_nonneg_left Real.binEntropy_le_log_two (add_nonneg ha hb)

theorem binEntropy_balanced_lower (δ t : ℝ) (hδ0 : 0 ≤ δ) (hδhalf : δ ≤ 2⁻¹)
    (ht0 : δ ≤ t) (ht1 : t ≤ 1 - δ) : Real.binEntropy δ ≤ Real.binEntropy t := by
  by_cases hthalf : t ≤ 2⁻¹
  · exact Real.binEntropy_strictMonoOn.monotoneOn ⟨hδ0, hδhalf⟩
      ⟨le_trans hδ0 ht0, hthalf⟩ ht0
  · have hl : 0 ≤ 1 - t := by linarith
    have hu : 1 - t ≤ 2⁻¹ := by norm_num at *; linarith
    have he := Real.binEntropy_strictMonoOn.monotoneOn
      ⟨hδ0, hδhalf⟩ ⟨hl, hu⟩ (by linarith : δ ≤ 1 - t)
    simpa only [Real.binEntropy_one_sub] using he

theorem binaryInformation_balanced_lower (a b δ : ℝ) (ha : 0 ≤ a) (hb : 0 ≤ b)
    (hδ0 : 0 ≤ δ) (hδhalf : δ ≤ 2⁻¹)
    (hl : δ ≤ a / (a + b)) (hu : a / (a + b) ≤ 1 - δ) :
    (a + b) * Real.binEntropy δ ≤ binaryInformation a b := by
  rw [binaryInformation_eq a b ha hb]
  exact mul_le_mul_of_nonneg_left (binEntropy_balanced_lower δ _ hδ0 hδhalf hl hu)
    (add_nonneg ha hb)

omit [DecidableEq H] in
theorem weighted_eq_normalized (w : H → ℝ) (S : Finset H) (hm : mass w S ≠ 0) :
    weighted w S = mass w S * ∑ h ∈ S, Real.negMulLog (w h / mass w S) := by
  have hs : ∑ h ∈ S, w h / mass w S = 1 := by
    rw [← Finset.sum_div]
    exact div_self hm
  have he : (∑ h ∈ S, Real.negMulLog (w h)) =
      ∑ h ∈ S, (mass w S * Real.negMulLog (w h / mass w S) +
        w h / mass w S * Real.negMulLog (mass w S)) := by
    apply Finset.sum_congr rfl
    intro h hh
    rw [← Real.negMulLog_mul, div_mul_cancel₀ _ hm]
  unfold weighted
  rw [he, Finset.sum_add_distrib, ← Finset.mul_sum, ← Finset.sum_mul, hs]
  ring

omit [DecidableEq H] in
theorem weighted_nonneg (w : H → ℝ) (S : Finset H) (hw : ∀ h ∈ S, 0 ≤ w h) :
    0 ≤ weighted w S := by
  by_cases hm : mass w S = 0
  · have hz : ∀ h ∈ S, w h = 0 := by
      intro h hh
      have he := weight_le_mass w S hw h hh
      rw [hm] at he
      exact le_antisymm he (hw h hh)
    simp [weighted, hm, Finset.sum_congr rfl (fun h hh => congrArg Real.negMulLog (hz h hh))]
  · have hp : 0 < mass w S := lt_of_le_of_ne (mass_nonneg w S hw) (Ne.symm hm)
    rw [weighted_eq_normalized w S hm]
    apply mul_nonneg (le_of_lt hp)
    apply Finset.sum_nonneg
    intro h hh
    exact Real.negMulLog_nonneg (div_nonneg (hw h hh) (le_of_lt hp))
      ((div_le_one hp).mpr (weight_le_mass w S hw h hh))

omit [DecidableEq H] in
theorem weighted_eq_log_ratio (w : H → ℝ) (S : Finset H)
    (hw : ∀ h ∈ S, 0 ≤ w h) :
    weighted w S = ∑ h ∈ S, w h * Real.log (mass w S / w h) := by
  by_cases hm : mass w S = 0
  · have hz : ∀ h ∈ S, w h = 0 := by
      intro h hh
      have he := weight_le_mass w S hw h hh
      rw [hm] at he
      exact le_antisymm he (hw h hh)
    simp [weighted, hm, Finset.sum_congr rfl (fun h hh => congrArg Real.negMulLog (hz h hh))]
  · rw [weighted_eq_normalized w S hm, Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro h hh
    by_cases hz : w h = 0
    · simp [hz]
    · rw [Real.negMulLog, Real.log_div hz hm, Real.log_div hm hz]
      field_simp
      ring

theorem mass_branches (M : QuerySystem H Q) (w : H → ℝ) (S : Finset H) (q : Q) :
    mass w S = mass w (Tree.branch M S q false) +
      mass w (Tree.branch M S q true) := by
  conv_lhs => rw [← Tree.branches_union M S q]
  exact mass_union w _ _ (Tree.branches_disjoint M S q)

theorem weighted_branches (M : QuerySystem H Q) (w : H → ℝ) (S : Finset H) (q : Q) :
    weighted w S = weighted w (Tree.branch M S q false) +
      weighted w (Tree.branch M S q true) +
      binaryInformation (mass w (Tree.branch M S q false))
        (mass w (Tree.branch M S q true)) := by
  conv_lhs => rw [← Tree.branches_union M S q]
  exact weighted_union w _ _ (Tree.branches_disjoint M S q)

theorem expected_node (M : QuerySystem H Q) (w : H → ℝ) (S : Finset H)
    (q : Q) (miss hit : Tree H Q) :
    expected M w S (.node q miss hit) = mass w S +
      expected M w (Tree.branch M S q false) miss +
      expected M w (Tree.branch M S q true) hit := by
  classical
  unfold expected mass Tree.branch
  rw [Finset.sum_filter, Finset.sum_filter]
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro h hh
  cases he : M.answer q h <;> simp [Tree.depth, he, Nat.cast_add] <;> ring

/-- The entropy lower bound is proved on the actual tree by induction;
every node has at most one bit of information, weighted by its live mass. -/
theorem weighted_le_expected_log_two (M : QuerySystem H Q) (w : H → ℝ)
    (S : Finset H) (T : Tree H Q) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hId : Tree.Identifies M S T) :
    weighted w S ≤ expected M w S T * Real.log 2 := by
  induction T generalizing S with
  | leaf label =>
    have hc := Tree.identification_capacity M S (.leaf label) hId
    simp only [Tree.height, pow_zero] at hc
    rw [weighted_card_le_one w S hc]
    simp [expected, Tree.depth]
  | node q miss hit ihm ihh =>
    have hc := Tree.identifies_children M S q miss hit hId
    have hwm : ∀ h ∈ Tree.branch M S q false, 0 ≤ w h :=
      fun h hh => hw h ((Tree.mem_branch M S q false h).mp hh).1
    have hwh : ∀ h ∈ Tree.branch M S q true, 0 ≤ w h :=
      fun h hh => hw h ((Tree.mem_branch M S q true h).mp hh).1
    have hm := ihm _ hwm hc.1
    have hh := ihh _ hwh hc.2
    have hi := binaryInformation_le _ _ (mass_nonneg w _ hwm) (mass_nonneg w _ hwh)
    rw [weighted_branches M w S q, expected_node M w S q miss hit]
    rw [← mass_branches M w S q] at hi
    nlinarith

theorem weighted_div_log_two_le_expected (M : QuerySystem H Q) (w : H → ℝ)
    (S : Finset H) (T : Tree H Q) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hId : Tree.Identifies M S T) :
    weighted w S / Real.log 2 ≤ expected M w S T := by
  exact (div_le_iff₀ (Real.log_pos (by norm_num : (1 : ℝ) < 2))).mpr
    (weighted_le_expected_log_two M w S T hw hId)

/-- Information decreases telescope to the root entropy, without discarding
zero-probability states or replacing supplied queries by arbitrary splits. -/
theorem executable_information_telescope (M : QuerySystem H Q) (w : H → ℝ)
    (S : Finset H) (T : Tree H Q) (hId : Tree.Identifies M S T) :
    Tree.potentialDecreaseSum M (weighted w) T S = weighted w S :=
  Tree.executable_potential_telescope M (weighted w) T S hId
    (weighted_card_le_one w)

theorem expected_rational_cast (M : QuerySystem H Q) (w : H → ℚ)
    (S : Finset H) (T : Tree H Q) :
    expected M (fun h => (w h : ℝ)) S T = (Tree.rawExpected M w S T : ℝ) := by
  simp [expected, Tree.rawExpected]

/-- Direct bridge to the paper's existing rational raw expected-cost model. -/
theorem rational_entropy_lower_bound (M : QuerySystem H Q) (w : H → ℚ)
    (S : Finset H) (T : Tree H Q) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hId : Tree.Identifies M S T) :
    (∑ h ∈ S, (w h : ℝ) * Real.log (mass (fun h => (w h : ℝ)) S / (w h : ℝ))) /
      Real.log 2 ≤ (Tree.rawExpected M w S T : ℝ) := by
  have hwr : ∀ h ∈ S, 0 ≤ (w h : ℝ) := fun h hh => by exact_mod_cast hw h hh
  rw [← weighted_eq_log_ratio _ S hwr, ← expected_rational_cast]
  exact weighted_div_log_two_le_expected M _ S T hwr hId

end PlanarQuery.Entropy
