import PlanarQuery.Model

/-! Reusable height credit for a shared branch prefix.

This module formalizes only the supplied-query tree fact.  It does not
derive common answers from planar hull supports; that geometric premise is
kept explicit in `CommonPrefix`. -/

namespace PlanarQuery
namespace Tree

variable {H Q : Type*} [DecidableEq H]

/-- `CommonPrefix M A T n` says that the first `n` nodes of `T` follow
answers that are constant over the live hypothesis set `A`. -/
def CommonPrefix (M : QuerySystem H Q) (A : Finset H) :
    Tree H Q → Nat → Prop
  | _, 0 => True
  | .leaf _, _ + 1 => False
  | .node q miss hit, n + 1 =>
      (∀ h ∈ A, M.answer q h = false) ∧ CommonPrefix M A miss n ∨
      (∀ h ∈ A, M.answer q h = true) ∧ CommonPrefix M A hit n

/-- If a nonempty live set agrees on the next answer at the root, restriction
contracts that root and retains exactly the corresponding restricted child. -/
theorem restrict_common_root {M : QuerySystem H Q} {A : Finset H}
    (hA : A.Nonempty) (q : Q) (miss hit : Tree H Q)
    (b : Bool) (hanswer : ∀ h ∈ A, M.answer q h = b) :
    restrict M (.node q miss hit) A =
      restrict M (if b then hit else miss) A := by
  have hbranch : branch M A q b = A := by
    ext h
    simp only [mem_branch]
    constructor
    · rintro ⟨ha, hb⟩
      exact ha
    · intro ha
      exact ⟨ha, hanswer h ha⟩
  have hempty : branch M A q (!b) = ∅ := by
    apply Finset.eq_empty_iff_forall_not_mem.mpr
    intro h hh
    have ⟨ha, hans⟩ := (mem_branch M A q (!b) h).mp hh
    rw [hanswer h ha] at hans
    cases b <;> simp at hans
  have hAne : A ≠ ∅ := Finset.nonempty_iff_ne_empty.mp hA
  cases b with
  | false =>
      have hmiss : branch M A q false ≠ ∅ := by rw [hbranch]; exact hAne
      have hhit : branch M A q true = ∅ := by simpa using hempty
      simp [restrict, hmiss, hhit, hbranch, hAne]
  | true =>
      have hhit : branch M A q true ≠ ∅ := by rw [hbranch]; exact hAne
      have hmiss : branch M A q false = ∅ := by simpa using hempty
      simp [restrict, hhit, hmiss, hbranch, hAne]

/-- Every common root answer saves one level from the height of the restricted
tree. The full prefix theorem composes this fact over `CommonPrefix`. -/
theorem height_restrict_common_root {M : QuerySystem H Q} {A : Finset H}
    (hA : A.Nonempty) (q : Q) (miss hit : Tree H Q)
    (b : Bool) (hanswer : ∀ h ∈ A, M.answer q h = b) :
    height (restrict M (.node q miss hit) A) ≤
      height (if b then hit else miss) := by
  rw [restrict_common_root hA q miss hit b hanswer]
  exact restriction_height_nonincrease M (if b then hit else miss) A

/-- Restricting a tree removes at least `n` levels when every member of the
live set shares its first `n` branch answers. -/
theorem height_restrict_commonPrefix {M : QuerySystem H Q} {A : Finset H}
    (hA : A.Nonempty) (T : Tree H Q) (n : Nat)
    (hp : CommonPrefix M A T n) :
    height (restrict M T A) + n ≤ height T := by
  induction n generalizing T with
  | zero => simpa using restriction_height_nonincrease M T A
  | succ n ih =>
      cases T with
      | leaf label => simp [CommonPrefix] at hp
      | node q miss hit =>
          simp only [CommonPrefix] at hp
          rcases hp with ⟨hfalse, hrest⟩ | ⟨htrue, hrest⟩
          · rw [restrict_common_root hA q miss hit false hfalse]
            have hchild := ih miss hrest
            have hmax := Nat.le_max_left (height miss) (height hit)
            simp [height]
            omega
          · rw [restrict_common_root hA q miss hit true htrue]
            have hchild := ih hit hrest
            have hmax := Nat.le_max_right (height miss) (height hit)
            simp [height]
            omega

end Tree
end PlanarQuery
