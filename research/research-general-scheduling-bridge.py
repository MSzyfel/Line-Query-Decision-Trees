"""Exact scheduling and continuation-profile audits; no general UDT oracle."""

from fractions import Fraction
from functools import lru_cache
import random


def sidney_schedule(chains):
    positions = [0] * len(chains)
    order = []
    while any(positions[i] < len(chain) for i, chain in enumerate(chains)):
        best = None
        for i, chain in enumerate(chains):
            weight = 0
            for length, value in enumerate(chain[positions[i]:], 1):
                weight += value
                candidate = Fraction(weight, length), -i, length
                if best is None or candidate > best:
                    best = candidate
        _, negative_i, length = best
        i = -negative_i
        for _ in range(length):
            order.append((i, positions[i]))
            positions[i] += 1
    return order


def schedule_cost(chains, order):
    return sum((time + 1) * chains[i][j] for time, (i, j) in enumerate(order))


def exact_schedule_cost(chains):
    @lru_cache(None)
    def solve(positions):
        if all(positions[i] == len(chain) for i, chain in enumerate(chains)):
            return 0
        time = sum(positions)
        options = []
        for i, chain in enumerate(chains):
            if positions[i] < len(chain):
                next_positions = list(positions)
                next_positions[i] += 1
                options.append((time + 1) * chain[positions[i]] + solve(tuple(next_positions)))
        return min(options)
    return solve((0,) * len(chains))


def exact_subset_optimum(n, tests):
    @lru_cache(None)
    def solve(state):
        size = state.bit_count()
        if size <= 1:
            return 0
        return size + min(solve(state & test) + solve(state & ~test)
                          for test in tests if state & test and state & ~test)
    return solve


def main():
    rng = random.Random(20261018)
    chain_checks = 0
    for _ in range(300):
        chains = tuple(tuple(rng.randrange(1, 9) for _ in range(rng.randrange(1, 5)))
                       for _ in range(rng.randrange(1, 5)))
        order = sidney_schedule(chains)
        assert schedule_cost(chains, order) == exact_schedule_cost(chains)
        chain_checks += 1

    tests = (3, 5, 15)
    core = exact_subset_optimum(4, tests)
    @lru_cache(None)
    def profile(state):
        if not state:
            return {0: 0}
        answer = {}
        for test in tests:
            hit, miss = state & test, state & ~test
            if hit:
                for length, cost in profile(miss).items():
                    candidate = state.bit_count() + core(hit) + cost
                    if length + 1 not in answer or candidate < answer[length + 1]:
                        answer[length + 1] = candidate
        return answer
    assert profile(15) == {1: 12, 2: 10, 3: 9}

    @lru_cache(None)
    def outside_optimum(state, outside):
        size = state.bit_count() + outside
        if size <= 1:
            return 0
        candidates = []
        for test in tests:
            hit, miss = state & test, state & ~test
            if hit and (miss or outside):
                candidates.append(size + core(hit) + outside_optimum(miss, outside))
        if outside:
            candidates.append(size + outside_optimum(state, outside - 1))
        return min(candidates)
    contexts = []
    for outside in (1, 2, 3, 4, 5):
        values = [(4 + outside + core(15 & test) + outside_optimum(15 & ~test, outside), test)
                  for test in tests]
        values.append((4 + outside + outside_optimum(15, outside - 1), "outside singleton"))
        value = outside_optimum(15, outside)
        best = [test for cost, test in values if cost == value]
        contexts.append((outside, value, best))
    assert contexts[0] == (1, 12, [3, 5])
    assert contexts[2] == (3, 20, [15])

    local_path_checks = 0
    for size in range(2, 11, 2):
        core_mask, witness = (1 << size) - 1, 1 << size
        local_tests = [1 << h for h in range(size)]
        local_tests += [(1 << h) | (1 << (h + 1)) for h in range(0, size, 2)]
        local_tests += [core_mask]
        solve = exact_subset_optimum(size + 1, local_tests)
        assert solve(core_mask) == size * size // 4 + 3 * size // 2 - 2
        assert solve(core_mask | witness) == size * size // 4 + 2 * size
        seen, pending = set(), [core_mask | witness]
        while pending:
            state = pending.pop()
            if state in seen or state.bit_count() <= 1:
                continue
            seen.add(state)
            for test in local_tests:
                hit, miss = state & test, state & ~test
                if hit and miss and state.bit_count() + solve(hit) + solve(miss) == solve(state):
                    assert not hit & witness
                    assert hit.bit_count() <= 2
                    pending.append(miss)
                    local_path_checks += 1

    freezing_rows = []
    for size in (4, 8, 16, 32, 64):
        blocks = size * size
        total_core = blocks * size
        frozen = total_core * total_core // 4 + 2 * total_core
        core_cost = size * size // 4 + 3 * size // 2 - 2
        membership = size * blocks * (blocks + 1) // 2 + blocks + blocks * core_cost
        ratio = Fraction(frozen, membership)
        assert ratio >= Fraction(size, 3)
        freezing_rows.append((size, total_core + 1, str(ratio)))

    pricing_rows = []
    for small in (2, 4, 8, 16, 32, 64):
        outside = small * small
        population = outside + small + 1
        work = population + small * (small + 3) // 2
        density = Fraction(work, small + 1)
        assert density == Fraction(3 * small, 2) + 1
        isolated_lower = Fraction(outside + 1, 2) - Fraction(1, outside)
        pricing_rows.append((population, str(density), str(isolated_lower / density)))

    print("PASS exact Sidney-chain comparisons:", chain_checks)
    print("Exact core clearing profile (length -> core work):", profile(15))
    print("Uniform context reversals (outside,OPT,best roots):", contexts)
    print("PASS all locally optimal default-path transitions:", local_path_checks)
    print("Frozen-optimum gaps (block size,n,frozen/membership):", freezing_rows)
    print("Cross-project pricing gaps (n,actual density,isolated/actual lower):", pricing_rows)


if __name__ == "__main__":
    main()
