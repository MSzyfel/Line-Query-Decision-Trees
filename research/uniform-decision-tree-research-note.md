# Uniform Decision Tree: research gap and attack routes

**Prepared:** 2026-10-11  
**Scope:** noiseless identification, equiprobable hypotheses, unit-cost tests, and a fixed constant upper bound on the number of outcomes per test.

**Subsequent proved progress:** [the improved-tradeoff proof](uniform-decision-tree-improved-tradeoffs.md) gives additional cost-mass, height-certificate, and shared-budget arguments that improve constant quasipolynomial and subexponential runtime powers. The leading subexponential curve is $5/\alpha$ rather than $9/\alpha$. A 10-approximation has power arbitrarily close above $143/288\approx0.496528$, rather than $9/10$ in the supplied curve. Refinements leaving a growing runtime power in the same asymptotic order are not counted under the user's stricter criterion. The original polynomial-time research gap remains open.

**Latest requested target:** an $o(\log n/\log\log n)$ approximation in genuinely quasipolynomial time. This remains unproved; the incremental bounds above do not fulfill it. The tradeoff note now includes a lower bound for the existing cutoff algorithms and isolates a different continuation-preserving spine oracle whose proof would suffice for a constant-factor quasipolynomial algorithm.

The latest oracle analysis, in Section 14 of [the tradeoff note](uniform-decision-tree-improved-tradeoffs.md), proves an ideal affine bound for exact continuation costs and a query obstruction for arbitrary assigned valid-code costs. The remaining positive route must jointly generate and reuse coherent continuation trees; treating their costs as arbitrary black-box numbers is insufficient.

Section 15 records a weaker, sufficient pricing target and exact consistency of finite reusable code pools. Logarithmic latency loss with $1+1/\log n$ continuation inflation would give an $O(\log\log n)$ quasipolynomial ratio. No algorithm achieving that pricing guarantee has been proved; this is a precise research objective, not a claimed approximation result.

Section 16 replaces that unproved oracle by a concrete repeated policy-improvement process and proves an unconditional instance-sensitive convergence bound. It also identifies explicit complementarity in code-pruning costs and repeated-error charging on long selector spines. A uniform quasipolynomial asymptotic improvement is still not established.

Section 17 retains the probe-generated states and codes and recombines them through an exact finite-state dynamic program. A strict-descent wrapper has quasipolynomial runtime and whole-spine comparison on represented states, without an oracle assumption. The unresolved global question is whether those represented states necessarily support a sufficiently good complete tree; no improved worst-case ratio is claimed.

**Latest lower-bound investigation:** [the shared lower-bounds note](uniform-decision-tree-lower-bounds.md) verifies adaptive-cover/MSSC sources and proves a joint entropy/shared-query relaxation, a time-profile/local-policy consistency hierarchy, and a certificate-guided quasipolynomial repair of the gated-grid obstruction. The repair is proved only for that explicit family; an improved worst-case ratio for arbitrary UDT instances remains unproved.

This note separates three kinds of statements:

- **Verified baseline:** statements checked in the primary sources listed at the end.
- **Derived observation:** a proof or calculation given here, sometimes accompanied by a small computational check.
- **Research proposal:** an unproved algorithmic or hardness direction. These are not claimed to be new theorems, or to be novel relative to all existing literature.

## Executive summary

The polynomial-time versus subexponential-time approximation gap is a worthwhile research target, but two qualifications are essential.

1. A 2026 preprint initially announced a polynomial-time constant approximation. Its constant-factor claim was withdrawn after a counterexample; the current version only gives logarithmic guarantees. It does **not** close the gap.
2. The classic hardness source proves a factor of $4-\varepsilon$ for **unrestricted arity**, but a factor of $2-\varepsilon$ for **binary tests**. The former must not be quoted automatically for the bounded-outcomes model.

My recommended algorithmic agenda is:

1. **Continuation-aware policy improvement:** evaluate a test by the cost of complete greedy continuations, not just its immediate split. This is polynomial, provably never worse than greedy, and escapes an explicitly constructed grid-type greedy trap.
2. **Branching-aware MSSC macros with global charging:** exploit the existing min-sum set cover connection, but account for the difficulty of side branches and avoid charging the same optimal cost at successive scales.
3. **Size-normalized pair/latency relaxations:** retain the tractable pair-separation machinery while correcting its mismatch with average identification cost. A size-bucketed version approximates the true objective within a factor of two at the level of an actual tree.
4. **Compress the subexponential prefix search:** target its real bottleneck, rather than merely substituting a smaller exponent into its running time.
5. **Cost-sensitive state compression and structural subcases:** use these as supporting routes, not as substitutes for a global approximation argument.

For hardness, the most concrete first target is an **arity-preserving improvement beyond the certified binary $2-\varepsilon$ bound**. A much more ambitious negative resolution would prove hardness for every fixed constant, with reduction size depending on that constant. This is compatible with the subexponential upper bounds; a single polynomial reduction giving a growing hardness factor is not, under ETH.

The central algorithmic obstacle is not finding a constant-quality balanced separator. A suitable **bicriteria** separator is already available. The obstacle is paying for a hierarchy of such operations without multiplying the optimum by the number of levels.

---

## 1. Model, normalization, and two useful reductions

Let $H$ be a set of $n$ hypotheses and let $\mathcal T$ contain $m$ tests. A test is a map

$$
\tau:H\longrightarrow [K],
$$

where $K$ is fixed independently of $n$. Tests cost one unit. A valid instance separates every pair of distinct hypotheses. Every leaf of the output tree must identify a single hypothesis.

For a complete tree $T$, its objective is

$$
C(T)=\frac1n\sum_{h\in H}d_T(h).
$$

For a candidate subset $S$, write $F(S)$ for the **unnormalized** optimal cost of identifying the hypotheses in $S$ using the original tests restricted to $S$. Thus its conditional optimum is $F(S)/|S|$, and $F(H)=nC_{\mathrm{OPT}}$.

The exact recurrence is

$$
F(S)=|S|+\min_{\tau\text{ splitting }S}
       \sum_a F(S\cap\tau^{-1}(a)),
\qquad F(\varnothing)=F(\{h\})=0.
$$

Only tests with at least two nonempty outcomes on $S$ are relevant. Consequently, a state can be represented by $S$: an already-used test cannot split the corresponding state again.

For any complete tree,

$$
\sum_h d_T(h)=\sum_{v\text{ internal}}|S_v|.
\tag{1}
$$

This identity is the right accounting language for both algorithms and lower bounds.

### 1.1 Binary tests suffice for the qualitative constant-factor goal

