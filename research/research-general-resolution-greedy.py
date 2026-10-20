"""Bounded audits for exact-credit plus integer-coding greedy.

No optimization oracle and no large adversarial search. The scalable result
is algebraic; only three explicit product instances are constructed here.
"""

from fractions import Fraction
from functools import lru_cache
import importlib.util
import math
from pathlib import Path
import sys


def load_family():
    spec = importlib.util.spec_from_file_location(
        "resolution_serial_family",
        Path(__file__).with_name("research-general-recursive-lifting.py"))
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


SERIAL = load_family()


def coding_cost(size):
    if size <= 1:
        return 0
    depth = (size - 1).bit_length()
    return size * (depth + 1) - (1 << depth)


def audit_explicit(alphabets):
    instance, points, tags, tag_index, _ = SERIAL.make_instance(alphabets)
    incumbent = instance.greedy(instance.full)
    nodes = {id(node): node for node in SERIAL.tree_nodes(incumbent)}

    @lru_cache(None)
    def restricted(node_id, state):
        if state.bit_count() <= 1:
            return 0
        node = nodes[node_id]
        if state == node.state:
            return node.cost
        hit = state & instance.tests[node.test]
        miss = state ^ hit
        if not hit:
            return restricted(id(node.right), state)
        if not miss:
            return restricted(id(node.left), state)
        return (state.bit_count() + restricted(id(node.left), hit)
                + restricted(id(node.right), miss))

    weights = [(gamma, price)
               for gamma in (Fraction(0), Fraction(1, 2), Fraction(1), Fraction(3))
               for price in (Fraction(1), Fraction(3))]
    query_checks = score_checks = 0
    for node in nodes.values():
        if node.test < 0:
            continue
        state, size = node.state, node.state.bit_count()
        options = []
        for index, test in enumerate(instance.tests):
            hit, miss = state & test, state & ~test
            if not hit or not miss:
                continue
            credit = (node.cost - restricted(id(node), hit)
                      - restricted(id(node), miss))
            drop = coding_cost(size) - coding_cost(hit.bit_count()) - coding_cost(miss.bit_count())
            assert 0 <= credit <= size, (alphabets, tags[index], size, credit)
            options.append((index, credit, drop))
            query_checks += 1
        incumbent_action = next(x for x in options if x[0] == node.test)
        assert incumbent_action[1] == size
        assert incumbent_action[2] == max(x[2] for x in options)
        for gamma, price in weights:
            chosen = min(options, key=lambda x: (-gamma * x[1] - price * x[2], x[0]))
            assert chosen[0] == node.test, (alphabets, size, chosen, node.test)
            score_checks += 1

    # Conditional expected marginal credit strictly increases after a selector.
    gate = tag_index[("bit", 1, (0,), 0)]
    selector = tag_index[("eq", 0, 0)]
    full, selected = instance.full, instance.tests[selector]

    def credit_at(state, index):
        hit = state & instance.tests[index]
        return (restricted(id(incumbent), state)
                - restricted(id(incumbent), hit)
                - restricted(id(incumbent), state ^ hit))

    before = Fraction(credit_at(full, gate), instance.n)
    after = Fraction(credit_at(selected, gate), selected.bit_count())
    first, second = alphabets[:2]
    assert before == Fraction(1, 2) + Fraction(second + 2, 8 * first)
    assert after == Fraction(second, 4) + Fraction(1, second)
    assert after > before

    # A real cross-context stage: a selector followed by complete active codes.
    selected_levels = len(alphabets) - 1

    def decode(state, level, context, next_bit=0):
        if level > selected_levels:
            return SERIAL.Tree(state)
        values = {points[h][level] for h in SERIAL.hypotheses(state)}
        if len(values) == 1:
            return decode(state, level + 1, context + (next(iter(values)),))
        for bit in range(next_bit, (alphabets[level] - 1).bit_length()):
            query = tag_index[("bit", level, context, bit)]
            hit = state & instance.tests[query]
            if hit and hit != state:
                return instance.branch(state, query,
                                       decode(hit, level, context, bit + 1),
                                       decode(state ^ hit, level, context, bit + 1))
        raise AssertionError("binary coordinates failed to identify a value")

    stage = instance.branch(full, selector, decode(selected, 1, (0,)),
                            SERIAL.Tree(full ^ selected))
    SERIAL.LIFT.validate_execution(instance, stage)
    residual = sum(restricted(id(incumbent), leaf.state)
                   for leaf in SERIAL.tree_nodes(stage) if leaf.test < 0)
    bundle_credit = incumbent.cost - residual
    expected_credit = instance.n + Fraction(instance.n, first) * sum(
        (Fraction(a + 1, 2) - Fraction(1, a)) for a in alphabets[1:])
    assert bundle_credit == expected_credit
    bundle_upper = instance.n + Fraction(instance.n, first) * sum(
        (a - 1).bit_length() for a in alphabets[1:])
    assert stage.cost <= bundle_upper
    fresh_child = instance.greedy(selected)
    for node in SERIAL.tree_nodes(fresh_child):
        if node.test < 0:
            continue
        unencoded = [k for k in range(1, len(alphabets))
                     if len({points[h][k] for h in SERIAL.hypotheses(node.state)}) > 1]
        tag = tags[node.test]
        assert tag[0] == "bit" and tag[1] == min(unencoded), tag
    fresh_bundle = instance.branch(full, selector, fresh_child, SERIAL.Tree(full ^ selected))
    SERIAL.LIFT.validate_execution(instance, fresh_bundle)
    assert fresh_bundle.cost <= bundle_upper
    return {"alphabets": alphabets, "n": instance.n, "queries": query_checks,
            "weighted_actions": score_checks, "raw_cost": incumbent.cost,
            "marginal_before": str(before), "marginal_after": str(after),
            "activation_bundle_work": stage.cost,
            "activation_bundle_credit": bundle_credit,
            "fresh_greedy_bundle_work": fresh_bundle.cost}


