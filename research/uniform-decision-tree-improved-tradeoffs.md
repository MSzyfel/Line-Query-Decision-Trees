# Uniform Decision Tree: improved constant-power tradeoffs

**Date:** 2026-10-11  
**Model:** $n$ equiprobable hypotheses, $m$ unit-cost tests, and at most $K\ge2$ outcomes per test, with $K$ fixed. Every pair of hypotheses is distinguishable.

All logarithms are base two.

This document gives two additional proof mechanisms, rather than merely substituting parameters into the supplied tradeoff:

1. **Cost-mass amortization:** charge a prefix generation by the smaller of global OPT and the maximum conditional cost times the surviving probability mass.
2. **An average-depth-to-height certificate:** use a complete bounded-height exact solver in the low-cost branch, instead of optimizing an unfinished prefix and recursing.

The continuation adds a third mechanism: **shared optimal-cost budgeting**. Prefix generations and terminal subproblems are charged jointly, rather than bounding their contributions separately. With generation-dependent cutoffs, this gives the stronger frontier in Result V and Sections 10-11.

The resulting guarantees improve the constant-power bounds stated in the supplied paper. Literature-wide priority is not asserted. No algorithms were implemented.

**Status under the latest research target:** the results below are incremental tradeoff refinements, not an $o(\log n/\log\log n)$ approximation in quasipolynomial time. That substantive target is unproved. Section 13 establishes that the present greedy-terminal cutoff paradigm cannot achieve it and isolates a different structural oracle that would suffice, without claiming that oracle exists.

**Further oracle analysis:** Section 14 proves an affine bound for exact continuation costs, a value-query obstruction for arbitrary assigned continuation-code costs, and a constructive code-extension bound. These narrow the missing step to the structure and reuse of the actual recursively generated codes; they do not complete the quasipolynomial approximation.

Section 15 gives exact consistency properties of a finite reusable code pool, explains why exact recombination closure would hide optimal decision-tree computation, and proves a weaker pricing condition sufficient for an $O(\log\log n)$ quasipolynomial approximation. The required pricing algorithm remains unproved.

Section 16 tests the pricing route against explicit code-tree complementarity, then analyzes a fully specified policy-improvement process without an oracle. It proves an unconditional instance-sensitive convergence bound and identifies the long-spine overcount that still prevents a uniform quasipolynomial asymptotic guarantee.

Section 17 replaces independent continuation trials by exact recombination on their represented state DAG. It gives a fully specified quasipolynomial finite-descent construction and exact whole-spine comparison on supported states. A global coverage theorem, and hence the requested better worst-case ratio, remains unproved.

**Exponent criterion:** when the runtime power $e(n)$ itself grows with $n$, a qualifying improvement must satisfy $e_{\mathrm{new}}(n)=o(e_{\mathrm{old}}(n))$. The growing-power refinement recorded below does not satisfy this condition and is not counted as meeting that target. The quasipolynomial and subexponential constant-power improvements do qualify.

**Latest lower-bound investigation:** [the shared lower-bounds note](uniform-decision-tree-lower-bounds.md) proves a joint conditional-entropy/shared-query certificate and its convex cover dual, completion-profile relaxations, and a local-policy consistency hierarchy. A certificate-guided state generator gives a nearly optimal quasipolynomial repair on the gated-grid obstruction, even with selector spines longer than the probe horizon. That restricted-family theorem does not establish the requested general asymptotic ratio.

## 1. Results

Write

$$
A=\lceil\log n\rceil,\qquad \ell=\log A,\qquad
D=C_{\mathrm{OPT}}.
$$

### Result I: a better quasipolynomial frontier

For every fixed $r>1$, there is a deterministic policy with

$$
\boxed{
\frac{C_{\mathrm{out}}}{D}
\le
\left(\frac4{r-1}+o(1)\right)\frac A\ell
+(r-1)\ell+O_K(1)}
\tag{I}
$$

and running time

$$
\operatorname{poly}(n,m,K)(Km)^{\lceil A^r\rceil+1}.
$$

In particular, if $m=n^{O(1)}$, the running time is $2^{O((\log n)^{r+1})}$.

Consequently, for every fixed $c>0$ and $\delta>0$, one can guarantee

$$
C_{\mathrm{out}}\le c\,\frac{\log n}{\log\log n}\,D
$$

for sufficiently large $n$, in time

$$
\boxed{2^{O((\log n)^{\,2+4/c+\delta})}.}
\tag{II}
$$

The supplied $(9+\varepsilon)/\alpha$ curve, specialized to the same approximation target, has a log-power approaching $2+9/c$. Here it approaches $2+4/c$.

For example, a target factor $\log n/\log\log n$ has a proven time power arbitrarily close to **6 instead of 11**.

This is a genuine improvement in the quasipolynomial running-time bound. It does not make the approximation factor $o(\log n/\log\log n)$ within quasipolynomial time.

### Result II: a growing-power refinement that does not meet the stricter criterion

Let

$$
g=\lfloor\log\ell\rfloor.
$$

Using horizon $B=\lceil A^{g+1}\rceil$ gives

$$
\boxed{
\frac{C_{\mathrm{out}}}{D}
\le(4+o(1))
\frac{\log n}{\log\log n\,\log\log\log n}}
\tag{III}
$$

in time

$$
\boxed{
2^{O(A^{g+2})}
=\exp((\log n)^{O(\log\log\log n)})}
\tag{IV}
$$

when $m=n^{O(1)}$.

This is unconditional and is $o(\log n/\log\log n)$. At the same time scale, the supplied tradeoff gives leading coefficient nine rather than four. The refinement comes from the new charging argument and the different stopping threshold, not from that tradeoff alone.

The established time bound is not quasipolynomial: its log-power grows with $n$.

For the same asymptotic approximation target, the new and old growing log-powers are still $\Theta(g)$. Their ratio does not tend to zero. This result is therefore **not counted as a qualifying growing-exponent improvement**, even though the constant-power results elsewhere in this document remain valid.

### Result III: a stronger subexponential constant-factor frontier

For every fixed $\alpha\in(1/2,1)$ and $\varepsilon>0$, there is a deterministic

$$
\boxed{\left(\frac4{2\alpha-1}+\varepsilon\right)\text{-approximation}}
\tag{V}
$$

in time

$$
\boxed{2^{O(n^\alpha\log(Km))}.}
\tag{VI}
$$

For $\alpha=3/4$, this is an **$8+\varepsilon$ approximation**, compared with approximately 12 from the supplied $9/\alpha$ curve at that exponent.

More generally, every constant $c>4$ is achievable in subexponential time with exponent arbitrarily close above

$$
\frac{1+4/c}{2}.
$$

For example, a 10-approximation can be certified with exponent $0.7+\delta$, instead of $0.9+\delta$ from the supplied curve.

### Result IV: a stronger hybrid subexponential frontier

The height certificate can also terminate a bounded number of prefix generations. For every fixed $\alpha\in(0,1)$ and integer $k\ge0$ with $(k+2)\alpha>1$, and every $\varepsilon>0$, this gives

$$
\boxed{
\left(k+\frac{4(k+1)}{(k+2)\alpha-1}+\varepsilon\right)
\text{-approximation in }
2^{O(n^\alpha\log(Km))}\text{ time}.}
\tag{VII}
$$

Examples:

| Time power $\alpha$ | Prefix generations $k$ | New approximation factor | Supplied leading $9/\alpha$ |
|---|---:|---:|---:|
| $3/4$ | 1 | $37/5+\varepsilon=7.4+\varepsilon$ | 12 |
| $5/8$ | 2 | $10+\varepsilon$ | 14.4 |
| $1/2$ | 3 | $41/3+\varepsilon$ | 18 |

Inverting the second row, a **10-approximation** is attainable with time power $5/8+\delta$ for every fixed $\delta\in(0,3/8)$, improving on powers approaching $9/10$ in the supplied curve.

All powers in these statements are constants. The result is not a constant-factor rescaling of a growing runtime power.

### Result V: shared-budget charging and generation-dependent cutoffs

For every fixed $\alpha\in(0,1)$ and $\varepsilon>0$, there is a deterministic

$$
\boxed{
\left(\frac5\alpha+\varepsilon\right)\text{-approximation in }
2^{O(n^\alpha\log(Km))}\text{ time}.}
\tag{VIII}
$$

This improves the supplied leading factor $9/\alpha$ for every fixed $\alpha$.

The height certificate permits a slightly stronger explicit fixed-factor frontier. Fix a rational $R>4$ and an integer $k\ge0$ such that

$$
r=R-k\in[4,6).
$$

Define

$$
C(x)=(x+1)(x+2)(x+3)(x+4),
$$

$$
f(r)=(6-r)r(r+1)(r+2)(r+3),
$$

and

$$
\alpha_{R,k}=
\frac5{R+f(r)/C(R)}.
$$

For every fixed $\varepsilon>0$, there is an $(R+\varepsilon)$-approximation in time

$$
\boxed{2^{O(n^{\alpha_{R,k}}\log(Km))}.}
\tag{IX}
$$

For integer $R\ge5$, taking $k=R-5$ gives:

| Approximation factor | Time power $\alpha_{R,k}$ | Decimal |
|---|---:|---:|
| $5+\varepsilon$ | $9/10$ | 0.900000 |
| $6+\varepsilon$ | $15/19$ | 0.789474 |
| $8+\varepsilon$ | $495/806$ | 0.614144 |
| $10+\varepsilon$ | $143/288$ | 0.496528 |
| $12+\varepsilon$ | $130/313$ | 0.415335 |

In particular, for every fixed $\delta\in(0,1-143/288)$, a **10-approximation** is attainable in time

$$
\boxed{
2^{O(n^{143/288+\delta}\log(Km))},}
\tag{X}
$$

improving the previous power approaching $5/8$ and the supplied power approaching $9/10$.

The proof is not a parameter substitution into the earlier hybrid bound: it replaces the additive prefix-plus-terminal estimate by a coupled estimate. All powers in (VIII)-(X) are constants. No new little-$o$ decrease in a growing power, or strict-quasipolynomial little-$o$ approximation, is claimed.

## 2. External facts and elementary bookkeeping

For a nonempty candidate set $S$, let:

- $d(S)$ be its optimal conditional average depth.
- $g(S)$ be the conditional average depth of a complete greedy tree.
- $F(S)=|S|d(S)$.
- $p(S)=|S|/n$.

Greedy minimizes the size of the largest outcome class.

