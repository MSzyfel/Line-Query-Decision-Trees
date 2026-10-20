# Polynomial general decision tree research progress

Research session dated 18–19 October 2026. Target: uniform hypotheses, unit test costs, a fixed number of outcomes per test, and polynomial runtime in the explicit input. The desired unrestricted guarantee is o(log n / log log n), ideally constant. All work in this session is recorded outside the planar article.

## Current outcome

No improved approximation guarantee for unrestricted instances has been established. The newest pass validates the user's logarithmic-depth small-menu proposal, including long partial-policy blocks, and couples it to exact deep-partition and fractional-policy optimization in polynomial time. A two-choice balance-band menu repairs a full-order greedy-gap family; merely offering the top few balanced queries provably does not. A constant-cost power-shrink partition oracle would give O(loglog n), but its unrestricted menu comparison is still unproved. Previous positive results include a recognized graph-product 2-approximation, lossless fractional-policy compilation, polynomial factor contexts and algebraic selector recovery. Details, counterexamples, and reproducible checks follow. Quasipolynomial algorithms in the older local notes are context only; they do not satisfy this session's runtime requirement.

The strongest positive transfer is a polynomial PTAS for arbitrary bounded-support tests whose interaction graph has polynomially findable strongly sublinear hereditary separators. This includes supplied bounded-treewidth decompositions. The full local test family replaces the planar interval type in the count-vector dynamic program. The exponent depends on the fixed support, separator, and accuracy parameters. An actual all-default hypothesis is unnecessary, and the proof handles any fixed response bound.

A second consequence of the reference paper is an O_K(f) polynomial approximation when each hypothesis has at most f nondefault responses relative to a supplied default string. This permits arbitrarily large supports. For fixed f,K it is constant; for f=o(log n/log log n) it improves the target order on that promised subclass. Neither structural promise is established for arbitrary instances.

## Reference and model audit

The local 1906.11385v2.pdf has been extracted and its model, Theorems 3.1 and 3.2, Proposition 3.3, greedy analysis, and prefix algorithm reviewed. Its greedy ratio is O(log n / log C_OPT), giving O(log n / log log n) for fixed arity. Its constant-factor algorithm enumerates prefixes with a superconstant depth budget and is subexponential. Reducing an exponent without making it fixed does not give a polynomial algorithm.

The classic hardness statement has an arity qualification. Chakaravarthy et al., Theorems 4.3 and 4.4, prove 4-epsilon for unrestricted outcomes and 2-epsilon for binary outcomes respectively. The former construction does not itself establish 4-epsilon for every fixed outcome bound. This qualification changes the certified lower-bound baseline, not the algorithmic target.

The current version of arXiv:2604.12036 is a logarithmic approximation paper. The initial constant-factor claim was withdrawn and is not used.

## Delegated investigations

| Direction | Auxiliary note | Intended contribution |
| --- | --- | --- |
| Continuation policies | [Continuation note](research-general-continuation.md) | Polynomial local policy improvement and adversarial tests of its limits |
| Lower potentials and credits | [Credit note](research-general-credit.md) | Triple-capacity coNP-completeness, polynomial pair replacement within 10/9 of the triple objective, and a fixed-width expressiveness gap |
| Shallow cap transfer | [Cap transfer note](research-general-caps.md) | Geometry-free separator PTAS, virtual default patterns, bounded-frequency approximation, and a bounded-overlap obstruction |
| Partition decoding | [Decoding note](research-general-decoding.md) | Exact syndrome obstruction to replacing the planar endpoint decoder by entropy alone |

## Progress record

1. Read the existing general-uniform notes before proposing new routes. They already contain extensive quasipolynomial code-pool, rank, activation, and MSSC arguments; these are not relabeled as new polynomial results.
2. Identified the planar mechanism to transfer: a legal stage is charged to restriction-cost decrease and output entropy, then these decreases telescope. Circular interval endpoint recovery supplies an essential decoder.
3. Proved the syndrome partition obstruction in research-general-decoding.md. Coordinate tests identify a uniform Boolean cube optimally in log_2 n steps. Learning one parity still needs log_2 n steps, although its output entropy and restriction decrease are each one per hypothesis.
4. Completed the cap separator transfer with an explicit local type count and exact quotient recurrence. Extended it to constructive strongly sublinear hereditary separators, fixed K responses, supplied incidence decompositions, and virtual default patterns. The continuation agent independently audited the positive proof and runtime.
5. Proved a strict insertion/pruning local optimum with an Omega(log n/log log n) gap and only O(n) supplied tests. A coding extension makes every fixed-length coordinate prefix after column activation neutral. This does not show that greedy initialization reaches that incumbent, does not exclude every mixed prefix, and does not refute fresh complete greedy rollout. The cap agent independently audited these qualifications and proofs.
6. Proved that exact all-state capacity validation for triple local-optimum resources is coNP-complete, despite polynomially many simple local values. A positive replacement maps every feasible triple potential to pairs with at least 90 percent of its root value and at least 75 percent of every deficit. Therefore the polynomial pair LP approximates the strongest width-at-most-three lower-bound objective within 10/9.
7. Extended that comparison to every fixed local width q: its best Bellman-credit lower bound is at most floor(q^2/4) times the best pair bound. On the documented affine-equality family, its gap remains Omega((log n/log log n)/q^2). This is an expressiveness obstruction even if optimization were free. It does not apply to arbitrary compact formulations with richer shared query information.

## Verification record

All four companion scripts ran successfully with Python 3.13. The finite checks are independent audits of the displayed identities and constructions, not proofs of asymptotic approximation or computational hardness.

| Script | Checked result |
| --- | --- |
| research-general-decoding.py | 227 exhaustive full-rank syndrome matrices, 96 seeded random matrices, parity examples through 256 hypotheses |
| research-general-caps.py | 558 graph-incidence cases; 271 clearing, exact count-quotient, and virtual-default cases, including 102 families without singleton tests |
| research-general-continuation.py --max-b 22 --audit-b 8 | All splitting node/test insertions checked up to 2048 hypotheses; 65,427 pairs in the largest audit; zero strict gains; 28 two-bit and 92 three-bit coordinate subsets neutral |
| research-general-credit.py | Exact local-deficit and pair-replacement identities; all state types on small cubic graphs, including 196,608 and 262,144 cases with and without a positive capacity violation |

The cap checker currently audits the binary specialization; the fixed-K extension is verified by its recurrence and proof. The continuation finite audit enumerates coordinate subsets; the written affine-space argument covers adaptive coordinate prefixes.

## Most useful next proof target

The positive separator theorem works because it can remove interactions at a small total charge and then retain every continuation choice exactly. The unrestricted problem needs an equally compact way to preserve interactions that cannot be removed cheaply.

The remaining promising target is a polynomial generator of complete, reusable conditional codes, together with a global query-synchronized comparison to OPT. It must cover the long activated-code examples without treating their individual shallow restrictions as independent costs. Fixed-tree pruning, constant-width cost resources, and output entropy alone each fail a different necessary part of that argument on explicit families above. No polynomial generator with the required worst-case coverage theorem has been proved. The continuation below turns this target into a precise weighted pricing problem.

## Deeper continuation requested by the user

The user requested further connections to information theory, coding, LPs, sophisticated greedy rules, non-greedy algorithms, lower certificates, and other subproblems, with a separate TeX writeup if an unrestricted asymptotic improvement is proved. Three agents explored new directions in parallel, and the root developed completion pricing, exact code-prefix mining, and a cooperative cost-sharing connection. No unrestricted asymptotic improvement has been established, so no new theorem manuscript in TeX has been created.

| Continuation | Auxiliary note | Main result |
| --- | --- | --- |
| Exact pricing and independent stopping | [Pricing note](research-general-pricing-next.md) | An exact completion-cover LP; weighted alpha-pricing gives an alpha UDT approximation through polynomial integer descent; exact polynomial pricing inside one supplied code |
| Non-greedy policy synthesis | [Algorithm note](research-general-algorithm-next.md) | Polynomial product-state weaving, quadratic intersection generation, and an implemented incumbent-depth prize separator |
| Synchronized LP and SDP | [LP note](research-general-lp-next.md) | A full-order gap for fixed-width local policy marginals plus PSD, Kraft, and static entropy constraints, with precise exclusions |
| Information and compact coding certificates | [Information note](research-general-information-next.md) | A causal-action relative-entropy program; its affine gap; finite-state and matroid-flat certificates for global history budgets |

### Exact LP and a sharper positive algorithmic target

A partial policy P has raw work W(P) and identifies C(P). The covering LP with one column per executable P, cost W(P), and one coverage row per hypothesis has value exactly F_OPT. The optimal leaf-depth vector is a feasible dual: execute P, append the restricted optimum on unfinished cells, and cancel costs. This keeps the adaptive computation inside the columns and has no fractional-cover integrality gap at the full ground set.

More concretely, suppose a polynomial oracle approximately minimizes W(P)/sum_{h in C(P)} w_h for integer prizes 1<=w_h<=n-1. Set w_h to the current incumbent depths. An alpha-approximate oracle gives an alpha-approximate decision-tree algorithm: whenever the incumbent exceeds alpha OPT, it finds a profitable executable partial policy. Splicing incumbent continuations strictly decreases its polynomially bounded integer raw cost. There are at most n(n-1) successful updates. All three agents independently checked the cancellation and approximation direction.

The oracle remains unsolved for unrestricted policies. Inside an explicit supplied template, however, independent stopping is exactly polynomial by tree DP or maximum closure. Uniform depth caps can be Theta(log n) worse than this exact internal pricing primitive. A supplied template library can now be tested against depth prizes by an exact executable separator, rather than by mean cost alone.

### Concrete non-greedy generator and its limit

The new prototype retains fresh greedy-deviation codes, adds quadratic intersections of their node states, and exactly optimizes represented partial policies using incumbent-depth prizes. It also supports long hypothesis-centered verification templates. The number of generated states and strict updates has a fixed-exponent polynomial bound; no lookahead parameter grows in an exponent.

The implementation repairs the old pruning plateau at n=96 and n=192, reaching the column-first benchmarks. On 500 seeded n=12 instances it improves greedy on 42 and reaches the exact optimum on 499. An explicit fixed point of cost 47 versus OPT 46 is included, so neither exactness nor an asymptotic ratio is inferred from those experiments.

