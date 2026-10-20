# Independent audit of uniform hardness and the new polynomial expected-depth factor

I independently reviewed `next-hardness.md`, `next-hardness-check.py`, `next-expected.md`, and `next-expected-check.py`, and checked the relevant exact-invoice and scale calculations in Section 8 of the manuscript. Both new results pass the audit. No shared TeX file was edited.

The conclusions are:

* Uniform expected-depth optimization is strongly NP-complete on the explicitly constructed supplied-line parabola instances, assuming the manuscript's established restricted 3-Partition reduction.
* The shrinking-factor barriers stated in `next-hardness.md` follow from the global reduction gaps and the improved output-size bounds. They do not establish APX hardness.
* The changed-first-batch and merged-batch polynomial algorithm has general expected-depth approximation factor **strictly below 5.197569**, for arbitrary positive rational priors.

## 1. Private-singleton exchange and cloud normalization

The singleton rotation is legal. Suppose the current first query isolates `x`; its other child begins with a proper query having nonempty classes `A,B`, and `x` would answer on the `A` side. Move that query first, then isolate `x` within its `A` child. The original subtrees on `A` and `B` remain valid without modification. Exactly `x` gains one depth unit, every member of `B` loses one, and all other depths remain unchanged. The raw uniform cost difference is `1-|B|<=0`.

The rotation requires uniform weights. It is correctly applied to the replicated cloud instance, rather than to its unequally weighted compressed instance.

The normalization process terminates. If an external private point remains on the distinguished cloud-0 anchor path, its own anchor also remains on that path: a private query never removes an anchor, and any earlier whole-cloud query removing that anchor would have removed the point too. Those two anchors must eventually be separated by a whole-cloud query, because all private queries give the same answer on both. Pushing the private query downward until that separation moves it into an off-spine branch. This removes one external private query from the distinguished path and does not introduce another there. Repetition removes all external private queries. Cloud-0 private queries can then be pushed through all remaining whole-cloud queries without changing the latter's path, so they occur last.

Consequently every first-hit whole-cloud exit contains one intact cloud or two intact adjacent clouds. A pair query first hitting only one previously unhit cloud can be replaced by its supplied singleton-cloud query on the current state. The two-cloud groups are disjoint and form a matching. There is no assumption here that private queries were absent from an initially optimal tree; the rotations prove that an optimal normalized tree exists.

## 2. Exact local and global costs

On a cloud of size `w`, every proper query isolates one available nonanchor. Its raw uniform chain cost is exactly

```
D(w)=(w-1)(w+2)/2.
```

On two clouds of sizes `u,v`, a supplied whole-cloud split costs

```
f(u,v)=D(u)+D(v)+u+v.
```

If a private point of the first cloud is asked instead, induction gives `u+v+f(u-1,v)`, whose excess above that split cost is `v-1>=0`. The corresponding excess for a private query in the second cloud is `u-1>=0`. The remaining subcloud still has its anchor and private queries for all its other remaining points, so induction depends only on its size; it does not require consecutive surviving positions. Every other whole-cloud query is either constant or splits the two clouds. The base cases, including a singleton cloud with no private query, are correct.

After normalization, cloud 0 contributes its weight times the whole-cloud spine length. Every first-hit group contributes its total size times its first-cover rank, every paired exit has the additional pair-size split cost, and every cloud contributes its own fixed `D(w_i)`. Sorting the disjoint groups by decreasing mass minimizes the rank sum. This is exactly the compressed weighted matching invoice plus

```
D_total=sum_i D(w_i).
```

The proposed construction attains that lower bound for every matching. Thus `OPT_cloud=OPT_weighted+D_total` holds for every positive integer weight vector, without requiring a dominant cloud-0 weight. Dominance is used separately in the hardness construction to force maximum matchings in the weighted optimum.

## 3. Geometric realization and strong NP-completeness

The whole-cloud query polynomial factors on the parabola as

```
4(x-Q(a-1/2))(x-Q(b+1/2)).
```

