"""Polynomial response-factor contexts and adaptive whole-factor planning.

No optimum UDT oracle is used by the candidate algorithm. Exact local subset
DP is used only when its alphabet has at most floor(log2(n+m+1)) values.
The independent unrestricted subset solver in main() is validation only.
"""

from dataclasses import dataclass
from functools import lru_cache
from itertools import product
from pathlib import Path
import importlib.util
import json
import math
import random
import sys


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, Path(__file__).with_name(filename))
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


PRODUCT = load("factor_context_product", "research-general-product-decomposition.py")
BACK = load("factor_context_backend", "research-general-algorithm-next.py")


def singleton_bits(mask):
    while mask:
        bit = mask & -mask
        yield bit
        mask ^= bit


class ResponseFactors:
    def __init__(self, instance, retained):
        self.instance = instance
        # Complement/duplicate rows have the same information. Keep one actual
        # original test for each nonconstant unordered response partition.
        distinct = {}
        for q in retained:
            test = instance.tests[q]
            if test and test != instance.full:
                distinct.setdefault(min(test, instance.full ^ test), q)
        self.retained = tuple(distinct.values())
        words = tuple(sum(1 << j for j, q in enumerate(self.retained)
                          if instance.tests[q] >> h & 1) for h in range(instance.n))
        self.words = words
        unique = tuple(sorted(set(words)))
        if not self.retained:
            masks = ()
            self.oracle_calls = 0
        else:
            cuts = PRODUCT.EntropyCuts(unique, len(self.retained))
            masks, _ = cuts.factorize()
            self.oracle_calls = cuts.calls
        # Constant factors must be removed: the context-count bound assumes
        # every nontrivial factor alphabet is at least two.
        self.masks = tuple(mask for mask in masks if len({word & mask for word in unique}) > 1)
        values = [tuple(sorted({word & mask for word in unique})) for mask in self.masks]
        self.alphabets = tuple(len(v) for v in values)
        maps = [{value: i for i, value in enumerate(v)} for v in values]
        self.labels = tuple(tuple(index[word & mask] for index, mask in zip(maps, self.masks))
                            for word in words)
        assert math.prod(self.alphabets) == len(unique)
        assert set(self.labels) == set(product(*(range(size) for size in self.alphabets)))
        self.cells = tuple(tuple(sum(1 << h for h, label in enumerate(self.labels) if label[i] == v)
                                 for v in range(size)) for i, size in enumerate(self.alphabets))
        self.contexts = {}
        for context in product(*(range(-1, size) for size in self.alphabets)):
            state = instance.full
            for i, v in enumerate(context):
                if v >= 0:
                    state &= self.cells[i][v]
            assert state
            self.contexts[context] = state
        assert len(self.contexts) == math.prod(size+1 for size in self.alphabets)
        # Exact integer version of the loose N^(log_2 3) size bound: 1+a<=a^2.
        assert len(self.contexts) <= len(unique)**2
        self.quotient_size = len(unique)
        self.nonuniform_residual_sizes = len({self.labels.count(label) for label in set(self.labels)}) > 1

    def conditioned(self, context, factor, value):
        child = list(context)
        assert child[factor] == -1
        child[factor] = value
        return tuple(child)


