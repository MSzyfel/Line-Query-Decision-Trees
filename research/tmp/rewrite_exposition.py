from pathlib import Path
import re

root=Path(__file__).resolve().parents[1]
def read(name): return (root/name).read_text(encoding="utf-8")
def write(name,s): (root/name).write_text(s,encoding="utf-8")

# Move the technical proofs out of the preliminary statement sequence.
s=read("sections/02-preliminaries.tex")
proofs={}
for label in ("thm:kraft","lem:log-sum","lem:entropy-chain-rule",
              "lem:alphabetic-endpoints","lem:restriction"):
    pos=s.index(r"\label{"+label+"}")
    start=s.index(r"\begin{proof}",pos)
    end=s.index(r"\end{proof}",start)+len(r"\end{proof}")
    proofs[label]=s[start:end]
    s=s[:start]+s[end:]
s=s.replace(r"$h(t)=-t\ln t-(1-t)\ln(1-t)$ for $0\le t\le1$.",
    r"$h(t)=-t\ln t-(1-t)\ln(1-t)$ for $0\le t\le1$."+"\n"+
    r"We write $H_2(t)=h(t)/\ln2$ when binary entropy is measured in bits.")
s=s.replace(r"\subsection{Binary codes and ordered comparisons}",r"""
\paragraph{Separate state quantities from calibration choices.}
The state $S$, its mass $w(S)$, pattern classes, and optimal costs
describe the input or the progress of the algorithm. Greek parameters
such as $\delta,\beta,\gamma$ specify construction choices. Their
admissible conditions are stated where needed; their numerical values
are chosen only after the structural proof. A subscripted coefficient
such as $\Phi_\beta$ is a derived accounting function, not another
independent tuning parameter.

\begin{proofstrategy}
The accounting facts below have three roles.
\begin{enumerate}
\item Prefix codes turn query transcripts into information lower bounds.
\item Restriction deletes queries that a known output class no longer needs.
\item Potential differences cancel across recursive states, so local
      charges are paid only once.
\end{enumerate}
The statements are collected first. Their proofs appear together in
the next technical subsection, before the geometric terminology.
\end{proofstrategy}

\subsection{Binary codes and ordered comparisons}
""")
start=s.index("Their differences telescope")
end=s.index(r"\subsection{Convex geometry",start)
s=s[:start]+r"""The approximation proofs bound each stage by these local decreases.
The following cancellation explains why this does not repeatedly
charge the same optimal cost.

\begin{proposition}[Local charges add to a global bound]
\label{prop:potential-cancellation}
Suppose a recursive partition ends in singletons, and its stage at
state $S$ costs at most
$a\Delta_{\mathrm E}(S,\Pi_S)+cI(S,\Pi_S)$.
The complete tree then has expected cost at most
$a\OPT_{\mathrm E}(\HH)+c\mathcal E(\HH)$.
\end{proposition}
\begin{proof}
Sum the stage invoices. Every child's potential appears once with a
minus sign at its parent and once with a plus sign at its own stage.
Only the root values remain, because both potentials vanish on
singleton leaves.
\end{proof}

\subsection{Proofs of the coding and accounting facts}

"""+s[end:]
tech=proofs["thm:kraft"].replace(r"\begin{proof}",r"\begin{proof}[Proof of Theorem~\ref{thm:kraft}]",1)+"\n\n"
tech+=proofs["lem:log-sum"].replace(r"\begin{proof}",r"\begin{proof}[Proof of Lemma~\ref{lem:log-sum}]",1)+"\n\n"
tech+=proofs["lem:entropy-chain-rule"].replace(r"\begin{proof}",r"\begin{proof}[Proof of Lemma~\ref{lem:entropy-chain-rule}]",1)+"\n\n"
ap=proofs["lem:alphabetic-endpoints"]
ap=ap.removeprefix(r"\begin{proof}").removesuffix(r"\end{proof}").strip()
cut1=ap.index("Since $")
cut2=ap.index("To minimize expected depth")
pieces=(ap[:cut1],ap[cut1:cut2],ap[cut2:])
tech+=r"""\begin{proofstrategy}
For Lemma~\ref{lem:alphabetic-endpoints}, place a small dyadic cell
inside each probability interval. Disjoint cells preserve outcome
order; their depths give the coding bound. A separate interval
recurrence optimizes the executable threshold tree.
\end{proofstrategy}
"""
for title,piece in zip(("Ordered disjoint cells give an alphabetic code",
                        "Threshold implementation preserves the depth bound",
                        "An interval recurrence minimizes expected depth"),pieces):
    tech+="\n"+r"\begin{claim}["+title+"]\n"+r"\label{clm:alphabetic-"+str(pieces.index(piece)+1)+"}\n"
    statements=[
      r"The midpoint cells are disjoint, occur in outcome order, and form an alphabetic prefix code.",
      r"Ordered threshold queries implement the code with depth at most $\log_2(1/\Pr[Y=y])+2$ on outcome $y$.",
      r"Optimal expected-depth threshold comparison uses a polynomial interval dynamic program."]
    tech+=statements[pieces.index(piece)]+"\n"+r"\end{claim}"+"\n"+r"\begin{proof}"+"\n"+piece+"\n"+r"\end{proof}"+"\n"
