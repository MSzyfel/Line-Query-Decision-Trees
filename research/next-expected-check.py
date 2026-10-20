"""Exact certificate for a changed initial geometric-batch schedule."""
from fractions import Fraction as F
from math import factorial
from random import Random
import runpy

helpers=runpy.run_path('poly-expected-check.py')
Bound,log,LOG2=helpers['Bound'],helpers['log'],helpers['LOG2']
oracle=helpers['candidate_sets']


def table(beta):
    c,d=F(228683,103683),F(250000,103683)
    # Option: probability, initial budget q, merge?, slope, intercept.
    v1=F(95240701,10**8)
    v2=F(37279986,10**8)
    v3=F(4271137,10**8)
    v4=F(33933837,10**8)
    v5=F(36583316,10**8)
    return [
        (F(1),4/beta,[(F(1),3,True,c,3*d)]),
        (4/beta,5/beta,[(v1,4,True,F(1),F(4)),(1-v1,4,True,F(0),F(0))]),
        (5/beta,F(2),[(F(1),1,False,c,d)]),
        (F(2),8/beta,[(v2,1,False,c,d),(1-v2,2,False,c,2*d)]),
        (8/beta,F(3),[(F(1),2,False,c,2*d)]),
        (F(3),11/beta,[(v3,2,False,c,2*d),(1-v3,3,False,c,3*d)]),
        (11/beta,12/beta,[(F(1),3,False,c,3*d)]),
        (12/beta,beta,[(v4,3,False,c,3*d),(v5,5,False,F(1),F(5)),
                       (1-v4-v5,6,False,F(0),F(0))]),
    ]


def correction(k0,k1,q,merge,t):
    if merge:
        assert q==k1
        return k0-k1+(k0+k1)*(t>k0)
    return k0-q+(k0+k1)*(t>k0)-(q+k1)*(t>q)


def certificate():
    beta=F(3512863,10**6)
    delta=F(155223384,10**9)
    lb=log(beta)
    assert (Bound(beta-1)-2*lb).lo>0
    # Preserve the accepted rational entropy-tent certificate.
    pstar=F(21317,125000)
    hstar=1-2*pstar
    assert (-pstar*log(pstar)-(1-pstar)*log(1-pstar)-hstar*LOG2).lo>0
    es={1:Bound(0)}
    for t in range(2,8):
        n=(beta*t).numerator//(beta*t).denominator
        integral=t*log(t)-log(factorial(t))
        integral+=(n-3)*lb+n*log(t)-log(F(factorial(n),6))
        es[t]=(Bound((beta+1)*(t-1))-integral)/lb
    a=es.copy()
    mu=Bound(0)
    dz={k:Bound(0) for k in range(1,8)}
    tailshift=Bound(0)
    rows=table(beta)
    for left,right,opts in rows:
        assert left<right
        assert sum(v for v,q,merge,c,d in opts)==1
        prob=log(right/left)/lb
        u=(left+right)/2
        k0=int(u)
        # Rows whose unchanged first budget spans several k1's have zero correction.
        k1=int(beta*u)
        for v,q,merge,c,d in opts:
            assert merge or q<k1
            if q!=k0 or merge:
                assert int(beta*left)==int(beta*right)-1 or int(beta*left)==int(beta*right)
            mu+=prob*v*d
            for t in range(1,8):
                a[t]+=prob*v*(correction(k0,k1,q,merge,t)+c*(t<=q))
            tailshift+=prob*v*correction(k0,k1,q,merge,7)
            for k in range(1,8):
                change=(-k0*(k0<k)) if merge else q*(q<k)-k0*(k0<k)
                dz[k]+=prob*v*change
    T=Bound(F(20718779,10**7)) # 2.0718779
    assert (T-a[1]).lo>0
    for t in range(2,8):assert (a[t]-T).lo>0
    assert (a[7]-es[7]-tailshift).lo<=0<=(a[7]-es[7]-tailshift).hi
    assert dz[1].lo==dz[1].hi==0
    for k in range(2,8):assert dz[k].hi<0
    # q<=6 and k0<=3; merged waiting change is -k0 1[k0<k].
    # Thus every k>=7 has the same waiting change as k=7.
    chi=T-2*delta*(T-a[1])-delta*mu
    assert (chi+Bound(2)/lb-T).lo>0
    A=Bound(beta+1)/lb
    C=7-log(6)/lb
    B=C-chi
    assert 6<1/delta<7
    rem=1-6*delta
    sigma=-6*delta*log(delta)-rem*log(rem)
    h=-delta*log(delta)-(1-delta)*log(1-delta)
    extra=max((LOG2/h).hi,(B*LOG2/sigma).hi)
    assert A.hi+extra<F(5197569,10**6)
    print('EXACT certificate R < 5.197569')
    print('A,B,chi,T,mu',*[float(x.hi) for x in (A,B,chi,T,mu)])
    print('a coefficients',{t:float(x.lo) for t,x in a.items()})
    print('zero waiting changes',{k:float(x.hi) for k,x in dz.items()})
    print('ratio upper',float(A.hi+extra))
    return beta,delta,rows


