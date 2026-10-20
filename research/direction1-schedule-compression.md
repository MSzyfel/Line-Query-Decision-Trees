# Direction 1: schedule compression and stronger quasipolynomial constants

13 October 2026. This report develops the nested interval scheduling route. It uses the manuscript's common-witness geometry, supporting-prefix restriction credit, and endpoint-code lemmas. The new scheduling and rounding arguments are self-contained below; the prerequisite geometry has not received a complete manuscript-wide audit.

## Main result

**Stronger derived theorem (final route): both maximum depth and arbitrary-prior expected depth admit deterministic quasipolynomial \((2+\varepsilon)\)-approximations for every fixed \(\varepsilon>0\).** An \(O(\log n)\)-query root rollout removes the logarithmic or entropy potential from the adjacent-block baseline's final ratio. Section 7 gives this generic argument in full. Direction 3 independently found the bounded-optimum-height route for maximum depth; the root-rollout lemma below also handles expected depth and does not require a positive lower bound on priors.

The intermediate smaller constants remain useful because they describe the baseline and make its leading coefficient explicit.

**Derived theorem:** adjacent-block discovery, with query ranks rounded after subtracting the first block, gives a deterministic quasipolynomial maximum-depth approximation below **4.464966**. Its limiting factor approaches

\[
2+\frac{1}{\log_2(1/(1-\delta_*))}
=4.464965255473\ldots,
\qquad \delta_*=(1-\delta_*)^5.
\]

The previous quasipolynomial route attained 4.764 and approached 4.76249351. The improvement comes from scheduling adjacent support blocks and charging a second-query positive exit's cached negative neighbor. The shifted grades then eliminate the rounding loss on the first block.

An explicit certified choice is

\[
\lambda=\frac{10000001}{10000000},\quad
a=2\lambda,\quad
\delta=\frac{245122334}{10^9},\quad
\gamma=\frac{246496526}{10^8}.
\]

The resulting factor is **4.46496546 < 4.464966**. A less finely graded alternative, \(\lambda=2001/2000\), gives **4.46596526 < 4.466** with exactly the same balance parameters. These are quasipolynomial theorems, not polynomial-time leading constants.

Direction 2 independently supplied shifted block grades for expected depth. Combining them with the same block construction gives a stage bound

\[
W_{\rm stage}\le 2\lambda\Delta+5b+\frac{I-J}{\ln2},
\]

and a limiting global factor approximately **3.7186751164**. Its detailed expected-depth audit and rational certificates belong to the direction 2 report.

## 1. Candidate blocks are full-hull edges

Work at a flat state \(S\), with \(s=|S|\), common strict witness \(p\), and normalized hull \(K=\operatorname{conv}(\{0\}\cup\{u_i\})\). For dimension two, retain the cyclic vertex order of the **full** hull, including the origin if it is a hull vertex. The origin is a free known-negative marker, not a supplied query.

For every hull edge, form a candidate block from its real endpoint queries. A block has either two real queries, or one real query and the free origin endpoint. Do not form a potentially fictitious wrap edge by deleting the origin from the hull order.

For a nonzero hull pattern \(A\), let \(P_A\) be its positive vertices. Its candidate blocks are exactly the edges incident to at least one vertex of \(P_A\). A consecutive cyclic vertex interval expands to a consecutive cyclic edge interval: for an ordinary positive interval \([l,r]\), its incident edges run from the edge immediately before \(l\) through the edge immediately after \(r\). This may be the full circle, which is harmless. Thus every pattern becomes a circular interval demand on the candidate-block order.

Every original query's support block embeds in one candidate block. A two-real-vertex support is a genuine full-hull edge by the manuscript's support lemma. A singleton support can be padded to either incident full-hull edge; padding only adds positive coverage. Original empty support blocks can be omitted from the comparison sequence or retained as unproductive analytical positions. A terminal positive singleton can likewise be padded to an incident edge.

For hull dimension zero, a valid nontrivial separating state cannot arise with no real query support. For dimension one, the hull has at most two real endpoints and the manuscript proves that a positive endpoint determines the full nonzero pattern. Query those endpoints directly, suppressing constant tests; no fictitious adjacency is required. The dimension-two block arguments are therefore needed only when the full hull has at least three vertices.

## 2. A complete positive exit costs at most \(2(k-1)+5\), apart from its information term

Let candidate block \(k\) be the first block containing a positive vertex of target pattern \(A\), with \(|A|=q\). Put

\[
z_A=\left\lfloor\log_2\frac{\delta s}{q}\right\rfloor.
\]

