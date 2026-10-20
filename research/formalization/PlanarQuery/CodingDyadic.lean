import PlanarQuery.CodingTree
import Mathlib.Data.Real.Archimedean
import Mathlib.Algebra.Order.Floor.Semiring
import Mathlib.Analysis.SpecialFunctions.Log.Basic
import Mathlib.Analysis.SpecialFunctions.BinaryEntropy
import Mathlib.Algebra.BigOperators.Field

/-! Exact binary words, their dyadic cells, and the word containing a given
point. Half-open cells use explicit endpoints and have no binary-expansion
ambiguity at dyadic rationals. -/

namespace PlanarQuery.Coding

def value : List Bool → ℕ
  | [] => 0
  | b :: u => (if b then 2 ^ u.length else 0) + value u

def binaryWord : ℕ → ℕ → List Bool
  | 0, _ => []
  | n + 1, k =>
      if k < 2 ^ n then false :: binaryWord n k
      else true :: binaryWord n (k - 2 ^ n)

theorem binaryWord_length (n k : ℕ) : (binaryWord n k).length = n := by
  induction n generalizing k with
  | zero => rfl
  | succ n ih => simp only [binaryWord]; split_ifs <;> simp [ih]

theorem value_lt (u : List Bool) : value u < 2 ^ u.length := by
  induction u with
  | nil => simp [value]
  | cons b u ih => cases b <;> simp [value, pow_succ] <;> omega

theorem binaryWord_value (n k : ℕ) (hk : k < 2 ^ n) : value (binaryWord n k) = k := by
  induction n generalizing k with
  | zero =>
    have he : k = 0 := by simpa using hk
    simp [binaryWord, value, he]
  | succ n ih =>
    simp only [binaryWord]
    split_ifs with h
    · simp [value, ih k h]
    · have hl : k - 2 ^ n < 2 ^ n := by simp only [pow_succ] at hk; omega
      simp [value, binaryWord_length, ih _ hl]
      omega

theorem value_append (u v : List Bool) :
    value (u ++ v) = value u * 2 ^ v.length + value v := by
  induction u with
  | nil => simp [value]
  | cons b u ih =>
    cases b <;> simp [value, List.length_append, pow_add, ih] <;> ring

noncomputable def cellLeft (u : List Bool) : ℝ := (value u : ℝ) / 2 ^ u.length
noncomputable def cellRight (u : List Bool) : ℝ := ((value u : ℝ) + 1) / 2 ^ u.length

theorem cell_width (u : List Bool) : cellRight u - cellLeft u = ((2 : ℝ)⁻¹) ^ u.length := by
  unfold cellLeft cellRight
  rw [inv_pow]
  field_simp

theorem cell_nonempty (u : List Bool) : cellLeft u < cellRight u := by
  unfold cellLeft cellRight
  exact (div_lt_div_iff_of_pos_right (pow_pos (by norm_num : (0 : ℝ) < 2) _)).mpr
    (by linarith)

theorem prefix_cellLeft_le {u v : List Bool} (hp : u <+: v) : cellLeft u ≤ cellLeft v := by
  obtain ⟨t, rfl⟩ := hp
  unfold cellLeft
  apply (div_le_div_iff₀ (pow_pos (by norm_num : (0 : ℝ) < 2) _)
    (pow_pos (by norm_num : (0 : ℝ) < 2) _)).mpr
  simp only [List.length_append, pow_add, value_append, Nat.cast_add, Nat.cast_mul,
    Nat.cast_pow, Nat.cast_ofNat]
  nlinarith [show (0 : ℝ) ≤ (value t : ℝ) from Nat.cast_nonneg _,
    pow_pos (by norm_num : (0 : ℝ) < 2) u.length]

theorem prefix_cellRight_le {u v : List Bool} (hp : u <+: v) : cellRight v ≤ cellRight u := by
  obtain ⟨t, rfl⟩ := hp
  unfold cellRight
  apply (div_le_div_iff₀ (pow_pos (by norm_num : (0 : ℝ) < 2) _)
    (pow_pos (by norm_num : (0 : ℝ) < 2) _)).mpr
  have ht : (value t : ℝ) + 1 ≤ (2 : ℝ) ^ t.length := by
    exact_mod_cast Nat.succ_le_of_lt (value_lt t)
  simp only [List.length_append, pow_add, value_append, Nat.cast_add, Nat.cast_mul,
    Nat.cast_pow, Nat.cast_ofNat]
  nlinarith [pow_pos (by norm_num : (0 : ℝ) < 2) u.length]

