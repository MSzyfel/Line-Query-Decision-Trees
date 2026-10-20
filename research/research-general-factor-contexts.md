# Polynomial context generation from filtered response factors

Final refinement on 19 October: `factor_decoder` and `plan_factors` also
accept `retained_fallback=True`. This optional version compares the selected
local decoder with the sequential code using the original retained rows
belonging to that factor. Those rows always identify its value and remain
eligible on every context. It has height at most their number, regardless
of quotient multiplicities. Its leaves are the same complete factor-value
cells, so choosing the lower raw decoder cost preserves every continuation
cost in the factor DP. The default remains false to keep earlier portfolio
audits' scope explicit; the newer linear-selector portfolio enables it.
Both the previous decoder's intermediate states and the retained-row
decoder's states enter the recombination pool, even when only one code is
chosen for the local cost. This preserves the earlier portfolio's entire
pool and therefore its recombination guarantee. A two-factor fixture checks
this containment explicitly.
The checker exercises a prime eight-value response factor with a balanced
decoy: ordinary local greedy costs26, while this retained-row code costs24.

Auxiliary research note, 19 October 2026. The article is unchanged. This
introduces an explicit polynomial candidate algorithm and proves its coverage
on a broad hidden-coordinate class. No unrestricted approximation improvement
is claimed.

The new observation is that **all complete-value contexts of independent
response factors fit in polynomial space**, even when the number of factors
grows. This replaces the need to find a favorable slice of the incumbent
tree. A dynamic program then chooses which factor to decode next, depending
on previously observed factor values. The algorithm discovers the factors;
it is not given selector/body roles or their correct order.

## 1. Factor the support of a retained response quotient

For each occurring global minority size t, keep original tests whose smaller
root response has at least t hypotheses. There are at most n/2 different
positive thresholds. Initially specialize to binary tests.

Two hypotheses may have identical retained response words. Deduplicate those
words, giving a quotient support R with N<=n words. Apply the exact
[response-product factorization](research-general-product-decomposition.md)
to the **uniform distribution on these distinct words**, not to their
original multiplicities. Remove constant factors. Write

    R=R_1 times ... times R_d,   n_i=|R_i|>=2,
    product_i n_i=N.

This is a factorization of the response support. It need not make the
original-hypothesis distribution independent. Keep each original hypothesis,
its factor labels, and its actual multiplicity throughout subsequent work.
The previous exact entropy-cut comparisons and polynomial factorization
runtime still apply, since they operate on the distinct support words.

Each factor is a group of retained query coordinates. Its values are
distinct marginal response words; no external geometric representation is
used. Retained tests in a factor always distinguish its values, even when
other original tests mix several factors.

## 2. All factor contexts have polynomial total size

A context specifies, independently for each factor, either one of its n_i
values or that the factor is still unknown. Its actual population is the
set of original hypotheses satisfying those specified values. The Cartesian
support guarantees every such context is nonempty.

**Counting lemma.** The number of contexts is

    C=product_i(1+n_i)
     =N product_i(1+1/n_i)
     <=N(3/2)^d <= N^(log_2 3) <= n^(log_2 3).

The second inequality uses d<=log_2 N. In particular C<=n² is a convenient
integer upper bound. When R is a Boolean cube, the exact count is 3^d for
N=2^d; the exponent is fixed. Constant factors must be discarded before
using this argument.

Thus enumerating every partial assignment of **whole factor values** is
polynomial in the explicit input. This is different from enumerating all
test histories of logarithmic depth, whose m-dependent exponent would be
superconstant. The new states may be absent from every initial greedy path.

Fresh greedy on the original test family can be run at every context. The
union of all its code states, all contexts, and the factor decoders below
is also polynomial. Arbitrary recursive refactorization of newly created
states is not included in this bound.

## 3. Legal factor decoders, including newly eligible queries

At context c with population S, consider an unknown factor i. Let S_v be
the actual hypotheses with its value v. For every original test q and value
v, record whether q is constantly zero, constantly one, or inconsistent on
S_v. On a surviving set A of i-values, q is eligible precisely when no
inconsistent value remains in A. An eligible q has an actual response
depending only on i and therefore reveals no other still-unknown factor or
residual identity.

Eligibility must be checked again after exclusions. For example, a query
that also depends on another factor only at i=0 becomes eligible once i=0
has been excluded. Freezing eligibility at the initial S would miss legal
factor codes. The implementation stores the inconsistent-value mask and
uses it at every local state.

Give factor value v the integer weight |S_v|. These are the actual
original-hypothesis multiplicities; they need not be uniform. If n_i is at
most floor(log_2(n+m+1)), exact subset DP computes its minimum raw decoder
cost using the eligible queries. This evaluates at most n+m+1 subsets and
is polynomial. At larger alphabets use weighted balance greedy, testing
eligibility in the same way. A proper greedy decoder has at most n_i−1
internal nodes. The retained factor queries guarantee that identification
is possible.

The decoder's original-test leaves have populations exactly S_v. No free
membership query or context oracle is introduced. Its query work is
charged on the actual hypotheses in every intermediate node.

## 4. Adaptive whole-factor planning

Compute V(c) in increasing context-population size. One option is the actual
fresh greedy code on S. For each unknown factor i, another option is

    D_i(c)+sum_v V(c with factor i fixed to v),              (1)

where D_i(c) is the actual weighted decoder cost above. Choose the cheaper
option and retain its original-test code. The continuation sum is
independent of the factor's internal decoding order because every value
exit is exactly S_v. All children of (1) have strictly smaller population.
At a full retained-response context, greedy identifies any remaining
residual hypotheses.

