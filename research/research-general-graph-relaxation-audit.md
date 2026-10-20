# Independent graph-relaxation audit and bounded-alias extension

Auxiliary research note, 19 October 2026. The article is unchanged.
This independently audits `research-general-dependency-graph.md` and
records an extension to physical tests with several activation tuples.
These are structured-class results; no unrestricted ratio follows.

The strongest audited version is the charged recurrence in Section 4:
private full-cube gates admit factor two, bounded aliases admit
\(D+P\), and supplied owner codes improve the latter to \(D+1\).
The uncharged comparisons below are intermediate valid bounds.

## 1. Audit of the initial uncharged private-gate comparison

No material issue was found in the free-activation proof. The following
points make its scope and conditioning explicit.

The relaxation's full history stores each paid coordinate-equality result
and every value learned by a free reveal. Every resulting state is a
Cartesian product of uniform coordinate candidate sets. The node of the
original simulated tree is a deterministic function of that stronger
history: every simulated original response has already been entailed by
the individual checks and revealed values. Conditioning on which original
query is visited therefore imposes no additional event once that full
history is fixed. It cannot introduce the correlation that would arise
from remembering only an unresolved conjunction's answer.

During one private-gate simulation, reaching the next paid parent check
requires the preceding paid check to have hit. Its conditional probability
is at most one half. Free-activation closure after a hit or a last-value
miss can only remove later checks. The conditional expected number of
paid checks is consequently below two. Summing this conditional bound
over the original tree's visited queries is valid even though the stronger
simulator may already know extra coordinates.

Directed cycles and self-parents do not invalidate the relaxation. No
coordinate is free until all its parents are genuinely known. A paid
singleton completion can trigger an activation cascade through a cycle.
With a self-parent, that coordinate simply cannot become newly free before
it is already known.

The count-only state is sufficient because equality values are symmetric
in the relaxation and eligibility depends on which coordinates are known,
not their values. Availability of a physical code at every parent tuple is
essential to this symmetry. Every paid transition strictly reduces the sum
of counts, including after closure. There are exactly
\(\prod_i M_i=n\) possible unclosed count vectors. The raw cost at a state,
obtained by multiplying its conditional mean by the product of its counts,
is an integer with polynomial bit length. Thus the exact DP is polynomial
in the explicit hypothesis count; it is not an exponential-in-input-width
oracle disguised as a constant-dimensional algorithm.

Finally, physically replacing each free reveal by a supplied enabled
single-coordinate code preserves product posteriors. The paid-equality
cost remains exactly the relaxation value; each coordinate incurs its
decoding overhead at most once on a path. The initial bound
\(A+\sum_i b_i\le3\operatorname{OPT}\) for \(M_i=2^{b_i}\) is sound.
Section 4 below audits the stronger charged recurrence and improves this
to two.

The theorem can use a supplied coordinate/parent representation as its
class certificate. The separate canonical response-matrix recovery
argument based on a target projection of size \(M/2\) requires the target
not to be its own parent. A self-parent gate can collapse to a singleton
or empty query, so that particular projection argument does not recover
self-loops. This does not affect the supplied-representation theorem.

## 2. A physical query with at most D activation tuples

Fix one parent set \(\mathrm{Pa}(i)\) for each coordinate. Allow a physical
target-\(i\) test to have the form
\[
 q(x)=\bigvee_{a\in A_q}
       [x_{\mathrm{Pa}(i)}=a]\,f_{q,a}(x_i),
 \qquad |A_q|\le D,
\]
where each \(f_{q,a}\) is any Boolean function. The tuples in \(A_q\)
are distinct and are full assignments to the same parent set. Arbitrary
additional cross-coordinate tests are not allowed.

Simulate the alternatives one by one. For an alternative whose already
known parent values disagree, or whose required value was excluded, its
contribution is zero. Otherwise check its unknown parent values in a fixed
order and stop that alternative at the first mismatch. If all agree, all
parents are now known and the relaxation freely reveals the target.
Its local function is then evaluable. Every alternative costs fewer than
two paid checks conditionally on the entire preceding stronger history.
There are at most \(D\) alternatives, hence
\[
 A_{\rm root}\le2D\operatorname{OPT}.                         \tag{1}
\]
The final original answer is still entailed by the checks and free values,
so the same rectangle invariant applies to subsequent original queries.
The alternatives need not be independent; the bound is conditional before
each alternative and simply sums their costs.

