# Structural routes for planar supplied-line decision trees

Prepared 13 October 2026. This note does not edit the manuscript. Statements marked **derived theorem** have proofs below, but their novelty has not been established. Statements marked **research target** remain conjectural. The model is the manuscript's binary, unit-cost, supplied-line model, with no hypothesis on a supplied line.

## 1. The boundary that the current reduction already settles

The manuscript's hypotheses lie on a parabola and are in strictly convex position. Thus exact polynomial-time algorithms based only on convex position, one convex layer, or constant numbers of convex layers are ruled out unless P=NP. Convex position does not rule out a PTAS; the existing reductions establish small exact gaps, not constant multiplicative gaps.

The original query matrix has affine sign rank at most three: its entries are signs of `(x_h,y_h,1)·(a_l,b_l,c_l)`. This is a representability restriction, not a route to polynomially many recursive states. For convex-position points with singleton queries, missing selected singleton caps can leave every subset as a reachable state. Intersections of arbitrarily many supplied halfplanes therefore have exponentially many distinct traces on the hypotheses, even though one halfplane has low VC dimension. Also, an arbitrary sign-rank-three matrix need not have a planar affine realization with all hypothesis representatives in one affine chart; do not equate these models without a realization argument.

## 2. Exact algorithms when the supplied lines have few directions

**Derived theorem.** If the supplied lines have k distinct unoriented directions, both objectives can be solved exactly in `(m+1)^{O(k)} poly(n, input bits)` time. This is XP in k, polynomial for every fixed k, and not an FPT claim.

For direction j, choose a common normal `a_j`. Its supplied lines are threshold comparisons of `a_j·h`. A transcript retains a lower and an upper threshold in this projection. All weaker same-direction constraints can be discarded. Every nonempty state is consequently the trace of an intersection of k slabs. Enumerate all lower/upper threshold choices, allowing infinite endpoints. There are at most `(m+1)^{2k}` choices. Deduplicate equal hypothesis subsets, order states by size, and apply the manuscript's exact Bellman recurrence. Every splitting query produces another represented slab intersection, and children are strictly smaller.

This gives clean exact baselines for two or three directions. It also suggests a practical hybrid: invoke this DP when a recursive state has few surviving query directions, and use the constant approximation elsewhere. Since replacing a subtree by an exact subtree cannot increase either objective, this is a sound improvement without a new approximation theorem.

For k=1, separability implies distinct projected hypothesis coordinates and a supplied cut between every adjacent pair. The expected objective becomes optimal alphabetic coding; the worst objective equals `ceil(log_2 n)`.

**Research target.** Identify an additional parameter that turns the XP dependence into FPT, such as a bounded number of occupied projection bins or a small exceptional line set. Parameterization by convex layers does not remove the existing hardness.

## 3. Concurrent lines are exactly solvable

**Derived theorem.** If all supplied lines pass through one point p, both objectives are exactly polynomial-time solvable.

No hypothesis equals p because boundary outcomes are excluded. Equal angular directions cannot be separate hypotheses because every concurrent line gives them identical signs. Consider a splitting root line. Each root answer restricts the hypotheses to an open semicircle around p. Order that answer class by angle, using the center of its semicircle as the angular cut. Every other concurrent line changes sign at most once inside this open semicircle: its two boundary rays are antipodal. Its restriction is therefore a threshold query, possibly constant.

Every pair of adjacent hypotheses in this angular order is separated by some supplied line, by global separability. That line's unique threshold is in their adjacent gap. Hence every adjacent threshold needed by any alphabetic tree is available. Solve the two answer classes by interval DP, then optimize over splitting root lines. The raw expected recurrence adds the root mass to both subtree costs; the worst recurrence adds one to the larger subtree height. An `O(m n^3)` implementation already suffices. Coincident or opposite angular directions cause no problem except that equal directions violate separability.

This case is a useful contrast with parabola interval-membership queries: after one concurrent query all later cuts are one-sided thresholds, whereas the complement of an interval cap on a parabola can retain two separated ranges and many gaps.

Novelty has not been checked. The proof is independent of any literature claim.

## 4. A concrete exact control class: uniform singleton/pair queries

