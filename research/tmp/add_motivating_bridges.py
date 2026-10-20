"""One-shot, prose-only motivation pass over four root-owned sections."""
from pathlib import Path

plans = {
    "sections/02-preliminaries.tex": [
        (r"\begin{theorem}[Kraft's inequality for binary prefix codes]",
         "Query transcripts occupy disjoint leaves of a binary code. The next\n"
         "inequality expresses their limited capacity; it will turn leaf depths\n"
         "into lower bounds on both decision-tree objectives."),
        (r"\begin{lemma}[Log-sum inequality]",
         "To lower-bound average depth, we compare hypothesis probabilities\n"
         "with the capacities assigned to their codewords. Log-sum makes this\n"
         "comparison without any assumption on the smallest probability."),
        (r"\begin{lemma}[Entropy chain rule]",
         "A stage first reveals a pattern and then identifies the hypothesis\n"
         "within that pattern. The chain rule separates these two information\n"
         "costs, so endpoint recovery can be charged only for what remains unknown."),
        (r"\begin{lemma}[Alphabetic threshold codes]",
         "An information-efficient code must also respect the queries we can\n"
         "ask. For ordered endpoint outcomes, alphabetic codes keep each branch\n"
         "consecutive and therefore make the coding bound executable by thresholds."),
        (r"\begin{lemma}\label{lem:restriction}",
         "Revealing an output class can only make identification easier: queries\n"
         "whose answers are then known disappear. This observation compares\n"
         "recursive optima, while the coding inequalities provide a lower bound\n"
         "on how much work any identifying tree still requires."),
        (r"\begin{claim}[Threshold implementation preserves the depth bound]",
         "The cells have given an abstract ordered code. We now check that its\n"
         "branches are legal threshold comparisons and that converting the code\n"
         "to a tree preserves the promised depth."),
        (r"\begin{claim}[An interval recurrence minimizes expected depth]",
         "The explicit code supplies a bound for each outcome. When only average\n"
         "depth matters, the consecutive ranges also admit an exact optimization\n"
         "that avoids constructing long codewords for very small probabilities."),
        (r"\begin{claim}[Entropy lower-bounds the expected invoice]",
         "Restriction gives feasible subproblem trees but does not yet say how\n"
         "expensive any such tree must be. The next claim uses their transcripts\n"
         "to obtain the distribution-sensitive lower bound."),
        (r"\begin{claim}[Binary capacity lower-bounds height]",
         "For maximum depth, probabilities are irrelevant. Counting the leaves\n"
         "that fit within a given height gives the corresponding lower bound."),
        (r"\begin{theorem}[Planar Helly theorem]",
         "The geometry will produce witnesses for every three majority sides.\n"
         "The planar Helly theorem is the step that turns this local consistency\n"
         "into a single witness for all supplied lines."),
    ],
    "sections/03-common-witness-geometry.tex": [
        (r"\begin{lemma}[Common witness]",
         "The majority answers must describe one coherent route before we can\n"
         "compare our discovery schedule with an optimal tree. A common witness\n"
         "provides that route even when no hypothesis has all majority answers."),
        (r"\begin{lemma}[Hull support and pattern structure]",
         "The witness lets us express every query relative to the same origin.\n"
         "The next lemma identifies the two properties that make this useful:\n"
         "each original cap is covered by adjacent hull caps, and each target\n"
         "sees those hull tests as one interval."),
        (r"\begin{lemma}[Minimum interval cover]",
         "A complete discovery route must hit every nonzero pattern. Once these\n"
         "patterns are intervals, we can compute its smallest possible test set;\n"
         "this will also provide the final budget in the batch construction."),
        (r"\begin{lemma}[Greedy cover length with adjacent-run credit]",
         "Priority and weight considerations can change the order in which tests\n"
         "are chosen. We therefore also need a length bound for greedy discovery,\n"
         "including the extra saving when the comparison cover has adjacent runs."),
        (r"\begin{lemma}[Query-free endpoint representation]",
         "Finding one positive vertex locates a small cap but does not determine\n"
         "the entire pattern. To recover the pattern cheaply, we need to open\n"
         "the circular order at a safe cut and justify every endpoint comparison."),
        (r"\begin{claim}[A positive margin gives a rational strict witness]",
         "Existence alone does not give the preprocessing algorithm. The next\n"
         "step converts the strict intersection into a rational witness that can\n"
         "be computed and encoded with polynomially many bits."),
        (r"\begin{claim}[Negative support answers force the original answer]",
         "The support expression is useful because it transfers a negative\n"
         "answer from the hull tests back to the original query. Only this\n"
         "one-way implication is needed to cover an optimal witness route."),
        (r"\begin{claim}[The hull patterns are intervals with at most one zero point]",
         "Having justified cap coverage, we now describe the states produced\n"
         "by hull tests. Their interval structure enables the scheduling tools;\n"
         "the uniqueness of the zero pattern makes the final negative route valid."),
        (r"\begin{claim}[An extreme greedy choice removes an extreme cover point]",
         "At an extreme, greedy can be charged to one comparison-cover point:\n"
         "the demands it removes are exactly those removed by that point. This\n"
         "is the induction step that reduces the cover size."),
        (r"\begin{claim}[An interior choice creates independent left and right problems]",
         "An interior choice need not remove a comparison-cover point. Instead,\n"
         "it separates the remaining demands, and the combined size-plus-run\n"
         "charge of the two sides supplies the required progress."),
        (r"\begin{claim}[The opposite-edge cut costs no query]",
         "When cached answers do not provide the cut, we must obtain one from\n"
         "the geometry itself. The origin prevents a compatible positive\n"
         "interval from crossing the opposite edge."),
        (r"\begin{claim}[Endpoint comparisons are supplied hull queries]",
         "The cut has removed wrap-around. We can now verify that learning the\n"
         "two endpoints amounts to asking existing hull tests, which is essential\n"
         "for keeping the construction within the supplied-query model."),
    ],
    "sections/05-scheduling.tex": [
        (r"\begin{lemma}[Exact budgeted interval coverage]",
         "The batch method needs the best covered weight for each integer\n"
         "budget, rather than just a minimum complete cover. The interval order\n"
         "makes this stronger optimization possible by remembering only the\n"
         "previous selected position."),
        (r"\begin{proposition}[A shifted schedule has a discrete invoice]",
         "We first bound a particular schedule before choosing its shift. The\n"
         "invoice retains integer budgets, since rounding savings in the early\n"
         "phases affect the final approximation factor."),
        (r"\begin{proposition}[One shift distribution pays both invoices]",
         "A shift that is good for likely positive targets might leave a long\n"
         "negative route. The next proposition averages both costs under one\n"
         "distribution, allowing them to be optimized together."),
        (r"\begin{proposition}[A finite shift search suffices]",
         "The average proves that a good schedule exists. Integer budgets change\n"
         "only at explicit breakpoints, so a finite search can find a schedule\n"
         "with at most that joint cost."),
        (r"\begin{claim}[Phase coverage and schedule length]",
         "Two global safeguards come first: each phase covers at least as much\n"
         "weight as a comparison prefix with the same budget, and geometric\n"
         "growth bounds the total number of tests."),
        (r"\begin{claim}[First-cover cost within one batch]",
         "Phase-end coverage alone would charge every new hit at the end of its\n"
         "batch. Greedy places the largest new gains first, giving the half-batch\n"
         "saving captured by the next claim."),
        (r"\begin{claim}[Shift-averaged schedule length]",
         "Positive first-cover times do not account for a target that receives\n"
         "only misses. We now average the length under the very same shift, so\n"
         "the two bounds can subsequently be added."),
    ],
    "sections/06a-quasipolynomial.tex": [
        (r"\begin{proposition}[Graded interval scheduling]",
         "A nearly exact schedule must satisfy several early-rank requirements\n"
         "at once. Separate coverage optima need not have compatible prefixes;\n"
         "the graded dynamic program retains that compatibility explicitly."),
        (r"\begin{proposition}[Graded continuation bounds]",
         "Scheduling ranks is only part of identification: endpoint recovery\n"
         "and later recursive work still cost queries. The next proposition\n"
         "combines them with restriction credit, leaving a small state potential\n"
         "as the only additive penalty."),
        (r"\begin{proposition}[Lookahead removes a bounded continuation penalty]",
         "The continuation bound alone is not the desired multiplicative result.\n"
         "Optimizing an initial prefix lets its queries be charged at their actual\n"
         "cost, and the resulting saving absorbs the remaining penalty."),
        (r"\begin{claim}[Counts and last positions decide every interval deadline]",
         "Each grade prefix has two obligations: stay within its rank budget and\n"
         "hit every interval whose deadline it represents. Counts enforce the\n"
         "first; the last selected position suffices to check the second."),
        (r"\begin{claim}[Rounded delays bound the joint objective]",
         "Exact deadline feasibility must now become an approximation for delay.\n"
         "Charging the first qualifying grade bounds each positive delay, while\n"
         "the final selected count also prices the complete negative route."),
        (r"\begin{claim}[An adjacent block has a uniform endpoint allowance]",
         "A block rank must be translated back into real queries. The next claim\n"
         "combines the two possible discovery exits with endpoint recovery;\n"
         "the second exit benefits from the cached negative first endpoint."),
        (r"\begin{claim}[Downward rounding retains every required integer rank]",
         "The computed deadlines use actual child heights, so their feasibility\n"
         "requires care with integer rounding. Restriction supplies the needed\n"
         "rank credit before the deadline is rounded down to a grade."),
        (r"\begin{claim}[Weighted delay and discovery information bound the expected stage]",
         "For expected depth, the same witness comparison is summed with the\n"
         "original hypothesis weights. Discovery information then pays for the\n"
         "endpoint allowance, giving a local bound that cancels through recursion."),
        (r"\begin{claim}[The maximum-depth penalty is paid on every frontier path]",
         "To analyze lookahead, compare with a prefix of an optimal tree. On\n"
         "every unfinished maximum-depth route, the prefix has already consumed\n"
         "exactly the queries that create the saving against factor~$a$."),
        (r"\begin{claim}[Expected prefix cost pays for every surviving frontier mass]",
         "The expected-depth comparison needs no common leaf depth. Only the\n"
         "mass still unfinished matters: each such hypothesis has paid all\n"
         "prefix queries, so their total payment absorbs its continuation penalty."),
    ],
}

