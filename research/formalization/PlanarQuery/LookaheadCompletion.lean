import PlanarQuery.Prefix
import PlanarQuery.TreePotentials
import Mathlib.Tactic.Linarith

/-! Exact-horizon completion acts on actual supplied-query trees. The
baseline assumption is its stated additive guarantee against every
identifying competitor; the approximation conclusion is proved here. -/

namespace PlanarQuery
namespace Tree
variable {H Q : Type*} [DecidableEq H]

def completePrefix (M : QuerySystem H Q) (B : Finset H → Tree H Q) :
    Tree H Q → Finset H → ℕ → Tree H Q
  | _, S, 0 => B S
  | .leaf h, _, _ + 1 => .leaf h
  | .node q miss hit, S, k + 1 => .node q
      (completePrefix M B miss (branch M S q false) k)
      (completePrefix M B hit (branch M S q true) k)

def prefixInvoice (M : QuerySystem H Q) (w : H → ℚ) :
    Tree H Q → Finset H → ℕ → ℚ
  | _, _, 0 => 0
  | .leaf _, _, _ + 1 => 0
  | .node q miss hit, S, k + 1 => mass w S +
      prefixInvoice M w miss (branch M S q false) k +
      prefixInvoice M w hit (branch M S q true) k

def tailInvoice (M : QuerySystem H Q) (w : H → ℚ) :
    Tree H Q → Finset H → ℕ → ℚ
  | T, S, 0 => rawExpected M w S T
  | .leaf _, _, _ + 1 => 0
  | .node q miss hit, S, k + 1 =>
      tailInvoice M w miss (branch M S q false) k +
      tailInvoice M w hit (branch M S q true) k

def frontierInvoice (M : QuerySystem H Q) (w : H → ℚ) :
    Tree H Q → Finset H → ℕ → ℚ
  | _, S, 0 => mass w S
  | .leaf _, _, _ + 1 => 0
  | .node q miss hit, S, k + 1 =>
      frontierInvoice M w miss (branch M S q false) k +
      frontierInvoice M w hit (branch M S q true) k

theorem branch_mass_add (M : QuerySystem H Q) (w : H → ℚ)
    (S : Finset H) (q : Q) :
    mass w (branch M S q false) + mass w (branch M S q true) = mass w S := by
  unfold mass
  rw [← Finset.sum_union (branches_disjoint M S q), branches_union M S q]

theorem invoices_decompose (M : QuerySystem H Q) (w : H → ℚ)
    (T : Tree H Q) (S : Finset H) (k : ℕ) :
    prefixInvoice M w T S k + tailInvoice M w T S k = rawExpected M w S T := by
  induction k generalizing T S with
  | zero => simp [prefixInvoice, tailInvoice]
  | succ k ih =>
    cases T with
    | leaf h => simp [prefixInvoice, tailInvoice, rawExpected, depth]
    | node q miss hit =>
      simp only [prefixInvoice, tailInvoice, rawExpected_node]
      have hm := ih miss (branch M S q false)
      have hh := ih hit (branch M S q true)
      linarith

