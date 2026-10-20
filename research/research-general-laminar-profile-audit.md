# Audit of arbitrary laminar count profiles

Auxiliary research note, 18 October 2026. Root files and the article were
not changed. The audit confirms the polynomial separation argument,
extends it to same-hierarchy weighted restriction features, and gives a
small exact quality gap for both cones.

## 1. Audited profile cone

Fix a proper supplied binary decision-tree hierarchy \(T\), with cluster
\(H_v\) at each internal node. The potential is
\[
 P(S)=\sum_{v\ {\rm internal}}g_v(|S\cap H_v|),
 \qquad g_v(0)=g_v(1)=0,\quad g_v(s)\ge0.
\]
Bellman capacities are
\[
 P(S)-P(S\cap\tau)-P(S\setminus\tau)\le |S|
 \quad\text{for every subset }S\text{ and supplied test }\tau.       \tag{1}
\]
They imply \(P(S)\le F^*(S)\), by telescoping down any identifying tree for
\(S\). Nonnegative profiles and the zero boundary conditions give
nonnegative potentials and zero singleton potentials.

For fixed \(\tau\), color hypotheses by its response. At each hierarchy
node retain the maximum deficit obtainable with each exact pair of red
and blue counts. At a parent, convolve the child tables and add
\[
 g_v(r+b)-g_v(r)-g_v(b).                                    \tag{2}
\]
This quantity may be negative. That does not invalidate the recurrence:
once child counts are fixed, every ancestor contribution is independent
of which child subset attained those counts. Keeping the maximum score
for each count pair is therefore exact. Maximize the final score divided
by \(r+b>0\) to separate (1). A witness subset is reconstructed by keeping
the chosen child masks.

There are \(O(n^2)\) profile variables and \(O(n^2)\) count states per node;
a direct convolution implementation is polynomial, even using the loose
\(O(n^5)\) operation bound. Exact rational operations have polynomial bit
length. The script correctly handles finite masks against Python's
unbounded bitwise complement. A zero singleton score ensures that the
maximum violation ratio is nonnegative even for nonmonotone profiles.

For a fixed response bound \(K\), keep a \(K\)-tuple of counts and add
\(g_v(\sum_a c_a)-\sum_a g_v(c_a)\). The direct complexity is
\(n^{O(K)}\), which is fixed-exponent polynomial when \(K\) is constant.

## 2. Harmless bounds and optimization status

Choose a subset \(S\subseteq H_v\) of size \(s\). Nonnegative features and
(1) imply
\[
 g_v(s)\le P(S)\le F^*(S)\le s(s-1).
\]
Thus the coordinate bounds in the root LP are harmless. They are not
additional assumptions about profile shape. The zero vector is feasible.
An exact rational separation oracle and these polynomial-bit bounds give
a polynomial ellipsoid optimization formulation. This statement does not
claim polynomial runtime for a floating simplex or repeated cutting-plane
implementation.

The root script labels its floating optimizer as finite validation only.
Its final rational profile is scaled by the exact maximum capacity ratio,
then every supplied test is separated exactly. Consequently the reported
number is a valid lower bound regardless of floating optimality, cut-loop
tolerances, or whether an already seen cut is slightly violated. The root
script does not claim a certified LP upper bound.

The audit additionally extracts a floating dual, converts it to
nonnegative rational weights, and repairs any exact dual coordinate
deficit using the corresponding harmless box constraint. If \(A x\le b\)
is the generated cut system and \(c\) is the objective, the repaired vector
satisfies
\[
 y\ge0,\qquad A^\top y\ge c.
\]
Hence \(b^\top y\) is an exact upper bound for the complete profile LP:
its feasible set is contained in that of every generated-cut relaxation.
The explicit primal and sparse dual certificates are saved separately.

## 3. Same-hierarchy weighted restriction features

