# Hostile referee report: Claims 1 and 2 of CLAIMS.md (Erdős #912)

Referee: fresh Claude seat (Opus 5.5), 2026-11-10. I read CLAIMS.md (Claims 1–2), bf.c and its logs, re-proved everything by hand, and wrote my own checker (`/tmp/referee912/ref912.py`, source in the appendix). It shares no code with bf.c or hfast.c and recomputes Legendre's formula from scratch at every n; it does not update incrementally.

## Verdict: HOLDS WITH FIXES

The Lemma is correct, and so is its proof. The Theorem's *statement* is correct, but the proof has a real gap: one missing inequality, which I fix below in a few lines. One corollary is **false as written** at n+1 = 4. The identity is correct. I found no counterexample, either by hand or by computation, for any n ≤ 2·10^5, nor in 801 structured or random m ≤ 5·10^6.

---

## Objections, by severity

### O1 (gap in the proof of Theorem (b); the statement survives)
> "(b) … h(m) − h(n) = [no prime p ≠ Q has e_n(p) = k] − [k ≥ 2 and no prime p ≠ Q has e_n(p) = k−1]."
> "… so they contribute |S_small| to both h(n) and h(m) and never share a value. On the other primes, e_m = e_n except at Q … Moving one element changes the number of distinct values by [k new] − [k−1 vacated]."

The proof splits off the small prime factors S_small = {q | m : q² ≤ m} and then counts over the remaining primes T = (primes) ∖ S_small. What the argument actually proves is

  Δh = [k ∉ O] − [k ≥ 2 and k−1 ∉ O],  O = {e_n(p) : p ∈ T∖{Q}} ∖ {0}.

The statement instead quantifies over **all** primes p ≠ Q, and that set includes S_small. The two versions agree only if no small factor q of m has e_n(q) ∈ {k−1, k}. That is not cosmetic. If some q ∈ S_small had e_n(q) = k, isolation would make q the *only* holder of k at time n. Then [k ∉ O] = 1 while the stated indicator is 0, and the stated formula would be wrong by 1. The proof never rules this out.

- **k−1 is covered by isolation.** For k ≥ 2, Q ≤ m/2 ≤ n and e_n(Q) = k−1. Since q is isolated at x = n, e_n(q) ≠ e_n(Q).
- **k is NOT covered by isolation.** Isolation together with monotonicity only gives e_n(q) > e_n(Q) = k−1, i.e. e_n(q) ≥ k. Strictness needs an extra argument.

**Fix (add to the proof).** Let q ∈ S_small. Since q | m = kQ and q ≠ Q, q | k. So m ≥ qQ > q², hence n ≥ q², and
  e_n(q) ≥ ⌊n/q⌋ + ⌊n/q²⌋ ≥ (m/q − 1) + 1 = m/q = (k/q)·Q ≥ Q > k.
Here ⌊(m−1)/q⌋ = m/q − 1 because q | m, and Q > k because Q² > m = kQ. Therefore e_n(q) ∉ {k−1, k}, and "no prime p ≠ Q" = "no prime p ∈ T∖{Q}" = "no prime p ∤ m".

*Computation:* in 146,708 case-(b) steps (m ≤ 2·10^5), no small factor ever held k (0) or k−1 (0). The bound e_n(q) ≥ m/q never failed, and it held with **equality** 2,013 times, so it cannot be tightened in general. Both readings of the rule (all p ≠ Q, or p ∤ m) gave 0 failures.

### O2 (corollary false as stated)
> "h moves only at n+1 = kQ, Q prime > √(n+1)."

Counterexample: n = 3. 3! = 2·3 has exponents {1,1}, so h(3) = 1. 4! = 2³·3 has exponents {3,1}, so h(4) = 2. Yet 4 = 2² has no prime factor > √4 = 2. This is the excluded m = 4 of the Theorem, but the corollary drops that exclusion. **Fix:** "… only at n+1 = 4 or n+1 = kQ with Q prime, Q² > n+1." My data: the only step with Δh ≠ 0 and no large factor is (m, Δ) = (4, +1).

### O3 (omission in the Theorem's proof)
> "For every n ≥ 1, |h(n+1) − h(n)| ≤ 1. Exactly, with m = n+1 ≠ 4: …"

