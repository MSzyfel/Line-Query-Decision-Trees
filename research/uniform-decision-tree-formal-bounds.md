# Uniform Decision Tree: formal refinements and subsequent proof attempts

**Date:** 2026-10-11  
**Model:** equiprobable hypotheses, unit-cost tests, at most $K\ge2$ outcomes per test, with $K$ fixed.

**Current proved results:** [the improved-tradeoff proof](uniform-decision-tree-improved-tradeoffs.md) supplies additional cost-mass, height-certificate, and shared-budget arguments. They improve constant quasipolynomial running-time powers and the subexponential constant-factor frontier: the leading curve is $5/\alpha$ instead of $9/\alpha$, and a 10-approximation has powers arbitrarily close above $143/288$ rather than $9/10$. Section 14 summarizes them. Refinements that leave a growing runtime power in the same asymptotic order are not counted under the user's stricter criterion. A strict-quasipolynomial little-$o$ ratio and a little-$o$ reduction in a growing runtime power remain unproved.

**Latest scope clarification:** the user seeks a substantive quasipolynomial asymptotic improvement, not the incremental frontiers above. That target has not been achieved. Section 13 of [the tradeoff note](uniform-decision-tree-improved-tradeoffs.md) proves a barrier for the current cutoff paradigm and states the exact continuation-preserving spine oracle needed by a different route.

Section 14 pushes that oracle further: exact continuation optima satisfy an ideal affine bound, while arbitrary assigned valid-code costs admit a black-box query obstruction. A constructive code-extension lemma identifies reuse/coherence that the actual recursive algorithm would need to exploit. None of these results is claimed to complete the quasipolynomial target.

Section 15 of the tradeoff note gives genuine partition and deletion consistency for finite code pools, but also explains why those properties alone are insufficient. It weakens the pricing target to small continuation inflation: a $1+1/\log n$ factor on future costs with $O(\log\log n)$ latency loss would suffice. That pricing theorem is not proved.

Section 16 checks the objective's non-submodularity and switches to a fully specified complete-policy improvement process. It proves an unconditional instance-sensitive convergence rate through Bellman residual identities. Independent state charging still overcounts long selector spines, so the strict-quasipolynomial worst-case improvement remains unproved.

Section 17 gives an oracle-free modification: retain probe states and code trees, recombine them exactly on a finite state DAG, and iterate strict integer-cost improvements. It has unconditional quasipolynomial running time and exact comparison against supported spines of arbitrary length. A global coverage theorem for missing optimal states, and hence a better worst-case ratio, is not established.

**Latest lower-bound investigation:** [the shared lower-bounds note](uniform-decision-tree-lower-bounds.md) develops globally budgeted conditional entropy and shared-query cover, completion-profile relaxations, and a local-policy flow hierarchy. Its certificate-guided code generator repairs the explicit gated-grid family in quasipolynomial time; no smaller general worst-case ratio is claimed.

All logarithms in this document are base two, except for the constant $e$.

The two directions are:

1. Majority-stable MSSC accounting, strengthened by the entropy cost of identification within the sets peeled off by an optimal spine.
2. Continuation-aware rollout, with an explicit improvement over a uniform upper bound for its greedy continuations.

The result is a **lower-order improvement**, not an improvement of the $O(\log n/\log\log n)$ asymptotic order.

## 1. Statements

Write

$$
\kappa=\log K,\qquad
L=\log n,\qquad
M=\frac{L}{\kappa}=\log_K n,\qquad
\ell=\log M,
$$

and let $D=C_{\mathrm{OPT}}$. Define

$$
g_K(n)=\frac{4L}{\ell}-\frac{L}{4\ell^3}.
$$

### Theorem 1: entropy-corrected greedy bound

For every valid instance with $\ell\ge16$, the greedy rule minimizing the largest outcome class satisfies

$$
\boxed{\frac{C_G}{C_{\mathrm{OPT}}}
\le \frac{4L}{\ell}-\frac{L}{4\ell^3}.}
\tag{T1}
$$

This holds for any fixed deterministic greedy tie rule. The threshold is deliberately conservative.

### Theorem 2: rollout bonus

Let $R$ choose, at each candidate set $S$, a splitting test minimizing

$$
|S|+\sum_a F_G(S_a),
\qquad S_a=S\cap\tau^{-1}(a),
$$

and recursively apply the same rule in its children. Here $F_G(A)$ is the unnormalized cost of a complete greedy tree on $A$, with one fixed, state-consistent tie rule.

If $\beta(n)\ge1$ bounds greedy's approximation ratio on **every** valid subinstance with at most $n$ hypotheses, then

$$
\boxed{C_R\le \beta(n)D-(\beta(n)-1).}
\tag{T2}
$$

In particular, for fixed $K$ and sufficiently large $n$,

$$
\boxed{\frac{C_R}{C_{\mathrm{OPT}}}
\le \frac{4L}{\ell}
-\frac{L}{4\ell^3}
-\frac{\kappa}{2\ell^2}.}
\tag{T3}
$$

Both rules are polynomial-time on an explicitly given hypothesis-test table. No implementation is needed for the proofs below.

For binary tests, these bounds become

$$
\frac{C_G}{C_{\mathrm{OPT}}}
\le
\frac{4\log n}{\log\log n}
-\frac{\log n}{4(\log\log n)^3},
$$

and

$$
\frac{C_R}{C_{\mathrm{OPT}}}
\le
\frac{4\log n}{\log\log n}
-\frac{\log n}{4(\log\log n)^3}
-\frac{1}{2(\log\log n)^2}.
$$

These refine the usual $(4+\varepsilon)\log n/\log\log_K n$ worst-case statement from the supplied paper. They do **not** establish an $o(\log n/\log\log n)$ approximation or a leading constant strictly smaller than four by a fixed amount.

## 2. Basic notation and cost identities

For a nonempty subset $U$, let $F(U)$ be its optimal unnormalized identification cost and

$$
d(U)=\frac{F(U)}{|U|}.
$$

For any complete tree,

$$
F(T)=\sum_{v\text{ internal}}|U_v|.
\tag{1}
$$

Entropy gives

$$
F(U)\ge |U|\log_K|U|,
\qquad D\ge M.
\tag{2}
$$

For any partition $\{U_1,\ldots,U_a,O\}$ of the hypotheses,

$$
\sum_{i=1}^a F(U_i)+F(O)\le F(H).
\tag{3}
$$

