import json,glob,math,random,sys
from sympy import isprime, n_order
D=sys.argv[1]
for f in sorted(glob.glob(D+"/pool_*.json"), key=lambda s:int(s.rsplit('_',1)[1].split('.')[0])):
    d=json.load(open(f)); N=d["N"]
    G=math.gcd(2**N-1,3**N-1)
    prod=1; bad=[]
    for r in d["pool"]:
        p=r["p"]
        if not isprime(p): bad.append(("notprime",p))
        e=math.lcm(n_order(2,p),n_order(3,p))
        if e!=r["e"]: bad.append(("e",p,e,r["e"]))
        if N%e: bad.append(("ediv",p,e))
        u,v=r["u"],r["v"]
        for _ in range(30):
            k=random.randrange(e*3); l=random.randrange(e*3)
            inL = (pow(2,k,p)*pow(3,l,p))%p==1
            if inL != ((u*k+v*l)%e==0): bad.append(("lat",p)); break
        if math.gcd(math.gcd(u,v),e)!=1: bad.append(("char-not-onto",p))
        vp=0; g=G
        while g%p==0: g//=p; vp+=1
        prod*=p**vp
    print(N, "cert", prod==G, "bad",bad[:3], len(d["pool"]))
