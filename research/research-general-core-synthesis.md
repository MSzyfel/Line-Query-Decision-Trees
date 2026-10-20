# Selected-row cores with legal continuation codes

Research checkpoint, 18 October 2026. This note develops a polynomial
**weighted pricing primitive** beyond all-row literal rank. It bounds the
price/work of a legal policy by an explicit capped-prize surplus benchmark.
That benchmark is not proved comparable to unrestricted partial-policy
pricing. No unrestricted improved decision-tree ratio is proved.

## 1. Selected rows and the collision problem

Choose any subfamily \(R\) of supplied binary test rows and write
\(r_R(A)\) for the column rank of the constant row and rows in \(R\), over
\(\mathbb F_2\), restricted to \(A\). Hypotheses with the same \(R\)-signature
are parallel columns. Thus a minimizer of rank minus a strictly positive
modular reward includes whole signature classes: adding an omitted member
of a represented class increases reward without increasing rank.

This is useful, but a row basis cannot distinguish members of such a class.
Selecting one representative per class and silently identifying it would
be invalid. We instead supply legal **continuation codes**.

Compute the global \(R\)-signature classes \(E_j\). For each class construct
any legal identifying code \(B_j\) using the original tests, for example
fresh greedy. Its raw class cost and mean are
\[
 F_j=F_{B_j}(E_j),\qquad \ell_j=F_j/|E_j|.
\]
For a rational threshold \(L\ge0\), let \(U=U_{R,L}\) be the union of classes
with \(\ell_j\le L\). Only the at most \(n\) distinct class means need be
considered.

For a union \(A\subseteq U\) of whole signature classes, take a row basis
starting with the free constant row and extending with actual rows in \(R\).
Ask the at most \(r_R(A)-1\) basis tests, suppressing queries constant on the
current core cell. Its leaves are the signature classes in \(A\). Append
their supplied codes \(B_j\). This is a legal identifying code for \(A\), and
\[
 F_A\le |A|\,[r_R(A)-1]+\sum_{E_j\subseteq A}F_j
       \le |A|\,[r_R(A)-1+L].                       \tag{1}
\]
The class code may have large height. Only its mean enters (1), because
load-threshold lifting controls total core work.

## 2. A polynomial weighted surplus oracle

Let \(w_h\ge0\) be polynomially bounded integer completion prizes. In the
intended application they are incumbent leaf depths, at most \(n-1\).
Choose an integer cap \(M\ge1\) and define
\[
 \widehat w_h=\min(w_h,M),\quad
 B(A)=\sum_{h\in A}(M+\widehat w_h),\quad
 Z(A)=B(A)-Mn,
\]
and
\[
 g(A)=r_R(A)+L\,\mathbf1[A\ne\varnothing].
\]
Both rank and the nonempty-set indicator are matroid rank functions, so
\(g\) is submodular. It is positive on every nonempty set.

**Theorem.** For fixed \(R,L,M\), one can in polynomial time either certify
that every \(A\subseteq U\) has \(Z(A)\le0\), or construct an actual partial
policy \(P\) such that
\[
 \frac{W(P)}{\sum_{h\in C(P)}w_h}
 \le \frac{2n}{\Lambda_{R,L,M}},\qquad
 \Lambda_{R,L,M}
   =\max_{\varnothing\ne A\subseteq U,\ Z(A)>0}\frac{Z(A)}{g(A)}. \tag{2}
\]
Every maximizing core can be taken to be a union of whole classes, so the
code construction in (1) applies. The computable benchmark in (2) is
explicit: capped prize retained by the core minus \(M\) for every outsider,
divided by a rank-plus-continuation cost.

To compute \(\Lambda\), first check \(Z(U)>0\); otherwise no subset has
positive surplus. Start with \(\lambda=Z(U)/g(U)\). Minimize the submodular
function
\[
 \lambda g(A)-B(A).
\]
If its minimum is less than \(-Mn\), the returned set has
\(Z(A)/g(A)>\lambda\); update \(\lambda\) to that ratio. Otherwise the
current core is an exact maximizer. This is Dinkelbach iteration with an
SFM subroutine. No nonempty-set constraint or cardinality constraint is
needed: an improving set has positive surplus and is nonempty.

