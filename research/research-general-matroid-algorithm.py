"""Exact uniform-matroid query algorithms and a rank-certificate obstruction."""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from math import comb
from pathlib import Path
import json


def first_bits(mask, count):
    result = 0
    for _ in range(count):
        assert mask
        bit = mask & -mask
        result |= bit
        mask ^= bit
    return result


def cardinality_dp(n, k, all_flats=False):
    assert 1 <= k < n
    costs, choices = [0] * (n+1), {}
    for size in range(2, n+1):
        lower = 1 if all_flats else max(1, k-(n-size))
        upper = min(k, size-1)
        value, chosen = min((costs[a]+costs[size-a], a)
                            for a in range(lower, upper+1))
        costs[size], choices[size] = size+value, chosen
    return costs, choices


@dataclass
class Node:
    state: int
    test: int | None = None
    positive: "Node | None" = None
    negative: "Node | None" = None


def reconstruct(n, k, choices, tests, all_flats=False):
    full = (1 << n)-1
    assert recognize(n, k, tests, all_flats)
    # A desired response cell can be supplied as either response of a test.
    # Keep the actual test identifier and record its orientation explicitly.
    descriptions = {}
    for test in sorted(tests):
        descriptions.setdefault(test, (test, False))
        descriptions.setdefault(full ^ test, (test, True))
    def build(state):
        size = state.bit_count()
        if size <= 1:
            return Node(state)
        a = choices[size]
        positive = first_bits(state, a)
        padding = 0 if all_flats else first_bits(full ^ state, k-a)
        desired_cell = positive | padding
        assert 1 <= desired_cell.bit_count() <= k if all_flats else desired_cell.bit_count() == k
        assert state & desired_cell == positive
        test, reversed_description = descriptions[desired_cell]
        yes, no = build(positive), build(state ^ positive)
        if reversed_description:
            yes, no = no, yes
        return Node(state, test, yes, no)
    return build(full)


def execute(n, root, tests):
    total, internal = 0, 0
    pending = [root]
    while pending:
        node = pending.pop()
        if node.test is not None:
            assert node.test in tests
            assert node.positive.state == node.state & node.test
            assert node.negative.state == node.state & ~node.test
            assert node.positive.state | node.negative.state == node.state
            assert not node.positive.state & node.negative.state
            pending.extend((node.positive, node.negative))
            internal += 1
    for h in range(n):
        node, bit = root, 1 << h
        while node.test is not None:
            node = node.positive if node.test & bit else node.negative
            total += 1
        assert node.state == bit
    assert internal == n-1
    return total


def supplied_queries(n, k, all_flats=False):
    sizes = range(1, k+1) if all_flats else [k]
    return {sum(1 << h for h in selected)
            for size in sizes for selected in combinations(range(n), size)}


def recognize(n, k, tests, all_flats=False):
    full = (1 << n)-1
    cells = set()
    for test in tests:
        if test & ~full:
            return False
        if not test or test == full:
            continue
        response = (test, full ^ test)
        legal = [cell for cell in response
                 if 1 <= cell.bit_count() <= k] if all_flats else [
                     cell for cell in response if cell.bit_count() == k]
        if not legal:
            return False
        cells.update(legal)
    wanted = sum(comb(n, size) for size in range(1, k+1)) if all_flats else comb(n, k)
    return len(cells) == wanted


def independent_exact_cost(n, tests):
    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        return state.bit_count() + min(
            solve(state & test)+solve(state & ~test)
            for test in tests if state & test and state & ~test)
    return solve((1 << n)-1)


def pair_closed_form(n):
    m = n//2
    return m*m+3*m-2 if n % 2 == 0 else m*m+4*m


def old_budget_two_cost(n):
    # Existing abstract-code recurrence; this is a lower certificate,
    # not the new executable cardinality algorithm.
    row_one = [0] + [size*(size+1)//2-1 for size in range(1, n+1)]
    row_two = [0, 0] + [0]*(n-1)
    for size in range(2, n+1):
        row_two[size] = size + min(row_one[a]+row_two[size-a]
                                  for a in range(1, size))
    return row_two[n]


def main():
    cases = executions = descriptions_checked = 0
    for n in range(2, 9):
        for k in range(1, n):
            for all_flats in (False, True):
                tests = supplied_queries(n, k, all_flats)
                assert recognize(n, k, tests, all_flats)
                costs, choices = cardinality_dp(n, k, all_flats)
                assert costs[n] == independent_exact_cost(n, tests)
                full = (1 << n)-1
                complemented = {full ^ test for test in tests}
                mixed = {test if i % 2 else full ^ test
                         for i, test in enumerate(sorted(tests))}
                for descriptions in (tests, complemented, mixed):
                    assert recognize(n, k, descriptions, all_flats)
                    tree = reconstruct(n, k, choices, descriptions, all_flats)
                    assert execute(n, tree, descriptions) == costs[n]
                    descriptions_checked += 1
                    executions += n
                if k == 2:
                    assert costs[n] == pair_closed_form(n)
                cases += 1
    obstruction = []
    for n in (16, 64, 256, 1024):
        cost = cardinality_dp(n, 2)[0][n]
        assert cost == pair_closed_form(n)
        rank_lower = old_budget_two_cost(n)
        assert rank_lower <= cost
        obstruction.append({"n": n, "discovered_uniform_rank": 3,
                            "exact_pair_query_OPT": cost,
                            "old_rank_coding_lower": rank_lower,
                            "certificate_gap": str(Fraction(cost, rank_lower)),
                            "cap_pair_raw_lower": str(Fraction(n*(n-1), 4))})
    output = {"status": "passed", "exact_class_DP_cases": cases,
              "supplied_description_execution_cases": descriptions_checked,
              "actual_hypothesis_executions": executions,
              "subset_solver_is_validation_only": True,
              "uniform_rank_obstruction": obstruction}
    Path(__file__).with_name("research-general-matroid-algorithm-results.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
