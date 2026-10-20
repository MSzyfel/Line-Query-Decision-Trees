import PlanarQuery.CodingDyadic
import PlanarQuery.TreePotentials
import Mathlib.Data.Finset.Lattice.Fold
import Mathlib.Order.Interval.Finset.Nat

/-! The interval recurrence for ordered threshold queries uses the original
rational weights. Its finite minimum is over actual interior split indices;
the optimum is compared with every identifying threshold tree. -/

namespace PlanarQuery.Coding

def interior (lo n : ℕ) : Finset ℕ := Finset.Ioo lo (lo + n)

theorem interior_nonempty (lo n : ℕ) (hn : 1 < n) : (interior lo n).Nonempty := by
  refine ⟨lo + 1, ?_⟩
  simp only [interior, Finset.mem_Ioo]
  omega

def intervalDP (w : ℕ → ℚ) (lo n : ℕ) : ℚ :=
  if hn : n ≤ 1 then 0 else
    Tree.mass w (Finset.Ico lo (lo + n)) +
      (interior lo n).attach.inf' ((interior_nonempty lo n (by omega)).attach)
        (fun k => intervalDP w lo (k.val - lo) + intervalDP w k.val (lo + n - k.val))
termination_by n
decreasing_by
  all_goals
    have hk := Finset.mem_Ioo.mp k.property
    omega

theorem intervalDP_base (w : ℕ → ℚ) (lo n : ℕ) (hn : n ≤ 1) : intervalDP w lo n = 0 := by
  rw [intervalDP, dif_pos hn]

theorem intervalDP_step (w : ℕ → ℚ) (lo n : ℕ) (hn : 1 < n) :
    intervalDP w lo n = Tree.mass w (Finset.Ico lo (lo + n)) +
      (interior lo n).attach.inf' ((interior_nonempty lo n hn).attach)
        (fun k => intervalDP w lo (k.val - lo) + intervalDP w k.val (lo + n - k.val)) := by
  rw [intervalDP, dif_neg (by omega)]

theorem threshold_branch_false (lo hi q : ℕ) :
    Tree.branch indexThresholdSystem (Finset.Ico lo hi) q false = Finset.Ico lo (min hi q) := by
  ext h
  simp only [Tree.branch, Finset.mem_filter, Finset.mem_Ico, indexThresholdSystem,
    decide_eq_false_iff_not]
  omega

theorem threshold_branch_true (lo hi q : ℕ) :
    Tree.branch indexThresholdSystem (Finset.Ico lo hi) q true = Finset.Ico (max lo q) hi := by
  ext h
  simp only [Tree.branch, Finset.mem_filter, Finset.mem_Ico, indexThresholdSystem,
    decide_eq_true_eq]
  omega

