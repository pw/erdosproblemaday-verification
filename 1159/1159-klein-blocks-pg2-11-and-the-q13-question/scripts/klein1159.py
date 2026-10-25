#!/usr/bin/env python3
import sys, json, itertools, collections
p=int(sys.argv[1]); S=[tuple(v) for v in json.load(open(sys.argv[2]))[sys.argv[3]]]
def norm(v):
    v=[x%p for x in v]
    for x in v:
        if x: inv=pow(x,-1,p); return tuple((y*inv)%p for y in v)
def det3(a,b,c): return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%p
def frame_of(S):
    for a,b,c,d in itertools.combinations(S,4):
        if det3(a,b,c) and det3(a,b,d) and det3(a,c,d) and det3(b,c,d): return (a,b,c,d)
def msend(a,b,c,d):
    A=[[a[i],b[i],c[i]] for i in range(3)]; D=det3(a,b,c); Di=pow(D,-1,p)
    def rep(col,vec):
        B=[row[:] for row in A]
        for i in range(3): B[i][col]=vec[i]
        return det3([B[0][0],B[1][0],B[2][0]],[B[0][1],B[1][1],B[2][1]],[B[0][2],B[1][2],B[2][2]])
    la,lb,lc=[(rep(k,d)*Di)%p for k in range(3)]
    if 0 in (la,lb,lc): return None
    return [[la*a[i]%p, lb*b[i]%p, lc*c[i]%p] for i in range(3)]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3))%p for j in range(3)] for i in range(3)]
def apply(M,v): return norm([sum(M[i][j]*v[j] for j in range(3)) for i in range(3)])
import sympy
Sset=set(norm(v) for v in S); F=frame_of(S); M0=msend(*F); M0i=[[int(x)%p for x in r] for r in sympy.Matrix(M0).inv_mod(p).tolist()]
G=[]
for a,b,c,d in itertools.permutations(Sset,4):
    if not(det3(a,b,c) and det3(a,b,d) and det3(a,c,d) and det3(b,c,d)): continue
    M1=msend(a,b,c,d)
    if M1 is None: continue
    g=mul(M1,M0i)
    if all(apply(g,s) in Sset for s in S): G.append(g)
print("stabilizer order",len(G))
def proj_eq(A,B):
    # A ~ lambda B
    for i in range(3):
        for j in range(3):
            if B[i][j]:
                lam=A[i][j]*pow(B[i][j],-1,p)%p; break
        else: continue
        break
    return all(A[i][j]==lam*B[i][j]%p for i in range(3) for j in range(3))
I=[[1,0,0],[0,1,0],[0,0,1]]
def order(g):
    h=g
    for k in range(1,200):
        if proj_eq(h,I): return k
        h=mul(h,g)
orders=collections.Counter(order(g) for g in G); print("element orders",dict(sorted(orders.items())))
# involutions: fixed points (eigenvectors) -> centre and axis
invs=[g for g in G if order(g)==2]
centres=set(); axes=set()
pts=[norm(v) for v in [(1,a,b) for a in range(p) for b in range(p)]+[(0,1,a) for a in range(p)]+[(0,0,1)]]
for g in invs:
    fixed=[v for v in pts if apply(g,v)==v]
    # a homology/involution in PGL(3,p), p odd: fixes a point (centre) and a line (axis) pointwise: 1 + (p+1) fixed points
    coll=[v for v in fixed]
    # axis = the p+1 collinear fixed points, centre = the remaining one
    for v in fixed:
        others=[w for w in fixed if w!=v]
        if all(det3(others[0],others[1],w)==0 for w in others[2:]) and det3(others[0],others[1],v)!=0:
            centres.add(v); axes.add((others[0],others[1])); break
print("involutions",len(invs),"distinct centres",len(centres),"centres ⊆ S:",centres<=Sset,"centres == S:",centres==Sset)
# which lines are the axes? count points of S on each axis
axis_counts=collections.Counter()
for a,b in axes:
    n=sum(1 for s in Sset if det3(a,b,s)==0); axis_counts[n]+=1
