"""Finite model of Section 5 (05-dichotomy.tex) of the OpenAI vdW preprint.

Keeps the paper's FORMULAS for D, M, h0, H, eta, lambda, H_x, alpha, the U mesh and the adaptive V mesh,
the coordinates x_i(n)=n/q^i, y_i=lambda*x_i, the centered representatives, labels, light/heavy.
Only q is chosen freely (a prime > k, coprime to lambda, large enough that labels actually repeat).

For every generated cyclic progression n_j = n0 + j d in Z/q^D Z it checks, EXACTLY (integer arithmetic over the
common denominator Q=q^D), every conclusion of Lemmas dichotomy:drift, dichotomy:path, dichotomy:heavy-width and
of Theorem dichotomy:main's short-period case (alternative (ii) for all j) and, when all of the paper's large-k
inequalities hold for this k, the longer-period block-eligibility claims (Definition count:eligible (i)-(iii),
>= h/2 regular positions, coverage >= 4k/5).

Controls (flags): --lam1 (drop dilation), --alpha 0.1 (alpha far above q^-D), --uniformV (no refinement at the cut),
--vscale X (feed X*v to the eligibility (iii) checker).
Usage: python3 toy_model.py MODEL NPROG SEED [flags]   MODEL in {A,B,C}
"""
import sys, random, math
from math import gcd
import mpmath
mpmath.mp.dps = 120

def ceil_root(k, r):
    lo, hi = 1, 2
    while hi**r < k: hi *= 2
    while lo < hi:
        mid = (lo+hi)//2
        if mid**r >= k: hi = mid
        else: lo = mid+1
    return lo

def primes_upto(n):
    return [p for p in range(2, n+1) if all(p % d for d in range(2, int(p**0.5)+1))]

MODELS = {  # k, q (prime)
    'A': (12, 10000019),
    'B': (100, 10000000019),
    'C': (1056, 100000000000000003),
}

