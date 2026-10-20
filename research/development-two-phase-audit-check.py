"""Independent structural and direct-integral audit of the two-phase table.

Unlike the theorem certificate, this computes mean first-hit bounds from
the modified phase sequence itself, without its factorial discount formula.
Decimal evaluation is a cross-check; the published bound uses the existing
outward Fraction certificate.
"""
from decimal import Decimal as D, localcontext
from fractions import Fraction as F
import json
from pathlib import Path


def dec(x):
    x = F(x)
    return D(x.numerator) / D(x.denominator)


def floor(x):
    return x.numerator // x.denominator


def floor_integral(c, lo, hi):
    """Integral floor(c*u) du/u over rational endpoints, directly by cells."""
    if hi <= lo:
        return D(0)
    total = D(0)
    for k in range(floor(c * lo), floor(c * hi) + 1):
        a, b = max(lo, F(k) / c), min(hi, F(k + 1) / c)
        if a < b:
            total += k * dec(b / a).ln()
    return total


def geometric_tail(beta, lo, hi, rank, first_phase):
    total, c = D(0), beta**first_phase
    while c * lo < rank:
        end = min(hi, F(rank) / c)
        total += (floor_integral(c, lo, end)
                  + floor_integral(beta * c, lo, end)) / 2
        c *= beta
    return total


def original_phi(beta, rank):
    lb = dec(beta).ln()
    return ((floor_integral(F(1), F(1), beta) / lb + 1) / 2
            + geometric_tail(beta, F(1), beta, rank, 0) / lb)


def phi_piece(beta, lo, hi, q, r, k2, rank):
    lp = dec(hi / lo).ln()
    total = D(q + 1) * lp / 2
    if r:
        total += D(q + r) * lp / 2 * (rank > q)
        total += D(r + k2) * lp / 2 * (rank > r)
    else:
        total += D(q + k2) * lp / 2 * (rank > q)
    return total + geometric_tail(beta, lo, hi, rank, 2)


def nominal_length(budgets, cover):
    length = 0
    for k in budgets:
        if k >= cover:
            return length + cover
        length += k
    raise AssertionError('insufficient budgets')


def main():
    data = json.loads(Path('expected-two-phase-certificate.json').read_text())
    beta, delta, tau = map(F, (data['beta'], data['delta'], data['tau']))
    rows = data['rows']
    pos = F(1)
    identity_checks = 0
    for row in rows:
        lo, hi = F(row['l']), F(row['h'])
        assert lo == pos < hi
        pos = hi
        # Check the ENTIRE half-open row, not only its midpoint.
        for j in range(3):
            k = row[f'k{j}']
            assert k <= beta**j * lo < beta**j * hi <= k + 1
        assert sum(F(o['v']) for o in row['opts']) == 1
        u = (lo + hi) / 2
        old = [floor(beta**j * u) for j in range(8)]
        k0, k1, k2 = old[:3]
        for o in row['opts']:
            v, q, r, cut = F(o['v']), o['q'], o['r'], o['cut']
            assert v >= 0 and 1 <= q <= 6
            assert q < k2 and (r == 0 or q < r < k2)
            assert r == 0 or r in {k1 - 1, k1, k1 + 1}
            # This particular table uses only FIRST-batch saving minorants.
            assert cut == q and o['credit'] in {'A', 'C', 'zero'}
            new = [q] + ([r] if r else []) + old[2:]
            for t in range(1, 81):
                phi_old = F(old[0] + 1, 2) + sum(
                    (F(a + b, 2) for a, b in zip(old, old[1:]) if t > a), F(0))
                phi_new = F(new[0] + 1, 2) + sum(
                    (F(a + b, 2) for a, b in zip(new, new[1:]) if t > a), F(0))
                formula = k0 - q + (k0 + k1) * (t > k0) + (k1 + k2) * (t > k1)
                formula -= (q + r) * (t > q) + (r + k2) * (t > r) if r else (q + k2) * (t > q)
                assert 2 * (phi_old - phi_new) == formula
                zero = q * (q < t) + r * (r < t) - k0 * (k0 < t) - k1 * (k1 < t)
                assert nominal_length(new, t) - nominal_length(old, t) == zero
                identity_checks += 1
    assert pos == beta

    with localcontext() as ctx:
        ctx.prec = 75
        lb = dec(beta).ln()
        lead = dec(beta + 1) / lb
        phi1 = original_phi(beta, 1)
        assert abs(phi1 - (2 - D(6).ln() / (2 * lb))) < D('1e-65')
        c, d = F(228683, 103683), F(250000, 103683)
        a, mu, dz = {}, D(0), {k: D(0) for k in range(1, 31)}
        for row in rows:
            lo, hi = F(row['l']), F(row['h'])
            probability = dec(hi / lo).ln() / lb
            for o in row['opts']:
                v, q, r = dec(F(o['v'])), o['q'], o['r']
                inter = d * q if o['credit'] == 'C' else F(q) if o['credit'] == 'A' else F(0)
                mu += probability * v * dec(inter)
                for k in dz:
                    dz[k] += probability * v * (
                        q * (q < k) + r * (r < k)
                        - row['k0'] * (row['k0'] < k)
                        - row['k1'] * (row['k1'] < k))
        for t in range(1, 31):
            phi_new, saving = D(0), D(0)
            for row in rows:
                lo, hi = F(row['l']), F(row['h'])
                p = dec(hi / lo).ln() / lb
                for o in row['opts']:
                    v, q, r = dec(F(o['v'])), o['q'], o['r']
                    phi_new += v * phi_piece(beta, lo, hi, q, r, row['k2'], t) / lb
                    slope = c if o['credit'] == 'C' else F(1) if o['credit'] == 'A' else F(0)
                    saving += p * v * dec(slope) * (t <= q)
            a[t] = lead * (t - 1) + 2 * phi1 - 2 * phi_new + saving
        assert a[1] < dec(tau) and all(a[t] > dec(tau) for t in range(2, 31))
        assert all(z <= 0 for z in dz.values())
        assert all(abs(dz[k] - dz[14]) < D('1e-65') for k in range(14, 31))
        chi = dec(tau) - 2 * dec(delta) * (dec(tau) - a[1]) - dec(delta) * mu
        assert chi + 2 / lb > dec(tau)
        coefficient = 7 - D(6).ln() / lb - chi
        hd = -dec(delta) * dec(delta).ln() - dec(1 - delta) * dec(1 - delta).ln()
        rem = 1 - 6 * delta
        sigma = -6 * dec(delta) * dec(delta).ln() - dec(rem) * dec(rem).ln()
        ratio = lead + max(D(2).ln() / hd, coefficient * D(2).ln() / sigma)
        assert ratio < D('5.182976')
        print(f'Independent direct-integral ratio cross-check: {ratio}')
        print(f'a1={a[1]}, a14={a[14]}, mu={mu}, chi={chi}, B={coefficient}')
    print(f'All {len(rows)} entire half-open rows and {identity_checks} exact phase/length identities pass.')
    print('First-batch minorant scope, finite exceptions, tail cutoff, and zero-route credit pass.')


if __name__ == '__main__':
    main()
