# Direction 2: joint discovery and endpoint decoding

Prepared 13 October 2026. This report uses the manuscript's binary, supplied-line, unit-query model and its common-witness, adjacent-support, restriction-credit, and capped-entropy lemmas. It does not claim a literature-wide novelty result. No shared TeX file was edited.

## A rigorous improved expected approximation

**The stage construction gives an additive expected guarantee that can be improved to a global (2+epsilon) approximation by the independently developed rollout from directions 1 and 3.** Without rollout, for every fixed rational eta > 0 this construction gives a quasipolynomial factor at most 3.71868 + 2 eta. A concrete choice eta = 1/100000 gives **3.71870**, improving the previous 3.835 result. The factor is certified using exact rational logarithm intervals in `direction2-joint-decoding-check.py`. The smaller scheduling accuracy exponent obtained with eta = 1/2000 gives the alternative bound 3.71968.

The proof combines adjacent support blocks with a scheduling objective shifted by one block. The shift is essential: ordinary rank rounding would unnecessarily add a positive-mass error term.

### Legal block candidates

At a mass-flat state S, let K be the convex hull of all normalized query vectors and the origin. In dimension two use **the edges of the full hull, including an origin vertex when present**, as block candidates. A block queries its real endpoints; an origin endpoint is the free constant negative answer and is omitted. Thus a block costs at most two supplied queries.

This use of the full hull matters. Deleting the origin before declaring the wraparound pair adjacent could produce a pair that is not a hull edge. Degenerate hulls of dimension at most one can be handled directly, as in the manuscript.

Every original query has its at most two supports in one block candidate. A positive hull pattern is a circular vertex interval, so the block candidates hitting it form a circular interval of edge positions. Repeated blocks and repeated endpoint queries can be suppressed; suppression decreases all realized costs.

Let k_A denote the index of the first scheduled block hitting a nonzero pattern class A, and let K_sch be the selected block count. Write p_0 = w(A_0), taking p_0 = 0 when the zero pattern is absent. Optimize the shifted objective

    F = 2 sum_{A != A_0} w(A)(k_A - 1) + 2 p_0 K_sch.

The zero term uses K_sch, rather than K_sch - 1: the witness must wait for the whole cover.

### A quasipolynomial approximation to the shifted objective

Fix lambda = 1 + eta. Enumerate the first selected block e. Give it grade zero, with delay d_0 = 0 and total-prefix capacity c_0 = 1. Every demand hit by e has zero shifted charge. Cut the circular block order at e; all remaining demands are ordinary intervals.

For the other grades use the distinct positive integers

    d_j = floor(lambda^j),      c_j = d_j + 1.

A grade-prefix may contain at most c_j selected blocks, including e. Equivalently, its capacity among the remaining candidates is d_j. Assign a candidate a grade or omit it. At each spatial position maintain, for every grade prefix, its selected count and its last selected position. When a demand interval [L,R] closes at R, find the smallest grade prefix whose last position is at least L and charge 2 w(A)d_j. At the end charge 2 p_0 K_sch using the actual selected count. Retain the minimum charge for every state and reconstruct by backpointers.

The ordinary interval invariant is the same as the earlier scheduling DP: a prefix hits [L,R] exactly when its last selected position after R is processed is at least L. Sorting selected candidates by grade implements the resulting assignment, and every demand's first hitting block has

    k_A - 1 <= d_j.

There are O(eta^{-1} log n) distinct grades. Cap the selected count by n, since an optimal proper witness path has at most n-1 original queries and at most one terminal block needs appending. The state count is (mn)^{O(eta^{-1} log n)}, with polynomial bit arithmetic for fixed rational eta. Positive prior weights only enter rational objective values; the number of grades does not depend on the smallest probability.

To compare with an arbitrary ordering, assign its rank-one block to d_0 = 0 and every block of rank k >= 2 to the least positive delay d_j >= k-1. Minimality gives

    d_j < lambda(k-1).

Indeed the preceding power, before duplicate floors are omitted, is smaller than the integer k-1, so its next power is smaller than lambda(k-1). All grade-prefix capacities are valid because ranks through d_j+1 include at most d_j+1 blocks. The zero term is kept exact. Therefore the DP's charge is at most lambda times that ordering's F and dominates the F of its reconstructed schedule.

### The optimum witness gives F <= 2 Delta

