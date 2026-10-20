# A polynomial general maximum-depth improvement: 4.46496526

This report establishes a new algorithm, rather than a barrier. The exact
joint interval-deadline problem admits a dynamic program exponential only in
the total number of available schedule ranks. A global logarithmic rank cap
and the existing priority-greedy fallback make the resulting identification
algorithm polynomial on **all** instances.

The bound is

\[
 C_W(S)\le 4.46496526\,\operatorname{OPT}_W(S).
\]

The manuscript's existing rational parameters are sufficient:
\(\delta=245122334/10^9\), \(\gamma=246496526/10^8\). In particular,
\(\gamma\log_2(1/(1-\delta))>1\) and
\(\gamma\log_2(1/\delta)>5\). The algorithm remains deterministic and uses
only supplied binary line queries.

## Exact scheduling in O(poly(M,N) 3^L) time

There are candidates \(1,\ldots,M\), interval demands \([a,b]\), integer
deadlines \(d_{[a,b]}\), and a total schedule cap \(L\). A demand must have
a selected point in its first \(d_{[a,b]}\) ranks. Empty or repeated queries
can be deleted, so selected points are distinct.

For a spatial region \([l,r]\), let \(\mathcal I(l,r)\) be all original
demands contained entirely in that region. For a subset
\(T\subseteq\{1,\ldots,L\}\), define \(F(l,r,T)\) to mean that the demands
in \(\mathcal I(l,r)\) can be hit by points in \([l,r]\) assigned distinct
absolute ranks from \(T\), respecting every deadline. Unused ranks are
allowed.

If \(\mathcal I(l,r)\) is empty, the state is true for every \(T\). If it
is nonempty and \(T\) is empty, the state is false. Otherwise set
\(t=\min T\). If any contained demand has deadline less than \(t\), reject.
For every \(p\in[l,r]\), and every partition
\(T\setminus\{t\}=T_L\mathbin{\dot\cup}T_R\), test

\[
 F(l,p-1,T_L)\quad\text{and}\quad F(p+1,r,T_R).
\]

The state is true if any such pair passes. The point \(p\) is scheduled at
rank \(t\), and it hits every contained interval that contains \(p\).
Every other interval lies entirely in exactly one of the two child regions.

The use of the earliest available rank is without loss: if a feasible
solution's first selected rank is later, move that query to \(\min T\).
This only accelerates hits. The selected points and their ranks form a
spatial Cartesian tree: the earliest point is the root, and its left and
right selected points form the two subtrees. Conversely, every feasible
schedule yields this recursion. An interval hit by an ancestor need never
be retained below it; precisely the original intervals wholly inside a
current region survive. Thus the recurrence is exact, including arbitrary
unequal deadlines.

Precompute whether each region has any demand and its minimum deadline in
\(O(NM^2)\) time. There are \(O(M^2 2^L)\) states. Summing the rank
partitions over all masks gives
\(\sum_T 2^{|T|}=3^L\), so the transition time is
\(O(M^3 3^L)\). Witness reconstruction orders the selected points by their
ranks. Removing unused ranks accelerates every first hit.

For circular intervals, enumerate the first selected candidate, remove
demands containing it, cut the remaining circle there, subtract one from
the remaining deadlines, and use \(L-1\) available ranks. The total time
has one additional factor \(M\). A deadline-one interval not containing
the forced first point makes that trial infeasible.

This is distinct from assuming integrality of the natural time-indexed LP.
The known six-candidate, five-slot fractional-only obstruction is correctly
rejected by the new DP. The earlier grade-vector DP has a different
parameterization and does not imply this rank-subset bound.

## Hybrid identification algorithm

Let \(n\) be the **original instance size**, not the current state's size.
Put

\[
 q=\lceil\log_2 n\rceil,\qquad L=2q+1.
\]

At singleton and count-balanced states, use the existing algorithm. At a
count-flat state, build the recursive **hybrid** code for every hull-pattern
class once and retain its actual height \(C_W(A)\). This keeps the same
disjoint-child recursion as the manuscript; alternative schedules do not
create overlapping recursive calls.

For every trial height \(H\), try both the existing priority-greedy
construction and the following capped exact construction. Select the least
passing trial over both constructions.

Use edges of the full normalized hull as adjacent blocks, including edges
incident to the origin when it is a hull vertex. The origin is a free
known-negative marker. A nonzero positive-vertex arc meets a circular
interval of these block candidates. Set

\[
 z_A=\lfloor\log_2(\delta s/|A|)\rfloor,\qquad
 B_A=\left\lfloor\frac{H-C_W(A)-z_A-5}{2}\right\rfloor.
\]

Reject a capped trial if any \(B_A<0\). Give class \(A\) its **unrounded**
block-rank deadline \(B_A+1\). Cap the total block count at
\(\min\{L,\lfloor H/2\rfloor\}\), rejecting a nonempty demand family
if this cap is zero. Enumerate its first block, remove its
hit demands, cut there, and run the rank-subset DP with the residual rank
cap and deadlines decreased by one. There is no geometric grade rounding
and no factor \(\lambda>1\).