print("points of S on each involution axis:",dict(axis_counts))
# orbit of G on S and on lines meeting S by type
orb=set(); 
for g in G: orb.add(apply(g,F[0]))
print("orbit of one point of S under G has size",len(orb),"(transitive on S:",len(orb)==len(Sset),")")
# simplicity test: a group of order 168 with 21 involutions, 56 elts of order 3, 42 of order 4, 48 of order 7 is PSL(2,7)
print("PSL(2,7) census (1,21,56,42,48) matches:", dict(sorted(orders.items()))=={1:1,2:21,3:56,4:42,7:48})
json.dump(G,open(f'runs/stab_{sys.argv[3]}_q{p}.json','w'))

# ---- rigorous identification: simplicity + the commuting-incidence criterion
def key(M):
    # canonical projective representative: scale so first nonzero entry is 1
    flat=[M[i][j] for i in range(3) for j in range(3)]
    for x in flat:
        if x: inv=pow(x,-1,p); return tuple((y*inv)%p for y in flat)
Gk={key(g):g for g in G}; assert len(Gk)==len(G)
def inv(g): return [[int(x)%p for x in r] for r in sympy.Matrix(g).inv_mod(p).tolist()]
def normal_closure(g):
    N={key(I)}; frontier=[g]; N.add(key(g))
    while frontier:
        h=frontier.pop(); 
        for a in G:
            c=mul(mul(a,h),inv(a))
            if key(c) not in N: N.add(key(c)); frontier.append(c)
        # close under products
    # closure under multiplication
    elems=[Gk[k] for k in N]; changed=True
    while changed:
        changed=False; cur=list(N)
        for k1 in cur:
            for k2 in cur:
                m=key(mul(Gk[k1],Gk[k2]))
                if m not in N: N.add(m); changed=True
    return len(N)
reps=[]; seen=set()
for g in G:
    k=key(g)
    if k in seen: continue
    cls={key(mul(mul(a,g),inv(a))) for a in G}; seen|=cls; reps.append((len(cls),order(g),g))
print("conjugacy classes (size,order):",sorted((s,o) for s,o,_ in reps))
nc=[normal_closure(g) for s,o,g in reps if o>1]
print("normal closures of nontrivial class reps have orders",nc,"-> SIMPLE:",all(n==len(G) for n in nc))
# commuting-incidence: centre(sigma) on axis(tau) <=> sigma tau = tau sigma, for distinct involutions
def centre_axis(g):
    fixed=[v for v in pts if apply(g,v)==v]
    for v in fixed:
        others=[w for w in fixed if w!=v]
        if all(det3(others[0],others[1],w)==0 for w in others[2:]) and det3(others[0],others[1],v)!=0:
            return v,(others[0],others[1])
CA=[centre_axis(g) for g in invs]
ok=True; inc_count=0
for i,gi in enumerate(invs):
    for j,gj in enumerate(invs):
        if i==j: continue
        on_axis = det3(CA[j][1][0],CA[j][1][1],CA[i][0])==0
        commute = proj_eq(mul(gi,gj),mul(gj,gi))
        inc_count+=on_axis
        if on_axis!=commute: ok=False
print("centre(σ)∈axis(τ) ⟺ στ=τσ for all 21·20 ordered pairs:",ok,"; incidences",inc_count,"(= 21·4 =",21*4,")")
# the 28 three-secants: are they exactly the lines through 3 centres pairwise NOT commuting? count lines with 3 centres
lines3=set()
for a,b,c in itertools.combinations(sorted(Sset),3):
    if det3(a,b,c)==0:
        # line through a,b: canonical as the set of points
        L=frozenset(v for v in pts if det3(a,b,v)==0); lines3.add(L)
print("distinct lines through ≥3 points of S:",len(lines3), "; sizes:",collections.Counter(len(L&Sset) for L in lines3))
