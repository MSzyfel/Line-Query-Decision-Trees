import PlanarQuery.Coding

/-! Constructive finite Kraft converse. Inductively insert a longest remaining
word. Previously allocated shorter prefixes forbid fewer than all words at
that depth, so a new word exists outside their extensions. -/

namespace PlanarQuery.Coding

theorem kraft_converse {I : Type*} (S : Finset I) (lengths : I → ℕ)
    (hk : ∑ i ∈ S, ((2 : ℚ)⁻¹) ^ lengths i ≤ 1) :
    ∃ code : I → List Bool, (∀ i ∈ S, (code i).length = lengths i) ∧ PrefixFree S code := by
  classical
  revert hk
  refine Finset.strongInductionOn S ?_
  intro S ih hk
  by_cases hn : S.Nonempty
  · obtain ⟨a, ha, hmax⟩ := Finset.exists_max_image S lengths hn
    let d := lengths a
    have hk' : (∑ i ∈ S.erase a, ((2 : ℚ)⁻¹) ^ lengths i) ≤ 1 := by
      apply le_trans _ hk
      exact Finset.sum_le_sum_of_subset_of_nonneg (Finset.erase_subset _ _)
        (fun i hi hni => pow_nonneg (by norm_num : (0 : ℚ) ≤ 2⁻¹) _)
    obtain ⟨code, hlen, hfree⟩ := ih (S.erase a) (Finset.erase_ssubset ha) hk'
    let forbidden := (S.erase a).biUnion (fun i => extensions (code i) d)
    have hfc : forbidden.card ≤ ∑ i ∈ S.erase a, 2 ^ (d - lengths i) := by
      apply le_trans Finset.card_biUnion_le
      apply Finset.sum_le_sum
      intro i hi
      have hil := hlen i hi
      rw [card_extensions _ _ (by rw [hil]; exact hmax i (Finset.mem_erase.mp hi).2), hil]
    have hs : (2 : ℚ) ^ d * (∑ i ∈ S, ((2 : ℚ)⁻¹) ^ lengths i) =
        ∑ i ∈ S, (2 : ℚ) ^ (d - lengths i) := by
      rw [Finset.mul_sum]
      apply Finset.sum_congr rfl
      intro i hi
      exact scaled_dyadic d _ (hmax i hi)
    have hsc : (∑ i ∈ S, (2 : ℚ) ^ (d - lengths i)) ≤ (2 : ℚ) ^ d := by
      rw [← hs]
      simpa using mul_le_mul_of_nonneg_left hk (pow_nonneg (by norm_num : (0 : ℚ) ≤ 2) d)
    have hsn : (∑ i ∈ S, 2 ^ (d - lengths i) : ℕ) ≤ 2 ^ d := by exact_mod_cast hsc
    have he : (∑ i ∈ S.erase a, 2 ^ (d - lengths i)) + 1 =
        ∑ i ∈ S, 2 ^ (d - lengths i) := by
      simpa [d] using Finset.sum_erase_add S (fun i => 2 ^ (d - lengths i)) ha
    have hlt : forbidden.card < (words d).card := by
      rw [card_words]
      omega
    obtain ⟨u, hu, huf⟩ := Finset.exists_mem_not_mem_of_card_lt_card hlt
    have hul : u.length = d := (mem_words u d).mp hu
    have havoid : ∀ i ∈ S.erase a, ¬code i <+: u := by
      intro i hi hp
      apply huf
      apply Finset.mem_biUnion.mpr
      exact ⟨i, hi, (mem_extensions _ _ _).mpr ⟨hul, hp⟩⟩
    refine ⟨fun i => if i = a then u else code i, ?_, ?_⟩
    · intro i hi
      by_cases hea : i = a
      · subst i; simpa using hul
      · simpa [hea] using hlen i (Finset.mem_erase.mpr ⟨hea, hi⟩)
    · intro i hi j hj hij
      by_cases hia : i = a
      · subst i
        have hja : j ≠ a := Ne.symm hij
        simp only [if_pos rfl, if_neg hja]
        intro hp
        simp only [ite_true] at hp
        have hjold := Finset.mem_erase.mpr ⟨hja, hj⟩
        have hl : (code j).length ≤ u.length := by rw [hlen j hjold, hul]; exact hmax j hj
        have heq := hp.eq_of_length_le hl
        exact havoid j hjold (by rw [heq])
      · by_cases hja : j = a
        · subst j
          simpa [hia] using havoid i (Finset.mem_erase.mpr ⟨hia, hi⟩)
        · simp only [if_neg hia, if_neg hja]
          exact hfree i (Finset.mem_erase.mpr ⟨hia, hi⟩)
            j (Finset.mem_erase.mpr ⟨hja, hj⟩) hij
  · refine ⟨fun _ => [], ?_, ?_⟩
    · intro i hi
      exact False.elim (hn ⟨i, hi⟩)
    · intro i hi
      exact False.elim (hn ⟨i, hi⟩)

end PlanarQuery.Coding