With `Q=4 max_i w_i`, it selects precisely clouds `a,...,b`, including the supplied singleton and adjacent-pair cases. Neighboring clouds cannot reach either root. The private query evaluates to `2(x-t)^2-1`, which is negative precisely at its target integer abscissa and never zero. Anchors receive no private query.

There are `n=sum_i w_i` points and `O(n)` queries. Because `Q=O(n)` and the number of clouds is at most `n`, abscissae are `O(n^2)` and ordinates and integer line coefficients are `O(n^4)`. All signs are strict and all points remain in strictly convex position on the parabola.

The manuscript's weighted reduction uses positive integers bounded by a fixed polynomial in its output's number of weighted vertices. Replication is therefore polynomial on the strongly restricted source family. Adding `D_total` to the raw threshold and dividing by the output population gives exact yes/no equivalence. A proper identifying tree has `n-1` internal nodes and polynomial certificate size. These observations justify strong NP-completeness of uniform expected depth in the stated geometric model.

Raw uniform cost is integral and bounded by `n(n-1)` for a proper tree. An FPTAS run with `epsilon=1/(2n(n-1))` would recover the exact optimum after removing constant queries. This rules out a uniform expected-depth FPTAS unless `P=NP`. Adding the fixed cloud cost preserves approximation schemes inherited from the compressed forest family, so this construction does not produce a fixed-factor gap or preclude a PTAS.

## 4. Global gaps and output-size bounds

The arbitrary-prior expected-depth NO gap is a bound on the global optimum. The dominant distinguished weight forces maximum matchings. For a boundary matching, the manuscript's quadratic identity and error bounds give a gap at least `V-E_--E_+ >= (1997/2000)V` above the threshold. For an internal unmatched choice, its Step 7 lower bound has excess greater than

```
[r/3-(p+8)(q+m+1)^2]V > V.
```

Thus restricting the gap calculation to boundary choices does not omit a cheaper internal optimum.

The population estimates use the manuscript's explicit item weights, not merely an asymptotic statement. Each item vertex has weight at most `(10+2p)V`; hence `P<=4(q+m)(p+10)V<rV/250`, so `W=P+rV/2<rV`. This yields `Omega<=n_0^2 V`. A feasible boundary code and the bounded errors give `k<n_0^3 V`. Therefore the final strengthened factor `1+9/(10n_0^3)` returns a YES cost below `k+(9/10)V`, whereas every NO cost is at least `k+(1997/2000)V`.

For the uniform replication, `n=Omega`. The explicit `r` ensures `N+2<=2r`, and `V>=2000r`, giving

```
n <= 2r^2 V+1 <=3r^2 V <=3V^3/4,000,000 <V^3/110^3.
```

Here `3*110^3=3,993,000<4,000,000`, so `V>=110n^(1/3)`. The lifted feasible boundary code has raw cost at most `n(n-1)`. Since `n>=V` and the total error is less than `(3/2000)V`, its shifted threshold satisfies `K'=k+D_total<n^2`. Consequently the final strengthened factor `1+100/n^(5/3)` returns a YES cost below `K'+100n^(1/3)<=K'+(10/11)V`. The exact transfer preserves the larger NO gap. A rational threshold strictly between these bounds separates the cases; no irrational root computation is needed by the reduction.

For maximum depth, the construction contains `u` high clouds of size `H=u+M`, so `n>=u(u+M)`. Its explicit parameters satisfy `q<=3u` and `0<M<=u`. The identity `(3u+M)^2-9u(u+M)=M(M-3u)<0` gives `K=q+M<3sqrt(n)`. The final strengthened factor `1+1/(3sqrt(n))` gives a YES height strictly below `K+1`, and integrality reduces this to height at most `K`. Every NO instance has height at least `K+1`. The strengthened maximum-depth shrinking-factor barrier follows.

All three hardness factors tend to one. The reports correctly distinguish these results from constant-factor inapproximability.

## 5. Changed first batches and merged batches