To prove (3), restrict one optimal tree on $H$ to each part and delete tests whose answer is determined on that part. Each hypothesis incurs no more than its original depth. Then replace each restricted tree by an optimal tree for its part.

Empty sets have cost zero. Expressions of the form $0\log0$ are interpreted as zero.

## 3. The entropy-corrected MSSC comparison

For a candidate set $U$ of size $u$, fix, for every test $\tau$, one largest outcome label $a_\tau(U)$. Consider the MSSC instance with universe $U$ and sets

$$
A_\tau(U)=U\setminus\tau^{-1}(a_\tau(U)),
$$

together with every singleton $\{h\}$, $h\in U$. The singleton sets are an **analytical MSSC device**, not added decision-tree tests.

Let $m(U)$ be the minimum average cover time in this MSSC instance.

### Lemma 1

For $u\ge2$,

$$
m(U)\le d(U)+\frac1u,
\tag{4}
$$

and, more importantly,

$$
\boxed{
m(U)\le
d(U)-\frac{\log u}{\kappa}
\frac{\log\!\left(e(d(U)+1/u)\right)+\log(K-1)}{\kappa}
\frac1u.}
\tag{5}
$$

#### Proof

Take a complete optimal tree on $U$. Starting at its root, follow the outcome label $a_\tau(U)$ at each encountered test, with the labels frozen relative to the original $U$.

For $K>2$, this frozen label may have no consistent hypothesis at a later node. In that case stop at that empty outcome. Otherwise stop at a singleton leaf.

Every hypothesis either:

- Exits this path at some test $i$, through one of the at most $K-1$ other outcomes; or
- Is the terminal singleton, if the path ends at a nonempty leaf.

List the MSSC sets associated with the tests on this path. If a singleton remains, append its singleton set. This covers $U$.

Let $\mu$ be the average number of path tests incurred by a hypothesis before exiting or reaching the terminal leaf. If $A$ is this ordering's average cover time, then

$$
A=\mu+\frac{\eta}{u},
\qquad \eta\in\{0,1\}.
\tag{6}
$$

The extra unit is paid only by a terminal singleton. Since $\mu\le d(U)$, (4) follows.

Let $J$ be the cover index in this ordering. It is a positive-integer random variable with mean $A$.

For a positive-integer variable of mean $A\ge1$,

$$
H(J)\le
\log A+(A-1)\log\!\left(1+\frac1{A-1}\right)
\le \log(eA).
\tag{7}
$$

The first inequality follows by comparison with the geometric distribution of mean $A$; the second uses $\ln(1+x)\le x$. At $A=1$, take the limiting expression, or observe that $J=1$ almost surely.

Let $Z$ record the exit outcome when $J$ corresponds to a path test. Conditional on any such $J$, it has at most $K-1$ possibilities. For a terminal singleton it is deterministic. Thus

$$
H(J,Z)\le \log(eA)+\log(K-1).
\tag{8}
$$

Conditioning on $(J,Z)$ partitions $U$ into the off-path groups and possibly one terminal singleton. Hypotheses remain uniform inside each group.

The residual subtrees identify those groups and therefore incur average cost at least

$$
\frac{H(h\mid J,Z)}{\kappa}
=\frac{\log u-H(J,Z)}{\kappa}.
$$

Consequently,

$$
d(U)-\mu
\ge \frac{\log u-\log(eA)-\log(K-1)}{\kappa}.
$$

Using (6) gives

$$
A\le d(U)-\frac{\log u}{\kappa}
+\frac{\log(eA)+\log(K-1)}{\kappa}+\frac1u.
$$

Finally $A\le d(U)+1/u$, so replacing $A$ inside the logarithm by this upper bound proves (5), since $m(U)\le A$. $\square$

The essential extra term is $-(\log u)/\kappa$. An optimal spine cannot use its entire identification budget merely to peel off groups: enough budget must remain to identify hypotheses inside those groups.

## 4. Greedy chains and balanced-node entropy

For a subset $U$, define its best complement-of-largest-outcome size by

$$
\sigma(U)=
\max_{\tau}
\left(|U|-\max_a |U\cap\tau^{-1}(a)|\right).
$$

If $R\subseteq U$, then

$$
\sigma(R)\le\sigma(U).
\tag{9}
$$

Indeed, for each fixed test the expression is

$$
\min_a |U\setminus\tau^{-1}(a)|,
$$

and every term is nondecreasing under inclusion. Taking a minimum and then a maximum preserves this monotonicity.

Fix $0<\delta\le1/2$, and set

$$
q=\log(1/\delta),
\qquad t=\left\lfloor\frac{L}{q}\right\rfloor.
$$

A greedy-tree node with candidate set $U_v$ is **level-$j$ skewed** if

$$
\sigma(U_v)\le n\delta^j,
\qquad |U_v|>2n\delta^j.
\tag{10}
$$

It is balanced if it is not skewed at any level.

### Lemma 2: chain reduction

For every fixed level $j$:

1. Its skewed nodes form disjoint downward chains following largest outcomes.
2. The candidate sets at the roots of these chains are disjoint.
3. If a chain starts with universe $U$, its total normalized cost is at most

$$
4\frac{|U|}{n}m(U).
\tag{11}
$$

#### Proof

Put $b=n\delta^j$.

At a level-$j$ node, the total size of all nonlargest children is at most $b$. None of those children can contain a later level-$j$ node, which would need more than $2b$ hypotheses.

If an ancestor and a descendant are both level-$j$, all intermediate nodes are too, by (9) and the monotonicity of candidate-set size. Thus each component is a largest-outcome chain. Its maximal nodes are incomparable, so their universes are disjoint.

For a chain rooted at $U$, every test's complement of its largest outcome on $U$ has size at most $b$. At every later chain state $R$, $|R|>2b$, and this complement still has size at most $b$ inside $R$. The original largest outcome therefore remains a strict majority and keeps the same label.

Hence the sets $A_\tau(U)$ have stable labels along the chain. Its remaining candidate set is exactly the set of elements not yet covered by the previously selected MSSC sets.

Greedy chooses the test covering the largest number of currently uncovered elements. The added singleton sets cannot beat it: a valid nonsingleton candidate state has a splitting test covering at least one element.

Thus the chain is a prefix of an MSSC-greedy ordering. Complete that ordering greedily. Its full MSSC cost is at least the chain cost, and the standard MSSC theorem bounds it by four times $m(U)$. This proves (11). $\square$

### Lemma 3: balanced-node cost

