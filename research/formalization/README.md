# Lean 4 formalization

This is a **partial, kernel-checked formalization** with an exhaustive inventory of the active manuscript's claims. A successful build verifies the included Lean statements; it does not certify every theorem in the article. `CLAIMS.md` distinguishes complete proofs, checked components, explicit conditional transfers, and outstanding claims.

The finite model retains the supplied-query constraint. Every internal tree node contains a supplied query identifier; rational planar coordinates and lines compute its answers. Expected cost uses original rational weights. Maximum live depth ignores branches containing no live hypotheses. The randomized objective bounds each hypothesis's mean depth over a finite mixture of correct trees.

The integrated development includes:

- Executable restriction and properization, identification preservation, depth and cost nonincrease, the `|S|-1` height bound, exact maximum live depth, finite exhaustive tree catalogs, and genuine global optimum attainment.
- Both directions of Kraft's inequality for actual Boolean words; actual-tree prefix-free transcripts; finite log-sum; joint, conditional, and functional entropy chain rules; support-size entropy bounds; and the expected-depth entropy lower bound, independently proved by tree induction and by Kraft plus log-sum.
- Cumulative-midpoint alphabetic codes implemented as actual ordered threshold-query trees, including their pointwise and expected-depth bounds. The rational interval recurrence attains the global optimum over all identifying threshold trees, with a valid increasing-length dependency order, at most `(r+1)^2` interval states, and at most `r(r+1)^2` split candidates.
- Full finite planar Helly over ordered fields, an actual strict rational common witness for the full majority-side family, normalized query semantics, convex-hull cap domination, conditional two-support implications, and conditional zero-pattern uniqueness.
- The executable ordinary-interval greedy cover's feasibility and optimality, empty-demand rejection, supplied-candidate correspondence, and quadratic filter-work bound.
- The batch-phase residual comparison: maximum covered mass and inclusion of the budget-optimal set's hits imply no larger residual than a feasible comparison prefix. The geometric floor-sum bound on all pre-final phase lengths is also proved. The interval DP's optimality theorem and the construction-specific links to these premises remain open.
- The extremal interval-cover exchange step: moving to an available extreme point contains the comparison intervals and cannot lower their remaining hit weight. The full greedy-length induction and circular reduction remain separate.
- Exact finite deadline feasibility, an actual supplied-query spine's identification and route-height certificate, and the compressed graded DP's state merging, feasibility, reconstruction, and product state-count bound.
- A common-answer prefix of length `n` contracts under tree restriction and saves `n` levels. The planar support argument establishing that common-answer premise remains open.
- The finite deadline-priority theorem: candidate scores sum the weights of remaining hit classes, and every global score maximizer maximizes every deadline prefix, including arbitrary ties. The geometric construction of the class/query incidence and the complete polynomial scheduler remain open.
- Executable finite exact-cost rollout for expected cost and height. The selector compares stopping, legal leaves, and every supplied root query. It inherits the full lookahead penalty-removal theorem for arbitrary real coefficients from actual prefix/frontier accounting.
- Arbitrary-arity recursive invoice accounting, actual-tree potential cancellation, capped-rank and floor arithmetic, and balanced-query entropy charging on actual partial stages and identifying trees.
- Finite legal-tree-game strong duality, optimum attainment, and optimal support of at most `n` trees, including a complete finite proper-tree catalog that extends the dual bound to every identifying tree.
- The actual multiplicative-weights logarithmic potential proof and depth regret bound, exact integer-to-rational-prior correspondence, and uniform-prior logarithmic lower bounds for actual finite legal mixtures.
- Executable ternary/two-bit conversions, identification preservation, both factor-two objective transfers, and actual rational shifted-line realizations of the virtual predicates.
- Exact integer-parabola interval/private-query encodings, strict signs and off-line conditions, tangent exposure, and the expected-depth reduction's load-variance identity, integral square gap, final error-budget separation, scalar internal-penalty transfer, and pair-perturbation estimate. The triangular rank-sum and aggregate $E_+$ bounds are checked under explicit pointwise correction premises; deriving those premises from the geometric construction remains open.
- On the alternating odd path, every matching has at most `t` edges; if it has `t`, every two-edge block is occupied. An odd-edge choice propagates through the suffix, so the even choices form a prefix and the odd choices form a suffix; every maximum matching leaves exactly one even vertex uncovered.

The main remaining obligations are geometric hull adjacency and circular patterns, legal endpoint geometry, circular/weighted interval scheduling and optimized certificates, the complete approximation algorithms and their complexity, restricted cap/matching algorithms, and the full strong NP-completeness reductions. Polynomial rational LP encoding, random-seed measure reduction, and exact fair-bit sampling complexity also remain. No unproved domain statement is introduced as an axiom or counted as a full proof merely by assuming its conclusion.

## Reproducible build

Lean is pinned to `leanprover/lean4:v4.19.0`; mathlib is pinned to the compatible official `v4.19.0` tag, commit `c44e0c8ee63ca166450922a373c7409c5d26b00b`.

From the workspace root, run:

```powershell
.\formalization\build.ps1
```

The script builds the integrated targets sequentially, rejects unfinished proof syntax and custom axioms, runs Lean's `#print axioms` on every inventoried theorem declaration, validates the dependencies, and regenerates manuscript claim coverage. Only the ordinary foundations `propext`, `Classical.choice`, and `Quot.sound` are permitted. `proved-declarations.json` and `axiom-audit.log` record the checked declarations and their actual dependencies.

The 2026-10-14 build checked **454 theorem declarations**. The regenerated inventory contains 170 active manuscript claims: 24 fully proved, 9 conditional transfers, 32 partial proofs, and 105 not formalized. The audit includes the odd-path cutoff characterization, the within-batch first-cover inequality under explicit monotonicity and hit-mass premises, the phase residual comparison and geometric schedule-length bound under stated premises, the 3-Partition bounds showing that every bin has three items, the expected-depth internal-penalty transfer, the aggregate pair-perturbation estimate, the floor-correction bound for the construction, and the quadratic threshold's $O(n^4)$ arithmetic bound. This update also formalizes the expected-depth endpoint-mode costs, the calibrated entropy tent and its payment by binary information loss, the exact single-merge identity for finite transcript fibers, local stage accounting under an explicit aggregate merge premise, and the interior-cut size-plus-run charge in the greedy-cover argument. The batch results leave the greedy schedule's premise derivation and budgeted interval dynamic program in the article proof. The expected-depth coarsening result still leaves the multi-block transcript map and endpoint-cap geometry open. The floor-correction theorem assumes the stated item-size, bin-level, denominator, and calibration bounds; deriving all of those from the geometric source instance remains open. The checked declarations use only standard classical foundations, with no unfinished proofs or custom axioms. One non-fatal style-linter warning remains in `PlanarQuery/CodingDyadic.lean:52` about an unnecessary sequential-focus combinator. Intermediate checked theorems do not count as complete proofs of the remaining article claims.

To reconstruct elsewhere, install the pinned toolchain, clone the mathlib tag into `formalization/mathlib-git`, run `lake update`, and fetch the official mathlib cache with `lake exe cache get`. For a workspace-local compressed cache, set `MATHLIB_CACHE_DIR` inside the project. The compiler and downloaded dependencies are generated files excluded by `.gitignore`; authored proofs are under `PlanarQuery/` and imported by `PlanarQuery.lean`.

After manuscript edits, regenerate the inventory with:

```powershell
python formalization/inventory.py
```

Run `audit.py` first if theorem declarations changed. The inventory checks that every cited Lean theorem exists in the source audit and tracks internal claims by stable title when their line numbers or labels change.
