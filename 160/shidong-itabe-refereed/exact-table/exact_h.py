#!/usr/bin/env python3
"""Exact h(N) for small N (Erdős #160): least k such that [1,N] has a k-colouring where every nontrivial 4-AP
sees >= 3 distinct colours.  SAT per (N,k): x[n][c] one-hot; y[n][{c1,c2}] <-> x[n][c1] v x[n][c2];
for every 4-AP and every colour pair {c1,c2}: not all four in {c1,c2}  (clause  ¬y1 ∨ ¬y2 ∨ ¬y3 ∨ ¬y4).
Symmetry breaking: colour(1)=0, colour(2)=1 (1,2 lie on the 4-AP 1,2,3,4 so they differ in any good colouring
... they do: 1,2,3,4 needs 3 colours so at least two of 1,2,3 differ — not necessarily 1 and 2. Use only colour(1)=0.)
Solver: cadical binary via DIMACS.  Monotone: h(N) is nondecreasing (restrict a colouring of [N+1] to [N]).
Writes exact_h.tsv: N  h(N)  sat_time  unsat_time  witness(colouring of [N] with h(N) colours).
"""
import sys, subprocess, itertools, time, os, tempfile

def solve(N, k, timeout):
    V = {}
    def var(key):
        if key not in V: V[key] = len(V)+1
        return V[key]
    cls = []
    for n in range(1, N+1):
        cls.append([var(('x',n,c)) for c in range(k)])
        for c1 in range(k):
            for c2 in range(c1+1, k): cls.append([-var(('x',n,c1)), -var(('x',n,c2))])
    pairs = [(c1,c2) for c1 in range(k) for c2 in range(c1+1,k)]
    for n in range(1, N+1):
        for (c1,c2) in pairs:
            y = var(('y',n,c1,c2)); a = var(('x',n,c1)); b = var(('x',n,c2))
            cls.append([-y, a, b]); cls.append([-a, y]); cls.append([-b, y])
    for a in range(1, N+1):
        d = 1
        while a + 3*d <= N:
            pts = (a, a+d, a+2*d, a+3*d)
            for (c1,c2) in pairs:
                cls.append([-var(('y',p,c1,c2)) for p in pts])
            d += 1
    cls.append([var(('x',1,0))])
    with tempfile.NamedTemporaryFile('w', suffix='.cnf', delete=False) as f:
        f.write(f"p cnf {len(V)} {len(cls)}\n")
        for c in cls: f.write(' '.join(map(str,c))+' 0\n')
        path = f.name
    t0 = time.time()
    try:
        r = subprocess.run(['cadical','-q',path], capture_output=True, text=True, timeout=timeout)
        out = r.stdout
    except subprocess.TimeoutExpired:
        os.unlink(path); return None, time.time()-t0, None
    os.unlink(path)
    el = time.time()-t0
    if 's SATISFIABLE' in out:
        lits = set()
        for line in out.splitlines():
            if line.startswith('v '):
                for t in line.split()[1:]:
                    v = int(t)
                    if v > 0: lits.add(v)
        col = [None]*(N+1)
        for n in range(1,N+1):
            for c in range(k):
                if var(('x',n,c)) in lits: col[n] = c
        return True, el, col
    if 's UNSATISFIABLE' in out: return False, el, None
    return None, el, None

def verify(col, N):
    for a in range(1,N+1):
        d=1
        while a+3*d<=N:
            if len({col[a],col[a+d],col[a+2*d],col[a+3*d]})<3: return False
            d+=1
    return True

def main():
    Nmax = int(sys.argv[1]) if len(sys.argv)>1 else 40
    timeout = float(sys.argv[2]) if len(sys.argv)>2 else 600
    out = open('exact_h.tsv','a')
    k = 3  # h(4) = 3 lower bound; monotone
    for N in range(4, Nmax+1):
        # find least k: try k (current lower bound) upward; UNSAT at k => h(N) > k
        while True:
            res, el, col = solve(N, k, timeout)
            if res is None:
                print(f"N={N} k={k}: TIMEOUT/UNKNOWN after {el:.0f}s — stopping", flush=True); out.close(); return
            if res:
                assert verify(col, N), "solver witness failed independent verification"
                print(f"N={N}: h(N)={k}  ({el:.2f}s)  witness={''.join(str(c) for c in col[1:])}", flush=True)
                out.write(f"{N}\t{k}\t{el:.2f}\t{''.join(str(c) for c in col[1:])}\n"); out.flush()
                break
            else:
                print(f"   N={N} k={k}: UNSAT ({el:.2f}s) -> h(N) >= {k+1}", flush=True)
                out.write(f"#UNSAT\t{N}\t{k}\t{el:.2f}\n"); out.flush()
                k += 1
    out.close()
main()
