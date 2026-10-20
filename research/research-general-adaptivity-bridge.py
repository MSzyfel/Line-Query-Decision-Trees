"""Finite audits of palette drift, actual balanced frontiers, and obstructions."""

from functools import lru_cache
from itertools import combinations
import importlib.util
import math
import random
import sys


spec = importlib.util.spec_from_file_location("adaptivity_bridge_backend", "research-general-algorithm-next.py")
library = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = library
spec.loader.exec_module(library)


def entropy(sizes):
    total = sum(sizes)
    return sum(-(size / total) * math.log2(size / total) for size in sizes if size)


def drift_potential(size):
    return 0.0 if size <= 1 else 1 + math.log(math.log2(size))


def identifies(tests, state, palette):
    signatures = set()
    for h in range(state.bit_length()):
        if state >> h & 1:
            signature = tuple((tests[q] >> h) & 1 for q in palette)
            if signature in signatures:
                return False
            signatures.add(signature)
    return True


def minimum_palette(tests, state):
    if state.bit_count() <= 1:
        return ()
    for size in range(1, len(tests) + 1):
        for palette in combinations(range(len(tests)), size):
            if identifies(tests, state, palette):
                return palette
    raise AssertionError("Nonseparable validation instance")


def balanced_prefix(tree, eta):
    if tree.test < 0:
        return 0, []
    size = tree.state.bit_count()
    if min(tree.left.state.bit_count(), tree.right.state.bit_count()) < eta * size:
        return 0, [tree]
    left, right = balanced_prefix(tree.left, eta), balanced_prefix(tree.right, eta)
    return size + left[0] + right[0], left[1] + right[1]


def main():
    rng = random.Random(20261018)
    instances = drift_states = frontier_checks = 0
    for n in range(2, 10):
        for _ in range(12):
            tests = [rng.randrange(1, (1 << n) - 1) for _ in range(4)]
            tests += [sum(1 << h for h in range(n) if (h >> bit) & 1)
                      for bit in range((n - 1).bit_length())]
            instance = library.Instance(n, tests)
            palette = minimum_palette(instance.tests, instance.full)
            d = len(palette)
            greedy = instance.greedy(instance.full)
            assert greedy.cost / n <= d * drift_potential(n) + 1e-10
            for state in range(1, 1 << n):
                size = state.bit_count()
                if size <= 1:
                    continue
                info = sum(entropy([(state & instance.tests[q]).bit_count(),
                                    (state & ~instance.tests[q]).bit_count()]) for q in palette)
                assert info + 1e-10 >= math.log2(size)
                code = instance.greedy(state)
                parts = [code.left.state.bit_count(), code.right.state.bit_count()]
                raw_drift = math.log2(size) - sum((part / size) * math.log2(part) for part in parts)
                assert raw_drift + 1e-10 >= math.log2(size) / d
                final_drift = drift_potential(size) - sum((part / size) * drift_potential(part) for part in parts)
                assert final_drift + 1e-10 >= 1 / d
                drift_states += 1
            optimum = instance.exact_cost()
            for eta in (1 / 3, 0.45):
                prefix_work, frontier = balanced_prefix(greedy, eta)
                entropy_drop = n * math.log2(n) - sum(node.state.bit_count() * math.log2(node.state.bit_count()) for node in frontier)
                assert prefix_work <= entropy_drop / entropy([eta, 1 - eta]) + 1e-9
                budget, continuation_bound = 0, 0.0
                for node in frontier:
                    size = node.state.bit_count()
                    local_d = len(minimum_palette(instance.tests, node.state))
                    budget += size * local_d
                    continuation_bound += size * local_d * drift_potential(size)
                assert greedy.cost == prefix_work + sum(node.cost for node in frontier)
                assert greedy.cost <= prefix_work + continuation_bound + 1e-9
                r = budget / optimum
                bound = (1 / entropy([eta, 1 - eta]) + r * drift_potential(n)) * optimum
                assert greedy.cost <= bound + 1e-9
                frontier_checks += 1
            instances += 1

    threshold_rows = []
    subset_palette_checks = 0
    for dimension in range(2, 8):
        n = 1 << dimension
        tests = [(1 << cut) - 1 for cut in range(1, n)]
        instance = library.Instance(n, tests)
        greedy = instance.greedy(instance.full)
        assert greedy.cost == n * dimension
        # At the full set, each adjacent pair has exactly one separating test.
        for h in range(n - 1):
            separating = [q for q, test in enumerate(tests) if bool(test >> h & 1) != bool(test >> (h + 1) & 1)]
            assert separating == [h]
        for _ in range(20):
            chosen = sorted(rng.sample(range(n), rng.randrange(1, n + 1)))
            state = sum(1 << h for h in chosen)
            palette = tuple(chosen[i] for i in range(len(chosen) - 1))
            assert identifies(tests, state, palette)
            required_sets = [{q for q, test in enumerate(tests)
                              if bool(test >> a & 1) != bool(test >> b & 1)}
                             for a, b in zip(chosen, chosen[1:])]
            assert all(required_sets[i].isdisjoint(required_sets[j])
                       for i in range(len(required_sets)) for j in range(i))
            size = len(chosen)
            depth = (size - 1).bit_length()
            coding_cost = 0 if size <= 1 else size * (depth + 1) - (1 << depth)
            assert instance.greedy(state).cost == coding_cost
            subset_palette_checks += 1
        threshold_rows.append((n, n - 1, dimension, (n - 1) / dimension))

    credit_rows = []
    credit_state_checks = 0
    def f(size):
        return 0 if size <= 1 else size * (size + 1) // 2 - 1
    for r in range(3, 10):
        n = 2 * r
        a = (1 << r) - 1
        b = ((1 << n) - 1) ^ a
        tests = [a] + [(1 << i) | (b ^ (1 << (r + j))) for i in range(r) for j in range(r)]
        assert all(test.bit_count() == r for test in tests)
        @lru_cache(None)
        def optimum(state):
            size = state.bit_count()
            if size <= 1:
                return 0
            return size + min(optimum(state & test) + optimum(state & ~test)
                              for test in tests if state & test and state & ~test)
        assert optimum(a) == optimum(b) == f(r)
        assert optimum(a | b) == 2 * f(r) + 6
        for size in range(3, r + 1):
            state = 1 | sum(1 << (r + j) for j in range(size - 1))
            assert optimum(state) == f(size) - size + 3
            credit_state_checks += 1
        assert optimum(a | b) - optimum(a) - optimum(b) == 6
        credit_rows.append((n, optimum(a | b), 6, n))

    print("PASS small exact-palette instances:", instances)
    print("PASS entropy and last-step drift states:", drift_states)
    print("PASS actual balanced-frontier inequalities:", frontier_checks)
    print("PASS threshold subset palette checks:", subset_palette_checks)
    print("Threshold adaptivity rows (n,D,OPTmean,D/OPTmean):", threshold_rows)
    print("PASS exact exceptional-state formulas:", credit_state_checks)
    print("Optimal-credit rows (n,OPTraw,credit,raw output entropy):", credit_rows)


if __name__ == "__main__":
    main()