### Stronger relaxations and a compact repair of their affine witness

The new LP construction shows that synchronizing all time-indexed query and pair co-location marginals on every fixed-size hypothesis subset is still insufficient, even with positive-semidefinite query matrices, Kraft, and every static subset-entropy demand. Its gap retains the full target order. This is a statement about those marginals, not complete transcript distributions. It excludes global sequential-rank or positive-answer budgets.

The causal-action entropy formulation charges the information needed to choose questions, but its explicit affine fractional channels also retain the gap. A new compact certificate repairs those witnesses: supply nonzero vectors v_h such that every oriented positive test set is a flat of their represented matroid. Gaussian elimination verifies this in polynomial time. Every positive branch then strictly decreases the rank of the actual candidate set; rank r gives a global per-hypothesis budget of r-1 positives. This does not enumerate the possible span states.

Adding this budget to the causal program yields log_2 n<=D h_2(B/D), with B<=d=r-1. When d<=log_2 n, it implies D>=(d/e)n^(1/d), correctly recovering Omega(Qd) on the affine family. The certificate's span conditions are also exactly linear index-code decoding conditions for an explicitly constructed side-information instance. Synthesis of a universally useful low-rank certificate remains open.

### A further connection to cost sharing

Let ell(C) be minimum raw work to identify the requested coalition C while still charging queries on outside hypotheses. The optimal full-tree depths form a nonnegative core allocation: their sum is ell(H), and every coalition receives total charge at most ell(C). Finding a violating coalition for an incumbent depth vector is precisely completion pricing.

This cost function is not submodular. The pricing note gives a four-hypothesis example with ell({1})=ell({1,2})=ell({1,3})=6 and ell({1,2,3})=8. Fixed-template costs are submodular coverage functions; optimizing over templates destroys that property. This rules out a tempting generic submodular-minimization shortcut while preserving exact closure pricing for explicit templates.

### New verification record

All five new checkers ran successfully, including independent cross-agent audits. The one material review correction restricted predictor potentials to target-specific reachable states, matching the actual graph verifier.

- Pricing: 240 exhaustive template-prefix cases, 720 weighted Lagrange cases, and the easy/hard cap construction through n=1024.
- Coalitions: exact adaptive DP finds the four-hypothesis submodularity counterexample.
- Code synthesis: 500 exact n=12 comparisons plus actual n=96 and n=192 adversarial constructions; explicit failure case retained.
- Local LP/SDP: all 129 local sets of width at most three on n=9 have the required common marginals; all 502 subset-entropy demands, PSD identities, and large symbolic horizon bounds pass; 79 partial-policy cover patterns check the exact dual.
- Information: 126 actual-policy projections; 53 finite-state predictor certificates; 42 represented-flat rank-drop audits; false predictor and false flat rejection; six affine channel matrices and their budget repairs.

The current concrete target is an o(log n/log log n) approximation for incumbent-depth-weighted completion pricing, or a comparably strong generation/rounding theorem for actual executable policies. That would immediately yield the requested unrestricted algorithm by the proved wrapper. The representation, pricing guarantee, and fixed-exponent runtime must all be established before a new TeX theorem manuscript is warranted.

## Third pass: pricing algorithms, actual continuation savings, and global certificates

This pass continued the unrestricted target rather than substituting a structured subclass for it. Three agents worked on adversarial policy synthesis, constructive pricing, and algorithm-linked certificates. The root developed a capacity-aware partial-coding theorem and a polynomial separation oracle for coherent tree potentials. The new results are intermediate primitives; there is still no unrestricted approximation improvement.

| Direction | New auxiliary files | Concrete progress |
| --- | --- | --- |
| Constructive weighted pricing | [Pricing oracle](research-general-pricing-oracle.md), companion Python and JSON | Exact rational pricing in the generated DAG; coalition-two verification and target-pair templates; a proved 5b comparison against policies completing at most fixed b targets |
| Adversarial and non-greedy policies | [Adversarial pricing](research-general-adversarial-pricing.md), companion Python and JSON | Explicit stronger failures; weighted templates; actual incumbent restriction credit with implicit one-query boundary macros |
| Global approximation certificates | [Certificate algorithm](research-general-certificate-algorithm.md), companion Python | Shared query budgets compose completion prices and endpoint pair prizes into the full completion-cover dual; factors 2 and 3 on specified nested activation families |
| Information/coding and unfinished resources | [Capacity pricing](research-general-capacity-pricing.md), companion Python and JSON | Every partial policy has density at least Qd/e under a saturated rank/capacity certificate; exact polynomial pricing in the abstract capacity model |
| A coherent LP direction | [Tree potential](research-general-tree-potential.md), companion Python and JSON | Exact all-subset separation for rationally weighted features of one hierarchy; a polynomial LP with arbitrarily large supports; explicit limitations recorded separately |
| Limits of combining the LPs | [Tree audit](research-general-tree-potential-audit.md) and [pair-plus-tree separation](research-general-pair-tree-separation.md), companion checkers | The weighted all-subset cone has a target-order gap on the cube, while pair charges are exact there; summing both classes makes fixed-query violation optimization NP-hard |
| Full-family code escape | [Grid validation](research-general-pricing-grid.py), results JSON | Proved raw gain r(C_R-b) from a forced column, a fresh positive code, and the actual negative incumbent restriction; ten O(n)-test grids checked through n=16384 |

### A stronger actual-credit algorithm

The former pricing certificate counted completed leaf prizes and discarded extra savings on unfinished hypotheses. The new recurrence optimizes those savings directly. At each represented state S, it can execute the incumbent pruned to S, or ask any supplied test and optimize the represented children. A child outside the represented family is an implicit terminal macro running the pruned incumbent; it is not recursively expanded. This preserves a fixed polynomial state bound.

For a policy P with output cells A, its actual credit is Gamma_T(P)=F(T)-sum_A F_T(A). Its spliced full-tree cost is exactly F(T)-Gamma_T(P)+W(P). A polynomial alpha-approximation for maximizing Gamma_T(P)/W(P) over all executable policies would give an alpha UDT approximation by the same integer-descent wrapper. That unrestricted oracle is still missing.

The new boundary primitive repairs failures even when their old generated families are frozen: raw costs 85 to 80 and 81 to 79, both reaching exact OPT. Eighty independent small-instance audits verified direct execution, actual pruning costs on every subset, and the recurrence's dominance over earlier variants. The strongest bounded searches matched exact OPT on 2,409 valid n=18 evaluations and 81 n=36 evaluations. Earlier combined depth-prize searches matched on 4,400 n=18 and 756 n=24 evaluations. These are finite observations and do not establish an asymptotic ratio.

### A constructive pricing primitive and its precise limit

For fixed coalition width b, compose greedy target verifiers while retaining shared observations, fill other exits by legal complete codes, and add the generated contexts to the polynomial state pool. The coalition-two generator repairs all four documented earlier fixed points. Its proved comparison is at most 5b against a comparator completing at most b targets. Both the restriction on the comparator and fixed b are essential.

Every root query costs n raw units. A policy completing at most b leaves with incumbent depths at most D_max cannot have positive completion-prize profit when b D_max<n. Thus the restricted coalition theorem alone cannot solve the low-depth regime. Filled continuation codes and actual restriction credit are necessary parts of the stronger candidate.

### Global certificates retain unfinished history

A positive-answer budget alone is insufficient for partial-policy pricing. Even with live unfinished leaves required to retain a positive budget, the abstract rank-two model admits density O(n^(1/3)) while its full mean is Theta(sqrt(n)). Resetting an unfinished resource silently would give a false certificate.

The root's new theorem adds remaining cardinality capacity: if n=Q^d and every reached state after j positives has size at most Q^(d-j), every partial policy finishing k hypotheses costs at least Qd k/e. The proof combines the output entropy telescope with the positive work on unfinished leaves, rather than applying the full-tree entropy bound separately. Distinct homogenized finite-field vectors and represented-flat test supports verify these assumptions compactly. A fixed-response extension is also proved, with price Qd/[e(K-1)] for Q>=K.

An exact abstract capacity pricer uses only population and remaining budget and has a fixed polynomial runtime. It is a lower-bound computation: its abstract splits are not executable supplied tests. The checker passed 136 independent completion-count cases and 2,200 entropy/resource audits; an independent agent audited the proof and code. A non-saturated counterexample is retained explicitly.

The certificate agent composes these uniform completion prices, entropy/singleton resources, and split endpoint pair prizes under one shared per-hypothesis/query budget. Adding domination of incumbent depths makes the resulting feasible solution a global approximation certificate for the actual incumbent. Explicit ledgers certify factor 2 for Boolean-core nested activation trees and factor 3 for saturated affine cores, independent of activation depth. Forty-five exact small-policy comparisons and nested-family audits passed. This does not prove a universal resource discovery or certificate-or-policy dichotomy.

### A polynomial LP with coherent large-support potentials

Assign separate nonnegative prices to the internal nodes of one explicit hierarchy, and use its weighted restriction cost as a potential. For one supplied test, a DP over selected counts of each response maximizes the Bellman deficit over all hypothesis subsets. Rational weights preserve polynomial bit complexity. This gives exact polynomial separation and hence a genuine polynomial LP, despite arbitrarily large feature supports.

It avoids the arbitrary-overlap triple separation obstruction by retaining a single hierarchy. It does not automatically produce a cheap decoder for a selected subset. Uniform scaling can already lose Omega(log n) on an entropy-optimal coordinate tree. The independent weighted-cone audit now proves a target-order gap on the plain cube: its value is O(n log log n), versus OPT=n log n. Pair charges certify that instance exactly. This is a gap for capacities on all subsets; the thin witnesses are generally unreachable, so it does not refute a reachable-state formulation. The current DP does not separate the latter formulation.

Combining the separately tractable pair and tree cones also needs care. A new, independently audited MaxCut reduction proves that finding a positive violation for one specified query is NP-hard for their sum. Disjoint triple tree features plus bipartite pair-consensus groups suffice. All 1,060,992 small subset/threshold identities pass. The theorem concerns fixed-query separation, not the complete all-query LP and not decision-tree approximation hardness.

