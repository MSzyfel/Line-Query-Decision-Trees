"""Independent finite checks for the general-cap research note.

No external packages.  Exact full adaptive Bellman optimization is compared
with two smaller recurrences: the graph-incidence invoice and a block-count
quotient after an actual legal clearing prefix.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import random


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit
        mask -= bit


def separated(n, caps):
    return len({tuple(bool(cap & (1 << i)) for cap in caps)
                for i in range(n)}) == n


def bellman(caps):
    @lru_cache(None)
    def raw(state):
        if state.bit_count() <= 1:
            return 0
        options = []
        for cap in caps:
            hit = state & cap
            miss = state ^ hit
            if hit and miss:
                options.append(raw(hit) + raw(miss))
        if not options:
            raise ValueError("Nonseparating supplied family")
        return state.bit_count() + min(options)
    return raw


def incidence_checks():
    checked = 0
    for v in range(2, 6):
        edges = list(combinations(range(v), 2))
        for family in range(1, 1 << len(edges)):
            chosen = [edge for i, edge in enumerate(edges) if family >> i & 1]
            degrees = [sum(x in edge for edge in chosen) for x in range(v)]
            if max(degrees) > 3 or min(degrees) == 0:
                continue
            # Bit zero is the all-miss witness.  Edges are hypotheses.
            caps = tuple(sum(1 << (i + 1) for i, edge in enumerate(chosen)
                             if x in edge) for x in range(v))
            n = len(chosen)
            full = (1 << (n + 1)) - 1
            target_edges = full ^ 1
            optimum = bellman(caps)(full)

            @lru_cache(None)
            def latency(state):
                if not state:
                    return 0
                return state.bit_count() + min(
                    latency(state ^ (state & cap))
                    for cap in caps if state & cap)

            @lru_cache(None)
            def invoice(state):
                if not state:
                    return 0
                return state.bit_count() + 1 + min(
                    # Singleton-search cost on the positive star branch.
                    (k * (k + 1) // 2 - 1 if k else 0)
                    + invoice(state ^ hit)
                    for cap in caps if (hit := state & cap)
                    for k in [hit.bit_count()])

            lower = latency(target_edges)
            assert optimum == invoice(target_edges)
            assert lower <= optimum <= lower + (max(degrees) - 1) * n + v
            assert 2 * max(degrees) * lower >= n * (n + 1)
            checked += 1
    return checked


def components(n, caps, deleted):
    live = ((1 << n) - 1) & ~deleted & ~1
    out = []
    while live:
        comp = live & -live
        while True:
            more = comp
            for cap in caps:
                if cap & comp:
                    more |= cap & live
            if more == comp:
                break
            comp = more
        out.append(comp)
        live &= ~comp
    return out


def quotient_cost(blocks, caps):
    # Type = physical block size and its supplied local mask family.
    # The number of types is bounded for bounded block size.
    def relabel(cap, block):
        return sum(1 << j for j, bit in enumerate(bits(block)) if cap & bit)

    types = []
    initial = Counter()
    for block in blocks:
        masks = tuple(sorted({relabel(cap, block) for cap in caps
                              if cap & block}))
        typ = (block.bit_count(), masks)
        if typ not in types:
            types.append(typ)
        initial[(types.index(typ), (1 << typ[0]) - 1)] += 1
    coordinates = [(i, r) for i, (size, _) in enumerate(types)
                   for r in range(1, 1 << size)]
    coord_index = {c: i for i, c in enumerate(coordinates)}
    local = [bellman(masks) for _, masks in types]

    @lru_cache(None)
    def solve(counts):
        if not any(counts):
            return 0
        total = 1 + sum(c * mask.bit_count()
                        for c, (_, mask) in zip(counts, coordinates))
        choices = []
        for j, ((i, r), c) in enumerate(zip(coordinates, counts)):
            if not c:
                continue
            for cap in types[i][1]:
                a = cap & r
                if not a:
                    continue
                successor = list(counts)
                successor[j] -= 1
                if r ^ a:
                    successor[coord_index[(i, r ^ a)]] += 1
                choices.append(local[i](a) + solve(tuple(successor)))
        return total + min(choices)

    return solve(tuple(initial[c] for c in coordinates))


def deletion_checks():
    rng = random.Random(190611385)
    checked = no_singletons = multiple_blocks = 0
    for n in range(5, 11):
        universe = list(range(1, n))
        allcaps = [sum(1 << i for i in group)
                   for k in (1, 2, 3)
                   for group in combinations(universe, k)]
        for attempt in range(90):
            caps = tuple(cap for cap in allcaps if rng.random() < 0.12)
            if not separated(n, caps):
                continue
            d = sum(1 << i for i in universe if rng.random() < 0.3)
            raw = bellman(caps)
            full = (1 << n) - 1
            live = full
            prefix = 0
            # Query only supplied caps, including collateral removals.
            while d & live:
                x = (d & live) & -(d & live)
                cap = next(cap for cap in caps if cap & x)
                hit = cap & live
                prefix += live.bit_count() + raw(hit)
                live ^= hit
            blocks = components(n, caps, full ^ live)
            residual = quotient_cost(blocks, caps)
            assert residual == raw(live)
            optimum = raw(full)
            b = max(cap.bit_count() for cap in caps)
            r = d.bit_count()
            # Removing the actual witness produces a virtual-default system.
            # Reintroducing that hypothesis has the claimed additive cost.
            original = raw(full ^ 1)
            assert original <= optimum <= original + n
            assert 2 * b * original >= (n - 1) * (n - 2)
            assert prefix <= r * (n + b * (b - 1))
            assert residual <= optimum
            assert 2 * b * optimum >= (n - 1) * n
            # Cross-multiplied claimed approximation bound.
            assert ((prefix + residual - optimum) * (n - 1) * n
                    <= 2 * b * r * (n + b * (b - 1)) * optimum)
            checked += 1
            no_singletons += not any(cap.bit_count() == 1 for cap in caps)
            multiple_blocks += len(blocks) > 1
    return checked, no_singletons, multiple_blocks


if __name__ == "__main__":
    incidence = incidence_checks()
    deletion, no_singletons, multiple_blocks = deletion_checks()
    print(f"PASS: {incidence} separating degree-at-most-3 graph-incidence instances")
    print(f"PASS: {deletion} legal deletion/count-quotient instances")
    print(f"PASS: {deletion} virtual-default augmentation bounds")
    print(f"      {no_singletons} without supplied singletons; "
          f"{multiple_blocks} with multiple residual blocks")
