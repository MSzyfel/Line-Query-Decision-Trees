# Adversarial audit of global conditional-code lifting

Auxiliary research note, 18 October 2026. The article is unchanged.

**Result of this pass.** No nonoptimal fixed point was found for plain global
lifting or the weighted/actual-boundary extension. Six completed mutation
campaigns account for 6,135 valid table evaluations, counted separately within
each run; different runs may overlap. This is finite experimental evidence,
not an approximation theorem. Several initially plausible camouflage families
are demonstrably easy for the generator. A saved executable certificate shows
one such escape. A separate construction proves that a known optimal adaptive
code can require a linear-size static identifying palette; it is not itself
an approximation lower bound.

The new runner is `research-general-lift-adversaries.py`. It imports the stable
`research-general-code-lifting.py`; the earlier synthesis files were not edited.
All completed data and ordered query masks are retained in the JSON files below.

## 1. Precisely which candidates were tested

Plain lifting uses fresh uniform greedy conditional codes at incumbent states
and at every supplied-query child of those states, including actual subcodes.
It replays every frozen source on the whole instance, fills collisions by the
cheaper of fresh greedy and incumbent restriction, retains resulting states,
takes quadratic intersections, and performs exact depth-prize policy descent.

The strong candidate adds depth, squared-depth, and every depth-threshold
weighted code generator. Its optimizer uses actual incumbent restriction
credit, and at every represented state may take a supplied query whose
unrepresented children receive terminal incumbent-restriction fallback. It
does not recursively expand those boundary states. Neither candidate uses
optimal subproblem values during generation or synthesis. Their fixed-exponent
polynomial bounds remain those in `research-general-code-lifting.md`.

There is an important evaluation shortcut. From the same initial incumbent,
the strong first-pass represented family contains the plain first-pass family.
Its actual-credit DP can realize every plain depth-prize splice and may do
better. Therefore, if the **first** plain pass already attains independently
certified OPT, the strong output is also OPT. The runner records
`strong_first_pass_optimum_certificate` and does not build the surplus strong
templates in that case. If the first plain pass does not attain OPT, it actually
runs the strong candidate.

The strong campaign counts below are counts of certified or explicitly computed
strong outputs. They are not counts of full strong synthesis executions. The
number of full strong executions within each historical campaign was not
counted separately. To verify a concrete rich execution, the final n=36 table
was rerun without the shortcut: greedy cost 214, explicit strong output 196,
exact OPT 196. Its two pass sizes were:

| Current raw cost | Conditional source codes | Base states | Quadratic states | Resulting cost |
| ---: | ---: | ---: | ---: | ---: |
| 214 | 2816 | 2963 | 15719 | 196 |
| 196 | 2044 | 3504 | 19057 | 196 |

That actual run and its boundary counts are saved under
`explicit_strong_validation` in `research-general-lift-strong-n36.json`.

## 2. Search families and independent validation

The initial structured bank includes:

* Expanded prior counterexamples, adding near-duplicate response words.
* Fibre substitution of prior tables, with conditional copy bits shared with
  another fibre to introduce outside collisions.
* Context grids with coordinate codes aliased onto one or two other contexts,
  together with competing unions of small row blocks.
* Sparse response words of weights one, two, or three, and graph-incidence
  response tables.

Mutations change response cells, nearby hypothesis words, test ordering,
correlated rectangles, AND/XOR combinations, and add or delete tests. Fitness
uses the actual final synthesized output divided by independently computed
OPT. Later coding campaigns also use first-pass difficulty as a secondary
objective. Flat fitness regions and a bounded elite archive permit movement
when all final ratios are one.

For general small tables, validation uses exact subset Bellman optimization
with branch-and-bound. The lower bound on the raw cost of a state of size s is

    L(s) = s (ceil(log2 s)+1) - 2 to the ceil(log2 s),

