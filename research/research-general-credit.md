# General uniform decision trees: local credit and its computational bottleneck

Research auxiliary note, 18 October 2026. This file does not modify the article.

**Status.** No improved general approximation ratio is claimed. The main new result below is an explicit coNP-completeness theorem for validating a natural local Bellman-credit relaxation. The obstruction already appears when every local resource has only three hypotheses, even though all of those local optima are trivial to compute. A separate theorem shows why retaining only local completion profiles loses the entire target-order factor. These results distinguish an actual polynomial formulation from one that merely has polynomially many resource variables.

## 1. Model and the transferable part of the planar proof

Let H be an explicitly listed set of n hypotheses and let each supplied binary test be an explicitly listed map H -> {0,1}. All hypotheses have probability 1/n and every query costs one. Write F(S) for the minimum **unnormalized** leaf-depth sum on S. Thus the root expected optimum is F(H)/n and

    F(S) = |S| + min_tau sum_a F(S intersect tau^{-1}(a)).

Empty and singleton sets have F=0. A proper binary tree on s hypotheses has height at most s-1.

The planar manuscript uses the exact restriction credit

    Delta(S,Pi) = F(S) - sum_{A in Pi} F(A).

These credits telescope over recursive stages. The difficult issue in the general model is to compute a useful, coherent surrogate and to produce an executable stage whose cost it pays for. The manuscript's support-prefix lemma by itself does not provide a general decoder. This note instead examines a direct local-optimum surrogate.

## 2. A concrete lower-potential formulation

Choose a family R of small hypothesis subsets and nonnegative rational coefficients lambda_A. Define

    P_lambda(S) = sum_{A in R} lambda_A F(A intersect S).

For a test tau, define its Bellman deficit at S by

    D_lambda(S,tau)
      = P_lambda(S) - sum_a P_lambda(S intersect tau^{-1}(a)).       (1)

Every local optimum is restriction-superadditive: restricting an optimal tree on B to the cells of any partition yields

    sum_cells F(B intersect cell) <= F(B).

Consequently D_lambda is nonnegative. Impose the capacities

    D_lambda(S,tau) <= |S|       for every S subset H and test tau.   (2)

Then P_lambda(S) <= F(S) for every S. One proof is induction in the exact Bellman recurrence. Equivalently, sum (2) down any complete tree: the P terms telescope and the leaf terms vanish.

If |A| <= q for a fixed q, all local values F(A intersect S) can be precomputed in polynomial time. There are only n^{O(q)} coefficient variables. Nevertheless, Section 4 proves that exact separation of (2) is hard already for q=3. The exponentially many S constraints cannot be silently ignored.

There is also a precise algorithmic target. Suppose (2) holds, P is polynomially evaluable, and every nonsingleton S encountered by the algorithm has a test satisfying

    D_lambda(S,tau) >= |S|/alpha.                                 (3)

Choose a test maximizing D_lambda. The resulting complete tree has

    F_alg(H) <= alpha P_lambda(H) <= alpha F(H).                   (4)

Indeed |S| <= alpha D_lambda(S,tau) at every chosen node, and those deficits telescope. This is a valid rounding/composition criterion, not a proof that coefficients satisfying (3) exist. Both polynomial construction/certification and the lower bound (3) must be proved; a strong scalar value P(H) alone is insufficient.

## 3. Pairs admit polynomial capacity separation

For a two-hypothesis resource A={u,v}, F(A)=2. At a fixed test tau, its contribution to (1) is 2 lambda_A when u,v are both in S and have different outcomes, and zero otherwise. Therefore the maximum capacity violation is

    max_S [2 sum_{uv separated by tau, u,v in S} lambda_uv - |S|].  (5)

This is a maximum-weight closure problem: create a profit node of weight 2 lambda_uv for every separated pair, a cost node of weight -1 for every hypothesis, and implications from each pair node to its two endpoints. A minimum s-t cut solves it. Thus the polynomial pair formulation is real; the transition to triples below is not just an artifact of a poorly implemented oracle.

## 4. Triples make exact capacity validation coNP-complete

