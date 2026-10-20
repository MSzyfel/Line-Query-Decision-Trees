# Established inapproximability and an exact uniform-cloud reduction

Research derivation, 13 October 2026. These results concern the manuscript's identification model: finite rational planar point hypotheses, only supplied strict binary line-side queries, unit query costs. Let n always denote the number of hypotheses in the instance to which the stated approximation guarantee applies. W is maximum depth, E expected depth. Under a uniform prior, write G = nE for the integral sum of leaf depths.

**New proved consequences, assuming the manuscript's audited 3-Partition reductions:** unless P = NP, polynomial-time approximation factors

    1 + 1/(3 sqrt(n))          for W,
    1 + 9/(10 n^3)            for arbitrary-prior E,
    1 + 100/n^(5/3)           for uniform-prior E

are impossible, even for integer-coordinate points on a parabola, polynomially bounded integer line coefficients, and O(n) supplied lines. The uniform-prior result follows from a new exact cloud-transfer lemma below, which also establishes strong NP-completeness of uniform E and rules out a uniform E FPTAS. These factors tend to one: **this is not APX hardness and does not exclude a PTAS or EPTAS.**

## 1. Uniform singleton exchange

Consider any proper identifying tree under a uniform prior. At a node on state S, suppose its query isolates a single hypothesis x and the other child has root query r. Because r is proper on S minus {x}, its two answer classes there, A and B, are nonempty. Suppose x would answer r on the A side. Replace these two queries by r at the first node, with the singleton query for x in its A child. Attach the original A and B subtrees without changing them.

The depth of x increases by one, the depth of every hypothesis in B decreases by one, and all other depths are unchanged. Consequently

    G(new) - G(old) = 1 - |B| <= 0.

Both trees use supplied queries. No inferred extra query is added. This is a statement about the sum of depths under uniform weights; it need not hold with arbitrary unequal weights.

**Useful consequence.** In a uniform instance consisting of whole-cloud membership queries and private singleton queries, a private singleton can be pushed down a chosen anchor's path, through intervening private queries and whole-cloud queries, without increasing cost. It moves off that path when it crosses a whole-cloud query selecting its cloud. Private queries belonging to the anchor's own cloud can be pushed after all whole-cloud queries.

The transformation terminates constructively. Take an external private query on the anchor path and move it through successive query nodes. The external point's cloud anchor is still on that path: private tests never remove an anchor. A whole-cloud query separating this anchor from the distinguished anchor must eventually occur, and at that query the private test moves into the hit branch. This removes one external private query from the distinguished path. Repeat, then move its own-cloud private tests past the remaining whole-cloud queries. Swapping adjacent private tests has zero cost and does not obstruct this process.

## 2. Exact uniform-cloud transfer for singleton/pair linear forests

Start with the manuscript's weighted singleton/pair linear forest model. Vertex 0 is distinguished; nonzero vertices 1,...,N form a disjoint union of paths and are ordered along each path, component by component. Every nonzero singleton membership test and every edge-pair membership test is supplied. Vertex i has positive integer raw weight w_i. The manuscript's exact invoice is

    OPT_weighted = min_matching M {
        w_0 (N-|M|) + C_completion(J(M))
        + sum_{uv in M}(w_u+w_v)
    },

where J(M) contains each matched pair's total weight and every unmatched vertex's weight, and C_completion sorts these masses decreasingly and charges mass times its one-based rank.

Replace vertex i by a cloud of w_i ordinary, uniformly weighted points. Choose Q = 4 max_i w_i and put

    cloud i = { (Qi+j, (Qi+j)^2) : 0 <= j < w_i }.

The j=0 point is its anchor. For a nonzero singleton cloud or an adjacent pair of clouds a,...,b, supply the negative-side whole-cloud query

    4y - 4Q(a+b)x + Q^2(2a-1)(2b+1) < 0.

It selects exactly the indicated clouds and excludes cloud 0. For every nonanchor point of abscissa t, supply its private query

    2y - 4tx + 2t^2 - 1 < 0.

Its negative answer isolates that one point. No private query is supplied for any anchor. All these signs are strict on all hypotheses. The construction is explicit and contains n = sum_i w_i hypotheses and O(n) queries. Abscissae are O(n^2), ordinates and line coefficients O(n^4); all points remain in strictly convex position on the parabola.

Define

    D(w) = (w-1)(w+2)/2,
    D_total = sum_{i=0}^N D(w_i).

**Exact transfer theorem.** The minimum raw uniform cost on the cloud instance is

    OPT_cloud = OPT_weighted + D_total.

**Proof: the single-cloud cost.** On one intact cloud of size w, whole-cloud queries are constant and private queries isolate its nonanchors. Its optimal local raw cost is the chain cost 1+2+...+(w-1)+(w-1) = D(w).

**Proof: the two-cloud cost.** On two intact clouds of sizes u,v, a whole-cloud query can split the two clouds. This gives raw local cost

    f(u,v) = D(u)+D(v)+u+v.

