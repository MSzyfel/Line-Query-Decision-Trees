# Genuine multi-context aliases and a root completion certificate

Auxiliary research note, 19 October 2026. No article or stable earlier script
was edited. The unrestricted approximation problem remains open.

**Result.** There is a deterministic growing serial family in which one
physical query is genuinely active on several contexts with different local
code meanings. A fixed-row slice's greedy code immediately loses the pure
projection property used by the previous recursive coverage theorem. Yet the
strong generator still has a constant approximation guarantee on a broad
algebraic version of this family, including arbitrary bounded-degree alias
graphs and different invertible affine local maps. A further result covers
independently nonlinear local maps under separated activation with bounded
incoming incidence. The proof uses executable
root partial policies and final stability, without replaying their conditional
codes outside the identified core. No claim that the first pass is optimal is
needed.

The core inequality is also a general certificate for any disjoint partition
whose cells are positive outcomes of supplied tests. It explains why breaking
projection purity alone is insufficient to defeat the generator.

## 1. A general root completion lemma

Suppose r>=2 disjoint nonempty cells C_1,...,C_r partition H, and for every v a
supplied binary test has positive outcome exactly C_v. Let B_v be an actual
complete code on C_v, with raw cost F_v. The following is an executable partial
policy P_v:

1. Ask the supplied test for C_v.
2. On its positive branch, run B_v and identify every hypothesis there.
3. On its negative branch, stop unfinished.

Its work and guaranteed completed set satisfy

    W(P_v) = n+F_v,    completed(P_v) contains C_v.          (1)

When the negative exit contains at least two hypotheses, its completed set
is exactly C_v. A singleton negative exit is already identified; that extra
completion only strengthens the inequality below.

This policy does not run B_v on an outsider. It does not assume a membership
test for any context other than the actual supplied C_v test.

For a current complete incumbent T, assign prize w_h=d_T(h). Running P_v,
then the incumbent restricted to its unfinished negative exit, gives raw cost
at most

    F_T - sum_{h in C_v} d_T(h) + n+F_v.                    (2)

The inequality holds because pruning T on H minus C_v can only reduce the
original depths of the remaining hypotheses. Hence a positive prize-work
profit is a strict actual improvement.

**Root completion certificate.** If the generator can optimize every P_v and
has reached a complete tree with no strict available improvement, then

    sum_{h in C_v} d_T(h) <= n+F_v    for every v,

and summing over the partition gives

    F_T <= r n + sum_v F_v.                                 (3)

The statement is about final incumbent depth prizes. It does not assume these
inequalities for the initial greedy tree, and it does not substitute arbitrary
fixed weights for d_T.

## 2. Why the existing polynomial generator contains these policies

Take B_v to be fresh uniform greedy on C_v. At every pass, the actual root is
H, and the source generator builds a full fresh greedy code on every supplied
root-query child. Thus all nodes of every B_v are retained as original
conditional source states. The negative outcome H minus C_v is also retained
as a forced-query child, or is a singleton already present as an incumbent
leaf. Consequently the exact supported depth-prize DP can take the root query,
complete its positive child, and stop at its negative child. It contains P_v
without using a lifted node or a quadratic intersection.

The strong actual-credit DP can realize the same partial policy with incumbent
fallback at its unfinished exit. A positive depth-prize profit would strictly
lower its actual output cost as well. Therefore its stopping condition implies
all the inequalities used in (3), irrespective of which other moves it chose
along the way. Weighted sources, global lifting, and state weaving do not
invalidate this certificate.

An explicit algorithm can simply choose any positive-profit P_v and splice
incumbent restriction at the miss. Each accepted move decreases the integer
raw cost by at least one. A proper n-leaf binary incumbent has raw cost less
than n squared, so there are fewer than n squared accepted moves. Codes B_v
can be precomputed and every current reward computed from the actual leaf
depths. This is a fixed-exponent polynomial procedure. More generally one can
enumerate root partial completions for both outcomes of all m supplied tests;
the algorithm need not recognize the useful partition in advance.

The certificate does not prove a constant in unrestricted instances: r can
be large compared with OPT, and the conditional greedy codes can be poor.

### Overlapping cores and a computable fractional-cover certificate