def factor_decoder(instance, factors, context, factor, exact_limit, retained_fallback=False,
                   state_pool=None):
    """Decode one factor with actual tests depending only on that factor here."""
    ambient = factors.contexts[context]
    cells = tuple(ambient & cell for cell in factors.cells[factor])
    assert all(cells)
    size, full = len(cells), (1 << len(cells))-1
    weights = tuple(cell.bit_count() for cell in cells)
    options = []
    for q, test in enumerate(instance.tests):
        local = inconsistent = 0
        for value, cell in enumerate(cells):
            hit = cell & test
            if hit and hit != cell:
                inconsistent |= 1 << value
            elif hit:
                local |= 1 << value
        # A presently inconsistent query may become eligible after all its
        # inconsistent factor values have been excluded. Keep that option.
        if local and local | inconsistent != full:
            options.append((local, inconsistent, q))
    static = [local for local, inconsistent, _ in options if not inconsistent]
    assert len({tuple(bool(test >> v & 1) for test in static) for v in range(size)}) == size

    @lru_cache(None)
    def mass(selected):
        return sum(weights[bit.bit_length()-1] for bit in singleton_bits(selected))

    @lru_cache(None)
    def mask(selected):
        return sum(cells[bit.bit_length()-1] for bit in singleton_bits(selected))

    actions = {}

    @lru_cache(None)
    def solve(selected):
        if selected.bit_count() <= 1:
            return 0
        proper = [(local, q) for local, inconsistent, q in options
                  if not selected & inconsistent and selected & local and selected & ~local]
        if size > exact_limit:
            local, q = min(proper, key=lambda item: (
                max(mass(selected & item[0]), mass(selected & ~item[0])), item[1]))
            best = solve(selected & local)+solve(selected & ~local)
        else:
            best, q, local = min((solve(selected & local)+solve(selected & ~local), q, local)
                                 for local, q in proper)
        actions[selected] = q, local
        return mass(selected)+best

    cost = solve(full)

    def build(selected):
        state = mask(selected)
        if selected.bit_count() <= 1:
            return BACK.Tree(state)
        q, local = actions[selected]
        return instance.branch(state, q, build(selected & local), build(selected & ~local))

    tree = build(full)
    assert tree.cost == cost
    if state_pool is not None:
        state_pool.update(node.state for node in BACK.tree_nodes(tree))
    retained_work = None
    used_retained = False
    if retained_fallback:
        # The original retained rows belonging to this factor identify it
        # regardless of quotient multiplicities. Their sequential code has
        # height at most the number of those rows, a useful separate bound.
        owner = [q for position, q in enumerate(factors.retained)
                 if factors.masks[factor] >> position & 1]
        local_rows = {q: local for local, bad, q in options if not bad}
        assert owner and all(q in local_rows for q in owner)

        def sequential(selected, start=0):
            state = mask(selected)
            if selected.bit_count() <= 1:
                return BACK.Tree(state)
            for position in range(start, len(owner)):
                q, local = owner[position], local_rows[owner[position]]
                hit = selected & local
                if hit and hit != selected:
                    return instance.branch(state, q, sequential(hit, position+1),
                                           sequential(selected ^ hit, position+1))
            raise AssertionError("Retained factor rows failed to identify its value")

        supplied = sequential(full)
        if state_pool is not None:
            state_pool.update(node.state for node in BACK.tree_nodes(supplied))
        retained_work = supplied.cost
        assert retained_work <= mass(full)*len(owner)
        if supplied.cost < tree.cost:
            tree, used_retained = supplied, True
    return tree, {"alphabet": size, "admissible_queries": len(options),
                  "queries_with_conditional_eligibility": sum(bool(bad) for _, bad, _ in options),
                  "local_DP": size <= exact_limit, "local_states_evaluated": solve.cache_info().currsize,
                  "retained_row_code_work": retained_work, "used_retained_row_code": used_retained}


def plan_factors(instance, factors, exact_limit=None, retained_fallback=False):
    """Choose factor order adaptively, with actual fresh greedy at any exit."""
    if exact_limit is None:
        exact_limit = (instance.n+len(instance.tests)+1).bit_length()-1
    # Keep the public runtime guarantee even if a caller supplies a large limit.
    exact_limit = min(exact_limit, (instance.n+len(instance.tests)+1).bit_length()-1)
    values, actions = {}, {}
    pool = set(factors.contexts.values()) | {0}
    local_calls = local_exact = 0
    for context, state in sorted(factors.contexts.items(), key=lambda item: item[1].bit_count()):
        greedy = instance.greedy(state)
        best, action = greedy.cost, ("fallback", greedy)
        pool.update(node.state for node in BACK.tree_nodes(greedy))
        for factor, value in enumerate(context):
            if value >= 0:
                continue
            decoder, stats = factor_decoder(instance, factors, context, factor, exact_limit,
                                             retained_fallback=retained_fallback, state_pool=pool)
            children = [factors.conditioned(context, factor, v) for v in range(factors.alphabets[factor])]
            candidate = decoder.cost+sum(values[child] for child in children)
            pool.update(node.state for node in BACK.tree_nodes(decoder))
            local_calls += 1
            local_exact += stats["local_DP"]
            if candidate < best:
                best, action = candidate, ("factor", factor, decoder)
        values[context], actions[context] = best, action

    def reconstruct(context):
        action = actions[context]
        if action[0] == "fallback":
            return action[1]
        _, factor, decoder = action
        continuation = {factors.contexts[factors.conditioned(context, factor, v)]:
                        reconstruct(factors.conditioned(context, factor, v))
                        for v in range(factors.alphabets[factor])}

        def fill(node):
            if node.test < 0:
                return continuation[node.state]
            return instance.branch(node.state, node.test, fill(node.left), fill(node.right))
        return fill(decoder)

    root = (-1,)*len(factors.alphabets)
    tree = reconstruct(root)
    assert tree.cost == values[root] <= instance.greedy(instance.full).cost
    return tree, pool, {"factors": len(factors.alphabets), "alphabets": factors.alphabets,
                        "quotient_size": factors.quotient_size, "contexts": len(factors.contexts),
                        "local_decoders": local_calls, "exact_local_decoders": local_exact,
                        "nonuniform_residual_sizes": factors.nonuniform_residual_sizes,
                        "cost": tree.cost, "retained_distinct_tests": len(factors.retained),
                        "retained_row_fallback": retained_fallback}


