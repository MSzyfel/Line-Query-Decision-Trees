"""Finite audit of the causal-action entropy relaxation and its affine gap.

Uses no numerical optimizer: checks actual-policy projections and explicit
fractional feasible channels. All pair/no-repeat tests are rational.
"""
from fractions import Fraction
from functools import lru_cache
from itertools import product, combinations
from math import ceil, log2
import random


def h2(p):
    return (-p * log2(p) if p else 0) - ((1-p) * log2(1-p) if p < 1 else 0)


def field_rank(rows, prime):
    if not rows:
        return 0
    matrix = [list(row) for row in rows]
    pivot = 0
    for column in range(len(matrix[0])):
        found = next((i for i in range(pivot, len(matrix))
                      if matrix[i][column] % prime), None)
        if found is None:
            continue
        matrix[pivot], matrix[found] = matrix[found], matrix[pivot]
        inverse = pow(matrix[pivot][column] % prime, -1, prime)
        matrix[pivot] = [(x * inverse) % prime for x in matrix[pivot]]
        for i in range(len(matrix)):
            if i != pivot:
                multiple = matrix[i][column] % prime
                matrix[i] = [(x - multiple * y) % prime
                             for x, y in zip(matrix[i], matrix[pivot])]
        pivot += 1
        if pivot == len(matrix):
            break
    return pivot


def certify_flat_columns(vectors, caps, prime):
    """Verify a nonloop represented-matroid flat for every oriented cap."""
    assert all(any(x % prime for x in row) for row in vectors)
    full_rank = field_rank(vectors, prime)
    for cap in caps:
        positive = [row for h, row in enumerate(vectors) if cap >> h & 1]
        cap_rank = field_rank(positive, prime)
        for h, row in enumerate(vectors):
            if not cap >> h & 1:
                if field_rank(positive + [row], prime) == cap_rank:
                    raise ValueError("Oriented support is not a represented flat")
    return full_rank - 1


def audit_flat_rank_drop(vectors, caps, prime):
    n = len(vectors)
    budget = certify_flat_columns(vectors, caps, prime)

    @lru_cache(None)
    def rank(state):
        return field_rank([row for h, row in enumerate(vectors)
                           if state >> h & 1], prime)

    @lru_cache(None)
    def maximum_positive_path(state):
        if state.bit_count() <= 1:
            return 0
        possibilities = []
        for cap in caps:
            hit = cap & state
            miss = state ^ hit
            if hit and miss:
                assert rank(hit) < rank(state)
                assert rank(miss) <= rank(state)
                possibilities += [1 + maximum_positive_path(hit),
                                  maximum_positive_path(miss)]
        return max(possibilities)

    maximum = maximum_positive_path((1 << n) - 1)
    assert maximum <= budget
    return budget, maximum


def flat_certificate_checks():
    rng = random.Random(261018)
    checked = 0
    for n in range(3, 10):
        # Rational-normal-curve points: any three columns are independent.
        vectors = [(1, h, h*h % 11) for h in range(n)]
        allcaps = [sum(1 << x for x in group)
                   for size in (1, 2) for group in combinations(range(n), size)]
        for _ in range(10):
            caps = tuple(cap for cap in allcaps if rng.random() < 0.25)
            if not caps or len({tuple(bool(cap >> h & 1) for cap in caps)
                                for h in range(n)}) < n:
                continue
            assert audit_flat_rank_drop(vectors, caps, 11)[0] == 2
            checked += 1
    # Three parallel columns cannot certify a proper singleton flat.
    try:
        certify_flat_columns([(1,), (1,), (1,)], (1,), 3)
    except ValueError:
        pass
    else:
        raise AssertionError("Nonflat support accepted")
    return checked


