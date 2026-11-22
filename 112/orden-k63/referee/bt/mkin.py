"""Generate backtracker inputs. Usage: mkin.py n k out in fixI(0/1) [maxsol]
vertex 0 gets out-neighbours 1..out, in-neighbours out+1..out+in, non-neighbours the rest (I).
If fixI, the 8 vertices of I (must be exactly 8) carry Bermond's graph on Z8 (x->x+1, x->x-2)."""
import sys
n, k, o, i, fixI = map(int, sys.argv[1:6]); maxsol = int(sys.argv[6]) if len(sys.argv) > 6 else 0
L = [f"{n} {k} {maxsol}"]
P = range(1, 1 + o); Q = range(1 + o, 1 + o + i); I = list(range(1 + o + i, n))
L += [f"A 0 {p}" for p in P] + [f"A {q} 0" for q in Q] + [f"N 0 {r}" for r in I]
if fixI:
    assert len(I) == 8
    arcs = {(x, (x + 1) % 8) for x in range(8)} | {(x, (x - 2) % 8) for x in range(8)}
    for a in range(8):
        for b in range(a + 1, 8):
            if (a, b) in arcs: L.append(f"A {I[a]} {I[b]}")
            elif (b, a) in arcs: L.append(f"A {I[b]} {I[a]}")
            else: L.append(f"N {I[a]} {I[b]}")
L.append("E")
print("\n".join(L))