The supplied paper establishes

$$
g(S)\le
\frac{12\log|S|}{\log d(S)}d(S)
\quad\text{when }d(S)\ge2.
\tag{1}
$$

It also establishes, for every fixed $\zeta>0$ and sufficiently large uniform instances,

$$
g(S)\le
\frac{(4+\zeta)\log|S|}{\log d(S)}d(S).
\tag{2}
$$

We will only use (2) on sets whose conditional optimum tends to infinity, so their sizes also tend to infinity. Its small-instance qualification is therefore satisfied uniformly.

For sufficiently large global $n$, depending only on fixed $K$, we have the crude envelope

$$
g(S)\le12A\,d(S)
\tag{3}
$$

on every nonsingleton subset.

Indeed, if $|S|\ge K^2$, entropy gives $d(S)\ge2$, and (1) implies (3). If $2\le|S|<K^2$, greedy uses a splitting test at every internal node, so its maximum depth is at most $|S|-1<K^2$. For $A\ge K^2$ and $d(S)\ge1$, (3) follows directly.

For any family of disjoint candidate subsets,

$$
\boxed{\sum_i p(S_i)d(S_i)\le D.}
\tag{4}
$$

To prove this, restrict one optimal global tree to each $S_i$ and delete redundant tests. Each hypothesis incurs no greater depth than before. Replacing these restricted trees by conditional optima can only decrease cost.

Finally,

$$
D\ge\log_K n=\frac{\log n}{\log K}.
\tag{5}
$$

These are the only optimal-cost lower bounds needed.

## 3. The prefix construction with a different cutoff

Fix an integer horizon $B\ge1$, the same in every recursive call.

On a candidate set $S$:

1. Return a leaf if $|S|\le1.
2. Compute a complete greedy tree and its conditional cost $g(S)$.
3. If $g(S)\ge B/2$, return that greedy tree.
4. Otherwise choose an optimal depth-$B$ prefix: every leaf is either a singleton or is at depth exactly $B$.
5. Recursively complete its unfinished leaf sets.

Let $c_B(S)$ be the conditional average depth of the optimal prefix. Truncating either a greedy or optimal complete tree gives

$$
c_B(S)\le d(S)\le g(S).
\tag{6}
$$

The prefix is computable by the usual additive recurrence with zero terminal cost at horizon zero. It requires no oracle for $d(S)$.

If the prefix is selected, then

$$
c_B(S)<B/2.
$$

Every unfinished hypothesis pays all $B$ prefix queries. Hence the total conditional mass left unfinished is less than $1/2$.

Thus recursion terminates, and every hypothesis is identified. All tests are original tests; no artificial identity-revealing queries are introduced.

The cutoff is deliberately **$B/2$**, not $B n^{-\alpha/3}$. The larger cutoff makes terminal greedy subproblems more expensive and therefore easier to approximate using (2). The next lemma is what permits this slower mass contraction.

## 4. The new cost-mass amortization lemma

Let $\mathcal F_j$ be the sets on which a prefix is selected at recursion generation $j$, and let

$$
M_j=\sum_{S\in\mathcal F_j}p(S).
$$

Sets within one generation are disjoint, and the unfinished-mass bound gives

$$
M_j\le2^{-j}.
\tag{7}
$$

The total cost $P_j$ of prefixes at that generation satisfies two different upper bounds:

$$
P_j=\sum_{S\in\mathcal F_j}p(S)c_B(S)\le D
$$

by (4) and (6), and

$$
P_j\le(B/2)M_j\le(B/2)2^{-j}
$$

by the conditional cutoff.

Therefore

$$
\boxed{P_j\le\min\{D,(B/2)2^{-j}\}.}
\tag{8}
$$

### Lemma

The total prefix cost is at most

$$
\boxed{
P_{\mathrm{total}}
\le D\left(3+\log^+\frac{B}{2D}\right),}
\tag{9}
$$

where $\log^+x=\max\{0,\log x\}$.

### Proof

Put $x=B/(2D)$ and sum (8), divided by $D$.

If $x\le1$, the sum is at most

$$
\sum_{j\ge0}x2^{-j}=2x\le2.
$$

If $x>1$, let $J=\lceil\log x\rceil$. The first $J$ summands are at most one, and the tail is at most

$$
\sum_{j\ge J}x2^{-j}\le2.
$$

Thus the sum is at most $J+2\le\log x+3$. This proves (9). $\square$

The important distinction from charging every generation by full OPT is that generations with small surviving mass become cheap even when recursion continues. No assumption about entropy-excess monotonicity or compatibility with the global optimal tree is made.

## 5. Terminal greedy cost and the master inequality

All greedy-terminal subsets are disjoint: once a greedy tree is returned, no descendant recursive calls are made.

On a terminal nonsingleton set,

$$
g(S)\ge B/2.
$$

Equation (3) implies

$$
d(S)\ge\frac{B}{24A}.
\tag{10}
$$

Suppose $B/(24A)\to\infty$. Then every such set eventually meets the size requirement of (2). Consequently its greedy ratio is at most

$$
\frac{(4+\zeta)A}{\log(B/(24A))}.
$$

Use (4) on all greedy-terminal sets, and add the prefix bound (9). For every fixed $\zeta>0$ and sufficiently large $n$,

$$
\boxed{
\frac{C_{\mathrm{out}}}{D}
\le
\frac{(4+\zeta)A}{\log(B/(24A))}
+3+\log^+\frac{B}{2D}.}
\tag{10a}
$$

This is an unconditional instance-sensitive inequality. OPT appears only in the proof, not in the construction.

## 6. Proof of the quasipolynomial improvement

Take $B=\lceil A^r\rceil$ for fixed $r>1$.

Then

$$
\log(B/(24A))=(r-1)\ell-\log24+o(1).
$$

By (5),

$$
\log^+\frac{B}{2D}\le(r-1)\ell+O_K(1).
$$

Apply (10a). Since $\zeta$ may be any fixed positive number and the greedy rule itself does not depend on it, the asymptotic leading coefficient is four. We obtain (I):

$$
\frac{C_{\mathrm{out}}}{D}
\le
\left(\frac4{r-1}+o(1)\right)\frac A\ell
+(r-1)\ell+O_K(1).
$$

Also $\ell=o(A/\ell)$.

For target coefficient $c>0$ and any $\delta>0$, choose

$$
r=1+\frac4c+\frac{\delta}{2}.
$$

The leading coefficient $4/(r-1)$ is strictly below $c$, so for sufficiently large $n$ the lower-order prefix cost fits inside that fixed margin. Since $A/\ell\sim\log n/\log\log n$, one obtains the stated target, with any necessary additional arbitrarily small margin in $r$.

The exact prefix routine makes at most $Km$ recursive evaluations per depth level. There are only polynomially many outer calls: at most $n$ disjoint sets per generation and at most $A+1$ generations.

Thus total running time is

$$
\operatorname{poly}(n,m,K)(Km)^{B+1}.
$$

When $m=n^{O(1)}$, this is $2^{O(A^{r+1})}$, proving (II).

For arbitrary explicit test count, retain the displayed $m$-dependent bound. It is quasipolynomial in the input size for fixed $r$.

## 7. Proof of the improved near-quasipolynomial ratio

Now take $g=\lfloor\log\ell\rfloor$ and $B=\lceil A^{g+1}\rceil$.

The master inequality gives

$$
\frac{C_{\mathrm{out}}}{D}
\le
\frac{(4+o(1))A}{g\ell-O(1)}
+g\ell+O_K(1).
$$

Because

$$
\frac{(g\ell)^2}{A}\longrightarrow0,
$$

the prefix term is negligible compared with $A/(g\ell)$. This proves (III).

The same exact prefix routine has time

$$
2^{O(A^{g+2})}
$$

for polynomially many tests, proving (IV).

This bound is faster than $2^{n^\epsilon}$ for every fixed $\epsilon>0$, because

$$
\log\!\left(A^{g+2}\right)=O(\ell\log\ell)=o(\log n).
$$

The supplied curve at this prefix-horizon scale has greedy-terminal and prefix-generation contributions totaling leading coefficient nine. Our cutoff and (8) instead make the prefix contribution lower order, leaving leading coefficient four.

## 8. A separate improvement: exact search using an average-to-height certificate

### Lemma

For any complete proper identification tree with height $H$,

$$
\boxed{
\sum_h d_T(h)\ge\frac{H(H+3)}2.}
\tag{11}
$$

Here proper means every internal node has at least two nonempty children. It does not mean that all leaves have the same depth.

### Proof

Take a deepest root-to-leaf path of length $H$. At its internal node of depth $i$, for $i=0,\ldots,H-1$, choose a leaf in a nonempty off-path child subtree.

These $H$ leaves are distinct and have depths at least $1,\ldots,H$. The deepest leaf is another distinct leaf of depth $H$.

Their total depth alone is at least

$$
1+\cdots+H+H=\frac{H(H+3)}2.
$$

Additional leaves only increase the sum. $\square$

An optimal tree can be assumed proper because redundant tests can be deleted.

If $G=C_G$ is the average cost of any known complete greedy tree, then $D\le G$, so an optimal tree has height at most

$$
\sqrt{2nD}\le\sqrt{2nG}.
\tag{12}
$$

### Complete bounded-height optimization

Define the unnormalized complete-tree objective with height cap $h$ by

$$
E(S,h)=0\quad\text{if }|S|\le1,
$$

$$
E(S,0)=+\infty\quad\text{if }|S|>1,
$$

and

$$
E(S,h)=|S|+
\min_{\tau\text{ splitting }S}\sum_a E(S\cap\tau^{-1}(a),h-1).
\tag{13}
$$

This optimizes average cost among complete trees of height at most $h$ in time

$$
\operatorname{poly}(n,m,K)(Km)^{h+1}.
$$

The $+\infty$ base case is essential. The zero-cost unfinished leaves of the supplied truncated-prefix routine would not justify an exact solution.

### Proof of Result III

Fix $\alpha\in(1/2,1)$ and put $\eta=2\alpha-1>0$.

Compute the greedy tree.

- If $G\ge\lceil n^\eta\rceil$, return it.
- Otherwise solve (13) with

$$
H=\min\{n-1,\lceil\sqrt{2nG}\rceil\}.
$$

The low-cost branch returns a global optimum: (11)-(12) certify that an optimal complete tree lies within this height cap.

In that branch,

$$
H\le2n^\alpha+O(1),
$$

