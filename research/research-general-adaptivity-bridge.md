# An adaptivity bridge through palette complexity

Auxiliary research note, 18 October 2026. The article is unchanged.

**Status.** The palette-based entropy drift bound is valid, including its final step. It gives a polynomial `O(log log n)` approximation on the promised class whose minimum identifying palette has size `O(OPT_mean)`. A stronger decomposition theorem also permits arbitrary high-adaptivity balanced routing before such regions. Neither promise is universal. Explicit threshold and gated-code families delimit the proposed decomposition. A separate example proves that even optimal restriction credit can be constant for a perfectly balanced supplied test.

## 1. Palette complexity and an entropy-greedy bound

For a hypothesis subset `S`, let `D(S)` be the smallest number of original tests whose **complete response vectors** distinguish every hypothesis in `S`. This is a cardinality parameter of an identifying nonadaptive palette. It is not the expected cost of an optimally ordered nonadaptive list with early stopping. Querying all tests of a supplied palette does identify its ambient set in at most its cardinality, but here the palette attaining `D(S)` need not be known.

Use the polynomial entropy-greedy algorithm: at a current uniform candidate set `A`, choose a supplied test maximizing the entropy of its responses. For binary tests this is exactly the usual most-balanced split, so selection uses only integer counts. For any number of outcomes it can still be implemented exactly in polynomial time: maximize

    log |A| - (1/|A|) sum_a |A_a| log |A_a|

by minimizing the integer product `prod_(a:|A_a|>0) |A_a|^|A_a|`. Its bit length is `O(|A| log |A|)`. This avoids an assumed exact-real logarithm oracle.

**Proposition.** For a uniform ambient set of `n>=2` hypotheses,

    E[greedy queries] <= D(H) [1+ln(log2 n)].                 (1)

In particular, if `D(H)<=r OPT_mean`, greedy has approximation ratio at most `r[1+ln(log2 n)]`, with no need to discover that palette. For fixed `r`, this is `O(log log n)`, smaller than the unrestricted target order. This is an elementary structural consequence, with no novelty claim for the drift argument.

To prove it, fix any identifying palette of `D` tests. At any candidate set `A`, its response vector still identifies the uniform target. Entropy subadditivity gives

    log2 |A| <= sum_(q in palette) H(q|A)
             <= D max_q H(q|A).                             (2)

Let `X_t=log2 |A_t|` on an actual random greedy execution. The expected decrease at an unfinished state is exactly the response entropy, so

    E[X_t-X_(t+1)|A_t] >= X_t/D.                            (3)

The final step needs care. Nonzero values of `X_t` are at least one because the posterior is uniform on a set of at least two hypotheses. Define `f(0)=0` and `f(x)=1+ln x` for `x>=1`. For `x>=1` and either `y=0` or `1<=y<=x`,

    f(x)-f(y) >= (x-y)/x.

For positive `y` this is `ln(x/y)>=1-y/x`; for `y=0` it follows from `f(x)>=1`. Equations (2)-(3) therefore imply expected `f`-decrease at least `1/D` per unfinished query. Summing to the finite stopping time proves (1). Proper queries imply height at most `n-1`, so no convergence assumption is hidden.

The proof works for fixed `K` responses, and in fact for an explicitly listed arbitrary response alphabet. Uniformity supplies the positive-state threshold `X>=1` used above.

## 2. Balanced routing can be charged before low-palette regions

For binary tests, fix `0<eta<=1/2`. In the actual greedy tree, retain the maximal root prefix for which every executed split has minority population at least `eta` times its current population. Stop that prefix at its first unbalanced states; call the non-singleton frontier cells `A_i`. Singleton frontier cells contribute zero below.

Write `s_i=|A_i|`, `D_i=D(A_i)`, and let `W_bal` be the prefix's raw work. The usual entropy telescope gives

    W_bal <= [n log2 n - sum_i s_i log2 s_i]/h2(eta),        (4)

