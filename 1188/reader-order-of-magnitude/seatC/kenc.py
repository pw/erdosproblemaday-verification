"""Seat C: SAT encoding for 'is there a minimal distinct covering system with moduli in M and >= k classes'.
Different from the paper's CP-SAT model (8.6), which uses one 'covered exactly once' variable per z and
translates a private integer to 0. Here:
  c[n,a]   class a mod n chosen; AMO per n (pairwise); used[n] <-> OR_a c[n,a]
  cover    for every z in Z/L: OR_n c[n, z mod n]
  witness  pi[n,z] -> c[n, z mod n], and pi[n,z] -> no OTHER chosen class contains z
           (via prefix-OR / suffix-OR chains over the moduli at z); c[n,a] -> OR_{z = a mod n} pi[n,z]
  card     sum used[n] >= k   (pysat totalizer)
  symmetry (optional) the class of the LARGEST used modulus has residue 0 (any system can be translated so).
usage: python3 kenc.py --moduli 2 3 ... --k K [--solver kissat|cadical] [--nosym] [--force 'a/n a/n ...'] [--forbid-used n ...]
Prints SAT + the system (re-verified by checker.py) or UNSAT.
"""
import sys, os, subprocess, argparse, time
from math import gcd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import checker
from pysat.card import CardEnc, EncType

KISSAT = os.path.expanduser('~/MathDyad/tools/kissat/build/kissat')

def smooth_set(x):
    import math
    r = math.isqrt(x)
    out = []
    for n in range(2, x + 1):
        m, p, big = n, 2, 0
        while p * p <= m:
            while m % p == 0:
                big = max(big, p); m //= p
            p += 1
        if m > 1: big = max(big, m)
        if big <= r:
            out.append(n)
    return out

def build(M, k, sym=True, force=None, forbid_used=()):
    M = sorted(M); K = len(M)
    L = 1
    for n in M: L = L // gcd(L, n) * n
    nv = [0]
    def new():
        nv[0] += 1; return nv[0]
    c = {(n, a): new() for n in M for a in range(n)}
    used = {n: new() for n in M}
    cls = []
    for n in M:
        for a in range(n):
            cls.append([-c[n, a], used[n]])
        cls.append([-used[n]] + [c[n, a] for a in range(n)])
        for a in range(n):
            for b in range(a + 1, n):
                cls.append([-c[n, a], -c[n, b]])
    for z in range(L):
        cls.append([c[n, z % n] for n in M])
    pi = {}
    for z in range(L):
        lits = [c[n, z % n] for n in M]
        P = [new() for _ in range(K)]
        S = [new() for _ in range(K)]
        for j in range(K):
            cls.append([-lits[j], P[j]])
            if j: cls.append([-P[j - 1], P[j]])
            cls.append([-lits[j], S[j]])
            if j < K - 1: cls.append([-S[j + 1], S[j]])
        for j, n in enumerate(M):
            v = new(); pi[n, z] = v
            cls.append([-v, lits[j]])
            if j: cls.append([-v, -P[j - 1]])
            if j < K - 1: cls.append([-v, -S[j + 1]])
    for n in M:
        for a in range(n):
            cls.append([-c[n, a]] + [pi[n, z] for z in range(a, L, n)])
    if sym:
        for i, n in enumerate(M):
            larger = [used[m] for m in M[i + 1:]]
            for a in range(1, n):
                cls.append([-c[n, a]] + larger)
    if k > 0:
        enc = CardEnc.atleast(lits=[used[n] for n in M], bound=k, top_id=nv[0], encoding=EncType.totalizer)
        nv[0] = max(nv[0], enc.nv)
        cls.extend(enc.clauses)
    if force is not None:
        for (a, n) in force:
            cls.append([c[n, a % n]])
        fm = {n for a, n in force}
        for n in M:
            if n not in fm:
                cls.append([-used[n]])
    for n in forbid_used:
        cls.append([-used[n]])
    return M, L, c, nv[0], cls

def solve(M, k, solver='kissat', sym=True, force=None, forbid_used=(), timeout=1800, tag='q'):
    M, L, c, nvars, cls = build(M, k, sym, force, forbid_used)
    path = '/tmp/seatC_%s_%d.cnf' % (tag, os.getpid())
    with open(path, 'w') as f:
        f.write('p cnf %d %d\n' % (nvars, len(cls)))
        for cl in cls:
            f.write(' '.join(map(str, cl)) + ' 0\n')
    t0 = time.time()
    if solver == 'kissat':
        cmd = [KISSAT, '-q', path]
    else:
        cmd = ['cadical', '-q', path]
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        out = p.stdout
    except subprocess.TimeoutExpired:
        os.unlink(path)
        return 'TIMEOUT', None, nvars, len(cls), time.time() - t0
    os.unlink(path)
    dt = time.time() - t0
    status = None; vals = set()
    for line in out.splitlines():
        if line.startswith('s '):
            status = line[2:].strip()
        elif line.startswith('v '):
            for t in line[2:].split():
                v = int(t)
                if v > 0: vals.add(v)
    if status == 'SATISFIABLE':
        sysm = [(a, n) for (n, a), v in c.items() if v in vals]
        return 'SAT', sorted(sysm, key=lambda t: t[1]), nvars, len(cls), dt
    return status, None, nvars, len(cls), dt

if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--moduli', type=int, nargs='*')
    ap.add_argument('--x', type=int)
    ap.add_argument('--k', type=int, required=True)
    ap.add_argument('--solver', default='kissat')
    ap.add_argument('--nosym', action='store_true')
    ap.add_argument('--force', default=None)
    ap.add_argument('--forbid-used', type=int, nargs='*', default=[])
    ap.add_argument('--timeout', type=int, default=1800)
    a = ap.parse_args()
    M = a.moduli if a.moduli else smooth_set(a.x)
    force = None
    if a.force:
        force = [tuple(map(int, t.split('/'))) for t in a.force.split()]
    st, sysm, nv, nc, dt = solve(M, a.k, a.solver, not a.nosym, force, a.forbid_used, a.timeout)
    print('MODULI', M, 'k>=', a.k, 'solver', a.solver, 'sym', not a.nosym, 'vars', nv, 'clauses', nc)
    print('RESULT', st, 'time %.1fs' % dt)
    if sysm:
        ok = checker.accept(sysm)
        print('SYSTEM (%d classes):' % len(sysm), ' '.join('%d/%d' % t for t in sysm))
        print('checker.accept =', ok, ' max modulus', max(n for a_, n in sysm))
