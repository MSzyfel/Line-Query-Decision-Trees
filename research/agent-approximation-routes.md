# Approximation routes for supplied-line planar decision trees

Prepared 13 October 2026. This report concerns the binary model in `sections/02-preliminaries.tex`: rational points, an explicitly supplied separating line family, unit query costs, and either maximum or arbitrary-prior expected depth. The manuscript is unchanged. Results below use its common-witness, adjacent-support, endpoint, and restriction lemmas; those manuscript lemmas have not received a complete independent audit here. Literature-wide novelty is not claimed.

## Main finding

There are two concrete **quasipolynomial improvements**. Nested interval deadlines give an exactly certified `4.764` approximation for maximum depth, with a limiting bound approaching `4.76249351`. The same spatial grade DP, minimizing weighted first-hit cost and zero-target waiting time, gives an exactly certified `3.835` approximation for arbitrary-prior expected depth, with a limiting bound near `3.83342161`. The complete derivations below assume the manuscript's structural lemmas. These improve the current `5.464966` and `5.445944` factors at a higher running-time cost. Neither is a polynomial-time approximation theorem.

For polynomial time, the clearest implementable improvement is an exact joint endpoint decoder with actual child-code costs as terminal penalties. It guarantees no regression, but a smaller global leading constant still needs a new analysis. The most promising harder project is a discovery algorithm that accounts for cached-neighbor endpoint savings in the scheduling objective itself.

## 1. Exact nested deadlines, and a quasipolynomial factor approaching 4.762494

**Status:** fully specified derived algorithm and proof below; finite verification of the scheduling DP; assumes manuscript geometry and supporting-prefix lemmas. Root and approximation-route agents independently checked the delicate rounding inequality.

### The scheduling primitive

There are candidates `1,...,M` on a line, interval demands `I`, and `r` distinct integer deadlines `b_1 < ... < b_r`. We need a candidate ordering in which every demand `I` is hit by its deadline. A candidate can be unused or assigned a grade `i in [r]`. Grade `i` means it is scheduled in the `i`-th deadline bucket. Demand `I` with grade `j` must contain a selected candidate of grade at most `j`, and at most `b_j` candidates in total may have grade at most `j`.

Scan the candidates in **spatial order**, not query order. A state stores:

- `p_j`: the last scanned candidate selected at grade at most `j`, or zero if none;
- `c_j`: the number of scanned candidates selected at grade at most `j`.

At candidate `q`, either skip it or assign grade `i`. The latter sets `p_j=q` and increments `c_j` for every `j >= i`. Reject states with `c_j > b_j`. Whenever an interval `[l,q]` ends, with deadline grade `j`, require `p_j >= l`. This is necessary and sufficient: the last qualifying selected candidate is in the interval exactly when the interval has any qualifying selected candidate.

The state count is at most `(M+1)^r (B+1)^r`, where `B=max b_j` can be capped by the number of useful candidates or the trial height. There are `r+1` transitions per state and candidate. Thus feasibility, with a witness, takes `(MB)^{O(r)}` time. The DP is exact for fixed `r` and polynomial for fixed `r`.

Recover a query schedule by listing selected candidates in increasing grade, with arbitrary order within a grade. Every deadline-`j` demand is hit within the first `c_j <= b_j` queries. Conversely, any feasible schedule can be converted to grades: assign each selected candidate to the first deadline at least its query rank and discard candidates occurring after all deadlines. Hence the grading DP is an exact feasibility test.

For circular intervals, enumerate a forced first candidate `v`. Demands hit by `v` exit immediately. All other intervals omit `v` and become ordinary intervals after cutting there. Apply the DP to the remainder, with each absolute deadline reduced by one. A feasible comparison schedule beginning at `v` induces a feasible DP state.

### Why separate exact budget covers are insufficient

