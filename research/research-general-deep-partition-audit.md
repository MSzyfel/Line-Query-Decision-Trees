# Independent audit of the deep-partition LP and branching compiler

Auxiliary review, 19 October 2026. This audits Sections 2–4 of
`research-general-coupled-branching.md`. The article is unchanged.

**Finding:** the full-column identity and lossless compiler are sound for a
downward-closed acceptable-state family. The copied-flow LP represents real
fractional bounded-menu adaptive policies. Its compiler can leave the
original bounded-horizon search class by restarting the virtual program;
this is legal and polynomial, but should be stated explicitly. None of these
claims proves that a proposed menu competes with unrestricted OPT.

## Full-column value identity

Fix an optimum tree T whose output cells are acceptable, and put y_h equal
to its depth. Append T restricted to the unacceptable outputs of any partial
policy P. Each new output is a subset of a T output, so downward closure is
exactly what makes the appended policy feasible. Its additional cost is at
most the sum of y_h over hypotheses not already settled by P. Cancelling
against the optimum value proves the claimed policy-column dual inequality.
No assumption about geometric embedding, uniform cell size, or singleton
outputs enters this cancellation.

## Fractional-cover compilation

For the fixed prices `v_h=sum_j x_j d_j(h)`, restriction to any actual state S
cannot increase any original path's work. An originally acceptable output
remains acceptable after intersection with S. These facts yield the weighted
nonpositive difference in equation (4) of the coupled-branching note.

Columns with no original settled hypothesis in S have nonnegative
differences. The remaining columns have positive total cover on every h in
S, so at least one productive column has a nonpositive difference. Its work
is paid by the prices of the hypotheses it settles. Recurse only on its
unacceptable exits. Every productive call settles at least one previously
unfinished h, so the total number of calls is at most n. Extra acceptance
created by restriction only lowers the final cost.

## Copied action weight in the unfolded search structure

The equality `w_child=x_(parent,action)` at **every** response exit is the
correct one. These are probabilities of including a structural policy
subtree, not probabilities of the hidden hypothesis following that exit.
An ordinary mass-conserving network-flow constraint would represent the
wrong object.

Normalize by the root incoming weight. At each reached state, independently
choose one action according to its fractional outgoing weights, or stop
with the unused weight. Choosing an action includes *all* its response
subtrees. The resulting random object is a deterministic adaptive policy,
and induction gives the advertised node-inclusion probabilities. The LP
objective is its weighted expected raw work; coverage is its weighted
expected acceptable completion. A free root weight allows a fractional sum
of policies whose total weight exceeds one. This is needed for covers by
partially productive policies.

The direct AND/OR profit optimizer may restart that fixed virtual structure
on a newly observed actual S. An occurrence originally concerning S_u then
executes on `S intersect S_u`; all tests are still original legal tests.
For a macro, early acceptance inside its explicit tree must earn the actual
state's price and stop that branch. Unreached original exits have empty
intersection and no contribution. This is compatible with the restriction
inequality used above.

After several productive restarts the final output need not obey the
original d-action horizon or the state-dependent menu at its newly observed
states. The proof only needs original-test legality, polynomial size, and
the fixed-price work bound, all of which remain valid. The restricted LP
may therefore be cheaper than every single bounded-menu policy while still
compiling to a legal global policy; that is not a contradiction.

## Bounded independent verification

`research-general-deep-partition-audit.py` independently computes optimal
acceptable partitions and the all-policy maximum-profit recurrence on tiny
response matrices. The exact all-subset optimizations are validation only,
not algorithm inputs or polynomial solvers.

The saved run covers 56 downward-closed target instances: fixed cardinality
caps and sets containing no supplied forbidden pair. Optimal depths satisfy
every partial-policy inequality, as checked by the exact maximum-profit
Bellman recurrence; all root maximum profits are zero. The audit evaluates
3,887 cached subset profit values. It also constructs 144 template-prefix
columns and tests a separate fixed-price compiler on explicit feasible
fractional covers with overcoverage, making 52 productive calls. All actual
partitions are acceptable and have cost at most their fractional objectives.

This checker does not optimize the compact copied-flow LP or test a claimed
unrestricted approximation ratio. The copied-flow representation and its
direct AND/OR implementation are justified by the decomposition argument
above; the root's separate branching checker tests its actual search code.
