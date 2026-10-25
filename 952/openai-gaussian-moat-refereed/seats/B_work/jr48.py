# Component of the Gaussian-prime graph (step <= sqrt2) through 1+i; size and longest simple path (steps).
import sys
sys.setrecursionlimit(10000)
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
P={(a,b) for a in range(-R,R+1) for b in range(-R,R+1) if gprime(a,b)}
nb=[(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
start=(1,1); comp={start}; st=[start]
while st:
    a,b=st.pop()
    for da,db in nb:
        q=(a+da,b+db)
        if q in P and q not in comp: comp.add(q); st.append(q)
print('component size', len(comp), 'max |coord|', max(max(abs(a),abs(b)) for a,b in comp))
adj={v:[(v[0]+da,v[1]+db) for da,db in nb if (v[0]+da,v[1]+db) in comp] for v in comp}
best=[0,None]
import time; t0=time.time()
def dfs(v,seen,length,path):
    if length>best[0]: best[0]=length; best[1]=list(path)
    for w in adj[v]:
        if w not in seen:
            seen.add(w); path.append(w)
            dfs(w,seen,length+1,path)
            path.pop(); seen.discard(w)
for s in comp:
    dfs(s,{s},0,[s])
    if time.time()-t0>500: print('timeout'); break
print('longest simple path: steps', best[0], 'vertices', best[0]+1)
print(best[1])
