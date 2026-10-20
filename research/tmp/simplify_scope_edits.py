from pathlib import Path

def replace(path, old, new):
    p = Path(path)
    text = p.read_text(encoding='utf-8')
    assert old in text, (path, old[:100])
    p.write_text(text.replace(old, new, 1), encoding='utf-8')

p = Path('sections/08a-uniform-hardness.tex')
text = p.read_text(encoding='utf-8')
text = text.split(r'\subsection{A quantitative gap in the weighted reduction}')[0]
text = text.replace(r'\section{Uniform expected-depth hardness and quantitative inapproximability}',
                    r'\section{Uniform expected-depth hardness}')
text = text.replace('We then quantify shrinking approximation gaps for both objectives.\n', '')
text = text.replace('The uniform-prior problem admits no FPTAS unless\n'
                    r'$\mathrm P=\mathrm{NP}$.'+'\n', '')
text = text.replace('For the last statement, the raw uniform optimum is integral\n'
                    'and at most $n(n-1)$. An FPTAS with\n'
                    r'$\varepsilon=1/(2n(n-1))$ returns raw cost less than'+'\n'
                    'the optimum plus one, hence returns the exact optimum in\n'
                    'polynomial time.\n', '')
text += r'''\begin{remark}[Limits of the reduction]
The cloud identity preserves exact hardness but adds the same
nonnegative internal cost $\Delta$ to every matching. An EPTAS for
the compressed weighted path family, such as
Theorem~\ref{thm:pair-eptas}, remains an EPTAS for these explicit
cloud instances: its additive error is at most
$\varepsilon\OPT_{\rm raw}^{\rm weighted}\le
\varepsilon(\OPT_{\rm raw}^{\rm weighted}+\Delta)$.
Thus this reduction does not establish constant-factor
inapproximability. That question requires a different construction.
\end{remark}
'''
p.write_text(text, encoding='utf-8')

p = Path('sections/08-strong-np-completeness.tex')
text = p.read_text(encoding='utf-8')
assert r'\subsection{A consequence for approximation schemes}' in text
p.write_text(text.split(r'\subsection{A consequence for approximation schemes}')[0],
             encoding='utf-8')

replace('planar-line-decision-trees.tex',
        'expected-depth reduction to uniform priors. Neither objective\n'
        r'admits an FPTAS unless $\mathrm P=\mathrm{NP}$. Every query in'+'\n',
        'expected-depth reduction to uniform priors. Every query in\n')

replace('sections/01-introduction.tex',
        'The polynomially bounded integral costs in the reductions\n'
        'also rule out an FPTAS for either objective unless\n'
        r'$\mathrm P=\mathrm{NP}$, including uniform expected depth. Quantified'+'\n'
        'gaps rule out polynomial approximation factors\n'
        r'$1+1/(3\sqrt n)$ for maximum depth, $1+9/(10n^3)$ for arbitrary-prior'+'\n'
        r'expected depth, and $1+100/n^{5/3}$ for uniform expected depth.'+'\n'
        'These input-dependent thresholds do not establish fixed-factor hardness.\n',
        'Constant-factor inapproximability remains open.\n')
replace('sections/01-introduction.tex',
        'an EPTAS is compatible with strong NP-completeness and absence of\n'
        'an FPTAS.',
        'an EPTAS is compatible with strong NP-completeness.')
replace('sections/01-introduction.tex',
        'and quantifies the approximation gaps.',
        'through an exact geometric cloud identity.')

replace('sections/09-conclusion.tex',
        'cost to the weighted optimum. The reductions exclude an FPTAS unless\n'
        r'$\mathrm P=\mathrm{NP}$, and give explicit approximation gaps'+'\n'
        r'$1+1/(3\sqrt n)$, $1+9/(10n^3)$, and $1+100/n^{5/3}$ for maximum,'+'\n'
        'arbitrary-prior expected, and uniform expected depth, respectively.\n'
        'They do not establish fixed-factor\n'
        'inapproximability.',
        'cost to the weighted optimum. Constant-factor inapproximability\n'
        'remains open.')
print('Removed size-dependent hardness and routine FPTAS consequences; retained exact hardness.')