For fixed rational \(L\), the ratio is determined by the integer pair
\((Z(A),r_R(A))\). With \(w_h,M\le n-1\), there are \(O(n^3)\) possible
positive pairs. Each iteration strictly increases the ratio, so the number
of SFM calls is polynomial. Rational bit lengths are polynomial. General
polynomially bounded integer prizes give the same fixed-exponent conclusion
with the corresponding bound. A primary SFM reference is
[Iwata, Fleischer, and Fujishige](https://arxiv.org/abs/math/0004089).

For \(\lambda>0\), adding a missing member of a represented signature class
does not change \(g\), and strictly increases \(B\), because \(M>0\).
Every SFM minimizer therefore contains whole classes. The initial set \(U\)
does as well.

## 3. Execution and proof of the guarantee

Build the code in (1) on the maximizing core \(A\). Execute its actual tests
on all hypotheses, stopping before any code node whose outsider count is
at least its core count. Contaminated singleton core leaves are stopped
unfinished. The load-threshold lemma in
[the lifting audit](research-general-code-lifting-audit.md) gives
\[
 W(P)\le2F_A\le2|A|\,[g(A)-1]\le2n\,g(A).
\]
At most \(n-|A|\) core hypotheses are lost. Each has capped prize at most
\(M\), so the actual finished prize is at least
\[
 \sum_{h\in A}\widehat w_h-M(n-|A|)=Z(A)>0.
\]
This proves (2). In particular, \(\Lambda>2n\) certifies an executable
positive-prize-minus-work policy. The exact prefix-pricing DP on the
explicit lifted code can only improve that certificate.

Notice that \(Z(A)>0\) implies \(|A|>n/2\), since
\(B(A)\le2M|A|\). The argument is a weighted majority-surplus argument; it
does not claim to price a small valuable core surrounded by many outsiders.
The restriction \(0<\alpha\le1\) in load-threshold lifting still matters:
using a threshold above one would leave some contaminated singleton core
leaves below the threshold.

For any fixed response bound \(K\), the proof extends by labeling each test's
outcomes with distinct elements of a fixed prime field \(\mathbb F_q\),
where \(q\ge K\). A row basis still consists of supplied tests, equality of
basis responses implies equality of all selected responses, and rank remains
submodular. Unused response branches stop unfinished in the lift. The
companion implementation and its finite checks are binary.

For unit prizes, \(M=1\), and a core of size at least \(3n/4\) with
\(r_R(C)+L\le s\), one has \(\Lambda\ge n/(2s)\), and (2) gives density at
most \(4s\). Setting \(L=0\) and taking singleton signature classes recovers
the earlier rank-core theorem. Taking classes of size at most \(b\) and
arbitrary proper local trees gives \(L\le b-1\), but cheap large classes are
also allowed.

## 4. Polynomial row-family menus and an executable candidate

One may take any polynomial menu of row families and choose the best actual
priced lift. Examples that are computable from the response table are:

* all prefixes of rows sorted by global minority population, and their
  suffixes;
* all prefixes of pair-cover greedy row selection;
* families of query rows appearing above each depth threshold in a supplied
  incumbent tree;
* fixed polynomially many seeded row permutations or samples.

For each \(R\), enumerate its distinct class means \(L\), and for each \(L\)
enumerate \(M=1,\ldots,n-1\), or any polynomial cap menu. The theorem then
holds simultaneously for the largest \(\Lambda\) over that menu. Row
selection has not been optimized over exponentially many subfamilies.

The companion script implements the legal code, global signature classes,
class mean filtering, threshold execution, and a **polynomial candidate
menu** that takes \(A=U_{R,L}\). It also implements exact ratio optimization
using an exhaustive SFM oracle only for small-instance validation. The
practical menu does not silently use an exponential oracle. Substituting a
standard polynomial SFM implementation gives the theorem's algorithm.

On a 64-hypothesis example, six coordinate rows encode a 56-point core;
eight outsiders have coordinate signature zero, and every singleton test is
also present. A balance-prefix family keeps the coordinates while removing
the singleton noise. Singleton-class continuation mean \(L=0\) selects 55
hypotheses and avoids the contaminated coordinate-zero class. Incumbent
prizes come from an actual legal singleton comb putting the outsiders first.
The checker verifies the positive pricing guarantee and actual execution.
All-row literal rank is 64 because of the singleton rows.

## 5. The remaining universal comparison

This is a concrete weighted pricing primitive, with legal collision handling
and a polynomial selection proof. It does not establish that its benchmark
\(\Lambda\) is comparable to unrestricted completion pricing on every input.
In particular, no full approximation follows from one successful root core.

Selecting rows by minimum rank alone is not a new tractable replacement for
minimum test cover. For any fixed \(C\), the minimum rank of a separating
selected-row matrix is exactly one plus the minimum number of supplied tests
needed to separate \(C\). A separating selected family has a basis of
\(r_R(C)-1\) supplied rows; conversely, \(k\) separating rows have rank at most
\(k+1\). The classical nonadaptive minimum test collection problem has
logarithmic approximation hardness; see the primary
[Halldorsson, Halldorsson, and Ravi paper](https://doi.org/10.1007/3-540-44676-1_13).
This is hardness for that nonadaptive surrogate, not for uniform
average-cost adaptive identification.

Adaptive local continuation codes partly avoid this surrogate: a large
signature class can be cheap, and then \(L\) is its actual supplied-code
mean rather than its cardinality or literal rank. For example, column tests
followed by balanced codes inside columns have small rank-plus-continuation
cost even when singleton noise makes all-row rank maximal. The missing step
is a theorem that some polynomially discoverable selected-row/continuation
family has large capped surplus relative to the optimum partial-policy
pricer at every frontier. Neither balance sorting nor minimum test cover
currently supplies that theorem.

## 6. Checks

Run the companion Python script. It checks exact ratio optimization
against all core subsets on small instances, verifies that the optimized
cores are whole signature-class unions, constructs the full legal core
codes and their lifted policies, and audits actual work and finished prize.
It separately executes the 64-hypothesis singleton-noise example with
genuine incumbent-depth prizes. Results are written to a JSON file.
An additional 32-hypothesis exact flat oracle checks genuine strict ratio
updates and the exclusion of eight independent outsider columns; it avoids
confusing cases where the full filtered ground is already optimal with a
test of the fractional iteration.
