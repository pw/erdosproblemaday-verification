#!/usr/bin/env python3
"""H1 analogue at general odd k (2026-10-19 15Z seat, insight probe, independent of fs/ and the authors):
n = k^2, one vertex x of degree k+1, all others degree k, C4-free.  Saturation at x ((k+1)(k-1) = n-1) forces
N(x) = perfect matching + every other vertex exactly one nbr in N(x), blocks of k-2.  We do NOT impose that here:
only x's degree, everyone else's degree, C4-freeness (codegree <= 1).  x = 0 and N(x) = 1..k+1 by relabelling.
Usage: h1k.py k [solver-seconds]   -> SAT (prints + re-checks the graph) / UNSAT / UNKNOWN"""
import itertools, sys, subprocess, tempfile, os
from pysat.formula import CNF
from pysat.card import CardEnc, EncType
k = int(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 600
n = k * k
var = {}
for a, b in itertools.combinations(range(n), 2):
    var[(a, b)] = len(var) + 1
e = lambda a, b: var[(a, b) if a < b else (b, a)]
cnf = CNF(); top = len(var)
for v in range(1, k + 2): cnf.append([e(0, v)])
for v in range(k + 2, n): cnf.append([-e(0, v)])
for v in range(1, n):
    lits = [e(v, w) for w in range(n) if w != v]
    c = CardEnc.equals(lits=lits, bound=k, top_id=top, encoding=EncType.seqcounter); top = max(top, c.nv)
    cnf.extend(c.clauses)
for a, b in itertools.combinations(range(n), 2):          # codegree <= 1
    others = [c for c in range(n) if c not in (a, b)]
    for c, d in itertools.combinations(others, 2):
        cnf.append([-e(a, c), -e(b, c), -e(a, d), -e(b, d)])
# lex SB on N(x) only would need care; leave unbroken (small k)
fd, path = tempfile.mkstemp(suffix='.cnf'); os.close(fd); cnf.to_file(path)
p = subprocess.run(["timeout", str(cap), os.path.expanduser("~/MathDyad/tools/kissat/build/kissat"), "-q", path],
                   capture_output=True, text=True)
out = p.stdout
if "s SATISFIABLE" in out:
    vals = set()
    for line in out.splitlines():
        if line.startswith("v "): vals |= {int(t) for t in line[2:].split() if int(t) > 0}
    E = [ab for ab, i in var.items() if i in vals]
    adj = {v: set() for v in range(n)}
    for a, b in E: adj[a].add(b); adj[b].add(a)
    degs = sorted(len(adj[v]) for v in range(n))
    cod = max(len(adj[a] & adj[b]) for a, b in itertools.combinations(range(n), 2))
    print(f"k={k} n={n}: SAT  edges={len(E)} degrees={degs[0]}..{degs[-1]} (x={len(adj[0])}) max codegree={cod}")
    nx_ = adj[0]
    print("N(x) induced edges:", sorted((a, b) for a, b in E if a in nx_ and b in nx_))
    print("EDGES", E)
elif "s UNSATISFIABLE" in out:
    print(f"k={k} n={n}: UNSAT")
else:
    print(f"k={k} n={n}: UNKNOWN (cap {cap}s)")
os.unlink(path)