Suppose that, whenever its parents are known, coordinate \(i\) can be
identified by at most \(c_i\) supplied target-only physical tests. The
same count policy gives a real code with
\[
 \operatorname{ALG}\le A_{\rm root}+\sum_i c_i
 \le2D\operatorname{OPT}+\sum_i c_i.                           \tag{2}
\]
For \(M_i=2^{b_i}\), if \(c_i\le P b_i\), binary information yields
\[
 \operatorname{ALG}\le(2D+P)\operatorname{OPT}.                 \tag{3}
\]
One sufficient certificate is that each full parent tuple is active in at
most \(P\) palettes of \(b_i\) bits, and at least one of these palettes
identifies all \(M_i\) target values. Asking the union of their active
physical bits uses at most \(Pb_i\) tests. Their local meanings can be
arbitrary unrelated bijections. No greedy-quality lemma is required.

If a complete owner palette is explicitly identified at each parent
tuple, it can instead be queried directly in \(b_i\) tests. The same
proof then gives the sharper \(2D+1\) ratio. More generally the additive
term in (2) should use the actual certified enabled-code widths, rather
than automatically charging \(P\).

All recognition assumptions are explicit: coordinate factors, the parent
sets, test activation tuples and local meanings, and a polynomial-time
enabled-code constructor can be supplied as a class certificate and
checked against the explicit response matrix. Their polynomial discovery
in arbitrary hidden representations is not proved here. The count DP and
reconstructed original-test tree are polynomial once this certificate is
available. If different alternatives of one query use different parent
sets, matching one alternative need not enable the target in this
relaxation; (1) has not been proved for that broader model.

## 3. Focused verification

The companion checker evaluates bounded directed cycles, self-parent
graphs, and mixed root/cycle graphs. It simulates original Boolean queries
with multiple activation tuples on explicit product states. It checks
actual answers, that every full simulation transcript induces a Cartesian
posterior, that each paid equality's conditional hit probability is at
most one half, and that mean paid cost is at most \(2D\). This is a finite
simulation audit, not an exact optimum search or a generalization beyond
the stated common-parent-set model.

The run passes 118 query-simulation cases, 2,256 hypothesis simulations,
1,389 exact Cartesian-posterior checks, and 261 conditional equality-hit
checks. The largest mean paid cost is \(9/4\), illustrating why aliases
cannot simply be given the private-query bound of two. The appropriate
\(2D\) bound holds in every case.

## 4. Charging activation improves the factors to two and D+P

The stronger recurrence charges \(c_i\ge1\) whenever closure newly reveals
an unknown coordinate \(i\). Coordinates already made singleton by either
outcome of a paid equality are not charged. Initial roots are charged if
they are initially unknown. Let \(V\) be the optimum count-DP objective
including paid equalities and these activation charges. A physical
realization has cost at most \(V\), because every activation has a supplied
code of width at most its charge. This remains true on a partially searched
candidate set; a full enabled code still separates that subset.

The same simulation admits a pathwise bound. Within one activation term,
every paid check after its first has an immediately preceding positive
paid check. These predecessors are distinct. The first paid check of each
term is charged to one baseline for that original query; there are at most
\(D\) terms. Ordinary equality queries need one baseline as well. Therefore,
for an entire simulated original root-to-leaf path of depth \(t\),
\[
 W_{\rm paid}\le Dt+N_+,
\]
where \(N_+\) is the number of positive paid checks. Each such check starts
with at least two candidates and permanently identifies a different
coordinate. That coordinate never incurs a free-activation charge. Thus
\[
 \begin{aligned}
 W_{\rm paid}+\sum_{i\text{ freely activated}}c_i
 &\le Dt+N_++\sum_i c_i-\sum_{i\text{ positive paid}}c_i\\
 &\le Dt+\sum_i c_i.
 \end{aligned}
\]
Negative answers leaving one candidate can only save further charges.
Taking expectations and minimizing the charged count recurrence yields
\[
 V\le D\operatorname{OPT}+\sum_i c_i.                         \tag{4}
\]
Unlike the initial comparison, this inequality does not need a half-hit
probability argument. Uniform independent factors are still essential to
the polynomial count-state optimization and its physical realization.

Consequently the private full-cube class has a **2-approximation**.
The alias class of Section 2 has a **\(D+P\)-approximation** with enabled
union widths \(c_i\le Pb_i\), or **\(D+1\)** if a complete owner palette is
provided. For unequal alphabets the exact expression is
\(D+\sum_i c_i/\sum_i\log_2M_i\). The constant-K/general-instance problem
is not solved by these binary structured-class bounds.

Immediate charged closure is valid even when the certified \(c_i\) exceeds
the cheapest residual decoding cost: it overestimates the actual physical
work, and the comparison above already allows charging every coordinate
once. The charged closure depends only on counts and the graph. Adding its
integer cost to the recurrence therefore keeps the same \(n\) states,
acyclic ordering, and polynomial exact arithmetic.

The checker additionally verifies the predecessor inequality, distinctness
of positive-check coordinates, their disjointness from freely revealed
coordinates, and the pathwise charged comparison on all 2,256 simulated
hypotheses. These finite checks audit the alias charging algebra; the
separate dependency-graph checker reconstructs the charged private codes.