Let Delta = OPT_E(S) - sum_A OPT_E(A) for the full hull-pattern partition. Replace each query of the optimum witness path by one full-hull edge containing its supports. A singleton support is included in an incident edge. Adding that edge's other endpoint can only produce earlier hits.

If t_A is the manuscript's first supporting block, then k_A <= t_A. The supporting-prefix lemma gives

    sum_A w(A)(t_A-1) <= Delta.

When the zero pattern exists, its supporting index is q+1, so its contribution p_0 q pays for the zero waiting term, and the comparison sequence has K_sch <= q. When it is absent, an unhit terminal nonzero singleton can be covered by appending an incident edge; it has k_A <= q+1 and prefix credit q. There is no zero waiting term in that case.

Hence the comparison ordering satisfies F <= 2 Delta, and the schedule returned by the DP satisfies F <= 2 lambda Delta.

### Adjacent blocks pay for discovery and decoding together

Execute each block's real endpoints in either orientation until the first positive answer. If the first endpoint is positive in block k, discovery costs at most 2k-1. Its endpoint decoder has expected overhead at most four plus its conditional pattern entropy in bits. Thus the nonentropy allowance is

    2k - 1 + 4 = 2(k-1) + 5.

If the second endpoint is the first positive answer, the first is a cached negative adjacent hull vertex. One endpoint is pinned, so the remaining endpoint decoder has overhead at most two. Discovery plus overhead is at most

    2k + 2 = 2(k-1) + 4.

Blocks incident to an origin vertex contain one real query: its first-positive route costs at most 2(k-1)+1 and requires at most four overhead queries, which also gives the allowance 2(k-1)+5. Origin and previously cached answers cost zero. Early singleton inference reduces the work.

Let I be full pattern information, J discovery information, and b the nonzero pattern mass. Applying the manuscript's entropy-chain accounting to these actual discovery transcripts yields

    W_stage <= 2 lambda Delta + 5b + (I-J)/ln 2.

Every nonzero discovery output is contained in a positive hull cap or is an inferred nonzero singleton. Its mass is below delta w(S); hence J >= b sigma(delta), with

    sigma(delta) = -k delta ln delta - r ln r,
    k = floor(1/delta),   r = 1-k delta.

Take

    c = max{1/h(delta), 5/sigma(delta)}.

The balanced query bound and the flat bound both become W_stage <= 2 lambda Delta + c I. Optimum decreases and entropy decreases telescope through recursion, giving the factor

    R = 2 lambda + max{ln 2/h(delta), 5 ln 2/sigma(delta)}.

For delta = 139087/1000000, exact rational logarithm intervals certify both terms in the maximum below 42967/25000 = 1.71868. Thus R < 3.71868 + 2 eta; eta = 1/100000 yields R < 37187/10000 = 3.71870. The alternative eta = 1/2000 yields R < 11624/3125 = 3.71968. Numerical optimization as eta tends to zero gives a limit approximately 3.71867511638 near delta = 0.139087299724.

## Independent audit of the stronger rollout

The preceding stage inequality actually establishes the baseline guarantee

    C(S) <= a OPT_E(S) + c E(S),
    a = 2 lambda,

where E(S) is the weighted conditional entropy in natural units. This holds on every state using the original weights. Directions 1 and 3 observed that bounded-depth exact lookahead removes the entire entropy term; the following independently checked proof gives the sharper depth bound.

Set K = ceil(c ln n/(a-1)). Enumerate legal query trunks through depth K and attach the actual feasible baseline trees at their frontier states. Optimize this complete cost by the depth-limited Bellman recurrence; a singleton stops early, and minimizing against the baseline tree at earlier states is also allowed.

For comparison, truncate an expected-optimal tree at depth K. Let P be its weighted prefix query cost and p the original mass reaching nonterminal states at that depth. Then P >= Kp. The remaining optimal costs sum to OPT_E(S)-P, and their total weighted entropy is at most p ln n. Attaching baseline tails to this particular trunk gives cost at most

    P + a(OPT_E(S)-P) + c p ln n
    <= a OPT_E(S) + [c ln n - (a-1)K]p
    <= a OPT_E(S).

The Bellman optimization can only improve on that feasible candidate. At most (2m)^{O(K)} transcript states are explored. For fixed lambda the depth is O(log n), and composing this search with the quasipolynomial baseline remains quasipolynomial. Choosing lambda <= 1+epsilon/2 gives a (2+epsilon) approximation. There is no dependence on the smallest prior probability. This argument also explains why optimizing only a fixed small number of root queries would not eliminate the asymptotic entropy term.

