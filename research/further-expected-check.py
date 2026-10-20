"""Exploration and exact certificates for further general polynomial E bounds."""
from fractions import Fraction as F
from math import log as mlog, floor, factorial, lgamma, sqrt
from random import Random
from functools import lru_cache
import runpy
import sys

old=runpy.run_path('poly-expected-prefix-opt.py')
discount=old['e']
discount=lru_cache(None)(discount)
golden=old['golden']
helpers=runpy.run_path('poly-expected-check.py')
Bound,log,LOG2=helpers['Bound'],helpers['log'],helpers['LOG2']


def regions(beta):
    breaks={1.,beta}
    for k in range(1,int(beta)+1):
        if 1<k<beta:breaks.add(float(k))
    for k in range(1,int(beta*beta)+1):
        if 1<k/beta<beta:breaks.add(k/beta)
    breaks=sorted(breaks)
    result=[]
    for l,r in zip(breaks,breaks[1:]):
        k0,k1=int((l+r)/2),int(beta*(l+r)/2)
        p=mlog(r/l)/mlog(beta)
        # option=(rank cutoff, slope, intercept multiplier times prefix length)
        strength,penalty=228683/103683,250000/103683
        result.append((l,r,p,[(0,0,0),(k0,1,k0),(k0,strength,penalty*k0),
                              (k1,1,k0+k1),(k1,strength,penalty*(k0+k1))]))
    return result


def profile(beta,regs,weights):
    a=[discount(beta,t) for t in range(1,31)]
    mu=0.
    for (_,_,p,opts),ws in zip(regs,weights):
        for w,(cut,c,dL) in zip(ws,opts):
            mu+=p*w*dL
            for t in range(cut):a[t]+=p*w*c
    return a,mu


def chi(beta,delta,regs,weights):
    a,mu=profile(beta,regs,weights)
    order=sorted(range(len(a)),key=lambda t:a[t])
    N=int(1/(2*delta))
    T=a[order[N]]
    return T-2*delta*sum(max(0,T-at) for at in a)-delta*mu,T,order,a,mu


def ratio(beta,delta,regs,weights):
    saving,T,order,a,mu=chi(beta,delta,regs,weights)
    lb=mlog(beta)
    if T>saving+2/lb+1e-8:return 1000.
    A=2*max((beta+1)/(2*lb),1+1/lb)
    r=int(beta)
    C=4+r-lgamma(r+1)/lb
    B=C-saving
    k=int(1/delta)
    rem=1-k*delta
    sigma=-k*delta*mlog(delta)-(rem*mlog(rem) if rem else 0)
    h=-delta*mlog(delta)-(1-delta)*mlog(1-delta)
    return A+max(mlog(2)/h,B*mlog(2)/sigma)


def optimize_weights(beta,delta,regs,weights,rounds=20):
    for rnd in range(rounds):
        before=chi(beta,delta,regs,weights)[0]
        for j in range(len(regs)):
            for option in range(5):
                start=weights[j][:]
                def score(alpha):
                    weights[j]=[(1-alpha)*x for x in start]
                    weights[j][option]+=alpha
                    return -chi(beta,delta,regs,weights)[0]
                alpha=golden(score,0.,1.,30)
                alpha=min([0.,alpha,1.],key=score)
                score(alpha)
        after=chi(beta,delta,regs,weights)[0]
        if after-before<1e-11:break
    return weights


def simplex_max(A,b,c):
    """Ordinary feasible-start simplex; all b must be nonnegative."""
    nv,nr=len(c),len(b)
    assert all(v>=-1e-10 for v in b)
    rows=[list(row)+[float(i==j) for j in range(nr)]+[max(0.,rhs)]
          for i,(row,rhs) in enumerate(zip(A,b))]
    objective=[-x for x in c]+[0.]*(nr+1)
    bases=list(range(nv,nv+nr))
    for iteration in range(20000):
        enter=next((j for j,v in enumerate(objective[:-1]) if v < -1e-9),None)
        if enter is None:
            solution=[0.]*nv
            for row,base in zip(rows,bases):
                if base<nv:solution[base]=row[-1]
            return objective[-1],solution
        candidates=[(row[-1]/row[enter],bases[i],i)
                    for i,row in enumerate(rows) if row[enter]>1e-9]
        if not candidates:raise ValueError('LP unbounded')
        _,_,pivot=min(candidates)
        scale=rows[pivot][enter]
        rows[pivot]=[x/scale for x in rows[pivot]]
        for i,row in enumerate(rows):
            if i!=pivot and abs(row[enter])>1e-12:
                factor=row[enter]
                rows[i]=[a-factor*v for a,v in zip(row,rows[pivot])]
        factor=objective[enter]
        objective=[a-factor*v for a,v in zip(objective,rows[pivot])]
        bases[pivot]=enter
    raise ValueError('Simplex iteration cap')