tech+=r"""
\begin{proof}[Proof of Lemma~\ref{lem:alphabetic-endpoints}]
Claims~\ref{clm:alphabetic-1} and~\ref{clm:alphabetic-2} construct
the stated executable code; averaging its pointwise bound proves
the expected-depth inequality. Claim~\ref{clm:alphabetic-3} gives
the optimal threshold-tree algorithm.
\end{proof}
"""
rp=proofs["lem:restriction"].removeprefix(r"\begin{proof}").removesuffix(r"\end{proof}").strip()
cut1=rp.index("For entropy")
cut2=rp.index("For the maximum-depth bound")
pieces=(rp[:cut1],rp[cut1:cut2],rp[cut2:])
tech+=r"""
\begin{proofstrategy}
For Lemma~\ref{lem:restriction}, contract known-answer queries to
obtain feasible subproblem trees. Then use the prefix transcripts in
two ways: Kraft and log-sum bound average depth; the number of binary
leaves bounds maximum depth.
\end{proofstrategy}
"""
statements=(r"Restriction to pairwise disjoint sets cannot increase their total expected optimum or any maximum-depth optimum.",
            r"Every identifying tree has expected cost at least $\mathcal E(S)/\ln2$.",
            r"A binary tree of height $d$ has at most $2^d$ leaves, so identifying $S$ requires height at least $\log_2|S|$.")
for i,(title,piece,statement) in enumerate(zip(
    ("Restriction cannot increase depth","Entropy lower-bounds the expected invoice","Binary capacity lower-bounds height"),pieces,statements),1):
    tech+="\n"+r"\begin{claim}["+title+"]\n"+r"\label{clm:restriction-"+str(i)+"}\n"+statement+"\n"+r"\end{claim}"+"\n"+r"\begin{proof}"+"\n"+piece+"\n"+r"\end{proof}"+"\n"
tech+=r"""
\begin{proof}[Proof of Lemma~\ref{lem:restriction}]
Claim~\ref{clm:restriction-1} gives both restriction inequalities.
Claims~\ref{clm:restriction-2} and~\ref{clm:restriction-3} supply
the two information lower bounds.
\end{proof}
"""
s=s.replace(r"\subsection{Convex geometry and finite set systems}",tech+"\n"+r"\subsection{Convex geometry and finite set systems}",1)
write("sections/02-preliminaries.tex",s)

# Keep the generic batch primitive, but make its three dependencies visible.
s=read("sections/05-scheduling.tex")
s=s.replace(r""",\qquad
 \eta_\beta=\frac{r_\beta+1}{2}
            -\frac{\ln(r_\beta!)}{2\ln\beta}-\lambda_\beta.""", ".")
s=s.replace(r"\lambda_\beta+\eta_\beta",r"\Phi_\beta(1)")
s=s.replace(r"\lambda_\beta t+\eta_\beta",r"\lambda_\beta(t-1)+\Phi_\beta(1)")
s=s.replace(r""" \Phi_\beta(t)
 &=\Phi_\beta(1)""",r""" \Phi_\beta(1)&=\frac{r_\beta+1}{2}
                 -\frac{\ln(r_\beta!)}{2\ln\beta},\\
 \Phi_\beta(t)
 &=\Phi_\beta(1)""",1)
