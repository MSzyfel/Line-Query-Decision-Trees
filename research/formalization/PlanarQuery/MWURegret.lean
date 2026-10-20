import PlanarQuery.Randomized
import PlanarQuery.Properization
import Mathlib.Analysis.Convex.SpecificFunctions.Basic
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-! The actual multiplicative-weights recursion and its logarithmic regret.
The gain bounds are proved for supplied-query tree depths below; neither
the potential estimate nor the final regret is a hypothesis. -/

namespace PlanarQuery
namespace MWU

open scoped BigOperators
noncomputable section

def weights {H : Type*} (η : ℝ) (g : ℕ → H → ℝ) : ℕ → H → ℝ
  | 0 => fun _ => 1
  | t + 1 => fun h => weights η g t h * (1 + η * g t h)

def total {H : Type*} [Fintype H] (η : ℝ) (g : ℕ → H → ℝ) (t : ℕ) : ℝ :=
  ∑ h, weights η g t h

def prior {H : Type*} [Fintype H] (η : ℝ) (g : ℕ → H → ℝ) (t : ℕ) (h : H) : ℝ :=
  weights η g t h / total η g t

def meanGain {H : Type*} [Fintype H] (η : ℝ) (g : ℕ → H → ℝ) (t : ℕ) : ℝ :=
  ∑ h, prior η g t h * g t h

theorem log_chord (η x : ℝ) (hη : 0 ≤ η) (hx : 0 ≤ x) (hx1 : x ≤ 1) :
    x * Real.log (1 + η) ≤ Real.log (1 + η * x) := by
  have hc : (1 - x) * Real.log 1 + x * Real.log (1 + η) ≤
      Real.log ((1 - x) * 1 + x * (1 + η)) :=
    (StrictConcaveOn.concaveOn strictConcaveOn_log_Ioi).2
    (by norm_num : (1 : ℝ) ∈ Set.Ioi 0)
    (by change 0 < 1 + η; linarith)
    (by linarith) hx (by ring)
  simp only [smul_eq_mul, Real.log_one, mul_zero, zero_add] at hc
  have he : (1 - x) * 1 + x * (1 + η) = 1 + η * x := by ring
  rw [he] at hc
  exact hc

theorem weights_pos {H : Type*} (η : ℝ) (g : ℕ → H → ℝ)
    (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) (h : H) :
    0 < weights η g t h := by
  induction t with
  | zero => simp [weights]
  | succ t ih =>
    exact mul_pos ih (by have := mul_nonneg hη (hg t h); linarith)

theorem total_pos {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) :
    0 < total η g t := by
  exact Finset.sum_pos (fun h _ => weights_pos η g hη hg t h) Finset.univ_nonempty

theorem prior_pos {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h)
    (t : ℕ) (h : H) : 0 < prior η g t h :=
  div_pos (weights_pos η g hη hg t h) (total_pos η g hη hg t)

theorem prior_sum {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) :
    (∑ h, prior η g t h) = 1 := by
  unfold prior
  rw [← Finset.sum_div]
  exact div_self (ne_of_gt (total_pos η g hη hg t))

theorem meanGain_nonneg {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) :
    0 ≤ meanGain η g t := by
  exact Finset.sum_nonneg fun h _ =>
    mul_nonneg (le_of_lt (prior_pos η g hη hg t h)) (hg t h)

