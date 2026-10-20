"""Polynomial target-aware pricing generators and small exact audits.

Imports the team's existing explicit-tree synthesis primitives. Exact global
optimization is used only by the finite audit, never by candidate generation.
"""

from functools import lru_cache
from itertools import combinations, permutations
from pathlib import Path
import importlib.util
import json
import random
import sys


def load_base():
    path = Path(__file__).with_name("research-general-algorithm-next.py")
    spec = importlib.util.spec_from_file_location("pricing_oracle_base", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BASE = load_base()
Instance, Tree, tree_nodes = BASE.Instance, BASE.Tree, BASE.tree_nodes


def depth_weights(tree):
    answer = {}
    def visit(node, depth):
        if node.test < 0:
            answer[node.state] = depth
        else:
            visit(node.left, depth + 1)
            visit(node.right, depth + 1)
    visit(tree, 0)
    return answer


def incident_template(instance, targets, weights, state=None):
    """Target-incident pair greedy; fill zero-target exits with ordinary greedy.

    Positive target weights are keyed by singleton bit masks. The gain is
    target reward times eliminated competitor count, including competitors
    outside the target region. No invented membership test is used.
    """
    root = instance.full if state is None else state

    @lru_cache(None)
    def mass(state):
        return sum(weight for bit, weight in weights.items() if state & bit & targets)

    @lru_cache(None)
    def build(state):
        if state.bit_count() <= 1 or not (state & targets):
            return instance.greedy(state)
        total = mass(state)
        options = []
        for j, test in enumerate(instance.tests):
            hit = state & test
            miss = state ^ hit
            if not hit or not miss:
                continue
            gain = state.bit_count() * total - hit.bit_count() * mass(hit) - miss.bit_count() * mass(miss)
            options.append((-gain, j))
        _, chosen = min(options)
        hit = state & instance.tests[chosen]
        return instance.branch(state, chosen, build(hit), build(state ^ hit))
    return build(root)


def verifier_paths(instance):
    answer = {}
    for h in range(instance.n):
        bit = 1 << h
        state, sequence = instance.full, []
        while state.bit_count() > 1:
            options = []
            for j, test in enumerate(instance.tests):
                hit = state & test
                miss = state ^ hit
                if hit and miss:
                    options.append(((hit if hit & bit else miss).bit_count(), j))
            _, chosen = min(options)
            sequence.append(chosen)
            hit = state & instance.tests[chosen]
            state = hit if hit & bit else state ^ hit
        answer[h] = tuple(sequence)
    return answer


def coalition_policy(instance, coalition, paths):
    """Execute full-instance verification paths only on the target's frontier cell."""
    policy = Tree(instance.full)

    def verify(state, h, position):
        if state.bit_count() <= 1:
            return Tree(state)
        bit = 1 << h
        while True:
            query = paths[h][position]
            position += 1
            hit = state & instance.tests[query]
            miss = state ^ hit
            if hit and miss:
                break
        if hit & bit:
            return instance.branch(state, query, verify(hit, h, position), Tree(miss))
        return instance.branch(state, query, Tree(hit), verify(miss, h, position))

    def add_target(node, h):
        if not node.state & (1 << h) or node.state.bit_count() <= 1:
            return node
        if node.test < 0:
            return verify(node.state, h, 0)
        return instance.branch(node.state, node.test,
                               add_target(node.left, h), add_target(node.right, h))

    for h in coalition:
        policy = add_target(policy, h)
    return policy


def fill_template(instance, policy):
    if policy.test < 0:
        return instance.greedy(policy.state)
    return instance.branch(policy.state, policy.test,
                           fill_template(instance, policy.left),
                           fill_template(instance, policy.right))


def identified(policy):
    return sum(node.state for node in tree_nodes(policy)
               if node.test < 0 and node.state.bit_count() == 1)


def generated_templates(instance, incumbent, coalition_width=2,
                        include_incident=True, include_coalitions=True):
    weights = depth_weights(incumbent)
    if include_incident:
        targets = {instance.full}
        targets.update(node.state for node in tree_nodes(incumbent))
        for test in instance.tests:
            targets.update((test, instance.full ^ test))
        for threshold in set(weights.values()):
            targets.add(sum(bit for bit, weight in weights.items() if weight >= threshold))
        for region in sorted(targets):
            if region:
                yield incident_template(instance, region, weights)
    if include_coalitions:
        paths = verifier_paths(instance)
        for size in range(1, coalition_width + 1):
            for group in combinations(range(instance.n), size):
                for order in permutations(group):
                    yield fill_template(instance, coalition_policy(instance, order, paths))


def represented_family(instance, incumbent, coalition_width=2,
                       include_incident=True, include_coalitions=True):
    family = {0}
    for node in tree_nodes(incumbent):
        family.add(node.state)
    for template in generated_templates(instance, incumbent, coalition_width,
                                        include_incident, include_coalitions):
        family.update(node.state for node in tree_nodes(template))
    # Retain the baseline's forced-root fresh conditional greedy templates.
    for node in tree_nodes(incumbent):
        if node.state.bit_count() <= 1:
            continue
        for test in instance.tests:
            hit = node.state & test
            miss = node.state ^ hit
            if hit and miss:
                for child in (hit, miss):
                    family.update(item.state for item in tree_nodes(instance.greedy(child)))
    base_count = len(family)
    base_items = tuple(family)
    for j, a in enumerate(base_items):
        family.update(a & b for b in base_items[j + 1:])
    return family, base_count


def exact_density(instance, family, incumbent, weights):
    """Exact weighted density in the finite represented-state policy DAG.

    Fractional Dinkelbach steps strictly decrease a ratio of two bounded
    integers. Prizes <=n-1 make the iteration bound fixed polynomial.
    """
    from fractions import Fraction
    best = incumbent
    density = Fraction(incumbent.cost, sum(weights.values()))
    limit = (instance.n * (instance.n - 1) + 1) ** 2
    for iteration in range(limit):
        values, choices, works, rewards = {0: Fraction(0)}, {}, {0: 0}, {0: 0}
        for state in sorted(family, key=int.bit_count):
            if state.bit_count() <= 1:
                reward = weights.get(state, 0)
                values[state], works[state], rewards[state] = density * reward, 0, reward
                continue
            value, choice, work, reward = Fraction(0), -1, 0, 0
            for query, test in enumerate(instance.tests):
                hit, miss = state & test, state & (instance.full ^ test)
                if not hit or not miss or hit not in values or miss not in values:
                    continue
                candidate = values[hit] + values[miss] - state.bit_count()
                if candidate > value:
                    value, choice = candidate, query
                    work = state.bit_count() + works[hit] + works[miss]
                    reward = rewards[hit] + rewards[miss]
            values[state], choices[state], works[state], rewards[state] = value, choice, work, reward
        if values[instance.full] <= 0:
            return best, density, iteration + 1

        def rebuild(state):
            if state.bit_count() <= 1 or choices[state] < 0:
                return Tree(state)
            query = choices[state]
            hit = state & instance.tests[query]
            return instance.branch(state, query, rebuild(hit), rebuild(state ^ hit))

        best = rebuild(instance.full)
        new_density = Fraction(works[instance.full], rewards[instance.full])
        assert new_density < density
        assert best.cost == works[instance.full]
        density = new_density
    raise AssertionError("Bounded rational density descent failed")


def candidate_pass(instance, incumbent, coalition_width=2,
                   include_incident=True, include_coalitions=True):
    family, base_count = represented_family(instance, incumbent, coalition_width,
                                             include_incident, include_coalitions)
    candidate, profit = instance.profit_fragment(family, incumbent)
    return candidate, {"old_cost": incumbent.cost, "new_cost": candidate.cost,
                       "profit": profit, "base_states": base_count,
                       "represented_states": len(family)}


def synthesize(instance, incumbent=None, coalition_width=2,
               include_incident=True, include_coalitions=True):
    incumbent = incumbent or instance.greedy(instance.full)
    history = []
    for _ in range(instance.n * (instance.n - 1) + 1):
        candidate, record = candidate_pass(instance, incumbent, coalition_width,
                                            include_incident, include_coalitions)
        history.append(record)
        if record["profit"] == 0:
            assert candidate.cost == incumbent.cost
            return incumbent, history
        assert candidate.cost < incumbent.cost
        incumbent = candidate
    raise AssertionError("Integer descent failed")


def small_audit(seed=20261018, cases=40):
    rng = random.Random(seed)
    checked = 0
    for _ in range(cases):
        n = rng.randrange(3, 9)
        tests = [1 << h for h in range(n)]
        tests += [rng.randrange(1, (1 << n) - 1) for _ in range(rng.randrange(2, 7))]
        instance = Instance(n, tests)
        paths = verifier_paths(instance)

        @lru_cache(None)
        def target_optimum(state, targets):
            if not targets or state.bit_count() <= 1:
                return 0
            return state.bit_count() + min(
                target_optimum(hit, targets & hit) + target_optimum(state ^ hit, targets & (state ^ hit))
                for test in instance.tests if (hit := state & test) and hit != state)

        for size in (1, 2):
            for coalition in combinations(range(n), size):
                target_bits = sum(1 << h for h in coalition)
                policy = coalition_policy(instance, coalition, paths)
                assert identified(policy) & target_bits == target_bits
                optimum = target_optimum(instance.full, target_bits)
                assert policy.cost <= 4 * size * optimum + 3 * size
                checked += 1
        weights = depth_weights(instance.greedy(instance.full))
        for targets in (instance.full, tests[0], instance.full ^ tests[0]):
            code = incident_template(instance, targets, weights)
            assert identified(code) == instance.full
        if n <= 6:
            incumbent = instance.greedy(instance.full)
            family, _ = represented_family(instance, incumbent)
            policy, density, _ = exact_density(instance, family, incumbent, weights)

            @lru_cache(None)
            def exhaustive(state):
                if state.bit_count() <= 1:
                    return {state: 0}
                answer = {0: 0}
                for test in instance.tests:
                    hit, miss = state & test, state & (instance.full ^ test)
                    if not hit or not miss or hit not in family or miss not in family:
                        continue
                    for a, aw in exhaustive(hit).items():
                        for b, bw in exhaustive(miss).items():
                            covered = a | b
                            cost = state.bit_count() + aw + bw
                            answer[covered] = min(answer.get(covered, cost), cost)
                return answer

            from fractions import Fraction
            reference = min(Fraction(work, sum(weight for bit, weight in weights.items()
                                               if covered & bit))
                            for covered, work in exhaustive(instance.full).items() if covered)
            assert density == reference
            reward = sum(weight for bit, weight in weights.items() if identified(policy) & bit)
            assert Fraction(policy.cost, reward) == density
    return checked


def known_witnesses():
    return [
        (12, [96, 1042, 129, 8, 2748, 3264, 3840]),
        (12, [3264, 700, 1153, 8, 1042, 97, 3840, 1022]),
        (18, [536, 203199, 44160, 88107, 228858, 41456, 514, 206464, 261742]),
        (18, [592, 211391, 44160, 88107, 228858, 33264, 514, 206464, 259695, 9772]),
    ]


if __name__ == "__main__":
    print(f"PASS: {small_audit()} constant-coalition target-cost comparisons")
    results = []
    for n, tests in known_witnesses():
        instance = Instance(n, tests)
        baseline, old_history = instance.synthesize(verification_templates=True)
        coalition_only, coalition_history = synthesize(instance, baseline, include_incident=False)
        incident_only, incident_history = synthesize(instance, baseline, include_coalitions=False)
        combined, combined_history = synthesize(instance, baseline)
        record = {"n": n, "tests": tests, "greedy": instance.greedy(instance.full).cost,
                  "baseline": baseline.cost, "exact_optimum": instance.exact_cost(),
                  "coalition2": coalition_only.cost, "incident": incident_only.cost,
                  "combined": combined.cost,
                  "coalition_history": coalition_history, "incident_history": incident_history,
                  "combined_history": combined_history}
        results.append(record)
        print(json.dumps(record))
    output = Path(__file__).with_name("research-general-pricing-oracle-results.json")
    output.write_text(json.dumps({"witnesses": results}, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {output.name}")
