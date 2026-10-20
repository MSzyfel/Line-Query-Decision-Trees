# General UDT: exact completion LP and polynomial code synthesis

Research notes, 2026-10-18. The article is unchanged. Hypotheses are
equiprobable, supplied tests have unit cost, and all costs below are raw
external path lengths. Results are supplied with proofs; literature-wide
novelty is not asserted.

**Main progress:** an exact covering LP for UDT and a weighted completion
pricing reduction with no approximation loss. A polynomial `alpha`-oracle
for the stated weighted partial-policy problem would give a polynomial
`alpha`-approximation for UDT by strict integer descent. The oracle is not
assumed solved. There is also an implemented fixed-exponent polynomial
code generator with exact prize-work separation on its represented states.
No unrestricted `o(log n/log log n)` guarantee is proved.

## 1. Partial policies and an exact completion LP

A partial policy is a legal finite test tree whose leaves are either
identified single hypotheses or unresolved candidate sets. Its nonempty
leaves partition the original hypothesis set `H`. Let `C(P)` be the set of
hypotheses identified by partial policy `P`, and let

```
W(P) = sum_(internal v in P) |S_v|
```

be its actual raw work. Queries made only on one outcome branch are
charged only for hypotheses reaching that branch. Root-only and uniform
depth truncations are not the only allowed policies.

Consider the finite, exponentially large LP

```
minimize    sum_P W(P) x_P
subject to  sum_(P:h in C(P)) x_P >= 1       for every h in H,
            x_P >= 0.
```

Its dual is

```
maximize    sum_h y_h
subject to  sum_(h in C(P)) y_h <= W(P)      for every partial policy P,
            y_h >= 0.
```

**Exactness theorem.** Both optimal LP objectives equal the raw optimum
`F_OPT` of the uniform decision-tree instance.

**Proof.** A complete optimal tree is one primal column covering every
hypothesis at cost `F_OPT`, so the primal is at most `F_OPT`.

For the dual, take `y_h=d_OPT(h)`. Run any partial policy `P`; at each
unresolved leaf `A`, append the optimum tree restricted to `A`, suppressing
constant tests. The appended raw cost is at most

```
sum_(h not in C(P)) d_OPT(h).
```

The resulting complete legal tree cannot beat the optimum. Thus

```
F_OPT <= W(P) + sum_(h not in C(P)) d_OPT(h),
```

or equivalently `sum_(h in C(P)) d_OPT(h) <= W(P)`. This proves dual
feasibility with objective `F_OPT`; weak duality completes the proof.

This is not a polynomial LP formulation: its columns contain the difficult
adaptive policy space. The useful point is that fractional combination
and rounding are not the source of the approximation loss. The actual
optimal leaf-depth vector is an exact dual certificate.

## 2. Weighted completion density gives the same approximation factor

For supplied positive integer prizes `w_h`, define

```
rho*(w) = min_(P:C(P) nonempty) W(P) / sum_(h in C(P)) w_h.
```

Suppose a polynomial oracle returns an executable `P` with density at
most `alpha rho*(w)` whenever `1 <= w_h <= n-1`. Its output policy has at
most polynomial representation size; suppressing redundant tests makes a
partial tree proper and gives at most `n-1` internal nodes anyway.

**Weighted pricing theorem.** Such an oracle yields a polynomial
`alpha`-approximation for uniform decision trees.

Algorithm:

1. Start with any proper complete incumbent `T`, for example greedy.
2. Give each hypothesis prize `w_h=d_T(h)`.
3. Ask the oracle for `P`.
4. If `W(P) < sum_(h in C(P)) d_T(h)`, run `P`, then append `T` restricted
   to every unresolved leaf. Adopt this complete tree and repeat.
5. Otherwise return `T`.

**Proof of improvement.** The spliced tree has cost at most

```
W(P) + sum_(h not in C(P)) d_T(h) < F(T).
```

Each strict improvement decreases an integer in `[0,n(n-1)]` by at least
one, so at most `n(n-1)` successful passes occur. Prizes remain positive
integers at most `n-1` for `n>=2`.