The new expected-depth candidate family uses either `q,k_1,k_2,...` with fixed `q<=6` and `q<k_1`, or `k_1,k_2,...` after merging the old first two batches. These are increasing integer-budget schedules. At each phase the exact at-most-budget coverage set is processed greedily by newly hit mass, with unproductive blocks omitted. Nonincreasing within-phase greedy scores justify the same phase upper-bound argument as before, independently of a geometric first budget.

The two signed doubled phase corrections are exactly

```
d_q=k_0-q+(k_0+k_1)1[t>k_0]-(q+k_1)1[t>q],
d_merge=k_0-k_1+(k_0+k_1)1[t>k_0].
```

They retain delays as well as accelerations. If the first budget already reaches minimum cover size, the actual phase is shorter; the nonnegative extended residual accounting remains an upper bound.

The corresponding full negative-route length changes are correctly charged as

```
z_q=q1[q<k_min]-k_01[k_0<k_min],
z_merge=-k_01[k_0<k_min].
```

In particular, the positive first-hit correction is not incorrectly substituted for the zero waiting cost. The exact certificate proves their distributional average is nonpositive for `k_min=1,...,7`; it is constant thereafter because all changed ordinary initial budgets are at most six and `k_0<=3`. This preserves the earlier zero-route mean length bound for every instance.

Each variant's first phase covers mass at least `M_q` and uses at most `q` productive blocks. The accepted rational block discount therefore gives either `M_q-delta w q`, `cM_q-d delta w q`, or zero as a bound on the same complete saving. Every row of the eight-row proof table is a convex distribution over actual available variants and valid minorants. For the two merged rows `k_1` is respectively three and four. Rows spanning changing `k_1` use an unchanged initial budget and have zero phase correction. No prefix or phase saving is counted twice.

A minor wording issue in the initial report was reported to the root agent: the original variant satisfies `k_0<k_1`, with `k_0<=3` and `k_1>=3`; the stronger phrase `k_0<=3<k_1` fails when `k_1=3`. The algorithm, proof table, and certificate already use the correct condition.

## 6. Infinite-rank tail, information accounting, and final factor

The finite certificate compares all exceptional ranks one through seven. Only `a_1` is below `tau=2.0718779`; its mass is at most `2delta w`. Every saving cutoff is at most six and every phase correction becomes constant by rank seven, so the accepted monotonicity of the old discrete discount handles the entire infinite tail. The exact zero-credit condition `chi+2/ln(beta)>tau` pays the conversion from total-state mass to positive mass.

The optional query-both mode and virtual-transcript entropy accounting are unchanged from the previously independently audited theorem. Changing the schedule does not change the cap bound on each virtual positive exit. The exact rational objective prices actual mode discounts and negative-route length together. Its minimum is at most the fixed shift/variant distribution used by the proof. The balanced-state argument, supporting-prefix restriction credit, and pattern recursion therefore give the asserted general potential bound.

The default exact logarithm certificate reports

```
A = 3.591810178840039
B = 4.445350596843871
chi = 1.1285791015302313
ratio upper < 5.197568047723 < 5.197569.
```

The test certifies all strict coefficient comparisons, the waiting changes, the accepted rational entropy tent, and the final upper bound using rational logarithm enclosures. Its floating-point exploratory optimizer is separate. There are at most seven candidates per geometric shift region and polynomially many regions and coverage budgets. Every algorithmic objective comparison is rational. No minimum-prior cutoff, logarithmic rank-subset program, or quasipolynomial subroutine enters this expected-depth algorithm.

## 7. Independent counterexample search and finite transfer tests

I added the separate `next-results-audit-check.py`. Its weighted and cloud costs use full adaptive Bellman recurrences, rather than assuming a matching or normalized spine. It compares the compressed Bellman optimum with an independently enumerated matching invoice, then compares the full uniform-cloud optimum with that value plus the cloud constant. The cases include weights up to five and up to six nonzero vertices, with total cloud population capped at sixteen for complete enumeration. It also evaluates every supplied geometric sign in those instances and checks sampled singleton rotations algebraically.