The proof only covers m ≠ 4. **Fix:** add "m = 4: h(3) = 1, h(4) = 2, Δ = +1." Note that case (a) would predict 0 here, which is why m = 4 must be excluded from the rule.

### O4 (expository: Lemma proof, all inequalities checked, none wrong)
- (a) and (b)(i) compare only the i = 1 terms:
  > "(a) e_x(q⁻) − e_x(q) ≥ ⌊x/q⁻ − x/q⌋"

  Say explicitly that Σ_{i≥2}(⌊x/q⁻^i⌋ − ⌊x/q^i⌋) ≥ 0 because p ↦ ⌊x/p^i⌋ is non-increasing. With that, ⌊a⌋ − ⌊b⌋ ≥ ⌊a−b⌋ is correct (a−b = (⌊a⌋−⌊b⌋) + ({a}−{b}) < ⌊a⌋−⌊b⌋+1). Also x/q⁻ − x/q = x(q−q⁻)/(q⁻q) ≥ x/(q⁻q), and q⁻q ≤ (q−1)q = q²−q ≤ x+1−q ≤ x. All correct.
- (b)(i): qq⁺ < q⁺² ≤ x gives ⌊x/(qq⁺)⌋ ≥ 1. Correct, but the hypothesis is stronger than needed (qq⁺ ≤ x suffices).
- (b)(ii) and (iii) need e_x(q⁺) = ⌊x/q⁺⌋, i.e. q⁺² > x. In (ii) this is the case condition. In (iii) it holds because q⁺² > q² = x+1. State it.
- (b)(ii) with q⁺ > x **cannot occur**: Bertrand gives q⁺ < 2q ≤ q² ≤ x. Even if it did, e_x(q⁺) = 0 < 1 ≤ e_x(q). Harmless either way.
- (iii): x = q²−1 gives ⌊x/q⌋ = q−1 and e_x(q) ≥ q−1. For q odd, q⁺ ≥ q+2. q²−1 = (q+2)(q−2) + 3 and 3 < q+2 for q ≥ 2, so ⌊(q²−1)/(q+2)⌋ = q−2. Correct. Example q = 3, x = 8: e_8(3) = 2, e_8(5) = 1.
- q = 2: there is no q⁻. Only (b) is needed: x ≥ 4 falls under (i) or (ii); (iii) means x = 3, which is excluded, and correctly so (e_3(2) = e_3(3) = 1; my code confirms (2,3) is not isolated). q = 3: q⁻ = 2, x ≥ 8. Fine.
- Uniqueness: the step "non-increasing along the primes + strict drop on both sides ⇒ unique" is applied correctly. It covers primes p > x too: e_x(p) ≤ e_x(q⁺) < e_x(q), and e_x(q) ≥ 1 because q² ≤ x+1 ⇒ q ≤ x. So an exponent of 0 never collides.

### O5 (expository: Theorem proof, implicit steps to make explicit)
- At most one prime factor exceeds √m (two would multiply to more than m). k = m/Q < Q, so **v_Q(m) = 1**. Q² > m > n gives e_n(Q) = ⌊n/Q⌋ = ⌊(kQ−1)/Q⌋ = k−1 and e_m(Q) = ⌊m/Q⌋ = k. Correct.
- Small factors satisfy q ≤ m/2 ≤ n, so e_n(q) ≥ 1 and q is counted in h(n).
- The Lemma applies at x = n because q² ≤ m = n+1, which is exactly why the Lemma carries "x+1". At x = m it applies because q² ≤ m ≤ m+1. The pair (q,x) = (2,3) is impossible at x = m (2 ∤ 3), and at x = n it forces m = 4. Correct.
- The case Q = m prime (k = 1): "vacated value 0" is uncounted, matching the [k ≥ 2] guard. Correct.
- Small primes NOT dividing m do not move, so they belong in O and in T. Fine.

### O6 (corollary for prime n+1: correct, slightly under-argued)
> "h(n+1) = h(n) when n+1 ≥ 5 is prime (Bertrand gives a prime with exponent 1)"