theorem frontierInvoice_le_mass (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (T : Tree H Q) (S : Finset H) (k : ℕ) :
    frontierInvoice M w T S k ≤ mass w S := by
  induction k generalizing T S with
  | zero => simp [frontierInvoice]
  | succ k ih =>
    cases T with
    | leaf h => exact Finset.sum_nonneg (fun h _ => hw h)
    | node q miss hit =>
      simpa only [frontierInvoice, branch_mass_add] using
        add_le_add (ih miss (branch M S q false)) (ih hit (branch M S q true))

theorem prefixInvoice_pays_frontier (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (T : Tree H Q) (S : Finset H) (k : ℕ) :
    (k : ℚ) * frontierInvoice M w T S k ≤ prefixInvoice M w T S k := by
  induction k generalizing T S with
  | zero => simp [prefixInvoice]
  | succ k ih =>
    cases T with
    | leaf h => simp [prefixInvoice, frontierInvoice]
    | node q miss hit =>
      have hm := ih miss (branch M S q false)
      have hh := ih hit (branch M S q true)
      have hmass := frontierInvoice_le_mass M w hw (.node q miss hit) S (k+1)
      simp only [prefixInvoice, frontierInvoice, Nat.cast_add, Nat.cast_one] at *
      nlinarith

theorem completePrefix_identifies (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (hB : ∀ U, Identifies M U (B U))
    (T : Tree H Q) (S : Finset H) (k : ℕ) (hT : Identifies M S T) :
    Identifies M S (completePrefix M B T S k) := by
  induction k generalizing T S with
  | zero => simpa [completePrefix] using hB S
  | succ k ih =>
    cases T with
    | leaf h => exact hT
    | node q miss hit =>
      obtain ⟨hm, hh⟩ := identifies_children M S q miss hit hT
      have ihm := ih miss (branch M S q false) hm
      have ihh := ih hit (branch M S q true) hh
      intro h hs
      cases hq : M.answer q h
      · have hx := ihm h ((mem_branch _ _ _ _ _).mpr ⟨hs, hq⟩)
        simpa [completePrefix, eval, hq] using hx
      · have hx := ihh h ((mem_branch _ _ _ _ _).mpr ⟨hs, hq⟩)
        simpa [completePrefix, eval, hq] using hx

theorem completePrefix_invoice_bound (M : QuerySystem H Q) (w : H → ℚ)
    (B : Finset H → Tree H Q) (a L : ℚ)
    (hB : ∀ U T, Identifies M U T →
      rawExpected M w U (B U) ≤ a * rawExpected M w U T + L * mass w U)
    (T : Tree H Q) (S : Finset H) (k : ℕ) (hT : Identifies M S T) :
    rawExpected M w S (completePrefix M B T S k) ≤
      prefixInvoice M w T S k + a * tailInvoice M w T S k +
        L * frontierInvoice M w T S k := by
  induction k generalizing T S with
  | zero => simpa [completePrefix, prefixInvoice, tailInvoice, frontierInvoice] using hB S T hT
  | succ k ih =>
    cases T with
    | leaf h => simp [completePrefix, prefixInvoice, tailInvoice, frontierInvoice, rawExpected, depth]
    | node q miss hit =>
      obtain ⟨hm, hh⟩ := identifies_children M S q miss hit hT
      have ihm := ih miss (branch M S q false) hm
      have ihh := ih hit (branch M S q true) hh
      simp only [completePrefix, rawExpected_node, prefixInvoice, tailInvoice, frontierInvoice]
      linarith

theorem frontierInvoice_nonneg (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (T : Tree H Q) (S : Finset H) (k : ℕ) :
    0 ≤ frontierInvoice M w T S k := by
  induction k generalizing T S with
  | zero => simpa [frontierInvoice, mass] using Finset.sum_nonneg (fun h (_ : h ∈ S) => hw h)
  | succ k ih =>
    cases T with
    | leaf h => simp [frontierInvoice]
    | node q miss hit => exact add_nonneg (ih miss _) (ih hit _)

/-- This is the full expected-cost cancellation on an executable
completion, with no assumed frontier or entropy inequalities. -/
theorem completePrefix_expected_approximation (M : QuerySystem H Q) (w : H → ℚ)
    (hw : ∀ h, 0 ≤ w h) (B : Finset H → Tree H Q) (a L : ℚ)
    (ha : 1 < a) (k : ℕ) (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T →
      rawExpected M w U (B U) ≤ a * rawExpected M w U T + L * mass w U)
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    rawExpected M w S (completePrefix M B T S k) ≤ a * rawExpected M w S T := by
  have hf := frontierInvoice_nonneg M w hw T S k
  have hp := prefixInvoice_pays_frontier M w hw T S k
  have hc := completePrefix_invoice_bound M w B a L hB T S k hT
  have he := invoices_decompose M w T S k
  have hl := mul_le_mul_of_nonneg_right hk hf
  have hp' := mul_le_mul_of_nonneg_left hp (sub_nonneg.mpr ha.le)
  nlinarith

theorem completePrefix_past_height (M : QuerySystem H Q) (B : Finset H → Tree H Q)
    (T : Tree H Q) (S : Finset H) (k : ℕ) (hk : height T < k) :
    completePrefix M B T S k = T := by
  induction k generalizing T S with
  | zero => omega
  | succ k ih =>
    cases T with
    | leaf h => rfl
    | node q miss hit =>
      have hm : height miss < k := by simp only [height] at hk; omega
      have hh : height hit < k := by simp only [height] at hk; omega
      simp [completePrefix, ih miss _ hm, ih hit _ hh]

/-- A completed height-D competitor either ends early, or pays k prefix
queries before invoking a baseline on a subtree of height at most D-k. -/
theorem completePrefix_height_envelope (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (a L : ℚ) (ha : 0 ≤ a)
    (hB : ∀ U T, Identifies M U T → (height (B U) : ℚ) ≤ a * height T + L)
    (T : Tree H Q) (S : Finset H) (D k : ℕ)
    (hT : Identifies M S T) (hD : height T ≤ D) (hk : k ≤ D) :
    (height (completePrefix M B T S k) : ℚ) ≤
      max (D : ℚ) ((k : ℚ) + a * (D - k : ℕ) + L) := by
  induction k generalizing T S D with
  | zero =>
    have hb := hB S T hT
    have hd : (height T : ℚ) ≤ D := by exact_mod_cast hD
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
      have ihm := ih miss (branch M S q false) (D-1) hm hmD hkd
      have ihh := ih hit (branch M S q true) (D-1) hh hhD hkd
      have heq : D - 1 - k = D - (k + 1) := by omega
      rw [heq] at ihm ihh
      have hcast : ((D - 1 : ℕ) : ℚ) + 1 = D := by
        exact_mod_cast (show D - 1 + 1 = D by omega)
      have hm' := max_le ihm ihh
      have hadd := add_le_add_left hm' 1
      simp only [completePrefix, height, Nat.cast_add, Nat.cast_one, Nat.cast_max]
      have hmax : 1 + max ((D-1 : ℕ) : ℚ)
          ((k : ℚ) + a * (D-(k+1) : ℕ) + L) =
          max (D : ℚ) ((k : ℚ) + 1 + a * (D-(k+1) : ℕ) + L) := by
        rw [add_max]
        congr 1 <;> linarith
      rw [hmax] at hadd
      exact hadd

theorem completePrefix_height_approximation (M : QuerySystem H Q)
    (B : Finset H → Tree H Q) (a L : ℚ) (ha : 1 < a) (k : ℕ)
    (hk : L ≤ (a - 1) * k)
    (hB : ∀ U T, Identifies M U T → (height (B U) : ℚ) ≤ a * height T + L)
    (T : Tree H Q) (S : Finset H) (hT : Identifies M S T) :
    (height (completePrefix M B T S k) : ℚ) ≤ a * height T := by
  by_cases hkh : k ≤ height T
  · have hb := completePrefix_height_envelope M B a L (by linarith) hB T S
      (height T) k hT (le_refl _) hkh
    apply hb.trans
    apply max_le
    · have hp := mul_nonneg (sub_nonneg.mpr ha.le) (Nat.cast_nonneg (height T) : (0:ℚ) ≤ _)
      nlinarith
    · have he : ((height T - k : ℕ) : ℚ) = (height T : ℚ) - k := by
        have hecast : ((height T - k : ℕ) : ℚ) + k = height T := by
          exact_mod_cast Nat.sub_add_cancel hkh
        linarith
      rw [he]
      nlinarith
  · rw [completePrefix_past_height M B T S k (by omega)]
    have hp := mul_nonneg (sub_nonneg.mpr ha.le) (Nat.cast_nonneg (height T) : (0:ℚ) ≤ _)
    nlinarith

end Tree
end PlanarQuery
