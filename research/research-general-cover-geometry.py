"""Direct deterministic compilation of an explicit fractional policy cover.

Public API: compile_cover(instance, policies, weights) -> (tree, statistics).
Input policies are actual possibly-partial original-test trees on full H.
All coefficients are exact nonnegative Fractions and cover every hypothesis.
No LP solver or exact decision-tree optimization is used by the compiler.
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


BACK = load("cover_geometry_backend", "research-general-algorithm-next.py")


def indices(state):
    while state:
        bit = state & -state
        yield bit.bit_length() - 1
        state ^= bit


def restrict_policy(instance, policy, state):
    """Actual restriction, including unresolved terminals and new singletons."""
    assert state and state & policy.state == state
    if state.bit_count() <= 1 or policy.test < 0:
        return BACK.Tree(state)
    hit = state & instance.tests[policy.test]
    if not hit:
        return restrict_policy(instance, policy.right, state)
    miss = state ^ hit
    if not miss:
        return restrict_policy(instance, policy.left, state)
    return instance.branch(state, policy.test,
                           restrict_policy(instance, policy.left, hit),
                           restrict_policy(instance, policy.right, miss))


def policy_profile(instance, policy):
    """Validate all actual paths; return per-h depths and completed mask."""
    assert policy.state == instance.full
    depths, completed = [], 0
    for h in range(instance.n):
        node, depth = policy, 0
        while node.test >= 0:
            assert node.state >> h & 1
            hit = node.state & instance.tests[node.test]
            assert hit and hit != node.state
            assert node.left.state == hit and node.right.state == node.state ^ hit
            node = node.left if hit >> h & 1 else node.right
            depth += 1
        assert node.state >> h & 1
        depths.append(depth)
        if node.state.bit_count() == 1:
            completed |= 1 << h
    assert sum(depths) == policy.cost
    return tuple(depths), completed


def compile_cover(instance, policies, weights):
    """Compile any explicit nonnegative fractional completion cover directly.

    The resulting complete tree costs at most sum_i weights[i]*policies[i].cost.
    Uses <=n productive policy applications; no rounding/approximation loss.
    """
    policies, weights = tuple(policies), tuple(Fraction(value) for value in weights)
    assert len(policies) == len(weights) and policies
    assert all(weight >= 0 for weight in weights)
    profiles = tuple(policy_profile(instance, policy) for policy in policies)
    completions = tuple(completed for _, completed in profiles)
    cover = tuple(sum(weight for weight, completed in zip(weights, completions) if completed >> h & 1)
                  for h in range(instance.n))
    assert all(value >= 1 for value in cover), "input columns do not cover every hypothesis"
    prizes = tuple(sum(weight * depths[h] for weight, (depths, _) in zip(weights, profiles))
                   for h in range(instance.n))
    benchmark = sum(weight * policy.cost for weight, policy in zip(weights, policies))
    assert sum(prizes) == benchmark
    history = []

    def potential(state):
        return sum(prizes[h] for h in indices(state))

    def build(state):
        if state.bit_count() == 1:
            return BACK.Tree(state)
        candidates = []
        weighted_difference = Fraction(0)
        for i, (policy, weight, completed) in enumerate(zip(policies, weights, completions)):
            if not weight:
                continue
            restricted = restrict_policy(instance, policy, state)
            old_completed = state & completed
            difference = restricted.cost - potential(old_completed)
            weighted_difference += weight * difference
            if old_completed:
                candidates.append((difference, i, restricted))
        assert weighted_difference <= 0
        difference, chosen, restricted = min(candidates, key=lambda item: (item[0], item[1]))
        assert difference <= 0
        history.append({"state_size": state.bit_count(), "policy": chosen,
                        "restricted_work": restricted.cost,
                        "credited_original_completions": (state & completions[chosen]).bit_count(),
                        "difference": str(difference)})
        assert len(history) <= instance.n

        def fill(node):
            if node.test < 0:
                return BACK.Tree(node.state) if node.state.bit_count() == 1 else build(node.state)
            return instance.branch(node.state, node.test, fill(node.left), fill(node.right))

        tree = fill(restricted)
        assert tree.cost <= potential(state)
        return tree

    tree = build(instance.full)
    actual_depths, actual_completed = policy_profile(instance, tree)
    assert actual_completed == instance.full
    assert tree.cost <= benchmark
    return tree, {"columns": len(policies), "cover_min": str(min(cover)),
                  "cover_max": str(max(cover)), "fractional_work_benchmark": str(benchmark),
                  "compiled_raw_cost": tree.cost, "productive_applications": len(history),
                  "history": history, "uses_LP_or_exact_OPT_solver": False}


def cycle_fixture():
    n, full = 5, (1 << 5) - 1
    edges = tuple((1 << i) | (1 << ((i + 1) % n)) for i in range(n))
    tests = (*edges, *(1 << i for i in range(n)))
    instance = BACK.Instance(n, tests)
    policies = []
    for i, edge in enumerate(edges):
        a, b = 1 << i, 1 << ((i + 1) % n)
        positive = instance.branch(edge, n + i, BACK.Tree(a), BACK.Tree(b))
        policies.append(instance.branch(full, i, positive, BACK.Tree(full ^ edge)))
    tree, stats = compile_cover(instance, policies, [Fraction(1, 2)] * n)
    assert tree.cost == 12
    return {"fixture": "five_cycle_pair_completion", **stats,
            "minimum_integral_column_cover_cost": 21,
            "binary_coding_lower_bound": 12}


def multi_exit_fixture(overcover=False):
    n = 8
    tests = tuple(sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(3))
    instance = BACK.Instance(n, tests)
    policies = []
    for shift in range(n):
        state = instance.full
        desired0, desired1 = 1 ^ (shift & 1), 1 ^ (shift >> 1 & 1)
        branch0 = state & tests[0] if desired0 else state & ~tests[0]
        branch1 = branch0 & tests[1] if desired1 else branch0 & ~tests[1]
        last = instance.branch(branch1, 2, BACK.Tree(branch1 & tests[2]), BACK.Tree(branch1 & ~tests[2]))
        second = instance.branch(branch0, 1,
                                 last if desired1 else BACK.Tree(branch0 & tests[1]),
                                 BACK.Tree(branch0 & ~tests[1]) if desired1 else last)
        policy = instance.branch(state, 0,
                                 second if desired0 else BACK.Tree(state & tests[0]),
                                 BACK.Tree(state & ~tests[0]) if desired0 else second)
        policies.append(policy)
    weights = [Fraction(1, 2)] * n
    if overcover:
        weights[0] = Fraction(3, 2)
    _, stats = compile_cover(instance, policies, weights)
    return {"fixture": "cube_multi_unfinished_exits", "nonexact_overcover": overcover, **stats}


def paired_bridge_fixture(bits, selectors, bodies):
    """Audit the ENTIRE newest affine-support query-selector portfolio."""
    xor = load("cover_geometry_xor", "research-general-xor-aliases.py")
    linear = load("cover_geometry_linear", "research-general-linear-selectors.py")
    raw, points, tags = xor.make_instance(bits, selectors, bodies)
    alphabet = 1 << bits
    first_selector = next(q for q, tag in enumerate(tags) if tag[0] == "selectoreq")
    new_tests, new_tags, pairs = [], [], []
    for coordinate in range(selectors):
        active = sum(1 << h for h, point in enumerate(points) if point[coordinate] in (0, 1))
        positive = sum(1 << h for h, point in enumerate(points)
                       if point[coordinate] in (0, 1) and
                       ((point[selectors] ^ point[(coordinate + 1) % selectors]) & 1))
        pairs.append((positive, active ^ positive))
        new_tests.extend(pairs[-1])
        new_tags.extend((("paired_bridge", coordinate, 1), ("paired_bridge", coordinate, 0)))
    tests = (*raw.tests[:first_selector], *new_tests, *raw.tests[first_selector:])
    tagged = (*tags[:first_selector], *new_tags, *tags[first_selector:])
    instance = linear.CONTEXT.BACK.Instance(raw.n, tests)
    assert len(instance.tests) == len(tagged)
    partitions, diagnostics = linear.linear_partition_components(instance, audit=True)
    b = instance.n // alphabet
    at_b = next(item for item in diagnostics if item["cell_size"] == b)
    supported = set(at_b["supported_queries"])
    for coordinate, pair in enumerate(pairs):
        cells = list(pair) + [test for test, tag in zip(instance.tests, tagged)
                              if tag[0] == "selectoreq" and tag[1] == coordinate and tag[2] not in (0, 1)]
        assert len(cells) == alphabet and not any(a & c for i, a in enumerate(cells) for c in cells[i + 1:])
        assert sum(cells) == instance.full
    assert all(q in supported for q, tag in enumerate(tagged) if tag[0] == "paired_bridge")
    factors = linear.CONTEXT.ResponseFactors(instance, tuple(sorted(supported)))
    candidate, _, factor_stats = linear.CONTEXT.plan_factors(instance, factors)
    tree, _, stats = linear.linear_selected_context_pass(instance)
    linear.CONTEXT.execute(instance, tree)
    assert tree.cost <= candidate.cost <= instance.greedy(instance.full).cost
    return {"M": alphabet, "selectors": selectors, "bodies": bodies,
            "n": instance.n, "m": len(instance.tests),
            "paired_bridge_columns_real_cover_supported": 2 * selectors,
            "affine_supported_B_queries": len(supported),
            "accepted_B_whole_components": sum(p["cell_size"] == b for p in partitions),
            "supported_family_factor_alphabets": factors.alphabets,
            "supported_family_quotient_size": factors.quotient_size,
            "supported_family_residuals_nonuniform": factors.nonuniform_residual_sizes,
            "supported_family_plan_cost": candidate.cost,
            "supported_family_plan_contexts": factor_stats["contexts"],
            "full_extended_portfolio": stats,
            "is_claimed_strong_generator_fixed_point": False,
            "uses_exact_OPT": False}


def main():
    results = [cycle_fixture(), multi_exit_fixture(), multi_exit_fixture(True)]
    output = {"compiler_checks": results, "paired_bridge_checks": []}
    path = Path(__file__).with_name("research-general-cover-geometry-results.json")
    path.write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps({"compiler_checks": results}), flush=True)
    for parameters in ((2, 2, 2), (3, 2, 1)):
        result = paired_bridge_fixture(*parameters)
        output["paired_bridge_checks"].append(result)
        path.write_text(json.dumps(output, indent=2), encoding="utf-8")
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
