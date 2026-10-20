from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def edit(name, start, end, replacement):
    path = ROOT / 'sections' / name
    text = path.read_text(encoding='utf-8')
    first = text.index(start)
    last = text.index(end, first)
    path.write_text(text[:first] + replacement + text[last:], encoding='utf-8')

edit('04-maximum-depth.tex',
     'Stop at a singleton. At a count-balanced state,',
     'For a passing trial,',
     r'''Algorithms~\ref{alg:priority-trial} and~\ref{alg:worst-tree} give the
explicit construction. At a balanced state query a balanced line and
recurse. At a flat state build every pattern child \emph{before}
scheduling; the trial uses its actual height, not its optimum. For an
oriented initial pair $(v,w)$, the first-positive classes satisfy the
direct one-query and two-query height checks. For classes negative on
both, put
\[
 u_A=c_{\mathrm W}(T_{\mathrm W}(A))+e_A^{(4)},\qquad
 B_A=H-u_A,\qquad d_A=\lfloor(B_A+2)/3\rfloor.
\]
Reject if $B_A<4$, then use the priority weights of
Lemma~\ref{lem:deadline-cover} and accept only if each actual first hit
satisfies $g_A+u_A\le H$. Trial heights range from one through
$\lfloor\kappa(s-1)\rfloor$.

After a positive answer, Algorithm~\ref{alg:endpoint-code} learns the
full pattern and the stored child identifies its hypothesis. The
second-query exit has a cached negative neighbor and uses only one
endpoint code. Stop discovery as soon as all nonzero patterns are
covered; its all-negative route identifies $A_0$ when present and is
omitted otherwise. Low-dimensional hulls use their extreme tests
directly. Every nonsingleton pattern child is smaller, so the recursion
is well founded.

''')

edit('04-maximum-depth.tex',
     '\\begin{proof}\nInduct on $s=|S|$, with the singleton bound equal to zero.',
     '\\end{proof}\n\nThe bound controls',
     r'''\begin{proof}
Induct on $s=|S|$, with a zero-cost singleton, and write
$D=\OPT_{\mathrm W}(S)$ and $H^*=3D+\lfloor\gamma\log_2s\rfloor$.
For every real $x\ge y$,
$\lfloor x\rfloor-\lfloor y\rfloor\ge\lfloor x-y\rfloor$.
A balanced child has size $a\le(1-\delta)s$ and optimum at most $D$,
so its count-potential drop is at least
$\lfloor\gamma\log_2(1/(1-\delta))\rfloor\ge1$.
This pays for its root query.

In a flat state put $L_A=\log_2(s/|A|)$ and
$\ell=\log_2(1/\delta)$. Since $|A|<\delta s$, $L_A>\ell$.
The conditions $\gamma\ge1$ and $\gamma\ell>5$ give the floor credit
\begin{equation}\label{eq:worst-floor-credit}
 \lfloor\gamma L_A\rfloor\ge5+\lfloor L_A-\ell\rfloor.
\end{equation}
Indeed, $\gamma L_A=\gamma\ell+\gamma(L_A-\ell)
>5+(L_A-\ell)$.

Choose an enumerated initial pair containing the first optimal-witness
query's supports; pad a singleton support with an adjacent real
neighbor. This only adds coverage. The inductive bound and
\eqref{eq:worst-floor-credit} leave at least one query after the
general endpoint allowance, and at least three after the singly pinned
allowance. Thus the first and second positive exits pass their direct
height checks, including classes hit by the padding.

For a class $A$ negative on both first supports, its comparison index
has $t_A\ge2$. Lemma~\ref{lem:height-prefix} and induction give
\[
\begin{aligned}
 B_A=H^*-u_A
 &\ge3(t_A-1)+\lfloor\gamma L_A\rfloor
                    -\lfloor L_A-\ell\rfloor-4\\
 &\ge3t_A-2\ge4.
\end{aligned}
\]
Hence $d_A=\lfloor(B_A+2)/3\rfloor\ge t_A$. The padded first block,
the original supporting blocks, and the terminal nonzero singleton
block when needed satisfy Lemma~\ref{lem:deadline-cover}. Its single
priority ordering therefore obeys
\[
 g_A\le3d_A-2
 =3\lfloor(B_A+2)/3\rfloor-2\le B_A.
\]
The last inequality follows by writing $B_A+2=3d_A+r$ with
$r\in\{0,1,2\}$. All actual-height checks pass. Truncating at the
last positive first hit also puts the zero singleton within $H^*$.
A one-dimensional hull needs at most two extreme tests; its count
potential drop pays for these directly.

Thus the least passing trial has height at most $H^*$. Since
$\log_2s\le D\le s-1$, this integer trial lies in the prescribed
range and $H^*\le(3+\gamma)D$. No optimum is queried by the algorithm.
''')

