"""Exact affine-cover support pruning for polynomial query-family selection.

Only Gaussian elimination is used. A column is removed only when its weight
is zero in EVERY REAL solution of A x = 1; a real solution is not interpreted
as a legal partition. Accepted partitions are checked using actual masks.
"""

from fractions import Fraction
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


SELECT = load("linear_selector_portfolio", "research-general-query-selectors.py")
CONTEXT = SELECT.CONTEXT


def affine_cover_support(n, cells, audit=False):
    """Return supported column indices, with an exact affine-space certificate.

    An inconsistent equation system has no cover and returns no columns.
    If audit=True, verify the particular solution and each kernel generator
    independently against the original incidence equations.
    """
    width = len(cells)
    rows = [[Fraction(bool(cell >> h & 1)) for cell in cells] + [Fraction(1)]
            for h in range(n)]
    pivots = []
    rank = 0
    for column in range(width):
        pivot = next((r for r in range(rank, n) if rows[r][column]), None)
        if pivot is None:
            continue
        rows[rank], rows[pivot] = rows[pivot], rows[rank]
        scale = rows[rank][column]
        rows[rank] = [value / scale for value in rows[rank]]
        for r in range(n):
            if r == rank or not rows[r][column]:
                continue
            scale = rows[r][column]
            rows[r] = [a - scale*b for a, b in zip(rows[r], rows[rank])]
        pivots.append(column)
        rank += 1
        if rank == n:
            break
    if any(not any(row[:width]) and row[-1] for row in rows):
        return (), {"consistent": False, "columns": width, "rank": rank,
                    "forced_zero_columns": width}
    free = tuple(column for column in range(width) if column not in pivots)
    supported = set(free)
    particular = [Fraction(0)] * width
    for row, pivot in zip(rows, pivots):
        particular[pivot] = row[-1]
        if row[-1] or any(row[column] for column in free):
            supported.add(pivot)
    if audit:
        def image(vector):
            return [sum(vector[q] for q, cell in enumerate(cells) if cell >> h & 1)
                    for h in range(n)]
        assert image(particular) == [1] * n
        kernel = []
        for column in free:
            vector = [Fraction(0)] * width
            vector[column] = 1
            for row, pivot in zip(rows, pivots):
                vector[pivot] = -row[column]
            assert image(vector) == [0] * n
            kernel.append(vector)
        assert supported == {q for q in range(width)
                             if particular[q] or any(vector[q] for vector in kernel)}
    return tuple(sorted(supported)), {
        "consistent": True, "columns": width, "rank": rank,
        "affine_dimension": len(free), "forced_zero_columns": width-len(supported)}


def linear_partition_components(instance, audit=False):
    by_size = {}
    for q, test in enumerate(instance.tests):
        for cell in (test, instance.full ^ test):
            if cell and cell != instance.full:
                by_size.setdefault(cell.bit_count(), {}).setdefault(cell, q)
    accepted, diagnostics = [], []
    for size, original in sorted(by_size.items()):
        cells = tuple(sorted(original))
        keep, stats = affine_cover_support(instance.n, cells, audit)
        diagnostics.append({"cell_size": size, **stats,
                            "supported_queries": tuple(sorted({original[cells[q]] for q in keep}))})
        masks = tuple(cells[q] for q in keep)
        adjacent = {cell: set() for cell in masks}
        for a, b in combinations(masks, 2):
            if not a & b:
                adjacent[a].add(b)
                adjacent[b].add(a)
        unseen = set(masks)
        while unseen:
            first = min(unseen)
            pending, component = [first], set()
            unseen.remove(first)
            while pending:
                cell = pending.pop()
                component.add(cell)
                fresh = adjacent[cell] & unseen
                unseen.difference_update(fresh)
                pending.extend(fresh)
            if len(component)*size != instance.n:
                continue
            if any(a & b for a, b in combinations(component, 2)):
                continue
            assert sum(component) == instance.full
            accepted.append({"cell_size": size, "cells": tuple(sorted(component)),
                             "queries": tuple(sorted({original[cell] for cell in component}))})
    return accepted, diagnostics


def linear_select_families(instance, independence=True):
    original, _, _ = SELECT.select_families(instance, independence=False)
    initial = set(original)
    partitions, diagnostics = linear_partition_components(instance)
    # Retain this menu even when supported cells still have interfering
    # disjointness edges and no whole component is a partition.
    initial.update(tuple(item["supported_queries"]) for item in diagnostics
                   if item["consistent"])
    by_size = {}
    for partition in partitions:
        initial.add(partition["queries"])
        by_size.setdefault(partition["cell_size"], set()).update(partition["queries"])
    initial.update(tuple(sorted(queries)) for queries in by_size.values())
    if partitions:
        initial.add(tuple(sorted({q for p in partitions for q in p["queries"]})))
    families, cache = set(initial), {}
    for retained in sorted(initial):
        if not independence:
            continue
        factors = CONTEXT.ResponseFactors(instance, retained)
        cache[retained] = factors
        for subset in range(1 << len(factors.alphabets)):
            families.add(SELECT.independent_queries(instance, factors, subset))
    return tuple(sorted(families)), cache, partitions, diagnostics


