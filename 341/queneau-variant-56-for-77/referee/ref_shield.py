#!/usr/bin/env python3
"""Referee's own recomputation of the mod-49 shield (PROOF.md / Li Lemma 3.1) and of every
cover pair actually usable in Theorem 3, Case r not in Q.  Pure Python sets, all pairs incl. equal ones."""
M = 49
P = {7, 14, 28}; B = {3, 22, 32, 40, 48}; D = {1, 2, 5, 13, 27, 36, 47}; Q = P | B
Z = set(range(M))
def ss(X, Y):   # residue sumset, equal summands INCLUDED when X is Y
    return {(x + y) % M for x in X for y in Y}
ok = True
def check(name, cond):
    global ok
    print(f"{'PASS' if cond else 'FAIL'}  {name}")
    ok &= cond
check("P, B, D pairwise disjoint", not (P & B) and not (P & D) and not (B & D))
cover = ss(B, B) | ss(P, B) | ss(D, B)
check("(cover)  (B+B) u (P+B) u (D+B) == Z/49 \\ Q", cover == Z - Q)
avoid = ss(B, B) | ss(P, B) | ss(D, B) | ss(D, P)
check("(avoid)  Q n ((B+B) u (P+B) u (D+B) u (D+P)) == {}", not (Q & avoid))
check("(avoid) includes doubled B: {2b} n Q == {}", not ({(2*b) % M for b in B} & Q))
check("(PP)     (P+P) n Q == P", ss(P, P) & Q == P)
pairs = sorted((x, y) for x in P for y in P if (x + y) % M in Q)
check(f"(PP) ordered pairs into Q are exactly the diagonal ones: {pairs}", pairs == [(7, 7), (14, 14), (28, 28)])
mixed = sorted({(x + y) % M for x in P for y in P if x != y})
check(f"mixed P+P residues {mixed} all outside Q", not (set(mixed) & Q))
# D+D and the q>=2 claim
print("max D+D (equal allowed) =", max(x + y for x in D for y in D), "; max distinct =",
      max(x + y for x in D for y in D if x != y), "; t > 97 means t >= 98")
# Theorem 3 Case r not in Q: enumerate ALL (x,b) with x in B u D u P, b in B, x+b = r mod 49,
# compute e_x, u_x, c and check: q-u_x-c >= 0 at q=2, other summand on the b-rail and != e_x.
e = {x: x for x in B | D}; e[7] = 7; e[14] = 63; e[28] = 28
# membership of e_x in the seed A (both controllers share A)
A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,56,63,71,81,89,97}
check("every e_x in A", all(v in A for v in e.values()))
worst = None; nr = 0; lines = []
for r in sorted(Z - Q):
    reps = []
    for x in sorted(B | D | P):
        for b in sorted(B):
            if (x + b) % M == r:
                u = e[x] // M; assert e[x] == M*u + x
                c = (x + b) // M; assert x + b == M*c + r and c in (0, 1)
                reps.append((x, b, u, c))
    if not reps:
        check(f"r={r} has a cover pair", False); continue
    nr += 1
    # the proof only needs ONE rep; check every rep anyway for q = 2 (the smallest q)
    for (x, b, u, c) in reps:
        for q in (2, 3, 10):
            t = M*q + r; other = M*(q - u - c) + b
            assert q - u - c >= 0 and other > 0 and other % M == b and e[x] + other == t
            assert other != e[x], (r, x, b, q)
    lines.append(f"r={r:2d}: " + " ".join(f"({x}+{b};u={u},c={c})" for x, b, u, c in reps))
check(f"all {len(Z-Q)} residues r not in Q have >=1 cover pair; all reps valid at q=2,3,10", nr == len(Z - Q))
uses14 = [l for l in lines if "(14+" in l]
print(f"residues whose ONLY representatives use x=14 (u=1): ",
      [l.split(':')[0] for l in lines if all('(14+' in p for p in l.split(': ')[1].split())])
open('shield_cover_pairs.txt', 'w').write("\n".join(lines) + "\n")
print("cover pair table written to shield_cover_pairs.txt")
print("OVERALL", "PASS" if ok else "FAIL")
