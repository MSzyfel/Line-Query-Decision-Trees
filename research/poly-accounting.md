# Polynomial-time accounting routes: proved limits and useful refinements

Prepared 13 October 2026 for the general supplied planar line-query model. This report audits polynomial-time improvements through constant-depth lookahead, endpoint coding, and stronger restriction accounting. It does not claim a new constant approximation factor. The separate polynomial scheduling reports establish the improved factors.

## 1. Constant-depth lookahead is polynomial, but its saving vanishes with instance size

Let the existing polynomial baseline satisfy

```
B_W(A) <= a OPT_W(A) + gamma log_2 |A|,
B_E(A) <= a OPT_E(A) + c H(A).
```

At the root optimize a depth-`k` trunk exactly and place the baseline at its frontier, where `k` is a fixed constant. This needs at most `(2m+1)^(k+1)` state descriptions and polynomial work per state. Thus it is polynomial for fixed `k`; allowing `k` to grow with `log n` is the quasipolynomial construction and does not answer the polynomial-time request.

For maximum depth `D`, if `D<k` the result is exact. Otherwise truncating an optimum tree gives

```
cost_W <= a D + gamma log_2(n-k) - (a-1)k.
```

Every proper query on a surviving branch removes at least one hypothesis, so a depth-`k` frontier has at most `n-k` hypotheses. This is a strict, instance-dependent improvement over the original additive bound, but its improvement in the certified uniform ratio is at most of order `k/(n-1)`. It supplies no fixed asymptotic improvement.

For expected depth use raw weights. If `P` is the raw expected prefix cost, `q` the raw frontier mass, and `R` the remaining optimum cost, then `P+R=OPT`, `P>=kq`, and

```
cost_E <= a OPT - (a-1)P + c sum_frontier H(A),
sum_frontier H(A) <= q ln(n-k).
```

The first inequality retains the prefix saving discarded in the earlier rollout statement. It can make practical polynomial lookahead useful on shallow or concentrated instances. Since `P>=w(S)` for a nontrivial root, it also improves the old bound by at least `(a-1)w(S)`. Neither statement turns into a fixed improvement for all growing instances: the relevant ratios can vanish when optimum depth grows.

## 2. A universal three-query endpoint redundancy is impossible

After a positive hull answer, patterns are intervals containing its vertex. Consider nine endpoint pairs

```
left in {1,2,3}, right in {5,6,7}, known positive vertex 4.
```

Each remaining hull query is one threshold on one of these two coordinates. Give pattern `(2,6)` probability `1-8 eta`, and give each other pattern probability `eta`.

Four axial neighbors force four distinct queries on the dominant pattern's path:

| Alternative pattern | Unique distinguishing hull vertex |
|---|---:|
| `(1,6)` | 1 |
| `(3,6)` | 2 |
| `(2,5)` | 6 |
| `(2,7)` | 7 |

Any correct endpoint tree therefore uses at least four queries on `(2,6)`. As `eta` tends to zero, its information approaches zero. This rules out both a universal pointwise `log_2(1/p)+3` bound and a universal expected `H_bits+3` bound for the endpoint subproblem. The existing additive four is asymptotically tight without further conditions.

These intervals are geometrically realizable: put hull vertices on a short arc of a unit circle, with all nine desired arcs spanning less than a semicircle. A primal point whose direction is the desired arc midpoint and whose norm selects its two boundary gaps realizes each interval by dot-product thresholds. Additional singleton patterns elsewhere on the circle can make every supplied hull cap have arbitrarily small total probability relative to the complete state. Thus mass-flatness at the parent does not eliminate the conditioned endpoint obstruction.

The exact finite check in `poly-accounting-check.py` uses `eta=1/10000`; it computes the optimal weighted endpoint tree, verifies all four forced questions, and checks redundancy exceeding three. This obstruction concerns the endpoint subproblem with hull queries. It does not prove a lower bound on complete general-case approximation algorithms, which may change discovery or combine its work with endpoint recovery.

## 3. Why naive dominance and boundary enumeration do not yet prove a better maximum-depth constant

A class with count exceeding half a hull cap is unique in that cap. If an adjacent supporting pair has two distinct such classes, each class has a boundary at its corresponding supporting vertex; an additional neighboring query can pin an endpoint. This is a real local improvement.

The remaining case is a large class positive on both supporting vertices. Replacing the original first pair with a pair at that class's boundary saves endpoint work for it. But the replacement can miss smaller classes originally covered by the first pair. Returning to that pair adds discovery work for later deadline prefixes. A constant class-size bonus pays for the early small classes, but it does not automatically pay for the delay of later large classes. Simply adding the new pair to the comparison loses the same units one hoped to save in decoding.

A successful lemma must maintain all deadline prefixes simultaneously. It cannot only show that the dominant class is decoded cheaply. Two concrete targets remain useful:

1. A deadline scheduler that can postpone the missed first-pair demands without delaying later large classes.
2. A larger removable-prefix credit when the initial dominant class is handled by a boundary query.

Neither target is proved here. The unchanged worst-case constant should be retained until one is established.

## 4. Stronger restriction accounting: the relevant missing statement

For a hull-pattern class, an original query can vary within it only if the class is positive on at least one of its at most two supporting hull vertices. Hence, at the initial flat state, the total mass of classes on which a particular supplied query can vary is at most `2 delta w(S)`.

This property is stronger than arbitrary partitions, but it is an absolute parent-state bound. Deep nodes of an optimal tree can have less mass than `2 delta w(S)`, so the bound does not give a useful fraction of the queries removed there. Any improved accounting proof must either control such small nodes separately or express the ambiguity bound in terms of their actual conditional masses.

In particular, one cannot assume the general inequality

```
OPT_E(S) - sum_A OPT_E(A) >= I(S,Pi)/ln 2.
```

An arbitrary partition can increase redundancy in the restricted subproblems. Entropy reduction and optimum-cost reduction are distinct quantities; the current analysis appropriately telescopes both. A new inequality for hull-pattern partitions would need a geometry-specific proof.

The most promising polynomial target is a stage inequality that retains actual block overlap, cached negative neighbors, and these mixed-class masses jointly. The endpoint obstruction shows why reducing the coding allowance alone cannot supply the improvement.
