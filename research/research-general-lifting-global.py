"""Exact executable pricing over one supplied logarithmic query palette.

Public integration API:
    optimize_palette(instance, incumbent, tuple_of_test_indices)
        -> (actual_complete_tree, stats)
    price_palette(instance, tuple_of_test_indices, weights, work_price=1,
                  ambient=None)
        -> (actual_partial_tree, stats)

Weights are a mapping from SINGLETON BIT MASKS to rational prizes, or a
sequence indexed by hypothesis number.  All trees use the existing binary
duck-type fields state/test/left/right/cost and instance.branch().
"""

from fractions import Fraction


class PartialTree:
    def __init__(self, state, test=-1, left=None, right=None, cost=0):
        self.state, self.test, self.left, self.right, self.cost = state, test, left, right, cost


def _palette_closure(instance, ambient, palette):
    palette = tuple(dict.fromkeys(palette))
    if any(q < 0 or q >= len(instance.tests) for q in palette):
        raise ValueError("A palette index is outside the supplied test list")
    seen, pending, splits = {ambient}, [ambient], {}
    while pending:
        state = pending.pop()
        options = []
        if state.bit_count() > 1:
            for q in palette:
                hit = state & instance.tests[q]
                miss = state ^ hit
                if hit and miss:
                    options.append((q, hit, miss))
                    for child in (hit, miss):
                        if child not in seen:
                            seen.add(child)
                            pending.append(child)
        splits[state] = options
    return palette, sorted(seen, key=int.bit_count), splits


def _restricted_cost(instance, tree, selected):
    total, pending = 0, [(tree, selected)]
    while pending:
        node, state = pending.pop()
        if state.bit_count() <= 1:
            continue
        if node.test < 0:
            raise ValueError("Incumbent must identify every ambient hypothesis")
        hit = state & instance.tests[node.test]
        miss = state ^ hit
        if hit and miss:
            total += state.bit_count()
            pending.extend(((node.left, hit), (node.right, miss)))
        elif hit:
            pending.append((node.left, hit))
        else:
            pending.append((node.right, miss))
    return total


def _prune(instance, tree, selected):
    """Iterative actual restriction; robust to a deep incumbent comb."""
    leaf_type = type(tree)
    result, pending = {}, [(tree, selected, False)]
    while pending:
        node, state, expanded = pending.pop()
        key = id(node), state
        if state.bit_count() <= 1:
            result[key] = leaf_type(state)
            continue
        if node.test < 0:
            raise ValueError("Incumbent must identify every ambient hypothesis")
        hit = state & instance.tests[node.test]
        miss = state ^ hit
        if not expanded:
            pending.append((node, state, True))
            if hit:
                pending.append((node.left, hit, False))
            if miss:
                pending.append((node.right, miss, False))
        elif hit and miss:
            result[key] = instance.branch(state, node.test,
                                          result[id(node.left), hit], result[id(node.right), miss])
        elif hit:
            result[key] = result[id(node.left), hit]
        else:
            result[key] = result[id(node.right), miss]
    return result[id(tree), selected]


