# Completion pricing and exact pruning of supplied codes

Research continuation, 18 October 2026. Uniform hypotheses, unit costs, fixed response bound, and fixed-exponent polynomial runtime remain the target. No unrestricted asymptotic approximation improvement has been proved. The results here give a concrete pricing subproblem, exact polynomial subroutines for explicit codes, and an obstruction to using uniform depth caps as their substitute. The article is unchanged.

## An exact covering LP over executable partial policies

An executable partial policy P uses original tests, identifies a set C(P) of hypotheses, and may stop unfinished on its other leaves. Let W(P) be its raw work: sum its query counts over all n hypotheses. Policies suppress determined tests and stop on singleton states. They have finite proper trees with at most n leaves, so the family of distinct policies is finite, although exponential.

Consider the covering LP and its dual:

    minimize sum_P W(P) x_P
    subject to sum_{P:h in C(P)} x_P >= 1 for each h; x_P >= 0,

    maximize sum_h y_h
    subject to sum_{h in C(P)} y_h <= W(P) for each P; y_h >= 0.

**Theorem 1.** Both values equal the optimal raw decision-tree cost F(H).

Let T* be a full optimal tree. It supplies one primal column covering everything, of cost F(H). Set y_h=d_T*(h). To check any dual constraint, execute P and append T* restricted to every unfinished output state. Its fallback cost is at most sum_{h not in C(P)} d_T*(h). Optimality of T* gives

    F(H) <= W(P) + sum_{h not in C(P)} d_T*(h),

which is exactly dual feasibility after cancellation. The dual objective is F(H), proving equality.

This is a covering formulation with no integrality gap at the full ground set. The columns retain the complete adaptive computation that ordinary certificate sets discard. It is not a polynomial LP: approximate column pricing is the central algorithmic task.

The LP and the following improvement reduction were derived jointly with the continuation and LP agents, who independently checked the cancellation argument. They are written out here to separate the precise oracle target from the code-library experiments.

## Weighted pricing gives the same approximation factor

For positive integer prizes w_h, the pricing problem minimizes

    W(P) / sum_{h in C(P)} w_h

over nonempty executable partial policies. Its reciprocal is weighted reward per unit work.

**Theorem 2.** A polynomial alpha-approximation for this pricing problem, for prizes w_h<=n-1, gives a polynomial alpha-approximation for uniform decision trees.

Start with any full proper incumbent T. Set w_h=d_T(h), call the pricing algorithm, execute its policy P, and append T restricted to each unfinished state. Compute the actual cost and accept every strict improvement. If the returned density is below one then

    W(P) < sum_{h in C(P)} d_T(h),

so the appended tree is strictly cheaper. If F(T)>alpha F(H), the full optimal tree is itself a pricing candidate of density F(H)/F(T)<1/alpha. The oracle must return density below one and therefore must improve T. At termination F(T)<=alpha F(H).

Every accepted move decreases the integer cost by at least one, and a proper identifying tree has raw cost at most n(n-1). Thus at most n(n-1) successful moves are possible. Construction and comparison of each output tree are polynomial. No horizon grows in an exponent.

At a nonimproving oracle call, its returned density at least one implies that the true minimum density is at least 1/alpha. Therefore y_h=d_T(h)/alpha is feasible for the full dual above. This is an algorithm-linked lower certificate, not a separate scalar lower bound recharged at each recursive level.

An exact or constant oracle has not been obtained. Defining an oracle over all policies does not make it computationally available.

## Cardinality density has a separate constant-factor transfer

There is a second useful reduction that needs no incumbent depth prizes. At the current unfinished frontier, let R be its r hypotheses. Suppose an alpha-approximate oracle minimizes actual raw work per newly identified hypothesis over executable partial forests on that frontier. Repeatedly execute its returned forest and mark all singleton outputs finished.

**Theorem 3.** The final raw cost is at most 4 alpha F(H).

