# Toy check of Lemma 3.7 (exact memory identity), one big group, no small groups.
# M = 2 slots (J=1 shared-capable slot, ell=1). Patterns: nu=0 (slot0 shared, t=1), nu=1 (slot0 free, t=2).
# Physical side: sum over lists/patterns/free labels of weights x E_residue[(3.8)].
# Memory side: Prod b_p x sum over memory histories (Section 3.4 rules) with distinct-birth rule.
import itertools, cmath, random, sys
from fractions import Fraction

P = [int(x) for x in sys.argv[1].split(',')] if len(sys.argv)>1 else [5,7,11]
N = int(sys.argv[2]) if len(sys.argv)>2 else 3
k = int(sys.argv[3]) if len(sys.argv)>3 else 1
q = 0.6; rho = 0.95; theta = 0.137
sig = [1 if i%2==0 else -1 for i in range(N)]
qv = [q**0.5] + [q]*(N-1) + [q**0.5]
eta = [1-x for x in qv]
V = sum(1.0/p for p in P)
mu = {p: 1.0/(V*p) for p in P}
b = {p: 1 - sum(eta)/p for p in P}
mut = {p: 1.0/(V*p*b[p]) for p in P}
M = 2
rng = random.Random(12345)
kap_cache = {}
def kappa(i, nu, src, tgt, f):
    key = (i, nu, src, tgt, f)
    if key not in kap_cache:
        kap_cache[key] = complex(rng.uniform(-1,1), rng.uniform(-1,1))
    return kap_cache[key]
def e(t): return cmath.exp(2j*cmath.pi*t)
def unshared_src(nu): return [1] if nu==0 else [0,1]
def unshared_tgt(nu): return [1] if nu==0 else [0,1]
def tcount(nu): return 1 if nu==0 else 2

# ---------------- physical ----------------
def E_res(lists, h):
    tot = 1.0
    for p in P:
        s = 0.0
        for r in range(p):
            prod = 1.0
            for i in range(N+1):
                hit = ((r + h[i]) % p == 0)
                if p in lists[i]:
                    if not hit: prod = 0.0; break
                else:
                    if hit: prod *= qv[i]
            s += prod
        tot *= s/p
    return tot

def phys():
    total = 0j
    ordered = [lst for lst in itertools.permutations(P, M)]
    for nus in itertools.product([0,1], repeat=N):
        def rec(i, lists, h, w):
            nonlocal total
            if i == N:
                total += w * E_res(lists, h)
                return
            src = lists[-1]; nu = nus[i]
            if nu == 0:
                D = src[0]
                for x in P:
                    if x == src[0]: continue
                    tgt = (src[0], x)
                    ww = w * V**(-1) * kappa(i,nu,src,tgt,None) * e(theta*sig[i]*k*D)
                    rec(i+1, lists+[tgt], h+[h[-1]+sig[i]*k*D], ww)
            else:
                for f in P:
                    if f in src: continue
                    for tgt in ordered:
                        if f in tgt: continue
                        D = f
                        ww = w * V**(-2) * mu[f] * kappa(i,nu,src,tgt,f) * e(theta*sig[i]*k*D)
                        rec(i+1, lists+[tgt], h+[h[-1]+sig[i]*k*D], ww)
        for L0 in ordered:
            rec(0, [L0], [0], V**(-M))
    return total

# ---------------- memory ----------------
def subsets(lst):
    for r in range(len(lst)+1):
        for c in itertools.combinations(lst, r):
            yield c

def memory():
    total = 0j
    # state: active list (tuple), memory: tuple of (prime,res) sorted, born: frozenset
    def ghost(i, act, mem, born, w, cont):
        zeros = [x for x in mem if x[1] % x[0] == 0]
        nonz = [x for x in mem if x[1] % x[0] != 0]
        for A in subsets(zeros):
            Aset = set(A)
            keep = [x for x in zeros if x not in Aset]
            w1 = w * (-eta[i]/rho)**len(A) * (qv[i]/rho**2)**len(keep)
            avail = [p for p in P if p not in born]
            for S in subsets(avail):
                w2 = w1
                for p in S: w2 *= (-eta[i]*V/rho) * mut[p]
                newmem = tuple(sorted(nonz + keep + [(p,0) for p in S]))
                cont(i, act, newmem, born | frozenset(S), w2)
    def edge(i, act, mem, born, w):
        nu = nus_g[i]
        frees = [None] if nu==0 else [f for f in P if f not in act]
        for f in frees:
            D = act[0] if nu==0 else f
            wf = w if nu==0 else w*mu[f]
            # (ii) rho per old pending zero
            nz = sum(1 for x in mem if x[1] % x[0] == 0)
            wf2 = wf * rho**nz
            us = unshared_src(nu)
            for St in subsets(us):
                stored = [act[s] for s in St]
                if any(D % p == 0 for p in stored): continue
                Delta = sig[i]*k*D
                old = [(p, (r+Delta) % p) for (p,r) in mem]
                new = [(p, Delta % p) for p in stored]
                ut = unshared_tgt(nu)
                # for each unshared target slot: promote an old zero (p not | D) or fresh
                cands = [idx for idx,(p,r) in enumerate(old) if r==0 and D % p != 0]
                def fill(slots, tgt, used, born2, w3):
                    if not slots:
                        if nu==1 and f in tgt: return
                        tg = tuple(tgt)
                        remaining = [old[j] for j in range(len(old)) if j not in used] + new
                        nz2 = sum(1 for x in remaining if x[1] % x[0] == 0)
                        w4 = w3 * rho**nz2 * kappa(i,nu,act,tg,f) * e(theta*sig[i]*k*D)
                        ghost(i+1, tg, tuple(sorted(remaining)), born2, w4, after_ghost)
                        return
                    s = slots[0]
                    for j in cands:
                        if j in used: continue
                        t2 = list(tgt); t2[s] = old[j][0]
                        fill(slots[1:], t2, used|{j}, born2, w3 * V**(-1))
                    for p in P:
                        if p in born2: continue
                        t2 = list(tgt); t2[s] = p
                        fill(slots[1:], t2, used, born2|{p}, w3 * mut[p])
                tgt0 = list(act)  # shared slots copied; unshared overwritten
                fill(ut, tgt0, frozenset(), born, wf2)
    def after_ghost(i, act, mem, born, w):
        nonlocal total
        if i == N:
            if len(mem) == 0: total += w
            return
        edge(i, act, mem, born, w)
    global nus_g
    for nus in itertools.product([0,1], repeat=N):
        nus_g = nus
        for L0 in itertools.permutations(P, M):
            w0 = mut[L0[0]] * mut[L0[1]]
            ghost(0, L0, tuple(), frozenset(L0), w0, after_ghost)
    base = 1.0
    for p in P: base *= b[p]
    return base * total

a = phys(); m = memory()
print("P=",P,"N=",N,"k=",k)
print("physical:", a)
print("memory  :", m)
print("abs diff:", abs(a-m), " rel:", abs(a-m)/max(abs(a),1e-300))
