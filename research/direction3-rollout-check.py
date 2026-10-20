"""Finite checks of continuation rollout; independent of planar realizability."""
from fractions import Fraction
from functools import lru_cache
import math
import random


def check(seed, n):
    rng = random.Random(seed)
    full = (1 << n) - 1
    tests = sorted(set([1 << h for h in range(n)] +
                       [rng.randrange(1, full) for _ in range(2 * n)]))
    weights = [Fraction(rng.randrange(1, 12), 10 ** rng.randrange(0, 8))
               for _ in range(n)]
    scale = sum(weights)
    weights = [x / scale for x in weights]

    @lru_cache(None)
    def mass(s):
        return sum((weights[h] for h in range(n) if s & (1 << h)), Fraction())

    def entropy(s):
        z = mass(s)
        return sum(float(weights[h]) * math.log(float(z / weights[h]))
                   for h in range(n) if s & (1 << h))

    def splits(s):
        for t in tests:
            p = s & t
            q = s ^ p
            if p and q:
                yield p, q

    @lru_cache(None)
    def opt_e(s):
        if s.bit_count() <= 1:
            return Fraction()
        return mass(s) + min(opt_e(p) + opt_e(q) for p, q in splits(s))

    @lru_cache(None)
    def opt_w(s):
        if s.bit_count() <= 1:
            return 0
        return 1 + min(max(opt_w(p), opt_w(q)) for p, q in splits(s))

    @lru_cache(None)
    def random_e(s):
        if s.bit_count() <= 1:
            return Fraction()
        p, q = rng.choice(list(splits(s)))
        return mass(s) + random_e(p) + random_e(q)

    @lru_cache(None)
    def random_w(s):
        if s.bit_count() <= 1:
            return 0
        p, q = rng.choice(list(splits(s)))
        return 1 + max(random_w(p), random_w(q))

    # Oracle filtering makes each supplied continuation obey the premise.
    # The approximation proof does not use the oracle: its actual baseline
    # is the manuscript's additive algorithm.
    @lru_cache(None)
    def base_e(s):
        candidate = random_e(s)
        return candidate if float(candidate) <= 2 * float(opt_e(s)) + 3 * entropy(s) else opt_e(s)

    @lru_cache(None)
    def rollout_e(s, k):
        if not k or s.bit_count() <= 1:
            return base_e(s)
        return min(base_e(s), mass(s) + min(rollout_e(p, k-1) + rollout_e(q, k-1)
                                          for p, q in splits(s)))

    @lru_cache(None)
    def rollout_w(s, k):
        if not k or s.bit_count() <= 1:
            return random_w(s)
        return min(random_w(s), 1 + min(max(rollout_w(p, k-1), rollout_w(q, k-1))
                                       for p, q in splits(s)))

    def frontier_e(s, k):
        if s.bit_count() <= 1:
            return Fraction(), []
        if not k:
            return Fraction(), [s]
        p, q = min(splits(s), key=lambda pq: opt_e(pq[0]) + opt_e(pq[1]))
        cp, fp = frontier_e(p, k-1)
        cq, fq = frontier_e(q, k-1)
        return mass(s) + cp + cq, fp + fq

    checks = 0
    for k in range(1, n+1):
        prefix, frontier = frontier_e(full, k)
        remainder = sum((opt_e(s) for s in frontier), Fraction())
        qmass = sum((mass(s) for s in frontier), Fraction())
        h = sum(entropy(s) for s in frontier)
        assert prefix + remainder == opt_e(full)
        assert k * qmass <= prefix <= opt_e(full)
        assert h <= float(qmass) * math.log(n) + 1e-12
        f = rollout_e(full, k)
        assert f >= opt_e(full)
        assert float(f) <= float(prefix + 2 * remainder) + 3 * h + 1e-12
        assert float(f) <= (2 + 3 * math.log(n) / k) * float(opt_e(full)) + 1e-12
        g = rollout_w(full, k)
        d = opt_w(full)
        assert d <= g
        assert g <= max(d, 2*d-k+4*math.log2(n)) + 1e-12
        if k >= d:
            assert g == d
        if not frontier:
            assert f == opt_e(full)
        checks += 1
    return checks


if __name__ == "__main__":
    total = sum(check(271828 + 97*n + case, n)
                for n in range(2, 10) for case in range(30))
    print(f"Passed {total} exact-rational rollout/frontier checks across 240 supplied-test instances.")
