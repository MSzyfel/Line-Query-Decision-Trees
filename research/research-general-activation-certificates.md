# Complete activation witnesses and a polynomial certificate compiler

Auxiliary research note, 19 October 2026. The article is unchanged.

**New result.** The charged count-DP theorem extends from one parent set per
coordinate to an arbitrary explicit OR-hypergraph of sufficient activation
sets. A query can combine terms from different such sets and even different
targets. A conservative polynomial compiler discovers these witnesses and
exact constant-size query covers from an explicit full Cartesian response
factorization. It gives
\[
 F_{\rm ALG}/n\le d_0\operatorname{OPT}_{\rm mean}+\sum_i c_i,
\]
where \(d_0\) is a fixed query-cover width and \(c_i\) are certified enabled
code heights. Thus \(c_i\le q\log_2M_i\) implies factor \(d_0+q\).
This is a new certified subclass theorem. It does not give a universal
\(o(\log n/\log\log n)\) ratio; the Cartesian and sparse-cover conditions
are substantial and are verified rather than assumed on rejection.

## 1. A complete witness is stronger than one useful context

Suppose \(H=\prod_{i=1}^d[M_i]\), with \(M_i\ge2\), uniform hypotheses,
and all pure factor-value equality tests available as original questions,
possibly complemented. Hence \(\prod_iM_i=n\) and \(d\le\log_2n\).
Fix integers \(1\le c_i\le M_i-1\).

An activation witness for target \(i\) is a set
\(W\subseteq[d]\setminus\{i\}\) with the following complete certificate:
for **every** value assignment \(a\in\prod_{p\in W}[M_p]\), supply an
actual original-test code \(B_{i,W,a}\) of height at most \(c_i\) which
identifies \(X_i\) on
\(C(W,a)=\{X_W=a\}\). Every query in this code must depend only on
\(X_i\) on that entire context, so it leaves all other unknown factors
unconditioned. The code can use different original questions and different
local labels at different assignments.

Completeness over all assignments is crucial. It makes eligibility depend
only on the set of known factors, rather than on their values. One cheap
code on one exceptional context is not an activation witness in this sense.
Let \(\mathcal W_i\) be any explicit family of such witnesses. Coordinate
\(i\) can be revealed at charge \(c_i\) as soon as any member of
\(\mathcal W_i\) is entirely known. These OR rules can contain cycles,
overlap arbitrarily, and have many alternatives per coordinate.

## 2. Sparse query covers by activation terms

An activation term has the form
\[
 [X_W=a]\,[X_i\in A],\qquad W\in\mathcal W_i,
\]
where \(A\) is any target-value subset. A nonconstant original binary
question is certified if either it is a pure coordinate equality, or one
of its response cells is the union of at most \(d_0\) such terms.
Terms can overlap and can have different targets and different witnesses.
The union must equal the response cell on **every original hypothesis**.

This strictly removes the common-parent-set restriction of the earlier
bounded-alias theorem. For example one target may have complete fast codes
when either factor 1 or factor 2 is known. Different physical questions,
or two alternatives in one physical question, may use these different
witnesses. It is not enough that the matching context happens to determine
one local bit: matching its witness must enable a complete target code.

## 3. The same n-state charged DP works

The state is a vector of remaining candidate counts \(r_i\). Closure sets
\(r_i=1\) and charges \(c_i\) whenever \(r_i>1\) and some witness
\(W\in\mathcal W_i\) has all its counts one. Repeat until stable. The final
known set and total charges do not depend on closure order. The possible
count vectors still number exactly \(\prod_iM_i=n\).

At a closed nonterminal state choose a paid equality on coordinate \(i\):
pay one; the hit child has \(r_i=1\) with probability \(1/r_i\), and the miss
child has \(r_i-1\) with probability \(1-1/r_i\). Apply charged closure to
either child. Each action reduces the sum of counts. The exact rational
DP therefore has polynomial runtime in \(n\) and the explicit witness
family. Its raw conditional costs are integers after multiplication by
\(\prod_i r_i\), so their bit complexity is polynomial as well.

