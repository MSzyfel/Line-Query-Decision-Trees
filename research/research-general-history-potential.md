# History-aware resource potentials and executable stage pricing

Auxiliary research note, 19 October 2026. No article edits and no
unrestricted approximation improvement are claimed. This connects the
polynomial matroid recognizer to the existing activation ledger and actual
palette-stage optimizer. It also sharpens the constants in the conditional
global contraction theorem.

## 1. Local history potentials in a shared query budget

For each member A of a polynomially supplied resource pool, restrict the
original response matrix to A. Verify or discover a loopless matroid in
which each restricted binary test has a flat response cell, using
[matroid discovery](research-general-matroid-discovery.md).
Let

    Phi_A(S)=M_(r_A(S intersect A)−1)(|S intersect A|),

with zero values at sizes zero and one. The existing rank-coding theorem
gives, for each query q,

    Delta_q Phi_A(S) <= |S intersect A|.

If q is constant on A, its deficit is exactly zero. Therefore nonnegative
weights lambda_A satisfying

    sum_(A containing h, q nonconstant on A) lambda_A <= 1
    for every original hypothesis h and original query q

give an all-subset Bellman-valid potential

    Phi(S)=sum_A lambda_A Phi_A(S),
    Phi(S)−sum_responses Phi(S_a) <= |S|.

This proof retains signed deficits. Sum the local inequalities with
nonnegative weights, then apply the pointwise query/hypothesis budget.
Consequently Phi(S)<=F*(S) for every subset, not only at the root.

**Relation to existing work.** The root LP and activation constraints are
already exactly Section 12 of the
[lower-bound note](uniform-decision-tree-lower-bounds.md), specialized to
these resource values. This is not a stronger root LP. The additions are
polynomial certificate discovery, a history-aware Bellman realization of
the same root objective, and its executable stage integration. Pair or
entropy resources can share the remaining endpoint capacity as before.

There are nm constraints and one variable per listed resource. Recognizing
each resource, evaluating its rank and coding table, and solving this
explicit rational packing LP all have polynomial runtime in the supplied
matrix and pool. No arbitrary-overlap profile separation problem is being
assumed solvable.

## 2. Conditional rank repairs the product-profile example

Consider coordinate equality queries on H=[Q]^d. For every coordinate i,
take every fiber obtained by fixing all the other coordinates. Each fiber
has a rank-two uniform matroid: its nonconstant queries are singleton
tests. Give every such resource weight one.

At a query on coordinate i, the fiber through h in direction i is the
only active resource containing h. Every other coordinate fiber sees a
constant query. Hence all weights fit the shared ledger, and

    Phi(H)=d(n/Q)[Q(Q+1)/2−1]=F*(H).

The number of fibers is dn/Q. Exact product factorization from the
[composition note](research-general-product-decomposition.md) can recover
the independent factors directly from the matrix; their conditional fibers
are then explicit. This construction needs neither a supplied affine
embedding nor an exponential subset family.

By contrast, the full natural-hierarchy arbitrary-profile LP has the
target-order gap on precisely these products; see the
[analytic profile-gap proof](research-general-affine-profiles.md). The
distinction is concrete: a coordinate fiber's actual conditional rank is
preserved by this resource, while arbitrary graph transversals collapse
its hierarchy-count features. Adding all non-coordinate affine tests would
invalidate the unit-weight all-axis ledger; on the complete affine system
use the global discovered affine matroid instead. The two examples are
not being conflated.

A root-tight potential can vanish on some nonsingleton subsets: a diagonal
that meets each axis fiber once has value zero in the product construction.
Terminal-code certification therefore remains an actual requirement.

## 3. Exact pricing accepts any fixed state potential

The existing `price_palette_stage` in
[the palette implementation](research-general-lifting-global.py) now accepts
an optional `state_potential(S)` callback. The default remains the earlier
unrestricted binary coding cost. For a fixed incumbent T, write F_T(S) for
the raw cost of its actual restriction to S, suppressing constant queries.
For an executable partial stage P on S with output cells R, set

    Gamma_T(P)=F_T(S)−sum_R F_T(R),
    Delta_Phi(P)=Phi(S)−sum_R Phi(R).