Assume a distinguished hypothesis 0 misses every designated cap. Every other hypothesis has a supplied singleton cap, and every remaining cap contains exactly two nonzero hypotheses. Let G be the graph of available pair caps, with N vertices. This statement is combinatorial and applies to arbitrary G when such tests are supplied; it does not assume every G has a planar realization.

**Derived theorem.** Under the uniform prior, a maximum-cardinality matching solves both objectives exactly. Let q be matching size and `r=N-q` the number of exit groups. Their optimal raw total depth is

`F(q) = r + r(r+1)/2 + q(q+1)/2 + 2q`.

To prove this, follow 0's all-miss spine. First-hit groups are singletons or pairs; the pairs form a matching. Query paired groups first because their masses are two, then singleton groups of mass one. Each paired group needs one additional query after its hit. The distinguished point contributes r; the completion sum contributes `r(r+1)/2 + q(q+1)/2`; and pair continuations contribute 2q. Every such schedule is executable using the supplied singleton tests. If `q+1` is feasible,

`F(q+1)-F(q) = 2q-N+2 <= 0`.

All matching sizes up to the maximum are feasible by deleting matching edges, so any maximum matching is optimal. Divide the raw sum by `N+1` for expected depth. The equality case for the last pair when N is even is harmless.

For worst depth, querying pairs first gives

`W(q) = max{N-q, q+1}` for q>0, and `W(0)=N`.

The first term is 0's spine length; the second is the last pair's position plus its continuation. This is nonincreasing over feasible q, including a possible tie at a perfect matching. Equivalently the formula `max{N-q,q+1}` works also at q=0 for N>=1.

The same reduction remains exact if all nonzero hypotheses have the same weight w, while 0 has arbitrary positive weight w0. The raw expected objective becomes

`w0(N-q) + w [r(r+1)/2 + q(q+1)/2 + 2q]`.

Evaluate this for `0<=q<=nu(G)`; there is still a polynomial exact algorithm. Thus skewing only the distinguished hypothesis is insufficient for hardness in this class. The manuscript's expected reduction needs varying nonzero weights; its worst reduction needs cloud continuation heights.

In a planar realization with all nonzero singleton tests available, every nonzero point is a convex-hull vertex. A two-point cap selects adjacent vertices of that hull. Consequently G is a subgraph of a cycle (paths and possibly one cycle); a hull position occupied by 0 can delete an edge. This is stronger than planarity. Without all singleton tests, neither this graph structure nor unrestricted schedule attainability should be asserted.

## 5. A QPTAS for the manuscript's weighted singleton/pair hardness class

**Derived theorem, novelty unestablished.** Expected depth on the weighted singleton/pair linear-forest class admits a `(1+epsilon)` approximation in `n^{O(epsilon^{-1} log(n/epsilon))}` time, polynomial in the original bit length outside this exponent. It extends to a pair graph that is a disjoint union of paths and cycles. This is a QPTAS for fixed epsilon, not a PTAS. The stronger exponent here uses group-mass buckets, suggested by the hardness agent and audited independently; endpoint-pair-type buckets are unnecessary.

The matching invoice in the manuscript is the starting point. For a matching M, let J(M) contain each matched pair mass and each unmatched singleton weight, and let C(J) be the weighted completion sum in nonincreasing order. The objective is

`w0(N-|M|) + C(J(M)) + sum_{uv in M}(wu+wv)`.

Let n=N+1 and let Omega be the **original** total raw weight, including 0. Set `eta=epsilon/3`, with `0<epsilon<=1`, and `tau=eta Omega/n^2`. Keep w0 exact. Raise each nonzero weight below tau to tau, obtaining tilde weights. Every tree has depth at most n-1. Raising weights therefore adds at most

`n tau (n-1) <= eta Omega <= eta OPT_raw`

to its raw cost. The last inequality holds because every hypothesis has depth at least one when n>=2, hence `OPT_raw>=Omega`.

Round each possible **group mass**, rather than each endpoint pair type. For singleton v, set `beta_v=roundup(tilde w_v)`. For each available edge uv, set `beta_uv=roundup(tilde w_u+tilde w_v)`. Round upwards to the next power of `1+eta` times tau. Every possible group mass is between tau and 2Omega, so there are

