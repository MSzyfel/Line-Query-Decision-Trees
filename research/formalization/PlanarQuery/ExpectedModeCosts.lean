import Mathlib

/-!
The integer route allowances and weighted mode-saving identities from
Claim `clm:expected-mode-costs`.  The entropy terms and the geometric facts
that justify the route-count premises are handled separately in the article.
-/

namespace PlanarQuery.ExpectedModeCosts

/-- If at most `2(k-1)` tests precede the hit, the first-positive stop route,
with one discovery query and two endpoint codes of overhead at most two each,
uses at most `2k+3` nonentropy queries. -/
theorem stop_first_positive_allowance (k preceding : Nat) (hk : 1 ≤ k)
    (hpreceding : preceding ≤ 2 * (k - 1)) :
    preceding + 1 + 2 * 2 ≤ 2 * k + 3 := by
  omega

/-- If at most `2(k-1)` tests precede the hit, the second-positive stop route,
with two discovery queries and one endpoint code of overhead at most two,
uses at most `2k+2` nonentropy queries. -/
theorem stop_second_positive_allowance (k preceding : Nat) (hk : 1 ≤ k)
    (hpreceding : preceding ≤ 2 * (k - 1)) :
    preceding + 2 + 2 ≤ 2 * k + 2 := by
  omega

/-- The exclusive route in query-both mode has the same count: two discovery
queries and one endpoint code, after at most `2(k-1)` preceding tests. -/
theorem both_exclusive_allowance (k preceding : Nat) (hk : 1 ≤ k)
    (hpreceding : preceding ≤ 2 * (k - 1)) :
    preceding + 2 + 2 ≤ 2 * k + 2 := by
  omega

/-- The shared route in query-both mode uses two discovery queries and two
endpoint codes, after at most `2(k-1)` preceding tests. -/
theorem both_shared_allowance (k preceding : Nat) (hk : 1 ≤ k)
    (hpreceding : preceding ≤ 2 * (k - 1)) :
    preceding + 2 + 2 * 2 ≤ 2 * k + 4 := by
  omega

/-- The weighted stop-mode allowance equals the common allowance
`(2k+3)(x+y+z)` less the saving `y`. -/
theorem stop_weighted_saving (k : Nat) (x y z : Real)
    (_hx : 0 ≤ x) (_hy : 0 ≤ y) (_hz : 0 ≤ z) :
    (x + z) * (2 * (k : Real) + 3) + y * (2 * (k : Real) + 2)
      = (2 * (k : Real) + 3) * (x + y + z) - y := by
  ring

/-- The weighted query-both allowance equals the common allowance
`(2k+3)(x+y+z)` less the saving `x+y-z`. -/
theorem both_weighted_saving (k : Nat) (x y z : Real)
    (_hx : 0 ≤ x) (_hy : 0 ≤ y) (_hz : 0 ≤ z) :
    (x + y) * (2 * (k : Real) + 2) + z * (2 * (k : Real) + 4)
      = (2 * (k : Real) + 3) * (x + y + z) - (x + y - z) := by
  ring

end PlanarQuery.ExpectedModeCosts
