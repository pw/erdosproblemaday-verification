# Lower-bound search: long simple paths (self-avoiding walks on distinct Gaussian primes, step <= sqrt2)
# inside the component of 1+i. Randomised DFS with a node budget per restart; prints best found.
import random, sys, time
R=60
def isprime(n):
    if n<2: return False
    i=2
    while i*i<=n:
        if n%i==0: return False
        i+=1
    return True
def gprime(a,b):
    if a==0: return abs(b)%4==3 and isprime(abs(b))
    if b==0: return abs(a)%4==3 and isprime(abs(a))
    return isprime(a*a+b*b)
P={(a,b) for a in range(0,R+1) for b in range(0,R+1) if gprime(a,b)}
nb=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
start=(1,1); comp={start}; st=[start]
while st:
    a,b=st.pop()
    for da,db in nb:
        q=(a+da,b+db)
        if q in P and q not in comp: comp.add(q); st.append(q)
adj={v:[(v[0]+da,v[1]+db) for da,db in nb if (v[0]+da,v[1]+db) in comp] for v in comp}
E=sum(len(x) for x in adj.values())//2
print('component', len(comp), 'edges', E, 'contains 1+i', (1,1) in comp, 'max norm', max(a*a+b*b for a,b in comp), flush=True)
# sanity: every vertex is a Gaussian prime, every pair distinct, steps <= sqrt2
best=[]
random.seed(1)
t0=time.time()
V=list(comp)
while time.time()-t0<60:
    s=random.choice(V); path=[s]; seen={s}; budget=[20000]
    def dfs(v):
        global best
        if len(path)>len(best): best=list(path)
        budget[0]-=1
        if budget[0]<=0: return
        nbrs=adj[v][:]; random.shuffle(nbrs)
        nbrs.sort(key=lambda w: sum(1 for x in adj[w] if x not in seen))  # Warnsdorff-ish
        for w in nbrs:
            if w not in seen:
                seen.add(w); path.append(w); dfs(w); path.pop(); seen.discard(w)
                if budget[0]<=0: return
    sys.setrecursionlimit(5000); dfs(s)
steps=len(best)-1
ok=all(best[i]!=best[j] for i in range(len(best)) for j in range(i)) and all(max(abs(best[i+1][0]-best[i][0]),abs(best[i+1][1]-best[i][1]))<=1 for i in range(steps)) and all(p in P for p in best)
print('best simple path found: steps', steps, 'vertices', len(best), 'verified', ok, flush=True)
print(best)
