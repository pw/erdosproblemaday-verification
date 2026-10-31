#!/usr/bin/env python3
"""Seat P -- small-case structural checks for arXiv 2604.23784v3 (Bae).

SMALL-CASE EVIDENCE ONLY.  Independent of the paper's code / Lean.

For small M, h, K (2h < M < K < M^2) we build n = tL - h - 1 with
||tL||_p < h for every prime M < p <= K (t built by CRT with random signed
targets z_p in (-h,h), BOTH signs, plus a random high part), and for every
1 <= k <= K we
  * compute nu_p(C(n,k)) by Legendre's floor formula and compare with the
    Kummer residue form [n]_q < [k]_q (Lemma 2.1),
  * cross-check log u(n,k) against direct factorisation of C(n,k) for some k,
  * split the carries into the four ranges (I)-(IV) of Section 6 and test
      (I)   == sub-sum of the carries of C(h+k,h)   and  <= log C(h+k,h)
      (II)  carry at p  <=>  [k]_p >= p - d_p ;  p in I_m(k), m=floor(k/p)+1,
            2<=m<=A+1 ; contribution <= sum_m theta(I_m(k))  (exact primes)
      (III) <= sum_{M<p^a<=K, a>=2} log p
      (IV)  <= Z(t)
  * compare with the UNSHIFTED n' = tL - 1 to show why the shift matters.
"""
import math, random, sys

def primes_upto(N):
    s = bytearray([1]) * (N + 1); s[0:2] = b'\x00\x00'
    for i in range(2, int(N ** 0.5) + 1):
        if s[i]:
            s[i*i::i] = bytearray(len(range(i*i, N + 1, i)))
    return [i for i in range(N + 1) if s[i]]

def lcm_upto(M):
    L = 1
    for i in range(1, M + 1):
        L = L * i // math.gcd(L, i)
    return L

def legendre_nu(n, k, p):
    v, q = 0, p
    while q <= n:
        v += n // q - k // q - (n - k) // q
        q *= p
    return v

def kummer_levels(n, k, p):
    """list of a with [n]_{p^a} < [k]_{p^a}"""
    out, a, q = [], 1, p
    while q <= n:
        if n % q < k % q:
            out.append(a)
        a += 1; q *= p
    return out

