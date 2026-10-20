"""Explore alternative first exact-coverage budgets, with joint zero waiting."""
import math
import runpy

base = runpy.run_path('further-expected-check.py')
simplex = base['simplex_max']
discount = base['discount']
golden = base['golden']


def optimize(beta, delta, qmax=6, nt=30):
    regs = base['regions'](beta)
    c, d = 228683/103683, 250000/103683
    choices = []
    for j, (left, right, prob, opts) in enumerate(regs):
        u = (left+right)/2
        k0, k1 = int(u), int(beta*u)
        for q in list(range(1, min(qmax, k1-1)+1))+[k1]:
            creditopts=[(0,0,0),(q,1,q),(q,c,d*q)]
            if q<k1:creditopts += [(k1,1,q+k1),(k1,c,d*(q+k1))]
            if q<k1:creditopts += [(q,c-1,d*q+k1)]
            for cutoff, slope, intercept in creditopts:
                if q==k1:
                    changes=[(k0-k1)+(k0+k1)*(t>k0) for t in range(1,nt+1)]
                else:
                    changes = [(k0-q)+(k0+k1)*(t>k0)-(q+k1)*(t>q)
                               for t in range(1,nt+1)]
                if slope==c-1:
                    changes=[value+(t<=k1) for t,value in enumerate(changes,1)]
                choices.append((j,prob,q,k0,k1,cutoff,slope,intercept,changes))
    nw = len(choices)
    nv = nw+nt+1
    tc = nw+nt
    A, rhs = [], []
    for j in range(len(regs)):
        row = [0.]*nv
        for z, option in enumerate(choices):
            if option[0]==j: row[z]=1.
        A.append(row); rhs.append(1.)
    lb=math.log(beta)
    lead=2*max((beta+1)/(2*lb),1+1/lb)
    gap=lead-(beta+1)/lb
    for t in range(1,nt+1):
        row = [0.]*nv
        for z, (_,p,q,k0,k1,cut,c,dL,changes) in enumerate(choices):
            row[z]=-p*(changes[t-1]+c*(t<=cut))
        row[nw+t-1]=-1.
        row[tc]=1.
        A.append(row);rhs.append(discount(beta,t)+gap*(t-1)+20)
    for k in range(1,qmax+2):
        row=[0.]*nv
        for z, (_,p,q,k0,k1,cut,c,dL,changes) in enumerate(choices):
            dz=(-k0*(k0<k)) if q==k1 else q*(q<k)-k0*(k0<k)
            row[z]=p*(delta*dL+2*dz)
        for t in range(nt):row[nw+t]=2*delta
        A.append(row);rhs.append(2/lb+(lead-2*(1+1/lb))*k)
    objective=[0.]*nv
    for z, (_,p,q,k0,k1,cut,c,dL,changes) in enumerate(choices):objective[z]=-delta*p*dL
    for t in range(nt):objective[nw+t]=-2*delta
    objective[tc]=1.
    value, solution=simplex(A,rhs,objective)
    chi=value-20
    B=4+int(beta)-math.lgamma(int(beta)+1)/lb-chi
    rem=1-int(1/delta)*delta
    sig=-int(1/delta)*delta*math.log(delta)-rem*math.log(rem)
    h=-delta*math.log(delta)-(1-delta)*math.log1p(-delta)
    ratio=lead+max(math.log(2)/h,B*math.log(2)/sig)
    chosen=[]
    for z, option in enumerate(choices):
        if solution[z]>1e-7:chosen.append((option,solution[z]))
    return ratio,chi,solution[tc]-20,chosen


if __name__=='__main__':
    import sys
    if '--grid' in sys.argv:
        for i in range(25):
            beta=3.+i*.05
            delta=golden(lambda d:optimize(beta,d)[0],.13,.18,22)
            print('grid',beta,delta,optimize(beta,delta)[:3],flush=True)
        sys.exit()
    beta=3512863/1e6
    delta=golden(lambda d:optimize(beta,d)[0],.12,.17,32)
    print('beta delta',beta,delta)
    result=optimize(beta,delta)
    print('R chi T',result[:3])
    for row in result[3]:print(row)
