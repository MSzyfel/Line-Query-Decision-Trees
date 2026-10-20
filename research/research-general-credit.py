"""Exact finite audits for research-general-credit.md; no third-party packages.

Enumeration here checks proofs. It is not the proposed runtime of an algorithm.
All computations use integers, with common denominator 9*r.
"""

from itertools import product


def local_cost(count):
    return (0, 0, 2, 5)[count]


def audit_triple_identity():
    for a, u, v in product((0, 1), repeat=3):
        deficit = local_cost(a + u + v) - local_cost(a) - local_cost(u + v)
        assert deficit == a * (2 * u + 2 * v - u * v)
        pair_deficit = 2 * a * (u + v)
        # Scaled replacement D_pair*(3/4) lies in [.75 D_triple,D_triple].
        assert 3 * deficit <= 3 * pair_deficit <= 4 * deficit


def graph_edges(name):
    if name == "K4":
        return 4, [(i, j) for i in range(4) for j in range(i + 1, 4)]
    if name == "K3,3":
        return 6, [(i, j) for i in range(3) for j in range(3, 6)]
    if name == "prism":
        return 6, [(0, 1), (1, 2), (0, 2), (3, 4), (4, 5), (3, 5),
                   (0, 3), (1, 4), (2, 5)]
    if name == "cube":
        return 8, [(i, i ^ (1 << b)) for i in range(8) for b in range(3)
                   if i < (i ^ (1 << b))]
    if name == "two cubes":
        _, one = graph_edges("cube")
        return 16, one + [(i + 8, j + 8) for i, j in one]
    raise ValueError(name)


def audit_graph(name, anchors):
    n, edges = graph_edges(name)
    r = anchors
    adjacency = [0] * n
    for u, v in edges:
        adjacency[u] |= 1 << v
        adjacency[v] |= 1 << u
    assert all(bits.bit_count() == 3 for bits in adjacency)

    # Coefficients are invariant under anchor permutations. For each graph
    # subset U, enumerating its anchor cardinality k covers every actual state.
    sizes = [0] * (1 << n)
    induced = [0] * (1 << n)
    cuts = [0] * (1 << n)
    for mask in range(1, 1 << n):
        low = mask & -mask
        u = low.bit_length() - 1
        rest = mask ^ low
        sizes[mask] = sizes[rest] + 1
        induced[mask] = induced[rest] + (adjacency[u] & rest).bit_count()
        cuts[mask] = 3 * sizes[mask] - 2 * induced[mask]

    def potential_numerator(k, mask):
        # Directly sums F(0)=F(1)=0, F(2)=2, F(3)=5 over all triples,
        # then multiplies by 2 because every coefficient is 2/(9*r).
        e, c = induced[mask], cuts[mask]
        return 2 * ((2 * r + 3 * k) * e + 2 * k * c)

    max_block_violation = 0
    max_singleton_violation = 0
    for mask in range(1 << n):
        s, e = sizes[mask], induced[mask]
        for k in range(r + 1):
            p = potential_numerator(k, mask)
            denominator_cost = 9 * r * (s + k)
            # Distinguished block test separates all anchors from graph U.
            deficit = p - potential_numerator(k, 0) - potential_numerator(0, mask)
            assert deficit == 2 * k * (6 * s - e)
            max_block_violation = max(max_block_violation, deficit - denominator_cost)

            if k:
                # Any selected anchor has the same singleton-test deficit.
                deficit = p - potential_numerator(k - 1, mask)
                assert deficit == 2 * (6 * s - e)
                max_singleton_violation = max(
                    max_singleton_violation, deficit - denominator_cost)

            remaining = mask
            while remaining:
                low = remaining & -remaining
                u = low.bit_length() - 1
                remaining ^= low
                neighbors = (adjacency[u] & mask).bit_count()
                deficit = p - potential_numerator(k, mask ^ low)
                assert deficit == 2 * (6 * k + 2 * r * neighbors - k * neighbors)
                max_singleton_violation = max(
                    max_singleton_violation, deficit - denominator_cost)

    max_cut = max(cuts)
    # Multiply max(0, MC/9-r) by common denominator 9*r.
    predicted = max(0, r * max_cut - 9 * r * r)
    assert max_block_violation == predicted
    assert max_singleton_violation == 0
    state_types = (1 << n) * (r + 1)
    print(f"{name}, r={r}: {state_types} state types audited; "
          f"MaxCut={max_cut}; block violation numerator={predicted}; "
          "all singleton capacities valid")


def audit_regularizing_gadget():
    # K4 with edge (0,1) subdivided through x=4. Attaching x to a fixed-color
    # old vertex v=5 yields an additive MaxCut contribution exactly seven.
    internal = [(i, j) for i in range(4) for j in range(i + 1, 4)
                if (i, j) != (0, 1)] + [(0, 4), (4, 1)]
    for color_v in (0, 1):
        best = 0
        for colors in product((0, 1), repeat=5):
            value = sum(colors[i] != colors[j] for i, j in internal)
            value += colors[4] != color_v
            best = max(best, value)
        assert best == 7


if __name__ == "__main__":
    audit_triple_identity()
    audit_regularizing_gadget()
    for graph in ("K4", "K3,3", "prism", "cube", "two cubes"):
        for r in (2, 3):
            audit_graph(graph, r)
    print("All exact audits passed.")