def factor_context_pass(instance, thresholds=None):
    if thresholds is None:
        thresholds = sorted({min(test.bit_count(), instance.n-test.bit_count())
                             for test in instance.tests if test and test != instance.full})
    best = instance.greedy(instance.full)
    pool, history = {node.state for node in BACK.tree_nodes(best)} | {0}, []
    for threshold in thresholds:
        retained = tuple(q for q, test in enumerate(instance.tests)
                         if min(test.bit_count(), instance.n-test.bit_count()) >= threshold)
        factors = ResponseFactors(instance, retained)
        candidate, states, stats = plan_factors(instance, factors)
        stats["threshold"] = threshold
        history.append(stats)
        pool.update(states)
        if candidate.cost < best.cost:
            best = candidate
    return best, pool, history


def execute(instance, tree):
    work, leaves = 0, set()
    for h in range(instance.n):
        bit, node = 1 << h, tree
        while node.test >= 0:
            assert node.state & bit
            node = node.left if instance.tests[node.test] & bit else node.right
            work += 1
        assert node.state == bit
        leaves.add(bit)
    assert work == tree.cost and len(leaves) == instance.n


def independent_optimum(instance):
    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        return state.bit_count()+min(solve(state & test)+solve(state & ~test)
                                     for test in instance.tests if state & test and state & ~test)
    return solve(instance.full)


