# Coupling bounded-menu branching with deep partition policies

Auxiliary research note, 19 October 2026. This develops the user's proposal
to search among a few alternatives for logarithmically many stages and to
spend roughly OPT on a much deeper partition. The article is unchanged.
There is no unrestricted approximation improvement in this note. The new
positive statement is a polynomial branching-and-LP compiler, together with
an exact partition version of the earlier completion-cover theorem.

Throughout, raw work is the sum of all hypotheses' query counts. A policy
uses original tests, suppresses constant tests, and may stop unfinished.
The hypotheses are explicit and uniformly weighted. Write n=|H|.

## 1. A logarithmic number of choices really can be searched exactly

Suppose every actual state S has at most b efficiently constructible actions.
An action can be a single original query, but it can also be an arbitrarily
long explicit partial original-test tree. Its nonempty exit states partition
S. Calling a complete greedy tree an action is legal, although that action
leaves no unresolved states on which a subsequent choice could help.

Allow at most d actions on each hypothesis's execution path. At different
response exits the algorithm may choose different subsequent actions. This
is fully response-adaptive search, not a common sequence of d heuristic
indices imposed on every branch.

Unfold all action choices and all their response exits. Let M_l be the sum
of the cardinalities of all state occurrences at action level l, counting
repeated states separately. Each one of the at most b actions partitions
its input state, and therefore

    M_0=n,                 M_(l+1) <= b M_l.

Every nonempty occurrence has mass at least one. Consequently the number
of occurrences through level d is at most

    n sum_(l=0)^d b^l.                                      (1)

This bound does not depend on the number of exits of an action. In particular,
it allows long greedy blocks with up to |S| exits. For constant b and
d=O(log n), the unfolding is polynomial. For growing b it remains polynomial
whenever d log(max{2,b})=O(log(n+m)). The exponent in this condition must be
an absolute constant.

Every explicit proper partial action has O(|S|) nodes for constant response
arity. The total sizes of all expanded actions are thus polynomial under
(1), not just the count of their boundaries. A state-dependent action menu
may be recomputed at every occurrence. Menus depending on the entire
recorded history are also permitted if they can be constructed in polynomial
time; retaining occurrences instead of merging equal states handles them.

For example, with a fixed size cap B, let V(S,t) be the cheapest work of a
menu policy that leaves only cells of size at most B, using at most t more
actions. The exact recurrence is

    V(S,t)=0                                      if |S|<=B,
    V(S,0)=infinity                               if |S|>B,
    V(S,t)=min_a {W(a on S)+sum_E V(E,t-1)}        otherwise. (2)

Actions are stopped early if they already reach an acceptable state. For
primitive-query actions, W(a on S)=|S| and E runs over the response children.
A supplied complete fallback can replace infinity in (2) if the goal is
minimum full-tree cost rather than a strict partition cap. This gives the
best fully adaptive bounded-menu tree in the searched class. It avoids
enumerating the exponentially many combinations of choices across sibling
response branches.

The difficult part is choosing a menu whose best policies compete with
unrestricted optimal trees. Polynomial search alone does not supply that
comparison.

## 2. A full-column LP for deep partitions has no integrality gap

Let A be a downward-closed family of acceptable nonempty states: if S is in
A and the nonempty R is a subset of S, then R is also in A. The main example
is A_B={S:|S|<=B}, with B fixed for this invocation. Singletons are assumed
acceptable so that identification always supplies a feasible partition.

For a partial policy P, let C(P) be the union of its acceptable exit states.
All other exits are unfinished. Let W(P) be its raw work, including tests
encountered by hypotheses it does not settle. Consider

    minimize sum_P W(P) x_P,
    sum_(P:h in C(P)) x_P >= 1              for every h,
    x_P>=0.                                                   (3)

The columns range over all actual partial original-test policies. Let F_A
be the minimum raw cost of any full partition into acceptable cells.

**Proposition.** The value of (3) equals F_A.

One optimal acceptable partition is a feasible primal column. For the reverse
bound, fix an optimal acceptable tree T and let y_h be h's depth in T. After
any partial policy P, append T restricted to each unfinished exit. Downward
closure ensures every restricted T exit remains acceptable. Suppression and
earlier acceptance can only lower its work. The combined tree therefore has
cost at most

    W(P)+sum_(h not in C(P)) y_h.

Its cost is at least F_A=sum_h y_h. Cancellation gives
sum_(h in C(P)) y_h<=W(P), which is exactly the dual constraint for (3).
Thus y is dual feasible with objective F_A.

This extends the existing exact completion-policy LP from singleton exits
to arbitrary downward-closed partition targets. It is an exponential-column
identity, not an optimization algorithm by itself.

## 3. Fractional deep partitions compile without a rounding loss

