# A general polynomial expected-depth factor below 5.197569

This report establishes a further algorithmic improvement in the unrestricted
binary, unit-cost, supplied-line planar model with arbitrary positive rational
priors. It replaces the previously certified **<5.272565** factor by

    C_E(S) < 5.197569 OPT_E(S).

The new ingredient changes the actual candidate schedules: the first exact
coverage batch can use a different small budget, and the first two geometric
batches can be merged. The subsequent geometric batches, rational adaptive
block modes, capped discovery entropy, and disjoint full-pattern recursion
remain the accepted constructions. No existing TeX file was edited.

## 1. Deterministic polynomial algorithm

Use the accepted rational entropy tent and block-mode choice from
`further-expected.md`, with

    p*=21317/125000, h*=41183/62500,
    c=228683/103683, d=250000/103683.

For newly hit block masses x<=y and shared mass z, select stop mode or
query-both mode according to the larger rational saving

    D=max{y, x+y-z+min{(h*/p*)x, h*(x+z), (h*/p*)z}}.

The coarsened discovery partition J* still has every positive cell inside
one supplied cap. Thus J*>=b sigma(delta), where b is the positive-pattern
mass. Its accepted affine block credits are

    D>=0, D>=m-delta w, D>=c m-d delta w.

Set

    beta=3512863/10^6, delta=155223384/10^9.

For each geometric shift u in [1,beta), write k_j=floor(beta^j u), and
retain the fixed exact maximum-weight coverage sets Q_k and the minimum
cover Q_* from the existing interval DP. Try the following initial-batch
variants:

* For each q in {1,...,6} with q<k_1, use budgets q,k_1,k_2,... .
* Use budgets k_1,k_2,..., merging the old first two batches.

At every budget k below the minimum cover size k_min, process Q_k; otherwise
process Q_* and finish. Order the candidates within the batch greedily by
their newly hit remaining mass. Omit duplicate and unproductive blocks.
Execute the accepted rational block modes, and choose among all schedules
by minimizing the rational objective

    2 MSSC_block(G)+2p_0 |G|-sum_blocks D.

All geometric breakpoint enumeration remains polynomial. There are only
seven possible initial variants per shift interval. Include the original
first budget k_0 whenever it is feasible; here k_0<=3<k_1. A constant
initial budget does not change the polynomial-bit geometry, exact coverage
oracle, proper output-tree size, or disjoint recursive class construction.
For a merged initial batch, k_1 can be as large as twelve; it is already one
of the polynomially computed coverage budgets. The proof distributions
below are fixed analytical choices, not optimization oracles used by the
algorithm.

## 2. Exact change to the batch accounting

Let phi_u(t) denote the unaveraged first-hit upper bound in the existing
geometric-batch proof:

    phi_u(t)=(k_0+1)/2
             +(1/2) sum_{j>=0}(k_j+k_{j+1}) 1[t>k_j].

For the variant q,k_1,k_2,..., its corresponding bound is

    phi_{u,q}(t)=(q+1)/2 +(q+k_1)/2 1[t>q]
                +(1/2) sum_{j>=1}(k_j+k_{j+1}) 1[t>k_j].

The exact doubled improvement is therefore

    d_q(u,t)=2(phi_u(t)-phi_{u,q}(t))
      =k_0-q+(k_0+k_1)1[t>k_0]-(q+k_1)1[t>q].       (2)

For the merged initial batch k_1,k_2,..., it is instead

    d_merge(u,t)=k_0-k_1+(k_0+k_1)1[t>k_0].           (3)

Both formulas come directly from the nonincreasing within-batch greedy
weights. They remain upper bounds when the minimum cover causes early
completion, because the unrolled nonnegative residual terms merely extend
the schedule accounting beyond its final phase. A changed first budget can
accelerate some comparison ranks and delay others; these signed corrections
retain both effects.

