# Polynomial separation for coherent tree restriction potentials

Auxiliary research note, 18 October 2026. This is an LP direction and a verified separation algorithm, not an improved unrestricted approximation theorem. The article is unchanged.

## The potential retains a whole supplied hierarchy

Fix an explicit proper binary identifying tree T. Let H_v be the hypotheses below an internal node v, with children L_v and R_v. Assign a nonnegative rational weight w_v to each internal node and define

    P_w(S) = sum_v w_v |S intersect H_v|
                    1[S meets both L_v and R_v].

For w_v=1, P_w(S) is exactly the raw cost of T pruned to S. For general weights it is that restriction's cost with the original query at v priced at w_v. The definition keeps the same original-node prices in every restriction.

For each supplied test q, impose the global Bellman capacities

    P_w(S) - P_w(S intersect q^-1(0))
           - P_w(S intersect q^-1(1)) <= |S|
                    for every subset S of H.                    (1)

As in the planar restriction-credit proof, capacities telescope down every actual identifying tree, giving P_w(H)<=F_OPT(H). All summands vanish at singleton leaves.

The small-resource cone in research-general-credit.md has coNP-hard separation already for overlapping triples. Here resources can involve arbitrarily many hypotheses, but all features share one laminar hierarchy. This coherence makes exact separation polynomial.

## Exact separation by a tree DP

Fix q and call its two outcome classes red and blue. At an original tree node v, suppose selected hypotheses have child counts (r_L,b_L) and (r_R,b_R). The contribution of v to the restriction deficit is zero if either selected child is empty. Otherwise it is

    w_v { r 1[red occurs in only one child]
          + b 1[blue occurs in only one child] },                 (2)

where r=r_L+r_R and b=b_L+b_R. Indeed the original restriction pays w_v(r+b); a monochromatic restriction retains v exactly when that color occurs in both children. Formula (2) subtracts those retained costs.

For each v and pair (r,b), retain the maximum total weighted deficit achievable by a selected subset of H_v with those counts, together with a witness subset. At a singleton leaf, allow selection and nonselection, both with zero deficit. At an internal node, combine its two child tables and add (2). Since contributions above v depend only on the two color counts, retaining only a maximum for each count pair loses no optimum.

At the root, maximize

    deficit(r,b) - (r+b)

over nonempty selections. A positive value returns a violated constraint (1), with the explicit subset S and supplied test q. Equivalently, maximize deficit/(r+b) to find the exact least uniform scaling of this weighted potential. Scanning all m supplied tests is a separation oracle.

Each table has O(n^2) entries. A loose bound of O(n^5) rational arithmetic operations per query follows from O(n) nodes and O(n^4) child-table combinations; tighter counting gives O(n^4), but no sharp exponent is required here. Witness subsets need O(n) bits. The input rational weights have polynomial bit complexity, and each score is a sum of at most n weighted integer coefficients bounded by n, so exact arithmetic also has polynomial bit complexity.

This oracle searches all subsets, including states absent from T. It does not assume a supplied test can activate an arbitrary returned subset cheaply.

## A genuine polynomial LP with large-support features

Consider

    maximize sum_v |H_v| w_v
    subject to (1), 0<=w_v<=1.                                  (3)

The upper bounds w_v<=1 are harmless: choose one hypothesis from each child of v and a supplied test separating that pair. The restriction deficit for that selected pair is exactly 2w_v, so (1) already implies w_v<=1.

