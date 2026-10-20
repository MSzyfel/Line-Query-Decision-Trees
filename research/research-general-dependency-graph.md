# A polynomial 2-approximation for graph-gated factorial tests

Auxiliary research note, 19 October 2026. The article is unchanged. This is a
structured-class theorem, not an unrestricted decision-tree approximation.

**Main result.** On a uniform product whose questions are coordinate
equalities and private coordinate-bit palettes gated by specified parent
values, a count-vector dynamic program gives a polynomial-time
**2-approximation**. It permits partial equality searches on several
coordinates, so it is stronger than choosing an order of fully decoded
factors. Its crucial comparison charges a full local code whenever activation
reveals a coordinate: every extra simulated equality check is paid for by a
successful check that saves that coordinate's later activation charge. The
comparison is pathwise. No feedback-vertex-set approximation is needed.

## 1. Model and an exact complete-factor benchmark

Let `H=[M]^d`, uniformly distributed, with `M=2^b>=2`. Supply all coordinate
equalities `xi=v`. A directed graph specifies parents `Pa(i)` of each
coordinate. For every parent-value tuple `a` and each of the `b` bits of `xi`,
supply the private test

    q(i,a,j)=1 iff x_Pa(i)=a and bit_j(xi)=1.

For a root, its palette is global. Self-parent loops can either be excluded
or treated literally; the algorithm and simulation below still work with
them. A full explicit table has polynomially many entries in `n=M^d`.

At a full-factor context, a block decoder for coordinate i costs `b` if all
its parents are known. Otherwise its useful factor-local tests are only
coordinate equalities or their equivalent singleton partitions, so it costs
`e(M)=(M+1)/2-1/M`. Conditional eligibility inside that block does not produce
an additional nontrivial bit query: any still-unknown parent makes each
target-bit-one value inconsistent, while target-bit-zero values make the
query constant. Gates on another already known target can at most provide a
singleton equality on i.

For a complete-factor order, let F be the coordinates decoded before at least
one of their parents. Then deleting F leaves an acyclic graph. Conversely,
decode a feedback vertex set first, then topologically decode the rest. Thus
the least complete-block mean is exactly

    d b+(e(M)-b) f(G),                                     (1)

where `f(G)` is the minimum directed feedback vertex set size. Value-adaptive
factor orders cannot improve this formula: each block has the same uniform
conditional cost independent of the previously observed values, and each
path's expensive set is a feedback vertex set. Computing `f(G)` by `2^d`
subset enumeration is polynomial in the explicit `n=M^d`, since `2^d<=n`.
Equation (1) is a benchmark for complete-factor blocks, not a lower bound on
unrestricted adaptive decision trees.

## 2. A charged-activation abstraction with only n count states

An oracle relaxation keeps independent candidate sets for all coordinates.
It may ask any ordinary coordinate equality at unit cost. Whenever all
parents of a still-unknown coordinate i are known, reveal its full value and
charge `c_i=b`; apply this rule repeatedly. In particular, root coordinates
are revealed and charged at the start. An equality hit or last-candidate
miss identifies its coordinate directly, without an activation charge, and
may trigger the same activation closure. More generally the proof permits
any fixed supplied complete-palette cost `c_i>=1`.

All remaining unknown coordinates have only equality-search histories. Their
posteriors are independent and uniform on their surviving candidate sets.
The optimal expected paid-plus-activation cost depends only on the candidate counts
`r=(r1,...,rd)`, not on which values remain. The activation closure `cl(r)`
sets `ri=1` whenever every parent already has count one, until stable. Its
charge is

    C(r)=sum_(i: ri>1 and cl(r)i=1) c_i.

Write `V(r)` for the minimum remaining paid-plus-activation cost. For a
nonclosed state,

    V(r)=C(r)+V(cl(r)).

At a closed state with all counts one, `V=0`. At any other closed state,

    V(r)=min_(i:ri>1) {1+(1/ri)V(r with ri=1)
                         +(1-1/ri)V(r with ri=ri-1)}.      (2)

A paid equality is a hit with probability `1/ri`. All choices of a remaining
value are symmetric. Each child reduces the sum of counts, so the recurrence
is acyclic. There are at most

    product_i M=M^d=n                                      (3)

count vectors, including unclosed vectors. There are at most d actions per
state, and closure is a polynomial graph operation. This is a fixed-exponent
polynomial DP in the explicit input, even when d grows with n.

