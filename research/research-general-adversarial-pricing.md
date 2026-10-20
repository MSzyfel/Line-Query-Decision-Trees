# Adversarial tests of complete-code pricing and state reuse

Auxiliary research notes, 2026-10-18. The article is unchanged.

The unrestricted polynomial approximation target remains open. This note
records adversarial search against actual executable synthesis policies,
explicit counterexamples to overly strong local-stability claims, and a
more expressive polynomial candidate. Exact exponential Bellman solvers
are used only to validate small instances; they are never inputs to the
candidate algorithm.

## 1. Candidate and adversarial objective

The initial candidate is the implemented algorithm from
`research-general-algorithm-next.py`: retain fresh one-step greedy
continuation codes at incumbent nodes, add a verification-first full code
for every hypothesis, close code-node states under pairwise intersections,
and solve the exact incumbent-depth prize-minus-work recurrence on that
represented DAG. Splice positive-profit fragments into the incumbent and
repeat strict integer descent.

The adversary's fitness is the **final complete output cost divided by
the exact optimal cost**, not greedy's cost or a shallow surrogate.
Test order is retained because it affects deterministic ties.

The search mutates response-table entries, correlated rectangles, whole
hypothesis response words, query order, whole test supports, and AND/XOR
combinations of supports. It can add and delete queries while preserving
pairwise separation. Seeds include the earlier failure, biased response
codes, graph-incidence families, and two-fibre activation products. An
annealed walk and an elite archive permit neutral and temporarily worse
mutations. All seeds and ordered test masks are saved.

The implementation is
[research-general-adversarial-pricing.py](research-general-adversarial-pricing.py).
The search is an experiment, not part of the polynomial approximation
algorithm. No bound on adversarial-search success is claimed.

## 2. New failures of quadratic plus verification synthesis

Positive masks below use bit `h` for hypothesis `h`, starting at zero.

| Hypotheses | Ordered positive test masks | Greedy | Final output | OPT | Ratio |
|---:|---|---:|---:|---:|---:|
| 12 | `3264,700,1153,8,1042,97,3840,1022` | 48 | 47 | 45 | 1.04444 |
| 14 | `536,5860,6400,10368,2061,1027,90,6055` | 61 | 60 | 57 | 1.05263 |
| 16 | `20736,57344,56032,17588,18624,16772,40448,1234,7735` | 66 | 66 | 65 | 1.01538 |
| 18 | `536,203199,44160,88107,228858,41456,514,206464,261742` | 87 | 85 | 80 | 1.06250 |

The full matrices and iteration traces are in
`research-general-adversarial-n12.json`, `research-general-adversarial-n14.json`,
`research-general-adversarial-n16.json`, and
`research-general-adversarial-n18.json`.

Search sizes were 30,000 proposals at `n=12`, 15,000 at `n=14`, 1,500 at
`n=16`, and 30,000 at `n=18`. Valid distinct evaluations were respectively
16,710, 9,424, 993, and 18,799 for the recorded runs. These are finite
experiments, not an asymptotic lower-bound family.

### What actually prevents improvement?

I reconstructed one exact optimal comparison tree and inspected its
missing candidate states against the final represented family.

- The `n=12` failure misses masks `140` and `12`, of sizes three and two.
- The `n=14` failure misses mask `676`, of size four.
- The `n=16` failure misses mask `36`, a pair.
- The `n=18` failure misses masks `22538,22530,6146,96`, of sizes five,
  four, three, and two.

Every listed missing state needs **three** intersections of existing base
code-node states; two do not suffice. Exact unrestricted prize-minus-work
separation, used only for diagnosis, finds profits two, three, one, and
five respectively, while the represented separator reports zero at the
final incumbent. Thus the failed condition is legal-history/state
coverage, not an arithmetic error in pricing or a failure to run integer
descent to completion.

This does not prove every optimum needs those particular states. The
strict output gaps are established independently by the exact cost
oracle, while the missing-state list explains one optimal witness.

## 3. Exact small tails and an expressivity invariant