For nonnegative prices gamma,a, the optimizer exactly maximizes

    gamma Gamma_T(P)+a Delta_Phi(P)−W(P)

over policies using a supplied query palette. It uses terminal energy
gamma F_T(R)+a Phi(R), charging actual work at every performed query.
All output cells, including unfinished and missing-response cells, remain
in the accounting. Negative drops are never clipped.

For d palette tests, there are at most 3^d binary response contexts.
Thus a supplied O(log(n+m))-size palette is polynomial, as long as
evaluating Phi is polynomial. Searching all such palettes would still
be superpolynomial and is not part of this claim. The callback is an
evaluation interface; the caller must supply its lower-bound proof.

## 4. A sharper conditional contraction theorem

Fix throughout one complete incumbent T, one nonnegative potential Phi
valid on every subset, and constants 0<=gamma<1, a>=0, alpha>=1. Construct
a complete output recursively from executable stages satisfying

    W(P)<=gamma Gamma_T(P)+a Delta_Phi(P).

At terminal cells R use actual codes G_R satisfying

    F(G_R)<=min(F_T(R),alpha Phi(R)).

The same Phi and the same restricted reference T must be used throughout
the pass. Independently resetting either at descendants would require
additional accounting.

**Theorem.** The complete result satisfies

    F_new <= gamma F_T(H)+max(a,(1−gamma)alpha) F*(H).        (1)

**Proof.** Let R run over terminal cells. Their partition has

    sum_R Phi(R) <= sum_R F*(R) <= F*(H).

For the second inequality, restrict one global optimum tree to each cell;
its retained path lengths sum to at most the original total. No
superadditivity of Phi is needed. Telescoping both actual incumbent
credits and signed potential drops gives

    F_new <= gamma F_T(H)+a Phi(H)
             +sum_R [F(G_R)−gamma F_T(R)−a Phi(R)]
          <= gamma F_T(H)+a Phi(H)
             +[(1−gamma)alpha−a] sum_R Phi(R).

If the displayed coefficient is nonnegative, bound both Phi(H) and the
terminal sum by F*(H), yielding coefficient (1−gamma)alpha. If it is
negative, discard its nonpositive contribution and bound Phi(H) alone,
yielding coefficient a. This proves (1).

In particular a=(1−gamma)alpha gives

    F_new <= gamma F_T(H)+(1−gamma)alpha F*(H).

With a fixed gamma<1 this contracts toward alpha, rather than the weaker
`a/(1−gamma)+alpha` fixed point obtained by separately charging both
resources in the earlier sufficient theorem. A polynomial number of
passes reaches alpha+epsilon when each complete pass satisfies the stated
coverage/certification requirements and epsilon is inverse polynomial.
This is a conditional theorem: useful stages or certified terminal codes
have **not** been proved available on arbitrary instances.

## 5. Exact verification

[The checker](research-general-history-potential.py) verifies:

- 5,392 all-subset Bellman comparisons on coordinate products, including
  sampled subsets at n=27; all smaller selected instances are exhaustive.
- Exact root values 8,24,30,135 on four products, equal to their independent
  exact optimum formulas.
- 36 actual stage executions and independent recursive signed-gain
  optimizations, with three rational coefficient pairs.
- The affine n=9 certificate with singleton noise, the near-pencil query
  with drop −5, and rejection of an overloaded resource ledger.
- 18 complete stage-plus-terminal comparisons against (1), including
  prices below, equal to, and above (1−gamma)alpha. Exact optimum and
  all-subset terminal-ratio calculations here are validation only.

The previous palette regression also passes all 144 complete/fallback,
144 weighted-pricing, and 144 mixed-stage comparisons after adding the
optional callback. Independent agents audited the sharper contraction
proof and the identification of the root ledger with existing Section 12.

Run `python research-general-history-potential.py`; results are saved in
[JSON](research-general-history-potential-results.json). This note improves
certificate discovery and a conditional reduction, with no unrestricted
ratio claim.
