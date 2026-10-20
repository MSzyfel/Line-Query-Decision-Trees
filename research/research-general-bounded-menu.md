# Constant menus, logarithmic lookahead, and portfolio races

Auxiliary research note, 19 October 2026. The article is unchanged. This
addresses the new branching suggestion directly. There is no unrestricted
improvement theorem here. There is a positive polynomial algorithm, a new
constant-menu repair of a full-gap greedy family, and a rigorous reason the
menu must contain different kinds of choices rather than just the next few
most balanced tests.

## 1. The proposed search really can be polynomial

Let `M(S)` be a polynomially computable menu of at most b proper original
queries at actual state S. There are at most K responses per query. Let G(S)
be any supplied complete fallback tree, for example fresh balance greedy.
For a search horizon t, use raw external path length:

    V(S,0) = F_G(S),
    V(S,t) = min { F_G(S),
                   |S| + sum_a V(S intersect q^{-1}(a),t-1)
                     : q in M(S) }.

Empty responses contribute zero. Retain the attaining original query and
recursively reconstruct its chosen children. This optimizes every adaptive
menu-admissible prefix of path depth at most t, with independent stopping and
fallback at any node. Every physical response branch is present.

The important runtime is `(Kb)^t * poly(n,m)`, not enumeration of all full
policy assignments. Once a query is fixed, its response children are
independent optimization problems, so their minimum values can simply be
added. The search expansion is bounded by

    1 + Kb + (Kb)^2 + ... + (Kb)^t.

For constant b and K and t=O(log n), this is a fixed polynomial. Even without
state merging this bound holds. Caching `(S,t)` can reduce it further when
the menu depends only on S. If the menu uses history, include that history
in the search state; the same expansion bound still applies, though the
state-only cache is then insufficient.

For growing b, the safe condition is `t log(Kb)=O(log(n+m))`. Thus a growing
menu with t=Theta(log n) is not automatically polynomial. A polylogarithmic
menu and t=Theta(log n/loglog n) does satisfy the bound for fixed K.

This directly validates the runtime aspect of the user's idea. The open
approximation issue is whether a constant or slowly growing menu contains
sufficiently useful choices on every instance.

## 2. A two-choice menu that repairs a full greedy gap

Here is a genuinely different pair of choices; both are computed from the
response matrix without coordinate labels. Let

    mu_S(q) = min(|S intersect q^{-1}(0)|,|S intersect q^{-1}(1)|),
    beta(S) = max_q mu_S(q).

Offer these two proper queries:

1. A maximum-balance query, maximizing `mu_S(q)`.
2. A query minimizing `mu_S(q)` subject to the STRICT inequality
   `2 mu_S(q) > beta(S)`.

For ties in either choice, prefer smaller ORIGINAL ROOT minority `mu_H(q)`,
and then the original query index. Deduplicate the two choices. The second
choice lies at the less balanced edge of a constant-factor balance band.
The strict inequality and the original-root tie rule are consequential.
This note does not claim arbitrary balance bands give the result.

### The private-selector family

For M=2^p>=8, put R=M-2, L=floor(M/p), and take the uniform product

    H = [M] times [R]^L.

The first coordinate C is the selector. Supply all pure coordinate
equalities. For each selector value c and each body Z_j, supply the ordinary
p-bit binary encoding of Z_j in {0,...,R-1}, gated on C=c. There are no other
queries. Query order and hypothesis order may be arbitrary. Complementing a
supplied query globally changes neither menu statistic nor the argument.

Ordinary maximum-balance greedy decodes every body by equality before
learning C: body equality has probability at least 1/R, selector equality
has probability 1/M, and a private gate has probability at most 1/(2M).
With `e(s)=(s+1)/2-1/s`, its mean cost is

    L e(R) + e(M) = Theta(M^2/log M).

A selector-first code instead costs at most

    e(M) + Lp = O(M).

Since `log_2 n=p+L log_2 R=Theta(M)`, this is the full
`Theta(log n/loglog n)` greedy gap.

### Why the two-choice menu contains the good selector search

Consider any selector-only history with r>=2 possible selector values and
all body values still free. The pure-selector, pure-body, and private-gate
minority probabilities are respectively

    1/r, 1/R, and at most 1/(2r).

Consequently every gate is at or below half the maximum balance and is
excluded from choice 2. If r>R, the selector equality is the least balanced
query strictly above half the maximum because

    r<=M<R*2.

If r<R, selector equality is a maximum-balance query, so choice 1 contains
it. If r=R, selector and body equalities tie in current balance, but the
original-root minority of selector equality is 1/M<1/R, so the stated tie
rule chooses a selector equality. Therefore at every such history the menu
contains a pure-selector query. The selector can be completely decoded by a
menu-admissible equality comb in at most M-1 forced steps on any path.

