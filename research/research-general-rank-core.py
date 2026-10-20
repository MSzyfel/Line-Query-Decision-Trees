"""Finite validation of the majority literal-rank constructor.

The research algorithm uses polynomial submodular minimization. This checker
enumerates subsets to validate every minimizer on small instances; it is NOT
an implementation of that polynomial SFM algorithm.
"""

from __future__ import annotations

import itertools
import json
import random
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path


def add_to_basis(value: int, pivots: dict[int, int]) -> bool:
    while value:
        pivot = value.bit_length() - 1
        if pivot in pivots:
            value ^= pivots[pivot]
        else:
            pivots[pivot] = value
            return True
    return False


def binary_rank(vectors: list[int]) -> int:
    pivots: dict[int, int] = {}
    for value in vectors:
        add_to_basis(value, pivots)
    return len(pivots)


@dataclass(frozen=True)
class Instance:
    n: int
    tests: tuple[int, ...]

    @property
    def full(self) -> int:
        return (1 << self.n) - 1

    def column(self, h: int) -> int:
        return 1 + sum(((test >> h) & 1) << (j + 1)
                       for j, test in enumerate(self.tests))

    def rank(self, core: int) -> int:
        return binary_rank([self.column(h) for h in range(self.n)
                            if core & (1 << h)])

    def identifying(self) -> bool:
        return len({self.column(h) for h in range(self.n)}) == self.n

    def basis_queries(self, core: int) -> tuple[int, ...]:
        assert core
        pivots: dict[int, int] = {}
        assert add_to_basis(core, pivots)  # the free constant row
        queries = []
        for j, test in enumerate(self.tests):
            if add_to_basis(test & core, pivots):
                queries.append(j)
        assert len(queries) == self.rank(core) - 1
        signatures = {tuple((self.tests[j] >> h) & 1 for j in queries)
                      for h in range(self.n) if core & (1 << h)}
        assert len(signatures) == core.bit_count()
        return tuple(queries)


@dataclass
class CoreNode:
    core: int
    query: int | None = None
    zero: CoreNode | None = None
    one: CoreNode | None = None


def core_code(instance: Instance, core: int) -> tuple[CoreNode, int, int]:
    queries = instance.basis_queries(core)

    def build(cell: int, start: int) -> tuple[CoreNode, int, int]:
        if cell.bit_count() == 1:
            return CoreNode(cell), 0, 0
        while start < len(queries):
            j = queries[start]
            positive = cell & instance.tests[j]
            if positive and positive != cell:
                zero, work0, height0 = build(cell ^ positive, start + 1)
                one, work1, height1 = build(positive, start + 1)
                return (CoreNode(cell, j, zero, one),
                        cell.bit_count() + work0 + work1,
                        1 + max(height0, height1))
            start += 1
        raise AssertionError("A separating row basis failed to identify core")

    result = build(core, 0)
    assert result[1] <= core.bit_count() * (instance.rank(core) - 1)
    assert result[2] <= instance.rank(core) - 1
    return result


def lift(instance: Instance, root: CoreNode) -> tuple[int, int, int]:
    """Return raw work, actually identified mask, and queried-node count."""
    def execute(node: CoreNode, cell: int) -> tuple[int, int, int]:
        assert node.core & cell == node.core
        outside = cell ^ node.core
        if outside.bit_count() >= node.core.bit_count():
            return 0, 0, 0
        if node.query is None:
            assert cell == node.core and cell.bit_count() == 1
            return 0, cell, 0
        positive = cell & instance.tests[node.query]
        assert node.zero is not None and node.one is not None
        work0, complete0, nodes0 = execute(node.zero, cell ^ positive)
        work1, complete1, nodes1 = execute(node.one, positive)
        assert not complete0 & complete1
        return (cell.bit_count() + work0 + work1,
                complete0 | complete1, 1 + nodes0 + nodes1)
    return execute(root, instance.full)


def check_instance(instance: Instance) -> dict[str, int]:
    assert instance.identifying()
    n = instance.n
    ranks = [instance.rank(core) for core in range(1 << n)]
    constructions = {}
    for core in range(1, 1 << n):
        root, core_work, height = core_code(instance, core)
        work, completed, nodes = lift(instance, root)
        a = core.bit_count()
        assert completed & core == completed
        assert work <= 2 * core_work
        assert completed.bit_count() >= 2 * a - n
        assert nodes <= a - 1
        constructions[core] = (work, completed.bit_count())

    minimizers_checked = 0
    promised_guesses = 0
    for guess in range(1, min(n, len(instance.tests) + 1) + 1):
        objective = [n * ranks[core] - 4 * guess * core.bit_count()
                     for core in range(1 << n)]
        best = min(objective)
        promise = any(4 * core.bit_count() >= 3 * n and ranks[core] <= guess
                      for core in range(1 << n))
        if not promise:
            continue
        promised_guesses += 1
        assert best <= -2 * n * guess
        for core, value in enumerate(objective):
            if value != best:
                continue
            minimizers_checked += 1
            a = core.bit_count()
            assert 2 * a > n
            assert 4 * guess * a - n * ranks[core] >= 2 * n * guess
            work, completed = constructions[core]
            assert completed > 0
            assert Fraction(work, completed) <= 4 * guess
            # Check the exact cancellation independently of actual work.
            assert Fraction(2 * a * ranks[core], 2 * a - n) <= 4 * guess
    return {"cores": len(constructions),
            "promised_rank_guesses": promised_guesses,
            "all_minimizers_checked": minimizers_checked}


