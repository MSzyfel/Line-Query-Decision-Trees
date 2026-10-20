from pathlib import Path
from fractions import Fraction as Q
from collections import Counter
import re

root = Path(__file__).resolve().parents[1]
visited = []
def expand(path):
    assert path not in visited, f'Duplicate active input: {path}'
    visited.append(path)
    s = path.read_text(encoding='utf-8')
    s = re.sub(r'(?<!\\)%[^\n]*', '', s)
    return re.sub(r'\\input\{([^}]+)\}', lambda m: expand(root / (m[1]+'.tex')), s)

s = expand(root / 'planar-line-decision-trees.tex')
labels = Counter(re.findall(r'\\label\{([^}]+)\}', s))
assert all(v == 1 for v in labels.values()), [k for k,v in labels.items() if v != 1]
refs = set(re.findall(r'\\(?:ref|eqref|autoref)\{([^}]+)\}', s))
assert refs <= labels.keys(), sorted(refs-labels.keys())
bib = set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}', s))
cites = {x.strip() for group in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}', s) for x in group.split(',')}
assert cites <= bib, sorted(cites-bib)
algorithms = s.count(r'\begin{algorithm}')
assert len([k for k in labels if k.startswith('alg:')]) == algorithms
assert '11-algorithm-recipes' not in s and 'cor:no-fptas' not in s
assert 'sec:two-phase-certificate' in labels
assert 'thm:uniform-cap-ptas' in labels
print(f'{len(visited)} active TeX files; {len(labels)} unique labels; all {len(refs)} references resolve; {algorithms} local algorithms.')

# Regression: the initial-family partition must retain k1=k_min+1 even
# when terminal minimum-cover completion truncates the base partition.
beta = Q(3512863, 10**6)
ceil = lambda x: -(-x.numerator//x.denominator)
cells = 0
for kmin in range(1, 81):
    powers = [Q(1)]
    while powers[-1] < kmin:
        powers.append(powers[-1]*beta)
    breaks = {Q(1), beta}
    for p in powers:
        breaks.update(Q(k)/p for k in range(1,kmin+1) if 1<=Q(k)/p<beta)
    for p in (beta,beta**2):
        breaks.update(Q(k)/p for k in range(1,ceil(beta**3)+1) if 1<=Q(k)/p<beta)
    bs = sorted(breaks)
    def signature(u):
        floor = lambda x: x.numerator//x.denominator
        k1,k2 = floor(beta*u), floor(beta**2*u)
        tail=[]
        j=2
        while True:
            k=floor(beta**j*u)
            tail.append(min(k,kmin))
            if k>=kmin: break
            j+=1
        return (k1,k2,tuple(tail))
    for lo,hi in zip(bs,bs[1:]):
        assert signature((2*lo+hi)/3) == signature((lo+2*hi)/3)
        cells += 1
    if 1<=Q(kmin+1)/beta<beta:
        assert Q(kmin+1)/beta in breaks
print(f'{cells} refined shift cells checked across 80 terminal cover sizes.')