The normalized cost of all balanced nodes is at most

$$
\frac{L}{H_2(\delta/2)},
\tag{12}
$$

where $H_2$ is binary entropy.

#### Proof

At a balanced node,

$$
\frac{\sigma(U_v)}{|U_v|}\ge\frac{\delta}{2}.
\tag{13}
$$

If $\sigma(U_v)/n>\delta$, this is immediate. Otherwise choose $j\ge1$ such that

$$
\delta^{j+1}<\sigma(U_v)/n\le\delta^j.
$$

Since the node is not level-$j$ skewed, $|U_v|/n\le2\delta^j$, which implies (13). Validity gives $\sigma(U_v)\ge1$, so all relevant levels lie within $1,\ldots,t$.

If the largest outcome has probability at least $1/2$, merging all other outcomes gives entropy at least $H_2(\delta/2)$. If its probability is below $1/2$, the answer entropy is at least one bit, also enough.

The entropy decomposition of a complete tree is

$$
L=\sum_{v\text{ internal}}\frac{|U_v|}{n}
H(\text{answer at }v\mid U_v).
$$

Applying the lower bound at balanced nodes proves (12). $\square$

Let

$$
T_j=\sum_{U\text{ a level-}j\text{ chain universe}}
\frac{|U|}{n}m(U).
$$

Nodes can be skewed at more than one level; counting such nodes more than once only increases the upper bound. Lemmas 2 and 3 therefore give

$$
C_G\le \frac{L}{H_2(\delta/2)}+4\sum_{j=1}^{t}T_j.
\tag{14}
$$

## 5. Retaining the entropy credit when summing a level

Define

$$
c_K(D)=
\frac{\log\!\left(e(D+1/2)+1\right)+\log(K-1)}{\kappa}
+\frac12.
\tag{15}
$$

### Lemma 4

For each level $j$,

$$
\boxed{
T_j\le D-M+\frac{jq}{\kappa}+c_K(D).}
\tag{16}
$$

Also, if $a_j$ is the number of its chains,

$$
T_j\le D+\frac{a_j}{n}.
\tag{17}
$$

#### Proof

Let its disjoint chain universes be $U_i$, with sizes $u_i$, masses $p_i=u_i/n$, and conditional optimum costs $d_i=d(U_i)$. Let $O$ be their complement, of mass $p_0$.

Equation (3) and the entropy lower bound for $O$ give

$$
\sum_i p_i d_i
\le D-\frac{p_0\log(np_0)}{\kappa}.
\tag{18}
$$

Applying Lemma 1 to all $U_i$, and retaining all the entropy terms, yields

$$
\begin{aligned}
T_j\le {}&
D-M+\frac{H(p_0,p_1,\ldots)}{\kappa}\\
&+\frac{\sum_i p_i\log(e(d_i+1/u_i))}{\kappa}\\
&+\frac{(\sum_i p_i)\log(K-1)}{\kappa}
+\frac{a_j}{n}.
\end{aligned}
\tag{19}
$$

This identity uses

$$
p_0\log(np_0)+\sum_i p_i\log(np_i)
=L-H(p_0,p_1,\ldots).
$$

Every chain universe has size greater than $2n\delta^j$. Thus

$$
a_j<\frac1{2\delta^j},
\qquad
H(p_0,p_1,\ldots)\le\log(a_j+1)\le jq.
\tag{20}
$$

The last inequality uses $\delta^j\le1/2$.

Since $j\le t$, $n\delta^j\ge1$. Hence $u_i>2$ and $a_j/n\le1/2$.

Add the outside term $p_0\log1=0$ and apply Jensen's inequality:

$$
\begin{aligned}
\sum_i p_i\log(e(d_i+1/u_i))
&\le \log\left(e\sum_i p_i d_i+e\,a_j/n+p_0\right)\\
&\le \log\left(e(D+1/2)+1\right).
\end{aligned}
\tag{21}
$$

Combining (19)-(21) gives (16).

Finally, (4) and disjointness directly give (17). $\square$

The entropy of the partition in (19) is essential. One must not replace it by zero or assume that optimal entropy excess is nonincreasing under arbitrary conditioning.

## 6. Two master bounds

Because $D\ge M$, the coefficient $D-M+c_K(D)$ is nonnegative. Summing (16), with $t\le L/q$, gives

$$
\begin{aligned}
\sum_{j=1}^{t}T_j
&\le t(D-M+c_K(D))
+\frac{q}{\kappa}\frac{t(t+1)}2\\
&\le
\frac{DL}{q}-\frac{LM}{2q}
+\frac{c_K(D)L}{q}+\frac{M}{2}.
\end{aligned}
$$

Substitute into (14):

$$
\boxed{
C_G\le
\frac{L}{H_2(\delta/2)}
+\frac{4DL}{q}
-\frac{2LM}{q}
+\frac{4c_K(D)L}{q}
+2M.}
\tag{22}
$$

For a simpler bound, use (17). The singleton-completion overhead sums geometrically:

$$
\sum_{j=1}^{t}\frac{a_j}{n}
\le\frac1{2n}\sum_{j=1}^{t}\delta^{-j}
\le\frac1{2(1-\delta)}.
$$

Therefore

$$
\boxed{
C_G\le
\frac{L}{H_2(\delta/2)}
+\frac{4DL}{q}
+\frac2{1-\delta}.}
\tag{23}
$$

In particular, the final term is at most four. No unjustified zero-overhead comparison between a full MSSC cover and a complete decision tree is used.

## 7. Proof of Theorem 1

Assume $\ell\ge16$, so $M=2^\ell$. We use

$$
H_2(\delta/2)\ge
\frac{\delta}{2}\log(2/\delta)
=\frac{\delta}{2}(q+1).
\tag{24}
$$

### Case I: $D\le2M\ell$

Take $\delta=1/M$, so $q=\ell$. From (22) and (24),

$$
\frac{C_G}{D}
\le
\frac{4L}{\ell}
-\frac{2LM}{D\ell(\ell+1)}
+\frac{4c_K(D)L}{D\ell}
+\frac{2M}{D}.
\tag{25}
$$

In this range,

$$
e(D+1/2)+1\le3eM\ell.
$$

Since $\kappa\ge1$ and $\log(K-1)\le\kappa$, (15) implies

$$
c_K(D)\le
\ell+\log\ell+\log(3e)+\frac32
\le3\ell.
\tag{26}
$$

For $\ell\ge16$,