**Derived observation.** A polynomial-time $c$-approximation for binary UDT would imply a polynomial-time

$$
c\lceil\log_2 K\rceil
$$

approximation for tests with at most $K$ outcomes.

Encode each outcome by $\lceil\log_2K\rceil$ bits and introduce the corresponding virtual binary tests. Simulating an original test with these bits shows that the optimum in the binary instance is at most $\lceil\log_2K\rceil$ times the original optimum.

Conversely, a binary strategy can be executed with the original tests. When it first requests a bit of a test's outcome, perform the original test once and cache its entire outcome. Subsequent bits of that outcome are free. The actual original-test cost is no larger than the binary strategy's cost.

This justifies attacking $K=2$ first. It does **not** preserve hardness factors in the reverse direction: outcome coding can increase the optimum by a non-negligible amount.

### 1.2 A uniform constant approximation would extend to bounded weight spread

Suppose a uniform algorithm has ratio $c$, and a weighted instance on the same hypotheses has $p_{\max}/p_{\min}\le R$. Running the uniform algorithm gives

$$
C_p(T_u)
\le np_{\max}C_u(T_u)
\le cnp_{\max}C_u(T_p^*)
\le cR C_p(T_p^*).
$$

Thus fixed $R$ would also admit a constant approximation. The automatic guarantee is $cR$, not $O(c\log R)$. This observation does not justify importing logarithmic hardness for polynomially nonuniform weights into the uniform problem.

---

## 2. Source-verified baseline

The directory contains [the 2019 arXiv v2 paper](1906.11385v2.pdf) by Ray Li, Percy Liang, and Stephen Mussmann, subsequently published at SODA 2020.

### 2.1 Algorithms

For uniform probabilities, its Theorem 3.1 gives

$$
C_G\le
\frac{12\log_2 n}{\log_2 C_{\mathrm{OPT}}}\,C_{\mathrm{OPT}}.
\tag{2}
$$

The paper improves the leading constant for uniform instances, eventually to $4+\varepsilon$ for sufficiently large $n$. The important point here is the dependence on $C_{\mathrm{OPT}}$, not the leading constant. Small cases where the displayed denominator degenerates are handled separately.

The greedy rule in this theorem minimizes the size of the largest outcome class. For binary tests it agrees with the usual entropy and pair-splitting rules; for more than two outcomes those rules need not agree.

Since $C_{\mathrm{OPT}}\ge\log_K n$, fixed $K$ gives

$$
C_G/C_{\mathrm{OPT}}=O(\log n/\log\log n).
$$

Proposition 3.3 reports matching, up-to-constants greedy lower bounds, already for binary tests. Therefore improving the analysis of the same one-test split rule cannot remove the asymptotic gap.

Theorem 3.2 gives, for every fixed $\alpha\in(0,1)$ and $\varepsilon>0$, a

$$
\frac{9+\varepsilon}{\alpha}
$$

approximation for UDT in time

$$
2^{O(n^\alpha\log n\log m)}.
\tag{3}
$$

For $m=n^{O(1)}$, this is $2^{\widetilde O(n^\alpha)}$. The explicit dependence on $m$ matters when interpreting the shorthand.

The algorithm combines greedy on sufficiently high-cost subproblems with exhaustive optimization of a long truncated tree prefix on the other subproblems. Its partial-tree routine runs in $O(n(Km)^{b+1})$ time for prefix depth $b$. This is a recursive optimization over prefixes, not simply enumeration of all full trees.

### 2.2 Hardness: the arity distinction

The original Chakaravarthy et al. journal paper establishes:

| Model | Verified hardness | Primary location |
|---|---|---|
| Uniform probabilities, unit costs, unrestricted outcomes | $4-\varepsilon$ | Theorem 4.3 |
| Uniform probabilities, unit costs, binary tests | $2-\varepsilon$ | Theorem 4.4 |

The unrestricted-arity construction lets a test reveal the identity of any element lying in its associated set. Its arity can be the set size plus one, and need not be constant.

The binary construction uses bounded-cardinality min-sum set cover and adds binary identification attributes. It has a different certified hardness factor.

Accordingly, the safe baseline for the bounded-outcomes research agenda is **at least $2-\varepsilon$**, inherited from binary instances. I did not verify a subsequent primary result upgrading this to $4-\varepsilon$ for binary or arbitrary fixed-arity instances. This is a statement about the evidence checked here, not a proof that no such result exists.

### 2.3 An important 2026 version-history warning

ArXiv:2604.12036 has the following history:

| Version | Date | Relevant status |
|---|---|---|
| v1 | 2026-04-13 | Announced a polynomial-time constant approximation below 11.57 |
| v2 | 2026-04-28 | Withdrawn; the author explicitly reports a fundamental proof mistake and a counterexample exceeding the claimed guarantee |
| v3 | 2026-08-10 | Retitled *Simpler Logarithmic Approximation Algorithms for the Optimal Decision Tree and Adaptive Set Cover* |

The current v3 claims $O(\log n)$ approximation, not a constant approximation. Its Theorem 1 retains an explicit logarithmic recursion factor. Its separating-subfamily/maximum-coverage primitive is relevant prior art, but the earlier constant-factor statement must not be used as an established theorem.

The working gap remains open on the primary-source evidence checked here.

---

## 3. Where the algorithmic difficulty actually lives

Equation (2) is already a constant approximation whenever

$$
C_{\mathrm{OPT}}\ge n^\gamma
$$

for a fixed $\gamma>0$. Thus large-cost instances are not the source of greedy's superconstant worst-case ratio.

The difficult regime is

$$
C_{\mathrm{OPT}}=n^{o(1)},
$$

especially $C_{\mathrm{OPT}}=\operatorname{polylog}(n)$.

The grid-type obstruction illustrates the mechanism:

- Slightly more balanced tests make attractive local progress.
- A less balanced test identifies a context or group.
- Within that context, a cheap code becomes available.
- Greedy spends too long improving the wrong coordinate before unlocking the useful tests.

There is a notable mismatch between two existing barriers:

- Greedy's superconstant failure can occur at near-information-theoretic optimum.
- The certified binary hardness construction uses bounded-size sets and has an optimum growing linearly with the number of hypotheses, up to constants depending on the set-size bound.

Therefore a useful hardness result would also distinguish **low-optimum** instances from the already constant-approximable, high-optimum regime.

---

## 4. Structural obstacles that any attack must respect

### 4.1 Restricting OPT is safe at one frontier, not at every level

For any disjoint family of subsets,

$$
\sum_i F(S_i)\le F(H).
\tag{4}
$$

Restrict an optimal tree on $H$ to each subset and delete redundant tests; disjointness prevents double-counting hypotheses at that frontier.

