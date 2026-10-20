import PlanarQuery.Randomized
import PlanarQuery.Properization
import Mathlib.Analysis.NormedSpace.HahnBanach.Separation
import Mathlib.Analysis.Convex.Topology
import Mathlib.Analysis.Convex.Caratheodory
import Mathlib.Topology.Order.Lattice
import Mathlib.LinearAlgebra.Dimension.Finite
import Mathlib.LinearAlgebra.Dimension.Constructions
import Mathlib.LinearAlgebra.AffineSpace.FiniteDimensional
import Mathlib.Tactic.Linarith
import Mathlib.Tactic.Positivity
import Mathlib.Tactic.FieldSimp

/-! Finite tree-game strong duality, proved by compact convex separation.
The matrix columns below will be the depths of actual supplied-query trees.
No LP-duality conclusion is a premise of the separation theorem. -/

namespace PlanarQuery
namespace FiniteGame

universe u v

open scoped BigOperators
noncomputable section

theorem linear_form_coordinates {H : Type*} [Fintype H] [DecidableEq H]
    (f : (H → ℝ) →L[ℝ] ℝ) (x : H → ℝ) :
    f x = ∑ h, x h * f (Pi.single h (1 : ℝ)) := by
  classical
  have hx : (∑ h, x h • (Pi.single h (1 : ℝ) : H → ℝ)) = x := by
    ext j
    simp [Finset.sum_apply, Pi.single_apply]
  calc
    f x = f (∑ h, x h • (Pi.single h (1 : ℝ) : H → ℝ)) := congrArg f hx.symm
    _ = _ := by rw [map_sum]; simp only [map_smul, smul_eq_mul]

/-- A functional bounded above on the lower orthant has nonnegative coordinates. -/
theorem lower_orthant_coeff_nonneg {H : Type*} [Fintype H] [DecidableEq H]
    (f : (H → ℝ) →L[ℝ] ℝ) (r u : ℝ)
    (hf : ∀ x : H → ℝ, (∀ h, x h ≤ r) → f x < u) (j : H) :
    0 ≤ f (Pi.single j (1 : ℝ)) := by
  classical
  by_contra hnonneg
  have ha : f (Pi.single j (1 : ℝ)) < 0 := lt_of_not_ge hnonneg
  let c := f (fun _ : H => r)
  let t := (|c - u| + 1) / (-f (Pi.single j (1 : ℝ)))
  have hapos : 0 < -f (Pi.single j (1 : ℝ)) := by linarith
  have ht : 0 ≤ t := div_nonneg (by positivity) (le_of_lt hapos)
  let x : H → ℝ := (fun _ => r) - t • (Pi.single j (1 : ℝ) : H → ℝ)
  have hx : ∀ h, x h ≤ r := by
    intro h
    dsimp [x]
    simp only [Pi.sub_apply, Pi.smul_apply, smul_eq_mul, Pi.single_apply]
    split_ifs <;> nlinarith
  have hupper := hf x hx
  have hvalue : f x = c + |c - u| + 1 := by
    dsimp [x, c, t]
    rw [map_sub, map_smul]
    simp only [smul_eq_mul]
    field_simp [ne_of_lt ha]
    ring
  have habs : u - c ≤ |c - u| := by
    have := neg_le_abs (c - u)
    linarith
  rw [hvalue] at hupper
  linarith

