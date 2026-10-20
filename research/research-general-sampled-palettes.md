# Sample a core, synthesize a code, reoptimize its palette

Auxiliary research note, 18 October 2026. This is a polynomial candidate generator with no unrestricted approximation ratio. The article is unchanged.

A supplied palette of `d` tests has at most `(K+1)^d` actual contexts: each test is either unasked or assigned one of its responses. Consequently all adaptive orders, stopping decisions, and incumbent-restriction exits can be optimized exactly in polynomial time when `d=O(log(n+m))` and `K` is fixed. This avoids the potentially poor fixed ordering of a directly lifted source code. It does not permit enumeration of every `m^d` possible palette.

The new generator obtains palettes as follows. Freeze an incumbent for one pass. At each of its nonsingleton states, draw a fixed number of uniform samples of size at most

    k = floor(log2(n+m+1)).

Solve the induced `k`-hypothesis training instance exactly by subset Bellman DP. It has at most `2^k` states and scans the original tests; this is polynomial in the explicit input. Train both with uniform weights and with incumbent leaf-depth weights. Equal training objectives are broken using the test's balance on the ambient state. The resulting proper binary sample tree uses at most `k-1` distinct tests. Keep that palette and discard the training order when optimizing on the **whole** hypothesis set.

For each generated palette, use the exact global recurrence from [global lifting](research-general-lifting-global.md), with the actual incumbent restriction as the stopping macro. This searches all reachable palette contexts and returns a legal complete original-test tree. In particular it dominates replaying its source sample code with the same incumbent-only fallback. The comparison does not include a fresh greedy fallback unless that fallback is explicitly added to both sides.

There are polynomially many sampled states and palettes. Each exact training DP costs `poly(n,m) 2^k`; each binary global optimization costs `poly(n,m) 3^k`. Accept only strict integer raw-cost decreases and freeze sources anew between passes. A proper identifying tree has raw cost at most `n(n-1)`, so the number of accepted passes is polynomial. The random bits merely choose candidate sources: the runtime bound and legality hold for every choice. Stopping after a batch without improvement does not certify failure of all possible palettes.

This makes logarithmic sample size computationally available without a superpolynomial `m^{log n}` enumeration. The missing step is statistical or combinatorial **coverage**: an exact empirical code may exploit rare tests that fit the sample and route many outsiders badly. Polynomial training and exact ambient reoptimization alone do not prove that a useful optimal-tree palette appears with appreciable probability.

Eighty independent small cases checked the training objective against a separate exact compressed instance, verified the context bound, and compared actual global palette cost against source replay and true optimum. On the six saved witnesses, results were:

| Instance | Greedy | Sampled-palette result | Exact optimum |
|---|---:|---:|---:|
| Original twelve-point failure | 47 | 47 | 46 |
| Second twelve-point failure | 48 | 46 | 45 |
| Fourteen-point failure | 61 | 60 | 57 |
| Sixteen-point failure | 66 | 66 | 65 |
| Eighteen-point failure | 87 | 82 | 80 |
| Weighted-source eighteen-point failure | 82 | 82 | 79 |

These finite results are weaker than the existing broad code-lifting library, which repairs all six. They also show a specific benefit of reordering: in the second twelve-point case, the best corresponding source replay costs 47, while global palette optimization costs 46. In the first eighteen-point pass, those costs are 86 and 83. The generator can be added to a library without worsening the incumbent, but these observations give no approximation theorem.

Files: [prototype](research-general-sampled-palettes.py), [recorded results](research-general-sampled-palettes-results.json). Exact global optimization is used solely for small-instance validation; the proposed runtime uses exact sample DP and logarithmic-palette DP only.