because every executed query has response entropy at least `h2(eta)`. Apply (1) independently **after actually reaching** each frontier cell. The rest of the same greedy tree costs at most

    sum_i s_i D_i [1+ln(log2 s_i)].                         (5)

Equations (4)-(5) are an actual decomposition of one executable tree. There is no membership query assumed, no context activated for free, and no independently reset entropy budget.

Consequently, if the weighted palette budget at this actual frontier satisfies

    sum_i s_i D_i <= r OPT_raw(H),                          (6)

then

    greedy_raw <= {1/h2(eta)+r[1+ln(log2 n)]} OPT_raw(H).     (7)

One sufficient version of (6) is `D_i<=r OPT_mean(A_i)` for every frontier cell: restricting one global optimum to disjoint cells proves `sum_i OPT_raw(A_i)<=OPT_raw(H)`.

This is broader than a small global identifying palette. The balanced prefix may have arbitrarily high adaptivity and arbitrarily many distinct queries. The algorithm remains ordinary polynomial entropy greedy; `D_i` and the condition (6) are used only in its guarantee. No polynomial procedure for verifying (6) in unrestricted instances is supplied.

If identifying palettes of cardinalities `D_i` are explicitly supplied instead, executing them on their already activated frontier cells has cost at most `sum_i s_iD_i`. This yields a constant bound under (6), but finding the required palettes is then an additional algorithmic obligation. The exact logarithmic-palette optimizer from `research-general-lifting-global.md` can process supplied small palettes without resetting shared query histories.

## 3. High adaptivity need not be confined to narrow chains

Consider ordered hypotheses `1,...,n` and all threshold tests `1[h<=j]`, for `j=1,...,n-1`. Each adjacent pair `j,j+1` is separated by only its own threshold. Hence

    D(H)=n-1.

For `n` a power of two, median threshold search is the complete balanced tree, with `OPT_mean=log2 n`; entropy greedy is exactly optimal. Thus the palette/adaptive-mean ratio is `Theta(n/log n)`, while every chosen query is maximally balanced.

The same phenomenon occurs inside **every** subset `C` of size `s`. Its `s-1` adjacent pairs in sorted order require threshold choices from disjoint intervals, so `D(C)=s-1`; median search attains the unrestricted optimal binary coding cost `L_2(s)`. Large cores therefore do not become low-palette simply by conditioning. For fixed `r`, `D(C)<=r OPT_mean(C)` forces `s=O(r log(2r))`.

High palette complexity in this family occupies the full balanced branching tree. In the perfect tree there are `n-1` internal nodes but a chain has only `log2 n` internal nodes; covering these nodes by chains requires at least `(n-1)/log2 n` chains. Thus a proposed universal reduction to low-palette regions plus a *small collection* of narrow high-adaptivity chains is false without a separate balanced-routing case. The decomposition in Section 2 includes that case.

