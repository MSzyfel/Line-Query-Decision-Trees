# Global completion certificates and the missing code alternative

Auxiliary research note, 18 October 2026. Uniform hypotheses, supplied binary unit-cost tests, fixed-exponent polynomial time. No article files were edited. No unrestricted `o(log n/log log n)` approximation is claimed.

The main positive result here is a polynomial shared-budget LP whose output certifies the **full weighted completion-cover dual**, directly against incumbent depth prizes. It combines conditional coding certificates and endpoint-assigned separation pairs in one ledger. A rank-only partial-code DP is also derived and falsified as a tight general pricing surrogate. The missing unrestricted theorem is a precise code-or-certificate alternative stated below.

## 1. The algorithm-linked object

For an executable partial policy `P`, let `C(P)` be its globally identified hypotheses and `W(P)` its raw work. The exact completion-cover dual, already proved in `research-general-pricing-next.md`, is

```
y_h >= 0,
sum_{h in C(P)} y_h <= W(P)       for every original-test P.       (1)
```

Its maximum objective is `OPT_G`. Given a complete incumbent `T`, put `w_h=d_T(h)`. A feasible `y` satisfying `y_h>=w_h/alpha` for every hypothesis proves `G(T)<=alpha OPT_G`. This is a global certificate. It is not a lower bound restarted at recursive states.

The same earlier note proves that an `alpha`-approximate weighted completion pricer would yield an `alpha`-approximation through strict integer descent. This note constructs a useful, verifiable part of the dual side of that alternative.

## 2. Uniform completion resources compose into the full dual

A resource `A subseteq H` has a certified uniform completion price `lambda_A` if, for every partial policy restricted to `A`,

```
retained raw work on A >= lambda_A * |C(P) intersect A|.           (2)
```

Restrictions suppress locally constant queries. An output that is singleton locally but unfinished globally may remain unrewarded. This convention matters: a bound only on the full identification cost of `A` does not automatically imply (2).

Set `kappa_A(q)=1` if the original test is nonconstant on the full resource `A`, and zero otherwise. The retained work on `A` is at most the work of all `A`-hypotheses on queries with `kappa_A(q)=1`.

For each pair `uv`, introduce weight `p_uv>=0`, query-specific first-separation allocations `f^q_(uv,u),f^q_(uv,v)>=0`, and completion-prize allocations `pi_(uv,u),pi_(uv,v)>=0`. Require

```
f^q_(uv,u)+f^q_(uv,v) >= p_uv     whenever q(u)!=q(v),
pi_(uv,u)+pi_(uv,v) <= p_uv.                                      (3)
```

Choose resource coefficients `z_A>=0`, with common query capacities

```
sum_{A:h in A} z_A kappa_A(q)
 + sum_{g:q(g)!=q(h)} f^q_(hg,h) <= 1       for every h,q.          (4)
```

Define

```
y_h = sum_{A:h in A} z_A lambda_A + sum_g pi_(hg,h).                (5)
```

**Global completion-certificate theorem.** Every `y` from (2)–(5) is feasible for (1).

For a partial policy `P`, every pair with at least one completed endpoint has already been separated. Charge its weight once, at its first common separating query. The prize assigned to its completed endpoints is at most its weight by (3), whether one or both finish. Allocate this charge to the two endpoints using that query's `f` values. Separately, (2) pays all completed resource prizes. At every actual query node, the combined charges are bounded by its population using (4). Summing all nodes yields `y(C(P))<=W(P)`.

This strengthens the interpretation of the old activation ledger: pair prices may be distributed among incumbent-depth coordinates, and uniform coding resources price partial completion rather than only full-tree cost.

### A polynomial LP that certifies an incumbent

For a polynomial list of verified resources and rational prices, add

```
sum_{A:h in A} z_A lambda_A + sum_g pi_(hg,h) >= theta w_h
                                                      for each h,
```

and maximize `theta`. Constraints (3)–(4) and these domination inequalities form a polynomial-size ordinary LP. A solution with `theta>=1/alpha` is an explicit full completion-dual certificate for `T`.

Rational conservative prices avoid any precision issue. For example, the saturated-flat resource below permits `lambda_A=Qd/3`, since `e<3`; binary entropy resources permit `floor(log_2 |A|)`. Query capacities and prizes share one ledger, so neither nested resources nor many activation levels cause repeated charging.

The resource list can be enlarged automatically by adding supplied test outcome cells, incumbent node sets, and incumbent depth level sets, then checking available certificates on those sets. This is polynomial for a fixed polynomial list. No proof says that this list is sufficient for arbitrary instances.

## 3. Verifiable uniform completion prices

**Entropy.** Every binary partial policy on `A` has work at least `k log_2|A|` when it finishes `k` designated hypotheses: its output partition contains those singleton cells, and the partition entropy lower-bounds query work. Other singleton outputs may be ignored. Thus `lambda_A=log_2|A|`, or a rational lower approximation, satisfies (2).

