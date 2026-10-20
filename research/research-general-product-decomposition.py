"""Exact polynomial Cartesian factorization via empirical entropy cuts.

Queyranne comparisons use integer cell-count products, never floating logs.
Exhaustive cuts and exact decision-tree DP appear only in finite validation.
"""

from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from math import prod
from pathlib import Path
import importlib.util
import json
import random
import sys


class EntropyCuts:
    def __init__(self, words, width):
        self.words, self.width = tuple(words), width
        self.n = len(self.words)
        assert self.n and len(set(self.words)) == self.n
        assert all(0 <= word < (1 << width) for word in self.words)
        self.calls = 0

    @lru_cache(None)
    def count_product(self, mask):
        counts = Counter(word & mask for word in self.words)
        return prod(count**count for count in counts.values())

    def score(self, subset, universe):
        """Larger score means smaller mutual information across the cut."""
        self.calls += 1
        assert subset & universe == subset
        return self.count_product(subset)*self.count_product(universe ^ subset)

    def zero_score(self, universe):
        return self.n**self.n*self.count_product(universe)

    def minimum_cut(self, universe):
        """Queyranne maximum-adjacency contractions: O(width**3) calls."""
        blocks = [1 << q for q in range(self.width) if universe >> q & 1]
        assert len(blocks) >= 2
        best = blocks[0]
        best_score = self.score(best, universe)
        while len(blocks) > 1:
            order, remaining = [blocks[0]], blocks[1:]
            joined = order[0]
            while remaining:
                # f(joined+v)-f(v) = log(score(v)/score(joined+v))/n.
                chosen = min(remaining, key=lambda block: (
                    Fraction(self.score(block, universe),
                             self.score(joined | block, universe)), block))
                order.append(chosen)
                remaining.remove(chosen)
                joined |= chosen
            penultimate, last = order[-2:]
            candidate_score = self.score(last, universe)
            if candidate_score > best_score:
                best, best_score = last, candidate_score
            blocks = [block for block in blocks if block not in (penultimate, last)]
            blocks.append(penultimate | last)
        assert best and best != universe
        assert best_score <= self.zero_score(universe)
        return best, best_score

    def factorize(self):
        factors, pending = [], [(1 << self.width)-1]
        while pending:
            universe = pending.pop()
            if universe.bit_count() <= 1:
                if universe:
                    factors.append(universe)
                continue
            cut, score = self.minimum_cut(universe)
            if score == self.zero_score(universe):
                pending.extend((cut, universe ^ cut))
            else:
                factors.append(universe)
        factors.sort(key=lambda mask: (mask & -mask, mask))
        sizes = [len({word & mask for word in self.words}) for mask in factors]
        assert prod(sizes) == self.n
        # Uniform marginal factors are essential to the UDT cost transfer.
        for mask, size in zip(factors, sizes):
            assert set(Counter(word & mask for word in self.words).values()) == {self.n//size}
        return tuple(factors), tuple(sizes)


def execute_factor_greedy(words, factors):
    """Return a legal original-query tree as state->query map and raw work."""
    n = len(words)
    width = max((mask.bit_length() for mask in factors), default=0)
    tests = [sum(1 << h for h, word in enumerate(words) if word >> q & 1)
             for q in range(width)]
    full = (1 << n)-1
    choices, pending, work = {}, [(full, 0)], 0
    while pending:
        state, first_factor = pending.pop()
        chosen = None
        for factor_id in range(first_factor, len(factors)):
            options = []
            for q in range(width):
                if factors[factor_id] >> q & 1:
                    hit = state & tests[q]
                    if hit and hit != state:
                        options.append((max(hit.bit_count(), (state ^ hit).bit_count()), q))
            if options:
                chosen = min(options)[1]
                break
        choices[state] = chosen
        if chosen is None:
            assert state.bit_count() == 1
            continue
        hit = state & tests[chosen]
        work += state.bit_count()
        pending.extend(((hit, factor_id), (state ^ hit, factor_id)))
    actual_work = 0
    for h in range(n):
        state, bit = full, 1 << h
        while choices[state] is not None:
            test = tests[choices[state]]
            state = state & test if bit & test else state & ~test
            actual_work += 1
        assert state == bit
    assert actual_work == work
    return work, choices


def validation_backend():
    spec = importlib.util.spec_from_file_location("product_validation_backend",
                                                "research-general-algorithm-next.py")
    backend = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = backend
    spec.loader.exec_module(backend)
    return backend


def tests_from_words(words, width):
    return [sum(1 << h for h, word in enumerate(words) if word >> q & 1)
            for q in range(width)]


def exact_depths_for_validation(instance):
    actions = {}

    @lru_cache(None)
    def cost(state):
        if state.bit_count() <= 1:
            return 0
        score, chosen = min((cost(state & test)+cost(state & ~test), q)
                            for q, test in enumerate(instance.tests)
                            if state & test and state & ~test)
        actions[state] = chosen
        return state.bit_count()+score

    cost(instance.full)
    depths, pending = {}, [(instance.full, 0)]
    while pending:
        state, depth = pending.pop()
        if state.bit_count() == 1:
            depths[state.bit_length()-1] = depth
        else:
            test = instance.tests[actions[state]]
            pending.extend(((state & test, depth+1), (state & ~test, depth+1)))
    return depths


def exact_completion_profit_for_validation(tests, prizes):
    @lru_cache(None)
    def solve(state):
        if state.bit_count() == 1:
            return prizes[state.bit_length()-1]
        return max([Fraction(0)] + [solve(state & test)+solve(state & ~test)-state.bit_count()
                                   for test in tests if state & test and state & ~test])
    return solve((1 << len(prizes))-1)


def main():
    rng = random.Random(2026101806)
    minimum_checks, zero_checks, factor_checks = 0, 0, 0
    for width in range(2, 9):
        for _ in range(12):
            words = rng.sample(range(1 << width), rng.randrange(2, min(17, 1 << width)+1))
            oracle = EntropyCuts(words, width)
            universe = (1 << width)-1
            selected, score = oracle.minimum_cut(universe)
            brute = max(oracle.score(mask, universe) for mask in range(1, universe))
            assert score == brute
            minimum_checks += 1
            for mask in range(1, universe):
                left = len({word & mask for word in words})
                right = len({word & (universe ^ mask) for word in words})
                assert (oracle.score(mask, universe) == oracle.zero_score(universe)) == (left*right == len(words))
                zero_checks += 1
            factors, sizes = oracle.factorize()
            assert prod(sizes) == len(words)
            # No returned nonsingleton query factor has a zero mutual-information cut.
            for factor in factors:
                if factor.bit_count() > 1:
                    assert oracle.minimum_cut(factor)[1] < oracle.zero_score(factor)
            factor_checks += 1

    backend = validation_backend()
    optimal_additivity_checks, legal_execution_checks, tensor_checks = 0, 0, 0
    product_examples = []
    for n1, n2 in ((2, 2), (2, 3), (3, 3), (2, 4), (3, 4)):
        for _ in range(8):
            width1, width2 = 3, 3
            first = rng.sample(range(1 << width1), n1)
            second = rng.sample(range(1 << width2), n2)
            words = [a | b << width1 for a, b in product(first, second)]
            width = width1+width2
            oracle = EntropyCuts(words, width)
            factors, sizes = oracle.factorize()
            full = backend.Instance(len(words), tests_from_words(words, width))
            full_optimum = Fraction(full.exact_cost(), len(words))
            summed_optimum, summed_greedy = Fraction(0), Fraction(0)
            local_depths = []
            for factor in factors:
                patterns = sorted({word & factor for word in words})
                factor_tests = [sum(1 << h for h, word in enumerate(patterns) if word >> q & 1)
                                for q in range(width) if factor >> q & 1]
                local = backend.Instance(len(patterns), factor_tests)
                summed_optimum += Fraction(local.exact_cost(), len(patterns))
                summed_greedy += Fraction(local.greedy(local.full).cost, len(patterns))
                depths = exact_depths_for_validation(local)
                local_depths.append({pattern: depths[h] for h, pattern in enumerate(patterns)})
            assert summed_optimum == full_optimum
            # This decomposition alone does not improve ordinary balance greedy:
            # on a product, greedy only interleaves the same marginal policies.
            assert Fraction(full.greedy(full.full).cost, len(words)) == summed_greedy
            optimal_additivity_checks += 1
            work, choices = execute_factor_greedy(words, factors)
            assert Fraction(work, len(words)) == summed_greedy
            assert len([q for q in choices.values() if q is not None]) <= len(words)-1
            legal_execution_checks += 1
            for mode in range(2):
                scales = [Fraction(1) if not mode else Fraction(1, rng.randrange(1, 5))
                          for _ in factors]
                prices = [sum(scale*depths[word & factor]
                              for scale, depths, factor in zip(scales, local_depths, factors))
                          for word in words]
                assert exact_completion_profit_for_validation(full.tests, prices) == 0
                tensor_checks += 1
            product_examples.append({"n": len(words), "factor_sizes": sizes,
                                     "optimum_mean": str(full_optimum),
                                     "factor_greedy_mean": str(summed_greedy)})

    # Pairwise independence must not be mistaken for a product partition.
    xor_oracle = EntropyCuts((0, 3, 5, 6), 3)
    xor_factors, _ = xor_oracle.factorize()
    assert xor_factors == (7,)

    result = {"status": "passed", "exact_Queyranne_vs_exhaustive_checks": minimum_checks,
              "zero_information_vs_cartesian_count_checks": zero_checks,
              "full_factorization_checks": factor_checks,
              "exact_optimum_additivity_checks": optimal_additivity_checks,
              "actual_factor_code_execution_checks": legal_execution_checks,
              "ordinary_greedy_product_identity_checks": legal_execution_checks,
              "exact_global_partial_policy_tensorized_dual_checks": tensor_checks,
              "pairwise_independent_XOR_rejected_as_product": True,
              "selected_small_product_examples": product_examples[:6],
              "factorization_uses_no_exponential_oracle": True,
              "exact_decision_tree_DP_is_validation_only": True,
              "no_unrestricted_approximation_claim": True}
    Path("research-general-product-decomposition-results.json").write_text(
        json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
