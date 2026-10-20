# Further polynomial expected-depth improvement

Prepared 13 October 2026. This report supplements `poly-expected.md` and `poly-expected-next.md`. It uses the unrestricted binary, unit-cost, supplied-line planar identification model and arbitrary strictly positive rational priors. No shared TeX file was edited.

**A new polynomial-time algorithm has expected-depth approximation factor strictly below 5.272565.** Its new ingredient is to ask the other endpoint of a hull-edge block even after a positive first answer when the resulting information makes that worthwhile. A rational lower bound on the binary entropy gained by that extra question permits all algorithmic choices to use rational arithmetic.

The optimum-witness and polynomial geometric-batch machinery from the previous reports is unchanged. The additional information is accounted for with a coarsened discovery transcript, so the original delta cap on positive discovery exits remains available.

## 1. Two block modes and their physical query costs

For each block on the all-negative route, partition its newly hit pattern mass into endpoint-exclusive masses x,y and shared mass z. Relabel the endpoints so x<=y, and put m=x+y+z. Both endpoint caps have mass at most delta w, where w=w(S).

In stop mode, query the endpoint with exclusive mass x first and stop at its first positive answer. Relative to the nonentropy allowance (2k+3)m for block rank k, the y mass exits on the second answer with a pinned endpoint and saves one query. The physical saving is y.

In query-both mode, query that same first endpoint and then ask the other endpoint even when the first was positive. The exclusive masses x,y have one negative adjacent endpoint and need at most one alphabetic endpoint code. They cost at most 2k+2 queries before conditional entropy. Shared mass z has two positive endpoints and costs at most 2k+4. Thus the physical saving relative to (2k+3)m is

    x+y-z.

The origin remains a free negative endpoint. Cached negative endpoints cause exclusive/shared masses to disappear and only decrease costs. For a clean entropy identity, the analyzed procedure completes its chosen block mode before inferring a singleton; avoid stopping between a positive first query and its planned second query. Subsequent deletion of constant queries is safe.

## 2. Retain the information learned by the optional second query

Let J_act be the information in the actual discovery transcript. Define a coarsened discovery transcript Z* by forgetting the second answer on a query-both route whose first endpoint was positive. That route's exclusive x and shared z subevents merge into one x+z event. Its y event remains separate. In stop mode no coarsening is necessary.

Every nonzero Z* event is contained in a positive first-endpoint cap, or in the positive second-endpoint cap following a negative first answer. All such event masses are at most delta w. The zero event is the same zero-pattern singleton as before. The capped entropy lemma therefore yields

    J* >= b sigma(delta).

Coarsening a query-both event loses exactly

    (x+z) H_nats(x/(x+z))

information. Summing over the disjoint query-both events gives J_act-J*. The actual endpoint code contribution is bounded by (I-J_act)/ln2. Consequently each query-both block may credit an additional

    (x+z) H_2(x/(x+z))

queries while retaining the common remaining-entropy term (I-J*)/ln2. This is an entropy-chain identity; the extra entropy credit is not added to a bound already using J_act.

## 3. Use a rational entropy tent

Choose the rational constants

    p*=21317/125000 = .170536,
    h*=1-2p*=41183/62500 = .658928.

The exact logarithm certificate verifies H_2(p*)>h*. Concavity and symmetry of binary entropy imply the rational lower bound

    L(p)=min{(h*/p*)p, h*, (h*/p*)(1-p)} <= H_2(p).

In homogeneous mass form, the credited entropy is at least

    E_L(x,z)=min{(h*/p*)x, h*(x+z), (h*/p*)z}.

Define the rational block saving

    D(x,y,z)=max{y, x+y-z+E_L(x,z)}.

Use stop mode if the first term is larger, and query-both mode otherwise. All mode comparisons are comparisons of rational linear forms in supplied prior weights.

An optional instance improvement is to orient a query-both block with the larger exclusive mass first and use E_L(y,z), which is no smaller. Its own coarsened transcript still has delta-capped cells. The certified theorem below uses the simpler common orientation x<=y.

