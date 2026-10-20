import PlanarQuery.AveragePairPerturbation
import Mathlib.Tactic

/-! Construction-side floor estimate for the expected-depth reduction.

The manuscript defines each boundary correction by a floor quotient.  The
existing aggregate calibration theorem assumes a pointwise estimate; this
module derives that estimate directly from the construction's bounds on item
sizes, bin levels, and denominators, then invokes the aggregate theorem. -/

namespace PlanarQuery

/-- A floor correction whose numerator has the manuscript's form is bounded
by replacing its bin factor and item size by their global upper bounds and
its denominator by the global positive lower bound. -/
theorem average_boundary_floor_correction_le
    (V betaTop aMax r : ℕ)
    (beta a t : ℕ → ℕ)
    (i b : ℕ)
    (ha : a i ≤ aMax)
    (ht : r ≤ t i)
    (hr : 0 < r)
    :
    V * ((betaTop - beta b) * a i) / t i ≤
      (V * betaTop * aMax) / r := by
  have hnum : V * ((betaTop - beta b) * a i) ≤ V * betaTop * aMax := by
    have hfactor : (betaTop - beta b) * a i ≤ betaTop * aMax := by
      have hsub : betaTop - beta b ≤ betaTop := Nat.sub_le _ _
      exact Nat.mul_le_mul hsub ha
    simpa [Nat.mul_assoc] using Nat.mul_le_mul_left V hfactor
  have hquotient_mul :
      (V * ((betaTop - beta b) * a i) / t i) * t i ≤
        V * ((betaTop - beta b) * a i) := Nat.div_mul_le_self _ _
  have hquotient_mul_le :
      (V * ((betaTop - beta b) * a i) / t i) * r ≤
        V * betaTop * aMax := by
    calc
      (V * ((betaTop - beta b) * a i) / t i) * r ≤
          (V * ((betaTop - beta b) * a i) / t i) * t i :=
            Nat.mul_le_mul_left _ ht
      _ ≤ V * ((betaTop - beta b) * a i) := hquotient_mul
      _ ≤ V * betaTop * aMax := hnum
  exact (Nat.le_div_iff_mul_le hr).2 hquotient_mul_le

/-- The manuscript's E+ scale estimate now follows from the actual floor
formula, provided the displayed integer calibration inequality holds.

Assumptions are exactly the construction bounds needed here: every bin level
is at most `betaTop`, every item size is at most `aMax`, every denominator is
at least the positive integer `r`, and the calibration scale dominates the
resulting aggregate coefficient. -/
theorem average_boundary_Eplus_lt_scale
    (m p q V betaTop aMax r : ℕ)
    (beta a t : ℕ → ℕ)
    (hm : 0 < m) (hV : 0 < V) (hC : 0 < betaTop * aMax)
    (ha : ∀ i < m, a i ≤ aMax)
    (ht : ∀ i < m, r ≤ t i)
    (hr : 0 < r)
    (hscale : 1000 * (q * m * p + 2 * m + 1) * (betaTop * aMax) < r) :
    1000 * expectedDepthEplus m p q
      (fun i b => V * ((betaTop - beta b) * a i) / t i) < V := by
  apply expected_depth_Eplus_lt_scale m p q V (betaTop * aMax) r
  · exact hm
  · exact hV
  · exact hC
  · intro i hi b hb
    simpa [Nat.mul_assoc] using
      average_boundary_floor_correction_le V betaTop aMax r beta a t
        i b (ha i hi) (ht i hi) hr
  · simpa [Nat.mul_assoc] using hscale

end PlanarQuery