## An exact polynomial joint endpoint decoder

After a positive answer and a legal geometric cut, represent each realized pattern by the pair (L,R). Every hull test is an ordered comparison on one of these two endpoints. A transcript therefore restricts the realized pairs to an axis-aligned rectangle. There are O(m^4) endpoint rectangles and O(m) possible thresholds per rectangle.

If a rectangle contains only pattern A, its terminal value is the stored child height H_A for maximum depth, or the stored raw expected contribution C_A for expected depth. At nonsingleton rectangles use

    H(rectangle) = 1 + min_threshold max{H(left),H(right)},
    E(rectangle) = mass(rectangle) + min_threshold {E(left)+E(right)}.

Only splitting thresholds are admitted. This yields an exact O(m^5) dynamic program among hull endpoint-comparison trees with the fixed continuations. Left and right questions may interleave. Sequential endpoint codes remain feasible comparison trees, so this optimization cannot worsen the complete objective. It can produce substantial instance improvements, especially with correlated pairs or unequal child heights.

Expected continuation costs sum to the same constant across any full decoder; they do not affect its optimal question order. Maximum-depth continuation heights do affect that order. A generic expected-optimal decoder does not dominate the sequential code pointwise and must not be substituted into a pointwise maximum-depth proof without using its actual heights.

## Geometry does not justify replacing four overhead queries by three

Here is a rational counterexample, also checked by the script. Use the normalized hull vertices, in cyclic order,

    (4,0),(3,2),(2,3),(0,4),(-2,3),(-3,2),
    (-4,0),(-3,-2),(-2,-3),(0,-4),(2,-3),(3,-2).

Every supplied query is u dot h > 1. Suppose v = (4,0) is known positive. The target hypothesis is

    h_0 = (2/5,0),

and the four alternatives are

    (17/50, -1/50), (17/50, 1/50),
    (12/25, 3/100), (12/25, -3/100).

All five hypotheses give a positive answer at v. The target has positive hull vertices (3,-2), (4,0), (3,2). Each alternative differs from the target on exactly one of the four boundary bits (3,-2), (3,2), (2,-3), (2,3), and the four differences are distinct. No hypothesis is on a query line. Consequently every hull-query tree certifying the target pattern must ask all four boundary questions.

Give h_0 conditional probability 1-4 epsilon and each alternative epsilon. The conditional entropy tends to zero, but expected endpoint decoding cost is at least 4(1-4 epsilon), tending to four. Thus no universal H_bits + 3 endpoint theorem holds, even with these explicitly planar realizable endpoint pairs.

This can be embedded in a mass-flat state: add the all-zero hypothesis h=(0,0), give the five-point cluster total mass b<delta, and give the origin mass 1-b. Every supplied minority cap has mass at most b<delta. Querying v positively gives exactly the above conditional example. Thus flatness alone does not remove the obstruction.

## The next improvement target

For a comparison block, split its newly hit mass into x positive only on v, y only on w, and z positive on both. With m=x+y+z, choosing v first gives complete nonentropy allowance relative to 2(t-1)m of

    5(x+z)+4y.

The reverse orientation gives 5(y+z)+4x. The best orientation therefore costs

    5m - max{x,y} = 4m + z + min{x,y}.

The theorem above drops this exclusive-mass saving. Preserving it in the scheduling objective, or coupling it to the entropy cap constraints, is a concrete possible route below 3.718677. There is no universal positive exclusive-mass fraction: a block may have all its new mass in the shared part z.

An order-sensitive penalty can also be written as rank-of-first-hit plus four minus two times the number of already queried neighbors of the first positive vertex. This pinning value is local in the grades of adjacent candidates, suggesting a multigrade DP augmentation. However the identity of a demand's earliest candidate within a tied grade must be carried consistently; merely replacing the grade charge by an average pinning credit is not valid.

## Checks

Running `python direction2-joint-decoding-check.py` succeeded. It checks the shifted-grade circular interval DP against exhaustive permutations on 150 seeded weighted instances with two to six block candidates; verifies all rational signs in the four-certification counterexample and its exact endpoint height; and certifies the approximation constants with rational logarithm intervals. These finite checks support the stated invariants and constants and do not replace their proofs.
