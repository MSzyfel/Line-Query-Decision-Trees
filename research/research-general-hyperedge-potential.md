# Nonnegative containment potentials: polynomial separation and a full gap

Auxiliary research note, 18 October 2026. The article is unchanged.
This note gives an analytic obstruction for an entire unbounded-support
cone, and a positive comparison for adding root entropy. It does not prove
an unrestricted decision-tree approximation.

Assume \(n\ge2\), an explicit identifying binary test family, and uniform
probabilities with unit query costs.

## 1. Explicit and implicit containment families

For a supplied family of supports \(A\subseteq H\), \(|A|\ge2\), let
\[
 P_w(S)=\sum_Aw_A\mathbf1[A\subseteq S],\qquad w_A\ge0.
\]
For a binary test \(\tau\), write \(A\pitchfork\tau\) when both responses
occur on \(A\). The Bellman deficit is exactly
\[
 D_w(S,\tau)=\sum_{A\pitchfork\tau,\ A\subseteq S}w_A.          \tag{1}
\]
It is nonnegative and supermodular as a function of \(S\).

To separate \(D_w(S,\tau)\le |S|\), make one reward node of weight \(w_A\)
for each cut support, and one cost-one node for each hypothesis. Selecting
a reward node implies selecting every vertex of its support. Maximum
closure, equivalently an \(s,t\) minimum cut, maximizes
\(D_w(S,\tau)-|S|\). Replacing vertex cost one by a rational price
\(\lambda\) gives the corresponding density comparison. This is polynomial
in the explicitly encoded support family, even for large supports and
arbitrary overlaps. It is not a polynomial-size representation of an
arbitrary list of \(2^n\) separate weights.