theorem dyadic_cell_containing (m : ℝ) (n : ℕ) (hm0 : 0 ≤ m) (hm1 : m < 1) :
    ∃ u : List Bool, u.length = n ∧ cellLeft u ≤ m ∧ m < cellRight u := by
  let k := ⌊m * (2 : ℝ) ^ n⌋₊
  have hp : 0 < (2 : ℝ) ^ n := pow_pos (by norm_num) _
  have hx : 0 ≤ m * (2 : ℝ) ^ n := mul_nonneg hm0 (le_of_lt hp)
  have hk : k < 2 ^ n := by
    apply (Nat.floor_lt hx).mpr
    simp only [Nat.cast_pow, Nat.cast_ofNat]
    exact mul_lt_of_lt_one_left hp hm1
  refine ⟨binaryWord n k, binaryWord_length n k, ?_, ?_⟩
  · simp only [cellLeft, binaryWord_length, binaryWord_value n k hk]
    exact (div_le_iff₀ hp).mpr (Nat.floor_le hx)
  · simp only [cellRight, binaryWord_length, binaryWord_value n k hk]
    exact (lt_div_iff₀ hp).mpr (Nat.lt_floor_add_one _)

/-- The midpoint construction uses an actual integer depth rather than an
abstract real code length. -/
noncomputable def midpointDepth (a : ℝ) : ℕ := ⌈Real.log (2 / a) / Real.log 2⌉₊

theorem midpoint_width_le (a : ℝ) (ha : 0 < a) :
    ((2 : ℝ)⁻¹) ^ midpointDepth a ≤ a / 2 := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have hn := (div_le_iff₀ hlog2).mp (Nat.le_ceil (Real.log (2 / a) / Real.log 2))
  change Real.log (2 / a) ≤ (midpointDepth a : ℝ) * Real.log 2 at hn
  apply (Real.log_le_log_iff (pow_pos (by norm_num) _) (by positivity : 0 < a / 2)).mp
  rw [Real.log_pow, Real.log_inv, Real.log_div (ne_of_gt ha) (by norm_num)]
  rw [Real.log_div (by norm_num) (ne_of_gt ha)] at hn
  linarith

theorem midpoint_depth_bound (a : ℝ) (ha : 0 < a) (ha1 : a ≤ 1) :
    (midpointDepth a : ℝ) ≤ Real.log (1 / a) / Real.log 2 + 2 := by
  have hlog2 : 0 < Real.log 2 := Real.log_pos (by norm_num)
  have htwo : 1 ≤ 2 / a := (le_div_iff₀ ha).mpr (by linarith)
  have hx : 0 ≤ Real.log (2 / a) / Real.log 2 :=
    div_nonneg (Real.log_nonneg htwo) (le_of_lt hlog2)
  have hn := (Nat.ceil_lt_add_one hx).le
  change (midpointDepth a : ℝ) ≤ Real.log (2 / a) / Real.log 2 + 1 at hn
  have he : Real.log (2 / a) / Real.log 2 + 1 =
      Real.log (1 / a) / Real.log 2 + 2 := by
    rw [Real.log_div (by norm_num) (ne_of_gt ha), one_div, Real.log_inv]
    field_simp
    ring
  exact hn.trans_eq he

/-- The cell containing the midpoint stays in its probability interval; the
strict left inequality handles dyadic midpoints without binary ambiguity. -/
theorem midpoint_cell_inside (F a : ℝ) (u : List Bool)
    (hl : cellLeft u ≤ F + a / 2) (hr : F + a / 2 < cellRight u)
    (hw : cellRight u - cellLeft u ≤ a / 2) :
    F < cellLeft u ∧ cellRight u ≤ F + a := by
  constructor <;> linarith

