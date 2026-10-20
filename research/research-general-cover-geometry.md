# Fractional policy covers compile directly; paired bridges expose a useful quotient

Auxiliary research note, 19 October 2026. The article is unchanged. This pass
proves a polynomial compiler for an explicitly supplied fractional cover and
a structured decoding guarantee for the complementary paired-bridge family.
It proves no unrestricted approximation improvement. The general task of
finding sufficiently good policies or a useful implicit pricing algorithm
remains open.

The executable completion LP and its exactness were already developed in
`research-general-algorithm-next.md` and `research-general-lp-next.md`. The
refinement here is a direct deterministic compiler for a feasible fractional
solution, without an incumbent, local-descent loop, or set-cover rounding
factor. Root independently derived the same compiler and extends it to a
compact template-prefix LP in `research-general-template-cover-lp.md`.
`research-general-fractional-rounding-audit.md` independently checks the proof.

## 1. Direct compilation of an explicit fractional completion cover

Write work in raw units: a query asked at state S costs |S|, so a full code
has work equal to the sum of its hypothesis depths. All policies below use
actual supplied queries. A partial policy may stop at several nonsingleton
states. Its actual completed set C_i consists of hypotheses reaching singleton
leaves. Let d_i(h) count **every** query asked on h, including paths ending
unfinished, and let W_i=sum_h d_i(h).

**Theorem.** Given explicitly represented partial policies P_1,...,P_s and
nonnegative rational weights x_i satisfying

    c_h = sum_(i:h in C_i) x_i >= 1       for every h in H,               (1)

one can construct a complete original-query decision tree T in polynomial
time with

    F_T <= sum_i x_i W_i.                                             (2)

The result holds for binary or any fixed finite response alphabet. It is
about the supplied finite policy family; its right side need not be a lower
bound on unrestricted OPT.

Define fixed prizes and state potential by

    v_h = sum_i x_i d_i(h),       V(S)=sum_(h in S) v_h.                 (3)

For n>1, (1) gives v_h>=1. At a current nonsingleton state S, restrict each
P_i to S by suppressing constant queries and retaining all of its actual
unfinished terminals. This executable restriction P_i|S has work

    W_i(S) <= sum_(h in S) d_i(h).                                    (4)

Every h in C_i intersect S remains completed; restriction can complete more
hypotheses. Define the conservative deficit

    D_i(S) = W_i(S) - V(C_i intersect S).

Equations (1), (3), and (4) imply

    sum_i x_i D_i(S)
      <= V(S) - sum_(h in S) c_h v_h <= 0.                            (5)

A policy is productive if C_i intersect S is nonempty. Unproductive columns
have D_i(S)=W_i(S)>=0, and some positive-weight productive column exists by
coverage. Thus at least one positive-weight productive column has D_i(S)<=0.
Choose a minimum-deficit productive column, execute its actual restriction,
and recurse at every nonsingleton unfinished exit.

For the disjoint unfinished exits U, induction and the guaranteed completed
hypotheses give

    cost(S) <= W_i(S) + sum_U V(U)
            <= W_i(S) + V(S)-V(C_i intersect S) <= V(S).                (6)

At the root, V(H)=sum_i x_i W_i, proving (2). Singleton exits accidentally
created by restriction only strengthen (6). The n=1 case is a free leaf.

Each productive application permanently completes at least one fresh
hypothesis. There are at most n such applications across the entire output
tree, because different recursive branches have disjoint hypothesis sets.
At an application, one can explicitly restrict and scan each positive-weight
policy and compare its exact rational deficit. Proper input policies have
O(n) nodes each; a safe straightforward implementation is polynomial in
n, s, total policy description length, and the input rational bit length.
All prize sums and comparisons have polynomial bit length. The final proper
binary tree has n leaves and n-1 query nodes. There is no optimum-tree,
pricing, or density oracle hidden in this compiler.

This also reproves the exactness of the all-executable-policy completion LP:
a full optimum tree is one feasible column, and the compiler turns any
finite feasible fractional solution into a tree of no larger cost. The
exponential implicit column family is the unresolved algorithmic issue.

## 2. A concrete polynomial root-core algorithm

For every supplied response cell C, compute a fresh greedy code B_C on C.
Use the partial policy that asks the original query defining C, runs B_C
on that response, and stops on the other responses. It has work

    W_C = n + F_(B_C)(C),                                             (7)

and completes at least C. If another response is already singleton, its
additional actual completion causes no difficulty. Choose nonnegative x_C
by the polynomial-size covering LP

    minimize sum_C x_C [n+F_(B_C)(C)]
    subject to sum_(C containing h) x_C >= 1 for every h.               (8)