def main():
    rng = random.Random(2026101903)
    cases, context_count, nonuniform_count = 0, 0, 0
    for n in range(2, 10):
        for _ in range(5):
            tests = [rng.randrange(1, (1 << n)-1) for _ in range(5)]
            tests += [sum(1 << h for h in range(n) if h >> bit & 1)
                      for bit in range((n-1).bit_length())]
            instance = BACK.Instance(n, tests)
            tree, pool, history = factor_context_pass(instance)
            execute(instance, tree)
            assert independent_optimum(instance) <= tree.cost <= instance.greedy(instance.full).cost
            assert all(node.state in pool for node in BACK.tree_nodes(tree))
            cases += 1
            context_count += sum(item["contexts"] for item in history)
            nonuniform_count += sum(item["nonuniform_residual_sizes"] for item in history)

    # Unequal residual multiplicities over a genuine 2x2 response support.
    labels = [(0, 0)]*1+[(0, 1)]*2+[(1, 0)]*3+[(1, 1)]*1
    tests = [sum(1 << h for h, label in enumerate(labels) if label[i]) for i in range(2)]
    tests += [1 << h for h in range(len(labels))]
    instance = BACK.Instance(len(labels), tests)
    factors = ResponseFactors(instance, (0, 1))
    assert factors.alphabets == (2, 2) and factors.nonuniform_residual_sizes
    tree, _, stats = plan_factors(instance, factors)
    execute(instance, tree)
    assert independent_optimum(instance) <= tree.cost

    # A query varying with the other factor only at A=0 becomes eligible once
    # A=0 is excluded. It then supplies a two-versus-two split of A=1,...,4.
    labels = tuple(product(range(5), range(2)))
    retained = [sum(1 << h for h, label in enumerate(labels) if label[0] == v) for v in range(5)]
    retained.append(sum(1 << h for h, label in enumerate(labels) if label[1]))
    extra = sum(1 << h for h, label in enumerate(labels)
                if label[0] in (1, 2) or label == (0, 0))
    instance = BACK.Instance(10, retained+[extra])
    factors = ResponseFactors(instance, tuple(range(len(retained))))
    factor = factors.alphabets.index(5)
    decoder, conditional_stats = factor_decoder(instance, factors, (-1, -1), factor, 4)
    assert decoder.cost == 26 < 28
    assert any(node.test == len(retained) for node in BACK.tree_nodes(decoder))

    # One balanced decoy leaves two one-hot four-point sets, making greedy
    # pay26 instead of the24 of the three original bit questions. A retained
    # zero-indicator couples their response support into ONE eight-value
    # factor; the optional listed-row fallback must take its better code.
    tests = [sum(1 << h for h in (0, 1, 2, 4))]
    tests += [sum(1 << h for h in range(8) if h >> bit & 1) for bit in range(3)]
    tests.append(1)
    listed_instance = BACK.Instance(8, tests)
    listed_factors = ResponseFactors(listed_instance, (1, 2, 3, 4))
    assert listed_factors.alphabets == (8,)
    ordinary, _ = factor_decoder(listed_instance, listed_factors, (-1,), 0, 0)
    listed_pool = set()
    listed_tree, listed_stats = factor_decoder(listed_instance, listed_factors, (-1,), 0, 0,
                                                retained_fallback=True, state_pool=listed_pool)
    assert ordinary.cost == 26 and listed_tree.cost == 24
    assert listed_stats["used_retained_row_code"]
    assert {node.state for node in BACK.tree_nodes(ordinary)} <= listed_pool
    assert {node.state for node in BACK.tree_nodes(listed_tree)} <= listed_pool
    execute(listed_instance, listed_tree)

    points = tuple(product(range(8), range(2)))
    product_tests = [sum(1 << h for h, point in enumerate(points) if test >> point[0] & 1)
                     for test in tests]
    product_tests.append(sum(1 << h for h, point in enumerate(points) if point[1]))
    pool_instance = BACK.Instance(16, product_tests)
    pool_factors = ResponseFactors(pool_instance, (1, 2, 3, 4, 5))
    assert sorted(pool_factors.alphabets) == [2, 8]
    old_plan, old_pool, _ = plan_factors(pool_instance, pool_factors)
    new_plan, new_pool, _ = plan_factors(pool_instance, pool_factors, retained_fallback=True)
    assert old_pool <= new_pool and new_plan.cost <= old_plan.cost
    execute(pool_instance, new_plan)

    # Automatically discovered private-selector coordinates, with reversed
    # original test order. The algorithm receives no selector/body role labels.
    replay = load("factor_context_replay_validation", "research-general-selector-replay.py")
    structured = []
    for selectors, bodies in (((3, 3), (2,)), ((4, 4), (2,)), ((4, 4), (3,)), ((6, 6), (4,))):
        original, _, _, _, edges = replay.make_instance(selectors, bodies, permuted=True)
        instance = BACK.Instance(original.n, tuple(reversed(original.tests)))
        threshold = instance.n//max(selectors)
        factors = ResponseFactors(instance, tuple(q for q, test in enumerate(instance.tests)
                                                 if min(test.bit_count(), instance.n-test.bit_count()) >= threshold))
        assert sorted(factors.alphabets) == sorted(selectors+bodies)
        tree, _, case_stats = plan_factors(instance, factors)
        execute(instance, tree)
        width = sum((size-1).bit_length() for size in bodies)
        upper = instance.n*(sum(replay.equality_mean(size) for size in selectors)+width)
        lower = len(edges)+math.prod(selectors)*replay.coding(math.prod(bodies))
        assert lower <= tree.cost <= upper
        structured.append({**case_stats, "n": instance.n, "threshold": threshold,
                           "joint_lower": str(lower), "comparison_upper": str(upper),
                           "initial_greedy_cost": instance.greedy(instance.full).cost,
                           "pure_queries_have_low_priority": True})

    # Root-to-leaf state count, not test-history enumeration: a full cube has
    # 3^d contexts while 2^d hypotheses. Audit d up to 7 without factorization.
    counts = [{"binary_factors": d, "n": 2**d, "contexts": 3**d}
              for d in range(1, 8)]
    output = {"status": "passed", "random_finite_instances": cases,
              "contexts_in_threshold_audits": context_count,
              "nonuniform_quotient_cases": nonuniform_count,
              "unequal_residual_example": stats, "cube_context_counts": counts,
              "conditional_eligibility_example": {**conditional_stats, "decoder_raw_cost": decoder.cost,
                                                    "static_singleton_decoder_raw_cost": 28},
              "retained_row_fallback_example": {**listed_stats, "ordinary_decoder_work": ordinary.cost,
                                                "chosen_decoder_work": listed_tree.cost},
              "multifactor_retained_pool_preserves_old_pool": True,
              "automatic_private_selector_cases": structured,
              "no_unrestricted_approximation_claim": True,
              "exact_UDT_subset_DP_is_validation_only": True}
    Path(__file__).with_name("research-general-factor-contexts-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
