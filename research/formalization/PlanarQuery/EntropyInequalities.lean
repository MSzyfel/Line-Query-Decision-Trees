import PlanarQuery.EntropyPartitions
import PlanarQuery.CodingTree
import Mathlib.Analysis.Convex.Jensen

/-! Finite log-sum and entropy bounds. The proof of log-sum uses the proved
convexity of `x * log x` and finite Jensen; zero numerator terms need no
separate limiting argument because `0 * log 0 = 0`. -/

namespace PlanarQuery.Entropy

variable {I : Type*}

theorem log_sum (s : Finset I) (a b : I → ℝ)
    (ha : ∀ i ∈ s, 0 ≤ a i) (hb : ∀ i ∈ s, 0 < b i)
    (_hA : 0 < ∑ i ∈ s, a i) (hB : 0 < ∑ i ∈ s, b i) :
    (∑ i ∈ s, a i) * Real.log ((∑ i ∈ s, a i) / (∑ i ∈ s, b i)) ≤
      ∑ i ∈ s, a i * Real.log (a i / b i) := by
  let A := ∑ i ∈ s, a i
  let B := ∑ i ∈ s, b i
  have hBn : B ≠ 0 := ne_of_gt hB
  have hw : ∀ i ∈ s, 0 ≤ b i / B :=
    fun i hi => div_nonneg (le_of_lt (hb i hi)) (le_of_lt hB)
  have hs : ∑ i ∈ s, b i / B = 1 := by
    rw [← Finset.sum_div]
    exact div_self hBn
  have hm : ∀ i ∈ s, a i / b i ∈ Set.Ici (0 : ℝ) :=
    fun i hi => div_nonneg (ha i hi) (le_of_lt (hb i hi))
  have hj := Real.convexOn_mul_log.map_sum_le hw hs hm
  simp only [smul_eq_mul] at hj
  have hmean : (∑ i ∈ s, b i / B * (a i / b i)) = A / B := by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i hi
    field_simp [ne_of_gt (hb i hi)]
    ring
  have hrhs : (∑ i ∈ s, b i / B * ((a i / b i) * Real.log (a i / b i))) =
      (∑ i ∈ s, a i * Real.log (a i / b i)) / B := by
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro i hi
    field_simp [ne_of_gt (hb i hi)]
    ring
  rw [hmean, hrhs] at hj
  have hj' := mul_le_mul_of_nonneg_left hj (le_of_lt hB)
  have hl : B * (A / B * Real.log (A / B)) = A * Real.log (A / B) := by
    field_simp
  have hr : B * ((∑ i ∈ s, a i * Real.log (a i / b i)) / B) =
      ∑ i ∈ s, a i * Real.log (a i / b i) := by field_simp
  rw [hl, hr] at hj'
  exact hj'

theorem normalized_entropy_le_log_card (s : Finset I) (p : I → ℝ)
    (hp : ∀ i ∈ s, 0 ≤ p i) (hs : ∑ i ∈ s, p i = 1) :
    (∑ i ∈ s, Real.negMulLog (p i)) ≤ Real.log (s.card : ℝ) := by
  have hne : s.Nonempty := by
    by_contra he
    have hz := Finset.not_nonempty_iff_eq_empty.mp he
    simp [hz] at hs
  have hc : 0 < (s.card : ℝ) := Nat.cast_pos.mpr (Finset.card_pos.mpr hne)
  have hb : 0 < ∑ _i ∈ s, (1 : ℝ) := by simpa using hc
  have hj := log_sum s p (fun _ => 1) hp (fun _ _ => zero_lt_one) (by rw [hs]; norm_num) hb
  simp only [hs, div_one, one_mul, Finset.sum_const, nsmul_eq_mul, mul_one, one_div,
    Real.log_inv] at hj
  simp only [Real.negMulLog, neg_mul, Finset.sum_neg_distrib]
  linarith

