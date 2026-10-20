# Independent audit of filtered conditional sources

Auxiliary review, 19 October 2026. This audits
`research-general-filtered-sources.md/.py` without editing them or the article.
No material defect was found in the stated binary-test subclass theorem.
There is no unrestricted approximation claim.

The filter separation is strict: every non-pure gate has positive mass at
most Dn/M^k<n/M, even after its target body has been fixed by equality.
Consequently ordinary greedy really completes all bodies before selectors,
and the full-selector, fixed-body slice is an actual incumbent node. At the
global root threshold n/M all pure equalities remain and every gate is
removed. Replaying this filtered source therefore produces exact full
selector fibers, with no assumption about conditional code behavior on an
outsider. Completing all replay exits uses at most n leaves in total.

The arbitrary-nonlinear per-row Pb_j bound is sound. Once selectors are
fixed, every proper query depends on one body only, so even an interleaved
global history preserves independent uniform surviving row subsets. At the
first pure singleton equality on a row, every unqueried owner bit has
minority count at most one. Previously asked owner bits are constant. Since
the owner labels are distinct, all but at most one surviving row value lie
in one of at most b_j-q singleton minority cells. Thus s-1<=b_j-q.
There were at most q+(P-1)b_j earlier bit queries, and every proper row-query
continuation has path length at most s-1. The sum is at most Pb_j. This does
not require a shared affine labeling, palette blocks, or consecutive queries
on the same row. P must bound incoming palettes per actual context/body;
the outgoing activation bound D serves a separate role.

The optimized joint resource uses a single feasible endpoint budget.
For a gate, each inactive hypothesis can receive at most D cut selector-pair
edges. Each active hypothesis can receive at most D-1 active-active edges,
and at most lambda coding load. With
`w=1/(D+q-1), lambda=q/(D+q-1)`, the two bounds are respectively
`Dw<=1` and `(D-1)w+lambda=1`. Selector equalities receive at most one
pair weight per hypothesis and no fiber coding deficit. Body equalities
receive no selector-pair weight and at most lambda<=1 coding load. The
coding deficit is at most the fiber population because an unconstrained
binary optimal code can ask that physical query and then use optimal codes
in its responses. The same assignments remain valid on every subset;
deleting other endpoints only decreases pair loads. This justifies the
Bellman lower bound, rather than summing independent full-strength ledgers.

The final comparison also checks algebraically:
`ke(M)/(k(M-1)/2)=1+2/M`, and
`B/(L_2(N)/N)<=1+1/log2(r_min)`. Choosing q=P matches the actual fiber
completion guarantee and yields the displayed D+P-1+o(1) class ratio.
No hidden enumeration exponent depends on k: the algorithm enumerates at
most 2n-1 actual incumbent states and at most n global minority thresholds,
then performs ordinary polynomial tree operations on frozen sources.

An independent bounded execution of `check_case(4,2,(2,),2,True)` passed.
It has n=32,m=26, initial raw cost172, the displayed filtered comparison176,
and all93 frozen-state/threshold menu candidates retain the incumbent172.
This is consistent with the note's warning that the conservative comparison
need not improve every finite case. Its maximum fiber depth is1, below the
proved bound2. No exact OPT call or adversarial search was used in this audit.