$$
\frac{14\ell(\ell+1)}{M}\le1.
\tag{27}
$$

It holds at 16, and $2^\ell/(\ell(\ell+1))$ is increasing thereafter.

Using $L=\kappa M\ge M$, (26)-(27) give

$$
\frac{4c_K(D)(\ell+1)}{M}
+\frac{2\ell(\ell+1)}{L}
\le1.
$$

Factor the last three terms of (25) by $LM/(D\ell(\ell+1))$. Their coefficient is at most $-1$. Hence

$$
\frac{C_G}{D}
\le\frac{4L}{\ell}
-\frac{LM}{D\ell(\ell+1)}
\le\frac{4L}{\ell}
-\frac{L}{2\ell^2(\ell+1)}
\le\frac{4L}{\ell}-\frac{L}{4\ell^3}.
\tag{28}
$$

### Case II: $D>2M\ell$

Take $\delta=\ell/D$, so

$$
q=\log(D/\ell)>\ell+1.
$$

Equations (23)-(24) imply

$$
\frac{C_G}{D}
\le
\frac{4L}{q}
+\frac{2L}{\ell(q+1)}
+\frac4D
\le
\frac{(4+2/\ell)L}{\ell+1}+\frac4D.
\tag{29}
$$

The difference between $4L/\ell$ and the first term on the right is

$$
\frac{2L}{\ell(\ell+1)}.
$$

Also,

$$
\frac4D<\frac2{M\ell}
\le\frac{L}{2\ell^2},
$$

because $4\ell\le LM$ for $\ell\ge16$. Since $\ell+1\le2\ell$,

$$
\frac{C_G}{D}
\le\frac{4L}{\ell}-\frac{L}{2\ell^2}
\le\frac{4L}{\ell}-\frac{L}{4\ell^3}.
\tag{30}
$$

Together, (28) and (30) prove Theorem 1. $\square$

## 8. Proof of Theorem 2

Write $F_R(S)$ for the unnormalized rollout cost.

First,

$$
F_R(S)\le F_G(S)
\tag{31}
$$

by induction on $|S|$. The greedy root test is an admissible candidate in the rollout minimization, and its score equals $F_G(S)$. The recursively constructed rollout children cost no more than their greedy continuations.

More precisely, for every splitting test $\tau$,

$$
F_R(S)\le |S|+\sum_a F_G(S_a).
\tag{32}
$$

Let $\tau^*$ be an optimal root test. The exact optimal recurrence gives

$$
F(S)=|S|+\sum_a F(S_a^*).
$$

If $\beta(n)$ bounds greedy on all subinstances of size at most $n$, then (32) gives

$$
\begin{aligned}
F_R(H)
&\le n+\beta(n)\sum_a F(H_a^*)\\
&= \beta(n)F(H)-(\beta(n)-1)n.
\end{aligned}
$$

Divide by $n$ to obtain (T2). $\square$

The subtraction is an unconditional improvement relative to any valid uniform continuation bound. A bound only for the original instance, rather than for every smaller instance, would not justify this argument.

## 9. A valid subproblem envelope and proof of the rollout corollary

Define

$$
\beta_0(K)=\max\{K^2,\ 24576\kappa+2\}.
\tag{33}
$$

For all sufficiently large $n$ satisfying

$$
\ell\ge16,\qquad g_K(n)\ge\beta_0(K),
\tag{34}
$$

$g_K(n)$ bounds greedy's ratio on every subinstance of size at most $n$.

To see this, let a subinstance have size $u$, information lower bound $M_u=\log_Ku$, and optimum $d$.

- If $M_u<2$, then $u<K^2$. Greedy uses at most $u-1$ tests on each path, so its ratio is at most $K^2$.
- If $2\le M_u<2^{16}$, then $d\ge M_u\ge2$. Apply (23) with $\delta=1/d$ and (24):

$$
\frac{C_G(U)}d
\le \frac{6\log u}{\log d}+2
\le\frac{6\kappa M_u}{\log M_u}+2
\le24576\kappa+2.
$$

The last inequality uses

$$
\max_{2\le x\le2^{16}}\frac{x}{\log x}
=\frac{2^{16}}{16}=4096.
$$

- If $M_u\ge2^{16}$, Theorem 1 gives $g_K(u)$. The function $g_K(u)$ is increasing in $u$ when $\log\log_Ku\ge16$, as follows by differentiation.

This proves the required uniform envelope under (34). Such $n$ exist because $g_K(n)\to\infty$ for fixed $K$.

Now apply Theorem 2 with $\beta(n)=g_K(n)$.

If $D\le2M\ell$, then $g_K(n)-1\ge L/\ell$ in the stated range, and

$$
\frac{g_K(n)-1}{D}
\ge\frac{L/\ell}{2M\ell}
=\frac{\kappa}{2\ell^2}.
$$

Thus

$$
\frac{C_R}{D}
\le g_K(n)-\frac{\kappa}{2\ell^2}.
$$

If $D>2M\ell$, (31) and the stronger large-$D$ estimate (30) give

$$
\frac{C_R}{D}
\le \frac{4L}{\ell}-\frac{L}{2\ell^2}
\le g_K(n)-\frac{\kappa}{2\ell^2},
$$

where the last inequality follows from $L(1-1/(2\ell))\ge\kappa$.

This proves (T3). $\square$

## 10. Why the partition-entropy term cannot be dropped

Here is a concrete obstruction to the stronger, but false, amortization claim

$$
\sum_i\left(F(U_i)-|U_i|\log_K|U_i|\right)
\le F(H)-n\log_Kn.
$$

Take $H=\{0,1\}^3$, with its three coordinate tests and one additional test indicating Hamming weight at most one.

The full instance has optimum $F(H)=8\cdot3=24$: coordinate tests attain the entropy bound.

Partition it into

$$
A=\{000,100,010,001\},
\qquad
B=\{111,110,101,011\}.
$$

On each part, the extra test is constant. Each coordinate test isolates one hypothesis, possibly with the outcome labels reversed. Therefore every first test has a $1$ versus $3$ split, and the optimum unnormalized cost is

$$
F(A)=F(B)=4+(3+2)=9.
$$

The two conditional entropy excesses are each $9-4\log4=1$, while the full instance's excess is $24-8\log8=0$.

Thus arbitrary conditioning can create positive excess from zero excess. The proof above avoids this mistake: it retains the partition entropy in (19) and bounds that entropy by the number and sizes of the chain universes.

