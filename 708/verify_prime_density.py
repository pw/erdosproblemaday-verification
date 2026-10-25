# The lower bound c_5 >= 2 needs: for every c<2 there are primes u<v<w with a prime
# q in (uv, vw) and ratio (2uv-1)/(vw) = 2u/w - 1/(vw) > c.
# Check the existence side empirically at ratios approaching 2.
import sympy
best=[]
targets=[1.9,1.99,1.999,1.9999,1.99999]
ti=0
p=sympy.nextprime(1000)
seen=set()
X=1000
while ti<len(targets) and X<10**9:
    # take three consecutive primes near X
    u=sympy.nextprime(X); v=sympy.nextprime(u); w=sympy.nextprime(v)
    ratio=2*u/w - 1/(v*w)
    if ratio>targets[ti]:
        q=sympy.nextprime(u*v)
        okq = q < v*w
        # also verify the uniqueness inequalities used in the general proof
        i1 = v*(v-1-u)+1 > 0           # x-v+v^2 outside I  (needs v>=u+2)
        i2 = u < 1+v+1/v               # x-v-v^2 outside I
        i3 = 2*u*v-1 < v**3            # no room for a second v^3 window
        print(f"target>{targets[ti]}: u,v,w=({u},{v},{w})  ratio={ratio:.8f}  "
              f"q={q} in (uv,vw)={okq}  (uv={u*v}, vw={v*w})  uniq-ineqs={i1 and i2 and i3}")
        ti+=1
    X=int(X*1.6)+7
