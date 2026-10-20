# Balanced bridges defeat the current generic query-selector portfolio

Auxiliary research note, 19 October 2026. The article is unchanged. This is
a proved obstruction to the **specific complete portfolio** implemented in
`research-general-query-selectors.py`, including its factor planning and
depth-prize pool recombination. It is not an unrestricted approximation lower
bound and is not a fixed-point claim about the stronger conditional-source,
completed-lift, weighted, verification, actual-boundary, or quadratic-state
generator.

**Result.** Adding one balanced bridge query to the XOR-alias family produces
a deterministic growing family with the full greedy approximation gap. Every
family selected by the current root-minority/whole-disjoint-component menu
and its one independence-refinement level is either body-only, empty, or
prime and fully identifying. None of their factor plans improves greedy.
Their combined represented-state pool cannot improve it either. The actual
full implementation, rather than a simplified family menu, was run on three
bounded tables and agrees exactly with the analytic characterization.

## 1. XOR core and a balanced bridge

Use the construction in `research-general-xor-aliases.md`: M=2^b, R=M/2,
fixed k>=2, selectors C in F_M^k, and ell body rows Z_j in F_2^{b-1}. The
ordinary gates are

    [f_j(C)>>1=g] AND bit_u[Z_j xor (C_0>>1)],

where the distinct nonzero-slope Vandermonde forms f_j have every coefficient
nonzero and are pairwise independent. Every pure coordinate equality is
also supplied. Body equalities precede gates; gates precede selector
equalities. Each non-body query has root minority n/M, while body equality
minorities are2n/M. The selector-plus-gate core is already a prime identifying
response family, as proved in the XOR note.

Choose a selector support A* of size `2M^{k-1}` avoiding at least one value
of **every** selector coordinate. Choose a binary mask u on A* taking zero
and one equally often. Add the one physical bridge

    q*=1 iff C lies in A* and [bit_0(Z_0) xor u(C)]=1.       (1)

For the growing family M>=2^{k+1}, an explicit support avoids a whole half
of each alphabet:

    C_0 in {M/2,...,M/2+2^k-1},
    C_i in {M/2,...,M-1} for every i>=1.

Its size is `2^k(M/2)^{k-1}=2M^{k-1}`. Take u(C) to be the low bit of C_0;
the first coordinate set has equal parities. In particular, no point of A*
has any selector coordinate zero. The checker also uses a smaller M=4,k=2
validator: select eight nonzero-coordinate contexts and alternate their mask
bits. This satisfies the same balance/avoidance hypotheses but is not the
half-alphabet asymptotic construction.

**Exact independence condition.** For a bridge of form (1), independence of
the whole body vector follows exactly from a balanced mask on A*: for either
fixed value of the selected body bit, precisely half of A* satisfies (1).
Thus for every full body tuple z,

    Pr(q*=1 | Z=z)=|A*|/(2M^k)=1/M.                        (2)

The ordinary gates satisfy the same identity by the independent pair
(f_j(C),C_0). All non-body tests are individually independent of the entire
body vector, though their joint response vector identifies it together with
the selectors. Pure body equalities are not independent of their own rows.

Consequently initial greedy still identifies every body by pure equalities
before asking any other test. Its body mean is exactly ell e(R), where
`e(s)=(s+1)/2-1/s`; every available non-body minority remains1/M after any
body-equality history, while a remaining body equality has minority at
least2/M. The explicit selector-first code still has mean at most

    U=k e(M)+ell(b-1).

For fixed k,c>0 and `ell=floor(cM/log2 M)`, the bridge-augmented greedy tree
T has ratio `Omega(log n/loglog n)`, by exactly the earlier body-cost/cheap-
comparison argument. A single added test does not remove that gap.

## 2. Exact initial selected-family classification

The portfolio's minority cutoffs yield only the whole supplied query set
and the union of all body equalities. There are only the two distinct
minorities n/M and2n/M.

At response cardinality B=n/M, each pure selector axis formerly formed a
whole disjointness-graph clique partitioning H. The bridge positive cell is
disjoint from the zero-value cell of every selector axis, so it connects
all those cliques into **one** graph component. Cells belonging to two
different selector axes overlap, so this component is not pairwise disjoint
and is rejected by the exact whole-component rule.

There are no other accepted components at B. Each ordinary body-gate
component either joins this rejected component through the bridge, or
retains its earlier structure: with at least two bits it is not a clique,
and with one bit its union is only half of H. There is only one bridge, and
its component already contains all selector axes. Thus no new isolated
bridge component can be accepted.

At cardinality2B the accepted components are exactly the individual body
equality axes. Other positive test cells have size B. Negative non-body cells
have size n-B>n/2, and negative body cells have size n-2B>n/2 when M>4, so
their graph components are isolated and cannot partition H. At M=4 the body
complements duplicate the same binary-axis cells and add no new family.

Hence the complete initial family list used by `select_families` consists
of the whole query family and body-axis families: each individual body axis,
their union, and any duplicate union added by the implementation. This
includes its union of accepted components at a fixed cardinality and union
across cardinalities; none hides an extra selector family.

## 3. The one-level independence refinements add no useful factor quotient

The whole query family is prime and identifying: it contains the earlier
prime identifying selector-plus-gate core. Adding a nonconstant response
column cannot split an identifying prime factor, since that new response is
already a deterministic function of its complete core word. Its only factor
subsets are the empty subset and its full identifying factor. Independence
from those selects respectively every original query or no nonconstant
query.

