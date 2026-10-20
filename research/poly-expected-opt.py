import math

def floor_integral(y):
    n = int(math.floor(y + 1e-12))
    return n * math.log(y) - math.lgamma(n + 1)

def discount(beta, t):
    if t == 1:
        return 0.0
    value = ((beta + 1) * (t - 1)
             - floor_integral(t)
             - floor_integral(beta * t) + floor_integral(beta)) / math.log(beta)
    return max(0.0, value)

def score(beta, delta):
    logb = math.log(beta)
    lam = (beta + 1) / (2 * logb)
    nu = 1 + 1 / logb
    r = int(beta)
    phi1 = (r + 1) / 2 - math.lgamma(r + 1) / (2 * logb)
    n = int(1 / (2 * delta))
    rem = 1 - 2 * delta * n
    chi = 2 * delta * sum(discount(beta, t) for t in range(1, n + 1)) + rem * discount(beta, n + 1)
    if discount(beta, n + 1) > chi + 2 / logb + 1e-10:
        return 1000.0
    B = 3 + 2 * phi1 - chi
    k = int(1 / delta)
    sr = 1 - k * delta
    sigma = -k * delta * math.log(delta) - (sr * math.log(sr) if sr else 0)
    h = -delta * math.log(delta) - (1 - delta) * math.log1p(-delta)
    return 2 * max(lam, nu) + max(math.log(2) / h, B * math.log(2) / sigma)

def golden(fn, low, high, rounds=100):
    ratio = (math.sqrt(5) - 1) / 2
    a, b = high - ratio * (high - low), low + ratio * (high - low)
    fa, fb = fn(a), fn(b)
    for _ in range(rounds):
        if fa <= fb:
            high, b, fb = b, a, fa
            a = high - ratio * (high - low)
            fa = fn(a)
        else:
            low, a, fa = a, b, fb
            b = low + ratio * (high - low)
            fb = fn(b)
    return (low + high) / 2

if __name__ == '__main__':
    best = (1000, 0, 0)
    for j in range(201):
        beta = 2 + j * .03
        for k in range(401):
            delta = .05 + k * .0005
            val = score(beta, delta)
            if val < best[0]: best = (val, beta, delta)
    val, beta, delta = best
    for _ in range(20):
        delta = golden(lambda d: score(beta, d), max(.03, delta - .01), min(.32, delta + .01))
        beta = golden(lambda b: score(b, delta), max(1.5, beta - .1), beta + .1)
    print('best', score(beta, delta), 'beta', beta, 'delta', delta)
    print('coefficients', (beta+1)/math.log(beta), 'B', score(beta,delta)-(beta+1)/math.log(beta))
