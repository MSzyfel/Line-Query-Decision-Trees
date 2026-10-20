# Information and restricted coding: causal actions and compact predictors

Auxiliary research note, 18 October 2026. No article files were edited. Model: explicit separating binary test matrix, uniform hypotheses, unit query costs, polynomial time in the explicit input.

## Outcome and separation from existing work

No unrestricted `o(log n/log log n)` approximation is proved here. This investigation supplies three concrete additions:

1. A polynomial-size relative-entropy relaxation that charges information needed to select queries and to stop correctly. It is valid, but an explicit fractional solution shows that even after adding shared-pair separation and no-repeat constraints it retains the full target-order gap on the affine-equality family.
2. A polynomial verifier for a supplied finite-state online predictor. Its certified mistake budget can supply the existing sequential-code lower bounds and activation-priced LP without computing Littlestone dimension. Finding useful compact predictors on arbitrary instances remains unresolved.
3. A compact algebraic certificate, developed with the root agent: represent hypotheses by nonzero finite-field columns and verify that every oriented positive test set is a represented-matroid flat. Gaussian elimination certifies a global bound on positive answers without enumerating span states. One linear budget per hypothesis then strengthens the causal relaxation and restores the missing affine-equality factor.

The sequential/Littlestone capacity, the rank-limited code recurrence, the affine-equality lower bound, and activation composition were **already proved in Sections 10–12 of `uniform-decision-tree-lower-bounds.md`**. They are used below as existing results, not relabeled as new. Likewise the general greedy approximation is inherited from the supplied `1906.11385v2.pdf`.

## 1. Why ordinary coding quantities do not settle the question

For a uniform source, unconstrained Shannon and Rényi entropies are all `log n`. They contain no information about which questions are available. Guesswork adds a completion-time profile, but that profile must respect actual adaptive questions. The existing sequential-rank construction does precisely this on affine equality tests; a static output-label entropy does not.

Relevant primary literature checked:

