"""Exact coefficient certificate for the first-batch orientation improvement."""
from fractions import Fraction as F
from math import factorial, log as math_log, floor, lgamma
from random import Random
import runpy

helpers = runpy.run_path('poly-expected-check.py')
Bound, log, LOG2 = helpers['Bound'], helpers['log'], helpers['LOG2']


def certificate():
    beta = F(3512863, 10**6)
    delta = F(142275675, 10**9)
    lb = log(beta)
    assert (Bound(beta-1)-2*lb).lo > 0
    e = [Bound(0)]
    for t in range(2, 5):
        n = (beta*t).numerator // (beta*t).denominator
        integral = t*log(t)-log(factorial(t))
        integral += (n-3)*lb+n*log(t)-log(F(factorial(n),6))
        e.append((Bound((beta+1)*(t-1))-integral)/lb)
    P1 = LOG2/lb
    P3 = log(beta/3)/lb
    a = [Bound(1), e[1]+1-P1, e[2]+P3]
    for at in a:
        assert (e[3]-at).lo > 0
    mu = 3-log(6)/lb
    chi = 2*delta*(e[1]+e[2])+(1-6*delta)*e[3]+delta*mu
    assert (chi+Bound(2)/lb-e[3]).lo > 0
    A = Bound(beta+1)/lb
    B = 7-log(6)/lb-chi
    assert 3 < 1/(2*delta) < 4 and 7 < 1/delta < 8
    rem = 1-7*delta
    h = -delta*log(delta)-(1-delta)*log(1-delta)
    sigma = -7*delta*log(delta)-rem*log(rem)
    ratio = max((LOG2/h).hi,(B*LOG2/sigma).hi)
    assert A.hi+ratio < F(5286244,10**6)
    print('Exact rational certificate: R < 5.286244.')
    print('A',float(A.hi),'B',float(B.hi),'entropy ratio',float(ratio))
    print('chi',float(chi.lo),'orientation bonus',float((delta*mu).lo))
    print('threshold gaps',[float((e[3]-at).lo) for at in a])


def profile_checks():
    beta = 3512863/10**6
    delta = 142275675/10**9
    lb = math_log(beta)

    def primitive(y):
        k=floor(y+1e-12)
        return k*math_log(y)-lgamma(k+1)

    def e(t):
        return ((beta+1)*(t-1)-primitive(t)-primitive(beta*t)+primitive(beta))/lb

    probs=[math_log(2)/lb,math_log(3/2)/lb,math_log(beta/3)/lb]
    chi=2*delta*(e(2)+e(3))+(1-6*delta)*e(4)+delta*sum(k*p for k,p in enumerate(probs,1))
    rng=Random(20261017)
    for _ in range(10000):
        raw=[rng.random()*2*delta for t in range(rng.randrange(4,20))]
        scale=rng.random()/sum(raw)
        scale=min(scale,1)
        masses=[scale*x for x in raw]
        b=sum(masses)
        discount=sum(m*e(t) for t,m in enumerate(masses,1))
        orient=sum(p*max(0,sum(masses[:k])-k*delta) for k,p in enumerate(probs,1))
        assert discount+orient+2*(1-b)/lb >= chi*b-1e-10
    print('10,000 source profiles passed the combined orientation/discrete/zero bound.')


def actual_block_checks():
    rng=Random(20261018)
    checked=0
    for vcount in range(3,15):
        for _ in range(100):
            demands=[]
            for j in range(rng.randrange(1,20)):
                start,length=rng.randrange(vcount),rng.randrange(1,vcount)
                arc={(start+k)%vcount for k in range(length)}
                demands.append((arc,rng.randrange(1,10)))
            cap=max(sum(w for arc,w in demands if v in arc) for v in range(vcount))
            remaining=set(range(len(demands)))
            pin,hit=0,0
            order=list(range(vcount))
            rng.shuffle(order)
            for rank,v in enumerate(order,1):
                nxt=(v+1)%vcount
                x=sum(demands[j][1] for j in remaining if v in demands[j][0] and nxt not in demands[j][0])
                y=sum(demands[j][1] for j in remaining if nxt in demands[j][0] and v not in demands[j][0])
                z=sum(demands[j][1] for j in remaining if v in demands[j][0] and nxt in demands[j][0])
                pin+=max(x,y)
                hit+=x+y+z
                assert max(x,y)>=max(0,x+y+z-cap)
                assert pin>=max(0,hit-rank*cap)
                remaining={j for j in remaining if v not in demands[j][0] and nxt not in demands[j][0]}
            checked+=1
    print(f'{checked} actual circular block profiles passed pin/prefix inequalities.')


