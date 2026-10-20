"""Bounded audits of the graph-gated factorial 2-approximation.

The algorithm uses at most product(M_i) count states. Exact unrestricted
optimization below is a validation oracle restricted to n <= 16.
"""

from __future__ import annotations

from collections import defaultdict
from fractions import Fraction
from functools import lru_cache
import importlib.util
from itertools import product
import json
from math import prod
from pathlib import Path
import sys


def load_backend():
    path = Path(__file__).with_name("research-general-algorithm-next.py")
    spec = importlib.util.spec_from_file_location("dependency_graph_backend", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BACK = load_backend()
Instance, Tree, tree_nodes = BACK.Instance, BACK.Tree, BACK.tree_nodes


class ActivationDP:
    def __init__(self, sizes, parents):
        self.sizes = tuple(sizes)
        self.parents = tuple(tuple(sorted(set(row))) for row in parents)
        self.d = len(sizes)
        self.actions = {}
        self.values = {}
        self.solve = lru_cache(None)(self._solve)

    def close(self, counts):
        counts = list(counts)
        changed = True
        while changed:
            changed = False
            for i, pa in enumerate(self.parents):
                if counts[i] > 1 and all(counts[p] == 1 for p in pa):
                    counts[i], changed = 1, True
        return tuple(counts)

    def _solve(self, counts):
        closed = self.close(counts)
        if closed != counts:
            value = self.solve(closed)
        elif max(counts) == 1:
            value = Fraction(0)
        else:
            options = []
            for i, count in enumerate(counts):
                if count == 1:
                    continue
                hit, miss = list(counts), list(counts)
                hit[i], miss[i] = 1, count - 1
                value = (1 + self.solve(tuple(hit)) / count
                         + Fraction(count - 1, count) * self.solve(tuple(miss)))
                options.append((value, i))
            value, self.actions[counts] = min(options)
        self.values[counts] = value
        raw = prod(counts) * value
        assert raw.denominator == 1
        assert 0 <= raw <= prod(counts) * sum(m - 1 for m in self.sizes)
        return value


class ChargedActivationDP(ActivationDP):
    """Charge c_i >= 1 whenever a still-unknown coordinate is revealed free.

    Positive/last-negative paid equalities already identify their coordinate
    and are not charged again. Root activations are charged at the initial
    closure, just as at every later closure.
    """

    def __init__(self, sizes, parents, charges):
        self.charges = tuple(charges)
        assert len(charges) == len(sizes) and min(charges) >= 1
        super().__init__(sizes, parents)

    def _solve(self, counts):
        closed = self.close(counts)
        if closed != counts:
            charge = sum(self.charges[i] for i in range(self.d)
                         if counts[i] > 1 and closed[i] == 1)
            value = charge + self.solve(closed)
        elif max(counts) == 1:
            value = Fraction(0)
        else:
            options = []
            for i, count in enumerate(counts):
                if count == 1:
                    continue
                hit, miss = list(counts), list(counts)
                hit[i], miss[i] = 1, count - 1
                value = (1 + self.solve(tuple(hit)) / count
                         + Fraction(count - 1, count) * self.solve(tuple(miss)))
                options.append((value, i))
            value, self.actions[counts] = min(options)
        self.values[counts] = value
        raw = prod(counts) * value
        assert raw.denominator == 1
        assert 0 <= raw <= prod(counts) * (
            sum(m - 1 for m in self.sizes) + sum(self.charges))
        return value


class GraphInstance:
    def __init__(self, m, parents):
        assert m >= 2 and m & (m - 1) == 0
        self.m, self.b, self.d = m, m.bit_length() - 1, len(parents)
        self.parents = tuple(tuple(sorted(set(pa))) for pa in parents)
        self.points = tuple(product(range(m), repeat=self.d))
        self.n = len(self.points)
        tests, metadata, lookup = [], [], {}

        def add(mask, desc):
            if not mask or mask == (1 << self.n) - 1:
                return None
            if mask not in lookup:
                lookup[mask] = len(tests)
                tests.append(mask)
                metadata.append(desc)
            return lookup[mask]

        self.eq, self.gate = {}, {}
        for i in range(self.d):
            for value in range(m):
                mask = sum(1 << h for h, x in enumerate(self.points) if x[i] == value)
                self.eq[i, value] = add(mask, ("eq", i, value))
        for i, pa in enumerate(self.parents):
            for context in product(range(m), repeat=len(pa)):
                for bit in range(self.b):
                    mask = sum(1 << h for h, x in enumerate(self.points)
                               if all(x[p] == a for p, a in zip(pa, context))
                               and (x[i] >> bit) & 1)
                    self.gate[i, context, bit] = add(mask, ("gate", i, context, bit))
        self.instance = Instance(self.n, tests)
        self.metadata = tuple(metadata)
        assert self.instance.tests == tuple(tests)

    @lru_cache(None)
    def state(self, candidates):
        return sum(1 << h for h, x in enumerate(self.points)
                   if all(mask >> value & 1 for mask, value in zip(candidates, x)))

    def close_for_target(self, candidates, target):
        candidates = list(candidates)
        changed = True
        while changed:
            changed = False
            for i, pa in enumerate(self.parents):
                if (candidates[i].bit_count() > 1
                        and all(candidates[p].bit_count() == 1 for p in pa)):
                    candidates[i], changed = 1 << target[i], True
        return tuple(candidates)


def physical_code(model, dp):
    instance = model.instance

    @lru_cache(None)
    def build(candidates):
        state = model.state(candidates)
        if state.bit_count() == 1:
            return Tree(state), 0, 0
        enabled = [i for i, pa in enumerate(model.parents)
                   if candidates[i].bit_count() > 1
                   and all(candidates[p].bit_count() == 1 for p in pa)]
        updated = list(candidates)
        if enabled:
            i = enabled[0]
            bit = next(j for j in range(model.b)
                       if 0 < sum((v >> j & 1) for v in range(model.m)
                                  if candidates[i] >> v & 1)
                       < candidates[i].bit_count())
            context = tuple(candidates[p].bit_length() - 1 for p in model.parents[i])
            test = model.gate[i, context, bit]
            assert test is not None
            left_mask = sum(1 << v for v in range(model.m)
                            if candidates[i] >> v & 1 and v >> bit & 1)
            paid = False
        else:
            counts = tuple(mask.bit_count() for mask in candidates)
            assert dp.close(counts) == counts
            dp.solve(counts)
            i = dp.actions[counts]
            value = (candidates[i] & -candidates[i]).bit_length() - 1
            test, left_mask, paid = model.eq[i, value], 1 << value, True
        updated[i] = left_mask
        left, left_paid, left_bits = build(tuple(updated))
        updated[i] = candidates[i] ^ left_mask
        right, right_paid, right_bits = build(tuple(updated))
        assert left.state == state & instance.tests[test]
        assert right.state == state ^ left.state
        return (instance.branch(state, test, left, right),
                left_paid + right_paid + (state.bit_count() if paid else 0),
                left_bits + right_bits + (0 if paid else state.bit_count()))

    return build(((1 << model.m) - 1,) * model.d)


def validate(model, tree):
    instance = model.instance
    leaves = 0
    for node in tree_nodes(tree):
        if node.test < 0:
            assert node.state.bit_count() == 1
            leaves += 1
        else:
            hit = node.state & instance.tests[node.test]
            assert hit and node.state ^ hit
            assert node.left.state == hit and node.right.state == node.state ^ hit
            assert node.cost == node.state.bit_count() + node.left.cost + node.right.cost
    assert leaves == model.n and tree.state == instance.full
    assert sum(1 for _ in tree_nodes(tree)) == 2 * model.n - 1


def exact_code(model):
    assert model.n <= 16, "validation oracle only"
    instance = model.instance

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return Tree(state)
        options = []
        for q, mask in enumerate(instance.tests):
            hit = state & mask
            if hit and hit != state:
                left, right = solve(hit), solve(state ^ hit)
                options.append(instance.branch(state, q, left, right))
        return min(options, key=lambda node: (node.cost, node.test))

    return solve(instance.full)


def simulate(model, tree, dp):
    """Full stronger histories remain product cells, checked at every node."""
    groups = defaultdict(lambda: [0, 0])
    total = total_charged = 0
    for h, target in enumerate(model.points):
        initial = ((1 << model.m) - 1,) * model.d
        candidates = model.close_for_target(initial, target)
        activated = {i for i in range(model.d)
                     if initial[i].bit_count() > 1 and candidates[i].bit_count() == 1}
        positives = set()
        paid_h = depth_h = 0

        def close(updated):
            closed = model.close_for_target(tuple(updated), target)
            for i in range(model.d):
                if updated[i].bit_count() > 1 and closed[i].bit_count() == 1:
                    assert i not in activated and i not in positives
                    activated.add(i)
            return closed

        node = tree
        while node.test >= 0:
            depth_h += 1
            start = candidates
            assert model.state(start) & node.state == model.state(start)
            desc = model.metadata[node.test]
            checks = 0
            if desc[0] == "eq":
                _, i, value = desc
                if candidates[i].bit_count() > 1 and candidates[i] >> value & 1:
                    update = list(candidates)
                    update[i] = ((1 << value) if target[i] == value
                                 else candidates[i] ^ (1 << value))
                    checks += 1
                    if target[i] == value:
                        assert i not in positives and i not in activated
                        positives.add(i)
                    candidates = close(update)
                answer = target[i] == value
            else:
                _, i, context, bit = desc
                answer = None
                for p, value in zip(model.parents[i], context):
                    if not candidates[p] >> value & 1:
                        answer = False
                        break
                    if candidates[p].bit_count() > 1:
                        update = list(candidates)
                        update[p] = ((1 << value) if target[p] == value
                                     else candidates[p] ^ (1 << value))
                        checks += 1
                        if target[p] == value:
                            assert p not in positives and p not in activated
                            positives.add(p)
                        candidates = close(update)
                        if target[p] != value:
                            answer = False
                            break
                if answer is None:
                    assert candidates[i].bit_count() == 1
                    answer = bool(target[i] >> bit & 1)
            assert answer == bool(model.instance.tests[node.test] >> h & 1)
            group = groups[id(node), start]
            group[0] += 1
            group[1] += checks
            total += checks
            paid_h += checks
            node = node.left if answer else node.right
        assert node.state == 1 << h
        assert paid_h <= depth_h + len(positives)
        assert not activated & positives
        charged_h = paid_h + model.b * len(activated)
        assert charged_h <= depth_h + model.b * model.d
        total_charged += charged_h
    for (node_id, candidates), (mass, checks) in groups.items():
        assert mass == prod(mask.bit_count() for mask in candidates)
        assert checks <= 2 * mass
    comparison = total_charged if isinstance(dp, ChargedActivationDP) else total
    assert dp.solve((model.m,) * model.d) <= Fraction(comparison, model.n)
    assert total <= 2 * tree.cost
    assert total_charged <= tree.cost + model.n * model.d * model.b
    return total, len(groups)


def main():
    cases = [
        (2, [(), ()]),
        (2, [(1,), (0,)]),
        (2, [(2,), (0,), (1,)]),
        (2, [(1, 2), (0, 2), (0, 1)]),
        (4, [(), (0,)]),
        (4, [(1,), (0,)]),
        (4, [(0,), ()]),
        (4, [(2,), (0,), (1,)]),
        (4, [(1, 2), (0, 2), (0, 1)]),
        (4, [(), (0,), (1,), (2,)]),
        (4, [(3,), (0,), (1,), (2,)]),
        (4, [(1, 2, 3), (0, 2, 3), (0, 1, 3), (0, 1, 2)]),
        (8, [(2,), (0,), (1,)]),
    ]
    rows, simulation_groups, exact_checks, integrality_checks = [], 0, 0, 0
    charged_integrality_checks = pathwise_checks = 0
    for m, parents in cases:
        model = GraphInstance(m, parents)
        dp = ActivationDP((m,) * model.d, parents)
        optimum_relaxation = dp.solve((m,) * model.d)
        tree, paid, palette = physical_code(model, dp)
        validate(model, tree)
        assert Fraction(paid, model.n) == optimum_relaxation
        assert palette <= model.n * model.d * model.b
        assert tree.cost == paid + palette
        assert len(dp.values) <= model.n
        charged_dp = ChargedActivationDP((m,) * model.d, parents, (model.b,) * model.d)
        charged_value = charged_dp.solve((m,) * model.d)
        charged_tree, charged_paid, charged_palette = physical_code(model, charged_dp)
        validate(model, charged_tree)
        assert charged_tree.cost <= model.n * charged_value
        assert charged_tree.cost == charged_paid + charged_palette
        assert len(charged_dp.values) <= model.n
        greedy = model.instance.greedy(model.instance.full)
        validate(model, greedy)
        _, groups = simulate(model, greedy, charged_dp)
        simulation_groups += groups
        pathwise_checks += model.n
        row = {"M": m, "parents": parents, "n": model.n,
               "tests": len(model.instance.tests), "count_states": len(dp.values),
               "relaxed_mean": str(optimum_relaxation),
               "legacy_actual_work": tree.cost, "greedy_work": greedy.cost,
               "charged_relaxed_mean": str(charged_value),
               "charged_count_states": len(charged_dp.values),
               "actual_work": charged_tree.cost}
        if model.n <= 16:
            exact = exact_code(model)
            validate(model, exact)
            _, groups = simulate(model, exact, charged_dp)
            simulation_groups += groups
            pathwise_checks += model.n
            assert charged_value <= Fraction(exact.cost, model.n) + model.d * model.b
            assert charged_tree.cost <= 2 * exact.cost
            row["optimal_work"] = exact.cost
            exact_checks += 1
        integrality_checks += len(dp.values)
        charged_integrality_checks += len(charged_dp.values)
        rows.append(row)
    result = {"cases": len(rows), "simulation_product_groups": simulation_groups,
              "small_exact_comparisons": exact_checks,
              "count_state_integrality_checks": integrality_checks,
              "charged_count_state_integrality_checks": charged_integrality_checks,
              "pathwise_charged_simulation_checks": pathwise_checks,
              "rows": rows}
    path = Path(__file__).with_suffix(".results.json")
    path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
