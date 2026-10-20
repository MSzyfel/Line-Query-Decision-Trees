# Audit: compiling an explicit fractional completion cover

Auxiliary independent proof audit, 19 October 2026. The article is unchanged.
The proposed theorem and compact template-prefix LP are valid with the scope
and small conventions below. This is a compiler for supplied policies, not
an unrestricted polynomial pricing or approximation theorem.

## 1. Explicit partial-policy rounding

Each P_i must be an actual legal partial decision tree on the same original
uniform H. Let C_i be its hypotheses ending at singleton leaves, and let
d_i(h) count **all** original questions asked of h, including paths that stop
unfinished. Given explicit rational `x_i>=0` with
`sum_(i:h in C_i)x_i>=1`, define

    v_h=sum_i x_i d_i(h).

For `n>1`, every policy completing h asks at least one question on h, so
`v_h>=sum_(i:h in C_i)x_i>=1`. The case n=1 terminates immediately at cost
zero. This positivity observation removes a possible degeneracy in selecting
a productive column.

At any current nonsingleton state S, restrict P_i to S and suppress constant
questions. Its physical work W_i(S) satisfies

    W_i(S)<=sum_(h in S)d_i(h).

Each original completion in `C_i intersect S` remains a singleton completion;
restriction can additionally complete other hypotheses. Define its guaranteed
reward `R_i(S)=sum_(h in C_i intersect S)v_h`. Then

    sum_i x_i [W_i(S)-R_i(S)]
      <=sum_(h in S)v_h
            -sum_(h in S)v_h sum_(i:h in C_i)x_i
      <=0.

At least one positive-weight policy is productive on S, since the columns
cover every h in S. Every nonproductive column has reward zero and nonnegative
work. If every positive-weight productive column had positive deficit, the
displayed weighted sum would be positive. Hence some such column has

    W_i(S)<=R_i(S).                                       (1)

Execute its actual restriction and recurse at nonsingleton unfinished exits.
By induction, those disjoint exits together cost at most their v-mass.
Every guaranteed completion has left the recursion, so (1) gives

    full_cost(S)<=W_i(S)+sum_(unfinished exits U)sum_(h in U)v_h
                 <=sum_(h in S)v_h.

At the root this is exactly

    full_cost(H)<=sum_h v_h=sum_i x_i W(P_i).

Each selected column permanently completes at least one hypothesis; no
completed hypothesis appears in another recursive call. There are therefore
at most n productive calls. Additional singleton completions caused by
restriction only help the argument.

With explicit partial trees, all restrictions, work/reward comparisons, and
column choices take polynomial time. Proper partial trees have at most n
leaves. The final proper full tree has n leaves and n-1 query nodes. Rational
arithmetic has polynomial bit complexity in the supplied x and policy data.
There is no optimum-tree, density, or pricing oracle in this compilation.

## 2. The compact template LP and its layer decomposition

Fix R supplied complete original-question templates B_k. For each internal
query node and each singleton leaf v, introduce `z_kv>=0`; require
`z_child<=z_parent`. For each hypothesis h require
`sum_k z_(k,leaf_h)>=1`. Minimize

    sum_(k,v internal)|S_kv| z_kv.                         (2)

The LP has `O(Rn)` variables and constraints apart from the n coverage rows,
with integer coefficients of polynomial size. It is feasible, for example
by assigning one whole template value one and the others zero. Standard
polynomial-time rational LP optimization returns an exact rational solution
of polynomial bit complexity. No claim is made that (2) is an OPT lower bound
for arbitrary original-test trees.

For one template, list its distinct positive z-values as
`0=a_0<a_1<...<a_t`; there are at most `2n-1`. For each j form a prefix policy
P_j by querying exactly internal nodes with `z_v>=a_j`, and stopping at any
excluded internal node. Monotonicity ensures the included query nodes form
a valid prefix-closed set. Give P_j coefficient `a_j-a_(j-1)`. Then

    sum_j (a_j-a_(j-1)) W(P_j)
      =sum_(v internal)|S_v| z_v.

The same threshold identity holds for the **declared** inclusion of each
singleton leaf. A technical leaf convention is worth stating: executing its
parent query already completes a singleton child even if that child's own
z-value is below the threshold. Thus actual completion coverage is at least
the leaf z-value, which is all the compiler requires. One must not pretend
that an already singleton response branch can be left unresolved.

Across all R templates, this produces `O(Rn)` explicit partial policies with
rational coefficients. Their actual completion sets cover each h at weight
at least `sum_k z_(k,leaf_h)>=1`, and their total fractional work equals (2).
Apply Section 1 to obtain an actual original-question full tree with cost at
most the LP value. Large root z-values are permitted: coefficients are
fractional-cover weights, not probabilities required to sum to one.

For n=1 the compiler returns the zero-cost singleton tree directly. If partial
templates are used instead, only actual singleton leaves may receive coverage
variables and LP feasibility must be checked; the complete-template statement
avoids that qualification.

## 3. Scope of the positive result

The LP can combine exponentially many abstract prunings of each supplied
template through its compact node variables, but its particular solution
decomposes into only polynomially many threshold policies. The compiler may
restrict and interleave these policies in ways absent from the original
template list. This is authorized by the use of actual original questions
and is the reason the final code need not be one of the templates.

This does not synthesize useful templates or solve the unrestricted column
pricing problem. No full-set integrality-gap conclusion should be transferred
to a target-cohort-only cover that omits completion coverage for outsiders:
the positivity and covering sum in Section 1 use every original hypothesis.

No material flaw was found in the theorem, layer decomposition, or polynomial
complexity claim.

## 4. Subsequent implementation audit

Independently read the saved `research-general-template-cover-lp.py` and its
companion note. The critical implementation agrees with the proof:

* Node prices are summed only over internal nodes and give the stated
  objective exactly; actual singleton-leaf coverage is checked separately.
* `profit_prefix` suppresses constant questions, stops unresolved branches
  with zero reward, and gives every actual singleton its full fixed price.
  Its lexicographic score breaks zero-profit ties in favor of more actual
  completions, ensuring the selected nonnegative-profit prefix is productive.
* Every unfinished exit of a productive prefix is a strict subset of the
  current state. Thus cached recursive construction cannot call itself on
  the same unfinished state, and potential induction applies to every graft.
* `layer_decomposition` uses the exact distinct rational thresholds and
  actual partial-tree completions. Its cost identity and coverage inequality
  are checked against the independent explicit-cover compiler.
* The implemented LP convention includes `z<=1`; the note correctly explains
  that clipping larger feasible values to one preserves monotonicity and
  leaf coverage. No LP optimizer is implemented or claimed to have run.

An independent rerun passed all 36 compact feasible points, all 155
decomposed-policy checks, and the 256-hypothesis switching example. That
example compiles objective 3456 to actual raw cost 2112, with two productive
applications, while each supplied complete template costs 3807. No material
implementation issue was found. The checker uses no unrestricted optimum
oracle, and this audit did not modify its code or the article.
