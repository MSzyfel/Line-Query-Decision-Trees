# Algorithm2e recipes and proof simplification

Implemented the requested pseudocode and readability pass without changing the stated approximation factors or hardness theorems. The final build for this pass has **80 pages**; the input manuscript had 74 pages. The recipes occupy nine pages, while the main text lost approximately three pages through consolidation and proof shortening.

The appendix is inserted after `sections/09-conclusion.tex` and before the bibliography. It begins with `\appendix` and `\input{sections/11-algorithm-recipes}`. The bibliography follows a `\clearpage`, so no algorithm floats enter the references. Algorithm environments use `[H]`, keeping each recipe next to its explanation.

## Inventory

| Number | Label | Coverage |
|---|---|---|
| 1 | `alg:exact-tree` | Exact supplied-query subset Bellman recursion for both objectives on bounded local states. |
| 2 | `alg:hull-data` | Strict LP witness, normalization, hull, adjacent supports, realized patterns. |
| 3 | `alg:alphabetic-code` | Explicit midpoint-dyadic pointwise code and exact expected alphabetic interval DP. |
| 4 | `alg:endpoint-code` | Cached pinning, legal opposite-edge/origin cut, conditional endpoint searches, complete-exit rectangle DP with fixed child heights. |
| 5 | `alg:interval-cover` | Exact ordinary/circular minimum hitting set and exact weighted budgeted coverage. |
| 6 | `alg:priority-trial` | Oriented first-pair enumeration, integer priority weights, and actual-height verification. |
| 7 | `alg:worst-tree` | Count-balanced/full-pattern priority recursion. |
| 8 | `alg:batch-orders` | Rational shift enumeration, exact coverage batches, greedy batch order, minimum final cover. |
| 9 | `alg:expected-tree` | Vertex, adjacent-block, orientation-aware, mixed-prefix, and adaptive polynomial expected-depth recursions. |
| 10 | `alg:block-mode` | Rational stop/query-both mode selection and optional reversed query-both orientation. |
| 11 | `alg:grade-dp` | Exact multigrade interval feasibility and minimum weighted surrogate delay, with the circular wrapper. |
| 12 | `alg:qp-baselines` | Graded adjacent-block quasipolynomial baselines for maximum and expected depth. |
| 13 | `alg:rollout` | Exact bounded-depth initial-tree optimization using a supplied legal baseline. |
| 14 | `alg:slot-dp` | Cartesian-region/rank-subset exact deadline scheduling and complete-exit variant. |
| 15 | `alg:hybrid-tree` | Fixed global logarithmic cap plus priority fallback for general polynomial maximum depth. |
| 16 | `alg:bounded-caps` | Exact polynomial maximum depth with a distinguished miss hypothesis and fixed cap bound. |
| 17 | `alg:pair-eptas` | Residue deletion, heavy enumeration, light convex optimization, conditional-expectation rounding, executable matching invoice. |
| 18 | `alg:boundary` | Two shifted virtual bits per ternary line and original-sign caching. |

Shared recipes replace duplication: the oriented and mixed-prefix expected theorems differ in their numerical threshold/certificate, and use the same schedule recipe; the complete-exit scheduler reuses the endpoint rectangle DP and rank partitions. Analysis-only witness paths and prefix-credit mixtures are explicitly excluded from algorithm inputs. The two NP-completeness reductions remain mathematical instance constructions, rather than new optimization algorithms.

## Proof simplifications

- Added `lem:stage-conversion` in `sections/06-expected-depth.tex`: one reusable balanced-query, capped-transcript, and potential-telescoping lemma. The base expected theorem and the polynomial block and adaptive-mode proofs now invoke it. Numerical logarithm enclosures and all numerical certificate inequalities remain in place.
- Shortened `lem:pruning-macro` to the actual essential argument: discovery is a function of the full pattern; endpoint pairs determine the remaining pattern; the conditional entropy chain rule pays for exactly the missing information; one or two fixed endpoints remove the corresponding code overheads. The zero singleton, early singleton inference, and double counting of doubly pinned mass are all retained.
- Shortened `thm:worst` by eliminating nested claims and repeated explanatory paragraphs. The parent/child floor inequality is retained, its five-unit count credit is labeled `eq:worst-floor-credit`, and the first/second exits, integer deadline conversion, terminal singleton block, zero route, prescribed search range, and binary information lower bound remain explicit.
- Replaced the long numbered priority-recursion description with a short invariant-oriented description and references to Algorithms 6 and 7. Replaced the duplicate expected-recursion numbered description with the shared Algorithm 9.
- Added references to recipes where the geometry, interval coverage, graded DP, capped DP, restricted algorithms, and boundary transfer are introduced. The endpoint coding lemma continues to distinguish pointwise dyadic coding from expected-cost-optimal alphabetic coding.

