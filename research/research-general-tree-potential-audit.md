# Audit of weighted restriction potentials of one fixed tree

Auxiliary research note, 18 October 2026. The article is unchanged.

**Status.** The supplied separation implementation passed an independent rerun: 864 exhaustive subset/query comparisons with unit weights, 864 with rational weights, and 140 comparisons of the resulting lower certificate with the exact optimum. The weighted separation extension is valid and polynomial. Nevertheless, its strongest all-subset certificate for an entropy-optimal coordinate tree can lose the full target-order factor. On that same instance the pair-potential cone is exact. No improved unrestricted approximation follows.

## 1. Weighted separation is valid

Let `T` be a supplied proper binary identifying tree. For each internal node `v`, let `H_v` denote its leaves and let its two child leaf sets be `H_v0,H_v1`. Assign a nonnegative rational weight `w_v` and define

    P_w(S) = sum_v w_v |S intersect H_v|
                       1[S meets both H_v0 and H_v1].

For a fixed test `q`, color selected leaves red and blue according to its two outcomes. At node `v`, let `(r_0,b_0),(r_1,b_1)` be the selected color counts in its two children, and put `r=r_0+r_1`, `b=b_0+b_1`. The contribution of this node to

    Delta_w(S,q) = P_w(S)-P_w(S intersect q)-P_w(S minus q)

is zero if one selected child is empty. Otherwise it is exactly

    w_v [r 1[r_0 r_1=0] + b 1[b_0 b_1=0]].                 (1)

An absent color has count zero, so (1) also covers monochromatic selected sets. All node contributions are nonnegative.

A tree dynamic program stores, for each node and feasible pair `(r,b)`, the largest total deficit attainable in that subtree, together with a selected-leaf witness. Combining child tables adds (1). The root table therefore gives the maximum deficit at every total selected size, and hence both the maximum ratio `Delta_w(S,q)/|S|` and a violated capacity witness. Empty and singleton selected sets have zero deficit.

There are at most quadratic many states per tree node. If its child leaf counts are `l_v,r_v`, its child-table product is `O(l_v^2 r_v^2)`. Every unordered leaf pair has one lowest common ancestor, so `sum_v l_v r_v=binom(n,2)` and `sum_v (l_v r_v)^2<=binom(n,2)^2`. Thus the arithmetic operation bound is `O(n^4)` for one fixed test. For rational weights of input bit length `B`, every stored value is an integer linear combination of at most `n-1` such weights, with integer coefficients at most `n`; the bit length remains polynomial in `n,B`. Thus this is a genuine rational polynomial separation oracle.

Consequently the bounded rational LP

    maximize sum_v |H_v| w_v
    subject to 0 <= w_v <= 1,
               Delta_w(S,q) <= |S| for every S,q

has polynomial optimization by separation. Each inequality is linear in the `n-1` variables. The coefficient of `w_v` is the nonnegative integer in brackets in (1), at most `|S|`. Telescoping down an arbitrary identifying tree proves `P_w(H) <= OPT_raw`. This scalar lower bound alone does not construct an approximation algorithm.

The explicit upper bounds `w_v<=1` are harmless. If the tests used in `T` belong to the supplied test family, they are also implied by the two-leaf state consisting of one hypothesis from each child of `v`, queried by the test at `v`.

## 2. A full-order gap on the plain coordinate cube

Let `H={0,1}^D`, `n=2^D`, and supply just the `D` coordinate tests. Let `T` query coordinates in the fixed order `1,...,D`. Every leaf has depth `D`, and entropy proves

    OPT_raw = n D.

Let `w` be any feasible all-subset weighted-tree certificate. For depth `i`, define the average node weight

    a_i = 2^(-i) sum_{v: depth(v)=i} w_v.

The objective is `P_w(H)=n sum_{i=0}^{D-1} a_i`.

Fix `0<=t<=D-1` and a depth-`t` node `u`. Let `R` consist of all descendants of `u` whose final coordinate is one. Its size is

    r = 2^(D-t-1).

For every strict ancestor `v` of `u`, choose one final-coordinate-zero leaf in the child of `v` not containing `u`. These `t` witnesses exist, are distinct, and lie outside `R`. Let `S_u` be their union with `R`; thus `|S_u|=r+t`.

Use the final-coordinate test as `q`. At every strict ancestor of `u`, both selected children are nonempty, while every red selected leaf is in the child toward `u`. Formula (1) therefore contributes at least `r w_v` at that ancestor. Other contributions are nonnegative. Feasibility gives

    r sum_{v strict ancestor of u} w_v <= r+t,
    sum_{v strict ancestor of u} w_v <= 1+t/r.             (2)

Averaging (2) over the `2^t` choices of `u` yields

    sum_{i=0}^{t-1} a_i <= 1+t/2^(D-t-1).                 (3)

The remaining levels contribute at most `D-t`, since `w_v<=1`. Hence every feasible certificate satisfies

    P_w(H)/n <= D-t+1+t/2^(D-t-1).                        (4)

For `D>=4`, take `k=ceil(log2 D)+1` and `t=D-k>=0`. Since `2^(k-1)>=D`, (4) implies

    P_w(H) <= n [ceil(log2 D)+3].                         (5)

Thus even the exactly optimized weighted-tree LP can have gap

    OPT_raw / max_w P_w(H)
       >= D/[ceil(log2 D)+3]
       = Omega(log n / log log n).                        (6)

This example does not need the added rare test used for the unweighted scaling obstruction. It already uses an optimal supplied tree. The gap concerns the proposed **all-subset** capacity cone: the thin sets `S_u` need not be reachable using only coordinate queries. Restricting capacities to reachable states changes the relaxation and requires a separate valid separation method. In this particular cube, the reachable coordinate subcubes can be enumerated in `3^D=n^(log2 3)` time; this special enumeration does not extend to arbitrary test tables.

## 3. The pair cone is exact on the same instance

Place pair coefficient `lambda_{xy}=1` on every edge of the `D`-dimensional hypercube and zero on other pairs. The pair potential is

    P_pair(S)=2 * number of hypercube edges with both endpoints in S.

For coordinate test `q_j`, its deficit is twice the number of selected cube edges parallel to coordinate `j`. These edges form a matching, so this deficit is at most `|S|` for **every** subset `S`. The pair potential is therefore feasible, and

    P_pair(H)=2 * (nD/2)=nD=OPT_raw.

Combining with (5), a single fixed-tree weighted cone can be asymptotically weaker in root objective than the pair cone by the full target-order factor. Polynomial support-size separation by itself does not imply domination of the pair cone. This proves one direction of non-domination; it does not prove that the two cones are incomparable or that pairs always dominate weighted-tree potentials.

The sum of an arbitrary pair potential and this tree potential has not been given a polynomial separation algorithm here. The tree dynamic program cannot summarize arbitrary selected pair crosslinks using only its two color counts. Neither polynomial solvability nor hardness of that joint cone is claimed.

## 4. Reproducible checks

The independent checker `research-general-tree-potential-audit.py` compares rational weighted separation with exhaustive subset enumeration on small coordinate and random trees. It checks the selected witness construction and the averaged inequalities above, and exhaustively checks matching capacities on all subsets of cubes through dimension four. These checks audit the proofs; they are not an LP implementation or a proposed approximation algorithm.
