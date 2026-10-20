# A growing-depth serial grid defeated by quadratic code lifting

Auxiliary research note, 18 October 2026. No article or earlier script was
edited. The main result is a coverage theorem for a structured subclass, not
an unrestricted approximation theorem.

**Proved result.** A natural serial composition can give ordinary balance
greedy its full-order `Omega(log n / loglog n)` approximation gap. Nevertheless,
the existing frozen-source global-lifting generator supports a constant-factor
comparison tree for this entire family in its **first** quadratic-state pass.
The number of serial levels may grow with n; no closure exponent or search
horizon grows with it. Thus simply recursively hiding fast row codes behind
more independent equality selectors does not defeat the generator.

The deterministic checker `research-general-recursive-lifting.py` verifies the
source membership and every required state intersection on three bounded
examples. It uses no optimal-subproblem oracle and no random search. In
particular, it does not infer the theorem from small-instance exactness.

## 1. Connection with the planar argument

I reread the common-witness normalization in
`sections/03-common-witness-geometry.tex`, the witness-path restriction credit
in `sections/06-expected-depth.tex`, and its stage-to-tree conversion. The
transferable idea is to identify which actual queries become constant after a
class is known, and to make the comparison through an executable policy.

Here the structural substitute for geometry is an exact product projection.
Pure context queries keep the same meaning when their conditional code is
lifted out of a slice. Their global leaf cells are full context fibers. A
quadratic intersection then restricts an unactivated code prefix to its correct
context. This is an explicit state-coverage argument, rather than an assumed
membership query. There is also a coherent external all-negative route for the
lower bound; it need not be the response word of a hypothesis.

## 2. A basic projection-lifting lemma

Let H=X times Y with equal multiplicity |X| over each y. Suppose an available
source code on the slice `{x0} times Y` uses only physical tests whose responses
depend on y. Its direct global replay identifies y, leaving the whole fibers
`X times {y}`. Its raw prefix work is `|X| F_B(Y)`. If each fiber receives an
actual complete fallback of raw cost C_y, the global full code has raw cost

    |X| F_B(Y) + sum_y C_y.

In particular, the source may be a poor decoder of Y: its cost can still cancel
against exactly the same Y decoder appearing after an expensive X decoder in
the incumbent. A recursive bad context code therefore does not automatically
protect an outer bad row code from query reordering.

The same statement holds for any transversal containing one representative
per y, provided its physical source queries depend only on y. Rectangular
activation is not necessary. For nonuniform fiber sizes the exact first term
is the corresponding weighted sum of source path depths; uniform cancellation
should not be assumed in that case.

The later theorem uses a second ingredient: not only pure fiber decoders, but
also conditional bit-code prefixes whose global cells can be clipped to a
known fiber using just one additional base-state intersection.

## 3. The instance family and the test priority

Fix L>=1 and strictly decreasing even integers

    M0 > M1 > ... > ML >= 6.

There are n=product_k Mk equiprobable hypotheses, represented by tuples
`x=(x0,...,xL)` with `0<=xk<Mk`. All tests are binary and unit cost.

Supply these physical tests:

1. For every coordinate k and every value v, the pure equality test `xk=v`.
2. For every k>=1, every full lower context
   `b=(x0,...,x{k-1})`, and every binary coordinate j of xk, the gated bit test

       q(k,b,j) = 1 exactly when lower context equals b and bit j of xk is 1.

Coordinate 0 has only equality tests. No direct full-context membership test
is added. The tests are ordered by ascending factor k; within each factor,
all gated bit tests precede its equality tests. This is an explicit tie rule.
The proof depends on this order. The decreasing alphabet sizes remove the
opposite tie that would otherwise force an incompatible global priority.

The number of tests is

    m = sum_k Mk
        + sum_{k=1}^L ceil(log2 Mk) product_{i<k} Mi
      = O(n log n).

Thus the response matrix is an ordinary explicit polynomial-size instance.
The construction does not enumerate a parameter-dependent family of policies.

