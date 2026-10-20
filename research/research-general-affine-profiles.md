# Full laminar profiles still have the affine gap

Auxiliary research note, 19 October 2026. No article or earlier stable
scripts were edited. This settles the previously open quality question for
the full arbitrary count-profile cone on the natural coordinate-equality
hierarchy. The conclusion is an analytic integrality gap, not a new
decision-tree approximation.

## 1. Statement

Let \(H=\mathbb F_Q^d\), \(n=Q^d\), with all affine-hyperplane membership
tests. Fix the natural identifying hierarchy \(T\): determine coordinates
in order \(x_1,\ldots,x_d\), using sequential value-equality tests inside
each coordinate. The equality order within a coordinate may vary from one
already identified prefix to another.

For every internal hierarchy node \(v\), let \(H_v\) be its cluster and
choose an arbitrary profile \(g_v\) with \(g_v(0)=g_v(1)=0\). In the intended
LP the profile values are nonnegative, but the upper bound below does not
need this sign restriction. Write
\[
 P(S)=\sum_v g_v(|S\cap H_v|).
\]
Assume all original-test Bellman capacities hold:
\[
 P(S)-P(S\cap\tau)-P(S\setminus\tau)\le |S|
 \qquad\text{for every }S\subseteq H\text{ and supplied }\tau.       \tag{1}
\]
Individual node deficits may be positive or negative.

Let
\[
 L_{\rm sing}(Q)=Q(Q+1)/2-1
\]
be the optimal raw cost of uniform sequential singleton search, and let
\[
 L_2(0)=L_2(1)=0,\qquad
 L_2(s)=s(\lceil\log_2s\rceil+1)-2^{\lceil\log_2s\rceil}
\]
be the unrestricted optimal binary coding cost.

**Theorem.** Every such feasible profile potential satisfies
\[
 P(H)\le \frac nQ L_{\rm sing}(Q)+Q L_2(n/Q)
       =O(nQ+n\log n).                                    \tag{2}
\]
The same bound holds after adding arbitrary same-hierarchy weighted
restriction-cost features
\[
 \sum_v\gamma_v\,|S\cap H_v|\,
 \mathbf1[S\cap H_{v0}\ne\varnothing,\ S\cap H_{v1}\ne\varnothing].
                                                               \tag{3}
\]
In particular, it holds for the combined nonnegative LP previously
audited. The proof does not require signs on the \(\gamma_v\) either.

The existing [affine lower bound](uniform-decision-tree-lower-bounds.md),
Sections 10–11, gives \(F^*(H)=\Theta(nQd)\). For the established parameter
choice \(d=\lfloor Q/\ln Q\rfloor\), one has
\(\log n=\Theta(Q)\) and
\(d=\Theta(\log n/\log\log n)\). Thus (2) proves the **full target-order
gap** for the arbitrary natural-hierarchy profile cone, including (3).

**Elementary corollary.** The same full-order gap already occurs if the
test family consists only of the \(dQ\) coordinate-equality queries.
The upper certificate uses no other affine queries. This instance is the
direct product of \(d\) independent uniform \(Q\)-symbol singleton-search
problems, so [product additivity](research-general-product-decomposition.md)
gives the exact optimum
\[
 F^*_{\rm coordinate}(H)=d\,\frac nQ\,L_{\rm sing}(Q).
\]
One can also prove this directly: condition on all coordinates except one,
lower-bound the retained queries by its singleton-search optimum, and sum
the disjoint query types. Sequential coordinate search attains equality.
Thus the gap has an elementary exact-OPT witness as well as the richer
all-affine test witness.

## 2. Graph transversals are invisible to the hierarchy

Put \(X=\mathbb F_Q^{d-1}\), of size \(N=n/Q\). For any \(D\subseteq X\)
and function \(f:D\to\mathbb F_Q\), define its graph transversal
\[
 G_f(D)=\{(x,f(x)):x\in D\}.
\]

Every hierarchy node querying a coordinate before the last is a union of
whole last-coordinate fibers \(\{x\}\times\mathbb F_Q\). Its selected
population on \(G_f(D)\) therefore depends only on \(D\), not on \(f\).
Every node querying the last coordinate lies inside a single such fiber,
so it has at most one selected graph point and its profile contribution
vanishes by \(g_v(0)=g_v(1)=0\).

