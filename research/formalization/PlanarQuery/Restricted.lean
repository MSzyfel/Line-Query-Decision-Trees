import Mathlib.Data.Real.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.Ring

namespace PlanarQuery

/-! Arithmetic in the shallow-cap PTAS. The geometric isolation and
    count-vector algorithm are not silently assumptions of a full PTAS:
    these are explicitly the numerical combination lemmas. -/

theorem capped_spine_lower_bound {N b : ℝ}
    (rankCost optimum : ℝ)
    (hgroup : N * (N + 1) / (2 * b) ≤ rankCost)
    (hcost : rankCost ≤ optimum) :
    N * (N + 1) / (2 * b) ≤ optimum := le_trans hgroup hcost

/-- Combining the actual gap-clearing overhead with a residual optimum
    gives the PTAS factor in the manuscript. -/
theorem shallow_cap_ratio (N b blockLength ε removed prefixCost residual optimum : ℝ)
    (hN : 0 ≤ N) (hb : 0 < b) (hL : 0 < blockLength)
    (hr : removed ≤ 2 * b * N / blockLength)
    (hp : prefixCost ≤ 2 * removed * (N + 1))
    (hres : residual ≤ optimum)
    (hopt : N * (N + 1) / (2 * b) ≤ optimum)
    (hscale : 8 * b ^ 2 ≤ ε * blockLength) :
    prefixCost + residual ≤ (1 + ε) * optimum := by
  have hden : 0 < 2 * b := by positivity
  have hprefixCost : prefixCost ≤ 4 * b * N * (N + 1) / blockLength := by
    calc
      prefixCost ≤ 2 * removed * (N + 1) := hp
      _ ≤ 2 * (2 * b * N / blockLength) * (N + 1) := by
        exact mul_le_mul_of_nonneg_right
          (mul_le_mul_of_nonneg_left hr (by norm_num)) (by positivity)
      _ = 4 * b * N * (N + 1) / blockLength := by ring
  have hopt' : N * (N + 1) ≤ optimum * (2 * b) :=
    (div_le_iff₀ hden).mp hopt
  have hprefixCost' : prefixCost * blockLength ≤ 4 * b * N * (N + 1) :=
    (le_div_iff₀ hL).mp hprefixCost
  have hopt_nonneg : 0 ≤ optimum := by
    have : 0 ≤ N * (N + 1) / (2 * b) := by positivity
    linarith
  have h1 := mul_le_mul_of_nonneg_left hopt' (by positivity : 0 ≤ 4 * b)
  have h2 := mul_le_mul_of_nonneg_right hscale hopt_nonneg
  have : prefixCost ≤ ε * optimum := by
    apply (mul_le_mul_right hL).mp
    nlinarith
  nlinarith

end PlanarQuery
