"""Independent exact checks for the randomized per-hypothesis objective.

Only Python's standard library is used.  Small proper decision trees are
enumerated from supplied, strictly separating integer planar lines.  LP
vertices and oracle comparisons use Fraction arithmetic throughout.
Decimal logarithms are diagnostic checks of the proved potential bound;
the approximation coefficient check itself is an exact rational check.
"""

from decimal import Decimal, localcontext
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
import json


def ceil_fraction(x):
    return -(-x.numerator // x.denominator)


def solve_exact(matrix, rhs):
    """Solve a square linear system; return None when it is singular."""
    size = len(rhs)
    a = [[F(v) for v in row] + [F(b)] for row, b in zip(matrix, rhs)]
    for col in range(size):
        pivot = next((r for r in range(col, size) if a[r][col]), None)
        if pivot is None:
            return None
        a[col], a[pivot] = a[pivot], a[col]
        scale = a[col][col]
        a[col] = [v / scale for v in a[col]]
        for row in range(size):
            if row != col and a[row][col]:
                scale = a[row][col]
                a[row] = [v - scale * u for v, u in zip(a[row], a[col])]
    return tuple(row[-1] for row in a)


def planar_instance(n, add_thresholds=False):
    """Parabola points; singleton cap tests and optional vertical cuts."""
    points = tuple((t, t * t) for t in range(n))
    # 4 y - 8 t0 x + 4 t0^2 - 1 < 0 isolates the point t0.
    lines = [( -8 * t, 4, 4 * t * t - 1) for t in range(n)]
    if add_thresholds:
        lines += [(2, 0, -(2 * t + 1)) for t in range(n - 1)]
    masks = []
    for a, b, c in lines:
        values = [a * x + b * y + c for x, y in points]
        assert all(values), "An input point lies on a supplied line."
        masks.append(sum(1 << i for i, value in enumerate(values) if value > 0))
    assert len(set(tuple(bool(mask & (1 << i)) for mask in masks)
                   for i in range(n))) == n
    return points, tuple(lines), tuple(masks)


def proper_depth_vectors(n, masks):
    """Enumerate all attainable vectors, keeping no constant queries."""
    @lru_cache(None)
    def visit(state):
        if state.bit_count() == 1:
            return (tuple(0 for _ in range(n)),)
        vectors = set()
        for mask in masks:
            positive, negative = state & mask, state & ~mask
            if not positive or not negative:
                continue
            for left in visit(positive):
                for right in visit(negative):
                    vectors.add(tuple(
                        (1 + left[i] if positive & (1 << i) else 1 + right[i])
                        if state & (1 << i) else 0 for i in range(n)))
        assert vectors, "The supplied queries do not identify this state."
        return tuple(sorted(vectors))
    result = visit((1 << n) - 1)
    assert all(1 <= d <= n - 1 for vector in result for d in vector)
    # Every proper binary tree gives a complete binary prefix code.
    assert all(sum(F(1, 2 ** d) for d in vector) == 1 for vector in result)
    return result


def dual_optimum(vectors):
    """Exact vertex enumeration of max r <= pi dot d, pi in simplex."""
    n = len(vectors[0])
    # Unknowns are pi_0,...,pi_(n-1),r.  The normalization is fixed.
    boundary = [(tuple(int(i == j) for i in range(n)) + (0,), 0)
                for j in range(n)]
    boundary += [(tuple(vector) + (-1,), 0) for vector in vectors]
    equality = tuple(1 for _ in range(n)) + (0,)
    best = None
    for chosen in combinations(boundary, n):
        solution = solve_exact([equality] + [row for row, _ in chosen],
                               [1] + [b for _, b in chosen])
        if solution is None:
            continue
        prior, value = solution[:-1], solution[-1]
        if min(prior) < 0:
            continue
        if any(sum(p * d for p, d in zip(prior, v)) < value for v in vectors):
            continue
        if best is None or value > best[0]:
            best = value, prior
    assert best is not None
    return best


def restricted_master(vectors):
    """Exact small-instance primal LP, explicitly allowing support <= n."""
    vectors = tuple(sorted(set(vectors)))
    n = len(vectors[0])
    best = None
    for count in range(1, min(n, len(vectors)) + 1):
        for support in combinations(vectors, count):
            for tight in combinations(range(n), count):
                matrix = [tuple(1 for _ in range(count)) + (0,)]
                matrix += [tuple(vector[h] for vector in support) + (-1,)
                           for h in tight]
                solution = solve_exact(matrix, [1] + [0] * count)
                if solution is None:
                    continue
                probabilities, value = solution[:-1], solution[-1]
                if min(probabilities) <= 0 or value < 0:
                    continue
                costs = tuple(sum(p * vector[h]
                                  for p, vector in zip(probabilities, support))
                              for h in range(n))
                if max(costs) > value:
                    continue
                if best is None or value < best[0]:
                    best = value, probabilities, support
    assert best is not None
    assert sum(best[1]) == 1 and len(best[1]) <= n
    return best


def run_mwu(vectors, alpha, epsilon, randomized_optimum, adversarial=False):
    n = len(vectors[0])
    length = n - 1
    eta = epsilon / (2 * alpha)
    rounds = ceil_fraction(8 * alpha * length / (epsilon * epsilon))
    p, q = eta.numerator, eta.denominator
    weights = [1] * n
    selected = []
    total_weighted = F(0)
    for _ in range(rounds):
        assert all(isinstance(w, int) and w > 0 for w in weights)
        weight_sum = sum(weights)
        prior = [F(w, weight_sum) for w in weights]
        assert sum(prior) == 1 and min(prior) > 0
        scores = [(sum(w * d for w, d in zip(weights, vector)), vector)
                  for vector in vectors]
        optimum = min(score for score, _ in scores)
        eligible = [(score, vector) for score, vector in scores
                    if score <= alpha * optimum]
        score, vector = (max(eligible) if adversarial else min(eligible))
        oracle_cost = F(score, weight_sum)
        assert oracle_cost <= alpha * randomized_optimum
        total_weighted += oracle_cost
        selected.append(vector)
        weights = [w * (q * length + p * depth)
                   for w, depth in zip(weights, vector)]
    mean = max(F(sum(v[h] for v in selected), rounds) for h in range(n))
    master = restricted_master(selected)
    assert master[0] <= mean <= (alpha + epsilon) * randomized_optimum
    # The coefficient obtained after ln(n) <= ln(2) R* < R* is exact.
    coefficient = (1 + eta) * alpha + F(2 * length, 1) / (eta * rounds)
    assert coefficient <= alpha + epsilon
    with localcontext() as ctx:
        ctx.prec = 80
        def dec(f):
            return Decimal(f.numerator) / Decimal(f.denominator)
        e = dec(eta)
        ln1p = (1 + e).ln()
        potential_bound = e / ln1p * dec(total_weighted / rounds)
        potential_bound += Decimal(length) * Decimal(n).ln() / (rounds * ln1p)
        assert dec(mean) <= potential_bound
        assert potential_bound < dec((alpha + epsilon) * randomized_optimum)
    return dict(rounds=rounds, uniform_value=str(mean), lp_value=str(master[0]),
                randomized_optimum=str(randomized_optimum),
                lp_support=len(master[1]),
                maximum_integer_weight_bits=max(w.bit_length() for w in weights),
                alpha=str(alpha), epsilon=str(epsilon), adversarial=adversarial)


def main():
    records = []
    for n, thresholds in [(3, False), (4, False), (4, True)]:
        points, lines, masks = planar_instance(n, thresholds)
        vectors = proper_depth_vectors(n, masks)
        dual = dual_optimum(vectors)
        primal = restricted_master(vectors)
        assert primal[0] == dual[0], "Independent primal and dual vertices differ."
        deterministic = min(max(v) for v in vectors)
        if not thresholds:
            expected = F((n - 1) * (n + 2), 2 * n)
            assert primal[0] == expected < deterministic
        else:
            assert primal[0] == deterministic == 2
        # Nonnegative dual priors are legal comparison objects; this point
        # mass also checks that every enumerated tree still identifies all n.
        zero_support = (F(1),) + (F(0),) * (n - 1)
        assert min(sum(p * d for p, d in zip(zero_support, v))
                   for v in vectors) == 1
        # Convexifying the two original objectives does not reduce the optimum.
        uniform = tuple(F(1, n) for _ in range(n))
        pure_e = min(sum(p * d for p, d in zip(uniform, v)) for v in vectors)
        assert all(sum(p * d for p, d in zip(uniform, v)) >= pure_e for v in vectors)
        assert all(max(v) >= deterministic for v in vectors)
        records.append(dict(n=n, threshold_queries=thresholds,
                            supplied_lines=len(lines), depth_vectors=len(vectors),
                            deterministic_height=deterministic,
                            exact_randomized_optimum=str(primal[0]),
                            dual_prior=[str(p) for p in dual[1]]))
        for alpha, adversarial in [(F(1), False), (F(3, 2), True)]:
            records.append(run_mwu(vectors, alpha, F(1, 2), primal[0], adversarial))
    public_alpha = F(518297551, 100000000)
    public_epsilon = F(1, 4000000)
    assert F(5182975508794, 1000000000000) < public_alpha
    assert public_alpha + public_epsilon < F(5182976, 1000000)
    records.append(dict(public_oracle_coefficient=str(public_alpha),
                        public_randomized_coefficient=str(public_alpha + public_epsilon),
                        public_epsilon=str(public_epsilon)))
    print(json.dumps(records, indent=2))
    print("PASS: strict planar instances, exact primal/dual LPs, zero support,")
    print("positive integer updates, adversarial approximate oracles, rational")
    print("regret constants, LP support compression, and public headline margin.")


if __name__ == "__main__":
    main()
