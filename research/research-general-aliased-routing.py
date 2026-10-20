"""Deterministic genuine-alias examples and root-star policy certificates.

No random search, exact OPT oracle, or unbounded-depth policy enumeration.
Every generated alias changes the meaning of an actual physical test on
several contexts.  A separate root-partial completion certificate is checked
without assuming those conditional codes can be replayed outside their core.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import importlib.util
from itertools import product
import json
import math
from pathlib import Path
import sys


def load_lifting():
    spec = importlib.util.spec_from_file_location(
        "aliased_routing_backend", Path(__file__).with_name("research-general-code-lifting.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LIFT = load_lifting()
Instance, Tree, tree_nodes = LIFT.Instance, LIFT.Tree, LIFT.tree_nodes


def hypotheses(state):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def affine_label(row, bits, alias_position):
    """Owner map and alias maps are different invertible affine maps."""
    full = (1 << bits) - 1
    if alias_position == 0:
        linear = row
    else:
        shift = 1 + (alias_position - 1) % (bits - 1)
        linear = ((row << shift) | (row >> (bits - shift))) & full
        # An invertible triangular shear after the coordinate permutation.
        for j in range(1, bits):
            if (alias_position + j) % 2:
                linear ^= ((linear >> (j - 1)) & 1) << j
    return linear ^ full


def is_affine_map(values):
    return all(values[x] ^ values[y] ^ values[0] == values[x ^ y]
               for x in range(len(values)) for y in range(len(values)))


def make_instance(bits, levels, degree, nonlinear=False):
    assert bits >= 2 and levels >= 1 and degree >= 2
    size = 1 << bits
    base_size = degree * size
    points = tuple(product(range(base_size), *(range(size) for _ in range(levels))))
    tests, tags = [], []
    maps = {a: tuple(affine_label(row, bits, a) for row in range(size))
            for a in range(degree)}
    if nonlinear:
        assert bits >= 3  # Every permutation of four points is affine.
        # A single output transposition after an invertible affine map.  Keep
        # row zero's all-one label, so the projection witness is unchanged.
        changed = list(maps[1])
        changed[1], changed[2] = changed[2], changed[1]
        maps[1] = tuple(changed)
        assert is_affine_map(maps[0]) and not is_affine_map(maps[1])
    assert all(sorted(values) == list(range(size)) for values in maps.values())
    assert maps[0] != maps[1]
    for k in range(1, levels + 1):
        ranges = (range(base_size), *(range(size) for _ in range(k - 1)))
        for origin in product(*ranges):
            active = {((origin[0] + a) % base_size, *origin[1:]): a
                      for a in range(degree)}
            for bit in range(bits):
                positive = 0
                for h, point in enumerate(points):
                    alias_position = active.get(point[:k])
                    if alias_position is not None and maps[alias_position][point[k]] >> bit & 1:
                        positive |= 1 << h
                tests.append(positive)
                tags.append(("bit", k, origin, bit))
    # Pure equality tie priority is descending factor order, after all bits.
    for k in range(levels, -1, -1):
        alphabet = size if k else base_size
        for value in range(alphabet):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[k] == value))
            tags.append(("eq", k, value))
    instance = Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    tag_index = {tag: j for j, tag in enumerate(tags)}
    cores = tuple(instance.tests[tag_index[("eq", 0, value)]] for value in range(base_size))
    return instance, points, tuple(tags), tag_index, cores, maps


def unbalanced_tree(instance):
    """A deliberately poor legal incumbent, only to exercise strict descent."""
    @lru_cache(None)
    def build(state):
        if state.bit_count() <= 1:
            return Tree(state)
        _, j = min((min(hit.bit_count(), (state ^ hit).bit_count()), j)
                   for j, test in enumerate(instance.tests)
                   if (hit := state & test) and hit != state)
        hit = state & instance.tests[j]
        return instance.branch(state, j, build(hit), build(state ^ hit))
    return build(instance.full)


def star_descent(instance, codes, selectors, initial):
    """Explicit root query + positive completion + incumbent negative fallback."""
    incumbent = initial
    history = []
    total_work = sum(instance.n + code.cost for code in codes)
    for _ in range(initial.cost + 1):
        weights = LIFT.BACK.depth_weights(incumbent)
        profits = []
        for code in codes:
            reward = sum(weights[1 << h] for h in hypotheses(code.state))
            profits.append(reward - instance.n - code.cost)
        assert sum(profits) == incumbent.cost - total_work
        profit, index = max((profit, i) for i, profit in enumerate(profits))
        if profit <= 0:
            assert incumbent.cost <= total_work
            history.append({"cost": incumbent.cost, "max_root_star_profit": profit,
                            "stable": True})
            return incumbent, history
        old_cost = incumbent.cost
        core = codes[index].state
        miss = instance.full ^ core
        incumbent = instance.branch(instance.full, selectors[index], codes[index],
                                    instance.prune(incumbent, miss))
        assert incumbent.cost <= old_cost - profit < old_cost
        history.append({"cost": old_cost, "max_root_star_profit": profit,
                        "candidate_cost": incumbent.cost, "completed_base_value": index})
    raise AssertionError("integer descent bound failed")


def check_case(bits, levels, degree, nonlinear=False):
    instance, points, tags, index, cores, maps = make_instance(bits, levels, degree, nonlinear)
    size, base_size = 1 << bits, degree * (1 << bits)
    initial = instance.greedy(instance.full)
    row_work = 0
    for node in tree_nodes(initial):
        if node.test < 0:
            continue
        unresolved = [k for k in range(1, levels + 1)
                      if len({points[h][k] for h in hypotheses(node.state)}) > 1]
        if unresolved:
            assert tags[node.test][0] == "eq" and tags[node.test][1] == max(unresolved)
            row_work += node.state.bit_count()
    expected_rows = instance.n * levels * (Fraction(size + 1, 2) - Fraction(1, size))
    assert row_work == expected_rows

    codes = tuple(instance.greedy(core) for core in cores)
    for source in codes:
        if nonlinear:
            assert source.cost <= source.state.bit_count() * degree * levels * bits
            assert max(LIFT.leaf_depths(source).values()) <= degree * levels * bits
        else:
            assert source.cost == source.state.bit_count() * levels * bits
            assert set(LIFT.leaf_depths(source).values()) == {levels * bits}
        for node in tree_nodes(source):
            if node.test < 0:
                continue
            remaining = [k for k in range(1, levels + 1)
                         if len({points[h][k] for h in hypotheses(node.state)}) > 1]
            assert tags[node.test][1] == min(remaining)
            if not nonlinear:
                assert tags[node.test][0] == "bit"
                assert node.left.state.bit_count() == node.right.state.bit_count()
        if nonlinear:
            for h in hypotheses(source.state):
                node = source
                row_counts = [0] * (levels + 1)
                while node.test >= 0:
                    row_counts[tags[node.test][1]] += 1
                    node = node.left if instance.tests[node.test] >> h & 1 else node.right
                assert all(count <= degree * bits for count in row_counts[1:])

    # The initial all-row-zero slice is a genuine incumbent node.  Its fresh
    # greedy code starts with an aliased context query, not a projected test.
    thin = sum(1 << h for h, point in enumerate(points) if all(value == 0 for value in point[1:]))
    assert thin in {node.state for node in tree_nodes(initial)}
    thin_code = instance.greedy(thin)
    assert tags[thin_code.test][0] == "bit"
    first = instance.tests[thin_code.test]
    assert (first & thin).bit_count() == degree
    # Find two global hypotheses with the same base context but different
    # responses to this supposedly projected source query.
    witness = None
    for value in range(base_size):
        same = [h for h, point in enumerate(points) if point[0] == value]
        hit = next((h for h in same if first >> h & 1), None)
        miss = next((h for h in same if not (first >> h & 1)), None)
        if hit is not None and miss is not None:
            witness = (hit, miss)
            break
    assert witness is not None

    selectors = tuple(index[("eq", 0, value)] for value in range(base_size))
    partials = tuple(instance.branch(instance.full, query, code,
                                     Tree(instance.full ^ code.state))
                     for query, code in zip(selectors, codes))
    for partial, core in zip(partials, cores):
        LIFT.validate_execution(instance, partial)
        assert LIFT.completed_mask(partial) == core
        assert partial.cost == instance.n + instance.greedy(core).cost
    star_bound = sum(partial.cost for partial in partials)
    row_bound = degree * levels * bits if nonlinear else levels * bits
    assert star_bound <= instance.n * (base_size + row_bound)
    if not nonlinear:
        assert star_bound == instance.n * (base_size + row_bound)
    family = {0, instance.full}
    for code in codes:
        family.update(node.state for node in tree_nodes(code))
        family.add(instance.full ^ code.state)
    incumbent_weights = LIFT.BACK.depth_weights(initial)
    profits = [sum(incumbent_weights[1 << h] for h in hypotheses(core)) - partial.cost
               for core, partial in zip(cores, partials)]
    assert sum(profits) == initial.cost - star_bound
    dp_tree, dp_profit = instance.profit_fragment(family, initial)
    assert dp_profit >= max(0, max(profits))
    LIFT.validate_execution(instance, dp_tree)

    poor = unbalanced_tree(instance)
    improved, history = star_descent(instance, codes, selectors, poor)
    LIFT.validate_execution(instance, improved)
    max_support = max(test.bit_count() for test in instance.tests)
    assert max_support == instance.n // size
    known_comparison_mean = Fraction(base_size + 1, 2) - Fraction(1, base_size) + levels * bits
    source_depths = sorted({depth for source in codes for depth in LIFT.leaf_depths(source).values()})
    source_costs = sorted({source.cost for source in codes})
    return {"bits": bits, "levels": levels, "alias_degree": degree,
            "nonlinear_incompatible_palettes": nonlinear,
            "row_size": size, "base_size": base_size,
            "n": instance.n, "m": len(instance.tests),
            "initial_greedy_cost": initial.cost,
            "initial_reverse_equality_row_work": row_work,
            "conditional_root_source_cost": codes[0].cost,
            "conditional_source_costs": source_costs,
            "conditional_source_leaf_depths": source_depths,
            "proved_conditional_path_depth_bound": row_bound,
            "thin_slice_source_first_test": tags[thin_code.test],
            "thin_slice_first_positive_contexts": degree,
            "nonprojection_same_context_witness": [points[h] for h in witness],
            "root_partial_policy_work": partials[0].cost,
            "root_partial_policy_work_values": sorted({partial.cost for partial in partials}),
            "root_star_actual_mean_certificate": str(Fraction(star_bound, instance.n)),
            "root_star_mean_bound": base_size + row_bound,
            "root_star_profit_sum_on_initial": sum(profits),
            "reduced_family_depth_prize_profit": dp_profit,
            "reduced_family_output": dp_tree.cost,
            "deliberately_poor_incumbent_cost": poor.cost,
            "star_descent_output": improved.cost,
            "star_descent_history": history,
            "explicit_context_first_average": str(known_comparison_mean),
            "rare_positive_average_lower_bound": str(Fraction(size + 1, 2)),
            "information_average_lower_bound": math.log2(instance.n),
            "strong_generator_mean_ratio_bound": (base_size + row_bound) /
                max(math.log2(instance.n), (size + 1) / 2),
            "different_local_maps": {str(a): list(value) for a, value in maps.items()},
            "local_map_is_affine": {str(a): is_affine_map(value) for a, value in maps.items()},
            "uses_exact_OPT_oracle": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("research-general-aliased-routing-results.json"))
    args = parser.parse_args()
    records = []
    for parameters in ((2, 1, 2), (2, 1, 3), (2, 2, 2), (3, 1, 2, True), (3, 2, 2, True)):
        result = check_case(*parameters)
        records.append(result)
        args.output.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
