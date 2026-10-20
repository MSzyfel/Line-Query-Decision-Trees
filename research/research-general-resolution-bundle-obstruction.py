"""Bounded proof audits for the two-selector greedy-bundle obstruction.

Only small explicit instances are built. Large growing-family checks use
integer alphabet/cost formulas, not response matrices or adversarial search.
"""

from fractions import Fraction
from functools import lru_cache
import importlib.util
from itertools import product
import math
from pathlib import Path
import sys


def load_lifting():
    spec = importlib.util.spec_from_file_location(
        "bundle_obstruction_lifting",
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


def equality_raw(size):
    return 0 if size <= 1 else size * (size + 1) // 2 - 1


def equality_depth(size, value):
    return min(value + 1, size - 1)


def hypothesis_ids(state):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def make_instance(selector, bodies):
    sizes = (selector, selector) + tuple(bodies)
    points = tuple(product(*(range(size) for size in sizes)))
    tests, tags = [], []
    for coordinate, size in enumerate(sizes):
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points)
                             if point[coordinate] == value))
            tags.append(("eq", coordinate, value))
    for body, size in enumerate(bodies, 2):
        for context in product(range(selector), repeat=2):
            for bit in range((size - 1).bit_length()):
                tests.append(sum(1 << h for h, point in enumerate(points)
                                 if point[:2] == context and point[body] >> bit & 1))
                tags.append(("gate", body, context, bit))
    instance = LIFT.Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    return instance, points, tuple(tags), sizes


def audit_instance(selector, bodies):
    instance, points, tags, sizes = make_instance(selector, bodies)
    incumbent = instance.greedy(instance.full)
    assert all(node.test < 0 or tags[node.test][0] == "eq"
               for node in LIFT.tree_nodes(incumbent))
    expected_mean = sum(equality_mean(size) for size in sizes)
    assert incumbent.cost == instance.n * expected_mean
    original_nodes = {id(node): node for node in LIFT.tree_nodes(incumbent)}

    @lru_cache(None)
    def restricted(node_id, state):
        if state.bit_count() <= 1:
            return 0
        node = original_nodes[node_id]
        if state == node.state:
            return node.cost
        hit = state & instance.tests[node.test]
        miss = state ^ hit
        if not hit:
            return restricted(id(node.right), state)
        if not miss:
            return restricted(id(node.left), state)
        return (state.bit_count() + restricted(id(node.left), hit)
                + restricted(id(node.right), miss))

    def old(state):
        return restricted(id(incumbent), state)

    def leaves(tree):
        return tuple(node.state for node in LIFT.tree_nodes(tree) if node.test < 0)

    def credit(tree):
        return incumbent.cost - sum(old(state) for state in leaves(tree))

    def resource(tree):
        return coding(instance.n) - sum(coding(state.bit_count()) for state in leaves(tree))

    def maximum_prefix_gain(tree, gamma, coding_price, work_price=1):
        """Exact all-pruning energy Bellman calculation for one template."""
        def visit(node):
            terminal = gamma * old(node.state) + coding_price * coding(node.state.bit_count())
            if node.test < 0:
                return terminal
            continued = (work_price * node.state.bit_count()
                         + visit(node.left) + visit(node.right))
            return min(terminal, continued)
        energy = gamma * incumbent.cost + coding_price * coding(instance.n)
        return energy - visit(tree)

    n, m = instance.n, selector
    cap = Fraction(1, 2 * m * m)
    depth_bound = sum(size - 1 for size in sizes)
    eta = Fraction(depth_bound, 2 * m * m)
    kappa = Fraction((n - 1).bit_length() + 1, 2 * m * m)
    equality_constant = Fraction(2 * ((m - 1).bit_length() + 4), min(sizes))
    resource_constant = equality_constant * (1 + eta) + kappa
    body_mean = sum(equality_mean(size) for size in bodies)
    template_count = commutations = gate_formulas = 0
    both_response_templates = 0
    positive_mixed_small_case = 0

    def cut(tree, depth):
        if depth == 0 or tree.test < 0:
            return LIFT.Tree(tree.state)
        return instance.branch(tree.state, tree.test,
                               cut(tree.left, depth - 1), cut(tree.right, depth - 1))

    for query, test in enumerate(instance.tests):
        hit, miss = test, instance.full ^ test
        query_credit = incumbent.cost - old(hit) - old(miss)
        if tags[query][0] == "gate":
            _, coordinate, context, bit = tags[query]
            size = sizes[coordinate]
            selected_values = [value for value in range(size) if value >> bit & 1]
            selector_deletion = m + equality_depth(m, context[0])
            expected_gate = Fraction(math.prod(bodies), size) * (
                len(selected_values) * selector_deletion
                + sum(equality_depth(size, value) for value in selected_values)
                - equality_raw(len(selected_values)))
            assert query_credit == expected_gate
            assert hit.bit_count() <= cap * n
            assert query_credit <= Fraction(3 * n, 2 * m)
            assert old(hit) <= hit.bit_count() * body_mean
            gate_formulas += 1
        else:
            assert query_credit == n

        for chosen_positive, core in ((True, hit), (False, miss)):
            source = instance.greedy(core)
            equality_source = tags[query][0] == "eq" or not chosen_positive
            if equality_source:
                assert all(node.test < 0 or tags[node.test][0] == "eq"
                           for node in LIFT.tree_nodes(source))
            if tags[query][0] == "gate" and not chosen_positive:
                for node in LIFT.tree_nodes(source):
                    if node.test < 0:
                        continue
                    body_unknown = any(len({points[h][coordinate]
                                            for h in hypothesis_ids(node.state)}) > 1
                                       for coordinate in range(2, len(sizes)))
                    assert not body_unknown or tags[node.test][1] >= 2
            if chosen_positive:
                template = instance.branch(instance.full, query, source, LIFT.Tree(miss))
            else:
                template = instance.branch(instance.full, query, LIFT.Tree(hit), source)
            assert maximum_prefix_gain(template, Fraction(1), Fraction(0)) == 0
            assert maximum_prefix_gain(template, Fraction(0), Fraction(1), resource_constant) == 0
            small_case_gain = maximum_prefix_gain(template, Fraction(1, 2), Fraction(1))
            positive_mixed_small_case += small_case_gain > 0
            template_count += 1

            if tags[query][0] != "gate" or chosen_positive:
                continue
            for depth in (0, 1, 3):
                partial = cut(source, depth)
                replay = LIFT.lift_partial(instance, partial)
                R_leaves = leaves(replay)
                gamma_R = credit(replay)
                gamma_A = old(hit) - sum(old(state & hit) for state in R_leaves)
                gamma_query_at_leaves = sum(old(state) - old(state & hit) - old(state & miss)
                                            for state in R_leaves)
                actual = instance.branch(instance.full, query, LIFT.Tree(hit), partial)
                assert gamma_R == replay.cost
                assert gamma_A >= 0
                assert credit(actual) == gamma_R + gamma_query_at_leaves - gamma_A
                assert gamma_query_at_leaves <= Fraction(4 * n, m)
                extra_work = replay.cost - partial.cost
                assert 0 <= extra_work <= hit.bit_count() * depth_bound
                assert resource(replay) <= equality_constant * replay.cost
                assert resource(actual) <= resource(replay) + hit.bit_count() * ((n - 1).bit_length() + 1)
                assert credit(actual) <= actual.cost
                commutations += 1

        both_template = instance.branch(instance.full, query,
                                        instance.greedy(hit), instance.greedy(miss))
        assert maximum_prefix_gain(both_template, Fraction(1), Fraction(0)) == 0
        both_resource_constant = equality_constant * (1 + eta) + 2 * kappa
        assert maximum_prefix_gain(both_template, Fraction(0), Fraction(1),
                                   both_resource_constant) == 0
        both_response_templates += 1

    return {"selector": selector, "bodies": tuple(bodies), "n": n,
            "m": len(instance.tests), "raw_incumbent": incumbent.cost,
            "all_pruning_templates": template_count, "gate_formula_checks": gate_formulas,
            "both_response_templates": both_response_templates,
            "commutation_checks": commutations,
            "small_case_profitable_half_credit_plus_coding": positive_mixed_small_case}