**Singleton systems.** When every nonconstant query on `A` isolates at most one hypothesis, the uniform completion price is the full singleton-search mean

```
lambda_A = [|A|(|A|+1)/2-1]/|A|.
```

For a proper partial singleton search finishing `k<|A|` hypotheses, its work is at least `k|A|-k(k-1)/2`, which is no smaller than `k lambda_A`; the full search attains equality. The singleton convention forces the final remaining hypothesis to finish as well. This includes a missing private singleton for an all-negative witness.

**Saturated affine-flat resources.** The root agent's independent entropy proof in `research-general-capacity-pricing.md` gives the following price. Suppose resource columns are distinct vectors with first coordinate one, rank `d+1`, over `F_Q`; every restricted positive test support is a represented-matroid flat; and `|A|=Q^d`. Then

```
lambda_A = Qd/e                                                   (6)
```

is a valid uniform completion price, even if the supplied tests do not preserve any transitive group.

For completeness, the mechanism is genuinely global. Let the output cells of a partial policy have mass `m`, and let `p` count their positive answers. Their remaining span rank gives `m<=Q^(d-p)`. If `k` designated targets finish, put `L=kd+B_unfinished`, where `B_unfinished` is positive-answer work on all unrewarded outputs. Output entropy is at least `L log_2 Q`; total positive-answer work `B` is at most `L`. Jensen gives

```
H_output <= W h_2(B/W) <= B log_2(eW/B).
```

Also `H_output<=W` and `Q>=2`, so `L<=W`. Monotonicity in `B<=L<=W` yields `L log_2 Q <= L log_2(eW/L)`, hence `W>=(Q/e)L>=(Qd/e)k`. Locally singleton but globally unfinished cells satisfy the same cardinality inequality and may be included among unrewarded outputs, so (2) survives restriction from a global partial policy.

This uses the compact flat certificate from `research-general-information-next.md`, verified by Gaussian elimination. It avoids finite-state span enumeration. Low-rank certificate discovery is still not supplied.

## 4. Rank-only abstract pricing: a valid DP and a sharp limitation

Let every proper path have at most `d` positives or predictor mistakes. An actual unfinished output state cannot have zero remaining budget: if it contained two distinguishable hypotheses, a further splitting query could cause another positive/mistake answer. Thus a live unfinished state requires at least one remaining unit.

To lower-bound the work of a partial policy finishing `k<n` hypotheses, retain all finished leaves and one shallowest unfinished leaf, remove the other unfinished leaves, and assign total unfinished mass `n-k` to the retained one. The resulting abstract code has no larger work and preserves the positive budget. Its live heavy leaf has at least one remaining unit. It can be extended by a rank-one comb, so this abstraction does not silently place live mass at remaining budget zero.

Let `M_d(s)` be the old exact full rank-limited coding cost. Let `A_d(k,u)` be the optimum abstract work for `k` unit finished leaves and one unfinished leaf of mass `u>=2`. Bases are

```
A_0(k,u)=infinity             for every k>=0,
A_d(0,u)=0                   for d>=1.
```

The recurrence is

```
A_d(k,u)=k+u+min{
    A_(d-1)(a,u)+M_d(k-a)          : 0<=a<k,
    M_(d-1)(a)+A_d(k-a,u)          : 1<=a<=k }.
```

Evaluate budgets and light-leaf counts in increasing order. For all `u+k<=n`, this costs `O(dn^3)` arithmetic operations. Fully completed `k=n` uses `M_d(n)`; `k=n-1` cannot occur under mandatory singleton completion.

For arbitrary incumbent prizes, let `W_k` be the sum of their `k` largest values. Every executable pricing density is at least

```
beta = min_{k in {1,...,n-2,n}}
          [A_d(k,n-k)/W_k],                                      (7)
```

using `M_d(n)` at `k=n`. Consequently `beta>=1/alpha` is itself a full completion-dual certificate for incumbent prizes scaled by `alpha`. It is a polynomial lower bound on pricing, not an executable pricer: its abstract splits do not become legal original tests merely because they optimize the DP.

### Why root rank alone is insufficient

Even with the live-leaf convention, this partial density need not be close to the full rank-limited mean. For `d=2`, put the unfinished heavy leaf on the positive branch, retaining budget one, and identify `k` unit leaves on the negative branch with budget two. Its work is at most `n+M_2(k)`. The sequential capacity and an elementary grouping construction give `M_2(k)=Theta(k^(3/2))`. Choosing `k=Theta(n^(2/3))` gives density `O(n^(1/3))`, whereas `M_2(n)/n=Theta(sqrt(n))`. Their ratio therefore has gap `Omega(n^(1/6))`.

Exact checks show the onset:

| n | Minimum abstract partial density | Complete mean |
| --- | --- | --- |
| 64 | 8 | 67/8 |
| 128 | 368/37 | 1479/128 |
| 256 | 828/67 | 16 |

These values falsify the tempting claim that uniform abstract partial density always equals the complete rank-limited mean. Small tests through `n=30` missed the gap.

