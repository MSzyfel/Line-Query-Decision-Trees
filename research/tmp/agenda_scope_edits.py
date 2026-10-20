from pathlib import Path
p=Path('planar-line-query-research-agenda.md')
text=p.read_text(encoding='utf-8')
text=text.replace(' Quantified reduction gaps give explicit input-dependent inapproximability thresholds for all three settings below.', '')
text=text.replace('| Uniform expected-depth complexity | Strong NP-completeness and no FPTAS | Exact cloud transfer and quantified integer gap; integrated in TeX |',
                  '| Uniform expected-depth complexity | Strong NP-completeness | Exact cloud transfer; integrated in TeX |')
text='\n'.join(line for line in text.split('\n') if not line.startswith('| Inapproximability |'))
text=text.replace('### Uniform hardness and explicit approximation gaps', '### Uniform expected-depth hardness')
start=text.index('Polynomially bounded weights therefore give a polynomial reduction establishing uniform expected-depth strong NP-completeness.')
end=text.index('### General polynomial maximum-depth improvement',start)
text=text[:start]+'''Polynomially bounded weights therefore give a polynomial reduction establishing uniform expected-depth strong NP-completeness. The cloud identity holds for arbitrary adaptive trees, because a cost-nonincreasing singleton rotation removes private queries from the distinguished spine before any cloud is hit. The geometric and full Bellman checks are retained as support for that identity.

The cloud family inherits its EPTAS because adding the same fixed nonnegative cloud cost preserves approximation ratios. A constant-factor hardness proof therefore needs a different construction. The current manuscript intentionally omits shrinking-factor inapproximability and routine FPTAS consequences, and focuses on the substantive exact hardness results and the open constant-factor question.

'''+text[end:]
text=text.replace('Uniform E strong NP-completeness via cloud transfer; explicit shrinking gaps;',
                  'Uniform E strong NP-completeness via cloud transfer;')
start=text.index('## 5 An immediate inapproximability corollary')
end=text.index('## 6 Why the current reductions do not give a fixed factor gap',start)
text=text[:start]+text[end:]
text=text.replace(' and is consistent with no FPTAS.', '.')
text=text.replace('Uniform expected depth is strongly NP-complete, and all three objective/prior settings have explicit input-dependent approximation gaps.',
                  'Uniform expected depth is strongly NP-complete. Constant-factor inapproximability remains open; size-dependent gaps are omitted from the manuscript.')
p.write_text(text,encoding='utf-8')
print('Updated research agenda scope.')