The disjoint partition is unnecessary. Let `mathcal C` be any explicit
collection of nonempty proper root-query outcomes, using either response of
any supplied test, and let G(C) be the actual raw cost of a fresh greedy code
on C. At a final stable incumbent, the same executable root partial gives

    sum_{h in C} d_T(h) <= n+G(C),    for every C in mathcal C.

For any nonnegative fractional cover satisfying
`sum_{C containing h} lambda_C >= 1` for every h, multiplication and summation
therefore give

    F_T <= sum_C lambda_C [n+G(C)].                         (3a)

All prizes are nonnegative, which justifies the first inequality when cores
overlap. Minimizing the right side is an explicit covering LP with n
constraints and at most 2m variables. Its codes, coefficients, and LP are
polynomially computable; singleton outcomes are allowed and have G(C)=0.
For identifying instances, the nontrivial supplied outcomes cover every
hypothesis. This is the restriction of the existing executable
completion-cover LP/prize-dual viewpoint from
`research-general-algorithm-next.md` to these root partial policies. It is
not a new LP relaxation. The restricted primal value is an **upper** bound on
both the final algorithm's cost and OPT, rather than a lower bound on OPT.
An approximation certificate additionally needs an independent lower bound,
such as entropy or a valid oriented support bound. Neither (3a) nor a good
small-instance value establishes a universal approximation ratio.

## 3. A genuine-alias serial family

Fix b>=2, M=2 to the b, an alias degree D>=2, and L>=1. Put M0=D M and

    H = [M0] times (F_2 to the b)^L,
    n = M0 M to the L.

The base coordinate x0 has M0 values; the later coordinates x1,...,xL are
uniform binary row vectors. Supply all pure equality tests for every coordinate.
For each k>=1 and each origin lower context
`a=(x0,...,x{k-1})`, choose an activation set A(k,a) of at most D lower contexts,
including a itself. For every actual context c in A(k,a), choose an invertible
affine map

    pi(k,a,c): F_2^b -> F_2^b.

Supply the b physical tests

    q(k,a,j)=1 exactly when the actual lower context c lies in A(k,a)
                           and bit j of pi(k,a,c)(xk) is 1.  (4)

Thus the **same physical test** is active in several different lower contexts,
and may read different affine functions of its row in each one. This is
genuine activation aliasing, not merely the private-context permutation
extension of the previous note. The activation graph and all affine maps can
be adversarial within the stated degree and invertibility conditions.

Test priority is: first all fast tests, ordered by ascending row factor k;
then pure equality tests, ordered by descending coordinate k. The order of
physical tests within each factor is arbitrary but fixed, including possible
interleaving of bits belonging to different origins. The affine theorem
permits all such orders; the finite checker uses consecutive palette blocks.
There are

    m = M0+LM+b M0 sum_{k=1}^L M to the (k-1)

tests before harmless exact duplicate removal. This is polynomial in the
explicit n-hypothesis instance. No parameter-dependent policy enumeration is
introduced when L grows.

Given x0 and then each successive lower context, the owner's palette in (4)
is an actual identifying code for the next row. It is therefore legal to
decode x0 by equality and all later rows in increasing order using b queries
per row. This gives the explicit comparison

    OPT <= e(M0)+Lb,    e(s)=(s+1)/2-1/s.                   (5)

## 4. Greedy is still bad before the base is fixed

**Lemma.** Initial balance greedy identifies all row coordinates in reverse
order xL,...,x1, using equality queries, before it starts decoding x0. The
row-query contribution alone is exactly L e(M).

At the start of a row, pure equality has positive mass 1/M. Every fast test
has positive mass at most D/(2M0)=1/(2M). When the current row has s<M remaining
values, equality has minority 1/s. A fast test on that same row has positive
mass at most D/M0=1/M, strictly smaller. A fast test on a lower, still uniform
row has positive mass at most 1/(2M). A fast test on an already fixed higher
row can hit at most D prescribed lower-context tuples; its mass is at most
`D/(M0 s)=1/(Ms)`, with additional factors of M when more lower rows remain.
These are also strictly smaller than 1/s. The descending equality priority
chooses the highest unresolved row whenever equality tests tie. It then
finishes that row before advancing.

After the rows are fixed, alias tests can be useful context-set tests on x0.
No claim that greedy uses pure equalities on x0 is made. In fact this is where
the previous projection argument can fail. This possible base improvement
does not erase the L e(M) row cost.