Execute the policy with actual factor-value equalities. For a charged
activation, choose any currently known witness \(W\), observe its actual
assignment \(a\), and replay the supplied code \(B_{i,W,a}\), restricted
to the target's remaining values. Its height remains at most \(c_i\).
Extra known factors do not invalidate a code that was factor-local on
the larger context. The physical posterior remains a product throughout.
Consequently the physical mean cost is at most the charged DP value \(V\).

To compare with an unrestricted original-test tree \(T\), simulate each
certified term by checking its still-unknown \(W\) values with ordinary
equalities. A mismatch makes the term false. If all match, witness \(W\)
enables target \(i\); its freely revealed value evaluates \([X_i\in A]\).
An OR of at most \(d_0\) terms computes the certified response; complement
the result if that was the physical-zero response. All original answers
are entailed by the simulator's stronger rectangular history.

On one path of \(T\) with depth \(t\), the first paid check of each term
uses one baseline, at most \(d_0t\). Every further paid check has a distinct
immediately preceding positive paid check. A positive check permanently
identifies its coordinate, which will never incur an activation charge.
For \(c_i\ge1\), the same cancellation as in the graph proof gives
\[
 W_{\rm paid}+\sum_{i\text{ activated}}c_i
 \le d_0t+\sum_i c_i.
\]
Taking expectations and minimizing proves
\[
 \operatorname{ALG}_{\rm mean}\le V
 \le d_0\operatorname{OPT}_{\rm mean}+\sum_i c_i.             \tag{1}
\]
Binary information supplies \(\operatorname{OPT}_{\rm mean}\ge\log_2n\).
This gives factor \(d_0+\sum_i c_i/\log_2n\), including \(d_0+q\) under
the displayed height promise. No assumption about disjoint query terms,
adaptive submodularity, or greedy source quality is used in the comparison.

## 4. Discovering a polynomial sufficient witness family

The following uses only the response matrix and a verified full Cartesian
factorization. Such factorizations can be tried from the polynomial
global-minority filter family in `research-general-factor-contexts.py`.
Require the retained quotient to identify all \(n\) hypotheses and check
that each factor-value equality is an original question or its complement.
Otherwise this compiler makes no claim for that factorization.

For every target \(i\), every subset \(W\) of other factors, and every
assignment \(a\) to \(W\), scan the original queries. Keep the ones which
are constant on each target-value fiber inside \(C(W,a)\); these are actual
factor-local tests there. Run ordinary greedy on the \(M_i\) values using
only these questions. All factor equalities are available, so this code
always identifies the target and has height at most \(M_i-1\). Store its
actual rows and height. Let \(h_i(W)\) be the maximum of these heights over
all assignments to \(W\). Retain \(W\) for target \(i\) when
\(h_i(W)\le c_i\).

There are only
\[
 \sum_{W\subseteq[d]}\prod_{p\in W}M_p
 =\prod_p(1+M_p)\le n^{\log_2 3}
\]
known-factor contexts. The inequality follows from
\(1+x\le x^{\log_2 3}\) for \(x\ge2\). Multiplying by the at most
\(d\) target choices keeps this polynomial. All locality and code checks
are finite matrix operations. This procedure is conservative: it certifies
the height of the constructed greedy code, not the unknown minimum height.

It can also try **all** charge vectors, since
\[
 \#\{c:1\le c_i\le M_i-1\}=\prod_i(M_i-1)\le n.
\]
Store the code-height table once; qualification under any charge vector
is then immediate. Thus no exponent depends on a height or rank parameter.

## 5. Exact fixed-width query-cover discovery

Fix the cover width \(d_0\) once, for example \(d_0=1\) or \(2\).
For every retained witness/context/target triple and desired response cell
\(Q\), compute
\[
 A=\{v:C(W,a)\cap\{X_i=v\}\subseteq Q\}.
\]
Its cylinder term is the largest target subset for that fixed witness and
context which is contained in \(Q\). Discard empty terms. There are
polynomially many candidate terms. If any cover of \(Q\) by at most
\(d_0\) activation terms exists using the retained witnesses, replacing
each term by this maximal one preserves containment in \(Q\) and preserves
coverage. Therefore enumerating all at-most-\(d_0\) tuples of these
candidate terms finds a cover whenever one exists. Try both response cells.

