import PlanarQuery.Accounting
import Mathlib.Algebra.Order.BigOperators.Group.List
import Mathlib.Algebra.BigOperators.Ring.List

namespace PlanarQuery

/-- An arbitrary-arity recursive stage ledger. Its children are a list,
    so no artificial binary restriction or fixed branching bound is used. -/
inductive StageLedger where
  | leaf (potential entropy : ℝ)
  | stage (potential entropy localCost : ℝ) (children : List StageLedger)

namespace StageLedger

def potential : StageLedger → ℝ
  | .leaf p _ => p
  | .stage p _ _ _ => p

def entropy : StageLedger → ℝ
  | .leaf _ e => e
  | .stage _ e _ _ => e

def cost : StageLedger → ℝ
  | .leaf _ _ => 0
  | .stage _ _ stageCost children => stageCost + (children.map cost).sum

def LocalBound (A c : ℝ) : StageLedger → Prop
  | .leaf p e => p = 0 ∧ e = 0
  | .stage p e stageCost children =>
      stageCost ≤ A * (p - (children.map potential).sum) +
        c * (e - (children.map entropy).sum) ∧
      ∀ child ∈ children, LocalBound A c child

/-- Local invoices imply the complete global bound for arbitrary-arity
    recursive partitions. The entire combination is proved by induction;
    the caller must establish its own stage invoices and zero leaf values. -/
theorem local_to_global (T : StageLedger) (A c : ℝ) (h : LocalBound A c T) :
    cost T ≤ A * potential T + c * entropy T := by
  cases hT : T with
  | leaf p e =>
    rw [hT] at h
    simp only [LocalBound] at h
    simp [cost, potential, entropy, h.1, h.2]
  | stage p e stageCost children =>
    rw [hT] at h
    simp only [LocalBound] at h
    have hchildren : (children.map cost).sum ≤
        (children.map (fun child => A * potential child + c * entropy child)).sum := by
      apply List.sum_le_sum
      intro child hc
      exact local_to_global child A c (h.2 child hc)
    have hsum :
        (children.map (fun child => A * potential child + c * entropy child)).sum =
        A * (children.map potential).sum + c * (children.map entropy).sum := by
      clear h hchildren hT
      induction children with
      | nil => simp
      | cons child rest ih => simp only [List.map_cons, List.sum_cons, ih]; ring
    rw [hsum] at hchildren
    simp only [cost, potential, entropy]
    nlinarith [h.1]
termination_by sizeOf T
decreasing_by
  rw [hT]
  have hs := List.sizeOf_lt_of_mem hc
  simp only [StageLedger.stage.sizeOf_spec]
  omega

end StageLedger
end PlanarQuery
