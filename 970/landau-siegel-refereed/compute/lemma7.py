"""Seat C: build the paper's Section-4 determinant exactly and test Lemma 7 (v_p(Delta) >= E_p at admissible p).
usage: lemma7.py d N H [variant=paper] [tiebreak=lex] [certify=1] [out.json]
variants: paper (theta, sigma theta, sigmatau theta) | swap (theta, sigmatau, sigma) | wrong2 (slot2 = sigma theta + 1)
          | tau (slot2 = tau theta: WRONG conjugate) | permslot2 (slot2 = sigma(theta_{pi(n)}): points perturbed)
"""
import sys, json, math, cmath, time, itertools
import numpy as np
import flint
sys.set_int_max_str_digits(0)
from sympy import primerange, isprime
sys.path.insert(0, '/tmp/oaimath/003/seats/C_work')
from biq import *

d, N, H = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
variant = sys.argv[4] if len(sys.argv) > 4 else 'paper'
tiebreak = sys.argv[5] if len(sys.argv) > 5 else 'lex'
certify = int(sys.argv[6]) if len(sys.argv) > 6 else 1
outpath = sys.argv[7] if len(sys.argv) > 7 else None
T0 = time.time()
M = N**4
U = M ** (1/3)
pts = list(itertools.product(range(N), repeat=4))            # fixed column order (lexicographic n)
theta = [tuple(n) for n in pts]                              # theta_n = n1 + n2 a + n3 b + n4 ab
# the three coordinates per column
if variant == 'paper':   X = [(t, sig(t), sigtau(t)) for t in theta]
elif variant == 'swap':  X = [(t, sigtau(t), sig(t)) for t in theta]
elif variant == 'wrong2': X = [(t, add(sig(t), ONE), sigtau(t)) for t in theta]
elif variant == 'tau':   X = [(t, tau(t), sigtau(t)) for t in theta]
elif variant == 'permslot2':
    idx = {n: i for i, n in enumerate(pts)}
    def pi(n): return (n[0], (n[1]+1) % N, n[2], n[3])
    X = [(theta[i], sig(theta[idx[pi(n)]]), sigtau(theta[i])) for i, n in enumerate(pts)]
else: raise ValueError(variant)

