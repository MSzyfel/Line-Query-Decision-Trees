"""Strict planar priority-greedy block schedules with dilation tending to two."""
from math import pi,cos,sin


def demands(k):
    out=[]
    for i in range(k):
        p=4*i+1
        out.extend([({p},k+2),({p+1},k+2)])
    for i in range(k-1):
        p=4*i+1
        # Positive vertex intervals; their incident-edge hit demands are
        # [p,p+2] and [p+2,p+4].
        out.extend([({p+1,p+2},i+3),({p+3,p+4},i+3)])
    return out


def check(k):
    m=4*k+2
    ds=demands(k)
    levels=sorted({d for _,d in ds})
    base=len(ds)+3
    weight={d:base**(len(levels)-1-i) for i,d in enumerate(levels)}
    remaining=list(ds)
    chosen=[4*k]  # Forced first edge, disjoint from all current demands.
    available=set(range(m))-{4*k}
    while remaining:
        score={e:sum(weight[d] for s,d in remaining
                     if s & {e,(e+1)%m}) for e in available}
        best=max(score.values())
        ties=[e for e,z in score.items() if z==best]
        step=len(chosen)-1
        if step<k-1:
            assert ties==[4*step+3],(k,step,ties)
        e=min(ties)
        chosen.append(e)
        available.remove(e)
        remaining=[(s,d) for s,d in remaining if not s & {e,(e+1)%m}]
    assert len(chosen)==2*k
    assert set(chosen[1:k])=={4*i+3 for i in range(k-1)}
    assert set(chosen[k:])=={4*i+1 for i in range(k)}
    comparison=[4*k]+[4*i+1 for i in range(k)]
    for s,d in ds:
        rank=min(j+1 for j,e in enumerate(comparison)
                 if s & {e,(e+1)%m})
        assert rank<=d
    # All nonforced selected edges have two fresh endpoints, so caching
    # does not shrink this asymptotic two-block obstruction.
    vertices=[v for e in chosen[1:] for v in (e,(e+1)%m)]
    assert len(vertices)==len(set(vertices))
    return len(chosen)/(k+2)


def geometry(k):
    m=4*k+2
    theta=2*pi/m
    vertices=[(cos(j*theta),sin(j*theta)) for j in range(m)]
    patterns=[s for s,_ in demands(k)]+[{4*k}]
    pts=[]
    for serial,s in enumerate(patterns):
        l,r=min(s),max(s)
        half=(r-l)*theta/2
        cutoff=(cos(half)+3*cos(half+theta))/4+(serial+1)*1e-9
        ang=(l+r)*theta/2
        h=(cos(ang)/cutoff,sin(ang)/cutoff)
        actual={j for j,u in enumerate(vertices)
                if u[0]*h[0]+u[1]*h[1]>1}
        assert actual==s
        pts.append(h)
    pairs=[(4*i+1,4*i+2) for i in range(k)]+[(4*k,4*k+1)]
    mids=[((vertices[a][0]+vertices[b][0])/2,
           (vertices[a][1]+vertices[b][1])/2) for a,b in pairs]
    allqueries=vertices+mids
    margin=min(abs(u[0]*h[0]+u[1]*h[1]-1)
               for u in allqueries for h in pts+[(0,0)])
    assert margin>1e-8
    assert all(any(u[0]*h[0]+u[1]*h[1]>1 for u in mids) for h in pts)
    maxcap=max(sum(u[0]*h[0]+u[1]*h[1]>1 for h in pts) for u in allqueries)
    assert maxcap<.245122334*(len(pts)+1)


if __name__=='__main__':
    for k in range(2,41):
        check(k)
    for k in range(5,21):
        geometry(k)
    print('39 exact schedule checks and 16 strict planar realizations passed.')
    print('Block/deadline ratio at k=40:',check(40),'limit: 2.')