def optimize_palette(instance, incumbent, palette):
    """Optimal palette-prefix policy with actual incumbent restrictions at exits.

    Every possible order/adaptive use of palette tests is considered.  Queries
    outside the palette are used only inside a terminal incumbent restriction.
    For d palette tests there are at most 3**d distinct nonempty contexts.
    """
    ambient = incumbent.state
    palette, states, splits = _palette_closure(instance, ambient, palette)
    values, actions = {}, {}
    for state in states:
        best = _restricted_cost(instance, incumbent, state)
        action = None
        for q, hit, miss in splits[state]:
            candidate = state.bit_count() + values[hit] + values[miss]
            if candidate < best:
                best, action = candidate, (q, hit, miss)
        values[state], actions[state] = best, action

    built, pending = {}, [(ambient, False)]
    prefix_work = fallback_cells = 0
    while pending:
        state, expanded = pending.pop()
        action = actions[state]
        if action is None:
            built[state] = _prune(instance, incumbent, state)
            fallback_cells += 1
        elif not expanded:
            q, hit, miss = action
            prefix_work += state.bit_count()
            pending.extend(((state, True), (hit, False), (miss, False)))
        else:
            q, hit, miss = action
            built[state] = instance.branch(state, q, built[hit], built[miss])
    actual = built[ambient]
    assert actual.cost == values[ambient]
    incumbent_cost = _restricted_cost(instance, incumbent, ambient)
    assert actual.cost <= incumbent_cost
    return actual, {"palette_size": len(palette), "reachable_states": len(states),
                    "incumbent_cost": incumbent_cost, "result_cost": actual.cost,
                    "raw_gain": incumbent_cost - actual.cost,
                    "palette_prefix_work": prefix_work, "fallback_cells": fallback_cells}


def _weight(weights, singleton):
    if hasattr(weights, "get"):
        return weights.get(singleton, 0)
    return weights[singleton.bit_length() - 1]


def binary_coding_cost(size):
    """Unrestricted optimal binary external path length on size equal leaves."""
    if size <= 1:
        return 0
    depth = (size - 1).bit_length()
    return size * (depth + 1) - (1 << depth)


def price_palette_stage(instance, incumbent, palette, gamma=Fraction(1, 2), coding_price=1,
                        state_potential=None):
    """Exact max gamma*actual_credit + coding_price*coding_drop - work.

    This is an executable partial stage.  Its two credits must be telescoped
    over actual recursive cells; they are not independent completion prices.
    An optional state_potential(S) replaces the unrestricted binary coding
    profile.  Its signed drop is retained exactly, including negative drops.
    The caller supplies its lower-bound proof; this optimizer only evaluates it.
    """
    gamma, coding_price = Fraction(gamma), Fraction(coding_price)
    if gamma < 0 or coding_price < 0:
        raise ValueError("Stage prices must be nonnegative")
    ambient = incumbent.state
    palette, states, splits = _palette_closure(instance, ambient, palette)
    old_cost = {state: _restricted_cost(instance, incumbent, state) for state in states}
    potential = ({state: binary_coding_cost(state.bit_count()) for state in states}
                 if state_potential is None else
                 {state: Fraction(state_potential(state)) for state in states})
    energy = {state: gamma * old_cost[state] + coding_price * potential[state]
              for state in states}
    values, actions = {}, {}
    for state in states:
        best, action = energy[state], None
        for q, hit, miss in splits[state]:
            candidate = state.bit_count() + values[hit] + values[miss]
            if candidate < best:
                best, action = candidate, (q, hit, miss)
        values[state], actions[state] = best, action
    built, pending, exits = {}, [(ambient, False)], []
    while pending:
        state, expanded = pending.pop()
        action = actions[state]
        if action is None:
            built[state] = type(incumbent)(state)
            exits.append(state)
        elif not expanded:
            q, hit, miss = action
            pending.extend(((state, True), (hit, False), (miss, False)))
        else:
            q, hit, miss = action
            built[state] = instance.branch(state, q, built[hit], built[miss])
    actual = built[ambient]
    credit = old_cost[ambient] - sum(old_cost[state] for state in exits)
    coding_drop = potential[ambient] - sum(potential[state] for state in exits)
    profit = gamma * credit + coding_price * coding_drop - actual.cost
    assert profit == energy[ambient] - values[ambient]
    return actual, {"palette_size": len(palette), "reachable_states": len(states),
                    "work": actual.cost, "actual_credit": credit, "coding_drop": coding_drop,
                    "profit": profit, "output_cells": len(exits),
                    "gamma": gamma, "coding_price": coding_price}


