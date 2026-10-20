import Mathlib.Data.List.Basic
import Lean.Elab.Tactic.Omega

/-!
# Cardinality of a 3-Partition bin

This file records the elementary numerical fact used in the strong
3-Partition reduction.  Items are listed with multiplicity, so two items
may have the same weight.
-/

namespace PlanarQuery
namespace ThreePartitionBounds

/-- Summing the strict lower item bound gives a weak aggregate bound. -/
theorem lower_sum_bound (B : Nat) :
    ∀ xs : List Nat, (∀ a ∈ xs, B < 4 * a) →
      xs.length * B ≤ 4 * xs.sum := by
  intro xs
  induction xs with
  | nil =>
      intro _
      simp
  | cons a xs ih =>
      intro h
      have ha : B < 4 * a := h a (by simp)
      have htail : ∀ x ∈ xs, B < 4 * x := by
        intro x hx
        exact h x (by simp [hx])
      have ht := ih htail
      simp only [List.length_cons, List.sum_cons, Nat.add_mul, Nat.mul_add]
      omega

/-- Summing the strict lower item bound is strict whenever the list has an
item. -/
theorem lower_sum_strict (B : Nat) (xs : List Nat) (hne : xs ≠ [])
    (h : ∀ a ∈ xs, B < 4 * a) :
    xs.length * B < 4 * xs.sum := by
  cases xs with
  | nil => contradiction
  | cons a xs =>
      have ha : B < 4 * a := h a (by simp)
      have htail : ∀ x ∈ xs, B < 4 * x := by
        intro x hx
        exact h x (by simp [hx])
      have ht := lower_sum_bound B xs htail
      simp only [List.length_cons, List.sum_cons, Nat.add_mul, Nat.mul_add]
      omega

/-- Summing the strict upper item bound gives a weak aggregate bound. -/
theorem upper_sum_bound (B : Nat) :
    ∀ xs : List Nat, (∀ a ∈ xs, 2 * a < B) →
      2 * xs.sum ≤ xs.length * B := by
  intro xs
  induction xs with
  | nil =>
      intro _
      simp
  | cons a xs ih =>
      intro h
      have ha : 2 * a < B := h a (by simp)
      have htail : ∀ x ∈ xs, 2 * x < B := by
        intro x hx
        exact h x (by simp [hx])
      have ht := ih htail
      simp only [List.length_cons, List.sum_cons, Nat.add_mul, Nat.mul_add]
      omega

/-- Summing the strict upper item bound is strict whenever the list has an
item. -/
theorem upper_sum_strict (B : Nat) (xs : List Nat) (hne : xs ≠ [])
    (h : ∀ a ∈ xs, 2 * a < B) :
    2 * xs.sum < xs.length * B := by
  cases xs with
  | nil => contradiction
  | cons a xs =>
      have ha : 2 * a < B := h a (by simp)
      have htail : ∀ x ∈ xs, 2 * x < B := by
        intro x hx
        exact h x (by simp [hx])
      have ht := upper_sum_bound B xs htail
      simp only [List.length_cons, List.sum_cons, Nat.add_mul, Nat.mul_add]
      omega

/-- If every item lies strictly between one quarter and one half of `B`,
then a list of such items with total weight `B` has exactly three entries.
The list formulation preserves multiplicity, as required for partition
items that can have equal numerical weights. -/
theorem length_eq_three_of_sum_eq (B : Nat) (xs : List Nat)
    (hB : 0 < B) (hsum : xs.sum = B)
    (hlower : ∀ a ∈ xs, B < 4 * a)
    (hupper : ∀ a ∈ xs, 2 * a < B) :
    xs.length = 3 := by
  have hne : xs ≠ [] := by
    intro hnil
    simp [hnil] at hsum
    omega
  have hlo := lower_sum_strict B xs hne hlower
  have hhi := upper_sum_strict B xs hne hupper
  rw [hsum] at hlo hhi
  have hlenlt : xs.length < 4 := by
    exact (Nat.mul_lt_mul_right hB).1 hlo
  have hlen_gt : 2 < xs.length := by
    exact (Nat.mul_lt_mul_right hB).1 hhi
  omega

end ThreePartitionBounds
end PlanarQuery
