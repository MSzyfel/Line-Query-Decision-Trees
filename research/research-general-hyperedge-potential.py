"""Exact containment closure/density audit and affine whole-cone counts."""
from fractions import Fraction
import itertools
import json
import math
from pathlib import Path
import random


def cut(support, test):
    return bool(support & test) and bool(support & ~test)


def deficit(selected, test, edges):
    return sum((weight for support, weight in edges
                if cut(support, test) and support & selected == support), Fraction(0))


def maximum_closure(n, test, edges, price):
    active = [(support, weight) for support, weight in edges
              if weight > 0 and cut(support, test)]
    source, sink = n + len(active), n + len(active) + 1
    graph = [dict() for _ in range(sink + 1)]
    def add(u, v, capacity):
        graph[u][v] = graph[u].get(v, Fraction(0)) + capacity
        graph[v].setdefault(u, Fraction(0))
    total = sum((weight for _, weight in active), Fraction(0))
    infinite = total + n * price + 1
    for j, (support, weight) in enumerate(active):
        reward = n + j
        add(source, reward, weight)
        for h in range(n):
            if support & (1 << h):
                add(reward, h, infinite)
    for h in range(n):
        add(h, sink, price)
    flow = Fraction(0)
    while True:
        parents = {source: None}
        queue = [source]
        for u in queue:
            for v, capacity in graph[u].items():
                if capacity > 0 and v not in parents:
                    parents[v] = u
                    queue.append(v)
                    if v == sink:
                        break
            if sink in parents:
                break
        if sink not in parents:
            selected = sum(1 << h for h in range(n) if h in parents)
            value = total - flow
            assert value == deficit(selected, test, edges) - price * selected.bit_count()
            return value, selected
        v, bottleneck = sink, None
        while v != source:
            u = parents[v]
            bottleneck = graph[u][v] if bottleneck is None else min(bottleneck, graph[u][v])
            v = u
        v = sink
        while v != source:
            u = parents[v]
            graph[u][v] -= bottleneck
            graph[v][u] += bottleneck
            v = u
        flow += bottleneck


def maximum_density(n, test, edges):
    active = [(support, weight) for support, weight in edges if cut(support, test)]
    if not active or not any(weight for _, weight in active):
        return Fraction(0), 0
    denominator = math.lcm(*(weight.denominator for _, weight in active))
    high = sum((weight for _, weight in active), Fraction(0))
    low, witness, calls = Fraction(0), 0, 0
    resolution = Fraction(1, denominator * n * n)
    while high - low >= resolution:
        midpoint = (low + high) / 2
        value, selected = maximum_closure(n, test, edges, midpoint)
        calls += 1
        if value > 0:
            low, witness = midpoint, selected
        else:
            high = midpoint
    assert witness
    ratio = deficit(witness, test, edges) / witness.bit_count()
    assert low < ratio <= high
    return ratio, witness


def entropy_density(selected, test):
    if not selected:
        return 0.0
    p = (selected & test).bit_count() / selected.bit_count()
    return 0.0 if p in (0, 1) else -p * math.log2(p) - (1-p) * math.log2(1-p)


def coding_cost(size):
    if size <= 1:
        return 0
    depth = (size - 1).bit_length()
    return size * (depth + 1) - (1 << depth)


def coding_density(selected, test):
    size = selected.bit_count()
    red = (selected & test).bit_count()
    return Fraction(coding_cost(size) - coding_cost(red)
                    - coding_cost(size-red), size)


def audit_integer_profile():
    checks = 0
    for size in range(65):
        for red in range(size+1):
            delta = coding_cost(size) - coding_cost(red) - coding_cost(size-red)
            assert 0 <= delta <= size
            checks += 1
    assert coding_cost(2) == 2
    return checks


