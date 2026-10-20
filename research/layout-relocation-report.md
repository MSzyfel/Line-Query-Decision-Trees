# Local pseudocode and procedure-flow placement

Prepared by the dedicated relocation agent. Existing analysis files were
not modified by this agent: this avoids conflicts with the parallel proof
simplification agents. The root agent can apply the changes when they finish:

```powershell
python tmp/relocate_algorithms.py --check
python tmp/relocate_algorithms.py
```

The mover checks every semantic anchor before writing any file, retains
all proof text, verifies all 18 former appendix labels, and verifies that a
second application is a no-op. It removes the `\appendix` and centralized
recipe input from the main source. The old appendix source remains as an
unreferenced historical file; the PDF includes only the local inputs.

## Recipe placements

| Procedure | Analysis file | Placement |
|---|---|---|
| Exact supplied-query Bellman recursion | `02-preliminaries.tex` | After the two objective recurrences and their interpretation |
| Alphabetic code | `02-preliminaries.tex` | After the alphabetic-code lemma and proof, before recursive accounting |
| HullData | `03-common-witness-geometry.tex` | After the hull support/pattern lemma and proof, before the geometry figure |
| EndpointCode | `03-common-witness-geometry.tex` | After the complete explanation of cuts and pinning |
| PriorityTrial | `04-maximum-depth.tex` | After the priority schedule lemma, before the recursive algorithm |
| WorstTree | `04-maximum-depth.tex` | After the recursive construction, before its approximation theorem |
| IntervalCover | `05-scheduling.tex` | After budgeted interval coverage and its proof |
| BatchOrders | `05-scheduling.tex` | After the geometric-batch lemma and its deterministic shift search |
| ExpectedTree | `06-expected-depth.tex` | After the recursive algorithm exposition, before its local accounting lemma |
| Rational orientation/adaptive block mode | `06e-adaptive-block-modes.tex` | After the rational score, mode selection, and physical-stage explanation |
| GradeDP | `06a-quasipolynomial.tex` | After the nested-deadline state invariant and feasibility example |
| Graded adjacent-block recursion | `06a-quasipolynomial.tex` | After common adjacent-block allowances, before the two objective analyses |
| Rollout | `06a-quasipolynomial.tex` | Immediately before the lookahead approximation theorem |
| SlotDP | `06d-polynomial-slot-scheduling.tex` | After the exact rank-subset lemma and proof |
| HybridTree | `06d-polynomial-slot-scheduling.tex` | After its hybrid trial construction, before the simultaneous invariants |
| Bounded-cap exact maximum depth | `06b-restricted-approximation.tex` | After its theorem statement, before the proof |
| Weighted pair-path/cycle EPTAS | `06b-restricted-approximation.tex` | After its theorem statement, before the proof |
| Transfer to on-line outcomes | `07-boundary-outcomes.tex` | After the virtual-bit explanation, before the transfer proposition |

Each standalone file in `procedures/` contains the original pseudocode
and its immediately following explanatory notes. Extraction was verified
against the whole former appendix algorithm-and-note body. The single
deliberate later update is in `procedures/hybrid-tree.tex`: its input now
uses the approved fixed global cap
`q = ceil(log_2 n), R = floor(gamma q/(gamma-1)), L = R+1`, and its note
uses the corresponding restricted threshold `OPT_W(S) <= R`.

The shared conventions from the old appendix introduction are in
`procedures/common-conventions.tex`, near the balanced/flat definitions
in the preliminaries. The obsolete recipe index is omitted; algorithms
are now encountered alongside the text that analyzes them.

The two algorithms that were already local, the improved first-phase
family in `06f-first-phase-improvement.tex` and the uniform cloud lift in
`08a-uniform-hardness.tex`, remain untouched. For the former, moving its
existing recipe from the end of the section to just before the signed
correction subsection would make it even closer to the construction.
Coordinate that change with the expected-depth agent's new improvements.

## Four procedure-flow figures

All diagrams use basic TikZ nodes, coordinates, and `-latex` arrows. No
additional TikZ library or main-preamble edit is needed.

1. `flow-recursion.tex`: near the balanced/flat definitions, before coding
   preliminaries. Shows balanced-query recursion versus hull discovery,
   endpoint recovery, and class recursion; explicitly distinguishes the
   zero-pattern cover route.
2. `flow-worst.tex`: after the hybrid construction. Shows child trees built
   once, height trials, the priority fallback, exact SlotDP, and optional
   complete-exit SlotDP. The caption states that the optimum is proof-only.
3. `flow-expected.tex`: after the first-phase schedule-family explanation,
   before signed correction formulas. Separate columns show rational
   construction-time selection and answer-dependent traversal. The
   certificate mixture is explicitly proof-only.
4. `flow-quasipolynomial.tex`: after Rollout's local pseudocode, before its
   approximation theorem. Shows comparison of supplied-query branches and
   the legal graded baseline, followed by memoization and reconstruction.

## Checks completed

- Exactly 18 standalone recipe inputs; every original algorithm label is
  preserved, with one local caller each.
- All 23 placement operations (18 recipes, four diagrams, conventions)
  pass the semantic-anchor dry run on the current analysis files.
- All four diagrams compiled in the separate same-preamble harness
  `tmp/pdfs/procedure-flow-preview.tex`; its second build has no LaTeX
  warnings, overfull boxes, or underfull boxes.
- All four rendered pages were inspected at 100 dpi. Node separation,
  arrow routing, text legibility, and construction/execution distinctions
  were checked and spacing was corrected.
- Final integration and a full manuscript rebuild remain the root agent's
  responsibility after parallel proof edits conclude.

Preview artifacts: `tmp/pdfs/procedure-flow-preview.pdf` and
`tmp/pdfs/procedure-flow-1.png` through `procedure-flow-4.png`.
