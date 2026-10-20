"""Inventory every active formal claim, with honest Lean coverage.

Run after any manuscript restructuring: python formalization/inventory.py.
Unlisted claims default to NOT FORMALIZED; nothing is silently certified.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "formalization"
CLAIM = re.compile(r"\\begin\{(theorem|lemma|proposition|corollary|claim)\}(?:\[([^\]]*)\])?")
INPUT = re.compile(r"\\input\{([^}]+)\}")

# Coverage records state the *actual scope*, rather than counting a theorem
# that assumes the entire paper statement as a verification of that statement.
COVERAGE = {
    "lem:restriction": ("PARTIAL", "Tree.disjoint_expected_optima_le; Tree.subset_live_height_optimum_le; Tree.identification_log_height; Tree.global_expected_minimum; Tree.global_live_height_minimum", "The exact restriction inequalities, logarithmic height lower bound, and genuine global optimum attainment are proved in the executable supplied-query model. The expected-cost entropy lower bound is not proved."),
    "clm:restriction-1": ("PROVED", "Tree.disjoint_expected_optima_le; Tree.subset_live_height_optimum_le; Tree.global_expected_minimum; Tree.global_live_height_minimum", "Complete disjoint expected-optimum and subset maximum-live-depth optimum inequalities. Genuine global minima are attained. Restriction preserves actual supplied-query semantics and original weights; irrelevant branches do not affect the maximum live depth."),
    "clm:restriction-3": ("PROVED", "Tree.leafCount_le_pow_height; Tree.identification_capacity; Tree.identification_log_liveHeight", "Actual binary leaf-occurrence capacity, including repeated labels, and the logarithmic lower bound on every identifying tree's maximum live depth are proved."),
    "prop:potential-cancellation": ("PROVED", "StageLedger.local_to_global", "Complete arbitrary-arity recursive invoice combination, with zero terminal potentials. The local stage invoices are exactly the proposition's premises, not claimed algorithmic results."),
    "lem:worst-floor-credit": ("PARTIAL", "floor_difference; flat_count_credit; balanced_count_credit", "The floor and coefficient inequalities are proved over real logarithmic coordinates. The geometric child-size-to-logarithm premises are not connected."),
    "lem:capped-rank-credit": ("PROVED", "capped_rank_credit", "All nonzero and zero-mass algebra is proved for a finite rank family; deficits outside the exceptional set vanish. The formulation sums all finite ranks instead of spelling out the exceptional set."),
    "lem:stage-conversion": ("CONDITIONAL TRANSFER", "flat_stage_absorption; StageLedger.local_to_global; Tree.executable_potential_telescope; entropy_to_ratio", "Absorption, arbitrary-arity invoice combination, and actual-tree potential cancellation are proved. Binary entropy bounds, balanced-query invoices, and extraction of the algorithm's stage ledger remain obligations."),
    "lem:lookahead-completion": ("CONDITIONAL TRANSFER", "lookahead_height; lookahead_expected; exact_choice_inherits; Tree.prefix_pays_frontier; Tree.prefix_suffix_decomposition", "Height and expected-mass cancellation plus the actual-tree weighted prefix payment are proved. Constructing and exhaustively evaluating all legal truncated trees/frontier continuations is not formalized."),
    "thm:poly-slot-worst": ("CONDITIONAL TRANSFER", "slot_cap_fallback", "The cap fallback inequality is proved with explicit depth/logarithm premises. The full slot scheduler, physical route bounds, and running time are unproved."),
    "prop:uniform-cap-charge": ("CONDITIONAL TRANSFER", "capped_spine_lower_bound; shallow_cap_ratio", "The final overhead-to-optimum ratio calculation is checked. Deriving the rank lower bound, residual optimum comparison, and actual clearing overhead remains unproved."),
    "thm:uniform-cap-ptas": ("CONDITIONAL TRANSFER", "shallow_cap_ratio", "The final ratio combination is proved with every overhead, optimum, and scale premise explicit. Geometric gap isolation, count-vector Bellman correctness, and complexity remain obligations."),
    "thm:uniform-cloud-transfer": ("CONDITIONAL TRANSFER", "uniform_cloud_threshold; exact_additive_threshold; additive_lift_preserves_ratio", "Threshold and approximation transfer arithmetic is proved assuming the cloud cost identity. The equality itself, rotations, and geometry remain obligations."),
    "lem:helly": ("PARTIAL", "three_small_sets_omit; PlanarInstance.small_majority_family_intersects; PlanarInstance.strict_query_semantics", "Every subfamily of at most three majority half-planes has an actual strict rational planar witness. Planar Helly for the full family and polynomial rational LP construction are not yet proved."),
    "lem:hull-structure": ("CONDITIONAL TRANSFER", "rationalDot_supportCombination; two_support_dot_le; two_support_cap_implication", "The exact rational two-support cap implication is proved given a nonnegative subconvex representation. Existence/adjacency of hull supports, circular intervals, and singleton zero classes remain unproved."),
    "prop:batch-derandomization": ("PARTIAL", "minimum_below_mixture", "Selecting a finite minimum costs no more than any probability mixture. Enumerating all shift representatives, equivalence to the continuous shift average, and polynomial time are not formalized."),
    "clm:batch-first-cover": ("PARTIAL", "BatchFirstCover.weighted_rank_le_average; BatchFirstCover.first_cover_bound", "The half-batch rank inequality and its first-cover invoice consequence are proved for a nonincreasing gain sequence, assuming the explicit hit-mass identity. Deriving these premises from the greedy interval schedule remains in the article proof and is not formalized."),
    "clm:batch-phase-cover": ("PARTIAL", "BatchPhaseCoverage.totalMass_eq_covered_add_uncovered; BatchPhaseCoverage.maximum_coverage_residual_le; BatchPhaseCoverage.phase_residual_le_comparison; BatchPhaseLength.schedule_length_geometric_bound", "The finite weighted residual-mass comparison is proved from maximum budgeted coverage and phase hit inclusion, with nonnegative weights stated explicitly. The geometric floor-sum schedule-length bound is also proved under the earlier-phase threshold premise. The interval DP's maximum-coverage property and its link to the constructed phases remain unformalized."),
    "clm:expected-mode-costs": ("PARTIAL", "ExpectedModeCosts.stop_first_positive_allowance; ExpectedModeCosts.stop_second_positive_allowance; ExpectedModeCosts.both_exclusive_allowance; ExpectedModeCosts.both_shared_allowance; ExpectedModeCosts.stop_weighted_saving; ExpectedModeCosts.both_weighted_saving", "All four query-count bounds in the endpoint-mode table and both weighted savings identities are proved from the displayed prefix-count premise. Deriving that premise from the geometric block schedule and formalizing legal endpoint-code construction remain outside Lean."),
    "clm:expected-coarsening": ("PARTIAL", "ExpectedCoarsening.calibrated_binary_entropy_tent; ExpectedCoarsening.coarseningPenalty_le_binaryInformation; ExpectedCoarsening.endpoint_credit_paid; ExpectedModeChoiceAlgebra.estar_mono_left; ExpectedModeChoiceAlgebra.both_mode_saving_le_D; ExpectedModeChoiceAlgebra.stop_saving_le_D; ExpectedCoarseningAccounting.block_score_paid; ExpectedCoarseningAccounting.stage_information_saving_bound; ExpectedTranscriptCoarsening.finite_label_merge_entropy_loss; ExpectedTranscriptCoarsening.transcript_fiber_merge_information_loss", "The calibrated tent pays for the named endpoint credit; the finite-label single-merge information identity, local mode algebra, and stage accounting are proved under explicit premises. The multi-block transcript map, endpoint-cap containment, and derivation of the aggregate merge-loss premise from the actual decision tree remain open."),
    "prop:randomized-duality": ("PARTIAL", "randomized_tree_weak_duality; Tree.restricted_height_le_card_pred; Tree.global_expected_minimum", "The actual finite tree game has weak duality, and properization and global expected minima are proved. Strong LP duality, random-seed reduction, and the expected entropy lower bound remain unproved."),
    "prop:randomized-compression": ("PARTIAL", "integer_weights_positive; integer_weights_size_bound; normalized_integer_prior_positive; normalized_integer_prior_sum; Tree.restricted_height_le_card_pred", "Integer MWU updates, exact positive rational normalized priors, their exponential magnitude bound, and the n-1 proper-tree height bound are checked. Polynomial bit-length, sparse LP support, optimality, and exact sampling complexity remain unproved."),
    "thm:randomized-transfer": ("CONDITIONAL TRANSFER", "randomized_transfer_arithmetic; randomized_calibration; integer_weights_positive; normalized_integer_prior_sum", "The strict final approximation and parameter calibration follow from explicit regret, hardest-prior, entropy, and oracle premises. Those premises, oracle-call complexity, LP support <= n, and sampling are not claimed verified."),
    "prop:height-encoding": ("PARTIAL", "interval_encoding_negative_iff; interval_encoding_nonzero; private_encoding_negative_iff; private_encoding_nonzero; interval_encoding_offLine; private_encoding_offLine; tangent_encoding_exposes", "The actual integer-parabola interval/private supplied lines, strict signs, off-line conditions, and tangent exposure are checked. Full reduction construction, numerical size bounds, and polynomial certificate verification are not formalized."),
    "thm:strong-worst": ("PARTIAL", "ThreePartitionBounds.length_eq_three_of_sum_eq", "The source-instance arithmetic is proved: if each item lies strictly between one quarter and one half of B, then every bin of total weight B contains exactly three items, with repeated item weights retained. The decision-tree normalization, histogram-to-load equivalence, geometric realization, and strong NP-hardness reduction remain unformalized."),
    "prop:average-internal-encoding": ("PARTIAL", "interval_encoding_negative_iff; private_encoding_negative_iff; interval_encoding_offLine; private_encoding_offLine; three_partition_square_decomposition; three_partition_quadratic_coefficient_le; three_partition_quadratic_threshold_le_fourth", "Exact interval and private-query geometry is checked, as are the source-total square decomposition and the parameterized O(n^4) threshold-term bound. The scalar internal-choice penalty transfer is proved under explicit invoice, rank, error, and scale premises; deriving the full set of numerical premises from the geometric reduction remains open."),
    "prop:average-normalization": ("PARTIAL", "expected_depth_scale_div; expected_depth_scale_dominates_bins; expected_depth_eminus_lt_scale_div; expected_depth_Eplus_le_of_pointwise; expected_depth_Eplus_lt_scale; average_boundary_floor_correction_le; average_boundary_Eplus_lt_scale", "The calibrated scale identity, its dominance over the bin count, and E_- bound are derived from the chosen integers. The floor formula now yields the pointwise correction bound and aggregate E_+ scale estimate under the displayed item-size, bin-level, denominator, and calibration bounds. Proving the remaining pair/unmatched weight separations from the source construction remains open."),
    "clm:average-linear-cancellation": ("PARTIAL", "nat_floor_multiple_error_eq_neg_remainder; nat_floor_multiple_error_bounds; sum_nat_floor_multiple_error_bounds", "The quotient remainder identity and the resulting individual and finite-sum rounding bounds are proved for natural numerators and positive denominators. Connecting the floor quotients to the constructed bin corrections and proving their exact cancellation remain open."),
    "clm:average-imbalance-gap": ("PARTIAL", "integer_zero_sum_gap; load_deviations_sum_zero; load_deviation_square_identity; unbalanced_load_square_gap; zero_load_deviation_iff_balanced; load_gap_exceeds_error_budget; unbalanced_invoice_exceeds_threshold; balanced_invoice_within_threshold; expected_depth_eminus_lt_scale_div", "The finite load identity, zero-deviation characterization, integral gap, error-budget comparison, and chosen-scale E_- bound are kernel-checked. The geometric histogram/invoice transfer and E_+ scale estimate remain open."),
    "clm:average-pair-perturbation": ("PARTIAL", "average_pair_perturbation_bound; expected_depth_Eplus_le_of_pointwise; expected_depth_Eplus_lt_scale; average_boundary_floor_correction_le; average_boundary_Eplus_lt_scale", "For arbitrary real pair-mass vectors, the minimum weighted ordering cost is monotone under coordinatewise nonnegative perturbations and increases by at most q times their total mass. The floor formula yields the pointwise E_+ correction and calibrated aggregate bound under explicit construction inequalities. Transferring boundary corrections to pair-mass perturbations using matching incidence remains open."),
    "clm:height-prefix-constant": ("PARTIAL", "Tree.restrict_common_root; Tree.height_restrict_common_root; Tree.height_restrict_commonPrefix", "A common-answer prefix of length n is shown to disappear under restriction and save n levels. Deriving that premise from planar support geometry remains open."),
    "lem:height-prefix": ("PARTIAL", "Tree.restrict_common_root; Tree.height_restrict_common_root; Tree.height_restrict_commonPrefix", "Restriction saves one level for each explicitly supplied common answer in the prefix. The geometric first-support argument and the full optimum-transfer statement remain open."),
    "lem:greedy-cover-length": ("PARTIAL", "PriorityInterval.extreme_hit_subset; PriorityInterval.extreme_hitWeight_le; PriorityInterval.extreme_maximizer_score_eq; GreedyRunAccounting.split_run_count_bound; GreedyRunAccounting.split_size_run_charge", "The extremal interval-containment and score comparison are formalized, and an interior cut is proved to preserve the combined candidate-size and run-count charge. The full greedy-length induction, its run decomposition in the actual schedule, circular case, and bit-complexity remain outside Lean."),
    "prop:uniform-threshold-certificate": ("CONDITIONAL TRANSFER", "uniform_cloud_threshold; exact_additive_threshold", "Scalar threshold equivalence is checked assuming the exact cloud equality. Polynomial encoding and NP certificate verification remain unproved."),
}

COVERAGE.update({
    "lem:odd-path": ("PARTIAL", "OddPathMatching.choiceSize_le; OddPathMatching.choiceSize_eq_of_full; OddPathMatching.matching_card_le; OddPathMatching.matching_card_eq_forces_block_occupancy; OddPathMatching.matching_odd_choice_propagates; OddPathMatching.matching_odd_choice_propagates_to; OddPathMatching.matching_has_even_to_odd_cutoff; OddPathMatching.matching_maximum_leaves_unique_even_vertex", "The block-count bound is proved, equality forces every two-edge block to contain a selected edge, and an odd-edge choice propagates through the suffix. Thus every maximum matching has a prefix of even choices followed by a suffix of odd choices, and leaves exactly one even endpoint uncovered."),
    "clm:average-internal-penalty": ("PARTIAL", "average_internal_penalty; fin_rank_sum; pair_completion_cost_le_triangular_bound", "The scalar threshold transfer and finite rank-sum bound are proved under explicit invoice, internal-coordinate, rank, reference-mass, error, and scale premises. Deriving those premises from the geometric reduction remains open."),
})

# Anonymous claims are matched by their stable titles, so prose insertions
# do not accidentally attach a proof to the wrong source line.
TITLE_COVERAGE = {
    "Three majority half-planes have a common strict point": ("PROVED", "PlanarInstance.small_majority_family_intersects; PlanarInstance.strict_query_semantics", "Every subfamily of at most three supplied majority half-planes has a common strict rational point, with minority mass and off-line premises explicit. The empty family and smaller subfamilies are included."),
    "Negative support answers force the original answer": ("CONDITIONAL TRANSFER", "two_support_dot_le; two_support_cap_implication", "Complete rational dot-product/cap implication, given the displayed subconvex support representation. The representation's geometric existence and adjacency remain unproved."),
    "Expected prefix cost pays for every surviving frontier mass": ("PROVED", "Tree.prefix_pays_frontier", "The actual tree prefix pays k times the mass of all hypotheses with depth at least k, a stronger bound than restricting the mass to hypotheses still needing continuation."),
    "Restriction and information telescope over pattern classes": ("PROVED", "StageLedger.local_to_global; Tree.executable_potential_telescope", "Complete recursive combination of local invoices with zero singleton potentials, for arbitrary finite branching. This claim combines invoices; it does not establish them."),
    "Each stage is paid for by two potential decreases": ("CONDITIONAL TRANSFER", "flat_stage_absorption", "The flat-stage algebra is proved given its information and coefficient bounds. Balanced-query entropy charging and the actual stage invoices are not proved."),
    "All oracle inputs have strictly positive rational weights": ("PARTIAL", "integer_update_positive; integer_weights_positive; integer_weights_size_bound; normalized_integer_prior_positive; normalized_integer_prior_sum", "Exact integer updates and positive normalized rational probability vectors are checked, including a magnitude bound. A formal bit-length encoding and polynomial bit-complexity proof is still absent."),
    "Random seeds reduce to a finite proper-tree mixture": ("PARTIAL", "Tree.restricted_height_le_card_pred; Tree.catalog_complete; Tree.restriction_preserves", "The deterministic properization, n-1 bound, and finite enumeration are checked. Almost-sure random-seed measure reduction is not formalized."),
    "Finite LP duality identifies the hardest prior": ("PARTIAL", "randomized_tree_weak_duality; linear_program_weak_duality", "Actual finite-game weak duality and general finite LP weak duality are checked. Equality of the two optima needs unproved strong duality."),
    "An unbalanced integral load costs more than the error budget": ("PARTIAL", "integer_zero_sum_gap", "A nonzero finite integral deviation vector of sum zero has sum of squares at least two. The paper's window identity, error budgets, and scale separation are not formalized."),
}

# Integrated proofs added after the original coverage snapshot. Keep full
# statements distinct from checked construction components and transfers.
COVERAGE.update({
    "thm:kraft": ("PROVED", "Coding.kraft; Coding.kraft_converse", "Both directions for actual finite Boolean-word prefix codes, including zero-length words and prescribed natural lengths, are proved."),
    "lem:log-sum": ("PROVED", "Entropy.log_sum", "The exact finite log-sum inequality is proved from finite Jensen, with nonnegative numerator terms and positive denominator terms. Zero numerator terms use the continuous convention."),
    "lem:entropy-chain-rule": ("PROVED", "Entropy.joint_information_chain_rule; Entropy.shannon_conditional_chain_rule_left; Entropy.determined_chain_rule; Entropy.normalized_entropy_bounds; Entropy.conditionalInformation_nonneg; Entropy.binary_entropy_bounds", "Finite joint, conditional, and functional chain rules are proved on actual partition fibers, together with support-size entropy bounds, nonnegative conditional entropy, and binary entropy bounds."),
    "lem:restriction": ("PROVED", "Tree.disjoint_expected_optima_le; Tree.subset_live_height_optimum_le; Tree.global_expected_minimum; Tree.global_live_height_minimum; Tree.identification_log_liveHeight; Entropy.rational_entropy_lower_bound", "Both optimum restriction inequalities, global optimum attainment, and expected entropy and logarithmic live-height lower bounds are proved in the actual supplied-query model with original weights."),
    "clm:restriction-2": ("PROVED", "Entropy.rational_entropy_lower_bound; Entropy.identifying_tree_entropy_lower_bound_via_kraft", "The expected entropy lower bound is proved on identifying supplied-query trees, both by node induction and independently using their actual prefix-free transcripts, Kraft, and log-sum."),
    "clm:alphabetic-1": ("PROVED", "Coding.midpoint_alphabetic_code", "The actual cumulative-midpoint dyadic code has the required lengths, disjoint ordered cells, prefix freeness, and expected-length bound."),
    "clm:alphabetic-2": ("PROVED", "Coding.alphabetic_threshold_tree", "The code is implemented as a genuine tree of ordered index-threshold queries, with identification, the pointwise log2(1/p)+2 depth bound, and its expected entropy/log(2)+2 bound."),
    "lem:alphabetic-endpoints": ("PARTIAL", "Coding.alphabetic_threshold_tree; Coding.midpoint_alphabetic_code; Coding.intervalDP_global_optimum; Coding.interval_state_count; Coding.interval_transition_count", "The alphabetic construction, actual threshold-tree implementation, both depth bounds, and globally optimal rational interval recurrence are proved. The finite tabulation graph has polynomial size and strictly shorter dependencies; a memoized implementation and rational bit-operation complexity remain unproved."),
    "clm:alphabetic-3": ("PARTIAL", "Coding.intervalDP_lower_bound; Coding.intervalDP_attained; Coding.intervalDP_global_optimum; Coding.interval_dependencies; Coding.interval_state_count; Coding.interval_transition_count", "The executable rational interval recurrence attains the true global optimum against every identifying threshold tree, with at most (r+1)^2 interval states and r(r+1)^2 split candidates in a valid dependency order. Verified memoization and rational bit-operation complexity remain unproved."),
    "thm:helly": ("PROVED", "planar_helly", "The finite planar Helly theorem is proved over every ordered field, including real and rational coordinates and empty families, using mathlib's proved finite-dimensional Helly theorem."),
    "lem:helly": ("PARTIAL", "PlanarInstance.majority_strict_point; planar_helly; PlanarInstance.small_majority_family_intersects", "The full finite family of strict majority half-planes has a common rational point in the actual planar model. Polynomial LP construction and its rational bit-complexity remain unproved."),
    "lem:hull-structure": ("PARTIAL", "RationalLine.normalized_cap_iff; convexHull_cap_domination; two_support_cap_implication; PlanarInstance.zero_pattern_forces_majority; QuerySystem.same_answers_unique", "Normalization, convex-hull cap domination, the two-support implication, and uniqueness of a zero pattern given hull coverage are proved. Adjacent support existence and circular-interval structure remain unproved."),
    "lem:minimum-interval-cover": ("PARTIAL", "IntervalCover.minimumCover_optimal; IntervalCover.solve_sound; IntervalCover.solve_complete; IntervalCover.solve_none_iff; IntervalCover.minimumCover_filter_work; IntervalCover.minimumCover_supplied_discovery", "The actual earliest-right-endpoint algorithm is sound and optimal for ordinary finite intervals, rejects empty demands, uses supplied candidates, and has a quadratic filter-work bound. The circular first-candidate reduction and full bit-complexity are not formalized."),
    "lem:deadline-cover": ("PARTIAL", "DeadlineScheduling.solve_feasible_iff; DeadlineScheduling.graded_solver_complete; DeadlineScheduling.querySpine_route_certificate", "Exact finite deadline feasibility and graded-capacity translation are checked, with legality and actual route depth of the resulting supplied-query spine. The manuscript's special polynomial greedy-prefix certificate is not proved."),
    "prop:qp-grade-schedule": ("PARTIAL", "GradedDP.run_feasible_iff; GradedDP.run_reconstructs; GradedDP.run_card_bound", "The actual compressed count/last-position DP decides ordinary-interval feasibility, reconstructs a distinct candidate schedule, and has at most (B+1)^r(M+1)^r reachable states. Circular cutting, joint-delay optimization, and bit-complexity remain unproved."),
    "lem:lookahead-completion": ("PROVED", "Tree.rollout_identifies; Tree.rollout_expected_real_approximation; Tree.rollout_height_real_approximation; Tree.prefixInvoice_pays_frontier", "An actual finite exact-cost selector compares stopping, legal leaves, and all supplied root queries. Its legal tree costs no more than any competitor's completed prefix; actual frontier accounting removes the stated penalties for arbitrary real coefficients. The baseline guarantees are exactly the proposition's premises."),
    "lem:stage-conversion": ("CONDITIONAL TRANSFER", "flat_stage_absorption; StageLedger.local_to_global; Tree.executable_potential_telescope; Entropy.balanced_cost_partial_stage; Entropy.balanced_cost_identifying; entropy_to_ratio", "Flat-stage algebra, actual balanced-query entropy charging, arbitrary-arity invoice combination, and executable-tree potential cancellation are proved. The complete geometric algorithm's flat-stage invoices and stage-ledger extraction remain obligations."),
    "prop:randomized-duality": ("PARTIAL", "FiniteGame.full_legal_tree_saddle; legal_mixture_log_two_lower_bound; Tree.restricted_height_le_card_pred", "Strong finite legal-tree-game duality, attainment, support at most n, completeness of the proper-tree catalog, and the uniform-prior logarithmic bound are proved. Almost-sure adaptive random-seed reduction remains unproved."),
    "prop:randomized-regret": ("PROVED", "MWU.legal_tree_mixture_regret; MWU.integer_depth_regret; MWU.integer_prior_eq; MWU.restricted_depth_cap", "The complete stated depth-scaled regret bound is proved from the actual weight recurrence, with exact rational normalized priors and a legal uniform mixture of supplied-query trees."),
    "prop:randomized-compression": ("PARTIAL", "FiniteGame.compressed_legal_tree_game; MWU.integer_prior_eq; integer_weights_positive; integer_weights_size_bound; normalized_integer_prior_positive; normalized_integer_prior_sum", "Optimal finite legal-tree mixtures with support at most n, exact positive rational iterative priors, and weight magnitude bounds are proved. Rational basic-solution encoding, polynomial bit-length, and exact fair-bit sampling complexity remain unproved."),
    "thm:randomized-transfer": ("CONDITIONAL TRANSFER", "randomized_transfer_arithmetic; randomized_calibration; MWU.legal_tree_mixture_regret; FiniteGame.full_legal_tree_saddle; legal_mixture_log_strict_lower_bound", "Regret, hardest-prior duality, and the strict entropy lower bound are now proved, alongside final parameter/ratio arithmetic. Oracle guarantees depend on the unfinished expected-depth algorithms; polynomial bit complexity and exact sparse rational sampling remain unproved."),
    "prop:boundary": ("PROVED", "TernaryTree.expected_real_approximation_transfer; TernaryTree.height_real_approximation_transfer; RationalLine.virtualShift_semantics; RationalLine.virtualShift_offLine; finite_rational_margin", "Actual two-bit ternary simulation preserves identification and gives the factor-two transfer for both costs with arbitrary nonnegative real approximation factors. Positive rational margins realize both virtual predicates by shifted off-line planar lines. Polynomial bit-complexity is separate from this factor statement."),
})

TITLE_COVERAGE.update({
    "A positive margin gives a rational strict witness": ("PARTIAL", "PlanarInstance.majority_strict_point", "A strict rational common witness for the full family is proved directly by rational Helly. The stated polynomial margin-LP construction and numerical encoding bound remain unproved."),
    "Counts and last positions decide every interval deadline": ("PARTIAL", "GradedDP.run_feasible_iff; GradedDP.run_reconstructs; GradedDP.run_card_bound", "The actual compressed DP's feasibility equivalence, state merging, schedule reconstruction, and product state-count bound are checked. A formal bit-operation running-time proof remains unproved."),
    "Finite LP duality identifies the hardest prior": ("PROVED", "FiniteGame.full_legal_tree_saddle", "Strong duality and attainment are proved for the entire supplied-query tree problem using compact convex separation and a complete finite proper-tree catalog. The dual prior bounds every identifying tree, not merely catalog members."),
    "The uniform prior provides a logarithmic lower bound": ("PROVED", "legal_mixture_log_two_lower_bound; legal_mixture_log_strict_lower_bound", "Kraft and log-sum on actual identifying trees give log2(n) <= every feasible finite-mixture randomized height; natural log(n) is strictly smaller for n >= 2."),
    "Individual weight growth is paid by total weight growth": ("PROVED", "MWU.individual_lower; MWU.total_log_upper; MWU.potential_comparison; MWU.integer_weights_eq", "The actual weight recurrence satisfies both logarithmic potential estimates and their comparison; clearing denominators preserves the normalized update."),
    "The potential comparison gives the stated regret": ("PROVED", "MWU.gain_regret; MWU.integer_depth_regret; MWU.legal_tree_mixture_regret", "The explicit logarithmic coefficient bounds, depth rescaling, and finite uniform-tree mixture produce the complete stated regret estimate."),
    "An optimal basic mixture uses at most $n$ trees": ("PARTIAL", "FiniteGame.compressed_legal_tree_game", "An optimal mixture of at most n actual legal trees is proved, and no finite mixture of the input family has lower randomized height. The additional rational basic-solution and determinant bit-length claims remain unproved."),
    "Later deadlines cannot change a prefix greedy choice": ("PROVED", "PriorityPrefix.lower_priority_geometric_budget; PriorityPrefix.finite_suffix_sum_below_level; PriorityPrefix.priority_level_sum_divisible; PriorityPrefix.priority_score_dominates_suffix; PriorityPrefix.global_maximizer_maximizes_prefix; PriorityPrefix.full_priority_score_split; PriorityPrefix.earlier_priority_score_divisible; PriorityPrefix.later_priority_score_lt_unit; PriorityPrefix.ranked_global_maximizer_maximizes_prefix", "The finite ranked-class model assigns each candidate the sum of the weights of its remaining hit classes. With at most s classes and base-(s+1) rank weights, every global score maximizer also maximizes every deadline-prefix score, including arbitrary ties. The construction of geometric classes and a polynomial implementation of the complete scheduler remain outside this local claim."),
    "The maximum-depth penalty is paid on every frontier path": ("PROVED", "Tree.rollout_height_real_approximation; Tree.completePrefix_height_real_envelope", "The actual finite exact lookahead and height envelope pay every frontier penalty, including paths that end before the horizon."),
    "Expected prefix cost pays for every surviving frontier mass": ("PROVED", "Tree.prefixInvoice_pays_frontier; Tree.rollout_expected_real_approximation", "The actual completed-prefix frontier has its mass paid k times by the prefix invoice, and the finite exact rollout inherits the resulting approximation guarantee."),
})


def uncomment(text):
    return re.sub(r"(?<!\\)%[^\n]*", "", text)


def active_files(path, seen=None):
    if seen is None:
        seen = set()
    path = path.resolve()
    if path in seen:
        return
    seen.add(path)
    yield path
    text = uncomment(path.read_text(encoding="utf-8"))
    for match in INPUT.finditer(text):
        child = ROOT / (match.group(1) + ".tex")
        yield from active_files(child, seen)


records = []
for path in active_files(ROOT / "planar-line-decision-trees.tex"):
    text = uncomment(path.read_text(encoding="utf-8"))
    for match in CLAIM.finditer(text):
        end = text.find("\\end{" + match.group(1) + "}", match.end())
        if end < 0:
            raise ValueError(f"Unclosed claim in {path}:{match.start()}")
        body = text[match.end():end].strip()
        labels = re.findall(r"\\label\{([^}]+)\}", body)
        line = text.count("\n", 0, match.start()) + 1
        label = labels[0] if labels else f"{path.relative_to(ROOT).as_posix()}:{line}"
        status, lean, scope = COVERAGE.get(label, TITLE_COVERAGE.get(match.group(2) or "",
            ("NOT FORMALIZED", "", "The exact TeX statement is inventoried, but no Lean statement or proof is supplied for this full manuscript claim.")))
        records.append(dict(label=label, environment=match.group(1),
                            title=match.group(2) or "", file=path.relative_to(ROOT).as_posix(),
                            line=line, status=status, lean=lean, scope=scope, tex=body))

# A typo in a proof mapping must not silently turn into a claimed proof.
declaration_file = OUT / "proved-declarations.json"
if declaration_file.exists():
    proved_names = {rec["name"] for rec in json.loads(declaration_file.read_text(encoding="utf-8"))}
    missing_names = set()
    for rec in records:
        for short_name in rec["lean"].split("; "):
            if short_name and "PlanarQuery." + short_name not in proved_names:
                missing_names.add(short_name)
    if missing_names:
        raise ValueError("Coverage refers to declarations absent from the source audit: " +
                         ", ".join(sorted(missing_names)) + ". Run audit.py after adding modules.")

(OUT / "claims.json").write_text(json.dumps(records, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
md = ["# Coverage of every active manuscript claim", "",
      "This is a coverage inventory, **not a claim of complete formal verification**.",
      "Every theorem, lemma, proposition, corollary, and named or unnamed claim in active TeX inputs is listed.",
      "`PROVED` means the complete mathematical statement has a corresponding kernel-checked proof.",
      "`PARTIAL` identifies precisely which component is checked; it does not certify the full manuscript claim.",
      "`CONDITIONAL TRANSFER` proves explicit combination/algebraic steps; the listed geometric, algorithmic, or analytic premises remain unproved.",
      "`NOT FORMALIZED` is an explicit outstanding obligation. No unproved claim is declared as a Lean axiom.", "",
      "| Claim | Status | Lean theorem(s) and scope |", "|---|---|---|"]
for rec in records:
    title = rec["title"].replace("|", r"\|")
    display = rec["label"] + (f" - {title}" if title else "")
    detail = ("`" + rec["lean"] + "`. " if rec["lean"] else "") + rec["scope"]
    md.append(f"| {display} | {rec['status']} | {detail} |")
counts = {status: sum(rec["status"] == status for rec in records)
          for status in ["PROVED", "CONDITIONAL TRANSFER", "PARTIAL", "NOT FORMALIZED"]}
md += ["", f"Total active claims: {len(records)}.",
       "Coverage counts: " + "; ".join(f"{status}: {count}" for status, count in counts.items()) + ".", "",
       "The exact raw statement and source location of each claim are saved in `claims.json`.",
       "Regenerate this inventory with `python formalization/inventory.py` after edits to the active manuscript.", ""]
(OUT / "CLAIMS.md").write_text("\n".join(md), encoding="utf-8")
print(f"Inventoried {len(records)} active formal claims.")
