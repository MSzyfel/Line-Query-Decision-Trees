# Constant-gap session: a PTAS obstruction for shallow convex-position caps

Research derivation, 13 October 2026. The model is finite point identification using only supplied strict binary line-side queries, each of unit cost. This session proves no fixed-factor inapproximability theorem. It also deliberately states no input-size-dependent approximation barrier. Its new result is a polynomial approximation scheme for a restricted family, which rules out a tempting fixed-gap construction in that family.

## New theorem

There is a distinguished hypothesis 0 whose answer to every query is miss. The other N hypotheses have a supplied cyclic order. Every query's hit set is a cyclic interval containing at most b hypotheses. The supplied queries separate the whole instance. Give all N+1 hypotheses equal weight. Private singleton queries are **not** required.

For each fixed b, uniform expected depth admits a PTAS. More precisely, for 0 < epsilon <= 1 choose

    L = max{2b, b(b-1), ceil(8b^2/epsilon)}.

If N < L, use exact subset Bellman optimization. Otherwise the construction below returns a tree of raw cost at most (1+epsilon) OPT. Its running time is polynomial in N and the query-list size for fixed b and epsilon. One explicit exponent is 2^((b+1)L); this is a **PTAS**, not an EPTAS or an efficient practical algorithm.

The geometric corollary applies when the N nonzero points are in strictly convex position and all supplied sides opposite the common witness contain at most b of them. A halfplane intersects vertices of a convex polygon in a cyclic interval: its boundary crosses the polygon boundary at most twice. Thus the cyclic-order hypothesis is satisfied. The distinguished witness need not be a polygon vertex.

This extends the earlier uniform two-cap exact theorem to an approximation scheme for every fixed cap size on one convex layer. It is consistent with the strong NP-completeness theorem for uniform clouds: their whole-cloud caps have unbounded cardinality.

## 1. Make small independent blocks

Partition the cyclic order into consecutive pieces of length L, allowing a shorter last piece. Mark the first b vertices of each piece for deletion, or the entire piece if it has at most b vertices. Let D be this set and r=|D|. Because N>=L,

    r <= b ceil(N/L) <= 2bN/L.

The unmarked portions are blocks of at most L vertices. Between every pair of neighboring nonempty blocks lie at least b marked vertices. A cyclic interval of at most b vertices therefore cannot meet two unmarked blocks: it would need to contain two unmarked vertices and all b marked vertices between them. This applies at the wraparound cut as well. If only one nonempty block remains, the conclusion is immediate.

Clear the marked vertices using a legal miss-spine prefix. While a marked vertex x is still live, choose any supplied cap containing x. Such a cap exists because the supplied tests distinguish x from the all-miss witness. Query it. Its first-hit group A has size at most b; identify A with any proper supplied-query code of height at most |A|-1, and continue on the miss branch. Proper local codes of this height exist in every separating finite binary test system, by repeatedly choosing a test separating two still-live points.

Each prefix query clears at least one still-live marked vertex, so there are at most r queries. It may clear additional unmarked points as well, which only shrinks the subsequent blocks. All residual caps are still contained in a single block.

The total raw prefix cost, including its positive exit codes, is at most

    r(N+1) + b(b-1)r.

The first term bounds the sum of the masses at the at most r prefix nodes. At most br points leave through hit exits; each incurs at most b-1 further local queries. Since N>=L>=b(b-1), the displayed expression is at most 2r(N+1).

## 2. Optimize independent blocks exactly

The residual instance has the miss witness and a collection of blocks, each of size at most L. Every query's hit set lies in one block. All these statements concern the actual supplied query restrictions; no extra geometric query is added.

Relabel the vertices of a block by their positions. Its **type** is its size and the set F of all distinct nonempty query masks restricted to that block. Every such mask is an ordinary interval of at most b positions. A wrapping cap would contain the full marked gap plus two unmarked endpoints, contradicting its size bound; deletion of additional points preserves interval order. There are at most bL possible masks, and hence at most 2^(bL) types. The union of a type's masks contains every block point because each point separates from the witness, so padding to L positions also determines the block size. For a type T and a nonempty live mask R, call (T,R) a local state. There are at most

    d_(b,L) = 2^((b+1)L)