Candidates `1,2,3` have deadline-one demands `[1,2]` and `[2,3]`, and deadline-two demands `{1}` and `{3}`. The first deadline prefix is covered by `{2}`; the second is covered by `{1,3}`. Nevertheless no schedule meets both deadlines: rank one must be `2`, leaving only one rank by time two to query both `1` and `3`.

This example shows that independent coverage feasibility at every deadline does not establish joint feasibility. It does not establish a fractional gap for the usual time-indexed LP; that LP also detects the example's infeasibility. A polynomial algorithm must enforce compatible nested prefixes, or tolerate dilation.

### Incorporation into the maximum-depth recursion

Fix a rational `lambda=1+epsilon>1` and let `a=2 lambda`. Choose fixed `0<delta<1/3` and `gamma>=1` satisfying

```
gamma log_2(1/(1-delta)) >= 1,
gamma log_2(1/delta) >= a+4.
```

The target inductive bound is

```
C(S) <= floor(a OPT_W(S) + gamma log_2 |S|).
```

At a flat state, recursively construct every hull-pattern child and record its actual height. Enumerate trial integer heights `H` and a first hull vertex `v`. Classes positive on `v` use the general endpoint allowance

```
e_A = floor(log_2(delta |S|/|A|)) + 4
```

and pass the direct check `1+C(A)+e_A <= H`. For classes negative on `v`, let

```
B_A = H - C(A) - e_A.
```

Round `B_A` **down** to the largest distinct integer level of the form `floor(lambda^j)` not exceeding it. Call this rounded absolute deadline `hat B_A`. Reject impossible budgets. Use the nested interval DP, after cutting at `v`, to find a schedule meeting all rounded deadlines. Check its actual first-hit indices and then use its endpoint exits followed by the stored children. Only one first vertex, rather than an adjacent first pair, is needed.

The number of distinct levels is `O(log n / epsilon)` because all trial heights are `O(n)` for fixed parameters. The trial height can be capped by `ceil((a+gamma)(|S|-1))`; the proof guarantees a passing trial by that height.

### The floor calculation that makes the theorem work

Put `s=|S|`, `D=OPT_W(S)`, `x=log_2(s/|A|)`, and `L=log_2(1/delta)`. Let `t=t_A` be the supporting-prefix index from the manuscript, so `OPT_W(A) <= D-(t-1)`. At

```
H* = floor(aD + gamma log_2 s),
```

the inductive child bound gives

```
B_A >= floor(a(t-1)+gamma x) - floor(x-L) - 4
    >= floor(a(t-1)+(gamma-1)x+L) - 4
    >= floor(a(t-1)+gamma L) - 4
    >= floor(at).
```

The middle inequality uses `x>L` and `gamma>=1`. This calculation subtracts the endpoint floor before estimating; estimating the two floors separately would introduce an unnecessary additional unit.

Let `j` be maximal with `floor(lambda^j) <= B_A`. Since the next integer level exceeds `B_A`,

```
lambda^(j+1) >= B_A+1 > at,
hat B_A = floor(lambda^j) > (B_A+1)/lambda - 1 > 2t-1.
```

Thus the integer rounded deadline satisfies **`hat B_A >= 2t`**. This is the exact rounding fact needed; no small-deadline exception is necessary.

Expand the optimal witness path's support blocks into their real hull vertices, omitting repeats. It hits every nonzero class by at most `2t_A` queries. Choose an enumerated `v` equal to its first real support and orient that first block so `v` is first. Every class negative on `v` is an ordinary interval after cutting there, and the expanded comparison sequence demonstrates feasibility for its rounded deadline. The DP therefore succeeds at `H*`.

Classes positive on `v` have `t_A=1`, or simply use monotonicity `OPT_W(A)<=D`; the same floor calculation leaves at least `floor(a)>=2` discovery units, enough for their one-query exit. This includes all first-query cases. The terminal nonzero singleton, if the witness path finishes without a supporting hit, can be appended as in the manuscript; its index `t=q+1` is covered by the same restriction credit and rounding argument.

