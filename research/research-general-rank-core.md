# Polynomial synthesis from a majority core of low literal rank

Research checkpoint, 18 October 2026. This auxiliary note records a positive,
conditional code constructor. It does **not** prove an improved approximation
for unrestricted uniform decision trees. The implementation in the companion
checker uses exhaustive subset enumeration only to validate the theorem on
small inputs; that enumeration is not the proposed polynomial algorithm.

## Statement

There are \(n\ge2\) hypotheses, unit-cost binary tests, and a uniform prior.
All supplied responses are known explicitly and distinguish the hypotheses.
Write

\[
 v_h=(1,\tau_1(h),\ldots,\tau_m(h))\in\mathbb F_2^{m+1},\qquad
 r(C)=\operatorname{rank}_{\mathbb F_2}\{v_h:h\in C\}.
\]

The rank here uses **every supplied response row**. It is a linear-matroid
rank, so it is nonnegative, monotone, integer-valued, and submodular, and can
be evaluated by Gaussian elimination in polynomial time.

**Theorem.** There is a polynomial-time algorithm producing an executable
partial decision tree \(P\) with at least one identified hypothesis such that

\[
 \frac{W(P)}{|C(P)|}\le4r
\]

whenever there exists a set \(C\) with 
\(|C|\ge3n/4\) and \(r(C)\le r\). Here \(W(P)\) is raw work, the sum of the
numbers of hypotheses reaching queried nodes, and \(C(P)\) is the set actually
identified by the partial tree. The constructor does not query membership in
the unknown core.

The algorithm enumerates \(r=1,\ldots,\min(n,m+1)\), constructs one candidate
for each \(r\), and returns the candidate of minimum actual density. Thus it
does not need the witness core or its rank as input. A candidate with no
completed hypothesis is discarded. The last guess, or simply a full legal
tree, ensures a candidate exists.

## Legal codes from a literal-rank core

For a nonempty \(A\), restrict every test row to the columns in \(A\).
Begin a row basis with the all-ones row, then extend it using actual supplied
test rows. Row rank equals column rank, so at most \(r(A)-1\) query rows are
needed. Their response patterns distinguish every pair in \(A\): otherwise
that pair would agree on a basis and hence on every supplied row.

Ask these supplied tests in a fixed order, suppressing queries constant on
the current core cell and stopping once that core cell is a singleton. This
gives a legal binary identifying tree \(B_A\) for \(A\), of height at most

\[
 r(A)-1,\qquad F_{B_A}(A)\le |A|\,[r(A)-1].
\]

The initial constant row is used only for linear algebra; it is not charged
or executed as a query. In particular, \(r(A)=1\) implies \(|A|=1\) because
the supplied tests distinguish hypotheses and every column has first entry
one.

## Lifting without a membership test

Run \(B_A\)'s actual tests on the full hypothesis set. At any reached cell,
let \(c\) be the number of core hypotheses and \(u\) the number outside the
core. Stop unfinished before querying whenever \(u\ge c\). A leaf of the
core code identifies its hypothesis only when no outsider shares that leaf.
An unused core response branch is stopped unfinished.

For each queried node, \(u<c\), so its full-instance work is less than twice
its core work. Hence

\[
 W(P_A)\le2F_{B_A}(A)\le2a[r(A)-1],\qquad a=|A|.
\]

The stopped frontier cells are disjoint. At each such cell, lost core count
is at most outsider count. Thus at most \(n-a\) core hypotheses fail to be
identified, and

\[
 |C(P_A)|\ge a-(n-a)=2a-n.
\]

This is a count argument for the uniform setting. An arbitrarily small
prior mass of outsiders can contaminate a heavy core leaf, so this particular
lost-mass argument is not asserted for arbitrary priors.

## Submodular selection and the factor four

For a rank guess \(r\), put \(\lambda=n/(4r)\). Minimize the unconstrained
submodular function

\[
 f_r(A)=n\,r(A)-4r|A|.
\]

