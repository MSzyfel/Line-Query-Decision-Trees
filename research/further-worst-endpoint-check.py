"""Audit exact axis-threshold endpoint decoding with terminal tree heights."""
from functools import lru_cache
from random import Random


def rectangle_dp(points):
    # points are distinct (left endpoint, right endpoint, child-code height).
    xs = sorted({x for x, _, _ in points})
    ys = sorted({y for _, y, _ in points})
    data = [(xs.index(x), ys.index(y), h) for x, y, h in points]

    @lru_cache(None)
    def solve(lx, rx, ly, ry):
        remaining = [(x, y, h) for x, y, h in data
                     if lx <= x <= rx and ly <= y <= ry]
        if not remaining:
            return -1
        if len(remaining) == 1:
            return remaining[0][2]
        best = float('inf')
        for q in range(lx, rx):
            a = solve(lx, q, ly, ry)
            b = solve(q + 1, rx, ly, ry)
            if a >= 0 and b >= 0:
                best = min(best, 1 + max(a, b))
        for q in range(ly, ry):
            a = solve(lx, rx, ly, q)
            b = solve(lx, rx, q + 1, ry)
            if a >= 0 and b >= 0:
                best = min(best, 1 + max(a, b))
        return best
    return solve(0, len(xs) - 1, 0, len(ys) - 1)


def arbitrary_subset_dp(points):
    # Independent complete decision-tree recursion over hypothesis subsets.
    cuts = []
    for coordinate in (0, 1):
        values = sorted({p[coordinate] for p in points})
        for threshold in values[:-1]:
            cuts.append(sum(1 << i for i, p in enumerate(points)
                            if p[coordinate] <= threshold))

    @lru_cache(None)
    def solve(mask):
        if not mask & (mask - 1):
            return points[mask.bit_length() - 1][2]
        best = float('inf')
        for cut in cuts:
            a = mask & cut
            b = mask ^ a
            if a and b:
                best = min(best, 1 + max(solve(a), solve(b)))
        return best
    return solve((1 << len(points)) - 1)


def main():
    rng = Random(20261013)
    for _ in range(1200):
        width = rng.randrange(2, 6)
        height = rng.randrange(2, 6)
        pairs = [(x, y) for x in range(width) for y in range(height)]
        sample = rng.sample(pairs, rng.randrange(1, min(12, len(pairs)) + 1))
        points = [(x, y, rng.randrange(9)) for x, y in sample]
        assert rectangle_dp(points) == arbitrary_subset_dp(points), points
    cross = [(2, 2, 10), (1, 2, 0), (3, 2, 0), (2, 1, 0), (2, 3, 0)]
    assert rectangle_dp(cross) == arbitrary_subset_dp(cross) == 14
    print('Verified 1,200 weighted endpoint instances against full subset decision-tree recursion.')
    print('Verified the heavy central cross requires four endpoint queries before its height-10 continuation.')


if __name__ == '__main__':
    main()
