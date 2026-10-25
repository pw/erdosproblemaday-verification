"""Re-verify every witness JSON under runs/ with the referee's own incidence (rpg.py)."""
import json, glob, re, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rpg
RUNS = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'runs')
planes = {}
def isprime(n): return n > 1 and all(n % k for k in range(2, int(n ** .5) + 1))
def check(q, raw, label):
    if not isprime(q):
        print(f"{label}: q={q} not prime -> SKIPPED (referee plane is prime-field only)"); return None
    if q not in planes: planes[q] = rpg.plane(q)
    pts, idx, lines, inc = planes[q]
    if not raw:
        print(f"{label}: EMPTY point list -> no witness (not a certificate)"); return None
    normed = [rpg.norm(P, q) for P in raw]
    nonnormal = sum(1 for P, N in zip(raw, normed) if tuple(x % q for x in P) != N)
    S = [idx[N] for N in normed]
    dup = len(S) - len(set(S))
    sp = rpg.spectrum(S, inc)
    blocking = 0 not in sp
    mx = max(sp)
    print(f"{label}: q={q} |S|={len(set(S))} (dups={dup}, non-normal-form inputs={nonnormal}) spectrum={sp} "
          f"blocking={blocking} max={mx}  lines={sum(sp.values())}")
    # three count identities
    v = q * q + q + 1; s = len(set(S))
    assert sum(sp.values()) == v
    assert sum(i * n for i, n in sp.items()) == s * (q + 1)
    assert sum(i * (i - 1) // 2 * n for i, n in sp.items()) == s * (s - 1) // 2
    return sp
for f in sorted(glob.glob(os.path.join(RUNS, '*witness*.json'))):
    m = re.search(r'_q(\d+)_', os.path.basename(f))
    q = int(m.group(1)) if m else None
    d = json.load(open(f))
    if isinstance(d, dict):
        for k, v in d.items(): check(q, v, f"{os.path.basename(f)}[{k}]")
    else:
        check(q, d, os.path.basename(f))
