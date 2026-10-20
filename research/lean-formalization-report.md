# Lean formalization status

The integrated project contains actual kernel-checked proofs and remains a **partial formalization of the article**. The exposition revision and completion of previously disconnected Lean modules do not establish the remaining geometric constructions, full approximation algorithms, complexity analyses, or strong NP-completeness reductions.

Validation on 2026-10-14 passed the complete integrated build, source audit, Lean axiom audit, dependency validation, and manuscript inventory. All **400 theorem declarations** are checked; their only axiom dependencies are `propext`, `Classical.choice`, and `Quot.sound`. There are no unfinished proofs or custom axioms in the authored Lean modules.

The 170 active manuscript claims have the following coverage. The theorem-declaration count includes intermediate results and does not mean that 375 article claims are fully formalized.

| Coverage | Claims |
|---|---:|
| Full statement proved | 24 |
| Conditional transfer proved | 9 |
| Concrete component proved | 22 |
| Not formalized | 115 |

## Mathematical coverage added and integrated

The coding foundation now includes both Kraft directions, actual-tree prefix-free transcripts, log-sum, full finite entropy chain rules, support-size entropy bounds, and the expected-depth entropy lower bound. The latter has two independent routes: binary-node induction and the manuscript's Kraft/log-sum argument. Cumulative-midpoint dyadic words are implemented as actual ordered threshold trees with the pointwise and expected-depth bounds.

The executable rational interval recurrence attains the global optimum over every identifying threshold tree. Its recursive dependencies have strictly smaller interval lengths; the tabulation domain has at most `(r+1)^2` states and `r(r+1)^2` split candidates. A separate formal memoization implementation and rational bit-operation model remain unproved.

Full planar Helly is proved over ordered fields. Applying it directly over the rationals gives a strict rational common witness for every finite majority-side family. Query normalization and convex-hull cap domination are also checked. Hull adjacency, circular-pattern geometry, and polynomial witness construction remain separate obligations.

The ordinary-interval greedy solver now has soundness, completeness, optimality, empty-demand detection, a quadratic filter-work bound, and correspondence to supplied queries. Exact deadline feasibility is checked, as are identification and route height for the actual supplied-query spine. The compressed graded DP proves state merging, ordinary-interval feasibility, reconstruction of a distinct candidate schedule, and the explicit state bound `(B+1)^r(M+1)^r`.

The priority-prefix module proves the finite deadline theorem: a candidate's score sums the weights of remaining classes it hits, with base-`s+1` weights for `r` finite ranks and at most `s` classes. Every global score maximizer then maximizes every deadline-prefix score, including arbitrary ties. The construction of geometric classes and proof of the complete polynomial ordering remain open.

Three further components are now checked. `WitnessPrefix` proves that a common-answer prefix of length `n` disappears under restriction and saves `n` levels, given the shared-answer premise. `PriorityInterval` proves the interval-containment and score comparison in the extreme-choice exchange step. `AverageInvoice` proves the finite load-variance identity, the integral gap of at least two for any unbalanced load vector, and the final rational error-budget separation. Their corresponding geometric support, complete greedy-length, and histogram/invoice premises remain open and are recorded as partial claims.

The lookahead formalization now constructs and compares actual trees. An executable list scan chooses among stopping, legal leaves, and every supplied root query. Its result identifies the live state, costs no more than any competitor's completed prefix, and removes the stated continuation penalties for both objectives with arbitrary real coefficients. The continuation guarantees are the lookahead proposition's genuine premises; the optimized geometric continuation algorithms themselves remain unfinished.

The randomized foundation now proves the logarithmic multiplicative-weights potential estimate and the full depth regret bound from the actual recurrence. Exact integer weights induce the same rational normalized priors. Compact convex separation proves strong finite legal-tree-game duality, attainment, and optimal mixtures on at most `n` trees. A complete proper-tree catalog extends the dual bound to every legal identifying tree. Uniform-prior entropy proves both `log2(n) <= R` and `ln(n) < R` for each feasible finite legal mixture when `n >= 2`.

The boundary development constructs both ternary/binary simulations and proves the factor-two transfer for expected cost and maximum live depth. Positive rational margins realize the two virtual predicates with actual shifted rational lines that avoid every hypothesis.

These results supplement the previously checked restriction and properization, global optimum attainment, binary capacity, prefix/suffix invoices, arbitrary-arity potential accounting, capped-rank and floor credit, conditional approximation transfers, exact parabola query encodings, and integral square-gap proofs. The logarithmic height lower bound is now stated directly for maximum live depth, including identifying trees with unused branches.

## Scope and remaining obligations

`formalization/CLAIMS.md` and `formalization/claims.json` are the regenerated authoritative coverage inventory of all active theorem, lemma, proposition, corollary, and internal claim statements. Each record gives its current source location, checked theorem names, and any unresolved scope. `PROVED` means the full mathematical statement is checked; `PARTIAL` means a concrete component is checked; `CONDITIONAL TRANSFER` names the still-unproved construction premises; `NOT FORMALIZED` records an outstanding claim.

The outstanding work includes:

- Adjacent hull-support existence, circular positive intervals, legal endpoint cuts and comparisons, and polynomial rational common-witness construction.
- Circular and weighted interval-cover/scheduling algorithms, joint graded-delay optimization, optimized numerical logarithm certificates, and the complete polynomial/quasipolynomial approximation algorithms and bit-complexity bounds.
- Restricted cap-height optimization, the matching EPTAS's convex model and rounding, and the uniform-cap type-compression/count-vector recurrence.
- Almost-sure adaptive random-seed reduction, rational basic-solution/determinant encoding bounds, polynomial oracle-input and sparse-mixture bit complexity, and exact fair-bit sampling complexity.
- Full strong NP-completeness reductions, including matching/window identities, scale separation, boundary/internal-choice exclusions, uniform cloud identity and rotations, and reduction/certificate complexity.

No constant-factor inapproximability theorem is established by this development. No unproved paper claim is replaced by a custom axiom or treated as verified by assuming its conclusion.

## Reproducible validation

Run `./formalization/build.ps1` for the sequential integrated build, unfinished-source audit, Lean `#print axioms` audit, dependency validation, and complete manuscript inventory. The audit rejects `sorry`, `admit`, `native_decide`, custom domain axioms, `sorryAx`, and every dependency outside the ordinary foundations `propext`, `Classical.choice`, and `Quot.sound`.

Lean is pinned to `leanprover/lean4:v4.19.0`; mathlib is pinned to official `v4.19.0`, commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`. The definitive declaration list is `formalization/proved-declarations.json`; its actual dependency output is `formalization/axiom-audit.log`. Generated toolchain and dependency files are excluded from authored source.
