"""Move the centralized recipes to their analysis sites, without editing proofs.

Run from the workspace with ``python tmp/relocate_algorithms.py --check`` to
validate every planned placement without writing; omit --check to apply.
Repeated application is a no-op.  The recipe sources in procedures/ were
extracted verbatim, including the explanatory notes after each algorithm.
"""

from pathlib import Path
import argparse
import re

ROOT = Path(__file__).resolve().parents[1]
MAIN = ROOT / "planar-line-decision-trees.tex"

# Each anchor is a unique semantic boundary, not a line number.  Placement is
# immediately BEFORE its anchor; None appends at the end of the analysis file.
PLAN = [
    ("02-preliminaries", "exact-tree", r"All logarithms are natural unless a base is displayed"),
    ("02-preliminaries", "common-conventions", r"\\subsection\{Binary codes and ordered comparisons\}"),
    ("02-preliminaries", "flow-recursion", r"\\subsection\{Binary codes and ordered comparisons\}"),
    ("02-preliminaries", "alphabetic-code", r"\\subsection\{Restriction and recursive accounting\}"),
    ("03-common-witness-geometry", "hull-data", r"Figure~\\ref\{fig:support-and-interval\} separates"),
    ("03-common-witness-geometry", "endpoint-code", None),
    ("04-maximum-depth", "priority-trial", r"\\subsection\{The recursive maximum-depth algorithm\}"),
    ("04-maximum-depth", "worst-tree", r"\\begin\{theorem\}\[Constant deterministic maximum-depth approximation\]"),
    ("05-scheduling", "interval-cover", r"The next lemma uses exact budgeted covers"),
    ("05-scheduling", "batch-orders", None),
    ("06-expected-depth", "expected-tree", r"\\begin\{lemma\}\[Capped-rank credit conversion\]"),
    ("06e-adaptive-block-modes", "block-mode", r"\\begin\{lemma\}\[Affine block credits\]"),
    ("06g-two-phase-improvement", "flow-expected", r"\\subsection\{One signed correction for each affected cost\}"),
    ("06a-quasipolynomial", "grade-dp", r"\\subsection\{Adjacent support blocks and shifted delays\}"),
    ("06a-quasipolynomial", "qp-baselines", r"\\subsection\{Maximum depth\}"),
    ("06a-quasipolynomial", "rollout", r"\\begin\{theorem\}\s*\\label\{thm:qp-two-plus-epsilon\}"),
    ("06a-quasipolynomial", "flow-quasipolynomial", r"\\begin\{theorem\}\s*\\label\{thm:qp-two-plus-epsilon\}"),
    ("06d-polynomial-slot-scheduling", "slot-dp", r"\\subsection\{The hybrid recursive algorithm\}"),
    ("06d-polynomial-slot-scheduling", "hybrid-tree", r"\\subsection\{Two simultaneous height invariants\}"),
    ("06d-polynomial-slot-scheduling", "flow-worst", r"\\subsection\{Two simultaneous height invariants\}"),
    ("06b-restricted-approximation", "bounded-caps", r"\\begin\{proof\}\s*Algorithm~\\ref\{alg:bounded-caps\}"),
    ("06b-restricted-approximation", "pair-eptas", r"\\begin\{proof\}\s*For \$n=1\$ the zero-query tree is exact"),
    ("07-boundary-outcomes", "boundary", r"\\begin\{proposition\}\[Boundary reduction\]"),
]

RECIPE_LABELS = [
    "exact-tree", "hull-data", "alphabetic-code", "endpoint-code",
    "interval-cover", "priority-trial", "worst-tree", "batch-orders",
    "expected-tree", "block-mode", "grade-dp", "qp-baselines", "rollout",
    "slot-dp", "hybrid-tree", "bounded-caps", "pair-eptas", "boundary",
]


def proposed_changes():
    original = {}
    changed = {}
    for section, procedure, anchor in PLAN:
        path = ROOT / "sections" / (section + ".tex")
        if path not in changed:
            original[path] = path.read_text(encoding="utf-8")
            changed[path] = original[path]
        snippet = ROOT / "procedures" / (procedure + ".tex")
        assert snippet.is_file(), f"Missing standalone procedure: {snippet}"
        text = changed[path]
        input_line = "\\input{procedures/" + procedure + "}"
        existing = text.count(input_line)
        assert existing <= 1, f"Duplicate input: {input_line}"
        if existing:
            continue
        if anchor is None:
            changed[path] = text.rstrip() + "\n\n" + input_line + "\n"
        else:
            matches = list(re.finditer(anchor, text))
            assert len(matches) == 1, (
                f"Anchor must occur exactly once for {procedure} in {path.name}; "
                f"found {len(matches)}: {anchor}"
            )
            at = matches[0].start()
            changed[path] = text[:at] + input_line + "\n\n" + text[at:]

    original[MAIN] = MAIN.read_text(encoding="utf-8")
    changed[MAIN] = original[MAIN]
    centralized = re.compile(
        r"\\appendix\s*\\input\{sections/11-algorithm-recipes\}\s*"
    )
    changed[MAIN], count = centralized.subn("", changed[MAIN])
    assert count <= 1, "Duplicate appendix input"
    assert "\\input{sections/11-algorithm-recipes}" not in changed[MAIN], (
        "Unexpected centralized input without adjacent \\appendix"
    )

    # Check every old label now has precisely one reachable local definition.
    recipe_sources = "\n".join(
        (ROOT / "procedures" / (name + ".tex")).read_text(encoding="utf-8")
        for name in RECIPE_LABELS
    )
    for label in RECIPE_LABELS:
        token = "\\label{alg:" + label + "}"
        assert recipe_sources.count(token) == 1, f"Lost or duplicated {token}"
        caller = [
            section for section, procedure, _ in PLAN if procedure == label
        ]
        assert len(caller) == 1
        path = ROOT / "sections" / (caller[0] + ".tex")
        assert changed[path].count("\\input{procedures/" + label + "}") == 1
    assert len(RECIPE_LABELS) == 18
    return original, changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Validate only; do not write")
    args = parser.parse_args()
    original, changed = proposed_changes()
    modified = [path for path in changed if changed[path] != original[path]]
    if args.check:
        print(f"All 18 recipe placements and 4 diagrams validated; {len(modified)} files would change.")
    else:
        for path in modified:
            path.write_text(changed[path], encoding="utf-8", newline="\n")
        print(f"Applied 18 recipe placements and 4 diagrams; {len(modified)} files changed.")
        # The same virtual operation after writing must leave every file intact.
        second_original, second_changed = proposed_changes()
        assert second_original == second_changed, "Relocation is not idempotent"
        print("Idempotency and unique-label checks passed.")


if __name__ == "__main__":
    main()