### What is still required

The most concrete remaining proof target is a universal polynomial certificate-or-policy alternative: either the actual-credit generator finds a strict executable improvement, or a computable global dual certificate bounds the incumbent by alpha OPT for alpha=o(log n/log log n). The current proofs establish this only on specified families. No TeX breakthrough manuscript has been created because the unrestricted asymptotic improvement has not been proved; all article sources remain unchanged.

## Direct code reuse: the latest constructive direction

A further root proposal removes an unnecessary prerequisite from the earlier code library: a conditional code on C can be run directly on a larger state, without first testing membership in C. The supplied tests route outsiders through the code. A core leaf is identified only if no outsider reaches it; collisions remain unfinished or use the actual incumbent fallback. The continuation agent implemented this in [code-lifting notes](research-general-code-lifting.md) and [prototype](research-general-code-lifting.py). The certificate and credit agents developed and audited stronger pruning bounds in the [lifting audit](research-general-code-lifting-audit.md).

The basic policy finishes at least |C|-c core hypotheses, where c is the number of contaminated core leaves, at exact work F_B(C) plus the outsiders' actual routed depths. In particular work is at most F_B(C)+u height(B), for u outsiders. The generator freezes its polynomial source pool before each pass and lifts those programs onto larger states. It never recursively harvests new sources within a pass. A conservative fixed bit-operation bound for the default is O(n^16 m^3 polylog(nm)); exact exponential OPT is validation only.

Plain unweighted lifting repairs all six saved failures, reaching OPT in the first improvement pass: 47 to 46, 47 to 45, 60 to 57, 66 to 65, 85 to 80, and 81 to 79. No weighted templates, target coalitions, small tails, or actual-boundary recurrence were needed for those lifting runs. One hundred random examples independently validate legal execution, weighted prize loss, collision fallback, and exact prefix pruning. This is finite positive evidence, not a general ratio theorem.

Two stronger executable bounds avoid the potentially large height penalty:

- Stop before any code node whose outsider population is at least alpha times its core population, for 0<alpha<=1. The policy completes at least |C|-u/alpha core hypotheses at work at most (1+alpha)F_B(C). At alpha=1 a majority-core code transfers at at most twice its original raw cost.
- Use the outsider distribution p over terminal routing outputs and allocate a rational pruning budget to each occupied output. For a code balanced in core prize mass, this gives an actual prefix completing a fixed fraction of the prize at outsider work controlled by its routing entropy. For a perfectly balanced binary uniform core with at most one quarter of its leaves contaminated, at least half the core completes at work at most F_B(C)+u[H_2(p)+3]. The general weighted statement and missing-response exits for fixed arity are handled explicitly in the audit.

The audit passes 60 lifted families, 300 cut-depth profiles, 180 threshold-pruning policies, 55 weighted budget constructions, 55 entropy bounds, 22 exhaustive prefix-profit dominance comparisons, and 48 ternary late-exit cases. For a 64-hypothesis core and 4,096 outsiders concentrated at one leaf, a legal pruned lift completes 32 at work 4,320, versus 24,960 for the unpruned replay. It needs no supplied membership test for the core.

A new [rank-core construction](research-general-rank-core.md) supplies a polynomial way to synthesize some useful cores rather than enumerate them. Let r(A) be the finite-field rank of the homogenized response columns. Submodular minimization of lambda r(A)-|A|, with lambda=n/(4r), finds A satisfying |A|-lambda r(A)>=n/2 whenever some three-quarter core has rank at most r. Query rows extending the constant row to a basis give a legal code of height at most r(A)-1. Threshold lifting then has completion density at most 4r, by cancellation of |A|-n/2 against the number of surviving completions. The small validation enumerates SFM minimizers only as a check; the proposed construction uses polynomial submodular minimization and Gaussian elimination.

The rank-core checker passes 101 exhaustive identifying instances through n=4, 80 random identifying instances through n=9, 17,263 lifted core codes, and every minimizer for 387 promised rank guesses. These tests validate the constructive inequalities; the general polynomial SFM subroutine is supplied by the cited standard theorem, rather than implemented by exhaustive search in the proposed algorithm.

This is a partial-code synthesis guarantee under a majority low-rank promise. The promise is not universal: coordinate tests plus singleton tests have optimal depth log_2 n while every subset's literal response columns are independent. An initial majority-core guarantee also does not by itself establish a full-tree approximation; the general pricing comparison still needs proof. No unrestricted asymptotic result is claimed.

## Fourth pass: exact adaptive palettes, stronger profiles, and unbounded-support LP limits

This pass continues the unrestricted target. No `o(log n/log log n)` approximation for general uniform decision trees has been proved, and no breakthrough TeX manuscript has been created. New statements below are polynomial primitives, conditional guarantees, or obstructions to specified relaxations. Article sources remain unchanged.

| Direction | Auxiliary note | Established result and remaining gap |
| --- | --- | --- |
| Global adaptive reuse of a source code | [Global lifting](research-general-lifting-global.md) | Exact pricing over all actual contexts of a supplied `O(log(n+m))`-test palette; adaptive reordering can beat every prefix of a fixed source order by `Theta(log n)` |
| Global approximation accounting | [Global lifting, Sections 3–4](research-general-lifting-global.md) | A certificate-or-stage condition gives a full contraction theorem with separately telescoping actual incumbent credit and integer coding resource; universal coverage is missing |
| Synthesizing palettes without `m^{log n}` search | [Sampled palettes](research-general-sampled-palettes.md) | Exact logarithmic-size sample DP followed by exact ambient palette DP is polynomial; no coverage or approximation theorem, and saved finite failures remain |
| Weighted code synthesis despite irrelevant rows | [Selected-row cores](research-general-core-synthesis.md) | SFM and a finite ratio search optimize a capped-prize majority-surplus benchmark, with legal continuation codes and threshold lifting; no comparison to unrestricted pricing |
| Coherent nonlinear LP features | [Laminar profiles](research-general-laminar-profile.md) and [independent audit](research-general-laminar-profile-audit.md) | Arbitrary nonnegative count profiles on one hierarchy admit polynomial all-subset separation, including negative local deficits; a rationally certified eight-point gap remains even after same-hierarchy restriction features |
| Arbitrarily large overlapping LP supports | [Containment potentials](research-general-hyperedge-potential.md) | Explicit hyperedges separate by mincut; implicit nonnegative binomial profiles separate by SFM; the entire unrestricted containment cone, even plus root entropy, still has the full target-order affine gap |
| Information theory and adaptivity | [Adaptivity bridge](research-general-adaptivity-bridge.md) | Entropy greedy has mean at most `D[1+ln(log2 n)]` for minimum identifying-palette size `D`; a balanced-routing decomposition extends this promised result, with explicit failures of universality |
| Adversarial validation of the strongest generator | [Lifting adversaries](research-general-lift-adversaries.md) | Six bounded mutation campaigns, large test families, and recursive adaptive codes find no surviving fixed point; all results are finite evidence, with exact validation and dominance shortcuts distinguished |

### Exact palettes and a sufficient global theorem

A palette of `d` fixed-response tests has at most `(K+1)^d` actual contexts, regardless of its original code order. Optimizing every adaptive order and actual incumbent fallback therefore costs fixed polynomial time for `d=O(log(n+m))`. This is not enumeration of all possible palettes. The source generator must provide a polynomial list.

The executable API now supports complete-tree improvement, weighted completion-prize pricing, and mixed stage pricing. The latter maximizes `gamma Gamma_T(P)+a Delta_L(P)-W(P)`, where actual restriction credit `Gamma_T` and unrestricted integer coding resource `L` are tracked separately. If every actual state either has an `alpha` incumbent certificate or such a stage with nonnegative profit, one pass satisfies

    F_new <= gamma F_T + [a+(1-gamma)alpha] F_OPT.

Integer descent would then imply approximation `alpha+a/(1-gamma)`. This is a proved conditional wrapper, not a proof that the current generator covers every state. Independent execution checks passed 144 complete optimizations, 144 rational weighted pricings, and 144 mixed-stage identities.

The sampled-palette implementation performs exact subset DP on at most `floor(log2(n+m+1))` sampled hypotheses, giving a palette of at most one fewer tests. Both the training DP (`2^k`) and ambient context DP (`(K+1)^k`) are polynomial. Eighty small independent checks passed. On the six existing saved failures it outputs costs 47, 46, 60, 66, 82, and 82, versus optima 46, 45, 57, 65, 80, and 79. These honest failures delimit this smaller generator. The broader lifting library repairs all six. Exact reordering does improve corresponding source replay in some cases, but finite improvements do not imply a ratio.

### Weighted majority cores with actual continuations

Selected response rows create signature classes, which cannot be identified by their row basis alone. The new construction appends a legal class code and filters classes by its actual mean `L`. For incumbent depth prizes capped at `M`, define

    Z(A) = sum_(h in A) min(w_h,M) - M(n-|A|),
    g(A) = rank_R(A)+L  for A nonempty.

For each polynomially supplied row family and class threshold, SFM plus a strictly increasing rational ratio search computes `Lambda=max Z(A)/g(A)` on positive-surplus cores. Whole signature classes are retained by every minimizer. Threshold lifting gives an executable partial code with work/prize at most `2n/Lambda`. There are polynomially many distinct integer numerator/rank pairs, so the ratio search has a fixed polynomial iteration bound; exact small subset enumeration appears only in validation.

Checks passed 347 exact ratio cases and 324 positive-surplus executions. A 64-point coordinate core with singleton-test noise has all-row rank 64, yet selected rows and legal collision handling give work 332 and actual finished incumbent prize 1812. This is a constructive weighted benchmark theorem, not a universal benchmark comparison or full-tree approximation.

### Stronger profile LP and an exact expressiveness gap

The new potential is `P(S)=sum_v g_v(|S intersect H_v|)`, with arbitrary nonnegative rational profiles and zero values at zero and one. At each supplied query, a hierarchy DP retains selected response counts and maximizes the Bellman deficit. Negative local profile contributions must be retained; the root implementation uses minus infinity for unreachable counts. This yields a polynomial rational separation oracle and, by standard separation/optimization equivalence, a polynomial LP. The floating optimizer in the checker is finite validation only; exact rational scaling gives the actual lower certificate.

