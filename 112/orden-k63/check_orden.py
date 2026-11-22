#!/usr/bin/env python3
"""Own checker (written from the submission text, not the submitter's code) for oriented-graph
witnesses of k(n,m) >= N+1: an oriented graph on N vertices with no independent n-set and no
transitive tournament on m vertices.  Bitset recursion; exit 0 = all pass."""
import sys, itertools

def circulant(N, S):
    arcs=set()
    for x in range(N):
        for s in S: arcs.add((x,(x+s)%N))
    return N, arcs

def bicirculant(M, Sij):
    # vertex (x,i) -> 19i+x style numbering M*i+x; arc (x,i)->(x+s, j) for s in S_ij
    arcs=set()
    for i in (0,1):
        for j in (0,1):
            for x in range(M):
                for s in Sij[(i,j)]:
                    arcs.add((M*i+x, M*j+(x+s)%M))
    return 2*M, arcs

def analyse(N, arcs):
    out=[0]*N; adj=[0]*N
    loops=sum(1 for (a,b) in arcs if a==b)
    two_cycles=sum(1 for (a,b) in arcs if (b,a) in arcs)//2
    for a,b in arcs:
        out[a]|=1<<b; adj[a]|=1<<b; adj[b]|=1<<a
    return out, adj, loops, two_cycles

def has_indep(N, adj, n):
    full=(1<<N)-1
    def rec(cand, need):
        if need==0: return True
        while cand:
            if bin(cand).count('1')<need: return False
            v=(cand&-cand).bit_length()-1
            cand&=~(1<<v)
            if rec(cand & ~adj[v], need-1): return True
        return False
    return rec(full, n)

def has_tt(N, out, m):
    # TT_m exists iff some v has TT_{m-1} inside its out-neighbourhood (v = source)
    def rec(cand, need):
        if need==0: return True
        while cand:
            if bin(cand).count('1')<need: return False
            v=(cand&-cand).bit_length()-1
            cand&=~(1<<v)
            if rec(cand & out[v], need-1): return True
        return False
    return rec((1<<N)-1, m)

def check(name, N, arcs, n, m, expect_pass=True):
    out, adj, loops, tc = analyse(N, arcs)
    ind = has_indep(N, adj, n); tt = has_tt(N, out, m)
    ok = (loops==0 and tc==0 and not ind and not tt)
    print(f"{name}: N={N} arcs={len(arcs)} loops={loops} 2cycles={tc} indep{n}={ind} TT{m}={tt} -> {'PASS' if ok else 'FAIL'}"
          + ("" if ok==expect_pass else "   <-- UNEXPECTED"))
    return ok==expect_pass

allok=True
# --- the four claimed witnesses, read from the submission text (eqf2h6) ---
N,a=bicirculant(19,{(0,0):{5,6,16,17},(0,1):{16,17},(1,0):{5,6},(1,1):{10,11,16,17}})
allok&=check("k(7,3)>=39 bicirculant Z19x2",N,a,7,3)
N,a=bicirculant(23,{(0,0):{2,5,11,19},(0,1):{4,10,18},(1,0):{0,8,17},(1,1):{2,11,19,20}})
allok&=check("k(8,3)>=47 bicirculant Z23x2",N,a,8,3)
N,a=circulant(77,{3,11,14,19,20,22,30,35,36,40,44,46,52,64,68,75})
allok&=check("k(6,4)>=78 circulant Z77",N,a,6,4)
N,a=circulant(70,{1,2,7,8,14,15,16,17,21,24,26,29,30,32,37,39,45,47,48,52,60,61,64})
allok&=check("k(3,6)>=71 circulant Z70",N,a,3,6)
# --- positive controls (known witnesses) ---
N,a=circulant(28,{3,8,10,12,17})            # Kirtchakov, k(6,3)>=29
allok&=check("control Kirtchakov Z28 k(6,3)>=29",N,a,6,3)
N,a=circulant(3,{1})                         # directed triangle: k(2,3)>=4
allok&=check("control C3 k(2,3)>=4",N,a,2,3)
# --- negative controls: the same graphs must FAIL one size up / with an arc set perturbed ---
N,a=bicirculant(19,{(0,0):{5,6,16,17},(0,1):{16,17},(1,0):{5,6},(1,1):{10,11,16,17}})
allok&=check("neg: Z19x2 asked for no indep6",N,a,6,3,expect_pass=False)
N,a=circulant(77,{3,11,14,19,20,22,30,35,36,40,44,46,52,64,68,75})
allok&=check("neg: Z77 asked for no TT3",N,a,6,3,expect_pass=False)
N,a=circulant(70,{1,2,7,8,14,15,16,17,21,24,26,29,30,32,37,39,45,47,48,52,60,61,64,69})
allok&=check("neg: Z70 with 69 added (2-cycle with 1)",N,a,3,6,expect_pass=False)
N,a=circulant(70,{1,2,7,8,14,15,16,17,21,24,26,29,30,32,37,39,45,47,48,52,60,61})
allok&=check("neg: Z70 with 64 dropped",N,a,3,6,expect_pass=False)
print("ALL AS EXPECTED" if allok else "SOMETHING UNEXPECTED"); sys.exit(0 if allok else 1)