For a fixed \(d_0\), this is polynomial with a fixed exponent. Letting
\(d_0\) grow with \(n\) would not be polynomial and is not part of the
proposal. Every original nonconstant query must pass, including unused
noise questions that the unrestricted optimum could exploit. Otherwise
reject its sparse-cover comparison certificate. A successful vector supplies the complete
certificate of Sections 1-3 and an executable code. Keep the cheapest code
over all successful charge vectors and factorizations, together with the
initial incumbent.

The witness-based charged program itself is an executable upper bound even
when a query fails the sparse-cover check. Such a code can still be kept
in the portfolio. What fails is inequality (1) against an unrestricted
optimum, because that optimum may use the uncovered query. Independently,
its actual raw cost divided by the integer unrestricted coding bound
\(L_2(n)\) is a valid a posteriori approximation certificate. In particular,
if empty witnesses already give a cheap complete global code, no sparse
query-cover proof is needed to use that code and information bound.

Thus if the table-constructed local codes admit some vector with small
\(\sum_i c_i\) and constant-width covers for all original questions, this
raw-matrix portfolio finds a code satisfying (1). The procedure need not
be given the graph, witness family, term covers, or code labels. Its
potentially large fixed exponent is a practical limitation; no efficient
unrestricted implementation or asymptotic improvement is asserted.

The companion prototype implements the local-code table, complete-witness
verification, exact width-one/two query covers, charged OR-closure DP,
physical reconstruction, and the full charge-vector portfolio for a
supplied Cartesian labeling. It does not repeat the outer root-threshold
factorization enumeration. Its deterministic \(n=64,m=45\) instance has
75 compiled local-context codes and 12 target/witness pairs. One target
has the distinct sufficient witnesses \(\{0\}\) and \(\{1\}\). An extra
physical question needs two terms: width one rejects and width two accepts.
All 27 charge vectors are tested, 18 qualify, and every produced code is
executed on every hypothesis. At charges \((2,2,2)\), the program visits
55 count states and produces raw cost 400, equal to its charged mean
\(25/4\) times 64. Complemented physical questions are included. There is
no unrestricted optimum oracle or random search.

## 6. Where the universal problem remains

The complete-witness condition is what permits polynomial count states.
If a code is cheap only at a few special assignments of \(W\), whether it
activates depends on actual known values. A state containing only counts
then loses information. The existing polynomial full-factor context pool
records known values but does not automatically represent all arbitrary
subsets left by partial equality searches. This note does not solve that
value-dependent activation problem.

Nor can an arbitrary non-Cartesian relation be substituted for the product.
For \(H=\{e_1,\ldots,e_d\}\subset\{0,1\}^d\), there are only \(n=d\)
hypotheses, but the nominal product count space has size \(2^d\). Observing
one positive coordinate fixes every other coordinate, and independent
uniform candidate sets are false. Exact support factorization correctly
treats this one-hot relation as coupled. Cartesian support of a retained
quotient with unequal original multiplicities is also insufficient: its
factor values need not have uniform independent posterior distributions.

For the fixed-width compiler, sparse query covers are a genuine
requirement rather than a formal relabeling of every instance. A coupled
Boolean function can need many activation terms even when its target
codes are cheap; the sparse-cover comparison then rejects. Section 7
replaces this particular requirement by a broader evaluator certificate.
Neither condition is proved universal. A low-charge certificate or an
alternative cheap code for every general instance remains missing.

## 7. Broader oracle-evaluator compiler: proved, not implemented

**Status.** This addendum is a theorem-described compiler. The companion
Python file and its saved results implement only the width-one/two
compiler of Sections 4-5. No run of the broader compiler is claimed.
The negative-answer idea comes from
`research-general-predicate-activation.md`; here it is combined with the
automatically verified complete OR-witness families and permits arbitrary
original query functions, mixed witnesses, and mixed targets.

