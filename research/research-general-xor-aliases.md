# XOR camouflage defeats information filtering, then exposes partition components

Auxiliary research note, 19 October 2026. No article or stable earlier script
is edited. All approximation statements below concern the explicit subclass.
The unrestricted polynomial approximation target remains open.

**Result.** A deterministic growing alias family preserves the full greedy
gap, makes every individual gate independent of the **entire** body vector,
and leaves a prime identifying response relation after the proposed
information filter. Thus neither root-minority separation nor this
independence-plus-product-factorization step discovers its selectors.
However, a polynomial whole-component disjointness menu proposed by root
recovers the selector partition exactly and gives a constant approximation
on the growing family. The new seed is therefore a useful obstruction to two
discovery arguments, **not** an obstruction to the strengthened generator.

The bounded prototype checks actual completed lifts, exact contingency
independence, exact polynomial response factorization on the small cases,
and the disjointness repair. No exact OPT, random search, or full quadratic
state-generator fixed-point computation is used.

## 1. Family and the surviving greedy gap

Fix M=2^b with b>=2, R=M/2, a fixed k>=2, and ell<M. Let

    H=F_M^k times (F_2^{b-1})^ell.

Write C for the selector vector and Z_j for body j. Supply all body equality
queries, then the gates below, then all pure selector equalities. In
particular a gate wins a selector-equality tie. Every body has alphabet R.

Choose distinct nonzero field slopes a_j and forms

    f_j(c)=sum_{i=0}^{k-1} a_j^i c_i,
    h(c)=c_0,
    t(c)=h(c)>>1 in F_2^{b-1}.

Every coefficient of f_j is nonzero. The pair (f_j,h) has full rank, and
any two f_j,f_l are independent: their first coefficient is1, so distinct
slopes cannot give proportional coefficient vectors. Partition contexts by
`f_j(c)>>1`, each activation cell having `2M^{k-1}` contexts. The palette
for body j and group g supplies all b-1 physical tests

    q(j,g,u)=1 iff f_j(C)>>1=g and bit_u[Z_j xor t(C)]=1.   (1)

Thus one physical query has a different translated row-code meaning at
different active contexts. The active palette becomes a complete code for
its body once C is known. There are

    kM+ell R+ell(M/2)(b-1)

tests and n=M^k R^ell listed hypotheses. For fixed k and
`ell=floor(cM/log2 M)` with fixed c>0, this is an explicit polynomial-size
matrix and `log2 n=(c+o(1))M`.

For any fixed body vector z, (f_j(C),h(C)) is uniform on F_M squared, so t is
uniform on R labels even after restricting to an activation group. Therefore

    Pr(q(j,g,u)=1 | Z=z)=1/M.                              (2)

This also holds after any pure-body equality history by averaging. A body
equality has minority at least1/R=2/M until its row is fixed, whereas gates
have minority1/M and selectors also have minority1/M. Greedy consequently
identifies **all** bodies with pure equalities before any other test. Its
body contribution is exactly `ell e(R)`, with e(s)=(s+1)/2-1/s.

A legal selector-first code has mean

    U=k e(M)+ell(b-1).                                    (3)

For the growing ell above, U=O_k,c(M), while greedy's body work is
Theta(M squared/log M). Its full-order
`Omega(log n/loglog n)` gap follows regardless of how cheaply it later
identifies selectors. In contrast to the preceding all-one-zero-label seed,
the greedy invariant now uses exact independence (2), not a priority tie
against a fixed-body activation mass2/M.

## 2. Both root-minority and information filters miss the selector quotient

All selector and gate minorities are n/M; body-equality minorities are2n/M.
Thus minority filtering either retains everything or keeps body equalities
alone. The latter response family factors into the body axes.

For the information filter using the whole body vector, (2) keeps every gate
and every selector query; body equalities are removed. The retained response
word nevertheless identifies **every original hypothesis**: selector queries
give C, the active gate group then gives Y_j=Z_j xor t(C), and C determines
t(C), hence Z_j. There are still n distinct response words. Individual
independence has not removed joint selector/body coupling.

The retained response relation is prime. Here is an analytic proof, rather
than an inference from pairwise correlations alone.

1. All pure equality columns of one selector coordinate must belong to one
   response factor: their nonempty positive cells are mutually exclusive,
   so any two such response bits are dependent.
2. All gates for one body must belong to one factor. Gates in different
   activation groups have disjoint positive cells and positive marginals.
   Gates for distinct bits in the same group also have dependent responses:
   their joint positive probability is1/(2M), rather than1/M squared.
   There are at least two activation groups, so these edges connect the
   whole body's gate family even when it has just one bit.
3. Let V_j be that body's complete gate-response vector and let F be its
   putative response factor. Suppose a selector coordinate lies outside F.
   Condition on selector coordinates inside F and all the other selector
   values. Varying the outside coordinate changes f_j(C)'s activation group
   because its coefficient is nonzero. Conditional on C, each bit in the
   active group is positive with probability1/2 and all other groups are
   zero. Hence the joint distribution of V_j and the selector coordinates
   inside F cannot be independent of the remaining selector coordinates.
   This contradicts product factorization. Therefore F contains every
   selector coordinate.
