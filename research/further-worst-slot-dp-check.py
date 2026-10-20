"""Exact interval deadline feasibility in O(poly(M,N) 3**L) time.

A schedule's spatial Cartesian tree assigns its earliest rank to the root.
This verifier compares the subset-of-ranks DP with exact subset-permutation DP.
Only Python's standard library is used.
"""
from functools import lru_cache
from random import Random


def slot_dp(m, slots, demands):
    """Return a feasible point sequence, or None. Demand is (l,r,deadline)."""
    @lru_cache(None)
    def inside(l, r):
        return tuple((a, b, d) for a, b, d in demands if l <= a <= b <= r)

    @lru_cache(None)
    def solve(l, r, mask):
        req = inside(l, r)
        if not req:
            return ()
        if not mask:
            return None
        bit = mask & -mask
        rank = bit.bit_length()
        if min(d for _, _, d in req) < rank:
            return None
        rest = mask ^ bit
        for point in range(l, r + 1):
            # Requests containing point are hit at rank. Others split spatially.
            left_need = bool(inside(l, point - 1))
            right_need = bool(inside(point + 1, r))
            if not left_need and not right_need:
                return ((rank, point),)
            # If one side is empty, assigning all remaining ranks to the other
            # side dominates every allocation to the empty side.
            if not left_need:
                right = solve(point + 1, r, rest)
                if right is not None:
                    return ((rank, point),) + right
                continue
            if not right_need:
                left = solve(l, point - 1, rest)
                if left is not None:
                    return ((rank, point),) + left
                continue
            sub = rest
            while True:
                left = solve(l, point - 1, sub)
                if left is not None:
                    right = solve(point + 1, r, rest ^ sub)
                    if right is not None:
                        return ((rank, point),) + left + right
                if not sub:
                    break
                sub = (sub - 1) & rest
        return None

    answer = solve(1, m, (1 << slots) - 1)
    if answer is None:
        return None
    # Removing unused ranks can only accelerate first hits.
    return tuple(point for _, point in sorted(answer))


def exhaustive(m, slots, demands):
    """Independent exact subset DP with no structural assumptions."""
    @lru_cache(None)
    def extend(mask):
        rank = mask.bit_count()
        unhit = [(l, r, d) for l, r, d in demands
                 if not any(mask & (1 << (p - 1)) for p in range(l, r + 1))]
        if not unhit:
            return ()
        if rank >= slots or min(d for _, _, d in unhit) <= rank:
            return None
        for p in range(1, m + 1):
            if not mask & (1 << (p - 1)):
                suffix = extend(mask | (1 << (p - 1)))
                if suffix is not None:
                    return (p,) + suffix
        return None
    return extend(0)


def valid(sequence, slots, demands):
    return sequence is not None and len(sequence) <= slots and all(
        any(l <= p <= r for p in sequence[:d]) for l, r, d in demands)


def circular_slot_dp(m, slots, demands):
    """Demand is (frozenset of one circular arc, deadline)."""
    for first in range(m):
        spatial = [(first + i) % m for i in range(1, m)]
        residual = []
        impossible = False
        for arc, deadline in demands:
            if first in arc:
                continue
            if deadline <= 1:
                impossible = True
                break
            indices = [i + 1 for i, p in enumerate(spatial) if p in arc]
            assert indices == list(range(indices[0], indices[-1] + 1))
            residual.append((indices[0], indices[-1], deadline - 1))
        if impossible:
            continue
        suffix = slot_dp(m - 1, slots - 1, residual)
        if suffix is not None:
            return (first,) + tuple(spatial[p - 1] for p in suffix)
    return None


def circular_exhaustive(m, slots, demands):
    @lru_cache(None)
    def extend(mask):
        rank = mask.bit_count()
        unhit = [(arc, d) for arc, d in demands
                 if not any(mask & (1 << p) for p in arc)]
        if not unhit:
            return ()
        if rank >= slots or min(d for _, d in unhit) <= rank:
            return None
        for p in range(m):
            if not mask & (1 << p):
                suffix = extend(mask | (1 << p))
                if suffix is not None:
                    return (p,) + suffix
        return None
    return extend(0)


def main():
    obstruction = [(1, 1, 4), (1, 2, 2), (2, 5, 2), (2, 3, 3),
                   (3, 3, 5), (3, 4, 3), (4, 5, 4), (4, 6, 1),
                   (5, 5, 5), (6, 6, 3)]
    assert slot_dp(6, 5, obstruction) is None
    assert exhaustive(6, 5, obstruction) is None
    # Relaxing every deadline by 6/5 makes this example feasible.
    relaxed = [(l, r, (6 * d) // 5) for l, r, d in obstruction]
    assert valid(slot_dp(6, 6, relaxed), 6, relaxed)
    rng = Random(20261013)
    checked = 0
    for m in range(1, 9):
        for slots in range(1, min(m, 6) + 1):
            intervals = [(l, r, d) for l in range(1, m + 1)
                         for r in range(l, m + 1) for d in range(1, slots + 1)]
            for _ in range(100):
                demands = rng.sample(intervals, rng.randrange(1, min(16, len(intervals)) + 1))
                answer = slot_dp(m, slots, demands)
                independent = exhaustive(m, slots, demands)
                assert (answer is None) == (independent is None), (m, slots, demands)
                if answer is not None:
                    assert valid(answer, slots, demands), (m, slots, demands, answer)
                checked += 1
    # Every feasible order induces its exact first-hit deadline family. These
    # dense targeted tests exercise all Cartesian tree shapes, not just noise.
    for m in range(2, 8):
        intervals = [(l, r) for l in range(1, m + 1) for r in range(l, m + 1)]
        for _ in range(100):
            order = list(range(1, m + 1))
            rng.shuffle(order)
            demands = [(l, r, next(i + 1 for i, p in enumerate(order) if l <= p <= r))
                       for l, r in intervals]
            answer = slot_dp(m, m, demands)
            assert valid(answer, m, demands)
            checked += 1
    circular_checked = 0
    for m in range(2, 8):
        for slots in range(1, min(m, 5) + 1):
            arcs = [frozenset((first + i) % m for i in range(length))
                    for first in range(m) for length in range(1, m + 1)]
            for _ in range(50):
                demands = [(rng.choice(arcs), rng.randrange(1, slots + 1))
                           for _ in range(rng.randrange(1, 15))]
                answer = circular_slot_dp(m, slots, demands)
                independent = circular_exhaustive(m, slots, demands)
                assert (answer is None) == (independent is None), (m, slots, demands)
                if answer is not None:
                    assert len(answer) <= slots
                    assert all(any(p in arc for p in answer[:d]) for arc, d in demands)
                circular_checked += 1
    print(f"Verified {checked} linear and {circular_checked} circular random/targeted instances against independent exact DPs.")
    print("Verified the known fractional-only five-slot obstruction and its six-slot repair.")
    print("Subset-of-ranks Cartesian DP: O(M^3*3^L + N*M^2) time; O(M^2*2^L) states.")


if __name__ == '__main__':
    main()
