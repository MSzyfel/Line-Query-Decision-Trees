"""Deterministic coverage certificates for serial, privately coded products.

No exact optimization oracle and no random search are used.  The checker
constructs explicit source codes already in the stable polynomial generator,
certifies that a context-first comparison tree lies in its quadratic family,
and executes that tree against the original response table.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
import importlib.util
from itertools import product
import json
import math
from pathlib import Path
import sys


def load_lifting():
    spec = importlib.util.spec_from_file_location(
        "recursive_lifting_backend", Path(__file__).with_name("research-general-code-lifting.py"))
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


def make_instance(alphabets):
    alphabets = tuple(alphabets)
    assert len(alphabets) >= 2
    assert all(a % 2 == 0 and a >= 6 for a in alphabets)
    assert all(a > b for a, b in zip(alphabets, alphabets[1:]))
    points = tuple(product(*(range(a) for a in alphabets)))
    tests, tags = [], []
    for k, size in enumerate(alphabets):
        # Ascending factor priority; bit tests precede equality tests within
        # each factor. Different alphabet sizes determine global greedy order.
        if k:
            for context in product(*(range(a) for a in alphabets[:k])):
                for bit in range((size - 1).bit_length()):
                    tests.append(sum(1 << h for h, point in enumerate(points)
                                     if point[:k] == context and point[k] >> bit & 1))
                    tags.append(("bit", k, context, bit))
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[k] == value))
            tags.append(("eq", k, value))
    instance = Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    tag_index = {tag: j for j, tag in enumerate(tags)}
    fibers = []
    for k in range(len(alphabets) + 1):
        layer = {}
        for h, point in enumerate(points):
            context = point[:k]
            layer[context] = layer.get(context, 0) | 1 << h
        fibers.append(layer)
    return instance, points, tuple(tags), tag_index, fibers


def coverage_certificate(alphabets):
    instance, points, tags, tag_index, fibers = make_instance(alphabets)
    levels = len(alphabets) - 1
    initial = instance.greedy(instance.full)
    incumbent_states = {node.state for node in tree_nodes(initial)}
    for node in tree_nodes(initial):
        if node.test >= 0:
            assert tags[node.test][0] == "eq", ("initial greedy used private bit", tags[node.test])

    expected_initial = instance.n * sum(
        (Fraction(size + 1, 2) - Fraction(1, size)) for size in alphabets)
    assert initial.cost == expected_initial

    base = {0, instance.full}
    base.update(node.state for node in tree_nodes(initial))
    context_decoders = {}
    sources = []
    for k in range(1, levels + 1):
        # One actual incumbent slice suffices to expose every lower context.
        core = sum(1 << h for h, point in enumerate(points)
                   if all(value == 0 for value in point[k:]))
        assert core in incumbent_states
        source = instance.greedy(core)
        assert all(node.test < 0 or
                   (tags[node.test][0] == "eq" and tags[node.test][1] < k)
                   for node in tree_nodes(source))
        replay = LIFT.lift_partial(instance, source)
        observed = {node.state for node in tree_nodes(replay) if node.test < 0}
        assert observed == set(fibers[k].values())
        base.update(node.state for node in tree_nodes(replay))
        base.update(node.state for node in tree_nodes(source))
        context_decoders[k] = replay
        sources.append({"kind": "incumbent-slice", "level": k, "core_size": core.bit_count()})

    # Complete context fibers (singletons) are already incumbent leaves.
    assert all(state in base for layer in fibers for state in layer.values())
    prefixes = {}
    for k in range(1, levels + 1):
        for context in fibers[k]:
            query = tag_index[("bit", k, context, 0)]
            core = instance.tests[query]
            assert core and core != instance.full
            # This source is generated at the incumbent ROOT's forced child.
            source = instance.greedy(core)

            def first_block(node):
                values = {points[h][k] for h in hypotheses(node.state)}
                if len(values) == 1:
                    return Tree(node.state)
                tag = tags[node.test]
                assert tag[:3] == ("bit", k, context) and tag[3] != 0, tag
                return instance.branch(node.state, node.test,
                                       first_block(node.left), first_block(node.right))

            prefix = first_block(source)
            replay = LIFT.lift_partial(instance, source)
            prefix_replay = LIFT.lift_partial(instance, prefix)
            represented = {node.state for node in tree_nodes(replay)}
            assert all(node.state in represented for node in tree_nodes(prefix_replay))
            base.update(represented)
            base.update(node.state for node in tree_nodes(source))
            prefixes[k, context] = prefix_replay
            sources.append({"kind": "forced-gated-LSB", "level": k,
                            "context": context, "core_size": core.bit_count()})

    certificates = {state: (state, instance.full) for state in base}

    def complete(k, context):
        state = fibers[k][context]
        if k == levels + 1:
            return Tree(state)
        prefix = prefixes[k, context]
        last_query = tag_index[("bit", k, context, 0)]

        def visit(node):
            actual = state & node.state
            assert actual
            certificates[actual] = (state, node.state)
            if node.test < 0:
                values = sorted({points[h][k] for h in hypotheses(actual)})
                assert len(values) == 2 and values[1] == values[0] + 1 and values[0] % 2 == 0
                left = complete(k + 1, context + (values[1],))
                right = complete(k + 1, context + (values[0],))
                assert actual & instance.tests[last_query] == left.state
                assert actual ^ left.state == right.state
                return instance.branch(actual, last_query, left, right)
            hit = actual & instance.tests[node.test]
            assert hit and hit != actual
            return instance.branch(actual, node.test, visit(node.left), visit(node.right))
        return visit(prefix)

    first = context_decoders[1]

    def splice_first(node):
        if node.test < 0:
            values = {points[h][0] for h in hypotheses(node.state)}
            assert len(values) == 1
            return complete(1, (values.pop(),))
        return instance.branch(node.state, node.test,
                               splice_first(node.left), splice_first(node.right))

    comparison = splice_first(first)
    for node in tree_nodes(comparison):
        assert node.state in certificates
        a, b = certificates[node.state]
        assert a in base and b in base and a & b == node.state
    LIFT.validate_execution(instance, comparison)
    bound = Fraction(alphabets[0] + 1, 2) - Fraction(1, alphabets[0])
    bound += sum((size - 1).bit_length() for size in alphabets[1:])
    assert comparison.cost <= bound * instance.n

    # No quadratic family enumeration is needed: this reduced family is a
    # certified subset of the actual Q^2 and contains the comparison tree.
    family = base | {node.state for node in tree_nodes(comparison)}
    synthesized, profit = instance.profit_fragment(family, initial)
    LIFT.validate_execution(instance, synthesized)
    assert synthesized.cost <= comparison.cost <= initial.cost
    maximum_positive = max(test.bit_count() for test in instance.tests)
    assert maximum_positive == instance.n // alphabets[-1]
    return {"alphabets": list(alphabets), "n": instance.n, "m": len(instance.tests),
            "initial_greedy_raw_cost": initial.cost,
            "comparison_raw_cost": comparison.cost,
            "reduced_family_synthesis_cost": synthesized.cost,
            "average_greedy": str(Fraction(initial.cost, instance.n)),
            "average_comparison": str(Fraction(comparison.cost, instance.n)),
            "proved_average_bound": str(bound),
            "represented_base_states": len(base), "reduced_family_states": len(family),
            "required_sources": len(sources), "witnessed_context_fibers": sum(map(len, fibers)),
            "comparison_states_certified_in_quadratic_family": len({node.state for node in tree_nodes(comparison)}),
            "integer_depth_prize_profit": profit,
            "rare_positive_average_lower_bound": str(Fraction(alphabets[-1] + 1, 2)),
            "information_average_lower_bound": math.log2(instance.n),
            "uses_exact_optimization_oracle": False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("research-general-recursive-lifting-results.json"))
    args = parser.parse_args()
    records = []
    for sizes in ((8, 6), (10, 8), (10, 8, 6)):
        result = coverage_certificate(sizes)
        records.append(result)
        args.output.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
