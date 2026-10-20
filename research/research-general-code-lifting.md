# Global lifting of conditional decision-tree codes

Auxiliary research note, 18 October 2026. This file does not alter the article.
The idea was proposed by the root researcher; this note supplies an independent
implementation, elementary bounds, and a limited validation suite. The stronger
threshold and entropy pruning certificate is being audited in the parallel
capacity notes. No unrestricted approximation guarantee is claimed here.

## 1. The operation and why it adds a different kind of state

Let H be the current ambient hypotheses, C a subset, and B an actual identifying
tree on C using the supplied tests. Execute B's physical queries directly on H.
Outside hypotheses follow their actual responses. Stop when B reaches a core
singleton, even if the current global response cell also contains outsiders. For
more than two responses, an outcome with no C-child also stops immediately.
This is a legal executable partial policy. It does not first test membership in C.

At a node whose core transcript cell is C_v, the lifted cell is instead the
intersection of H with that transcript. The two cells can be very different.
Thus retaining only conditional code states does not provide these states.
Each unresolved exit can subsequently receive the incumbent restricted to that
exit, or a fresh greedy code, whichever is cheaper. Both choices are legal.

The binary implementation is `lift_partial` in
`research-general-code-lifting.py`. It preserves the supplied query indices;
it does not invent a membership test or change the meaning of a query.

## 2. Proved elementary bounds

Write k = |H minus C|, F_C for B's raw external path length on C, and L for
its height. Every outsider either exits at a missing core response or reaches
one core leaf. At most k core leaves are contaminated. Consequently:

* At least max(0, |C| minus k) core hypotheses are identified by the lifted
  partial policy.
* Its actual raw work is exactly F_C plus the sum of the executed path lengths
  of the outsiders, hence is at most F_C + k L.
* If core hypotheses have nonnegative prizes w_h, the completed prize is at
  least the total core prize minus the sum of the largest min(k, |C|) core
  prizes. Singleton outside-only exits may give additional prize.

Proof: a core hypothesis follows its original B path, giving exactly F_C work
and one different core leaf per core hypothesis. Each contaminated core leaf
requires at least one distinct outsider. Each outsider makes at most L queries.
For weighted loss, delete the prizes of the contaminated core leaves and bound
their sum by the largest min(k, |C|) prizes. These arguments also cover a fixed
number K greater than two of responses; missing-core response branches are
unresolved exits of depth at most L.

For incumbent-depth prizes, a directly checkable sufficient condition for an
improvement is

    core prize - sum of largest min(k, |C|) core prizes > F_C + k L.

The exact lifted policy can give a much stronger certificate than this coarse
inequality. In particular, stopping before the contaminated leaves can avoid
most of the outsider work. A claim about all-core completion would miss that.

## 3. Exact prefix pruning of one lifted template

For each template node v and integer j, let D_v(j) be the minimum raw work of a
pruning below v that completes j hypotheses. Stopping unresolved has D_v(0)=0.
A singleton template leaf also has D_v(1)=0; a nonsingleton terminal leaf has
only j=0. Continuing at v costs |S_v| plus the min-convolution of child profiles.
Minimize D_root(j)/j over j positive. This searches every nonuniform stopping
prefix of that explicit template, including prefixes that decode clean cells
and stop contaminated cells.

The implementation reconstructs an executable partial tree and checks that its
actual singleton count and work equal the selected profile. With at most n
template leaves the profile convolutions take O(n squared) arithmetic work:
each pair of distinct leaves is charged at their unique least common ancestor.
This exact routine prices one explicit template; it does not price all legal
policies.

## 4. A fixed-pool polynomial synthesis algorithm

One pass of `generated_pass` does the following.

1. Freeze the actual incumbent's node states. At every nonsingleton incumbent
   state, generate fresh complete greedy codes on that state and on every
   nonempty child of every supplied query that splits that state. Optional
   weighted generators use current depths, squared depths, and every distinct
   depth threshold. Retain every actual subtree of these generated codes as a
   conditional source code.
2. Freeze that source-code list. Replay each source on the full hypothesis set,
   then complete its collision exits with the cheaper of fresh greedy and
   incumbent restriction. Optionally replay it on every containing incumbent
   state instead. Retain the resulting actual node states.
3. Add the pairwise intersections of retained states and optimize the earlier
   exact supported-state depth-prize policy DP. An optional stronger version
   uses exact incumbent restriction credit and one-query terminal fallback
   boundaries, as described in `research-general-adversarial-pricing.md`.
4. Accept only a strict decrease in the integer raw cost. Retain the base states
   and start a new pass from the actual resulting tree.

Crucially, the list in step 1 is frozen before any lifting. Lifted codes,
collision fallback codes, and quadratic intersections do not recursively
generate further source codes within the pass. On a later pass, the accepted
actual tree may of course provide new incumbent states.

Here is a conservative polynomial bound. There are O(n) incumbent nodes and
O(nm) conditional root requests per unweighted generator. Including O(n)
weighted generators and all subcodes gives at most O(n cubed m) source codes
per pass. Each lifted complete code has O(n) nodes. There are at most
n(n minus 1) accepted cost decreases, so the persistent base has size
O(n to the sixth m), and its quadratic closure has size
O(n to the twelfth m squared). The optional actual-fallback DP scans m queries
per represented state, with at most O(m times the closure size) distinct
terminal boundary cells. Evaluating each fallback by scanning the incumbent
costs O(n) bit-set operations. Across all passes, a loose bound is
O(n to the fifteenth m cubed polylog(nm)) bit-set/arithmetic operations, or
O(n to the sixteenth m cubed polylog(nm)) bit operations with n-bit masks.
Generating and fingerprinting the source codes is below this bound.

