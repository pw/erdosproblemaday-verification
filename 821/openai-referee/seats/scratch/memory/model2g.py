# Two (or more) genuine big groups, raw pattern only (J=1 shared, l=1 unshared per group, M=2), exact.
import itertools, random, zlib, sys, time
from fractions import Fraction as Fr
import field as F

class Toy2:
    def __init__(self, groups, N, q, rho, th, k, seed=1, flags=()):
        self.groups = [sorted(g) for g in groups]; self.N = N; self.q = Fr(q); self.rho = Fr(rho)
        self.th = th; self.k = k; self.seed = seed; self.flags = set(flags)
        self.allp = sorted(p for g in self.groups for p in g)
        self.gof = {p: gi for gi, g in enumerate(self.groups) for p in g}
        self.V = [sum(Fr(1, p) for p in g) for g in self.groups]
        sq = F.sqrt_of_q(self.q)
        self.qv = [sq if i in (0, N) else F.E(self.q) for i in range(N + 1)]
        self.eta = [F.sub(F.ONE, x) for x in self.qv]
        se = F.ZERO
        for x in self.eta: se = F.add(se, x)
        self.b = {p: F.sub(F.ONE, F.scal(se, Fr(1, p))) for p in self.allp}
        self.mu_t = {p: F.inv(F.mul(F.E(self.V[self.gof[p]] * p), self.b[p])) for p in self.allp}
        self.memo = {}; self._psi = {}
    def psi(self, D):
        if D not in self._psi:
            r = random.Random(zlib.crc32(repr(('psi', self.seed, D)).encode()))
            self._psi[D] = F.E(Fr(r.randint(1, 9), r.randint(1, 5)), 0, Fr(r.randint(-9, 9), r.randint(1, 5)), 0)
        return self._psi[D]
    def mult(self, i, D):
        sig = 1 if i % 2 == 0 else -1
        m = self.psi(D) if sig == 1 else F.conj(self.psi(D))
        return F.mul(m, F.e8(self.th * sig * D))
    # ---------- LHS ----------
    def lhs(self):
        self.tot = F.ZERO; self.nz = 0; self.cross = 0
        w0 = F.ONE
        for V in self.V: w0 = F.mul(w0, F.E(V ** -2))
        for L0 in itertools.product(*[list(itertools.permutations(g, 2)) for g in self.groups]):
            self._rec(0, [L0], [0], w0)
        return self.tot
    def _rec(self, i, lists, hs, w):
        if i == self.N:
            E = self._Ey(lists, hs)
            if E != F.ZERO: self.nz += 1
            self.tot = F.add(self.tot, F.mul(w, E)); return
        sig = 1 if i % 2 == 0 else -1
        L = lists[-1]
        for perms in itertools.product([(0, 1), (1, 0)], repeat=len(self.groups)):
            S = tuple(tuple(Lg[j] for j in pm) for Lg, pm in zip(L, perms))
            D = self.k
            for Sg in S: D *= Sg[0]
            choices = [[(Sg[0], c) for c in g if c != Sg[0]] for Sg, g in zip(S, self.groups)]
            for T in itertools.product(*choices):
                we = F.scal(w, Fr(1, 2 ** len(self.groups)))
                for V in self.V: we = F.mul(we, F.E(1 / V))
                we = F.mul(we, self.mult(i, D))
                self._rec(i + 1, lists + [T], hs + [hs[-1] + sig * D], we)
    def _Ey(self, lists, hs):
        tot = F.ONE
        for p in self.allp:
            gi = self.gof[p]
            act = [i for i, L in enumerate(lists) if p in L[gi]]
            if act:
                rs = {(-hs[i]) % p for i in act}
                if len(rs) > 1: return F.ZERO
                r = rs.pop(); v = F.E(Fr(1, p))
                for i in range(len(lists)):
                    if i not in act and (r + hs[i]) % p == 0: v = F.mul(v, self.qv[i])
            else:
                cls = {}
                for i in range(len(lists)):
                    c = (-hs[i]) % p; cls[c] = F.mul(cls.get(c, F.ONE), self.qv[i])
                v = F.E(p - len(cls))
                for x in cls.values(): v = F.add(v, x)
                v = F.scal(v, Fr(1, p))
            tot = F.mul(tot, v)
        return tot
    # ---------- RHS ----------
    def rhs(self):
        tot = F.ZERO
        for L0 in itertools.product(*[list(itertools.permutations(g, 2)) for g in self.groups]):
            w = F.ONE
            for Lg in L0:
                for p in Lg: w = F.mul(w, self.mu_t[p])
            born = frozenset(p for Lg in L0 for p in Lg)
            tot = F.add(tot, F.mul(w, self.G(0, L0, (), born)))
        bp = F.ONE
        for p in self.allp: bp = F.mul(bp, self.b[p])
        return F.mul(bp, tot)
    def G(self, i, L, mem, born):
        key = ('G', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho)
        Z = [j for j, (p, r) in enumerate(mem) if r == 0]
        ct = F.div(F.neg(self.eta[i]), rho); cc = F.div(self.qv[i], F.mul(rho, rho))
        unborn = [p for p in self.allp if p not in born]
        tot = F.ZERO
        for na in range(len(Z) + 1):
            for A in itertools.combinations(Z, na):
                wA = F.mul(F.powe(ct, na), F.powe(cc, len(Z) - na))
                mem1 = tuple(x for j, x in enumerate(mem) if j not in A)
                for nb in range(len(unborn) + 1):
                    for Bs in itertools.combinations(unborn, nb):   # batch in each group (product over groups)
                        wB = wA
                        for p in Bs:
                            cb = F.div(F.mul(F.neg(self.eta[i]), F.E(self.V[self.gof[p]])), rho)
                            wB = F.mul(wB, F.mul(cb, self.mu_t[p]))
                        mem2 = tuple(sorted(mem1 + tuple((p, 0) for p in Bs)))
                        born2 = born | frozenset(Bs)
                        if i == self.N:
                            if not mem2: tot = F.add(tot, wB)
                        else:
                            tot = F.add(tot, F.mul(wB, self.E(i, L, mem2, born2)))
        self.memo[key] = tot; return tot
    def E(self, i, L, mem, born):
        key = ('E', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho); sig = 1 if i % 2 == 0 else -1
        nz_old = sum(1 for (p, r) in mem if r == 0)
        tot = F.ZERO
        ng = len(self.groups)
        for perms in itertools.product([(0, 1), (1, 0)], repeat=ng):
            S = tuple(tuple(Lg[j] for j in pm) for Lg, pm in zip(L, perms))
            D = self.k
            for Sg in S: D *= Sg[0]
            w0 = F.mul(F.E(Fr(1, 2 ** ng)), F.powe(rho, nz_old))
            for stores in itertools.product([False, True], repeat=ng):     # store slot 1 of each group?
                if any(st and D % S[g][1] == 0 for g, st in enumerate(stores)): continue
                stored = [(S[g][1], 0) for g, st in enumerate(stores) if st]
                if 'own_D' in self.flags:   # NEGATIVE CONTROL: translate group-g residues by k*(own shared label) only
                    Dg = {g: self.k * S[g][0] for g in range(ng)}
                    old_tr = [(p, (r + sig * Dg[self.gof[p]]) % p) for (p, r) in mem]
                    new_tr = [(p, (r + sig * Dg[self.gof[p]]) % p) for (p, r) in stored]
                else:
                    old_tr = [(p, (r + sig * D) % p) for (p, r) in mem]
                    new_tr = [(p, (r + sig * D) % p) for (p, r) in stored]
                # per group: target slot 1 is promoted from an old zero of that group, or fresh
                opts = []
                for g in range(ng):
                    o = [('prom', j) for j, (p, r) in enumerate(old_tr) if r == 0 and self.gof[p] == g and D % p != 0]
                    o += [('fresh', p) for p in self.groups[g] if p not in born]
                    opts.append(o)
                for ch in itertools.product(*opts):
                    proms = [c[1] for c in ch if c[0] == 'prom']
                    if len(set(proms)) < len(proms): continue
                    fresh = [c[1] for c in ch if c[0] == 'fresh']
                    if len(set(fresh)) < len(fresh): continue
                    w = w0
                    T = []
                    for g, c in enumerate(ch):
                        if c[0] == 'prom':
                            w = F.mul(w, F.E(1 / self.V[g])); T.append((S[g][0], old_tr[c[1]][0]))
                        else:
                            w = F.mul(w, self.mu_t[c[1]]); T.append((S[g][0], c[1]))
                    rem = tuple(sorted([x for j, x in enumerate(old_tr) if j not in proms] + new_tr))
                    w = F.mul(w, F.powe(rho, sum(1 for (p, r) in rem if r == 0)))
                    w = F.mul(w, self.mult(i, D))
                    tot = F.add(tot, F.mul(w, self.G(i + 1, tuple(T), rem, born | frozenset(fresh))))
        self.memo[key] = tot; return tot