## 11. Exact scope of the improvement

- The MSSC direction gives the main new term $-L/(4\ell^3)$, already for greedy.
- The rollout direction gives the general subtraction $\beta(n)-1$ in total mean cost, and the further global term $-\kappa/(2\ell^2)$.
- The leading normalized constant still tends to four.
- The approximation factor still has order $\log n/\log\log n$.
- No constant approximation, fixed leading-constant reduction, or $o(\log n/\log\log n)$ guarantee is claimed.

## 12. Attempting the clarified asymptotic target

The goal here is a ratio

$$
r(n)=o\!\left(\frac{\log n}{\log\log n}\right),
$$

not a vanishing relative correction to a factor of that same order. Quasipolynomial time means $\exp((\log N)^{O(1)})$ in the input length $N$, with a fixed exponent.

### 12.1 Direction A: quasipolynomial-horizon greedy-tail lookahead

This strengthens one-test rollout without implementing it.

Let $G(S)=F_G(S)$, and define Bellman backups

$$
Q_0(S)=G(S),
$$

$$
Q_j(S)=|S|+\min_{\tau\text{ splitting }S}
\sum_a Q_{j-1}(S\cap\tau^{-1}(a))
\quad(j\ge1).
\tag{A1}
$$

All $Q_j$ vanish on empty sets and singletons.

For a fixed horizon $b\ge1$, let $P_b$ be the receding-horizon policy: at every encountered state, choose a test attaining the minimum in $Q_b$, then use this same horizon-$b$ policy in its children. This differs from decrementing the horizon during actual execution.

#### Proposition A: a rigorous tail-sensitive bound

Let $\beta_n$ be any upper bound on greedy's approximation ratio on every subinstance with at most $n$ hypotheses. Let $T^*$ be any complete optimal tree, and let $d^*(h)$ be its leaf depths. Then

$$
\boxed{
C_{P_b}
\le
D+(\beta_n-1)
\frac1n\sum_{h\in H}(d^*(h)-b)_+.}
\tag{A2}
$$

Moreover $C_{P_b}\le C_G$, and the policy can be specified by a computation taking

$$
\operatorname{poly}(n,m,K)(Km)^{b+1}
$$

time. Thus $b=(\log(n+m))^{O(1)}$ gives quasipolynomial time for fixed $K$.

#### Proof

The greedy root test is available in (A1), so $Q_1(S)\le Q_0(S)$. Induction in $j$ gives

$$
Q_j(S)\le Q_{j-1}(S)
$$

for every state.

Let $F_{P_b}(S)$ denote the actual unnormalized policy cost. Induction on $|S|$ gives

$$
F_{P_b}(S)\le Q_b(S).
\tag{A3}
$$

Indeed, if $\tau$ is its selected test, the induction hypothesis and the previous monotonicity give

$$
\begin{aligned}
F_{P_b}(S)
&=|S|+\sum_a F_{P_b}(S_a)\\
&\le |S|+\sum_a Q_b(S_a)\\
&\le |S|+\sum_a Q_{b-1}(S_a)
=Q_b(S).
\end{aligned}
$$

In particular, (A3) and $Q_b\le Q_0$ prove nonregression relative to greedy.

Execute the first $b$ levels of $T^*$ as a competitor in (A1), putting greedy tails on its unfinished leaves. Its prefix cost is

$$
W_b=\sum_h\min\{b,d^*(h)\}.
$$

The unfinished conditional subtrees of an optimal tree are themselves optimal. Their total unnormalized cost is exactly

$$
F(H)-W_b=\sum_h(d^*(h)-b)_+.
$$

The uniform greedy envelope therefore gives

$$
\begin{aligned}
Q_b(H)
&\le W_b+\beta_n(F(H)-W_b)\\
&=F(H)+(\beta_n-1)\sum_h(d^*(h)-b)_+.
\end{aligned}
$$

Use (A3) and divide by $n$ to prove (A2).

A depth-$b$ backup branches into at most $Km$ recursive evaluations per level. It is evaluated at at most $n-1$ actual internal nodes, with polynomial table-processing overhead. This proves the stated running-time bound. $\square$

This proves exactness when an optimal tree has maximum depth at most $b$, and a better ratio whenever the optimum's residual cost beyond depth $b$ is sufficiently small. Those are conditional or restricted-instance consequences, not the requested unrestricted theorem.

#### Why this proof alone does not give an asymptotic improvement

One might hope that a fixed polylogarithmic horizon captures a nonvanishing fraction of the optimal cost on every instance that is hard for greedy. The source paper rules out that shortcut.

Fix any horizon exponent $c>0$, write $L=\log n$, and choose a fixed $a>\max\{c,1\}$. Apply the paper's Proposition 3.3 with $C^*=L^a$. It supplies binary instances satisfying

$$
C_G\ge\frac{L^{a+1}}{16a\log L},
\qquad D\le8L^a.
\tag{A4}
$$

Their information lower bound is $D\ge L$. Combining (A4) with the paper's uniform greedy upper bound,

$$
C_G\le\frac{12DL}{\log D},
$$

gives

$$
D\ge\frac{L^a\log D}{192a\log L}
\ge\frac{L^a}{192a}.
\tag{A5}
$$

Thus $D=\Theta(L^a)$, while

$$
\frac{C_G}{D}
\ge\frac{L}{128a\log L}.
\tag{A6}
$$

These are genuinely same-order greedy-hard instances, not merely high-cost examples on which greedy is already constant-factor.

For every horizon $b=O(L^c)$ and every optimal tree on these instances,

$$
\frac{1}{nD}\sum_h(d^*(h)-b)_+
=1-\frac{W_b}{nD}
\ge1-\frac bD
=1-o(1).
\tag{A7}
$$

Consequently (A2), using only a uniform $\beta_n=\Theta(L/\log L)$ envelope, retains that same asymptotic order.

**Scope:** (A7) is an obstruction to the tail-capture argument, not an approximation lower bound for $P_b$. The actual lookahead may choose much better tests than the particular optimal-prefix-with-greedy-tails competitor used in this proof. Establishing that improvement requires an additional structural lemma that has not been proved here.

Allowing the exponent of $b=(\log n)^{c(n)}$ to tend to infinity avoids this particular fixed-exponent obstruction, but the displayed computation is then not quasipolynomial in the stated fixed-exponent sense. It must not be advertised as such.

### 12.2 Direction B: branching-aware MSSC macros