Root validation passed 514 exact comparisons. An independent combined-profile/restriction audit passed 299 exhaustive checks, including 342 negative local terms. Test masks `[4,10,86,92,190,212,214]` on eight hypotheses have greedy cost 26 and true optimum 25, while both profile-only and same-hierarchy combined LPs have exact optimum 24. Saved rational primal and dual certificates prove this gap. It is a fixed-hierarchy finite gap; no asymptotic lower bound for the full profile cone is established.

### A whole-cone obstruction for positive hyperedge potentials

For arbitrary containment supports, `P(S)=sum_A w_A 1[A subset S]`, query deficit is the total weight of contained supports cut by the query. It is supermodular in `S`; explicit support separation is maximum closure/mincut. Nonnegative binomial expansions on overlapping supports also admit SFM separation. Arbitrarily large supports do not repair the lower-bound quality, however.

On `H=F_Q^d`, let `n=Q^d` and supply every affine-hyperplane membership query. There are `M=Q(n-1)/(Q-1)` tests, and each pair is cut by `R=2n/Q` of them. Every support of size at least two contains a pair. Summing only root capacities therefore gives

    P(H) <= nM/R = Q^2(n-1)/[2(Q-1)] = O(nQ),

even if all possible supports are allowed simultaneously. The actual optimum is `Theta(nQd)`. Adding a nonnegative root entropy coefficient does not remove the gap: every valid combined potential has coefficient at most one and an independently valid containment component, giving value at most `n log2 n+O(nQ)`. With `d=floor(Q/ln Q)`, this remains an `Omega(log n/log log n)` gap. This is a limitation of the stated LP cone, not decision-tree inapproximability.

The independent checker passed 84 exact closure, 84 exact density, and 84 entropy-witness comparisons, plus exact affine support-count audits. The two components also give a factor `2+epsilon` optimization approximation for that combined cone; that statement does not approximate the original decision-tree objective.

Replacing root entropy by the integer unrestricted coding profile `L_2` gives exact rational factor-two component-selection and capacity-witness comparisons for that modified cone. Its affine gap is unchanged. The checker additionally passed 2,145 exact integer split inequalities and 84 exact integer-profile witness checks. These are comparisons for the lower-bound cone, not approximation ratios for decision trees.

### Information theory separates two sources of difficulty

Let `D(A)` be the minimum number of supplied tests whose full response vectors identify all hypotheses in `A`. Entropy subadditivity gives `log2|A| <= D(A) max_q H(q|A)`. Along entropy greedy, `X=log2|A|` therefore has multiplicative drift at least `X/D(H)`. The positive values of `X` are at least one, and the potential `1+ln X`, with value zero at identification, handles the last query exactly. Thus

    greedy_mean <= D(H)[1+ln(log2 n)].

The palette attaining `D(H)` need not be known or computed. This is a polynomial `O(log log n)` approximation on the promised class `D(H)=O(OPT_mean)`. A stronger actual-frontier theorem first charges a balanced greedy prefix to its single entropy telescope, then uses the weighted sum of conditional palette sizes. It does not obtain those contexts for free.

Neither promise is universal. Threshold search has identifying palette size `n-1` and optimal adaptive mean `log2 n`; its high adaptivity is fully balanced. Gated coordinate codes also make the weighted unbalanced-frontier palette budget arbitrarily large, while cheap column activation still solves the instance. The missing case is finding and charging general activation procedures while retaining reusable conditional code information.

The adaptivity checker passed 96 exact small-palette cases, 11,616 entropy/drift states, 192 actual-frontier inequalities, 120 threshold-subset checks, and 28 exceptional-state identities. A further exact construction strengthens the credit warning: a perfectly balanced supplied query can have **optimal** restriction credit exactly six while its raw output entropy is `n`. The two resources must remain separately justified even if the incumbent is replaced by an optimum.

### Bounded adversarial campaigns and a genuine adaptivity witness

The continuation agent completed six campaigns with 8,100 mutation proposals and 6,135 valid evaluations summed within runs; cross-run overlap is possible. All final outputs equal independently certified OPT. The strong-output count includes first-pass dominance certificates when plain lifting already attains OPT; it is not a count of 6,135 complete rich executions. The final n=36 representative was also explicitly rerun with the full weighted/actual-boundary procedure: greedy 214, output 196, exact optimum 196. The [adversary note](research-general-lift-adversaries.md) preserves the precise accounting, ordered query tables, and bounded validation commands.

Further suites cover 12 larger-test cases with up to 134 physical tests, 24 recursive adaptive-code cases on n=32 and n=64, and four n=128 cases. Rich independent decoys often make greedy optimal by adding genuine coding power. A saved single-source coordinate escape requires fresh greedy fallback on four exits; incumbent restriction alone would cost 392 rather than 384. The note corrects that distinction explicitly.

A proved modified camouflage family requires at least `n/4` particular queries in every static identifying palette, while an actual supplied adaptive code has depth `log2 n`. Its private sibling-pair separators establish the palette lower bound. Greedy is optimal on its two tested representatives, so this is an adaptivity witness rather than an approximation obstruction. Forty-eight independent exact-solver checks, 30 resilient-marginal checks, and 32 actual adaptive-code execution checks passed. No new nonoptimal stable example or unrestricted ratio theorem emerged from these campaigns.

## Fifth pass: a coverage theorem and sharper composition requirements

The previous pass changed the authoritative state through proofs, checked implementations, and counterexamples; it was progress rather than a waiting or status-only turn. This pass focused on the missing general comparison instead of extending the same random campaigns. Three agents explored recursive coverage, scheduling with continuation choices, and global causal resources. The root developed target-cohort and exact product-composition results. The unrestricted objective remains open and active; the following narrower theorems do not redefine success.

| Direction | New auxiliary note | Proved progress |
| --- | --- | --- |
| Growing-depth code coverage | [Recursive lifting](research-general-recursive-lifting.md), [independent audit](research-general-recursive-lifting-audit.md) | The first quadratic lifting pass supports a constant-factor tree on a serial family with a full-order greedy gap; `3/2+o(1)` on the specified growing subfamily, with no closure exponent depending on depth |
| Target cohorts and fractional covers | [Target coalitions](research-general-target-coalitions.md) | Requiring only selected targets creates an `Omega(log n)` completion-cover LP gap, despite exact full-H covering; on the same instances weighted target pricing is polynomial and nearly exact |
| Exact response-product composition | [Product decomposition](research-general-product-decomposition.md), [composition audit](research-general-composition-audit.md) | Symmetric submodular entropy cuts recover independent factors in exact polynomial arithmetic; optimal means add and feasible completion prices tensorize against every global partial policy |
| Scheduling and continuation choices | [Scheduling bridge](research-general-scheduling-bridge.md) | Fixed disjoint clearing plans have an exact Sidney scheduler, but freezing any uniform-local-optimal plans can lose `Omega(n^(1/3))`; isolated-project completion pricing can lose `Omega(sqrt n)` |
| Algorithm-linked resources | [Causal resource](research-general-causal-resource.md) | A shared pair ledger proves the near-exact target-pricer guarantee; an affine-times-threshold product disproves a root-only pair/entropy-versus-global-palette dichotomy |

### A first nontrivial growing-depth coverage theorem

Take tuple hypotheses `x=(x0,...,xL)` over decreasing even alphabets `M0>...>ML>=6`. Supply pure equality queries for every coordinate and binary codes for coordinate `k` gated on its complete lower context. With the stated fixed query priority, ordinary greedy decodes coordinates in reverse by equality, with mean `sum_k [(Mk+1)/2-1/Mk]`.

One global lifting pass supports the context-first comparison

    C=e(M0)+sum_(k>=1) ceil(log2 Mk).

The proof identifies every required source and state. An actual incumbent slice with higher coordinates fixed has a pure lower-coordinate decoder; its global lift exposes every full lower-context fiber. A forced positive-LSB source decodes all other bits first. Each global prefix cell, intersected with its context fiber, supplies an intermediate comparison state. Its final LSB children are already full context fibers. Thus every comparison node lies in the intersection of **two** generated base states, even as `L` grows. Full depth-prize optimization then gives an actual output no more expensive than the supported comparison tree.

Every positive test side has size at most `n/ML`, and this cap exceeds one. Following the common all-negative route gives `OPT_mean>=(ML+1)/2`; information independently gives `OPT_mean>=log2 n`. The exact family ratio is therefore at most

    C / max(log2 n,(ML+1)/2).

For `L=floor(M/log2 M)` and `Mk=M+2(L-k)`, ordinary greedy has ratio `Omega(log n/log log n)`, while this first pass has ratio `3/2+o(1)`. For fixed `c>=1/2`, choosing `L=floor(cM/log2 M)` gives `1+1/(2c)+o(1)` on that specified subfamily. Arbitrary context-dependent permutations of each local code also preserve the proof. These are structured-family guarantees, not a general constant approximation or a PTAS for arbitrary serial instances.

The deterministic checker uses no exact OPT oracle or full quadratic enumeration. At n=48,80,480 it executes original-test comparison and synthesized policies, and supplies explicit two-base-state witnesses for every used state. The largest case improves raw cost 6292 to 5312 using 92 required sources, 1906 base states, and a 2086-state certified reduced family. The independent audit checked source generation, retained prefix cells, priorities, all-negative lower bound, growing-depth runtime, and output comparison; its separate n=48 run passed.

This rules out independent serial selectors and local code permutations as a surviving obstruction to the present generator. Genuinely aliased activation across several contexts can destroy projection purity and remains outside the proof.

### Target-cover exactness does not survive arbitrary requested cohorts

Add `u` outsiders that answer zero to all tests on a target universe of size `N`; distinguish outsiders by singleton tests. Target caps form an arbitrary covering set system and target singleton tests are also supplied. For a required cohort `D` and `u>=2N`, its exact partial-identification cost obeys

    u*tau(D) <= ell(D) <= u*tau(D)+2N^2,

