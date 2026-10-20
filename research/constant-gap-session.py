"""Exact checks for a uniform shallow-convex-cap PTAS.

The full adaptive Bellman oracle is independent of the block count DP.
Only supplied singleton and cyclic-interval tests are used.
"""
from collections import Counter
from functools import lru_cache
from random import Random


def raw_optimum(points, caps, witness=True):
    """Uniform raw cost on the given point labels and an optional miss witness."""
    masks = tuple(sorted({sum(1 << j for j, p in enumerate(points) if cap >> p & 1)
                          for cap in caps}))
    n = len(points) + witness

    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        candidates = [solve(state & cap) + solve(state & ~cap)
                      for cap in masks if state & cap and state & ~cap]
        assert candidates, (points, masks, state)
        return state.bit_count() + min(candidates)

    return solve((1 << n) - 1)


def gap_decomposition(n, b, length):
    """Delete b-point gaps at the starts of length-sized cyclic blocks."""
    deleted, blocks = [], []
    for start in range(0, n, length):
        part = list(range(start, min(start + length, n)))
        deleted.extend(part[:b])
        if part[b:]:
            blocks.append(tuple(part[b:]))
    return deleted, blocks


def count_dp(blocks, caps):
    """Exact raw identification cost of independent blocks plus miss witness."""
    families = []
    for block in blocks:
        family = tuple(sorted({sum(1 << j for j, p in enumerate(block) if cap >> p & 1)
                               for cap in caps} - {0}))
        families.append((len(block), family))
    type_keys = tuple(sorted(set(families)))
    type_index = {key: i for i, key in enumerate(type_keys)}
    states = tuple((i, state)
                   for i, (size, _) in enumerate(type_keys)
                   for state in range(1, 1 << size))
    state_index = {key: i for i, key in enumerate(states)}
    initial = Counter(state_index[(type_index[family], (1 << family[0]) - 1)]
                      for family in families)
    counts = tuple(initial[i] for i in range(len(states)))

    @lru_cache(None)
    def local(typ, state):
        if state.bit_count() <= 1:
            return 0
        family = type_keys[typ][1]
        return state.bit_count() + min(local(typ, state & cap)
                                       + local(typ, state & ~cap)
                                       for cap in family
                                       if state & cap and state & ~cap)

    @lru_cache(None)
    def solve(counts):
        weight = 1 + sum(count * states[i][1].bit_count()
                         for i, count in enumerate(counts))
        if weight == 1:
            return 0
        choices = []
        for i, count in enumerate(counts):
            if not count:
                continue
            typ, state = states[i]
            for cap in type_keys[typ][1]:
                hit = state & cap
                if not hit:
                    continue
                after = list(counts)
                after[i] -= 1
                rest = state & ~cap
                if rest:
                    after[state_index[(typ, rest)]] += 1
                choices.append(local(typ, hit) + solve(tuple(after)))
        return weight + min(choices)

    return solve(counts)


def interval_caps(n, b):
    return tuple(sorted({sum(1 << ((start + j) % n) for j in range(size))
                         for start in range(n) for size in range(1, min(b, n) + 1)}))


def assert_local_intervals(blocks, caps, b):
    """Audit the sharper bound of at most b*L local masks per block."""
    for block in blocks:
        for cap in caps:
            selected = [j for j, point in enumerate(block) if cap >> point & 1]
            assert len(selected) <= b
            if selected:
                assert selected[-1] - selected[0] + 1 == len(selected)


def run_checks():
    rng = Random(13102026)
    checked = 0
    block_checks = 0
    for n in range(4, 13):
        for b in range(1, min(n, 4) + 1):
            full = interval_caps(n, b)
            singleton = {1 << p for p in range(n)}
            for repetition in range(5):
                caps = tuple(sorted(singleton | {cap for cap in full
                                                 if rng.random() < 0.4}))
                optimum = raw_optimum(tuple(range(n)), caps)
                assert 2 * b * optimum >= n * (n + 1)
                for length in range(max(2 * b, 3), n + 1):
                    deleted, blocks = gap_decomposition(n, b, length)
                    retained = tuple(p for block in blocks for p in block)
                    for cap in caps:
                        touched = sum(any(cap >> p & 1 for p in block) for block in blocks)
                        assert touched <= 1, (n, b, length, cap, blocks)
                    assert_local_intervals(blocks, caps, b)
                    exact_reduced = raw_optimum(retained, caps)
                    block_value = count_dp(blocks, caps)
                    assert block_value == exact_reduced
                    assert block_value <= optimum
                    r = len(deleted)
                    feasible_cost = block_value + r * (n - r + 1) + r * (r + 1) // 2
                    assert feasible_cost <= optimum + r * (n + 1)
                    assert r * length <= 2 * b * n
                    assert (feasible_cost - optimum) * length <= 4 * b * b * optimum
                    block_checks += 1
                checked += 1
    print(f"{checked} independent full adaptive instances checked;")
    print(f"{block_checks} deletions: exact block DP, geometry, reconstruction and ratio passed.")

    # Repeat without a private singleton supply. The gap-clearing prefix is
    # built from ordinary supplied caps, and its hit exits use exact local DP.
    nonprivate = 0
    nonprivate_decompositions = 0
    for n in range(4, 13):
        for b in range(2, min(n, 4) + 1):
            full = interval_caps(n, b)
            for repetition in range(5):
                # Retry until the complete supplied family separates all
                # hypotheses, including the all-miss witness.
                for trial in range(1000):
                    caps = tuple(cap for cap in full if rng.random() < 0.5)
                    signatures = [tuple(bool(cap >> p & 1) for cap in caps)
                                  for p in range(n)] + [(False,) * len(caps)]
                    if len(set(signatures)) == n + 1:
                        break
                else:
                    raise AssertionError("No separating random family")
                optimum = raw_optimum(tuple(range(n)), caps)
                nonprivate += 1
                for length in range(max(2 * b, b * (b - 1)), n + 1):
                    deleted, blocks = gap_decomposition(n, b, length)
                    active = (1 << n) - 1
                    prefix_raw = 0
                    used = 0
                    for p in deleted:
                        if not (active >> p & 1):
                            continue
                        cap = next(cap for cap in caps if cap >> p & 1)
                        hit = active & cap
                        labels = tuple(j for j in range(n) if hit >> j & 1)
                        local_raw = raw_optimum(labels, caps, witness=False)
                        assert local_raw <= len(labels) * (b - 1)
                        prefix_raw += 1 + active.bit_count() + local_raw
                        active &= ~hit
                        used += 1
                    reduced_blocks = [tuple(p for p in block if active >> p & 1)
                                      for block in blocks]
                    reduced_blocks = [block for block in reduced_blocks if block]
                    assert_local_intervals(reduced_blocks, caps, b)
                    reduced_labels = tuple(p for block in reduced_blocks for p in block)
                    assert active == sum(1 << p for p in reduced_labels)
                    reduced = count_dp(reduced_blocks, caps)
                    assert reduced == raw_optimum(reduced_labels, caps)
                    r = len(deleted)
                    assert used <= r
                    assert prefix_raw <= r * (n + 1) + b * (b - 1) * r
                    feasible = prefix_raw + reduced
                    assert feasible <= optimum + 2 * r * (n + 1)
                    assert (feasible - optimum) * length <= 8 * b * b * optimum
                    nonprivate_decompositions += 1
    print(f"{nonprivate} separating families without required private tests checked;")
    print(f"{nonprivate_decompositions} ordinary-cap prefixes: exact continuation and 8b^2/L ratio passed.")


if __name__ == "__main__":
    run_checks()