The strengthened entropy accounting in Sections 3-7 still analyzes the unchanged greedy tree. Since the supplied paper proves its approximation order tight, no refinement of that accounting can prove an $o(L/\log L)$ worst-case ratio for the same rule.

The actual algorithmic direction must select different macros, with their continuation costs included.

For a spine $S_0\supset S_1\supset\cdots\supset S_q$, with exit cells $A_i$, the full conditional objective has the form

$$
\sum_{i=0}^{q-1}|S_i|
+\sum_i F(A_i)+F(S_q).
\tag{B1}
$$

Ordinary MSSC optimizes the first term, not the whole expression. Improving the local MSSC factor four to a different fixed constant, while retaining the same per-level charging argument, changes only a constant in

$$
O\!\left(\frac{L}{\log D}\right).
$$

It does not remove the repeated-scale factor.

A tempting global certificate is the optimal entropy excess

$$
E(S)=F(S)-|S|\log|S|
$$

in the binary case. The following explicit counterexample invalidates the needed restriction inequality.

#### Proposition B: entropy excess is not superadditive over test outcomes

Take four hypotheses $H=\{00,01,10,11\}$, the two coordinate tests, and the binary test asking whether the hypothesis is $11$.

The information lower bound and the coordinate strategy give

$$
F(H)=8,\qquad E(H)=0.
$$

The additional test partitions $H$ into

$$
A=\{00,01,10\},\qquad B=\{11\}.
$$

On $A$, every nonconstant available test isolates one hypothesis; hence

$$
F(A)=3+2=5,\qquad F(B)=0.
$$

Therefore

$$
E(A)+E(B)=5-3\log3>0=E(H).
\tag{B2}
$$

The strict inequality follows from $2^5>3^3$. $\square$

Thus one cannot make (B1) telescope by assuming that the sum of conditional optimal entropy excesses is bounded by the original excess. The partition-entropy term retained in Section 5 is necessary, and its existence is exactly why the earlier refinement did not change the order.

#### The unresolved proof obligation

A qualifying improvement would need a different macro-selection theorem and a global accounting certificate. For example, a computable nonnegative lower bound $\Phi$, zero on singleton states and satisfying $\Phi(H)\le F(H)$, together with macros whose full recursive selection can be charged as

$$
W(P)\le r(n)\left(\Phi(S)-\sum_{A\text{ unfinished}}\Phi(A)\right),
\qquad r(n)=o(L/\log L),
\tag{B3}
$$

would telescope to the desired result. A bounded-overlap global dual certificate would also suffice.

Neither a suitable $\Phi$ nor an oracle with the required guarantee has been constructed in this attempt. Merely asserting (B3), or using exact but unavailable conditional optima, would not be a proof or a quasipolynomial algorithm.

### 12.3 Outcome of the asymptotic attempt

The two proved statements are:

1. The quasipolynomial-horizon tail-sensitive guarantee (A2), together with a precise obstruction to concluding the desired worst-case improvement from that guarantee alone.
2. The explicit failure (B2) of the entropy-excess potential proposed for nonduplicating MSSC accounting.

**This attempt did not obtain an unconditional $o(\log n/\log\log n)$ approximation in polynomial or quasipolynomial time.** This is not an impossibility result for those algorithms. Section 14 records subsequent improvements from a different charging argument at the broadened runtime accepted by the user.

## 13. Next approach: cost-aware coded spines, not depth-only truncation

The next candidate combines two kinds of computation:

1. Quasipolynomial search for a bounded-depth adaptive prefix and for shallow codes on test-outcome classes.
2. A cost-aware stopping/order oracle that can traverse arbitrarily long inspection spines.

This avoids treating a long spine as something that necessarily needs to be enumerated test by test. The computational reduction below is complete; its comparison with unrestricted UDT optimum is not.

### 13.1 The relevant 2025 theorem, and its exact scope

Bansal, Huang, and Zhu, *Optimal 4-Approximation for the Correlated Pandora's Problem*, arXiv:2509.17029v2 / FOCS 2025, Theorem 15, gives a factor-four randomized rounding guarantee for the **partially adaptive** benchmark:

- Fix the order of box inspections before observing outcomes.
- Adapt the stopping decision to the observations.
- Pay inspection costs plus the value of the selected inspected box.

For an explicitly supported distribution and polynomially bounded cost ratios, their convex-program approximation gives a polynomial-time $4+\varepsilon$ guarantee for every fixed $\varepsilon>0$.

Their Section 2.2 explicitly distinguishes this benchmark from the fully adaptive one and states that the latter remains connected to the UDT open question. Therefore this theorem cannot be used as a black-box constant approximation for UDT.

It can, however, price both inspection latency and **fixed certified side-code caps**, rather than latency alone as in ordinary MSSC.

### 13.2 A sound cost-aware spine oracle

Fix a nonsingleton candidate set $S$.

For each test $\tau$ and each nonempty outcome class

$$
A_{\tau,a}=S\cap\tau^{-1}(a),
$$

provide a complete valid identification tree $T_{\tau,a}$ for that class and a certified bound

$$
q_{\tau,a}\ge
\max_{h\in A_{\tau,a}}d_{T_{\tau,a}}(h).
\tag{C1}
$$

Use original tests only in those code trees.

Define a virtual Pandora instance:

- Each ordinary test is a box of inspection cost one.
- In scenario $h$, its box value is

$$
v_\tau(h)=q_{\tau,\tau(h)}.
\tag{C2}
$$

- Include a fallback box of inspection cost $m$ and value zero in every scenario. Its real execution queries all original tests and therefore identifies the hypothesis.
- The scenario distribution is uniform on $S$.

Let $B_{\mathrm{cap}}(S)$ be the minimum expected **charged** objective over partially adaptive policies in this virtual instance.

The benchmark uses caps, not actual conditional average code costs. This distinction is necessary.

#### Proposition C: cost-aware coded-spine lemma

For every $\varepsilon>0$, the above instance yields a valid original-test policy satisfying

$$
\boxed{
\mathbb E[C_{\mathrm{macro}}(S)]
\le(4+\varepsilon)B_{\mathrm{cap}}(S).}
\tag{C3}
$$

When the supplied code trees and their caps are polynomially represented, this oracle has polynomial running time in their representation.

#### Proof

The virtual box value in (C2) is observable without learning the hidden identity: perform $\tau$, observe $a$, and look up the fixed number $q_{\tau,a}$. No extra information is revealed by the reduction.

