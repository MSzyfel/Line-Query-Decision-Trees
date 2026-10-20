"""Independent exact audit of laminar profile and restriction separation.

Floating simplex is used only to discover small primal/dual certificates.
Every reported lower and upper bound is repaired and checked with Fractions.
"""
from __future__ import annotations

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import random
import sys

spec = importlib.util.spec_from_file_location(
    "profile_audited", Path(__file__).with_name("research-general-laminar-profile.py"))
P = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = P
spec.loader.exec_module(P)
CERTIFICATES = []


def restriction_value(tree, selected, weights):
    total = Fraction(0)
    for node in P.BACK.tree_nodes(tree):
        if node.test < 0:
            continue
        if selected & node.left.state and selected & node.right.state:
            total += weights[node.state] * (selected & node.state).bit_count()
    return total


def combined_separate(tree, test, profiles, weights):
    def visit(node):
        if node.test < 0:
            key = (1, 0) if node.state & test else (0, 1)
            return {(0, 0): (Fraction(0), 0), key: (Fraction(0), node.state)}
        left, right = visit(node.left), visit(node.right)
        result = {}
        profile, gamma = profiles[node.state], weights[node.state]
        for (rl, bl), (vl, ml) in left.items():
            for (rr, br), (vr, mr) in right.items():
                r, b = rl + rr, bl + br
                feature = ((r+b) * int(rl+bl > 0 and rr+br > 0)
                           - r * int(rl > 0 and rr > 0)
                           - b * int(bl > 0 and br > 0))
                assert feature >= 0
                score = (vl + vr + profile[r+b] - profile[r] - profile[b]
                         + gamma * feature)
                if (r, b) not in result or score > result[r, b][0]:
                    result[r, b] = score, ml | mr
        return result
    table = visit(tree)
    return max((score / (r+b), selected)
               for (r, b), (score, selected) in table.items() if r+b)


def simplex_with_dual(c, constraints, max_pivots=30000):
    n, m = len(c), len(constraints)
    tableau = []
    for i, (a, rhs) in enumerate(constraints):
        tableau.append(list(map(float, a))
                       + [float(i == j) for j in range(m)] + [float(rhs)])
    tableau.append([-float(x) for x in c] + [0.0] * (m+1))
    basis = list(range(n, n+m))
    width = n+m+1
    for pivot in range(max_pivots):
        entering = next((j for j in range(width-1)
                         if tableau[-1][j] < -1e-8), None)
        if entering is None:
            primal = [Fraction(0)] * n
            for i, variable in enumerate(basis):
                if variable < n:
                    primal[variable] = Fraction(max(0.0, tableau[i][-1])).limit_denominator(10**6)
            dual = [Fraction(max(0.0, value)).limit_denominator(10**6)
                    for value in tableau[-1][n:n+m]]
            # Constraints 0..n-1 are the valid coordinate upper bounds.
            # Repair every exact dual deficit with its corresponding box.
            for j in range(n):
                residual = Fraction(c[j]) - sum(
                    dual[i] * constraints[i][0][j] for i in range(m))
                if residual > 0:
                    dual[j] += residual
            assert all(value >= 0 for value in dual)
            assert all(sum(dual[i] * constraints[i][0][j] for i in range(m))
                       >= c[j] for j in range(n))
            upper = sum(value * rhs for value, (_, rhs) in zip(dual, constraints))
            return primal, upper, pivot, dual
        possible = [i for i in range(m) if tableau[i][entering] > 1e-9]
        assert possible
        leaving = min(possible, key=lambda i: (
            tableau[i][-1] / tableau[i][entering], basis[i]))
        scale = tableau[leaving][entering]
        tableau[leaving] = [value / scale for value in tableau[leaving]]
        row = tableau[leaving]
        for i in range(m+1):
            if i == leaving:
                continue
            multiplier = tableau[i][entering]
            if abs(multiplier) > 1e-12:
                tableau[i] = [tableau[i][j] - multiplier * row[j]
                              for j in range(width)]
        basis[leaving] = entering
    raise AssertionError("finite audit simplex limit")