def main():
    for selector, bodies in ((6, (4,)), (6, (4, 2)), (8, (6,))):
        print("PASS bounded exact all-prefix audit:", audit_instance(selector, bodies), flush=True)
    rows = []
    for selector in (16, 32, 64, 128, 256, 512, 1024):
        levels = math.floor(selector / (4 * math.log2(selector)))
        bodies = tuple(selector - 2 * j for j in range(1, levels + 1))
        n = selector * selector * math.prod(bodies)
        depth_bound = 2 * (selector - 1) + sum(size - 1 for size in bodies)
        eta = Fraction(depth_bound, 2 * selector * selector)
        kappa = Fraction((n - 1).bit_length() + 1, 2 * selector * selector)
        c = Fraction(2 * ((selector - 1).bit_length() + 4), min(bodies))
        C = c * (1 + eta) + kappa
        assert eta + Fraction(4, selector) < 1
        body_mean = sum(equality_mean(size) for size in bodies)
        assert Fraction(3, 2 * selector) + body_mean / (2 * selector * selector) < 1
        comparison = 2 * equality_mean(selector) + sum((size - 1).bit_length() for size in bodies)
        greedy = 2 * equality_mean(selector) + body_mean
        if selector >= 64:
            assert C < Fraction(1, 2)
        rows.append({"M": selector, "levels": levels, "n_bitlength": n.bit_length(),
                     "C_M": float(C), "required_a_over_1_minus_gamma": float(1 / C),
                     "greedy_over_feasible_comparison": float(greedy / comparison)})
    print("PASS analytic growing family (no large matrix constructed):", rows)


if __name__ == "__main__":
    main()
