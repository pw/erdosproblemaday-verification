# Hostile referee report: Theorem 2 (moves of h have density 0; Eldar's Conjecture 2 is false)

Referee: the Claims 1–2 referee seat (Opus 5.5), 2026-11-10. I checked the write-up line by line against the jump rule (Claim 2(b), with O1–O6 applied). I re-derived every inequality and recomputed the data near 10^9 with my own sieve (`/tmp/referee912/thm2_check.py`, appendix). I also fetched OEIS A357385 through Hetzner (exe.dev gets 403).

## Verdict: HOLDS WITH FIXES

The argument is unconditional and correct: the jump rule, a pigeonhole count over prime gaps, and the Selberg upper-bound sieve for prime pairs. It assumes nothing beyond what has been proved. One sentence is false as written: the sieve bound fails for odd d. One inequality is off by a constant. The sieve citation is unverified. The heuristic "≈" is contradicted by the data by about 36% at 10^9. None of these touches the conclusion.

**OEIS check (verbatim, via `oeis.org/search?q=id:A357385&fmt=text`).** "%N a(n) = A071626(n+1) − A071626(n)." "2) The asymptotic density of the occurrences of 0 is 0.943..., and the asymptotic densities of the occurrences of -1 and 1 are equal and the common value is 0.028... ." Offset 1. _Amiram Eldar_, Sep 26 2022. Theorem 2 gives density of 0 equal to 1, and densities of −1 and +1 both equal to 0. That refutes Conjecture 2 (its "equal" clause survives trivially; the "0.943" and "0.028" clauses fail). Eldar's 0.943 is the finite-range share at 10^7: 9,434,309/10^7.

---

## Objections (quoted), in order of weight

### T1. The sieve bound as stated is false for odd d (needs a one-word fix)
> "uniformly for 1 ≤ d ≤ x, #{q ≤ x : q, q+d both prime} ≪ 𝔖(d) x/log² x"

With the usual convention 𝔖(d) = 0 for odd d, the right side is 0. But q = 2 gives count 1 whenever 2 + d is prime (d = 1: the pair (2, 3)). **Fix:** either count only q ≥ 3, or restrict to even d, or write "≪ 𝔖(d)x/log²x + 1". In the application Q > √N and p > √n are both odd, so odd d contribute nothing. HR's prime-pair theorem is, as far as I know, stated for even h anyway.

### T2. Citation not verified; uniformity should be justified, not just cited
> "(Halberstam–Richert, Thm 3.11)"

I could not open *Sieve Methods* (a web search did not surface the statement), so I cannot confirm the theorem number, or that its O-term is uniform in h. The bound itself is standard and genuinely uniform. **Recommend** quoting the theorem verbatim after checking it, or adding the two-line justification:

- Apply the Selberg sieve to A = {q(q+d) : q ≤ x} with ω(p) = 2 for p ∤ d and ω(p) = 1 for p | d.
- Then |A_e| = xω(e)/e + O(ω(e)), with remainder independent of d.
- This gives S(A, x^{1/4}) ≤ x/G(x^{1/4}) + O(x^{1/2+ε}) with G(z) ≫ 𝔖(d)^{−1} log² z, all constants absolute.
- Add π(x^{1/4}) for q ≤ z. That term is negligible here too: Σ_k D_k (N/k)^{1/4} ≪ N/log N.

### T3. "log(N/k) ≥ ½ log N" is false by a constant
> "With Q ≤ 3N/k and log(N/k) ≥ ½ log N"

For k = √(2N) we get N/k = √(N/2) < √N. **Fix:** "log(N/k) ≥ ⅓ log N for N ≥ 8", or use x = 2N/k ≥ √(2N), so log x ≥ ½ log N. Also Q ≤ 2N/k; the "3N/k" is merely loose.

### T4. Gap-adjacency count: correct; make two steps explicit
> "So Q is adjacent to a prime gap of length ≥ G_k ≥ N/(2k²)."

- The A side: A ⇒ Q⁻ ≤ ⌊n/(k+1)⌋. Since Q = (n+1)/k, Q − Q⁻ ≥ (n+1)/k − n/(k+1) = (n+k+1)/(k(k+1)) > n/(k(k+1)) ≥ N/(2k²). ✓
- The B side: B ⇒ Q⁺ > n/(k−1), so Q⁺ − Q > (n−k+1)/(k(k−1)) ≥ N/k² − 1. That is ≥ N/(2k²) **only if k ≤ √(N/2)**. This holds for k ≤ L, but say so.

> "the gaps are disjoint, so at most 2(ℓ/G + 2) = 4k + O(1) such Q."

