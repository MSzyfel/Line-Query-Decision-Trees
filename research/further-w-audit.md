# Independent audit: polynomial general maximum-depth factor below 4.464966

Prepared 13 October 2026. This audits the capped exact interval-deadline dynamic program and hybrid maximum-depth construction proposed by the scheduling agent and root agent. No TeX files were edited by this audit.

## Audit conclusion

The proposed polynomial general-case theorem is valid: the hybrid algorithm has maximum depth at most **4.46496526 times optimum**. Its capped exact scheduler uses a rank-subset dynamic program with running time exponential only in the number of rank slots, which is a fixed constant times the logarithm of the global number of hypotheses. The existing polynomial scheduler covers instances whose optimum exceeds that threshold.

This is distinct from the earlier quasipolynomial multigrade program. It has no logarithmic exponent in the number of supplied queries.

## 1. Exact ordinary-interval scheduling with L rank slots

Number candidate block positions linearly. For a spatial region `[l,r]`, the relevant demands are exactly all original intervals whose endpoints are within that region. Define a state by this region and a subset `T` of available global ranks from `{1,...,L}`.

If the region has no demanded intervals, the state is feasible for every `T`; unused ranks can be discarded. If it has demanded intervals but `T` is empty, it is infeasible. Otherwise let `t=min(T)`. Choose any candidate `p` in the region at rank `t`. Reject if a demand containing `p` has deadline below `t`. Every other demand is wholly left or wholly right of `p`; partition `T\{t}` between the two child regions and require both resulting states to be feasible.

The state definition is exact. Every earlier queried separator lies outside a child region, so it cannot have hit an interval wholly within that child region. Conversely, a demand not hit by the new separator has both endpoints on one side. Thus no information about earlier choices is needed beyond the spatial region and its assigned rank subset.

Completeness follows by taking the earliest selected candidate in any feasible rank-labeled schedule. Its later selected candidates split spatially between the two sides, inducing exactly one tested rank partition. Soundness follows by combining two feasible child schedules with their parent candidate. Unused ranks or queries hitting no remaining demand can be deleted; compacting the surviving query ranks only improves deadlines.

There are `O(M^2 2^L)` states. Summing the rank partitions over all `T` costs at most `3^L`; including spatial choices gives `O(M^3 3^L)` combinatorial work, with additional polynomial demand scanning. For circular intervals, enumerate a forced first block, check its hit demands against rank one, remove them, and cut there. The remaining demands are ordinary intervals and use ranks `{2,...,L}`. The extra factor `M` preserves polynomiality.

## 2. Hybrid recursive construction

Let global input size be `n`, fixed throughout the entire recursion, and choose

```
L=ceil(2 log_2 n)+1.
```

A harmless fully integer variant is `L=2 ceil(log_2 n)+1`. Then `3^L=n^{O(1)}`.

Construct each hull-pattern child tree once, recording its actual height. At every flat state, search the original priority-greedy trials and the capped exact block-schedule trials, choosing the least feasible parent height. At balanced states use the existing balanced query. The original feasibility checks preserve

```
height(S)<=3 OPT_W(S)+floor(gamma log_2 |S|)
```

for every state, because improved actual child heights only make its trial budgets easier to meet.

There is also a restricted induction for every state satisfying `OPT_W(S)<=2 log_2 n`:

```
height(S)<=2 OPT_W(S)+floor(gamma log_2 |S|).
```

Every descendant also satisfies the threshold: restriction of an optimal identifying tree shows `OPT_W(A)<=OPT_W(S)`. Hence this restricted induction applies to all child codes used in its trial proof.

## 3. Exact block-trial feasibility

Use the existing rational maximum-depth parameters, which satisfy

```
gamma log_2(1/(1-delta))>1,
gamma log_2(1/delta)>5,
gamma=2.46496526.
```

Write `D=OPT_W(S)`, `s=|S|`, and `H*=2D+floor(gamma log_2 s)`. Balanced children fit because their sizes are at most `(1-delta)s` and the logarithmic potential pays their one query.

At a flat state, let class `A` have size `a`, and let `t_A` be its first supporting-hit index on an optimal witness path. Supporting-prefix credit gives `OPT_W(A)<=D-(t_A-1)`. A positive exit in actual block rank `k` has complete discovery-plus-decoding allowance at most

```
2k+floor(log_2(delta s/a))+3.
```

The first endpoint uses discovery `2k-1` plus the four-overhead endpoint allowance; the second uses discovery `2k` plus the pinned two-overhead allowance. Their maximum is the displayed expression.

The inductive child height leaves at least

```
H* - height(A) - floor(log_2(delta s/a)) - 3 >= 2 t_A
```

units of discovery budget. This follows from the same floor inequality as the original proof, with the potential gap at least `floor(log_2(delta s/a))+5`. Its integer block deadline is therefore at least `t_A`.

Replace the optimum witness queries by adjacent full-hull edge blocks containing their supports. The comparison covers every nonzero class by block `t_A`. If its nonzero terminal singleton remains unhit, append an incident edge. Its index is `q+1<=D+1<=L` and its prefix credit is `q`; no append is required when the zero class exists. Thus the exact capped scheduler has a feasible comparison.

When the zero class exists, its completed negative route has at most `2q<=2D<=H*` queries. When it does not exist, a completed negative cover is impossible. Origin endpoints and cached answers only reduce these lengths. The exact trial can therefore check and accept the concrete reconstruction without access to the optimal path.

## 4. Global factor

At the root, if `D<=2 log_2 n`, the restricted induction and binary information lower bound `D>=log_2 n` give

```
height<=2D+gamma log_2 n <=(2+gamma)D=4.46496526 D.
```

If `D>2 log_2 n`, the unrestricted original induction gives

```
height/D<=3+gamma log_2 n/D <3+gamma/2
                                    =4.23248263<4.46496526.
```

Thus both regimes satisfy the claimed polynomial factor. The exact scheduler, circular enumeration, trial-height loops, and the linear-size recursive stage hierarchy all have polynomial complexity. Its arithmetic uses integer deadlines and exact count ratios; logarithms are needed only in the proof and in integer power-of-two floor computations.

No hidden restriction on supplied-line directions, priors, cap size, or geometry was used. This result concerns maximum depth only; it does not itself provide a comparable expected-depth conversion.
