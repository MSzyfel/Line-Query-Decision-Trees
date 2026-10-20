# General uniform decision trees: what transfers from shallow planar caps

Research auxiliary note, 18 October 2026. The article is unchanged. All statements below concern uniform hypotheses, unit-cost supplied tests, and polynomial time for fixed parameters. “Proved here” means the argument is supplied in this note; it does not assert literature novelty.

The unrestricted target remains open: this investigation does **not** prove an `o(log n / log log n)` approximation for arbitrary test systems. It proves a geometry-free separator transfer, extends it to a virtual all-miss pattern, and identifies a strong obstruction to replacing geometric locality by bounded overlap.

## 1. Context read and retained

I read `sections/06h-uniform-bounded-cap-ptas.tex`, `uniform-cap-ptas-audit.md`, the uniform and weighted pair discussions in `direction5-robust-gadget-hardness.md` and `direction6-pair-forest-ptas.md`, the model and baseline in `uniform-decision-tree-research-note.md`, and Theorem 3.1, Proposition 3.3, and the balanced/imbalanced chain analysis of the supplied `1906.11385v2.pdf` (extracted in `tmp/pdfs/general-1906-v2.txt`).

The supplied paper's greedy guarantee is `O(log n / log OPT)`; its binary greedy examples match that dependence up to constants. Thus a cap subclass with `OPT = Omega(n)` already has a constant approximation. Improving that subclass to a PTAS is structural progress, but does not address the difficult low-optimum general instances.

The exact maximum-matching result for arbitrary uniform caps of size two, including absent singleton queries, was already proved in the local direction-5 note. It is not a new result of this investigation.

## 2. A separator transfer for arbitrary supplied binary tests — proved here

Let the hypotheses be `P union {p}`, with `|P| = N`, and orient every supplied binary test so that its positive cap `C` excludes `p`. Suppose `|C| <= b`. The family separates all hypotheses. No planar representation, cyclic order, or singleton tests are assumed.

Form the **interaction graph** `J` on `P`: two hypotheses are adjacent exactly when some supplied cap contains both. Suppose a polynomial procedure provides a set `D subseteq P`, of size `r`, such that every component of `J-D` has at most `L` vertices. For fixed `b,L`, there is a polynomial algorithm with raw expected-depth cost

```
G_alg <= OPT_G + r (N+1+b(b-1)),

G_alg / OPT_G <= 1 + [2 b r / N] [1+b(b-1)/(N+1)].                 (1)
```

When `N+1 >= b(b-1)`, the simpler ratio is `1+4br/N`.

### Legal clearing prefix

Follow the all-miss route. While a marked hypothesis `x in D` remains, ask any supplied cap containing `x`; such a cap exists by separation from `p`. Its current positive group has at most `b` hypotheses. Identify that group with a supplied local tree of height at most `b-1`, then continue on the miss branch. At most `r` spine queries occur. Their raw contribution is at most `r(N+1)`; their disjoint positive groups contain at most `br` hypotheses and contribute at most `b(b-1)r` further raw cost. Collateral removals are allowed and only help.

After clearing, every nonempty residual cap lies inside one component of `J-D`: all pairs of vertices of the cap are adjacent. Collateral removal cannot destroy this locality. Therefore residual components are independent bounded-size blocks in precisely the sense needed by the planar count-vector method.

### Exact residual optimization, with the larger nongeometric type count

For a block `B`, relabel its `s <= L` vertices by `[s]`. Its type consists of `s` and the family of nonempty supplied cap masks restricted to `B`. Store a realizing physical query for every mask. Different blocks with the same type and same live subset are interchangeable because every surviving query misses every other block.

Put

```
t(b,L) = sum_{j=1}^{min(b,L)} binomial(L,j),
d(b,L) = L 2^{t(b,L)+L}.
```

There are at most `d(b,L)` type/live-mask pairs: for each block size, there are at most `2^{t(b,L)}` mask families and `2^L-1` nonempty live masks. This replaces the planar interval count `2^{(b+1)L}`. For unrestricted local masks one may use the looser `L 2^{2^L+L}` bound. Both are constants only when `b,L` are fixed.

For type `T`, let `g_T(A)` be the exact raw identification cost on local subset `A`, found by subset Bellman optimization using the supplied local masks. Let `c_(T,R)` count blocks in local state `(T,R)` and `W(c)=1+sum c_(T,R)|R|`. Then

```
F(0) = 0,
F(c) = W(c) + min_{c_(T,R)>0, q in F_T, A=R intersect q nonempty}
              [g_T(A) + F(c-e_(T,R)+e_(T,R\A))].                 (2)
```

Every proper residual root query hits one block; its positive branch has cost at least `g_T(A)` and its miss branch changes exactly one block state. Conversely, the stored physical query realizes every transition, and exact local trees realize its positive branches. Induction on the number of live nonwitness hypotheses proves equality. This includes all interleavings between blocks.

