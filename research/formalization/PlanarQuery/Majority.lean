import PlanarQuery.Model
import Mathlib.Tactic.Linarith

/-! Finite-state majority intersection and the algebraic two-support cap
implication. These are separate from geometric existence obligations:
this module does not prove planar Helly, the existence of a common strict
witness, a hull support decomposition, or the circular-interval property.
The two-support implication requires its displayed representation as data.
All state masses use the original rational weights from `Tree.mass`. -/

namespace PlanarQuery

variable {H Q : Type*} [DecidableEq H]

/-- Positive original weights give positive mass on a nonempty live state. -/
theorem state_mass_positive (weight : H → ℚ) (S : Finset H)
    (hS : S.Nonempty) (hw : ∀ h ∈ S, 0 < weight h) :
    0 < Tree.mass weight S := by
  exact Finset.sum_pos hw hS

/-- Union mass is subadditive when the sets lie in a nonnegative state. -/
theorem state_union_mass_le (weight : H → ℚ) (S A B : Finset H)
    (hA : A ⊆ S) (_hB : B ⊆ S) (hw : ∀ h ∈ S, 0 ≤ weight h) :
    Tree.mass weight (A ∪ B) ≤ Tree.mass weight A + Tree.mass weight B := by
  have hi : 0 ≤ Tree.mass weight (A ∩ B) := by
    apply Finset.sum_nonneg
    intro h hh
    exact hw h (hA (Finset.mem_inter.mp hh).1)
  have he := Finset.sum_union_inter (s₁ := A) (s₂ := B) (f := weight)
  change Tree.mass weight (A ∪ B) + Tree.mass weight (A ∩ B) =
    Tree.mass weight A + Tree.mass weight B at he
  linarith

/-- Three minority sets cannot cover a nonempty live state when each has
mass strictly below delta times state mass and delta is below one third.
Overlaps are allowed; positivity is required only on the live state. -/
theorem three_small_sets_omit (weight : H → ℚ) (S A B C : Finset H)
    (hS : S.Nonempty) (hw : ∀ h ∈ S, 0 < weight h)
    (hA : A ⊆ S) (hB : B ⊆ S) (hC : C ⊆ S)
    (delta : ℚ) (hdelta : delta < (1 : ℚ) / 3)
    (ha : Tree.mass weight A < delta * Tree.mass weight S)
    (hb : Tree.mass weight B < delta * Tree.mass weight S)
    (hc : Tree.mass weight C < delta * Tree.mass weight S) :
    ∃ h ∈ S, h ∉ A ∧ h ∉ B ∧ h ∉ C := by
  classical
  by_contra hnone
  have hcover : S ⊆ (A ∪ B) ∪ C := by
    intro h hs
    by_cases hmA : h ∈ A
    · exact Finset.mem_union.mpr
        (Or.inl (Finset.mem_union.mpr (Or.inl hmA)))
    by_cases hmB : h ∈ B
    · exact Finset.mem_union.mpr
        (Or.inl (Finset.mem_union.mpr (Or.inr hmB)))
    by_cases hmC : h ∈ C
    · exact Finset.mem_union.mpr (Or.inr hmC)
    exact False.elim (hnone ⟨h, hs, hmA, hmB, hmC⟩)
  have hAB : A ∪ B ⊆ S := Finset.union_subset hA hB
  have hABC : (A ∪ B) ∪ C ⊆ S := Finset.union_subset hAB hC
  have heq : (A ∪ B) ∪ C = S := Finset.Subset.antisymm hABC hcover
  have hnonneg : ∀ h ∈ S, 0 ≤ weight h := fun h hs => (hw h hs).le
  have hboundAB := state_union_mass_le weight S A B hA hB hnonneg
  have hboundABC := state_union_mass_le weight S (A ∪ B) C hAB hC hnonneg
  rw [heq] at hboundABC
  have hmass := state_mass_positive weight S hS hw
  have hscaled := mul_lt_mul_of_pos_right hdelta hmass
  nlinarith

/-- For a binary supplied query, avoiding one answer class inside S means
belonging to the opposite class. No new query or partition is introduced. -/
theorem mem_opposite_branch (M : QuerySystem H Q) (S : Finset H)
    (q : Q) (b : Bool) (h : H) (hs : h ∈ S)
    (hn : h ∉ Tree.branch M S q b) :
    h ∈ Tree.branch M S q (!b) := by
  apply (Tree.mem_branch M S q (!b) h).mpr
  refine ⟨hs, ?_⟩
  have hne : M.answer q h ≠ b := by
    intro he
    exact hn ((Tree.mem_branch M S q b h).mpr ⟨hs, he⟩)
  cases ha : M.answer q h <;> cases b <;> simp_all

