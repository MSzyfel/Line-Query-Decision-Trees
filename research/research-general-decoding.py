"""Check the syndrome partition obstruction by exact original-test DP."""
from functools import lru_cache
from itertools import product
import json
import random


def rank(rows):
    basis = {}
    for value in rows:
        while value:
            pivot = value.bit_length() - 1
            if pivot in basis:
                value ^= basis[pivot]
            else:
                basis[pivot] = value
                break
    return len(basis)


def check(d, rows):
    n = 1 << d
    tests = [sum(1 << h for h in range(n) if h & (1 << i))
             for i in range(d)]
    labels = [sum(((h & row).bit_count() & 1) << j
                  for j, row in enumerate(rows)) for h in range(n)]
    fibres = [sum(1 << h for h in range(n) if labels[h] == label)
              for label in range(1 << len(rows))]

    @lru_cache(None)
    def identify(state):
        size = state.bit_count()
        if size <= 1:
            return 0
        options = []
        for test in tests:
            hit = state & test
            miss = state ^ hit
            if hit and miss:
                options.append(identify(hit) + identify(miss))
        assert options
        return size + min(options)

    @lru_cache(None)
    def reveal(state):
        if sum(bool(state & fibre) for fibre in fibres) <= 1:
            return 0
        options = []
        for test in tests:
            hit = state & test
            miss = state ^ hit
            if hit and miss:
                options.append(reveal(hit) + reveal(miss))
        assert options
        return state.bit_count() + min(options)

    whole = (1 << n) - 1
    r = rank(rows)
    assert r == len(rows)
    active = 0
    for row in rows:
        active |= row
    full_cost = identify(whole)
    continuation = sum(identify(fibre) for fibre in fibres)
    stage = reveal(whole)
    assert full_cost == n * d, (d, rows, full_cost)
    assert continuation == n * (d-r), (d, rows, continuation)
    assert stage == n * active.bit_count(), (d, rows, stage)
    return full_cost, continuation, stage


def main():
    exhaustive = 0
    for d in range(1, 4):
        for r in range(1, d+1):
            for rows in product(range(1 << d), repeat=r):
                if rank(rows) == r:
                    check(d, rows)
                    exhaustive += 1
    rng = random.Random(20261018)
    randomized = 0
    for d in range(4, 8):
        for _ in range(24):
            r = rng.randint(1, d)
            rows = []
            while len(rows) < r:
                candidate = rng.randrange(1, 1 << d)
                if rank(rows + [candidate]) > len(rows):
                    rows.append(candidate)
            check(d, rows)
            randomized += 1
    parity = []
    for d in range(1, 9):
        full, continuation, stage = check(d, [(1 << d)-1])
        parity.append({"d": d, "n": 1 << d, "F": full,
                       "Delta": full-continuation, "stage_work": stage})
    print(json.dumps({"exhaustive_matrices": exhaustive,
                      "seeded_random_matrices": randomized,
                      "parity_examples": parity,
                      "status": "all exact recurrences agree"}, indent=2))


if __name__ == "__main__":
    main()
