"""Exact small target-pricing audit; no exponential routine in the algorithm.

The cap algorithm and pair ledger are polynomial. The subset DP below is
used only to validate its ratio on small explicitly generated instances.
"""
from fractions import Fraction
from functools import lru_cache
import itertools
import json
import math
from pathlib import Path
import random


def singleton_cost(size):
    return 0 if size == 0 else size * (size+1) // 2 - 1


def pricing_algorithm(targets, outsiders, caps, weights):
    cap = max(caps, key=lambda cell: sum(
        weight for h, weight in enumerate(weights) if cell & (1 << h)))
    reward = sum(weight for h, weight in enumerate(weights) if cap & (1 << h))
    work = targets + outsiders + singleton_cost(cap.bit_count())
    assert work <= outsiders + targets * targets
    return Fraction(reward, work), work, reward


def exact_pricing(n, tests, weights, starting_ratio):
    ratio, updates = starting_ratio, 0
    while True:
        @lru_cache(None)
        def optimize(state):
            if state.bit_count() == 1:
                return weights[state.bit_length()-1], 0
            best = (0, 0)
            for test in tests:
                positive = state & test
                if not positive or positive == state:
                    continue
                r0, w0 = optimize(state ^ positive)
                r1, w1 = optimize(positive)
                candidate = r0+r1, w0+w1+state.bit_count()
                if (candidate[0] - ratio*candidate[1], -candidate[1]) > (
                        best[0] - ratio*best[1], -best[1]):
                    best = candidate
            return best
        reward, work = optimize((1 << n)-1)
        if reward - ratio*work <= 0:
            return ratio, updates
        assert work > 0
        new_ratio = Fraction(reward, work)
        assert new_ratio > ratio
        ratio = new_ratio
        updates += 1
        assert updates <= n**4


def ledger_check(targets, outsiders, caps, weights):
    maximum = max(sum(weight for h, weight in enumerate(weights)
                      if cap & (1 << h)) for cap in caps)
    assert maximum > 0
    for cap in caps + [1 << h for h in range(targets)]:
        outside_load = sum(Fraction(weight, maximum) for h, weight in enumerate(weights)
                           if cap & (1 << h))
        assert outside_load <= 1
    for weight in weights:
        assert Fraction(weight, maximum) <= 1
    return maximum


def small_pricing_checks():
    rng = random.Random(18102026)
    cases = updates = 0
    largest_actual_ratio = Fraction(1)
    for targets in range(1, 6):
        for outsiders in range(1, 5):
            for _ in range(6):
                caps = sorted({rng.randrange(1, 1 << targets) for _ in range(5)})
                # Ensure caps cover every target; this changes only the
                # supplied family, not the analysis.
                cover = 0
                for cap in caps:
                    cover |= cap
                caps += [1 << h for h in range(targets) if not cover & (1 << h)]
                weights = [rng.randrange(8) for _ in range(targets)]
                if not any(weights):
                    weights[rng.randrange(targets)] = 1
                maximum = ledger_check(targets, outsiders, caps, weights)
                ratio, _, _ = pricing_algorithm(targets, outsiders, caps, weights)
                n = targets + outsiders
                tests = tuple(dict.fromkeys(caps + [1 << h for h in range(n)]))
                optimum, strict_updates = exact_pricing(
                    n, tests, tuple(weights + [0]*outsiders), ratio)
                assert optimum <= Fraction(maximum, outsiders)
                assert optimum / ratio <= 1 + Fraction(targets*targets, outsiders)
                largest_actual_ratio = max(largest_actual_ratio, optimum/ratio)
                cases += 1
                updates += strict_updates
    return {"exact_small_pricing_cases": cases,
            "strict_pricing_DP_updates": updates,
            "largest_observed_approximation_ratio": str(largest_actual_ratio)}


def large_outsider_example():
    r, k = 6, 3
    labels = list(itertools.combinations(range(r), k))
    targets = len(labels)
    outsiders = targets**3
    caps = [sum(1 << h for h, label in enumerate(labels) if i in label)
            for i in range(r)]
    weights = [1] * targets
    maximum = ledger_check(targets, outsiders, caps, weights)
    density, work, reward = pricing_algorithm(targets, outsiders, caps, weights)
    return {"r": r, "k": k, "targets": targets, "outsiders": outsiders,
            "cap_reward": reward, "cap_raw_work": work,
            "candidate_exact_density": str(density),
            "certified_optimum_density_upper": str(Fraction(maximum, outsiders)),
            "certified_approximation_factor": str(Fraction(work, outsiders))}


def coding_cost(size):
    if size <= 1:
        return 0
    depth = (size-1).bit_length()
    return size*(depth+1) - (1 << depth)


def direct_product_checks():
    q, dimension, t = 3, 3, 27
    points = list(itertools.product(range(q), repeat=dimension))
    a = len(points)
    normals = [normal for normal in itertools.product(range(q), repeat=dimension)
               if next((entry for entry in normal if entry), None) == 1]
    affine = [sum(1 << h for h, point in enumerate(points)
                  if sum(x*y for x, y in zip(normal, point)) % q == offset)
              for normal in normals for offset in range(q)]
    expected = q*(a-1)//(q-1)
    separation = 2*a//q
    assert len(affine) == len(set(affine)) == expected
    for h in range(a):
        for g in range(h):
            pair = (1 << h) | (1 << g)
            assert sum(bool(test & pair) and bool(pair & ~test)
                       for test in affine) == separation
    thresholds = [(1 << boundary)-1 for boundary in range(1, t)]
    for boundary in range(1, t):
        left, right = 1 << (boundary-1), 1 << boundary
        assert [j+1 for j, test in enumerate(thresholds)
                if bool(test & left) != bool(test & right)] == [boundary]
    n = a*t
    pair_upper = Fraction(n*expected, separation) + a*coding_cost(t)
    return {"q": q, "dimension": dimension, "affine_points": a,
            "threshold_points": t, "n": n, "affine_tests": expected,
            "necessary_threshold_palette": t-1,
            "pair_cone_raw_upper": str(pair_upper)}


def main():
    result = {"status": "passed", "subset_pricing_is_validation_only": True,
              **small_pricing_checks(),
              "large_outsider_example": large_outsider_example(),
              "direct_product_checks": direct_product_checks()}
    Path(__file__).with_name("research-general-causal-resource-results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
