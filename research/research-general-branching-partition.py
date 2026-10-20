"""Exact logarithmic-depth search over a small menu of partial-tree macros.

Optimizes adaptive menu policies by Bellman recursion, including all response
branches. Also optimizes raw work against the squared-size frontier moment.
All returned query trees use the original binary response matrix.
"""

from functools import lru_cache
from itertools import product
from pathlib import Path
import importlib.util
import json
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


BACK = load("branching_partition_backend", "research-general-algorithm-next.py")


def leaves(tree):
    return tuple(node for node in BACK.tree_nodes(tree) if node.test < 0)


def graft(instance, partial, continuation):
    if partial.test < 0:
        return continuation[partial.state]
    return instance.branch(partial.state, partial.test,
                           graft(instance, partial.left, continuation),
                           graft(instance, partial.right, continuation))


def cut_at_size(instance, tree, bound):
    if tree.state.bit_count() <= bound or tree.test < 0:
        return BACK.Tree(tree.state)
    return instance.branch(tree.state, tree.test,
                           cut_at_size(instance, tree.left, bound),
                           cut_at_size(instance, tree.right, bound))


def validate(instance, tree):
    work = 0
    for h in range(instance.n):
        if not tree.state >> h & 1:
            continue
        node = tree
        while node.test >= 0:
            hit = node.state & instance.tests[node.test]
            assert hit and hit != node.state
            assert node.left.state == hit and node.right.state == node.state ^ hit
            node = node.left if hit >> h & 1 else node.right
            work += 1
        assert node.state >> h & 1
    assert work == tree.cost
    assert sum(node.state for node in leaves(tree)) == tree.state


def band_menu(instance, state):
    """Two one-query macros: maximum balance and opposite end of its band."""
    candidates = []
    for q, test in enumerate(instance.tests):
        hit = state & test
        if hit and hit != state:
            minority = min(hit.bit_count(), (state ^ hit).bit_count())
            root_minority = min(test.bit_count(), instance.n-test.bit_count())
            candidates.append((minority, root_minority, q))
    if not candidates:
        return ()
    largest = max(item[0] for item in candidates)
    maximum = min((item for item in candidates if item[0] == largest),
                  key=lambda item: (item[1], item[2]))
    # Strictness excludes a private gate with exactly half the best minority.
    band = min((item for item in candidates if 2*item[0] > largest),
               key=lambda item: (item[0], item[1], item[2]))
    output = []
    for q in dict.fromkeys((maximum[2], band[2])):
        hit = state & instance.tests[q]
        output.append(instance.branch(state, q, BACK.Tree(hit), BACK.Tree(state ^ hit)))
    return tuple(output)


class MenuSearch:
    def __init__(self, instance, menu, choices=2):
        self.instance, self.menu_function, self.choices = instance, menu, choices
        self.macros = lru_cache(None)(self._macros)
        self._cut_cache = {}
        self._frontier_cache = {}
        self._template_frontier_cache = {}

    def _macros(self, state):
        if state.bit_count() <= 1:
            return ()
        macros = tuple(self.menu_function(self.instance, state))
        assert len(macros) <= self.choices
        for macro in macros:
            assert macro.state == state
            validate(self.instance, macro)
        return macros

    def cut(self, state, depth, bound):
        """Best menu composition, with fresh greedy mass-cut fallback anywhere."""
        assert depth >= 0 and bound >= 1
        key = state, depth, bound
        if key in self._cut_cache:
            return self._cut_cache[key]
        if state.bit_count() <= bound:
            result = BACK.Tree(state)
        else:
            result = cut_at_size(self.instance, self.instance.greedy(state), bound)
            if depth:
                for original in self.macros(state):
                    macro = cut_at_size(self.instance, original, bound)
                    continuation = {leaf.state: self.cut(leaf.state, depth-1, bound)
                                    for leaf in leaves(macro)}
                    candidate = graft(self.instance, macro, continuation)
                    if candidate.cost < result.cost:
                        result = candidate
        self._cut_cache[key] = result
        return result

    def _combine(self, macro, child_frontiers):
        # Each candidate records the actual continuation trees so grafting
        # never substitutes an unavailable synthetic split.
        combined = {0: (0, {})}
        for state, frontier in child_frontiers:
            updated = {}
            for q0, (work0, codes) in combined.items():
                for q1, child in frontier.items():
                    collision, work = q0+q1, work0+child.cost
                    if collision not in updated or work < updated[collision][0]:
                        updated[collision] = work, {**codes, state: child}
            combined = updated
        return {collision: graft(self.instance, macro, codes)
                for collision, (_, codes) in combined.items()}

    def template_frontier(self, tree):
        """Exact work/collision map over all prunings of one supplied tree."""
        if tree in self._template_frontier_cache:
            return self._template_frontier_cache[tree]
        result = {tree.state.bit_count()**2: BACK.Tree(tree.state)}
        if tree.test >= 0:
            root = self.instance.branch(tree.state, tree.test,
                                        BACK.Tree(tree.left.state), BACK.Tree(tree.right.state))
            candidates = self._combine(root, [(tree.left.state, self.template_frontier(tree.left)),
                                               (tree.right.state, self.template_frontier(tree.right))])
            for collision, code in candidates.items():
                if collision not in result or code.cost < result[collision].cost:
                    result[collision] = code
        self._template_frontier_cache[tree] = result
        return result

    def frontier(self, state, depth):
        """Exact work/collision map, including greedy-prefix fallback anywhere."""
        assert depth >= 0
        key = state, depth
        if key in self._frontier_cache:
            return self._frontier_cache[key]
        result = dict(self.template_frontier(self.instance.greedy(state)))
        if depth and state.bit_count() > 1:
            for macro in self.macros(state):
                candidates = self._combine(macro, [(leaf.state, self.frontier(leaf.state, depth-1))
                                                   for leaf in leaves(macro)])
                for collision, code in candidates.items():
                    if collision not in result or code.cost < result[collision].cost:
                        result[collision] = code
        self._frontier_cache[key] = result
        return result

    def collision_cut(self, state, depth, budget):
        candidates = [tree for collision, tree in self.frontier(state, depth).items()
                      if collision <= budget]
        assert candidates, "Budget is below singleton frontier collision"
        return min(candidates, key=lambda tree: tree.cost)


