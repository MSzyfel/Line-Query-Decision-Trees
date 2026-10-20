# Two-selector obstruction to one-response greedy-code bundles

Auxiliary research note, 19 October 2026. The article is unchanged.

**Status: proved analytic obstruction.** The polynomial library that asks one
supplied test, decodes one chosen response with fresh uniform greedy, and stops
the other response has a full-order barrier in the mixed-credit stage
framework. This remains true when every pruning of every such template is
priced exactly. The result concerns that library, not the stronger global
lifting/intersection generator or arbitrary partial policies.

## 1. The family

For even `M>=16`, put

    ell=floor(M/(4 log2 M)),  rj=M-2j,  j=1,...,ell.

Let the hypotheses be the uniform product

    H=[M] times [M] times product_j [rj].

Call the first two coordinates selectors `x,y` and the remaining ones bodies
`zj`. Write `N=product_j rj`, `n=M^2 N`,

    e(r)=(r+1)/2-1/r,
    D=sum_j e(rj),
    H_eq=2(M-1)+sum_j(rj-1).

Supply all pure coordinate equalities. Also supply, for every selector pair
`b=(x,y)`, body coordinate `j`, and ordinary binary bit of `zj`, the test
positive exactly when the pair equals `b` and that bit is one. Put all pure
equalities before all gated tests in the input order. No selector-pair
membership test is supplied. There are `O(M^3)` tests and `log2 n=Theta(M)`.

Initial balance greedy uses only body equalities, starting with the smallest
body alphabet, then selector equalities. Gates have positive mass at most
`1/(2M^2)` initially, and after a body is fixed its gates are at most a
selector-pair point. Its incumbent `T` has average depth

    D+2e(M)=Theta(M^2/log M).                               (1)

A valid comparison first identifies both selectors with their equality
queries, then uses the now-active bits on all bodies. Its average cost is at
most `2e(M)+sum_j ceil(log2 rj)=O(M)`. Thus

    F_T/OPT=Omega(M/log M)=Omega(log n/loglog n).             (2)

The construction and its explicit response matrix have polynomial size. No
parameter-dependent horizon is enumerated.

## 2. The precise forbidden library and theorem

At the root, for each supplied query `q` and each nonempty response `C`, build
the actual template `q` followed by fresh balance greedy on `C`, stopping the
other response unresolved. Include **all prunings** of these at most `2m`
templates. A pruning may stop at any internal node. Let `P` be any nonempty
such policy; let `W(P)` be actual raw query work,

    Gamma_T(P)=F_T(H)-sum_output F_T(A),
    Delta_L(P)=L(n)-sum_output L(|A|),

where `L` is the exact unconstrained binary coding cost used in the preceding
notes. Define the rational constants

    r_min=M-2ell,
    c=2(ceil(log2 M)+4)/r_min,
    eta=H_eq/(2M^2),
    kappa=(ceil(log2 n)+1)/(2M^2),
    C_M=c(1+eta)+kappa=O(log M/M).                          (3)

**Theorem.** For all sufficiently large even `M`, every policy in this library
satisfies

    Gamma_T(P)<=W(P),
    Delta_L(P)<=C_M W(P).                                  (4)

Consequently, for any `0<=gamma<1,a>=0`, a stage satisfying
`W<=gamma Gamma_T+a Delta_L` requires

    a/(1-gamma)>=1/C_M=Omega(M/log M).                      (5)

This includes coefficients depending on `n`. If a certificate instead accepts
the incumbent, (2) requires its factor to have the same order. Thus neither
coefficient tuning nor exact prefix pricing of this library supplies an
unrestricted little-o guarantee through that certificate-or-stage framework.
The proof gives the first inequality in (4) already for `M>=16`; the
asymptotic qualification keeps the statement independent of loose small-case
constants.

## 3. A partial-policy entropy lemma for equality-only products

Consider a uniform independent product with coordinate sizes between
`r_min` and `M`. For **any** partial policy `R` using only pure coordinate
equalities,

    Gamma_T(R)=W(R),
    Delta_L(R)<=c W(R),                                    (6)

where `T` is any fixed product equality decoder. Its restriction to a
rectangular state of size `s` has cost `s sum_i e(si)`. A singleton query on an
`si`-element coordinate has exact credit `s`, proving the first identity by
telescoping.

Here is a self-contained proof of the coding inequality. A partial equality
search on a uniform `r`-element coordinate has `t` singleton exits and one
remaining cell, with `0<=t<=r-1`. Its entropy and expected queries satisfy

    H_t <= t(log2 r+log2 e)/r,
    Q_t = t-t(t-1)/(2r) >= t/2.

The entropy bound uses `-(1-u)ln(1-u)<=u`. Its expected number of positive
answers is `t/r<=2 Q_t/r`.