There are at most `(N+1)^{d(b,L)}` count states. Each tries a constant number of transitions for fixed `b,L`. Input preparation and physical-query reconstruction are polynomial. A bound is `f(b,L) (N+1)^{d(b,L)} poly(N,m)` with polynomial bit complexity. This is a PTAS-style polynomial exponent; it is not claimed to be an EPTAS.

### Charging

Restrict a full optimum tree to the surviving hypotheses and suppress constant queries. Its raw cost cannot increase, so the exact residual optimum is at most `OPT_G`. On the original witness path, the first `j` queries remove at most `bj` nonwitness hypotheses. Consequently

```
OPT_G >= sum_{i=1}^N ceil(i/b) >= N(N+1)/(2b).                    (3)
```

Adding the prefix estimate and dividing by (3) gives (1). These arguments contain no geometric assumption.

### Fixed numbers of responses

The whole theorem extends to tests with at most fixed `K` responses. Relabel each test's witness response as `0`, and assume the union of its other outcome classes contains at most `b` hypotheses. Use that union as its support in `J`. A local test type is now a map to `[K]` with at most `b` nonzero positions. The number of possible nonconstant local maps is at most

```
t_K(b,L) = sum_{j=1}^{min(b,L)} binomial(L,j) (K-1)^j,
```

so one may use `d_K(b,L)=L 2^{t_K(b,L)+L}` in the exponent. In (2), set `A_a={x in R:q(x)=a}` and replace `g_T(A)` by `sum_{a!=0} g_T(A_a)`, while the miss transition removes `union_{a!=0} A_a`. The local Bellman tables also sum over all outcomes. A clearing query removes at most `b` nonwitness hypotheses in total, and every positive continuation still has height at most `b-1`. Thus all charging constants and separator corollaries remain valid. The checker currently covers the binary specialization.

## 3. Strongly sublinear separators give polynomial PTASs — proved here

Assume every induced subgraph of `J` with `s` vertices has a polynomially findable vertex separator of size at most `c s^{1-alpha}`, leaving components of size at most `beta s`, for fixed `0<alpha<=1` and `0<beta<1`. Recurse only on components larger than `L`.

The union `D` of removed separators satisfies

```
|D| <= C N / L^alpha,       C = c/(1-beta^alpha).                 (4)
```

To prove this, group recursion nodes by sizes in `(beta^{-j}L, beta^{-j-1}L]`. Within each group they form an antichain: a child is smaller than the group's lower endpoint. Their vertex sets are disjoint, so their total size is at most `N`. The sum of separator sizes in group `j` is at most `c N beta^{j alpha}/L^alpha`. Sum the geometric series. This proof permits arbitrary numbers of components per separator.

For `N+1 >= b(b-1)`, choose fixed

```
L >= (4 b C / epsilon)^{1/alpha}.
```

Equations (1) and (4), followed by exact count DP, give a `(1+epsilon)` approximation. Smaller instances can be solved exactly because the relevant cutoff depends only on fixed parameters. Thus this is a polynomial PTAS for arbitrary supplied test systems whose support interaction graphs have the stated separator property. Planar and fixed-minor graph theorems can be plugged into this statement when their constructive separator hypotheses are supplied; no geometric realization of the tests is needed.

### Explicit bounded-treewidth corollary

Given a width-`t` tree decomposition, a bag of at most `t+1` vertices is a weighted-centroid separator with `beta=1/2`. Assign each graph vertex to one containing bag, take a centroid of the decomposition tree under those vertex weights, and remove its bag. Each surviving graph component lies on one side of that bag and has at most half the graph's vertices. Restriction gives the same construction recursively.

Hence `|D| <= 2(t+1)N/L`, and choosing

```
L >= 8 b(t+1)/epsilon
```

gives a PTAS for fixed `b,t`, with the count-DP exponent stated above. Supplying the decomposition avoids importing a treewidth-recognition algorithm as an unproved primitive.

The same conclusion holds when a fixed-width decomposition of the **bipartite cap-incidence graph** is supplied and `b` is fixed. Replace every test vertex appearing in a bag by all at most `b` hypotheses of its cap. A width-`s` incidence decomposition becomes an interaction decomposition of width at most `b(s+1)-1`. The bags containing a hypothesis stay connected: its original bag subtree meets each incident test's subtree in a bag containing their incidence edge.

## 4. A virtual all-miss pattern is enough asymptotically — proved here

Suppose there are `n` original hypotheses and every binary test has an oriented positive side of size at most fixed `b`, but the all-negative answer string need not be an actual hypothesis. The interaction graph is still formed from these oriented positive supports.

