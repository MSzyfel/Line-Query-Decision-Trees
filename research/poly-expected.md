# Polynomial improvement for arbitrary-prior expected depth

Prepared 13 October 2026. This report concerns the unrestricted binary supplied-line, unit-cost planar identification model. It uses the manuscript's common-witness geometry, supporting-prefix credit, geometric-batch interval ordering, alphabetic endpoint coding, and capped discovery entropy lemmas. The proof makes no bounded-weight, fixed-direction, singleton-query, or cap-size assumption.

**A deterministic polynomial-time algorithm achieves expected depth strictly less than 5.312551 times optimum for every positive rational prior.** This improves the manuscript's polynomial bound 5.445944. It does not use the quasipolynomial scheduling DP or logarithmic-depth lookahead.

The proof below is fully compatible with the manuscript's existing recursion. The change is to apply its polynomial geometric-batch interval scheduling lemma to adjacent hull edges, rather than to individual hull vertices, and to account for discovery and endpoint decoding together.

## Construction

At a mass-flat state S, form the full convex hull K of the normalized query vectors together with the origin. Use edges of the full hull as block candidates. A block executes its real endpoints in one chosen orientation; an origin endpoint is the free constant-negative answer and is omitted. Repeated or already known endpoint queries are omitted. Degenerate hulls have at most two real vertices and can be handled directly; alternatively execute all their real hull tests, applying the same upper bounds.

An original query's one or two supports lie in an edge block. If it has only one supporting vertex, choose an incident edge. Enlarging the support set this way can only make a positive hit occur earlier. The origin must remain in the cyclic hull order: deleting it and calling its two real neighbors an edge can create a pair that is not adjacent in K.

A nonzero hull pattern is a circular interval of vertices. The edge blocks intersecting that vertex interval are a circular interval of edge positions. Thus the existing exact budgeted interval coverage DP and geometric-batch ordering lemma apply without alteration to the block incidence table.

Write b for the total mass of nonzero patterns, p0 for the all-zero mass, and k_A for the first block that hits pattern A. Apply the existing geometric-batch algorithm with beta = 3512863/10^6 and objective

    sum_{A != A0} w(A) k_A + p0 K_schedule.

Its selected shift minimizes this actual rational objective among its polynomially many candidate schedules. Multiplying by two and subtracting b changes neither the minimizing shift nor the order, so this also optimizes the shifted block objective needed below.

Query blocks until the first positive hull answer or an earlier singleton inference. Recover the rest of the full hull pattern by the supplied endpoint comparisons, then recurse on its class. In the balanced case use a supplied line whose two side masses are at least delta w(S), where

    delta = 138821934 / 10^9.

## Joint discovery and endpoint cost

If the first endpoint of block k is positive, discovery costs at most 2k-1 queries. The two alphabetic endpoint codes add at most four overhead queries plus the conditional pattern entropy in bits. The complete nonentropy allowance is therefore

    2k-1 + 4 = 2(k-1)+5.

If the second endpoint is the first positive answer, its preceding adjacent endpoint is known negative. One endpoint is pinned. Discovery costs at most 2k, and the remaining endpoint code adds at most two overhead queries. The complete allowance is at most

    2k+2 <= 2(k-1)+5.

An edge incident to the origin contains one real query and obeys the same bound. Cached answers and early inference only decrease the work. The zero class costs at most 2K_schedule.

Let I be full-pattern information and J the information in the actual discovery transcript partition. The entropy chain-rule argument from the manuscript therefore gives

    W_stage <= 2 sum_{A != A0} w(A) k_A + 3b
               + 2p0 K_schedule + (I-J)/ln 2.

This is the key coefficient: it is **3b after using ordinary first-hit ranks**, or equivalently 5b after shifting each positive rank by one. Adding 5b to the ordinary first-hit sum would lose the improvement.