with L(0)=L(1)=0. A candidate root query has lower bound
`s+L(child1 size)+L(child2 size)`; a branch at least as expensive as an available
complete tree can be skipped. This retains exactness. The old unrestricted
subset solver was impractical on some fibre substitutions because it explored
arbitrary combinations of private local tests. The new bound was independently
checked against that solver on 48 cases with n from 3 through 18.

For coding families, OPT instead has an explicit certificate: an actual full
binary code attaining the information lower bound. No exponential optimization
is required. Every such certificate is executed against the supplied response
table, not inferred from a label attached to the construction.

## 3. Completed mutation campaigns

An evaluation count includes valid initial seeds and previously unseen valid
mutations within that run. Proposal counts include invalid or repeated
proposals. Each saved table is the strongest final proxy selected by that run;
because no final output ratio exceeded one, it need not be a worst-case table.

| Family / candidate | n | Mutation proposals | Valid evaluations | Saved greedy cost | Saved final cost = OPT |
| --- | ---: | ---: | ---: | ---: | ---: |
| Structured / plain | 18 | 3000 | 2045 | 88 | 80 |
| Structured / plain | 24 | 1200 | 930 | 124 | 113 |
| Coordinate code plus decoys / plain | 32 | 1200 | 1084 | 164 | 160 |
| Resilient decoys plus coordinates / strong | 32 | 1600 | 1127 | 165 | 160 |
| Structured / strong | 36 | 500 | 422 | 214 | 196 |
| Adaptive-code outside responses / strong | 32 | 600 | 527 | 165 | 160 |

The six runs completed 8,100 mutation proposals in total. The saved files are
`research-general-lift-plain-n18.json`, `...plain-n24.json`, `...code-n32.json`,
`...resilient-search-n32.json`, `...strong-n36.json`, and
`...adaptive-search-n32.json`. Their matching `.log` files retain progress
trajectories. No nonoptimal stable table is being presented as a witness.

For the final adaptive mutation table, plain descent has trajectory
165 -> 160 -> 160, with base sizes 972 and 997 and represented sizes 4177 and
4225. Thus its strong result is certified by first-pass dominance. The mutation
does not merely retain a static coordinate code: it changes answers outside
the intended domain of each query of an explicitly supplied adaptive code.

## 4. Resilient decoys and the larger-test suite

A decoy is one-coordinate resilient if it is balanced both globally and after
fixing any one canonical coordinate. It can therefore continue tying a useful
coordinate query after a correct first canonical query.

The runner generates such functions by starting with parity and repeatedly
flipping a checkerboard two-dimensional face. The four current values on that
face must be 0,1,1,0 or 1,0,0,1. The flip preserves total positive population.
For either varying coordinate, each slice loses one positive and gains one;
for every other coordinate, the entire changed face lies in one slice and has
two positives before and after. This proves preservation of every one-bit
marginal. Thirty direct balance/marginal audits passed.

The larger test suite uses 32, 64, or 128 genuinely different resilient decoys,
plus the known coordinate queries. Complementary duplicates are excluded.
Independent variants and clustered variants of one function are both tested.
Clustered walks avoid a protected small cell in an attempt to preserve local
difficulty. This protection does not prove that greedy remains suboptimal.

All 12 cases were exact. In ten, greedy itself was information-optimal, so the
runner records that certificate and does not construct unnecessary templates.
The only nontrivial cases were clustered n=64:

| Total physical tests | Greedy | Plain lifting | OPT | First-pass base / quadratic states |
| ---: | ---: | ---: | ---: | --- |
| 38 | 386 | 384 | 384 | 12417 / 169200 |
| 70 | 385 | 384 | 384 | 17178 / 463681 |

The n=64 case with 134 tests was already greedy-optimal. The n=32 cases used
37, 69, and 133 physical tests and were all greedy-optimal. Adding many
independent decoys can increase the algorithm's actual coding power; it does
not necessarily make the example harder. These data also expose a practical
cost of the conservative generator: the two nontrivial cases took roughly
101 and 155 seconds despite n=64. Polynomial worst-case runtime does not
guarantee a small implementation footprint.