def price_palette(instance, palette, weights, work_price=1, ambient=None):
    """Exact maximum completed-prize minus work_price * work on a palette."""
    ambient = instance.full if ambient is None else ambient
    palette, states, splits = _palette_closure(instance, ambient, palette)
    work_price = Fraction(work_price)
    if work_price < 0:
        raise ValueError("Work price must be nonnegative")
    values, actions = {}, {}
    for state in states:
        best = Fraction(_weight(weights, state)) if state.bit_count() == 1 else Fraction(0)
        action = None
        for q, hit, miss in splits[state]:
            candidate = values[hit] + values[miss] - work_price * state.bit_count()
            if candidate > best:
                best, action = candidate, (q, hit, miss)
        values[state], actions[state] = best, action
    built, pending = {}, [(ambient, False)]
    reward, completed = Fraction(0), 0
    while pending:
        state, expanded = pending.pop()
        action = actions[state]
        if action is None:
            built[state] = PartialTree(state)
            if state.bit_count() == 1:
                reward += _weight(weights, state)
                completed += 1
        elif not expanded:
            q, hit, miss = action
            pending.extend(((state, True), (hit, False), (miss, False)))
        else:
            q, hit, miss = action
            built[state] = instance.branch(state, q, built[hit], built[miss])
    actual = built[ambient]
    assert reward - work_price * actual.cost == values[ambient]
    return actual, {"palette_size": len(palette), "reachable_states": len(states),
                    "work": actual.cost, "completed": completed,
                    "reward": reward, "profit": values[ambient], "work_price": work_price}


def _load_library():
    import importlib.util
    import sys
    spec = importlib.util.spec_from_file_location("lifting_global_test_backend", "research-general-algorithm-next.py")
    library = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = library
    spec.loader.exec_module(library)
    return library


def _template_profiles(instance, code, state, weights):
    if code.test < 0:
        return {0: 0, _weight(weights, state): 0} if state.bit_count() == 1 else {0: 0}
    hit = state & instance.tests[code.test]
    left = _template_profiles(instance, code.left, hit, weights)
    right = _template_profiles(instance, code.right, state ^ hit, weights)
    answer = {0: 0}
    for a, ca in left.items():
        for b, cb in right.items():
            prize, work = a + b, state.bit_count() + ca + cb
            if prize and (prize not in answer or work < answer[prize]):
                answer[prize] = work
    return answer