Exact arithmetic also has polynomial bit complexity. For any count vector,
`(product_i ri) V(r)` is integer: it is raw charged query work on the corresponding
uniform product, with all activation revelations expanded into their actual
value branches. Its magnitude is at most `n [d(M-1)+sum_i c_i]`. Equivalently, in (2) one may
multiply child raw costs by the integer numbers of free-value branches.
Fractions therefore have polynomially many bits; no exact real oracle is used.

## 3. Simulating every unrestricted tree with a pathwise charge bound

Let T be **any** complete legal tree for the original graph-gated tests.
Simulate its queries in the abstraction while retaining all extra information
from paid equalities and charged full revelations. The simulator's state stays an
independent uniform product:

* A coordinate equality is answered for free if already determined. Otherwise
  ask that equality, paying one, and update the charged activation closure.
* For a gate `q(i,a,j)`, first check already known parents or values excluded
  from a parent's candidate set. A mismatch determines answer zero for free.
  Otherwise check the still-unknown parents one by one with their equalities
  `xp=ap`. The first miss determines answer zero. If all match, every parent
  is known, so activation reveals xi, if it is not already known, and its bit
  answers q without another paid equality.

Every simulated original answer is **entailed** by these coordinate checks
and full free revelations. The simulator never conditions additionally on an
unresolved conjunction. Consequently no cross-coordinate correlation is
introduced. The stronger simulator history determines the original T node,
so reaching that node imposes no further conditioning. Newly activated
variables can only eliminate further checks. A complete original T leaf is a
singleton; the simulator's smaller product cell must therefore also be fully
known.

Fix one target hypothesis h. Let `P(h)` be the number of positive **paid**
equality checks throughout this simulation. In simulating a gate with l paid
checks, each check after the first is preceded by a successful paid check:
the first failure stops the gate. Match its `l-1` extra checks injectively to
these preceding successes. A pure equality costs at most one. Thus pathwise

    paid_checks(h) <= depth_T(h)+P(h).                      (4)

Every positive paid equality identifies a previously unknown coordinate.
That coordinate remains known and is never charged for activation. The
positive-check coordinates are distinct, while every other coordinate can
be charged for activation at most once. As `c_i>=1`,

    paid_checks(h)+activation_charges(h)
      <= depth_T(h)+P(h)+sum_i c_i
                          -sum_(positive-check coordinates i) c_i
      <= depth_T(h)+sum_i c_i.                             (5)

Last-candidate negative equalities may identify additional coordinates without
activation charges; this only improves the bound. Roots are charged once at
the initial closure. Cycles and self-parent loops create no extra charges.
Taking expectations and comparing the optimal abstraction policy with this
specific simulator gives

    V_root <= OPTmean+sum_i c_i.                           (6)

No probability bound on successful checks is needed for (4)-(6). Uniformity
is used for the count-only DP, not for this pathwise accounting. In particular,
there is no need to charge overlapping directed cycles separately.

## 4. Executing the count policy with real tests

Run the policy chosen by (2), keeping the actual remaining values as well as
their counts. Each paid action is the supplied equality for any remaining
value. Whenever the abstract policy activates coordinate i, query its
physical gated palette using its now-known parent tuple; at most b questions
identify it. Skip any bit that is already constant on its surviving values.
This costs at most its charge `c_i=b`. Then continue the activation closure
and the count policy.

Every real query is either a supplied coordinate equality or an enabled
supplied bit. It affects only one coordinate, preserving a uniform product.
The actual paid equality work plus physical palette work is at most the
abstract paid-plus-charge objective, including root activations. Consequently

    ALGmean <= V_root <= OPTmean+d b <= 2 OPTmean,          (7)

where the last inequality is binary information `OPTmean>=log2 n=d b`.

The reconstructed proper binary tree has at most n leaves and n-1 query
nodes. Its explicit output size is polynomial. The DP counts all partial
equality-search progress rather than only unknown/known factor status; this
is why it can use adaptive activation opportunities missed by (1).

## 5. Scope and extensions

The proof also allows unequal coordinate alphabets `Mi` and a supplied private
injective palette of width `bi` at every parent tuple. The state bound becomes
`product_i Mi=n`, the charged simulation comparison (6) is unchanged, and the real
algorithm costs at most `OPTmean+sum_i bi`. When
`bi=ceil(log2 Mi)`, information gives an approximation bound

    1+sum_i ceil(log2 Mi)/sum_i log2 Mi <= 3,

with factor 2 for power-of-two alphabets or negligible total coding rounding.
The stronger stated theorem (7) uses full binary-cube alphabets. Context-specific
injective local labels are harmless: enabling still supplies a complete
single-coordinate code, and simulation answers a bit once that coordinate is
freely known.