theorem total_meanGain {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) :
    total η g t * meanGain η g t = ∑ h, weights η g t h * g t h := by
  unfold meanGain prior
  rw [Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro h hh
  field_simp [ne_of_gt (total_pos η g hη hg t)]

theorem total_succ {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (t : ℕ) :
    total η g (t + 1) = total η g t * (1 + η * meanGain η g t) := by
  calc
    total η g (t + 1) = total η g t + η * ∑ h, weights η g t h * g t h := by
      unfold total
      simp only [weights]
      rw [Finset.mul_sum, ← Finset.sum_add_distrib]
      apply Finset.sum_congr rfl
      intro h hh
      ring
    _ = total η g t * (1 + η * meanGain η g t) := by
      rw [← total_meanGain η g hη hg t]
      ring

theorem individual_log {H : Type*} (η : ℝ) (g : ℕ → H → ℝ)
    (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (K : ℕ) (h : H) :
    Real.log (weights η g K h) = ∑ t ∈ Finset.range K, Real.log (1 + η * g t h) := by
  induction K with
  | zero => simp [weights]
  | succ K ih =>
    rw [weights, Real.log_mul (ne_of_gt (weights_pos η g hη hg K h))
      (by have := mul_nonneg hη (hg K h); linarith), Finset.sum_range_succ, ih]

theorem individual_lower {H : Type*} (η : ℝ) (g : ℕ → H → ℝ)
    (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (hg1 : ∀ t h, g t h ≤ 1)
    (K : ℕ) (h : H) :
    Real.log (1 + η) * (∑ t ∈ Finset.range K, g t h) ≤ Real.log (weights η g K h) := by
  rw [individual_log η g hη hg K h, Finset.mul_sum]
  exact Finset.sum_le_sum fun t _ => by
    simpa only [mul_comm] using log_chord η (g t h) hη (hg t h) (hg1 t h)

theorem total_log_upper {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h) (K : ℕ) :
    Real.log (total η g K) ≤ Real.log (Fintype.card H : ℝ) +
      η * ∑ t ∈ Finset.range K, meanGain η g t := by
  induction K with
  | zero => simp [total, weights]
  | succ K ih =>
    have hp : 0 < 1 + η * meanGain η g K := by
      have := mul_nonneg hη (meanGain_nonneg η g hη hg K)
      linarith
    have hs := Real.log_le_sub_one_of_pos hp
    rw [total_succ η g hη hg K,
      Real.log_mul (ne_of_gt (total_pos η g hη hg K)) (ne_of_gt hp),
      Finset.sum_range_succ]
    nlinarith

theorem potential_comparison {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 ≤ η) (hg : ∀ t h, 0 ≤ g t h)
    (hg1 : ∀ t h, g t h ≤ 1) (K : ℕ) (h : H) :
    Real.log (1 + η) * (∑ t ∈ Finset.range K, g t h) ≤
      Real.log (Fintype.card H : ℝ) + η * ∑ t ∈ Finset.range K, meanGain η g t := by
  classical
  have hw : weights η g K h ≤ total η g K := by
    exact Finset.single_le_sum (fun j _ => le_of_lt (weights_pos η g hη hg K j))
      (Finset.mem_univ h)
  exact le_trans (individual_lower η g hη hg hg1 K h)
    (le_trans (Real.log_le_log (weights_pos η g hη hg K h) hw)
      (total_log_upper η g hη hg K))

theorem log_ratio_bounds (η : ℝ) (hη : 0 < η) (hη1 : η ≤ 1) :
    η / Real.log (1 + η) ≤ 1 + η ∧
      1 / Real.log (1 + η) ≤ 2 / η := by
  have hp : 0 < 1 + η := by linarith
  have hl : 0 < Real.log (1 + η) := Real.log_pos (by linarith)
  have hc : η / (1 + η) ≤ Real.log (1 + η) := by
    have hs := Real.one_sub_inv_le_log_of_pos hp
    convert hs using 1
    field_simp
  have hb : η ≤ Real.log (1 + η) * (1 + η) :=
    (div_le_iff₀ hp).mp hc
  constructor
  · apply (div_le_iff₀ hl).mpr
    nlinarith
  · apply (div_le_div_iff₀ hl hη).mpr
    nlinarith

/-- Regret for the actual recurrence, without assuming a potential estimate. -/
theorem gain_regret {H : Type*} [Fintype H] [Nonempty H]
    (η : ℝ) (g : ℕ → H → ℝ) (hη : 0 < η) (hη1 : η ≤ 1)
    (hg : ∀ t h, 0 ≤ g t h) (hg1 : ∀ t h, g t h ≤ 1)
    (K : ℕ) (hK : 0 < K) (h : H) :
    (∑ t ∈ Finset.range K, g t h) / (K : ℝ) ≤
      (1 + η) * ((∑ t ∈ Finset.range K, meanGain η g t) / (K : ℝ)) +
        2 * Real.log (Fintype.card H : ℝ) / (η * (K : ℝ)) := by
  have hl : 0 < Real.log (1 + η) := Real.log_pos (by linarith)
  have hn : 0 ≤ Real.log (Fintype.card H : ℝ) := by
    apply Real.log_nonneg
    exact_mod_cast Fintype.card_pos
  have hm : 0 ≤ ∑ t ∈ Finset.range K, meanGain η g t :=
    Finset.sum_nonneg fun t _ => meanGain_nonneg η g (le_of_lt hη) hg t
  have hc := potential_comparison η g (le_of_lt hη) hg hg1 K h
  have hr := log_ratio_bounds η hη hη1
  have hs : (∑ t ∈ Finset.range K, g t h) ≤
      (1 + η) * (∑ t ∈ Finset.range K, meanGain η g t) +
        2 * Real.log (Fintype.card H : ℝ) / η := by
    calc
      _ ≤ (Real.log (Fintype.card H : ℝ) +
          η * ∑ t ∈ Finset.range K, meanGain η g t) / Real.log (1 + η) := by
        apply (le_div_iff₀ hl).mpr
        simpa only [mul_comm] using hc
      _ = (η / Real.log (1 + η)) * (∑ t ∈ Finset.range K, meanGain η g t) +
          (1 / Real.log (1 + η)) * Real.log (Fintype.card H : ℝ) := by ring
      _ ≤ (1 + η) * (∑ t ∈ Finset.range K, meanGain η g t) +
          (2 / η) * Real.log (Fintype.card H : ℝ) :=
        add_le_add (mul_le_mul_of_nonneg_right hr.1 hm)
          (mul_le_mul_of_nonneg_right hr.2 hn)
      _ = _ := by ring
  have hpK : 0 < (K : ℝ) := Nat.cast_pos.mpr hK
  calc
    _ ≤ ((1 + η) * (∑ t ∈ Finset.range K, meanGain η g t) +
        2 * Real.log (Fintype.card H : ℝ) / η) / (K : ℝ) :=
      div_le_div_of_nonneg_right hs (le_of_lt hpK)
    _ = _ := by ring

def depthGain {H : Type*} (L : ℕ) (d : ℕ → H → ℕ) (t : ℕ) (h : H) : ℝ :=
  (d t h : ℝ) / (L : ℝ)

/-- Clearing denominators changes all weights by the same positive factor. -/
theorem integer_weights_eq {H : Type*} (p q L : ℕ) (d : ℕ → H → ℕ)
    (hq : 0 < q) (hL : 0 < L) (t : ℕ) (h : H) :
    (integerWeights p q L d t h : ℝ) =
      ((q : ℝ) * (L : ℝ)) ^ t * weights ((p : ℝ) / (q : ℝ)) (depthGain L d) t h := by
  have hq0 : (q : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hq)
  have hL0 : (L : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hL)
  induction t with
  | zero => simp [integerWeights, weights]
  | succ t ih =>
    simp only [integerWeights, integerUpdate, Nat.cast_mul, Nat.cast_add, ih,
      weights, depthGain, pow_succ]
    field_simp [hq0, hL0]
    ring

/-- The rational prior supplied to the tree oracle is exactly the real MWU prior. -/
theorem integer_prior_eq {H : Type*} [Fintype H] [Nonempty H]
    (p q L : ℕ) (d : ℕ → H → ℕ) (hq : 0 < q) (hL : 0 < L) (t : ℕ) (h : H) :
    (normalizedIntegerPrior (integerWeights p q L d t) h : ℝ) =
      prior ((p : ℝ) / (q : ℝ)) (depthGain L d) t h := by
  classical
  have hq0 : (q : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hq)
  have hL0 : (L : ℝ) ≠ 0 := ne_of_gt (Nat.cast_pos.mpr hL)
  have hs : ∑ j, (integerWeights p q L d t j : ℝ) =
      ((q : ℝ) * (L : ℝ)) ^ t * total ((p : ℝ) / (q : ℝ)) (depthGain L d) t := by
    simp only [integer_weights_eq p q L d hq hL t, total, Finset.mul_sum]
  unfold normalizedIntegerPrior prior
  push_cast
  rw [integer_weights_eq p q L d hq hL t h, hs]
  exact mul_div_mul_left _ _ (pow_ne_zero _ (mul_ne_zero hq0 hL0))

/-- Depth regret with the exact rational priors used by the algorithm. -/
theorem integer_depth_regret {H : Type*} [Fintype H] [Nonempty H]
    (p q L : ℕ) (d : ℕ → H → ℕ) (hp : 0 < p) (hq : 0 < q)
    (hpq : p ≤ q) (hL : 0 < L) (hd : ∀ t h, d t h ≤ L)
    (K : ℕ) (hK : 0 < K) (h : H) :
    (∑ t ∈ Finset.range K, (d t h : ℝ)) / (K : ℝ) ≤
      (1 + (p : ℝ) / (q : ℝ)) *
        ((∑ t ∈ Finset.range K,
          ∑ j, (normalizedIntegerPrior (integerWeights p q L d t) j : ℝ) *
            (d t j : ℝ)) / (K : ℝ)) +
      2 * (L : ℝ) * Real.log (Fintype.card H : ℝ) /
        (((p : ℝ) / (q : ℝ)) * (K : ℝ)) := by
  have hLpos : 0 < (L : ℝ) := Nat.cast_pos.mpr hL
  have hqpos : 0 < (q : ℝ) := Nat.cast_pos.mpr hq
  have hη : 0 < (p : ℝ) / (q : ℝ) := div_pos (Nat.cast_pos.mpr hp) hqpos
  have hη1 : (p : ℝ) / (q : ℝ) ≤ 1 := by
    apply (div_le_iff₀ hqpos).mpr
    simpa using (Nat.cast_le.mpr hpq : (p : ℝ) ≤ (q : ℝ))
  have hg : ∀ t h, 0 ≤ depthGain L d t h := by
    intro t h
    exact div_nonneg (Nat.cast_nonneg _) (le_of_lt hLpos)
  have hg1 : ∀ t h, depthGain L d t h ≤ 1 := by
    intro t h
    apply (div_le_iff₀ hLpos).mpr
    simpa using (Nat.cast_le.mpr (hd t h) : (d t h : ℝ) ≤ (L : ℝ))
  have hc := gain_regret ((p : ℝ) / (q : ℝ)) (depthGain L d) hη hη1 hg hg1 K hK h
  have hm : ∀ t, meanGain ((p : ℝ) / (q : ℝ)) (depthGain L d) t =
      (∑ j, (normalizedIntegerPrior (integerWeights p q L d t) j : ℝ) *
        (d t j : ℝ)) / (L : ℝ) := by
    intro t
    unfold meanGain
    rw [Finset.sum_div]
    apply Finset.sum_congr rfl
    intro j hj
    rw [integer_prior_eq p q L d hq hL t j]
    change prior ((p : ℝ) / (q : ℝ)) (depthGain L d) t j *
      ((d t j : ℝ) / (L : ℝ)) =
        (prior ((p : ℝ) / (q : ℝ)) (depthGain L d) t j * (d t j : ℝ)) / (L : ℝ)
    ring
  simp only [depthGain, ← Finset.sum_div, hm] at hc
  have hmul := mul_le_mul_of_nonneg_left hc (le_of_lt hLpos)
  convert hmul using 1 <;> field_simp [ne_of_gt hLpos] <;> ring

/-- One tree is sampled uniformly once for the whole identification run.
All trees in this mixture are supplied-query trees and are checked legal. -/
theorem legal_tree_mixture_regret {H Q : Type*} [Fintype H] [Nonempty H]
    [DecidableEq H] (M : QuerySystem H Q) (trees : ℕ → Tree H Q)
    (p q L K : ℕ) (hp : 0 < p) (hq : 0 < q) (hpq : p ≤ q)
    (hL : 0 < L) (hK : 0 < K)
    (hlegal : ∀ t, Tree.Identifies M Finset.univ (trees t))
    (hheight : ∀ t, Tree.height (trees t) ≤ L) :
    LegalMixture M Finset.univ (fun t : Fin K => trees t) (fun _ => 1 / (K : ℝ)) ∧
    RandomizedHeightAtMost M (fun t : Fin K => trees t) (fun _ => 1 / (K : ℝ))
      ((1 + (p : ℝ) / (q : ℝ)) *
        ((∑ t ∈ Finset.range K,
          ∑ j, (normalizedIntegerPrior
            (integerWeights p q L (fun s h => Tree.depth M (trees s) h) t) j : ℝ) *
              (Tree.depth M (trees t) j : ℝ)) / (K : ℝ)) +
        2 * (L : ℝ) * Real.log (Fintype.card H : ℝ) /
          (((p : ℝ) / (q : ℝ)) * (K : ℝ))) := by
  have hKpos : 0 < (K : ℝ) := Nat.cast_pos.mpr hK
  constructor
  · refine ⟨fun _ => by positivity, ?_, fun t _ => hlegal t⟩
    simp only [Finset.sum_const, Finset.card_univ, Fintype.card_fin, nsmul_eq_mul]
    field_simp
  · intro h
    have hc := integer_depth_regret p q L (fun t h => Tree.depth M (trees t) h)
      hp hq hpq hL (fun t h => le_trans (Tree.depth_le_height M (trees t) h) (hheight t))
      K hK h
    have he : randomizedDepth M (fun t : Fin K => trees t) (fun _ => 1 / (K : ℝ)) h =
        (∑ t ∈ Finset.range K, (Tree.depth M (trees t) h : ℝ)) / (K : ℝ) := by
      unfold randomizedDepth
      rw [← Finset.mul_sum]
      change (1 / (K : ℝ)) * (∑ t : Fin K, (Tree.depth M (trees (t : ℕ)) h : ℝ)) = _
      rw [Fin.sum_univ_eq_sum_range (fun t => (Tree.depth M (trees t) h : ℝ))]
      ring
    exact he.symm ▸ hc

/-- Properization supplies the depth cap required by the regret theorem. -/
theorem restricted_depth_cap {H Q : Type*} [Fintype H] [Nonempty H]
    [DecidableEq H] (M : QuerySystem H Q) (trees : ℕ → Tree H Q)
    (t : ℕ) (h : H) :
    Tree.depth M (Tree.restrict M (trees t) Finset.univ) h ≤ Fintype.card H - 1 := by
  exact le_trans (Tree.depth_le_height M _ h)
    (by simpa using (Tree.restricted_height_le_card_pred M (trees t) Finset.univ
      Finset.univ_nonempty))

end
end MWU
end PlanarQuery
