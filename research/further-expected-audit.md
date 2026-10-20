# Independent review of the new general polynomial improvements

This review checks the new expected-depth factor **below 5.272565** and records the independent maximum-depth review establishing a factor **at most 4.46496526**. Both results concern the unrestricted binary, unit-cost, supplied-line planar identification model. The expected-depth result permits arbitrary positive rational priors. No shared TeX file was edited.

## Expected-depth proof audit

I read `further-expected.md` and the exact-certificate portion of `further-expected-check.py`. The argument is sound. The key distinction is between actual discovery information and the information in a coarsened, virtual discovery transcript.

For a newly covered block, let `x<=y` be its endpoint-exclusive masses and `z` its shared mass. Stop mode saves `y` relative to the allowance `(2k+3)(x+y+z)`. Query-both mode physically saves `x+y-z`. In query-both mode, merging its actual `x` and `z` exits into one virtual first-positive exit of mass `x+z` loses exactly

```
(x+z) H_nats(x/(x+z)).
```

The virtual positive cells still lie in individual supporting caps, so each has mass at most `delta w`. Thus its information retains the existing capped-entropy lower bound. Rewriting endpoint conditional entropy against that virtual transcript permits the corresponding information gain to be credited once. It is not added to a bound that already uses the finer actual transcript.

The rational tent with

```
p*=21317/125000,
h*=1-2p*=41183/62500
```

is valid by the certified inequality `H_2(p*)>h*`, concavity, and symmetry. Therefore the implemented exact rational block discount

```
D=max{y, x+y-z+min{(h*/p*)x, h*(x+z), (h*/p*)z}}
```

is a legal lower bound on the physical saving plus retained information saving. Its two mode choices leave the same coverage blocks and greedy block order. Origin endpoints, previously cached negatives, and later deletion of constant queries only decrease actual cost.

The affine minorant

```
D >= (228683/103683)m - (250000/103683)delta w
```

holds globally, alongside `D>=0` and `D>=m-delta w`. For fixed mass between `delta w` and `2delta w`, the feasible `(x,y)` region is the stated triangle. The query-both expression is concave there. Its two zero-shared vertices give mass `m`; its third vertex gives the stated tent function. The chord beginning at `m=(1+p*)delta w`, combined with the old slope-one bound below that point, proves the minorant. This proof does not require an optimizer or a realizability claim about an abstract source profile.

All nine rows in the fixed shift table are valid bounds on the same total saving. First-phase and second-phase length bounds are used correctly. The second-phase rows have budgets four and five, with cumulative lengths at most five and six. A completed schedule still covers all positive mass, so early completion preserves the bounds. The row containing `zeta A(2,2)` uses zero for its remaining mixture weight, justified by nonnegative total saving. The analysis uses convex combinations; it does not add overlapping prefix credits.

The analytical witness masses and actual newly covered block masses remain distinct throughout the transfer. Exact budgeted coverage supplies `H>=M_k`; summing the actual affine inequalities then transfers to `M_k`. In the final threshold step only coefficient `a_4` is below `T=1.382412`, so its deficit is paid using `m_4<=2delta w`. All other first five comparisons and the monotone tail are certified. The retained zero waiting credit gives the claimed `chi b` bound because `chi+2/ln(beta)>=T`. The final entropy and restriction credits telescope correctly.

The resulting certificate values are

```
A = 3.591810178840039
B = 4.717880246118900
chi = .856049452255203
extra entropy coefficient < 1.680753968383097
factor < 5.272565.
```

The exact rational certificate verifies the strict final inequality directly. Its exploratory floating-point optimization is not part of the algorithm or the certificate. The algorithm compares rational prior-mass expressions and enumerates polynomially many budget covers and rational shift regions; no logarithm evaluation, small-prior cutoff, or quasipolynomial subroutine is needed.

## Independent actual-circle checks

I added `further-expected-audit-check.py`, separate from the author's analytical-profile and certificate script. It constructs weighted circular interval instances on four through nine vertices and uses exhaustive enumeration of all block subsets as an independent exact at-most-budget coverage oracle. The generated cap weights are strictly below `delta w`; demand intervals and zero mass use exact rational weights.

For each actual geometric schedule the script computes the newly covered endpoint-exclusive and shared masses, chooses the implemented rational mode, and builds both actual and virtual transcript cells. It checks the pointwise affine bound with rational arithmetic, the physical query allowance, and the entropy-chain identity. It separately tests every constituent and every convex row in the nine-row prefix table against the actual complete schedule's saving. It then enumerates every rational shift region, integrates by its log-uniform probability, and checks the combined averaged surrogate against an independent comparison block sequence.

Running

```
python further-expected-audit-check.py
```

passed **150 actual circular instances, 1,350 table-row transfers, and 333 complete shift schedules**. The local mass and row-transfer assertions are exact rational checks. Entropy identities and averaged logarithmic quantities in this supplementary finite test use floating-point tolerances; the author's separate theorem certificate supplies rigorous logarithm enclosures. Finite checks corroborate the proof and do not replace it or claim that arbitrary abstract source profiles are geometrically realizable.

The author's default `python further-expected-check.py` also passed its exact theorem certificate, 5,000 rational block-credit checks, and 10,000 analytical profile checks.

## Maximum-depth review

The full independent argument is recorded in `further-w-audit.md`. The interval-deadline program indexed by spatial region and a subset of global rank slots is exact: an earliest selected position hits its containing demands, and every unhit interval lies wholly in one child region. Its rank-partition recurrence has combinatorial complexity `O(M^3 3^L)`; enumerating the first circular block adds only a polynomial factor.

Taking the global cap `L=ceil(2 log_2 n)+1` makes that program polynomial. The hybrid construction retains the old general induction and also obtains the coefficient-two induction whenever the state's optimum is at most `2 log_2 n`. Restriction keeps every descendant within that global threshold. The supporting-prefix deadlines and terminal-singleton append fit within the rank cap, and the zero route fits within the target height.

At the root, the smaller-optimum regime gives the factor `2+gamma=4.46496526`. The larger-optimum regime uses the old induction and gives the smaller bound `3+gamma/2=4.23248263`. This establishes the claimed general polynomial maximum-depth factor without assuming an unknown optimum can be computed or using the quasipolynomial algorithm.

The scheduler author's finite dynamic-program-versus-enumeration checks are supplementary evidence; this review independently checks the state sufficiency, recurrence, rank cap, induction, floor budgets, and global regime argument.

## Conclusion

Both new bounds pass the independent proof audit. The expected-depth theorem additionally passes actual block-schedule and shift-transfer tests, beyond local credit and abstract-profile checks. No double counting of discovery information or overlapping prefix savings, hidden dependence on the least prior weight, or quasipolynomial step was found.
