# Toy instance of OpenAI 011 paper, Sections 3.2-3.4: physical independent-residue path sum (LHS of (3.17))
# versus  prod_p b_p * <1_empty, G_0 E_0 G_1 ... E_{N-1} G_N 1_empty>_distinct  (RHS of (3.17)).
# One big group P (no small groups; small-group shifts emulated by per-edge integer factors kseq[i]).
import itertools, random, zlib
from fractions import Fraction as Fr
from math import factorial
import field as F

class Toy:
    def __init__(self, P, J, ell, patterns, N, q, rho, theta_num, kseq, seed=1, flags=(), sqrtq=None,
                 edge_patterns=None, edge_perms=None):
        self.P = sorted(P); self.J = J; self.ell = ell; self.M = J + ell
        self.patterns = patterns          # list of frozensets C (free slots among 0..J-1); C empty = raw (K=1)
        self.N = N; self.q = Fr(q); self.rho = Fr(rho); self.th = theta_num
        assert len(kseq) == N; self.kseq = kseq
        for p in self.P: assert all(p > abs(k) for k in kseq), "group primes must exceed |k| (paper p.15)"
        self.flags = set(flags)
        self.sq = F.sqrt_of_q(self.q) if sqrtq is None else sqrtq
        assert F.approx(self.sq).real < float(self.rho)**2, "need rho^2 > sqrt q"
        self.V = sum(Fr(1, p) for p in self.P)
        self.Ve = F.E(self.V)
        self.qv = [self.sq if i in (0, N) else F.E(self.q) for i in range(N + 1)]
        self.eta = [F.sub(F.ONE, x) for x in self.qv]
        # RHS-side copies (negative controls may perturb only the RHS)
        self.qvR = list(self.qv)
        if 'q0_bulk' in self.flags:
            self.qvR = [F.E(self.q) for i in range(N + 1)]
        self.etaR = [F.sub(F.ONE, x) for x in self.qvR]
        sum_eta = F.ZERO
        for x in self.etaR: sum_eta = F.add(sum_eta, x)
        if 'baseline_internal_only' in self.flags:
            sum_eta = F.ZERO
            for x in self.etaR[1:-1]: sum_eta = F.add(sum_eta, x)
        self.b = {p: F.sub(F.ONE, F.scal(sum_eta, Fr(1, p))) for p in self.P}
        self.mu = {p: F.E(1 / (self.V * p)) for p in self.P}
        self.mut = {p: F.inv(F.mul(F.E(self.V * p), self.b[p])) for p in self.P}
        self.seed = seed
        self._K = {}; self._psi = {}
        self.memo = {}
        # optional restriction to fixed pattern / permutation sequences (identity is claimed path by path)
        self.edge_patterns = edge_patterns if edge_patterns is not None else [list(range(len(patterns)))] * N
        allperms = list(itertools.permutations(range(self.M)))
        self.edge_perms = edge_perms if edge_perms is not None else [allperms] * N

    # ---- arbitrary coefficients (identical on both sides) ----
    def K(self, pi, S, T, free):
        if not self.patterns[pi]: return F.ONE        # raw pattern K_0 = 1
        key = (pi, S, T, free)
        if key not in self._K:
            r = random.Random(zlib.crc32(repr(('K', self.seed, key)).encode()))
            self._K[key] = F.E(Fr(r.randint(-9, 9), r.randint(1, 7)), 0,
                               Fr(r.randint(-9, 9), r.randint(1, 7)), 0)
        return self._K[key]

    def psi(self, D):          # stands in for D^{i zeta}; backward edges use the conjugate
        if D not in self._psi:
            r = random.Random(zlib.crc32(repr(('psi', self.seed, D)).encode()))
            self._psi[D] = F.E(Fr(r.randint(1, 9), r.randint(1, 5)), 0,
                               Fr(r.randint(-9, 9), r.randint(1, 5)), 0)
        return self._psi[D]

    def edge_mult(self, i, pi, S, T, free, D):
        sig = 1 if i % 2 == 0 else -1
        if sig == 1:
            return F.mul(self.K(pi, S, T, free), self.psi(D))
        else:   # adjoint: interchange source/target labels in the coefficient and conjugate
            return F.conj(F.mul(self.K(pi, T, S, free), self.psi(D)))

    def slots(self, C):
        shared = [s for s in range(self.J) if s not in C]
        unsh = sorted(C) + list(range(self.J, self.M))
        return shared, unsh

    def Dval(self, i, S, shared, free):
        D = self.kseq[i]
        for s in shared: D *= S[s]
        for f in free: D *= f
        return D

    # =================== LHS: physical path sum in the independent-residue model ===================
    def lhs(self, brute=False):
        P, M, N = self.P, self.M, self.N
        self._lhs_total = F.ZERO; self._npaths = 0
        w0 = F.E(self.V ** (-M))
        self.stats = dict(nonzero=0, hN_nonzero=0, cmp_edge=0, multirun=0, endpoint_hit=0, pending_hit=0,
                          ghost_needed=0, orphan_possible=0, two_orphans_possible=0)
        for L0 in itertools.permutations(P, M):
            self._lhs_rec(0, [L0], [0], w0, brute, [])
        return self._lhs_total

    def _lhs_rec(self, i, lists, hs, w, brute, pats):
        N, M, P = self.N, self.M, self.P
        if i == N:
            Efac = self._Ey_brute(lists, hs) if brute else self._Ey(lists, hs)
            ph = F.e8(self.th * hs[-1])             # e(theta h_N), theta = th/8   (3.11)
            c = F.mul(F.mul(w, Efac), ph)
            self._lhs_total = F.add(self._lhs_total, c)
            self._npaths += 1
            if Efac != F.ZERO: self._stat(lists, hs, pats)
            return
        sig = 1 if i % 2 == 0 else -1
        L = lists[-1]
        for perm in self.edge_perms[i]:
            S = tuple(L[j] for j in perm)
            wp = F.scal(w, Fr(1, factorial(M)))
            for pi in self.edge_patterns[i]:
                C = self.patterns[pi]
                shared, unsh = self.slots(C)
                t = len(unsh)
                for free in itertools.product(P, repeat=len(C)):
                    if 'free_equal_only' in self.flags and len(set(free)) > 1: continue
                    if any(f in S for f in free): continue          # ban: free labels not in source list
                    wf = wp
                    for f in free: wf = F.mul(wf, self.mu[f])          # free labels have law mu_g
                    D = self.Dval(i, S, shared, free)
                    for tl in itertools.product(P, repeat=t):
                        T = list(S)
                        for idx, s in enumerate(unsh): T[s] = tl[idx]
                        T = tuple(T)
                        if len(set(T)) < M: continue                 # physical lists: distinct labels
                        if any(f in T for f in free): continue      # ban: free labels not in target list
                        we = F.mul(wf, F.E(self.V ** (-t)))           # prod V_g^{-t_g}
                        we = F.mul(we, self.edge_mult(i, pi, S, T, free, D))
                        self._lhs_rec(i + 1, lists + [T], hs + [hs[-1] + sig * D], we, brute, pats + [pi])

    def _stat(self, lists, hs, pats):
        st = self.stats; st['nonzero'] += 1
        if hs[-1] != 0: st['hN_nonzero'] += 1
        if any(self.patterns[pi] for pi in pats): st['cmp_edge'] += 1
        N = len(lists) - 1
        mr = eh = ph = gh = False
        norph = 0
        for p in self.P:
            act = [i for i, L in enumerate(lists) if p in L]
            if not act:
                cls = {}
                for i in range(N + 1): cls[(-hs[i]) % p] = cls.get((-hs[i]) % p, 0) + 1
                if max(cls.values()) >= 2: norph += 1
            if act:
                runs = 1 + sum(1 for a, b in zip(act, act[1:]) if b > a + 1)
                if runs >= 2: mr = True
                r = (-hs[act[0]]) % p
                hits = [i for i in range(N + 1) if i not in act and (r + hs[i]) % p == 0]
                if any(i in (0, N) for i in hits): eh = True
                if any(act[0] < i < act[-1] for i in hits): ph = True
                if any(i < act[0] or i > act[-1] for i in hits): gh = True
        st['multirun'] += mr; st['endpoint_hit'] += eh; st['pending_hit'] += ph; st['ghost_needed'] += gh
        st['orphan_possible'] += (norph >= 1); st['two_orphans_possible'] += (norph >= 2)

    def _Ey(self, lists, hs):
        # expectation over independent uniform residues of (3.8); factorizes over primes
        tot = F.ONE
        for p in self.P:
            act = [i for i, L in enumerate(lists) if p in L]
            if act:
                rs = {(-hs[i]) % p for i in act}
                if len(rs) > 1: return F.ZERO
                r = rs.pop()
                v = F.E(Fr(1, p))
                for i in range(len(lists)):
                    if i not in act and (r + hs[i]) % p == 0: v = F.mul(v, self.qv[i])
            else:
                cls = {}
                for i in range(len(lists)):
                    c = (-hs[i]) % p
                    cls[c] = F.mul(cls.get(c, F.ONE), self.qv[i])
                v = F.E(p - len(cls))
                for x in cls.values(): v = F.add(v, x)
                v = F.scal(v, Fr(1, p))
            tot = F.mul(tot, v)
        return tot

    def _Ey_brute(self, lists, hs):
        # honest Haar average over y in prod Z/pZ of (3.8) -- control for the shortcut
        tot = F.ZERO; cnt = 0
        for y in itertools.product(*[range(p) for p in self.P]):
            v = F.ONE
            for i, L in enumerate(lists):
                for p, yp in zip(self.P, y):
                    hit = (yp + hs[i]) % p == 0
                    if p in L:
                        if not hit: v = F.ZERO; break
                    elif hit: v = F.mul(v, self.qv[i])
                if v == F.ZERO: break
            tot = F.add(tot, v); cnt += 1
        return F.scal(tot, Fr(1, cnt))

    # =================== RHS: memory evolution with distinct-birth rule ===================
    def rhs(self):
        P, M = self.P, self.M
        tot = F.ZERO
        for L0 in itertools.permutations(P, M):        # initial active slots are births: distinct
            w = F.ONE
            for p in L0: w = F.mul(w, self.birthmass(p))
            tot = F.add(tot, F.mul(w, self.G(0, L0, (), frozenset(L0))))
        return tot

    def birthmass(self, p):
        return self.mu[p] if 'mu_not_mut' in self.flags else self.mut[p]

    def baseline(self):
        x = F.ONE
        for p in self.P: x = F.mul(x, self.b[p])
        return x

    def G(self, i, L, mem, born):
        key = ('G', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        rho = F.E(self.rho)
        Z = [j for j, (p, r) in enumerate(mem) if r == 0]
        tot = F.ZERO
        cterm = F.div(F.neg(self.etaR[i]), rho)                       # -eta_i/rho  (termination)
        ccont = F.div(self.qvR[i], F.mul(rho, rho))                    # q_i/rho^2   (continuing zero)
        cbirth = F.div(F.mul(F.neg(self.etaR[i]), self.Ve), rho)       # -eta_i V_g/rho (birth)
        unborn = list(self.P) if 'ghost_repeat' in self.flags else [p for p in self.P if p not in born]
        for na in range(len(Z) + 1):
            for A in itertools.combinations(Z, na):
                wA = F.mul(F.powe(cterm, na), F.powe(ccont, len(Z) - na))
                mem1 = tuple(x for j, x in enumerate(mem) if j not in A)
                for nb in range(len(unborn) + 1):
                    for Bs in itertools.combinations(unborn, nb):
                        # (1/b!) * ordered integral over distinct values == sum over b-sets
                        wB = wA
                        for p in Bs: wB = F.mul(wB, F.mul(cbirth, self.mut[p]))
                        if 'no_bfact' in self.flags: wB = F.scal(wB, factorial(nb))
                        mem2 = tuple(sorted(mem1 + tuple((p, 0) for p in Bs)))
                        born2 = born | frozenset(Bs)
                        if i == self.N:
                            if not mem2: tot = F.add(tot, wB)      # 1_empty at the end
                        else:
                            tot = F.add(tot, F.mul(wB, self.E(i, L, mem2, born2)))
        self.memo[key] = tot
        return tot

    def E(self, i, L, mem, born):
        key = ('E', i, L, mem, born)
        if key in self.memo: return self.memo[key]
        P, M = self.P, self.M
        rho = F.E(self.rho)
        sig = 1 if i % 2 == 0 else -1
        tot = F.ZERO
        nz_old = sum(1 for (p, r) in mem if r == 0)
        for perm in self.edge_perms[i]:
            S = tuple(L[j] for j in perm)
            wp = F.E(Fr(1, factorial(M)))
            for pi in self.edge_patterns[i]:
                C = self.patterns[pi]
                shared, unsh = self.slots(C)
                for free in itertools.product(P, repeat=len(C)):
                    if 'free_equal_only' in self.flags and len(set(free)) > 1: continue
                    if 'no_ban' not in self.flags and any(f in S for f in free): continue
                    wf = wp
                    for f in free: wf = F.mul(wf, self.mut[f] if 'free_mut' in self.flags else self.mu[f])
                    D = self.Dval(i, S, shared, free)
                    w_ii = F.mul(wf, F.powe(rho, nz_old))                 # (ii) rho per old pending zero
                    for ns in range(len(unsh) + 1):
                        for St in itertools.combinations(unsh, ns):      # subset of unshared source slots stored
                            if 'no_pnotD' not in self.flags and any(D % S[s] == 0 for s in St): continue
                            stored = [(S[s], 0) for s in St]
                            old_tr = [(p, (r + sig * D) % p) for (p, r) in mem]      # (iii) translate
                            new_tr = [(p, (r + sig * D) % p) for (p, r) in stored]
                            pool = list(enumerate(old_tr))
                            if 'prom_new' in self.flags:
                                pool = pool + [(len(old_tr) + j, x) for j, x in enumerate(new_tr)]
                            allp = old_tr + new_tr
                            cand = [j for j, (p, r) in pool if r == 0 and
                                    ('no_pnotD' in self.flags or D % p != 0)]
                            for npro in range(len(unsh) + 1):
                                for Tp in itertools.combinations(unsh, npro):
                                    for inj in itertools.permutations(cand, npro):
                                        rem = tuple(sorted(x for j, x in enumerate(allp) if j not in inj))
                                        wpr = F.mul(w_ii, F.E(self.V ** (-npro)))   # V_g^{-1} per promotion
                                        fresh_slots = [s for s in unsh if s not in Tp]
                                        if 'fresh_repeat' in self.flags:
                                            fpool = list(P)
                                        else:
                                            fpool = [p for p in P if p not in born]
                                        for fl in itertools.product(fpool, repeat=len(fresh_slots)):
                                            if 'fresh_repeat' not in self.flags and len(set(fl)) < len(fl):
                                                continue                       # distinct births
                                            T = list(S)
                                            for s, j in zip(Tp, inj): T[s] = allp[j][0]
                                            for s, p in zip(fresh_slots, fl): T[s] = p
                                            T = tuple(T)
                                            if 'no_ban' not in self.flags and any(f in T for f in free): continue
                                            wfr = wpr
                                            for p in fl: wfr = F.mul(wfr, self.birthmass(p))
                                            nz_new = sum(1 for (p, r) in rem if r == 0)
                                            if 'no_rho_iv' not in self.flags:
                                                wfr = F.mul(wfr, F.powe(rho, nz_new))   # (iv)
                                            wfr = F.mul(wfr, self.edge_mult(i, pi, S, T, free, D))
                                            wfr = F.mul(wfr, F.e8(self.th * sig * D))     # (i) e(theta sigma k D)
                                            born2 = born | frozenset(fl)
                                            tot = F.add(tot, F.mul(wfr, self.G(i + 1, T, rem, born2)))
        self.memo[key] = tot
        return tot

    def rhs_full(self):
        return F.mul(self.baseline(), self.rhs())