A cheap repair is to add **every hypothesis subset of size at most three**
to the represented family. The original tests separate every such subset,
and its proper child subsets are also represented, so exact local code
tables and prize-work optimization are available in polynomial time.

This has a useful invariant that explains the near-optimal behavior of
small random tests:

**Proved expressivity fact.** The base family contains every nonempty
single-test outcome on the full hypothesis set. Its quadratic closure
therefore contains every state reached by at most two tests. After adding
all subsets of size at most `k`, the family contains every node of any
complete tree whose depth-three frontier sets all have size at most `k`.
If one optimum has that property, exact supported-state optimization
recovers the global optimum.

**Proof.** States at depths zero, one, and two are intersections of at most
two raw test outcomes and hence represented. States at depth three are
the small frontier sets, and every descendant is a subset of one of
them, so has size at most `k` and is also represented. All edges of that
complete comparison tree are supported.

This is a restricted expressivity guarantee, not an approximation theorem
for general instances. In particular, it cautions against reading tiny
balanced-instance success rates as evidence of a global bound.

## 4. Conditional code generation from incumbent-depth prizes

At every incumbent node and every forced root test, also generate greedy
continuations using the following artificial split weights:

1. The current full-tree leaf depth `d_T(h)`.
2. Its square.
3. `1+n * indicator[d_T(h)>=median depth]`.

These weights guide code construction only. Actual query work and the
pricing recurrence still use uniform hypotheses and unit costs. Generated
codes use original supplied queries, and every stored state belongs to a
complete legal code.

This constant menu repairs all four failures in Section 2. It is still
incomplete, even when all subsets of size at most three are included.
Adversarial optimization against this stronger actual output found:

```
n = 18
tests = [592,211391,44160,88107,228858,33264,514,206464,259695,9772]
greedy cost = 82
quadratic + verification output = 81
depth/squared-depth/median-prize templates + small tails output = 81
exact OPT = 79.
```

The omitted optimal state is mask `200707`, namely hypotheses
`{0,1,12,16,17}`. It has size five and needs three base intersections.
Unrestricted prize-work profit is two; represented profit is zero.
The run used 10,000 proposals and 6,978 distinct valid evaluations. See
`research-general-adversarial-enriched-n18.json`; the independently
re-diagnosed witness is also saved in the corresponding `-interim.json`.

### All depth levels are affordable and can matter

Instead of choosing only one high-depth threshold, generate weighted
greedy codes for **every distinct incumbent depth**. There are at most
`n-1` levels, so this adds a polynomial factor without a growing exponent
or a growing query horizon.

On the preceding witness, this changes cost `81 -> 80 -> 79`. The first
profitable level is depth at least five, targeting six hypotheses
`{0,1,11,12,16,17}`. Merely targeting the deepest pair `{1,12}` or the
three hypotheses at depth at least six is not profitable in isolation.
This provides a concrete reason to retain moderately deep coalitions,
rather than concentrating only on the few deepest hypotheses.

The exact per-level diagnostic is reproducible with

```
python research-general-adversarial-pricing.py --threshold-input research-general-adversarial-enriched-n18-interim.json
```

There is no proof that all depth levels suffice in general.

## 5. Combined polynomial candidate

The next candidate combines all depth-threshold templates and exact small
tails with the other branch's target-incident pair templates and ordered
two-target verification compositions, implemented in
`research-general-pricing-oracle.py`.

An ordered two-target composition executes the first target's verification
spine, preserves every resulting exit, and then executes the second
target's spine only in its current unfinished cell. All unresolved exits
are filled with fresh greedy. It creates contexts that are absent from
the union of separate single-target spines. The other branch checked
that this repairs all four Section 2 failures and the stronger `81/79`
failure above.

In every improvement pass the combined candidate:

1. Adds target-incident codes for incumbent states, test outcomes, and
   depth-level target regions.
2. Retains all static ordered two-target verification codes.
3. Generates the forced-root conditional uniform and depth-weighted codes.
4. Closes their node states under **two** intersections and adds all
   subsets of size at most three.
