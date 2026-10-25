# Toy brute-force check of §3: identity (3.2), Lemma 3.1 (alternating included-node sum <= S_1(B), with and without
# prefix-free lower stops), size claim J_d >= w^{a*}, and the comparison identity (3.5), over random AND adversarial
# residue classes.  Controls: (i) moving the admission test to LOWER nodes must break the lower bound for some classes;
# (ii) a perturbed reference recursion must break (3.5).
import math, random, itertools
import numpy as np

def primes_upto(n):
    return [p for p in range(2, n+1) if all(p % q for q in range(2, int(p**.5)+1))]

def run(w, z, Y, astar, trials, rng, adversarial=False, wrong_rule=False):
    P = primes_upto(z); small = [p for p in P if p <= w]; big = sorted([p for p in P if p > w], reverse=True)
    lw = math.log(w); x = {p: math.log(p)/lw for p in big}
    V0 = np.prod([1-1/p for p in small]); B = math.log(z)/lw
    H = lambda t: max(2*t, t+2)
    n = np.arange(1, Y+1)
    worst = math.inf; fails = 0; maxid = 0.0; minJ = math.inf; idviol = 0.0
    for tr in range(trials):
        cls = {p: rng.randrange(p) for p in P}
        if adversarial:   # greedy covering: choose each big prime's class to hit the most current survivors
            alive = np.ones(Y, bool)
            for p in small: alive &= (n % p != cls[p])
            for p in sorted(big):
                cnt = np.bincount(n[alive] % p, minlength=p); cls[p] = int(np.argmax(cnt)); alive &= (n % p != cls[p])
        smallok = np.ones(Y, bool)
        for p in small: smallok &= (n % p != cls[p])
        hit = {p: (n % p == cls[p]) for p in big}
        def Nd(tup):
            m = smallok.copy()
            for p in tup: m &= hit[p]
            return int(m.sum())
        def Sd(tup):
            m = smallok.copy()
            for p in tup: m &= hit[p]
            avail = [q for q in big if (not tup or q < tup[-1])]
            for q in avail: m &= ~hit[q]
            return int(m.sum())
        S1 = Sd(())
        # build included tree; tree value T_d; also a random prefix-free stopped variant
        def gap(tup):
            d = math.prod(tup) if tup else 1
            return math.log(Y/d)/lw - astar + 2, Y/d
        stops = set()
        def T(tup, stop_prob):
            nonlocal minJ
            r, J = gap(tup); minJ = min(minJ, J)
            lower = (len(tup) % 2 == 0)
            if lower and tup and rng.random() < stop_prob:
                stops.add(tup); return Sd(tup)
            avail = [q for q in big if (not tup or q < tup[-1])]
            val = Nd(tup)
            for q in avail:
                xq = x[q]; child = tup + (q,)
                if lower and not wrong_rule: inc = True
                elif lower and wrong_rule: inc = (r - xq >= H(xq))
                else: inc = True if wrong_rule else (r - xq >= H(xq))
                if inc: val -= T(child, stop_prob)
            return val
        for sp in [0.0, 0.3]:
            stops.clear()
            Lval = T((), sp)
            worst = min(worst, S1 - Lval)
            if Lval > S1: fails += 1
        # identity (3.2) at random nodes
        for _ in range(5):
            k = rng.randrange(0, 4); tup = tuple(sorted(rng.sample(big, k), reverse=True))
            avail = [q for q in big if (not tup or q < tup[-1])]
            lhs = Sd(tup); rhs = Nd(tup) - sum(Sd(tup+(q,)) for q in avail)
            idviol = max(idviol, abs(lhs-rhs))
    return dict(B=B, worst_margin=worst, fails=fails, minJ=minJ, wa=w**astar, id32_maxviol=idviol)

