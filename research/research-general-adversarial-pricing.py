"""Adversarial search for the polynomial quadratic/verification pricer.

Exact subset optimization is used ONLY for small-instance validation.
The candidate synthesis algorithm never receives optimal values.
All randomness has an explicit seed, and witnesses retain ordered masks.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
import time
from functools import lru_cache
from itertools import combinations


def load_synthesis():
    path = Path(__file__).with_name("research-general-algorithm-next.py")
    spec = importlib.util.spec_from_file_location("pricing_synthesis", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SYN = load_synthesis()
Instance, Tree, tree_nodes = SYN.Instance, SYN.Tree, SYN.tree_nodes


@lru_cache(None)
def load_target_oracle():
    path = Path(__file__).with_name("research-general-pricing-oracle.py")
    spec = importlib.util.spec_from_file_location("pricing_target_oracle", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def valid(n, tests):
    return len({tuple(bool(test >> h & 1) for test in tests)
                for h in range(n)}) == n


def clean(n, tests):
    full = (1 << n) - 1
    return tuple(dict.fromkeys(test & full for test in tests
                               if 0 < (test & full) < full))


def extend_seed(rng, n):
    original = (96, 1042, 129, 8, 2748, 3264, 3840)
    words = [sum(((test >> h) & 1) << j for j, test in enumerate(original))
             for h in range(12)]
    while len(words) < n:
        parent = rng.choice(words)
        word = parent ^ (1 << rng.randrange(len(original)))
        if word not in words:
            words.append(word)
    return clean(n, [sum(((word >> j) & 1) << h for h, word in enumerate(words))
                     for j in range(len(original))])


def random_seed(rng, n, m):
    words = set()
    density = [rng.choice((0.12, 0.2, 0.3, 0.5, 0.7)) for _ in range(m)]
    while len(words) < n:
        words.add(sum((rng.random() < p) << j for j, p in enumerate(density)))
    words = sorted(words)
    return clean(n, [sum(((word >> j) & 1) << h for h, word in enumerate(words))
                     for j in range(m)])


def product_seed(n):
    # Two six-/seven-/...-point activation fibres, with both gated and
    # ungated local code columns.  Mutation may remove easy activation tests.
    rows = n // 2
    points = [(column, row) for column in range(2) for row in range(rows)]
    tests = [sum(1 << h for h, (c, _) in enumerate(points) if c == 0)]
    for bit in range((rows - 1).bit_length()):
        for column in (0, 1, None):
            tests.append(sum(1 << h for h, (c, r) in enumerate(points)
                             if (column is None or c == column) and r >> bit & 1))
    return clean(n, tests)


def graph_seed(rng, n):
    vertices = max(7, math.ceil(math.sqrt(2 * n)) + 2)
    edges = [(u, v) for u in range(vertices) for v in range(u)]
    rng.shuffle(edges)
    edges = edges[:n]
    return clean(n, [sum(1 << h for h, edge in enumerate(edges) if v in edge)
                     for v in range(vertices)])


def mutate(rng, n, tests, min_m=5, max_m=12):
    tests = list(tests)
    operation = rng.randrange(11)
    j = rng.randrange(len(tests))
    if operation <= 2:
        for _ in range(1 if operation < 2 else 2):
            tests[j] ^= 1 << rng.randrange(n)
    elif operation == 3:
        k = rng.randrange(len(tests))
        tests[j], tests[k] = tests[k], tests[j]
    elif operation == 4:
        probability = rng.choice((0.1, 0.2, 0.35, 0.5, 0.65, 0.8))
        tests[j] = sum((rng.random() < probability) << h for h in range(n))
    elif operation == 5:
        # Replace one hypothesis's whole response word by a nearby word.
        h, parent = rng.sample(range(n), 2)
        for k, test in enumerate(tests):
            bit = (test >> parent) & 1
            tests[k] = (test & ~(1 << h)) | (bit << h)
        tests[rng.randrange(len(tests))] ^= 1 << h
    elif operation == 6 and len(tests) > min_m:
        tests.pop(j)
    elif operation == 7 and len(tests) < max_m:
        tests.append(rng.randrange(1, (1 << n) - 1))
    elif operation in (8, 9):
        a, b = rng.sample(tests, 2)
        tests[j] = (a & b) if operation == 8 else (a ^ b)
    else:
        # A small correlated rectangle mutation can change which latent
        # context a code bit hits without changing every column at once.
        hs = rng.sample(range(n), min(3, n))
        ks = rng.sample(range(len(tests)), min(2, len(tests)))
        for k in ks:
            for h in hs:
                tests[k] ^= 1 << h
    result = clean(n, tests)
    return result if min_m <= len(result) <= max_m and valid(n, result) else None


def depth_weights(tree):
    weights = {}

    def visit(node, depth):
        if node.test < 0:
            weights[node.state] = depth
        else:
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)
    visit(tree, 0)
    return weights


def prize_greedy(instance, weights):
    @lru_cache(None)
    def mass(state):
        value = 0
        while state:
            bit = state & -state
            value += weights[bit]
            state ^= bit
        return value

    @lru_cache(None)
    def build(state):
        if state.bit_count() <= 1:
            return Tree(state)
        total = mass(state)
        options = []
        for i, test in enumerate(instance.tests):
            hit = state & test
            if hit and hit != state:
                value = mass(hit)
                options.append((max(value, total - value), i))
        _, test = min(options)
        hit = state & instance.tests[test]
        return instance.branch(state, test, build(hit), build(state ^ hit))
    return build


def actual_restriction_dp(instance, family, incumbent, implicit_boundary=True):
    """Optimize full incumbent restriction credit, with optional one-query edges.

    Outside-family children are TERMINAL incumbent-pruning macros. They
    are not inserted into the represented family and are never expanded
    recursively during this pass.
    """
    internal = tuple(node for node in tree_nodes(incumbent) if node.test >= 0)

    @lru_cache(None)
    def fallback_cost(state):
        if state.bit_count() <= 1:
            return 0
        return sum((node.state & state).bit_count() for node in internal
                   if node.left.state & state and node.right.state & state)

    values = {0: 0}
    choices = {}
    boundary_edges = 0
    for state in sorted(family, key=int.bit_count):
        if state.bit_count() <= 1:
            values[state] = 0
            choices[state] = -1
            continue
        best_cost, best_test = fallback_cost(state), -1
        for i, test in enumerate(instance.tests):
            hit = state & test
            miss = state ^ hit
            if not hit or not miss:
                continue
            supported = hit in values and miss in values
            if not implicit_boundary and not supported:
                continue
            if not supported:
                boundary_edges += 1
            left_cost = values[hit] if hit in values else fallback_cost(hit)
            right_cost = values[miss] if miss in values else fallback_cost(miss)
            cost = state.bit_count() + left_cost + right_cost
            if cost < best_cost:
                best_cost, best_test = cost, i
        values[state], choices[state] = best_cost, best_test

    def build(state):
        test = choices.get(state, -1)
        if test < 0:
            return instance.prune(incumbent, state)
        hit = state & instance.tests[test]
        return instance.branch(state, test, build(hit), build(state ^ hit))

    result = build(instance.full)
    assert result.cost == values[instance.full] <= incumbent.cost
    return result, {"actual_improvement": incumbent.cost - result.cost,
                    "implicit_boundary_edges": boundary_edges,
                    "fallback_cost_states": fallback_cost.cache_info().currsize}


def enriched_synthesis(instance, incumbent, tail_size=0, weighted_templates=True,
                       intersection_arity=2, return_state=False,
                       all_depth_thresholds=False, target_templates=False,
                       actual_fallback=False, implicit_boundary=True):
    """A fixed-exponent extension: fresh depth-prize-biased code templates.

    Each pass adds ordinary greedy and three fixed weighted greedy variants:
    depth, depth squared, and a high-depth indicator with background weight.
    """
    base = {0}
    for h in range(instance.n):
        base.update(v.state for v in tree_nodes(instance.verification_first(h)))
    if target_templates:
        oracle = load_target_oracle()
        for template in oracle.generated_templates(
                instance, incumbent, coalition_width=2,
                include_incident=False, include_coalitions=True):
            base.update(v.state for v in tree_nodes(template))
    history = []
    for _ in range(incumbent.cost + 1):
        if target_templates:
            for template in oracle.generated_templates(
                    instance, incumbent, coalition_width=2,
                    include_incident=True, include_coalitions=False):
                base.update(v.state for v in tree_nodes(template))
        weights = depth_weights(incumbent)
        threshold = sorted(weights.values())[len(weights) // 2]
        variants = [weights,
                    {h: w * w for h, w in weights.items()},
                    {h: 1 + instance.n * (w >= threshold) for h, w in weights.items()}]
        if all_depth_thresholds:
            variants.extend(
                {h: 1 + instance.n * (w >= cutoff) for h, w in weights.items()}
                for cutoff in sorted(set(weights.values()))
            )
        generators = [instance.greedy]
        if weighted_templates:
            generators += [prize_greedy(instance, w) for w in variants]
        for node in tuple(tree_nodes(incumbent)):
            base.add(node.state)
            if node.state.bit_count() <= 1:
                continue
            for test in instance.tests:
                hit = node.state & test
                if not hit or hit == node.state:
                    continue
                for child in (hit, node.state ^ hit):
                    for generator in generators:
                        base.update(v.state for v in tree_nodes(generator(child)))
        family = set(base)
        items = tuple(base)
        for i, a in enumerate(items):
            family.update(a & b for b in items[i + 1:])
        for _ in range(2, intersection_arity):
            previous = tuple(family)
            family.update(a & b for a in previous for b in items)
        for size in range(2, tail_size + 1):
            family.update(sum(1 << h for h in subset)
                          for subset in combinations(range(instance.n), size))
        extra = {}
        if actual_fallback:
            candidate, extra = actual_restriction_dp(
                instance, family, incumbent, implicit_boundary)
            profit = extra["actual_improvement"]
        else:
            candidate, profit = instance.profit_fragment(family, incumbent)
        history.append({"cost": incumbent.cost, "base_states": len(base),
                        "states": len(family), "profit": profit,
                        "candidate_cost": candidate.cost, **extra})
        if not profit:
            assert candidate.cost == incumbent.cost
            return (incumbent, history, base, family) if return_state else (incumbent, history)
        incumbent = candidate
    raise AssertionError("descent failed")


def evaluate(n, tests, fitness="baseline"):
    instance = Instance(n, tests)
    greedy = instance.greedy(instance.full)
    result, history = instance.synthesize(verification_templates=True)
    baseline_cost = result.cost
    if fitness != "baseline":
        combined = fitness in ("combined", "actual", "actual-pruned")
        result, history = enriched_synthesis(
            instance, result,
            tail_size=3 if "tail3" in fitness or combined else 0,
            weighted_templates="weighted" in fitness or combined,
            intersection_arity=3 if fitness == "cubic" else 2,
            all_depth_thresholds="levels" in fitness or combined,
            target_templates=combined,
            actual_fallback=fitness in ("actual", "actual-pruned"),
            implicit_boundary=fitness != "actual-pruned",
        )
    optimum = instance.exact_cost()
    assert optimum <= result.cost <= greedy.cost
    return {"n": n, "tests": list(tests), "m": len(tests),
            "greedy_cost": greedy.cost, "output_cost": result.cost,
            "baseline_output_cost": baseline_cost, "fitness": fitness,
            "optimum": optimum, "ratio": result.cost / optimum,
            "history": history}


def diagnose(n, tests, mode="baseline"):
    """Exact small-instance falsification of missing comparison contexts."""
    instance = Instance(n, tests)
    incumbent = instance.greedy(instance.full)
    base = {0}
    for h in range(n):
        base.update(v.state for v in tree_nodes(instance.verification_first(h)))
    for _ in range(incumbent.cost + 1):
        for node in tuple(tree_nodes(incumbent)):
            base.add(node.state)
            if node.test < 0:
                continue
            for test in instance.tests:
                hit = node.state & test
                if hit and hit != node.state:
                    for child in (hit, node.state ^ hit):
                        base.update(v.state for v in tree_nodes(instance.greedy(child)))
        family = set(base)
        items = tuple(base)
        for i, a in enumerate(items):
            family.update(a & b for b in items[i + 1:])
        candidate, profit = instance.profit_fragment(family, incumbent)
        if not profit:
            break
        incumbent = candidate
    if mode != "baseline":
        combined = mode in ("combined", "actual", "actual-pruned")
        incumbent, _, base, family = enriched_synthesis(
            instance, incumbent, tail_size=3 if "tail3" in mode or combined else 0,
            weighted_templates="weighted" in mode or combined,
            intersection_arity=3 if mode == "cubic" else 2,
            return_state=True,
            all_depth_thresholds="levels" in mode or combined,
            target_templates=combined,
            actual_fallback=mode in ("actual", "actual-pruned"),
            implicit_boundary=mode != "actual-pruned",
        )

    @lru_cache(None)
    def exact(state):
        if state.bit_count() <= 1:
            return 0, -1
        return min((state.bit_count() + exact(hit)[0] + exact(state ^ hit)[0], i)
                   for i, test in enumerate(instance.tests)
                   if (hit := state & test) and hit != state)

    def build(state):
        cost, test = exact(state)
        if test < 0:
            return Tree(state)
        hit = state & instance.tests[test]
        return instance.branch(state, test, build(hit), build(state ^ hit))

    optimum = build(instance.full)
    missing = []
    for node in tree_nodes(optimum):
        state = node.state
        if state in family:
            continue
        eligible = [a for a in base if a & state == state]
        level = {instance.full}
        visited = set(level)
        arity = None
        for depth in range(1, 7):
            new_level = {a & b for a in level for b in eligible} - visited
            if state in new_level:
                arity = depth
                break
            visited.update(new_level)
            level = new_level
        missing.append({"mask": state, "size": state.bit_count(),
                        "minimum_base_intersection_arity_up_to_6": arity,
                        "optimal_subtree_cost": node.cost})
    # Here and only here a full exponential validation oracle finds the
    # partial policy omitted by the represented-state separation routine.
    weights = depth_weights(incumbent)

    @lru_cache(None)
    def unrestricted_profit(state):
        if state.bit_count() <= 1:
            return weights.get(state, 0)
        return max(0, max(unrestricted_profit(hit) + unrestricted_profit(state ^ hit)
                          - state.bit_count()
                          for test in instance.tests
                          if (hit := state & test) and hit != state))

    supported_fallback, _ = actual_restriction_dp(instance, family, incumbent, False)
    boundary_fallback, boundary_record = actual_restriction_dp(instance, family, incumbent, True)

    return {"mode": mode, "stable_cost": incumbent.cost, "optimum_cost": optimum.cost,
            "stable_depths": [weights[1 << h] for h in range(n)],
            "optimal_root_mask": instance.tests[optimum.test],
            "missing_optimal_states": missing,
            "unrestricted_maximum_prize_work_profit": unrestricted_profit(instance.full),
            "supported_actual_fallback_cost": supported_fallback.cost,
            "boundary_actual_fallback_cost": boundary_fallback.cost,
            "actual_boundary_diagnostics": boundary_record,
            "base_states": len(base), "represented_states": len(family)}


def threshold_diagnostics(n, tests):
    instance = Instance(n, tests)
    incumbent, _ = instance.synthesize(verification_templates=True)
    incumbent, _, base, family = enriched_synthesis(
        instance, incumbent, tail_size=3, return_state=True)
    weights = depth_weights(incumbent)
    results = []
    for cutoff in sorted(set(weights.values())):
        generator = prize_greedy(instance, {
            h: 1 + n * (depth >= cutoff) for h, depth in weights.items()})
        augmented = set(base)
        for node in tree_nodes(incumbent):
            if node.test < 0:
                continue
            for test in instance.tests:
                hit = node.state & test
                if hit and hit != node.state:
                    for child in (hit, node.state ^ hit):
                        augmented.update(v.state for v in tree_nodes(generator(child)))
        represented = set(augmented)
        items = tuple(augmented)
        for i, a in enumerate(items):
            represented.update(a & b for b in items[i + 1:])
        represented.update(sum(1 << h for h in subset)
                           for size in (2, 3)
                           for subset in combinations(range(n), size))
        candidate, profit = instance.profit_fragment(represented, incumbent)
        results.append({"depth_cutoff": cutoff,
                        "target_hypotheses": [h for h in range(n) if weights[1 << h] >= cutoff],
                        "new_base_states": len(augmented - base),
                        "profit": profit, "candidate_cost": candidate.cost})
    return {"incumbent_cost": incumbent.cost, "thresholds": results}


def audit_actual_fallback(cases=80, seed=20261018):
    rng = random.Random(seed)
    for _ in range(cases):
        n = rng.randrange(3, 9)
        tests = random_seed(rng, n, rng.randrange(5, 8))
        instance = Instance(n, tests)
        incumbent = instance.greedy(instance.full)
        base = {0} | {node.state for node in tree_nodes(incumbent)}
        for test in instance.tests:
            base.update((test, instance.full ^ test))
        family = set(base)
        for a in base:
            family.update(a & b for b in base)
        prize_candidate, _ = instance.profit_fragment(family, incumbent)
        restricted, _ = actual_restriction_dp(instance, family, incumbent, False)
        boundary, _ = actual_restriction_dp(instance, family, incumbent, True)
        assert boundary.cost <= restricted.cost <= prize_candidate.cost <= incumbent.cost
        optimum = instance.exact_cost()
        all_states = set(range(instance.full + 1))
        exhaustive, _ = actual_restriction_dp(instance, all_states, incumbent, True)
        assert exhaustive.cost == optimum <= boundary.cost
        # Verify reconstructed policy directly against its physical query table.
        total = 0
        for h in range(n):
            node, depth = boundary, 0
            while node.test >= 0:
                assert node.state >> h & 1
                node = node.left if instance.tests[node.test] >> h & 1 else node.right
                depth += 1
            assert node.state == 1 << h
            total += depth
        assert total == boundary.cost
        for state in all_states:
            formula = sum((node.state & state).bit_count()
                          for node in tree_nodes(incumbent)
                          if node.test >= 0
                          and node.left.state & state and node.right.state & state)
            assert formula == instance.prune(incumbent, state).cost
    return {"actual_fallback_audit_cases": cases, "status": "passed"}


def search(n, iterations, seed, checkpoint, report_every=100, fitness="baseline",
           seed_input=None):
    rng = random.Random(seed)
    cache = {}
    seeds = [extend_seed(rng, n), product_seed(n), graph_seed(rng, n)]
    if seed_input:
        supplied = json.loads(Path(seed_input).read_text(encoding="utf-8"))
        assert supplied["n"] == n
        seeds.insert(0, tuple(supplied["tests"]))
    seeds.extend(random_seed(rng, n, rng.randint(7, 10)) for _ in range(5))

    def score(tests):
        if tests not in cache:
            cache[tests] = evaluate(n, tests, fitness)
        return cache[tests]

    def fitness_key(item):
        return (item["ratio"], item["output_cost"] - item["optimum"],
                item["baseline_output_cost"] / item["optimum"],
                item["greedy_cost"] / item["optimum"])

    archive = [score(tests) for tests in seeds if valid(n, tests)]
    archive.sort(key=fitness_key, reverse=True)
    current = archive[0]
    best = current
    accepted = 0
    started = time.time()
    for iteration in range(iterations):
        if rng.random() < 0.35:
            parent = rng.choice(archive[:min(8, len(archive))])
        else:
            parent = current
        proposal = mutate(rng, n, tuple(parent["tests"]))
        if proposal is None:
            continue
        candidate = score(proposal)
        # Flat fitness regions are retained; rare uphill moves escape local
        # mutation minima.  Fitness is the ACTUAL complete synthesized ratio.
        temperature = 0.007 + 0.02 * (1 - iteration / max(1, iterations))
        delta = candidate["ratio"] - current["ratio"]
        if delta >= 0 or rng.random() < math.exp(delta / temperature):
            current = candidate
            accepted += 1
        if all(candidate["tests"] != item["tests"] for item in archive):
            archive.append(candidate)
            archive.sort(key=fitness_key, reverse=True)
            del archive[20:]
        if fitness_key(candidate) > fitness_key(best):
            best = candidate
            print(json.dumps({"new_best": best, "iteration": iteration}), flush=True)
            checkpoint.write_text(json.dumps(best, indent=2), encoding="utf-8")
        if (iteration + 1) % report_every == 0:
            print(json.dumps({"progress": {"n": n, "iteration": iteration + 1,
                  "distinct_valid_evaluations": len(cache), "accepted": accepted,
                  "best_ratio": best["ratio"], "seconds": time.time() - started}}), flush=True)
    instance = Instance(n, best["tests"])
    baseline, _ = instance.synthesize(verification_templates=True)
    searched = baseline
    if fitness != "baseline":
        combined = fitness in ("combined", "actual", "actual-pruned")
        searched, _ = enriched_synthesis(
            instance, baseline,
            tail_size=3 if "tail3" in fitness or combined else 0,
            weighted_templates="weighted" in fitness or combined,
            intersection_arity=3 if fitness == "cubic" else 2,
            all_depth_thresholds="levels" in fitness or combined,
            target_templates=combined,
            actual_fallback=fitness in ("actual", "actual-pruned"),
            implicit_boundary=fitness != "actual-pruned",
        )
    enriched, enrichment_history = enriched_synthesis(instance, searched)
    best = dict(best, evaluations=len(cache), iterations=iterations,
                enriched_output_cost=enriched.cost,
                enriched_ratio=enriched.cost / best["optimum"],
                enrichment_history=enrichment_history)
    best["diagnosis"] = diagnose(n, best["tests"], fitness)
    checkpoint.write_text(json.dumps(best, indent=2), encoding="utf-8")
    print(json.dumps({"finished": best}), flush=True)
    return best


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=16)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=190611385)
    parser.add_argument("--output", default="research-general-adversarial-witness.json")
    parser.add_argument("--diagnose-input")
    parser.add_argument("--threshold-input")
    parser.add_argument("--audit-actual", action="store_true")
    parser.add_argument("--finalize-input")
    parser.add_argument("--seed-input")
    parser.add_argument("--fitness", choices=("baseline", "weighted", "tail3", "weighted-tail3", "weighted-levels-tail3", "cubic", "combined", "actual", "actual-pruned"),
                        default="baseline")
    args = parser.parse_args()
    if args.finalize_input:
        path = Path(args.finalize_input)
        data = json.loads(path.read_text(encoding="utf-8"))
        log_path = path.with_suffix(".log")
        progress = None
        log_bytes = log_path.read_bytes()
        log_text = log_bytes.decode("utf-16" if log_bytes.startswith(b"\xff\xfe") else "utf-8-sig")
        for line in log_text.splitlines():
            try:
                parsed = json.loads(line)
            except json.JSONDecodeError:
                continue
            if "progress" in parsed:
                progress = parsed["progress"]
        data["search_status"] = "wrapped at requested checkpoint; no background process remains"
        data["last_completed_progress_checkpoint"] = progress
        data["diagnosis"] = diagnose(data["n"], data["tests"], data.get("fitness", "baseline"))
        assert data["diagnosis"]["stable_cost"] == data["output_cost"]
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(json.dumps(data))
        return
    if args.audit_actual:
        print(json.dumps(audit_actual_fallback()))
        return
    if args.threshold_input:
        data = json.loads(Path(args.threshold_input).read_text(encoding="utf-8"))
        print(json.dumps(threshold_diagnostics(data["n"], data["tests"])))
        return
    if args.diagnose_input:
        path = Path(args.diagnose_input)
        data = json.loads(path.read_text(encoding="utf-8"))
        data["diagnosis"] = diagnose(data["n"], data["tests"], data.get("fitness", "baseline"))
        instance = Instance(data["n"], data["tests"])
        baseline, _ = instance.synthesize(verification_templates=True)
        enriched, history = enriched_synthesis(instance, baseline)
        data["enriched_output_cost"] = enriched.cost
        data["enriched_ratio"] = enriched.cost / data["optimum"]
        data["enrichment_history"] = history
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")
        print(json.dumps(data))
        return
    search(args.n, args.iterations, args.seed, Path(args.output),
           fitness=args.fitness, seed_input=args.seed_input)


if __name__ == "__main__":
    main()
