"""Discover a matroid history certificate from explicit response-cell families.

Recognition and discovery are polynomial.  Exhaustive subset checks below
are finite audits, not the proposed recognition or coding computation.
"""

from functools import lru_cache
from fractions import Fraction
from itertools import combinations, product
from pathlib import Path
import json
import random


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit
        mask ^= bit


class HyperplaneMatroid:
    def __init__(self, n, hyperplanes):
        self.n, self.full = n, (1 << n)-1
        self.hyperplanes = tuple(sorted(set(hyperplanes)))

    def validate(self):
        hs, full = self.hyperplanes, self.full
        if not hs or any(h == full or h & ~full for h in hs):
            return False
        if any(a & b == a or a & b == b for a, b in combinations(hs, 2)):
            return False
        for a, b in combinations(hs, 2):
            common = a & b
            for x in bits(full & ~(a | b)):
                required = common | x
                if not any(required & h == required for h in hs):
                    return False
        # Loops would invalidate the rank-minus-one positive-budget convention.
        return self.closure(0) == 0

    @lru_cache(None)
    def closure(self, selected):
        result = self.full
        for hyperplane in self.hyperplanes:
            if selected & hyperplane == selected:
                result &= hyperplane
        return result

    @lru_cache(None)
    def rank(self, selected):
        basis, closed, rank = 0, self.closure(0), 0
        for bit in bits(selected):
            if not (closed & bit):
                basis |= bit
                rank += 1
                closed = self.closure(basis)
        return rank

    def orientations(self, tests):
        positive = []
        for test in tests:
            choices = [cell for cell in (test, self.full ^ test)
                       if self.closure(cell) == cell]
            if not choices:
                return None
            positive.append(min(choices, key=lambda cell: (cell.bit_count(), cell)))
        return tuple(positive)

    def default_responses(self, partitions):
        """Every response except one must be a flat; returns default indices."""
        defaults = []
        for cells in partitions:
            union = 0
            for cell in cells:
                if cell & union or cell & ~self.full:
                    raise ValueError("Response cells do not form a partition")
                union |= cell
            if union != self.full:
                raise ValueError("Response cells do not cover the ground set")
            nonflats = [a for a, cell in enumerate(cells) if self.closure(cell) != cell]
            if len(nonflats) > 1:
                return None
            defaults.append(nonflats[0] if nonflats else
                            max(range(len(cells)), key=lambda a: cells[a].bit_count()))
        return tuple(defaults)


def discover(n, tests):
    """Try all cardinality classes of original response cells; no subset search."""
    full = (1 << n)-1
    assert len({tuple(bool(test & h) for test in tests) for h in bits(full)}) == n
    families = {}
    for test in tests:
        for cell in (test, full ^ test):
            if cell and cell != full:
                families.setdefault(cell.bit_count(), set()).add(cell)
    candidates = []
    for size, family in sorted(families.items()):
        matroid = HyperplaneMatroid(n, family)
        if not matroid.validate():
            continue
        positive = matroid.orientations(tests)
        if positive is not None:
            candidates.append((matroid.rank(full), size, matroid, positive))
    if not candidates:
        return None
    _, _, matroid, positive = min(candidates, key=lambda item: item[:2])
    return matroid, positive, len(families)


def coding_table(n, maximum_budget):
    """The already established rank-limited code recurrence, exact integers."""
    table = [[0, 0]+[None]*(n-1)]
    for budget in range(1, maximum_budget+1):
        row = [0, 0]+[None]*(n-1)
        for size in range(2, n+1):
            row[size] = size+min(table[budget-1][a]+row[size-a]
                                for a in range(1, size)
                                if table[budget-1][a] is not None)
        table.append(row)
    return table


