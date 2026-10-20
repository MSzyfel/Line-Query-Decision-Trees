# Mixed simplification and development session

13 October 2026. All results below concern supplied binary unit-cost planar line queries unless otherwise specified.

The manuscript now proves a general deterministic polynomial expected-depth factor **below 5.182976**, improving 5.197569 for arbitrary strictly positive rational priors. The maximum-depth factor remains **4.46496526**, with a smaller global slot cap and lower polynomial mask contributions. A new **uniform bounded-cap convex-position PTAS** requires an actual distinguished all-miss hypothesis but no singleton-query supply. Constant-factor inapproximability remains open. Shrinking-factor barriers and routine no-FPTAS consequences have been removed from the active manuscript and agenda; both strong NP-completeness results, including uniform expected depth, remain.

## Proof simplification without weakening guarantees

- Maximum depth now has one integer count-potential credit lemma and one local discovery/decoder/child-height ledger. The hybrid proof separates universal fallback, small-optimum comparison, and large-optimum root conversion; terminal singleton, zero route and global-cap cases are explicit.
- Expected depth uses one capped-rank credit lemma for all numerical variants. The exact capped-discovery entropy bound follows from concentration, concavity between cap multiples, and endpoint checks. An actual-versus-witness table keeps physical first hits separate from supporting-prefix credits.
- Quasipolynomial lookahead uses one lemma: pathwise frontier height for maximum depth, and mass-weighted frontier continuation cost for expected depth. It retains `(2+epsilon)` and the arbitrary-prior scope, independent of the smallest probability.

All earlier approximation guarantees, direct procedures and edge cases remain present. The numerical certificate appendix contains proof data, rather than centralized pseudocodes.

## Further algorithmic development

**Two initial budgets.** Try `q,r,k2,k3,...` for `q=1,...,6` and `r=k1-1,k1,k1+1`, subject to increasing budgets, plus `q,k2,k3,...`. Keep exact budgeted coverage and rational adaptive-mode scores. A fixed 43-row rational comparison distribution yields `B=4.374727111311243...` and ratio `5.182975508793123...`. Signed positive-rank changes, the complete negative route, first-batch savings, and early cover completion are accounted for separately. The actual shift partition explicitly includes all initial `k/beta` and `k/beta²` breakpoints through `ceil(beta³)`; this covers the terminal transition at `k1=k_min+1` even when the base partition is truncated. No logarithms or proof randomization enter tree construction.

**Smaller maximum-depth cap.** With `q=ceil(log2 n)`, use `R=floor(gamma*q/(gamma-1))`, `L=R+1`, retaining this cap in all children. For `D>R`, integrality gives the same factor from the universal bound. With `K=gamma/(gamma-1)`, the rank-mask terms become `3^L=O(n^(K log2 3))` and `2^L=O(n^K)`, with exponents below **2.666874** and **1.682611**. Other polynomial factors remain; these are not claims about the whole running-time exponent.

**Uniform convex-position cap PTAS.** Mark bounded gaps and clear them using ordinary supplied caps, with legal positive-exit identification codes. Every residual cap meets one bounded block. Uniformity makes blocks with identical local mask families interchangeable; a count-vector Bellman recurrence optimizes all adaptive interleavings exactly. For `ell>=8b²/epsilon`, prefix overhead is at most an epsilon fraction of the full optimum. Each local mask is an interval of size at most `b`, yielding at most `2^((b+1)*ell)` local states. Reconstruction retains realizing supplied lines separately for each physical block. This is a PTAS, with exponent depending on `b,epsilon`.

The PTAS rules out constant-factor NP-hardness on uniform bounded-size convex-position caps with an actual all-miss hypothesis unless P=NP. The existing GOOD/BAD coverage-profile examples remain true, but cannot supply such hardness merely by adding bounded interval interactions. Promising general hardness routes require unbounded caps, several convex layers, different witness structures, or robust global choice coupling that survives every adaptive tree.

## Layout and verification

All **22 algorithm2e recipes** sit beside their analyses. Four TikZ diagrams show the common recursive flow, maximum-depth construction, expected-depth construction versus execution, and quasipolynomial baseline/lookahead flow. The obsolete centralized pseudocode source was removed; shared pseudocode conventions remain in the preliminaries.

Verification programs and independent reports:

- [Exact two-budget certificate](expected-two-phase-check.py): all 43 rows, outward rational logarithm bounds, 9,900 phase identities and 1,650 modified-batch cases.
- [Independent two-budget audit](development-two-phase-audit.md) and [checker](development-two-phase-audit-check.py): direct floor-cell phase integration and 4,400 identities.
- [Maximum-depth simplification](simplification-worst-report.md) and [cap checker](simplification-worst-cap-check.py): exact exponent bounds and 10,000 integer boundaries.
- [Expected-depth simplification](simplification-expected-report.md): shared credit, entropy, finite-tail and zero-route audits.
- [Quasipolynomial simplification](simplification-quasipolynomial-report.md): exact lookahead proof and the current factor-two barrier.
- [Cap PTAS development](constant-gap-session.md) and [checks](constant-gap-session.py): 1,080 decompositions against full adaptive Bellman optima.
- [Independent PTAS audit](uniform-cap-ptas-audit.md) and [checks](uniform-cap-ptas-audit.py): 3,033 decompositions, including multiple blocks and families without singleton queries.
- [Active-source and shift-partition audit](tmp/mixed_source_audit.py): local algorithm count, unique labels, complete references and truncated-cover shift regression.

These finite checks supplement the proofs. Literature-wide novelty is not claimed. The final 98-page PDF compiles without LaTeX warnings, overflow or unresolved references. All pages were rendered and visually reviewed, with independent inspection of the four flow diagrams, new algorithms and certificate tables. The active source contains 187 unique labels and 135 resolved references; 4,140 refined shift cells passed the terminal-cover regression. A final clarity edit places the all-negative label on the flat discovery connector, and the certificate tables retain the larger small font.
