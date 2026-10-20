"""Independent actual-circle, exact-cover, and shift-transfer verification."""
from fractions import Fraction as F
from itertools import combinations
from math import log, lgamma
from random import Random

BETA=F(3512863,10**6)
DELTA=F(144136826,10**9)
ANCHOR=F(21317,125000)
HEIGHT=1-2*ANCHOR
STRENGTH=F(228683,103683)
PENALTY=F(250000,103683)
ETA,ZETA,THETA=F(830027,10**7),F(472577,10**6),F(1701301,5*10**6)
TABLE=[
    (F(1),4/BETA,[(F(1),1,STRENGTH,PENALTY)]),
    (4/BETA,5/BETA,[(ETA,1,STRENGTH,PENALTY),(1-ETA,4,F(1),F(5))]),
    (5/BETA,6/BETA,[(F(1),5,F(1),F(6))]),
    (6/BETA,F(2),[(F(1),1,STRENGTH,PENALTY)]),
    (F(2),10/BETA,[(F(1),2,F(1),F(2))]),
    (10/BETA,F(3),[(ZETA,2,F(1),F(2))]),
    (F(3),11/BETA,[(THETA,3,F(1),F(3)),(1-THETA,3,STRENGTH,3*PENALTY)]),
    (11/BETA,12/BETA,[(F(1),3,STRENGTH,3*PENALTY)]),
    (12/BETA,BETA,[(F(1),3,F(1),F(3))]),
]


def covers(blocks,demands,m):
    vertices={v for q in blocks for v in (q,(q+1)%m)}
    return {j for j,(arc,weight) in enumerate(demands) if arc&vertices}


def oracle(m,demands):
    all_sets=[]
    for size in range(m+1):
        for selected in combinations(range(m),size):
            hit=covers(selected,demands,m)
            profit=sum(demands[j][1] for j in hit)
            all_sets.append((selected,profit))
    total=sum(weight for arc,weight in demands)
    k0=min(len(selected) for selected,profit in all_sets if profit==total)
    best={}
    for k in range(1,k0+1):
        best[k]=max((record for record in all_sets if len(record[0])<=k),
                    key=lambda record:(record[1],-len(record[0]),record[0]))[0]
    return best,k0


def entropy(cells,total):
    return sum(float(mass)*log(float(total/mass)) for mass in cells if mass)


def schedule(shift,m,demands,best,k0,zero,total):
    remaining=set(range(len(demands)))
    query_blocks=[]
    physical=F(0)
    gain=F(0)
    actual_cells=[]
    virtual_cells=[]
    information_bonus=0.
    u=shift
    while True:
        k=u.numerator//u.denominator
        candidates=list(best[min(k,k0)])
        while candidates:
            def new_mass(q):
                return sum(demands[j][1] for j in remaining
                           if q in demands[j][0] or (q+1)%m in demands[j][0])
            q=max(candidates,key=lambda q:(new_mass(q),-q))
            candidates.remove(q)
            if not new_mass(q):
                continue
            x=y=z=F(0)
            newly=[]
            for j in remaining:
                arc,weight=demands[j]
                if q in arc and (q+1)%m in arc:
                    z+=weight;newly.append(j)
                elif q in arc:
                    x+=weight;newly.append(j)
                elif (q+1)%m in arc:
                    y+=weight;newly.append(j)
            if x>y:x,y=y,x
            mass=x+y+z
            assert x+z<DELTA*total and y<DELTA*total
            tent=min(HEIGHT/ANCHOR*x,HEIGHT/ANCHOR*z,HEIGHT*(x+z))
            both_gain=x+y-z+tent
            both=both_gain>y
            discount=both_gain if both else y
            assert discount>=max(0,mass-DELTA*total,
                                 STRENGTH*mass-PENALTY*DELTA*total)
            query_blocks.append(q)
            rank=len(query_blocks)
            gain+=discount
            if both:
                physical+=(2*rank+2)*(x+y)+(2*rank+4)*z
                actual_cells.extend([x,y,z])
                extra=entropy([x,z],x+z) if x+z else 0.
                information_bonus+=extra
                assert float(tent)*log(2)<=extra+1e-10
            else:
                physical+=(2*rank+3)*mass-y
                actual_cells.extend([x+z,y])
            virtual_cells.extend([x+z,y])
            remaining.difference_update(newly)
        if k>=k0:
            assert not remaining
            break
        u*=BETA
    actual_cells.append(zero)
    virtual_cells.append(zero)
    ja=entropy(actual_cells,total)
    jv=entropy(virtual_cells,total)
    assert abs((ja-jv)-information_bonus)<1e-8
    ranks={q:t+1 for t,q in enumerate(query_blocks)}
    first_cost=sum(weight*min(ranks[q] for q in query_blocks
                             if q in arc or (q+1)%m in arc)
                   for arc,weight in demands)
    b=sum(weight for arc,weight in demands)
    assert float(physical)-information_bonus/log(2)<=float(2*first_cost+3*b-gain)+1e-8
    surrogate=2*first_cost+2*zero*len(query_blocks)-gain
    return gain,surrogate,len(query_blocks)


