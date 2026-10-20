import Mathlib
import PlanarQuery.Entropy
import PlanarQuery.ExpectedModeChoiceAlgebra

/-!
The entropy-tent estimate used when two positive transcript cells are merged.
Concavity supplies a chord bound on each of the three intervals separated by
`p` and `1-p`; the weighted information bound then follows by rescaling the
conditional binary entropy of the merged cells.
-/

namespace PlanarQuery.ExpectedCoarsening

private theorem entropy_left_arm (p h v : ℝ)
    (hp0 : 0 < p) (hpHalf : p < 1 / 2)
    (hhCal : Real.log 2 * h <= Real.binEntropy p)
    (hv0 : 0 <= v) (hvp : v <= p) :
    Real.log 2 * ((h / p) * v) <= Real.binEntropy v := by
  have hp1 : p <= 1 := by linarith
  have hzero : Real.binEntropy 0 = 0 := by simp [Real.binEntropy]
  have hconc : ConcaveOn ℝ (Set.Icc (0 : ℝ) 1) Real.binEntropy :=
    Real.strictConcave_binEntropy.concaveOn
  have hpSet : p ∈ Set.Icc (0 : ℝ) 1 := by
    constructor
    · exact le_of_lt hp0
    · exact hp1
  have hzeroSet : (0 : ℝ) ∈ Set.Icc 0 1 := by norm_num
  have hweight : 0 <= v / p := div_nonneg hv0 (le_of_lt hp0)
  have hweightLe : v / p <= 1 := (div_le_one hp0).2 hvp
  have hremain : 0 <= 1 - v / p := sub_nonneg.mpr hweightLe
  have hsum : (1 - v / p) + (v / p) = 1 := by ring
  have hcomb : (1 - v / p) * 0 + (v / p) * p = v := by
    field_simp [ne_of_gt hp0]
  have hchord := hconc.2 hzeroSet hpSet hremain hweight hsum
  have hchord' :
      (1 - v / p) * Real.binEntropy 0 + (v / p) * Real.binEntropy p <=
        Real.binEntropy ((1 - v / p) * 0 + (v / p) * p) := by
    simpa only [smul_eq_mul] using hchord
  rw [hzero, hcomb] at hchord'
  have hraw : (v / p) * Real.binEntropy p <= Real.binEntropy v := by
    simpa using hchord'
  have hscale : Real.log 2 * ((h / p) * v) = (v / p) * (Real.log 2 * h) := by
    field_simp [ne_of_gt hp0]
    ring
  rw [hscale]
  exact (mul_le_mul_of_nonneg_left hhCal hweight).trans hraw

private theorem entropy_middle_plateau (p h v : ℝ)
    (hp0 : 0 < p) (hpHalf : p < 1 / 2)
    (hhCal : Real.log 2 * h <= Real.binEntropy p)
    (hvp : p <= v) (hvUpper : v <= 1 - p) :
    Real.log 2 * h <= Real.binEntropy v := by
  have hconc : ConcaveOn ℝ (Set.Icc (0 : ℝ) 1) Real.binEntropy :=
    Real.strictConcave_binEntropy.concaveOn
  have hp1 : p <= 1 := by linarith
  have hright0 : 0 <= 1 - p := by linarith
  have hright1 : 1 - p <= 1 := by linarith
  have hpSet : p ∈ Set.Icc (0 : ℝ) 1 := by
    constructor
    · exact le_of_lt hp0
    · exact hp1
  have hrightSet : 1 - p ∈ Set.Icc (0 : ℝ) 1 := by
    constructor
    · exact hright0
    · exact hright1
  have hden : 0 < (1 - p) - p := by linarith
  let alpha : Real := ((1 - p) - v) / ((1 - p) - p)
  let beta : Real := (v - p) / ((1 - p) - p)
  have halpha : 0 <= alpha := by
    dsimp [alpha]
    exact div_nonneg (sub_nonneg.mpr hvUpper) (le_of_lt hden)
  have hbeta : 0 <= beta := by
    dsimp [beta]
    exact div_nonneg (sub_nonneg.mpr hvp) (le_of_lt hden)
  have hsum : alpha + beta = 1 := by
    dsimp [alpha, beta]
    field_simp [ne_of_gt hden]
  have hcomb : alpha * p + beta * (1 - p) = v := by
    dsimp [alpha, beta]
    field_simp [ne_of_gt hden]
    ring
  have hc := hconc.2 hpSet hrightSet halpha hbeta hsum
  have hc' : alpha * Real.binEntropy p + beta * Real.binEntropy p <=
      Real.binEntropy v := by
    simpa [smul_eq_mul, Real.binEntropy_one_sub p, hcomb] using hc
  have hcollapse : alpha * Real.binEntropy p + beta * Real.binEntropy p =
      Real.binEntropy p := by
    calc
      alpha * Real.binEntropy p + beta * Real.binEntropy p =
          (alpha + beta) * Real.binEntropy p := by ring
      _ = Real.binEntropy p := by rw [hsum, one_mul]
  rw [hcollapse] at hc'
  exact le_trans hhCal hc'