theorem probability_interval_codeword (F a : ℝ) (hF : 0 ≤ F) (ha : 0 < a)
    (hFa : F + a ≤ 1) :
    ∃ u : List Bool, u.length = midpointDepth a ∧
      F < cellLeft u ∧ cellRight u ≤ F + a ∧
      (u.length : ℝ) ≤ Real.log (1 / a) / Real.log 2 + 2 := by
  obtain ⟨u, hu, hl, hr⟩ := dyadic_cell_containing (F + a / 2) (midpointDepth a)
    (by linarith) (by linarith)
  have hw : cellRight u - cellLeft u ≤ a / 2 := by
    rw [cell_width, hu]
    exact midpoint_width_le a ha
  have hi := midpoint_cell_inside F a u hl hr hw
  refine ⟨u, hu, hi.1, hi.2, ?_⟩
  rw [hu]
  exact midpoint_depth_bound a ha (by linarith)

/-- Ordered nonoverlapping dyadic cells cannot have comparable codewords.
Together with `probability_interval_codeword`, this proves the prefix-free
part of the manuscript's alphabetic midpoint construction. -/
theorem ordered_cells_prefix_free {I : Type*} (S : Finset I) (code : I → List Bool)
    (hordered : ∀ i ∈ S, ∀ j ∈ S, i ≠ j →
      cellRight (code i) ≤ cellLeft (code j) ∨
        cellRight (code j) ≤ cellLeft (code i)) : PrefixFree S code := by
  intro i hi j hj hne hp
  have hl := prefix_cellLeft_le hp
  have hr := prefix_cellRight_le hp
  have hni := cell_nonempty (code i)
  have hnj := cell_nonempty (code j)
  rcases hordered i hi j hj hne with ho | ho <;> linarith

noncomputable def cumulative (p : ℕ → ℝ) (i : ℕ) : ℝ := ∑ j ∈ Finset.range i, p j

theorem cumulative_add (p : ℕ → ℝ) (i : ℕ) :
    cumulative p i + p i = cumulative p (i + 1) := by
  exact (Finset.sum_range_succ p i).symm

theorem cumulative_mono (r : ℕ) (p : ℕ → ℝ) (hp : ∀ i < r, 0 ≤ p i)
    (i j : ℕ) (hij : i ≤ j) (hjr : j ≤ r) : cumulative p i ≤ cumulative p j := by
  apply Finset.sum_le_sum_of_subset_of_nonneg (Finset.range_mono hij)
  intro k hk _
  exact hp k (lt_of_lt_of_le (Finset.mem_range.mp hk) hjr)

/-- The finite cumulative-probability construction yields actual ordered
binary words with the advertised pointwise and average length bounds. -/
theorem midpoint_alphabetic_code (r : ℕ) (p : ℕ → ℝ)
    (hp : ∀ i < r, 0 < p i) (hs : ∑ i ∈ Finset.range r, p i = 1) :
    ∃ code : ℕ → List Bool,
      PrefixFree (Finset.range r) code ∧
      (∀ i < r, (code i).length = midpointDepth (p i) ∧
        cumulative p i < cellLeft (code i) ∧
        cellRight (code i) ≤ cumulative p i + p i ∧
        ((code i).length : ℝ) ≤ Real.log (1 / p i) / Real.log 2 + 2) ∧
      (∀ i j, i < j → j < r → cellRight (code i) ≤ cellLeft (code j)) ∧
      (∑ i ∈ Finset.range r, p i * ((code i).length : ℝ)) ≤
        (∑ i ∈ Finset.range r, Real.negMulLog (p i)) / Real.log 2 + 2 := by
  classical
  have hpn : ∀ i < r, 0 ≤ p i := fun i hi => le_of_lt (hp i hi)
  have hx : ∀ i < r, ∃ u : List Bool, u.length = midpointDepth (p i) ∧
      cumulative p i < cellLeft u ∧ cellRight u ≤ cumulative p i + p i ∧
      (u.length : ℝ) ≤ Real.log (1 / p i) / Real.log 2 + 2 := by
    intro i hi
    refine probability_interval_codeword _ _ ?_ (hp i hi) ?_
    · exact Finset.sum_nonneg (fun j hj => hpn j (lt_trans (Finset.mem_range.mp hj) hi))
    · rw [cumulative_add, ← hs]
      exact cumulative_mono r p hpn (i + 1) r (by omega) le_rfl
  let code : ℕ → List Bool := fun i => if hi : i < r then Classical.choose (hx i hi) else []
  have hc : ∀ i < r, (code i).length = midpointDepth (p i) ∧
      cumulative p i < cellLeft (code i) ∧ cellRight (code i) ≤ cumulative p i + p i ∧
      ((code i).length : ℝ) ≤ Real.log (1 / p i) / Real.log 2 + 2 := by
    intro i hi
    simpa only [code, dif_pos hi] using Classical.choose_spec (hx i hi)
  have ho : ∀ i j, i < j → j < r → cellRight (code i) ≤ cellLeft (code j) := by
    intro i j hij hj
    have hi : i < r := lt_trans hij hj
    have hcum : cumulative p i + p i ≤ cumulative p j := by
      rw [cumulative_add]
      exact cumulative_mono r p hpn _ _ (by omega) (le_of_lt hj)
    exact le_trans (hc i hi).2.2.1 (le_trans hcum (le_of_lt (hc j hj).2.1))
  refine ⟨code, ?_, hc, ho, ?_⟩
  · apply ordered_cells_prefix_free
    intro i hi j hj hne
    rcases lt_or_gt_of_ne hne with hij | hji
    · exact Or.inl (ho i j hij (Finset.mem_range.mp hj))
    · exact Or.inr (ho j i hji (Finset.mem_range.mp hi))
  · calc
      _ ≤ ∑ i ∈ Finset.range r, p i * (Real.log (1 / p i) / Real.log 2 + 2) := by
        apply Finset.sum_le_sum
        intro i hi
        exact mul_le_mul_of_nonneg_left (hc i (Finset.mem_range.mp hi)).2.2.2
          (hpn i (Finset.mem_range.mp hi))
      _ = (∑ i ∈ Finset.range r, Real.negMulLog (p i)) / Real.log 2 + 2 := by
        simp only [mul_add, ← mul_div_assoc, one_div, Real.log_inv, Real.negMulLog,
          mul_neg, neg_mul]
        rw [Finset.sum_add_distrib, ← Finset.sum_div, ← Finset.sum_mul, hs]
        ring

