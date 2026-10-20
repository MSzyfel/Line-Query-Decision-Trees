# Uniform Decision Tree: shared lower bounds and an algorithmic route

**Date:** 2026-10-11  
**Scope:** uniform hypotheses, unit-cost deterministic tests, and a constant bound on test arity. All results below are proof-only; no algorithms were implemented.

## Status and main conclusions

The requested general target remains an unconditional

$$
o(\log n/\log\log n)
$$

approximation in genuinely quasipolynomial time. **This note does not prove that target.**

It does establish the following:

1. A compact, global pair-packing lower bound, equivalently a fractional **shared-query cover**. It can be a factor $\Theta(n)$ stronger than the sum of independent fractional identification certificates.
2. A joint conditional-entropy/pair certificate whose resources share the cost of every possible query. Its convex dual is a shared-query cover with entropy demands. The certificates are not restarted at successive size scales.
3. An explicit binary family on which the joint bound is nearly equal to OPT and asymptotically twice the stronger of ordinary entropy and static pair packing. This is a lower-bound improvement, not a new general approximation guarantee.
4. A time-expanded relaxation combining query synchronization, Kraft constraints, conditional entropy, and MSSC completion profiles.
5. A local-policy consistency hierarchy indexed by the number of hypotheses, not by query depth. Its size is quasipolynomial at polylogarithmic levels; it permits arbitrarily long selector spines up to the natural $n-1$ horizon.
6. A concrete certificate-guided code-generation modification. It preserves the greedy guarantee on every instance. Using an explicitly constructed certificate, it gives a $1+O(1/(C+b))$ approximation on the gated $C$-column, $2^b$-row family that defeats the previous cutoff approach.

The last result is a genuine repair of a documented obstruction, but **only for that family**. No good-certificate discovery theorem or improved approximation theorem for arbitrary instances is inferred from it.

The lower bounds are derived here from elementary arguments. Literature-wide priority is not asserted.

**Stronger continuation:** Sections 10--13 identify a full-order gap in the entire static certificate cone of Section 4, even with every subset included. A different, quasipolynomially computable certificate based on sequential/Littlestone dimension removes that gap. Activation-priced coding resources then give a depth-independent composition theorem: a two-approximation for arbitrarily deep factored activation instances with a polylogarithmic-size arbitrary core, and stronger constants for specified cores. These are unconditional structural-class results, not an improved guarantee for arbitrary UDT instances.

**Current scope restriction:** only a worst-case improvement for arbitrary bounded-outcome UDT instances counts. The structural-class algorithms in Sections 11--12 are set aside and do not meet that requirement. The general lower-bound and relaxation-gap proofs remain supporting results, but no improved general approximation ratio has been established.

**Latest explicit geometric question:** the user subsequently asked about points in the plane and a fixed supplied set of side-of-line tests. Section 15 proves a polynomial-time $O(\log n/\log\log n)=o(\log n)$ approximation for the worst-case depth in that model. It does not prove the requested little-$o$ average-cost ratio. Section 14 develops general-instance MSSC-linked greedy rules and complete comparisons to explicit code-menu benchmarks, without identifying those benchmarks with unrestricted UDT OPT.

**Earlier TeX writeup and prior/cost extensions:** [the standalone manuscript](planar-line-decision-trees.tex) records the full worst-case proof and the precursor polynomial-time $O(\log n/\log\log\log n)=o(\log n)$ expected-cost approximation for arbitrary positive hypothesis probabilities and unit-cost supplied lines. That analysis uses heavy verification, a first-light entropy frontier, and merged MSSC/minimum-cover spines. The original algorithm fails for unrestricted test costs; cost-spread-dependent extensions give an $o(\log n)$ expected-cost guarantee when $c_{\max}/c_{\min}=o(\log\log n)$. The next paragraph states the stronger current results.

**Current active geometric results:** [the TeX manuscript](planar-line-decision-trees.tex) now gives constant polynomial-time approximations for unit-cost supplied-line tests: factor 10 for deterministic maximum depth and a factor below 11.53206 for arbitrary-prior expected depth. The maximum-depth proof uses deadline-priority hull greedy, with no optimum-code oracle and no invented queries; Section 17 summarizes its complete argument. The earlier logarithmic average algorithms are not active. Generic cost-independent $O(\log n)$ arbitrary-cost algorithms are not counted as improvements over the general-case literature. Section 16 records the historical partial hull investigation that preceded the completed constant proofs.

## 1. What the literature supplies, and what it does not

### 1.1 Verified primary sources