At a balanced state the count-potential drop is at least one, so the single balanced query also fits `H*`. On the all-negative route, stop when all nonzero classes have been covered. Its length is the largest positive first-hit index, which is at most the accepted height. The zero pattern has no continuation. The proof therefore does not require an additional total-length estimate against `2D`.

### Resulting factor and bit complexity

Since `D >= log_2 s`, the ratio is at most `a+gamma`. For fixed `a`, the best threshold in this proof balances the two parameter constraints, giving

```
delta = (1-delta)^(a+4),
gamma = 1/log_2(1/(1-delta)).
```

As `epsilon` tends to zero, `a` tends to two and

```
delta -> 0.2219104013213989,
gamma -> 2.762493509736569,
a+gamma -> 4.762493509736569.
```

For every fixed `eta>0`, pick a rational epsilon sufficiently small and rational delta/gamma slightly above the constraints, obtaining a factor below `4.762494+eta`. A concrete exactly certified choice is

```
epsilon=1/2000, a=2001/1000,
delta=2219/10000, gamma=2763/1000,
a+gamma=1191/250=4.764.
```

The verification script uses exact rational lower and upper logarithm bounds with 180 terms and verifies `gamma ln(1/(1-delta)) > ln 2` and `gamma ln(1/delta) > (a+4) ln 2`. The powers `lambda^j` are rational, and `j=O(log n/epsilon)`, so their bit lengths and the comparisons are polynomial for fixed epsilon. The running time is `(mn)^{O(log n/eta)}`; storing backpointers and reconstructing the selected grades remain within that bound. There are only polynomially many recursive stages, trials, and first-vertex choices.

**What this does not prove:** polynomial-time factor `4.762494`, a PTAS, or any analogous expected-depth improvement. The stored grade vectors have quasipolynomially many possibilities.

### Verification

`agent-approximation-check.py` independently implements the grade/last-position/count DP and compares it with all candidate permutations on 750 seeded random instances, candidate counts two through six and at most three deadline levels. All agree. It also verifies the three-candidate obstruction above and exactly certifies the rational parameters for factor `4.764`. These finite checks support implementation correctness; the proof is the state invariant and grade/order equivalence.

**Next polynomial-time attack:** compress or round these grade vectors without multiplying deadline dilation back to `3/2`. A theorem that simultaneously hits the relevant deadline prefixes by at most `(2+zeta)t_A` supports, with `zeta<1`, would improve the manuscript's polynomial maximum-depth coefficient. Independent maximum coverage at each prefix cannot establish it.

## 2. Joint endpoint decoding with continuation penalties

**Status:** proved polynomial primitive and no-regression modification. No smaller universal leading factor yet.

After a positive hull answer and a valid linear cut, represent each nonzero pattern by its endpoint pair `(L,R)`. Queries left of the known positive vertex compare `L` to a threshold; queries right of it compare `R` to a threshold. Every compatible endpoint state reached by such comparisons is the original finite support intersected with an axis-parallel rectangle in the endpoint grid.

There are `O(M^4)` rectangles. For each rectangle `R`, precompute the total original hypothesis weight `w(R)` and its occupied pattern classes. For maximum depth, let `F_W(R)` be the least possible total height from that state, including the already built child tree as a terminal continuation:

```
F_W(R) = C_W(A)                         if R contains only pattern A,
F_W(R) = 1 + min_threshold max(F_W(R0),F_W(R1)) otherwise.
```

For expected depth use original, unnormalized weights:

```
F_E(R) = C_E(A)                         if R contains only pattern A,
F_E(R) = w(R) + min_threshold (F_E(R0)+F_E(R1)) otherwise.
```

