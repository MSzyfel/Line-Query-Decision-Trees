import PlanarQuery.LiveHeight
import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

/-! Executable two-bit simulation of on-line (ternary) answers. Both
directions use the original supplied query identifiers. The return
simulation does not even require caching to meet the depth bound. -/

namespace PlanarQuery

inductive SignAnswer | negative | zero | positive
  deriving DecidableEq

structure TernarySystem (H Q : Type*) where
  answer : Q → H → SignAnswer

inductive TernaryTree (H Q : Type*)
  | leaf (h : H)
  | node (q : Q) (negative zero positive : TernaryTree H Q)

namespace TernaryTree
variable {H Q : Type*}

def eval (M : TernarySystem H Q) : TernaryTree H Q → H → H
  | .leaf label, _ => label
  | .node q neg zero pos, h => match M.answer q h with
    | .negative => eval M neg h
    | .zero => eval M zero h
    | .positive => eval M pos h

def depth (M : TernarySystem H Q) : TernaryTree H Q → H → ℕ
  | .leaf _, _ => 0
  | .node q neg zero pos, h => 1 + match M.answer q h with
    | .negative => depth M neg h
    | .zero => depth M zero h
    | .positive => depth M pos h

def Identifies (M : TernarySystem H Q) (S : Finset H) (T : TernaryTree H Q) :=
  ∀ h ∈ S, eval M T h = h

def rawExpected (M : TernarySystem H Q) (w : H → ℚ)
    (S : Finset H) (T : TernaryTree H Q) : ℚ := ∑ h ∈ S, w h * depth M T h

def liveHeight (M : TernarySystem H Q) (S : Finset H) (T : TernaryTree H Q) :=
  S.sup (depth M T)

/-- False selects the strictly-negative bit, true the nonpositive bit. -/
def virtualSystem (M : TernarySystem H Q) : QuerySystem H (Q × Bool) where
  answer qb h := match M.answer qb.1 h with
    | .negative => true
    | .zero => qb.2
    | .positive => false

def toBinary : TernaryTree H Q → Tree H (Q × Bool)
  | .leaf h => .leaf h
  | .node q neg zero pos =>
      .node (q, false) (.node (q, true) (toBinary pos) (toBinary zero)) (toBinary neg)

/-- Each virtual request is implemented by one original supplied query. -/
def fromBinary : Tree H (Q × Bool) → TernaryTree H Q
  | .leaf h => .leaf h
  | .node (q, false) miss hit => .node q (fromBinary hit) (fromBinary miss) (fromBinary miss)
  | .node (q, true) miss hit => .node q (fromBinary hit) (fromBinary hit) (fromBinary miss)

theorem toBinary_eval (M : TernarySystem H Q) (T : TernaryTree H Q) (h : H) :
    Tree.eval (virtualSystem M) (toBinary T) h = eval M T h := by
  induction T with
  | leaf label => rfl
  | node q neg zero pos ihn ihz ihp =>
    simp only [virtualSystem] at ihn ihz ihp
    cases hs : M.answer q h <;>
      simp [toBinary, Tree.eval, virtualSystem, eval, hs, ihn, ihz, ihp]

theorem toBinary_depth (M : TernarySystem H Q) (T : TernaryTree H Q) (h : H) :
    Tree.depth (virtualSystem M) (toBinary T) h ≤ 2 * depth M T h := by
  induction T with
  | leaf label => simp [toBinary, Tree.depth, depth]
  | node q neg zero pos ihn ihz ihp =>
    simp only [virtualSystem] at ihn ihz ihp
    cases hs : M.answer q h <;>
      simp [toBinary, Tree.depth, virtualSystem, depth, hs] <;> omega

theorem fromBinary_eval (M : TernarySystem H Q) (T : Tree H (Q × Bool)) (h : H) :
    eval M (fromBinary T) h = Tree.eval (virtualSystem M) T h := by
  induction T with
  | leaf label => rfl
  | node qb miss hit ihm ihh =>
    rcases qb with ⟨q, b⟩
    cases b <;> cases hs : M.answer q h <;>
      simp [fromBinary, eval, Tree.eval, virtualSystem, hs, ihm, ihh]

theorem fromBinary_depth (M : TernarySystem H Q) (T : Tree H (Q × Bool)) (h : H) :
    depth M (fromBinary T) h = Tree.depth (virtualSystem M) T h := by
  induction T with
  | leaf label => rfl
  | node qb miss hit ihm ihh =>
    rcases qb with ⟨q, b⟩
    cases b <;> cases hs : M.answer q h <;>
      simp [fromBinary, depth, Tree.depth, virtualSystem, hs, ihm, ihh]