However, summing (4) over multiple recursive frontiers can pay for the same optimal cost repeatedly.

**Concrete example.** Let $n=2^d$ and provide the tests of a balanced binary identification hierarchy. At depth $j$, the subsets have size $n/2^j$, and each has optimum

$$
F(S)=|S|\log_2|S|.
$$

The sum of restricted optima at that frontier is $n(d-j)$. Summing over all nontrivial frontiers gives

$$
\sum_{j=0}^{d-1}n(d-j)=\frac{nd(d+1)}2,
$$

whereas $F(H)=nd$. The ratio is $(d+1)/2$.

This disproves the generic charging claim that all recursive restricted optima sum to $O(F(H))$. It is **not** a counterexample showing that a particular balanced-separator algorithm has poor actual cost; the balanced hierarchy itself is optimal.

### 4.2 Unweighted pair latency is the wrong objective

Let $\operatorname{sep}_T(h,g)$ be the number of tests shared by a pair, including the test that separates them. Then

$$
Q(T)=\sum_{\{h,g\}}\operatorname{sep}_T(h,g)
    =\sum_{v\text{ internal}}\binom{|S_v|}{2}.
\tag{5}
$$

UDT instead charges $|S_v|$. A node's pair charge overweights its identification charge by $(|S_v|-1)/2$.

Pair separation is excellent for finding a coarse partition, but an unweighted min-sum objective over all pairs is not interchangeable with average identification time.

The exact correction at a node of size $s$ is

$$
\binom{s}{2}\frac{2}{s-1}=s.
\tag{6}
$$

The catch is that these weights depend on the evolving candidate set.

### 4.3 A globally nonadaptive family can be much more expensive

For a complete binary hierarchy, take tests whose positive sets are the left-child subsets of its internal nodes. These sets are laminar. Any $q$ selected sets induce at most $q+1$ nonempty membership-signature cells.

Consequently, a family distinguishing all $n$ hypotheses needs at least $n-1$ tests, while an adaptive strategy has depth $\log_2 n$.

This rules out paying for one global identifying family on every hypothesis as a general constant-factor reduction. It does **not** rule out conditional batches, adaptive skipping, or replanning after responses.

### 4.4 Exact half-balanced separator search is too strong

A constant-cost approximation for a separator that leaves **every** cell of size at most exactly half the original set would solve a logarithmically hard set cover problem. Section 7.4 gives a unit-cost, binary, fully separating construction proving this directly.

A bicriteria relaxation of the balance threshold is therefore important, not merely cosmetic.

### 4.5 Small probability does not mean small expected cost

Take a rare block of $r=n^{3/4}$ hypotheses that can only be distinguished by singleton tests. The remaining hypotheses have a cheap binary code, and a test separates the rare block from the rest.

The rare block has probability $r/n=n^{-1/4}$, but its unavoidable contribution to the expected cost is

$$
\frac rn\left(\frac{r+1}{2}-\frac1r\right)
=\Theta(n^{1/2}).
$$

A polylogarithmic uniform sample misses the block with probability tending to one. Thus ordinary sampling that preserves split cardinalities can miss almost all of the objective.

---

## 5. Algorithmic attack routes

### Route A. Continuation-aware policy improvement

**Priority:** high; the best inexpensive first experiment.  
**Goal:** escape delayed-unlocking traps with an implementable polynomial algorithm, then prove a better worst-case ratio or find its obstruction.

Let $F_G(S)$ be the unnormalized cost of a complete greedy tree on $S$, using a fixed deterministic tie rule.

Define a new policy $R$ recursively. At $S$, choose a splitting test minimizing

$$
|S|+\sum_a F_G(S\cap\tau^{-1}(a)),
\tag{7}
$$

then apply $R$ recursively in the selected test's children.

The continuation value is a cost of a **complete** strategy. This differs substantially from choosing a shallow prefix and assigning zero cost to its unfinished leaves.

```text
Rollout(S):
    if |S| <= 1:
        return a leaf
    choose a splitting test t minimizing
        |S| + sum(GreedyCost(A) for nonempty outcome cells A of t on S)
    recursively build Rollout(A) for those cells
    return the resulting tree
```

#### A proved safety property

For every instance and every subset,

$$
F_R(S)\le F_G(S).
\tag{8}
$$

Proof: the greedy root test is an admissible candidate in (7). Its score is exactly $F_G(S)$. By induction on $|S|$, the recursive rollout cost in each chosen child is no larger than that child's greedy cost. Combining the two inequalities proves (8).

The construction terminates because every selected test has smaller nonempty children. A straightforward implementation is polynomial; a conservative bound with constant arity and ordinary table scans is $O(m^2n^3)$, before caching improvements.

The same argument gives monotonic improvement if one uses the **actual complete policy cost** from the previous round as the continuation value. Every fixed number of such policy-improvement rounds is polynomial. A number of rounds growing with $n$ needs a separate complexity argument.

Policy improvement itself is standard. The research question is its approximation behavior on UDT.

#### A grid variant on which continuation matters

For reproducibility, use $n=Cr$ hypotheses indexed by column and row, with $r$ a power of two. Provide:

1. A membership test for each column.
2. Row-code bit tests gated to each individual column.
3. A recursive row partition: a row node of size $s>1$ has a small child of size $1+\lfloor s/C\rfloor$ and the remaining rows as its other child. Add a membership test for the **small child only**, across all columns.

Use columns first, then column-gated code bits, then row decoys as the deterministic test ordering for greedy ties.

This is an explicitly specified grid-type variant inspired by the greedy lower-bound construction, not an assertion that every literal transcription of Appendix C.1 is identical. Adding arbitrary large descendant row sets can create much more balanced shortcuts and change the experiment.

For $C\ge4$, while the current row node has size $s>C^2$, its own small-child decoy is strictly larger than every descendant decoy and than the positive part of a column-gated test. Ancestor decoys are constant on that node. Greedy therefore follows the row hierarchy. Its small-child fraction is at most $2/C$, so each such query reveals at most $H_2(2/C)=O(\log C/C)$ bits of row information.

Reducing the row uncertainty from $\log_2r$ to at most $2\log_2C$ consequently requires expected cost at least

$$
\frac{\log_2r-2\log_2C}{H_2(2/C)}.
$$

Here $H_2$ is binary entropy. This establishes the delayed-unlocking lower bound for the specified variant whenever $r>C^2$.

In contrast, after a column membership test has a negative answer, only $C-1$ columns remain. If

$$
r>C(C-1),
$$

