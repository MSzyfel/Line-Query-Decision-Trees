"""Exact sparse dual certificate for affine natural-hierarchy profile gap.

No LP optimization is used. Coefficient identities cover all free profile
variables and same-hierarchy weighted restriction features simultaneously.
"""
from collections import defaultdict
from dataclasses import dataclass
from itertools import product
import json
from pathlib import Path
import random


@dataclass
class Node:
    state: int
    coordinate: int = -1
    positive: "Node | None" = None
    negative: "Node | None" = None


def coding_cost(size):
    if size <= 1:
        return 0
    depth = (size-1).bit_length()
    return size*(depth+1) - (1 << depth)


def singleton_cost(size):
    return size*(size+1)//2-1


def natural_hierarchy(q, dimension, points):
    def build(state, coordinate, remaining):
        if coordinate == dimension:
            assert state.bit_count() == 1
            return Node(state)
        if len(remaining) == 1:
            return build(state, coordinate+1, tuple(range(q)))
        value = remaining[0]
        positive = sum(1 << h for h, point in enumerate(points)
                       if state & (1 << h) and point[coordinate] == value)
        assert positive and positive != state
        return Node(state, coordinate,
                    build(positive, coordinate+1, tuple(range(q))),
                    build(state ^ positive, coordinate, remaining[1:]))
    return build((1 << len(points))-1, 0, tuple(range(q)))


def internal_nodes(root):
    result, pending = [], [root]
    while pending:
        node = pending.pop()
        if node.coordinate >= 0:
            result.append(node)
            pending.extend((node.positive, node.negative))
    return result


def feature_vector(nodes, selected):
    result = {}
    for j, node in enumerate(nodes):
        count = (selected & node.state).bit_count()
        if count >= 2:
            result[("profile", j, count)] = 1
        if selected & node.positive.state and selected & node.negative.state:
            result[("restriction", j)] = count
    return result


def add_capacity(coefficients, nodes, selected, test, weight):
    for sign, cell in [(1, selected), (-1, selected & test), (-1, selected & ~test)]:
        for variable, value in feature_vector(nodes, cell).items():
            coefficients[variable] += weight * sign * value


def dual_certificate(q, dimension, points, nodes):
    prefix_points = list(product(range(q), repeat=dimension-1))
    point_index = {point: h for h, point in enumerate(points)}
    last_zero = sum(1 << h for h, point in enumerate(points) if point[-1] == 0)
    capacities = []
    # Actual root equality search of the last coordinate.
    remaining = (1 << len(points))-1
    for value in range(q-1):
        test = sum(1 << h for h, point in enumerate(points) if point[-1] == value)
        capacities.append((remaining, test, 1))
        remaining &= ~test
    # Artificial quotient splits, each simulated on a legal graph subset.
    def quotient_code(labels):
        if len(labels) <= 1:
            return 0
        middle = len(labels)//2
        left, right = labels[:middle], labels[middle:]
        selected = (sum(1 << point_index[prefix_points[j] + (0,)] for j in left)
                    | sum(1 << point_index[prefix_points[j] + (1,)] for j in right))
        capacities.append((selected, last_zero, q))
        return len(labels) + quotient_code(left) + quotient_code(right)
    quotient_work = quotient_code(list(range(len(prefix_points))))
    assert quotient_work == coding_cost(len(prefix_points))
    accumulated = defaultdict(int)
    rhs = 0
    for selected, test, weight in capacities:
        assert selected & test and selected & ~test
        add_capacity(accumulated, nodes, selected, test, weight)
        rhs += weight * selected.bit_count()
    accumulated = {variable: value for variable, value in accumulated.items() if value}
    objective = feature_vector(nodes, (1 << len(points))-1)
    assert accumulated == objective
    n, count = len(points), len(prefix_points)
    assert rhs == count*singleton_cost(q) + q*coding_cost(count)
    assert len(capacities) == count + q - 2
    return len(capacities), rhs, len(objective)


def graph_checks(q, dimension, points, nodes, rng):
    prefixes = list(product(range(q), repeat=dimension-1))
    index = {point: h for h, point in enumerate(points)}
    count, checked = len(prefixes), 0
    # Exhaust all partial graph functions only on very small quotients.
    if count <= 4:
        functions = product(range(-1, q), repeat=count)
    else:
        functions = [[rng.randrange(-1, q) for _ in range(count)] for _ in range(120)]
    for values in functions:
        selected = baseline = 0
        for prefix, value in zip(prefixes, values):
            if value >= 0:
                selected |= 1 << index[prefix + (value,)]
                baseline |= 1 << index[prefix + (0,)]
        assert feature_vector(nodes, selected) == feature_vector(nodes, baseline)
        checked += 1
    return checked


def main():
    rng = random.Random(20261019)
    results, total_graphs, total_variables = [], 0, 0
    cases = [(2, 1), (2, 2), (2, 3), (2, 4),
             (3, 1), (3, 2), (3, 3), (3, 4),
             (4, 2), (4, 3), (5, 1), (5, 2), (5, 3)]
    for q, dimension in cases:
        points = list(product(range(q), repeat=dimension))
        root = natural_hierarchy(q, dimension, points)
        nodes = internal_nodes(root)
        assert len(nodes) == len(points)-1
        capacities, bound, _ = dual_certificate(q, dimension, points, nodes)
        checked = graph_checks(q, dimension, points, nodes, rng)
        variables = sum(node.state.bit_count()-1 for node in nodes) + len(nodes)
        total_variables += variables
        total_graphs += checked
        results.append({"q": q, "dimension": dimension, "n": len(points),
                        "profile_and_restriction_variables": variables,
                        "nonzero_dual_capacities": capacities,
                        "exact_root_upper_bound": bound,
                        "coordinate_only_exact_OPT": dimension * (len(points)//q) * singleton_cost(q),
                        "graph_invariance_checks": checked})
    output = {"status": "passed", "no_numerical_LP_or_exponential_algorithm": True,
              "exact_dual_identities": len(cases),
              "all_variable_coefficients_checked": total_variables,
              "graph_invariance_checks": total_graphs, "cases": results}
    Path(__file__).with_name("research-general-affine-profiles-results.json").write_text(
        json.dumps(output, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