theorem intervalDP_lower_bound (w : ℕ → ℚ) (hw : ∀ i, 0 ≤ w i) (lo n : ℕ)
    (T : Tree ℕ ℕ) (hId : Tree.Identifies indexThresholdSystem (Finset.Ico lo (lo + n)) T) :
    intervalDP w lo n ≤ Tree.rawExpected indexThresholdSystem w (Finset.Ico lo (lo + n)) T := by
  induction n using Nat.strong_induction_on generalizing lo T with
  | h n ih =>
    by_cases hn : n ≤ 1
    · rw [intervalDP_base w lo n hn]
      exact Tree.rawExpected_nonneg _ w hw _ T
    · have hn' : 1 < n := by omega
      induction T with
      | leaf label =>
        have hc := Tree.identification_capacity indexThresholdSystem
          (Finset.Ico lo (lo + n)) (.leaf label) hId
        simp only [Tree.height, pow_zero, Nat.card_Ico, Nat.add_sub_cancel_left] at hc
        omega
      | node q miss hit ihm ihh =>
        have hc := Tree.identifies_children indexThresholdSystem
          (Finset.Ico lo (lo + n)) q miss hit hId
        rw [threshold_branch_false] at hc
        rw [threshold_branch_true] at hc
        by_cases hqlo : q ≤ lo
        · have hmiss : Finset.Ico lo (min (lo + n) q) = ∅ := by
            ext h; simp only [Finset.mem_Ico, Finset.not_mem_empty, iff_false]; omega
          have hhit : max lo q = lo := max_eq_left hqlo
          rw [hhit] at hc
          have hchild := ihh hc.2
          rw [Tree.rawExpected_node, threshold_branch_false, threshold_branch_true,
            hmiss, hhit]
          simp only [Tree.rawExpected, Finset.sum_empty, zero_add, add_zero]
          have hmass : 0 ≤ Tree.mass w (Finset.Ico lo (lo + n)) := Finset.sum_nonneg (fun i _ => hw i)
          exact le_trans hchild (le_add_of_nonneg_left hmass)
        · by_cases hqhi : lo + n ≤ q
          · have hhit : Finset.Ico (max lo q) (lo + n) = ∅ := by
              ext h; simp only [Finset.mem_Ico, Finset.not_mem_empty, iff_false]; omega
            have hmiss : min (lo + n) q = lo + n := min_eq_left hqhi
            rw [hmiss] at hc
            have hchild := ihm hc.1
            rw [Tree.rawExpected_node, threshold_branch_false, threshold_branch_true,
              hmiss, hhit]
            simp only [Tree.rawExpected, Finset.sum_empty, add_zero]
            have hmass : 0 ≤ Tree.mass w (Finset.Ico lo (lo + n)) :=
              Finset.sum_nonneg (fun i _ => hw i)
            exact le_trans hchild (le_add_of_nonneg_left hmass)
          · have hq : q ∈ interior lo n := by simp only [interior, Finset.mem_Ioo]; omega
            have hq1 : q - lo < n := by omega
            have hq2 : lo + n - q < n := by omega
            have hleft : lo + (q - lo) = q := by omega
            have hright : q + (lo + n - q) = lo + n := by omega
            rw [min_eq_right (by omega : q ≤ lo + n), max_eq_right (by omega : lo ≤ q)] at hc
            have hL := ih (q - lo) hq1 lo miss (by simpa only [hleft] using hc.1)
            have hR := ih (lo + n - q) hq2 q hit (by simpa only [hright] using hc.2)
            have hmin := Finset.inf'_le
              (fun k : {k // k ∈ interior lo n} =>
                intervalDP w lo (k.val - lo) + intervalDP w k.val (lo + n - k.val))
              (Finset.mem_attach (interior lo n) ⟨q, hq⟩)
            rw [intervalDP_step w lo n hn', Tree.rawExpected_node,
              threshold_branch_false, threshold_branch_true,
              min_eq_right (by omega : q ≤ lo + n), max_eq_right (by omega : lo ≤ q)]
            simp only [hleft] at hL
            simp only [hright] at hR
            simpa only [add_assoc] using add_le_add_left (le_trans hmin (add_le_add hL hR))
              (Tree.mass w (Finset.Ico lo (lo + n)))

theorem intervalDP_attained (w : ℕ → ℚ) (lo n : ℕ) :
    ∃ T : Tree ℕ ℕ, Tree.Identifies indexThresholdSystem (Finset.Ico lo (lo + n)) T ∧
      Tree.rawExpected indexThresholdSystem w (Finset.Ico lo (lo + n)) T = intervalDP w lo n := by
  induction n using Nat.strong_induction_on generalizing lo with
  | h n ih =>
    by_cases hn : n ≤ 1
    · refine ⟨.leaf lo, ?_, ?_⟩
      · intro h hh
        have hh' := Finset.mem_Ico.mp hh
        change lo = h
        omega
      · rw [Tree.rawExpected_leaf, intervalDP_base w lo n hn]
    · have hn' : 1 < n := by omega
      let f : {k // k ∈ interior lo n} → ℚ := fun k =>
        intervalDP w lo (k.val - lo) + intervalDP w k.val (lo + n - k.val)
      obtain ⟨k, hk, he⟩ := Finset.exists_mem_eq_inf'
        ((interior_nonempty lo n hn').attach) f
      have hkp := Finset.mem_Ioo.mp k.property
      have hleft : lo + (k.val - lo) = k.val := by omega
      have hright : k.val + (lo + n - k.val) = lo + n := by omega
      obtain ⟨L, hIL, hEL⟩ := ih (k.val - lo) (by omega) lo
      obtain ⟨R, hIR, hER⟩ := ih (lo + n - k.val) (by omega) k.val
      simp only [hleft] at hIL hEL
      simp only [hright] at hIR hER
      refine ⟨.node k.val L R, ?_, ?_⟩
      · intro h hh
        have hh' := Finset.mem_Ico.mp hh
        by_cases hkh : k.val ≤ h
        · simpa [Tree.eval, indexThresholdSystem, hkh] using hIR h
            (Finset.mem_Ico.mpr ⟨hkh, hh'.2⟩)
        · simpa [Tree.eval, indexThresholdSystem, hkh] using hIL h
            (Finset.mem_Ico.mpr ⟨hh'.1, by omega⟩)
      · rw [Tree.rawExpected_node, threshold_branch_false, threshold_branch_true,
          min_eq_right (le_of_lt hkp.2), max_eq_right (le_of_lt hkp.1), hEL, hER,
          intervalDP_step w lo n hn']
        rw [he]
        simp only [f, add_assoc]

theorem intervalDP_global_optimum (w : ℕ → ℚ) (hw : ∀ i, 0 ≤ w i) (lo n : ℕ) :
    ∃ T : Tree ℕ ℕ, Tree.Identifies indexThresholdSystem (Finset.Ico lo (lo + n)) T ∧
      Tree.rawExpected indexThresholdSystem w (Finset.Ico lo (lo + n)) T = intervalDP w lo n ∧
      ∀ U, Tree.Identifies indexThresholdSystem (Finset.Ico lo (lo + n)) U →
        Tree.rawExpected indexThresholdSystem w (Finset.Ico lo (lo + n)) T ≤
          Tree.rawExpected indexThresholdSystem w (Finset.Ico lo (lo + n)) U := by
  obtain ⟨T, hId, he⟩ := intervalDP_attained w lo n
  refine ⟨T, hId, he, ?_⟩
  intro U hU
  rw [he]
  exact intervalDP_lower_bound w hw lo n U hU

theorem intervalDP_entropy_bound (r : ℕ) (w : ℕ → ℚ) (hw : ∀ i, 0 ≤ w i)
    (hp : ∀ i < r, 0 < w i) (hs : ∑ i ∈ Finset.range r, w i = 1) :
    (intervalDP w 0 r : ℝ) ≤
      (∑ i ∈ Finset.range r, Real.negMulLog (w i : ℝ)) / Real.log 2 + 2 := by
  have hpr : ∀ i < r, 0 < (w i : ℝ) := fun i hi => by exact_mod_cast hp i hi
  have hsr : ∑ i ∈ Finset.range r, (w i : ℝ) = 1 := by
    have he := congrArg (fun q : ℚ => (q : ℝ)) hs
    simpa only [Rat.cast_sum, Rat.cast_one] using he
  obtain ⟨T, hId, _, hE⟩ := alphabetic_threshold_tree r (fun i => (w i : ℝ)) hpr hsr
  have hl := intervalDP_lower_bound w hw 0 r T
    (by simpa only [zero_add, Nat.Ico_zero_eq_range] using hId)
  simp only [zero_add, Nat.Ico_zero_eq_range] at hl
  have hlr : (intervalDP w 0 r : ℝ) ≤
      ∑ i ∈ Finset.range r, (w i : ℝ) * (Tree.depth indexThresholdSystem T i : ℝ) := by
    have he := (Rat.cast_le (K := ℝ)).mpr hl
    simpa only [Tree.rawExpected, Rat.cast_sum, Rat.cast_mul, Rat.cast_natCast] using he
  exact hlr.trans hE

def intervalStates (r : ℕ) : Finset (ℕ × ℕ) :=
  ((Finset.range (r + 1)).product (Finset.range (r + 1))).filter (fun p => p.1 ≤ p.2)

/-- Every recursive dependency is another tabulation state with a strictly
smaller interval length; hence increasing length is a valid evaluation order. -/
theorem interval_dependencies (r lo hi k : ℕ) (hp : (lo, hi) ∈ intervalStates r)
    (hk : k ∈ Finset.Ioo lo hi) :
    (lo, k) ∈ intervalStates r ∧ (k, hi) ∈ intervalStates r ∧
      k - lo < hi - lo ∧ hi - k < hi - lo := by
  simp only [intervalStates, Finset.mem_filter, Finset.product_eq_sprod,
    Finset.mem_product, Finset.mem_range] at hp ⊢
  simp only [Finset.mem_Ioo] at hk
  omega

theorem interval_state_count (r : ℕ) : (intervalStates r).card ≤ (r + 1) ^ 2 := by
  calc
    _ ≤ ((Finset.range (r + 1)).product (Finset.range (r + 1))).card := Finset.card_filter_le _ _
    _ = (r + 1) ^ 2 := by simp [Finset.card_product, pow_two]

theorem interval_transition_count (r : ℕ) :
    (∑ p ∈ intervalStates r, (Finset.Ioo p.1 p.2).card) ≤ r * (r + 1) ^ 2 := by
  calc
    _ ≤ ∑ _p ∈ intervalStates r, r := by
      apply Finset.sum_le_sum
      intro p hp
      have hb := Finset.mem_product.mp (Finset.mem_filter.mp hp).1
      have hr := Finset.mem_range.mp hb.2
      rw [Nat.card_Ioo]
      omega
    _ = r * (intervalStates r).card := by simp [Nat.mul_comm]
    _ ≤ r * (r + 1) ^ 2 := Nat.mul_le_mul_left r (interval_state_count r)

end PlanarQuery.Coding