Outputs are in `research-general-lift-large-tests.json`. This suite does not
show that a small polynomial library covers arbitrary hard query combinations.

## 5. A proved escape certificate, including the necessary fresh fallback

A first nonlinear construction uses majority of three disjoint pair parities
as a balanced decoy on a six-dimensional cube. One, two, and three such decoys
give greedy raw costs 400, 392, and 386; plain lifting reaches OPT 384. Five and
eight decoys make greedy itself optimal. The suite is saved in
`research-general-lift-resilient-n64.json`.

The following elementary lemma explains a useful class of escapes.

**Coordinate completion lemma.** Suppose H is the full d-dimensional binary
cube. A source code uses only coordinate queries, and each lifted terminal
cell A is given a complete fallback of cost `|A| log2 |A|`. Then the lifted full
code has raw cost exactly `d 2 to the d`.

Proof: every proper coordinate path has distinct queried coordinates. After q
queries its cell is a face of dimension d-q. Each hypothesis receives q prefix
queries and d-q queries in an information-optimal fallback. Summing the common
total d over all hypotheses proves the claim. Different paths may stop at
different dimensions.

The saved example is a direct SINGLE lifted source, requiring no quadratic
weaving. Its core mask is 73469388526781700, with 12 hypotheses and conditional
work 44. It uses four of the canonical coordinates. Global replay has work
224, leaving eight faces of size four and four faces of size eight. The chosen
fallback work is 160, giving total 384. Eighteen available source codes satisfy
this exact completion certificate.

**Correction of an initially tempting explanation:** incumbent restriction
alone is not enough for this saved example. On each of the four size-eight
faces it costs 26 instead of the information optimum 24. Fresh greedy attains
24 there; the implementation explicitly selects it. Pure incumbent fallback
would give total 392. An audit found no coordinate-only source in this pool
whose incumbent restriction alone is information-optimal at every exit.
Consequently the executable certificate and the lemma use the chosen fallback,
which may be fresh greedy. Full source programs and exit costs are saved in
`research-general-lift-coordinate-escape.json`.

## 6. Why a fixed coordinate palette is a limited obstruction

The root researcher observed a useful general upper bound. Suppose a fixed
palette of D binary tests identifies all hypotheses. At a uniform posterior
state S, the joint entropy of the palette answers is log2 |S|. Subadditivity
implies that one palette test has answer entropy at least log2 |S| / D.
Balance greedy maximizes binary answer entropy among all supplied tests.
Its expected entropy drift is therefore at least the current entropy divided
by D. Multiplicative drift until the nonzero entropy threshold one gives

    average greedy depth <= D [1+ln(log2 n)].

One direct drift proof uses the concave potential g(x)=x for x<=1 and
g(x)=1+ln x for x>=1. At any unresolved uniform state, x=log2 |S|>=1,
and expected potential decrease is at least 1/D. The zero state is absorbing.

When D=log2 n and a coordinate code attains OPT, these examples can be only
O(loglog n)-hard for greedy. They remain useful finite checks but do not
represent a general adaptive obstruction. The next suites avoid assuming a
designated logarithmic identifying palette.

## 7. Adaptive common-answer camouflage

The construction supplies a known perfect binary code with a different physical
query assigned to every intended node. Inside that node's intended cell, its
query performs the required half split. Outside that cell, it agrees with a
common bad balanced function f, except the few response flips needed to make
the physical query globally balanced. All tests can then tie at the global
root while still supporting a known balanced adaptive code. Deduplicating
queries leaves roughly a linear number of physical tests.

Twelve n=32 examples used 26--28 physical tests; greedy cost ranged from 161
through 164, and plain lifting reached certified OPT 160. Twelve n=64 examples
used 51--56 tests; greedy ranged from 384 through 393, and plain lifting reached
OPT 384. Four larger n=128 examples used 107--110 tests; greedy costs were
909, 912, 911, and 911, and plain lifting reached OPT 896 in every case.