edit('06-expected-depth.tex',
     '\\begin{proof}\nUse the endpoint procedure of Section~\\ref{sec:endpoint-geometry}.',
     '\\end{proof}\n\n\\subsection{The recursive algorithm',
     r'''\begin{proof}
Discovery depends only on the full hull pattern. An inferred singleton
therefore has a unique pattern; on other positive exits the endpoints
identify it. The completed negative cover identifies the zero singleton.
Hence the output partition is exactly $\Pi$.

Use Algorithm~\ref{alg:endpoint-code} with the optimal expected-depth
alphabetic codes of Algorithm~\ref{alg:alphabetic-code}. An unpinned exit
uses two searches, a singly pinned exit one, and a doubly pinned exit
none. Their two-query code overheads sum to
$4b-2b_{\mathrm{pin}}-2b_{\mathrm{both}}$; the doubly pinned mass is
also included in $b_{\mathrm{pin}}$.

Let $\Sigma$ denote the full pattern and $Z$ the discovery transcript
under the conditional hypothesis distribution on $S$. The transcript
is determined by $\Sigma$, and after each transcript the realized
endpoint pair $(L,R)$ uniquely describes the positive pattern. Use a
fixed dummy pair on already determined routes. The entropy chain rule
then gives
\[
 w(S)H((L,R)\mid Z)=w(S)H(\Sigma\mid Z)=I(S,\Pi)-J(S),
\]
and $H((L,R)\mid Z)=H(L\mid Z)+H(R\mid L,Z)$.
Lemma~\ref{lem:alphabetic-endpoints} bounds the conditional search cost
by these entropy terms divided by $\ln2$, plus the overheads already
counted. Consequently additional endpoint work is at most
\[
 4b-2b_{\mathrm{pin}}-2b_{\mathrm{both}}
     +\frac{I-J}{\ln2}.
\]
Adding Lemma~\ref{lem:hull-discovery} proves the claim.
''')

edit('06-expected-depth.tex',
     'At a nonsingleton state $S$:\n\\begin{enumerate}',
     '\\begin{lemma}[Flat-state discrete credit]',
     r'''Algorithm~\ref{alg:expected-tree}, in its \emph{vertex} variant,
gives the recursion. A mass-balanced supplied line is queried directly.
Otherwise compute the common-witness hull and execute the full-pattern
stage of Lemma~\ref{lem:pruning-macro}; recurse on its classes and stop
at singletons. Its schedule comes from Algorithm~\ref{alg:batch-orders}
with score $\MSSC(G)+w(A_0)|G|$. All decisions use the supplied
incidence table and rational probabilities. The optima and restriction
credit occur only in the analysis.

''')

path=ROOT/'sections'/'06-expected-depth.tex'
text=path.read_text(encoding='utf-8')
anchor='\\begin{theorem}[Constant expected-depth approximation]'
conversion=r'''\begin{lemma}[Common stage-to-tree conversion]\label{lem:stage-conversion}
Suppose a recursive algorithm uses mass-balanced queries and flat
full-pattern stages, and every flat stage satisfies
\[
 W\le A\Delta_{\mathrm E}+Bb+\frac{I-J}{\ln2},\qquad
 0\le J\le I,\qquad J\ge b\sigma(\delta),
\]
with nonnegative $A,B$. Put
$c=\max\{1/h(\delta),B/\sigma(\delta)\}$. Then
\[
 c_{\mathrm E}(T(S))\le A\OPT_{\mathrm E}(S)+c\mathcal E(S)
 \le(A+c\ln2)\OPT_{\mathrm E}(S).
\]
\end{lemma}
\begin{proof}
Binary entropy is minimized on $[\delta,1-\delta]$ at an endpoint,
so a balanced query has information at least $w(S)h(\delta)$ and
costs at most $cI$. Also $c\ge1/\ln2$. A flat stage satisfies
\[
 Bb+\frac{I-J}{\ln2}\le cJ+c(I-J)=cI.
\]
Thus every stage costs at most $A\Delta_{\mathrm E}+cI$. The identities
$\Delta_{\mathrm E}=\OPT_{\mathrm E}(S)-\sum_A\OPT_{\mathrm E}(A)$
and $I=\mathcal E(S)-\sum_A\mathcal E(A)$ telescope over the disjoint
recursive classes; both potentials vanish at singleton leaves.
Lemma~\ref{lem:restriction} gives the last inequality.
\end{proof}

'''
text=text.replace(anchor,conversion+anchor,1)
path.write_text(text,encoding='utf-8')

