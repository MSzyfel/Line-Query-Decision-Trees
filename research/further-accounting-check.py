"""Exact finite checks for the optional second-positive-query primitive."""
from fractions import Fraction
from random import Random
import runpy


def local_checks():
    rng=Random(20261021)
    checked=0
    for _ in range(10000):
        cap=rng.randrange(1,100)
        shared=rng.randrange(cap+1)
        x,y=[rng.randrange(cap-shared+1) for _ in range(2)]
        mass=x+y+shared
        discount=max(x,y,x+y-shared)
        stop=5*mass-max(x,y)
        both=4*(x+y)+6*shared
        assert min(stop,both)==5*mass-discount
        assert (both<stop)==(min(x,y)>shared)
        assert discount>=max(0,mass-cap,3*mass-4*cap)
        rank=rng.randrange(1,30)
        if both<stop:
            actual=(2*rank+2)*(x+y)+(2*rank+4)*shared
        else:
            actual=(2*rank+3)*mass-max(x,y)
        assert actual==(2*rank+3)*mass-discount
        checked+=1
    # The piecewise guarantee is exact: symmetrize the exclusives and use
    # the largest feasible shared mass for each fixed total mass.
    for numerator in range(201):
        mass=Fraction(numerator,100)
        shared=min(mass,2-mass)
        x=y=(mass-shared)/2
        assert x+shared<=1 and y+shared<=1
        discount=max(x,y,x+y-shared)
        assert discount==max(0,mass-1,3*mass-4)
    print(f'{checked} local mode/cap-bound checks and 201 exact tight profiles passed.')


def prefix_checks():
    rng=Random(20261022)
    checked=0
    for _ in range(2000):
        vcount=rng.randrange(3,20)
        demands=[]
        for _ in range(rng.randrange(1,30)):
            start,length=rng.randrange(vcount),rng.randrange(1,vcount)
            arc={(start+j)%vcount for j in range(length)}
            demands.append((arc,rng.randrange(1,20)))
        cap=max(sum(weight for arc,weight in demands if v in arc)
                for v in range(vcount))
        remaining=set(range(len(demands)))
        order=list(range(vcount))
        rng.shuffle(order)
        discount=covered=0
        for rank,v in enumerate(order,1):
            w=(v+1)%vcount
            x=y=z=0
            for j in remaining:
                arc,weight=demands[j]
                if v in arc and w in arc:
                    z+=weight
                elif v in arc:
                    x+=weight
                elif w in arc:
                    y+=weight
            discount+=max(x,y,x+y-z)
            covered+=x+y+z
            assert discount>=max(0,covered-rank*cap,3*covered-4*rank*cap)
            remaining={j for j in remaining if v not in demands[j][0] and w not in demands[j][0]}
            checked+=1
    print(f'{checked} exact circular-prefix discount checks passed.')


def entropy_tent_checks():
    helpers=runpy.run_path('poly-expected-check.py')
    Bound, log, LOG2=helpers['Bound'],helpers['log'],helpers['LOG2']
    anchor=Fraction(8527,50000)
    height=Fraction(329469,500000)
    entropy=(-anchor*log(anchor)-(1-anchor)*log(1-anchor))/LOG2
    assert entropy.lo>height
    assert height+2*anchor>1
    K=height/anchor
    a=(2*K+3)/(K+1)
    b=2*(K+2)/(K+1)
    assert a==Fraction(914748,414739) and b==Fraction(1000018,414739)
    rng=Random(20261023)
    for _ in range(10000):
        cap=rng.randrange(1,100)
        z=rng.randrange(cap+1)
        x,y=sorted(rng.randrange(cap-z+1) for _ in range(2))
        mass=x+y+z
        tent=min(K*x,K*z,height*(x+z))
        discount=max(Fraction(y),x+y-z+tent)
        better_tent=min(K*y,K*z,height*(y+z))
        better_discount=max(Fraction(y),x+y-z+better_tent)
        assert better_discount>=discount
        assert discount>=max(0,mass-cap,a*mass-b*cap)
    print('Exact entropy anchor certificate passed:', float(entropy.lo), '>', float(height))
    print('Rational affine entropy discount:', a, b)
    print('10,000 exact rational entropy-mode/cap-minorant checks passed.')


if __name__=='__main__':
    local_checks()
    prefix_checks()
    entropy_tent_checks()
