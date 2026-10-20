# Causal resources: a near-exact target pricer and a composition warning

Auxiliary research note, 18 October 2026. No article files were changed.
This pass did not obtain a stronger universal causal LP. It obtained a
polynomial near-exact **weighted target-pricing algorithm**, an explicit
realization of its lower certificate in the existing pair ledger, and a
direct-product obstruction to a root-only certificate/palette dichotomy.
No unrestricted approximation improvement is claimed.

## 1. Why partition-cover and pricing quality must be distinguished

Primary literature checked:

* [Jain–Klauck, *The Partition Bound for Classical Communication Complexity
  and Query Complexity*](https://arxiv.org/abs/0910.4266), introduces
  partition LP lower bounds for randomized query and communication models.
* [Jain–Lee–Vishnoi, *A quadratically tight partition bound for classical
  communication complexity and query complexity*](https://arxiv.org/abs/1401.4512),
  introduces the public-coin variant and proves quadratic relations for
  the logarithm of its value in those models.

Their bounds do not supply a polynomial separation oracle for the present
explicit promise matrix or a linear-factor rounding theorem for uniform
average depth. The constraints, query model, objective, and representation
must be checked before using those results.

The exact full-completion LP in the existing
[LP note](research-general-lp-next.md) has value \(F^*\), but this exactness
need not survive after requiring coverage only of a target subset. The
root agent's [target-coalition note](research-general-target-coalitions.md)
constructs a logarithmic gap for that restricted-cover LP. The independent
audit confirms its proof. Crucially, the same example nevertheless has a
near-exact polynomial **weighted target-pricer**, as proved next.

## 2. Model and polynomial algorithm

There are \(N\ge1\) target hypotheses \(C\) and \(u\ge1\) outsiders \(O\).
The allowed tests are:

1. A supplied family of target caps \(S_i\subseteq C\), covering \(C\).
2. Every target singleton query.
3. Every outsider singleton query.

Outsiders answer zero to every target cap and target singleton. Completion
prizes \(w_h\ge0\) are arbitrary on \(C\), and zero on outsiders. Let
\[
 B=\max_i\sum_{h\in S_i}w_h.
\]
If all prizes vanish the pricing problem is trivial; otherwise \(B>0\).

Choose a maximum-prize cap. Query it, identify all targets on its positive
branch by their supplied singleton tests, and stop its negative branch
unfinished. This is an actual original-test partial policy. If the chosen
cap has size \(s\), its reward is \(B\), and its raw work is
\[
 W_{\rm cap}=u+N+L_{\rm sing}(s),\qquad
 L_{\rm sing}(s)=s(s+1)/2-1\quad(s\ge1).
\]
Here \(L_{\rm sing}(1)=0\). Because
\(N+L_{\rm sing}(s)\le N^2\), its density satisfies
\[
 \frac{\text{reward}}{W_{\rm cap}}\ge\frac{B}{u+N^2}.        \tag{1}
\]
Scanning all caps and selecting the best actual density can improve this
candidate. Computing the cap prizes and emitting the singleton code takes
polynomial time in the explicit input.

## 3. Exact global lower certificate

**Theorem.** Every executable partial policy \(P\), regardless of which
outsiders it also identifies, satisfies
\[
 W(P)\ge \frac uB\sum_{h\in C(P)\cap C}w_h.                 \tag{2}
\]
This holds for every \(u\ge1\); the condition \(u\ge2N\) needed in the
elementary default-spine audit is unnecessary.

**Pair-ledger proof.** For each target–outsider pair \((h,o)\), assign price
\[
 p_{ho}=w_h/B.
\]
Give its full completion prize to \(h\), and none to \(o\). Charge this pair
once, at its first common separating query:

* At a target cap or target singleton query, charge the outsider endpoint.
  Each outside hypothesis receives total load at most
  \(w(S_i)/B\le1\). A target singleton is contained in a cap, so the same
  bound applies to it.
* At outsider singleton query \(o\), charge the target endpoint. Each
  target receives load \(w_h/B\le1\).

These are simultaneous pointwise endpoint/query capacities, not budgets
restarted at different tree nodes. At every actual query node the total
charge is at most its population. If target \(h\) is completed, it has
been separated from every outsider, so all \(u\) pair prices paying \(h\)
have been charged. Summing proves (2).

Equivalently, \(y_h=uw_h/B\) on targets and \(y_o=0\) on outsiders is feasible
for the **full executable-completion dual**. This is a global causal
statement against all partial policies. Its representation already belongs
to the pair-completion ledger from
[the certificate note](research-general-certificate-algorithm.md), and is
not a newly stronger LP cone.

Together, (1) and (2) show that the explicit cap algorithm approximates the
maximum weighted target-pricing density within
\[
 1+\frac{N^2}{u}.                                         \tag{3}
\]
In the root agent's \(u=N^3\) family, the ratio is at most \(1+1/N\).
The selected cap's actual singleton decoding cost gives a sharper
instance-specific ratio \(W_{\rm cap}/u\).

## 4. Why the restricted-cover gap does not contradict this algorithm

The root construction takes targets to be the \(k\)-subsets of \([r]\)
and caps \(S_i=\{A:i\in A\}\). The target-cover LP has a feasible fractional
solution of weight \(1/k\) on each cap coalition, while covering all targets
integrally requires at least \(r-k+1\) caps. Large outsiders make activation
work dominate target decoding, giving a logarithmic restricted-cover gap.

Pricing asks for the best prize/work ratio of **one executable policy**,
rather than integral coverage of all targets. A maximum-prize cap already
has near-optimal pricing density, as (2) proves. Thus neither that
restricted-cover gap nor a partition-style relaxation gap automatically
implies hard pricing. The root's full-H LP exactness and its pricing-to-UDT
reduction remain intact.

The present algorithm prices target-supported weights. It is not an
arbitrary-weight pricer when outsiders have positive prizes, and it is not
an unrestricted decision-tree approximation.

## 5. A root-only pair/palette dichotomy fails under direct product

Another question in this pass was whether weak pair certificates might
always coincide with a small identifying palette of test rows. A root-only
version fails even after adding root entropy.

Let \(A=\mathbb F_Q^d\), \(a=Q^d\), with all affine-hyperplane equality
tests, and let \(B=\{1,\ldots,t\}\) with all threshold tests. The new uniform
instance is \(H=A\times B\), with queries acting on only one coordinate.
Its optimum mean is exactly the sum of the two component optimum means:
condition on the second coordinate and suppress constant threshold queries
to lower-bound affine work, and condition on the first coordinate to
lower-bound threshold work. Sequential component codes attain the sum.
Thus, with \(d=\lfloor Q/\ln Q\rfloor\) and \(t=a\),
\[
 F^*(H)=\Theta(nQd),\qquad n=at=a^2.
\]

Every threshold boundary is necessary in any identifying palette: the two
adjacent labels at that boundary, with the same affine coordinate, disagree
on exactly that threshold among the supplied queries. Hence every palette
contains at least \(t-1=\sqrt n-1\) distinct tests.

Yet the pair Bellman potential remains weak. Split its objective into pairs
with distinct affine coordinates and pairs in the same affine fiber.
Sum full-root affine-test capacities for the first class. There are
\(M=Q(a-1)/(Q-1)\) tests, and each such pair is separated by \(R=2a/Q\), so
\[
 P_{\rm cross}(H)\le nM/R=O(nQ).
\]
For a fixed affine coordinate, restrict the capacity inequalities to its
\(t\)-point threshold fiber. Its pair potential is at most its optimal
threshold raw cost \(L_2(t)\). Summing fibers gives
\[
 P_{\rm within}(H)\le aL_2(t)=O(n\log t).
\]
Nonnegative pair features justify both restrictions separately. Therefore
the entire pair cone has value \(O(nQ+n\log t)=O(nQ)\).
Any valid added nonnegative root entropy coefficient is at most one,
so root entropy adds \(O(n\log n)=O(nQ)\) as well.

This disproves a dichotomy between a strong **root** pair/entropy
certificate and a small **global** palette. It does not defeat conditional
balanced routing: threshold-first search routes to an affine fiber, where
the supplied coordinate palette is small. Rather, it makes the missing
structural requirement precise: any useful theorem needs conditional
decomposition and shared global charging, not only the two root scalars.

The root agent's separate
[product-decomposition note](research-general-product-decomposition.md)
develops automatic recovery of exact Cartesian query factors using
symmetric submodular entropy minimization. That is a constructive response
to this particular product obstruction. The obstruction above remains
useful for the root-only dichotomy; it does not purport to defeat that
decomposition or its factorwise algorithms.

## 6. Checks and remaining task

The companion script audits the pair ledger and near-exact pricing theorem
against exact subset pricing DPs on small target/outside matrices, with
arbitrary integer target prizes. It also computes the explicit large-outsider
cap code's exact ratio bound and checks finite direct-product test counts
and necessary threshold boundaries.

No stronger universal causal LP was obtained. The general missing task is
still a polynomial code-or-certificate alternative covering arbitrary
incumbent weights and arbitrary test matrices, with a ratio below
\(O(\log n/\log\log n)\).
