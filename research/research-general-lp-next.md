# Query-synchronized LPs, completion pricing, and a new consistency gap

Auxiliary research note, 18 October 2026. No article files are changed.

**Status.** No unrestricted approximation improvement is proved. Two concrete conclusions are established. First, the team's executable-partial-policy completion-cover LP is exactly OPT; approximate weighted pricing would yield an approximation without a fractional set-cover rounding loss. Second, the previously proposed **query-synchronized local-policy hierarchy** has a full-order gap at every fixed hypothesis width, even after adding natural positive-semidefinite query/co-location constraints, Kraft, and every static conditional-entropy demand. This is a different and stronger statement than the fixed-width independent-cost-cone limitation in research-general-credit.md.

## 1. Exact completion-cover LP and the useful positive target

Write F(T)=sum_h d_T(h), with F*=min_T F(T). A partial policy P is an executable tree using original supplied tests. It identifies a set C(P) of hypotheses at singleton output leaves and may leave other hypotheses unfinished. Its raw work W(P) is the sum of its path lengths over all hypotheses, including unfinished ones.

For every nontrivial partial policy P introduce a column x_P. Consider

    min sum_P W(P)x_P,
    sum_{P:h in C(P)} x_P >= 1       for every h,
    x_P >= 0.                                                       (1)

Its dual is

    max sum_h y_h,
    sum_{h in C(P)} y_h <= W(P)      for every P,
    y_h >= 0.                                                       (2)

**Proposition 1 (team completion-pricing bridge, independently audited here).** The value of (1) is exactly F*. Moreover, a polynomial alpha-approximation to the weighted maximum-density pricing problem

    max_P [sum_{h in C(P)} w_h] / W(P)                               (3)

would imply a polynomial alpha-approximation for UDT, when it applies to arbitrary nonnegative input weights and returns an explicit partial policy.

For exactness, let T* be an optimal complete tree. Execute any P and append T* restricted to each unfinished output cell. Restriction never increases a surviving hypothesis's depth, so the resulting tree costs at most

    W(P) + sum_{h not in C(P)} d_{T*}(h).

Optimality of T* consequently gives

    sum_{h in C(P)} d_{T*}(h) <= W(P).

Thus y_h=d_{T*}(h) is dual-feasible, with value F*. Conversely the single full-tree column T* is primal-feasible with cost F*.

For the algorithmic claim, start with any proper complete tree T. Use weights w_h=d_T(h), and ask the approximate pricer for P. If its returned weighted reward exceeds W(P), execute P and then append the restrictions of T at unfinished leaves. This strictly decreases F(T). If F(T)>alpha F*, the full T* column has density F(T)/F*>alpha, so the alpha-approximate pricer must return density greater than one, and an improvement exists. Therefore termination certifies F(T)<=alpha F*. The raw cost is an integer at most n(n-1), so at most n(n-1) strict decreases occur. Prune constant queries after every update.

This is an exact LP and a valid reduction. It does not make (3) polynomially solvable. A pricer only for a polynomial library certifies optimality against that library's columns, rather than against unrestricted UDT. A polynomial number of variables in a proposed pricing relaxation is also insufficient unless its actual constraints and rounding are supplied.

There is an additional useful exact consequence. Suppose the test instance admits a transitive group of hypothesis permutations that preserves supplied tests and costs. Apply those permutations to the optimal-depth dual and average. Dual feasibility is preserved, and the averaged weight at every hypothesis is D*=F*/n. Therefore every partial policy satisfies

    W(P) >= D* |C(P)|,
    min_{P:C(P) nonempty} W(P)/|C(P)| = D*.                       (17)

The full optimal tree attains equality. Thus on transitive instances even the **uniform-prize** completion-density oracle computes the optimal mean cost in value; arbitrary weights are not needed for that value equivalence. This is an exact structural observation, not a polynomial algorithm.

## 2. A precise polynomial SDP strengthening of time-indexed co-location

Let E_tau be the n by n zero-one matrix

    E_tau(h,g) = 1[tau(h)=tau(g)],

and let J be the all-ones matrix. At query time t use a symmetric arrival matrix Y_t, a nonnegative stopping vector e_t, a query co-location matrix

    Z_t = Y_t - Diag(e_t),

