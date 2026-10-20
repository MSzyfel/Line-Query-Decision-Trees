"""Adversarial audit of frozen-pool global conditional-code lifting.

All tree synthesis is the fixed-exponent candidate from code-lifting.py.
Exponential subset optimization appears only in the validation/search fitness.
No article source is changed.
"""

from __future__ import annotations

import argparse
from functools import lru_cache
import importlib.util
import json
import math
from pathlib import Path
import random
import sys
import time


def load_lifting():
    path = Path(__file__).with_name("research-general-code-lifting.py")
    spec = importlib.util.spec_from_file_location("lift_adversary_backend", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


LIFT = load_lifting()
BACK = LIFT.BACK
Instance, Tree, tree_nodes = LIFT.Instance, LIFT.Tree, LIFT.tree_nodes


def expansion(n, source_n, tests, rng):
    """Keep a saved hard table, add near-duplicate response words."""
    m = len(tests)
    words = [sum(((test >> h) & 1) << j for j, test in enumerate(tests))
             for h in range(source_n)]
    if n < len(words):
        words = words[:n]
    while len(words) < n:
        parent = rng.choice(words)
        word = parent ^ sum(1 << j for j in rng.sample(range(m), rng.choice((1, 1, 2))))
        if word not in words:
            words.append(word)
    return BACK.clean(n, [sum(((word >> j) & 1) << h for h, word in enumerate(words))
                          for j in range(m)])


def substitution(n, source_n, source_tests, rng, camouflage=True):
    """Replace a small table by fibres, with mixed-context local copy codes."""
    points = [(h, copy) for copy in range(math.ceil(n / source_n))
              for h in range(source_n)][:n]
    copies = max(copy for _, copy in points) + 1
    tests = [sum(1 << h for h, (base, _) in enumerate(points)
                 if test >> base & 1) for test in source_tests]
    # Each base hypothesis has its own identifying copy bit.  Camouflage
    # answers on other fibres introduce collisions without changing its code.
    for base in range(source_n):
        partner = rng.randrange(source_n)
        for bit in range((copies - 1).bit_length()):
            tests.append(sum(1 << h for h, (a, copy) in enumerate(points)
                             if ((a == base) or (camouflage and a == partner))
                             and copy >> bit & 1))
    return BACK.clean(n, tests)


def camouflage_grid(n, columns, rng, aliases=1, recursive=False):
    """Coordinate codes whose outside answers cover many core code outputs."""
    rows = math.ceil(n / columns)
    points = [(column, row) for column in range(columns) for row in range(rows)][:n]
    b = (rows - 1).bit_length()
    tests = [sum(1 << h for h, (a, _) in enumerate(points) if a == column)
             for column in range(columns)]
    for column in range(columns):
        partners = [a for a in range(columns) if a != column]
        rng.shuffle(partners)
        shifts = {a: rng.randrange(1 << b) for a in partners[:aliases]}
        for bit in range(b):
            tests.append(sum(1 << h for h, (a, row) in enumerate(points)
                             if (a == column and row >> bit & 1) or
                             (a in shifts and (row ^ shifts[a]) >> bit & 1)))
    # Unions of the same small row blocks give a competing global code.
    if recursive:
        for size in (1, 2, 3):
            for start in range(0, rows, size + 1):
                tests.append(sum(1 << h for h, (_, row) in enumerate(points)
                                 if start <= row < min(rows, start + size)))
    else:
        for row in range(0, rows, 2):
            tests.append(sum(1 << h for h, (_, value) in enumerate(points)
                             if value == row))
    return BACK.clean(n, tests)


def sparse_code(n, rng, m=18):
    """Sparse fixed-weight response words: long rare-positive corridors."""
    words = set()
    while len(words) < n:
        size = rng.choice((1, 2, 2, 3))
        words.add(sum(1 << i for i in rng.sample(range(m), size)))
    words = sorted(words)
    tests = [sum(1 << h for h, word in enumerate(words) if word >> j & 1)
             for j in range(m)]
    rng.shuffle(tests)
    return BACK.clean(n, tests)


def cube_code(n, rng, decoys):
    """A known information-optimal coordinate code, preceded by decoy tests."""
    extra = []
    for _ in range(decoys):
        size = rng.choice((n // 2, n // 2, (n + 1) // 2, n // 3))
        extra.append(sum(1 << h for h in rng.sample(range(n), size)))
    coordinates = [sum(1 << h for h in range(n) if h >> bit & 1)
                   for bit in range((n - 1).bit_length())]
    return BACK.clean(n, extra + coordinates)


def parity_majority_code(d, rng, decoys):
    """Nonlinear resilient decoys before a known coordinate code (d=6,9,...)."""
    assert d % 3 == 0
    width = d // 3
    n = 1 << d
    extras = []
    for _ in range(decoys):
        variables = list(range(d))
        rng.shuffle(variables)
        groups = [variables[i * width:(i + 1) * width] for i in range(3)]
        flips = rng.randrange(8)
        positive = 0
        for h in range(n):
            values = [((sum((h >> j) & 1 for j in block) & 1) ^ (flips >> i & 1))
                      for i, block in enumerate(groups)]
            if sum(values) >= 2:
                positive |= 1 << h
        extras.append(positive)
    return BACK.clean(n, extras + [sum(1 << h for h in range(n) if h >> bit & 1)
                                   for bit in range(d)])


def resilient_trade(test, d, rng, attempts=40, protected=0):
    """Flip a checkerboard 2-face, preserving balance and one-bit marginals."""
    for _ in range(attempts):
        i, j = rng.sample(range(d), 2)
        base = rng.randrange(1 << d) & ~(1 << i) & ~(1 << j)
        points = (base, base | 1 << i, base | 1 << j, base | 1 << i | 1 << j)
        if any(protected >> h & 1 for h in points):
            continue
        values = tuple((test >> h) & 1 for h in points)
        if values in ((0, 1, 1, 0), (1, 0, 0, 1)):
            return test ^ sum(1 << h for h in points)
    return test


def resilient_code(d, rng, decoys):
    n = 1 << d
    extras = []
    for _ in range(decoys):
        test = sum(1 << h for h in range(n) if h.bit_count() & 1)
        for _ in range(40):
            test = resilient_trade(test, d, rng)
        assert test.bit_count() == n // 2
        for bit in range(d):
            assert sum(1 for h in range(n) if h >> bit & 1 and test >> h & 1) == n // 4
        extras.append(test)
    coordinates = [sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(d)]
    return BACK.clean(n, extras + coordinates)


def diverse_resilient_code(d, rng, decoys, clustered=False):
    n = 1 << d
    initial = resilient_code(d, rng, 1)[0]
    coordinates = [sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(d)]
    protected = 0
    if clustered:
        baseline = Instance(n, [initial] + coordinates)
        tree = baseline.greedy(baseline.full)
        bad = [node for node in tree_nodes(tree) if node.test >= 0 and
               node.cost > node.state.bit_count() * ((node.state.bit_count() - 1).bit_length() + 1)
               - (1 << (node.state.bit_count() - 1).bit_length())]
        if bad:
            protected = min(bad, key=lambda node: node.state.bit_count()).state
    chosen = {initial}
    current = initial
    attempts = 0
    while len(chosen) < decoys:
        attempts += 1
        if attempts > 10000:
            raise AssertionError(("insufficient genuinely distinct resilient decoys", d, len(chosen)))
        if not clustered:
            current = sum(1 << h for h in range(n) if h.bit_count() & 1)
        for _ in range(12 if clustered else 40):
            current = resilient_trade(current, d, rng, protected=protected)
        if current not in chosen and ((1 << n) - 1) ^ current not in chosen:
            chosen.add(current)
    extras = [initial] + sorted(chosen - {initial})
    return BACK.clean(n, extras + coordinates), protected


def large_test_suite(path, seed):
    rng = random.Random(seed)
    records = []
    for d in (5, 6):
        for clustered in (False, True):
            for count in (32, 64, 128):
                tests, protected = diverse_resilient_code(d, rng, count, clustered)
                started = time.time()
                record = evaluate(1 << d, tests, "strong", known_coordinate_certificate=True)
                record.update({"distinct_resilient_decoys": count, "clustered": clustered,
                               "protected_hypotheses": protected.bit_count(),
                               "seconds": time.time() - started})
                records.append(record)
                path.write_text(json.dumps(records, indent=2), encoding="utf-8")
                print(json.dumps({k: record[k] for k in
                      ("n", "m", "clustered", "greedy_cost", "plain_cost", "output_cost",
                       "optimum", "seconds")}), flush=True)
    return records


def adaptive_camouflage(d, rng, extra_decoys=0):
    """Known balanced ADAPTIVE code, with a common outside camouflage answer."""
    n = 1 << d
    full = (1 << n) - 1
    common = resilient_code(d, rng, 1)[0]
    masks = [common]
    programs = {}
    priority = list(range(n))
    rng.shuffle(priority)

    def generate(start, size):
        if size == 1:
            return
        core = ((1 << size) - 1) << start
        left = ((1 << (size // 2)) - 1) << start
        query = left | (common & (full ^ core))
        difference = n // 2 - query.bit_count()
        if difference:
            eligible = [h for h in priority if not (core >> h & 1)
                        and bool(query >> h & 1) == (difference < 0)]
            assert len(eligible) >= abs(difference)
            query ^= sum(1 << h for h in eligible[:abs(difference)])
        assert query.bit_count() == n // 2 and query & core == left
        programs[core] = query
        masks.append(query)
        generate(start, size // 2)
        generate(start + size // 2, size // 2)
    generate(0, n)
    # Redundant clustered variants increase physical query diversity without
    # supplying a static coordinate palette.  They are optional in the suite.
    current = common
    for _ in range(extra_decoys):
        for _ in range(4):
            current = resilient_trade(current, d, rng)
        masks.insert(1, current)
    instance = Instance(n, BACK.clean(n, masks))

    def build(start, size):
        core = ((1 << size) - 1) << start
        if size == 1:
            return Tree(core)
        query = instance.tests.index(programs[core])
        return instance.branch(core, query, build(start, size // 2),
                               build(start + size // 2, size // 2))
    certificate = build(0, n)
    assert certificate.cost == n * d
    return instance, certificate


def reserve_adaptive_camouflage(d):
    """Known optimal adaptive code with a PROVED linear static-palette demand."""
    assert d >= 6
    n, full = 1 << d, (1 << (1 << d)) - 1
    quarter = n // 4
    reserve = (1 << (n // 2)) - 1
    common = sum(1 << h for h in range(n)
                 if sum((h >> j) & 1 for j in (1, 2, 3)) >= 2)
    masks, programs = [common], {}

    def generate(start, size):
        if size == 1:
            return
        core = ((1 << size) - 1) << start
        left = ((1 << (size // 2)) - 1) << start
        query = left | (common & (full ^ core))
        difference = n // 2 - query.bit_count()
        if difference:
            # Only reserve points may have camouflage compensation altered.
            eligible = [h for h in range(n // 2)
                        if not (core >> h & 1) and
                        bool(query >> h & 1) == (difference < 0)]
            assert len(eligible) >= abs(difference)
            query ^= sum(1 << h for h in eligible[:abs(difference)])
        assert query.bit_count() == n // 2 and query & core == left
        programs[core] = query
        masks.append(query)
        generate(start, size // 2)
        generate(start + size // 2, size // 2)
    generate(0, n)
    instance = Instance(n, BACK.clean(n, masks))
    program = {state: instance.tests.index(query) for state, query in programs.items()}
    certificate = certificate_from_program(instance, program)
    forced = []
    for h in range(n // 2, n, 2):
        distinguishing = [j for j, test in enumerate(instance.tests)
                          if bool(test >> h & 1) != bool(test >> (h + 1) & 1)]
        assert len(distinguishing) == 1
        pair = (1 << h) | (1 << (h + 1))
        assert distinguishing[0] == program[pair]
        forced.append(distinguishing[0])
    assert len(set(forced)) == n // 4
    return instance, certificate, forced


def reserve_adaptive_suite(path):
    records = []
    for d in (6, 7):
        instance, certificate, forced = reserve_adaptive_camouflage(d)
        record = evaluate(instance.n, instance.tests, "strong",
                          known_optimum_tree=certificate)
        record.update({"family": "reserve-protected adaptive majority camouflage",
                       "forced_static_palette_queries": len(forced),
                       "forced_query_indices": forced})
        records.append(record)
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(json.dumps({k: record[k] for k in
              ("n", "m", "greedy_cost", "plain_cost", "output_cost", "optimum",
               "forced_static_palette_queries")}), flush=True)
    return records


def adaptive_suite(path, seed, depths=(5, 6), trials=12, mode="strong"):
    rng = random.Random(seed)
    records = []
    for d in depths:
        for trial in range(trials):
            instance, certificate = adaptive_camouflage(d, rng, extra_decoys=0)
            started = time.time()
            record = evaluate(instance.n, instance.tests, mode,
                              known_optimum_tree=certificate)
            record.update({"trial": trial, "family": "adaptive common-f camouflage",
                           "seconds": time.time() - started})
            records.append(record)
            path.write_text(json.dumps(records, indent=2), encoding="utf-8")
            print(json.dumps({k: record[k] for k in
                  ("n", "m", "trial", "greedy_cost", "plain_cost", "output_cost",
                   "optimum", "seconds")}), flush=True)
            if record["output_cost"] > record["optimum"]:
                print(json.dumps({"fixed_point": True, "index": len(records) - 1}), flush=True)
                return records
    return records


def certificate_from_program(instance, program):
    def build(state):
        if state.bit_count() == 1:
            return Tree(state)
        query = program[state]
        hit = state & instance.tests[query]
        assert hit.bit_count() * 2 == state.bit_count()
        return instance.branch(state, query, build(hit), build(state ^ hit))
    return build(instance.full)


def adaptive_search(n, iterations, seed, path, mode="strong"):
    """Mutate only answers irrelevant to a fixed known optimal adaptive code."""
    d = (n - 1).bit_length()
    assert n == 1 << d
    rng = random.Random(seed)
    cache = {}
    started = time.time()

    def score(tests, program):
        key = tuple(tests)
        if key not in cache:
            instance = Instance(n, tests)
            certificate = certificate_from_program(instance, program)
            item = evaluate(n, tests, mode, known_optimum_tree=certificate)
            item["certificate_program"] = sorted(program.items())
            cache[key] = item
        return cache[key]

    def rank(item):
        return (item["ratio"], item["plain_cost"] / item["optimum"],
                item["plain_history"][0]["candidate_cost"] / item["optimum"],
                item["greedy_cost"] / item["optimum"])

    archive = []
    for trial in range(8):
        instance, certificate = adaptive_camouflage(d, rng)
        program = {node.state: node.test for node in tree_nodes(certificate) if node.test >= 0}
        archive.append(score(instance.tests, program))
    archive.sort(key=rank, reverse=True)
    current = best = archive[0]
    for iteration in range(iterations):
        parent = rng.choice(archive[:8]) if rng.random() < 0.4 else current
        tests = list(parent["tests"])
        program = dict(parent["certificate_program"])
        required = [0] * len(tests)
        for state, j in program.items():
            required[j] |= state
        editable = [j for j, core in enumerate(required) if core != (1 << n) - 1]
        j = rng.choice(editable)
        outside = ((1 << n) - 1) ^ required[j]
        positives = list(LIFT.bits(outside & tests[j]))
        negatives = list(LIFT.bits(outside & ~tests[j]))
        if not positives or not negatives:
            continue
        for _ in range(rng.choice((1, 1, 1, 2, 4))):
            tests[j] ^= rng.choice(positives) | rng.choice(negatives)
        if len(set(tests)) != len(tests):
            continue
        # Rebalance if repeated choices in a multi-swap changed cardinality.
        if tests[j].bit_count() != n // 2:
            continue
        candidate = score(tests, program)
        delta = candidate["ratio"] - current["ratio"]
        temperature = 0.003 + 0.01 * (1 - iteration / max(1, iterations))
        if delta >= 0 or rng.random() < math.exp(delta / temperature):
            current = candidate
        if all(candidate["tests"] != old["tests"] for old in archive):
            archive.append(candidate)
            archive.sort(key=rank, reverse=True)
            del archive[24:]
        if rank(candidate) > rank(best):
            best = candidate
            print(json.dumps({"adaptive_new_best": {k: best[k] for k in
                  ("n", "m", "greedy_cost", "plain_cost", "output_cost", "optimum")}}), flush=True)
        if (iteration + 1) % 50 == 0:
            saved = dict(best, status="running", family="adaptive outside-answer mutation",
                         iterations_completed=iteration + 1, evaluations=len(cache),
                         seed=seed, seconds=time.time() - started)
            path.write_text(json.dumps(saved, indent=2), encoding="utf-8")
            print(json.dumps({"adaptive_progress": {k: saved[k] for k in
                  ("n", "iterations_completed", "evaluations", "plain_cost", "output_cost",
                   "optimum", "seconds")}}), flush=True)
    saved = dict(best, status="complete", family="adaptive outside-answer mutation",
                 iterations_completed=iterations, evaluations=len(cache), seed=seed,
                 seconds=time.time() - started)
    path.write_text(json.dumps(saved, indent=2), encoding="utf-8")
    print(json.dumps({"adaptive_finished": {k: saved[k] for k in
          ("n", "iterations_completed", "evaluations", "plain_cost", "output_cost", "optimum",
           "seconds")}}), flush=True)
    return saved


def audit(seed=7):
    rng = random.Random(seed)
    exact_cases = 0
    for n in range(3, 19):
        for _ in range(3):
            instance = Instance(n, BACK.random_seed(rng, n, 8))
            tree, solve = exact_tree(instance)
            assert tree.cost == instance.exact_cost()
            LIFT.validate_execution(instance, tree)
            exact_cases += 1
    resilient_cases = 0
    for d in (4, 5, 6):
        for _ in range(10):
            tests = resilient_code(d, rng, 1)
            first = tests[0]
            n = 1 << d
            assert first.bit_count() == n // 2
            for bit in range(d):
                coordinate = sum(1 << h for h in range(n) if h >> bit & 1)
                assert (first & coordinate).bit_count() == n // 4
            resilient_cases += 1
    adaptive_cases = 0
    for d in (3, 4, 5, 6):
        for _ in range(8):
            instance, certificate = adaptive_camouflage(d, rng)
            LIFT.validate_execution(instance, certificate)
            assert certificate.cost == instance.n * d
            assert all(test.bit_count() == instance.n // 2 for test in instance.tests)
            adaptive_cases += 1
    return {"exact_bound_against_unpruned_dp": exact_cases,
            "resilient_balance_and_marginal_checks": resilient_cases,
            "adaptive_code_execution_and_information_optimality": adaptive_cases,
            "seed": seed}


def coordinate_escape(path):
    source = json.loads(Path(__file__).with_name(
        "research-general-lift-resilient-n64.json").read_text(encoding="utf-8"))[0]
    instance = Instance(source["n"], source["tests"])
    incumbent = instance.greedy(instance.full)
    d = (instance.n - 1).bit_length()
    coordinate_tests = {sum(1 << h for h in range(instance.n) if h >> bit & 1)
                        for bit in range(d)}
    coordinate_tests |= {instance.full ^ test for test in tuple(coordinate_tests)}
    candidates = []
    for code in LIFT.source_codes(instance, incumbent):
        if any(instance.tests[node.test] not in coordinate_tests
               for node in tree_nodes(code) if node.test >= 0):
            continue
        partial = LIFT.lift_partial(instance, code)
        exits = []
        correct = True
        for leaf in tree_nodes(partial):
            if leaf.test >= 0:
                continue
            count = leaf.state.bit_count()
            dimension = (count - 1).bit_length()
            old_cost = instance.prune(incumbent, leaf.state).cost
            fresh_cost = instance.greedy(leaf.state).cost
            cost = min(old_cost, fresh_cost)
            if count != 1 << dimension or cost != count * dimension:
                correct = False
                break
            exits.append({"state": leaf.state, "size": count,
                          "dimension": dimension, "incumbent_restriction_cost": old_cost,
                          "fresh_greedy_cost": fresh_cost, "selected_fallback_cost": cost})
        if correct:
            work = partial.cost + sum(exit["selected_fallback_cost"] for exit in exits)
            assert work == instance.n * d
            candidates.append((code.state.bit_count(), code.state, code, partial, exits))
    _, _, code, partial, exits = min(candidates, key=lambda item: item[:2])
    result = {"n": instance.n, "tests": list(instance.tests),
              "greedy_cost": incumbent.cost, "optimum": instance.n * d,
              "core": code.state, "core_size": code.state.bit_count(),
              "core_work": code.cost, "lifted_partial_work": partial.cost,
              "code_program": [(node.state, node.test) for node in tree_nodes(code)],
              "exits": exits, "full_selected_fallback_cost": instance.n * d,
              "exits_requiring_fresh_greedy": sum(
                  exit["incumbent_restriction_cost"] > exit["selected_fallback_cost"]
                  for exit in exits),
              "number_of_such_sources": len(candidates)}
    path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({k: result[k] for k in
          ("n", "greedy_cost", "optimum", "core_size", "core_work",
           "lifted_partial_work", "number_of_such_sources")}))
    return result


def resilient_suite(path, seed=2026101805):
    rng = random.Random(seed)
    records = []
    for count in (1, 2, 3, 5, 8):
        tests = parity_majority_code(6, rng, count)
        record = evaluate(64, tests, "plain", known_coordinate_certificate=True)
        assert record["optimum"] == 384
        if record["output_cost"] > record["optimum"]:
            record["diagnosis"] = diagnose(record)
            strong = evaluate(64, tests, "strong", known_coordinate_certificate=True)
            record["strong_result"] = strong
            if strong["output_cost"] > strong["optimum"]:
                record["strong_diagnosis"] = diagnose(strong)
        records.append(record)
        path.write_text(json.dumps(records, indent=2), encoding="utf-8")
        print(json.dumps({"resilient_decoys": count, "greedy": record["greedy_cost"],
                          "plain": record["output_cost"], "optimum": record["optimum"],
                          "strong": record.get("strong_result", {}).get("output_cost")}), flush=True)
    return records


def seed_bank(n, rng, include_cube=True):
    seeds = []
    for name in ("adversarial12", "adversarial18", "weighted18"):
        source_n, tests = LIFT.WITNESSES[name]
        seeds.append(("expanded-" + name, expansion(n, source_n, tests, rng)))
        seeds.append(("substitution-" + name, substitution(n, source_n, tests, rng)))
    for columns in (3, 4, 5, 6):
        for aliases in (0, 1, 2):
            seeds.append((f"camouflage-{columns}-{aliases}",
                          camouflage_grid(n, columns, rng, aliases, True)))
    seeds.extend(("sparse-code", sparse_code(n, rng, m)) for m in (12, 18, 22))
    seeds.append(("graph-incidence", BACK.graph_seed(rng, n)))
    seeds.append(("biased-code", BACK.random_seed(rng, n, 12)))
    if include_cube:
        seeds.extend((f"known-coordinate-code-{d}", cube_code(n, rng, d))
                     for d in (2, 4, 6, 9, 12))
    return [(label, tests) for label, tests in seeds if BACK.valid(n, tests)]


def evaluate(n, tests, mode="plain", retain_histories=True,
             known_coordinate_certificate=False, known_optimum_tree=None):
    instance = Instance(n, tests)
    greedy = instance.greedy(instance.full)
    if known_coordinate_certificate or known_optimum_tree is not None:
        level = (n - 1).bit_length()
        bound = n * (level + 1) - (1 << level)
        coordinates = [sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(level)]
        if known_optimum_tree is None:
            assert all(test in instance.tests for test in coordinates)
        else:
            LIFT.validate_execution(instance, known_optimum_tree)
            assert known_optimum_tree.cost == bound
        if greedy.cost == bound:
            return {"n": n, "m": len(instance.tests), "tests": list(instance.tests),
                    "mode": mode, "greedy_cost": bound, "plain_cost": bound,
                    "output_cost": bound, "optimum": bound, "ratio": 1.0,
                    "validation_exact_states": 0,
                    "explicit_optimum_coordinate_certificate": known_coordinate_certificate,
                    "explicit_optimum_adaptive_certificate": known_optimum_tree is not None,
                    "strong_first_pass_optimum_certificate": mode == "strong",
                    "initial_tree_information_optimal": True,
                    "plain_history": [{"cost": bound, "candidate_cost": bound,
                                       "information_bound_optimality_certificate": True}],
                    "strong_history": []}
    plain, plain_history = LIFT.synthesize(instance, greedy)
    if known_coordinate_certificate or known_optimum_tree is not None:
        coordinates = [sum(1 << h for h in range(n) if h >> bit & 1)
                       for bit in range((n - 1).bit_length())]
        if known_optimum_tree is None:
            assert all(test in instance.tests for test in coordinates)
        level = (n - 1).bit_length()
        optimum = n * (level + 1) - (1 << level)
        exact_stats = {"states": 0}
    else:
        _, solve, exact_stats = exact_tree(instance, initial_tree=plain, return_stats=True)
        optimum = solve(instance.full)
    assert optimum <= plain.cost <= greedy.cost
    strong = None
    shortcut = False
    if mode == "strong":
        # The first strong family contains the first plain family.  Its exact
        # actual-credit DP is no worse than the plain depth-prize splice.
        # If that first plain splice already attains OPT, the strong output is
        # certified exactly OPT without constructing all its surplus templates.
        if plain_history[0]["candidate_cost"] == optimum:
            strong_cost, strong_history, shortcut = optimum, [], True
        else:
            strong, strong_history = LIFT.synthesize(
                instance, greedy, weighted=True, actual_fallback=True)
            strong_cost = strong.cost
            LIFT.validate_execution(instance, strong)
        cost = strong_cost
    else:
        strong_history, cost = [], plain.cost
    result = {"n": n, "m": len(instance.tests), "tests": list(instance.tests),
              "mode": mode, "greedy_cost": greedy.cost, "plain_cost": plain.cost,
              "output_cost": cost, "optimum": optimum, "ratio": cost / optimum,
              "validation_exact_states": exact_stats["states"],
              "explicit_optimum_coordinate_certificate": known_coordinate_certificate,
              "explicit_optimum_adaptive_certificate": known_optimum_tree is not None,
              "strong_first_pass_optimum_certificate": shortcut}
    if retain_histories:
        result.update({"plain_history": plain_history, "strong_history": strong_history})
    return result


def exact_tree(instance, initial_tree=None, return_stats=False):
    actions = {}
    fallbacks = {}
    statistics = {"states": 0, "information_bound_prunings": 0}

    def information_bound(count):
        if count <= 1:
            return 0
        level = (count - 1).bit_length()
        return count * (level + 1) - (1 << level)

    @lru_cache(None)
    def solve(state):
        statistics["states"] += 1
        if state.bit_count() <= 1:
            return 0
        fallback = (initial_tree if initial_tree is not None and state == instance.full
                    else instance.greedy(state))
        fallbacks[state] = fallback
        best, action = fallback.cost, -1
        size = state.bit_count()
        options = []
        for j, test in enumerate(instance.tests):
            hit = state & test
            if hit and hit != state:
                miss = state ^ hit
                lower = size + information_bound(hit.bit_count()) + information_bound(miss.bit_count())
                options.append((lower, j, hit, miss))
        for lower, j, hit, miss in sorted(options):
            if lower >= best:
                statistics["information_bound_prunings"] += 1
                continue
            # Solve the smaller side first; then its exact value may already
            # prune the second call. This affects only validation runtime.
            if hit.bit_count() > miss.bit_count():
                hit, miss = miss, hit
            left = solve(hit)
            if size + left + information_bound(miss.bit_count()) >= best:
                statistics["information_bound_prunings"] += 1
                continue
            value = size + left + solve(miss)
            if value < best:
                best, action = value, j
        actions[state] = action
        return best

    def build(state):
        if state.bit_count() <= 1:
            return Tree(state)
        query = actions[state]
        if query < 0:
            return fallbacks[state]
        hit = state & instance.tests[query]
        return instance.branch(state, query, build(hit), build(state ^ hit))

    solve(instance.full)
    return (build(instance.full), solve, statistics) if return_stats else (build(instance.full), solve)


def diagnose(record):
    instance = Instance(record["n"], record["tests"])
    incumbent = instance.greedy(instance.full)
    strong = record.get("mode") == "strong"
    base, history = {0}, []
    while True:
        candidate, base, family, stats = LIFT.generated_pass(
            instance, incumbent, base, weighted=strong, actual_fallback=strong)
        history.append(stats)
        if candidate.cost == incumbent.cost:
            break
        incumbent = candidate
    optimum, conditional_opt = exact_tree(instance)
    missing = []
    for node in tree_nodes(optimum):
        if node.state not in family:
            missing.append({"state": node.state, "size": node.state.bit_count(),
                            "greedy_conditional_cost": instance.greedy(node.state).cost,
                            "optimum_conditional_cost": conditional_opt(node.state)})
    sources = LIFT.source_codes(instance, incumbent, weighted=strong)
    cores = {code.state for code in sources}
    collisions = []
    for code in sources:
        partial, stats = LIFT.lift_statistics(
            instance, code, weights=BACK.depth_weights(incumbent))
        prefix, rho, profile = LIFT.template_density(instance, partial)
        collisions.append({"core": code.state, "core_size": code.state.bit_count(),
                           "core_cost": code.cost,
                           "core_optimum": conditional_opt(code.state),
                           "completed": stats["completed_core"],
                           "contaminated": stats["contaminated_core_leaves"],
                           "density": str(rho), "prefix": profile})
    # This exponential policy pricing is an independent validation oracle.
    # It reveals whether the global fixed point is genuinely improvable.
    all_states = set()

    def collect(state):
        if state in all_states:
            return
        all_states.add(state)
        for test in instance.tests:
            hit = state & test
            if hit and hit != state:
                collect(hit)
                collect(state ^ hit)
    collect(instance.full)
    unrestricted, profit = instance.profit_fragment(all_states, incumbent)
    supported_actual, supported_stats = BACK.actual_restriction_dp(
        instance, family, incumbent, False)
    boundary_actual, boundary_stats = BACK.actual_restriction_dp(
        instance, family, incumbent, True)
    missing_core = [entry for entry in missing if entry["state"] not in cores]
    return {"stable_cost": incumbent.cost, "optimum": optimum.cost,
            "history": history, "base_states": len(base), "represented_states": len(family),
            "missing_optimum_states": missing, "missing_optimum_core_states": missing_core,
            "distinct_source_cores": len(cores), "source_codes": len(sources),
            "source_collision_profiles": collisions,
            "unrestricted_depth_profit": profit,
            "unrestricted_splice_cost": unrestricted.cost,
            "supported_actual_cost": supported_actual.cost,
            "boundary_actual_cost": boundary_actual.cost}


def search(n, iterations, seed, path, mode="plain", max_m=26, seed_input=None,
           known_code=False, resilient=False, legacy_bank=False, legacy_rank=False):
    assert not resilient or n == 1 << (n - 1).bit_length()
    rng = random.Random(seed)
    cache = {}
    labels = {}
    started = time.time()

    def score(tests, label="mutation"):
        key = tuple(tests)
        if key not in cache:
            cache[key] = evaluate(n, key, mode,
                                  known_coordinate_certificate=known_code or resilient)
            labels[key] = label
            if label != "mutation":
                print(json.dumps({"seed_result": {"label": label, "n": n,
                      "m": cache[key]["m"], "output_cost": cache[key]["output_cost"],
                      "optimum": cache[key]["optimum"],
                      "seconds_including_seeds": time.time() - started}}), flush=True)
        return cache[key]

    def key(item):
        if legacy_rank:
            return (item["ratio"], item["plain_cost"] / item["optimum"],
                    item["greedy_cost"] / item["optimum"])
        return (item["ratio"], item["plain_history"][0]["candidate_cost"] / item["optimum"],
                item["plain_cost"] / item["optimum"],
                item["greedy_cost"] / item["optimum"])

    bank = ([(f"resilient-trades-{count}", resilient_code((n - 1).bit_length(), rng, count))
             for count in (1, 2, 3, 4, 5, 6, 8)] if resilient else
            [(f"known-coordinate-code-{d}", cube_code(n, rng, d))
             for d in (2, 3, 4, 5, 6, 8, 10, 12)] if known_code else
            seed_bank(n, rng, include_cube=not legacy_bank))
    if seed_input:
        saved = json.loads(Path(seed_input).read_text(encoding="utf-8"))
        bank.insert(0, ("saved-input", expansion(n, saved["n"], saved["tests"], rng)))
    archive = [score(tests, label) for label, tests in bank]
    archive.sort(key=key, reverse=True)
    del archive[24:]
    current, best = archive[0], archive[0]
    seed_bank_seconds = time.time() - started
    accepted = 0
    path.write_text(json.dumps(dict(best, status="running", seed=seed,
                                   iterations_completed=0, evaluations=len(cache)), indent=2),
                    encoding="utf-8")
    print(json.dumps({"seed_bank": [{"label": labels[tuple(item["tests"])],
                                     "n": n, "m": item["m"], "cost": item["output_cost"],
                                     "optimum": item["optimum"]} for item in archive]}), flush=True)
    for iteration in range(iterations):
        parent = rng.choice(archive[:8]) if rng.random() < 0.4 else current
        if resilient and rng.random() < 0.85:
            d = (n - 1).bit_length()
            coordinates = [sum(1 << h for h in range(n) if h >> bit & 1) for bit in range(d)]
            decoys = [test for test in parent["tests"] if test not in coordinates]
            if decoys:
                j = rng.randrange(len(decoys))
                decoys[j] = resilient_trade(decoys[j], d, rng)
                if rng.random() < 0.1:
                    rng.shuffle(decoys)
            proposal = BACK.clean(n, decoys + coordinates)
        else:
            proposal = BACK.mutate(rng, n, parent["tests"], min_m=6, max_m=max_m)
        if (known_code or resilient) and proposal is not None:
            # Coordinate queries are retained, so the binary information lower
            # bound is always attained by a known legal full tree.
            coordinates = [sum(1 << h for h in range(n) if h >> bit & 1)
                           for bit in range((n - 1).bit_length())]
            proposal = BACK.clean(n, list(proposal) + coordinates)
        if proposal is None:
            continue
        candidate = score(proposal)
        temperature = 0.004 + 0.012 * (1 - iteration / max(1, iterations))
        delta = candidate["ratio"] - current["ratio"]
        if delta >= 0 or rng.random() < math.exp(delta / temperature):
            current = candidate
            accepted += 1
        if all(candidate["tests"] != item["tests"] for item in archive):
            archive.append(candidate)
            archive.sort(key=key, reverse=True)
            del archive[24:]
        if key(candidate) > key(best):
            best = candidate
            saved = dict(best, status="running", seed=seed, iterations_completed=iteration + 1,
                         evaluations=len(cache), seconds=time.time() - started)
            path.write_text(json.dumps(saved, indent=2), encoding="utf-8")
            print(json.dumps({"new_best": saved}), flush=True)
        if (iteration + 1) % 100 == 0:
            checkpoint = dict(best, status="running", seed=seed,
                              iterations_completed=iteration + 1, evaluations=len(cache),
                              seconds=time.time() - started, accepted=accepted)
            path.write_text(json.dumps(checkpoint, indent=2), encoding="utf-8")
            print(json.dumps({"progress": {k: checkpoint[k] for k in
                  ("n", "mode", "iterations_completed", "evaluations", "ratio", "seconds")}}),
                  flush=True)
    finished = dict(best, status="complete", seed=seed, iterations_completed=iterations,
                    evaluations=len(cache), seconds=time.time() - started, accepted=accepted,
                    origin=labels[tuple(best["tests"])], seed_bank_seconds=seed_bank_seconds)
    if best["output_cost"] > best["optimum"]:
        finished["diagnosis"] = diagnose(best)
    path.write_text(json.dumps(finished, indent=2), encoding="utf-8")
    print(json.dumps({"finished": {k: finished[k] for k in
          ("n", "mode", "iterations_completed", "evaluations", "ratio", "seconds")}}), flush=True)
    return finished


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=24)
    parser.add_argument("--iterations", type=int, default=1000)
    parser.add_argument("--seed", type=int, default=2026101801)
    parser.add_argument("--mode", choices=("plain", "strong"), default="plain")
    parser.add_argument("--output", type=Path, default=Path("research-general-lift-adversary.json"))
    parser.add_argument("--max-m", type=int, default=26)
    parser.add_argument("--seed-input")
    parser.add_argument("--diagnose")
    parser.add_argument("--known-code", action="store_true")
    parser.add_argument("--resilient-suite", action="store_true")
    parser.add_argument("--resilient", action="store_true")
    parser.add_argument("--large-test-suite", action="store_true")
    parser.add_argument("--adaptive-suite", action="store_true")
    parser.add_argument("--adaptive-search", action="store_true")
    parser.add_argument("--large-adaptive-suite", action="store_true")
    parser.add_argument("--reserve-adaptive-suite", action="store_true")
    parser.add_argument("--audit", action="store_true")
    parser.add_argument("--verify-input")
    parser.add_argument("--coordinate-escape", action="store_true")
    parser.add_argument("--legacy-structured-bank", action="store_true")
    parser.add_argument("--legacy-rank", action="store_true")
    args = parser.parse_args()
    if args.reserve_adaptive_suite:
        reserve_adaptive_suite(args.output)
    elif args.coordinate_escape:
        coordinate_escape(args.output)
    elif args.audit:
        result = audit()
        args.output.write_text(json.dumps(result, indent=2), encoding="utf-8")
        print(json.dumps(result))
    elif args.verify_input:
        path = Path(args.verify_input)
        record = json.loads(path.read_text(encoding="utf-8"))
        instance = Instance(record["n"], record["tests"])
        strong, history = LIFT.synthesize(instance, weighted=True, actual_fallback=True)
        LIFT.validate_execution(instance, strong)
        record["explicit_strong_validation"] = {"cost": strong.cost, "history": history}
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(json.dumps({"n": instance.n, "strong": strong.cost,
                          "optimum": record["optimum"], "passes": len(history)}))
    elif args.large_adaptive_suite:
        adaptive_suite(args.output, args.seed, depths=(7,), trials=4, mode="plain")
    elif args.adaptive_search:
        adaptive_search(args.n, args.iterations, args.seed, args.output, args.mode)
    elif args.adaptive_suite:
        adaptive_suite(args.output, args.seed)
    elif args.large_test_suite:
        large_test_suite(args.output, args.seed)
    elif args.resilient_suite:
        resilient_suite(args.output, args.seed)
    elif args.diagnose:
        path = Path(args.diagnose)
        record = json.loads(path.read_text(encoding="utf-8"))
        record["diagnosis"] = diagnose(record)
        path.write_text(json.dumps(record, indent=2), encoding="utf-8")
        print(json.dumps({"cost": record["diagnosis"]["stable_cost"],
                          "optimum": record["diagnosis"]["optimum"],
                          "missing": record["diagnosis"]["missing_optimum_states"]}))
    else:
        search(args.n, args.iterations, args.seed, args.output, args.mode,
               args.max_m, args.seed_input, args.known_code, args.resilient,
               args.legacy_structured_bank, args.legacy_rank)


if __name__ == "__main__":
    main()
