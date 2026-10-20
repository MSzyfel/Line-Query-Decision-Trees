"""Exact checks for polynomial-lookahead and endpoint-accounting obstacles."""
from fractions import Fraction
from functools import lru_cache
from math import log2


def endpoint_grid_check():
    cells = [(left, right) for left in (1, 2, 3) for right in (5, 6, 7)]
    masks = []
    for query in range(9):
        mask = sum(1 << i for i, (left, right) in enumerate(cells)
                   if left <= query <= right)
        if mask not in (0, (1 << len(cells)) - 1) and mask not in masks:
            masks.append(mask)
    eta = Fraction(1, 10000)
    central = cells.index((2, 6))
    weights = [eta] * len(cells)
    weights[central] = 1 - 8 * eta

    @lru_cache(None)
    def exact(state):
        if state & (state - 1) == 0:
            return Fraction(0)
        mass = sum(weights[i] for i in range(len(cells)) if state >> i & 1)
        result = None
        for mask in masks:
            left, right = state & mask, state & ~mask
            if not left or not right:
                continue
            value = mass + exact(left) + exact(right)
            result = value if result is None else min(result, value)
        assert result is not None
        return result

    axial = [(1, 6), (3, 6), (2, 5), (2, 7)]
    distinguishing = []
    for other in axial:
        tests = []
        for query in range(9):
            central_bit = 2 <= query <= 6
            other_bit = other[0] <= query <= other[1]
            if central_bit != other_bit:
                tests.append(query)
        assert len(tests) == 1
        distinguishing.append(tests[0])
    assert len(set(distinguishing)) == 4
    entropy = -sum(float(weight) * log2(float(weight)) for weight in weights)
    optimum = exact((1 << len(cells)) - 1)
    assert float(optimum) > entropy + 3
    assert 4 > -log2(float(weights[central])) + 3
    print(f"Endpoint grid: optimum {float(optimum):.9f}, entropy {entropy:.9f}, "
          f"redundancy {float(optimum) - entropy:.9f} bits.")
    print(f"Four necessary central-cell tests: {distinguishing}.")


if __name__ == "__main__":
    endpoint_grid_check()