and a query matrix A_{tau,t} for every test. Impose

    Y_0=J,
    A_{tau,t} positive semidefinite and entrywise nonnegative,
    sum_tau A_{tau,t}=Z_t,
    Y_{t+1}=sum_tau A_{tau,t} Hadamard E_tau.                        (4)

Only diagonal mass can stop. The objective is sum_t trace(Z_t). At a terminal time all remaining arrival mass must stop, so its matrix is diagonal. A horizon T=n-1 is sufficient for every proper identifying tree.

Every randomized classical tree gives a feasible point: each currently queried state S contributes its policy probability times 1_S 1_S^T to the matrix for its chosen test. Querying tau refines this into its outcome cells, exactly the Schur/Hadamard update in (4). Stopping at a singleton removes a diagonal contribution.

The diagonals x_{h,tau,t} and off-diagonals a_{hg,tau,t} project to the existing pair-synchronization LP. Add its co-location triangles if desired. Also add the existing local policy flows for every U of size at most q, synchronizing **the full query marginals x and pair history/co-location marginals a,z**, not merely costs or depths. For fixed q, all of these variables and constraints have fixed-exponent polynomial size.

Finally one may impose global Kraft on completion times, and the static conditional-entropy demands from uniform-decision-tree-lower-bounds.md, Section 4, on aggregate query masses

    mu_{h,tau}=sum_t x_{h,tau,t}.                                  (5)

The gap below survives all these additions. The entropy family may even contain every subset, despite its exponential explicit size; the failure is therefore not caused by omitting those entropy demands.