The pattern class lies in a minority hull cap, so \(q<\delta s\) and \(z_A\ge0\).

Each earlier block asks at most two actual questions. In a two-real-endpoint block:

* If the first queried vertex is positive, its discovery position is at most \(2k-1\). The general endpoint allowance is \(z_A+4\), yielding total discovery plus pattern decoding at most \(2k+z_A+3\).
* If only the second queried vertex is positive, the first vertex is already known negative and is geometrically adjacent. The exit is pinned and its endpoint allowance is \(z_A+2\), yielding at most \(2k+z_A+2\).

A real-plus-origin edge uses at most one actual query and has a free adjacent negative marker; the pinned allowance applies. Its total is at most \(2k+z_A+1\), which satisfies the general bound.

Cached negative endpoints and repeated blocks only reduce actual query counts. A repeated vertex cannot newly return positive on the all-negative route. If a vertex is suppressed because it is already negative, that negative still gives pinning credit to its adjacent positive endpoint. Thus the universally valid bound is

\[
\boxed{\text{discovery plus endpoint queries for }A
\le 2(k-1)+z_A+5.}
\]

The orientation of each two-query block may be arbitrary for this maximum-depth bound. No guarantee that a positive fraction of the mass is pinned is required.

## 3. Exact grading DP with shifted block capacities

The ordinary-interval grading DP from the original report remains exact. For distinct nonnegative delay deadlines \(d_1<\cdots<d_r\), a demand with delay deadline \(d_j\) must be hit within block rank \(d_j+1\). Assign each selected candidate block the grade of the first deadline at least its rank minus one. Enforce cumulative cardinality at most \(d_j+1\) at grade \(j\).

In spatial order, the state stores for each grade prefix:

* the last selected candidate position \(p_j\);
* the number \(c_j\) of selected blocks in that grade prefix.

Selecting candidate \(x\) at grade \(i\) updates every \(p_j\) and \(c_j\) for \(j\ge i\). At the right endpoint \(r\) of an interval \([l,r]\) of grade \(j\), require \(p_j\ge l\). Reject any prefix count exceeding its capacity. This condition is equivalent to the interval containing a selected candidate of eligible grade. Backpointers give the selected grade assignment; querying blocks in grade order realizes all deadlines.

To handle circular demands, enumerate a **forced first candidate block** \(e\). Every demand hit by \(e\) has block rank one and is removed after a direct exit-height check. Cut the edge order at \(e\); remaining demands omit \(e\) and become ordinary intervals. Reduce every cumulative capacity \(d_j+1\) by one, giving capacity \(d_j\) for the remainder. In particular, delay deadline zero leaves no remaining capacity. An unhit demand with that deadline is rejected. Do not charge the forced block a second time.

For \(r\) grades, \(M\) candidate edges, and capacities at most \(B\), the state count is at most \((M+1)^r(B+1)^r\), with \(r+1\) transitions per candidate and state. This is polynomial for fixed \(r\) and quasipolynomial when \(r=O(\log n)\).

Separate optimal cardinality-budget covers remain insufficient. With candidates \(1,2,3\), deadline-one demands \([1,2]\) and \([2,3]\), and deadline-two demands \(\{1\}\) and \(\{3\}\), every individual deadline prefix has a feasible cover, but no compatible ordering exists. The grade DP enforces compatibility.

## 4. Maximum-depth algorithm and proof

Fix rational \(\lambda>1\), let \(a=2\lambda\), and choose \(\gamma\ge1\), \(0<\delta<1/3\), satisfying

\[
\gamma\log_2\frac1{1-\delta}\ge1,
\qquad
\gamma\log_2\frac1\delta\ge5.
\]

The inductive target is

\[
C(S)\le \left\lfloor a\operatorname{OPT}_{\rm W}(S)
                           +\gamma\log_2s\right\rfloor.
\]

At a singleton, stop. At a count-balanced state, query a balanced supplied line and recurse. At a flat state, recursively construct every hull-pattern child and record its actual height \(C(A)\). The zero class, if present, is a singleton with height zero.

Enumerate integer trial heights \(H\) up to \(\lceil(a+\gamma)(s-1)\rceil\). For each nonzero class, define its allowed discovery **delay**

\[
B_A=\left\lfloor\frac{H-C(A)-z_A-5}{2}\right\rfloor.
\]

Reject negative delay budgets. Round each \(B_A\) down to the largest member of

\[
\mathcal D=\{0\}\cup\{\lfloor\lambda^j\rfloor:j=0,1,2,\ldots\}
\]

