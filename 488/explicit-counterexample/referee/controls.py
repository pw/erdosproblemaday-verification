# Brute-force controls for the lemmas of the Gessel #488 construction.
# Positive controls: real parameters (primes<257, band (T,256T], mod 8) for the near-count lemmas;
#   small analogue (primes<17, band (T,16T], mod 4, Q=3*5*7*11*13) for near AND far lemmas.
# Negative controls: break one hypothesis at a time and show the checker reports FAIL.
import numpy as np, sys, random
from math import gcd, prod
random.seed(488)

def primes_upto(N):
    s = np.ones(N+1, bool); s[:2] = False
    for i in range(2, int(N**.5)+1):
        if s[i]: s[i*i::i] = False
    return np.nonzero(s)[0]

GPF_N = 1 << 21
GPF = np.ones(GPF_N+1, np.int64)
for p in primes_upto(GPF_N): GPF[p::p] = p     # increasing p => largest prime factor survives
GPF[0] = 0

def gpf(x):
    if x <= GPF_N: return int(GPF[x])
    g, y, p = 1, x, 2
    while p*p <= y:
        while y % p == 0: g, y = p, y//p
        p += 1
    return max(g, y) if y > 1 else g

def v2(a): return (a & -a).bit_length()-1

def band(T, pb, mult):           # P-smooth (all primes < pb) in (T, mult*T]
    xs = np.arange(T+1, mult*T+1); return xs[GPF[xs] < pb]

def multiples(A, x):             # covered integers in [1, x]
    cov = np.zeros(x+1, bool)
    for a in A: cov[a::a] = True
    return cov

def near_check(T, pb, mult, resmod):
    A = band(T, pb, mult); n = mult*T
    cov = multiples(A, n)
    ok_i = np.array_equal(np.nonzero(cov)[0], A)
    xs = np.arange(1, n+1); oddS = int(np.count_nonzero((xs % 2 == 1) & (GPF[xs] < pb)))
    ok_ii = len(A) <= resmod*oddS
    keys = {(int(a) >> v2(int(a)), v2(int(a)) % resmod) for a in A}
    ok_inj = len(keys) == len(A)
    return ok_i, ok_ii, ok_inj, len(A), oddS

def report(name, rows, expect_all_true):
    bad = [r for r in rows if not all(r[1])]
    status = ("PASS" if not bad else "FAIL") if expect_all_true else ("FAIL-as-expected" if bad else "UNEXPECTED-PASS")
    print(f"[{name}] {status}: {len(rows)} cases, {len(bad)} with a failed check", end="")
    if bad: print(f"; first failing T={bad[0][0]} checks(i,ii,inj)={bad[0][1]}", end="")
    print()
    return bad

print("== POSITIVE: real parameters, primes<257, band (T,256T], n=256T, residues mod 8 ==")
Ts = list(range(1, 65)) + [256] + random.sample(range(65, 4097), 40) + [4096]
rows = []
for T in Ts:
    i, ii, inj, a, h1 = near_check(T, 257, 256, 8); rows.append((T, (i, ii, inj), a, h1))
report("near lemmas, real P", rows, True)
mx = max(rows, key=lambda r: r[2]/(8*r[3]))
print(f"   tightest |band|/(8*H): T={mx[0]} |band|={mx[2]} 8*oddsmooth={8*mx[3]} ratio={mx[2]/(8*mx[3]):.4f}")
for T in (1, 256, 4096):
    r = [x for x in rows if x[0] == T][0]; print(f"   T={T}: |A|={r[2]}, #oddS<=256T={r[3]}")

print("== POSITIVE: real parameters, far-injection with truncated R (r<20000 coprime to Q, INCLUDING even r) ==")
P = [int(p) for p in primes_upto(256)]; S = [p for p in P if p != 2]; Q = prod(S)
Rtr = [r for r in range(1, 20000) if gcd(r, Q) == 1]
print(f"   |R_trunc|={len(Rtr)}, even members={sum(1 for r in Rtr if r%2==0)}, e.g. {Rtr[:8]}")
far_rows = []
for T in [1, 7, 64, 256, 1000, 4096]:
    D = [d for d in range(1, T+1, 2) if gpf(d) < 257]
    seen, ok_land, coll = set(), True, 0
    for d in D:
        e = 0
        while (d << e) <= T: e += 1
        c = d << e
        if not (T < c <= 2*T and gpf(c) < 257): ok_land = False
        for r in Rtr:
            v = c*r
            if v in seen: coll += 1
            seen.add(v)
    far_rows.append((T, (ok_land, coll == 0, True)))
    print(f"   T={T}: h={len(D)} pairs={len(D)*len(Rtr)} c_d in band: {ok_land}  collisions={coll}")
report("far injection, real P (truncated R)", far_rows, True)

