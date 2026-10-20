# Further polynomial expected-depth improvement from actual orientation savings

Prepared 13 October 2026. This supplements `poly-expected.md`, retaining the unrestricted planar supplied-line model and arbitrary positive rational priors.

**A mixture of actual first- and second-prefix orientation savings improves the certified polynomial expected-depth factor to less than 5.283310.** A simpler first-batch version gives 5.286244. Both are transfers through exact budgeted coverage, rather than identifications of actual schedule blocks with analytical optimum-witness blocks.

## Modify the deterministic shift objective

Keep the exact budgeted coverage sets and their greedy internal block order. In each scheduled hull-edge block, let x and y be the newly hit masses exclusive to its endpoints and z their shared mass. Query the endpoint with smaller exclusive mass first. The larger exclusive mass then exits on the second query with a pinned endpoint. With m=x+y+z, the complete nonentropy allowance is at most

    2(k-1)m + 5m - max{x,y}.

Define

    Pin(G) = sum_scheduled_blocks max{x,y}.

Choose the geometric shift by minimizing the rational surrogate

    2 MSSC_blocks(G) + 2p0 |G| - Pin(G).

The additive 3b in the stage bound is the same for every schedule, so it need not appear in the minimizing objective. The chosen shift's surrogate is at most its log-uniform average. This change is essential: minimizing only ordinary first-hit cost would not retain the averaged orientation saving.

All x,y,z values are computed from remaining hull-pattern demands on the all-negative route. Orientation does not alter which block first hits a demand. The actual first-positive endpoint classes retain their delta mass cap, so J>=b sigma(delta) holds for every considered shift.

## A valid lower bound from the actual first batch

Let w=w(S). Each endpoint cap has mass at most delta w, hence

    x+z <= delta w, y+z <= delta w,
    max{x,y} >= max{0,m-delta w}.

If a prefix has k executed blocks and covers mass H, its cumulative orientation credit is at least

    sum_i max{0,m_i-delta w} >= max{0,H-k delta w}.

Let m_t be the analytical supporting-prefix block masses from the optimum witness path and M_k=sum_{t<=k}m_t. Its comparison edge sequence covers at least M_k with its first k blocks. Exact maximum-weight k-coverage therefore ensures that the first geometric batch, with budget k=floor(u), covers H>=M_k. Even if this is already the final batch, its minimum cover uses at most k blocks and covers all positive mass. Consequently

    Pin(G_u) >= max{0,M_floor(u)-delta w floor(u)}.

For beta between 3 and 4, write

    P1 = ln 2 / ln beta,
    P2 = ln(3/2) / ln beta,
    P3 = ln(beta/3) / ln beta,
    mu = P1+2P2+3P3 = 3-ln 6/ln beta.

Under the log-uniform shift distribution,

    E[Pin(G_u)] >= sum_{k=1}^3 Pk (M_k-k delta w)_+
                 >= sum_{k=1}^3 Pk M_k - delta w mu.

The final inequality is the linear minorant a_+>=a. It avoids any unjustified transfer of a separately minimized actual-block mass profile.

## Combine the source profile with the averaged actual pin credit

Use e(t)=2[lambda_beta t+eta_beta-Phi_beta(t)] from the baseline report; e(1)=0 and e is nondecreasing. Define effective analytical coefficients

    a1 = 1,
    a2 = e(2)+P2+P3,
    a3 = e(3)+P3,
    a_t = e(t), t>=4.

Then

    sum_t m_t e(t) + E[Pin(G_u)]
        >= sum_t m_t a_t - delta w mu.

The first three a_t need not be in increasing order. The required condition is only

    max{a1,a2,a3} <= e(4).

Because every analytical m_t<=2delta w, and a_t>=e(4) for t>=4,

    sum_t m_t a_t
      >= e(4)b - 2delta w sum_{t=1}^3 [e(4)-a_t].

This is a direct threshold bound: write each coefficient as e(4)+(a_t-e(4)); cap each of the three negative contributions by m_t<=2delta w, and drop all later nonnegative contributions.

Put

    chi_or = e(4) - 2delta sum_{t=1}^3[e(4)-a_t] - delta mu
           = 2delta[e(2)+e(3)] +(1-6delta)e(4) + delta mu.

The last equality follows from sum_{t=1}^3 a_t=e(2)+e(3)+mu. Thus chi_or is the old discrete saving plus delta mu.

Combining with the retained zero waiting-time saving gives

    sum_t m_t e(t)+E[Pin(G_u)]+2p0/ln beta
      >= chi_or w + [2/ln beta-e(4)]p0
      >= chi_or b,

provided

    chi_or+2/ln beta >= e(4).

The second step uses w=b+p0. This condition and the threshold inequalities are certified below.

The complete flat-stage bound becomes

    W_stage <= A Delta + B_or b + (I-J)/ln 2,
    A = 2lambda_beta,
    B_or = 7-ln6/ln beta-chi_or,

with lambda_beta>=nu_beta. The same balanced-stage and telescoping proof therefore gives

    C_E(S) <= [A+max{ln2/h(delta), B_or ln2/sigma(delta)}] OPT_E(S).

## Certified parameters

Take

    beta = 3512863 / 10^6,
    delta = 142275675 / 10^9.

The exact rational logarithm certificate in `poly-expected-next-check.py` verifies

    lambda_beta > nu_beta,
    3 < 1/(2delta) < 4,
    7 < 1/delta < 8,
    e(4)-a1 > .0681529857,
    e(4)-a2 > .0823083400,
    e(4)-a3 > .1043293267,
    chi_or+2/ln beta > e(4),
    A+max{ln2/h(delta), B_or ln2/sigma(delta)} < 5286244/10^6.

