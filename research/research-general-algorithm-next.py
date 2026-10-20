"""Polynomial code harvesting with quadratic intersection synthesis.

All parameters are fixed: no horizon growing with n is enumerated.
Theoretical iteration bound is integer external-path-length descent.
Small-instance optimal costs are validation oracles, NOT algorithm inputs.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from functools import lru_cache
import json
import random

@dataclass(frozen=True)
class Tree:
    state: int
    test: int = -1
    left: "Tree | None" = None
    right: "Tree | None" = None
    cost: int = 0


def tree_nodes(tree):
    stack = [tree]
    while stack:
        item = stack.pop()
        yield item
        if item.test >= 0:
            stack.extend((item.left, item.right))


class Instance:
    def __init__(self, n, tests):
        self.n = n
        self.full = (1 << n) - 1
        self.tests = tuple(dict.fromkeys(tests))
        self.greedy = lru_cache(None)(self._greedy)

    def branch(self, state, test, left, right):
        return Tree(state, test, left, right,
                    state.bit_count() + left.cost + right.cost)

    def _greedy(self, state):
        if state.bit_count() <= 1:
            return Tree(state)
        options = []
        for i, test in enumerate(self.tests):
            hit = state & test
            if hit and hit != state:
                options.append((max(hit.bit_count(), (state ^ hit).bit_count()), i))
        _, test = min(options)
        hit = state & self.tests[test]
        return self.branch(state, test, self.greedy(hit), self.greedy(state ^ hit))

    def verification_first(self, target):
        """Root-proposed extra generator: greedy h-oriented verification spine."""
        target_bit = 1 << target

        def build(state):
            if state.bit_count() <= 1:
                return Tree(state)
            options = []
            for i, test in enumerate(self.tests):
                hit = state & test
                if hit and hit != state:
                    h_side = hit if hit & target_bit else state ^ hit
                    options.append((h_side.bit_count(), i))
            _, test = min(options)
            hit = state & self.tests[test]
            miss = state ^ hit
            if hit & target_bit:
                return self.branch(state, test, build(hit), self.greedy(miss))
            return self.branch(state, test, self.greedy(hit), build(miss))

        return build(self.full)

    def represented_dp(self, family):
        values = {0: 0}
        choices = {}
        for state in sorted(family, key=int.bit_count):
            if state.bit_count() <= 1:
                values[state] = 0
                continue
            best = None
            for i, test in enumerate(self.tests):
                hit = state & test
                miss = state ^ hit
                if hit and miss and hit in values and miss in values:
                    candidate = (state.bit_count() + values[hit] + values[miss], i)
                    if best is None or candidate < best:
                        best = candidate
            if best is None:
                raise AssertionError(("unsupported complete code", state))
            values[state], choices[state] = best

        def reconstruct(state):
            if state.bit_count() <= 1:
                return Tree(state)
            test = choices[state]
            hit = state & self.tests[test]
            return self.branch(state, test, reconstruct(hit), reconstruct(state ^ hit))

        return reconstruct(self.full), values

    def prune(self, tree, state):
        if state.bit_count() <= 1:
            return Tree(state)
        hit = state & self.tests[tree.test]
        miss = state ^ hit
        if not hit:
            return self.prune(tree.right, state)
        if not miss:
            return self.prune(tree.left, state)
        return self.branch(state, tree.test,
                           self.prune(tree.left, hit), self.prune(tree.right, miss))

    def profit_fragment(self, family, incumbent):
        """Exact prize-work separation over all supported stopping policies.

        Prizes are INCUMBENT leaf depths.  A stop at a nonsingleton gives
        no prize.  Singleton leaves give their prize for free.
        """
        weights = {}

        def depths(tree, depth=0):
            if tree.test < 0:
                weights[tree.state] = depth
            else:
                depths(tree.left, depth + 1)
                depths(tree.right, depth + 1)

        depths(incumbent)
        values = {0: 0}
        actions = {}
        for state in sorted(family, key=int.bit_count):
            if state.bit_count() <= 1:
                values[state] = weights.get(state, 0)
                continue
            best = (0, -1)  # Explicitly stop unresolved.
            for i, test in enumerate(self.tests):
                hit = state & test
                miss = state ^ hit
                if hit and miss and hit in values and miss in values:
                    candidate = (values[hit] + values[miss] - state.bit_count(), i)
                    if candidate[0] > best[0]:
                        best = candidate
            values[state], actions[state] = best

        def splice(state):
            if state.bit_count() <= 1:
                return Tree(state)
            test = actions[state]
            if test < 0:
                return self.prune(incumbent, state)
            hit = state & self.tests[test]
            return self.branch(state, test, splice(hit), splice(state ^ hit))

        result = splice(self.full)
        profit = values[self.full]
        assert result.cost <= incumbent.cost - profit
        return result, profit

    def synthesize(self, incumbent=None, close_intersections=True,
                   verification_templates=False):
        incumbent = incumbent or self.greedy(self.full)
        base = {0}
        if verification_templates:
            for target in range(self.n):
                base.update(node.state for node in tree_nodes(self.verification_first(target)))
        history = []
        max_passes = incumbent.cost + 1
        for pass_index in range(max_passes):
            incumbent_nodes = tuple(tree_nodes(incumbent))
            base.update(node.state for node in incumbent_nodes)
            # Complete conditional code generation, only at <=2n-1 current nodes.
            for node in incumbent_nodes:
                state = node.state
                if state.bit_count() <= 1:
                    continue
                for test in self.tests:
                    hit = state & test
                    if not hit or hit == state:
                        continue
                    for child in (hit, state ^ hit):
                        base.update(v.state for v in tree_nodes(self.greedy(child)))
            # Baseline DP is a diagnostic; intersection closure is the new step.
            baseline_tree, _ = self.represented_dp(base)
            family = set(base)
            if close_intersections:
                base_items = tuple(base)
                for i, a in enumerate(base_items):
                    family.update(a & b for b in base_items[i + 1:])
            candidate, _ = self.represented_dp(family)
            assert candidate.cost <= baseline_tree.cost <= incumbent.cost
            fragment_candidate, profit = self.profit_fragment(family, incumbent)
            assert fragment_candidate.cost <= candidate.cost
            history.append({
                "pass": pass_index,
                "incumbent_cost": incumbent.cost,
                "base_states": len(base), "represented_states": len(family),
                "base_dp_cost": baseline_tree.cost,
                "intersection_dp_cost": candidate.cost,
                "maximum_prize_work_profit": profit,
                "fragment_splice_cost": fragment_candidate.cost,
            })
            if profit == 0:
                assert fragment_candidate.cost == incumbent.cost
                return incumbent, history
            incumbent = fragment_candidate
        raise AssertionError("Integer-descent termination bound exceeded")

    def exact_cost(self):
        @lru_cache(None)
        def solve(state):
            if state.bit_count() <= 1:
                return 0
            return state.bit_count() + min(
                solve(hit) + solve(state ^ hit)
                for test in self.tests
                if (hit := state & test) and hit != state
            )
        return solve(self.full)


def random_instance(rng, n=12, m=8):
    # Unique biased response words ensure separation without supplying an
    # artificial balanced encoding that would make almost every case easy.
    words = set()
    probabilities = [rng.choice((0.12, 0.2, 0.3, 0.5)) for _ in range(m)]
    while len(words) < n:
        word = sum((rng.random() < p) << bit
                   for bit, p in enumerate(probabilities))
        words.add(word)
    ordered = sorted(words)
    tests = [sum(1 << h for h, word in enumerate(ordered) if word >> bit & 1)
             for bit in range(m)]
    tests = [test for test in tests if test and test != (1 << n) - 1]
    rng.shuffle(tests)
    return Instance(n, tests)


def paired_instance(b=3, c=6):
    # Import the independently audited adversary without requiring a module name
    # change to its user-facing hyphenated filename.
    import importlib.util
    from pathlib import Path
    import sys
    path = Path(__file__).with_name("research-general-continuation.py")
    spec = importlib.util.spec_from_file_location("paired_adversary", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    tests, nodes, root = module.paired_instance(b, c)
    instance = Instance(c * (1 << b), [mask for _, mask in tests])
    built = []
    for node in nodes:
        if node.left < 0:
            built.append(Tree(node.mask))
        else:
            left, right = built[node.left], built[node.right]
            test = next(i for i, positive in enumerate(instance.tests)
                        if node.mask & positive == left.state)
            built.append(instance.branch(node.mask, test, left, right))
    return instance, built[root]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--random-cases", type=int, default=100)
    parser.add_argument("--adversary-b", type=int, default=3)
    parser.add_argument("--verification-templates", action="store_true")
    args = parser.parse_args()
    rng = random.Random(190611385)
    strict = intersection_helped = optimal = 0
    worst_ratio = 1.0
    example = None
    suboptimal_example = None
    for _ in range(args.random_cases):
        instance = random_instance(rng)
        result, history = instance.synthesize(
            verification_templates=args.verification_templates
        )
        optimum = instance.exact_cost()
        assert optimum <= result.cost <= instance.greedy(instance.full).cost
        strict += result.cost < instance.greedy(instance.full).cost
        intersection_helped += any(
            p["intersection_dp_cost"] < p["base_dp_cost"] for p in history
        )
        optimal += result.cost == optimum
        worst_ratio = max(worst_ratio, result.cost / optimum)
        if suboptimal_example is None and result.cost > optimum:
            suboptimal_example = {
                "tests": list(instance.tests), "optimum": optimum,
                "greedy_cost": instance.greedy(instance.full).cost,
                "output_cost": result.cost, "history": history,
            }
        if example is None and any(
            p["intersection_dp_cost"] < p["base_dp_cost"] for p in history
        ):
            example = {"tests": list(instance.tests), "optimum": optimum,
                       "history": history}
    print(json.dumps({"random_validation": {
        "cases": args.random_cases, "n": 12,
        "verification_templates": args.verification_templates,
        "strictly_improved_greedy": strict,
        "intersection_closure_strictly_helped": intersection_helped,
        "optimal_outputs": optimal, "worst_observed_ratio": worst_ratio,
        "first_intersection_example": example,
        "first_suboptimal_example": suboptimal_example,
    }}))
    instance, bad = paired_instance(args.adversary_b, 6)
    result, history = instance.synthesize(
        bad, verification_templates=args.verification_templates
    )
    print(json.dumps({"paired_pruning_plateau": {
        "n": instance.n, "m": len(instance.tests),
        "incumbent_mean": bad.cost / instance.n,
        "synthesized_mean": result.cost / instance.n,
        "greedy_mean": instance.greedy(instance.full).cost / instance.n,
        "history": history,
    }}))


if __name__ == "__main__":
    main()