5. Performs exact depth-prize profit separation, splices a positive
   fragment, and repeats strict integer descent.

All represented states and complete codes are retained. Coalition width
is fixed at two, tail size at three, and intersection arity at two.
Depth levels may grow in number, but are enumerated as a polynomial list
of generators. There are at most `n(n-1)` successful passes.

A conservative base-family bound is `O(n^5 m)`: there are at most `n`
incumbent nodes, `m` forced tests, `O(n)` weighted generators, and `O(n)`
nodes per generated code in each of at most `n^2` passes. Static
two-target codes and target-incident templates are smaller terms. Hence
the quadratic family has `O(n^10 m^2)` states, and a loose total runtime
bound, including `n`-bit scans, is

```
O(n^13 m^3 polylog(nm)).
```

This is a fixed-exponent polynomial candidate, not a proved improved
approximation. The exponent is deliberately conservative, and the bound
does not suggest practical scalability to large matrices.

## 6. Actual restriction credits and implicit boundary queries

The depth-prize test counts only completed hypotheses. Actual incumbent
restriction can also save work on unfinished output cells. The following
stronger polynomial synthesis step prices those savings exactly.

For the incumbent `T`, define

```
V_T(S) = raw cost of T restricted to S, suppressing constant queries.
```

It is computed directly from incumbent nodes:

```
V_T(S) = sum_(internal v of T) |S intersect S_v| * indicator[
             S intersects both children of v].
```

On a represented family `Q`, evaluate in increasing set size:

```
J(S) = min{ V_T(S),
            |S| + min_(supplied splitting tau) sum_a B(S_a) },

B(A) = J(A)     if A is represented,
       V_T(A)   otherwise.
```

The minimum ranges over **all** splitting tests, even when their outcomes
are absent from `Q`. An absent child is a terminal macro executing the
actual incumbent restricted to that child. It is never expanded again
during the pass. The stop choice at any represented node is also an
actual incumbent restriction, not an optimistic assigned cost.

**Proved finite-family guarantee.** This recurrence computes exactly the
minimum actual cost of a partial policy which uses represented states
for continued optimization, may make one final query into unrepresented
children, and completes every stopping cell by the incumbent restriction.

The proof is the root decomposition of its explicit legal policy space.
Children decrease in size, so the recurrence is acyclic. Store decisions
and reconstruct the complete actual tree. All fallback leaves identify
their hypotheses and all queries are supplied. At most `n-1` internal
nodes survive in the output.

For the same incumbent and represented family it is never worse than the
supported-state-only fallback recurrence, or the former depth-prize
fragment followed by incumbent fallback. This is a per-pass statement;
different policy-iteration trajectories need not visit identical states.

Adopt only strict decreases and retain every accepted actual tree's node
states on the following pass. There remain at most `n(n-1)` improvements.
There are at most `O(m|Q|)` distinct implicit boundary children; their
fallback costs are computed without inserting them into the recursive
state family. This is crucial to the fixed-exponent runtime. With the
combined generator above, a conservative bit-scan bound is

```
O(n^14 m^3 polylog(nm)).
```

The implementation is `actual_restriction_dp`; `--fitness actual` searches
against the combined generator with this stronger recurrence.

The boundary step has a concrete effect even with the **old represented
families frozen**, so its benefit is not merely another code generator:

- On the Section 2 `n=18` failure, the final family has 264 states. Both
  depth-prize separation and supported actual fallback retain cost 85.
  One-query terminal boundaries attain 80, the exact optimum.
- On the stronger `81/79` witness of Section 4, the frozen family has
  1,191 states. Both earlier methods retain 81; the boundary recurrence
  attains 79, again the exact optimum.

### A corresponding unrestricted pricing target

For any executable partial policy `P`, let its full output partition be
`Pi(P)` and define actual restriction credit

```
Gamma_T(P) = F(T) - sum_(A in Pi(P)) V_T(A).
```