No other supplied query improves it. A nonconstant whole-cloud query splits the clouds; every other nonconstant query isolates one nonanchor point. Induct on u+v. Querying a private point in the u cloud first costs

    u+v + f(u-1,v),

which exceeds the displayed split cost by v-1 >= 0, since D(u)-D(u-1)=u. The analogous difference for a private point of the v cloud is u-1 >= 0. The base u=v=1 has cost two. If u=1, no private test of that cloud exists; the same induction still applies. Thus the formula is exact.

**Proof: global lower bound and normalization.** Follow the anchor of cloud 0 in an optimal proper tree. Apply the uniform singleton exchange to remove all external private queries from this path and postpone all cloud-0 private queries until its end. At every first-hit whole-cloud exit, all points of every newly hit cloud are intact: private singleton queries never occurred earlier on this path. First-hit groups therefore consist of one full cloud or two adjacent full clouds, and pair groups form a matching. Replace a query first hitting only one cloud by its supplied whole-cloud singleton query. There are N-|M| whole-cloud spine queries; their order contributes the weighted first-cover invoice. Cloud 0 contributes w_0 times this spine length. Every cloud contributes its fixed D(w_i); each paired exit contributes the additional w_u+w_v from the exact two-cloud calculation. Sorting the disjoint exit groups decreasingly by mass gives precisely the weighted invoice plus D_total.

**Proof: attainability.** For any matching, query its disjoint pairs and unmatched singleton clouds in decreasing total cloud size. On each hit exit use the exact local one- or two-cloud code. After the last whole-cloud query identify cloud 0 by its private tests. This attains the invoice plus D_total, proving equality.

The proof does not use a dominant weight and holds for every positive integer weight vector. It also addresses the previously unresolved concern about private cloud queries appearing near the root: the uniform singleton exchange makes those queries removable from the distinguished spine without a cost increase. The quadratic cloud cost is added exactly once and is independent of the matching.

## 3. Uniform E strong NP-completeness and no FPTAS

Apply the exact transfer theorem to the manuscript's strongly NP-hard weighted linear forest construction. Its weights are positive integers bounded by a fixed polynomial in the original number of vertices, so the replication has polynomial size. If its raw threshold is k, use the uniform cloud threshold

    (k + D_total)/n.

The exact-transfer equality proves the yes/no equivalence for arbitrary adaptive trees. The uniform prior has no encoded weights, coordinates and lines have polynomially bounded integer coefficients, and the threshold numerator is polynomially bounded in the output size. Membership in NP follows from a proper tree with n-1 internal nodes. Thus uniform E is strongly NP-complete on these explicit supplied-line instances.

Since G is integral and every proper identifying tree has G <= n(n-1), an FPTAS with epsilon=1/(2n(n-1)) would recover the exact optimum. Therefore even uniform E admits no FPTAS unless P = NP.

This construction has large whole-cloud caps; it does not establish uniform E hardness for bounded-size caps. It also does not contradict the weighted singleton/pair EPTAS: adding the same nonnegative D_total preserves an approximation ratio, so this exact cloud family inherits approximation schemes from the compressed weighted family. It is unsuitable for proving a fixed-factor gap.

## 4. A square-root shrinking-factor barrier for W

Use the existing maximum-depth reduction's notation:

    m=3p, s=sum_i a_i, p>=2,
    u=2s(p-1), M=m+2,
    q=(p-1)(4s+2m), K=q+M,
    H=M+u.

The construction contains exactly u internal even clouds of size H: there are two H clouds per repeated four-row block, a_i repetitions per segment, and p-1 segments per item. Hence its total point count satisfies

    n >= uH >= u^2.

Because every item is a positive integer, s>=m. Therefore

    q = 2u+2m(p-1) <= 3u,
    M=m+2 <= 2m <= u,
    0 < M <= u.

The identity (3u+M)^2 - 9u(u+M) = M(M-3u) < 0 and n >= u(u+M) imply K <= 3u+M < 3sqrt(n). The source reduction has optimum at most K on yes-instances and at least K+1 on no-instances. A polynomial approximation of factor 1+1/(3sqrt(n)) would, on a yes-instance, return a tree of height at most K+K/(3sqrt(n)) < K+1. Height is integral, so it returns height at most K. A no-instance can never return such a tree. This decides restricted 3-Partition in polynomial time. Thus that approximation guarantee is NP-hard.

This improves the explicit n-dependent threshold over the generic 1+Theta(1/n) integrality argument. It still tends to one and does not amplify the reduction to a constant gap.

## 5. Cubic shrinking-factor barrier for arbitrary-prior E

Use the expected-depth reduction's exact parameters and the symbol n_0=N+1 for its original number of weighted hypotheses. Its source scale V and error bounds give

    E_+ <= V/1000, E_- < V/2000,
    NO optimum >= k + (1997/2000)V,
    YES optimum <= k.

