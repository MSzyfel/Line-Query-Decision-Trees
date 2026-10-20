# Randomized per-hypothesis depth and a polynomial-size master LP

Status: proved, with independent exact small-instance checks. This report
does not change the active manuscript. Parent review is requested before
creating `sections/13-randomized-programming.tex`.

## What is improved, and which objective is meant

Let H have n identifiable hypotheses. Write d_T(h) for the depth of h in
a legal supplied-line tree T. For a distribution mu over legal trees,
consider the Las Vegas objective

    R(mu) = max_h E_{T ~ mu} d_T(h),    R* = min_mu R(mu).

The hidden hypothesis is chosen before the algorithm's random bits. Every
sampled tree identifies every hypothesis without error. This is a distinct
objective from deterministic maximum depth and from the ordinary expected
depth under a given prior. It is also different from E_T[max_h d_T(h)].

There is a proved approximation-preserving transfer: an alpha-approximation
for arbitrary positive rational prior expected depth gives an
(alpha+epsilon)-approximation for R*, in O(n/epsilon^2) oracle calls. After
those calls, an explicit polynomial-size linear program improves the
mixture and compresses its support to at most n legal trees. It is not
necessary to enumerate all legal trees or invoke an exponential LP solver.

Consequently the current polynomial expected-depth result gives a
polynomial approximation below 5.182976 for this randomized objective.
The quasipolynomial expected-depth oracle gives a (2+epsilon)
approximation for R*, with the same quasipolynomial asymptotic exponent.
Both comparisons are with the randomized optimum R*, not with OPT_W.

## Why the new objective is substantive

Three parabola points (t,t^2), t=0,1,2, admit strict supplied singleton tests

    4y - 8t0 x + 4t0^2 - 1 = 0,    t0=0,1,2.

On its own point the left side is -1, and on any other point it is at least
3. Thus these are legal integer-coefficient binary line tests and no input
point lies on a supplied line. Every proper tree has depth vector equal to
a permutation of (1,2,2). Deterministic maximum depth is 2. The uniform
mixture of the three depth vectors has per-hypothesis expected depth 5/3.
The uniform prior makes every tree's expected depth 5/3, proving R*=5/3.

By contrast, for a fixed prior pi,

    min_mu sum_h pi_h E_mu d_T(h) = min_T sum_h pi_h d_T(h),

because the left-hand cost is linear in the mixture. Likewise

    min_mu E_mu[max_h d_T(h)] = min_T max_h d_T(h).

The essential supremum over sampled tree heights has the same optimum.
These equalities concern the optimization objectives; they do not rule out
randomized approximation constructions for the original objectives.

## Proper trees and the exact minmax LP

Contract every query constant on its current hypothesis set. Each
remaining query properly splits that set, so a tree identifying n
hypotheses has n leaves, n-1 internal nodes, and all depths at most
L=n-1. There are finitely many such supplied-query trees; call their set
T. A zero-error adaptive randomized algorithm that terminates almost
surely for each hypothesis induces a distribution on this finite set:
condition on its random seed, discard the probability-zero union of bad
seeds for the finitely many hypotheses, and contract its constant tests.
This contraction can only improve its query depths.

The finite primal LP is

    minimize r
    subject to sum_T mu_T d_T(h) <= r       for every h,
               sum_T mu_T = 1,             mu_T >= 0.

Its dual is

    maximize lambda
    subject to lambda <= sum_h pi_h d_T(h) for every T,
               sum_h pi_h = 1,             pi_h >= 0.

Finite LP duality therefore gives

    R* = max_{pi in Delta(H)} OPT_E(pi).

The dual may use zero prior masses. Its comparison tree must still identify
all of H. The implementation below never submits zero masses to the
expected-depth oracle: every weight remains a strictly positive integer.
Thus the existing arbitrary-positive-prior theorem applies directly.
No support-dependent oracle extension is assumed.

For n>=2, the uniform-prior binary coding lower bound gives

    R* >= OPT_E(uniform) >= log_2 n.

For completeness, each proper tree's leaf depths satisfy Kraft's
inequality. Jensen's inequality applied to 2^{-x} then gives
2^{-average depth} <= 1/n, proving the bound. The n=1 case is a single
leaf with cost zero and is handled separately.

## One algorithm: best responses, then optimal mixing

Assume a deterministic oracle A_E returns a legal proper tree on every
strictly positive rational prior pi and satisfies

    c_pi(A_E(pi)) <= alpha OPT_E(pi),    alpha >= 1.

Fix rational 0<epsilon<=1. Set

    eta = epsilon/(2 alpha),    K = ceil(8 alpha (n-1)/epsilon^2).