An implicit polynomial representation is also possible. On polynomially
many possibly overlapping supports \(C\), take
\[
 g_C(s)=\sum_{k=2}^{|C|}a_{C,k}\binom{s}{k},\qquad a_{C,k}\ge0.
\]
Each term is the sum of containment indicators of all \(k\)-subsets of
\(C\), so its deficit is supermodular. Its value is computable from the
selected red and blue counts using binomial coefficients. Therefore
minimizing \(|S|-D(S,\tau)\) is a polynomial value-oracle submodular
minimization problem, even when the supports overlap. A primary SFM
reference is [Iwata, Fleischer, and Fujishige](https://arxiv.org/abs/math/0004089).
The integer binomial coefficients have \(O(n)\) bits, so evaluation has
polynomial bit complexity.

This conclusion requires the nonnegative binomial expansion. Arbitrary
nonnegative count profiles do not have this property.
Coordinate bounds are polynomial: an explicit weight satisfies
\(w_A\le |A|\) by considering \(S=A\) and any test cutting \(A\).
For an implicit coefficient, choose a \(k\)-subset of its support and use
\(P(S)\le F^*(S)\le k(k-1)\), giving \(a_{C,k}\le k(k-1)\).
Thus the polynomial-dimensional containment LP has harmless polynomial-bit
bounds as well as a polynomial separation oracle.

## 2. All support sizes still have the full affine gap

Take \(H=\mathbb F_Q^d\), \(n=Q^d\), and all distinct affine-hyperplane
membership tests. As established in the existing
[lower-bounds note, Sections 10–11](uniform-decision-tree-lower-bounds.md),
\[
 F^*(H)=\Theta(nQd).
\]
There are
\[
 M=\frac{Q(n-1)}{Q-1}
\]
distinct tests, and every distinct pair is separated by exactly
\[
 R=\frac{2n}{Q}
\]
of them. To verify the latter count, use one normal per nonzero scalar
class. Of the \((n-1)/(Q-1)\) normal directions, \(n/Q\) are not orthogonal
to the pair difference. Exactly two offsets in each such direction
separate the pair.

Every support \(A\) of size at least two contains a pair. Thus it is cut
by at least \(R\) tests, regardless of its size or overlap with other
supports. Sum only the full-root capacity inequalities:
\[
 \sum_{\tau}D_w(H,\tau)\le nM.
\]
Equation (1) and nonnegative weights give
\[
 R\sum_Aw_A\le nM,\qquad
 P_w(H)\le \frac{nM}{R}
       =\frac{Q^2(n-1)}{2(Q-1)}=O(nQ).                     \tag{2}
\]

**Theorem.** The nonnegative containment cone, allowing all support sizes
and even all supports simultaneously, has an
\(\Omega(d)\) lower-bound gap on this family. In particular, with
\(d=\lfloor Q/\ln Q\rfloor\),
\[
 d=\Theta(\log n/\log\log n).
\]
Every polynomial explicit or implicit subfamily described above inherits
the obstruction. This argument is stronger in support width than the
earlier fixed-width restriction-credit obstruction.

No constant-factor domination of the containment cone by pair potentials
is proved here. The theorem rules out this cone as a sufficient lower
certificate for the target approximation, independently of that question.

## 3. Adding a root entropy profile

Consider the combined cone
\[
 P(S)=\beta |S|\log_2|S|+P_w(S),\qquad \beta,w_A\ge0,
\]
with \(0\log 0=0\). Entropy deficit is
\[
 D_E(S,\tau)=|S|\,h_2(|S\cap\tau|/|S|),
 \qquad 0\le D_E(S,\tau)\le |S|.
\]

The scaling matters: independently valid components cannot simply be
added and remain valid. Nevertheless any **valid combined** potential
has the following two properties:

1. Its containment component is independently valid, because the entropy
   deficits are nonnegative.
2. \(\beta\le1\), because a two-point set split by a supplied test has
   entropy deficit two and containment deficit nonnegative.

Let \(B_{\rm cont}\) be the best value of the specified containment cone.
The best combined root value satisfies
\[
 B_{\rm combined}\le B_{\rm cont}+n\log_2n.                 \tag{3}
\]
Both individual potentials are allowed combined-cone choices, so
\[
 \max(B_{\rm cont},n\log_2n)
 \le B_{\rm combined}
 \le2\max(B_{\rm cont},n\log_2n).                           \tag{4}
\]
Thus optimizing the two components separately and selecting the better
gives the mathematical factor-two comparison for the combined cone's root
objective. With polynomial-precision evaluation of the entropy constant,
this gives a polynomial-time factor \(2+\epsilon\) algorithm for every
fixed positive \(\epsilon\).
This is a cone-optimization statement, not a factor-two approximation to
the decision-tree problem. Containment optimization is polynomial by its
separation oracle for polynomial-dimensional libraries. The fixed entropy
constant can be evaluated to any required polynomial precision; the
binomial/cardinality bounds and the asymptotic conclusion do not rely on
numerical optimization with logarithms.

For the affine family, (2) and (3) give
\[
 B_{\rm combined}\le n\log_2n+
                   \frac{Q^2(n-1)}{2(Q-1)}.
\]
With \(d=\lfloor Q/\ln Q\rfloor\), one has \(\log_2n=\Theta(Q)\).
Therefore the combined cone still has value \(O(nQ)\) versus true cost
\(\Theta(nQd)\). The full target-order gap survives addition of root
entropy.

### Exact integer coding-profile variant

Replace root entropy by the unrestricted optimal binary coding cost
\[
 L_2(0)=L_2(1)=0,\qquad
 L_2(s)=s(\lceil\log_2s\rceil+1)-2^{\lceil\log_2s\rceil}
 \quad(s\ge2).
\]
This integer profile satisfies, for \(s=a+b\),
\[
 0\le L_2(s)-L_2(a)-L_2(b)\le s.                            \tag{6}
\]
For the lower inequality, restrict an optimal unrestricted code on \(s\)
labels to each label set and suppress constant queries. The two restricted
costs sum to at most the original cost, and are at least their unrestricted
optima. For the upper inequality, query the partition first and append
optimal child codes; if a side is empty the deficit is zero. A split pair
has deficit \(L_2(2)=2\).

Consequently the component-sandwich and two-witness arguments transfer to
\(P(S)=\beta L_2(|S|)+P_w(S)\). In this **modified cone** all coefficients
are rational. Its optimum \(B_{{\rm combined},2}\) satisfies
\[
 \max(B_{\rm cont},L_2(n))
 \le B_{{\rm combined},2}
 \le2\max(B_{\rm cont},L_2(n)).
\]
Exact rational component optimization and comparison therefore give a
polynomial-time factor-two approximation to this modified cone's root
objective. The capacity-ratio witness comparison is also an exact
factor-two statement implementable in rational arithmetic. This does not
assert an exact factor-two implementation for the entropy cone.

Finally \(L_2(n)\le n\lceil\log_2n\rceil\le n\log_2n+n\), so the same
affine-family full-order gap survives.

## 4. A factor-two capacity-ratio witness

For one nonconstant test and fixed nonnegative coefficients, let
\[
 c=\max_{\varnothing\ne S\subseteq H}D_w(S,\tau)/|S|,
 \quad
 \nu=\max_{\varnothing\ne S\subseteq H}
        [D_w(S,\tau)+\beta D_E(S,\tau)]/|S|.
\]
Since \(D_E(S,\tau)\le |S|\), one has \(\nu\le c+\beta\).
A containment-density maximizing witness has combined density at least
\(c\). A pair with opposite test responses has combined density at least
\(\beta\). The better actual witness consequently has density at least
\[
 \max(c,\beta)\ge\nu/2.                                   \tag{5}
\]
Constant tests have zero deficit and can be ignored.

Containment density is polynomially computable by threshold-price closure
and rational binary search. To make the bit-complexity argument explicit,
let \(D\) be a common denominator of all input weights. Every candidate
density is an integer divided by \(D|S|\); two distinct densities differ
by at least \(1/(Dn^2)\). Binary search to a smaller interval isolates an
exact optimum and a maximizing witness. The bit length of \(D\) is at most
the sum of the input denominator bit lengths. For implicit binomial
profiles the same argument applies, using SFM for threshold comparisons.

Equation (5) is an approximation to maximum **capacity ratio**. A witness
ratio above one is a genuine violated constraint; failure to find such a
witness only guarantees that the true maximum is at most two. It is not
an exact feasible/infeasible separation oracle. Logarithmic evaluations can
be handled with certified numerical intervals, giving a factor \(2+\epsilon\)
implementation for any fixed positive \(\epsilon\). The exact component
optimization comparison (4) avoids needing this approximate oracle.

## 5. Finite audit

The companion checker implements rational maximum closure using a finite
mincut network and exact rational density search. It checks closure
values and density witnesses against exhaustive subsets on small random
hypergraphs. It also checks the two-witness inequality for root entropy,
with a small floating tolerance only in that numerical entropy check.

Separate affine checks enumerate all supports through nine points and
sample larger supports, confirming the exact test and pair-separation
counts and the cut-count domination used in (2). The asymptotic gap is
proved above, not inferred from numerical ratios.
The checker also verifies (6) for every split through size 64 and audits
the coding-profile two-witness comparison with exact rational arithmetic.
