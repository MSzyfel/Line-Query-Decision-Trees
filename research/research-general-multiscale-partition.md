# Multiscale partitioning, collision frontiers, and the missing oracle

Auxiliary research note, 19 October 2026. This addresses the proposed
combination of branching with stronger partial partitions. The article is
unchanged. No unrestricted approximation improvement is claimed.

**The useful positive target is precise:** a constant-factor polynomial
algorithm for the cheapest partial tree whose average posterior cardinality
is at most a fixed power of the current population would give an
`O(loglog n)` approximation. This partial-tree problem has not been solved
here. There is, however, an exact polynomial frontier optimizer inside each
explicit template. It can be applied to branching-generated templates.

## 1. Why stronger partitioning would improve the bound

Write `F*(S)` for optimal raw work on a uniform state S. A partial original-test
tree P has work W(P) and a partition of output states R. It may stop with
several hypotheses still possible. Suppress constant queries.

First fix a shrink factor k. If an oracle always returns

    W(P) <= a F*(S),       max_R |R| <= |S|/k,

recursing on its exits gives an `a ceil(log_k n)` approximation, with the
usual final small-state convention. At every recursive level the states are
disjoint. Restricting one global optimal tree to them proves

    sum_states_at_level F*(S) <= F*(H).

Thus an individual level costs at most `a F*(H)`. A factor k polynomial in
log n only yields the familiar `O(log n/loglog n)` scale. Increasing the
number of hypotheses distinguished by a block is exactly the right place
to seek an improvement.

There is an important distinction between two stronger guarantees. A fixed
root-scale shrink k=`n^delta` would give a constant number of levels, but
when a descendant has fewer than k hypotheses that guarantee asks for full
identification. A state-relative power shrink

    max_R |R| <= |S|^eta,       0<eta<1,                    (1)

needs `O(loglog n)` levels, rather than a constant number. Indeed after j
levels every surviving size is at most `n^(eta^j)`. Therefore a polynomial
oracle of work at most `a F*(S)` satisfying (1) gives

    F(output) <= a [floor(log_(1/eta)(log_2 n))+1] F*(H).   (2)

All proper stages make progress, and the final explicit tree has at most n
leaves. Polynomial per-stage runtime therefore gives a fixed polynomial
overall runtime. There is no enumeration with a growing exponent in this
reduction.

The comparator policy exists: a full optimal tree meets every shrink
target at work `F*(S)`. The missing algorithmic task is finding a competitive
partial policy without knowing that tree. Existence of the truncation is
not an implementation of this oracle.

## 2. A collision target sufficient for O(loglog n)

For a partial policy define its unnormalized collision moment

    Z(P) = sum_R |R|^2.

Equivalently `Z(P)/|S|` is the expected size of the posterior state of a
uniform random hypothesis. Suppose that for a fixed `0<=theta<1` a polynomial
oracle produces

    Z(P) <= |S|^(1+theta),       W(P) <= a F*(S).           (3)

Every output R then has

    |R| <= sqrt(Z(P)) <= |S|^((1+theta)/2).

Consequently (2) gives `O(a loglog n)`. In particular, a constant-factor
approximation to the *minimum-work* policy subject to the collision target
would suffice: a full optimum is a feasible comparator. The condition in
(3) allows different paths to stop at different depths.

The analogous fixed integer p>=2 moment condition is

    sum_R |R|^p <= |S|^(1+(p-1)theta).

It implies a maximum leaf exponent `eta=(1+(p-1)theta)/p<1`. Higher fixed p
approaches the stronger maximum-size target, at a larger but still fixed
polynomial exponent for the template DP below.

More generally, `Z(P)<=|S|^2/k(|S|)` gives a maximum child size
`|S|/sqrt(k(|S|))`. For example, if `log k(s)=Theta((log s)^beta)` with fixed
`0<beta<1`, the number of recursive levels is
`O((log n)^(1-beta))`. If `k(s)=s^delta`, it is `O(loglog n)`.
A merely polylogarithmic k(s) yields `Theta(log n/loglog n)` levels.
These calculations specify useful targets for a branching search: seek a
superpolylogarithmic collision reduction at a constant multiple of OPT.

## 3. Exact polynomial frontier optimization inside one template

