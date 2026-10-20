"""Audit a cooperative-code escape on full row-decoy/gated-column grids.

Large cases verify an explicit full code and a symbolic represented-state
membership certificate; they do not materialize the quadratic state pool.
Small cases run the actual coalition-two pricer as well.
"""

from functools import lru_cache
from pathlib import Path
import importlib.util
import json
import sys
import time


def load_oracle():
    path = Path(__file__).with_name("research-general-pricing-oracle.py")
    spec = importlib.util.spec_from_file_location("grid_pricing_oracle", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


ORACLE = load_oracle()
Instance, tree_nodes = ORACLE.Instance, ORACLE.tree_nodes


def grid_instance(bits, columns, decoy_scale=1):
    rows = 1 << bits
    n = rows * columns
    column_masks = [sum(1 << (row * columns + col) for row in range(rows))
                    for col in range(columns)]
    tests = list(column_masks)
    for col in range(columns):
        for bit in range(bits):
            tests.append(sum(1 << (row * columns + col) for row in range(rows)
                             if row & (1 << bit)))

    @lru_cache(None)
    def row_cost(count):
        if count <= 1:
            return 0
        small = min(count // 2, 1 + decoy_scale * count // columns)
        return count + row_cost(small) + row_cost(count - small)

    def add_decoys(first, count):
        if count <= 1:
            return
        small = min(count // 2, 1 + decoy_scale * count // columns)
        tests.append(((1 << (small * columns)) - 1) << (first * columns))
        add_decoys(first, small)
        add_decoys(first + small, count - small)

    add_decoys(0, rows)
    assert len(tests) == columns + columns * bits + rows - 1
    return Instance(n, tests), column_masks, row_cost(rows)


def audit(bits, columns, scale, run_pricer=False):
    start = time.perf_counter()
    instance, column_masks, row_raw = grid_instance(bits, columns, scale)
    rows = 1 << bits
    incumbent = instance.greedy(instance.full)
    q = lambda c: c * (c + 1) // 2 - 1
    predicted_bad = columns * row_raw + rows * q(columns)
    assert incumbent.cost == predicted_bad, (bits, columns, scale, incumbent.cost, predicted_bad)
    positive = instance.greedy(column_masks[0])
    negative_state = instance.full ^ column_masks[0]
    negative = instance.prune(incumbent, negative_state)
    assert positive.cost == rows * bits
    assert negative.cost == (columns - 1) * row_raw + rows * q(columns - 1)
    candidate = instance.branch(instance.full, 0, positive, negative)
    predicted_saving = row_raw - rows * bits
    assert incumbent.cost - candidate.cost == predicted_saving

    # Every negative-code state is an intersection of an incumbent node
    # (base state) and the forced root's negative cell (also a base state).
    allowed = {node.state & negative_state for node in tree_nodes(incumbent)}
    allowed.update(node.state for node in tree_nodes(positive))
    allowed.add(instance.full)
    assert all(node.state in allowed for node in tree_nodes(candidate))
    record = {"row_bits": bits, "columns": columns, "decoy_scale": scale,
              "n": instance.n, "m": len(instance.tests),
              "row_mean": row_raw / rows, "greedy_mean": incumbent.cost / instance.n,
              "column_first_mean": q(columns) / columns + bits,
              "certified_one_pass_raw_gain": predicted_saving,
              "certified_candidate_mean": candidate.cost / instance.n}
    if run_pricer:
        full_candidate, step = ORACLE.candidate_pass(instance, incumbent,
                                                    include_incident=False,
                                                    include_coalitions=True)
        assert step["profit"] >= predicted_saving
        assert full_candidate.cost <= candidate.cost
        record["actual_coalition_pricer"] = step
    record["seconds"] = round(time.perf_counter() - start, 4)
    return record


if __name__ == "__main__":
    records = []
    for scale, columns in ((1, 4), (2, 8)):
        records.append(audit(4, columns, scale, run_pricer=True))
    for bits, columns, scale in ((6, 8, 1), (8, 8, 1), (10, 8, 1),
                                  (6, 16, 2), (8, 16, 2), (10, 16, 2),
                                  (6, 36, 1), (8, 64, 1)):
        records.append(audit(bits, columns, scale))
    path = Path(__file__).with_name("research-general-pricing-grid-results.json")
    path.write_text(json.dumps(records, indent=2) + "\n", encoding="utf-8")
    for record in records:
        print(json.dumps(record))
    print(f"All product-grid escape audits passed; saved {path.name}")
