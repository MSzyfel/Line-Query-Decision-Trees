"""Selected-row cores with legal continuations and capped-prize pricing.

The polynomial candidate menu uses A=U. Exhaustive subset SFM below is ONLY
small-input validation of the polynomial-SFM theorem, never the large menu.
"""
from __future__ import annotations

import importlib.util
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

_spec = importlib.util.spec_from_file_location(
    "rank_core_validation", Path(__file__).with_name("research-general-rank-core.py"))
_rank = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _rank
_spec.loader.exec_module(_rank)
Instance, CoreNode = _rank.Instance, _rank.CoreNode


def greedy_code(instance, cell):
    if cell.bit_count() == 1:
        return CoreNode(cell), 0
    candidates = []
    for j, test in enumerate(instance.tests):
        positive = cell & test
        if positive and positive != cell:
            candidates.append((max(positive.bit_count(),
                                   (cell ^ positive).bit_count()), j))
    _, j = min(candidates)
    positive = cell & instance.tests[j]
    zero, w0 = greedy_code(instance, cell ^ positive)
    one, w1 = greedy_code(instance, positive)
    return CoreNode(cell, j, zero, one), cell.bit_count() + w0 + w1


def signature_classes(instance, rows):
    classes = {}
    for h in range(instance.n):
        signature = tuple((instance.tests[j] >> h) & 1 for j in rows)
        classes[signature] = classes.get(signature, 0) | (1 << h)
    return tuple(classes.values())


def selected_rank(instance, rows, core):
    return _rank.binary_rank([
        1 + sum(((instance.tests[j] >> h) & 1) << (k + 1)
                for k, j in enumerate(rows))
        for h in range(instance.n) if core & (1 << h)])


def continuation_data(instance, rows):
    result = {}
    for cell in signature_classes(instance, rows):
        root, work = greedy_code(instance, cell)
        result[cell] = (root, work, Fraction(work, cell.bit_count()))
    return result


def construct_core_code(instance, rows, core, data):
    pivots = {}
    assert _rank.add_to_basis(core, pivots)
    queries = []
    for j in rows:
        if _rank.add_to_basis(instance.tests[j] & core, pivots):
            queries.append(j)
    assert len(queries) == selected_rank(instance, rows, core) - 1
    assert all(not (cell & core) or cell & core == cell for cell in data)

    def build(cell, start):
        while start < len(queries):
            j = queries[start]
            positive = cell & instance.tests[j]
            if positive and positive != cell:
                zero, w0 = build(cell ^ positive, start + 1)
                one, w1 = build(positive, start + 1)
                return CoreNode(cell, j, zero, one), cell.bit_count() + w0 + w1
            start += 1
        root, work, _ = data[cell]
        return root, work
    return build(core, 0)


def surplus(core, weights, cap, n):
    return sum(cap + min(weight, cap) for h, weight in enumerate(weights)
               if core & (1 << h)) - cap * n


def exhaustive_ratio_oracle(instance, rows, ground, mean, weights, cap):
    """Exponential SFM stand-in ONLY for finite validation."""
    subsets = [core for core in range(1 << instance.n) if core & ground == core]
    ranks = {core: selected_rank(instance, rows, core) for core in subsets}
    gains = {core: surplus(core, weights, cap, instance.n) for core in subsets}
    if gains[ground] <= 0:
        assert all(gain <= 0 for gain in gains.values())
        return None
    core = ground
    ratio = Fraction(gains[core], 1) / (ranks[core] + mean)
    iterations = 0
    while True:
        def objective(candidate):
            g = ranks[candidate] + (mean if candidate else 0)
            modular = gains[candidate] + cap * instance.n
            return ratio * g - modular
        optimum = min(subsets, key=lambda candidate: (objective(candidate), candidate))
        if objective(optimum) >= -cap * instance.n:
            break
        new_ratio = Fraction(gains[optimum], 1) / (ranks[optimum] + mean)
        assert new_ratio > ratio
        core, ratio = optimum, new_ratio
        iterations += 1
        assert iterations <= instance.n ** 3
    exact = max(Fraction(gains[candidate], 1) / (ranks[candidate] + mean)
                for candidate in subsets if gains[candidate] > 0)
    assert ratio == exact
    return core, ratio, iterations


