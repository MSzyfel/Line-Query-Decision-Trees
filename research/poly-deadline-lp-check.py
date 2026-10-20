"""Targeted exact deadline LP search via convex mixtures of orders.

Every generated assignment is rational LP-feasible by construction.  Include
every interval at its earliest fractionally covered deadline.  Test integer
feasibility by subset dynamic programming rather than factorial enumeration.
"""
from random import Random
from time import monotonic
from fractions import Fraction
from itertools import permutations
import sys


COUNTEREXAMPLE = [(0, 0, 4), (0, 1, 2), (1, 4, 2), (1, 2, 3),
                 (2, 2, 5), (2, 3, 3), (3, 4, 4), (3, 5, 1),
                 (4, 4, 5), (5, 5, 3)]


def induced_demands(m, t, orders, weights):
    total = sum(weights)
    cumulative = [0] * m
    demands = {}
    for d in range(1, t + 1):
        for order, weight in zip(orders, weights):
            cumulative[order[d - 1]] += weight
        for l in range(m):
            mass = 0
            mask = 0
            for r in range(l, m):
                mass += cumulative[r]
                mask |= 1 << r
                if mass >= total and mask not in demands:
                    demands[mask] = d
    return [(mask, d) for mask, d in demands.items()]


def integer_feasible(m, t, demands, witness=False):
    # Retain only inclusion-minimal demands at each deadline prefix.
    prefixes = []
    for d in range(1, t + 1):
        masks = sorted({mask for mask, deadline in demands if deadline <= d},
                       key=int.bit_count)
        minimal = []
        for mask in masks:
            if not any(small & mask == small for small in minimal):
                minimal.append(mask)
        prefixes.append(minimal)
    states = {0: ()}
    full = (1 << m) - 1
    for d in range(t):
        next_states = {}
        for mask, order in states.items():
            available = full ^ mask
            while available:
                bit = available & -available
                available -= bit
                larger = mask | bit
                if larger in next_states:
                    continue
                if all(larger & interval for interval in prefixes[d]):
                    next_states[larger] = order + (bit.bit_length() - 1,)
        states = next_states
        if not states:
            return None if witness else False
    return next(iter(states.values())) if witness else True


def format_demands(demands):
    return sorted((mask.bit_length() - mask.bit_count(), mask.bit_length() - 1, d)
                  for mask, d in demands)


def minimize(m, t, demands, rng):
    best = demands
    for _ in range(20):
        small = list(demands)
        rng.shuffle(small)
        j = 0
        while j < len(small):
            candidate = small[:j] + small[j+1:]
            if not integer_feasible(m, t, candidate):
                small = candidate
            else:
                j += 1
        if len(small) < len(best):
            best = small
    return best


def certificate():
    pairs = [(3, 5), (0, 1), (2, 5), (0, 4), (2, 4)]
    x = {(p, slot): Fraction(1, 2) for slot, pair in enumerate(pairs, 1)
         for p in pair}
    assert all(sum(x.get((p, slot), 0) for p in range(6)) == 1
               for slot in range(1, 6))
    assert all(sum(x.get((p, slot), 0) for slot in range(1, 6)) <= 1
               for p in range(6))
    for l, r, d in COUNTEREXAMPLE:
        assert sum(x.get((p, slot), 0) for p in range(l, r + 1)
                   for slot in range(1, d + 1)) == 1
    demands = [(((1 << (r + 1)) - 1) ^ ((1 << l) - 1), d)
               for l, r, d in COUNTEREXAMPLE]
    assert not integer_feasible(6, 5, demands)
    for j in range(10):
        assert integer_feasible(6, 5, demands[:j] + demands[j + 1:])
    best = min(max(Fraction(next(j for j, p in enumerate(order, 1)
                                if l <= p <= r), d)
                   for l, r, d in COUNTEREXAMPLE)
               for order in permutations(range(6)))
    assert best == Fraction(6, 5)
    print('Exact rational LP certificate, integer infeasibility, 10 deletion',
          'checks, and 720-order dilation optimum 6/5 passed.', flush=True)


if __name__ == '__main__':
    certificate()
    if '--search' not in sys.argv:
        raise SystemExit(0)
    rng = Random(1091326)
    started = monotonic()
    count = 0
    for m, t in [(6, 3), (8, 4), (10, 5), (12, 6), (14, 7)]:
        for _ in range(3000):
            k = rng.randrange(2, 6)
            weights = [rng.randrange(1, 5) for __ in range(k)]
            orders = [rng.sample(range(m), t) for __ in range(k)]
            demands = induced_demands(m, t, orders, weights)
            count += 1
            if not integer_feasible(m, t, demands):
                print('FRACTIONAL ONLY', m, t, 'orders', orders, 'weights', weights,
                      'demands', format_demands(demands), flush=True)
                small = minimize(m, t, demands, rng)
                print('MINIMAL', format_demands(small), flush=True)
                raise SystemExit(1)
        print('Checked', count, 'through', (m, t), 'seconds', monotonic()-started,
              flush=True)
    print('No obstruction found.', flush=True)