Spell it out. Bertrand gives a prime p ∈ (n/2, n] for n ≥ 2, so ⌊n/p⌋ = 1. Then p > n/2 ⇒ p² > n²/4 ≥ n for n ≥ 4, so e_n(p) = 1. And p ≤ n < m, so p ≠ Q. The corollary also holds for n+1 = 3 (p = 2, e_2(2) = 1); only n+1 = 2 moves (+1). My data: every prime m ≥ 3 had Δ = 0.

### O7 (instruments: bf.c tests what it claims, with caveats)
- **Rule prediction is pre-step.** `pred` is computed before the "apply the step" block, from pre-step `cnt`. Confirmed. `cnt[k]==0` counts all primes, small factors included, so bf tests the **statement as written** (the stronger form in O1), which is good. `cnt[k-1]==1` stands in for "no p ≠ Q at k−1" and presumes e_n(Q) = k−1 without checking it. The d == pred comparison would still expose an error except by coincidence. Recommend `assert(e[Q] == k-1)` before predicting. (My checker asserts e_n(Q) = k−1, e_m(Q) = k and v_Q(m) = 1: 0 failures.)
- **Isolation check is not vacuous**, but its scope is narrow. `cnt[e[q]]==1` counts q itself, so it fails exactly when another prime shares q's value. If e[q] were 0, cnt[0] = 0 would also fail. However it checks only q | m with q² ≤ m, at x = n and at x = m. Those are exactly the instances the Theorem uses, **not the Lemma in full** (every prime q with q² ≤ x+1, at every x). The identity needs every p ≤ √n to be isolated at x = n, and bf's check does not test that; it is tested only indirectly through hfast = bf. My checker tests the full Lemma: 12,177,306 instances (q,x), x ≤ 2·10^5, 0 failures.
- "isolation 242,570,204 checks" counts (m,q) pairs. Each pair is checked twice (before and after).
- Mutants: MUT_RULE removes only the "vacate" term. No mutant removes the "insert" term. ISOMUL=4 fires partly on q = Q, which is not a small factor; it still proves the code path can go red. My mutants on m ≤ 2·10^5: drop-vacate gives 27,336 failures, drop-insert gives 27,679.
- Off by one: the loop is m = 2..N, so it covers steps n → n+1 for n ≤ 10^8 − 1. "every n ≤ 10^8" in CLAIMS should read "every n < 10^8" (or "n+1 ≤ 10^8").
- Cross-check: I ran the existing `bf` binary with N = 2·10^5, writing only to /tmp: up = 6495, down = 6151, zero = 187353, 0 failures. My independent code gives **identical** up/down/zero counts.

---

## Identity h(n) = π(√n) + #{⌊n/p⌋ : √n < p ≤ n}: HOLDS
For p ≤ √n we have p² ≤ n ≤ n+1, and (2,3) is impossible since 4 > 3, so the Lemma isolates each such p at x = n. Their exponents are pairwise distinct and distinct from all others (and in fact exceed them, by the strict drop at the largest p ≤ √n). For p > √n, p² > n, so e_n(p) = ⌊n/p⌋. Hand table for n = 1..10:

| n | exponents | h | π(√n) | J | ok |
|---|---|---|---|---|---|
| 1 | – | 0 | 0 | 0 | ✓ |
| 2 | 1 | 1 | 0 | 1 | ✓ |
| 3 | 1,1 | 1 | 0 | 1 | ✓ |
| 4 | 3,1 | 2 | 1 | 1 | ✓ |
| 5 | 3,1,1 | 2 | 1 | 1 | ✓ |
| 6 | 4,2,1 | 3 | 1 | 2 | ✓ |
| 7 | 4,2,1,1 | 3 | 1 | 2 | ✓ |
| 8 | 7,2,1,1 | 3 | 1 | 2 | ✓ |
| 9 | 7,4,1,1 | 3 | 2 | 1 | ✓ |
| 10 | 8,4,2,1 | 4 | 2 | 2 | ✓ |

