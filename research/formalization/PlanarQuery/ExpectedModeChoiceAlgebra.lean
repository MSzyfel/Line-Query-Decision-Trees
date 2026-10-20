import Mathlib

/-!
Local real-algebra for the expected-depth two-endpoint mode choice.

The article compares stopping after the middle-weight endpoint with querying
both endpoints.  This file isolates only the corresponding minimum and
maximum expressions; it does not formalize the probabilistic or coding
premises that lead to them.
-/

namespace PlanarQuery.ExpectedModeChoiceAlgebra

/-- The capped expected-depth contribution for an endpoint of weight `a`
opposite an endpoint of weight `z`. -/
noncomputable def EStar (p h a z : ℝ) : ℝ :=
  min (min ((h / p) * a) (h * (a + z))) ((h / p) * z)

/-- The better of stopping at the middle endpoint and taking the both-mode
route, with the latter evaluated at the larger endpoint weight `y`. -/
noncomputable def D (p h x y z : ℝ) : ℝ :=
  max y (x + y - z + EStar p h y z)

/-- Each candidate term in `EStar` is nondecreasing in its first endpoint
weight when `h` is nonnegative and `p` is positive.  Taking their minimum
preserves that order. -/
theorem estar_mono_left (p h x y z : ℝ) (hp : 0 < p) (hh : 0 ≤ h)
    (hxy : x ≤ y) :
    EStar p h x z ≤ EStar p h y z := by
  unfold EStar
  apply min_le_min
  · apply min_le_min
    · exact mul_le_mul_of_nonneg_left hxy (div_nonneg hh (le_of_lt hp))
    · exact mul_le_mul_of_nonneg_left (add_le_add_right hxy z) hh
  · exact le_rfl

/-- Evaluating the both-mode saving at the smaller endpoint cannot exceed
the comparison value `D`: monotonicity of `EStar` lets us replace `x` by
`y` in its final term. -/
theorem both_mode_saving_le_D (p h x y z : ℝ)
    (hp : 0 < p) (hh : 0 ≤ h) (hxy : x ≤ y) :
    x + y - z + EStar p h x z ≤ D p h x y z := by
  unfold D
  apply le_max_of_le_right
  have hE := estar_mono_left p h x y z hp hh hxy
  linarith

/-- The stop-mode saving, namely the middle weight, is one of the two
alternatives in `D`, and hence is bounded by their maximum. -/
theorem stop_saving_le_D (p h x y z : ℝ) :
    y ≤ D p h x y z := by
  unfold D
  exact le_max_left _ _

end PlanarQuery.ExpectedModeChoiceAlgebra
