# General toy check of Lemma 3.7. One big group, no small groups.
# args: primes N k M J m [mutation]
import itertools, cmath, random, sys
P = [int(x) for x in sys.argv[1].split(',')]
N = int(sys.argv[2]); k = int(sys.argv[3]); M = int(sys.argv[4]); J = int(sys.argv[5]); m = int(sys.argv[6])
MUT = sys.argv[7] if len(sys.argv) > 7 else ''
q = 0.6; rho = 0.95; theta = 0.137
sig = [1 if i%2==0 else -1 for i in range(N)]
qv = [q**0.5] + [q]*(N-1) + [q**0.5]
eta = [1-x for x in qv]
V = sum(1.0/p for p in P)
mu = {p: 1.0/(V*p) for p in P}
b = {p: 1 - sum(eta)/p for p in P}
assert all(b[p] > 0 for p in P)
mut = {p: 1.0/(V*p*b[p]) for p in P}
rng = random.Random(777)
kap = {}
def kappa(i, C, src, tgt, fr):
    key = (i, C, src, tgt, fr)
    if key not in kap: kap[key] = complex(rng.uniform(-1,1), rng.uniform(-1,1))
    return kap[key]
def e(t): return cmath.exp(2j*cmath.pi*t)
patterns = [C for r in range(m+1) for C in itertools.combinations(range(J), r)]
def shared(C): return [s for s in range(J) if s not in C]
def unsh(C): return list(C) + list(range(J, M))
ordered = list(itertools.permutations(P, M))
STATS = {'phys_nodes':0, 'term':0, 'gbirth_final':0, 'promo':0, 'store':0, 'final':0}

def phys():
    tot = 0j
    def visit_update(vecs, lst, hi, i):
        new = {}
        for p in P:
            v = vecs[p][:]
            rr = (-hi) % p
            if p in lst:
                for r in range(p):
                    if r != rr: v[r] = 0.0
                if v[rr] == 0.0: return None
            else:
                v[rr] *= qv[i]
            new[p] = v
        return new
    def rec(i, src, h, vecs, w, Cs):
        nonlocal tot
        STATS['phys_nodes'] += 1
        if i == N:
            E = 1.0
            for p in P: E *= sum(vecs[p])/p
            tot += w*E; return
        C = Cs[i]; sh = shared(C); us = unsh(C)
        for fr in itertools.product(P, repeat=len(C)):
            if any(f in src for f in fr): continue
            D = 1
            for s in sh: D *= src[s]
            for f in fr: D *= f
            for tgt in ordered:
                if any(tgt[s] != src[s] for s in sh): continue
                if any(f in tgt for f in fr): continue
                wf = 1.0
                for f in fr: wf *= mu[f]
                hn = h + sig[i]*k*D
                nv = visit_update(vecs, tgt, hn, i+1)
                if nv is None: continue
                ww = w * V**(-len(us)) * wf * kappa(i, C, src, tgt, fr) * e(theta*sig[i]*k*D)
                rec(i+1, tgt, hn, nv, ww, Cs)
    for Cs in itertools.product(patterns, repeat=N):
        for L0 in ordered:
            vecs = {p: [1.0]*p for p in P}
            vecs = visit_update(vecs, L0, 0, 0)
            if vecs is None: continue
            rec(0, L0, 0, vecs, V**(-M), Cs)
    return tot

def subsets(lst):
    for r in range(len(lst)+1):
        for c in itertools.combinations(lst, r): yield c

def memory():
    tot = 0j
    def ghost(i, act, mem, born, w, Cs):
        nonlocal tot
        zeros = [x for x in mem if x[1] == 0]
        nonz = [x for x in mem if x[1] != 0]
        for A in subsets(zeros):
            keep = [x for x in zeros if x not in A]
            tc = (eta[i]/rho) if MUT=='termsign' else (-eta[i]/rho)
            w1 = w * tc**len(A) * (qv[i]/rho**2)**len(keep)
            avail = [p for p in P if p not in born]
            for S in subsets(avail):
                w2 = w1
                bc = (-eta[i]/rho) if MUT=='birthnoV' else (-eta[i]*V/rho)
                for p in S: w2 *= bc*mut[p]
                nm = tuple(sorted(nonz + keep + [(p,0) for p in S]))
                if i == N:
                    if len(nm) == 0:
                        tot += w2; STATS['final'] += 1
                        if A: STATS['term'] += 1
                    continue
                edge(i, act, nm, born | frozenset(S), w2, Cs)
    def edge(i, act, mem, born, w, Cs):
        C = Cs[i]; sh = shared(C); us = unsh(C)
        for fr in itertools.product(P, repeat=len(C)):
            if any(f in act for f in fr): continue
            D = 1
            for s in sh: D *= act[s]
            for f in fr: D *= f
            wf = w
            for f in fr: wf *= mu[f]
            nz = sum(1 for x in mem if x[1] == 0)
            if MUT != 'norho2': wf *= rho**nz
            Delta = sig[i]*k*D
            for St in subsets(us):
                stored = [act[s] for s in St]
                if MUT != 'storeD' and any(D % p == 0 for p in stored): continue
                old = [(p, (r+Delta) % p) for (p,r) in mem]
                new = [(p, Delta % p) for p in stored]
                if MUT == 'promnew':
                    pool = old + new
                else:
                    pool = old
                cands = [j for j,(p,r) in enumerate(pool) if r == 0 and D % p != 0]
                def fill(slots, tgt, used, born2, w3):
                    if not slots:
                        if any(f in tgt for f in fr): return
                        tg = tuple(tgt)
                        rem = [pool[j] for j in range(len(pool)) if j not in used]
                        if MUT != 'promnew': rem = rem + new
                        nz2 = sum(1 for x in rem if x[1] == 0)
                        w4 = w3 * rho**nz2 * kappa(i, C, act, tg, fr) * e(theta*sig[i]*k*D)
                        if used: STATS['promo'] += 1
                        if St: STATS['store'] += 1
                        ghost(i+1, tg, tuple(sorted(rem)), born2, w4, Cs)
                        return
                    s = slots[0]
                    for j in cands:
                        if j in used: continue
                        t2 = list(tgt); t2[s] = pool[j][0]
                        fill(slots[1:], t2, used | {j}, born2, w3 * V**(-1))
                    for p in P:
                        if p in born2 and MUT != 'nodistinct': continue
                        t2 = list(tgt); t2[s] = p
                        fill(slots[1:], t2, used, born2 | {p}, w3 * mut[p])
                fill(us, list(act), frozenset(), born, wf)
    for Cs in itertools.product(patterns, repeat=N):
        for L0 in ordered:
            w0 = 1.0
            for p in L0: w0 *= mut[p]
            ghost(0, L0, tuple(), frozenset(L0), w0, Cs)
    base = 1.0
    for p in P: base *= b[p]
    return base * tot

a = phys(); mm = memory()
print("args", sys.argv[1:], "phys", a, "mem", mm, "rel", abs(a-mm)/abs(a), STATS)