Let a chosen stage have work W, complete k hypotheses, and price p=W/k. Compare to a full optimal tree truncated at original depth t on every unfinished state, suppressing constant queries. This forest has work at most rt and completes at least

    k*(t) = |{h in R : d_T*(h)<=t}|.

Hence p<=alpha rt/k*(t) whenever k*(t)>0. Set t=p/(2alpha). If more than r/2 remaining hypotheses had optimal depth at most t, this inequality would contradict the definition of p. Thus at least r/2 of the remaining hypotheses have optimal depth greater than p/(2alpha).

Charge p to each newly identified hypothesis; total charged price equals actual work. Sort the comparison depths in decreasing order. In the greedy completion order, the hypothesis with j positions remaining is charged at most 2alpha times comparison depth number ceil(j/2): at its stage at least half that stage's remaining population has larger comparison depth. Each comparison depth appears at most twice. Summing gives the factor 4alpha. The comparison needs no monotonicity of successive greedy prices.

This theorem also explains precisely what a code library must supply: it must compete with adaptive truncated optimal policies, not merely with each hypothesis's cheapest separate certificate.

## Exact pricing inside one explicit template

Fix a full supplied-test tree B on the current state. A template prefix can stop independently at different internal nodes. It identifies exactly the template leaves it reaches. All queries, transcript states, and node work are explicit.

Let C_v(k) be the least raw work in the subtree at v that finishes k leaves. At a singleton leaf, C_v(1)=0. At a nonsingleton node, stopping gives C_v(0)=0; continuing gives

    C_v(k) = |S_v| + min_{sum_i k_i=k} sum_i C_child_i(k_i).

Retain the better stop/continue value. For binary trees the convolutions require O(n^2) arithmetic operations over the whole tree: sum_v |left_v||right_v|=binomial(n,2), and the remaining size terms are also O(n^2). Fixed arity changes only a fixed polynomial factor. Minimizing C_root(k)/k gives exact cardinality density among all template prefixes.

For arbitrary prizes, use a Lagrange multiplier lambda and define the maximum profit

    G_leaf(lambda)=lambda w_h,
    G_v(lambda)=max{0, sum_i G_child_i(lambda)-|S_v|}.

This is a linear-time exact maximum-closure calculation for the template. Equivalently, choose a rooted prefix of test nodes with costs |S_v| and collect a leaf's prize only when all its ancestor tests are chosen. The precedence graph is a tree, so the binary-selection LP has an integral order-polytope description; thresholding fractional selections preserves feasibility and yields an integral selection with at least the same reward/work ratio. This provides a direct link between code pruning, maximum closure, and fractional pricing.

Exact weighted minimum density can also be found by a DP indexed by total finished prize. In the improvement reduction, sum_h w_h<=n(n-1), so this is polynomial without a numerical pseudo-polynomial dependence on arbitrary enormous prizes. The linear-time profit DP at lambda=1 is enough to detect a strictly improving template prefix.

Conditioning a complete template on any observed state only prunes constant tests. Thus every one of these subroutines works at arbitrary algorithm-generated frontiers. It uses a supplied tree, not a nonimplementable entropy decoder.

## A cooperative cost sharing connection without submodularity

Define ell(C) to be the minimum raw work of a partial policy that identifies every member of C, with all outside hypotheses still charged for tests they encounter. It may identify extra hypotheses. Then ell is monotone and subadditive: execute one partial policy and then the other on the remaining frontier; conditioning and caching only decrease their combined work.

The optimal depth vector is a cost allocation in the core of this game:

    sum_h d_T*(h) = ell(H),
    sum_{h in C} d_T*(h) <= ell(C) for every C.

The second inequality is the exact completion dual applied to a cheapest policy identifying C. Thus every instance has such a nonnegative supporting cost allocation. Fractional covers by coalitions cannot beat ell(H), which is another way to express the exact covering LP. For an incumbent depth vector, a coalition violating this allocation is precisely a profitable partial-policy pricing opportunity. Approximate pricing therefore searches for an approximately blocking coalition and simultaneously improves an actual code.

