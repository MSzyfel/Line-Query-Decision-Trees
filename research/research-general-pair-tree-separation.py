"""Small exhaustive audit of the FIXED-QUERY pair+tree MaxCut reduction.

This does not test all-query capacity validity.  Test-family completion
making the hierarchy legal may introduce other capacity violations.
"""

from fractions import Fraction
from math import lcm
from pathlib import Path
import json


def construct(vertices, edges, threshold):
    denominator = 24 * len(edges)
    red, blue = [[] for _ in range(vertices + 1)], [[] for _ in range(vertices + 1)]
    triples = []
    next_symbol = 0
    def symbol(group, color):
        nonlocal next_symbol
        value = 1 << next_symbol
        next_symbol += 1
        (red if color else blue)[group].append(value)
        return value
    for u, v in edges:
        triples.append((symbol(vertices, True), symbol(u, False), symbol(v, False)))
    degrees = [sum(v in edge for edge in edges) for v in range(vertices)]
    assert min(degrees) > 0
    for v, degree in enumerate(degrees):
        for _ in range(degree):
            symbol(v, True)
    for _ in edges:
        symbol(vertices, False)
    groups = []
    for v in range(vertices + 1):
        p = len(red[v])
        assert p == len(blue[v])
        cost = (Fraction(3 * degrees[v], 2 * denominator) if v < vertices
                else Fraction(threshold, 2 * denominator))
        coefficient = (2*p-cost)/(p*p)
        groups.append((sum(red[v]), sum(blue[v]), p, coefficient))
    multiple = lcm(2 * denominator, *(x[3].denominator for x in groups))
    groups_int = [(r, b, p, int(a * multiple)) for r, b, p, a in groups]
    return next_symbol, triples, groups_int, denominator, multiple


def audit(vertices, edges):
    maxcut = max(sum(bool(mask >> u & 1) != bool(mask >> v & 1) for u, v in edges)
                 for mask in range(1 << vertices))
    cases = []
    for threshold in range(len(edges) + 1):
        n, triples, groups, denominator, multiple = construct(vertices, edges, threshold)
        best = 0
        nonconsensus_best = None
        for selected in range(1 << n):
            score = -multiple * selected.bit_count()
            consensus = True
            for red, blue, p, coefficient in groups:
                r, b = (selected & red).bit_count(), (selected & blue).bit_count()
                score += coefficient * r * b
                consensus &= ((r == b == 0) or (r == b == p))
            tree_drop = 0
            for a, u, v in triples:
                if selected & a:
                    xu, xv = bool(selected & u), bool(selected & v)
                    tree_drop += 2 * (xu + xv) - xu * xv
            score += (multiple // denominator) * tree_drop
            best = max(best, score)
            if not consensus:
                nonconsensus_best = (score if nonconsensus_best is None
                                     else max(nonconsensus_best, score))
        expected = max(0, maxcut - threshold) * (multiple // (2 * denominator))
        assert best == expected
        assert nonconsensus_best < 0
        cases.append({"threshold": threshold, "n": n,
                      "maximum_violation": str(Fraction(best, multiple)),
                      "nonconsensus_maximum": str(Fraction(nonconsensus_best, multiple))})
    return {"vertices": vertices, "edges": edges, "maximum_cut": maxcut, "cases": cases}


def main():
    rows = [audit(2, [(0, 1)]),
            audit(3, [(0, 1), (1, 2)]),
            audit(3, [(0, 1), (1, 2), (0, 2)])]
    output = {"fixed_query_only": True, "families": rows,
              "subset_threshold_checks": sum((1 << c["n"]) for r in rows for c in r["cases"])}
    Path("research-general-pair-tree-separation-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
