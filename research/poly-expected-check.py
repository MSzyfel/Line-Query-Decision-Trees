"""Exact certificates and finite checks for the polynomial block improvement.

This script verifies the numerical certificate using only Fraction arithmetic.
The finite schedule tests check the implementation invariants used in the proof.
"""
from fractions import Fraction as F
from math import factorial, floor, log as math_log, lgamma
from itertools import combinations, permutations
from random import Random


class Bound:
    def __init__(self, lo, hi=None):
        self.lo = F(lo)
        self.hi = self.lo if hi is None else F(hi)
        assert self.lo <= self.hi

    def __add__(self, other):
        other = other if isinstance(other, Bound) else Bound(other)
        return Bound(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Bound(-self.hi, -self.lo)

    def __sub__(self, other):
        other = other if isinstance(other, Bound) else Bound(other)
        return self + -other

    def __rsub__(self, other):
        return Bound(other) - self

    def __mul__(self, other):
        other = other if isinstance(other, Bound) else Bound(other)
        products = [a*b for a in [self.lo, self.hi] for b in [other.lo, other.hi]]
        return Bound(min(products), max(products))

    __rmul__ = __mul__

    def __truediv__(self, other):
        other = other if isinstance(other, Bound) else Bound(other)
        assert other.lo > 0
        return self * Bound(1/other.hi, 1/other.lo)


def raw_log(x, terms=100):
    assert 1 <= x <= 2
    z = (x-1)/(x+1)
    lo = 2*sum(z**(2*j+1)/F(2*j+1) for j in range(terms))
    hi = lo + 2*z**(2*terms+1)/(F(2*terms+1)*(1-z*z))
    return Bound(lo, hi)


LOG2 = raw_log(F(2))


def log(x):
    x = F(x)
    assert x > 0
    powers = 0
    while x < 1:
        x *= 2
        powers -= 1
    while x > 2:
        x /= 2
        powers += 1
    return raw_log(x) + powers*LOG2


def certificate():
    beta = F(3512863, 10**6)
    delta = F(138821934, 10**9)
    lb = log(beta)
    assert (Bound(beta-1) - 2*lb).lo > 0  # lambda > nu
    A = Bound(beta+1) / lb
    C = 7 - log(6)/lb
    discounts = [Bound(0)]
    for t in range(2, 5):
        n = (beta*t).numerator // (beta*t).denominator
        assert n == {2: 7, 3: 10, 4: 14}[t]
        integral = t*log(t) - log(factorial(t))
        integral = integral + (n-3)*lb + n*log(t) - log(F(factorial(n), 6))
        discounts.append((Bound((beta+1)*(t-1))-integral)/lb)
    assert 3 < 1/(2*delta) < 4
    chi = 2*delta*(discounts[1]+discounts[2]) + (1-6*delta)*discounts[3]
    assert (chi + Bound(2)/lb - discounts[3]).lo > 0
    B = C - chi
    h = -delta*log(delta) - (1-delta)*log(1-delta)
    assert 7 < 1/delta < 8
    rem = 1-7*delta
    sigma = -7*delta*log(delta) - rem*log(rem)
    balanced = LOG2/h
    flat = B*LOG2/sigma
    upper = F(5312551, 10**6)
    assert A.hi + max(balanced.hi, flat.hi) < upper
    print('Rational certificate: R < 5.312551.')
    print('A interval', float(A.lo), float(A.hi))
    print('B interval', float(B.lo), float(B.hi))
    print('Entropy-ratio upper', float(max(balanced.hi, flat.hi)))
    print('Discrete-credit condition slack', float((chi + Bound(2)/lb - discounts[3]).lo))


def candidate_sets(m, demands):
    """Exact maximum-coverage oracle, exhaustive only for small validation cases."""
    sets = {}
    for k in range(1, m+1):
        options = [combo for r in range(k+1) for combo in combinations(range(m), r)]
        sets[k] = max(options, key=lambda combo: (sum(w for arc,w in demands if set(combo)&arc), -len(combo), combo))
    full = sum(w for _,w in demands)
    k0 = next(k for k in sets if sum(w for arc,w in demands if set(sets[k])&arc) == full)
    return sets, k0


def schedule(beta, shift, m, demands, sets, k0):
    order, hit = [], set()
    u = shift
    while True:
        k = u.numerator // u.denominator
        chosen = list(sets[min(k,k0)])
        while chosen:
            weights = {q: sum(w for j,(arc,w) in enumerate(demands) if j not in hit and q in arc) for q in chosen}
            q = max(chosen, key=lambda q: (weights[q], -q))
            chosen.remove(q)
            if weights[q] and q not in order:
                order.append(q)
                hit.update(j for j,(arc,_) in enumerate(demands) if q in arc)
        if k >= k0:
            assert len(hit) == len(demands)
            return order
        u *= beta


def finite_checks():
    rng = Random(20261015)
    checked = 0
    beta = F(3512863, 10**6)
    for m in range(2, 9):
        for _ in range(50):
            demands = []
            for j in range(rng.randrange(1, 15)):
                start, length = rng.randrange(m), rng.randrange(1,m+1)
                arc = {(start+k)%m for k in range(length)}
                demands.append((arc,rng.randrange(1,10)))
            sets,k0 = candidate_sets(m,demands)
            for shift in [F(1), F(3,2), F(2), beta-F(1,1000000)]:
                order = schedule(beta,shift,m,demands,sets,k0)
                assert len(order) <= (1+beta/(beta-1))*k0
                ranks = {q:i+1 for i,q in enumerate(order)}
                first_cost = sum(w*min(ranks[q] for q in arc if q in ranks) for arc,w in demands)
                shifted = sum(w*(min(ranks[q] for q in arc if q in ranks)-1) for arc,w in demands)
                assert 2*first_cost + 3*sum(w for _,w in demands) == 2*shifted+5*sum(w for _,w in demands)
                checked += 1
    print(f'{checked} finite circular-interval batch schedule checks passed.')


def ordering_bound_checks():
    """Compare the best shifted batch schedule with all source permutations.

    This supplementary check uses floats for the already-established scheduling
    lemma; the theorem's final constant certificate above remains exact.
    """
    rng = Random(20261016)
    beta = F(3512863, 10**6)
    beta_float = float(beta)
    lb = math_log(beta_float)

    def primitive(y):
        k = floor(y+1e-12)
        return k*math_log(y)-lgamma(k+1)

    phi1 = 2-math_log(6)/(2*lb)

    def phi(t):
        return phi1+(primitive(t)+primitive(beta_float*t)-primitive(beta_float))/(2*lb)

    count = 0
    for m in range(2, 8):
        for _ in range(15):
            demands = []
            for j in range(rng.randrange(1, 10)):
                start, length = rng.randrange(m), rng.randrange(1, m+1)
                arc = {(start+k)%m for k in range(length)}
                demands.append((arc, rng.randrange(1, 10)))
            p0 = rng.randrange(0, 10)
            sets,k0 = candidate_sets(m,demands)
            powers = [F(1)]
            while powers[-1] < k0:
                powers.append(powers[-1]*beta)
            breaks = {F(1), beta}
            for power in powers:
                for k in range(1,k0+1):
                    u=F(k)/power
                    if 1 <= u < beta:
                        breaks.add(u)
            breaks = sorted(breaks)
            shifts = breaks[:-1]+[(a+b)/2 for a,b in zip(breaks,breaks[1:])]
            actuals = []
            for shift in shifts:
                order = schedule(beta,shift,m,demands,sets,k0)
                rank = {q:i+1 for i,q in enumerate(order)}
                actuals.append(sum(w*min(rank[q] for q in arc if q in rank) for arc,w in demands)+p0*len(order))
            z = k0+(k0*math_log(k0)-lgamma(k0+1))/lb
            comparison = min(sum(w*phi(min(rank[q] for q in arc)) for arc,w in demands)
                             for order in permutations(range(m))
                             for rank in [{q:i+1 for i,q in enumerate(order)}])+p0*z
            assert min(actuals) <= comparison+1e-8
            count += 1
    print(f'{count} joint first-hit / zero-wait bounds passed against all source permutations.')


if __name__ == '__main__':
    certificate()
    finite_checks()
    ordering_bound_checks()
