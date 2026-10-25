# The self-contained upper-bound route: for ANY 5-element A, in any block of 2M
# consecutive integers, each a in A has consecutive multiples l_a, r_a bracketing
# the midpoint gamma; claim: these 5 edges admit a system of distinct representatives
# (Hall), giving 5 distinct integers, one multiple of each a.
import random, itertools
def bracket(a, gamma_num, gamma_den=2):
    # gamma = t + M + 1/2 ; use exact rational via doubling
    # l_a = a*floor(gamma/a)
    import math
    g = gamma_num/gamma_den
    l = a*math.floor(g/a)
    return l, l+a

def test(A, t):
    M=max(A); I=(t+1, t+2*M)
    gamma2 = 2*t+2*M+1   # 2*gamma
    edges=[]
    for a in A:
        l = a*((gamma2//2)//a)
        r = l+a
        if not (I[0]<=l<=I[1] and I[0]<=r<=I[1]): return ('endpoint_outside',a,l,r,I)
        edges.append((l,r))
    # Hall condition / SDR via brute force over choices
    for pick in itertools.product(*[(e[0],e[1]) for e in edges]):
        if len(set(pick))==len(A):
            # verify divisibility
            ok=all(any(p%a==0 for p in [pick[i]] ) for i,a in enumerate(A))
            ok=all(pick[i]%A[i]==0 for i in range(len(A)))
            if ok: return ('SDR_OK', pick)
    return ('NO_SDR', A, t, edges)

random.seed(11)
fails=[]
trials=0
for _ in range(60000):
    n=5
    A=sorted(random.sample(range(2,60), n))
    t=random.randrange(0,10**6)
    r=test(A,t)
    trials+=1
    if r[0]!='SDR_OK': fails.append(r)
print("5-element random trials:",trials," failures:",len(fails))
for f in fails[:5]: print("  FAIL:",f)

# does it break at 6, as claimed ("stops genuinely at six: K_{2,3} has six edges on five vertices")
fails6=[]
for _ in range(60000):
    A=sorted(random.sample(range(2,60), 6))
    t=random.randrange(0,10**6)
    r=test(A,t)
    if r[0]!='SDR_OK': fails6.append(r)
print("6-element random trials: 60000  failures:",len(fails6))
for f in fails6[:3]: print("  FAIL(6):",f[0], f[1] if len(f)>1 else '')