## 5. Explicit failure of slice projection

The checker uses deterministic D-context cyclic activation:

    A(k,a) = {(a0+t mod M0, a1,...,a{k-1}): 0<=t<D}.

Owner and alias meanings are different invertible affine maps, all sending
the zero row to the all-one label. The owner map complements the row; an alias
first permutes its coordinates and may apply an invertible triangular shear,
then complements. The actual finite maps are included in the saved results.

Consider the incumbent node where every row is zero. On that slice, a physical
bit test is positive on D base contexts, whereas an equality query is positive
on only one. The slice's fresh greedy code therefore begins with an aliased
test, not a pure base selector. Globally, that physical answer varies with the
row even when x0 is held fixed. The checker exhibits two such hypotheses
explicitly. Thus the pure-projection/transversal premise of the earlier serial
coverage proof really is false; it is not simply left unverified.

This construction breaks a particular proof mechanism. It does not give a
nonoptimal fixed point of the strongest generator.

## 6. Conditioning one base value nevertheless gives exact greedy row codes

**Lemma.** On every source core C_v={x0=v}, fresh uniform greedy identifies
x1,...,xL in ascending order, using exactly b queries for each. Hence

    F_G(C_v) = |C_v| Lb.                                    (6)

Assume earlier rows are known and the current row has a nontrivial uniform
affine-subspace posterior. Every active physical current-row test is an affine
functional of that row. On an affine subspace such a functional is either
constant or exactly balanced. The owner's invertible palette separates the
remaining points, so at least one of its functionals is nonconstant and
balanced. Taking any balanced current-row affine query decreases the posterior
dimension by exactly one.

No other test can have minority above one half. Earlier-factor tests are
constant. A higher-row fast test has positive probability equal to one half
times the probability that its lower activation context occurs, because its
target row is still independent uniform. Even if it ties at one half, the
ascending fast-test priority picks the current row first. Equality tests occur
after all fast tests. Thus greedy completes exactly b independent current-row
questions, and the induction advances to the next row. The argument uses the
actual context-specific affine meanings, not a globally consistent replay of
those meanings across different contexts.

Activation degree is irrelevant for this conditional lemma; its boundedness
is needed later to make the base partition cheap relative to OPT and to retain
the initial reverse-equality behavior.

## 7. Final strong-generator guarantee despite aliases

The supplied pure tests x0=v have disjoint positive outcomes C_v partitioning
H. Inserting (6) into the root completion certificate (3) gives

    final mean depth <= M0+Lb = DM+Lb.                      (7)

This is a final-stability bound. It is not asserted after one arbitrary pass.
It applies to the actual full strong generator because every required P_v is
generated afresh at its root on every pass, and any positive profit would be
a strict actual improvement. The earlier polynomial integer-descent bound
ensures that its final stable output is reached in polynomial time with a
fixed exponent. The proof is independent of global lifting behavior.

All supplied positive supports have size at most B=n/M. Pure row equalities
attain B. Affine bit positives are balanced within each active context and
have total support at most `D n/(2 M0)=n/(2M)` for k=1, and less for later rows.
The base equality support is n/M0. Because B>1, the oriented all-negative-path
argument from the previous note gives

    OPT >= (M+1)/2,
    OPT >= log2 n = log2 M0+Lb.                             (8)

Consequently the exact proved class-specific ratio is

    final output / OPT
      <= (DM+Lb) / max(log2 M0+Lb, (M+1)/2).                (9)

For fixed D and fixed c>=1/2, take `L=floor(c M/log2 M)`. Then (9) is at most
`1+D/c+o(1)`. For example c=D gives 2+o(1), and c=2D gives 3/2+o(1).

Meanwhile greedy pays at least L e(M)=Theta(M squared/log M), while the
explicit legal policy (5) costs O(M). Since log2 n=(c+o(1))M, greedy still has
an `Omega(log n/loglog n)` approximation gap. Thus this subclass combines
full-order greedy difficulty, actual multi-context activation, different local
code meanings, and a genuine failure of slice projection, yet the final
strong generator has a constant guarantee.

The result covers arbitrary degree-D activation graphs, including graph
patterns with no useful interval or laminar order. It is the algebra of the
conditional row queries and the cheap first partition that make the argument
work. The explicit cyclic example only verifies the projection failure.

