# Direction 3: eliminating the entropy surcharge by bounded-depth rollout

Prepared 13 October 2026. This report concerns the supplied unit-cost binary line-query model, with maximum depth or arbitrary positive prior expected depth. The two new theorems below use the previously proved additive quasipolynomial baseline bounds. They do not need the newer adjacent-block refinement, and do not establish novelty relative to the complete literature.

## Main proved result

**Both objectives admit a quasipolynomial-time `(2+epsilon)` approximation for every fixed positive epsilon.** The key step is to optimize a logarithmic-depth initial decision tree exactly, using the additive baseline algorithm at its frontier. For maximum depth, every surviving branch has used the same number of optimal queries. For expected depth, the total probability reaching the frontier is at most optimum expected depth divided by the frontier depth. These observations eliminate the additive entropy term.

The earlier numerical factors approaching 4.465 and approximately 3.718675 remain useful bounds for the simpler baseline without rollout. They are superseded as broad quasipolynomial approximation guarantees by this construction.

## 1. A general continuation recurrence

Let `B(S)` be the actual cost of a deterministic baseline tree constructed on a nonempty hypothesis subset `S`. All supplied queries remain available. Ignore a query unless both answer subsets are nonempty. Write `S_i^0,S_i^1` for its children and `w(S)` for the original, unnormalized prior mass. Stop at a singleton with value zero.

For maximum depth define

```
F_0^W(S) = B_W(S),
F_j^W(S) = min { B_W(S),
                 1 + min_i max(F_(j-1)^W(S_i^0), F_(j-1)^W(S_i^1)) }.
```

For expected depth use

```
F_0^E(S) = B_E(S),
F_j^E(S) = min { B_E(S),
                 w(S) + min_i [F_(j-1)^E(S_i^0) + F_(j-1)^E(S_i^1)] }.
```

Each minimum has a concrete witness. Choosing the first alternative runs the baseline tree immediately; choosing a query constructs the selected two child trees. Thus these are implementable decision-tree recurrences, not lower-bound computations. The option to stop early is useful but unnecessary for the guarantee: the truncated optimum is already an admissible comparison.

Memoize `(S,j)`. A state at rollout depth `t` is an intersection of `t` queried answer sides with the initial hypothesis set. There are at most `(2m)^t` descriptions at depth `t`, and therefore at most `(2m+1)^(k+1)` descriptions through depth `k`, up to an immaterial constant. Duplicate descriptions of the same subset may be merged. Test every supplied query by scanning the explicit hypothesis table; this costs polynomial time per state. A depth-`k` trunk can have many leaves, but its **distinct states** are bounded by query histories, so it does not require enumerating all `(m^(2^k))` labelled trees.

If a baseline invocation takes `(mn)^{O(log n/epsilon)}` time, doing one invocation per memoized state preserves quasipolynomial time for `k=O(log n/epsilon)`. Baseline costs and all expected-cost recurrence comparisons are rational with polynomial encoding length: a proper tree has at most `n-1` internal nodes and every query has unit cost. No entropy value is required by the recurrence itself.

## 2. Maximum depth: a factor of `2 lambda`

Assume the baseline has the additive guarantee

```
B_W(S) <= a OPT_W(S) + gamma log_2 |S|,
```

where `a>1` and `gamma` are fixed. At the root with `n>=2` choose

```
k = ceil(gamma log_2 n / (a-1)).
```

Let `D=OPT_W(S)`, and truncate an optimal proper tree after depth `k`. A leaf ending at depth less than `k` has total cost at most `D`. Every surviving frontier state `A` has an optimal identifying subtree of height at most `D-k`, because the original optimal subtree is available. Hence following this trunk and using the baseline at its frontier gives on a surviving branch

```
k + B_W(A)
 <= k + a(D-k) + gamma log_2 n
 = aD - (a-1)k + gamma log_2 n
 <= aD.
```

Early leaves also have cost at most `D<=aD`. The recurrence minimizes over all admissible trunks, so `F_k^W(S)<=aD`. If `D<k`, the optimum ends completely before the frontier, and the rollout returns the exact optimum.

The existing quasipolynomial baseline has `a=2 lambda`. Therefore choosing `lambda=1+epsilon/2` gives a **`(2+epsilon)` approximation**. For an entirely rational parameter recipe for `0<epsilon<=1`, the original individual-vertex baseline may use `delta=1/5` and `gamma=4`; its conditions hold since

```
(5/4)^4 > 2,
5^4 > 2^7,
a+4 <= 7.
```

One can choose the integer depth `k=4 ceil(log_2 n)` without computing a transcendental ceiling; `a-1>=1` makes this depth sufficient. The rollout state count is `(2m)^{O(log n)}`, while the baseline grade count is `O(log n/epsilon)`. Total time is `(mn)^{O(log n/epsilon)}` for these fixed parameters, with ordinary polynomial bit arithmetic.

This proof is stronger than the initial small-optimum patch: exact bounded-height solution up to `c log n` plus the additive baseline also yields `(2+epsilon)`, but rollout removes the additive term directly and needs no guess for optimum height.

## 3. Expected depth: arbitrary positive priors, also `(2+epsilon)`

Use global raw weights throughout. Define

```
H(A) = sum_(h in A) w_h ln(w(A)/w_h).
```

Assume the baseline satisfies

```
B_E(A) <= a OPT_E(A) + c H(A),   a>=1,
```

for every nonempty subset `A`. Let `OPT=OPT_E(S)` denote the root raw expected cost. Truncate an expected-optimal proper tree at depth `k`. Let `P` be its expected raw prefix cost, let `R` be its remaining raw cost, and let `mathcal A` be its nonterminal frontier states. Then `P+R=OPT`. The sum of restricted optima at the frontier is at most `R` because the original subtrees are legal continuations. Applying the baseline there costs at most

