"""Polynomial query-family selection before response-factor context planning.

The selection depth is fixed: root minority/partition families, followed by
one independence refinement over factor subsets. New families do not recurse.
"""

from itertools import combinations
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


CONTEXT = load("selected_contexts", "research-general-factor-contexts.py")


def partition_components(instance):
    """Try whole disjointness components, never maximum clique/subfamily search."""
    by_size = {}
    for q, test in enumerate(instance.tests):
        for cell in (test, instance.full ^ test):
            if cell and cell != instance.full:
                by_size.setdefault(cell.bit_count(), {}).setdefault(cell, q)
    accepted = []
    for size, cells in sorted(by_size.items()):
        masks = tuple(cells)
        adjacent = {mask: set() for mask in masks}
        for a, b in combinations(masks, 2):
            if not a & b:
                adjacent[a].add(b)
                adjacent[b].add(a)
        unseen = set(masks)
        while unseen:
            first = min(unseen)
            component, pending = set(), [first]
            unseen.remove(first)
            while pending:
                current = pending.pop()
                component.add(current)
                fresh = adjacent[current] & unseen
                unseen.difference_update(fresh)
                pending.extend(fresh)
            if len(component)*size != instance.n:
                continue
            if any(a & b for a, b in combinations(component, 2)):
                continue
            assert sum(component) == instance.full
            accepted.append({"cell_size": size, "cells": tuple(sorted(component)),
                             "queries": tuple(sorted({cells[mask] for mask in component}))})
    return accepted


def independent_queries(instance, factors, subset):
    """Independence uses actual original-h counts, not uniform quotient words."""
    groups = {}
    indices = [i for i in range(len(factors.alphabets)) if subset >> i & 1]
    for h, label in enumerate(factors.labels):
        key = tuple(label[i] for i in indices)
        groups[key] = groups.get(key, 0) | (1 << h)
    return tuple(q for q, test in enumerate(instance.tests)
                 if all(instance.n*(test & group).bit_count() == group.bit_count()*test.bit_count()
                        for group in groups.values()))


def select_families(instance, independence=True):
    initial = set()
    for threshold in sorted({min(test.bit_count(), instance.n-test.bit_count())
                             for test in instance.tests if test and test != instance.full}):
        initial.add(tuple(q for q, test in enumerate(instance.tests)
                          if min(test.bit_count(), instance.n-test.bit_count()) >= threshold))
    partitions = partition_components(instance)
    by_size = {}
    for partition in partitions:
        initial.add(partition["queries"])
        by_size.setdefault(partition["cell_size"], set()).update(partition["queries"])
    initial.update(tuple(sorted(queries)) for queries in by_size.values())
    if partitions:
        initial.add(tuple(sorted({q for partition in partitions for q in partition["queries"]})))
    families = set(initial)
    factor_cache = {}

    def factor(retained):
        if retained not in factor_cache:
            factor_cache[retained] = CONTEXT.ResponseFactors(instance, retained)
        return factor_cache[retained]

    if independence:
        # Freeze this list: no new independence family seeds another level.
        for retained in sorted(initial):
            factors = factor(retained)
            assert (1 << len(factors.alphabets)) <= instance.n
            for subset in range(1 << len(factors.alphabets)):
                families.add(independent_queries(instance, factors, subset))
    return tuple(sorted(families)), factor_cache, partitions


def selected_context_pass(instance, independence=True, recombine=True):
    families, cache, partitions = select_families(instance, independence)
    incumbent = instance.greedy(instance.full)
    best = incumbent
    pool = {0} | {node.state for node in CONTEXT.BACK.tree_nodes(incumbent)}
    history = []
    for retained in families:
        factors = cache.get(retained)
        if factors is None:
            factors = CONTEXT.ResponseFactors(instance, retained)
        candidate, states, stats = CONTEXT.plan_factors(instance, factors)
        pool.update(states)
        history.append(stats)
        if candidate.cost < best.cost:
            best = candidate
    if recombine:
        candidate, _ = instance.profit_fragment(pool, incumbent)
        assert candidate.cost <= best.cost
        best = candidate
    return best, pool, {"initial_greedy_cost": incumbent.cost, "output_cost": best.cost,
                        "selected_families": len(families), "partition_components": len(partitions),
                        "contexts_summed_across_families": sum(item["contexts"] for item in history),
                        "pool_states": len(pool), "one_independence_refinement_level": independence}


