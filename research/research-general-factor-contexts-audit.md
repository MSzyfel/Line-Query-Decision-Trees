# Factor-context count, weighted composition, and a private-context guarantee

Auxiliary proof audit, 19 October 2026. The article is unchanged. This reviews
the threshold/quotient/factor-context algorithm and its subsequently saved
`research-general-factor-contexts.py` implementation. The count and legality
claims are sound with the qualifications below.

## 1. The context count really is polynomial

For a retained query set, identify hypotheses with the same full retained
response word. Let `N<=n` be the number of **distinct** quotient words. Apply
the exact Cartesian response-relation factorization to these distinct words,
temporarily giving every distinct word equal probability. Discard constant
factors, and let the remaining factor alphabet sizes be `n_i>=2`. Then

    product_i n_i=N.

A full-factor context gives each factor either the status unknown or one of
its `n_i` values. All such contexts are actual nonempty subsets because the
quotient support is Cartesian. Their number is

    C=product_i(1+n_i)
      =N product_i(1+1/n_i)
      <=N(3/2)^d
      <=N^(log2 3),                                        (1)

using `d<=log2 N`. Equality is possible for all-binary factors. Constant
factors must not contribute an artificial unknown/fixed choice; otherwise
arbitrarily many constant query coordinates would invalidate the count.
For `N=1`, there are no nonconstant factors and just one context, namely H.

Every threshold can be chosen from the finitely many observed global minority
sizes, plus an empty/full-set endpoint. Thus the number of retained relations
is polynomial as well. Repeating the exact entropy-cut factorization remains
polynomial in the explicit response matrix. Neither (1) nor the algorithm
enumerates all original-test subsets or all logarithmic test palettes.

## 2. Uniform distinct words are a support device, not the true prior

Discarding duplicate quotient words is correct for testing whether the support
is Cartesian. It does **not** make the original posterior independent or
uniform on factor values. The original hypotheses still each have unit mass,
so distinct quotient tuples can have different multiplicities.

At an actual context S, for an unknown factor i and value v, use

    w_i(v)=#{h in S : factor_i(h)=v}.

A complete local factor code has actual raw work
`sum_v w_i(v) depth(v)`, regardless of whether the quotient tuple weights
factor. Its physical queries are legal if their outcome is constant over all
original hypotheses in S with the same i-value. The retained queries assigned
to factor i satisfy this automatically and identify its values, so there is
always a valid local decoder.

Once i is decoded as v, the actual output is exactly the full child context
`S(i=v)`: a factor-local transcript has imposed no further restriction on other
factors or on the hypotheses sharing the same quotient tuple. This fact makes
the context DP valid under arbitrary multiplicities. At a fully fixed coarse
tuple, a fresh code must identify its original-hypothesis residual; the
residual is not a free singleton unless its multiplicity really is one.

## 3. Exact composition and its precise benchmark

Given local factor-code costs `c_i(S)` and a supplied fallback `g(S)`,
the implemented complete-block recurrence is

    J(S)=min{g(S), min_unknown_i [c_i(S)+sum_v J(S(i=v))]},

with `J(S)=g(S)` when every factor is fixed. Each child fixes one more factor,
so the recurrence is acyclic over the contexts counted in (1). The sum of
continuation costs is independent of the internal factor-code order.

If every `c_i(S)` is the exact least weighted cost over its declared admissible
query class, this DP is exactly optimal among policies that **completely
decode one factor at each block boundary or stop with the supplied fallback**,
with future factor choices depending on all previously observed values. It is not an optimum over
arbitrary partial-factor interleavings or arbitrary original-query policies.
If every block decoder and residual fallback is a beta-approximation to the
corresponding block-policy benchmark, induction gives the same beta factor
for the complete DP. No independence of the true tuple weights is needed.

For `n_i<=floor(log2(n+m+1))`, exact factor subset DP has at most `2^n_i<=n+m+1`
subsets. Its raw query cost on a subset A is `sum_(v in A)w_i(v)`. The number of
contexts, factors, candidate tests, and subset-DP calls is still polynomial.
For larger factors a supplied greedy decoder remains polynomial, but exact
block-policy optimality then refers to the chosen decoder library unless an
additional local approximation theorem is supplied.

There is a small eligibility distinction worth making explicit. A test can
fail to depend solely on i over all of S because of one i-value, yet become
factor-local after that value is excluded inside the factor code. Static
eligibility `Q_i(S)` gives a valid, narrower code class. Exact subset DP can
also handle these newly eligible queries at no exponential penalty: record
for each query/value a response or the marker inconsistent, and allow the
query on A precisely when every v in A has a consistent response and the
responses split A. Any optimality statement should say which version it uses.