Run the partially adaptive Pandora approximation. Simulate ordinary inspections by the corresponding original tests. If it stops and selects an inspected ordinary box, execute that box's code tree.

The true hypothesis lies in its original outcome class. Any additional observations may be ignored, or used to skip redundant tests; they do not invalidate the code. Its additional query cost is at most the selected cap by (C1).

If the fallback box is inspected and selected, querying all original tests identifies the hypothesis, with real cost at most its charged inspection cost. Previously queried tests can be reused.

Hence, for every scenario and every realization of the rounding randomness, the real identification cost is no greater than the corresponding virtual charged objective. Applying the verified partially adaptive approximation theorem proves (C3).

All virtual values are determined by original outcomes, and the distribution has $|S|$ explicit scenarios. Codes may always be chosen with depth at most $m$, so the fallback and ordinary inspection costs have ratio at most $m$. The cited convex-program computation consequently has polynomial cost in this setting. $\square$

Every charged policy simulates a feasible UDT policy, while the fallback is always available. Consequently

$$
d(S)\le B_{\mathrm{cap}}(S)\le m.
\tag{C4}
$$

Equation (C3) is an unconditional guarantee for this charged benchmark. It is **not** a factor-four guarantee relative to $d(S)$ or to the best coded policy's actual average cost.

### 13.3 Finding shallow codes without implementing them

The code family can be generated rather than supplied.

Fix a global side-code horizon $h_0$. On every relevant outcome class $A$, search for the smallest feasible maximum depth $j\le h_0$, trying the depth budgets in increasing order.

The exact feasibility recurrence is

$$
\mathsf{Feasible}_j(A)=
\begin{cases}
\mathrm{true},& |A|\le1,\\
\mathrm{false},& |A|>1,\ j=0,\\
\displaystyle\bigvee_{\tau\text{ splitting }A}
\bigwedge_a\mathsf{Feasible}_{j-1}(A\cap\tau^{-1}(a)),
&\text{otherwise}.
\end{cases}
\tag{C5}
$$

It is a mathematical search definition, not an implementation. Its recursive evaluation, including the scan of depth budgets, costs $\operatorname{poly}(n,m,K,h_0)(Km)^{h_0+1}$. A successful search supplies a minimum-height code within the horizon and an honest cap.

If no shallow code exists, use a complete greedy code with its actual maximum depth as the cap. One can retain the smaller certified cap whenever both choices are available.

Thus polylogarithmic $h_0$ gives a quasipolynomially constructible finite-cap oracle. Unlike pure horizon lookahead, the subsequent inspection spine is not limited to $h_0$ tests.

### 13.4 A complete quasipolynomial transfer to a structural benchmark

Use the above code-generation rule consistently at every candidate set. Let $B_{\mathrm{cap}}(A)$ refer to that fixed rule on $A$.

For an adaptive prefix $P$ of depth at most $b$, let $W(P)$ be its unnormalized query cost and let its unfinished leaf sets be $A$. Define

$$
\mathcal B_{b,h_0}(H)=
\min_P\left\{
W(P)+\sum_{A\text{ unfinished}}
|A|B_{\mathrm{cap}}(A)
\right\}.
\tag{C6}
$$

Singleton leaves contribute zero. A prefix is allowed to stop early and use a coded-spine macro.

#### Proposition D: constructive benchmark reduction

For every fixed $\varepsilon>0$, there is a randomized original-test identification policy with

$$
\boxed{
\mathbb E[C_{\mathrm{out}}]
\le(4+\varepsilon)
\frac{\mathcal B_{b,h_0}(H)}{n},}
\tag{C7}
$$

computable in quasipolynomial time when $b$ and $h_0$ are bounded by fixed powers of $\log(n+m)$.

#### Proof

At every candidate set $A$, let $\widehat L(A)$ be a $(1+\eta)$-accurate feasible convex-program objective for its virtual Pandora instance, with $\eta=\varepsilon/4$.

Its lower-bound property and the factor-four rounding theorem give

$$
\widehat L(A)\le(1+\eta)B_{\mathrm{cap}}(A),
\qquad
\mathbb E[C_{\mathrm{rounded}}(A)]
\le4\widehat L(A).
\tag{C8}
$$

Use the unnormalized terminal value $J(A)=|A|\widehat L(A)$ and define

$$
V_0(A)=J(A),
$$

$$
V_j(A)=
\min\left\{
J(A),\
|A|+\min_{\tau\text{ splitting }A}\sum_a V_{j-1}(A_a)
\right\}.
\tag{C9}
$$

All values are zero on singletons.

Choose the minimizing prefix in (C9), then use the rounded coded-spine policy at each unfinished leaf. Induction on $j$ shows that its expected unnormalized cost is at most $4V_j(A)$: terminal rounding costs at most $4J(A)$, while an ordinary prefix query costs

$$
|A|+\sum_a4V_{j-1}(A_a)
\le4\left(|A|+\sum_aV_{j-1}(A_a)\right).
$$

For every competing prefix in (C6), (C8) gives

$$
W(P)+\sum_A J(A)
\le(1+\eta)\left(W(P)+\sum_A|A|B_{\mathrm{cap}}(A)\right).
$$

Therefore

$$
4V_b(H)\le4(1+\eta)\mathcal B_{b,h_0}(H),
$$

which proves (C7).

The prefix evaluation generates at most $(Km)^{b+O(1)}$ recursive states. At each terminal candidate set, shallow-code searches have cost $(Km)^{h_0+O(1)}$ times polynomial overhead, and the convex-program oracle is polynomial. Their product is quasipolynomial for the stated horizons. $\square$

This closes the computational part of a more expressive benchmark. It does not assert that the benchmark approximates unrestricted optimum.

### 13.5 It removes the specific long-gate grid obstruction

Consider the specified $C$-column, $r$-row grid, with $r$ a power of two:

- Column membership tests.
- Binary row-code tests gated to each column.
- Row-only decoys.

Take $h_0\ge\log r$. Every positive column class has a complete row code of depth $\log r$, which (C5) can find.

A competing partially adaptive charged policy opens column membership tests in order until the first positive answer, then selects its row code. Hence

$$
B_{\mathrm{cap}}(H)\le\frac{C+1}{2}+\log r.
\tag{C10}
$$

This statement has no dependence on whether greedy improves on the negative column branch.

For comparison with UDT optimum, give the unknown row to the algorithm for free. Conditional on that row, every available nonconstant test isolates at most one column; row-only tests become constant. Uniform singleton search on $C$ columns has optimal mean