Let B be an explicit full tree made of original queries on S. Every internal
node v has actual population s_v. For an integer z define C_v(z) to be the
minimum work of a stopping prefix in that subtree whose output collision
moment equals z.

Stopping immediately gives

    C_v(s_v^2)=0.

At a singleton this is the only option. At a proper binary query, continuing
gives

    C_v(z)=min(C_v(z), s_v+min_(z1+z2=z)[C_left(z1)+C_right(z2)]).       (4)

The index is at most `s_v^2<=n^2`; there are O(n) nodes. The deliberately
loose bound O(n^5) arithmetic operations is sufficient. Reconstruction
retains actual original queries and permits independent stopping at every
branch. Fixed response count gives fixed-arity convolutions. For fixed
integer p, replace the stopping index by `s_v^p`; the same argument is
polynomial, with a fixed exponent depending on p.

Minimizing C_root(z) over z no larger than a chosen target is exact for all
prunings of this template. Minimize also over a supplied polynomial template
library. On newly observed states, restrict every template to the actual
state and rerun (4). This needs no precomputed closure under all possible
intersections.

`research-general-multiscale-partition.py` implements (4), reconstruction,
and recursion with the exact integer target `floor(s^(3/2))`. It uses
`isqrt(s^3)`, not approximate floating-point comparisons. This target gives
maximum leaf size at most `s^(3/4)`. The implemented procedure is polynomial
and legal. Its cost has **not** been compared within a constant factor to
unrestricted `F*(S)`; (2) is conditional on that missing comparison.

## 4. Coupling with bounded-menu branching

Suppose a polynomial-time rule supplies at most B candidate tests at every
actual state, and the response bound is r. At depth d, the number of
reachable transcript states is at most

    1+(rB)+...+(rB)^d.

For constant r,B and `d=O(log n)`, this is polynomial. Dynamic programming
over a state, remaining horizon, and collision integer z can use the same
stop and convolution recurrence (4), minimizing over its B candidate
queries. It optimizes all adaptive policies in that menu class without
enumerating `B^(r^d)` whole policy trees.

For slowly growing B, the elementary state-count argument instead requires

    d log(rB)=O(log(n+m)),

unless some separate structural state compression is proved. In particular,
`B=loglog n` and `d=Theta(log n)` does not satisfy this elementary polynomial
bound. A fixed menu and logarithmic depth are compatible with polynomial
runtime; choosing a menu that contains enough of a good partition policy is
the substantive approximation question.

The root's coupled-branching note develops the macro-policy version, which
can insert explicit greedy or conditional-code blocks as one menu action.
Such a macro must charge its *actual tests*, rather than being assigned unit
cost just because it occupies one search step.

## 5. Shannon entropy alone does not justify the same charging

One might weaken (3) to a constant-factor contraction in expected log size:

    sum_R (|R|/s) log_2 |R| <= (1/2)log_2 s,
    W(P)<=a F*(S).                                         (5)

These two guarantees alone do **not** imply an `O(loglog n)` approximation.
The cost of difficult hypotheses can be concentrated in the one continuing
cell, while entropy progress is collected on easy hypotheses. Here is an
explicit legal example. It concerns the sufficiency of (5), not hardness of
the minimum-cost entropy-target policy problem.

Let t>=4, `n=2^(3t)` and `K=2^(2t)`. There is a hard core of K hypotheses,
with only singleton tests nonconstant on the core. The remaining hypotheses
form dyadic easy blocks E_j of sizes `n/2^(j+1)`, j=0,...,t-1. Supply all
singleton tests, each block-membership test, and a balanced binary bit code
inside each easy block, with every bit test zero outside its own block.
There are O(n) tests and no nonconstant nonsingleton test on the core.

The core's exact raw optimum is

    f(K)=K(K+1)/2-1 >= K^2/2.

Restricting any full code to the core proves `F*(H)>=f(K)`. Conversely,
sequentially route to each easy block, decode it with its bits, and finally
search the core. This gives

    F*(H) <= f(K)+n(log_2 n+2)=Theta(K^2).

At state S_j, containing the core and all remaining blocks, `s_j=n/2^j` and
the next easy block has `e_j=s_j/2` hypotheses. Ask its membership query. On
the positive branch first perform

    u_j=ceil(K^2/(4e_j))