Write eta=p/q in lowest terms, and initialize integer weights w_h=1.
For n=1 return the single identifying leaf. Otherwise, for t=1,...,K:

1. Set pi_{h,t}=w_h/sum_g w_g.
2. Obtain T_t=A_E(pi_t), and compute every integer depth d_{T_t}(h).
3. Update w_h <- w_h (qL + p d_{T_t}(h)).

The common factor (qL)^t cancels when weights are normalized. This is
exactly the usual rational multiplicative update
w_h <- w_h(1+eta d_{T_t}(h)/L), with no logarithmic or irrational
algorithmic comparisons.

Now solve the *restricted master LP*

    minimize r
    subject to sum_{t=1}^K mu_t d_{T_t}(h) <= r   for every h,
               sum_t mu_t = 1,                  mu_t >= 0.

Take an optimal basic solution. At execution time sample t according to
its exact rational probabilities and execute T_t. The LP is part of the
algorithm: it improves its actual mixture, rather than merely serving as
an interpretation of the analysis. The uniform mixture is feasible, so
this last step cannot worsen the proved bound.

## Proof of the approximation coefficient

Let g_{h,t}=d_{T_t}(h)/L in [0,1]. Analyze the scaled weights whose update is
1+eta g_{h,t}, and put W_t=sum_h w_{h,t}. Concavity gives

    log(1+eta x) >= x log(1+eta),    0<=x<=1.

Consequently, for each h,

    log w_{h,K+1} >= log(1+eta) sum_t g_{h,t}.

On the other hand,

    W_{t+1}/W_t = 1+eta sum_h pi_{h,t} g_{h,t},

and log(1+x)<=x implies

    log W_{K+1} <= log n + eta sum_t sum_h pi_{h,t} g_{h,t}.

Comparing these inequalities and multiplying by L/K gives

    max_h (1/K) sum_t d_{T_t}(h)
       <= [eta/log(1+eta)] (1/K) sum_t c_{pi_t}(T_t)
          + L log n/[K log(1+eta)].

For 0<eta<=1,

    log(1+eta) >= eta/(1+eta) >= eta/2,
    eta/log(1+eta) <= 1+eta.

Each oracle response has cost at most alpha R*, by the LP dual identity.
Therefore the uniform mixture obeys

    R(uniform mixture) <= (1+eta) alpha R* + 2L log n/(eta K).

Since log n <= (log 2) R* < R* for n>=2, its coefficient is strictly less
than

    (1+eta) alpha + 2L/(eta K) <= alpha + epsilon.

The last inequality is an exact rational consequence of the chosen eta
and K: alpha eta=epsilon/2 and 2L/(eta K)<=epsilon/2. The master LP can
only improve this bound. This proves a strict (alpha+epsilon) guarantee
against the randomized optimum.

The entropy lower bound removes an unnecessary extra factor n from a
generic bounded-payoff additive-regret construction. Only O(n/epsilon^2)
oracle calls are required, rather than O(n^2 log n/epsilon^2).

## Finite bit complexity, support compression, and exact sampling

The updated integer factor is at most qL(1+eta). After K rounds each
weight therefore has at most

    O(K[log(qL)+log(1+eta)])

bits. This is polynomial in n, 1/epsilon, and the bit lengths of alpha
and epsilon. Every normalized prior is strictly positive and rational.
The expected-depth oracle's running time is polynomial in this bit length;
the exponent must not depend on the smallest prior mass. The existing
oracle has this property. The generated trees have O(nK) total nodes.

The restricted master LP has K probability variables, one r variable,
and n+1 constraints excluding nonnegativity. Its coefficients are
integers with absolute value at most L, and it can be solved in
polynomial time. To see the support bound, rewrite its depth inequalities
as

    sum_t mu_t d_{T_t}(h) + s_h - r = 0,    s_h>=0,

with the normalization equality. Since n>=2 implies every tree depth is
at least one, r>=1 and the variable r is positive. A basic solution has
at most n+1 positive variables in this standard-form LP. Thus at most n
of them can be tree probabilities. This conclusion also holds if some
constraints are dependent, since dependence can only reduce the basis
size. Cramer's rule and Hadamard's determinant bound give polynomial bit
length for the resulting rational probabilities.

For exact sampling, choose a common denominator D, draw a uniform integer
in {0,...,D-1} by fair bits with rejection, and use the cumulative
probability intervals. The expected number of attempts is less than two.
The expected number of random bits is polynomial. Every output tree is
correct, and every actual query run uses at most n-1 supplied line tests.