print("== POSITIVE: small analogue, primes<17, band (T,16T], n=16T, mod 4, m=2TQs, Qs=15015 ==")
Ps = [2,3,5,7,11,13]; Ss = Ps[1:]; Qs = prod(Ss); phis = prod(p-1 for p in Ss)
Rs = [r for r in range(Qs) if gcd(r, Qs) == 1]; assert len(Rs) == phis
print(f"   Qs={Qs} phi={phis} phi/Q={phis/Qs:.4f}; (32/3)... analogue bound needs 4*b*ratio < 2^b*phi/Q, b=4 cannot succeed")
def far_check(T, pb, Ss, Qs, Rs, mode="ok"):
    A = band(T, pb, 16); m = 2*T*Qs
    cov = multiples(A, m); Mm = int(cov[1:].sum())
    if mode == "evend":   # NEG: allow even d (P-smooth d) -> injectivity must fail
        D = [d for d in range(1, T+1) if gpf(d) < pb]
    else:
        D = [d for d in range(1, T+1, 2) if gpf(d) < pb]
    R = list(range(1, Qs)) if mode == "allr" else Rs
    seen = set(); coll = 0; land = True; inband = True
    for d in D:
        e = 0
        while (d << e) <= T: e += 1
        c = d << e
        if mode == "cbelow": c >>= 1          # NEG: c_d in (T/2, T], not in the band
        if not (T < c <= 16*T and gpf(c) < pb): inband = False
        for r in R:
            v = c*r
            if v > m or not cov[v]: land = False
            if v in seen: coll += 1
            seen.add(v)
    return (land, coll == 0, Mm >= len(D)*len(R)), len(D), Mm, len(A), m
rows = []
for T in list(range(1, 41)) + [64, 100, 256]:
    ok, h, Mm, a, m = far_check(T, 17, Ss, Qs, Rs)
    i, ii, inj, _, _ = near_check(T, 17, 16, 4)
    rows.append((T, (i, ii, inj) + ok, h, Mm, a, m))
report("small analogue near+far (i, ii, inj, land, far-inj, M(m)>=h*phi)", rows, True)
for r in rows:
    if r[0] in (1, 16, 64, 256):
        T, _, h, Mm, a, m = r; n = 16*T
        print(f"   T={T}: |A|={a} h={h} M(m)={Mm} >= h*phi={h*phis}; density ratio (M(m)/m)/(M(n)/n)={(Mm/m)/(a/n):.3f}"
              f"  [2mM(n) < nM(m)? {2*m*a < n*Mm}]")

print("== NEGATIVE controls (each breaks one hypothesis; checker must report failures) ==")
def percheck(rows):
    k = len(rows[0][1]); return [sum(1 for r in rows if not r[1][j]) for j in range(k)]
# N1: band ratio 18 (cofactor 17 possible); residues mod 5 so ONLY check (i) is stressed (2^5 > 18)
rows = [(T, near_check(T, 17, 18, 5)[:3]) for T in range(1, 200)]
bad = report("N1 band (T,18T] with primes<17, mod 5: cofactor 17 can appear", rows, False)
print("   failures per check (i, ii, inj):", percheck(rows))
Tf = next(r[0] for r in rows if not r[1][0])
A = band(Tf, 17, 18); cov = multiples(A, 18*Tf); extra = sorted(set(np.nonzero(cov)[0].tolist()) - set(A.tolist()))[:5]
print(f"   first T failing (i): T={Tf}; covered-but-not-in-band {extra} (gpf {[gpf(int(x)) for x in extra]})")
# N1': real P, band ratio 258 (cofactor 257 possible); residues mod 9 so only (i) is stressed (2^9 > 258)
rows = [(T, near_check(T, 257, 258, 9)[:3]) for T in list(range(1, 40)) + [255, 256, 257, 300, 1000]]
bad = report("N1' real P, band (T,258T], mod 9: cofactor 257 can appear", rows, False)
print("   failures per check (i, ii, inj):", percheck(rows))
fl = [r[0] for r in rows if not r[1][0]]
if fl:
    Tf = fl[0]; A = band(Tf, 257, 258); cov = multiples(A, 258*Tf); extra = sorted(set(np.nonzero(cov)[0].tolist()) - set(A.tolist()))[:3]
    print(f"   T failing (i): {fl}; witness at T={Tf}: {extra} gpf {[gpf(int(x)) for x in extra]}")
rows = [(T, near_check(T, 17, 16, 3)[:3]) for T in range(1, 200)]
bad = report("N2 residues mod 3 instead of mod 4 (base 16=2^4)", rows, False)
print("   failures per check (i, ii, inj):", percheck(rows))
T = 1; A = band(T, 17, 16); keys = {}
for a in A.tolist():
    key = (a >> v2(a), v2(a) % 3)
    if key in keys: print(f"   collision at T=1: {keys[key]} and {a} both map to (d, e mod 3) = {key}"); break
    keys[key] = a
for mode, label in (("allr", "N3 far map with r over ALL of [1,Q) (drop coprimality)"),
                    ("evend", "N4 far map with even d allowed (drop d odd)"),
                    ("cbelow", "N5 far map with c_d in (T/2,T] (not in band)")):
    rows = []
    for T in (5, 12, 33):
        ok, *_ = far_check(T, 17, Ss, Qs, Rs, mode)
        rows.append((T, ok))
    report(label + " -> (land, inj, count)", rows, False)
    print("   per-T (land, inj, count):", [(t, ok) for t, ok in rows])