Grafting the selected continuations yields a proper original-test tree.
Every original hypothesis reaches a singleton. The root greedy option
ensures nonregression. Factor order may depend on all earlier factor
values; it is not a single global ordering. The state pool also retains
all factor-decoder nodes and fresh greedy nodes, for later supported-policy
recombination. The present prototype returns that pool but does not claim
that the broader pricing algorithm already consumes it.

**Runtime.** There are at most n thresholds, at most n² contexts per
threshold, and at most log_2 n nonconstant factors. Local exact DP has at
most n+m+1 states; large-alphabet greedy creates at most 2n_i−1 states.
Each step scans original tests and explicit hypothesis cells. Exact
factorization uses the earlier polynomial entropy-product comparisons.
The entire construction has a fixed-exponent polynomial time and space
bound. Output trees have at most n leaves. There is no n_i-dependent
exponent left implicit in the algorithm.

**Benchmark scope.** When every local decoder is exact, (1) is optimal
among programs which completely decode one factor at a block boundary,
or stop at a context and use the fixed greedy fallback. If supplied
conditional decoders and terminal continuations approximate their
corresponding benchmark costs within beta, induction gives the same beta
factor for this block-program benchmark. It does not compare block
programs with arbitrary policies that interleave partial information from
several factors. A prime retained quotient may give only one large
factor, in which case this generator can offer little beyond greedy.

## 5. An automatic near-optimal hidden-selector guarantee

Consider the private-selector class of
[completed selector replay](research-general-selector-replay.md):

    H=product_(i=1)^k [M_i] times product_(j=1)^L [r_j],
    min_i M_i > max_j r_j >=2.

Supply all pure coordinate equality tests. For every full selector context
b and body factor j, supply an injective b-dependent binary labeling of
its r_j values, with b_j=ceil(log_2 r_j) bits. Its physical bit tests are
positive only in context b. Labels may be arbitrary and independently
nonlinear. Original test order is arbitrary.

Let M_max=max_i M_i and select threshold t=n/M_max. All pure equalities
survive. Each private gated bit has strictly smaller minority: its support
is below n/product_i M_i, hence below or equal to t with strictness from
the nonconstant minimal-width bit. Thus only pure-coordinate tests remain,
up to harmless copies and constants. Their support is exactly a Cartesian
product of one-hot response relations. Each one-hot relation is prime,
so exact factorization recovers all the coordinate axes.

The context DP therefore includes the following legal program, without
being supplied any roles: decode all selectors by equality, then the
bodies by their now-active bit palettes. Selector decoding has mean
sum_i e(M_i), where e(s)=(s+1)/2−1/s. A body greedy code spends at most b_j
queries on each actual path. Before its first singleton equality, only
owner bits have been used; if q owner bits were asked and s values remain,
choosing that singleton implies s−1<=b_j−q by the distinct-label argument.
Any proper continuation then needs at most s−1 more queries. Hence the
candidate mean is at most

    U=sum_i e(M_i)+B,   B=sum_j ceil(log_2 r_j).             (2)

The earlier joint selector-axis-pair plus context-coding ledger proves

    OPT_mean >= A+L_2(N_body)/N_body,
    A=sum_i(M_i−1)/2,   N_body=product_j r_j.                (3)

Pairs agree on all bodies and differ in exactly one selector coordinate.
A private gate assigns every cut-pair charge outside its active context;
coding uses only that context, so the budgets are disjoint. This is the
existing ledger specialized to the class, not a new LP cone.

Equations (2)-(3) give the automatic polynomial guarantee

    output/OPT <= 1+max(2/M_min, 1/log_2 r_min).             (4)

It holds with a growing number of selectors and arbitrary query priorities.
The previous completed-source proof required a useful actual incumbent
slice and pure-equality tie priority; this algorithm needs neither. The
class includes the full-order fixed-lookahead obstructions, yet (4)
approaches one when its alphabets grow. This remains a structured-class
result, not the requested unrestricted approximation improvement.

For the genuinely aliased multiple-selector class with an actual global
minority gap, the same context construction exposes its coordinate axes.
The selector-first/P-per-row program and optimized shared ledger from
[filtered sources](research-general-filtered-sources.md) therefore give its
corresponding D+P−1 asymptotic class bound without requiring an incumbent
slice. This statement needs the actual support gap D<M^(k−1). It does not
cover every earlier serial-alias family: when the base has size DM, a
degree-D gate can be globally larger than the base equalities.

## 6. Finite checks and remaining comparison

[The prototype](research-general-factor-contexts.py) passes 40 small seeded
instances, with 627 threshold contexts and four nonuniform-quotient cases.
An independent unrestricted subset solver is used only to check these
finite outputs; it is not an algorithm input. A dedicated 2x2 support with
unequal residual multiplicities verifies the distinction between support
factorization and weighted execution. A conditional-eligibility example
has decoder cost 26 rather than the static singleton decoder's 28.

Four automatically factored private-context cases use reversed original
query order and shuffled private labels. Their contexts number 48,75,100,
and 245. At n=144 the algorithm improves ordinary greedy from 1284 to 1248,
matching the displayed selector-first upper bound. All original-test
paths are executed. These small examples are implementation checks; the
asymptotic guarantee is proved above.

The independent [factor-context audit](research-general-factor-contexts-audit.md)
checked the context count, actual multiplicity accounting, block-policy
composition, eligibility refinement, and the automatic private-class
guarantee. The essential open step is a comparison with arbitrary adaptive
decision trees when no filtered quotient exposes useful product structure,
or when completing one factor before using partial knowledge of another
is too restrictive. The general objective remains active.

Run `python research-general-factor-contexts.py`; results are saved in
[JSON](research-general-factor-contexts-results.json).
