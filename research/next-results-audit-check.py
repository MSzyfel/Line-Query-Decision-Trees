"""Independent Bellman, geometry, and changed-batch schedule checks.

The theorem constants have a separate exact logarithm certificate. All local
costs and discrete transfer inequalities here use integers or Fractions;
supplementary entropy and averaged shift checks use floating-point tolerances.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import log
from random import Random


BETA=F(3512863,10**6)
DELTA=F(155223384,10**9)
P=F(21317,125000)
H=1-2*P
C,D=F(228683,103683),F(250000,103683)
V1,V2,V3,V4,V5=(F(x,10**8) for x in
                (95240701,37279986,4271137,33933837,36583316))
ROWS=[
    (F(1),4/BETA,[(F(1),3,True,C,3*D)]),
    (4/BETA,5/BETA,[(V1,4,True,F(1),F(4)),(1-V1,4,True,F(0),F(0))]),
    (5/BETA,F(2),[(F(1),1,False,C,D)]),
    (F(2),8/BETA,[(V2,1,False,C,D),(1-V2,2,False,C,2*D)]),
    (8/BETA,F(3),[(F(1),2,False,C,2*D)]),
    (F(3),11/BETA,[(V3,2,False,C,2*D),(1-V3,3,False,C,3*D)]),
    (11/BETA,12/BETA,[(F(1),3,False,C,3*D)]),
    (12/BETA,BETA,[(V4,3,False,C,3*D),(V5,5,False,F(1),F(5)),
                      (1-V4-V5,6,False,F(0),F(0))]),
]


def bellman(weights,caps):
    """Full adaptive optimum; no matching or spine normalization is assumed."""
    @lru_cache(None)
    def weight(mask):
        return sum(w for i,w in enumerate(weights) if mask>>i&1)
    @lru_cache(None)
    def solve(mask):
        if mask.bit_count()<=1:return 0
        hitset={mask&cap for cap in caps}-{0,mask}
        assert hitset
        return weight(mask)+min(solve(hit)+solve(mask^hit) for hit in hitset)
    return solve((1<<len(weights))-1)


def completion(masses):
    return sum(t*w for t,w in enumerate(sorted(masses,reverse=True),1))


def invoice(weights,edges):
    best=None
    for subset in range(1<<len(edges)):
        used=set();groups=[];pairmass=0
        for i,(u,v) in enumerate(edges):
            if not subset>>i&1:continue
            if u in used or v in used:break
            used.update((u,v));mass=weights[u]+weights[v]
            groups.append(mass);pairmass+=mass
        else:
            pairs=len(groups)
            groups.extend(weights[i] for i in range(1,len(weights)) if i not in used)
            value=weights[0]*(len(weights)-1-pairs)+completion(groups)+pairmass
            best=value if best is None else min(best,value)
    return best


def cloud_checks():
    rng=Random(20261029)
    cases=rotations=0
    for _ in range(100):
        vertices=rng.randrange(1,7)
        weights=[rng.randrange(1,6) for _ in range(vertices+1)]
        while sum(weights)>16:
            i=rng.randrange(len(weights))
            if weights[i]>1:weights[i]-=1
        edges=[(i,i+1) for i in range(1,vertices) if rng.randrange(2)]
        caps=[1<<i for i in range(1,len(weights))]
        caps.extend((1<<u)|(1<<v) for u,v in edges)
        raw=bellman(weights,caps)
        assert raw==invoice(weights,edges)
        cloudcaps=[];clouds=[];points=[]
        scale=4*max(weights)
        for i,w in enumerate(weights):
            cloudmask=0
            for j in range(w):
                bit=1<<len(points);points.append((scale*i+j,i,j))
                cloudmask|=bit
                if j:cloudcaps.append(bit)
            clouds.append(cloudmask)
        cloudcaps.extend(clouds[1:])
        cloudcaps.extend(clouds[u]|clouds[v] for u,v in edges)
        extra=sum((w-1)*(w+2)//2 for w in weights)
        assert bellman([1]*len(points),cloudcaps)==raw+extra
        for a,b in [(i,i) for i in range(1,len(weights))]+edges:
            expected=clouds[a] if a==b else clouds[a]|clouds[b]
            actual=0
            for t,(x,_,_) in enumerate(points):
                value=4*x*x-4*scale*(a+b)*x+scale*scale*(2*a-1)*(2*b+1)
                assert value
                if value<0:actual|=1<<t
            assert actual==expected
        for t,(x,_,j) in enumerate(points):
            if not j:continue
            for s,(y,_,_) in enumerate(points):
                value=2*y*y-4*x*y+2*x*x-1
                assert value and (value<0)==(s==t)
        # Check the local exchange on independently sampled states and roots.
        allmask=(1<<len(points))-1
        for _ in range(20):
            state=rng.randrange(1,allmask+1)
            if state.bit_count()<3:continue
            singles=[cap for cap in cloudcaps if (state&cap).bit_count()==1]
            for cap in singles:
                isolated=state&cap
                rest=state^isolated
                for nextcap in cloudcaps:
                    a,b=rest&nextcap,rest&~nextcap
                    if not a or not b:continue
                    if not isolated&nextcap:a,b=b,a
                    before=state.bit_count()+rest.bit_count()
                    after=state.bit_count()+a.bit_count()+1
                    assert after-before==1-b.bit_count()<=0
                    rotations+=1
        cases+=1
    print(cases,'independent full weighted/cloud Bellman and geometry checks;',
          rotations,'singleton-exchange checks passed')


def quantitative_checks():
    rng=Random(20261030)
    for _ in range(40):
        p=rng.randrange(2,7);unit=rng.randrange(9,13)
        items=[]
        for _ in range(p):
            a,b=rng.randrange(-1,2),rng.randrange(-1,2)
            items.extend((unit+a,unit+b,unit-a-b))
        m=len(items);s=sum(items);target=s//p
        assert all(target/4<x<target/2 for x in items)
        q=2*s*(p-1);baseline=q-s
        r=1000*((p+10)*(q+m+1)**2+(q*m*p+2*m+1)*baseline*max(items)+1)
        scale=2000*m*(r+q+m+1)
        adjustments=[[scale*(baseline-(baseline if b==1 else 2*s*(p-b)))*a
                      //(q+r+m-i) for b in range(1,p+1)]
                     for i,a in enumerate(items,1)]
        biggest=max(map(max,adjustments))
        bases=[1+(2*biggest+1)*i for i in range(1,m+1)]
        pathweights=[];reference=[]
        for i,(a,base) in enumerate(zip(items,bases)):
            length=2*a*(p-1)
            even0=[base if j%(2*a)==0 else base+(1 if j%2 else 2)*scale
                   for j in range(length+1)]
            even=even0[:]
            for b in range(p):even[2*a*b]+=adjustments[i][b]
            odd=[]
            for j in range(1,length+1):
                b=(j-1)//(2*a)+1
                odd.append((10+2*b)*scale-even0[j-1] if even0[j]>even0[j-1]
                           else (10+2*(b+1))*scale-even0[j])
            pathweights.extend(even+odd)
            reference.extend(odd[j-1]+even[j] for j in range(1,length+1))
        assert len(pathweights)==2*q+m
        assert max(pathweights)<=(10+2*p)*scale
        totalpath=sum(pathweights);forest=totalpath+r*(scale//2)
        vertices=2*q+m+r;count0=vertices+1
        witness=(vertices+1)*forest+1
        population=forest+witness
        eplus=q*sum(map(sum,adjustments))
        eminus=sum(q+r+m-i-1 for i in range(1,m+1))
        assert eplus<=scale//1000 and eminus<F(scale,2000)
        assert forest<r*scale and population<=count0*count0*scale
        assert vertices+2<=2*r and scale<=population<=scale**3
        assert population*110**3<scale**3
        fixed=witness*(q+m+r)+(scale//2)*r*(r+1)//2+q*r*(scale//2)+totalpath
        boundary=fixed+completion(reference)+completion(bases)+(q-1+r)*sum(bases)
        # Unperturbed reference masses for the threshold's fixed histogram.
        unperturbed=[]
        for a in items:
            for b in range(1,p):
                unperturbed.extend([(11+2*b)*scale]*a+[(12+2*b)*scale]*a)
        threshold=fixed+sum((q+r+m-i)*base for i,base in enumerate(bases,1))
        threshold+=completion(unperturbed)+scale*(p*target*target-s*s)//2+eplus
        assert threshold<=boundary+eminus+eplus<count0**3*scale
        added=sum((w-1)*(w+2)//2 for w in pathweights)
        added+=r*((scale//2-1)*(scale//2+2)//2)+(witness-1)*(witness+2)//2
        assert threshold+added<population*population
        gap=scale-eminus-eplus
        assert gap>=F(1997,2000)*scale
        assert F(9,10)*scale<gap and F(10,11)*scale<gap
        internal=(F(r,3)-(p+8)*(q+m+1)**2)*scale
        assert internal>scale
        # W proof's count-independent inequality, with its different q.
        u=2*s*(p-1);q_w=(p-1)*(4*s+2*m);aux=m+2
        assert q_w<=3*u and aux<=u and q_w+aux<=4*u
        assert (q_w+aux)**2<= (3*u+aux)**2<9*u*(u+aux)
    print('40 nonuniform explicit parameter constructions passed all gap/size bounds')


def covered(blocks,demands,m):
    endpoints={v for e in blocks for v in (e,(e+1)%m)}
    return {i for i,(arc,w) in enumerate(demands) if arc&endpoints}


def cover_oracle(m,demands):
    records=[]
    for size in range(m+1):
        for selected in combinations(range(m),size):
            hit=covered(selected,demands,m)
            records.append((selected,sum(demands[i][1] for i in hit)))
    b=sum(w for arc,w in demands)
    minimum=min(len(selected) for selected,profit in records if profit==b)
    best={k:max((record for record in records if len(record[0])<=k),
                key=lambda record:(record[1],-len(record[0]),record[0]))[0]
          for k in range(1,minimum+1)}
    return best,minimum


def ent(cells,total):
    return sum(float(w)*log(float(total/w)) for w in cells if w)


def actual_schedule(u,q,merge,m,demands,best,minimum,total):
    remaining=set(range(len(demands)));order=[];save=F(0);physical=F(0)
    actual=[];virtual=[];bonus=0.;firstsave=None
    budget=q;scale=BETA*BETA*u if merge else BETA*u
    while True:
        candidates=list(best[min(budget,minimum)])
        while candidates:
            def profit(edge):
                return sum(demands[i][1] for i in remaining
                           if edge in demands[i][0] or (edge+1)%m in demands[i][0])
            edge=max(candidates,key=lambda edge:(profit(edge),-edge))
            candidates.remove(edge)
            if not profit(edge):continue
            x=y=z=F(0);new=set()
            for i in remaining:
                arc,w=demands[i]
                left,right=edge in arc,(edge+1)%m in arc
                if left or right:new.add(i)
                if left and right:z+=w
                elif left:x+=w
                elif right:y+=w
            if x>y:x,y=y,x
            mass=x+y+z
            assert x+z<DELTA*total and y+z<DELTA*total
            tent=min(H/P*x,H*(x+z),H/P*z)
            both=x+y-z+tent>y
            credit=x+y-z+tent if both else y
            assert credit>=max(0,mass-DELTA*total,C*mass-D*DELTA*total)
            save+=credit;order.append(edge);rank=len(order)
            if both:
                physical+=(2*rank+2)*(x+y)+(2*rank+4)*z
                actual.extend((x,y,z));bonus+=ent((x,z),x+z) if x+z else 0.
            else:
                physical+=(2*rank+3)*mass-y;actual.extend((x+z,y))
            virtual.extend((x+z,y));remaining-=new
        if firstsave is None:firstsave=save
        if budget>=minimum:
            assert not remaining
            break
        budget=int(scale);scale*=BETA
    b=sum(w for arc,w in demands);zero=total-b
    actual.append(zero);virtual.append(zero)
    assert abs(ent(actual,total)-ent(virtual,total)-bonus)<1e-7
    ranks={edge:i+1 for i,edge in enumerate(order)}
    first=sum(w*min(ranks[edge] for edge in order
                    if edge in arc or (edge+1)%m in arc) for arc,w in demands)
    assert float(physical)-bonus/log(2)<=float(2*first+3*b-save)+1e-7
    return 2*first+2*zero*len(order)-save,save,firstsave,len(order)


def phase(u,q,merge,t):
    value=F(q+1,2);previous=q
    scale=BETA*BETA*u if merge else BETA*u
    while previous<t:
        current=int(scale);value+=F(previous+current,2)
        previous=current;scale*=BETA
    return value


def row_at(u):
    return next(options for left,right,options in ROWS if left<=u<right)


def schedule_checks():
    rng=Random(20261031);cases=transfers=regions=identities=0
    beta=float(BETA);lb=log(beta);lam=(beta+1)/(2*lb)
    chi=1.1285791015302313;B=7-log(6)/lb-chi
    for m in range(4,10):
        for _ in range(20):
            merged={}
            for _ in range(rng.randrange(2,20)):
                start,length=rng.randrange(m),rng.randrange(1,m//2+1)
                arc=frozenset((start+j)%m for j in range(length))
                merged[arc]=merged.get(arc,F(0))+rng.randrange(1,10)
            demands=list(merged.items());b=sum(w for arc,w in demands)
            cap=max(sum(w for arc,w in demands if vertex in arc) for vertex in range(m))
            total=max(F(b),F(cap)/DELTA+1);zero=total-b
            best,minimum=cover_oracle(m,demands)
            source=list(range(m));rng.shuffle(source);hit=set();masses=[]
            for edge in source:
                new=covered([edge],demands,m)-hit
                masses.append(sum(demands[i][1] for i in new));hit|=new
                if len(hit)==len(demands):break
            assert all(w<=2*DELTA*total for w in masses)
            breaks={point for left,right,options in ROWS for point in (left,right)}
            scale=F(1)
            while scale<=BETA*minimum:
                for integer in range(1,minimum+1):
                    point=F(integer)/scale
                    if 1<point<BETA:breaks.add(point)
                scale*=BETA
            breaks=sorted(breaks);averaged=0.;newlength=oldlength=0.
            for left,right in zip(breaks,breaks[1:]):
                u=(left+right)/2;k0,k1=int(u),int(BETA*u)
                probability=log(float(right/left))/lb
                oldbound=minimum
                scale=u
                while int(scale)<minimum:
                    oldbound+=int(scale);scale*=BETA
                oldlength+=probability*oldbound
                for v,q,merge,slope,intercept in row_at(u):
                    assert (q==k1) if merge else (q<=6 and q<k1)
                    objective,save,firstsave,length=actual_schedule(
                        u,q,merge,m,demands,best,minimum,total)
                    prefix=sum(masses[:q])
                    assert save>=firstsave>=slope*prefix-intercept*DELTA*total
                    transfers+=1
                    correction=(k0-k1+(k0+k1)*(len(masses)>k0)) if merge else (
                        k0-q+(k0+k1)*(len(masses)>k0)-(q+k1)*(len(masses)>q))
                    assert 2*(phase(u,k0,False,len(masses))-phase(u,q,merge,len(masses)))==correction
                    identities+=1
                    upper=sum(w*phase(u,q,merge,t) for t,w in enumerate(masses,1))
                    # Objective plus saving removes its mode discount.
                    assert objective+save-2*zero*length<=2*upper
                    waitingchange=-k0*(k0<minimum) if merge else (
                        q*(q<minimum)-k0*(k0<minimum))
                    assert length<=oldbound+waitingchange
                    averaged+=probability*float(v*objective)
                    newlength+=probability*float(v)*(oldbound+waitingchange)
                    regions+=1
            assert newlength<=oldlength+1e-8
            dplus=sum(float(w)*t for t,w in enumerate(masses))
            comparison=dplus+float(zero)*len(masses)
            assert averaged<=2*lam*comparison+(B-3)*float(b)+1e-7
            cases+=1
    print(cases,'actual modified-batch circles;',transfers,'exact credit transfers;',
          regions,'shift/variant schedules;',identities,'phase identities passed')


if __name__=='__main__':
    cloud_checks()
    quantitative_checks()
    schedule_checks()
