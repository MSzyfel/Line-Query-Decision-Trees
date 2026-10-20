# Arbitrary cardinality profiles on one hierarchy

Auxiliary research note, 18 October 2026. This does not change the article and does not establish the requested unrestricted approximation improvement.

The earlier weighted restriction potential loses a factor of order `log n / log log n` even on a coordinate cube. A root entropy profile repairs that particular obstruction. This motivates optimizing arbitrary cardinality profiles on an entire supplied hierarchy rather than scaling its original node contributions.

Fix a binary identifying tree `T`, with hypothesis cluster `H_v` at internal node `v`. Introduce nonnegative rational variables `g_v(s)` for `2 <= s <= |H_v|`, with `g_v(0)=g_v(1)=0`, and define

    P(S) = sum_v g_v(|S intersect H_v|).

Maximize `P(H)` subject to every supplied test `q` and every subset `S` satisfying

    P(S) - P(S intersect q) - P(S minus q) <= |S|.             (1)

Telescoping (1) down any executable identifying tree proves `P(S) <= F_OPT(S)`. Thus the objective is a lower certificate for the original supplied-test problem. A profile need not be monotone, convex, or individually satisfy a Bellman inequality.

For a fixed query, color hypotheses by its two responses. A bottom-up DP keeps the maximum deficit for each pair `(r,b)` of selected color counts in a hierarchy subtree. Convolve the two child tables and add

    g_v(r+b) - g_v(r) - g_v(b).                               (2)

The local contribution can be negative. Store unreachable counts as minus infinity; keep negative reachable optima. Once the child counts are fixed, ancestors cannot distinguish two subsets with those counts, so retaining the larger score is exact. At the root maximize score divided by `r+b>0`; a value above one gives a violated capacity and a reconstructible witness subset.

There are `O(n^2)` variables and a direct polynomial number of rational DP operations. For fixed response bound `K`, replace the count pair by a `K`-tuple, giving `n^{O(K)}` time. The harmless coordinate bounds

    0 <= g_v(s) <= s(s-1)

follow from nonnegative features, (1), and a proper identifying tree of height at most `s-1`. Consequently exact rational separation yields a genuine polynomial LP optimization algorithm via the [separation/optimization theorem of Groetschel, Lovasz, and Schrijver](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1981a.pdf). The accompanying floating simplex and cut loop is **small-instance validation**, not an implementation of that polynomial theorem.

The validator converts its candidate to rational numbers and computes the exact maximum violation ratio `beta` using the separator. Scaling by `1/max(1,beta)` gives a rigorously feasible lower certificate, independently of floating tolerances or numerical optimality. Independent audit files also save rational primal and repaired dual certificates on selected examples.

The family includes the unrestricted binary coding lower bound as a root profile:

    L_2(0)=L_2(1)=0,
    L_2(s)=s(ceil(log2 s)+1)-2^{ceil(log2 s)}  for s>=2.

A root query followed by optimal unrestricted child codes proves `L_2(a+b) <= a+b+L_2(a)+L_2(b)`. If every designated positive test side has at most `B` hypotheses, the analogous count recurrence with `1<=a<=min(B,s-1)` is also feasible. Its minimizing splits are abstract lower bounds and need not be supplied tests.

Completed root validation: 514 exhaustive rational-profile/query comparisons against all subsets, and exact feasible certificates of 24, 35, and 30 on the eight-point cube, eight singleton tests, and affine `Q=3,d=2` family. Each equals its exact optimum. The audit establishes that all three values are already obtainable by root-only profiles; they do not demonstrate an advantage from the laminar sum.

The independent [audit](research-general-laminar-profile-audit.md) extends the separator to weighted restriction features on the **same** hierarchy and gives a certified quality gap. For eight hypotheses with test masks `[4,10,86,92,190,212,214]`, greedy raw cost is 26 and true optimum is 25, while both the arbitrary-profile cone and the combined same-hierarchy cone have exact value 24. Exact primal/dual certificates establish these LP values. This is a fixed-instance expressiveness gap, not an asymptotic lower bound. Crossing hierarchies are outside the separator theorem.

Root-only profiles retain a large affine obstruction. With `n=Q^d` and all affine equality tests, capacities allow abstract peeling of blocks of `n/Q`, followed by unrestricted coding in each block. Therefore a root-only profile has value at most `O(nQ+n log n)`, versus actual optimum `Theta(nQd)`. In the regime `Q=Theta(log n)`, this is the full target-order gap. This statement does not bound the entire laminar-profile cone.

The unresolved question is whether a polynomially generated hierarchy, its profile LP, and the executable code library obey a useful certificate-or-policy alternative. No rounding theorem or universal comparison has been proved. An attempted larger numerical LP was stopped without a certificate and is not included among results.

Implementation and validation: [separator and finite optimizer](research-general-laminar-profile.py), [root results](research-general-laminar-profile-results.json), and the independent audit, checker, and exact certificate files linked above.
