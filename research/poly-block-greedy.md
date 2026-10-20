# Why block priority greedy does not improve maximum depth

Prepared 13 October 2026. This is a supplementary scheduling audit for
the general supplied-line planar problem. It proves a barrier to two
specific polynomial schedulers; it is not a hardness-of-approximation
result for the identification problem.

## Full-edge priority greedy has deadline dilation approaching two

Let a block be a full-hull edge, querying its two real endpoints. In
block spatial order every positive vertex interval induces an interval
of incident edges, of length at least two. This special expansion does
not improve maximum-remaining-weight greedy to dilation below 3/2.
Its dilation can approach two, even after one forced first block and
even when all positive vertex patterns are singletons or adjacent pairs.

Use k comparison blocks P_i spaced four block positions apart. In
zero-based edge indexing put

    P_i = 4i+1,     i=0,...,k-1,
    g_i = P_i+2,   i=0,...,k-2.

The positive patterns are:

* Each of the two vertices incident to P_i is a singleton pattern,
  with deadline k+2. Its block-hit interval is [P_i-1,P_i] or
  [P_i,P_i+1].
* At gap block g_i, add the two adjacent-vertex patterns whose
  block-hit intervals are [P_i,g_i] and [g_i,P_(i+1)]. Give both
  deadline i+3.

Force an initial edge disjoint from these demands. The comparison
ordering then queries P_0,...,P_(k-1), so it has k+1 blocks and meets
every stated deadline. The later of the two neighboring P blocks has
rank i+3, which pays for the corresponding bridge interval.

Give each deadline level the manuscript's exponential priority weight
M^(r-j), taking M greater than the number of demands plus two. Gap g_0
hits both highest-priority bridge demands, for score twice their
common weight. Every other block hits at most one such demand. Its
total later-level contribution is smaller than one highest-priority
weight. Thus g_0 is the unique greedy choice. Delete its newly hit
demands; the same argument now forces g_1, then g_2, and so on.
The last bridge level is still earlier than the singleton level, so
the strict argument continues through g_(k-2).

Every one of the 2k singleton-positive vertex patterns remains. Each
P_i block hits its own two singleton patterns; every other block hits
at most one. Hence greedy must now select all k blocks P_i. Its total
block count, including the forced first block, is

    1+(k-1)+k = 2k.

The last positive singleton has assigned deadline k+2, giving dilation
2k/(k+2), which tends to two. Relative to the complete comparison
length k+1 the ratio also tends to two. All nonforced chosen edges
have mutually disjoint endpoints, so cached answers do not shrink
the asymptotic query-count obstruction. Pinned endpoint decoding can
reduce an exit's additive work; it cannot repair these discovery ranks.

These are legal planar patterns. Put all query vertices on a regular
(4k+2)-gon, use normalized side tests u dot h > 1, and realize the
singleton and adjacent-pair positive arcs by strict radial hypotheses.
Add normalized midpoints of the P_i hull edges as supplied original
queries and slightly enlarge the radial locations so these midpoint
queries cover their singleton and adjacent-pair hypotheses. Add an
all-zero origin hypothesis and a singleton on the forced edge.
Every supplied cap has bounded cardinality while the hypothesis count
is 4k; count-flatness follows for sufficiently large k. The verifier
checks strict signs and the actual supplied midpoint-query cap sizes.
Strict inequalities permit rational perturbations of all coordinates.

## Exact minimum covers of the current urgent horizon have the same failure

For any j=1,...,k-1, the first j bridge pairs consist of the intervals

    A_i=[P_i,g_i],  B_i=[g_i,P_(i+1)],   i=0,...,j-1.

Their intersection graph is a path on 2j vertices: A_i intersects B_i
only at g_i, and B_i intersects A_(i+1) only at P_(i+1). No candidate
hits three of these intervals. A size-j cover must therefore pair all
2j interval demands. A path with an even number of vertices has a
unique perfect matching, namely (A_0,B_0),...,(A_(j-1),B_(j-1)).
The common point of each such pair is exactly g_i, so the unique
minimum cover is {g_0,...,g_(j-1)}.

An algorithm that queries exact minimum covers of successive urgent
horizons therefore queries all the gap blocks before the late
singleton horizon. At that point it still needs all k comparison
blocks to cover the singleton patterns, again using 2k blocks
overall. Early minimum cardinality is the wrong objective here:
a compatible schedule must deliberately spend
additional early capacity on P blocks to avoid paying for obsolete
gap choices later.

The single chain can be repaired by forcing P_0 immediately after
the initial mandatory block; future-coverage tie effects can then
propagate along the chain. Thus the counterexample does not rule out
additional prefix enumeration or the full manuscript algorithm's
enumeration of first pairs. It establishes the failure of the two
specified scheduler routines for their specified forced prefix. The
generic deadlines also have not been derived from actual recursive
child-height allowances. A polynomial algorithm that optimizes all
horizons jointly, a carefully rounded strengthened LP, or a different
restriction potential remains possible.

## Checks and the remaining route

`python poly-block-greedy-check.py` passed 39 exact integer schedule
checks for k=2,...,40 and 16 strict regular-polygon realizations for
k=5,...,20. At k=40 the block/deadline ratio is 80/42 > 1.90476.

The independent deadline LP counterexample in `poly-deadline-lp.md`
also transfers to full-edge block demands by replacing every spatial
candidate p with two consecutive twins and interval [l,r] with
[2l-1,2r]. Thus the naive feasibility LP is not an exact replacement
for the quasipolynomial grade-vector DP. The promising target is a
polynomial joint-deadline scheduler with quantified dilation strictly
below 3/2, or stronger optimal-tree restriction credit that pays for
its unavoidable delay.
