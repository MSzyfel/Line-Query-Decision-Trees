# Logarithmic menu search for deeper hypothesis partitions

Auxiliary research note, 19 October 2026. This answers the user's proposed
combination of small-menu branching and stronger partial partitions. The
article is unchanged. No unrestricted asymptotic approximation improvement
has been established.

## 1. The proposed search is polynomial

At state S, compute at most b candidate original queries. For a fixed
fallback tree G(S), use

    V(S,0)=F_G(S),
    V(S,t)=min{F_G(S), |S|+sum_a V(S intersect q^-1(a),t-1):q in menu(S)}.

Every response child is optimized independently; their optimal costs add.
The algorithm does not enumerate the Cartesian product of all complete
child policies. With at most K responses, expansion has at most
sum_(j<=d)(bK)^j histories. Constant b,K and d=O(log n) therefore give a
fixed-exponent polynomial. State caching can help but is not needed for
that guarantee. A growing menu requires d log(bK)=O(log(n+m)), with an
absolute constant, rather than automatically allowing both b and d to grow.

More significantly, a choice may be a long explicit partial query tree P,
not just one test. Let its exit states E partition S. The recurrence is

    V(S,t)=min{fallback(S), W(P)+sum_E V(E,t-1):P in menu(S)}.

At action level j, the sum of all state-occurrence populations is at most
n b^j: each candidate policy partitions its input, and offering b policies
multiplies that sum by at most b. Every nonempty occurrence has population
at least one, so the number of occurrences is at most

    n sum_(j=0)^d b^j.                                     (1)

This remains polynomial for constant b and logarithmic d even when a block
has n exits or many physical queries. It permits a small menu of long
greedy blocks, conditional code runs or other executable procedures.
Primitive query depth and the number of design choices must be distinguished.
Singleton-query instances can require linear primitive depth even for a
half-size cut, while greedy already solves them optimally.

The menu is the remaining approximation issue: exact optimization of a
restricted action family does not establish its quality against all trees.

## 2. What a deep partition must achieve

Write F*(S) for the optimum raw query work on the current uniform state.
If a polynomial procedure produces an original-test partial tree satisfying

    W(P)<=a F*(S),             max_exit |E|<=|S|/k,

then recursion costs at most a ceil(log_k n) times global OPT. At each
recursive level the states are disjoint, and restricting one global optimal
tree to them proves sum_S F*(S)<=F*(H). The factor counts recursive levels;
it is not a fractional-rounding loss.

A particularly useful target is, for a fixed 0<eta<1,

    W(P)<=a F*(S),             max_exit |E|<=|S|^eta.         (2)

After j levels the largest state is at most n^(eta^j). Thus (2) gives an
O(a loglog n) approximation. For example a constant-cost comparison and
square-root-size exits would already improve the requested asymptotic bound.
This cut exists by pruning OPT; finding a competitive cut is unproved.
The full optimal tree is a comparator, not a polynomial oracle.

A slightly weaker maximum-size condition can be obtained by controlling the
integer collision moment

    Q(P)=sum_exits |E|^2.

Its normalized value Q(P)/|S| is expected remaining population. If, for
fixed 0<theta<1,

    Q(P)<=|S|^(1+theta),       W(P)<=a F*(S),                (3)

every exit is at most |S|^((1+theta)/2), so the same O(a loglog n) reduction
applies. A superpolylogarithmic shrink slower than a power can also improve
the target order; a power shrink is a clean stronger target.

For a constant approximation, another sufficient route is to charge the
actual selected block to a decrease in residual optimum:

    W(P)<=C [F*(S)-sum_exit F*(E)].

This telescopes over the whole recursion and removes the phase count.
Optimal-tree prefix cuts satisfy such an identity, but that optimum is
unknown. A computable search can use actual incumbent restriction costs
as its terminal scores. Comparing the menu's profitable cuts with the
optimal-cost decrease remains a coverage theorem, not a consequence of
longer lookahead alone. Earlier auxiliary contraction notes develop that
incumbent-credit version in detail.

Large average Shannon information alone is insufficient for this level
argument: it can be earned on easy hypotheses while leaving the hypotheses
carrying most of OPT in a large cell. The multiscale note gives a precise
counterexample to relying only on entropy gain and a per-stage OPT bound.
It does not refute approximating the minimum entropy-target policy itself.

## 3. Coupling the search to a fixed deep target

For a size cap B fixed during one invocation, replace full fallback by fresh
greedy cut at its first states of size at most B. Stop for free whenever
|S|<=B. The same Bellman recurrence finds the cheapest searched menu policy
with that fallback and the required cap. Its final tree uses original tests.
Mass-cut macros are also stopped at their first internal states of size at
most B. This compulsory early acceptance differs from arbitrary pruning of
their interiors.

For a collision target, keep an integer-indexed cost curve A_(S,t)(z).
At depth zero use every stopping prefix of G(S), whose exact curve is a
bottom-up tree convolution. For a macro with exits E_i, continuing gives

    W(P)+min_(sum_i z_i=z) sum_i A_(E_i,t-1)(z_i).           (4)