noncomputable def thresholdSystem {H : Type*} (x : H → ℝ) : QuerySystem H ℝ where
  answer q h := decide (q ≤ x h)

def mapThresholds {H : Type*} (φ : ℝ → ℝ) : Tree H ℝ → Tree H ℝ
  | .leaf h => .leaf h
  | .node q miss hit => .node (φ q) (mapThresholds φ miss) (mapThresholds φ hit)

theorem mapThresholds_eval {H : Type*} (M N : QuerySystem H ℝ) (φ : ℝ → ℝ)
    (T : Tree H ℝ) (h : H) (he : ∀ q, M.answer (φ q) h = N.answer q h) :
    Tree.eval M (mapThresholds φ T) h = Tree.eval N T h := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh => simp only [mapThresholds, Tree.eval, he, ihm, ihh]

theorem mapThresholds_depth {H : Type*} (M N : QuerySystem H ℝ) (φ : ℝ → ℝ)
    (T : Tree H ℝ) (h : H) (he : ∀ q, M.answer (φ q) h = N.answer q h) :
    Tree.depth M (mapThresholds φ T) h = Tree.depth N T h := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh => simp only [mapThresholds, Tree.depth, he, ihm, ihh]

theorem cellLeft_nonneg (u : List Bool) : 0 ≤ cellLeft u := by
  exact div_nonneg (Nat.cast_nonneg _) (le_of_lt (pow_pos (by norm_num) _))

theorem cellLeft_lt_one (u : List Bool) : cellLeft u < 1 := by
  apply (div_lt_one (pow_pos (by norm_num : (0 : ℝ) < 2) _)).mpr
  exact_mod_cast value_lt u

theorem cellLeft_false (u : List Bool) : cellLeft (false :: u) = cellLeft u / 2 := by
  simp only [cellLeft, value, Bool.false_eq_true, if_false, zero_add,
    List.length_cons, pow_succ]
  field_simp

theorem cellLeft_true (u : List Bool) : cellLeft (true :: u) = (cellLeft u + 1) / 2 := by
  simp only [cellLeft, value, if_true, List.length_cons, pow_succ, Nat.cast_add,
    Nat.cast_pow, Nat.cast_ofNat]
  field_simp
  ring

