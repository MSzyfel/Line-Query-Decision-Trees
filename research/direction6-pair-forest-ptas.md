# Direction 6: an EPTAS for weighted singleton/pair path and cycle instances

Prepared 13 October 2026. This note does not edit the manuscript. The theorem below is derived here; its novelty has not been established. All weights are positive rationals, queries have unit cost, and the tree identifies the target exactly.

## Outcome

The earlier histogram QPTAS can be replaced by a **deterministic EPTAS** for the weighted singleton/pair subclass with all nonzero singleton caps available and with pair graph a disjoint union of paths and cycles. For every fixed `0 < epsilon <= 1`, the running time is

`2^{O(epsilon^{-3})} poly(n, input bit length, log(1/epsilon))`,

with a polynomial exponent independent of epsilon, and the returned expected cost is at most `(1+epsilon) OPT`. This is compatible with the manuscript's strong NP-hardness and excludes APX-hardness of this subclass unless P=NP. It makes the original weighted pair-forest hardness construction an unsuitable candidate for a constant multiplicative hardness gap.

The improvement uses the matching invoice directly, instead of keeping logarithmically many mass-bucket counts. It combines cheap path/cycle edge deletion, a constant-size heavy-part enumeration, a convex configuration relaxation, and deterministic conditional-expectation rounding.

## 1. The exact matching invoice

Let `0` be the all-negative witness, with weight `w0`. The other vertices have weights `w_v`; their count is `N=n-1`. Every designated cap misses `0` and contains one or two nonzero vertices. All nonzero singleton caps are supplied. Let `G` be the graph of supplied two-vertex caps. Assume `G` is a disjoint union of paths and cycles; the planar realization with every singleton cap supplied has this property.

For a matching `M`, let `J(M)` consist of a group of mass `w_u+w_v` for each matching edge and a singleton of mass `w_v` for each unmatched vertex. Write `k=N-|M|` for its number of groups and `P(M)=sum_{uv in M}(w_u+w_v)`. Query groups in nonincreasing mass order, and use a singleton query to distinguish each pair after a positive answer. Its raw weighted depth is

`G(M)=w0*k+C(J(M))+P(M)`,

where `C(J)=sum_{j=1}^k j*a_j` for group masses `a_1>=...>=a_k`. Following the witness spine of an arbitrary tree gives disjoint first-hit groups of size at most two and therefore a matching. It cannot improve the sorted completion sum or avoid one additional query in a pair exit. Conversely every matching is executable because all singleton tests are supplied. Thus minimizing this invoice gives the exact optimum in the subclass.

Let `Omega=w0+sum_v w_v`. Raw and normalized expected costs have identical approximation ratios.

## 2. Splitting a sparse set of matching edges is cheap

Consider a matched pair with weights `a>=b` at position `j` on an original sorted group spine. Let `R_j` be the total weight of all later groups plus `w0`. Replace its pair query and positive continuation by consecutive singleton queries for `a` and `b`. Retain the original group order, placing these two singletons at the old pair location; this temporary schedule need not be sorted.

The exact change in raw cost is

`Delta_j=R_j-a`.

Indeed the later targets and witness receive one extra query, the lighter endpoint receives its second singleton query, and the pair continuation of mass `a+b` disappears. Changes add over any set of split pairs: later group masses do not change when their own pairs split. In particular

`sum_{split j} Delta_j <= sum_{split j} R_j`.

For any matching, the sum of `R_j` over all its pair positions is at most its original witness-spine cost, hence at most its full invoice. This last bound uses the original spine, before any split.

Number the edges of each path or cycle consecutively from zero, using any cut for a cycle. For a common residue `r in {0,...,K-1}`, delete edges whose number is `r modulo K`. Each original edge is deleted for exactly one of the K residues. Split any original matching edges that were deleted. Averaging the preceding inequality shows that at least one residue yields a feasible surviving matching whose invoice is at most

`(1+1/K) G(M)`.

