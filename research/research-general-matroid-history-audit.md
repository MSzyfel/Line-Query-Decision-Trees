# Independent audit of discovered matroids and signed history potentials

Auxiliary review, 19 October 2026. This reviews
`research-general-matroid-discovery.md` and
`research-general-history-potential.md`; it does not change those files or
the article. No material proof or runtime issue was found.

The hyperplane-family test is the dual circuit-elimination axiom applied
to complements, with the proper antichain and nonempty-complement
conditions. Requiring empty closure of the empty set gives looplessness.
The closure-intersection and greedy rank operations are consequently
valid. If the supplied query matrix separates points and every query has
a flat response, parallel points are impossible. For any actual live
state, a proper positive successor strictly decreases its rank: equality
would put the entire parent in the closure of its positive successor,
which is contained in the queried flat. This contradicts a nonempty
negative successor. No assumption about preceding negative history is
needed. The cardinality-class candidate menu and the explicit-family
axiom checks have polynomial size and runtime; exhaustive state checks in
the accompanying validation are not part of discovery.

The shared-resource potential is also valid. A query constant on a
resource's whole support has zero potential deficit. Every other local
deficit is at most the live population in that support. Multiplying these
inequalities by nonnegative weights and using the per-hypothesis,
per-query capacities proves the global Bellman inequality, even when
some local deficits are negative. The root resource LP is correctly
identified as the earlier activation ledger; automatic discovery and
the signed, statewise executable potential are the additional content.
The axis-fiber product construction charges each query on exactly its own
axis fiber through each hypothesis, so unit fiber weights are feasible.
The note correctly warns that extra non-coordinate queries can invalidate
that assignment and that nontrivial diagonal states can have zero
potential.

The sharper contraction needs no superadditivity. Restrict one global
optimal code to every member of a disjoint terminal partition. Summing
its restriction costs gives at most its original cost, hence the sum of
the terminal Bellman potentials is at most the global optimum. For
nonnegative terminal values \(f,p\) and \(0\le\gamma<1\),
\[
 \min(f,\alpha p)-\gamma f\le(1-\gamma)\alpha p.
\]
Applying this after the exact signed telescope gives precisely
\[
 F_{\rm new}\le\gamma F_T+
 \max\{a,(1-\gamma)\alpha\}\,F^*.
\]
The choice \(a=(1-\gamma)\alpha\) therefore contracts toward \(\alpha\).
The note retains all signed increments and fixes both the reference code
and potential throughout a pass. Its general coverage premise remains
unproved and is explicitly separated from the conditional contraction;
neither the discovery procedure nor this audit supplies an unrestricted
approximation ratio.

The separate `research-general-matroid-algorithm.md` supplies an exact
polynomial algorithm for complete uniform-matroid hyperplane/all-flat
classes and a rank-only certificate obstruction. The obstruction is
repaired by a basic minority-cap resource and therefore does not refute
combined rank and search certificates.

The subsequently added constant-response extension also checks out. When
all but at most one response cell are flats, every nondefault child of a
proper actual split has strictly smaller rank. The possible exceptional
default child preserves the weak rank bound. Flat responses cannot split
parallel elements, and their complement cannot either, so identification
still implies simplicity. The abstract recurrence correctly allows an
empty default child only when at least two nondefault children are
nonempty. Tracking that count truncated at two in the min-plus convolution
is sufficient; the increasing-size default recurrence is acyclic and uses
\(O(Krn^2)\) arithmetic operations. Monotonicity in the budget supplies the
same statewise Bellman inequality. Requiring only one flat response would
not suffice for \(K>2\), as the root note correctly states. The extension is
a certificate theorem; the executable palette implementation remains
binary.
