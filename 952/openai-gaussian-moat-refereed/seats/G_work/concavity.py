# Exact check that f_Z(s) = E_S H(F_S(Z)) (uniform s-subset of batch, fair independent signs)
# is concave in s with f(0)=0, f(s)<=s*L_*, for random and structured finitely supported Z.
import math, random, itertools
from fractions import Fraction
random.seed(7)
def two_squares(p):
    for a in range(1,int(p**0.5)+1):
        b2=p-a*a; b=int(round(b2**0.5))
        if b*b==b2 and b>0: return a,b
def res_map(p,a,b,sign):
    # pi = a + s*b*i ; i == -a/(s b) mod pi
    inv=pow(sign*b % p, -1, p)
    iv=(-a*inv)%p
    return lambda x,y: (x+y*iv)%p
def H(counts,total):
    return -sum(c/total*math.log(c/total) for c in counts.values() if c)
def f_values(Z, primes):
    # Z: dict point->weight (ints)
    k=len(primes); tot=sum(Z.values())
    maps={}
    for p in primes:
        a,b=two_squares(p)
        maps[p]=[res_map(p,a,b,1),res_map(p,a,b,-1)]
    fs=[]
    for s in range(k+1):
        acc=0.0; n=0
        for sub in itertools.combinations(primes,s):
            for signs in itertools.product([0,1],repeat=s):
                cnt={}
                for (x,y),w in Z.items():
                    key=tuple(maps[p][sg](x,y) for p,sg in zip(sub,signs))
                    cnt[key]=cnt.get(key,0)+w
                acc+=H(cnt,tot); n+=1
        fs.append(acc/n)
    return fs
batches=[[5,13,17,29,37,41],[101,109,113,137,149,157],[13,17,29]]
worst=1e9; viol=0; checks=0
for primes in batches:
    L=sum(math.log(p) for p in primes)/len(primes)
    for trial in range(40):
        kind=trial%4
        if kind==0:   # random support, random weights
            Z={(random.randint(-60,60),random.randint(-60,60)):random.randint(1,9) for _ in range(random.randint(2,60))}
        elif kind==1: # points along a line (structured)
            st=(random.randint(1,4),random.randint(0,4))
            Z={(i*st[0],i*st[1]):1 for i in range(random.randint(2,80))}
        elif kind==2: # a few multiples of one Gaussian factor plus noise
            p=random.choice(primes); a,b=two_squares(p)
            Z={((a*u-b*v),(b*u+a*v)):random.randint(1,5) for u in range(-3,4) for v in range(-3,4)}
        else:         # a walk segment
            x=y=0; Z={(0,0):1}
            for _ in range(random.randint(5,120)):
                dx,dy=random.choice([(1,0),(-1,0),(0,1),(0,-1)]); x+=dx; y+=dy; Z[(x,y)]=Z.get((x,y),0)+1
        fs=f_values(Z,primes)
        assert abs(fs[0])<1e-12
        for s in range(len(fs)):
            assert fs[s]<=s*L+1e-9
        for s in range(1,len(fs)-1):
            d1=fs[s]-fs[s-1]; d2=fs[s+1]-fs[s]
            checks+=1
            worst=min(worst,d1-d2)
            if d2>d1+1e-9: viol+=1
print(f"concavity checks={checks}, violations={viol}, min (Delta_s - Delta_(s+1)) = {worst:.3e}")
