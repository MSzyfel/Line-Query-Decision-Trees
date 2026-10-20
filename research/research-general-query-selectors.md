# Selecting response quotients by information and disjointness

Auxiliary research note, 19 October 2026. The article is unchanged. This
adds an explicit polynomial portfolio of query families to the
[factor-context planner](research-general-factor-contexts.md). It has
proved coverage on two new camouflage families and finite executable
improvements. No unrestricted approximation guarantee follows.

## 1. Why root minority alone is insufficient

The [rotating-alias family](research-general-rotating-aliases.md) has
selector alphabets of size M and body alphabets of size M/2. Every selector
equality and every physical gated bit has root minority n/M; body
equalities have minority 2n/M. All useful cutoff levels therefore either
keep the misleading gates with selectors or discard both. Ordinary greedy
still spends Theta(M²/log M) queries on body equalities, whereas an actual
selector-first code costs O(M) for a fixed number of selectors.

This is a proved failure of support-size separation and of a particular
slice-projection premise. It is not a fixed-point theorem for the strongest
lifting algorithm. The new selectors below act on the actual response
matrix and do not require supplied latent coordinates.

## 2. One exact independence refinement

An initial query family gives a factored response-support quotient, with
factor labels Z_1,...,Z_d. For every subset A of these factors, let Z_A be
its joint label. Retain every original test q whose response is statistically
independent of Z_A under the **actual uniform original hypotheses**.
For each label event z and response a, the exact test is

    n count(q=a,Z_A=z)=count(q=a) count(Z_A=z).

It uses integer counts, with no logarithms or numerical tolerance. There
are at most 2^d<=N<=n factor subsets per initial quotient. This is another
place where the explicit Cartesian support makes an apparently exponential
enumeration polynomial.

Independence of each selected query does not imply joint independence of
their whole response vector. For independent bits X,Z, both X and X xor Z
are independent of Z, while their joint vector determines Z. The algorithm
does not make that invalid inference. It simply factors the actual support
of the selected query family, then plans actual original-test codes using
the resulting labels and original multiplicities.

On the rotating family, a high cutoff first reveals the body factors.
Every gate is dependent on its target body: fixing its zero row changes
its positive probability from 1/M to 2/M. Pure selector tests are independent
of the whole body vector. Selecting tests independent of that vector
therefore leaves exactly the pure selector family. Its quotient factors
recover the selector axes; the context planner then includes the cheap
selector-first/body-code program. No useful incumbent slice is required.

## 3. XOR cancellation defeats independence selection

The [XOR camouflage note](research-general-xor-aliases.md) modifies a body
label to Y_j=Z_j xor t_j(C), with a selector-dependent uniform mask inside
each activation group. Each physical gate is now independent of every
fixed full body tuple. Independence selection keeps the gates along with
the selectors. The selected response relation is identifying and prime:
it has one factor containing all n hypotheses.

The analytic statement covers every subset of the body factors exposed
by the initial high cutoff, not just their full vector. Exact factorization
confirms the prime relation on bounded instances. Ordinary greedy retains
the full asymptotic gap. Several standalone completed lifts of the obvious
body-fixed source are more expensive than the incumbent. These facts do
not establish stability of the full global code library.

This cancellation is why independence selection is only a candidate-family
generator, not a proof that all selected responses involve a complementary
set of latent variables.

## 4. Whole disjointness components expose partition seeds

For each occurring response-cell size B, collect distinct original cells
of that size, allowing either response of a binary test. Build a graph
whose edges join disjoint cells. Compute its connected components. Accept
a component only if all its cells are pairwise disjoint and their union
is H. It then supplies a genuine uniform partition through actual original
response cells.

The algorithm tries whole components. It does not solve maximum clique,
search for a hidden subfamily, or assume arbitrary partition recovery is
polynomial. Its limited menu can fail when extra queries bridge components.

Keep each accepted partition's query family, the union of accepted
partitions at each cardinality B, and the union of all accepted partitions.
Different-cardinality families remain separate candidates; singleton noise
must not silently contaminate every useful partition family. The total
number of candidate families is polynomial in n,m.

On the XOR family, all selector equalities in one coordinate form a
disjoint M-clique covering H. They have no disjointness edges to any gate:
the activation form remains surjective when one selector coordinate is
fixed, and the body value can realize the requested bit. Gate cells from
different body rows intersect because their activation forms are pairwise
independent. Within one body, different activation groups are disjoint,
while different bits of the same group intersect.

Consequently the whole components at size n/M are precisely the selector
partition cliques and the body-gate components. A body-gate component
either is not pairwise disjoint, or has only one bit per group and covers
half of H. It is rejected. The accepted union recovers exactly the pure
selector queries. Their partial greedy decoder exposes full selector
fibers, where fresh greedy runs the cheap body codes. The source labels,
activation forms, and selector roles are not supplied to this procedure.

For L=floor(cM/log_2 M), fixed selector count k, the proved comparison has
mean at most k e(M)+L log_2(M/2), while information gives mean at least
log_2 n. Its class-specific ratio is at most 1+k/(2c)+o(1). Thus this menu
also escapes a full-order greedy gap on the XOR family. It does not prove
that every prime quotient contains a recoverable partition component.

## 5. The implemented portfolio and its polynomial bound

[The implementation](research-general-query-selectors.py) freezes these
initial families: all global-minority cutoffs and the whole-component
partition families above. For every initial family it computes the support
factorization and tries one independence refinement for each factor
subset. Newly selected families do not seed another refinement level.
Deduplicate the resulting families, run the factor-context planner on
each, and retain all actual context/factor-decoder/fresh-code states.

Finally run the existing incumbent-depth-prize DP on the union of those
states, with actual incumbent restriction at unresolved exits. Every
complete candidate is supported, so the result is no more expensive than
the cheapest candidate or the original greedy tree. This recombination
does not assume that independent query families have independent costs.

There are O(n+m) initial families, at most n factor subsets per family,
and at most n^(log_2 3) contexts per selected family. Every factor planner
and exact count comparison is polynomial. Thus one fixed refinement level
and supported-policy recombination have a fixed-exponent polynomial
runtime. Repeating this selection recursively without a bound is not part
of the algorithm.

## 6. Exact finite checks

The checker passes 24 complete small portfolio executions, 838 exact
independence-event checks, and 32 accepted-partition checks. A four-point
XOR example explicitly verifies the joint-independence caveat. The
unrestricted exact subset solver appears only in finite validation.

On the n=128 rotating instance, the automatically selected selector family
gives 1072 versus ordinary greedy 1073. The full eight-family portfolio,
including depth-prize recombination, gives 1065 from 240 summed contexts
and 540 distinct pool states.

On n=64 XOR camouflage, the full 21-family portfolio gives 400 versus
ordinary greedy 404. Its four accepted partition components include the
two selector partitions at the correct cardinality; it has 681 summed
contexts and 458 distinct pool states. These are actual original-query
outputs, not exact optimum claims or evidence of a universal ratio.

Run `python research-general-query-selectors.py`; results are saved in
[JSON](research-general-query-selectors-results.json). The next obstruction
under investigation adds correlation-cancelled bridge queries that merge
these components. Even if that menu is defeated, its failure would not
establish hardness for the unrestricted problem or for the larger global
lifting/intersection algorithm.
