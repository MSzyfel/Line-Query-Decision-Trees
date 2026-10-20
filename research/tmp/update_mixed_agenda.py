from pathlib import Path

p = Path('planar-line-query-research-agenda.md')
s = p.read_text(encoding='utf-8')
s = s.replace('below 5.197569 for arbitrary-prior expected depth', 'below 5.182976 for arbitrary-prior expected depth')
s = s.replace('The expected factor improves 5.272565 by changing the initial coverage budget and merging selected first geometric phases, while retaining rational endpoint-information credits.', 'Modifying both initial coverage budgets improves the previous 5.197569 factor. A smaller global slot cap reduces the maximum-depth scheduler\'s polynomial degree. A new PTAS covers uniform fixed-size convex-position caps with a distinguished all-miss hypothesis, without singleton supply.')
s = s.replace('Factor below `5.197569` for arbitrary positive priors', 'Factor below `5.182976` for arbitrary positive priors')
s = s.replace('General polynomial E `<5.197569` after initial-phase changes', 'General polynomial E `<5.182976` after two initial-budget changes')
s = s.replace('They are now superseded by 4.464966 and 5.197569 above.', 'They are now superseded by 4.464966 and 5.182976 above.')
s = s.replace('The latest broad polynomial factors are **4.464966** and **5.197569**', 'The latest broad polynomial factors are **4.464966** and **5.182976**')
s = s.replace('Appendix A now supplies algorithm2e pseudocode for all optimization constructions, and repeated entropy inductions use one stage-to-tree lemma.', 'Pseudocodes are now local to their analyses, and repeated entropy inductions use one stage-to-tree lemma.')
row = '| Fixed-size caps, all-miss hypothesis | Exact polynomial maximum-depth algorithm | Derived suffix-enumeration proof; integrated in TeX |'
s = s.replace(row, row + '\n| Uniform fixed-size convex-position caps, all-miss hypothesis | PTAS, no singleton supply required | Exact block-interleaving DP and independent adaptive-tree audit; integrated in TeX |')

old_heading = '### Modified initial batches: general polynomial expected depth below 5.197569'
new_intro = r'''### Two initial budgets: general polynomial expected depth below 5.182976

The [new two-budget section](sections/06g-two-phase-improvement.tex) tries `q,r,k2,k3,...` with `q=1,...,6` and `r=k1-1,k1,k1+1`, when `q<r<k2`, as well as `q,k2,k3,...`. The rational shift partition includes all initial `k/beta` and `k/beta²` breakpoints through `ceil(beta³)`, including when the minimum cover is small. Exact coverage, rational block modes and full-pattern recursion remain unchanged.

With `beta=3512863/10^6` and `delta=393931/2500000`, a fixed 43-row rational certificate gives `A=3.591810178840039...`, `B=4.374727111311243...`, and factor **below 5.182976**. It retains signed first-hit corrections and complete zero-route changes; first-batch saving is counted once. The complete table is [in the numerical appendix](sections/12-two-phase-certificate.tex), and [exact checks](expected-two-phase-check.py) verify the certificate, 9,900 phase identities and 1,650 actual-batch cases. An [independent direct phase audit](development-two-phase-audit.md) reproduces the ratio without the older discount formula.

All 22 algorithm2e recipes now sit beside their analyses. Four flow diagrams explain recursion, maximum-depth scheduling, expected-depth schedule construction and execution, and quasipolynomial lookahead. Shared floor, capped-rank, entropy and lookahead lemmas shorten repeated reasoning while preserving the guarantees and edge cases.

### Uniform shallow-cap PTAS and the revised hardness target

The [new PTAS](sections/06h-uniform-bounded-cap-ptas.tex) applies to uniform hypotheses in convex position, with an actual distinguished all-miss hypothesis and cap size at most fixed `b`. Mark `b` points in each cyclic piece of length `ell>=8b²/epsilon`; clear them using supplied caps, with legal local positive-exit codes. Every residual cap acts within one block. An exact count-vector Bellman DP optimizes all query interleavings; uniform weights permit grouping identical local mask families. At most `b*ell` interval masks give at most `2^((b+1)*ell)` local states. Realizing-query maps remain attached to physical blocks.

The prefix adds at most `2r(N+1)`, whereas every full tree costs at least `N(N+1)/(2b)` in raw uniform depth. With `r<=2bN/ell`, the ratio is at most `1+8b²/ell`. This is a PTAS whose exponent depends on `b,epsilon`. [Development checks](constant-gap-session.py) passed 1,080 decompositions and an [independent audit](uniform-cap-ptas-audit.md) passed 3,033 adaptive-oracle comparisons, including families without singleton tests.

The GOOD/BAD prefix examples remain valid, but bounded-size interval caps on one convex layer cannot supply constant-factor NP-hardness under uniform priors unless P=NP. Future reductions must escape that class, for example through unbounded caps, several convex layers, or a different witness architecture, and must prove robust global assignment extraction for arbitrary adaptive trees.

### Earlier single-initial-budget factor below 5.197569'''
assert old_heading in s
s = s.replace(old_heading, new_intro)

