"""Deterministic XOR alias camouflage and whole-component partition repair.

No random search, exact OPT, or full quadratic-state generator is used.
The prime response-factor check uses the existing exact polynomial routine.
"""

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


ROTATE = load("xor_alias_rotate", "research-general-rotating-aliases.py")
FILTER, LIFT = ROTATE.FILTER, ROTATE.LIFT
PRODUCT = load("xor_alias_products", "research-general-product-decomposition.py")


def make_instance(bits, selectors, bodies):
    m, row = 1 << bits, 1 << (bits - 1)
    assert selectors >= 2 and 1 <= bodies < m
    points = tuple(product(*(range(m) for _ in range(selectors)),
                           *(range(row) for _ in range(bodies))))
    tests, tags = [], []
    for coordinate in range(selectors, selectors + bodies):
        for value in range(row):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            tags.append(("bodyeq", coordinate, value))
    for body in range(bodies):
        slope = body + 1
        for group in range(m // 2):
            for bit in range(bits - 1):
                test = 0
                for h, point in enumerate(points):
                    context = point[:selectors]
                    active = ROTATE.linear_form(context, slope, bits) >> 1 == group
                    label = point[selectors + body] ^ (context[0] >> 1)
                    if active and label >> bit & 1:
                        test |= 1 << h
                tests.append(test)
                tags.append(("gate", body, group, bit))
    # Fixed-body gates tie selector equalities and receive priority.
    for coordinate in range(selectors):
        for value in range(m):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            tags.append(("selectoreq", coordinate, value))
    instance = LIFT.Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    return instance, points, tuple(tags)


def partition_components(instance, size):
    queries = tuple(q for q, test in enumerate(instance.tests) if test.bit_count() == size)
    neighbors = {q: set() for q in queries}
    for i, q in enumerate(queries):
        for other in queries[i + 1:]:
            if not instance.tests[q] & instance.tests[other]:
                neighbors[q].add(other)
                neighbors[other].add(q)
    unseen, accepted, components = set(queries), [], []
    while unseen:
        pending, component = [min(unseen)], set()
        while pending:
            q = pending.pop()
            if q in component:
                continue
            component.add(q)
            unseen.discard(q)
            pending.extend(neighbors[q] - component)
        union = 0
        disjoint = True
        for q in sorted(component):
            disjoint &= not bool(union & instance.tests[q])
            union |= instance.tests[q]
        good = disjoint and union == instance.full
        components.append({"queries": sorted(component), "pairwise_disjoint": disjoint,
                           "union_size": union.bit_count(), "accepted": good})
        if good:
            accepted.extend(component)
    return tuple(sorted(accepted)), components


def audit(bits, selectors, bodies, prime_check=False):
    instance, points, tags = make_instance(bits, selectors, bodies)
    m, row = 1 << bits, 1 << (bits - 1)
    incumbent = instance.greedy(instance.full)
    body_work = 0
    for node in LIFT.tree_nodes(incumbent):
        if node.test < 0:
            continue
        unknown = any(len({points[h][j] for h in FILTER.indices(node.state)}) > 1
                      for j in range(selectors, selectors + bodies))
        if unknown:
            assert tags[node.test][0] == "bodyeq"
            body_work += node.state.bit_count()
    assert body_work == instance.n * bodies * ((row + 1) / 2 - 1 / row)
    cells = {}
    for h, point in enumerate(points):
        word = point[selectors:]
        cells[word] = cells.get(word, 0) | (1 << h)
    independent = tuple(q for q, test in enumerate(instance.tests)
                        if all((test & cell).bit_count() * instance.n ==
                               test.bit_count() * cell.bit_count()
                               for cell in cells.values()))
    assert set(independent) == {q for q, tag in enumerate(tags) if tag[0] != "bodyeq"}
    words = tuple(sum(1 << index for index, q in enumerate(independent)
                      if instance.tests[q] >> h & 1) for h in range(instance.n))
    assert len(set(words)) == instance.n
    factors = None
    if prime_check:
        cut = PRODUCT.EntropyCuts(words, len(independent))
        factor_masks, factor_sizes = cut.factorize()
        assert len(factor_masks) == 1 and factor_sizes == (instance.n,)
        factors = {"factor_sizes": factor_sizes, "entropy_oracle_calls": cut.calls}
    thin = sum(1 << h for h, point in enumerate(points) if not any(point[selectors:]))
    assert thin in {node.state for node in LIFT.tree_nodes(incumbent)}
    code = instance.greedy(thin)
    assert tags[code.test][0] == "gate"
    source_lift = LIFT.finish_partial(instance, LIFT.lift_partial(instance, code), incumbent)
    LIFT.validate_execution(instance, source_lift)
    accepted, components = partition_components(instance, instance.n // m)
    assert set(accepted) == {q for q, tag in enumerate(tags) if tag[0] == "selectoreq"}
    assert len([component for component in components if component["accepted"]]) == selectors
    for component in components:
        kinds = {tags[q][0] for q in component["queries"]}
        assert len(kinds) == 1
        if not component["accepted"]:
            assert kinds == {"gate"}
    partial = FILTER.filtered_greedy(instance, instance.full, accepted)
    repair = LIFT.finish_partial(instance, partial, incumbent)
    LIFT.validate_execution(instance, repair)
    upper_mean = selectors * ((m + 1) / 2 - 1 / m) + bodies * (bits - 1)
    assert repair.cost <= instance.n * upper_mean
    return {"M": m, "selectors": selectors, "bodies": bodies, "body_size": row,
            "n": instance.n, "m": len(instance.tests), "initial_raw": incumbent.cost,
            "initial_equality_body_work": body_work,
            "each_gate_independent_of_joint_body_vector": True,
            "kept_response_words_distinct": len(set(words)),
            "prime_factorization_check": factors,
            "thin_source_first_query": tags[code.test],
            "thin_source_completed_lift_raw": source_lift.cost,
            "disjointness_components": components,
            "accepted_component_queries": len(accepted),
            "accepted_component_code_raw": repair.cost,
            "selector_first_mean_bound": upper_mean,
            "full_strong_generator_run": False, "uses_exact_OPT": False}


def main():
    results = [audit(2, 2, 2, True), audit(2, 3, 2, True), audit(3, 2, 2)]
    Path(__file__).with_name("research-general-xor-aliases-results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps([{key: value for key, value in result.items()
                       if key != "disjointness_components"} for result in results], indent=2), flush=True)


if __name__ == "__main__":
    main()
