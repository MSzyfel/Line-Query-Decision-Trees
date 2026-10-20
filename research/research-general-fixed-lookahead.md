# Every fixed forced-query depth has a greedy-rollout barrier

Auxiliary research note, 19 October 2026. No article or stable earlier script
is edited. The unrestricted polynomial approximation target remains open.

**Status: proved for a robustly spaced variant of the selector family.** For
every fixed integer r>=1, there is an explicit uniform/unit-cost binary-test
family on which the initial balance-greedy tree has the full
`Omega(log n/loglog n)` approximation gap, but no depth-r adaptive forced-query
prefix, followed by fresh greedy at any or every prefix exit, improves it.
This includes all nonuniform prunings and actual incumbent fallback. The same
library has only `O(loglog n/log n)` unconstrained-coding drop per unit work.

The construction uses body alphabets `M-(2r+2)j`, rather than claiming without
proof the tighter `M-2j` spacing from the earlier two-selector note. The wider
fixed spacing makes arbitrary negative-gate punctures harmless to the
equality-only continuation argument. It changes no asymptotic conclusion for
fixed r. The existing completed-lift/conditional-source/intersection generator
is explicitly **outside** this negative class; fresh fallback at the leaves
of a globally replayed selector code already repairs this family.

## 1. Family and exact algorithm class

Fix r>=1, let k=r+1, and put a=2r+2. For sufficiently large even M, set

    ell=floor(M/(4a log2 M)),
    s_j=M-a j, j=1,...,ell,
    H=[M]^k times product_j [s_j], n=|H|.

Call the first k coordinates selectors and the remaining coordinates bodies.
All body alphabets are even and at least
`M(1-1/(4 log2 M))`. Supply every pure coordinate equality. For every full
selector context b, body coordinate j, and ordinary binary bit of its value,
supply the test positive exactly when the selector vector is b and that bit
is one. Put all pure equalities before all gates in tie priority. For fixed r,
the number of tests is `O(M^k ell log M)`, polynomial in the explicit instance.

The starting incumbent T is balance greedy. It decodes all bodies with pure
equalities, in increasing alphabet order, and then all selectors by equality.
Indeed a gate is supported on only one selector context, and all body
alphabets are strictly below M. With

    e(s)=(s+1)/2-1/s,
    D=sum_j e(s_j),
    H_eq=k(M-1)+sum_j(s_j-1),

its mean cost is `D+k e(M)=Theta_r(M^2/log M)`. A legal comparison identifies
the selectors first and then uses the active bit codes, at mean cost at most

    k e(M)+sum_j ceil(log2 s_j)=O_r(M).

Since `log2 n=Theta_r(M)`, T has the claimed full-order approximation gap.
No hypothesis/test geometry is used.

The forbidden class consists of every executable template obtained by:

1. Asking an arbitrary adaptive prefix of at most r proper supplied queries
   on each path. Different branches may use different queries or stop sooner.
2. At any subset of its exits, attaching the actual fresh uniform
   balance-greedy code for that exit's true state. Other exits may stay
   unfinished.
3. Pruning the resulting template at any collection of internal nodes.

Both responses and all adaptive branches can be used simultaneously. This is
stronger than choosing one favorable response of one root test. It does not
include inserting another forced query after a continuation has started,
iteratively retaining/grafting sources, global code replay, or state weaving.

For fixed r the number of adaptive prefix shapes and test assignments is at
most `m^{2^r-1}` times a constant depending on r. Generating their greedy codes
and optimizing all prunings is polynomial with an exponent depending on the
fixed algorithm parameter r. The statement rules out **each** such fixed
depth, not an algorithm whose exponent secretly grows with n.

## 2. Deleting points from a rectangular equality code

Write `F_T(S)` for the raw cost of the actual restriction of T to S. On a
rectangle U, T restricted to U is a product of equality combs, has height at
most H_eq, and at every internal node the larger child has at most M-1 times
as many hypotheses as the smaller child. For any E contained in U,

    F_T(U)-F_T(U minus E) <= (H_eq+M-1)|E|.                (1)