so its running time is as in (VI).

In the high-cost branch, (3) implies

$$
D\ge\frac{n^\eta}{12A},
\qquad
\log D\ge\eta\log n-\log(12A).
$$

Apply the refined root greedy guarantee (2):

$$
\frac GD
\le
\frac{(4+o(1))\log n}
{\eta\log n-\log(12A)}
=\frac4\eta+o(1).
$$

For every fixed $\varepsilon>0$, this is at most $4/(2\alpha-1)+\varepsilon$ for sufficiently large $n$. The exact branch has ratio one. This proves (V).

Finite small instances can be handled exactly without changing these asymptotic bounds.

## 9. A hybrid height-filter and prefix proof

Fix constants $\alpha\in(0,1)$, $k\ge0$ with $(k+2)\alpha>1$, and choose

$$
0<t<
\frac{(k+2)\alpha-1}{k+1}
=\alpha-\frac{1-\alpha}{k+1}.
\tag{14}
$$

Set the global prefix horizon $B=\lceil n^\alpha\rceil$ and the greedy threshold $T=n^t$.

At every candidate set $S$, compute its complete greedy tree and conditional cost $g(S)$, then:

1. If the certified height

$$
h(S)=\min\{|S|-1,\lceil\sqrt{2|S|g(S)}\rceil\}
$$

is at most $B$, use the complete exact routine (13).
2. Otherwise, if $g(S)\ge T$, return the greedy tree.
3. Otherwise, optimize a depth-$B$ prefix and recurse on its unfinished leaves.

The exact terminal call returns a conditional optimum, by the height lemma. Every active prefix has conditional cost less than $T$, so its unfinished mass is at most

$$
T/B\le n^{t-\alpha}.
\tag{15}
$$

After $j$ prefix generations, their total surviving global mass is at most $n^{-j(\alpha-t)}$. In particular, every reached candidate set has size at most

$$
|S|\le n^{1-j(\alpha-t)}.
\tag{16}
$$

At generation $k$, consider any state with $g(S)<T$. Equations (16) and (14) imply

$$
\begin{aligned}
2|S|g(S)
&<2n^{\,1-k(\alpha-t)+t}\\
&=2n^{\,1-k\alpha+(k+1)t}\\
&=2n^{\,2\alpha-\gamma},
\end{aligned}
\tag{17}
$$

for a fixed $\gamma>0$. Thus, for sufficiently large $n$,

$$
\lceil\sqrt{2|S|g(S)}\rceil\le B.
$$

It terminates exactly. Any other state at that generation either already passes the exact-height test or has $g(S)\ge T$ and terminates greedily.

Consequently there are at most **$k$ prefix generations**, not $k+1$: only generations $0,\ldots,k-1$ can contain active prefixes.

Each such generation costs at most $D$ by (4) and (6). Their total contribution is at most $kD$.

All terminal sets, whether exact or greedy, are mutually disjoint. On greedy-terminal sets, (3) gives

$$
d(S)\ge \frac{n^t}{12A}.
$$

The refined greedy guarantee (2) therefore bounds their ratio by $4/t+o(1)$. Exact-terminal ratios equal one. Since $t<\alpha<1$, their combined cost is at most

$$
\left(\frac4t+o(1)\right)D
$$

by (4), with no extra charge for exact terminals.

The output ratio is at most

$$
k+\frac4t+o(1).
$$

Let $t$ approach the strict upper bound in (14), while keeping a fixed positive margin sufficient for (17). For every fixed $\varepsilon>0$, choose that margin and the greedy accuracy so the ratio is at most

$$
k+\frac{4(k+1)}{(k+2)\alpha-1}+\varepsilon.
$$

Every complete or partial exact call has height at most $B$ and time $\operatorname{poly}(n,m,K)(Km)^{B+1}$. There are polynomially many outer calls, proving (VII).

For a factor of 10, take $k=2$ and $\alpha=5/8+\delta$. The right-hand side of (14) is $1/2+4\delta/3$. Choose $t$ strictly between $1/2$ and this value. Then $2+4/t<10$, so the fixed margin absorbs the vanishing greedy term for sufficiently large $n$. This proves the claimed 10-approximation runtime.

## 10. Shared optimal-cost budgeting

Consider any recursive construction with at most $k$ prefix generations, numbered $0,\ldots,k-1$, and terminal subproblems at generations $0,\ldots,k$.

For generation $i$, let $\mathcal T_i$ be the candidate sets on which the construction terminates, either with a complete greedy tree or with an exact complete solution. Define their conditional-optimal cost mass by

$$
X_i=\sum_{S\in\mathcal T_i}p(S)d(S).
\tag{18}
$$

All terminal candidate sets, including those at different generations, are disjoint. Thus

$$
\sum_{i=0}^{k}X_i\le D.
\tag{19}
$$

Let $P_j$ be the total prefix cost at generation $j$.

The active candidate sets at that generation are disjoint not only from one another, but also from every terminal set at generations $0,\ldots,j$. Applying (4) to this combined disjoint family, and using $c_B(S)\le d(S)$, gives

$$
\boxed{
P_j\le D-\sum_{i=0}^{j}X_i.}
\tag{20}
$$

This is stronger than bounding every $P_j$ separately by $D$.

### Shared-budget lemma

Suppose a terminal subproblem at generation $i$ is solved with ratio at most $R-i+\varepsilon$, where $R\ge k$. Then

$$
\boxed{C_{\mathrm{out}}\le(R+\varepsilon)D.}
\tag{21}
$$

### Proof

Sum (20):

$$
\sum_{j=0}^{k-1}P_j
\le kD-\sum_{i=0}^{k-1}(k-i)X_i.
$$

The total terminal cost is at most

$$
\sum_{i=0}^{k}(R-i+\varepsilon)X_i.
$$

Adding these expressions cancels the generation index:

$$
\begin{aligned}
C_{\mathrm{out}}
&\le kD+(R-k+\varepsilon)\sum_{i=0}^{k}X_i\\
&\le(R+\varepsilon)D,
\end{aligned}
$$

using (19) and $R-k+\varepsilon\ge0$. $\square$

The $X_i$ are analysis quantities, not values queried by the construction.

The improvement works because early terminal costs cannot simultaneously be used again to pay for later active prefixes. It does not assume that the sum of conditional optima across multiple frontiers is bounded by OPT.

## 11. Generation-dependent thresholds and proof of Result V

Fix $R,k,r,\alpha=\alpha_{R,k}$ as in Result V. These are constants independent of the instance size.

For $i=0,\ldots,k$, put

$$
x_i=R-i,
$$

$$
s_i=\frac{\alpha}{5}
\left(x_i+\frac{f(r)}{C(x_i)}\right),
\qquad
t_i=\frac{4s_i}{x_i}.
\tag{22}
$$

The exponent $s_i$ will bound the size of a reached candidate set, while $t_i$ controls its greedy cutoff.

### 11.1 Exact identities

First,

$$
s_0=\frac{\alpha}{5}\left(R+\frac{f(r)}{C(R)}\right)=1.
\tag{23}
$$

Since

$$
C(x-1)=\frac{x}{x+4}C(x),
$$

we obtain

$$
\boxed{s_{i+1}=s_i+t_i-\alpha}
\quad(i<k).
\tag{24}
$$

At the final generation, $x_k=r$, and

$$
\frac{f(r)}{C(r)}=\frac{(6-r)r}{r+4}.
$$

Therefore

$$
s_k=\frac{2\alpha r}{r+4},
\qquad
t_k=\frac{8\alpha}{r+4},
$$

so

$$
\boxed{s_k+t_k=2\alpha.}
\tag{25}
$$

Also

$$
t_i=
\frac{4\alpha}{5}
\left(1+\frac{f(r)}{x_iC(x_i)}\right).
$$

Because $xC(x)$ is increasing for $x\ge4$, the maximum occurs at $x_k=r$. Hence

$$
0<t_i\le t_k=\frac{8\alpha}{r+4}\le\alpha.
\tag{26}
$$

For $i<k$, the inequality $t_i<\alpha$ is strict. Equality can occur only at the final generation when $r=4$.

Finally $\alpha\in(0,1)$. If $R\ge5$, then $\alpha<5/R\le1$, since $f(r)>0$. If $4<R<5$, the only admissible $k$ is zero, and the formula simplifies to $\alpha=(R+4)/(2R)<1$.

### 11.2 The construction and integer thresholds

Set

$$
B=\lceil2n^\alpha\rceil,
\qquad
T_i=\lceil n^{t_i}\rceil.
\tag{27}
$$

At a reached set $S$ at generation $i$:

1. Return a leaf if $|S|\le1.
2. Compute its complete greedy tree and cost $g(S)$.
3. If

$$
\min\{|S|-1,\lceil\sqrt{2|S|g(S)}\rceil\}\le B,
$$

return the complete optimum from the bounded-height recurrence (13).
4. Otherwise, if $g(S)\ge T_i$, return its greedy tree.
5. Otherwise, return an optimal depth-$B$ prefix and complete its unfinished leaves at generation $i+1$.

Only original tests are used. The last case will be proved impossible at $i=k$.

The parameters can all be chosen rational. Their ceilings can consequently be evaluated by polynomial-time integer comparisons; no exact real-number oracle is required.

### 11.3 State-size induction and exact termination

Every state reached at generation $i$ satisfies

$$
|S|\le n^{s_i}.
\tag{28}
$$

The root satisfies this by (23).

If a prefix is selected, its conditional cost is less than $T_i$. The number of hypotheses left unfinished is at most

$$
|S|\frac{T_i}{B}
\le |S|n^{t_i-\alpha}.
$$

Here we used

$$
T_i\le n^{t_i}+1\le2n^{t_i},
\qquad B\ge2n^\alpha.
$$

Each unfinished leaf set therefore has size at most

$$
n^{s_i+t_i-\alpha}=n^{s_{i+1}},
$$

proving (28) by induction.

Now consider a generation-$k$ state with $g(S)<T_k$. Then

$$
g(S)<T_k\le2n^{t_k},
$$

and (25), (28) give

$$
2|S|g(S)\le4n^{s_k+t_k}=4n^{2\alpha}.
$$

Thus

$$
\lceil\sqrt{2|S|g(S)}\rceil
\le\lceil2n^\alpha\rceil=B.
$$

It passes the complete exact-search certificate. Any other generation-$k$ state terminates exactly or greedily. Hence there are at most $k$ prefix generations.

