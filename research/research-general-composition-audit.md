# Independent audit of product decomposition and target coalitions

Auxiliary review, 18 October 2026. Reviewed the root notes and companion
implementations without editing them or restarting searches. No material
proof, runtime, or scope issue was found.

## Product decomposition

Reviewed:
[note](research-general-product-decomposition.md) and
[implementation](research-general-product-decomposition.py).

The entropy cut \(H(A)+H(R\setminus A)-H(R)\) is symmetric and submodular,
and is zero exactly at an independent split. The integer count-product
formula has the correct direction: maximizing
\(P(A)P(R\setminus A)\) minimizes the cut. The implementation's
maximum-adjacency choice minimizes
\(f(W\cup v)-f(v)\), comparing the exact ratio
\(M_R(v)/M_R(W\cup v)\). The pendant-pair contraction step preserves the
original universe and operates on unions of disjoint query-index blocks.
Its zero test is an exact integer equality.

Each count product has \(O(n\log n)\) bits, and cross multiplication
preserves a polynomial bound. Projected word masks may have \(m\) bits,
which adds only polynomial scan and arithmetic cost. The implemented
factorization does not enumerate query subsets. The exhaustive cut
comparison occurs only in validation.

Independence together with uniform probability on distinct complete words
forces uniform factor supports and an actual Cartesian relation. This
remains valid at recursive groups: their empirical marginals are the
corresponding independent uniform factors, with equal multiplicities in
the original word list.

The optimal mean-depth additivity proof correctly conditions on every
other factor, suppresses determined queries, and then sums disjoint query
types. A sequential global code has exactly the product number of leaves,
so its explicit binary representation has at most \(n-1\) proper query
nodes. Replicating marginal codes therefore does not create a hidden
superpolynomial output.

The greedy identity is valid with consistent original query-index
tie-breaking, as used by the implementation. Querying another independent
factor cannot change the ordering of candidate queries within a factor.
Thus factorization followed by the same greedy rule supplies no direct
greedy-cost improvement. The note states this limitation and correctly
places the value in selecting different marginal procedures/certificates.
Gated or conditionally factored systems are not silently treated as
independent root products.

The added completion-dual tensorization statement is sound and stronger
than scalar additivity. For nonnegative feasible marginal prices \(y_i\),
fix all other coordinates \(z\) in an arbitrary global partial policy.
Suppress their constant queries and any locally determined factor queries.
The remaining local policy completes every globally completed \((a,z)\),
and may complete additional local singletons. Nonnegativity permits those
additional outputs to be ignored when applying local dual feasibility.
Its work is at most the original factor-\(i\) query work on that fiber.
Summing over \(z\) and then \(i\) charges each global query exactly once.
Thus \(y(h)=\sum_i y_i(h_i)\) is a valid full completion-dual price, with
objective \(n\sum_i(\sum_a y_i(a)/n_i)\). A one-point marginal has feasible
price zero because its singleton completes with no query.

The reported 84 exact cut comparisons, 5,928 zero-vs-Cartesian checks,
84 recursive factorizations, and 40 cost/execution comparisons support
the specific implementation. They are finite checks rather than the
runtime proof. No additional broad run was performed for this review.

## Target coalitions

Reviewed:
[note](research-general-target-coalitions.md) and
[implementation](research-general-target-coalitions.py).

The integer covering optimum equals the cheapest target-completing partial
policy: sequentially replaying selected policies on the actual current
cells, while suppressing determined queries, never increases their
aggregate raw work. Every covered target remains identified. This argument
does not make the fractional target cover exact.

The default-spine lower bound is valid. If an outsider remains unprobed,
every requested target must have exited positively on a target query.
Adding singleton queries does not lower the original cap-cover number,
since a singleton can be replaced by a cap containing that target.
The displayed outside-work expression is at least \(u\tau(D)\) for
\(u\ge2N\), including the case in which every outsider is probed.
The cap-cover spine and its disjoint singleton-decoding exits give the
claimed \(2N^2\) additive upper bound.

The central \(k\)-subset cover identity, the weight-\(1/k\) executable
fractional cover, and \(u=N^3\) give the stated
\(\Omega(\log n)\) restricted-cover gap. The construction still has
uniform hypotheses, unit costs, binary tests, and \(m=O(n)\).
Large symbolic rows are explicitly separated from materialized instances.

The arbitrary target-prize theorem is also valid. Its pair ledger charges
target-cap separations to outsider endpoints and outsider-singleton
separations to target endpoints, giving
\[
 W(P)\ge (u/B)\,w(C(P)\cap C)
\]
for every \(u\ge1\). The maximum-prize cap and its supplied singleton decoder
cost at most \(u+N^2\), proving the
\(1+N^2/u\) pricing factor. This price belongs to the earlier pair
completion ledger; it is not relabeled as a stronger causal relaxation.

The weighted validation computes minimum cost divided by requested prize
over all target subsets. This does equal actual optimal target density,
even when a cheapest policy completes extra targets: choosing its entire
completed target set establishes one inequality, and the extra reward
only improves the reverse inequality.

The stated scope distinctions are necessary and correctly present:
the gap is target-only fractional-cover versus integral completion;
the pricer assumes zero outsider prizes; neither is hardness for
unrestricted UDT or for its full-H exact completion-cover LP.
The reported 125 independent cost/execution audits, 119 weighted pricing
checks, and 120 central-cover identities are consistent with the code.

## Conclusion

Both results are sound within their stated scope. They strengthen the
research infrastructure and expose useful composition requirements.
They establish no unrestricted improvement over
\(O(\log n/\log\log n)\), and the notes do not claim one.