At each selector exit, attach fresh greedy. Only pure-body equalities and
one-coordinate owner-bit queries are proper there. Fresh greedy has path
height at most Lp. To recall the useful bit-code argument: before the first
singleton equality on a body, suppose q owner bits have been asked. If that
equality wins maximum balance among s remaining values, every remaining
owner bit has minority at most one. All but at most one remaining label can
be charged to one of the p-q minority singleton bit cells, so s-1<=p-q.
Even asking only equalities thereafter takes at most p-q additional tests.
Thus each body's total contribution on every path is at most p, including
arbitrary interleaving between bodies.

The menu witness is therefore a legal full tree of mean cost at most
`e(M)+Lp`. Moreover `log_2 n >= 2M/3+1`, so M-1 is at most
`2 log_2 n`. Running the exact menu DP at

    t=ceil(2 log_2 n)

finds a tree no more expensive than this witness. Its search expansion is
`O(4^t)=O(n^4)` before polynomial per-state query/fallback work. This is a
polynomial constant-menu logarithmic-lookahead repair, with no supplied
selector representation, factorization, or fortunate initial greedy slice.
The entropy bound alone gives a constant approximation on this family
(for example less than 9/4); the earlier private-selector lower bounds give
sharper comparisons if desired.

**Scope.** This is a coverage proof for the stated one-selector family,
not arbitrary UDT. Canonical bit labels ensure each gate's on-fiber positive
fraction is at most one half. An arbitrary relabeling with a majority-one
gated bit can invalidate the simple balance-band exclusion argument. Extra
queries or noise need new analysis. Also M=4,R=2 does
not satisfy M<2R: the strict half-band rule then need not include the
selector initially. These exceptions are not hidden in the asymptotics.

### A deterministic refinement, including growing selector count

There is an even simpler rule on this canonical class: from the two offered
queries, choose the one with the smaller ORIGINAL root minority, breaking
remaining ties by query index. This repairs the stated family without
branching. Thus the example proves the menu's coverage, not a separation
between branching and every possible sophisticated greedy rule.

The same deterministic rule works with k selector coordinates, even when k
grows with the input, if every private gate requires the full selector tuple
and each selector still has alphabet M. At a selector-only history write
`r_i` for each unknown selector's remaining alphabet, `r_min=min_i r_i`,
and `A=product_i r_i`. A gate has minority at most `1/(2A)`, hence at most
half the maximum balance `beta>=1/r_min`. It enters neither offered choice.
If r_min<R the maximum-balance choice is a selector equality. If r_min=R,
the original-root tie also chooses a selector. If every r_i>R=M-2, all
r_i lie in {M-1,M}, and the less balanced edge of the strict half-band is
a selector. Therefore one of the two choices is always a selector. Its
original-root minority 1/M is smaller than the body-equality minority 1/R,
so the deterministic refinement chooses a selector.

After the full selector tuple is known, each nonconstant supplied test is
an owner bit or a pure-body equality. For a body with s remaining values,
some owner bit is proper and has minority at least 1/s, which is the
minority of a singleton equality. Thus a maximum-balance query can always
be an owner bit; the original-root tie prefers it because its root minority
is at most `1/(2 M^k)<1/R`. The first offered choice is therefore an owner
bit, and the root-minority comparison of the two choices selects an owner
bit as well. Every such query fixes one previously nonconstant label bit,
so at most Lp further tests occur on each path.

Selector equality cost telescopes over its product equality potential,
regardless of adaptive interleaving, and has expectation k e(M). The final
mean cost is consequently at most

    k e(M) + Lp.

This deterministic algorithm has a fixed polynomial runtime for growing k;
it scans the explicit tests at at most n-1 proper physical nodes. In
contrast, merely extending the logarithmic-lookahead witness to k selectors
would use horizon k(M-1), giving an exponent depending on k. No such hidden
exponent is needed for the deterministic refinement.

All the earlier scope restrictions remain. In particular arbitrary
majority-one gated label bits can enter the half-band before their selectors
are known. Extra noise/cross-coordinate queries can also change which
choices appear. No unrestricted approximation theorem follows.

## 3. Why the top b most balanced queries are insufficient

On exactly the same product family, consider the menu containing the b most
balanced proper partitions; complementary descriptions count as one
partition. Ties may be arbitrary. Suppose a history has never asked a
selector test or a gate and at least b body coordinates remain unresolved.
The actual state is still a product rectangle with the selector completely
free. Each unresolved body supplies a distinct proper equality partition
with minority probability at least

    1/R > 1/M.

Every selector query has minority 1/M and every gate at most 1/(2M).
Hence all b menu entries are body equalities. This remains true after every
body-equality response. It is independent of the search horizon. Fresh
greedy fallback has the same property.

