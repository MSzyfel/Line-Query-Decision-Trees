"""Checks the asymptotically tight adjacent-run priority-greedy family.

Run with Python 3. No dependencies. The combinatorial check uses integers.
The optional geometric check independently realizes the short arcs on a
regular polygon and checks all supplied-line signs strictly.
"""
from math import cos, sin, pi


def instance(k):
    # Two forced real vertices come last in the circular order.  After
    # removing them, pair i is [3*i, 3*i+1], gap i is 3*i+2.
    intervals = []
    for i in range(k):
        for p in (3*i, 3*i+1):
            intervals.append((p, p, k+1, f"s{p}"))
    for i in range(k-1):
        g = 3*i+2
        for l, r in ((g-2,g),(g-1,g),(g,g+1),(g,g+2)):
            intervals.append((l,r,i+3,f"a{l}:{r}"))
    return intervals


def check_schedule(k):
    demands = instance(k)
    levels = sorted({d for _,_,d,_ in demands})
    base = len(demands)+2
    weights = {d: base**(len(levels)-1-j) for j,d in enumerate(levels)}
    remaining = list(demands)
    order = []
    available = set(range(3*k-1))
    while remaining:
        scores = {p:sum(weights[d] for l,r,d,_ in remaining if l<=p<=r)
                  for p in available}
        best = max(scores.values())
        tied = [p for p,z in scores.items() if z==best]
        # Every first k-1 choices must be the next gap, strictly.
        if len(order)<k-1:
            assert tied == [3*len(order)+2], (k,order,tied)
        p = min(tied)
        order.append(p)
        available.remove(p)
        remaining = [z for z in remaining if not z[0]<=p<=z[1]]
    assert len(order) == 3*k-1
    assert 2+len(order) == 3*(k+1)-2
    # The comparison starts with the forced pair and then pairs left-to-right.
    for l,r,d,_ in demands:
        first = min(i+2 for i in range(k)
                    if any(l<=p<=r for p in (3*i,3*i+1)))
        assert first<=d
    return len(order)


def check_geometry(k):
    m = 3*k+1
    theta = 2*pi/m
    vertices = [(cos(theta*j),sin(theta*j)) for j in range(m)]
    patterns = [(l,r) for l,r,_,_ in instance(k)]
    patterns.append((m-2,m-2))
    points = []
    for serial,(l,r) in enumerate(patterns):
        half = (r-l)*theta/2
        inner,outer = cos(half),cos(half+theta)
        # Strictly below the average makes edge midpoints cover two-point
        # arcs that otherwise sit on their line; stay above outer threshold.
        threshold = (inner+3*outer)/4
        threshold += (serial+1)*1e-9
        assert threshold>0
        ang = (l+r)*theta/2
        h = (cos(ang)/threshold,sin(ang)/threshold)
        bits = [u[0]*h[0]+u[1]*h[1]>1 for u in vertices]
        assert bits == [l<=j<=r for j in range(m)]
        points.append(h)
    # Origin supplies the all-zero singleton.  Pair midpoints are legal
    # supplied original queries supported on the adjacent hull pair.
    pair_indices = [(3*i,3*i+1) for i in range(k)]+[(m-2,m-1)]
    midpoints = [((vertices[a][0]+vertices[b][0])/2,
                  (vertices[a][1]+vertices[b][1])/2)
                 for a,b in pair_indices]
    margin = min(abs(u[0]*h[0]+u[1]*h[1]-1)
                 for u in vertices+midpoints for h in points+[(0,0)])
    assert margin>1e-8, margin
    for h in points:
        assert any(u[0]*h[0]+u[1]*h[1]>1 for u in midpoints)
    # Flatness is checked for every actual supplied query, not only hull bits.
    n = len(points)+1
    maxcap = max(sum(u[0]*h[0]+u[1]*h[1]>1 for h in points)
                 for u in vertices+midpoints)
    assert maxcap < .245122334*n, (k,maxcap,n)
    return m,n,maxcap,margin


if __name__ == "__main__":
    for k in range(2,41):
        check_schedule(k)
    for k in range(8,21):
        check_geometry(k)
    print("39 integer schedule checks and 13 strict planar realizations passed.")
