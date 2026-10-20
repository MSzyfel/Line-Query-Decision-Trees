# Exact hierarchy resolution, coding, and activation bundles

Auxiliary research note, 19 October 2026. The article is unchanged.

**Status.** A natural polynomial greedy rule maximizing exact incumbent
restriction credit plus integer coding drop has a full-order
`Omega(log n/loglog n)` gap. More generally, a certificate-or-stage scheme
restricted to one-query stages cannot improve that bound within the shared
coding-ledger analysis. A polynomial `2m` library of actual one-response
conditional-code bundles escapes this obstruction on the same family. This
library is already included in earlier forced-child source generation; the new
point here is its exact mixed-credit comparison. No unrestricted approximation
improvement is proved.

## 1. A precise mixed greedy rule

Fix an actual incumbent `T`. At a current state `S`, let

    Gamma_T(q|S)=F_T(S)-F_T(S intersect q)-F_T(S minus q),
    Delta_L(q|S)=L(|S|)-L(|S intersect q|)-L(|S minus q|),

where `F_T` is the raw cost of the actual pruned incumbent, and

    L(s)=s(ceil(log2 s)+1)-2^ceil(log2 s),  L(0)=L(1)=0.

Choose a proper query maximizing `gamma Gamma_T + a Delta_L`, with the original
test order breaking ties; recurse on its actual outcomes. Query work is `|S|`,
so dividing this score by work does not change the choice. The score is exactly
computable in polynomial time. Allow `gamma>=0` and `a>0`, including coefficients
chosen separately at each state.

Use the serial product family proved in
`research-general-recursive-lifting.md`: strictly decreasing even alphabets
`M0>...>ML>=6`, all pure coordinate equalities, and coordinate bits gated by the
full lower-coordinate context. Tests are ordered by ascending coordinate, with
bits before equalities within a coordinate. The incumbent is ordinary balance
greedy, which decodes all coordinates by equalities in reverse order. Write

    e(r)=(r+1)/2-1/r,
    f(r)=r e(r)=r(r+1)/2-1,  f(0)=f(1)=0.

## 2. Pareto dominance forces the same bad policy

At every state reached by the reverse-equality policy, higher coordinates are
fixed, one coordinate has `r` remaining values, and all lower coordinates are
uniform products. Every proper pure equality query has

    Gamma_T(q|S)=|S|.                                      (1)

Indeed, restricting the equality comb on an `r`-element coordinate gives the
same optimal equality comb on either subset, and
`f(r)-f(r-1)=r`. Contributions of other coordinates add unchanged across the
two query outputs.

Every gated query has credit at most `|S|` as well. The following calculation
also covers bit subsets that become biased after earlier equality exclusions.
Suppose a gate fixes a lower context in a product of size `p`, then selects a
subset `A` of `a` values of its current `r`-element coordinate. Here `p>=r`.
Let `R_b` be the raw cost lost from the lower equality code when deleting its
one context `b`, and let `d_r(v)` be equality-comb depths. Per independent
higher-coordinate copy, its credit is exactly

    a R_b + sum_(v in A) d_r(v) - f(a).                     (2)

Deleting a lower-product leaf gives
`R_b=M0+sum_(j>=1 below the gate) d_Mj(bj)<=p`.
For an equality comb, selecting the `a` deepest leaves shows

    sum_(v in A) d_r(v)-f(a)<=a(r-a).

Thus (2) is at most

    ap+a(r-a)<=pr,                                         (3)

because `(p-a)(r-a)>=0`. A gated test on an already fixed higher coordinate is
either constant or a single remaining lower-context indicator; the same bound
applies. At coordinate 0 it is merely a pure singleton partition, which loses
the tie to the earlier coordinate-0 equality test.

The most balanced remaining equality also maximizes the integer coding drop.
For completeness, `L(s)-L(s-1)=ceil(log2 s)+1` for `s>=2`. Therefore
`L(n)-L(t)-L(n-t)` is nondecreasing up to `n/2`, and strictly increasing up to
`n/3`. While coordinate `i>=1` is searched, every competing query other than
its remaining pure equalities has minority at most `1/6` and strictly below
their `1/r`.
Strictness in the first third, followed by monotonicity, removes possible flat
coding-drop ties near one half. Within coordinate 0 the only tied gated
partitions are its singleton aliases and lose the specified input-order tie.
Equalities on different remaining values of the current coordinate tie each
other and retain the original value order, exactly as ordinary greedy does.

**Theorem 1.** For every `gamma>=0,a>0`, the mixed greedy rule makes exactly the
same choices as ordinary balance greedy on this family. It remains true for
state-dependent coefficients with these signs. Thus a monotone myopic mixture
of the two exact resources does not repair the greedy obstruction.

Take `L=floor(M/log2 M)` and `Mk=M+2(L-k)` for even growing `M`. The incumbent
has average cost `Theta(M^2/log M)`, while the executable context-first code has
cost `O(M)` and `log2 n=Theta(M)`. Hence the mixed greedy rule has approximation
gap `Omega(log n/loglog n)`.

## 3. A quantitative barrier to one-query stage coverage

At the root every positive support has size at most `n/M`, with `M=ML`, and
every query has credit at most `n`. For a positive side of size `b<=n/M`,

    Delta_L <= b(log2(n/b)+2)
            <= (n/M)(log2 M+2).                            (4)

