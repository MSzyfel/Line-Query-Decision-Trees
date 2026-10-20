# Independent audit of the two-initial-phase expected-depth improvement

The fixed rational table in `expected-two-phase-certificate.json`
supports **rho < 5.182976** for the general polynomial expected-depth
algorithm. I found no mathematical obstacle to this fixed-table result.
This audit does not endorse any later numerically optimized parameter set.

Audited source files:

- `expected-two-phase-check.py`;
- `expected-two-phase-certificate.json`;
- the exploratory family's definition in `expected-two-phase-explore.py`;
- the established physical block-mode bound, discrete witness-rank
  discount, capped-rank lemma, and stage-to-tree conversion in the
  manuscript.

## Actual schedule family and signed change

For `k_j=floor(beta^j u)`, the audited variants have budgets

- `q,r,k2,k3,...`, with `1 <= q <= 6`,
  `r in {k1-1,k1,k1+1}`, and `q < r < k2`;
- `q,k2,k3,...`, represented by `r=0`.

Every budget at or above the minimum cover size uses that minimum cover
and terminates. Earlier phases use exact at-most-budget maximum coverage,
with newly covered weight greedy within the chosen set. Repeated and
unproductive queries are omitted.

For `r>0`, subtracting the two phase accounting expressions gives

\[
d=k_0-q+(k_0+k_1)\mathbf1[t>k_0]
 -(q+r)\mathbf1[t>q]
 +(k_1+k_2)\mathbf1[t>k_1]
 -(r+k_2)\mathbf1[t>r].
\]

For `r=0`, the two negative terms are replaced by
`-(q+k2) 1[t>q]`. This is exactly twice the improvement in the
unaveraged first-hit upper bound. Its sign must be retained.
The modified bound is nondecreasing in `t`, since its phase-sequence
form is a positive constant plus positive step increments. Therefore
a comparison block that hits earlier than its witness supporting-prefix
index only improves the upper bound.

The separate all-negative change is

\[
z(k)=q\mathbf1[q<k]+r\mathbf1[r<k]
 -k_0\mathbf1[k_0<k]-k_1\mathbf1[k_1<k].
\]

Here `r=0` contributes zero. This remains correct when either changed
phase reaches the minimum cover early: an executed final phase has
exact size bounded by `k`, rather than its nominal larger budget, and
the same terminal `k` cancels in the difference.

## Saving is counted once

Every option in this particular table has cutoff exactly `q`. Thus it
uses only one of the **first-batch** minorants

\[
0,\qquad M_q-\delta wq,\qquad c_*M_q-d_*\delta wq.
\]

Exact maximum coverage covers at least witness mass `M_q`, using at
most `q` actual blocks. If that phase instead completes the minimum
cover, it covers all nonzero mass in at most `q` blocks, so the same
minorant holds. A minorant may be negative; this is harmless because
it is only a lower bound on the actual saving.

Conditional mixtures choose one valid minorant per option and hence
bound the total physical saving once. No second-phase saving is added
to this same first-batch credit. The script permits more general
cutoffs, but the fixed table being certified uses none of them.

## Entire row audit and direct integral cross-check

The new independent script `development-two-phase-audit-check.py`
checks all **43 entire half-open rational rows**, not just their
midpoints. For each `j=0,1,2`, it verifies

\[
k_j\le\beta^j l<\beta^j h\le k_j+1.
\]

Thus the three floor budgets are constant throughout `[l,h)`, including
one-sided breakpoint behavior. Each conditional distribution is
nonnegative and sums to one, and every actual table variant satisfies
the family's budget constraints.

The independent cross-check computes the logarithmic-shift mean directly:
it partitions `floor(cu)` into its rational cells and integrates each
constant as `k ln(h/l)`. It computes the modified first-hit expression
from the actual sequence `q,r,k2,...` or `q,k2,...`, without using the
theorem certificate's factorial formula or its signed-change update.

It reproduces

\[
\begin{aligned}
a_1&=1.2764767886276687154\ldots,\\
a_{14}&=2.1900797165207981174\ldots,\\
\mu&=4.4611837273193143498\ldots,\\
\chi&=1.1992025870628590033\ldots,\\
B&=4.3747271113112432463\ldots,\\
\rho&=5.1829755087931224137\ldots.
\end{aligned}
\]

These high-precision Decimal computations are an independent numerical
cross-check. The actual theorem's strict upper bound comes from
`expected-two-phase-check.py`, which uses Fraction arithmetic and
outward rational logarithm enclosures. Its final assertion was tightened
to match the published `5.182976` constant.

## All witness ranks and arbitrary zero mass

With `tau=2190079/10^6`, only `a1` lies below `tau`; all other checked
coefficients exceed it. Because `k0 <= 3`, `k1 <= 12`, `q <= 6`, and
`r <= 13`, every signed change is constant for `t >= 14` and all credit
indicators vanish there. Hence `a_t=e_beta(t)+constant` throughout that
tail. The established monotonicity of `e_beta` proves the bound for
every larger integer rank from the `a14` check; this is not a finite-only
claim.

The table's zero corrections are nonpositive for `k=1,...,14` and
constant for every `k>=14`. Therefore the previous mean waiting-length
upper bound and its `2p0/ln(beta)` saving remain valid for **every**
minimum cover size.

The capped-rank lemma applies with

\[
\chi=\tau-2\delta(\tau-a_1)-\delta\mu,
\qquad \zeta=2/\ln\beta,
\]

and the certified inequality `chi+zeta>tau`. This last inequality
pays the intercept also when much of the state mass is zero-pattern
mass. Thus the argument covers arbitrary strictly positive rational
priors and does not assume a negligible zero route.

The physical decoder estimate and the coarse transcript cap are
unchanged. Minimizing the rational score over actual schedules is at
most averaging that score using this table, while the selected
schedule's own transcript satisfies the same cap. The existing
stage-to-tree lemma consequently gives the advertised factor.

## Polynomial enumeration and retaining earlier results

The second modified budget depends only on `k1`; its three offsets
create no shift breakpoint beyond the previous geometric enumeration.
The tail budgets are unchanged. The family has a constant number of
variants per shift and uses rational tests only. When a later budget
is already above the minimum cover size, its precise value cannot
change the executed minimum-cover phase, so omitted higher-power
breakpoints in small-cover instances are harmless.

The new family includes the original geometric sequence by taking
`q=k0,r=k1`. It does **not**, by itself, include every earlier merged
first-phase schedule when `k1>6`. The agent and parent were notified:
take the union with the preceding `alg:first-phase-family` to retain
all its schedules as well. The new certificate uses only the two-phase
subset, so this union costs only a constant number of variants and
preserves both the stronger bound and prior instance-wise alternatives.

## Checks performed

- Reran the full outward rational two-phase certificate successfully.
- Checked all 43 entire rational rows and all option constraints.
- Checked **4,400 exact signed phase and early-completion length
  identities**, including all ranks/cover sizes 1 through 80.
- Independently reproduced all relevant coefficient behavior through
  rank 30 using direct floor-cell integration.
- Verified all zero corrections through 30 and their exact cutoff at 14.

No expected-depth TeX file was edited by this auditor.
