"""All-subset separation for arbitrary nonnegative laminar count profiles.

The separation oracle is polynomial.  The optional floating simplex/cut loop
is a SMALL-INSTANCE RESEARCH OPTIMIZER, not the polynomial ellipsoid algorithm
used in the theoretical LP statement.  Its final lower certificate is checked
and scaled using exact rational separation.
"""

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import random
import sys

spec = importlib.util.spec_from_file_location("profile_backend", "research-general-code-lifting.py")
BACK = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = BACK
spec.loader.exec_module(BACK)


def potential(tree, selected, profiles):
    return sum(profiles[v.state][(selected & v.state).bit_count()]
               for v in BACK.tree_nodes(tree) if v.test >= 0)


def deficit(tree, selected, test, profiles):
    return (potential(tree, selected, profiles)
            - potential(tree, selected & test, profiles)
            - potential(tree, selected & ~test, profiles))


def separate(tree, test, profiles):
    def visit(node):
        if node.test < 0:
            key = (1, 0) if node.state & test else (0, 1)
            return {(0, 0): (Fraction(0), 0), key: (Fraction(0), node.state)}
        left, right = visit(node.left), visit(node.right)
        profile = profiles[node.state]
        result = {}
        for (rl, bl), (vl, ml) in left.items():
            for (rr, br), (vr, mr) in right.items():
                r, b = rl + rr, bl + br
                score = vl + vr + profile[r+b] - profile[r] - profile[b]
                if score > result.get((r, b), (float("-inf"), 0))[0]:
                    result[r, b] = score, ml | mr
        return result
    table = visit(tree)
    ratio, witness = max((value / (r+b), selected)
                         for (r, b), (value, selected) in table.items() if r+b)
    assert deficit(tree, witness, test, profiles) == ratio * witness.bit_count()
    return ratio, witness


def feature_variables(tree):
    return [(v.state, size) for v in BACK.tree_nodes(tree) if v.test >= 0
            for size in range(2, v.state.bit_count()+1)]


def vector_profiles(tree, variables, vector):
    profiles = {v.state: [Fraction(0)] * (v.state.bit_count()+1)
                for v in BACK.tree_nodes(tree) if v.test >= 0}
    for (state, size), weight in zip(variables, vector):
        profiles[state][size] = weight
    return profiles


def cut_coefficients(variables, selected, test):
    result = []
    for state, size in variables:
        cell = selected & state
        r, b = (cell & test).bit_count(), (cell & ~test).bit_count()
        result.append(int(r+b == size)-int(r == size)-int(b == size))
    return result


def simplex(c, constraints, max_pivots=30000):
    """Feasible-slack primal simplex for validation; no polynomial claim."""
    n, m = len(c), len(constraints)
    tableau = []
    for i, (a, rhs) in enumerate(constraints):
        assert rhs >= 0
        tableau.append(list(map(float, a)) + [float(i == j) for j in range(m)] + [float(rhs)])
    tableau.append([-float(x) for x in c] + [0.0] * (m+1))
    basis = list(range(n, n+m))
    width = n+m+1
    for pivot in range(max_pivots):
        entering = next((j for j in range(width-1) if tableau[-1][j] < -1e-8), None)
        if entering is None:
            vector = [0.0] * n
            for i, variable in enumerate(basis):
                if variable < n:
                    vector[variable] = max(0.0, tableau[i][-1])
            return vector, pivot
        possible = [i for i in range(m) if tableau[i][entering] > 1e-9]
        if not possible:
            raise AssertionError("bounded profile LP reported unbounded")
        leaving = min(possible, key=lambda i: (tableau[i][-1]/tableau[i][entering], basis[i]))
        scale = tableau[leaving][entering]
        tableau[leaving] = [x/scale for x in tableau[leaving]]
        row = tableau[leaving]
        for i in range(m+1):
            if i == leaving:
                continue
            multiplier = tableau[i][entering]
            if abs(multiplier) > 1e-12:
                tableau[i] = [tableau[i][j]-multiplier*row[j] for j in range(width)]
        basis[leaving] = entering
    raise AssertionError("small validation simplex pivot limit")


