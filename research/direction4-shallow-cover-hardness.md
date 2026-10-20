# Direction 4: shallow ordered halfplane cover and approximation hardness

Research audit, 13 October 2026. The model is identification of finite rational planar points by a supplied separating family of binary line-side queries, with unit query costs. This report distinguishes derived theorems from unresolved source hardness. It does not claim novelty established by an exhaustive literature review.

The main new result is algorithmic: **maximum depth is exactly polynomial-time solvable when every query's side opposite a common supplied witness contains at most a fixed number b of hypotheses**. The proposed shallow-cover hardness route therefore belongs to expected depth. A strengthened conditional transfer would establish **uniform-prior** expected-depth hardness if the appropriate ordered geometric source can be shown gap-hard.

## 1. The precise source problem

There are N planar source points P, a rational point p outside every supplied open cap, and m supplied caps A_i = P intersect H_i, each of cardinality at most b. No point or p lies on a supplied boundary. The caps cover P, and their incidence signatures separate all points in P. Thus P union {p} is a valid identification instance.

Order the caps, removing queries that cover no previously uncovered point. If tau(x) is the first position covering x, minimize

\[
 F=\sum_{x\in P}\tau(x).
\]

Every useful ordering has at most N queries. The geometric assumptions are part of the source, not consequences of an arbitrary three-element incidence table.

For fixed b, a gap-hardness theorem for this source is **unproved here**. Searches of primary papers did not identify a theorem giving APX hardness for this exact shallow, common-witness planar halfplane source.

## 2. Proved: bounded-cap maximum depth is exactly tractable