/-- Strong finite-game duality in feasibility form.  The left side is the
primal convex-hull feasibility problem, and the right side is the normalized
dual test for every distribution over rows. -/
theorem hull_feasible_iff_dual {H I : Type*} [Fintype H] [Fintype I]
    [Nonempty I] (A : I → H → ℝ) (r : ℝ) :
    (∃ x ∈ convexHull ℝ (Set.range A), ∀ h, x h ≤ r) ↔
      (∀ a : H → ℝ, (∀ h, 0 ≤ a h) → (∑ h, a h) = 1 →
        ∃ i, (∑ h, a h * A i h) ≤ r) := by
  classical
  constructor
  · rintro ⟨x, hx, hxr⟩ a ha hasum
    by_contra hn
    push_neg at hn
    let C : Set (H → ℝ) := {y | r < ∑ h, a h * y h}
    have hconv : Convex ℝ C := by
      intro y hy z hz s t hs ht hst
      change r < ∑ h, a h * (s * y h + t * z h)
      have he : (∑ h, a h * (s * y h + t * z h)) =
          s * (∑ h, a h * y h) + t * (∑ h, a h * z h) := by
        rw [Finset.mul_sum, Finset.mul_sum, ← Finset.sum_add_distrib]
        apply Finset.sum_congr rfl
        intro h hh
        ring
      rw [he]
      dsimp [C] at hy hz
      rcases hs.eq_or_lt with hs0 | hspos
      · have ht1 : t = 1 := by linarith
        simp only [← hs0, zero_mul, zero_add, ht1, one_mul]
        exact hz
      · have h1 := mul_lt_mul_of_pos_left hy hspos
        have h2 := mul_le_mul_of_nonneg_left (le_of_lt hz) ht
        have heq : s * r + t * r = r := by rw [← add_mul, hst, one_mul]
        linarith
    have hrange : Set.range A ⊆ C := by rintro y ⟨i, rfl⟩; exact hn i
    have hc : x ∈ C := convexHull_min hrange hconv hx
    have hb : (∑ h, a h * x h) ≤ r :=
      finite_mixture_bound a x r ha hasum hxr
    exact (not_lt_of_ge hb) hc
  · intro hdual
    by_contra hn
    let L : Set (H → ℝ) := {x | ∀ h, x h ≤ r}
    have hLc : Convex ℝ L := by
      intro x hx y hy s t hs ht hst h
      change s * x h + t * y h ≤ r
      have h1 := mul_le_mul_of_nonneg_left (hx h) hs
      have h2 := mul_le_mul_of_nonneg_left (hy h) ht
      calc
        _ ≤ s * r + t * r := add_le_add h1 h2
        _ = r := by rw [← add_mul, hst, one_mul]
    have hLclosed : IsClosed L := by
      have heq : L = ⋂ h : H, {x : H → ℝ | x h ≤ r} := by ext x; simp [L]
      rw [heq]
      exact isClosed_iInter fun h => isClosed_le (continuous_apply h) continuous_const
    have hcompact : IsCompact (convexHull ℝ (Set.range A)) :=
      (Set.finite_range A).isCompact_convexHull
    have hdisj : Disjoint L (convexHull ℝ (Set.range A)) := by
      rw [Set.disjoint_left]
      intro x hxL hxC
      exact hn ⟨x, hxC, hxL⟩
    obtain ⟨f, u, v, hLf, huv, hCf⟩ :=
      geometric_hahn_banach_closed_compact hLc hLclosed (convex_convexHull ℝ _) hcompact hdisj
    let a : H → ℝ := fun h => f (Pi.single h (1 : ℝ))
    have ha : ∀ h, 0 ≤ a h := lower_orthant_coeff_nonneg f r u hLf
    have hsumNonneg : 0 ≤ ∑ h, a h := Finset.sum_nonneg fun h _ => ha h
    have hsum : 0 < ∑ h, a h := by
      by_contra hnpos
      have hs0 : (∑ h, a h) = 0 := le_antisymm (le_of_not_gt hnpos) hsumNonneg
      have hazero : ∀ h, a h = 0 := by
        simpa only [Finset.mem_univ, forall_true_left] using
          (Finset.sum_eq_zero_iff_of_nonneg (fun h _ => ha h)).mp hs0
      have hfzero : ∀ x : H → ℝ, f x = 0 := by
        intro x
        rw [linear_form_coordinates f x]
        change (∑ h, x h * a h) = 0
        simp only [hazero, mul_zero, Finset.sum_const_zero]
      obtain ⟨i⟩ := ‹Nonempty I›
      have hlow := hLf (fun _ => r) (fun _ => le_rfl)
      have hhigh := hCf (A i) (subset_convexHull ℝ _ (Set.mem_range_self i))
      rw [hfzero] at hlow hhigh
      linarith
    have hp : ∑ h, a h / (∑ j, a j) = 1 := by
      rw [← Finset.sum_div]
      exact div_self (ne_of_gt hsum)
    obtain ⟨i, hi⟩ := hdual (fun h => a h / (∑ j, a j))
      (fun h => div_nonneg (ha h) (le_of_lt hsum)) hp
    have hlow := hLf (fun _ => r) (fun _ => le_rfl)
    have hhigh := hCf (A i) (subset_convexHull ℝ _ (Set.mem_range_self i))
    have he : f (A i) ≤ r * ∑ h, a h := by
      rw [linear_form_coordinates f (A i)]
      have hs : (∑ h, a h / (∑ j, a j) * A i h) =
          (∑ h, a h * A i h) / (∑ j, a j) := by
        rw [Finset.sum_div]
        apply Finset.sum_congr rfl
        intro h hh
        ring
      rw [hs] at hi
      have hib := (div_le_iff₀ hsum).mp hi
      simpa only [mul_comm] using hib
    have hr : f (fun _ : H => r) = r * ∑ h, a h := by
      rw [linear_form_coordinates]
      exact (Finset.mul_sum _ _ _).symm
    rw [hr] at hlow
    linarith