def coding_table_responses(n, maximum_budget, responses):
    """One default branch and at most responses-1 budget-decreasing branches.

    Min-plus convolution tracks the number of nonempty positive branches,
    truncated at two. This excludes a constant query when the default is empty.
    Complexity O(responses * maximum_budget * n**2), exact integers.
    """
    assert responses >= 2
    table = [[0, 0]+[None]*(n-1)]
    for budget in range(1, maximum_budget+1):
        positive = {(0, 0): 0}
        for _ in range(responses-1):
            extended = {}
            for (size, count), value in positive.items():
                for amount in range(n-size+1):
                    entry = table[budget-1][amount]
                    if entry is None:
                        continue
                    key = size+amount, min(2, count+bool(amount))
                    extended[key] = min(extended.get(key, value+entry), value+entry)
            positive = extended
        row = [0, 0]+[None]*(n-1)
        for size in range(2, n+1):
            choices = []
            for default_size in range(size):
                for count in range(1 if default_size else 2, 3):
                    entry = positive.get((size-default_size, count))
                    if entry is not None and row[default_size] is not None:
                        choices.append(row[default_size]+entry)
            if choices:
                row[size] = size+min(choices)
        table.append(row)
    return table


def affine_tests(q, dimension):
    # Prime q only in this finite checker.
    points = tuple(product(range(q), repeat=dimension))
    tests = sorted(set(sum(1 << h for h, point in enumerate(points)
                           if sum(a*x for a, x in zip(normal, point)) % q == value)
                       for normal in product(range(q), repeat=dimension)
                       if any(normal) for value in range(q)))
    return points, tuple(tests)


def greedy_cost(n, tests):
    @lru_cache(None)
    def solve(state):
        if state.bit_count() <= 1:
            return 0
        _, chosen = min((max((state & test).bit_count(), (state & ~test).bit_count()), q)
                        for q, test in enumerate(tests) if state & test and state & ~test)
        return state.bit_count()+solve(state & tests[chosen])+solve(state & ~tests[chosen])
    return solve((1 << n)-1)