✓, with these spelled out:
- Consecutive-prime gaps have disjoint interiors.
- At most ℓ/G long gaps lie inside the Q-interval, plus at most 2 that straddle its ends.
- Each gap has 2 endpoints.

With ℓ = N/k + 1 we get ℓ/G ≤ 2k + 2k²/N ≤ 2k + 1, so the honest constant is **≤ 4k + 6**. (Sharper still: A-type Q are right endpoints and B-type Q are left endpoints, giving ≤ 2(ℓ/G + 1).)

### T5. Small-prime boundary: correct; one implicit converse
> "A prime p ≤ √n has e_n(p) ≥ ⌊√n⌋, so it can hold k or k−1 only if k ≥ ⌊√n⌋ − 1, i.e. Q ≤ √m + O(1). There are O(√N) such m"

✓. e_n(p) ≥ ⌊n/p⌋ ≥ ⌊√n⌋, so the threshold k ≥ ⌊√n⌋ already suffices (the stated −1 is safe). Q ≤ (n+1)/(√n − 2) = √n + 2 + o(1). For each prime Q in (√N, √(2N) + 3], only O(1) values of k remain, so the count is O(√N/log N), better than claimed.

> "Otherwise every prime with exponent k or k−1 is > √n, with exponent ⌊n/p⌋."

The argument also uses the **converse**: every prime in the windows (⌊n/(k+1)⌋, Q−1] and (Q, ⌊n/(k−1)⌋] has exponent k, resp. k−1. That needs the windows to lie above √n, i.e. n/(k+1) ≥ √n. This holds because k + 1 < ⌊√n⌋ off the discarded set. Say it.

### T6. Region k > L: correct
> "p ∈ (n/(k+1), n/(k−1)] and |p − Q| ≤ D_k ≤ 5N/k²"

✓ for k ≥ 3: 2n/(k²−1) < 4N/(k²−1) ≤ 5N/k² ⇔ k² ≥ 5. Also d ≤ D_k ≤ 2N/k = x for k ≥ 3, so the "d ≤ x" range of the sieve applies.

- Q − d prime is the same as q = Q − d with q + d prime, so a factor of 2 covers it. ✓
- **Σ_{d≤D} 𝔖(d) ≪ D holds for every D > 0**, including D < 2 (the sum is then 0). Proof: 𝔖(d) ≤ 2C₂ Σ_{e|d, e odd squarefree} g(e) with g(p) = 1/(p−2). So Σ_{d≤D} 𝔖(d) ≤ 2C₂ D Σ_e g(e)/e = 2C₂ D ∏_{p>2}(1 + 1/(p(p−2))) < ∞. ✓
- In this range D_k ≥ 5N/(2N) = 5/2 anyway, so the "max(D_k, 1)" is redundant.
- Sums: Σ_{k>L} N²/(k³ log²N) ≤ N²/(2L² log²N) = N/(2 log N) ✓. The redundant Σ_{k≤√(2N)} N/(k log²N) = N/(2 log N) ✓.
- Note: the sieve is essential here, not decorative. The trivial bound π(2N/k) summed over L < k ≤ √(2N) gives ≍ (N/log N)·log log N.

### T7. Assembly: correct
- Every m ∈ (N, 2N] with a move has k ≥ 2 and k < Q ⇒ k < √m ≤ √(2N). The ranges k ≤ L, L < k ≤ √(2N), and the discarded set cover everything. ✓
- "exactly one of A, B" ⇔ Δ ≠ 0 for k ≥ 2 (Δ = [A] − [B]). ✓
- Dyadic sum: Σ_j (X/2^j)/log(X/2^j) ≪ X/log X. Split at 2^j = √X; the tail is ≤ √X. ✓ Implied constants are uniform for N ≥ N₀; finitely many small m contribute O(1).
- Nothing conditional is used: no Cramér model, no Hardy–Littlewood, no short-interval PNT. ✓
- Label: "By Theorem (ii)" should be "(b)" in CLAIMS' numbering.

### T8. Heuristic constant: the "≈" is not supported at accessible n
> "The heuristic constant (Poisson/Cramér) is 2 log 2: share ≈ 2 log 2/log n."

As a *limit* heuristic I re-derive it:
- Move ⇔ exactly one of the two adjacent windows is empty, with P ≈ 2e^{−λ}(1 − e^{−λ}), λ ≍ N/(k² log(N/k)).
- Then Σ_k (N/(k log(N/k)))·f(λ_k) ≈ (N/log(N/k))·∫₀^∞ (e^{−λ} − e^{−2λ})/λ dλ = log 2 · N/log(N/k) ≈ 2 log 2 · N/log N (Frullani).