not exceeding it, deleting duplicate levels. Call the result \(\widehat B_A\). Enumerate the forced first block and apply the grading DP with delay deadlines \(\widehat B_A\). On each positive exit, use the corresponding general or pinned endpoint code, then the stored child. It is valid to reject an additional trial after checking its actual total exit heights, but the proof below already gives their bound.

**Balanced step.** Each child has size at most \((1-\delta)s\) and optimum height at most \(D=\operatorname{OPT}_{\rm W}(S)\). The count potential drops by at least one under the balanced constraint, paying for the query. The floor comparison holds even though \(aD\) is nonintegral: \(\lfloor X\rfloor-\lfloor Y\rfloor\ge\lfloor X-Y\rfloor\).

**Flat-step budget.** Set

\[
H^*=\lfloor aD+\gamma\log_2s\rfloor,
\quad x=\log_2(s/|A|),
\quad L=\log_2(1/\delta),
\quad d=t_A-1.
\]

The supporting-prefix lemma gives \(\operatorname{OPT}_{\rm W}(A)\le D-d\). Hence, using the inductive child height and subtracting the endpoint floor before estimating,

\[
\begin{aligned}
H^*-C(A)-z_A-5
&\ge \lfloor ad+\gamma x\rfloor-\lfloor x-L\rfloor-5\\
&\ge \lfloor ad+(\gamma-1)x+L\rfloor-5\\
&\ge \lfloor ad+\gamma L\rfloor-5\\
&\ge \lfloor ad\rfloor.
\end{aligned}
\]

Here \(x>L\), \(\gamma\ge1\), and \(\gamma L\ge5\). Therefore

\[
B_A\ge\left\lfloor\frac{\lfloor2\lambda d\rfloor}{2}\right\rfloor
       =\lfloor\lambda d\rfloor.
\]

For \(d=0\), \(\widehat B_A\ge0=d\) directly. For \(d\ge1\), let \(j\) be the largest exponent whose integer power level is at most \(B_A\). The next power has integer floor greater than \(B_A\), so

\[
\lambda^{j+1}\ge B_A+1>\lambda d,
\qquad
\lambda^j>d,
\qquad
\boxed{\widehat B_A\ge d=t_A-1.}
\]

This uses the next **distinct** integer level, equivalently the last exponent on a plateau; repeated power floors do not create an exception.

**Feasibility.** Replace each query on an optimal witness path by a padded full-hull edge block. It covers \(A\) by at most block \(t_A\), hence by delay \(t_A-1\le\widehat B_A\). A nonzero terminal singleton can be appended as one padded edge if needed, exactly as in the supporting-prefix lemma. Omit duplicate candidate edges and unproductive blocks; this shortens all block ranks. If the analytical first query contributes no support, skip it; the first productive comparison edge still occurs no later than any class's original supporting index. One forced-edge enumeration is the first edge of this comparison ordering, so the cut grading instance is feasible at \(H^*\).

For any accepted schedule, a class first hit at block \(k\le\widehat B_A+1\le B_A+1\) satisfies

\[
2(k-1)+z_A+5+C(A)
\le 2B_A+z_A+5+C(A)\le H.
\]

Thus every positive exit plus endpoint decoding plus its child code fits the accepted height. Stop the all-negative discovery route as soon as all nonzero patterns have been covered. If \(K\) is its last useful block, some pattern has first hit \(K\), so the preceding inequality implies \(2K\le H\) (indeed \(2K+3\le H\) because \(z_A,C(A)\ge0\)). The zero singleton therefore also fits. Its all-negative route is absent when there is no zero class.

The first passing height is at most \(H^*\). Since \(D\ge\log_2s\) and \(D\le s-1\), the stated height search contains \(H^*\), and

\[
C(S)\le\lfloor aD+\gamma\log_2s\rfloor\le(a+\gamma)D.
\]

## 5. Parameters, runtime, and independent checks

Unlike the unshifted block proof, the flat condition is **five**, independent of \(\lambda\). The optimized count threshold therefore equals the manuscript's polynomial count threshold: \(\delta_*=(1-\delta_*)^5\). The difference from the polynomial theorem is the discovery coefficient, which becomes \(2\lambda\) rather than three.

All trial heights and delay budgets are \(O(n)\) for fixed parameters. The number of distinct power levels is \(O(\log n/\log\lambda)\), giving runtime

\[
(mn)^{O(\log n/\log\lambda)}.
\]

