# Independent audit of branching/partition search

Auxiliary audit, 19 October 2026. Reviewed
`research-general-branching-partition.py` and its explanatory note. The
article is unchanged. No defect was found in the stated search class,
Bellman recurrences, or polynomial runtime argument.

## Search semantics and reconstruction

`MenuSearch.cut(S,t,B)` returns the cheapest program in its explicitly
stated class: stop immediately at population at most B; otherwise choose
fresh greedy stopped at B, or execute one menu macro with compulsory early
acceptance upon first reaching B and independently recurse at its exits.
The macro choice consumes one action level, not one original query.
Arbitrary pruning inside other macro interiors is not included. The note
states this distinction correctly.

`frontier(S,t)` includes every stopping prefix of fresh greedy as its
fallback. Other macros execute their fixed interiors and then attach
independently chosen child frontiers. The result maps each exact integer
collision value to minimum raw work within this class. Consequently
`collision_cut` correctly minimizes work over the returned values at or
below the requested budget. These statements do not compare the generated
class against unrestricted OPT.

The min-plus helper chooses minimum sums of child costs at fixed total
collision. Although it does not add the macro's own work while choosing a
child combination, that work is the same for every combination of the same
macro. `graft` then restores the entire original macro and its work. This
is correct. Every attached child is an actual original-test tree; no
synthetic response split is substituted.

## Runtime and partition claims

For an occurrence with population s, each candidate macro has disjoint
nonempty exits whose populations sum to s. At most b macros therefore
produce total child-occurrence population at most bs. Summing over one
action level gives at most n b^j population at level j and hence at most
that many nonempty occurrences. The bound remains valid for long macros
with n exits; no n^d factor is necessary. It assumes the small menu itself
is polynomially computable and explicitly executable, as stated.

Collision indices lie between s and s^2. Repeated convolution over a
macro's at most s nonempty exits adds only a fixed polynomial factor.
Keeping an actual witness tree per collision also adds a polynomial factor:
any proper binary partial tree on s hypotheses has at most 2s-1 nodes.
Thus constant b and logarithmic action depth give a polynomial algorithm,
including reconstruction.

The level-accounting argument for recursive maximum-size cuts is valid:
restrict one fixed global optimal tree to each state in a disjoint level,
and sum their raw costs. The power-shrink target and the collision-moment
sufficient condition consequently give O(loglog n) recursive levels, if
cuts with the asserted OPT-relative work can be computed. That conditional
coverage theorem remains unproved, as the note says.

The pure collision gain/work obstruction is also correct. For response
counts a_i, with A=sum_i a_i,

    g(a)=A-sum_i a_i^2/A,
    partial g / partial a_j
      =(1-a_j/A)^2+sum_(i!=j)(a_i/A)^2 >= 0.

Every restricted query has coordinatewise smaller response counts than the
same root query. A partial policy's total collision gain/work is the
work-weighted average of its local g values, so no such ratio exceeds the
best single root query. This does not rule out optimizing a fixed large
collision target.

## Independent bounded verification

The new checker `research-general-branching-search-audit.py` literally
enumerates all menu compositions and fallback stopping prefixes on bounded
instances, including all combinations of child policies. It independently
compares exact collision/work maps at action depths 0, 1, and 2. It covers
both the two one-query menu and a long full-greedy macro paired with one
query.

Results: 60 exact-frontier comparisons, 737 literal policies, and 266
reconstructed frontier witnesses passed. No unrestricted optimum oracle
is used. The results are saved in
`research-general-branching-search-audit-results.json`. The original
branching/partition checker was also rerun and passed its 24 size-target
comparisons, 69 moment-witness checks, and long-macro occurrence example.

This audit does not independently review the separate menu-partition LP or
its compiler; those are separate artifacts. The bounded executions verify
implementation details, while the general search guarantee follows from
the recurrences and counting arguments above.
