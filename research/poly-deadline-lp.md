# Deadline interval LP: a fractional feasibility obstruction

This report addresses the proposed polynomial route through exact feasibility
of interval stabbing with deadlines.  The natural time-indexed feasibility LP
is **not integral in feasibility**, even on six candidate points.  This is an
obstruction to that particular exact-LP route, not a hardness proof for deadline
stabbing and not a lower bound on all polynomial decision-tree approximations.

## Formulation

For candidate points `1,...,M` and time slots `1,...,T`, let `x[p,t] >= 0`.
The LP requires at most one unit per slot, at most one unit per point, and

\[
\sum_{p\in[l,r]}\sum_{t\le d}x_{p,t}\ge1
\]

for each demand `([l,r],d)`.  The integer problem chooses distinct candidates
in order, with each interval hit by its deadline.

## Six-point, five-slot counterexample

Use the following ten demands.

| Interval | Deadline |
|---|---:|
| `[1,1]` | 4 |
| `[1,2]` | 2 |
| `[2,5]` | 2 |
| `[2,3]` | 3 |
| `[3,3]` | 5 |
| `[3,4]` | 3 |
| `[4,5]` | 4 |
| `[4,6]` | 1 |
| `[5,5]` | 5 |
| `[6,6]` | 3 |

Place half a unit on each listed candidate in the indicated slot:

| Slot | Candidates receiving `1/2` |
|---:|---|
| 1 | 4, 6 |
| 2 | 1, 2 |
| 3 | 3, 6 |
| 4 | 1, 5 |
| 5 | 3, 5 |

Every slot has mass one.  Point totals, in spatial order, are
`(1,1/2,1,1/2,1,1)`, so point capacities hold.  Each of the ten demand
constraints has left-hand side **exactly one**.  Thus this is an exact rational
feasible solution, independent of numerical optimization.

## Elementary integer impossibility proof

The singleton demands force candidates `1,3,5,6` into the first five slots.
Consequently at most one of candidates `2,4` can occur there.

If candidate `2` is absent, `[1,2]` forces `1` by time 2 and `[2,3]` forces
`3` by time 3.  Candidate `6` must also occur by time 3.  The first three
slots are therefore exactly `1,3,6`.  The deadline-one demand `[4,6]` forces
`6` first.  At time 2, `[1,2]` then requires `1`, while `[2,5]` requires
`3`.  This is impossible.

If candidate `2` is present, candidate `4` is absent.  The demand `[3,4]`
forces `3` by time 3, the singleton `[6,6]` forces `6` by time 3, and
`[1,2]` forces either `1` or `2` by time 2.  The deadline-one demand
`[4,6]` forces `6` first.  Both deadline-two intervals then force `2`
second, and `3` is third.  The deadline-four demands `[1,1]` and `[4,5]`
require both new candidates `1` and `5` in the single remaining fourth
slot.  This is impossible as well.

## Exact dilation gap

The best possible common deadline dilation for this example is `6/5`.
For a dilation smaller than `6/5`, all five integer deadlines remain unchanged
after flooring, so the impossibility proof applies.  The order

\[
(4,2,6,1,3,5)
\]

meets every deadline except `[5,5]`, which is hit at time 6 instead of 5.
It therefore attains dilation `6/5`.  The LP attains dilation one.
This rules out lossless rounding, but leaves rounding factors above `6/5`
open as an algorithmic direction.

## Transfer to full-edge block demands

The obstruction persists when every interval must have length at least two,
as happens when positive vertex patterns are expanded to incident hull-edge
blocks.  Replace candidate `p` by two consecutive twins `2p-1,2p`, and
replace `[l,r]` by `[2l-1,2r]`.  Put each original fractional mass on one
twin.  Any integer schedule of twins projects to a schedule of original
candidates; deleting repeated projected candidates only moves first hits
earlier.  Thus a feasible twin schedule would contradict the original
impossibility.  All new intervals have length at least two.

For block candidates indexed along a hull arc, the expanded block interval
`[a,b]` corresponds to the positive vertex interval `[a+1,b]`: its incident
edges are exactly the block indices `a,...,b`.  Additional unused hull
vertices can make these arcs shorter than half a cycle, allowing strict
regular-polygon realizations.  This transfer is combinatorial; it does not
by itself provide a decision-tree hardness reduction.

## Verification and search method

`poly-deadline-lp-check.py` generates rational fractional solutions as convex
mixtures of query orders, inserts every interval at its earliest fractionally
covered deadline, and tests integer feasibility by exact subset dynamic
programming.  The targeted search found a 12-candidate example after more
than 9,000 feasible fractional instances, which was simplified to the above
six-candidate instance.  The exact certificate routine checks all ten LP
constraints using `Fraction`, all 720 candidate permutations, and the ten
constraint-deletion cases.  Removing any one of the ten demands yields an
integer-feasible instance.  The independent phase-I oracle in
`poly-schedule-lp-check.py` also confirms fractional feasibility.

The nearby graph formulation remains useful: demands are vertices of a
cointerval graph, with edges between disjoint intervals.  Query ranks give
a proper coloring from prefix lists `{1,...,d(I)}`.  Conversely, each color
class is a pairwise-intersecting family of intervals, hence has a common
candidate point; this constructs the query schedule.  Exact polynomial
feasibility would need a separate combinatorial algorithm or a stronger
relaxation, rather than integrality of the displayed LP.