Write

    e(M) = (M+1)/2 - 1/M

for the average cost of identifying a uniform M-element set by equality
queries. The last value is inferred, so its raw equality-tree cost is
`M(M+1)/2-1`.

## 4. Initial greedy is exactly the reverse equality policy

**Lemma.** Balance greedy decodes `xL,x{L-1},...,x0`, using only pure equality
tests and completing each coordinate before starting the next. Its average
depth is exactly

    D_G = sum_{k=0}^L e(Mk).                                (1)

At the beginning the largest equality minority is `1/ML`, strictly larger
than that of the other equality tests. Once some values of that coordinate
have been excluded, an equality test on a remaining value has minority at
least its original `1/ML`, so that coordinate remains preferred.

More generally, suppose coordinate i is being searched, has s remaining
values, all higher coordinates are fixed, and lower ones remain uniform.
Its equality tests have minority `1/s`. A gated test on an undecoded coordinate
must also hit a prescribed lower context, and cannot beat that minority.
A gated test on an already fixed higher coordinate is either zero or the
indicator of a specified remaining lower-context tuple. For i>=1 its minority
is at most `1/(s M0)`, strictly smaller. When i=0 this may tie `1/s`, but the
factor-ascending order places the coordinate-0 equality test first.

The same argument applies on a slice where all coordinates k,...,L have been
fixed. Fresh greedy there decodes only the lower coordinates, by pure
equalities. This fact supplies the projection transversals needed below.

## 5. Every full lower-context fiber is a generated base state

For a lower context b of length k, let

    S(k,b) = {x: (x0,...,x{k-1}) = b}.

The initial greedy tree contains the node

    C_k = {x: xk=...=xL=0},

because it identifies the higher coordinates first. On C_k, fresh greedy uses
only pure equality queries on the lower k coordinates. `source_codes` generates
this actual conditional code at that incumbent node. Its global lift uses
exactly those lower-coordinate equality queries, independent of higher
coordinates. Its leaves are precisely **all** cells S(k,b).

The existing completion rule fills each nonsingleton lifted leaf while
retaining that leaf cell as the root of its fallback tree. Therefore every
S(k,b) is a base state. This holds for every k from 1 through L. The state
S(0,empty)=H and the full-context singleton fibers at k=L+1 are already base
states. One fixed-higher-coordinate slice per level is enough; we are not
enumerating all possible policy orders.

This is the first reason a nested equality gate does not hide a context from
lifting: a code learned at a thin final slice can expose the full global
context partition without activating that slice.

## 6. Forced positive LSB sources supply the intermediate bit states

Fix k>=1 and context b. The physical root test `q(k,b,0)` is available. Its
positive outcome is the conditional source domain

    C = {lower context b, xk odd, higher coordinates arbitrary}.

The source generator explicitly builds fresh greedy on every supplied root
query child, so this source is included even when the incumbent never visits C.

**Lemma.** On C, fresh greedy first identifies xk using only its active gated
bits other than the already known LSB. It does not begin decoding higher
coordinates until xk is known.

To prove this, divide xk by two: the odd values correspond to the consecutive
integers 0,...,Mk/2-1. Under any partial assignment of their binary coordinates,
the least free coordinate splits the remaining values into floor(s/2) and
ceil(s/2). Every complete pair of values in that free coordinate occurs before
the interval endpoint, with at most one unmatched value. Thus an active bit
has minority at least 1/3 whenever s>=2, with the s=2 case giving 1/2.

An equality on xk has minority 1/s and can tie only at a small state; the gated
bit comes first. An equality on a higher coordinate has minority at most
`1/ML<=1/6`. A higher gated bit must additionally guess the current xk value
and a binary response, so its positive mass is at most `1/(2s)` until xk is
known. Lower-coordinate tests are constant. This proves the claimed prefix.
Its path length is at most `ceil(log2 Mk)-1`.

