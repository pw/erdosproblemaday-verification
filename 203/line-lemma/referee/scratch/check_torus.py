import json
from math import gcd
from fractions import Fraction as F
D='/home/exedev/MathDyad/erdos203'
def lcm(a,b): return a*b//gcd(a,b)
pool=json.load(open(f'{D}/pool_5040.json'))['pool']
fails=0; n=0
for T in (8,9,15,20,24,36):
    for q in pool:
        p,e,u,v=q['p'],q['e'],q['u'],q['v']
        if e>360: continue
        R=lcm(T,e)
        img=set(); 
        # density of the coset C = {phi = target} inside each torus cell, target = 2^1*3^2
        target=pow(2,1,p)*pow(3,2,p)%p
        cnt={}
        for k in range(R):
            pk=pow(2,k,p)
            for l in range(R):
                x=pk*pow(3,l,p)%p
                if x==1: img.add((k%T,l%T))
                if x==target: cnt[(k%T,l%T)]=cnt.get((k%T,l%T),0)+1
        i=gcd(T,e)
        pred={(k,l) for k in range(T) for l in range(T) if (u*k+v*l)%i==0}
        per_cell=(R//T)**2
        dens={F(c,per_cell) for c in cnt.values()}
        predcells={(k,l) for k in range(T) for l in range(T) if (u*(k-1)+v*(l-2))%i==0}
        ok = img==pred and dens=={F(i,e)} and set(cnt)==predcells
        n+=1
        if not ok: fails+=1; print('FAIL',T,p,e,len(img),len(pred),dens)
print('torus lattice-image + intensity checks:',n,'failures',fails)
