# Logarithmic exact prefixes for arbitrary-prior expected depth

This supplements the accepted general polynomial bound **<5.272565**. It
does not replace that bound by a smaller uniform factor. There is a valid
polynomial algorithmic improvement using the new rank-subset DP, and a
specific obstruction to transferring the worst-depth cap argument directly.

## A weighted prefix objective that the DP optimizes exactly

Let the circular hull-edge candidates be numbered spatially, and let each
positive full-pattern class A have block-hit interval I_A and mass w_A.
Fix a prefix cap K and a legal completion tree B on the entire current
state. Write

    b_A = sum_{h in A} pi_h depth_B(h).

These are unnormalized weighted costs. Give A any fixed, legal weighted
positive-exit continuation allowance g_A. For example, choose a legal
pattern decoder for each first-hit block in advance, followed by the stored
class tree; a block-dependent allowance g_{A,p} is equally permissible.
One may instead use the stronger local decoder costs discussed below.

For a selected schedule P of at most K distinct blocks, let t_A(P) be its
first-hit rank. Optimize the rational objective

    U_K(P) = sum_{A hit} [2 t_A(P) w_A + g_{A,p_A}]
             + sum_{A unhit} [2 K w_A + b_A].             (1)

The all-zero class, when present, is always unhit and contributes
2 K w_0+b_0. Crucially, an unhit class pays for **every** executed prefix
block. The factor 2K is a conservative allowance when fewer than K blocks
are selected; it remains valid after unused ranks and constant queries are
suppressed. The algorithm enumerates K=0,...,L, so this conservatism does
not force an unnecessarily long prefix.

After all prefix answers are negative, restrict B to the unresolved union
R and contract its constant queries. Its weighted continuation cost is at
most sum_{h in R} pi_h depth_B(h), precisely the additive b_A term in (1).
If a positive block occurs, use the selected legal pattern decoder and the
stored class tree. Thus (1) is an upper bound on the actual expected cost
of a concrete supplied-query tree. All costs in (1) can be rational: actual
finite-tree depths, rather than entropy expressions, suffice.

For a linear candidate region [l,r], let I(l,r) be the **original** demand
intervals wholly contained in it. For a rank mask T subseteq {1,...,K}, use
a state V(l,r,T). A stop transition costs

    sum_{A in I(l,r)} (2K w_A + b_A).

Otherwise set t=min T, choose a candidate p in [l,r], and charge

    sum_{A in I(l,r), p in I_A} (2t w_A + g_{A,p}).

Partition T minus {t} into disjoint masks T_left,T_right, and add
V(l,p-1,T_left)+V(p+1,r,T_right). Take the minimum over stop, p, and the
mask partition. A state with no ranks must stop. A region with no contained
demands has cost zero and needs no selected points.

The recurrence is exact for (1). Earlier selected points form the ancestors
of the schedule's spatial Cartesian tree. An interval survives these
ancestors precisely when it is wholly inside the current region. Every
surviving interval containing p first meets p; every other survivor lies in
one child region. Moving the first used rank to min T cannot increase the
rank cost, and miss penalties do not depend on unused ranks. Conversely,
the selected points reconstructed from every recurrence form a legal
schedule, ordered by their absolute ranks. Missing ranks can be compressed.

Circular intervals require enumerating the first selected point p, removing
its hit demands, cutting the circle at p, and running the linear recurrence
with the remaining absolute ranks {2,...,K}. Include the no-query option.
This adds one factor M to the linear running time

    O(poly(M,N) 3^K), with O(M^2 2^K) states.

Hence L=ceil(c log_2 n), for any fixed c, is polynomial in the original
instance size and prior bit length. There is no inverse-minimum-probability
dependence. Selecting the best actual output tree among these prefix
constructions and the existing <5.272565 algorithm preserves the certified
global guarantee and can improve individual instances.

## Stronger local positive exits remain additive

The fixed g_{A,p} version above suffices for the exact theorem. More
generally, a transition may have a precomputed rational total exit cost
G(l,r,p) for all newly hit classes in the current region. The recurrence
then charges 2t times their total mass plus G(l,r,p). Its proof and rank-mask
complexity are unchanged.

This permits the manuscript's polynomial endpoint-rectangle DP, with
stored weighted class continuation costs as terminal costs, to price the
whole positive exit. Ancestor-negative blocks leave exactly the original
pattern intervals contained in [l,r]; other queries interleaved outside
this region cannot hit such a pattern. Thus the compatible class sets and
their endpoint restrictions depend only on [l,r] and p. Query both endpoints
of p, divide into the possible nonzero answer cells, and optimize each
legal coordinate-threshold decoder. Charging two queries per earlier block
and two queries for the current block is conservative; cached queries can
only improve the actual tree. Every precomputed decoder is an actual
supplied-query tree, so its weighted cost is rational and checkable.

