import PlanarQuery.LookaheadCompletion
import PlanarQuery.FiniteSearch
import Mathlib.Data.Finset.Sort

/-! Finite exact lookahead using the actual costs of constructed trees.
The selector is an executable list scan, not an assumed minimization oracle.
All root queries are supplied queries. Stopping, legal leaves, and every
supplied root query are compared at each horizon. -/

namespace PlanarQuery.Tree

variable {H Q : Type*}

def selectBest (score : Tree H Q → ℚ) (seed : Tree H Q) :
    List (Tree H Q) → Tree H Q
  | [] => seed
  | T :: rest => selectBest score (if score T ≤ score seed then T else seed) rest

theorem selectBest_le_seed (score : Tree H Q → ℚ) (seed : Tree H Q)
    (candidates : List (Tree H Q)) :
    score (selectBest score seed candidates) ≤ score seed := by
  induction candidates generalizing seed with
  | nil => exact le_refl _
  | cons T rest ih =>
    simp only [selectBest]
    by_cases hT : score T ≤ score seed
    · rw [if_pos hT]; exact (ih T).trans hT
    · rw [if_neg hT]; exact ih seed

theorem selectBest_le_member (score : Tree H Q → ℚ) (seed : Tree H Q)
    (candidates : List (Tree H Q)) (T : Tree H Q) (hT : T ∈ candidates) :
    score (selectBest score seed candidates) ≤ score T := by
  induction candidates generalizing seed with
  | nil => simp at hT
  | cons U rest ih =>
    simp only [selectBest]
    rcases List.mem_cons.mp hT with rfl | hT
    · by_cases hU : score T ≤ score seed
      · rw [if_pos hU]; exact selectBest_le_seed score T rest
      · rw [if_neg hU]
        exact (selectBest_le_seed score seed rest).trans (le_of_not_ge hU)
    · exact ih _ hT

theorem selectBest_preserves (score : Tree H Q → ℚ) (seed : Tree H Q)
    (candidates : List (Tree H Q)) (P : Tree H Q → Prop)
    (hseed : P seed) (hcandidates : ∀ T ∈ candidates, P T) :
    P (selectBest score seed candidates) := by
  induction candidates generalizing seed with
  | nil => exact hseed
  | cons T rest ih =>
    simp only [selectBest]
    apply ih
    · split_ifs
      · exact hcandidates T List.mem_cons_self
      · exact hseed
    · intro U hU
      exact hcandidates U (List.mem_cons_of_mem _ hU)

variable [Fintype H] [Fintype Q] [LinearOrder H] [LinearOrder Q]

instance (M : QuerySystem H Q) (S : Finset H) (T : Tree H Q) :
    Decidable (Identifies M S T) :=
  inferInstanceAs (Decidable (∀ h ∈ S, eval M T h = h))

def legalLeaves (M : QuerySystem H Q) (S : Finset H) : List (Tree H Q) :=
  ((Finset.univ.sort (· ≤ ·) : List H).map Tree.leaf).filter
    (fun T => decide (Identifies M S T))

omit [Fintype Q] [LinearOrder Q] in
theorem mem_legalLeaves (M : QuerySystem H Q) (S : Finset H) (h : H)
    (hId : Identifies M S (.leaf h)) : .leaf h ∈ legalLeaves M S := by
  simp only [legalLeaves, List.mem_filter, decide_eq_true_eq]
  exact ⟨List.mem_map.mpr ⟨h, by simp, rfl⟩, hId⟩

def rolloutCandidates (M : QuerySystem H Q) (S : Finset H)
    (continuation : Finset H → Tree H Q) : List (Tree H Q) :=
  legalLeaves M S ++ (Finset.univ.sort (· ≤ ·) : List Q).map (fun q =>
    .node q (continuation (branch M S q false)) (continuation (branch M S q true)))

def rollout (M : QuerySystem H Q) (score : Finset H → Tree H Q → ℚ)
    (B : Finset H → Tree H Q) : ℕ → Finset H → Tree H Q
  | 0, S => B S
  | k + 1, S => selectBest (score S) (B S)
      (rolloutCandidates M S (rollout M score B k))