def small_profile_lp(instance, tree, max_rounds=100):
    variables = feature_variables(tree)
    c = [int(size == state.bit_count()) for state, size in variables]
    constraints, seen = [], set()
    for j, (_, size) in enumerate(variables):
        row = [0]*len(variables)
        row[j] = 1
        constraints.append((row, size*(size-1)))
    for test in instance.tests:
        row = cut_coefficients(variables, instance.full, test)
        constraints.append((row, instance.n))
        seen.add((instance.full, test))
    total_pivots = 0
    for iteration in range(max_rounds):
        vector, pivots = simplex(c, constraints)
        total_pivots += pivots
        rational = [Fraction(x).limit_denominator(1000000) for x in vector]
        profiles = vector_profiles(tree, variables, rational)
        new_cuts, maximum_ratio = [], Fraction(1)
        for test in instance.tests:
            ratio, witness = separate(tree, test, profiles)
            maximum_ratio = max(maximum_ratio, ratio)
            if ratio > Fraction(10000001, 10000000) and (witness, test) not in seen:
                new_cuts.append((cut_coefficients(variables, witness, test), witness.bit_count()))
                seen.add((witness, test))
        if not new_cuts:
            # This is an EXACT feasible lower certificate, independent of the
            # floating optimizer's optimality or tolerance.
            scaled = [value/maximum_ratio for value in rational]
            exact_profiles = vector_profiles(tree, variables, scaled)
            for test in instance.tests:
                assert separate(tree, test, exact_profiles)[0] <= 1
            lower = sum(value*coefficient for value, coefficient in zip(scaled, c))
            return {"lower_bound": str(lower), "lower_float": float(lower),
                    "variables": len(variables), "cut_rounds": iteration+1,
                    "constraints": len(constraints), "simplex_pivots": total_pivots,
                    "certificate_scaling": str(maximum_ratio)}
        constraints.extend(new_cuts)
    raise AssertionError("small validation cut limit")


def main():
    rng = random.Random(20261020)
    checks = 0
    for n in range(2, 9):
        for _ in range(12):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if h >> b & 1)
                      for b in range((n-1).bit_length())]
            instance = BACK.Instance(n, tests)
            tree = instance.greedy(instance.full)
            variables = feature_variables(tree)
            vector = [Fraction(rng.randrange(17), 8) for _ in variables]
            profiles = vector_profiles(tree, variables, vector)
            for test in instance.tests:
                result = separate(tree, test, profiles)[0]
                brute = max(deficit(tree, selected, test, profiles)/selected.bit_count()
                            for selected in range(1, 1 << n))
                assert result == brute
                checks += 1
    benchmarks = []
    cases = [("cube", 8, [sum(1 << h for h in range(8) if h >> b & 1) for b in range(3)]),
             ("singletons", 8, [1 << h for h in range(8)])]
    q, dimension = 3, 2
    points = [(a, b) for a in range(q) for b in range(q)]
    affine_tests = sorted(set(sum(1 << h for h, point in enumerate(points)
                                  if (a*point[0]+b*point[1]) % q == value)
                             for a in range(q) for b in range(q) if a or b
                             for value in range(q)))
    cases.append(("affine_Q3_d2", 9, affine_tests))
    for name, n, tests in cases:
        instance = BACK.Instance(n, tests)
        tree = instance.greedy(instance.full)
        result = small_profile_lp(instance, tree)
        exact = instance.exact_cost()
        assert Fraction(result["lower_bound"]) <= exact
        result.update({"case": name, "n": n, "greedy": tree.cost, "exact_optimum": exact})
        benchmarks.append(result)
    output = {"separation_checks": checks, "benchmark_certificates": benchmarks,
              "simplex_is_validation_only": True}
    Path("research-general-laminar-profile-results.json").write_text(json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
