# Quasipolynomial simplification audit

Edited only `sections/06a-quasipolynomial.tex`. All existing labels, numerical guarantees, grade invariants, and runtime bounds are preserved. The file is released for pseudocode relocation. No PDF build was run, as requested.

## Changes

- Added a two-step roadmap: the cumulative-grade DP constructs additive-potential baseline trees; exact logarithmic-depth lookahead then removes the additive penalty.
- Stated immediately that comparison witness paths and optimum values are analysis objects, while actual child costs, interval demands, and input probabilities drive the algorithms.
- Replaced the repeated expected-depth telescoping argument with a direct application of `lem:stage-conversion` using `A = 2 lambda` and `B = 5`. The displayed constant is unchanged; its `1/ln 2` term follows already from `h(delta) <= ln 2`.
- Extracted a reusable `lem:lookahead-completion`. A maximum-depth baseline penalty bounded by `L_W` is paid by the pathwise saving `(a-1) k`. An expected-depth penalty bounded by `L_E w(S')` is paid by `(a-1) P`, using `P >= k M_k`. This explicitly preserves the mass argument required for arbitrarily small prior probabilities.
- Moved the exact lookahead recurrences ahead of the lemma, so the algorithm is specified before its comparison analysis.
- The final `thm:qp-two-plus-epsilon` now plugs in `L_W = gamma log_2 n` and `L_E = c ln n`, then explains rational caps, reachable-state counting, schedule-grade complexity, and reconstructed-tree size.
- Made the claim `gamma > 2` explicit by splitting at `delta = 1/4`. This justifies the total-block-count allowance `floor(H*/2) >= D+1`, including an appended terminal nonzero singleton.

## Preserved delicate cases

1. The graded interval DP retains all cumulative counts and last positions; independently feasible covers at different deadlines do not replace this nesting constraint.
2. The maximum-depth proof keeps `floor(floor(2 lambda (t-1))/2) = floor(lambda (t-1))` and the last exponent on a duplicate-floor plateau. Downward grade rounding still leaves an integer deadline at least the supporting-prefix index.
3. Circular forcing consumes one unit of every prefix capacity, in both objectives.
4. The comparison includes an appended nonzero terminal singleton when needed, and handles the zero singleton by the all-negative route when present.
5. Expected delay levels are rounded upward to the first integer level covering the rank delay; the surrogate is at most `lambda` times positive delay plus the unchanged zero waiting term.
6. Expected discovery information remains that of the actual vertex-answer transcript. A logical two-endpoint block does not make its union mass eligible for the single-cap entropy bound.
7. All restricted expected costs use original probabilities. The lookahead proof does not invoke the maximum-depth lower bound `log_2 |S|` or a lower bound on the smallest probability.
8. Capping lookahead at `n-1` permits every proper tree and returns the exact optimum. A lookahead state is determined by at most `k` supplied answers; baseline calls still have `O(epsilon^{-1} log n)` simultaneous grades.

## Further-development barrier

A polynomial-time `(1+eta)` optimizer for the same logical block-order delay would speed up the baseline, but would not by itself lower the lookahead factor below two. The stage ledger starts with two physical endpoint queries per logical supporting block, giving coefficient `2(1+eta)` on the restriction decrease. The lookahead lemma cancels the additive penalty and retains that coefficient; exact scheduling gives its limit two.

This is a limitation of the current proof architecture, not an inapproximability claim. A factor below two needs a new discovery ledger: for example, an amortized credit proportional to supporting-prefix delay for one-endpoint exits, or an analysis that queries an original supplied line instead of paying for both of its hull supports. Endpoint entropy credits that pay only a fixed charge per discovered class remove additive overhead but do not alter the leading restriction coefficient.

The existing grade state has quasipolynomial size because it retains `O(log n / eta)` simultaneous cumulative positions and counts. Making that state polynomial requires a compression preserving their correlations; separately optimizing each deadline is insufficient, as the three-position example in the section demonstrates.
