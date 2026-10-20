"""Searches for a fractional-feasible, integer-infeasible deadline family.

Pure-Python phase-I simplex plus exhaustive ordering; for exploration only.
"""
from itertools import permutations
from random import Random


def lp_feasible(m,t,demands):
    nv=m*t
    constraints=[]
    for d in range(t):
        constraints.append(([1. if j%m==d else 0. for j in ()],1))
    # Flatten by point then time.
    constraints=[]
    for d in range(t):
        constraints.append(([1. if j%t==d else 0. for j in range(nv)],False))
    for p in range(m):
        constraints.append(([1. if j//t==p else 0. for j in range(nv)],False))
    for l,r,d in demands:
        constraints.append(([1. if l<=j//t<=r and j%t<d else 0.
                             for j in range(nv)],True))
    nr=len(constraints)
    na=len(demands)
    total=nv+nr+na
    rows=[]
    bases=[]
    art=nv+nr
    for i,(vals,is_ge) in enumerate(constraints):
        row=vals+[0.]*(nr+na)+[1.]
        row[nv+i]=-1. if is_ge else 1.
        if is_ge:
            row[art]=1.
            bases.append(art)
            art+=1
        else:
            bases.append(nv+i)
        rows.append(row)
    obj=[0.]*(total+1)
    for j in range(nv+nr,total):
        obj[j]=1.
    for i,b in enumerate(bases):
        if b>=nv+nr:
            obj=[a-bb for a,bb in zip(obj,rows[i])]
    for iteration in range(10000):
        # Bland pivoting prevents cycling.
        enters=[j for j in range(total) if obj[j]<-1e-9]
        if not enters:
            return obj[-1]>=-1e-7
        q=enters[0]
        options=[(rows[i][-1]/rows[i][q],bases[i],i)
                 for i in range(nr) if rows[i][q]>1e-9]
        assert options, "unbounded phase-I objective"
        _,_,p=min(options)
        scale=rows[p][q]
        rows[p]=[v/scale for v in rows[p]]
        for i in range(nr):
            if i!=p and abs(rows[i][q])>1e-12:
                factor=rows[i][q]
                rows[i]=[a-factor*b for a,b in zip(rows[i],rows[p])]
        factor=obj[q]
        obj=[a-factor*b for a,b in zip(obj,rows[p])]
        bases[p]=q
    raise AssertionError("simplex iteration limit")


def integer_feasible(m,t,demands):
    for order in permutations(range(m),min(m,t)):
        if all(any(l<=order[j]<=r for j in range(min(d,len(order))))
               for l,r,d in demands):
            return True
    return False


if __name__=='__main__':
    # Independent basic cases sanity-check the feasibility oracle.
    assert lp_feasible(3,2,[(0,1,1),(1,2,1)])
    assert not lp_feasible(3,2,[(0,1,1),(1,2,1),(0,0,2),(2,2,2)])
    rng=Random(8675309)
    found=False
    count=0
    for m,t in [(6,3),(7,3),(7,4),(8,4),(8,5)]:
        possible=[(l,r,d) for l in range(m) for r in range(l,m)
                  for d in range(2,t+1)]
        for _ in range(1500):
            demands=rng.sample(possible,rng.randint(7,min(24,len(possible))))
            integer=integer_feasible(m,t,demands)
            fractional=lp_feasible(m,t,demands)
            assert not integer or fractional
            count+=1
            if fractional and not integer:
                print('Fractional-only family:',m,t,demands)
                found=True
                break
        if found:
            break
    print('Cases:',count,'Fractional-only family found:',found)
