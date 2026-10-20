# Further polynomial accounting: a second positive answer can be worth asking

Prepared 14 October 2026 for the unrestricted supplied unit-cost binary planar line-query model. This report supplies a new polynomial block primitive. Its theorem is a rigorously proved local stage bound; the resulting optimized numerical factor is certified separately by the expected-depth scheduling agent.

## Main new lemma

The orientation-aware block algorithm can improve its discount by occasionally querying the second endpoint **after the first endpoint has already answered positive**.

For an actual scheduled adjacent block, let `x,y` be newly hit pattern masses exclusive to its two endpoints, let `z` be shared mass, and write `m=x+y+z`. Define

```
D(x,y,z)=max{x,y,x+y-z}.
```

There is a deterministic local choice of orientation and exit rule with weighted nonentropy allowance

```
5m-D(x,y,z)
```

in addition to shifted block discovery ranks. It improves the previous allowance `5m-max{x,y}`.

Use the previous stop-at-first-positive mode when `max{x,y}>=x+y-z`, querying the smaller exclusive mass first. Otherwise, query both endpoints before exiting. Equivalently, query both when `min{x,y}>z`. The mode and orientation are chosen from exact rational class masses. They do not change block coverage sets or the greedy block order.

## 1. Legal cost accounting

At ordinary block rank `k`, the baseline positive-route nonentropy allowance is `2k+3` queries per unit of newly covered mass.

In stop mode, suppose `x<=y` and query the endpoint exclusive to `x` first. Its `x+z` mass exits after at most `2k-1` discovery queries and uses two endpoint codes with overhead four, for allowance `2k+3`. The other endpoint's exclusive mass `y` exits after at most `2k` queries and has an adjacent negative endpoint; one endpoint code with overhead two gives allowance `2k+2`. The saving is `y=max{x,y}`.

In query-both mode, both endpoints are asked, even if the first is positive. Either exclusive transcript has one adjacent negative endpoint and therefore costs at most `2k+2` including endpoint overhead. The shared transcript has two positive endpoints and costs at most `2k+4`, using two endpoint codes. The weighted allowance is

```
(2k+2)(x+y)+(2k+4)z
= (2k+3)m-(x+y-z).
```

Choosing the less expensive mode gives precisely the discount `D`.

The transcript is still determined by the full hull pattern. Every positive transcript lies in the cap of an actual positive endpoint, so its mass remains below `delta w(S)`. The capped discovery entropy bound still gives `J>=b sigma(delta)`. Endpoint recovery identifies the same full hull pattern as before. Applying the entropy chain rule to the **new transcript** gives the legal conditional endpoint term `(I-J)/ln 2`.

Therefore the modified complete stage satisfies

```
W_stage <= 2 MSSC_block(G)+3b+2p0|G|-sum_blocks D+(I-J)/ln 2.
```

Choose the shift minimizing the rational surrogate `2 MSSC_block+2p0|G|-sum D`. This uses the same polynomial set of shift intervals. The local exit rule is part of the output tree; stopping immediately at its first positive answer would not implement the new bound.

Cached negative endpoints and edges incident to the origin remain valid. On the all-negative route, every previously queried endpoint is negative for every still-unhit pattern, so its exclusive and shared masses vanish. Suppressing its cached query only reduces the cost. Degenerate hulls can use the existing direct treatment.

## 2. A stronger transfer to analytical witness mass

Let `C=delta w(S)`. The two endpoint-cap bounds give

```
x+z<=C, y+z<=C,
max{x,y}>=m-C,
z<=2C-m.
```

It follows that

```
D >= max{0,m-C,3m-4C}.
```

The last term is the new one: `x+y-z=m-2z>=3m-4C`.

For any prefix of at most `L` productive scheduled blocks, with total covered positive mass `H`, the total discount is at least

```
sum_prefix D >= max{0,H-LC,3H-4LC}.
```

This follows by summing either linear lower bound separately. If its latest geometric batch has budget `k`, exact maximum coverage gives `H>=M_k`, where `M_k` is the analytical witness mass covered by its first `k` blocks. Thus both transferable linear bounds are valid:

```
sum_all D >= M_k-LC,
sum_all D >= 3M_k-4LC.
```

For the first batch, `L<=k`, yielding the stronger comparison `3M_k-4kC`. For later batches, `L` is bounded by the sum of their budgets. A schedule that already ended covers all positive mass and uses fewer blocks, so these bounds remain valid in that case too.

One may take a maximum of the bounds, or a convex combination with nonnegative weights summing to one. Adding independent prefix bounds would count the same discount repeatedly and is invalid. The existing shift-average optimization applies to any such convex combination because it retains the same actual `sum D` saving once.

## 3. Why this can improve the current framework

The old pointwise guaranteed saving was `(m-C)_+`. The new saving equals at least that amount and increases further when `m>3C/2`. In the limiting symmetric realizations, its guaranteed value is exactly

