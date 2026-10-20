# Planar line query decision tree research agenda

13 October 2026. Binary answers, unit query costs, a supplied separating family of rational planar lines, and identification of every hypothesis.

The latest exploration gives **general deterministic polynomial-time factors 4.46496526 for maximum depth and below 5.182976 for arbitrary-prior expected depth**. Modifying both initial coverage budgets improves the previous 5.197569 factor. A smaller global slot cap reduces the maximum-depth scheduler's polynomial degree. A new PTAS covers uniform fixed-size convex-position caps with a distinguished all-miss hypothesis, without singleton supply. An exact geometric cloud transfer establishes **strong NP-completeness for uniform expected depth**. The earlier **quasipolynomial `(2+epsilon)` approximations for both objectives**, **EPTAS for weighted singleton/pair path-and-cycle instances**, and **exact polynomial maximum-depth optimization for bounded caps with an all-miss hypothesis** remain valid. Fixed-factor hardness remains open.

The derived algorithms below use the current manuscript's common witness, adjacent support, supporting prefix, endpoint coding, and entropy lemmas. The new scheduling and rounding arguments have been checked independently by multiple agents and against small exact instances. This is a research derivation, with literature wide novelty unestablished; it is not a complete independent audit of the manuscript.

| Direction | Result or target | Status |
|---|---|---|
| Maximum depth | `2+epsilon` in quasipolynomial time | Derived and independently audited proof; integrated in TeX |
| Arbitrary prior expected depth | `2+epsilon` in quasipolynomial time, without a minimum-prior dependence | Derived and independently audited proof; integrated in TeX |
| General polynomial expected depth | Factor below `5.182976` for arbitrary positive priors | Rational certificate, modified-batch checks and independent audit; integrated in TeX |
| General polynomial maximum depth | Factor `4.46496526`, with an optional exact whole-exit decoder | Rank-subset scheduling and two simultaneous invariants; independent audit; integrated in TeX |
| Uniform expected-depth complexity | Strong NP-completeness | Exact cloud transfer; integrated in TeX |
| Fixed factor hardness | Shallow ordered halfplane cover or robust coupled choice gadgets | Research candidates; no APX hardness proved |
| Weighted singleton and pair subclass, all singletons, path/cycle pair graph | EPTAS: `2^{O(epsilon^-3)} poly(n,input bits)` | Derived proof; integrated in TeX |
| Uniform singleton and pair caps, all-miss hypothesis | Exact optimization by matching, even without all singleton tests | Derived and tested theorem |
| Fixed-size caps, all-miss hypothesis | Exact polynomial maximum-depth algorithm | Derived suffix-enumeration proof; integrated in TeX |
| Uniform fixed-size convex-position caps, all-miss hypothesis | PTAS, no singleton supply required | Exact block-interleaving DP and independent adaptive-tree audit; integrated in TeX |

## Latest algorithms and the six attacking routes

### Two initial budgets: general polynomial expected depth below 5.182976

The [new two-budget section](sections/06g-two-phase-improvement.tex) tries `q,r,k2,k3,...` with `q=1,...,6` and `r=k1-1,k1,k1+1`, when `q<r<k2`, as well as `q,k2,k3,...`. The rational shift partition includes all initial `k/beta` and `k/beta²` breakpoints through `ceil(beta³)`, including when the minimum cover is small. Exact coverage, rational block modes and full-pattern recursion remain unchanged.

With `beta=3512863/10^6` and `delta=393931/2500000`, a fixed 43-row rational certificate gives `A=3.591810178840039...`, `B=4.374727111311243...`, and factor **below 5.182976**. It retains signed first-hit corrections and complete zero-route changes; first-batch saving is counted once. The complete table is [in the numerical appendix](sections/12-two-phase-certificate.tex), and [exact checks](expected-two-phase-check.py) verify the certificate, 9,900 phase identities and 1,650 actual-batch cases. An [independent direct phase audit](development-two-phase-audit.md) reproduces the ratio without the older discount formula.

All 22 algorithm2e recipes now sit beside their analyses. Four flow diagrams explain recursion, maximum-depth scheduling, expected-depth schedule construction and execution, and quasipolynomial lookahead. Shared floor, capped-rank, entropy and lookahead lemmas shorten repeated reasoning while preserving the guarantees and edge cases.

### Uniform shallow-cap PTAS and the revised hardness target

The [new PTAS](sections/06h-uniform-bounded-cap-ptas.tex) applies to uniform hypotheses in convex position, with an actual distinguished all-miss hypothesis and cap size at most fixed `b`. Mark `b` points in each cyclic piece of length `ell>=8b²/epsilon`; clear them using supplied caps, with legal local positive-exit codes. Every residual cap acts within one block. An exact count-vector Bellman DP optimizes all query interleavings; uniform weights permit grouping identical local mask families. At most `b*ell` interval masks give at most `2^((b+1)*ell)` local states. Realizing-query maps remain attached to physical blocks.

The prefix adds at most `2r(N+1)`, whereas every full tree costs at least `N(N+1)/(2b)` in raw uniform depth. With `r<=2bN/ell`, the ratio is at most `1+8b²/ell`. This is a PTAS whose exponent depends on `b,epsilon`. [Development checks](constant-gap-session.py) passed 1,080 decompositions and an [independent audit](uniform-cap-ptas-audit.md) passed 3,033 adaptive-oracle comparisons, including families without singleton tests.

The GOOD/BAD prefix examples remain valid, but bounded-size interval caps on one convex layer cannot supply constant-factor NP-hardness under uniform priors unless P=NP. Future reductions must escape that class, for example through unbounded caps, several convex layers, or a different witness architecture, and must prove robust global assignment extraction for arbitrary adaptive trees.