## 8. Nonlinear extensions

### Shared latent coordinates

The conditional-row lemma still holds if, for every true lower context c,
there is an arbitrary bijection phi_c from row values to F_2^b, and **all**
physical palettes active at c have the form

    pi(k,a,c)(row) = A(k,a,c) phi_c(row)+t(k,a,c),

with A invertible. Greedy does not need to know phi_c. Uniform row points map
to uniform labels, and its posterior stays an affine subspace in those common
latent coordinates. The rest of the proof is unchanged. This allows nonlinear
context-specific row labels, provided the active palettes share this affine
coordinate system. The checker implements phi_c equal to the identity.

Arbitrary independently nonlinear local permutations need not preserve that
posterior invariant under an arbitrary interleaving of their queries. The
preceding proof of the exact Lb conclusion no longer applies. The following
two different structural conditions nevertheless give useful row bounds.

### Consecutive palette priority

If each origin's b queries are consecutive within its factor's test priority,
the exact Lb conclusion holds for arbitrary activation graphs and arbitrary
independent nonlinear bijections. Once the actual lower context is known,
take the first active current-row palette in that order. Its first query is
balanced on the uniform row. After its first t queries, its next bit is
balanced on its own uniform-label subcube. All preceding palettes are
inactive at the known context, and every competing current-row palette has
later priority. Higher tests cannot beat balance one half, and ascending
factor priority resolves any tie. Thus greedy completes this same palette
in exactly b queries before advancing rows. No activation-separation or
incoming-incidence assumption is required for this ordering corollary.

The checker uses this favorable block priority. Its nonlinear cases therefore
sanity-check actual nonlinear execution, but do not show tightness of the
more robust Pb bound proved next.

### Separated activation and bounded incidence

Now allow each `pi(k,a,c)` to be an arbitrary bijection from the M row values
to the b-bit labels. Impose these two additional activation conditions, for
every factor k:

* No origin activation set A(k,a) contains two contexts with the same x0.
  Thus fixing a base value leaves at most one of its actual contexts active.
* Each actual lower context belongs to at most P origin activation sets.
  This is an incoming-incidence bound; the earlier bound D is on the size of
  each origin's outgoing activation set. The two bounds are distinct.

The deterministic cyclic activation used by the checker satisfies both
conditions with P=D. Each origin's aliases differ only in their base value.
The assumptions also permit aliases with different other lower coordinates,
provided their base values are distinct.

**Conditional-row lemma.** On every C_v, fresh greedy completes the rows in
ascending order and spends at most Pb queries on each actual row path.
Consequently

    G(C_v) <= |C_v| PLb.                                   (10)

Assume earlier rows are known and the current row has a uniform surviving
set S of s>1 values; higher rows remain independent uniform. Some owner bit
separates S, so an available current-row query has minority at least 1/s.
By separated activation, any higher-factor physical bit can activate at only
one full lower-context tuple consistent with the known base value. Its
positive probability is at most 1/(2s); additional intermediate unknown rows
only decrease it. Higher equality tests have minority 1/M. At the initial
state s=M an owner bit is balanced, and later 1/s>1/M. Thus no higher-factor
test wins. Earlier-factor tests are constant. Greedy stays on the current
row until it is identified; no affine-posterior invariant is needed.

At the known current lower context there are at most P active palettes,
each with b physical bits, together with singleton row equalities. Fix the
owner's complete b-bit palette. Before the first singleton equality chosen
on an actual path, all queries are palette bits. If no singleton is chosen,
there are at most Pb such proper queries. Otherwise let q be the number of
owner bits already asked, and let s be the remaining row size just before
the first singleton query. Every remaining owner bit has minority at most
one, because greedy chose an equality of minority one. The previous owner
bits are constant. Among the s distinct owner labels, at most one agrees
with all remaining-bit majority answers; every other label lies in one of
at most b-q minority singleton cells. Hence s-1<=b-q. The prefix contains at
most q+(P-1)b bit queries, and any proper binary continuation on s row values
has path length at most s-1. The total path length is therefore at most Pb.
This argument includes the first singleton query in that continuation.

The root certificate and the unchanged entropy/support lower bounds give

    final mean depth <= DM+PLb,
    final output / OPT
      <= (DM+PLb) / max(log2 M0+Lb, (M+1)/2).              (11)