if __name__ == '__main__':
    runs = [([[5, 7, 17], [11, 19, 23]], 2, Fr(1,2), Fr(9,10), 1, 1),
            ([[5, 7, 17], [11, 13, 19]], 2, Fr(1,4), Fr(3,4), 3, 2),
            ([[5, 7, 17], [11, 13, 19]], 2, Fr(4,9), Fr(5,6), 1, 3)]
    if len(sys.argv) > 1 and sys.argv[1] == 'control':
        for (groups, N, q, rho, th, k) in runs[1:2]:
            t = Toy2(groups, N, q, rho, th, k, seed=71); L = t.lhs()
            tc = Toy2(groups, N, q, rho, th, k, seed=71, flags=('own_D',)); R = tc.rhs()
            print(f"control own_D (group-g memory translated by k*s_g instead of k*D): equal={L == R}  RHS-LHS ~ {F.approx(F.sub(R, L)):.6g}")
        sys.exit()
    for (groups, N, q, rho, th, k) in runs:
        t0 = time.time(); t = Toy2(groups, N, q, rho, th, k, seed=71)
        L = t.lhs(); R = t.rhs()
        print(f"[{'EQUAL' if L == R else 'DIFFER'}] two big groups {groups} N={N} q={q} rho={rho} theta={th}/8 k={k}:"
              f" nonzero physical paths={t.nz}  ({time.time()-t0:.1f}s)\n    LHS = {F.fmt(L)}\n    RHS = {F.fmt(R)}\n    LHS ~ {F.approx(L):.10g}", flush=True)
