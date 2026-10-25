#!/usr/bin/env python3
"""Independent cross-check of entire_cert_0indexed + deep large-N gap probes.
Re-implements the greedy base condition from scratch (not via lab.greedy_entire)
and verifies M independently, to catch any bug in the cert function itself."""
from fractions import Fraction
import lab
def F(x): return Fraction(x)

def my_f(t,a,n): return t*(a**(n+1))*(2-a) - Fraction(n)*(a-1) - t

def independent_check(t, a, N_deep):
    """Return dict; 'contradiction' key set if cert says proven but we find a problem."""
    c = lab.entire_cert_0indexed(t, a)
    if not c["proven"]:
        return {"cert": "not-proven"}
    M = c["M"]
    # (a) independently verify M is the SMALLEST n with f(n)>=0
    for n in range(0, M):
        if my_f(t,a,n) >= 0:
            return {"contradiction": "M-not-smallest", "cert_M": M, "earlier": n}
    if my_f(t,a,M) < 0:
        return {"contradiction": "f(M)<0", "M": M}
    # (b) independently verify greedy base: s_k <= 1 + sum_{j<k} s_j for k=0..M, s_0<=1
    terms = lab.floors(t, a, n_terms=M+2, start=0)
    S = 0
    for k in range(0, M+1):
        sk = terms[k]
        if sk > 1 + S:
            return {"contradiction": "greedy-base-fails", "k": k, "sk": sk, "S_prev": S}
        S += sk
    if S < 1:
        return {"contradiction": "C_M<1"}
    # (c) verify f(n)>=0 for a window past M (monotonicity consequence)
    for n in range(M, M+300):
        if my_f(t,a,n) < 0:
            return {"contradiction": "f<0 past M", "n": n}
    # (d) deep empirical gap search
    g = lab.gap_to_N(t, a, N=N_deep, start=0)
    if g["max_gap"] != 0:
        return {"contradiction": "GAP", "N": N_deep, "gap": g}
    return {"ok": True, "M": M, "C_M": S, "fM": float(my_f(t,a,M)), "N": N_deep}

if __name__ == "__main__":
    import sys
    # broad grid, deep N
    alphas = ["1.05","1.2","1.3","1.4","1.5","1.6","1.618","1.7","1.8","1.85","1.88","1.9"]
    ts = ["1","21/20","11/10","6/5","5/4","13/10","7/5","3/2","8/5","9/5"]
    Ndeep = 600000
    nprov = nbad = 0
    thinnest = None
    for als in alphas:
        a = F(als)
        for tts in ts:
            t = F(tts)
            r = independent_check(t, a, Ndeep)
            if r.get("contradiction"):
                nbad += 1
                print(f"!!! CONTRADICTION t={tts} a={als}: {r}")
            elif r.get("ok"):
                nprov += 1
                if thinnest is None or r["fM"] < thinnest[0]:
                    thinnest = (r["fM"], tts, als, r["M"])
    print(f"independent cross-check: proven-ok={nprov} contradictions={nbad} (N={Ndeep})")
    if thinnest:
        print(f"thinnest certified margin f(M)={thinnest[0]:.6f} at t={thinnest[1]} a={thinnest[2]} M={thinnest[3]}")