The structure is essential. Every non-equality query must be one specified
parent conjunction and one target-coordinate bit. A physical test active in
several alternative parent tuples need not be answered after the first
equality mismatch; arbitrary cross-coordinate tests need not preserve the
simulator's product posterior. Unequal or correlated priors need not admit
this count-only exact DP. No such algorithmic generalization is asserted,
although the pathwise simulation remains valid whenever the same complete
activation palettes are supplied.

The graph and coordinate representation can be supplied as a class certificate.
It can also be recovered in polynomial time for the **loop-free canonical
`M>=4` cube model**. This is a recognition statement about exactly that family,
not arbitrary hidden representations:

1. Retain questions with global minority at least `n/M`. All pure equalities
   and global root bits survive. A nonroot private gate has support
   `n/(2 M^|Pa(i)|)<n/M`, so none survives. Cartesian factorization of the
   distinct retained response words recovers the coordinate axes. Each axis
   has all its equality indicators, whose one-hot support cannot split into
   two nontrivial independent factors. Additional root bits stay in that axis.
2. In these recovered coordinates, test both response cells of each original
   question for an axis-aligned Cartesian box. A pure equality has one
   singleton projection and all other projections full. A private gate has
   exactly one target projection of size `M/2>1`, singleton parent projections,
   and all other projections full. Check the full box equality, rather than
   just its projections. The target is unique; the parent tuple is explicit.
   Complemented question orientations cause no difficulty because both cells
   are tried. For a global root bit either orientation works.
3. Check that every target's questions have the same parent set. Group them by
   parent tuple; check that every parent tuple is present, and its canonical
   b rows give M different target response labels. All pure equalities must
   be present, and every question must have one of these permitted forms.
   The number of parent tuples `M^|Pa(i)|` is at most n. Constants and repeated
   questions can be discarded before recognition.

These checks use explicit response masks and integer arithmetic. If M is not
given, try all power-of-two alphabet sizes dividing n with integral
`d=log_M n`; there are at most `log2 n` choices. The factorization method here
is the exact Cartesian support factorization used in
`research-general-factor-contexts.py`. The restriction to loop-free recovery
matters: a self-parent gate may instead be empty or singleton, so its target
need not have an `M/2` projection. The supplied-representation theorem above
still allows self-loops. For `M=2`, pure coordinate equalities already give the
entropy-optimal d-query code.

Thus a general polynomial portfolio can recognize this canonical class, run
its certified count policy, and keep the cheaper actual code. This gives the
structured factor-two guarantee without requiring graph roles or test
priorities as input. It provides no unrestricted approximation guarantee.
The recognizer and physical executor are now implemented in
`research-general-graph-recognition.py`, documented in
`research-general-graph-recognition.md`, and exercised with permuted orders,
independently relabeled private palettes, and complemented question responses.

## 6. Finite audits and reproducibility

`research-general-dependency-graph.py` executes the actual original questions,
keeps equality work separate from enabled-palette work, and verifies the
result is a proper full identifying tree. Its 13 bounded examples include
DAGs, directed cycles, complete directed graphs, a self-parent loop, alphabet
sizes 2/4/8, and up to 512 hypotheses. It checks:

* 1,100 reached charged count-state values have integer raw work and at most n
  count states are retained in each case; the former uncharged DP is retained
  as a separate 1,100-state comparison;
* real paid-plus-palette work is at most `n V_root`; the old uncharged policy
  also has exactly its predicted paid work;
* 7,987 stronger simulation histories are full Cartesian posterior cells,
  their mean query-simulation work is at most two, and every simulated
  original answer is entailed by that stronger cell;
* all 1,552 simulated full hypothesis paths satisfy both the distinct-positive
  accounting (4) and the charged pathwise inequality (5), including roots and
  a self-loop;
* seven cases with at most 16 hypotheses also compare with exact unrestricted
  optimal codes and verify the factor-two inequality.

Run `.venv\\Scripts\\python.exe research-general-dependency-graph.py`. Exact
unrestricted optimization is used only by these seven bounded validation
cases; the proposed algorithm is the n-state count DP. The saved results are
`research-general-dependency-graph.results.json`.

The independent audit `research-general-graph-relaxation-audit.md` checks the
main proof and extends the simulation to a specified bounded union of full
parent-tuple gates. No article edit or unrestricted approximation claim
follows from this class theorem.

The original uncharged-activation argument gave factor three by adding its
palette overhead after optimizing equality work. The charged recurrence is
the authoritative algorithm here: it retains the same polynomial state space
and accounts for successful parent checks against saved activation charges,
improving that result to factor two.