| Source | Verified ingredient | Relevance and limitation |
|---|---|---|
| Li, Liang, Mussmann, [arXiv:1906.11385v2](https://arxiv.org/abs/1906.11385v2), SODA 2020 | Greedy has ratio $O(\log n/\log D)$, where $D=C_{\mathrm{OPT}}$; its order is tight. The proof balances entropy against level-by-level MSSC lower bounds. | An asymptotic improvement requires changing the algorithm, not merely analyzing unchanged binary greedy more sharply. |
| Golovin, Krause, [arXiv:1003.3967v5](https://arxiv.org/abs/1003.3967v5) | The 2017 correction replaces the original cover theorem by a squared-logarithmic guarantee with additional strong adaptive-submodularity assumptions. Uniform version-space elimination satisfies the required conditions. | The uncorrected logarithmic cover theorem must not be used. |
| Al-Thani, Cui, Nagarajan, [arXiv:2208.08351v2](https://arxiv.org/abs/2208.08351v2) | Theorem 1.5 gives $4(1+\ln(Q/\eta))$ for adaptive-submodular cover. Lemmas 2.5--2.6 compare noncompletion profiles over all time suffixes. | The profile argument is promising for global amortization. Its direct UDT specialization is still logarithmic and uses the same binary greedy split. |
| Navidi, Kambadur, Nagarajan, [arXiv:1606.01530v2](https://arxiv.org/abs/1606.01530v2) | Adaptive submodular ranking combines information and functional-coverage gains additively; the proof uses truncated optimal stems and bad/okay/good states. | The standard binary uniform UDT specialization again chooses the same split as greedy. Arbitrary scenario functions are allowed, but they do not remove the logarithmic losses automatically. |
| Feige, Lovasz, Tetali, [primary MSSC journal manuscript](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf) | Greedy is a four-approximation by price/histogram fitting. The key property is a bound on what any set can cover in a remaining universe. | The comparison is to a fixed set ordering, not to feedback-sensitive continuation trees. |
| Bansal, Batra, Farhadi, Tetali, [arXiv:2007.09172v1](https://arxiv.org/abs/2007.09172v1), SODA 2021 | Time-indexed MSSC LP, four-approximation rounding; strengthened GMSSC LP with knapsack-cover inequalities and a $4.642$ approximation. | The kernel and alpha-point rounding construct one ordering. Independently rounding an ordering for each hypothesis would violate adaptive query consistency. |
| Golovin, Krause, Ray, [arXiv:1010.3091v2](https://arxiv.org/abs/1010.3091v2) | EC2 uses equivalence-class edge cutting with prior-product edge weights. | Its noiseless uniform binary identification score agrees with the usual split rule. Arbitrary pair-packing weights do not inherit adaptive submodularity. |

The classical-adversary equivalence paper [arXiv:1709.08985v3](https://arxiv.org/abs/1709.08985v3) concerns randomized query lower bounds for total functions. It is related background, **not a source establishing the average-identification LP below**. No equivalence with that theorem is assumed.

### 1.2 Why the direct specializations do not improve the bound

At a uniform binary state of size $s$, let a test split it into sizes $a$ and $b$, with $a+b=s$ and $b\le s/2$.

Expected version-space elimination is

$$
s-\frac{a^2+b^2}{s}=\frac{2ab}{s}.
$$

Thus adaptive-cover greedy maximizes $ab$, equivalently $b$.

For adaptive submodular ranking, use the usual scenario objective: the fraction of the other hypotheses eliminated. Its residual denominator is proportional to $s-1$. Up to the common prior normalization, the score is

$$
b+\frac{2ab}{s-1}.
$$

Its derivative as a function of $b\in[0,s/2]$ is

$$
1+\frac{2(s-2b)}{s-1}>0.
$$

It also maximizes $b$.

For EC2 with one equivalence class per hypothesis and equal edge weights, the expected number of newly cut edges is

$$
\binom{s}{2}
-\frac{a\binom{a}{2}+b\binom{b}{2}}s
=ab\left(\frac32-\frac1s\right).
$$

Again the same rule results. These calculations concern binary uniform instances; the equivalences need not hold for larger arity.

Consequently, these off-the-shelf scores cannot beat the known asymptotic lower bound for binary greedy.

### 1.3 The useful analytical import is completion profiles

Write $a(t)$ and $o(t)$ for the noncompletion probabilities of an algorithm and its optimal comparison policy. Expected cost is

$$
C=\int_0^\infty a(t)\,dt.
$$

In Al-Thani--Cui--Nagarajan, with $\Lambda=1+\ln(Q/\eta)$ and $\beta>1$, the suffix score potential satisfies

$$
G_i\le \Lambda a(i),
\qquad
\mathbb E[\operatorname{score}(t,\Psi_t)]
\ge
\frac{a(t)-o(t/(\Lambda\beta))}{t/(\Lambda\beta)}
\quad(t>0).
$$

This is an all-time comparison, rather than a fresh charge of the entire optimum at each mass scale. In adaptive ranking the analogous proof obtains a recurrence of the form

$$
a_k\le0.2a_{k-1}+3x_k.
$$

These are templates for a possible new UDT analysis, not bounds already established for the new scores below.

The higher-moment guarantees in adaptive cover compare against the optimum for the corresponding higher moment. That benchmark cannot silently replace mean-cost OPT.

## 2. Model and accounting

Let $H$ contain $n$ hypotheses and let $\mathcal T$ contain $m$ tests, each with at most $K$ outcomes. Assume that every pair is distinguished by some test.

For a complete tree $T$, write

$$
F_T(H)=\sum_{h\in H}d_T(h),
\qquad
F(H)=\min_T F_T(H)=nD.
$$

Every internal node has a candidate set $S_v$ and a test $\tau_v$. Suppress constant queries, so every internal node has at least two nonempty children. Then

$$
F_T(H)=\sum_{v\text{ internal}}|S_v|,
\qquad
\max_h d_T(h)\le n-1.
\tag{A}
$$

We use $\ln$ for natural logarithms and $\log_2$ for binary logarithms. Set $0\ln0=0$.

The elementary entropy bound is

$$
F(H)\ge n\log_K n.
$$

All subsequent bounds are unnormalized; divide by $n$ to compare them with $D$.

## 3. From independent certificates to shared-query pair packing

### 3.1 Independent fractional certificates

For each $h$, let

$$
c_h=\min\left\{\sum_\tau x_{h\tau}:
x_{h\tau}\ge0,\ 
\sum_{\tau:\tau(h)\ne\tau(g)}x_{h\tau}\ge1
\text{ for every }g\ne h\right\}.
$$

Every root-to-$h$ path supplies a feasible integral certificate. Therefore

$$
\sum_h c_h\le F(H).
\tag{B}
$$

This misses the difficulty of finding the right certificate adaptively: a hypothesis may have a one-test certificate that the algorithm does not know to ask.

### 3.2 A global pair-packing LP

Assign a nonnegative weight $w_{uv}$ to each unordered pair. Require

$$
\sum_{\substack{\{u,v\}\subseteq S\\ \tau(u)\ne\tau(v)}}w_{uv}
\le |S|
\quad
\text{for every }S\subseteq H,\ \tau\in\mathcal T.
\tag{P}
$$

Let $P(H)$ be the maximum total pair weight subject to (P).

**Theorem 1.**

$$
P(H)\le F(H).
$$

**Proof.** Charge each pair at the node where its two hypotheses first obtain different outcomes. Each pair is charged exactly once. At a node with candidate set $S$ and test $\tau$, (P) bounds the charged weight by $|S|$. Sum over the tree and use (A). $\square$

#### Compact representation

For each test $\tau$ and each pair it separates, introduce endpoint assignments

$$
f^\tau_{uv,u},f^\tau_{uv,v}\ge0,
\qquad
f^\tau_{uv,u}+f^\tau_{uv,v}=w_{uv}.
$$

Require

$$
\sum_{v:\tau(v)\ne\tau(u)}f^\tau_{uv,u}\le1
\quad\text{for every }u,\tau.
\tag{O}
$$

These constraints are equivalent to (P), not merely sufficient.

To see the nontrivial direction, for a fixed test create a source node for every separated edge, of supply $w_{uv}$, and route its supply to its two endpoints, each of capacity one. The max-flow condition is precisely that every collection of edges has total supply at most the capacity of its incident vertices. The induced-subgraph inequalities (P) imply that condition. Conversely, summing endpoint assignments over any induced subgraph proves (P).

Thus $P(H)$ is an ordinary polynomial-size LP with $O(mn^2)$ variables. Assignments may differ between tests, but are fixed globally, not chosen separately at each candidate state.

#### Equivalent fractional shared-query cover

The compact LP dual is

$$
\begin{aligned}
\min\quad&\sum_{h,\tau}\mu_{h\tau}\\
\text{subject to}\quad&
\mu_{h\tau}\ge0,\\
&\sum_{\tau:\tau(u)\ne\tau(v)}
\min(\mu_{u\tau},\mu_{v\tau})\ge1
\quad\text{for every }\{u,v\}.
\end{aligned}
\tag{SC}
$$

The minimum terms are linearized by variables $r_{uv,\tau}\le\mu_{u\tau},\mu_{v\tau}$ and $\sum_{\tau\text{ separating }u,v}r_{uv,\tau}\ge1$.

Unlike independent certificates, a pair must be covered by **common query mass**. A real tree satisfies (SC): its separating test is queried by both hypotheses before they diverge.

Another, exponential-size dual is a fractional cover of pairs by restricted cuts $(S,\tau)$, each of cost $|S|$. Actual tree cuts form a compatible laminar family; arbitrary fractional restricted cuts need not.

### 3.3 Domination of independent certificates

Let $\xi_{hg}$ be feasible dual weights for the certificate LP of $h$, so

$$
\sum_{g:\tau(g)\ne\tau(h)}\xi_{hg}\le1.
$$

Set $w_{hg}=\xi_{hg}+\xi_{gh}$ and, for every separating test, assign $\xi_{hg}$ to $h$ and $\xi_{gh}$ to $g$. This is feasible in (O). Hence

$$
P(H)\ge\sum_h c_h.
$$

### 3.4 Two exact examples

**Singleton search.** Give the $n$ tests $\mathbf1_{\{h\}}$, one per hypothesis. Then

$$
\sum_h c_h=n,\qquad
P(H)=\frac{n^2}{2},\qquad
F(H)=\frac{n(n+1)}2-1.
\tag{S}
$$

For the pair upper bound, sum (P) at $S=H$ over all singleton tests; each pair is counted twice. For feasibility, put $w_{uv}=n/(n-1)$. In a singleton-test star, assign one unit of each edge to the outside endpoint and the remaining $1/(n-1)$ to the center. The center receives total one.

The tree cost follows from $F(n)=n+F(n-1)$ and $F(1)=0$. Thus pair packing is a factor $\Theta(n)$ stronger than independent fractional certificates.

**All parity tests.** Let $H=\mathbb F_2^a$, $n=2^a$, and give every nonzero linear parity test. Every distinct pair is separated by $n/2$ of the $n-1$ tests. Consequently

$$
P(H)=2(n-1),\qquad F(H)=na.
\tag{L}
$$

The upper bound sums (P) at $H$ over all tests. Uniform pair weights $4/n$ are feasible because a test cuts at most $|S|^2/4$ pairs inside $S$, and $|S|\le n$. Entropy and the $a$ coordinate tests prove the exact optimum.

Static shared-query cover alone therefore has a $\Theta(\log n)$ integrality gap. It needs an information resource as well as pair synchronization.

## 4. Conditional entropy and pairs with one shared budget

### 4.1 The certificate

Choose any explicitly listed family $\mathcal A$ of subsets of $H$, of size at least two. They may overlap.

For each $A\in\mathcal A$ choose $\theta_A\ge0$. For every test $\tau$ and every outcome occurring on $A$, choose a nonnegative length $\ell_{A,\tau,a}$ satisfying

$$
\sum_{a\in\tau(A)}
\exp(-\ell_{A,\tau,a}/\theta_A)\le1
\quad(\theta_A>0).
\tag{C}
$$

At $\theta_A=0$ use the closed perspective extension; choosing all its lengths zero is allowed. Equivalently, for positive $\theta_A$, these are scaled negative logarithms of subnormalized outcome-prediction probabilities.

Choose pair weights and endpoint assignments as in Section 3, but replace (O) by the **shared** constraint

$$
\sum_{\substack{A\in\mathcal A\\h\in A}}
\ell_{A,\tau,\tau(h)}
+\sum_{g:\tau(g)\ne\tau(h)}f^\tau_{hg,h}
\le1
\quad\text{for every }h,\tau.
\tag{J}
$$

The code lengths are fixed per resource and test. Allowing unrelated predictions at every state would not prove the global certificate below.

### 4.2 A state potential valid for every tree

Define

$$
\Phi(S)=
\sum_{A\in\mathcal A}\theta_A|S\cap A|\ln|S\cap A|
+\sum_{\{u,v\}\subseteq S}w_{uv}.
\tag{V}
$$

For a test partition $S=\bigsqcup_a S_a$, let

$$
g_\Phi(S,\tau)=\Phi(S)-\sum_a\Phi(S_a).
$$

**Theorem 2.** Every feasible certificate satisfies

$$
0\le g_\Phi(S,\tau)\le |S|
\quad\text{for every }S,\tau,
\qquad
\boxed{\Phi(H)\le F(H).}
\tag{LB}
$$

**Proof.** For one resource, put $s_a=|A\cap S_a|$, $s=\sum_a s_a$. Its decrement is

$$
\theta_A\left(s\ln s-\sum_a s_a\ln s_a\right).
$$

It is nonnegative. The entropy/cross-entropy inequality and (C) give

$$
\theta_A\left(s\ln s-\sum_a s_a\ln s_a\right)
\le\sum_a s_a\ell_{A,\tau,a}.
$$

The pair decrement is exactly the weight of separated pairs inside $S$. Assign that weight to its endpoints and sum (J) over $h\in S$. The combined decrement is at most $|S|$.

On a complete tree, decrements telescope to $\Phi(H)$; a singleton or empty set has potential zero. Equation (A) proves the lower bound. $\square$

This proof works for overlapping entropy resources: their query costs are added **before** the unit capacity is enforced. It does not add unrelated valid lower bounds after the fact.

### 4.3 Endpoints and computational size

With all entropy resources zero, this is pair packing. If $\mathcal A$ contains $H$, choosing

$$
\theta_H=1/\ln K,\qquad \ell_{H,\tau,a}=1,\qquad w=0
$$

recovers ordinary entropy; fewer than $K$ nonempty outcomes only make (C) easier.

The program maximizing $\Phi(H)$ is convex: (C) is the perspective-log-sum-exp constraint

$$
\theta_A\ln\!\left(\sum_a e^{-\ell_{A,\tau,a}/\theta_A}\right)\le0.
$$

All remaining constraints are linear. It has $O(mn^2+|\mathcal A|mK)$ variables. For each nontrivial $A$, separability supplies a test with at least two outcomes on $A$; (J) bounds its lengths by one and hence bounds $\theta_A\le1/\ln2$. The objective is bounded by $F(H)\le n(n-1)$.

Standard weak convex optimization applies to finite families and finite precision. There is no claim of an exact finite-bit solution to transcendental equations. In particular, a family generated by polylogarithmic test histories has quasipolynomial explicit size; an arbitrary exponentially listed family is not a free oracle.

### 4.4 Equivalent entropy-constrained shared-query cover

The dual makes the association with a different optimization problem particularly explicit.

For $\mu_{h\tau}\ge0$, define

$$
M_{A,\tau,a}=\sum_{\substack{h\in A\\\tau(h)=a}}\mu_{h\tau},
\qquad
M_{A,\tau}=\sum_a M_{A,\tau,a},
$$

and

$$
\mathcal I_A(\mu)=
\sum_\tau
\left(
M_{A,\tau}\ln M_{A,\tau}
-\sum_a M_{A,\tau,a}\ln M_{A,\tau,a}
\right).
\tag{I}
$$

Let $L_{\mathcal A}(H)$ be the optimum of

$$
\begin{aligned}
\min\quad&\sum_{h,\tau}\mu_{h\tau}\\
\text{subject to}\quad&
\sum_{\tau:\tau(u)\ne\tau(v)}
\min(\mu_{u\tau},\mu_{v\tau})\ge1
&&\text{for every pair},\\
&\mathcal I_A(\mu)\ge |A|\ln|A|
&&\text{for every }A\in\mathcal A.
\end{aligned}
\tag{EC}
$$

**Theorem 3.** (EC) has the same optimum as the joint certificate program, and

$$
L_{\mathcal A}(H)\le F(H).
$$

**Dual derivation.** Attach multipliers $\mu_{h\tau}\ge0$ to (J). For a pair of weight $w$, the cheapest endpoint assignment at test $\tau$ costs $w\min(\mu_{u\tau},\mu_{v\tau})$. Boundedness gives exactly the shared-query pair constraints.

For a resource $A$ and fixed positive $\theta_A$, the minimum weighted length cost is

$$
\theta_A\mathcal I_A(\mu).
$$

Indeed the minimizing prediction at each test is proportional to the outcome weights $M_{A,\tau,a}$; the minimum weighted cross-entropy is their mass times their entropy. Zero masses are handled by a limit. Since $\theta_A$ can be scaled, boundedness requires $\mathcal I_A(\mu)\ge |A|\ln|A|$. The remaining dual objective is $\sum_{h,\tau}\mu_{h\tau}$.

Finite-family strong duality holds: choose all positive resource parameters sufficiently small, lengths strictly inside their code cones, and sufficiently small positive pair weights. Then every query capacity is strict, relative to the orientation equalities. The primal optimum is finite by Theorem 2.

**Direct lower-bound proof.** In a real tree, let $\mu_{h\tau}$ count queries of $\tau$ on the path of $h$. Pair constraints hold at first separation. To verify an entropy demand, restrict node populations to $A$. Entropy decrements telescope:

$$
\sum_v\left(
|A\cap S_v|\ln|A\cap S_v|
-\sum_a|A\cap S_{v,a}|\ln|A\cap S_{v,a}|
\right)
=|A|\ln|A|.
$$

Group nodes using the same test. The mass-entropy function

$$
(z_a)_a\longmapsto
\left(\sum_a z_a\right)\ln\left(\sum_a z_a\right)
-\sum_a z_a\ln z_a
$$

is concave and homogeneous, hence superadditive. Aggregating the node populations for one test can only increase their total mass-entropy. This gives (I). Thus every actual tree supplies a feasible solution of cost $F_T(H)$. $\square$

The entropy constraints in (EC) are convex superlevel constraints of concave functions. They can also be viewed as infinitely many linear code-length inequalities, with efficient separation by the weighted outcome distributions.

The main relaxation gap is now identifiable: common **total** query mass need not admit compatible query histories.

### 4.5 A genuine submodular macro objective, but not adaptive submodularity

For a fixed set of tests $Q$, partition $S$ by their joint outcomes and define

$$
\Gamma(S,Q)=\Phi(S)-\sum_{\text{joint-outcome cells }R}\Phi(R).
$$

As a function of $Q$, $\Gamma$ is monotone submodular:

- The pair part is weighted set coverage of the pairs distinguished by at least one test in $Q$.
- For each entropy resource, it is $\theta_A|A\cap S|$ times the entropy of the joint outcomes on the uniform distribution on $A\cap S$. Joint entropy is submodular.

Thus fixed-macro selection is associated with ordinary submodular maximization/coverage, with both information and pair gains in the same objective.

This does **not** imply adaptive submodularity. For example, an indicator of one hypothesis has outcome entropy $H_2(1/4)$ on four hypotheses but entropy one after conditioning to a two-hypothesis set containing it.

Nor do arbitrary EC2 edge weights preserve its property. Give weight one only to edge $\{u,v\}$ on $\{u,v,w,x\}$. A test with positive outcome $\{x\}$ eliminates this edge with probability $1/4$. After a negative singleton test for $w$, that probability increases to $1/3$. Additional singleton tests can make the instance identifying. Therefore the adaptive-cover theorem cannot be invoked for arbitrary optimized pair weights.

## 5. A separating family: the joint bound is nearly exact

Let

$$
H=[r]\times\mathbb F_2^a,\qquad B=2^a,\qquad n=rB.
$$

Give the $r$ group-membership tests and all $B-1$ nonzero parity tests on the second coordinate, ungated.

### 5.1 Exact optimum and pair bound

On each fixed group, coding the second coordinate costs at least $a$ on average. On each fixed second coordinate, group identification is singleton search. Since these two kinds of queries are disjoint,

$$
F(H)=n\left(a+\frac{r+1}{2}-\frac1r\right).
\tag{OPT}
$$

A coordinate code followed by singleton group search achieves equality.

The static pair optimum is exactly

$$
P(H)=n\left(\frac r2+2-\frac2B\right).
\tag{PP}
$$

For the upper bound, split pairs into those with equal second coordinate and those with different second coordinates. Summing the group-test capacities bounds the former by $nr/2$. Every pair of the latter kind is separated by $B/2$ parity tests, so summing parity-test capacities bounds their total by $2n(1-1/B)$.

For feasibility:

- Give pairs with the same second coordinate and different groups weight $r/(r-1)$.
- Within a group, give every different-second-coordinate pair weight $4/B$.
- Give the other pairs weight zero.

Group tests see disjoint stars, with the endpoint assignments from (S). Parity tests see only the within-group balanced cuts; assigning half of each incident edge to each endpoint gives load one. This proves equality.

### 5.2 Joint allocation

Use entropy resources

$$
A_i=\{i\}\times\mathbb F_2^a,\qquad \theta_{A_i}=1/\ln2.
$$

For a nonzero parity test put length one in every resource. For a group test put length zero: it is constant on each resource.

Retain only the same-second-coordinate pair weights $r/(r-1)$. Parity tests separate none of them, while group tests spend no entropy budget. The constraints are feasible and give

$$
\Phi(H)=n\left(a+\frac r2\right).
\tag{JO}
$$

For the family consisting just of the $A_i$, this is the **exact** joint-program value. A matching solution of (EC) assigns:

- $\mu_{h\tau}=1/2$ for every group test and every hypothesis;
- $\mu_{h\tau}=1$ for the $a$ coordinate parity tests;
- zero to the other parity tests.

Different second coordinates share a separating coordinate query. Equal second coordinates in two different groups share two separating group queries of mass $1/2$ each. Every resource receives exactly $Ba\ln2=B\ln B$ entropy. Total cost is (JO).

One may add $H$ as another resource, recovering the ordinary entropy endpoint as well; the optimum can only increase and is still bounded by (OPT).

### 5.3 Quantified separation

Set $r=2a$. Ordinary entropy, pair packing, and the joint lower bound are respectively

$$
E(H)=n(a+\log_2(2a)),\qquad
P(H)=n(a+2-2^{1-a}),\qquad
\Phi(H)=2an.
$$

For sufficiently large $a$, $E(H)\ge P(H)$, and

$$
\frac{\Phi(H)}{\max\{E(H),P(H)\}}
=\frac{2a}{a+\log_2(2a)}
\longrightarrow2.
$$

Meanwhile

$$
\frac{F(H)}{\Phi(H)}
=1+\frac{1/2-1/(2a)}{2a}
=1+O(1/a).
$$

For the explicit choice $a=8,r=16$, there are $4096$ hypotheses and $271$ binary tests:

$$
E=12n,\quad P=(10-1/128)n,\quad
\Phi=16n,\quad F=(16+7/16)n.
$$

The joint certificate is at least $4/3$ times the stronger endpoint.

**Interpretation.** This exhibits two genuinely different cost sources and a valid way to combine them. It does not establish a new approximation ratio. The factor-two separation in this example is a constant-factor strengthening of a lower bound, not the asymptotic approximation improvement requested by the user.

## 6. A time-expanded relaxation with completion-profile demands

### 6.1 Pairwise synchronization over time

Let $T=n-1$ and $t=0,\ldots,T-1$. Introduce:

- $y_{h,t}$: alive mass before query number $t+1$;
- $x_{h,\tau,t}$: mass that queries $\tau$ at that time;
- $z_{uv,t}$: mass in which a pair is still together;
- $a_{uv,\tau,t}$: common query mass for that pair.

Impose nonnegativity, $0\le y,z\le1$, and

$$
y_{h,0}=1,\quad y_{h,T}=0,\quad
y_{h,t+1}\le y_{h,t},\quad
\sum_\tau x_{h,\tau,t}=y_{h,t},
$$

$$
z_{uv,0}=1,\quad z_{uv,T}=0,\quad
a_{uv,\tau,t}\le x_{u,\tau,t},x_{v,\tau,t},
$$

$$
\sum_\tau a_{uv,\tau,t}=z_{uv,t},
\qquad
z_{uv,t+1}=\sum_{\tau:\tau(u)=\tau(v)}a_{uv,\tau,t}.
\tag{TS}
$$

Minimize

$$
\sum_h\sum_{t=0}^{T-1}y_{h,t}.
\tag{TC}
$$

Every actual tree supplies an integral feasible point. At each time a pair is either together and queries the same test, or already separated.

Useful valid triangle inequalities are

$$
z_{uv,t}+y_{w,t}\ge z_{uw,t}+z_{wv,t}
$$

for distinct $u,v,w$. They express the consistency of same-node events, but pairwise constraints and triangles alone are not a full policy distribution.

The LP has $O(mn^3)$ variables.

### 6.2 Kraft and entropy strengthen different aspects

Set $p_{h,d}=y_{h,d-1}-y_{h,d}$ for $d=1,\ldots,T$. Add

$$
\sum_h\sum_{d=1}^T K^{-d}p_{h,d}\le1.
\tag{K}
$$

This is valid by Kraft's inequality. Since $\sum_d p_{h,d}=1$, Jensen's inequality gives

$$
nK^{-(\sum_{h,t}y_{h,t})/n}\le1.
$$

Thus the objective is at least $n\log_K n$, but (K) also constrains the completion profile, not just its mean.

Pairwise synchronization without (K) is insufficient even on the parity family. For $n=2^a\ge8$, set $y_{h,0}=y_{h,1}=1$ and $y_{h,t}=0$ thereafter. Query uniformly among the $n-1$ parities at both times. After the first query each pair has

$$
z_{uv,1}=\frac{n/2-1}{n-1}.
$$

At the second time, give that pair common mass $z_{uv,1}/(n/2)$ on each separating parity and zero on the others. This is at most the available $1/(n-1)$ query mass, and resolves every pair. It satisfies (TS) and the triangles, at cost $2n$, although OPT is $n\log_2 n$. The Kraft constraint rules it out.

For conditional entropy, aggregate

$$
\mu_{h\tau}=\sum_t x_{h,\tau,t}
$$

and add the demands $\mathcal I_A(\mu)\ge |A|\ln|A|$ from (EC). These are convex constraints, not linear ones. Equivalently, use their separated linear code-length inequalities. There is no bilinear optimization over unfixed predictors and query masses.

Any feasible (TS) point has

$$
\sum_{t,\tau:\tau(u)\ne\tau(v)}a_{uv,\tau,t}=1.
$$

The aggregate common masses are bounded by both endpoint query totals. Hence $\mu$ satisfies shared-query cover, and the strengthened objective is at least $L_{\mathcal A}(H)$. This integrates the joint certificate into a time/profile relaxation.

### 6.3 Valid MSSC demands

For a subset $A$, freeze an outcome $c_\tau$ for each test, for example its largest outcome on $A$. Form sets

$$
B_\tau=A\setminus\tau^{-1}(c_\tau)
$$

and add one analytical singleton set per hypothesis of $A$.

Let $M_A$ be the optimum of the ordinary time-indexed MSSC LP on these sets, with capacity one set per time and constraints

$$
u_{h,t}+\sum_{t'<t,\ j:h\in B_j}X_{j,t'}\ge1.
\tag{MC}
$$

The singleton sets are only a lower-bound device; they are not new UDT tests.

For every complete tree,

$$
M_A-1\le \sum_{h\in A}d_T(h).
\tag{MD}
$$

**Proof.** Follow the frozen-outcome path through the tree. Each hypothesis that exits is covered by the test at its first exit, no later than its own depth. If one hypothesis survives to a leaf, cover it with its analytical singleton at the next time. This adds at most one to total cover time. Remove steps covering no new member of $A$; this can only improve the cover times. Apply the MSSC LP lower bound. $\square$

For a finite family of such demands, one valid scalar aggregation is

$$
\max_{\lambda_A\ge0}
\left\{\sum_A\lambda_A\max(0,M_A-1):
\sum_{A\ni h}\lambda_A\le1\ \forall h\right\}
\le F(H).
\tag{MP}
$$

This explicitly prevents repeatedly charging the same hypothesis at nested scales.

A stronger profile coupling keeps the MSSC variables themselves. Use times $t=1,\ldots,n$, put $u_{A,h,1}=1$ and $u_{A,h,n+1}=0$, and add nonnegative exception variables satisfying

$$
u_{A,h,t}\le y_{h,t-1}+e_{A,h,t},
\qquad
\sum_{h\in A,t}e_{A,h,t}\le1.
\tag{PF}
$$

Keep (MC), one set per time, and monotone uncovered variables. Original tests and analytical singleton sets are the available MSSC sets.

Every tree supplies a valid point: first cover time is at most depth, except possibly for the one final singleton, which may be one time later. Thus only one unit of exception mass is necessary. The same $y$ variables are used by all demands. Their costs are not independently added to the objective.

These constraints capture noncompletion profiles and imply (MD). They provide a concrete way to import MSSC time-indexed machinery without pretending that a rounded fixed ordering is already an adaptive tree.

## 7. Local-policy consistency on small hypothesis sets

Pair synchronization can couple different pairs to incompatible query histories. A stronger, still explicit hierarchy addresses that issue.

### 7.1 Local flows

For every $U\subseteq H$ with $1\le |U|\le q$, introduce a policy flow over

$$
(S,t),\qquad \varnothing\ne S\subseteq U,\quad 0\le t\le T.
$$

Let $r^U_{S,t}$ be arrival mass, $p^U_{S,\tau,t}$ query mass, and $e^U_{S,t}$ stopping mass. Require:

$$
r^U_{U,0}=1,\quad r^U_{S,0}=0\ (S\ne U),
$$

$$
r^U_{S,t}=\sum_\tau p^U_{S,\tau,t}+e^U_{S,t}
\quad(t<T),
\qquad e^U_{S,t}=0\quad(|S|>1),
$$

$$
r^U_{R,t+1}
=
\sum_{\substack{S,\tau,a\\S\cap\tau^{-1}(a)=R}}
p^U_{S,\tau,t}.
\tag{FL}
$$

At time $T$, permit only singleton stopping: $r^U_{S,T}=e^U_{S,T}$ and $e^U_{S,T}=0$ for $|S|>1$.

Queries constant on $S$ are allowed and move the flow from $(S,t)$ to $(S,t+1)$. Even a singleton may continue querying before it stops. This is necessary to project a global tree whose local restriction has already identified its hypothesis but whose global path is not finished.

Synchronize these flows with the global marginals:

$$
x_{h,\tau,t}
=\sum_{S\subseteq U:h\in S}p^U_{S,\tau,t}
\quad(h\in U),
$$

$$
z_{uv,t}
=\sum_{S\subseteq U:\{u,v\}\subseteq S}r^U_{S,t},
\qquad
a_{uv,\tau,t}
=\sum_{S\subseteq U:\{u,v\}\subseteq S}p^U_{S,\tau,t}.
\tag{PR}
$$

The alive variables already satisfy $y_{h,t}=\sum_\tau x_{h,\tau,t}$. Arrival mass includes a leaf that stops at time $t$; query mass excludes it. This distinction avoids an off-by-one completion error.

### 7.2 Validity, size, and exactness at the top level

**Theorem 4.** Adding (FL)--(PR) for all $U$ of size at most $q$ gives a valid lower-bound hierarchy. It can be combined with the Kraft, entropy, and MSSC profile constraints above.

**Proof of validity.** Intersect every global node population with $U$, omitting empty intersections. A global query can become a constant local query, which is permitted. Stop only at the original global leaves. This defines a local flow with exactly the required global query and pair marginals. $\square$

There are at most

$$
\sum_{j=1}^q\binom nj 2^j mT
=n^{O(q)}mT
$$

local variables, and a comparable number of linear constraints. For fixed-power polylogarithmic $q$, this is genuine quasipolynomial size. **The exponent depends on the number of sampled hypotheses, not on the length of an arbitrary selector spine.**

At $q=n$, the full-set flow is exact. To see this, randomize independently at each reachable $(S,t)$ according to its query/stopping proportions. Flow conservation reproduces the prescribed node marginals. Every realized policy stops only at singletons by time $T$. Its expected cost is

$$
\sum_{S,t}|S|\sum_\tau p^H_{S,\tau,t}
=\sum_{h,t}y_{h,t}.
$$

Each realized policy has cost at least $F(H)$, while an optimum tree is feasible. Thus the optimum equals $F(H)$. Constant queries do not change the optimum because they can be suppressed.

This top-level statement is another formulation of exponential exact optimization, not a faster exact algorithm. At quasipolynomial levels, no small integrality gap or rounding theorem is proved.

The important distinction from bounded-query-prefix search is that local flows retain the entire time horizon. Long majority spines are not simply truncated.

## 8. A concrete algorithm modification and a proved obstruction repair

### 8.1 Certificate-guided state generation

Given an explicitly obtained feasible potential $\Phi$, perform the following proof-level construction:

1. Build a complete tree $T_\Phi$ by choosing a splitting test maximizing $g_\Phi(S,\tau)$ at each state. On ties prefer the larger binary minority; if the potential gives no progress, a splitting test still exists.
2. At every node state of $T_\Phi$, probe all test histories of depth at most $q$, with complete greedy continuations. Retain the complete codes produced.
3. Also retain the complete greedy tree on $H$.
4. Retain all node states of these codes and recombine exactly on the resulting supported-state DAG.

The probe cost is given by

$$
R_0(S)=F_G(S),
\qquad
R_j(S)=
\min\left\{
F_G(S),\ 
|S|+\min_{\tau\text{ splitting }S}\sum_aR_{j-1}(S_a)
\right\}.
$$

A probe takes $(nmK)^{O(q+1)}$ time. There are at most $2n-1$ nodes in $T_\Phi$.

For represented states, recombination uses

$$
J(S)=|S|+
\min_{\tau:\text{splitting, all nonempty children represented}}\sum_aJ(S_a),
$$

with zero cost at singletons. Strict size decrease makes this an acyclic exact computation.

**Theorem 5.** The construction takes

$$
\operatorname{poly}(|\mathcal A|,n,m)\,(nmK)^{O(q+1)}
$$

time, apart from the chosen finite-precision certificate computation, and its output is no worse than greedy. It also compares exactly against every complete tree assembled from its represented states.

**Proof.** A proper candidate tree has at most $n-1$ internal nodes. The retained family has at most a polynomial factor times the total probe size. Recombination is polynomial in that family. The greedy tree is a supported competitor. $\square$

The unconditional time/nonregression claims do not require an exact transcendental gain comparison: any explicitly evaluated approximate candidate policy can be used. For the grid proof below, inverse-polynomial-accuracy evaluations suffice because all relevant strict comparisons have constant additive separation. Exact ties can be handled by a small tie window and the minority rule.

This is code generation, not an assumption that a continuation-pricing oracle exists. It is related to the retained-state construction in [the earlier tradeoff note](uniform-decision-tree-improved-tradeoffs.md), but generates states from a global lower-bound potential rather than only from bounded-depth probes of the incumbent.

### 8.2 The gated-grid family

Let

$$
H=[C]\times\{0,1\}^b,\qquad r=2^b,\qquad n=Cr,
$$

with $C\ge16$ and $r\ge C$. Give:

- Each column-membership test.
- Each row-coordinate bit gated to one column.
- Common row-decoy tests: their outcomes depend only on the row, and their positive row sets have size at most $2r/C$.

This includes the recursive decoys in Section 13 of [the tradeoff note](uniform-decision-tree-improved-tradeoffs.md): a row node of size $s$ has small child $1+\lfloor s/C\rfloor$.

For $C=\lceil b^\gamma\rceil$ with any fixed $\gamma>1$, that recursive construction makes greedy cost

$$
\Omega(Cb/\log C),
$$

while a column-first tree costs $O(C+b)$. Its greedy ratio is $\Omega(\log n/\log\log n)$.

### 8.3 Explicit feasible certificate

Take the column entropy resources

$$
A_i=\{i\}\times\{0,1\}^b,\qquad \theta_{A_i}=1/\ln2.
$$

For a test nonconstant on a resource give both outcomes length one; for a constant test give its sole outcome length zero.

Give weight one to each pair in different columns but the same row, and zero to other pairs. Then

$$
\Phi(S)=
\sum_i|S\cap A_i|\log_2|S\cap A_i|
+\#\{\text{same-row, different-column pairs inside }S\}.
\tag{GV}
$$

Feasibility is explicit:

- A common row test separates no positive-weight pair and spends at most one entropy unit per hypothesis.
- A column-membership test spends no entropy. Assign every separated same-row pair to its endpoint outside that column; each outside endpoint has just one such edge.
- A gated bit spends an entropy unit in its active column and zero outside. Assign its separated pairs wholly to the outside endpoints, again at most one per endpoint.

Thus Theorem 2 applies, and

$$
F(H)\ge\Phi(H)
=n\left(b+\frac{C-1}{2}\right).
\tag{GL}
$$

This is a constructed feasible point, not a claim that an arbitrary optimizer of the joint program must return this same potential.

### 8.4 Why the new score finds a long selector spine

Suppose the current state consists of all $r$ rows in $k$ full columns. Then:

- Column membership has gain $r(k-1)$.
- A gated coordinate bit has entropy gain $r$ and pair gain $r(k-1)/2$, hence total $r(k+1)/2$.
- A common row decoy of fraction $p$ has gain $krH_2(p)$ and zero pair gain.

Here $p\le2/C$, and

$$
H_2(p)\le H_2(1/8)<2/3.
$$

For every $k\ge3$, column membership beats every decoy and is at least as good as every gated bit. At $k=3$ the gated-bit tie is broken by the larger minority of column membership.

Therefore $T_\Phi$ has an all-negative selector spine until two full columns remain. Every positive exit is a full single column.

This contrasts with ordinary greedy, which selects the row decoys at the large row states.

### 8.5 A quasipolynomial, nearly optimal repair on this family

**Theorem 6.** Run the construction of Section 8.1 with the explicit potential (GV) and $q\ge b+1$. Its output on this family satisfies

$$
\frac{C_{\mathrm{out}}}{D}
\le
\frac{b+(C+1)/2-1/C}{b+(C-1)/2}
=
1+\frac{1-1/C}{b+(C-1)/2}.
\tag{GR}
$$

**Proof.** The selector-spine states and their positive single-column exits are represented. A depth-$q$ probe at each single-column exit contains a complete $b$-bit code of cost $rb$. At the final two-column state, a probe contains one column query followed by those codes, of cost $2r(b+1)$.

Recombine the existing selector spine with these probe codes. Its cost is at most the column-first cost

$$
r\left(Cb+\sum_{k=2}^C k\right)
=n\left(b+\frac{C+1}{2}-\frac1C\right).
$$

Use (GL) for the denominator. $\square$

Choosing $q=\lceil\log_2 n\rceil$ works. With an explicit polynomial-size test matrix, the time is $\exp(O((\log N)^2))$, where $N$ is input size.

The selector spine may have $C-2$ queries, much more than $q$. It is discovered by the certificate-guided policy, not enumerated as a depth-$C$ prefix. Only the side codes need logarithmic-depth probing.

This is an unconditional theorem for the specified family and specified explicit certificate. It is **not** a general UDT approximation theorem, and does not solve the user's worst-case target.

## 9. Implications for the original two-scheme balance

The supplied analysis charges:

1. Balanced queries to total entropy.
2. Imbalanced chains to MSSC optima, with a separate global-OPT comparison at each minority-size level.

The second charge can repeat the same useful selector at many levels. The gated grid demonstrates why the resulting logarithmic number of levels is not merely a loose analysis of unchanged greedy.

The new schemes change the available accounting:

- Shared-query cover records that two hypotheses need common distinguishing query mass.
- Conditional entropy accounts for coding within subsets without forcing every coding cost into global entropy.
- Joint endpoint capacities prevent counting these two resources twice at a single query.
- Kraft and MSSC profiles constrain when completion occurs.
- Local policy flows constrain whether the claimed common queries have compatible histories.

However, valid lower bounds alone do not bound a produced tree. In particular, taking the maximum of several scalars, or repeatedly resolving a certificate independently at recursive states, does not establish a shared global charge.

The new split score and state generator pass a concrete test that the earlier cutoff paradigm fails. Generalizing that proof is now a precise algorithmic question:

**Most promising direction 1: time-profile rounding with local policy consistency.** Work with the fully specified relaxation of Sections 6--7. A new proof must convert its fractional common-query histories into an actual tree with a smaller loss than $\log n/\log\log n$. Adaptive-cover suffix comparisons suggest the right amortization, but pairwise couplings cannot simply be rounded independently. No such rounding theorem is proved here.

**Most promising direction 2: certificate-guided coherent code generation.** Use explicit joint certificates to expose long useful spines, probe only their side codes, and recombine the generated states. The grid proof shows that this can handle a selector much longer than the query-probe horizon. The missing general theorem is that the generated states support a sufficiently good complete tree, or that unsupported states have a global charge to the joint certificate.

Both routes have explicit, finite optimization objects and proven lower-bound validity. Neither rests on assuming an exact continuation-cost oracle. Their general approximation analyses remain open.

Further scalar balancing of unchanged greedy is not a plausible route to the requested asymptotic improvement.

## 10. A genuinely different third scheme: sequential coding capacity

The old static cone can allocate query mass as if the algorithm already knows which tests are useful for the realized hypothesis. Shared pair mass and even all conditional subset entropies do not fully prevent this. The missing information is the **number of distinct observation histories that the tests can generate**.

This leads to sequential/Littlestone dimension, not VC dimension. The relevant tree-growth theorem is established in Bhaskar's *Thicket Density*, Theorem 4.1, [arXiv:1702.03956v4](https://arxiv.org/abs/1702.03956v4). Its application and the comparisons below are proved explicitly here; the tree-growth theorem itself is not claimed as new.

### 10.1 Definition and quasipolynomial computation

For binary tests, let $\rho(S)$ be the greatest height of a complete binary query tree for which every outcome path is realized by a hypothesis in $S$. Put $\rho(\varnothing)=-1$. Separability implies $\rho(\{h\})=0$ and $\rho(S)\ge1$ when $|S|\ge2$.

Restriction gives $\rho(A)\le\rho(S)$ for $A\subseteq S$, and

$$
\rho(S)\le\lfloor\log_2|S|\rfloor.
$$

For every splitting test, at least one outcome has rank at most $\rho(S)-1$, and the other has rank at most $\rho(S)$. Otherwise the two child witnesses would produce a complete witness of height $\rho(S)+1$.

No optimal-cost oracle is needed to compute this rank. Define

$$
V_0(S)=\mathbf1[S\ne\varnothing],\qquad
V_j(S)=\bigvee_\tau
\left(V_{j-1}(S_0)\wedge V_{j-1}(S_1)\right).
\tag{R1}
$$

Then $\rho(S)=\max\{j:V_j(S)=1\}$. For a fixed $j$, only subsets reached by at most $j$ test outcomes need evaluation. Trying $j\le\lfloor\log_2 n\rfloor$ therefore takes

$$
(nm)^{O(\log n)}
=\exp(O((\log N)^2))
$$

time in the explicit input size $N$. This searches complete **rank witnesses**, not a complete identifying tree of potentially linear height.

### 10.2 A completion-profile lower bound

Write

$$
B_r(t)=\sum_{j=0}^{\min(r,t)}\binom tj.
$$

**Theorem 7.** If $\rho(H)=r$, every complete tree satisfies

$$
\#\{h:d_T(h)\le t\}\le B_r(t),
\qquad
D\ge
\sum_{t=0}^{n-2}\left(1-\frac{B_r(t)}n\right)_+.
\tag{R2}
$$

**Proof.** At each node, label a rank-decreasing child by 1 and the other child by 0. A path has at most $r$ occurrences of 1. Encode each leaf of depth at most $t$ by its outcome string padded with zeros to length $t$. The encoding is injective because leaf paths are prefix-free. There are at most $B_r(t)$ such strings.

The mean depth equals the sum of noncompletion probabilities:

$$
\frac1n\sum_h d_T(h)
=\sum_{t\ge0}\Pr[d_T(h)>t].
$$

Apply the counting bound. $\square$

This argument also holds for randomized policies by averaging over their deterministic trees.

For every explicitly listed subset $A$, the time-indexed relaxation of Section 6 can consequently include the **linear** constraints

$$
\sum_{h\in A}(1-y_{h,t})\le B_{\rho(A)}(t).
\tag{R3}
$$

A global tree restricted to $A$ may contain constant queries and delayed singleton stopping. Neither creates additional outcome histories, so the proof still applies. All subsets constrain the same completion variables; their lower bounds are not separately charged and summed.

### 10.3 A stronger scalar bound: optimal rank-limited coding

Let $M_r(s)$ be the minimum unnormalized leaf-depth sum of an abstract proper binary tree with $s$ leaves, where along a suitable orientation every path contains at most $r$ ones. This is equivalently a bound on the tree's register/Strahler number.

It has the exact recurrence

$$
M_r(0)=M_r(1)=0,\qquad M_0(s)=+\infty\quad(s\ge2),
$$

$$
M_r(s)=s+
\min_{1\le a<s}
\left(M_{r-1}(a)+M_r(s-a)\right)
\quad(r\ge1,\ s\ge2).
\tag{R4}
$$

At least one root child has budget $r-1$, and the other has budget $r$; conversely any such two trees can be joined. Evaluate ranks in increasing order and sizes in increasing order. The computation takes $O(rn^2)$ arithmetic operations, with integer costs of $O(\log n)$ bits.

Every actual tree admits the rank-decreasing orientation above. Thus

$$
\boxed{F(S)\ge M_{\rho(S)}(|S|).}
\tag{R5}
$$

This dominates unrestricted binary coding entropy and the profile bound (R2). For rank one it is exact:

$$
M_1(s)=\frac{s(s+1)}2-1\quad(s\ge1).
$$

The all-state function $S\mapsto M_{\rho(S)}(|S|)$ is also an admissible Bellman lower bound:

$$
M_{\rho(S)}(|S|)
\le |S|+\sum_aM_{\rho(S_a)}(|S_a|).
\tag{R6}
$$

Indeed $M_r$ decreases as the allowed rank increases; use the child-rank bounds in (R4).

The decrement in (R6) need not be nonnegative. Conditioning can activate a more expensive rank-limited coding problem. This is **not** an adaptive-submodularity claim, nor permission to discard negative increments in a charging proof.

## 11. The whole static entropy--pair cone has a full-order gap

This is a stronger obstruction than an example showing that two scalar endpoints are weaker than their sum. It applies even after optimizing all pair weights, all fixed outcome predictors, and every subset entropy resource simultaneously.

### 11.1 An explicit binary family

Let $Q\ge128$ be a prime power and set

$$
d=\left\lfloor\frac Q{\ln Q}\right\rfloor,\qquad
H=\mathbb F_Q^d,\qquad n=Q^d.
$$

Give the binary tests

$$
\tau_{a,b}(h)=\mathbf1[a\cdot h=b],
\qquad (a,b)\in\mathbb F_Q^d\times\mathbb F_Q.
\tag{G1}
$$

There are $m=nQ$ listed tests. Constant tests and duplicate descriptions are harmless and can be removed; they do not change the decision-tree optimum. Keeping the list simplifies exact incidence counts.

This is a polynomial-size explicit binary instance. Its sequential rank is exactly $d$:

- Coordinate equalities provide a complete witness of height $d$.
- Every nonconstant positive answer adds a linearly independent affine equation. If its normal were in the span of earlier positive normals, its outcome would be constant on their affine solution space, and hence constant on the current state.
- Thus a proper path has at most $d$ positive answers, ruling out a complete witness of height $d+1$.

### 11.2 Mean cost is of order $Qd$

For $t\ge2d$,

$$
B_d(t)\le(d+1)\binom td
\le(d+1)\left(\frac{et}{d}\right)^d.
$$

Choose

$$
t=\left\lfloor(1/e-d^{-1/3})Qd\right\rfloor.
$$

For large $d$, $t\ge2d$, and

$$
\frac{B_d(t)}n
\le(d+1)(1-ed^{-1/3})^d
\le(d+1)e^{-e d^{2/3}}
=o(1).
$$

Theorem 7 gives the unconditional lower bound

$$
\boxed{D\ge(1/e-o(1))Qd.}
\tag{G2}
$$

A simple strategy searches the $Q$ possible values of each coordinate by equality tests, inferring the final value without querying it. Its mean cost is

$$
D_{\mathrm{coord}}
=d\left(\frac{Q+1}{2}-\frac1Q\right).
\tag{G3}
$$

Therefore $D=\Theta(Qd)$. This is binary equality testing; it is not a $Q$-outcome linear measurement.

**Corollary 9 (affine equality search).** Equations (G2)--(G3) give a polynomial-time

$$
\boxed{e/2+o(1)<1.36+o(1)}
\tag{G4}
$$

approximation for this structured family as $Q,d\to\infty$. The same lower bound holds if some hyperplane tests are deleted, and the same upper bound holds whenever the coordinate equality tests remain available.

This is a complete structural-class approximation theorem, not a guarantee for arbitrary UDT.

### 11.3 A feasible shared-query cover for every subset entropy demand

Let $J_{\mathrm{all}}(H)$ be the maximum certificate from Section 4 when **all** subsets of size at least two are available.

Define query masses

$$
\mu_{h,\tau}=
\begin{cases}
64Q^2/m,&\tau(h)=1,\\
64Q/m,&\tau(h)=0.
\end{cases}
\tag{G5}
$$

Each hypothesis is positive on exactly $m/Q$ tests, so

$$
\sum_{h,\tau}\mu_{h,\tau}
=64n(2Q-1)\le128nQ.
\tag{G6}
$$

For distinct $u,v$, their two equality indicators under a uniformly chosen $(a,b)$ are pairwise independent Bernoulli variables of parameter $1/Q$. Consequently $2m(Q-1)/Q^2$ tests separate them, and

$$
\sum_{\tau:\tau(u)\ne\tau(v)}
\min(\mu_{u,\tau},\mu_{v,\tau})
=128(Q-1)/Q\ge1.
$$

It remains to prove **every** entropy demand, not merely the root demand.

Fix $A\subseteq H$, $s=|A|\ge2$, and let $Z=|A\cap\tau^{-1}(1)|$ for a uniformly chosen listed test. Pairwise independence gives

$$
\mathbb EZ=s/Q=:\lambda,\qquad
\mathbb E[Z(Z-1)]=s(s-1)/Q^2,\qquad
\mathbb EZ^2\le\lambda^2+\lambda.
$$

For nonnegative $u,v$, write

$$
\mathcal H(u,v)=(u+v)\ln(u+v)-u\ln u-v\ln v.
$$

The demand's left side is exactly

$$
\mathcal I_A(\mu)=64Q\,\mathbb E[\mathcal H(QZ,s-Z)].
\tag{G7}
$$

**Small subsets, $2\le s\le Q/2$.** Since
$\mathbf1[Z=1]\ge Z-Z(Z-1)$,

$$
\Pr[Z=1]\ge s/Q-s(s-1)/Q^2\ge s/(2Q).
$$

Also

$$
\mathcal H(Q,s-1)
\ge(s-1)\ln\left(1+\frac Q{s-1}\right)
\ge\ln s.
$$

For the last inequality use $Q\ge s$ and $2^{s-1}\ge s$. Equation (G7) is therefore at least $32s\ln s$.

**Large subsets, $s>Q/2$.** Here $\lambda>1/2$. Paley--Zygmund and Markov give

$$
\Pr[Z\ge\lambda/2]\ge1/12,\qquad
\Pr[Z>24\lambda]\le1/24.
$$

Thus with probability at least $1/24$,
$QZ\ge s/2$ and $s-Z\ge3s/4$, because $Q\ge96$. The function $\mathcal H$ is increasing in each argument, so it is at least $\mathcal H(s/2,s/2)=s\ln2$ on that event.

Since $\ln s\le\ln n=d\ln Q\le Q$,

$$
\mathcal I_A(\mu)
\ge \frac{64\ln2}{24}Qs
\ge s\ln s.
$$

This proves all subset demands with no sampling or union bound.

Weak duality in (EC) now implies

$$
\boxed{J_{\mathrm{all}}(H)\le128nQ.}
\tag{G8}
$$

One can use weak duality without relying on strong duality: multiply each capacity (J) by $\mu_{h,\tau}$; pair coverage pays for each pair weight, and weighted cross-entropy pays for each resource entropy. Their combined objective cannot exceed (G6).

### 11.4 A full asymptotic separation

Uniform pair weights

$$
w_{uv}=\frac{Q^2}{n(Q-1)}
$$

are feasible. At a hyperplane test, write $a,b$ for the positive and negative populations of $S$. The ratio $ab/(a+b)$ increases in both arguments and is at most its value at the full populations $n/Q$ and $n(Q-1)/Q$. Thus $w_{uv}ab\le|S|$ for every state.

Their total weight is at least $nQ/2$. Combining this with (G2), (G3), and (G8) proves:

**Theorem 8.**

$$
J_{\mathrm{all}}(H)=\Theta(nQ),\qquad
F(H)=\Theta(nQd),\qquad
\boxed{\frac{F(H)}{J_{\mathrm{all}}(H)}
=\Theta\!\left(\frac{\log n}{\log\log n}\right).}
\tag{G9}
$$

Here $Q\sim\ln n$ and $d\sim\ln n/\ln\ln n$ by construction.

Consequently, no algorithm can have an $o(\log n/\log\log n)$ guarantee **relative to this static relaxation**, even if the relaxation uses exponentially many entropy resources.

This is a relaxation-gap theorem, not computational hardness and not a lower bound against all quasipolynomial algorithms.

The new rank certificate is asymptotically stronger:

$$
M_{\rho(H)}(n)\ge(1/e-o(1))nQd.
$$

Adding the rank completion constraints (R3) at the root to the time LP also forces cost $\Omega(nQd)$. Thus the third scheme removes a whole asymptotic factor on an explicit instance where the previous entire static cone fails.

## 12. Activation-priced coding resources and depth-independent composition

The rank bound is useful not only as another root scalar. It can be allocated to an internal coding problem while pair weights pay for finding which coding problem is active.

### 12.1 A general shared-budget certificate

For each listed resource $A$, obtain an actual certified number $b_A\le F(A)$, and put

$$
\kappa_A(\tau)=\mathbf1[\tau\text{ is nonconstant on }A].
$$

Two concrete, oracle-free choices are:

- $b_A=M_{\rho(A)}(|A|)$, computable in quasipolynomial time.
- $b_A=F(A)$ for $|A|$ polylogarithmic in input size, computed by the exact subset recurrence in $O(m|A|2^{|A|})$ time.

Choose $\lambda_A\ge0$, pair weights, and their global test-specific endpoint assignments, subject to

$$
\sum_{A\ni h}\lambda_A\kappa_A(\tau)
+\sum_{g:\tau(g)\ne\tau(h)}f^\tau_{hg,h}
\le1
\quad\text{for every }h,\tau.
\tag{A1}
$$

**Theorem 10.**

$$
\boxed{\sum_A\lambda_A b_A+\sum_{\{u,v\}}w_{uv}\le F(H).}
\tag{A2}
$$

**Proof.** Restrict an arbitrary complete tree to $A$ and suppress queries that become constant. Every retained query uses a test nonconstant on the original $A$. Therefore

$$
b_A\le F(T|A)
\le\sum_{h\in A,\tau}\kappa_A(\tau)\,
\#\{\tau\text{ queries on the path of }h\}.
$$

Multiply by $\lambda_A$. Charge every pair once at first separation and assign its weight to its endpoints. At any actual query node, sum (A1) over its hypotheses. The combined charge is at most that node's population. Sum over the tree. $\square$

The resources may overlap. A test constant on one resource does not reserve coding budget there, leaving that resource's vertices available to pay for an activation/search charge.

This is an ordinary polynomial-size LP once the $b_A$ are computed. It can be combined with the entropy code-length terms of Section 4 in the **same** endpoint capacity.

In the cover dual, the added constraints are simply

$$
\sum_{h\in A,\tau}\kappa_A(\tau)\mu_{h,\tau}\ge b_A.
\tag{A3}
$$

These are stronger than entropy alone on the finite-field example. They price the internal computation/identification task, not just its number of possible outputs.

The stated choices of $b_A$ are actually computable within their specified budgets. No assumption that an approximation oracle returns them is used.

### 12.2 A factored activation class with arbitrarily many levels

Let $L\ge1$ and

$$
H=[C_1]\times\cdots\times[C_L]\times X,
\qquad C_j\ge2,\quad |X|=p.
\tag{A4}
$$

The product coordinates and test types are part of this structural instance description. A proposed description can be checked against the explicit test matrix in polynomial time; there is no claim that such a description exists or is discoverable for every UDT instance.

Let $\mathcal T_X$ be a separating binary test family on $X$. Permit:

1. Selector tests whose positive set is a prescribed gate prefix $(i_1,\ldots,i_j)$.
2. Tests $\mathbf1[(i_1,\ldots,i_j)=a]\sigma(x)$, where $\sigma\in\mathcal T_X$ and $a$ is a prescribed prefix. The empty prefix gives ungated distractors.

Require the selector queries needed to search each next gate coordinate, and full-prefix copies of the core tests. Additional tests of either permitted type are allowed without restriction.

Both the number of activation levels and the lengths of selector spines may grow. All actual tests still have two outcomes.

For each full gate vector $i$, let $A_i=\{i\}\times X$. Every fibre has the same restricted core instance.

### 12.3 A single global charge for all levels

Take $\lambda_{A_i}=1$ and give weight one to each pair with the same $x$ and gate vectors differing in exactly one coordinate.

These are feasible in (A1):

- A selector is constant on every fibre, so it spends no coding budget. Assign each separated edge to its endpoint outside its positive prefix.
- A core test gated to prefix $a$ spends one coding unit in each active fibre and zero in every inactive fibre. Assign every separated gate edge to its endpoint outside $a$.
- An outside gate vector has at most one neighbor inside the prescribed prefix: such a neighbor exists only when the prefix differs in exactly one coordinate, and then it is unique. Thus every outside endpoint receives at most one unit.
- Ungated core tests separate no positive-weight pair, because these pairs share $x$.

There are $\frac n2\sum_j(C_j-1)$ positive-weight pairs. Hence, for any certified core cost $b\le F(X)$,

$$
\boxed{
D\ge \frac bp+\frac12\sum_{j=1}^L(C_j-1).
}
\tag{A5}
$$

This does not charge OPT independently at the successive activation levels. All coding and search charges coexist in one globally feasible certificate.

### 12.4 An actual algorithm and a depth-independent guarantee

Search each gate coordinate by its $C_j-1$ selector queries, then execute a complete core code. Suppose that code has conditional mean cost $U_X$.

The exact mean selector cost is

$$
s(C)=\frac{C+1}{2}-\frac1C
=\frac{C-1}{2}\left(1+\frac2C\right).
$$

Therefore

$$
C_{\mathrm{out}}=U_X+\sum_j s(C_j).
$$

**Theorem 11.** If the chosen core code and certified bound satisfy the verified inequality $U_X\le c\,b/p$, then this explicit construction has ratio at most

$$
\boxed{\max\{c,\ 1+2/C_{\min}\},\qquad
C_{\min}=\min_j C_j.}
\tag{A6}
$$

**Proof.** Use the displayed identity for $s(C)$ to bound the algorithm's cost by this factor times the right side of (A5). $\square$

The important feature is that the factor has **no multiplicative dependence on $L$**. The following corollaries fill in both the core algorithm and the certificate, rather than assuming an oracle.

**Arbitrary polylogarithmic core.** If $p\le(\log N)^a$ for a fixed $a$, compute the exact core code and its exact cost by subset DP. Then $c=1$, and (A6) gives a genuinely quasipolynomial **two-approximation** for the entire structural class, with arbitrarily many activation levels and long spines.

If additionally $C_{\min}\ge\lceil2/\varepsilon\rceil$, it gives a $(1+\varepsilon)$ approximation in the same quasipolynomial time. This is a structural-class guarantee, not a PTAS for arbitrary UDT.

The only exponential computation is $2^p$ on the core. The selector tree and copies of the core code have at most $n-1$ internal nodes and are constructed in polynomial time after the core solve. There is no enumeration to the depth of a long selector spine.

**Heterogeneous cores.** The two-approximation does not require identical core test families. More generally, permit each core predicate $\sigma$ to depend on the test and its gate prefix, while remaining the same predicate on $X$ throughout that prefix. Once the full gate vector $i$ is known, use the actual tests restricted to $A_i$. Instance separability ensures that this restricted core is identifying; extra full-prefix copies are unnecessary.

Set $b_i=F(A_i)$ and compute these $p$-hypothesis optima exactly. The same pair assignment and $\lambda_{A_i}=1$ give

$$
D\ge \frac1n\sum_i b_i+\frac12\sum_j(C_j-1).
$$

The gate-first algorithm's core contribution is exactly $\frac1n\sum_i b_i$. The selector identity proves the same $1+2/C_{\min}\le2$ ratio. Solving every fibre takes at most a polynomial factor in $N$ times $2^p$, so the quasipolynomial claim is unchanged.

This gives a parameterized approximation result for a verified prefix-activation description of width $p$, even when every leaf has a different internal decision-tree problem. It still does not assert that arbitrary test matrices admit such a small-width description.

**Affine core.** Take $X=\mathbb F_Q^d$ with coordinate equality tests and any additional affine-hyperplane tests. Use $b=M_d(Q^d)$ and the coordinate code. Equations (G2)--(G3) give $c=e/2+o(1)$ as $Q,d\to\infty$. The entire activation instance then has ratio

$$
\max\{e/2+o(1),\ 1+2/C_{\min}\}.
$$

In particular, if every gate has at least six values, it has ratio $e/2+o(1)$, independently of the number of activation levels. For arbitrary gate sizes it has ratio at most $2+o(1)$.

For a single gate, its selector overhead above the pair lower bound is less than one. Consequently the single-gate affine-core family has ratio $e/2+o(1)$ even without a lower bound on the gate size.

These are fully proved algorithms on explicit structural families. They do not assume that arbitrary UDT instances possess the factorization (A4).

## 13. What the stronger results change in the general attack

The previous static scheme is now known to be insufficient in a sharp sense: Theorem 8 exhibits its entire old asymptotic loss, even with all subset resources. Optimizing more fixed entropy predictors within that cone cannot eliminate the example.

The new resources distinguish three genuinely different obstacles:

- **Coding entropy:** many possible answers.
- **Sequential capacity:** too few realizable feedback histories, even when a clairvoyant fractional allocation appears to supply enough entropy.
- **Activation/search:** locating the right internal code, sometimes through a selector much longer than a quasipolynomial depth-probe horizon.

The activation composition theorem supplies an unconditional positive proof that these budgets can be charged together without multiplying the loss at each level. It is not just a maximum of unrelated scalar lower bounds.

### 13.1 A computable general lower-bound base

For a finite resource family, let $J_{\mathcal A}(S)$ be the optimized old entropy/pair bound restricted to $S$. Both it and the rank-code bound satisfy the Bellman lower-bound inequality. Therefore

$$
B(S)=\max\{J_{\mathcal A}(S),M_{\rho(S)}(|S|)\}
$$

does as well: use the constituent attaining the parent maximum and bound each child by its own maximum.

One may lift this base by

$$
B_0(S)=B(S),\qquad
B_{j+1}(S)=|S|+\min_{\tau\text{ splitting }S}
\sum_a B_j(S_a),
$$

with zero at empty sets and singletons. Then

$$
B(S)\le B_j(S)\le B_{j+1}(S)\le F(S).
$$

For a fixed-power polylogarithmic horizon this remains quasipolynomial, including the fresh rank computations on the reached states. Lifting is ordinary dynamic programming, not a newly claimed approximation algorithm. The substantive new separation is that the rank base already exceeds the whole static cone by an asymptotic factor on Theorem 8's instance, without probing to the depth of its identifying tree.

Activation-priced resources (A1), exact small-core costs, and shared rank-profile constraints (R3) can also be added to the finite relaxation of Sections 6--7.

### 13.2 The remaining global problem

The most promising modification is now to use rank/profile constraints to detect codes that cannot be paid for by ordinary entropy, while activation-priced resources expose where such codes can be reused. Retain and recombine actual codes generated from these states; do not independently regenerate and recharge their values at every level.

For arbitrary instances, the outstanding step is to discover sufficiently useful activation regions and compatible code states within a quasipolynomial budget, and prove that their complete recombined tree has a smaller worst-case ratio.

The structural-class composition proof shows what a successful global charge should look like. It does not prove that all instances admit that charge. Neither the new lower bounds nor the verified class algorithms establish an unconditional $o(\log n/\log\log n)$ guarantee for arbitrary UDT.

## 14. New greedy rules with a single MSSC price ledger

The main change is to select a code experiment by its **actual total work per newly identified hypothesis across the entire unfinished frontier**, rather than independently selecting a split inside each branch.

This retains one global ordering of completions, which permits an MSSC histogram argument. The internal experiments and the final decision tree are still adaptive.

These are general-instance constructions. Their guarantees compare to explicitly defined finite code-menu benchmarks, not an assumed continuation-cost oracle.

### 14.1 Executable code menus

Work on an initial hypothesis set $S$ of size $s$. A menu experiment $j$ has:

- A static guaranteed-completion set $A_j\subseteq S$.
- A positive inspection allowance $a_j$.
- A nonnegative service allowance $b_j$.
- An explicit partial original-test policy that, on any $h\in A_j$, identifies $h$.
- On any hypothesis $h$, a query-cost upper bound

$$
a_j+b_j\mathbf1[h\in A_j].
\tag{MG1}
$$

Conditioning on observations, caching answers, and suppressing constant queries may only reduce this cost and may produce additional identifications.

Two useful, fully realizable experiment types are:

1. **Outcome-code service.** Query an original test. On a selected outcome class $A_j$, execute a known complete code for that class; on other outcomes, return unfinished. Take $a_j=1$ and $b_j$ equal to the code's maximum depth.
2. **Capped code harvesting.** A membership filter for a represented region $A$ takes at most $\ell$ queries. If the filter accepts, run a known code $T_A$ down to original code depth $t$. The static completion set is
   $A_j=\{h\in A:d_{T_A}(h)\le t\}$. Take $a_j=\ell+t$, $b_j=0$. Unfinished paths return to the outer controller.

A region represented by a test history has an actual membership filter: ask its history tests and reject at the first mismatching outcome. No synthetic membership oracle is used.

A complete code on $S$, such as greedy, is a backup experiment covering all of $S$. Thus the menu covers every hypothesis.

For full outcome codes, maximum depth is an honest invoice. The full-set average depth cannot silently replace it: a later restricted subset can have larger conditional average depth.

### 14.2 Shared-frontier, actual-work greedy

Let $\mathcal F$ be the current frontier of unfinished candidate sets and let

$$
R=\bigcup_{B\in\mathcal F}B,\qquad r=|R|.
$$

The sets in $\mathcal F$ are disjoint. Singleton leaves are marked finished immediately.

For each menu experiment $j$, simulate its conditioned execution on every frontier set, using the explicit test table and code. Define:

$$
W_j(\mathcal F)=
\sum_{h\in R}
\{\text{new queries executed on the path of }h\},
$$

$$
K_j(\mathcal F)=
\#\{\text{hypotheses newly identified by this experiment}\}.
$$

Choose

$$
\boxed{
j\in\arg\min_{K_j(\mathcal F)>0}
\frac{W_j(\mathcal F)}{K_j(\mathcal F)}.
}
\tag{MG2}
$$

Apply that same experiment throughout the unfinished frontier, retaining all its observations. Repeat.

This is an offline construction of a valid decision tree. Selection depends on the entire known partial policy, not on unavailable knowledge of the actual target. Each experiment itself branches only on allowed test outcomes.

At least one hypothesis finishes at every stage. The backup code ensures a feasible choice. There are therefore at most $s$ stages.

For a single binary outcome-code experiment, when the other outcome does not itself become a singleton, the actual-work score is

$$
\frac{|R|+F_{T_A}(R\cap A)}{|R\cap A|}.
$$

This can prefer a less balanced split with a genuinely cheaper side code. It is not another symmetric function of the two outcome sizes.

The simpler conservative **service-density greedy** score is

$$
b_j+\frac{a_j|R|}{|R\cap A_j|}.
\tag{MG3}
$$

The actual-work rule takes advantage of pruning, cache reuse, and extra identifications instead of charging all allowances at equality.

### 14.3 The fixed-menu MSSC benchmark

Let $Q$ be any ordering of menu experiments that covers $S$. For each hypothesis $h$, let $j_Q(h)$ be its first covering experiment, and let $t_Q(h)$ be the cumulative inspection allowances through that experiment.

Define

$$
L_Q=\sum_h t_Q(h),\qquad
C_Q=\sum_h b_{j_Q(h)}.
\tag{MG4}
$$

This is MSSC with processing times $a_j$ and an additional first-cover service fee $b_j$. Executing that ordering as a policy costs at most $L_Q+C_Q$. The benchmark itself can overestimate that policy because it does not credit cached queries or additional feedback.

Crucially, this benchmark is not unrestricted UDT OPT.

Suppose actual-work greedy chooses an experiment with price

$$
p=\frac{W_j(\mathcal F)}{K_j(\mathcal F)}.
$$

For any other menu experiment $i$, put $k_i=|R\cap A_i|$. Its invoice and completion guarantee imply

$$
K_i(\mathcal F)\ge k_i,\qquad
W_i(\mathcal F)\le a_i r+b_i k_i.
$$

Thus, whenever $k_i>0$,

$$
\boxed{p\le b_i+\frac{a_i r}{k_i}.}
\tag{MG5}
$$

Charge the selected price $p$ to every newly completed hypothesis. Total assigned price is exactly the actual unnormalized cost $G$ of the finished greedy policy:

$$
G=\sum_{\text{stages}}W_j(\mathcal F)=\sum_h p_h.
\tag{MG6}
$$

The shared frontier, rather than independent local greedies, is what makes $R$ the global set of not-yet-completed hypotheses in this price ledger.

### 14.4 A complete MSSC comparison

**Theorem 12.** The actual-work greedy policy satisfies, for every fixed covering ordering $Q$,

$$
G\le6(L_Q+C_Q).
\tag{MG7}
$$

If $Q$ uses only zero-service experiments, the stronger bound is

$$
\boxed{G\le4L_Q.}
\tag{MG8}
$$

The algorithm may select service experiments even when the comparison ordering has zero service fees.

**Proof.** At a greedy stage with remaining population $r$ and price $p$, (MG5) bounds the number of remaining hypotheses a comparison experiment can cover.

For (MG7), a hypothesis with comparison cost $t_Q(h)+b_{j_Q(h)}\le p/3$ has first-cover time at most $p/3$ and service fee at most $p/3$. Every such comparison experiment covers at most

$$
k_i\le \frac{3a_i r}{2p}
$$

members of $R$. Those experiments' total inspection allowance is at most $p/3$. They can therefore cover at most $r/2$ members of $R$. At least $r/2$ members of $R$ have comparison cost greater than $p/3$.

Draw a greedy price histogram, with unit-width columns in greedy completion order and heights $p_h$. Draw the comparison cost histogram, with columns sorted by $t_Q(h)+b_{j_Q(h)}$. A point in the current greedy stage's columns is at distance at most $r$ from the right boundary and at height at most $p$.

Shrink the greedy histogram's width by two and height by three, aligning it to the right. The preceding tail bound places every shrunk point under the comparison histogram. Its area is $G/6$, proving (MG7).

For a zero-service comparison, (MG5) gives $k_i\le a_i r/p$. By inspection time $p/2$, comparison experiments cover at most $r/2$ members of $R$. Shrinking both width and height by two proves (MG8). $\square$

This is the Feige--Lovasz--Tetali price/histogram mechanism, now applied to actual adaptive code work with extra completions. It does not invoke the fully adaptive interpretation of a fixed-order Pandora theorem.

### 14.5 An affine service-preserving comparison

**Theorem 13.** For every $\varepsilon>0$ and every fixed covering ordering $Q$,

$$
\boxed{
G\le
\frac{2(1+\varepsilon)^2}{\varepsilon}
\ln\left(1+\frac2\varepsilon\right)L_Q
+(1+\varepsilon)C_Q.
}
\tag{MG9}
$$

**Proof.** Choose $\beta>1$, $\alpha>0$, and put

$$
\mu=\frac{\beta}{\alpha}\ln\frac{\beta}{\beta-1}<1.
$$

At a greedy stage of price $p$, a hypothesis satisfying
$\alpha t_Q(h)+\beta b_{j_Q(h)}\le p$
is first covered by an experiment finishing at time $t_i\le p/\alpha$ and having
$b_i\le(p-\alpha t_i)/\beta$.

Equation (MG5) bounds that experiment's coverage in $R$ by

$$
k_i\le
\frac{\beta r a_i}{(\beta-1)p+\alpha t_i}.
$$

Since the denominator increases with $t_i$, a right-endpoint integral estimate over the comparison inspection intervals gives

$$
\sum_{\text{eligible }i}k_i
\le
\beta r\int_0^{p/\alpha}
\frac{dt}{(\beta-1)p+\alpha t}
=\mu r.
$$

At least $(1-\mu)r$ members of $R$ consequently have comparison height
$\alpha t_Q(h)+\beta b_{j_Q(h)}>p$.

Shrink only the width of the greedy price histogram by $1-\mu$ and align it to the right. It fits under this comparison histogram. Therefore

$$
G\le\frac{\alpha}{1-\mu}L_Q+\frac{\beta}{1-\mu}C_Q.
$$

Set

$$
\beta=1+\varepsilon/2,\qquad
\mu=\frac{\varepsilon}{2(1+\varepsilon)},\qquad
\alpha=\frac{\beta}{\mu}\ln\frac{\beta}{\beta-1}.
$$

Then $\beta/(1-\mu)=1+\varepsilon$ and the latency coefficient is exactly the one in (MG9). $\square$

This is an unconditional comparison for the explicit menu. It is not the missing general continuation-pricing oracle: its fees are honest fixed code-depth allowances, and its latency loss is $O(\varepsilon^{-1}\ln(1/\varepsilon))$. For $\varepsilon=1/\log n$, that loss is too large to complete the earlier quasipolynomial target.

### 14.6 Cost-aware code harvesting and algorithmic scope

For a known complete code $T$, add capped prefixes at depths $1,2,4,\ldots$, stopping at a cap at least its height. These are zero-service experiments. A hypothesis of depth $d$ is covered by a cap ordering of total inspection allowance less than $4d$. Consequently the zero-fee coded-MSSC benchmark is at most $4F_T(S)$, and (MG8) gives $G\le16F_T(S)$.

Choosing the best known full code directly gives a better bound when there is only one useful code. The reason to harvest is to combine short successful parts of **different** codes while retaining all their feedback.

An oracle-free library can contain:

- The complete greedy backup.
- Complete codes on states already produced by finite-depth rollout, each with its explicit history membership filter.
- Their capped prefixes.
- Newly assembled complete codes from the represented-state DAG.

A finite quasipolynomial library gives quasipolynomial planning time: at most $s$ greedy stages, each using polynomial-time simulations of explicit codes. Long code paths need not be enumerated as new test histories; they are already represented by their code trees.

To guarantee nonregression, also evaluate every greedy stage prefix followed by the available greedy backup restricted to its remaining frontier. Return the cheapest complete policy among these, including the empty prefix. The returned cost is at most both $G$ and the original greedy cost.

Thus the construction preserves the established general UDT approximation bound while gaining the MSSC comparisons above. It does not yet prove a smaller general ratio.

The remaining obstacle is now specific: prove that an affordable code library has a coded-MSSC benchmark small enough relative to unrestricted UDT OPT. Taking each hypothesis's cheapest available certificate as its fee would be invalid; those individually cheap certificates can still be costly to locate.

## 15. Planar supplied-line tests: a sublogarithmic worst-case approximation

This section answers the subsequent explicit geometric question. Unlike Sections 11--12, it applies to **all** finite sets of distinct planar points and separating supplied line families. No product structure, parallelism, convex-position assumption, or availability of invented separator lines is required.

### 15.1 Statement

Let $P$ be $n$ distinct points in $\mathbb R^2$, and let $\mathcal L$ be a supplied finite family of lines separating every pair of points. Each line query costs one.

First assume that no point lies on a test line, so outcomes are binary. Let

$$
D_\infty=\min_T\max_{h\in P}d_T(h).
$$

**Theorem 15.** A polynomial-time algorithm using only the supplied line tests constructs a tree of height

$$
\boxed{
O\left(\frac{\log n}{\log\log n}\right)D_\infty.
}
\tag{PL1}
$$

This is an $o(\log n)$ worst-case approximation. The same asymptotic guarantee holds when a point on a line produces a third, zero outcome.

For the binary case, with $L=\ln n\ge16$, the proof gives the explicit ratio

$$
3+(6+\ln2)\frac{L}{\ln L}.
\tag{PL2}
$$

No little-$o(\log n/\log\log n)$ approximation to **average-cost** OPT is claimed by this theorem.

### 15.2 A flat state's majority answers have a geometric witness

Fix one global parameter $0<\delta<1/3$. A state $S\subseteq P$ is balanced if some supplied line has no outcome class larger than $(1-\delta)|S|$.

Otherwise call it flat. In the binary case, every line has a unique majority side containing more than $(1-\delta)|S|$ points. Its minority cap contains fewer than $\delta|S|$ points.

Any three majority open halfplanes contain a common member of $S$: their excluded caps together contain fewer than $3\delta|S|<|S|$ points. Helly's theorem in the plane therefore gives a point $p$ lying **strictly** in every majority halfplane.

This witness need not be a hypothesis. It is used only for offline selection of supplied tests. It can be found by linear programming with a positive common slack; no query through $p$ is introduced.

### 15.3 A polynomial three-approximation for a majority certificate

A majority certificate is a set of supplied lines whose minority caps cover all but at most one point of $S$.

Let $q^*(S)$ be the minimum number of lines in such a certificate.

**Lemma 15.1.** In a flat planar state, a certificate of size at most $3q^*(S)$ can be found in polynomial time.

**Proof.** Translate coordinates so that the common majority witness $p$ is the origin. Write every minority halfplane as

$$
H_i=\{x:a_i\cdot x\ge b_i\},\qquad b_i>0,
$$

and define the candidate dual point $u_i=a_i/b_i$. A supplied line covers a point $h$ precisely when

$$
u_i\cdot h\ge1.
\tag{PL3}
$$

The use of a closed halfplane is harmless in the binary case because no hypothesis lies on a test line.

Thus choosing covering lines is equivalent to selecting candidate dual points that hit the demand halfplanes

$$
R_h=\{u:u\cdot h\ge1\}.
$$

Let $V$ be the vertices of the convex hull of all candidate dual points. Every candidate point is a convex combination of at most three vertices, by Caratheodory's theorem. If it lies in a demand halfplane, at least one of those three vertices lies in that halfplane. Replacing each selected candidate by these at most three hull vertices preserves every covered demand.

An optimal $q^*$-line certificate consequently has a hull-vertex replacement of size at most $3q^*$.

On the cyclic order of the hull vertices, the vertices in a demand halfplane form a circular interval, possibly empty or the entire cycle. A minimum hitting set for circular intervals is computable exactly:

1. Choose any nonempty demand interval.
2. Enumerate its possible selected vertices $v$.
3. Remove intervals already hit by $v$ and cut the cycle at $v$.
4. The remaining demands are ordinary intervals. Hit them greedily at the right endpoint of the earliest-ending interval.
5. Keep the smallest solution over the choices of $v$.

To cover all but one hypothesis, enumerate the possible omitted hypothesis and solve the corresponding interval problem. Discard infeasible choices. At least one is feasible: two hypotheses missed by every minority cap would have identical outcomes on all supplied tests, contradicting separability.

The best hull solution is no larger than the threefold replacement of an optimal certificate. Every selected hull vertex is an actual candidate dual point, hence an actual supplied line. Degenerate hulls of dimension zero or one only require one or two replacement vertices. $\square$

No arbitrary dual candidate, artificial separator line, or geometric membership oracle is allowed in this construction.

### 15.4 The certificate size is lower-bounded by optimal height

**Lemma 15.2.**

$$
q^*(S)\le D_\infty(S)\le D_\infty(P).
\tag{PL4}
$$

**Proof.** Follow the answers of the witness point $p$ through an optimal tree for $S$. All these answers are the frozen majority answers relative to the initial $S$. Add empty outcome leaves to the tree if necessary; doing so does not increase its height.

When this path ends, at most one hypothesis remains consistent with its answers. The queried lines' minority caps therefore cover all but at most one member of $S$. The path contains at most $D_\infty(S)$ tests.

The second inequality follows by restricting an optimal full-instance tree to $S$ and suppressing constant queries. $\square$

This is a worst-case certificate comparison, not an assertion that an arbitrary witness is a likely hypothesis.

### 15.5 The algorithm

Use the same $\delta$ throughout the construction.

At a nonsingleton state $S$:

1. **Balanced state:** choose any line whose largest outcome has size at most $(1-\delta)|S|$, query it, and recurse.
2. **Flat state:** compute the certificate of Lemma 15.1 and query its lines along their frozen-majority spine. On a minority answer, recurse on that outcome class. If the majority spine leaves one hypothesis, stop.

The certificate lines can be ordered greedily by their remaining cap coverage, in the spirit of MSSC. The worst-case proof only uses the certificate's cardinality, so any ordering works.

At every minority exit of a flat spine, the new state has size less than $\delta|S|$, where $S$ is the state at the **start** of that spine. The lines need not retain their majority status on all later residual states.

Constant queries are suppressed. If a proposed spine query is constant with its nonmajority answer on the residual state, that entire residual state already has size less than $\delta|S|$ and can be passed directly to recursion.

Each flat spine has at most

$$
3q^*(S)\le3D_\infty(P)
$$

queries, and terminates or makes a factor-$\delta$ size reduction.

This is a complete algorithm on every valid supplied-line instance.

### 15.6 Height analysis

Consider any root-to-leaf path. Balanced queries shrink its candidate population by at least a factor $1-\delta$. All other queries are nonexpanding. Their number is at most

$$
\frac{\ln n}{-\ln(1-\delta)}
\le\frac{L}{\delta}.
$$

Every flat spine except possibly the final one ends in a factor-$\delta$ reduction. The number of flat spines is at most

$$
1+\frac{L}{\ln(1/\delta)}.
$$

Using (PL4), the output height satisfies

$$
H_{\mathrm{out}}
\le
\frac{L}{\delta}
+3D_\infty\left(1+\frac{L}{\ln(1/\delta)}\right).
\tag{PL5}
$$

Since $D_\infty\ge\log_2 n=L/\ln2$,

$$
\frac{H_{\mathrm{out}}}{D_\infty}
\le
\frac{\ln2}{\delta}
+3\left(1+\frac{L}{\ln(1/\delta)}\right).
\tag{PL6}
$$

For $L\ge16$, choose

$$
\delta=\frac{\ln L}{L}.
$$

Then $\delta<1/3$ and
$\ln(1/\delta)=\ln L-\ln\ln L\ge\frac12\ln L$.
Substitution proves (PL2), hence (PL1).

For the remaining bounded range of $n$, fix $\delta=1/4$; it has no effect on the asymptotic ratio.

The improvement comes from a constant-factor geometric certificate-cover algorithm. It is not obtained by substituting parameters into the supplied subexponential tradeoff.

### 15.7 Points lying on supplied lines

Suppose queries return negative, zero, or positive.

Keep the balanced rule: some line has largest outcome at most $(1-\delta)|S|$.

In a flat state there are two possibilities:

- **Every dominant outcome is a sign.** Its nonmajority cap is the closed opposite halfplane, including points on the line. The strict majority halfplanes satisfy the same Helly argument. The dual hitting-set construction and the threefold certificate bound remain valid. There are now two possible minority exits, each of size less than $\delta|S|$.
- **Some dominant outcome is zero.** Query that line. Its zero class is collinear; both off-line classes have size less than $\delta|S|$ and recurse as before. Identify the collinear class by median threshold queries using supplied lines.

For completeness, any two adjacent distinct collinear hypotheses must be distinguished by some supplied line. Such a line intersects their segment, possibly at an endpoint. Choosing the pair at the median gap therefore gives a query whose negative and positive groups each have size at most $\lceil |S|/2\rceil$, while the zero group has at most one point. Recursion yields a collinear code of height at most $\lceil\log_2|S|\rceil$.

A zero-dominant stage thus either makes a factor-$\delta$ reduction after one query, or finishes with height at most $1+\lceil\log_2 n\rceil$. Since $D_\infty\ge\log_3 n$ and $D_\infty\ge1$, this stage's height is at most $4D_\infty$.

Replacing the coefficient three in (PL5) by four, and using the ternary information lower bound, gives

$$
\frac{H_{\mathrm{out}}}{D_\infty}
\le
\frac{\ln3}{\delta}
+4\left(1+\frac{L}{\ln(1/\delta)}\right)
\le
4+(8+\ln3)\frac{L}{\ln L}
\quad(L\ge16).
\tag{PL7}
$$

Thus the same $o(\log n)$ approximation holds without a general-position assumption.

### 15.8 Runtime and precise scope

At each flat state, the algorithm performs planar convex-hull computation, a fixed-dimensional linear program, and polynomially many circular-interval hitting-set computations. All choices are polynomial in the explicit point/line input size. Rational coordinates admit ordinary polynomial-bit-complexity implementations.

Balanced cuts, side branches, and collinear median cuts are also polynomial-time operations. Suppressing constant tests leaves a proper complete tree with at most $n-1$ internal nodes, so the full construction is polynomial time.

The theorem concerns the **approximation ratio**, not a claim of absolute $o(\log n)$ query depth. Some supplied-line instances require linear depth.

It fulfills the user's worst-case alternative for the explicitly requested planar subcase. The proof does not compare its tree with uniform average-depth OPT, nor establish an improved approximation for arbitrary nongeometric test matrices.

The proof uses classical Helly and Caratheodory theorems and elementary circular-interval stabbing. Literature-wide priority for this combination is not asserted. General-test hardness or point-location results allowing invented comparison lines must not be substituted for this supplied-line model.

## 16. Further planar investigation: full hull-pattern learning

This section records the intermediate investigation after the requested manuscript cleanup. The local lemmas and the rejected cyclic-order shortcut below remain useful, but their missing global step has since been closed by supporting-prefix credit. The active TeX manuscript contains the stronger constant expected-depth proof, and Section 17 below records the subsequent constant deterministic maximum-depth proof.

Work with unit-cost binary supplied-line tests, a candidate state $S$, and original unnormalized probabilities $\pi_h$. Choose a point $p$ on no test line. Freeze each test's answer at $p$. Translate $p$ to the origin and write its opposite half-plane as

$$
C_i=\{x:u_i\cdot x>1\}.
$$

The finite hypothesis coordinates here are $x_h=h-p$. Off-boundary input makes strict and weak inequalities equivalent for their outcomes.

Let

$$
K=\operatorname{conv}(\{0\}\cup\{u_i:i\in[m]\}),
$$

and let $V$ be its actual, nonzero vertices. Every element of $V$ is an original supplied test. The point $0$ is a preprocessing marker with a known negative outcome; it is never an information query.

### 16.1 Hull replacement and interval structure

By Caratheodory, each original $u_i$ is a convex combination of at most three vertices of $K$. If $u_i\cdot x_h>1$, at least one supporting nonzero vertex $v$ also has $v\cdot x_h>1$. Thus every original cap is contained in the union of at most three actual hull-vertex caps.

For each hypothesis, its positive vertices in the cyclic order on $K$ form a circular interval. This follows because its positive region in the dual plane is a half-plane. Adding the known-negative origin to the cyclic boundary when it is a boundary point does not change this property.

There is an important compactness consequence which does **not** require querying the vertices in cyclic order.

**Three-neighbor footprint lemma.** Suppose a frozen-answer spine uses hull-vertex tests in any order. Before querying an unqueried vertex $v$, let $a,b$ be the nearest already-queried vertices on either side of $v$ in the cyclic order. If there is just one previous vertex, use it for both neighbors. The first-positive exit at $v$ is exactly

$$
S\cap C_v\cap C_a^c\cap C_b^c.
$$

When there is no previous query it is simply $S\cap C_v$.

**Proof.** A positive circular interval containing $v$ and excluding its two neighboring queried vertices cannot contain any other queried vertex: doing so would require crossing one of those negative neighbors. Therefore these two negative constraints imply all previous negative spine answers on the exit. The converse is immediate. Degenerate hulls have at most two nonzero vertices and are handled directly.

Consequently, first-positive exits at one fixed parent state have polynomially many three-test descriptions, even for a long, arbitrarily ordered spine. This avoids the earlier temptation to impose a cyclic query order.

The parent state $S$ is still present in the formula. Deeper states can accumulate parent constraints; this lemma does not make the full exact Bellman state family polynomial.

### 16.2 A stronger partial operation with a complete cost proof

**Hull-pattern lemma.** There is a polynomial-time partial policy that learns all hull-vertex test outcomes on the target at expected cost at most

$$
32F(S).
$$

It uses only supplied line queries. Its leaves are the hypotheses' hull-pattern classes, not necessarily singleton hypotheses.

**First-positive search.** Enumerate a terminal hypothesis $z$ as in the forced-witness spine construction. Run weighted MSSC greedy on $S\setminus\{z\}$ using hull caps, and merge it with an exact minimum-cardinality hull-cap cover.

Fix an optimal conditional tree and follow $p$ through it, obtaining a comparison spine $Q$ with

$$
\operatorname{MSSC}_{S\setminus\{z\}}(Q)+\pi_z|Q|\le F(S)
$$

for a suitable terminal choice $z$. Replace each comparison test by its at most three supporting hull tests. This proves that hull-MSSC optimum is at most three times the comparison latency, and that a hull cover exists with at most $3|Q|$ tests.

Weighted MSSC greedy therefore costs at most twelve times the comparison latency. The two-schedule merge gives a first-positive search invoice at most

$$
24\operatorname{MSSC}_{S\setminus\{z\}}(Q)+6\pi_z|Q|
\le24F(S).
$$

Take the best computed terminal choice. If the actual remaining state becomes a singleton, its full pattern can be inferred from the known hypothesis without further queries. No other hypothesis shares that singleton's hull pattern: such a hypothesis would have the same outcomes on the covering spine and would not have been eliminated.

**A negative anchor.** On a positive exit, a known negative vertex is also needed. If $0$ lies on the boundary of $K$, the origin is a free known-negative marker. If $0$ is interior, choose at most three actual vertices whose convex hull contains $0$ and query them. At least one is negative, because three values all greater than one cannot have a convex combination equal to zero. This uses at most three extra tests. Hulls of dimension at most one can be learned by querying at most two actual vertices.

**Entropy-sensitive endpoint search.** Cut the cyclic order at the known-negative anchor. The positive pattern is now an ordinary interval containing the known-positive vertex. Before that vertex, membership is a threshold test for the left endpoint; after it, membership is a threshold test for the right endpoint.

For an ordered random variable $Y$, an alphabetic binary threshold tree has expected cost at most

$$
H(Y)/\ln2+2.
$$

A self-contained existence proof uses the midpoint of each cumulative-probability interval and a dyadic cell of width at most half that interval's probability. Its cell is contained in the interval; these cells are disjoint and ordered, giving a prefix-free alphabetic code of length at most $\log_2(1/\Pr[Y])+2$. Contract unary nodes. An optimal alphabetic tree can also be computed by the ordinary polynomial interval dynamic program.

Learn the left endpoint, then the right endpoint conditioned on the left. The sum of their conditional entropies is the entropy of the positive pattern conditioned on the already observed transcript. Each threshold query is an actual hull test; the origin marker is never queried. Conditional distributions are obtained from the known hypothesis table.

If $P_V$ denotes the hull pattern, the total weighted endpoint invoice is at most

$$
\frac{w(S)H(P_V)}{\ln2}+4w(S).
$$

Since $P_V$ is a function of the hypothesis and costs are one, entropy gives $w(S)H(P_V)/\ln2\le F(S)$. Also $w(S)\le F(S)$ for a nonsingleton state. Including the three anchor queries, the added work is at most $8F(S)$. Together with the first-positive search, this proves the stated factor 32.

All choices are explicit finite menus or polynomial dynamic programs. This lemma does not assume an optimum-code oracle.

Positive full-pattern classes have descriptions using at most four actual test outcomes: their positive interval endpoints and the adjacent negative endpoints. A boundary origin contributes only a free constant, not a query. The all-negative class has at most one hypothesis, because hull replacement preserves coverage of every original cap and the original instance separates all pairs.

### 16.3 A new ambiguity budget

Now suppose $S$ is mass-flat with parameter $\delta<1/3$ and the frozen answers are its mass-majority answers. Every actual hull cap has mass less than $\delta w(S)$.

For any original supplied test $\tau$, choose its at most three supporting hull vertices. A hull-pattern class in which $\tau$ is nonconstant must be positive at at least one of these supporting vertices. Otherwise all supporting values are less than one and convexity forces $\tau$ to have its frozen answer throughout that class.

Hence

$$
\boxed{
\sum_{\substack{A\text{ a hull-pattern class}\\
                  \tau\text{ nonconstant on }A}}w(A)
\le3\delta w(S)
}
$$

for **every** original test. Learning the full hull pattern therefore does more than merely peel a small exit: it leaves each unqueried original test ambiguous on a small total mass.

For an optimal comparison node $v$ with test $\tau_v$ and population $S_v\subseteq S$, its cost remaining after restriction to the pattern classes is at most

$$
\min\{w(S_v),3\delta w(S)\}.
$$

Consequently the total optimal continuation cost is bounded by

$$
\sum_A F(A)
\le
\sum_{v\in T^*_S}
\min\{w(S_v),3\delta w(S)\}
\le
\min\{F(S),3\delta(|S|-1)w(S)\}.
$$

This is a genuine all-test geometric strengthening of a single first-hit cap argument.

It does **not** yet close a constant or smaller-order approximation. The small-mass bound is relative to the **parent** $S$, not the individual comparison node $S_v$. A small comparison subtree may lie entirely in one ambiguous pattern class and retain its whole cost. Replacing the last display by a uniform $O(\delta)F(S)$ contraction would be unjustified.

Summing only the present bound over flat ordinals returns a geometric finite-support tail of the same asymptotic order as the active algorithm. A sharper joint charge for these small optimal subtrees, or a constructive shared-code argument exploiting the four-test outlet descriptions, is still required.

### 16.4 A failed shortcut: cyclic query order

The compact footprints above do not justify forcing the spine queries into cyclic order.

Here is a supplied-line counterexample. Take the rational convex-position points

$$
h_i=(i,i^2),\qquad i=1,\ldots,n,
$$

and the unit-cost lines

$$
y=2ix-i^2+\tfrac14.
$$

The below-line outcome isolates $h_i$; every other point is strictly above. A common above-line witness gives a hull with one private vertex per hypothesis, in the cyclic order of these supporting lines.

Let $n\ge2k$ be divisible by $k\ge4$. Place total probability $1-\varepsilon$ equally on $k$ evenly spaced hull positions, and spread $\varepsilon=n^{-3}$ positively over the remaining hypotheses. Every individual cap has mass below $2/k$, so the state is mass-flat with, for example, $\delta=2/k$ when $k>6$.

A complete certificate must query at least $n-1$ singleton tests. In any cyclic ordering, the heavy targets remain evenly spread; deleting one vertex changes their positions by at most one, and an omitted heavy target waits until the terminal inference. Their average query position is $\Omega(n)$, regardless of the cyclic starting point.

An unrestricted order asks the $k$ heavy singleton tests first and has expected cost at most $k+\varepsilon n=O(k)$. Thus cyclic ordering can lose $\Omega(n/k)$ even in a mass-flat state; taking $k$ of order $\log n$ gives a loss far worse than the current guarantee.

The cyclic-order counterexample remains valid. The subsequent proofs retain arbitrary scheduling and use supporting-prefix credit, rather than the unsupported parent-mass contraction. The current active manuscript establishes constant complete-tree ratios; the preceding discussion describes the historical missing step, not their present status.

## 17. Completed deterministic maximum-depth proof: deadline-priority hull greedy

For every separating finite family of unit-cost supplied-line tests on planar points, there is a polynomial-time deterministic algorithm with

$$
\boxed{\widehat D(S)\le
\left\lceil4D_\infty(S)+6\log_2|S|\right\rceil
\le10D_\infty(S).}
$$

This is a guarantee for the longest path of one deterministic identifying tree. It is not a randomized expected-query statement. With an on-line third outcome, the sign-bit simulation gives factor 20.

The full construction and proof are in the maximum-depth section of [the TeX manuscript](planar-line-decision-trees.tex). The following summarizes the complete charge and the explicit algorithm.

### 17.1 Two real supports and pathwise prefix credit

Use count-balance threshold $\delta=1/8$. In a flat state $S$ of size $s$, Helly gives a strict frozen-answer witness. Normalize all opposite caps and take the dual hull including the origin.

Every original dual point has a representation

$$
u_i=\alpha_i v_i+\beta_i w_i,\qquad
\alpha_i,\beta_i\ge0,\qquad\alpha_i+\beta_i\le1,
$$

using at most two real hull vertices: extend its ray from the origin to a hull edge and scale the edge representation back. Thus negative supporting bits force the original test's frozen answer.

Partition $S$ by its full hull pattern. Every nonzero class $A$ lies in a cap, so $a=|A|<s/8$. The zero class, if present, is a singleton.

On a maximum-depth-optimal witness path, let $t_A$ be the first query whose real supports hit class $A$, or one plus the path length when there is no hit. All preceding queries are constant on the whole class and disappear on restriction. Hence

$$
D_\infty(A)\le D_\infty(S)-(t_A-1).
$$

Replacing each path query by its two hull supports gives a hull ordering hitting every nonzero class by time $2t_A$. If the path's terminal singleton has no supporting hit but has a nonzero pattern, append one positive hull test; its time is at most $2q+1\le2(q+1)$.

### 17.2 A two-speed deadline schedule without an oracle

Assign positive integer deadlines $d_A$. Sort their distinct values as $d^{(1)}<\cdots<d^{(r)}$ and give a class of deadline $d^{(j)}$ the auxiliary weight

$$
(s+1)^{r-j}.
$$

Greedy repeatedly selects the hull vertex hitting maximum remaining auxiliary weight. For any deadline prefix, its score differences are multiples of its smallest weight, while the sum of all later weights is smaller than that smallest weight. Therefore, until a deadline prefix is covered, global greedy is also weighted greedy on that prefix, with legitimate arbitrary tie breaking.

Weighted greedy hitting circular intervals finishes in at most twice minimum cover cardinality. A deadline-feasible ordering supplies a cover of every deadline-$d$ prefix using at most $d$ vertices. Consequently deadline-priority greedy hits every class by time $2d_A$ and finishes all positive hits by time $2\max_A d_A$.

The auxiliary integers have $O(s\log s)$ bits. This is a polynomial greedy schedule, not an assumed minimum-cost continuation oracle.

### 17.3 Use actual child heights and check actual discovery times

Construct the child code on every pattern class first, and record its actual height $\widehat D(A)$. Uniform-count explicit alphabetic endpoint codes give the pointwise pattern-decoding allowance

$$
e_A=\left\lceil\log_2(s/a)\right\rceil+7.
$$

The allowance includes a negative anchor and both endpoints; it does not rely on an expected-depth-optimal code having a pointwise guarantee.

Try the integer budgets $H=1,\ldots,10(s-1)$. Set

$$
u_A=\widehat D(A)+e_A,\qquad
d_A=\left\lfloor\frac{H-u_A}{2}\right\rfloor.
$$

Reject nonpositive deadlines. Otherwise construct the deadline-priority schedule and accept only if its actual first-hit positions satisfy $g_A\le2d_A$ for all nonzero classes. An accepted budget bounds the full code's height: discovery plus endpoint decoding plus the stored child uses at most $2d_A+u_A\le H$. The zero singleton requires at most $2\max_A d_A\le H$ and has no continuation.

### 17.4 Induction closes without multiplying future costs

Let $D=D_\infty(S)$ and $H^*=\lceil4D+6\log_2s\rceil$. By induction and prefix credit,

$$
\begin{aligned}
u_A
&\le4D_\infty(A)+6\log_2a+1+\log_2(s/a)+8\\
&\le4D-4t_A+13+6\log_2a+\log_2(s/a).
\end{aligned}
$$

As $\log_2(s/a)\ge3$,

$$
H^*-u_A\ge4t_A-13+5\log_2(s/a)\ge4t_A.
$$

Thus the trial $H^*$ gives $d_A\ge2t_A$. The supporting expansion is a deadline-feasible comparison ordering, so the actual greedy checks pass.

At a balanced state, each child has size at most $7s/8$ and conditional optimum height at most $D$. Since $6\log_2(8/7)>1$, the logarithmic-size potential pays for the one balanced query, including ceiling rounding.

Finally $\log_2s\le D\le s-1$ gives $H^*\le10D\le10(s-1)$, so a passing budget is always searched. Children at every stage are disjoint proper subsets; the stage hierarchy has at most $n-1$ nonterminal nodes. Geometry, integer-weight greedy schedules, actual-height checks, and uniform-count endpoint-code construction all take polynomial time.

This proof is specific to the planar supplied-line model and uniform query costs. It does not establish a constant approximation for arbitrary nonuniform costs or arbitrary nongeometric test tables. Literature-wide priority is not asserted.

## References and connections to the existing notes

- Ray Li, Percy Liang, Stephen Mussmann, *A Tight Analysis of Greedy Yields Subexponential Time Approximation for Uniform Decision Tree*, [arXiv:1906.11385v2](https://arxiv.org/abs/1906.11385v2); [supplied local paper](1906.11385v2.pdf).
- Daniel Golovin, Andreas Krause, *Adaptive Submodularity: Theory and Applications in Active Learning and Stochastic Optimization*, [corrected v5](https://arxiv.org/abs/1003.3967v5).
- Hessa Al-Thani, Yubing Cui, Viswanath Nagarajan, *Minimum Cost Adaptive Submodular Cover*, [v2](https://arxiv.org/abs/2208.08351v2), Theorems 1.5--1.6, Lemmas 2.5--2.6, and the UDT application.
- Fatemeh Navidi, Prabhanjan Kambadur, Viswanath Nagarajan, *Adaptive Submodular Ranking and Routing*, [v2](https://arxiv.org/abs/1606.01530v2), Sections 2 and 4.4.
- Uriel Feige, Laszlo Lovasz, Prasad Tetali, *Approximating Min-sum Set Cover*, [primary journal manuscript](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf), Theorem 4 and its price/histogram proof.
- Nikhil Bansal, Jatin Batra, Majid Farhadi, Prasad Tetali, *Improved Approximations for Min Sum Vertex Cover and Generalized Min Sum Set Cover*, [arXiv:2007.09172v1](https://arxiv.org/abs/2007.09172v1), the time-indexed LP and kernel-rounding sections.
- Daniel Golovin, Andreas Krause, Debajyoti Ray, *Near-Optimal Bayesian Active Learning with Noisy Observations*, [v2](https://arxiv.org/abs/1010.3091v2), the EC2 edge-cutting objective.
- Siddharth Bhaskar, *Thicket Density*, [arXiv:1702.03956v4](https://arxiv.org/abs/1702.03956v4), Theorem 4.1; Journal of Symbolic Logic 86 (2021), 110--127, [DOI:10.1017/jsl.2020.55](https://doi.org/10.1017/jsl.2020.55). Used for the sequential tree-growth principle, not for a UDT approximation theorem.
- [Original research agenda](uniform-decision-tree-research-note.md).
- [Formal refinements and earlier proof attempts](uniform-decision-tree-formal-bounds.md).
- [Tradeoff refinements, cutoff barrier, and retained-state construction](uniform-decision-tree-improved-tradeoffs.md).
