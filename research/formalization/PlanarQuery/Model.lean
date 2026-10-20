import Mathlib.Data.Finset.Card
import Mathlib.Algebra.BigOperators.Group.Finset.Basic
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Rat.Defs
import Mathlib.Data.Rat.Cast.Order
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

/-! A finite *supplied-query* model. No theorem in this file assumes that
    an arbitrary partition can be queried. A node contains an element of Q.
    Raw expected costs use the original rational hypothesis weights. -/

namespace PlanarQuery

structure QuerySystem (H Q : Type*) where
  answer : Q → H → Bool

inductive Tree (H Q : Type*) where
  | leaf (h : H)
  | node (q : Q) (miss hit : Tree H Q)
  deriving DecidableEq

namespace Tree

variable {H Q : Type*}

def eval (M : QuerySystem H Q) : Tree H Q → H → H
  | .leaf label, _ => label
  | .node q miss hit, h =>
      if M.answer q h then eval M hit h else eval M miss h

def depth (M : QuerySystem H Q) : Tree H Q → H → ℕ
  | .leaf _, _ => 0
  | .node q miss hit, h =>
      1 + if M.answer q h then depth M hit h else depth M miss h

def height : Tree H Q → ℕ
  | .leaf _ => 0
  | .node _ miss hit => 1 + max (height miss) (height hit)

def Identifies (M : QuerySystem H Q) (S : Finset H) (T : Tree H Q) : Prop :=
  ∀ h ∈ S, eval M T h = h

def branch [DecidableEq H] (M : QuerySystem H Q)
    (S : Finset H) (q : Q) (b : Bool) : Finset H :=
  S.filter (fun h => M.answer q h = b)

@[simp] theorem mem_branch [DecidableEq H] (M : QuerySystem H Q)
    (S : Finset H) (q : Q) (b : Bool) (h : H) :
    h ∈ branch M S q b ↔ h ∈ S ∧ M.answer q h = b := by
  simp [branch]

theorem branches_disjoint [DecidableEq H] (M : QuerySystem H Q)
    (S : Finset H) (q : Q) :
    Disjoint (branch M S q false) (branch M S q true) := by
  rw [Finset.disjoint_left]
  intro h hm hh
  simp only [mem_branch] at hm hh
  rw [hm.2] at hh
  cases hh.2

theorem branches_union [DecidableEq H] (M : QuerySystem H Q)
    (S : Finset H) (q : Q) :
    branch M S q false ∪ branch M S q true = S := by
  ext h
  cases hq : M.answer q h <;> simp [hq]

theorem depth_le_height (M : QuerySystem H Q) (T : Tree H Q) (h : H) :
    depth M T h ≤ height T := by
  induction T with
  | leaf label => simp [depth, height]
  | node q miss hit ihm ihh =>
    cases hq : M.answer q h
    · simpa [depth, height, hq] using
        Nat.add_le_add_left (le_trans ihm (Nat.le_max_left _ _)) 1
    · simpa [depth, height, hq] using
        Nat.add_le_add_left (le_trans ihh (Nat.le_max_right _ _)) 1

def leaves [DecidableEq H] : Tree H Q → Finset H
  | .leaf h => {h}
  | .node _ miss hit => leaves miss ∪ leaves hit

theorem eval_mem_leaves [DecidableEq H] (M : QuerySystem H Q)
    (T : Tree H Q) (h : H) : eval M T h ∈ leaves T := by
  induction T with
  | leaf label => simp [eval, leaves]
  | node q miss hit ihm ihh =>
    cases hq : M.answer q h <;> simp [eval, leaves, hq, ihm, ihh]

theorem leaf_capacity [DecidableEq H] (T : Tree H Q) :
    (leaves T).card ≤ 2 ^ height T := by
  induction T with
  | leaf h => simp [leaves, height]
  | node q miss hit ihm ihh =>
    calc
      (leaves (.node q miss hit)).card
          ≤ (leaves miss).card + (leaves hit).card := Finset.card_union_le _ _
      _ ≤ 2 ^ height miss + 2 ^ height hit := Nat.add_le_add ihm ihh
      _ ≤ 2 ^ max (height miss) (height hit) +
          2 ^ max (height miss) (height hit) := by
        exact Nat.add_le_add
          (Nat.pow_le_pow_right (by omega) (Nat.le_max_left _ _))
          (Nat.pow_le_pow_right (by omega) (Nat.le_max_right _ _))
      _ = 2 ^ height (.node q miss hit) := by
        simp [height, Nat.add_comm 1, pow_succ, Nat.mul_two]

