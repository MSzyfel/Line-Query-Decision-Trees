# Capacity-aware completion pricing

Auxiliary research note, 18 October 2026. This does not modify the article. It develops a global pricing certificate for a structured class; it does not establish an unrestricted improvement over O(log n/log log n).

## Why a mistake budget alone is insufficient

A bound of d on the number of oriented positive answers is a useful full-identification lower certificate. It need not give an equally strong lower bound on the work per completed hypothesis of a partial policy. A partial policy can spend one positive answer to discard a large unfinished population, then decode a smaller cheap population on its other branch.

The certificate agent exhibited a rank-two example: with n live symbols and no restriction on the population left after a positive answer, place n-k unfinished symbols on the positive branch and identify k symbols on the negative branch using a rank-two code. Its work is at most n+O(k^(3/2)). Taking k of order n^(2/3) gives density O(n^(1/3)), whereas the full optimal rank-two mean is Theta(sqrt(n)). Requiring every unfinished nonsingleton leaf to retain at least one unit of budget does not remove this example.

The missing information is the size of a candidate set that can survive with a given remaining budget. In the affine construction, a positive answer both consumes a budget unit and restricts the surviving population to at most a 1/Q fraction of the original capacity.

## A partial-policy theorem from entropy and remaining capacity

Consider binary unit-cost tests on n=Q^d uniform hypotheses, with Q>=2 and positive integer d. Orient one answer of every test as positive. Suppose every proper reachable transcript state S satisfies

    |S| <= Q^(d-j),

where j is the number of positive answers on that transcript. Thus the virtual remaining budget b=d-j is nonnegative, and a state with b=0 has at most one hypothesis. Negative answers leave the virtual budget unchanged. The bound must hold for all actual reachable states, including the unfinished leaves of a partial policy.

**Theorem.** Every executable partial policy of raw work W that identifies k hypotheses satisfies

    W >= (Qd/e) k.

In particular, assigning the same dual price Qd/e to every hypothesis is feasible for the full completion-cover LP from research-general-pricing-next.md. This is a statement about every partial policy, rather than only a scalar full-tree lower bound.

**Proof.** Let an unfinished leaf have population m and j positive answers, and let a completed leaf have its individual positive count j_h. Define

    B_U = sum_unfinished m j,
    B_C = sum_completed j_h,
    B = B_U+B_C,
    L = kd+B_U.

Here B is the total raw number of positive answers over all hypotheses. Since j_h<=d, B<=L.

Let E be the sum of the raw answer entropies of all queried nodes, using base-two logarithms. Entropy telescopes exactly over the output partition:

    E = n log_2 n - sum_unfinished m log_2 m.

The remaining-capacity assumption gives log_2 m<=(d-j)log_2 Q. Since unfinished mass is n-k, it follows that

    E >= [kd+B_U] log_2 Q = L log_2 Q.

At a query node with positive fraction p, the raw entropy contribution is its population times h_2(p). Concavity, with raw query work W as the total weight, gives

    E <= W h_2(B/W) <= B log_2(eW/B).

If W=0, k=0 and the conclusion is immediate. Otherwise E<=W and log_2 Q>=1 imply L<=W. For fixed W, the function x log_2(eW/x) is increasing on [0,W]. Because B<=L<=W,

    L log_2 Q <= L log_2(eW/L).

For k>0, L>0. Cancel L and rearrange to obtain W>=(Q/e)L>=(Qd/e)k. The zero-completion case is immediate. This proof also permits locally singleton leaves to be marked unrewarded; their entropy contribution is zero, and their capacity inequality remains valid. That detail is useful when restricting a global policy to an overlapping resource. QED.

The actual root-to-leaf histories, rather than independent endpoint or pair marginals, enforce the relation between unfinished mass and remaining capacity. This explains why adding a global mistake budget to an LP can still miss a necessary pricing constraint.

## A compact, verifiable source of the assumptions

Supply distinct vectors v_h over F_Q, all with first coordinate one, spanning a space of rank d+1. For each oriented positive test set C, verify

    v_h is not in span{v_g:g in C} for every h outside C.

These are the represented-flat conditions from research-general-information-next.md; Gaussian elimination verifies them in polynomial time. At a proper positive branch, the rank of the actual candidate span strictly decreases. A negative branch cannot increase it. After j positive answers, rank(S)<=d+1-j.

An r-dimensional vector space whose first coordinate is nonzero somewhere has exactly Q^(r-1) vectors with first coordinate one. Distinctness therefore gives |S|<=Q^(d-j). If n=Q^d, the theorem applies. All proof assumptions have a compact checkable representation; no enumeration of reachable spans is required.

This certificate also works when positive sets are flats smaller than hyperplanes, and when only an arbitrary separating subfamily of flat tests is supplied. It supplies a lower certificate; it does not synthesize a cheap identifying code from an arbitrary such subfamily.