## Counterexample hunting (by hand)
- m = q·q⁺ (q just below √m, Q = q⁺ just above): k = q, and the small factor has e_n(q) ≥ m/q = q⁺ > k (O1 bound), so there is no clash at k or k−1.
- m = q² (the x+1 = q² boundary, Lemma case (iii)): this fails only for q = 2 (m = 4), which is excluded and accounted for.
- Two prime factors of m both near √m: at most one can exceed √m, and the other has q² ≤ m, so it is isolated.
- Sharpness of the Lemma's hypothesis, from my negative control (the first prime with q² > x+1): 9 non-isolated cases with x ≤ 2·10^5, all with x ≤ 65. Example: x = 14, q = 5 has e_14(5) = e_14(7) = 2. So q² ≤ x+1 cannot be loosened much, and the isolation instrument can fire.

## My computation
Independent Python and numpy. Eratosthenes, checked against sympy `primerange`. Full Legendre for **every** prime ≤ n, recomputed at **every** n with no incremental state, and checked against `sympy.factorint(n!)` for n ≤ 400 (exponent maps identical). m was factored with sympy `factorint`, not my sieve.

Exhaustive, every n ≤ 2·10^5 (817 s):
- h agrees with the OEIS A071626 b-file: 10000/10000. h(10)=4, h(100)=11, h(10^3)=31, h(10^4)=87, h(10^5)=252, h(2·10^5)=344.
- |Δh| ≤ 1: 0 failures. Steps: up 6495, down 6151, zero 187353 (= bf).
- Jump rule: 199,999 steps (53,291 case (a), 146,708 case (b)), 0 failures, with m = 4 as the only exception (Δ = +1). The p ∤ m variant also gives 0 failures.
- e_n(Q) = k−1, e_m(Q) = k, v_Q(m) = 1: 0 failures. Two prime factors > √m: never.
- Isolation of small factors at both x = n and x = m: 0 failures. Full Lemma (strict drop on both sides and uniqueness): 0/12,177,306 failures. Monotonicity: 0 failures.
- Identity: 0 failures. Heyman–Miraj #{⌊n/p⌋ : p ≤ n}: 0 failures.
- Prime m ≥ 3 ⇒ Δ = 0: 0 exceptions.

Targeted: 801 values of m ≤ 5·10^6 (structured q·q⁺, q², q²+q, 2q·q⁺, plus uniform in [2.5·10^6, 5·10^6), seed 912), with h recomputed from scratch at m−1 and m. 0 failures of any kind. 373,962 Lemma instances. Steps: up 12, down 5, zero 784.

## Summary of required edits
1. Add the O1 inequality e_n(q) ≥ m/q ≥ Q > k (and the isolation argument for k−1) to the proof of (b).
2. Corollary 2: add "or n+1 = 4".
3. Theorem proof: add the m = 4 line (h(3) = 1, h(4) = 2).
4. Optional: the expository additions in O4–O6. In bf.c, assert e[Q] == k−1 and add an "insert-term" mutant. Fix "n ≤ 10^8" → "n < 10^8".

---
## Appendix: referee script (`/tmp/referee912/ref912.py`)
Runs: `python3 ref912.py exh 200000` ; `python3 ref912.py rand 5000000 800 912`