The zero-pattern waiting time must be changed simultaneously. Relative to
the old per-shift length bound

    k_min+sum_{j:k_j<k_min} k_j,

the q variant changes it by

    z_q(u,k_min)=q 1[q<k_min]-k_0 1[k_0<k_min],       (4)

and the merged variant changes it by

    z_merge(u,k_min)=-k_0 1[k_0<k_min].                (5)

Unlike a positive first-hit bound, (4) prices the entire all-negative route.
The proof below verifies that the average change is nonpositive for every
possible k_min; no zero-pattern waiting credit is discarded.

## 3. Fixed rational eight-row proof distribution

Let M_q=sum_{t<=q}m_t denote the original analytical witness mass covered
through comparison rank q. As in the accepted proof,

    m_t<=2 delta w, sum_t m_t=b,
    Delta_E>=sum_t m_t(t-1),

with the separately charged zero-pattern witness contribution. Exact
coverage makes the first batch hit at least M_q. Since it processes at most
q blocks, the total actual saving has the valid lower bounds

    A_q=M_q-delta w q,
    C_q=c M_q-d delta w q,
    0.

They may be negative; each is still a lower bound. In a merged variant the
same first-batch bounds apply with q=k_1. Different choices below are convex
mixtures, so no actual saving is counted twice.

Use the rational mixing weights

    v1=95240701/10^8,
    v2=37279986/10^8,
    v3=4271137/10^8,
    v4=33933837/10^8,
    v5=36583316/10^8.

Average over the usual log-uniform shift density 1/(u ln beta). Conditional
on each shift, use this analytical distribution of schedule variants and
saving minorants:

| Shift range | Variant and saving minorant |
|---|---|
| [1,4/beta) | Merge to initial q=3; use C_3. |
| [4/beta,5/beta) | Merge to initial q=4; use A_4 with weight v1 and zero with weight 1-v1. |
| [5/beta,2) | Original initial q=1; use C_1. |
| [2,8/beta) | Initial q=1 and C_1 with weight v2; original q=2 and C_2 with weight 1-v2. |
| [8/beta,3) | Original initial q=2; use C_2. |
| [3,11/beta) | Initial q=2 and C_2 with weight v3; original q=3 and C_3 with weight 1-v3. |
| [11/beta,12/beta) | Original initial q=3; use C_3. |
| [12/beta,beta) | Original q=3 and C_3 with weight v4; q=5 and A_5 with weight v5; q=6 and zero with weight 1-v4-v5. |

All regular variants satisfy q<k_1. The two merged rows have k_1 exactly
three or four. Rows spanning several k_1 values use the original first
budget and therefore have correction zero.

## 4. A finite coefficient certificate and monotone tail

Use the old geometric functions Phi_beta and

    e_beta(t)=2[lambda_beta(t-1)+Phi_beta(1)-Phi_beta(t)].

Begin with a_t=e_beta(t), mu=0. A row [l,r) has probability
P=ln(r/l)/ln beta. An option with conditional weight v, initial budget q,
correction d_q(t), and saving minorant s M_q-rho delta w contributes

    a_t += P v [d_q(t)+s 1[t<=q]],
    mu  += P v rho.

For a merged option use (3) as its correction. This definition gives

    sum_t m_t e_beta(t)
       +E[phase correction + actual saving]
       >= sum_t m_t a_t-delta w mu.                    (6)

Set tau=20718779/10^7=2.0718779. Exact rational logarithm enclosures prove

    a_1 = 1.22325584614... < tau,
    a_2 > 2.07187805487,
    a_3 > 2.07187805533,
    a_4 > 2.07187805471,
    a_5 > 2.07187805502,
    a_6 > 2.07187805311,
    a_7 > 2.07187805484.

Every first-batch saving cutoff is at most six, and every phase correction
is constant for t>=7. Consequently a_t=e_beta(t)+constant for all t>=7.
The accepted monotonicity of e_beta controls the infinite remaining tail.
Only analytical rank one lies below tau, and its mass is at most 2 delta w:

    sum_t m_t a_t >= tau b-2 delta w(tau-a_1).