Suppose explicit policies P_j and nonnegative rational weights x_j satisfy
the coverage constraints of (3). Define fixed hypothesis prices

    v_h=sum_j x_j d_j(h),

where d_j(h) is h's actual query count in P_j. Then sum_h v_h equals the
fractional objective L=sum_j x_j W(P_j).

At a current unfinished state S, restrict P_j to S, suppress constant tests,
and stop whenever an acceptable state is reached. Its work is at most
sum_(h in S)d_j(h), and it settles every member of C(P_j) intersect S.
Consequently

    sum_j x_j [W(P_j restricted to S)
                   -sum_(h in C(P_j) intersect S) v_h]
      <= sum_(h in S) v_h
                   -sum_(h in S) v_h sum_(j:h in C(P_j)) x_j
      <= 0.                                                   (4)

A policy settling no originally covered hypothesis has a nonnegative
bracket. Positive-weight productive policies cover S. Hence a productive
policy has work at most the total prices of the hypotheses it settles.
Execute it and recurse only on its unacceptable exits. Each execution
settles at least one previously unfinished hypothesis; at most n productive
executions occur. Prices telescope over the disjoint settled sets, giving

    W(output acceptable partition) <= L.                      (5)

Extra hypotheses settled after conditioning only help. The compiler can
switch policies at states that occur in none of the original templates.
There is no set-cover logarithm or additional partition-rounding factor.

The same direct maximum-profit prefix DP used by the template-cover compiler
works here: an acceptable actual state earns the sum of all its hypotheses'
prices, rather than just one singleton price. At an unacceptable state,
stopping earns zero, and continuing earns child profits minus actual work.
Ties favor a productive policy.

For supplied full template trees, truncate each tree at its first acceptable
states. The earlier compact precedence LP over all its stopping prefixes
applies verbatim, with coverage of h attached to its first acceptable node.
Its feasible points compile by (5). The cost of a whole acceptable template
is always an available benchmark.

## 4. A compact LP over every bounded-menu adaptive policy

There is no need to enumerate complete template trees before applying the
LP. Use the polynomial unfolded history structure of Section 1. At a
nonacceptable virtual state occurrence u, write S_u for its original state,
w_u for an incoming policy weight, and x_(u,a)>=0 for the weight choosing
action a. Impose

    sum_a x_(u,a) <= w_u.                                     (6)

The unused incoming weight stops unfinished at u. For **each** response-exit
child v of action a impose

    w_v=x_(u,a).                                              (7)

Equation (7) copies the action's probability weight to every response exit;
it is not a conservation-of-hypothesis-mass equation. Every member of an
exit follows that same choice in a deterministic policy. The root weight
is a free nonnegative variable. Nodes at action level d may only stop.
Acceptable nodes stop and credit their entire state. Require

    sum_(u acceptable and h in S_u) w_u >= 1       for each h. (8)

Minimize

    L=sum_(u,a) W(a on S_u) x_(u,a).                          (9)

There are polynomially many variables and constraints under (1), and all
coefficients are explicitly computable integers of polynomial bit length.
The LP may be infeasible if the chosen menu and horizon cannot settle some
hypothesis. A complete fallback action, if included, supplies feasibility.

**Why these are real fractional policies.** Divide a feasible point by its
root weight. At each reached u, choose action a with probability
x_(u,a)/w_u, or stop with the remaining probability. Choose independently at
different reached response branches. This samples a deterministic fully
adaptive menu policy. Its probability of activating u is w_u divided by the
root weight, by induction using (7). Thus (8) is its weighted completion
coverage and (9) is its weighted expected actual work. This is a decomposition
argument; sampling is unnecessary for the final deterministic algorithm.

**Direct deterministic compilation.** Obtain prices directly as

    v_h=sum_(u,a:h in S_u) x_(u,a) d_(u,a)(h),                (10)

where d_(u,a)(h) is h's test count within the explicit macro action. Their
sum is exactly (9). At any actual unfinished state S, restrict the unfolded
history structure to S. An occurrence u then concerns S intersect S_u.
Perform an AND/OR profit DP: an acceptable actual state earns its price sum;
stopping earns zero; choosing an action earns the sum of its response-exit
profits minus its actual restricted work. Early acceptance and constant-test
suppression are handled inside the action. At every OR node select the best
action, using completed cardinality to break zero-profit ties.

The fractional decomposition and (4) guarantee a productive policy of
nonnegative profit. The DP finds one without generating the decomposition's
potentially exponentially many full trees. Execute it and recurse on its
unacceptable exits. As in Section 3, at most n productive applications occur
and total work is at most the LP objective. Restriction may create states
outside the original history structure, but each DP occurrence still knows
its actual intersection S intersect S_u; no closure under all intersections
is precomputed.