There are at most K m columns for K responses. Standard rational LP
optimization, followed by Section 1, produces an actual code no more
expensive than (8). Given a rational feasible point, the prototype verifies
it and compiles it directly; it does not require an LP installation.

The same upper benchmark was previously obtained from the root-star
depth-prize certificate in `research-general-aliased-routing.md`. The new
point is direct constructive compilation, without first reaching a stable
incumbent. Neither formulation proves that (8) approximates OPT: the local
codes themselves can be poor and useful policies can require several
conditional queries before reaching a profitable core.

## 3. Convex support filtering: precise capability and limitation

At one response-cell size B, let A be the 0/1 incidence matrix of all supplied
cells of that size. Root's affine-support filter retains a column j exactly
when some real solution of Ax=1 has x_j nonzero. A stronger polynomial
convex-support filter can instead use

    P = {x >= 0 : Ax=1}.                                              (9)

For a nonempty cell, any feasible x obeys x_j<=1. Thus P is bounded, and its
support is computable with at most one feasibility LP and one coordinate
maximization LP per column: retain j iff max_(x in P) x_j>0. This preserves
every actual partition and prunes every column forced zero by nonnegative
exact coverage. It uses no clique search or vertex enumeration. This note
does not claim that the remaining columns expose a useful partition.

In particular, the paired bridges below occur in genuine partitions. They
survive both affine support and this convex-support strengthening. A method
that retains **all** supported queries can nevertheless exploit their full
response quotient, which is much smaller than the original hypothesis set.

## 4. Complementary paired bridges preserve the initial greedy gap

Use the XOR-alias construction of `research-general-xor-aliases.md`:

    M=2^b, R=M/2, k>=2, 0<ell<M,
    H=F_M^k times (F_2^(b-1))^ell.

C=(C_0,...,C_(k-1)) are selectors and Z_j are body rows. The original tests
are all body equalities, pure selector equalities, and the translated-bit
gates

    q(j,g,u) = [f_j(C)>>1=g] AND bit_u[Z_j xor (C_0>>1)],

where each f_j is a nonzero-coefficient linear form, distinct body forms
have independent rows, and (f_j,C_0) has rank two. These are exactly the
forms and deterministic field implementation in the earlier XOR note.

For each selector coordinate i, add the two opposite bridge tests

    q_i^+ = [C_i in {0,1}] AND [Z_0,0 xor (C_(i+1 mod k)&1)],
    q_i^- = [C_i in {0,1}] AND NOT[Z_0,0 xor (C_(i+1 mod k)&1)].          (10)

Each positive support has size B=n/M. Given the complete body vector Z,
the next selector's low bit is still independent and balanced, so each
bridge remains positive with probability 1/M. This remains true after any
pure-body equality history. Ordinary gates have the same independence.
An unfinished body equality has minority at least 1/R=2/M. Therefore fresh
greedy identifies all body rows by equality tests first, paying at least
ell e(R), where e(s)=(s+1)/2-1/s.

A legal selector-first code still has mean at most

    U=k e(M)+ell(b-1).                                                (11)

For fixed k,c>0 and ell=floor(cM/log2 M), initial greedy consequently retains
the full-order Omega(log n/loglog n) gap from the XOR construction.

Each paired bridge belongs to an actual size-B partition:

    {positive(q_i^+), positive(q_i^-)}
      union {C_i=v : v=2,...,M-1}.                                    (12)

Thus no exact-cover coordinate-support test, even over nonnegative weights,
can remove these columns while preserving all partitions. In the disjointness
graph both bridges connect to selector i's other-value cells. The resulting
component contains overlapping selector and bridge cells and fails the
whole-component partition check. Every bridge is attached to a selector
axis, so none of the B components is accepted. This is a limitation of that
specific component rule, not a hardness claim for finding arbitrary covers.

## 5. The entire affine-supported family has a cheap quotient decoder

The newest `linear_select_families` deliberately includes the **whole**
affine-supported query family at every response size, even when none of its
disjointness components is accepted. On the paired family that provision
prevents the preceding geometry from being a full-gap obstruction.

For M>=8, its supported size-B cells are exactly the pure selectors and
paired bridges. To prove this, consider any real Ax=1 solution. Varying one
body bit at a fixed selector context kills its ordinary gate coefficient
unless that bit is Z_0,0, because bridges depend only on Z_0,0. For the
exceptional bit, use a context outside

    U_0 = {C : at least one C_i lies in {0,1}}.