For each internal hierarchy node \(v\), add
\[
 \gamma_v\,|S\cap H_v|\,
 \mathbf1[S\cap H_{v0}\ne\varnothing,\ S\cap H_{v1}\ne\varnothing],
 \qquad \gamma_v\ge0.                                      \tag{3}
\]
These are the weighted work contributions of the supplied tree restricted
to \(S\), with constant queries suppressed. Given child color counts
\((r_l,b_l),(r_r,b_r)\), add to the DP score
\[
 \gamma_v\big[
 (r+b)\mathbf1[r_l+b_l>0,\ r_r+b_r>0]
 -r\mathbf1[r_l>0,\ r_r>0]
 -b\mathbf1[b_l>0,\ b_r>0]\big].                            \tag{4}
\]
This is exactly the deficit of (3). Its unweighted bracket is nonnegative,
although the profile term (2) need not be. The same fixed-count recurrence
therefore separates the combined cone in polynomial time.

The bounds \(0\le\gamma_v\le1\) are harmless. Take two hypotheses, one from
each child of \(v\). Their restricted-tree feature at \(v\) is \(2\gamma_v\);
other features are nonnegative, and their optimal raw identifying cost is
two. Thus (1) implies \(\gamma_v\le1\).

This extension uses the **same hierarchy** as the profiles. Arbitrarily
combining features from crossing hierarchies is not covered by this DP:
the state would need additional information about overlapping clusters.

## 4. Exact small counterexample

Hypotheses are the bit positions \(0,\ldots,7\), and binary tests are the
following integer masks:

    [4, 10, 86, 92, 190, 212, 214].

On the root implementation's deterministic greedy hierarchy:

| Quantity | Exact value |
|---|---:|
| Greedy full-tree raw cost | 26 |
| Optimal full-tree raw cost | 25 |
| Maximum arbitrary laminar profile potential | 24 |
| Maximum combined profile + restriction potential | 24 |

Both LP values have an exact rational feasible lower certificate and an
exact rational nonnegative dual upper certificate. Thus this is an actual
strict expressiveness gap, rather than a floating optimizer failing to find
a stronger profile. It is a \(25/24\) gap on this fixed hierarchy, not an
asymptotic obstruction and not a claim about every possible hierarchy.

For comparison, tests

    [48, 72, 84, 128, 186, 250]

have greedy cost 27 and optimum 25, and their greedy-hierarchy profile LP
has exact value 25. The relaxation can certify an improvement over its
generating tree, but does not always certify the optimum.

## 5. Analytic baseline and interpretation of the first benchmarks

Every hierarchy contains its root. A root-only cardinality profile already
contains the optimal unrestricted binary count function
\[
 f(s)=s\ell-(2^\ell-s),\qquad \ell=\lceil\log_2 s\rceil
 \quad(s\ge1),\qquad f(0)=0.
\]
For every split \(s=a+b\), a root query followed by the two optimal
unrestricted codes gives \(f(s)\le s+f(a)+f(b)\). Hence this integer profile
is always feasible. It yields the standard information lower bound, with
the exact integer binary-tree correction.

If each test's designated positive side has at most \(k\) hypotheses, the
stronger root-only capacity recurrence
\[
 f_k(0)=f_k(1)=0,\qquad
 f_k(s)=s+\min_{1\le a\le\min(k,s-1)}[f_k(a)+f_k(s-a)]
\]
is feasible by the same split inequality. It is a lower potential, not an
assertion that every minimizing split is supplied.

Consequently the three completed root benchmarks do not yet show an
advantage from laminar features:

* Cube eight: the unrestricted count profile gives 24.
* Singleton tests on eight points: \(f_1(8)=35\).
* Affine \(Q=3,d=2\): each hyperplane has three points, and \(f_3(9)=30\).

All three equal the reported exact optima. The newly certified small
counterexample concerns a setting where the true optimum is above the
unrestricted count baseline. No analytic constant-factor relation between
the full laminar-profile cone and unrestricted optimal trees is established.

## 6. Validation files

The audit script checks 299 exact combined separation cases by exhaustive
subset comparison, encountering 342 negative individual profile terms.
Its bounded quality search examines 438 identifying instances and optimizes
two nonoptimal greedy hierarchies whose optima exceed the unrestricted
count baseline. It saves exact primal/dual intervals and the masks above.
No \(n=27\) process was restarted or counted.

Files:

* research-general-laminar-profile-audit.py
* research-general-laminar-profile-audit-results.json
* research-general-laminar-profile-audit-certificates.json