### Earlier single-initial-budget factor below 5.197569

The [new section](sections/06f-first-phase-improvement.tex) tries every initial budget `q=1,...,6` below the second geometric budget, as well as merging the first two batches. All later batches, exact interval coverage, rational block modes and full-pattern recursion remain the same. Select the actual deterministic schedule by its rational surrogate; the fixed eight-row proof distribution is used only in the analysis.

For `k0=floor(u)` and `k1=floor(beta*u)`, replacing the first budget by q changes the doubled first-cover allowance by

\[
d_q(u,t)=k_0-q+(k_0+k_1)\mathbf1[t>k_0]-(q+k_1)\mathbf1[t>q].
\]

The entire zero-route length changes by `q*1[q<k_min]-k0*1[k0<k_min]`. Merge variants have their own corrections. Both signed effects are kept. With `beta=3512863/10^6`, `delta=155223384/10^9`, the certificate gives

\[
A=3.591810178840039\ldots,\quad B=4.445350596843871\ldots,\quad
R=A+\max\{\ln2/h(\delta),B\ln2/\sigma(\delta)\}<5.197569.
\]

Only analytical rank one falls below the certified threshold `2.0718779`; its mass is capped by `2*delta*w`. Ranks two through seven and every zero waiting case are certified explicitly, and a monotone tail handles all remaining ranks. [Proof](next-expected.md), [exact certificate and 1,950 scheduling checks](next-expected-check.py), and [independent audit](next-results-audit.md) document the result. Pseudocodes are now local to their analyses, and repeated entropy inductions use one stage-to-tree lemma.

### Uniform expected-depth hardness

The [new hardness section](sections/08a-uniform-hardness.tex) replaces a weighted forest vertex of integer weight w by w uniform parabola points. Whole-cloud singleton and adjacent-pair tests are retained, and private singleton tests identify each cloud internally while leaving one anchor unqueried. A uniform singleton rotation removes premature private queries from the all-miss spine. The exact identity is

\[
\operatorname{OPT}_{\rm uniform,raw}
=\operatorname{OPT}_{\rm weighted,raw}
+\sum_i\frac{(w_i-1)(w_i+2)}2.
\]

Polynomially bounded weights therefore give a polynomial reduction establishing uniform expected-depth strong NP-completeness. The cloud identity holds for arbitrary adaptive trees, because a cost-nonincreasing singleton rotation removes private queries from the distinguished spine before any cloud is hit. The geometric and full Bellman checks are retained as support for that identity.

The cloud family inherits its EPTAS because adding the same fixed nonnegative cloud cost preserves approximation ratios. A constant-factor hardness proof therefore needs a different construction. The current manuscript intentionally omits shrinking-factor inapproximability and routine FPTAS consequences, and focuses on the substantive exact hardness results and the open constant-factor question.

### General polynomial maximum-depth improvement

The [new proof section](sections/06d-polynomial-slot-scheduling.tex) uses a Cartesian-tree DP for interval deadlines. State `([l,r],T)` retains the spatial region and a subset of available absolute query ranks. The earliest rank goes to a selected root point; all unhit intervals split entirely left or right, and the remaining ranks are partitioned between those children. Demands surviving in a region are exactly the original intervals contained in it. This gives exact scheduling in `O(M^3 3^L + N M^2)` time, with one additional factor `M` for circular first-block enumeration.

Fix `q=ceil(log2 original_n)`, `R=floor(gamma*q/(gamma-1))` and `L=R+1`. Every recursive stage builds its hybrid pattern children once, then chooses between the priority schedule and the capped exact schedule using those actual child heights. The two simultaneous invariants are

\[
C_W(S)\le3D+\lfloor\gamma\log_2|S|\rfloor,
\qquad D\le R\Longrightarrow
C_W(S)\le2D+\lfloor\gamma\log_2|S|\rfloor.
\]

The original-instance threshold survives restriction to every child. If the root optimum is small, the stronger invariant and `D>=log2 n` give `2+gamma=4.46496526`. If it exceeds `R`, integrality gives `D>gamma*q/(gamma-1)`, so the universal bound also gives a factor below `2+gamma`. The algorithm never needs the optimum as input. The zero route has a separate `floor(H/2)` total-block cap, and the terminal nonzero singleton append fits `D+1` slots.

An optional stronger variant inserts exact rectangular endpoint decoders with actual child heights directly into Cartesian-node feasibility. It remains polynomial and can improve complete trees, while retaining the proved factor. No smaller uniform factor follows merely from that replacement.

With `K=gamma/(gamma-1)<1.682611`, the smaller cap gives slot contributions `3^L=O(n^(K log2 3))` and `2^L=O(n^K)`, with exponents below **2.666874** and **1.682611**. These are the mask contributions, with other polynomial factors still present. The cap is a floor of a fixed rational times `q`, so its implementation is exact. [Cap certificate](simplification-worst-cap-check.py) checks the exponents and 10,000 integer boundaries.

[Proof and extensions](further-worst.md), [scheduler verification](further-worst-slot-dp-check.py), [endpoint verification](further-worst-endpoint-check.py), and [independent audit](further-w-audit.md) document the result. All 5,100 linear/circular scheduling comparisons and 1,200 endpoint comparisons passed. The natural deadline LP's fractional gap and earlier forced-prefix greedy examples remain valid, but do not obstruct this different algorithm.

### Earlier adaptive-mode factor below 5.272565

