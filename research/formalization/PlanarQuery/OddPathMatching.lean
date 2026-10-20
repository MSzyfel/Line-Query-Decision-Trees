import Mathlib.Data.Finset.Card
import Mathlib.Data.Finset.Basic
import Mathlib.Data.Finset.Max
import Mathlib.Data.Fintype.Basic
import Mathlib.Data.Fintype.Card
import Mathlib.Data.Fintype.EquivFin
import Lean.Elab.Tactic.Omega

/-!
# Matchings on the alternating odd path

This file isolates the finite combinatorics used by the odd-path lemma.  The
vertices are numbered `0, …, 2*t`; even numbers denote `E` vertices and odd
numbers denote `B` vertices.  Edge `i` joins vertices `i` and `i+1`.

The matching predicate below is stated directly on edge positions.  We also
record the basic one-choice-per-two-edge-block counting bound.  The present
file does not yet prove that arbitrary path matchings admit that encoding.
-/

namespace PlanarQuery
namespace OddPathMatching

/-- The finite edge positions of the path `E₀,B₁,…,Eₜ`. -/
abbrev Edge (t : Nat) := Fin (2 * t)

/-- A set of edge positions is a matching when it contains no adjacent pair. -/
def IsMatching (t : Nat) (M : Finset (Edge t)) : Prop :=
  ∀ i j : Edge t, i ∈ M → j ∈ M → i ≠ j →
    i.val + 1 ≠ j.val ∧ j.val + 1 ≠ i.val

/-- The even-position vertices `E₀,…,Eₜ`, indexed by `0,…,t`. -/
abbrev EvenVertex (t : Nat) := Fin (t + 1)

/-- The odd-position vertices `B₁,…,Bₜ`, indexed by `1,…,t`. -/
abbrev OddVertex (t : Nat) := Fin t

/-- The position of the even endpoint of edge `i`. -/
def evenEndpoint {t : Nat} (i : Edge t) : EvenVertex t :=
  Fin.mk (if i.val % 2 = 0 then i.val / 2 else (i.val + 1) / 2) (by
    have hi := i.isLt
    split_ifs <;> omega)

/-- The position of the odd endpoint of edge `i`, in the `1,…,t` indexing. -/
def oddEndpoint {t : Nat} (i : Edge t) : OddVertex t :=
  Fin.mk (i.val / 2) (by
    have hi := i.isLt
    omega)

/-- The chosen edge in a two-edge block: `false` is its even edge and `true`
is its odd edge. `none` means that the block is unused. -/
abbrev AlternatingChoice (t : Nat) := Fin t → Option Bool

/-- The number of selected edges in an alternating-choice representation. -/
def choiceSize {t : Nat} (c : AlternatingChoice t) : Nat :=
  (Finset.univ.filter fun j : Fin t => (c j).isSome).card

/-- Every block contributes at most one edge, so the represented matching has
at most `t` edges. -/
theorem choiceSize_le (t : Nat) (c : AlternatingChoice t) :
    choiceSize c <= t := by
  classical
  unfold choiceSize
  calc
    _ <= Finset.univ.card := Finset.card_le_card (Finset.filter_subset _ _)
    _ = t := Finset.card_fin t

/-- A choice occupying every block has exactly `t` edges. -/
theorem choiceSize_eq_of_full (t : Nat) (c : AlternatingChoice t)
    (hc : forall j : Fin t, (c j).isSome) : choiceSize c = t := by
  classical
  unfold choiceSize
  have hfilter : (Finset.univ.filter (fun j : Fin t => (c j).isSome)) =
      Finset.univ := by
    ext j
    simp only [Finset.mem_filter, Finset.mem_univ, true_and]
    simpa using hc j
  rw [hfilter]
  exact Finset.card_fin t

/-- The two-edge block containing an edge. -/
def blockIndex {t : Nat} (i : Edge t) : Fin t :=
  Fin.mk (i.val / 2) (by
    have hi := i.isLt
    omega)

