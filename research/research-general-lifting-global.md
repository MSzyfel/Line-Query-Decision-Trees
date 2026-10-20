# Global lifting: exact reachable palettes and a certificate-or-stage target

Auxiliary research note, 18 October 2026. The article is unchanged.

**Status.** No unrestricted approximation improvement is proved. Two concrete positive results are established: a logarithmic supplied query palette admits exact global adaptive pricing in polynomial time, and a certificate-or-stage condition implies a global contraction theorem with a single coding-resource ledger. The missing theorem is universal coverage of that condition by a polynomial source generator and polynomial lower certificates. Two explicit examples show why outside entropy and incumbent restriction credit cannot simply be substituted for one another.

## 1. Reoptimize a supplied palette instead of preserving one code order

Let `Q` be a supplied set of `d` original tests, with at most `K` responses per test. A context obtainable by asking tests in `Q` is specified by giving each test either one observed response or the status unasked. Thus there are at most

    (K+1)^d                                                   (1)

distinct nonempty contexts. Different specifications may give the same hypothesis subset and can be merged. A query already asked on a path is constant on its current context, so allowing every palette test at every state does not permit useful repetition.

Generate the closure of the ambient set under all palette outcomes. Order these actual subsets by size and optimize a Bellman recurrence. Every proper child is smaller. For weighted completion pricing at work price `lambda>=0`, use

    V(S)=max{ singleton_prize(S),
              max_(q in Q splitting S)
                  [sum_a V(S_a)-lambda |S|] },                (2)

where stopping gives zero on nonsingletons. This exactly maximizes completed prize minus `lambda` times raw work over **all** executable partial policies using only palette tests. It does not preserve the order of the source code from which `Q` was obtained.

For an actual incumbent `T`, write `F_T(S)` for its pruned raw cost on `S`. The recurrence

    J(S)=min{F_T(S),
             |S|+min_(q in Q splitting S) sum_a J(S_a)}         (3)

finds the exact cheapest complete tree that may adaptively use palette queries, then execute an actual incumbent restriction at every stopping exit. Reconstruction produces an executable full tree, not an abstract lower code.

With `d<=c log n` and fixed `c,K`, (1) is polynomial. Computing every terminal restriction cost by a scan of the incumbent adds a polynomial factor `n`. A polynomial list of such palettes is therefore polynomially searchable. The algorithm does not enumerate all `m^d` possible palettes; a separate source generator must supply the list. The source may have superconstant adaptive depth. Its number of distinct tests, rather than its height alone, controls (1).

For a code on a subset, its directly lifted query sequence and every pruning of it are included in (2). Equation (3) also dominates its actual-incumbent collision completion. This is a strict extension of fixed-template prefix mining.

### Public integration API

`research-general-lifting-global.py` exports

    optimize_palette(instance, incumbent, tuple_of_test_indices)
        -> (actual_complete_tree, stats)

and

    price_palette(instance, tuple_of_test_indices, weights,
                  work_price=1, ambient=None)
        -> (actual_partial_tree, stats).

The first uses `incumbent.state` as its ambient set. The binary implementation uses the existing duck-type fields `state,test,left,right,cost` and `instance.branch`. Prize mappings use singleton **bit masks** as keys, matching the previous pricing implementations; sequences may instead be indexed by hypothesis number. Complete-tree statistics contain ordinary integers. Restriction evaluation and reconstruction are iterative and permit a deep incumbent comb. The fixed-response theorem is (1)-(3); the current implementation is binary.

## 2. Reordering can improve every fixed-template prefix by a logarithmic factor

Let a core contain `C=2^D` binary strings and use its coordinate code in order `1,...,D`. Add `u=C^2` outsiders, all answering zero on these `D` queries. Append outsider singleton tests to the original test family so the whole instance is separable; they are not in the palette.

Give one clean core string `h*=(0,...,0,1)` prize `u+D`, all other core strings except the all-zero string prize `D`, and the all-zero core string prize `u+D` as well. Outsiders can have any nonnegative prizes, since no palette policy identifies them. These core prizes are the exact depths of a legal incumbent: query the first `D-1` coordinates, finish the ordinary two-leaf cells, and on the all-zero prefix query all outsider singletons before the final coordinate. Outsider depths can be assigned their actual depths in that incumbent. Every prize is at most `n-1`, where `n=C+u`.