start = s.index('Fix `q=ceil(log2 original_n)` and `L=2q+1`.')
end = s.index('An optional stronger variant', start)
s = s[:start] + r'''Fix `q=ceil(log2 original_n)`, `R=floor(gamma*q/(gamma-1))` and `L=R+1`. Every recursive stage builds its hybrid pattern children once, then chooses between the priority schedule and the capped exact schedule using those actual child heights. The two simultaneous invariants are

\[
C_W(S)\le3D+\lfloor\gamma\log_2|S|\rfloor,
\qquad D\le R\Longrightarrow
C_W(S)\le2D+\lfloor\gamma\log_2|S|\rfloor.
\]

The original-instance threshold survives restriction to every child. If the root optimum is small, the stronger invariant and `D>=log2 n` give `2+gamma=4.46496526`. If it exceeds `R`, integrality gives `D>gamma*q/(gamma-1)`, so the universal bound also gives a factor below `2+gamma`. The algorithm never needs the optimum as input. The zero route has a separate `floor(H/2)` total-block cap, and the terminal nonzero singleton append fits `D+1` slots.

''' + s[end:]
start = s.index('The rank cap can also reduce the polynomial degree.')
end = s.index('[Proof and extensions]', start)
s = s[:start] + '''With `K=gamma/(gamma-1)<1.682611`, the smaller cap gives slot contributions `3^L=O(n^(K log2 3))` and `2^L=O(n^K)`, with exponents below **2.666874** and **1.682611**. These are the mask contributions, with other polynomial factors still present. The cap is a floor of a fixed rational times `q`, so its implementation is exact. [Cap certificate](simplification-worst-cap-check.py) checks the exponents and 10,000 integer boundaries.

''' + s[end:]
s = s.replace('Uniform E strong NP-completeness via cloud transfer; prefix obstruction with asymptotic E ratio `11/10` | Couple local choices to one global gap-CSP assignment', 'Uniform E strong NP-completeness; uniform bounded-cap convex-position PTAS | Escape bounded cyclic caps and prove robust global choice coupling')
s = s.replace('Its source hardness is unproved here. Uniform cap size two is matching like, so size three is the first useful case to investigate. A PTAS for the source would also be valuable.', 'Its source hardness is unproved here. The new PTAS rules out this identification-hardness route for uniform convex-position fixed-size caps with an actual all-miss hypothesis. A source reduction must escape at least one of these conditions; merely increasing a fixed cap size is insufficient.')
s = s.replace('Bounded-cap height and the full-singleton pair-path weighted expected subclass have stronger algorithmic obstructions.', 'Bounded-cap height, uniform convex-position bounded-cap expected depth, and the full-singleton pair-path weighted expected subclass have stronger algorithmic obstructions.')
p.write_text(s, encoding='utf-8', newline='\n')
print('Updated current results, local pseudocode layout, smaller cap, PTAS and hardness targets.')