where `tau(D)` is minimum set-cover count. The lower bound counts actual outside work on the all-default spine, including attempts to eliminate all outsiders by singleton probes. The upper bound is an executable cover spine with disjoint positive decoders.

Targets equal to the `k`-subsets of `[r]`, with caps for containing index `i`, have `tau(C)=r-k+1`; weight `1/k` on each cap policy fractionally covers all targets. At `k=floor(r/2)` and `u=N^3`, the target-only completion-cover LP has an `Omega(log n)` integrality gap with `O(n)` binary tests. This does not contradict full-H LP exactness and does not prove pricing or UDT hardness.

In fact target-supported prizes admit a polynomial `(1+N^2/u)` density pricer on the same construction. For maximum cap prize `B`, assign price `w_h/B` to every target/outside pair. Charge target-cap queries at outside endpoints and outsider-singleton queries at target endpoints. Endpoint load is at most one, so every policy satisfies `W>=u*reward/B`. Asking a maximum-prize cap and decoding it costs at most `u+N^2`. This explicitly realizes the lower certificate in the existing pair ledger; it is not a newly stronger causal cone.

The root checker passed 125 independent exact cohort-cost comparisons, 125 actual cover-policy executions and sandwich checks, 119 weighted density cases, and 120 central-cover identities. The resource checker independently passed 120 exact pricing cases. The composition auditor found no proof/runtime/scope defect.

### Exact product structure is discoverable and its certificates compose

For a query-index group `R`, the function `H(A)+H(R minus A)-H(R)` is symmetric submodular. Recursively split at zero nontrivial minimum. Queyranne contractions use only entropy differences, which are compared exactly via products of empirical integer cell counts. Their bit lengths are `O(n log n)`; a loose `O(m^4)` total oracle-call bound gives fixed polynomial runtime. Independence and uniform distinct full response words imply a true Cartesian relation with uniform marginal factors.

Optimal mean costs add across the discovered factors. More strongly, if each factor has nonnegative feasible completion prices `y_i`, then `y(h)=sum_i y_i(h_i)` is feasible against every global partial policy. Fix the other coordinates, restrict the policy, and charge each physical query to its own factor exactly once. This gives a shared global certificate, not independently restarted local resources.

The implemented exact factorization passed 84 exhaustive minimizer comparisons, 5928 zero-information versus Cartesian-count checks, and 84 complete factorizations. Forty small product instances verify optimal-cost additivity, actual factor-code execution, and the greedy product identity under consistent ties; 80 exact global partial-profit checks verify tensorized prices. Running the same greedy rule after factorization reproduces its product cost, so decomposition alone is not a new greedy improvement. It supports independently selecting different algorithms and certificates on the factors. Gated dependent systems need not factor at all.

### Why an exact scheduling index is not the missing general theorem

Fixed independent block clearing plans reduce exactly to weighted completion-time scheduling on disjoint chains. The maximum-average remaining-prefix rule is polynomial and optimal. Selecting each block's own uniform-optimal plan first can nevertheless lose `Omega(n^(1/3))`: locally it prefers repeated pair exits, while global outside population makes block membership plus its decoder much cheaper. This holds for every local optimum, not merely a bad tie choice.

Even exact isolated-project completion prefixes can lose `Omega(sqrt n)` as a global pricing oracle. A query may finish none of its own project's hypotheses but activate a cheap decoder in another project on its negative response, while the positive response stops unfinished. Continuation profiles must retain these cross-project handoffs and actual outside work. The scheduling checker passed 300 exact chain comparisons, 264 all-optimal local-path transitions, and the uniform context-reversal examples. These are obstructions to stated scheduling reductions, not hardness of uniform decision trees.

The next general proof must therefore discover useful dependent response quotients or activation programs while preserving cross-context continuations. Neither independent products, scalar block optima, fractional target-cover values, nor the current root-only certificate alternatives provide that theorem. No unrestricted improvement or breakthrough TeX manuscript is claimed.

## Sixth pass: history-sensitive certificates, genuine aliases, and bundle limits

This pass continues the unrestricted objective rather than treating structured guarantees as completion. Three agents investigated true multi-context activation, the full profile LP, and sophisticated greedy/bundle rules. The root developed representation-free matroid discovery, integrated signed resource potentials into actual stage pricing, and sharpened the global contraction. Auxiliary proofs and exact checkers were written; the article remains unchanged. No unrestricted asymptotic improvement or new TeX manuscript is claimed.

| Direction | Auxiliary note | New result |
| --- | --- | --- |
| Aliased conditional codes | [Aliased routing](research-general-aliased-routing.md) | Constant final-stability guarantees with genuine multi-context activation and different local meanings, including nonlinear extensions; a polynomial root-core fractional-cover certificate |
| Full count-profile LP | [Affine profiles](research-general-affine-profiles.md) | An exact sparse dual gives the full target-order gap, even with arbitrary signed profile deficits and same-hierarchy restriction features; coordinate equality products already suffice |
| Discovering sequential structure | [Matroid discovery](research-general-matroid-discovery.md), [independent audit](research-general-matroid-history-audit.md) | Polynomial hyperplane recognition and a response-cell candidate menu recover affine rank despite singleton noise; constant-K extension has an O(Krn²) coding DP |
| Algorithm-linked history resources | [History potentials](research-general-history-potential.md) | Existing activation-ledger values receive a globally Bellman-valid signed state potential and an executable pricing interface; sharper conditional contraction toward alpha |
| Complete matroid query classes | [Matroid algorithm](research-general-matroid-algorithm.md) | Exact polynomial cardinality DP with original-query reconstruction; rank-only certificates can have a Theta(sqrt n) gap, repaired here by search capacities |
| Sophisticated greedy and stages | [Resolution greedy](research-general-resolution-greedy.md) | Every nonnegative myopic mixture of exact incumbent resolution and integer coding credit follows the bad greedy policy; full conditional-code bundles escape on that serial family |
| A genuine bundle fixed point | [Bundle obstruction](research-general-resolution-bundle-obstruction.md), [independent audit](research-general-resolution-bundle-audit.md) | A two-selector family defeats every pruning of every one-response fresh-greedy root template, even with actual incumbent fallback; the stronger lifting/intersection generator is excluded |

### Full profiles fail because they cannot distinguish graph histories

On `[Q]^d`, fix any natural coordinate-equality hierarchy and allow an arbitrary count profile at every internal node, with zero values at counts zero and one. Also allow weighted restriction-cost features from the same hierarchy. For every subset D of the first d−1 coordinates, all graph transversals `{(x,f(x)):x in D}` have identical potential, independent of the arbitrary function f. Earlier hierarchy nodes see only D; last-coordinate nodes see at most one selected point.

Choosing f to be zero on any B subset D and one elsewhere makes the supplied last-coordinate equality test simulate an arbitrary binary split of D in the potential constraints. Hence the common quotient value is at most the unrestricted binary coding cost `L_2(|D|)`. An actual last-coordinate equality spine then proves

    P(H) <= (n/Q) [Q(Q+1)/2−1] + Q L_2(n/Q).

This is an explicit exact sparse LP dual with at most `n/Q+Q−2` nonzero capacities. The argument retains negative terms and even permits signed feature coefficients. The true coordinate-only product optimum is exactly `d(n/Q)[Q(Q+1)/2−1]`; with `d=floor(Q/ln Q)`, the full cone loses `Omega(log n/log log n)`. It has only dQ physical queries. The all-affine version has the same order. This is a limitation of that fixed-hierarchy cone, not general inapproximability or a claim about arbitrary crossing hierarchies.

The checker verifies 13 exact dual identities, 2,516 coefficient cancellations, and 1,512 graph-invariance cases. No numerical LP is required.

### Certificate discovery now uses the response matrix itself

An explicit proposed hyperplane family can be checked by the finite matroid hyperplane axioms. Intersections compute closure and greedy independence computes rank in polynomial time. Require every original binary query to have a flat response. An identifying matrix then forces simplicity, and every actual proper positive branch strictly lowers rank, regardless of previous negative responses.

The discovery algorithm tries the families of all response cells of each occurring cardinality. There are at most n−1 such families, each of size at most 2m. This menu is incomplete but polynomial. On full affine-hyperplane systems plus all singleton tests it discovers rank d+1, while literal response rank is n. A nonflat decoy correctly invalidates the strong certificate. The old rank-limited recurrence and Bellman theorem are explicitly attributed to earlier notes; the new contribution is automatic recognition and discovery without a supplied representation.

For K responses, all but at most one cell of every test must be flat. Every nondefault branch then decreases rank. A min-plus convolution computes the corresponding one-default/K−1-positive coding table in O(Krn²) operations. The checker passes 21,241 binary subset rank/Bellman comparisons, plus 3,264 genuine ternary comparisons and exact binary-recurrence agreement. Exhaustive subsets are finite validation only.

A separate complete-class algorithm handles all hyperplane queries of the uniform matroid U_(k+1,n), or all its flats. Permutation symmetry reduces the exact Bellman recurrence to live population s. Desired local splits are realized by an original k-subset query padded with already eliminated points; reconstruction translates complemented descriptions and swaps actual response branches. The checker passes 56 exact DP cases, 168 supplied-description executions, and 1,008 hypothesis executions. Complete pair-query systems have true cost Theta(n²) but discovered rank-coding lower bound only Theta(n^(3/2)), disproving a rank-only comparison. The existing maximum-minority-cap pair ledger already repairs this particular example.

### Signed history potentials compose and sharpen the reduction

For a polynomially listed resource A, use its discovered conditional-rank coding value on `S intersect A`. Pack nonnegative weights in the existing per-hypothesis/per-query activation ledger. A test constant on A has zero deficit; other local deficits are at most `|S intersect A|`. This gives a polynomially evaluable, all-subset Bellman potential Phi. Its root packing LP is already Section 12 of the earlier lower-bound note; no stronger root LP is being claimed.

Unit-weight coordinate fibers in every direction fit the same ledger and give the exact coordinate-product optimum. This repairs the new profile-gap witness through history-sensitive conditional ranks. Conversely, a near-pencil has root potential 30 and a legal line child's potential 35: its signed drop is −5. Discarding negative increments would be invalid. Root-tight product potentials can also vanish on nonsingleton diagonal states, so terminal certification is substantive.

