import Mathlib.Algebra.Order.Floor.Ring
import Mathlib.Data.Real.Basic
import Mathlib.Data.Real.Archimedean
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.NormNum
import Mathlib.Tactic.Ring
import Lean.Elab.Tactic.Omega

namespace PlanarQuery

theorem floor_difference (x y : ℝ) :
    Int.floor (x - y) ≤ Int.floor x - Int.floor y := by
  have h := Int.le_floor_add (x - y) y
  simp only [sub_add_cancel] at h
  omega

/-- All numerical choices in the flat-state height argument reduce to
    three transparent requirements on the count-potential coefficient. -/
theorem flat_count_credit (γ x capLog : ℝ)
    (hγ : 1 ≤ γ) (hx : capLog < x) (hcredit : 5 < γ * capLog) :
    5 + Int.floor (x - capLog) ≤ Int.floor (γ * x) := by
  have hmul := mul_nonneg (sub_nonneg.mpr hγ) (sub_nonneg.mpr hx.le)
  have hreal : 5 + (x - capLog) ≤ γ * x := by nlinarith
  have hfloor := Int.floor_mono hreal
  simpa only [Int.floor_ofNat_add] using hfloor

theorem balanced_count_credit (γ x y : ℝ)
    (hgap : 1 ≤ γ * (x - y)) :
    1 ≤ Int.floor (γ * x) - Int.floor (γ * y) := by
  have hf := Int.floor_mono hgap
  norm_num at hf
  have hd := floor_difference (γ * x) (γ * y)
  have heq : γ * x - γ * y = γ * (x - y) := by ring
  rw [heq] at hd
  omega

/-- The smaller global slot cap used by the retained polynomial algorithm:
    beyond this threshold the priority fallback is already sufficient. -/
theorem slot_cap_fallback (γ q D : ℝ) (hγ : 1 < γ)
    (hD : γ * q / (γ - 1) < D) :
    3 * D + γ * q < (2 + γ) * D := by
  have hden : 0 < γ - 1 := by linarith
  have h := (div_lt_iff₀ hden).mp hD
  nlinarith

end PlanarQuery
