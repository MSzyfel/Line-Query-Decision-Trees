"""Root-minority filtered sources: a polynomial generator and bounded audit.

No subset optimum or random adversarial search is used. Default source_pass
enumerates every incumbent node and every distinct root-minority cutoff.
The bounded class audit also directly checks the useful source and joint
pair/coding resource capacities; it does not run the expensive whole menu
on the larger examples.
"""

from fractions import Fraction
from functools import lru_cache
import importlib.util
from itertools import product
import json
from math import log2
from pathlib import Path
import sys


def load_lifting():
    spec = importlib.util.spec_from_file_location(
        "filtered_source_lifting", Path(__file__).with_name("research-general-code-lifting.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LIFT = load_lifting()
Instance, Tree, tree_nodes = LIFT.Instance, LIFT.Tree, LIFT.tree_nodes


def indices(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length()-1
        mask ^= bit


def coding(size):
    if size <= 1:
        return 0
    depth = (size-1).bit_length()
    return size*(depth+1)-(1 << depth)


def filtered_greedy(instance, state, allowed):
    """Greedy using supplied indices; stop unresolved if the filter cannot split."""
    @lru_cache(None)
    def build(selected):
        options = []
        if selected.bit_count() > 1:
            for q in allowed:
                hit = selected & instance.tests[q]
                if hit and hit != selected:
                    options.append((max(hit.bit_count(), (selected ^ hit).bit_count()), q))
        if not options:
            return Tree(selected)
        _, q = min(options)
        hit = selected & instance.tests[q]
        return instance.branch(selected, q, build(hit), build(selected ^ hit))
    return build(state)


def source_pass(instance, incumbent, thresholds=None, source_states=None):
    """Polynomial full menu; retain the best actual completed lifted tree.

    Filters use GLOBAL root minorities, even for a conditional source state.
    All source states are frozen before any lifting. Partial sources are legal:
    their nonsingleton terminals are filled after actual global replay.
    """
    assert incumbent.state == instance.full
    minorities = [min(test.bit_count(), instance.n-test.bit_count())
                  for test in instance.tests]
    thresholds = sorted(set(minorities)) if thresholds is None else tuple(thresholds)
    states = ({node.state for node in tree_nodes(incumbent) if node.state.bit_count() > 1}
              if source_states is None else set(source_states))
    best, count = incumbent, 0
    for cutoff in thresholds:
        allowed = tuple(q for q, mass in enumerate(minorities) if mass >= cutoff)
        for state in sorted(states):
            code = filtered_greedy(instance, state, allowed)
            replay = LIFT.lift_partial(instance, code)
            candidate = LIFT.finish_partial(instance, replay, incumbent)
            if candidate.cost < best.cost:
                best = candidate
            count += 1
    return best, {"frozen_source_states": len(states), "thresholds": len(thresholds),
                  "source_candidates": count, "incumbent_cost": incumbent.cost,
                  "result_cost": best.cost}


def row_labels(size, origin_number, alias_position):
    # Deterministic distinct local bijections. For eight or more labels these
    # need not be affine; the row-bound proof does not assume affine structure.
    remainder = list(range(size-1))
    shift = (origin_number+3*alias_position) % (size-1)
    remainder = remainder[shift:]+remainder[:shift]
    if (origin_number+alias_position) % 2:
        remainder.reverse()
    return (size-1, *remainder)


def make_instance(m, selectors, bodies, degree):
    assert selectors >= 2 and 1 <= degree < m**(selectors-1)
    assert all(2 <= size < m for size in bodies)
    contexts = tuple(product(range(m), repeat=selectors))
    points = tuple(product(*(range(m) for _ in range(selectors)),
                           *(range(size) for size in bodies)))
    tests, tags = [], []
    for coordinate, size in enumerate((m,)*selectors+tuple(bodies)):
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            tags.append(("eq", coordinate, value))
    active = {}
    labels = {}
    for origin_number, origin in enumerate(contexts):
        activation = tuple((*origin[:-1], (origin[-1]+a) % m) for a in range(degree))
        active[origin] = frozenset(activation)
        for j, size in enumerate(bodies):
            for a, context in enumerate(activation):
                labels[j, origin, context] = row_labels(size, origin_number+j, a)
    # Bit-major interleaving deliberately does not assume consecutive palettes.
    for j, size in enumerate(bodies):
        for bit in range((size-1).bit_length()):
            for origin in contexts:
                test = 0
                for h, point in enumerate(points):
                    context = point[:selectors]
                    if context in active[origin] and labels[j, origin, context][point[selectors+j]] >> bit & 1:
                        test |= 1 << h
                tests.append(test)
                tags.append(("gate", j, origin, bit))
    # Preserve one actual supplied description if harmless duplicates occur.
    retained = {}
    for test, tag in zip(tests, tags):
        retained.setdefault(test, tag)
    instance = Instance(len(points), tuple(retained))
    fibers = {context: sum(1 << h for h, point in enumerate(points)
                           if point[:selectors] == context) for context in contexts}
    return instance, points, tuple(retained.values()), fibers, active


def joint_capacity_audit(instance, points, tags, fibers, active, m, selectors, degree, quality):
    """Exact per-(hypothesis,query) resource loads, not a subset relaxation."""
    denominator = degree+quality-1
    pair_weight, coding_weight = Fraction(1, denominator), Fraction(quality, denominator)
    lookup = {point: h for h, point in enumerate(points)}
    edges = []
    for h, point in enumerate(points):
        for coordinate in range(selectors):
            for value in range(point[coordinate]+1, m):
                changed = (*point[:coordinate], value, *point[coordinate+1:])
                edges.append((h, lookup[changed]))
    max_load, capacity_checks = Fraction(0), 0
    for test, tag in zip(instance.tests, tags):
        loads = [Fraction(0) for _ in points]
        for left, right in edges:
            if bool(test >> left & 1) == bool(test >> right & 1):
                continue
            if tag[0] == "eq":
                assert tag[1] < selectors
                endpoint = right if test >> left & 1 else left
            else:
                activation = active[tag[2]]
                left_active = points[left][:selectors] in activation
                right_active = points[right][:selectors] in activation
                assert left_active or right_active
                endpoint = right if left_active and not right_active else left
                # If both are active, either endpoint is allowed.
            loads[endpoint] += pair_weight
        for fiber in fibers.values():
            if fiber & test and fiber & ~test:
                for h in indices(fiber):
                    loads[h] += coding_weight
        assert max(loads) <= 1
        max_load = max(max_load, max(loads))
        capacity_checks += len(loads)
    fiber_size = next(iter(fibers.values())).bit_count()
    objective = pair_weight*len(edges)+coding_weight*len(fibers)*coding(fiber_size)
    target = instance.n*(Fraction(selectors*(m-1), 2)+
                         quality*Fraction(coding(fiber_size), fiber_size))/denominator
    assert objective == target
    return objective, {"pair_edges": len(edges), "per_hypothesis_query_capacities": capacity_checks,
                       "maximum_exact_load": str(max_load), "joint_lower_raw": str(objective)}


def check_case(m, selectors, bodies, degree, whole_menu=False):
    instance, points, tags, fibers, active = make_instance(m, selectors, bodies, degree)
    incumbent = instance.greedy(instance.full)
    thin = sum(1 << h for h, point in enumerate(points) if not any(point[selectors:]))
    assert thin in {node.state for node in tree_nodes(incumbent)}
    cutoff = instance.n//m
    allowed = tuple(q for q, test in enumerate(instance.tests)
                    if min(test.bit_count(), instance.n-test.bit_count()) >= cutoff)
    assert all(tags[q][0] == "eq" for q in allowed)
    assert len(allowed) == selectors*m+sum(bodies)
    source = filtered_greedy(instance, thin, allowed)
    assert all(node.state.bit_count() == 1 for node in tree_nodes(source) if node.test < 0)
    replay = LIFT.lift_partial(instance, source)
    replay_leaves = {node.state for node in tree_nodes(replay) if node.test < 0}
    assert replay_leaves == set(fibers.values())
    equality_mean = Fraction(m+1, 2)-Fraction(1, m)
    assert replay.cost == instance.n*selectors*equality_mean
    b = sum((size-1).bit_length() for size in bodies)
    quality = degree  # Each context belongs to exactly degree palettes per body.
    fiber_executions = 0
    max_fiber_depth = 0
    for fiber in fibers.values():
        code = instance.greedy(fiber)
        for h in indices(fiber):
            node, per_row = code, [0]*len(bodies)
            while node.test >= 0:
                tag = tags[node.test]
                coordinate = tag[1]-selectors if tag[0] == "eq" else tag[1]
                assert coordinate >= 0
                per_row[coordinate] += 1
                node = node.left if instance.tests[node.test] >> h & 1 else node.right
            assert node.state == 1 << h
            assert all(count <= quality*(size-1).bit_length()
                       for count, size in zip(per_row, bodies))
            max_fiber_depth = max(max_fiber_depth, sum(per_row))
            fiber_executions += 1
    candidate = LIFT.finish_partial(instance, replay, incumbent)
    LIFT.validate_execution(instance, candidate)
    upper = instance.n*(selectors*equality_mean+quality*b)
    assert candidate.cost <= upper
    lower, ledger = joint_capacity_audit(instance, points, tags, fibers, active,
                                         m, selectors, degree, quality)
    assert lower <= candidate.cost
    thin_unfiltered = instance.greedy(thin)
    projection_failure = any(tags[node.test][0] == "gate"
                             for node in tree_nodes(thin_unfiltered) if node.test >= 0)
    menu = None
    if whole_menu:
        result, menu = source_pass(instance, incumbent)
        LIFT.validate_execution(instance, result)
        assert result.cost <= candidate.cost
    return {"M": m, "selector_coordinates": selectors, "body_sizes": bodies,
            "D": degree, "P": quality, "n": instance.n, "m": len(instance.tests),
            "incumbent_raw": incumbent.cost, "filtered_lift_raw": candidate.cost,
            "proved_upper_raw": str(upper), "proved_approximation_ratio": str(upper/lower),
            "actual_ratio_to_joint_lower": str(Fraction(candidate.cost, lower)),
            "fiber_hypothesis_executions": fiber_executions,
            "max_fiber_depth": max_fiber_depth, "P_B": quality*b,
            "unfiltered_slice_uses_nonprojection_gate": projection_failure,
            "joint_resource": ledger, "whole_polynomial_menu": menu}


def main():
    cases = [check_case(4, 2, (2,), 2, True),
             check_case(6, 2, (4,), 2),
             check_case(8, 2, (6,), 2),
             check_case(4, 3, (2,), 2),
             check_case(6, 2, (4, 4), 2),
             check_case(10, 2, (8,), 2),
             check_case(8, 2, (6, 6), 2)]
    output = {"status": "passed", "cases": cases,
              "no_exact_OPT_or_subset_oracle": True,
              "whole_menu_run_only_on_smallest_case": True,
              "no_unrestricted_approximation_claim": True}
    path = Path(__file__).with_name("research-general-filtered-sources-results.json")
    path.write_text(json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
