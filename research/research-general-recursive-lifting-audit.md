# Independent audit of serial recursive lifting

Auxiliary correctness audit, 18 October 2026. I read
`research-general-recursive-lifting.md/.py`, the actual `source_codes`,
`generated_pass`, `lift_partial`, and `finish_partial` implementations, and the
underlying supported-state depth-prize DP. I found **no mathematical defect in
the stated family-specific theorem**. No article or audited source was edited.

## Sources and state coverage

The initial greedy claim uses the stated order and strict alphabet decrease.
While coordinate `i` has `s` remaining values, its equality minority is `1/s`.
Lower-coordinate equalities have smaller minority; undecoded gated bits pay a
lower-context probability; already fixed higher-coordinate bits are either
constant or exact lower-context indicators. The only relevant tie without a
further context penalty is at coordinate 0, where its equality queries precede
all higher-factor gates. This also proves the pure-equality behavior on the
fixed-higher-coordinate incumbent slices.

The slice with coordinates `k,...,L` equal to zero is an actual incumbent node:
equality values are ordered with zero first. Its fresh greedy code is explicitly
requested by `source_codes`. Its physical tests depend only on lower
coordinates, so its global lifted leaves are exactly all lower-context fibers
`S(k,b)`. Completion at a lifted leaf retains that cell as the fallback root.
Consequently these fibers really are generated **base** states; there is no
recursive sourcing assumption.

The forced-positive LSB domain is also explicitly requested: it is a proper
child of a supplied query at the incumbent root. On that domain, odd values
identify with the consecutive integers `0,...,Mk/2-1`. Fixing arbitrary binary
coordinates leaves an initial segment in the numeric order of the remaining
free binary coordinates. Its least free coordinate therefore alternates zero
and one, giving a floor/ceiling split. For at least two remaining values an
active bit has minority at least `1/3` (and `1/2` for two). Higher equality
minorities are at most `1/6`; a higher gate has positive probability at most
`1/(2s)`. Current-factor equalities can tie, but come after its bits. Thus the
claimed initial decoding prefix really occurs in the complete fresh source.

Every global cell `P` of this prefix occurs in the full lifted source as well:
before the prefix ends both source children are nonempty, and at its endpoint
the complete source either continues from that same cell or receives a
fallback rooted there. Clipping by the known fiber gives exactly
`S(k,b) intersect P`. The terminal pair is `2v,2v+1`, since every odd value has
its even partner under the even-alphabet assumption. Querying the final LSB
then reaches the two already generated next-context fibers. Hence every
comparison-tree state has a genuine intersection-of-two-base-states witness.
No repeated-intersection closure whose exponent grows with `L` is being used.

## Lower bounds, runtime, and actual output

All physical positive supports are bounded by `B=n/ML`; the common rare-positive
orientation, rather than just an unoriented minority bound, is important.
Since `L>=1`, here `B>1`. At each all-negative depth
`t=0,...,ML-1`, at least `n-tB>=B>1` hypotheses remain, so that node must issue a
query. Before the last such node the negative branch is necessarily nonempty.
Thus summing `1-t/ML` really proves `OPT>=(ML+1)/2`; there is no singleton-leaf
endpoint error. The separate `log2 n` information bound and the displayed
`rho+1+1/log2 ML` ratio follow. For `B=1` the last summand would require a
different argument, which the note explicitly excludes.

The growing-depth choice `L=floor(M/log2 M)` gives `log2 n=Theta(M)`, greedy
cost `Theta(M^2/log M)`, and a supported context-first code of cost `O(M)`.
The same family has `rho=1+o(1)`. The resulting full-order greedy obstruction
and constant first-pass guarantee are therefore compatible. The number of
factors can grow, while the generator still performs only its fixed polynomial
source requests and quadratic state closure. Its running-time exponent does
not depend on `L`; this is polynomial in the explicit response-matrix size,
not necessarily practical at the conservative worst-case exponent.

Finally, a complete supported comparison code earns all incumbent-depth prizes,
whose sum is exactly the incumbent raw cost. Its profit is
`F_incumbent-F_comparison`. Exact supported profit optimization, followed by
actual incumbent restriction at unfinished exits, returns a complete tree of
cost at most `F_comparison`; if the incumbent was cheaper, it already satisfies
that bound. Thus the conclusion concerns the executable first-pass output,
not only existence of a code inside the represented family. The optional
weighted and actual-boundary variants include the same sources and comparison
code, so their first-pass upper bound is valid too.

## Bounded independent check and scope

I independently reran `coverage_certificate((8,6))`: `n=48`, `m=38`, initial
raw cost `370`, comparison and reduced-family output both `338`, and all `95`
comparison nodes certified in the quadratic family. The run used no exact
optimal-subproblem oracle. I did not launch a larger search.

The result depends on the specified priority, even alphabets, pure context
queries, and source generation on forced query children. It does not establish
an unrestricted approximation, nor defeat a family with dependent or aliased
context semantics. Within its explicit scope, the proof is sound.
