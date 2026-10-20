import Mathlib

/-!
Finite algebra for the expected-depth stage's two-mode accounting.
The selected mode attains the larger local score, while a query-both block's
information loss, measured in bits, pays its entropy credit.  Geometry and
the derivation of the global information-loss identity are explicit premises
handled elsewhere.
-/

namespace PlanarQuery.ExpectedCoarseningAccounting

noncomputable def blockScore (x y z credit : Real) : Real :=
  max y (x + y - z + credit)

def physicalSaving (both : Bool) (x y z : Real) : Real :=
  if both then x + y - z else y

def informationCredit (both : Bool) (loss : Real) : Real :=
  if both then loss else 0

/-- For either selected mode, the local score is paid by its physical saving
plus the information loss charged to query-both mode. -/
theorem block_score_paid {G : Type*} [Fintype G] [DecidableEq G]
    (both : G -> Bool) (x y z credit loss : G -> Real)
    (hselected : forall g,
      (if both g then x g + y g - z g + credit g else y g) =
        blockScore (x g) (y g) (z g) (credit g))
    (hcredit : forall g, both g = true -> credit g <= loss g) :
    (Finset.univ.sum fun g =>
      blockScore (x g) (y g) (z g) (credit g)) <=
    (Finset.univ.sum fun g =>
      physicalSaving (both g) (x g) (y g) (z g) +
        informationCredit (both g) (loss g)) := by
  classical
  apply Finset.sum_le_sum
  intro g hg
  cases hmode : both g with
  | false =>
      have hs := hselected g
      have hs' : y g = max (y g) (x g + y g - z g + credit g) := by
        simpa [blockScore, hmode] using hs
      simp [physicalSaving, informationCredit, hmode, blockScore]
      have hmax : max (y g) (x g + y g - z g + credit g) <= y g :=
        le_of_eq hs'.symm
      exact (max_le_iff.mp hmax).2
  | true =>
      have hs := hselected g
      simp [blockScore, hmode] at hs
      simp [physicalSaving, informationCredit, hmode]
      apply max_le
      · linarith [hs, hcredit g (by simp [hmode])]
      · linarith [hcredit g (by simp [hmode])]

/-- Summing the chosen mode costs and substituting the exact accumulated
merge loss yields the stage inequality.  `hmerge` is the entropy identity
for the coarsened transcript; this theorem supplies its algebraic use. -/
theorem stage_information_saving_bound {G : Type*} [Fintype G] [DecidableEq G]
    (both : G -> Bool) (x y z credit loss : G -> Real)
    (I Jactual Jcoarse lnTwo : Real)
    (hlnTwo : Ne lnTwo 0)
    (hselected : forall g,
      (if both g then x g + y g - z g + credit g else y g) =
        blockScore (x g) (y g) (z g) (credit g))
    (hcredit : forall g, both g = true -> credit g <= loss g)
    (hmerge : Jactual = Jcoarse + lnTwo *
      (Finset.univ.sum fun g => informationCredit (both g) (loss g))) :
    -(Finset.univ.sum fun g => physicalSaving (both g) (x g) (y g) (z g)) +
        (I - Jactual) / lnTwo <=
      (I - Jcoarse) / lnTwo -
        (Finset.univ.sum fun g => blockScore (x g) (y g) (z g) (credit g)) := by
  have hpaid := block_score_paid both x y z credit loss hselected hcredit
  have hinformation : (I - Jactual) / lnTwo =
      (I - Jcoarse) / lnTwo -
        (Finset.univ.sum fun g => informationCredit (both g) (loss g)) := by
    rw [hmerge]
    field_simp [hlnTwo]
    ring
  have hpaid' :
      (Finset.univ.sum fun g => blockScore (x g) (y g) (z g) (credit g)) <=
      (Finset.univ.sum fun g => physicalSaving (both g) (x g) (y g) (z g)) +
        (Finset.univ.sum fun g => informationCredit (both g) (loss g)) := by
    simpa only [Finset.sum_add_distrib] using hpaid
  rw [hinformation]
  linarith

end PlanarQuery.ExpectedCoarseningAccounting
