"""Independent literal enumeration audit of bounded-menu collision frontiers."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import importlib.util
import json
import random
import sys

spec = importlib.util.spec_from_file_location(
    "branching_search_audit_backend", Path(__file__).with_name("research-general-branching-partition.py"))
MOD = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = MOD
spec.loader.exec_module(MOD)


def literal_prunings(instance, node):
    result = [MOD.BACK.Tree(node.state)]
    if node.test >= 0:
        for left, right in product(literal_prunings(instance, node.left),
                                   literal_prunings(instance, node.right)):
            result.append(instance.branch(node.state, node.test, left, right))
    return tuple(result)


def literal_menu_policies(search, state, depth):
    @lru_cache(None)
    def build(current, remaining):
        policies = list(literal_prunings(search.instance, search.instance.greedy(current)))
        if remaining and current.bit_count() > 1:
            for macro in search.macros(current):
                exits = MOD.leaves(macro)
                child_menus = [build(leaf.state, remaining - 1) for leaf in exits]
                for children in product(*child_menus):
                    policies.append(MOD.graft(search.instance, macro,
                                              {leaf.state: child for leaf, child in zip(exits, children)}))
        return tuple(policies)
    return build(state, depth)


def run():
    rng = random.Random(202610191927)
    comparisons = policies_enumerated = actual_codes = 0
    for n in range(2, 7):
        for trial in range(2):
            tests = [1 << h for h in range(n)]
            tests += [rng.randrange(1, (1 << n) - 1) for _ in range(5)]
            instance = MOD.BACK.Instance(n, tests)
            def long_menu(inst, state):
                return inst.greedy(state), MOD.band_menu(inst, state)[0]
            for menu in (MOD.band_menu, long_menu):
                search = MOD.MenuSearch(instance, menu)
                for depth in range(3):
                    literal = literal_menu_policies(search, instance.full, depth)
                    expected = {}
                    for tree in literal:
                        collision = sum(leaf.state.bit_count() ** 2 for leaf in MOD.leaves(tree))
                        expected[collision] = min(expected.get(collision, tree.cost), tree.cost)
                    actual = search.frontier(instance.full, depth)
                    assert expected == {collision: tree.cost for collision, tree in actual.items()}
                    for collision, tree in actual.items():
                        assert collision == sum(leaf.state.bit_count() ** 2 for leaf in MOD.leaves(tree))
                        MOD.validate(instance, tree)
                        actual_codes += 1
                    comparisons += 1
                    policies_enumerated += len(literal)
    return {"status": "passed", "exact_frontier_comparisons": comparisons,
            "literal_policies_enumerated": policies_enumerated,
            "actual_frontier_codes_validated": actual_codes,
            "menu_types": ["two_one_query_macros", "full_greedy_plus_one_query"],
            "maximum_action_depth": 2,
            "maximum_hypotheses": 6,
            "unrestricted_optimum_not_used": True}


if __name__ == "__main__":
    result = run()
    Path(__file__).with_name("research-general-branching-search-audit-results.json").write_text(
        json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
