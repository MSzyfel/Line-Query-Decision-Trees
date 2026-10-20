# Independent audit of affine-cover support pruning

Auxiliary review, 19 October 2026. This audits
`research-general-linear-selectors.py` without editing it or the article.
No defect was found in the RREF support calculation, preservation of legal
partitions, or the one-bridge recovery argument. This gives a repair of that
specific portfolio obstruction, not an unrestricted approximation theorem.

## 1. The exact object computed by elimination

For actual same-size response cells C_q, the incidence system is A x=1.
Every true response partition supplies a zero/one solution, so a column zero
in **every real solution** cannot belong to any true partition. Removing it
is safe. The converse is not claimed: real affine support need not give a
nonnegative solution or a legal partition. For example all four three-point
subsets of a four-point universe have the real cover x_q=1/3, but cannot form
a partition at that cell size.

The implementation's Gauss-Jordan rows are reduced in every pivot column.
Setting free coordinates to zero gives the displayed particular solution.
Setting one free coordinate to1 gives the kernel vector with pivot entries
the negatives of that free column's reduced coefficients. A pivot coordinate
is identically zero exactly when its particular value and every free-column
coefficient are zero. Every free coordinate is supported by its own kernel
direction. These are exactly the conditions used in `affine_cover_support`.
The inconsistent-system check is correct and safely returns no columns.

With audit enabled, the code checks both A x0=1 and A v=0 for every basis
direction against the original incidence masks. Its final support equality
therefore has an exact affine-space certificate. Rational Gaussian
elimination is polynomial in the listed matrix size and bit encoding:
entries and reduced fractions are ratios of integer minors of a zero/one
matrix augmented by ones, with polynomial bit length. No optimum decision
tree or real feasibility oracle is assumed.

Whole-component detection after pruning checks actual disjoint masks and
actual union H. The newly retained **whole pruned-column family** is also a
legitimate candidate response family; it need not itself be a partition.
Factor planning always uses its actual response support. Neither branch
interprets an arbitrary real affine solution as an executable query code.

## 2. Why the current single bridge is removed

At B=n/M the one-bridge instance's incidence equation is

    sum_i alpha_i(C_i)
      + sum_{j,g,u} beta(j,g,u) q(j,g,u)
      + delta q*=1.

Fix C and vary a target body bit. Outside the bridge support A*, the bridge
term vanishes and different ordinary body bits vary independently, forcing
the coefficient of each active ordinary gate bit to be zero. Every oblique
activation group has a context outside A*: it has a point with some selector
coordinate zero, because its linear form has another nonzero coefficient,
whereas every point of A* has all coordinates nonzero. Consequently every
beta is zero, not just the gates active at one particular context. With all
betas zero, varying the bridge's body bit at any C in A* forces delta=0.

Every pure selector column is supported by the genuine partition of its
own selector axis. Therefore affine support at B is **exactly** the pure
selector cells. Their whole disjointness components are the original axes,
and the repaired menu generates the selector-first comparison. This proof
holds for the half-alphabet asymptotic support and the smaller M=4 validator.

## 3. Independent bounded checks

I ran all96 families of nonempty equal-size cells on a four-point universe
(sizes1,2,3), with exact affine audit enabled. An independent enumeration of
coefficients in {-1,0,1} found52 signed integer exact-cover witnesses; every
nonzero witness column was retained. These include49 legal partition
witnesses, all preserved. This bounded enumeration is validation only.

I independently reran the actual n=64 bridge instance. Exact support pruning
and whole-component detection recover precisely its eight selector tests.
The full current extended portfolio, including the whole pruned-column
families, one independence refinement, factor planning, and depth-prize
pool recombination, returns400 from incumbent404 over21 selected families.
Direct hypothesis execution passes. The larger n=256/1024 recovery checks
were already run by root and were not duplicated in this audit.

## 4. Scope boundary for a possible next construction

Opposite balanced bridge pairs can remain supported in real covers. For
example q_i^+ and q_i^- supported on two values of selector i can sum to
those two pure equality cells, so replacing those cells by the opposite
pair is a genuine partition. Affine pruning must retain both. This can
break whole-component detection again. However retaining the **entire**
pruned family may expose a useful nonidentifying quotient, which whole-factor
planning can decode without wasting unrelated body variables. Root added
that family to the menu. No counterexample to that full strengthened menu
is established by the paired-bridge observation.