start=s.index(r"\begin{proof}",s.index(r"\label{lem:mssc}"))
end=s.index(r"\input{procedures/batch-orders}",start)
body=s[start:end]
deriv=body.index("No random shift")
derand=body[deriv:body.rindex(r"\end{proof}")]
body=body[:deriv]
introend=body.index(r"\begin{claim}[Phase coverage")
construction=body[len(r"\begin{proof}"):introend]
avgstart=body.index(r"\paragraph{Average the first-cover cost.}")
invbody=body[introend:avgstart]
avgbody=body[avgstart:]
# State definitions outside the result so its dependencies can be read first.
lemma_start=s.index(r"\begin{lemma}[Geometric-batch ordering]")
defs_start=s.index("Fix rational",lemma_start)
defs_end=s.index("A deterministic",defs_start)
defs=s[defs_start:defs_end]
s=s[:defs_start]+s[defs_end:]
lemma_start=s.index(r"\begin{lemma}[Geometric-batch ordering]")
preface=r"""
\subsection{The batch-ordering guarantee}

Fix a nonempty demand family $U$, its minimum cover size $k_0$, and
the waiting weight $p_0$. The only independent scheduling parameter
is the rational growth factor $\beta>1$. The following functions
record the shift-averaged first-cover and length invoices; they are
derived quantities rather than further choices.

"""+defs+r"""
\begin{proposition}[A shifted schedule has a discrete invoice]
\label{prop:batch-invoice}
For a comparison ordering $Q$, put
$r_Q(x)=\sum_{h:t_Q(h)>x}\pi_h$. The shifted construction $G_u$
using budgets $k^{(j)}=\lfloor\beta^ju\rfloor$ satisfies
\[
\MSSC(G_u)\le\frac{\lfloor u\rfloor+1}{2}w(U)
 +\frac12\sum_{j\ge0}(k^{(j)}+k^{(j+1)})r_Q(\beta^ju).
\]
Each such schedule has length at most
$(1+\beta/(\beta-1))k_0$.
\end{proposition}

\begin{proposition}[One shift distribution pays both invoices]
\label{prop:batch-average}
For the log-uniform shift on $[1,\beta)$,
\[
\mathbb E[\MSSC(G_u)]\le\sum_h\pi_h\Phi_\beta(t_Q(h)),
\qquad \mathbb E[|G_u|]\le Z_\beta(k_0).
\]
Moreover $\Phi_\beta(t)\le\lambda_\beta(t-1)+\Phi_\beta(1)$
and $Z_\beta(k)\le\nu_\beta k-1/\ln\beta$.
\end{proposition}

\begin{proposition}[A finite shift search suffices]
\label{prop:batch-derandomization}
For fixed rational $\beta$, polynomially many rational shifts
represent every distinct $G_u$. Minimizing the joint invoice
$\MSSC(G_u)+p_0|G_u|$ over these representatives attains at most
its log-uniform average.
\end{proposition}

\begin{proofstrategy}
\begin{enumerate}
\item Exact budget coverage bounds the mass left after each phase.
\item Greedy order within a phase gives a half-batch first-cover invoice.
\item Average over the same shift for discovery and waiting, then
      choose the best of finitely many distinct schedules.
\end{enumerate}
The averaging is a proof device; the returned schedule is deterministic.
\end{proofstrategy}

"""
s=s[:lemma_start]+preface+s[lemma_start:]
start=s.index(r"\begin{proof}",s.index(r"\label{lem:mssc}"))
end=s.index(r"\input{procedures/batch-orders}",start)
assembly=r"""\begin{proof}
Proposition~\ref{prop:batch-invoice} supplies the shifted schedules.
By Proposition~\ref{prop:batch-average}, their joint expected invoice
has the stated bound. Proposition~\ref{prop:batch-derandomization}
returns a schedule no more expensive than this average. The
length bound holds for every candidate and therefore for the selected one.
\end{proof}

\input{procedures/batch-orders}

\subsection{Proofs of the batch-ordering propositions}

\begin{proof}[Proof of Proposition~\ref{prop:batch-invoice}]
"""+construction+invbody+r"\end{proof}"+"\n\n"+r"\begin{proof}[Proof of Proposition~\ref{prop:batch-average}]"+"\n"+avgbody+r"\end{proof}"+"\n\n"+r"\begin{proof}[Proof of Proposition~\ref{prop:batch-derandomization}]"+"\n"+derand+r"\end{proof}"+"\n"
s=s[:start]+assembly+s[end+len(r"\input{procedures/batch-orders}"):]
s=s.replace("Fix rational $\\beta>1$, and put", "Put")
write("sections/05-scheduling.tex",s)

