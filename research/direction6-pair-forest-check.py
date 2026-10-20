"""Exact small-instance checks for the weighted pair-forest EPTAS proof.

No external dependencies. This verifies the relaxation/rounding identities;
the standard convex-QP optimization step is not implemented here.
"""
from fractions import Fraction as F
from itertools import product
from random import Random


def matchings(vertices, edges):
    vertices = tuple(vertices)
    if not vertices:
        yield ()
        return
    u, rest = vertices[0], vertices[1:]
    for m in matchings(rest, edges):
        yield m
    for v in rest:
        e = tuple(sorted((u, v)))
        if e in edges:
            for m in matchings(tuple(x for x in rest if x != v), edges):
                yield (e,) + m


def groups(vertices, weights, matching):
    used = {v for e in matching for v in e}
    answer = [((v,), weights[v]) for v in vertices if v not in used]
    answer += [(e, sum(weights[v] for v in e)) for e in matching]
    return sorted(answer, key=lambda x: -x[1])


def schedule_cost(gs, weights, w0):
    return (w0 * len(gs) + sum((i + 1) * mass for i, (_, mass) in enumerate(gs))
            + sum(mass for vs, mass in gs if len(vs) == 2))


def invoice(vertices, weights, w0, matching):
    return schedule_cost(groups(vertices, weights, matching), weights, w0)


def integral_completion(masses):
    breaks = sorted({F(0), *masses})
    value = F(0)
    for a, b in zip(breaks, breaks[1:]):
        z = sum(x >= b for x in masses)
        value += (b - a) * z * (z + 1) / 2
    return value


def components(n, edges):
    remaining = set(range(n))
    out = []
    while remaining:
        start = min(remaining)
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for a, b in edges:
                v = b if a == u else a if b == u else None
                if v is not None and v not in seen:
                    seen.add(v)
                    stack.append(v)
        remaining -= seen
        out.append(sorted(seen))
    return out


def check_splitting_and_residues(rng):
    checked = 0
    for _ in range(300):
        n = rng.randrange(2, 11)
        cyclic = rng.choice((True, False))
        edge_order = [(i, i + 1) for i in range(n - 1)]
        if cyclic:
            edge_order.append((0, n - 1))
        edges = set(edge_order)
        weights = [F(rng.randrange(1, 25), rng.randrange(1, 8)) for _ in range(n)]
        w0 = F(rng.randrange(1, 25), rng.randrange(1, 8))
        allm = list(matchings(range(n), edges))
        optimum = min(invoice(range(n), weights, w0, m) for m in allm)
        H = rng.randrange(n + 1)
        tail = sum(sorted(weights, reverse=True)[H:])
        assert tail <= 2 * optimum / (H + 1)
        K = rng.randrange(1, 6)
        residue_costs = []
        for residue in range(K):
            deleted = {e for i, e in enumerate(edge_order) if i % K == residue}
            surviving = edges - deleted
            assert max(map(len, components(n, surviving))) <= 2 * K
            residue_costs.append(min(invoice(range(n), weights, w0, m)
                                     for m in allm if not (set(m) & deleted)))
        assert min(residue_costs) <= (1 + F(1, K)) * optimum
        original = rng.choice(allm)
        gs = groups(range(n), weights, original)
        cost = schedule_cost(gs, weights, w0)
        selected = {e for e in original if rng.randrange(2)}
        out = []
        changes = F(0)
        for j, (vs, mass) in enumerate(gs):
            if vs in selected:
                a, b = sorted(vs, key=lambda v: -weights[v])
                later = w0 + sum(x for _, x in gs[j + 1:])
                changes += later - weights[a]
                out.extend([((a,), weights[a]), ((b,), weights[b])])
            else:
                out.append((vs, mass))
        assert schedule_cost(out, weights, w0) == cost + changes
        assert integral_completion([mass for _, mass in gs]) == sum(
            (i + 1) * mass for i, (_, mass) in enumerate(gs))
        checked += 1
    return checked


def moments(distributions, configurations, weights, w0):
    """Return convex Q and exact independent-rounding expectation."""
    breaks = sorted({F(0), *(mass for configs in configurations for gs in configs
                            for _, mass in gs)})
    linear = F(0)
    for probs, configs in zip(distributions, configurations):
        linear += sum(p * (w0 * len(gs) + sum(mass for vs, mass in gs if len(vs) == 2))
                      for p, gs in zip(probs, configs))
    convex, expectation = linear, linear
    for a, b in zip(breaks, breaks[1:]):
        means, variances = [], []
        for probs, configs in zip(distributions, configurations):
            counts = [sum(mass >= b for _, mass in gs) for gs in configs]
            mean = sum(p * z for p, z in zip(probs, counts))
            second = sum(p * z * z for p, z in zip(probs, counts))
            means.append(mean)
            variances.append(second - mean * mean)
        mu = sum(means)
        base = (b - a) * (mu * mu + mu) / 2
        convex += base
        expectation += base + (b - a) * sum(variances) / 2
    return convex, expectation


def check_fractional_rounding(rng):
    checked = 0
    for _ in range(200):
        sizes = [rng.randrange(1, 4) for _ in range(rng.randrange(2, 5))]
        n = sum(sizes)
        weights = [F(rng.randrange(1, 18), rng.randrange(1, 9)) for _ in range(n)]
        w0 = F(rng.randrange(1, 20), rng.randrange(1, 9))
        configurations, distributions = [], []
        start = 0
        for i, size in enumerate(sizes):
            vs = list(range(start, start + size))
            edges = {(u, u + 1) for u in vs[:-1]}
            configs = [groups(vs, weights, m) for m in matchings(vs, edges)]
            raw = [rng.randrange(1, 8) for c in configs]
            # One component fixed, others rounded independently.
            if i == 0:
                raw = [int(j == 0) for j in range(len(configs))]
            probs = [F(p, sum(raw)) for p in raw]
            configurations.append(configs)
            distributions.append(probs)
            start += size
        convex, expected = moments(distributions, configurations, weights, w0)
        enumerated = F(0)
        for choices in product(*(range(len(c)) for c in configurations)):
            probability = F(1)
            allgs = []
            for i, j in enumerate(choices):
                probability *= distributions[i][j]
                allgs.extend(configurations[i][j])
            allgs.sort(key=lambda x: -x[1])
            enumerated += probability * schedule_cost(allgs, weights, w0)
        assert enumerated == expected
        tailmass = sum(weights[sizes[0]:])
        B = max(sizes)
        assert expected <= convex + F(B, 2) * tailmass
        # Derandomize using the exact conditional moment objective.
        conditional = [list(p) for p in distributions]
        previous = expected
        for i, configs in enumerate(configurations):
            choices = []
            for j in range(len(configs)):
                trial = [list(p) for p in conditional]
                trial[i] = [F(int(k == j)) for k in range(len(configs))]
                value = moments(trial, configurations, weights, w0)[1]
                choices.append((value, j))
            value, best = min(choices)
            assert value <= previous
            conditional[i] = [F(int(k == best)) for k in range(len(configs))]
            previous = value
        assert moments(conditional, configurations, weights, w0)[0] == previous
        assert previous <= expected
        checked += 1
    return checked


if __name__ == '__main__':
    rng = Random(613991)
    print('splitting, residues, cycle size, rank integral, and tail:',
          check_splitting_and_residues(rng))
    print('fractional identity, variance bound, and deterministic rounding:',
          check_fractional_rounding(rng))
