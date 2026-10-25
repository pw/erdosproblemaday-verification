#!/usr/bin/env python3
# Independent second instrument for sieve_perc.c: BFS on the torus assigning lift positions; a node reached at two different
# lift positions => infinite component. Small Q only. usage: bfs_check.py R2 p1 p2 ...
import sys
from collections import deque
R2=int(sys.argv[1]); P=[int(a) for a in sys.argv[2:]]
Q=1
for p in P: Q*=p
roots={p: next(r for r in range(1,p) if (r*r+1)%p==0) for p in P}
def inA(x,y): return all((x+y*roots[p])%p and (x-y*roots[p])%p for p in P)
R=int(R2**0.5)+1
steps=[(a,b) for a in range(-R,R+1) for b in range(-R,R+1) if 0<a*a+b*b<=R2]
pos={}; big=0; cnt=0
for x0 in range(Q):
    for y0 in range(Q):
        if not inA(x0,y0) or (x0,y0) in pos: continue
        pos[(x0,y0)]=(x0,y0); dq=deque([(x0,y0)]); size=1
        while dq:
            c=dq.popleft(); X,Y=pos[c]
            for a,b in steps:
                nx,ny=X+a,Y+b; w=(nx%Q,ny%Q)
                if not inA(*w): continue
                if w in pos:
                    if pos[w]!=(nx,ny): print(f"R2={R2} P={P} Q={Q} INFINITE shift={(nx-pos[w][0],ny-pos[w][1])}"); sys.exit(0)
                else: pos[w]=(nx,ny); dq.append(w); size+=1
        big=max(big,size)
print(f"R2={R2} P={P} Q={Q} FINITE max_component={big}")
