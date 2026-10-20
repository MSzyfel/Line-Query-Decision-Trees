# Cooperative verification states for a weighted completion pricer

Auxiliary research note, 18 October 2026. No article edits. All algorithms below use original supplied tests and fixed-exponent polynomial runtime for every fixed coalition width b.

The implementation is binary. The verifier/composition bounds and incident-pair score extend to any fixed response count by retaining every non-target outcome as a stopped exit and summing (3)-(4) over all outcomes; that extension is not separately implemented in this checker.

**Current result.** This pass produces an executable polynomial pricing candidate with two new code generators. The coalition-of-two generator repairs all four previously documented finite fixed points, including the latest 18-hypothesis incumbent of cost 81 versus optimum 79. It reaches the exact optimum in all four cases. A constant-factor comparison is proved against partial policies that finish at most b hypotheses; the unrestricted pricing guarantee remains open. These finite repairs are not an asymptotic approximation theorem.

The implementation and audits are in research-general-pricing-oracle.py, with exact numerical records in research-general-pricing-oracle-results.json. The root's completion-cover/pricing reduction is in research-general-pricing-next.md.

## 1. Why a verification oracle needs cooperative branching

For a current full tree T, prizes are w_h=d_T(h), integers in [1,n-1]. The pricing objective is

    rho(P) = W(P) / sum_{h identified by P} w_h,

where every hypothesis pays for the queries its path encounters, including hypotheses left unfinished.

A nontrivial policy starts with a query of raw cost n. A policy that identifies only one hypothesis has prize at most n-1. It cannot satisfy rho<1 and therefore cannot by itself certify an improving move. Verification matters here as a generator of reusable **conditional states and cooperative codes**, not as a claim that individually cheap certificates solve the pricing problem.

There is a second caution. Even a random-pivot verifier can choose singleton tests before an available balanced code. On a Boolean cube with coordinate and all singleton tests, greedy verification of h queries its singleton first; repeating such verifications gives expensive singleton search, while coordinate coding costs log_2 n per hypothesis. Thus verification alone has no asserted global approximation.

## 2. A polynomial greedy verifier with an audited constant

Fix target h. While the current set R containing h is not a singleton, choose the original test with the smallest outcome class containing h. Continue on that class and stop unfinished on the other outcome. This is an explicit verification spine. Let V_h be its raw work.

For each test tau define B_tau={g:tau(g)!=tau(h)}. These cover H minus {h}. Add one analytical singleton set {h}, solely for an MSSC comparison, and break ties in favor of actual B_tau sets. Until the other hypotheses are covered, some B_tau covers a remaining element, so ordinary maximum-coverage greedy always chooses an actual set before the analytical singleton. If the actual spine has length k and g exits at time t_g, its augmented MSSC objective is

    (k+1) + sum_{g!=h} t_g = V_h+1.

Appending the analytical singleton after any optimal h-verification spine gives MSSC objective V_h*+1. The classical greedy four-approximation therefore yields

    V_h <= 4V_h*+3.                                             (1)

This comparison uses the proved MSSC theorem of Feige, Lovasz, and Tetali, [Approximating Min-sum Set Cover](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf). The analytical singleton is never executed as a new decision-tree test.

The additive constant matters for an honest finite statement. For n>=3, V_h*>=n gives V_h<=5V_h*. The n=2 case is exact.

## 3. Coalition composition preserves observations

Precompute the greedy verification sequence for each h on the original full set. For every ordered coalition C=(h_1,...,h_k), k<=b:

1. Start with the single unfinished root state H.
2. Locate the current frontier cell containing h_i.
3. Restrict h_i's precomputed verification spine to that cell, omitting constant queries. Execute it only there. Preserve all exit cells and their learned answers.
4. Continue with the next coalition member. Every singleton cell counts as an actual identification, including any extra singleton formed by inference.

This yields a partial policy P_C identifying at least C. It is cooperative: the second verifier starts in the state created by the first verifier's actual answers. It is not a list of independent full-instance invoices. To make a complete code template, fill every remaining nonsingleton frontier cell with the ordinary greedy code. All its states can then enter the represented-state pricing DAG.

**Theorem 1 (restricted comparator guarantee).** For every partial policy P that identifies k<=b hypotheses, the generated pool contains an executable partial policy Q with

    rho(Q) <= (4+3/n) k rho(P) <= 5b rho(P)      for n>=3.        (2)

This holds for arbitrary nonnegative integer prizes whenever the comparison policy collects positive prize, not only incumbent depths.