def main():
    rng = random.Random(2026101901)
    closure_checks = budget_checks = bellman_checks = negative_drops = 0
    examples = []
    for q, dimension in ((2, 2), (2, 3), (3, 2), (3, 3), (5, 2)):
        points, tests = affine_tests(q, dimension)
        n = len(points)
        tests = tests+tuple(1 << h for h in range(n))  # Literal response rank is n.
        result = discover(n, tests)
        assert result is not None
        matroid, positive, family_count = result
        rank = matroid.rank(matroid.full)
        assert rank == dimension+1
        table = coding_table(n, rank-1)
        lower = table[rank-1][n]
        upper = greedy_cost(n, tests)
        assert lower <= upper
        # Constant a-posteriori certificate; the asymptotic recurrence is not inferred here.
        examples.append({"q": q, "dimension": dimension, "n": n, "physical_tests": len(tests),
                         "cardinality_families_tried": family_count,
                         "discovered_rank": rank, "positive_budget": rank-1,
                         "coding_lower_raw": lower, "greedy_upper_raw": upper,
                         "certified_greedy_ratio": str(Fraction(upper, lower)),
                         "singleton_noise_makes_literal_rank": n})
        selected_states = (range(1 << n) if n <= 9 else
                           [rng.randrange(1 << n) for _ in range(100)])
        for state in selected_states:
            assert matroid.closure(matroid.closure(state)) == matroid.closure(state)
            closure_checks += 1
            if state.bit_count() <= 1:
                continue
            state_rank = matroid.rank(state)
            value = table[state_rank-1][state.bit_count()]
            assert value is not None
            for cell in positive:
                hit, miss = state & cell, state & ~cell
                if not hit or not miss:
                    continue
                assert matroid.rank(hit) < state_rank
                assert matroid.rank(miss) <= state_rank
                budget_checks += 1
                left = table[matroid.rank(hit)-1][hit.bit_count()]
                right = table[matroid.rank(miss)-1][miss.bit_count()]
                drop = value-left-right
                assert drop <= state.bit_count()
                negative_drops += drop < 0
                bellman_checks += 1

    # A non-flat response invalidates the strong affine certificate, but the
    # singleton-complement class can still give the weak free-matroid one.
    _, tests = affine_tests(3, 2)
    n = 9
    noisy = tests+tuple(1 << h for h in range(n))+(15,)
    result = discover(n, noisy)
    assert result is not None and result[0].rank((1 << n)-1) == n
    assert not HyperplaneMatroid(4, (3, 5, 10, 12)).validate()

    # A near-pencil: U_(2,8) direct-sum one independent point.  Its line
    # response is a flat, but conditioning on it activates MORE coding work.
    # This is an explicit warning against clipping negative potential drops.
    line, outside = (1 << 8)-1, 1 << 8
    pencil = HyperplaneMatroid(9, (line,)+tuple(outside | (1 << h) for h in range(8)))
    assert pencil.validate() and pencil.rank(pencil.full) == 3
    pencil_table = coding_table(9, 2)
    pencil_root = pencil_table[2][9]
    pencil_line = pencil_table[1][8]
    assert (pencil_root, pencil_line, pencil_root-pencil_line) == (30, 35, -5)

    # Exhaustive closure exchange audit on accepted small families.
    exchange_checks, accepted = 0, 0
    for n in (3, 4):
        proper = list(range(1, (1 << n)-1))
        for _ in range(100):
            family = rng.sample(proper, rng.randrange(1, len(proper)+1))
            matroid = HyperplaneMatroid(n, family)
            if not matroid.validate():
                continue
            accepted += 1
            for state in range(1 << n):
                closed = matroid.closure(state)
                for x in bits(matroid.full & ~closed):
                    for y in bits(matroid.closure(state | x) & ~closed):
                        assert matroid.closure(state | y) & x
                        exchange_checks += 1

    response_checks, response_examples = 0, []
    assert coding_table_responses(12, 5, 2) == coding_table(12, 5)
    for dimension in (1, 2, 3):
        points = tuple(product(range(3), repeat=dimension))
        n = len(points)
        normals = [normal for normal in product(range(3), repeat=dimension)
                   if any(normal) and next(a for a in normal if a) == 1]
        partitions = [tuple(sum(1 << h for h, point in enumerate(points)
                                if sum(a*x for a, x in zip(normal, point)) % 3 == value)
                            for value in range(3)) for normal in normals]
        family = {cell for cells in partitions for cell in cells}
        matroid = HyperplaneMatroid(n, family)
        assert matroid.validate() and matroid.rank(matroid.full) == dimension+1
        defaults = matroid.default_responses(partitions)
        assert defaults is not None
        table = coding_table_responses(n, dimension, 3)
        assert table[dimension][n] == dimension*n
        states = range(1 << n) if n <= 9 else [rng.randrange(1 << n) for _ in range(100)]
        for state in states:
            if state.bit_count() <= 1:
                continue
            parent = table[matroid.rank(state)-1][state.bit_count()]
            for cells, default in zip(partitions, defaults):
                child_value = 0
                nonempty = sum(bool(state & cell) for cell in cells)
                if nonempty < 2:
                    continue
                for response, cell in enumerate(cells):
                    selected = state & cell
                    if selected:
                        child_value += table[matroid.rank(selected)-1][selected.bit_count()]
                        if response != default:
                            assert matroid.rank(selected) < matroid.rank(state)
                assert parent-child_value <= state.bit_count()
                response_checks += 1
        response_examples.append({"responses": 3, "dimension": dimension, "n": n,
                                  "discovered_rank": dimension+1,
                                  "coding_lower_and_exact_OPT": dimension*n})
        if dimension == 2:
            assert matroid.default_responses([(15, 240, 256)]) is None

    output = {"status": "passed", "affine_discovery_examples": examples,
              "closure_idempotence_checks": closure_checks,
              "actual_subset_positive_rank_drop_checks": budget_checks,
              "rank_coding_Bellman_checks": bellman_checks,
              "negative_Bellman_drops_retained": negative_drops,
              "accepted_small_hyperplane_families": accepted,
              "small_closure_exchange_checks": exchange_checks,
              "constant_response_extension_examples": response_examples,
              "multiresponse_rank_and_Bellman_checks": response_checks,
              "binary_convolution_matches_existing_recurrence": True,
              "two_nonflat_response_decoy_rejected": True,
              "nonflat_decoy_rejects_strong_affine_certificate": True,
              "negative_drop_witness": {"matroid": "U_(2,8) direct-sum U_(1,1)",
                                        "root_potential": pencil_root,
                                        "line_child_potential": pencil_line,
                                        "other_child_potential": 0,
                                        "signed_query_drop": pencil_root-pencil_line},
              "discovery_has_no_exponential_oracle": True,
              "exhaustive_subsets_are_validation_only": True,
              "no_unrestricted_approximation_claim": True}
    Path("research-general-matroid-discovery-results.json").write_text(
        json.dumps(output, indent=2), encoding="utf-8")
    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()