But at 10^9 the observed share is **4.28%** (my count on (9·10^8, 10^9]), while 2 log 2/log(10^9) = **6.69%** (ratio 0.64). Your own finite-n Cramér value (move_density.log) is 5.60%, which also overshoots by about 31%. The implied c(n) = share × (mean log n) climbs only slowly: ≈ 0.70, 0.73, 0.88, 0.84, 0.89 over the five decades 10^4–10^9. **Fix:** say "heuristically ~ 2 log 2/log n as n → ∞; at n ≈ 10^9 the observed share is about 0.64 of that". Do not set the data beside "≈". The Theorem is an upper bound only; no matching lower bound is proved.

### T9. The data split: totals reproduced exactly, the k ≤ L / k > L split not
> "Data: decade shares 6.40, 5.54, 5.66, 4.74, 4.44% … near 1e9 moves with k ≤ L are 0.40% of steps and with k > L 3.86%."

- All five decade shares recompute exactly from `bf_1e9.log`.
- My independent count for (10^8, 10^9] matches bf **to the unit**: up 19,989,802, down 19,977,738, share 4.4408%. Method: own sieve to 10^9, π(10^9) = 50,847,534 asserted; every m = kQ with Q prime > k; jump rule with exact Legendre fix-up for primes ≤ √n in the 8,688 rows with k ≥ ⌊√n⌋ − 1.
- The 0.40/3.86 split depends on the L convention, and I could not reproduce it exactly:

  | block | L | k ≤ L | k > L | total |
  |---|---|---|---|---|
  | (5·10^8, 10^9] | 4,996 | 0.143% | 4.198% | 4.341% |
  | (5·10^8, 10^9] | 6,946 | 0.849% | 3.492% | 4.341% |
  | (9·10^8, 10^9] | 6,946 | 0.453% | 3.822% | 4.275% |
  | (9·10^8, 10^9] | 6,606 | 0.341% | 3.934% | 4.275% |

  Your total is 0.40 + 3.86 = 4.26%. **Fix:** state the window and the L used.

---

## Numerical check requested: #(moves with given k ≤ L) ≤ 4k + 4

Dyadic block (5·10^8, 10^9], N = 5·10^8, L = ⌊(N/log N)^{1/2}⌋ = 4,996. For every k = 2..L I counted Q with A ∨ B, which is the quantity the proof bounds (it upper-bounds moves).

- **0 violations of 4k + 4.** The largest ratio #(A∨B)/(4k+4) is 0.053, at k = 4,995 (1,053 Q with A∨B, 1,021 moves, 8,403 Q in range).
- With L = 6,946 the largest ratio is 0.103 on (5·10^8, 10^9] and 0.013 on (9·10^8, 10^9].
- **No moves at all for k < 2,659.** This is consistent with the proof: the needed gap N/(2k²) exceeds every prime gap near 10^9 once k is small.

| k | moves | #(A∨B) | #Q | 4k+4 |
|---|---|---|---|---|
| 2 | 0 | 0 | 12,676,549 | 12 |
| 100 | 0 | 0 | 316,066 | 404 |
| 1000 | 0 | 0 | 36,960 | 4,004 |
| 2000 | 0 | 0 | 19,494 | 8,004 |
| 3000 | 12 | 12 | 13,440 | 12,004 |
| 4000 | 265 | 266 | 10,310 | 16,004 |
| 4996 | 1,021 | 1,053 | 8,399 | 19,988 |

## Required edits
1. T1: restrict the sieve bound to q ≥ 3 / even d, or add "+1".
2. T2: verify and quote HR's theorem (number, even-h hypothesis, uniformity), or add the Selberg-sieve sketch.
3. T3: replace "log(N/k) ≥ ½ log N" with "≥ ⅓ log N" (or use x = 2N/k).
4. T4/T5: note k ≤ √(N/2) on the B side; constant 4k + 6; windows lie above √n.
5. T8: requalify the 2 log 2 sentence against the data.
6. T9: state the window and L for the 0.40/3.86 split.
7. Label "(ii)" → "(b)".