The [adaptive-mode proof section](sections/06e-adaptive-block-modes.tex) uses two modes for each edge block. Write `x<=y` for newly covered exclusive endpoint masses and `z` for shared mass. Stop mode saves `y`; query-both mode saves `x+y-z` physically and reveals an additional `(x+z)*H2(x/(x+z))` bits. Credit that information relative to a coarsened transcript that merges the first-positive exclusive/shared events. Every coarsened positive cell remains in one cap, retaining the smaller `delta` entropy cap.

With fixed rational `p*=21317/125000` and `h*=1-2p*`, use the rational entropy lower bound

\[
E_*(x,z)=\min\{(h_*/p_*)x,h_*(x+z),(h_*/p_*)z\},\qquad
D=\max\{y,x+y-z+E_*\}.
\]

Modes and the geometric shift minimize the exact rational surrogate `2*MSSC_blocks + 2*p0*K - sum D`. Concavity proves the affine credits `D>=0`, `D>=m-delta*w`, and `D>=c*m-d*delta*w`, where `c=228683/103683`, `d=250000/103683`. Exact first/second-batch coverage transfers each credit to the optimal witness's prefix masses. A fixed nine-row convex mixture counts the same actual saving once. With `beta=3512863/10^6`, `delta=144136826/10^9`, the rational certificate gives

\[
A=3.591810178840039\ldots,\quad
B=4.717880246118900\ldots,\quad
R=A+\max\{\ln2/h(\delta),B\ln2/\sigma(\delta)\}<5.272565.
\]

[Full proof](further-expected.md), [exact certificate](further-expected-check.py), [independent actual-circle checks](further-expected-audit-check.py), and [combined independent review](further-expected-audit.md) support this result. Verification passed 5,000 rational local-credit cases, 10,000 analytical profiles, 150 actual weighted circles, 1,350 table-row transfers, and 333 complete geometric shift schedules. All logarithms and analysis mixtures stay outside the tree-construction algorithm. The bound applies to arbitrary strictly positive rational priors, with no minimum-prior dependence.

### Further exact-prefix and hardness directions

The rank-subset DP also optimizes a weighted partial discovery prefix with fixed, additive completion penalties in polynomial time under a logarithmic cap. Every unresolved class pays for all `K` prefix blocks plus its point-specific cost in a fixed legal completion tree; query hits pay their first rank and actual endpoint continuation. Selecting the best resulting tree alongside the certified algorithm improves individual instances. The [proof and obstruction](further-expected-tail.md) and [900 exhaustive comparisons](further-expected-tail-check.py) make the remaining obstacle precise: recomputing a good completion on the unresolved union of Cartesian gaps is nonadditive. A small expected optimum does not bound witness length, and a uniform original-instance height multiplied by rare residual mass can lose an unbounded factor. A polynomial additive conditional-completion potential would be a promising route to a larger expected-depth improvement.

The [new hardness report](further-hardness.md) gives a concrete planar prefix obstruction. In each six-point parabola block, GOOD supplies caps of sizes `(4,2)` covering disjoint groups. BAD supplies a central four-point cap plus two disjoint three-point caps; its dominant first-hit patterns are `(4,1,1)` or `(3,3)`. All singleton tests are supplied. Across `M` blocks, both families have the same entire static maximum-coverage curve, yet

\[
\operatorname{OPT}_F(\mathrm{GOOD})=5M^2+3M,\qquad
\operatorname{OPT}_F(\mathrm{BAD})=\frac{11}{2}M^2+3M+
\frac{M\bmod2}{2}.
\]

Local identification adds only `O(M)` raw cost, so the optimal uniform expected-depth ratio also tends to **11/10**. This is a proved example, not an NP-hardness reduction. It exposes ordering incompatibility while every individual coverage budget is tractable. The precise missing hardness lemma is to couple these local choices to one gap-CSP assignment, charging violations `Omega(M^2)` while preserving the geometric incidences and static coverage profile. [Geometry and exact checks](further-hardness-check.py) passed.

For unrestricted maximum-depth hardness, the same report realizes arbitrary graph edge pairs by lines: `a_i=2^i`, `L_i:y=a_i*x+a_i^2`, and pair points `(-(a_i+a_j),-a_i*a_j) +/- (0,1/4)`. Exactly the two incident lines separate each pair. This pair-separation fact does not realize an arbitrary full test table or force a global vertex purchase. A commitment gadget must survive separate local choices, address routing, and promotion of supplied queries to the root.

### Earlier polynomial expected-depth refinements

The new [proof section](sections/06c-polynomial-block-improvement.tex) first obtains **5.312551** by applying the existing polynomial geometric-batch circular-interval scheduler to adjacent full-hull edges. A first positive endpoint in block rank `k` costs at most `2k-1` discovery queries plus four endpoint-code overhead queries. A positive second endpoint costs at most `2k` plus two, because the negative first endpoint pins one boundary. Thus ordinary block ranks give stage cost

\[
2\operatorname{MSSC}_{\mathrm{blocks}}+3b+2p_0K+(I-J)/\ln2.
\]

For a block's newly hit exclusive masses `x,y` and shared mass `z`, querying the smaller exclusive part first further saves `max(x,y)`. Choose the geometric shift by minimizing the rational surrogate `2*MSSC_blocks + 2*p0*K - Pin`. Exact first-batch coverage transfers this actual saving to the analytical witness profile: for first budget `k`, covered mass is at least witness prefix mass `M_k`, and `Pin >= (M_k-k*delta*w)_+`. This retains an additional average credit `delta*(3-ln(6)/ln(beta))` after combining positive and zero-route discounts.