The factor two in (27) absorbs both threshold rounding and the height square root. No strict inequality in an asymptotic exponent is needed for termination.

### 11.4 The terminal approximation budget

A greedy-terminal state at generation $i$ has $g(S)\ge T_i\ge n^{t_i}$. By (3),

$$
d(S)\ge\frac{n^{t_i}}{12A}.
\tag{29}
$$

All $t_i$ are positive constants, so these conditional optima and state sizes tend to infinity. The refined greedy guarantee (2) applies uniformly over all terminal states.

Using (28)-(29), for every fixed $\zeta>0$,

$$
\frac{g(S)}{d(S)}
\le
\frac{(4+\zeta)s_i\log n}
{t_i\log n-\log(12A)}.
$$

Since $4s_i/t_i=x_i=R-i$, choosing $\zeta$ sufficiently small gives, for every fixed $\varepsilon>0$ and sufficiently large $n$,

$$
\frac{g(S)}{d(S)}\le R-i+\varepsilon.
\tag{30}
$$

There are only finitely many generations, so one size threshold suffices for all of them.

An exact-terminal set has ratio one, also at most $R-i+\varepsilon$, because $R-i\ge r\ge4$. Singletons contribute zero.

The shared-budget lemma now proves

$$
C_{\mathrm{out}}\le(R+\varepsilon)D.
$$

### 11.5 Running time

Every partial or complete exact call has depth cap at most $B$. Its recursive evaluation takes

$$
\operatorname{poly}(n,m,K)(Km)^{B+1}.
$$

The outer construction makes polynomially many calls: its candidate sets are disjoint within each generation and there are at most $k+1$ generations. Thus the total time is

$$
2^{O(n^\alpha\log(Km))}.
$$

Finite exceptional instance sizes can be handled exactly without changing this asymptotic statement. This proves (IX).

### 11.6 The universal leading-five frontier

Fix $\alpha_0\in(0,1)$ and $\varepsilon>0$. Choose a rational $R$ with

$$
\frac5{\alpha_0}<R<
\frac5{\alpha_0}+\frac{\varepsilon}{2}.
$$

Choose $k$ so $r=R-k\in[5,6)$. Then

$$
\alpha_{R,k}<\frac5R<\alpha_0.
$$

Apply (IX) with approximation slack smaller than $\varepsilon/2$. It gives a $(5/\alpha_0+\varepsilon)$-approximation within the time bound of power $\alpha_0$, proving (VIII).

This is a consequence of the new shared-budget construction, not of the supplied $9/\alpha$ guarantee.

### 11.7 The 10-approximation calculation

Take $R=10$, $k=5$, and $r=5$. Then

$$
C(10)=11\cdot12\cdot13\cdot14=24024,
$$

$$
f(5)=5\cdot6\cdot7\cdot8=1680.
$$

Consequently

$$
\alpha_{10,5}
=\frac5{10+1680/24024}
=\frac{143}{288}
=\frac12-\frac1{288}.
\tag{31}
$$

This gives a $(10+\varepsilon)$-approximation at that exact power.

To obtain factor exactly 10 at any fixed larger power, keep $k=5$ and choose a rational $R<10$ sufficiently close to 10. Then $r=R-5$ remains in $[4,6)$, and the expression for $\alpha_{R,5}$ is continuous in $R$.

For every fixed $\delta>0$, one can therefore arrange

$$
\alpha_{R,5}<\frac{143}{288}+\delta.
$$

Choose approximation slack $0<\varepsilon<10-R$ in (IX). Its output has ratio less than 10, establishing (X).

## 12. Comparison and exact scope

The height-filter factor improves on the supplied leading $9/\alpha$ whenever

$$
\frac4{2\alpha-1}<\frac9\alpha
\quad\Longleftrightarrow\quad
\alpha>\frac9{14}.
$$

It also removes the supplied prefix horizon's extra $\log n$ factor in the running-time exponent.

The hybrid strengthens the height-filter result, including a $37/5+\varepsilon$ approximation at power $3/4$ and a 10-approximation at powers approaching $5/8$.

Shared-budget charging strengthens this further:

- The leading subexponential curve improves from $9/\alpha$ to $5/\alpha$.
- A 10-approximation has a time power arbitrarily close above $143/288$, improving on the preceding $5/8$ bound.
- A $6+\varepsilon$ approximation has power $15/19$, and an $8+\varepsilon$ approximation has power $495/806$.

The cost-mass proof improves the **constant** quasipolynomial log-power for a fixed target coefficient from $2+9/c$ to $2+4/c$.

The near-quasipolynomial coefficient refinement leaves its growing log-power in the same asymptotic order, and is not counted under the stricter exponent criterion.

The continuation does not further reduce the previously proved quasipolynomial power approaching six for coefficient one. Improving that bound, or obtaining a strict-quasipolynomial little-$o$ approximation, needs an additional argument.

These are unconditional guarantees for unrestricted valid instances of the stated model. They do not rely on the coded-spine benchmark from the previous attempt, or on the partially adaptive Pandora approximation.

What remains unresolved:

- A polynomial-time constant approximation.
- An $o(\log n/\log\log n)$ ratio in strictly quasipolynomial time.
- A little-$o$ reduction in a runtime power that itself grows with $n$.
- Optimality or literature-wide novelty of the improved tradeoffs.

## 13. The substantive quasipolynomial target

The requested target is now explicitly

$$
\frac{C_{\mathrm{out}}}{C_{\mathrm{OPT}}}
=o\!\left(\frac{\log n}{\log\log n}\right),
\qquad
\mathrm{time}=\exp((\log N)^{O(1)}),
\tag{32}
$$

where $N$ is the explicit input size and the exponent is fixed.

The constant-power refinements in this document do not establish (32). The following barrier shows that further adjustment of their cutoff constants cannot do so.

### 13.1 A lower bound for the present cutoff paradigm

Consider a construction that, at the root:

- Can search an exact prefix or complete tree only up to a fixed polylogarithmic horizon $B$.
- Returns greedy when $g(H)\ge T$, with $T\le B$.
- Optionally first applies the current complete-tree certificate

$$
\min\{n-1,\lceil\sqrt{2ng(H)}\rceil\}\le B.
$$

All the cutoff constructions above have this form when their search horizon is genuinely quasipolynomial.

#### Proposition

For every fixed polylogarithmic choice of $B$, this paradigm has worst-case approximation ratio

$$
\Omega(\log n/\log\log n)
$$

on valid binary, unit-cost, uniform instances with polynomially many tests.

#### Proof

Fix $c>0$ with $B\le(\log N)^c$ for sufficiently large inputs.

Let $r=2^b$, choose a fixed $a>\max\{c,1\}$, and put $C=\lceil b^a\rceil$. The hypotheses are a $C$-column, $r$-row grid, with $n=Cr$.

Provide:

1. Membership in each column.
2. Each row-code bit gated to each individual column.
3. Small-child row decoys across all columns. At a row node of size $s>1$, its small child has size $1+\lfloor s/C\rfloor$; recursively partition the two children and include membership in the small child only.

There are $O(r+C\log r)$ tests. The instance is valid, and $\log N=\Theta(\log n)=\Theta(b)$.

Whenever the current row node has size $s>C^2$, its small-child decoy has positive size

$$
C(1+\lfloor s/C\rfloor)>s,
$$

while each column-gated test has minority size at most $s$. Ancestor decoys are constant on that node, and descendant decoys have strictly smaller positive sets there. Thus greedy selects the current row decoy.

Its small-child fraction is at most $2/C$. Greedy therefore reveals at most $H_2(2/C)$ bits of row information per query until at most $C^2$ candidate rows remain.

The entropy reduction gives

$$
g(H)\ge
\frac{b-2\log C}{H_2(2/C)}.
$$

Using

$$
H_2(2/C)\le
\frac2C(\log C+\log e),
$$

we obtain

$$
g(H)=\Omega\!\left(\frac{Cb}{\log C}\right)
=\Omega(b^{a+1}/\log b).
\tag{33}
$$

A column-first strategy identifies the column in at most $C-1$ tests, then identifies the row in $b$ gated bit tests. Hence

$$
D\le C+b,
$$

and consequently

$$
\frac{g(H)}D=\Omega(b/\log b)
=\Omega(\log n/\log\log n).
\tag{34}
$$

Since $a>c$, (33) eventually exceeds $B$ and therefore $T$.

The complete-tree certificate also fails: $g(H)\ge1$, so both $n-1$ and $\lceil\sqrt{2ng(H)}\rceil$ eventually exceed every fixed polylogarithmic $B$. Using the actual greedy height instead does not help, because that height is at least its average $g(H)>B$.

The root therefore returns greedy immediately. Equation (34) proves the proposition. $\square$

This is an approximation lower bound for this particular algorithmic paradigm, not a complexity-theoretic hardness result or a lower bound for all quasipolynomial algorithms.

It rules out reaching (32) merely by tuning the cutoffs, strengthening their generation accounting, or adding the current height certificate.

### 13.2 A genuinely different structural route

For clarity, restrict to binary tests.

At a candidate set $S$, freeze one largest outcome of every test relative to $S$. Following these frozen outcomes in any complete decision tree defines a spine. Each off-spine exit set has size at most $|S|/2$.

An optimal tree therefore decomposes exactly into:

$$
F(S)=W(P^*)+\sum_{A\text{ an exit of }P^*}F(A),
\tag{35}
$$

where $W(P^*)$ is the unnormalized query cost of the spine and all nonsingleton exits have size at most $|S|/2$. The terminal singleton has cost zero.

This decomposition bounds recursive branching depth by $\log n$, without bounding the length of a spine.

Let $U(A)$ denote the cost of a recursively produced complete policy for an exit set $A$.

The key missing oracle would have the following **affine** guarantee: using polynomially many queries for values $U(A)$ on sets of size at most $|S|/2$, return a valid spine $P$ such that, for every competing valid frozen-outcome spine $Q$,

$$
\boxed{
W(P)+\sum_{A\in\mathrm{exits}(P)}U(A)
\le
\lambda W(Q)+
\sum_{A\in\mathrm{exits}(Q)}U(A),}
\tag{36}
$$

for a fixed constant $\lambda$.

Crucially, the continuation term on the right is **not** multiplied by $\lambda$.

### 13.3 What (36) would prove

If such an oracle existed for the recursively generated continuation values, it would give a constant-factor quasipolynomial approximation.

