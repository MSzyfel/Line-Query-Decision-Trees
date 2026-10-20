# A completed selector replay already repairs the private-context barrier

Auxiliary research note, 19 October 2026. The article is unchanged.

**Proved result.** The existing first pass of global code lifting already
contains a nearly optimal complete code on the private selector/body product
class below, including a growing number of selector coordinates and arbitrary
context-dependent injective body labels. No additional harvesting layer or
larger intersection closure is required. A joint selector-pair and fiber-coding
certificate proves the approximation bound. This is a structured-class result,
not an unrestricted approximation improvement or a new lower-bound cone.

## 1. Class and priorities

Let the uniform hypotheses be

    H=(product_(i=1)^k [Mi]) times (product_(j=1)^ell [rj]),
    P=product_i Mi,  N=product_j rj,  n=PN,

with `k,ell>=1`, all alphabets at least two, and

    min_i Mi > max_j rj.

The first coordinates are selectors; the last are bodies. Supply every pure
coordinate equality. For each complete selector context `b` and body `j`,
supply a private palette of `bj` binary tests whose labels inject the `rj`
body values into `{0,1}^bj`. A palette test is positive only in context `b`.
The injection may depend arbitrarily on `b` and `j`; it need not be affine or
preserve zero. Put pure equalities before all private palette tests in the
input tie order. Other ordering within these groups is unrestricted.

Write `B=sum_j bj` and `e(s)=(s+1)/2-1/s`. The minimal-width specialization is
`bj=ceil(log2 rj)`. Both numbers of coordinates may grow with the explicit
input; the algorithm does not enumerate policies of a growing horizon.

## 2. The source really is generated before lifting

Initial balance greedy identifies the bodies using pure equalities before it
queries a selector. While a body remains unknown, a body equality has minority
at least `1/max_j rj`. A selector equality has minority at most
`1/min_i Mi`, and every private palette test has positive probability at most
`1/P`. These are strictly smaller. Equality queries preserve the product
posterior, so the argument continues throughout the body phase.

Consequently every fixed-body slice

    C_z={all selector tuples} times {one fixed body tuple z}

is an actual incumbent node. Its size is `P>1`, so `source_codes` explicitly
requests fresh complete greedy there before freezing the source list.

On `C_z`, a private palette test is zero or a singleton **selector-context**
test. Any proper pure selector equality has integer minority at least one,
at least as much as a singleton-context test; pure equalities win ties.
Fresh greedy on this slice therefore uses only pure selector queries.
It identifies the independent uniform selector coordinates at average cost
`sum_i e(Mi)`. This holds for any fixed `z`: an all-zero anchor is convenient
but unnecessary, including under independently relabeled body codes.

## 3. Its ordinary completed replay is already a good full tree

Replay that slice source globally. Its physical tests depend only on selectors,
so its lifted leaves are exactly all full selector fibers

    S_b={b} times {all body tuples}.

Selector-query raw work is exactly `n sum_i e(Mi)`. The actual implementation
then calls `finish_partial` at each lifted leaf. That function compares the
incumbent restricted to `S_b` with fresh greedy on `S_b` and grafts the cheaper
actual complete tree. `generated_pass` retains **all nodes of the completed
lift**, including these fallback codes.

Here fresh greedy on each `S_b` has path length at most `B`, regardless of bit
ordering or how queries of different bodies interleave. Once the selector is
known, queries affect only one body coordinate. Each body remains uniform on
its surviving values, independently of the others, and has just one active
injective owner palette plus singleton body equalities.

For body `j`, before its first chosen equality, suppose `q` owner bits have
been asked. If greedy now chooses a singleton equality among `s` remaining
values, every remaining owner bit has minority at most one in that coordinate.
Previously asked owner bits are constant. At most one distinct owner label
agrees with all remaining-bit majority answers; every other label lies in one
of at most `bj-q` minority singleton cells. Thus `s-1<=bj-q`. The prior `q`
queries plus any proper continuation of that body on `s` values use at most
`q+s-1<=bj` queries. If no equality is chosen, at most `bj` proper owner-bit
queries can occur. Applying this argument separately to each body proves the
path bound, even with arbitrary interleaving across bodies.

The one completed replay therefore has average depth at most

    U=sum_i e(Mi)+B.                                       (1)

If incumbent restriction is cheaper at some replay leaf, the bound improves.
All nodes of this complete tree are already first-pass base states. Hence the
exact supported-state depth-prize DP can realize it without using pairwise
intersections. A complete comparison tree earns all incumbent prizes, so the
actual first-pass output has cost at most this tree (and at most its original
incumbent). No inference from existence of an unexecuted abstract code is used.