Fix a constant integer \(\kappa\ge1\). For every original question \(q\),
seek an acyclic equality evaluator in the following activation oracle.
It can ask any proper coordinate-value equality. Whenever a complete
witness \(W\in\mathcal W_i\) is known, it may freely reveal the actual
value of \(X_i\). It can stop with response zero or one only when the
original query is constant with that response on its whole current product
cell. Require at most \(\kappa\) negative equality responses on every
path. Positive responses and oracle reveals need not be bounded by
\(\kappa\). Pure coordinate equalities have their direct one-question
evaluator, which is why \(\kappa\ge1\) covers them.

The evaluator need not identify one prescribed full parent tuple. A true
or false exit can follow any combination of known values and exclusions
which actually determines \(q\). A reveal is justified only by a verified
complete witness; a convenient partial parent predicate alone does not
authorize it.

Replay such a fresh-root evaluator inside the stronger simulation of an
arbitrary original tree. Skip equalities already determined by the actual
stronger history, and select the known value at any oracle reveal which
has already occurred. The actual candidate cell always lies inside the
fresh evaluator's abstract candidate cell. An abstract witness known there
is also known in the stronger state, so its reveal is valid. Additional
known factors can only enable more complete witnesses. A terminal response
constant on the fresh cell is therefore correct in the actual cell.
The original response adds no conditioning constraint beyond the saved
equality and reveal history.

On a simulated path of original depth \(t\), there are at most
\(\kappa t\) paid negative equalities. Every paid positive equality fixes
a distinct coordinate and saves that coordinate's later activation charge.
For \(c_i\ge1\), cancellation gives
\[
 W_{\rm paid}+\sum_{i\text{ activated}}c_i
 \le\kappa t+\sum_i c_i.
\]
Thus the same executable **n-state charged DP** satisfies
\[
 \operatorname{ALG}_{\rm mean}
 \le\kappa\operatorname{OPT}_{\rm mean}+\sum_i c_i.           \tag{2}
\]
The factor is \(\kappa+\sum_i c_i/\log_2n\). Activation-term covers give
such an evaluator with \(\kappa\le d_0\), but the evaluator criterion can
accept much more compact Boolean computations than explicit term covers.
The comparison still concerns every original question, including noise.

These evaluators can be synthesized exactly in polynomial time for fixed
\(\kappa\). A fresh evaluator state consists of each already known factor
value, each still-unknown factor's excluded values, and the remaining
negative budget. Across unknown factors there are at most \(\kappa\)
exclusions. Exclusions disappear from the representation when a factor
becomes a singleton, while its actual singleton value is retained. With
\(S=\sum_iM_i\), the number of states is at most
\[
 (\kappa+1)\prod_i(1+M_i)
          \sum_{j=0}^{\kappa}\binom Sj,
\]
which is polynomial for every fixed \(\kappa\).

At a state, first accept if \(q\) is constant on its product cell, as
verified by directly scanning its original response column. If a target is
enabled by a known complete witness, take a free-reveal transition:
**every possible remaining value child must be feasible at the same
negative budget**. This is a universal transition over all values, never
an existential choice of a convenient reveal. Otherwise try proper
equalities. Feasibility requires both the positive child at the same
budget and the negative child with budget reduced by one. At budget zero
no proper paid equality is allowed, but constant exits and free reveals
remain available. Each child strictly decreases the sum of candidate-set
sizes. The recurrence is acyclic, exhaustive, and constructs an explicit
polynomial DAG when feasible. Free-reveal transitions have at most \(n\)
children; the bound above already includes their known-value states.

Performing this synthesis for each original question and each of the at
most \(n\) charge vectors gives a polynomial certificate portfolio at fixed
\(\kappa\). It retains the full Cartesian/equality prerequisites and the
low-total-charge promise. Allowing \(\kappa\) to grow with \(n\) would make
the synthesis exponent grow and is not a polynomial-runtime claim. A
supplied compact evaluator can still be verified independently in its
explicit size, but that is a different input promise.