def w(al): return al[0] + H*al[1] + H*al[2]
def candidates():
    W = 0
    while True:
        group = []
        for s in range(W // H + 1):
            a1 = W - H*s
            for a2 in range(s+1):
                group.append((a1, a2, s-a2))
        if tiebreak == 'lex':    group.sort(key=lambda al: (al[1], al[2]))      # alpha1 desc, then alpha2 asc
        elif tiebreak == 'rev':  group.sort(key=lambda al: (-al[1], -al[2]))    # alpha1 asc
        else: raise ValueError(tiebreak)
        for al in group: yield al
        W += 1

# ---------- greedy over K, decided mod three independent split primes (one prime of K above each) ----------
def greedy_modp(p, s, t, maxcand=10**6):
    vals = [[embed(c, p, s, t) for c in X[i]] for i in range(M)]
    pw = {}
    def pw_row(j, k):
        key = (j, k)
        if key not in pw:
            pw[key] = np.array([pow(vals[i][j], k, p) for i in range(M)], dtype=np.int64)
        return pw[key]
    basis = []  # (pivot, row) with row[pivot]=1
    retained, order = [], []
    for c, al in enumerate(candidates()):
        if c > maxcand: raise RuntimeError('too many candidates')
        v = pw_row(0, al[0]) * pw_row(1, al[1]) % p * pw_row(2, al[2]) % p
        for piv, row in basis:
            if v[piv]: v = (v - v[piv] * row) % p
        order.append(al)
        nz = np.nonzero(v)[0]
        if len(nz):
            piv = int(nz[0]); inv = pow(int(v[piv]), p-2, p)
            basis.append((piv, v * inv % p)); retained.append(al)
            if len(retained) == M: break
    return retained, order

gprimes = split_primes(d, nbits=31, count=3, seed=7 + abs(d))
results = [greedy_modp(*pr) for pr in gprimes]
P, order = results[0]
agree = all(r[0] == P for r in results)
print(f'd={d} N={N} H={H} variant={variant} tb={tiebreak}: M={M}, candidates scanned={len(order)}, '
      f'greedy agree across 3 primes: {agree}  [{time.time()-T0:.1f}s]', flush=True)
assert agree, 'mod-p greedy disagreement'

# ---------- exact rows over R ----------
powcache = {}
def xpow(i, j, k):
    key = (i, j, k)
    if key not in powcache:
        powcache[key] = ONE if k == 0 else (X[i][j] if k == 1 else mul(xpow(i, j, k-1), X[i][j], d))
    return powcache[key]
def row_exact(al):
    return [mul(mul(xpow(i, 0, al[0]), xpow(i, 1, al[1]), d), xpow(i, 2, al[2]), d) for i in range(M)]

BASIS = [ONE, (0, 1, 0, 0), (0, 0, 1, 0), (0, 0, 0, 1)]
def regrep(row):
    """Q-span of {e*row : e in Z-basis of R} as 4 integer vectors of length 4M; Q-rank = 4 * K-rank."""
    out = []
    for e in BASIS:
        v = []
        for x in row: v.extend(mul(e, x, d))
        out.append(v)
    return out

cert = None
if certify:
    # every skipped candidate must lie in the K-span of the retained rows before it: one exact rank per gap
    Pset = set(P); cert_ok = True; ngaps = 0
    retained_so_far = []
    gap = []
    for al in order:
        if al in Pset:
            if gap:
                rows = []
                for r in retained_so_far: rows += regrep(row_exact(r))
                for g in gap: rows += regrep(row_exact(g))
                rk = flint.fmpz_mat(rows).rank()
                if rk != 4*len(retained_so_far): cert_ok = False; print('CERT FAIL at gap before', al, rk)
                ngaps += 1; gap = []
            retained_so_far.append(al)
        else:
            gap.append(al)
    assert not gap
    cert = cert_ok
    print(f'exact Q-rank certification of every skipped row: {cert_ok} ({ngaps} gaps) [{time.time()-T0:.1f}s]', flush=True)

rows = [row_exact(al) for al in P]

# ---------- Delta by multimodular CRT over R ----------
def logabs_embed(x, e1, e2):
    a = cmath.sqrt(d); b = math.sqrt(2)
    z = x[0] + x[1]*e1*a + x[2]*e2*b + x[3]*e1*e2*a*b
    return -math.inf if abs(z) == 0 else math.log(abs(z))
logB = -math.inf
for e1 in (1, -1):
    for e2 in (1, -1):
        L = [[logabs_embed(X[i][j], e1, e2) for j in range(3)] for i in range(M)]
        tot = 0.0
        for al in P:
            ls = []
            for i in range(M):
                l = 0.0
                for j in range(3):
                    if al[j]: l += al[j] * L[i][j]
                ls.append(l)
            mx = max(ls)
            tot += mx + 0.5*math.log(sum(math.exp(2*(l - mx)) for l in ls if l > -math.inf))
        logB = max(logB, tot)
bits_needed = logB / math.log(2) + 64
cprimes = split_primes(d, nbits=62, count=int(bits_needed // 61) + 3, seed=1000 + abs(d))
def det_conj_modp(p, s, t):
    out = {}
    for e1 in (1, -1):
        for e2 in (1, -1):
            Mx = flint.nmod_mat([[embed(x, p, s, t, e1, e2) for x in r] for r in rows], p)
            out[(e1, e2)] = int(Mx.det())
    return out
residues = []
for (p, s, t) in cprimes:
    c = det_conj_modp(p, s, t)
    inv4 = pow(4, p-2, p)
    z1 = sum(c.values()) * inv4 % p
    z2 = (c[(1,1)] + c[(1,-1)] - c[(-1,1)] - c[(-1,-1)]) * inv4 * pow(s, p-2, p) % p
    z3 = (c[(1,1)] - c[(1,-1)] + c[(-1,1)] - c[(-1,-1)]) * inv4 * pow(t, p-2, p) % p
    z4 = (c[(1,1)] - c[(1,-1)] - c[(-1,1)] + c[(-1,-1)]) * inv4 * pow(s*t % p, p-2, p) % p
    residues.append((p, (z1, z2, z3, z4)))
def crt(res):
    Mod = 1; vals = [0, 0, 0, 0]
    for p, z in res:
        for k in range(4):
            # combine vals[k] mod Mod with z[k] mod p
            x = vals[k]; y = z[k]
            tt = ((y - x) * pow(Mod, -1, p)) % p
            vals[k] = x + Mod * tt
        Mod *= p
    return tuple(v - Mod if v > Mod // 2 else v for v in vals), Mod
Delta, Mod = crt(residues)
Delta_less, _ = crt(residues[:-2])
stable = (Delta == Delta_less)
# independent check at a fresh prime
fp, fs, ft = split_primes(d, nbits=62, count=1, seed=99999 + abs(d))[0]
c = det_conj_modp(fp, fs, ft)
fresh_ok = all(embed(Delta, fp, fs, ft, e1, e2) == c[(e1, e2)] for e1 in (1, -1) for e2 in (1, -1))
print(f'Delta via CRT: {len(cprimes)} primes, log2 Hadamard bound {logB/math.log(2):.0f}, stable={stable}, '
      f'fresh-prime check={fresh_ok}, nonzero={Delta != ZERO} [{time.time()-T0:.1f}s]', flush=True)
assert stable and fresh_ok and Delta != ZERO

# ---------- norm ----------
NmD = norm(Delta, d)
# ---------- valuations ----------
S1 = sum(al[0] for al in P); S2 = sum(al[1] + al[2] for al in P)
amax = [max(al[j] for al in P) for j in range(3)]
pmax = max(max(amax) + 12, 30)
table = []
for p in primerange(2, pmax + 1):
    cl = frob_class(p, d)
    adm = (p > H and cl in ('sigma', 'sigtau'))
    Ep = sum(al[0] // p for al in P)
    E2 = sum(al[1] // p for al in P); E3 = sum(al[2] // p for al in P)
    v = vp_R(Delta, p)
    vN = vp_int(NmD, p)
    # extended prediction from the SAME argument (my derivation; valid only for variant paper/swap/wrong2):
    c1 = {'id': 1, 'sigma': int(p > H), 'sigtau': int(p > H), 'tau': 0}.get(cl, 0)
    c2 = {'id': 1, 'sigma': 1, 'sigtau': 0, 'tau': 1}.get(cl, 0)
    c3 = {'id': 1, 'sigma': 0, 'sigtau': 1, 'tau': 1}.get(cl, 0)
    Lext = sum(c1*(al[0]//p) + c2*(al[1]//p) + c3*(al[2]//p) for al in P)
    table.append(dict(p=p, cls=cl, adm=adm, Ep=Ep, E2=E2, E3=E3, Lext=Lext, vp=v if v != math.inf else 'inf',
                      vpNm=vN if vN != math.inf else 'inf', holds=(v >= Ep), ext_holds=(v >= Lext),
                      norm_holds=(vN >= 4*Ep)))
adm_rows = [r for r in table if r['adm']]
viol_adm = [r for r in adm_rows if not r['holds']]
print(f'S1={S1} S2={S2} amax={amax} maxweight={max(w(al) for al in P)}  M={M} U={U:.3f}')
print(f'{"p":>4} {"class":>7} {"adm":>4} {"E_p":>5} {"v_p":>5} {"Lext":>5} {"v_p(Nm)":>8}  E_p<=v_p')
for r in table:
    if r['Ep'] or r['Lext'] or (r['vp'] not in (0,)):
        print(f"{r['p']:>4} {r['cls']:>7} {str(r['adm'])[0]:>4} {r['Ep']:>5} {str(r['vp']):>5} {r['Lext']:>5} {str(r['vpNm']):>8}  {r['holds']}"
              + ('' if r['ext_holds'] else '   (ext-pred FAILS)'))
print(f'ADMISSIBLE primes with E_p>0: {sum(1 for r in adm_rows if r["Ep"]>0)}; violations of Lemma 7: {len(viol_adm)}')
prod_ok = all(NmD % (r['p']**(4*r['Ep'])) == 0 for r in adm_rows)
print(f'Nm(Delta) nonzero integer: {NmD != 0}; log10|Nm|={math.log10(abs(NmD)):.1f}; prod over admissible p^(4E_p) | Nm: {prod_ok}')
# size bound (5.3) check, base-e logs
maxnu = max(abs(complex(x[0] + x[1]*e1*cmath.sqrt(d) + x[2]*e2*math.sqrt(2) + x[3]*e1*e2*cmath.sqrt(d)*math.sqrt(2)))
            for i in range(M) for x in X[i] for e1 in (1, -1) for e2 in (1, -1))
upper_53_ours = 0.5*M*math.log(M) + (S1 + S2) * math.log(maxnu) if maxnu > 0 else None
lhs = 0.25 * math.log(abs(NmD))
print(f'(1/4)log|Nm Delta| = {lhs:.2f};  Hadamard with actual max|nu x| ({maxnu:.3f}): {upper_53_ours:.2f};  '
      f'sum_adm E_p log p = {sum(r["Ep"]*math.log(r["p"]) for r in adm_rows):.2f};  '
      f'sum_all Lext log p = {sum(r["Lext"]*math.log(r["p"]) for r in table if r["cls"]!="ram"):.2f}')
print(f'[{time.time()-T0:.1f}s]')
if outpath:
    json.dump(dict(d=d, N=N, H=H, variant=variant, tiebreak=tiebreak, M=M, U=U, P=P, ncand=len(order),
                   greedy_agree=agree, exact_cert=cert, Delta=[str(z) for z in Delta], NmD=str(NmD), S1=S1, S2=S2,
                   amax=amax, maxweight=max(w(al) for al in P), table=table, viol_adm=len(viol_adm),
                   prod_ok=prod_ok, quarter_log_Nm=lhs, hadamard=upper_53_ours), open(outpath, 'w'), indent=1)
