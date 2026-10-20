"""Direct one-source completed-lift audit for the serial private-code family.

Uses actual fresh fallback at every globally replayed x0-fiber. No forced
positive source, intersections, or exact optimization oracle is needed.
"""

from fractions import Fraction
import importlib.util
import json
from pathlib import Path
import sys


spec = importlib.util.spec_from_file_location(
    "serial_single_backend", Path(__file__).with_name("research-general-recursive-lifting.py"))
SERIAL = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = SERIAL
spec.loader.exec_module(SERIAL)
LIFT = SERIAL.LIFT


def check(alphabets, permuted=False):
    original, points, tags, _, fibers = SERIAL.make_instance(alphabets)
    if permuted:
        tests = []
        for test, tag in zip(original.tests, tags):
            if tag[0] == "eq":
                tests.append(test)
                continue
            _, k, context, bit = tag
            shift = (k + sum((i + 1) * value for i, value in enumerate(context))) % alphabets[k]
            tests.append(sum(1 << h for h, point in enumerate(points)
                             if point[:k] == context and
                             ((alphabets[k] - 1 - point[k] + shift) % alphabets[k]) >> bit & 1))
        instance = SERIAL.Instance(original.n, tests)
        assert len(instance.tests) == len(tags)
    else:
        instance = original
    incumbent = instance.greedy(instance.full)
    core = sum(1 << h for h, point in enumerate(points) if not any(point[1:]))
    assert core in {node.state for node in SERIAL.tree_nodes(incumbent)}
    source = instance.greedy(core)
    assert all(node.test < 0 or tags[node.test][:2] == ("eq", 0)
               for node in SERIAL.tree_nodes(source))
    replay = LIFT.lift_partial(instance, source)
    assert {node.state for node in SERIAL.tree_nodes(replay) if node.test < 0} == set(fibers[1].values())

    def fresh_fill(node):
        if node.test < 0:
            return instance.greedy(node.state)
        return instance.branch(node.state, node.test, fresh_fill(node.left), fresh_fill(node.right))

    fresh = fresh_fill(replay)
    actual = LIFT.finish_partial(instance, replay, incumbent)
    bound = Fraction(alphabets[0] + 1, 2) - Fraction(1, alphabets[0])
    bound += sum((size - 1).bit_length() for size in alphabets[1:])
    for fiber in fibers[1].values():
        code = instance.greedy(fiber)
        for h in SERIAL.hypotheses(fiber):
            node, counts = code, [0] * len(alphabets)
            while node.test >= 0:
                tag = tags[node.test]
                assert tag[0] == "bit"
                counts[tag[1]] += 1
                node = node.left if instance.tests[node.test] >> h & 1 else node.right
            assert all(count <= (size - 1).bit_length() for count, size in zip(counts[1:], alphabets[1:]))
    LIFT.validate_execution(instance, fresh)
    LIFT.validate_execution(instance, actual)
    assert actual.cost <= fresh.cost <= instance.n * bound
    return {"alphabets": alphabets, "context_dependent_permutations": permuted,
            "n": instance.n, "m": len(instance.tests), "initial_cost": incumbent.cost,
            "source_population": core.bit_count(), "source_nodes": len(tuple(SERIAL.tree_nodes(source))),
            "replayed_x0_fibers": len(fibers[1]), "fresh_only_completion_cost": fresh.cost,
            "existing_min_fallback_completion_cost": actual.cost,
            "proved_mean_bound": str(bound), "uses_intersections": False,
            "uses_exact_optimization_oracle": False}


def main():
    results = [check(sizes, permuted) for sizes in ((8, 6), (10, 8), (10, 8, 6))
               for permuted in (False, True)]
    Path(__file__).with_name("research-general-recursive-single-lift-results.json").write_text(
        json.dumps(results, indent=2), encoding="utf-8")
    print(json.dumps(results, indent=2), flush=True)


if __name__ == "__main__":
    main()