Its minimizers maximize \(|A|-\lambda r(A)\). If the promised witness exists,
its objective is at least

\[
 3n/4-\lambda r=n/2.
\]

Consequently every minimizer \(A\) satisfies

\[
 a-\lambda r(A)\ge n/2.
\]

It is nonempty and \(r(A)\ge1\), giving \(a>n/2\), so the lifted code
completes at least one hypothesis. The two estimates from the previous
section give

\[
 \frac{W(P_A)}{|C(P_A)|}
 \le\frac{2a\,r(A)}{2a-n}
 \le\frac{2a(a-n/2)}{\lambda(2a-n)}
 =\frac a\lambda\le4r.
\]

The cancellation matters: a minimizer need not retain a constant fraction
strictly above \(n/2\). The theorem promises low density, not a constant
number of completions relative to \(n\).

For a rational majority threshold \(\theta>1/2\), the same proof with
\(\lambda=(\theta-1/2)n/r\) gives density at most
\(r/(\theta-1/2)\) from a core of size at least \(\theta n\).

## Runtime and status

Unconstrained submodular minimization has a strongly polynomial value-oracle
algorithm; no cardinality-constrained oracle is used here. A primary reference
is Iwata, Fleischer, and Fujishige, [*A Combinatorial, Strongly Polynomial-Time
Algorithm for Minimizing Submodular Functions*](https://arxiv.org/abs/math/0004089).
The rank oracle is polynomial Gaussian elimination. The objective above is
integral with polynomial bit length, and there are at most \(n\) rank guesses.
Row-basis extraction, construction of a pruned core tree, computation of all
outsider routes, threshold pruning, and comparison of actual densities are
polynomial in the explicit response matrix dimensions. A proper core tree
has at most \(2|A|-1\) nodes, regardless of the chosen basis height.

Thus this is a fixed-exponent polynomial construction using a standard
polynomial SFM subroutine. The companion script deliberately does **not**
implement that general subroutine. It checks its possible minimizers by
exhaustive enumeration on small instances, separately from the runtime proof.

If a three-quarter core has literal rank at most \(cD^*\), where
\(D^*=F^*/n\) is the optimal full-tree mean depth, the constructor yields a
partial code of density at most \(4cD^*\). This is a root partial-code promise,
not an approximation to the unrestricted minimum completion density, and
not by itself a full decision-tree approximation. Iteration or weighted
incumbent-depth pricing would require an additional hereditary or weighted
guarantee.

## Why this is a promise, not a general solution

Let \(n=2^b\), include the \(b\) coordinate-bit queries on
\(\{0,1\}^b\), and also include every singleton query. The coordinate code
has mean depth \(b\), and the information lower bound shows \(D^*=b\).
The singleton rows restricted to any \(C\) contain its identity matrix, so

\[
 r(C)=|C|.
\]

Every three-quarter core therefore has literal rank at least \(3n/4\),
although the optimal tree has depth \(\log_2 n\). This also shows that the
literal-rank promise is brittle under the addition of redundant tests. The
constructor supplies a genuine polynomial code-synthesis primitive on
instances satisfying the promise; no unrestricted asymptotic improvement is
claimed.

## Finite validation

Run `python research-general-rank-core.py`. The checker uses integer
Gaussian elimination, verifies row-basis separation, evaluates every
unconstrained minimizer on small instances, constructs and executes the
actual lifted partial code, checks both lifting inequalities and the factor
four bound, and checks the singleton-augmented coordinate obstruction.
It writes a compact results JSON. Enumeration in this checker is only a
finite validation mechanism.

The structured validation also includes 32 hypotheses with a 24-hypothesis
rank-six core and eight independent outsider columns. At \(\lambda=4/3\),
each outsider decreases the maximized objective, so every optimum excludes
them. The script enumerates all spans generated by the core's six-dimensional
columns and checks the unique optimal core closure. This tests a genuinely
nontrivial SFM selection, rather than only cases whose optimum is the full
hypothesis set.
