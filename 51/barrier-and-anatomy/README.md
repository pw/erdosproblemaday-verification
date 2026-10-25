# Erdős #51 — a barrier for "no", exact smooth-family least preimages, the ratio's anatomy (2026-10-21)

Entry: https://erdosproblemaday.com/day/51-a-no-answer-needs-smooth-shifted-primes. The entry is a partial result and ours; the problem stays OPEN.
It was produced by the 15:00Z erdos cron seat (Claude Opus 5.5, Team seat 3). ℓ(a) is the least n with φ(n) = a, and R(a) = ℓ(a)/a.

## Claims and labels

### (a) Barrier theorem
Let S be a finite set of primes that is φ-closed, meaning p−1 is S-smooth for every p ∈ S. Let Q_S = {primes q ∉ S : q−1 is S-smooth}, n_K = ∏_{p∈S} p^K and a_K = φ(n_K).

**Theorem.** If Q_S is finite, then ℓ(a_K) = n_K whenever K−1 > max_p Σ_{q∈Q_S} v_p(q−1).

- **S = {2}** is Carmichael 1907: ℓ(2^k) = 2^{k+1} for k ≥ 32 if no Fermat prime lies beyond F_4. We have this second-hand, via the zbMATH review of Gupta 1981 and OEIS A002181.
- **Corollaries:**
  - sup ℓ(a)/a < ∞ ⇒ some fixed y ≥ 3 has infinitely many primes p with p−1 y-smooth. No fixed y is known to have this; see Luca–Menares–Pizarro-Madariaga 2013, arXiv:1311.2527, p. 1.
  - ℓ(a) < 3a ∀a ⇒ infinitely many Pierpont primes.
  - ℓ(a) < 2.5a ∀a ⇒ infinitely many primes 2^α5^β+1, and ℓ(a) < 2.125a ∀a ⇒ the same for 2^α17^β+1.
  - No 3-seed ⇒ infinitely many primes 2^α3^β5^γ+1, with γ = 0 allowed. Equivalently, if Q_{2,3,5} is finite, a 3-seed exists. For S = {2,3,q} with q−1 3-smooth, the conclusion is only a disjunction.
- **Precursor:** Kovač's forum comment of 28 Aug 2025, linking the swaps to #203.
- **Proof:** on the entry, in `CLAIMS_working_notes.md` / `seats/CLAIMS_v1.md` (with addendum), and in the sharpened form in `seats/referee_math.md` §2.

### (a) Erdős 1979 implies YES
Erdős's "I hope that m′_X/m_X → 1" (Astérisque 61 p. 80, scan in `world/Er79e_p80.png`) implies a YES answer, because m_X ≫ X log log X and m′_X = max_{a≤X} ℓ(a).

### (a) The split R = T·W with T ≤ 2
- ℓ is never ≡ 2 mod 4 (a ≥ 2).
- If 4 | ℓ, no Fermat prime divides ℓ exactly once.
- Finite products of (1+2^{−2^s}) are below 2.

### (d) 3-smooth totients
Every 3-smooth totient 2^X3^Y with X ≤ 120 and 1 ≤ Y ≤ 80 has ℓ(a) < (2 + 10^−20)a. The exact maximum is 2 + 9.035·10^−21, at 2^98·3.

### (d) Diagonals
The diagonals are a_K = φ(∏_{p∈S}p^K).

| S | range of K | max R |
|---|---|---|
| {2,3} | K ≤ 40 | 13/12 (K = 2) |
| {2,3,5} | K ≤ 20 | 1.0240 |
| {2,5}, {2,3,7}, {2,3,13} | K ≤ 30 | ≤ 1.094 |
| {2,17} | K ≤ 30 | 1.328 |

### (d) 5-smooth totients
For 5-smooth totients with exponents up to (60,30,20) and odd part > 1, the maximum R is 15/8 + 3·2^−58, at 2^58·5. Every other cell is ≤ 1.6000000092. A first draft said "≤ 1.875"; the compute referee's exact pass corrected it.

### (d) Census
The census scanned n ≤ 2.5·10^9, which gives every totient ≤ 10^9.

- **Count:** 139,847,905, which equals V(10^9) from the #416 tick.
- **Max R:** 2.043447080 at 387,383,296, matching OEIS A393265.
- **Max W:** 1.583664159 at 559,789,704 (ℓ = 3^3·19^3·4787, T = 1).
- **Even least preimages:** only 6 below 10^9, at a = 2^16·257·2^j.
- **Second program:** the compute referee's `knap.c` reproduced all of this, with a byte-identical record list, and agrees per value for all a ≤ 4·10^7.

### (d) The July safe-marker chain
The chain from `july-report/` was re-checked by `bnb.py`, which is independent of the July DP.

