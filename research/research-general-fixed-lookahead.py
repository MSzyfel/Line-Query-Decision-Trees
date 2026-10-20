"""Bounded analytic audits for the fixed-depth greedy-rollout obstruction.

No random search and no exact OPT oracle.  The finite prefix sample does not
replace the universal proof in research-general-fixed-lookahead.md.
"""

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
        "fixed_lookahead_lifting", Path(__file__).with_name("research-general-code-lifting.py"))
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


def make_instance(selector, k, bodies):
    sizes = (selector,) * k + tuple(bodies)
    points = tuple(product(*(range(size) for size in sizes)))
    tests, tags = [], []
    for coordinate, size in enumerate(sizes):
        for value in range(size):
            tests.append(sum(1 << h for h, point in enumerate(points) if point[coordinate] == value))
            tags.append(("eq", coordinate, value))
    for coordinate, size in enumerate(bodies, k) if k else ():
        for context in product(range(selector), repeat=k):
            for bit in range((size - 1).bit_length()):
                tests.append(sum(1 << h for h, point in enumerate(points)
                                 if point[:k] == context and point[coordinate] >> bit & 1))
                tags.append(("gate", coordinate, context, bit))
    instance = LIFT.Instance(len(points), tests)
    assert len(instance.tests) == len(tags)
    return instance, points, tuple(tags), sizes


def leaves(tree):
    return tuple(node.state for node in LIFT.tree_nodes(tree) if node.test < 0)


def deletion_audit():
    checks = 0
    for sizes in ((2, 3), (2, 2, 2)):
        instance, points, _, _ = make_instance(sizes[0], 0, sizes)
        incumbent = instance.greedy(instance.full)
        height, maximum = sum(size - 1 for size in sizes), max(sizes)

        @lru_cache(None)
        def old(state):
            return instance.prune(incumbent, state).cost

        # Every nonempty rectangular state, and every deletion subset of it.
        subsets = [tuple(mask for mask in range(1, 1 << size)) for size in sizes]
        for rectangle in product(*subsets):
            ids = [h for h, point in enumerate(points)
                   if all(rectangle[j] >> value & 1 for j, value in enumerate(point))]
            state = sum(1 << h for h in ids)
            for removed in range(1 << len(ids)):
                deleted = sum(1 << h for j, h in enumerate(ids) if removed >> j & 1)
                assert old(state) - old(state ^ deleted) <= (height + maximum - 1) * deleted.bit_count()
                checks += 1
    return checks


