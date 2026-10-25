#!/usr/bin/env python3
"""Projective equivalence + stabilizer order of point sets in PG(2,p), p prime, by frame enumeration.
A projectivity is determined by the images of an ordered frame (4 points, no 3 collinear).
usage: equiv1159.py p witnesses.json   (json: {name: [[x,y,z],...], ...})
"""
import sys, json, itertools
p=int(sys.argv[1]); W=json.load(open(sys.argv[2]))
def norm(v):
    v=[x%p for x in v]
    for x in v:
        if x:
            inv=pow(x,-1,p); return tuple((y*inv)%p for y in v)
    raise ValueError
def det3(a,b,c):
    return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%p
def frame_of(S):
    for a,b,c,d in itertools.combinations(S,4):
        if det3(a,b,c) and det3(a,b,d) and det3(a,c,d) and det3(b,c,d): return (a,b,c,d)
def matrix_sending_std_to(a,b,c,d):
    """M with M e1~a, M e2~b, M e3~c, M(1,1,1)~d: columns la*a, lb*b, lc*c where la*a+lb*b+lc*c = d (solve)."""
    # solve [a b c] (la,lb,lc)^T = d mod p via adjugate
    A=[[a[i],b[i],c[i]] for i in range(3)]
    D=det3(a,b,c); Dinv=pow(D,-1,p)
    # Cramer
    def rep(col,vec):
        B=[row[:] for row in A]
        for i in range(3): B[i][col]=vec[i]
        return det3([B[0][0],B[1][0],B[2][0]],[B[0][1],B[1][1],B[2][1]],[B[0][2],B[1][2],B[2][2]])
    la=(rep(0,d)*Dinv)%p; lb=(rep(1,d)*Dinv)%p; lc=(rep(2,d)*Dinv)%p
    if 0 in (la,lb,lc): return None
    return [[la*a[i]%p, lb*b[i]%p, lc*c[i]%p] for i in range(3)]
def apply(M,v): return norm([sum(M[i][j]*v[j] for j in range(3)) for i in range(3)])
def maps_between(S,T):
    """all projectivities g with g(S)=T (as a list of matrices), via frame enumeration."""
    S=[norm(v) for v in S]; T=[norm(v) for v in T]; Tset=set(T)
    F=frame_of(S); M0=matrix_sending_std_to(*F)
    # g = M1 * M0^{-1}; enumerate ordered frames in T
    def inv3(M):
        import sympy
        return [[int(x)%p for x in row] for row in sympy.Matrix(M).inv_mod(p).tolist()]
    M0i=inv3(M0); out=[]
    for a,b,c,d in itertools.permutations(T,4):
        if not(det3(a,b,c) and det3(a,b,d) and det3(a,c,d) and det3(b,c,d)): continue
        M1=matrix_sending_std_to(a,b,c,d)
        if M1 is None: continue
        G=[[sum(M1[i][k]*M0i[k][j] for k in range(3))%p for j in range(3)] for i in range(3)]
        if all(apply(G,s) in Tset for s in S): out.append(G)
    return out
names=list(W)
for n in names:
    g=maps_between(W[n],W[n]); print(f"{n}: |S|={len(W[n])} stabilizer order in PGL(3,{p}) = {len(g)}")
for a,b in itertools.combinations(names,2):
    g=maps_between(W[a],W[b]); print(f"{a} ~ {b}: {len(g)} projectivities map one onto the other -> {'EQUIVALENT' if g else 'NOT equivalent'}")