**Proof of approximation at stopping.** The full optimal tree is a valid
competitor for the density oracle, so

```
rho*(d_T) <= F_OPT / F(T).
```

If `F(T)>alpha F_OPT`, the oracle's returned density is less than one and
step 4 must strictly improve. Therefore stopping implies
`F(T)<=alpha F_OPT`.

An equivalent formulation approximately maximizes collected prize/work.
The reduction uses the guarantee in the correct direction: approximation
of a minimum density is an upper bound, while approximation of a maximum
reward/work is a lower bound.

This improves the factor-four histogram transfer for a **uniform**
completion-density oracle by using a stronger, incumbent-depth-weighted
oracle. It does not prove that the stronger oracle is tractable. The case
`n=1` is trivial and needs no oracle call.

Uniform priors and unit costs matter to the polynomial wrapper: raw costs
and prizes are small integers, so a strict decrease has size at least one
in a polynomially bounded range. The LP splicing argument itself also
has weighted-prior analogues, but arbitrary rational priors do not inherit
this polynomial iteration bound merely by clearing denominators.

## 3. Exact separation inside an explicit policy family

Let `S` be a finite represented state family containing all singletons and
`H`. A test is supported at `A in S` if all its nonempty outcome subsets
are in `S`.

For fixed incumbent-depth prizes `w_h`, the maximum prize-minus-work of
every supported partial policy is computed exactly by

```
V({h}) = w_h,
V(A)   = max(0, max_(supported splitting tau)
                    [sum_a V(A intersect tau^-1(a)) - |A|]).
```

The zero option means stop unresolved; it is not a zero-cost completion.
Evaluate in increasing candidate-set size. Store the maximizing action to
recover an executable partial policy. For a fixed represented family the
runtime is polynomial in `n,m,|S|`, with integer bit complexity polynomial
as well. The recurrence sums all outcomes for fixed response bound `K`.

If `V(H)>0`, splice the recovered fragment into the incumbent. Its actual
cost decreases by at least `V(H)`, often more because restriction can save
additional incumbent queries. This checks a violated completion-LP dual
constraint rather than comparing only the mean costs of complete codes.

If `V(H)=0`, the incumbent depths satisfy every represented partial-policy
dual constraint. If the incumbent complete tree is itself supported, the
restricted completion LP is then exactly tight at its cost.

For one explicit template, an alternative computes the least work to
collect each integral prize total by a child-convolution DP. Incumbent
depth prizes have total at most `n(n-1)`, so this exact weighted version
of a finish-`k` prefix DP remains polynomial. The profit recurrence is
enough to detect a strict improvement at density threshold one.

## 4. Product-state policy weaving

For two proper complete supplied-test codes `A,B`, consider states

```
S_u^A intersect S_v^B.
```

There are at most `(2n-1)^2` such states. An action executes the next
nonconstant query of either code. Tests rendered constant by the other
code's information are skipped without charge. Querying the first code
advances its pointer; querying the second advances its pointer. A simple
acyclic DP computes the optimal adaptive interleaving in polynomial time,
even when a selector spine has length `Theta(n)`.

**Pointwise portfolio bound.** The optimal weave has raw cost at most

```
2 sum_h min(d_A(h),d_B(h)).
```

Proof: alternate advancing the two codes until one identifies the target.
For each target this spends at most twice the shorter code depth; skipping
known tests only helps. Exact optimization is no worse.

The constant two is tight for this benchmark even without restricting the
weaving method. Give only singleton tests on `n=2q` uniform hypotheses.
One template uses forward singleton order and the other reverse order.
The pointwise-minimum depth sum is `q(q+1)`, but every complete legal tree
has cost `2q^2+q-1`. Their ratio tends to two.

This portfolio comparison does not compare the generated templates with
OPT. It does explain why exact interleaving can be stronger than selecting
the cheapest whole code.

## 5. A concrete fixed-exponent polynomial generator

Implemented in
[research-general-algorithm-next.py](research-general-algorithm-next.py).

Maintain a base family `B` of node states of actual complete generated
codes. At each pass:

1. Retain every node of the incumbent.
2. At every incumbent node `S`, and for every supplied test splitting `S`,
   generate the full candidate with that root and complete fresh greedy
   codes on every outcome. Retain all their node states.
3. Form `Q={A intersect B:A,B in B}`, also retaining the base states.
4. Evaluate the exact prize-work recurrence of Section 3 on `Q` with
   incumbent-depth prizes.
5. Splice a positive-profit fragment into the incumbent and repeat; stop
   when maximum profit is zero.

The prototype also computes the exact supported **complete**-tree DP on
the base family and on `Q` for diagnostics. The prize-work splice is never
worse than either complete-tree result: every represented complete tree
is an admissible fragment with collected prize `F(T)`.

### Feasibility of intersection states

If `S=A intersect B` and `A` is a base code node, prune its associated
subtree to `S`. Every surviving node has form `A_u intersect B`, again in
`Q`. Thus every represented nonsingleton has a supported complete code.
This is the closure property needed by the exact DP; arbitrary assigned
continuation costs are never used.

### Runtime

There are at most `n(n-1)` improving passes. Each pass probes at most
`n-1` incumbent internal nodes, at most `m` root tests, and a fixed number
of greedy outcome codes, each with at most `2n-1` nodes. Consequently the
number of accumulated base states is `O(n^4 m)` and the quadratic family
has at most `O(n^8 m^2)` states. A conservative implementation bound,
including `n`-bit set scans and repeated passes, is

```
O(n^11 m^3 polylog(nm)).
```

The exponents are fixed. This is an intentionally loose existence bound,
not a claim of practical scalability. Importantly, fresh codes are
generated only at incumbent nodes, not recursively at **all** newly
represented states; the latter substitution would invalidate the stated
polynomial bound.

For any fixed intersection arity `d`, a corresponding `d`-fold closure is
still polynomial with larger fixed exponents. Letting `d` grow with `n`
would need a new runtime argument.

### Optional verification-first templates

The root investigation proposed one additional static template for every
target `h`. Follow an `h`-verification spine: choose the test whose
`h`-outcome leaves the fewest candidates, continue on that outcome, and
complete every off-spine branch by fresh greedy. Retain all template node
states before policy iteration. This adds at most `O(n^2)` base states,
so it preserves the polynomial bound. It can expose deep target-centered
states absent from one-step deviations. The option is implemented as
`--verification-templates`.

## 6. Quantitative stability for conditional depth profiles

At a final incumbent node `S`, let `B` be a retained code whose domain
contains `S`, and let `d_B(h)` be its depth after restriction to `S`.
Let `d_T,S(h)` be the incumbent's remaining depth from `S`.

The quadratic family supports running `B` for at most `t` nonconstant
queries and then falling back to the incumbent subtree: all states have
form `S_u^T intersect S_v^B`. Thus final stability implies

```
sum_(h:d_B(h)<=t) d_T,S(h) <= sum_(h in S) min(t,d_B(h)).          (A)
```

Otherwise that woven prefix plus incumbent continuations would strictly
decrease cost. This is a profile statement, stronger than comparing the
two whole-code means.

For example, for every `x>0`,

```
|{h:d_T,S(h)>x and d_B(h)<=t}| <= (1/x) sum_h min(t,d_B(h)).      (B)
```

Nonnegative combinations of (A) give a fractional completion-cover upper
bound on incumbent cost whenever the corresponding generated completion
sets cover the hypotheses. The global exact LP in Section 1 is the
unrestricted version of this certificate.

What remains missing is a proof that these generated profiles provide
such a cheap cover compared with OPT, or that they separate incumbent
depth prizes with factor `o(log n/log log n)`. No claim that means alone
or random experiments supply that theorem is made.

## 7. Reproducible experiments and an explicit failure case

Executed:

```
python research-general-algorithm-next.py --random-cases 500 --adversary-b 4
python research-general-algorithm-next.py --random-cases 500 --adversary-b 4 --verification-templates
```

