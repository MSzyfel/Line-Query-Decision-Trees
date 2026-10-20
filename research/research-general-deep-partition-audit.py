"""Independent bounded audit of the downward-closed partition LP theorem.

The exact all-subset DPs are validation only. They are not polynomial-time
candidate algorithms, LP optimizers, or inputs to the branching procedure.
"""

from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BASE = load("deep_partition_base", "research-general-multiscale-partition.py")
BACK = BASE.BACK


def indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def restrict(instance, policy, state, acceptable):
    if acceptable(state) or policy.test < 0:
        return BACK.Tree(state)
    hit = state & instance.tests[policy.test]
    miss = state ^ hit
    if not hit:
        return restrict(instance, policy.right, state, acceptable)
    if not miss:
        return restrict(instance, policy.left, state, acceptable)
    return instance.branch(state, policy.test,
                           restrict(instance, policy.left, hit, acceptable),
                           restrict(instance, policy.right, miss, acceptable))


def profile(instance, tree, acceptable):
    depths, settled = [0] * instance.n, 0
    BASE.validate_tree(instance, tree)
    for node in BASE.leaves(tree):
        if acceptable(node.state):
            settled |= node.state
    stack = [(tree, 0)]
    while stack:
        node, depth = stack.pop()
        if node.test < 0:
            for h in indices(node.state):
                depths[h] = depth
        else:
            stack.extend(((node.left, depth+1), (node.right, depth+1)))
    assert sum(depths[h] for h in indices(tree.state)) == tree.cost
    return tuple(depths), settled


def compile_partition_cover(instance, policies, weights, acceptable):
    profiles = [profile(instance, p, acceptable) for p in policies]
    prices = tuple(sum(x * depths[h] for x, (depths, _) in zip(weights, profiles))
                   for h in range(instance.n))
    coverage = tuple(sum(x for x, (_, settled) in zip(weights, profiles) if settled >> h & 1)
                     for h in range(instance.n))
    assert min(coverage) >= 1
    objective = sum(x*p.cost for x, p in zip(weights, policies))
    assert sum(prices) == objective
    calls = []

    def potential(state):
        return sum(prices[h] for h in indices(state))

    def build(state):
        if acceptable(state):
            return BACK.Tree(state)
        candidates, total = [], Fraction(0)
        for p, x, (_, settled) in zip(policies, weights, profiles):
            if x == 0:
                continue
            restricted = restrict(instance, p, state, acceptable)
            work_minus_credit = restricted.cost - potential(state & settled)
            total += x * work_minus_credit
            if state & settled:
                candidates.append((work_minus_credit, restricted))
        assert total <= 0
        score, chosen = min(candidates, key=lambda item: item[0])
        assert score <= 0
        calls.append(state)
        assert len(calls) <= instance.n

        def graft(node):
            if node.test < 0:
                return build(node.state)
            return instance.branch(node.state, node.test, graft(node.left), graft(node.right))

        tree = graft(chosen)
        assert tree.cost <= potential(state)
        return tree

    result = build(instance.full)
    _, settled = profile(instance, result, acceptable)
    assert settled == instance.full and result.cost <= objective
    return len(calls)


def audit_one(instance, acceptable):
    @lru_cache(None)
    def optimum(state):
        if acceptable(state):
            return BACK.Tree(state)
        candidates = []
        for q, test in enumerate(instance.tests):
            hit, miss = state & test, state & ~test
            if hit and miss:
                candidates.append(instance.branch(state, q, optimum(hit), optimum(miss)))
        return min(candidates, key=lambda tree: tree.cost)

    best = optimum(instance.full)
    prizes, complete = profile(instance, best, acceptable)
    assert complete == instance.full

    @lru_cache(None)
    def profit(state):
        if acceptable(state):
            return sum(prizes[h] for h in indices(state))
        value = 0
        for test in instance.tests:
            hit, miss = state & test, state & ~test
            if hit and miss:
                value = max(value, profit(hit)+profit(miss)-state.bit_count())
        return value

    assert profit(instance.full) == 0
    # Every pruning of the known optimal template is an actual column. A
    # full best-tree column of weight1 supplies coverage; add strictly
    # positive fractional, partially productive columns to test overcover.
    prefixes = BASE.all_prefixes(instance, best)
    partials = [p for p in prefixes if profile(instance, p, acceptable)[1] not in (0, instance.full)]
    selected = partials[:3]
    policies = [best, *selected]
    weights = [Fraction(1), *(Fraction(i+1, 5) for i in range(len(selected)))]
    calls = compile_partition_cover(instance, policies, weights, acceptable)
    return len(prefixes), calls, profit.cache_info().currsize


def main():
    rng = random.Random(202610194)
    cases = prefixes = calls = subset_values = 0
    for n in range(2, 9):
        for repeat in range(4):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests.extend(1 << h for h in range(n))
            instance = BACK.Instance(n, tests)
            cap = max(1, n//2)
            edges = tuple((1 << h) | (1 << j) for h in range(n) for j in range(h)
                          if rng.randrange(3) == 0)
            for acceptable in (lambda state, cap=cap: state.bit_count() <= cap,
                               lambda state, edges=edges: not any(state & e == e for e in edges)):
                a, b, c = audit_one(instance, acceptable)
                cases += 1
                prefixes += a
                calls += b
                subset_values += c
    result = {"status": "bounded audit only; no LP optimizer or unrestricted approximation",
              "downward_closed_instances": cases, "template_prefix_columns_checked": prefixes,
              "productive_compiler_calls": calls, "exact_profit_subset_values": subset_values,
              "target_families": ["fixed cardinality cap", "forbidden-pair independent sets"]}
    Path(__file__).with_name("research-general-deep-partition-audit-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