proof_plans = {
    "sections/03-common-witness-geometry.tex": [
        (r"\begin{proof}[Proof of Lemma~\ref{lem:helly}]",
         "There are two distinct tasks: obtain a common strict point from\n"
         "flatness, then find such a point with controlled rational encoding.\n"
         "The following claims separate the geometric existence argument from\n"
         "its algorithmic realization."),
        (r"\begin{proof}[Proof of Lemma~\ref{lem:hull-structure}]",
         "We establish the structure in three steps. First represent each query\n"
         "by neighboring hull vertices; next prove the cap-cover implication;\n"
         "finally identify the interval patterns and the unique possible\n"
         "all-zero target. Each step is used by a different part of the algorithms."),
        (r"\begin{proof}[Proof of Lemma~\ref{lem:legal-endpoint-queries}]",
         "First exploit a cached negative answer if one exists. Otherwise find a\n"
         "safe cut geometrically. After either construction, verify that the\n"
         "resulting endpoint searches ask only supplied hull queries."),
    ],
    "sections/05-scheduling.tex": [
        (r"\begin{proof}[Proof of Proposition~\ref{prop:batch-average}]",
         "A logarithmic shift moves the phase boundaries across every scale\n"
         "with the same density. After substitution, their averaging intervals\n"
         "tile $[1,\\infty)$; this yields one integral for discovery and another\n"
         "for waiting. Keeping floors in both integrals preserves the discrete savings."),
    ],
}

for filename, insertions in plans.items():
    path = Path(filename)
    original = path.read_text(encoding="utf-8")
    rewritten = original
    additions = []
    for anchor, prose in insertions:
        assert rewritten.count(anchor) == 1, (filename, anchor)
        addition = prose + "\n\n"
        rewritten = rewritten.replace(anchor, addition + anchor, 1)
        additions.append(addition)
    for anchor, prose in proof_plans.get(filename, []):
        assert rewritten.count(anchor) == 1, (filename, anchor)
        addition = "\n" + prose + "\n"
        rewritten = rewritten.replace(anchor, anchor + addition, 1)
        additions.append(addition)
    recovered = rewritten
    for addition in reversed(additions):
        assert recovered.count(addition) == 1
        recovered = recovered.replace(addition, "", 1)
    assert recovered == original, filename
    path.write_text(rewritten, encoding="utf-8", newline="\n")
    print(f"{filename}: {len(additions)} prose additions; original text recovered exactly")