variable [DecidableEq H]

omit [DecidableEq H] in
theorem toBinary_identifies (M : TernarySystem H Q) (S : Finset H)
    (T : TernaryTree H Q) (hT : Identifies M S T) :
    Tree.Identifies (virtualSystem M) S (toBinary T) := by
  intro h hh
  rw [toBinary_eval]
  exact hT h hh

omit [DecidableEq H] in
theorem fromBinary_identifies (M : TernarySystem H Q) (S : Finset H)
    (T : Tree H (Q × Bool)) (hT : Tree.Identifies (virtualSystem M) S T) :
    Identifies M S (fromBinary T) := by
  intro h hh
  rw [fromBinary_eval]
  exact hT h hh

theorem toBinary_expected (M : TernarySystem H Q) (S : Finset H)
    (w : H → ℚ) (hw : ∀ h ∈ S, 0 ≤ w h) (T : TernaryTree H Q) :
    Tree.rawExpected (virtualSystem M) w S (toBinary T) ≤ 2 * rawExpected M w S T := by
  unfold Tree.rawExpected rawExpected
  rw [Finset.mul_sum]
  apply Finset.sum_le_sum
  intro h hh
  have hd : (Tree.depth (virtualSystem M) (toBinary T) h : ℚ) ≤ 2 * depth M T h := by
    exact_mod_cast toBinary_depth M T h
  nlinarith [mul_le_mul_of_nonneg_left hd (hw h hh)]

theorem fromBinary_expected (M : TernarySystem H Q) (S : Finset H)
    (w : H → ℚ) (T : Tree H (Q × Bool)) :
    rawExpected M w S (fromBinary T) = Tree.rawExpected (virtualSystem M) w S T := by
  simp [rawExpected, Tree.rawExpected, fromBinary_depth]

omit [DecidableEq H] in
theorem toBinary_liveHeight (M : TernarySystem H Q) (S : Finset H)
    (T : TernaryTree H Q) :
    Tree.liveHeight (virtualSystem M) S (toBinary T) ≤ 2 * liveHeight M S T := by
  apply Finset.sup_le
  intro h hh
  exact (toBinary_depth M T h).trans (Nat.mul_le_mul_left 2 (Finset.le_sup hh))

omit [DecidableEq H] in
theorem fromBinary_liveHeight (M : TernarySystem H Q) (S : Finset H)
    (T : Tree H (Q × Bool)) :
    liveHeight M S (fromBinary T) = Tree.liveHeight (virtualSystem M) S T := by
  unfold liveHeight Tree.liveHeight
  congr 1
  funext h
  exact fromBinary_depth M T h

/-- The expected-cost approximation transfer compares with every
original identifying competitor, rather than an assumed optimum value. -/
theorem expected_approximation_transfer (M : TernarySystem H Q) (S : Finset H)
    (w : H → ℚ) (hw : ∀ h ∈ S, 0 ≤ w h) (alpha : ℚ) (ha : 0 ≤ alpha)
    (A : Tree H (Q × Bool)) (hA : Tree.Identifies (virtualSystem M) S A)
    (happrox : ∀ U, Tree.Identifies (virtualSystem M) S U →
      Tree.rawExpected (virtualSystem M) w S A ≤
        alpha * Tree.rawExpected (virtualSystem M) w S U) :
    Identifies M S (fromBinary A) ∧ ∀ T, Identifies M S T →
      rawExpected M w S (fromBinary A) ≤ (2 * alpha) * rawExpected M w S T := by
  refine ⟨fromBinary_identifies M S A hA, ?_⟩
  intro T hT
  rw [fromBinary_expected]
  calc
    Tree.rawExpected (virtualSystem M) w S A
        ≤ alpha * Tree.rawExpected (virtualSystem M) w S (toBinary T) :=
      happrox _ (toBinary_identifies M S T hT)
    _ ≤ alpha * (2 * rawExpected M w S T) :=
      mul_le_mul_of_nonneg_left (toBinary_expected M S w hw T) ha
    _ = (2 * alpha) * rawExpected M w S T := by ring

