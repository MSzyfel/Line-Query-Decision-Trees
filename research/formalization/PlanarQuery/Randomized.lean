import PlanarQuery.Model
import PlanarQuery.Programming
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

namespace PlanarQuery

/-- The distinct randomized objective: maximum expected depth across
    hypotheses. This definition does not interchange maximum and expectation. -/
def randomizedDepth {H Q I : Type*} [Fintype I]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ)
    (h : H) : ℝ :=
  ∑ i, probability i * (Tree.depth M (trees i) h : ℝ)

def RandomizedHeightAtMost {H Q I : Type*} [Fintype I]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (probability : I → ℝ)
    (bound : ℝ) : Prop :=
  ∀ h, randomizedDepth M trees probability h ≤ bound

/-- Finite zero-sum-game weak duality on actual supplied-query trees.
    A distribution over hypotheses lower-bounding every candidate tree
    lower-bounds every feasible randomized-height value. -/
theorem randomized_tree_weak_duality
    {H Q I : Type*} [Fintype H] [Fintype I]
    (M : QuerySystem H Q) (trees : I → Tree H Q)
    (probability : I → ℝ) (adversary : H → ℝ) (lower bound : ℝ)
    (hp : ∀ i, 0 ≤ probability i) (hpSum : ∑ i, probability i = 1)
    (ha : ∀ h, 0 ≤ adversary h) (haSum : ∑ h, adversary h = 1)
    (hfeasible : RandomizedHeightAtMost M trees probability bound)
    (hdual : ∀ i, lower ≤ ∑ h, adversary h * (Tree.depth M (trees i) h : ℝ)) :
    lower ≤ bound := by
  have hleft : lower ≤
      ∑ i, probability i * (∑ h, adversary h * (Tree.depth M (trees i) h : ℝ)) := by
    calc
      lower = ∑ i, probability i * lower := by
        rw [← Finset.sum_mul, hpSum, one_mul]
      _ ≤ _ := Finset.sum_le_sum fun i _ =>
        mul_le_mul_of_nonneg_left (hdual i) (hp i)
  have hright : (∑ h, adversary h * randomizedDepth M trees probability h) ≤ bound :=
    finite_mixture_bound adversary (randomizedDepth M trees probability)
      bound ha haSum hfeasible
  have hswap :
      (∑ i, probability i * (∑ h, adversary h * (Tree.depth M (trees i) h : ℝ))) =
      ∑ h, adversary h * randomizedDepth M trees probability h := by
    unfold randomizedDepth
    simp only [Finset.mul_sum]
    rw [Finset.sum_comm]
    apply Finset.sum_congr rfl
    intro h hh
    apply Finset.sum_congr rfl
    intro i hi
    ring
  rw [hswap] at hleft
  exact le_trans hleft hright

/-- Validity of a randomized mixture is checked independently for every
    supplied-query tree in its positive support. -/
def LegalMixture {H Q I : Type*} [Fintype I] [DecidableEq H]
    (M : QuerySystem H Q) (S : Finset H) (trees : I → Tree H Q)
    (probability : I → ℝ) : Prop :=
  (∀ i, 0 ≤ probability i) ∧ (∑ i, probability i = 1) ∧
    ∀ i, 0 < probability i → Tree.Identifies M S (trees i)

def integerUpdate {H : Type*} (p q heightCap : ℕ)
    (currentDepth weight : H → ℕ) (h : H) : ℕ :=
  weight h * (q * heightCap + p * currentDepth h)

theorem integer_update_positive {H : Type*} (p q heightCap : ℕ)
    (currentDepth weight : H → ℕ) (h : H)
    (hq : 0 < q) (hL : 0 < heightCap) (hw : 0 < weight h) :
    0 < integerUpdate p q heightCap currentDepth weight h := by
  apply Nat.mul_pos hw
  exact lt_of_lt_of_le (Nat.mul_pos hq hL) (Nat.le_add_right _ _)

theorem integer_update_bound {H : Type*} (p q heightCap bound : ℕ)
    (currentDepth weight : H → ℕ) (h : H)
    (hw : weight h ≤ bound) (hdepth : currentDepth h ≤ heightCap) :
    integerUpdate p q heightCap currentDepth weight h ≤
      bound * ((p + q) * heightCap) := by
  unfold integerUpdate
  apply Nat.mul_le_mul hw
  calc
    q * heightCap + p * currentDepth h ≤ q * heightCap + p * heightCap :=
      Nat.add_le_add_left (Nat.mul_le_mul_left p hdepth) _
    _ = (p + q) * heightCap := by ring

def integerWeights {H : Type*} (p q heightCap : ℕ)
    (depthSequence : ℕ → H → ℕ) : ℕ → H → ℕ
  | 0 => fun _ => 1
  | round + 1 => integerUpdate p q heightCap (depthSequence round)
      (integerWeights p q heightCap depthSequence round)