column membership is more balanced than any of the original small-child row decoys. Greedy then identifies the column, and the code-bit-first tie rule finishes its row in $\log_2r$ tests.

Hence the score of a column-root candidate in (7), divided by $n$, is

$$
\frac{C+1}{2}-\frac1C+\log_2r.
\tag{9}
$$

Equation (8) applied below that root makes (9) an upper bound on the full rollout's cost.

Taking $C=\Theta(\log n)$ and $r\gg C^2$ gives $O(\log n)$ rollout cost on this family, against an information lower bound of $\log_2n$. Thus this ordered variant's asymptotic greedy trap is genuinely removed, not just cosmetically improved.

#### Computed checks

| $n$ | $C$ | $r$ | Tests | Greedy mean | Column-first mean / rollout upper bound | Full rollout measured |
|---|---:|---:|---:|---:|---:|---|
| 256 | 4 | 64 | 91 | 8.984375 | 8.250000 | 8.250000 |
| 3072 | 12 | 256 | 363 | 22.412760 | 14.416667 | Not run; the bound follows from (8) and the computed candidate |

These are not global approximation guarantees.

#### Research targets and first falsification tests

- Test one, two, and three policy-improvement rounds on exact small instances and growing adversarial families.
- Seek a theorem that a fixed number of rounds gives $o(\log n/\log\log n)$, ideally a constant.
- Build **persistent-decoy** instances: after removing a group, new decoys should keep greedy continuations expensive.
- Test nested activation gates and adversarial tie orderings, not only the friendly grid above.
- If $C=\Theta(\log n)$, enumerating contexts indexed by all subsets of the $C$ groups can still yield a polynomial-size test family. This makes persistent-decoy lower-bound constructions worth investigating.
- Recompute OPT after adding decoys: new tests may create unintended cheap strategies.

The central desired structural lemma is that large continuation overestimates cannot persist through many profitable improvements in the uniform, bounded-arity model. It is plausible enough to test, but is not proved here and could be false.

### Route B. Majority-stable MSSC macros plus a nonduplicating certificate

**Priority:** high for theory.  
**Goal:** promote the paper's local MSSC connection into a global constant-cost construction.

LLM already connects imbalanced chains to min-sum set cover. A crucial ingredient is **majority-label stability**: within a chain, every test keeps the same majority outcome. Its minority set is then a fixed set, and progress down the chain is equivalent to covering more elements.

This stability is not automatic for an arbitrary path. A generic fixed-reference-hypothesis cover problem can select a test whose reference outcome is a tiny child, abandoning the intended majority spine. Standard MSSC guarantees therefore cannot simply be imported for arbitrary recursively selected paths.

Consider a valid spine macro with successive candidate sets

$$
S=S_0\supset S_1\supset\cdots\supset S_q.
$$

Its internal cost is

$$
W(P)=\sum_{i=0}^{q-1}|S_i|.
$$

Each test produces side cells $A_{i,a}$. Completing the macro optimally costs

$$
W(P)+\sum_{i,a}F(A_{i,a})+F(S_q).
\tag{10}
$$

Optimizing $W(P)$ alone ignores exactly the side-branch difficulty responsible for delayed unlocking.

#### Concrete algorithmic proposal

Search for majority-stable macros using an MSSC-style primitive, but score them using

$$
W(P)+\sum_{\text{unfinished leaves }A}U(A),
$$

where $U$ is a computable complete-policy upper bound, such as greedy or rollout. This extends Route A from one test to a long, cheaply optimized skewed segment.

The ordering problem with continuation terms is no longer ordinary MSSC. Its approximation or pricing algorithm is a genuine new bottleneck; do not assume the MSSC factor four survives unchanged.

#### The certificate that would actually remove the logarithm

Suppose a nonnegative, computable potential $L$ has $L(\{h\})=0$, $L(S)\le F(S)$, and the algorithm can choose a prefix $P$ whose unfinished leaves partition into subsets $A$, with

$$
W(P)\le c\left(L(S)-\sum_A L(A)\right).
\tag{11}
$$

Then recursion telescopes:

$$
F_{\mathrm{ALG}}(H)\le cL(H)\le cF(H).
$$

This is a sufficient condition, not an oracle we already know how to compute. Replacing the right-hand side by $cF(S)$ loses telescoping and returns to the frontier-overcounting obstacle.

A more flexible global-dual version could assign each optimal node or lower-bound witness to a bounded number of macros. The important condition is that witnesses are not restarted and charged again at every mass scale.

#### Where to look for $L$

- Entropy is a valid lower bound and handles genuinely balanced progress, but cannot account for a singleton-search instance with quadratic unnormalized cost.
- Valid MSSC-chain lower bounds can account for expensive skewed progress, but their witnesses must have controlled ownership across scales.
- The size-normalized pair relaxation in Route C may provide a shared dual certificate.

Start by seeking a constant bound on witness reuse. An $O(\log\log n)$ bound would already be interesting progress if it improves the current guarantee.

### Route C. Size-normalized pair/latency LPs with adaptive consistency

**Priority:** high-to-medium; promising shared infrastructure for Routes A and B.  
**Goal:** exploit pair-based coverage without optimizing the wrong objective.

The maximum-coverage machinery is attractive because each test separates a known set of pairs. But (5) shows that ordinary pair latency is too biased toward large candidate sets.

#### A constant-factor objective representation using only size levels

For a node of size $s\ge2$, let $j=\lfloor\log_2s\rfloor$. Charge each co-located pair at that node

$$
w_j=\frac{2}{2^j-1}.
$$

Then

$$
s\le \binom{s}{2}w_j
   =s\frac{s-1}{2^j-1}
   \le2s.
\tag{12}
$$

Therefore a tree's size-bucketed pair charge lies between its true unnormalized cost and twice that cost.

This representation uses only $O(\log n)$ size levels. The levels do not inherently create an extra logarithmic approximation factor: every actual node belongs to exactly one level.

The difficult part is enforcing that the pair occupancies really come from common adaptive candidate states.

#### Start from an exact formulation, then relax deliberately

An exponential occupation-flow LP has a variable $y_{S,\tau}$ for using test $\tau$ at state $S$:

- Total root outgoing flow is one.
- Each other non-singleton state's outgoing flow equals its incoming flow from parent-test outcomes.
- Singleton states are sinks.
- Each selected test sends its state flow to all its nonempty outcome cells.
- The objective is $\sum_{S,\tau}|S|y_{S,\tau}$.

With all states included, this is exact. Mixing strategies does not improve a linear expected-cost objective over the optimal deterministic tree. Its problem is exponentially many states, not an integrality gap.

A polynomial relaxation could project this flow onto:

- Individual completion/survival marginals.
- Pair co-location marginals indexed by time and size level.
- Local test-response histories.
- Triple or higher-order consistency constraints.

Any such proposal must be demonstrated to be a relaxation of real trees. Merely omitting inequalities from a maximization-form Bellman lower-bound LP can move the bound in the wrong direction and overestimate OPT.

#### Key constraints and failure modes

1. Hypotheses still in the same state receive the same next test.
2. Unseparated pairs form equivalence classes; arbitrary pair cuts can violate transitivity.
3. A hypothesis completes only when all competitors have been eliminated along its own consistent path.
4. Size-level membership must reflect the cardinality of a common state, not an independently chosen label for each pair.
5. Rare deep tails must remain in the objective.

The algorithmic target is a constant-gap relaxation with global rounding into adaptive blocks. Solving an unrelated local LP at every recursive level would reintroduce the charging problem.

#### A warning about overly strong survival-profile goals

For a complete tree,

$$
C(T)=\frac1n\sum_{t\ge0}|\{h:d_T(h)>t\}|.
\tag{13}
$$

An integral comparison of survival curves is useful. However, asking one polynomial policy to dominate the **best deadline policy** within a constant time stretch at every deadline is too strong: at the optimum worst-case depth the deadline optimum has zero survivors, forcing a constant approximation for the logarithmically hard worst-case problem.

A viable rounding argument should control the integral, or allow an explicitly budgeted tail error, rather than demand this pointwise zero-tail property.

#### First experiments

Compare pair-only, size-bucketed, and local-history relaxations with exact subset DP. Search especially for:

- The grid family.
- A large cheap region plus a small singleton-hard block.
- Incompatible fractional response histories.
- Instances whose root is unbalanced but whose correct child is easy.

An integrality-gap construction here would be useful information even if it rules out the proposed relaxation.

### Route D. Compress the long-prefix optimization

**Priority:** medium; directly targets the subexponential bottleneck.  
**Goal:** replace exhaustive prefix optimization by a structured polynomial procedure.

For depth budget $B$, let

$$
D_B(S)=\min_P W(P),
$$

where every leaf of $P$ is either a singleton or an unfinished leaf at depth exactly $B$. This is the minimum truncated expected-depth objective, in unnormalized form.

Two elementary facts explain the original algorithm:

$$
D_B(S)\le F(S),
\qquad
|\text{unfinished hypotheses}|\le W(P)/B.
\tag{14}
$$

The second fact follows because every unfinished hypothesis pays all $B$ prefix tests.

#### A useful conditional hybrid lemma

Fix $0<\gamma<\beta<1$ and use the original universe size $n$.

Suppose a polynomial procedure could return an $a$-approximation to $D_B(S)$ for $B=\lceil n^\beta\rceil$, for the subproblems needed by the hybrid.

- If the local greedy cost is at least $n^\gamma$, (2) and the crude greedy bound certify a local optimum at least $n^\gamma/O(\log n)$. Greedy is then an $O(1/\gamma)$ approximation.
- Otherwise, the local optimum is below $n^\gamma$. The prefix procedure costs at most $aF(S)$ and leaves at most an $a n^{\gamma-\beta}$ fraction unfinished.
- For fixed parameters and sufficiently large $n$, the number of prefix generations is $O(1/(\beta-\gamma))$: along a recursive branch the number of hypotheses decreases by a fixed polynomial factor in the original $n$.
- At each generation, disjointness gives a total prefix cost at most $aF(H)$. Greedy terminal subproblems are mutually disjoint and can be charged once.

This would yield a constant approximation.

**Important circularity check:** if $|S|\le B$, the truncated problem can already be the full UDT problem on $S$. Thus declaring a general constant prefix oracle does not make the original difficulty disappear. The useful task is to construct it through actual compression, or to provide a separate valid charging treatment of small residual states.

#### Compression ideas worth testing

- Replace long majority-stable stretches by MSSC macros.
- Merge histories only when their relevant restricted-test partitions and continuation values are equivalent or safely approximable.
- Enumerate a bounded number of genuinely branching activation events, not every test on a long skewed path.
- Maintain certified aggregate error budgets for discarded histories.
- Use continuation values instead of zero-cost unfinished leaves when a short lookahead cannot reveal any completed hypothesis.

Every returned tree already has only $O(n)$ nodes after redundant tests are removed. The issue is **search-space compression**, not output compression.

A single-exponential dependence on a promised average optimum, such as $2^{O(C_{\mathrm{OPT}})}\operatorname{poly}(n,m)$, would be useful at $C_{\mathrm{OPT}}=O(\log n)$. It would not by itself settle all polylogarithmic or other subpolynomial-optimum regimes. Average depth also does not bound maximum depth.

Simply letting $\alpha$ shrink with $n$ in (3) is not a polynomial-time constant approximation: the ratio grows as $1/\alpha$, and the original prefix depth still contains a logarithmic factor.

### Route E. Cost-sensitive coresets and structural intermediate targets

**Priority:** lower as a stand-alone approach; useful supporting work.

#### E1. Coresets for continuation values, not ordinary split balance

The rare-block example rules out trusting an unweighted uniform sample as a generic certificate.

A more plausible objective is to preserve the complete-policy continuation values actually used by Route A, or bounded collections of macro objectives used by Route B.

Possible ingredients:

- Importance sampling based on certified query-cost upper bounds.
- Rebuilding summaries after conditioning on a candidate state.
- Exact evaluation of shortlisted tests before making an irreversible choice.
- A global bound on the sum of omitted expected costs.

Sampling by one greedy tree's depth is not automatically sufficient: another candidate policy may put its expensive tail on different hypotheses. The missing theorem is a sensitivity bound for the relevant continuation-value class under conditioning.

The payoff would be faster macro search or history compression. A coreset alone does not establish an approximation guarantee.

#### E2. Bounded-minority instances as an intermediate theorem

Suppose every binary test has a globally designated minority set of size at most a fixed $d$. While a candidate set is large, the complementary outcome is a stable majority, and side branches have bounded size.

This is a particularly clean place to study:

- An MSSC backbone plus exact bounded-size side-branch optimization.
- The additive cost of side-branch identification.
- Constants approaching the certified $2-\varepsilon$ hardness threshold.

Greedy is already constant-factor in the corresponding high-cost regime, so this does not solve the general gap. A sharper approximation here could nevertheless expose the correct ownership/coding lemma before confronting large, overlapping side branches.

Laminar and gated-code families are also useful structural benchmarks. Do not assume that a laminar-looking incidence structure automatically makes the full optimization easy; any claimed tractability needs its own proof.

---

