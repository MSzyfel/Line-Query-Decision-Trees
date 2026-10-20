"""Compile feasible branching-policy LP points into small-cell partitions.

Exact Fractions; original binary tests; explicit long macro actions allowed.
There is no LP optimizer and no unrestricted optimum oracle in this checker.
"""

from dataclasses import dataclass, field
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


BACK = load("menu_partition_lp_backend", "research-general-algorithm-next.py")


def indices(state):
    while state:
        bit = state & -state
        yield bit.bit_length()-1
        state ^= bit


def profile(instance, policy):
    """Validate every original-test path of an explicit partial policy."""
    depths = {}
    leaf_masks = set()
    for h in indices(policy.state):
        node, depth = policy, 0
        while node.test >= 0:
            hit = node.state & instance.tests[node.test]
            assert hit and hit != node.state
            assert node.left.state == hit and node.right.state == node.state ^ hit
            assert node.cost == node.state.bit_count()+node.left.cost+node.right.cost
            node = node.left if hit >> h & 1 else node.right
            depth += 1
        assert node.state >> h & 1 and node.cost == 0
        depths[h] = depth
        leaf_masks.add(node.state)
    assert sum(depths.values()) == policy.cost
    assert sum(mask.bit_count() for mask in leaf_masks) == policy.state.bit_count()
    return depths, leaf_masks


@dataclass
class Action:
    policy: object
    children: dict = field(default_factory=dict)


@dataclass
class Occurrence:
    state: int
    level: int
    actions: list = field(default_factory=list)


def unfold(instance, menu, horizon, cap):
    """Unfold occurrences; do not assume equal-state policy consistency."""
    assert horizon >= 0 and cap >= 1
    occurrences = []

    def visit(state, level):
        index = len(occurrences)
        occurrence = Occurrence(state, level)
        occurrences.append(occurrence)
        if state.bit_count() <= cap or level == horizon:
            return index
        for policy in menu(state):
            assert policy.state == state
            _, leaves = profile(instance, policy)
            action = Action(policy)
            occurrence.actions.append(action)
            for leaf in sorted(leaves):
                action.children[leaf] = visit(leaf, level+1)
        return index

    visit(instance.full, 0)
    maximum_menu = max(len(item.actions) for item in occurrences)
    by_level = [sum(item.state.bit_count() for item in occurrences if item.level == level)
                for level in range(horizon+1)]
    assert all(mass <= instance.n * maximum_menu**level
               for level, mass in enumerate(by_level))
    return occurrences, {"occurrences": len(occurrences), "mass_by_level": by_level,
                         "maximum_menu": maximum_menu, "horizon": horizon}


def feasible_random_point(occurrences, cap, rng):
    """Generate a feasible exact point by scaling a stochastic partial policy.

    Half-cut actions guarantee positive coverage within the chosen horizon.
    This supplies a checker input, not an LP optimization routine.
    """
    incoming = [Fraction(0)]*len(occurrences)
    actions = {}
    incoming[0] = Fraction(1)
    for u, occurrence in enumerate(occurrences):
        count = len(occurrence.actions)
        if not count:
            continue
        weights = [rng.randrange(1, 5) for _ in range(count+1)]
        denominator = sum(weights)  # Last weight stops unfinished.
        for a, action in enumerate(occurrence.actions):
            value = incoming[u]*Fraction(weights[a], denominator)
            actions[u, a] = value
            for child in action.children.values():
                incoming[child] = value
    n = occurrences[0].state.bit_count()
    coverage = [sum(incoming[u] for u, item in enumerate(occurrences)
                    if item.state.bit_count() <= cap and item.state >> h & 1)
                for h in range(n)]
    assert min(coverage) > 0
    scale = 1/min(coverage)
    return [scale*value for value in incoming], {key: scale*value for key, value in actions.items()}