Let C be the completed hypotheses of P. For each h in C, keep only P's root-to-h spine and stop on all other exits. This is a legal h-verifier of work at most W(P). Equation (1) gives V_h<=4W(P)+3. Composition can only reduce each verifier's full-instance work, so

    W(P_C) <= sum_{h in C} V_h <= 4kW(P)+3k.

Its collected prize is at least that of C. Since W(P)>=n at the root, division gives (2). An ordering of C is enumerated by the generator, so the argument does not assume a hidden choice of targets. Exact pruning/recombination in the represented-state DAG can only improve the pool's best density.

This is a genuine constant comparison for fixed-size completion coalitions. It is not a constant approximation to unrestricted pricing: an optimum partial policy may identify arbitrarily many hypotheses whose cooperation is essential.

## 4. A different target-aware pair-gain generator

The second candidate interpolates between verification and branching codes. Choose a target region R and positive target prizes w_h. At current S define W_R(S)=sum_{h in S intersect R} w_h and choose a test maximizing

    G_tau(S,R)
      = |S| W_R(S) - sum_a |S_a| W_R(S_a).                      (3)

This counts weighted target-competitor pairs separated by the test. Competitors outside R are counted because they still incur actual query work. Recurse on every child containing a target and fill target-free exits with ordinary greedy when making a complete template.

For a single target, (3) chooses the smallest outcome class containing it, recovering the MSSC verification rule. For R=S with equal prizes, it is the usual pair/Gini split gain. For general target prizes it differs from minimizing the larger **prize mass** outcome: the actual numbers of target-free competitors also enter (3).

The polynomial target-region list contains:

* every incumbent subtree state;
* both outcomes of every supplied binary test;
* all high-prize level sets {h:w_h>=theta};
* the full set H.

Each generated tree is executable and proper. When a current target remains and |S|>1, separability ensures some query has positive gain. No universal approximation guarantee is proved for this target-pair rule. Its value is as a specific competing generator, with its exact code and work available to the pricer.

## 5. Exact pricing in the generated state DAG

The candidate retains states from the incumbent, from every coalition template, from the target-pair templates, and from the existing forced-root fresh-greedy templates. It then adds all pairwise intersections of those base states, as in the team's previous quadratic construction. On this fixed represented family, each original test may be used when both child states are represented. A nonsingleton may stop unfinished at value zero; a singleton earns its input prize.

For a rational density parameter lambda, maximize

    lambda * completed prize - raw work

by the exact state recurrence

    V_lambda({h})=lambda*w_h,
    V_lambda(S)=max(0, max_tau[sum_a V_lambda(S_a)-|S|]).           (4)

The implementation uses (4) at lambda=1 to obtain the largest represented prize-work profit, then appends the incumbent restricted to each unfinished leaf. Positive profit strictly decreases the integer full-tree cost. At most n(n-1) accepted passes occur.

It also implements an exact **minimum-density oracle** for the represented family. Start with any represented complete code of density rho. Solve (4) at lambda=rho. A positive optimum supplies a represented policy of strictly smaller W/prize; replace rho by that rational ratio. When the optimum is zero, the current rho is the exact minimum. For incumbent-depth prizes, both W and total prize are integers at most n(n-1), so at most O(n^4) distinct ratios occur. Every recurrence evaluation and every reconstruction is polynomial. This is an actual finite polynomial pricing routine, not an assumed exact optimizer for unrestricted histories.

Pairwise intersections preserve support for a full code: restrict the supplied code on A to A intersect B; all its surviving node sets are intersections of a base code node with B. Thus full represented codes remain available. The profit recurrence additionally allows partial stopping.

## 6. Runtime and implementation limits

There are O(n^b) ordered coalitions for fixed b, up to the fixed factor b!. Each composed proper policy and each completed template has O(n) nodes. Coalition base-state count is therefore O(n^(b+1)). The target-pair region list has O(n+m) entries, each with O(n) nodes. Existing forced-root conditional greedy templates at O(n) incumbent nodes and m tests add only a fixed polynomial number of states. Quadratic intersections square that finite bound. Construction, state-DAG evaluation, and the bounded integer improvement loop therefore have fixed-exponent polynomial runtime in n,m for every fixed b.

The actual code uses b=2. Allowing b to grow with n would change this to a superpolynomial enumeration and is not proposed as an unrestricted polynomial algorithm. The theoretical polynomial bounds are generous and are not offered as practical scalability estimates.

## 7. Finite repairs and independent checks

The inherited baseline includes fresh conditional greedy codes, all single-target verification-first full templates, quadratic intersection synthesis, and exact incumbent-depth profit. The following results are reproduced by the new script without giving OPT to the candidate:

| Hypotheses | Baseline raw cost | Coalition-two result | Target-pair result | Combined result | Exact OPT, validation only |
| --- | --- | --- | --- | --- | --- |
| 12, first witness | 47 | 46 | 46 | 46 | 46 |
| 12, second witness | 47 | 45 | 45 | 45 | 45 |
| 18, first witness | 85 | 80 | 80 | 80 | 80 |
| 18, enriched-stable witness | 81 | 79 | 81 | 79 | 79 |

The final witness also defeats the other agent's fresh depth-, squared-depth-, and high-depth-biased greedy templates plus small exact tails. Coalition composition supplies the missing interaction on that instance. The distinct target-pair generator repairs the earlier three witnesses but fails on this fourth one, so it is not silently credited with the coalition repair.

The script records ordered test masks, generated state counts, exact prize-work gains, and every accepted pass in research-general-pricing-oracle-results.json. It also checks 912 small one-/two-target comparisons against an independently solved full adaptive target-completion recurrence, and checks the rational density descent against exhaustive represented-policy reward profiles on small instances.

These are finite candidate tests. An adversarial search against the coalition-two generator is the next necessary audit. The four successes do not establish a bound on its pricing loss, and the unrestricted target remains open.

## 8. Whole-family escape mechanism on row-decoy/gated-column grids

The additional checker research-general-pricing-grid.py uses full product grids with C columns and r=2^b rows, every column-membership test, all column-gated coordinate tests, and the minority-child tests of a recursive row tree. There are exactly

    m=C+Cb+(r-1)=O(n),       n=Cr.

It tests both the classical minority size 1+floor(s/C) and the more robust scale 1+floor(2s/C), capped at floor(s/2). Only the designated minority child is supplied as a row decoy. These are the row-decoy variants used in the existing general notes. The uniform-count greedy code is checked to identify the row first and then use column singleton search.

Here is a complete, family-wide **escape statement**, rather than an approximation claim. Let R_raw be the row code's raw cost and C_R=R_raw/r. Put Q(C)=C(C+1)/2-1. The row-first incumbent has cost

    F_bad = C R_raw + r Q(C).

Force one column-membership query, decode its positive column with the fresh b-coordinate code, and put the incumbent restricted to the other C-1 columns on its negative side. The resulting full original-test tree has cost

    F_new = Cr + rb + (C-1)R_raw + rQ(C-1),
    F_bad-F_new = R_raw-rb = r(C_R-b).                            (5)

The positive fresh code is in the forced-root template library. Every node of the negative restricted incumbent has form B intersect (H minus column), where B is an incumbent node; these are in the quadratic represented family. Therefore the exact represented profit is at least (5). Whenever the row code is less efficient than the b-bit coordinate code, the pricer must escape that row-first incumbent in one pass, however long a useful complete selector spine might be. The proof uses the actual full-code saving, including savings on unfinished fallback paths; it is stronger than claiming a one-column completion invoice is profitable.

This mechanism already belongs to fresh-code/restriction synthesis; the coalition-of-two generator is not credited with inventing it. Its relevance is that the stronger candidate preserves a provable escape on a full O(n)-test family, beyond isolated small repairs.

For the minority-size 1+floor(s/C) family there is an even simpler eventual behavior. If r>C(C-1), then (C-1)(1+floor(r/C))<r. After one forced column query, on the negative branch every row decoy has minority size below r, while a column query has minority size r. Fresh greedy therefore selects columns, and inside each column the gated coordinates give the b-bit code. One forced-root fresh-greedy template already supplies the entire column-first code of mean Q(C)/C+b. The robust scale-two family does not satisfy that one-column threshold in general; (5) still applies.

The checker runs the actual coalition-two pricer on 64- and 128-hypothesis full grids and verifies its profit exceeds the certified one-column gain. On larger grids through n=16384,m=1199, it verifies the actual greedy incumbent, the explicit improving full code, exact gain (5), and the represented-state membership certificate. It avoids materializing the large quadratic pool for those larger cases; this distinction is recorded in the results JSON. Both decoy scales pass. These checks establish escape mechanisms, not a final approximation factor on all grid variants or unrestricted instances.

A useful boundary on the restricted theorem is also explicit: if a completion policy finishes at most b hypotheses and b*max_h d_T(h)<n, its completion reward cannot exceed its root work. Thus fixed-b partial pricing alone cannot certify improvement in that regime. The filled full templates and their cooperative recombination are essential parts of this candidate.