def exact_profile_interval(instance, tree, combined=False):
    variables = P.feature_variables(tree)
    nodes = [node for node in P.BACK.tree_nodes(tree) if node.test >= 0] if combined else []
    count = len(variables)
    c = ([int(size == state.bit_count()) for state, size in variables]
         + [node.state.bit_count() for node in nodes])
    def coefficients(selected, test):
        result = P.cut_coefficients(variables, selected, test)
        for node in nodes:
            rl = (selected & node.left.state & test).bit_count()
            bl = (selected & node.left.state & ~test).bit_count()
            rr = (selected & node.right.state & test).bit_count()
            br = (selected & node.right.state & ~test).bit_count()
            r, b = rl + rr, bl + br
            result.append((r+b) * int(rl+bl > 0 and rr+br > 0)
                          - r * int(rl > 0 and rr > 0)
                          - b * int(bl > 0 and br > 0))
        return result
    def decode(vector):
        return (P.vector_profiles(tree, variables, vector[:count]),
                {node.state: vector[count+j] for j, node in enumerate(nodes)})
    def separation(profiles, weights, test):
        return (combined_separate(tree, test, profiles, weights)
                if combined else P.separate(tree, test, profiles))
    constraints, seen = [], set()
    for j in range(len(c)):
        row = [0] * len(c)
        row[j] = 1
        bound = variables[j][1] * (variables[j][1]-1) if j < count else 1
        constraints.append((row, bound))
    for test in instance.tests:
        constraints.append((coefficients(instance.full, test), instance.n))
        seen.add((instance.full, test))
    for iteration in range(60):
        primal, upper, _, dual = simplex_with_dual(c, constraints)
        profiles, weights = decode(primal)
        maximum_ratio = Fraction(1)
        added = 0
        for test in instance.tests:
            ratio, witness = separation(profiles, weights, test)
            maximum_ratio = max(maximum_ratio, ratio)
            if ratio > 1 and (witness, test) not in seen:
                seen.add((witness, test))
                constraints.append((coefficients(witness, test),
                                    witness.bit_count()))
                added += 1
        if not added:
            repaired = [value / maximum_ratio for value in primal]
            exact_profiles, exact_weights = decode(repaired)
            assert all(separation(exact_profiles, exact_weights, test)[0] <= 1
                       for test in instance.tests)
            lower = sum(value * coefficient for value, coefficient in zip(repaired, c))
            assert lower <= upper
            CERTIFICATES.append({
                "n": instance.n, "tests": list(instance.tests), "combined": combined,
                "lower": str(lower), "upper": str(upper),
                "primal": [str(value) for value in repaired],
                "objective": c,
                "dual_constraints": [
                    {"weight": str(value), "coefficients": row, "rhs": rhs}
                    for value, (row, rhs) in zip(dual, constraints) if value]})
            return lower, upper, iteration+1
    raise AssertionError("finite audit cutting-plane limit")


def audit_combined():
    rng = random.Random(19102026)
    cases = negative_profile_terms = 0
    for n in range(2, 9):
        for _ in range(8):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(4)]
            tests += [sum(1 << h for h in range(n) if h >> b & 1)
                      for b in range((n-1).bit_length())]
            instance = P.BACK.Instance(n, tests)
            tree = instance.greedy(instance.full)
            variables = P.feature_variables(tree)
            profiles = P.vector_profiles(tree, variables,
                        [Fraction(rng.randrange(21), 7) for _ in variables])
            weights = {node.state: Fraction(rng.randrange(11), 9)
                       for node in P.BACK.tree_nodes(tree) if node.test >= 0}
            for test in instance.tests:
                result, witness = combined_separate(tree, test, profiles, weights)
                def brute(selected):
                    red, blue = selected & test, selected & ~test
                    value = (P.deficit(tree, selected, test, profiles)
                             + restriction_value(tree, selected, weights)
                             - restriction_value(tree, red, weights)
                             - restriction_value(tree, blue, weights))
                    return value / selected.bit_count()
                assert result == max(brute(selected) for selected in range(1, 1 << n))
                assert result == brute(witness)
                for node in P.BACK.tree_nodes(tree):
                    if node.test < 0:
                        continue
                    profile = profiles[node.state]
                    r = (node.state & test).bit_count()
                    b = node.state.bit_count() - r
                    negative_profile_terms += int(profile[r+b] - profile[r] - profile[b] < 0)
                cases += 1
    return {"combined_exact_separation_cases": cases,
            "negative_node_profile_deficits_encountered": negative_profile_terms}


def seek_small_quality_gap():
    rng = random.Random(26062026)
    examined = optimized = 0
    records = []
    for attempt in range(1500):
        n = 8
        tests = sorted({rng.randrange(1, (1 << n)-1) & ~1
                        for _ in range(rng.randrange(4, 8))} - {0})
        # Explicit identifying check avoids calling greedy on unresolved input.
        if len({tuple((test >> h) & 1 for test in tests) for h in range(n)}) < n:
            continue
        examined += 1
        instance = P.BACK.Instance(n, tests)
        tree = instance.greedy(instance.full)
        optimum = instance.exact_cost()
        # Do not count examples where the root entropy/count profile is
        # already exact; these cannot demonstrate hierarchy sensitivity.
        unrestricted = n * ((n-1).bit_length()) - ((1 << ((n-1).bit_length())) - n)
        if tree.cost == optimum or optimum <= unrestricted:
            continue
        lower, upper, rounds = exact_profile_interval(instance, tree)
        optimized += 1
        row = {"n": n, "tests": tests, "greedy": tree.cost, "optimum": optimum,
               "profile_lower": str(lower), "profile_upper": str(upper),
               "cut_rounds": rounds, "strict_certified_gap": upper < optimum}
        records.append(row)
        if upper < optimum:
            lo, hi, combined_rounds = exact_profile_interval(instance, tree, combined=True)
            row.update({"combined_lower": str(lo), "combined_upper": str(hi),
                        "combined_cut_rounds": combined_rounds})
            break
        if optimized >= 3:
            break
    return {"identifying_instances_examined": examined,
            "nonoptimal_greedy_hierarchies_optimized": optimized,
            "records": records}


def main():
    result = {"status": "passed", "floating_search_has_exact_repaired_certificates": True,
              **audit_combined(), "quality_search": seek_small_quality_gap()}
    Path(__file__).with_name("research-general-laminar-profile-audit-results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    Path(__file__).with_name("research-general-laminar-profile-audit-certificates.json").write_text(
        json.dumps(CERTIFICATES, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