Define

    chi=tau-2delta(tau-a_1)-delta mu,
    B=3+2Phi_beta(1)-chi=7-ln6/ln beta-chi.

The exact certificate gives

    mu < 4.379796439666,
    chi > 1.128579101530,
    B < 4.445350596844.

## 5. Certify every zero-pattern waiting length

Let D(k) be the shift- and variant-averaged change (4) or (5). The exact
certificate gives

| Minimum cover size k | D(k) |
|---|---:|
| 1 | 0 |
| 2 | < -0.24242759363 |
| 3 | < -0.31657832437 |
| 4 | < -0.36504839634 |
| 5 | < -0.36504839634 |
| 6 | < -0.32434872768 |
| 7 | < -0.28498842133 |

Every regular changed initial budget is at most six and every k_0 is at
most three. Equation (5) depends only on k_0 once k>k_0. Hence D(k)=D(7)
for all k>=7. These finitely many inequalities establish D(k)<=0 for all
minimum cover sizes, retaining the old mean length bound

    E[|G|]<=Z_beta(k_min)<=nu_beta k_min-1/ln beta.

Moreover chi+2/ln beta>tau, with substantial positive slack. Thus the old
zero-route credit pays the conversion of the w terms in (6) to b terms.
There is no assumption that the all-zero prior is small.

## 6. Full stage and final approximation factor

The accepted physical and entropy accounting still gives

    W_pattern <= 2 MSSC_block+2p_0 |G|-Save+3b+(I-J*)/ln2.

The algorithm's minimum rational surrogate is at most its average under
the table distribution. Equations (2)--(6), the rank-one mass cap, and the
zero credit therefore yield

    W_pattern <= A Delta_E+B b+(I-J*)/ln2,
    A=2 max{lambda_beta,nu_beta}=(beta+1)/ln beta
      <3.591810178841.

The chosen beta satisfies lambda_beta>nu_beta. The coarsened transcript
continues to satisfy J*>=b sigma(delta). The usual balanced-state entropy
decrease is h(delta). The manuscript's existing expected-cost potential
induction therefore gives the general approximation factor

    R=A+max{ln2/h(delta), B ln2/sigma(delta)} <5.197569.

Here 6<1/delta<7, and

    sigma(delta)=-6delta ln delta-(1-6delta)ln(1-6delta),
    h(delta)=-delta ln delta-(1-delta)ln(1-delta).

Exact rational upper enclosures give R<5.197568047723. The rounded public
bound 5.197569 leaves a clear certification margin. No instance property,
restricted prior range, or optimum parameter is supplied to the algorithm.

## 7. Verification and boundaries of the result

`next-expected-check.py` uses Fraction arithmetic and rigorously bounded
atanh logarithm series for the complete constant certificate. It checks
the existing entropy tent, all seven exceptional rank coefficients, the
constant monotone-tail reduction, every exceptional zero waiting change,
the zero-credit inequality, and the final rational upper bound. It also
checks both exact phase-correction identities and 1,950 modified-batch
comparisons against random source orders on small circular interval
families, including early minimum-cover completion. All checks pass.

`next-expected-phase-opt.py` records the exploratory LP that found the
schedule family and proof mixture. It is not needed by the algorithm or
the theorem. The final certificate has fixed rational weights and contains
no reliance on floating-point LP optimality.

I also tested a valid extra minorant obtained from disjoint phase savings:
use slope c in the first phase and slope one in the second to obtain
(c-1)M_q+M_{k_1}-delta w(dq+k_1). This is valid by summation of the
actual disjoint phase masses and their cumulative coverage inequalities.
It did not improve the optimized certificate for the present schedule
family. A coarse beta search likewise placed the best result near the
existing lambda/nu crossing. Neither observation is a lower bound for
other algorithms or proof distributions.