/-- A finite prefix code is implemented by actual dyadic threshold queries
on its ordered cell coordinates. Unary branches are allowed; terminating
early at a singleton only decreases the prescribed codeword length. -/
theorem prefix_code_threshold_tree {H : Type*} [DecidableEq H]
    (fallback : H) (S : Finset H) (code : H → List Bool)
    (hf : PrefixFree S code) (n : ℕ) (hn : ∀ h ∈ S, (code h).length ≤ n) :
    ∃ T : Tree H ℝ,
      Tree.Identifies (thresholdSystem (fun h => cellLeft (code h))) S T ∧
      ∀ h ∈ S, Tree.depth (thresholdSystem (fun h => cellLeft (code h))) T h ≤
        (code h).length := by
  classical
  induction n generalizing S code with
  | zero =>
    by_cases hne : S.Nonempty
    · obtain ⟨a, ha⟩ := hne
      have hc : ∀ h ∈ S, code h = [] := by
        intro h hh
        exact List.length_eq_zero_iff.mp (Nat.eq_zero_of_le_zero (hn h hh))
      refine ⟨.leaf a, ?_, ?_⟩
      · intro h hh
        change a = h
        by_contra hne
        exact hf a ha h hh hne (by simp [hc a ha, hc h hh])
      · intro h hh
        simp [Tree.depth]
    · refine ⟨.leaf fallback, ?_, ?_⟩
      · intro h hh; exact False.elim (hne ⟨h, hh⟩)
      · intro h hh; exact False.elim (hne ⟨h, hh⟩)
  | succ n ih =>
    by_cases hz : ∃ a ∈ S, code a = []
    · obtain ⟨a, ha, hac⟩ := hz
      refine ⟨.leaf a, ?_, ?_⟩
      · intro h hh
        change a = h
        by_contra hne
        exact hf a ha h hh hne (by simp [hac])
      · intro h hh; simp [Tree.depth]
    · have hnonempty : ∀ h ∈ S, code h ≠ [] := by
        intro h hh he
        exact hz ⟨h, hh, he⟩
      let A := S.filter (fun h => (code h).head? = some false)
      let B := S.filter (fun h => (code h).head? = some true)
      have hcA : ∀ h ∈ A, code h = false :: (code h).tail := by
        intro h hh
        have hh' := (Finset.mem_filter.mp hh).2
        cases he : code h with
        | nil => simp [he] at hh'
        | cons b u => cases b <;> simp_all
      have hcB : ∀ h ∈ B, code h = true :: (code h).tail := by
        intro h hh
        have hh' := (Finset.mem_filter.mp hh).2
        cases he : code h with
        | nil => simp [he] at hh'
        | cons b u => cases b <;> simp_all
      have htail : ∀ C : Finset H, ∀ b : Bool, C ⊆ S →
          (∀ h ∈ C, code h = b :: (code h).tail) →
          PrefixFree C (fun h => (code h).tail) ∧
            ∀ h ∈ C, ((code h).tail).length ≤ n := by
        intro C b hCS hc
        constructor
        · intro h hh k hk hne hp
          apply hf h (hCS hh) k (hCS hk) hne
          rw [hc h hh, hc k hk]
          exact List.cons_prefix_cons.mpr ⟨rfl, hp⟩
        · intro h hh
          have he := congrArg List.length (hc h hh)
          have hl := hn h (hCS hh)
          simp only [List.length_cons] at he
          omega
      have hA := htail A false (Finset.filter_subset _ _) hcA
      have hB := htail B true (Finset.filter_subset _ _) hcB
      obtain ⟨TA, hIA, hDA⟩ := ih A (fun h => (code h).tail) hA.1 hA.2
      obtain ⟨TB, hIB, hDB⟩ := ih B (fun h => (code h).tail) hB.1 hB.2
      let M := thresholdSystem (fun h => cellLeft (code h))
      let N := thresholdSystem (fun h => cellLeft ((code h).tail))
      have hcellA : ∀ h ∈ A, cellLeft (code h) = cellLeft ((code h).tail) / 2 := by
        intro h hh
        exact (congrArg cellLeft (hcA h hh)).trans (cellLeft_false _)
      have hcellB : ∀ h ∈ B, cellLeft (code h) = (cellLeft ((code h).tail) + 1) / 2 := by
        intro h hh
        exact (congrArg cellLeft (hcB h hh)).trans (cellLeft_true _)
      have heA : ∀ h ∈ A, ∀ q, M.answer (q / 2) h = N.answer q h := by
        intro h hh q
        simp only [M, N, thresholdSystem, hcellA h hh,
          decide_eq_decide]
        exact div_le_div_iff_of_pos_right (by norm_num : (0 : ℝ) < 2)
      have heB : ∀ h ∈ B, ∀ q, M.answer ((q + 1) / 2) h = N.answer q h := by
        intro h hh q
        simp only [M, N, thresholdSystem, hcellB h hh,
          decide_eq_decide]
        constructor <;> intro hq <;> linarith
      refine ⟨.node (1 / 2) (mapThresholds (fun q => q / 2) TA)
        (mapThresholds (fun q => (q + 1) / 2) TB), ?_, ?_⟩
      · intro h hh
        cases he : code h with
        | nil => exact False.elim (hnonempty h hh he)
        | cons b u =>
          cases b with
          | false =>
            have ha : h ∈ A := by simp [A, hh, he]
            have hr : M.answer (1 / 2) h = false := by
              have hu := cellLeft_lt_one u
              simp only [M, thresholdSystem, he, cellLeft_false, decide_eq_false_iff_not]
              linarith
            change Tree.eval M (.node _ _ _) h = h
            rw [Tree.eval, hr]
            simp only [Bool.false_eq_true, if_false]
            rw [mapThresholds_eval M N _ TA h (heA h ha)]
            exact hIA h ha
          | true =>
            have hb : h ∈ B := by simp [B, hh, he]
            have hr : M.answer (1 / 2) h = true := by
              have hu := cellLeft_nonneg u
              simp only [M, thresholdSystem, he, cellLeft_true, decide_eq_true_eq]
              linarith
            change Tree.eval M (.node _ _ _) h = h
            rw [Tree.eval, hr]
            simp only [if_true]
            rw [mapThresholds_eval M N _ TB h (heB h hb)]
            exact hIB h hb
      · intro h hh
        cases he : code h with
        | nil => exact False.elim (hnonempty h hh he)
        | cons b u =>
          cases b with
          | false =>
            have ha : h ∈ A := by simp [A, hh, he]
            have hr : M.answer (1 / 2) h = false := by
              have hu := cellLeft_lt_one u
              simp only [M, thresholdSystem, he, cellLeft_false, decide_eq_false_iff_not]
              linarith
            change Tree.depth M (.node _ _ _) h ≤ _
            rw [Tree.depth, hr]
            simp only [Bool.false_eq_true, if_false]
            rw [mapThresholds_depth M N _ TA h (heA h ha)]
            have hd := hDA h ha
            simpa [he, Nat.add_comm] using Nat.add_le_add_left hd 1
          | true =>
            have hb : h ∈ B := by simp [B, hh, he]
            have hr : M.answer (1 / 2) h = true := by
              have hu := cellLeft_nonneg u
              simp only [M, thresholdSystem, he, cellLeft_true, decide_eq_true_eq]
              linarith
            change Tree.depth M (.node _ _ _) h ≤ _
            rw [Tree.depth, hr]
            simp only [if_true]
            rw [mapThresholds_depth M N _ TB h (heB h hb)]
            have hd := hDB h hb
            simpa [he, Nat.add_comm] using Nat.add_le_add_left hd 1

