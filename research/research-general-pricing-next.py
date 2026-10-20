"""Exact completion pricing inside an explicit decision-tree template.

The experiments audit finite identities, not an improved UDT approximation.
No third-party modules are needed.
"""
from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
import json
import random


@dataclass(frozen=True)
class Tree:
    leaves: tuple
    children: tuple = ()

    @property
    def size(self):
        return len(self.leaves)


def join(left, right):
    return Tree(left.leaves + right.leaves, (left, right))


def balanced(leaves):
    if len(leaves) == 1:
        return Tree(tuple(leaves))
    mid = len(leaves) // 2
    return join(balanced(leaves[:mid]), balanced(leaves[mid:]))


def comb(leaves):
    result = Tree((leaves[-1],))
    for leaf in reversed(leaves[:-1]):
        result = join(Tree((leaf,)), result)
    return result


def finish_count_dp(tree):
    """Minimum raw work for every exactly declared completion count."""
    if not tree.children:
        return {1: 0}
    left = finish_count_dp(tree.children[0])
    right = finish_count_dp(tree.children[1])
    out = {0: 0}
    for kl, wl in left.items():
        for kr, wr in right.items():
            k = kl + kr
            work = tree.size + wl + wr
            if k not in out or work < out[k]:
                out[k] = work
    return out


def prize_dp(tree, prizes, multiplier):
    """Minimum W - multiplier * completed prize over all template prefixes."""
    if not tree.children:
        return -multiplier * prizes[tree.leaves[0]]
    return min(0, tree.size + sum(prize_dp(c, prizes, multiplier)
                                 for c in tree.children))


def enumerate_prefixes(tree):
    """Audit oracle: enumerates actual completion sets, exponential in size."""
    if not tree.children:
        return [(0, frozenset(tree.leaves))]
    out = [(0, frozenset())]
    for wl, cl in enumerate_prefixes(tree.children[0]):
        for wr, cr in enumerate_prefixes(tree.children[1]):
            out.append((tree.size + wl + wr, cl | cr))
    return out


def uniform_depth(tree, depth):
    if not tree.children:
        return 0, 1
    if depth == 0:
        return 0, 0
    results = [uniform_depth(child, depth-1) for child in tree.children]
    return tree.size + sum(x[0] for x in results), sum(x[1] for x in results)


def all_uniform_depth_densities(tree):
    """All depth caps simultaneously, without repeatedly traversing the tree."""
    frontier = [tree]
    work = 0
    done = 0
    values = []
    depth = 0
    while frontier:
        internal = [node for node in frontier if node.children]
        done += sum(not node.children for node in frontier)
        if done:
            values.append((Fraction(work, done), depth, work, done))
        work += sum(node.size for node in internal)
        frontier = [child for node in internal for child in node.children]
        depth += 1
    return values


def height(tree):
    return 0 if not tree.children else 1 + max(height(c) for c in tree.children)


def random_tree(leaves, rng):
    if len(leaves) == 1:
        return Tree(tuple(leaves))
    order = list(leaves)
    rng.shuffle(order)
    k = rng.randrange(1, len(leaves))
    return join(random_tree(order[:k], rng), random_tree(order[k:], rng))


def audit_small():
    rng = random.Random(20261019)
    cases = 0
    weighted_cases = 0
    for n in range(2, 10):
        for _ in range(30):
            tree = random_tree(list(range(n)), rng)
            prefixes = enumerate_prefixes(tree)
            dp = finish_count_dp(tree)
            exact = {}
            for work, completed in prefixes:
                k = len(completed)
                if k not in exact or work < exact[k]:
                    exact[k] = work
            assert dp == exact
            density = min(Fraction(w, k) for k, w in dp.items() if k)
            assert density == min(Fraction(w, len(c)) for w, c in prefixes if c)
            # The threshold/closure formulation is checked with arbitrary
            # integer prizes and rational Lagrange multipliers.
            prizes = {h: rng.randint(1, n) for h in range(n)}
            for mult in (Fraction(1, 3), Fraction(1), Fraction(7, 2)):
                got = prize_dp(tree, prizes, mult)
                expected = min(w - mult * sum(prizes[h] for h in c)
                               for w, c in prefixes)
                assert got == expected
                weighted_cases += 1
            cases += 1
    return cases, weighted_cases


def depth_gap():
    results = []
    # n=(d+1)2^d, easy block=2^d. The nonuniform prefix stops at the
    # hard-block root and fully decodes the balanced easy block.
    for d in range(2, 8):
        easy = 1 << d
        n = (d+1) * easy
        tree = join(balanced(list(range(easy))), comb(list(range(easy, n))))
        dp = finish_count_dp(tree)
        optimal, k, work = min((Fraction(w, k), k, w)
                              for k, w in dp.items() if k)
        uniform, depth, _, _ = min(all_uniform_depth_densities(tree))
        witness = Fraction(n + easy*d, easy)
        assert optimal <= witness
        # Cross-check cap accounting on small trees.
        if d <= 4:
            for value, t, w, count in all_uniform_depth_densities(tree):
                assert uniform_depth(tree, t) == (w, count)
        results.append({"d": d, "n": n, "easy": easy,
                        "optimal_density": float(optimal),
                        "optimal_completed": k, "optimal_work": work,
                        "best_uniform_cap_density": float(uniform),
                        "best_uniform_depth": depth,
                        "density_loss_from_uniform_caps": float(uniform/optimal)})
    return results


if __name__ == "__main__":
    # Comb recursion reaches 896 leaves in the last construction.
    import sys
    sys.setrecursionlimit(10000)
    small, weighted = audit_small()
    print(json.dumps({"exact_prefix_cases": small,
                      "weighted_Lagrange_cases": weighted,
                      "uniform_depth_gap": depth_gap(),
                      "status": "all exact audits passed"}, indent=2))