A body-axis family factors into its genuine body coordinates. For any subset
J of those factors, exact original-hypothesis independence counts retain
precisely

    all non-body queries, plus equalities on body rows outside J. (3)

Every non-body query satisfies (2) even for the full vector. An equality on
a selected body coordinate is dependent on it; an equality on an unselected
coordinate is independent of the selected coordinates. The retained family
in (3) again contains the prime identifying core and is therefore one prime
factor with alphabet n. Empty selected subsets duplicate the whole family.

Thus **every actual selected family** is empty, body-only, or prime
identifying. This classification covers all subset refinements, not just the
whole-body choice. The implementation freezes the initial families and does
not recurse independence selection, as required by the portfolio audited
here.

## 4. Whole-factor plans and conditional test eligibility

For a prime identifying family, its contexts are H and the n singletons.
For all sufficiently large family members, `n>floor(log2(n+m+1))`. The
planner's public exact-alphabet limit is therefore below n. Its one-factor
decoder uses ordinary balance greedy on all original supplied tests, exactly
T, and every singleton continuation is free. These families add only T's
nodes and the singleton states to the pool. The empty family does the same.
This explicitly uses the implementation's size cap; no exponential exact
solver is being assumed.

For a body-only family, contexts fix arbitrary subsets of its body axes.
The ambient state remains a rectangle of body values times **all** selectors.
In `factor_decoder`, every non-body test is inconsistent on every live value
cell of a body factor. In fact (2) says that within each fixed complete body
tuple it takes both answers, with probabilities1/M and1-1/M. Fixing other
bodies or excluding some values of the current factor never makes that
test constant on a surviving value cell. Therefore the implementation's
conditional-eligibility feature cannot admit it later. Equalities on a
different unfixed body are likewise inconsistent on every value cell;
equalities on a fixed body are constant. Only equalities on the actual
decoded body factor are proper eligible tests.

This conclusion holds whether the local factor solver uses its allowed
small-alphabet exact DP or greedy. Both produce equality combs. Fresh greedy
on any body context also uses only body equalities until the whole body tuple
is known, by (2). Given the resulting tuple z, its remaining selector tree
is the same fixed-priority T_z appearing in T. The equality-only product
identity makes the mean body work ell e(R), independent of the adaptive
coordinate order, and the final expected T_z work is unchanged. Hence every
individual whole-factor plan has exactly T's cost, not merely at least a
conservative comparison bound.

## 5. Why depth-prize pool recombination cannot repair the plans

The preceding construction completely characterizes the union pool Q:

1. A state can be a body rectangle with all selector contexts present.
2. Once a full body tuple z is fixed, it can be a node of the original
   selector subtree T_z.

Zero is harmless. Singletons belong to the second category. Local exact-DP
states are added only when reconstructed into the chosen decoder, and those
are equality-comb rectangles; the implementation does not pool every subset
visited by that internal DP. Even pooling those subsets would remain within
category1 and would not change the argument.

At a category1 state containing at least two possible full body tuples,
each non-body query has both responses in **every** such body tuple by (2).
Each response has only a proper fraction of the selectors. Neither child
is a full-selector body rectangle, and neither fixes one full body tuple.
Thus neither response child belongs to Q. The represented depth-prize DP
cannot execute that query. Only pure body equality queries can continue
from such a state.

Within one full tuple z, all proper pool states are nodes of one laminar
binary tree T_z. Two disjoint proper descendant nodes can cover a parent
node only if they are its original two children. Hence any executable
query with both children in Q induces the original T_z split, possibly
with reversed responses or an equivalent test. There is no different
supported selector partition.

Complete any represented partial policy with the actual incumbent restricted
at every unfinished exit. It must identify bodies through pure equality
queries and then follow T_z for each resulting tuple. Stopping early and
using incumbent restriction has that same form. Its cost is exactly F_T by
the equality-only product identity. A positive incumbent-depth-prize profit
would imply a strictly cheaper such actual completion, which is impossible.
The exact represented profit is zero and `selected_context_pass(...,
independence=True,recombine=True)` returns T's cost.

This proves a full-order approximation barrier for this complete **specific
portfolio**, including pool recombination. It does not include adding global
code lifting, conditional greedy source libraries, verification paths,
quadratic intersections, or implicit boundary fallback moves to Q.

## 6. Actual bounded full-portfolio checks

`research-general-bridge-aliases.py` imports and executes the authoritative
`select_families`, `plan_factors`, and `selected_context_pass` functions. It
also checks exact joint-body independence, initial equality-only body work,
every selected family's factor type and individual planned cost, and the
structural classification of every pooled state.

| M,k,ell | n | m | Initial=portfolio raw | Selected families | Pool states |
| --- | ---: | ---: | ---: | ---: | ---: |
| 4,2,2 | 64 | 17 | 404 | 9 | 130 |
| 8,2,1 | 256 | 29 | 2546 | 4 | 512 |
| 8,2,2 | 1024 | 41 | 12270 | 8 | 2062 |

Every selected family's factor plan equals the incumbent. The n=1024 pool
contains29 full-selector body rectangles,2032 actual known-body selector
nodes, and zero states outside those categories (plus zero). Its run selected
two body partition components and summed4136 contexts across all families.
All three checks use the complete actual generic portfolio, including its
single independence refinement and final depth-prize optimization. They do
not stand in for the analytic proof or use any optimum oracle.

Results are saved in `research-general-bridge-aliases-results.json`. No run
is left active. A broader component-deletion or neighborhood partition menu
could remove or bypass a single bridge; that is outside this exact portfolio
and should be audited separately rather than inferred from this theorem.