`L=O(eta^{-1} log(n/eta))`

distinct rounded group-mass buckets, independent of the numerical spread or bit length of the original weights. Keeping weight 0 exact removes any need to assign it a bucket.

Now optimize the bucketed **surrogate**, which need not itself arise from a consistent assignment of rounded vertex weights. For a matching M let `J_beta(M)` contain the bucketed mass of each group and define

`A(M)=w0(N-|M|)+C(J_beta(M))+sum_{uv in M} beta_uv`.

A matching on a path can be generated by leaving the first remaining vertex unmatched or matching it to the next vertex. Maintain two counts for each mass bucket: the number of unmatched singleton groups and the number of matched pair groups. There are `2L` coordinates. A component DP enumerates all attainable count vectors using the precomputed singleton/edge bucket labels. Combine components by count-vector convolution. Every coordinate is at most n, so there are `n^{O(L)}` vectors, and convolutions preserve that asymptotic bound. For every final vector, build its bucketed group masses, sort them, and evaluate A. Backtracking recovers a matching. Order its actual groups by nonincreasing bucketed mass, then use the supplied pair and singleton queries and pair continuations. A cycle is handled by conditioning on whether one chosen cycle edge belongs to the matching; both branches reduce to paths.

This surrogate is sufficient. The actual raw cost of that executable bucket-sorted tree is at most A(M): every actual group mass is at most its bucket label, and every actual pair continuation mass is at most its pair bucket label. The completion sum is coordinatewise monotone and homogeneous. Therefore, for each fixed matching,

`A(M)<= (1+eta) G_tilde(M)`,

where `G_tilde(M)` is the exact matching invoice with raised vertex weights. Keeping w0 unchanged preserves this inequality because all terms are nonnegative. If M' minimizes A and M* is an original optimum matching, then

`C_original(T_{M'}) <= A(M') <= A(M*) <= (1+eta) G_tilde(M*)`

`                         <= (1+eta)^2 OPT_original <= (1+epsilon) OPT_original`.

The raising bound applies to an original optimal tree implementing M*; the optimum raised invoice for M* cannot be larger than that tree's raised cost. This avoids assuming that the best group ordering stays fixed under raising weights.

Use the same original normalization Omega to evaluate the delivered tree, so the expected-depth ratio is identical to this raw-cost ratio. This removes a potential normalization ambiguity.

**Research target.** Remove the log n dependence from the number of essential histogram levels, perhaps using coarse completion-time quantiles rather than multiplicative weight levels. That would turn this QPTAS into a PTAS for a strongly NP-complete geometric subclass. Merely rounding polynomially bounded integer weights does not yield a PTAS: their multiplicative range still needs Theta(log n) levels.

For a fixed number L of exact nonzero weight values, there are only `O(L^2)` exact group masses and the same count-vector DP is polynomial. With bounded numerical spread and fixed epsilon, group-mass rounding also gives a PTAS for that restriction.

## 6. Exact joint endpoint decoding after discovery

**Derived theorem.** After one positive hull vertex v and the manuscript's free geometric cut are known, optimum endpoint decoding can be computed by a two-coordinate rectangle DP.

Every compatible pattern is an interval containing v. Represent its left and right endpoints by their ranks. A hull test left of v compares the left endpoint to a threshold; a hull test right of v compares the right endpoint to a threshold. Every transcript restricts the endpoint pairs to an axis-aligned rectangle in this discrete rank space. The original set of realized endpoint pairs may be sparse and correlated, but there are only `O(|V|^4)` rectangles. Scan splitting supplied hull tests and apply exact DP.

For maximum depth, give a terminal pattern class A its actual recursively constructed continuation height `c_W(T(A))`, rather than zero, and minimize total decoder-plus-continuation height. For expected depth the continuation contribution of a fixed pattern class is paid once regardless of decoding order, so exact weighted decoding suffices. Cached answers restrict the initial rectangle. Pinning and singleton inference arise automatically.

This can replace the sequential left-then-right decoder while preserving polynomial time, and it cannot worsen the constructed tree. It captures correlations that sequential coding ignores.

