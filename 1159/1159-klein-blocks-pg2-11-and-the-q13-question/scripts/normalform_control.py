#!/usr/bin/env python3
"""Constructive control for the symmetry breaks: map the known q=11 witness K into break2 / cube-(3,3) normal form by an
explicit projectivity, then check the CNF accepts it (append unit clauses for all point variables; cadical must say SAT)."""
import sys, json, itertools, subprocess
sys.path.insert(0,'.'); from model1159 import plane, check
q=11; pts,idx,lines=plane(q)
K=[tuple(p) for p in json.load(open('runs/witnesses_q11_c4.json'))['cadical']]; Kset=set(K)
def norm(v):
    v=[x%q for x in v]
    for x in v:
        if x: inv=pow(x,-1,q); return tuple((y*inv)%q for y in v)
def det3(a,b,c): return (a[0]*(b[1]*c[2]-b[2]*c[1])-a[1]*(b[0]*c[2]-b[2]*c[0])+a[2]*(b[0]*c[1]-b[1]*c[0]))%q
def line_through(a,b): return [p for p in pts if det3(a,b,p)==0]
def msend(a,b,c,d):
    A=[[a[i],b[i],c[i]] for i in range(3)]; D=det3(a,b,c); Di=pow(D,-1,q)
    def rep(col,vec):
        B=[row[:] for row in A]
        for i in range(3): B[i][col]=vec[i]
        return det3([B[0][0],B[1][0],B[2][0]],[B[0][1],B[1][1],B[2][1]],[B[0][2],B[1][2],B[2][2]])
    la,lb,lc=[(rep(k,d)*Di)%q for k in range(3)]; assert 0 not in (la,lb,lc)
    return [[la*a[i]%q, lb*b[i]%q, lc*c[i]%q] for i in range(3)]
def mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3))%q for j in range(3)] for i in range(3)]
def apply(M,v): return norm([sum(M[i][j]*v[j] for j in range(3)) for i in range(3)])
import sympy
def inv(M): return [[int(x)%q for x in r] for r in sympy.Matrix(M).inv_mod(q).tolist()]
P=K[0]
tangents=[L for L in [line_through(P,X) for X in pts if X!=P] if len(set(L)&Kset)==1]
T=tangents[0]
foursec=[L for L in {tuple(sorted(line_through(P,X))) for X in K if X!=P} if len(set(L)&Kset)==4]
L1=list(foursec[0]); L2=list(foursec[1])
Q=[X for X in L1 if X in Kset and X!=P][0]
U=[L for L in [line_through(Q,X) for X in pts if X!=Q] if len(set(L)&Kset)==1 and P not in L][0]
TU=[X for X in T if X in U][0]
R=[X for X in T if X!=P and X!=TU][0]; W=[X for X in U if X!=Q and X!=TU][0]
M0=msend(P,Q,R,W); M1=msend((0,0,1),(1,0,0),(0,1,1),(1,1,0)); g=mul(M1,inv(M0))
img=[apply(g,X) for X in K]
assert (0,0,1) in img and (1,0,0) in img
assert len(set(img)&set(line_through((0,0,1),(0,1,0))))==1, "L0 not tangent"   # x=0
assert len(set(img)&set(line_through((1,0,0),(0,1,0))))==1, "M1 not tangent"   # z=0
print("break2 normal form reached: P0,Q1 in image; x=0 and z=0 tangents. image check:",check(q,4,[list(p) for p in img]))
# cube (3,3): L2 image is y = m x through P0; scale y by 1/m; then put (1,0,b)->(1,0,1)
L2img=[apply(g,X) for X in L2]; aff=[X for X in L2img if X[0]==1]; m=aff[0][1]; assert m!=0
D1=[[1,0,0],[0,pow(m,-1,q),0],[0,0,1]]; img2=[apply(D1,X) for X in img]
b=[X for X in img2 if X[0]==1 and X[1]==0 and X[2]!=0][0][2]
D2=[[1,0,0],[0,1,0],[0,0,pow(b,-1,q)]]; img3=[apply(D2,X) for X in img2]
assert (1,0,1) in img3 and (0,0,1) in img3 and (1,0,0) in img3
yx=[X for X in pts if (X[0]-X[1])%q==0]; print("points of image on y=x:",len(set(img3)&set(yx)),"(expect 4); on y=0:",len(set(img3)&set(line_through((0,0,1),(1,0,0)))),"(expect 4)")
print("cube-normal-form image check:",check(q,4,[list(p) for p in img3]))
json.dump({'break2':[list(p) for p in img],'cube33':[list(p) for p in img3]},open('runs/klein_normal_forms_q11.json','w'))
def accept(cnf_path,S):
    Sidx={idx[p] for p in S}
    hdr=open(cnf_path).readline().split(); nv,nc=int(hdr[2]),int(hdr[3])
    tmp=cnf_path+'.unitctl.cnf'
    with open(tmp,'w') as f:
        f.write(f"p cnf {nv} {nc+len(pts)}\n")
        with open(cnf_path) as src:
            next(src); f.write(src.read())
        for i in range(len(pts)): f.write(f"{i+1 if i in Sidx else -(i+1)} 0\n")
    out=subprocess.run(['cadical','-q','-t','60',tmp],capture_output=True,text=True).stdout
    return [l for l in out.splitlines() if l.startswith('s ')][0]
print("break2 CNF accepts the normal-form Klein set:",accept('runs/pg11_c4_b2.cnf',img))
print("cube (3,3) CNF accepts the cube-normal-form Klein set:",accept('runs/cube_q11_c4_33.cnf',img3))
print("cube (3,2) CNF on the same set (expect UNSAT: L2 has 3 further points, not 2):",accept('runs/cube_q11_c4_32.cnf',img3))