def exhaustive_policies(search, state, depth, bound):
    """Bounded independent Cartesian enumeration, validation only."""
    if state.bit_count() <= bound:
        return [BACK.Tree(state)]
    policies = [cut_at_size(search.instance, search.instance.greedy(state), bound)]
    if depth:
        for original in search.macros(state):
            macro = cut_at_size(search.instance, original, bound)
            exits = leaves(macro)
            descendants = [exhaustive_policies(search, leaf.state, depth-1, bound) for leaf in exits]
            for children in product(*descendants):
                policies.append(graft(search.instance, macro,
                                      {leaf.state: child for leaf, child in zip(exits, children)}))
    return policies


def all_prunings(instance, tree):
    if tree.test < 0:
        return [tree]
    result = [BACK.Tree(tree.state)]
    for left, right in product(all_prunings(instance, tree.left), all_prunings(instance, tree.right)):
        result.append(instance.branch(tree.state, tree.test, left, right))
    return result


def main():
    rng = random.Random(2026101919)
    mass_cases = frontier_cases = full_policies = 0
    for n in range(2, 7):
        for _ in range(3):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests += [1 << h for h in range(n)]
            instance = BACK.Instance(n, tests)
            search = MenuSearch(instance, band_menu)
            for bound in {1, max(1, n//2)}:
                candidate = search.cut(instance.full, 2, bound)
                actual = exhaustive_policies(search, instance.full, 2, bound)
                assert candidate.cost == min(tree.cost for tree in actual)
                assert max(leaf.state.bit_count() for leaf in leaves(candidate)) <= bound
                validate(instance, candidate)
                mass_cases += 1
                full_policies += len(actual)
            # The depth-zero frontier is independently checked against ALL
            # literal stopping prefixes of the supplied greedy tree.
            exhaustive = {}
            for tree in all_prunings(instance, instance.greedy(instance.full)):
                collision = sum(leaf.state.bit_count()**2 for leaf in leaves(tree))
                exhaustive[collision] = min(exhaustive.get(collision, tree.cost), tree.cost)
            actual = search.frontier(instance.full, 0)
            assert {q: tree.cost for q, tree in actual.items()} == exhaustive
            # Further menu levels preserve the valid actual moment/work map.
            for collision, tree in search.frontier(instance.full, 2).items():
                assert collision == sum(leaf.state.bit_count()**2 for leaf in leaves(tree))
                validate(instance, tree)
                frontier_cases += 1

    # Long macro with n exits: the occurrence count is still bounded by the
    # hypothesis-mass argument, not by n^depth.
    instance = BACK.Instance(12, [1 << h for h in range(12)])
    def macro_menu(inst, state):
        return inst.greedy(state), band_menu(inst, state)[0]
    search = MenuSearch(instance, macro_menu)
    occurrences = [instance.full]
    levels = []
    for level in range(5):
        mass = sum(state.bit_count() for state in occurrences)
        assert len(occurrences) <= mass <= instance.n*2**level
        levels.append({"level": level, "occurrences": len(occurrences), "summed_population": mass,
                       "upper_bound": instance.n*2**level})
        occurrences = [leaf.state for state in occurrences if state.bit_count() > 1
                       for macro in search.macros(state) for leaf in leaves(macro)]
    cut = search.cut(instance.full, 4, 3)
    moment = search.collision_cut(instance.full, 2, 36)
    validate(instance, cut)
    validate(instance, moment)
    output = {"status": "passed", "mass_cut_comparisons": mass_cases,
              "exhaustively_enumerated_small_full_policies": full_policies,
              "actual_collision_frontiers_checked": frontier_cases,
              "long_macro_occurrence_levels": levels,
              "long_macro_cut_cost": cut.cost, "long_macro_collision_cut_cost": moment.cost,
              "no_unrestricted_optimum_oracle": True,
              "no_unrestricted_approximation_claim": True}
    Path(__file__).with_name("research-general-branching-partition-results.json").write_text(
        json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
