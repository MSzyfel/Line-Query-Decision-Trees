"""Exact certificate for a smaller cap in the polynomial W hybrid.

The proof uses only rational arithmetic except for logarithms, which
are enclosed by the positive atanh series with a rational tail bound.
This checks a runtime improvement, not a new approximation factor.
"""
from fractions import Fraction as F


def log_bounds(x, terms=80):
    x = F(x)
    assert x >= 1
    z = (x - 1) / (x + 1)
    total = F(0)
    power = z
    for j in range(terms):
        total += power / (2 * j + 1)
        power *= z * z
    lower = 2 * total
    tail = 2 * power / ((2 * terms + 1) * (1 - z * z))
    return lower, lower + tail


def main():
    gamma = F(246496526, 10**8)
    k = gamma / (gamma - 1)
    assert k == F(123248263, 73248263)
    assert 1 < k < 2
    assert 3 + gamma / k == 2 + gamma
    ln2_lower, ln2_upper = log_bounds(2)
    delta = F(245122334, 10**9)
    balanced_log, _ = log_bounds(1 / (1 - delta))
    flat_log, _ = log_bounds(1 / delta)
    assert gamma * balanced_log / ln2_upper > 1
    assert gamma * flat_log / ln2_upper > 5
    ln3_lower, ln3_upper = log_bounds(3)
    exponent_lower = k * ln3_lower / ln2_upper
    exponent_upper = k * ln3_upper / ln2_lower
    assert F(2666873, 10**6) < exponent_lower
    assert exponent_upper < F(1333437, 500000)
    assert k < F(1682611, 10**6)

    # For every q >= 1, R=floor(k*q). Integer D>R implies D>k*q,
    # giving 3+gamma*q/D < 2+gamma; D<=R fits L=R+1 blocks.
    # Check the rounding boundary, including the smallest inputs.
    for q in range(1, 10001):
        r = (k * q).numerator // (k * q).denominator
        assert r + 1 <= 2 * q + 1
        assert F(r + 1) > k * q
        assert 3 + gamma * q / (r + 1) < 2 + gamma
        assert r >= q
    print('Certified K = 123248263/73248263 < 1.682611.')
    print('Certified strict balanced-query and flat-decoder count credits.')
    print('Certified K*log2(3) < 2.666874 with exact rational log bounds.')
    print('Checked 10,000 integer cap boundaries, including q=1.')
    print('The approximation factor stays 2+gamma = 4.46496526.')


if __name__ == '__main__':
    main()
