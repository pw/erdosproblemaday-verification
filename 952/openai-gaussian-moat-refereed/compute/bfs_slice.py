# Second instrument over the WHOLE scan population (not a spot check): every split-prime set with Q <= 4000 from primes < 400,
# R2 in {2,4}; bfs_check.py's algorithm (lift positions) re-implemented inline. Prints one line per set; INFINITE needs a witness shift.
import itertools, sys
from collections import deque
ps=[p for p in range(5,400) if p%4==1 and all(p%d for d in range(2,int(p**.5)+1))]
sets=[]
for r in (1,2,3,4):
    for c in itertools.combinations(ps,r):
        q=1
        for p in c: q*=p
        if q<=4000: sets.append((q,c))
sets.sort()
print("sets",len(sets),flush=True)
R2s=[int(sys.argv[1])]; QMIN=int(sys.argv[2]); K=int(sys.argv[3]); NS=int(sys.argv[4])
for R2 in R2s:
    fin=0
    for Q,P in [x for x in sets if x[0]>=QMIN][K::NS]:
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
        if res: print(R2,Q,P,"INFINITE",res,flush=True)
        else: print(R2,Q,P,"FINITE",flush=True); fin+=1
    print("R2",R2,"finite_count",fin,flush=True)