This standard ordered-search example is used as a structural obstruction, not a new adaptivity-gap result. The distinction between adaptive decision trees and nonadaptive lists is discussed, for example, in the primary paper [Gupta, Nagarajan, and Ravi, Approximation Algorithms for Optimal Decision Trees and Adaptive TSP Problems](https://www.contrib.andrew.cmu.edu/~ravi/adaptive-mor17.pdf).

## 4. The weighted palette budget is not universal either

Let `H=[C] times {0,1}^b`, with `r=2^b` words in each column. Supply each column-membership query and each binary word coordinate gated to one column. The latter is positive exactly on hypotheses in that column with the chosen word bit one. There are no global word-coordinate queries.

Every one of the `Cb` gated bit tests is necessary in an identifying palette: in a fixed column, the all-zero word and its one-bit neighbor are separated by only that bit's gated query. In addition, the `C` all-zero words require at least `C-1` column-membership queries. These choices suffice, so

    D(H)=Cb+C-1.                                            (8)

The adaptive mean is `Theta(C+b)`. A sequential search for the column followed by its bit code gives the upper bound. Entropy gives `Omega(b+log C)`, and the global minority support bound `B=r` gives `OPT_mean>=(n-1)/(2r)=Omega(C)`. The latter follows directly from the feasible cardinality potential `P(S)=|S|(|S|-1)/(2r)`: a query splitting sizes `a,b`, with one side at most `r`, has deficit `ab/r<=|S|`.

Take `C=b` growing. Then `D/OPT_mean=Theta(b)=Theta(log n)`, and every root query has minority fraction at most `1/C`, so the unbalanced frontier of Section 2 is the root for every fixed `eta`. Condition (6) fails with constant `r`.

This is not a bad-greedy construction: column-membership queries already expose a good chain. It isolates the missing additional case. Cheap min-sum-style activation may coexist with a very large identifying palette, even at an unbalanced root. The general decoder problem is to find and compose those activation chains with useful conditional codes. The bounds above do not solve it, and the known arbitrary-grid failures of simple local insertion remain relevant.

## 5. Even optimal restriction credit need not pay balanced-output entropy

Let `A={a_1,...,a_r}` and `B={b_1,...,b_r}`, with `r>=3`. Supply the class-membership test `A` and, for every `i,j`, the binary test whose positive set is

    {a_i} union (B minus {b_j}).

All supplied tests are balanced on `H=A union B`.

Within either class every nonconstant query is a singleton split or its complement. Thus its exact optimum is

    f(r)=r(r+1)/2-1.

After any mixed test at the full root, each size-`r` child consists of one exceptional hypothesis from one class and `r-1` ordinary hypotheses from the other. Let `g(s)` be the optimum on such a state of size `s`. Its nonconstant query types isolate an ordinary singleton, the exceptional singleton, or a pair consisting of the exception and one ordinary hypothesis. Therefore

    g(1)=0, g(2)=2,
    g(s)=s+min{g(s-1), f(s-1), 2+f(s-2)}, s>=3.

The singleton formula uses `f(0)=f(1)=0`. Induction gives

    g(s)=f(s)-s+3, s>=3.

At the full root, a mixed test costs `2r+2g(r)=2f(r)+6`. The class test costs `2r+2f(r)` and cannot improve it. Hence

    OPT_raw(H)=2f(r)+6,
    OPT_raw(H)-OPT_raw(A)-OPT_raw(B)=6.                     (9)

The supplied class-membership test has raw output entropy `2r`, but its optimal restriction credit is the constant six. In particular, no universal positive constant can lower-bound optimal restriction credit by output entropy, even for uniform binary unit-cost instances and a perfectly balanced supplied test.

This also explains why (4) and the conditional-OPT budget are kept as separate global lower ledgers in (7). Replacing their sum by an assumed entropy-plus-restriction lower bound is invalid. The example does not refute the mixed contraction theorem: that theorem explicitly telescopes the two resources separately.

## 6. What is proved and what remains missing

The positive polynomial guarantee is (1), or (7) under the stated actual-frontier palette budget. Its runtime does not depend on finding a minimum palette. The explicit palette algorithms remain polynomial only for a polynomial supplied list of logarithmic-size palettes; they do not enumerate all such test subsets.

The threshold example requires balanced high-adaptivity routing. The gated example additionally requires unbalanced activation chains whose conditional code families can have high total palette complexity. A universal bound must charge those real activations and preserve reusable conditional code information. Neither low global palette size nor the budget (6) is universal, and no unrestricted approximation improvement is asserted.

`research-general-adaptivity-bridge.py` checks the entropy subadditivity and last-step drift on small instances, the hybrid frontier inequalities, the threshold palette obstruction, and the exact constant-credit family. Its exhaustive palette search and exact subset optimization are finite validation oracles only; neither is used by the polynomial entropy-greedy algorithm.