def mixed_prefix_certificate():
    beta = F(3512863,10**6)
    delta = F(142671046,10**9)
    alpha0,alpha1 = F(7963376,10**7),F(952407,10**6)
    lb=log(beta)
    es={1:Bound(0)}
    for t in range(2,7):
        n=(beta*t).numerator//(beta*t).denominator
        integral=t*log(t)-log(factorial(t))
        integral+=(n-3)*lb+n*log(t)-log(F(factorial(n),6))
        es[t]=(Bound((beta+1)*(t-1))-integral)/lb
    P1=LOG2/lb
    P3=log(beta/3)/lb
    q0=alpha0*log(4/beta)/lb
    q1=alpha1*log(F(5,4))/lb
    q2=log(F(6,5))/lb
    a={1:Bound(1),2:es[2]+1-P1+q0+q1+q2,
       3:es[3]+P3+q0+q1+q2,
       4:es[4]+q1+q2,5:es[5]+q2,6:es[6]}
    T=Bound(F(345603,250000))  # 1.382412, slightly below near-tied a2,a4,a5
    # Only indices 1,3 lie below this rational threshold. All t>=6
    # have e(t)>=e(6), by the established monotonicity of e.
    for t in [1,3]: assert (T-a[t]).lo > 0
    for t in [2,4,5,6]: assert (a[t]-T).lo > 0
    mu=3-log(6)/lb+3*q0+4*q1+5*q2
    chi=T-2*delta*sum((T-a[t] for t in [1,3]),Bound(0))-delta*mu
    assert (chi+Bound(2)/lb-T).lo > 0
    A=Bound(beta+1)/lb
    B=7-log(6)/lb-chi
    rem=1-7*delta
    h=-delta*log(delta)-(1-delta)*log(1-delta)
    sigma=-7*delta*log(delta)-rem*log(rem)
    ratio=max((LOG2/h).hi,(B*LOG2/sigma).hi)
    assert A.hi+ratio < F(5283310,10**6)
    print('Mixed-prefix exact rational certificate: R < 5.283310.')
    print('A',float(A.hi),'B',float(B.hi),'chi',float(chi.lo),'T',float(T.hi))
    print('mu',float(mu.hi),'entropy ratio',float(ratio))
    print('mixed coefficients',{t:float(at.hi) for t,at in a.items()})


def mixed_profile_checks():
    beta=3512863/10**6
    delta=142671046/10**9
    alpha0,alpha1=7963376/10**7,952407/10**6
    lb=math_log(beta)
    opt=runpy.run_path('poly-expected-prefix-opt.py')
    regions,_=opt['profiles'](beta)
    alphas=[alpha0,alpha1,1.]+[0.]*(len(regions)-3)
    record=opt['mixed_record'](beta,regions,alphas)
    R,chi,mask,order,mu,values,B=opt['best_score'](beta,delta,record)
    ef=opt['e']
    rng=Random(20261019)
    for _ in range(10000):
        raw=[rng.random()*2*delta for t in range(rng.randrange(6,22))]
        scale=min(1,rng.random()/sum(raw))
        masses=[scale*x for x in raw]
        b=sum(masses)
        discount=sum(m*ef(beta,t) for t,m in enumerate(masses,1))
        pin=0
        for (_,_,p,k0,k1),alpha in zip(regions,alphas):
            first=max(0,sum(masses[:k0])-delta*k0)
            second=max(0,sum(masses[:k1])-delta*(k0+k1))
            pin+=p*((1-alpha)*first+alpha*second)
        assert discount+pin+2*(1-b)/lb >= chi*b-1e-10
    print('10,000 source profiles passed the mixed-prefix combined saving bound.')


if __name__=='__main__':
    certificate()
    profile_checks()
    actual_block_checks()
    mixed_prefix_certificate()
    mixed_profile_checks()