For an arbitrary adaptive product policy, condition on all coordinates except
`i`. Removing queries with now-deterministic answers induces just such a
partial equality search on coordinate `i`. Independence and the entropy chain
rule give

    H(transcript)<=sum_i I(Xi;transcript | all other coordinates).

Averaging the one-coordinate bounds proves
`n H(transcript)<=2(log2 M+log2 e)W/r_min`, and total raw positive-answer mass
`B<=2W/r_min`. At an equality query whose positive side has mass `b<=s/2`,

    L(s)-L(b)-L(s-b)<=s h2(b/s)+2b.

Indeed, the coding increments are at most `ceil(log2 s)+1` and
`L(b)>=b log2 b`. Summing and telescoping yields
`Delta_L<=nH(transcript)+2B<=cW`, with the slightly rounded constant in (3).
No independent entropy ledger is reset at different cores.

## 4. Pure equality root queries

After either outcome of one pure equality, the state is a uniform product.
At least one selector is still unfixed, with at least `M-1` possibilities.
While a body is unfixed, a body equality has minority at least `1/(M-2)`;
every selector query or gate has minority at most `1/(M-1)`. Thus fresh greedy
continues using body equalities. Once all bodies are known, each gate is zero
or a selector-context point, dominated or tied by a pure equality. The input
order resolves the ties. Fresh greedy on the chosen root response therefore
uses only pure equalities. Its entire template, and every pruning of it,
satisfies (6), hence (4).

## 5. Positive gated response

For a gate on body coordinate `j`, let `A` be its positive response and `a`
the number of positive values of that body coordinate. Every bit on an even
initial interval has `a<=rj/2`, so `|A|<=n/(2M^2)`.

Let `R_b` be the raw loss from deleting selector pair `b` from its product
equality code. Deleting one leaf gives `R_b<=2M-1`. Cancellation of all
unaffected body-coordinate costs gives the exact gate-query identity

    Gamma_T(q)=(N/rj)[a R_b+sum_(v in bitset) d_rj(v)-f(a)], (7)

where `f(r)=r e(r)` and `d_r` are equality-comb depths. As before,
`sum d_r-f(a)<=a(r-a)`. Thus `Gamma_T(q)<=3n/(2M)`.

Completing `A` can earn at most its entire remaining incumbent cost, which is
at most `|A|D`. Hence every pruning of the positive-response template has

    Gamma_T(P)<=n[3/(2M)+D/(2M^2)]=o(n),
    Delta_L(P)<=|A|(ceil(log2 n)+1)<=kappa n.                (8)

Any nonempty template pruning pays the root work `n`. This proves (4) in this
case. Neither bound assumes that fresh greedy on `A` is optimal.

## 6. Negative gated response: greedy remains equality-only

Write `B=H minus A`. After any sequence of body equality outcomes, every
selector pair except `b` retains the full remaining body rectangle; `b`
retains a possibly smaller part of that rectangle. Thus each pair has
posterior probability at most `1/(M^2-1)`. A selector equality has positive
probability at most `M/(M^2-1)`, and a gate at most `1/(M^2-1)`.

For an unfixed body, its values have multiplicities between `M^2-1` and `M^2`
after normalization by the remaining other-body volume.
There is a body equality with minority at least

    (M^2-1)/(M^2(M-2)) > M/(M^2-1).

For two remaining values use the smaller probability; for three or more,
the largest value probability is still below one half. The strict displayed
comparison follows from `(M^2-1)^2>M^3(M-2)`.
Greedy therefore asks only body equalities until all bodies are known.
Afterwards the selector state is a rectangle, possibly missing `b`. Gates
are singleton-pair queries. Any proper pure equality has integer minority
at least one, at least as much as such a gate; pure equalities win ties.
The full greedy code on `B` uses only equalities and has height at most `H_eq`.

## 7. Commuting the gate and an arbitrary pruned negative code

Fix any pruning of the code on `B`. Replay just its equality queries directly
on all of `H`, obtaining the legal partial policy `R` with output rectangles
`U`. Each original query has both `B` children nonempty, so replay creates no
missing-response issue. Write `W_B` and `W_A` for work contributed by `B` and
`A` in this replay. Then

    W(R)=W_B+W_A,  W_A<=|A|H_eq<=eta n,
    W(P)=n+W_B.                                            (9)

Commuting `q` and `R` gives the exact credit identity

    Gamma_T(P)=Gamma_T(R)+sum_U Gamma_T(q|U)-Gamma_T(R|A).

Restriction credit is nonnegative, so (6) implies

    Gamma_T(P)<=W_B+W_A+sum_U Gamma_T(q|U).                 (10)

If a replay leaf `U` still has an unknown body, no selector query has occurred
on its path. Its selectors are the full `[M]^2`; the same calculation as (7),
allowing any remaining bit subset, bounds its gate credit by `3|U|/M`.
If every body is known, at most one point of `A` lies in `U`. Deleting that
selector point from a rectangular selector code costs at most `2M`, even
after earlier selector exclusions. Distinct leaves contain distinct such
points. Consequently

    sum_U Gamma_T(q|U)<=3n/M+2M|A|<=4n/M.