The algorithm tries all K residues; it does not need to know which one is good. Every connected component of a remaining path has at most K vertices. A cycle's wraparound component can have almost twice that many, so use the uniform bound `B=2K`. An uncut cycle has fewer than K edges and also fits this bound. This avoids an incorrect K-vertex bound for cycles and requires only K global trials even when there are many components.

## 3. A lower bound pays for the light tail

Order individual nonzero weights as `w_(1)>=...>=w_(N)`. In any spine schedule a group contains at most two vertices. Therefore the i-th smallest available vertex rank is at least `ceil(i/2)`. Rearrangement gives

`OPT_raw >= sum_{i=1}^N ceil(i/2)*w_(i)`.

Consequently, after removing the H heaviest vertices, their remaining total weight obeys

`Omega_tail=sum_{i>H} w_(i) <= 2 OPT_raw/(H+1)`.

This is an individual-vertex bound, not a claim that all light vertices occur late in the optimal group order. A light vertex can share an early group with a heavy neighbor. The rank-capacity argument remains valid despite such pairs.

For a fixed residue, declare a surviving component heavy if it contains at least one of the H heaviest vertices. There are at most H such components, each with at most B vertices. Enumerate every matching configuration of every heavy component. Their number of joint choices is at most `2^{BH}`. All components are determined by the instance and the chosen residue, so this incurs no `n^H` factor. The total weight of vertices in the remaining components is at most `Omega_tail`, since fixing a heavy component also removes all its light neighbors from the rounding stage.

## 4. The convex configuration relaxation

For each remaining component `i`, enumerate its matching configurations `c`. A configuration supplies its singleton and pair groups, its group count `k_ic`, and its pair-continuation mass `P_ic`. Write

`z_ic(t)=number of its groups with mass >= t`.

For any complete group multiset with cumulative count `Z(t)`, the sorted completion sum has the exact identity

`C(J)=1/2 * integral_0^infinity (Z(t)^2+Z(t)) dt`.

At a threshold t, the contributing groups occupy precisely ranks 1 through `Z(t)`, whose sum is `Z(t)(Z(t)+1)/2`. Integrating proves the identity, including ties.

Let `x_ic>=0`, `sum_c x_ic=1`, be a distribution over configurations for each light component. Heavy components are already fixed. Define `mu(t)=Z_fixed(t)+sum_ic x_ic*z_ic(t)` and minimize

`Q(x)=w0*(k_fixed+sum_ic x_ic*k_ic)`

`     +P_fixed+sum_ic x_ic*P_ic`

`     +1/2*integral (mu(t)^2+mu(t)) dt`.

This is a convex quadratic program over a product of simplices: the quadratic part is a nonnegative combination of squares of affine functions. It lower-bounds the optimum integral invoice for the fixed heavy branch.

No continuous integration oracle is needed. Every breakpoint is the weight of a singleton or of an available pair, so there are at most `N+|E|=O(N)` breakpoints. On each open interval between successive breakpoints all `z_ic` are constant. The quadratic objective therefore has rational coefficients of polynomial bit length. There are at most `N*2^B` configuration variables.