The complete spliced tree has exact cost
`F(T)-Gamma_T(P)+W(P)`. Thus any policy with `Gamma_T(P)>W(P)` strictly
improves the incumbent, including cases where few or no hypotheses were
identified by the partial policy itself.

An `alpha`-approximate polynomial maximizer of `Gamma_T(P)/W(P)` over all
nontrivial executable partial policies would give an `alpha`-approximate
UDT algorithm by integer descent. Indeed the full optimal tree has
`Gamma_T=F(T)` and work `F_OPT`; if `F(T)>alpha F_OPT`, the returned ratio
must exceed one. This is a sufficient oracle condition, not a solved
pricing algorithm. The earlier complementarity obstruction applies to
restriction credit, so ordinary submodular greedy is not justified.

### Independent finite audit

```
python research-general-adversarial-pricing.py --audit-actual
```

passed 80 small separating instances. Every reconstructed tree was
executed directly on every hypothesis; depths and singleton identities
matched. On every subset, the displayed restriction-cost formula matched
the independently constructed pruned incumbent. Boundary optimization
never exceeded supported fallback or the former prize-fragment splice.
When all subsets were represented, the result equaled the independent
full adaptive Bellman optimum. These checks validate the recurrence,
not a global approximation bound for a small represented family.

## 7. Current limitation and next structural target

### Stable final search checkpoints

The following bounded searches are complete or were wrapped at the
requested checkpoint. No background search process remains.

| Candidate searched | n | Mutation checkpoint | Distinct valid evaluations | Counterexample found |
|---|---:|---:|---:|---|
| Combined depth-prize generator | 18 | 6,000 | 4,400 | No |
| Combined depth-prize generator | 24 | 1,200 | 756 | No |
| Combined actual-credit and boundary generator | 18 | 3,300 | at least 2,409 | No |
| Combined actual-credit and boundary generator | 36 | 100 | at least 81 | No |

"No" means every evaluated output matched its exact small-instance
optimum. It is not a claim about untested inputs. The last two evaluation
counts are conservative counts from the last completed progress
checkpoint before the requested wrap; additional proposals between that
checkpoint and stopping are not counted. The witnesses were reevaluated
and their final diagnostics saved in
`research-general-adversarial-actual-n18.json` and
`research-general-adversarial-actual-n36.json`. Combined depth-prize traces
are in the corresponding `research-general-adversarial-combined-*.json`.

These runs validate executable behavior and expose weaknesses in simpler
families. They do not prove a general coverage or approximation theorem.

**A small-completion barrier, proved directly.** Every nontrivial global
partial policy pays at least `n` raw work for its first query. If incumbent
depth prizes are at most `D_max` and the policy identifies at most `b`
hypotheses, its reward is at most `b D_max`. Consequently it cannot have
positive prize-minus-work when `b D_max<n`. In particular, a fragment
identifying just one hypothesis never has positive depth-prize profit for
a proper incumbent, because its prize is at most `n-1`.

Thus fixed-size coalition pricing alone does not certify improvement in
large instances with polylogarithmic incumbent depths. Its constructive
value is to expose contexts in which full continuation codes collectively
complete many hypotheses. This is why the combined candidate retains
**filled full coalition codes**, not only their short completion lists.
The lemma concerns the depth-prize certificate: actual splicing may also
gain from pruning queries on unfinished hypotheses, savings which that
certificate deliberately ignores.

The best failures found so far are missing third-intersection contexts,
with comparison states of size up to five. A constant larger intersection
arity repairs these finite examples, but the current evidence does not
justify letting the arity grow with the input or claiming a universal
bound from it.

The important remaining target is an approximation theorem for generated
depth-prize completion profiles: whenever the incumbent is much more
expensive than OPT, one of the generated legal partial policies must
collect enough incumbent-depth prize to outweigh its actual work.
Equivalently, its weighted density must compete with **all** executable
partial policies, not only with the represented library.

The search code records exact missing-state and unrestricted-profit
diagnostics precisely to distinguish that global obligation from a
finite library that merely appears to converge on sampled inputs.