This Gram-matrix viewpoint resembles the query-SDP viewpoint in Barnum, Saks, and Szegedy, [Quantum Decision Trees and Semidefinite Programming](https://www.osti.gov/servlets/purl/975874/). We do not identify (4) with a quantum-query SDP or infer a quantum algorithm from it. In particular, (4) uses equality masks and nonnegative entries. The witness below is an elementary classical-moment ambiguity.

## 3. Affine-equality instance and parameters

Use exactly the family already proved in the existing lower-bounds note:

    H = F_Q^d,   n=Q^d,   d=floor(Q/ln Q),
    tau_{a,b}(h)=1[a dot h=b],   (a,b) in F_Q^d times F_Q,
    M=nQ listed tests.                                            (6)

Take Q>=128 a prime power. Constants and duplicate test descriptions can remain. Every hypothesis is positive on M/Q tests. For distinct h,g, their two test answers under a uniformly chosen listed test are independent Bernoulli(1/Q). Hence

    sigma = Pr[tau(h) != tau(g)] = 2(Q-1)/Q^2,
    c = 1-sigma,
    (1/M) sum_tau E_tau = cJ + sigma I.                            (7)

The true optimum is F*=Theta(nQd). A coordinate-by-coordinate equality search is a legal backup code of height L<=d(Q-1) and raw cost at most nL.

For q>=2 define

    z_t=c^t,
    r_t=min(1,(q-1)c^t),
    s_t=1-r_t.                                                    (8)

Let t_q be the first integer with (q-1)c^{t_q}<=1. Then

    t_q = O(Q(1+ln q)),
    sum_{t>=t_q} r_t <= 1/sigma.                                 (9)

## 4. Local policies with globally identical query marginals

**Lemma 2.** For every U subset H of size at most q, there is a valid randomized local policy, with delayed singleton stopping allowed, such that before any stopping:

* each pair h,g in U is still co-located at time t with mass z_t;
* the same mass s_t of each hypothesis h is reserved in its local singleton state;
* reserved singleton mass may query any prescribed distribution nu_{h,tau};
* every other local state queries a uniformly chosen listed test.

Consequently the global marginals, identical for every U containing the relevant indices, are

    x_{h,tau,t} = r_t/M + s_t nu_{h,tau},
    a_{hg,tau,t} = z_t/M,
    pair-arrival mass = z_t.                                     (10)

To prove this, an unseparated pair cannot occupy a reserved singleton. Its common next test is uniform, so its co-location mass obeys z_{t+1}=cz_t, starting at one. For a fixed h in U, a union bound gives

    Pr[h has a local competitor at time t]
       <= sum_{g in U minus {h}} Pr[h,g still co-located]
       <= (q-1)c^t.

Thus its local singleton arrival mass is at least s_t. Since s_t increases, reserve enough of that singleton mass to bring the reserved total to exactly s_t. Existing reserved singleton paths remain singleton under every future query, so no reservation has to be revoked. Reservations for different h occupy different local singleton states and cause no conflict. A reserved path knows h locally, so the h-dependent query choice nu is a legal local action. This yields (10) and all local flow constraints, including common x,a,z across every U.

The important qualification is local knowledge. A singleton in every separately constructed q-hypothesis policy need not correspond to one common globally identifying history. The relaxation has not coupled those histories; it couples only their shared x,a,z marginals.

## 5. Filling every static entropy demand before stopping

The old all-subset static certificate obstruction supplies explicit aggregate query masses

    mu*_{h,tau} = 64 Q^2/M     if tau(h)=1,
                 64 Q/M       if tau(h)=0,                        (11)

which satisfy every static conditional-subset entropy demand. Their per-hypothesis total is

    B = sum_tau mu*_{h,tau} = 64(2Q-1).

Set nu_{h,tau}=mu*_{h,tau}/B. Hold every local hypothesis alive through

    D = t_q + B + ceil(1/sigma) + ceil(log_2 n).                  (12)

By (9), sum_{t=0}^{D-1}s_t >= D-t_q-1/sigma >= B. The aggregate reserved query mass in (10) therefore dominates mu* coordinatewise. Static entropy demand left sides are monotone in each nonnegative query mass, so all those demands hold. This step uses the explicit, already proved all-subset certificate; it is not a new assumption that local query entropy telescopes.

No hypothesis has stopped yet. Since D>=ceil(log_2 n), any completion distribution supported on times at least D obeys the global binary Kraft inequality.

## 6. Stopping the local singleton reserves and finishing the residue

At time D stop the reserved singleton mass s_D, leaving per-hypothesis alive mass r_D. For each subsequent time t continue uniform tests on every remaining local state, and stop enough singleton mass to make its per-hypothesis alive mass exactly r_t=(q-1)c^t.

This is feasible. At arrival time t, the surviving mass of h is r_{t-1}. Its mass sharing a state with any local competitor is at most (q-1)z_t=r_t, by the same union bound. Thus at least r_{t-1}-r_t is available in singleton states to stop. The pair mass is still z_t and its common-query mass remains z_t/M. These quantities, and x_{h,tau,t}=r_t/M, are independent of U.

Choose a final switching time t_0>=D with r_{t_0}<=1/n. At that point run the same actual coordinate-search backup tree on all remaining mass, ignoring previously cached answers and delaying local singleton stopping until the corresponding global backup leaf. Its local restrictions are executable and have common global x,a,z: each h has remaining mass r_{t_0}, and each still-together pair has remaining mass z_{t_0}. Thus the backup completes every local policy and the global matrix relaxation exactly in finite time.

For sufficiently large Q, t_0+L<n-1: t_0=O(Q(ln n+ln q)+D), L=O(Qd), whereas n=Q^d. Therefore the witness fits the original natural horizon T=n-1. All numbers in the witness can be chosen rational, with polynomial bit length; powers c^t have O(T log Q) bits.

Its total objective is at most

    nD + n sum_{t>=D} r_t + r_{t_0} nL
      <= nD + n/sigma + L
      = O(nQ(1+ln q)).                                           (13)

## 7. Positive-semidefinite query matrices do not remove the witness

Before D define

    A_{tau,t}
      = (z_t/M)J
        + Diag_h[(r_t-z_t)/M + s_t nu_{h,tau}].                  (14)

Since q>=2 gives r_t>=z_t, every diagonal term is nonnegative. Each query matrix is consequently PSD and entrywise nonnegative. Their sum has diagonal one and off-diagonal z_t. Equation (7) gives exactly the next arrival matrix with off-diagonal z_{t+1} and diagonal one. Thus (4) holds with no stopping in this phase.

After D use

    A_{tau,t}=(z_t/M)J + ((r_t-z_t)/M)I.                         (15)

Their next arrival matrix has diagonal r_t and off-diagonal z_{t+1}. Removing singleton diagonal mass r_t-r_{t+1} leaves the next query matrix sum, exactly as required. Co-location triangles and their action-conditioned counterparts hold as well, since every diagonal x is at least z_t/M. More fundamentally, the explicitly constructed local flows already satisfy every such inequality visible on at most q hypotheses.

For the backup, use z_{t_0} times the actual backup-tree query matrices, plus diagonal mass (r_{t_0}-z_{t_0}) following each hypothesis's backup path. This is again a PSD, nonnegative construction with the required marginals.

**Theorem 3 (new query-history hierarchy gap).** For every fixed q>=2, the query-synchronized local-policy hierarchy on all U of size at most q, strengthened by (4), global Kraft, and every static conditional-subset entropy demand, has gap

    Omega(d)=Omega(log n/log log n).                            (16)

More generally, the displayed witness gives gap Omega(d/(1+ln q)) whenever the construction fits the natural horizon. The proof is the ratio of F*=Theta(nQd) to (13). This rules out the desired improved ratio **relative to this specific relaxation**. It is not computational hardness for UDT and does not apply to a richer compact global-history formulation.

Here synchronization means common time-indexed query marginals x and pair co-location/query marginals z,a, even though each small restriction has a genuine local policy. It does not synchronize full labeled query/answer transcripts. The theorem also excludes additional sequential-rank or positive-answer-count constraints. On the affine family every proper original-test path has at most d positive answers: each nonconstant positive equality adds an independent affine equation. The witness's reserved query mass alone has at least 64Q positive queries per hypothesis, so it violates that global d-positive-answer budget for the asymptotic parameters. A compact algebraic certificate of such a budget is therefore a genuinely stronger history constraint and is not ruled out by this theorem.

The synchronization in this theorem is exactly the x,a,z time marginals in (10), not joint distributions of complete labeled transcripts. The theorem also excludes global rank or positive-answer budgets. On the affine family, every proper path has at most d positive hyperplane answers. Its reserved masses in (11) instead have positive total at least 64Q per hypothesis, so that inexpensive affine-specific constraint eliminates this witness. The compact matroid-flat certificates developed in research-general-information-next.md provide a way to certify such a budget without enumerating every span state. No gap is claimed after adding all such certificates.

This also explains why a generic Euclidean/SDP clustering rounding guarantee cannot be imported without further constraints. The matrices are already PSD, entrywise nonnegative, and locally executable at every fixed width. A rounding theorem with loss o(log n/log log n) relative to their objective would contradict (16), even if it only queried allowed tests.

The affine-equality instance is hypothesis-transitive: translations of F_Q^d permute its hypotheses and its supplied tests. By (17), every true partial policy has uniform-prize work per identified hypothesis at least D*=Theta(Qd). The local LP/SDP witness completes all mass with work per hypothesis O(Q) for fixed q. Hence the same construction is also an Omega(d) **completion-pricing integrality gap with uniform prizes**, directly addressing the oracle in Section 1. Merely applying this hierarchy to pricing rather than to complete identification does not repair it.

## 8. What remains promising

The exact completion-pricing LP of Section 1 keeps actual executable partial policies as columns, so it cannot make the local-history substitution responsible for this witness. Its missing ingredient is approximate weighted pricing over complete legal histories. A polynomial family of state-independent costs, pair moments, or fixed-width locally executable policies is not sufficient for that task, as the new construction shows.

A useful future oracle could still exploit a compact library of complete conditional templates, provided its approximation compares against **all** executable partial policies. A density guarantee only against its present library, or a strong LP root value without a feasible policy, does not supply that comparison. The exact template-pruning/pricing dynamic programs being developed in the other auxiliary notes are valid restricted oracles and remain a constructive starting point.

The stochastic-cover and latency literature supports the importance of a suffix-completion or density ledger, but its approximation bounds do not bypass this legal-history obligation. For example, Im, Nagarajan, and van der Zwaan, [Minimum Latency Submodular Cover](https://arxiv.org/abs/1110.2207), study paths and adaptive submodular ranking. Their reported logarithmic losses are context, not a constant-factor UDT theorem used here.

## 9. Verification and scope

The companion research-general-lp-next.py explicitly constructs the affine test tables in small prime fields, audits the pair coincidence counts and PSD matrix identities, and simulates every local policy of width at most three on the nine-hypothesis instance. It checks that all those independently constructed policies have the same global x,a,z marginals, including the h-dependent reserved queries and the subsequent stopping phase. It also verifies static entropy demands on every nontrivial subset of that small instance and checks the asymptotic horizon/parameter inequalities on large symbolic instances.

Small finite-field instances are algebra audits; the large-Q asymptotic proof supplies (16). No exponential enumeration in this checker is offered as a polynomial approximation algorithm.
