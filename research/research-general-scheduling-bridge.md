# Scheduling bridge: exact interleaving, continuation choices, and externalities

Auxiliary research note, 18 October 2026. The article is unchanged.

**Status.** Fixed independent block plans admit an exact polynomial Sidney index scheduler. However, freezing locally optimal plans before scheduling can have a polynomial approximation gap, even with uniform local priors and disjoint blocks. More strongly, an exact best isolated-project completion index can have an `Omega(sqrt n)` gap as a global completion-pricing oracle. These results identify the continuation information a broader scheduling bridge must preserve. No unrestricted approximation improvement or new UDT hardness is claimed.

## 1. Exact scheduling once the local clearing plans are fixed

Partition the nondefault hypotheses into disjoint blocks `C_i` and supply one actual all-default hypothesis `z`. A test assigned to a block is zero outside that block. Fix a clearing plan for each block. Its default path is a sequence of tests with disjoint fresh positive groups `A_ij` covering `C_i`; write `a_ij=|A_ij|`. At each positive exit execute a fixed actual identifying code on `A_ij`, of raw cost `g_ij`.

Only the default-path queries of different blocks can interleave. Every positive exit proves which block contains the target, so its side code is run immediately. If query `(i,j)` has global default-path position `t_ij`, the exact raw cost is

    sum_(i,j) a_ij t_ij + sum_(i,j) g_ij + L,               (1)

where `L` is the total number of default queries and the final term is the depth of `z`. The side-code sum and `L` are constants for these fixed plans.

Therefore the exact interleaving problem is single-machine weighted completion-time scheduling with one precedence chain per block, unit processing times, and job weights `a_ij`. At each step choose a remaining chain prefix maximizing

    total fresh-positive mass / number of queries,           (2)