Lift this actual source code globally. Consider just its initial xk-decoding
prefix and call its global node cells P. Inside S(k,b), its physical tests
depend only on xk, and ignore the LSB. Thus

    A = S(k,b) intersect P                                  (2)

is exactly a cell of the same binary program on all values of xk. Every such
P is a base state of the **full** lifted source: a cut inside the source
remains an internal lifted node, and an original core leaf receives a fallback
whose root retains that lifted cell. Section 5 supplies S(k,b) as a base state.
Consequently every A in (2) belongs to the quadratic family Q squared.

At the end of this prefix, the remaining xk values are precisely a pair
`2v,2v+1`. Query its LSB last. The two resulting cells are

    S(k+1, b followed by 2v),
    S(k+1, b followed by 2v+1),

both already base states by Section 5. No third intersection is needed.
The even-alphabet assumption is essential here: every odd representative
has its even partner, with exactly the same remaining binary coordinates.

This “decode all but one bit, then use known context fibers” is the specific
quadratic coverage mechanism. Simply taking all bit outcomes and intersecting
them to unbounded depth would not be a polynomial argument.

## 7. Full supported-tree theorem

**Theorem.** On the family above, the first pass of the existing plain lifting
generator supports a complete tree with average depth at most

    C = e(M0) + sum_{k=1}^L ceil(log2 Mk).                   (3)

The weighted/actual-boundary candidate is at least as good in this first pass.

Construct the tree as follows. First decode x0 by a lifted pure equality code.
For each resulting context, use the prefix in Section 6 to decode all but the
LSB of x1, then ask its LSB. Continue to x2 and so on. Every intermediate node
is certified by (2); every full context node is a base state. Thus every query
has represented children, and the entire policy is supported by the quadratic
family. Its first coordinate costs e(M0); each later coordinate costs at most
`ceil(log2 Mk)-1+1`, proving (3).

For a complete supported policy P, incumbent-depth prizes give reward exactly
the incumbent's full raw cost. Its depth-prize profit is therefore
`F_incumbent-F_P`. Exact supported policy optimization and splicing returns
a tree of raw cost at most F_P. If the incumbent is already cheaper, the
desired bound holds directly. Hence the comparison is about the actual output
tree, not just existence of an abstract low-cost policy or a pruning bound.

The strong candidate's first-pass source set includes the unweighted sources
used here, and actual-credit DP can realize the same complete tree. All other
generated templates, weighted choices, and boundary edges can only improve
this first-pass upper bound.

## 8. A constant ratio on this subclass

Every supplied **positive** support has size at most

    B = n/ML.

Equality supports have size n/Mk. A gated bit has positive mass at most
`1/(2 product_{i<k} Mi)`, because each coordinate bit on an initial interval
has at most half its values positive. All tests use this same rare-positive
orientation; the assertion is stronger than an unoriented minority cap.

**Oriented all-negative lower bound.** Here B>1 because L>=1 and all factors
are at least six. Follow the all-negative path of any complete identifying
tree. After t tests, the union of positive supports can exclude at most tB
hypotheses, so at least n-tB hypotheses remain. For every
`t=0,...,ML-1`, that cell has at least B>1 hypotheses and is necessarily
internal. Its uniform mass, and hence its contribution to raw expected work,
is at least `1-t/ML`. Summing those actual queries gives

    OPT >= (ML+1)/2.                                        (4)

The B>1 condition matters: for B=1 the last cell could already be a singleton.
Likewise, merely knowing a small minority side without a common physical
positive orientation would not justify this all-negative calculation.
Independently, binary information gives

    OPT >= log2 n.                                         (5)

Put rho=M0/ML. The first term in (3) is smaller than `(M0+1)/2`, which is at
most rho times (4). Also L is at most `log2 n / log2 ML`, so the remaining terms
in (3) are at most

    log2 n + L <= (1+1/log2 ML) log2 n.

Keeping the two lower bounds together gives the sharper exact comparison

    first-pass output / OPT
      <= [e(M0)+sum_{k=1}^L ceil(log2 Mk)]
            / max(log2 n, (ML+1)/2).                        (6a)