If an all-negative hypothesis already exists, use it as the witness. Otherwise add one artificial all-negative hypothesis `p`. It is separated from every original hypothesis because each original hypothesis has at least one positive answer.

For any original proper tree `T`, follow negative answers until its terminal leaf `h`. This route has at most `n-1` queries. Add at that leaf one supplied query positive on `h`, distinguishing `h` from `p`. No other original route changes. The original hypothesis `h` receives one additional query, and the new hypothesis has depth at most `n`. Therefore

```
OPT_G(original) <= OPT_G(augmented) <= OPT_G(original)+n+1.       (5)
```

The lower bound in the original system is

```
OPT_G(original) >= sum_{i=1}^{n-1} ceil(i/b)
                >= n(n-1)/(2b).                                (6)
```

Indeed, all but the terminal hypothesis first leave the negative route through groups of size at most `b`. An actual witness is needed to charge *every* nonwitness point as in (3), but dropping one terminal hypothesis gives (6).

For a requested `0<epsilon<=1`, run an augmented-system PTAS at accuracy `epsilon/3`, then restrict its output to the original hypotheses. If `n-1 >= 12b/epsilon`, equations (5)-(6) give augmentation inflation at most `1+epsilon/3`; the product is at most `1+epsilon`. Below this cutoff, solve exactly. Thus every separator PTAS above extends to a virtual common default pattern.

For a fixed number of outcomes the same bounds hold when the *union* of all nondefault outcomes has size at most `b`. There is one additional case: the default route might encounter an internal test whose default outcome is absent among the current original hypotheses. Attach the dummy leaf to that absent outcome; no original depth changes and the dummy depth is at most `n-1`. Otherwise use the terminal-leaf graft above. For the rank lower bound, an absent default outcome removes every remaining original hypothesis through at most `b` nondefault hypotheses at that last query, which is at least as strong as (6). The multioutcome count recurrence is described in Section 2.

## 5. Bounded cap overlap alone cannot provide a PTAS — proved reduction

There is no polynomial PTAS for arbitrary uniform binary cap systems with caps of size at most **three**, even when each nonwitness hypothesis lies in at most **two** distinct supplied caps, unless `P=NP`.

