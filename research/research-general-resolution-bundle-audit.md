# Independent audit of the two-selector bundle obstruction

Auxiliary review, 19 October 2026. This audits
`research-general-resolution-bundle-obstruction.md` without editing its
proof or the article. No material flaw was found. The result applies to
individual one-response fresh-greedy templates and all their prunings;
it does not cover interleavings, repeated synthesis, or the stronger
lifting/intersection generator.

For an arbitrary equality-only partial policy on a uniform product, fixing
all coordinates except one and suppressing their deterministic queries
leaves a pruned singleton comb on that coordinate. If it has \(t\) proper
queries on an \(r\)-point coordinate, its expected work is at least \(t/2\),
its entropy is at most \(t(\log_2r+\log_2e)/r\), and its expected number of
positive answers is \(t/r\). Averaging over the fixed coordinates counts
each original query once. Independence gives
\(H(\mathrm{transcript})\le\sum_i I(X_i;\mathrm{transcript}\mid X_{-i})\).
Together with the querywise integer-coding bound
\(\Delta L\le s h_2(b/s)+2b\), this proves the stated
\(O(\log M/M)\) coding-drop/work inequality even for unequal stopping
depths. It does not incorrectly bound each late balanced query separately.

On the complement of a gated positive response, a body value's normalized
multiplicity is between \(M^2-1\) and \(M^2\). The interval, rather than an
assertion that every averaged multiplicity equals an endpoint, is what
the greedy comparison requires. Every unfixed body offers a more balanced
equality than any selector or gate. Once all bodies are fixed, a gate is
a singleton selector-pair test and is dominated or tied by a pure equality.
The prescribed order therefore proves the equality-only continuation
claim.

Replaying a pruning of that continuation on the full product produces
rectangular states and only proper queries: each query was already proper
on the negative response. Its exact incumbent restriction credit equals
its work. Commuting the gate through the replay gives the stated exact
identity, including subtraction of the nonnegative credit of the replay
restricted to the positive response. Unrelated body-coordinate costs
cancel in each leaf gate credit. Leaves with an unknown body retain both
full selector coordinates; body-known leaves contain at most one positive
point. These two cases justify the total \(4n/M\) gate-credit overhead.
The replay's extra work on positive hypotheses is at most
\(|A|H_{\rm eq}\), as claimed.

The elementary estimate
\[
 \eta+4/M\le 5/M+1/(8\log_2 M)<1\qquad(M\ge16)
\]
makes the work comparison explicit. The positive-response argument and
the refinement/superadditivity argument for the coding drop are also
valid. Consequently both \(\Gamma_T(P)\le W(P)\) and
\(\Delta L(P)\le C_M W(P)\) hold within the stated library, with
\(C_M=O(\log M/M)\). In particular, no individual allowed pruning gives a
strict actual incumbent-fallback improvement on the initial tree.
This is a restricted algorithm/proof-class obstruction, not an
unrestricted decision-tree inapproximability result.
