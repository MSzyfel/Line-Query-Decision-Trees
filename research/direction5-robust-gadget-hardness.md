# Direction 5: robust coupled choices and several witnesses

Research audit, 13 October 2026. The model is identification of finitely many planar hypotheses by a supplied separating family of binary, unit-cost line queries. Every supplied query is legal at every node. Queries may be reused in different branches. The results below distinguish proved structural obstructions from unproved reduction projects.

This direction did **not** produce an APX-hardness theorem. It produced three useful gadget rejection criteria, a stronger exact tractability result for uniform two-point caps, and a more precise target for a gap-preserving construction. The new quasipolynomial `(2+epsilon)` algorithms do not preclude fixed-factor hardness below two; they do mean that no geometric reduction should casually import the logarithmic hardness of unrestricted test systems.

## 1. A supplied query can always be asked early at small additive cost

Let `T` be any proper identifying tree, with raw prior weights `w_h>0`, total weight `Omega`, and maximum depth `H(T)`. For a supplied query `q`, let `U_T(q)` be the set of hypotheses whose route in `T` asks `q`. A proper tree never asks the same binary query twice on one route, because its second answer would be known.

**Query-promotion lemma.** There is a proper tree `T'` whose root asks `q`, unless `q` is constant on the complete instance, such that

\[
 d_{T'}(h)\le d_T(h)+1-\mathbf 1_{h\in U_T(q)},
\]

\[
 G(T')\le G(T)+\Omega-w(U_T(q)),\qquad
 H(T')\le H(T)+1.
\]

**Proof.** Put `q` at the root. Under each outcome attach `T` restricted to the hypotheses giving that outcome; suppress nodes with only one nonempty answer. Every surviving route is a subsequence of its old route. If the old route contained `q`, that node is now constant and is suppressed. If it did not, the new root is the only additional node. Multiply the pointwise inequality by the weights and sum. Empty outcomes and all other constant nodes can be suppressed. This construction uses only supplied queries and works in every dimension.

For a set `Q` of `k` distinct supplied queries, put the queries into a common prefix and then attach the restricted original tree at each attainable transcript. The analogous bound is

\[
 d_{T_Q}(h)\le d_T(h)+k-|Q\cap\operatorname{path}_T(h)|,
\]

\[
 G(T_Q)\le G(T)+k\Omega-
 \sum_{q\in Q}w(U_T(q)),\qquad H(T_Q)\le H(T)+k.
\]

The prefix contains only attainable answer branches and can be pruned; it need not have `2^k` nonempty leaves. The output remains a proper identification tree with at most `n-1` internal nodes.

**Consequence for reductions.** A gadget cannot penalize asking one specified downstream test prematurely by an arbitrarily long compulsory detour. Starting from its intended tree, that test can be moved to the root for at most one extra query on any route. Moving `k` distinct tests early costs at most `k` in height and `k*Omega` in raw expected cost. A proposed gate must therefore make evasion require many distinct useful questions, or lose an advantage that is not just the order in which a fixed test is asked.

This is an upper bound, not a theorem excluding every order gadget. A unit-cost order preference is possible. A claimed order penalty larger than the promotion bound needs another explicit mechanism.

There is a simpler related fact: if a query is constant on a state `S`, it is constant on every subset of `S`. Restriction cannot activate a previously uninformative query. Geometric incidence alone cannot make a test unavailable before a gate and informative after it.

This sharply separates the present model from [Szyfelbein and Dereniowski's precedence-constrained decision trees](https://arxiv.org/abs/2602.21312), where legal trees must respect an externally specified predecessor relation. Their constraints are part of the input model. They cannot be imported by drawing a line and calling it a gate.

## 2. Several witnesses do not automatically synchronize branch choices

**Independent-continuation lemma.** Fix a supplied-query routing tree `R` whose leaves partition the hypothesis set into `S_1,...,S_k`. Write

\[
 C_R=\sum_h w_h d_R(h),\qquad
 L_R=\sum_i\operatorname{OPT}_{G}(S_i).
\]

Then

\[
 L_R\le\operatorname{OPT}_{G}(S)\le L_R+C_R.
\]

The minimum expected cost among trees extending that particular router is exactly `L_R+C_R`. Local optimum continuations can be chosen independently: there is no global budget on using a supplied query, and there is no requirement that a query occupy the same position in different branches.

**Proof.** Restrict a global optimal tree to each `S_i`. Suppression of constant nodes never increases a depth, so the sum of the restricted costs is at most the original raw cost. Conversely, attach an optimum identifying tree for `S_i` below every leaf of `R`; their raw costs add to `L_R`, in addition to the router's own cost. The same argument gives maximum-depth cost `max_i(d_R(S_i)+OPT_W(S_i))` for a fixed router.

If `k` distinct hypotheses are designated witnesses, their pairwise separation by the supplied tests gives a routing tree of height at most `k-1`, with exactly one witness in each leaf. Repeatedly choose a test separating two current witnesses. Both witness answer classes are nonempty and strictly smaller. Other hypotheses follow the same queries and are assigned to one of these leaves. Therefore `C_R <= (k-1)*Omega`.

**Quantitative rejection criterion.** If a candidate several-witness construction becomes independently easy after this router, and its independent cost `L_R/Omega` grows with the instance size, the cost of escaping global synchronization is an asymptotically negligible fraction:

\[
 \operatorname{OPT}_G(S)/L_R
 \le 1+(k-1)\Omega/L_R.
\]

For constant `k`, an intended gap of constant relative size cannot come solely from forcing the same assignment in these independently routable branches. Several witnesses can still help when the unresolved constraints remain together before separation, when the number of witnesses grows, or when the independently optimal residual states themselves retain a hard interaction. Those properties must be proved, not inferred from sharing query names.

### Explicit rational example

Put six points `(x,x^2)` at `x=1,2,3,5,6,7`, with weights `8,1,1,1,1,8`. Supply the five vertical cuts at `x=1.5,2.5,4,5.5,6.5`; multiply their equations by two to obtain integer coefficients. Every sign is strict.

The router at `x=4` separates two three-point branches. In the left branch the cheapest first query isolates its leftmost heavy point; in the right branch the cheapest first query isolates its rightmost heavy point. Their local raw costs are independently `12` each, so this legitimate routed tree costs `20+12+12=44`. Forcing the corresponding same-side choice in both branches costs `20+12+19=51`. The intended consistency rule is absent from the actual model.

An unrestricted tree improves further to raw cost `40`: isolate the heavy left point first, isolate the heavy right point second on the remaining branch, then identify the four light middle points in two threshold queries. Exact subset DP confirms optimum raw expected cost `40` and optimum height `3`. This example is illustrative; it does not purport to be a gap reduction.

## 3. Uniform caps of size at most two are exactly solvable without private singletons

This strengthens the previously known barrier, which assumed that every nonzero hypothesis had a supplied singleton cap.

**Theorem.** Consider any separating binary cap system on a distinguished all-miss hypothesis `0` and `N` other hypotheses. Every designated positive cap has size one or two and excludes `0`. Give every hypothesis weight one. Singleton tests need not be supplied for every hypothesis. Let `nu` be the maximum matching size in the graph formed by the supplied two-point caps. Then both objectives are exactly solvable by maximum matching, and their optima are

\[
 \operatorname{OPT}_G
 =\frac{N(N+3)}2-(N-1)\nu+\nu^2,
\]

\[
 \operatorname{OPT}_W=\max\{N-\nu,\nu+1\}.
\]

Expected depth is the raw formula divided by `N+1`. The theorem holds for abstract tests as well as for planar lines.

**Lower bound.** Follow `0` through any proper identifying tree. Each query's first-hit group is a singleton or a pair, and the groups partition the `N` other hypotheses. The pair groups are vertex-disjoint supplied edges, hence a matching of size `r<=nu`. There are `k=N-r` groups. A hit pair requires at least one more query to distinguish its two members. The raw cost is therefore at least

\[
 k+\sum_{j=1}^{k}j\,|A_j|+2r.
\]

Ordering the `r` mass-two groups before the mass-one groups minimizes this expression. The group completion sum is

\[
 \frac{k(k+1)+r(r+1)}2,
\]

giving `G(r)=N(N+3)/2-(N-1)r+r^2`. Its successive difference is `2r-N+2<=0` for feasible increments. The witness route has depth `k`, and the last of the `r` pair exits occurs no earlier than position `r`, giving height at least `max{k,r+1}`. This quantity also does not increase up to `r=nu`.

**Attainment without singletons.** A maximum matching is maximal. Query all its edges first. Each pair hit can be identified in one additional supplied query because separation of its two vertices is part of the instance assumption. On the all-miss route, all matched vertices have now disappeared. Every unmatched nonisolated vertex has a matched neighbor; querying their incident edge now hits exactly that unmatched vertex. An isolated vertex must have a supplied singleton, since otherwise its all-miss code would equal the witness's code. Thus all unmatched vertices can be queried individually after the matched edges. This realizes the lower bounds exactly.

This theorem rules out a broad family of uniform-prior consistency gadgets, including gadgets that try to recover hardness merely by deleting private singleton tests from two-cap instances. Larger caps, multiple witness sign patterns, or a fundamentally different continuation architecture are necessary for uniform hardness. It does not settle arbitrary-prior two-cap optimization: the desirable mass-sorted order may require a singleton before its matched neighbor has disappeared.

The planar pair graph has an additional geometric restriction: vertex-disjoint edge segments cannot cross. A halfplane containing one segment's endpoints and excluding the other segment's endpoints cannot separate two crossing segments. When all private singletons are supplied, all nonzero points are exposed, and the pair graph reduces further to paths or a cycle. These restrictions obstruct a direct import of an arbitrary bounded-degree constraint graph.

## 4. Gap accounting: choose a source whose promise is actually hard

The expected-depth target should be written with two source thresholds:

\[
 \nu_{\rm yes}\le\alpha M,\qquad
 \nu_{\rm no}\ge\beta M,\qquad \beta>\alpha.
\]

Seek a forward construction of cost at most `A+B*nu(x)` and, for **every** arbitrary adaptive output tree, a polynomial-time decoded assignment satisfying

\[
 \nu(x_T)\le\frac{G(T)-A}{B}.
\]

If `A<=cBM`, the resulting gap is at least

\[
 \frac{A+B\beta M}{A+B\alpha M}
 \ge1+\frac{\beta-\alpha}{c+\alpha}.
\]

A preferred normal form or an exact optimum cost identity is insufficient. The inverse inequality is the essential approximation-preserving obligation. In particular, unmatched interior positions, early private tests, and different choices in separate branches must all be accounted for by that inequality.

**Source correction.** MAX-2SAT cannot be used with an NP-hard perfect-completeness promise of zero violations versus `delta*M` violations: satisfiability of a 2CNF formula is polynomially decidable. A MAX-2SAT source must have a nonzero yes threshold. Alternatively, use gap-3SAT or an appropriate Label Cover promise with a genuinely valid perfect-completeness theorem. [Dinur's PCP paper](https://www.wisdom.weizmann.ac.il/~dinuri/mypapers/combpcp.pdf) supplies the general gap-amplification framework; a concrete bounded-occurrence restriction still needs the exact reduction and parameters intended for the gadget construction.

### Entropy makes constant-size local penalties too small under a uniform prior

With `N=Theta(M)` uniform hypotheses, every binary identifying tree has raw cost at least `N*log_2 N` by Kraft's inequality. If one violated constraint changes the cost by only `O(1)` and there are `Theta(M)` violations, the total extra cost is only `O(M)`, producing ratio `1+O(1/log M)`.

The same obstruction holds for a constant range of comparable per-constraint weights: the normalized hypothesis entropy is `Theta(log M)`. A constant-factor gap then needs each violated constraint to cause `Omega(log M)` extra depth on a comparable mass, or another penalty architecture whose total is comparable to the complete yes-instance cost. Appending identical logarithmic searches to every gadget does not help: it enlarges the baseline too. The extra work must occur selectively in no-instance trees and survive query promotion.

For maximum depth, penalties in different branches take a maximum rather than a sum. A gap-CSP promise with `delta*M` violated constraints is useless if each violation merely adds one query to a separate branch. Soundness must force many of the violations to serialize on one common route, or force one violated constraint to add a depth proportional to the whole yes depth.

## 5. Why modifying the current 3-Partition paths is not enough

The manuscript's maximum construction distinguishes `K` from `K+1`, where `K=q+m+2`. Its distinguished route forces intact clouds and maximum matchings only when it is exactly tight. A `(1+epsilon)` approximation may spend `Theta(epsilon*K)` extra queries there. Any new hardness proof must decode imperfect matchings and damaged clouds quantitatively.

The expected construction has a quadratic variance penalty of scale `V`, but its witness-plus-padding baseline is at least `V*r^3/2`. Increasing `V` multiplies both terms. Subtracting the baseline changes an exact decision threshold; it does not change a multiplicative approximation ratio.

There is also a source issue. Unrestricted assignments of independent jobs to identical bins with convex load objectives admit approximation schemes; [Alon, Azar, Woeginger, and Yadid](https://web.math.princeton.edu/~nalon/PDFS/aawy2.pdf) cover, in particular, sums of fixed powers. A 3-Partition exact-balance detector cannot be treated as an APX-hard source simply by replacing zero variance by positive variance.

The weighted path/cycle singleton-and-pair class already has a proved group-histogram QPTAS in the preceding reports. Direction 6 is investigating a stronger polynomial approximation scheme. Coupling choices while keeping exactly this cap class cannot yield a fixed-gap hardness reduction unless the algorithmic conclusion fails or the required complexity assumption is strengthened. Adding eligibility labels to unmatched path positions does not itself change the actual supplied-query optimization problem.

## 6. A viable next proof target: persistent constraints before mass release

The strongest remaining coupled-choice route is a shared live state in which variable choices affect many not-yet-exited constraint clients. The consistency must occur on that state, before clients can be routed into independently optimized branches. A useful next lemma would have the following form.

**Persistent-client extraction target, unproved.** Given any tree `T` for a realized gadget instance, select a set of common live states and decode one global source assignment. For every inconsistent or unsatisfied occurrence, charge either a distinct additional query on an identified surviving route, or a node mass not charged to any other occurrence. Prove

\[
 B\,\bigl(\nu(x_T)-\alpha M\bigr)
 \le G(T)-(A+B\alpha M),
\]

with `A<=cBM`, constants independent of the source size, and no subtraction of cost absent from the original objective. For maximum depth, the charged queries must all occur on a single route of the decoded tree.

The extraction statement should be designed before the numerical scales. It rejects both the premature-query shortcut and the branch-specific assignment shortcut. It also makes clear whether the true hard primitive is ordered cover, residual identification, or global adaptive synchronization.

Three concrete experiments can make progress toward it:

1. **Search for a persistent state with two genuine choices.** Enumerate small rational point sets and all their strict line cuts. Keep supplied subfamilies for which every near-optimal exact-DP tree leaves a substantial mass of designated constraint clients together after either choice. Test the competing root queries as well as the intended two queries. A good local optimum under a fixed root is insufficient.
2. **Search for selective long penalties.** For each candidate violated relation, find a family of clients that needs `Omega(log M)` additional useful supplied queries after *every* possible early test prefix of length `o(log M)`. The query-promotion lemma sets the minimum scale of this search. Check that satisfied clients have a materially shorter code with the same complete query supply.
3. **Couple before copying gadgets.** Test two adjacent occurrences together by exact subset DP before attempting a source graph embedding. Confirm that a near-optimal tree cannot choose their variable states independently. Only then seek a polynomial-size rational planar realization for a bounded-degree source.

The geometry must be audited on the complete instance. A halfplane that isolates a local cap may swallow remote gadgets, and a query intended for a remote gadget may provide a shortcut inside the current one. Planar sign matrices necessarily factor as

\[
 \operatorname{sign}(a_jx_i+b_jy_i+c_j),
\]

so their sign rank is at most three. That necessary condition is not a realization theorem for a proposed incidence table. Fixed query incidences can be checked by linear inequalities once coordinates are given; simultaneous choice of coordinates and lines is a much more constrained geometric problem. Every claimed catalogue should include its explicit rational coordinates, all query equations, all signs, and a bound on bit length.

A source graph that becomes a bounded-arity local planar CSP is also a poor default target: [Baker's planar decomposition technique](https://dl.acm.org/doi/10.1145/174644.174650) is a warning that local planar objectives often have approximation schemes. This observation does not by itself prove a scheme for the present tree objective, whose ordering costs are nonlocal. It means the source problem's gap must be checked after the geometric restrictions are imposed.

## 7. What is ready to use, and what remains open

- The query-promotion lemma and the independent-continuation sandwich are proved. They are useful as rigorous design constraints for new reductions.
- Uniform all-miss systems with cap size at most two are exactly solvable by maximum matching even without a full singleton supply. The proof applies beyond planar geometry.
- Constant-factor inapproximability for the full planar supplied-line model remains open in this investigation. No APX-hardness or uniform-prior NP-hardness is claimed.
- The best next coupled-gadget milestone is a persistent-client extraction lemma with a chargeable global assignment. A realized two-occurrence gadget surviving arbitrary root choices would be a meaningful first success.

Finite checks are in `direction5-gadget-checks.py`: 2,466 separating singleton/pair families matched the exact subset-DP formulas, 1,000 random trees satisfied the pointwise and weighted query-promotion bounds, and the rational six-point counterexample had exact raw expected optimum `40`. These are checks of the arguments, not replacements for their proofs.
