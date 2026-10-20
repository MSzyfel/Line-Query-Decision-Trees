# General uniform decision trees: continuation and local-surgery audit

Date: 2026-10-18. Auxiliary research notes; the article sources were not edited.

Model: finitely many equiprobable hypotheses, unit-cost binary tests, and
polynomial time in the explicit hypothesis/test matrix. The construction is
already binary, so it applies to every fixed response bound at least two.

## Status

**Proved here:** a strict one-test insertion/pruning local optimum can retain
an approximation gap of order `log n / log log n`. There is an explicit
linear-size test family. An orthogonal-code extension gives arbitrarily long
constant-horizon neutral plateaus along the intended column-then-code route.

**Implemented and checked:** an exact audit of every splitting test at every
incumbent node, plus two-bit and three-bit plateau checks. The script is
[research-general-continuation.py](research-general-continuation.py).

**Not proved:** an improved approximation algorithm for general UDT. These
are counterexamples to particular cheap continuation substitutes, not
complexity lower bounds and not counterexamples to actual rollout with fresh
complete greedy continuations. Literature-wide novelty is not asserted.

The existing notes already give polynomial algorithms for a fixed number
of complete-policy improvement rounds and for the fixed-horizon version of
the probe/retain/recombine/descent process. That specialization is not new
progress here. Their global approximation analysis remains unresolved.

## 1. Why inspect pruning rather than another shallow rollout?

The planar argument in `sections/06-expected-depth.tex`, especially the
witness-path restriction credit and stage-to-tree conversion, charges work
to queries that become constant under restriction. This motivates a very
cheap general-instance method: keep one complete incumbent tree, move a
test to the front of one subtree, and finish both outcomes by pruning that
same incumbent subtree.

This operation has a polynomial implementation with an integer-descent
bound. It could in principle avoid the exponent that grows with the number
of nested complete-policy evaluations. The obstruction below shows why
that particular shortcut cannot establish a better ratio by proving that
every resulting local optimum is good.

For context, I read the abstract, model, Theorem 3.1 discussion, majority
chain analysis, and Appendix C.1 of the supplied `1906.11385v2.pdf`, using
the local extraction `tmp/pdfs/general-1906-v2.txt`. Its grid/gated-code
construction is the starting point; the complement-pair and orthogonal
block modifications below enforce additional restriction stability.

## 2. Exact all-node insertion credits

For a complete tree `T` and subset `A`, write `V_T(A)` for the unnormalized
cost of its pruned restriction to `A`. At a node `v`, let its two child leaf
sets be `L_v,R_v`, and let `S_v=L_v union R_v`.

For one test with outcome cells `A_0,A_1`, define

```
Gamma_v = V_(T_v)(S_v) - V_(T_v)(S_v intersect A_0)
                              - V_(T_v)(S_v intersect A_1).
```

The cost improvement from inserting that test at `v` is exactly

```
Gamma_v - |S_v|.
```

The credits for all nodes can be calculated in one bottom-up pass:

```
Gamma_v = Gamma_left + Gamma_right + |S_v|
          - sum_a |S_v intersect A_a| * indicator[
                 L_v intersect A_a and R_v intersect A_a are both nonempty].
```

**Proof.** The last term is precisely the contribution of the original
node after restriction: it remains a query in one outcome cell exactly
when both original children still occur in that cell. Add the independent
child contributions. Leaves have zero credit.

Thus every candidate at every incumbent node can be audited in `O(m n)`
arithmetic operations once leaf outcomes are directly accessible. Bitset
representations have an additional polynomial bit-operation cost.

Adopt the best strictly improving insertion and repeat. Each successful
move decreases the integer external path length by at least one. Since a
proper tree has cost at most `n(n-1)`, at most `n(n-1)` moves occur. A direct
implementation is polynomial; no horizon grows with `n` in an exponent.
The theorem below concerns the possible final local optima of this method.

## 3. A full-order bad local optimum

Let there be `C` columns and `r=2^b` rows. A hypothesis is `(column,row)`.
Identify each row with its `b`-bit string, and pair each row `x` with its
bitwise complement. There are `q=r/2` such pairs.

Construct a row tree `R` on these pairs. At a node containing `s>1` pairs,
choose a child with

```
a(s) = min(floor(s/2), max(1, floor(2s/C)))
```

pairs, and put the other pairs in the other child. Every main-row child is
therefore a union of complete complement pairs. At a terminal pair, use
one query to distinguish its two rows.

The available tests are:

1. Membership in every column.
2. Every row-coordinate bit, gated to every individual column.
3. Membership in the small child at every internal node of `R`, across all
   columns.

There are `m=(r-1)+C+Cb=O(n)` tests, where `n=Cr`. They separate all pairs.

The incumbent `T_bad` first executes `R` and then performs uniform column
singleton search. If

```
Q(C) = C(C+1)/2 - 1,
```

its mean cost is

```
C_bad = C_R + Q(C)/C.
```

Column-first search followed by the gated binary row code has mean cost

```
C_good = Q(C)/C + b,
```

and consequently `OPT <= C_good`.

### 3.1 No row-test insertion is strictly profitable

Consider a row-state subtree with `s` rows and all `C` columns. Any splitting
row test is membership in a descendant small-child row set `D`. Let `P`
be its parent row node, and let there be `ell` strict ancestors of `P`
inside the current row subtree. Its exact pruning credit is

```
C * (|P| + ell * |D|).
```

At `P`, the query disappears from both restrictions. At every strict
ancestor, it disappears only for the `D` restriction and saves `|D|`.
All other row nodes and every column search retain their combined costs.

Every off-path sibling of such an ancestor has at least `|D|` rows. This
follows because `a(s)` is nondecreasing, is at most `s/2`, and pair-terminal
small children have one row. The siblings are disjoint, so

```
|P| + ell * |D| <= s.
```

Hence credit does not exceed the insertion cost `Cs`.

### 3.2 Column insertions are neutral

At every complete row state, moving any column test to the front preserves
the row cost and changes each row's column cost from `Q(C)` to

```
C + Q(C-1) = Q(C).
```

Thus its credit is exactly `Cs`, equal to its insertion cost. Within an
existing column-search subtree, all useful tests are singleton tests on
the remaining columns. Their uniform search cost is already optimal.

### 3.3 Gated row-bit insertions are strictly worse

At a complete-pair row state containing `s` rows, a column-gated coordinate
selects exactly one row from every pair in that column.

On its positive branch, every main-row child remains nonempty. The only
row queries pruned are the terminal pair queries: their total credit is
`s/2`. On its negative branch, the other `C-1` columns retain every row, so
no row query is pruned. Column-search credit is

```
(s/2) * (Q(C)-Q(C-1)) = Cs/2.
```

The total credit is exactly `(C+1)s/2`, strictly less than the insertion
cost `Cs` for `C>1`.

Inside a terminal single-row state, a gated bit is either constant or a
column singleton test. This handles every incumbent node and every
available test. **Therefore `T_bad` is a strict-insertion local optimum.**

### 3.4 Its gap has the entire currently known asymptotic order

At a pair-state of size `s>C^2`, the small-child fraction is at most `3/C`.
For sufficiently large `C`, each such query reveals at most
`H_2(3/C)=O(log C/C)` bits about the pair index. Stopping once at most
`C^2` pairs remain leaves at most `2 log C` bits of uncertainty. Therefore

```
C_R >= (log q - 2 log C) / H_2(3/C).
```

Set `C=b` and let `b` grow. Then `C_bad=Omega(b^2/log b)`, while
`C_good=O(b)`. Since `log n=Theta(b)`,

```
C_bad / OPT >= C_bad / C_good
             = Omega(log n / log log n).
```

This is a local-search obstruction, not a UDT hardness theorem. It does
not prove that strictly descending from a particular greedy baseline
reaches this particular incumbent.

## 4. A column query followed by one row bit does not fix the trap

The obvious depth-two surgery is to ask a column test and, on its positive
branch, ask a gated row bit, completing all leaves by pruning `T_bad`.
It is exactly **neutral**. The column query costs and saves `Cr`. The row
bit, now on the single-column branch, costs `r` and saves the `r` terminal
pair queries. Total prefix cost and pruning credit both equal `Cr+r`.

This answers a concrete possible repair, but is not a theorem that every
depth-two move is nonimproving.

Replacing the positive column branch by a **complete** binary row code
does escape whenever `C_R>b`: the column move is neutral, while that
replacement saves `r(C_R-b)`. With gated-code tests ahead of decoys in a
fixed tie rule, greedy constructs that complete `b`-query code on the
single-column state. This is why actual complete-policy continuations
retain value after the cheap pruning substitute fails.

## 5. Arbitrary fixed horizons along the useful coding route

There is a stronger plateau construction. Fix a constant `k`. Choose
vectors `v_1,...,v_b` in `F_2^d`, spanning the space, such that every at most
`k` vectors are linearly independent, with `d=O(k log b)`.

