# Target cohorts: a logarithmic cover gap alongside easy density pricing

Auxiliary research note, 18 October 2026. The article is unchanged. This does not establish an improved approximation for unrestricted uniform decision trees.

The exact full completion-cover LP from [the pricing note](research-general-pricing-next.md) has a useful but limited scope: **all hypotheses** are required to be identified. Requiring only a designated target cohort while still charging queries on outside hypotheses gives a different optimization problem. This note proves a logarithmic integrality gap for its analogous covering LP. On the same construction, a simple polynomial weighted density pricer is nearly optimal. Thus the gap concerns converting fractional target covers to one integral target policy, rather than an inherent difficulty of density pricing.

## 1. Target completion and its covering LP

An executable partial policy may stop unfinished on nonsingleton cells. Let `C(P)` be its singleton outputs and `W(P)` its raw work over **every** hypothesis. For a requested cohort `D`, define

    ell(D) = min { W(P) : D subset C(P) }.

Consider the LP with one variable for every executable partial policy:

    minimize sum_P W(P) x_P,
    subject to sum_(P:h in C(P)) x_P >= 1  for h in D,
               x_P >= 0.                                     (1)

The integer covering optimum equals `ell(D)`. A single cheapest partial policy is an integer cover. Conversely, execute a chosen integer collection sequentially, restricting each program to actual current cells and suppressing determined queries. Conditioning and shared observations do not increase its aggregate raw work, and every required target is eventually identified. This gives one policy costing at most the integer cover.

For `D=H`, the earlier optimal-depth dual proves LP exactness. For proper cohorts, that argument cannot allocate all work to the requested hypotheses: outside hypotheses also incur query costs. In fact (1) can have a logarithmic gap.

## 2. A uniform construction retaining a large outside population

Start with an arbitrary finite set-cover system on `N` target elements, with caps `S_i` covering the target universe `C`. Make each cap a binary supplied test, positive exactly on that cap. Add every target singleton test. Add `u` distinct outside hypotheses, all answering zero to all target tests, and one positive singleton test for each outside hypothesis. The complete response matrix separates every hypothesis; costs and probabilities are uniform. There are `n=N+u` hypotheses and `m<=m_set+n` binary tests.

For `D subset C`, let `tau(D)` be its minimum cover size using the original caps. Added target singletons do not change this number: replace any chosen singleton by an original cap containing its element. Assume `u>=2N`.

**Set-cover sandwich.**

    u tau(D) <= ell(D) <= u tau(D)+2N^2.                       (2)

For the lower bound, follow the path that answers zero to every target query and every outside singleton query. Before it stops, let `s` be the number of distinct outside singleton queries and `t` the number of target queries. Proper policies do not repeat determined tests.

If `s<u`, an unprobed outside hypothesis follows this entire path. Any requested target never hit positively by a target query follows it as well, and therefore could not be identified. Consequently the target queries cover `D`, so `t>=tau(D)`. Charge only work performed on outside hypotheses. The `u-s` unprobed outsiders incur every target query. The outside probes themselves cost at least `u+(u-1)+...+(u-s+1)` on outsiders. These are disjoint query types, giving

    W(P) >= (u-s) tau(D)+s(2u-s+1)/2
         = u tau(D)+s[u-tau(D)-(s-1)/2]
         >= u tau(D).

The last inequality uses `tau(D)<=N` and `u>=2N`. If instead `s=u`, outside probes alone cost `u(u+1)/2>=uN>=u tau(D)`. This also covers policies that try to identify the last target by eliminating every outsider.

For the upper bound, ask an optimal `tau(D)`-cap cover on its all-negative spine. On each positive exit, identify all targets there with supplied singleton tests; the exits are disjoint. Stop the final negative state unfinished. Outside work is `u tau(D)`. Target work on the spine is at most `N tau(D)<=N^2`, and all positive exit decoders together cost at most `N^2`. This is an executable original-test policy and proves (2).

## 3. An explicit logarithmic gap, without a hardness assumption

Take target hypotheses to be the `k`-element subsets of `[r]`. Thus `N=binom(r,k)`. For each `i in [r]`, supply the cap

    S_i = { A subset [r] : |A|=k and i in A }.

A chosen set of indices covers all target hypotheses exactly when its complement contains fewer than `k` indices. Hence

    tau(C)=r-k+1.                                             (3)

For each cap, execute its membership query and then decode its positive targets by singleton tests. Its work is

    u+N+f(|S_i|),
    f(s)=s(s+1)/2-1  for s>=1.

