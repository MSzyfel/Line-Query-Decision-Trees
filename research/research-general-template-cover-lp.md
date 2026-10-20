# A compact LP over supplied codes with lossless adaptive compilation

Auxiliary research note, 19 October 2026. The article is unchanged. This
develops the earlier exact completion LP into a polynomial algorithm over a
supplied polynomial template library. It does not prove that any current
library approximates unrestricted OPT.

**Result.** Given R explicit complete original-test trees, a polynomial-size
LP simultaneously optimizes over every stopping prefix of every tree. Any
feasible rational point compiles in polynomial time to a legal complete tree
of no greater raw cost. Compilation can switch templates on newly observed
states; it does not enumerate all intersections or rely on integer descent.

The key is an exact deterministic compiler for fractional covers by executable
partial policies, developed jointly with the continuation agent and audited
independently. The LP's full-column value being OPT was already proved in
`research-general-pricing-next.md`; that value identity is not a new claim.
The addition here is constructive rounding for explicit columns and the
compact multiple-template formulation.

## 1. Lossless rounding of an explicit fractional policy cover

Let P_j be explicit proper partial trees on H, made from original questions.
Let d_j(h) be the number of tests encountered by h, including work on h even
when P_j leaves it unfinished. Let C_j be the hypotheses identified by
singleton exits. Suppose rational weights x_j>=0 satisfy

    c_h = sum_(j:h in C_j) x_j >= 1 for every h.             (1)

Define fixed nonnegative prices

    v_h = sum_j x_j d_j(h).

Their total is exactly the fractional work sum_j x_j W(P_j). For n>1,
coverage implies v_h>=1, because any full-H policy completing h must query at
least once on that path.

On a current unfinished state S, restrict each P_j by suppressing queries
that have become constant. Stop at its original unfinished exits, or earlier
when the actual state becomes a singleton. This partial-aware restriction
has work

    W(P_j|S) <= sum_(h in S) d_j(h),

and identifies at least C_j intersect S. Set

    D_j(S) = W(P_j|S) - sum_(h in C_j intersect S) v_h.

Multiplying by x_j and summing gives

    sum_j x_j D_j(S)
      <= sum_(h in S) v_h - sum_(h in S) c_h v_h <= 0.       (2)

A column with C_j intersect S empty has D_j(S)>=0. Positive-weight productive
columns cover every member of S. Hence some productive column has D_j(S)<=0.
Choose one, execute its restricted policy, and recurse independently on all
unfinished nonsingleton exits. Extra singleton completions only help: they
remove additional nonnegative prices.

The potential V(S)=sum_(h in S) v_h pays for that execution and all recursive
children. Each productive application identifies at least one new original
hypothesis, so there are at most n applications over the entire output.
The output is a proper full original-test tree and

    F(output) <= sum_h v_h = sum_j x_j W(P_j).               (3)

All restrictions, scores and grafts are polynomial in the explicit policy
library and rational bit encoding. There is no approximation or set-cover
rounding factor in (3). This argument even handles overcoverage in (1);
exact coverage and equal-size response cells are unnecessary.

Ordinary set-cover columns cannot be substituted for these policies. The
per-hypothesis work on outsiders is essential to (2). Likewise the theorem
does not compute a cheap fractional cover over an implicit exponential family.

## 2. A polynomial extended formulation for all template prefixes

Let B_1,...,B_R be explicit full proper original-test trees on H. Each has n
singleton leaves. Associate a variable z_(k,u) with every internal node and
every singleton leaf of B_k. Impose

    0 <= z_(k,u) <= 1,
    z_(k,child) <= z_(k,parent),
    sum_k z_(k,leaf h) >= 1 for every h.                   (4)

Minimize

    L(z)=sum_k sum_(u internal in B_k) |S_(k,u)| z_(k,u).    (5)

There are O(Rn) variables and constraints with integer coefficients of
polynomial bit size. A standard polynomial rational LP algorithm can optimize
(4)-(5). Every supplied complete template gives a feasible solution of its
own cost, so the optimum is no larger than the cheapest supplied tree.