This first-batch orientation transfer certifies **5.286244**. A convex mixture of first- and second-prefix lower bounds on the same actual orientation credit lowers the factor further. The mixture uses second-prefix coefficient `7963376/10^7` for shifts in `[1,4/beta)`, `952407/10^6` for `[4/beta,5/beta)`, one for `[5/beta,6/beta)`, and zero elsewhere. The two prefix credits are never added. A rational threshold `1.382412` lower-bounds all effective witness coefficients except indices one and three, whose masses are capped by `2*delta`.

With `beta=3512863/10^6` and `delta=142671046/10^9`, the final exact certificate gives

\[
A=3.591810178840039\ldots,\quad
B=4.766748469917878\ldots,\quad
R=A+\max\{\ln2/h(\delta),B\ln2/\sigma(\delta)\}<5.283310.
\]

The proof keeps the smaller `delta` cap on actual individual discovery exits, and the separate `2*delta` cap on analytical support-block masses. It uses polynomial interval coverage DPs, rational shift enumeration, and supplied endpoint queries. There is no bounded-cap, singleton-availability, fixed-direction, uniform-prior, or minimum-prior assumption. The logarithms occur only in the analysis.

The [baseline proof](poly-expected.md), [orientation transfer and mixed-prefix proof](poly-expected-next.md), and [exact certificate](poly-expected-next-check.py) document these earlier improvements. A separate [accounting audit](poly-accounting.md) checks the baseline and shows why a universal endpoint redundancy of three is false. The [independent orientation audit](poly-orientation-audit.md) verifies both refinements and the decreasing-coefficient accounting. The [deadline LP counterexample](poly-deadline-lp.md) gives a six-candidate fractional solution with no legal integral schedule and exact dilation gap `6/5`, including a transfer to edge-block demand lengths. Lossless rounding of that natural LP is therefore impossible; the new capped exact scheduler avoids the LP entirely.

### Earlier quasipolynomial and restricted algorithms

GPT-6 Luna implemented the first quasipolynomial TeX section. Six distinct normal agents then explored the six research directions, in waves because the concurrency limit includes the root. The root integrated and audited the stronger results that emerged.

The multigrade DP scans candidates in spatial order and stores each grade prefix's count and last selected position. Adjacent **full-hull edge blocks**, including an origin vertex as a free negative marker, preserve interval demands and cached-neighbor decoding credits. Scheduling the delay `first-hit block rank minus one` gives additive bounds

\[
B_W(S)\le 2\lambda\mathrm{OPT}_W(S)+\gamma\log_2|S|,
\qquad B_E(S)\le2\lambda\mathrm{OPT}_E(S)+c\mathcal E(S).
\]

The direct certified ratios are below **4.464966** and **3.7187**. They are intermediate results; the strongest broad guarantee is obtained by exact optimization of a logarithmic-depth initial tree with these baseline continuations. The reachable states number `(2m)^{O(k)}`, rather than the number of all labelled trees.

For maximum depth, a surviving optimal frontier state has residual height at most `D-k`, and `k >= gamma log2 n/(a-1)` pays for its count potential. For expected depth, write `P` for the optimal prefix cost and `q` for mass reaching depth `k`. Then `P >= kq`, and frontier entropy is at most `q ln n`. The baseline continuation costs at most

\[
a\mathrm{OPT}_E-(a-1)P+cq\ln n
\le a\mathrm{OPT}_E+[c\ln n-(a-1)k]q.
\]

Thus `k >= c ln n/(a-1)` removes the entire entropy surcharge. Choosing `a=2lambda=2+epsilon` proves both guarantees in `(mn)^{O(epsilon^-1 log n)}` time. This approaches two; it is not a `(1+epsilon)` QPTAS for the general problem.

| Agent direction | Concrete outcome | Next target |
|---|---|---|
| [1. Schedule compression](direction1-schedule-compression.md) | General polynomial W `4.46496526` via rank-subset cap and fallback | Probability-weighted tail completion for polynomial E; compatible whole-exit height analysis |
| [2. Joint discovery and decoding](direction2-joint-decoding.md) | General polynomial E `<5.182976` after two initial-budget changes; rational entropy modes; exact endpoint DP | Couple later phase masses and conditional completion costs |
| [3. Original caps and restriction credit](direction3-cap-accounting.md) | Independent `(2+epsilon)` rollout proofs | Prove an additive coefficient `alpha<2` using actual optimum decrease for an original-cap output partition |
| [4. Shallow ordered cover hardness](direction4-shallow-cover-hardness.md) | Uniform E strong NP-completeness; uniform bounded-cap convex-position PTAS | Escape bounded cyclic caps and prove robust global choice coupling |
| [5. Robust coupled gadgets](direction5-robust-gadget-hardness.md) | Query-promotion and independent-routing barriers; broader uniform matching exactness | Persistent-client extraction with one global assignment and a gap comparable to full tree cost |
| [6. Weighted pair forests](direction6-pair-forest-ptas.md) | EPTAS via sparse deletion, heavy enumeration, convex configuration relaxation and rounding | Extend legal splitting or bounded-component deletion to richer weighted geometric cap families |

The EPTAS uses the exact sorted matching invoice. Its rank cost equals one half of the integral of `Z(t)^2+Z(t)`, where `Z(t)` counts groups above mass threshold `t`. Sparse path/cycle cuts lose at most `OPT/K`. Enumerate the components containing the heaviest `H` vertices, then solve a convex configuration relaxation on the small remaining components. Independent rounding costs at most `B*OPT/(H+1)` by variance and a vertex-rank tail bound, and conditional expectation makes the output deterministic. Choosing `K=ceil(3/epsilon)`, component bound `B=2K`, and `H=ceil(3B/epsilon)` proves the EPTAS. All-singleton availability is essential.

