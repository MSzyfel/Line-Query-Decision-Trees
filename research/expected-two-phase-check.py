"""Exact fixed-table certificate for two initial geometric-batch budgets."""
from fractions import Fraction as F
from math import factorial
import json,runpy
from pathlib import Path
helpers=runpy.run_path('poly-expected-check.py')
Bound,log,LOG2=helpers['Bound'],helpers['log'],helpers['LOG2']


def correction(k0,k1,k2,q,r,t):
    if r:
        return k0-q+(k0+k1)*(t>k0)-(q+r)*(t>q)+(k1+k2)*(t>k1)-(r+k2)*(t>r)
    return k0-q+(k0+k1)*(t>k0)+(k1+k2)*(t>k1)-(q+k2)*(t>q)


def certificate():
    data=json.loads(Path('expected-two-phase-certificate.json').read_text())
    beta,delta,tau=map(F,(data['beta'],data['delta'],data['tau']))
    lb=log(beta);nt=16;c,d=F(228683,103683),F(250000,103683)
    assert (Bound(beta-1)-2*lb).lo>F('0.000000250968')
    pstar=F(21317,125000);hstar=1-2*pstar
    assert c==(2-pstar)/(1-pstar) and d==2/(1-pstar)
    assert (-pstar*log(pstar)-(1-pstar)*log(1-pstar)-hstar*LOG2).lo>F('0.000001006640')
    e={1:Bound(0)}
    for t in range(2,nt+1):
        n=int(beta*t)
        integral=t*log(t)-log(factorial(t))
        integral+=(n-3)*lb+n*log(t)-log(F(factorial(n),6))
        e[t]=(Bound((beta+1)*(t-1))-integral)/lb
    a=e.copy();mu=Bound(0);dz={k:Bound(0) for k in range(1,15)}
    pos=F(1)
    for row in data['rows']:
        l,h=F(row['l']),F(row['h']);k0,k1,k2=row['k0'],row['k1'],row['k2']
        assert l==pos and l<h
        pos=h
        # Floors are monotone; the largest value below the excluded
        # right endpoint is ceil(beta**j*h)-1. Check the entire row.
        for j,expected in enumerate((k0,k1,k2)):
            left,right=beta**j*l,beta**j*h
            largest=(right.numerator+right.denominator-1)//right.denominator-1
            assert int(left)==largest==expected
        assert sum(F(opt['v']) for opt in row['opts'])==1
        prob=log(h/l)/lb
        if l==1:
            assert prob.lo>F('0.041455991537') and prob.hi<F('0.041455991538')
        for opt in row['opts']:
            v=F(opt['v']);q,r,cut=opt['q'],opt['r'],opt['cut'];credit=opt['credit']
            assert v>=0 and 1<=q<=6 and (r==0 or q<r<k2 and r in {k1-1,k1,k1+1})
            assert cut==q  # The published proof uses only first-batch credit.
            if credit=='C':s,inter=c,d*(q+r if cut==r else q)
            elif credit=='A':s,inter=F(1),F(q+r if cut==r else q)
            elif credit=='zero':s,inter=F(0),F(0)
            else:raise AssertionError('Unexpected credit')
            mu+=prob*v*inter
            for t in range(1,nt+1):a[t]+=prob*v*(correction(k0,k1,k2,q,r,t)+s*(t<=cut))
            for k in dz:dz[k]+=prob*v*(q*(q<k)+r*(r<k)-k0*(k0<k)-k1*(k1<k))
    assert pos==beta
    exceptions=[t for t in a if a[t].hi<tau]
    assert exceptions==[1]
    assert all(a[t].lo>=tau for t in a if t not in exceptions)
    assert a[1].lo>F('1.276476788627') and a[1].hi<F('1.276476788629')
    assert min(a[t].lo for t in range(2,15))>F('2.1900797')
    assert mu.lo>F('4.461183727319') and mu.hi<F('4.461183727320')
    short=sum((Bound(tau)-a[t] for t in exceptions),Bound(0))
    chi=Bound(tau)-2*delta*short-delta*mu
    maxchange=max(x.hi for x in dz.values())
    assert dz[1].lo==dz[1].hi==0
    assert max(dz[k].hi for k in range(2,15))<F('-0.06992')
    assert maxchange==0
    zeta=Bound(2)/lb-2*maxchange
    # All possible q<=6, r<=13,k0<=3,k1<=12, so k>=14 has dz(14).
    assert (chi+zeta-tau).lo>0
    assert chi.lo>F('1.199202587061')
    # Signed corrections are constant for t>=14; remaining e(t) is monotone.
    assert a[14].lo>tau
    A=Bound(beta+1)/lb;B=7-log(6)/lb-chi
    k=int(1/delta);rem=1-k*delta
    sigma=-k*delta*log(delta)-rem*log(rem)
    h=-delta*log(delta)-(1-delta)*log(1-delta)
    assert A.lo>2 and B.lo>2 and B.hi<F('4.374727111314')
    assert lb.lo>F('1.256431374515') and lb.hi<F('1.256431374516')
    assert h.lo>F('0.435622350180') and h.hi<F('0.435622350181')
    assert sigma.lo>F('1.905736047002') and sigma.hi<F('1.905736047003')
    # Exact outward decimal endpoints displayed in the calibration table.
    rank_lower=list(map(F,('1.276476788627','2.190079716489','2.190079716462',
        '2.190079716311','2.190079716316','2.190079716371','2.190079716472',
        '2.190079716131','2.190079716691','2.190079716422','2.190079716565',
        '2.190079716480','2.190079716692','2.190079716520')))
    wait_upper=list(map(F,('0','-0.246077347242','-0.308016911051',
        '-0.339177879272','-0.313280064542','-0.261411526812','-0.219499207512',
        '-0.186529025533','-0.158717650632','-0.135101669420','-0.115461022418',
        '-0.097796497729','-0.083683085595','-0.069926303070')))
    assert all(a[t].lo>=value for t,value in enumerate(rank_lower,1))
    assert all(dz[k].hi<=value for k,value in enumerate(wait_upper,1))
    upper=A.hi+max((LOG2/h).hi,(B*LOG2/sigma).hi)
    print('exceptions',exceptions)
    print('a',[(t,float(x.lo),float(x.hi)) for t,x in a.items()])
    print('mu chi B zeta zerogap',*[float(x.hi) for x in (mu,chi,B,zeta,chi+zeta-tau)])
    print('dz',[(k,float(x.lo),float(x.hi)) for k,x in dz.items()])
    print('R upper',float(upper))
    assert upper<F(5182975508794,10**12)<F(5182976,10**6)
    print(len(data['rows']),'entire half-open rows and all published strict rational bounds passed')
    return data


