"""Small exact checks for the geometric prefix obstruction and edge-pair gadget."""
from functools import lru_cache
from fractions import Fraction


def families(blocks, good):
    caps = [1 << i for i in range(6 * blocks)]
    for j in range(blocks):
        intervals = [(0, 3), (4, 5)] if good else [(1, 4), (0, 2), (3, 5)]
        for a, b in intervals:
            caps.append(sum(1 << (6 * j + i) for i in range(a, b + 1)))
    return caps


def optimal_latency(n, caps):
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        return mask.bit_count() + min(solve(mask & ~a) for a in caps if a & mask)
    return solve((1 << n) - 1)


def coverage_curve(n, caps):
    distance = {0: 0}
    pending = [0]
    for mask in pending:
        for a in caps:
            nxt = mask | a
            if nxt not in distance:
                distance[nxt] = distance[mask] + 1
                pending.append(nxt)
    return [max(mask.bit_count() for mask, d in distance.items() if d <= q)
            for q in range(n + 1)]


for m in (1, 2):
    expected_good = 5 * m * m + 3 * m
    expected_bad = min(6 * m * m - 2 * m * k + 2 * k * k + 3 * m
                       for k in range(m + 1))
    good, bad = families(m, True), families(m, False)
    assert optimal_latency(6 * m, good) == expected_good
    assert optimal_latency(6 * m, bad) == expected_bad
    assert coverage_curve(6 * m, good) == coverage_curve(6 * m, bad)
    print(f"{m} blocks: F_good={expected_good}, F_bad={expected_bad}; identical coverage curves")

for m in range(1, 101):
    formula = Fraction(11, 2) * m * m + 3 * m + Fraction(m % 2, 2)
    assert min(6 * m * m - 2 * m * k + 2 * k * k + 3 * m
               for k in range(m + 1)) == formula

# Verify integer-precision interval lines on the parabola, including the witness.
for a in range(1, 12):
    for b in range(a, 12):
        for x in range(0, 14):
            sign = 4 * x * x - 4 * (a + b) * x + (2 * a - 1) * (2 * b + 1)
            assert sign != 0
            assert (sign < 0) == (a <= x <= b)

# Every graph edge can be represented by a vertical pair separated by exactly
# the two endpoint lines. This is incidence only, not a vertex-cover reduction.
vertices = range(1, 21)
centers = set()
for i in vertices:
    for j in vertices:
        if i >= j:
            continue
        ai, aj = 2 ** i, 2 ** j
        x, y = -(ai + aj), -ai * aj
        assert x not in centers
        centers.add(x)
        for k in vertices:
            ak = 2 ** k
            vals = [Fraction(y) + delta - ak * x - ak * ak
                    for delta in (Fraction(-1, 4), Fraction(1, 4))]
            assert all(v != 0 for v in vals)
            assert (vals[0] * vals[1] < 0) == (k in (i, j))
print("Interval geometry, all 100 analytic sizes, and 190 edge-pair gadgets verified.")