For fixed cap size `b`, minimum halfplane cover gives `K <= OPT_W <= K+b-1`. Guess at most `b-1` witness-spine suffix queries and their at most `b(b-1)` surviving points. Exact cover of the remaining points, restricted to caps missing the guessed survivors, supplies the prefix. Exact small positive-exit codes verify the suffix. This decides each of the `b` candidate heights in `m^{b-1}2^{O(b^2)} poly(n,m,input bits)` time.

Uniform-prior strong NP-completeness is now established; APX hardness remains open. The new bounds also constrain possible gaps: under ETH, a polynomial-size 3-SAT reduction to a fixed gap above two would conflict with the general quasipolynomial algorithms. Gaps at or below two remain possible. Bounded-cap height, uniform convex-position bounded-cap expected depth, and the full-singleton pair-path weighted expected subclass have stronger algorithmic obstructions.

The sections below retain the first exploration's derivations and source analysis. Their **4.764/3.835 bounds, pair-class QPTAS, statements that polynomial scheduling improvement is still needed, and statements that uniform-prior hardness is unresolved are superseded by the results above**, but their intermediate derivations remain valid.

## 1 Existing guarantees and the losses to attack

Before these polynomial improvements, the [manuscript](planar-line-decision-trees.tex) established factors below 5.464966 for maximum depth and 5.445944 for arbitrary-prior expected depth. They are now superseded by 4.464966 and 5.182976 above. Its strong NP completeness reductions use points on a parabola. Convex position or a single convex layer therefore cannot make the general exact problem easy.

For maximum depth, the current induction has the form

\[
H(S)\le 3D(S)+\lfloor\gamma\log_2|S|\rfloor.
\]

The coefficient three comes from simultaneous discovery deadlines. The remaining potential pays for endpoint identification and shrinkage. For expected depth, the current discovery coefficient is about 3.592; the analysis then pays for endpoint information and up to four additive endpoint queries per nonzero pattern, with useful cached neighbor credits sometimes discarded.

Changing only the numerical balance threshold gives little improvement because the current proof already optimizes that threshold closely. The substantive opportunities are a better scheduling primitive, a better complete pattern decoder, or a different accounting potential.

## 2 Quasipolynomial maximum depth below 4.764

Replace deadline priority greedy by exact feasibility for a logarithmic number of rounded deadline levels. This sacrifices polynomial time while preserving the original supplied query family.

### Exact interval deadlines with few levels

Let candidates be spatially ordered and let interval demands have deadlines \(d_1<\cdots<d_r\). Assign each selected candidate a grade, meaning the deadline bucket in which it will be queried. Scan candidates in spatial order. Store, for every grade prefix, its selected count and last selected position. Selecting a candidate at grade \(j\) updates both records for all prefixes at least \(j\). When an interval ends, its deadline prefix must have a last selected position within that interval. Impose the cumulative count bound at every deadline.

This is an exact dynamic program with \((mn)^{O(r)}\) states when counts are capped by a trial height of \(O(n)\). Listing selected candidates in grade order yields a feasible query schedule. For circular intervals, enumerate the first query, discard demands hit there, and cut the circle there. The forced query consumes one unit in every remaining prefix count.

Independent minimum covers for each deadline are insufficient. On candidates \(1,2,3\), give \([1,2]\) and \([2,3]\) deadline one, and \(\{1\}\), \(\{3\}\) deadline two. Each deadline prefix has a cover of the required size, but no nested schedule works: its first query must be 2, and both 1 and 3 would then be needed by time two.

### The new induction

Take fixed rational \(\lambda=1+\eta>1\), \(a=2\lambda\), and parameters satisfying

\[
\gamma\log_2\frac1{1-\delta}\ge1,
\qquad
\gamma\log_2\frac1\delta\ge a+4,
\qquad \gamma\ge1.
\]

Use the target \(H(S)\le\lfloor aD(S)+\gamma\log_2|S|\rfloor\). At a flat state, build every hull pattern child first. Its actual height determines the discovery budget after reserving the manuscript's general endpoint allowance.

For a class \(A\), write \(x=\log_2(|S|/|A|)\), \(L=\log_2(1/\delta)\), and let \(t\) be its first supporting block on an optimal witness path. The existing restriction lemma gives \(D(A)\le D(S)-(t-1)\). At the proposed parent height the residual discovery budget satisfies

\[
\begin{aligned}
B_A
&\ge \lfloor a(t-1)+\gamma x\rfloor-\lfloor x-L\rfloor-4\\
&\ge \lfloor a(t-1)+(\gamma-1)x+L\rfloor-4\\
&\ge \lfloor at\rfloor.
\end{aligned}
\]

Round this budget down to the largest distinct level \(\widehat B_A=\lfloor\lambda^j\rfloor\le B_A\). Maximality gives

\[
\lambda^{j+1}\ge B_A+1>at,
\qquad \widehat B_A>2t-1.
\]

Thus \(\widehat B_A\ge2t\). Expanding every optimal witness query into its at most two hull supports hits every class by time \(2t\), so it supplies a feasible comparison schedule for the rounded deadline DP. The algorithm enumerates its first vertex without knowing the optimal tree. Include the forced query in all counts, permit the manuscript's appended terminal positive vertex, and impose a total schedule length cap at the trial height. These checks also cover the zero pattern route.

