#!/usr/bin/env python3
"""Write certs.json: for t=2..14 the K_{2,t} instance (A, A+, x) with exact minima and a witness cover of that size.
Lower bound = LEMMA.md (proof) + exact.py (computation); witness = upper bound, checkable by one product mod."""
import json
from math import prod
from k2t2 import choose_primes, placement
from exact import solve
out = []
for t in range(2, 15):
    ws, qu, qv = choose_primes(t)
    M, m, k, u, x = placement(ws, qu, qv)
    A = sorted([w * qu for w in ws] + [w * qv for w in ws]); Ap = sorted(A + [qu])
    g, wit = solve(A, x); gp, witp = solve(Ap, x)
    # independent re-check of the witnesses (plain arithmetic)
    for S, AA, gg in ((wit, A, g), (witp, Ap, gp)):
        assert len(set(S)) == gg and all(x < b <= x + m for b in S) and prod(S) % prod(AA) == 0
    # facts F2/F3 scanned directly on the window
    D = ws + [qu, qv]
    two = [b for b in range(x + 1, x + m + 1) if sum(b % p == 0 for p in D) >= 2]
    sq = [b for b in range(x + 1, x + m + 1) if b % (qu * qu) == 0 or b % (qv * qv) == 0]
    assert two == [u] and sq == []
    out.append(dict(t=t, w=ws, q_u=qu, q_v=qv, m=m, k=k, u=str(u), x=str(x), n=2 * t, A=A, min_B=g, witness=[str(b) for b in wit],
                    n_plus=2 * t + 1, A_plus=Ap, min_B_plus=gp, witness_plus=[str(b) for b in witp]))
    print(t, 2 * t, g, 2 * t + 1, gp, 'F2/F3 scan ok', flush=True)
json.dump(out, open('certs.json', 'w'), indent=1)