Any prefix of the supplied coordinate-order template that completes `h*` asks all `D` queries on all outsiders. Its work is at least `uD`, while its total possible completed prize is at most `u+(C-1)D`. Any nonempty prefix omitting `h*` has work at least `n` and prize at most `(C-2)D`. Thus its minimum work/prize ratio is at least

    min{uD/[u+(C-1)D], n/[(C-2)D]} = Omega(D).                (4)

The same palette can ask coordinate `D` first, stop its outsider-containing branch, and verify `h*` in the clean branch. Its work is less than `u+2C`, with prize at least `u+D`, giving ratio less than `1+2/C`. Since `D=Theta(log n)`, palette reordering can improve the strongest fixed-template prefix density by `Theta(log n)`.

This example concerns the pricing primitive, not the approximation ratio of the complete global generator. The source library may contain other useful code orders; no lower bound on that larger generator follows.

## 3. One globally shared coding resource

For the following theorem, let `B(s)` be a nonnegative superadditive resource on cardinalities, with `B(0)=B(1)=0` and

    B(n)<=F_OPT(H).

The uniform unrestricted `K`-ary coding cost `L_K(s)` is a valid choice. Restricting its optimal code proves superadditivity; the coding lower bound proves `L_K(n)<=F_OPT(H)`. Its Bellman recurrence also gives a query drop between zero and `s`. For binary codes,

    L_2(s)=s(ceil(log2 s)+1)-2^ceil(log2 s),  s>=2.            (5)

All values in (5) are integers. This avoids numerical entropy comparisons and cardinality floors. More generally, the contraction theorem below only needs the stated nonnegative, superadditive, globally bounded resource properties.

Fix an incumbent `T` for an entire pass. At a real current context `S`, let a proper executable partial stage `P` have output cells `A`. Its actual restriction credit and resource drop are

    Gamma_T(P)=F_T(S)-sum_A F_T(A),
    Delta_B(P)=B(|S|)-sum_A B(|A|).

Both are nonnegative. Every cost and credit refers to the actual current context; no outside population or unfinished resource is reset.

**Conditional global contraction theorem.** Fix constants `0<=gamma<1`, `a>=0`, and `alpha>=1`. Suppose a polynomial procedure, at every actual context `S`, does one of the following:

1. It supplies a valid certificate `F_T(S)<=alpha F_OPT(S)`, and executes `T` pruned to `S`.
2. It supplies an executable proper stage satisfying

       W(P)<=gamma Gamma_T(P)+a Delta_B(P),                 (6)

   and recurses on its actual output cells.

Then the resulting actual complete tree `T_new` satisfies

    F(T_new)<=gamma F(T)
               +[a+(1-gamma)alpha] F_OPT(H).                 (7)

To prove this, let `Z` be the terminal cells handled by certificates. Proper refinement makes them a partition. The actual credits telescope to

    sum_stages Gamma_T = F_T(H)-sum_(A in Z) F_T(A).

The resource drops telescope to `B(n)-sum_(A in Z)B(|A|)<=B(n)<=F_OPT(H)`. Adding the terminal actual costs to (6) gives

    F(T_new)<=gamma F_T(H)+a F_OPT(H)
                         +(1-gamma) sum_(A in Z)F_T(A).

Finally use the terminal certificates and `sum_Z F_OPT(A)<=F_OPT(H)`, which follows by restricting one global optimal tree to the disjoint terminal cells. This proves (7).

Repeatedly construct this tree and accept only strict integer cost decreases. If the certificate-or-stage condition is universally available, a nonimproving incumbent has approximation ratio at most

    alpha+a/(1-gamma).                                      (8)

Indeed (7) would force a strict improvement above (8). A proper unit-cost identifying tree has raw cost at most `n(n-1)`, so there are polynomially many accepted decreases. Each pass has polynomially many stages because every stage makes a proper refinement in the final identifying tree. This is a sufficient algorithm theorem, **conditional on universal certificate-or-stage coverage**. No such coverage is proved here.

## 4. Exact palette pricing of the mixed stage condition

For a supplied palette, set terminal energy

    Phi_T(S)=gamma F_T(S)+a L_2(|S|).

Replace the stopping term `F_T(S)` in (3) by `Phi_T(S)`. The difference between root energy and the minimum objective is exactly

    max_P {gamma Gamma_T(P)+a Delta_L(P)-W(P)}.               (9)