To prove this, first charge to every deleted hypothesis the original queries
on its path, at most H_eq. The remaining lost query contributions come from
nodes whose one child is fully deleted and whose other child retains a point.
Their fully deleted child subtrees are pairwise disjoint: if two such nodes
are nested, the deeper node lies in the ancestor's surviving child. Each
surviving sibling has size at most M-1 times the size of its fully deleted
child, in the original rectangular code. Their total extra charge is
therefore at most `(M-1)|E|`. This proves (1), including cascading pruning.

This is a special deletion bound for a rectangular product equality code,
not a generic Lipschitz claim about arbitrary trees or arbitrary states.

For any equality-only partial policy R run on the original uniform product,
each output state is rectangular and the standard equality identity gives

    Gamma_T(R)=F_T(H)-sum_output F_T(U)=W(R).               (2)

It holds for adaptive coordinate orders and unequal stopping depths.

## 3. Negative-only greedy continuations use only equalities

Consider any forced-prefix exit with no positive gate response. Its state is
a rectangle R minus at most g<=r gated pieces, each lying inside one full
selector context. A prefix of at most r queries leaves at least one selector
coordinate completely untouched by pure equality queries; denote it x_i.
It still has its full M values in the underlying rectangle.

We show inductively that fresh greedy does not query x_i or any gate while a
body remains unknown. It may use equalities on other selectors, which is
allowed and preserves the argument. At such a state, let A be the number of
selector tuples in the underlying rectangle, so A>=M, and let a remaining
body coordinate have s>=2 values. Each body value's multiplicity is between
A-g and A, times the common other-body volume. A body equality therefore has
minority probability at least

    (A-g)/(A s).

An x_i equality has positive probability at most `A/[M(A-g)]`, and any gate
has positive probability at most `1/(A-g)`. Since s<=M-2r-2, g<=r and A>=M,

    M(1-g/A)^2 >= M-2r+r^2/M > s,
    (A-g)^2/A >= M-2r > s.                                (3)

Thus a body equality strictly beats both alternatives. No x_i equality or
gate is selected before all bodies are known. All intermediate equality
outcomes keep the same form and the same untouched selector.

After the bodies are known, each gate is zero or a single selector point.
Every proper gate therefore has integer minority at most one. Some pure
equality is proper whenever more than one hypothesis remains and has integer
minority at least one. Pure equalities win ties. The entire fresh continuation
is equality-only and has height at most H_eq. The result also holds for
every pruning of it.

## 4. Exceptional positive mass and a single equality replay

Take any permitted partial policy P. Let E be the hypotheses whose execution
gets a positive gated answer during the forced prefix. Record only their
**first** such answer. These first-positive sets are disjoint. Let W_g be the
total raw work of gated queries in the forced prefix, including those on
already-positive branches if present, and put

    epsilon=1/((M-r)^2-r).

At a first-positive gate node, fewer than r earlier forced queries have
occurred. At least two selector coordinates are not fixed by positive pure
equalities; each retains at least M-r values in the underlying rectangle.
It consequently has at least `(M-r)^2` selector tuples. Earlier negative
gates remove pieces in at most r of them. The current gate's positive set
lies in one tuple. Therefore its positive mass is at most epsilon times that
node's actual state size. Summing the disjoint first-positive sets gives

    |E| <= epsilon W_g.                                   (4)

Delete all gated prefix queries, keep their negative branches, and discard
their positive branches. Keep the pure equality queries and the pruned
negative-only continuations. Replay this tree directly on H, obtaining R.
Every retained query was proper already on its smaller original state, so
the replay is executable, proper, and equality-only. Every replay output U
is a rectangle; its corresponding no-positive output of P is exactly
`U minus E`. Hypotheses in E may additionally be partitioned however P likes.