The source list remains frozen: fallback codes are not used as new global
sources in this argument. The initially proposed extra harvest layer was
unnecessary because these fresh fallback codes are already included by the
existing completion operation.

## 4. A joint pair/coding lower certificate

For an arbitrary candidate subset `S`, count all unordered pairs contained in
`S` which agree in every body and all but one selector coordinate. Give each
such pair weight **one**. Let `S_b=S intersect S_b_full` and define

    Phi(S)=selector_axis_pairs(S)+sum_b L2(|S_b|),           (2)

where `L2` is the exact integer binary coding cost, zero on sizes zero and one.
There is no factor of two in the pair term. The query deficit of that term is
exactly the weight of cut pairs.

For every actual subset and supplied query,

    Phi(S)-Phi(S_0)-Phi(S_1)<=|S|.                          (3)

The endpoint accounting proves this directly:

* A selector equality cuts only pairs differing in that selector. Assign each
  cut pair to its endpoint outside the queried value. Every such endpoint has
  at most one matching endpoint inside. Whole context fibers are routed
  intact, so their coding deficit is zero.
* A body equality cuts no selector-axis pairs. Its binary coding deficit in
  every fiber is at most that fiber's population; these populations sum to
  `|S|`.
* A private palette query on context `b` has a coding deficit only inside
  `S_b`, at most `|S_b|`. Assign its cut pairs to endpoints outside context
  `b`. Each outside endpoint has at most one matching positive point in `b`,
  since pairs agree on the body tuple and all other selector coordinates.
  Pair charges and coding charges use disjoint endpoints, each with load at
  most one.

Nonnegativity, singleton value zero, and (3) telescope down any complete legal
decision tree. Consequently

    OPTmean >= A+L2(N)/N >= A+log2 N,
    A=(1/2) sum_i(Mi-1).                                  (4)

This is a specialization of the existing joint pair/resource ledger. It is
polynomially verifiable from the explicit class representation, with at most
quadratically many pairs and at most `n` fibers. No difficult certificate
synthesis or all-subset LP separation is assumed.

For minimal-width body palettes, put `M_min=min_i Mi` and
`r_min=min_j rj`. The elementary bounds

    sum_i e(Mi)<=A(1+2/M_min),
    B<=log2 N+ell<=(1+1/log2 r_min)log2 N

combine with (1)-(4) to give

    first-pass output / OPT
       <= [sum_i e(Mi)+B]/[A+L2(N)/N]
       <= 1+max(2/M_min,1/log2 r_min).                     (5)

In particular, the class has a constant guarantee even for growing `k`, and
the guarantee tends to one as the selector and body alphabets grow. The
uniformity of the product and the private single-context meaning of every
body query are essential hypotheses. For wider supplied palettes (1) and (4)
still hold, while the last bound in (5) must retain their actual `B`.

## 5. What this repairs and what it does not prove

The two-selector family in
`research-general-resolution-bundle-obstruction.md` is a special case. The
same argument covers its private multi-selector extensions with any number of
selectors. Its one-root-query/fresh-greedy template neighborhood has a
full-order bad fixed point, yet the existing global replay of a selector-only
slice, followed by existing fresh collision completion, repairs that family in
one pass. These are different algorithmic neighborhoods.

This result does not establish universal source quality or global approximation.
Aliased body tests active in multiple selector contexts need not become
singleton-context tests on a fixed-body slice, and several unrelated active
palettes in one fiber need not satisfy the owner-palette path bound. Those
cases require separate arguments. The guarantee here does not require
recognizing the product structure to run the full generic generator; the
analysis identifies a source and completed lift that it automatically includes.

## 6. Bounded verification

`research-general-selector-replay.py` checks seven explicit instances through
`n=750`, including one, two, three, and five selector coordinates. Several
use independently permuted context/body labels with globally interleaved
palette order. It verifies actual incumbent slice membership, source query
purity, every full selector fiber in the replay, actual complete fallback
execution, the per-coordinate path bound, and exact supported output on a
reduced subset of the original first-pass base states.

It also checks the endpoint ledger directly, and exhausts `61,952`
subset/query inequalities on the `n=6,12` cases. All seven have zero extra
harvest layers and use no quadratic closure or exact optimal-subproblem oracle.
Growing-parameter ratio checks through `M=512`, with both fixed and growing
selector counts, use only exact cost formulas and integer products. Large
response matrices are never constructed. All checks passed.
