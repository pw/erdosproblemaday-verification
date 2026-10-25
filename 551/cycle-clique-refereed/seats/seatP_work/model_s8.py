# Exhaustive abstract model check of Lemmas 7.1/8.1/8.2/8.3 and the separation claims of Prop 8.4,
# using ONLY Lemma 6.1/6.2 (forbidden amount window on any valid sub-system) as the source of contradictions.
# Independent of the paper's code: own pattern generator, own construction of replacement systems.
import sys, itertools
from functools import lru_cache

def chain_types(maxedges, maxamt):
    """reversal-normalized tuples of positive ints, 1..maxedges entries, sum<=maxamt (plus empty tuple)."""
    out = [()]
    def rec(pref, s):
        if pref:
            tp = tuple(pref)
            if tp <= tp[::-1]: out.append(tp)
        if len(pref) == maxedges: return
        for x in range(1, maxamt - s + 1):
            pref.append(x); rec(pref, s + x); pref.pop()
    rec([], 0)
    return sorted(set(out))

def patterns(t, B):
    types = chain_types(t - 1, B)
    res = []
    def rec(start, verts, amt, acc):
        if verts == t:
            res.append(tuple(acc)); return
        for i in range(start, len(types)):
            p = types[i]
            nv = len(p) + 1
            if verts + nv > t or amt + sum(p) > B: continue
            acc.append(p); rec(i, verts + nv, amt + sum(p), acc); acc.pop()
    rec(0, 0, 0, [])
    return res

class Sys:
    def __init__(self, pat, t):
        self.t = t
        self.chains = []   # each: dict(cl=[clique ids], edges=[edge ids])
        self.edges = []    # each: (u, w, amount, chain idx, position i (1-based), interior list)
        cid = 0
        for ci, p in enumerate(pat):
            cl = list(range(cid, cid + len(p) + 1)); cid += len(p) + 1
            eids = []
            for i, q in enumerate(p, start=1):
                eid = len(self.edges)
                interior = [('i', eid, j) for j in range(q)]   # ordered from cl[i-1] to cl[i]
                self.edges.append((cl[i-1], cl[i], q, ci, i, interior))
                eids.append(eid)
            self.chains.append(dict(cl=cl, edges=eids))
        assert cid == t
        self.L = sum(e[2] for e in self.edges); self.e = len(self.edges)
        self.chain_of = {}
        for ci, ch in enumerate(self.chains):
            for c in ch['cl']: self.chain_of[c] = ci
        self.v = sum(len(ch['cl']) for ch in self.chains if ch['edges'])
        self.missing = [c for ch in self.chains if not ch['edges'] for c in ch['cl']]

    def incoming(self, q, orient):
        """orient: dict chain->+1/-1. Returns (edge id or None, representative vertex)."""
        ci = self.chain_of[q]; ch = self.chains[ci]
        if not ch['edges']: return None, q
        pos = ch['cl'].index(q); r = len(ch['edges'])
        if orient[ci] == 1:
            if pos == 0: return None, q
            eid = ch['edges'][pos - 1]; return eid, self.edges[eid][5][0]
        else:
            if pos == r: return None, q
            eid = ch['edges'][pos]; return eid, self.edges[eid][5][-1]

def forbidden(old_edges, new_edge, L, e, k, t):
    """old_edges: list of (u,w,amt) kept old paths; new_edge (u,w,amt). True if some sub-system containing
    the new path satisfies L + [|X|>=e] <= A <= k+1-v  (Lemma 6.2; includes Lemma 6.1)."""
    n = len(old_edges)
    for mask in range(1 << n):
        A = new_edge[2]; vs = {new_edge[0], new_edge[1]}; cnt = 1
        for i in range(n):
            if mask >> i & 1:
                u, w, a = old_edges[i]; A += a; vs.add(u); vs.add(w); cnt += 1
        lo = L + (1 if cnt >= e else 0)
        if lo <= A <= k + 1 - len(vs): return True
    return False