For each k, threshold its variables at t>0. The inequalities in (4) ensure
included nodes form an ancestor-closed prefix. Execute the included internal
queries and stop at excluded nodes. If a singleton leaf is reached, it is
already identified, even when its own z value is below t. Therefore the
weighted actual completion of h is **at least** z_(k,leaf h), while the
integrated raw work is exactly the contribution of B_k to (5).

Only the distinct positive z values matter. Sorting them yields at most
2n-1 explicit prefixes per template; each gets the difference between two
successive thresholds as its nonnegative rational weight. This is a
polynomial fractional completion cover with work exactly L(z). Section 1
then gives a complete actual tree of cost at most L(z).

The upper bound one is optional. If a feasible point has larger entries,
clipping all entries at one preserves precedence and leaf coverage and never
increases cost. There is thus no need to allow unbounded multiplicities.

## 3. Direct compilation without even forming the prefixes

One can compute prices straight from the compact point:

    v_h = sum_k sum_(u internal on B_k's path to h) z_(k,u).

Their sum is L(z). At state S, optimize the profit

    completed-price - actual-work

over all stopping prefixes of B_k restricted to S. A reverse tree DP does
this exactly. An actual singleton gives profit v_h for free. At a proper
query node choose between stopping with zero profit and continuing with
the two child profits minus the current population. Constant queries are
suppressed. Break zero-profit ties in favor of more actual completions.

The threshold decomposition and (2) guarantee that some template has a
productive prefix of nonnegative profit. Select the best such DP output,
execute it, and recurse on unfinished exits. Its work is paid by prices of
the hypotheses it actually completes, so (3) applies unchanged. This version
uses at most n productive applications and polynomial arithmetic per
template per application. All prices remain fixed for the entire construction.

The newly observed states need not occur as nodes of any supplied template,
nor belong to a precomputed quadratic intersection pool. Only the states
encountered in the one actual constructed tree are evaluated. This avoids
assuming closure under every possible multi-template history.

The proofs in Sections 1-3 also work for any fixed number of responses per
test: sum over all nonempty response children in the profit recurrence.
The current executable backend is binary. No binary entropy inequality is
used in this LP compilation theorem.

## 4. What this supplies, and what it does not

The optimized LP and compiler are a polynomial non-greedy combination
procedure for an explicit library. They compare against all fractional
mixtures of all its prunings, and the resulting adaptive tree may be cheaper
than that library optimum. This is stronger than just selecting the cheapest
complete member or rounding a cover to a subset of whole policies.

Its objective is a feasible-policy upper benchmark, not a lower bound on
unrestricted OPT. The full completion LP contains every executable policy
and is exact, but replacing it by the template LP is a restriction of its
columns. No current theorem bounds this restricted optimum by
o(log n/loglog n) times unrestricted OPT. Generating templates that support
that comparison remains the central task. The previous fixed-lookahead
barriers also warn against assuming shallow fresh-greedy templates suffice.

## 5. Implementation and bounded verification

`research-general-cover-geometry.py` implements the general explicit-cover
compiler. `research-general-template-cover-lp.py` implements feasibility
checking, exact threshold decomposition, direct price computation and
restricted-template profit compilation. The latter accepts a feasible
rational point; it **does not implement an LP optimizer**. The polynomial
optimization statement above is a theorem about the explicit LP, not a
claim that its optimum was computed by the bounded checker.

The template checker validates 36 exact feasible compact points and 155
decomposed partial columns, checking coverage and work identities. It runs
both the direct template compiler and the independent explicit-cover
compiler on the decompositions. No unrestricted optimum oracle is used.

A 256-hypothesis example has two supplied templates of raw cost 3807 each.
Each wastes an equality search on a different quarter of H. A feasible point
keeps their efficient three-quarter prefixes, of total LP objective 3456.
Direct compilation finishes 192 hypotheses for work 1728, then switches
templates on the remaining 64 for work 384, totaling 2112. This illustrates
conditional combination. The same matrix supplies a simpler global bit code
of cost 2048, so this example is deliberately **not** presented as beating
matrix greedy or establishing a new approximation ratio.

Independent review is recorded in
`research-general-fractional-rounding-audit.md`. Result files distinguish
feasible-point compilation from LP optimization throughout.
