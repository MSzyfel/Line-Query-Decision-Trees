# Independent audit of the polynomial orientation theorem

Prepared 13 October 2026. Audited `sections/06c-polynomial-block-improvement.tex` and the first-batch orientation argument independently of its exact numerical certificate. The proof establishes the proposed general polynomial-time expected-depth improvement; the final numerical factor is certified separately in `poly-expected-next-check.py`.

## Audit conclusion

The first-batch transfer is valid. It couples an actual schedule saving to analytical witness masses through the exact coverage oracle and uses the same shift average as the positive-latency and zero-waiting bounds. It avoids the earlier invalid possibility of independently splicing actual orientation discounts into witness-block profiles.

No mathematical defect was found in the theorem proof. A wording adjustment is recommended when referring to the earlier deterministic block inequality: the new surrogate-minimizing shift is justified by the **shift-average proof underlying** that inequality, rather than by applying the old deterministic inequality directly to a different minimizing shift.

## 1. Actual orientation saving

For a block of rank `k`, write its newly covered positive mass as `m=x+y+z`, with exclusive endpoint masses `x,y` and shared mass `z`. First-endpoint exits have complete nonentropy allowance `2(k-1)+5`; second-endpoint exits have allowance at most `2(k-1)+4` because their adjacent predecessor is known negative. Querying the smaller exclusive mass first therefore yields a saving `max(x,y)` from the baseline `5m` allowance.

Each endpoint cap has mass at most `delta w(S)`. Consequently

```
max(x,y) >= (m-delta w(S))_+.
```

This also holds for edges incident to the origin, where the free negative endpoint has exclusive mass zero, and for cached endpoints on the negative route. Previously queried endpoints are negative for every still-unhit pattern. Suppressing cached or unproductive queries only reduces actual costs.

The block order must remain greedy by total newly covered block mass, as in the existing batch proof. Changing its endpoint orientation leaves the block union unchanged and therefore preserves this order and its decreasing newly covered masses.

## 2. First-batch transfer to the witness

The first budget is `k=floor(u)`, with `u` log-uniform on `[1,beta)` and `beta` between three and four. Let `H` be the positive mass hit by its at-most-`k` exact coverage set. Summing the actual block savings gives

```
Pin(G_u) >= sum_first_batch (g_j-delta w(S))_+
         >= (H-k delta w(S))_+.
```

The original witness's first `k` support blocks form a feasible at-most-`k` edge cover of all classes whose analytical support-hit index is at most `k`. Thus `H>=M_k=sum_{t<=k}m_t`. If the first budget already reaches the minimum cover size, it covers all positive mass and the same comparison remains valid.

For

```
P_k=ln(min(k+1,beta)/k)/ln(beta),
mu=sum_{k=1}^3 k P_k=3-ln(6)/ln(beta),
```

averaging the linear minorant gives

```
E Pin(G_u) >= sum_{t=1}^3 m_t sum_{k=t}^3 P_k - delta w(S) mu.
```

Both the latency/waiting bound and this saving hold under the same shift distribution. Choosing the shift minimizing the rational surrogate `2 MSSC+2 p0 K-Pin` makes its deterministic value at most this combined average. Choosing the old surrogate without `Pin` would not justify retaining the saving.

The actual transcript entropy can vary with orientation and shift, but its universal lower bound `J>=b sigma(delta)` applies to the selected schedule. Therefore it need not be added to the optimized surrogate.

## 3. Augmented coefficients and the partial-mass inequality

Let `e_t` be the existing monotone discrete discounts, and define

```
a_t=e_t+sum_{k=t}^3 P_k  for t<=3,
a_t=e_t                 for t>=4.
```

At the proposed parameters the first coefficients are approximately

```
a1=1,
a2=0.985844645695521,
a3=0.963823658967077,
e4=1.068152985707934.
```

They are not increasing. An earliest-in-index fill rule for partial mass would therefore be wrong. The manuscript correctly uses the direct threshold inequality instead:

```
sum_t m_t a_t
 >= e4 b - 2 delta w(S) sum_{t=1}^3 (e4-a_t).
```