**Research target.** Prove a universal joint-decoding redundancy bound that improves the manuscript's pointwise `log_2(delta s/|A|)+4` allowance, or improve the expected redundancy enough to affect the final factor. An optimal average-cost decoder by itself gives no pointwise guarantee. Related entropy-sensitive point-location papers allow a richer comparison set, so their bounds cannot be imported without checking every query's availability. The useful next experiment is exact decoding on adversarial correlated endpoint distributions, with continuation heights included for the worst objective.

## 7. Exact halfplane cover is an available primitive, but does not solve the tree

**Verified literature fact.** Minimum-weight cover of planar points by supplied halfplanes is exactly polynomial-time solvable. Har-Peled and Mira Lee prove this in Section 3 of their 2012 Journal of Computational Geometry paper. Wang and Xue's SoCG 2024 paper gives a much faster exact algorithm for the unweighted case. Badanidiyuru, Kleinberg, and Hooyeon Lee's Appendix B explicitly records that adapting the same DP solves maximum budgeted halfplane coverage exactly in dimension two; a weighted-profit adaptation requires checking the DP or giving the additive-profit proof.

For each fixed hypothesis h, orient every line toward the side that excludes h. Cover all other hypotheses by these caps. This computes the shortest certificate for h exactly. It supplies valid lower bounds

`max_h tau(h) <= OPT_W` and `sum_h pi_h tau(h) <= OPT_E`.

Consequently a generic Set Cover reduction attached solely to a heavy distinguished spine cannot establish logarithmic hardness here. Hardness must arise from scheduling, branch continuations, or consistency across many target paths.

**Research target.** Use exact cover or exact maximum budgeted coverage to replace the adjacent-hull support loss. The obstacle is precise: a hull-pattern class is constant on hull vertices but need not be constant on an interior supplied query. First-hit time on original caps is therefore per hypothesis, whereas the current recursive credit needs a common prefix for an entire class. Refining the algorithm's exit by the hull pattern does not make the unknown comparison path constant on that refined class. A valid improvement needs a new partition or a restriction/charging lemma that handles this variability.

Priority cover results are useful evidence that extra demands can retain geometric structure: Banik, Raman, and Ray obtain a PTAS for priority covering by pseudo-halfspaces. However their priority relation does not enforce one query per time slot and all nested deadline prefixes simultaneously. A time-indexed schedule has additional coupling; this is a research lead, not an applicable oracle.

## 8. Priorities and suggested milestones

1. **Immediate rigorous additions:** uniform singleton/pair exact theorem, few-direction/concurrent exact algorithms, and the weighted pair-forest QPTAS. These map the genuine source of hardness and provide exact benchmarks. Novelty checks remain necessary.
2. **Most direct broad algorithm improvement:** joint endpoint-plus-continuation DP. Implement it as a baseline, then search for a better global redundancy/charging theorem. A universal improvement in the current factor is not established here.
3. **Higher-risk broad approximation route:** original-cap maximum coverage plus a new classwise prefix lemma. Exact geometric coverage is stronger than the interval surrogate, but replacing it mechanically is invalid.
4. **Focused complexity question:** does the weighted pair-forest class have a PTAS, or is it APX-hard? Its QPTAS and the existing strong NP-hardness are consistent. A claim of APX-hardness needs a constant gap, not the existing 3-Partition exact gap.
5. **Uniform hardness question:** construct hardness with caps larger than two or with nontrivial continuation branches. Uniform bare singleton/pair instances cannot provide it. Weight cloning must account for the additional legal separating queries and internal clone costs; it is not a black-box transfer.

## Verification and primary references

`structural-route-checks.py` compares the derived formulas against exact subset Bellman optimization. It checked all 1,099 graphs on 1–5 nonzero vertices, with four distinguished-point priors each (4,396 expected/worst comparisons), and 276 randomly generated separable concurrent-line instances with arbitrary positive weights. It also checked the stronger group-bucket surrogate on 2,000 random weighted forests, using exact rational arithmetic, weights spanning up to eight decimal orders, and three rounding precisions. For every feasible matching it checked that the bucket-sorted actual tree costs at most its surrogate and that the surrogate is at most `(1+eta)` times the raised matching invoice; identical 2L-dimensional histograms gave identical surrogates. The surrogate minimizer obeyed the proved `(1+eta)^2` ratio on every case. These are consistency checks, not substitutes for the proofs.