## Files changed

- `planar-line-decision-trees.tex`: algorithm2e setup, robust routine-name macros, appendix input, bibliography separation.
- `sections/02-preliminaries.tex`: exact local algorithm reference.
- `sections/03-common-witness-geometry.tex`: preprocessing reference.
- `sections/04-maximum-depth.tex`: recursion and proof simplification.
- `sections/05-scheduling.tex`: shared interval-oracle reference.
- `sections/06-expected-depth.tex`: simplified full-pattern proof/recursion, reusable stage conversion, shorter approximation proof.
- `sections/06a-quasipolynomial.tex`: shared graded/baseline/rollout references.
- `sections/06b-restricted-approximation.tex`: restricted algorithm and EPTAS references.
- `sections/06c-polynomial-block-improvement.tex`: shared stage-conversion proof.
- `sections/06d-polynomial-slot-scheduling.tex`: rank-subset/hybrid recipe references.
- `sections/06e-adaptive-block-modes.tex`: mode/recursion references and shared conversion proof.
- `sections/07-boundary-outcomes.tex`: transfer recipe reference.
- New `sections/11-algorithm-recipes.tex`: all 18 algorithm2e recipes.
- Rebuilt `planar-line-decision-trees.pdf` and normal LaTeX auxiliary files.

The edit helper is retained at `tmp/pseudocode_proof_edits.py`; it is a one-use transformation script, not an algorithm implementation or checker.

## Validation

- Read the PDF skill and ran its edit-operation marker successfully exactly once immediately before the first authoring edit.
- `latexmk -g -pdf -interaction=nonstopmode -halt-on-error planar-line-decision-trees.tex` passed.
- Final log has no undefined references, LaTeX warnings, overfull boxes, or underfull boxes.
- `pdftotext -layout` confirmed algorithm numbering and references; bibliography begins after Algorithm 18.
- Rendered and inspected all nine recipe pages and the conclusion/bibliography in `tmp/pdfs/pseudocode-final-overview.png`. Captions, code, notes, and page boundaries are clean. The root agent will perform the final whole-manuscript QA after integrating any further research results.

Current claims deliberately retained: general polynomial maximum depth below 4.464966, arbitrary-prior expected depth below 5.272565, and quasipolynomial (2 + epsilon) for both objectives. Research results developed concurrently are left for the root agent's separately audited integration.

## Subsequent root integration and final verification

The root integrated the independently audited research results in `sections/06f-first-phase-improvement.tex` and `sections/08a-uniform-hardness.tex`. Each has an additional algorithm2e recipe, bringing the final manuscript total to **20**. The appendix inventory references both new recipes.

The strongest general polynomial expected-depth factor is now **below 5.197569**, obtained by changing the first coverage budget and sometimes merging the first two geometric batches. Maximum depth retains **4.46496526**. Repeated expected-depth inductions use the shared stage-conversion lemma.

The cloud lift proves uniform expected-depth strong NP-completeness and no FPTAS. The explicit final hardness factors are `1+1/(3 sqrt(n))` for W, `1+9/(10 n^3)` for arbitrary-prior E, and `1+100/n^(5/3)` for uniform E, unless P = NP. These are shrinking gaps; APX hardness remains open.

The final PDF has **91 pages**. The build has no undefined references, duplicate labels, LaTeX warnings, or overfull/underfull boxes. Text extraction finds 20 algorithm captions and no unresolved reference markers. All pages were rendered for final visual inspection; changed formulas, tables and recipes were also checked at higher resolution. The final overview is `tmp/pdfs/next-final-overview.png`.

Exact numerical certificates and finite checks pass. The independent review and integration audit are in `next-results-audit.md`; the independent Bellman/rotation/geometry/scheduling checks are in `next-results-audit-check.py`.