class Model:
    def __init__(s, k, q, lam1=False, alpha=None, uniformV=False):
        s.k = k; s.q = q
        s.D = ceil_root(k, 10); s.M = ceil_root(k, 2); s.h0 = s.D**2
        # paper formulas (H = k^-2, eta = 1/(1000 D), delta = 1/10)
        s.Hden = k*k                     # H = 1/Hden
        s.etaden = 1000*s.D              # eta = 1/etaden
        lam = 1
        for l in primes_upto(s.h0):
            a = 0
            while l**(a+1) <= 2*s.M: a += 1
            lam *= l**a
        s.lam = 1 if lam1 else lam
        s.lam_true = lam
        assert gcd(s.lam, q) == 1 and q > k
        s.Q = q**s.D; s.N = s.Q
        s.Hxden = s.Hden*s.lam           # H_x = 1/(k^2 lambda)
        s.alpha = mpmath.mpf(1)/mpmath.mpf(q)**(s.D+1) if alpha is None else mpmath.mpf(alpha)
        s.uniformV = uniformV
        s.R = mpmath.log(1 + 1/(2*s.alpha))
        s.m = int(mpmath.ceil(k*k*s.R))
        s.theta = s.R/s.m
        s.Rf = float(s.R); s.alphaf = float(s.alpha); s.thetaf = float(s.theta)
        s.lam_inv = pow(s.lam, -1, s.Q)
        s.mesh_fallbacks = 0
    # ---- representatives (numerators over Q) ----
    def xnum(s, n):   # xhat_i(n) * Q, in [0,Q)
        return [ (n % s.q**i) * s.q**(s.D-i) for i in range(1, s.D+1) ]
    def ynum(s, n):   # ytilde_i(n) * Q, in [-Q/2, Q/2)
        out = []
        for i in range(1, s.D+1):
            Qi = s.q**i
            r = (s.lam*n) % Qi
            if 2*r >= Qi: r -= Qi
            out.append(r * s.q**(s.D-i))
        return out
    # ---- labels ----
    def Ulab(s, X):   # floor(xhat / H_x)
        return (X * s.Hxden) // s.Q
    def phi(s, a_num, a_den):  # (m/R) log(1 + a/alpha), with exact fallback near integers
        a = a_num / a_den
        v = s.m * math.log1p(a / s.alphaf) / s.Rf
        if abs(v - round(v)) < 1e-5:
            s.mesh_fallbacks += 1
            am = mpmath.mpf(a_num)/mpmath.mpf(a_den)
            return mpmath.mpf(s.m)*mpmath.log1p(am/s.alpha)/s.R, True
        return v, False
    def Vlab(s, Y):   # Y = ytilde*Q in [-Q/2,Q/2)
        if s.uniformV:  # control: uniform mesh of width 1/(k^2) = H on [-1/2,1/2)
            return ('U', ((2*Y + s.Q) * s.Hden) // (2*s.Q))
        if Y < 0:      # left half: a = ytilde + 1/2 in [0,1/2); a_l <= a < a_{l+1}
            v, ex = s.phi(2*Y + s.Q, 2*s.Q)
            l = int(mpmath.floor(v)) if ex else math.floor(v)
            return ('L', l)
        else:          # right half: b = 1/2 - ytilde in (0,1/2]; a_l < b <= a_{l+1}
            v, ex = s.phi(s.Q - 2*Y, 2*s.Q)
            l = (int(mpmath.ceil(v)) if ex else math.ceil(v)) - 1
            return ('R', l)
    def Vwidth(s, lab):  # |I| as float
        if s.uniformV: return 1.0/s.Hden
        l = lab[1]
        return s.alphaf * math.exp(l*s.thetaf) * math.expm1(s.thetaf)
    def labels(s, ns):
        XS = [s.xnum(n) for n in ns]; YS = [s.ynum(n) for n in ns]
        L = [tuple(s.Ulab(X) for X in XS[j]) + tuple(s.Vlab(Y) for Y in YS[j]) for j in range(len(ns))]
        return XS, YS, L

def centered(r, Qi):
    r %= Qi
    return r - Qi if 2*r >= Qi else r

MINS = {}
FAMILIES = ['small', 'rat', 'rat', 'rat', 'digit', 'rand', 'laminv']

def run(model, nprog, seed, vscale=1):
    s = model; k, D, M, Q, q, lam = s.k, s.D, s.M, s.Q, s.q, s.lam
    rng = random.Random(seed)
    C = dict()
    def bump(key, ok=True):
        C.setdefault(key, [0, 0]); C[key][0] += 1
        if not ok: C[key][1] += 1
    fails = []
    # does this k satisfy every large-k inequality of the longer-period case? (see thresholds.py)
    longer_ok = (s.D >= 3 and 32*M <= k and 20*M <= k and 4*M <= k)
    def gen():
        fam = rng.choice(FAMILIES)
        if fam == 'small':
            d = rng.randint(1, 60) * rng.choice([1, -1])
        elif fam == 'rat':
            h = rng.randint(1, 2*M); j = rng.randrange(h)
            while True:
                e = rng.randint(-60*h, 60*h)
                if e != 0 and (j*Q + e) % h == 0: break
            d = (j*Q + e)//h
        elif fam == 'ratsmall':   # rational step t/h with a tiny drift: heavy labels with long periods
            h = rng.randint(s.h0 + 1, max(s.h0 + 1, k // (k // M + 1)))
            j = rng.randrange(1, h)
            while True:
                e = rng.randint(-2*h, 2*h)
                if e != 0 and (j*Q + e) % h == 0: break
            d = (j*Q + e)//h
        elif fam == 'digit':
            a = rng.randint(1, D-1) if D > 1 else 0
            d = rng.randint(1, 60) * q**a
        elif fam == 'laminv':
            d = s.lam_inv * rng.randint(1, 60)
        else:
            d = rng.randrange(1, Q)
        d %= Q
        if d == 0: d = 1
        # n0: random, or engineered so that some coordinate passes near its cut at some index jc
        if rng.random() < 0.35:
            n0 = rng.randrange(Q); where = 'rand'
        else:
            i = rng.randint(1, D); Qi = q**i; jc = rng.randrange(k)
            off = rng.choice([rng.randint(-3, 3), rng.randint(-10**3, 10**3), rng.randint(-10**6, 10**6),
                              rng.choice([1, -1]) * rng.randint(1, 9) * 10**rng.randint(0, max(0, len(str(Qi)) - 2))])
            target = ((Qi - 1)//2 - off) % Qi
            nt = (pow(s.lam, -1, Qi) * target) % Qi + Qi * rng.randrange(Q // Qi)
            n0 = (nt - jc*d) % Q; where = f'cut{i}'
        return n0, d, fam, where
    for it in range(nprog):
        n0, d, fam, where = gen()
        ns = [(n0 + j*d) % Q for j in range(k)]
        XS, YS, L = s.labels(ns)
        mult = {}
        for lab in L: mult[lab] = mult.get(lab, 0) + 1
        heavy = {lab for lab, c in mult.items() if c*M > k}
        nlight = sum(1 for lab in L if lab not in heavy)
        bump('progressions')
        # ---- independent check of the core cut claim (needs no heavy label):
        # if every centred y-step w_i = ytilde(y_i(d)) has k|w_i| < 1/2 and the sampled representatives are NOT affine,
        # the paper's argument says all full labels are distinct.
        wv = []
        for i in range(1, D+1):
            Qi = q**i
            wv.append(centered(s.lam*d, Qi) * q**(D-i))
        small = all(2*k*abs(w) < Q for w in wv)
        affine = all(YS[j][i] - YS[0][i] == j*wv[i] for j in range(k) for i in range(D))
        if small and not affine:
            ok = len(mult) == k
            bump('cut-crossing small-step progressions: all labels distinct', ok)
            if not ok: fails.append(('cutclaim', n0, d, fam, where))
        if 10*nlight >= k:
            bump('case (i): >= delta k light (nothing to check without c_*)')
            continue
        bump('heavy case (< delta k light)')
        for lab in heavy:   # the paper says "choose a heavy label": test EVERY choice
            J = [j for j in range(k) if L[j] == lab]; ms = len(J)
            gaps = [(J[a+1]-J[a], J[a]) for a in range(ms-1)]
            h, jp = min(gaps)
            # drift lemma
            u = [XS[jp+h][i] - XS[jp][i] for i in range(D)]   # over Q
            v = [YS[jp+h][i] - YS[jp][i] for i in range(D)]
            bump('drift: 1<=h<=2M', 1 <= h <= 2*M)
            # |u_i| <= H_x/(m*-1) <= 2 M H_x / k ; |v_i| <= 2H/(m*-1) <= 4 M H / k   (exact, over Q)
            okb = all(abs(u[i])*s.Hxden*(ms-1) <= Q and (ms-1)*2*M >= k for i in range(D)) and \
                  all(abs(v[i])*s.Hden*(ms-1) <= 2*Q for i in range(D))
            bump('drift: |u_i|,|v_i| bounds', okb)
            bump('drift: v == lambda u (real)', all(v[i] == lam*u[i] for i in range(D)))
            # path lemma: t' = h xhat(d) - u integral, t = t' mod h
            Xd = s.xnum(d)
            tp = []
            okint = True
            for i in range(D):
                num = h*Xd[i] - u[i]
                okint &= (num % Q == 0); tp.append(num // Q)
            bump('path: t\' integral', okint)
            t = [x % h for x in tp]
            okp = True
            for j in range(k):
                for i in range(D):
                    # h*(xhat_j - xhat_0) - j*(t Q + u) == 0 mod hQ   (x-path)
                    if (h*(XS[j][i] - XS[0][i]) - j*(t[i]*Q + u[i])) % (h*Q): okp = False
                    if (h*(YS[j][i] - YS[0][i]) - j*(lam*t[i]*Q + v[i])) % (h*Q): okp = False
            bump('path: both path equations, all j', okp)
            g = h
            for x in t: g = gcd(g, x)
            bump('path: gcd(t,h)=1', g == 1)
            okr = all((J2[0] - J2[-1]) % h == 0 and all((a - J2[0]) % h == 0 for a in J2)
                      for J2 in ([j for j in range(k) if L[j] == lb] for lb in mult))
            bump('path: each label in one residue class mod h', okr)
            # heavy-width at every heavy index, every coordinate (|v_i| <= (2M/k)|V(y_i(n_j*))|)
            okw = True
            for js in range(k):
                if L[js] in heavy:
                    for i in range(D):
                        if abs(v[i]) / Q > (2*M/k) * s.Vwidth(L[js][D+i]) * (1 + 1e-12): okw = False
            bump('heavy-width at every heavy index', okw)
            for js in range(k):
                if L[js] in heavy:
                    for i in range(D):
                        if v[i]:
                            r_ = s.Vwidth(L[js][D+i]) * Q / abs(v[i]) * (2*M/k)
                            key_ = 'min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1)'
                            MINS[key_] = min(MINS.get(key_, 1e300), r_)
            # diagnostic (instrument can fail on natural data): the same inequality at LIGHT indices
            for js in range(k):
                if L[js] not in heavy:
                    bad = any(abs(v[i]) / Q > (2*M/k) * s.Vwidth(L[js][D+i]) for i in range(D))
                    bump('diag(control): heavy-width inequality evaluated at a LIGHT index', not bad)
            bump(f'diag: chosen heavy label has h={h}')
            if h <= s.h0:
                # short period
                minrho = min((Q - 2*abs(YS[j][i])) for j in range(k) for i in range(D)) / (2*Q)
                if minrho < 1e-6: bump('diag: short-period heavy case with some rho < 1e-6 (near cut, no crossing)')
                if any(t[i] != 0 for i in range(D)): bump('diag: short-period heavy case with t != 0 (genuine rational step)')
                bump('short: h | lambda', lam % h == 0)
                okl = all(v[i] % h == 0 and (v[i]//h) % (q**(D-1-i)) == 0 for i in range(D))  # w_i = v_i/h in q^-i Z
                bump('short: w_i in q^{-i}Z', okl)
                bump('short: k|w_i| < 1/2', all(2*k*abs(v[i]) < h*Q for i in range(D)))
                ok2 = all(h*(YS[j][i] - YS[0][i]) == j*v[i] for j in range(k) for i in range(D))
                bump('SHORT-PERIOD CONCLUSION (ii): ytilde(n_j)=ytilde(n_0)+j w for ALL j', ok2)
                if not ok2: fails.append(('short', n0, d, fam, where, h, lab))
            elif longer_ok:
                # longer period: every full block; eligibility for blocks containing a heavy index
                rot = [ (h // gcd(h, lam*t[i])) != 1 for i in range(D) ]
                for i in range(D):
                    if rot[i]: bump('longer: rotating s_i > h0', h // gcd(h, lam*t[i]) > s.h0)
                covered = 0
                for j0 in range(0, k - h + 1, h):
                    blk = range(j0, j0+h)
                    reg = [z for z in blk if all((not rot[i]) or (Q - 2*abs(YS[z][i]))*s.etaden >= 2*Q for i in range(D))]
                    bump('longer: every full block has >= h/2 regular positions', 2*len(reg) >= h)
                    bump('longer: labels in a full block pairwise distinct', len({L[z] for z in blk}) == h)
                    if not any(L[z] in heavy for z in blk):
                        bad = not all(abs(v[i]) / Q <= s.Vwidth(L[z][D+i]) for z in blk for i in range(D) if not rot[i])
                        bump('diag(control): elig (iii) in a block with NO heavy index (not claimed)', not bad)
                    if any(L[z] in heavy for z in blk):
                        st = [i for i in range(D) if not rot[i]]
                        if st:
                            ratio = min(s.Vwidth(L[z][D+i]) * Q / max(1, abs(v[i])) for z in blk for i in st)
                            if ratio < 100: bump('diag: used block whose stationary coord has min width/|v_i| < 100 (stress)')
                            MINS['min over used blocks, stationary coords, positions of |V|/|v_i|'] = min(MINS.get('min over used blocks, stationary coords, positions of |V|/|v_i|', 1e300), ratio)
                            bump('diag: used blocks with >=1 stationary coordinate')
                        if any(rot): bump('diag: used blocks with >=1 rotating coordinate')
                        covered += h
                        bump('longer: elig (ii) |u_i|<=H_x all i, |v_i|<=H rotating',
                             all(abs(u[i])*s.Hxden <= Q for i in range(D)) and all(abs(v[i])*s.Hden <= Q for i in range(D) if rot[i]))
                        ok3 = all(abs(vscale*v[i]) / Q <= s.Vwidth(L[z][D+i]) for z in blk for i in range(D) if not rot[i])
                        bump('longer: elig (iii) stationary |v_i| <= |V(Y_z,i)| at every position', ok3)
                        if not ok3: fails.append(('iii', n0, d, fam, where, h))
                bump('longer: used full blocks cover >= 4k/5', 5*covered >= 4*k)
            else:
                bump('h > h0 but this k does not satisfy the longer-period inequalities: not checked')
    return C, fails

if __name__ == '__main__':
    name, nprog, seed = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    lam1 = '--lam1' in sys.argv; uni = '--uniformV' in sys.argv
    alpha = float(sys.argv[sys.argv.index('--alpha')+1]) if '--alpha' in sys.argv else None
    vscale = float(sys.argv[sys.argv.index('--vscale')+1]) if '--vscale' in sys.argv else 1
    if '--longer' in sys.argv: FAMILIES[:] = ['ratsmall']*6 + ['rat', 'small', 'digit']
    k, q = MODELS[name]
    mdl = Model(k, q, lam1=lam1, alpha=alpha, uniformV=uni)
    print(f"model {name}: k={k} D={mdl.D} M={mdl.M} h0={mdl.h0} lambda={mdl.lam} (formula {mdl.lam_true}) q={q} "
          f"alpha={mpmath.nstr(mdl.alpha,5)} m={mdl.m} |V|={2*mdl.m} H_x=1/{mdl.Hxden} flags={sys.argv[4:]}")
    C, fails = run(mdl, nprog, seed, vscale)
    for key, (n, f) in C.items():
        print(f"  {key:95s} checked={n:6d} FAIL={f}")
    print(f"  mesh exact-fallbacks: {mdl.mesh_fallbacks}")
    for key, val in MINS.items(): print(f"  {key}: {val:.4g}")
    print(f"  total failures recorded: {len(fails)}")
    for x in fails[:3]: print("   e.g.", x)