There are \(O(\log n/\eta)\) deadline levels. The resulting time is \((mn)^{O(\log n/\eta)}\), and the factor is \(a+\gamma\). At \(\eta\to0\), the best threshold satisfies

\[
\delta=(1-\delta)^6,
\quad \delta\approx0.2219104013,
\quad a+\gamma\to4.7624935097.
\]

A concrete rational choice is \(\lambda=2001/2000\), \(a=2001/1000\), \(\delta=2219/10000\), \(\gamma=2763/1000\), giving **4.764**. Rational logarithm intervals certify both parameter inequalities.

The polynomial research target is now precise: compress the grade vectors, or prove simultaneous deadline dilation strictly below three, while retaining actual child heights. Exact coverage at separate budgets does not solve that problem.

## 3 Quasipolynomial expected depth below 3.835

The same spatial dynamic program can minimize weighted first cover cost rather than merely test deadlines. This removes most of the geometric batching loss from discovery.

Let \(d_j\) be the distinct integer levels \(\lfloor\lambda^j\rfloor\), up to a level covering all useful query ranks. After a forced first query and the circular cut, assign grades to remaining candidates. When a demand interval reaches its right endpoint, find the smallest grade prefix whose last selected candidate lies inside the interval and charge its weight times \(d_j\). At the end, charge the zero pattern's weight times the actual total selected count. Every demand receives one charge, and every selected query is shared by all demands.

For an actual query rank \(k\), the smallest rounded level at least \(k\) is less than \(\lambda k\), because the preceding power is less than \(k\). The grade ordering's actual cover time is at most its charged level. Therefore the DP approximates the joint objective of positive first cover times and zero pattern waiting time within factor \(\lambda\). An optimum ordering has at most \(n\) useful queries, so the number of levels is \(O(\log n/\eta)\).

Let \(\Delta\) be the optimum cost decrease after restriction to full hull pattern classes, \(b\) the nonzero pattern mass, \(I\) the full pattern information, and \(J\) the discovery information, all with the manuscript's unnormalized state weights. Order an optimal witness query's two supports so the heavier newly hit mass comes first. Their average first hit is at most \(2t-1/2\). The existing supporting prefix credit then gives

\[
W_{\rm discovery}\le2\lambda\Delta+\frac32\lambda b.
\]

The zero pattern is included: its comparison cover length is at most twice the witness path length. If there is no zero pattern, the terminal singleton can be appended without adding a waiting term.

Adding the existing endpoint decoder gives

\[
W_{\rm stage}\le2\lambda\Delta+
\left(4+\frac32\lambda\right)b+\frac{I-J}{\ln2}.
\]

In a mass flat state the capped discovery entropy lemma gives \(J\ge b\sigma(\delta)\), where

\[
\sigma(\delta)=-k\delta\ln\delta-r\ln r,
\qquad k=\lfloor1/\delta\rfloor,
\quad r=1-k\delta.
\]

With \(h(\delta)=-\delta\ln\delta-(1-\delta)\ln(1-\delta)\), set

\[
c=\max\left\{\frac1{h(\delta)},
\frac{4+\tfrac32\lambda}{\sigma(\delta)}\right\}.
\]

Then the whole stage costs at most \(2\lambda\Delta+cI\). Optimum restriction decreases and entropy decreases telescope through recursion. The global factor is

\[
R=2\lambda+
\max\left\{\frac{\ln2}{h(\delta)},
\frac{(4+\tfrac32\lambda)\ln2}{\sigma(\delta)}\right\}.
\]

Taking \(\lambda=2001/2000\) and \(\delta=3141/25000\), exact logarithm bounds certify both terms in the maximum below \(917/500\), so **\(R<3.835\)**. The runtime is quasipolynomial. Numerical optimization as \(\lambda\to1\) suggests a limit about 3.833422 near \(\delta=0.12566495\); the explicit 3.835 bound has a rational certificate.

This improves arbitrary prior expected depth at a higher time cost. A polynomial improvement still needs a more efficient schedule or stronger local charging.

## 4 Polynomial algorithms worth developing

### Joint endpoint decoding

After one positive hull vertex and the free geometric cut, every pattern is an endpoint pair \((L,R)\) containing that vertex. Every further hull test compares one endpoint to a threshold. Transcripts restrict the realized endpoint pairs to axis aligned rectangles, giving \(O(m^4)\) states and \(O(m^5)\) transitions.

At a rectangle containing only pattern \(A\), use the actual recursive child height or raw expected cost. Else use the ordinary minimax or weighted Bellman recurrence over splitting endpoint thresholds. This computes the best joint decoder among these hull tests and permits left and right endpoint questions to interleave.

It can only improve on the sequential endpoint codes. For maximum depth, varying child heights affect the best decoding tree. For expected depth, fixed child costs sum to a constant over all pattern leaves, so continuation penalties alone do not change the best weighted decoder; they matter when comparing different partial macros or partitions.

The missing global theorem is a stronger redundancy bound. A generic replacement of entropy plus four by entropy plus three is unsafe: an almost certain internal endpoint pair can require two threshold certifications per coordinate. A better result must use flatness, cached answers, or geometric constraints.

### Schedule discovery for complete exit cost

The existing expected analysis earns \(-2b_{\rm pin}-2b_{\rm both}\) when cached negative neighbors fix endpoints. Keep this credit in the scheduling objective. For an adjacent pair with exclusive masses \(x,y\) and shared positive mass \(z\), the generic discovery plus endpoint allowance is \(5(x+z)+4y\) in one orientation, and \(5(y+z)+4x\) in the other. Under this allowance, querying the smaller exclusive mass first helps complete decoding, even though first cover latency alone prefers the opposite order.

