# Brute-force check of Lemma 4.1 (Many differences) on random and structured
# self-avoiding lattice walks, D = 1, sqrt2, 2.
import random, math, itertools, sys
random.seed(12345)

def steps_for(D):
    S=[]
    m=int(math.floor(D))
    for x in range(-m,m+1):
        for y in range(-m,m+1):
            if (x,y)!=(0,0) and x*x+y*y<=D*D+1e-9:
                S.append((x,y))
    return S

def random_saw(n, steps, bias=None):
    # grow until n steps; restart if stuck
    while True:
        pts=[(0,0)]; seen={(0,0)}
        ok=True
        for _ in range(n):
            x,y=pts[-1]
            cand=[(x+a,y+b) for a,b in steps if (x+a,y+b) not in seen]
            if not cand: ok=False; break
            if bias is not None and random.random()<bias:
                # persist in previous direction if possible (makes long straight-ish walks)
                if len(pts)>=2:
                    dx=pts[-1][0]-pts[-2][0]; dy=pts[-1][1]-pts[-2][1]
                    c=(x+dx,y+dy)
                    if c in cand:
                        nxt=c
                    else: nxt=random.choice(cand)
                else: nxt=random.choice(cand)
            else:
                nxt=random.choice(cand)
            pts.append(nxt); seen.add(nxt)
        if ok: return pts

def spiral(n, D):
    # square spiral on lattice with step 1 (valid for any D>=1)
    pts=[(0,0)]; x=y=0; dirs=[(1,0),(0,1),(-1,0),(0,-1)]; L=1; d=0
    while len(pts)<n+1:
        for _ in range(2):
            for _ in range(L):
                x+=dirs[d][0]; y+=dirs[d][1]; pts.append((x,y))
                if len(pts)==n+1: return pts
            d=(d+1)%4
        L+=1
    return pts

def serpentine(n, width, step=1):
    pts=[]; x=0; y=0; dx=1
    pts.append((0,0))
    while len(pts)<n+1:
        nx=x+dx*step
        if 0<=nx<=width*step:
            x=nx
        else:
            y+=step; dx=-dx
        pts.append((x,y))
    return pts

def line(n, step):
    return [(i*step[0], i*step[1]) for i in range(n+1)]

def analyse(pts, D):
    n=len(pts)-1
    assert len(set(pts))==n+1
    for i in range(n):
        dx=pts[i+1][0]-pts[i][0]; dy=pts[i+1][1]-pts[i][1]
        assert dx*dx+dy*dy<=D*D+1e-9
    # diameter
    best=-1; P0=P1=None
    for i in range(len(pts)):
        xi,yi=pts[i]
        for j in range(i+1,len(pts)):
            d2=(xi-pts[j][0])**2+(yi-pts[j][1])**2
            if d2>best: best=d2; P0=pts[i]; P1=pts[j]
    R=math.sqrt(best)
    ax=(P1[0]-P0[0])/R; ay=(P1[1]-P0[1])/R
    # projections lie in [0,R]
    maxd=0.0
    for (x,y) in pts:
        t=(x-P0[0])*ax+(y-P0[1])*ay
        assert -1e-9<=t<=R+1e-9, "projection claim fails"
        dist=abs(-(x-P0[0])*ay+(y-P0[1])*ax)
        maxd=max(maxd,dist)
    W=max(1.0,maxd)
    A=R*W
    diffs=set((a[0]-b[0],a[1]-b[1]) for a in pts for b in pts)
    return n,R,W,A,len(diffs)

results={}
for Dname,D in [("1",1.0),("sqrt2",math.sqrt(2)),("2",2.0)]:
    steps=steps_for(D)
    worst_ratio=1e9; worst=None; worst_cn=1e9; worst_up=0
    walks=[]
    for n in [1,2,3,5,8,13,21,34,55,89,144,233,300]:
        for rep in range(12):
            walks.append(("rand",random_saw(n,steps)))
            walks.append(("randbias",random_saw(n,steps,bias=0.8)))
        walks.append(("spiral",spiral(n,D)))
        for w in [1,2,3,5,10]:
            walks.append(("serp%d"%w,serpentine(n,w,1)))
            if D>=2: walks.append(("serp2_%d"%w,serpentine(n,w,2)))
        for st in steps:
            walks.append(("line",line(n,st)))
    for name,pts in walks:
        n,R,W,A,nd=analyse(pts,D)
        ratio=nd/A
        if ratio<worst_ratio: worst_ratio=ratio; worst=(name,n,R,W,A,nd)
        worst_cn=min(worst_cn,A/n)
        worst_up=max(worst_up,A/(D*D*n*n))
    cD=min(1/D,1/(4*math.pi*D*D))
    print(f"D={Dname}: walks={len(walks)} min |E-E|/A = {worst_ratio:.4f} (paper's c_D = min(1/D,1/(4 pi D^2)) = {cD:.4f}); worst={worst}")
    print(f"   min A/n = {worst_cn:.4f} (paper: c n <= A, proof gives c = pi/40 = {math.pi/40:.4f});  max A/(D^2 n^2) = {worst_up:.4f} (<=1 claimed)")
