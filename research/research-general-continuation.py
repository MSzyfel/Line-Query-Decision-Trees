"""Audits continuation by pruning one incumbent decision tree.

No third-party dependencies.  The exact insertion audit uses a bottom-up
credit formula, so it checks EVERY test at EVERY incumbent node in O(m*n)
arithmetic operations.  This is an experiment, not a proof of a new UDT
approximation ratio.  See research-general-continuation.md for the proof.
"""

from __future__ import annotations

import argparse
import itertools
import json
from dataclasses import dataclass


@dataclass(frozen=True)
class Node:
    mask: int
    left: int = -1
    right: int = -1


def column_cost(c: int) -> int:
    return c * (c + 1) // 2 - 1 if c else 0


def row_cost_table(b: int, c: int) -> float:
    """Exact mean of the specified row tree; O(2**b) memory/time."""
    q = 1 << (b - 1)
    cost = [0] * (q + 1)
    for s in range(2, q + 1):
        a = min(s // 2, max(1, (2 * s) // c))
        cost[s] = s + cost[a] + cost[s - a]
    return cost[q] / q + 1


def paired_instance(b: int, c: int):
    """Return tests and a row-first incumbent in postorder.

    Row x is paired with its bit complement.  Internal main-row children
    are unions of complete pairs.  Tests use hypothesis ID x*c + column.
    """
    if b < 1 or c < 3:
        raise ValueError("Require b >= 1 and C >= 3")
    r = 1 << b
    full_columns = (1 << c) - 1
    row_masks = [full_columns << (x * c) for x in range(r)]
    tests: list[tuple[str, int]] = []
    column_masks = []
    for j in range(c):
        mask = sum(1 << (x * c + j) for x in range(r))
        column_masks.append(mask)
        tests.append((f"column:{j}", mask))
    for j in range(c):
        for bit in range(b):
            mask = sum(
                1 << (x * c + j) for x in range(r) if (x >> bit) & 1
            )
            tests.append((f"gate:{j}:bit:{bit}", mask))

    nodes: list[Node] = []

    def leaf(h: int) -> int:
        nodes.append(Node(1 << h))
        return len(nodes) - 1

    def branch(left: int, right: int) -> int:
        nodes.append(Node(nodes[left].mask | nodes[right].mask, left, right))
        return len(nodes) - 1

    def column_chain(x: int, j: int = 0) -> int:
        if j == c - 1:
            return leaf(x * c + j)
        return branch(leaf(x * c + j), column_chain(x, j + 1))

    pairs = [(x, x ^ (r - 1)) for x in range(r // 2)]

    def row_tree(block: list[tuple[int, int]]) -> int:
        if len(block) == 1:
            x, y = block[0]
            tests.append((f"row:{x}", row_masks[x]))
            return branch(column_chain(x), column_chain(y))
        s = len(block)
        a = min(s // 2, max(1, (2 * s) // c))
        left_block, right_block = block[:a], block[a:]
        positive = 0
        for x, y in left_block:
            positive |= row_masks[x] | row_masks[y]
        tests.append((f"row-block:{len(tests)}", positive))
        return branch(row_tree(left_block), row_tree(right_block))

    root = row_tree(pairs)
    return tests, nodes, root


def insertion_audit(b: int, c: int) -> dict:
    tests, nodes, root = paired_instance(b, c)
    sizes = [v.mask.bit_count() for v in nodes]
    incumbent_cost = sum(sizes[i] for i, v in enumerate(nodes) if v.left >= 0)
    max_improvement = -10**30
    best = None
    checked = 0
    root_by_kind: dict[str, list[int]] = {}
    for name, positive in tests:
        counts = [0] * len(nodes)
        credits = [0] * len(nodes)
        for i, node in enumerate(nodes):
            if node.left < 0:
                counts[i] = int(bool(node.mask & positive))
                continue
            left, right = node.left, node.right
            pl, pr = counts[left], counts[right]
            p = counts[i] = pl + pr
            retained = 0
            if pl and pr:
                retained += p
            if pl < sizes[left] and pr < sizes[right]:
                retained += sizes[i] - p
            credits[i] = credits[left] + credits[right] + sizes[i] - retained
            if 0 < p < sizes[i]:
                checked += 1
                improvement = credits[i] - sizes[i]
                if improvement > max_improvement:
                    max_improvement = improvement
                    best = {"test": name, "state_size": sizes[i]}
                if improvement > 0:
                    raise AssertionError((b, c, name, i, improvement))
        root_by_kind.setdefault(name.split(":")[0], []).append(
            credits[root] - sizes[root]
        )
    n = sizes[root]
    row_mean = row_cost_table(b, c)
    incumbent_mean = incumbent_cost / n
    assert abs(incumbent_mean - row_mean - column_cost(c) / c) < 1e-10
    assert all(v == 0 for v in root_by_kind["column"])
    assert all(v == -(c - 1) * (1 << b) // 2 for v in root_by_kind["gate"])
    comparator = b + column_cost(c) / c
    return {
        "b": b, "C": c, "n": n, "m": len(tests),
        "incumbent_mean": incumbent_mean,
        "column_first_mean": comparator,
        "certified_ratio_at_least": incumbent_mean / comparator,
        "checked_splitting_node_test_pairs": checked,
        "maximum_strict_insertion_improvement": max_improvement,
        "example_maximizer": best,
        "root_gate_insertion_cost_increase": -root_by_kind["gate"][0],
    }


def block_plateau_audit(columns: list[int], dimension: int, horizon: int, c: int):
    """Exact row-only audit of a k-wise independent coset plateau.

    columns[i] describes row coordinate i as a linear form on the block's
    coefficient vector.  Every <=horizon columns must be independent.
    We check all nonadaptive coordinate sets; the proof covers adaptive
    prefixes too.  This does NOT enumerate all depth-horizon test trees.
    """
    b = len(columns)
    r = 1 << b
    code = [
        sum(((v & z).bit_count() & 1) << i for i, v in enumerate(columns))
        for z in range(1 << dimension)
    ]
    assert len(set(code)) == 1 << dimension
    unseen = set(range(r))
    blocks = []
    while unseen:
        representative = min(unseen)
        block = [representative ^ word for word in code]
        blocks.append(block)
        unseen.difference_update(block)
    nodes: list[Node] = []

    def branch(left, right):
        nodes.append(Node(nodes[left].mask | nodes[right].mask, left, right))
        return len(nodes) - 1

    def basis_tree(block):
        if len(block) == 1:
            nodes.append(Node(1 << block[0]))
            return len(nodes) - 1
        half = len(block) // 2
        return branch(basis_tree(block[:half]), basis_tree(block[half:]))

    def main_tree(current):
        if len(current) == 1:
            return basis_tree(current[0])
        s = len(current)
        a = min(s // 2, max(1, (2 * s) // c))
        return branch(main_tree(current[:a]), main_tree(current[a:]))

    root = main_tree(blocks)
    full_cost = sum(v.mask.bit_count() for v in nodes if v.left >= 0)

    def restricted_cost(mask):
        return sum(
            (v.mask & mask).bit_count()
            for v in nodes
            if v.left >= 0
            and (nodes[v.left].mask & mask)
            and (nodes[v.right].mask & mask)
        )

    checks = 0
    for q in range(1, horizon + 1):
        for bits in itertools.combinations(range(b), q):
            cells = [0] * (1 << q)
            for x in range(r):
                answer = sum(((x >> bit) & 1) << j for j, bit in enumerate(bits))
                cells[answer] |= 1 << x
            for block in blocks:
                projection = {
                    sum(((x >> bit) & 1) << j for j, bit in enumerate(bits))
                    for x in block
                }
                assert len(projection) == 1 << q
            completed_cost = r * q + sum(restricted_cost(cell) for cell in cells)
            assert completed_cost == full_cost, (bits, completed_cost, full_cost)
            checks += 1
    return {
        "b": b, "block_dimension": dimension,
        "blocks": len(blocks), "horizon": horizon,
        "coordinate_sets_checked": checks,
        "row_tree_mean": full_cost / r,
        "every_checked_prefix_net_improvement": 0,
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-b", type=int, default=20)
    parser.add_argument("--audit-b", type=int, default=8)
    args = parser.parse_args()
    for b in sorted({4, 5, 6, args.audit_b}):
        print(json.dumps({"exact_all_nodes_audit": insertion_audit(b, max(6, b))}))
    print(json.dumps({"two_bit_plateau_audit": block_plateau_audit(
        list(range(1, 8)), dimension=3, horizon=2, c=8
    )}))
    print(json.dumps({"three_bit_plateau_audit": block_plateau_audit(
        list(range(8, 16)), dimension=4, horizon=3, c=8
    )}))
    for b in range(8, args.max_b + 1, 2):
        c = b
        incumbent = row_cost_table(b, c) + column_cost(c) / c
        comparator = b + column_cost(c) / c
        print(json.dumps({
            "exact_cost_only": {
                "b": b, "C": c, "n": c * (1 << b),
                "incumbent_mean": incumbent,
                "column_first_mean": comparator,
                "certified_ratio_at_least": incumbent / comparator,
            }
        }))


if __name__ == "__main__":
    main()