def indexThresholdSystem : QuerySystem ℕ ℕ where
  answer q i := decide (q ≤ i)

noncomputable def thresholdIndex (r : ℕ) (x : ℕ → ℝ) (q : ℝ) : ℕ :=
  if he : ∃ i, i < r ∧ q ≤ x i then Nat.find he else r

theorem thresholdIndex_answer (r : ℕ) (x : ℕ → ℝ)
    (hm : ∀ i j, i < j → j < r → x i < x j) (h : ℕ) (hh : h < r) (q : ℝ) :
    indexThresholdSystem.answer (thresholdIndex r x q) h = (thresholdSystem x).answer q h := by
  simp only [indexThresholdSystem, thresholdSystem, decide_eq_decide]
  unfold thresholdIndex
  split_ifs with he
  · constructor
    · intro hn
      have hs := Nat.find_spec he
      by_cases heq : Nat.find he = h
      · simpa [heq] using hs.2
      · exact le_trans hs.2 (le_of_lt (hm _ h (lt_of_le_of_ne hn heq) hh))
    · intro hq
      exact Nat.find_min' he ⟨hh, hq⟩
  · constructor
    · intro hr; omega
    · intro hq; exact False.elim (he ⟨h, hh, hq⟩)

noncomputable def toIndexThresholds (r : ℕ) (x : ℕ → ℝ) : Tree ℕ ℝ → Tree ℕ ℕ
  | .leaf h => .leaf h
  | .node q miss hit => .node (thresholdIndex r x q)
      (toIndexThresholds r x miss) (toIndexThresholds r x hit)