For any block schedule G with these mode choices, the full stage satisfies

    W_stage(G) <= 2 MSSC_blocks(G) +3b +2p0 |G|
                   -sum_blocks D +(I-J*)/ln2.

Choose the deterministic geometric shift by minimizing the exact rational surrogate

    2 MSSC_blocks(G) +2p0 |G| -sum_blocks D.

The existing exact maximum-weight coverage sets and greedy internal block order are unchanged. The best surrogate is at most its log-uniform average. All shifts' coarsened transcripts obey the same entropy cap.

## 4. Stronger affine block credit

Put

    c=228683/103683 = 1+1/(1-p*),
    d=250000/103683 = 2/(1-p*).

For every block,

    D >= 0,
    D >= m-delta w,
    D >= c m-d delta w.

The second inequality follows from y>=m-delta w. Here is a proof of the third.

If m<=delta w, the affine right side is negative. For m between delta w and 2delta w, scale delta w to one and write u=m/(delta w). Feasible pairs x<=y satisfy x,y>=m-delta w and x+y<=m. Their triangle has vertices

    (m-delta w,m-delta w), (m-delta w,delta w), (m/2,m/2).

The query-both credited saving x+y-z+E_L(x,z) is concave on this triangle, because E_L is a minimum of three affine forms. Its minimum is at least the smallest vertex value. The two vertices with z=0 give saving m. The first vertex gives delta w times

    F(u)=3u-4+L(u-1).

Thus D>=max{m-delta w,min{m,delta w F(u)}}. If u<=1+p*, the desired line c u-d is no larger than u-1. If u>=1+p*, F is concave, F(1+p*)=p* and F(2)=2. Its chord between those endpoints is exactly c u-d. Also u>=c u-d for u<=2. Both entries in that minimum therefore dominate the line. This proves the claim globally.

## 5. Transfer affine credits through exact budgeted coverage

Let m_t be the analytical optimal-witness supporting-prefix masses, M_k=sum_{t<=k}m_t. As before m_t<=2delta w, and an optimal comparison edge sequence hits at least M_k with its first k blocks.

A schedule prefix through a batch of budget k has covered mass H>=M_k, by exact budgeted coverage. If it uses at most ell blocks, summing the affine block inequalities gives each of the valid total-saving bounds

    sum_blocks D >= M_k-delta w ell,
    sum_blocks D >= c M_k-d delta w ell,
    sum_blocks D >= 0.

Total savings over the complete schedule dominate any prefix's savings because D>=0. If the schedule has already finished, use the full schedule as that prefix; all-positive coverage and the same budget-length upper bounds still prove the inequalities.

For the first phase k=floor(u), ell<=floor(u). For the first two phases k=floor(beta u), ell<=floor(u)+floor(beta u). Therefore any convex combination, including a zero choice, of these prefix bounds is valid for the same sum D. It is charged once.

## 6. A fixed certified analysis mixture

Keep beta=3512863/10^6. Define fixed rational mixing weights

    eta=.0830027,
    zeta=.472577,
    theta=.3402602.

For brevity let A(k,ell)=M_k-delta w ell and C(k,ell)=c M_k-d delta w ell. The following analysis choices are lower bounds on total block saving for each shift range:

| Shift range | Convex combination used in the analysis |
|---|---|
| [1,4/beta) | C(1,1) |
| [4/beta,5/beta) | eta C(1,1)+(1-eta) A(4,5) |
| [5/beta,6/beta) | A(5,6) |
| [6/beta,2) | C(1,1) |
| [2,10/beta) | A(2,2) |
| [10/beta,3) | zeta A(2,2)+(1-zeta) 0 |
| [3,11/beta) | theta A(3,3)+(1-theta) C(3,3) |
| [11/beta,12/beta) | C(3,3) |
| [12/beta,beta) | A(3,3) |

These fixed breakpoints are rational and occur in the displayed order. The table changes only the analysis, not the polynomial scheduling algorithm.

