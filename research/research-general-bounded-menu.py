"""Bounded-menu Bellman search, portfolio races, and a balance-menu barrier.

All algorithm routines below use supplied tests only. Exhaustive full-policy
lists are a validation oracle for depth <= 3, never part of the algorithm.
"""
from __future__ import annotations

from functools import lru_cache
from fractions import Fraction
import importlib.util
import itertools
import json
import math
from pathlib import Path
import random
import sys


def load_backend():
    spec = importlib.util.spec_from_file_location(
        "bounded_menu_backend", Path(__file__).with_name("research-general-algorithm-next.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BACK = load_backend()
Instance, Tree = BACK.Instance, BACK.Tree


def balanced_menu(instance, state, width):
    """Top-width proper partitions by balance; complements count only once."""
    partitions = {}
    for query, test in enumerate(instance.tests):
        hit = state & test
        miss = state ^ hit
        if hit and miss:
            key = min(hit, miss)
            score = (max(hit.bit_count(), miss.bit_count()), query)
            if key not in partitions or score < partitions[key][0]:
                partitions[key] = score, query
    return tuple(query for _, query in sorted(partitions.values())[:width])


def banded_balance_menu(instance, state, width=2):
    """Max balance and least balance strictly above half of that maximum.

    Equal-current-balance ties prefer smaller ORIGINAL root minority. This
    is a directly computable query statistic, not a hidden-coordinate label.
    """
    options = []
    for query, test in enumerate(instance.tests):
        hit = state & test
        miss = state ^ hit
        if hit and miss:
            minority = min(hit.bit_count(), miss.bit_count())
            root_minority = min(test.bit_count(), instance.n - test.bit_count())
            options.append((minority, root_minority, query))
    if not options:
        return ()
    maximum = max(value[0] for value in options)
    best = min(options, key=lambda value: (-value[0], value[1], value[2]))[2]
    edge = min(value for value in options if 2 * value[0] > maximum)[2]
    return tuple(dict.fromkeys((best, edge)))


def bounded_menu_search(instance, width, depth, menu=balanced_menu):
    """Exact best menu-admissible depth-depth prefix with fresh greedy exits."""
    @lru_cache(None)
    def solve(state, remaining):
        best = instance.greedy(state)
        if remaining == 0 or state.bit_count() <= 1:
            return best
        for query in menu(instance, state, width):
            hit = state & instance.tests[query]
            candidate = instance.branch(state, query,
                                        solve(hit, remaining - 1),
                                        solve(state ^ hit, remaining - 1))
            if candidate.cost < best.cost:
                best = candidate
        return best
    result = solve(instance.full, depth)
    return result, solve.cache_info().misses


def random_policy(instance, rng, state=None):
    state = instance.full if state is None else state
    if state.bit_count() <= 1:
        return Tree(state)
    options = [q for q, mask in enumerate(instance.tests)
               if state & mask and state & mask != state]
    query = rng.choice(options)
    hit = state & instance.tests[query]
    return instance.branch(state, query,
                           random_policy(instance, rng, hit),
                           random_policy(instance, rng, state ^ hit))


def race_cut(instance, policies, target):
    """Round robin virtual policies; stop when actual candidate size <= target.

    Virtual queries constant on the stronger actual state cost no physical
    test, but still consume the expert's scheduled virtual step. This keeps
    the pointwise b-competitive scheduling proof literal.
    """
    assert policies and target >= 1
    assert all(policy.state == instance.full for policy in policies)
    width = len(policies)

    def build(state, pointers, turn):
        while state.bit_count() > target:
            expert = turn % width
            node = pointers[expert]
            assert node.state & state == state
            assert node.test >= 0
            hit = state & instance.tests[node.test]
            miss = state ^ hit
            turn += 1
            if not hit or not miss:
                advanced = node.left if hit else node.right
                pointers = pointers[:expert] + (advanced,) + pointers[expert + 1:]
                continue
            hit_pointers = pointers[:expert] + (node.left,) + pointers[expert + 1:]
            miss_pointers = pointers[:expert] + (node.right,) + pointers[expert + 1:]
            return instance.branch(state, node.test,
                                   build(hit, hit_pointers, turn),
                                   build(miss, miss_pointers, turn))
        return Tree(state)

    return build(instance.full, tuple(policies), 0)


def depths(tree):
    result = {}
    def visit(node, depth):
        if node.test < 0:
            for h in range(node.state.bit_length()):
                if node.state >> h & 1:
                    result[h] = depth
        else:
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)
    visit(tree, 0)
    return result


def cut_depth(tree, target, h):
    depth = 0
    while tree.state.bit_count() > target:
        assert tree.test >= 0
        tree = tree.left if tree.left.state >> h & 1 else tree.right
        depth += 1
    return depth


def check_tree(instance, tree, complete=False):
    assert tree.state == instance.full
    work = 0
    def visit(node):
        nonlocal work
        if node.test < 0:
            if complete:
                assert node.state.bit_count() == 1
            return
        hit = node.state & instance.tests[node.test]
        miss = node.state ^ hit
        assert hit and miss
        assert node.left.state == hit and node.right.state == miss
        work += node.state.bit_count()
        visit(node.left)
        visit(node.right)
    visit(tree)
    assert work == tree.cost == sum(depths(tree).values())


def equality_cost(size):
    return Fraction(size + 1, 2) - Fraction(1, size)


def barrier_instance(M, L):
    s = M - 2
    points = list(itertools.product(range(M), *(range(s) for _ in range(L))))
    masks, labels = [], []
    for coordinate, alphabet in enumerate([M] + [s] * L):
        for value in range(alphabet):
            masks.append(sum(1 << h for h, point in enumerate(points)
                             if point[coordinate] == value))
            labels.append(("selector" if coordinate == 0 else "body", coordinate, value))
    for selector in range(M):
        for body in range(1, L + 1):
            for bit in range((s - 1).bit_length()):
                masks.append(sum(1 << h for h, point in enumerate(points)
                                 if point[0] == selector and point[body] >> bit & 1))
                labels.append(("gate", body, selector, bit))
    instance = Instance(len(points), masks)
    assert len(instance.tests) == len(labels)
    return instance, points, labels


def private_product_instance(M, L, selectors):
    R = M - 2
    points = list(itertools.product(*(range(M) for _ in range(selectors)),
                                    *(range(R) for _ in range(L))))
    masks, labels = [], []
    for coordinate, alphabet in enumerate([M] * selectors + [R] * L):
        for value in range(alphabet):
            masks.append(sum(1 << h for h, point in enumerate(points)
                             if point[coordinate] == value))
            labels.append(("selector" if coordinate < selectors else "body",
                           coordinate, value))
    for selector in itertools.product(range(M), repeat=selectors):
        for body in range(selectors, selectors + L):
            for bit in range((R - 1).bit_length()):
                masks.append(sum(1 << h for h, point in enumerate(points)
                                 if point[:selectors] == selector and point[body] >> bit & 1))
                labels.append(("gate", body, selector, bit))
    instance = Instance(len(points), masks)
    assert len(instance.tests) == len(labels)
    return instance, points, labels


def root_rare_band_policy(instance):
    """Choose smaller original-root minority from the two offered queries."""
    @lru_cache(None)
    def build(state):
        if state.bit_count() <= 1:
            return Tree(state)
        menu = banded_balance_menu(instance, state)
        query = min(menu, key=lambda q: (
            min(instance.tests[q].bit_count(), instance.n - instance.tests[q].bit_count()), q))
        hit = state & instance.tests[query]
        return instance.branch(state, query, build(hit), build(state ^ hit))
    return build(instance.full)


def run_checks():
    rng = random.Random(2026101907)
    bellman_cases = 0
    race_paths = 0
    maximum_search_states = 0
    for trial in range(24):
        n = 4 + trial % 7
        tests = [sum(1 << h for h in range(n) if h >> bit & 1)
                 for bit in range((n - 1).bit_length())]
        tests += [rng.randrange(1, (1 << n) - 1) for _ in range(6)]
        instance = Instance(n, tests)
        width = 1 + trial % 3
        depth = min(3, math.ceil(math.log2(n)))
        chosen, states = bounded_menu_search(instance, width, depth)
        maximum_search_states = max(maximum_search_states, states)
        check_tree(instance, chosen, complete=True)

        @lru_cache(None)
        def all_costs(state, remaining):
            values = [instance.greedy(state).cost]
            if remaining and state.bit_count() > 1:
                for query in balanced_menu(instance, state, width):
                    hit = state & instance.tests[query]
                    for a in all_costs(hit, remaining - 1):
                        for b in all_costs(state ^ hit, remaining - 1):
                            values.append(state.bit_count() + a + b)
            return tuple(values)

        assert chosen.cost == min(all_costs(instance.full, depth))
        bellman_cases += 1
        policies = [random_policy(instance, rng) for _ in range(width)]
        for target in sorted({1, max(1, n // 2), max(1, n // 3)}):
            race = race_cut(instance, policies, target)
            check_tree(instance, race)
            actual_depth = depths(race)
            for h in range(n):
                best = min(cut_depth(policy, target, h) for policy in policies)
                assert actual_depth[h] <= width * best
                race_paths += 1

    barrier_states, potential_equalities = 0, 0
    fixtures = []
    for M, L in ((4, 3), (5, 3), (6, 2)):
        instance, points, labels = barrier_instance(M, L)
        s = M - 2
        subsets = [tuple(value for value in range(s) if mask >> value & 1)
                   for mask in range(1, 1 << s)]
        for domains in itertools.product(subsets, repeat=L):
            unresolved = sum(len(domain) > 1 for domain in domains)
            if not unresolved:
                continue
            state = sum(1 << h for h, point in enumerate(points)
                        if all(point[j + 1] in domain for j, domain in enumerate(domains)))
            for width in range(1, unresolved + 1):
                menu = balanced_menu(instance, state, width)
                assert len(menu) == width
                assert all(labels[q][0] == "body" for q in menu)
                barrier_states += 1
            for domain in domains:
                r = len(domain)
                if r > 1:
                    assert equality_cost(r) == 1 + Fraction(r - 1, r) * equality_cost(r - 1)
                    potential_equalities += 1
        for width in range(1, min(3, L + 1)):
            tree, states = bounded_menu_search(instance, width, 5)
            check_tree(instance, tree, complete=True)
            lower = (L - width + 1) * equality_cost(s)
            assert Fraction(tree.cost, instance.n) >= lower
            fixtures.append({"n": instance.n, "M": M, "L": L, "width": width,
                             "depth": 5, "raw_cost": tree.cost, "states": states,
                             "lower": str(lower)})

    positive_fixtures = []
    for M, L in ((6, 1), (6, 2), (8, 2), (10, 2)):
        base, points, labels = barrier_instance(M, L)
        order = sorted(range(len(labels)), key=lambda q: (
            {"body": 0, "selector": 1, "gate": 2}[labels[q][0]], q))
        instance = Instance(base.n, [base.tests[q] for q in order])
        reordered_labels = [labels[q] for q in order]
        selector_states = 0
        for remaining in range(2, M + 1):
            allowed = set(range(M - remaining, M))
            state = sum(1 << h for h, point in enumerate(points) if point[0] in allowed)
            menu = banded_balance_menu(instance, state)
            assert any(reordered_labels[q][0] == "selector" for q in menu)
            selector_states += 1

        def witness(state):
            selectors = {points[h][0] for h in range(instance.n) if state >> h & 1}
            if len(selectors) == 1:
                return instance.greedy(state)
            query = next(q for q in banded_balance_menu(instance, state)
                         if reordered_labels[q][0] == "selector")
            hit = state & instance.tests[query]
            return instance.branch(state, query, witness(hit), witness(state ^ hit))

        tree = witness(instance.full)
        check_tree(instance, tree, complete=True)
        upper = equality_cost(M) + L * (M - 3).bit_length()
        assert Fraction(tree.cost, instance.n) <= upper
        fixture = {"n": instance.n, "M": M, "L": L,
                   "selector_state_checks": selector_states,
                   "greedy_raw_cost": instance.greedy(instance.full).cost,
                   "witness_raw_cost": tree.cost, "upper": str(upper)}
        if instance.n <= 24:
            horizon = math.ceil(2 * math.log2(instance.n))
            found, states = bounded_menu_search(instance, 2, horizon,
                                                menu=banded_balance_menu)
            assert found.cost <= tree.cost
            check_tree(instance, found, complete=True)
            fixture.update({"search_depth": horizon, "search_states": states,
                            "search_raw_cost": found.cost})
        positive_fixtures.append(fixture)

    deterministic_fixtures = []
    for M, L, selectors in ((6, 2, 1), (6, 2, 2), (6, 1, 3), (8, 1, 2)):
        instance, points, labels = private_product_instance(M, L, selectors)
        tree = root_rare_band_policy(instance)
        check_tree(instance, tree, complete=True)
        counts = {"selector": 0, "gate": 0}

        def inspect(node):
            if node.test < 0:
                return
            contexts = {points[h][:selectors] for h in range(instance.n) if node.state >> h & 1}
            expected = "selector" if len(contexts) > 1 else "gate"
            assert labels[node.test][0] == expected
            counts[expected] += 1
            inspect(node.left)
            inspect(node.right)

        inspect(tree)
        upper = selectors * equality_cost(M) + L * (M - 3).bit_length()
        assert Fraction(tree.cost, instance.n) <= upper
        deterministic_fixtures.append({"n": instance.n, "M": M, "L": L,
                                       "selectors": selectors, "raw_cost": tree.cost,
                                       "upper": str(upper), "node_types": counts})

    symbolic = []
    for exponent in (6, 8, 10, 12, 16):
        M = 1 << exponent
        L = M // exponent
        width = max(1, L // 2)
        lower = (L - width + 1) * equality_cost(M - 2)
        upper = equality_cost(M) + L * exponent
        symbolic.append({"M": M, "L": L, "width": width,
                         "log2_n": exponent + L * math.log2(M - 2),
                         "proven_cost_ratio_lower": float(lower / upper)})
    return {"bellman_exhaustive_cases": bellman_cases,
            "maximum_small_search_states": maximum_search_states,
            "race_pointwise_path_checks": race_paths,
            "balance_menu_rectangle_checks": barrier_states,
            "equality_potential_checks": potential_equalities,
            "finite_fixtures": fixtures, "positive_banded_menu": positive_fixtures,
            "deterministic_root_rare_band": deterministic_fixtures,
            "symbolic_scaling": symbolic}


if __name__ == "__main__":
    result = run_checks()
    path = Path(__file__).with_name("research-general-bounded-menu-results.json")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
