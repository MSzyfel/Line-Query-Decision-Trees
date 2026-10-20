"""Compile any feasible compact template-prefix LP point without cost loss.

The compiler is polynomial. This file does not implement an LP optimizer;
the theorem may use any standard polynomial rational LP algorithm. Bounded
checks supply exact feasible points and use no unrestricted optimum oracle.
"""

from fractions import Fraction
from functools import lru_cache
from pathlib import Path
import importlib.util
import json
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


COVER = load("template_cover_geometry", "research-general-cover-geometry.py")
BACK = COVER.BACK


def bits(state):
    while state:
        bit = state & -state
        yield bit
        state ^= bit


def profit_prefix(instance, template, state, prizes):
    """Best restricted-template stopping policy; ties maximize completions."""
    if state.bit_count() <= 1:
        return BACK.Tree(state), (sum(prizes[bit] for bit in bits(state)), state.bit_count())
    assert template.test >= 0
    hit = state & instance.tests[template.test]
    miss = state ^ hit
    if not hit:
        return profit_prefix(instance, template.right, state, prizes)
    if not miss:
        return profit_prefix(instance, template.left, state, prizes)
    left, left_score = profit_prefix(instance, template.left, hit, prizes)
    right, right_score = profit_prefix(instance, template.right, miss, prizes)
    score = (left_score[0]+right_score[0]-state.bit_count(), left_score[1]+right_score[1])
    if score >= (0, 0):
        return instance.branch(state, template.test, left, right), score
    return BACK.Tree(state), (Fraction(0), 0)


def layer_decomposition(instance, templates, levels):
    """Exact layer cake: return explicit partial policies and their weights."""
    policies, weights = [], []
    for template, values in zip(templates, levels):
        previous = Fraction(0)
        for threshold in sorted({Fraction(values.get(node.state, 0))
                                 for node in BACK.tree_nodes(template)} - {Fraction(0)}):
            def prefix(node):
                if node.test < 0 or values.get(node.state, 0) < threshold:
                    return BACK.Tree(node.state)
                return instance.branch(node.state, node.test, prefix(node.left), prefix(node.right))
            policies.append(prefix(template))
            weights.append(threshold-previous)
            previous = threshold
    return policies, weights


def compile_template_point(instance, templates, levels):
    """Return original-test Tree, statistics, from a feasible rational z point."""
    assert len(templates) == len(levels) and templates
    coverage = {bit: Fraction(0) for bit in bits(instance.full)}
    prizes = {bit: Fraction(0) for bit in bits(instance.full)}
    objective = Fraction(0)
    for template, values in zip(templates, levels):
        assert template.state == instance.full
        COVER.policy_profile(instance, template)
        for node in BACK.tree_nodes(template):
            value = Fraction(values.get(node.state, 0))
            assert 0 <= value <= 1
            if node.test < 0:
                assert node.state.bit_count() == 1
                coverage[node.state] += value
                continue
            assert Fraction(values.get(node.left.state, 0)) <= value
            assert Fraction(values.get(node.right.state, 0)) <= value
            objective += node.state.bit_count()*value
            for bit in bits(node.state):
                prizes[bit] += value
    assert all(value >= 1 for value in coverage.values())
    assert sum(prizes.values()) == objective
    stages = []

    @lru_cache(None)
    def build(state):
        if state.bit_count() <= 1:
            return BACK.Tree(state)
        candidates = [profit_prefix(instance, tree, state, prizes) for tree in templates]
        partial, score = max(candidates, key=lambda item: item[1])
        assert score[0] >= 0 and score[1] > 0
        stages.append({"population": state.bit_count(), "work": partial.cost,
                       "completed": score[1], "profit": str(score[0])})

        def finish(node):
            if node.test < 0:
                return build(node.state)
            return instance.branch(node.state, node.test, finish(node.left), finish(node.right))
        result = finish(partial)
        assert result.cost <= sum(prizes[bit] for bit in bits(state))
        return result

    tree = build(instance.full)
    assert tree.cost <= objective and len(stages) <= instance.n
    _, complete = COVER.policy_profile(instance, tree)
    assert complete == instance.full
    return tree, {"LP_point_objective": str(objective), "actual_cost": tree.cost,
                  "templates": len(templates), "productive_applications": len(stages),
                  "stage_trace": stages, "uses_an_LP_optimizer": False}