theorem rollout_identifies (M : QuerySystem H Q)
    (score : Finset H → Tree H Q → ℚ) (B : Finset H → Tree H Q)
    (hB : ∀ S, Identifies M S (B S)) (k : ℕ) (S : Finset H) :
    Identifies M S (rollout M score B k S) := by
  induction k generalizing S with
  | zero => exact hB S
  | succ k ih =>
    apply selectBest_preserves (score S) (B S) _ (Identifies M S) (hB S)
    intro T hT
    rcases List.mem_append.mp hT with hleaf | hnode
    · exact of_decide_eq_true (List.mem_filter.mp hleaf).2
    · obtain ⟨q, _, rfl⟩ := List.mem_map.mp hnode
      intro h hh
      cases he : M.answer q h
      · simpa only [eval, he] using ih (branch M S q false) h (by simp [hh, he])
      · simpa only [eval, he] using ih (branch M S q true) h (by simp [hh, he])

theorem rollout_le_baseline (M : QuerySystem H Q)
    (score : Finset H → Tree H Q → ℚ) (B : Finset H → Tree H Q)
    (k : ℕ) (S : Finset H) : score S (rollout M score B k S) ≤ score S (B S) := by
  cases k
  · exact le_refl _
  · exact selectBest_le_seed _ _ _

/-- Dynamic lookahead costs no more than copying any identifying
competitor's first k levels and completing its actual frontier. -/
theorem rollout_expected_le_completion (M : QuerySystem H Q) (w : H → ℚ)
    (B : Finset H → Tree H Q) (k : ℕ) (S : Finset H) (T : Tree H Q)
    (hT : Identifies M S T) :
    rawExpected M w S (rollout M (rawExpected M w) B k S) ≤
      rawExpected M w S (completePrefix M B T S k) := by
  induction k generalizing S T with
  | zero => simp [rollout, completePrefix]
  | succ k ih =>
    cases T with
    | leaf h =>
      simp only [rollout, completePrefix]
      exact selectBest_le_member (rawExpected M w S) (B S) _ (.leaf h)
        (List.mem_append_left _ (mem_legalLeaves M S h hT))
    | node q miss hit =>
      have hchildren := identifies_children M S q miss hit hT
      have hm := ih (branch M S q false) miss hchildren.1
      have hh := ih (branch M S q true) hit hchildren.2
      have hcandidate : (.node q
          (rollout M (rawExpected M w) B k (branch M S q false))
          (rollout M (rawExpected M w) B k (branch M S q true))) ∈
          rolloutCandidates M S (rollout M (rawExpected M w) B k) :=
        List.mem_append_right _ (List.mem_map.mpr ⟨q, by simp, rfl⟩)
      simp only [rollout]
      apply (selectBest_le_member (rawExpected M w S) (B S) _ _ hcandidate).trans
      simp only [completePrefix, rawExpected_node]
      exact add_le_add (add_le_add_left hm _) hh