$$
\frac{C+1}{2}-\frac1C\ge\frac C2
\quad(C\ge2).
$$

Also $D\ge\log(Cr)\ge\log r$. Thus

$$
B_{\mathrm{cap}}(H)\le2D+\frac12.
$$

For $C\ge4$, (C3) yields a constant factor at most $9+\varepsilon$, after choosing its accuracy appropriately.

In particular, $C$ may be any fixed power of $\log n$ larger than the prefix horizon. Such long selectors defeated the previous tail-capture proof, but they are not a depth barrier for the coded-spine oracle.

This is a proved structural-family result, not the requested unconditional worst-case improvement.

### 13.6 The remaining global proof obligation

The exact missing statement is a structural bound of the form

$$
\boxed{
\mathcal B_{b,h_0}(H)
\le\rho(n)F(H),
\qquad
\rho(n)=o(\log n/\log\log n),}
\tag{C11}
$$

for fixed polylogarithmic horizons and for the specified computable code family.

If (C11) holds, Proposition D immediately provides the desired quasipolynomial approximation. No further unproved macro oracle is needed.

However, (C11) has not been proved. Nested activation contexts and hard tails inside full test-outcome classes are the main cases still requiring analysis.

In particular, conditional mean code costs cannot be substituted for the caps in (C2).

Here is an explicit reason. Let $r=2^k$. A code has:

- $r^3$ cheap hypotheses, identified by a balanced $3k$-bit code.
- $r$ rare hypotheses, identified by singleton search.
- A root test distinguishing these two groups.

Its unconditional average depth is

$$
1+
\frac{r^3(3k)+r((r+1)/2-1/r)}{r^3+r}
=\Theta(\log r).
$$

If a prior observation identifies the rare group, even after skipping the now-known root test, the conditional remaining average depth is

$$
\frac{r+1}{2}-\frac1r=\Theta(r).
$$

A box value frozen at the original conditional mean therefore does not bound the cost after this history. The discrepancy is unbounded. Worst-case caps avoid this error but make (C11) harder.

This example invalidates that substitution; it does not prove that the full prefix-plus-coded-spine benchmark fails.

### 13.7 Current conclusion

The selected approach is now **cost-aware spine optimization combined with quasipolynomial shallow-code and prefix search**.

The unconditional progress is Proposition C and the constructive transfer Proposition D. The old fixed-depth tail obstruction is bypassed on the grid family, by a proved constant-factor bound.

This coded-spine route has not proved the unrestricted asymptotic target. It would be incorrect to count either the 2025 partially adaptive theorem or the structural-family result as resolving it. The subsequent results below use different arguments and do not assume its outstanding structural inequality.

## 14. Genuine improved tradeoffs from different proof mechanisms

See [the complete new proof](uniform-decision-tree-improved-tradeoffs.md).

The main additional observation is

$$
\text{prefix cost at generation }j
\le\min\{C_{\mathrm{OPT}},(B/2)2^{-j}\}.
$$

Summing this gives a total prefix charge of at most

$$
\left(3+\log_2^+\frac{B}{2C_{\mathrm{OPT}}}\right)C_{\mathrm{OPT}},
$$

rather than charging full OPT at every generation.

Consequences:

- A target factor $c\,\log n/\log\log n$ has a proven quasipolynomial time power approaching $2+4/c$, instead of $2+9/c$ from the supplied curve.
- The near-quasipolynomial coefficient refinement leaves its growing runtime power in the same order. It is **not counted as a qualifying growing-exponent improvement**.
- The certificate $H(H+3)/2\le nC_{\mathrm{OPT}}$ permits complete bounded-height exact search. Combining it with $k$ prefix generations gives ratio $k+4(k+1)/((k+2)\alpha-1)+\varepsilon$ in $2^{O(n^\alpha\log(Km))}$ time. In particular, a 10-approximation has time power arbitrarily close above $5/8$, rather than $9/10$ in the supplied curve.

The next continuation couples active prefixes to terminal optimal costs. If $X_i$ is the conditional-optimal cost mass of terminal states at generation $i$, then a prefix generation costs at most

$$
C_{\mathrm{OPT}}-\sum_{i\le j}X_i.
$$

Making the terminal approximation budget decrease as $R-i$ causes these charges to cancel. The complete generation-dependent proof is in Sections 10-11 of [the improved-tradeoff note](uniform-decision-tree-improved-tradeoffs.md). It strengthens the preceding hybrid:

- Leading curve $(5/\alpha+\varepsilon)$ at power $\alpha$.
- A 10-approximation at every fixed power above $143/288\approx0.496528$.
- An $8+\varepsilon$ approximation at power $495/806$.

The constant-power improvements require the new accounting or exact low-cost routine. They are not merely substitutions into the supplied tradeoff. No polynomial-time constant-factor, strict-quasipolynomial little-$o$, or little-$o$ growing-power improvement is claimed.

## Sources used

1. Ray Li, Percy Liang, and Stephen Mussmann, *A Tight Analysis of Greedy Yields Subexponential Time Approximation for Uniform Decision Tree*, arXiv:1906.11385v2 / SODA 2020. [Local paper](1906.11385v2.pdf), [arXiv](https://arxiv.org/abs/1906.11385v2). The chain/entropy framework above follows the paper, while retaining the additional entropy credit of Lemma 1.
2. Uriel Feige, Laszlo Lovasz, and Prasad Tetali, *Approximating Min-sum Set Cover*, MSR-TR-2003-21 / Algorithmica 2004. [Original technical report](https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/tr-2003-21.pdf). The only MSSC approximation theorem used is its factor-four greedy guarantee.
3. Nikhil Bansal, Zhiyi Huang, and Zixuan Zhu, *Optimal 4-Approximation for the Correlated Pandora's Problem*, arXiv:2509.17029v2 / FOCS 2025. [Primary paper](https://arxiv.org/abs/2509.17029v2). Checked directly: Section 2.2's partially adaptive benchmark; convex-program approximation and computational cost; Theorem 15.
4. Shuchi Chawla, Evangelia Gergatsouli, Jeremy McMahan, and Christos Tzamos, *Approximating Pandora's Box with Correlations*, arXiv:2108.12976v4. [Primary paper](https://arxiv.org/abs/2108.12976v4). The fully adaptive equivalence is not a license to apply a partially adaptive approximation theorem to UDT.

This document supplies the derivation and does not claim an exhaustive novelty check.