def exhaustive_instances() -> list[Instance]:
    instances = []
    for n in range(2, 5):
        # One representative of each complementary nonconstant binary test.
        canonical_tests = list(range(2, 1 << n, 2))
        for selected in range(1 << len(canonical_tests)):
            tests = tuple(test for j, test in enumerate(canonical_tests)
                          if selected & (1 << j))
            instance = Instance(n, tests)
            if instance.identifying():
                instances.append(instance)
    return instances


def random_instances(seed: int = 170419) -> list[Instance]:
    rng = random.Random(seed)
    instances = []
    for n in range(5, 10):
        for _ in range(16):
            while True:
                count = rng.randint(max(2, (n - 1).bit_length()), 2 * n)
                tests = tuple(sorted({rng.randrange(1, 1 << n)
                                      & ~1 for _ in range(count)} - {0}))
                instance = Instance(n, tests)
                if instance.identifying():
                    instances.append(instance)
                    break
    return instances


def obstruction() -> list[dict[str, int]]:
    result = []
    for bits in range(1, 5):
        n = 1 << bits
        coordinates = [sum(((h >> j) & 1) << h for h in range(n))
                       for j in range(bits)]
        instance = Instance(n, tuple(coordinates + [1 << h for h in range(n)]))
        # Identity singleton rows prove the claim for all subsets; exhaust
        # all subsets through n=8 and sample sizes for n=16.
        subsets = range(1 << n) if n <= 8 else [0, (1 << n) - 1,
                   *[(1 << k) - 1 for k in range(1, n)]]
        for core in subsets:
            assert instance.rank(core) == core.bit_count()
        result.append({"n": n, "coordinate_code_mean": bits,
                       "minimum_three_quarter_literal_rank": (3 * n + 3) // 4})
    return result


def structured_nontrivial_core() -> dict[str, int]:
    """Exact finite flat enumeration where SFM discards eight outsiders.

    The 24 core columns have the form (1,x,0^8), x=0,...,23;
    outsider j has form (1,0^5,e_j). With lambda=4/3, each outsider
    independently reduces the maximized objective by 1/3 and is excluded.
    Every optimal core subset is its linear-span closure, so enumerating
    the finite six-dimensional spans checks the global optimum exactly.
    This special finite enumeration is also validation, not general SFM.
    """
    n, core_size, rank_guess = 32, 24, 6
    coordinate_tests = [sum(((h >> j) & 1) << h for h in range(core_size))
                        for j in range(5)]
    outsider_tests = [1 << h for h in range(core_size, n)]
    instance = Instance(n, tuple(coordinate_tests + outsider_tests))
    core = (1 << core_size) - 1
    assert instance.identifying() and instance.rank(core) == rank_guess
    columns = [1 + (h << 1) for h in range(core_size)]
    spans = {1}  # A bitset of vector values; bit zero is the zero vector.
    frontier = [1]
    while frontier:
        span = frontier.pop()
        values = [x for x in range(64) if span & (1 << x)]
        for vector in columns:
            if span & (1 << vector):
                continue
            enlarged = span
            for value in values:
                enlarged |= 1 << (value ^ vector)
            if enlarged not in spans:
                spans.add(enlarged)
                frontier.append(enlarged)
    optimum = None
    minimizers = []
    for span in spans:
        closure = sum(1 << h for h, vector in enumerate(columns)
                      if span & (1 << vector))
        rank = span.bit_count().bit_length() - 1
        assert instance.rank(closure) == rank
        objective = n * rank - 4 * rank_guess * closure.bit_count()
        if optimum is None or objective < optimum:
            optimum, minimizers = objective, [closure]
        elif objective == optimum:
            minimizers.append(closure)
    assert minimizers == [core]
    root, core_work, height = core_code(instance, core)
    work, completed, _ = lift(instance, root)
    assert completed.bit_count() >= 2 * core_size - n
    assert work <= 2 * core_work
    assert Fraction(work, completed.bit_count()) <= 4 * rank_guess
    return {"n": n, "selected_core_size": core_size,
            "selected_core_rank": rank_guess, "discarded_outsiders": n - core_size,
            "exact_generated_spans_checked": len(spans),
            "core_code_height": height, "core_code_raw_work": core_work,
            "lifted_raw_work": work, "identified": completed.bit_count()}


def main() -> None:
    exhaustive = exhaustive_instances()
    random_sample = random_instances()
    totals = {"cores": 0, "promised_rank_guesses": 0,
              "all_minimizers_checked": 0}
    for instance in itertools.chain(exhaustive, random_sample):
        checked = check_instance(instance)
        for key, value in checked.items():
            totals[key] += value
    result = {"status": "passed", "enumeration_is_validation_only": True,
              "exhaustive_identifying_instances_n2_through_n4": len(exhaustive),
              "random_identifying_instances_n5_through_n9": len(random_sample),
              **totals, "structured_nontrivial_core": structured_nontrivial_core(),
              "singleton_augmented_coordinate_obstruction": obstruction()}
    destination = Path(__file__).with_name("research-general-rank-core-results.json")
    destination.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