```
0                    for m<=C,
m-C                  for C<=m<=3C/2,
3m-4C                for 3C/2<=m<=2C.
```

At the maximum possible block mass `m=2C`, the saving doubles from `C` to `2C`. Exact coverage can expose this large-block regime through the witness-prefix transfer without conflating actual and analytical block masses.

Optimizing convex mixtures of the old slope-one and new slope-three prefix bounds is now a concrete numerical proof task. The geometric construction, polynomial complexity, arbitrary-prior validity, and local entropy accounting are proved above. No inapproximability claim or factor below two follows from this lemma alone.

## 4. A stronger rational discount by crediting the second answer's information

There is a further improvement. In query-both mode, keep the orientation `x<=y`, with the smaller exclusive mass first. Define a **virtual stop transcript** by merging the actual `x` and `z` exits into their first-positive group `x+z`. The `y` exit and all negative-spine answers are unchanged. In stop mode the virtual and actual transcripts coincide.

Every virtual positive cell is still contained in one actual positive hull cap, so its information `J_v` has the same universal bound `J_v>=b sigma(delta)`. For each query-both block, the actual transcript's extra information is exactly

```
J_actual-J_v=(x+z) H_nats(x/(x+z)).
```

Thus charging endpoint information against `J_v` permits an additional saving `(x+z) H_bits(x/(x+z))`. This is information from the additional second question; it is counted once by writing the entropy chain rule relative to the coarser virtual transcript.

To keep every algorithmic comparison rational, use a rational lower tent for binary entropy. Choose

```
p=8527/50000,
c=329469/500000,
K=c/p=329469/85270.
```

Exact rational logarithm enclosures certify `H_bits(p)>c`; also `c+2p>1`. Concavity and symmetry of binary entropy give

```
H_bits(t)>=min{Kt,K(1-t),c} for every t in [0,1].
```

Therefore define the rational extra information credit

```
E_L(x,z)=min{Kx,Kz,c(x+z)},
D_L=max{y,x+y-z+E_L(x,z)},  with x<=y.
```

Choose stop mode or query-both mode according to the larger term in `D_L`. The complete stage, now measured against virtual transcript information, obeys

```
W_stage <= 2 MSSC_block+3b+2p0|G|-sum D_L+(I-J_v)/ln 2.
```

Its optimized shift surrogate remains entirely rational. The tent and its constants are fixed; no approximation or comparison of transcendental entropy values is required by the algorithm.

### A universal affine minorant

Under cap bound `C=delta w(S)`, the new rational discount satisfies

```
D_L >= max{0,m-C,a m-b C},
a=914748/414739 approximately 2.2056,
b=1000018/414739 approximately 2.4112.
```

Here is a proof that does not depend on numerical optimization. For fixed `m` between `C` and `2C`, set `x<=y`. The cap constraints imply `x,y>=m-C`, and `x+y<=m`. Their feasible triangle has vertices

```
(m-C,m-C), (m-C,C), (m/2,m/2).
```

The query-both expression `x+y-z+E_L(x,z)` is concave on that triangle because `z=m-x-y` and `E_L` is the minimum of three affine functions. Its minimum is therefore attained at a vertex. At the two zero-shared vertices the expression is `m`. At the remaining vertex it is

```
3m-4C+C min{K(m/C-1),K(2-m/C),c}.
```

Write `r=m/C-1` and `r0=1/(K+2)`. Below `r0`, the old discount `m-C` dominates `a m-bC`. Above `r0`, each term of the entropy tent is at least `K(1-r)/(K+1)`: the first by `r>=r0`, the second trivially, and the constant because `c+2p>=1` implies `c>=K/(K+2)`. The two vertex bounds consequently dominate the affine expression with

```
a=(2K+3)/(K+1), b=2(K+2)/(K+1).
```

For `m<C` the affine expression is negative and zero suffices. This proves the universal minorant. Summing over a prefix of at most `L` blocks and transferring its covered mass through exact coverage gives

```
sum D_L >= a M_k-b L C,
```

alongside the old `M_k-LC` and zero bounds. These may again be mixed convexly under the same shift average.

As an optional instance improvement, query-both mode may put the larger exclusive endpoint first and use `E_L(y,z)`. This entropy credit is at least `E_L(x,z)`, and its virtual positive group `y+z` remains in an individual cap. Stop mode keeps the smaller exclusive endpoint first. The same universal affine bound remains valid; the simpler version above is already sufficient.

`further-accounting-check.py` verifies the entropy-anchor inequality using exact rational log enclosures and checks 10,000 exact rational local mass configurations against the affine minorant. Together with the earlier tests, it checks 10,000 mode identities, 201 exact tight profiles, and 22,057 circular-prefix inequalities. The actual numerical approximation factor requires the separate global prefix-mixture certificate.