---
## Appendix: `/tmp/referee912/thm2_check.py`
(Run time ~130 s, ~1.5 GB. The L-convention variants reuse `block()` with other (lo, hi, L).)
```python
#!/usr/bin/env python3
# thm2_check.py — referee numerics for Theorem 2 (density of moves). Own sieve; uses the
# (proved, checked) jump rule: for m = kQ, Q prime > k (<=> Q^2 > m), k >= 2, with n = m-1,
#   A = no prime p != Q has e_n(p) = k,  B = no prime p != Q has e_n(p) = k-1;  up iff A&~B, down iff B&~A.
# Large primes (p > isqrt(n)) via windows; primes p <= isqrt(n) handled EXACTLY (Legendre) whenever
# k >= isqrt(n) - 1 (the only case where they can hold k or k-1).
import numpy as np, math, time, sys
X = 10**9
t0 = time.time()
size = X // 2 + 1
s = np.ones(size, dtype=bool); s[0] = False
for i in range(1, (math.isqrt(X) - 1) // 2 + 1):
    if s[i]:
        p = 2 * i + 1
        s[p * p // 2::p] = False
P = np.concatenate((np.array([2], dtype=np.int64), 2 * np.nonzero(s)[0].astype(np.int64) + 1))
P = P[P <= X]
del s
assert len(P) == 50847534, len(P)      # pi(10^9)
print("sieve ok", round(time.time() - t0), "s", flush=True)
pi = lambda x: np.searchsorted(P, x, side='right')

def leg(n, p):
    e = 0; t = p
    while t <= n: e += n // t; t *= p
    return e

def block(lo, hi, perk=False, Lk=0):
    up = down = 0; exc = 0
    per = {}
    K = math.isqrt(hi)
    for k in range(2, K + 1):
        a = max(k, lo // k); b = hi // k
        if b <= a: continue
        i0, i1 = int(pi(a)), int(pi(b))
        if i1 <= i0: continue
        Q = P[i0:i1]; idx = np.arange(i0, i1, dtype=np.int64)
        n = k * Q - 1
        r = np.floor(np.sqrt(n.astype(np.float64))).astype(np.int64)
        r -= (r * r > n); r += ((r + 1) * (r + 1) <= n)
        leftA = np.maximum(n // (k + 1), r)
        cntA = idx - pi(leftA)                       # primes in (leftA, Q-1]  (pi(Q-1) = idx)
        cntA = np.maximum(cntA, 0)
        cntB = pi(n // (k - 1)) - (idx + 1)          # primes in (Q, n//(k-1)]
        A = cntA == 0; B = cntB == 0
        ex = np.nonzero(k >= r - 1)[0]
        for j in ex:                                 # exact small-prime fix-up
            exc += 1
            nn = int(n[j]); rr = int(r[j])
            lo_p = nn // (k + 1)                     # small p with floor(n/p) <= k must exceed n/(k+1)
            for p in P[int(pi(lo_p)):int(pi(rr))]:
                v = leg(nn, int(p))
                if v == k: A[j] = False
                if v == k - 1: B[j] = False
        u = int(np.count_nonzero(A & ~B)); d = int(np.count_nonzero(B & ~A))
        up += u; down += d
        if perk and k <= Lk:
            per[k] = (u + d, int(np.count_nonzero(A | B)), len(Q))
        elif perk:
            per.setdefault('big', [0, 0]); per['big'][0] += u + d
    return up, down, exc, per

# 1) decade (1e8, 1e9] vs bf_1e9.log
u, d, exc, _ = block(10**8, 10**9)
print("decade (1e8,1e9]: up=%d down=%d moves=%d share=%.4f%%  exceptional-k rows=%d  (%ds)"
      % (u, d, u + d, 100 * (u + d) / 9e8, exc, round(time.time() - t0)), flush=True)
print("bf_1e9.log      : up=%d down=%d" % (22410411 - 2420609, 22392178 - 2414440), flush=True)

# 2) dyadic block (N, 2N], N = 5e8: per-k counts for k <= L, vs 4k+4
N = 5 * 10**8
L = int(math.sqrt(N / math.log(N)))
u, d, exc, per = block(N, 2 * N, perk=True, Lk=L)
small = sum(v[0] for k, v in per.items() if k != 'big')
big = per['big'][0]
print("block (5e8,1e9]: L=%d  moves=%d  k<=L: %d (%.3f%% of steps)  k>L: %d (%.3f%%)"
      % (L, u + d, small, 100 * small / N, big, 100 * big / N))
viol = [(k, v) for k, v in per.items() if k != 'big' and v[1] > 4 * k + 4]
print("k<=L with #(A or B) > 4k+4:", viol[:10], "count", len(viol))
first = min([k for k, v in per.items() if k != 'big' and v[0] > 0] or [None])
print("smallest k with a move:", first)
worst = max(((v[1] / (4 * k + 4), k, v) for k, v in per.items() if k != 'big'))
print("max over k<=L of #(A or B)/(4k+4) = %.4f at k=%d %s" % worst)
for k in (2, 100, 500, 1000, 1500, 2000, 3000, 4000, L):
    if k in per: print("  k=%d moves=%d #(AvB)=%d #Q=%d 4k+4=%d" % (k, per[k][0], per[k][1], per[k][2], 4 * k + 4))
print("time", round(time.time() - t0), "s")
```