The first inequality uses `L(b)>=b log2 b` and the largest coding increment
`ceil(log2 n)+1`; the second follows by monotonicity on `b<=n/2`.

A one-query stage of work `n` satisfying

    W<=gamma Gamma_T+a Delta_L,  0<=gamma<1,

therefore requires

    a/(1-gamma)>=M/(log2 M+2).                             (5)

If a terminal certificate instead accepts this incumbent, its factor must be
at least the incumbent's `Omega(M/log M)` gap. Thus any universally valid
certificate-or-stage method using only one-query stages inherits the baseline
order in either its certificate factor or its coding-ledger coefficient.
Taking `gamma` close to one does not evade (5). This is a restriction on that
proof/algorithm class, not hardness of UDT or of larger executable stages.

## 4. Exact resolution utility is not adaptively submodular

For a fixed target `h`, one incumbent ancestor is resolved only after all
opposite-child rivals have been excluded. Exact resolution is therefore an
AND-completion objective. Its conditional expected marginal is
`Gamma_T(q|S)/|S|`.

There is an explicit violation of diminishing returns in this same family.
Let `q` be the LSB test of coordinate 1 gated by `x0=b`, and let `s` be the pure
selector `x0=b`. Before observing `s`,

    E[marginal of q]=1/2+(M1+2)/(8M0).

After observing its positive response,

    E[marginal of q | s=1]=M1/4+1/M1.                       (6)

The latter is strictly larger, and its ratio grows with `M1`. The first value
follows from (2), using `a=M1/2` and the odd-value comb depths; the second is
`[f(M1)-2f(M1/2)]/M1`.

The direct utility consequently does not satisfy the conditional diminishing
returns used by [Golovin and Krause's adaptive-submodularity theorem](https://arxiv.org/abs/1003.3967).
Likewise, [adaptive submodular ranking](https://arxiv.org/abs/1606.01530) assumes
scenario submodular coverage functions; calling the present AND-completion
credit a coverage function does not establish that hypothesis. This does not
rule out a different submodular surrogate or a new comparison theorem.

## 5. A concrete polynomial activation-bundle score

For every proper supplied query and each of its two responses `C`, build an
actual partial template: ask that query, run fresh uniform greedy to completion
on `C`, and stop its other output unresolved. There are at most `2m` such
templates, each with `O(n)` nodes. Its exact full-template statistics are

    W=|S|+F_greedy(C),
    Gamma_T=F_T(S)-F_T(S minus C),
    Delta_L=L(|S|)-L(|S minus C|).                          (7)

Their score `gamma Gamma_T+a Delta_L-W` is polynomially computable. Every
pruning of a template can also be priced exactly: assign terminal energy
`Phi(A)=gamma F_T(A)+a L(|A|)` and use the bottom-up recurrence
`min(Phi(A), |A|+sum_child value)`. This evaluates actual restrictions and
actual query work. These conditional source codes are inherited from the
earlier `source_codes` generator, rather than a new source class.

On the serial family choose `C={x0=b}`. Fresh greedy on `C` decodes the remaining
coordinates in forward order using their active gated bits. The least free
binary coordinate gives minority at least `1/3` under any partial bit pattern;
higher equalities have minority at most `1/6`, and higher gates must first guess
the present value. The factor priority handles small ties. This proves

    W<=n+(n/M0) sum_(j=1)^L ceil(log2 Mj),
    Gamma_T=n+(n/M0) sum_(j=1)^L e(Mj).                     (8)

The first `n` units of credit come from the selector query; completely
identifying its positive child earns the displayed remaining incumbent cost.
On the growing family, `W=O(n)` and
`Gamma_T=Theta(n M/log M)`. Hence this generic `2m` bundle library contains a
stage satisfying `W<=gamma Gamma_T` for every fixed `gamma>0`, for all
sufficiently large `M`. It escapes the one-query mixed-score barrier without
spending any coding resource.

There is also a smaller explicit bundle: after the selector, decode only the
next fixed `t` coordinates. Its work and credit obey (8) with sums through `t`,
so `Gamma_T/W -> 1+t/2`. Any fixed
`t>2(1/gamma-1)` suffices eventually. Its actual conditional code has
`O(M^t log M)` nodes on this family; the growing bit depth is not being
enumerated as all possible test sequences.

Equation (8) is a family-specific coverage theorem for this simple bundle
score, not universal coverage. The full first-pass quadratic-lifting theorem
already provides a stronger complete-tree guarantee for this family.

The follow-up `research-general-resolution-bundle-obstruction.md` proves that
this `2m` library itself has a full-order bad fixed point on a different
two-selector family, even with exact pruning and actual incumbent fallback.
Thus the positive serial-family calculation in (8) does not establish global
coverage of these bundles.

## 6. Bounded checks

`research-general-resolution-greedy.py` checked every incumbent node and every
proper supplied test for `n=48,80,480`: 17,246 exact credit comparisons and
4,840 mixed-action choices over eight coefficient pairs. Every mixed action
matched ordinary greedy. It checked 26,600 strict integer-coding increments,
both values in (6), and actual execution/credit of the activation bundles.
For `n=480`, the full conditional bundle has work `752` and credit `850`.
Algebraic growing-family checks through `M=512` construct only alphabet lists
and large integers, not their enormous response matrices. No exact optimum
oracle or random adversarial search is used.
