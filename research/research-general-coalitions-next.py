"""Search exact partial-identification costs for submodularity failure."""
from functools import lru_cache
import json
import random


def coalitions(n, tests):
    full = (1 << n)-1

    @lru_cache(None)
    def cost(state, wanted):
        if state.bit_count() <= 1 or not (state & wanted):
            return 0
        best = n*n
        for test in tests:
            a = state & test
            b = state ^ a
            if a and b:
                best = min(best, state.bit_count() + cost(a, wanted & a)
                           + cost(b, wanted & b))
        assert best < n*n
        return best

    return [cost(full, wanted) for wanted in range(1 << n)]


def search():
    rng = random.Random(190611385)
    checked = 0
    for n in range(3, 9):
        for _ in range(300):
            m = min(n+1, 10)
            words = rng.sample(range(1 << m), n)
            tests = tuple(sorted(set(sum(1 << h for h in range(n)
                                         if words[h] & (1 << j))
                                     for j in range(m))))
            tests = tuple(t for t in tests if t and t != (1 << n)-1)
            values = coalitions(n, tests)
            checked += 1
            for base in range(1 << n):
                missing = [h for h in range(n) if not base & (1 << h)]
                for i, x in enumerate(missing):
                    for y in missing[i+1:]:
                        ax = base | (1 << x)
                        ay = base | (1 << y)
                        both = ax | ay
                        if values[ax] + values[ay] < values[base] + values[both]:
                            return {"status": "submodularity disproved",
                                    "instances_checked": checked, "n": n,
                                    "tests": tests, "base": base, "x": x, "y": y,
                                    "cost_base": values[base], "cost_base_x": values[ax],
                                    "cost_base_y": values[ay], "cost_union": values[both]}
    return {"status": "no counterexample in finite search", "instances_checked": checked}


if __name__ == "__main__":
    print(json.dumps(search(), indent=2))