These data are in `research-general-lift-adaptive.json` and
`research-general-lift-adaptive-n128.json`. Supplying a code adaptively does
not by itself prove that no small static identifying palette exists for its
response table. That stronger statement is established for a modified family
in the next section.

The n=32 outside-answer campaign mutates only entries outside every intended
domain of the selected physical query, so the full optimal code remains legal.
Balanced outside swaps keep all physical queries globally balanced. If one
physical query is reused at multiple intended nodes, the union of their domains
is protected. Duplicate physical queries are rejected. The 527 resulting
validated tables also all repair to OPT.

## 8. A genuine large-static-palette family

This is a proved structural fact, not an approximation lower bound.

For d>=6, let n=2 to the d and use the usual balanced dyadic code. Let the common
function f be majority of coordinate bits 1, 2, and 3, with bit 0 the least
significant bit. Thus f is constant on every bottom sibling pair and balanced
on every top-level quarter. Reserve the first two quarters, containing n/2
hypotheses, solely for outside compensation flips. Every physical node query
still gives its intended half split inside its intended cell and agrees with
f elsewhere except on reserve points.

This is feasible. At the top two levels the intended cell is a union of
balanced quarters, so no compensation is needed. A smaller cell lies in one
quarter. At least one entire reserve quarter lies outside it; that quarter
contains n/8 zeros and n/8 ones of f, enough to supply every required positive
or negative compensation. No nonreserve response is changed by compensation.

Consider any bottom sibling pair outside the reserve. The common f gives the
same response to both. An intended ancestor query places both siblings on the
same side. Any query whose intended cell is disjoint from the pair also gives
both their common f response, because compensation is confined to the reserve.
Only the intended query at that very pair separates them. These private
queries are distinct for different pairs. Therefore **every static identifying
palette must contain at least n/4 specified physical queries**, whereas the
supplied adaptive code identifies every hypothesis in d queries.

`reserve_adaptive_camouflage` audits every one of these forced pair separations.
For n=64,m=64 it checks 16 mandatory static queries; for n=128,m=128 it checks
32. In both examples greedy itself attains OPT, respectively 384 and 896.
Thus high adaptivity alone is insufficient to make this construction hard.
The family and certificates are saved in
`research-general-lift-reserve-adaptive.json`.

## 9. Reproduction, checks, and remaining gap

The runner grew during this research pass. For the original n18/n24/n36
structured campaign configuration, use `--legacy-structured-bank --legacy-rank`.
The original coordinate n32 campaign uses `--known-code --legacy-rank`.
The resilient n32 campaign uses `--resilient`, and the adaptive mutation campaign
uses `--adaptive-search`. Each saved record includes its seed and exact ordered
test masks. `--verify-input FILE` reruns the actual full strong candidate on a
saved table, independently of the search shortcut.

Additional commands are `--large-test-suite`, `--resilient-suite`,
`--adaptive-suite`, `--large-adaptive-suite`, `--reserve-adaptive-suite`, and
`--coordinate-escape`. All accept `--output`. The exact completed outputs and
logs, rather than wall-clock timing, are the record of the historical runs.
The first aborted n36 attempt, stopped before a completed checkpoint while
using unpruned exact validation, is not counted anywhere above.

`--audit` passed 48 exact-solver comparisons, 30 resilient-function checks,
and 32 direct adaptive-code execution/information-bound checks. The two reserve
examples separately check all forced static-palette pairs. The corrected
coordinate escape checks every collision face and selected fallback cost.
`py_compile` passed. No search process is intentionally left running.

The important unanswered question is unchanged: does the frozen polynomial
source pool always provide a partial policy or actual-credit move within a
constant or o(log n/loglog n) factor of the best unrestricted policy? This pass
produced neither such a theorem nor a surviving bad family. With no nonoptimal
fixed point, it cannot diagnose a universal choice between poor conditional
source codes and excessive outsider collisions. The next meaningful target is
a recursive family combining mandatory private selectors with difficult
conditional code generation and camouflage that survives lifted reordering.