Every nonzero actual discovery exit remains contained in one positive hull cap of mass less than delta w(S). The edge union may have mass as large as 2delta w(S), but the actual first positive endpoint event still has the original delta cap. Hence the capped entropy lemma still yields

    J >= b sigma(delta),
    sigma(delta) = -k delta ln delta - r ln r,
    k = floor(1/delta), r=1-k delta.

## Compare the polynomial schedule to an optimal witness path

Use the manuscript's notation Phi_beta, lambda_beta, nu_beta, eta_beta and put

    g_beta(t) = lambda_beta t + eta_beta - Phi_beta(t).

The existing integral formula gives

    g_beta(1)=0,
    g_beta(t) = [1/(2ln beta)] integral_1^t
               (beta+1 - (floor x + floor(beta x))/x) dx.

Consequently g_beta is nonnegative and nondecreasing. Define e_beta(t)=2g_beta(t).

Follow the common witness through an expected-optimal tree, with q queries. Replace each query by an edge block containing its supports. If t_A is the manuscript's first supporting-hit index, the first-hit index of this edge comparison sequence is no larger than t_A. Removing duplicate blocks and unproductive blocks preserves that inequality. If there is no zero pattern and its terminal nonzero singleton has not been hit, append an incident edge; its index is at most q+1 and its restriction credit is q. With a zero pattern no terminal append is needed, and the minimum block cover size k0 is at most q.

Set

    Dplus = sum_{A != A0} w(A)(t_A-1).

Supporting-prefix credit gives Dplus + p0 q <= Delta, where Delta is the expected-optimum decrease upon revealing the full hull pattern. When p0=0 this reads Dplus<=Delta.

The existing geometric-batch lemma, applied to blocks, gives

    MSSC(G) + p0 |G|
        <= sum_{A != A0} w(A) Phi_beta(t_A) + p0 Z_beta(k0).

Multiply by two and add 3b. Since

    2Phi_beta(t) = 2lambda_beta(t-1)
                  + 2Phi_beta(1) - e_beta(t),
    Z_beta(k0) <= nu_beta k0 - 1/ln beta,

the complete stage satisfies

    W_stage <= 2lambda_beta Dplus + 2nu_beta p0 q
               + [3+2Phi_beta(1)] b
               - sum_t m_t e_beta(t) - 2p0/ln beta
               + (I-J)/ln 2,

where m_t is the total nonzero pattern mass first support-hit in analytical block t. This uses only monotonicity of Phi to replace actual edge-comparison hit times by t_A; the saving is evaluated in the resulting upper bound at t_A. It does not need an equality of those two indices.

For the rational beta above, lambda_beta>nu_beta, certified below. Thus the first two terms are at most A Delta, with

    A = 2lambda_beta = (beta+1)/ln beta.

## Discrete flat-state savings

Each analytical block contains at most two positive hull caps, so m_t < 2delta w(S). This is an analytical witness-block constraint; it must not be confused with the smaller delta cap on actual individual positive discovery exits.

Put N=floor(1/(2delta)) and s=1-2delta N. By the same earliest-fill argument as the manuscript's flat discrete-credit lemma,

    sum_t m_t e_beta(t) >= w(S) P_delta(b/w(S)),

where P_delta(x) fills mass 2delta at the smallest coefficients e_beta(t), with a final remainder. Write

    chi = P_delta(1)
        = 2delta sum_{t=1}^N e_beta(t) + s e_beta(N+1).

If

    e_beta(N+1) <= chi + 2/ln beta,

then the monotone-slope argument gives

    P_delta(x) + 2(1-x)/ln beta >= x chi.

Here 1-x=p0/w(S). Therefore positive and zero-route savings together are at least chi b, and the polynomial full-pattern stage obeys

    W_stage <= A Delta + B b + (I-J)/ln 2,
    B = 3+2Phi_beta(1)-chi.

For our parameters floor(beta)=3, N=3 and floor(1/delta)=7, so

    B = 7 - ln 6/ln beta
        - 2delta[e_beta(2)+e_beta(3)]
        - (1-6delta)e_beta(4).

This retains both the discrete positive-hit discounts and twice the zero waiting-time discount, which is essential to obtaining the stated constant.

