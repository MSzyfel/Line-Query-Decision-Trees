# Linear cover equations recover hidden selector tests

Auxiliary research note, 19 October 2026. The article is unchanged. This is
a new polynomial query-family selector and a structured coverage theorem.
It does not establish an unrestricted approximation ratio.

The previous query-family portfolio can be trapped by one balanced bridge:
the bridge merges all selector partitions into a nonclique disjointness
component while surviving the independence filter. Exact linear equations
remove that bridge and the aliased bit tests without being given their
roles. The useful connection with LP is **support of the affine exact-cover
system**, rather than rounding an arbitrary fractional cover.

## 1. A polynomial filter that preserves every actual partition

Fix a cardinality B. List the distinct original response cells of size B,
including both response orientations, and let A be their n-by-s incidence
matrix. Consider

    A x = 1.                                               (1)

The usual fractional exact-cover polytope also imposes x>=0. We initially
allow arbitrary real coefficients. If (1) is inconsistent, these cells
contain no partition of H. Otherwise Gaussian elimination gives one
particular solution x0 and a basis v1,...,vt for ker A. Retain column j iff

    x0_j != 0 or some vl_j != 0.                            (2)

This criterion is exact: it says that x_j is nonzero in at least one real
solution. In particular, every cell occurring in ANY actual partition of H
survives. Its partition incidence vector is a solution of (1), so it cannot
use a column discarded by (2).

This does not solve exact cover. Retained cells may belong only to signed
solutions, or to fractional covers, and may still interfere with one another.
After filtering, we explicitly check entire disjointness components for
pairwise disjointness and union H. Only such checked components are called
partitions. We also retain the original-query family corresponding to ALL
surviving cells of each B, whether or not components succeed. This family is
only a source for response factorization; it need not itself be a partition.

For each retained partition, each union at a fixed B, and the union over B,
run the existing response-factor context planner. Keep all previous initial
families. As before, apply exactly one independence-refinement level to this
frozen initial list, then pool the actual generated states and use actual
incumbent fallback in the depth-prize DP. No new family recursively starts
another refinement level.

There are at most n-1 cardinalities, at most 2m columns per system, and
rational Gaussian elimination takes polynomial time and polynomial bit
complexity on these 0/1 matrices. The particular solution and kernel basis
can be verified directly. The subsequent factorization and context count
are polynomial by the previous counting lemma. Thus this is a fixed-exponent
polynomial algorithm in n and m, including reconstruction of original-test
trees. It also contains the entire previous portfolio and cannot give a
worse result. No input labels or guessed selector roles are used.

## 2. Exact recovery on the bridge camouflage family

Use the family in `research-general-bridge-aliases.md`. There are k>=2 uniform
M-symbol selectors C, L independent R-symbol bodies Z, and R=M/2, with
M=2^b>=4. All pure equalities are present. The private questions are

    q_(j,g,u)(C,Z) = 1_[f_j(C)>>1=g] bit_u(Z_j xor h(C)),

where h(C)=C0>>1 and each nonzero-coefficient linear form f_j maps the
selector cube onto the field of size M. A full group has 2 M^(k-1) contexts.
Add one bridge

    q_*(C,Z) = 1_A(C) [bit_0(Z_0) xor t(C)].

The set A has size 2 M^(k-1), avoids zero on every selector axis, and t is
balanced on A. Such an A is given explicitly by the half-alphabet rectangle
in the bridge note when M>=2^(k+1). Every gate and bridge has root minority
B=n/M. Body equalities have size 2B; selector equalities have size B.

**Theorem.** At cardinality B, affine-support pruning retains exactly the
pure selector cells. Consequently its checked disjointness components recover
all k selector partitions, without their roles or coordinate values supplied.

Let alpha_(i,a), beta_(j,g,u), and delta be the real cover coefficients of
selector cells, ordinary gates, and the bridge. Equation (1), at each (C,Z),
is

    sum_i alpha_(i,C_i)
      + sum_(j,u) beta_(j,f_j(C)>>1,u) bit_u(Z_j xor h(C))
      + delta 1_A(C) [bit_0(Z_0) xor t(C)] = 1.              (3)

Fix any j,g. Its activation group contains a context outside A: set one
selector to zero and solve for another selector using its nonzero coefficient
in f_j. This uses k>=2. At such a context the bridge vanishes. Varying one
bit of Z_j, holding all other bits and bodies fixed, changes exactly the
corresponding ordinary gate term. Hence every beta_(j,g,u)=0, even though
the coefficients are allowed to have either sign.

