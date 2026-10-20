"""Independent checks for joint endpoint decoding and shifted block schedules.

Finite checks supplement the proofs in direction2-joint-decoding.md.
All displayed approximation-constant certificates use exact rational arithmetic.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import permutations
from random import Random


def interval_grade_cost(m, demands, delays, zero_weight):
    """One first block is forced outside these ordinary interval demands.

    A grade of delay d has total-prefix capacity d+1, including that block.
    Thus its remaining-candidate capacity is d. Output omits factor two.
    """
    r = len(delays)
    if not r:
        assert not demands
        return zero_weight
    states = {((0,) * r, (0,) * r): 0}
    for q in range(1, m + 1):
        following = {}
        ending = [(left, weight) for left, right, weight in demands if right == q]
        for (last, count), value in states.items():
            for grade in range(r + 1):
                new_last, new_count = list(last), list(count)
                if grade < r:
                    for j in range(grade, r):
                        new_last[j] = q
                        new_count[j] += 1
                if any(new_count[j] > delays[j] for j in range(r)):
                    continue
                new_value = value
                for left, weight in ending:
                    j = next((j for j in range(r) if new_last[j] >= left), None)
                    if j is None:
                        break
                    new_value += weight * delays[j]
                else:
                    key = (tuple(new_last), tuple(new_count))
                    following[key] = min(following.get(key, float("inf")), new_value)
        states = following
    return min(value + zero_weight * (1 + count[-1])
               for (last, count), value in states.items())


def circular_grade_cost(m, demands, delays, zero_weight):
    values = []
    for first in range(m):
        positions = {(first + q) % m: q for q in range(1, m)}
        ordinary = []
        for arc, weight in demands:
            if first in arc:
                continue
            locs = sorted(positions[q] for q in arc)
            assert locs == list(range(locs[0], locs[-1] + 1))
            ordinary.append((locs[0], locs[-1], weight))
        values.append(interval_grade_cost(m - 1, ordinary, delays, zero_weight))
    return min(values)


def circular_brute_cost(m, demands, zero_weight):
    result = None
    for order in permutations(range(m)):
        rank = {q: j + 1 for j, q in enumerate(order)}
        hits = [(min(rank[q] for q in arc), weight) for arc, weight in demands]
        final = max((time for time, _ in hits), default=1)
        value = sum((time - 1) * weight for time, weight in hits) + zero_weight * final
        result = value if result is None else min(result, value)
    return result


def endpoint_decoder(records, objective):
    """Exact coordinate-threshold decoder. Records are (L,R,mass,tail).

    Rectangle states can equivalently be keyed by their realized record set.
    Each transition is a supplied threshold in the endpoint realization.
    """
    @lru_cache(None)
    def solve(indices):
        if len(indices) == 1:
            _, _, mass, tail = records[indices[0]]
            return mass * tail if objective == "expected" else tail
        best = float("inf")
        for axis in [0, 1]:
            values = sorted({records[i][axis] for i in indices})
            for threshold in values[:-1]:
                left = tuple(i for i in indices if records[i][axis] <= threshold)
                right = tuple(i for i in indices if records[i][axis] > threshold)
                if objective == "expected":
                    cost = sum(records[i][2] for i in indices) + solve(left) + solve(right)
                else:
                    cost = 1 + max(solve(left), solve(right))
                best = min(best, cost)
        return best
    return solve(tuple(range(len(records))))


def rational_log_bounds(x, terms=220):
    assert x >= 1
    z = (x - 1) / (x + 1)
    lower = 2 * sum(z ** (2 * j + 1) / (2 * j + 1) for j in range(terms))
    upper = lower + 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, upper


def main():
    rng = Random(20261013)
    checked = 0
    for m in range(2, 7):
        for _ in range(30):
            demands = []
            for _ in range(rng.randrange(1, 9)):
                start, length = rng.randrange(m), rng.randrange(1, m + 1)
                arc = {(start + j) % m for j in range(length)}
                demands.append((arc, rng.randrange(1, 10)))
            zero = rng.randrange(0, 8)
            exact = circular_grade_cost(m, demands, list(range(1, m)), zero)
            assert exact == circular_brute_cost(m, demands, zero)
            checked += 1
    print(f"Shifted-grade circular DP agrees with exhaustive optimum on {checked} instances.")

    hull = [(4, 0), (3, 2), (2, 3), (0, 4), (-2, 3), (-3, 2),
            (-4, 0), (-3, -2), (-2, -3), (0, -4), (2, -3), (3, -2)]
    points = [(F(2, 5), 0), (F(17, 50), -F(1, 50)),
              (F(17, 50), F(1, 50)), (F(12, 25), F(3, 100)),
              (F(12, 25), -F(3, 100))]
    patterns = []
    for x, y in points:
        products = [a*x+b*y for a, b in hull]
        assert all(value != 1 for value in products)
        patterns.append(tuple(value > 1 for value in products))
    differences = [{j for j in range(len(hull)) if pattern[j] != patterns[0][j]}
                   for pattern in patterns[1:]]
    assert {frozenset(difference) for difference in differences} == {
        frozenset([1]), frozenset([2]), frozenset([10]), frozenset([11])}
    assert all(pattern[0] for pattern in patterns)
    # Endpoints around known vertex 0: move indices 10,11 to -2,-1.
    records = []
    epsilon = F(1, 10000)
    for index, pattern in enumerate(patterns):
        positive = [j if j <= 2 else j-12 for j, bit in enumerate(pattern) if bit]
        records.append((min(positive), max(positive), 1-4*epsilon if index == 0 else epsilon, 0))
    cost = endpoint_decoder(records, "expected")
    assert cost >= 4 * (1 - 4*epsilon)
    assert endpoint_decoder(records, "height") == 4
    print("Rational five-point endpoint example requires four certifications of its dominant pattern.")

    delta = F(139087, 1000000)
    coefficient = F(42967, 25000)  # 1.71868
    log_delta, _ = rational_log_bounds(1/delta)
    log_complement, _ = rational_log_bounds(1/(1-delta))
    remainder = 1-7*delta
    log_remainder, _ = rational_log_bounds(1/remainder)
    entropy_lower = delta*log_delta+(1-delta)*log_complement
    sigma_lower = 7*delta*log_delta+remainder*log_remainder
    _, ln2_upper = rational_log_bounds(F(2))
    assert coefficient*entropy_lower > ln2_upper
    assert coefficient*sigma_lower > 5*ln2_upper
    factor = 2*F(2001, 2000)+coefficient
    assert factor == F(11624, 3125)  # 3.71968
    print("Exact rational logarithm intervals certify the shifted-block expected factor 3.71968.")
    best_explicit = 2*F(100001, 100000)+coefficient
    assert best_explicit == F(37187, 10000)  # 3.71870
    print("Lambda=100001/100000 gives the certified explicit expected factor 3.71870.")
    print("For any fixed eta>0, the certified factor is 3.71868+2 eta.")


if __name__ == "__main__":
    main()