theorem toIndexThresholds_eval (r : ℕ) (x : ℕ → ℝ)
    (hm : ∀ i j, i < j → j < r → x i < x j) (T : Tree ℕ ℝ) (h : ℕ) (hh : h < r) :
    Tree.eval indexThresholdSystem (toIndexThresholds r x T) h =
      Tree.eval (thresholdSystem x) T h := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh =>
    simp only [toIndexThresholds, Tree.eval, thresholdIndex_answer r x hm h hh, ihm, ihh]

theorem toIndexThresholds_depth (r : ℕ) (x : ℕ → ℝ)
    (hm : ∀ i j, i < j → j < r → x i < x j) (T : Tree ℕ ℝ) (h : ℕ) (hh : h < r) :
    Tree.depth indexThresholdSystem (toIndexThresholds r x T) h =
      Tree.depth (thresholdSystem x) T h := by
  induction T with
  | leaf label => rfl
  | node q miss hit ihm ihh =>
    simp only [toIndexThresholds, Tree.depth, thresholdIndex_answer r x hm h hh, ihm, ihh]

/-- The alphabetic midpoint code becomes a genuine tree of comparisons
`q ≤ i` on the ordered outcomes, with both the pointwise and expected-depth
bounds. No arbitrary code is asserted to be executable by supplied lines. -/
theorem alphabetic_threshold_tree (r : ℕ) (p : ℕ → ℝ)
    (hp : ∀ i < r, 0 < p i) (hs : ∑ i ∈ Finset.range r, p i = 1) :
    ∃ T : Tree ℕ ℕ, Tree.Identifies indexThresholdSystem (Finset.range r) T ∧
      (∀ i < r, (Tree.depth indexThresholdSystem T i : ℝ) ≤
        Real.log (1 / p i) / Real.log 2 + 2) ∧
      (∑ i ∈ Finset.range r, p i * (Tree.depth indexThresholdSystem T i : ℝ)) ≤
        (∑ i ∈ Finset.range r, Real.negMulLog (p i)) / Real.log 2 + 2 := by
  obtain ⟨code, hf, hc, ho, hE⟩ := midpoint_alphabetic_code r p hp hs
  have hne : (Finset.range r).Nonempty := by
    by_contra he
    rw [Finset.not_nonempty_iff_eq_empty.mp he] at hs
    simp at hs
  obtain ⟨a, ha, hmax⟩ := Finset.exists_max_image (Finset.range r)
    (fun i => (code i).length) hne
  obtain ⟨T, hId, hd⟩ := prefix_code_threshold_tree 0 (Finset.range r) code hf
    (code a).length hmax
  let x : ℕ → ℝ := fun i => cellLeft (code i)
  have hm : ∀ i j, i < j → j < r → x i < x j := by
    intro i j hij hj
    exact lt_of_lt_of_le (cell_nonempty (code i)) (ho i j hij hj)
  refine ⟨toIndexThresholds r x T, ?_, ?_, ?_⟩
  · intro i hi
    rw [toIndexThresholds_eval r x hm T i (Finset.mem_range.mp hi)]
    exact hId i hi
  · intro i hi
    rw [toIndexThresholds_depth r x hm T i hi]
    have hlen : (Tree.depth (thresholdSystem x) T i : ℝ) ≤ ((code i).length : ℝ) := by
      exact_mod_cast hd i (Finset.mem_range.mpr hi)
    exact hlen.trans (hc i hi).2.2.2
  · apply le_trans _ hE
    apply Finset.sum_le_sum
    intro i hi
    have hil := Finset.mem_range.mp hi
    rw [toIndexThresholds_depth r x hm T i hil]
    apply mul_le_mul_of_nonneg_left _ (le_of_lt (hp i hil))
    exact_mod_cast hd i hi

end PlanarQuery.Coding
