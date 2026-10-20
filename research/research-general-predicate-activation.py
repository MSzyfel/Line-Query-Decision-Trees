"""Bounded checks of predicate activation certificates and the dense gap.

Uses an explicit original-query upper code, never an unrestricted OPT oracle.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import comb
from pathlib import Path
import importlib.util
import json
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


GRAPH = load("predicate_activation_graph", "research-general-dependency-graph.py")
BACK = GRAPH.BACK


def synthesize_evaluator(sizes, true_tuples, negative_budget):
    """Exact synthesis, polynomial for each FIXED negative_budget.

    True leaves must know every parent; false leaves may stop on a larger
    all-false cell. Each positive equality fixes one coordinate, while each
    negative consumes one budget unit. No arbitrary subset is enumerated.
    """
    sizes, true_tuples = tuple(sizes), tuple(true_tuples)
    full = tuple((1 << size) - 1 for size in sizes)

    @lru_cache(None)
    def solve(candidates, remaining):
        exclusions = sum(size - mask.bit_count() for size, mask in zip(sizes, candidates)
                         if mask.bit_count() > 1)
        assert exclusions <= negative_budget - remaining
        compatible = [point for point in true_tuples
                      if all(mask >> value & 1 for mask, value in zip(candidates, point))]
        if not compatible:
            return ("leaf", False)
        if all(mask.bit_count() == 1 for mask in candidates):
            return ("leaf", True)
        if not remaining:
            return None
        for i, mask in enumerate(candidates):
            if mask.bit_count() == 1:
                continue
            for value in range(sizes[i]):
                if not mask >> value & 1:
                    continue
                updated = list(candidates)
                updated[i] = 1 << value
                positive = solve(tuple(updated), remaining)
                if positive is None:
                    continue
                updated[i] = mask ^ (1 << value)
                negative = solve(tuple(updated), remaining - 1)
                if negative is not None:
                    return ("eq", i, value, positive, negative)
        return None

    program = solve(full, negative_budget)
    if program is not None:
        true_set = set(true_tuples)
        for point in product(*(range(size) for size in sizes)):
            node, candidates, negatives = program, list(full), 0
            while node[0] != "leaf":
                _, i, value, positive, negative = node
                if point[i] == value:
                    candidates[i], node = 1 << value, positive
                else:
                    candidates[i] ^= 1 << value
                    node = negative
                    negatives += 1
            assert node[1] == (point in true_set)
            assert negatives <= negative_budget
            if node[1]:
                assert all(mask.bit_count() == 1 for mask in candidates)
    return program, {"budget": negative_budget, "states": solve.cache_info().currsize,
                     "feasible": program is not None}


def hamming_evaluator(values, alphabet, exceptions):
    """Equality-only evaluator; keep the exact candidate-value transcript."""
    remaining = [(1 << alphabet) - 1] * len(values)
    negative = used = 0
    for i, value in enumerate(values):
        if value == 0:
            remaining[i] = 1
            continue
        negative += 1
        remaining[i] ^= 1
        if used == exceptions:
            return False, negative, remaining
        if value == 1:
            remaining[i] = 2
            used += 1
        else:
            negative += 1
            remaining[i] ^= 2
            return False, negative, remaining
    assert all(mask.bit_count() == 1 for mask in remaining)
    return True, negative, remaining


def dense_instance(alphabet):
    width = alphabet.bit_length() - 1
    points = tuple(product(range(alphabet), repeat=2))
    tests = []
    for i in range(2):
        for value in range(alphabet):
            tests.append(sum(1 << h for h, x in enumerate(points) if x[i] == value))
    dense, rare = [], []
    for enabled_nonzero, collection in ((True, dense), (False, rare)):
        for i in range(2):
            for bit in range(width):
                mask = sum(1 << h for h, x in enumerate(points)
                           if bool(x[1-i]) == enabled_nonzero and x[i] >> bit & 1)
                if mask not in tests:
                    tests.append(mask)
                collection.append(tests.index(mask))
    return BACK.Instance(len(points), tests), points, tuple(dense), tuple(rare)


def ordered_code(instance, query_order):
    @lru_cache(None)
    def build(state, position):
        if state.bit_count() == 1:
            return BACK.Tree(state)
        while position < len(query_order):
            query = query_order[position]
            hit = state & instance.tests[query]
            position += 1
            if hit and hit != state:
                return instance.branch(state, query,
                                       build(hit, position), build(state ^ hit, position))
        raise AssertionError("supplied ordered code failed to identify")
    return build(instance.full, 0)


def execute(instance, tree):
    work = 0
    for h in range(instance.n):
        node = tree
        while node.test >= 0:
            assert node.state >> h & 1
            node = node.left if instance.tests[node.test] >> h & 1 else node.right
            work += 1
        assert node.state == 1 << h
    assert work == tree.cost


def main():
    evaluations, true_exits, maximum_negatives = 0, 0, 0
    hamming_rows = []
    for alphabet, parents in ((4, 1), (4, 2), (4, 3), (4, 4), (4, 5), (8, 3)):
        for exceptions in range(min(2, parents) + 1):
            true_count = max_negative = 0
            for values in product(range(alphabet), repeat=parents):
                answer, negative, candidates = hamming_evaluator(values, alphabet, exceptions)
                expected = all(value in (0, 1) for value in values) and sum(values) <= exceptions
                assert answer == expected
                assert negative <= exceptions + 1
                if answer:
                    assert all(mask.bit_count() == 1 for mask in candidates)
                    true_count += 1
                max_negative = max(max_negative, negative)
                evaluations += 1
            assert true_count == sum(comb(parents, j) for j in range(exceptions + 1))
            true_exits += true_count
            maximum_negatives = max(maximum_negatives, max_negative)
            hamming_rows.append({"alphabet": alphabet, "parents": parents,
                                 "exceptions": exceptions, "full_tuple_aliases": true_count,
                                 "maximum_negative_answers": max_negative})

    synthesis = []
    for parents, exceptions in ((2, 0), (2, 1), (3, 1), (3, 2), (4, 1)):
        true_tuples = [values for values in product(range(4), repeat=parents)
                       if all(value in (0, 1) for value in values) and sum(values) <= exceptions]
        program, stats = synthesize_evaluator((4,) * parents, true_tuples, exceptions + 1)
        assert program is not None
        synthesis.append({"alphabet": 4, "parents": parents,
                          "exceptions": exceptions, **stats})
    for budget in (1, 2, 3):
        program, stats = synthesize_evaluator((4,), [(1,), (2,), (3,)], budget)
        assert (program is not None) == (budget == 3)
        synthesis.append({"predicate": "one parent is nonzero", "alphabet": 4, **stats})

    dense_rows = []
    for alphabet in (4, 8, 16, 32, 64):
        instance, points, dense, rare = dense_instance(alphabet)
        width = alphabet.bit_length() - 1
        code = ordered_code(instance, dense + rare)
        execute(instance, code)
        zero_cell = instance.full
        for query in dense:
            zero_cell &= ~instance.tests[query]
        expected_cell = sum(1 << h for h, x in enumerate(points) if not x[0] or not x[1])
        assert zero_cell == expected_cell and zero_cell.bit_count() == 2 * alphabet - 1
        upper = 2 * width * (instance.n + 2 * alphabet - 1)
        assert code.cost <= upper
        dp = GRAPH.ChargedActivationDP((alphabet, alphabet), ((1,), (0,)), (width, width))
        charged = dp.solve((alphabet, alphabet))
        first_identification_lower = sum(Fraction(alphabet - t, alphabet)
                                         for t in range(alphabet // 2))
        assert first_identification_lower == Fraction(3 * alphabet + 2, 8)
        assert charged >= first_identification_lower
        dense_rows.append({"alphabet": alphabet, "n": instance.n,
                           "actual_code_raw_work": code.cost,
                           "actual_code_mean": str(Fraction(code.cost, instance.n)),
                           "explicit_upper_mean": str(Fraction(upper, instance.n)),
                           "full_parent_charged_mean": str(charged),
                           "first_identification_lower": str(first_identification_lower),
                           "charged_to_actual_code": str(charged / Fraction(code.cost, instance.n)),
                           "count_states": len(dp.values)})
    result = {"predicate_truth_table_evaluations": evaluations,
              "verified_full_parent_true_exits": true_exits,
              "largest_negative_budget_seen": maximum_negatives,
              "hamming_predicates": hamming_rows,
              "fixed_budget_synthesis": synthesis,
              "dense_predicate_obstructions": dense_rows,
              "no_unrestricted_optimum_oracle": True}
    Path(__file__).with_suffix(".results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