A convenient bound depending only on the alphabet spread is

    first-pass output / OPT <= rho + 1 + 1/log2 ML.          (6b)

For comparable alphabets this is a constant. This ratio is not asserted for
arbitrary response tables, unequal prior weights, or a different source pool.

## 9. The family still contains a full-order greedy obstruction

Take even M tending to infinity, let `L=floor(M/log2 M)`, and put

    Mk = M + 2(L-k),  k=0,...,L.

Then `rho=1+O(1/log M)`, and (6b) is `2+o(1)`. In fact (6a) is sharper:
`log2 n=(1+o(1))M`, `e(M0)=(1/2+o(1))M`, and the remaining bit-code sum is
`(1+o(1))M`. Thus the first-pass output is a **3/2+o(1) approximation on this
growing-depth full-gap subfamily**. Meanwhile (1) is
`Theta(M squared / log M)`. The explicit context-first tree in (3) has average
depth O(M), so the ordinary greedy approximation ratio is at least
`Omega(M/log M)`. Finally

    log2 n = sum_k log2 Mk = Theta(M),

and thus greedy has gap `Omega(log n / loglog n)` on this growing-depth
subfamily. The one-pass coverage theorem defeats that full asymptotic
obstruction, not merely a fixed small instance or a bounded number of levels.

More generally, the root researcher observed that for any fixed c>=1/2,
choosing `L=floor(c M/log2 M)` makes (6a) at most
`1+1/(2c)+o(1)`. Greedy still has a full-order gap, with a constant depending
on c. These comparisons use the explicit constructive upper bound and the
binary entropy lower bound; no claim that the comparison tree is exactly OPT
is needed.

The result is not an unrestricted constant approximation. It establishes that
this tempting serial amplification of hidden conditional codes cannot serve
as a lower-bound family for the generator under the stated priorities.

## 10. Polynomial scope and bounded independent checks

The theorem invokes only sources already generated in one pass:

* One actual incumbent slice code per level, exposing all context fibers.
* One forced-positive-LSB source per lower context, exposing its next-factor
  binary prefix.

All of these are actual complete uniform-greedy source codes. Only their
prefixes are used in the proof, and every used prefix state is explicitly
checked to occur in the full lifted code. Intersections are always of **two**
generated base states. L can grow up to O(log n), but neither the generator's
closure exponent nor a policy enumeration width depends on L. The earlier
fixed-exponent runtime analysis therefore applies unchanged.

The checker constructs only the required sources and a reduced family
consisting of their actual base states plus the certified comparison-tree
states. It does not enumerate the full quadratic family. Since every added
state comes with an explicit two-base-state witness, this reduced family is a
subset of the real generator's family. Exact depth-prize DP on it independently
realizes the comparison tree's cost.

| Alphabets | n | m | Initial greedy raw cost | Supported comparison | Reduced-family output |
| --- | ---: | ---: | ---: | ---: | ---: |
| (8,6) | 48 | 38 | 370 | 338 | 338 |
| (10,8) | 80 | 48 | 782 | 672 | 672 |
| (10,8,6) | 480 | 294 | 6292 | 5312 | 5312 |

For n=480, 92 required source codes produce 1906 base states; 2086 states
suffice for the reduced pricing check. All 959 actual comparison-tree node
states are certified in the quadratic family. Direct per-hypothesis query
execution verifies the resulting policies. Initial greedy uses only the
predicted reverse-order equality tests, and its raw cost agrees exactly with
(1). The maximum positive support agrees with n/ML. No exponential exact
optimization was called.

Run `python research-general-recursive-lifting.py`; the stable output is
`research-general-recursive-lifting-results.json`. Syntax compilation passed.

## 11. Context-dependent code permutations do not change the theorem

The same proof permits an arbitrary bijection `pi(k,b)` of the Mk labels for
every factor and lower context. Replace each gated test by the corresponding
bit of `pi(k,b)(xk)`, while retaining the pure equality tests on the original
xk values and their priorities. The family and lower bounds are unchanged.

