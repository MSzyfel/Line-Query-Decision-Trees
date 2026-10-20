# Further hardness routes: prefix incompatibility and geometric commitment

Research audit, 13 October 2026. The instance consists of rational planar point hypotheses and a supplied separating family of strict binary line-side queries, each of unit cost. W is maximum depth; E is expected depth. All hardness statements below concern this precise model. **No new APX-hardness theorem is proved here.** The new proved contribution is a planar prefix-incompatibility example with an asymptotic 11/10 separation in optimal uniform expected cost, although every static maximum-coverage budget has the same value in the two examples.

## 1. What the improved algorithms allow

The current manuscript/report gives polynomial approximations W <= 4.464966 OPT_W and E < 5.272565 OPT_E, and quasipolynomial (2+epsilon) approximations for both. These upper bounds constrain possible gaps. Under ETH, a polynomial-size reduction from SAT establishing a fixed gap rho > 2 is impossible: choose epsilon < rho-2 and the quasipolynomial approximation would give a subexponential SAT algorithm. This argument requires polynomial instance size and bit length and does not follow from P != NP alone. A fixed gap strictly between 1 and 2 remains consistent with these algorithms.

Two restricted families need special care. With a common all-miss witness and every opposite cap of bounded cardinality, W is exactly polynomial-time solvable; see [direction4-shallow-cover-hardness.md](direction4-shallow-cover-hardness.md). Weighted singleton/pair expected-cost paths and cycles with all singleton queries have an EPTAS. Consequently, a fixed-cap common-witness hardness construction must target E and escape that pair-path-and-cycle subclass; caps of size at least three are a natural target, but the restricted EPTAS alone does not rule out every geometric pair system. An unrestricted W construction must escape the bounded-cap common-witness family.

The existing strong NP-completeness results already exclude an FPTAS, subject to the manuscript's polynomially bounded integer objectives: an approximation error below the reciprocal objective bound recovers the exact integer optimum. This is weaker than APX hardness and does not exclude a PTAS or EPTAS. Uniform-prior E hardness is still unresolved.

## 2. Why known decision-tree gaps do not transfer automatically

