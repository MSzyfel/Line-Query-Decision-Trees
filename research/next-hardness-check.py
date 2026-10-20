"""Exact audit of uniform clouds and quantitative reduction bounds."""
from functools import lru_cache
from itertools import product


def completion(masses):
    return sum(j * mass for j, mass in enumerate(sorted(masses, reverse=True), 1))


def weighted_forest_opt(weights, edges):
    n = len(weights) - 1
    best = None
    for mask in range(1 << len(edges)):
        used, groups, pairs, count = set(), [], 0, 0
        for e, (u, v) in enumerate(edges):
            if mask >> e & 1:
                if u in used or v in used:
                    break
                used.update((u, v))
                groups.append(weights[u] + weights[v])
                pairs += weights[u] + weights[v]
                count += 1
        else:
            groups.extend(weights[v] for v in range(1, n + 1) if v not in used)
            cost = weights[0] * (n - count) + completion(groups) + pairs
            best = cost if best is None else min(best, cost)
    return best


def cloud_caps(weights, edges):
    blocks, private, offset = [], [], 0
    for w in weights:
        blocks.append(((1 << w) - 1) << offset)
        private.extend(1 << (offset + j) for j in range(1, w))
        offset += w
    caps = private + blocks[1:] + [blocks[u] | blocks[v] for u, v in edges]
    return offset, caps


def exact_raw_uniform(n, caps):
    @lru_cache(None)
    def solve(mask):
        if mask.bit_count() <= 1:
            return 0
        splits = {mask & a for a in caps}
        splits.discard(0)
        splits.discard(mask)
        assert splits
        return mask.bit_count() + min(solve(hit) + solve(mask ^ hit) for hit in splits)
    return solve((1 << n) - 1)


checks = 0
for vertices in range(1, 5):
    weight_range = range(1, 4) if vertices <= 2 else range(1, 3)
    for weights in product(weight_range, repeat=vertices + 1):
        for edge_mask in range(1 << (vertices - 1)):
            edges = [(i, i + 1) for i in range(1, vertices)
                     if edge_mask >> (i - 1) & 1]
            size, caps = cloud_caps(weights, edges)
            expected = weighted_forest_opt(weights, edges)
            expected += sum((w - 1) * (w + 2) // 2 for w in weights)
            assert exact_raw_uniform(size, caps) == expected, (weights, edges)
            checks += 1
print(f"Exact cloud-transfer identity verified on {checks} weighted forest instances.")

# Audit integer cloud geometry, with gaps between anchors.
for weights in ((3, 2, 5, 1), (1, 4, 2, 3, 2)):
    qscale = 4 * max(weights)
    points = [(qscale * i + j, i, j)
              for i, w in enumerate(weights) for j in range(w)]
    for a in range(1, len(weights)):
        for b in (a, a + 1):
            if b >= len(weights):
                continue
            for x, cloud, _ in points:
                value = (4 * x * x - 4 * qscale * (a + b) * x
                         + qscale * qscale * (2 * a - 1) * (2 * b + 1))
                assert value != 0
                assert (value < 0) == (a <= cloud <= b)
    for target, cloud, j in points:
        if j == 0:
            continue
        for x, _, _ in points:
            value = 2 * x * x - 4 * target * x + 2 * target * target - 1
            assert value != 0
            assert (value < 0) == (x == target)
print("Explicit whole-cloud and private-query parabola geometry verified.")

# Check the algebraic constant sharpening without floating-point arithmetic.
assert 3 * 110 ** 3 < 4_000_000
assert 9 * 2000 < 1997 * 10
assert 10 * 2000 < 1997 * 11
for u in range(1, 101):
    for auxiliary in range(1, u + 1):
        assert (3 * u + auxiliary) ** 2 < 9 * u * (u + auxiliary)

# Concrete parameters verify the strengthened W threshold K < 3 sqrt(n).
for p in range(2, 21):
    for unit in range(1, 21):
        m, target = 3 * p, 3 * unit
        sizes = [unit] * m
        total = sum(sizes)
        u = 2 * total * (p - 1)
        q = (p - 1) * (4 * total + 2 * m)
        auxiliary = m + 2
        high = auxiliary + u
        connector = high + 1
        count = auxiliary + 2
        for item in sizes:
            count += 2
            for b in range(1, p):
                lam_b = auxiliary if b == 1 else auxiliary + (2 * b - 3) * total
                lam_next = auxiliary + (2 * (b + 1) - 3) * total
                window = total - target
                count += connector + auxiliary
                count += item * (lam_b + high + lam_b + window + auxiliary
                                  + lam_next + window + high + lam_next + auxiliary)
                count += connector + 2
        assert count >= u * high >= u * u
        assert q <= 3 * u and 0 < auxiliary <= u
        assert (q + auxiliary) ** 2 < 9 * count
print("Maximum-depth square-root gap bound verified on 380 parameter instances.")

# Explicit expected-depth parameters: 110^3 times population < V^3.
for p in range(2, 16):
    for unit in (1, 2, 5):
        m = 3 * p
        total, amax = m * unit, unit
        q = 2 * total * (p - 1)
        beta1 = q - total
        r = 1000 * ((p + 10) * (q + m + 1) ** 2
                    + (q * m * p + 2 * m + 1) * beta1 * amax + 1)
        vscale = 2000 * m * (r + q + m + 1)
        deltas = [[vscale * (beta1 - (beta1 if b == 1 else 2 * total * (p - b)))
                   * unit // (q + r + m - i)
                   for b in range(1, p + 1)] for i in range(1, m + 1)]
        dmax = max(max(row) for row in deltas)
        path_total = 0
        for i in range(1, m + 1):
            base = 1 + (2 * dmax + 1) * i
            length = 2 * unit * (p - 1)
            even0 = [base if j % (2 * unit) == 0 else base + (1 if j % 2 else 2) * vscale
                     for j in range(length + 1)]
            even = even0[:]
            for b in range(1, p + 1):
                even[2 * unit * (b - 1)] += deltas[i - 1][b - 1]
            odd = []
            for j in range(1, length + 1):
                b = (j - 1) // (2 * unit) + 1
                if even0[j] - even0[j - 1] == vscale:
                    odd.append((10 + 2 * b) * vscale - even0[j - 1])
                else:
                    odd.append((10 + 2 * (b + 1)) * vscale - even0[j])
            path_total += sum(even) + sum(odd)
        forest_weight = path_total + r * (vscale // 2)
        vertices = 2 * q + m + r
        witness_weight = (vertices + 1) * forest_weight + 1
        population = forest_weight + witness_weight
        assert forest_weight <= r * vscale
        assert vertices + 2 <= 2 * r
        assert 110 ** 3 * population < vscale ** 3
        assert vscale <= population
print("Uniform-E cube bound verified on 42 explicit reduction instances.")
