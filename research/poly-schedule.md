# Polynomial scheduling audit for the general planar problem

Prepared 13 October 2026. This report concerns supplied binary unit-cost
line queries, general finite planar hypothesis sets, and both maximum and
arbitrary-prior expected depth. It does not establish a new maximum-depth
approximation factor. The expected-depth block improvement is developed in
`poly-expected.md` by the other agent and is consistent with this audit.

## What can and cannot be made polynomial immediately

The quasipolynomial baseline uses a vector containing one selected count
and one last selected spatial position for every deadline grade. A fixed
number of grades is polynomial, but a multiplicative grade spacing bounded
away from one still gives Theta(log n) grades. Dropping intermediate grades
without a replacement rounding theorem loses simultaneous deadline
feasibility. Exact maximum coverage separately for each budget supplies no
compatible sequence of prefixes.

The adjacent-block polynomial expected algorithm is nevertheless a real
improvement. An exit in block rank k has complete discovery-plus-endpoint
allowance at most 2k+3, plus conditional pattern entropy. Therefore the
geometric batch ordering can be applied to blocks and analyzed with

    W_stage <= 2 MSSC_blocks + 3 b + 2 p0 K + residual entropy.

Relative to a comparison first-supporting rank t, its positive term is
2 Phi_beta(t)+3. Since Phi_beta(t) = lambda_beta t + eta_beta - g_beta(t),
this is

    2 lambda_beta (t-1) + 3 + 2 Phi_beta(1) - 2 g_beta(t).

The existing capped early-mass argument applies to the increasing saving
profile 2 g_beta(t), with each analytical support block's new mass at most
2 delta. The zero route retains saving 2/ln beta. These details support the
other agent's polynomial factor near 5.31351; the bare raw endpoint
allowance must not be mistaken for the final cap-discounted coefficient.

## The maximum-depth greedy coefficient three is tight

The current maximum-depth algorithm forces an adjacent pair, then gives
every demand with block deadline d^(j) auxiliary weight M^(r-j). It uses
maximum-remaining-weight greedy on individual hull vertices. The bound
g_A <= 3 d_A - 2 cannot be improved by refining the adjacent-run counting
argument. The following infinite family makes every relevant greedy
choice strict.

After the forced pair, arrange k adjacent pairs P_1,...,P_k in a line,
with a single gap candidate g_i between P_i and P_(i+1). Thus this line
has 3k-1 candidates. Every vertex in every P_i has a singleton demand
with deadline k+1. For each gap g_i, add four demands: the interval from
each of the two vertices of P_i to g_i, and the interval from g_i to each
of the two vertices of P_(i+1). Give all four deadline i+2, where i starts
at one. The comparison order is the forced pair followed by P_1,...,P_k.
Every demand meets its deadline in this comparison.

Choose M larger than the total demand count. At the first remaining
step, g_1 hits all four earliest-deadline intervals, whereas either
neighboring pair vertex hits at most two, with all later scores too
small to reverse that strict comparison. After g_1 is queried negatively,
the same argument applies to g_2, then g_3, and so on. At the final gap,
the gap has score four and each adjacent pair vertex score at most
three, even though singleton demands now have the same priority.
Consequently greedy selects all k-1 gaps first. Every one of the 2k
singleton demands remains, so all 2k pair vertices must be queried
afterwards. Including the forced pair, the last singleton's first-hit
rank is

    2 + (k-1) + 2k = 3k+1 = 3(k+1)-2.

This is exactly the manuscript's deadline bound for the specified
forced pair. It is a barrier to improving that scheduling lemma by its
adjacent-run accounting alone, not a barrier to every algorithm that
enumerates different first pairs. The full decision-tree algorithm's
height allowances impose additional relations on its deadlines, which
this generic deadline construction does not establish. This is not an
inapproximability theorem for the decision-tree problem.