An additional useful certificate is available without any new oracle:
the restricted LP value is an upper bound on R*, while

    max_t c_{pi_t}(T_t)/alpha <= R*

is a valid lower bound. An implementation can report their ratio or stop
early when that ratio meets its target. The fixed K analysis does not
rely on early termination or on this certificate being tight.

## Calibration using the current best expected-depth results

The current rigorous certificate is

    rho < 5.182975508794 < 5.18297551.

Thus the rational oracle coefficient alpha=518297551/100000000 is valid.
With epsilon=1/4000000, the new randomized coefficient is strictly below

    alpha+epsilon = 5.18297576 < 5.182976.

This is a polynomial-time result with the same public approximation
threshold as the current expected-depth theorem. This tiny tolerance
makes the constant in the iteration bound very large. It is a theorem
about polynomial time, not a practical runtime claim. The parameterized
transfer theorem and optimized master LP are more useful computationally.

For a target rational 0<epsilon<=1, call the quasipolynomial expected
oracle at coefficient alpha=2+epsilon/2 and use the transfer with tolerance
epsilon/2. The resulting coefficient is strictly below 2+epsilon, with

    K = ceil(32 alpha (n-1)/epsilon^2).

The expected-oracle calls have running time
(mn)^{O(epsilon^{-1} log n)} times a polynomial in input bit length.
The polynomial number of calls, their polynomial-size rational priors,
and the master LP preserve that asymptotic running-time form.

## Exact independent checks

Run `python randomized-programming-report.py`. It enumerates every proper
depth vector for three strict planar supplied-line instances, then solves
both the complete-tree dual LP and the primal mixture LP by independent
Fraction-based vertex enumeration. Results:

| Instance | Proper depth vectors | Deterministic height | Exact R* |
|---|---:|---:|---:|
| 3 singleton cap lines | 3 | 2 | 5/3 |
| 4 singleton cap lines | 12 | 3 | 9/4 |
| 4 singleton cap lines and 3 vertical cuts | 13 | 2 | 2 |

The last instance has an optimum dual vertex (0,1/3,1/3,1/3), explicitly
testing zero support in the dual while all iterative priors remain positive.

For each instance the script runs exact best responses and adversarial
alpha=3/2 approximate responses with epsilon=1/2. It checks positive
integer updates, rational oracle guarantees against R*, exact coefficient
inequalities, actual mixture bounds, and optimized support of at most n.
As a diagnostic, 80-digit Decimal logarithms also check the proved
potential inequality on each run. Those numerical checks are not used
to establish the theorem's constants.

For the singleton instances, the optimized master LP recovers 5/3 and
9/4 from exact-oracle runs; it improves the respective uniform empirical
mixture values 107/64 and 217/96. An adversarial approximate-oracle run on
the four-point example gives LP value 13/5, still within the transfer
guarantee. The public headline margin is checked with exact Fractions.

## Primary sources and novelty limits

The generic connection between multiplicative weights, approximate
zero-sum game strategies, and linear programming is standard; see
[Arora, Hazan, and Kale, *The Multiplicative Weights Update Method: A Meta-Algorithm and Applications*, Theory of Computing 8 (2012)](https://theoryofcomputing.org/articles/v008a006/v008a006.pdf), especially
Sections 2 and 3.2, and
[Freund and Schapire, *Adaptive Game Playing Using Multiplicative Weights*, Games and Economic Behavior 29 (1999)](https://cseweb.ucsd.edu/~yfreund/papers/games_long.pdf).

The research contribution here is the supplied-line application with the
correct randomized comparator, a concrete strict planar separation of
models, the entropy-scaled O(n/epsilon^2) call bound, and an exact rational
implementation including an explicit optimal mixture LP of support at
most n. The general MWU transfer method should not be presented as a new
optimization theorem. These results do not improve the existing
deterministic worst-depth factor, ordinary expected-depth factor, or
establish a constant inapproximability result.

## A separate check on further endpoint-mode improvements

The stronger larger-exclusive-first query-both mode in the current best
algorithm improves actual asymmetric blocks. It does not improve a
universal saving lower bound depending only on total newly hit mass.
Write m=x+y+z with x<=y. For fixed z and m, the saving is

    D(x,y,z) = max{y, m-2z+E_*(y,z)}.

The rational tent E_*(y,z) is nondecreasing in y. Both expressions are
therefore nondecreasing in y, and the feasible range is
(m-z)/2 <= y <= m-z. The minimum occurs at x=y=(m-z)/2. Hence the
symmetric mass configuration remains the worst case for a mass-only
affine certificate. A further factor improvement from this mode would
need additional structural control of asymmetry, rather than an
orientation-only improvement of the existing certificate.