## 6. A primitive that is already available, and what it does not buy

For a subset $S$, let a separating family be a collection of tests whose joint outcome cells all have size at most $|S|/2$.

Following an optimal tree's majority path until the candidate size falls to half provides such a family of cost at most

$$
2F(S)/|S|.
$$

Each test along that path is paid by at least half of $S$, which proves the bound.

Reduce tests to the pairs they separate and use budgeted maximum coverage. A family whose cells have size at most $f|S|$ separates at least $(1-f)|S|^2/2$ pairs. A coverage ratio $\gamma$ therefore guarantees maximum remaining cell size at most

$$
\sqrt{1-\gamma(1-f)}\,|S|.
$$

With $f=1/2$ and $\gamma=1-1/e$,

$$
q=\sqrt{\frac{e+1}{2e}}\approx0.827006.
$$

The current 2026 paper formalizes this as a bicriteria separating-subfamily approximation. Unit costs also allow trying integer cardinality budgets; refining budget-guess constants does not address the research gap.

Thus a constant-cost, constant-shrinkage primitive exists. Recursing and bounding each phase by $O(F(S))$ still incurs the hierarchy-depth factor.

The next theorem must control **amortization across phases**, not merely improve the separator's coverage constant.

---

## 7. Hardness routes

### H1. Transfer stronger MSSC hardness without losing it to binary coding

**Priority:** high among hardness approaches; a sharply defined first target beyond binary $2-\varepsilon$.

The original binary reduction supplies an unusually useful quantitative template. Let $A$ be the optimum average MSSC cost and let $d$ be the maximum set size. Its Lemmas 4.5 and 4.6 give:

$$
C^*_{\mathrm{binary}}\le A+\lceil\log_2d\rceil,
$$

and any binary tree of average cost $C$ can be converted into an MSSC ordering of average cost at most $C+1$.

An $\alpha$-approximation for the binary instance would therefore give an MSSC solution of cost at most

$$
\alpha A+\alpha\lceil\log_2d\rceil+1.
\tag{15}
$$

For fixed $d$, $A\ge N/(2d)$, so the coding overhead vanishes asymptotically. This is why bounded-cardinality MSSC hardness transfers cleanly.

A sufficient condition for transferring the unrestricted MSSC $4-\varepsilon$ hardness almost intact would be a gap-hard family with

$$
A/\log d\longrightarrow\infty.
$$

**Research task:** obtain such a family through gap-preserving latency inflation, or prove that a natural inflation scheme fails.

Pitfalls:

- Duplicating elements inside the same sets does not increase their cover times.
- Independent copies can change the optimal interleaving and the gap.
- Charging multiple units per query changes the unit-cost model.
- Binary auxiliary tests can be queried before the membership test. The original reduction handles this through solution extraction, not by assuming a mandatory test order.

This route aims first at a larger binary constant, not at a superconstant NP-hardness factor.

### H2. Gated latency amplification, potentially for every fixed constant

**Priority:** medium; ambitious and technically risky.

A negative resolution of the polynomial constant-factor question could prove:

> For every fixed $R$, approximating binary UDT within $R$ is NP-hard.

This is stronger than a hardness result for one larger constant. It is not ruled out by the subexponential algorithms if the reduction's polynomial degree grows with $R$.

Plain independent composition does not amplify ratios. If a hard part has costs $A$ versus $\rho A$ and both cases acquire a common coding cost $B$, the resulting ratio is

$$
\frac{\rho A+B}{A+B}<\rho.
$$

Likewise, independently identifying two coordinates usually adds their costs rather than multiplies their approximation gaps.

A plausible amplification gadget must make a wrong or incompatible outer choice cause expensive identification of many inner hypotheses. Conditional tests that are informative in one group and constant outside it provide a possible implementation language.

Required proof obligations:

1. All hypotheses remain equiprobable.
2. Every available test is binary and unit-cost.
3. Every pair is distinguishable.
4. Inner tests cannot bypass the intended gate cheaply.
5. The no-case lower bound holds for **all** adaptive trees, not just trees following a proposed canonical order.
6. The expensive behavior affects enough hypothesis mass to create an average-cost gap.
7. Extra coding and filler hypotheses do not dilute that gap.

Precedence constraints cannot simply be imposed: they define a different problem. Any apparent prerequisite must arise from the response table itself.

A useful preliminary result would be a constant-gap hardness family with $C_{\mathrm{OPT}}=\Theta(\log n)$ in both cases. That would test the difficult algorithmic regime more directly than the existing high-cost binary reduction.

### H3. Fine-grained tradeoffs and the reduction-blowup constraint

**Priority:** high for keeping hardness proposals realistic.

Suppose a deterministic gap reduction from a 3-SAT instance with $N$ variables produces

$$
n=O(N^d),\qquad m=N^{O(1)},\qquad d\ge1,
$$

and has hardness gap $\rho$. If

$$
\frac{9+\varepsilon}{\rho}<\alpha<\frac1d,
$$

then (3) distinguishes the gap in time

$$
2^{O(N^{d\alpha}\log^2N)}=2^{o(N)},
$$

contradicting ETH.

In particular, a reduction of degree $d$ with $\rho>9d$ is incompatible with ETH, choosing $\varepsilon$ sufficiently small. This is a restriction on that reduction's parameters, not a universal upper bound of nine on NP-hardness.

The same fixed-$\alpha$ argument rules out a **single polynomial-size reduction** proving a hardness factor $f(n)\to\infty$: a fixed constant approximation eventually beats $f(n)$.

However, reductions for every fixed $R$ with degrees $d(R)$ growing at least proportionally to $R$ can remain compatible with ETH. They cannot automatically be combined into a growing-factor polynomial reduction.

Fine-grained lower bounds should therefore specify:

- The target approximation factor.
- The allowed running-time exponent.
- The hypothesis-count blowup.
- The test-count blowup.
- Whether the reduction parameter is fixed or input-dependent.

Avoid qualitative claims of "subexponential hardness" that conflict with an already available exponent in (3).

### H4. A rigorous barrier for exact balanced-block strategies

**Status:** derived reduction for a primitive, not UDT inapproximability.

Start with a feasible unit-cost set cover instance on $N$ real elements. Add $N$ dummy hypotheses.

Provide binary unit-cost tests:

- For each original set, membership in that set of real elements; every dummy answers zero.
- A singleton test for every real or dummy hypothesis.

The singleton tests make the full decision-tree instance valid. Consider only the primitive of selecting a minimum-size test family whose joint cells all have size at most $N$, exactly half the $2N$ hypotheses.

Every set cover yields such a separator: all dummies form a size-$N$ cell, and all other cells contain only real elements.