Indeed, assume inductively that $U(A)\le\lambda F(A)$ on smaller exit sets. Apply (36) with the spine of an optimal tree:

$$
\begin{aligned}
U(S)
&\le\lambda W(P^*)+
\sum_{A\in\mathrm{exits}(P^*)}U(A)\\
&\le\lambda W(P^*)+
\lambda\sum_{A\in\mathrm{exits}(P^*)}F(A)\\
&=\lambda F(S).
\end{aligned}
$$

Each recursively requested set has at most half the parent size. If the oracle uses $N^{O(1)}$ local work and continuation-value queries, evaluation takes at most

$$
N^{O(\log n)}
$$

time. The induction does not multiply approximation factors along those levels.

This is only a sufficient-condition proof: (36) has not been established.

### 13.4 Why the available oracles do not supply (36)

- Ordinary MSSC approximation controls cover latency, but not the costs of the exit groups that its ordering creates.
- The partially adaptive Pandora theorem multiplies both inspection cost and the selected continuation charge. It is not the affine guarantee (36).
- The MSSC-with-feedback equivalence reduces the original UDT difficulty to another fully adaptive problem; it is not an independent solution to this oracle.
- A recursively generated policy-cost function cannot silently be replaced by exact $F(A)$ or assumed to be closed under arbitrary restrictions and recombinations.

For exact continuation values $F(A)$, restriction arguments give strong inequalities. That does not make those exact values computable, or justify applying the same inequalities to an approximate recursive $U$.

The actual new research task is therefore to prove a continuation-preserving spine oracle, or a weaker variant with a globally controlled error that still yields (32). No such proof has been completed here.

### 13.5 Current outcome

The requested substantive quasipolynomial asymptotic improvement remains unproved.

The verified new information in this continuation is:

1. A concrete worst-case obstruction to the whole existing greedy-terminal cutoff paradigm at fixed polylogarithmic horizons.
2. An exact frozen-spine decomposition and a precise continuation-preserving oracle condition that would give a constant-factor quasipolynomial algorithm.

Neither the earlier constant-frontier refinements nor this unproved oracle should be described as resolving the research gap.

## 14. Pushing the affine oracle: exact structure and a black-box obstruction

This section continues the binary-test structural route of Section 13. It separates exact conditional optimum costs from arbitrary costs of valid continuation policies.

### 14.1 MSSC already gives an ideal affine bound

Fix a candidate set $S$. For every test, take its complement-of-largest-outcome set relative to $S$, and add singleton sets for the analytical MSSC instance.

Run MSSC greedy, preferring an original test set over an added singleton in a tie. Use the selected original tests as a frozen-outcome spine, stopping when at most one hypothesis remains.

Let $P_G$ be this spine. For any competing complete frozen-outcome spine $Q$,

$$
\boxed{
W(P_G)+\sum_{A\in\mathrm{exits}(P_G)}F(A)
\le
5W(Q)+\sum_{B\in\mathrm{exits}(Q)}F(B)+4.}
\tag{37}
$$

All costs here are unnormalized.

#### Proof

Every pair is distinguishable. Therefore at most one hypothesis belongs to none of the original MSSC sets: two such hypotheses would return the same frozen outcome on every test.

When at least two hypotheses remain, some original set covers at least one of them. Thus an added singleton is unnecessary until the final possible singleton. The original-test greedy spine costs no more than its completed MSSC ordering.

The tests of $Q$, followed by its terminal singleton set if needed, form an MSSC cover ordering with cost at most $W(Q)+1$. The factor-four MSSC guarantee gives

$$
W(P_G)\le4(W(Q)+1).
\tag{38}
$$

Complete each exit of $Q$ by an optimal conditional code. The resulting full tree has cost

$$
W(Q)+\sum_{B\in\mathrm{exits}(Q)}F(B).
$$

The exit sets of $P_G$ partition $S$, including its terminal singleton if any. Restrict this same full comparison tree to all of them. Conditional optimality and disjointness imply

$$
\sum_{A\in\mathrm{exits}(P_G)}F(A)
\le W(Q)+\sum_{B\in\mathrm{exits}(Q)}F(B).
\tag{39}
$$

Adding (38) and (39) proves (37). $\square$

The singleton sets in this argument are not new decision-tree tests. The additive four accounts for the possible final analytical cover step.

Spine selection itself requires no queries to $F$. The unavailable part is completing its exits with optimal codes, or preserving (39) for the costs of approximate recursive codes.

To see the exact algebraic gap, an inductive bound $U(A)\le bF(A)$ would only give

$$
W(P_G)+\sum_AU(A)
\le
(4+b)W(Q)+b\sum_BF(B)+4.
\tag{40}
$$

This does not close a factor-$b$ induction: the extra $4W(Q)$ remains at every recursive level.

Thus the issue is not that affine charging is impossible for the true cost function. It is preserving its restriction structure without evaluating exact conditional optima.

### 14.2 Being a valid code cost is not sufficient

The proposed oracle must not be assumed to work for arbitrary value-access functions $U$, even if every value is the exact cost of a supplied valid proper continuation tree.

#### Proposition: value-query obstruction

For every fixed constant $\lambda$ and every fixed quasipolynomial bound on continuation-value queries, there are:

- A valid binary unit-cost hypothesis-test matrix.
- Continuation functions $U$ whose values are costs of valid proper original-test trees.

for which no oracle with that query bound can guarantee

$$
W(P)+\sum_AU(A)
\le\lambda W(Q)+\sum_BU(B)
$$

for every competing spine $Q$.

The same obstruction applies to a guarantee with any fixed additive constant.

This is a statement about black-box continuation-value access, not computational hardness of UDT with its explicit matrix.

#### Construction

Let $q=2^d$, and let the hypotheses be

$$
H=A\cup B\cup\{z\},
\qquad |A|=|B|=q.
$$

Provide:

1. Membership in $A$ and in $B$.
2. Binary coordinate tests on $A$, gated to $A$.
3. Binary coordinate tests on $B$, gated to $B$.
4. A singleton membership test for every hypothesis.

Every positive test class is contained in $A$, in $B$, or in $\{z\}$. Its size is at most $q<(2q+1)/2$. Hence its unique largest outcome on $H$ is zero.

The explicit matrix size $N$ is polynomial in $q$, and $\log N=\Theta(d)$. In fact, identification on this matrix is easy; the lower bound below concerns an adversarially assigned continuation-cost function.

Choose an integer $k=o(q)$ and hide one set

$$
C\subseteq A,\qquad |C|=q-k.
$$

For all possible continuation subsets $X$ of size at most $|H|/2$, define $U_C(X)$ by choosing these actual codes:

- If $|X|\le1$, use the zero-cost leaf.
- If $X\subseteq B$, use the restricted $B$ coordinate code.
- If $X=C$, use the restricted $A$ coordinate code.
- Otherwise, use singleton search on $X$.

For $s\ge1$, singleton search has unnormalized cost

$$
u_{\mathrm{sing}}(s)=\frac{s(s+1)}2-1.
\tag{41}
$$

The coordinate codes cost at most $|X|d$. All these codes use original tests and can be made proper by deleting redundant nodes.

Only the value at the hidden set $C$ differs from the corresponding function with singleton search on every nonsingleton subset of $A$.

#### A cheap comparison spine

Test the $k$ singleton hypotheses in $A\setminus C$, then membership in $A$, then membership in $B$. Its exits are those singletons, $C$, $B$, and the terminal hypothesis $z$.

For this spine $Q_C$,

$$
W(Q_C)\le(2q+1)(k+2),
$$

and

$$
\sum_XU_C(X)\le2qd.
$$

Therefore

$$
\lambda W(Q_C)+\sum_XU_C(X)
=O_\lambda(q(k+d)).
\tag{42}
$$

#### Every spine that misses the hidden cheap set is expensive

Suppose a spine does not have $C$ as an exit set. Every nonsingleton exit containing hypotheses from $A$ then pays the singleton-search cost. Its continuation cost is at least

$$
\frac{b(b-1)}2
$$

if it contains $b$ hypotheses from $A$.

Consider the prefix up to the first point where at least $q/2$ hypotheses from $A$ have exited. At most one terminal singleton can avoid an associated spine query.

Call an exit large if it contains at least $\sqrt q$ hypotheses from $A$.

- If large exits in this prefix contain at least $q/4$ such hypotheses, their continuation costs total at least

$$
\frac{q}{8}(\sqrt q-1).
$$

- Otherwise, small exits in this prefix contain at least $q/4$ hypotheses from $A$. There are at least $\sqrt q/4$ such exits. Apart from a possible terminal exit, each requires a query while at least $q/2$ hypotheses from $A$ remain. Their spine cost is at least

$$
\left(\frac{\sqrt q}{4}-1\right)\frac q2.
$$

For sufficiently large $q$, either case yields

$$
\boxed{
W(P)+\sum_XU_C(X)\ge\frac{q^{3/2}}{16}.}
\tag{43}
$$

The argument also permits an unfinished final code group: if that group contains many remaining hypotheses from $A$ and is not $C$, its singleton-code cost supplies the first case.

#### Hiding the cheap set from quasipolynomially many queries

Suppose the oracle makes at most

$$
2^{O((\log N)^p)}=2^{O(d^p)}
$$

queries, for fixed $p$. Choose a fixed $a>\max\{p,1\}$ and let $k=\lceil d^a\rceil$.

The number of hidden-set possibilities is

$$
\binom qk
=2^{\Omega(k\log(q/k))}
=2^{\Omega(d^{a+1})}.
\tag{44}
$$

This exceeds the query bound by an unbounded factor.

For a deterministic oracle, answer using the nonhidden continuation function. Choose $C$ afterwards outside all queried subsets and all exit sets in its output spine. This is possible by (44); the output has at most $|H|$ nonempty exits. The resulting $U_C$ is consistent with every answer.

Its output incurs (43), while the comparator in (42) costs only $O_\lambda(qd^a)$. Since $\sqrt q/d^a\to\infty$, the affine guarantee fails.

For a randomized oracle, choose $C$ uniformly among the hidden possibilities. Until it queries $C$, its answers follow the nonhidden transcript. The probability of querying or outputting $C$ is at most the query count plus the exit count, divided by (44), and tends to zero. Its expected cost therefore obeys (43) up to a $1-o(1)$ factor, whereas (42) holds for every $C$. Some fixed hidden set consequently violates any claimed expected affine guarantee. $\square$

#### Exact scope

The proposition does not rule out the affine oracle for a specially structured recursively generated $U$.