theorem identification_capacity [DecidableEq H] (M : QuerySystem H Q)
    (S : Finset H) (T : Tree H Q) (hId : Identifies M S T) :
    S.card ≤ 2 ^ height T := by
  have hsub : S ⊆ leaves T := by
    intro h hh
    have he := eval_mem_leaves M T h
    rw [hId h hh] at he
    exact he
  exact le_trans (Finset.card_le_card hsub) (leaf_capacity T)

def mass [DecidableEq H] (weight : H → ℚ) (S : Finset H) : ℚ :=
  ∑ h ∈ S, weight h

def rawExpected [DecidableEq H] (M : QuerySystem H Q) (weight : H → ℚ)
    (S : Finset H) (T : Tree H Q) : ℚ :=
  ∑ h ∈ S, weight h * depth M T h

theorem rawExpected_nonneg [DecidableEq H] (M : QuerySystem H Q)
    (weight : H → ℚ) (hw : ∀ h, 0 ≤ weight h)
    (S : Finset H) (T : Tree H Q) :
    0 ≤ rawExpected M weight S T := by
  apply Finset.sum_nonneg
  intro h hh
  exact mul_nonneg (hw h) (Nat.cast_nonneg _)

theorem rawExpected_leaf [DecidableEq H] (M : QuerySystem H Q)
    (weight : H → ℚ) (S : Finset H) (label : H) :
    rawExpected M weight S (.leaf label) = 0 := by
  simp [rawExpected, depth]