A short equality-potential argument makes the cost loss precise. At a body
rectangle with r_j surviving values in body j, put

    Phi = sum_j e(r_j).

A proper equality on a body drops its expected Phi by exactly one, since

    e(r) = 1 + ((r-1)/r) e(r-1).

Before the menu can offer any nonbody query, at most b-1 body coordinates
remain unresolved. At that stopping time Phi is at most `(b-1)e(R)`.
Telescoping the preceding equality queries therefore gives the mean-cost
lower bound

    L e(R) - (b-1)e(R) = (L-b+1)e(R).

For b<=L/2 this is Omega(M^2/log M), whereas the selector-first comparison
costs O(M). Thus even unlimited depth of exact top-b-menu search retains
an `Omega(log n/loglog n)` gap. This includes constant b and many slowly
growing choices. It is a barrier for this particular menu, not for constant
menus in general: Section 2 gives a two-choice repair on the very same
instances.

## 4. A second implementation: physically race candidate cut policies

Branching over algorithmic options has another useful compilation when the
options are whole partial policies rather than individual queries. Suppose
P_1,...,P_b are supplied executable policies starting at S, each stopping
when its own remaining population has at most s hypotheses. For target h,
let tau_i(h) be the number of queries until policy i achieves this cutoff.

Run one virtual step of each policy in round-robin order. Keep every queried
answer and the actual intersection of their implied candidate states. A
virtual query constant on that stronger actual state is inferred for free.
Stop as soon as the actual state has at most s hypotheses. The first expert
to reach its own cutoff also certifies that the actual intersection has
reached the cutoff. Thus, pointwise for every h,

    depth_race(h) <= b min_i tau_i(h).

The best expert may differ from target to target. This is stronger than
comparing only the menu's cheapest expected-cost expert. No unknown
hypothesis is guessed, and no oracle membership query is used. With
explicit candidate policies the compiled proper partial tree has at most
n leaves, hence polynomial output size; virtual simulation work is also
polynomial in their total explicit representation size and n.

Let C_rho(S) denote minimum expected work of an actual partial tree all of
whose leaves have population at most |S|/rho. If a small generated menu
satisfies

    E_h[min_i tau_i(h)] <= kappa C_rho(S),

the race gives a b*kappa approximation for that cut problem. Recursing on
its leaves and using C_rho(S)<=OPT(S) gives the coarse global bound

    b*kappa*ceil(log_rho n) * OPT(H).

The restriction of one fixed global optimal tree to each disjoint phase
state justifies summing the local OPT terms per phase. This identifies the
needed tradeoff in the user's partition proposal: improve the achieved
shrinkage relative to the cost and menu factor, rather than improve one
factor in isolation. For this argument to beat log n/loglog n, it would
suffice to establish

    log rho / (b*kappa) = omega(loglog n).

No such universal menu-coverage theorem has been proved here.

To remove the phase count, a stronger sufficient certificate is an actual
amortized bound on the COMPILED cut, with raw potential Phi:

    W(cut) <= kappa [Phi(S) - sum_leaves Phi(leaf)],
    Phi(H)<=F_OPT(H),  Phi(singleton)=0.

That bound telescopes over recursive cuts. It does not follow automatically
from separate candidate-cut potential bounds: the race can stop before a
given expert reaches its own cutoff, so its output need not refine that
expert's completed cut partition. Finding a sufficiently strong computable
Phi and a universally covering menu is the substantive missing step;
entropy alone does not charge the expensive equality/activation histories
on all instances.

## 5. Reproducible checks

Run `python research-general-bounded-menu.py`. The algorithm implementation
uses only supplied queries. Exhaustive full-policy lists are confined to
depth-3 small-instance validation, and no optimal UDT oracle is supplied to
the algorithms.

The checked results are in `research-general-bounded-menu-results.json`:

- 24 Bellman outputs agree with explicit full-policy enumeration.
- 450 target paths satisfy the pointwise portfolio-race inequality.
- 945 body rectangles/widths satisfy the top-b menu exclusion, and 945
  equality-potential identities pass exactly over rational numbers.
- Six finite top-b DP runs pass actual-tree reconstruction and the proven
  cost lower bound.
- Four positive balance-band fixtures check every selector-count history
  on the witness comb, actual query legality, and the selector-first upper
  bound. On the 24-hypothesis fixture the complete depth-10 two-menu DP
  searches 118 cached states and reduces raw cost 134 to 128. Larger
  positive fixtures verify the supported witness rather than silently
  claiming the entire logarithmic-horizon search was executed there.
- Four deterministic root-minority fixtures include 1, 2, and 3 selectors,
  up to 864 hypotheses. Actual execution checks that every selected test
  before full selector identification is a selector equality and every
  later selected test is an owner bit, and verifies the mean-cost bound.

These finite checks support the implementations; the growing-family
claims rest on the arguments above.
