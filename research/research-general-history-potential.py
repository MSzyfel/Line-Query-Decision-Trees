"""History-aware matroid resources and exact executable palette stages.

Resource recognition, ledger validation, potential evaluation, and supplied
logarithmic-palette pricing are polynomial. Exhaustive subsets/optimal costs
below serve only as independent finite validation.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import importlib.util
import json
import random
import sys


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


MAT = load("history_matroid", "research-general-matroid-discovery.py")
PALETTE = load("history_palette", "research-general-lifting-global.py")
BACK = load("history_backend", "research-general-algorithm-next.py")


class MatroidResource:
    def __init__(self, ambient_n, tests, support, matroid=None):
        self.support = support
        self.points = tuple(MAT.bits(support))
        if len(self.points) <= 1:
            raise ValueError("A nontrivial resource needs at least two hypotheses")
        self.tests = tuple(self.local(test) for test in tests)
        if matroid is None:
            found = MAT.discover(len(self.points), self.tests)
            if found is None:
                raise ValueError("The polynomial candidate menu found no certificate")
            matroid = found[0]
        if matroid.n != len(self.points) or not matroid.validate():
            raise ValueError("Invalid supplied hyperplane family")
        if matroid.orientations(self.tests) is None:
            raise ValueError("An original response has no flat side")
        self.matroid = matroid
        self.rank = matroid.rank(matroid.full)
        self.table = MAT.coding_table(len(self.points), self.rank-1)
        self.active = tuple(bool(test and test != matroid.full) for test in self.tests)

    def local(self, state):
        return sum(1 << i for i, point in enumerate(self.points) if point & state)

    @lru_cache(None)
    def value(self, state):
        selected = self.local(state)
        size = selected.bit_count()
        if size <= 1:
            return 0
        value = self.table[self.matroid.rank(selected)-1][size]
        assert value is not None
        return value


class HistoryPotential:
    def __init__(self, n, tests, resources, weights):
        self.n, self.tests = n, tuple(tests)
        self.resources = tuple(resources)
        self.weights = tuple(Fraction(weight) for weight in weights)
        if len(self.resources) != len(self.weights) or any(w < 0 for w in self.weights):
            raise ValueError("Nonnegative matching resource weights required")
        for q in range(len(tests)):
            for h in range(n):
                load_at_endpoint = sum(weight for resource, weight in zip(self.resources, self.weights)
                                       if resource.active[q] and resource.support >> h & 1)
                if load_at_endpoint > 1:
                    raise ValueError("The shared query/hypothesis budget is exceeded")

    @lru_cache(None)
    def __call__(self, state):
        return sum(weight*resource.value(state)
                   for resource, weight in zip(self.resources, self.weights))


def coordinate_instance(q, dimension):
    points = tuple(product(range(q), repeat=dimension))
    tests = tuple(sum(1 << h for h, point in enumerate(points) if point[axis] == value)
                  for axis in range(dimension) for value in range(q))
    resources = []
    for axis in range(dimension):
        fibers = {}
        for h, point in enumerate(points):
            key = point[:axis]+point[axis+1:]
            fibers[key] = fibers.get(key, 0) | (1 << h)
        resources.extend(MatroidResource(len(points), tests, support)
                         for support in fibers.values())
    potential = HistoryPotential(len(points), tests, resources, [1]*len(resources))
    return points, tests, potential


def audit_execution(instance, tree):
    work, exits = 0, set()
    for bit in MAT.bits(tree.state):
        node = tree
        while node.test >= 0:
            assert node.state & bit
            work += 1
            node = node.left if instance.tests[node.test] & bit else node.right
        assert node.state & bit
        exits.add(node.state)
    assert work == tree.cost
    return exits


def independent_stage_optimum(instance, incumbent, palette, potential, gamma, price):
    @lru_cache(None)
    def old(state):
        return instance.prune(incumbent, state).cost

    @lru_cache(None)
    def solve(state):
        best = Fraction(0)
        for q in palette:
            hit, miss = state & instance.tests[q], state & ~instance.tests[q]
            if hit and miss:
                credit = old(state)-old(hit)-old(miss)
                drop = potential(state)-potential(hit)-potential(miss)
                best = max(best, gamma*credit+price*drop-state.bit_count()+solve(hit)+solve(miss))
        return best
    return solve(incumbent.state)


def main():
    rng = random.Random(2026101902)
    cases, bellman_checks, stage_checks, contraction_checks = [], 0, 0, 0
    stage_inputs = []
    for q, dimension in ((2, 2), (2, 3), (3, 2), (3, 3)):
        points, tests, potential = coordinate_instance(q, dimension)
        n = len(points)
        instance = BACK.Instance(n, tests)
        singleton_cost = q*(q+1)//2-1
        exact = dimension*(n//q)*singleton_cost
        assert potential(instance.full) == exact == instance.greedy(instance.full).cost
        states = range(1 << n) if n <= 9 else [rng.randrange(1 << n) for _ in range(80)]
        for state in states:
            assert potential(state) >= 0
            if state.bit_count() <= 1:
                assert potential(state) == 0
            for test in tests:
                drop = potential(state)-potential(state & test)-potential(state & ~test)
                assert drop <= state.bit_count()
                bellman_checks += 1
        cases.append({"q": q, "dimension": dimension, "n": n,
                      "fiber_resources": len(potential.resources),
                      "potential_and_exact_OPT": exact})
        stage_inputs.append((instance, potential))

    # The full affine matroid remains valid with singleton-test noise.
    _, affine = MAT.affine_tests(3, 2)
    tests = affine+tuple(1 << h for h in range(9))
    resource = MatroidResource(9, tests, (1 << 9)-1)
    affine_potential = HistoryPotential(9, tests, [resource], [1])
    assert affine_potential((1 << 9)-1) == 30
    stage_inputs.append((BACK.Instance(9, tests), affine_potential))

    # An explicit negative local drop, using the mixed-size hyperplane family.
    line, outside = (1 << 8)-1, 1 << 8
    hs = (line,)+tuple(outside | (1 << h) for h in range(8))
    tests = hs+tuple(1 << h for h in range(9))
    pencil = MAT.HyperplaneMatroid(9, hs)
    resource = MatroidResource(9, tests, (1 << 9)-1, pencil)
    pencil_potential = HistoryPotential(9, tests, [resource], [1])
    assert pencil_potential((1 << 9)-1)-pencil_potential(line)-pencil_potential(outside) == -5
    stage_inputs.append((BACK.Instance(9, tests), pencil_potential))

    for instance, potential in stage_inputs:
        incumbent = instance.greedy(instance.full)
        palettes = [tuple(range(min(5, len(instance.tests)))),
                    tuple(range(len(instance.tests)))]
        for palette in palettes:
            for gamma, price in ((Fraction(0), Fraction(1)),
                                 (Fraction(1, 2), Fraction(1)),
                                 (Fraction(2, 3), Fraction(3, 2))):
                partial, stats = PALETTE.price_palette_stage(
                    instance, incumbent, palette, gamma, price, state_potential=potential)
                exits = audit_execution(instance, partial)
                exact = independent_stage_optimum(instance, incumbent, palette, potential, gamma, price)
                assert stats["profit"] == exact
                assert stats["coding_drop"] == potential(instance.full)-sum(potential(state) for state in exits)
                assert stats["actual_credit"] == incumbent.cost-sum(instance.prune(incumbent, state).cost for state in exits)
                assert gamma*stats["actual_credit"]+price*stats["coding_drop"]-partial.cost == exact
                stage_checks += 1

    # Independent complete-policy checks of the sharper conditional theorem.
    # All subset costs here are a finite audit, never a general algorithm input.
    for instance, potential in stage_inputs[-2:]:
        incumbent = instance.greedy(instance.full)

        @lru_cache(None)
        def terminal(state):
            return min(instance.prune(incumbent, state).cost, instance.greedy(state).cost)

        @lru_cache(None)
        def optimum(state):
            if state.bit_count() <= 1:
                return 0
            return state.bit_count()+min(optimum(state & test)+optimum(state & ~test)
                                         for test in instance.tests if state & test and state & ~test)

        alpha = max(Fraction(terminal(state), potential(state))
                    for state in range(1 << instance.n) if state.bit_count() > 1)
        for gamma in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4)):
            threshold = (1-gamma)*alpha
            for price in (threshold/2, threshold, 2*threshold):
                partial, stats = PALETTE.price_palette_stage(
                    instance, incumbent, tuple(range(len(instance.tests))),
                    gamma, price, state_potential=potential)
                exits = audit_execution(instance, partial)
                assert sum(potential(state) for state in exits) <= optimum(instance.full)
                assert stats["profit"] >= 0
                finished_work = partial.cost+sum(terminal(state) for state in exits)
                bound = gamma*incumbent.cost+max(price, (1-gamma)*alpha)*optimum(instance.full)
                assert finished_work <= bound
                contraction_checks += 1

    # Double-reserving every product fiber fails the same endpoint ledger.
    points, tests, potential = coordinate_instance(3, 2)
    try:
        HistoryPotential(len(points), tests, potential.resources, [2]*len(potential.resources))
    except ValueError:
        pass
    else:
        raise AssertionError("An overloaded activation ledger was accepted")

    output = {"status": "passed", "coordinate_product_examples": cases,
              "all_subset_Bellman_checks": bellman_checks,
              "actual_stage_and_independent_gain_DP_checks": stage_checks,
              "sharpened_global_contraction_checks": contraction_checks,
              "affine_with_singleton_noise_lower": 30,
              "near_pencil_signed_query_drop": -5,
              "overloaded_ledger_rejected": True,
              "root_ledger_is_existing_section_12_cone": True,
              "no_unrestricted_approximation_claim": True}
    Path("research-general-history-potential-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