Indeed, initial reverse-order dominance used only the activation cap when the
lower context is unknown. Once a higher row value is fixed, its gated test
remains either zero or an indicator of one full lower-context tuple, whatever
its permuted bit is. Thus the slice context decoders remain pure equality
codes. The forced positive LSB source now sees uniform odd **labels**. Its
other-bit prefix identifies the label pair 2v,2v+1, and the final LSB leads to
the known fibers with original values `pi(k,b)^{-1}(2v)` and
`pi(k,b)^{-1}(2v+1)`. The same two-base-state intersections certify every node.

This is a proved relabeling corollary; the bounded checker above implements
identity labels only. It rules out merely changing local code labels by
permutations, including permutation patterns chosen from a graph, as a way of
breaking this particular argument. It does not cover tests simultaneously
activated on several different contexts.

### Addendum, 19 October 2026: one completed lift already suffices

Root observed a simpler proof of the same constructive upper bound. The
quadratic clipping certificate above remains valid, but its additional
sources and intersections are unnecessary once the **existing** fresh-greedy
fallback in `finish_partial` is included.

Take the actual incumbent node C0 where x1,...,xL are all zero and x0 is
free. On C0 each higher private gated test is either zero or one x0-value
indicator: its other lower coordinates are fixed, as is its target row.
This remains true under every context-dependent code permutation from this
section. Every nonconstant gate is therefore identical on C0 to a supplied
x0 equality. The ascending-factor priority puts x0 equalities first, so
fresh greedy on C0 is a pure equality decoder of x0.

Its global replay has exactly the full x0 fibers as leaves and costs
`n e(M0)`. On each such leaf the actual fresh greedy fallback decodes the
remaining factors in ascending order using their now-active owner bits.
The conditional-code lemma already proved above applies after every newly
identified row: a current-row bit is sufficiently balanced, higher private
gates activate only on a single remaining current value, and higher pure
equalities have minority at most1/6. Context-dependent permutations merely
relabel the uniform initial-interval labels; the same bit-query argument
uses at most `ceil(log2 Mk)` queries per row path. Consequently this single
completed lifted source has mean at most

    e(M0)+sum_{k=1}^L ceil(log2 Mk).

`finish_partial` chooses the cheaper of that fresh code and actual incumbent
restriction on each leaf, so it inherits the bound directly. Its completed
tree's actual nodes are retained in the base pool before any intersection
closure. Thus the main first-pass bound and its constant/asymptotic
corollaries follow already from one actual incumbent source, one global
replay, and existing fresh fallback. No extra harvest layer, forced-positive
source, or quadratic intersection is needed for this family.

`research-general-recursive-single-lift.py` directly executes this shorter
construction on the same three tables, and on three versions with explicit
context-dependent nontrivial code permutations. In all six checks, both
fresh-only completion and the existing fresh/pruned minimum cost338,672,
and5312 for n=48,80,and480 respectively, matching the earlier constructive
outputs. Initial costs remain370,782,and6292. The source uses only15,19,
and19 nodes, respectively. Results are saved in
`research-general-recursive-single-lift-results.json`. No optimum oracle or
intersection construction is called by this direct checker.

## 12. What a surviving recursive obstruction must change

This proof uses three exact properties: a thin slice produces a pure projected
context decoder, forced positive bit outcomes produce a balanced next-factor
prefix, and a global context fiber clips the lifted prefix with only one
intersection. Aliased outside answers may destroy the projection property;
irregular fibers may destroy uniform cost cancellation; and several dependent
context restrictions may require more than quadratic state clipping.

No scalable family surviving all those operations is proved here. The result
narrows the adversarial target: independent serial selectors plus private bit
codes, even over a growing number of levels and with a full greedy gap, are
not enough. A useful next construction would need genuinely dependent routing
or code semantics that prevent these exact context fibers or their one-factor
prefixes from appearing in the generated pool.