**Theorem 1.** Given an explicitly listed binary-test instance and nonnegative rational coefficients on three-hypothesis resources, deciding whether all capacities (2) hold is coNP-complete. This remains true when the test family consists of one block-membership test together with every singleton test. Every subset S is then an actually reachable candidate state, so the hardness does not come from imposing constraints on unrealizable sets.

The reduction is from strict-threshold MaxCut on 3-regular graphs: given G and integer C, ask whether MC(G)>C. Its complement is reduced to capacity validity. Thresholds C>=2 suffice. NP-hardness of MaxCut with degree at most three follows, for example, from Alimonti and Kann, *Some APX-completeness results for cubic graphs*, Theoretical Computer Science 237 (2000), 123-134, [primary paper](https://www.sciencedirect.com/science/article/pii/S0304397598001583), also [available PDF](https://par.cse.nsysu.edu.tw/resource/paper/2016/160607/Some%20APX-completeness%20results%20for%20cubic%20graphs.pdf). The elementary regularization described at the end of this section removes any convention about whether cubic means degree three or degree at most three.

Let G' be the disjoint union of nine copies of G. It is 3-regular and

    MC(G') = 9 MC(G).

Put r=C and create r new anchor hypotheses a_1,...,a_r, together with one hypothesis for every vertex of G'. The distinguished block test tau_0 returns 0 on anchors and 1 on graph vertices. Supply all singleton tests as well, ensuring separability and reachability of every subset by singleton misses.

For every anchor a_i and graph edge uv of G', use resource

    A_{i,uv} = {a_i,u,v},          lambda_{A_{i,uv}} = 2/(9r).      (6)

Any separable binary instance on three hypotheses has F(3)=5, F(2)=2, and F(1)=0: a proper three-leaf tree has depths 1,2,2. Thus all resource costs are known exactly without solving a hard local problem.

At tau_0, a resource has one anchor on one side and its graph endpoints on the other. With x_h=1[h in S], its unweighted deficit is

    x_{a_i}(2x_u + 2x_v - x_ux_v).                                (7)

Fix S, let k be its number of anchors, let U be its graph vertices, and let e(U) count edges of G' induced by U. Put lambda=2/9. Summing (7), and using 3-regularity, gives the exact violation

    V(S,tau_0)
      = (k lambda/r)(6|U|-e(U)) - |U| - k.                        (8)

For fixed U, this is affine in k in [0,r]. Its maximum is at k=0 or k=r. The first choice gives -|U|. The second gives

    lambda(6|U|-e(U)) - |U| - r
      = |cut_{G'}(U)|/9 - r.                                     (9)

The empty S gives zero. Hence

    max_S V(S,tau_0) = max(0, MC(G')/9-r)
                     = max(0, MC(G)-C).                          (10)

The distinguished capacity has a strict violation exactly when the source MaxCut instance is YES.

It remains essential to check all other tests. They do not introduce spurious violations:

* A singleton test for anchor a_i has deficit at most

      (2/(9r)) * 6|U| = (4/(3r))|U| <= (2/3)|U| <= |S|,

  because r>=2. Resources for other anchors are constant on one side.

* A singleton test for graph vertex u contributes zero unless u belongs to S. If it does, let k be the number of selected anchors and l<=3 the number of selected graph neighbors of u. Its exact deficit is

      (2/(9r))(6k + 2rl - kl)
       <= (4/(3r))k + (4/9)l
       <= (2/3)k + (4/9)l
       <= 1+k+l <= |S|.

These cover the entire supplied test list. Therefore **all** capacities hold if and only if MC(G)<=C. The construction has polynomial size: C can be assumed at most |E(G)|, there are O(C|E(G)|) nonzero resources, and their coefficients have polynomial bit length. A violated capacity has a polynomially checkable witness (S,tau), proving membership of invalidity in NP and completing coNP-completeness of validity.

For completeness, a subcubic graph can be made 3-regular while preserving MaxCut up to a known additive constant. For every missing unit of degree at v, attach a fresh K4 with one edge subdivided, joining its degree-two subdivision vertex to v. All new vertices then have degree three. The gadget has maximum internal cut six; its attaching edge can also be cut for either prescribed color of v, so each attachment adds exactly seven to MaxCut. The number of attachments is linear in the original graph size.

**Scope.** This theorem blocks exact all-state separation for this proposed triple-credit LP unless P=NP. It does not rule out a conservative polynomial relaxation, approximate separation with a controlled loss, a different extended formulation, or a decision-tree algorithm with a better ratio. The test instances used in this reduction themselves have an easy direct structural description; the obstruction concerns validating the proposed certificate, not the hardness of identifying those instances.

### 4.1 A stronger limitation: every fixed resource width retains a full-order gap

Let B_2(H) be the optimum root value of the pair-potential program of Section 3. Let B_q(H) permit all exact local-optimum resources A of size at most q, with the all-state capacities (2).

**Theorem 2.** For q>=2,

    B_q(H) <= floor(q^2/4) B_2(H).                               (13)

For q=3 the sharper bound holds:

    B_3(H) <= (10/9) B_2(H).                                    (14)

These comparisons do not require polynomial computation of B_q.

Here is a direct proof. For any nontrivial partition B=B_0 union B_1, the exact restriction credit obeys

    F(B)-F(B_0)-F(B_1) >= 2.                                   (15)

Take an optimal tree on B, color its leaves by their two partition classes, and choose a deepest node whose subtree contains both colors. Its children are monochromatic and nonempty. Restricting the tree to each color contracts the query at that node on every surviving leaf below it, saving at least two in total. Every other node's total contribution to the two restrictions is at most its original contribution. Finally replace the two restricted costs by their optima to obtain (15).

For resource A, replace F(A intersect S) by the pair sum

    G_A(S) = sum_{uv subset A} F({u,v} intersect S).

At a test splitting A intersect S into a and b hypotheses, the G_A deficit is 2ab, which is at most 2 floor(q^2/4). By (15) this is at most floor(q^2/4) times the original local-optimum deficit. If the test is constant both deficits vanish. Therefore, from any feasible coefficients lambda_A, the pair potential

    [sum_A lambda_A G_A(S)] / floor(q^2/4)

is feasible. At the root, G_A(H)=|A|(|A|-1), whereas a proper binary tree has

    F(A) <= |A|(|A|+1)/2 - 1 <= |A|(|A|-1).

The first inequality is the maximum leaf-depth sum of a proper binary tree, attained by a comb and proved by its elementary size recurrence. Thus the feasible pair potential has root value at least P_lambda(H)/floor(q^2/4), proving (13).

For q=3, keep each original pair resource unchanged and replace each triple resource lambda_A F(A intersect S) by (3/4)lambda_A G_A(S). When all three members occur and the test splits them, the two deficits are both 3lambda_A. When only a separated pair occurs, the replacement deficit is (3/2)lambda_A, below the original 2lambda_A. Other cases give zero. The resulting pair potential is consequently feasible. At the root each triple contributes (9/2)lambda_A instead of 5lambda_A, while pair resources contribute exactly their original value. Its root value is at least (9/10)P_lambda(H), proving (14).

This has a **positive polynomial consequence**: because pairs are allowed in the width-at-most-three program, B_2<=B_3<=10B_2/9. Solving the polynomial pair LP therefore returns a feasible certificate within factor 10/9 of the strongest width-at-most-three lower-potential objective, despite exact triple-capacity validation being coNP-complete. Pair coefficients are bounded by one, using the constraint on their two-element state and any separating test, so the pair optimization is a bounded rational LP with the mincut separation oracle of Section 3.

More strongly, the converted deficit at every S,tau lies between 3/4 and one times the original deficit, including mixtures with original pair resources. Thus if a particular supplied triple certificate satisfies the coverage condition (3), its converted pair certificate satisfies the same condition with alpha replaced by 4alpha/3. This preserves an existing coverage witness. Optimizing only the pair root value does not, by itself, guarantee that its chosen optimizer satisfies coverage (3).

For clarity, the pair Bellman program here need not be identified with the older shared-query program. Its required upper bound on the affine-equality family follows directly. Remove duplicate affine-hyperplane tests, which changes neither the optimum nor these capacity constraints. On H=F_Q^d, n=Q^d, there are

    M = Q(n-1)/(Q-1)

distinct affine hyperplanes: (n-1)/(Q-1) normal directions and Q offsets each. For distinct u,v, there are n/Q normal directions not orthogonal to u-v, and exactly two offsets in each such direction separate the pair. Every unordered pair is therefore separated by exactly

    R = 2n/Q

tests. For any feasible pair coefficients, summing the full-root capacities D_lambda(H,tau)<=n over these M tests yields

    R B_2(H) <= nM,
    B_2(H) <= Q^2(n-1)/(2(Q-1)) = O(nQ).                        (17)

Together with F(H)=Theta(nQd), proved for this family in the existing lower-bounds note, and d=Theta(log n/log log n), this gives

    F(H)/B_q(H) = Omega(d/q^2).                                 (16)

In particular, **every fixed-q exact local Bellman-credit cone has the full target-order gap**, regardless of how it is solved. Increasing q without bound is necessary within this formulation to remove that asymptotic obstruction; explicitly enumerating all q-subsets then has superpolynomial cost. This rules out a polynomial constant-width repair of the pair certificate, not other polynomial formulations or a compact implicit representation at growing q.

## 5. Local completion profiles alone have a full-order gap

A different tempting simplification is to solve every small restriction exactly, retain all its possible completion-profile vectors, and couple these profiles only through global leaf-depth marginals. This avoids the separation problem but loses adaptive query information.

For each A with |A|<=q, let C_A be the convex hull of completion-time marginals of **actual** identifying policies on A; allow a locally identified singleton to keep querying until its declared completion time. This padding is necessary when projecting a global policy to a smaller hypothesis set. Impose every such exact local constraint, with common global p_{h,t}, together with global K-ary Kraft.

**Theorem 3.** These constraints always admit the deterministic common completion time

    D = max(q-1, ceil(log_K n)),          p_{h,D}=1 for every h.    (11)

Consequently their optimum is at most nD, irrespective of the test table.

For each A, build any proper identifying tree of height at most |A|-1 and pad every leaf to depth D. It realizes the required local completion vector. Global Kraft holds because n K^{-D}<=1. No further fact about the instance is used.

In particular, even exact completion-profile restrictions on **every** subset of size q<=ceil(log_K n)+1 cannot force a lower bound above n ceil(log_K n). This remains true if one adds all local inequalities valid for those profile hulls, rather than just a selected list of entropy, rank, or mean-depth inequalities.

The affine-equality family already proved in [the existing lower-bounds note, Sections 10-11](uniform-decision-tree-lower-bounds.md) has n=Q^d, d=floor(Q/ln Q), binary tests 1[a dot h=b], and

    F(H) = Theta(nQd),        log n = Theta(Q).

For this family, (11) has cost O(nQ) when q=O(log n), leaving gap

    Omega(d) = Omega(log n/log log n).                            (12)

This does **not** refute the existing query-synchronized local-policy hierarchy: that hierarchy also couples x_{h,tau,t} and co-location/query marginals, which (11) does not supply. It shows precisely why those query couplings must not be discarded as a convenience. Constant-size exact depth profiles cannot provide the requested improvement.

## 6. Concrete next direction and remaining proof obligations

The pair/triple boundary suggests retaining tractable endpoint or closure capacities and spending extra expressive power on the **query-selection coupling**, rather than solving exact triple Bellman separation. A candidate polynomial method should provide all of the following in one formulation:

1. A finite, polynomially sized representation and an actual polynomial separation/optimization method.
2. A potential or global completion ledger shared across the eventual recursive tree.
3. A constructive analogue of (3), or a suffix-completion comparison with a proved loss.
4. A rounding rule that queries one common supplied test on every current state.

The exact triple-resource program above fulfills the potential accounting but fails the first obligation. Small local profile hulls fulfill a finite-state local validity requirement but fail the second/third obligations on an explicit full-order family. No polynomial repair or improved general ratio has been proved here.

## 7. Reproducible audit

The companion [research-general-credit.py](research-general-credit.py) exhaustively checks the local deficit identities, the full capacity maximum, and singleton-test feasibility on small regular graphs. Exhaustive enumeration is used only to audit the theorem; it is not proposed as a polynomial decision-tree algorithm.
