# Filtered conditional sources recover multiple-selector activation codes

Auxiliary research note, 19 October 2026. The article is unchanged.

**Result.** A new polynomial source-generation variation has a constant
approximation guarantee on the multiple-selector class below, including
arbitrary local bijections and arbitrary bounded-incidence activation sets.
The comparison constant approaches \(D+P-1\) for large alphabets. This is
a subclass theorem, not an unrestricted approximation improvement. The
ordinary source generator in `research-general-code-lifting.py` does not
filter tests by their global root minority; this note adds that operation.

## 1. Model and the polynomial variation

Let
\[
 H=[M]^k\times\prod_{j=1}^{\ell}[r_j],\qquad
 k\ge2,\quad 2\le r_j<M,\quad N=\prod_jr_j,\quad n=M^kN.
\]
The first \(k\) coordinates are selectors. All pure coordinate-equality
queries are supplied, preceding the remaining queries in the input order.
Every other physical query belongs to a body-\(j\) palette: it is active on
a set of at most \(D\) selector contexts and, at each active context, reads
one bit of a context-specific bijection from \([r_j]\) to the labels
\(\{0,\ldots,r_j-1\}\). A palette supplies all
\(b_j=\lceil\log_2r_j\rceil\) bits. Each selector context has at least one
complete palette for each body, and belongs to at most \(P\) palettes per
body. The local bijections can be unrelated. Assume
\[
 D<M^{k-1},\qquad B=\sum_jb_j.
\]
Here gating depends only on the selector context and the target body. It
does not depend on earlier body values, unlike the serial model in
`research-general-aliased-routing.md`.

Start with actual ordinary greedy \(T\). For every nonsingleton incumbent
node \(C\) and every distinct global root-minority threshold \(t\), build
greedy on \(C\) using only supplied tests whose root minority is at least
\(t\). If that filter cannot split a nonsingleton cell, stop it unresolved.
Replay the resulting actual partial source on \(H\), then fill every exit
with the cheaper of fresh ordinary greedy and actual incumbent restriction.
Keep the cheapest complete tree, including the original incumbent.

There are at most \(2n-1\) incumbent states and at most \(n\) different
filters. A proper conditional source and its replay have at most \(n\)
leaves; completing all disjoint exits still gives at most \(n\) leaves.
All greedy choices scan the supplied matrix, and restrictions are direct
tree operations. Thus the whole variation has a fixed-exponent polynomial
runtime in the explicit \((n,m)\) input. No selector representation,
activation sets, palette identities, or useful threshold need be given to
the algorithm. Those objects describe the class and its proof. Sources
are frozen before lifting, so the count does not hide recursive generation.

## 2. A useful source is necessarily present

Until every body is fixed, ordinary root greedy uses only body equalities.
Indeed the selectors remain uniform on \([M]^k\). A gate has positive
mass at most \(D/M^k<1/M\); a selector equality has mass \(1/M\); and an
unfixed body offers an equality with minority at least \(1/r_j>1/M\).
After negative equality answers its remaining alphabet only shrinks. This
proves the invariant by induction, including all branches.

Consequently the actual incumbent has a node \(C\) containing every selector
context and exactly one fixed tuple of body values. Its population is
\(M^k\). Its fresh unfiltered greedy may use aliased gates and fail to
project to selectors; no projection claim is made for that source.

Choose the global threshold \(t=n/M\). Every pure equality has root
minority at least \(n/M\), while every gate has root minority strictly
below it. This filter is among the enumerated filters, because selector
equalities have exactly that minority. On \(C\), all body equalities are
constant. Filtered greedy is therefore a pure selector equality decoder.

Replay uses only selector queries, so each source leaf becomes precisely
one full selector fiber \(H_c=\{c\}\times\prod_j[r_j]\). Its raw work is
\[
 W_{\rm selectors}=nk e(M),\qquad
 e(M)=(M+1)/2-1/M.
\]
This remains true for any adaptive ordering of the selector equalities:
restricting a coordinate comb to a live subset gives the same optimal
singleton-search mean for that subset. Outsider replay creates no
contamination difficulty here: the intended global exits are exactly the
fibers on which fresh completion is permitted.

## 3. Fiber greedy has height at most \(PB\)

Once all selectors are known, every nonconstant query depends on one body
coordinate only. Every equality/bit history is therefore a product of
uniform surviving body subsets. Queries on different bodies can interleave;
the following argument applies separately to each body along each path.

Fix a body's owner palette of \(b\) bits, and suppose its row has not yet
been identified. Before the first singleton equality chosen on that row,
all queries on it are bits from at most \(P\) palettes. If no singleton is
ever chosen, at most \(Pb\) proper row queries occur.

Otherwise let \(q\) owner bits have been asked, and let \(s\) be the surviving
row population immediately before its first singleton equality. That query
has minority \(1/s\). Every remaining owner bit has minority count at most
one, since it was available to global greedy and could not beat the chosen
equality. Already asked owner bits are constant. Among distinct owner labels,
at most one agrees with all remaining-bit majority responses. Every other
label is in at least one of the at most \(b-q\) minority singleton cells.
Thus \(s-1\le b-q\).