def audit_prefixes(selector, horizon, bodies, seeds):
    k = horizon + 1
    instance, points, tags, sizes = make_instance(selector, k, bodies)
    incumbent = instance.greedy(instance.full)
    assert all(node.test < 0 or tags[node.test][0] == "eq" for node in LIFT.tree_nodes(incumbent))
    height = sum(size - 1 for size in sizes)
    epsilon = Fraction(1, (selector - horizon) ** 2 - horizon)
    coefficient = (2 * height + selector - 1) * epsilon
    c = Fraction(2 * ((selector - 1).bit_length() + 4), min(sizes))
    resource = c * (1 + height * epsilon) + ((instance.n - 1).bit_length() + 1) * epsilon
    equalities = [j for j, tag in enumerate(tags) if tag[0] == "eq"]
    gates = [j for j, tag in enumerate(tags) if tag[0] == "gate"]

    @lru_cache(None)
    def old(state):
        return instance.prune(incumbent, state).cost

    def gain(tree, old_weight=1, coding_weight=0, work_weight=1):
        def visit(node):
            stop = old_weight * old(node.state) + coding_weight * coding(node.state.bit_count())
            if node.test < 0:
                return stop
            return min(stop, work_weight * node.state.bit_count() + visit(node.left) + visit(node.right))
        return old_weight * incumbent.cost + coding_weight * coding(instance.n) - visit(tree)

    def build(seed):
        def visit(state, depth, path):
            if state.bit_count() <= 1:
                return LIFT.Tree(state)
            if depth == horizon:
                return instance.greedy(state)
            # Deterministic adaptive prefixes covering equality/gate mixtures,
            # repeated-context negative gates, and selector-positive branches.
            choose_gate = (seed + depth + path) % 3 != 0
            pool = gates if choose_gate else equalities
            offset = (seed * 7 + depth * 11 + path * 3) % len(pool)
            query = next((pool[(offset + t) % len(pool)] for t in range(len(pool))
                          if 0 < (state & instance.tests[pool[(offset + t) % len(pool)]]).bit_count()
                          < state.bit_count()), None)
            if query is None:
                query = next(j for j, test in enumerate(instance.tests)
                             if (state & test) and state & test != state)
            hit = state & instance.tests[query]
            return instance.branch(state, query, visit(hit, depth + 1, 2 * path + 1),
                                   visit(state ^ hit, depth + 1, 2 * path + 2))
        return visit(instance.full, 0, 0)

    def accounting(tree):
        exceptional, gate_work, no_positive_outputs = 0, 0, []

        def gather(node, depth, positive):
            nonlocal exceptional, gate_work
            if node.test < 0:
                if not positive:
                    no_positive_outputs.append(node.state)
                return
            prefix_gate = depth < horizon and tags[node.test][0] == "gate"
            if prefix_gate:
                gate_work += node.state.bit_count()
                if not positive:
                    exceptional |= node.left.state
                gather(node.left, depth + 1, True)
                gather(node.right, depth + 1, positive)
            else:
                if not positive and depth >= horizon:
                    assert tags[node.test][0] == "eq"
                gather(node.left, depth + 1, positive)
                gather(node.right, depth + 1, positive)
        gather(tree, 0, False)

        def replay(node, state, depth):
            if node.test < 0:
                return LIFT.Tree(state)
            if depth < horizon and tags[node.test][0] == "gate":
                return replay(node.right, state, depth + 1)
            assert tags[node.test][0] == "eq"
            hit = state & instance.tests[node.test]
            assert hit and hit != state
            return instance.branch(state, node.test, replay(node.left, hit, depth + 1),
                                   replay(node.right, state ^ hit, depth + 1))
        replayed = replay(tree, instance.full, 0)
        outputs = leaves(replayed)
        assert sorted(state & ~exceptional for state in outputs) == sorted(no_positive_outputs)
        assert exceptional.bit_count() <= epsilon * gate_work
        assert replayed.cost <= tree.cost - gate_work + height * exceptional.bit_count()
        assert incumbent.cost - sum(old(state) for state in outputs) == replayed.cost
        for state in outputs:
            assert old(state) - old(state & ~exceptional) <= (height + selector - 1) * (state & exceptional).bit_count()
        credit = incumbent.cost - sum(old(state) for state in leaves(tree))
        assert credit <= tree.cost - gate_work + (2 * height + selector - 1) * exceptional.bit_count()
        drop = coding(instance.n) - sum(coding(state.bit_count()) for state in leaves(tree))
        assert drop <= resource * tree.cost
        return exceptional.bit_count(), gate_work

    records = []
    for seed in seeds:
        tree = build(seed)
        LIFT.validate_execution(instance, tree)
        exceptional, gate_work = accounting(tree)
        best_credit_gain = gain(tree)
        assert best_credit_gain == 0
        assert gain(tree, 0, 1, resource) == 0
        records.append({"seed": seed, "template_cost": tree.cost,
                        "all_pruning_maximum_actual_improvement": best_credit_gain,
                        "exceptional_first_positive_hypotheses": exceptional,
                        "forced_gate_work": gate_work})
    return {"M": selector, "horizon": horizon, "selectors": k, "bodies": bodies,
            "n": instance.n, "m": len(instance.tests), "incumbent_raw_cost": incumbent.cost,
            "epsilon": str(epsilon), "sufficient_credit_overhead": str(coefficient),
            "sufficient_asymptotic_condition_holds": coefficient < 1,
            "templates": records}


def growing_formula_audit():
    results = []
    for horizon in range(1, 7):
        for selector in (256, 1024, 4096, 16384):
            a, k = 2 * horizon + 2, horizon + 1
            ell = selector // (4 * a * (selector.bit_length() - 1))
            if not ell:
                continue
            bodies = [selector - a * j for j in range(1, ell + 1)]
            height = k * (selector - 1) + sum(size - 1 for size in bodies)
            epsilon = Fraction(1, (selector - horizon) ** 2 - horizon)
            assert (2 * height + selector - 1) * epsilon < 1
            minimum = bodies[-1]
            # Worst-case dominance at A=M, g=r.  Increasing A improves it.
            assert selector * (selector - horizon) ** 2 > selector ** 2 * (selector - a)
            assert (selector - horizon) ** 2 > selector * (selector - a)
            logn = k * math.log2(selector) + sum(math.log2(size) for size in bodies)
            c = Fraction(2 * ((selector - 1).bit_length() + 4), minimum)
            coding_constant = float(c * (1 + height * epsilon)) + (math.ceil(logn) + 1) * float(epsilon)
            results.append({"horizon": horizon, "M": selector, "body_count": ell,
                            "credit_overhead": float((2 * height + selector - 1) * epsilon),
                            "coding_drop_per_work_bound": coding_constant,
                            "log2_n": logn})
    return results


def main():
    result = {"deletion_checks": deletion_audit(),
              "bounded_template_checks": [audit_prefixes(8, 1, (4,), range(6)),
                                           audit_prefixes(8, 2, (2,), range(12))],
              "growing_parameter_checks": growing_formula_audit(),
              "uses_exact_OPT_oracle": False,
              "finite_templates_exhaust_all_forced_prefixes": False}
    Path(__file__).with_name("research-general-fixed-lookahead-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"deletion_checks": result["deletion_checks"],
                      "finite_template_count": sum(len(case["templates"]) for case in result["bounded_template_checks"]),
                      "growing_parameter_count": len(result["growing_parameter_checks"])}), flush=True)


if __name__ == "__main__":
    main()