def audit_closure():
    rng = random.Random(20261021)
    closure_cases = density_cases = entropy_cases = integer_witness_cases = 0
    for n in range(2, 9):
        for _ in range(12):
            edges = []
            for _ in range(12):
                while True:
                    support = rng.randrange(1, 1 << n)
                    if support.bit_count() >= 2:
                        break
                edges.append((support, Fraction(rng.randrange(9), rng.randrange(1, 6))))
            test = rng.randrange(1, (1 << n)-1)
            price = Fraction(rng.randrange(13), 5)
            value, _ = maximum_closure(n, test, edges, price)
            brute = max(deficit(selected, test, edges) - price * selected.bit_count()
                        for selected in range(1 << n))
            assert value == brute
            closure_cases += 1
            ratio, witness = maximum_density(n, test, edges)
            exact = max(deficit(selected, test, edges) / selected.bit_count()
                        for selected in range(1, 1 << n))
            assert ratio == exact
            density_cases += 1
            beta = Fraction(rng.randrange(9), 7)
            red = test & -test
            blue_mask = ((1 << n)-1) & ~test
            blue = blue_mask & -blue_mask
            pair = red | blue
            def combined(selected):
                return (float(deficit(selected, test, edges) / selected.bit_count())
                        + float(beta) * entropy_density(selected, test))
            chosen = max(combined(pair), combined(witness) if witness else 0.0)
            optimum = max(combined(selected) for selected in range(1, 1 << n))
            assert 2 * chosen + 1e-10 >= optimum
            entropy_cases += 1
            def integer_combined(selected):
                return (deficit(selected, test, edges) / selected.bit_count()
                        + beta * coding_density(selected, test))
            integer_chosen = max(integer_combined(pair),
                                 integer_combined(witness) if witness else Fraction(0))
            integer_optimum = max(integer_combined(selected)
                                  for selected in range(1, 1 << n))
            assert 2 * integer_chosen >= integer_optimum
            integer_witness_cases += 1
    return {"exact_closure_cases": closure_cases,
            "exact_density_cases": density_cases,
            "two_witness_entropy_checks": entropy_cases,
            "exact_two_witness_integer_profile_checks": integer_witness_cases}


def affine_tests(q, dimension):
    points = list(itertools.product(range(q), repeat=dimension))
    normals = []
    for normal in itertools.product(range(q), repeat=dimension):
        first = next((entry for entry in normal if entry), None)
        if first == 1:
            normals.append(normal)
    tests = [sum(1 << h for h, point in enumerate(points)
                 if sum(a*x for a, x in zip(normal, point)) % q == offset)
             for normal in normals for offset in range(q)]
    return points, tests


def audit_affine():
    rng = random.Random(91827)
    result = []
    for q, dimension in [(2, 3), (3, 2), (5, 2)]:
        points, tests = affine_tests(q, dimension)
        n = len(points)
        expected_m = q * (n-1) // (q-1)
        expected_r = 2 * n // q
        assert len(tests) == len(set(tests)) == expected_m
        assert all(test.bit_count() == n // q for test in tests)
        for u in range(n):
            for v in range(u):
                pair = (1 << u) | (1 << v)
                assert sum(cut(pair, test) for test in tests) == expected_r
        supports = ([support for support in range(1 << n) if support.bit_count() >= 2]
                    if n <= 9 else [rng.randrange(1, 1 << n) for _ in range(500)])
        checked = 0
        for support in supports:
            if support.bit_count() >= 2:
                assert sum(cut(support, test) for test in tests) >= expected_r
                checked += 1
        result.append({"q": q, "dimension": dimension, "n": n,
                       "tests": expected_m, "pair_cut_count": expected_r,
                       "supports_checked": checked,
                       "containment_upper_raw": str(Fraction(n * expected_m, expected_r))})
    return result


def main():
    result = {"status": "passed", "exact_integer_profile_split_checks": audit_integer_profile(),
              **audit_closure(), "affine_checks": audit_affine()}
    Path(__file__).with_name("research-general-hyperedge-potential-results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
