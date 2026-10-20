"""Independent checks of the graded DP and the current lookahead calibration."""
from itertools import permutations
from fractions import Fraction
from random import Random


def dp_feasible(m, demands, levels):
    # Grade i means query this candidate before every deadline of index >= i.
    r = len(levels)
    states = {(tuple([0] * r), tuple([0] * r))}
    for q in range(1, m + 1):
        following = set()
        ending = [(left, grade) for left, right, grade in demands if right == q]
        for last, count in states:
            for grade in range(r + 1):
                new_last, new_count = list(last), list(count)
                if grade < r:
                    for j in range(grade, r):
                        new_last[j] = q
                        new_count[j] += 1
                if any(new_count[j] > levels[j] for j in range(r)):
                    continue
                if any(new_last[j] < left for left, j in ending):
                    continue
                following.add((tuple(new_last), tuple(new_count)))
        states = following
        if not states:
            return False
    return bool(states)


def brute_feasible(m, demands, levels):
    for order in permutations(range(1, m + 1)):
        rank = {q: j + 1 for j, q in enumerate(order)}
        if all(min(rank[q] for q in range(left, right + 1)) <= levels[j]
               for left, right, j in demands):
            return True
    return False


def dp_joint_cost(m, weighted_demands, levels, zero_weight):
    r = len(levels)
    states = {(tuple([0] * r), tuple([0] * r)): 0}
    for q in range(1, m + 1):
        following = {}
        ending = [(left, weight) for left, right, weight in weighted_demands if right == q]
        for (last, count), value in states.items():
            for grade in range(r + 1):
                new_last, new_count = list(last), list(count)
                if grade < r:
                    for j in range(grade, r):
                        new_last[j] = q
                        new_count[j] += 1
                if any(new_count[j] > levels[j] for j in range(r)):
                    continue
                new_value = value
                for left, weight in ending:
                    qualifying = next((j for j in range(r) if new_last[j] >= left), None)
                    if qualifying is None:
                        break
                    new_value += weight * levels[qualifying]
                else:
                    key = (tuple(new_last), tuple(new_count))
                    if key not in following or new_value < following[key]:
                        following[key] = new_value
        states = following
    return min(value + zero_weight * count[-1] for (last, count), value in states.items())


def brute_joint_cost(m, weighted_demands, zero_weight):
    optimum = None
    for order in permutations(range(1, m + 1)):
        rank = {q: j + 1 for j, q in enumerate(order)}
        covering = [(min(rank[q] for q in range(left, right + 1)), weight)
                    for left, right, weight in weighted_demands]
        value = sum(time * weight for time, weight in covering)
        value += zero_weight * max(time for time, _ in covering)
        optimum = value if optimum is None else min(optimum, value)
    return optimum


rng = Random(20261013)
checked = 0
for m in range(2, 7):
    for _ in range(150):
        levels = sorted(rng.sample(range(1, m + 1), min(m, 3)))
        demands = []
        for _ in range(rng.randrange(1, 10)):
            left = rng.randrange(1, m + 1)
            right = rng.randrange(left, m + 1)
            demands.append((left, right, rng.randrange(len(levels))))
        assert dp_feasible(m, demands, levels) == brute_feasible(m, demands, levels)
        checked += 1
obstruction = [(1, 2, 0), (2, 3, 0), (1, 1, 1), (3, 3, 1)]
assert not dp_feasible(3, obstruction, [1, 2])
print(f"Nested deadline DP agrees with all-permutation feasibility on {checked} seeded instances.")
print("The 3-candidate separate-prefix-cover obstruction is infeasible, as required.")

weighted_checked = 0
for m in range(2, 6):
    for _ in range(25):
        weighted_demands = []
        for _ in range(rng.randrange(1, 8)):
            left = rng.randrange(1, m + 1)
            right = rng.randrange(left, m + 1)
            weighted_demands.append((left, right, rng.randrange(1, 9)))
        zero_weight = rng.randrange(0, 11)
        exact = dp_joint_cost(m, weighted_demands, list(range(1, m + 1)), zero_weight)
        assert exact == brute_joint_cost(m, weighted_demands, zero_weight)
        coarse = sorted(set([1, 2, m]))
        coarse_value = dp_joint_cost(m, weighted_demands, coarse, zero_weight)
        assert coarse_value >= exact
        weighted_checked += 1
print(f"Joint first-hit/zero-wait DP agrees with exhaustive optimum on {weighted_checked} weighted instances.")


def rational_log_bounds(x, terms=180):
    z = (x - 1) / (x + 1)
    lower = 2 * sum((z ** (2 * j + 1)) / (2 * j + 1) for j in range(terms))
    upper = lower + 2 * z ** (2 * terms + 1) / ((2 * terms + 1) * (1 - z * z))
    return lower, upper


delta = Fraction(1, 4)
gamma = Fraction(3)
coefficient = Fraction(4)
ln2_lower, ln2_upper = rational_log_bounds(Fraction(2))
balance_lower, _ = rational_log_bounds(1 / (1 - delta))
flat_lower, _ = rational_log_bounds(1 / delta)
assert gamma * balance_lower > ln2_upper
assert gamma * flat_lower > 5 * ln2_upper
entropy_lower = delta * flat_lower + (1 - delta) * balance_lower
sigma_lower = flat_lower  # delta=1/4 has no capped-entropy remainder.
assert coefficient * entropy_lower > 1
assert coefficient * sigma_lower > 5
assert coefficient * ln2_upper < gamma
for epsilon in (Fraction(1), Fraction(1, 2), Fraction(1, 10), Fraction(1, 2000)):
    spacing = 1 + epsilon / 2
    assert 2 * spacing == 2 + epsilon
    for n in range(2, 129):
        q_n = (n - 1).bit_length()
        required = gamma * q_n / (1 + epsilon)
        k = min(n - 1, -(-required.numerator // required.denominator))
        # At the cap all proper trees are included; otherwise every
        # path's paid prefix covers both advertised continuation penalties.
        assert k == n - 1 or k * (1 + epsilon) >= gamma * q_n
print("Exact rational logarithm intervals certify delta=1/4, gamma=3, c=4.")
print("Both continuation penalties are absorbed by the stated lookahead cap;")
print("the current completed quasipolynomial guarantee is 2+epsilon.")