```python
#!/usr/bin/env python3
# ref912.py — independent referee check of CLAIMS.md Claims 1-2 (Erdos #912).
# Written from scratch; does not reuse bf.c / hfast.c. Not incremental: e_n(p) is
# recomputed from Legendre's formula at every n, for every prime p <= n.
# mode "exh N": every n <= N.   mode "rand M T seed": T random + structured m <= M.
import sys, math, time, random
import numpy as np
from sympy import factorint, factorial, primerange, isprime

mode = sys.argv[1]
LIM = int(sys.argv[2]) + 2
sv = np.ones(LIM + 1, dtype=bool); sv[:2] = False
for i in range(2, math.isqrt(LIM) + 1):
    if sv[i]: sv[i*i::i] = False
P = np.nonzero(sv)[0].astype(np.int64)
if LIM <= 3_000_000:
    assert list(P) == list(primerange(2, LIM + 1)), "own sieve disagrees with sympy"

def legendre(n):
    """e_n(p) = sum_i floor(n/p^i) for every prime p <= n (full sum, all i)."""
    k = int(np.searchsorted(P, n, side='right'))
    Pk = P[:k]
    e = n // Pk
    pw = Pk * Pk
    L = k
    while True:
        L = int(np.count_nonzero(pw[:L] <= n))   # p^i increasing in p => prefix
        if L == 0: break
        pw = pw[:L]
        e[:L] += n // pw
        pw = pw * Pk[:L]
    return e

class State:
    def __init__(self, n):
        self.n = n
        self.e = legendre(n)
        self.vals, self.cnts = np.unique(self.e, return_counts=True)
        self.h = len(self.vals)
    def count(self, v):
        i = int(np.searchsorted(self.vals, v))
        return int(self.cnts[i]) if i < len(self.vals) and self.vals[i] == v else 0
    def exp(self, p):
        if p > self.n: return 0
        i = int(np.searchsorted(P, p)); assert P[i] == p
        return int(self.e[i])

stats = dict(lemma_checks=0, lemma_fail=0, lemma23=0, ctl_checks=0, ctl_fail=0,
             mono_fail=0, ident_fail=0, hm_fail=0, step_fail=0, rule_fail=0, alt_rule_fail=0,
             up=0, down=0, zero=0, caseA=0, caseB=0, small_hits_k=0, small_hits_km1=0,
             small_bound_fail=0, small_bound_tight=0, two_big=0, vQ_fail=0, eQ_fail=0,
             prime_m_nonzero=0, mut_rule_fail=0, mut_first_fail=0, move_without_Q=[], iso_small_fail=0, rule_checked=0)

def lemma_and_identity(S):
    n, e = S.n, S.e
    k = len(e)
    if k == 0: return
    if np.any(np.diff(e) > 0): stats['mono_fail'] += 1
    Pk = P[:k]
    Lq = int(np.count_nonzero(Pk * Pk <= n + 1))
    idx = np.searchsorted(S.vals, e[:Lq])
    c = S.cnts[idx]
    for i in range(Lq):
        q = int(Pk[i])
        if (q, n) == (2, 3):
            stats['lemma23'] += int(c[i] != 1); continue
        stats['lemma_checks'] += 1
        down_ok = (i == 0) or (e[i-1] > e[i])
        nxt = e[i+1] if i + 1 < k else 0
        up_ok = e[i] > nxt
        if c[i] != 1 or not down_ok or not up_ok:
            stats['lemma_fail'] += 1
            if stats['lemma_fail'] < 10: print("LEMMA FAIL", n, q, flush=True)
    # negative control: the next prime after the Lemma's range (q^2 > n+1) is often NOT isolated
    if Lq < k:
        stats['ctl_checks'] += 1
        if S.cnts[np.searchsorted(S.vals, e[Lq])] != 1: stats['ctl_fail'] += 1
    # identity h(n) = pi(sqrt n) + #{floor(n/p) : sqrt n < p <= n}
    pis = int(np.count_nonzero(Pk * Pk <= n))
    J = len(np.unique(n // Pk[pis:]))
    if pis + J != S.h:
        stats['ident_fail'] += 1; print("IDENT FAIL", n, S.h, pis, J, flush=True)
    if len(np.unique(n // Pk)) != S.h: stats['hm_fail'] += 1

def step(Sn, Sm):
    n, m = Sn.n, Sm.n
    d = Sm.h - Sn.h
    if abs(d) > 1:
        stats['step_fail'] += 1; print("STEP FAIL", m, d, flush=True)
    stats['up' if d == 1 else 'down' if d == -1 else 'zero'] += 1
    f = factorint(m)
    bigs = [p for p in f if p * p > m]
    smalls = [q for q in f if q * q <= m]
    if len(bigs) > 1: stats['two_big'] += 1
    # isolation of small factors at both x=n and x=m
    for q in smalls:
        if m == 4: continue
        if Sn.count(Sn.exp(q)) != 1 or Sm.count(Sm.exp(q)) != 1: stats['iso_small_fail'] += 1
    if bigs:
        stats['caseB'] += 1
        Q = bigs[0]; k = m // Q
        if f[Q] != 1: stats['vQ_fail'] += 1
        if Sn.exp(Q) != k - 1 or Sm.exp(Q) != k: stats['eQ_fail'] += 1
        # statement as written: "no prime p != Q has e_n(p) = k" etc.
        ck = Sn.count(k) - (1 if Sn.exp(Q) == k else 0)
        ckm1 = (Sn.count(k - 1) - (1 if Sn.exp(Q) == k - 1 else 0)) if k >= 2 else None
        pred = int(ck == 0) - int(k >= 2 and ckm1 == 0)
        # variant over primes NOT dividing m (what the proof's 'moving one element' actually computes)
        sk = sum(1 for q in smalls if Sn.exp(q) == k)
        skm1 = sum(1 for q in smalls if Sn.exp(q) == k - 1) if k >= 2 else 0
        stats['small_hits_k'] += sk; stats['small_hits_km1'] += skm1
        for q in smalls:   # the missing lemma: e_n(q) >= m/q >= Q > k
            if Sn.exp(q) < m // q: stats['small_bound_fail'] += 1
            if Sn.exp(q) == m // q: stats['small_bound_tight'] += 1
        alt = int(ck - sk == 0) - int(k >= 2 and (ckm1 - skm1) == 0)
        stats['rule_checked'] += 1
        if d != pred and m != 4:
            stats['rule_fail'] += 1; print("RULE FAIL", m, d, pred, flush=True)
        if d != alt and m != 4: stats['alt_rule_fail'] += 1
        if m != 4 and d != int(ck == 0): stats['mut_rule_fail'] += 1        # mutant: drop vacate term
        if m != 4 and d != -int(k >= 2 and ckm1 == 0): stats['mut_first_fail'] += 1  # mutant: drop insert term
        if isprime(m) and m >= 3 and d != 0: stats['prime_m_nonzero'] += 1
    else:
        stats['caseA'] += 1
        stats['rule_checked'] += 1
        if d != 0:
            stats['move_without_Q'].append((m, d))
            if m != 4:
                stats['rule_fail'] += 1; print("RULE(a) FAIL", m, d, flush=True)

t0 = time.time()
if mode == "exh":
    N = int(sys.argv[2])
    # Legendre cross-check against sympy's factorisation of n! itself (n <= 400)
    for n in range(1, 401):
        fe = factorint(factorial(n))
        hs = len(set(fe.values()))
        S = State(n)
        assert hs == S.h, (n, hs, S.h)
        assert dict(zip(map(int, P[:len(S.e)]), map(int, S.e))) == {int(a): int(b) for a, b in fe.items()}
    print("legendre == factorint(n!) for n<=400", flush=True)
    H = [0] * (N + 1)
    prev = State(1); H[1] = prev.h
    lemma_and_identity(prev)
    for m in range(2, N + 1):
        cur = State(m); H[m] = cur.h
        lemma_and_identity(cur)
        step(prev, cur)
        prev = cur
        if m % 50000 == 0: print("..", m, round(time.time() - t0), flush=True)
    # OEIS A071626 b-file
    bad = 0; tot = 0
    for line in open('/home/exedev/MathDyad/erdos912/sources/A071626_b071626.txt.out'):
        a = line.split()
        if len(a) == 2 and a[0].isdigit():
            i, v = int(a[0]), int(a[1])
            if i <= N: tot += 1; bad += (H[i] != v)
    print("OEIS A071626 b-file: %d/%d match" % (tot - bad, tot))
    print("h(1..12) =", H[1:13])
    for x in (10, 100, 1000, 10000, 100000, 200000):
        if x <= N: print("h(%d) = %d" % (x, H[x]))
else:
    M, T, seed = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rng = random.Random(seed)
    ms = set()
    qs = list(primerange(2, math.isqrt(M) + 1))
    for q in qs:                       # structured families
        qp = int(P[np.searchsorted(P, q, side='right')])
        for m in (q * qp, q * q, q * q + q, 2 * q * qp):
            if 5 <= m <= M: ms.add(m)
    ms = sorted(ms)
    ms = [ms[i] for i in sorted(rng.sample(range(len(ms)), min(T // 2, len(ms))))]
    ms += [rng.randrange(M // 2, M) for _ in range(T // 2)]
    ms += [int(p) for p in (P[np.searchsorted(P, M // 2)], )]   # a prime m
    for m in sorted(set(ms)):
        Sn, Sm = State(m - 1), State(m)
        lemma_and_identity(Sn); lemma_and_identity(Sm)
        step(Sn, Sm)
    print("random/structured m count:", len(set(ms)))
stats['time_s'] = round(time.time() - t0)
for k, v in stats.items(): print(k, v)
```