The interval family is planar realizable. Put the candidates at the
vertices of a regular (3k+1)-gon in normalized query space and use the
origin as witness. Every pattern above is a consecutive arc with at most
three vertices, so a strict half-plane cut realizes it. For each P_i,
include the normalized midpoint of its hull edge as an original query;
slightly increase the radial location of each singleton and two-vertex
arc hypothesis so that the relevant edge-midpoint query hits it too.
This change preserves the strict hull pattern. Include an all-zero
origin hypothesis and a singleton pattern on a forced vertex. Every
supplied query's cap is bounded by a constant while the hypothesis
count grows as 6k-2, so the family is count-flat for all sufficiently
large k. The script checks this last condition for the actual supplied
midpoint queries as well as the hull vertices.

## A concrete polynomial feasibility question worth investigating

One direct LP relaxation of nested interval deadlines is

    x[p,t] >= 0;
    sum_p x[p,t] <= 1                 for each time t;
    sum_t x[p,t] <= 1                 for each spatial candidate p;
    sum_{p in I, t <= d(I)} x[p,t] >= 1  for every interval demand I.

An integral feasible solution is a legal deadline schedule. The model
has a polynomial number of variables and constraints, but **fractional
feasibility does not imply integer feasibility**. The independent LP
agent subsequently found and exactly verified a six-candidate,
five-slot counterexample, documented in `poly-deadline-lp.md`.
Consequently this LP cannot immediately turn the quasipolynomial
baseline into a polynomial algorithm. A strengthened formulation or
a quantitative deadline-dilation rounding theorem is needed.

The LP's matrix is not automatically totally unimodular just because
the spatial demands are intervals: a demand row is a spatial interval
times a time prefix. For example the three rows [1,2] by time 2,
[2,3] by time 2, and [1,3] by time 1, restricted to columns
(1,1),(2,2),(3,1), give a determinant-two triangle matrix. This does
not refute integral feasibility for the special right-hand sides, but
it rules out the simplest consecutive-ones proof.

There is also a useful graph reformulation. Form the co-interval graph
whose demand vertices are adjacent exactly when their intervals are
disjoint. Assigning each demand its first hitting rank is a proper
coloring with permitted colors {1,...,d(I)}. Conversely any such coloring
gives one common stabbing point per color class, by the interval Helly
property; repeated points may be suppressed and colors compacted.
Thus deadline feasibility is prefix-list coloring of a co-interval graph.
The graph equivalence is proved here; it does not establish polynomial
complexity. Classical clique-cover integrality is insufficient because
it has no color/deadline dimension. The distinction is visible in
[Delle Donne's thesis, Section 6.2.3](https://bibliotecadigital.exactas.uba.ar/download/tesis/tesis_n6096_DelleDonne.pdf),
whose co-interval polyhedral result concerns the classical independent-set
formulation.

The initial computational search found no fractional-feasible/integer-infeasible
instance among 20,000 random cases with four to eight spatial candidates
and two to five time slots. The later six-candidate counterexample shows
why these random tests were insufficient. The checker uses floating-point phase-I simplex;
all integer feasibility decisions use exhaustive permutation enumeration.
The independent agent's counterexample now has an exact rational
certificate and exhaustive integer verifier. Cloning every original
candidate into two consecutive twins transfers that obstruction to
full-edge block demands: replace interval [l,r] by [2l-1,2r], whose
length is at least two. Fractional feasibility is preserved. Any integer
schedule projects to the original candidates, and suppressing duplicate
twins only improves all deadlines, contradicting original infeasibility.
These expanded intervals are exactly the incident-edge sets of positive
vertex intervals, so minimum block-demand length does not repair
integrality.

## Verification

`python poly-schedule-check.py` passed 39 exact combinatorial schedule
checks, for k=2,...,40, and 13 strict planar realizations, for k=8,...,20.
`python poly-schedule-lp-check.py` ran the targeted 7,500-case portion of
the LP search; the earlier 12,500-case search also found no fractional-only
instance. These experiments validate the stated tight family and identify
the LP question; they do not improve the maximum-depth theorem.