such states. A global miss-spine state is represented by counts c_(T,R) of blocks in each local state. Its total live mass, including the witness, is

    W(c) = 1 + sum_(T,R) c_(T,R) |R|.

For each type, precompute the exact raw local identification costs g_T(A) on all subsets A using ordinary subset Bellman DP, with all query masks in that type. There is no witness in this local positive branch, and g_T(A)=0 for |A|<=1.

Let e_(T,R) denote a unit count vector, treating e_(T,empty)=0. The exact global recurrence is

    F(0)=0,
    F(c)= W(c) + min {
        g_T(A) + F(c - e_(T,R) + e_(T,R\A))
      : c_(T,R)>0, q in F_T, A=R intersect q nonempty
    }.

Every transition removes at least one live point, so this is an acyclic dynamic program. Every proper query in a state has its positive group in exactly one block; the positive code can be optimized independently, and the negative state has the displayed count update. Conversely, each transition is a legal supplied query on any physical block of the chosen type and state, followed by its legal positive code and its miss continuation. Thus the recurrence is exact for **arbitrary adaptive identifying trees**, not merely for an assumed ordering or a restricted normal form.

The count-vector state space has at most (N+1)^d_(b,L) states. Local DPs and transition counts depend only on L, apart from reading/deduplicating the input. Backtracking reconstructs a legal tree by tracking which physical blocks realize each local state. Store a supplied realizing query for every mask of **each physical block**: identical abstract types can be represented by different original lines in different blocks. Uniformity is essential for the finite type count: arbitrary real input weights cannot be grouped this way without an additional rounding argument.

## 3. Charge the discarded prefix against the full optimum

Let OPT be the original raw uniform optimum. Restrict an optimal full tree to the residual hypotheses, suppressing nodes whose answers become constant. Its raw cost can only decrease. Therefore the exact residual block optimum is at most OPT.

Following the all-miss witness in any full tree gives first-hit groups of size at most b. The sum of first-hit depths of the N other points is at least

    sum_(i=1)^N ceil(i/b) >= N(N+1)/(2b).

This lower-bounds OPT; the witness depth and all local positive costs are nonnegative additional terms. For the constructed tree, the excess over OPT is therefore at most 2r(N+1), and

    (G_alg - OPT)/OPT
      <= 4br/N
      <= 8b^2/L
      <= epsilon.

Normalizing by N+1 gives exactly the same expected-depth ratio. No subtraction from the original objective is used.

If every singleton query is supplied, clearing the r marked points by their singleton tests requires no positive local costs, and the same argument gives the slightly sharper error bound 4b^2/L. The no-singleton theorem above is the more general statement.

## What this resolves for constant-factor hardness

The GOOD/BAD six-point examples remain useful demonstrations that static coverage curves do not determine optimal ordered cost. However, they lie on one convex layer with bounded cap size. Adding more bounded-size interval caps, even caps coupling neighboring blocks, cannot turn this whole subclass into a fixed-gap NP-hard source unless P=NP: choose a fixed epsilon below the proposed gap and run the PTAS.

Consequently a constant-gap reduction based on common-witness shallow cover must escape at least one condition: fixed cap size, a single cyclic interval order, or uniform weights. Several convex layers might escape the cyclic order, but their geometric realizability and an extraction of one globally consistent assignment from every near-optimal adaptive tree remain unproved. Arbitrary-prior weighted paths already have an EPTAS, so merely changing the six-point blocks to weighted singleton/pair paths is also insufficient.

For the unrestricted problem, constant-factor inapproximability remains open in this investigation. The missing proof obligation is still global choice coupling that survives independent branch optimization and legal query promotion. This session narrows the viable geometry rather than pretending that a local example supplies that obligation.

## Verification

`constant-gap-session.py` uses an independent full adaptive subset Bellman solver and the count-vector block recurrence. It checks cyclic-interval geometry, exact residual costs, original-tree prefix reconstruction, and the quantitative ratio bound, both with a complete singleton supply and with randomly sampled separating families having no required singleton supply. The proof above establishes the PTAS; the finite checks audit its mechanics.