The actual palette-stage optimizer now accepts a fixed potential callback. It exactly optimizes `gamma Gamma_T+a Delta_Phi−W`, retaining actual output cells and signed drops. For one fixed reference incumbent and potential throughout a complete pass, suppose stages obey `W<=gamma Gamma_T+a Delta_Phi` and terminal codes obey `G(R)<=min(F_T(R),alpha Phi(R))`. Restriction of one global optimum to the terminal partition gives `sum_R Phi(R)<=OPT(H)`, even without superadditivity. The sharper telescope yields

    F_new <= gamma F_T + max(a,(1−gamma)alpha) OPT.

Thus `a=(1−gamma)alpha` contracts toward alpha, removing the extra factor from separately charging the two resources. Universal availability of qualifying stages or terminal certificates remains unproved. Two agents independently audited the algebra and scope. Checks include 5,392 Bellman comparisons, 36 independent signed-stage comparisons, 18 complete contraction comparisons, and the unchanged 144+144+144 palette regressions.

### Multi-context and nonlinear aliases need not defeat conditional-code generation

For any supplied root-response partition C_v, executable partial policies ask its membership query and then run fresh greedy only on its hit. At final incumbent-depth-prize stability,

    F_T <= r n + sum_v F_G(C_v).

The same statement allows arbitrary overlapping root cores and any fractional cover. Optimizing that explicit at-most-2m-core cover is a polynomial restriction of the existing completion-cover viewpoint; its value upper-bounds the final stable tree, not lower-bounds OPT.

Apply this to a base alphabet `M0=DM` followed by L uniform M-symbol rows. Every physical bit may be active on up to D different lower contexts with distinct local meanings. With arbitrary invertible affine meanings, conditional greedy after `x0=v` uses exactly `L log2 M` queries. This holds even where fixed-row slices provably lose the projection property used in the previous pass. For `L=floor(cM/log2 M)`, the final class-specific ratio is at most `1+D/c+o(1)`, while initial greedy retains its full-order gap.

The new note also handles independent nonlinear permutations: consecutive palette priority gives exact row depth for arbitrary alias graphs; separated activation and bounded incoming incidence P permit arbitrary within-factor priority and give a worst-path PL-bit bound. The latter yields ratio `P+D/c+o(1)`. The five bounded checks include genuinely nonaffine local maps at n=128 and n=1024. They verify source costs, actual partial work/prizes, projection failure, and reduced descents; they do not claim to have run the full strong generator to a fixed point.

### Exact credit does not make myopic greedy sufficient

On the previous serial family, every pure equality has exact incumbent credit `|S|`; every gated test has at most that credit. The most balanced equality also maximizes integer coding drop. Thus every nonnegative myopic mixture with positive coding coefficient repeats bad reverse-equality greedy, even with state-dependent prices. Exact resolution credit also violates adaptive diminishing returns. A complete one-response conditional-code bundle does have a profitable constant-price stage there, which explains why the larger generator escapes.

One activation step is still insufficient in general. The new family has two independent M-symbol selectors and `Theta(M/log M)` body coordinates, whose bits activate only after both selectors are known. After either outcome of any one equality, conditional greedy still decodes bodies by slow equalities. A gate's positive response identifies both selectors on only `O(1/M²)` mass. The gate's negative response admits an equality-only replay with controlled extra work.

The analytic theorem covers every pruning of all 2m such root templates. Each has `Gamma_T<=W` and `Delta_L<=O(log M/M)W`. Consequently actual incumbent fallback cannot improve the full-order bad incumbent, and a mixed stage needs `a/(1−gamma)=Omega(M/log M)`. The proof includes arbitrary nonuniform stopping depths and actual outsider work. It has an independent audit. It does not apply to template interleaving, shared palette optimization, global source lifting, or quadratic intersection synthesis.

The theorem also extends to fresh greedy on both responses of the forced root query, with independent arbitrary pruning. Its extra positive-branch credit is too small to repay the root work. The root reran the new exact checkers successfully. The bundle audit covers 856 one-response and 428 both-response small analogue templates, 372 exact gate formulas, and 1,116 gate/replay commutations, plus algebraic growing-family constants through M=1024 without constructing its enormous matrix. Some small analogues still have profitable half-credit/coding stages; these are explicitly reported and are not presented as evidence that the asymptotic obstruction already holds at those parameters.

The next comparison must therefore exploit reusable conditional codes or dependent contexts beyond a single forced-response greedy template. A fixed-lookahead extension of the two-selector obstruction is being investigated, alongside a direct positive certificate for completed selector-code replay. The audit observed that existing fresh-greedy fallback at lifted leaves already supplies that repair; the root's initial suggestion to add a second harvesting layer was unnecessary. A separate new candidate filters source queries by their global minority sizes to expose selector fibers despite multi-context aliasing. Its coverage and shared-budget proof are under investigation. The universal coverage/pricing theorem remains open. Structured positive results and lower-cone/neighborhood obstructions do not settle the user's unrestricted objective.

## Seventh pass: partial activation, polynomial contexts, and algebraic discovery

This pass developed actual polynomial policies, rather than only improved
first splits. Its strongest numerical guarantee is **2 for a recognized
structured class**, not for unrestricted decision trees. The article has
not been edited, and no new unrestricted-improvement TeX manuscript has been
created.

| Direction | Auxiliary note | Established contribution |
| --- | --- | --- |
| Charged graph activation | [Graph note](research-general-dependency-graph.md) | An n-count-state DP, compared pathwise with every original-test tree, gives factor 2 on power-of-two product alphabets |
| Automatic graph recovery | [Recognition note](research-general-graph-recognition.md) | Recovers axes, parents, palettes and actual response orientations, then executes the charged policy; every original test is checked |
| All factor contexts | [Context note](research-general-factor-contexts.md) | At most n^(log_2 3) full-value contexts, adaptive factor ordering, conditional query eligibility and actual residual fallback |
| General query-family portfolio | [Selector note](research-general-query-selectors.md) | Root-minority, whole-component partition and joint-factor independence families, with actual state-pool recombination |
| Linear cover support | [Linear selector note](research-general-linear-selectors.md) | Exact Gaussian elimination prunes cells absent from every real exact cover; recovers selectors hidden by a balanced bridge |
| Fractional policy compilation | [Template LP note](research-general-template-cover-lp.md) | A polynomial compact LP over all prunings of supplied templates; every feasible point compiles to an actual tree without cost loss |
| Alternative activation sets | [Activation compiler note](research-general-activation-certificates.md) | Complete sufficient-parent witnesses replace a single graph; sparse original-query covers give certified count-policy guarantees |
| Predicate gates | [Predicate note](research-general-predicate-activation.md) | A negative-answer-budget extension, fixed-budget synthesis, and a growing obstruction to using ordinary predicate depth |
| Fixed lookahead barrier | [Lookahead note](research-general-fixed-lookahead.md) | Every fixed forced-prefix depth with fresh-greedy exits and arbitrary pruning retains the full-order gap on a growing family |
| Camouflaged aliases | [Rotating](research-general-rotating-aliases.md), [XOR](research-general-xor-aliases.md), [bridge](research-general-bridge-aliases.md) | Successive, precisely scoped obstructions to minority filtering, information filtering and the original full portfolio |

### Charging activation improves the graph guarantee from three to two

Let H=[M]^d, M=2^b, with all coordinate equalities. Each coordinate i has
parents Pa(i); every parent tuple has a private b-question palette identifying
xi, active only on that tuple. Roots have global palettes. Context-dependent
injective bit labels, directed cycles and, for a supplied representation,
self-parent loops are permitted.

Maintain independent candidate sets with counts r_i. When all parents of i
are known, reveal its value and charge b if it was not already known. Paid
equality hits and final-candidate misses fix their coordinates without that
charge. The exact charged DP chooses which coordinate equality to ask next.
There are only product_i M=n count vectors. Rational raw costs have polynomial
bit complexity, and every activation compiles to original palette queries.

To compare with an arbitrary original decision tree T, simulate a gated query
by checking its unknown parent equalities until the first miss. Every extra
paid check after the first is preceded by a positive paid check. Each such
positive fixes a distinct coordinate, saving at least one unit of its later
activation charge. Thus, pathwise,

    paid checks + activation charges <= depth_T(h) + d b.

The simulation's stronger history entails every original answer, so no hidden
conditioning destroys its product posterior. Hence the optimal count policy
has mean at most OPT+d b, its actual tree is no more expensive, and binary
information gives d b=log_2 n<=OPT. This proves factor 2. The original
uncharged-policy factor three is explicitly superseded.

The automatic recognizer is conservative and polynomial. A minority threshold
recovers pure-coordinate response factors. Both response cells of every test
are checked for their full Cartesian-box description; all equalities, common
parent sets, every context and injective palettes must be present. Semantic
orientations are translated back into actual query indices and physical
branches. It excludes self-loop recovery and M=2, whose equalities are already
entropy optimal. No representation is supplied to this recognizer.

The independent audit also proves D+P for a test that aliases at most D full
contexts on one common parent set and an enabled union-code cost at most P b;
with supplied b-cost owner codes it gives D+1. The common-parent restriction
is essential to that particular proof. Alternative complete activation
witnesses and more general predicate evaluators are investigated separately.

The root reran all three graph checkers successfully: 1,100 charged count
values, 1,552 pathwise full simulations, 7,987 Cartesian simulation histories,
and seven bounded exact-UDT comparisons in the main checker; 2,256 independent
charged path checks; eight positive and seven negative recognition cases.
The recognizer exercises shuffled hypotheses and questions, arbitrary local
label permutations, and complemented test responses. The optimum subset DP
appears only in the seven bounded validation cases.

### All complete-value contexts fit in polynomial space

For a retained query family, factor the uniform support of DISTINCT response
words. This is deliberately separate from original-hypothesis multiplicities.
If its nonconstant factors have alphabets n_i>=2 and product N<=n, every
context fixes a factor to one value or leaves it unknown. There are

    product_i(1+n_i) <= N^(log_2 3) <= n^(log_2 3)

contexts. All original hypotheses remain present, and their actual counts
determine every decoder and fallback cost, even for dependent or unequal
quotient multiplicities.