def main():
    from functools import lru_cache
    import random
    library = _load_library()
    rng = random.Random(20261018)
    complete_checks = partial_checks = stage_checks = 0

    def execute(instance, tree):
        total, completed = 0, 0
        for h in range(instance.n):
            if not tree.state >> h & 1:
                continue
            node, depth = tree, 0
            while node.test >= 0:
                assert node.state >> h & 1
                node = node.left if instance.tests[node.test] >> h & 1 else node.right
                depth += 1
            assert node.state >> h & 1
            total += depth
            if node.state.bit_count() == 1:
                completed |= node.state
        assert total == tree.cost
        return completed

    for n in range(2, 10):
        for _ in range(18):
            tests = [rng.randrange(1, (1 << n) - 1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if (h >> bit) & 1)
                      for bit in range((n - 1).bit_length())]
            instance = library.Instance(n, tests)
            incumbent = instance.greedy(instance.full)
            palette = tuple(rng.sample(range(len(instance.tests)), rng.randrange(min(4, len(instance.tests)) + 1)))
            weights = {1 << h: rng.randrange(1, n) for h in range(n)}
            price = Fraction(rng.randrange(1, 8), rng.randrange(1, 8))

            @lru_cache(None)
            def brute(state):
                options = []
                for q in palette:
                    hit = state & instance.tests[q]
                    if hit and hit != state:
                        options.append((hit, state ^ hit))
                cost = _restricted_cost(instance, incumbent, state)
                profit = Fraction(weights[state]) if state.bit_count() == 1 else Fraction(0)
                for hit, miss in options:
                    left, right = brute(hit), brute(miss)
                    cost = min(cost, state.bit_count() + left[0] + right[0])
                    profit = max(profit, left[1] + right[1] - price * state.bit_count())
                return cost, profit

            actual, stats = optimize_palette(instance, incumbent, palette)
            partial, pstats = price_palette(instance, palette, weights, price)
            stage, sstats = price_palette_stage(instance, incumbent, palette)
            assert actual.cost == brute(instance.full)[0]
            assert pstats["profit"] == brute(instance.full)[1]
            assert stats["reachable_states"] <= 3 ** len(palette)
            assert execute(instance, actual) == instance.full
            finished = execute(instance, partial)
            actual_reward = sum(weights[1 << h] for h in range(n) if finished >> h & 1)
            assert actual_reward == pstats["reward"]
            execute(instance, stage)
            stage_checks += 1
            complete_checks += 1
            partial_checks += 1

    examples = []
    for dimension in range(3, 8):
        core_n, u = 1 << dimension, 1 << (2 * dimension)
        n = core_n + u
        tests = [sum(1 << h for h in range(core_n) if (h >> bit) & 1)
                 for bit in range(dimension)]
        instance = library.Instance(n, tests)
        valuable = 1 << (dimension - 1)
        weights = {1 << h: (u + dimension if h in (0, valuable) else dimension)
                   for h in range(core_n)}
        weights.update({1 << h: dimension - 1 + (h - core_n + 1) for h in range(core_n, n)})

        def core_code(state, depth):
            if state.bit_count() == 1:
                return library.Tree(state)
            hit = state & tests[depth]
            return instance.branch(state, depth, core_code(hit, depth + 1), core_code(state ^ hit, depth + 1))
        code = core_code((1 << core_n) - 1, 0)
        profiles = _template_profiles(instance, code, instance.full, weights)
        template_density = min(Fraction(work, prize) for prize, work in profiles.items() if prize)
        partial, pstats = price_palette(instance, tuple(range(dimension)), weights, Fraction(1, 2))
        assert pstats["profit"] > 0
        palette_density = Fraction(partial.cost, pstats["reward"])
        assert palette_density < 2
        bound = min(Fraction(u * dimension, u + (core_n - 1) * dimension),
                    Fraction(n, max(1, (core_n - 2) * dimension)))
        assert template_density >= bound
        examples.append((dimension, n, str(template_density), str(palette_density), pstats["reachable_states"]))

    noisy_examples = []
    for dimension in range(2, 10):
        n = 1 << dimension
        tests = [sum(1 << h for h in range(n) if (h >> bit) & 1)
                 for bit in range(dimension)]
        instance = library.Instance(n, tests)
        def coordinate_code(state, depth):
            if state.bit_count() <= 1:
                return library.Tree(state)
            red = state & tests[depth]
            return instance.branch(state, depth, coordinate_code(red, depth + 1), coordinate_code(state ^ red, depth + 1))
        tree = coordinate_code(instance.full, 0)
        noisy = tests[0] ^ 1 ^ 2
        assert noisy.bit_count() == n // 2
        credit = tree.cost - _restricted_cost(instance, tree, noisy) - _restricted_cost(instance, tree, instance.full ^ noisy)
        assert credit == 2 * dimension
        noisy_examples.append((n, credit, n))

    for size in range(2, 100):
        assert binary_coding_cost(size) >= 0
        for left in range(1, size):
            drop = binary_coding_cost(size) - binary_coding_cost(left) - binary_coding_cost(size - left)
            assert 0 <= drop <= size

    print("PASS exact complete palette/fallback comparisons:", complete_checks)
    print("PASS exact rational weighted palette pricing comparisons:", partial_checks)
    print("PASS actual executable mixed-stage identities:", stage_checks)
    print("Palette ordering gaps (D,n,fixed-template density,palette density,states):", examples)
    print("Noisy-coordinate restriction vs output entropy (n,actual credit,entropy):", noisy_examples)


if __name__ == "__main__":
    main()