def compile_point(instance, occurrences, cap, incoming, action_weights):
    """Validate an LP point and compile it without explicitly decomposing it."""
    assert occurrences[0].state == instance.full and len(incoming) == len(occurrences)
    incoming = tuple(Fraction(value) for value in incoming)
    assert all(value >= 0 for value in incoming)
    valid_actions = {(u, a) for u, occurrence in enumerate(occurrences)
                     for a in range(len(occurrence.actions))}
    assert set(action_weights) <= valid_actions
    child_indices = [child for occurrence in occurrences for action in occurrence.actions
                     for child in action.children.values()]
    assert sorted(child_indices) == list(range(1, len(occurrences)))
    coverage = [Fraction(0)]*instance.n
    prices = [Fraction(0)]*instance.n
    objective = Fraction(0)
    for u, occurrence in enumerate(occurrences):
        if occurrence.state.bit_count() <= cap:
            assert not occurrence.actions
            for h in indices(occurrence.state):
                coverage[h] += incoming[u]
        used = Fraction(0)
        for a, action in enumerate(occurrence.actions):
            value = Fraction(action_weights.get((u, a), 0))
            assert value >= 0
            used += value
            depths, leaves = profile(instance, action.policy)
            assert set(action.children) == leaves
            for mask, child in action.children.items():
                assert occurrences[child].state == mask
                assert occurrences[child].level == occurrence.level+1
                assert incoming[child] == value
            objective += value*action.policy.cost
            for h, depth in depths.items():
                prices[h] += value*depth
        assert used <= incoming[u]
    assert min(coverage) >= 1 and sum(prices) == objective
    stages = []
    restricted_problems = 0

    def potential(state):
        return sum(prices[h] for h in indices(state))

    def profit_policy(state):
        nonlocal restricted_problems
        restricted_problems += 1

        @lru_cache(None)
        def best(u, actual):
            occurrence = occurrences[u]
            assert actual and actual & occurrence.state == actual
            if actual.bit_count() <= cap:
                return BACK.Tree(actual), (potential(actual), actual.bit_count())
            result = BACK.Tree(actual), (Fraction(0), 0)
            for action in occurrence.actions:
                def within(node, current):
                    if current.bit_count() <= cap:
                        return BACK.Tree(current), (potential(current), current.bit_count())
                    if node.test < 0:
                        return best(action.children[node.state], current)
                    hit = current & instance.tests[node.test]
                    miss = current ^ hit
                    if not hit:
                        return within(node.right, current)
                    if not miss:
                        return within(node.left, current)
                    left, left_score = within(node.left, hit)
                    right, right_score = within(node.right, miss)
                    score = (left_score[0]+right_score[0]-current.bit_count(),
                             left_score[1]+right_score[1])
                    return instance.branch(current, node.test, left, right), score

                candidate = within(action.policy, actual)
                if candidate[1] > result[1]:
                    result = candidate
            return result

        return best(0, state)

    @lru_cache(None)
    def build(state):
        if state.bit_count() <= cap:
            return BACK.Tree(state)
        partial, score = profit_policy(state)
        depths, leaves = profile(instance, partial)
        settled = sum(mask.bit_count() for mask in leaves if mask.bit_count() <= cap)
        assert score[0] >= 0 and score[1] == settled and settled > 0
        stages.append({"population": state.bit_count(), "actual_work": partial.cost,
                       "settled": settled, "profit": str(score[0])})
        assert len(stages) <= instance.n

        def finish(node):
            if node.test < 0:
                return build(node.state)
            return instance.branch(node.state, node.test, finish(node.left), finish(node.right))

        result = finish(partial)
        assert result.cost <= potential(state)
        return result

    result = build(instance.full)
    _, leaves = profile(instance, result)
    assert all(mask.bit_count() <= cap for mask in leaves)
    assert result.cost <= objective
    return result, {"LP_point_objective": str(objective), "actual_work": result.cost,
                    "size_cap": cap, "accepted_cells": len(leaves),
                    "productive_applications": len(stages), "stages": stages,
                    "minimum_coverage": str(min(coverage)),
                    "root_policy_weight": str(incoming[0]),
                    "restricted_profit_DPs": restricted_problems,
                    "uses_an_LP_optimizer": False}