In particular, these adversarial functions need not satisfy $U(X)\le F_G(X)$ on every subset. They also do not enforce reuse of a cheap code discovered for a large subset on related subsets.

An algorithm that jointly constructs and reuses codes, rather than accepting prescribed black-box values, is not subject to this particular obstruction.

### 14.3 A constructive code-extension inequality

There is a useful positive consistency property available directly from the identification model.

Let $\varnothing\ne B\subseteq A$, let $k=|A\setminus B|$, and suppose $T_B$ is any proper complete binary identification code for $B$. Then there is a complete original-test code for $A$ with

$$
\boxed{
F(T_A)\le F(T_B)+|A|k.}
\tag{45}
$$

#### Proof

Run $T_B$ on every hypothesis in $A$. Its original $B$ hypotheses retain their old costs. Each of the $k$ additional hypotheses follows a path of length at most $|B|-1$, since $T_B$ is proper.

At a leaf of $T_B$, there is one original hypothesis from $B$ and some number $k_v$ of added hypotheses. Identify this group with original tests. Pairwise distinguishability permits a proper tree of height at most $k_v$, with total additional cost at most $(k_v+1)k_v$.

Since $\sum_vk_v=k$,

$$
\begin{aligned}
F(T_A)-F(T_B)
&\le k(|B|-1)+\sum_v(k_v+1)k_v\\
&\le k(|B|-1)+k^2+k\\
&=k(|B|+k)=|A|k.
\end{aligned}
$$

This proves (45). $\square$

In particular,

$$
F(A)\le F(B)+|A||A\setminus B|.
\tag{46}
$$

More importantly for an algorithm, (45) applies to any available code, not merely an optimal one.

The hidden-cheap-set construction assigns a very expensive code to $A$ even though its cheap code for $C$ could be extended to $A$ at cost $O(q(k+d))$. It violates this natural reuse property at the level of its assigned costs. This explains which extra structure a non-black-box algorithm can exploit.

### 14.4 The most promising remaining version

The refined route is to construct the spine and its continuation codes jointly, with:

1. A complete code tree returned with every continuation estimate.
2. Reuse of restrictions of already available codes.
3. The extension repair (45) whenever a useful code for a nearby smaller set is available.
4. A greedy fallback, so an assigned cost is never needlessly larger than a known greedy code.

The missing proof is that such a computably represented code system preserves the comparison-tree restriction inequality sufficiently well to obtain an affine bound, or a controlled error yielding the strict-quasipolynomial target.

The extension inequality alone does not supply that proof: it does not identify which unknown subsets have useful codes, or enforce consistency across all exponentially many candidate partitions.

Likewise, simply postulating exact closure under every restriction and recombination would hide the original optimization problem.

### 14.5 Current result

This continuation establishes:

- The ideal affine bound (37) for exact continuation optima.
- A rigorous obstruction to extending it to arbitrary valid-code value functions, even with quasipolynomially many queries.
- The constructive code-reuse bound (45).

It does **not** establish an unconditional $o(\log n/\log\log n)$ approximation in quasipolynomial time. The substantive remaining problem is preserving enough comparison-tree consistency in the actual generated code system, not obtaining another latency-only MSSC approximation.

## 15. Coherent code pools and a weaker pricing target

The constant affine oracle of Section 13 may be stronger than necessary. This section identifies consistency that can actually be maintained and a weaker oracle guarantee that would still meet the substantive target.

Neither consistency alone nor the conditional composition theorem below is an unconditional approximation algorithm.

### 15.1 A finite code pool has genuine restriction consistency

Let $\mathcal L$ be a finite nonempty family of proper complete binary trees for the full hypothesis set $H$.

For $S\subseteq H$, let $T|S$ be the restriction of $T$ to $S$, with redundant nodes removed, and define

$$
V_{\mathcal L}(S)=\min_{T\in\mathcal L}F(T|S).
\tag{47}
$$

Empty sets and singletons have value zero.

These are valid code costs and satisfy

$$
F(S)\le V_{\mathcal L}(S).
$$

They can be evaluated in polynomial time in the explicit pool representation. A quasipolynomial-size pool therefore has quasipolynomial evaluation cost.

For every disjoint partition $S_1,\ldots,S_t$ of $S$,

$$
\boxed{
\sum_i V_{\mathcal L}(S_i)\le V_{\mathcal L}(S).}
\tag{48}
$$

#### Proof

Choose one tree attaining the minimum on $S$. Each restricted code cost on $S_i$ is an admissible upper bound for $V_{\mathcal L}(S_i)$. Restricting that same tree to disjoint parts cannot increase the sum of depths. Summing and then taking the minima proves (48). $\square$

The use of one comparison tree is essential: independent, unrelated continuation estimates do not automatically have this property.

### 15.2 A sharper deletion-stability inequality

If $\varnothing\ne B\subseteq S$, $s=|S|$, and $k=|S\setminus B|$, then

$$
\boxed{
0\le V_{\mathcal L}(S)-V_{\mathcal L}(B)
\le ks-\frac{k(k-1)}2.}
\tag{49}
$$

This holds for the actual restriction of each proper tree, not merely for a specially constructed extension.

#### Proof

First consider deleting one leaf $h$ from a proper tree on $s$ hypotheses. Let its depth be $d$ and let its sibling subtree contain $b$ leaves.

The restriction deletes $h$ and contracts its parent. The sibling leaves each move up by one level. Consequently the cost decreases by exactly

$$
d+b.
$$

The other $d-1$ ancestors on the path to $h$ each have a nonempty off-path subtree. Counting those leaves, the sibling leaves, and $h$ gives

$$
s\ge(d-1)+b+1=d+b.
$$

Thus deleting one leaf changes the cost by at most $s$.

Delete the $k$ leaves successively. Their total effect is at most

$$
s+(s-1)+\cdots+(s-k+1)
=ks-\frac{k(k-1)}2.
$$

For the pool minimum, choose a tree attaining $V_{\mathcal L}(B)$ and apply the same restriction bound to that tree on $S$. Monotonicity gives the other inequality. $\square$

These properties exclude the arbitrary hidden-cheap-code assignment in Section 14: a coherent pool cannot assign a huge cost to a set while assigning a much smaller restriction cost to a nearby large subset.

### 15.3 Reuse can be represented, but is not an approximation proof

A code found on a subset can be extended to a complete tree on $H$ using the construction of Section 14.3. Restricting that extension back to the subset recovers the found code after redundant tests are removed.

Therefore a pool can retain discovered conditional codes as full-tree templates. Adding a template only decreases (47), and preserves (48)-(49).

However, a coherent pool may still be poor. For example, the pool consisting of one bad greedy tree on the grid of Section 13 has the same

$$
\Omega(\log n/\log\log n)
$$

root approximation ratio, while satisfying both (48) and (49).

Thus these consistency properties do not by themselves establish a better approximation. The code-generation or pricing step must make a quantitative improvement.

### 15.4 Why exact recombination closure is not a free assumption

Suppose an upper-cost function $V$ satisfies $V(S)\ge F(S)$, vanishes on singletons, and obeys, for every splitting test $\tau$,

$$
V(S)\le |S|+\sum_aV(S\cap\tau^{-1}(a)).
\tag{50}
$$

Then

$$
\boxed{V(S)=F(S)\text{ for every }S.}
\tag{51}
$$

#### Proof

Induct on $|S|$. At the root test of an optimal tree,

$$
V(S)\le |S|+\sum_aV(S_a^*)
\le |S|+\sum_aF(S_a^*)=F(S).
$$

Combine with $V(S)\ge F(S)$. $\square$

In particular, assuming that the represented pool already dominates every possible test-plus-child-code recombination would conceal exact optimal-value computation. Restriction closure is affordable; exact closure under all recombinations is the missing optimization, not a bookkeeping convention.

### 15.5 A weaker oracle sufficient for a substantive improvement

Let $L=\lceil\log n\rceil$ and $\varepsilon=1/L$, fixed using the original instance size.

Suppose there is a recursively computable frozen-spine procedure whose actual unnormalized output cost is $U(S)$ and whose exits always have size at most $|S|/2$.

Replace the exact affine condition by

$$
\boxed{
U(S)\le
a_n W(Q)
+(1+\varepsilon)\sum_{B\in\mathrm{exits}(Q)}U(B)
+b_n|S|}
\tag{52}
$$

for every competing frozen spine $Q$, where $a_n,b_n\ge0$ and $a_n+b_n\ge1$.

The continuation values in (52) must be those of the same well-defined recursive construction. Independent estimates, changed code-pool snapshots, or exact conditional optima cannot silently replace them.

#### Conditional composition theorem

Under (52),

$$
\boxed{
U(H)\le e(a_n+b_n)F(H).}
\tag{53}
$$

If a pricing call takes $N^{O(L^c)}$ time and continuation-value queries for a fixed $c$, the full evaluation remains quasipolynomial.

#### Proof

For a nonsingleton state, every complete comparison spine has $W(Q)\ge|S|$. Thus absorb the additive term into the latency coefficient:

$$
U(S)\le(a_n+b_n)W(Q)
+(1+\varepsilon)\sum_BU(B).
$$

Put $d(S)=\lceil\log|S|\rceil$ and

$$
\beta_j=(a_n+b_n)(1+\varepsilon)^j.
$$

Every nonsingleton exit has $d(B)\le d(S)-1$. Apply induction and choose the spine of an optimal conditional tree:

$$
\begin{aligned}
U(S)
&\le(a_n+b_n)W(Q^*)
+(1+\varepsilon)\beta_{d(S)-1}\sum_BF(B)\\
&\le\beta_{d(S)}
\left(W(Q^*)+\sum_BF(B)\right)\\
&=\beta_{d(S)}F(S).
\end{aligned}
$$

The singleton base is zero. Since $d(H)=L$,

$$
(1+1/L)^L\le e,
$$

which proves (53).

Recursive query depth is at most $L$. Multiplying a per-call bound $N^{O(L^c)}$ across these levels gives

$$
N^{O(L^{c+1})},
$$

still quasipolynomial in the explicit input size. $\square$

Consequently, a pricing algorithm with

$$
a_n+b_n=O(\log L)
$$

would give an

$$
O(\log\log n)
$$

quasipolynomial approximation. That would be a substantive asymptotic improvement over $\log n/\log\log n$.

This target permits logarithmic latency loss and a small continuation inflation, rather than requiring a constant latency factor and exactly uninflated continuations.