Every ordinary activation group contains such a context. Indeed, solve its
linear equation for one selector coordinate after fixing all but one other
coordinate outside {0,1}. As that remaining free coordinate varies, at most
two choices are forbidden by its own value and at most two by the solved
coordinate; each group has a permitted solution for M>=8. At that point all
bridges vanish, so varying Z_0,0 forces the exceptional ordinary gate
coefficient to zero too. Selector and bridge columns are supported by their
actual partitions. No assertion that real cover coefficients are themselves
nonnegative is used in this elimination.

The retained response word reveals exactly C and, if C lies in U_0, the one
bit W=Z_0,0. Outside U_0 it reveals no body bit. Its quotient alphabet size is

    Q=M^k+|U_0|=2M^k-(M-2)^k,                                        (13)

and its residual hypothesis multiplicities are R^ell or R^ell/2. Their
ratio is two. The retained original-query palette has size at most

    D=kM+2k.                                                         (14)

It remains to justify what the actual factor planner does on this nonuniform
quotient; treating the quotient values as uniform would be incorrect.

**Entropy decoder lemma.** Suppose a finite value Y is identified by D_i
static binary queries and all its surviving atom weights have ratio at most
two. Let h_*=h_2(1/3). A most-balanced eligible-query decoder, where the
static queries are always eligible, has expected depth at most

    D_i [1+ln(H(Y)/h_*)]                                             (15)

when H(Y)>0. All entropies use base two; ln denotes the natural logarithm.

At a nonsingleton state, its largest atom is at most 2/3, so H>=h_*.
Subadditivity for the identifying palette gives

    H(Y) <= sum_q H(q(Y)) <= D_i max_q H(q(Y)).

The most-balanced query maximizes binary response entropy, even if extra
queries become eligible conditionally. For the selected query, child entropy
H' therefore satisfies E H'<=H-H/D_i. Define phi(0)=0 and
phi(H)=1+ln(H/h_*) for H>0. For every positive child entropy,

    phi(H)-phi(H')=-ln(H'/H) >= 1-H'/H,

including children with H'>H. For a zero-entropy child the same inequality
holds because phi(H)>=1. Thus expected phi decrease is at least 1/D_i.
Induction on the finite decoder tree gives (15), with no discrete-tail
rounding assumption. An exact small-alphabet decoder only improves this bound.

The factorization routine partitions the retained query coordinates into
independent **support** factors. If their static palette sizes are D_i, then
sum_i D_i<=D. At every factor context and every surviving subset of one
factor, its original-hypothesis atom weights still have ratio at most two:
each factor value contains the same number of remaining quotient words,
each with residual weight between R^ell/2 and R^ell. The retained queries of
that factor are always eligible in the implemented conditional decoder and
identify its values. Additional original queries may become eligible; (15)
continues to apply. Hence decoding every factor in any fixed order costs at
most

    D [1+ln(log2(Q)/h_*)]                                             (16)

in mean. This argument does not require the quotient to be prime. The dynamic
factor planner is no more expensive than this fixed factor-order plan.

After all quotient factors are decoded, C is known and perhaps W is known.
Every remaining body bit has an active ordinary query giving a balanced
split. Bridge queries are now constant or one such body bit. Body equalities
cannot give a more balanced split; ties on a two-label row also finish that
row in one query. Actual fresh greedy therefore finishes in at most
ell(b-1) further questions, even with arbitrary interleaving of body rows.

The entire newest portfolio includes this supported family, its factor plan,
and a recombination stage no more expensive than that plan. Its output obeys

    output_mean <= D [1+ln(log2(Q)/h_*)] + ell(b-1).                     (17)

For the growing fixed-k,c regime above, (17) is O_(k,c)(M loglog M), whereas
OPT>=log2 n=(c+o(1))M. Thus the output/OPT ratio on this subclass is
O_(k,c)(loglog M)=O_(k,c)(logloglog n). This is a repair of this specific
candidate obstruction, **not** a general approximation theorem. No source
code lifting, unsupported outsider replay, or unknown optimal-code oracle
is used in the proof.

## 6. Bounded executions and exact scope

The public prototype is `research-general-cover-geometry.py`:

    compile_cover(instance, policies, weights) -> (complete_tree, statistics)

All weights and deficit comparisons use `fractions.Fraction`. Its
`restrict_policy` explicitly handles unfinished terminals; the older backend
restriction routine assumes a complete tree and is unsuitable here. The
prototype validates every actual path, singleton completion, stored work,
coverage inequality, and final compiled work. It never calls an LP or an
exact decision-tree solver.