- ℓ(17,776,474,638,307,328) = 3·5·17·47·347·1187·1367·5387, with R = 2.0449753841.
- The stage a = 3,300,496,590,848 has R = 2.0445958. That beats every value below 1.2·10^11, so the next term of A393265 is ≤ 3.3·10^12.
- No safe prime 5387 < p ≤ 6·10^6 extends the chain (`out/chain_safe.log`).
- A greedy extension over all primes was also started (`chain.py 200000 4`, 3,000 s cap). It is not on the page.

## Instruments and controls

- **Smooth families.** `smoothdp.py` (lattice DP, float costs, BPSW) was cross-checked three ways:
  - against `bnb.py` (branch-and-bound, exact integers) by `xcheck.py`, which sampled 600 points and 80 non-totients with 0 mismatches;
  - by `exact_top.py`, which recomputed the near-2 points exactly;
  - by `seats/compute_referee_code/exactdp.py`, the referee's exact-integer DP. Every free prime there is certified by Lucas–Pocklington from the factorization of q−1, and it agrees on EVERY cell of both lattices.
  
  Because of those certificates, the lattice upper bounds (claims of the form "≤") do not rest on BPSW.
- **Census.** `omega.c` (an increasing scan; the first hit is the least preimage) was checked against `seats/compute_referee_code/knap.c` (a multiplicative knapsack over primes, no scan). On the referee's mutations, the count-equals-V control certified coverage but missed the bugs that scrambled ℓ. The per-value comparison caught them.
- **Mutation tests.** These are in `seats/compute_referee_code/mut/`. Every planted bug that changes an output was caught by at least one check. M4, B4 and S1 change nothing on our data.
- **Guards added after review:**
  - `smoothdp.py` asserts that the base is all primes ≤ y (objection 1).
  - `bnb.py` asserts that the supplied factorization multiplies back to a (objection 3).
  
  Neither affects any published number, because every reported run used a complete, φ-closed base.

## Referee seats and what changed

- **`seats/referee_math.md`** — no hole found. What changed:
  - the theorem was sharpened to ℓ(a_K) = n_K;
  - credit to Carmichael and Kovač was added;
  - "open for every fixed y" became "no fixed y is known", with the LMP13 quote, which we verified from the arXiv PDF;
  - the y = 2 parenthetical was removed;
  - "consistent with Tao" replaced "the precise form of Tao's";
  - "YES needs" became "one route to YES";
  - the C6 disjunction was stated;
  - T < 2 is now justified by finiteness;
  - the reason given for the sup-equivalence was dropped.
- **`seats/referee_compute.md`** — all numbers reproduced. What changed:
  - the 5-smooth inequality was corrected;
  - the two guards above were added;
  - the README's primality wording was fixed;
  - the knap / exactdp cross-checks are now cited on the page.
- **`seats/blind_read.md`** — a blind read of the rendered page. Its fixes are listed at the end of that file.

## Notes

- `code/chain.py` was restructured after its first run (the search moved into `main()` so `chain_safe.py` can import `is_least`). The logic is unchanged.
- `census/records_1e7.tsv` is the record list from the 10^7 test run. The 10^9 records are in `census/records.tsv`.
- `world/world.md` is the literature seat's report, with each claim marked read, inferred or not read. Not read: Guy B36/B39/A18, [Er98], and Carmichael 1907 in the original.

## Reproduce

```
gcc -O2 -o omega code/omega.c -lm && ./omega 1000000000 2500000000          # ~12 min one core
cd code && python3 smoothdp.py 2,3 120,80 --odd --save R23.npy && python3 smoothdp.py 2,3,5 60,30,20 --odd --save R235.npy
python3 xcheck.py ; python3 exact_top.py ; python3 diag.py 3 40 ; python3 diag.py 5 20 ; python3 diag.py 2,17 30
python3 -c "from chain import main" ; python3 chain_safe.py 3000000
```

## Blind read (seats/blind_read.md) — fixes applied before deploy
- Title/H1 said bounded ratios ⇒ Pierpont primes; corrected to "ratios bounded below 3" (bounded alone gives some fixed y).
- "Every ratio record has T = 255/128" → "from a = 128 on" (records 3 and 15 have T = 3/2, 15/8).
- 3-smooth maximum is attained at every a = 3·2^X, 98 ≤ X ≤ 120 (no prime 3·2^j+1 for 67 ≤ j ≤ 188), not at one point.
- Title's "up to 2¹²⁰·3⁸⁰" (read as a size bound) → the exponent box X ≤ 120, Y ≤ 80.
- lim sup ≥ 2.043447 updated with the chain's 2.044975; the positive-proportion step labelled (b); "two instruments" → three;
  Guy A18 cited via erdosproblems.com/1055 (A18 itself not read); trivial-cover list completed (2.125); {2,17} diagonal
  is not "one to three huge primes"; the July chain starts with the Fermat primes; Tao quote ellipsis; the September 2026
  OpenAI preprint named; "refereed here" → "read by AI seats and Lean-replayed"; three hard-to-parse sentences rewritten.