For hypotheses outside E the equality execution is unchanged. For hypotheses
in E, the additional replay work after their first positive answer is at
most H_eq each, because a proper equality-only path cannot exceed H_eq.
Discarded positive-side work is nonnegative. Thus

    W(R) <= W(P)-W_g+H_eq |E|.                            (5)

Ignoring P's nonnegative fallback costs on its positive-gate outputs, (1),
(2), and (5) imply

    Gamma_T(P)
      <= Gamma_T(R)+sum_U[F_T(U)-F_T(U minus E)]
      <= W(P)-W_g+(2H_eq+M-1)|E|
      <= W(P)-[1-(2H_eq+M-1)epsilon] W_g.                  (6)

For fixed r, `(2H_eq+M-1)epsilon=O_r(1/log M)`, hence is below one for all
sufficiently large M. Consequently

    Gamma_T(P) <= W(P).                                   (7)

This is uniform over all permitted prefixes, choices of continuation exits,
and prunings. Completing P by the actual incumbent restricted at every exit
costs exactly `F_T(H)+W(P)-Gamma_T(P)`, so no such move strictly improves T.
Repeated strict descent with this neighborhood cannot leave its starting
incumbent.

## 5. Coding potential and mixed-credit consequence

Let L(s) be the optimal unconstrained binary raw coding cost on s equiprobable
points, and put

    s_min=M-a ell,
    c=2(ceil(log2 M)+4)/s_min,
    K_n=ceil(log2 n)+1.

The equality-only product entropy lemma in
`research-general-resolution-bundle-obstruction.md` applies to R and gives
`Delta_L(R)<=c W(R)`. Also the increments of L up to n are at most K_n.
Ignoring P's nonnegative positive-side coding terms yields

    Delta_L(P) <= Delta_L(R)+K_n |E|
      <= [c(1+H_eq epsilon)+K_n epsilon] W(P).

Write `C_M=c(1+H_eq epsilon)+K_n epsilon=O_r(log M/M)`.
Together with (7), any accepted mixed-credit stage

    W(P) <= gamma Gamma_T(P)+alpha Delta_L(P), 0<=gamma<1,

requires `alpha/(1-gamma)>=1/C_M=Omega_r(M/log M)`. Accepting the bad
incumbent instead also requires this order of approximation factor. Thus
allowing any one fixed forced depth, all responses, arbitrary pruning, and
actual incumbent fallback does not remove the earlier mixed-score barrier.
This is a lower bound on the stated local template/certificate class, not
on arbitrary polynomial algorithms.

## 6. Bounded verification and remaining scope

`research-general-fixed-lookahead.py` checks the rectangular deletion lemma,
the exact all-pruning Bellman objective on a bounded deterministic set of
adaptive templates, and the symbolic constants for growing M. It makes no
exact OPT calls and no adversarial search. Finite template checks only audit
the accounting; the universal statement is the analytic argument above.

The saved run passed 592 exhaustive deletion checks on two tiny product
spaces, 18 deterministic full adaptive templates (with exact optimization of
all their prunings), and 21 growing parameter checks for r=1,...,6. The
explicit template instances have `(r,M,n,m)=(1,8,256,148)` and
`(2,8,1024,538)`. All 18 have maximum actual incumbent-fallback improvement
zero over their prunings. The second toy's coarse sufficient coefficient is
3/2, so the asymptotic theorem does not certify that toy solely from (6);
its zero gains are direct finite checks. The first toy's coefficient is
41/48. All 21 growing-family parameter checks satisfy the sufficient
coefficient below one. Results are in
`research-general-fixed-lookahead-results.json`; syntax compilation passed.

The original tighter `M-2j` family is not claimed for every r: with several
negative punctures its untouched-selector comparison needs extra care. The
spacing change in this note avoids that issue explicitly.

The existing stronger generator already escapes: an actual body-zero slice
has a pure selector code, its global replay produces full selector fibers,
and `finish_partial` runs fresh greedy fallback on each fiber, where the
body bit codes are active. Their completed code is retained in the first
pass. The forced-prefix barrier cannot be transferred to that generator or
to iterative global source synthesis.