It follows solely from `m_t<=2 delta w(S)`, all first three coefficients being below `e4`, and all later coefficients being at least `e4`.

Since `sum_{t=1}^3 sum_{k=t}^3 P_k=mu`, subtracting the orientation intercept gives

```
sum_t m_t a_t-delta w(S) mu
 >= e4 b - (e4-chi_or) w(S),
chi_or=2 delta(e2+e3)+(1-6delta)e4+delta mu.
```

Adding the zero-route discount `2p0/ln(beta)` leaves at least `chi_or b` whenever `chi_or+2/ln(beta)>=e4`. The remainder is precisely

```
p0 [chi_or+2/ln(beta)-e4],
```

so the sign condition is sufficient. This completes the revised local accounting, after which the existing optimum and entropy potentials telescope.

## 4. Independent finite checks

`python poly-orientation-audit-check.py` passed:

- 1,001 partial-mass linear-program checks, sorting the augmented coefficients explicitly rather than assuming their index order;
- 2,700 random first-batch checks, using exact small maximum-coverage enumeration and verifying the actual orientation saving against the analytical witness-prefix mass.

At `beta=3.512863` and `delta=0.142275675`, the exploratory floating values are `chi_or≈0.771720051343996` and zero-route slack approximately `1.29537704472917`. These checks test the accounting invariants; they do not replace the separate exact rational certificate of the approximation constant.

## 5. Audit of the mixed first/second-prefix refinement

The further refinement certified in `poly-expected-next-check.py` is also valid. It proves a general polynomial approximation below **5.283310**, using the same orientation-aware algorithm and changing its balance threshold to `delta=142671046/10^9`. The interpolation choices appear only in the analysis.

For any shift, the actual orientation saving obeys both linear bounds

```
Pin >= M_k0-delta w(S) k0,
Pin >= M_k1-delta w(S)(k0+k1),
```

where `k0=floor(u)` and `k1=floor(beta u)`. The latter follows by summing orientation savings through the second batch, whose union has at least the weight of the analytical witness's first `k1` blocks. If the algorithm already finished, its coverage is all positive mass and its length only decreases, so the same inequality holds.

Any convex combination with weight `alpha` between zero and one is valid and counts the saving once. The analysis uses

```
alpha=7963376/10^7 on [1,4/beta),
alpha=952407/10^6 on [4/beta,5/beta),
alpha=1 on [5/beta,6/beta),
alpha=0 elsewhere.
```

All three displayed intervals lie below two, so `k0=1` throughout them and `k1` is respectively three, four, or five. Let `q0,q1,q2` be their log-uniform probabilities multiplied by the stated interpolation weights. Relative to the old first-batch bound, interpolation adds `q_j(M_(j+3)-M_1)` to the mass credit and `delta w(S)(j+3)q_j` to its intercept. This gives exactly the reported augmented coefficients:

```
a1=1,
a2=e2+1-P1+q0+q1+q2,
a3=e3+P3+q0+q1+q2,
a4=e4+q1+q2,
a5=e5+q2,
a_t=e_t for t>=6,
mu=3-ln(6)/ln(beta)+3q0+4q1+5q2.
```

The latest exact certificate uses the rational threshold `T=345603/250000=1.382412`. Only `a1,a3` are below this threshold; `a2,a4,a5,a6` are above it, and monotonicity of `e_t` handles every later index. The correct capped-mass inequality is therefore

```
sum_t m_t a_t >= T b-2 delta w(S)[(T-a1)+(T-a3)],
chi=T-2 delta[(T-a1)+(T-a3)]-delta mu.
```

The zero-route condition is `chi+2/ln(beta)>=T`. The same local telescoping proof then applies with `B=3+2Phi(1)-chi`. No assumptions about ordering near-tied coefficients are required.

I ran the full exact certificate successfully. It gives `chi≈0.807181228456225`, `B≈4.766748469917878`, and an outward-certified ratio below `5.283310`. The independent audit script additionally passed 10,000 randomized checks of the **unclipped** convex-interpolation expression, its coefficient expansion, and its threshold lower bound. Using unclipped linear bounds specifically verifies the stated algebra rather than relying on extra positive-part savings.
