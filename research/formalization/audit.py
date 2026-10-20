"""Create a Lean axiom audit and reject unfinished/custom-axiom source.

The printed dependency audit is then run by build.ps1 using Lean itself.
"""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
declarations = []
for path in sorted((ROOT / "PlanarQuery").glob("*.lean")):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/-.*?-/", "", text, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    if re.search(r"\b(sorry|admit|native_decide)\b", text):
        raise SystemExit(f"Unfinished or native-evaluation proof in {path.name}")
    if re.search(r"(?m)^\s*(axiom|constant)\s", text):
        raise SystemExit(f"Custom unproved declaration in {path.name}")
    namespace = []
    for line in text.splitlines():
        ns = re.match(r"namespace\s+([\w.]+)", line)
        if ns:
            namespace.append(ns.group(1))
        if re.match(r"end(?:\s+[\w.]+)?\s*$", line) and namespace:
            namespace.pop()
        theorem = re.match(r"(?:@\[[^\]]*\]\s*)?theorem\s+([\w.]+)", line)
        if theorem:
            name = ".".join(namespace + [theorem.group(1)])
            declarations.append(dict(name=name, file=path.name))
lines = ["import PlanarQuery", ""]
lines += ["#print axioms " + entry["name"] for entry in declarations]
(ROOT / "AxiomAudit.lean").write_text("\n".join(lines) + "\n", encoding="utf-8")
(ROOT / "proved-declarations.json").write_text(json.dumps(declarations, indent=2) + "\n", encoding="utf-8")
print(f"Audit prepared for {len(declarations)} proved declarations; source contains no unfinished proofs or custom axioms.")