For fixed D,P and `L=floor(cM/log2 M)`, c>=1/2, this is at most
`P+D/c+o(1)`. The initial reverse-equality proof only uses uniform balance of
each bijective palette bit, so its full-order greedy gap also survives.
Thus arbitrary independently nonlinear local meanings are covered for
separated, bounded-incidence activation. General activation graphs which
retain several aliased contexts after fixing x0, or have unbounded incoming
incidence, remain outside this theorem. There is no unrestricted guarantee.

## 9. Bounded checks and what they do not establish

`research-general-aliased-routing.py` checks five deterministic instances.
There is no random search and no exact OPT oracle. It directly executes every
root partial policy, checks its completed set and work, verifies all positive
affine source depths equal Lb and nonlinear source depths at most PLb, audits
the initial reverse equality row contribution,
and exhibits the first nonprojected slice query.

It also starts an explicit root-partial descent from a deliberately poor legal
tree to exercise positive profits, actual pruning fallback, strict integer
decreases, and the final summed inequality. This reduced descent is weaker
than the full generator. Its outputs are evidence about the certificate
implementation, not counterexamples or claims about the strong algorithm's
finite output.

| b,L,D | n | m | Initial greedy raw cost | Poor legal incumbent | Root-partial descent output |
| --- | ---: | ---: | ---: | ---: | ---: |
| 2,1,2 | 32 | 28 | 203 | 356 | 205 |
| 2,1,3 | 48 | 40 | 361 | 740 | 406 |
| 2,2,2 | 128 | 96 | 1073 | 4920 | 1072 |
| 3,1,2, nonlinear | 128 | 72 | 1395 | 3924 | 1465 |
| 3,2,2, nonlinear | 1024 | 464 | 14905 | 204079 | 14784 |

At n=128 the known context-first tree also costs 1072, whereas initial greedy
costs 1073. The **reduced root-partial pricer** has no positive profit on that
initial tree; this merely shows that root-partial stability alone need not
imply exact optimality. The full lifting/weighted/boundary family was not run
to a fixed point here, so this is explicitly not a strong-generator failure.

For the two nonlinear checks, the owner's map is affine and the alias map
is an invertible affine permutation followed by a single transposition of
two nonzero-row images. Both send row zero to the all-one label. The checker
directly verifies bijectivity and that the alias map violates the affine
identity `f(x)^f(y)^f(0)=f(x^y)`. It uses b=3 because every permutation on
four points is affine. In both checks the actual source depths are exactly
Lb (3 and 6), consistent with the consecutive-palette corollary. Their robust
Pb path bounds are 6 and 12. Their actual summed root-certificate mean values
are 19 and 22; the order-independent separated-incidence bounds are 22 and
28. The full strong generator is not executed in these checks.

The root certificate's mean bounds are 10, 14, and 12 in the affine examples.
The initial greedy trees already fall below those conservative bounds; the
asymptotic theorem, not a finite improvement ratio, is the substantive result.
Saved raw trajectories, different affine maps, conditional code depths, signed
profit sums, nonlinear-map flags, and projection witnesses are in
`research-general-aliased-routing-results.json`. Syntax compilation passed.

## 10. Relation to the earlier serial proof and the next obstruction

The root certificate can simplify the **final-stability** analysis of the
earlier private serial family as well: fixing x0 starts its chain of fast
greedy conditional codes. It gives the coarser final bound M0 plus the bit-code
sum. The earlier quadratic coverage proof is stronger there: it supports the
complete comparison tree in one pass and pays e(M0), rather than M0, for the
base coordinate. Neither argument should be substituted for the other without
tracking that difference.

For the covered alias classes, outsider collisions are bypassed rather
than bounded: every root partial first identifies its core using an actual
supplied query. A surviving obstruction must therefore make that partition
too expensive relative to OPT, make its fresh conditional codes poor, or
remove the useful partition from the one-query outcomes. Independently
nonlinear palettes with interleaved priority and several aliases surviving
base conditioning remain a possible source-quality route; no failing family
is proved for them here. A recursively hidden first
partition is another; enumerating a growing number of conditioning tests
would not meet the required fixed-polynomial runtime. Those extensions remain
open, as does the unrestricted o(log n/loglog n) target.
