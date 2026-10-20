"""Independent audit of the uniform fixed-cap cyclic-interval PTAS.

The oracle optimizes arbitrary adaptive trees on physical hypotheses.
The residual solver quotients by a sorted multiset of local states,
independently of the count-vector implementation in constant-gap-session.py.
"""
from functools import lru_cache
from itertools import combinations
from random import Random


def interval_masks(n, b):
    return tuple(sorted({sum(1 << ((start + j) % n) for j in range(size))
                         for start in range(n) for size in range(1, b + 1)}))


def separates(n, masks):
    signatures = [tuple(bool(q & (1 << i)) for q in masks) for i in range(n)]
    return len(set(signatures + [(False,) * len(masks)])) == n + 1


def adaptive_oracle(masks):
    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        choices = []
        for q in masks:
            yes, no = state & q, state & ~q
            if yes and no:
                choices.append(solve(yes) + solve(no))
        assert choices, (state, masks)
        return state.bit_count() + min(choices)
    return solve


def quotient_cost(blocks, masks):
    types = []
    for block in blocks:
        family = tuple(sorted({sum(1 << j for j, physical in enumerate(block)
                                   if q & (1 << physical)) for q in masks} - {0}))
        types.append((len(block), family))
    unique = sorted(set(types))
    index = {kind: i for i, kind in enumerate(unique)}

    local = [adaptive_oracle(family) for _, family in unique]

    @lru_cache(None)
    def solve(bags):
        if not bags:
            return 0
        live = 1 + sum(state.bit_count() for _, state in bags)
        candidates = []
        for i, (kind, state) in enumerate(bags):
            if i and bags[i - 1] == bags[i]:
                continue
            for query in unique[kind][1]:
                hit = state & query
                if not hit:
                    continue
                residual = state & ~query
                updated = list(bags[:i] + bags[i + 1:])
                if residual:
                    updated.append((kind, residual))
                candidates.append(local[kind](hit) + solve(tuple(sorted(updated))))
        return live + min(candidates)

    start = tuple(sorted((index[kind], (1 << kind[0]) - 1) for kind in types))
    return solve(start)


def verify_instance(n, b, masks, length):
    assert separates(n, masks)
    deleted, initial_blocks = [], []
    for start in range(0, n, length):
        piece = list(range(start, min(n, start + length)))
        deleted.extend(piece[:b])
        if piece[b:]:
            initial_blocks.append(piece[b:])
    assert len(deleted) * length <= 2 * b * n
    for q in masks:
        assert sum(any(q & (1 << h) for h in block) for block in initial_blocks) <= 1

    oracle = adaptive_oracle(masks)
    witness = 1 << n
    live = (1 << n) - 1
    original = oracle(live | witness)
    assert 2 * b * original >= n * (n + 1)
    prefix_cost, prefix_queries = 0, 0
    for marked in deleted:
        if not (live & (1 << marked)):
            continue
        # Pick the LARGEST currently productive supplied cap. This exercises
        # collateral deletion of unmarked points without using private tests.
        available = [q for q in masks if q & (1 << marked)]
        q = max(available, key=lambda q: (live & q).bit_count())
        hit = live & q
        prefix_cost += live.bit_count() + 1 + oracle(hit)
        assert oracle(hit) <= hit.bit_count() * (b - 1)
        live &= ~hit
        prefix_queries += 1
    assert prefix_queries <= len(deleted)
    blocks = [tuple(h for h in block if live & (1 << h)) for block in initial_blocks]
    blocks = [block for block in blocks if block]
    assert live == sum(1 << h for block in blocks for h in block)
    for block in blocks:
        union = 0
        for q in masks:
            positions = [j for j, h in enumerate(block) if q & (1 << h)]
            if positions:
                assert len(positions) <= b
                assert positions[-1] - positions[0] + 1 == len(positions)
                union |= sum(1 << j for j in positions)
        # This recovers the actual block size from the padded family alone.
        assert union == (1 << len(block)) - 1
    residual = quotient_cost(blocks, masks)
    assert residual == oracle(live | witness)
    assert residual <= original
    assert prefix_cost <= len(deleted) * (n + 1 + b * (b - 1))
    if n >= b * (b - 1):
        assert prefix_cost <= 2 * len(deleted) * (n + 1)
        total = prefix_cost + residual
        assert (total - original) * length <= 8 * b * b * original
    return len(blocks)


def main():
    checked = 0
    multi_block = 0
    # Exhaust every separating family of singleton and adjacent-pair tests.
    # The singleton masks may all be absent.
    for n in range(4, 7):
        b = 2
        full = interval_masks(n, b)
        for flags in range(1 << len(full)):
            family = tuple(q for j, q in enumerate(full) if flags & (1 << j))
            if separates(n, family):
                multi_block += verify_instance(n, b, family, 4) >= 2
                checked += 1

    # Larger instances exercise repeated types and genuinely independent blocks.
    rng = Random(1301026)
    without_singletons = 0
    for n in range(8, 13):
        for b in range(2, min(4, n // 2) + 1):
            full = interval_masks(n, b)
            pair_cycle = tuple(q for q in full if q.bit_count() == 2)
            candidates = [pair_cycle]
            for _ in range(10):
                candidates.append(tuple(q for q in full if rng.random() < 0.5))
                candidates.append(tuple(q for q in full
                                        if q.bit_count() >= 2 and rng.random() < 0.7))
            for family in candidates:
                if not separates(n, family):
                    continue
                without_singletons += all(q.bit_count() > 1 for q in family)
                for length in range(max(2 * b, b * (b - 1)), n + 1):
                    multi_block += verify_instance(n, b, family, length) >= 2
                    checked += 1

    # Type bound: sum over different local universe sizes, then all residuals.
    for length in range(1, 9):
        type_count = sum(1 << ((1 << size) - 1) for size in range(1, length + 1))
        assert type_count * (1 << length) <= 1 << ((1 << length) + length)
    for length in range(1, 65):
        for b in range(1, length + 1):
            interval_count = sum(length - size + 1 for size in range(1, b + 1))
            assert interval_count <= b * length
            # Families and live subsets give 2^(interval_count+length) states.
            assert interval_count + length <= (b + 1) * length
    print(f"{checked} independently optimized decompositions passed.")
    print(f"{multi_block} retained multiple blocks; {without_singletons} families had no singleton queries.")
    print("Full adaptive oracle, multiset quotient, supplied-cap prefix, constants, ordinary masks, and sharpened type bound all passed.")


if __name__ == '__main__':
    main()
