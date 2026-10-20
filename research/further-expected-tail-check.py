"""Exact checks for the capped weighted-prefix Cartesian recurrence."""

from fractions import Fraction
from functools import lru_cache
from itertools import permutations
from random import Random


def linear_dp(m, demands, ranks, miss, g, labels=None):
    """demands: (lo,hi,weight,id), fixed absolute ranks and miss costs."""
    if labels is None:
        labels = tuple(range(m))

    @lru_cache(None)
    def solve(lo, hi, mask):
        inside = [a for a in demands if lo <= a[0] <= a[1] <= hi]
        answer = sum(miss[a[3]] for a in inside)
        if not inside or not mask:
            return answer
        bit = mask & -mask
        rank = ranks[bit.bit_length() - 1]
        rest = mask ^ bit
        for point in range(lo, hi + 1):
            hit = [a for a in inside if a[0] <= point <= a[1]]
            charge = sum(2 * rank * a[2] + g[a[3]][labels[point]] for a in hit)
            left_mask = rest
            while True:
                value = charge + solve(lo, point - 1, left_mask)
                value += solve(point + 1, hi, rest ^ left_mask)
                answer = min(answer, value)
                if not left_mask:
                    break
                left_mask = (left_mask - 1) & rest
        return answer

    return solve(0, m - 1, (1 << len(ranks)) - 1)


def brute(m, sets, weights, k, b, g):
    answer = sum(2 * k * w + cost for w, cost in zip(weights, b))
    for size in range(1, min(m, k) + 1):
        for order in permutations(range(m), size):
            total = 0
            for ident, (interval, w) in enumerate(zip(sets, weights)):
                first = next(((t, p) for t, p in enumerate(order, 1) if p in interval), None)
                if first is None:
                    total += 2 * k * w + b[ident]
                else:
                    t, p = first
                    total += 2 * t * w + g[ident][p]
            answer = min(answer, total)
    return answer


def circle_dp(m, sets, weights, k, b, g):
    miss = [2 * k * w + cost for w, cost in zip(weights, b)]
    answer = sum(miss)
    if k == 0:
        return answer
    for first in range(m):
        labels = tuple((first + 1 + i) % m for i in range(m - 1))
        position = {p: i for i, p in enumerate(labels)}
        remaining = []
        charge = 0
        for ident, (interval, w) in enumerate(zip(sets, weights)):
            if first in interval:
                charge += 2 * w + g[ident][first]
            else:
                places = sorted(position[p] for p in interval)
                assert places == list(range(places[0], places[-1] + 1))
                remaining.append((places[0], places[-1], w, ident))
        value = charge + linear_dp(m - 1, remaining, tuple(range(2, k + 1)), miss, g, labels)
        answer = min(answer, value)
    return answer


def check_schedules():
    rng = Random(132610)
    for circular, trials in ((False, 600), (True, 300)):
        for trial in range(trials):
            m = rng.randrange(1, 8)
            k = rng.randrange(0, min(m, 4) + 1)
            count = rng.randrange(1, 11)
            sets, bounds = [], []
            for _ in range(count):
                start = rng.randrange(m)
                if circular:
                    length = rng.randrange(1, m + 1)
                    interval = {(start + offset) % m for offset in range(length)}
                else:
                    end = rng.randrange(start, m)
                    interval = set(range(start, end + 1))
                    bounds.append((start, end))
                sets.append(interval)
            weights = [rng.randrange(1, 10) for _ in sets]
            b = [rng.randrange(0, 100) for _ in sets]
            g = [[rng.randrange(0, 35) for _ in range(m)] for _ in sets]
            exact = brute(m, sets, weights, k, b, g)
            if circular:
                dynamic = circle_dp(m, sets, weights, k, b, g)
            else:
                demands = [(lo, hi, weights[i], i) for i, (lo, hi) in enumerate(bounds)]
                miss = [2 * k * w + cost for w, cost in zip(weights, b)]
                dynamic = linear_dp(m, demands, tuple(range(1, k + 1)), miss, g)
            assert dynamic == exact, (circular, trial, m, k, dynamic, exact)
        print(f"PASS {trials} {'circular' if circular else 'linear'} exact weighted-prefix instances")


def check_tail_family():
    delta = Fraction(144136826, 10**9)
    r = 8
    for power in (14, 20, 26, 32):
        n = 2**power
        nonzero = n - 1
        middle = 2 ** (power // 2)
        eta = Fraction(1, n**3)
        head_each = (1 - Fraction(1, middle) - eta) / r
        middle_each = Fraction(1, middle**2)
        tail_each = eta / (nonzero - r - middle + 1)
        assert delta > head_each > middle_each > tail_each > 0
        head_cost = head_each * r * (r + 1) / 2
        middle_cost = middle_each * (middle * r + middle * (middle + 1) // 2)
        tail_first = r + middle + 1
        tail_sum = (nonzero * (nonzero + 1) - (tail_first - 1) * tail_first) // 2
        exact = head_cost + middle_cost + tail_each * (tail_sum + nonzero)
        bound = Fraction(r + 1, 2) + Fraction(1, 2) + Fraction(2 * r + 1, 2 * middle) + Fraction(1, n**2)
        assert exact <= bound < 6
        k = 2 * power
        residual = Fraction(middle - 2 * k, middle**2)
        assert residual > 0
        charged = nonzero * residual
        assert charged > Fraction(middle, 2)
        print(f"n=2^{power}: OPT_E<={float(bound):.9f}; uniform-height tail charge>={float(charged):.6f}")


if __name__ == "__main__":
    check_schedules()
    check_tail_family()