Assign `x_i=1/k` to these `r` executable partial policies. Each target belongs to exactly `k` caps, so this is a feasible fractional solution of (1). It has cost at most `(r/k)(u+2N^2)`. By (2)-(3), the integer optimum is at least `u(r-k+1)`. Therefore

    integer optimum / LP optimum
      >= [k(r-k+1)/r] [u/(u+2N^2)].                           (4)

Choose `k=floor(r/2)` and `u=N^3`. The right side is `Omega(r)`. Since `log N=Theta(r)` and `n=N+N^3`, this is `Omega(log n)`. The instance has `m=O(n)` explicit binary tests. Large symbolic rows in the checker evaluate (4) and the sharper displayed one-cap cost; they do not claim to materialize or solve these large matrices.

This is an integrality gap for **target-only** completion covering. It does not contradict exactness when every outside hypothesis must also be identified. In cooperative-game language, the full completion-cost game has an optimal-depth core allocation, but its restricted target subgames need not have a nonempty core; the family is not totally balanced.

A small exact illustration uses three targets, pair caps `{a,b}`, `{a,c}`, `{b,c}`, and `u` outsiders. For `u>=8`, `ell(C)=2u+6`, while each pair costs `u+5`. Weighting the three pair policies by one half costs `3(u+5)/2`, giving a gap approaching `4/3`.

## 4. The density pricer is nevertheless nearly exact here

The LP agent independently audited (2)-(4) and found the following positive counterpart. Give arbitrary nonnegative prizes `w_h` to the targets and zero prize to outsiders. Let

    B=max_i sum_(h in S_i) w_h.

If `B>0`, every executable partial policy satisfies

    W(P) >= (u/B) sum_(h in C(P) intersect C) w_h.              (5)

This holds for every `u>=1`; the stronger outside-size assumption is unnecessary for (5).

Here is an explicit shared pair ledger. For each target/outside pair `(h,o)`, assign charge `w_h/B`, entirely to completion of target `h`. Identifying `h` must separate it from all `u` outsiders, yielding its total charge `u w_h/B`. Charge each pair at its first common separating query. At a target-cap query, put the pair charge on its outside endpoint: each outside hypothesis receives total load at most `w(S_i)/B<=1`. A target singleton has the same property because it is contained in an original cap. At an outside singleton query, charge each separated pair to its target endpoint, whose load is `w_h/B<=1`. Thus each query's pair charges are at most its actual population cost. Summing proves (5). This is a feasible instance of the existing pair completion ledger, not a newly stronger causal relaxation.

Choose a cap with prize `B`, ask it, and decode its positive targets by singleton tests. The policy finishes prize `B` at work

    u+N+f(|S_i|) <= u+N^2.

Together with (5), this is a polynomial `(1+N^2/u)` approximation to the best target-only weighted density. At `u=N^3`, the factor is `1+1/N`. The zero-prize case has no nonempty positive-reward pricing candidate.

This near-exact pricer coexists with the `Omega(log n)` integral target-cover gap. Hence that gap is neither pricing hardness nor a lower bound against the full uniform decision-tree approximation. It specifically prevents treating fractional covers as exact costs of arbitrary requested cohorts with outsiders still present.

## 5. Implication for the general search

The exact full completion-cover formulation remains a sound route to a general approximation via incumbent-depth weighted pricing. The construction gives no obstruction to that theorem. It does show why recursive code assembly must retain the actual outside population and cannot replace a requested partial code by the fractional covering value of its targets. Actual activated frontier cells, whose entire live population is relevant, avoid this particular mismatch.

The near-exact target pricer also supplies a useful comparison case for future candidate algorithms: they should recognize a dense cap and retain its legal positive decoder, without first solving the hard integral cover of all targets. Extending that principle to overlapping adaptive continuations, with a shared global ledger, remains unresolved.

## 6. Finite validation

[The checker](research-general-target-coalitions.py) compares an exact DP exploiting outsider symmetry with an independent full-mask Bellman optimizer on 125 small target-cohort cases. It checks the set-cover sandwich and executes the actual cover-spine decoder on all 125 cases. It also checks 119 weighted pricing cases against exact target-subset density optimization and verifies the pair-ledger endpoint capacities, plus 120 explicit central-cover combinatorial identities. Four triangle instances have exact cohort and fractional-cover costs saved.

Subset and coalition enumeration are validation only. The positive max-prize-cap pricer uses only scanning the explicit cap family and constructing supplied singleton decoders. [Results](research-general-target-coalitions-results.json) distinguish symbolic asymptotic bounds from actual small-instance optimization.
