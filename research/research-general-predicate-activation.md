# Predicate gates: a negative-answer budget and a sharp activation obstruction

Auxiliary research note, 19 October 2026. The article is unchanged. This
extends the charged simulation in `research-general-dependency-graph.md` and
isolates a limitation of that abstraction. It gives no unrestricted ratio.

There is a useful parameter beyond the number of full-tuple activation
aliases: a supplied equality evaluator's **negative-answer budget**, provided
every true exit fixes the complete parent tuple. Ordinary Boolean circuit
size or ordinary gate-evaluation depth does not suffice. Even a predicate
decidable by one equality can make the full-parent activation DP worse than
an actual code by `Omega(sqrt(n)/log n)`.

## 1. An executable extension of the charged theorem

Keep the uniform product `H=product_i [Mi]`, all pure coordinate equalities,
and one fixed parent set `Pa(i)` per target. Every other physical question is
of the form

    q(x)=G(x_Pa(i)) AND f(xi).

The target function f can be a supplied bit of an injective local label.
For every full parent tuple, a supplied enabled owner palette of width
`c_i>=1` must identify all Mi values of target i. Different tuples may use
different owner palettes. The full-parent charged DP is unchanged: revealing
i when all its parents are known costs c_i, so it has only `product Mi=n`
count states.

For every original gate, supply an acyclic evaluator using parent equalities
only. It must meet both conditions:

* It evaluates G correctly, and at every true exit it has determined the
  **entire** parent tuple, including parents irrelevant to the particular
  true certificate.
* On every path it receives at most kappa negative equality answers.

Determined questions may be skipped. True exits can then answer the target
bit after its activation; false exits answer the original question zero.
As before, retaining every equality result and complete free revelation
keeps the simulator's posterior a product, and its history entails every
original answer.

Fix one target hypothesis. Paid negative answers contribute at most
`kappa depth_T`; a pure equality contributes at most one, so assume
`kappa>=1`. Every paid positive answer fixes a previously unknown coordinate,
which never incurs an activation charge. If P is the set of these distinct
coordinates, pathwise

    paid_checks + activation_charges
      <= kappa depth_T + |P| + sum_i c_i - sum_(i in P)c_i
      <= kappa depth_T + sum_i c_i.                        (1)

There is no need to count tests, terms, or repeated parent occurrences
separately. Full-parent revelations can skip additional evaluator questions
and only improve (1). Consequently the actual code produced by the charged
DP satisfies

    ALGmean <= kappa OPTmean + sum_i c_i.                  (2)

For power-of-two alphabets and owner widths `c_i=log2 Mi`, this is a
`(kappa+1)` approximation. It retains an explicit fixed-exponent polynomial
runtime. For a supplied union of at most D full-parent tuples, sequentially
checking the tuples has at most D negative answers; this recovers the
`D+1` owner-palette bound. The new parameter can be much smaller than D.

The full-parent true-exit condition is essential. Finishing evaluation of a
Boolean predicate need not reveal its remaining parents, so one cannot
silently activate the target at that point under this DP.

## 2. A compact evaluator beating the alias-count parameter

Let a gate have p parents, each of alphabet at least four, and `0<=s<=p`.
Define G to hold
when all parent values lie in `{0,1}` and at most s of them equal one. Its
number of activating full tuples is

    D=sum_(j=0)^s binom(p,j).

Evaluate parents successively. Ask `xp=0`. A hit fixes that parent. On a
miss, return false immediately if s exceptions have already occurred;
otherwise ask `xp=1`, returning false on a miss and continuing on a hit.
Every true exit has fixed all p parents. A true path has at most s negative
answers. A false path either detects the `(s+1)`st nonzero value or receives
one additional miss while checking a value outside `{0,1}`. Its negative
budget is therefore at most `s+1`.

The evaluator can be represented by an acyclic program with states
`(next parent, exceptions used, which equality is next)`, using `O(p(s+1))`
states. Its saved equality transcript still retains all earlier values.
For fixed s, (2) gives a constant `s+2` class guarantee even though D grows
as `Theta(p^s)`. For growing s the same explicit program and count DP remain
polynomial; the approximation depends on s rather than on that much larger
binomial sum. This is a genuine extension of the full-tuple alias bound,
though these activating predicates are sparse rather than dense.

## 3. A one-equality dense predicate defeats full-parent activation

Let `H=[M]^2`, `M=2^b>=4`, with coordinates x,y and all pure equalities. Give
each target two b-bit palettes:

    dense_x,j = [y != 0] AND bit_j(x),
    rare_x,j  = [y == 0] AND bit_j(x),

and the symmetric palettes for y. Thus every actual parent value has a
complete active owner code. Each predicate is decided by just **one** equality
and has constant circuit size. The actual dependency graph is a two-cycle.

Ask all 2b dense questions first. If both coordinates are nonzero, their
responses give x and y exactly. If at least one coordinate is zero, every
dense response is zero. Therefore only the single exceptional cell

    E={(x,y): x=0 or y=0},  |E|=2M-1,

remains unresolved. On E, all 2b rare questions identify the hypothesis:
when y=0 they give x, and when x=0 they give y. Skipping questions already
constant gives an actual proper original-query code of mean at most

    U=2b [1+(2M-1)/M^2]=O(log M).                         (3)

In contrast, the full-parent activation abstraction cannot activate either
coordinate before an equality search has identified the other. Along its
all-negative prefix, the first t equality questions exclude at most tM
hypotheses. For `0<=t<M/2`, neither coordinate is yet a singleton, so another
paid question is required. Its expected paid work before the first complete
coordinate is at least

    sum_(t=0)^(M/2-1) (1-t/M) = 3M/8+1/4.                (4)

