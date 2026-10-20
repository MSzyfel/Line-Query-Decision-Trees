# General decision tree partition decoding

Research note dated 18 October 2026. The model has an explicit separating binary test matrix, uniform hypotheses, and unit test costs. This note isolates a limitation of transferring the planar potential argument. It does not prove a better approximation ratio for unrestricted instances.

## What transfers from the planar argument

Write F(S) for the minimum unnormalized identifying cost on S. For a partition Pi of S, define

    Delta(S,Pi) = F(S) - sum_{A in Pi} F(A),
    I_2(S,Pi) = |S| log_2 |S| - sum_{A in Pi} |A| log_2 |A|.

The restriction inequality gives Delta >= 0. Both quantities telescope over a recursive partition tree. Consequently a legal stage with output Pi and work

    W(S) <= a Delta(S,Pi) + c I_2(S,Pi)

at every state would give an (a+c)-approximation for binary uniform identification. Here work is the sum, over hypotheses, of the queries made by that stage. This is the accounting in sections/02-preliminaries.tex, with entropy measured in bits instead of natural logarithms.

The planar proof obtains an affordable full-pattern decoder from the circular interval of positive hull tests. The following theorem shows why an arbitrary partition cannot be substituted for that pattern partition.

## Exact obstruction from linear syndromes

Let H = F_2^d, n = 2^d, and supply just the d coordinate tests. Let M be an r by d binary matrix of rank r, with 1 <= r <= d. Partition H by its syndrome Mx. Write a(M) for the number of nonzero columns of M.

**Proposition.** For this explicit binary uniform instance:

    F(H) = nd,
    sum_{A in Pi_M} F(A) = n(d-r),
    Delta(H,Pi_M) = nr,
    I_2(H,Pi_M) = nr,
    minimum work of a stage revealing Pi_M = n a(M).

**Proof.** Identifying all d coordinates costs d per hypothesis. The binary entropy lower bound is d, so this is optimal.

Every syndrome fibre is an affine space of dimension d-r and cardinality 2^(d-r). A linear information set gives d-r coordinates whose values determine a point in that fibre: choose a basis of the coordinate functionals restricted to its translation space. Query those coordinates. The entropy lower bound gives the reverse inequality. Therefore F(A)=|A|(d-r) on every fibre, proving the first four identities.

If column i of M is nonzero, two vectors differing just in coordinate i have different syndromes. On any decision tree path which has not queried coordinate i, both such vectors remain possible. Hence every path of an exact syndrome-revealing stage must query every coordinate with nonzero column. Querying precisely those coordinates suffices. Thus each path has minimum length a(M), proving the last identity. This lower bound also applies to zero-error randomized stages by conditioning on their randomness. QED.

For the parity partition M=(1,...,1), this specializes to

    Delta = n, I_2 = n, minimum stage work = n log_2 n.

Thus there are no absolute constants a,c giving an affordable decoder bound a Delta+c I_2 for every partition. More generally, dense syndromes of rank r require a+c >= d/r under such a bound.

The underlying identification problem here is easy and greedy is optimal. This is an obstruction to a proposed partition-decoding argument, not a hardness result for decision tree approximation. The planar theorem is unaffected: it chooses partitions with a supplied-query endpoint decoder.

## Where the restriction saving occurs

For parity, restricting a coordinate identification tree to one parity class deletes its final coordinate query. Knowing the class therefore saves one query on every hypothesis. Learning that class initially still requires all d coordinates. Restriction savings can come from queries near the leaves without making the class cheap to reveal near the root.

This distinguishes two algorithmic obligations. A candidate partition must expose useful continuation savings, and there must also be a legal original-test strategy that reaches its classes at a comparable cost. Optimizing a partition only by Delta and entropy cannot supply the second obligation.

## A concrete test for general macros

For every proposed macro, record its actual partial tree, its output partition, its exact small-instance work, and both potential decreases. On larger instances where F is unavailable, use complete restricted continuation trees for upper costs and a separately proved Bellman-consistent lower potential for certificates. Do not replace an implementable decoder by the entropy of its output label.

The most useful next target is a polynomial generator of query-aligned partitions with an affine stage inequality. Merely requiring a small support replacement for every original test is insufficient: taking each test as its own support satisfies that requirement in every instance.

## Computational verification

research-general-decoding.py independently solves both the identification and syndrome-revelation recurrences on small explicit coordinate instances. It checks all full-rank matrices through dimension three and seeded random matrices in higher dimensions. The mathematical proof above supplies the asymptotic statement; these checks verify the formulas and cost normalization.

## Sources

- Local sections/02-preliminaries.tex: restriction and recursive potential cancellation.
- Local sections/03-common-witness-geometry.tex and sections/06-expected-depth.tex: adjacent supports, circular patterns, and endpoint recovery.
- [Li, Liang, and Mussmann, arXiv v2](https://arxiv.org/abs/1906.11385v2): the general greedy bound and its matching obstruction. The syndrome argument above is a separate derivation.