Conversely, suppose a separator selects $c$ original-set tests and $h$ helper singleton tests. Let $r$ real elements remain uncovered by the original-set tests. If $h_D$ dummy singletons and $h_R$ of those uncovered real singletons are selected, the all-zero cell has size

$$
N-h_D+r-h_R.
$$

Its size is at most $N$, so

$$
r\le h_D+h_R\le h.
$$

Cover each remaining real element using any one original set containing it. This produces a set cover of size at most $c+h$, the separator cost. Hence

$$
\mathrm{OPT}_{\mathrm{exact\ half\ separator}}
=\mathrm{OPT}_{\mathrm{set\ cover}}.
\tag{16}
$$

This transfers set cover's logarithmic inapproximability to the exact-half separator primitive even with binary unit-cost tests and full pairwise distinguishability.

It does **not** transfer to average-depth UDT. Inside the dummy block, all original-set tests are constant and only singleton tests distinguish hypotheses. Its contribution alone to the full tree's mean cost is asymptotically $N/4$. That baseline can swamp the set cover gap.

This example simultaneously explains:

- Why exact-balance block search is an unsuitable constant oracle.
- Why bicriteria balance slack is valuable.
- Why set-cover hardness and dummy padding do not automatically yield logarithmic hardness for uniform average depth.

---

## 8. Computational evidence collected for this note

All computations used the exact stated objectives. No performance conclusion is inferred merely from a split-quality proxy.

### 8.1 Policy-improvement sanity checks

For 180 deterministic-seed binary instances:

- $n=2,\ldots,10$, with 20 instances at each size.
- Tests were all singleton tests plus eight sampled nonconstant binary columns, deduplicated.
- Seed: `20261011`.
- Exact subset DP computed the optimum.
- Complete greedy, one policy-improvement round, and two rounds were evaluated.

Every instance satisfied

$$
F_{\mathrm{OPT}}\le F_{R_2}\le F_{R_1}\le F_G.
$$

One round strictly improved greedy on four instances and matched OPT on all 180. These tiny, singleton-rich instances are a sanity check only; matching OPT here is not evidence of general exactness or a constant ratio.

### 8.2 Structural checks

For balanced laminar hierarchies with $n=2,4,8,16$:

- Exact DP returned mean optimum $\log_2n$.
- Repeated restricted-OPT charging had ratio $(\log_2n+1)/2$.
- The normalized-pair identity (6) matched the true cost.
- Exhaustive selection of test subfamilies verified the bound of at most one more signature cell than selected tests.

For 80 small set cover instances, exact enumeration verified (16). Additional arbitrary feasible separator families were checked for cost-preserving cover extraction.

The grid checks in Route A used the small-child-only decoy construction specified there.

### 8.3 What has not been done

- No improvement to the $O(\log n/\log\log n)$ asymptotic order has been proved. The [formal follow-up](uniform-decision-tree-formal-bounds.md) establishes a lower-order greedy refinement and a rollout bonus.
- No polynomial LP or constant-gap rounding algorithm has been completed.
- No larger binary UDT hardness factor has been proved.
- No full audit of every proof in the cited manuscripts has been performed.
- No exhaustive claim about all literature or novelty is made.

---

## 9. Suggested research sequence and stopping criteria

### First stage: establish a meaningful adversarial benchmark

1. Implement bitset subset DP for small instances and a memoized continuation-aware policy.
2. Reproduce the specified grid, then add persistent and nested decoys.
3. Include rare hard tails, overlapping side branches, and reordered tests.
4. Measure actual mean depth, exact optimum where feasible, and scaling of their ratio.
5. Keep a complete greedy tree as a baseline and compare complete output trees.

Do not continue optimizing a heuristic solely because it performs well on one friendly unlocking example.

### Second stage: choose the theorem bottleneck

**If rollout survives adversarial growth:** analyze its Bellman improvement against a shared lower-bound certificate, not only against greedy's cost.

**If rollout fails:** preserve the no-regression observation and extract the smallest persistent-decoy mechanism. Use it to design a macro oracle or prove a lower bound for fixed-depth/fixed-round policy improvement.

**In parallel conceptually:** formulate the size-bucketed pair relaxation and search for its smallest consistency gap. Only add higher-order constraints when a concrete gap identifies the missing information.

### Third stage: attack hardness with the correct model

1. Try the latency-inflated MSSC route using inequality (15).
2. If pursuing amplification, write yes/no average costs including all coding overhead before designing the full gadget.
3. State the blowup degree as a function of the target constant.
4. Check every proposed result against the ETH inequality in H3.

### The most valuable near-term outcomes

- A polynomial algorithm with a rigorously smaller-than-greedy worst-case ratio.
- A constant approximation on a substantively broader structural class, with a reusable charging lemma.
- A constant-gap size-normalized relaxation, or a decisive integrality-gap obstruction.
- A stronger binary hardness constant.
- A low-optimum constant-gap hardness construction.
- A clean lower bound for continuation-aware or bounded-macro policies that explains what information a successful algorithm must use.

---

## 10. Bottom line

The most promising route is to replace **myopic split quality** by **continuation-aware adaptive blocks**, while building a **single global mass-sensitive certificate** for their cost.

Three facts make this more than a generic suggestion:

1. Complete greedy continuations give an immediately implementable, provably safe rollout, and expose a real unlocking effect on the specified grid.
2. Size-normalized pair charges recover the actual average-depth objective; size buckets preserve it within a factor of two.
3. Existing constant bicriteria separators isolate the missing step: cross-level amortization, not local separator quality.

On the negative side, a successful hardness argument must preserve uniformity, unit costs, bounded outcomes, and average latency simultaneously. The straightforward unrestricted-arity reduction, exact-separator hardness, independent products, and weight cloning do not accomplish this automatically.

The central open choice is therefore between a global constant-factor charging/rounding theorem and a genuinely gated hardness construction whose difficulty survives those four restrictions.

---

## 11. Formal follow-up: a proved lower-order improvement

**Status after clarification:** this section does not meet the requested asymptotic target. Even with quasipolynomial time allowed, no unconditional $o(\log n/\log\log n)$ guarantee has been obtained. Section 12 of [the proof-only follow-up](uniform-decision-tree-formal-bounds.md) records the stronger lookahead attempt and the precise outstanding gaps.

The proof-only continuation pursues Routes A and B. Set $L=\log_2n$, $\kappa=\log_2K$, and $\ell=\log_2\log_Kn$. It proves

$$
\frac{C_G}{C_{\mathrm{OPT}}}
\le\frac{4L}{\ell}-\frac{L}{4\ell^3}
$$

