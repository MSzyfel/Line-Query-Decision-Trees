"""Weighted completion certificates from rank-limited partial codes.

All coding objects here are abstract lower bounds. No abstract partition
is silently converted into an executable original-test partial policy.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import combinations
from itertools import product
import random


INF = float("inf")


def rank_code_table(n, d):
    full = [[0, 0] + [INF] * (n-1) for _ in range(d+1)]
    for budget in range(1, d+1):
        for size in range(2, n+1):
            full[budget][size] = size + min(
                full[budget-1][a] + full[budget][size-a]
                for a in range(1, size))
    return full


def partial_code_table(n, d):
    full = rank_code_table(n, d)
    # partial[k] has k completed unit leaves and one unfinished leaf
    # of mass n-k; k=n is a complete rank-limited code instead.
    partial = {n: full[d][n]}
    for heavy in range(2, n):
        target = n-heavy
        # An unfinished cell of mass >=2 needs at least one remaining
        # mistake/positive budget, because the instance is separating.
        table = [[INF] * (target+1)] + [[0] + [INF] * target for _ in range(d)]
        for budget in range(1, d+1):
            for lights in range(1, target+1):
                left_heavy = min(
                    table[budget-1][a] + full[budget][lights-a]
                    for a in range(lights))
                right_heavy = min(
                    full[budget-1][a] + table[budget][lights-a]
                    for a in range(1, lights+1))
                table[budget][lights] = lights+heavy+min(left_heavy, right_heavy)
        partial[target] = table[d][target]
    return full, partial


def certificate_density(prizes, d):
    n = len(prizes)
    _, costs = partial_code_table(n, d)
    ordered = sorted(prizes, reverse=True)
    prefix = [0]
    for prize in ordered:
        prefix.append(prefix[-1] + prize)
    return min((Fraction(cost, prefix[k]), k, cost)
               for k, cost in costs.items())


def actual_partial_policies(caps, n):
    @lru_cache(None)
    def choices(state):
        if state.bit_count() == 1:
            return ((0, state),)
        out = {(0, 0)}
        for cap in caps:
            hit = state & cap
            miss = state ^ hit
            if not hit or not miss:
                continue
            for wa, ca in choices(hit):
                for wb, cb in choices(miss):
                    out.add((state.bit_count()+wa+wb, ca | cb))
        # Keep only the least work for each actual completion set.
        costs = {}
        for work, completed in out:
            costs[completed] = min(work, costs.get(completed, INF))
        return tuple((work, completed) for completed, work in costs.items())
    return choices((1 << n)-1)


def exact_positive_budget(caps, n):
    @lru_cache(None)
    def maximum(state):
        if state.bit_count() <= 1:
            return 0
        options = []
        for cap in caps:
            a = state & cap
            if a and a != state:
                options += [1 + maximum(a), maximum(state ^ a)]
        return max(options)
    return maximum((1 << n)-1)


def audit_pricing_bound():
    rng = random.Random(26101823)
    checked = 0
    for n in range(3, 8):
        allcaps = [sum(1 << h for h in subset)
                   for size in (1, 2) for subset in combinations(range(n), size)]
        for _ in range(12):
            caps = tuple(cap for cap in allcaps if rng.random() < 0.30)
            if len({tuple(bool(cap >> h & 1) for cap in caps) for h in range(n)}) != n:
                continue
            d = exact_positive_budget(caps, n)
            policies = actual_partial_policies(caps, n)
            _, lower = partial_code_table(n, d)
            for work, completed in policies:
                if completed:
                    assert completed.bit_count() in lower
                    assert lower[completed.bit_count()] <= work
            prizes = [rng.randrange(1, n) for _ in range(n)]
            bound = certificate_density(prizes, d)[0]
            actual = min(Fraction(work, sum(prizes[h] for h in range(n)
                                            if completed >> h & 1))
                         for work, completed in policies if completed)
            assert bound <= actual
            checked += 1
    return checked


def uniform_density_comparison(max_n=30):
    rows = []
    minimum = Fraction(1)
    witness = None
    for n in range(2, max_n+1):
        for d in range(1, min(6, n-1)+1):
            full, partial = partial_code_table(n, d)
            density, k = min((Fraction(work, k), k) for k, work in partial.items())
            reference = Fraction(full[d][n], n)
            ratio = density/reference
            if ratio < minimum:
                minimum, witness = ratio, (n, d, k)
    return minimum, witness


def activation_completion_ledger(gate_sizes, bits):
    gates = list(product(*(range(c) for c in gate_sizes)))
    rows = range(1 << bits)
    hypotheses = [(gate, row) for gate in gates for row in rows]
    n = len(hypotheses)
    tests = []
    # All selector prefixes, and core bits at every gating level.
    for length in range(1, len(gate_sizes)+1):
        for prefix in product(*(range(c) for c in gate_sizes[:length])):
            tests.append(sum(1 << h for h, (gate, row) in enumerate(hypotheses)
                             if gate[:length] == prefix))
    for length in range(len(gate_sizes)+1):
        for prefix in product(*(range(c) for c in gate_sizes[:length])):
            for bit in range(bits):
                tests.append(sum(1 << h for h, (gate, row) in enumerate(hypotheses)
                                 if gate[:length] == prefix and row >> bit & 1))
    # Arbitrary ungated row distractors preserve the same pair ledger.
    for cutoff in range(1, 1 << bits):
        tests.append(sum(1 << h for h, (_, row) in enumerate(hypotheses)
                         if row < cutoff))
    resources = [sum(1 << h for h, (gate, _) in enumerate(hypotheses) if gate == g)
                 for g in gates]
    edges = [(u, v) for u, v in combinations(range(n), 2)
             if hypotheses[u][1] == hypotheses[v][1]
             and sum(a != b for a, b in zip(hypotheses[u][0], hypotheses[v][0])) == 1]
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    for cap in tests:
        charge = [0] * n
        for resource in resources:
            hit = resource & cap
            if hit and hit != resource:
                for h in range(n):
                    if resource >> h & 1:
                        charge[h] += 1
        for u, v in edges:
            if ((cap >> u) ^ (cap >> v)) & 1:
                outside = v if cap >> u & 1 else u
                charge[outside] += 1
        assert max(charge) <= 1
    prices = [Fraction(bits) + Fraction(d, 2) for d in degree]
    depths = [bits + sum(min(value+1, c-1) for value, c in zip(gate, gate_sizes))
              for gate, _ in hypotheses]
    assert all(Fraction(w, 2) <= y for w, y in zip(depths, prices))
    return {"gates": gate_sizes, "bits": bits, "n": n,
            "tests": len(tests), "resources": len(resources), "pairs": len(edges),
            "uniform_completion_price": str(prices[0]),
            "maximum_incumbent_depth": max(depths), "certified_alpha": 2}


def affine_completion_ledger(q, dim):
    hypotheses = list(product(range(q), repeat=dim))
    price = Fraction(q*dim, 3)
    depths = [sum(min(value+1, q-1) for value in h) for h in hypotheses]
    assert all(Fraction(w, 3) <= price for w in depths)
    return {"Q": q, "dimension": dim, "n": len(hypotheses),
            "uniform_completion_price": str(price),
            "maximum_incumbent_depth": max(depths), "certified_alpha": 3}


if __name__ == "__main__":
    print("PASS: exact partial-policy lower-density checks:", audit_pricing_bound())
    print("Small n<=30 comparison (not an asymptotic theorem):", uniform_density_comparison())
    for gates, bits in [((3,), 2), ((2, 3), 2), ((2, 2, 2), 1), ((2, 2, 2, 2), 1)]:
        print("PASS: global activation/prize ledger:", activation_completion_ledger(gates, bits))
    for q, dim in [(3, 2), (5, 3), (7, 2)]:
        print("PASS: affine completion-price dominance:", affine_completion_ledger(q, dim))
    for n, d in [(64, 2), (128, 2), (256, 2)]:
        full, partial = partial_code_table(n, d)
        value, k = min((Fraction(work, k), k) for k, work in partial.items())
        print("Rank-only pricing gap:", {"n": n, "d": d, "price": str(value),
                                         "completed": k, "full_mean": str(Fraction(full[d][n], n))})