Lifting to every containing incumbent state adds a factor at most n to the
base size, so the corresponding loose bit-operation bound is
O(n to the eighteenth m cubed polylog(nm)). The exponents are fixed. No horizon,
coalition width, or closure exponent grows with n. These bounds are deliberately
loose; they establish polynomial runtime, not practical scalability at the
worst-case bound.

The exponential subset optimizer is used only in the small benchmark function
to validate the achieved output, never by generation, pricing, or descent.

## 5. Saved adversarial witnesses: finite positive evidence

The suite reruns all six previously saved failures. The conditional-only
comparison uses exactly the same frozen source generation and quadratic
closure, but disables global lifting. No weighted generator, target coalition,
small-tail completion, or actual-boundary fallback is enabled in the plain
global-lift column.

| Saved witness | n | Greedy raw cost | Conditional-only output | Global-lift output | Exact OPT |
| --- | ---: | ---: | ---: | ---: | ---: |
| old12 | 12 | 47 | 47 | 46 | 46 |
| adversarial12 | 12 | 48 | 47 | 45 | 45 |
| adversarial14 | 14 | 61 | 60 | 57 | 57 |
| adversarial16 | 16 | 66 | 66 | 65 | 65 |
| adversarial18 | 18 | 87 | 85 | 80 | 80 |
| weighted18 | 18 | 82 | 81 | 79 | 79 |

All six lifted runs reached OPT in their first improvement pass from the fresh
greedy incumbent, then made one stability pass. Their first-pass source-code
counts were respectively 45, 50, 69, 81, 98, and 110; the number of nontrivial
global lifts was one fewer in each case. Final represented-state counts were
140, 144, 221, 255, 465, and 487. The weighted-generator and actual-boundary
variants also reached OPT on this suite. These are finite repairs, not an
approximation theorem or evidence that arbitrary optimal states are represented.

The exact ordered query masks and all run histories are in
`research-general-code-lifting-benchmarks.json`. The earlier adversarial notes
explain how the witnesses were found and the missing contexts of the preceding
algorithms.

## 6. A toy with no membership query for the core

Take C = 2 to the b core hypotheses, one for every b-bit string. The b core-code
queries are coordinate bits, and every outsider answers zero to every one of
them. There are k even outsiders. Other queries are the edges of a cycle on
outsiders and all outsider singletons; each is positive only on its one or two
listed outsiders. There is no supplied test for C or for its complement.

A strategy that first establishes membership in C using only these outside
tests requires at least k/2 negative queries, because every query covers at
most two outsiders; a perfect matching attains this. Before then using the
balanced core code, its raw work on core hypotheses alone is at least
C times (k/2 + b).

Direct lifting instead makes b queries per hypothesis, completes C minus 1
core hypotheses, and has work (C+k)b. Only the all-zero core leaf is contaminated.
This does not show that fresh greedy is bad: it already starts using the useful
core queries on these examples. It isolates why context activation is an
unnecessary prerequisite for reusing a conditional code.

The clean-frontier prefix first queries one coordinate. It stops the zero-side
cell containing all outsiders and fully decodes the clean positive half.
It completes C/2 hypotheses with raw work C(b+1)/2 + k, hence density
b+1+2k/C. This remains useful when outsiders greatly outnumber the core.
It is one of the prefixes searched by the exact template DP.

| b | C | k | Full lifted prefix work / completed | Clean-half work / completed | Exact best prefix density |
| ---: | ---: | ---: | --- | --- | --- |
| 6 | 64 | 12 | 456 / 63 | 236 / 32 | 106/15 |
| 10 | 1024 | 32 | 10560 / 1023 | 5664 / 512 | 1305/127 |
| 6 | 64 | 1024 | 6528 / 63 | 1248 / 32 | 39 |

The first two exact prefixes improve on the clean-half choice; the third
selects the clean half exactly. Complete lifted codes with the implemented
collision fallback cost 516, 10880, and 270720. Fresh greedy costs 510, 10864,
and 270208, respectively. The partial density, rather than superiority of a
fixed full completion, is the useful feature of the last example. The
activation-first core-work lower bounds are 768, 26624, and 33152, respectively.

Actual output and exact pruning profiles are in
`research-general-code-lifting-toys.json`.

## 7. Checks and current limit

`python research-general-code-lifting.py --audit` passed 100 seeded random
instances with random core subsets. It checks direct per-hypothesis execution,
the exact outsider-work identity, contamination bounds, arbitrary nonnegative
integer-prize loss bounds, complete collision fallback, and exact prefix DP
against exhaustive enumeration of every pruning of the same small template.
`python -m py_compile research-general-code-lifting.py` also passed. The
validation output is in `research-general-code-lifting-audit.json`.

The unresolved comparison is global: there is no proof that these polynomially
many source codes contain, or lift into, a partial policy of density within a
constant or o(log n/loglog n) factor of the best legal policy. Outside response
collisions can still destroy the elementary completion bound, and the finite
repair suite does not control that obstruction. The root's completion-cover
and actual-credit oracle reductions remain the precise sufficient targets.