For \(\lambda=1+\eta\) with fixed small \(\eta>0\), this is \((mn)^{O(\log n/\eta)}\). Very small \(\eta\) improves the numerical factor but makes the theoretical grading exponent very large; the practical \(4.466\) certificate uses \(\eta=1/2000\). Rational powers have polynomial encoding length for fixed \(\eta\), and no logarithms are evaluated by the actual scheduler. There are at most \(n-1\) nonterminal recursive stages.

`direction1-block-schedule-check.py` verifies:

* exact rational logarithm certificates for **4.46496546 < 4.464966** and **4.46596526 < 4.466**;
* earlier unshifted certificates 4.465 and 4.467;
* incident-edge circular interval expansion and cuts, for all circular positive intervals with three through nine candidates;
* agreement between the grading DP and all permutations on 350 seeded small interval instances;
* the scaled-floor identity on 40,000 parameter/rank pairs.

The logarithm certificates use positive rational series, range-reduced to \([1,2]\), with exact rational tail bounds. The finite examples support the implementation invariant; the mathematical proof is the grading equivalence and floor inequalities above.

## 6. Polynomial compression: current status and useful narrower targets

No smaller polynomial-time leading constant is proved by this report. The adjacent-block argument identifies a stronger target: obtain simultaneous near-exact block delays while retaining the cached-neighbor stage bound. Separate coverage oracles still do not achieve this.

