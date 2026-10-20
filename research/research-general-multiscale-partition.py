"""Exact collision-frontier pruning inside explicit original-test templates.

This is a polynomial primitive, not an unrestricted approximation algorithm.
The executable candidate uses supplied templates only. Exhaustive prefix
enumeration below is bounded validation and is never called by the candidate.
"""

from functools import lru_cache
from fractions import Fraction
import importlib.util
import json
from math import isqrt, log2
from pathlib import Path
import random
import sys


def load_backend():
    path = Path(__file__).with_name("research-general-algorithm-next.py")
    spec = importlib.util.spec_from_file_location("multiscale_backend", path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


BACK = load_backend()


def leaves(tree):
    return [node for node in BACK.tree_nodes(tree) if node.test < 0]


def collision(tree):
    return sum(leaf.state.bit_count() ** 2 for leaf in leaves(tree))


def collision_frontier(instance, template):
    """Every attainable collision integer -> minimum-work template prefix.

    Arithmetic index range is at most s^2. A deliberately loose bound is
    O(s^5) arithmetic operations per explicit binary template. The tree is
    proper, and only its actual supplied tests can be reconstructed.
    """
    tables = {}

    def visit(node):
        size = node.state.bit_count()
        table = {size * size: (0, None)}
        if node.test >= 0:
            left, right = visit(node.left), visit(node.right)
            for zl, (wl, _) in left.items():
                for zr, (wr, _) in right.items():
                    z, work = zl + zr, size + wl + wr
                    if z not in table or work < table[z][0]:
                        table[z] = work, (zl, zr)
        tables[id(node)] = table
        return table

    root_table = visit(template)

    def reconstruct(node, z):
        work, action = tables[id(node)][z]
        if action is None:
            return BACK.Tree(node.state)
        zl, zr = action
        result = instance.branch(node.state, node.test,
                                 reconstruct(node.left, zl),
                                 reconstruct(node.right, zr))
        assert result.cost == work
        return result

    def choose(budget):
        feasible = [(work, z) for z, (work, _) in root_table.items() if z <= budget]
        if not feasible:
            return None
        work, z = min(feasible)
        result = reconstruct(template, z)
        assert result.cost == work and collision(result) == z
        return result

    return {z: value[0] for z, value in root_table.items()}, choose


def recursive_partition(instance, templates):
    """Compile collision <= floor(s^(3/2)) stages, using actual restrictions.

    If these stages additionally had cost <= a OPT(S), the note proves an
    O(a loglog n) ratio. That missing unrestricted comparison is NOT assumed
    or checked here. Runtime is fixed polynomial for an explicit library.
    """
    stages = []

    def solve(state):
        size = state.bit_count()
        if size <= 1:
            return BACK.Tree(state)
        budget = isqrt(size ** 3)
        candidates = []
        for template in templates:
            restricted = instance.prune(template, state)
            _, choose = collision_frontier(instance, restricted)
            candidate = choose(budget)
            assert candidate is not None
            candidates.append(candidate)
        partial = min(candidates, key=lambda tree: (tree.cost, collision(tree)))
        assert partial.test >= 0
        assert collision(partial) <= budget < size * size
        stages.append({"size": size, "work": partial.cost,
                       "collision": collision(partial),
                       "largest_leaf": max(x.state.bit_count() for x in leaves(partial))})

        def finish(node):
            if node.test < 0:
                return solve(node.state)
            return instance.branch(node.state, node.test,
                                   finish(node.left), finish(node.right))

        return finish(partial)

    return solve(instance.full), stages


def all_prefixes(instance, node):
    """Bounded exhaustive validation only."""
    result = [BACK.Tree(node.state)]
    if node.test >= 0:
        for left in all_prefixes(instance, node.left):
            for right in all_prefixes(instance, node.right):
                result.append(instance.branch(node.state, node.test, left, right))
    return result


def validate_tree(instance, tree, complete=False):
    seen = 0
    for node in BACK.tree_nodes(tree):
        assert node.state
        if node.test < 0:
            assert not (seen & node.state)
            seen |= node.state
            assert node.cost == 0
            if complete:
                assert node.state.bit_count() == 1
        else:
            hit = node.state & instance.tests[node.test]
            assert hit and hit != node.state
            assert node.left.state == hit
            assert node.right.state == (node.state ^ hit)
            assert node.cost == node.state.bit_count() + node.left.cost + node.right.cost
    assert seen == tree.state


def random_template(n, rng):
    tests = []

    def structure(values):
        if len(values) == 1:
            return values[0]
        rng.shuffle(values)
        cut = rng.randrange(1, len(values))
        left, right = values[:cut], values[cut:]
        mask = sum(1 << h for h in left)
        tests.append(mask)
        return (mask, structure(left), structure(right))

    shape = structure(list(range(n)))
    instance = BACK.Instance(n, tests)

    def materialize(item):
        if isinstance(item, int):
            return BACK.Tree(1 << item)
        mask, left, right = item
        left, right = materialize(left), materialize(right)
        return instance.branch(left.state | right.state, instance.tests.index(mask), left, right)

    return instance, materialize(shape)


def entropy_counterexample_formula(t):
    n, k = 2 ** (3 * t), 2 ** (2 * t)
    core = k * (k + 1) // 2 - 1
    stage_work, stages = 0, []
    for j in range(t):
        s, e = n >> j, n >> (j + 1)
        probes = (k * k + 4 * e - 1) // (4 * e)
        point_work = e * probes - probes * (probes - 1) // 2
        # An actual binary bit code after the probes has no greater cost.
        upper_work = s + point_work + (e - probes) * (e.bit_length() - 1)
        stage_work += point_work
        stages.append({"size": s, "easy": e, "point_probes": probes,
                       "point_work": point_work, "work_upper_bound": upper_work,
                       "conditional_log_size": 0.5 * log2(s / 2),
                       "entropy": 0.5 * log2(s) + 0.5})
        assert point_work >= k * k / 8
        if t >= 4:
            assert upper_work <= 3 * core
    comparison_upper = core + sum((n >> j) + (n >> (j + 1)) * (3 * t - j - 1)
                                  for j in range(t))
    return {"t": t, "n": n, "core_size": k, "core_optimum": core,
            "global_optimum_upper_bound": comparison_upper,
            "algorithm_work_lower_bound": core + stage_work,
            "ratio_lower_bound": (core + stage_work) / comparison_upper,
            "stages": stages}


def entropy_counterexample_actual(t):
    """Build and execute the specified legal partial policies on tiny inputs."""
    n, k = 2 ** (3 * t), 2 ** (2 * t)
    tests = [1 << h for h in range(n)]
    blocks, membership, codes = [], [], []
    cursor = k
    for j in reversed(range(t)):
        e = n >> (j + 1)
        block = list(range(cursor, cursor + e))
        cursor += e
        blocks.insert(0, block)
    assert cursor == n
    for block in blocks:
        membership.append(len(tests))
        tests.append(sum(1 << h for h in block))
        rows = []
        for bit in range(len(block).bit_length() - 1):
            rows.append(len(tests))
            tests.append(sum(1 << h for value, h in enumerate(block) if value >> bit & 1))
        codes.append(rows)
    instance = BACK.Instance(n, tests)
    # Instance deduplicates rows, so map actual stored rows back to indices.
    membership = [instance.tests.index(sum(1 << h for h in block)) for block in blocks]
    codes = [[instance.tests.index(sum(1 << h for value, h in enumerate(block) if value >> bit & 1))
              for bit in range(len(block).bit_length() - 1)] for block in blocks]
    state, actual_stages = instance.full, []

    def bit_code(mask, rows, index=0):
        if mask.bit_count() <= 1:
            return BACK.Tree(mask)
        q = rows[index]
        hit, miss = mask & instance.tests[q], mask & ~instance.tests[q]
        if not hit or not miss:
            return bit_code(mask, rows, index + 1)
        return instance.branch(mask, q, bit_code(hit, rows, index + 1),
                               bit_code(miss, rows, index + 1))

    for block, q, rows in zip(blocks, membership, codes):
        hit = state & instance.tests[q]
        miss = state ^ hit
        e = len(block)
        probes = (k * k + 4 * e - 1) // (4 * e)

        def poor_code(mask, index=0):
            if mask.bit_count() <= 1:
                return BACK.Tree(mask)
            if index == probes:
                return bit_code(mask, rows)
            h = block[index]
            single = 1 << h
            return instance.branch(mask, instance.tests.index(single), BACK.Tree(single),
                                   poor_code(mask ^ single, index + 1))

        partial = instance.branch(state, q, poor_code(hit), BACK.Tree(miss))
        validate_tree(instance, partial)
        assert sum(x.state.bit_count() == 1 for x in leaves(partial)) == e
        assert collision(partial) == e + (state.bit_count() // 2) ** 2
        actual_stages.append(partial.cost)
        state = miss
    assert state == (1 << k) - 1
    formula = entropy_counterexample_formula(t)
    assert all(work <= record["work_upper_bound"] for work, record in zip(actual_stages, formula["stages"]))
    return {"t": t, "n": n, "actual_stage_work": actual_stages}


def main():
    rng = random.Random(80341)
    prefix_comparisons = threshold_comparisons = recursive_stages = density_checks = 0
    for n in range(2, 11):
        for repeat in range(5):
            instance, tree = random_template(n, rng)
            states = [instance.full]
            if n > 2:
                states.append(sum(1 << h for h in rng.sample(range(n), rng.randrange(2, n))))
            for state in states:
                template = instance.prune(tree, state)
                size = state.bit_count()
                table, choose = collision_frontier(instance, template)
                brute = {}
                for prefix in all_prefixes(instance, template):
                    z = collision(prefix)
                    brute[z] = min(brute.get(z, 10 ** 9), prefix.cost)
                    prefix_comparisons += 1
                    if prefix.cost:
                        root_density = max(
                            Fraction(2 * (state & test).bit_count() *
                                     (state & ~test).bit_count(), size)
                            for test in instance.tests
                        )
                        assert Fraction(size * size - z, prefix.cost) <= root_density
                        density_checks += 1
                assert table == brute
                for budget in range(size, size * size + 1):
                    result = choose(budget)
                    optimum = min(work for z, work in brute.items() if z <= budget)
                    assert result is not None and result.cost == optimum
                    validate_tree(instance, result)
                    threshold_comparisons += 1
            compiled, stages = recursive_partition(instance, [tree, instance.greedy(instance.full)])
            validate_tree(instance, compiled, complete=True)
            assert len(stages) <= n - 1
            recursive_stages += len(stages)
    formulas = [entropy_counterexample_formula(t) for t in range(1, 31)]
    actual = [entropy_counterexample_actual(t) for t in range(1, 4)]
    result = {"status": "conditional transfer and exact supplied-template primitive; no unrestricted ratio",
              "prefix_comparisons": prefix_comparisons,
              "collision_threshold_comparisons": threshold_comparisons,
              "adaptive_collision_density_checks": density_checks,
              "recursive_stage_checks": recursive_stages,
              "entropy_counterexample_actual": actual,
              "entropy_counterexample_formula": formulas}
    path = Path(__file__).with_name("research-general-multiscale-partition-results.json")
    path.write_text(json.dumps(result, indent=2), encoding="utf8")
    print(json.dumps({key: value for key, value in result.items()
                      if key not in ("entropy_counterexample_formula",)}, indent=2))


if __name__ == "__main__":
    main()
