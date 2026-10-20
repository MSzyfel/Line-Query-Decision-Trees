from pathlib import Path
from collections import Counter
import re

root=Path(__file__).resolve().parents[1]
seen=[]
def expand(path):
    assert path not in seen, path
    seen.append(path)
    s=path.read_text(encoding="utf-8")
    bad=[(i,ord(c)) for i,c in enumerate(s) if ord(c)<32 and c not in "\n\r\t"]
    assert not bad,(path,bad)
    s=re.sub(r"(?<!\\)%[^\n]*","",s)
    return re.sub(r"\\input\{([^}]+)\}",lambda m:expand(root/(m[1]+".tex")),s)

s=expand(root/"planar-line-decision-trees.tex")
labels=Counter(re.findall(r"\\label\{([^}]+)\}",s))
refs=set(re.findall(r"\\(?:ref|eqref|autoref)\{([^}]+)\}",s))
duplicates=[k for k,v in labels.items() if v!=1]
missing=sorted(refs-labels.keys())
assert not duplicates,duplicates
assert not missing,missing
envs=[]
for m in re.finditer(r"\\(begin|end)\{([^}]+)\}",s):
    if m[1]=="begin": envs.append(m[2])
    else:
        assert envs and envs[-1]==m[2],(m[0],envs[-4:])
        envs.pop()
assert not envs,envs
print(f"{len(seen)} active files; {len(labels)} unique labels; all {len(refs)} references resolve; environments balanced.")

# Flag stale exposition, without traversing the large vendored Lean installation.
for term in ("5.445944","5.283310","5.272565","5.197569","3.7187",
             "sec:polynomial-blocks","sec:adaptive-blocks","sec:first-phase"):
    assert term not in s,term
assert r"\tableofcontents" in s
for path in seen:
    t=path.read_text(encoding="utf-8")
    for m in re.finditer(r"\\begin\{proof\}",t):
        end=t.index(r"\end{proof}",m.start())
        lines=t[m.start():end].count("\n")
        if lines>95: print(f"Long unsplit proof: {path.name}, line {t[:m.start()].count(chr(10))+1}, {lines} lines")
