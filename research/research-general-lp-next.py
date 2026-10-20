"""Proof audits for research-general-lp-next.md, using only the standard library.

The finite local-policy audit is deliberately exhaustive at width three. Its
runtime is not proposed as a UDT approximation algorithm.
"""

from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import ceil, log, log2


def affine_table(q, dimension):
    points = list(product(range(q), repeat=dimension))
    tests = []
    for normal in points:
        for offset in range(q):
            mask = sum(1 << i for i, h in enumerate(points)
                       if sum(a * b for a, b in zip(normal, h)) % q == offset)
            tests.append(mask)
    return points, tests


def psd_exact(matrix):
    """Exact PSD test by symmetric Schur elimination, allowing zero pivots."""
    work = [row[:] for row in matrix]
    size = len(work)
    for pivot in range(size):
        value = work[pivot][pivot]
        assert value >= 0
        if value == 0:
            assert all(work[pivot][j] == 0 for j in range(pivot + 1, size))
            continue
        for i in range(pivot + 1, size):
            for j in range(i, size):
                new_value = work[i][j] - work[i][pivot] * work[pivot][j] / value
                work[i][j] = work[j][i] = new_value


def audit_masks_and_psd(q=3, dimension=2):
    points, tests = affine_table(q, dimension)
    n, m = len(points), len(tests)
    sigma = Fraction(2 * (q - 1), q * q)
    c = 1 - sigma
    nu = [[Fraction(q if mask & (1 << h) else 1, n * (2 * q - 1))
           for mask in tests] for h in range(n)]
    assert all(sum(row) == 1 for row in nu)
    for h in range(n):
        assert sum(bool(mask & (1 << h)) for mask in tests) == m // q
        for g in range(h):
            count = sum(bool(mask & (1 << h)) == bool(mask & (1 << g))
                        for mask in tests)
            assert Fraction(count, m) == c

    for width in (2, 3):
        for time in (0, 1, 2, 5):
            z = c ** time
            r = min(Fraction(1), (width - 1) * z)
            s = 1 - r
            summed = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            following = [[Fraction(0) for _ in range(n)] for _ in range(n)]
            for test_id, mask in enumerate(tests):
                diagonal = [(r - z) / m + s * nu[h][test_id] for h in range(n)]
                assert min(diagonal) >= 0
                matrix = [[z / m + (diagonal[h] if h == g else 0)
                           for g in range(n)] for h in range(n)]
                psd_exact(matrix)
                for h in range(n):
                    for g in range(n):
                        summed[h][g] += matrix[h][g]
                        if bool(mask & (1 << h)) == bool(mask & (1 << g)):
                            following[h][g] += matrix[h][g]
            for h in range(n):
                for g in range(n):
                    assert summed[h][g] == (1 if h == g else z)
                    assert following[h][g] == (1 if h == g else c * z)
    print(f"Affine F_{q}^{dimension}: exact coincidence and PSD identities passed")
    return points, tests, nu, float(c), float(sigma)


def audit_local_flows(points, tests, nu_exact, c, width=3, switch=5, tail=6):
    n, m = len(points), len(tests)
    nu = [[float(value) for value in row] for row in nu_exact]
    all_mask = (1 << n) - 1
    checked_sets = 0
    max_error = 0.0
    for local_size in range(1, width + 1):
        for members in combinations(range(n), local_size):
            checked_sets += 1
            population = sum(1 << h for h in members)
            states = {population: 1.0}
            pairs = list(combinations(members, 2))
            for time in range(switch + tail):
                z = c ** time
                r = min(1.0, (width - 1) * z)
                s = 1.0 - r
                if time >= switch:
                    # Remove the same per-hypothesis stopping mass in each U.
                    for h in members:
                        arrival = sum(mass for state, mass in states.items()
                                      if state & (1 << h))
                        stop = arrival - r
                        singleton = states.get(1 << h, 0.0)
                        assert stop >= -1e-10
                        assert singleton + 1e-10 >= stop
                        states[1 << h] = max(0.0, singleton - stop)

                x = {h: [0.0] * m for h in members}
                common = {pair: [0.0] * m for pair in pairs}
                next_states = {}
                for state, mass in states.items():
                    if mass < 1e-15:
                        continue
                    inside = [h for h in members if state & (1 << h)]
                    singleton = state.bit_count() == 1
                    if singleton and time < switch:
                        h = inside[0]
                        assert mass + 1e-10 >= s
                        query = [(mass - s) / m + s * nu[h][j] for j in range(m)]
                    else:
                        query = [mass / m] * m
                    for j, amount in enumerate(query):
                        assert amount >= -1e-12
                        for h in inside:
                            x[h][j] += amount
                        for pair in combinations(inside, 2):
                            common[pair][j] += amount
                        positive = state & tests[j]
                        negative = state & (all_mask ^ tests[j])
                        for child in (positive, negative):
                            if child:
                                next_states[child] = next_states.get(child, 0.0) + amount

                for h in members:
                    for j in range(m):
                        expected = r / m + s * nu[h][j] if time < switch else r / m
                        max_error = max(max_error, abs(x[h][j] - expected))
                for pair in pairs:
                    pair_arrival = sum(mass for state, mass in states.items()
                                       if all(state & (1 << h) for h in pair))
                    max_error = max(max_error, abs(pair_arrival - z))
                    for value in common[pair]:
                        max_error = max(max_error, abs(value - z / m))
                states = next_states
    assert max_error < 1e-9
    print(f"All {checked_sets} local sets of width <= {width}: synchronized "
          f"x,a,z and stopping passed; max error={max_error:.3g}")