This is a genuine combination of logarithmic-depth bounded-menu search,
deep partition targets, fractional optimization, and adaptive compilation.
Its approximation factor is entirely determined by the quality of the
menu-policy family. It does not yet prove that this family has constant or
improved asymptotic approximation ratio on arbitrary response matrices.

The compiled output may restart the virtual menu program on newly observed
subsets. It therefore need not itself remain in the original d-action menu
class. The d-action bound controls LP size and its comparison family; the
compiler's separate n-application bound controls its polynomial runtime and
actual legal output. In contrast, the direct Bellman optimizer in Section 1
does return a member of the bounded-action class (or that class with its
stated fallback).

## 5. What an OPT-cost deep partition exists, and why primitive depth is tight

For 2<=k<=s, prune an optimal full tree on a state S, of size s, at its first
nodes of size at most s/k. Its partial work is at most F_OPT(S), and all
exits have the desired size. This is an existence statement for every such
k, including k=s.

If its mean optimal cost is C_OPT(S)=F_OPT(S)/s, that cut has height less
than k C_OPT(S)+1. Indeed, a path to a still-unacceptable depth-l node has
l ancestors, each with population greater than s/k, so their raw work alone
exceeds l s/k. A logarithmic primitive-query horizon therefore cannot simply
assume it includes this cut.

Singleton tests show why that issue is real. If the only queries are
individual hypothesis equalities, a partition into cells of size at most B
must follow a negative spine of s-B queries. Its raw work is

    sum_(r=B+1)^s r = [s(s+1)-B(B+1)]/2.

For B=floor(s/2), this is a constant fraction of the optimal full raw cost,
but the required primitive depth is Theta(s). Greedy is optimal on this
example, so it is not an approximation obstruction. It demonstrates why a
successful logarithmic branching procedure must either recognize a good
long greedy block or certify that its fallback is already competitive.

The subexponential prefix algorithm of Li, Liang and Mussmann searches deep
optimal prefixes and uses a greedy-cost dichotomy. Its depth parameter is
polynomially large in n, and it does not itself give a polynomial menu.
The reference is arXiv:1906.11385v2, Sections 5 and 7, already available in
the workspace as tmp/pdfs/general-1906-v2.txt.

## 6. Precise missing comparison

For a desired shrinkage k>=2, let F_MENU(S,k,d) denote the optimum of the compact
LP with acceptable size cap max{1,floor(|S|/k)}. The compiler constructs a partition
at cost at most F_MENU. If, for all relevant S,

    F_MENU(S,k,d) <= alpha F_OPT(S),                           (11)

then recursively applying such partitions gives at most
alpha ceil(log_k n) times global OPT: each recursive partition level consists
of disjoint states, and the sum of their restricted optimal costs is at most
global OPT. To beat log n/loglog n by this argument with constant alpha,
k must grow faster than every fixed power of log n. A fixed polynomially
large k gives a constant number of levels.

Equation (11) is unproved for an unrestricted efficiently generated menu.
Nor does the exact LP identity imply it for a restricted menu. Stronger
telescoping comparisons could avoid charging OPT at every partition level,
but require controlling the residual optimal cost after the algorithm's
chosen cut. Merely proving that some OPT-cost cut exists does not control
the cut produced by a heuristic.

The positive progress here is that all choices, all response adaptivity,
all fractional combinations and all rounding can be handled in polynomial
time once a small sufficient menu of executable blocks is supplied. The
unrestricted research task is now concentrated in that menu comparison.

## 7. Bounded executable verification

`research-general-menu-partition-lp.py` implements the unfolded occurrence
structure, validation of exact feasible rational copied-flow points, price
calculation, and the direct restriction-aware AND/OR compiler. It does not
implement LP optimization. Its random feasible points come from local
stochastic partial policies, scaled to cover every hypothesis. The checker
uses no unrestricted optimum oracle.

There are 29 checked feasible points, 1,442 unfolded occurrences, and 31
productive compiler applications. All output leaves meet their stated size
caps and all actual original-test costs are at most the supplied LP-point
objectives. Two fixtures use complementary partial policies with total root
weight two and exact coverage one. Neither policy completes the partition;
the compiler uses one and then restricts the other to the remaining state,
requiring two productive applications. For cap two, supplied work is 64 and
actual compiled work is 48. Thus these checks include fractional partial
coverage rather than only convex combinations of complete trees.

A 32-hypothesis singleton-only fixture uses a first greedy-half-cut macro
of primitive depth 16, demonstrating that the macro occurrence bound does
not rely on short query depth. Its five macro stages still produce a
polynomial unfolding. Results are recorded in
`research-general-menu-partition-lp-results.json`.

The root agent's separate `research-general-branching-partition.py` implements
the direct bounded-menu cost optimizer, rather than this feasible-point
compiler. The distinction between optimization and point compilation is
deliberate.