/-- An actual state hypothesis simultaneously has all three majority
answers when the three opposite, minority branches have small mass. -/
theorem three_minority_branches_intersect (M : QuerySystem H Q)
    (weight : H → ℚ) (S : Finset H) (q₁ q₂ q₃ : Q) (b₁ b₂ b₃ : Bool)
    (hS : S.Nonempty) (hw : ∀ h ∈ S, 0 < weight h)
    (delta : ℚ) (hdelta : delta < (1 : ℚ) / 3)
    (h₁ : Tree.mass weight (Tree.branch M S q₁ b₁) < delta * Tree.mass weight S)
    (h₂ : Tree.mass weight (Tree.branch M S q₂ b₂) < delta * Tree.mass weight S)
    (h₃ : Tree.mass weight (Tree.branch M S q₃ b₃) < delta * Tree.mass weight S) :
    ((Tree.branch M S q₁ (!b₁) ∩ Tree.branch M S q₂ (!b₂)) ∩
      Tree.branch M S q₃ (!b₃)).Nonempty := by
  have hsub : ∀ (q : Q) (b : Bool), Tree.branch M S q b ⊆ S := by
    intro q b h hh
    exact ((Tree.mem_branch M S q b h).mp hh).1
  obtain ⟨h, hs, hn₁, hn₂, hn₃⟩ := three_small_sets_omit weight S
    (Tree.branch M S q₁ b₁) (Tree.branch M S q₂ b₂) (Tree.branch M S q₃ b₃)
    hS hw (hsub q₁ b₁) (hsub q₂ b₂) (hsub q₃ b₃)
    delta hdelta h₁ h₂ h₃
  exact ⟨h, Finset.mem_inter.mpr ⟨Finset.mem_inter.mpr
    ⟨mem_opposite_branch M S q₁ b₁ h hs hn₁,
     mem_opposite_branch M S q₂ b₂ h hs hn₂⟩,
    mem_opposite_branch M S q₃ b₃ h hs hn₃⟩⟩

/-- Exact rational two-dimensional dot product. -/
def rationalDot (v x : ℚ × ℚ) : ℚ := v.1 * x.1 + v.2 * x.2

/-- A support representation with the omitted coefficient assigned to
 the origin when alpha + beta is below one. -/
def rationalSupportCombination (alpha beta : ℚ) (v w : ℚ × ℚ) : ℚ × ℚ :=
  (alpha * v.1 + beta * w.1, alpha * v.2 + beta * w.2)

theorem rationalDot_supportCombination (alpha beta : ℚ) (v w x : ℚ × ℚ) :
    rationalDot (rationalSupportCombination alpha beta v w) x =
      alpha * rationalDot v x + beta * rationalDot w x := by
  unfold rationalDot rationalSupportCombination
  ring

/-- If neither support vector has a positive normalized cap answer, a
nonnegative subconvex combination cannot have one either. -/
theorem two_support_dot_le (alpha beta : ℚ) (v w x : ℚ × ℚ)
    (ha : 0 ≤ alpha) (hb : 0 ≤ beta) (hsum : alpha + beta ≤ 1)
    (hv : rationalDot v x ≤ 1) (hw : rationalDot w x ≤ 1) :
    rationalDot (rationalSupportCombination alpha beta v w) x ≤ 1 := by
  rw [rationalDot_supportCombination]
  calc
    alpha * rationalDot v x + beta * rationalDot w x
        ≤ alpha * 1 + beta * 1 :=
      add_le_add (mul_le_mul_of_nonneg_left hv ha) (mul_le_mul_of_nonneg_left hw hb)
    _ = alpha + beta := by ring
    _ ≤ 1 := hsum

/-- Elementary normalized two-support cap containment. Existence and
adjacency of such supports are not hypotheses silently discharged here. -/
theorem two_support_cap_implication (alpha beta : ℚ) (u v w x : ℚ × ℚ)
    (ha : 0 ≤ alpha) (hb : 0 ≤ beta) (hsum : alpha + beta ≤ 1)
    (hu : u = rationalSupportCombination alpha beta v w)
    (hcap : 1 < rationalDot u x) :
    1 < rationalDot v x ∨ 1 < rationalDot w x := by
  by_cases hv : 1 < rationalDot v x
  · exact Or.inl hv
  by_cases hw : 1 < rationalDot w x
  · exact Or.inr hw
  have hbound := two_support_dot_le alpha beta v w x ha hb hsum
    (le_of_not_gt hv) (le_of_not_gt hw)
  rw [← hu] at hbound
  linarith

end PlanarQuery