schedule that prefix consecutively, and repeat. This gives an optimal interleaving in polynomial time. A naive implementation takes `O(L^2)` rational comparisons. This is the disjoint-chain specialization of [Sidney's decomposition theorem](https://pubsonline.informs.org/doi/10.1287/opre.23.2.283), not a new general scheduling theorem.

Here is a direct exchange proof. Let a maximum-density prefix `P` have length `p`, weight `dp`, and prefix weights at most `dj` after its first `j` jobs. Move `P` to the front of an arbitrary feasible schedule, preserving the order of other jobs. If an outside job of weight `w` originally preceded the last `p-j` jobs of `P`, the cost change associated with this crossing is

    (p-j)w - weight_of_suffix_P_after_j <= (p-j)(w-d).

For each other chain, the outside jobs involved form an initial prefix, all of whose own prefix weights are at most `d` times length. Their coefficients `p-j` are nonnegative and nonincreasing in chain order. Summation by parts makes their total contribution nonpositive. Thus an optimum can begin with `P` consecutively; recurse on the remaining chains. This proves (2) without assuming that the one-step positive mass is the correct index.

The established MSSC/Sidney connection extends much further in scheduling, for example [Happach and Schulz, Approximation Algorithms and LP Relaxations for Scheduling Problems Related to Min-Sum Set Cover](https://arxiv.org/abs/2001.07011). Those results do not by themselves select the conditional identification codes or settle the adaptive UDT comparison.

## 2. Locally optimal plans plus exact scheduling can be polynomially bad

Let every block have an even number `C=2p>=4` of hypotheses. Supply all singleton tests inside each block, the `p` disjoint pair-membership tests, and the whole-block membership test. All these tests are zero on other blocks and on `z`. There are `k` blocks. Every hypothesis, including `z`, has unit weight.

On a single block together with one unit-weight `z`, the whole-block test is the same binary partition as the singleton test for `z`. In that local instance the test family is just a graph of `p` disjoint pairs, with singleton tests at every vertex including `z`. Its exact optimum is

    G_local=C^2/4+2C.                                      (3)

It is attained by querying the `p` pairs along the `z` path and identifying a positive pair with one more query. The core alone has optimum

    F_core=C^2/4+3C/2-2.                                   (4)

Both formulas follow from the matching/first-hit proof already established in `direction5-robust-gadget-hardness.md`; this note does not relabel that result as new.

The local witness has unit weight throughout this argument. This obstruction does not rely on optimizing a local problem with a zero-weight witness; that weaker convention can also discard useful continuation options, but is not needed here.

The important additional fact is that **every** local optimal tree's path to `z` has fresh positive groups of size at most two. To see this, orient the local membership test as the singleton `z` and follow the all-miss path to its final leaf `w`. All first-hit groups are singletons or disjoint graph pairs. The matching lower bound is attained only with at least `p-1` pair groups, and all mass-two groups must precede all mass-one groups; reversing a singleton and a later pair strictly worsens weighted completion time. If `w=z`, the membership test is not queried on this path. Otherwise `z` is isolated only after at least `p-1` pair exits, which have already removed at least `C-2` core points. Along the path to `z`, the membership test therefore hits at most two residual core points.

Now freeze any local optimal plan in every block and permit globally optimal interleaving. Every default-path first-hit group still has size at most two. With `N=kC` core hypotheses, its raw cost is at least `Omega(N^2)`. The canonical pair plans have exact total cost

    G_frozen=N^2/4+2N.                                    (5)

There is a different valid global plan: query whole-block membership tests, then run the optimal core code in its positive branch. Its exact cost is

    G_membership=C k(k+1)/2 + k + k F_core
                =O(Ck^2+kC^2).                            (6)

For `k=C^2`, the ratio between (5) and this feasible benchmark is `Omega(C)=Omega(n^(1/3))`. The lower bound using groups of size at most two applies to every frozen collection of locally optimal plans, so tie-breaking among local optima does not remove the gap.

This is an approximation obstruction to a specific decomposition, not hardness of the full instance. The global membership-first plan is easy to construct. Exact interleaving cannot compensate for deleting globally useful continuation options when the local code is selected.

## 3. A small exact context reversal

A four-point core has tests with positive masks `3,5,15`: its two coordinate bits and its membership query. Give every outside hypothesis a private singleton test, and let all core tests be zero outside. On the uniform five-hypothesis instance with one outsider, the full optimum is `12`; either coordinate is an optimal first query, while core membership costs `13`.

On the uniform seven-hypothesis instance with three outsiders, the full optimum is `20`; core membership is the unique optimal core first query, while either coordinate costs `21`. An outsider singleton costs `23`, so the core is selected first in both environments.

Thus a fixed local core action, selected without its outside population, cannot be optimal in both contexts. This does not rule out index formulas that explicitly include global posterior mass or other context. It shows why a scalar local mean cost, or a local control chosen once, is insufficient.

The exact clearing profile of this core against an idle outside population of mass `M` is

    min{12+M, 10+2M, 9+3M}.                                (7)

The alternatives retain default-path length as well as core work. The best local continuation changes with `M`.

These complete-instance values have a short exact recurrence as well. Write `F(S,m)` for the remaining core subset `S` and `m` indistinguishable outside hypotheses, each with its private singleton query. It is zero when `|S|+m<=1`; otherwise it is `|S|+m` plus the minimum of `F_core(S intersect q)+F(S minus q,m)` over proper core queries, and `F(S,m-1)` when `m>0`. Thus the check uses only `16(m+1)` states rather than a general unrestricted oracle.

## 4. Polynomial parametric profiles retain this necessary information

For a supplied explicit local state DAG, let `R` be its residual core set, and let an allowed query split off `A` with supplied side-code raw cost `g(A)`. Define `a(R,l)` as the least core work of a clearing plan using exactly `l` further default queries. Then

    a(empty,0)=0,
    a(R,l)=|R|+min_query [g(A)+a(R minus A,l-1)].             (8)

All positive groups are nonempty, so `l<=|R|`. Evaluating (8) is polynomial in the explicitly represented DAG, local population, and allowed actions. The exact cost against `M` idle outsiders is

    min_l [a(R,l)+Ml].                                     (9)

Only `|R|` possible slopes occur. Prefix versions retain the actual residual state, default length, completed mass, and side-code cost. This provides a concrete continuation-aware replacement for selecting one local optimum before global scheduling. It is polynomial **when the local state DAG and side codes are supplied polynomially**; unrestricted local state generation is not solved by (8).

The profile (9) resolves the two context reversals above. It does not prove that choosing the currently best block profile or prefix gives a constant global approximation. The next obstruction shows why an isolated-project completion density can miss useful cross-project control even if every local profile is optimized exactly.

## 5. Exact isolated-project completion pricing can lose `Omega(sqrt n)`

Let the hypotheses be a small core `C` of size `k`, an outside block `O` of size `M=k^2`, and one default hypothesis `z`. Supply every singleton in `C` and `O`, and one membership test positive exactly on `O`. There is no core-membership test. All costs and priors are uniform.

Consider a proposed global completion oracle that chooses one project, may execute any of its tests and partial side codes, and stops its other-project outputs unfinished. Thus a `C` policy uses only its singleton tests; an `O` policy may use its membership query and singleton tests, but cannot continue in `C` on the negative membership response.

Every newly completed `C` hypothesis requires a separate singleton query that also charges all `M` outside hypotheses, so a nonempty isolated `C` policy has density at least `M`. Any isolated `O` policy restricts to a partial singleton-search policy on `M` equally weighted hypotheses. Its work per completed outside hypothesis is at least

    f(M)/M=(M+1)/2-1/M.                                   (10)

For completeness, if it finishes `t<M` requested singleton outputs, its restricted work is at least `tM-t(t-1)/2`; for full completion the minimum is `f(M)`. Allowing a locally singleton but globally unfinished last output does not weaken (10). Thus the exact best isolated-project density is `Omega(M)`.

There is a legal cross-project policy of much smaller density. Ask the `O` membership test. Stop its positive output unfinished. On the negative output identify all of `C union {z}` with the core singleton queries. It finishes `k+1` hypotheses at work

    (M+k+1)+k(k+3)/2.

With `M=k^2`, its density is exactly

    3k/2+1.                                               (11)

The gap between (10) and (11) is `Omega(k)=Omega(sqrt n)`. The useful query of the outside project may complete none of that project's hypotheses, yet its negative response activates a cheap continuation in another project.

This is a rigorous failure of a completion-index **pricing oracle** based only on isolated project continuations. It is not a UDT approximation lower bound: the full objective is dominated by identifying the large singleton-hard block. It does not rule out a richer branching-bandit formulation. It requires such a formulation to retain negative-response handoffs, unfinished positive branches, and actual outside query work. Simply summing local completion indices or treating an unfinished project as retired is insufficient.

## 6. Overlap and the remaining global bridge

Independent-chain scheduling in Section 1 assumes that a test changes only its own block's default state. General supplied tests do not satisfy that condition. Their answers may change several proposed code projects simultaneously, and a query may route to useful continuations in both responses. An exact representation by an explicit DAG of actual candidate contexts is possible and supports the existing Bellman algorithms; its unrestricted size can be exponential.

Classical branching bandits can retain some correlated project structure, but no primary theorem inspected here supplies a constant approximation for these overlapping, controlled identification projects. In particular, the partially adaptive correlated-Pandora approximation already audited in `uniform-decision-tree-formal-bounds.md` compares against a fixed inspection order and fixed observable side caps. It cannot be applied to the fully adaptive UDT benchmark or to the state-dependent continuation profiles above without a new comparison theorem.

The concrete algorithmic change supported by this pass is to preserve the full local time/core-work profile and to permit cross-project branch continuations in the actual policy DAG. Fixed-plan interleaving can then be optimized exactly as a subroutine. Universal polynomial generation and pricing of the overlapping continuation DAG remains open in this work; no little-o unrestricted guarantee follows.

## 7. Verification

`research-general-scheduling-bridge.py` compares the exact prefix-density chain scheduler with exhaustive product-state scheduling on small supplied chains, verifies the parametric core profile and uniform context reversal, audits all optimal local default paths in the pair-block construction, and checks the explicit asymptotic cost formulas and cross-project density family. Exponential local optimizers are used only for finite falsification and proof auditing, not as claimed polynomial UDT subroutines.