Execute the selected blocks, skipping cached endpoint queries. The
manuscript's adjacent-block exit allowance is

\[
 2(k-1)+z_A+5+C_W(A)
\]

when \(A\) first meets block \(k\). Hence every passing positive exit fits
\(H\). The total-cap constraint pays for the all-negative route:
at most \(2\lfloor H/2\rfloor\le H\) actual supplied queries. It identifies
the zero singleton when present. If no zero class exists, the infeasible
all-negative leaf is omitted. Origin edges, cached answers, singleton
inference, and low-dimensional hulls only shorten the code.

It suffices to try the same height range as the old polynomial algorithm,
through \(\lfloor(3+\gamma)(s-1)\rfloor\), since the priority option always
has a passing trial. Construct each class code once; only its discovery
schedule and endpoint exits vary between trials.

## Two simultaneous inductive guarantees

The hybrid obeys the old universal invariant

\[
 C_W(S)\le3D+\lfloor\gamma\log_2s\rfloor,
 \qquad D=\operatorname{OPT}_W(S).
\]

The existing priority-greedy proof remains valid with hybrid child codes:
by induction their actual heights satisfy the same universal bound, and
the algorithm can choose its passing priority trial. Balanced states use
the same count-potential decrease.

There is also the restricted invariant

\[
 D\le2q\quad\Longrightarrow\quad
 C_W(S)\le2D+\lfloor\gamma\log_2s\rfloor.
\]

The global threshold \(2q\) is crucial. Restriction of the optimal tree
gives \(\operatorname{OPT}_W(A)\le D\), so **every child** of a state
meeting this threshold meets the very same threshold. Induction may
therefore use the stronger coefficient two on all its children, even if
their own cardinalities are much smaller than \(n\).

In a flat state, let \(t=t_A\), \(x=\log_2(s/|A|)\), and
\(\ell=\log_2(1/\delta)\). The supporting-prefix lemma gives
\(\operatorname{OPT}_W(A)\le D-(t-1)\). At
\(H^*=2D+\lfloor\gamma\log_2s\rfloor\), the stronger child bound yields

\[
\begin{aligned}
 H^*-C_W(A)-z_A-5
 &\ge 2(t-1)+\lfloor\gamma x\rfloor-\lfloor x-\ell\rfloor-5\\
 &\ge 2(t-1).
\end{aligned}
\]

The last inequality is exactly the manuscript's integer potential credit,
using \(x>\ell\), \(\gamma\ge1\), and \(\gamma\ell>5\). Thus
\(B_A\ge t_A-1\), and the comparison support blocks meet every deadline.
Padding singleton supports to incident full-hull edges can only accelerate
hits. The witness path has at most \(D\) blocks if the zero pattern is
present, and at most \(D+1\) otherwise, because an uncovered terminal
nonzero singleton may need an appended incident edge. Therefore its total
count fits \(L=2q+1\).

For \(s\ge2\), \(\lfloor\gamma\log_2s\rfloor\ge2\), so
\(\lfloor H^*/2\rfloor\ge D+1\) as well. The comparison therefore meets
**both** total caps. Enumerating its first block and using exact deadline
feasibility proves that trial \(H^*\) passes. Balanced states again use the
one-unit count-potential drop, with coefficient two. This establishes the
restricted invariant without assuming that the algorithm knows \(D\).

## General approximation ratio and polynomial time

For the original instance, if \(D\le2q\), the restricted invariant and
\(D\ge\log_2n\) give

\[
 C_W\le(2+\gamma)D=4.46496526D.
\]

If \(D>2q\), the universal invariant gives

\[
 \frac{C_W}{D}\le3+\frac{\gamma\log_2n}{D}
 <3+\frac{\gamma}{2}=4.23248263<4.46496526.
\]

These cases exhaust every general instance. The algorithm uses no optimum
depth as input. The logarithmic cap is fixed from the original \(n\).

Since \(3^L\le27n^{2\log_2 3}\), every exact scheduling call is polynomial.
There are at most \(n-1\) nonterminal recursive stages, polynomially many
trial heights and first blocks, and polynomial-bit geometry and endpoint
codes. A simple upper bound for all capped scheduling calls is
\(O(n^2M^4 3^L)\), before other polynomial bookkeeping factors. The state
memory is \(O(M^2 2^L)=O(M^2n^2)\). The resulting proper output tree has
at most \(n\) leaves and \(n-1\) internal nodes.

More generally, \(L=\lceil K\log_2n\rceil+1\) for fixed \(K>0\) gives
factor \(\max\{2+\gamma,3+\gamma/K\}\), apart from harmless upward
rounding. Any \(K\ge\gamma/(\gamma-1)\approx1.6827\) reaches the stated
bound; \(K=2\) makes the proof and cap integral without numerical tuning.

## Verification and further routes

`further-worst-slot-dp-check.py` independently compares the Cartesian DP
with exact subset-permutation DPs on 3,900 linear and 1,200 circular random
and targeted instances. The dense targeted families impose every interval's
exact first-hit deadline from a random schedule, exercising compatible
prefixes and varied Cartesian tree shapes. It also checks the prior
fractional-only five-slot obstruction and its six-slot repair. All tests
pass under standard-library Python.