Normalize all weights by Omega, and solve the rational convex QP to additive accuracy `eta=epsilon/3`; equivalently the unnormalized error is `eta*Omega`. The feasible domain is a product of bounded simplices, and the objective is bounded by O(n). Standard polynomial-time convex quadratic programming yields a feasible rational solution with this accuracy in time polynomial in the program size, input bit length, and `log(1/eta)`. The computational ingredient is the standard linearly constrained convex QP result, not a new optimization claim; see [Nesterov and Nemirovskii, Interior-Point Polynomial Algorithms in Convex Programming, Chapter 8](https://epubs.siam.org/doi/abs/10.1137/1.9781611970791.ch8).

## 5. Independent rounding has a small variance penalty

Independently select a matching configuration for every light component according to its distribution. At threshold t, let its random count be `X_i(t)`. Then `0<=X_i(t)<=B` and

`Var X_i(t) <= E X_i(t)^2 <= B E X_i(t)`.

Independence makes the variance of the total count the sum of component variances. Witness-spine and pair-continuation terms are linear and introduce no additional rounding penalty. Thus

`E G(M_random)=Q(x)+1/2*integral sum_i Var X_i(t) dt`

`             <= Q(x)+(B/2)*sum_i integral E X_i(t) dt`.

For every configuration of component i, the sum of its group masses is exactly the sum of its vertex weights. Therefore the last integral is the component's fixed raw mass, independent of its matching choice. The total penalty is at most

`(B/2)*Omega_tail <= B*OPT_raw/(H+1)`.

The rounding can be deterministic. Expose configurations one component at a time, choose a configuration minimizing the conditional expectation of the final invoice, and continue. The old conditional expectation is the probability-weighted average of the candidate new expectations, so it never increases. Each conditional expectation is computed exactly from rational first and second count moments at the O(n) mass breakpoints, together with the two linear terms. The resulting integral matching has invoice no larger than the initial expected invoice. Sorting its actual group masses supplies the executable tree.

## 6. Parameters, ratio, and running time

Choose

`K=ceil(3/epsilon), B=2K, H=ceil(3B/epsilon), eta=epsilon/3`.

If H exceeds N, enumerate all surviving component configurations; the preceding bounds still hold, with zero light mass. For the good residue, take the branch fixing the heavy components exactly as in an optimum surviving matching. The fractional program cannot exceed that surviving matching's cost, except for its additive solver error. Since `Omega<=OPT_raw` for nontrivial instances, the delivered invoice is at most

`(1+1/K)*OPT_raw + eta*Omega + B*OPT_raw/(H+1)`

`<= (1+epsilon)*OPT_raw`.

The algorithm returns the cheapest tree over every residue and every heavy branch. Configurations per component cost `2^{O(B)}`; heavy enumeration costs `2^{O(BH)}=2^{O(epsilon^{-3})}`; the QP and conditional-expectation computations have polynomial exponent independent of epsilon. Consequently this is an EPTAS. It is not an FPTAS: its dependence on `1/epsilon` is exponential, as permitted by the existing strong NP-hardness.

## 7. Complexity implications and further directions

The full-singleton assumption is used twice: it makes every matching invoice executable and it permits every deleted matching edge to split into two legal singleton exits. Dropping that assumption invalidates this proof; legal splitting is the precise issue to settle before extending the weighted theorem. The uniform result can be strengthened without that assumption, as the direction-5 agent observes: a maximum matching is maximal, and unmatched vertices can exit using an edge to an already queried matched neighbor. That argument does not make arbitrary weighted matchings executable.

Uniform hardness therefore needs caps of size at least three, a lack of a common all-negative witness, or substantial continuation subproblems. The weighted path/cycle construction also cannot yield APX-hardness under its present assumptions. New hardness should encode coupled choices with a constant penalty relative to the whole tree, rather than amplify the present exact 3-Partition gap.

A useful extension is the following abstract theorem template. If a pair graph admits a polynomial-size family of edge deletions that (i) leaves components of size at most `B(epsilon)` and (ii) deletes every matching edge with probability at most epsilon, the same argument gives an EPTAS whenever singleton splitting is legal. The cycle/path residue family supplies the simplest instance. For general planar graphs, bounded-component decompositions and edge deletion probabilities require care; bounded treewidth alone does not make the global sorted completion invoice local.

For implementation, the convex relaxation is more promising than the earlier global histogram DP: there are O(n) mass breakpoints and only finitely many options per small component. The EPTAS is a theoretical algorithm with a large dependence on epsilon; practical experiments should start with small B, numerical convex QP, and exact conditional-expectation rounding.

## 8. Verification scope

`direction6-pair-forest-check.py` uses exact rational arithmetic to check the rank integral identity, the splitting formula and its additivity, path/cycle residue losses, the individual-weight tail bound, the fractional first/second-moment identity, the variance upper bound, and deterministic conditional-expectation rounding against full enumeration on small instances. It tests the mathematical relaxation and rounding machinery, rather than claiming to implement a polynomial-time convex-QP solver. The theorem's convex optimization step uses the standard result cited above.