The source fact is classical: the proof of Theorem 14 in [Feige–Lovász–Tetali, Approximating Min-sum Set Cover](https://tetali.math.gatech.edu/PUBLIS/mssc_final.pdf), pp. 15–16, preserves the source graph's maximum degree by adding only isolated edges. Its stated degree-three vertex-cover hardness is supported directly by Theorem 3.1 of [Alimonti–Kann, Hardness of Approximating Problems on Cubic Graphs](https://cs.yale.edu/homes/aspnes/pinewiki/attachments/MarkovChains/alimanti-mis-cubic.pdf). Thus bounded-degree-three min-sum vertex cover has no PTAS. This is the only imported hardness fact in the transfer below.

Here is the objective-preserving transfer. Given a simple graph `G=(V,E)` of maximum degree `d`, remove isolated vertices and let `N=|E|`. Create one hypothesis per edge plus one all-negative witness. For each graph vertex `v`, supply the binary cap of incident edge hypotheses. Every cap has size at most `d`; every edge hypothesis belongs to exactly two caps. The tests separate hypotheses because distinct simple edges have distinct endpoint sets.

An isolated graph edge has two identical named singleton tests; these may be coalesced, giving frequency one rather than two. Thus the statement uses *at most* two distinct caps, without relying on duplicated test names.

Let `L*` be the minimum sum of first cover times of graph edges under a vertex ordering, and let `F*` be the raw optimum of this uniform decision-tree instance. Then

```
L* <= F* <= L* + (d-1)N + |V|,
L* >= N(N+1)/(2d),       |V| <= 2N.                              (7)
```

For the lower bound, extract the decision tree's all-negative witness spine. It queries a sequence of graph vertices covering every edge; append unused vertices to obtain a permutation. Every edge's leaf depth is at least its first cover time. For the upper bound, execute an optimal cover ordering on the witness spine, discarding zero-gain queries, identify each positive group with a supplied local tree of height at most `d-1`, and use at most `|V|` witness queries. Equation (7)'s rank bound is the same capacity argument as (3).

Given a `(1+delta)` decision-tree solution, its extracted vertex ordering has latency at most

```
(1+delta) [1+2d(d+1)/(N+1)] L*.                                 (8)
```

For any desired MSSC accuracy, choose constant `delta` sufficiently small and solve the finitely many cases below the corresponding constant threshold on `N` exactly. A decision-tree PTAS would therefore imply a min-sum vertex-cover PTAS at maximum degree three. Set `d=3` for the claimed cap-size-three, frequency-two obstruction.

No quantitative lower bound near two or four follows from this reduction. It only rules out arbitrarily accurate approximation in this restricted class. The cap-size-two exact matching result and the cap-size-three obstruction explain why planar locality is a real algorithmic resource rather than a convenient picture.

### A separate obstruction to clearing almost all interactions cheaply

Even cap size two does not ensure a small deletion `D`. Supply every singleton cap and every pair cap on `N` vertices. Then `J` is complete, so making residual components have size at most `L` requires `|D| >= N-L`. More sparsely, in a maximum-degree-`Delta` graph with edge expansion at least `h` for sets of size at most `N/2`, any deletion leaving components of size at most `L<=N/2` satisfies

```
h (N-|D|) <= Delta |D|,
|D|/N >= h/(Delta+h).
```

Sum the expansion boundaries of the residual components; all such boundary edges end in `D`. Thus fixed bounded support and even bounded graph degree cannot guarantee the arbitrarily small deletion fraction needed for this transfer. This is a limitation of the localization technique, not a hardness proof: cap-two instances themselves have the old exact matching algorithm.

## 6. Bounded positive frequency already gives a constant approximation

This is a separate positive consequence of the supplied Li–Liang–Mussmann greedy theorem. It requires no bound on support size and no separator. Its underlying greedy approximation theorem is inherited, not claimed as new.

For each test choose a default outcome and relabel it `0`. Suppose every hypothesis has a nondefault answer on at most `f>=1` supplied tests. The default pattern may be virtual. Let `K>=2` be the maximum number of responses and let `D=OPT_G/n` be optimal mean depth. Then

```
n/2 <= sum_{j=0}^{min(f,floor(2D))}
          binomial(floor(2D),j) (K-1)^j
    <= [1+2(K-1)D]^f,

D >= [(n/2)^{1/f}-1] / [2(K-1)].                                (9)
```

At least half of the hypotheses have optimal depth at most `2D`. Their response words are prefix-free. Extend each by zeros to length `floor(2D)`; extension is injective, since one original leaf word cannot be a prefix of another. A proper tree never repeats a test on one route, so each word has at most `f` nonzero symbols. Counting their positions and labels gives the first inequality. For `x>=0`, `sum_{j<=f} x^j/j! <= (1+x)^f`; apply `binomial(d,j)<=d^j/j!` to obtain the second inequality. This proves (9) without a real witness.

For fixed `f,K` and growing `n`, (9) gives `log D >= (log n)/f-O_K(1)`. Thus Theorem 3.1 of the supplied paper gives a polynomial `(12+o(1))f` approximation; its improved uniform leading constant gives `(4+o(1))f`. More generally the same greedy algorithm has an `O_K(f)` guarantee for every `n`, in addition to its unrestricted bound:

```
ratio <= min{ O(log n/log log n), O_K(f) }.
```

For an explicit all-size constant, put `A=8(K-1)`. If `n>=A^{2f}`, (9) implies `D>=n^{1/f}/A`, and the paper's factor is at most `24f`. If `K^2<=n<A^{2f}`, the entropy bound gives `D>=2`, so its factor is at most `12 log_2 n < 24f log_2 A`. Finally, when `n<K^2`, any proper tree has mean at most `n-1` and optimum at least one, so its ratio is at most `K^2 f`. These cases give an explicit `max{24 log_2(8(K-1)),K^2}f` bound, with harmless small-instance handling when `n=1`.

The frequency condition is polynomially checkable for a supplied choice of defaults. It is enough to have hypotheses close in Hamming distance: choose any hypothesis's complete response string as defaults; a Hamming diameter of at most `f` gives the required frequency bound. Hence constant Hamming diameter is another geometry-free constant-approximable class, even with arbitrarily large positive supports. If `f=o(log n/log log n)`, this instance class already has a little-`o` ratio. No assertion is made that arbitrary uniform test systems admit such defaults or a reduction to this class.

## 7. Verification and remaining target

`research-general-caps.py` compares an independently written full adaptive subset Bellman oracle with the graph-incidence invoice and with the post-clearing count-vector quotient. The run passed:

* 558 simple degree-at-most-three graph-incidence instances, exhaustive through five graph vertices;
* 271 random separating cap systems, with actual supplied-query clearing and collateral removals;
* the virtual-default augmentation and rank bounds on those same 271 systems;
* among those, 102 families without supplied singleton queries and 53 with multiple retained blocks.

The checks confirm the finite identities and inequalities used in (1), (2), and (7). They do not establish computational hardness, literature novelty, or an improved general ratio.

The general problem needs a mechanism beyond bounded overlap, bounded exceptional support, or clearing a sparse set of graph interactions. One concrete next target is to find a polynomially computable decomposition whose clearing cost is charged to *local optimum mass* at several scales while continuation optimization retains interactions between blocks. The separator theorem solves the case where such interactions can actually be removed at a small global charge. No proof handles the dense low-optimum instances where this charge ceases to be small.