def main():
    rng = random.Random(2026101904)
    cases = independence_checks = partition_checks = 0
    for n in range(2, 10):
        for _ in range(3):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if h >> bit & 1)
                      for bit in range((n-1).bit_length())]
            instance = CONTEXT.BACK.Instance(n, tests)
            tree, _, stats = selected_context_pass(instance)
            CONTEXT.execute(instance, tree)
            assert CONTEXT.independent_optimum(instance) <= tree.cost <= instance.greedy(instance.full).cost
            _, cache, partitions = select_families(instance)
            for partition in partitions:
                cells = partition["cells"]
                assert sum(cell.bit_count() for cell in cells) == instance.n
                assert not any(a & b for a, b in combinations(cells, 2))
                partition_checks += 1
            for factors in cache.values():
                for subset in range(1 << len(factors.alphabets)):
                    selected = set(independent_queries(instance, factors, subset))
                    # Independent elementary frequency audit of every selected
                    # response against each joint factor-label event.
                    axes = [i for i in range(len(factors.alphabets)) if subset >> i & 1]
                    events = {tuple(label[i] for i in axes) for label in factors.labels}
                    for q in selected:
                        for event in events:
                            hits = sum(bool(instance.tests[q] >> h & 1) and
                                       tuple(factors.labels[h][i] for i in axes) == event for h in range(n))
                            mass = sum(tuple(label[i] for i in axes) == event for label in factors.labels)
                            assert n*hits == instance.tests[q].bit_count()*mass
                            independence_checks += 1
            cases += 1

    # Pairwise independence does NOT imply that the whole retained tuple is
    # independent. The algorithm never assumes otherwise.
    labels = [(x, z) for x in range(2) for z in range(2)]
    tests = [sum(1 << h for h, (x, z) in enumerate(labels) if z),
             sum(1 << h for h, (x, z) in enumerate(labels) if x),
             sum(1 << h for h, (x, z) in enumerate(labels) if x ^ z)]
    instance = CONTEXT.BACK.Instance(4, tests)
    factors = CONTEXT.ResponseFactors(instance, (0,))
    kept = independent_queries(instance, factors, 1)
    assert kept == (1, 2)
    assert len({tuple(bool(tests[q] >> h & 1) for q in kept) for h in range(4)}) == 4

    # Rotating activation seed: minority thresholds alone cannot select the
    # selector-only family. Joint-body independence does select it exactly.
    rotating = load("selected_rotating_validation", "research-general-rotating-aliases.py")
    raw, points, tags = rotating.make_instance(3, 1, 2)
    instance = CONTEXT.BACK.Instance(raw.n, raw.tests)
    high = tuple(q for q, test in enumerate(instance.tests)
                 if min(test.bit_count(), instance.n-test.bit_count()) > instance.n//8)
    factors = CONTEXT.ResponseFactors(instance, high)
    kept = independent_queries(instance, factors, (1 << len(factors.alphabets))-1)
    assert all(tags[q][0] == "eq" and tags[q][1] < 1 for q in kept)
    assert len(kept) == 8
    selectors = CONTEXT.ResponseFactors(instance, kept)
    repaired, _, repair_stats = CONTEXT.plan_factors(instance, selectors)
    CONTEXT.execute(instance, repaired)
    assert repaired.cost <= instance.greedy(instance.full).cost
    rotating_stats = {**repair_stats, "n": instance.n,
                      "initial_cost": instance.greedy(instance.full).cost, "output_cost": repaired.cost}
    portfolio, _, portfolio_stats = selected_context_pass(instance)
    CONTEXT.execute(instance, portfolio)
    assert portfolio.cost <= repaired.cost

    # XOR masking makes the gates themselves independent of all body values.
    # Whole disjointness components nevertheless isolate selector partitions.
    camouflage = load("selected_xor_validation", "research-general-xor-aliases.py")
    raw, _, tags = camouflage.make_instance(2, 2, 2)
    instance = CONTEXT.BACK.Instance(raw.n, raw.tests)
    accepted = partition_components(instance)
    selector_queries = {q for partition in accepted if partition["cell_size"] == instance.n//4
                        for q in partition["queries"]}
    assert selector_queries == {q for q, tag in enumerate(tags) if tag[0] == "selectoreq"}
    camouflage_tree, _, camouflage_stats = selected_context_pass(instance)
    CONTEXT.execute(instance, camouflage_tree)

    output = {"status": "passed", "small_full_portfolio_instances": cases,
              "exact_independence_event_checks": independence_checks,
              "accepted_partition_checks": partition_checks,
              "XOR_joint_independence_caveat_verified": True,
              "rotating_seed_information_repair": rotating_stats,
              "rotating_seed_full_portfolio": portfolio_stats,
              "XOR_camouflage_full_portfolio": camouflage_stats,
              "no_unrestricted_approximation_claim": True}
    Path(__file__).with_name("research-general-query-selectors-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
