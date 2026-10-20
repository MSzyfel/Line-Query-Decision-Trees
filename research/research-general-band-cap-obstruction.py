"""Constant balance-band obstruction using bounded-cardinality body tests."""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import importlib.util
import json
import math
import sys

spec = importlib.util.spec_from_file_location(
    "band_cap_menu_backend", Path(__file__).with_name("research-general-bounded-menu.py"))
MENU = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MENU
spec.loader.exec_module(MENU)


def instance_with_caps(M, L, cap=3):
    R = M - 2
    points = list(product(range(M), *(range(R) for _ in range(L))))
    tests, labels = [], []
    for coordinate, alphabet in enumerate([M] + [R] * L):
        for value in range(alphabet):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            labels.append(("selector" if coordinate == 0 else "body", coordinate, value))
    for body in range(1, L + 1):
        for subset in combinations(range(R), cap):
            chosen = set(subset)
            tests.append(sum(1 << h for h, point in enumerate(points) if point[body] in chosen))
            labels.append(("body", body, subset))
    for selector in range(M):
        for body in range(1, L + 1):
            for bit in range((R - 1).bit_length()):
                tests.append(sum(1 << h for h, point in enumerate(points)
                                 if point[0] == selector and point[body] >> bit & 1))
                labels.append(("gate", body, selector, bit))
    instance = MENU.Instance(len(points), tests)
    assert len(instance.tests) == len(labels)
    return instance, points, labels


def run():
    rectangle_checks = 0
    all_band_queries_checked = 0
    path_role_checks = 0
    fixtures = []
    for M, L in ((8, 1), (8, 2), (10, 1)):
        instance, points, labels = instance_with_caps(M, L)
        R = M - 2
        domains = [set(v for v in range(R) if mask >> v & 1)
                   for mask in range(1, 1 << R)]
        for current in product(domains, repeat=L):
            if all(len(domain) == 1 for domain in current):
                continue
            state = sum(1 << h for h, point in enumerate(points)
                        if all(point[j + 1] in domain for j, domain in enumerate(current)))
            proper = []
            for query, mask in enumerate(instance.tests):
                hit = state & mask
                miss = state ^ hit
                if hit and miss:
                    proper.append((min(hit.bit_count(), miss.bit_count()), query))
            maximum = max(minority for minority, _ in proper)
            assert Fraction(maximum, state.bit_count()) >= min(Fraction(1, 3), Fraction(3, R))
            assert maximum * M > 2 * state.bit_count()
            for minority, query in proper:
                if 2 * minority >= maximum:
                    assert labels[query][0] == "body"
                    all_band_queries_checked += 1
            rectangle_checks += 1

        tree = MENU.root_rare_band_policy(instance)
        MENU.check_tree(instance, tree, complete=True)
        @lru_cache(None)
        def inspect(node):
            nonlocal path_role_checks
            if node.test < 0:
                return
            values = [set() for _ in range(L)]
            for h, point in enumerate(points):
                if node.state >> h & 1:
                    for j in range(L):
                        values[j].add(point[j + 1])
            if any(len(domain) > 1 for domain in values):
                assert labels[node.test][0] == "body"
                selectors = {points[h][0] for h in range(instance.n) if node.state >> h & 1}
                assert len(selectors) == M
            path_role_checks += 1
            inspect(node.left)
            inspect(node.right)
        inspect(tree)
        lower = Fraction(L * (R - 1), 6)
        assert Fraction(tree.cost, instance.n) >= lower
        fixtures.append({"M": M, "R": R, "L": L, "n": instance.n,
                         "tests": len(instance.tests), "raw_cost": tree.cost,
                         "proven_body_work_lower": str(lower)})

    padding_checks = potential_checks = 0
    for cap in range(2, 7):
        for R in range(2 * cap, 2 * cap + 10):
            for r in range(2, R + 1):
                t = min(cap, r // 2)
                assert 0 <= cap - t <= R - r
                assert Fraction(t, r) >= min(Fraction(1, 3), Fraction(cap, R))
                padding_checks += 1
                for positive in range(1, min(cap, r - 1) + 1):
                    phi = Fraction(r - 1, 2 * cap)
                    after = Fraction(positive, r) * Fraction(positive - 1, 2 * cap)
                    after += Fraction(r - positive, r) * Fraction(r - positive - 1, 2 * cap)
                    assert phi - after == Fraction(positive * (r - positive), cap * r)
                    assert phi - after <= 1
                    potential_checks += 1

    scaling = []
    for p in (6, 8, 10, 12, 16):
        M = 1 << p
        R, L = M - 2, M // p
        lower = Fraction(L * (R - 1), 6)
        upper = MENU.equality_cost(M) + L * p
        scaling.append({"M": M, "L": L, "log2_n": p + L * math.log2(R),
                        "ratio_lower": float(lower / upper)})
    return {"status": "passed", "body_rectangle_checks": rectangle_checks,
            "all_half_band_query_checks": all_band_queries_checked,
            "deterministic_policy_internal_nodes_checked": path_role_checks,
            "padding_checks": padding_checks, "cap_potential_checks": potential_checks,
            "fixtures": fixtures, "symbolic_scaling": scaling,
            "no_unrestricted_constant_menu_impossibility_claim": True}


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("research-general-band-cap-obstruction-results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