for $\ell\ge16$, and, for fixed $K$ and sufficiently large $n$,

$$
\frac{C_R}{C_{\mathrm{OPT}}}
\le\frac{4L}{\ell}-\frac{L}{4\ell^3}
-\frac{\kappa}{2\ell^2}.
$$

The main refinement comes from charging the identification entropy remaining inside an optimal MSSC spine's exit groups. The rollout adds a separate Bellman bonus. These are smaller explicit approximation factors, but their asymptotic order and limiting leading constant remain unchanged.

See [the complete formal proofs](uniform-decision-tree-formal-bounds.md). No algorithm was implemented for this follow-up.

---

## 12. Next proof route: cost-aware coded spines

The latest attempt makes the macro's side-branch costs explicit rather than optimizing only cover time.

A useful verified source is Bansal, Huang, and Zhu's [2025 correlated-Pandora paper](https://arxiv.org/abs/2509.17029v2). Its factor-four theorem compares against **partially adaptive** policies: inspection order is fixed, stopping is adaptive. It does not close the fully adaptive UDT gap.

The [formal continuation](uniform-decision-tree-formal-bounds.md), Section 13, proves:

- A $4+\varepsilon$ cost-aware spine oracle when each observed test outcome has a supplied complete code with a fixed certified maximum-depth cap.
- A quasipolynomial transfer combining that oracle with bounded-depth adaptive prefixes and exact shallow-code search.
- A constant-factor guarantee on the specified column/row grid even when the column-selection spine is longer than every fixed polylogarithmic query horizon under consideration.

Unlike a hypothetical MSSC-with-continuations oracle, the computational primitive and its benchmark guarantee are now proved. The remaining obligation is structural: show that the prefix-plus-coded-spine benchmark is within $o(\log n/\log\log n)$ of unrestricted optimum on every instance.

That statement remains unproved. Fixed caps cannot be silently replaced by conditional mean costs: observations can make those means increase by an unbounded factor. Nested activation contexts remain an important stress case.

---

## 13. Proved improvements beyond parameter substitution

The [new standalone proof](uniform-decision-tree-improved-tradeoffs.md) establishes two additional mechanisms:

1. A prefix generation costs at most the smaller of OPT and its capped conditional cost times surviving mass. This makes the sum of prefix costs much smaller than the number of generations times OPT.
2. A proper uniform tree of height $H$ has total leaf depth at least $H(H+3)/2$. This certifies a complete bounded-height exact search in the low-cost case.

The resulting unconditional guarantees include:

- For target factor $c\,\log n/\log\log n$, a quasipolynomial time power arbitrarily close to $2+4/c$, compared with $2+9/c$ from the supplied tradeoff. For coefficient one, this changes powers approaching 11 to powers approaching 6.
- The near-quasipolynomial coefficient refinement leaves its growing runtime power in the same order and is not counted as a qualifying growing-exponent improvement.
- Combining the height certificate with a bounded number of prefix generations gives a $37/5+\varepsilon$ approximation in $2^{O(n^{3/4}\log(Km))}$ time, compared with approximately 12 at that exponent in the supplied curve.
- A 10-approximation has time power arbitrarily close above $5/8$, improving on $9/10$ in the supplied tradeoff. Every fixed factor above four is attainable in subexponential time by the height-filter method.

The subsequent shared-budget continuation improves that 10-approximation power further to every fixed value above $143/288\approx0.496528$, and improves the leading curve to $5/\alpha$ for every fixed $\alpha$.

Its new inequality charges a prefix generation against OPT minus the conditional-optimal costs of all states that have already terminated. Generation-dependent terminal budgets $R-i$ then cancel the repeated prefix charges. The proof uses only disjointness, valid greedy guarantees, and the height certificate; it does not assume a new macro oracle or a conditional entropy-excess inequality.

The constant-power results genuinely improve the stated tradeoff bounds, rather than merely reparameterizing them. A little-$o$ reduction of a growing runtime power, strict-quasipolynomial little-$o$ approximation, and polynomial-time constant approximation remain unresolved. Literature-wide priority is not asserted.

---

## References and verification notes

### LLM: approximation baseline and prefix algorithm

Ray Li, Percy Liang, and Stephen Mussmann. *A Tight Analysis of Greedy Yields Subexponential Time Approximation for Uniform Decision Tree*. ArXiv v2, 2019; SODA 2020, pp. 102-121.

- [Local paper](1906.11385v2.pdf)
- [ArXiv v2](https://arxiv.org/abs/1906.11385v2)
- Checked: model and greedy definition; Theorems 3.1-3.2; Proposition 3.3; Sections 4-7, related work, conclusion, and the relevant grid-construction passage.
- The MSSC factor-four theorem used here is attributed there to Feige, Lovasz, and Tetali, *Approximating Min Sum Set Cover*, Algorithmica 40(4), 219-234, 2004.

### CPR: model-correct hardness

Venkatesan T. Chakaravarthy, Vinayaka Pandit, Sambuddha Roy, Pranjal Awasthi, and Mukesh K. Mohania. *Decision Trees for Entity Identification: Approximation Algorithms and Hardness Results*. ACM Transactions on Algorithms 7(2), Article 15, 2011.

- [Author-hosted journal PDF](https://www.cse.iitd.ac.in/~pandit/TALG_Published.pdf)
- [DOI](https://doi.org/10.1145/1921659.1921661)
- Checked: Theorems 4.2-4.4; Lemmas 4.5-4.6 and 4.8; Proposition 4.7.
- This is the source for the distinction between unrestricted-arity $4-\varepsilon$ and binary $2-\varepsilon$ hardness.

### S26 withdrawal: do not treat the initial claim as a theorem

Michal Szyfelbein. ArXiv:2604.12036.

- [Initial v1 claim](https://arxiv.org/abs/2604.12036v1)
- [Explicit withdrawal and explanation in v2](https://arxiv.org/abs/2604.12036v2)
- Checked directly in arXiv version metadata, not inferred from search summaries.

### S26 current: separating-subfamily prior art

Michal Szyfelbein. *Simpler Logarithmic Approximation Algorithms for the Optimal Decision Tree and Adaptive Set Cover*. ArXiv:2604.12036v3, August 2026.

- [Current v3](https://arxiv.org/abs/2604.12036v3)
- [Current PDF](https://arxiv.org/pdf/2604.12036v3)
- Checked: abstract and introduction; Theorem 1's logarithmic factor; separating-subfamily and maximum-coverage machinery; conclusion and primitive hardness discussion.
- Used as a claimed logarithmic result and as prior art for the primitive, not as an independently certified constant-factor solution.
