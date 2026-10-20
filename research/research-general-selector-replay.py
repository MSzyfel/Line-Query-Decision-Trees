"""Direct completed-selector-replay certificates, without another harvest.

Bounded explicit verification; no exact optimal-subproblem oracle, no random
search, and no full quadratic state-family generation.
"""

from fractions import Fraction
import importlib.util
from itertools import product
import math
from pathlib import Path
import random
import sys


def load_lifting():
    spec = importlib.util.spec_from_file_location(
        "selector_replay_lifting",
        Path(__file__).with_name("research-general-code-lifting.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LIFT = load_lifting()


def coding(size):
    if size <= 1:
        return 0
    depth = (size - 1).bit_length()
    return size * (depth + 1) - (1 << depth)


def equality_mean(size):
    return Fraction(size + 1, 2) - Fraction(1, size)


def hypotheses(state):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def make_instance(selectors, bodies, permuted=False):
    selectors, bodies = tuple(selectors), tuple(bodies)
    assert selectors and bodies and min(selectors) > max(bodies) >= 2
    sizes = selectors + bodies
    selector_count = len(selectors)
    points = tuple(product(*(range(size) for size in sizes)))
    point_index = {point: h for h, point in enumerate(points)}
    fibers = {}
    for h, point in enumerate(points):
        context = point[:selector_count]
        fibers[context] = fibers.get(context, 0) | 1 << h
    tests, tags = [], []
    # The source-projection proof only requires pure equalities to win ties
    # against private selector-context point tests.
    for coordinate, size in enumerate(sizes):
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points)
                             if point[coordinate] == value))
            tags.append(("eq", coordinate, value))
    palette = []
    for context_index, context in enumerate(fibers):
        for body, size in enumerate(bodies):
            width = (size - 1).bit_length()
            labels = list(range(1 << width))
            if permuted:
                random.Random(83071 + 1009 * context_index + body).shuffle(labels)
            labels = labels[:size]
            assert len(set(labels)) == size
            for bit in range(width):
                test = sum(1 << h for h, point in enumerate(points)
                           if point[:selector_count] == context
                           and labels[point[selector_count + body]] >> bit & 1)
                palette.append((test, ("gate", body, context, bit)))
    # Deliberately interleave contexts and body palettes. The path bound does
    # not depend on favorable palette blocks or bit ordering.
    if permuted:
        random.Random(1957).shuffle(palette)
    for test, tag in palette:
        tests.append(test)
        tags.append(tag)
    instance = LIFT.Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    selector_edges = []
    for h, point in enumerate(points):
        for coordinate, size in enumerate(selectors):
            for value in range(point[coordinate] + 1, size):
                changed = list(point)
                changed[coordinate] = value
                selector_edges.append((h, point_index[tuple(changed)]))
    return instance, points, tuple(tags), fibers, tuple(selector_edges)