A row (l,r) has log-uniform probability ln(r/l)/ln beta. If its chosen minorant has source coefficient alpha M_k and intercept rho delta w, add alpha times that probability to every effective source coefficient a_t with t<=k, and add rho times that probability to mu. Start with

    e(t)=2[lambda_beta t+eta_beta-Phi_beta(t)],
    a_t=e(t), mu=0.

For a convex row apply those updates to each choice times its rational mixing weight. This completely specifies a_t and mu without any optimization oracle in the theorem.

The exact certificate gives

    a1≈1.382412135842154,
    a2≈1.382412116541417,
    a3≈1.382412114823743,
    a4≈1.376123320347661,
    a5≈1.382412122892163,
    a_t=e(t)>=e(6)≈1.383820291407644, t>=6,
    mu≈3.639248217489951.

Use T=345603/250000=1.382412. Only a4 is below T. Hence

    sum_t m_t e(t)+E[sum_blocks D]
      >= sum_t m_t a_t-delta w mu
      >= T b-2delta w(T-a4)-delta w mu.

Define

    chi=T-2delta(T-a4)-delta mu.

With the retained zero waiting-time credit, the total saving is at least chi b whenever chi+2/ln beta>=T. This follows by adding 2p0/ln beta and using w=b+p0, exactly as in the earlier threshold proof.

## 7. Certified global ratio and polynomial runtime

Take delta=144136826/10^9. The exact certificate verifies lambda_beta>nu_beta, all threshold comparisons, chi+2/ln beta>T and

    chi≈.856049452255203,
    B=7-ln6/ln beta-chi≈4.717880246118900,
    A=(beta+1)/ln beta≈3.591810178840039.

The source-prefix and geometric-batch bounds therefore give the flat-stage inequality

    W_stage <= A Delta+B b+(I-J*)/ln2.

Since J*>=b sigma(delta), use the same balanced-stage argument and telescoping recursion with

    q=max{1/h(delta), B/sigma(delta)}.

The certificate establishes

    max{ln2/h(delta),B ln2/sigma(delta)} <1.680753968383097,
    A+max{ln2/h(delta),B ln2/sigma(delta)} <5272565/10^6.

Thus the expected-depth approximation factor is strictly below **5.272565**.

The algorithm is polynomial for the same reasons as the earlier geometric-batch algorithm: polynomially many exact cardinality-budget interval cover DPs, polynomially many rational shift regions, polynomially many recursively proper states, and rational objective arithmetic. The tent has fixed rational coefficients. Neither the optimization of the analysis table nor any entropy/logarithm calculation occurs in the decision-tree algorithm. The runtime exponent has no dependence on the smallest prior weight.

## 8. Checks and remaining barriers

`python further-expected-check.py` passed the exact rational theorem certificate, 5,000 exact rational block-credit checks, and 10,000 analytical profile checks. The script keeps the floating-point feasible-start LP optimizer behind `--explore` and its beta grid behind `--beta-grid`. Its default theorem certificate does not rely on either optimizer.

The coefficient table was found by a small LP over analysis mixtures; the resulting rational table is certified directly. Coordinate ascent alone stalled around 5.28025, so that weaker numerical result should not be mistaken for the best bound proved here.

An orientation-only prefix-analysis barrier explains the limited gain available before the entropy mode: at the previous beta/delta, the abstract source profile (2delta,delta,2delta,delta,1-6delta) makes the active first/second-prefix inequalities tight, while every third-or-later prefix bound is nonpositive since its budget sum is at least 1+3+12. This is a limitation of that aggregate analysis, not a realizable-instance lower bound for the decision-tree problem.

The next substantial improvement would require a stronger polynomial scheduling lemma, or direct coupling of individual greedy phase masses and their information credits. Adding two overlapping prefix credits is invalid. Phase credits may be added only after proving that they refer to disjoint newly covered mass. General source-profile LP certificates can search that stronger accounting, but the current theorem does not assume it.