def phase_bounds(beta,u,q,merge,t):
    k0,k1=int(u),int(beta*u)
    budget=beta*u if merge else F(q)
    value=F(q+1,2)
    previous=q
    nextbudget=beta*beta*u if merge else beta*u
    while previous<t:
        current=int(nextbudget)
        value+=F(previous+current,2)
        previous=current
        nextbudget*=beta
    return value


def schedule(beta,u,q,merge,m,demands,sets,kmin):
    order,hit=[],set()
    budget=q
    nextbudget=beta*beta*u if merge else beta*u
    while True:
        chosen=list(sets[min(budget,kmin)])
        while chosen:
            gain={p:sum(w for j,(arc,w) in enumerate(demands) if j not in hit and p in arc)
                  for p in chosen}
            p=max(chosen,key=lambda p:(gain[p],-p))
            chosen.remove(p)
            if gain[p] and p not in order:
                order.append(p)
                hit.update(j for j,(arc,w) in enumerate(demands) if p in arc)
        if budget>=kmin:
            assert len(hit)==len(demands)
            return order
        budget=int(nextbudget)
        nextbudget*=beta


def finite_checks(beta,delta,rows):
    rng=Random(20261107)
    tests=0
    for left,right,opts in rows:
        u=(left+right)/2
        k0,k1=int(u),int(beta*u)
        for weight,q,merge,c,d in opts:
            for t in range(1,30):
                old=phase_bounds(beta,u,k0,False,t)
                new=phase_bounds(beta,u,q,merge,t)
                assert 2*(old-new)==correction(k0,k1,q,merge,t)
            for _ in range(30):
                m=rng.randrange(3,9)
                demands=[]
                for j in range(rng.randrange(1,12)):
                    start,length=rng.randrange(m),rng.randrange(1,m+1)
                    arc={(start+off)%m for off in range(length)}
                    demands.append((arc,rng.randrange(1,10)))
                sets,kmin=oracle(m,demands)
                order=schedule(beta,u,q,merge,m,demands,sets,kmin)
                ranks={p:i+1 for i,p in enumerate(order)}
                actual=sum(w*min(ranks[p] for p in arc if p in ranks) for arc,w in demands)
                for _ in range(5):
                    source=list(range(m));rng.shuffle(source)
                    times=[next(i for i,p in enumerate(source,1) if p in arc) for arc,w in demands]
                    upper=sum(w*phase_bounds(beta,u,q,merge,t) for (arc,w),t in zip(demands,times))
                    assert actual<=upper
                    tests+=1
    print(tests,'finite modified-batch comparison checks passed')


if __name__=='__main__':
    parameters=certificate()
    finite_checks(*parameters)
