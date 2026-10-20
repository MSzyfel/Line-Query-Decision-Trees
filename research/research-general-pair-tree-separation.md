# Combining a pair potential and one tree: a fixed-query obstruction

Auxiliary research note, 18 October 2026. This concerns separation of a particular relaxation, not hardness of approximating uniform decision trees. It does not modify the article.

The pair cone and the weighted single-tree cone each have polynomial all-subset separation. It is tempting to assume that their sum does too. The following reduction shows that optimizing the capacity violation for one specified query is already NP-hard for their sum. It does **not** prove that separating the complete all-query LP is NP-hard: other supplied tests might provide easy violations.

## Statement and potential

Use a potential

    P(S)=sum_pairs 2 lambda_uv 1[u,v in S]
          + sum_internal_v w_v |S intersect H_v|
                         1[S meets both children of v].

All pair weights and tree-node weights are nonnegative and at most one. The hierarchy is one explicit legal binary identifying tree T. Given one specified supplied binary query q, deciding whether

    max_S {P(S)-P(S intersect q^-1(0))-P(S intersect q^-1(1))-|S|}>0

is NP-complete. Membership follows from an explicit subset witness. The proof below reduces strict-threshold MaxCut on a cubic graph; the standard degree-three hardness is documented in the [primary Alimonti-Kann paper](https://www.sciencedirect.com/science/article/pii/S0304397598001583).

## Copies and the coherent tree features

Let G=(V,E) be cubic, let e=|E|, and let C be a cut threshold with 0<=C<=e. Put epsilon=1/(24e). For every edge uv, make a disjoint triple consisting of a red anchor copy, a blue copy of u, and a blue copy of v. Query q separates red from blue.

Each vertex has three blue copies, one for each incident edge. Add three red auxiliary copies for it. The anchor has e red copies; add e blue auxiliary copies. Thus every variable group, and the anchor group, has p red and p blue copies. Different groups are disjoint.

Place each mixed edge triple below its own tree node that separates the anchor from its two endpoints. Give that node weight epsilon. Give all other tree nodes weight zero, including the endpoint-pair decoder. Unite the disjoint triples and auxiliary leaves under any binary hierarchy. Supplying its child-membership tests makes this T legal. These additional tests are the reason the theorem is scoped to the specified q rather than full all-query capacity validation.

Writing x_a,x_u,x_v for selected copies of one edge triple, its q-deficit is

    epsilon x_a(2x_u+2x_v-x_u x_v).                              (1)

The feature is part of one coherent hierarchy, not an arbitrary overlap of triple potentials.

## Pair groups enforce consensus

Within each group, put a pair between every red and blue copy. For a group with p copies of each color and prescribed residual selection cost c, set

    2 lambda = (2p-c)/p^2.

If S selects r red and b blue copies from it, its pair deficit minus its contribution to |S| is

    f(r,b)=-(r+b)+(2p-c)rb/p^2.                                 (2)

At (0,0) this is zero; at (p,p) it is -c. Every other integral choice has f(r,b)<=-1. To check the last assertion, drop the nonpositive term -c rb/p^2. On the rectangle r<=p-1, 0<=b<=p, the remaining bilinear function is maximized at a corner; the only zero corner is (0,0), and every other nonempty integral boundary is at most -1. The analogous rectangle b<=p-1 covers all remaining non-consensus choices.

For a vertex group set c_v=(3/2)epsilon deg(v)=9epsilon/2. For the anchor group set c_A=epsilon C/2. These costs are nonnegative and less than one, so every pair weight lies in [0,1].

The total positive tree contribution is at most 3epsilon e=1/8. Consequently any S with a non-consensus group has strictly negative total violation. A maximizing positive witness therefore selects either all copies or none of each group.

## Consensus is exactly a cut

Let U be the vertices whose groups are fully selected, and A indicate selection of the full anchor group. At consensus, (1), (2), and cubic regularity give total violation

    A epsilon(6|U|-e(U)) - (9epsilon/2)|U| - A epsilon C/2.

For A=0 this is nonpositive and is maximized by selecting no group. For A=1 it equals

    (epsilon/2) [3|U|-2e(U)-C]
      = (epsilon/2) [cut(U)-C].                                (3)

Thus the maximum violation is exactly

    max(0, (epsilon/2)(MaxCut(G)-C)),

and a positive violation exists exactly when MaxCut(G)>C. The construction uses 6e hypotheses, O(e^2) pair coefficients, O(e) tree nodes, and polynomial-size rational numbers.

## Verification and implication

The certificate agent independently audited the algebra and the consensus bound. research-general-pair-tree-separation.py checks every subset on small edge, path, and triangle constructions at all thresholds: 1,060,992 subset/threshold cases in total. It verifies both the exact maximum in (3) and strict negativity for every non-consensus selection.

The checks validate the reduction identities; the asymptotic hardness follows from the reduction and the cited MaxCut hardness. This does not imply any new approximation hardness for the decision-tree problem, nor establish hardness of separating the all-query combined cone. It rules out treating the two existing per-query polynomial separation algorithms as automatically composable. A resource portfolio can choose the larger separately computed lower bound without encountering this joint optimization; the quality of that portfolio is a separate open question.
