"""Small exact checks for the structural research note. No dependencies."""
from functools import lru_cache
from itertools import combinations
from math import atan2, pi
from random import Random
from fractions import Fraction
from bisect import bisect_left


def exact(tests, weights):
    n = len(weights)

    @lru_cache(None)
    def solve(s):
        if s.bit_count() <= 1:
            return 0, 0
        mass = sum(w for i, w in enumerate(weights) if s >> i & 1)
        alternatives = []
        for test in tests:
            a, b = s & test, s & ~test
            if a and b:
                wa, ea = solve(a)
                wb, eb = solve(b)
                alternatives.append((1 + max(wa, wb), mass + ea + eb))
        return min(w for w, e in alternatives), min(e for w, e in alternatives)

    return solve((1 << n) - 1)


def matching_number(n, edges):
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u

    @lru_cache(None)
    def solve(s):
        if not s:
            return 0
        u = (s & -s).bit_length() - 1
        rest = s & ~(1 << u)
        best = solve(rest)
        neighbors = adjacency[u] & rest
        while neighbors:
            bit = neighbors & -neighbors
            neighbors ^= bit
            best = max(best, 1 + solve(rest ^ bit))
        return best

    return solve((1 << n) - 1)


def alpha_cost(order, weights):
    @lru_cache(None)
    def solve(i, j):
        if j - i <= 1:
            return 0, 0
        mass = sum(weights[order[k]] for k in range(i, j))
        options = [(solve(i, k), solve(k, j)) for k in range(i + 1, j)]
        return (1 + min(max(a[0], b[0]) for a, b in options),
                mass + min(a[1] + b[1] for a, b in options))
    return solve(0, len(order))


def check_pair_formula():
    checked = 0
    for n in range(1, 6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            edges = [e for j, e in enumerate(possible) if mask >> j & 1]
            tests = [1 << (i + 1) for i in range(n)]
            tests += [(1 << (u + 1)) | (1 << (v + 1)) for u, v in edges]
            nu = matching_number(n, edges)
            want_w = max(n - nu, nu + 1) if nu else n
            # Integral weights implement distinguished masses .5, 1, 2, 10.
            for w0 in [1, 2, 4, 20]:
                got_w, got_e = exact(tests, [w0] + [2] * n)
                candidates = []
                for q in range(nu + 1):
                    r = n - q
                    candidates.append(w0*r + r*(r+1) + q*(q+1) + 4*q)
                assert got_w == want_w, (n, edges, got_w, want_w)
                assert got_e == min(candidates), (n, edges, got_e, candidates)
            checked += 1
    return checked


def check_concurrent():
    rng = Random(8137)
    checked = 0
    for _ in range(2500):
        normals = rng.sample([(1, 0), (0, 1), (1, 1), (1, -1), (2, 1), (1, 2)], 5)
        points = rng.sample([(x, y) for x in range(-5, 6) for y in range(-5, 6)
                             if x or y], rng.randint(2, 7))
        if any(a*x+b*y == 0 for a, b in normals for x, y in points):
            continue
        signs = [tuple(a*x+b*y > 0 for a, b in normals) for x, y in points]
        if len(set(signs)) != len(points):
            continue
        weights = [rng.randrange(1, 20) for p in points]
        tests = [sum(1 << i for i, (x, y) in enumerate(points) if a*x+b*y > 0)
                 for a, b in normals]
        options = []
        for (a, b), test in zip(normals, tests):
            sides = [[i for i in range(len(points)) if bool(test >> i & 1) == sign]
                     for sign in [True, False]]
            if not all(sides):
                continue
            costs = []
            for sign, side in zip([True, False], sides):
                center = atan2(b, a) + (0 if sign else pi)
                order = sorted(side, key=lambda i: (atan2(points[i][1], points[i][0])
                                                     - center + pi) % (2*pi) - pi)
                costs.append(alpha_cost(order, weights))
            options.append((1 + max(c[0] for c in costs),
                            sum(weights) + sum(c[1] for c in costs)))
        want = min(w for w, e in options), min(e for w, e in options)
        assert exact(tests, weights) == want, (points, normals, weights)
        checked += 1
    return checked


def check_group_buckets():
    rng = Random(98433)
    checked = 0
    for _ in range(2000):
        n = rng.randrange(1, 9)  # number of nonzero hypotheses
        weights = [rng.randrange(1, 11) * 10**rng.randrange(9) for i in range(n+1)]
        available = [rng.random() < .8 for i in range(n-1)]
        eta = rng.choice([Fraction(1, 10), Fraction(1, 4), Fraction(1, 100)])
        omega = sum(weights)
        tau = eta * omega / (n+1)**2
        tilde = [max(Fraction(w), tau) for w in weights[1:]]
        levels = [tau]
        while levels[-1] < 2 * omega:
            levels.append(levels[-1] * (1+eta))

        def bucket(mass):
            j = bisect_left(levels, mass)
            return j, levels[j]

        def groups(i=0):
            if i == n:
                yield []
                return
            for tail in groups(i+1):
                yield [(i,)] + tail
            if i+1 < n and available[i]:
                for tail in groups(i+2):
                    yield [(i, i+1)] + tail

        def completion(masses):
            return sum(j*x for j, x in enumerate(sorted(masses, reverse=True), 1))

        candidates = []
        histograms = {}
        for parts in groups():
            q = sum(len(p) == 2 for p in parts)
            orig_masses = [sum(weights[i+1] for i in p) for p in parts]
            tilde_masses = [sum(tilde[i] for i in p) for p in parts]
            indexed = [bucket(mass) for mass in tilde_masses]
            beta = [b for j, b in indexed]
            counts = [0] * (2*len(levels))
            for part, (j, b) in zip(parts, indexed):
                counts[j + (len(levels) if len(part) == 2 else 0)] += 1
            original = (weights[0] * (n-q) + completion(orig_masses)
                        + sum(m for p, m in zip(parts, orig_masses) if len(p) == 2))
            raised = (weights[0] * (n-q) + completion(tilde_masses)
                      + sum(m for p, m in zip(parts, tilde_masses) if len(p) == 2))
            surrogate = (weights[0] * (n-q) + completion(beta)
                         + sum(m for p, m in zip(parts, beta) if len(p) == 2))
            order = sorted(range(len(parts)), key=lambda j: beta[j], reverse=True)
            actual = (weights[0] * (n-q)
                      + sum(j*orig_masses[k] for j, k in enumerate(order, 1))
                      + sum(m for p, m in zip(parts, orig_masses) if len(p) == 2))
            assert actual <= surrogate
            assert surrogate <= (1+eta)*raised
            key = tuple(counts)
            if key in histograms:
                assert histograms[key] == surrogate
            histograms[key] = surrogate
            candidates.append((surrogate, actual, original))
        optimum = min(original for surrogate, actual, original in candidates)
        surrogate, actual, original = min(candidates)
        assert actual <= (1+eta)**2 * optimum
        checked += 1
    return checked


if __name__ == '__main__':
    print('Pair graphs checked:', check_pair_formula(), '(four priors each)')
    print('Concurrent instances checked:', check_concurrent())
    print('Weighted group-bucket forests checked:', check_group_buckets())