def random_template(instance, rng):
    def build(state):
        if state.bit_count() <= 1:
            return BACK.Tree(state)
        choices = [q for q, test in enumerate(instance.tests) if (state & test) not in (0, state)]
        q = rng.choice(choices)
        hit = state & instance.tests[q]
        return instance.branch(state, q, build(hit), build(state ^ hit))
    return build(instance.full)


def main():
    rng = random.Random(2026101917)
    checked = decomposed_columns = 0
    for n in range(2, 11):
        for _ in range(4):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(6)]
            tests += [1 << h for h in range(n)]
            instance = BACK.Instance(n, tests)
            templates = [random_template(instance, rng) for _ in range(3)]
            levels = []
            # Start from a convex full-template mixture, then independently
            # increase some internal-node levels. Leaves still cover exactly1.
            for j, template in enumerate(templates):
                base = (Fraction(1, 2), Fraction(1, 3), Fraction(1, 6))[j]
                def values(node, parent):
                    value = base if node.test < 0 else rng.choice((base, parent))
                    result = {node.state: value}
                    if node.test >= 0:
                        result.update(values(node.left, value))
                        result.update(values(node.right, value))
                    return result
                levels.append(values(template, Fraction(1)))
            tree, stats = compile_template_point(instance, templates, levels)
            policies, weights = layer_decomposition(instance, templates, levels)
            raw = sum(weight*policy.cost for weight, policy in zip(weights, policies))
            assert raw == Fraction(stats["LP_point_objective"])
            coverage = [Fraction(0)]*n
            for weight, policy in zip(weights, policies):
                _, complete = COVER.policy_profile(instance, policy)
                for h in range(n):
                    if complete >> h & 1:
                        coverage[h] += weight
            assert min(coverage) >= 1
            other, _ = COVER.compile_cover(instance, policies, weights)
            assert other.cost <= raw
            checked += 1
            decomposed_columns += len(policies)

    # Two templates each deliberately waste work in one different quarter.
    # A compact feasible LP point retains just their easy branches. The
    # compiler can switch to the other template on the remaining quarter.
    n = 256
    full = (1 << n)-1
    tests = [sum(1 << h for h in range(n) if (h // (n//4)) != quarter) for quarter in (0, 1)]
    tests += [sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(8)]
    tests += [1 << h for h in range(n)]
    instance = BACK.Instance(n, tests)
    templates, levels = [], []
    for quarter in (0, 1):
        root_query = quarter
        easy = instance.tests[root_query]
        hard = full ^ easy
        def chain(state):
            if state.bit_count() <= 1:
                return BACK.Tree(state)
            bit = next(bits(state))
            q = instance.tests.index(bit)
            return instance.branch(state, q, BACK.Tree(bit), chain(state ^ bit))
        template = instance.branch(full, root_query, instance.greedy(easy), chain(hard))
        value = {node.state: Fraction(1) for node in BACK.tree_nodes(template)
                 if node.state == full or node.state & easy}
        templates.append(template)
        levels.append(value)
    tree, example = compile_template_point(instance, templates, levels)
    example["complete_template_costs"] = [template.cost for template in templates]
    assert tree.cost < min(template.cost for template in templates)
    example["LP_optimizer_not_run"] = True
    output = {"status": "passed", "feasible_compact_points": checked,
              "layer_decomposed_partial_columns": decomposed_columns,
              "cross_template_example": example, "no_unrestricted_optimum_oracle": True,
              "no_unrestricted_approximation_claim": True}
    Path(__file__).with_name("research-general-template-cover-lp-results.json").write_text(
        json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
