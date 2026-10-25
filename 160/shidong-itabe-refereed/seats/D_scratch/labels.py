#!/usr/bin/env python3
"""Referee seat D: full-label brute force in the NON-injective regime.
 lambda^(m): (d_0 mod m,...,d_{L-1} mod m, ||v_P||^2), P = mB+1; the paper uses m=24, which is injective-ish on any
 brute-forceable horizon, so we exercise the identical proof with m=4/m=6 (proof needs m>=3 for Lemma 4.1 and m even
 for the parity step).  mu_{B,L}: dyadic buckets + square norm.  nu_p: thirds of low two digits + F_{p^3} norm."""
import itertools, random, sys

def digits(n,base,k):
    xs=[]
    for _ in range(k): xs.append(n%base); n//=base
    return xs

def scan(col,N,pats):
    cnt={k:0 for k in pats}; first={}
    for a in range(N):
        ca=col[a]
        for d in range(1,(N-1-a)//3+1):
            c0=ca; c1=col[a+d]; c2=col[a+2*d]; c3=col[a+3*d]
            for k,f in pats.items():
                if f(c0,c1,c2,c3):
                    cnt[k]+=1; first.setdefault(k,(a,d))
    return cnt,first

three=lambda c0,c1,c2,c3: (c0==c1==c2) or (c1==c2==c3) or (c0==c1==c3) or (c0==c2==c3)
abab=lambda c0,c1,c2,c3: c0==c2 and c1==c3
aabb=lambda c0,c1,c2,c3: c0==c1 and c2==c3
abba=lambda c0,c1,c2,c3: c0==c3 and c1==c2

rc=0
which=sys.argv[1:] or ['lam','mu','nu']
if 'lam' in which:
  for (m,B,L) in [(4,1,4),(6,1,3),(4,2,3),(2,2,3),(3,2,3)]:
    P=m*B+1; N=P**(L+1)
    col=[tuple(x%m for x in digits(n,P,L+1)[:L])+(sum(v*v for v in digits(n,P,L+1)),) for n in range(N)]
    cnt,first=scan(col,N,{'three':three,'abab':abab})
    tag='' if (m>=3 and m%2==0 and P%2==1) else '  <- CONTROL (m<3 or m odd / P even): violations expected'
    print(f"lambda^(m={m}) P={P} L={L}: N={N} palette {len(set(col))}  three-equal {cnt['three']}  ABAB {cnt['abab']}  first {first}{tag}")
    if not tag and (cnt['three'] or cnt['abab']): rc=1
if 'mu' in which:
  for (B,L) in [(4,4),(4,5),(16,2),(32,1),(6,3),(12,2)]:
    N=B**(L+1)
    beta=lambda r:(r+1).bit_length()-1
    col=[tuple(beta(x) for x in digits(n,B,L+1)[:L])+(sum(v*v for v in digits(n,B,L+1)),) for n in range(N)]
    cnt,first=scan(col,N,{'aabb':aabb})
    print(f"mu B={B} L={L}: N={N} palette {len(set(col))}  AABB {cnt['aabb']}")
    if cnt['aabb']: rc=1
if 'nu' in which:
  sys.path.insert(0,'/home/exedev/MathDyad/erdos160')
  import importlib.util
  spec=importlib.util.spec_from_file_location('ci','/home/exedev/MathDyad/erdos160/check_itabe.py')
  # reuse field arithmetic without running main(): copy minimal functions
  def irreducible_cubics(p):
    return [(c0,c1,c2) for c2 in range(p) for c1 in range(p) for c0 in range(p) if all((t**3+c2*t*t+c1*t+c0)%p for t in range(p))]
  def mul(a,b,p,f):
    c0,c1,c2=f; r=[0]*5
    for i in range(3):
        for j in range(3): r[i+j]=(r[i+j]+a[i]*b[j])%p
    for deg in (4,3):
        k=r[deg]
        if k:
            r[deg]=0; s=deg-3
            r[s+2]=(r[s+2]-k*c2)%p; r[s+1]=(r[s+1]-k*c1)%p; r[s]=(r[s]-k*c0)%p
    return tuple(r[:3])
  def norm(z,p,f):
    # det of multiplication matrix
    cols=[mul(z,e,p,f) for e in ((1,0,0),(0,1,0),(0,0,1))]
    M=[[cols[j][i] for j in range(3)] for i in range(3)]
    d=(M[0][0]*(M[1][1]*M[2][2]-M[1][2]*M[2][1])-M[0][1]*(M[1][0]*M[2][2]-M[1][2]*M[2][0])+M[0][2]*(M[1][0]*M[2][1]-M[1][1]*M[2][0]))%p
    return d
  random.seed(7)
  for p in [13,17]:
    f=random.choice(irreducible_cubics(p)); N=p**3
    # random F_p-linear change of basis iota (paper: 'choose an F_p-linear isomorphism')
    while True:
      A=[[random.randrange(p) for _ in range(3)] for _ in range(3)]
      det=(A[0][0]*(A[1][1]*A[2][2]-A[1][2]*A[2][1])-A[0][1]*(A[1][0]*A[2][2]-A[1][2]*A[2][0])+A[0][2]*(A[1][0]*A[2][1]-A[1][1]*A[2][0]))%p
      if det: break
    t=lambda r:0 if 3*r<p else (1 if 3*r<2*p else 2)
    col=[]
    for n in range(N):
      r,w,u=digits(n,p,3)
      z=tuple(sum(A[i][j]*(r,w,u)[j] for j in range(3))%p for i in range(3))
      col.append((t(r),t(w),norm(z,p,f)))
    cnt,first=scan(col,N,{'abba':abba})
    print(f"nu p={p} f={f} random iota: N={N} palette {len(set(col))} (9p={9*p})  ABBA-equalities {cnt['abba']}")
    if cnt['abba']: rc=1
print("RC",rc)
