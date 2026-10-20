import Mathlib

/-!
The finite discrete estimate used for first-cover charges.  The hit-mass
equation remains an explicit premise in `first_cover_bound`.
-/

namespace PlanarQuery.BatchFirstCover

theorem weighted_rank_le_average (m : Nat) (g : Fin (m + 1) -> Real)
    (hmono : forall i j, i <= j -> g j <= g i) :
    (Finset.univ.sum fun i : Fin (m + 1) => (i.val + 1 : Nat) * g i) <=
      ((m + 2 : Nat) : Real) / 2 *
        (Finset.univ.sum fun i : Fin (m + 1) => g i) := by
  classical
  let c : Fin (m + 1) -> Real := fun i => 2 * (i.val : Real) - (m : Real)
  have hterm (i : Fin (m + 1)) : c i * (g i - g i.rev) <= 0 := by
    dsimp [c]
    by_cases hi : i <= i.rev
    · have hg := hmono i i.rev hi
      have hv : i.val + i.rev.val = m := Fin.add_rev_cast i
      have hc : 2 * (i.val : Real) - (m : Real) <= 0 := by
        have hv' : 2 * i.val <= m := by omega
        have hvR : 2 * (i.val : Real) <= (m : Real) := by
          exact_mod_cast hv'
        change 2 * (i.val : Real) - (m : Real) <= 0
        exact sub_nonpos.mpr hvR
      exact mul_nonpos_of_nonpos_of_nonneg hc (sub_nonneg.mpr hg)
    · have hi' : i.rev <= i := (Fin.le_total _ _).resolve_left hi
      have hg := hmono i.rev i hi'
      have hv : i.val + i.rev.val = m := Fin.add_rev_cast i
      have hc : 0 <= 2 * (i.val : Real) - (m : Real) := by
        have hv' : m <= 2 * i.val := by omega
        have hvR : (m : Real) <= 2 * (i.val : Real) := by
          exact_mod_cast hv'
        exact sub_nonneg.mpr hvR
      exact mul_nonpos_of_nonneg_of_nonpos hc (sub_nonpos.mpr hg)
  have hsum :
      (Finset.univ.sum fun i : Fin (m + 1) => c i * (g i - g i.rev)) <= 0 :=
    Finset.sum_nonpos fun i hi => hterm i
  have hrev :
      (Finset.univ.sum fun i : Fin (m + 1) => c i * g i.rev) =
        -(Finset.univ.sum fun i : Fin (m + 1) => c i * g i) := by
    calc
      (Finset.univ.sum fun i : Fin (m + 1) => c i * g i.rev) =
          Finset.univ.sum (fun i : Fin (m + 1) => c i.rev * g i) := by
            rw [← Equiv.sum_comp (Fin.revPerm (n := m + 1))
              (fun i : Fin (m + 1) => c i.rev * g i)]
            simp [Fin.rev_rev]
      _ = -(Finset.univ.sum fun i : Fin (m + 1) => c i * g i) := by
        calc
          _ = Finset.univ.sum (fun i : Fin (m + 1) => -(c i * g i)) := by
            apply Finset.sum_congr rfl
            intro i hi
            have hc : c i.rev = -c i := by
              have hv : i.val + i.rev.val = m := Fin.add_rev_cast i
              have hvR : (i.val : Real) + (i.rev.val : Real) = (m : Real) := by
                exact_mod_cast hv
              change 2 * (i.rev.val : Real) - (m : Real) =
                -(2 * (i.val : Real) - (m : Real))
              linarith
            rw [hc]
            ring
          _ = _ := by simp
  have hcenter :
      2 * (Finset.univ.sum fun i : Fin (m + 1) => c i * g i) <= 0 := by
    simp_rw [mul_sub] at hsum
    rw [Finset.sum_sub_distrib, hrev] at hsum
    nlinarith
  have hcoeff (i : Fin (m + 1)) :
      c i = 2 * ((i.val + 1 : Nat) : Real) - (m + 2 : Real) := by
    dsimp [c]
    push_cast
    ring
  have hidentity :
      (Finset.univ.sum fun i : Fin (m + 1) => c i * g i) =
        2 * (Finset.univ.sum fun i : Fin (m + 1) => (i.val + 1 : Nat) * g i) -
          (m + 2 : Real) * (Finset.univ.sum fun i : Fin (m + 1) => g i) := by
    calc
      _ = Finset.univ.sum (fun i : Fin (m + 1) =>
          (2 * ((i.val + 1 : Nat) : Real) - (m + 2 : Real)) * g i) := by
            apply Finset.sum_congr rfl
            intro i hi
            rw [hcoeff]
      _ = (Finset.univ.sum fun i : Fin (m + 1) =>
            2 * (((i.val + 1 : Nat) : Real) * g i)) -
          (Finset.univ.sum fun i : Fin (m + 1) => (m + 2 : Real) * g i) := by
            rw [show (fun i : Fin (m + 1) =>
              (2 * ((i.val + 1 : Nat) : Real) - (m + 2 : Real)) * g i) =
              (fun i => 2 * (((i.val + 1 : Nat) : Real) * g i) - (m + 2 : Real) * g i)
              from funext fun i => by ring]
            exact Finset.sum_sub_distrib
      _ = _ := by
        rw [← Finset.mul_sum, ← Finset.mul_sum]
  rw [hidentity] at hcenter
  rw [show ((m + 2 : Nat) : Real) / 2 *
      (Finset.univ.sum fun i : Fin (m + 1) => g i) =
        (((m + 2 : Nat) : Real) *
          (Finset.univ.sum fun i : Fin (m + 1) => g i)) / 2 by ring]
  rw [le_div_iff₀ (by norm_num : (0 : Real) < 2)]
  push_cast
  push_cast at hcenter
  nlinarith [hcenter]

theorem first_cover_bound (m : Nat) (g : Fin m -> Real) (r r' : Real)
    (hmono : forall i j, i <= j -> g j <= g i)
    (hmass : (Finset.univ.sum fun i : Fin m => g i) = r - r') :
    m * r' + (Finset.univ.sum fun i : Fin m => (i.val + 1 : Nat) * g i) <=
      ((m + 1 : Nat) : Real) / 2 * r + ((m - 1 : Int) : Real) / 2 * r' := by
  cases m with
  | zero => simp at hmass; linarith
  | succ n =>
      have h := weighted_rank_le_average n g hmono
      rw [hmass] at h
      push_cast at h ⊢
      nlinarith

end PlanarQuery.BatchFirstCover