proper singleton queries, then finish the easy block with its available bit
code. Leave the negative branch unfinished. The singleton prefix alone costs

    e_j u_j-u_j(u_j-1)/2 >= K^2/8.

For t>=4 the total stage work is at most `3 f(K)<=3 F*(S_j)`: its upper
bound is `K^2/4+n(log_2 n+2)<=5K^2/4`. Its outputs are e_j singleton cells
and one continuing cell of size s_j/2. Therefore its expected posterior log
size is exactly

    (1/2)log_2(s_j/2) <= (1/2)log_2 s_j.

Thus every one of the t stages meets (5) with one fixed constant a. But
they spend at least `t K^2/8` before finally decoding the core. Since
`t=(1/3)log_2 n`, the resulting approximation loss is `Omega(log n)`.

The inefficient singleton prefixes are intentional. A minimum-work policy
for the same entropy target can omit them. The example shows that the two
stated guarantees are insufficient; it does not rule out a stronger greedy
or pricing rule that detects avoidable work. A collision target rejects this
example directly: the surviving half contributes `s_j^2/4` by itself.

## 6. Pure collision-gain density cannot benefit from lookahead

There is a sharp distinction between reaching the fixed deep target in (3)
and greedily maximizing collision reduction per unit work. For any actual
state S, the latter optimization over *all* adaptive partial trees is solved
by one best root query.

To see this, let a query q have response-cell sizes a_1,...,a_r on a state U,
with u their sum. Its collision reduction divided by its raw query work is

    g_q(U)=u-(sum_i a_i^2)/u.

This function is nondecreasing in every coordinate a_i. Indeed, with
`p_i=a_i/u`, its partial derivative is

    1-2p_i+sum_j p_j^2
       =(1-p_i)^2+sum_(j!=i) p_j^2 >= 0.

When U is a subset of S, each response count on U is at most the corresponding
count on S. Thus `g_q(U)<=g_q(S)`. Collision reductions telescope over all
internal nodes of any partial tree P, giving

    [|S|^2-sum_R |R|^2]/W(P)
       =sum_(query nodes U) [|U|/W(P)] g_(q_U)(U)
       <= max_q g_q(S).                                    (6)

The maximum is achieved by the single query attaining it. The weights in
the middle expression sum to one, because W(P) includes work on every
hypothesis, including those left unfinished.

Consequently a sophisticated multistep search scored only by collision gain
per unit work has exactly the same optimum as a single balance-greedy
query. This holds for any fixed response count, and in fact for arbitrary
finite arity. It does **not** apply to the cheapest policy meeting a fixed
deep collision target: that policy cannot substitute a cheaper shallow
query merely because the shallow query has better density. Nor does it
establish an analogous claim for Shannon entropy; conditional query entropy
can increase after restriction.

## 7. Avoiding repeated charges requires a stronger invariant

The existing completion-pricing reduction offers a different way to pay for
an entire block. Let T be a fixed incumbent. Credit a partial policy for the
*incumbent depths of the hypotheses it actually completes*, while charging
all tests on unfinished hypotheses as well. An alpha-approximation to this
weighted work/reward ratio gives an alpha-approximation to the full problem
by strict integer descent. The cardinality version gives a 4 alpha transfer
by a depth-quantile argument. These are proved in
`research-general-pricing-next.md`.

This is relevant to the new proposal because a well-chosen branching block
need not balance every exit. It could instead finish an efficiently selected
population and let the depth-prize or fixed-price LP compiler pay for its
work. That accounting does not charge the same scalar OPT once per size
level. The algorithmic gap remains proving that a polynomially generated
menu or template library contains a competitive block for the current
prizes. The collision oracle above is a concrete alternative target, with a
weaker but already valuable conditional `O(loglog n)` consequence.

## 8. Verification

The companion checker compares the collision DP to exhaustive independent
prefix enumeration on small supplied binary trees and their actual
restrictions. The saved run passed 792 prefix comparisons, 2,393 collision
threshold comparisons, 707 adaptive-density inequalities from (6), and 173
actual recursive stage checks. Every
reconstructed partial or complete tree uses original tests and has verified
state partitions and raw work. It also constructs and executes the entropy
counterexample policies at n=8,64,512, and checks the growing-parameter
formulas through t=30. These finite checks audit the exact primitive and the
counterexample accounting; the unrestricted oracle guarantee remains open.