def audit_entropy(points, tests, q=3):
    n, m = len(points), len(tests)
    minimum_slack = float("inf")
    for subset in range(1, 1 << n):
        size = subset.bit_count()
        if size < 2:
            continue
        total = 0.0
        for mask in tests:
            positive = (mask & subset).bit_count()
            negative = size - positive
            a = positive * (64 * q * q / m)
            b = negative * (64 * q / m)
            if a and b:
                total += (a + b) * log(a + b) - a * log(a) - b * log(b)
        minimum_slack = min(minimum_slack, total - size * log(size))
    assert minimum_slack >= -1e-9
    print(f"All {2**n-n-1} nontrivial subset-entropy demands passed; "
          f"minimum slack={minimum_slack:.4g}")


def audit_parameters():
    for q in (127, 1009, 100003):
        dimension = int(q / log(q))
        n = q ** dimension
        width = 3
        sigma = 2 * (q - 1) / (q * q)
        c = 1 - sigma
        tq = ceil(log(width - 1) / sigma) + 2
        budget = 64 * (2 * q - 1)
        switch = tq + budget + ceil(1 / sigma) + ceil(dimension * log2(q))
        finish = max(switch, ceil((dimension * log(q) + log(width - 1)) / sigma) + 2)
        height = dimension * (q - 1)
        assert log(width - 1) + tq * log(c) <= 0
        assert log(width - 1) + finish * log(c) <= -dimension * log(q)
        assert finish + height < n - 1
        assert switch >= dimension * log2(q)
        assert switch - tq - 1 / sigma >= budget
        print(f"Q={q}, d={dimension}: horizon and entropy-reservation budgets passed; "
              f"n has {n.bit_length()} bits")


def audit_completion_dual():
    instances = [
        (4, [0b1100, 0b1010]),
        (5, [1 << h for h in range(5)]),
        (6, [0b000111, 0b001001, 0b010010, 0b100100,
             0b001010, 0b010100, 0b100001]),
    ]
    checked = 0
    for n, tests in instances:
        full = (1 << n) - 1

        @lru_cache(None)
        def optimum(state):
            if state.bit_count() <= 1:
                return 0, None
            choices = []
            for test in tests:
                left, right = state & test, state & (full ^ test)
                if left and right:
                    choices.append((state.bit_count() + optimum(left)[0] + optimum(right)[0],
                                    test))
            return min(choices)

        depths = [0] * n

        def trace(state, depth):
            if state.bit_count() == 1:
                depths[state.bit_length() - 1] = depth
                return
            test = optimum(state)[1]
            trace(state & test, depth + 1)
            trace(state & (full ^ test), depth + 1)

        trace(full, 0)

        @lru_cache(None)
        def partials(state):
            if state.bit_count() == 1:
                return {state: 0}
            answer = {0: 0}
            for test in tests:
                left, right = state & test, state & (full ^ test)
                if not left or not right:
                    continue
                for covered_l, work_l in partials(left).items():
                    for covered_r, work_r in partials(right).items():
                        covered = covered_l | covered_r
                        work = state.bit_count() + work_l + work_r
                        answer[covered] = min(answer.get(covered, work), work)
            return answer

        for covered, work in partials(full).items():
            reward = sum(depths[h] for h in range(n) if covered & (1 << h))
            assert reward <= work
            if n in (4, 5):
                # These two instances are hypothesis-transitive: average the
                # depth dual to the constant optimum/n and check (17).
                assert n * work >= optimum(full)[0] * covered.bit_count()
            checked += 1
        assert partials(full)[full] == optimum(full)[0] == sum(depths)
    print(f"Completion-cover exact dual audited on {checked} partial-policy cover patterns")


if __name__ == "__main__":
    points, tests, nu, c, sigma = audit_masks_and_psd()
    audit_local_flows(points, tests, nu, c)
    audit_entropy(points, tests)
    audit_parameters()
    audit_completion_dual()
    print("All query-synchronized LP/SDP and pricing audits passed.")
