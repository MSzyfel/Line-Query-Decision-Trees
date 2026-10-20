# Expected-depth simplification and development session

## Manuscript edits and preserved results

Owned and edited these existing sections only:

- `sections/06-expected-depth.tex`
- `sections/06c-polynomial-block-improvement.tex`
- `sections/06e-adaptive-block-modes.tex`
- `sections/06f-first-phase-improvement.tex`

Added:

- `sections/06g-two-phase-improvement.tex`
- `sections/12-two-phase-certificate.tex`

No main-file headline was changed by this agent. All previous guarantees,
parameter values, algorithm labels, and numerical certificates remain valid
and present. The preexisting first-phase pseudocode was moved from its
section's end into the actual candidate-family exposition, before analysis.

The repeated threshold and zero-mass argument is now one lemma,
`lem:capped-rank-credit`. If w=b+p0, each analytical witness mass is at
most 2 delta w, and all coefficients a_t exceed tau except on a finite
set E, then

    chi = tau - 2delta sum_E (tau-a_t)_+ - delta mu
    sum_t m_t a_t - delta w mu + zeta p0 >= chi b,

provided chi+zeta>=tau. Its proof is the exact two-line identity

    tau b - (tau-chi)w + zeta p0
      = chi b + p0(chi+zeta-tau).

All vertex, block, orientation, mixed-prefix, adaptive-mode, and first-phase
proofs invoke this lemma; the original common stage-to-tree conversion remains
the only recursive-potential argument. Numerical certificate tables and the
case-specific signed phase/tail details remain explicit.

The capped-discovery entropy proof is shorter without losing its exact sigma:
concentrate capped entries to minimize entropy; the resulting T(b) is concave
between multiples of delta; check its endpoints against b sigma(delta).
This removes an unnecessary derivative analysis of T(b)/b while retaining
positive-mass and zero-entry edge cases, the exact remainder, and
sigma(delta)>=ln(1/delta). Root independently audited both new simplifications.

The block section also gives an explicit actual-versus-witness table: actual
block ranks and discovery cells pay physical cost and information; witness
supporting-prefix ranks and two-cap masses pay restriction and discounts.
Exact coverage connects these columns through prefix mass M_q, without ever
identifying their partitions. Each later section includes a proof roadmap.

## Stronger general polynomial expected-depth approximation

The new actual schedule family is the union of the existing first-phase
family and, for every rational shift representative u,

    q,r,k2,k3,...     q=1,...,6; r in {k1-1,k1,k1+1}; q<r<k2,
    q,k2,k3,...       q=1,...,6,

where kj=floor(beta^j u). Every budget below k_min uses exact maximum
coverage; the first budget reaching k_min uses Q* and finishes. Productive
blocks are ordered greedily within the batch. The mode and schedule score
remain the existing rational surrogate

    2 MSSC_block + 2 p0 |G| - sum D.

Use beta=3512863/10^6 and delta=393931/2500000=.1575724. The construction
adds at most 24 variants per shift, with no new kind of breakpoint or
prior-dependent exponent. Its recursive state threshold changes, so retaining
old per-state schedule variants does not assert instance-wise dominance of the
complete older recursion.

For r>0, subtracting the old and new unaveraged phase allowances gives

    d = k0-q + (k0+k1)1[t>k0] + (k1+k2)1[t>k1]
          - (q+r)1[t>q] - (r+k2)1[t>r].

For r=0, the last two terms become -(q+k2)1[t>q]. This is exactly twice
the first-hit improvement; it keeps adverse signs. The all-negative invoice
changes by

    z = q1[q<k] + r1[r<k] - k0 1[k0<k] - k1 1[k1<k],

with r term zero when r=0. Arbitrary increasing budget sequences retain the
within-batch residual proof. Early minimum-cover completion only removes
nonnegative continuation terms.

A fixed 43-row rational distribution uses ONLY FIRST-BATCH minorants
A_q=M_q-delta w q or C_q=c*M_q-d*delta w q. Thus there is no extra
second-prefix or disjoint-phase credit to audit in the published proof.
Its full self-contained table, including all twelve rational weights, is
in the numerical certificate appendix section. The algorithm does not read
this distribution or compute a logarithm.

Set tau=2190079/10^6. The effective coefficients satisfy:

    a1 = 1.2764767886276687... < tau,
    min(a2,...,a14) > 2.1900797161 > tau,
    mu = 4.461183727319314...,
    chi = 1.199202587062859...,
    B = 4.374727111311243....

All signed changes are constant from rank 14 onward, while e_beta is
nondecreasing; the complete infinite tail reduces to a14. Average zero-length
changes are zero at k=1 and strictly negative at every k=2,...,14; from k=14
onward they are constant. Therefore the old mean zero waiting bound, and its
2p0/ln(beta) credit, remain valid for every cover size. Also
chi+2/ln(beta)>tau. The common capped-rank and stage-to-tree lemmas now yield

    R = A + max{ln2/h(delta), B ln2/sigma(delta)}
      < 5.182975508794 < 5.182976.

New theorem label `thm:two-phase-expected`, section label `sec:two-phase`,
algorithm label `alg:two-phase-family`, numerical appendix label
`sec:two-phase-certificate`.

## Verification

`expected-two-phase-check.py` uses exact Fraction arithmetic with outward
atanh logarithm bounds. Its final assertion is R<5182976/10^6. It checks:

- lambda_beta>nu_beta and the accepted rational entropy tent;
- all exceptional coefficient comparisons and the constant tail;
- every exceptional zero waiting correction and its constant tail;
- the zero-credit inequality and final ratio;
- 9,900 exact old-versus-new phase identities;
- 1,650 actual modified-batch comparisons on small circular interval demands,
  including early Q* completion and full negative-route length invoices.

All passed. `simplification-expected-check.py` separately checks 3,000 exact
instances of the shared capped-rank lemma. Root independently audited the
shared simplifications and the new stage algebra; another agent is completing
an independent certificate and full-row audit.

Exploration files `expected-two-phase-explore.py`, `expected-fast-simplex.js`,
and `expected-two-phase-optimize.py` found the table but are not theorem
assumptions. Fixed data are `expected-two-phase-certificate.json`.
The final table has no reliance on floating-point optimizer optimality.
A grouped 12-row distribution gives approximately 5.184174; it was not selected,
as shortening the table would weaken the proved result. Wider second-budget
families produced a small additional exploratory gain but were not developed
into a claim; the completed manuscript retains the best fully certified result.

No PDF marker or build was run by this agent. Root owns final integration,
compilation, diagram review, and visual QA.
