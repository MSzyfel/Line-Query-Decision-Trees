# Inapproximability routes for planar supplied-line identification trees

Research audit, 13 October 2026. This report concerns binary, unit-cost supplied-line queries and the exact model of the current manuscript. It does not modify the manuscript. Results labelled **proved observation** follow from the manuscript or the arguments below; routes labelled **candidate** have essential unproved obligations.

## 1. An immediate, rigorous upgrade: no FPTAS

**Proved observation.** Unless P = NP, neither maximum-depth optimization nor arbitrary-prior expected-depth optimization has an FPTAS in this model.

For maximum depth, every proper identifying tree has integer cost at most n−1. Run a hypothetical FPTAS with ε = 1/[2(n−1)]. Its output satisfies

\[
\operatorname{OPT}_W\le H_A\le(1+\varepsilon)\operatorname{OPT}_W
 <\operatorname{OPT}_W+1.
\]

Since H_A is integral, it is optimal. The runtime is polynomial because 1/ε is O(n). Ordinary NP-hardness already suffices here; strong NP-hardness is unnecessary.

For expected depth use the manuscript's hard restriction with positive integer raw weights, total Ω, and Ω bounded by a fixed polynomial in n. The raw cost G(T)=Σ_h ω_h d_T(h) is integral and at most Ω(n−1). Running a hypothetical FPTAS with ε=1/[2Ω(n−1)] returns a tree of raw cost below OPT_G+1 and therefore solves the exact hard problem. Here the polynomial bound on Ω is essential. Arbitrary binary-encoded rational priors do not themselves give a polynomial-size cost grid.

This establishes inverse-polynomial-factor hardness, not a fixed factor greater than one. In particular it does **not** exclude a PTAS. The expected-depth conclusion concerns the arbitrary-prior problem; it does not establish hardness under a uniform prior.

## 2. Why the present 3-Partition constructions do not give APX-hardness

### Maximum depth

The reduction distinguishes height K from height at least K+1, with

\[
K=q+m+2,\qquad q=(p-1)(4s+2m).
\]

Its certified ratio is only 1+1/K. More seriously, several soundness arguments use equality of the distinguished path length to K. An approximately optimal tree of height (1+ε)K may use Θ(εK) extra private or singleton queries, need not preserve full clouds at exits, and need not induce the maximum matchings used in the histogram calculation. One cannot apply the exact matching normal form to such a tree without a separate robust-normalization theorem.

Replicating item blocks or multiplying cloud sizes does not automatically fix this: the number of compulsory spine queries and the local exit baselines grow with the signal. A genuine constant-gap construction needs either a violation cost comparable to the entire yes-instance depth, or many violation costs that necessarily serialize on one path.

### Expected depth

The boundary-matching identity is

\[
G=G_{\rm base}+\frac V2\sum_b(L_b-B)^2+e,
\qquad -E_-\le e\le E_+.
\]

The proved no-instance separation from the yes threshold is

\[
V-E_--E_+>0.9985V.
\]

But with r medium-weight isolated vertices,

\[
W\ge rV/2,\quad
\omega_0=(N+1)W+1,\quad
d_T(0)=q+m+r\ge r,
\]

so every normalized boundary solution's raw baseline is at least

\[
\omega_0(q+m+r)\ge Vr^3/2.
\]

The currently certified signal-to-baseline ratio is therefore O(r^{−3}), even before other fixed costs are counted. Increasing V scales both signal and baseline. Increasing the distinguished weight or the padding only worsens this ratio. Subtracting G_base in the analysis is legal for exact threshold reduction, but an approximation ratio is measured on the original nonnegative cost and cannot subtract that baseline.

The dominant witness also forces maximum matching only for an exact optimum. A constant-factor approximation may spend Θ(ε(q+m+r)) additional queries on it. Approximation-preserving soundness must allow imperfect matchings and recover a comparably good source solution.