This extension optimizes a conservative complete positive-exit allowance,
not the unrestricted optimum identification tree. It avoids making an
uncertified claim that endpoint entropy alone pays for every legal decoder.

## Why small expected optimum does not give a short witness path

Here is an explicit family in the planar supplied-line model. Take N=n-1
points in strictly convex position and one point in their interior. Supply
one line per hull point that separates precisely that point from all the
others. Such lines exist by strict convexity, and rational coordinates and
strict separating rational lines can be used. The interior point is the
all-negative pattern. Every informative query isolates one hull point,
so the maximum-depth optimum is N, while expected depth is minimized by
querying hull points in decreasing prior order.

Fix a constant r with 1/r<delta, for example r=8 for the current
delta=0.144136826. Put M=floor(sqrt(n)), and use sufficiently large n that
r+M<N. Give:

* r hull points total mass 1-1/M-eta, shared equally;
* M other hull points total mass 1/M, shared equally, so each has mass 1/M^2;
* all remaining hull points and the interior point total mass eta=n^{-3},
  shared equally.

All priors are strictly positive rational numbers. For large n every
supplied minority cap has mass below delta, so even the mass-flat case
exhibits this behavior. The descending-prior query order has expected cost
at most

    (r+1)/2 + [r+(M+1)/2]/M + N eta
      <= (r+1)/2 + 1/2 + (r+1/2)/M + n^{-2}.          (2)

Thus OPT_E is bounded by a constant independent of n although OPT_W=n-1.
An adjacent block of two singleton-isolating caps can hit at most two hull
points. Every L-block prefix therefore leaves at least M-2L middle points,
and hence at least

    (M-2L)/M^2

unresolved probability. If L=O(log n), charging a uniform continuation
height of order n to this unresolved mass yields Omega(sqrt(n)), although
(2) is bounded. Markov's inequality on witness first-hit ranks cannot
repair this charge: mass O(OPT_E/L) times a height of order n is still not a
constant multiple of OPT_E.

This is an obstruction to the uniform-height tail accounting, not an
inapproximability result or an obstruction to all weighted prefix methods.
The singleton family itself is exactly solvable by sorting its priors.
Point-specific fixed-tree penalties correctly account for its middle tier
when B uses the appropriate order.

## The unresolved step for a better uniform factor

Recomputing the existing expected-depth algorithm on the actual unresolved
union R would supply a useful *conditional* bound in terms of OPT_E(R) and
the entropy of R. In a comparison with the optimum witness, a prefix of
L blocks earns an optimum restriction decrease of order L times residual
mass. With L proportional to log n, that decrease could pay a residual
entropy term of order residual mass times log n. A rare long tail need not
have small conditional optimum; its weighted optimum cost can instead be
retained with the existing leading coefficient A=3.5918101789.

The present Cartesian DP does not optimize that adaptive continuation
cost. Its all-negative unresolved set is generally the union of several
Cartesian gaps. The cost of a newly constructed algorithm B(R) is not a
sum of independent costs for the individual gaps. Keeping that entire
union in the state can produce M^{Theta(L)} states, which is
quasipolynomial for L=Theta(log n). Replacing it by fixed-tree additive
penalties restores polynomial time, but the known global expectation bound
for B does not provide a corresponding bound for its restriction B|R.
That conditional guarantee cannot be inferred from its average cost.

A promising next theorem would therefore provide either:

1. a polynomially computable additive completion potential that dominates
   every restricted B|R and satisfies the needed conditional optimum bound;
2. a polynomial state compression for adaptive completion on unions of
   Cartesian gaps; or
3. a multiscale weighted-prefix construction with an explicit amortized
   continuation bound, so that it never multiplies rare unresolved mass by
   the original state's worst-case depth.

These are precise missing proof ingredients. None has been established
here, so the accepted **<5.272565** universal expected-depth bound remains
unchanged.

## Verification

`further-expected-tail-check.py` compares the weighted rank-mask recurrence
against exhaustive distinct-point prefix enumeration on 600 linear and
300 circular instances, using exact integer costs and varied fixed miss
penalties. All objectives agree, including empty-prefix and unused-rank
cases. It also checks exact rational expected-cost upper bounds and the
middle-tier residual charge in the displayed planar family.