def run_checks():
    rng=Random(20261025)
    cases=rows=schedules=0
    beta=float(BETA);lb=log(beta)
    strength=float(STRENGTH)
    phi1=2-log(6)/(2*lb)
    lam=(beta+1)/(2*lb)
    coefficient=[0.]*31
    mu=0.
    for left,right,choices in TABLE:
        prob=log(float(right/left))/lb
        for weight,cut,slope,intercept in choices:
            mu+=prob*float(weight*intercept)
            for t in range(cut):coefficient[t]+=prob*float(weight*slope)
    def primitive(value):
        integer=int(value+1e-12)
        return integer*log(value)-lgamma(integer+1)
    def e(t):
        return ((beta+1)*(t-1)-primitive(t)-primitive(beta*t)+primitive(beta))/lb
    at=[e(t)+coefficient[t-1] for t in range(1,31)]
    threshold=1.382412
    chi=threshold-2*float(DELTA)*sum(max(0,threshold-value) for value in at)-float(DELTA)*mu
    B=3+2*phi1-chi
    for m in range(4,10):
        for _ in range(25):
            merged={}
            for _ in range(rng.randrange(2,20)):
                start,length=rng.randrange(m),rng.randrange(1,m//2+1)
                arc=frozenset((start+j)%m for j in range(length))
                merged[arc]=merged.get(arc,F(0))+rng.randrange(1,10)
            demands=list(merged.items())
            b=sum(weight for arc,weight in demands)
            cap=max(sum(weight for arc,weight in demands if v in arc) for v in range(m))
            total=max(F(b+1),F(cap)/DELTA+1)
            zero=total-b
            best,k0=oracle(m,demands)
            source=list(range(m));rng.shuffle(source)
            source_hit=set();mass_by_rank=[]
            for q in source:
                new=covers([q],demands,m)-source_hit
                mass_by_rank.append(sum(demands[j][1] for j in new))
                source_hit.update(new)
                if len(source_hit)==len(demands):break
            qcount=len(mass_by_rank)
            assert all(mass<=2*DELTA*total for mass in mass_by_rank)
            for left,right,choices in TABLE:
                gain,_,_=schedule((left+right)/2,m,demands,best,k0,zero,total)
                lower=F(0)
                for weight,cut,slope,intercept in choices:
                    mk=sum(mass_by_rank[:cut])
                    bound=slope*mk-intercept*DELTA*total
                    assert gain>=bound
                    lower+=weight*bound
                assert gain>=lower
                rows+=1
            breaks={F(1),BETA}
            scale=F(1)
            while scale<=BETA*k0:
                for integer in range(1,k0+1):
                    value=F(integer)/scale
                    if 1<value<BETA:breaks.add(value)
                scale*=BETA
            breaks=sorted(breaks)
            average_surrogate=average_gain=0.
            for left,right in zip(breaks,breaks[1:]):
                gain,surrogate,_=schedule((left+right)/2,m,demands,best,k0,zero,total)
                prob=log(float(right/left))/lb
                average_surrogate+=prob*float(surrogate)
                average_gain+=prob*float(gain)
                schedules+=1
            averaged_linear=sum(float(mass)*coefficient[t]
                                for t,mass in enumerate(mass_by_rank))-float(DELTA*total)*mu
            assert average_gain>=averaged_linear-1e-8
            dplus=sum(float(mass)*t for t,mass in enumerate(mass_by_rank))
            delta_comparison=dplus+float(zero)*qcount
            assert average_surrogate<=2*lam*delta_comparison+(B-3)*float(b)+1e-7
            cases+=1
    print(f'{cases} actual circular instances, {rows} exact table-row transfers, '
          f'{schedules} complete shift schedules passed.')
    print('Virtual entropy identities, exact rational mode credits, and combined shift bounds passed.')


if __name__=='__main__':run_checks()