```
P + aR + c sum_(A in mathcal A) H(A)
 <= a OPT + c sum_(A in mathcal A) H(A).
```

Write `q=sum_A w(A)`. Every hypothesis reaching a frontier state has already paid `k` queries, so `kq<=P<=OPT`. Moreover, the normalized entropy inside each state is at most `ln |A|<=ln n`. Consequently

```
sum_A H(A) <= q ln n <= OPT ln n / k.
```

Thus the exact continuation recurrence returns

```
F_k^E(S) <= (a + c ln n/k) OPT.
```

This is valid for arbitrary positive priors, including exponentially small probabilities; it uses their total frontier mass and does not bound their maximum depth. Choose `a=2+epsilon/2` and `k=ceil(2c ln n/epsilon)`. The result is a **`(2+epsilon)` approximation**.

A simple fixed parameter recipe uses the already proved individual-vertex baseline with `lambda=1+epsilon/4`, `delta=1/8`, and `c=3`, for `0<epsilon<=1`. Its local coefficients satisfy

```
4 + (3/2)lambda <= 47/8 < 6 <= 9 ln 2 = c sigma(1/8),
h(1/8) >= (3/8) ln 2 + 7/64 >= 23/64 > 1/3,
```

where `sigma(1/8)=ln 8=3 ln 2`, `ln 2>=2/3`, and `-ln(1-x)>=x` were used. Thus all balanced, flat, and endpoint-information inequalities hold for this fixed `c`. Take `L=ceil(log_2 n)` and the rationally computed depth `k=ceil(6L/epsilon)`. Since `ln n<=L`, this is sufficient. The grade count and trunk depth are both `O(log n/epsilon)`, giving time `(mn)^{O(log n/epsilon)}`. For `epsilon>1` simply run the algorithm with epsilon one, since factor three is at most `2+epsilon`.

The approximation uses one deterministic output tree. The dynamic program is permitted to shorten the route of a rare hypothesis or lengthen it relative to a different trunk; the guarantee concerns the global expected cost. No maximum-depth truncation of the final output tree is imposed.

## 4. What remains open: going below two

The factor two remains the coefficient of the two-hull-support expansion in the additive baseline. Rollout eliminates the logarithmic count/entropy surcharge, but cannot lower this coefficient without a stronger baseline inequality. Adjacent-block pinning changes its surcharge and therefore the required rollout depth; it does not by itself change the limiting coefficient.

The strongest direct next target is an additive theorem

```
B_W(S) <= alpha OPT_W(S) + O(log |S|),
B_E(S) <= alpha OPT_E(S) + O(H(S)),
```

with `alpha<2`. The same rollout conversion immediately turns it into a quasipolynomial approximation approaching `alpha`. This gives a clear reason to revisit original caps and stronger restriction accounting.

### Original caps: the missing lemma

The hull partition ensures each class is constant on every original witness query whose two hull supports are both negative. A direct original-cap ordering does not have this property: a single hull-pattern class may be split by an interior normalized query vector. A long first-hit time of individual hypotheses need not be a removable common prefix of their eventual output class.

The useful possible lemma should compare complete macro cost against **the actual optimum decrease of its output partition**, not against optimum at the current state alone. A desired inequality is

```
macro_E(S) <= alpha Delta_E(S,Pi') + c I(S,Pi'),  alpha<2.
```

Its proof must name the optimal-tree nodes removed when each output cell is revealed, or quantitatively bound nodes that remain mixed. Cover feasibility alone does not supply this credit. The exact halfplane coverage primitive means this is chiefly an accounting/normalization problem, not simply a geometric coverage-oracle problem.

### Two concrete experiments

1. Compute original-query constancy on every actual hull cell. Use these larger negative-constant and positive-constant regions as candidates in an exact small-instance macro solver. Compare their removable-prefix credits to those obtained from mere hull-support negativity.
2. Search cells split by interior queries where first original-cap hit is late but supporting hit is early. Test proposed information-compensation inequalities against these instances before claiming a one-support coefficient.

More constancy can improve individual instances, but a universal improvement needs a lower bound on useful constancy or a tradeoff with information. The present `(2+epsilon)` theorems do not assume either unproved statement.

## 5. Literature checks

The relevant direct-cover primary sources remain [Har-Peled and Lee, minimum halfplane cover](https://jocg.org/index.php/jocg/article/view/2950), and the explicit maximum-coverage adaptation in [Badanidiyuru, Kleinberg and Lee, Appendix B](https://arxiv.org/html/1112.0689). Their planar coverage structure is useful for an original-cap route, but does not establish the restriction-credit inequality above.

A search result indexed arXiv:2604.12036 with an older title asserting a constant uniform decision-tree approximation. The current [version 3](https://arxiv.org/abs/2604.12036), dated August 2026, is *Simpler Logarithmic Approximation Algorithms for the Optimal Decision Tree and Adaptive Set Cover*, by Michał Szyfelbein, and states logarithmic approximation guarantees. The stale search snippet should not be treated as a current competing constant-factor theorem.

## 6. Status and checks

The bounded-depth rollout lemmas are elementary general reductions from additive baselines and were independently checked by the root agent. They do not require any new geometry assertion beyond those already used in the existing additive baselines. Finite checks in `direction3-rollout-check.py` compare the memoized recurrence to exact optimal costs on small supplied-test tables, check raw frontier accounting with skewed priors, and check maximum-depth truncation bounds. Finite checks support the implementation invariants; the preceding proofs supply the approximation guarantees.
