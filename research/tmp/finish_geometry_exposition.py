from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]

def proof_end(s,start):
    depth=0
    for m in re.finditer(r"\\(begin|end)\{proof\}",s[start:]):
        depth += 1 if m[1]=="begin" else -1
        if depth==0: return start+m.end()
    raise ValueError("Unclosed proof")

p=root/"sections/02-preliminaries.tex"
s=p.read_text(encoding="utf-8")
for label in ("lem:alphabetic-endpoints","lem:restriction"):
    start=s.index(r"\begin{proof}[Proof of Lemma~\ref{"+label+"}]")
    end=proof_end(s,start)
    block=s[start:end]
    s=s[:start]+s[end:]
    pos=s.index(r"\end{lemma}",s.index(r"\label{"+label+"}"))+len(r"\end{lemma}")
    s=s[:pos]+"\n"+block+s[pos:]
p.write_text(s,encoding="utf-8")

p=root/"sections/03-common-witness-geometry.tex"
s=p.read_text(encoding="utf-8")
summaries={
 "lem:helly":r"""Flatness forces every three majority sides to intersect.
Helly gives a common strict point, and a positive-margin linear
program finds a rational one. The two claims below justify these steps.""",
 "lem:hull-structure":r"""Project each query vector radially to a hull edge.
Its adjacent endpoints dominate that query's cap. A half-plane
intersects the hull boundary in one circular interval; separation
then makes the all-zero class a singleton at most. These three
facts are proved in the technical subsection.""",
 "lem:minimum-interval-cover":r"""On a line, an exchange argument permits choosing the right endpoint
of the earliest-ending demand. On a circle, enumerate one forced
hit and cut there; the remaining problem is linear. The detailed
exchange argument is given below.""",
 "lem:greedy-cover-length":r"""Induct on the comparison cover size. An extreme greedy choice
removes an extreme cover point. An interior choice splits the
remaining interval demands into independent sides whose combined
size-plus-run charge does not increase. The two claims below
make this induction precise. A first circular choice reduces
the circular case to the linear case.""",
 "lem:legal-endpoint-queries":r"""A cached negative neighbor supplies a cut and pins one endpoint.
Otherwise an opposite hull edge gives a cut without asking a query.
In the resulting linear order, supplied hull tests are endpoint
comparisons. The three claims below establish legality, including
degenerate hulls."""
}
proofs=[]
for label,summary in summaries.items():
    pos=s.index(r"\label{"+label+"}")
    start=s.index(r"\begin{proof}",pos)
    end=proof_end(s,start)
    block=s[start:end]
    block=block.replace(r"\begin{proof}",r"\begin{proof}[Proof of Lemma~\ref{"+label+"}]",1)
    proofs.append(block)
    short=r"\begin{proof}"+"\n"+summary+"\n"+r"\end{proof}"
    s=s[:start]+short+s[end:]
s=s.replace("endpoints, as described above;",r"endpoints, as in Lemma~\ref{lem:legal-endpoint-queries};")
s+=r"""

\subsection{Proofs of the geometric and interval facts}

The conceptual bottleneck is the conversion from planar caps to
executable endpoint comparisons. Radial projection gives a
\emph{cover implication}, not equivalence of a cap with its supports.
The proofs keep that distinction explicit. The endpoint cut is
deduced from geometry or cached answers, so it costs no additional query.

"""+("\n\n".join(proofs))+"\n"
p.write_text(s,encoding="utf-8")

p=root/"sections/05-scheduling.tex"
s=p.read_text(encoding="utf-8")
a=s.index(r"\paragraph{Average the first-cover cost.}")
b=s.index(r"\begin{claim}[Shift-averaged schedule length]",a)
chunk=s[a:b].replace(r"\paragraph{Average the first-cover cost.}","",1)
s=s[:a]+r"""\begin{claim}[Shift averaging yields the discrete first-cover function]
The same log-uniform shift satisfies
$\mathbb E[\MSSC(G_u)]\le\sum_h\pi_h\Phi_\beta(t_Q(h))$.
\end{claim}
\begin{proof}
"""+chunk+r"\end{proof}"+"\n\n"+s[b:]
p.write_text(s,encoding="utf-8")
print("Short geometric assembly proofs and separate technical claims installed.")