The DP adaptively chooses the next whole factor after previous values are
observed. A query may become factor-local only after some values are excluded;
the implementation includes this conditional eligibility. Alphabets no larger
than floor(log_2(n+m+1)) use exact subset decoding, so this step is polynomial;
larger alphabets use weighted balance greedy. The benchmark is a whole-factor
block program with the stated local decoders and fresh-greedy fallback. It
does not cover arbitrary interleaving of partial factors.

On private multi-selector activation products, one threshold exposes the
axes despite arbitrary question priority and context-specific bit labels.
The planner contains selector-first decoding followed by fast body codes.
Together with the earlier joint pair/fiber coding lower bound this gives
ratio at most 1+max(2/M_min,1/log_2 r_min), independently of the number of
selectors. Forty small generic cases, 627 threshold contexts and explicit
unequal-multiplicity/conditional-eligibility examples pass execution checks.

The existing global lifting generator already has another repair here:
`finish_partial` appends the cheaper of actual incumbent restriction and fresh
greedy at every lifted leaf, retaining the chosen complete code. The selector
replay theorem uses exactly this existing behavior. An initially suggested
extra harvesting layer was unnecessary. The note and checker cover arbitrary
injective private labels and growing selector counts.

For the older serial activation family, the new direct addendum proves that
one completed lift already suffices. Its actual thin-slice source is a pure
decoder of the first coordinate; global replay exposes all its fibers, and
the existing fresh-greedy exit fallback decodes the remaining rows in order.
No quadratic intersections are needed for that family. Six direct checks,
including context-dependent code permutations, reproduce raw costs
338/672/5312 at n=48/80/480. The root reran them successfully.

### Information filtering needs algebraic support as well

The new general portfolio starts from root-minority families and checked
whole disjointness components of equally sized response cells. It also keeps
queries individually independent of every joint subset of discovered factors.
There are at most 2^d<=n such subsets, and only one frozen refinement level.
Individual independence does not imply joint independence of the retained
query tuple; the XOR example is explicitly checked. Generated actual states
are recombined by the incumbent-depth-prize DP.

Rotating aliases have the same minority as selector equalities, defeating
minority thresholds, but joint-body independence isolates the selector tests.
XOR masking makes the gates themselves independent of the full body vector,
so that information filter retains a prime identifying query family. Whole
disjointness components still isolate the selector partitions. A further
balanced bridge merges those components and leaves the full original
`selected_context_pass` portfolio at its bad incumbent. Its proof includes
conditional eligibility and state-pool recombination, not just individual
factor plans. Full runs at n=64,256,1024 confirm that particular fixed point.
This is not a fixed-point claim about the stronger global lifting generator.

The root's new LP connection repairs this bridge. For all cardinality-B cells,
form the incidence equations A x=1. Retain exactly columns that can be nonzero
in some REAL solution; rational elimination finds them. Every true partition
is preserved, because its 0/1 incidence vector solves those equations. Signed
solutions are only used for filtering, never treated as executable partitions.
Whole components are checked afterwards, and all surviving columns are also
retained as a factorization seed.

For the XOR-plus-one-bridge family at B=n/M, varying a body bit outside the
bridge forces every gate coefficient to zero: every oblique activation group
contains such a selector context. Varying inside the bridge then forces its
coefficient to zero. Only pure selector cells remain, with one constant
coefficient per axis. Their exact partitions and product factors are recovered
automatically. The resulting policy costs at most k e(M)+L(log_2 M-1).
For fixed k and L=floor(cM/log_2 M), its ratio is at most
1+k/(2c)+o(1), on a family with the full-order greedy gap.

Thirty-five affine systems and 17 exhaustive bounded partition-preservation
checks pass. All three bridge examples recover exactly the pure selectors;
candidate costs are 400,2528,12270 versus greedy 404,2546,12270. The entire
extended portfolio was run at n=64 and improves 404 to 400. The largest finite
case is explicitly a nonimprovement; the growing-family ratio has a separate
proof. Complementary noise pairs that themselves belong to actual exact
covers survive this filter, so recovery is not universal.

The particular paired-bridge continuation is nevertheless repaired. Its
entire supported family identifies a nonuniform quotient with at most one
conditional body bit in addition to all selectors. Root added an optional
sequential retained-row decoder to the factor planner, enabled by the newer
linear portfolio. It uses at most kM+2k rows pointwise, keeps the cheaper
actual local code, and has the same factor-value exits. After body completion
this gives class ratio 1+k/c+o(1), replacing an earlier O(loglog M) bound for
the greedy-only version. It does not require whole-component recovery or
uniform quotient weights. A separate n=8 fixture verifies the new fallback
actually replaces a decoy-driven greedy decoder, lowering raw work26 to24.
The original portfolio's default is unchanged; its prior scoped barrier
therefore remains a statement about the same algorithm.
The final independent audit caught that merely choosing a cheaper decoder
could drop old intermediate states needed for recombination. The implementation
now pools BOTH decoder state families. A two-factor fixture verifies old-pool
containment and actual execution, preserving the stated portfolio nonregression.

### LP mixing can be compiled directly, without rounding loss

The earlier full completion-cover LP was already proved equal to OPT. The
new addition is a constructive compiler for any EXPLICIT fractional policy
cover. Let partial original-test policies P_j complete sets C_j, have path
depths d_j(h) on every h including outsiders, and receive rational weights
x_j>=0 covering every hypothesis at least once. Fix prices
v_h=sum_j x_j d_j(h). On a remaining state S, restriction only lowers each
policy's work. Therefore some productive policy satisfies

    W(P_j restricted to S) <= sum_(h in C_j intersect S) v_h.

Execute it and recurse on its unfinished exits. The fixed price potential
pays for every query, and each application permanently completes at least
one hypothesis. At most n productive applications yield a legal full tree of
raw cost at most sum_j x_j W(P_j). Multiple unfinished exits and additional
singleton completions under restriction are handled explicitly. This is a
polynomial actual compiler, not just the old value identity or a density
oracle hypothesis.

For R full supplied templates, introduce z at every node and leaf, constrain
child z<=parent z, and require each h's leaf z-values to sum to at least one.
Minimize sum_internal |S_v|z_v. This is an O(Rn)-size LP. Thresholding a
rational solution yields at most O(Rn) weighted prefixes, with exact work
and sufficient completion coverage. The compiler above gives an actual tree
of no greater cost. A direct implementation instead obtains fixed prices
from internal z-values and optimizes a profit prefix of each restricted
template on each newly encountered state. Thus it needs no precomputed
intersection closure. The theorem works for any fixed response bound; the
current prototype is binary.

The LP's optimized value remains an UPPER benchmark for unrestricted OPT,
since its columns are supplied legal policies. No approximation comparison
to OPT follows without a template-generation theorem. The compact-point
prototype implements feasibility, layer decomposition and compilation; it
does not implement an LP optimizer. Standard polynomial LP optimization
supplies the optimization step in the algorithmic theorem. These distinctions
are explicit in the note and saved results.

Independent audit found no flaw. Thirty-six feasible compact points and 155
layer policies pass exact work/coverage checks and both independent compilers.
An illustrative pair of 256-hypothesis templates of cost 3807 combines to a
tree of cost 2112 from a point of objective 3456. The same response matrix has
an ordinary global bit code of cost 2048, so this illustrates code combination,
not an approximation improvement over matrix greedy. The full cover compiler
has separate genuinely fractional and overcoverage fixtures.

### Activation can use alternative witnesses, but enabling information matters

An activation witness W for target i must supply a factor-local height-c_i
code for EVERY assignment to W. Then eligibility depends only on which
factors are known, even if many alternative W enable the same target. The
charged count DP still has at most n states. If each original query response
is a union of at most fixed d0 terms [X_W=a][X_i in A], with W a complete
witness, simulation gives

    ALGmean <= d0 OPTmean + sum_i c_i.

Terms may use different witnesses and targets. A conservative compiler checks
all full-value contexts, constructs actual local greedy codes, tries all
product_i(M_i-1)<=n charge vectors, and discovers exact d0-term covers by
enumerating maximal contained cylinders. This is polynomial for fixed d0.
The bounded implementation compiles 75 local codes on a 64-hypothesis table,
handles alternative parent sets and complemented descriptions, rejects width
one and accepts width two, and executes every accepted policy. Its outer
factorization portfolio is described in the theorem rather than reimplemented.

The activation note's final addendum removes the fixed-width term requirement
using an equality evaluator in the verified OR-witness activation oracle.
Every terminal answer must be constant on its whole current product cell;
all free-reveal outcomes must be feasible, and each path has at most fixed
kappa negative equality answers. Known-factor values plus at most kappa
excluded values across unknown factors give a polynomial synthesis state
space. The same cancellation yields ALG<=kappa OPT+sum_i c_i for every
accepted matrix. This broader compiler is proved and precisely specified
but NOT implemented; the saved Python results remain width-one/two only.
The Cartesian, supplied-equality and low-total-charge requirements remain.

For gates with a fixed parent set, a different extension bounds the number
kappa of NEGATIVE equality answers in an evaluator whose true exits determine
all parents. Positive paid checks save later activation charges, giving
ALG<=kappa OPT+sum_i c_i. Such evaluators can be synthesized in polynomial
time for each fixed kappa by retaining known values and at most kappa excluded
values across unknown factors. For growing kappa, supplied compact evaluators
can still be used; the fixed-budget synthesis exponent may not grow.

Ordinary predicate-evaluation depth is insufficient. Two M-value coordinates
have dense palettes gated by the other's nonzero status and rare palettes
gated by zero. Each predicate needs one equality to evaluate, and an actual
code costs O(log M), yet insisting on a full known parent before activation
needs Omega(M) work. The resulting Omega(sqrt(n)/log n) abstraction gap is
proved and checked through n=4096. This is not UDT inapproximability. It shows
why certified partial information must be represented, rather than treated
as a free full-coordinate revelation.

### Constant forced lookahead cannot replace reusable codes

For every fixed r, a family with r+1 selectors and a suitably separated body
alphabet has the full-order initial greedy gap. All adaptive forced-query
prefixes of depth at most r, with fresh greedy at any or all exits, fail to
improve after any pruning and actual incumbent fallback. Their mixed integer
coding drop per work is only O_r(log M/M).