The earlier forced-prefix greedy counterexamples remain correct, but they
do not obstruct this algorithm: the DP chooses a globally compatible order
within its logarithmic cap rather than committing to a local urgent choice.
No transfer of arbitrary synthetic deadlines to actual child allowances is
needed for the new theorem; feasibility is proved directly from the real
supporting-prefix witness and the actual recursive code heights.

## A further polynomial extension: optimize entire positive exits

The following is a concrete algorithmic extension of the capped DP. It can
improve its actual output heights while preserving the proved constant.
It does not yet give a smaller uniform approximation factor.

After a positive vertex answer, encode each compatible pattern by its
ordered endpoint pair \((a_A,b_A)\). With the known positive anchor and
the manuscript's geometric cut, a hull query on one side tests a threshold
of \(a_A\); a query on the other side tests a threshold of \(b_A\).
Every subsequent compatible pattern set is a rectangle in these two
ordered endpoint coordinates. The class is unique at each endpoint pair.

Give leaf \(A\) terminal height equal to its stored actual child height
\(C_W(A)\). For a coordinate rectangle \(R\), set

\[
 E(R)=\min_{\text{proper coordinate thresholds }q}
       \left(1+\max\{E(R\cap q^-),E(R\cap q^+)\}\right),
\]

with \(E(R)=C_W(A)\) for a rectangle containing only class \(A\), and
empty rectangles discarded. Each split is a supplied hull query. There
are \(O(M^4)\) rectangles and \(O(M)\) threshold transitions each, so
this exact minimax decoder is polynomial. A second-endpoint positive exit
has one endpoint pinned and is the one-coordinate special case.

At a Cartesian scheduling state with spatial region \([l,r]\), all unhit
classes are exactly those whose block-hit intervals are contained in that
region. For candidate block \(p\) and either orientation, divide its hit
classes into those positive on the first endpoint and those negative on
the first but positive on the second. For each cell obtain the exact
endpoint decoder's **whole** height, including its terminal class code:
\(E_1(l,r,p)\) and \(E_2(l,r,p)\). The region's ancestor-negative blocks
give rectangular endpoint restrictions, so these values depend on the
region and chosen block, rather than the entire earlier block permutation.

If the candidate is at absolute block rank \(k\), require

\[
 2(k-1)+1+E_1(l,r,p)\le H,\qquad
 2k+E_2(l,r,p)\le H,
\]

omitting a check when its cell is empty. For origin edges or cached
endpoints the same upper bounds are conservative. Then partition the
remaining ranks between the strictly left and right unhit demands as
before. The rank-subset recurrence, first-block circular cut, total cap,
and all-negative-route check are unchanged. The positive-exit tests now
replace the individual fixed deadlines. Either orientation may be tried.

This DP is exact for these conservative two-queries-per-block prefix
bounds and the optimal coordinate-threshold endpoint decoders. Its
precomputation and transition count are polynomial times \(3^L\). Every
schedule passing the earlier fixed-allowance DP also passes this extension:
the explicit dyadic endpoint codes already provide legal decoders meeting
all the earlier per-class exit bounds, and the new minimax decoder can only
improve their largest complete height. Thus the 4.46496526 guarantee is
retained, and actual trial heights may decrease.

`further-worst-endpoint-check.py` compares the rectangle recurrence with
unrestricted complete subset decision-tree recursion on 1,200 weighted
endpoint instances. All agree. It also verifies a cautionary weighted
cross: the central pattern has child height 10, its four axis neighbors
have height zero, and every decoder needs height 14. The center requires
four endpoint comparisons. Consequently an aggregate endpoint weight
\(\sum_A2^{C_W(A)}\) does **not** by itself justify replacing the universal
four-query overhead by two or three. This is an endpoint-decoder barrier,
not a lower bound for the whole planar identification algorithm, which can
choose a different discovery anchor.

Three additional avenues remain useful:

1. To prove a smaller constant using whole-exit optimization, one must
   jointly exploit the chosen anchor and the child-height distribution.
   A large difficult class may be pinned by choosing a boundary block,
   but the proof must still pay for all other classes' compatible ranks.
   An independent per-budget cover or an endpoint-only aggregate bound
   does not establish that compatibility.
2. A natural time-indexed LP remains nonintegral; its known gap is 6/5.
   A stronger LP or a below-3/2 rounding theorem is still interesting when
   unrestricted discovery lengths are needed. It is no longer necessary
   for the polynomial 4.46496526 result.
3. The cap-and-fallback argument does **not** immediately transfer to
   arbitrary-prior expected depth. A witness path can be long while the
   optimum expected cost is small. Truncating rare long paths would require
   a probability-weighted argument that pays both zero-route waiting and
   all residual continuation costs.

The primary literature result for Priority Line Cover is exact polynomial
optimization, but it concerns choosing priority-bearing covering segments
over demand points. Our problem chooses stabbing points with globally
ordered rank capacities. No unproved reduction between these orientations
is used. Source: [Chakrabarty, Grant, and Könemann, *On Column-restricted
and Priority Covering Integer Programs*](https://arxiv.org/abs/1003.1507).
