# Explicit WLOG chain at q=13, with explicit group elements, run over ALL choices (every P0 with a tangent, every tangent L0,
# every max line L1, every Q1, every tangent M1 at Q1, every second-max line L2, every Q2).  After EVERY step it re-asserts
# everything fixed before it, in the docstring's order.  Input: a minimal blocking set with max line intersection C.
import sys,json,itertools
from pg import plane,norm
import os; q=int(os.environ.get("Q","13")); pts,lines=plane(q); PS=set(pts)
inv=lambda a:pow(a%q,q-2,q)
def mat_mul(A,B): return [[sum(A[i][k]*B[k][j] for k in range(3))%q for j in range(3)] for i in range(3)]
def mat_inv(A):
    a,b,c=A[0];d,e,f=A[1];g,h,i=A[2]
    det=(a*(e*i-f*h)-b*(d*i-f*g)+c*(d*h-e*g))%q; assert det; di=inv(det)
    adj=[[e*i-f*h,c*h-b*i,b*f-c*e],[f*g-d*i,a*i-c*g,c*d-a*f],[d*h-e*g,b*g-a*h,a*e-b*d]]
    return [[(x*di)%q for x in r] for r in adj]
def act(M,S): return {norm(tuple(sum(M[i][k]*p[k] for k in range(3))%q for i in range(3)),q) for p in S}
L=lambda key: lines[key]
X0,Y0,Z0,YX=L((1,0,0)),L((0,1,0)),L((0,0,1)),L((1,q-1,0))
P0,Q1,Q2=(0,0,1),(1,0,0),(1,0,1)
pencil=[k for k,s in lines.items() if P0 in s]
def further(S,key): return len(S&lines[key])-(P0 in S)
def tangents(S,p): return [k for k,s in lines.items() if p in s and len(S&s)==1]
def check(S,stage,C,c1=None,c2=None):
    assert all(1<=len(S&s)<=C for s in lines.values())
    assert P0 in S and S&X0=={P0}, stage+': flag'
    if stage=='flag': return
    oth=[k for k in pencil if k!=(1,0,0)]
    assert further(S,(0,1,0))==c1==max(further(S,k) for k in oth), stage+': y=0 max'
    if stage=='L1': return
    assert Q1 in S, stage+': Q1'
    if stage=='Q1': return
    assert S&Z0=={Q1}, stage+': z=0 tangent at Q1'
    if stage=='M1': return
    assert further(S,(1,q-1,0))==c2==max(further(S,k) for k in oth if k!=(0,1,0)), stage+': y=x second max'
    if stage=='L2': return
    if c1>=2: assert Q2 in S, stage+': Q2'
def run(S0,C):
    cubes={}; nconf=0
    for p in S0:
        for l0 in tangents(S0,p):
            # A: p -> (0,0,1), l0 -> x=0 ; columns of A^-1 = (point off l0, second point of l0, p)
            r=next(t for t in sorted(lines[l0]) if t!=p); u=next(t for t in pts if t not in lines[l0])
            Ainv=[[u[i],r[i],p[i]] for i in range(3)]; A=mat_inv(Ainv); S1=act(A,S0); check(S1,'flag',C)
            oth=[k for k in pencil if k!=(1,0,0)]; c1=max(further(S1,k) for k in oth)
            for l1 in [k for k in oth if further(S1,k)==c1]:
                # l1 = [a:1:0] i.e. y=-a x ; elation (x,y,z)->(x,y+a x,z) (axis x=0, centre P0) sends it to y=0
                a=l1[0]*inv(l1[1]); E=[[1,0,0],[a,1,0],[0,0,1]]; S2=act(E,S1); check(S2,'L1',C,c1)
                for qq in sorted(S2&Y0-{P0}):
                    t=qq[2]; E2=[[1,0,0],[0,1,0],[-t,0,1]]; S3=act(E2,S2); check(S3,'Q1',C,c1)   # (x,y,z)->(x,y,z-tx)
                    for m1 in tangents(S3,Q1):
                        b,c=m1[1],m1[2]; assert m1[0]==0 and c!=0          # by+cz=0, z=-(b/c)y
                        g=b*inv(c); Sh=[[1,0,0],[0,1,0],[0,g,1]]; S4=act(Sh,S3); check(S4,'M1',C,c1)   # z->z+(b/c)y
                        oth2=[k for k in oth if k!=(0,1,0)]; c2=max(further(S4,k) for k in oth2)
                        for l2 in [k for k in oth2 if further(S4,k)==c2]:
                            mu=(-l2[0]*inv(l2[1]))%q; assert mu   # y=mu x
                            D=[[1,0,0],[0,inv(mu),0],[0,0,1]]; S5=act(D,S4); check(S5,'L2',C,c1,c2)
                            q2s=sorted(S5&Y0-{P0,Q1}) if c1>=2 else [None]
                            for qq2 in q2s:
                                if qq2 is None: S6=S5
                                else:
                                    D2=[[1,0,0],[0,1,0],[0,0,inv(qq2[2])]]; S6=act(D2,S5)
                                check(S6,'Q2',C,c1,c2); nconf+=1; cubes.setdefault((c1,c2),S6)
    return nconf,cubes
if __name__=='__main__':
    W=[norm(tuple(p),q) for p in json.load(open(sys.argv[1]))]; C=int(sys.argv[2]); S=set(W)
    # minimalise (drop points with no tangent until none left), report max after each drop
    while True:
        bad=[p for p in sorted(S) if not tangents(S,p)]
        if not bad: break
        S=S-{bad[0]}; print('dropped tangentless',bad[0],'-> |S|',len(S),'max',max(len(S&s) for s in lines.values()),'blocking',all(S&s for s in lines.values()))
    n,cubes=run(S,C)
    print('minimal |S|=',len(S),'max',max(len(S&s) for s in lines.values()),'| normalisations performed (all choices):',n,'| every one passed every re-check | cubes hit:',sorted(cubes))
    json.dump({str(k):sorted(v) for k,v in cubes.items()},open(sys.argv[3],'w'))