def main():
    coding_checks = 0
    for size in range(2, 401):
        drops = [coding_cost(size) - coding_cost(a) - coding_cost(size - a)
                 for a in range(size // 2 + 1)]
        assert drops == sorted(drops)
        for a in range(size // 3):
            assert drops[a + 1] > drops[a]
            coding_checks += 1

    results = [audit_explicit(alphabets)
               for alphabets in ((8, 6), (10, 8), (10, 8, 6))]
    algebra_rows = []
    for base in (16, 32, 64, 128, 256, 512):
        levels = math.floor(base / math.log2(base))
        alphabets = tuple(base + 2 * (levels - k) for k in range(levels + 1))
        population = math.prod(alphabets)
        cap = population // base
        drop = coding_cost(population) - coding_cost(cap) - coding_cost(population - cap)
        # Exact best root mixed score for gamma=1/2, coding price=1.
        assert Fraction(population, 2) + drop < population
        greedy = sum((Fraction(a + 1, 2) - Fraction(1, a)) for a in alphabets)
        comparison = Fraction(alphabets[0] + 1, 2) - Fraction(1, alphabets[0])
        comparison += sum((a - 1).bit_length() for a in alphabets[1:])
        assert comparison <= 4 * base
        bundle_credit_per_mass = 1 + sum(
            (Fraction(a + 1, 2) - Fraction(1, a)) for a in alphabets[1:4]) / alphabets[0]
        bundle_work_upper_per_mass = 1 + Fraction(
            sum((a - 1).bit_length() for a in alphabets[1:4]), alphabets[0])
        if base >= 128:
            assert bundle_work_upper_per_mass <= bundle_credit_per_mass / 2
        full_bundle_credit_per_mass = 1 + sum(
            (Fraction(a + 1, 2) - Fraction(1, a)) for a in alphabets[1:]) / alphabets[0]
        full_bundle_work_upper_per_mass = 1 + Fraction(
            sum((a - 1).bit_length() for a in alphabets[1:]), alphabets[0])
        if base >= 64:
            assert full_bundle_work_upper_per_mass <= full_bundle_credit_per_mass / 2
        algebra_rows.append({"M": base, "levels": levels,
                             "n_bitlength": population.bit_length(),
                             "greedy_over_comparison": float(greedy / comparison),
                             "best_root_mixed_score_over_work": float(Fraction(1, 2) + Fraction(drop, population)),
                             "three_level_bundle_half_credit_over_work_upper": float(
                                 bundle_credit_per_mass / (2 * bundle_work_upper_per_mass)),
                             "fresh_child_bundle_half_credit_over_work_upper": float(
                                 full_bundle_credit_per_mass / (2 * full_bundle_work_upper_per_mass))})

    print("PASS integer coding monotonicity/strictness checks:", coding_checks)
    for result in results:
        print("PASS exact hierarchy-credit and mixed-action audit:", result)
    print("PASS algebraic growing-depth family (no response matrices constructed):", algebra_rows)


if __name__ == "__main__":
    main()
