import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Tactic

set_option maxHeartbeats 300000

/-! Arithmetic for the internal-unmatched-vertex penalty in the
expected-depth reduction.  The theorem assumes the manuscript's matching
invoice and scale estimates explicitly; it does not prove those estimates
from the geometric construction. -/

namespace PlanarQuery

open Finset

/-- The calibration and invoice inequalities exclude an internal unmatched
item.  `Amax` bounds all baseline item weights, while `iInternal` is an item
whose unmatched weight reaches the isolated-vertex threshold `Z`.

The hypotheses package the matching-dependent invoice in the manuscript:
nonnegative pair and unmatched completion costs, nonnegative unmatched
weights, and the isolated-vertex term `r * ∑ min (U i) Z`.  The remaining
hypotheses are precisely the threshold formula and scale/calibration bounds
listed in the proof of `clm:average-internal-penalty`. -/
theorem average_internal_penalty
    {m : ℕ} (A U t : Fin m → ℝ) (iInternal : Fin m)
    (G Gfix pairCost unmatchedCompletion q r p V B s Z Amax Cref Eplus k : ℝ)
    (hG : G = Gfix + pairCost + unmatchedCompletion
        + (q - 1) * (∑ i : Fin m, U i)
        + r * (∑ i : Fin m, min (U i) Z))
    (hpair : 0 ≤ pairCost)
    (hunmatchedCompletion : 0 ≤ unmatchedCompletion)
    (hU : ∀ i, 0 ≤ U i)
    (hUdominatesA : ∀ i, A i ≤ U i)
    (hA_nonneg : ∀ i, 0 ≤ A i)
    (hAmax : ∀ i, A i ≤ Amax)
    (hinternal : Z ≤ U iInternal)
    (hq : 1 ≤ q) (hr : 0 ≤ r) (hp : 1 ≤ p) (hm : 1 ≤ (m : ℝ))
    (hV : 0 < V)
    (hZvalue : Z = V / 2)
    (hAmax_small : Amax < V / 100)
    (hthreshold_s : s = p * B)
    (ht_rank : ∀ i, t i - r ≤ q + (m : ℝ))
    (hCref : Cref ≤ (p + 6) * (q + 1) ^ 2 * V)
    (hEplus : Eplus ≤ V / 1000)
    (hcalibration :
      r / 3 ≥ (1000 / 3 : ℝ) * (p + 10) * (q + (m : ℝ) + 1) ^ 2)
    (hk : k = Gfix + (∑ i : Fin m, t i * A i) + Cref
        + (V / 2) * (p * B ^ 2 - s ^ 2) + Eplus) :
    G > k := by
  have hA_sum : (∑ i : Fin m, A i) < (m : ℝ) * V / 100 := by
    have hsum_max : (∑ i : Fin m, A i) ≤ (m : ℝ) * Amax := by
      calc
        (∑ i : Fin m, A i) ≤ ∑ _i : Fin m, Amax :=
          Finset.sum_le_sum fun i _ => hAmax i
        _ = (m : ℝ) * Amax := by simp [nsmul_eq_mul]
    have hscale : (m : ℝ) * Amax < (m : ℝ) * (V / 100) :=
      mul_lt_mul_of_pos_left hAmax_small (by linarith)
    have hrewrite : (m : ℝ) * (V / 100) = (m : ℝ) * V / 100 := by ring
    rw [← hrewrite]
    exact lt_of_le_of_lt hsum_max hscale
  have hZ : Amax < Z := by
    calc
      Amax < V / 100 := hAmax_small
      _ < V / 2 := by linarith
      _ = Z := hZvalue.symm
  have hmin_lower (i : Fin m) : A i ≤ min (U i) Z := by
    exact le_min (hUdominatesA i) ((hAmax i).trans hZ.le)
  have hmin_internal : min (U iInternal) Z = Z := by
    exact min_eq_right hinternal
  have hmin_sum :
      (∑ i : Fin m, A i) + (Z - Amax) ≤
        ∑ i : Fin m, min (U i) Z := by
    have hdiff (i : Fin m) : 0 ≤ min (U i) Z - A i := by
      linarith [hmin_lower i]
    have hsingle : Z - Amax ≤ min (U iInternal) Z - A iInternal := by
      rw [hmin_internal]
      linarith [hAmax iInternal]
    have hsumdiff := Finset.single_le_sum
      (fun i _ => hdiff i) (Finset.mem_univ iInternal)
    rw [Finset.sum_sub_distrib] at hsumdiff
    linarith
  have hG_lower :
      Gfix + r * (∑ i : Fin m, A i) + r * (Z - Amax) ≤ G := by
    rw [hG]
    have hqterm : 0 ≤ (q - 1) * (∑ i : Fin m, U i) := by
      apply mul_nonneg
      · linarith
      · exact Finset.sum_nonneg fun i hi => hU i
    have hpair_terms : 0 ≤ pairCost + unmatchedCompletion := add_nonneg hpair hunmatchedCompletion
    have hrmin :
        r * ((∑ i : Fin m, A i) + (Z - Amax)) ≤
          r * (∑ i : Fin m, min (U i) Z) :=
      mul_le_mul_of_nonneg_left hmin_sum hr
    rw [mul_add] at hrmin
    linarith
  have hthreshold_upper :
      k < Gfix + r * (∑ i : Fin m, A i)
        + (p + 8) * (q + (m : ℝ) + 1) ^ 2 * V := by
    rw [hk]
    have hcoeff :
        (∑ i : Fin m, t i * A i) ≤
          r * (∑ i : Fin m, A i) + (q + (m : ℝ)) * (∑ i : Fin m, A i) := by
      calc
        (∑ i : Fin m, t i * A i)
            ≤ ∑ i : Fin m, (r + (q + (m : ℝ))) * A i := by
                apply Finset.sum_le_sum
                intro i hi
                have hti : t i ≤ r + (q + (m : ℝ)) := by linarith [ht_rank i]
                exact mul_le_mul_of_nonneg_right hti (hA_nonneg i)
        _ = r * (∑ i : Fin m, A i) +
              (q + (m : ℝ)) * (∑ i : Fin m, A i) := by
                rw [← Finset.mul_sum]
                ring
    have hquad : p * B ^ 2 - s ^ 2 ≤ 0 := by
      rw [hthreshold_s]
      have hpsq : p ≤ p ^ 2 := by nlinarith only [hp]
      have hmul := mul_le_mul_of_nonneg_right hpsq (sq_nonneg B)
      nlinarith only [hmul]
    have hY : 0 < q + (m : ℝ) + 1 := by positivity
    have hq1 : 0 ≤ q + 1 := by linarith
    have hq_bound : q + 1 ≤ q + (m : ℝ) + 1 := by linarith
    have hqm_bound : q + (m : ℝ) ≤ q + (m : ℝ) + 1 := by linarith
    have hbase :
        (p + 6) * (q + 1) ^ 2 * V
          + (q + (m : ℝ)) * ((m : ℝ) * V / 100)
          + V / 1000
        < (p + 8) * (q + (m : ℝ) + 1) ^ 2 * V := by
      have hp_nonneg : 0 ≤ p + 6 := by linarith
      have hq_sq : (q + 1) ^ 2 ≤ (q + (m : ℝ) + 1) ^ 2 := by
        nlinarith [sq_nonneg (q + 1), sq_nonneg (q + (m : ℝ) + 1)]
      have hqm_sq : (q + (m : ℝ)) * (m : ℝ) ≤
          (q + (m : ℝ) + 1) ^ 2 := by
        have hQ : 0 ≤ q + (m : ℝ) := by linarith
        have hm0 : 0 ≤ (m : ℝ) := by linarith
        have hQleY : q + (m : ℝ) ≤ q + (m : ℝ) + 1 := by linarith
        have hmleY : (m : ℝ) ≤ q + (m : ℝ) + 1 := by linarith
        calc
          (q + (m : ℝ)) * (m : ℝ)
              ≤ (q + (m : ℝ) + 1) * (m : ℝ) :=
                mul_le_mul_of_nonneg_right hQleY hm0
          _ ≤ (q + (m : ℝ) + 1) * (q + (m : ℝ) + 1) :=
                mul_le_mul_of_nonneg_left hmleY (by linarith)
          _ = (q + (m : ℝ) + 1) ^ 2 := by ring
      have hVY : 0 ≤ (q + (m : ℝ) + 1) ^ 2 * V := by positivity
      have hfirst := mul_le_mul_of_nonneg_left hq_sq hp_nonneg
      have hfirst' := mul_le_mul_of_nonneg_right hfirst hV.le
      have hsecond := mul_le_mul_of_nonneg_right hqm_sq (by positivity : 0 ≤ V / 100)
      have hthird : V / 1000 ≤ (q + (m : ℝ) + 1) ^ 2 * V / 1000 := by
        have hYlarge : 1 ≤ (q + (m : ℝ) + 1) ^ 2 := by nlinarith only [hY, hq, hm]
        nlinarith only [hYlarge, hV]
      have hcoeffgap : (1 : ℝ) / 100 + 1 / 1000 < 2 := by norm_num
      have hsecond' : (q + (m : ℝ)) * ((m : ℝ) * V / 100) ≤
          (1 / 100 : ℝ) * ((q + (m : ℝ) + 1) ^ 2 * V) := by
        calc
          (q + (m : ℝ)) * ((m : ℝ) * V / 100)
              = ((q + (m : ℝ)) * (m : ℝ) * (V / 100)) := by ring
          _ ≤ (q + (m : ℝ) + 1) ^ 2 * (V / 100) := hsecond
          _ = (1 / 100 : ℝ) * ((q + (m : ℝ) + 1) ^ 2 * V) := by ring
      have hthird' : V / 1000 ≤
          (1 / 1000 : ℝ) * ((q + (m : ℝ) + 1) ^ 2 * V) := by
        nlinarith only [hthird]
      have hcoeffgap' :
          p + 6 + (1 : ℝ) / 100 + 1 / 1000 < p + 8 := by linarith
      have hVYpos : 0 < (q + (m : ℝ) + 1) ^ 2 * V := by positivity
      have hscaled := mul_lt_mul_of_pos_right hcoeffgap' hVYpos
      nlinarith only [hfirst', hsecond', hthird', hscaled]
    have hAterm :
        (q + (m : ℝ)) * (∑ i : Fin m, A i) <
          (q + (m : ℝ)) * ((m : ℝ) * V / 100) := by
      exact mul_lt_mul_of_pos_left hA_sum (by positivity)
    have hA_nonneg_sum : 0 ≤ (∑ i : Fin m, A i) :=
      Finset.sum_nonneg fun i hi => hA_nonneg i
    have hquad_term : (V / 2) * (p * B ^ 2 - s ^ 2) ≤ 0 := by
      exact mul_nonpos_of_nonneg_of_nonpos (by positivity) hquad
    calc
      Gfix + (∑ i : Fin m, t i * A i) + Cref
          + (V / 2) * (p * B ^ 2 - s ^ 2) + Eplus
          ≤ Gfix + (r * (∑ i : Fin m, A i)
              + (q + (m : ℝ)) * (∑ i : Fin m, A i))
              + (p + 6) * (q + 1) ^ 2 * V + Eplus := by
                nlinarith only [hcoeff, hCref, hquad_term]
      _ ≤ Gfix + r * (∑ i : Fin m, A i)
          + (p + 6) * (q + 1) ^ 2 * V
          + (q + (m : ℝ)) * ((m : ℝ) * V / 100) + V / 1000 := by
            have hE : Eplus ≤ V / 1000 := hEplus
            have hAterm_nonneg : 0 ≤
                (q + (m : ℝ)) * (∑ i : Fin m, A i) :=
              mul_nonneg (by linarith) hA_nonneg_sum
            linarith
      _ < Gfix + r * (∑ i : Fin m, A i)
          + (p + 8) * (q + (m : ℝ) + 1) ^ 2 * V := by
            linarith [hbase]
  have hpenalty :
      (p + 8) * (q + (m : ℝ) + 1) ^ 2 * V < r * (Z - Amax) := by
    have hZgap : V / 3 < Z - Amax := by
      rw [hZvalue]
      nlinarith only [hAmax_small, hV]
    have hrmul :
        (1000 / 3 : ℝ) * (p + 10) * (q + (m : ℝ) + 1) ^ 2 * V
          ≤ r * (V / 3) := by
      have hcal := hcalibration
      nlinarith only [hcal, hV]
    have hcal_lt :
        (p + 8) * (q + (m : ℝ) + 1) ^ 2 * V <
          (1000 / 3 : ℝ) * (p + 10) * (q + (m : ℝ) + 1) ^ 2 * V := by
      have hYsq : 0 < (q + (m : ℝ) + 1) ^ 2 := sq_pos_of_pos (by linarith)
      have hcoefflt : p + 8 < (1000 / 3 : ℝ) * (p + 10) := by
        nlinarith only [hp]
      have hfirst := mul_lt_mul_of_pos_right hcoefflt hYsq
      exact mul_lt_mul_of_pos_right hfirst hV
    have hcalpos : 0 < (1000 / 3 : ℝ) * (p + 10) *
        (q + (m : ℝ) + 1) ^ 2 := by positivity
    have hrpos : 0 < r := by linarith [hcalibration]
    have hmul : r * (V / 3) < r * (Z - Amax) :=
      mul_lt_mul_of_pos_left hZgap hrpos
    linarith
  linarith

end PlanarQuery
