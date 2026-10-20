import PlanarQuery.Model
import Mathlib.Data.Finset.Max
import Mathlib.Data.List.Infix
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Linarith

/-! Finite binary words and the combinatorial capacity underlying Kraft's
inequality. Codes are actual lists of Boolean symbols, not abstract lengths. -/

namespace PlanarQuery.Coding

def words : ℕ → Finset (List Bool)
  | 0 => {[]}
  | n + 1 => (words n).image (List.cons false) ∪ (words n).image (List.cons true)

theorem mem_words (u : List Bool) (n : ℕ) : u ∈ words n ↔ u.length = n := by
  induction n generalizing u with
  | zero => cases u <;> simp [words]
  | succ n ih =>
    cases u with
    | nil => simp [words]
    | cons b u => cases b <;> simp [words, ih]

theorem cons_images_disjoint (A B : Finset (List Bool)) :
    Disjoint (A.image (List.cons false)) (B.image (List.cons true)) := by
  rw [Finset.disjoint_left]
  intro u ha hb
  obtain ⟨a, _, rfl⟩ := Finset.mem_image.mp ha
  obtain ⟨b, _, he⟩ := Finset.mem_image.mp hb
  cases he

theorem card_words (n : ℕ) : (words n).card = 2 ^ n := by
  induction n with
  | zero => simp [words]
  | succ n ih =>
    rw [words, Finset.card_union_of_disjoint (cons_images_disjoint _ _),
      Finset.card_image_of_injective _ (fun _ _ h => List.cons_injective h),
      Finset.card_image_of_injective _ (fun _ _ h => List.cons_injective h), ih]
    simp [pow_succ, Nat.mul_two]

def extensions (u : List Bool) (n : ℕ) : Finset (List Bool) :=
  (words n).filter (fun v => u <+: v)

@[simp] theorem mem_extensions (u v : List Bool) (n : ℕ) :
    v ∈ extensions u n ↔ v.length = n ∧ u <+: v := by
  simp [extensions, mem_words]

theorem extensions_eq_image (u : List Bool) (n : ℕ) (hn : u.length ≤ n) :
    extensions u n = (words (n - u.length)).image (fun v => u ++ v) := by
  ext v
  constructor
  · intro hv
    obtain ⟨hl, t, ht⟩ := (mem_extensions u v n).mp hv
    apply Finset.mem_image.mpr
    refine ⟨t, (mem_words t _).mpr ?_, ht⟩
    have he := congrArg List.length ht
    simp only [List.length_append] at he
    omega
  · intro hv
    obtain ⟨t, ht, rfl⟩ := Finset.mem_image.mp hv
    apply (mem_extensions u (u ++ t) n).mpr
    refine ⟨?_, ⟨t, rfl⟩⟩
    have hl := (mem_words t _).mp ht
    simp only [List.length_append, hl]
    omega

theorem card_extensions (u : List Bool) (n : ℕ) (hn : u.length ≤ n) :
    (extensions u n).card = 2 ^ (n - u.length) := by
  rw [extensions_eq_image u n hn, Finset.card_image_of_injective]
  · exact card_words _
  · intro v t he
    exact List.append_cancel_left he

def PrefixFree {I : Type*} (S : Finset I) (code : I → List Bool) : Prop :=
  ∀ i ∈ S, ∀ j ∈ S, i ≠ j → ¬code i <+: code j

theorem prefix_extensions_disjoint {I : Type*} (S : Finset I) (code : I → List Bool)
    (hf : PrefixFree S code) (n : ℕ) :
    S.toSet.PairwiseDisjoint (fun i => extensions (code i) n) := by
  intro i hi j hj hij
  change Disjoint (extensions (code i) n) (extensions (code j) n)
  rw [Finset.disjoint_left]
  intro u hui huj
  have hp := List.prefix_or_prefix_of_prefix
    ((mem_extensions _ _ _).mp hui).2 ((mem_extensions _ _ _).mp huj).2
  rcases hp with hp | hp
  · exact hf i hi j hj hij hp
  · exact hf j hj i hi (Ne.symm hij) hp

theorem scaled_dyadic (n l : ℕ) (hl : l ≤ n) :
    (2 : ℚ) ^ n * ((2 : ℚ)⁻¹) ^ l = (2 : ℚ) ^ (n - l) := by
  have he : n = (n - l) + l := by omega
  rw [he, pow_add, mul_assoc, ← mul_pow]
  norm_num

theorem kraft {I : Type*} (S : Finset I) (code : I → List Bool)
    (hf : PrefixFree S code) : ∑ i ∈ S, ((2 : ℚ)⁻¹) ^ (code i).length ≤ 1 := by
  classical
  by_cases hn : S.Nonempty
  · obtain ⟨a, ha, hm⟩ := Finset.exists_max_image S (fun i => (code i).length) hn
    let n := (code a).length
    have hsub : S.biUnion (fun i => extensions (code i) n) ⊆ words n := by
      intro u hu
      obtain ⟨i, hi, hui⟩ := Finset.mem_biUnion.mp hu
      exact (Finset.mem_filter.mp hui).1
    have hc := Finset.card_le_card hsub
    rw [Finset.card_biUnion (prefix_extensions_disjoint S code hf n), card_words] at hc
    have he : (∑ i ∈ S, (extensions (code i) n).card) =
        ∑ i ∈ S, 2 ^ (n - (code i).length) := by
      apply Finset.sum_congr rfl
      intro i hi
      exact card_extensions _ _ (hm i hi)
    rw [he] at hc
    have hcr : (∑ i ∈ S, (2 : ℚ) ^ (n - (code i).length)) ≤ (2 : ℚ) ^ n := by
      exact_mod_cast hc
    have hs : (2 : ℚ) ^ n * (∑ i ∈ S, ((2 : ℚ)⁻¹) ^ (code i).length) =
        ∑ i ∈ S, (2 : ℚ) ^ (n - (code i).length) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      exact scaled_dyadic _ _ (hm i hi)
    rw [← hs] at hcr
    exact (mul_le_mul_left (pow_pos (by norm_num : (0 : ℚ) < 2) n)).mp
      (by simpa using hcr)
  · rw [Finset.not_nonempty_iff_eq_empty.mp hn]
    simp

end PlanarQuery.Coding
