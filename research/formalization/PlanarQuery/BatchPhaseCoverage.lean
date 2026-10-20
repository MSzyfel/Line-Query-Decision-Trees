import Mathlib

/-!
Finite weighted coverage comparison used in the batch-phase argument.
The interval dynamic program and the schedule's phase-union construction
are separate premises; this module proves the residual-mass implication.
-/

namespace PlanarQuery.BatchPhaseCoverage

noncomputable def coveredMass {H Q : Type*} [Fintype H]
    (weight : H -> Real) (hits : Q -> H -> Prop) (queries : Finset Q) : Real := by
  classical
  exact Finset.univ.sum fun h =>
    if Exists fun q => q ∈ queries ∧ hits q h then weight h else 0

noncomputable def uncoveredMass {H Q : Type*} [Fintype H]
    (weight : H -> Real) (hits : Q -> H -> Prop) (queries : Finset Q) : Real := by
  classical
  exact Finset.univ.sum fun h =>
    if Exists fun q => q ∈ queries ∧ hits q h then 0 else weight h

theorem totalMass_eq_covered_add_uncovered {H Q : Type*} [Fintype H]
    (weight : H -> Real) (hits : Q -> H -> Prop) (queries : Finset Q) :
    (Finset.univ.sum fun h : H => weight h) =
      coveredMass weight hits queries + uncoveredMass weight hits queries := by
  classical
  unfold coveredMass uncoveredMass
  rw [← Finset.sum_add_distrib]
  apply Finset.sum_congr rfl
  intro h hh
  by_cases hhit : Exists fun q => q ∈ queries ∧ hits q h
  · simp [hhit]
  · simp [hhit]

/-- If a selected set maximizes covered mass among all query sets of size at
most `k`, then its residual mass is no larger than that of any feasible
comparison set. This is the exact set-cover inference used after a batch. -/
theorem maximum_coverage_residual_le {H Q : Type*} [Fintype H]
    (weight : H -> Real) (hits : Q -> H -> Prop)
    (selected comparison : Finset Q) (k : Nat)
    (hcomparison : comparison.card <= k)
    (hmax : forall candidate : Finset Q, candidate.card <= k ->
      coveredMass weight hits candidate <= coveredMass weight hits selected) :
    uncoveredMass weight hits selected <= uncoveredMass weight hits comparison := by
  have hselected := totalMass_eq_covered_add_uncovered weight hits selected
  have hcomparisonMass := totalMass_eq_covered_add_uncovered weight hits comparison
  have hcoverage := hmax comparison hcomparison
  linarith

/-- Adding phase queries that preserve every hit of the budget-optimal set
cannot leave more weight uncovered than the comparison prefix. This packages
the two logical steps used in the manuscript: schedule inclusion first, then
maximum coverage against the prefix. -/
theorem phase_residual_le_comparison {H Q : Type*} [Fintype H]
    (weight : H -> Real) (hits : Q -> H -> Prop)
    (selected phase comparison : Finset Q) (k : Nat)
    (hweight : forall h, 0 <= weight h)
    (hcomparison : comparison.card <= k)
    (hmax : forall candidate : Finset Q, candidate.card <= k ->
      coveredMass weight hits candidate <= coveredMass weight hits selected)
    (hphase : forall h, (Exists fun q => q ∈ selected ∧ hits q h) ->
      Exists fun q => q ∈ phase ∧ hits q h) :
    uncoveredMass weight hits phase <= uncoveredMass weight hits comparison := by
  classical
  have hphaseResidual : uncoveredMass weight hits phase <=
      uncoveredMass weight hits selected := by
    unfold uncoveredMass
    apply Finset.sum_le_sum
    intro h hh
    by_cases hs : Exists fun q => q ∈ selected ∧ hits q h
    · have hp : Exists fun q => q ∈ phase ∧ hits q h := hphase h hs
      simp [hs, hp]
    · by_cases hp : Exists fun q => q ∈ phase ∧ hits q h
      · simp [hs, hp, hweight h]
      · simp [hs, hp]
  exact hphaseResidual.trans
    (maximum_coverage_residual_le weight hits selected comparison k hcomparison hmax)

end PlanarQuery.BatchPhaseCoverage