def half_cut(instance, state):
    target = max(1, state.bit_count()//2)

    def prune(node):
        if node.state.bit_count() <= target:
            return BACK.Tree(node.state)
        return instance.branch(node.state, node.test, prune(node.left), prune(node.right))

    return prune(instance.greedy(state))


def menu_for(instance):
    def menu(state):
        cut = half_cut(instance, state)
        options = []
        for q, test in enumerate(instance.tests):
            hit = state & test
            if hit and hit != state:
                options.append((min(hit.bit_count(), (state ^ hit).bit_count()), q))
        _, q = min(options)
        hit = state & instance.tests[q]
        question = instance.branch(state, q, BACK.Tree(hit), BACK.Tree(state ^ hit))
        return cut, question
    return menu


def complementary_partial_fixture(cap):
    """Two genuinely partial columns, total policy weight2, adaptive reuse."""
    instance = BACK.Instance(16, [sum(1 << h for h in range(8))]
                             + [sum(1 << h for h in range(16) if h >> bit & 1)
                                for bit in range(4)])
    left_state = instance.tests[0]
    right_state = instance.full ^ left_state

    def cut(node):
        if node.state.bit_count() <= cap:
            return BACK.Tree(node.state)
        return instance.branch(node.state, node.test, cut(node.left), cut(node.right))

    first = instance.branch(instance.full, 0, cut(instance.greedy(left_state)), BACK.Tree(right_state))
    second = instance.branch(instance.full, 0, BACK.Tree(left_state), cut(instance.greedy(right_state)))
    occurrences, unfolding = unfold(instance, lambda state: (first, second), 1, cap)
    incoming = [Fraction(1)]*len(occurrences)
    incoming[0] = Fraction(2)
    weights = {(0, 0): Fraction(1), (0, 1): Fraction(1)}
    _, stats = compile_point(instance, occurrences, cap, incoming, weights)
    assert stats["productive_applications"] == 2
    assert stats["root_policy_weight"] == "2" and stats["minimum_coverage"] == "1"
    assert stats["actual_work"] < Fraction(stats["LP_point_objective"])
    return {"n": instance.n, "complementary_partial_policies": True, **unfolding, **stats}


def main():
    rng = random.Random(20261019091)
    results = []
    for n in range(3, 13):
        for cap in sorted({1, max(1, n//3), max(1, n//2)}):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(6)]
            tests += [1 << h for h in range(n)]
            instance = BACK.Instance(n, tests)
            horizon = n.bit_length()
            occurrences, unfolding = unfold(instance, menu_for(instance), horizon, cap)
            incoming, action_weights = feasible_random_point(occurrences, cap, rng)
            _, stats = compile_point(instance, occurrences, cap, incoming, action_weights)
            results.append({"n": n, **unfolding, **stats})
    results.extend(complementary_partial_fixture(cap) for cap in (1, 2))
    # Only singleton tests: the first action has a genuinely long spine,
    # while logarithmically many macro choices still suffice to partition.
    instance = BACK.Instance(32, [1 << h for h in range(32)])
    occurrences, unfolding = unfold(instance, menu_for(instance), 5, 2)
    incoming, action_weights = feasible_random_point(occurrences, 2, rng)
    tree, stats = compile_point(instance, occurrences, 2, incoming, action_weights)
    first_depths, _ = profile(instance, occurrences[0].actions[0].policy)
    assert max(first_depths.values()) == 16
    results.append({"n": 32, "singleton_only": True,
                    "first_macro_primitive_depth": max(first_depths.values()),
                    **unfolding, **stats})
    output = {"checked_points": len(results),
              "total_virtual_occurrences": sum(item["occurrences"] for item in results),
              "total_productive_applications": sum(item["productive_applications"] for item in results),
              "uses_an_LP_optimizer": False, "results": results}
    Path(__file__).with_name("research-general-menu-partition-lp-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items() if key != "results"}, indent=2))


if __name__ == "__main__":
    main()