def linear_selected_context_pass(instance, independence=True, recombine=True):
    families, cache, partitions, diagnostics = linear_select_families(instance, independence)
    incumbent = best = instance.greedy(instance.full)
    pool = {0} | {node.state for node in CONTEXT.BACK.tree_nodes(incumbent)}
    contexts = 0
    for retained in families:
        factors = cache.get(retained) or CONTEXT.ResponseFactors(instance, retained)
        tree, states, stats = CONTEXT.plan_factors(instance, factors, retained_fallback=True)
        pool.update(states)
        contexts += stats["contexts"]
        if tree.cost < best.cost:
            best = tree
    if recombine:
        tree, _ = instance.profit_fragment(pool, incumbent)
        assert tree.cost <= best.cost
        best = tree
    return best, pool, {"initial_cost": incumbent.cost, "output_cost": best.cost,
                        "selected_families": len(families), "pool_states": len(pool),
                        "contexts": contexts, "linear_partitions": len(partitions),
                        "linear_systems": diagnostics, "retained_row_fallback": True,
                        "both_old_and_retained_decoder_states_are_pooled": True}


def main():
    rng = random.Random(2026101913)
    systems = partition_checks = 0
    for n in range(2, 9):
        full = (1 << n)-1
        for _ in range(5):
            size = rng.randrange(1, n)
            candidates = [cell for cell in range(1, full) if cell.bit_count() == size]
            rng.shuffle(candidates)
            cells = tuple(candidates[:9])
            support, _ = affine_cover_support(n, cells, audit=True)
            supported = set(support)
            # Independent exhaustive partition audit is bounded validation only.
            for selection in range(1 << len(cells)):
                chosen = [q for q in range(len(cells)) if selection >> q & 1]
                if sum(cells[q].bit_count() for q in chosen) != n:
                    continue
                if any(cells[a] & cells[b] for a, b in combinations(chosen, 2)):
                    continue
                assert set(chosen) <= supported
                partition_checks += 1
            systems += 1

    bridge = load("linear_selector_bridge", "research-general-bridge-aliases.py")
    cases = []
    for parameters in ((2, 2, 2), (3, 2, 1), (3, 2, 2)):
        instance, points, tags, _, half_rectangle = bridge.make_instance(*parameters)
        alphabet = 1 << parameters[0]
        partitions, diagnostics = linear_partition_components(instance, audit=True)
        selected = tuple(sorted({q for p in partitions if p["cell_size"] == instance.n//alphabet
                                 for q in p["queries"]}))
        truth = tuple(q for q, tag in enumerate(tags) if tag[0] == "selectoreq")
        assert selected == truth
        factors = CONTEXT.ResponseFactors(instance, selected)
        assert factors.alphabets == (alphabet,)*parameters[1]
        tree, _, stats = CONTEXT.plan_factors(instance, factors, retained_fallback=True)
        CONTEXT.execute(instance, tree)
        equality = Fraction(alphabet+1, 2)-Fraction(1, alphabet)
        bound = instance.n*(parameters[1]*equality+parameters[2]*(parameters[0]-1))
        assert tree.cost <= bound
        case = {"n": instance.n, "queries": len(instance.tests), "parameters": parameters,
                "half_alphabet_bridge": half_rectangle,
                "initial_cost": instance.greedy(instance.full).cost,
                "linear_selector_candidate_cost": tree.cost, "comparison_upper": str(bound),
                "recovered_exactly_pure_selectors": True,
                "selector_factor_contexts": stats["contexts"], "linear_systems": diagnostics}
        if instance.n == 64:
            old, _, _ = SELECT.selected_context_pass(instance)
            new, _, complete_stats = linear_selected_context_pass(instance)
            CONTEXT.execute(instance, new)
            assert old.cost == case["initial_cost"] and new.cost <= tree.cost < old.cost
            case["old_portfolio_cost"] = old.cost
            case["entire_extended_portfolio"] = complete_stats
        cases.append(case)
    output = {"status": "passed", "bounded_affine_systems": systems,
              "exhaustive_legal_partition_preservation_checks": partition_checks,
              "bridge_repairs": cases, "no_exact_UDT_oracle": True,
              "no_unrestricted_approximation_claim": True}
    Path(__file__).with_name("research-general-linear-selectors-results.json").write_text(
        json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