/-- The convex-hull feasibility theorem is exactly strong duality for
mixtures of the supplied legal trees, rather than an abstract surrogate game. -/
theorem legal_tree_game_duality {H Q I : Type*} [Fintype H] [Fintype I]
    [Nonempty I] [DecidableEq H] (M : QuerySystem H Q)
    (trees : I → Tree H Q) (r : ℝ)
    (hlegal : ∀ i, Tree.Identifies M Finset.univ (trees i)) :
    (∃ (J : Type) (_ : Fintype J) (choice : J → I) (probability : J → ℝ),
      LegalMixture M Finset.univ (fun j => trees (choice j)) probability ∧
      RandomizedHeightAtMost M (fun j => trees (choice j)) probability r) ↔
    (∀ a : H → ℝ, (∀ h, 0 ≤ a h) → (∑ h, a h) = 1 →
      ∃ i, (∑ h, a h * (Tree.depth M (trees i) h : ℝ)) ≤ r) := by
  classical
  let A : I → H → ℝ := fun i h => (Tree.depth M (trees i) h : ℝ)
  rw [← hull_feasible_iff_dual A r]
  constructor
  · rintro ⟨J, instJ, choice, probability, hmix, hbound⟩
    letI := instJ
    let x : H → ℝ := ∑ j, probability j • A (choice j)
    refine ⟨x, ?_, ?_⟩
    · exact mem_convexHull_of_exists_fintype probability (fun j => A (choice j))
        hmix.1 hmix.2.1 (fun j => Set.mem_range_self (choice j)) rfl
    · intro h
      have he : x h = randomizedDepth M (fun j => trees (choice j)) probability h := by
        simp only [x, A, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, randomizedDepth]
      exact he.symm ▸ hbound h
  · rintro ⟨x, hx, hbound⟩
    obtain ⟨J, instJ, probability, z, hp, hpsum, hz, hsum⟩ :=
      mem_convexHull_iff_exists_fintype.mp hx
    letI := instJ
    let choice : J → I := fun j => Classical.choose (hz j)
    have hchoice : ∀ j, A (choice j) = z j := fun j => Classical.choose_spec (hz j)
    refine ⟨J, instJ, choice, probability, ⟨hp, hpsum, fun j _ => hlegal (choice j)⟩, ?_⟩
    intro h
    have he : randomizedDepth M (fun j => trees (choice j)) probability h = x h := by
      have hv : (∑ j, probability j • A (choice j)) = x := by
        simpa only [hchoice] using hsum
      have he := congrArg (fun y : H → ℝ => y h) hv
      simpa only [A, Finset.sum_apply, Pi.smul_apply, smul_eq_mul, randomizedDepth] using he
    exact he ▸ hbound h

def bestResponseCost {H I : Type*} [Fintype H] [Fintype I] [Nonempty I]
    (A : I → H → ℝ) (a : H → ℝ) : ℝ :=
  Finset.univ.inf' Finset.univ_nonempty (fun i => ∑ h, a h * A i h)

theorem best_response_continuous {H I : Type*} [Fintype H] [Fintype I] [Nonempty I]
    (A : I → H → ℝ) : Continuous (bestResponseCost A) := by
  classical
  unfold bestResponseCost
  apply Continuous.finset_inf'_apply
  intro i hi
  exact continuous_finset_sum _ (fun h _ => (continuous_apply h).mul continuous_const)

