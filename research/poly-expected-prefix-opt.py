"""Exploratory optimizer for a shift-dependent first/second prefix minorant."""
import math
import runpy
base=runpy.run_path('poly-expected-opt.py')
e=base['discount']
golden=base['golden']


def profiles(beta):
    lb=math.log(beta)
    breaks={1.,beta}
    for k in range(1,math.ceil(beta)+1):
        if 1<k<beta: breaks.add(float(k))
    for k in range(1,math.ceil(beta*beta)+1):
        x=k/beta
        if 1<x<beta:breaks.add(x)
    breaks=sorted(breaks)
    regions=[]
    for l,r in zip(breaks,breaks[1:]):
        u=(l+r)/2
        k0,k1=int(u),int(beta*u)
        regions.append((l,r,math.log(r/l)/lb,k0,k1))
    coeff=[e(beta,t) for t in range(1,31)]
    result=[]
    for mask in range(1<<len(regions)):
        a=coeff.copy()
        mu=0
        for j,(_,_,p,k0,k1) in enumerate(regions):
            use1=(mask>>j)&1
            rank=k1 if use1 else k0
            mu+=p*(k0+k1 if use1 else k0)
            for t in range(rank): a[t]+=p
        order=sorted(range(len(a)),key=lambda t:a[t])
        smallest=[a[t] for t in order[:8]]
        result.append((smallest,mu,mask,[t+1 for t in order[:8]]))
    return regions,result


def best_score(beta,delta,records):
    lb=math.log(beta)
    A=2*max((beta+1)/(2*lb),1+1/lb)
    C=7-math.log(6)/lb
    N=int(1/(2*delta))
    rem=1-2*delta*N
    candidates=[]
    for values,mu,mask,order in records:
        chi=2*delta*sum(values[:N])+rem*values[N]-delta*mu
        if values[N]>chi+2/lb+1e-9: continue
        candidates.append((chi,mask,order,mu,values))
    chi,mask,order,mu,values=max(candidates)
    B=C-chi
    k=int(1/delta)
    r=1-k*delta
    sigma=-k*delta*math.log(delta)-(r*math.log(r) if r else 0)
    h=-delta*math.log(delta)-(1-delta)*math.log1p(-delta)
    R=A+max(math.log(2)/h,B*math.log(2)/sigma)
    return R,chi,mask,order,mu,values,B


def mixed_record(beta, regions, alphas):
    a=[e(beta,t) for t in range(1,31)]
    mu=0
    for (_,_,p,k0,k1),alpha in zip(regions,alphas):
        mu+=p*(k0+alpha*k1)
        for t in range(k0):a[t]+=p
        for t in range(k0,k1):a[t]+=p*alpha
    order=sorted(range(len(a)),key=lambda t:a[t])
    return [([a[t] for t in order[:8]],mu,0,[t+1 for t in order[:8]])]


def mixed_opt(beta, delta, regions, alphas):
    for rounds in range(20):
        old=alphas.copy()
        for j in range(len(regions)):
            def objective(alpha):
                trial=alphas.copy()
                trial[j]=alpha
                return -best_score(beta,delta,mixed_record(beta,regions,trial))[1]
            alpha=golden(objective,0,1,50)
            alphas[j]=min([0.,alpha,1.],key=objective)
        if max(abs(a-b) for a,b in zip(old,alphas))<1e-10:break
    return alphas


if __name__=='__main__':
    beta=3512863/1e6
    regions,records=profiles(beta)
    delta=golden(lambda d:best_score(beta,d,records)[0],.13,.165)
    result=best_score(beta,delta,records)
    print('beta delta',beta,delta,'result',result)
    mask=result[2]
    print('regions',[(l,r,k0,k1,(mask>>j)&1) for j,(l,r,p,k0,k1) in enumerate(regions)])
    alphas=[float((mask>>j)&1) for j in range(len(regions))]
    for _ in range(10):
        alphas=mixed_opt(beta,delta,regions,alphas)
        record=mixed_record(beta,regions,alphas)
        delta=golden(lambda d:best_score(beta,d,record)[0],.13,.165)
    print('MIX delta',delta,'alphas',alphas,'result',best_score(beta,delta,record))