Take the cheaper of this and the fallback curve. Stopping at S contributes
z=|S|^2 and zero work. All indices are at most n^2, so these convolutions
add a fixed polynomial factor to (1). This optimizes all adaptive menu
compositions, permitting independent later choices and stopping depths at
different exits. Interiors of the supplied macros are fixed; only the
stated fallback tree permits arbitrary internal pruning in this prototype.

This is a concrete way to couple both suggestions. The search objective
specifies a large total partition improvement, rather than selecting a
single test by immediate progress per unit cost.

For collision gain this distinction is necessary. In fact the best ratio

    [|S|^2-Q(P)]/W(P)

over every nontrivial adaptive partial policy is attained by a single root
query. For response counts a_i on a node U, its local gain per work is
g(a)=sum_i a_i-sum_i a_i^2/(sum_i a_i). This function is nondecreasing in
each response count, so g(q,U)<=g(q,S) for U subset S. A whole policy's
ratio is the work-weighted average of its query-node ratios, hence cannot
exceed the best root value. Lookahead therefore cannot improve this pure
gain/work rule. A fixed deep target as in (4) is a different optimization
problem and is not ruled out by this observation.

## 4. A small menu needs different sorts of choices

The bounded-menu note proves a failure of the most immediate shortlist:
offering just the top b most balanced tests can retain the full greedy gap
even with unlimited search depth. Many body-equality queries can exclude
all useful selector queries from that menu.

A concrete alternative is the pair

* a maximum-minority query;
* a minimum-minority query among those with minority STRICTLY greater than
  half the current maximum.

Break ties by smaller ORIGINAL root minority, then query index. Both are
computed from the response matrix, without hidden coordinate labels.
On the stated canonical private-selector family, the second option offers
the selector when it is slightly less balanced than a body equality, and
the first offers it once its remaining alphabet is smaller. Private gates
stay at or below half the current maximum along this selector-first witness
until the relevant selectors
are known. Thus logarithmic-depth search contains a selector-first code
of cost O(M), where ordinary greedy costs Theta(M^2/log M) and log n=Theta(M).

This is a proved coverage example, not a general ratio theorem. A subsequent
refinement can select between these offerings deterministically by original
root minority and repairs the same canonical class even with growing
selector count. Consequently the example does not show branching is
necessary against every possible greedy rule. Arbitrary extra tests or
unbalanced relabelings are outside this coverage proof.

There is now a stronger explicit limit to balance-only menus. Add all
three-value membership tests on every body of that family. As long as any
body remains unresolved, an available body test has minority probability
at least min(1/3,3/R)>2/M. Every selector or private gate has probability
at most 1/M while the selector is untouched. Thus ANY choice within half
the best balance is forced to remain a body test. Such tests have positive
caps at most three and need Omega(R) expected queries per body. The full
greedy gap survives arbitrary search depth. More generally constant caps
c>A defeat every rule restricted to a factor A of best balance, for large
enough M. This does not rule out arbitrary small menus: it says they must
sometimes offer much less balanced queries or structured code blocks.
Proof and checks are in `research-general-band-cap-obstruction.md`.

## 5. A compact LP combines the entire bounded search family

The coupled-branching note extends the earlier exact policy-cover LP to
any downward-closed family of acceptable exits, including |E|<=B. Fractional
coverage of all hypotheses by acceptable exits compiles to an actual such
partition without cost increase. Outsider work remains in every column.

The polynomial unfolded menu structure also gives an extended LP over all
of its adaptive policies and prunings. At each virtual state, split incoming
policy weight among the candidate actions, and COPY each action weight to
every response-exit child. Coverage of h is its total acceptable-exit weight.
This is policy inclusion weight, not a split of hypothesis probability mass.

A direct restriction-aware AND/OR profit compiler turns feasible rational
flows into actual partitions at no greater work. It may restart the virtual
program on newly observed subsets; its output need not retain the original
d-action horizon. A separate at-most-n productive-application bound gives
polynomial compilation. The restricted LP is an upper benchmark for the
unrestricted cut optimum; no missing approximation theorem is supplied by
the formulation alone.

## 6. Prototype and verification

`research-general-branching-partition.py` implements size-cut search, full
work-versus-collision curves, long-macro composition, reconstruction, and
the explicit two-query menu. Its checker compares 24 size-target solutions
against 99 exhaustively enumerated small full policies. Exhaustive policy
enumeration is validation only. It checks 69 actual collision frontiers
and a long-macro unfolding with 12 response exits; all output paths and
work values use the original matrix. Fixed-template frontiers are compared
independently against every stopping prefix on bounded instances.

`research-general-menu-partition-lp.py` separately validates 29 exact feasible
rational flow points over 1,442 unfolded occurrences. The compiler performs
31 productive applications and always meets the stated leaf caps at work
at most its point's objective. It does not implement LP optimization.
Other bounded-menu, multiscale and independent-audit checks are recorded
in their separate notes and result files.

The precise remaining target is a polynomially generated small menu whose
searched or fractional policy family satisfies (2) or (3), or an equivalent
OPT-drop amortized bound, for arbitrary response matrices. Both user ideas
fit a polynomial algorithmic framework; that universal menu comparison
remains open.