This connection does **not** make ell submodular. A four-hypothesis example disproves that stronger hope. Let H={0,1,2,3}, and supply positive sets {0}, {1,2}, {1,3}. Then

    ell({1})=ell({1,2})=ell({1,3})=6,
    ell({1,2,3})=8.

For the two-element targets, query the corresponding pair cap, then split its positive pair, paying 4+2. Identifying just 1 also costs 6: either pair query leaves a two-element target branch; the singleton-zero query leaves a three-element branch and cannot do better. Identifying three out of four identifies the fourth by inference, so the full binary entropy lower bound gives cost 8, attained by a pair split and its two pair decoders. Therefore

    ell({1,2})+ell({1,3}) < ell({1})+ell({1,2,3}).

For a *fixed* full template T, its cost of identifying a requested set is the weighted coverage function sum_v |S_v| indicator[C meets S_v], summed over its internal nodes. This is submodular. Optimizing over different templates destroys that property in the explicit example. Therefore a generic submodular-minimization claim for unrestricted completion pricing would be incorrect, while the fixed-template closure algorithm remains valid.

research-general-coalitions-next.py independently computes ell by the full adaptive recurrence and finds this example. It is a finite falsification of submodularity, not an inapproximability result. The nonempty core and its depth allocation have the direct proof above; no cooperative-game theorem is assumed as an oracle.

## Uniform depth caps lose a logarithmic factor even within one template

Exact independent stopping is substantially stronger than uniform-depth harvesting.

For integer d, put s=2^d and n=(d+1)s. Let a template first split an easy group of s hypotheses from a hard group of ds hypotheses. Use a balanced d-level code on the easy branch and singleton search on the hard branch. Every query can be supplied explicitly as membership in the appropriate child set, so this is a valid binary test instance and template.

Stop immediately on the hard branch and fully decode the easy branch. This prefix costs

    n+sd=(2d+1)s

and finishes s hypotheses, with density 2d+1. Conversely any binary partial policy that finishes k uniform hypotheses has work at least k log_2 n. Its output partition includes k singleton cells; the entropy bound for that partition gives this inequality. Thus the optimum template-prefix density is Theta(d).

A uniform cap before depth d+1 finishes only a few singleton-search hypotheses and has density Omega(ds). For caps t between d+1 and ds/2, the hard branch alone costs Omega(dst), while at most s+t hypotheses finish. Its density is Omega(ds t/(s+t)), minimized at the start of this interval and equal to Omega(d^2). Later caps already pay Omega((ds)^2) work and finish at most n hypotheses, giving an even larger asymptotic lower bound. The cap at depth d+1 has density O(d^2). Therefore the best uniform cap has density Theta(d^2), a Theta(log n) loss compared with exact prefix mining.

This is an improvement of an internal pricing primitive, not an approximation improvement for the unrestricted decision-tree problem. Returning the cheapest complete known tree remains a valid nonregression candidate.

## Verification and remaining task

research-general-pricing-next.py compares the finish-count DP against exhaustive enumeration of all rooted stopping prefixes on 240 small binary trees. It checks 720 weighted rational Lagrange cases against the same independent enumeration. All agree. It also checks the easy/hard construction through n=1024, where exact prefix density is 15 and the best uniform-cap density is about 60.526. The asymptotic logarithmic loss follows from the proof above.

The continuation agent's polynomial state/intersection construction can use these weighted profit computations as a pricing diagnostic. Its explicit n=12 fixed point still has raw cost 47 versus optimum 46, so available code generation is not exact. The remaining general theorem would bound its pricing loss or supply a stronger polynomial generator; neither has been proved.

The primary-source search found related maximum-density precedence formulations in [Precedence-Constrained Decision Trees and Coverings](https://arxiv.org/abs/2602.21312). That paper treats extra precedence constraints, so its general approximation bounds do not solve the present unrestricted uniform target. The template closure derivation above is supplied directly and does not rely on importing a theorem for that different model.