Let K be the minimum number of supplied caps covering P. Exact minimum-weight cover of planar points by supplied halfplanes is polynomial-time solvable; taking unit weights gives K and a cover. This is the only nontrivial geometric oracle needed below. [Har-Peled and Lee, Section 3](https://jocg.org/index.php/jocg/article/download/2950/2644/7396).

Following p through any identification tree produces a cover, so OPT_W >= K. Querying a minimum cover along the miss spine, and identifying every first-hit group locally, gives

\[
 K\le\mathrm{OPT}_{\mathrm W}\le K+b-1.
\]

The local bound follows from separation: any group of at most b points has a proper identifying tree of height at most b-1 using the original supplied queries. This already gives a polynomial approximation scheme, since K >= N/b. The following suffix argument strengthens it to an exact algorithm for fixed b.

**Theorem.** Maximum depth can be optimized in

\[
 m^{O(b)}2^{O(b^2)}\operatorname{poly}(N,m,L)
\]

time in this class, where L is the coordinate and coefficient encoding length. Thus the algorithm is XP in b and polynomial for each fixed b; it is not an FPT claim.

**Proof.** For each integer D from K through K+b-1, set

\[
 d_0=\max\{0,D-b+1\},\qquad t=D-d_0\le b-1.
\]

Enumerate an ordered suffix of at most t supplied caps, and a set R contained in their union. Its size is at most b(b-1). Think of R as the source points still present immediately before that suffix; p is also present.

For a suffix A_1,...,A_l, define its first-hit groups on R by

\[
 B_j=(R\setminus\bigcup_{i<j}A_i)\cap A_j.
\]

Reject if the suffix does not cover R. Nonproductive suffix queries can be omitted. For each nonempty B_j, compute its exact local optimum height h(B_j) by ordinary subset Bellman DP on at most b points, using every original supplied query. Require

\[
 \ell\le t,\qquad j+h(B_j)\le t\quad\text{for every }j.
\]

Now filter the original caps to those disjoint from R. Use the exact halfplane-cover oracle to cover P minus R with at most d_0 filtered caps. If this is possible, the target D is feasible.

For soundness, use that cover as a prefix of length k_0 <= d_0. It leaves exactly R on p's spine because its caps avoid R. Every prefix exit contains at most b hypotheses and therefore has total depth at most k_0+b-1 <= D when d_0>0. If d_0=0 the prefix is empty. Append the guessed suffix and its exact local codes: its relative height is at most t, so its absolute height is at most k_0+t <= D. No padding queries are required when the prefix is shorter than d_0.

For completeness, take any tree of height at most D and let q <= D be its p-spine length. If q < d_0, choose the empty suffix and R empty; the spine itself is a cover of size at most d_0. Otherwise retain its first d_0 spine queries as the prefix, let R be the then-uncovered points, and take the remaining q-d_0 queries as the suffix. This suffix has at most t <= b-1 queries, and R is contained in its union. Every prefix cap avoids R and the prefix covers P minus R. Every original positive subtree identifies its first-hit group, so replacing it by an exact local code cannot violate the suffix bounds. The enumeration consequently accepts this guess.

There are at most sum_{l=0}^{b-1} m^l suffixes, at most 2^{b(b-1)} candidate remaining sets per suffix, b target depths, and polynomial work per geometric cover call. Local height tables take m 2^{O(b)} polynomial work. Return the first feasible D. QED.

**Sharper local parameter.** Precompute c = max_i h(A_i), where h is the exact optimum on a full supplied cap. Restricting an optimal cap tree shows h(B) <= c for every possible first-hit subgroup B of that cap. Therefore every occurrence of b-1 in the suffix proof can be replaced by c: the target range is K through K+c, the suffix has at most c queries, and its remaining set has at most bc points. The enumeration then takes m^{O(c)} 2^{O(bc)} polynomial work, in addition to the m 2^{O(b)} local-code precomputation. This helps when available queries identify cap branches in substantially fewer than b-1 steps.

**Consequence.** Caps of size three, or any other fixed size, cannot yield NP hardness of maximum-depth optimization in this common-witness model unless P=NP. They cannot yield APX hardness for height either. Larger caps, multiple witnesses without a common shallow side, or a different architecture are needed for height hardness.

## 3. Proved: the expected-depth transfer can use a uniform prior

Give every source point and p raw weight one. Let G(T) be the raw sum of all N+1 leaf depths; the normalized expected cost is G(T)/(N+1).

Following p in any tree gives a cover ordering. The first-cover depth of a source point is no greater than its complete leaf depth, so

\[
 F^*\le G^*.
\]

Conversely, an optimum useful cover ordering has k <= N queries. Its first-hit groups have size at most b. Attach a local identifying tree of height at most b-1 to every hit, and leave p at the end of the miss spine. This adds at most (b-1)N to the source depths and k <= N for p. Therefore

\[
 \boxed{F^*\le G^*\le F^*+bN.}
\]

Each query first covers at most b points. Consequently

\[
 F^*\ge\sum_{i=1}^N\left\lceil\frac{i}{b}\right\rceil
 \ge\frac{N^2}{2b},
\qquad
 G^*\le\left(1+\frac{2b^2}{N}\right)F^*.
\]

A returned tree can be converted to its witness-spine cover in polynomial time and F(output) <= G(output). Thus a PTAS for **uniform-prior expected-depth trees** would give a PTAS for this ordered source: for desired epsilon <=1, use tree accuracy epsilon/3 when N >= 6b^2/epsilon. Both distortions are at most epsilon/3, and (1+epsilon/3)^2 <= 1+epsilon. For smaller N, exact source subset DP takes 2^{O(b^2/epsilon)} polynomial work.

Equivalently, a source fixed gap rho>1 transfers to any smaller fixed ratio rho'>1 on sufficiently large instances. Under a source yes threshold L, the tree yes bound is L+bN and the no bound is rho L, with ratio at least rho/(1+2b^2/N). No large distinguished weight, denominator amplification, or replication of weighted hypotheses is necessary.

**Status.** The transfer theorem is proved. Its geometric source hardness is not. In particular it does not currently prove uniform-prior NP hardness or APX hardness for the tree problem.

## 4. Proved: cap size two is exact even without all singleton tests

This strengthens the earlier singleton/pair observation. Only coverage and separation are required; private singleton tests need not exist.

Build a graph whose vertices are the N source points and whose edges are the supplied two-point caps. Let r be a maximum-cardinality matching size and k=N-r.

Query the r disjoint matching caps first. Every unmatched point has some cap covering it. A two-point cap cannot contain two unmatched points, since the matching is maximal; hence after the matching queries any cap covering an unmatched point hits only that remaining point. Query those points one at a time. Each paired exit can be identified in one query because the full supplied family separates its two points.

The resulting maximum depth is

\[
 H=\max\{N-r,r+1\}
\]

when r>0, and H=N when r=0. Any tree's first-covered pairs form a matching, its spine has at least N-r queries, and its last pair exit is at position at least r and needs another query. The same bound is therefore optimal.

For uniform expected depth, any matching of size r gives r first-hit groups of mass 2 and N-2r of mass 1. The optimal order puts all pairs first. The ordered-cover and raw tree invoices are respectively

\[
 F(r)=\frac{(N-r)(N-r+1)+r(r+1)}2,
\]

\[
 G(r)=\frac{N(N+3)}2-(N-1)r+r^2.
\]

F strictly decreases with successive feasible r. G decreases or ties, since G(r+1)-G(r)=2r-N+2 <=0. A maximum matching therefore solves uniform ordered cover, uniform expected identification, and height. This argument actually applies to arbitrary abstract membership caps of size at most two; geometry is unnecessary for this exact uniform result.

For unequal weights, ordering unmatched singleton exits can be constrained by the absence of singleton queries, so the unrestricted sorted weighted invoice is not justified by this argument.

## 5. Proved geometric restriction: at most b convex layers

Peel the convex hull repeatedly, removing every boundary point in each layer. If a point x lies in layer d, every strict halfplane containing x contains at least d points of P.

To see this, write the halfplane as a dot product exceeding a threshold. For every earlier layer, x belongs to the convex hull enclosed by that layer. Some point of that layer has dot product at least that of x and hence also belongs to the halfplane. These d-1 earlier points and x are distinct.

Since every source point is covered by a cap of size at most b, every point has convex depth at most b. Cap size three therefore forces at most three convex layers. This is a necessary restriction on a geometric source reduction, and a potential avenue for an algorithm using a constant number of circular orders.

If all source singleton caps are supplied, every source point is exposed on the hull. Then the points are in convex position and all halfplane caps are circular intervals. Caps of bounded cardinality have bounded interval length. This further narrows which sources are available.

Finite layers alone do not prove bounded treewidth of the co-cap graph or a PTAS for ordered cover. A graph-power or planar-support argument can fail around high-degree vertices, and such a structural theorem must be proved rather than assumed.

## 6. What the literature does and does not supply

General MSSC is hard below factor 4, and min-sum vertex cover has a fixed gap above one; the latter proof starts from bounded-degree vertex cover and adds isolated-edge padding. These are abstract incidence families, and neither result supplies our planar cap realization. [Feige, Lovasz and Tetali, Section 5](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf).

The exact halfplane-cover result blocks a dominant-witness reduction whose entire cost is the witness's shortest certificate. Its maximum-coverage adaptation also obstructs treating ordinary maximum coverage by planar halfplanes as a hard source. [Badanidiyuru, Kleinberg and Lee, Appendix B](https://arxiv.org/html/1112.0689).

An ordered objective can still be hard even when each fixed-budget unordered cover is tractable: one needs one nested sequence of prefixes, rather than independently optimal solutions for each budget. That distinction is the remaining opportunity. It is not a proof of hardness.

## 7. Hardness targets compatible with the new general algorithms

The new broad quasipolynomial (2+epsilon) algorithms place a precise limit on fixed-gap hardness arguments. Under ETH, no polynomial-size reduction from 3-SAT can establish a fixed gap rho>2 for either objective: choose a fixed epsilon with 2+epsilon<rho and compose the reduction with the quasipolynomial algorithm. An input with v variables produces size v^{O(1)}, so the resulting SAT algorithm runs in exp(polylog v)=2^{o(v)}, contrary to ETH.

This does not exclude a fixed gap 1<rho<=2. It also does not turn P!=NP alone into a ban on quasipolynomial algorithms. For the weighted pair subclass with a QPTAS, the same ETH argument obstructs every fixed gap above one, but that observation concerns that subclass.

The existing hardness does yield the manuscript-ready **no FPTAS** conclusion. Maximum depth is integral and at most n-1; accuracy 1/[2(n-1)] would recover an exact optimum. On the expected-depth hard restriction, polynomially bounded positive integer raw weights have total Omega polynomial in n, and raw cost is integral and at most Omega(n-1). Accuracy 1/[2 Omega(n-1)] would again recover the exact optimum in polynomial time. This excludes an FPTAS, not a PTAS; the expected conclusion does not establish uniform hardness.

## 8. Recommended next attacks

1. Focus the shallow capsize-three source on **uniform expected depth**. The strengthened transfer gives a clean final target, and the new exact height algorithm removes an unproductive branch of the project.
2. Work directly with rational configurations on two or three convex layers. Enumerate realized shallow caps, then search for a local choice whose latency penalty survives arbitrary query order. Record every sign; arbitrary bounded-occurrence test tables are insufficient.
3. Test whether ordered cover on constant convex layers admits a polynomial approximation scheme. A constant-layer scheduling DP or a geometric decomposition would be a positive result and would rule out this hardness route under P!=NP.
4. If there is a usable geometric source gap, keep the uniform witness and use the additive bN transfer. Avoid a huge witness baseline and avoid replacing probability weights by ordinary copies.
5. For general height hardness, use unbounded caps or several interacting witnesses, with serialized penalties comparable to the yes-instance height. Shallow single-witness caps cannot work because their exact algorithm is now established.

## 9. Independent finite checks

`direction4-shallow-cover-check.py` compares the suffix algorithm using an exact subset-cover oracle with full exact identification Bellman DP on random abstract separating cap systems of size at most one, two, or three. The oracle model tests a stronger combinatorial claim than the geometric instance class; the polynomial-time geometric cover implementation is external to the script.

The checks passed on **418 systems** for exact maximum depth and the uniform transfer inequalities, including systems without a full singleton supply. On **277 size-at-most-two systems**, the script also checked the ordered-cover matching formula, raw uniform tree invoice, and height formula against exact DP.

These finite checks support the derivations and do not replace the proofs above. No new fixed-factor inapproximability theorem is claimed.