The stated gap concerns the raw weighted objective. For boundary choices it follows directly from V-E_--E_+ >= (1997/2000)V. Internal unmatched choices have an even larger gap: the manuscript's Step 7 bounds their excess above k from below by

    [r/3 - (p+8)(q+m+1)^2]V.

Because r >= 1000(p+10)(q+m+1)^2, this exceeds (1/3-1/1000)rV > V. Maximum matching is forced at the optimum by the distinguished weight. Thus every possible optimum either is a boundary solution with the displayed gap or an internal solution with a larger gap. The bound is on the global optimum, not only on a chosen normal form.

Write P for total item-path weight, W=P+rV/2, and w_0=(N+1)W+1. A useful explicit bound is W<=rV. Indeed, item vertex weights are at most (10+2p)V, so

    P <= (2q+m)(10+2p)V
      <= 4(q+m)(p+10)V.

The chosen r >= 1000(p+10)(q+m+1)^2 makes P < rV/250. Adding rV/2 proves W<rV. Since r<=N=n_0-1, the total weight obeys

    Omega = (N+2)W+1
          <= (n_0+1)(n_0-1)V+1 <= n_0^2 V.

To bound the decision threshold, take any boundary matching. Its feasible code has raw cost G_B <= Omega(n_0-1). The quadratic identity with nonnegative variance and error at least -E_- yields k <= G_B+E_-+E_+. Consequently

    k < n_0^3 V.

A polynomial approximation factor 1+9/(10n_0^3), applied to normalized priors and evaluated in raw units, returns a yes-instance cost below k+9V/10. Every no-instance cost is at least k+(1997/2000)V. Comparing with k+9V/10 decides the source. This proves the claimed factor inapproximability; normalization does not change any ratio.

## 6. A 5/3-power shrinking-factor barrier for uniform E

In the uniform cloud instance, n=Omega and the raw threshold is K'=k+D_total. The whole weighted optimum, including its no-gap, transfers exactly, so

    YES optimum <= K',
    NO optimum >= K' + (1997/2000)V.

We need two bounds on the construction.

**Population versus gap scale.** The explicit choice of r ensures q+m+1<=r/1000, hence N+2=2q+m+r+2<=2r. Using W<=rV gives

    n = (N+2)W+1 <= 2r^2V+1 <= 3r^2V.

Since V=2000m(r+q+m+1)>=2000r,

    n <= 3V^3/4,000,000 < V^3/110^3,
    V >= 110n^(1/3).

The strict numerical inequality follows from 3 * 110^3 = 3,993,000 < 4,000,000.

**Threshold versus population.** Take the feasible boundary code used above and lift it to clouds. Its raw cost G'_B is at most n(n-1). Because k<=G_B+E_-+E_+,

    K' <= G'_B+E_-+E_+
       < n(n-1)+(3/2000)V.

Also n>=rV/2>=V, so K'<n^2.

A polynomial approximation factor 1+100/n^(5/3) therefore returns, on a yes-instance,

    G_A <= K' + 100K'/n^(5/3)
         < K' + 100n^(1/3) <= K'+10V/11.

On a no-instance every feasible tree has cost at least K'+(1997/2000)V. The rational comparison threshold K'+10V/11 separates the two cases. Dividing all costs by n gives exactly the same proof for uniform expected depth E. This establishes the announced approximation barrier, which is stronger than the generic inverse-quadratic threshold obtained only from uniform objective integrality.

## 7. Verification and the remaining constant-gap problem

[next-hardness-check.py](next-hardness-check.py) independently checks the exact full adaptive uniform Bellman optimum against the cloud-transfer invoice on 383 weighted linear forest instances, with cloud weights 1,...,3 and up to four nonzero vertices. It verifies all supplied geometric signs, the strict W bound K < 3sqrt(n) on 380 concrete parameter instances, and 110^3 n < V^3 on 42 complete expected-depth parameter constructions. These checks support the analytic proofs above; the asymptotic and NP-hardness claims are proved by the reductions, not by enumeration.

The fixed-factor target remains open here. The cloud transfer establishes previously missing uniform hardness and sharper quantitative inapproximability, but its fixed additive costs and the weighted linear forest EPTAS prevent it from providing APX hardness. The bounded-cap prefix example in [further-hardness.md](further-hardness.md) remains the most concrete fixed-factor mechanism: a global realizable choice-coupling gadget would have to preserve static coverage while forcing incompatible nested prefixes. None is asserted in this report.

A primary-literature search also found the April 2026 general uniform decision-tree constant-factor result, [Szyfelbein, *Constant-Factor Approximation for the Uniform Decision Tree*](https://arxiv.org/abs/2604.12036). Its test families are general, whereas this report's transfer explicitly preserves supplied strict planar line queries. No claim of first-known general uniform hardness or a complete novelty search is made.
