# Discovering a matroid certificate from response cells

Auxiliary research note, 19 October 2026. The article is unchanged. This is
a polynomial certificate-discovery result, not an unrestricted approximation
improvement.

The earlier [rank-coding note](uniform-decision-tree-lower-bounds.md),
Sections 10–11, already proves the rank-limited coding recurrence and its
Bellman potential. The [information note](research-general-information-next.md)
already uses supplied linear/affine representations to certify a positive
answer budget. The contribution here is recognizing a suitable matroid
directly from an explicit family of response cells, and trying a polynomial
menu of such families without being supplied any representation.

## 1. A verifiable certificate

Consider an identifying binary response matrix on a ground set E of n
hypotheses. A candidate certificate lists a nonempty family C of proper
subsets of E. Verify the hyperplane axioms:

1. No two distinct members contain one another.
2. For distinct A,B in C and x outside their union, some member of C
   contains (A intersect B) union {x}.

These are the standard finite-matroid hyperplane axioms; see Proposition
0.3.14 of [Finschi's research thesis](https://finschi.com/math/publ/2001-08-31_Finschi_A-Graph-Theoretical-Approach-for-Reconstruction-and-Generation-of-Oriented-Matroids.pdf).
Their direct verification is polynomial in the explicit family size.
Define cl(X) as the intersection of listed hyperplanes containing X,
or E if there are none. Require cl(empty)=empty, excluding loops.
The resulting closure is a matroid closure. Greedily adding elements outside
the current closure computes ranks in polynomial time.

Finally, require that every original test has at least one response cell
which is a flat: cl(C)=C. Orient that cell as the positive response. This
condition is checked for all original tests, including any added noise
tests. Constants cause no difficulty: choose their empty response.

An identifying matrix satisfying this condition forces the matroid to be
simple. Parallel elements belong to exactly the same flats and therefore
could not be separated by any original test. In particular, every nonempty
rank-one subset is a singleton.

**History certificate.** At an actual proper split of S, its positive child
S+ has strictly smaller rank than S; its negative child S− has no larger
rank. Indeed, S+ lies in the chosen flat C. Equal ranks would imply
S is contained in cl(S+), hence in C, contradicting S− nonempty.
Thus a proper root-to-singleton path has at most r(E)−1 positive answers.
This statement holds after arbitrary negative responses, without assuming
that a current state is itself a flat.

## 2. A polynomial discovery menu

For every cardinality B appearing among original proper response cells,
form the family of all such cells of size B. Apply the verifier above to
each family and retain the accepted certificate of minimum rank. There
are at most n−1 families and at most 2m cells in any family. No search over
subfamilies or embeddings is performed.

This menu need not find every possible certificate. An explicitly supplied
mixed-size hyperplane family can still be verified. Failure to discover a
certificate says nothing about the optimum decision tree.

On all affine-hyperplane membership queries in F_Q^d, the B=Q^(d−1)
family is exactly the affine matroid's hyperplane family. It discovers rank
d+1 from the response matrix alone. Adding every singleton-membership
query preserves this certificate, because singleton cells are flats. The
literal response-column rank becomes n, illustrating the distinction from
the earlier linear-rank extraction.

Conversely, a genuinely nonflat query can invalidate the certificate. On
AG(2,3), adding the four-point cell with mask 15 makes the rank-three
candidate fail; with singleton noise the detector returns only the weak
free-matroid certificate of rank nine. The test-by-test flat check cannot
be omitted.

## 3. The existing coding bound becomes available automatically

Use the earlier recurrence, with infinite entries understood:

    M_d(0)=M_d(1)=0,  M_0(s)=infinity for s>1,
    M_d(s)=s+min_(1<=a<s) [M_(d−1)(a)+M_d(s−a)].

Its table through budget r(E)−1 and size n takes O(r(E)n²) arithmetic
operations and polynomial bit complexity. The automatically discovered
certificate gives

    F*(E) >= M_(r(E)−1)(n).

The stronger statewise form is

    Phi(S)=M_(r(S)−1)(|S|),

with value zero on empty sets and singletons. Monotonicity of M in the
budget and the positive-child rank decrease show

    Phi(S) <= |S|+Phi(S+)+Phi(S−)

for every supplied proper query on every subset S. This is the old coding
potential, now evaluable through the recognized closure.

Neither this recurrence nor the statewise inequality is claimed as new.
The [history-potential note](research-general-history-potential.md) gives
the new algorithm integration and a sharper conditional contraction bound.

## 4. Negative drops are real

Take the direct sum U_(2,8) plus one independent point x. Its hyperplanes
are the eight-point line L and the eight pairs {x,a}, a in L. Membership
in L is a legal flat query, but

    Phi(E)=M_2(9)=30,
    Phi(L)=M_1(8)=35,  Phi({x})=0.

Its signed potential drop is −5. Conditioning has activated a harder
singleton-search problem. All-subset Bellman validity allows this. Clipping
the drop to zero would corrupt a telescope. The mixed-size family is
verified directly; it is outside the cardinality-only discovery menu.

## 5. Finite verification and limits

[The checker](research-general-matroid-discovery.py) passes 984 closure
checks, 21,241 actual-subset rank-drop and Bellman checks, 63 closure-exchange
checks on five accepted small candidate families, the nonflat decoy, and
the explicit negative-drop example. Exhaustive subsets occur only in this
finite audit.

| Q,d | n | Discovered rank | Lower bound | Greedy cost | Certified ratio |
| --- | --- | --- | --- | --- | --- |
| 2,2 | 4 | 3 | 8 | 8 | 1 |
| 2,3 | 8 | 4 | 24 | 24 | 1 |
| 3,2 | 9 | 3 | 30 | 30 | 1 |
| 3,3 | 27 | 4 | 132 | 135 | 45/44 |
| 5,2 | 25 | 3 | 136 | 140 | 35/34 |

All cases include singleton-test noise. These are a posteriori certificates
on the stated examples. They do not establish a universal approximation,
a constant bound for arbitrary matroid-flat systems, or a partial-policy
completion price from rank alone.

Run `python research-general-matroid-discovery.py`; exact results are saved
in [JSON](research-general-matroid-discovery-results.json).

## 6. Extension to any fixed response bound K

The binary statement has a direct extension, with a stronger flat condition.
For each original test, require **all but at most one** response cell to be
flats. Designate the possible exceptional cell as the default response. If
every cell is a flat, designate any one as default. The earlier hyperplane
verifier and cardinality-family discovery menu are otherwise unchanged.
Requiring just one flat response would be insufficient when K exceeds two.

At a proper query every nondefault child has smaller actual-state rank, and
the default child has no larger rank. Parallel hypotheses still cannot be
distinguished: every flat nondefault response contains both or neither, hence
so does the remaining default cell. Thus the same simplicity and positive
answer budget conclusions hold.

Let M_d^K be the minimum abstract coding cost with at most d nondefault
responses on every root-to-leaf path. Its recurrence partitions s among one
default child with budget d and at most K−1 children with budget d−1:

    M_d^K(s)=s+min [M_d^K(a0)+sum_(i=1)^(K−1) M_(d−1)^K(ai)],
    sum_i ai=s, with at least two nonempty children.

Use the same zero/singleton bases and impossible-budget convention. A
min-plus convolution for the K−1 nondefault children, tracking their number
of nonempty cells truncated at two, computes a table in O(K r n²) arithmetic
operations. The default has size below s at a proper query, so increasing s
is an acyclic order. The state potential M_(r(S)−1)^K(|S|) has the same signed
Bellman proof and fits the same activation ledger.

The checker implements the generalized recurrence and response-flat check.
For genuine ternary linear-form tests on F_3^d, d=1,2,3, it obtains exact
root values dn, matching the coordinate code and the ternary information
bound. It checks actual-subset rank decreases and Bellman inequalities,
rejects a response partition with two nonflat cells, and verifies that K=2
reproduces the earlier binary table exactly. The executable palette callback
and product-resource examples in the companion implementation remain binary;
the constant-K certificate theorem does not claim that code was generalized.
