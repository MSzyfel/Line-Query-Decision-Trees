"""Exact uniform completion pricing in a rank-and-cardinality code relaxation.

Root research prototype; no UDT approximation theorem is asserted.  A state
has s live equiprobable symbols and b units of positive-answer budget.  Its
capacity is Q**b.  A binary query can put a symbols in the positive child,
which has budget b-1, and s-a in the negative child with budget b.  Stopping
without reward is allowed only at nonsingletons.  Singleton leaves finish.
"""

from fractions import Fraction
import argparse
import json
import math
from pathlib import Path
import random


def capacities(n, q, budget):
    result = [1]
    for _ in range(budget):
        result.append(min(n, q * result[-1]))
    return result


def full_cost(n, q, budget):
    cap = capacities(n, q, budget)
    table = [[None] * (cap[b] + 1) for b in range(budget + 1)]
    for b in range(budget + 1):
        table[b][1] = 0
        for s in range(2, cap[b] + 1):
            table[b][s] = min(
                s + table[b - 1][a] + table[b][s - a]
                for a in range(1, min(cap[b - 1], s - 1) + 1)
            )
    return table[budget][n]


def best_profit(n, q, budget, price):
    """Return (work, completions) maximizing price*completions-work."""
    cap = capacities(n, q, budget)
    table = [[None] * (cap[b] + 1) for b in range(budget + 1)]
    p, denominator = price.numerator, price.denominator
    for b in range(budget + 1):
        table[b][1] = (0, 1)
        for s in range(2, cap[b] + 1):
            best, value = (0, 0), 0
            for a in range(1, min(cap[b - 1], s - 1) + 1):
                positive = table[b - 1][a]
                negative = table[b][s - a]
                work = s + positive[0] + negative[0]
                finished = positive[1] + negative[1]
                profit = p * finished - denominator * work
                if profit > value or (profit == value and finished > best[1]):
                    best, value = (work, finished), profit
            table[b][s] = best
    return table[budget][n]


def density(n, q, budget):
    assert q >= 2 and budget >= 1 and n <= q**budget
    complete = full_cost(n, q, budget)
    price = Fraction(complete, n)
    steps = 0
    while True:
        work, finished = best_profit(n, q, budget, price)
        assert finished > 0
        candidate = Fraction(work, finished)
        steps += 1
        if candidate == price:
            return {
                "n": n, "Q": q, "budget": budget,
                "full_work": complete, "full_mean": float(Fraction(complete, n)),
                "density": str(price), "density_float": float(price),
                "work": work, "completed": finished, "iterations": steps,
                "full_to_partial": float(Fraction(complete, n) / price),
            }
        assert candidate < price
        price = candidate


def exhaustive(n, q, budget):
    """Independent all-completion-count DP, for small verification only."""
    cap = capacities(n, q, budget)
    table = [[None] * (cap[b] + 1) for b in range(budget + 1)]
    for b in range(budget + 1):
        table[b][1] = {1: 0}
        for s in range(2, cap[b] + 1):
            costs = {0: 0}
            for a in range(1, min(cap[b - 1], s - 1) + 1):
                for kp, wp in table[b - 1][a].items():
                    for kn, wn in table[b][s - a].items():
                        k, work = kp + kn, s + wp + wn
                        if work < costs.get(k, float("inf")):
                            costs[k] = work
            table[b][s] = costs
    return min(Fraction(w, k) for k, w in table[budget][n].items() if k)


def audit_entropy(rng, q, budget):
    """Random actual abstract policies; independently audit the telescopes."""
    n = q**budget
    work = positives = completed = unfinished_positive = 0
    query_entropy = unfinished_entropy = final_resource = 0.0

    def visit(s, b, depth):
        nonlocal work, positives, completed, unfinished_positive
        nonlocal query_entropy, unfinished_entropy, final_resource
        assert s <= q**b and depth <= n - 1
        if s == 1:
            completed += 1
            final_resource += b
            return
        if rng.random() < 0.35:
            unfinished_positive += s * (budget - b)
            unfinished_entropy += s * math.log2(s)
            final_resource += s * b
            return
        assert b >= 1
        a = rng.randint(1, min(s - 1, q ** (b - 1)))
        p = a / s
        work += s
        positives += a
        query_entropy += s * (-p * math.log2(p) - (1-p) * math.log2(1-p))
        visit(a, b - 1, depth + 1)
        visit(s - a, b, depth + 1)

    visit(n, budget, 0)
    assert math.isclose(query_entropy, n * math.log2(n) - unfinished_entropy,
                        rel_tol=1e-10, abs_tol=1e-8)
    assert math.isclose(positives, n * budget - final_resource, abs_tol=1e-8)
    resource = completed * budget + unfinished_positive
    assert positives <= resource
    assert query_entropy + 1e-7 >= resource * math.log2(q)
    assert work + 1e-7 >= completed * budget * q / math.e
    return completed > 0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-n", type=int, default=729)
    args = parser.parse_args()
    checks = 0
    for q in range(2, 6):
        for b in range(1, 5):
            for n in range(2, min(13, q**b) + 1):
                result = density(n, q, b)
                assert Fraction(result["density"]) == exhaustive(n, q, b)
                checks += 1
    rows = []
    for q in [2, 3, 4, 5, 7, 11, 17, 31]:
        for b in range(1, 7):
            n = q**b
            if n <= args.max_n:
                rows.append(density(n, q, b))
    for row in rows:
        assert row["density_float"] + 1e-10 >= row["Q"] * row["budget"] / math.e
    rng = random.Random(20261018)
    policy_checks = nonempty_checks = 0
    for q in range(2, 8):
        for b in range(1, 5):
            if q**b <= args.max_n:
                for _ in range(100):
                    nonempty_checks += audit_entropy(rng, q, b)
                    policy_checks += 1
    # A non-saturated root really can have a cheaper partial policy.
    warning = density(256, 256, 2)
    assert Fraction(warning["density"]) == Fraction(828, 67)
    assert warning["full_to_partial"] > 1.29
    output = {"exhaustive_checks": checks, "policy_entropy_checks": policy_checks,
              "policies_with_completions": nonempty_checks,
              "non_saturation_counterexample": warning, "results": rows}
    Path("research-general-capacity-pricing-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8"
    )
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
