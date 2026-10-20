"""Exploratory schedules q,r,k2,...; no numerical output is a theorem."""
import math,runpy,json,subprocess,time
base=runpy.run_path('further-expected-check.py')
discount=base['discount']

def explore(beta,delta):
    bs={1.,beta}
    for power in range(2):
        bp=beta**power
        for k in range(1,int(beta*bp)+1):
            u=k/bp
            if 1<u<beta:bs.add(u)
    bs=sorted(bs)
    regs=[]
    for l,r in zip(bs,bs[1:]):
        u=(l+r)/2
        regs.append((l,r,math.log(r/l)/math.log(beta),int(u),int(beta*u),int(beta*beta*u)))
    nt=16;c=228683/103683;d=250000/103683
    choices=[]
    for j,(l,rr,p,k0,k1,k2) in enumerate(regs):
        pieces={l,rr}
        for v in range(int(beta*beta*l),int(beta*beta*rr)+2):
            cut=v/(beta*beta)
            if l<cut<rr:pieces.add(cut)
        pieces=sorted(pieces)
        k2mean=sum(int(beta*beta*(ll+hh)/2)*math.log(hh/ll) for ll,hh in zip(pieces,pieces[1:]))/math.log(rr/l)
        for q in range(1,7):
            rs=sorted({0,k1-1,k1,k1+1})
            for r in rs:
                if r and not q<r<k2:continue
                if r:
                    changes=[k0-q+(k0+k1)*(t>k0)-(q+r)*(t>q)+(k1+k2mean)*(t>k1)-(r+k2mean)*(t>r) for t in range(1,nt+1)]
                    opts=[(0,0,0),(q,1,q),(q,c,d*q),(r,1,q+r),(r,c,d*(q+r)),(q,c-1,d*q+r)]
                else:
                    changes=[k0-q+(k0+k1)*(t>k0)+(k1+k2mean)*(t>k1)-(q+k2mean)*(t>q) for t in range(1,nt+1)]
                    opts=[(0,0,0),(q,1,q),(q,c,d*q)]
                for cutoff,slope,intercept in opts:
                    corr=changes.copy()
                    if slope==c-1:corr=[v+(t<=r) for t,v in enumerate(corr,1)]
                    choices.append((j,p,q,r,k0,k1,k2,cutoff,slope,intercept,corr))
    nw=len(choices);nv=nw+nt+1;tc=nw+nt
    A=[];rhs=[]
    for j in range(len(regs)):
        row=[0.]*nv
        for z,o in enumerate(choices):
            if o[0]==j:row[z]=1.
        A.append(row);rhs.append(1.)
    lb=math.log(beta);lead=2*max((beta+1)/(2*lb),1+1/lb);gap=lead-(beta+1)/lb
    for t in range(1,nt+1):
        row=[0.]*nv
        for z,(_,p,q,r,k0,k1,k2,cut,s,inter,corr) in enumerate(choices):row[z]=-p*(corr[t-1]+s*(t<=cut))
        row[nw+t-1]=-1;row[tc]=1
        A.append(row);rhs.append(discount(beta,t)+gap*(t-1)+20)
    for k in range(1,15):
        row=[0.]*nv
        for z,(_,p,q,r,k0,k1,k2,cut,s,inter,corr) in enumerate(choices):
            dz=q*(q<k)+r*(r<k)-k0*(k0<k)-k1*(k1<k)
            row[z]=p*(delta*inter+2*dz)
        for t in range(nt):row[nw+t]=2*delta
        A.append(row);rhs.append(2/lb+(lead-2*(1+1/lb))*k)
    objective=[0.]*nv
    for z,(_,p,q,r,k0,k1,k2,cut,s,inter,corr) in enumerate(choices):objective[z]=-delta*p*inter
    for t in range(nt):objective[nw+t]=-2*delta
    objective[tc]=1
    Path=__import__('pathlib').Path
    Path('expected-two-phase-lp.json').write_text(json.dumps({'A':A,'b':rhs,'c':objective}),encoding='utf8')
    node=r'C:/Users/micha/AppData/Local/OpenAI/Codex/runtimes/cua_node/cfb32733c877621e/bin/node.exe'
    result=subprocess.run([node,'expected-fast-simplex.js','expected-two-phase-lp.json'],capture_output=True,text=True,check=True)
    lp=json.loads(result.stdout)
    chi=lp['value']-20
    B=7-math.log(6)/lb-chi
    rem=1-int(1/delta)*delta;sig=-int(1/delta)*delta*math.log(delta)-rem*math.log(rem)
    h=-delta*math.log(delta)-(1-delta)*math.log1p(-delta)
    ratio=lead+max(math.log(2)/h,B*math.log(2)/sig)
    selected=[(o,x) for o,x in zip(choices,lp['solution'][:nw]) if x>1e-7]
    print('beta delta regions options R chi T',beta,delta,len(regs),nw,ratio,chi,lp['solution'][tc]-20,flush=True)
    print('SELECTED',selected,flush=True)
    Path('expected-two-phase-compact-result.json').write_text(json.dumps({'beta':beta,'delta':delta,'ratio':ratio,'chi':chi,'T':lp['solution'][tc]-20,'choices':selected,'regions':regs}),encoding='utf8')
    return ratio

if __name__=='__main__':
    import sys
    explore(3512863/1e6,float(sys.argv[1]) if len(sys.argv)>1 else .155223384)