## Global factor and exact certificate

Choose

    c = max{1/h(delta), B/sigma(delta)},
    h(delta) = -delta ln delta -(1-delta)ln(1-delta).

The balanced stage has cost w(S)<=I/h(delta)<=cI. For a flat stage, J>=b sigma(delta), so B b <= cJ. Also c>=1/ln 2 because h(delta)<=ln 2. Therefore

    B b + (I-J)/ln 2 <= cI.

Both stages satisfy W_stage<=A Delta+cI. Telescope over the recursive tree to obtain

    C_E(S) <= A OPT_E(S) + c E(S)
           <= [A + c ln 2] OPT_E(S).

The exact rational logarithm intervals in `poly-expected-check.py` certify

    lambda_beta > nu_beta,
    A in [3.591810178840038..., 3.591810178840040...],
    B in [5.013509704362398..., 5.013509704362401...],
    max{ln 2/h(delta), B ln 2/sigma(delta)}
         < 1.720740274489660,
    e_beta(4) < chi + 2/ln beta,
    A + max{ln 2/h(delta), B ln 2/sigma(delta)} < 5312551/10^6.

The logarithms are enclosed using the convergent atanh series after rational scaling to [1,2]. All assertions compare exact Fractions, rather than floating-point values. The certified ratio is strictly below **5.312551**.

For numerical orientation only, the optimized continuous limit of this particular analysis is approximately 5.312550401655 near beta=3.512862417252 and delta=0.138821941965. This is not an additional certified theorem; the rational parameters and bound above are the theorem.

## Complexity and restrictions

There are polynomially many edge candidates, demands, cardinality-budget coverage calls, and rational shift breakpoints. The integer budgets are at most the minimum cover size, which is at most the number of hypotheses. The geometric-batch schedule uses a fixed rational beta. All algorithmic comparison objectives use exact sums of rational prior weights and integer ranks; the logarithms appear only in the analysis. There is no dependence in the running-time exponent on the smallest nonzero prior probability.

Each recursive full-pattern partition or balanced query is proper at nonsingleton states, so the recursion has O(n) states. Endpoint coding uses only supplied hull lines. Standard deletion of constant queries yields a proper identifying tree with at most n leaves and n-1 internal nodes. The whole algorithm is polynomial in the incidence/geometric input and its rational bit length.

## Further polynomial improvements that remain unproved

Within one actual block, let x,y be the newly hit masses exclusive to its two endpoints, and z the shared mass. Querying the endpoint with smaller exclusive mass first puts the larger exclusive mass on the pinned second exit. The complete overhead allowance improves from 5m to

    5m-max{x,y}, m=x+y+z.

Because each endpoint cap has mass at most delta w(S),

    max{x,y} >= max{0,m-delta w(S)}.

This is a valid instance-dependent saving and should be used in the implementation when selecting among candidate schedules. However these are **actual scheduled block** masses, while the discrete profile e_beta(t) is evaluated on **analytical optimal-witness blocks**. Adding their independently minimized profiles without a transfer argument would be invalid. A sharper polynomial proof should bound actual orientation savings and actual discovery entropy within the geometric-batch analysis, rather than splice them into the witness profile.

The strongest other candidate is an improved polynomial ordering lemma for circular intervals. The present constant is dominated by A≈3.59181, twice the positive-target batch coefficient. A scheduling approximation to the shifted block objective below the current ~1.7959 could yield a much larger improvement. Exact budgeted coverage alone does not make optimal prefixes nested, so independently choosing every optimal budget prefix is insufficient.

## Verification

`python poly-expected-check.py` passed. In addition to the exact theorem certificate, it checked 1,400 small seeded circular-interval geometric-batch schedules for complete coverage, the existing length bound, and the shifted-versus-unshifted joint cost identity. These finite checks support the construction; the arguments above provide the general proof.

`poly-expected-opt.py` is a separate floating-point exploratory optimizer. It is not used for the theorem certificate.