Now choose any C in A and vary bit_0(Z_0). Equation (3) forces delta=0.
The remaining equation is sum_i alpha_(i,C_i)=1 for every selector tuple.
Varying just C_i forces alpha_(i,a)=s_i independent of a, with sum_i s_i=1.
Conversely all these choices are real solutions. Each selector cell has a
nonzero coefficient in the solution s_i=1, s_other=0. Thus the affine support
is exactly the kM selector cells, with dimension k-1. Different selector
axes' cells intersect; within each axis they form one disjoint full partition.
This proves the recovery statement.

The proof uses the explicit full product only to analyze recovery. The
algorithm performs ordinary incidence-matrix elimination on the response
matrix. It does not perform this symbolic decomposition itself.

## 3. A class-specific constant comparison

The union of the recovered selector families factors into k independent
M-value axes. The context planner contains the program that decodes them by
equalities and then completes each body using its now-enabled bit palette.
All questions are original tests, including the physical aliased code rows.
Its mean cost is at most

    U = k e(M) + L(b-1),
    e(M)=(M+1)/2-1/M.                                    (4)

This comparison is valid even if the planner finds a cheaper code, or the
incumbent itself is cheaper at a small parameter value. Binary information
gives OPT>=L(b-1). For fixed k and L=floor(cM/log2 M), c>0, (4) gives

    ALG/OPT <= 1+k/(2c)+o(1).                             (5)

There is also selector entropy in the lower bound, which is unnecessary for
this displayed comparison. The same class has the full-order balance-greedy
gap: every nonbody test remains independent of the full body vector, while
the body equalities are initially more balanced. Hence greedy decodes the
bodies by slow equality search. For the growing L above, this costs
Omega(M^2/log M) per hypothesis, whereas U=O(M) and
log n/loglog n=Theta(M/log M). The new selector therefore repairs a scalable
barrier, rather than only one finite greedy decision.

## 4. What is still missing

The criterion preserves every true partition, but it does not guarantee that
whole components isolate one. There is a concrete next interference pattern:
two cells can split a union of two selector values into complementary body-bit
parts. Their sum equals the sum of those selector cells, so both new columns
occur in actual covers and MUST survive affine pruning. Adding such pairs
across axes can merge disjointness components again. This observation limits
the component argument; it has not been proved to defeat the full extended
portfolio, which also retains all supported columns as a factorization seed.

The completed follow-up in `research-general-cover-geometry.md` proves a
positive result for these particular paired bridges. Their whole supported
family identifies a quotient containing the selector tuple and at most one
conditional body bit. The listed retained rows identify that quotient in
at most D=kM+2k actual questions. The linear-selector portfolio now enables
the optional retained-row decoder fallback, so it inherits this height
bound even when the quotient is prime and has unequal fiber sizes. Once
known, fresh greedy finishes all bodies in at most L(b-1) further questions.
For the same fixed-k growing family its class-specific ratio is therefore
at most 1+k/c+o(1). This is a repair of the paired example, not a universal
partition-discovery theorem.

More generally the current filter does not supply a comparison between its
generated partial policies and arbitrary truncated optimal policies. It is
neither a new OPT lower bound nor a polynomial exact-cover algorithm.
Approximate completion pricing remains the unresolved general step.

## 5. Executable checks

`research-general-linear-selectors.py` implements (1)-(2), checked component
recovery, the extended query-family portfolio, and original-test execution.
Its saved output is `research-general-linear-selectors-results.json`.

The bounded validation includes 35 small exact affine systems. Each consistent
case independently checks its particular solution and every nullspace
generator against the original equations. Exhaustive subset enumeration
confirms preservation of 17 actual partitions; that enumeration is validation
only and is not used by the algorithm.

Three bridge instances at n=64,256,1024 recover exactly the pure selector
families and execute their planned code on every original hypothesis. The
selector candidates have raw costs 400,2528,12270, compared with greedy
404,2546,12270 respectively. In particular the largest finite example does
not improve the incumbent. The complete old and extended portfolios were
also executed at n=64: 404 versus 400. No unrestricted optimum oracle is
used, and the asymptotic statement (5) follows from the proof, not from these
small cost comparisons.