Consequently
\[
 P(G_f(D))=p(D):=P(D\times\{0\})                            \tag{4}
\]
for **every** function \(f\), even nonlinear functions.
This is a functional identity, not a comparison of average profiles.

For (3), nodes before the last coordinate have both child clusters made of
whole fibers, so their populations and child-presence flags depend only on
\(D\). Last-coordinate nodes contain at most one selected point, so their
child-presence products vanish. Hence (4) holds for the combined features
as well.

## 3. One supplied query simulates every split of the quotient

Take any \(B\subseteq D\). Choose \(f(x)=0\) for \(x\in B\), and \(f(x)=1\)
for \(x\in D\setminus B\). Query the original coordinate hyperplane
\(\tau=\mathbf1[x_d=0]\). Its two graph outcomes are
\(B\times\{0\}\) and \((D\setminus B)\times\{1\}\).
Using (4), capacity (1) becomes
\[
 p(D)-p(B)-p(D\setminus B)\le |D|.                         \tag{5}
\]
The key point is that \(B\) is completely arbitrary.

Thus \(p\) obeys the Bellman inequalities for **all unrestricted binary
partitions** of \(X\). Its singleton values are zero. Sum (5) down an
optimal unrestricted binary code on any \(D\); all internal potential
values telescope, giving
\[
 p(D)\le L_2(|D|),\qquad p(X)\le L_2(N).                   \tag{6}
\]

There is no claim that an unrestricted quotient split is a legal query on
the original constant fiber. Each inequality is obtained on a different
graph subset, whose profile values happen to be identical. Precisely this
inability to distinguish histories creates the relaxation's gap.

## 4. Lift the quotient upper bound back to the root

Run the actual equality-search spine for \(x_d\), leaving its \(Q\)
coordinate fibers unfinished. The raw work is \(N L_{\rm sing}(Q)\).
Telescoping its original capacities gives
\[
 P(H)\le N L_{\rm sing}(Q)
          +\sum_{b\in\mathbb F_Q}P(X\times\{b\}).
\]
Every summand equals \(p(X)\) by (4). Apply (6) to obtain (2).
No lower-level profile deficit has been dropped or assumed nonnegative.

This is also an explicit polynomial-support LP dual certificate. Choose a
balanced unrestricted binary tree on the \(N\) quotient labels. Include one
capacity on the corresponding zero/one graph subset for each of its
\(N-1\) internal splits, with weight \(Q\). Include the \(Q-1\) actual
last-coordinate search capacities, with weight one. Their weighted left
sides equal \(P(H)\) identically for every profile vector and every
restriction-feature vector. Their total right side is exactly
\[
 N L_{\rm sing}(Q)+Q L_2(N).
\]
There are at most \(N+Q-2\) nonzero capacities. No numerical LP optimization,
ellipsoid implementation, or sign cancellation heuristic is used.

## 5. Scope

The proof applies to any fixed coordinate order and any ordered linear
change of coordinates: use its last linear coordinate for the graph
construction. It permits arbitrary profiles at every individual node,
arbitrary overlap through ancestors, nonmonotone profiles, and negative
node deficits.

It does not establish a common bound for a jointly optimized sum of
features from arbitrary crossing hierarchies. Such a sum need not have
graph-transversal invariance, and the earlier one-hierarchy polynomial
separator does not automatically extend to it. It also does not rule out
history-aware capacity resources; the root's saturated-capacity certificate
already captures \(\Theta(nQd)\) using the actual positive-answer history.

The natural hierarchy is itself an optimal-order affine code, yet its full
polynomially separable count-profile potential cone loses the entire target
factor. A stronger code-or-certificate theorem cannot rely on that cone
alone, even when supplied this particularly favorable hierarchy.

## 6. Exact finite audit

The companion script constructs the hierarchy and the sparse dual
certificate, without solving a numerical LP. It compares coefficients for
**every** free profile value and every weighted restriction feature:
the weighted sum of capacities equals the root objective exactly.
It independently checks graph invariance, including nonlinear graph
functions, and verifies the exact total right side.

The dual identity is tested on several \(Q,d\) combinations through
\(n=125\). Small graph families are enumerated only as validation; larger
ones are sampled. The theorem and certificate construction are polynomial
and do not enumerate graph functions.