/-- Both sides attain their common value.  In particular the optimizing
prior is obtained from compactness, not assumed as a dual certificate. -/
theorem attained_saddle {H I : Type*} [Fintype H] [Fintype I]
    [Nonempty H] [Nonempty I] (A : I → H → ℝ) :
    ∃ (a x : H → ℝ) (r : ℝ), a ∈ stdSimplex ℝ H ∧
      x ∈ convexHull ℝ (Set.range A) ∧ (∀ h, x h ≤ r) ∧
      (∀ i, r ≤ ∑ h, a h * A i h) := by
  classical
  have hnonempty : (stdSimplex ℝ H).Nonempty := by
    obtain ⟨h⟩ := ‹Nonempty H›
    exact ⟨Pi.single h 1, single_mem_stdSimplex ℝ h⟩
  obtain ⟨a, ha, hamax⟩ := (isCompact_stdSimplex H).exists_isMaxOn hnonempty
    (best_response_continuous A).continuousOn
  let r := bestResponseCost A a
  have hdual : ∀ b : H → ℝ, (∀ h, 0 ≤ b h) → (∑ h, b h) = 1 →
      ∃ i, (∑ h, b h * A i h) ≤ r := by
    intro b hb hbsum
    have hbmax : bestResponseCost A b ≤ r := hamax ⟨hb, hbsum⟩
    obtain ⟨i, hi, hieq⟩ := Finset.exists_mem_eq_inf' Finset.univ_nonempty
      (fun i => ∑ h, b h * A i h)
    exact ⟨i, hieq ▸ hbmax⟩
  obtain ⟨x, hx, hxr⟩ := (hull_feasible_iff_dual A r).mpr hdual
  refine ⟨a, x, r, ha, hx, hxr, ?_⟩
  intro i
  exact Finset.inf'_le _ (Finset.mem_univ i)