Its charged objective is no smaller. Comparing (3)-(4), the full-parent DP
can lose `Omega(M/log M)=Omega(sqrt(n)/log n)` to an actual code despite two
constant-size predicate families per target. This is an obstruction to this
abstraction and to replacing kappa by ordinary predicate-evaluation depth;
it is not a decision-tree approximation hardness result.

The missing true-exit condition explains the discrepancy. The true answer
`y!=0` leaves M-1 possible parent values. A simulator that insists on full
parent knowledge must still identify y. An equality evaluator satisfying
the true-exit condition has a path with at least M-2 negative answers, even
though ordinary evaluation of this predicate needs one question. Alternatively
activating on partial parent information would repair this example, but the
state would need to retain which values remain and which predicates are
already enabled; the n-count-state proof would no longer apply.

## 4. Representation, verification, and the discovery limit

The sufficient theorem uses supplied product coordinates, target/parent
assignments, and owner palettes. Evaluator programs can either be supplied
or synthesized exactly in polynomial time for each **fixed** kappa, as below.
This does not synthesize an optimal unrestricted coordinate representation.

All gate truth tables have at most `product_(p in Pa(i)) Mi<=n` rows. Given
an evaluator DAG, simulate every parent assignment through it, retaining its
equality constraints. Check the stated output, and check that each true exit
has singleton candidates for every parent. This is polynomial in the explicit
table and program size. A longest-path computation with negative edges
weighted one and positive edges weighted zero certifies kappa; allowing
unreachable paths only overestimates it. Owner-code injectivity and original
question equality can likewise be checked directly on the response matrix.
No minimization over unbounded kappa, circuit synthesis, or palette subset
search is assumed.

### Exact polynomial synthesis at any fixed negative budget

For one gate, let the parent product have size `N=product Mi<=n`. A state
keeps its parent candidate sets and remaining negative budget k. Along any
path with initial budget kappa, every parent is either fixed to one value,
or has its full alphabet minus some excluded values. There are at most kappa
excluded values across the still-unknown parents: each needs a negative
answer, and exclusions disappear from the representation when a coordinate
becomes a singleton.

There are at most

    (kappa+1) product_i(Mi+1)
                 sum_(j=0)^kappa binom(sum_i Mi,j)         (5)

such states. The fixed-or-unknown context count is at most `N^(log2 3)`;
the exclusion factor is `O((sum Mi)^kappa)`. Thus (5) is polynomial for every
fixed kappa, with no dependence on the number of activating aliases.

At a candidate product C and remaining budget k, stop false if G is false
throughout C, and stop with its truth value if every parent is known.
Otherwise try each proper parent equality `xi=v`. It is feasible precisely
when both its positive child at budget k and its negative child at budget
`k-1` are feasible. At `k=0` no proper query is possible. Every child reduces
the sum of candidate counts, and each negative child additionally decreases
the budget. The recurrence is acyclic and exhaustive for equality evaluators
meeting the true-exit requirement. Checking whether a cell contains any true
parent tuple is a direct scan of the explicit G table.

This DP either constructs the desired evaluator or correctly reports that
none exists within the specified fixed budget. Its choices form a polynomial
DAG over these states. Positive answers retain their full actual values in
the transcript, so merging future-equivalent program states does not erase
the information needed for activation. Running this synthesis for every
original gate gives an executable `(kappa+1)` class algorithm whenever all
gates pass and the supplied owner palettes are valid. For a kappa growing
with n the exponent in (5) grows; only supplied compact evaluators retain the
earlier polynomial guarantee in that regime.

With supplied axes, a gate's target-cylinder form can be checked by scanning
the matrix for each candidate target and its declared parents. Given a common
activation predicate and declared b rows, injectivity is a direct test. If
many rows are supplied, discovering a minimum identifying subpalette cannot
be replaced by an enumeration of `m^log n` possibilities. Likewise arbitrary
Boolean parent predicates can mix the coordinates in the retained response
relation, so the earlier singleton-parent box recognizer does not establish
automatic axis recovery here. These are separate unresolved discovery issues.

Thus the useful next abstraction must permit activation by **certified
partial parent information** and retain its continuation state without
enumerating arbitrary candidate subsets. A low ordinary gate-evaluation
complexity by itself gives neither that compact state space nor the charged
simulation comparison.

## 5. Bounded checks

The companion `research-general-predicate-activation.py` checks the Hamming
predicate evaluator against its full truth table and negative budget, and
executes the dense/rare code (3) using original question indices. It compares
that actual code with the exact full-parent charged DP for growing bounded
M. All 5,624 predicate assignments pass; 75 true exits have fully determined
parents, and every negative budget obeys `s+1`. Five dense-gate examples use
`M=4,8,16,32,64`, up to 4,096 hypotheses. At M=64 the actual code has mean
`49473/4096`, while the charged full-parent optimum is `2463/64`, already a
factor `52544/16491>3` larger. There is no unrestricted optimum oracle;
(3) is an explicit upper bound and (4) is an analytic obstruction. Results
are saved in `research-general-predicate-activation.results.json`.
The exact synthesis routine also constructs five bounded Hamming evaluators
from their truth tables alone. For `G(x)=[x!=0]` on four values it rejects
budgets one and two and accepts budget three, confirming that ordinary
one-question evaluation does not imply a small full-parent budget.