theorem rawExpected_node [DecidableEq H] (M : QuerySystem H Q)
    (weight : H → ℚ) (S : Finset H) (q : Q) (miss hit : Tree H Q) :
    rawExpected M weight S (.node q miss hit) =
      mass weight S + rawExpected M weight (branch M S q false) miss +
      rawExpected M weight (branch M S q true) hit := by
  classical
  unfold rawExpected mass branch
  rw [Finset.sum_filter, Finset.sum_filter]
  rw [← Finset.sum_add_distrib, ← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro h hh
  cases hq : M.answer q h <;> simp [depth, hq, Nat.cast_add] <;> ring

theorem rawExpected_mono_depth [DecidableEq H] (M : QuerySystem H Q)
    (weight : H → ℚ) (hw : ∀ h, 0 ≤ weight h)
    (S : Finset H) (T U : Tree H Q)
    (hdepth : ∀ h ∈ S, depth M T h ≤ depth M U h) :
    rawExpected M weight S T ≤ rawExpected M weight S U := by
  apply Finset.sum_le_sum
  intro h hh
  exact mul_le_mul_of_nonneg_left (Nat.cast_le.mpr (hdepth h hh)) (hw h)

/-- Restrict a tree and contract each query whose answer is constant on
    the live set. All retained nodes still use supplied queries. -/
def restrict [DecidableEq H] (M : QuerySystem H Q) :
    Tree H Q → Finset H → Tree H Q
  | .leaf h, _ => .leaf h
  | .node q miss hit, S =>
    if branch M S q false = ∅ then restrict M hit (branch M S q true)
    else if branch M S q true = ∅ then restrict M miss (branch M S q false)
    else .node q (restrict M miss (branch M S q false))
      (restrict M hit (branch M S q true))

theorem restriction_preserves [DecidableEq H] (M : QuerySystem H Q)
    (T : Tree H Q) (S : Finset H) (h : H) (hh : h ∈ S) :
    eval M (restrict M T S) h = eval M T h ∧
    depth M (restrict M T S) h ≤ depth M T h := by
  induction T generalizing S with
  | leaf label => simp [restrict, eval, depth]
  | node q miss hit ihm ihh =>
    cases hq : M.answer q h
    · have hm : h ∈ branch M S q false := by simp [hh, hq]
      have hne : branch M S q false ≠ ∅ := Finset.nonempty_iff_ne_empty.mp ⟨h, hm⟩
      have ih := ihm (branch M S q false) hm
      by_cases he : branch M S q true = ∅
      · simp only [restrict, hne, he, if_false, if_true, eval, depth, hq,
          Bool.false_eq_true] 
        exact ⟨ih.1, by omega⟩
      · simp only [restrict, hne, he, if_false, eval, depth, hq,
          Bool.false_eq_true]
        exact ⟨ih.1, Nat.add_le_add_left ih.2 1⟩
    · have hm : h ∈ branch M S q true := by simp [hh, hq]
      have hne : branch M S q true ≠ ∅ := Finset.nonempty_iff_ne_empty.mp ⟨h, hm⟩
      have ih := ihh (branch M S q true) hm
      by_cases he : branch M S q false = ∅
      · simp only [restrict, he, if_true, eval, depth, hq]
        exact ⟨ih.1, by omega⟩
      · simp only [restrict, he, hne, if_false, eval, depth, hq]
        exact ⟨ih.1, Nat.add_le_add_left ih.2 1⟩

theorem restriction_identifies [DecidableEq H] (M : QuerySystem H Q)
    (T : Tree H Q) (S U : Finset H) (hsub : U ⊆ S)
    (hId : Identifies M S T) : Identifies M U (restrict M T U) := by
  intro h hh
  rw [(restriction_preserves M T U h hh).1]
  exact hId h (hsub hh)

theorem restriction_expected_nonincrease [DecidableEq H] (M : QuerySystem H Q)
    (weight : H → ℚ) (hw : ∀ h, 0 ≤ weight h) (S : Finset H)
    (T : Tree H Q) :
    rawExpected M weight S (restrict M T S) ≤ rawExpected M weight S T := by
  apply rawExpected_mono_depth M weight hw
  intro h hh
  exact (restriction_preserves M T S h hh).2

theorem restriction_height_nonincrease [DecidableEq H] (M : QuerySystem H Q)
    (T : Tree H Q) (S : Finset H) :
    height (restrict M T S) ≤ height T := by
  induction T generalizing S with
  | leaf label => simp [restrict, height]
  | node q miss hit ihm ihh =>
    simp only [restrict]
    split_ifs with hm hh
    · exact le_trans (ihh _) (by simp [height]; omega)
    · exact le_trans (ihm _) (by simp [height]; omega)
    · simp only [height]
      exact Nat.add_le_add_left (max_le_max (ihm _) (ihh _)) 1

end Tree

/-! The geometric data are exact rationals. Geometry is not erased into
    an oracle: the supplied-query matrix is computed by its signed lines.
    Proving the paper's hull and interval assertions remains a separate
    obligation, recorded in CLAIMS.md. -/

structure RationalLine where
  a : ℚ
  b : ℚ
  c : ℚ
  nonzero : a ≠ 0 ∨ b ≠ 0

structure PlanarInstance (n m : ℕ) where
  point : Fin n → ℚ × ℚ
  line : Fin m → RationalLine
  offLine : ∀ q h,
    (line q).a * (point h).1 + (line q).b * (point h).2 ≠ (line q).c
  weight : Fin n → ℚ
  positive : ∀ h, 0 < weight h

def PlanarInstance.querySystem {n m : ℕ} (I : PlanarInstance n m) :
    QuerySystem (Fin n) (Fin m) where
  answer q h := decide
    ((I.line q).c < (I.line q).a * (I.point h).1 +
      (I.line q).b * (I.point h).2)

theorem PlanarInstance.query_semantics {n m : ℕ} (I : PlanarInstance n m)
    (q : Fin m) (h : Fin n) :
    I.querySystem.answer q h = true ↔
      (I.line q).c < (I.line q).a * (I.point h).1 +
        (I.line q).b * (I.point h).2 := by
  simp [PlanarInstance.querySystem]

end PlanarQuery