def lp_profile(beta,delta,regs):
    # Four nonzero prefix/affine choices per shift region; option0 is slack.
    choices=[(j,opt) for j,reg in enumerate(regs) for opt in range(1,5)]
    nt=30
    nw=len(choices)
    nv=nw+nt+1
    tcol=nw+nt
    constraints,rhs=[],[]
    for j,reg in enumerate(regs):
        row=[0.]*nv
        for i,(jj,opt) in enumerate(choices):
            if jj==j:row[i]=1.
        constraints.append(row);rhs.append(1.)
    for t in range(1,nt+1):
        row=[0.]*nv
        for i,(j,opt) in enumerate(choices):
            p=regs[j][2];cut,c,dL=regs[j][3][opt]
            if t<=cut:row[i]=-p*c
        row[nw+t-1]=-1.
        row[tcol]=1.
        constraints.append(row);rhs.append(max(0.,discount(beta,t)))
    row=[0.]*nv;row[tcol]=1.
    constraints.append(row);rhs.append(discount(beta,nt))
    obj=[0.]*nv
    for i,(j,opt) in enumerate(choices):
        p=regs[j][2];cut,c,dL=regs[j][3][opt]
        obj[i]=-delta*p*dL
    for i in range(nt):obj[nw+i]=-2*delta
    obj[tcol]=1.
    value,sol=simplex_max(constraints,rhs,obj)
    weights=[[0.]*5 for reg in regs]
    for i,(j,opt) in enumerate(choices):weights[j][opt]=max(0.,sol[i])
    for ws in weights:ws[0]=max(0.,1-sum(ws))
    return value,sol[tcol],weights


def explore_lp():
    beta=3512863/1e6
    regs=regions(beta)
    def objective(d):
        value,T,weights=lp_profile(beta,d,regs)
        return ratio(beta,d,regs,weights)
    delta=golden(objective,.12,.18,45)
    value,T,weights=lp_profile(beta,delta,regs)
    print('LP RESULT beta',beta,'delta',delta,'R',ratio(beta,delta,regs,weights),
          'chi',value,'T',T,'profile',chi(beta,delta,regs,weights))
    print('LP WEIGHTS',weights)
    print('LP REGIONS',regs)


def beta_grid():
    best=None
    for i in range(41):
        b=3.4+i*.005
        rs=regions(b)
        v,t,w=lp_profile(b,.1441,rs)
        r=ratio(b,.1441,rs,w)
        if best is None or r<best[0]:best=r,b,v,t,w
    print('fixed-delta grid',best[:4])
    for b in [best[1],3512863/1e6]:
        rs=regions(b)
        d=golden(lambda d:ratio(b,d,rs,lp_profile(b,d,rs)[2]),.13,.16,40)
        print('optimized',b,d,ratio(b,d,rs,lp_profile(b,d,rs)[2]),lp_profile(b,d,rs))


def certified_mixture():
    beta=F(3512863,10**6)
    delta=F(144136826,10**9)
    pstar=F(21317,125000) # .170536
    hstar=1-2*pstar
    h_at=-pstar*log(pstar)-(1-pstar)*log(1-pstar)
    assert (h_at-hstar*LOG2).lo > 0
    c=F(228683,103683)
    d=F(250000,103683)
    assert c==1+1/(1-pstar) and d==2/(1-pstar)
    lb=log(beta)
    assert (Bound(beta-1)-2*lb).lo > 0
    es={1:Bound(0)}
    for t in range(2,7):
        n=(beta*t).numerator//(beta*t).denominator
        integral=t*log(t)-log(factorial(t))
        integral+=(n-3)*lb+n*log(t)-log(F(factorial(n),6))
        es[t]=(Bound((beta+1)*(t-1))-integral)/lb
    eta=F(830027,10**7)
    zeta=F(472577,10**6)
    theta=F(1701301,5*10**6) # .3402602
    # Options contain (mixing weight, source rank cutoff, slope, intercept).
    table=[
        (F(1),4/beta,[(F(1),1,c,d)]),
        (4/beta,5/beta,[(eta,1,c,d),(1-eta,4,F(1),F(5))]),
        (5/beta,6/beta,[(F(1),5,F(1),F(6))]),
        (6/beta,F(2),[(F(1),1,c,d)]),
        (F(2),10/beta,[(F(1),2,F(1),F(2))]),
        (10/beta,F(3),[(zeta,2,F(1),F(2))]),
        (F(3),11/beta,[(theta,3,F(1),F(3)),(1-theta,3,c,3*d)]),
        (11/beta,12/beta,[(F(1),3,c,3*d)]),
        (12/beta,beta,[(F(1),3,F(1),F(3))]),
    ]
    a={t:es[t] for t in range(1,7)}
    mu=Bound(0)
    for left,right,options in table:
        assert left<right
        assert sum(w for w,cut,sl,it in options)<=1
        prob=log(right/left)/lb
        for w,cut,sl,it in options:
            mu+=prob*w*it
            for t in range(1,cut+1):a[t]+=prob*w*sl
    T=Bound(F(345603,250000)) # 1.382412
    assert (T-a[4]).lo > 0
    for t in [1,2,3,5,6]:assert (a[t]-T).lo > 0
    saving=T-2*delta*(T-a[4])-delta*mu
    assert (saving+Bound(2)/lb-T).lo > 0
    A=Bound(beta+1)/lb
    B=7-log(6)/lb-saving
    assert 6<1/delta<7
    rem=1-6*delta
    entropy=-6*delta*log(delta)-rem*log(rem)
    balanced=-delta*log(delta)-(1-delta)*log(1-delta)
    extras=max((LOG2/balanced).hi,(B*LOG2/entropy).hi)
    assert A.hi+extras<F(5272565,10**6)
    print('EXACT certificate R < 5.272565')
    print('p*, h*, c, d',pstar,hstar,c,d)
    print('A,B,chi,T,mu',float(A.hi),float(B.hi),float(saving.lo),float(T.lo),float(mu.hi))
    print('a coefficients',{t:float(at.hi) for t,at in a.items()})
    print('entropy extra',float(extras))
    return beta,delta,pstar,hstar,c,d,table


