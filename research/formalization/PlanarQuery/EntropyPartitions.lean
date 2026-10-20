import PlanarQuery.Entropy

/-! Finite partition information and Shannon chain rules. Random variables are
actual functions of the hypothesis; the conditional quantities use their
actual fibers and the original, unnormalized weights. -/

namespace PlanarQuery.Entropy

variable {H Y Z W : Type*}

def fiber [DecidableEq Y] (S : Finset H) (f : H → Y) (y : Y) : Finset H :=
  S.filter (fun h => f h = y)

theorem sum_fiber [Fintype Y] [DecidableEq Y] (S : Finset H) (f : H → Y)
    (a : H → ℝ) :
    (∑ y, ∑ h ∈ fiber S f y, a h) = ∑ h ∈ S, a h := by
  simp only [fiber, Finset.sum_filter]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro h hh
  simp

noncomputable def information [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) : ℝ :=
  weighted (fun y => mass w (fiber S f y)) Finset.univ

noncomputable def conditionalWeighted [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) : ℝ :=
  ∑ y, weighted w (fiber S f y)

noncomputable def conditionalInformation [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (g : H → Z) : ℝ :=
  ∑ z, information w (fiber S g z) f

theorem information_eq [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) :
    information w S f = (∑ y, Real.negMulLog (mass w (fiber S f y))) -
      Real.negMulLog (mass w S) := by
  unfold information weighted
  have he : mass (fun y => mass w (fiber S f y)) Finset.univ = mass w S :=
    sum_fiber S f w
  rw [he]

theorem information_normalized [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (hm : mass w S = 1) :
    information w S f = ∑ y, Real.negMulLog (mass w (fiber S f y)) := by
  rw [information_eq, hm, Real.negMulLog_one, sub_zero]

/-- Unnormalized chain rule for an arbitrary finite partition of a live state. -/
theorem weighted_chain_rule [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) :
    weighted w S = information w S f + conditionalWeighted w S f := by
  rw [information_eq]
  unfold conditionalWeighted weighted
  rw [Finset.sum_sub_distrib, sum_fiber S f (fun h => Real.negMulLog (w h))]
  ring

theorem information_nonneg [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (hw : ∀ h ∈ S, 0 ≤ w h) :
    0 ≤ information w S f := by
  apply weighted_nonneg
  intro y hy
  apply mass_nonneg
  intro h hh
  exact hw h (Finset.mem_filter.mp hh).1

theorem conditionalWeighted_nonneg [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (hw : ∀ h ∈ S, 0 ≤ w h) :
    0 ≤ conditionalWeighted w S f := by
  apply Finset.sum_nonneg
  intro y hy
  apply weighted_nonneg
  intro h hh
  exact hw h (Finset.mem_filter.mp hh).1

theorem conditionalInformation_nonneg [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (g : H → Z) (hw : ∀ h ∈ S, 0 ≤ w h) :
    0 ≤ conditionalInformation w S f g := by
  apply Finset.sum_nonneg
  intro z hz
  apply information_nonneg
  intro h hh
  exact hw h (Finset.mem_filter.mp hh).1

theorem information_le_weighted [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (hw : ∀ h ∈ S, 0 ≤ w h) :
    information w S f ≤ weighted w S := by
  have hc := conditionalWeighted_nonneg w S f hw
  rw [weighted_chain_rule w S f]
  linarith

theorem fiber_fiber [DecidableEq Y] [DecidableEq Z]
    (S : Finset H) (f : H → Y) (g : H → Z) (y : Y) (z : Z) :
    fiber (fiber S g z) f y = fiber S (fun h => (f h, g h)) (y, z) := by
  ext h
  simp [fiber, and_assoc, and_left_comm, and_comm]

/-- Shannon's chain rule for two finite random variables, using their actual
joint distribution. It holds without normalization, including zero fibers. -/
theorem joint_information_chain_rule [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (g : H → Z) :
    information w S (fun h => (f h, g h)) =
      information w S g + conditionalInformation w S f g := by
  unfold conditionalInformation
  simp_rw [information_eq, fiber_fiber]
  rw [Finset.sum_sub_distrib]
  have hs : (∑ p : Y × Z, Real.negMulLog (mass w
      (fiber S (fun h => (f h, g h)) p))) =
      ∑ z : Z, ∑ y : Y, Real.negMulLog (mass w
        (fiber S (fun h => (f h, g h)) (y, z))) := by
    rw [Fintype.sum_prod_type, Finset.sum_comm]
  rw [hs]
  ring

theorem joint_information_symmetric [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (g : H → Z) :
    information w S (fun h => (f h, g h)) = information w S (fun h => (g h, f h)) := by
  rw [information_eq, information_eq]
  congr 1
  rw [Fintype.sum_prod_type, Fintype.sum_prod_type, Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro z hz
  apply Finset.sum_congr rfl
  intro y hy
  congr 2
  ext h
  simp [fiber, and_comm]

/-- The conditional chain rule is obtained by applying the ordinary chain
rule separately on each actual conditioning fiber, then summing. -/
theorem conditional_joint_chain_rule [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] [Fintype W] [DecidableEq W]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (g : H → Z) (k : H → W) :
    conditionalInformation w S (fun h => (f h, g h)) k =
      conditionalInformation w S g k +
        ∑ c, conditionalInformation w (fiber S k c) f g := by
  unfold conditionalInformation
  simp_rw [joint_information_chain_rule]
  rw [Finset.sum_add_distrib]
  rfl

theorem conditional_pair_eq_sum [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] [Fintype W] [DecidableEq W]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (g : H → Z) (k : H → W) :
    conditionalInformation w S f (fun h => (g h, k h)) =
      ∑ c, conditionalInformation w (fiber S k c) f g := by
  unfold conditionalInformation
  simp_rw [fiber_fiber]
  rw [Fintype.sum_prod_type, Finset.sum_comm]

theorem shannon_conditional_chain_rule [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] [Fintype W] [DecidableEq W]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (g : H → Z) (k : H → W) :
    conditionalInformation w S (fun h => (f h, g h)) k =
      conditionalInformation w S g k +
        conditionalInformation w S f (fun h => (g h, k h)) := by
  rw [conditional_pair_eq_sum]
  exact conditional_joint_chain_rule w S f g k

theorem shannon_conditional_chain_rule_left [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] [Fintype W] [DecidableEq W]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (g : H → Z) (k : H → W) :
    conditionalInformation w S (fun h => (f h, g h)) k =
      conditionalInformation w S f k +
        conditionalInformation w S g (fun h => (f h, k h)) := by
  have he : conditionalInformation w S (fun h => (f h, g h)) k =
      conditionalInformation w S (fun h => (g h, f h)) k := by
    unfold conditionalInformation
    apply Finset.sum_congr rfl
    intro c hc
    exact joint_information_symmetric w (fiber S k c) f g
  rw [he]
  exact shannon_conditional_chain_rule w S g f k

theorem fiber_graph [DecidableEq Y] [DecidableEq Z]
    (S : Finset H) (f : H → Y) (φ : Y → Z) (y : Y) (z : Z) :
    fiber S (fun h => (f h, φ (f h))) (y, z) =
      if φ y = z then fiber S f y else ∅ := by
  ext h
  by_cases hz : φ y = z
  · simp only [fiber, Finset.mem_filter, Prod.mk.injEq, hz, if_true]
    constructor
    · intro he; exact ⟨he.1, he.2.1⟩
    · intro he; exact ⟨he.1, he.2, by rw [he.2, hz]⟩
  · simp only [fiber, Finset.mem_filter, Prod.mk.injEq, hz, if_false,
      Finset.not_mem_empty, iff_false, not_and]
    intro hh hf hφ
    exact hz (by rw [← hf]; exact hφ)

theorem graph_information_eq [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (φ : Y → Z) :
    information w S (fun h => (f h, φ (f h))) = information w S f := by
  rw [information_eq, information_eq, Fintype.sum_prod_type]
  congr 1
  apply Finset.sum_congr rfl
  intro y hy
  simp_rw [fiber_graph]
  have he : ∀ z : Z,
      Real.negMulLog (mass w (if φ y = z then fiber S f y else ∅)) =
      if φ y = z then Real.negMulLog (mass w (fiber S f y)) else 0 := by
    intro z
    split_ifs <;> simp [mass]
  simp_rw [he]
  simp

/-- If the second variable is determined by the first, joint entropy is the
first variable's entropy; this gives the functional form of the chain rule. -/
theorem determined_chain_rule [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (φ : Y → Z) :
    information w S f = information w S (fun h => φ (f h)) +
      conditionalInformation w S f (fun h => φ (f h)) := by
  rw [← graph_information_eq w S f φ]
  exact joint_information_chain_rule w S f (fun h => φ (f h))

theorem information_postprocess_le [Fintype Y] [DecidableEq Y]
    [Fintype Z] [DecidableEq Z] (w : H → ℝ) (S : Finset H)
    (f : H → Y) (φ : Y → Z) (hw : ∀ h ∈ S, 0 ≤ w h) :
    information w S (fun h => φ (f h)) ≤ information w S f := by
  have hc := conditionalInformation_nonneg w S f (fun h => φ (f h)) hw
  rw [determined_chain_rule w S f φ]
  linarith

end PlanarQuery.Entropy