def run(t, ks):
    stats = dict(patterns=0, C1=0, C1_surv=0, C2=0, C2_surv=0, bad=0, sepfail=0, countfail=0, alt_patterns=0)
    for k in ks:
        B = k - t
        for pat in patterns(t, B):
            stats['patterns'] += 1
            S = Sys(pat, t); L, e = S.L, S.e
            alledges = [(E[0], E[1], E[2]) for E in S.edges]
            nontriv = [ci for ci, ch in enumerate(S.chains) if ch['edges']]
            survivors = []
            # ---- C1: Lemma 7.1 constructions, every pair of targets, every orientation of the two chains
            memo = {}
            for q, q2 in itertools.combinations(range(t), 2):
                cis = sorted({S.chain_of[q], S.chain_of[q2]})
                cis_nt = [c for c in cis if S.chains[c]['edges']]
                for bits in itertools.product((1, -1), repeat=len(cis_nt)):
                    orient = {c: 1 for c in range(len(S.chains))}
                    for c, b in zip(cis_nt, bits): orient[c] = b
                    e1, r1 = S.incoming(q, orient); e2, r2 = S.incoming(q2, orient)
                    removed = [x for x in (e1, e2) if x is not None]
                    kept = [alledges[i] for i in range(e) if i not in removed]
                    ramt = sum(alledges[i][2] for i in removed)
                    for d in range(1, 7):
                        stats['C1'] += 1
                        key = (tuple(sorted(removed)), q, q2, d)
                        if key in memo: f = memo[key]
                        else:
                            f = forbidden(kept, (q, q2, ramt + d), L, e, k, t); memo[key] = f
                        if not f:
                            stats['C1_surv'] += 1
                            survivors.append((q, q2, tuple(sorted(removed)), d, r1, r2, orient))
            # check Lemma 8.1/8.2 conclusions on survivors
            alts = set()
            for (q, q2, removed, d, r1, r2, orient) in survivors:
                ok = True
                if removed: ok = False                              # no old path removed (Lemma 8.1)
                if L != k - t: ok = False                           # L = k - t
                if d < 2: ok = False
                if any(E[2] < d for E in S.edges): ok = False       # every old amount >= d
                a = sum(1 for x in (q, q2) if x in S.missing)
                if d == 2 and S.v >= t - 2 and set(S.missing) <= {q, q2}: alt = 1
                elif d == 3 and t in (9, 11) and 2*e == t - 3 and S.v == t - 3 and a == 2 and all(E[2] >= 3 for E in S.edges): alt = 2
                elif d == 5 and t == 9 and k == 19 and e == 2 and S.v == 4 and a == 2 and all(E[2] == 5 for E in S.edges): alt = 3
                else: alt = None; ok = False
                if not ok:
                    stats['bad'] += 1
                    if stats['bad'] <= 10: print("BAD survivor", t, k, pat, (q, q2, removed, d))
                alts.add(alt)
            if len(alts) > 1:
                stats['bad'] += 1; print("two alternatives for one pattern", t, k, pat, alts)
            # ---- C2: replace one step of one old path by a detour (same endpoints, amount + d); must be forbidden
            for i in range(e):
                for d in range(1, 7):
                    stats['C2'] += 1
                    kept = [alledges[j] for j in range(e) if j != i]
                    u, w, a0 = alledges[i]
                    if not forbidden(kept, (u, w, a0 + d), L, e, k, t):
                        stats['C2_surv'] += 1
                        if stats['C2_surv'] <= 5: print("C2 survivor", t, k, pat, i, d)
            if not survivors: continue
            stats['alt_patterns'] += 1
            alt = alts.pop() if len(alts) == 1 else None
            # ---- Lemma 8.3: >= 2 nonsingleton chains
            if len(nontriv) < 2:
                stats['bad'] += 1; print("Lemma 8.3 fails", t, k, pat)
            # ---- Prop 8.4: build the paper's bases; verify pairwise separation via constructions
            def reps_all_orients():
                """set of (vertex, orientation-dict) pairs"""
                pass
            def forb_pair(x, y, dset):
                """for every d in dset, some construction (C1 in an orientation where x,y are reps of distinct
                targets, or C2 when x,y consecutive on one old path) is forbidden."""
                for d in dset:
                    good = False
                    # C2: consecutive vertices on one old path
                    for i, E in enumerate(S.edges):
                        seq = [E[0]] + E[5] + [E[1]]
                        for s1, s2 in zip(seq, seq[1:]):
                            if {s1, s2} == {x, y}:
                                kept = [alledges[j] for j in range(e) if j != i]
                                if forbidden(kept, (E[0], E[1], E[2] + d), L, e, k, t): good = True
                    if not good:
                        for orient_bits in itertools.product((1, -1), repeat=len(S.chains)):
                            orient = dict(enumerate(orient_bits))
                            rep = {}
                            for q in range(t):
                                eid, r = S.incoming(q, orient); rep[r] = (q, eid)
                            if x in rep and y in rep:
                                q, e1 = rep[x]; q2, e2 = rep[y]
                                removed = [z for z in (e1, e2) if z is not None]
                                kept = [alledges[j] for j in range(e) if j not in removed]
                                ramt = sum(alledges[j][2] for j in removed)
                                if forbidden(kept, (q, q2, ramt + d), L, e, k, t): good = True; break
                    if not good: return False
                return True
            fixed = {c: 1 for c in range(len(S.chains))}
            bases = []   # (vertex, radius, alpha-lower-bound)
            c = t - S.v
            if alt == 1 and c >= 1:
                for q in range(t):
                    if q in S.missing: continue
                    eid, r = S.incoming(q, fixed); bases.append((r, 2, 3))
            elif alt == 1 and c == 0:
                if t % 2 == 0:
                    for E in S.edges:
                        if E[2] == 2: bases += [(E[5][0], 2, 3), (E[5][1], 2, 3)]
                        else: bases.append((E[5][0], 2, 3))
                else:
                    for ch in S.chains:
                        if len(ch['edges']) == 2:
                            for eid in ch['edges']: bases.append((S.edges[eid][5][0], 2, 3))   # forward-orientation reps
                        elif len(ch['edges']) == 1:
                            E = S.edges[ch['edges'][0]]; bases += [(E[5][0], 2, 3), (E[5][1], 2, 3)]
            elif alt == 2:
                for q in range(t):
                    if q in S.missing: continue
                    eid, r = S.incoming(q, fixed); bases.append((r, 2, 3))
                bases.append((S.missing[0], 2, 3))
            elif alt == 3:
                for q in range(t):
                    eid, r = S.incoming(q, fixed)
                    bases.append((r, 2, 3) if q not in S.missing else (r, 1, 2))
            else:
                print("no alternative?", t, k, pat); stats['bad'] += 1; continue
            assert len({b[0] for b in bases}) == len(bases)
            for (x, rx, _), (y, ry, _) in itertools.combinations(bases, 2):
                if not forb_pair(x, y, range(1, rx + ry + 3)):
                    stats['sepfail'] += 1; print("separation not derivable", t, k, pat, x, y, rx, ry)
            if sum(b[2] for b in bases) <= k:
                stats['countfail'] += 1; print("count fails", t, k, pat, len(bases))
            # paper's size claims
            if alt == 1 and c >= 1: assert len(bases) == t - c
            if alt == 1 and c == 0: assert len(bases) >= t - 1, (pat, len(bases))
            if alt == 2: assert len(bases) == t - 2
            if alt == 3: assert len(bases) == 9
    return stats

if __name__ == "__main__":
    t = int(sys.argv[1])
    ks = range(t, 2*t + 2) if len(sys.argv) < 3 else [int(x) for x in sys.argv[2].split(',')]
    print("t =", t, "k in", list(ks))
    print(run(t, ks))