The proof controls rectangle punctures from negative gates and bounds the
small first-positive mass; it is not merely a simulation of one preferred
prefix. Fixed r permits polynomial enumeration, but r cannot grow in the
input exponent. The check covers 592 deletion inequalities, 18 bounded full
adaptive templates with exact all-pruning optimization and 21 growing-parameter
algebra checks. A small case where a coarse coefficient is inadequate is
reported, rather than mislabeled as asymptotic certification.

These barriers and repairs narrow the remaining general question: can a
polynomial generator discover enough reusable conditional codes to approximate
weighted completion pricing, including nonproduct supports and aliases that
belong to genuine competing covers? Neither the graph factor-two theorem nor
the new algebraic selector proves that comparison.

## Eighth pass: the user's branching and deeper-partition proposal

The user suggested branching among O(1), or slowly growing, choices for
O(log n) levels, and using that search to find a much deeper partition for
roughly OPT cost. Three new agents explored complementary routes, while the
root implemented the combined size/moment optimizer. The computational
framework is valid. Its unrestricted approximation comparison remains open.
All new results are auxiliary; there is no article edit or general-result
TeX manuscript.

| Component | Note | Result |
| --- | --- | --- |
| Combined executable search | [Branching and partition note](research-general-branching-partition.md) | Exact adaptive small-menu search, long macros, size targets and integer collision frontiers |
| Which greedy choices | [Bounded-menu note](research-general-bounded-menu.md) | A positive balance-band menu, a top-b balance obstruction, and pointwise policy racing |
| A stronger balance-only limit | [Cap obstruction](research-general-band-cap-obstruction.md) | All fixed-factor-near-balanced choices can retain the full gap, irrespective of branching depth |
| How much partition progress | [Multiscale note](research-general-multiscale-partition.md) | A precise O(loglog n) oracle target, exact frontier DPs, and two warnings about unsuitable progress scores |
| All adaptive policies in one LP | [Coupling note](research-general-coupled-branching.md) | Polynomial copied-flow LP over bounded-menu policy histories and lossless deep-partition compilation |
| Independent audit | [Partition audit](research-general-deep-partition-audit.md) | Verifies downward-closed target coverage, copied weights, restrictions, profits and productive restarts |

### Branching is polynomial even with full response adaptivity

With b menu queries and at most K responses, Bellman minimization adds
independently optimized response-child costs. Its history expansion has at
most sum_(j<=d)(bK)^j nodes, rather than enumerating the Cartesian product of
all complete child policies. Constant b,K and d=O(log n) are polynomial.
For growing b the safe condition is d log(bK)=O(log(n+m)), with an absolute
constant in the exponent. A state-only cache assumes a state-only menu;
history-dependent menus can retain their whole recorded history instead.

Even a menu action can be an arbitrarily long explicit partial query tree.
Its exits partition its state. The sum of populations across all virtual
occurrences at action level j is at most n b^j; therefore the occurrence
count is at most n sum_(j<=d)b^j, regardless of each action's number of
response exits. This permits long greedy blocks and structured code runs
without an n^d branching factor. A proper block has O(n) nodes. The search
can optimize every response branch separately and remain polynomial.

Primitive depth alone is insufficient: singleton queries need linear depth
even to produce a half-size maximum cell, although greedy is optimal there.
Long blocks, or a proof that a deep leftover is already cheap, are necessary
to compare a logarithmic search horizon with arbitrary OPT.

### A target that would yield an unrestricted improvement

Suppose a polynomial cut oracle always costs at most a F*(S), with raw
costs normalized consistently, and produces cells of size at most |S|^eta
for fixed eta<1. Disjoint states at one recursive level have total optimal
restriction cost at most global OPT. Since the maximum size after j levels
is n^(eta^j), this gives O(a loglog n), already an asymptotic improvement
when a is constant.

An integer collision target also suffices. For fixed 0<theta<1, require
Q=sum_exit |R|²<=|S|^(1+theta) at cost at most a F*(S). Each exit is then at
most |S|^((1+theta)/2), so the same reduction applies. The full optimal tree
is a feasible comparator, but finding a competitive partial policy is the
unproved step. A merely polylogarithmic shrink factor gives the familiar
log n/loglog n number of levels; a stronger scale is needed for this argument.

The root implements exact size-cut search and collision-frontier convolution
over the small-menu histories. Collision indices are at most n², adding a
fixed polynomial factor. Both arbitrary physical response branches and
branch-specific stopping are represented. Macro interiors are fixed for
the collision optimizer; the specified greedy fallback permits all its
stopping prefixes. Size cuts stop macros early at their accepted size cap.

### The menu must contain different kinds of decisions

The top b most balanced queries can exclude all selector equalities behind
many slightly more balanced body equalities. The bounded-menu note proves
that this retains the full approximation gap even with unlimited horizon
for b<=L/2 on its growing family. Extra search depth cannot recover a query
which never enters the menu.

A concrete two-choice alternative uses maximum minority and minimum minority
STRICTLY above half the current maximum. Ties prefer smaller original-root
minority. On the canonical private-selector family this menu contains a
selector-first program of cost O(M), versus ordinary greedy's
Theta(M²/log M), with log n=Theta(M). A depth ceil(2 log2 n) search therefore
repairs that full-order gap in polynomial time without coordinate labels.
The strict band and root tie statistic are consequential. Arbitrary extra
tests and majority-one relabelings are outside the coverage theorem.

The root proposed and the bounded-menu agent proved a sharper limitation:
adding all triple-membership tests on every body defeats even that entire
half-best-balance band. While any body is unresolved its available balance
exceeds 2/M, while selector and private-gate balance is at most 1/M. Thus
every band query remains a body test until all bodies are known. A cap-three
potential forces Omega(R) expected work per body and preserves the full
greedy gap even with unlimited lookahead. For any fixed balance factor A,
constant caps c>A give the analogous result. This constrains balance-only
menus, not arbitrary small menus or structural macro actions. Checks cover
4,237 rectangles, 158,228 allowed queries, 575 padding constructions,
2,150 exact potential identities and 413 executed policy nodes.

A later deterministic refinement chooses the smaller original-root minority
between the two offerings. It repairs that same canonical class even with
growing selector count, at mean at most k e(M)+L ceil(log2 R). Thus this is
a constructive coverage example, not evidence that branching is required
against every possible greedy rule or that the menu is universally good.

### Progress per work is not the right objective by itself

Large Shannon entropy gain plus cost O(OPT) per stage does not alone justify
a loglog n total bound. A stage can earn its information on easy hypotheses
while repeatedly leaving the hypotheses carrying OPT in a large state.
The multiscale note's counterexample makes the repeated charge explicit;
it does not disprove approximation of the minimum entropy-target policy.

For pure collision-gain/work the barrier is sharper. A node with response
counts a_i has gain/work g=sum a_i-sum a_i²/sum a_i, nondecreasing in every
count. Restricting a root query to a smaller state cannot increase g beyond
its original root value. Any adaptive partial tree's total gain/work is a
work-weighted average of these node values. It is therefore at most the best
single root query's value. Branching cannot improve that ratio. A fixed deep
target, optimized by the new frontier DP, is a different problem and avoids
this particular collapse to myopic greedy.

### Fractional deep partitions need no additional rounding loss

The exact completion LP extends to any downward-closed acceptable-state
family, including a fixed size cap. An explicit fractional cover of all h
by acceptable exits compiles to an actual acceptable partition at no cost
increase, with at most n productive applications.

Moreover the polynomial unfolded menu structure has a compact LP over ALL
adaptive bounded-menu policies and their prunings. Incoming policy weight
is split among action choices and COPIED to every response-exit child.
Acceptable-exit weights cover each h; the objective is actual macro work
times inclusion weight. A restriction-aware AND/OR profit compiler builds
the final partition without enumerating all complete policies or their full
mixture. This compiler can restart the virtual program on actual subsets,
so its output need not preserve the original d-action horizon. Its separate
n-application bound preserves polynomial runtime. The direct Bellman search
does remain in its bounded-action class, with its specified fallback.

The LP is an upper benchmark for unrestricted cut OPT. No current argument
bounds that restricted LP or the searched menu by a constant multiple of
an unrestricted power-shrink cut. This coverage comparison is the remaining
step in the user's proposed coupling.

### Verification

The root's combined driver passes 24 exact size-cut comparisons against 99
exhaustively enumerated bounded policies, 69 actual collision frontiers and
a long-macro 12-exit mass-count check. Exhaustive enumeration is validation
only. The copied-flow checker passes 29 feasible rational points, 1,442
virtual occurrences and 31 productive applications; it does not implement
an LP optimizer. Two genuinely partial policies of total weight two compile
work64 into work48 under a size-two cap.

Other independent checks include 792 template-prefix comparisons, 2,393
collision thresholds, 707 adaptive-density inequalities, 173 recursive
stages, 56 downward-closed target instances and 3,887 exact profit states.
The bounded-menu checker verifies 945 menu rectangles, 945 potential
identities, 450 pointwise racing paths and actual positive policies through
864 hypotheses. Large asymptotic instances have analytic proofs; saved
finite runs are not used to infer an unrestricted approximation guarantee.

## Runtime requirements for accepting a candidate

A proposed general algorithm must give an explicit original-test tree and a bound polynomial in both hypothesis count n and test count m. A parameter depending on log n in the exponent of n or m fails this requirement. A subset DP exponential in a fixed structural parameter can support a polynomial structured-class theorem, but cannot be reported as a general polynomial approximation.

Any claimed ratio improvement must hold for the complete recursively constructed tree. Better first splits, finite-instance improvements, or additive improvements to the old ratio do not establish the requested asymptotic result.

## Primary references

- [Li, Liang, and Mussmann, 2019 v2](https://arxiv.org/abs/1906.11385v2).
- [Chakaravarthy et al., 2011, author-hosted journal paper](https://www.cse.iitd.ac.in/~pandit/TALG_Published.pdf).
- [Szyfelbein, current v3](https://arxiv.org/abs/2604.12036v3) and [withdrawn v2](https://arxiv.org/abs/2604.12036v2).