omit [DecidableEq H] in
/-- The same transfer for maximum live depth, using the pointwise
simulation rather than the height of unreachable branches. -/
theorem height_approximation_transfer (M : TernarySystem H Q) (S : Finset H)
    (alpha : ℚ) (ha : 0 ≤ alpha) (A : Tree H (Q × Bool))
    (hA : Tree.Identifies (virtualSystem M) S A)
    (happrox : ∀ U, Tree.Identifies (virtualSystem M) S U →
      (Tree.liveHeight (virtualSystem M) S A : ℚ) ≤
        alpha * Tree.liveHeight (virtualSystem M) S U) :
    Identifies M S (fromBinary A) ∧ ∀ T, Identifies M S T →
      (liveHeight M S (fromBinary A) : ℚ) ≤ (2 * alpha) * liveHeight M S T := by
  refine ⟨fromBinary_identifies M S A hA, ?_⟩
  intro T hT
  rw [fromBinary_liveHeight]
  have hb : (Tree.liveHeight (virtualSystem M) S (toBinary T) : ℚ) ≤
      2 * liveHeight M S T := by exact_mod_cast toBinary_liveHeight M S T
  calc
    (Tree.liveHeight (virtualSystem M) S A : ℚ)
        ≤ alpha * Tree.liveHeight (virtualSystem M) S (toBinary T) :=
      happrox _ (toBinary_identifies M S T hT)
    _ ≤ alpha * (2 * liveHeight M S T) := mul_le_mul_of_nonneg_left hb ha
    _ = (2 * alpha) * liveHeight M S T := by ring

/-- The expected-cost transfer also permits arbitrary real approximation
coefficients; only the underlying input weights need be rational. -/
theorem expected_real_approximation_transfer (M : TernarySystem H Q) (S : Finset H)
    (w : H → ℚ) (hw : ∀ h ∈ S, 0 ≤ w h) (alpha : ℝ) (ha : 0 ≤ alpha)
    (A : Tree H (Q × Bool)) (hA : Tree.Identifies (virtualSystem M) S A)
    (happrox : ∀ U, Tree.Identifies (virtualSystem M) S U →
      (Tree.rawExpected (virtualSystem M) w S A : ℝ) ≤
        alpha * (Tree.rawExpected (virtualSystem M) w S U : ℝ)) :
    Identifies M S (fromBinary A) ∧ ∀ T, Identifies M S T →
      (rawExpected M w S (fromBinary A) : ℝ) ≤
        (2 * alpha) * (rawExpected M w S T : ℝ) := by
  refine ⟨fromBinary_identifies M S A hA, ?_⟩
  intro T hT
  rw [fromBinary_expected]
  have hb : (Tree.rawExpected (virtualSystem M) w S (toBinary T) : ℝ) ≤
      2 * (rawExpected M w S T : ℝ) := by
    exact_mod_cast toBinary_expected M S w hw T
  calc
    (Tree.rawExpected (virtualSystem M) w S A : ℝ)
        ≤ alpha * (Tree.rawExpected (virtualSystem M) w S (toBinary T) : ℝ) :=
      happrox _ (toBinary_identifies M S T hT)
    _ ≤ alpha * (2 * (rawExpected M w S T : ℝ)) :=
      mul_le_mul_of_nonneg_left hb ha
    _ = (2 * alpha) * (rawExpected M w S T : ℝ) := by ring

omit [DecidableEq H] in
/-- Arbitrary real approximation coefficients are valid for the maximum
live-depth transfer as well. -/
theorem height_real_approximation_transfer (M : TernarySystem H Q) (S : Finset H)
    (alpha : ℝ) (ha : 0 ≤ alpha) (A : Tree H (Q × Bool))
    (hA : Tree.Identifies (virtualSystem M) S A)
    (happrox : ∀ U, Tree.Identifies (virtualSystem M) S U →
      (Tree.liveHeight (virtualSystem M) S A : ℝ) ≤
        alpha * (Tree.liveHeight (virtualSystem M) S U : ℝ)) :
    Identifies M S (fromBinary A) ∧ ∀ T, Identifies M S T →
      (liveHeight M S (fromBinary A) : ℝ) ≤
        (2 * alpha) * (liveHeight M S T : ℝ) := by
  refine ⟨fromBinary_identifies M S A hA, ?_⟩
  intro T hT
  rw [fromBinary_liveHeight]
  have hb : (Tree.liveHeight (virtualSystem M) S (toBinary T) : ℝ) ≤
      2 * (liveHeight M S T : ℝ) := by
    exact_mod_cast toBinary_liveHeight M S T
  calc
    (Tree.liveHeight (virtualSystem M) S A : ℝ)
        ≤ alpha * (Tree.liveHeight (virtualSystem M) S (toBinary T) : ℝ) :=
      happrox _ (toBinary_identifies M S T hT)
    _ ≤ alpha * (2 * (liveHeight M S T : ℝ)) :=
      mul_le_mul_of_nonneg_left hb ha
    _ = (2 * alpha) * (liveHeight M S T : ℝ) := by ring

end TernaryTree
end PlanarQuery