# Introduction: only current best results and a conceptual reading order.
s=read("sections/01-introduction.tex")
start=s.index(r"\subsection{Results and the main ideas}")
geo=s.index("The geometric structure behind",start)
prefix=r"""\subsection{Results and the main ideas}

\begin{center}
\small
\begin{tabular}{@{}p{0.45\linewidth}p{0.20\linewidth}p{0.26\linewidth}@{}}
\hline
Setup and objective & Guarantee & Running time\\ \hline
General maximum depth & $<4.464966$ & Polynomial\\
General arbitrary-prior expected depth & $<5.182976$ & Polynomial\\
Either general objective & $2+\varepsilon$ & Quasipolynomial\\
All-miss, fixed-size caps: maximum depth & Exact & Polynomial\\
All-miss, weighted singleton/pair paths and cycles: expected depth
 & $1+\varepsilon$ & EPTAS\\
All-miss, uniform fixed-size convex caps: expected depth
 & $1+\varepsilon$ & PTAS\\ \hline
\end{tabular}
\end{center}

Only the strongest algorithm in each setup is presented. Scheduling
and coding procedures are supporting components of those algorithms.
The expected-depth guarantee permits arbitrary strictly positive
rational priors. For $0<\varepsilon\le1$, the general
quasipolynomial algorithms run in
$(mn)^{O(\varepsilon^{-1}\log n)}$ time.

Both exact objectives are strongly NP-complete, including expected
depth under a uniform prior. The reductions use integer-coordinate
points on a parabola and supplied line queries. Constant-factor
inapproximability remains open.

"""
s=s[:start]+prefix+s[geo:]
start=s.index("Section~\\ref{sec:preliminaries} fixes notation")
s=s[:start]+r"""\begin{proofstrategy}
\textbf{Reading order.}
\begin{enumerate}
\item Sections~\ref{sec:preliminaries}--\ref{sec:geometry} explain the
      model, restriction credits, and the circular-interval geometry.
\item Sections~\ref{sec:worst}--\ref{sec:scheduling} build the
      deadline and weighted-coverage primitives.
\item Sections~\ref{sec:mass-improvement},
      \ref{sec:quasipolynomial}, and~\ref{sec:polynomial-slots}
      assemble the best general approximation algorithms.
\item Sections~\ref{sec:small-caps}--\ref{sec:uniform-cap-ptas}
      exploit bounded caps. The randomized mixture setup follows,
      connecting expected-depth oracles to mathematical programming.
\item Sections~\ref{sec:boundaries}--\ref{sec:uniform-hardness}
      treat boundary answers and strong NP-completeness.
\end{enumerate}
Each long result first states its supporting propositions and gives
the overall proof. The next subsection proves those propositions.
Construction parameters are calibrated only after the structural argument.
\end{proofstrategy}
"""
# The old maximum-depth explanation no longer calls a weaker algorithm a result.
s=s.replace("A priority-greedy fallback preserves", "The priority fallback preserves")
write("sections/01-introduction.tex",s)

s=read("sections/09-conclusion.tex")
start=s.index("Retaining an orientation credit")
end=s.index("In both analyses",start)
s=s[:start]+"""The final algorithm chooses its first two coverage budgets jointly
with the geometric shift and the two-endpoint mode. Signed
first-cover corrections and a separate all-negative waiting invoice
retain both restriction and information credits.
"""+s[end:]
start=s.index("The quasipolynomial algorithms retain")
end=s.index("The on-line-answer entries",start)
s=s[:start]+"""The quasipolynomial algorithms store compatible discovery grades
rather than optimizing each deadline separately. Their internal
bounds have leading coefficient arbitrarily close to two and an
additive count or entropy potential. Exact logarithmic-depth
lookahead absorbs that potential and gives the final
$(2+\\varepsilon)$ ratio.
"""+s[end:]
write("sections/09-conclusion.tex",s)
print("Preliminaries, batch scheduling, introduction, and conclusion rewritten.")
