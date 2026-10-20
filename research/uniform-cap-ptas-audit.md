# Independent audit: uniform shallow-cap PTAS

Assessment: **the theorem and approximation analysis are sound**. The result needs a distinguished hypothesis whose oriented answers are all miss, a supplied cyclic order in which every cap is an interval of at most fixed size `b`, and a uniform prior. Private singleton tests are unnecessary. Strict convex position supplies the cyclic-interval property; it suffices for the nonwitness hypotheses alone to be in convex position.

I read `constant-gap-session.md`, its verification program, and `sections/06h-uniform-bounded-cap-ptas.tex`. The following checks are independent of the development agent's count-vector implementation.

## Geometric decomposition and legal prefix

Marking the first `b` vertices in each length-`ell` cyclic piece leaves unmarked blocks separated by at least `b` marked vertices, including the wraparound gap. A size-`b` cyclic interval cannot hit two blocks: it would contain at least two unmarked vertices and an intervening gap, at least `b+2` points. If there is only one nonempty block, independence is immediate.

Separation from the actual witness supplies a cap covering every still-live marked point. Querying such a cap clears that point on the miss branch, and its positive branch contains at most `b` hypotheses. Any separating test family admits a proper local code of height at most `b-1`, so no singleton availability is used. Previously tested miss queries cannot be chosen productively again. Additional unmarked points cleared by the prefix only shrink the remaining independent blocks.

The prefix raw cost is at most `r(N+1)+b(b-1)r`, hence at most `2r(N+1)` for `N >= ell >= b(b-1)`. This accounts both for every prefix query on every live hypothesis and for all local positive continuations.

## Exact global continuation

At any residual state, every productive supplied query's positive group lies in exactly one block. Its negative branch retains the witness and updates only that block. Positive local Bellman costs use the entire restricted supplied test family and original unit weights. This proves the global recurrence's lower bound for **every adaptive tree**, without imposing an order or normal form. Conversely, each transition is realized by an original supplied query and its two stored continuations.

Blocks with the same test-mask family and live mask are interchangeable under uniform weights. The count vector therefore suffices. Its transitions remove at least one live hypothesis, so the DP is acyclic. Backtracking need only materialize one optimal tree; it need not duplicate the whole memoization graph in the output.

One reconstruction detail should be stated explicitly: store a realizing supplied line **for each physical block and each abstract mask**. A representative line from another block of the same type need not realize the mask on the chosen block. Root and the development agent were notified of this clarity fix; it does not change the proof.

## Sharper type bound

The proposed improvement from `2^(2^ell+ell)` to

    d_(b,ell) <= 2^((b+1)ell)

is also sound. The complement of an unmarked block contains a marked gap of at least `b` vertices. A size-`b` cyclic cap cannot hit both ends of the block by wrapping through that complement, because it would contain at least `b+2` points. Each mask on a block is consequently an ordinary interval. Filtering points removed collaterally by the prefix preserves its consecutive order, and its size remains at most `b`.

There are at most `b ell` possible interval masks after padding to `ell` positions. A type is a family of these masks, giving at most `2^(b ell)` types. Its family determines the actual block size: every residual point belongs to some supplied cap because it separates from the witness, so the union of the masks is exactly the first `size` positions. No extra factor for the block size is needed. Multiplying by at most `2^ell` nonempty live subsets proves the sharper bound.

The explicit running time is therefore

    f(b,ell) (n+1)^(2^((b+1)ell)) poly(n,m,input bit length).

This remains a PTAS: its polynomial exponent depends on the fixed accuracy and cap bound. The exact small-instance branch `N < ell` uses only parameter-dependent work times a polynomial in the query-list size. Raw costs on reachable states are integers of at most `n(n-1)`, and all geometric and mask operations have polynomial bit complexity.

## Approximation charging

Restriction of an optimal full tree to the residual hypotheses cannot increase any remaining depth. Thus the exact residual optimum is at most the original raw optimum, without a subtraction that would risk overcounting prefix savings.

Along the distinguished hypothesis's all-miss spine, at most `b` other hypotheses first exit at each query. The sum of their exit depths is at least

    sum_(i=1)^N ceil(i/b) >= N(N+1)/(2b).

The complete cost also includes nonnegative local-code and witness-depth terms. Combining this lower bound with `r <= 2bN/ell` and the prefix bound gives excess ratio at most `8b^2/ell <= epsilon`. Normalization divides both costs by the same `N+1`.

The actual distinguished witness is essential to this argument. An external common witness at an arbitrary flat recursive state need not be a hypothesis and does not by itself force its path to identify an all-miss point.

## Independent finite verification

`uniform-cap-ptas-audit.py` uses a full adaptive subset Bellman oracle on physical hypotheses and an independently written multiset-of-local-states quotient solver. It exhausts all separating supplied singleton/pair families for `N=4,5,6`, then samples larger cyclic-cap systems and includes families with no singleton queries.

The run passed **3,033 decompositions**, including **129 cases with multiple retained blocks** and **123 supplied-family instances having no singleton queries**. Checks cover exact adaptive continuation cost, legal ordinary-cap prefix cost, collateral deletions, first-hit lower bound, ratio constants, mask consecutiveness after deletion, recovery of block size from mask union, and the improved type count.

This PTAS rules out a fixed approximation gap through the stated uniform shallow-cap subclass unless P=NP. It makes no claim about constant-factor inapproximability of unrestricted instances.