def run(M, h, K, trials, seed):
    rng = random.Random(seed)
    assert 2 * h < M < K < M * M
    PR = primes_upto(K + 2 * h + 5)
    L = lcm_upto(M)
    P2 = [p for p in PR if M < p <= K]
    P = 1
    for p in P2: P *= p
    A = K / M
    theta = lambda a, b: sum(math.log(p) for p in PR if a < p <= b)  # theta(b)-theta(a)
    rangeIII = sum(math.log(p) for p in PR if p <= K for a in range(2, 64) if M < p ** a <= K)
    worst = {'I': 0, 'II': 0, 'III': 0, 'IV': 0}
    fails = []
    sign_stats = {'shift_pos': [], 'shift_neg': [], 'unshift_pos': [], 'unshift_neg': []}
    directs = 0
    for tr in range(trials):
        z = {p: rng.randint(-h + 1, h - 1) for p in P2}
        # CRT: t*L == z_p (mod p)
        t0 = 0
        for p in P2:
            Np = P // p
            coeff = (z[p] * pow(L, -1, p)) % p
            t0 = (t0 + coeff * Np * pow(Np, -1, p)) % P
        t = t0 + P * rng.randint(1, 10 ** 12)
        n = t * L - h - 1
        nprime = t * L - 1
        # signed rep check + d_p
        d = {}
        for p in P2:
            r = (t * L) % p
            s = r if r <= p // 2 else r - p
            if s != z[p] or abs(s) >= h:
                fails.append(('signed', p, s, z[p]))
            d[p] = h - s
            if not (1 <= d[p] <= 2 * h - 1):
                fails.append(('d_range', p, d[p]))
            if n % p != p - 1 - d[p]:
                fails.append(('nmodp', p))
            # sign statistics: # residues k mod p (k in [0,p)) producing a level-p carry
            cs = sum(1 for kk in range(p) if n % p < kk)
            cu = sum(1 for kk in range(p) if nprime % p < kk)
            key = 'pos' if s > 0 else 'neg'
            sign_stats['shift_' + key].append(cs / p)
            sign_stats['unshift_' + key].append(cu / p)
        # Z(t)
        Z = 0.0
        for p in PR:
            if p > K: break
            a, q = 1, p
            while q <= n:
                if a >= 2 and q > K and n % q < K:
                    Z += math.log(p)
                a += 1; q *= p
        for k in range(1, K + 1):
            contrib = {'I': 0.0, 'II': 0.0, 'III': 0.0, 'IV': 0.0}
            logu = 0.0
            for p in PR:
                if p > k: break
                lv = kummer_levels(n, k, p)
                if len(lv) != legendre_nu(n, k, p):
                    fails.append(('kummer', k, p))
                for a in lv:
                    q = p ** a
                    logu += math.log(p)
                    if q <= M: contrib['I'] += math.log(p)
                    elif a == 1 and q <= K: contrib['II'] += math.log(p)
                    elif q <= K: contrib['III'] += math.log(p)
                    else: contrib['IV'] += math.log(p)
                # (II) structural: carry at p (M<p<=k) iff [k]_p >= p - d_p
                if M < p <= K:
                    carry = (n % p) < (k % p)
                    if carry != ((k % p) >= p - d[p]):
                        fails.append(('II_iff', k, p))
                    if carry:
                        m = k // p + 1
                        if not (2 <= m <= A + 1 and k / m < p <= (k + 2 * h) / m):
                            fails.append(('II_interval', k, p, m))
            # (I): exact equality with the sub-sum of C(h+k,h) carries (p<=k, q<=M)
            subI = 0.0
            for p in PR:
                if p > k: break
                q = p
                while q <= M:
                    if (h % q) + (k % q) >= q: subI += math.log(p)
                    q *= p
            if abs(subI - contrib['I']) > 1e-9: fails.append(('I_identity', k))
            lbin = math.lgamma(h + k + 1) - math.lgamma(h + 1) - math.lgamma(k + 1)
            if contrib['I'] > lbin + 1e-9: fails.append(('I_bound', k))
            # (II) bound: sum over active m of theta(I_m(k)), exact
            act = set()
            for p in PR:
                if p <= M: continue
                if p > k: break
                if n % p < k % p: act.add(k // p + 1)
            boundII = sum(theta(k / m, (k + 2 * h) / m) for m in act)
            if contrib['II'] > boundII + 1e-9: fails.append(('II_bound', k))
            if contrib['III'] > rangeIII + 1e-9: fails.append(('III_bound', k))
            if contrib['IV'] > Z + 1e-9: fails.append(('IV_bound', k))
            if abs(sum(contrib.values()) - logu) > 1e-9: fails.append(('partition', k))
            worst['I'] = max(worst['I'], contrib['I'] / max(lbin, 1e-9))
            worst['II'] = max(worst['II'], contrib['II'])
            worst['III'] = max(worst['III'], contrib['III'])
            worst['IV'] = max(worst['IV'], contrib['IV'])
            # direct factorisation cross-check on a few k
            if tr == 0 and k in (1, 2, 7, M - 1, M + 1, K // 2, K):
                C = math.comb(n, k)
                lu = 0.0
                for p in PR:
                    if p > k: break
                    while C % p == 0:
                        C //= p; lu += math.log(p)
                if abs(lu - logu) > 1e-6: fails.append(('direct', k, lu, logu))
                directs += 1
    avg = lambda xs: (sum(xs) / len(xs)) if xs else float('nan')
    mx = lambda xs: max(xs) if xs else float('nan')
    print(f"M={M} h={h} K={K} A=K/M={A:.2f} trials={trials} #primes(M,K]={len(P2)} "
          f"log10 n ~ {math.log10(n):.1f} direct-factorisation checks={directs}")
    print(f"  failures: {len(fails)}  {fails[:5]}")
    print(f"  max over k,trials: (I)/log C(h+k,h)={worst['I']:.3f}  (II)={worst['II']:.2f}  "
          f"(III)={worst['III']:.2f} [bound {rangeIII:.2f}]  (IV)={worst['IV']:.2f}")
    print("  fraction of residues k mod p giving a level-p carry (mean / max):")
    for key in ('shift_pos', 'shift_neg', 'unshift_pos', 'unshift_neg'):
        print(f"    {key:12s} n={len(sign_stats[key]):4d}  mean={avg(sign_stats[key]):.3f}  max={mx(sign_stats[key]):.3f}")
    print(f"    (shifted bound (2h-1)/p <= {(2*h-1)/(M+1):.3f})")
    return len(fails)

if __name__ == '__main__':
    tot = 0
    for (M, h, K, T) in [(12, 2, 40, 30), (20, 3, 80, 20), (30, 3, 150, 10), (40, 4, 200, 6), (60, 5, 300, 3)]:
        tot += run(M, h, K, T, seed=M * 1000 + h)
    print("TOTAL FAILURES:", tot)