General min-sum set cover has strong constant-gap hardness, and general entity-identification trees have constant-factor uniform-prior hardness and logarithmic hardness with arbitrary priors. The supplied binary tests in those results need not be planar halfplanes. In particular, the dominant-witness set-cover reduction cannot be reused: minimum-weight cover of planar points by supplied halfplanes is exactly polynomial-time solvable. Static maximum coverage by supplied planar halfplanes is also exactly solvable. [Feige, Lovasz and Tetali](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf), [Chakaravarthy et al.](https://doi.org/10.1145/1921659.1921661), [Har-Peled and Lee, Section 3](https://jocg.org/index.php/jocg/article/download/2950/2644/7396), [Badanidiyuru, Kleinberg and Lee, Appendix B](https://arxiv.org/html/1112.0689).

This has a concrete consequence: a construction in which satisfiability produces higher static coverage at some efficiently known query budget, and unsatisfiability lowers that coverage by a constant fraction, cannot be a polynomial planar-halfplane reduction unless P = NP. A valid ordered-cover source must hide difficulty in the compatibility of good prefixes across multiple budgets, or in later identification costs, while static optimization remains tractable.

Covering points by lines is APX-hard even under a bound on collinearity. However, those tests ask whether a point lies *on* a line. Replacing an equality query by two nearby parallel side queries also reveals which side contains every nonmember, so the replacement does not preserve the decision-tree optimization problem. The primary paper is a useful source of explicit geometric incidence constructions, not a completed reduction for binary line-side queries. [Dumitrescu and Jiang](https://adriandumitrescu.org/line-cover.pdf).

## 3. Proved: static coverage curves do not determine optimal ordering

Let M be a positive integer. Put 6M source points at (t,t^2), t=1,...,6M, and the witness p=(0,0). A query with negative side

    4y - 4(a+b)x + (2a-1)(2b+1) < 0

contains exactly the integer-indexed points a,...,b. It misses p, and no point lies on the boundary. Supply all singleton caps as well. Every cap below has cardinality at most four, and the singleton queries separate the instance.

Partition the source points into consecutive blocks of six. In each block relabel the indices 1,...,6. The GOOD family additionally supplies [1,4] and [5,6]. The BAD family additionally supplies [2,5], [1,3], and [4,6]. Intervals in different blocks never hit the same point.

For both families the optimal static coverage using at most q queries is

    C(q) = 4q                         for 0 <= q <= M,
           2q + 2M                   for M <= q <= 2M,
           6M                        for q >= 2M.

For one block, both families cover four points with one query and all six with two. Summing independent block budgets gives the displayed common curve.

For an ordering let F be the sum, over source points, of their first-hit query positions. The static area lower bound is

    F >= sum_{q >= 0}(6M - C(q)) = 5M^2 + 3M.

GOOD attains it: first query the M four-point caps, then the M two-point caps. Hence

    OPT_F(GOOD) = 5M^2 + 3M.

BAD cannot attain all static optima with one nested sequence. In a block, a fresh-hit group of size four must be [2,5], after which points 1 and 6 need separate first-hit queries. Its group sizes are therefore dominated by (4,1,1). If there is no fresh-hit group of size four, every group is at most three; its sizes are dominated by (3,3). Both dominant patterns are feasible. For lower bounds, replace any fragmented pattern by its dominant one and globally sort first-hit group sizes in decreasing order. Majorization can only reduce F. Conversely, that sorted schedule is feasible for these dominant patterns: every four-point group precedes its two singleton tails, and the two three-point groups are disjoint.

If k blocks use (4,1,1) and M-k use (3,3), there are k groups of size four, 2(M-k) of size three, and 2k of size one. Their minimum invoice is

    F(k) = 6M^2 - 2Mk + 2k^2 + 3M.

The integer optimum chooses k nearest M/2, giving

    OPT_F(BAD) = (11/2)M^2 + 3M + (M mod 2)/2.

Thus OPT_F(BAD)/OPT_F(GOOD) tends to 11/10, despite identical complete static coverage curves.

This persists for uniform expected-depth identification. If G is the sum of leaf depths including p, following p in any tree gives a cover ordering and hence G >= OPT_F. Conversely, query an optimal cover ordering on the miss spine and identify its first-hit groups locally. Since every cap has at most b=4 points,

    OPT_F <= OPT_G <= OPT_F + bN = OPT_F + 24M.

The additive term covers the witness's spine length and at most b-1 extra queries per source point. Both examples have the same N+1 hypotheses, so the ratio of their optimal uniform expected depths also tends to 11/10.

**Scope.** This is an explicit gap between two easily recognized families, not a reduction from an NP-hard problem. It proves that exact static cover and exact static maximum coverage do not rule out a constant ordered-cover gap. It also shows why a useful reduction should preserve access to the four-point cap in a bad gadget: simply replacing (4,2) by (3,3) would already expose the violation to static maximum coverage.

The coordinates have polynomial bit length. [further-hardness-check.py](further-hardness-check.py) verified exact latency and all static coverage budgets for M=1,2, interval signs, and the analytic minimum for M=1,...,100. The formulas above are proved analytically, not inferred from those checks.

## 4. Precise unresolved prefix-gap target

The most promising E target is a **gap-preserving geometric prefix-compatibility lemma**. Its desired statement is a polynomial construction from a perfect-completeness gap CSP, with M constraints, producing N = Theta(M) rational planar points, a strict common witness, supplied separating caps of some fixed cardinality b >= 4, and a scale A_M = Theta(M^2), such that:

1. A satisfying assignment yields an ordering of cost at most A_M + O(M).
2. If every assignment violates at least delta M constraints, every ordering costs at least (1+eta)A_M - O(M), for a constant eta > 0 depending only on delta.
3. The soundness proof decodes one globally consistent assignment from every ordering, or charges all failures to decode at least Omega(M^2) additional latency.
4. The static coverage optima remain tractable and reveal no CSP gap; the cost gap is caused by incompatible good prefixes.
5. The geometric construction proves all intended incidences, all unintended cross-gadget incidences, polynomial coordinate bit length, and separation using the actual supplied lines.

The GOOD/BAD block example supplies a local source of quadratic latency: a linear fraction of incompatible blocks, competing in one ordering, can produce a constant relative gap. What it does **not** supply is assignment coupling. Selecting the best local pattern independently is easy. The missing geometric lemma must couple choices across clauses while retaining the four-point fallback caps and must prevent independent repairs at negligible cost. This is the central unresolved step; no coordinates or gap-CSP reduction meeting it are currently proved.

An arbitrary 3-uniform test table is not enough. Fixed-size halfplane caps imply a bounded number of convex peeling layers, and points on a single convex layer yield interval-like caps. A source construction confined to disjoint parabola blocks has no hard global coupling. Several convex layers, nonlocal caps, or a different common-witness geometry should be investigated, with an explicit proof that the added interactions do not reveal the gap to a static coverage oracle.

**Conditional theorem once that lemma is proved.** For bounded caps and a separating common-witness source, the identification raw objective differs from ordered-cover F by at most bN. Since A_M=Theta(M^2) and N=Theta(M), any fixed source gap transfers to uniform E with every slightly smaller fixed gap. The proof is the all-miss spine lower bound and the local-identification upper bound above. This is a valid reduction framework with an unproved source-hardness hypothesis.

## 5. Proved pair-separation geometry, and its commitment failure

There is a compact way to realize arbitrary graph edge pairs without pretending to realize an arbitrary whole test table. Let graph vertices be i=1,...,r, put a_i=2^i, and supply

    L_i: y = a_i x + a_i^2.

For edge ij, define

    z_ij = (-(a_i+a_j), -a_i a_j),
    h_ij^- = z_ij - (0,1/4),     h_ij^+ = z_ij + (0,1/4).

At L_k the affine signs of these two points are

    -(a_k-a_i)(a_k-a_j) - 1/4,
    -(a_k-a_i)(a_k-a_j) + 1/4.

Exactly L_i and L_j separate the pair; every other central value is a nonzero integer. All queries are strict, distinct edges have distinct x coordinates, and the coordinate bit length is O(r). This explicit geometric fact is checked for the complete graph on 20 vertices in the accompanying script.

It does **not** imply a vertex-cover reduction. The cost of querying L_i in a decision tree is charged each time it occurs on a root-to-leaf path, and separate branches can choose different endpoint lines for their own pairs. There is no global one-time purchase of vertex i. Moreover, different edge pairs can have the same full sign code under the vertex lines. If the input must be repaired by supplying vertical address lines between distinct edge-center x coordinates, a tree identifies the edge by binary search and then queries one of its endpoints. This gives height at most ceil(log_2 |E|)+1 and similarly small expected depth, regardless of minimum vertex cover size.

Trying to force all edge pairs to share one anchor-side sign for every vertex line would recreate a common-witness static vertex-cover instance. A polynomial geometric realization of arbitrary hard graph incidence in that form would contradict exact planar-halfplane cover unless P = NP. Hence the useful geometric feature here is pair separation only.

For an unrestricted W route, the missing lemma is a **global commitment gadget**: augment these clients with rational points and lines so that every identifying tree yields a globally chosen cover/assignment C, and its cost has a lower bound A+B f(C), with A/B bounded on the relevant scale; a matching upper bound must hold for a good C. The proof must make local branch-by-branch endpoint selection and address routing expensive, before they separate the clients. This statement is currently unproved.

Any proposed commitment gadget should be tested against query promotion. A supplied query can be moved to the root, followed by restricted copies of the original tree, increasing maximum depth by at most one and raw expected depth by at most total prior weight. Promoting k queries costs at most k in W and k times total prior weight in the raw E objective. A gadget charging a growing penalty for one omitted literal line can therefore fail if adding that line near the root cheaply repairs all affected clients. [direction5-robust-gadget-hardness.md](direction5-robust-gadget-hardness.md) gives the formal lemma and witness-routing obstruction.

## 6. Recommended next proof tasks

The E route has the clearest concrete target: couple GOOD/BAD prefix patterns to a gap CSP while preserving static coverage and prove an Omega(M^2) soundness charge. Start with caps of size four or a slightly larger constant, uniform clients, and several convex layers. Its potential gap near 1.1 is consistent with every current approximation result. It would establish uniform E APX hardness, whereas the bounded-cap W result would remain exact.

For W, investigate the explicit edge-pair construction only together with a commitment gadget that survives address queries and promotion. A weighted dominant witness or constant number of routing witnesses alone is unlikely to suffice: exact static cover and cheap routing remove those proposed barriers. A direct constant-depth promise gap is another possibility, but each fixed depth is enumerable in polynomial time, so the hardness threshold must grow with input size.

No logarithmic inapproximability, no general 2-epsilon hardness, and no planar realization of unrestricted set systems should be stated without an independent reduction. The current rigorous hardness improvement is the no-FPTAS corollary; the new concrete research contribution here is the prefix obstruction and its precise missing coupling lemma.