def statistics(matrix, caps, stop=None):
    n, m = len(matrix), len(caps)
    stop = [0] * n if stop is None else stop
    marginals = [sum(row[q] for row in matrix) / n for q in range(m)]
    information = sum(float(stop[h]) * log2(n) / n for h in range(n))
    for h, row in enumerate(matrix):
        for q, x in enumerate(row):
            if x:
                information += float(x) * log2(float(x) / marginals[q]) / n
    entropy = 0
    for q, p in enumerate(marginals):
        if p:
            positive = sum(matrix[h][q] for h in range(n) if caps[q] >> h & 1) / n
            entropy += float(p) * h2(float(positive / p))
    return information, entropy


def actual_policy_checks():
    rng = random.Random(11385)
    checked = 0
    for n in range(3, 10):
        allcaps = list(range(1, (1 << n) - 1))
        for _ in range(18):
            caps = tuple(rng.sample(allcaps, min(12, len(allcaps))))
            if len({tuple(bool(cap >> h & 1) for cap in caps) for h in range(n)}) < n:
                continue

            @lru_cache(None)
            def exact(state):
                if state.bit_count() <= 1:
                    return 0, None
                opts = []
                for q, cap in enumerate(caps):
                    a = state & cap
                    if a and a != state:
                        opts.append((exact(a)[0] + exact(state ^ a)[0], q))
                cost, q = min(opts)
                return state.bit_count() + cost, q

            paths = [[] for _ in range(n)]

            def fill(state, prefix):
                _, q = exact(state)
                if q is None:
                    h = state.bit_length() - 1
                    paths[h] = prefix
                    return
                hit = state & caps[q]
                fill(hit, prefix + [q])
                fill(state ^ hit, prefix + [q])

            fill((1 << n) - 1, [])
            budget = 0
            for t in range(n):
                matrix = [[0] * len(caps) for _ in range(n)]
                stop = [int(t >= len(path)) for path in paths]
                for h, path in enumerate(paths):
                    if t < len(path):
                        matrix[h][path[t]] = 1
                info, gain = statistics(matrix, caps, stop)
                assert info <= budget + 1e-9, (n, t, info, budget)
                budget += gain
            assert budget + 1e-9 >= log2(n)
            assert sum(map(len, paths)) == exact((1 << n) - 1)[0]
            assert all(len(path) == len(set(path)) for path in paths)
            checked += 1
    return checked


def certify_finite_predictor(n, caps, predictions, transitions, initial=0):
    """Polynomial verifier: longest mistake path for each possible target.

    predictions[state][query] is a bit; transitions[state][query][answer]
    is a new state. Repeated queries are allowed by the certificate.
    Bellman--Ford on nonnegative mistake weights detects positive cycles.
    """
    states = len(predictions)
    worst = 0
    for h in range(n):
        distance = [-1] * states
        distance[initial] = 0
        for step in range(states):
            updated = distance[:]
            for state, value in enumerate(distance):
                if value < 0:
                    continue
                for query, cap in enumerate(caps):
                    answer = (cap >> h) & 1
                    successor = transitions[state][query][answer]
                    value2 = value + (predictions[state][query] != answer)
                    updated[successor] = max(updated[successor], value2)
            if updated == distance:
                break
            if step == states-1:
                raise ValueError("Reachable positive-mistake cycle")
            distance = updated
        worst = max(worst, max(distance))
    return worst


def finite_predictor_checks():
    rng = random.Random(20191018)
    checked = 0
    for n in range(3, 13):
        allcaps = [sum(1 << x for x in group)
                   for size in (1, 2) for group in combinations(range(1, n), size)]
        for _ in range(14):
            caps = tuple(cap for cap in allcaps if rng.random() < 0.25)
            if not caps or len({tuple(bool(cap >> h & 1) for cap in caps)
                                for h in range(n)}) < n:
                continue
            # Unknown state first, then all singleton and positive-cap states.
            live_sets = [None] + sorted(set(caps) | {1 << h for h in range(n)})
            index = {mask: i for i, mask in enumerate(live_sets)}
            predictions, transitions = [], []
            for mask in live_sets:
                p, delta = [], []
                for cap in caps:
                    if mask is None:
                        p.append(0)
                        delta.append([0, index[cap]])
                    else:
                        hit = mask & cap
                        p.append(int(hit.bit_count() * 2 > mask.bit_count()))
                        delta.append([index[mask ^ hit] if mask ^ hit else 0,
                                      index[hit] if hit else 0])
                predictions.append(p)
                transitions.append(delta)
            d = certify_finite_predictor(n, caps, predictions, transitions)
            assert d <= 2
            checked += 1
    # A deliberately broken one-state predictor must be rejected.
    try:
        certify_finite_predictor(2, (2,), [[0]], [[[0, 0]]])
    except ValueError:
        pass
    else:
        raise AssertionError("Positive-mistake cycle was accepted")
    return checked