Random instances use 12 distinct biased binary response words and at most
8 tests, with fixed seed `190611385`. No balanced encoding is supplied
artificially. An independent full adaptive subset Bellman oracle supplies
the exact optimum for validation only.

Both runs improved greedy on 42 of 500 instances and matched the exact
optimum on 499. Quadratic closure strictly helped in three cases. These
counts are debugging evidence, not approximation evidence.

One explicit case, with tests encoded as positive bit masks on hypotheses
`0,...,11`, is

```
[4032, 258, 1024, 2096, 138, 780, 1571].
```

Greedy and base-state recombination both have raw cost 45; quadratic
intersection synthesis finds raw cost 44, which is optimal. Thus the new
closure operation has a concrete effect beyond the old base-state DP.

The stronger generator is **not exact**. For

```
[96, 1042, 129, 8, 2748, 3264, 3840],
```

greedy and the final generated tree have raw cost 47, while the exact
optimum is 46. Maximum represented prize-work profit is zero, even after
adding all 12 verification-first templates. This is a useful explicit
test against any unsupported claim that local stability equals global
optimality. Its asymptotic approximation gap is not known.

On the independently audited paired-grid pruning plateau from
`research-general-continuation.md`, with `n=96,m=45`, incumbent and greedy
raw cost 740 becomes 728 and then 704, matching the known column-first
benchmark. The first-pass base DP alone obtains 734. This shows that
complete code generation and intersection weaving repair the earlier
cheap-pruning obstruction.

Verification templates add genuine new states: first-pass base size
1,278 becomes 1,350 on that grid, and quadratic-family size 7,461 becomes
7,851. The measured objective is unchanged on these examples.

A larger adversarial run with `--adversary-b 5 --verification-templates`
also passed: at `n=192,m=67`, raw cost `1708 -> 1656 -> 1600`, again
matching column first. The final represented family contains 60,011
states. This test constructs and optimizes the actual supplied-test
instance; it is not a cost-only extrapolation.

## 8. Primary-literature checks

I checked the original authors' sources rather than treating general
policy-improvement results as a UDT approximation theorem.

- [Bertsekas, Multiagent Rollout Algorithms and Reinforcement Learning](https://web.mit.edu/dimitrib/www/Multiagent_Rollout.pdf)
  states the standard complete-base-policy improvement property and a
  multiagent reduction in control-space cost. That supports using actual
  complete continuations; it supplies no uniform-UDT constant here.
- [Streeter and Smith, New Techniques for Algorithm Portfolio Design](https://arxiv.org/abs/1206.3286)
  frames portfolio construction through scheduling and learning. The
  exact two-code product DP and UDT dual-depth argument above are proved
  directly in this note rather than imported from that work.
- [Navidi, Kambadur, and Nagarajan, Adaptive Submodular Ranking and Routing](https://arxiv.org/html/1606.01530)
  gives an information-plus-normalized-coverage score and a completion-tail
  analysis. In uniform binary ODT, its score is, up to a common factor,

  ```
  min(a,s-a) + 2a(s-a)/(s-1),
  ```

  where a test splits `s` candidates into sizes `a,s-a`. This is strictly
  increasing in `min(a,s-a)`, so its rule specializes exactly to balanced
  greedy. Reusing that score alone therefore retains the binary greedy
  obstruction. Its completion-profile analysis is the more relevant
  connection to the weighted-pricing route.

## 9. What would resolve the unrestricted target

The exact LP and weighted-pricing theorem give a precise sufficient target:
for incumbent depth prizes, generate a partial policy with

```
W(P) / sum_completed d_T(h)
  <= alpha(n) * min_Q W(Q) / sum_completed(Q) d_T(h)
```

in fixed-exponent polynomial time. Any
`alpha(n)=o(log n/log log n)` proves the requested improvement with the
same factor, and a fixed `alpha` proves a constant approximation.

The implemented generator prices exactly over a polynomial, coherent
adaptive policy family. Proving its comparison with all partial policies,
or enlarging it through a polynomial procedure with a provable comparison,
is the unsolved step. Neither the conditional theorem nor the successful
grid repair is reported as an unrestricted approximation result.
