"""Bounded full-portfolio audit of balanced bridges on XOR activation aliases.

Uses the ACTUAL generic query-selector + factor-planner + depth-prize-pool
implementation. No exact OPT, random search, or stronger global lifting.
"""

from fractions import Fraction
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


XOR = load("bridge_alias_xor", "research-general-xor-aliases.py")
SELECT = load("bridge_alias_select", "research-general-query-selectors.py")


def make_instance(bits, selectors, bodies):
    raw, points, tags = XOR.make_instance(bits, selectors, bodies)
    m = 1 << bits
    contexts = tuple(product(range(m), repeat=selectors))
    needed = 2 * m ** (selectors - 1)
    if m >= 2 ** (selectors + 1):
        first = range(m // 2, m // 2 + 2 ** selectors)
        others = (range(m // 2, m),) * (selectors - 1)
        support = tuple(product(first, *others))
        assert len(support) == needed
        masks = {context: context[0] & 1 for context in support}
        half_rectangle = True
    else:
        # Smaller explicit validator: still avoids zero in every selector,
        # while the asymptotic family uses the half-alphabet construction.
        support = tuple(context for context in contexts if all(context))[:needed]
        assert len(support) == needed
        masks = {context: i & 1 for i, context in enumerate(support)}
        half_rectangle = False
    assert sum(masks.values()) * 2 == needed
    assert all(all(value for value in context) for context in support)
    bridge = sum(1 << h for h, point in enumerate(points)
                 if point[:selectors] in masks and
                 ((point[selectors] & 1) ^ masks[point[:selectors]]))
    # Gate priority remains ahead of selector equalities; insert the bridge
    # immediately before the pure selector section.
    first_selector = next(i for i, tag in enumerate(tags) if tag[0] == "selectoreq")
    tests = (*raw.tests[:first_selector], bridge, *raw.tests[first_selector:])
    tagged = (*tags[:first_selector], ("bridge", 0), *tags[first_selector:])
    instance = SELECT.CONTEXT.BACK.Instance(raw.n, tests)
    assert len(instance.tests) == len(tagged)
    assert bridge.bit_count() == instance.n // m
    return instance, points, tagged, support, half_rectangle


def classify_pool(instance, points, selectors, incumbent, pool):
    body_words = {point[selectors:] for point in points}
    context_nodes = {node.state for node in SELECT.CONTEXT.BACK.tree_nodes(incumbent)
                     if node.state and len({points[h][selectors:]
                                           for h in XOR.FILTER.indices(node.state)}) == 1}
    rectangles = 0
    known_body = 0
    for state in pool:
        if not state:
            continue
        words = {points[h][selectors:] for h in XOR.FILTER.indices(state)}
        if len(words) == 1 and state in context_nodes:
            known_body += 1
            continue
        per_body = [set() for _ in next(iter(body_words))]
        for word in words:
            for j, value in enumerate(word):
                per_body[j].add(value)
        expected = {h for h, point in enumerate(points)
                    if all(point[selectors + j] in values for j, values in enumerate(per_body))}
        assert state == sum(1 << h for h in expected)
        assert words == set(product(*per_body))
        rectangles += 1
    return {"body_rectangles_with_full_selectors": rectangles,
            "original_known_body_selector_nodes": known_body,
            "other_nonempty_states": 0}


def audit(bits, selectors, bodies):
    instance, points, tags, support, half_rectangle = make_instance(bits, selectors, bodies)
    m, row = 1 << bits, 1 << (bits - 1)
    incumbent = instance.greedy(instance.full)
    joint_body_cells = {}
    for h, point in enumerate(points):
        word = point[selectors:]
        joint_body_cells[word] = joint_body_cells.get(word, 0) | (1 << h)
    for q, test in enumerate(instance.tests):
        independent = all(instance.n * (test & cell).bit_count() ==
                          cell.bit_count() * test.bit_count() for cell in joint_body_cells.values())
        assert independent == (tags[q][0] != "bodyeq")
    body_work = 0
    for node in SELECT.CONTEXT.BACK.tree_nodes(incumbent):
        if node.test < 0:
            continue
        if len({points[h][selectors:] for h in XOR.FILTER.indices(node.state)}) > 1:
            assert tags[node.test][0] == "bodyeq"
            body_work += node.state.bit_count()
    assert body_work == instance.n * bodies * (Fraction(row + 1, 2) - Fraction(1, row))
    partitions = SELECT.partition_components(instance)
    assert len(partitions) == bodies
    assert all(all(tags[q][0] == "bodyeq" for q in partition["queries"]) for partition in partitions)
    families, cache, _ = SELECT.select_families(instance)
    original = tuple(range(len(instance.tests)))
    family_records = []
    for retained in families:
        factors = cache.get(retained) or SELECT.CONTEXT.ResponseFactors(instance, retained)
        if not retained:
            classification = "empty"
            assert not factors.alphabets
        elif all(tags[q][0] == "bodyeq" for q in retained):
            classification = "body_axes"
            assert factors.quotient_size == row ** len(factors.alphabets)
        else:
            classification = "prime_identifying"
            assert factors.alphabets == (instance.n,)
        tree, _, stats = SELECT.CONTEXT.plan_factors(instance, factors)
        assert tree.cost == incumbent.cost
        family_records.append({"retained_queries": len(retained), "classification": classification,
                               "factor_alphabets": factors.alphabets,
                               "planned_raw_cost": tree.cost, "contexts": stats["contexts"]})
    output, pool, stats = SELECT.selected_context_pass(instance, independence=True, recombine=True)
    SELECT.CONTEXT.execute(instance, output)
    assert output.cost == incumbent.cost
    structural = classify_pool(instance, points, selectors, incumbent, pool)
    return {"M": m, "selectors": selectors, "bodies": bodies, "body_size": row,
            "n": instance.n, "m": len(instance.tests), "bridge_context_support": len(support),
            "half_alphabet_bridge": half_rectangle,
            "initial_cost": incumbent.cost, "initial_body_equality_work": body_work,
            "accepted_partitions_are_exactly_body_axes": True,
            "all_nonbody_queries_independent_joint_body_vector": True,
            "actual_selected_families": family_records,
            "full_generic_portfolio": stats, "pool_structure": structural,
            "is_fixed_point_of_this_generic_portfolio": True,
            "full_stronger_lifting_generator_run": False, "uses_exact_OPT": False}


def main():
    results = []
    for parameters in ((2, 2, 2), (3, 2, 1), (3, 2, 2)):
        result = audit(*parameters)
        results.append(result)
        Path(__file__).with_name("research-general-bridge-aliases-results.json").write_text(
            json.dumps(results, indent=2), encoding="utf-8")
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