If one additionally bounds every state size by `B_b` at remaining budget `b`, merging all unfinished leaves into one may violate that capacity. The correct abstraction instead keeps a finish-count DP `C_b(s,k)`, allowing a zero-work stop at a nonsingleton and forcing a singleton to finish. Its continuation recurrence is

```
C_b(s,k)=s+min_(a,j)[C_(b-1)(a,j)+C_b(s-a,k-j)],
```

with `s<=B_b` and `a<=B_(b-1)`. Straightforward computation is polynomial `O(dn^4)`; fixed-price profit optimization takes `O(dn^2)`. The independent root script `research-general-capacity-pricing.py` implements this stronger abstraction. Geometric capacities `B_b=Q^b` still do not imply equality for arbitrary unsaturated `n`: `Q=256,d=2,n=256` reproduces the rank-only counterexample. The saturated case instead has the analytic constant price (6).

## 5. Concrete benchmark certificates and executable codes

**Singletons.** A singleton-search tree has maximum depth `n-1`. The exact uniform completion resource above has price roughly `n/2`, so one root resource certifies domination with `alpha=2`.

**Affine equality.** Coordinate equality search has maximum depth `d(Q-1)`. A saturated root resource with rational price `Qd/3` certifies every incumbent depth divided by three. These are actual original-test coordinate searches in the classical family; no abstract split is used as a query.

**Gated grid and arbitrarily many activation levels.** Use the factored source from the existing activation note,

```
H=[C_1] x ... x [C_L] x {0,1}^b,
```

with supplied prefix selectors and gated core tests. Let `A_i` be each full gate fibre. Give it entropy completion price `b`, coefficient one. Give pair weight one to each pair sharing its core row and differing in exactly one gate coordinate. At each separated pair assign its entire first-separation query charge to the endpoint outside the active prefix; every outside endpoint has at most one neighbor inside. Active fibres spend their one unit on the core query, while selectors are constant on them. Thus (4) holds.

Split each pair's completion prize equally between its endpoints. Then every hypothesis receives

```
y_h=b+(1/2)sum_j(C_j-1).
```

The explicit sequential selector/coordinate-code tree has depth at most `b+sum_j(C_j-1)`, hence `w_h<=2y_h`. This gives a full weighted completion-dual certificate with `alpha=2`, independent of the number of activation levels. For a saturated affine core in place of the Boolean core, the same construction with `Qd/3` gives `alpha=3` for coordinate equality continuations.

For the classical bad row-first grid incumbent, the certificate need not dominate its large depth prizes. The other side of the alternative is constructive: ask a column test, completely decode its positive row cube with the supplied gated bits, and leave the miss branch unfinished. Its work is `r(C+b)`, while its reward from the bad incumbent's depths is `r(C_R+d_column)`. In the full-order trap `C_R=Omega(b^2/log b)` and `C=b`, this is strictly profitable for large `b`. Exact prefix mining of the complete activated-code template finds at least this policy. Thus the pricing alternative passes this bad-incumbent stress test as well as the already-good trees above.

## 6. The precise missing unrestricted dichotomy

All steps on either side below are concrete polynomial operations once the listed representations/codes are available:

1. Generate a polynomial family of actual complete conditional codes. Mine their independently stopping prefixes by the exact weighted closure DP from `research-general-pricing-next.md`.
2. Generate a polynomial family of uniform completion resources, verify their entropy/singleton/flat certificates, and solve the shared-budget domination LP (3)–(5).
3. If a mined prefix has reward greater than work, append the incumbent restrictions and accept the strict integer improvement. Otherwise use a domination solution to certify the incumbent.

A universal `alpha` guarantee would follow from the following **unproved** alternative: for every incumbent reached by the generator, either a mined original-test prefix has strictly positive profit, or the shared-budget LP dominates every incumbent depth with factor `alpha`. A polynomial number of successful improvements then suffices by integer descent, while the LP handles the terminating case globally.

The tests above establish this alternative only for specified benchmark constructions. They do not prove it for arbitrary matrices, nor show how to synthesize low-rank flat representations or the needed conditional resources. In particular, Littlestone dimension is a maximum over adaptive witness trees, whereas UDT optimizes a minimum-cost identifying policy; hardness of approximating the former in [Manurangsi–Rubinstein](https://proceedings.mlr.press/v65/manurangsi17a.html) is a limitation on that synthesis approach, not an approximation-hardness result for UDT.

## 7. Checks

`research-general-certificate-algorithm.py` passed:

* exact abstract work and weighted-density inequalities against all distinct completion sets of 45 small original-test instances;
* shared query capacities and incumbent-prize domination on four gated/nested activation matrices, including four activation levels;
* rational affine-price domination on three parameter choices;
* the three rank-only partial-density counterexamples above.

The checker does not solve the shared-budget LP numerically: it verifies the explicit feasible ledger just proved. It does not enumerate exponentially many states as an implementation of the proposed general algorithm; exhaustive small-state enumeration is used only to audit the pricing lower bound.