def audit_case(selectors, bodies, permuted=False, all_subsets=False):
    instance, points, tags, fibers, edges = make_instance(selectors, bodies, permuted)
    k, n = len(selectors), instance.n
    body_volume = math.prod(bodies)
    width = sum((size - 1).bit_length() for size in bodies)
    incumbent = instance.greedy(instance.full)
    incumbent_states = {node.state for node in LIFT.tree_nodes(incumbent)}
    assert all(node.test < 0 or tags[node.test][0] == "eq"
               for node in LIFT.tree_nodes(incumbent))
    expected_incumbent = n * sum(equality_mean(size) for size in selectors + bodies)
    assert incumbent.cost == expected_incumbent
    core = sum(1 << h for h, point in enumerate(points) if not any(point[k:]))
    assert core in incumbent_states and core.bit_count() == math.prod(selectors)
    source = instance.greedy(core)
    assert all(node.test < 0 or tags[node.test][0] == "eq" and tags[node.test][1] < k
               for node in LIFT.tree_nodes(source))
    replay = LIFT.lift_partial(instance, source)
    replay_leaves = {node.state for node in LIFT.tree_nodes(replay) if node.test < 0}
    assert replay_leaves == set(fibers.values())
    assert replay.cost == body_volume * source.cost

    maximum_body_path = owner_bit_checks = 0
    for context, state in fibers.items():
        fresh = instance.greedy(state)
        for h in hypotheses(state):
            node = fresh
            queries = [0] * len(bodies)
            owner_bits = [set() for _ in bodies]
            singleton_started = [False] * len(bodies)
            while node.test >= 0:
                tag = tags[node.test]
                if tag[0] == "gate":
                    _, body, actual_context, bit = tag
                    assert actual_context == context
                    owner_bits[body].add(bit)
                else:
                    _, coordinate, _ = tag
                    assert coordinate >= k
                    body = coordinate - k
                    if not singleton_started[body]:
                        surviving_values = {points[g][coordinate] for g in hypotheses(node.state)}
                        assert len(surviving_values) - 1 <= (bodies[body] - 1).bit_length() - len(owner_bits[body])
                        singleton_started[body] = True
                        owner_bit_checks += 1
                queries[body] += 1
                node = node.left if instance.tests[node.test] >> h & 1 else node.right
            assert all(count <= (size - 1).bit_length() for count, size in zip(queries, bodies))
            maximum_body_path = max(maximum_body_path, sum(queries))
        assert fresh.cost <= state.bit_count() * width

    completed = LIFT.finish_partial(instance, replay, incumbent)
    LIFT.validate_execution(instance, completed)
    assert all(node.state.bit_count() == 1 for node in LIFT.tree_nodes(completed) if node.test < 0)
    upper_mean = sum(equality_mean(size) for size in selectors) + width
    assert completed.cost <= n * upper_mean
    # Its nodes are already first-pass base states of one finished lifted
    # source. No extra harvest and no pairwise-intersection closure is needed.
    family = incumbent_states | {node.state for node in LIFT.tree_nodes(completed)} | {0}
    output, profit = instance.profit_fragment(family, incumbent)
    LIFT.validate_execution(instance, output)
    assert output.cost <= completed.cost

    pair_lower = Fraction(n, 2) * sum(size - 1 for size in selectors)
    assert len(edges) == pair_lower
    lower = pair_lower + len(fibers) * coding(body_volume)
    assert lower <= output.cost
    endpoint_checks = 0
    for query, test in enumerate(instance.tests):
        tag = tags[query]
        load = [0] * n
        for a, b in edges:
            if bool(test >> a & 1) != bool(test >> b & 1):
                outside = b if test >> a & 1 else a
                load[outside] += 1
        if tag[0] == "gate":
            # Integer coding is charged only inside this context; every
            # cut-pair charge was assigned outside that context.
            for h in hypotheses(fibers[tag[2]]):
                load[h] += 1
        elif tag[1] >= k:
            assert not any(load)
            load = [1] * n
        assert max(load, default=0) <= 1
        endpoint_checks += n

    subset_checks = 0
    if all_subsets:
        def phi(state):
            return (sum(bool(state >> a & 1) and bool(state >> b & 1) for a, b in edges)
                    + sum(coding((state & fiber).bit_count()) for fiber in fibers.values()))
        for state in range(1 << n):
            value = phi(state)
            for test in instance.tests:
                assert value - phi(state & test) - phi(state & ~test) <= state.bit_count()
                subset_checks += 1
    return {"selectors": selectors, "bodies": bodies, "permuted_labels": permuted,
            "n": n, "m": len(instance.tests), "source_size": core.bit_count(),
            "selector_fibers": len(fibers), "initial_raw": incumbent.cost,
            "completed_single_lift_raw": completed.cost, "supported_output_raw": output.cost,
            "joint_pair_coding_lower": str(lower), "certified_output_ratio": str(Fraction(output.cost, lower)),
            "body_path_bound": width, "maximum_body_path": maximum_body_path,
            "first_singleton_path_checks": owner_bit_checks,
            "endpoint_load_checks": endpoint_checks, "all_subset_query_checks": subset_checks,
            "extra_harvest_layers": 0, "quadratic_closure_used": False}


def main():
    cases = [((3,), (2,), False, True), ((4,), (3,), True, True),
             ((6, 6), (4,), False, False), ((6, 6), (4, 2), True, False),
             ((4, 4, 4), (2,), True, False), ((5, 5, 5), (3, 2), True, False),
             ((3, 3, 3, 3, 3), (2,), True, False)]
    for case in cases:
        print("PASS completed replay and joint resource:", audit_case(*case), flush=True)
    rows = []
    for base in (16, 32, 64, 128, 256, 512):
        levels = math.floor(base / (4 * math.log2(base)))
        bodies = tuple(base - 2 * j for j in range(1, levels + 1))
        volume = math.prod(bodies)
        for selector_count in (2, 4, (base - 1).bit_length()):
            upper = selector_count * equality_mean(base) + sum((size - 1).bit_length() for size in bodies)
            lower = Fraction(selector_count * (base - 1), 2) + Fraction(coding(volume), volume)
            assert upper / lower <= 1 + max(Fraction(2, base), 1 / math.log2(min(bodies)))
            rows.append((base, selector_count, levels, float(upper / lower)))
    print("PASS growing-parameter algebra only (M,k,bodycount,upper/lower):", rows)


if __name__ == "__main__":
    main()