theorem rollout_height_le_completion (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (k : ℕ) (S : Finset H) (T : Tree H Q)
    (hT : Identifies M S T) :
    (height (rollout M (fun _ U => (height U : ℚ)) B k S) : ℚ) ≤
      height (completePrefix M B T S k) := by
  induction k generalizing S T with
  | zero => simp [rollout, completePrefix]
  | succ k ih =>
    cases T with
    | leaf h =>
      simp only [rollout, completePrefix]
      exact selectBest_le_member (fun U => (height U : ℚ)) (B S) _ (.leaf h)
        (List.mem_append_left _ (mem_legalLeaves M S h hT))
    | node q miss hit =>
      have hchildren := identifies_children M S q miss hit hT
      have hm := ih (branch M S q false) miss hchildren.1
      have hh := ih (branch M S q true) hit hchildren.2
      have hcandidate : (.node q
          (rollout M (fun _ U => (height U : ℚ)) B k (branch M S q false))
          (rollout M (fun _ U => (height U : ℚ)) B k (branch M S q true))) ∈
          rolloutCandidates M S (rollout M (fun _ U => (height U : ℚ)) B k) :=
        List.mem_append_right _ (List.mem_map.mpr ⟨q, by simp, rfl⟩)
      simp only [rollout]
      apply (selectBest_le_member (fun U => (height U : ℚ)) (B S) _ _ hcandidate).trans
      simp only [completePrefix, height, Nat.cast_add, Nat.cast_one, Nat.cast_max]
      exact add_le_add_left (max_le_max hm hh) _

theorem rollout_expected_approximation (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (B : Finset H → Tree H Q)
    (hlegal : ∀ S, Identifies M S (B S)) (a L : ℚ) (ha : 1 < a)
    (k : ℕ) (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T →
      rawExpected M w U (B U) ≤ a * rawExpected M w U T + L * mass w U)
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    Identifies M S (rollout M (rawExpected M w) B k S) ∧
      rawExpected M w S (rollout M (rawExpected M w) B k S) ≤ a * rawExpected M w S T :=
  ⟨rollout_identifies M _ B hlegal k S,
    (rollout_expected_le_completion M w B k S T hT).trans
      (completePrefix_expected_approximation M w hw B a L ha k hk hB T S hT)⟩

theorem rollout_height_approximation (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (hlegal : ∀ S, Identifies M S (B S))
    (a L : ℚ) (ha : 1 < a) (k : ℕ) (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T → (height (B U) : ℚ) ≤ a * height T + L)
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    Identifies M S (rollout M (fun _ U => (height U : ℚ)) B k S) ∧
      (height (rollout M (fun _ U => (height U : ℚ)) B k S) : ℚ) ≤ a * height T :=
  ⟨rollout_identifies M _ B hlegal k S,
    (rollout_height_le_completion M B k S T hT).trans
      (completePrefix_height_approximation M B a L ha k hk hB T S hT)⟩

omit [Fintype H] [Fintype Q] [LinearOrder Q] in
/-- Real continuation coefficients need not be rounded to rationals.
Only the constructed trees' exact comparison costs are rational. -/
theorem completePrefix_expected_real_invoice (M : QuerySystem H Q) (w : H → ℚ)
    (B : Finset H → Tree H Q) (a L : ℝ)
    (hB : ∀ U T, Identifies M U T →
      (rawExpected M w U (B U) : ℝ) ≤ a * (rawExpected M w U T : ℝ) + L * (mass w U : ℝ))
    (T : Tree H Q) (S : Finset H) (k : ℕ) (hT : Identifies M S T) :
    (rawExpected M w S (completePrefix M B T S k) : ℝ) ≤
      (prefixInvoice M w T S k : ℝ) + a * (tailInvoice M w T S k : ℝ) +
        L * (frontierInvoice M w T S k : ℝ) := by
  induction k generalizing T S with
  | zero => simpa [completePrefix, prefixInvoice, tailInvoice, frontierInvoice] using hB S T hT
  | succ k ih =>
    cases T with
    | leaf h => simp [completePrefix, rawExpected_leaf, prefixInvoice, tailInvoice, frontierInvoice]
    | node q miss hit =>
      obtain ⟨hm, hh⟩ := identifies_children M S q miss hit hT
      have him := ih miss (branch M S q false) hm
      have hih := ih hit (branch M S q true) hh
      simp only [completePrefix, rawExpected_node, prefixInvoice, tailInvoice,
        frontierInvoice, Rat.cast_add]
      linarith

theorem rollout_expected_real_approximation (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (B : Finset H → Tree H Q)
    (hlegal : ∀ S, Identifies M S (B S)) (a L : ℝ) (ha : 1 < a)
    (k : ℕ) (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T →
      (rawExpected M w U (B U) : ℝ) ≤ a * (rawExpected M w U T : ℝ) + L * (mass w U : ℝ))
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    Identifies M S (rollout M (rawExpected M w) B k S) ∧
      (rawExpected M w S (rollout M (rawExpected M w) B k S) : ℝ) ≤
        a * (rawExpected M w S T : ℝ) := by
  have hc := completePrefix_expected_real_invoice M w B a L hB T S k hT
  have hf : 0 ≤ (frontierInvoice M w T S k : ℝ) := by
    exact_mod_cast frontierInvoice_nonneg M w hw T S k
  have hp : (k : ℝ) * (frontierInvoice M w T S k : ℝ) ≤ (prefixInvoice M w T S k : ℝ) := by
    exact_mod_cast prefixInvoice_pays_frontier M w hw T S k
  have he : (prefixInvoice M w T S k : ℝ) + (tailInvoice M w T S k : ℝ) =
      (rawExpected M w S T : ℝ) := by exact_mod_cast invoices_decompose M w T S k
  have hl := mul_le_mul_of_nonneg_right hk hf
  have hp' := mul_le_mul_of_nonneg_left hp (sub_nonneg.mpr ha.le)
  refine ⟨rollout_identifies M _ B hlegal k S, ?_⟩
  have hr : (rawExpected M w S (rollout M (rawExpected M w) B k S) : ℝ) ≤
      (rawExpected M w S (completePrefix M B T S k) : ℝ) := by
    exact_mod_cast rollout_expected_le_completion M w B k S T hT
  nlinarith

omit [Fintype H] [Fintype Q] [LinearOrder Q] in
theorem completePrefix_height_real_envelope (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (a L : ℝ) (ha : 0 ≤ a)
    (hB : ∀ U T, Identifies M U T → (height (B U) : ℝ) ≤ a * height T + L)
    (T : Tree H Q) (S : Finset H) (D k : ℕ)
    (hT : Identifies M S T) (hD : height T ≤ D) (hk : k ≤ D) :
    (height (completePrefix M B T S k) : ℝ) ≤
      max (D : ℝ) ((k : ℝ) + a * (D - k : ℕ) + L) := by
  induction k generalizing T S D with
  | zero =>
    have hb := hB S T hT
    have hd : (height T : ℝ) ≤ D := by exact_mod_cast hD
    have he := mul_le_mul_of_nonneg_left hd ha
    simp only [completePrefix, Nat.cast_zero, Nat.sub_zero, zero_add]
    exact (hb.trans (by linarith)).trans (le_max_right _ _)
  | succ k ih =>
    cases T with
    | leaf h =>
      simp only [completePrefix, height, Nat.cast_zero]
      exact (Nat.cast_nonneg D).trans (le_max_left _ _)
    | node q miss hit =>
      have hmD : height miss ≤ D - 1 := by simp only [height] at hD; omega
      have hhD : height hit ≤ D - 1 := by simp only [height] at hD; omega
      have hkd : k ≤ D - 1 := by omega
      obtain ⟨hm, hh⟩ := identifies_children M S q miss hit hT
      have him := ih miss (branch M S q false) (D - 1) hm hmD hkd
      have hih := ih hit (branch M S q true) (D - 1) hh hhD hkd
      have heq : D - 1 - k = D - (k + 1) := by omega
      rw [heq] at him hih
      have hcast : ((D - 1 : ℕ) : ℝ) + 1 = D := by
        exact_mod_cast (show D - 1 + 1 = D by omega)
      have hadd := add_le_add_left (max_le him hih) 1
      simp only [completePrefix, height, Nat.cast_add, Nat.cast_one, Nat.cast_max]
      have hmax : 1 + max ((D - 1 : ℕ) : ℝ)
          ((k : ℝ) + a * (D - (k + 1) : ℕ) + L) =
          max (D : ℝ) ((k : ℝ) + 1 + a * (D - (k + 1) : ℕ) + L) := by
        rw [add_max]
        congr 1 <;> linarith
      rw [hmax] at hadd
      exact hadd

theorem rollout_height_real_approximation (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (hlegal : ∀ S, Identifies M S (B S))
    (a L : ℝ) (ha : 1 < a) (k : ℕ) (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T → (height (B U) : ℝ) ≤ a * height T + L)
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    Identifies M S (rollout M (fun _ U => (height U : ℚ)) B k S) ∧
      (height (rollout M (fun _ U => (height U : ℚ)) B k S) : ℝ) ≤ a * height T := by
  have hcompletion : (height (completePrefix M B T S k) : ℝ) ≤ a * height T := by
    by_cases hkh : k ≤ height T
    · have hb := completePrefix_height_real_envelope M B a L (by linarith) hB T S
        (height T) k hT (le_refl _) hkh
      apply hb.trans
      apply max_le
      · have hp := mul_nonneg (sub_nonneg.mpr ha.le) (Nat.cast_nonneg (height T) : (0 : ℝ) ≤ _)
        nlinarith
      · have he : ((height T - k : ℕ) : ℝ) = (height T : ℝ) - k := by
          have hecast : ((height T - k : ℕ) : ℝ) + k = height T := by
            exact_mod_cast Nat.sub_add_cancel hkh
          linarith
        rw [he]
        nlinarith
    · rw [completePrefix_past_height M B T S k (by omega)]
      have hp := mul_nonneg (sub_nonneg.mpr ha.le) (Nat.cast_nonneg (height T) : (0 : ℝ) ≤ _)
      nlinarith
  refine ⟨rollout_identifies M _ B hlegal k S, ?_⟩
  have hr : (height (rollout M (fun _ U => (height U : ℚ)) B k S) : ℝ) ≤
      height (completePrefix M B T S k) := by
    exact_mod_cast rollout_height_le_completion M B k S T hT
  exact hr.trans hcompletion

end PlanarQuery.Tree
