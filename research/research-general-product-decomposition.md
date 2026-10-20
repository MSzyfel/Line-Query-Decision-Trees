# Exact product decomposition through symmetric entropy cuts

Auxiliary research note, 18 October 2026. This gives an exact polynomial preprocessing and composition theorem. It does not improve the unrestricted approximation ratio. The article is unchanged.

The resource agent found a warning for root-only certificate alternatives: a Cartesian product of a certificate-poor affine system and threshold search simultaneously has a poor pair-plus-entropy lower bound and a large minimum global identifying palette. This note supplies a constructive response to **exact products**. The response relation can be factored in polynomial time, and the uniform optimal mean cost adds across its factors. This is not a solution for arbitrary dependent response systems.

## 1. Factor the response relation, not the hypothesis labels

Let `Q` be the supplied test indices. A hypothesis is its complete response word; these words are distinct. Under the uniform prior, write `H(A)` for the Shannon entropy of the response subvector on indices `A subset Q`.

For any query group `R`, consider the cut function

    f_R(A)=H(A)+H(R minus A)-H(R),  A subset R.                (1)

It is nonnegative, symmetric, and submodular. It is zero exactly when the two response subvectors are independent. The [symmetric submodular minimization algorithm of Queyranne](https://doi.org/10.1007/BF01585863) finds its minimum over nonempty proper subsets in a polynomial number of oracle calls. A primary accessible account of the maximum-adjacency and contraction statements is [Iwata and Konno, Section 2](https://arxiv.org/html/2605.01473v1).

Recursively split a group `R` whenever its minimum in (1) is zero. Stop otherwise. Independent groups stay independent when an individual group splits internally, so this yields a product partition of the entire response vector. No exhaustive query-subset enumeration is used by the algorithm.

Because complete response words are distinct and the joint distribution is uniform, every resulting marginal is uniform on its support. To see this, fix all factors except one: independence makes each product cell have the same probability `1/n`, forcing all probabilities within the remaining factor to agree. If factor support sizes are `n_i`, their Cartesian product has exactly `n=product_i n_i` cells.

This connects to relational factorization in databases. Polynomial factorization of explicit relations is already known; see [Olteanu, Koch, and Antova](https://arxiv.org/abs/0705.4442). No novelty is claimed for relational factorization or symmetric submodular minimization. The construction here makes their use for uniform decision trees and exact entropy comparisons explicit.

## 2. Exact comparisons without a real-valued entropy oracle

For the empirical uniform distribution on the `n` listed words, let `c_z(A)` be the number with projection `z` onto `A`, and put

    P(A)=product_z c_z(A)^{c_z(A)}.

Then

    H(A)=log2 n-(1/n)log2 P(A).

For fixed `R`, define `M_R(A)=P(A)P(R minus A)`. Equation (1) becomes

    f_R(A)=(1/n)log2[ n^n P(R) / M_R(A) ].                    (2)

Thus minimizing the entropy cut is equivalent to maximizing the integer `M_R(A)`. Its zero condition is the exact integer equality

    M_R(A)=n^n P(R).                                         (3)

The maximum-adjacency ordering used in Queyranne's algorithm compares `f_R(W union v)-f_R(v)`. By (2), compare the rational ratios

    M_R(v)/M_R(W union v).

Contraction only merges index blocks; it still calls the same cut function on their unions. All products and cross-products have polynomial bit length `O(n log n)`, since `sum_z c_z=n`. Consequently the combinatorial minimizer is implementable with exact integer arithmetic; there is no numerical zero test or assumed exact logarithm operation.

Each projection count can be computed by scanning the explicit response matrix. With at most `O(m^3)` calls per minimization and at most `O(m)` recursive groups, a loose `O(m^4)` oracle-call bound suffices. Including direct projection scans and polynomial-bit arithmetic gives fixed-exponent polynomial time in `n,m` and the input encoding. Faster relational algorithms are available, but are unnecessary for this runtime claim.

Pairwise independence of tests is insufficient. For instance, the uniform four words `000,011,101,110` have pairwise independent coordinates but no nontrivial product factor. The full entropy cut correctly leaves them together.

## 3. Uniform optimal mean cost is additive

Let the discovered response factors have uniform hypothesis sets `H_i`. Each original test belongs to one query-index factor and acts only on that factor. Write `OPT_i` for its optimal mean identification cost.

**Additivity theorem.**

    OPT_mean(H)=sum_i OPT_i.                                 (4)

For the upper bound, identify factors sequentially, using their original tests. Their responses together determine the original hypothesis. For the lower bound, take any full global tree and fix all factors other than `i`. Prune queries to those other factors, whose answers are now determined. The remaining queries give a correct identifying tree on the uniform `H_i`. Its mean is at least `OPT_i`. Average over the independent fixed factor values, then sum over `i`: every global query is counted once. Randomized choices induced by other factors cannot lower the optimum of the deterministic marginal identification problem.

Therefore any polynomial algorithm library can be applied separately on the factors and its cheapest returned marginal code chosen independently. Executing these codes sequentially gives a legal original-test global tree. If marginal code `i` costs `a_i`, the resulting mean is `sum_i a_i`; if every code has ratio at most `alpha`, their sum has ratio at most `alpha`. Different algorithms can be selected on different factors. No outside population is ignored or charged twice.

The explicitly reconstructed global tree has `n` leaves and at most `n-1` proper query nodes. Factor codes are replicated only as needed at actual product cells; the final representation remains polynomial. The companion prototype constructs and executes this tree for balance greedy on each factor.

**Limitation.** With one fixed original-test priority for ties, ordinary entropy greedy already interleaves the same marginal greedy policies on a product: relative query entropies within a factor do not change when another factor is queried. Its mean is therefore the sum of marginal greedy means under that consistent tie rule. Factoring and then running the same greedy rule does not by itself improve its output. The value of (4) is exposing reusable quotient codes, permitting different procedures and certificates per factor, and avoiding false root-only dichotomies. A tie rule depending on other factors need not reproduce the same deterministic marginal code.

## 4. Completion-dual certificates tensorize as well

There is a stronger statement than the scalar cost identity. Suppose each uniform factor has nonnegative completion prices `y_i(a)` satisfying

    sum_(a completed by P_i) y_i(a) <= W(P_i)

for every executable local partial policy. Then

    y(h)=sum_i y_i(h_i)                                       (5)

is feasible for the **global executable-completion dual**, against every partial policy on the whole product. Its objective is

    sum_h y(h)=n sum_i [sum_a y_i(a)/n_i].

Fix the other factor coordinates to a tuple `z`. In any global partial policy, suppress queries to those fixed factors. The retained queries form a legal partial policy on factor `i`. Every globally completed hypothesis `(a,z)` is locally completed, possibly together with extra local singleton outputs. Nonnegative prices therefore give

    sum_(globally completed (a,z)) y_i(a)
       <= retained local work
       <= global i-query work on that fiber.

Sum over `z`, and then over `i`. Each actual global query belongs to one factor, so its work is counted exactly once. This proves (5) with no independently reset resources. One-point factors have zero feasible completion price, since their zero-query singleton policy already completes them.

The resource agent independently audited this argument. It permits local code-or-certificate procedures to compose their full partial-policy certificates across automatically detected independent factors, rather than merely adding scalar lower estimates. It still requires useful marginal procedures; irreducible factors remain unrestricted.

## 5. The affine-times-threshold obstruction is decomposable

The [resource note](research-general-causal-resource.md) proves that an affine equality factor times an ordered-search factor defeats the proposed root-only combination of a pair/entropy bound and small global palette size. Its threshold factor can force a palette of order `sqrt(n)` despite logarithmic adaptive search.

The product partition is found automatically by (1)-(3). Ordered search can be solved optimally; the affine factor has an identifying palette of size `O(OPT_mean)` and hence the earlier entropy-drift `O(log log n)` guarantee. Additivity transfers those marginal guarantees to the product without a free activation or repeated ledger. This is a promised-family consequence. It does not say every instance has such a product decomposition or such marginal guarantees; a prime response relation may remain completely unrestricted.

Conditional versions can be applied at already reached actual states, but choosing which paid queries expose useful factors remains a separate obligation. Gated tests generally couple the factors and may destroy root factorization even if the hypothesis labels have a convenient Cartesian description. An arbitrary labeling of hypotheses by tuples is not evidence of response independence.

## 6. Finite verification

[The implementation](research-general-product-decomposition.py) uses exact maximum-adjacency contractions and count products. It passed 84 minimizer comparisons against exhaustive query cuts, 5,928 exact checks of zero mutual information against Cartesian support cardinalities, and 84 full-factorization checks. Forty independent small product instances verify optimal mean additivity against an exact full-instance Bellman solver, reconstruct actual original-query factor codes, and verify the ordinary-greedy product identity. Eighty exact global partial-policy profit computations check tensorized optimal-depth prices and independently scaled marginal prices. The pairwise-independent XOR example is rejected as a product.

The exhaustive cut comparisons and exact decision-tree DP are validation oracles only. The implemented factorization and greedy reconstruction contain neither exhaustive query-subset search nor an exact general decision-tree oracle. [Results](research-general-product-decomposition-results.json) preserve that distinction. No unrestricted approximation improvement is claimed.