def phase_bound(beta,u,q,r,t):
    budgets=[q]+([r] if r else [])
    power=beta*beta*u
    while budgets[-1]<t:
        budgets.append(int(power));power*=beta
    value=F(q+1,2)
    for prev,current in zip(budgets,budgets[1:]):
        if t>prev:value+=F(prev+current,2)
    return value


def finite_checks(data):
    from random import Random
    rng=Random(20261013)
    beta=F(data['beta']);oracle=helpers['candidate_sets']
    identity_count=batch_count=0
    for row in data['rows']:
        left,right=F(row['l']),F(row['h'])
        # Cover both row endpoints from within and the midpoint.
        for u in [(999*left+right)/1000,(left+right)/2,(left+999*right)/1000]:
            k0,k1,k2=int(u),int(beta*u),int(beta*beta*u)
            assert (k0,k1,k2)==(row['k0'],row['k1'],row['k2'])
            for opt in row['opts']:
                q,r=opt['q'],opt['r']
                for t in range(1,61):
                    old=phase_bound(beta,u,k0,k1,t)
                    new=phase_bound(beta,u,q,r,t)
                    assert 2*(old-new)==correction(k0,k1,k2,q,r,t)
                    identity_count+=1
                for _ in range(2):
                    m=rng.randrange(3,9)
                    demands=[]
                    for _ in range(rng.randrange(1,13)):
                        start,length=rng.randrange(m),rng.randrange(1,m+1)
                        demands.append(({(start+j)%m for j in range(length)},rng.randrange(1,12)))
                    sets,kmin=oracle(m,demands)
                    order=[];hit=set();budgets=[q]+([r] if r else [])
                    power=beta*beta*u
                    while budgets[-1]<kmin:
                        budgets.append(int(power));power*=beta
                    for budget in budgets:
                        selected=list(sets[min(budget,kmin)])
                        while selected:
                            gains={p:sum(w for j,(arc,w) in enumerate(demands) if j not in hit and p in arc) for p in selected}
                            p=max(selected,key=lambda p:(gains[p],-p));selected.remove(p)
                            if gains[p] and p not in order:
                                order.append(p);hit.update(j for j,(arc,w) in enumerate(demands) if p in arc)
                        if budget>=kmin:break
                    assert len(hit)==len(demands)
                    # Executed length is bounded by the full all-negative invoice.
                    old_length=kmin
                    old_power=u
                    while int(old_power)<kmin:
                        old_length+=int(old_power);old_power*=beta
                    dz=q*(q<kmin)+r*(r<kmin)-k0*(k0<kmin)-k1*(k1<kmin)
                    assert len(order)<=old_length+dz
                    ranks={p:i+1 for i,p in enumerate(order)}
                    actual=sum(w*min(ranks[p] for p in arc if p in ranks) for arc,w in demands)
                    for _ in range(5):
                        source=list(range(m));rng.shuffle(source)
                        times=[next(i for i,p in enumerate(source,1) if p in arc) for arc,w in demands]
                        upper=sum(w*phase_bound(beta,u,q,r,t) for (arc,w),t in zip(demands,times))
                        assert actual<=upper
                        batch_count+=1
    print(identity_count,'exact phase identities;',batch_count,'finite batch/early-completion checks passed')

if __name__=='__main__':
    data=certificate()
    finite_checks(data)