def finite_credit_checks(parameters):
    beta,delta,pstar,hstar,c,d,table=parameters
    rng=Random(20261023)
    for _ in range(5000):
        xv,yv,zv=[F(rng.randrange(0,101),100) for j in range(3)]
        if xv>yv:xv,yv=yv,xv
        cap=max(xv+zv,yv+zv,F(1,100))
        xv,yv,zv=xv/cap,yv/cap,zv/cap
        m=xv+yv+zv
        extra=min(hstar/pstar*xv,hstar*(xv+zv),hstar/pstar*zv)
        gain=max(yv,xv+yv-zv+extra)
        assert gain>=m-1 and gain>=c*m-d
    print('5000 exact rational block-credit checks passed')


def finite_profile_checks(parameters):
    beta,delta,pstar,hstar,c,d,table=parameters
    b=float(beta);dd=float(delta);lb=mlog(b)
    rng=Random(20261024)
    a=[discount(b,t) for t in range(1,25)]
    mu=0.
    for l,r,opts in table:
        prob=mlog(float(r/l))/lb
        for weight,cut,sl,it in opts:
            mu+=prob*float(weight*it)
            for t in range(cut):a[t]+=prob*float(weight*sl)
    threshold=1.382412
    saving=threshold-2*dd*sum(max(0,threshold-at) for at in a)-dd*mu
    for _ in range(10000):
        masses=[rng.random()*2*dd for t in range(rng.randrange(6,25))]
        scale=min(1,rng.random()/sum(masses))
        masses=[scale*m for m in masses]
        pos=sum(masses)
        pin=0.
        for l,r,opts in table:
            prob=mlog(float(r/l))/lb
            for weight,cut,sl,it in opts:
                pin+=prob*float(weight)*max(0,float(sl)*sum(masses[:cut])-float(it)*dd)
        analytical=sum(m*discount(b,t) for t,m in enumerate(masses,1))
        assert analytical+pin+2*(1-pos)/lb >= saving*pos-2e-7
    print('10000 analytical profile checks passed')


def explore():
    beta=3512863/1e6
    delta=.148
    regs=regions(beta)
    rng=Random(20261019)
    best=None
    for starttype in range(6):
        if starttype<3:
            weights=[[float(j==starttype) for j in range(5)] for reg in regs]
        else:
            weights=[]
            for reg in regs:
                vals=[rng.random() for j in range(5)]
                weights.append([x/sum(vals) for x in vals])
        d=delta
        for _ in range(6):
            weights=optimize_weights(beta,d,regs,weights)
            d=golden(lambda d:ratio(beta,d,regs,weights),.12,.18,60)
        value=ratio(beta,d,regs,weights)
        if best is None or value<best[0]:best=value,d,[w[:] for w in weights]
        print('start',starttype,'R',value,'delta',d)
    value,d,weights=best
    print('BEST',value,d,'profile',chi(beta,d,regs,weights))
    print('WEIGHTS',weights)
    print('REGIONS',regs)


if __name__=='__main__':
    if '--beta-grid' in sys.argv:beta_grid()
    elif '--explore' in sys.argv:explore_lp()
    else:
        params=certified_mixture()
        finite_credit_checks(params)
        finite_profile_checks(params)
