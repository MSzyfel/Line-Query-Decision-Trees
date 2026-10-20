import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith

namespace PlanarQuery

/-! Cancellation inside exact lookahead. Prefixes and frontier costs are
    explicit quantities. A later theorem connects them to an actual tree. -/

/-- A surviving branch has spent k levels and has optimal height at most
    D-k. Its additive baseline penalty is removed by those k levels. -/
theorem lookahead_height (a D k penalty : ℝ)
    (hpenalty : penalty ≤ (a - 1) * k) :
    k + a * (D - k) + penalty ≤ a * D := by
  nlinarith

/-- The expected-depth argument uses total surviving mass, never minimum
    prior probability or the height of an expected-depth-optimal tree. -/
theorem lookahead_expected (a prefixCost remainder frontierMass k penalty : ℝ)
    (ha : 1 ≤ a) (hM : 0 ≤ frontierMass)
    (hprefixCost : k * frontierMass ≤ prefixCost)
    (hpenalty : penalty ≤ (a - 1) * k) :
    prefixCost + a * remainder + penalty * frontierMass ≤
      a * (prefixCost + remainder) := by
  have h1 := mul_le_mul_of_nonneg_left hprefixCost (sub_nonneg.mpr ha)
  have h2 := mul_le_mul_of_nonneg_right hpenalty hM
  nlinarith

theorem exact_choice_inherits {α : Type*} (score : α → ℝ) (chosen compare : α)
    (hmin : ∀ candidate, score chosen ≤ score candidate)
    (factor optimum : ℝ) (hcompare : score compare ≤ factor * optimum) :
    score chosen ≤ factor * optimum :=
  le_trans (hmin compare) hcompare

end PlanarQuery
