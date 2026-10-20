import Mathlib

/-!
The geometric part of the batch-phase schedule-length estimate.  This file
formalizes the arithmetic bound from Claim `clm:batch-phase-cover`; the
coverage comparison with the greedy interval schedule is separate.
-/

namespace PlanarQuery.BatchPhaseLength

private theorem geom_sum_mul_sub_one (beta : Real) (n : Nat) :
    (Finset.range n).sum (fun j => beta ^ j) * (beta - 1) = beta ^ n - 1 := by
  induction n with
  | zero => simp
  | succ n ih =>
      simp only [Finset.sum_range_succ]
      calc
        ((Finset.range n).sum (fun j => beta ^ j) + beta ^ n) * (beta - 1)
            = (Finset.range n).sum (fun j => beta ^ j) * (beta - 1)
                + beta ^ n * (beta - 1) := by ring
        _ = (beta ^ n - 1) + beta ^ n * (beta - 1) := by rw [ih]
        _ = beta ^ (n + 1) - 1 := by rw [pow_succ]; ring

/-- The number of queries in phases before the first budget reaching `k0`,
plus the final `k0`-query phase, is bounded by the geometric factor stated in
Claim `clm:batch-phase-cover`.

`hfirst` records that every earlier integer budget is strictly below `k0`;
`hfinal` records that phase `J` has reached the threshold. -/
theorem schedule_length_geometric_bound
    (u beta : Real) (k0 J : Nat)
    (hu : 1 <= u) (hbeta : 1 < beta)
    (hfirst : forall j : Nat, j < J -> Nat.floor (beta ^ j * u) < k0) :
    ((Finset.range J).sum (fun j => Nat.floor (beta ^ j * u)) : Real) + k0
      <= (1 + beta / (beta - 1)) * k0 := by
  have hbeta0 : 0 < beta := by linarith
  have hu0 : 0 < u := by linarith
  have hden : 0 < beta - 1 := by linarith
  have hfloor_le (j : Nat) :
      (Nat.floor (beta ^ j * u) : Real) <= beta ^ j * u := by
    apply Nat.floor_le
    exact mul_nonneg (le_of_lt (pow_pos hbeta0 _)) (le_of_lt hu0)
  have hsum_floor :
      ((Finset.range J).sum (fun j => Nat.floor (beta ^ j * u)) : Real)
        <= u * (Finset.range J).sum (fun j => beta ^ j) := by
    calc
      (Finset.range J).sum (fun j => (Nat.floor (beta ^ j * u) : Real))
          <= (Finset.range J).sum (fun j => beta ^ j * u) :=
        Finset.sum_le_sum fun j hj => hfloor_le j
      _ = u * (Finset.range J).sum (fun j => beta ^ j) := by
        rw [← Finset.sum_mul]
        ring
  by_cases hJ : J = 0
  · subst J
    simp only [Finset.range_zero, Finset.sum_empty, Nat.cast_zero, zero_add]
    have hcoef : 1 <= 1 + beta / (beta - 1) := by
      have hpos : 0 <= beta / (beta - 1) := div_nonneg (le_of_lt hbeta0) (le_of_lt hden)
      linarith
    calc
      (k0 : Real) = 1 * k0 := by ring
      _ <= (1 + beta / (beta - 1)) * k0 :=
        mul_le_mul_of_nonneg_right hcoef (Nat.cast_nonneg k0)
  · have hJpos : 0 < J := Nat.pos_of_ne_zero hJ
    let n : Nat := J - 1
    have hn : n + 1 = J := by
      dsimp [n]
      omega
    have hprev : n < J := by omega
    have hprev_floor : Nat.floor (beta ^ n * u) < k0 := hfirst n hprev
    have hlast_real : beta ^ n * u < k0 := by
      apply (Nat.floor_lt (mul_nonneg (le_of_lt (pow_pos hbeta0 _)) (le_of_lt hu0))).mp
      simpa [Nat.cast_ofNat] using hprev_floor
    have hgeom := geom_sum_mul_sub_one beta J
    have hgeom_bound :
        (Finset.range J).sum (fun j => beta ^ j)
          <= beta * beta ^ n / (beta - 1) := by
      rw [le_div_iff₀ hden]
      rw [← hn] at hgeom
      rw [← hn]
      rw [hgeom, pow_succ]
      nlinarith [pow_pos hbeta0 n]
    have hpre_bound :
        u * (Finset.range J).sum (fun j => beta ^ j)
          <= beta / (beta - 1) * k0 := by
      calc
        u * (Finset.range J).sum (fun j => beta ^ j)
            <= u * (beta * beta ^ n / (beta - 1)) :=
          mul_le_mul_of_nonneg_left hgeom_bound (le_of_lt hu0)
        _ = (beta / (beta - 1)) * (beta ^ n * u) := by ring
        _ <= (beta / (beta - 1)) * k0 :=
          mul_le_mul_of_nonneg_left (le_of_lt hlast_real)
            (div_nonneg (le_of_lt hbeta0) (le_of_lt hden))
    calc
      ((Finset.range J).sum (fun j => Nat.floor (beta ^ j * u)) : Real) + k0
          <= u * (Finset.range J).sum (fun j => beta ^ j) + k0 := by
            exact add_le_add_right hsum_floor _
      _ <= beta / (beta - 1) * k0 + k0 := add_le_add_right hpre_bound _
      _ = (1 + beta / (beta - 1)) * k0 := by ring

end PlanarQuery.BatchPhaseLength
