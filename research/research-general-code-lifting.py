"""Global replay of conditional identifying codes, without context activation.

This is a separate experimental generator.  The synthesis routine uses only
fixed-exponent polynomial operations.  Exponential subset optimization is
called solely by the explicit small-instance validation command.
"""

from __future__ import annotations

import argparse
from fractions import Fraction
from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import random
import sys


def load_backend():
    path = Path(__file__).with_name("research-general-adversarial-pricing.py")
    spec = importlib.util.spec_from_file_location("lifting_backend", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BACK = load_backend()
Instance, Tree, tree_nodes = BACK.Instance, BACK.Tree, BACK.tree_nodes


def bits(state):
    while state:
        bit = state & -state
        yield bit
        state ^= bit


def leaf_depths(tree):
    result = {}
    stack = [(tree, 0)]
    while stack:
        node, depth = stack.pop()
        if node.test < 0:
            for bit in bits(node.state):
                result[bit] = depth
        else:
            stack.extend(((node.left, depth + 1), (node.right, depth + 1)))
    return result


def completed_mask(tree):
    return sum(node.state for node in tree_nodes(tree)
               if node.test < 0 and node.state.bit_count() == 1)


def lift_partial(instance, code, ambient=None, dirty_stop_depth=None):
    """Replay code's supplied queries on a containing ambient state.

    Each binary core branch is nonempty, so both global branches remain
    executable.  At an original singleton leaf, stop even if outsiders remain.
    With dirty_stop_depth=t, also stop every contaminated node at depth t;
    clean nodes continue through the actual remaining conditional code.
    """
    ambient = instance.full if ambient is None else ambient
    core = code.state
    assert core and core & ambient == core
    outside = ambient ^ core

    def visit(node, state, depth):
        assert node.state & state == node.state
        if node.test < 0 or (dirty_stop_depth is not None
                            and depth >= dirty_stop_depth and state & outside):
            return Tree(state)
        hit = state & instance.tests[node.test]
        miss = state ^ hit
        assert hit and miss
        return instance.branch(state, node.test,
                               visit(node.left, hit, depth + 1),
                               visit(node.right, miss, depth + 1))

    return visit(code, ambient, 0)


def finish_partial(instance, partial, incumbent):
    """Use the cheaper of actual incumbent restriction and fresh greedy at exits."""
    if partial.test < 0:
        if partial.state.bit_count() <= 1:
            return partial
        old = instance.prune(incumbent, partial.state)
        fresh = instance.greedy(partial.state)
        return min((old, fresh), key=lambda tree: tree.cost)
    return instance.branch(partial.state, partial.test,
                           finish_partial(instance, partial.left, incumbent),
                           finish_partial(instance, partial.right, incumbent))


def lift_statistics(instance, code, ambient=None, weights=None):
    ambient = instance.full if ambient is None else ambient
    partial = lift_partial(instance, code, ambient)
    core, outside = code.state, ambient ^ code.state
    depths = leaf_depths(partial)
    complete = completed_mask(partial)
    core_depths = leaf_depths(code)
    height = max(core_depths.values(), default=0)
    occupied = sum(1 for leaf in tree_nodes(partial)
                   if leaf.test < 0 and leaf.state & outside)
    stats = {"core_size": core.bit_count(), "outside_size": outside.bit_count(),
             "core_work": code.cost, "core_height": height,
             "partial_work": partial.cost,
             "outside_path_work": sum(depths[h] for h in bits(outside)),
             "contaminated_core_leaves": occupied,
             "completed_core": (complete & core).bit_count(),
             "completed_outside": (complete & outside).bit_count()}
    assert partial.cost == code.cost + stats["outside_path_work"]
    assert occupied <= min(outside.bit_count(), core.bit_count())
    assert stats["completed_core"] == core.bit_count() - occupied
    assert stats["partial_work"] <= code.cost + outside.bit_count() * height
    if weights is not None:
        prizes = sorted((weights[h] for h in bits(core)), reverse=True)
        lost_bound = sum(prizes[:min(len(prizes), outside.bit_count())])
        total = sum(prizes)
        reward = sum(weights[h] for h in bits(complete))
        stats.update({"core_prize": total, "completed_prize": reward,
                      "prize_lower_bound": total - lost_bound})
        assert reward >= total - lost_bound
    return partial, stats


def template_density(instance, template):
    """Exact minimum work/completion ratio among every pruning of one template.

    A nonsingleton terminal of the supplied partial template is unresolved.
    Dynamic programming uses at most n+1 entries per node.  Across a binary
    template with at most n leaves all child-profile convolutions cost O(n^2).
    """
    profiles, choices = {}, {}

    def profile(node):
        if node.test < 0:
            out = {0: 0}
            if node.state.bit_count() == 1:
                out[1] = 0
            profiles[id(node)] = out
            return out
        left, right = profile(node.left), profile(node.right)
        out, action = {0: 0}, {}
        size = node.state.bit_count()
        for a, ca in left.items():
            for b, cb in right.items():
                k, work = a + b, size + ca + cb
                if k and (k not in out or work < out[k]):
                    out[k], action[k] = work, (a, b)
        profiles[id(node)], choices[id(node)] = out, action
        return out

    root = profile(template)
    if not any(root):
        return None, None, {"work": 0, "completed": 0}
    count = min((k for k in root if k),
                key=lambda k: (Fraction(root[k], k), -k))

    def rebuild(node, k):
        if not k or node.test < 0:
            return Tree(node.state)
        a, b = choices[id(node)][k]
        return instance.branch(node.state, node.test,
                               rebuild(node.left, a), rebuild(node.right, b))

    partial = rebuild(template, count)
    actual = completed_mask(partial).bit_count()
    assert partial.cost == root[count] and actual == count
    return partial, Fraction(partial.cost, count), {
        "work": partial.cost, "completed": count,
        "density": float(Fraction(partial.cost, count)),
        "density_fraction": str(Fraction(partial.cost, count))}


def code_key(code):
    return tuple((node.state, node.test) for node in tree_nodes(code))


def source_codes(instance, incumbent, weighted=False, all_subcodes=True):
    """Freeze conditional sources before lifting; never harvest new lifted codes."""
    generators = [instance.greedy]
    if weighted:
        weights = BACK.depth_weights(incumbent)
        variants = [weights, {h: w * w for h, w in weights.items()}]
        variants += [{h: 1 + instance.n * (w >= cutoff)
                      for h, w in weights.items()}
                     for cutoff in sorted(set(weights.values()))]
        generators += [BACK.prize_greedy(instance, w) for w in variants]
    sources = {}

    def add(code):
        for source in tree_nodes(code) if all_subcodes else (code,):
            if source.state.bit_count() > 1:
                sources.setdefault(code_key(source), source)

    for node in tree_nodes(incumbent):
        if node.test < 0:
            continue
        for generator in generators:
            add(generator(node.state))
        for test in instance.tests:
            hit = node.state & test
            if hit and hit != node.state:
                for child in (hit, node.state ^ hit):
                    for generator in generators:
                        add(generator(child))
    return tuple(sources.values())


def generated_pass(instance, incumbent, base=None, enable_lifting=True,
                   weighted=False, containing_states=False,
                   actual_fallback=False, implicit_boundary=True):
    """One polynomial pass, plus exact supported-policy/fallback optimization."""
    base = {0} if base is None else set(base)
    nodes = tuple(tree_nodes(incumbent))
    base.update(node.state for node in nodes)
    sources = source_codes(instance, incumbent, weighted)
    for code in sources:
        base.update(node.state for node in tree_nodes(code))
    lift_count = 0
    if enable_lifting:
        ambient_states = ({node.state for node in nodes}
                          if containing_states else {instance.full})
        # Sources and ambients are frozen: generated exits do not seed more lifts.
        for code in sources:
            for ambient in ambient_states:
                if code.state == ambient or code.state & ambient != code.state:
                    continue
                partial = lift_partial(instance, code, ambient)
                full = finish_partial(instance, partial, incumbent)
                base.update(node.state for node in tree_nodes(full))
                lift_count += 1
    family = set(base)
    ordered = tuple(base)
    for i, a in enumerate(ordered):
        family.update(a & b for b in ordered[i + 1:])
    extras = {}
    if actual_fallback:
        result, extras = BACK.actual_restriction_dp(
            instance, family, incumbent, implicit_boundary)
        profit = incumbent.cost - result.cost
    else:
        result, profit = instance.profit_fragment(family, incumbent)
    return result, base, family, {
        "cost": incumbent.cost, "candidate_cost": result.cost,
        "source_codes": len(sources), "lifted_codes": lift_count,
        "base_states": len(base), "states": len(family),
        "profit": profit, **extras}


def synthesize(instance, incumbent=None, enable_lifting=True, weighted=False,
               containing_states=False, actual_fallback=False,
               implicit_boundary=True):
    incumbent = instance.greedy(instance.full) if incumbent is None else incumbent
    base, history = {0}, []
    for _ in range(incumbent.cost + 1):
        candidate, base, _, stats = generated_pass(
            instance, incumbent, base, enable_lifting, weighted,
            containing_states, actual_fallback, implicit_boundary)
        history.append(stats)
        if candidate.cost == incumbent.cost:
            return incumbent, history
        assert candidate.cost < incumbent.cost
        incumbent = candidate
    raise AssertionError("integer descent exceeded initial cost")


def activation_toy(b, outsiders):
    """Binary core code; outsiders have all-zero codewords and pair cover tests."""
    assert b >= 1 and outsiders >= 2 and outsiders % 2 == 0
    core_size = 1 << b
    n = core_size + outsiders
    core = (1 << core_size) - 1
    tests = [sum(1 << h for h in range(core_size) if h >> bit & 1)
             for bit in range(b)]
    # Outsider cycle edges force >=k/2 negative tests to activate all of C.
    tests += [(1 << (core_size + i)) |
              (1 << (core_size + (i + 1) % outsiders))
              for i in range(outsiders)]
    tests += [1 << (core_size + i) for i in range(outsiders)]
    instance = Instance(n, tests)
    code = instance.greedy(core)
    partial, stats = lift_statistics(instance, code)
    assert code.cost == core_size * b
    assert stats["completed_core"] == core_size - 1
    assert stats["contaminated_core_leaves"] == 1
    # Supply a complete legal incumbent, but it does not influence the pure lift.
    incumbent = instance.greedy(instance.full)
    full = finish_partial(instance, partial, incumbent)
    clean = lift_partial(instance, code, dirty_stop_depth=1)
    density_partial, density, density_stats = template_density(instance, partial)
    exact_clean_work = core_size * (b + 1) // 2 + outsiders
    assert clean.cost == exact_clean_work
    assert completed_mask(clean).bit_count() == core_size // 2
    assert density <= Fraction(exact_clean_work, core_size // 2)
    # There is deliberately no supplied membership test for C or its complement.
    assert all(test not in (core, instance.full ^ core) for test in instance.tests)
    return {"b": b, "n": n, "m": len(instance.tests), **stats,
            "minimum_all_negative_activation_tests": outsiders // 2,
            "activation_first_core_work_lower_bound": core_size * (outsiders // 2 + b),
            "greedy_full_cost": incumbent.cost,
            "lifted_complete_cost": full.cost,
            "clean_frontier_work": clean.cost,
            "clean_frontier_completed": completed_mask(clean).bit_count(),
            "clean_frontier_density": str(Fraction(clean.cost, core_size // 2)),
            "exact_template_pruning": density_stats}


def validate_execution(instance, tree):
    total = 0
    seen = set()
    for h in range(instance.n):
        bit, node, depth = 1 << h, tree, 0
        while node.test >= 0:
            assert node.state & bit
            node = node.left if instance.tests[node.test] & bit else node.right
            depth += 1
        assert node.state & bit
        seen.add(node.state)
        total += depth
    assert total == tree.cost
    leaves = [node.state for node in tree_nodes(tree) if node.test < 0]
    assert len(seen) == len(leaves)


def audit(cases=100, seed=20261019):
    rng = random.Random(seed)
    for index in range(cases):
        n = rng.randrange(3, 11)
        m = max(4, (n - 1).bit_length() + 2)
        tests = BACK.random_seed(rng, n, m)
        instance = Instance(n, tests)
        incumbent = instance.greedy(instance.full)
        core = rng.randrange(1, instance.full + 1)
        code = instance.greedy(core)
        weights = {1 << h: rng.randrange(1, n + 1) for h in range(n)}
        partial, stats = lift_statistics(instance, code, weights=weights)
        validate_execution(instance, partial)
        full = finish_partial(instance, partial, incumbent)
        validate_execution(instance, full)
        assert all(node.state.bit_count() == 1 for node in tree_nodes(full)
                   if node.test < 0)
        prefix, ratio, profile = template_density(instance, partial)
        if prefix is not None:
            validate_execution(instance, prefix)
            assert profile["completed"] == completed_mask(prefix).bit_count()
        # Exhaustively enumerate all policy prunings of the same small template.
        def all_profiles(node):
            if node.test < 0:
                return {(0, 0), (int(node.state.bit_count() == 1), 0)}
            result = {(0, 0)}
            for a, ca in all_profiles(node.left):
                for b, cb in all_profiles(node.right):
                    result.add((a + b, node.state.bit_count() + ca + cb))
            return result
        possible = [Fraction(work, count) for count, work in all_profiles(partial)
                    if count]
        assert ratio == min(possible, default=None)
    return {"audit_cases": cases, "seed": seed,
            "checks": ["direct per-hypothesis execution", "contamination and work identities",
                       "weighted prize lower bound", "collision fallback identifies all",
                       "template prefix DP equals exhaustive pruning"]}


WITNESSES = {
    "old12": (12, [96, 1042, 129, 8, 2748, 3264, 3840]),
    "adversarial12": (12, [3264, 700, 1153, 8, 1042, 97, 3840, 1022]),
    "adversarial14": (14, [536, 5860, 6400, 10368, 2061, 1027, 90, 6055]),
    "adversarial16": (16, [20736, 57344, 56032, 17588, 18624, 16772, 40448, 1234, 7735]),
    "adversarial18": (18, [536, 203199, 44160, 88107, 228858, 41456, 514, 206464, 261742]),
    "weighted18": (18, [592, 211391, 44160, 88107, 228858, 33264, 514, 206464, 259695, 9772]),
}


def benchmarks():
    result = []
    for name, (n, tests) in WITNESSES.items():
        instance = Instance(n, tests)
        greedy = instance.greedy(instance.full)
        runs = {}
        for label, lifting, weighted, actual in (
                ("conditional_only", False, False, False),
                ("global_lift", True, False, False),
                ("weighted_conditional_only", False, True, False),
                ("weighted_global_lift", True, True, False),
                ("lift_actual_boundary", True, False, True)):
            tree, history = synthesize(instance, greedy, lifting, weighted,
                                       actual_fallback=actual)
            validate_execution(instance, tree)
            runs[label] = {"cost": tree.cost, "history": history}
        # Independent exponential optimizer is validation only, never a generator.
        record = {"name": name, "n": n, "tests": tests,
                  "greedy_cost": greedy.cost, "optimum": instance.exact_cost(),
                  "runs": runs}
        result.append(record)
        print(json.dumps({"witness": name, "greedy": greedy.cost,
                          "optimum": record["optimum"],
                          "outputs": {label: run["cost"] for label, run in runs.items()}}),
              flush=True)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--benchmarks", action="store_true")
    parser.add_argument("--toy", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    output = {}
    if args.audit:
        output["audit"] = audit()
        print(json.dumps(output["audit"]), flush=True)
    if args.toy:
        output["activation_toys"] = [activation_toy(6, 12), activation_toy(10, 32),
                                     activation_toy(6, 1024)]
        for toy in output["activation_toys"]:
            print(json.dumps(toy), flush=True)
    if args.benchmarks:
        output["benchmarks"] = benchmarks()
    if args.output:
        args.output.write_text(json.dumps(output, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
