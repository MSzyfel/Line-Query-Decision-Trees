"""Independent finite checks for the first-batch orientation discount."""
from itertools import combinations
from math import floor, lgamma, log
from random import Random


def coefficient_checks():
    beta, delta = 3.512863, 0.142275675
    lb = log(beta)
    probabilities = [log(2)/lb, log(1.5)/lb, log(beta/3)/lb]
    mu = sum((k+1)*p for k,p in enumerate(probabilities))
    assert abs(mu - (3-log(6)/lb)) < 1e-12

    def primitive(value):
        integer = floor(value + 1e-12)
        return integer*log(value)-lgamma(integer+1)

    def discount(t):
        integral = primitive(t) + primitive(beta*t)-primitive(beta)
        return ((beta+1)*(t-1)-integral)/lb

    e = [discount(t) for t in range(1, 101)]
    a = e.copy()
    for t in range(3):
        a[t] += sum(probabilities[t:])
    assert all(value < e[3] for value in a[:3])
    chi_old = 2*delta*sum(e[:3]) + (1-6*delta)*e[3]
    chi_new = chi_old + delta*mu
    assert chi_new + 2/lb > e[3]

    # Minimize the linear mass expression explicitly, without presuming the
    # first three augmented coefficients are in increasing order.
    indices = sorted(range(len(a)), key=a.__getitem__)
    for step in range(1001):
        b = step/1000
        remaining, value = b, 0.0
        for index in indices:
            mass = min(remaining, 2*delta)
            value += mass*a[index]
            remaining -= mass
            if remaining <= 1e-14:
                break
        assert remaining <= 1e-12
        value -= delta*mu
        value += 2*(1-b)/lb
        assert value >= chi_new*b-1e-10
    print('Augmented coefficients:', a[:4])
    print('Orientation intercept:', delta*mu)
    print('Full-mass credit:', chi_new)
    print('Zero-credit slack:', chi_new+2/lb-e[3])
    print('1001 independent linear-fill checks passed.')


def first_batch_checks():
    rng = Random(20261017)
    delta = 0.142275675
    checked = 0
    for m in range(4, 13):
        for _ in range(100):
            demands = []
            for _ in range(rng.randrange(2, 20)):
                start = rng.randrange(m)
                length = rng.randrange(1, max(2, m//3+1))
                arc = {(start+j)%m for j in range(length)}
                demands.append((arc, rng.randrange(1, 20)))
            total_positive = sum(weight for _,weight in demands)
            maximum_cap = max(sum(weight for arc,weight in demands if v in arc)
                              for v in range(m))
            # Adding zero-pattern mass makes the desired cap bound hold;
            # the credit inequality itself does not require its value.
            total_mass = max(total_positive, maximum_cap/delta*1.0001)
            witness = list(range(m))
            rng.shuffle(witness)
            for k in range(1, 4):
                def coverage(blocks):
                    vertices = {v for block in blocks for v in (block, (block+1)%m)}
                    return sum(weight for arc,weight in demands if vertices & arc)
                options = [combo for size in range(k+1)
                           for combo in combinations(range(m), size)]
                chosen = list(max(options, key=lambda combo: (coverage(combo), -len(combo))))
                hit, pin, batch_mass = set(), 0, 0
                while chosen:
                    def new_weight(block):
                        vertices = {block, (block+1)%m}
                        return sum(weight for j,(arc,weight) in enumerate(demands)
                                   if j not in hit and vertices & arc)
                    block = max(chosen, key=new_weight)
                    chosen.remove(block)
                    v, w = block, (block+1)%m
                    x = y = shared = 0
                    for j,(arc,weight) in enumerate(demands):
                        if j in hit:
                            continue
                        if v in arc and w in arc:
                            shared += weight
                        elif v in arc:
                            x += weight
                        elif w in arc:
                            y += weight
                    g = x+y+shared
                    assert max(x,y) >= g-delta*total_mass-1e-9
                    pin += max(x,y)
                    batch_mass += g
                    hit.update(j for j,(arc,_) in enumerate(demands) if v in arc or w in arc)
                witness_mass = coverage(witness[:k])
                assert batch_mass >= witness_mass
                assert pin >= max(0, batch_mass-k*delta*total_mass)-1e-8
                assert pin >= witness_mass-k*delta*total_mass-1e-8
                checked += 1
    print(f'{checked} first-batch orientation/coverage transfer checks passed.')


def mixed_prefix_checks():
    beta, delta = 3.512863, 0.142671046
    alpha0, alpha1 = 0.7963376, 0.952407
    lb = log(beta)
    probabilities = [log(2)/lb, log(1.5)/lb, log(beta/3)/lb]
    q = [alpha0*log(4/beta)/lb,
         alpha1*log(5/4)/lb,
         log(6/5)/lb]
    assert 1 < 4/beta < 5/beta < 6/beta < 2
    assert 0 <= alpha0 <= 1 and 0 <= alpha1 <= 1

    def primitive(value):
        integer = floor(value+1e-12)
        return integer*log(value)-lgamma(integer+1)

    def discount(t):
        return ((beta+1)*(t-1)-primitive(t)-primitive(beta*t)
                +primitive(beta))/lb

    e = [discount(t) for t in range(1, 31)]
    a = e.copy()
    a[0] = 1
    a[1] += 1-probabilities[0]+sum(q)
    a[2] += probabilities[2]+sum(q)
    a[3] += q[1]+q[2]
    a[4] += q[2]
    mu = sum((k+1)*p for k,p in enumerate(probabilities))
    mu += sum((j+3)*value for j,value in enumerate(q))
    threshold = 1.382412
    assert a[0] < threshold and a[2] < threshold
    assert all(a[j] > threshold for j in [1,3,4,5])
    chi = threshold-2*delta*((threshold-a[0])+(threshold-a[2]))-delta*mu
    assert chi+2/lb > threshold
    rng = Random(20261020)
    for _ in range(10000):
        masses = [rng.random()*2*delta for _ in range(rng.randrange(6,31))]
        scale = min(1, rng.random()/sum(masses))
        masses = [value*scale for value in masses]
        b = sum(masses)
        first = sum(probabilities[k-1]*(sum(masses[:k])-k*delta)
                    for k in range(1,4))
        interpolation = sum(value*(sum(masses[:j+3])-masses[0]-(j+3)*delta)
                            for j,value in enumerate(q))
        linear_pin = first+interpolation
        coefficient_pin = sum(mass*(a[t]-e[t])
                              for t,mass in enumerate(masses))-delta*mu
        assert abs(linear_pin-coefficient_pin) < 1e-12
        combined = sum(mass*e[t] for t,mass in enumerate(masses))+linear_pin+2*(1-b)/lb
        assert combined >= chi*b-1e-10
    print('Mixed-prefix rational threshold:', threshold)
    print('Mixed-prefix credit:', chi)
    print('10,000 unclipped interpolation/coefficient-transfer checks passed.')


if __name__ == '__main__':
    coefficient_checks()
    first_batch_checks()
    mixed_prefix_checks()