Only thresholds yielding two nonempty pattern sets are considered. The state ordering is by rectangle size, and one of the rectangle coordinate bounds strictly shrinks at every child. There are `O(M)` thresholds per state, so `O(M^5)` arithmetic operations suffice after preprocessing. The resulting decoder is exactly optimal among hull-threshold endpoint trees with these fixed child continuations. A decoder subtree may have a single remaining pattern with many hypotheses; then it must execute its stored child code rather than use zero cost.

This removes the restriction that the entire left endpoint must be learned before any right endpoint query. For maximum depth, it also lets expensive children receive shorter pattern codes. For expected depth, the terminal continuation costs sum to the same quantity for every full pattern decoder, because every class is reached once; including them does not change the optimal decoding order. Sequential midpoint-dyadic codes remain feasible comparison trees, so the joint decoder's worst-case and expected objectives can only improve. The current constants remain valid.

For the maximum-depth recursion, build these actual endpoint decoders conditioned on each discovery transcript and check their realized total exit heights. For expected depth, build the decoder minimizing total expected cost including continuations and compare the complete resulting tree to the manuscript tree. Do not assume pointwise domination: optimizing total expected depth can lengthen rare paths.

**Candidate theorem to seek:** an inequality for the joint decoder combining conditional pattern entropy, pattern mass, and continuation variation that strictly improves on `4b+(I-J)/ln2` in a flat stage. Generic `H+3` is not justified. An internal, high-probability endpoint pair can need two threshold certifications per coordinate, approaching four queries while its entropy approaches zero. Any improvement needs geometric/flatness/cached-answer or continuation structure.

**Experiment:** compare sequential exact alphabetic decoding, the rectangle DP without tails, and the tail-aware DP. Use independently skewed endpoint marginals, four nearby alternatives around a dominant internal pair, and patterns with widely varying continuation heights. Measure complete returned-tree costs, not endpoint entropy alone.

## 3. Couple discovery order to pinning and endpoint work

**Status:** promising polynomial research route, with a rigorous local accounting observation; global approximation theorem open.

The manuscript already obtains

```
W_pattern <= A_beta Delta + B_(beta,delta) b
             -2 b_pin -2 b_both + (I-J)/ln2.
```

The final proof drops the two cached-neighbor savings. Instead, optimize a discovery ordering using its **complete** exit cost: first-hit rank plus a conditional endpoint decoder. A block containing two adjacent supports naturally creates a pinned exit on its second positive route.

Consider one adjacent pair `v,w` after earlier misses. Its newly covered pattern mass decomposes into `x` positive only on `v`, `y` positive only on `w`, and `z` positive on both. Ignoring the conditional entropy term for the moment, use the manuscript's generic allowances of four endpoint queries on a first exit and two on a second exit. Ordering `v,w` contributes

```
5(x+z)+4y,
```

whereas ordering `w,v` contributes

```
5(y+z)+4x.
```

Thus the pair's complete discovery-plus-endpoint additive allowance is smaller when the **smaller exclusive mass is queried first**. This is the reverse of the first-cover-only preference. Both-positive mass exits first in either orientation; it does not earn pinning credit. The calculation is an upper-bound comparison, not a statement that every target actually needs four or two endpoint queries.

Adjacent pairs themselves form a circular candidate order. The pairs intersecting a demand interval form a circular interval expanded by one position, so exact budgeted coverage remains available for blocks. Potential approaches are a block-batch scheduler, a time-indexed relaxation with pinned/unpinned exit states, or geometric batches whose within-batch order minimizes full conditional decoder cost.

**Candidate theorem:** produce one deterministic schedule such that its discovery and remaining endpoint cost satisfy

```
W_complete <= alpha Delta + c I
```

with `alpha+c ln2 < 5.445944`, retaining the zero-pattern completion term. A sufficient intermediate goal is a guaranteed positive amount of pinning credit on configurations near the current worst-case flat-state ratio.