/-- Affine independence becomes linear independence on a nonzero level
of a linear functional; this is the dimension saving from n+1 to n. -/
theorem independent_on_positive_level {H J : Type*} [Fintype H] [Fintype J]
    (z : J → H → ℝ) (a : H → ℝ) (c : ℝ) (hc : 0 < c)
    (hind : AffineIndependent ℝ z) (hz : ∀ j, ∑ h, a h * z j h = c) :
    LinearIndependent ℝ z := by
  classical
  apply Fintype.linearIndependent_iff.mpr
  intro w hw
  have hscore : (∑ j, w j) * c = 0 := by
    calc
      _ = ∑ j, w j * (∑ h, a h * z j h) := by simp only [hz, Finset.sum_mul]
      _ = ∑ h, a h * (∑ j, w j • z j) h := by
        simp only [Finset.mul_sum, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
        rw [Finset.sum_comm]
        apply Finset.sum_congr rfl
        intro h hh
        apply Finset.sum_congr rfl
        intro j hj
        ring
      _ = 0 := by simp only [hw, Pi.zero_apply, mul_zero, Finset.sum_const_zero]
  have hwsum : ∑ j, w j = 0 := (mul_eq_zero.mp hscore).resolve_right (ne_of_gt hc)
  exact fun j => hind.eq_zero_of_sum_eq_zero hwsum hw j (Finset.mem_univ j)

/-- An attained positive finite-game value has a mixture with at most n
columns.  Positivity holds for nontrivial legal identification problems. -/
theorem compressed_saddle {H : Type u} {I : Type v} [Fintype H] [Fintype I]
    [Nonempty H] [Nonempty I] (A : I → H → ℝ)
    (hpositive : ∀ i h, 1 ≤ A i h) :
    ∃ (J : Type u) (_ : Fintype J) (choice : J → I) (w : J → ℝ) (r : ℝ),
      Fintype.card J ≤ Fintype.card H ∧ (∀ j, 0 < w j) ∧ (∑ j, w j) = 1 ∧
      (∀ h, (∑ j, w j * A (choice j) h) ≤ r) ∧
      (∀ p : H → ℝ, (∀ h, 0 ≤ p h) → (∑ h, p h) = 1 →
        ∃ i, (∑ h, p h * A i h) ≤ r) ∧
      (∃ a : H → ℝ, a ∈ stdSimplex ℝ H ∧ ∀ i, r ≤ ∑ h, a h * A i h) := by
  classical
  obtain ⟨a, x, r, ha, hx, hxr, hdual⟩ := attained_saddle A
  have hr : 0 < r := by
    obtain ⟨i, hi⟩ := (hull_feasible_iff_dual A r).mp ⟨x, hx, hxr⟩ a ha.1 ha.2
    have hb : 1 ≤ ∑ h, a h * A i h := by
      calc
        1 = ∑ h, a h * 1 := by simp only [mul_one, ha.2]
        _ ≤ _ := Finset.sum_le_sum fun h _ =>
          mul_le_mul_of_nonneg_left (hpositive i h) (ha.1 h)
    linarith
  obtain ⟨J, instJ, z, w, hzrange, hind, hw, hwsum, hsum⟩ :=
    eq_pos_convex_span_of_mem_convexHull hx
  letI := instJ
  let choice : J → I := fun j => Classical.choose (hzrange (Set.mem_range_self j))
  have hz : ∀ j, A (choice j) = z j := fun j =>
    Classical.choose_spec (hzrange (Set.mem_range_self j))
  have hlower : ∀ j, r ≤ ∑ h, a h * z j h := by
    intro j
    rw [← hz j]
    exact hdual (choice j)
  have havg : (∑ j, w j * (∑ h, a h * z j h)) ≤ r := by
    have he : (∑ j, w j * (∑ h, a h * z j h)) = ∑ h, a h * x h := by
      rw [← hsum]
      simp only [Finset.mul_sum, Finset.sum_apply, Pi.smul_apply, smul_eq_mul]
      rw [Finset.sum_comm]
      apply Finset.sum_congr rfl
      intro h hh
      apply Finset.sum_congr rfl
      intro j hj
      ring
    rw [he]
    exact finite_mixture_bound a x r ha.1 ha.2 hxr
  have hzero : ∑ j, w j * ((∑ h, a h * z j h) - r) = 0 := by
    have hnonneg : 0 ≤ ∑ j, w j * ((∑ h, a h * z j h) - r) :=
      Finset.sum_nonneg fun j _ => mul_nonneg (le_of_lt (hw j)) (sub_nonneg.mpr (hlower j))
    have he : (∑ j, w j * ((∑ h, a h * z j h) - r)) =
        (∑ j, w j * (∑ h, a h * z j h)) - r := by
      simp only [mul_sub, Finset.sum_sub_distrib, ← Finset.sum_mul, hwsum, one_mul]
    rw [he] at hnonneg ⊢
    linarith
  have hlevel : ∀ j, (∑ h, a h * z j h) = r := by
    have hz0 := (Finset.sum_eq_zero_iff_of_nonneg (fun j _ =>
      mul_nonneg (le_of_lt (hw j)) (sub_nonneg.mpr (hlower j)))).mp hzero
    intro j
    exact sub_eq_zero.mp ((mul_eq_zero.mp (hz0 j (Finset.mem_univ j))).resolve_left
      (ne_of_gt (hw j)))
  have hlin := independent_on_positive_level z a r hr hind hlevel
  have hcard : Fintype.card J ≤ Fintype.card H := by
    simpa only [Module.finrank_pi, Module.finrank_self, Finset.sum_const,
      Finset.card_univ, nsmul_eq_mul, mul_one] using hlin.fintype_card_le_finrank
  refine ⟨J, instJ, choice, w, r, hcard, hw, hwsum, ?_, ?_, ⟨a, ha, hdual⟩⟩
  · intro h
    have he := congrArg (fun y : H → ℝ => y h) hsum
    have hxv : (∑ j, w j * A (choice j) h) = x h := by
      simpa only [hz, Finset.sum_apply, Pi.smul_apply, smul_eq_mul] using he
    exact hxv ▸ hxr h
  · exact (hull_feasible_iff_dual A r).mp ⟨x, hx, hxr⟩

theorem legal_depth_positive {H Q : Type*} [Fintype H] [DecidableEq H]
    (M : QuerySystem H Q) (T : Tree H Q) (hcard : 2 ≤ Fintype.card H)
    (hlegal : Tree.Identifies M Finset.univ T) (h : H) : 1 ≤ Tree.depth M T h := by
  cases T with
  | leaf label =>
    have hc := Tree.identification_capacity M Finset.univ (Tree.leaf label) hlegal
    simp only [Finset.card_univ, Tree.height, pow_zero] at hc
    omega
  | node q miss hit => exact Nat.le_add_right 1 _

/-- The restricted master LP's optimal support bound for an actual finite
family of legal trees, with optimality against every mixture of that family. -/
theorem compressed_legal_tree_game {H : Type u} {Q I : Type*}
    [Fintype H] [Fintype I] [Nonempty H] [Nonempty I] [DecidableEq H]
    (M : QuerySystem H Q) (trees : I → Tree H Q) (hcard : 2 ≤ Fintype.card H)
    (hlegal : ∀ i, Tree.Identifies M Finset.univ (trees i)) :
    ∃ (J : Type u) (_ : Fintype J) (choice : J → I) (w : J → ℝ) (r : ℝ),
      Fintype.card J ≤ Fintype.card H ∧
      LegalMixture M Finset.univ (fun j => trees (choice j)) w ∧
      RandomizedHeightAtMost M (fun j => trees (choice j)) w r ∧
      (∀ (K : Type*) (_ : Fintype K) (other : K → I) (probability : K → ℝ) (b : ℝ),
        LegalMixture M Finset.univ (fun k => trees (other k)) probability →
        RandomizedHeightAtMost M (fun k => trees (other k)) probability b → r ≤ b) := by
  classical
  let A : I → H → ℝ := fun i h => (Tree.depth M (trees i) h : ℝ)
  have hpositive : ∀ i h, 1 ≤ A i h := fun i h =>
    Nat.one_le_cast.mpr (legal_depth_positive M (trees i) hcard (hlegal i) h)
  obtain ⟨J, instJ, choice, w, r, hJ, hw, hwsum, hbound, _, a, ha, hdual⟩ :=
    compressed_saddle A hpositive
  letI := instJ
  refine ⟨J, instJ, choice, w, r, hJ,
    ⟨fun j => le_of_lt (hw j), hwsum, fun j _ => hlegal (choice j)⟩, hbound, ?_⟩
  intro K instK other probability b hmix hb
  letI := instK
  exact randomized_tree_weak_duality M (fun k => trees (other k)) probability a r b
    hmix.1 hmix.2.1 ha.1 ha.2 hb (fun k => hdual (other k))

noncomputable def legalCatalog {H Q : Type*} [Fintype H] [Fintype Q]
    [DecidableEq H] [DecidableEq Q] (M : QuerySystem H Q) : Finset (Tree H Q) := by
  classical
  exact (Tree.catalog (Fintype.card H - 1)).filter (Tree.Identifies M Finset.univ)

theorem restriction_mem_legal_catalog {H Q : Type*} [Fintype H] [Fintype Q]
    [Nonempty H] [DecidableEq H] [DecidableEq Q]
    (M : QuerySystem H Q) (T : Tree H Q) (hlegal : Tree.Identifies M Finset.univ T) :
    Tree.restrict M T Finset.univ ∈ legalCatalog M := by
  classical
  apply Finset.mem_filter.mpr
  constructor
  · apply Tree.catalog_complete
    simpa using (Tree.restricted_height_le_card_pred M T Finset.univ Finset.univ_nonempty)
  · exact Tree.restriction_identifies M T Finset.univ Finset.univ (fun _ hh => hh) hlegal

/-- Strong duality, attainment, and support≤n for the entire supplied-query
tree problem.  Completeness of the proper-tree catalog extends the optimal
dual prior to every legal tree, including trees outside that finite catalog. -/
theorem full_legal_tree_saddle {H : Type u} {Q : Type*}
    [Fintype H] [Fintype Q] [Nonempty H] [DecidableEq H] [DecidableEq Q]
    (M : QuerySystem H Q) (hcard : 2 ≤ Fintype.card H)
    (hfeasible : ∃ T : Tree H Q, Tree.Identifies M Finset.univ T) :
    ∃ (J : Type u) (_ : Fintype J) (trees : J → Tree H Q) (w : J → ℝ)
      (a : H → ℝ) (r : ℝ),
      Fintype.card J ≤ Fintype.card H ∧ LegalMixture M Finset.univ trees w ∧
      (∀ j, Tree.height (trees j) ≤ Fintype.card H - 1) ∧
      RandomizedHeightAtMost M trees w r ∧ a ∈ stdSimplex ℝ H ∧
      (∀ T : Tree H Q, Tree.Identifies M Finset.univ T →
        r ≤ ∑ h, a h * (Tree.depth M T h : ℝ)) ∧
      (∀ (K : Type*) (_ : Fintype K) (other : K → Tree H Q)
        (probability : K → ℝ) (b : ℝ),
        LegalMixture M Finset.univ other probability →
        RandomizedHeightAtMost M other probability b → r ≤ b) := by
  classical
  let I := ↥(legalCatalog M)
  haveI : Nonempty I := by
    obtain ⟨T, hT⟩ := hfeasible
    exact ⟨⟨Tree.restrict M T Finset.univ, restriction_mem_legal_catalog M T hT⟩⟩
  let A : I → H → ℝ := fun i h => (Tree.depth M i h : ℝ)
  have hlegal : ∀ i : I, Tree.Identifies M Finset.univ i := fun i =>
    (Finset.mem_filter.mp i.property).2
  have hpositive : ∀ i h, 1 ≤ A i h := fun i h =>
    Nat.one_le_cast.mpr (legal_depth_positive M i hcard (hlegal i) h)
  obtain ⟨J, instJ, choice, w, r, hJ, hw, hwsum, hbound, _, a, ha, hdual⟩ :=
    compressed_saddle A hpositive
  letI := instJ
  let trees : J → Tree H Q := fun j => choice j
  have hfulldual : ∀ T : Tree H Q, Tree.Identifies M Finset.univ T →
      r ≤ ∑ h, a h * (Tree.depth M T h : ℝ) := by
    intro T hT
    let i : I := ⟨Tree.restrict M T Finset.univ, restriction_mem_legal_catalog M T hT⟩
    calc
      r ≤ ∑ h, a h * (Tree.depth M (Tree.restrict M T Finset.univ) h : ℝ) := hdual i
      _ ≤ _ := Finset.sum_le_sum fun h _ =>
        mul_le_mul_of_nonneg_left (Nat.cast_le.mpr
          (Tree.restriction_preserves M T Finset.univ h (Finset.mem_univ h)).2) (ha.1 h)
  refine ⟨J, instJ, trees, w, a, r, hJ,
    ⟨fun j => le_of_lt (hw j), hwsum, fun j _ => hlegal (choice j)⟩,
    ?_, hbound, ha, hfulldual, ?_⟩
  · intro j
    exact Tree.catalog_sound (trees j) _ (Finset.mem_filter.mp (choice j).property).1
  · intro K instK other probability b hmix hb
    letI := instK
    obtain ⟨T, hT⟩ := hfeasible
    let adjusted : K → Tree H Q := fun k => if 0 < probability k then other k else T
    have hadjusted : ∀ k, Tree.Identifies M Finset.univ (adjusted k) := by
      intro k
      by_cases hk : 0 < probability k
      · simpa only [adjusted, if_pos hk] using hmix.2.2 k hk
      · simpa only [adjusted, if_neg hk] using hT
    have he : ∀ h, randomizedDepth M adjusted probability h =
        randomizedDepth M other probability h := by
      intro h
      apply Finset.sum_congr rfl
      intro k hkMem
      by_cases hk : 0 < probability k
      · simp only [adjusted, if_pos hk]
      · have hpzero : probability k = 0 := le_antisymm (le_of_not_gt hk) (hmix.1 k)
        simp only [hpzero, zero_mul]
    have habound : RandomizedHeightAtMost M adjusted probability b := fun h => he h ▸ hb h
    exact randomized_tree_weak_duality M adjusted probability a r b
      hmix.1 hmix.2.1 ha.1 ha.2 habound (fun k => hfulldual (adjusted k) (hadjusted k))

end
end FiniteGame
end PlanarQuery