/-- Regard the edges of a matching as a finite subtype, so that the block
assignment can be studied as a map between finite types. -/
def matchingBlockMap {t : Nat} (M : Finset (Edge t)) :
    {i : Edge t // i ∈ M} → Fin t := fun i => blockIndex i.1

/-- Distinct matching edges cannot lie in the same two-edge block. -/
theorem matchingBlockMap_injective (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) : Function.Injective (matchingBlockMap M) := by
  intro a b hab
  apply Subtype.ext
  apply Fin.ext
  have hquot : a.1.val / 2 = b.1.val / 2 := by
    simpa [matchingBlockMap, blockIndex] using congrArg Fin.val hab
  by_contra hne
  have hdiff : a.1 ≠ b.1 := by
    intro heq
    apply hne
    exact congrArg Fin.val heq
  have hsep := hM a.1 b.1 a.2 b.2 hdiff
  have ha := a.1.isLt
  have hb := b.1.isLt
  omega

/-- If a path matching has the maximum possible size `t`, every two-edge
block contains one of its edges. Indeed, the injective block assignment then
maps two finite sets of the same cardinality, so it is surjective. -/
theorem matching_card_eq_forces_block_occupancy (t : Nat)
    (M : Finset (Edge t)) (hM : IsMatching t M) (hcard : M.card = t) :
    Function.Surjective (matchingBlockMap M) := by
  have hmap := matchingBlockMap_injective t M hM
  have hsource : Fintype.card {i : Edge t // i ∈ M} = M.card := by simp
  have htarget : Fintype.card (Fin t) = t := Fintype.card_fin t
  have hbijective := (Fintype.bijective_iff_injective_and_card
      (matchingBlockMap M)).2 ⟨hmap, by simp [hsource, htarget, hcard]⟩
  exact hbijective.2

/-- In a maximum matching, an odd-position choice forces the next block to
choose its odd edge as well. The even edge in that next block would be
adjacent to the already chosen edge, so block occupancy forces propagation
to the right. -/
theorem matching_odd_choice_propagates (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) (hcard : M.card = t)
    (j : Fin t) (hnext : j.val + 1 < t)
    (i : Edge t) (hiM : i ∈ M)
    (hiblock : blockIndex i = j) (hiodd : i.val % 2 = 1) :
    ∃ k : Edge t, k ∈ M ∧ blockIndex k = ⟨j.val + 1, hnext⟩ ∧
      k.val % 2 = 1 := by
  have hocc := matching_card_eq_forces_block_occupancy t M hM hcard
  obtain ⟨k, hk⟩ := hocc ⟨j.val + 1, hnext⟩
  have hkM : k.1 ∈ M := k.2
  have hkblock : blockIndex k.1 = ⟨j.val + 1, hnext⟩ := hk
  have hival : i.val = 2 * j.val + 1 := by
    have hq := congrArg Fin.val hiblock
    simp [blockIndex] at hq
    omega
  have hkv := k.1.isLt
  have hq := congrArg Fin.val hkblock
  simp [blockIndex] at hq
  have hkeven_or_odd : k.1.val = 2 * (j.val + 1) ∨
      k.1.val = 2 * (j.val + 1) + 1 := by
    omega
  rcases hkeven_or_odd with hkeven | hkodd
  · have hdiff : i ≠ k.1 := by
      intro heq
      have := congrArg Fin.val heq
      omega
    have hsep := hM i k.1 hiM hkM hdiff
    omega
  · exact ⟨k.1, hkM, hkblock, by omega⟩

/-- The even endpoints used by a matching.  Each chosen edge contributes its
unique even endpoint to this finite set. -/
def coveredEvenVertices {t : Nat} (M : Finset (Edge t)) :
    Finset (EvenVertex t) :=
  Finset.univ.image (fun i : {i : Edge t // i ∈ M} => evenEndpoint i.1)

/-- Distinct edges in a matching have distinct even endpoints: the two edges
incident to one even vertex are consecutive, and hence cannot both be chosen. -/
theorem matchingEvenEndpoint_injective (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) :
    Function.Injective (fun i : {i : Edge t // i ∈ M} => evenEndpoint i.1) := by
  intro a b hab
  apply Subtype.ext
  apply Fin.ext
  have haform : a.1.val = 2 * (evenEndpoint a.1).val ∨
      a.1.val + 1 = 2 * (evenEndpoint a.1).val := by
    unfold evenEndpoint
    split_ifs <;> simp only [Fin.val_mk] <;> omega
  have hbform : b.1.val = 2 * (evenEndpoint b.1).val ∨
      b.1.val + 1 = 2 * (evenEndpoint b.1).val := by
    unfold evenEndpoint
    split_ifs <;> simp only [Fin.val_mk] <;> omega
  have hendpoint : (evenEndpoint a.1).val = (evenEndpoint b.1).val :=
    congrArg Fin.val hab
  have hval : a.1.val = b.1.val := by
    by_contra hneval
    have hneq : a.1 ≠ b.1 := by
      intro heq
      apply hneval
      exact congrArg Fin.val heq
    have hsep := hM a.1 b.1 a.2 b.2 hneq
    rcases haform with ha | ha <;> rcases hbform with hb | hb <;> omega
  exact hval

/-- A maximum matching on the path with `2*t` edges covers all but one of the
`t+1` even vertices.  The missing vertex is unique: every chosen edge has one
even endpoint, distinct matching edges have distinct even endpoints, and the
matching contains `t` edges.  Thus its endpoint set has size `t`, while the
even side has size `t+1`. -/
theorem matching_maximum_leaves_unique_even_vertex (t : Nat)
    (M : Finset (Edge t)) (hM : IsMatching t M) (hcard : M.card = t) :
    ∃! v : EvenVertex t, v ∉ coveredEvenVertices M := by
  classical
  let S := coveredEvenVertices M
  have hS_card : S.card = t := by
    dsimp [S, coveredEvenVertices]
    rw [Finset.card_image_of_injective _ (matchingEvenEndpoint_injective t M hM)]
    simp [hcard]
  have hS_subset : S ⊆ Finset.univ := Finset.subset_univ _
  have hmissing_card : (Finset.univ \ S).card = 1 := by
    rw [Finset.card_sdiff hS_subset]
    simp only [Finset.card_univ, Fintype.card_fin, hS_card]
    omega
  obtain ⟨v, hv⟩ := Finset.card_eq_one.mp hmissing_card
  refine ⟨v, ?_, ?_⟩
  · have hvmem : v ∈ Finset.univ \ S := by
      rw [hv]
      simp
    exact (Finset.mem_sdiff.mp hvmem).2
  · intro w hw
    have hwmem : w ∈ Finset.univ \ S :=
      Finset.mem_sdiff.mpr ⟨Finset.mem_univ _, hw⟩
    rw [hv] at hwmem
    simpa using hwmem

/-- Once a block uses its odd edge, every later block uses its odd edge too.
The one-block step is `matching_odd_choice_propagates`; induction extends that
local implication across the remainder of the path. -/
theorem matching_odd_choice_propagates_to (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) (hcard : M.card = t)
    (j : Fin t) (i : Edge t) (hiM : i ∈ M)
    (hiblock : blockIndex i = j) (hiodd : i.val % 2 = 1)
    (d : Nat) (hd : j.val + d < t) :
    ∃ e : Edge t, e ∈ M ∧
      blockIndex e = ⟨j.val + d, hd⟩ ∧ e.val % 2 = 1 := by
  induction d with
  | zero =>
      refine ⟨i, hiM, ?_, hiodd⟩
      apply Fin.ext
      have hval := congrArg Fin.val hiblock
      simpa using hval
  | succ d ih =>
      have hmid : j.val + d < t := by omega
      obtain ⟨e, heM, heblock, heodd⟩ := ih hmid
      let mid : Fin t := ⟨j.val + d, hmid⟩
      have hnext : mid.val + 1 < t := by
        dsimp [mid]
        omega
      obtain ⟨e', he'M, he'block, he'odd⟩ :=
        matching_odd_choice_propagates t M hM hcard mid hnext e heM heblock heodd
      refine ⟨e', he'M, ?_, he'odd⟩
      apply Fin.ext
      have hval := congrArg Fin.val he'block
      dsimp [mid] at hval
      simpa using hval

/-- The choices in a maximum matching on the path have a single cutoff:
before it every block uses its even edge, and from it onward every block
uses its odd edge.  If no odd edge occurs, the cutoff is the right boundary. -/
theorem matching_has_even_to_odd_cutoff (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) (hcard : M.card = t) :
    ∃ cutoff : Fin (t + 1),
      (∀ j : Fin t, j.val < cutoff.val →
        ∃ i : Edge t, i ∈ M ∧ blockIndex i = j ∧ i.val % 2 = 0) ∧
      (∀ j : Fin t, cutoff.val ≤ j.val →
        ∃ i : Edge t, i ∈ M ∧ blockIndex i = j ∧ i.val % 2 = 1) := by
  classical
  let oddAt : Fin t → Prop := fun j =>
    ∃ i : Edge t, i ∈ M ∧ blockIndex i = j ∧ i.val % 2 = 1
  let oddBlocks : Finset (Fin t) := Finset.univ.filter oddAt
  have hoccupy := matching_card_eq_forces_block_occupancy t M hM hcard
  by_cases hne : oddBlocks.Nonempty
  · let first := oddBlocks.min' hne
    let cutoff : Fin (t + 1) := ⟨first.val, by
      have := first.isLt
      omega⟩
    refine ⟨cutoff, ?_, ?_⟩
    · intro j hj
      obtain ⟨q, hq⟩ := hoccupy j
      have hiblock : blockIndex q.1 = j := by
        simpa [matchingBlockMap] using hq
      have hiodd : q.1.val % 2 ≠ 1 := by
        intro hi
        have hjodd : j ∈ oddBlocks := by
          simp [oddBlocks, oddAt]
          exact ⟨q.1, q.2, hiblock, hi⟩
        have hmin := Finset.min'_le oddBlocks j hjodd
        have hminval := (Fin.le_iff_val_le_val).mp hmin
        dsimp [cutoff, first] at hj
        omega
      refine ⟨q.1, q.2, hiblock, ?_⟩
      have hi_lt : q.1.val < 2 * t := q.1.isLt
      omega
    · intro j hj
      have hfirstOdd : oddAt first := by
        have hmem : first ∈ oddBlocks := Finset.min'_mem oddBlocks hne
        simpa [oddBlocks] using (Finset.mem_filter.mp hmem).2
      obtain ⟨i, hiM, hiblock, hiodd⟩ := hfirstOdd
      have hstart : first.val ≤ j.val := by
        dsimp [cutoff, first] at hj ⊢
        exact hj
      have hdist : j.val - first.val < t := by
        have := j.isLt
        omega
      obtain ⟨e, heM, heblock, heodd⟩ :=
        matching_odd_choice_propagates_to t M hM hcard first i hiM hiblock hiodd
          (j.val - first.val) (by omega)
      refine ⟨e, heM, ?_, heodd⟩
      apply Fin.ext
      have hval := congrArg Fin.val heblock
      simp at hval
      omega
  · let cutoff : Fin (t + 1) := ⟨t, by omega⟩
    refine ⟨cutoff, ?_, ?_⟩
    · intro j hj
      have hjoddFalse : ¬ oddAt j := by
        intro hjodd
        have : j ∈ oddBlocks := by simp [oddBlocks, hjodd]
        exact hne ⟨j, this⟩
      obtain ⟨q, hq⟩ := hoccupy j
      have hiblock : blockIndex q.1 = j := by
        simpa [matchingBlockMap] using hq
      have hiodd : q.1.val % 2 ≠ 1 := by
        intro hi
        exact hjoddFalse ⟨q.1, q.2, hiblock, hi⟩
      refine ⟨q.1, q.2, hiblock, ?_⟩
      have hi_lt : q.1.val < 2 * t := q.1.isLt
      omega
    · intro j hj
      have hjlt := j.isLt
      dsimp [cutoff] at hj
      omega

/-- Every matching on the `2*t` edges of the path has at most `t` edges.
Map each chosen edge to the two-edge block containing it. Two distinct edges
in one block are adjacent, so the matching condition makes this map injective. -/
theorem matching_card_le (t : Nat) (M : Finset (Edge t))
    (hM : IsMatching t M) : M.card <= t := by
  have hcard := Fintype.card_le_of_injective
    (matchingBlockMap M) (matchingBlockMap_injective t M hM)
  have hsource : Fintype.card {i // i ∈ M} = M.card := by simp
  have htarget : Fintype.card (Fin t) = t := Fintype.card_fin t
  omega

end OddPathMatching
end PlanarQuery