* [Bhaskar, Thicket Density](https://arxiv.org/abs/1702.03956v4): the sequential tree-growth theorem underlying the existing local rank note.
* [Manurangsi–Rubinstein, COLT 2017](https://proceedings.mlr.press/v65/manurangsi17a.html): hardness of approximating Littlestone dimension even from an explicit finite binary matrix, under randomized ETH.
* [Chase–Freitag–Reyzin, MFCS 2024](https://drops.dagstuhl.de/entities/document/10.4230/LIPIcs.MFCS.2024.42): compression and equivalence queries with random counterexamples. That query model provides counterexamples rather than the original unit-cost yes/no answers, so its query bounds cannot be substituted into UDT.
* [Chandrasekaran–Shah, Relative Entropy Optimization](https://people.lids.mit.edu/pari/REO.pdf): convex formulations with linear and relative-entropy constraints.

The new attempt was to impose a causal information budget on the *choice of a question*. This addresses a real omission of certificate-only relaxations: choosing a useful question may itself require knowing something about the target.

## 2. A polynomial causal-action relaxation — validity proved here

Let `X` be uniform on `H`, `|H|=n`, and let the original tests be indexed by `q in [m]`. Use times `t=1,...,T+1`, with `T=n-1`. At time `t`, an action `U_t` is either a query index or a correctly labeled terminal output `stop_h`. Terminal outputs are absorbing; after a path finishes, keep repeating its output action without charge.

Variables are conditional action marginals:

```
x_(h,q,t) = Pr[U_t=q | X=h],
y_(h,t)   = Pr[U_t=stop_h | X=h].
```

Require nonnegativity, `sum_q x_(h,q,t)+y_(h,t)=1`, nondecreasing `y_(h,t)`, and `y_(h,T+1)=1`. For `n>1` one may set `y_(h,1)=0`. Other terminal labels have conditional probability zero. Define `A_t` to be the answer to the selected query, or the fixed symbol zero after stopping.

Both of the following are explicit functions of these marginals:

```
I_t = I(X;U_t),
E_t = H(A_t | U_t).
```

Impose

```
I_t <= sum_{s<t} E_s                 for every t.                (C1)
```

Minimize mean query cost

```
D_rel = (1/n) sum_(h,q,t<=T) x_(h,q,t).                            (C2)
```

**Validity theorem.** Every proper deterministic tree, and every distribution over such trees, supplies a feasible point with objective equal to its mean depth. Consequently the relaxation optimum is a lower bound on `OPT`.

Let `R` be the policy's target-independent random seed. The action at time `t` is a function of `R` and the previous answers. Thus

```
I(X;U_t) <= I(X;R,A_<t)
         = sum_{s<t} H(A_s | R,A_<s)
         <= sum_{s<t} H(A_s | U_s).
```

Noiselessness gives the equality; conditioning reduces entropy for the last inequality. Correct final stopping gives `I_(T+1)=log_2 n`. Since `E_t <= Pr[query at t]`, the relaxation includes Shannon's lower bound `D_rel>=log_2 n`.

### Convexity and size

Put `p_(q,t)=(1/n)sum_h x_(h,q,t)` and `s_(q,a,t)=(1/n)sum_{h:q(h)=a}x_(h,q,t)`. Then

```
I_t = (1/n) sum_(h,q) x_(h,q,t) log_2[x_(h,q,t)/p_(q,t)]
      + (log_2 n/n) sum_h y_(h,t),

E_t = sum_q [p_(q,t) log_2 p_(q,t)
             - sum_a s_(q,a,t) log_2 s_(q,a,t)].
```

Use the continuous zero-mass conventions. Mutual information is convex in the conditional action channel under a fixed input prior, while conditional answer entropy is concave in the joint masses. Therefore `I_t-sum_(s<t)E_s` is convex. The formulation has `O(nmT)` action variables and admits a polynomial-size relative-entropy/exponential-cone representation. This is a finite convex formulation suitable for standard weak numerical optimization; no exact transcendental optimizer or numerical optimization implementation is claimed in this session.

### Two natural linear strengthenings

Suppressing repeated queries on each actual path gives

```
sum_t x_(h,q,t) <= 1.                                            (C3)
```

For each unordered pair `u,v`, add common-query masses

```
0 <= w_(uv,q,t) <= min(x_(u,q,t),x_(v,q,t)),
sum_{q:q(u)!=q(v),t} w_(uv,q,t) >= 1.                             (C4)
```

An actual tree charges its first common separating query. Mixtures of trees charge that random first separation. Thus these are valid. Introducing `w` makes (C4) linear and uses `O(n^2mT)` variables. These are endpoint-shared pair constraints; they are not claimed to be the stronger co-location flow hierarchy of the older note.

## 3. Explicit full-order gap even with (C1)–(C4)

Use the affine-equality family already analyzed in the local lower-bounds note. Let `H=F_Q^d`, `n=Q^d`; take one copy of every distinct affine-hyperplane membership test. Put

```
J = (n-1)/(Q-1),       m=QJ.
```

Every test is positive on `n/Q` hypotheses, each hypothesis lies in exactly `J` tests, and each distinct pair is separated by exactly `2n/Q` tests. The existing result is `OPT=Theta(Qd)`. For `d=floor(Q/ln Q)`, this is the familiar full-order obstruction.

Define two action channels, with no stopping during their query phases.

**Uniform channel:** `x_(h,q)=1/m` for every `h,q`. It has

```
I_uniform = 0,       E_uniform = h_2(1/Q).
```

**Biased channel:** given `h`, choose uniformly from hyperplanes containing `h` with total probability one half, and uniformly from hyperplanes missing `h` with total probability one half:

```
x_(h,q) = 1/(2J)                 if q(h)=1,
          1/[2(Q-1)J]            if q(h)=0.
```

Its unconditional query marginal remains uniform. Conditional on the query, its positive answer has probability one half. Direct calculation gives

```
I_biased = log_2 Q - 1 - (1/2)log_2(Q-1),
E_biased = 1.                                                     (C5)
```

Use the uniform channel for `Q` steps, then the biased channel for `ceil(log_2 n)` steps, then stop correctly. Fill the rest of the `n-1`-step horizon by repeated terminal actions. For the asymptotic family the query phases fit inside the horizon.

Every causal constraint holds. The uniform phase asks for no target-dependent selection information. Before the biased phase,

```
Q h_2(1/Q) >= log_2 Q >= I_biased.
```

Each biased step adds one to the relaxed entropy budget. At final stopping this budget is at least `log_2 n`, paying for the terminal output action.

All pair demands already hold in the uniform phase: give `w=1/m` to each separated pair/test/time there. A pair receives

```
Q (2n/Q)/m = 2n/(QJ)
            = 2n(Q-1)/[Q(n-1)] >= 1.                             (C6)
```

No-repeat marginals also hold for sufficiently large family members. The largest accumulated mass on any `(h,q)` is

```
Q/m + ceil(log_2 n)/(2J)
= [1+ceil(log_2 n)/2]/J <= 1,                                     (C7)
```

since `J` grows exponentially in `d` while the numerator is `O(d log Q)`.

Thus (C1)–(C4) have a feasible solution of cost

```
D_rel <= Q + ceil(log_2 n),
OPT/D_rel = Omega(d)
          = Omega(log n/log log n)                               (C8)
```

on `d=floor(Q/ln Q)`. The construction is explicit in the original polynomial-size matrix; it does not use an oracle or a superpolynomial enumeration.

### What the relaxation falsely permits

The actual new information at a step is `H(A_t|R,A_<t)`, not `H(A_t|U_t)`. Their difference is an answer/history redundancy. The latter marginal entropy can remain one even when the information that made the selected question attractive also makes its answer redundant with the actual history. Charging the information required to select an action does not identify that redundancy.

The feasible point above is therefore more than a reminder that entropy ignores query identities: it retains query identities, charges their mutual information, forbids repeated-query marginals, and pays every pair through common tests. Those conditions still permit a sequence of noncausal posterior channels. A useful replacement must preserve enough joint history to prevent this information reuse.

## 4. Benchmark checks beyond the affine counterexample

The same formulation does capture two basic scales; this helps isolate the missing dimension rather than rejecting every information quantity indiscriminately.

**Singleton search.** In a family of singleton tests, summing all pair demands (C4) gives at least `n(n-1)/2` total common-pair charge. Assign each separated pair to its endpoint outside the singleton. At every endpoint/query, at most one such pair is assigned. Hence total conditional query mass is at least `n(n-1)/2`, and `D_rel >= (n-1)/2`. Uniform singleton search has optimum `(n+1)/2-1/n`, so the relaxation has the right linear scale, within an additive constant.

**Bounded caps.** If every test's oriented positive side has at most `b` hypotheses, assign separated pairs to their negative endpoints. At most `b` pairs use any endpoint/query. This gives `D_rel >= (n-1)/(2b)`. For fixed `b`, even a proper arbitrary tree has cost at most `n-1`, so this is a constant-factor scale check. It includes arbitrary pair-cap matching systems; it does not claim to recover their exact matching invoice.

**Gated grid.** In the existing family `[C] x {0,1}^b`, column caps have size `r=2^b`, gated bits have size `r/2`, and decoy positive supports have size at most `2r`. Thus (C4) gives `D_rel >= (Cr-1)/(4r)`, while final-stop entropy gives `D_rel >= b+log_2 C`. Column search followed by the complete active row code costs at most `C+b`. These two lower bounds already match that benchmark within a constant. The affine counterexample is stronger because it exposes a missing factor despite these benchmark successes.

## 5. A positive compact certificate: finite-state predictors

This section makes a limited algorithmic refinement to the **existing** sequential-capacity method. The new part is a polynomial, checkable certificate format; the coding theorem it invokes is already in the local note and in the primary sequential-growth literature.

A supplied deterministic predictor has `S` states, an initial state, a prediction `p(s,q) in {0,1}`, and transition `delta(s,q,a)` after seeing answer `a`. The predictor must work for any realizable sequence of original queries, including repeated queries. Its transition table has polynomial size when `S` is polynomial.

**Certificate-verification theorem.** In `O(n S^2 m)` time one can either compute its exact worst-case number `d` of mistakes, over all hypotheses and all realizable finite query sequences, or detect that no finite mistake bound exists.

For each possible target `h`, form a directed state graph with an edge

```
s -> delta(s,q,q(h)),
weight = indicator[p(s,q) != q(h)]
```

for every state and query. Restrict attention to states reachable from the initial state. A reachable directed cycle with a positive-weight edge allows arbitrarily many mistakes by repetition. If no such cycle exists, contracting strongly connected components gives a DAG, whose longest weighted path is the exact mistake budget for this `h`. Maximizing over `h` gives `d`. SCC/DAG processing gives `O(nSm)` after graph construction; ordinary longest-path Bellman–Ford with positive-cycle detection gives the simpler stated `O(nS^2m)` bound used by the checker. All weights are zero or one, so bit complexity is polynomial.

This is equivalent to checking state/target potentials `r_(h,s)>=0` only on states reachable from the initial state under target `h`, with

```
r_(h,s) >= indicator[p(s,q)!=q(h)] + r_(h,delta(s,q,q(h))).        (P1)
```

Transitions from such a reachable state remain reachable. Unreachable states impose no inequalities: a positive-mistake cycle there cannot invalidate a predictor that never enters it for that target. The minimum initial potential is the longest-mistake count. The constraint table is polynomial and is not an implicit all-subsets oracle.

### From a verified predictor to a coding lower bound

Given a verified mistake bound `d`, label any actual tree edge by whether the predictor errs there. Its prediction is determined by the preceding query/answer history. Therefore a mistake/no-mistake string reconstructs the original response string, and every path has at most `d` mistakes. This proves the same sequential capacity bound used in the earlier note:

```
#completed leaves by depth t <= sum_{j<=min(d,t)} binomial(t,j).
```

In particular one may compute the old rank-limited coding lower bound `M_d(n)` in `O(dn^2)` time. This may be weaker than using exact Littlestone dimension, because the supplied predictor need not be optimal; it is nevertheless valid and polynomial to verify. If `d` exceeds `floor(log_2 n)`, use the known halving-predictor budget instead.

Likewise, for a polynomial list of resources `A`, a supplied compact predictor for each restriction yields a polynomially verified bound `b_A=M_(d_A)(|A|)`. These numbers can be inserted into the existing activation-priced shared-budget LP (Section 12 of `uniform-decision-tree-lower-bounds.md`). Its original endpoint capacities then ensure that coding and activation charges are not added repeatedly. This makes that LP genuinely polynomial for this certificate format; it does not prove that useful compact predictors exist or can be found on arbitrary resources.

The supplied greedy theorem consequently gives an `O(d)` approximation on classes admitting a certified mistake bound `d`, in addition to its unrestricted bound. This structural consequence is inherited from the coding bound and greedy theorem. It is not a new unrestricted approximation ratio.

### An executable example and a size limitation

For arbitrary caps of size at most two, use an unknown state that predicts zero until the first positive answer. That answer leaves at most two candidates. Thereafter predict their majority answer, updating the candidate pair after every query. After at most one further error the target is known. States consist of the unknown state, singleton states, and supplied cap states, so `S<=1+n+m` and `d<=2`. The checker validates these transition tables directly, without invoking maximum matching or a sequential-rank oracle. This is a certificate illustration; the old matching algorithm already solves the uniform cap-two optimization exactly.

The affine positive-equation predictor also has at most `d` mistakes and a compact linear-algebra description, as already observed in the old note. Its number of possible span states can be superpolynomial in the explicit hypothesis count. The finite-table verifier does **not** make that full state enumeration polynomial. Its rank bound instead has a separate algebraic proof. Confusing compact arithmetic representation with polynomially many finite states would invalidate the runtime claim.

## 6. A compact algebraic history certificate — proved here

Finite-state tables are not the only way to verify a global history restriction. Supply columns `v_h` over a finite field, with actual matrix rank `r`, and choose an orientation for every binary test. Require every column to be nonzero. For every oriented positive support `C`, verify

```
v_h not in span{v_g:g in C}             for every h outside C.    (P2)
```

Thus `C` is a flat of the represented matroid on the hypothesis columns. Form a basis of its columns and test each outside column for span membership by Gaussian elimination. This takes polynomial time in `n,m`, the supplied column dimension, and the field encoding. It does not enumerate the potentially enormous family of reachable spans.

**Rank-budget theorem.** Every proper identifying tree has at most `r-1` positive answers on every root-to-leaf path.

Let `S` be the **actual current candidate set**, after all previous positive and negative answers, and suppose test `C` properly splits it. If the positive successor had the same rank as `S`, then for any `h in S\C`,

```
v_h in span(S) = span(S intersect C) subseteq span(C),
```

contradicting (P2). Hence a positive answer strictly reduces current span rank. A negative answer cannot increase it. The initial rank is `r`, and the terminal nonzero singleton has rank one, proving the budget. The argument does not replace `S` by the affine solution space of positive equations; arbitrary earlier negative restrictions are included.

If zero columns are present, the analogous bound is `r`, since a loop target can end at rank zero. Alternatively homogenize every column to `(1,v_h)`. This preserves (P2), makes all columns nonzero, and increases rank by at most one. The nonloop convention must not be omitted from the `r-1` statement.

### A linear constraint that repairs the causal affine counterexample

Put `d=r-1`. Every actual policy now satisfies, separately for each hypothesis,

```
sum_{q,t:q(h)=1} x_(h,q,t) <= d.                                 (P3)
```

These are polynomially many **global** positive-answer budgets. They are not restarted inside subtrees. Their validity follows from the rank proof, while (C1) keeps track of the entropy required for correct stopping.

Let `D` be a feasible relaxation point's query cost and `B` its average total positive-answer mass. Then `B<=d`. Jensen's inequality over all query/time masses gives

```
log_2 n <= sum_t E_t <= D h_2(B/D)
                         <= B log_2(eD/B).                       (P4)
```

If `d<=D`, the last expression is at most `d log_2(eD/d)`, since `z log_2(eD/z)` increases for `0<z<=D`. In particular, `d<=log_2 n` suffices, because (C1) already gives `D>=log_2 n`. Under this explicit condition,

```
D >= (d/e) n^{1/d}.                                               (P5)
```

When `d>log_2 n`, retain the entropy baseline or the previously proved rank-limited coding bound; substituting `d` into (P4) without `d<=D` would be invalid. The condition is satisfied in the affine family of interest.

For affine hypotheses `h in F_Q^d`, use homogenized columns `(1,h)`. Their rank is `d+1`. Every positive hyperplane test is a flat: its columns lie in the kernel of the functional `(-b,a)`, while any outside hypothesis does not. Thus (P3) has budget `d`, and (P5) gives `D>=Qd/e`. This captures the same scale as the existing sequential-capacity bound using a polynomially verified representation and a simple linear addition to the relative-entropy program.

The fractional channel from Section 3 has positive mass `1+ceil(log_2 n)/2`; on `d=floor(Q/ln Q)` this exceeds `d` for large `Q`, so it violates (P3). The algebraic constraint therefore repairs that concrete full-order gap. It is not claimed to make the strengthened relaxation roundable on arbitrary instances.

For a polynomial list of restricted resources, separately verified flat representations also give the old activation LP polynomially computed coding bounds, using its existing shared-budget composition. This is an algebraic certificate format for the old composition theorem, not a new proof of that theorem.

### Link to scalar linear index coding

The certificate has a direct coding interpretation. Introduce one independent field message `z_h` per hypothesis and broadcast the vector

```
Y = sum_h v_h z_h.
```

For every test support `C` and every `h outside C`, create a receiver wanting `z_h`, knowing all messages outside `C union {h}`. After subtracting the known messages it sees

```
v_h z_h + sum_{g in C} v_g z_g.
```

It can recover its desired message exactly if and only if `v_h` is outside `span(C)`. If outside, a linear functional annihilating `span(C)` and taking value one on `v_h` decodes it. If inside, changing `z_h` and compensating the interfering messages leaves the broadcast unchanged, preventing any decoder from recovering it. Adding a receiver with empty interference for each message enforces nonzero columns. Thus all these receivers' linear decodability constraints are exactly (P2) plus the nonloop condition.

The established relationship between index coding and matroid representation provides useful context; see [El Rouayheb–Sprintson–Georghiades](https://arxiv.org/abs/0810.0068). The span equivalence above is proved directly. It supplies no polynomial method to synthesize a low-rank representation. The identity columns always give a certificate of rank `n`; finding a sufficiently small rank is the substantive task.

As an executable check, columns `(1,t,t^2)` with distinct field elements have every set of at most two points as a flat, because every three columns are independent. They certify a two-positive-answer budget for arbitrary singleton/pair cap systems. This holds without a geometric plane or singleton availability, but the old matching theorem already gives stronger exact optimization in the uniform pair subclass.

## 7. Experiments and remaining target

`research-general-information-next.py` uses only the Python standard library. It passed:

* the causal inequalities on 126 independently computed exact optimal-policy projections;
* 53 finite-state singleton/pair-cap predictor certificates, each with at most two mistakes;
* rejection of a deliberately false one-state predictor with a positive-mistake cycle;
* 42 represented-flat certificates on singleton/pair systems using moment-curve columns, with exhaustive proper-subset rank-drop and maximum-positive-path checks;
* rejection of a false flat certificate using parallel columns;
* explicit affine fractional channels for `(Q,d)=(2,3),(2,4),(3,2),(3,3),(5,2),(5,3)`, checking every pair demand, the no-repeat bound, each causal information constraint, and final correct stopping;
* homogenized affine flat verification on those same matrices; the new positive budget rejects the fake channels in every checked `Q=3,5` case. The `Q=2` instances have no analogous missing `Q` factor and need not violate the new budget.

The affine checks evaluate explicit feasible points. They do not numerically optimize the convex formulation or infer an asymptotic gap from small numerical ratios; (C5)–(C8) prove that gap.

This direction isolates the next genuine obligation. A compact coding certificate must represent which information is still fresh after an activated query is selected. Marginal query-selection information cannot do that, even when combined with all endpoint pair demands. Verified finite-state predictors and flat representations can certify global history restrictions without an expensive dimension oracle; the latter repairs the explicit affine failure in polynomial verification time. Constructing a useful polynomial family of these certificates, and using it to generate actual conditional codes with a nonduplicating approximation proof, remains open. No polynomial generator, rounding theorem, or unrestricted improvement has been established.
