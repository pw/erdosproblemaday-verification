#!/usr/bin/env python3
"""fs_extend.py -- second, structurally different checker for Erdos #531 (written 2026-10-22).
Instead of enumerating every eligible k-set and testing it, it GROWS monochromatic sets: a set A (all of
whose subset sums lie in colour class C and sum(A) <= N) extends by d > max(A) iff d in C, sum(A)+d <= N,
and s+d in C for every subset sum s of A.  FS(A+{d}) = FS(A) | {d} | (FS(A)+d).  Counts monochromatic
k-sets for k = 1..K by colour.  Also counts eligible k-sets by an independent partition DP.
Usage: fs_extend.py FILE [K=4] [N]"""
import sys
def read(path):
    s=''.join(ch for ch in open(path).read() if ch in '01')
    if set(open(path).read())-set('01\r\n'): raise SystemExit('bad chars')
    return s
def mono_counts(col, N, K):
    # col: string, col[i-1] is the colour of i
    cls=[set(),set()]
    for i in range(1,N+1): cls[int(col[i-1])].add(i)
    counts={(c,k):0 for c in (0,1) for k in range(1,K+1)}
    example={}
    def grow(c, A, fs, total, k):
        counts[(c,k)]+=1
        if (c,k) not in example: example[(c,k)]=tuple(A)
        if k==K: return
        C=cls[c]
        for d in range(A[-1]+1, N-total+1):
            if d not in C: continue
            if all((s+d) in C for s in fs):
                grow(c, A+[d], fs|{d}|{s+d for s in fs}, total+d, k+1)
    for c in (0,1):
        for a in sorted(cls[c]):
            grow(c,[a],{a},a,1)
    return counts, example
def eligible(N,K):
    # number of K-sets of distinct positive integers with sum <= N:
    # partitions into K distinct parts: subtract (0,1,..,K-1) -> partitions into K parts (allowing equal, >=1)
    # p(m, parts<=K exactly K parts) via DP over m - K(K-1)/2.
    tot=0
    M=N-K*(K-1)//2
    if M<K: return 0
    # q[m] = # partitions of m into exactly K positive parts = # partitions of m-K into parts <= K
    # partitions of n into parts <= K: standard coin DP
    P=[0]*(M+1); P[0]=1
    for part in range(1,K+1):
        for n in range(part,M+1): P[n]+=P[n-part]
    return sum(P[m-K] for m in range(K,M+1))
if __name__=='__main__':
    path=sys.argv[1]; K=int(sys.argv[2]) if len(sys.argv)>2 else 4
    col=read(path); N=int(sys.argv[3]) if len(sys.argv)>3 else len(col)
    assert 1<=N<=len(col)
    counts,ex=mono_counts(col,N,K)
    print(f"N={N} K={K} eligible_K(DP)={eligible(N,K)}")
    for k in range(1,K+1):
        print(f"  k={k}: mono colour0={counts[(0,k)]} colour1={counts[(1,k)]}" + (f"  e.g. {ex.get((0,k)) or ex.get((1,k))}" if counts[(0,k)]+counts[(1,k)] else ''))
    m=counts[(0,K)]+counts[(1,K)]
    print("RESULT", "PROPER (no monochromatic K-set)" if m==0 else f"NOT PROPER: {m} monochromatic K-sets")
    sys.exit(1 if m else 0)