I checked the primary paper [Chakrabarty, Grant, and Könemann, *On Column-restricted and Priority Covering Integer Programs*](https://www.cs.dartmouth.edu/~deepc/PUBS/CGK-full.pdf). It gives an exact polynomial algorithm for priority line cover, but that is a different covering orientation: demand priorities reside at points and fixed-priority supplies are intervals. Our problem assigns selectable point grades while imposing a global nested family of cardinality capacities. Transposing incidence does not preserve the line-cover structure, and the paper does not settle the deadline scheduler. A reduction or a laminar-budget extension would itself need proof.

Promising focused proof targets are:

1. A polynomial DP for deadline instances whose demands have at most a fixed number of distinct continuation heights. The grading DP already gives such a theorem when the number of grades is fixed.
2. A compatible-prefix rounding theorem for the interval time-indexed LP with dilation strictly below 3/2. Combining that with two-support blocks would improve the polynomial maximum-depth coefficient below three. Ordinary interval-cover integrality alone does not imply this theorem.
3. A stronger dominance compression of the last-position and count grade vectors. Monotonicity cuts down state counts but does not presently turn \(n^{O(\log n)}\) into polynomial time.
4. Optimize conservative pinned-exit credits within each rounded grade, using a fixed spatial order inside grades. When grade blocks are queried in decreasing spatial order, a demand first hit at its right boundary edge can be pinned by orienting that edge from its negative endpoint toward its positive endpoint. This is an implementable additional credit, but no universal lower bound on its mass has been proved.

The largest remaining analytical opportunity is to combine coverage latency and the endpoint decoder's actual conditional redundancy. The universal four-query endpoint overhead can be approached by a highly likely internal endpoint pair, so simply replacing four by three is not valid. The adjacent block theorem obtains its improvement by including the discovery query positions in that accounting.

## 7. Root rollout removes the potential from the approximation ratio

This last step is a general theorem about decision-tree baselines, rather than a new geometric lemma. Let \(n\) be the total number of hypotheses and \(m\) the number of supplied binary queries. Fix a constant \(a>1\). Suppose a computable baseline tree \(B(S)\) is available for every reachable subset.

For maximum depth assume

\[
c_{\rm W}(B(S))\le a\operatorname{OPT}_{\rm W}(S)+\gamma\log_2|S|,
\qquad B(\{h\})=0.
\]

For expected depth use original, unnormalized masses and assume

\[
c_{\rm E}(B(S))\le a\operatorname{OPT}_{\rm E}(S)+c\mathcal E(S),
\quad
\mathcal E(S)=\sum_{h\in S}\pi_h\ln\frac{w(S)}{\pi_h},
\qquad B(\{h\})=0.
\]

In either case enumerate all states obtainable by at most \(K\) supplied queries, suppressing empty answers and constant queries. There are at most \(\sum_{j=0}^K(2m)^j\) transcript descriptions. Compute the actual baseline cost for each state. A depth-limited Bellman DP minimizes the complete tree cost obtained by attaching \(B(S)\) at each depth-\(K\) leaf. A singleton can stop earlier, and allowing a baseline continuation earlier can only improve the result. The DP uses

\[
\begin{aligned}
F_{\rm W}(0,S)&=c_{\rm W}(B(S)),\\
F_{\rm W}(k,S)&=\min_i\{1+\max(F_{\rm W}(k-1,S_i^-),F_{\rm W}(k-1,S_i^+))\},\\
F_{\rm E}(0,S)&=c_{\rm E}(B(S)),\\
F_{\rm E}(k,S)&=\min_i\{w(S)+F_{\rm E}(k-1,S_i^-)+F_{\rm E}(k-1,S_i^+)\},
\end{aligned}
\]

with value zero at singleton states. Queries are restricted to two nonempty child states. If optional early baseline stopping is allowed, additionally minimize against the baseline value.

### Maximum depth

Choose

\[
K=\left\lceil\frac{\gamma\log_2 n}{a-1}\right\rceil.
\]

Compare the optimal rollout to the first \(K\) levels of a maximum-depth-optimal tree of height \(D\), attaching baseline continuations there. If an optimal-tree route terminates earlier, its total depth is at most \(D\). If it reaches a nonterminal state \(A\) at depth \(K\), the optimal subtree has height at most \(D-K\), and the completed depth is at most

\[
K+a(D-K)+\gamma\log_2|A|
\le aD-(a-1)K+\gamma\log_2n
\le aD.
\]

Thus the DP returns a tree of height at most \(aD\). If \(D<K\), the optimal tree itself is a feasible prefix with only singleton leaves, so the same bound holds.

### Expected depth

Choose

\[
K=\left\lceil\frac{c\ln n}{a-1}\right\rceil.
\]

Let \(P\) be the weighted cost of the first \(K\) levels of an expected-depth-optimal tree, stopped earlier at singleton leaves. Let \(\mathcal T\) be its nonterminal states at depth \(K\), and let \(p=\sum_{A\in\mathcal T}w(A)\) be their total original mass. Every target in \(\mathcal T\) has incurred exactly \(K\) prefix queries, giving \(P\ge Kp\). The entropy bound \(\mathcal E(A)\le w(A)\ln|A|\le w(A)\ln n\) gives \(\sum_{A\in\mathcal T}\mathcal E(A)\le p\ln n\).

The optimum residual subtrees are feasible identifying trees for their states, hence

\[
\sum_{A\in\mathcal T}\operatorname{OPT}_{\rm E}(A)
\le \operatorname{OPT}_{\rm E}(S)-P.
\]

Attaching baseline tails to that optimum prefix gives cost at most

\[
\begin{aligned}
P+\sum_{A\in\mathcal T}c_{\rm E}(B(A))
&\le P+a(\operatorname{OPT}_{\rm E}(S)-P)+cp\ln n\\
&\le a\operatorname{OPT}_{\rm E}(S)
   +\bigl(c\ln n-(a-1)K\bigr)p\\
&\le a\operatorname{OPT}_{\rm E}(S).
\end{aligned}
\]

The root Bellman DP can only improve on this feasible prefix. This reasoning uses total tail mass, so a very rare branch may have arbitrarily large depth without invalidating the result. It does not require an a priori maximum-depth bound on an expected-depth-optimal tree.

### Application and complexity

Both adjacent-block baselines have \(a=2\lambda\) and fixed potential coefficients. Choose rational \(1<\lambda\le1+\varepsilon/2\). The root rollout therefore gives both objectives approximation factor at most \(2+\varepsilon\).

For fixed \(\varepsilon>0\), \(K=O(\log n)\). Enumerating reachable states and computing their baseline tails uses quasipolynomial time: the product of \((2m)^{O(\log n)}\) states with \((mn)^{O(\log n/\varepsilon)}\) baseline time is still \((mn)^{O(\log n/\varepsilon)}\). The Bellman operations use only actual integer heights or rational masses/costs. Choose a conservative rational upper bound on the potential coefficients and an integer bound on \(\ln n\) or \(\log_2n\) if exact logarithm evaluations are inconvenient. The theoretical constants appear only in selecting a sufficiently large depth cap.

All supplied queries remain available inside every tail. The final output is a proper binary decision tree with \(n-1\) internal nodes after suppressing constant questions. The quasipolynomial state search is an offline construction cost, not a larger output tree.

**Limit of this result:** the leading coefficient two is inherited from expanding each original query into at most two supports. The rollout eliminates the additive potentials; it does not remove that geometric support factor. A factor below two needs stronger original-cap restriction accounting or another discovery invariant. No inapproximability barrier at two is claimed.