There is a conceptual source barrier too. Identical-machine makespan and the unshifted quadratic load objective Σ_b L_b² admit PTASs. A fixed relative overload gap for unrestricted bin assignment cannot be obtained by treating 3-Partition as though it were APX-hard load balancing. [Alon, Azar, Woeginger and Yadid](https://web.math.princeton.edu/~nalon/PDFS/aawy2.pdf) give approximation schemes for suitable convex load objectives, including powers. The shifted zero-at-balance variance is an exactness detector, but that fact does not make the original decision-tree baseline disappear.

## 3. Three geometric barriers that should guide reductions

### A dominant witness encodes a polynomial-time cover problem

Fix a hypothesis p. For each supplied line take its open halfplane on the side opposite p. The minimum number of lines that certify p against all other hypotheses equals the minimum number of these supplied halfplanes covering H\{p}. Covering planar points by supplied weighted halfplanes is exactly polynomial-time solvable; see [Har-Peled and Lee, *Weighted Geometric Set Cover Problems Revisited*, JoCG 2012, §3](https://jocg.org/index.php/jocg/article/download/2950/2644/7396).

Thus a reduction in which one overwhelmingly likely witness's certificate length is the whole hard objective cannot import arbitrary Set Cover or Vertex Cover hardness. Hardness must survive in ordering, exit identification, several interacting branches, or another resource beyond that static certificate.

### A fixed number of directions admits exact state dynamic programming

**Proved observation.** If supplied lines have k fixed directions, both objectives are exactly solvable in m^{O(k)} poly(n) time.

Along a direction, every query is a threshold on one scalar projection. A transcript retains an interval of allowable projections, determined by at most one lower and one upper supplied threshold. There are O((m+1)²) choices per direction. A state is the hypothesis set in the intersection of these k projection intervals, so there are at most (m+1)^{2k} distinct states. Enumerate them, identify equal subsets, and evaluate the manuscript's Bellman recurrences in increasing state cardinality. Every nontrivial transition strictly decreases cardinality, and rational expected costs have polynomial arithmetic bit complexity.

In particular horizontal/vertical supplied-line trees are exactly solvable. APX-hardness of **nonadaptive** axis-parallel point separation is not an APX-hardness proof for these adaptive objectives. Nor is a constant number of arbitrary orientation families enough for a hardness gadget.

### Two-point caps are strongly restricted

**Proved observation.** Draw an edge for every supplied halfplane whose selected side consists of exactly two hypotheses. This graph is straight-line planar. If two vertex-disjoint edge segments crossed, the halfplane selecting the endpoints of one would contain that segment and exclude the whole other segment, an impossibility.

There is a stronger restriction when every nonzero hypothesis has a supplied singleton cap and all caps exclude one distinguished hypothesis. Singleton separability makes every nonzero point an exposed convex-hull vertex. A halfplane selects a consecutive hull block, so a two-point cap can connect only adjacent hull vertices. The pair graph consequently has degree at most two: paths and possibly a cycle. If the witness is a hull vertex, it breaks the cycle. This explains why the manuscript's parabola realization naturally yields a linear forest.

The exact singleton/pair invoice cannot therefore be generalized directly to arbitrary planar graphs while retaining all private singleton tests. Dropping singleton availability introduces scheduling and local-continuation constraints that require a new formula.

## 4. Uniform singleton/pair instances are exactly tractable

**Proved observation.** Give all N nonzero vertices and the distinguished point weight one. For a matching of size r let k=N−r. The invoice has r group masses 2, N−2r group masses 1, and paired exit cost 2r. Hence

\[
\mathcal C(J)=\frac{k(k+1)+r(r+1)}2,
\]

\[
G(r)=k+\mathcal C(J)+2r
=\frac{N(N+3)}2-(N-1)r+r^2.
\]

For every feasible successive increment,

\[
G(r+1)-G(r)=2r-N+2\le0.
\]

The final increment ties when N is even; otherwise it strictly improves. A maximum-cardinality matching is optimal, computable in polynomial time. Divide G by N+1 for the uniform expected depth. This uses the full singleton/pair invoice and needs no dominant witness.

For example N=2 gives raw optimum 5 whether one queries the pair first or uses singleton queries. This sanity check rules out the alternative expression with r(r−1)/2 in place of r².

Therefore the weighted expected-depth construction does not immediately prove uniform-prior hardness. Replacing a point of weight w by w ordinary copies changes the local identification objective. With only private singleton queries their local raw depth sum is (w−1)(w+2)/2, a quadratic addition. Adding balanced within-cloud tests can introduce extra root-level queries and change the matching mechanism. A uniform-hardness reduction needs a construction-level audit of those extra tests.

## 5. A useful robust cost lemma: splitting matched groups

Consider any valid singleton/pair schedule in the exact-invoice regime. Its original groups have masses m_1,…,m_k in their chosen order. For a paired group j with individual weights a≥b, replace its pair query and one-query local identification by singleton a followed by singleton b.

The group's original raw contribution is (j+1)(a+b). Its new contribution is ja+(j+1)b. Thus its own contribution decreases by a. Every later group and the distinguished point gains one query. The exact change is

\[
\Delta_j=R_j-a,\qquad
R_j=\omega_0+\sum_{\ell>j}m_\ell.
\]

Write ρ_j=ω_0+Σ_{ℓ≥j}m_ℓ, the raw mass queried at the original spine node. Then Δ_j≤ρ_j. Splitting several original pairs adds these Δ_j exactly: the total mass after each original group does not change. Since Σ_jρ_j is precisely the spine contribution and is at most G,

\[
\Pr[\text{each original matched edge is removed}]\le\eta
\quad\Longrightarrow\quad
\mathbb E[G_{\rm split}]\le(1+\eta)G.
\]

No independence is needed. This is a rigorous approximation-friendly normalization lemma. It applies where the requisite singleton tests exist. It could support decomposition/rounding algorithms for forest/cycle instances. A Baker argument for general planar pair graphs would additionally need a legal way to perform these singleton splits and a new continuation-aware dynamic program; that extension is not proved.

## 6. Candidate route A: ordered shallow halfplane cover, with a precise transfer lemma

This is the cleanest source problem to isolate before attempting a full APX reduction.

**Source primitive.** N planar points, m supplied caps excluding a rational strict witness p, all caps of size at most b=O(1). Their signs must separate every pair of source points, and the caps must cover the points. Minimize the uniform sum F of first-cover positions in an ordering of the caps. Its approximation complexity in this geometrically restricted regime is not established here.

**Proved conditional transfer.** Add p as a hypothesis of raw weight γ=1/m; all N source points have raw weight one. For any identifying tree, p's all-miss spine gives a cover ordering, and first-exit depth is no greater than total leaf depth. Thus F*≤OPT_G.

Conversely, a cover ordering first discovers a group A_j of size at most b at each hit. Existing separating queries identify A_j in at most b−1 additional queries. The witness uses at most m queries, so

\[
F^*\le\operatorname{OPT}_G\le F^*+(b-1)N+1.
\]

Moreover F*≥Σ_{i=1}^N ceil(i/b)≥N²/(2b). The additive distortion is O(b²/N). A returned tree yields its source ordering with F(T)≤G(T), so a PTAS for the tree problem would give a PTAS for this source primitive after treating bounded N by exhaustive search. Equivalently, fixed-gap APX-hardness of this explicit source would transfer without an enormous witness baseline. Multiplying all weights by m makes the prior come from positive polynomial-size integers.

**Missing obligation:** prove fixed-gap hardness of the source while satisfying its geometric realization and pair separation. General MSSC's 4−ε hardness does not prove this. Uniform two-element cover is matching-like, so b=3 is the first useful shallow test case. Geometric decomposition could instead produce a PTAS for this source, which would still be valuable information.

**First experiments/proofs:** enumerate small realizable three-point caps, optimize their latency exactly, test whether the convex layers yield a bounded-width decomposition, and search for a constant-size local gadget with two choices and a robust latency difference. Do not presume an arbitrary bounded-frequency incidence table is realizable by planar lines.

## 7. Candidate route B: replace independent bins by coupled assignment constraints

The present path-transfer mechanism can encode independent item-to-bin choices but independent identical-bin load balancing is approximation-friendly. A more promising source is a genuinely gap-hard assignment problem with eligibility restrictions, machine-dependent loads, or coupled Boolean choices.

The desired cost identity is

\[
G(T_x)=A+B\,\operatorname{viol}(x),\qquad
A\le cBm,
\]

for a source with m constraints and a promise of zero violations versus at least δm violations. Then the multiplicative gap is at least 1+δ/c. For height, replacing Σ violations by a maximum is insufficient: either penalties must serialize or a single violated constraint must trigger a branch of length Θ(A).

**Necessary gadget obligations:**

1. Each admissible source choice has a rational planar realization of polynomial bit size.
2. Illegal choices or internal unmatched positions can be repaired with cost controlled by the approximation error; exact-threshold exclusions are insufficient.
3. A candidate query cannot be used prematurely to evade a purported gate.
4. Bin-window compensation and enforcement costs remain O(Bm), with no polynomially larger witness or padding baseline.
5. Every arbitrary adaptive tree maps to a source assignment whose violations are bounded by its excess cost, not merely every tree in a preferred normal form.

One should first formulate a robust normalization lemma quantitatively, e.g. source violation ≤c'(G−A)/B, and only then build the geometry. Existing boundary adjustments change both unmatched weights and adjacent pair masses; they do not provide free eligibility gates. This is a substantial new reduction, not a substitution of one source name for 3-Partition.

## 8. Candidate route C: several witnesses and consistency gadgets

Single-witness static cover is polynomial. Hardness may instead come from sharing the same supplied lines among several high-mass branches, so independently good local choices cannot be implemented consistently in one global tree.

Use a bounded-occurrence gap CSP as the combinatorial template, but require a small catalogue of explicitly realized planar gadgets. A variable gadget should have two cheap legal query orders; a constraint gadget should charge a fixed extra amount when the neighboring orders disagree with the satisfying pattern. Branch synchronization must survive arbitrary earlier queries. The expected-depth target above gives the required accounting: m local penalty masses, Θ(m) yes cost, and Ω(δm) no excess.

The strongest initial question is whether four- or six-point gadgets can enforce a useful order relation by line signs without making their intended tests informative earlier. Search small rational order types and verify candidate gadgets by exact state DP. Geometric realizability should be tested during discovery, not postponed until an abstract test-table reduction is complete. Planar line sign matrices have sign rank at most three and satisfy stronger oriented-matroid constraints; low VC dimension alone does not license arbitrary bounded-occurrence tables.

This route is more ambitious than A, but it attacks the actual adaptive coupling rather than a polynomial-time static certificate.

## 9. Priority and safe claims

1. **Ready for the manuscript:** no-FPTAS corollaries, exact fixed-direction DP, and the uniform singleton/pair formula if these structural side results fit the scope.
2. **Best focused hardness project:** classify ordered shallow halfplane cover and use the transfer lemma in §6. Its missing source hardness is explicit and geometrically faithful.
3. **Best ambitious project:** robust, several-witness consistency gadgets with constant baseline accounting. Use a gap-CSP source only after concrete gadget geometry exists.
4. **Avoid as direct shortcuts:** Set Cover under a dominant witness; nonadaptive axis-parallel separator hardness; arbitrary graph pair caps with all singleton tests; multiplying current weights/clouds to obtain a constant ratio; unqualified transfer from weighted to uniform priors.

The current work has not established APX-hardness, any fixed-factor inapproximability above one, or uniform expected-depth NP-hardness. These remain distinct questions. A QPTAS for a hard subclass would be compatible with strong NP-hardness and no FPTAS; it is not by itself an unconditional refutation of APX-hardness under P≠NP.

Primary references used for the barriers: [Har-Peled and Lee](https://jocg.org/index.php/jocg/article/download/2950/2644/7396); [Alon, Azar, Woeginger and Yadid](https://web.math.princeton.edu/~nalon/PDFS/aawy2.pdf). General MSSC hardness is background only; see [Feige, Lovász and Tetali](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf). None of those general test-system hardness claims is imported into the planar model without a realization proof.