Try adjacent block schedules, a relaxation recording pinned exits, or local exchanges evaluated by the exact joint decoder. The intermediate theorem should bound complete stage cost by \(\alpha\Delta+cI\) with \(\alpha+c\ln2<5.445944\). A universal positive pinning fraction is not automatic: long overlapping intervals can exit before any useful negative neighbor is cached.

### Original caps with new restriction accounting

Planar supplied halfplane cover is exactly polynomial, and the geometric DP also has an exact maximum coverage adaptation. These are stronger primitives than the two support surrogate. [Har Peled and Lee](https://jocg.org/index.php/jocg/article/view/2950), [Badanidiyuru, Kleinberg and Lee, Appendix B](https://arxiv.org/html/1112.0689).

The obstruction is class constancy. Original interior query vectors can distinguish hypotheses with the same hull pattern. A hypothesis's late first hit on original caps need not yield a long common prefix that disappears when an entire output class is revealed. Refining an algorithm's exit by the hull pattern does not automatically make the unknown comparison tree's earlier queries constant on that class.

Seek a mixed original and hull macro, or a quantitative restriction lemma paying for this discrepancy with additional information. Removing the two support factor without such a lemma is an invalid shortcut.

### Continuation aware lookahead

One step rollout evaluated with complete baseline subtrees cannot worsen that baseline. For a \(\rho\) approximate expected baseline it gives \(C\le\rho\mathrm{OPT}-(\rho-1)\) at a normalized nontrivial root. For a \(\kappa\) approximate maximum depth baseline it gives \(H\le\kappa\mathrm{OPT}-(\kappa-1)\). Fixed deeper lookahead is polynomial with a large degree.

These are useful practical and instance sensitive improvements, not smaller leading worst case constants when the optimum grows. Their role is to generate better continuation codes and identify recurring geometric traps.

## 6 Why the current reductions do not give a fixed factor gap

The height construction certifies \(K\) versus at least \(K+1\), hence only ratio \(1+1/K\). Its soundness relies on a tight distinguished path. A tree allowed \(\varepsilon K\) extra queries can damage clouds early or use imperfect matchings, so a new normalization theorem is required even before amplification.

The expected construction has a quadratic deviation penalty, but its large witness and padding costs dominate that penalty. The certified gap is of order \(V\), while a compulsory raw baseline is at least \(Vr^3/2\) for the padding parameter \(r\). Multiplying weights multiplies both. Subtracting the baseline is useful for an exact threshold proof and cannot be done in a multiplicative approximation guarantee.

Moreover, independent identical bin load balancing is approximation friendly; the relevant convex load objectives admit approximation schemes. A shifted zero at exact balance is an exactness detector, not automatically an APX hard source. [Alon, Azar, Woeginger and Yadid](https://web.math.princeton.edu/~nalon/PDFS/aawy2.pdf).

For a fixed witness, its shortest certificate is a cover by halfplanes opposite that witness. Exact geometric cover therefore prevents a direct import of Set Cover hardness in which that one certificate is the entire objective. Constant gap hardness must involve query order, continuation costs, or interactions among several paths.

## 7 Three hardness projects with explicit proof obligations

### Shallow ordered halfplane cover

First classify min sum first cover time on planar points with supplied halfplanes of bounded cap size, all excluding a common strict witness. Require the signs to separate the source points. This is a geometrically faithful scheduling source rather than an arbitrary incidence matrix.

There is a clean conditional transfer. With \(N\) unit weight source points, caps of size at most fixed \(b\), and \(m\) supplied queries, add the witness with raw weight \(1/m\). Let \(F^*\) be optimal ordered cover cost and \(G^*\) optimal raw identification cost. Following the witness through any tree gives an ordered cover. Conversely every cover's first hit group has at most \(b\) hypotheses and can be identified with at most \(b-1\) more queries. Thus

\[
F^*\le G^*\le F^*+(b-1)N+1,
\qquad F^*\ge\frac{N^2}{2b}.
\]

The additive distortion is \(O(b^2/N)\). Fixed gap hardness for this source would transfer to identification without a dominant witness baseline. Its source hardness is unproved here. The new PTAS rules out this identification-hardness route for uniform convex-position fixed-size caps with an actual all-miss hypothesis. A source reduction must escape at least one of these conditions; merely increasing a fixed cap size is insufficient.

### Robust coupled assignment gadgets

Replace independent bin choices by eligibility, machine dependent loads, or coupled Boolean constraints. The desired expected identity is

\[
G(T_x)=A+B\,\operatorname{viol}(x),
\qquad A\le cBM,
\]

with a source gap of at least \(\delta M\) violations. This yields ratio at least \(1+\delta/c\), provided arbitrary adaptive trees admit a quantitatively controlled normalization to assignments.

Establish that normalization first: every illegal local choice or extra query must be chargeable to excess cost. Then build rational planar gadgets and verify every supplied query's effect on every hypothesis. Exact threshold exclusions and intended query orders do not establish robust soundness. For maximum depth, penalties must serialize on one path or a violation must create a branch whose additional height is a constant fraction of the entire yes depth.

### Several witnesses and consistency

Investigate whether several high mass branches force incompatible cheap local query choices. Start with a small rational gadget catalogue: two variable choices, one consistency relation, and a quantitatively expensive violation. Search realizable order types and optimize each proposed gadget by exact subset DP.

The central obligations are that early queries cannot evade the intended gate, all adaptive trees can be normalized, and enforcing consistency costs only a constant fraction of the final baseline. Planar line sign matrices have sign rank at most three, with additional realizability constraints; an abstract bounded occurrence test table is not enough.

## 8 The weighted singleton and pair subclass admits a QPTAS

Assume one distinguished hypothesis misses every designated cap, every other hypothesis has a supplied singleton cap, and the remaining designated caps contain two nonzero hypotheses. For a matching \(M\), the manuscript's exact invoice is

\[
G(M)=w_0(N-|M|)+\mathcal C(J(M))+
\sum_{uv\in M}(w_u+w_v).
\]

Here \(J\) contains singleton and matched pair group masses and \(\mathcal C\) is the completion sum in decreasing mass order. In the planar model the full singleton supply forces every nonzero point onto the convex hull; pair caps join adjacent hull vertices. The graph is therefore paths and possibly a cycle.

Let \(\Omega\) be the original total weight and \(\tau=\eta\Omega/n^2\). Raise each nonzero weight below \(\tau\) to \(\tau\), keeping \(w_0\) exact. Precompute a rounded bucket for every singleton mass and every available pair mass, using powers of \(1+\eta\). There are \(L=O(\eta^{-1}\log(n/\eta))\) buckets.

Use path matching DP with only two counts per bucket: singleton groups and pair groups. Evaluate the surrogate invoice

\[
A(M)=w_0(N-|M|)+\mathcal C(J_\beta(M))+
\sum_{e\in M}\beta_e.
\]

Rounded pair masses need not be sums of rounded singleton masses. The surrogate remains valid because the delivered legal tree, ordered by bucket mass, has original cost at most \(A(M)\). Weight flooring adds at most \(\eta\Omega\le\eta\mathrm{OPT}_{\rm raw}\) to every proper tree, and group mass rounding multiplies the raised invoice by at most \(1+\eta\). Hence minimizing the surrogate gives cost at most \((1+\eta)^2\mathrm{OPT}\).

With \(\eta=\varepsilon/3\), this is a **QPTAS in \(n^{O(\varepsilon^{-1}\log(n/\varepsilon))}\)** for \(0<\varepsilon\le1\), with ordinary polynomial bit arithmetic. It covers the existing weighted expected hardness subclass. Removing the logarithmic number of mass buckets is a focused PTAS project. Under ETH, fixed gap NP hardness for this subclass would conflict with its quasipolynomial approximation scheme; richer gadgets are a better hardness target.

## 9 Exact control classes and uniform hardness

Uniform singleton and pair instances are polynomially solvable. If a maximum matching has size \(r\), the raw expected optimum is

\[
G(r)=\frac{N(N+3)}2-(N-1)r+r^2,
\]

and the height is \(\max\{N-r,r+1\}\). Divide the expected invoice by \(N+1\). Maximum matching attains both optima. Therefore uniform expected hardness needs larger caps, nontrivial continuations, or a different architecture. Replacing weight by copies changes internal identification costs and the available queries and requires its own proof.

With \(k\) line directions, every transcript is an intersection of \(k\) projection slabs. There are at most \((m+1)^{2k}\) state descriptions, giving exact algorithms in \((m+1)^{O(k)}\operatorname{poly}(n)\). This is XP in \(k\), not an FPT claim. Constant directions, including axis parallel lines, are unsuitable for hardness in this identification model.

Concurrent supplied lines are also exactly tractable. After the root query each answer class lies in an angular semicircle; all remaining lines restrict to thresholds, and separability supplies every adjacent threshold. Solve alphabetic subproblems and optimize the root. These cases provide good baselines for experiments and local exact replacements.

## 10 Suggested order of work

1. Benchmark complete hybrid trees with whole-exit endpoint optimization against exact small-instance optima, including correlated endpoints and unequal child heights.
2. Seek a joint anchor/rank/child-height argument that lowers the maximum-depth decoding potential; an endpoint-only aggregate estimate is insufficient.
3. Extend exact capped scheduling to expected depth by charging rare long tails and their recursive continuation costs. The maximum-depth small/large optimum dichotomy alone does not transfer.
4. Strengthen expected-stage accounting with disjoint phase credits, or prove an original-cap output partition that supports restriction credit. Exact original halfplane coverage alone does not supply that partition.
5. Develop an unbounded-cap or no-all-miss planar gap gadget with one committed global assignment. Uniform strong NP-completeness is now proved; the next target is a constant relative gap, which the cloud transfer does not preserve. Avoid the exactly solvable bounded-cap all-miss subclass.
6. Extend the weighted pair-path EPTAS to richer legal geometric cap systems; keep all-singleton availability and legal group splitting explicit.

## Supporting reports and checks

- [Approximation report](agent-approximation-routes.md): scheduling proofs, joint decoding, original cap accounting, and lookahead directions.
- [Hardness report](agent-hardness-routes.md): gap algebra, geometric restrictions, robust normalization, and the conditional shallow cover reduction.
- [Structural report](agent-structural-routes.md): exact classes, group mass QPTAS, and independent proof checks.
- [Scheduling checks](agent-approximation-check.py), [structural checks](structural-route-checks.py), and [additional checks](planar-research-checks.py): finite exact comparisons and rational parameter certificates. These support the derivations and do not replace their proofs.

The latest broad polynomial factors are **4.464966** and **5.182976**, with independent audits and exact certificates. General quasipolynomial factors remain `(2+epsilon)`. Uniform expected depth is strongly NP-complete. Constant-factor inapproximability remains open; size-dependent gaps are omitted from the manuscript. No APX-hardness theorem or general polynomial factor below two is established. Literature-wide novelty of these new derivations is not established.