### 15.6 What remains unproved

There is no established pricing procedure here satisfying (52), even for the coherently represented code pools in (47).

The generic value-query obstruction still prevents claiming (52) for arbitrary assigned valid-code costs. The coherent subclass avoids that particular construction, but avoiding a counterexample is not a pricing theorem.

The concrete remaining task is to exploit the actual template trees, their restrictions, and code reuse to obtain the $1+1/L$ continuation guarantee with latency loss $o(L/\log L)$.

The new unconditional statements in this section are (48), (49), and the exact-closure implication (51). Equation (53) is a conditional composition theorem, not an unconditional approximation ratio. The requested quasipolynomial bound remains unproved.

## 16. From an unproved pricing oracle to a concrete policy process

The relaxed pricing construction in Section 15 has not been completed. Before assuming a standard coverage argument can supply it, the actual restriction-cost objective needs to be checked.

### 16.1 Explicit code costs are neither submodular nor supermodular

For one fixed proper tree $T$, write

$$
V_T(S)=F(T|S).
$$

These are genuine coherent costs, but neither of the usual marginal-gain assumptions holds in general.

**Failure of submodularity.** Let $T$ be the balanced tree on four leaves, with sibling pairs $\{a,b\}$ and $\{c,d\}$. Then

$$
V_T(\{a\})=0,\qquad
V_T(\{a,b\})=V_T(\{a,c\})=2,
$$

and

$$
V_T(\{a,b,c\})=5.
$$

Adding $b$ to $\{a\}$ costs two, but adding it to the larger set $\{a,c\}$ costs three. This violates diminishing returns.

**Failure of supermodularity.** Let the root of $T$ separate a block $B$ of $b\ge3$ leaves from a two-leaf subtree $\{h,y\}$. Use any proper complete subtree on $B$. Then

$$
V_T(B\cup\{h\})-V_T(B)=b+1,
$$

whereas

$$
V_T(B\cup\{h,y\})-V_T(B\cup\{y\})=3.
$$

The marginal cost decreases when the underlying set grows.

Thus monotonicity, disjoint-partition consistency, and deletion stability do not put these costs into a standard submodular or supermodular optimization class.

### 16.2 The pruning benefit has unbounded complementarity

For a family of tests $\mathcal Q$, let its joint outcome cells be $\Pi(\mathcal Q)$ and define the saved code cost

$$
\Gamma_T(\mathcal Q)
=V_T(H)-\sum_{A\in\Pi(\mathcal Q)}V_T(A).
\tag{54}
$$

Take the preceding $B,\{h,y\}$ tree, and let $\tau_h,\tau_y$ be singleton tests for $h$ and $y$. The original matrix includes these tests and the tests of $T$.

Then

$$
\Gamma_T(\{\tau_h\})=\Gamma_T(\{\tau_y\})=3,
$$

but

$$
\Gamma_T(\{\tau_h,\tau_y\})=b+4.
$$

The marginal benefit of $\tau_y$ is three before $\tau_h$, and $b+1$ after it.

This rules out applying the ordinary maximum-coverage diminishing-returns proof to $\Gamma_T$. It is not a complexity lower bound, and it does not show that every other pricing algorithm fails.

### 16.3 A fully specified alternative: repeated complete-policy improvement

The next candidate avoids an unproved pricing oracle and keeps every continuation value tied to one well-defined actual policy.

Define $U_0(S)=F_G(S)$, the unnormalized cost of the complete greedy policy with a fixed state-consistent tie rule.

For $j\ge1$, the policy $R_j$ at a nonsingleton state $S$ chooses a splitting test minimizing

$$
|S|+\sum_a U_{j-1}(S_a),
\qquad S_a=S\cap\tau^{-1}(a),
\tag{55}
$$

and then executes $R_j$ recursively in its chosen children.

Let $U_j(S)$ be its **actual complete cost**, not merely the score in (55). All $U_j$ vanish on empty sets and singletons.

Since every selected test splits the candidate set, each output tree is proper and has at most $n-1$ internal nodes.

For fixed $q$, producing $R_q$ and its exact cost takes

$$
(nmK)^{O(q+1)}
\tag{56}
$$

time. To see this, each level-$j$ output has at most $n-1$ actual nodes; at each one, it evaluates at most $mK$ level-$(j-1)$ continuation policies, plus polynomial table work. Induction in $j$ gives (56).

Thus $q=(\log N)^{O(1)}$ is a genuine quasipolynomial computation. This is a mathematical construction only; no implementation is supplied.

### 16.4 Exact residual and improvement identities

For a splitting test $\tau$, define

$$
r_j(S,\tau)=
U_{j-1}(S)-|S|-\sum_a U_{j-1}(S_a).
\tag{57}
$$

Let

$$
\Delta_j(S)=U_{j-1}(S)-U_j(S).
$$

For every state,

$$
\boxed{\Delta_j(S)\ge0.}
\tag{58}
$$

Indeed, the root test of $R_{j-1}(S)$ is a candidate in (55), with score exactly $U_{j-1}(S)$. Induction on $|S|$ proves nonregression in the selected children.

If $\tau_j(S)$ is the chosen test, then

$$
\boxed{
\Delta_j(S)
=r_j(S,\tau_j(S))
+\sum_a\Delta_j(S_a).}
\tag{59}
$$

The chosen residual is the maximum over splitting tests, and is nonnegative because the previous policy's root has residual zero.

Consequently, for every splitting test,

$$
r_j(S,\tau)\le\Delta_j(S).
\tag{60}
$$

This inequality is valid even when the competitor's residual is negative.

For any complete comparison tree $T$, telescoping (57) over its internal nodes gives the exact identity

$$
\boxed{
U_{j-1}(H)-F(T)
=\sum_{v\in T\text{ internal}}
r_j(S_v,\tau_v).}
\tag{61}
$$

In particular, the excess of the current policy is the sum of its Bellman residuals on the comparison tree's states. Those states need not be visited by the current policy.

### 16.5 An unconditional convergence bound

Let $T^*$ be any complete optimal tree. Define

$$
\mathcal E_G(T^*)
=\sum_{v\in T^*\text{ internal}}
\left(F_G(S_v)-F(S_v)\right).
\tag{62}
$$

Every summand is nonnegative.

For every integer $q\ge1$,

$$
\boxed{
U_q(H)\le F(H)+\frac{\mathcal E_G(T^*)}{q}.}
\tag{63}
$$

#### Proof

Apply (61) to $T^*$ and use (60):

$$
U_{j-1}(H)-F(H)
\le\sum_{v\in T^*}\Delta_j(S_v).
$$

Sum over $j=1,\ldots,q$. Monotonicity (58) makes the left side at least

$$
q\left(U_q(H)-F(H)\right).
$$

For every comparison state, the right side telescopes:

$$
\sum_{j=1}^{q}\Delta_j(S_v)
=U_0(S_v)-U_q(S_v)
\le F_G(S_v)-F(S_v),
$$

because $U_q$ is the cost of a valid complete policy. This proves (63). $\square$

More generally, for any complete comparison tree $T$,

$$
U_q(H)\le
F(T)+\frac1q
\sum_{v\in T\text{ internal}}
\left(F_G(S_v)-F(S_v)\right).
\tag{64}
$$

The same proof applies. The algorithm does not need to know $T$, $F$, or the right-hand side.

This is an unconditional, instance-sensitive theorem for an explicitly defined quasipolynomial process. It is not yet a smaller worst-case approximation factor.

### 16.6 A valid but weaker moment corollary

Let $\beta_n$ bound greedy's ratio on every subinstance of size at most $n$. For fixed arity one can take $\beta_n=O(\log n/\log\log n)$, with finite small cases included.

Each conditional subtree of $T^*$ is itself optimal. Therefore

$$
\sum_{v\in T^*\text{ internal}}F(S_v)
=\frac12\sum_{h\in H}d^*(h)(d^*(h)+1).
\tag{65}
$$

The identity follows by summing a leaf's remaining depths $d^*(h),d^*(h)-1,\ldots,1$ along its ancestors.

Equations (63)-(65) give

$$
\boxed{
C_{R_q}\le
D+
\frac{\beta_n-1}{2q}
\mathbb E[d^*(h)(d^*(h)+1)].}
\tag{66}
$$

This controls instances with sufficiently bounded optimal depth moments. Arbitrary uniform instances do not have such a bound in terms of a fixed polylogarithm alone.

The exact excess budget (62) is potentially stronger: comparison states on which greedy is already optimal contribute zero.

### 16.7 Why the new rate theorem still does not close the target

The quantity in (62) can count one long selector's continuation error repeatedly. Here is a concrete illustration for a natural asymptotically optimal comparison tree.

Use a $C$-column, $r=2^b$-row grid, with $C=\lceil b^a\rceil$ for a fixed $a>1$. Provide column membership, column-gated row bits, and row decoys whose small child at size $s$ has

$$
1+\lfloor2s/C\rfloor
$$

rows. Use $C\ge6$ and sufficiently large $b$.

On every state consisting of at least $C/2$ complete columns, greedy follows row decoys while more than $C^2$ rows remain: their minority fraction is strictly greater than $2/C$, while column tests have minority fraction at most $2/C$.

The decoy answer entropy is at most $H_2(3/C)$ in that range. Consequently the conditional greedy cost is

$$
\Omega(Cb/\log C).
$$

Conditional optimum is at most $C+b$, using columns first and then row bits.

The column-first comparison tree $T_{\mathrm{col}}$ has at least $C/2$ spine states of size at least $n/2$. Hence

$$
\sum_{v\in T_{\mathrm{col}}}
\left(F_G(S_v)-F(S_v)\right)
=\Omega(nC^2b/\log C).
\tag{67}
$$

Its own cost is $\Theta(nC)$. Giving the row for free leaves uniform singleton search on the columns, so its cost is also within $1+o(1)$ of the unrestricted optimum.

Thus the normalized excess budget in (64) can be larger than the greedy approximation factor by another factor of order $C$. For every fixed polylogarithmic round count, $a$ can be chosen large enough that this bound is uninformative compared with nonregression.

This does **not** prove that $R_q$ performs badly on the grid, and does not prove that all optimal comparison trees have this excess budget. It shows that charging every state of a near-optimal long spine independently is insufficient to obtain the desired uniform rate.

The necessary improvement is to charge the residuals of a whole selector spine jointly, or otherwise compare them with the actual cost decreases (59), without multiplying the same continuation error by the spine length.

