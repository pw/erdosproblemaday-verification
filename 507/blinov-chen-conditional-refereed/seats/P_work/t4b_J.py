# Seat P, task 4 (cont.): the ACTUAL event J (det C has a representative in [-tau, tau]) with a base B large
# enough for the carry bounds (B-1 >= 100 k^2 P), exact enumeration, Python integers.
# Checks: J => F_{k-1}=0 on every outcome; P(J) <= 1/M; P(b>=j, J) <= M^-(2j+1); b <= a;
# E[D 1_J] <= (1/M)(1+sum_{j<=a} theta^j); distinct labels => J never; uniform P(b>=j) <= M^-2j.
import sys, itertools, random
from fractions import Fraction

def is_prime(n):
    if n < 2: return False
    i = 2
    while i*i <= n:
        if n % i == 0: return False
        i += 1
    return True

def run(r, tags, k, M, labels, row3='zero', seed=3):
    rng = random.Random(seed)
    span = max(tags)+1
    L1 = L2 = r; L3 = r*M; P = L1*L2*L3
    B = 100*k*k*P + 1
    while not is_prime(B): B += 1
    h = B**k; tau = B**(k-1)//2
    table = {}
    def res(key):
        if key not in table: table[key] = rng.randrange(r)
        return table[key]
    def top(label):
        A, Q = [], []
        for p in range(k):
            if p < span:
                ra = 1 if p == 0 else 0
                rq = label[tags.index(p)] if p in tags else 0
            else:
                ra, rq = res((label, 1, p)), res((label, 2, p))
            A.append(ra or r); Q.append(rq or r)
        return A, Q
    def opts(label):
        reps = [r]*k if row3 == 'zero' else [(res((label, 3, p)) or r) for p in range(k)]
        return [tuple(reps[p] + r*c[p] for p in range(k)) for c in itertools.product(range(M), repeat=k)]
    def ev(d): return sum(x*B**i for i, x in enumerate(d))
    def pmul(a, b):
        o = [0]*(len(a)+len(b)-1)
        for i, x in enumerate(a):
            for j, y in enumerate(b): o[i+j] += x*y
        return o
    tops = [top(l) for l in labels]
    O = [opts(l) for l in labels]
    Ev = [[ev(d) for d in o] for o in O]
    # cofactors along row 3 (integers at Y=B and as polynomials for F_{k-1})
    cof_int = []; cof_w = []
    for j in range(3):
        oth = [c for c in range(3) if c != j]
        (Ap, Qp), (Aq, Qq) = tops[oth[0]], tops[oth[1]]
        sg = (-1)**(3 + j + 1)
        poly = [x - y for x, y in zip(pmul(Ap, Qq), pmul(Aq, Qp))]
        cof_int.append(sg*(ev(Ap)*ev(Qq) - ev(Aq)*ev(Qp)))
        cof_w.append([sg*(poly[k-1-p] if 0 <= k-1-p < len(poly) else 0) for p in range(k)])
    TA = [ev(t[0]) for t in tops]; TQ = [ev(t[1]) for t in tops]
    def val(x):
        x %= h
        if x == 0: return k
        v = 0
        while x % B == 0: x //= B; v += 1
        return v
    U = TA[0]*TQ[2] - TA[2]*TQ[0]
    n = len(O[0])
    tot = n**3; cJ = 0; cbJ = [0]*(k+1); cb = [0]*(k+1); sumDJ = 0; viol_imp = 0; bmax = 0
    Fw = [[sum(w*d for w, d in zip(cof_w[j], O[j][i])) for i in range(n)] for j in range(3)]
    for i1 in range(n):
        z1 = Ev[0][i1]
        for i2 in range(n):
            z2 = Ev[1][i2]
            for i3 in range(n):
                z3 = Ev[2][i3]
                det = (z1*cof_int[0] + z2*cof_int[1] + z3*cof_int[2]) % h
                if det > h//2: det -= h
                J = abs(det) <= tau
                F = Fw[0][i1] + Fw[1][i2] + Fw[2][i3]
                if J and F != 0: viol_imp += 1
                C = [[TA[0], TA[1], TA[2]], [TQ[0], TQ[1], TQ[2]], [z1, z2, z3]]
                b = k
                for (ra, rb) in ((0,1),(0,2),(1,2)):
                    for (ca, cb_) in ((0,1),(0,2),(1,2)):
                        b = min(b, val(C[ra][ca]*C[rb][cb_] - C[ra][cb_]*C[rb][ca]))
                bmax = max(bmax, b)
                for j in range(1, b+1): cb[j] += 1
                if J:
                    cJ += 1; sumDJ += B**b
                    for j in range(1, b+1): cbJ[j] += 1
    return dict(B=B, tot=tot, cJ=cJ, cbJ=cbJ, cb=cb, sumDJ=sumDJ, viol_imp=viol_imp, bmax=bmax)

def report(r, tags, k, M, labels, row3):
    d = run(r, tags, k, M, labels, row3)
    lam, lam2, mu = labels
    tot = d['tot']; B = d['B']
    out = f'labels {labels} row3={row3} B={B}: J=>F_(k-1)=0 violations {d["viol_imp"]}; P(J)={Fraction(d["cJ"], tot)}'
    ok = d['viol_imp'] == 0
    for j in range(1, 3):
        ok &= Fraction(d['cb'][j], tot) <= Fraction(1, M**(2*j))
    if lam == lam2 and lam != mu:
        s = next(i for i in range(len(lam)) if lam[i] != mu[i]); a = tags[s]
        ok &= Fraction(d['cJ'], tot) <= Fraction(1, M) and d['bmax'] <= a
        out += f' a={a} b_max={d["bmax"]}'
        for j in range(1, a+1):
            p = Fraction(d['cbJ'][j], tot); bd = Fraction(1, M**(2*j+1)); ok &= p <= bd
            out += f' | P(b>={j},J)={p} <= {bd}'
        th = Fraction(B, M*M)
        bnd = Fraction(1, M)*(1 + sum(th**j for j in range(1, a+1)))
        ED = Fraction(d['sumDJ'], tot); ok &= ED <= bnd
        out += f' | E[D1_J]={float(ED):.4g} <= {float(bnd):.4g}'
    elif len(set(labels)) == 3:
        ok &= d['cJ'] == 0
        out += ' (distinct: J must be empty)'
    print(out, 'OK' if ok else 'FAIL')
    return ok

if __name__ == '__main__':
    allok = True
    for M in (2, 3):
        r, tags, k = 5, (0, 1), 4
        for row3 in ('zero', 'random'):
            for labels in [((2, 3), (2, 3), (2, 4)), ((2, 3), (2, 3), (4, 3)), ((0, 0), (0, 0), (0, 1)),
                           ((1, 2), (1, 2), (1, 2))]:
                allok &= report(r, tags, k, M, labels, row3)
    print('ALL OK' if allok else 'SOME FAIL')
