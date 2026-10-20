"""Polynomial sampling -> exact small-core code -> exact ambient palette DP.

All core sizes are <= floor(log2(n+m+1)); 2**k and 3**k are polynomial
in the original explicit input.  No m**k search occurs.  This is a candidate
generator with NO unrestricted approximation guarantee.
"""

from functools import lru_cache
import importlib.util
import json
from pathlib import Path
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, filename)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


LIFT = load("sample_palette_lift", "research-general-code-lifting.py")
PAL = load("sample_palette_exact", "research-general-lifting-global.py")


def exact_core_code(instance, core, weights=None, ambient=None):
    """Exact training objective on the listed core, not on ambient outsiders."""
    ambient = instance.full if ambient is None else ambient
    members = tuple(LIFT.bits(core))
    weights = {h: 1 for h in members} if weights is None else weights
    assert all(weights[h] > 0 for h in members)
    global_balance = [min((ambient & test).bit_count(), (ambient & ~test).bit_count())
                      for test in instance.tests]
    actions = {}

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        options = []
        for q, test in enumerate(instance.tests):
            hit = state & test
            if hit and hit != state:
                options.append((solve(hit) + solve(state ^ hit), -global_balance[q], q))
        child_score, _, query = min(options)
        actions[state] = query
        return sum(weights[h] for h in LIFT.bits(state)) + child_score

    score = solve(core)

    def build(state):
        if state.bit_count() <= 1:
            return LIFT.Tree(state)
        q = actions[state]
        hit = state & instance.tests[q]
        return instance.branch(state, q, build(hit), build(state ^ hit))

    tree = build(core)
    actual_weighted = sum(weights[h] * depth for h, depth in LIFT.leaf_depths(tree).items())
    assert actual_weighted == score
    palette = tuple(sorted({v.test for v in LIFT.tree_nodes(tree) if v.test >= 0}))
    assert len(palette) <= len(members)-1
    return tree, palette, {"core_size": len(members), "core_states": solve.cache_info().currsize,
                           "training_objective": score, "palette_size": len(palette)}


def sampled_sources(instance, incumbent, samples_per_state=2, seed=20261020,
                    incumbent_states=True, weighted_training=True):
    rng = random.Random(seed)
    k = min(instance.n, (instance.n+len(instance.tests)+1).bit_length()-1)
    ambient_states = ({v.state for v in LIFT.tree_nodes(incumbent) if v.test >= 0}
                      if incumbent_states else {instance.full})
    depth = LIFT.BACK.depth_weights(incumbent)
    requests = {}
    for ambient in sorted(ambient_states):
        members = list(LIFT.bits(ambient))
        cores = {ambient} if len(members) <= k else {
            sum(rng.sample(members, k)) for _ in range(samples_per_state)}
        for core in sorted(cores):
            modes = (False, True) if weighted_training else (False,)
            for weighted in modes:
                code, palette, stats = exact_core_code(
                    instance, core, depth if weighted else None, ambient)
                requests.setdefault(palette, {"code": code, "core": core,
                                               "weighted_training": weighted, **stats})
    return k, requests


def sampled_pass(instance, incumbent, **options):
    k, requests = sampled_sources(instance, incumbent, **options)
    best, best_palette = incumbent, ()
    total_reachable = max_reachable = 0
    lifted_best = incumbent.cost
    def finish_old(partial):
        if partial.test < 0:
            return PAL._prune(instance, incumbent, partial.state)
        return instance.branch(partial.state, partial.test,
                               finish_old(partial.left), finish_old(partial.right))
    for palette, request in requests.items():
        code = request["code"]
        lifted = finish_old(LIFT.lift_partial(instance, code))
        lifted_best = min(lifted_best, lifted.cost)
        candidate, stats = PAL.optimize_palette(instance, incumbent, palette)
        assert candidate.cost <= lifted.cost  # Palette can replay the source.
        total_reachable += stats["reachable_states"]
        max_reachable = max(max_reachable, stats["reachable_states"])
        if candidate.cost < best.cost:
            best, best_palette = candidate, palette
    return best, {"incumbent": incumbent.cost, "candidate": best.cost,
                  "sample_bound": k, "palettes": len(requests),
                  "maximum_palette_size": max(map(len, requests), default=0),
                  "maximum_reachable_states": max_reachable,
                  "total_reachable_states": total_reachable,
                  "source_replay_best": lifted_best,
                  "selected_palette": list(best_palette)}


def synthesize(instance, samples_per_state=2, seed=20261020):
    tree = instance.greedy(instance.full)
    history = []
    for iteration in range(instance.n*(instance.n-1)+1):
        candidate, stats = sampled_pass(instance, tree, samples_per_state=samples_per_state,
                                        seed=seed+iteration)
        history.append(stats)
        if candidate.cost >= tree.cost:
            return tree, history
        tree = candidate
    raise AssertionError("strict integer descent bound")


def main():
    rng = random.Random(20261020)
    checks = 0
    for n in range(3, 11):
        for _ in range(10):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if h >> b & 1)
                      for b in range((n-1).bit_length())]
            instance = LIFT.Instance(n, tests)
            core_members = rng.sample(range(n), rng.randrange(2, n+1))
            core = sum(1 << h for h in core_members)
            code, palette, stats = exact_core_code(instance, core)
            compressed_tests = [sum(1 << i for i, h in enumerate(core_members) if test >> h & 1)
                                for test in instance.tests]
            compressed = LIFT.Instance(len(core_members), compressed_tests)
            assert stats["training_objective"] == compressed.exact_cost()
            assert stats["core_states"] <= 2**len(core_members)
            incumbent = instance.greedy(instance.full)
            result, actual = PAL.optimize_palette(instance, incumbent, palette)
            assert actual["reachable_states"] <= 3**len(palette)
            # Compare against replay with the SAME incumbent-only exit macro.
            partial = LIFT.lift_partial(instance, code)
            def finish_old(node):
                if node.test < 0:
                    return PAL._prune(instance, incumbent, node.state)
                return instance.branch(node.state, node.test,
                                       finish_old(node.left), finish_old(node.right))
            assert result.cost <= finish_old(partial).cost
            assert result.cost >= instance.exact_cost()
            checks += 1
    rows = []
    for name, (n, tests) in LIFT.WITNESSES.items():
        instance = LIFT.Instance(n, tests)
        result, history = synthesize(instance)
        rows.append({"case": name, "n": n, "greedy": instance.greedy(instance.full).cost,
                     "result": result.cost, "exact_optimum": instance.exact_cost(), "history": history})
    output = {"core_palette_checks": checks, "results": rows,
              "exact_global_optimum_is_validation_only": True}
    Path("research-general-sampled-palettes-results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