theorem integer_weights_positive {H : Type*} (p q heightCap : ℕ)
    (depthSequence : ℕ → H → ℕ) (hq : 0 < q) (hL : 0 < heightCap)
    (round : ℕ) (h : H) :
    0 < integerWeights p q heightCap depthSequence round h := by
  induction round with
  | zero => simp [integerWeights]
  | succ round ih =>
    exact integer_update_positive p q heightCap
      (depthSequence round) (integerWeights p q heightCap depthSequence round)
      h hq hL ih

theorem integer_weights_size_bound {H : Type*} (p q heightCap : ℕ)
    (depthSequence : ℕ → H → ℕ) (hdepth : ∀ round h, depthSequence round h ≤ heightCap)
    (round : ℕ) (h : H) :
    integerWeights p q heightCap depthSequence round h ≤ ((p + q) * heightCap) ^ round := by
  induction round with
  | zero => simp [integerWeights]
  | succ round ih =>
    simpa only [pow_succ] using integer_update_bound p q heightCap
      (((p + q) * heightCap) ^ round) (depthSequence round)
      (integerWeights p q heightCap depthSequence round) h ih (hdepth round h)

def normalizedIntegerPrior {H : Type*} [Fintype H] (weight : H → ℕ) (h : H) : ℚ :=
  (weight h : ℚ) / ∑ g, (weight g : ℚ)

theorem positive_integer_total {H : Type*} [Fintype H] [Nonempty H]
    (weight : H → ℕ) (hw : ∀ h, 0 < weight h) :
    0 < ∑ g, (weight g : ℚ) := by
  exact Finset.sum_pos (fun h _ => Nat.cast_pos.mpr (hw h)) Finset.univ_nonempty

theorem normalized_integer_prior_positive {H : Type*} [Fintype H] [Nonempty H]
    (weight : H → ℕ) (hw : ∀ h, 0 < weight h) (h : H) :
    0 < normalizedIntegerPrior weight h := by
  exact div_pos (Nat.cast_pos.mpr (hw h)) (positive_integer_total weight hw)

theorem normalized_integer_prior_sum {H : Type*} [Fintype H] [Nonempty H]
    (weight : H → ℕ) (hw : ∀ h, 0 < weight h) :
    (∑ h, normalizedIntegerPrior weight h) = 1 := by
  unfold normalizedIntegerPrior
  rw [← Finset.sum_div, div_self (ne_of_gt (positive_integer_total weight hw))]

/-- The final transfer proof is separate from proving the regret estimate,
    comparison-game duality, or the oracle guarantee. -/
theorem randomized_transfer_arithmetic
    (randomizedCost optimum averageOracle entropy L η K α ε : ℝ)
    (hL : 0 < L) (hη : 0 < η) (hK : 0 < K)
    (hopt : 0 ≤ optimum)
    (haverage : averageOracle ≤ α * optimum)
    (hentropy : entropy < optimum)
    (hregret : randomizedCost ≤ (1 + η) * averageOracle + 2 * L * entropy / (η * K))
    (hcalibration : (1 + η) * α + 2 * L / (η * K) ≤ α + ε) :
    randomizedCost < (α + ε) * optimum := by
  have hmean := mul_le_mul_of_nonneg_left haverage (by positivity : 0 ≤ 1 + η)
  have hstrict := mul_lt_mul_of_pos_left hentropy
    (by positivity : 0 < 2 * L / (η * K))
  have hcal := mul_le_mul_of_nonneg_right hcalibration hopt
  have hrearrange : (2 * L / (η * K)) * entropy = 2 * L * entropy / (η * K) := by ring
  rw [hrearrange] at hstrict
  nlinarith

theorem randomized_calibration (α ε L K : ℝ)
    (hα : 1 ≤ α) (hε : 0 < ε) (hL : 0 < L)
    (hK : 8 * α * L / ε ^ 2 ≤ K) :
    (1 + ε / (2 * α)) * α + 2 * L / ((ε / (2 * α)) * K) ≤ α + ε := by
  have hαpos : 0 < α := by linarith
  have hKpos : 0 < K := lt_of_lt_of_le (by positivity) hK
  have hden : 0 < (ε / (2 * α)) * K := by positivity
  have hscale : 8 * α * L ≤ K * ε ^ 2 := (div_le_iff₀ (sq_pos_of_pos hε)).mp hK
  have hratio : 2 * L / ((ε / (2 * α)) * K) ≤ ε / 2 := by
    apply (div_le_iff₀ hden).mpr
    have hbound : 2 * L ≤ ε ^ 2 * K / (4 * α) := by
      apply (le_div_iff₀ (by positivity : 0 < 4 * α)).mpr
      nlinarith [hscale]
    have halgebra : ε / 2 * ((ε / (2 * α)) * K) = ε ^ 2 * K / (4 * α) := by ring
    rw [halgebra]
    exact hbound
  have hfirst : (1 + ε / (2 * α)) * α = α + ε / 2 := by
    field_simp [ne_of_gt hαpos]
    ring
  rw [hfirst]
  linarith

end PlanarQuery