This follows by summing the terminal energies over the actual output cells. The recurrence is exact over every adaptive palette policy. It reconstructs a legal stage whenever its value is positive; equality candidates can also be evaluated explicitly. All comparisons are rational when `gamma,a` are rational.

The implementation exports

    price_palette_stage(instance, incumbent, palette,
                        gamma=1/2, coding_price=1)
        -> (actual_partial_tree, stats).

This makes the stage side of the conditional theorem executable for a polynomial palette library. Existing entropy, cap-size, represented-flat, or endpoint-pair certificates can provide some terminal certificates. The unresolved assertion is that these two polynomial mechanisms cover every remaining state with constants or any better asymptotic target.

## 5. Output entropy does not lower-bound actual incumbent credit

Let `H={0,1}^D` and let `T` be the optimal fixed-order coordinate tree. Add a test `q` equal to its first coordinate, except flip one leaf in each of the root's two halves. The test remains balanced and has output entropy one bit, or `n` raw bits.

Both test colors occur in both root children, so the root contributes zero to the restriction credit. Within either half, one exceptional leaf has a different color from all others. In a balanced binary tree of depth `D-1`, separating that leaf saves two units at its parent and one at each of its other `D-2` ancestors, for exactly `D` units. Consequently

    Gamma_T(q)=2D,
    raw output entropy(q)=n.                                (10)

The ratio is unbounded. Thus paying outside routing entropy from actual incumbent restriction decrease alone is invalid, even when the incumbent is optimal. The shared coding-resource term in (6) is separate from this actual credit and telescopes independently. Equation (10) does not obstruct that mixed accounting.

## 6. Independent outside entropies cannot simply be summed over cores

Take `H=[k] times {0,1}^D` with `k` a power of two. Supply group-coordinate tests and word-coordinate tests. The optimum is exactly

    n(log2 k+D)

by entropy and the matching coordinate code. For each group `i`, let `C_i` contain its `2^D` word hypotheses and let its supplied code use the global word-coordinate tests. Every outsider distribution is uniform over all `2^D` core outputs, so its routing entropy is `D`. Summing independent outside entropy charges over this optimal frontier gives

    sum_i (n-|C_i|) H_i = (k-1)nD.                          (11)

This can exceed OPT by an arbitrarily large factor. The physical word queries in these codes are identical, and one actual global execution followed by group queries is optimal. Equation (11) is an obstruction to resetting a separate outside-entropy ledger at every core; it is not a lower bound on the source generator. Palette contexts retain shared answers, so they do not make this reset.

## 7. Scope of the cardinality-profile extension

The root's parallel LP permits arbitrary nonnegative cardinality profiles on nodes of one hierarchy, rather than only weighted restriction features. The same count DP separates that cone even if individual local deficits are negative. Its root-only specialization still has the affine equality gap.

Indeed, if every supplied test has exactly `n/Q` positives, a root cardinality profile `g(s)` must satisfy

    g(a+b)<=a+b+g(a)+g(b)
       whenever a<=n/Q and b<=n-n/Q.

The all-subset constraints permit peeling blocks of `n/Q` until none remain, then balanced abstract coding inside each block. Thus

    g(n)<= (n/Q)[Q(Q+1)/2-1]+n ceil(log2(n/Q))
         =O(nQ+n log n).                                   (12)

On the documented hard affine regime `log n=Theta(Q)`, this is `O(nQ)`, while OPT is `Theta(nQd)`. Equation (12) concerns the root-only profile, not the sum over a supplied laminar hierarchy. No full-hierarchy expressiveness gap is proved here. The exact coding potential in (5) repairs the earlier plain-cube obstruction but does not by itself repair (12).

## 8. Verification and remaining obligation

The companion checker passed 144 exact complete palette/fallback comparisons and 144 rational weighted partial-pricing comparisons against an independent recursive optimizer. It checks actual per-hypothesis execution, the `3^d` context bound, 144 reconstructed mixed-stage identities, the coding-resource query inequalities, the ordering-gap examples through `n=16512`, and (10) through `n=512`.

The sample-based palette generator is developed separately by the root. Selecting only logarithmically many distinct queries from each supplied sample code makes exact global reoptimization polynomial; it does not prove that the selected palettes cover the stage side of (6). A proof of that coverage together with polynomial terminal certificates, or a full-order adversarial obstruction to it, is the next concrete global question.
