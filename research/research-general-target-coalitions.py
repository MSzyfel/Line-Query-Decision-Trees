"""Target-only completion costs: finite exact audits and symbolic LP gaps.

The subset optimizers below are validation oracles, not a proposed general
polynomial decision-tree approximation.  Large gap rows are symbolic bounds;
their exponentially large-in-r explicit matrices are not materialized.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path
import json
import random


def cover_number(n_targets, caps, wanted):
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        return 1 + min(solve(remaining & ~cap) for cap in caps
                       if cap & remaining)
    return solve(wanted)


def compressed_cost(n_targets, caps, outsiders, wanted):
    """Exact Bellman DP, exploiting exchangeable outside singleton tests."""
    full_targets = (1 << n_targets)-1
    target_tests = tuple(sorted(set(caps) | {1 << h for h in range(n_targets)}))

    @lru_cache(None)
    def solve(targets, live_outsiders):
        population = targets.bit_count() + live_outsiders
        if not (targets & wanted) or population <= 1:
            return 0
        candidates = []
        for test in target_tests:
            hit = targets & test
            if hit and hit.bit_count() < population:
                candidates.append(population + solve(hit, 0)
                                  + solve(targets ^ hit, live_outsiders))
        if live_outsiders:
            candidates.append(population + solve(targets, live_outsiders-1))
        return min(candidates)

    return solve(full_targets, outsiders)


def explicit_cost(n_targets, caps, outsiders, wanted):
    """Independent full-hypothesis-mask Bellman DP for small validation."""
    n = n_targets + outsiders
    tests = tuple(set(caps) | {1 << h for h in range(n)})

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1 or not (state & wanted):
            return 0
        return state.bit_count() + min(
            solve(state & test) + solve(state & ~test)
            for test in tests if state & test and state & ~test)

    return solve((1 << n)-1)


def cover_policy(n_targets, caps, outsiders, wanted):
    """An actual partial tree: a minimum cover spine and singleton exits."""
    full = (1 << (n_targets+outsiders))-1
    target_full = (1 << n_targets)-1

    @lru_cache(None)
    def choose(remaining):
        if not remaining:
            return 0, ()
        count, suffix, first = min(
            (choose(remaining & ~cap)[0], choose(remaining & ~cap)[1], cap)
            for cap in caps if cap & remaining)
        return count+1, (first,)+suffix

    sequence = choose(wanted)[1]

    def identify(state):
        if state.bit_count() <= 1:
            return state, None, None, None
        singleton = state & -state
        return state, singleton, identify(singleton), identify(state ^ singleton)

    def build(state, position):
        if position == len(sequence):
            return state, None, None, None
        hit = state & sequence[position]
        assert hit and state ^ hit
        assert not (hit & ~target_full)
        return state, sequence[position], identify(hit), build(state ^ hit, position+1)

    tree = build(full, 0)
    work, completed = 0, 0
    for h in range(n_targets+outsiders):
        bit, node, depth = 1 << h, tree, 0
        while node[1] is not None:
            node = node[2] if bit & node[1] else node[3]
            depth += 1
        assert node[0] & bit
        if node[0].bit_count() == 1:
            completed |= bit
        work += depth
    assert completed & wanted == wanted
    return work


def main():
    rng = random.Random(2026101805)
    exact_checks, bound_checks, execution_checks, pricing_checks = 0, 0, 0, 0
    for n_targets in range(2, 5):
        all_targets = (1 << n_targets)-1
        for _ in range(5):
            caps = tuple(sorted(set(rng.randrange(1, all_targets+1)
                                    for _ in range(4)) | {all_targets}))
            # Include less trivial covers too; the all-target cap may be removed.
            if rng.randrange(2):
                caps = tuple(sorted((set(caps)-{all_targets})
                                    | {1 << h for h in range(n_targets)}))
            outsiders = 2*n_targets
            coalition_costs = {}
            for wanted in range(1, all_targets+1):
                exact = compressed_cost(n_targets, caps, outsiders, wanted)
                coalition_costs[wanted] = exact
                assert exact == explicit_cost(n_targets, caps, outsiders, wanted)
                exact_checks += 1
                tau = cover_number(n_targets, caps, wanted)
                upper = cover_policy(n_targets, caps, outsiders, wanted)
                assert outsiders*tau <= exact <= upper <= outsiders*tau+2*n_targets**2
                bound_checks += 1
                execution_checks += 1
            for _ in range(8):
                prizes = [rng.randrange(9) for _ in range(n_targets)]
                reward = lambda state: sum(prizes[h] for h in range(n_targets)
                                            if state >> h & 1)
                best_cap = max(caps, key=lambda cap: (reward(cap), -cap.bit_count()))
                cap_reward = reward(best_cap)
                if not cap_reward:
                    continue
                exact_density = min(Fraction(cost, reward(wanted))
                                    for wanted, cost in coalition_costs.items()
                                    if reward(wanted))
                cap_size = best_cap.bit_count()
                cap_work = outsiders+n_targets+cap_size*(cap_size+1)//2-1
                candidate_density = Fraction(cap_work, cap_reward)
                assert Fraction(outsiders, cap_reward) <= exact_density <= candidate_density
                assert candidate_density <= (1+Fraction(n_targets**2, outsiders))*exact_density
                # The shared target/outside pair ledger has unit endpoint load.
                assert all(Fraction(reward(cap), cap_reward) <= 1 for cap in caps)
                assert all(Fraction(w, cap_reward) <= 1 for w in prizes)
                pricing_checks += 1

    triangle_rows = []
    for outsiders in (8, 16, 64, 128):
        n_targets, caps = 3, (3, 5, 6)
        full_cost = compressed_cost(n_targets, caps, outsiders, 7)
        cap_costs = [compressed_cost(n_targets, caps, outsiders, cap) for cap in caps]
        assert full_cost == 2*(outsiders+3)
        assert cap_costs == [outsiders+5]*3
        fractional_cover = Fraction(sum(cap_costs), 2)
        assert fractional_cover < full_cost
        triangle_rows.append({"outside_hypotheses": outsiders,
                              "cohort_exact_cost": full_cost,
                              "feasible_fractional_cover_cost": str(fractional_cover),
                              "certified_gap_at_least": str(Fraction(full_cost, fractional_cover))})

    # Independent finite combinatorial check of the central k-subset cover.
    explicit_cover_checks = 0
    for r in range(3, 7):
        k = r//2
        targets = list(combinations(range(r), k))
        for count in range(r+1):
            for selected in combinations(range(r), count):
                covered = all(set(a) & set(selected) for a in targets)
                assert covered == (count >= r-k+1)
                explicit_cover_checks += 1
        cap_size = comb(r-1, k-1)
        assert all(sum(i in a for i in range(r)) == k for a in targets)
        assert r*cap_size == k*len(targets)

    symbolic_rows = []
    for r in (4, 8, 12, 16, 24, 32, 64):
        k = r//2
        n_targets, cap_size = comb(r, k), comb(r-1, k-1)
        outsiders = n_targets**3
        tau = r-k+1
        singleton_exit_work = cap_size*(cap_size+1)//2-1
        one_cap_work = outsiders+n_targets+singleton_exit_work
        fractional_upper = Fraction(r*one_cap_work, k)
        lower = outsiders*tau
        ratio = Fraction(lower, fractional_upper)
        assert outsiders >= 2*n_targets
        assert ratio >= Fraction(k*tau, 2*r)  # A deliberately loose asymptotic check.
        symbolic_rows.append({"r": r, "k": k, "target_count": n_targets,
                              "outside_count": outsiders,
                              "full_cohort_cost_lower": lower,
                              "fractional_cover_upper": str(fractional_upper),
                              "gap_lower": str(ratio), "gap_lower_float": float(ratio),
                              "symbolic_bounds_only": True})

    result = {"status": "passed", "independent_exact_cost_checks": exact_checks,
              "set_cover_sandwich_checks": bound_checks,
              "actual_cover_policy_execution_checks": execution_checks,
              "exact_target_only_weighted_pricing_checks": pricing_checks,
              "central_cover_combinatorial_checks": explicit_cover_checks,
              "triangle_exact_examples": triangle_rows, "asymptotic_family_bounds": symbolic_rows,
              "exponential_dp_is_validation_only": True,
              "no_unrestricted_approximation_claim": True}
    Path("research-general-target-coalitions-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
