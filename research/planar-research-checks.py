"""Small exact checks for the research agenda; no third-party packages needed."""

from functools import lru_cache
from fractions import Fraction
from itertools import permutations
import random


def exact_costs(weights, tests):
    """Unnormalized expected cost and height, by subset Bellman recurrences."""
    weights = tuple(weights)
    tests = tuple(tests)

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0, 0
        mass = sum(w for i, w in enumerate(weights) if state >> i & 1)
        candidates = []
        for test in tests:
            left = state & test
            right = state ^ left
            if left and right:
                expected_l, height_l = solve(left)
                expected_r, height_r = solve(right)
                candidates.append((mass + expected_l + expected_r,
                                   1 + max(height_l, height_r)))
        if not candidates:
            raise ValueError("Tests do not separate the hypotheses")
        return min(x[0] for x in candidates), min(x[1] for x in candidates)

    return solve((1 << len(weights)) - 1)


def maximum_matching_size(n, edges):
    @lru_cache(None)
    def solve(remaining):
        if not remaining:
            return 0
        vertex = (remaining & -remaining).bit_length() - 1
        rest = remaining & ~(1 << vertex)
        best = solve(rest)
        for u, v in edges:
            other = v if u == vertex else u if v == vertex else None
            if other is not None and rest >> other & 1:
                best = max(best, 1 + solve(rest & ~(1 << other)))
        return best

    return solve((1 << n) - 1)


def check_uniform_pair_formula():
    rng = random.Random(13102026)
    checked = 0
    for n in range(1, 8):
        for _ in range(30):
            edges = tuple((u, v) for u in range(n) for v in range(u + 1, n)
                          if rng.random() < 0.3)
            r = maximum_matching_size(n, edges)
            tests = [1 << (v + 1) for v in range(n)]
            tests += [(1 << (u + 1)) | (1 << (v + 1)) for u, v in edges]
            expected, height = exact_costs([1] * (n + 1), tests)
            k = n - r
            predicted_expected = k + (k * (k + 1) + r * (r + 1)) // 2 + 2 * r
            predicted_height = max(k, r + 1) if r else k
            assert (expected, height) == (predicted_expected, predicted_height)
            checked += 1
    return checked


def check_deadline_obstruction():
    demands = (({1, 2}, 1), ({2, 3}, 1), ({1}, 2), ({3}, 2))
    assert all(any(point in interval for point in {2})
               for interval, deadline in demands if deadline == 1)
    assert all(any(point in interval for point in {1, 3})
               for interval, _ in demands)
    for order in permutations((1, 2, 3)):
        assert not all(min(order.index(v) + 1 for v in interval) <= deadline
                       for interval, deadline in demands)


def check_rounded_deadlines():
    checked = 0
    for scale in (Fraction(101, 100), Fraction(11, 10), Fraction(3, 2)):
        levels = []
        power = Fraction(1)
        while power < 10000:
            levels.append(power.numerator // power.denominator)
            power *= scale
        for t in range(1, 300):
            lower = 2 * scale * t
            budget = lower.numerator // lower.denominator
            rounded = max(level for level in levels if level <= budget)
            assert rounded >= 2 * t
            checked += 1
    return checked


if __name__ == "__main__":
    pair_checks = check_uniform_pair_formula()
    check_deadline_obstruction()
    rounding_checks = check_rounded_deadlines()
    print(f"PASS: {pair_checks} exact uniform singleton/pair instances")
    print("PASS: independent prefix covers do not imply a feasible schedule")
    print(f"PASS: {rounding_checks} rational rounded-deadline checks")