### 16.8 Research status

The coherent pricing route has not yielded a constructive guarantee. Its pruning objective has genuine complementarity, so standard coverage results cannot simply be imported.

The alternative process is fully specified, computable in genuine quasipolynomial time for polylogarithmic rounds, and has the unconditional bounds (63)-(66). The missing step is now a global rate bound for its actual residual decreases, not the existence of an unspecified pricing oracle.

No unconditional $o(\log n/\log\log n)$ worst-case approximation has been proved in this continuation.

## 17. A computable whole-spine correction: supported-state recombination

The residual sum in Section 16 counts the same continuation error many times along a selector spine. Instead of assuming an affine pricing oracle to remove that count, one can reuse all the states and code trees already discovered by the continuation computation.

This yields an explicit algorithmic modification with exact supported-spine guarantees. It does not yet yield an improved worst-case approximation factor.

### 17.1 Exact optimization on a finite represented state family

Let $\mathcal S$ be a finite family of candidate subsets of $H$, containing $H$, the empty set, and all singletons.

Assume every represented nonsingleton is the root of at least one known complete proper code whose node states are also in $\mathcal S$. Codes may have different root domains; all use original tests.

For a splitting test $\tau$ at $S$, its edge is **supported** if every nonempty outcome set

$$
S_a=S\cap\tau^{-1}(a)
$$

belongs to $\mathcal S$.

Define

$$
J_{\mathcal S}(S)=0
\quad\text{if }|S|\le1,
$$

and otherwise

$$
\boxed{
J_{\mathcal S}(S)
=|S|+
\min_{\tau\text{ splitting }S\text{ with supported outcomes}}
\sum_a J_{\mathcal S}(S_a).}
\tag{68}
$$

This is evaluated in increasing candidate-set size. Every supported child is strictly smaller than its parent.

#### Proposition

Equation (68) is the exact minimum unnormalized cost of a complete tree whose every node state is represented in $\mathcal S$. It is computable in time polynomial in $n,m,K,|\mathcal S|$.

#### Proof

The retained complete code supplies a feasible supported root edge and feasible descendants, so every value is finite.

At any proper complete tree's root, conditional costs add as $|S|+\sum_a F(T_a)$. Induction on $|S|$ proves both the lower bound and attainability in (68).

Each state checks at most $m$ original tests and their at most $K$ outcomes. Exact set representations and lookup give polynomial processing cost. $\square$

The minimization may use an edge not selected in any retained code, provided its outcome states were independently represented. Thus it recombines codes across trials rather than merely selecting the cheapest stored full tree.

### 17.2 Whole supported spines are handled without a length factor

Let $Q$ be a valid comparison spine from a represented state $S$. Its exit family includes the final unfinished continuation set, if any. Suppose all its continuation states and exit states belong to $\mathcal S$. Then

$$
\boxed{
J_{\mathcal S}(S)
\le W(Q)+
\sum_{A\in\mathrm{exits}(Q)}J_{\mathcal S}(A).}
\tag{69}
$$

#### Proof

At every query of $Q$, its outcome states are represented, so (68) permits its root edge. Follow those edges down the spine, choosing the minimum represented continuation code at each exit.

The result is a complete supported tree with the displayed cost. Equivalently, repeatedly apply (68) along the spine and telescope. $\square$

There is no multiplicative latency loss, continuation inflation, or dependence on the number of queries in $Q$.

The important qualification is support. Equation (69) cannot be applied to a comparison spine with states absent from $\mathcal S$.

### 17.3 A small example of strict cross-trial recombination

Let

$$
H=\{1,2,3,4,5,6\},
$$

and provide singleton tests for $1,2,3,4$ and the test with positive set $\{3,4,5\}$. These tests distinguish every pair.

Consider two valid full codes:

- $T_1$: first test singleton $1$. On the negative branch, test $\{3,4,5\}$ and then identify the triple $\{3,4,5\}$ and the pair $\{2,6\}$.
- $T_2$: first test singleton $3$. On the negative branch, test $\{3,4,5\}$ and then identify the pair $\{4,5\}$ and the triple $\{1,2,6\}$.

Every pair has complete-code cost two, and every triple has cost five. Thus both full codes have cost

$$
6+5+5+2=18.
$$

Their combined state family contains both triples $\{3,4,5\}$ and $\{1,2,6\}$. At the root, (68) may therefore use the test $\{3,4,5\}$ immediately, giving

$$
6+5+5=16.
$$

This is globally optimal: the binary information lower bound gives $6\log6>15$, and the unnormalized cost is an integer.

The example illustrates recombination, not the global approximation guarantee on arbitrary instances.

### 17.4 Generating the state family without an assumed oracle

Fix a positive integer probe budget $q$.

Use the complete-policy process $R_q$ of Section 16. While evaluating a probe $R_q(S)$, retain:

1. Every complete policy tree actually produced in the recursive continuation evaluations, including greedy base trees.
2. Every node state of those trees.
3. Every candidate state on which a continuation call is made.

Every retained candidate state has a produced complete code, and all its node states are retained. Thus the feasibility assumption of Section 17.1 holds.

The work and number of represented states from one probe are bounded by

$$
(nmK)^{O(q+1)}.
\tag{70}
$$

Now define the following finite-descent construction.

1. Start with the complete greedy tree on $H$ and its represented states.
2. Keep a current incumbent complete tree.
3. For every node state of the incumbent, run the above $R_q$ probe and add all produced states and codes to $\mathcal S$.
4. Recompute (68), and obtain a minimum-cost supported complete tree on $H$.
5. If its root cost is strictly smaller, adopt it and repeat.
6. Otherwise stop, retaining the previous incumbent.

The construction does not discard discovered states.

On a nonimproving pass it keeps the incumbent rather than enumerating equal-cost alternatives. This is part of the definition and avoids an unsupported convergence claim about exploring plateaus.

No step queries an optimal cost or an unproved pricing oracle.

### 17.5 Quasipolynomial running time is unconditional

Every proper complete tree has at most $n-1$ internal nodes and maximum depth at most $n-1$. Therefore its unnormalized cost is an integer at most $n(n-1)$.

Each successful pass decreases that integer by at least one. There are consequently at most $n(n-1)$ successful passes and one final nonimproving pass.

Each pass probes at most $2n-1$ incumbent node states. By (70), the total represented family and the time spent generating it remain

$$
(nmK)^{O(q+1)}.
$$

Repeated evaluation of the polynomial-size supported-state recurrence adds only a polynomial factor in the accumulated family size.

Thus the full finite-descent construction takes

$$
\boxed{(nmK)^{O(q+1)}\text{ time}.}
\tag{71}
$$

For $q=(\log N)^{O(1)}$, with fixed exponent, this is genuine quasipolynomial time in the explicit input size $N$.

This is a proof of running time, not an implementation.

### 17.6 Unconditional output and stability guarantees

Let $T_{\mathrm{out}}$ be the final incumbent, and let $\mathcal S_{\mathrm{final}}$ include the states added in the last nonimproving pass.

Then

$$
\boxed{
F(T_{\mathrm{out}})
=J_{\mathcal S_{\mathrm{final}}}(H)
\le U_q(H)\le F_G(H).}
\tag{72}
$$

The root $R_q(H)$ probe is included in every pass, so its complete code is always a supported competitor.

Moreover, at every node state $S$ of the final incumbent,

$$
\boxed{
F(T_{\mathrm{out}}|S)
=J_{\mathcal S_{\mathrm{final}}}(S)
\le U_q(S).}
\tag{73}
$$

#### Proof of the node equality

The incumbent subtree is a supported code, giving the inequality $J_{\mathcal S_{\mathrm{final}}}(S)\le F(T_{\mathrm{out}}|S)$.

If the inequality were strict, replacing that subtree by its cheaper supported code would strictly reduce the root unnormalized cost. That would contradict the last pass being nonimproving.

The probe at $S$ supplies the final inequality in (73). $\square$

For every supported spine $Q$ starting at such a state $S$, (69) and (73) consequently give

$$
\boxed{
F(T_{\mathrm{out}}|S)
\le W(Q)+
\sum_{A\in\mathrm{exits}(Q)}
J_{\mathcal S_{\mathrm{final}}}(A).}
\tag{74}
$$

This is an actual, computably maintained whole-spine comparison property. It is not the affine oracle assumption from Section 13.

It also implies the usual probe-neighborhood guarantee: the final incumbent subtree is no more expensive than any depth-$q$ prefix with complete greedy continuations. The probe recursion evaluates every test history of length at most $q$ and includes the greedy completion codes at the horizon states.

### 17.7 What this fixes, and what it does not

The construction fixes two specific problems:

- A long represented selector is handled jointly by exact dynamic programming, not by summing its error independently at every query.
- Useful codes discovered in different continuation trials can be recombined into one complete policy.

However, an unknown optimal comparison tree can contain candidate states that are absent from the represented family.

There is no proof here that the final family contains a complete tree of cost

$$
o(\log n/\log\log n)\,F(H).
$$

Nor is there a proof that stability (74) forces that bound when optimal states are missing.

If all states of an optimal tree were represented, (68) would recover an optimum. That observation does not prove they are generated within the quasipolynomial budget.

The only inherited unconditional worst-case approximation factor currently established for this construction is the greedy bound, by (72).

### 17.8 Current most promising route

The route is now a concrete **probe, retain, recombine, and descend** process, rather than a hypothetical continuation-pricing oracle.

The next substantive proof would show either:

1. The represented state family necessarily contains a sufficiently good complete comparison tree; or
2. Whole-spine stability on the generated states controls the residual contribution of missing comparison states.

Both statements remain unproved. No smaller unconditional quasipolynomial worst-case ratio is claimed.

## Source

Ray Li, Percy Liang, and Stephen Mussmann, *A Tight Analysis of Greedy Yields Subexponential Time Approximation for Uniform Decision Tree*, arXiv:1906.11385v2 / SODA 2020.

- [Local paper](1906.11385v2.pdf)
- [Primary arXiv version](https://arxiv.org/abs/1906.11385v2)
- Used: Theorem 3.1, its uniform leading-$4+\varepsilon$ refinement, and the exact additive prefix optimization.
- Improved relative to: the stated $(9+\varepsilon)/\alpha$ frontier and its per-generation OPT charging.
- The shared-budget estimate (20) and the generation-dependent schedule (22) are the additional arguments in this continuation; they do not follow by substituting parameters into that stated frontier.