edit('06-expected-depth.tex',
     '\\begin{proof}\nPut $c=c(\\delta)$. We first bound',
     'The concrete constant can be certified',
     r'''\begin{proof}
Lemma~\ref{lem:flat-discrete-credit}, with its nonpositive pinning terms
discarded, supplies the local stage bound. Equation~\eqref{eq:pattern-entropy-slack}
supplies the capped-transcript bound. Apply
Lemma~\ref{lem:stage-conversion} with $A=A_\beta$ and
$B=B_{\beta,\delta}$ to obtain the additive guarantee and
\eqref{eq:parameter-ratio}.

''')

edit('06c-polynomial-block-improvement.tex',
     '\\begin{proof}\nAt a balanced state, the query cost is',
     'For completeness, the numerical certificate',
     r'''\begin{proof}
Apply Lemma~\ref{lem:stage-conversion} to
\eqref{eq:poly-block-local} and \eqref{eq:poly-block-entropy}.
This proves the additive guarantee and its stated ratio.

''')

edit('06e-adaptive-block-modes.tex',
     '\\begin{proof}\nUse \\eqref{eq:coarse-discovery-cap}',
     'The exact rational certificate',
     r'''\begin{proof}
Apply Lemma~\ref{lem:stage-conversion} with $B=B_*$ to
\eqref{eq:adaptive-local} and \eqref{eq:coarse-discovery-cap}.
The coarsened transcript is a function of the full pattern, so
$0\le J_*\le I$ and the lemma applies unchanged.

''')

# Add concise references where the constructions are first developed.
refs={
 '02-preliminaries.tex':('These recurrences define the quantities used in the analysis;',
  'Algorithm~\\ref{alg:exact-tree} implements these recurrences on the\\nsmall local states used later. These recurrences define the quantities used in the analysis;'),
 '03-common-witness-geometry.tex':('we prove the structural facts shared by both algorithms.',
  'we prove the structural facts shared by both algorithms.\\nAlgorithm~\\ref{alg:hull-data} records their common preprocessing.'),
 '05-scheduling.tex':('For ordinary intervals, number the candidates',
  'Algorithm~\\ref{alg:interval-cover} gives both interval oracles.\\nFor ordinary intervals, number the candidates'),
 '06a-quasipolynomial.tex':('Let $M$ candidates be in linear spatial order,',
  'Algorithm~\\ref{alg:grade-dp} gives the shared DP; Algorithm~\\ref{alg:qp-baselines}\\nuses it in the two recursions, and Algorithm~\\ref{alg:rollout} performs\\nthe exact initial-tree optimization.\\n\\nLet $M$ candidates be in linear spatial order,'),
 '06b-restricted-approximation.tex':('Let $K$ be the minimum number of supplied caps covering $P$.',
  'Algorithm~\\ref{alg:bounded-caps} gives the construction.\\nLet $K$ be the minimum number of supplied caps covering $P$.'),
 '06d-polynomial-slot-scheduling.tex':('Candidates are the integers $1,\\ldots,M$.',
  'Algorithm~\\ref{alg:slot-dp} specifies the rank-subset DP, and\\nAlgorithm~\\ref{alg:hybrid-tree} gives the capped recursion.\\nCandidates are the integers $1,\\ldots,M$.'),
 '07-boundary-outcomes.tex':('In this section a supplied line returns one of three answers:',
  'Algorithm~\\ref{alg:boundary} implements the reduction below.\\nIn this section a supplied line returns one of three answers:')
}
for name,(old,new) in refs.items():
    p=ROOT/'sections'/name
    t=p.read_text(encoding='utf-8')
    assert old in t,name
    p.write_text(t.replace(old,new.replace('\\n','\n'),1),encoding='utf-8')

p=ROOT/'sections'/'06b-restricted-approximation.tex'
t=p.read_text(encoding='utf-8')
t=t.replace('We work with raw weights; normalization preserves ratios.',
            'Algorithm~\\ref{alg:pair-eptas} records the steps.\\nWe work with raw weights; normalization preserves ratios.'.replace('\\n','\n'),1)
p.write_text(t,encoding='utf-8')

p=ROOT/'sections'/'06e-adaptive-block-modes.tex'
t=p.read_text(encoding='utf-8')
t=t.replace('Use the mode attaining this maximum.',
 'Algorithm~\\ref{alg:block-mode} selects the mode attaining this maximum;\\nAlgorithm~\\ref{alg:expected-tree} gives the full recursion.'.replace('\\n','\n'),1)
p.write_text(t,encoding='utf-8')

print('Added algorithm references and shortened four proof families; numerical certificates retained.')