- [Har-Peled and Mira Lee, Weighted geometric set cover problems revisited, JoCG 2012](https://jocg.org/index.php/jocg/article/view/2950): exact weighted planar halfplane cover.
- [Wang and Xue, Algorithms for Halfplane Coverage and Related Problems, SoCG 2024](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.SoCG.2024.79): faster exact unweighted cover.
- [Badanidiyuru, Kleinberg, and Hooyeon Lee, Approximating Low-Dimensional Coverage Problems](https://arxiv.org/html/1112.0689): Appendix B's exact two-dimensional maximum-coverage observation and analysis of greedy.
- [Banik, Raman, and Ray, On Geometric Priority Set Cover Problems, ISAAC 2021](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.ISAAC.2021.12): priority pseudo-halfspace PTAS; query-time slot coupling remains outside this statement.
- [Arya, Malamatos, Mount, and Wong, Optimal Expected-Case Planar Point Location, SIAM J. Comput. 2007](https://epubs.siam.org/doi/abs/10.1137/S0097539704446724): entropy-sensitive point location background; richer allowed comparisons are a material model difference.

## 9. Peer audit of the new quasipolynomial maximum-depth route

The coordinating agent proposed replacing priority greedy by exact feasibility for geometrically rounded nested interval deadlines. I audited the following algebra and found no issue; a full standalone theorem still needs the algorithm, its state transitions, and bit-complexity details written out.

Take `lambda=1+epsilon`, `a=2 lambda`, and the invariant `H(S)<=floor(a D(S)+gamma log_2 |S|)`. Let `L=log_2(1/delta)`, and require `gamma log_2(1/(1-delta))>=1`, `gamma L>=a+4`, and `gamma>=1`. For a class with comparison support-block first hit t and `x=log_2(s/|A|)>L`, its residual discovery budget satisfies

`B_A >= floor(a(t-1)+gamma x)-floor(x-L)-4`

`     >= floor(a(t-1)+(gamma-1)x+L)-4 >= floor(a t)`.

The first inequality uses the existing classwise supporting-prefix credit and the unpinned endpoint allowance. The next uses `floor u-floor v>=floor(u-v)`. The last uses `gamma L>=a+4`.

Round B down to the largest value `hat B=floor(lambda^j)<=B`. Since the next floor exceeds B,

`hat B > (B+1)/lambda-1 > 2t-1`,

hence integer `hat B>=2t`. An optimum support-block sequence, expanded into individual vertices, hits each class by time 2t. Enumerate its first vertex v, force that query, remove classes positive there, and cut the remaining circular intervals at v.

With r distinct rounded deadlines, exact feasibility can scan the ordinary candidate order. Store a selected-count vector and the last selected position for every prefix of grades. Selecting a candidate at grade j updates the last position and count for every grade prefix at least j. When a demand interval's right endpoint passes, its deadline prefix must have a selected position at least its left endpoint. Impose prefix counts at most `hat B-1` for the remaining choices, because the forced vertex already consumed one query. Impose total selected count at most `H-1` as well. Grade order yields an executable schedule. The state space is `(mn)^{O(r)}`, where `r=O(log n/epsilon)`.

The total-count constraint has a valid comparator. If the zero pattern exists, all support queries fit within 2D. If the witness terminal leaf has a nonzero pattern, append one positive vertex, giving at most 2D+1 choices. The trial height `floor(aD+gamma log_2 s)` is at least 2D+1 for s>=2, since a>=2 and the balanced-query condition forces gamma>1 for delta<1/3. Thus the appendix query does not break feasibility. Each positive exit obeys its residual budget; the all-zero route obeys the total count.

At epsilon tending to zero the parameter balance is `delta=(1-delta)^6`, with `delta≈0.2219104`, `gamma≈2.7624935`, and limiting ratio `2+gamma≈4.7624935`. This is a quasipolynomial route, not a polynomial-time improvement. It uses the existing supplied hull queries and classwise credit, so the original-cap class-constancy obstacle from Section 7 does not apply.