def audit_candidate(instance, rows, data, mean, core, weights, cap):
    assert core
    assert all(not (cell & core) or cell & core == cell for cell in data)
    assert all(data[cell][2] <= mean for cell in data if cell & core)
    root, core_work = construct_core_code(instance, rows, core, data)
    rank = selected_rank(instance, rows, core)
    g = rank + mean
    assert core_work <= core.bit_count() * (g - 1)
    work, completed, _ = _rank.lift(instance, root)
    assert work <= 2 * core_work
    assert completed.bit_count() >= 2 * core.bit_count() - instance.n
    prize = sum(weight for h, weight in enumerate(weights)
                if completed & (1 << h))
    z = surplus(core, weights, cap, instance.n)
    assert prize >= z
    if z > 0:
        assert prize > 0
        assert Fraction(work, prize) <= Fraction(2 * instance.n, 1) * g / z
    return {"core_size": core.bit_count(), "rank": rank,
            "continuation_mean_bound": str(mean), "core_work": core_work,
            "lifted_work": work, "completed": completed.bit_count(),
            "actual_finished_prize": prize, "surplus": z,
            "positive_profit": prize - work}


def balance_row_families(instance):
    """A fixed polynomial library; no subsets of rows are enumerated."""
    ordered = sorted(range(len(instance.tests)), key=lambda j: (
        -min(instance.tests[j].bit_count(),
             instance.n - instance.tests[j].bit_count()), j))
    families = {(), tuple(ordered)}
    for length in range(1, len(ordered)):
        families.add(tuple(ordered[:length]))
        families.add(tuple(ordered[length:]))
    return sorted(families, key=lambda rows: (len(rows), rows))


def candidate_menu(instance, weights):
    """Polynomial executable menu using full filtered grounds, without SFM."""
    best = None
    evaluated = 0
    for rows in balance_row_families(instance):
        data = continuation_data(instance, rows)
        for mean in sorted({item[2] for item in data.values()}):
            ground = sum(cell for cell, item in data.items() if item[2] <= mean)
            row = audit_candidate(instance, rows, data, mean, ground, weights, 1)
            evaluated += 1
            if row["actual_finished_prize"] > 0:
                ratio = Fraction(row["lifted_work"], row["actual_finished_prize"])
                if best is None or ratio < best[0]:
                    best = ratio, {"selected_rows": list(rows), **row}
    return {"polynomial_candidates_evaluated": evaluated, "best": best[1]}


