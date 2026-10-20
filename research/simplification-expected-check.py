"""Exact sanity check of the common capped-rank credit lemma."""
from fractions import Fraction as F
from random import Random
rng=Random(20261013)
for _ in range(3000):
    delta=F(rng.randrange(10,40),100)
    p0=F(rng.randrange(0,100),100);w=F(1);b=w-p0
    n=12;m=[F(0) for _ in range(n)];left=b
    for i in range(n):
        if not left:break
        value=min(left,2*delta,F(rng.randrange(0,100),100));m[i]=value;left-=value
    if left:
        for i in range(n):
            value=min(left,2*delta-m[i]);m[i]+=value;left-=value
            if not left:break
    assert sum(m)==b and max(m)<=2*delta
    a=[F(rng.randrange(-30,100),10) for _ in range(n)]
    tau=F(rng.randrange(0,50),10);mu=F(rng.randrange(0,30),10)
    chi=tau-2*delta*sum(max(F(0),tau-x) for x in a)-delta*mu
    zeta=tau-chi+F(rng.randrange(0,30),10)
    lhs=sum(v*x for v,x in zip(m,a))-delta*w*mu+zeta*p0
    assert lhs>=chi*b
print('3000 exact capped-rank credit instances passed')