**Obstacle:** no universal lower bound on pinned mass follows merely from positive mass. If every likely interval contains both vertices of any selected adjacent pair, it exits first and remains unpinned. Conversely, disjoint singleton-like patterns have large pinning potential but low endpoint cost already. Discovery mass, overlap, entropy, and endpoint redundancy should therefore be optimized jointly rather than minimized independently.

**Experiment:** exact subset ordering for `M<=18`, with cached-neighbor masks and rectangle-DP endpoint costs, to find the Pareto frontier in first-cover cost, full schedule length, pinning mass, and complete pattern cost. Seek a small counterexample to each proposed universal pinning inequality before proving a general bound.

## 4. Use original caps to avoid the two-support expansion

**Status:** research direction with an available geometric coverage oracle and a precise unresolved restriction-credit issue.

The spatial coverage oracle is stronger than it may initially appear. Har-Peled and Lee prove exact polynomial minimum-weight cover of points by supplied planar halfplanes. Badanidiyuru, Kleinberg, and Lee explicitly state in Appendix B that a modification of this DP solves two-dimensional maximum halfspace coverage optimally in polynomial time. [Har-Peled–Lee, JoCG 2012](https://jocg.org/index.php/jocg/article/view/2950); [Badanidiyuru–Kleinberg–Lee, Appendix B](https://arxiv.org/html/1112.0689).

Consequently, direct discovery using original minority caps has an exact budgeted coverage route. Weighted point profits should be checked in the original DP, rather than assumed from a cardinality theorem; its additive-profit form is the natural extension. The real obstacle is accounting, not simply the existence of a coverage algorithm.

An original query can vary within one hull-pattern class. If direct discovery ends at an original-cap hit, refine its output class by the learned hull pattern. This gives cells `original discovery transcript intersect hull pattern`. Such a cell still need not be constant on the **comparison** optimal witness path queries prior to its members' various original first-hit times. The expected direct first-cover time therefore does not automatically correspond to a common prefix removable from the restricted optimum.

The original hull argument pays only for queries before the first **supporting** hit, where every member of a hull-pattern class has all support bits negative. A later original-cap first hit can have a much larger latency without yielding extra pruning credit. Replacing discovery entropy `J` by mutual information does not by itself cure this mismatch.

**Candidate invariant:** construct a mixed original/hull macro whose output cells are constant on enough original witness-path queries, or show a quantitative inequality charging the discrepancy to the information retained inside those cells. A useful target is an affine stage inequality

```
W_original <= alpha Delta(S,Pi') + c I(S,Pi')
```

with `alpha` close to the one-support batch coefficient rather than `2 lambda`. Any proof must explicitly explain which comparison-path queries disappear when each cell is revealed.

**Experiment:** random rational instances whose normalized line vectors have long radial distances inside hull edges. Compare direct original-cap first-hit times with supporting-hit times, compute exact small-instance `Delta` for the algorithm's refined cells, and record whether the putative credit bound fails. These examples expose the missing invariant more effectively than hull-vertex-only instances.

## 5. Instance-dependent potentials and fixed-depth macro improvement

**Status:** safe algorithmic improvements are available; a smaller leading universal factor needs genuinely new amortization.

The current expected-depth proof minimizes discrete discovery saving and exit entropy largely through separate lower bounds. It also discards cached-neighbor credits and the nonnegative `Delta` term at balanced queries. Record the complete flat-stage profile: discovery-class masses, support-block masses, endpoint overlaps, `b_pin`, `b_both`, endpoint conditional entropy, and exact endpoint redundancy from Route 2. Seek a joint inequality for the profiles that can actually arise geometrically.

One must first test whether the extremizers of the existing inequalities are compatible. For example, filling early support blocks to mass `2delta` and discovery exits to mass `delta` can be compatible when each block has two disjoint caps, so incompatibility cannot simply be asserted. Overlap can decrease available mass but simultaneously remove pinning savings. A finite optimization over the profile, or a small LP strengthened by explicit interval incidences, is useful for discovering the correct inequality.

For a practical baseline, use a fixed-depth adaptive prefix, then complete every leaf with the current geometric algorithm or its restricted stored tree. Pick the complete tree with least actual objective and retain the baseline as a candidate. This is polynomial for each fixed prefix depth and cannot worsen the baseline. The uniform notes correctly emphasize complete continuation costs rather than split quality and the need to charge globally. This transfers well to the planar setting, but does not prove a new asymptotic leading factor by itself.

The root agent derives fixed-prefix additive improvements such as `rho OPT_E-(rho-1)` for one-step expected rollout, and a corresponding maximum-depth improvement with larger fixed lookahead. Those are useful refinements and experiment baselines. They should be reported as additive or instance-dependent gains, rather than a universal improvement of the leading factor for unbounded optimum.

**Candidate stronger theorem:** every flat state with poor pinning or endpoint redundancy admits a bounded-depth supplied-line prefix obtaining a specified additional restriction/entropy decrease. The theorem must cover original lines inside hull edges and rare difficult posterior tails. A dichotomy of this form could make the costs of the current worst-case configurations incompatible with a locally improved policy.

## Recommended next steps

1. Formalize Route 1 as a standalone quasipolynomial theorem, preserving the exact rounding proof. The concrete factor `4.764` already has a rational parameter certificate in the verification script.
2. Implement the rectangle DP and use it to measure complete endpoint-plus-child costs. It is polynomial and has a clean correctness proof.
3. Search exact small coupled schedules for a reusable pinning/overlap inequality. This is the likeliest direct polynomial expected-depth improvement.
4. Attack direct original-cap discovery only with the pruning-credit obstacle stated explicitly; the coverage oracle is already available.
5. Use a shared small-instance exact optimum and adversarial families to test every conjectured potential, rather than using random instances alone.

## 6. Expected-depth improvement from a joint cover-order QPTAS

**Status:** derived, fully specified quasipolynomial theorem, with an exact rational factor `3.835` and finite verification of the optimization DP. Assumes the manuscript's supporting-prefix, endpoint, and capped-discovery entropy lemmas. The rounding and accounting have been independently checked by the root and approximation-route agents.

### Optimize the grade DP rather than just feasibility

Given positively weighted interval demands and zero-target weight `p0>=0`, the joint objective of an ordering `Q` is

```
L(Q) = sum_I weight(I) first_hit_Q(I) + p0 |Q|.
```

Unproductive queries can be deleted, so an optimal cover ordering uses at most the number of demands. In the decision-tree application there are at most `n` distinct patterns. It is therefore safe to cap the total number of selected candidates by `n`; this cap supplies a quasipolynomial rather than an exponential number of deadline levels.

Fix rational `lambda>1`. Use the distinct integer levels `d_j=floor(lambda^j)` through the first level at least `n`. The spatial state again stores the last selected position `p_j` of grade at most `j`, and its cumulative count `c_j`, with `c_j<=d_j`. This time there are no externally assigned interval deadlines. When interval `[l,q]` ends, let

```
tau(I) = min {j : p_j >= l}.
```

Reject the state if no such grade exists; otherwise add `weight(I) d_tau(I)` to the objective. The first qualifying grade is precisely the smallest grade among selected candidates inside the interval. All its candidates have already been scanned when the interval ends, so this cost is final and charged exactly once. Keep the least accumulated objective for each state. At the end, add `p0 c_last`.

Ordering selected candidates by grade yields actual first-hit time at most `c_tau<=d_tau`; the actual completion length is exactly `c_last`. Consequently the DP objective is an upper bound on the resulting ordering's joint cost.

### Integer rounding up has no additive loss

For integer rank `k>=1`, round up to the smallest level `d_j>=k`. If `k=1`, this is exact. Otherwise the preceding power has `floor(lambda^(j-1))<k`, hence `lambda^(j-1)<k`. Thus

```
d_j = floor(lambda^j) < lambda k.
```

Repeated integer levels may simply be ignored. This argument avoids a ceiling error and needs no separate collection of exact small levels.

Map each candidate of a comparison cover ordering `Q` to the first grade whose level is at least its rank. Its cumulative grade counts satisfy all capacities. An interval first hit at rank `k` is hit by a candidate assigned to a level less than `lambda k` (or level one for rank one). Therefore the minimum surrogate obeys

```
surrogate_min <= lambda sum_I weight(I) first_hit_Q(I) + p0 |Q|.
```

The actual returned ordering is no worse than its surrogate, so this is a joint weighted cover-order QPTAS. The zero-target term is actually preserved with coefficient one; using coefficient lambda there would also be valid.

### Circular demands and a forced first candidate

Enumerate first candidate `v`. Pay exactly rank one for demands containing it and remove those demands. All remaining demands omit `v`, so cutting at `v` makes them ordinary intervals. Reduce every count capacity by one to account for the forced rank-one query: `c_j<=d_j-1`. Add `p0(1+c_last)` at the end. The complete surrogate is

```
mass_hit_by_v + sum_remaining weight(I) d_tau(I) + p0(1+c_last).
```

A comparison ordering's first candidate occurs in this enumeration. Assign grades to its remaining candidates using their **absolute** ranks, so the same comparison bound holds. Any enumeration with a constant or unproductive first query can be ignored or executed with that query suppressed; it is enough that the comparison's useful first candidate is considered. Reconstruction, suppression of repeated/constant queries, and singleton inference only decrease the actual cost.

The number of levels is `O(log n/(lambda-1))`. The DP has `(mn)^{O(log n/(lambda-1))}` states and transitions, uses rational additions and comparisons, and returns an explicit deterministic ordering. There is no hidden oracle for optimal decision trees.

### Improved discovery bound

Let `D_plus=sum_nonzero w(A)(t_A-1)` for the manuscript's optimal-witness supporting-prefix indices, and let `b=w(S)-w(A0)`. Expand each witness query into its one or two real hull supports. Within a two-support block, query the support covering the heavier newly hit mass first. At least half the block's new mass then exits by rank `2t-1`, and all of it by rank `2t`. Thus

```
MSSC(Q_support) <= 2 D_plus + (3/2) b.
```

A singleton-support block obeys this bound with room to spare. If the witness leaf is a nonzero singleton not already covered, append one of its positive supports. Its index is at most `2q+1=2(t_A-1)+1`, which also fits the bound. When the zero pattern exists, no terminal positive singleton needs appending and the complete support ordering has length at most `2q`.

The QPTAS comparison then yields

```
W_discovery <= lambda(2 D_plus + (3/2)b) + 2 w(A0) q
            <= 2 lambda Delta_E(S,Pi) + (3/2) lambda b.
```

The second inequality uses the manuscript's restriction credit `D_plus+w(A0)q<=Delta_E` and `lambda>=1`. When `A0` is absent, its waiting term vanishes and the appended-singleton case is already included in the first-hit bound.

### Full-pattern and recursive accounting

Use the existing endpoint procedure. If `I=I(S,Pi)` is full-pattern information and `J` is discovery-transcript information, the endpoint contribution is at most

```
4b + (I-J)/ln2
```

after discarding nonnegative pinning credits. Thus the full stage satisfies

```
W_pattern <= 2 lambda Delta_E + (4+(3/2)lambda)b + (I-J)/ln2.
```

Every nonzero discovery class lies in its first positive hull cap, with mass below `delta w(S)`; an inferred nonzero singleton obeys the same cap bound. The manuscript's capped-discovery lemma gives `J>=b sigma(delta)`. Consequently, with

```
c = max {1/h(delta), (4+(3/2)lambda)/sigma(delta), 1/ln2},
```

the stage cost is at most `2lambda Delta_E+cI`: its capped-mass term is paid by `cJ` and the remaining endpoint entropy is paid by `c(I-J)`. Balanced queries cost at most `cI` as well. Telescoping over recursive states gives

```
C_E(S) <= 2lambda OPT_E(S) + c E(S),
ratio <= 2lambda + max {ln2/h(delta),
                       (4+(3/2)lambda) ln2/sigma(delta),
                       1}.
```

Here `E(S)` is weighted state entropy in natural-log units. The third term is redundant at these parameters but makes the endpoint accounting explicit. There is **no subtraction of one** from the flat-state coefficient: the endpoint entropy remains in the potential and must still be paid.

### An exactly certified factor 3.835

Use

```
lambda=2001/2000,
delta=3141/25000=0.12564,
2lambda=2001/1000,
k_delta=7, r_delta=3013/25000,
extra_coefficient=917/500=1.834.
```

`agent-approximation-check.py` applies exact Fraction logarithm bounds with 180 positive-series terms to verify

```
(917/500) h(delta) > ln2,
(917/500) sigma(delta) > (4+(3/2)lambda) ln2.
```

The extra coefficient exceeds one, so all three terms in the ratio bound fit, giving

```
C_E <= (2001/1000 + 917/500) OPT_E
    = (767/200) OPT_E
    = 3.835 OPT_E.
```

The guarantee is independent of the smallest positive hypothesis probability. The algorithm compares rational DP objectives, not entropy or floating-point values. This is a quasipolynomial approximation theorem for arbitrary positive priors, with supplied binary lines and unit costs.

For a simpler but weaker parameter presentation, `lambda=1001/1000` and `delta=1/8` give a factor below `3.842` by certifying `ln2/h(1/8)<1.84` and noting the flat coefficient is less than `1.84`.

As lambda tends to one, numerical minimization of the bound gives a crossing near `delta=0.12566495055` and limiting ratio `3.83342160628`. That numerical limiting value is a useful direction, while `3.835` is the exactly certified concrete theorem established here.

### Additional finite checks

With every integer rank as a level, the surrogate DP must recover the exact joint ordering optimum: mapping an optimal order to exact ranks gives an equal surrogate, while every surrogate dominates its reconstructed order. The verification script checks this identity against all permutations on 100 weighted instances with candidate counts two through five, positive integer demand weights and zero-target weights from zero through ten. All agree. Coarser levels are also checked not to beat the exact optimum.

No globally smaller **polynomial-time** approximation constant has been proved by this report. Both improved factors rely on retaining `O(log n)` grade coordinates in a quasipolynomial state space.

## Sources and scope notes

- [Har-Peled and Lee, Weighted Geometric Set Cover Problems Revisited, JoCG 3(1), 2012](https://jocg.org/index.php/jocg/article/view/2950): exact weighted full halfplane cover.
- [Badanidiyuru, Kleinberg, Lee, Approximating Low-Dimensional Coverage Problems, arXiv:1112.0689](https://arxiv.org/html/1112.0689): Appendix B explicitly identifies exact polynomial two-dimensional maximum-halfspace coverage via the Har-Peled–Lee DP.
- [Hu and Tucker, Optimal Computer Search Trees and Variable-Length Alphabetical Codes](https://epubs.siam.org/doi/abs/10.1137/0121057): classical optimal alphabetic-tree background; Route 2 needs joint coordinate comparisons and terminal continuation penalties, not merely the alphabetic one-dimensional problem.
- [Zhang and Cao, Minimum Sum Set Cover: Structures and Algorithm, 2026](https://arxiv.org/abs/2605.21920): optimal latency covers can be larger than minimum-cardinality covers; its stated FPT result concerns bounded-rank hypergraphs. Long hull intervals have unbounded rank, so that result is not a direct polynomial algorithm for this discovery problem.
- Local uniform notes were consulted for the continuation-aware macro and amortization pitfalls. Their unrestricted-test results do not automatically establish a planar supplied-line theorem.