theorem normalized_entropy_nonneg (s : Finset I) (p : I → ℝ)
    (hp : ∀ i ∈ s, 0 ≤ p i) (hs : ∑ i ∈ s, p i = 1) :
    0 ≤ ∑ i ∈ s, Real.negMulLog (p i) := by
  apply Finset.sum_nonneg
  intro i hi
  have hu : p i ≤ 1 := by
    rw [← hs]
    exact Finset.single_le_sum hp hi
  exact Real.negMulLog_nonneg (hp i hi) hu

noncomputable def support (s : Finset I) (p : I → ℝ) : Finset I := by
  classical
  exact s.filter (fun i => p i ≠ 0)

theorem sum_support (s : Finset I) (p : I → ℝ) :
    (∑ i ∈ support s p, p i) = ∑ i ∈ s, p i := by
  classical
  rw [support, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro i hi
  by_cases hz : p i = 0 <;> simp [hz]

theorem entropy_sum_support (s : Finset I) (p : I → ℝ) :
    (∑ i ∈ support s p, Real.negMulLog (p i)) = ∑ i ∈ s, Real.negMulLog (p i) := by
  classical
  rw [support, Finset.sum_filter]
  apply Finset.sum_congr rfl
  intro i hi
  by_cases hz : p i = 0 <;> simp [hz]

theorem normalized_entropy_bounds (s : Finset I) (p : I → ℝ)
    (hp : ∀ i ∈ s, 0 ≤ p i) (hs : ∑ i ∈ s, p i = 1) :
    0 ≤ (∑ i ∈ s, Real.negMulLog (p i)) ∧
      (∑ i ∈ s, Real.negMulLog (p i)) ≤ Real.log ((support s p).card : ℝ) := by
  constructor
  · exact normalized_entropy_nonneg s p hp hs
  · rw [← entropy_sum_support s p]
    apply normalized_entropy_le_log_card
    · intro i hi
      exact hp i (Finset.mem_filter.mp hi).1
    · rw [sum_support, hs]

theorem binary_entropy_bounds (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1) :
    0 ≤ Real.binEntropy t ∧ Real.binEntropy t ≤ Real.log 2 :=
  ⟨Real.binEntropy_nonneg ht0 ht1, Real.binEntropy_le_log_two⟩

theorem information_normalized_bounds {H Y : Type*} [Fintype Y] [DecidableEq Y]
    (w : H → ℝ) (S : Finset H) (f : H → Y) (hw : ∀ h ∈ S, 0 ≤ w h)
    (hm : mass w S = 1) :
    0 ≤ information w S f ∧ information w S f ≤
      Real.log ((support Finset.univ (fun y => mass w (fiber S f y))).card : ℝ) := by
  rw [information_normalized w S f hm]
  apply normalized_entropy_bounds
  · intro y hy
    apply mass_nonneg
    intro h hh
    exact hw h (Finset.mem_filter.mp hh).1
  · rw [show (∑ y, mass w (fiber S f y)) = mass w S from sum_fiber S f w, hm]

theorem weighted_le_mass_log_card {H : Type*} (w : H → ℝ) (S : Finset H)
    (hw : ∀ h ∈ S, 0 ≤ w h) :
    weighted w S ≤ mass w S * Real.log (S.card : ℝ) := by
  by_cases hz : mass w S = 0
  · have hzero : ∀ h ∈ S, w h = 0 := by
      intro h hh
      have hl := weight_le_mass w S hw h hh
      rw [hz] at hl
      exact le_antisymm hl (hw h hh)
    simp [weighted, hz, Finset.sum_congr rfl
      (fun h hh => congrArg Real.negMulLog (hzero h hh))]
  · have hm : 0 < mass w S := lt_of_le_of_ne (mass_nonneg w S hw) (Ne.symm hz)
    have hn : ∑ h ∈ S, w h / mass w S = 1 := by
      rw [← Finset.sum_div]
      exact div_self hz
    rw [weighted_eq_normalized w S hz]
    exact mul_le_mul_of_nonneg_left (normalized_entropy_le_log_card S _
      (fun h hh => div_nonneg (hw h hh) (le_of_lt hm)) hn) (le_of_lt hm)

/-- Kraft and log-sum imply the coding lower bound, including zero-probability
symbols. This is the direct code-length route used in the manuscript, in
addition to the independent executable-tree induction in `Entropy.lean`. -/
theorem normalized_entropy_le_code_length (s : Finset I) (p : I → ℝ)
    (lengths : I → ℕ) (hp : ∀ i ∈ s, 0 ≤ p i) (hs : ∑ i ∈ s, p i = 1)
    (hk : ∑ i ∈ s, ((2 : ℝ)⁻¹) ^ lengths i ≤ 1) :
    (∑ i ∈ s, Real.negMulLog (p i)) ≤
      (∑ i ∈ s, p i * (lengths i : ℝ)) * Real.log 2 := by
  have hne : s.Nonempty := by
    by_contra hn
    rw [Finset.not_nonempty_iff_eq_empty.mp hn] at hs
    simp at hs
  have hb : ∀ i ∈ s, 0 < ((2 : ℝ)⁻¹) ^ lengths i :=
    fun i _ => pow_pos (by norm_num) _
  have hB : 0 < ∑ i ∈ s, ((2 : ℝ)⁻¹) ^ lengths i := Finset.sum_pos hb hne
  have hlog := log_sum s p (fun i => ((2 : ℝ)⁻¹) ^ lengths i) hp hb
    (by rw [hs]; norm_num) hB
  rw [hs, one_mul, one_div, Real.log_inv] at hlog
  have hnonpos := Real.log_nonpos (le_of_lt hB) hk
  have he : (∑ i ∈ s, p i * Real.log (p i / ((2 : ℝ)⁻¹) ^ lengths i)) =
      -(∑ i ∈ s, Real.negMulLog (p i)) +
        (∑ i ∈ s, p i * (lengths i : ℝ)) * Real.log 2 := by
    have hterm : ∀ i ∈ s,
        p i * Real.log (p i / ((2 : ℝ)⁻¹) ^ lengths i) =
          -Real.negMulLog (p i) + (p i * (lengths i : ℝ)) * Real.log 2 := by
      intro i hi
      by_cases hz : p i = 0
      · simp [hz]
      · rw [Real.log_div hz (ne_of_gt (hb i hi)), Real.log_pow, Real.log_inv]
        unfold Real.negMulLog
        ring
    rw [Finset.sum_congr rfl hterm, Finset.sum_add_distrib,
      Finset.sum_neg_distrib, ← Finset.sum_mul]
  rw [he] at hlog
  linarith

theorem prefix_code_entropy_lower_bound (s : Finset I) (p : I → ℝ)
    (code : I → List Bool) (hp : ∀ i ∈ s, 0 ≤ p i) (hs : ∑ i ∈ s, p i = 1)
    (hf : Coding.PrefixFree s code) :
    (∑ i ∈ s, Real.negMulLog (p i)) / Real.log 2 ≤
      ∑ i ∈ s, p i * ((code i).length : ℝ) := by
  have hk := (Rat.cast_le (K := ℝ)).mpr (Coding.kraft s code hf)
  have hkr : ∑ i ∈ s, ((2 : ℝ)⁻¹) ^ (code i).length ≤ 1 := by
    simpa only [Rat.cast_sum, Rat.cast_pow, Rat.cast_inv, Rat.cast_ofNat,
      Rat.cast_one] using hk
  exact (div_le_iff₀ (Real.log_pos (by norm_num : (1 : ℝ) < 2))).mpr
    (normalized_entropy_le_code_length s p (fun i => (code i).length) hp hs hkr)

theorem identifying_tree_entropy_lower_bound_via_kraft {H Q : Type*}
    [DecidableEq H] (M : QuerySystem H Q) (p : H → ℝ) (S : Finset H)
    (T : Tree H Q) (hp : ∀ h ∈ S, 0 ≤ p h) (hs : mass p S = 1)
    (hId : Tree.Identifies M S T) :
    weighted p S / Real.log 2 ≤ expected M p S T := by
  have he := prefix_code_entropy_lower_bound S p (Coding.transcript M T) hp hs
    (Coding.identifying_transcripts_prefix_free M S T hId)
  simpa only [weighted, hs, Real.negMulLog_one, sub_zero, expected,
    Coding.transcript_length] using he

end PlanarQuery.Entropy