This is explicit in polynomial time for fixed `k`: start with the standard
basis, then choose each new vector outside the spans of every at most
`k-1` previous vectors. At most

```
sum_(j=0)^(k-1) binomial(b,j) 2^j
```

vectors are forbidden; choose `2^d` larger than this count. For fixed `k`,
enumerating these forbidden spans and finding each vector costs
`b^{O(k)}`. For sufficiently large `b`, `d<b`.

Let

```
L = { (v_1 dot z,...,v_b dot z) : z in F_2^d }.
```

Partition the `2^b` rows into affine cosets of `L`. Every assignment to any
at most `k` coordinate bits occurs equally often in every coset. Put the
imbalanced decoy tree on the cosets, and use a balanced `d`-query basis
tree inside every coset. As before, make each row-tree small-child set an
available row test, and provide all column-gated original coordinate bits.

**Plateau lemma.** Activate one column. Then execute any adaptive prefix
of depth at most `k` consisting of gated row-coordinate tests, and complete
the leaves by pruning the incumbent row tree. Its total cost equals the
original incumbent cost on that column, after suppressing repeated or
constant tests.

**Proof.** Each prefix transcript imposes at most `k` independent affine
constraints. Every coset retains an equal positive number of rows, so
every decoy query above the cosets remains a query in every transcript
restriction. Their combined costs are unchanged.

Inside a coset, sequentially querying the basis coordinates of an affine
subspace of dimension `d-t` uses exactly `d-t` nonconstant queries on every
path. Thus a transcript of depth `t` saves exactly `t` internal-basis
queries per surviving hypothesis. These savings equal exactly the work
of the inserted adaptive prefix. Sum over transcripts.

With `C=b`, there are `2^{b-d}` cosets and `d=O(k log b)=o(b)`. The same
entropy argument gives incumbent cost `Omega(b^2/log b)`, while column
first and the full original row code still cost `O(b)`. The plateau
therefore coexists with a full-order approximation gap.

The lemma concerns the specified column-plus-coordinate neighborhood. It
does not exclude a profitable prefix mixing several kinds of row-decoy
tests, or actual rollout using fresh complete greedy continuations.

## 6. Computational checks

Executed successfully:

```
python research-general-continuation.py --max-b 22 --audit-b 8
```

The exact all-node audits checked respectively 1,465, 3,503, 8,131, and
65,427 splitting node/test pairs on instances with 96, 192, 384, and 2,048
hypotheses. Maximum strict insertion improvement was exactly zero in
every case. At `b=C=8`, every root gated-bit insertion increases total
unnormalized cost by exactly 896.

The coset audit used all seven nonzero vectors in `F_2^3` for the two-bit
case, and all eight vectors with leading bit one in `F_2^4` for the
three-bit case. It checked all 28 coordinate subsets of size one or two,
and all 92 subsets of size one, two, or three, respectively. Every
completed prefix was exactly neutral. The proof covers adaptive prefixes;
the experiment directly enumerates coordinate subsets rather than all
adaptive trees.

Exact cost-only calculations, without constructing the much larger test
matrices, give:

| b=C | n | Incumbent mean | Column-first mean | Ratio lower bound |
|---:|---:|---:|---:|---:|
| 8 | 2,048 | 14.2265625 | 12.375 | 1.1496 |
| 12 | 49,152 | 24.5240885 | 18.4166667 | 1.3316 |
| 16 | 1,048,576 | 36.9869080 | 24.4375 | 1.5135 |
| 20 | 20,971,520 | 51.6255295 | 30.45 | 1.6954 |
| 22 | 92,274,688 | 59.7935562 | 33.4545455 | 1.7873 |

These finite ratios support the exact formulas; the asymptotic separation
is established by the entropy proof, not extrapolated from the table.

## 7. Research implication and remaining target

The planar restriction-credit approach uses geometry to ensure that a
discovering query removes a useful prefix of the comparison tree. In the
general setting, an enormous part of the incumbent cost can remain
unpruned after every bounded number of individually useful code bits.
Exact local credit, arbitrary polynomial integer descent, and a fixed
depth of such surgery do not resolve that issue by themselves.

The viable continuation direction should generate complete coherent
alternative codes on activated sets and preserve them across long
selector spines. The existing probe/retain/recombine construction does
this on represented states; its missing global coverage or amortization
theorem remains the appropriate open target. A claim that fixed-tree
pruning alone supplies its needed continuation oracle is now ruled out
by an explicit family.

No `o(log n/log log n)` polynomial approximation ratio has been obtained
in this branch of the investigation.
