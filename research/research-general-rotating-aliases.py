"""A bounded deterministic audit of root-minority-tied activation aliases.

This constructs a scalable greedy-bad seed, not a certified fixed point of
the full lifting/state-weaving generator. No exact OPT or random search.
"""

from fractions import Fraction
import importlib.util
from itertools import product
import json
from pathlib import Path
import sys


def load_filtered():
    spec = importlib.util.spec_from_file_location(
        "rotating_alias_filtered", Path(__file__).with_name("research-general-filtered-sources.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


FILTER = load_filtered()
LIFT = FILTER.LIFT


def multiply(x, y, bits):
    # Fixed primitive polynomials suffice for the bounded explicit checks.
    modulus = {2: 0b111, 3: 0b1011, 4: 0b10011}[bits]
    result = 0
    while y:
        if y & 1:
            result ^= x
        y >>= 1
        x <<= 1
        if x >> bits:
            x ^= modulus
    return result


def linear_form(context, slope, bits):
    coefficient, value = 1, 0
    for coordinate in context:
        value ^= multiply(coefficient, coordinate, bits)
        coefficient = multiply(coefficient, slope, bits)
    return value


def label(row, context, body, row_bits):
    # Context-dependent coordinate rotation, then complement: always bijective
    # and always maps zero to all ones. Two-bit palettes genuinely differ.
    shift = (sum(context) + body) % row_bits
    full = (1 << row_bits) - 1
    return (((row << shift) | (row >> (row_bits - shift))) & full) ^ full


def make_instance(bits, selectors, bodies):
    m, row = 1 << bits, 1 << (bits - 1)
    assert bodies < m and selectors >= 1
    points = tuple(product(*(range(m) for _ in range(selectors)),
                           *(range(row) for _ in range(bodies))))
    tests, tags = [], []
    # Body equalities win every equality/gate tie, including after rows fixed.
    for coordinate in tuple(range(selectors, selectors + bodies)) + tuple(range(selectors)):
        size = m if coordinate < selectors else row
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            tags.append(("eq", coordinate, value))
    for body in range(bodies):
        slope = body + 1
        for group in range(m // 2):
            for bit in range(bits - 1):
                test = 0
                for h, point in enumerate(points):
                    context = point[:selectors]
                    if linear_form(context, slope, bits) >> 1 == group:
                        if label(point[selectors + body], context, body, bits - 1) >> bit & 1:
                            test |= 1 << h
                tests.append(test)
                tags.append(("gate", body, group, bit))
    retained = {}
    for test, tag in zip(tests, tags):
        retained.setdefault(test, tag)
    instance = LIFT.Instance(len(points), tuple(retained))
    return instance, points, tuple(retained.values())


def check(bits, selectors, bodies, whole_menu=False):
    instance, points, tags = make_instance(bits, selectors, bodies)
    m, row = 1 << bits, 1 << (bits - 1)
    incumbent = instance.greedy(instance.full)
    minorities = [min(test.bit_count(), instance.n - test.bit_count()) for test in instance.tests]
    assert set(minorities) == {instance.n // m, 2 * instance.n // m}
    body_work = 0
    for node in LIFT.tree_nodes(incumbent):
        if node.test < 0:
            continue
        unknown = any(len({points[h][j] for h in FILTER.indices(node.state)}) > 1
                      for j in range(selectors, selectors + bodies))
        if unknown:
            assert tags[node.test][0] == "eq" and tags[node.test][1] >= selectors
            body_work += node.state.bit_count()
    body_mean = bodies * (Fraction(row + 1, 2) - Fraction(1, row))
    assert body_work == instance.n * body_mean
    thin = sum(1 << h for h, point in enumerate(points) if not any(point[selectors:]))
    assert thin in {node.state for node in LIFT.tree_nodes(incumbent)}
    source = instance.greedy(thin)
    assert tags[source.test][0] == "gate"
    assert (thin & instance.tests[source.test]).bit_count() == 2 * thin.bit_count() // m
    replay = LIFT.lift_partial(instance, source)
    candidate = LIFT.finish_partial(instance, replay, incumbent)
    LIFT.validate_execution(instance, candidate)
    high = tuple(q for q, mass in enumerate(minorities) if mass > instance.n // m)
    assert all(tags[q][0] == "eq" and tags[q][1] >= selectors for q in high)
    high_checks = 0
    for node in LIFT.tree_nodes(incumbent):
        if node.state.bit_count() <= 1:
            continue
        code = FILTER.filtered_greedy(instance, node.state, high)
        actual = LIFT.finish_partial(instance, LIFT.lift_partial(instance, code), incumbent)
        assert actual.cost == incumbent.cost
        high_checks += 1
    # Independent audit of root's information-filter repair. The high-cutoff
    # family consists exactly of body equalities; its factorization exposes
    # this body vector without the algorithm being given our labels.
    body_cells = {}
    for h, point in enumerate(points):
        word = point[selectors:]
        body_cells[word] = body_cells.get(word, 0) | (1 << h)
    independent = tuple(q for q, test in enumerate(instance.tests)
                        if all((test & cell).bit_count() * instance.n ==
                               test.bit_count() * cell.bit_count()
                               for cell in body_cells.values()))
    assert len(independent) == selectors * m
    assert all(tags[q][0] == "eq" and tags[q][1] < selectors for q in independent)
    selector_code = FILTER.filtered_greedy(instance, instance.full, independent)
    selector_fibers = {sum(1 << h for h, point in enumerate(points) if point[:selectors] == context)
                       for context in product(range(m), repeat=selectors)}
    assert {node.state for node in LIFT.tree_nodes(selector_code) if node.test < 0} == selector_fibers
    information_repair = LIFT.finish_partial(instance, selector_code, incumbent)
    LIFT.validate_execution(instance, information_repair)
    explicit_mean = selectors * (Fraction(m + 1, 2) - Fraction(1, m)) + bodies * (bits - 1)
    assert information_repair.cost <= instance.n * explicit_mean
    menu = None
    if whole_menu:
        result, menu = FILTER.source_pass(instance, incumbent)
        LIFT.validate_execution(instance, result)
    return {"M": m, "selector_count": selectors, "body_count": bodies, "body_size": row,
            "n": instance.n, "m": len(instance.tests), "initial_raw_cost": incumbent.cost,
            "initial_body_equality_work": body_work,
            "root_minority_values": sorted(set(minorities)),
            "body_zero_source_first_query": tags[source.test],
            "body_zero_completed_lift_cost": candidate.cost,
            "body_only_filtered_source_checks": high_checks,
            "every_body_only_candidate_equals_incumbent": True,
            "known_context_first_mean_upper": str(explicit_mean),
            "body_independent_original_tests": len(independent),
            "body_information_filter_exactly_selectors": True,
            "information_filtered_actual_completion_cost": information_repair.cost,
            "whole_filtered_menu": menu,
            "full_strong_generator_run": False,
            "uses_exact_OPT": False}


def main():
    results = [check(2, 2, 2, True), check(2, 3, 2, True),
               check(3, 1, 2), check(3, 1, 3), check(3, 2, 1), check(3, 2, 2)]
    Path(__file__).with_name("research-general-rotating-aliases-results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
