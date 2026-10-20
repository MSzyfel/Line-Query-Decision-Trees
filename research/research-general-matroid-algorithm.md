# Complete uniform-matroid query classes: exact codes and a rank limitation

Auxiliary research note, 19 October 2026. No article files were edited.
This gives a polynomial exact algorithm for a complete matroid query class,
and a sharp obstruction to using its discovered rank alone as a general
quality certificate. It is not an unrestricted decision-tree approximation.

## 1. A complete non-affine class with an exact algorithm

In the uniform matroid \(U_{k+1,n}\), \(1\le k<n\), every \(k\)-subset is a
hyperplane. Suppose the supplied binary queries are exactly membership in
all these hyperplanes, allowing redundant copies, complemented descriptions,
and constant queries. The hypotheses and query costs are uniform.

The query family is invariant under every permutation of the hypotheses,
so the optimal continuation cost depends only on the current population
\(s\), with the original \(n,k\) still fixed. A query can have exactly \(a\)
positive hypotheses in a live state of size \(s\) if and only if
\[
 \max(0,k-(n-s))\le a\le\min(k,s).
\]
The upper bounds are immediate. For sufficiency, choose \(a\) live
hypotheses and pad with any \(k-a\) already eliminated hypotheses. This is
an actual supplied hyperplane; it does not assume a free membership query.

Suppress constant queries. The exact raw Bellman recurrence is therefore
\[
 C(0)=C(1)=0,\qquad
 C(s)=s+\min_{a\in I_s}\{C(a)+C(s-a)\},
\]
where
\[
 I_s=\{\max(1,k-(n-s)),\ldots,\min(k,s-1)\}.
                                                               \tag{1}
\]
Every child has fewer than \(s\) hypotheses. Compute in increasing \(s\),
store one minimizing split, and reconstruct actual supplied queries by
the padding rule. A dictionary maps each response cell to an actual
supplied test and its orientation. If the desired cell is the negative
response of that test, reconstruction swaps the two child trees. Thus
complemented-only and mixed query descriptions still produce a tree using
only actual supplied tests. This gives an exact polynomial algorithm, with
\(O(n^2)\) DP operations and a proper output tree of \(n\) leaves.

For the all-flats query class of the same uniform matroid, every subset of
size at most \(k\) is available, together with the whole ground set. The
exact recurrence instead uses
\[
 I_s=\{1,\ldots,\min(k,s-1)\}.                              \tag{2}
\]
The chosen live subset is already a supplied flat and needs no padding.
This is again an exact polynomial algorithm.

The promised complete classes can themselves be checked polynomially from
an explicit query matrix. Collect the response cells of size \(k\);
their distinct count equals \(\binom nk\) exactly when all \(k\)-subsets are
present. Also verify that every nonconstant query is equivalent to a
\(k\)-subset query. For all flats, do the analogous check on response
cells of sizes \(1,\ldots,k\), with required count
\(\sum_{j=1}^k\binom nj\). These counts have polynomial bit length; no
missing-subset enumeration is needed. Extra arbitrary queries cannot be
silently retained while claiming these recurrences remain exact.

This class is generally not an affine coordinate product. Completeness
and permutation symmetry, rather than a rank bound alone, make the DP
exact.

## 2. Discovered rank alone is far from sufficient

Take \(k=2\), \(n\ge5\). The all-hyperplanes system of \(U_{3,n}\) is exactly
the family of all pair queries. Its all-flats extension additionally
contains singleton queries.

The response-cell discovery method finds rank three on either family.
Indeed the size-two response cells are all pairs, precisely the
hyperplanes of \(U_{3,n}\), and every query can be oriented to a flat.
The alternative complementary hyperplane class has rank \(n-1\). In the
all-flats system the size-one class would give rank two, but it is rejected:
a pair and its complement are neither singleton nor empty nor the entire
ground set, so that class cannot orient the pair queries to flats.

The old rank-limited coding certificate is therefore
\[
 \Phi(H)=M_2(n)=\Theta(n^{3/2}).                            \tag{3}
\]
For completeness, its lower-order scale follows from the sequential
capacity bound \(1+t+\binom t2\): a constant fraction of \(n\) leaves cannot
finish before \(\Theta(\sqrt n)\) queries. For an upper bound, group the
abstract leaves into \(\lceil\sqrt n\rceil\)-sized batches, use a
budget-two selector comb, and a budget-one singleton comb inside each
batch. This costs \(O(n^{3/2})\). These are abstract coding arguments,
not a claim that those batch queries exist in the pair system.

Actual pair queries instead have exact optimal raw cost
\[
 C(2m)=m^2+3m-2,\qquad C(2m+1)=m^2+4m.                    \tag{4}
\]
The bases are \(C(1)=0,C(2)=2,C(3)=5\); thereafter an optimal split removes
two live hypotheses and costs \(s+2+C(s-2)\). Comparing the alternative
singleton split using these formulas proves the recurrence by induction.
The required two-subset is always an original pair; when only two or three
live hypotheses remain, padding with eliminated hypotheses realizes the
necessary singleton splits. The all-flats extension has the same optimum.

Equations (3)-(4) give
\[
 F^*(H)/\Phi(H)=\Theta(\sqrt n).
\]
Thus there is no constant, or even polylogarithmic, code-versus-discovered-
rank-only guarantee for the complete all-hyperplanes/all-flats matroid
query class. This is a certificate-quality obstruction, not hardness:
the class has just been solved exactly by (1)-(2).

## 3. Search resources repair this particular obstruction

The example does not defeat the combined rank-plus-cap or pair ledgers.
If every query has an oriented side of population at most \(b\), charging
each first-separated pair to its endpoint outside that side gives
\[
 F^*(H)\ge \frac{n(n-1)}{2b}.
\]
Every outside endpoint pays at most \(b\) pair charges per queried node.
For pair queries \(b=2\), this already has the correct quadratic scale.
The maximum minority cap is directly readable from the matrix.

More generally, a size-by-rank envelope
\(c_j=\max\{|F|:F\text{ is a flat of rank at most }j\}\)
can strengthen the old abstract capacity DP. For uniform matroids it is
explicit: \(c_j=j\) below full rank, and \(c_{k+1}=n\).
The present note does not claim that discovering all lower-rank envelopes
is polynomial for a general explicitly listed hyperplane family, nor that
such an envelope gives an executable code for every matroid.

The unresolved broader task remains a code-or-certificate theorem on
general complete matroid query classes with varying hyperplane densities
and negative-history restrictions. Root rank alone cannot be that theorem.

## 4. Verification

The companion checker compares (1)-(2) against an independent full-mask
Bellman solver for all small \(n,k\), builds the supplied-query output trees,
and executes them on every hypothesis for original, complemented-only,
and mixed descriptions. The 56 exact recurrence cases give 168 actual
description cases and 1,008 hypothesis executions. It checks the completeness
recognizer and the pair-query closed form. Deterministic larger rows
compare the exact pair-query optimum to the existing \(M_2\) recurrence.
Full-mask and abstract-code DPs in the audit are validation only; the
proposed class algorithm is the polynomial cardinality DP.
