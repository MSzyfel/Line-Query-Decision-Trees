"""Exact finite checks for the common-witness shallow-cap observations.

The suffix algorithm uses an exact cover oracle.  For these small tests the
oracle is subset DP; on geometric halfplanes it is Har-Peled--Lee's algorithm.
Random abstract incidence systems test a more general combinatorial statement.
"""
from functools import lru_cache
from itertools import product
from random import Random


def separated(n, caps):
    signatures = [sum((bool(cap & (1 << v))) << j
                      for j, cap in enumerate(caps)) for v in range(n)]
    return len(set(signatures + [0])) == n + 1


def objectives(n, caps):
    @lru_cache(None)
    def height(state):
        if state.bit_count() <= 1:
            return 0
        return 1 + min(max(height(state & cap), height(state & ~cap))
                       for cap in caps if state & cap and state & ~cap)

    @lru_cache(None)
    def raw(state):
        if state.bit_count() <= 1:
            return 0
        return state.bit_count() + min(raw(state & cap) + raw(state & ~cap)
                                      for cap in caps
                                      if state & cap and state & ~cap)
    return height, raw


def cover_oracle(target, caps):
    @lru_cache(None)
    def cover(state):
        if not state:
            return 0
        least = state & -state
        choices = [cap for cap in caps if cap & least]
        if not choices:
            return 10**9
        return 1 + min(cover(state & ~cap) for cap in choices)
    return cover(target)


def suffix_optimum(n, caps, b, height):
    points = (1 << n) - 1
    minimum_cover = cover_oracle(points, caps)
    for target_depth in range(minimum_cover, minimum_cover + b):
        prefix_bound = max(0, target_depth - b + 1)
        tail_budget = target_depth - prefix_bound
        for length in range(tail_budget + 1):
            for suffix in product(caps, repeat=length):
                union = 0
                for cap in suffix:
                    union |= cap
                remaining = union
                while True:
                    state = remaining
                    feasible = True
                    for rank, cap in enumerate(suffix, 1):
                        group = state & cap
                        if not group or rank + height(group) > tail_budget:
                            feasible = False
                            break
                        state &= ~cap
                    if feasible and not state:
                        allowed = tuple(cap for cap in caps
                                        if not cap & remaining)
                        if cover_oracle(points & ~remaining, allowed) <= prefix_bound:
                            return target_depth
                    if not remaining:
                        break
                    remaining = (remaining - 1) & union
    raise AssertionError("No accepted suffix, despite additive upper bound")


def matching_size(n, caps):
    adjacent = [0] * n
    for cap in caps:
        if cap.bit_count() == 2:
            u = (cap & -cap).bit_length() - 1
            v = (cap ^ (1 << u)).bit_length() - 1
            adjacent[u] |= 1 << v
            adjacent[v] |= 1 << u

    @lru_cache(None)
    def match(state):
        if not state:
            return 0
        low = state & -state
        vertex = low.bit_length() - 1
        rest = state ^ low
        result = match(rest)
        for neighbor in range(n):
            if rest & adjacent[vertex] & (1 << neighbor):
                result = max(result, 1 + match(rest ^ (1 << neighbor)))
        return result
    return match((1 << n) - 1)


def first_cover_optimum(n, caps):
    @lru_cache(None)
    def latency(state):
        if not state:
            return 0
        return state.bit_count() + min(latency(state & ~cap)
                                       for cap in caps if state & cap)
    return latency((1 << n) - 1)


def main():
    rng = Random(4013)
    suffix_checks = matching_checks = 0
    for b in (1, 2, 3):
        for n in range(1, 9):
            all_caps = [cap for cap in range(1, 1 << n)
                        if cap.bit_count() <= b]
            for _ in range(18):
                m = min(len(all_caps), n + 3)
                caps = tuple(sorted(rng.sample(all_caps, m)))
                if not separated(n, caps):
                    continue
                height, raw = objectives(n, caps)
                full = (1 << (n + 1)) - 1
                exact_height = height(full)
                assert suffix_optimum(n, caps, b, height) == exact_height
                suffix_checks += 1
                first = first_cover_optimum(n, caps)
                exact_raw = raw(full)
                assert first <= exact_raw <= first + b * n
                if b <= 2:
                    r = matching_size(n, caps)
                    k = n - r
                    assert exact_height == max(k, r + 1) if r else exact_height == k
                    assert exact_raw == n * (n + 3) // 2 - (n - 1) * r + r * r
                    assert first == (k * (k + 1) + r * (r + 1)) // 2
                    matching_checks += 1
    print(f"PASS: {suffix_checks} exact suffix/height and uniform transfer checks")
    print(f"PASS: {matching_checks} size-at-most-two matching checks without singleton supply")


if __name__ == "__main__":
    main()