def affine_checks(q, dim):
    hypotheses = list(product(range(q), repeat=dim))
    n = len(hypotheses)
    directions = []
    for normal in hypotheses[1:]:
        leading = next(x for x in normal if x)
        if leading == 1:
            directions.append(normal)
    assert len(directions) == (n-1) // (q-1)
    caps = []
    for normal in directions:
        for offset in range(q):
            caps.append(sum(1 << h for h, point in enumerate(hypotheses)
                            if sum(a*b for a, b in zip(normal, point)) % q == offset))
    m, dcount = len(caps), len(directions)
    uniform = [[Fraction(1, m)] * m for _ in range(n)]
    biased = [[Fraction(1, 2*dcount) if cap >> h & 1
               else Fraction(1, 2*(q-1)*dcount) for cap in caps]
              for h in range(n)]
    assert all(sum(row) == 1 for row in biased)
    info0, entropy0 = statistics(uniform, caps)
    info1, entropy1 = statistics(biased, caps)
    expected_info = log2(q) - 1 - log2(q-1)/2
    assert abs(info0) < 1e-9
    assert abs(entropy0 - h2(1/q)) < 1e-9
    assert abs(info1 - expected_info) < 1e-9
    assert abs(entropy1 - 1) < 1e-9
    biased_steps = ceil(log2(n))
    budget = 0
    for info, gain, count in [(info0, entropy0, q), (info1, entropy1, biased_steps)]:
        for _ in range(count):
            assert info <= budget + 1e-9
            budget += gain
    assert log2(n) <= budget + 1e-9  # correctly labelled final-stop action
    assert q + biased_steps <= n-1
    assert Fraction(q, m) + Fraction(biased_steps, 2*dcount) <= 1
    pair_demands = []
    for u, v in combinations(range(n), 2):
        separating = sum(((cap >> u) ^ (cap >> v)) & 1 for cap in caps)
        assert separating == 2*n // q
        mass = Fraction(q * separating, m)
        assert mass >= 1
        pair_demands.append(mass)
    flat_budget = certify_flat_columns([(1,) + point for point in hypotheses], caps, q)
    assert flat_budget == dim
    if n <= 9:
        assert audit_flat_rank_drop([(1,) + point for point in hypotheses], caps, q)[0] == dim
    positive_mass = Fraction(1) + Fraction(biased_steps, 2)
    return {"Q": q, "dimension": dim, "n": n, "tests": m,
            "relaxed_cost": q + biased_steps,
            "biased_action_information": round(info1, 8),
            "biased_answer_entropy": round(entropy1, 8),
            "minimum_pair_cover": str(min(pair_demands)),
            "max_per_test_repeat_mass": str(Fraction(q, m) + Fraction(biased_steps, 2*dcount)),
            "verified_flat_positive_budget": flat_budget,
            "fractional_positive_mass": str(positive_mass),
            "rank_budget_rejects_channel": positive_mass > flat_budget}


if __name__ == "__main__":
    checked = actual_policy_checks()
    print(f"PASS: causal-action constraints on {checked} exact optimal-policy projections")
    print(f"PASS: {finite_predictor_checks()} finite-state pair-cap predictor certificates")
    print(f"PASS: {flat_certificate_checks()} represented-flat certificates/rank-drop audits")
    for q, dim in [(2, 3), (2, 4), (3, 2), (3, 3), (5, 2), (5, 3)]:
        print("PASS:", affine_checks(q, dim))
