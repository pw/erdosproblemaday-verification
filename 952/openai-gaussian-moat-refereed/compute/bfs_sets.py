# Same BFS as bfs_all.py, on an explicit list of sets (the five R2=2 sets the 4 GB-capped slices could not finish).
import sys
from collections import deque
R2=int(sys.argv[1]); P=tuple(int(a) for a in sys.argv[2:])
Q=1
for p in P: Q*=p
roots={p: next(r for r in range(1,p) if (r*r+1)%p==0) for p in P}
inA=lambda x,y: all((x+y*roots[p])%p and (x-y*roots[p])%p for p in P)
R=int(R2**0.5)+1
steps=[(a,b) for a in range(-R,R+1) for b in range(-R,R+1) if 0<a*a+b*b<=R2]
pos={}; res=None
for x0 in range(Q):
    for y0 in range(Q):
        if res or not inA(x0,y0) or (x0,y0) in pos: continue
        pos[(x0,y0)]=(x0,y0); dq=deque([(x0,y0)])
        while dq and not res:
            c=dq.popleft(); X,Y=pos[c]
            for a,b in steps:
                nx,ny=X+a,Y+b; w=(nx%Q,ny%Q)
                if not inA(*w): continue
                if w in pos:
                    if pos[w]!=(nx,ny): res=(nx-pos[w][0],ny-pos[w][1]); break
                else: pos[w]=(nx,ny); dq.append(w)
    if res: break
print(R2,Q,P,"INFINITE" if res else "FINITE",res if res else "",flush=True)