The prefix contains at most \(q+(P-1)b\) row queries. Any subsequent proper
binary policy on the remaining \(s\) values has path length at most \(s-1\)
when only its row queries are counted. Their sum is at most \(Pb\).
The argument does not require a common affine representation, consecutive
palette priority, or a row-by-row greedy execution. Therefore each fiber's
fresh greedy height is at most \(PB\), and the new source variation outputs
a complete code with mean at most
\[
 U=ke(M)+PB.                                                   \tag{1}
\]

## 4. A jointly feasible pair-and-coding lower resource

More generally suppose a fiber completion guarantee is \(qB\), with
\(q\ge1\). Take
\[
 w=\frac1{D+q-1},\qquad \lambda=\frac q{D+q-1}.
\]
For every unordered pair differing in exactly one selector coordinate and
agreeing on all bodies, give its containment potential weight \(w\).
Give each selector fiber the coding potential
\(\lambda L_2(|S\cap H_c|)\), where \(L_2\) is the exact unrestricted
binary coding profile. These resources share the same query/hypothesis
capacities; they are not independently valid ledgers added at full weight.

For a pure selector equality, assign each separated pair to its endpoint
outside the equality cell. Every hypothesis receives at most one weight
\(w\), and all fiber coding deficits are zero. A pure body equality separates
no selector pair, and incurs coding load at most \(\lambda\le1\).

For a gate with activation set \(A\), assign a cut edge with one inactive
endpoint to that endpoint. It has at most \(D\) active neighbors in all
selector directions combined, so receives load at most \(Dw\le1\). Among
active endpoints assign each cut edge arbitrarily to one endpoint. Every
active point has at most \(D-1\) active neighbors, and its fiber's coding
load is at most \(\lambda\). Its total load is at most
\((D-1)w+\lambda=1\). Inactive fibers have zero coding deficit. These
assignments prove all-subset Bellman validity by the usual endpoint ledger.

There are \(nk(M-1)/2\) selector pair features and \(M^k\) fibers. Hence
\[
 \operatorname{OPT}\ge
 \frac{A+qL_2(N)/N}{D+q-1},\qquad A=\frac{k(M-1)}2.             \tag{2}
\]
With \(q=P\), (1)-(2) give the explicit class guarantee
\[
 \frac{F_{\rm output}}{F^*}\le
 (D+P-1)\max\left\{1+\frac2M,
             \frac{B}{L_2(N)/N}\right\}
 \le(D+P-1)\max\left\{1+\frac2M,
                       1+\frac1{\log_2 r_{\min}}\right\}.     \tag{3}
\]
The first ratio uses the exact identity \(ke(M)/A=1+2/M\).
Thus fixed \(D,P\) give \(D+P-1+o(1)\) as all alphabet sizes grow.
The number of selector coordinates may grow; the proof does not pay
\(M^k\) queries to recognize one context.

The same argument gives \(q=1\), and thus \(D+o(1)\), when fiber greedy is
known to finish each body in \(b_j\) queries. Sufficient examples are full
binary-cube bodies with all active palettes affine in a common local cube
coordinate system, or full-cube bodies with arbitrary bijective palettes
and consecutive palette priority. For non-power-of-two bodies, consecutive
priority alone does not prove this stronger conclusion. Equation (3) uses
the robust \(q=P\) theorem and needs neither special condition.

## 5. Relation to the greedy obstruction and bounded checks

This class includes full-order greedy lower examples. For example take
fixed \(k=2,D,P\), body sizes \(\Theta(M)\) below \(M\), and
\(\ell=\Theta(M/\log M)\). Initial greedy pays
\(\sum_j e(r_j)=\Theta(M^2/\log M)\) on the bodies alone, whereas (1) is
\(O(M)\), and \(\log n=\Theta(M)\). The filtered variation therefore
escapes a \(\Omega(\log n/\log\log n)\) greedy gap on this class.
This does not imply a ratio for arbitrary query systems, where no useful
threshold or selector slice need exist.

The checker executes deterministic cyclic degree-two activation examples
with two or three selectors, interleaved palettes, and unrelated local
bijections. It checks the actual incumbent slice, the global root filter,
all selector-fiber replay exits, every fiber path's \(Pb_j\) bound, actual
completed-tree execution, and every query/hypothesis load of the joint
resource. It also runs the entire polynomial source menu on the smallest
example. The finite examples are mechanism and certificate checks; their
initial greedy trees can already outperform the displayed conservative
filtered comparison. No exact optimum oracle or adversarial search is
used, and the full source menu is not run on the larger examples.

One explicit two-body example has \(M=8,k=2,r_1=r_2=6,D=P=2\), with
\(n=2304\) hypotheses and 412 queries. Its filtered-source replay and fresh
completion costs 32,448, compared with initial greedy cost 33,029. Its
unfiltered incumbent slice really uses a nonprojection alias gate. This
checks an actual improvement mechanism, rather than only the conservative
class comparison.

A broader retained-quotient context generator is being developed
separately: factoring the retained response support can explicitly supply
selector fibers, without needing their witness slice in the incumbent.
That direction is distinct from the lighter filtered-source variation
proved here. Its general quality is not asserted by this note.