Here `eta<=1/M+1/(8 log2 M)`, so
`eta+4/M<=5/M+1/(8 log2 M)<1` for `M>=16`.
Equations (9)-(10) therefore prove `Gamma_T(P)<=W(P)`.

For coding, the joint partition obtained by asking `q` at every `R` leaf
refines the outputs of `P`. Superadditivity of `L` gives

    Delta_L(P)<=Delta_L(R)+sum_U Delta_L(q|U)
               <=c W(R)+|A|(ceil(log2 n)+1)
               <=[c(1+eta)+kappa]W(P).

The middle inequality uses the largest coding increment and
`sum_U |A intersect U|=|A|`. This proves the second part of (4) without assuming
that `L` has nonnegative drops on an arbitrary invented decomposition: all
partitions and replays used here are actual policies, and `L` is superadditive.

## 8. Consequence and remaining scope

The useful global policy decodes **both** selectors before using body codes.
A single equality outcome leaves one selector unknown; a single gate outcome
can reveal both selectors, but only on `O(1/M^2)` probability mass. This is the
specific activation barrier missed by every template in the stated library.

The proof covers arbitrary nonuniform pruning depths, both responses of every
root query, actual outsider work, and exact incumbent restriction credit. It
also gives a fixed-point statement independent of the coding coefficient:
completing any permitted pruning by the actual incumbent restricted at every
exit costs exactly `F_T+W-Gamma_T>=F_T`. Thus this template neighborhood with
exact prefix optimization and incumbent fallback cannot improve its full-order
bad starting incumbent.

The theorem
does not cover unions or interleavings of templates, reoptimization of a
supplied palette, repeated global state synthesis, or the stronger frozen-source
lifting/intersection generator. No hardness or unrestricted approximation lower
bound is inferred.

The complementary `research-general-selector-replay.md` now proves that the
existing completed global-lifting pass repairs this private-context family:
a selector-only slice source exposes every full context, and its already
implemented fresh collision fallback supplies the fast body codes. No extra
source-harvest layer is needed. The bad fixed point above is restricted to
its specified smaller template neighborhood.

## 9. Both-response fresh-greedy templates also fail

The result extends to the larger neighborhood that forces any supplied root
query, attaches fresh greedy to **both** responses, and permits arbitrary
independent pruning on both sides. For a pure equality, the entire template is
still equality-only. For a gate, denote the positive and negative continuation
credits by `Gamma_A,Gamma_B` and their work by `W_A,W_B`. Section 7 gives

    Gamma_T(q)+Gamma_B<=W_B+n(eta+4/M).

The positive side earns at most `F_T(A)<=nD/(2M^2)`, even if its continuation
were chosen arbitrarily. Therefore total credit is at most

    W_B+n[eta+4/M+D/(2M^2)]<=n+W_A+W_B.

The last inequality holds for `M>=16`: `D<=ell M` bounds the bracket by
`5/M+1/(4log2 M)<1`. Adding the positive continuation spends at most `L(|A|)`
additional coding resource, so its counterpart of (3) is

    C'_M=c(1+eta)+2kappa=O(log M/M).

Thus all prunings of all these full forced-first-query templates have
`Gamma<=W`, admit the same asymptotic coding-coefficient barrier, and cannot
improve the incumbent under actual incumbent fallback. This extension does
not permit a second forced query before selecting the fresh greedy sources.

## 10. Bounded verification

`research-general-resolution-bundle-obstruction.py` constructs only the small
analogs `(M,bodies)=(6,(4)),(6,(4,2)),(8,(6))`, of sizes `144,288,384`.
It checks `856` root-response templates by exact bottom-up optimization over
**all** their prunings: maximum `Gamma-W` is zero, and the asserted rational
coding bound holds. It also checks the `428` full both-response templates of
Section 9 over all prunings. It separately checks `372` exact gate-credit identities,
the equality-only and body-before-selector behavior of every relevant greedy
source, and `1116` gate/replay commutation identities and bounds. No optimal
UDT oracle or random search is called.

These smaller examples are proof audits, not the growing family in Section 1.
In particular, many small templates still have positive
`(Gamma/2)+Delta_L-W`; the checker reports this openly. The theorem asserts
that their necessary coding coefficient grows in the prescribed asymptotic
family, not that a selected constant already fails on every small analog.

The actual prescribed family is checked only through exact alphabet/cost
formulas for `M=16,...,1024`. The largest `n` is represented by a `270`-bit
integer; its response matrix is never constructed. The analytic coefficient
`C_M` decreases from the loose small-case bound to approximately `0.02925`
at `M=1024`, while the guaranteed feasible-comparison gap grows. These finite
calculations verify the formulas; the asymptotic conclusion follows from the
proof above.