Numerically, A≈3.591810178840039, B_or≈4.802209647030106 and chi_or≈.771720051343996. The additional orientation credit delta mu≈.223931910238722. These displayed decimals explain the values; the script's theorem certificate uses only exact Fraction bounds.

The algorithm remains polynomial. The shift breakpoints, greedy phase orders, orientations, and surrogate objectives are rational and computable in polynomial time. The prior's smallest positive weight does not enter the exponent. No quasipolynomial schedule DP or root lookahead is used.

## Verification and next route

`python poly-expected-next-check.py` passed its exact coefficient certificate, 10,000 analytical source-mass profile checks, and 1,200 actual circular block profile checks for the pin and prefix inequalities.

A subsequent prefix through phases 0,...,j also gives

    Pin(G_u) >= [M_floor(beta^j u)
                 -delta w sum_{i=0}^j floor(beta^i u)]_+.

One may choose different prefix indices on fixed shift ranges and average this single-credit lower bound; credits from two prefixes must not be added because both charge the same actual Pin. The following mixture gives the stronger certified result.

## Stronger certified first/second-prefix mixture

For shift u, put k0=floor(u), k1=floor(beta u). Consider the actual schedule through its first two phases, taking the entire schedule if it has already finished. Its block count is at most k0+k1 and its covered mass at least M_k1. Consequently both inequalities hold for the same actual total orientation credit:

    Pin(G_u) >= M_k0-delta w k0,
    Pin(G_u) >= M_k1-delta w(k0+k1).

If the first phase already finishes, its count is at most k0 and its covered mass is all b>=M_k1, which also proves the second inequality. If the second phase finishes, its final minimum cover uses at most k1 blocks and covers all b. Thus there is no missing-final-phase exception.

For any fixed alpha(u) in [0,1], their convex combination is a valid bound on Pin(G_u), charged once:

    Pin(G_u) >= (1-alpha(u)) M_k0 + alpha(u) M_k1
                 -delta w[k0+alpha(u)k1].

Set

    alpha0 = 7963376 / 10^7,
    alpha1 = 952407 / 10^6,

and use the following piecewise constant analysis function:

    alpha(u)=alpha0 for 1<=u<4/beta,
    alpha(u)=alpha1 for 4/beta<=u<5/beta,
    alpha(u)=1      for 5/beta<=u<6/beta,
    alpha(u)=0      for 6/beta<=u<beta.

In the first three ranges k0=1 and k1 is respectively 3,4,5. These rational breakpoints lie in the shift domain for our beta. This mixture changes only the proof; the implemented algorithm still chooses the shift by the same actual oriented surrogate.

Put

    q0 = alpha0 ln(4/beta)/ln beta,
    q1 = alpha1 ln(5/4)/ln beta,
    q2 = ln(6/5)/ln beta,
    mu_mix = 3-ln6/ln beta + 3q0+4q1+5q2.

Averaging the convex combination and adding the source e(t) discounts yields the effective coefficients

    a1 = 1,
    a2 = e(2)+1-P1+q0+q1+q2,
    a3 = e(3)+P3+q0+q1+q2,
    a4 = e(4)+q1+q2,
    a5 = e(5)+q2,
    a_t = e(t) for t>=6,

and the bound

    sum_t m_t e(t)+E[Pin(G_u)]
        >= sum_t m_t a_t - delta w mu_mix.

The increment q0 adds to coefficients 2,3; q1 to 2,3,4; and q2 to 2,3,4,5. The first coefficient remains exactly one because every considered prefix contains the first analytical block.

Use the rational threshold

    T = 345603 / 250000 = 1.382412.

The exact certificate establishes a1<T, a3<T, and a2,a4,a5,e(6)>T. Monotonicity of e gives a_t>=e(6)>T for all t>=6. Applying m1,m3<=2delta w gives the particularly short lower bound

    sum_t m_t a_t >= T b
                      -2delta w[(T-1)+(T-a3)].

Define

    chi_mix = T -2delta[(T-1)+(T-a3)] -delta mu_mix.

As in the first-batch proof, the complete source discount, orientation saving and zero waiting-time saving are at least chi_mix b whenever

    chi_mix + 2/ln beta >= T.

Indeed their lower bound is chi_mix w + [2/ln beta-T]p0, and w=b+p0.

The flat-stage inequality is therefore

    W_stage <= A Delta + B_mix b + (I-J)/ln2,
    B_mix = 7-ln6/ln beta-chi_mix.

Choose the rational parameters

    beta = 3512863 / 10^6,
    delta = 142671046 / 10^9.

The exact certificate verifies every coefficient-threshold inequality, the zero-slope condition, lambda_beta>nu_beta and

    A+max{ln2/h(delta), B_mix ln2/sigma(delta)} < 5283310/10^6.

Numerically, mu_mix≈3.223001891527124, a3≈1.360391132732657, chi_mix≈.807181228456225 and B_mix≈4.766748469917878. The maximum entropy ratio is below 1.691499244573601, and A≈3.591810178840039. Thus the unrestricted arbitrary-prior expected-depth polynomial factor is **strictly less than 5.283310**.

The slightly smaller numerical limit near optimal irrational mixing coefficients is not needed. The theorem uses fixed rational alpha values, a rational threshold, rational beta and delta, and exact logarithm enclosures in its certificate.

The additional 10,000 mixed analytical profile checks in `poly-expected-next-check.py` also passed. Each profile evaluates a convex combination of the two actual-prefix lower bounds, rather than adding the two credits.