/-- Under the calibration `h <= H_2(p)`, binary entropy dominates the tent
whose endpoint slopes are `h/p` and whose central plateau has height `h`.
The three proof cases follow the three chords in the article. -/
theorem calibrated_binary_entropy_tent (p h v : ℝ)
    (hp0 : 0 < p) (hpHalf : p < 1 / 2)
    (hhCal : Real.log 2 * h <= Real.binEntropy p)
    (hv0 : 0 <= v) (hv1 : v <= 1) :
    Real.log 2 * min ((h / p) * v) (min h ((h / p) * (1 - v))) <=
      Real.binEntropy v := by
  have hlog : 0 < Real.log 2 := by positivity
  by_cases hvp : v <= p
  · have hleft := entropy_left_arm p h v hp0 hpHalf hhCal hv0 hvp
    calc
      Real.log 2 * min ((h / p) * v) (min h ((h / p) * (1 - v))) <=
          Real.log 2 * ((h / p) * v) :=
        mul_le_mul_of_nonneg_left (min_le_left _ _) (le_of_lt hlog)
      _ <= Real.binEntropy v := hleft
  · by_cases hvRight : v <= 1 - p
    · have hmid := entropy_middle_plateau p h v hp0 hpHalf hhCal
        (le_of_not_ge hvp) hvRight
      have hmin : min ((h / p) * v) (min h ((h / p) * (1 - v))) <= h :=
        (min_le_right _ _).trans (min_le_left _ _)
      exact (mul_le_mul_of_nonneg_left hmin (le_of_lt hlog)).trans hmid
    · have htail0 : 0 <= 1 - v := by linarith
      have htailp : 1 - v <= p := by linarith
      have hright := entropy_left_arm p h (1 - v) hp0 hpHalf hhCal
        htail0 htailp
      have hmin : min ((h / p) * v) (min h ((h / p) * (1 - v))) <=
          (h / p) * (1 - v) :=
        (min_le_right _ _).trans (min_le_right _ _)
      calc
        Real.log 2 * min ((h / p) * v) (min h ((h / p) * (1 - v))) <=
            Real.log 2 * ((h / p) * (1 - v)) :=
          mul_le_mul_of_nonneg_left hmin (le_of_lt hlog)
        _ <= Real.binEntropy (1 - v) := hright
        _ = Real.binEntropy v := Real.binEntropy_one_sub v

/-- The calibrated tent credit is paid for by the information lost when two
cells of masses `a` and `z` are merged. The premise uses the equivalent
natural-log calibration `log(2) * h <= binEntropy(p)`. -/
theorem coarseningPenalty_le_binaryInformation
    (p h a z : ℝ)
    (hp0 : 0 < p) (hpHalf : p < 1 / 2)
    (hhCal : Real.log 2 * h <= Real.binEntropy p)
    (ha : 0 <= a) (hz : 0 <= z) :
    Real.log 2 * min ((h / p) * a) (min (h * (a + z)) ((h / p) * z)) <=
      PlanarQuery.Entropy.binaryInformation a z := by
  by_cases hsum : a + z = 0
  · have ha0 : a = 0 := by linarith
    have hz0 : z = 0 := by linarith
    simp [ha0, hz0, PlanarQuery.Entropy.binaryInformation]
  · have hsumPos : 0 < a + z := by
      rcases lt_or_eq_of_le (add_nonneg ha hz) with hpos | heq
      · exact hpos
      · exact (hsum heq.symm).elim
    have hv0 : 0 <= a / (a + z) := div_nonneg ha (le_of_lt hsumPos)
    have hv1 : a / (a + z) <= 1 :=
      (div_le_one hsumPos).2 (by linarith)
    have htent := calibrated_binary_entropy_tent p h (a / (a + z))
      hp0 hpHalf hhCal hv0 hv1
    have hsumNonneg : 0 <= a + z := add_nonneg ha hz
    have hscaled := mul_le_mul_of_nonneg_left htent hsumNonneg
    have hleftScale : (a + z) * ((h / p) * (a / (a + z))) = (h / p) * a := by
      field_simp [ne_of_gt hsumPos, ne_of_gt hp0]
      ring
    have hrightScale :
        (a + z) * ((h / p) * (1 - a / (a + z))) = (h / p) * z := by
      field_simp [ne_of_gt hsumPos, ne_of_gt hp0]
      ring
    have hscaleMin : (a + z) * (Real.log 2 *
        min ((h / p) * (a / (a + z)))
          (min h ((h / p) * (1 - a / (a + z))))) =
        Real.log 2 * min ((h / p) * a)
          (min (h * (a + z)) ((h / p) * z)) := by
      calc
        _ = Real.log 2 * ((a + z) *
            min ((h / p) * (a / (a + z)))
              (min h ((h / p) * (1 - a / (a + z))))) := by ring
        _ = Real.log 2 * min
            ((a + z) * ((h / p) * (a / (a + z))))
            (min ((a + z) * h)
              ((a + z) * ((h / p) * (1 - a / (a + z))))) := by
                rw [mul_min_of_nonneg _ _ hsumNonneg,
                  mul_min_of_nonneg _ _ hsumNonneg]
        _ = Real.log 2 * min ((h / p) * a)
            (min (h * (a + z)) ((h / p) * z)) := by
                rw [hleftScale, hrightScale]
                congr 2
                ring
    rw [hscaleMin] at hscaled
    rw [PlanarQuery.Entropy.binaryInformation_eq a z ha hz]
    exact hscaled

/-- The exact endpoint credit used by the expected-depth mode comparison is
paid for by the information lost when the two endpoint cells are merged. -/
theorem endpoint_credit_paid
    (p h a z : ℝ)
    (hp0 : 0 < p) (hpHalf : p < 1 / 2)
    (hhCal : Real.log 2 * h <= Real.binEntropy p)
    (ha : 0 <= a) (hz : 0 <= z) :
    Real.log 2 * PlanarQuery.ExpectedModeChoiceAlgebra.EStar p h a z <=
      PlanarQuery.Entropy.binaryInformation a z := by
  rw [PlanarQuery.ExpectedModeChoiceAlgebra.EStar, min_assoc]
  exact coarseningPenalty_le_binaryInformation p h a z hp0 hpHalf hhCal ha hz

end PlanarQuery.ExpectedCoarsening
