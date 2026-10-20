"""Independent checks for adjacent-block quasipolynomial improvements.

Finite checks support the report's proofs; they are not a theorem proof.
Run with Python 3, without third-party dependencies.
"""

from fractions import Fraction as F
from itertools import permutations
from math import floor
import random


def log_bounds(x, terms=100):
    """Exact rational enclosure, range-reduced to [1,2]."""
    assert x >= 1
    k = 0
    while x >= 2:
        x /= 2
        k += 1

    def series(y):
        z = (y - 1) / (y + 1)
        lo = sum((2 * z ** (2 * j + 1) / (2 * j + 1)
                  for j in range(terms)), F(0))
        tail = 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1-z*z))
        return lo, lo + tail

    a, b = series(x)
    l2, u2 = series(F(2))
    return a + k*l2, b + k*u2


def certify_max(lam, delta, gamma, shifted=False):
    a = 2*lam
    l2, u2 = log_bounds(F(2))
    lb, _ = log_bounds(1/(1-delta))
    lf, _ = log_bounds(1/delta)
    assert gamma*lb > u2
    assert gamma*lf > (F(5) if shifted else a+3)*u2
    return str(a+gamma)


def grade_feasible(m, intervals):
    """Exact ordinary-interval grading feasibility, absolute ranks."""
    if not intervals:
        return True
    levels = sorted({d for l, r, d in intervals})
    grades = {d: i for i, d in enumerate(levels)}
    end = [[] for _ in range(m+1)]
    for l, r, d in intervals:
        end[r].append((l, grades[d]))
    zero = (0,)*len(levels)
    states = {(zero, zero)}
    for q in range(1, m+1):
        nxt = set()
        for p, c in states:
            for i in range(-1, len(levels)):
                pp, cc = list(p), list(c)
                if i >= 0:
                    for j in range(i, len(levels)):
                        pp[j] = q
                        cc[j] += 1
                if any(cc[j] > b for j, b in enumerate(levels)):
                    continue
                if any(pp[j] < l for l, j in end[q]):
                    continue
                nxt.add((tuple(pp), tuple(cc)))
        states = nxt
    return bool(states)


def brute_feasible(m, intervals):
    for order in permutations(range(1, m+1)):
        if all(any(l <= p <= r for p in order[:d])
               for l, r, d in intervals):
            return True
    return False


def edge_demands(vertices, positive, forced):
    """Expand a circular positive interval to incident edge candidates."""
    hits = {i for i in range(vertices)
            if i in positive or (i+1) % vertices in positive}
    if forced in hits:
        return None
    remaining = [(forced+i) % vertices for i in range(1, vertices)]
    linear = [j+1 for j, e in enumerate(remaining) if e in hits]
    assert linear == list(range(min(linear), max(linear)+1))
    return min(linear), max(linear)


def main():
    assert certify_max(F(10000001, 10000000), F(245122334, 10**9),
                       F(246496526, 10**8), shifted=True) == "223248273/50000000"
    assert F(223248273, 50000000) < F(4464966, 10**6)
    assert certify_max(F(2001, 2000), F(245122334, 10**9),
                       F(246496526, 10**8), shifted=True) == "223298263/50000000"
    print("Shifted exact certificates: 4.46496546 < 4.464966; 4.46596526 < 4.466 PASS")
    assert certify_max(F(100001, 100000), F(2451211, 10000000),
                       F(123249, 50000)) == "893/200"
    assert certify_max(F(2001, 2000), F(2451, 10000),
                       F(1233, 500)) == "4467/1000"
    print("Exact rational certificates: factors 4.465 and 4.467 PASS")

    for m in range(3, 10):
        for start in range(m):
            for size in range(1, m+1):
                positive = {(start+j) % m for j in range(size)}
                for forced in range(m):
                    edge_demands(m, positive, forced)
    print("Circular interval expansion and forced-block cut: PASS")

    rng = random.Random(20261013)
    for test in range(350):
        m = rng.randrange(2, 7)
        ds = rng.sample(range(1, m+1), min(3, m))
        intervals = []
        for _ in range(rng.randrange(1, 9)):
            l = rng.randrange(1, m+1)
            r = rng.randrange(l, m+1)
            intervals.append((l, r, rng.choice(ds)))
        assert grade_feasible(m, intervals) == brute_feasible(m, intervals)
    print("Grade DP vs all permutations on 350 small instances: PASS")

    for lam in [F(11, 10), F(101, 100), F(2001, 2000),
                F(100001, 100000)]:
        for t in range(1, 10001):
            # The two floors commute exactly at this scaling.
            assert floor(F(floor(2*lam*t), 2)) == floor(lam*t)
    print("Block budget floor identity on 40000 parameter/rank pairs: PASS")


if __name__ == "__main__":
    main()