4. Each body's factor contains these same selector columns, so all retained
   columns belong to one factor.

The same obstruction holds when the information filter uses **any subset**
of body axes. It always retains this prime identifying selector-plus-gate
core, together with equality queries for unselected body axes. Adding a
nonconstant response column to a prime identifying core cannot create a
new independent factor: its value is already determined by the complete
core word. Thus every such retained relation is again one identifying prime
factor. This is a failure of this particular response-family discovery
step, not a claim that all information-based algorithms fail.

On the actual all-body-zero incumbent slice, gates and selector equalities
both have minority1/M. The chosen priority makes a gate the first source
query. Its physical response still depends on body values globally. The
source is therefore not the pure selector projection needed by the earlier
completed-selector replay theorem.

## 3. Root's polynomial whole-component partition repair

At each distinct supplied response cardinality B, build a graph whose
vertices are actual response cells of size B, with an edge exactly when two
cells are disjoint. For every **whole connected component**, check whether
its cells are pairwise disjoint and their union is H. Retain all queries
from accepted components at that one cardinality, build their actual partial
greedy code, and complete every exit with fresh greedy or pruned incumbent.
Trying every cardinality is polynomial. This does not solve maximum clique,
arbitrary exact cover, or a search over subfamilies of one component.

For the XOR family, take B=n/M. Its cells are precisely selector-equality
positives and gate positives. The connected components have an exact form:

* The M values of one selector coordinate form a clique partitioning H.
  Different selector axes have intersecting cells and no graph edges.
* No selector cell is disjoint from a gate. Fixing one selector value leaves
  another nonzero-coefficient variable free to meet the activation group,
  and its body value is free to make the desired encoded bit positive.
* Gates from different bodies intersect. Their two f forms are independent,
  so any two activation groups have a common context; independent bodies
  can make both encoded bits positive.
* Within one body, different activation groups are disjoint, whereas bits
  in the same group intersect. Its gates therefore form one connected
  complete multipartite component. With at least two bits it is not
  pairwise disjoint. With only one bit it is disjoint but covers only half
  of H. Either way it is rejected.

Thus this whole-component rule accepts **exactly the selector axes**. The
partial greedy code using their union has full selector fibers as exits and
mean work k e(M). Fresh completion uses ell(b-1) body queries because at a
known context each body's one active palette is a complete binary cube code.
The code (3) is actually generated. No outsider replay argument, supplied
activation membership query, or inferred hidden-factor independence is used.

For completeness entropy gives OPT>=log2 n. All oriented positive supports
are at most n/R, and n/R>1, so the all-negative path also gives
`OPT>=(R+1)/2`. The exact class comparison is therefore

    output/OPT <= U/max(log2 n,(R+1)/2).                   (4)

For fixed k,c and the growing ell, entropy alone makes this at most
`1+k/(2c)+o(1)`. For k=2,c=1 the repaired class guarantee is2+o(1).
These are subclass statements; the component rule has no general guarantee
of finding a useful partition, and it deliberately never searches inside a
component that fails the whole-component check.

## 4. Bounded executions and strict limitations

`research-general-xor-aliases.py` performs three deterministic table checks:

| M,k,ell | n | m | Initial raw | Completed body-zero lift | Component comparison |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4,2,2 | 64 | 16 | 404 | 430 | 416 |
| 4,3,2 | 256 | 20 | 2192 | 2296 | 2240 |
| 8,2,2 | 1024 | 40 | 12296 | 13492 | 13056 |

Every query's exact joint-body contingency counts are checked, and the
information-retained words remain all n distinct. The existing exact
polynomial factorizer confirms one prime factor on the n=64 and256 retained
relations (584 and1376 entropy-oracle calls). Its larger n=1024 factorization
is covered by the analytic proof rather than a repeated expensive run.
All three component graphs accept exactly their k selector partitions and
their actual completed codes obey (3). The displayed component comparisons
can be more expensive than greedy at these small parameters; an algorithm
retains the cheaper incumbent. Their asymptotic constant guarantee comes
from (3)-(4), not a finite improvement claim.

The body-zero source is globally replayed with **actual fresh/pruned minimum
fallback at every exit**; each listed completed lift is worse than its
incumbent. These facts do not prove that some other conditional source,
verification policy, weighted source, or quadratic/actual-boundary state
optimizer fails. None of those full strong fixed points was computed here.
The component repair already prevents an asymptotic obstruction to the
expanded menu containing it.

The substantive new boundary is that exact individual independence can
leave a prime, fully identifying camouflaged relation. At the same time,
the positive-cell intersection geometry can reveal useful partitions even
when entropy factorization cannot. A surviving family would also have to
connect or disguise these selector partition components while controlling
new large-support tests and their conditional code lifts. That problem
remains open here.