For the reduction scale checks, the script constructs forty nonuniform item sets satisfying the restricted 3-Partition bounds, evaluates the actual path weights, boundary invoice, decision threshold, cloud constant, population, and gaps, and verifies every quantitative inequality used above.

For the approximation audit, it generates actual weighted circular positive intervals on four through nine vertices, enumerates all block subsets for an independent exact coverage oracle, and reconstructs every relevant shifted schedule and variant. It checks actual newly covered `x,y,z`, rational mode credit, actual-versus-virtual entropy identities, first-phase transfers, signed phase identities, early completion, and full waiting-route length. Integrating all rational shift regions checks the final averaged surrogate against independent comparison orders.

Running `python next-results-audit-check.py` passed:

* 100 full adaptive weighted/cloud Bellman and geometry comparisons;
* 84,098 singleton-exchange checks;
* 40 nonuniform complete reduction parameter constructions;
* 120 actual changed-batch circles, with 1,560 prefix transfers, 1,560 phase identities, and 1,560 shift/variant schedules.

The discrete checks use exact integers or fractions. The supplementary entropy identities and log-uniform averages use floating-point tolerances; the separate theorem certificate supplies rigorous logarithm bounds for the final constant. The author's default scripts also pass their 383 cloud comparisons, 380 W parameter tests, 42 E parameter tests, exact approximation certificate, and 1,950 modified-batch comparison tests.

These finite searches found no counterexample. The normalization, transfer, quantitative reduction, and approximation claims are justified by the proof arguments above, rather than by enumeration alone.

## 8. Final manuscript integration review

I compared `sections/06f-first-phase-improvement.tex` and `sections/08a-uniform-hardness.tex` with the audited reports, and checked the algorithm recipes, abstract, introduction, conclusion, and boundary corollary. The new theorem, certificate values, convex mixtures, mode credit, cloud theorem, and geometric construction are transcribed consistently. All cloud statements and their pseudocode specify a linear forest with components ordered along their paths; no arbitrary pair graph is implicitly claimed.

The initial-family pseudocode uses `j_0=1` for ordinary variants and `j_0=2` for the merged variant. It processes `Q_*` and finishes whenever any budget, including the first, reaches the minimum cover size. It therefore handles early completion without attempting to access an undefined `Q_q`. The explicit source text now correctly uses `k_0<k_1`.

The previous breakpoint family suffices for the new variants. If `q<k_min`, its availability condition changes only at an existing rank-one geometric breakpoint `(q+1)/beta`, since `q+1<=k_min`. If `q>=k_min`, its first batch is `Q_*`; any additional availability change merely introduces the same complete-cover schedule already supplied by the merged variant. Thus no unenumerated change removes a distinct relevant schedule.

The summary constants agree with the theorem: binary expected depth below `5.197569`, on-line expected depth below `10.395138`, binary maximum depth at most `4.46496526`, and on-line maximum depth at most `8.92993052`. The boundary corollary cites the new expected-depth theorem. Older constants appear only as historical intermediate theorems or explanatory steps.

The active-source cross-reference scan covered nineteen files and found 166 unique labels and 125 distinct referenced labels, with no duplicate labels or missing references. The current compilation log contains no warnings, undefined references, overfull/underfull boxes, or TeX errors.

The root subsequently sharpened the three inapproximability constants to `1+1/(3sqrt(n))`, `1+9/(10n^3)`, and `1+100/n^(5/3)`. Section 4 above records the independently verified strengthened algebra. These changes preserve the exponents, geometric scope, and shrinking-gap limitation. The independent quantitative script now additionally checks the strict W square-root inequality, the `110` cube constant, and both expected-depth margins.

I also read the subsequently updated hardness theorem and proof in `08a`, and its updated introduction and conclusion statements. All three strengthened constants and their rational separating thresholds are transcribed correctly. The forty nonuniform quantitative constructions pass the additional strengthened assertions.
