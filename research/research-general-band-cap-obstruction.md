# Bounded-cap tests defeat every fixed balance band

Auxiliary research note, 19 October 2026. The article and earlier canonical
positive theorem are unchanged. This gives an explicit extra-query
obstruction to the proposed balance-band menu. It does not refute arbitrary
constant menus or logarithmic menu search in general.

## Construction and claim

Let M=2^p>=8, R=M-2, and L=floor(M/p). Use the uniform product

    H=[M] times [R]^L,      n=M R^L.

Supply the pure coordinate equalities and all canonical body-bit queries
gated on each selector value, as in the earlier positive example. Add every
THREE-ELEMENT membership test on each body coordinate. Thus a new query is
`Z_j in A` for a supplied A subset [R] of size exactly three. These are
original binary unit-cost tests. Their number is `L binom(R,3)`, polynomial
in the explicit input; indeed it is only polynomial in M.

Any algorithm constrained to ask queries whose current minority is at least
half the best current minority must identify ALL body coordinates before
asking any selector/gated query. Consequently every such tree has mean cost

    Omega(LR)=Omega(M^2/log M),

while a legal selector-first comparison costs at most

    e(M)+Lp=O(M),    e(s)=(s+1)/2-1/s.

Since `log_2 n=Theta(M)`, the approximation gap is
`Omega(log n/loglog n)`. The restriction includes both offerings of the
earlier two-query balance-band menu, their root-rarity refinement, every
adaptive composition of these choices at any search depth, and maximum-
balance greedy fallback. Offering MORE choices within that same band does
not help.

## Why every surviving body dominates the selector

Until a selector or gate is asked, the actual state remains a product
rectangle with all M selector values present. Suppose an unresolved body
has r>=2 surviving values. An available global triple can intersect its
surviving domain in

    t=min(3,floor(r/2))

values: for r>=6 choose three surviving values; for r=2,...,5 choose t
surviving values and pad the triple using excluded values. Padding is
possible because R>=6. Its current minority fraction is t/r. Therefore the
maximum body minority is at least

    min(1/3,3/R) > 2/M.

The `1/3` is necessary: at r=3 the largest possible minority is one third,
not one half.

Every selector equality has minority 1/M. Every private gate has positive
fraction at most 1/M, even if previous body tests have made its bit
constant one. Hence both have minority at most 1/M, strictly below half the
best body minority. Neither can appear in any half-best-balance menu while
an unresolved body remains. This inductively forces the whole body phase.

## Uniform bounded-cap identification costs linear work

All permitted queries during that phase act on a single body coordinate,
and their positive side has at most c=3 values of that coordinate. An exact
potential avoids assumptions about query ordering or interleaving. For a
body with r surviving values set

    phi(r)=(r-1)/(2c),       Phi=sum_j phi(r_j).

If a proper query separates a positive values from r-a negative values,
where a<=c, then under the actual uniform product posterior its expected
potential drop is

    phi(r) - [a phi(a)+(r-a)phi(r-a)]/r
       = a(r-a)/(c r) <= 1.

This applies to singleton and triple queries. The potential starts at
`L(R-1)/(2c)` and is zero once all bodies are known. Summing the conditional
expected drops proves that the expected work of the forced body phase is
at least

    L(R-1)/(2c).

This is additive over coordinates despite arbitrary adaptive interleaving.
No optimal-tree oracle, selector-label oracle, or geometric structure is
used by the algorithms being constrained.

## Any fixed balance-factor threshold has the same obstruction

Fix A>=1, and constrain every chosen query to minority at least beta/A,
where beta is the best current minority. Choose a fixed integer c>A and
add all c-element membership queries on every body. For sufficiently large
M satisfying R=M-2>=2c and M>3A, the same padding argument gives

    beta >= min(1/3,c/R) > A/M.

Selector and private-gate minorities at most 1/M therefore lie below the
entire admissible band. The cap-c potential gives body work at least
`L(R-1)/(2c)`, still a full-order asymptotic gap because A and c are fixed.
The number of added tests `L binom(R,c)` is polynomial for fixed c.

Thus lookahead must sometimes admit choices a superconstant factor less
balanced than the best available test, or use other sorts of long macro
choices. This is a statement about the restriction on PRIMITIVE choices;
a useful executable macro may contain such a temporarily unbalanced query.
It supplies no impossibility for a constant-size menu whose entries are
chosen by richer structural criteria.

## Checks

Run `python research-general-band-cap-obstruction.py`. Saved results are in
`research-general-band-cap-obstruction-results.json`:

- 4,237 actual body rectangles satisfy the strict exclusion inequality.
- All 158,228 admissible queries in their half-best bands are body tests.
- Three reconstructed deterministic band policies through 288 hypotheses
  have only body queries before the full body tuple is known; 413 internal
  nodes and their actual original-test execution are checked.
- 575 bounded-cap padding inequalities and 2,150 exact rational potential
  identities pass, including caps from two through six.

The small examples test the implementation and exclusion invariant. The
asymptotic cost gap follows from the potential proof, not from extrapolating
small-instance ratios.
