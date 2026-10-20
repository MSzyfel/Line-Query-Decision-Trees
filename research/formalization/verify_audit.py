"""Accept only Lean's ordinary classical foundations in printed dependencies."""
from pathlib import Path
import json
import re

ROOT = Path(__file__).resolve().parent
text = (ROOT / "axiom-audit.log").read_text(encoding="utf-8-sig")
allowed = {"propext", "Classical.choice", "Quot.sound"}
lists = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", text)
axiom_free = len(re.findall(r"does not depend on any axioms", text))
for dependency_list in lists:
    found = {name.strip() for name in dependency_list.split(",") if name.strip()}
    if not found <= allowed:
        raise SystemExit(f"Unexpected axiom dependencies: {sorted(found - allowed)}")
declarations = json.loads((ROOT / "proved-declarations.json").read_text())
if len(lists) + axiom_free != len(declarations):
    raise SystemExit(f"Expected {len(declarations)} audited declarations, found {len(lists) + axiom_free}")
print(f"Lean audited {len(declarations)} proved declarations; only standard classical foundations occur.")