There are at most n-1 variables. All constraint coefficients are explicitly recoverable nonnegative integers at most n. The tree DP supplies exact separation for rational trial weights. The bounded rational LP is therefore polynomially optimizable using the standard separation/optimization equivalence; see the [primary paper of Groetschel, Lovasz, and Schrijver](https://www.zib.de/userpage/groetschel/pubnew/paper/groetschellovaszschrijver1981a.pdf). This is a polynomial formulation, rather than a claim that polynomially many variables suffice by themselves.

The current companion implements and audits the separation oracle. It does not implement an ellipsoid optimizer or claim an approximation ratio for (3).

If an actual incumbent T has F_T(H)/value(3)<=alpha, solving this LP certifies T as an alpha approximation. A rounding theorem or a way to improve T when the LP value is too small is still needed for an unrestricted approximation algorithm.

The dual of the equivalent LP with the redundant bounds w_v<=1 omitted also makes that missing step concrete. Its variables are nonnegative masses z_(S,q). They fractionally cover each original node's cost |H_v| using that node's restriction-deficit coefficient, while minimizing sum_(S,q) |S|z_(S,q). The dual charges a test as though its context S were already available. Executing these contexts at comparable total cost is a decoding problem. The planar witness geometry addresses a related issue; an arbitrary subset returned by this DP has no such automatic decoder.

## Why one uniform scaling is too weak

Even an optimal supplied tree can require a logarithmic scaling in (1).

Let H={0,1}^D, n=2^D, with coordinate tests. Use the complete coordinate tree T, so every hypothesis has depth D and F_T(H)=nD. This is globally optimal by the binary entropy lower bound. Add one supplied test whose positive set consists of alternating members of

    S={0,e_1,...,e_D}.

The coordinate tree restricted to S is a comb with s=D+1 leaves. Its restriction to either test color is also a comb. If the two color counts are a and b, a+b=s, then

    F_T(S)-F_T(S_red)-F_T(S_blue)=ab+1.

Consequently the least feasible uniform scaling beta of the unweighted restriction potential is at least (ab+1)/s=Omega(D), although T remains exactly optimal after adding the test. The failure concerns a sparse restriction of an otherwise efficient global code.

This disproves using the maximum all-subset restriction deficit of one unweighted incumbent as a universally tight approximation certificate. Entropy already certifies the full cube optimally.

The independently weighted LP also has a proved target-order gap, even on the plain coordinate cube without the extra rare test. The [independent audit](research-general-tree-potential-audit.md) constructs a core of last-coordinate-one hypotheses plus one opposite-color witness in each ancestor sibling. All-subset capacity forces the sum of the ancestor node weights to be at most 1+t/2^(D-t-1). Averaging over depth-t nodes and taking D-t=ceil(log_2 D)+1 gives LP value at most n(ceil(log_2 D)+3), versus OPT=nD. By comparison, the pair cone is exact here: give weight one to every hypercube edge; each coordinate query cuts a matching.

This limitation applies to the all-subset cone. The thin witness sets are generally not reachable by coordinate tests, so it does not refute the stronger cone imposing capacities only at reachable states. The current DP does not separate that latter cone.

Reachability itself has a simple polynomial test. For nonempty S, intersect every supplied response cell that contains all of S, and call the result cl(S). Then S is a reachable transcript state exactly when cl(S)=S. One direction follows because every cell defining a transcript containing S also appears in this intersection; the other follows by asking the constant-on-S tests and following their common responses. This takes polynomial time in the explicit matrix. On the cube, the thin set {0,e_1,...,e_D} has no constant coordinate, so its closure is the whole cube. Optimizing a deficit over closed subsets is a different task from checking one subset's closure; no polynomial separation guarantee for that optimization is established here.

The [pair-plus-tree note](research-general-pair-tree-separation.md) gives a further warning about combining formulations: maximizing a violation for one fixed query becomes NP-hard for the sum of a pair potential and one weighted tree potential. Both classes separately have polynomial fixed-query separation. The reduction does not prove hardness of the full all-query separation task, and supplies no decision-tree approximation hardness.

## Relation to the strengthened non-greedy procedure

The continuation agent's new procedure optimizes actual incumbent restriction costs at the unfinished boundaries of a represented partial policy. If V_T(S)=F_T(S), the represented-state recurrence is

    J(S)=min{V_T(S), |S|+min_q sum_a J(S_a)}.

Absent child states may be terminal macros executing T pruned to that child; they are not recursively expanded. This preserves a fixed polynomial number of represented contexts and yields a legal tree. It measures the exact credit

    Gamma_T(P)=F_T(H)-sum_unfinished V_T(A),

rather than only completed-leaf depth prizes. The credit telescopes into local restriction deficits along P. An alpha approximation for maximizing Gamma_T(P)/W(P) over all executable partial policies would yield an alpha UDT approximation by strict integer descent: a full optimal tree has ratio F_T(H)/F_OPT(H). No such unrestricted oracle is supplied by the separation DP above, because it cannot make arbitrary S reachable for free.

Thus the LP and the non-greedy algorithm expose the same unresolved issue from two sides: coherent lower potentials can be separated efficiently, but a low-cost activation procedure for their useful contexts is still missing.

## Verification

research-general-tree-potential.py passed 864 query/subset comparisons against exhaustive enumeration with unit weights, another 864 comparisons with independently sampled rational node weights, and 140 exact small-instance lower-certificate comparisons. It checks the cube comb-restriction identity through n=2048. The results are saved in research-general-tree-potential-results.json.

No article source or TeX theorem manuscript was changed. The polynomial oracle is a research primitive; the unrestricted o(log n/log log n) approximation objective remains open in this work.
