# Maximum-depth simplification and development

The verified approximation guarantee remains **4.46496526** in
deterministic polynomial time for general supplied planar line queries.
No smaller approximation factor is asserted in these edits.

## Manuscript edits

Owned and edited only:

- `sections/04-maximum-depth.tex`;
- `sections/06d-polynomial-slot-scheduling.tex`.

The reasoning now has three explicit interfaces:

1. **Count credit:** Lemma `lem:worst-floor-credit` isolates the one
   floor calculation shared by balanced steps and flat endpoint exits.
   The old equation label `eq:worst-floor-credit` is retained.
2. **Actual route height:** Lemma `lem:worst-local-height` states what a
   passing schedule certifies: discovery + legal endpoint decoder +
   the already constructed child. It also accounts for the zero singleton
   and omits an absent zero leaf.
3. **Unknown comparison to actual deadlines:** Equation
   `eq:slot-deadline-credit` gives
   `H - C_W(A) - z_A - 5 >= 2(t_A-1)` in the restricted induction.
   This ensures that the computed deadline meets the supporting-prefix
   comparison index. The comparison path proves existence; the scheduler
   never receives an optimal tree.

The rank-subset proof explains why original intervals wholly in the
current spatial region are exactly the unhit demands and why **absolute
rank subsets**, rather than just their cardinalities, retain arbitrary
interleaving of the left and right regions.

All existing labels, assumptions, approximation results, low-dimensional
cases, terminal nonzero singleton append, zero-route cap, exact floors,
fixed global threshold, reconstruction, and polynomial bit-complexity
arguments are retained. Redundant algorithm prose was removed where the
new local lemma already supplies the complete argument.

Suggested flow for the layout agent:

`flat hull data -> construct each child once -> record actual child heights`

`-> trial H -> {priority fallback, capped exact interval DP}`

`-> positive exits: endpoint decoder + stored child; negative exit: zero leaf`

The witness supporting-prefix path should be a separate dashed analysis
arrow to the deadline-feasibility statement, not an algorithm input.

## Verified further development: a smaller logarithmic cap

This is a running-time/state-space improvement preserving the factor.
The parent independently audited the argument and approved it. The
smaller cap is now integrated in `sections/06d-polynomial-slot-scheduling.tex`;
the layout agent is updating the colocated HybridTree recipe accordingly.

Let

\[
\gamma=246496526/10^8,\qquad
K=\frac{\gamma}{\gamma-1}=\frac{123248263}{73248263},\qquad
q=\lceil\log_2n\rceil.
\]

Replace `L=2q+1` by

\[
R=\lfloor Kq\rfloor,\qquad L=R+1.
\]

The universal invariant is unchanged. Prove the restricted invariant
when `D <= R`, rather than `D <= 2q`. Restriction preserves this same
global threshold in every child, and the comparison has at most `D+1`
blocks, hence fits `L`. The height cap `floor(H/2)` is unchanged and
still at least `D+1`, including the terminal append.

At the root, small optimum gives `(2+gamma)D` as before. If integer
`D > R`, then `D > Kq >= K log_2 n`, and

\[
\frac{C_W}{D}
\le 3+\frac{\gamma\log_2n}{D}
<3+\frac\gamma K=2+\gamma.
\]

Since `q < log_2 n+1`, the rank-mask contribution is now

\[
3^L < 3^{K+1}n^{K\log_2 3},\qquad
2^L < 2^{K+1}n^K.
\]

Exact rational logarithm certificates establish

- `K < 1.682611`;
- `K log_2 3 < 2.666874`.

Previously the corresponding exponents were `2` and
`2 log_2 3 = 3.169925...`. Other polynomial factors are unchanged.
The smaller cap can exclude individually favorable longer schedules,
so this should be presented as an optional cheaper implementation if
the intention is to retain every previous feasible trial. Keeping the
larger cap as an optional additional alternative retains that stronger
instance-wise behavior at its previous running time.

The floor is safe: `D > floor(Kq)` for integer `D` implies `D > Kq`.
No irrational parameter or logarithm comparison is needed to compute
`R`: obtain `q` by integer powers of two and take the floor of a
fixed rational multiple.

## Why numerical tuning does not lower the approximation factor

Within the current two-credit argument, the logarithmic coefficient
must meet

\[
\gamma\ge\max\left\{
1/\log_2(1/(1-\delta)),\ 5/\log_2(1/\delta)\right\}.
\]

The decreasing and increasing terms meet at
`delta=(1-delta)^5`; their minimum is approximately `2.4649652555`.
The current rational certificate is already within `5e-9` of this
minimum. Integer-floor tuning and changing the cap therefore do not
produce a material improvement of the factor. A smaller factor needs
a stronger structural lemma.

The whole-exit rectangle optimizer is useful algorithmically, but an
endpoint-only height aggregation cannot justify reducing the four-query
allowance. The existing heavy central cross has endpoint pairs
`(2,2),(1,2),(3,2),(2,1),(2,3)`, central continuation height 10, and
the others zero; every coordinate-threshold decoder has whole height 14.
Changing the discovery anchor can pin an endpoint and avoid this local
obstruction, which is why the promising missing lemma is **joint**:
choose anchors and compatible ranks together, while ensuring every
child continuation remains within the same trial height.

A potential route is to identify the classes with the tightest actual
continuation budgets and pin them using boundary blocks. The unresolved
step is proving that the resulting block ordering meets all other
deadlines simultaneously. Separate covers for each deadline do not
establish this. No unproved anchor or aggregate endpoint inequality has
been inserted into the manuscript.

## Verification

Read the existing check implementations and reran:

- `further-worst-slot-dp-check.py`: **3,900** linear and **1,200**
  circular instances against independent exact subset DPs; the known
  five-slot fractional obstruction and six-slot repair also pass.
- `further-worst-endpoint-check.py`: **1,200** weighted endpoint
  instances against full subset decision-tree recursion; the central
  cross requires four comparisons before the height-10 continuation.
- New `simplification-worst-cap-check.py`: exact rational certificates
  for the cap identity and the two exponent bounds, plus **10,000**
  integer rounding-boundary checks including the smallest cap.

No PDF build was run; the parent coordinates layout relocation and the
final compilation. All owned TeX files are ready to be handed to the
layout agent.