For rational certificate verification, Qd/3 is a valid conservative price because e<3. One need not use floating point arithmetic in a dual feasibility certificate.

## Fixed arity

The same proof applies to K responses if one default response preserves budget and each of the other at most K-1 responses consumes one unit, with the same candidate-capacity bound. Write B for all nondefault answer work. Query entropy is at most

    W h_2(B/W) + B log_2(K-1)
    <= B log_2(e(K-1)W/B).

For Q>=K, E>=L log_2 Q and E<=W log_2 K give L<=W. The same monotonicity argument yields

    W >= Qd k / [e(K-1)].

The binary implementation below does not test this extension; its proof is given here. A compact multiresponse certificate must verify the flat condition for every nondefault answer cell.

## Exact polynomial pricing in the abstract capacity model

The Python companion forgets the actual test family and hypothesis labels, retaining only population s and remaining budget b. It permits every split into a positive child of population a and budget b-1 and a negative child of population s-a and budget b, provided their capacities are respected. It also permits stopping at any nonsingleton. A singleton is identified automatically.

This enlarges the available policy set. Its exact minimum completion density is consequently a lower bound for the actual instance's minimum uniform completion density, whenever the capacity certificate is valid. The abstract output is not an executable original-test policy.

For a rational unit completion prize lambda, let G_b(s) be maximum profit. Then

    G_b(1)=lambda,
    G_b(s)=max(0, max_a [G_(b-1)(a)+G_b(s-a)-s]), s>1,

with 1<=a<=min(s-1,Q^(b-1)) and s<=Q^b. Increasing s and then b computes all values in O(d n^2) arithmetic operations and O(d n) memory. Capacities are clipped at n.

The implementation retains actual integer work and completion count for each maximizing choice. Starting with the mean of an optimal full abstract code, exact rational Dinkelbach updates replace lambda by W/k whenever profit is positive. Each strict update decreases the ratio. There are at most O(n^3) possible work/count ratios because 0<=W<=n(n-1) and 1<=k<=n. This gives a deliberately loose fixed polynomial bound O(d n^5), with polynomial bit lengths. The procedure does not put a growing lookahead parameter in an exponent.

An independent completion-count DP records the least work C_b(s,k) for every k. It uses the same stop/singleton semantics and min-convolves the two children. Its straightforward running time is O(d n^4). The companion uses it only on small cases to audit rational pricing.

For arbitrary nonnegative prizes w_h, let W_k be the sum of the k largest prizes. The computable quantity

    rho_lower = min_(k>=1) C_d(n,k)/W_k

is a valid global lower bound on actual weighted completion density: an actual policy finishing k hypotheses has work at least C_d(n,k) and reward at most W_k. Thus rho_lower*w is feasible for the full completion-cover dual. With incumbent-depth prizes, 1/rho_lower is an a posteriori approximation certificate for that incumbent. This last weighted certificate is a direct consequence of the count DP; the current Python entry point exercises uniform prizes, not an LP solver or a weighted certificate implementation.

## Saturation is a material assumption

One cannot replace n=Q^d by n<=Q^d in the Qd/e theorem. At Q=256, d=2, n=256, the capacity at budget one is already 256, so the rank-two dumping example is allowed. Exact abstract pricing gives work 828, completions 67, and density 828/67, while the optimal full mean is 16. The claimed saturated lower price 512/e would be false on this input; the root entropy is only log_2 n, rather than d log_2 Q.

For non-saturated roots the exact abstract DP remains valid. More generally, if n=Q^(d-delta), the entropy argument gives

    E >= [kd+B_U-n delta] log_2 Q.

The root capacity deficit cannot be silently reset or charged afresh in each continuation. This is the same resource-accounting issue that makes the naive rank-only partial bound fail.

On all tested saturated inputs Q^d<=729, exact abstract minimum partial density equals optimal full mean. That stronger equality is an observation, not a proved general theorem. A sufficient condition is that the root full mean dominate every allowed conditional full mean: append an optimal code using each unfinished leaf's actual remaining budget and capacity, then apply root optimality. Monotonicity of the saturated means in d has not been proved here. The Qd/e theorem does not need that conjecture.

## Verification and consequence for the general objective

research-general-capacity-pricing.py passed 136 independent completion-count comparisons and 2,200 random actual abstract-policy audits, including 1,288 policies with completed hypotheses. The latter independently check the entropy identity, remaining-budget identity, and the Qd/e inequality. It retains the non-saturated counterexample above. Results are in research-general-capacity-pricing-results.json.

The certificate agent is extending these prices to overlapping verified resources with one global per-hypothesis/query charging budget. Such a certificate can support the exact completion-cover dual directly. A universal algorithm would still need to find either a sufficiently strong certificate or a profitable executable policy in polynomial time. That certificate-or-policy theorem has not been obtained. No unrestricted asymptotic improvement or new TeX theorem manuscript is claimed.