def comparison_identity(w, z, Y, astar, rng, perturb=False):
    P = primes_upto(z); small = [p for p in P if p <= w]; big = sorted([p for p in P if p > w], reverse=True)
    lw = math.log(w); x = {p: math.log(p)/lw for p in big}; V0 = np.prod([1-1/p for p in small])
    H = lambda t: max(2*t, t+2) + (0.3 if perturb else 0.0)
    Hstop = lambda t: max(2*t, t+2)
    n = np.arange(1, Y+1); cls = {p: rng.randrange(p) for p in P}
    smallok = np.ones(Y, bool)
    for p in small: smallok &= (n % p != cls[p])
    hit = {p: (n % p == cls[p]) for p in big}
    def mask(tup):
        m = smallok.copy()
        for p in tup: m &= hit[p]
        return m
    def avail(tup): return [q for q in big if (not tup or q < tup[-1])]
    from functools import lru_cache
    @lru_cache(None)
    def Pref(r, lastidx, lower, root):
        # reference recursion (3.4) normalized by mu_d; state = gap r and set of available primes
        av = big if root else big[lastidx+1:]
        tot = 1.0
        for i, q in enumerate(av):
            idx = (big.index(q))
            if lower: tot -= Pref(r - x[q], idx, False, False)/q
            elif r - x[q] >= H(x[q]): tot -= Pref(r - x[q], idx, True, False)/q
        return tot
    def gap(tup):
        d = math.prod(tup) if tup else 1
        return math.log(Y/d)/lw - astar + 2, Y/d
    # stopped tree: stop at random lower nonroot nodes
    Tset = []; Sset = []
    def walk(tup):
        r, J = gap(tup); lower = len(tup) % 2 == 0
        if lower and tup and rng.random() < 0.35:
            Sset.append(tup); return
        Tset.append(tup)
        for q in avail(tup):
            if lower or r - x[q] >= Hstop(x[q]): walk(tup+(q,))
    walk(())
    Lstop = sum((-1)**len(t)*int(mask(t).sum()) for t in Tset)
    for t in Sset:
        m = mask(t)
        for q in avail(t): m &= ~hit[q]
        Lstop += int(m.sum())
    r0, _ = gap(())
    lhs = Lstop - Y*V0*Pref(r0, -1, True, True)
    rhs = sum((-1)**len(t)*(int(mask(t).sum()) - Y/math.prod(t or (1,))*V0) for t in Tset)
    for t in Sset:
        m = mask(t)
        for q in avail(t): m &= ~hit[q]
        r, J = gap(t); li = big.index(t[-1])
        rhs += int(m.sum()) - J*V0*Pref(r, li, True, False)
    return lhs, rhs, len(Tset), len(Sset)

if __name__ == "__main__":
    rng = random.Random(970)
    for (w, z, Y) in [(5, 60, 3000), (3, 40, 1500), (7, 90, 6000)]:
        for astar in [0.01, 0.5, 1.5]:
            res = run(w, z, Y, astar, 40, rng)
            resA = run(w, z, Y, astar, 3, rng, adversarial=True)
            print(f"w={w} z={z} Y={Y} a*={astar}: random fails={res['fails']} worst S1-L={res['worst_margin']}  "
                  f"adversarial fails={resA['fails']} worst={resA['worst_margin']}  minJ={min(res['minJ'],resA['minJ']):.2f} "
                  f"(w^a*={res['wa']:.2f})  (3.2) max viol={max(res['id32_maxviol'],resA['id32_maxviol'])}")
    print("control (i): admission test applied at LOWER nodes instead of upper:")
    for (w, z, Y) in [(5, 60, 3000), (3, 40, 1500)]:
        res = run(w, z, Y, 0.01, 40, rng, wrong_rule=True)
        print(f"  w={w} z={z}: fails={res['fails']} of 80, worst S1-L={res['worst_margin']}")
    print("comparison identity (3.5):")
    for (w, z, Y) in [(5, 60, 3000), (3, 40, 1500), (7, 90, 6000)]:
        lhs, rhs, nt, ns = comparison_identity(w, z, Y, 0.01, rng)
        lhs2, rhs2, _, _ = comparison_identity(w, z, Y, 0.01, rng, perturb=True)
        print(f"  w={w} z={z}: |T|={nt} |S|={ns}  lhs={lhs:.9f} rhs={rhs:.9f} diff={lhs-rhs:.2e} | perturbed-reference control diff={lhs2-rhs2:.3e}")
