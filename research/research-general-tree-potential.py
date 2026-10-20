"""Polynomial separation for the restriction potential of ONE explicit tree."""

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import random

spec = importlib.util.spec_from_file_location("code_library", "research-general-algorithm-next.py")
library = importlib.util.module_from_spec(spec)
# Dataclasses need the module registered while annotations are processed.
import sys
sys.modules[spec.name] = library
spec.loader.exec_module(library)


def restricted_work(tree, selected, weights=None):
    if selected.bit_count() <= 1:
        return 0
    left = selected & tree.left.state
    right = selected ^ left
    if not left:
        return restricted_work(tree.right, right, weights)
    if not right:
        return restricted_work(tree.left, left, weights)
    weight = 1 if weights is None else weights.get(tree.state, 0)
    return (weight * selected.bit_count() + restricted_work(tree.left, left, weights)
            + restricted_work(tree.right, right, weights))


def drop(tree, selected, test, weights=None):
    return (restricted_work(tree, selected, weights)
            - restricted_work(tree, selected & test, weights)
            - restricted_work(tree, selected & ~test, weights))


def separate(tree, test, weights=None):
    """Maximize restriction drop/|S| over ALL S, not just tree-node states."""
    entries = 0

    def solve(node):
        nonlocal entries
        if node.test < 0:
            key = (1, 0) if node.state & test else (0, 1)
            return {(0, 0): (0, 0), key: (0, node.state)}
        left, right = solve(node.left), solve(node.right)
        result = {}
        for (rl, bl), (dl, ml) in left.items():
            for (rr, br), (dr, mr) in right.items():
                r, b = rl + rr, bl + br
                increment = 0
                if rl + bl and rr + br:
                    if not (rl and rr):
                        increment += r
                    if not (bl and br):
                        increment += b
                weight = 1 if weights is None else weights.get(node.state, 0)
                candidate = (dl + dr + weight * increment, ml | mr)
                if candidate[0] > result.get((r, b), (-1, 0))[0]:
                    result[r, b] = candidate
        entries += len(result)
        return result

    table = solve(tree)
    best = (Fraction(0), 0, 0)
    for (r, b), (saving, selected) in table.items():
        if r + b:
            candidate = (Fraction(saving, r + b), selected, saving)
            if candidate[0] > best[0]:
                best = candidate
    assert drop(tree, best[1], test, weights) == best[2]
    return best, entries


def main():
    rng = random.Random(20261018)
    checks = 0
    weighted_checks = 0
    certificates = 0
    for n in range(2, 9):
        for _ in range(20):
            tests = [rng.randrange(1, (1 << n) - 1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if h >> b & 1)
                      for b in range((n - 1).bit_length())]
            instance = library.Instance(n, tests)
            tree = instance.greedy(instance.full)
            beta = Fraction(0)
            weights = {v.state: Fraction(rng.randrange(9), 8)
                       for v in library.tree_nodes(tree) if v.test >= 0}
            for test in instance.tests:
                result, _ = separate(tree, test)
                brute = max(Fraction(drop(tree, s, test), s.bit_count())
                            for s in range(1, 1 << n))
                assert result[0] == brute
                beta = max(beta, result[0])
                checks += 1
                weighted_result, _ = separate(tree, test, weights)
                weighted_brute = max(Fraction(drop(tree, s, test, weights), s.bit_count())
                                     for s in range(1, 1 << n))
                assert weighted_result[0] == weighted_brute
                weighted_checks += 1
            assert beta >= 1
            assert Fraction(tree.cost, 1) / beta <= instance.exact_cost()
            certificates += 1

    cubes = []
    for dimension in range(3, 12):
        n = 1 << dimension
        coordinates = [sum(1 << h for h in range(n) if h >> b & 1)
                       for b in range(dimension)]
        special = 1 | sum(1 << (1 << b) for b in range(dimension))
        selected_symbols = [h for h in range(n) if special >> h & 1]
        added_test = sum(1 << h for h in selected_symbols[::2])
        instance = library.Instance(n, coordinates + [added_test])
        # Coordinate code is supplied explicitly, independently of greedy ties.
        def coordinate_code(state, depth=0):
            if state.bit_count() <= 1:
                return library.Tree(state)
            hit = state & coordinates[depth]
            miss = state ^ hit
            return instance.branch(state, depth,
                                   coordinate_code(hit, depth + 1),
                                   coordinate_code(miss, depth + 1))
        tree = coordinate_code(instance.full)
        assert tree.cost == n * dimension
        s = dimension + 1
        a = (special & added_test).bit_count()
        b = s - a
        saving = drop(tree, special, added_test)
        assert saving == a*b + 1
        cubes.append({"n": n, "optimal_mean": dimension,
                      "witness_size": s, "drop": saving,
                      "beta_lower": str(Fraction(saving, s))})

    result = {"exhaustive_query_checks": checks,
              "weighted_exhaustive_query_checks": weighted_checks,
              "exact_lower_certificates": certificates,
              "optimal_tree_scaling_counterexamples": cubes}
    Path("research-general-tree-potential-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
