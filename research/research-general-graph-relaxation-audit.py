"""Exact finite audit of bounded-alias query simulation in free activation."""

from collections import defaultdict
from fractions import Fraction
from itertools import product, combinations
import json
from pathlib import Path


def simulate(point, initial, parents, target, terms, charges):
    candidates = [set(values) for values in initial]
    history, paid = [], 0
    paid_events = []

    def close():
        changed = True
        while changed:
            changed = False
            for i, family in enumerate(parents):
                if len(candidates[i]) > 1 and all(len(candidates[p]) == 1 for p in family):
                    candidates[i] = {point[i]}
                    history.append(("free", i, point[i]))
                    changed = True

    close()
    answer = False
    for required, local in terms:
        failed = False
        for parent, value in zip(parents[target], required):
            if value not in candidates[parent]:
                failed = True
                break
            if len(candidates[parent]) == 1:
                continue
            event = tuple(history), parent, value
            hit = point[parent] == value
            paid_events.append((event, hit))
            paid += 1
            history.append(("paid", parent, value, hit))
            if hit:
                candidates[parent] = {value}
            else:
                candidates[parent].remove(value)
                failed = True
            close()
            if failed:
                break
        if not failed:
            close()
            assert len(candidates[target]) == 1
            if point[target] in local:
                answer = True
                break
    expected = any(all(point[p] == value for p, value in zip(parents[target], required))
                   and point[target] in local for required, local in terms)
    assert answer == expected
    history.append(("original_answer", answer))
    positive = [event[1] for event, hit in paid_events if hit]
    freely_revealed = [event[1] for event in history if event[0] == "free"]
    assert len(positive) == len(set(positive))
    assert len(freely_revealed) == len(set(freely_revealed))
    assert not set(positive) & set(freely_revealed)
    assert paid <= len(terms)+len(positive)
    charged = paid+sum(charges[i] for i in freely_revealed)
    assert charged <= len(terms)+sum(charges)
    return tuple(history), paid, paid_events, charged


def audit(initial, parents, target, terms, charges):
    points = tuple(product(*initial))
    transcripts = defaultdict(list)
    events = defaultdict(list)
    cost = 0
    for point in points:
        history, paid, paid_events, charged = simulate(point, initial, parents, target, terms, charges)
        transcripts[history].append(point)
        cost += paid
        for event, hit in paid_events:
            events[event].append(hit)
    for group in transcripts.values():
        projections = [set(point[i] for point in group) for i in range(len(initial))]
        assert len(group) == len(tuple(product(*projections)))
    for results in events.values():
        assert 2*sum(results) <= len(results)
    mean = Fraction(cost, len(points))
    assert mean <= 2*len(terms)
    return len(points), len(transcripts), len(events), mean


def main():
    cases = executions = posterior_checks = check_nodes = 0
    max_cost = Fraction(0)
    examples = []
    graphs = [((1,), (0,)),
              ((1,), (2,), (0,)),
              ((), (2,), (1,)),
              ((0,), (1,)),
              ((0, 1), (0, 1))]
    for parents in graphs:
        dimension = len(parents)
        for size in (2, 4):
            initial_states = [tuple(tuple(range(size)) for _ in range(dimension)),
                              tuple((0, 1) if i % 2 else tuple(range(size))
                                    for i in range(dimension))]
            for initial in initial_states:
                for target in range(dimension):
                    contexts = tuple(product(*(range(size) for _ in parents[target])))
                    for width in range(1, min(3, len(contexts))+1):
                        selected = contexts[:width]
                        terms = tuple((context,
                                       frozenset(value for value in range(size)
                                                 if (value+position) % 2))
                                      for position, context in enumerate(selected))
                        charges = ((size-1).bit_length(),)*dimension
                        tested, posteriors, nodes, mean = audit(initial, parents, target, terms, charges)
                        cases += 1
                        executions += tested
                        posterior_checks += posteriors
                        check_nodes += nodes
                        max_cost = max(max_cost, mean)
                        examples.append({"parents": parents, "size": size, "target": target,
                                         "D": width, "paid_mean": str(mean)})
    output = {"status": "passed", "query_simulation_cases": cases,
              "actual_hypothesis_simulations": executions,
              "exact_Cartesian_posterior_checks": posterior_checks,
              "conditional_paid_hit_probability_checks": check_nodes,
              "pathwise_charged_comparisons": executions,
              "maximum_paid_mean": str(max_cost),
              "cycles_and_self_parents_included": True,
              "no_OPT_or_subset_search": True,
              "common_parent_set_required": True,
              "examples": examples}
    Path(__file__).with_name("research-general-graph-relaxation-audit-results.json").write_text(
        json.dumps(output, indent=2)+"\n", encoding="utf-8")
    print(json.dumps({key: value for key, value in output.items() if key != "examples"}, indent=2))


if __name__ == "__main__":
    main()
