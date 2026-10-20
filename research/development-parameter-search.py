"""Exploration only: vary proof parameters; no floating result is a theorem."""
import math
import runpy

prior=runpy.run_path('next-expected-check.py')
rows=prior['table'](prior['F'](3512863,10**6))
mixes=[[float(o[0]) for o in options] for _,_,options in rows]

def entropy(p):
    return -p*math.log(p)-(1-p)*math.log1p(-p)

def coefficients(beta,p):
    lb=math.log(beta)
    c,d=(2-p)/(1-p),2/(1-p)
    bounds=[1,4/beta,5/beta,2,8/beta,3,11/beta,12/beta,beta]
    opts=[[(3,True,c,3*d)],[(4,True,1,4),(4,True,0,0)],
          [(1,False,c,d)],[(1,False,c,d),(2,False,c,2*d)],
          [(2,False,c,2*d)],[(2,False,c,2*d),(3,False,c,3*d)],
          [(3,False,c,3*d)],[(3,False,c,3*d),(5,False,1,5),(6,False,0,0)]]
    a=[0.]
    for t in range(2,8):
        n=int(beta*t)
        integ=(t+n)*math.log(t)-math.lgamma(t+1)+(n-3)*lb-math.lgamma(n+1)+math.log(6)
        a.append(((beta+1)*(t-1)-integ)/lb)
    mu=0.; zero=[0.]*7
    for j,(left,right) in enumerate(zip(bounds,bounds[1:])):
        prob=math.log(right/left)/lb
        k0,k1=int((left+right)/2),int(beta*(left+right)/2)
        for v,(q,merge,cq,dq) in zip(mixes[j],opts[j]):
            mu+=prob*v*dq
            for t in range(1,8):
                change=k0-q+(k0+k1)*(t>k0)
                if not merge:change-=(q+k1)*(t>q)
                a[t-1]+=prob*v*(change+cq*(t<=q))
            for k in range(1,8):
                z=-k0*(k0<k) if merge else q*(q<k)-k0*(k0<k)
                zero[k-1]+=prob*v*z
    return a,mu,zero

def evaluate(beta,delta,p):
    # Restrict to the exact existing entropy-tent proof: H2(p)>=1-2p.
    if entropy(p)/math.log(2)<1-2*p:return 1000.
    lb=math.log(beta)
    if beta-1<2*lb:return 1000.
    a,mu,zero=coefficients(beta,p)
    tau=min(a[1:])
    chi=tau-2*delta*(tau-a[0])-delta*mu
    if max(zero)>1e-12 or chi+2/lb<tau:return 1000.
    B=7-math.log(6)/lb-chi
    residual=1-6*delta
    sigma=-6*delta*math.log(delta)-residual*math.log(residual)
    return (beta+1)/lb+max(math.log(2)/entropy(delta),B*math.log(2)/sigma)

def best_delta(beta,p):
    lo,hi=.15,.16
    for _ in range(65):
        m1=(2*lo+hi)/3;m2=(lo+2*hi)/3
        if evaluate(beta,m1,p)<evaluate(beta,m2,p):hi=m2
        else:lo=m1
    delta=(lo+hi)/2
    return evaluate(beta,delta,p),delta

if __name__=='__main__':
    best=(1000,None)
    for p in [.170536+i*.0001 for i in range(150)]:
        for beta in [3.512863+i*.0005 for i in range(100)]:
            value,delta=best_delta(beta,p)
            if value<best[0]:best=(value,(beta,delta,p))
    print('Fixed-mixture search:',best,flush=True)
    for beta in [3.512863,3.515,3.52,3.53,3.54]:
        print(beta,best_delta(beta,.170536),flush=True)