Reconstruction uses only original physical queries. A proper complete code on
n original hypotheses has at most `n-1` query nodes; memoized polynomial
context computation does not require an exponentially large output tree.

## 4. Automatic nearly optimal coverage of private selector/body products

The proposed threshold procedure has a clean guarantee on the entire class of
`research-general-selector-replay.md`, without supplied roles, anchor slices,
or favorable greedy tie priority. Let

    H=(product_i [Mi]) times (product_j [rj]),
    min_i Mi > max_j rj,

and supply all pure coordinate equalities plus private full-selector-context
body palettes of width `bj=ceil(log2 rj)`, with arbitrary context-dependent
injective labels. There are no additional tests in this guarantee.

Let `M_max=max_i Mi`, and retain queries of global minority **at least**

    t=n/M_max.

Every pure equality survives. Every private palette test is discarded. Indeed,
its support is at most `n/P`, where `P=product_i Mi`. With two or more selectors
this is strictly below `n/M_max`. With one selector, each minimal-width
injective label bit is nonconstant, so its positive support is still strictly
below `n/P=n/M_max`. All these gate supports are below one half, so their
positive support is their global minority.

The retained response relation is therefore exactly the Cartesian product of
the pure-coordinate equality relations. Each individual equality relation is
prime: splitting its r one-hot test coordinates into nonempty groups of sizes
u and v gives projected support product `(u+1)(v+1)>u+v=r`.
Consequently exact factorization recovers the actual coordinate axes, up to
permutation, without any role labels being input to the algorithm.

The block DP includes the order that first decodes every selector by equality,
then every body by its active private palette and singleton equalities. The
selector block cost is `e(Mi)`. The first-singleton owner-bit argument from
the selector-replay note gives body path length at most `bj` under arbitrary
bit/equality ties. Therefore

    output_mean <= U=sum_i e(Mi)+sum_j ceil(log2 rj).        (2)

This does not depend on the initial incumbent or on harvesting a particular
source. It also does not require favorable test priorities: support filtering
and exact factorization expose the axes before the factor-order optimization.

The independently verified selector-axis-pair plus fiber-coding certificate
from the same note is valid for this whole class, regardless of test order:

    OPTmean >= A+L2(N)/N >= A+log2 N,
    A=(1/2)sum_i(Mi-1),  N=product_j rj.

Thus, with `M_min=min_i Mi,r_min=min_j rj`,

    output/OPT <= U/[A+L2(N)/N]
               <=1+max(2/M_min,1/log2 r_min).               (3)

The number of selectors and bodies may both grow. This is a structured-class
guarantee for an automatic algorithm, not an unrestricted approximation or a
claim that all response relations reveal such a factorization at some threshold.

## 5. Caution about genuine activation aliases

Threshold separation is not automatic for the genuine-alias family in
`research-general-aliased-routing.md`. There the base alphabet is `M0=DM`,
so pure base equalities have minority `n/(DM)`, while degree-D first-row
affine bit gates can have minority `n/(2M)` and pure row equalities have
minority `n/M`. For `D>2`, no high-minority threshold retains the base equality
queries while discarding all these gates. A threshold above the gates can
expose only the body factors, leaving the base in an unresolved quotient
multiplicity rather than an available factor to decode first.

This observation does not prove that the full threshold algorithm fails on
those instances; other thresholds or conditional relations might help. It
does mean that the private-context proof in Section 4 cannot simply be asserted
for arbitrary alias graphs. A separate coverage argument or an explicit
factorization certificate is required.

## 6. Audit status

The context count, actual-weight recurrence, original-query legality, and
private-context ratio were checked directly as proofs. The existing exact
`EntropyCuts` implementation and its prior audit establish the support
factorization primitive. A subsequent direct code read checked that:

* quotient duplicates are removed only for support factorization, while local
  costs use actual original-hypothesis cell populations;
* constants and complementary retained partitions are removed safely;
* queries carry their inconsistent-value mask and are allowed only after all
  such values have been excluded, including in the large-alphabet greedy mode;
* the exact alphabet cutoff is clamped to `floor(log2(n+m+1))` by the public
  planner, preserving its stated polynomial bound;
* fallback is available at every context, child contexts strictly shrink, and
  reconstruction grafts full original-hypothesis child codes at actual local
  decoder leaves.

No implementation defect was found. This audit did not independently rerun
the root implementation's finite suite and does not use that suite as a
proof of the ratio. No article or other agent's implementation was edited.