| Compiler fixture | Columns | Fractional work | Compiled work | Productive calls |
| --- | ---: | ---: | ---: | ---: |
| Five-cycle pair completions | 5 | 35/2 | 12 | 2 |
| Cube, multiple unfinished exits | 8 | 56 | 24 | 4 |
| Same cube, nonexact cover weights | 8 | 70 | 24 | 4 |

In the five-cycle fixture each policy completes one adjacent pair, costing7;
weights1/2 give exact coverage. Any integral selection of these columns needs
at least three policies, costing21, yet the compiler constructs the optimal
binary coding work12. This distinguishes executable policy restriction and
interleaving from integral set-cover selection. The cube overcover has
minimum coverage1 and maximum coverage2, checking that equality is not
required in (1).

The paired-bridge checks execute the **entire** newest
`linear_selected_context_pass`, including its original families, all-supported
families, one independence-refinement level, actual factor plans, and pooled
depth-prize recombination:

| M,k,ell | n | m | Initial/output raw work | Supported B queries | B components accepted | Quotient Q | Families / pool states / contexts |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| 4,2,2 | 64 | 20 | 400 / 400 | 12 | 0 | 28 | 11 / 192 / 317 |
| 8,2,1 | 256 | 32 | 2520 / 2520 | 20 | 0 | 92 | 5 / 766 / 613 |

Both supported response relations factor as one nonuniform-residual quotient
in these finite executions, and their factor-plan cost equals the displayed
incumbent cost. The M=4 support classification is checked directly; the
general elimination proof above is stated for M>=8. The finite equalities
are not asymptotic fixed-point evidence: (17) rules out a surviving full-order
greedy gap along the growing paired family. Neither computation checks the
separate stronger library containing every completed conditional source lift,
weighted code, verification policy, or quadratic/actual-boundary closure.

Exact results and trajectories are saved in
`research-general-cover-geometry-results.json`. No broad random campaign,
unbounded search, or exact-OPT validation was used in this pass.

The constructive progress is a lossless polynomial compiler for finite
fractional policy covers. The geometric limitation is that even genuine
partition membership does not make whole-component extraction sufficient.
The positive subclass result is that keeping the whole supported response
family can recover a useful small quotient when no component partition is
accepted. The unrestricted challenge is to generate cheap covering policies
or prove a useful quotient exists; these results do not settle it.

## 7. Refinement: a static retained-row fallback gives a constant class bound

Root's subsequent local-decoder refinement adds a second candidate at each
factor context: ask that factor's retained original queries in a fixed
sequence, skipping queries constant on the current factor-value subset.
Compare its raw work with the existing greedy decoder and retain the cheaper
code. This paragraph describes that strengthened decoder; (15)-(17) remain
valid for the preceding greedy-only implementation.

If factor i has D_i retained queries, their joint responses identify its
values by the definition of the response factor. Each is constant on every
actual factor-value cell at the context, so each remains eligible throughout
this sequence. After at most D_i questions the factor is known. Constant
queries cost zero because they are suppressed. This is a pointwise depth
bound and makes no uniformity assumption about the value weights.
The candidate is built directly by partitioning the explicitly listed
factor-value cells with successive retained rows. It takes polynomial time
in D_i and the input table size; it never enumerates all 2^D_i answer words.

The sequential decoder and the greedy decoder have exactly the same factor
values as their terminal states. All continuation costs used by the factor
planner therefore agree, independent of which decoder is used; comparing
their raw works is sufficient. At most D_i original questions are asked by
the sequential candidate, and summing over all factors gives at most
sum_i D_i<=D questions to identify the whole retained quotient. The planner
is no more expensive than the plan that decodes every factor this way and
then invokes its existing fresh-greedy fallback.

For the paired family, the full quotient reveals C and possibly Z_0,0.
The actual fresh body continuation is consequently still bounded by
ell(b-1), exactly as in Section 5. Hence the strengthened entire portfolio
obeys the sharper explicit class bound

    output_mean <= D+ell(b-1),       D=kM+2k,
    output/OPT <= [kM+2k+ell(b-1)]/[k log2 M+ell(b-1)].                 (18)

For fixed k,c>0 and ell=floor(cM/log2 M), this is

    output/OPT <= 1+k/c+o(1).                                        (19)

Thus paired-bridge camouflage does not survive this polynomial decoder
fallback even as a superconstant approximation obstruction. The guarantee
is for this subclass and the strengthened decoder, not an unrestricted
constant-factor theorem. The original finite values in Section 6 are the
saved executions before this new fallback; they are preserved rather than
silently relabeled as results for the modified algorithm. Root handles the
new decoder's regression checks separately.