def finite_validation():
    rng = random.Random(2129)
    instances = calls = candidates = ratio_iterations = 0
    for n in range(3, 9):
        for _ in range(6):
            while True:
                tests = tuple(sorted({rng.randrange(1, 1 << n) & ~1
                                      for _ in range(n + 2)} - {0}))
                instance = Instance(n, tests)
                if instance.identifying():
                    break
            instances += 1
            incumbent, _ = greedy_code(instance, instance.full)
            weights = [0] * n
            def depths(node, depth=0):
                if node.query is None:
                    weights[node.core.bit_length() - 1] = depth
                else:
                    depths(node.zero, depth + 1)
                    depths(node.one, depth + 1)
            depths(incumbent)
            families = [(), tuple(range(len(tests))),
                        tuple(sorted(range(len(tests)), key=lambda j:
                              -min(tests[j].bit_count(),
                                   n - tests[j].bit_count()))[:len(tests) // 2])]
            for rows in dict.fromkeys(families):
                data = continuation_data(instance, rows)
                for mean in sorted({item[2] for item in data.values()}):
                    ground = sum(cell for cell, item in data.items()
                                 if item[2] <= mean)
                    for cap in sorted({1, max(weights), (max(weights) + 1) // 2}):
                        calls += 1
                        solution = exhaustive_ratio_oracle(
                            instance, rows, ground, mean, weights, cap)
                        if solution is None:
                            continue
                        core, ratio, iterations = solution
                        audit_candidate(instance, rows, data, mean, core, weights, cap)
                        candidates += 1
                        ratio_iterations += iterations
    return {"instances": instances, "exhaustive_ratio_optimization_cases": calls,
            "positive_surplus_lifts_checked": candidates,
            "strict_Dinkelbach_updates": ratio_iterations}


def singleton_noise_example():
    n, core_size = 64, 56
    coordinates = [sum(((h >> j) & 1) << h for h in range(core_size))
                   for j in range(6)]
    instance = Instance(n, tuple(coordinates + [1 << h for h in range(n)]))
    rows = tuple(range(6))
    data = continuation_data(instance, rows)
    mean = Fraction(0)
    ground = sum(cell for cell, item in data.items() if item[2] <= mean)
    order = list(range(core_size, n)) + list(range(core_size))
    weights = [0] * n
    for position, h in enumerate(order):
        weights[h] = min(position + 1, n - 1)
    cap = max(weights)
    selected = audit_candidate(instance, rows, data, mean, ground, weights, cap)
    g = selected_rank(instance, rows, ground)
    assert selected["surplus"] > 2 * n * g
    assert selected["positive_profit"] > 0
    assert instance.rank(instance.full) == n
    result = {"n": n, "all_row_rank": n, "incumbent_raw_cost": sum(weights),
              "selected_coordinate_rows": len(rows), **selected}
    result["polynomial_menu"] = candidate_menu(instance, weights)
    return result


def structured_strict_ratio_updates():
    """Exact finite flat-based oracle, validating genuine ratio improvements."""
    n, core_size = 32, 24
    coordinates = [sum(((h >> j) & 1) << h for h in range(core_size))
                   for j in range(5)]
    instance = Instance(n, tuple(coordinates + [1 << h for h in range(n)]))
    rows = tuple(range(5)) + tuple(5 + h for h in range(core_size, n))
    data = continuation_data(instance, rows)
    assert all(item[2] == 0 for item in data.values())
    columns = [1 + (h << 1) for h in range(core_size)]
    spans, frontier = {1}, [1]
    while frontier:
        span = frontier.pop()
        values = [x for x in range(64) if span & (1 << x)]
        for vector in columns:
            if span & (1 << vector):
                continue
            enlarged = span
            for value in values:
                enlarged |= 1 << (value ^ vector)
            if enlarged not in spans:
                spans.add(enlarged)
                frontier.append(enlarged)
    closures = []
    for span in spans:
        cell = sum(1 << h for h, vector in enumerate(columns)
                   if span & (1 << vector))
        rank = span.bit_count().bit_length() - 1
        closures.append((cell, rank))
    order = list(range(core_size, n)) + list(range(core_size))
    weights = [0] * n
    for position, h in enumerate(order):
        weights[h] = min(position + 1, n - 1)
    cap = n - 1
    modular = [cap + weight for weight in weights]
    rank_full = selected_rank(instance, rows, instance.full)
    ratio = Fraction(sum(weights), rank_full)
    core, updates = instance.full, 0
    while True:
        # Every outsider column adds an independent dimension. For a fixed
        # core flat, its best subset is exactly the positive marginal set.
        outside = sum(1 << h for h in range(core_size, n)
                      if modular[h] > ratio)
        outside_rank = outside.bit_count()
        outside_value = sum(modular[h] for h in range(core_size, n)
                            if outside & (1 << h)) - ratio * outside_rank
        chosen, rank = max(closures, key=lambda item:
            sum(modular[h] for h in range(core_size)
                if item[0] & (1 << h)) - ratio * item[1])
        maximum = (sum(modular[h] for h in range(core_size)
                       if chosen & (1 << h)) - ratio * rank + outside_value)
        if maximum <= cap * n:
            assert maximum == cap * n
            break
        candidate = chosen | outside
        new_ratio = Fraction(surplus(candidate, weights, cap, n),
                             rank + outside_rank)
        assert new_ratio > ratio
        core, ratio = candidate, new_ratio
        updates += 1
    assert core == (1 << core_size) - 1
    assert updates >= 2
    audited = audit_candidate(instance, rows, data, Fraction(0),
                              core, weights, cap)
    return {"n": n, "generated_core_spans_checked": len(spans),
            "initial_ratio": str(Fraction(sum(weights), rank_full)),
            "optimal_ratio": str(ratio), "strict_updates": updates, **audited}


def main():
    result = {"status": "passed", "small_oracle_enumeration_is_validation_only": True,
              "finite_validation": finite_validation(),
              "structured_strict_ratio_updates": structured_strict_ratio_updates(),
              "singleton_noise_example": singleton_noise_example()}
    output = Path(__file__).with_name("research-general-core-synthesis-results.json")
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
