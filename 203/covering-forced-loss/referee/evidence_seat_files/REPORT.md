# Erdős #203: evidence-seat recomputation (2026-10-12)

Everything below was recomputed from scratch with my own code in `/tmp/evidence203/scripts/`, run under `nice -n 19` with `~/.venv/bin/python` (sympy 1.14, numpy 2.4) and PARI/GP for cross-checks. I read nobody's argument before computing. The README and forum were read only at step 7. Every script finished in under 10 s. Nothing under `/home/exedev/MathDyad/erdos203/` was touched.

Notation: H_p = <2,3> ≤ (Z/p)^×, e_p = |H_p|, L_p = {(k,l): 2^k 3^l ≡ 1 mod p}, and pool(N) = {p ≥ 5 prime : e_p | N}.

## 1. The complete pools for N = 720, 5040, 55440

**Method (`pool.py`).**
- p | g_N := gcd(2^N − 1, 3^N − 1) ⇔ 2^N ≡ 3^N ≡ 1 (mod p) ⇔ exp(H_p) | N ⇔ e_p | N. The last step holds because H_p is cyclic, so its order equals its exponent, which is lcm(ord_p 2, ord_p 3).
- So pool(N) is exactly the set of prime factors of g_N; 2 and 3 never divide g_N.
- I split g_N by gcd with Φ_d(2) for d | N, factored each piece, and **certified completeness** by dividing every found prime out of g_N to full multiplicity and asserting that the cofactor is exactly 1.
- Primality: every prime is below 2^64, where sympy's `isprime` is deterministic. (Largest: 332641 for N = 55440; 11,321,831 overall in step 2.)

**Cross-checks.**
- PARI/GP (`xcheck.gp`): `factor(gcd(2^N-1,3^N-1))` gives the same sets and sums.
- An independent direct sieve over all primes p ≤ 10^7 (test 2^N ≡ 3^N ≡ 1 mod p) finds the identical sets below 10^7.

| N | g_N digits | #primes | Σ 1/e_p (exact) | ≈ |
|---|---|---|---|---|
| 720 | 25 | 15 | **641/720** | 0.890278 |
| 5040 | 68 | 31 | **143/140** | 1.021429 |
| 55440 | 148 | 55 | **21493/18480** | 1.163041 |

The lists below are p:e_p.

- **N = 720:** 5:4, 7:6, 11:10, 13:12, 17:16, 19:18, 31:30, 37:36, 41:40, 61:60, 73:36, 97:48, 181:180, 241:120, 577:144
- **N = 5040:** 5:4, 7:6, 11:10, 13:12, 17:16, 19:18, 29:28, 31:30, 37:36, 41:40, 43:42, 61:60, 71:35, 73:36, 97:48, 113:112, 127:126, 181:180, 211:210, 241:120, 281:280, 337:168, 421:420, 577:144, 631:630, 673:336, 1009:504, 2017:1008, 2521:1260, 3361:1680, 13441:1680
- **N = 55440:** the 31 primes above plus 23:11, 67:66, 89:88, 199:198, 331:330, 397:396, 463:462, 617:616, 661:660, 881:880, 991:990, 1321:660, 2311:2310, 2971:990, 3169:1584, 3697:1848, 4621:4620, 5281:2640, 7393:1848, 9241:2310, 18481:9240, 55441:4620, 110881:11088, 332641:55440

(ord_p 2 and ord_p 3 for each prime are in `pool_N.json`.)

## 2. Which N ≤ 5040 have Σ_{e_p | N} 1/e_p ≥ 1

**Method (`all_e_upto.py`, `densities.py`).**
- I took every prime with e_p ≤ 5040 by factoring g_d = gcd(2^d − 1, 3^d − 1) for every d ≤ 5040. This is complete because p | g_{e_p}, and each d was certified with cofactor = 1.
- Result: **1016 primes**, the largest being 11,321,831 (e = 3995). The largest g_d has 68 digits.
- I then computed density(N) = Σ_{d | N} n_d / d exactly, for every N ≤ 5040.
- GP cross-check (`xcheck2.gp`): the same 1016-prime set (compared element by element) and the same table.
- Sub-counts: 442 primes with e_p ≤ 2000 (Σ ≈ 1.973087) and 1006 with e_p ≤ 5000 (Σ ≈ 2.145535).

**Density ≥ 1: only N = 5040** (143/140).

**All N ≤ 5040 with density ≥ 0.9:**

| N | density | ≈ |
|---|---|---|
| 5040 | 143/140 | 1.021429 |
| 3960 | 739/792 | 0.933081 |
| 3600 | 3349/3600 | 0.930278 |
| 4320 | 83/90 | 0.922222 |
| 2520 | 2311/2520 | 0.917063 |
| 2160 | 1969/2160 | 0.911574 |
| 2880 | 2599/2880 | 0.902431 |
| 1440 | 1297/1440 | 0.900694 |

The next ones down are 3360 (3007/3360 ≈ 0.894940), 2640 (107/120), 3780 (1123/1260) and 720 (641/720).

## 3. e for products of two primes (`composite.py`)

I computed |<2,3> mod n| by closure (BFS).

| n | e_n | e_p · e_q | e_n = e_p e_q? |
|---|---|---|---|
| 35 | **24** | 4·6 = 24 | yes |
| 91 | **72** | 6·12 = 72 | yes |
| 55 | **40** | 4·10 = 40 | yes |

In each case <2,3> is the whole group (Z/n)^×.

Equivalent formulation: [Z² : L_p ∩ L_q] = e_{pq}, so [Z² : L_p + L_q] = e_p e_q / e_{pq} = 1. Every coset of L_p meets every coset of L_q.

Extra checks:
- Not every pair behaves this way. **e_143 = 60 ≠ 120**, so cosets of L_11 and L_13 can be disjoint. Likewise e_119 = 48 ≠ 96 (7 and 17).
- e_65, e_77, e_85, e_187 and e_221 do equal the products.
- e_5005 = 720 (vs 2880), and e_85085 = 2880 (vs 46080).

## 4. Primes 5 and 7 (`cosets.py`)

Derivation: take a generator g of the cyclic group H_p and write 2 = g^a, 3 = g^b. Then L_p = {ak + bl ≡ 0 (mod e_p)} and the cosets are {ak + bl ≡ c}.

- **L_5 = {(k,l): k + 3l ≡ 0 (mod 4)}**, because 3 ≡ 2^3 (mod 5).
- **L_7 = {(k,l): 2k + l ≡ 0 (mod 6)}**, because 2 ≡ 3^2 (mod 7).
- For later use: L_11: k + 8l ≡ 0 (mod 10); L_13: k + 4l ≡ 0 (mod 12); L_17: 14k + l ≡ 0 (mod 16).
- Each form was checked against the definition on a 48×48 box.

**Brute force.** Both systems are 12-periodic, so I worked on (Z/12)², 144 points. For **all 24 pairs** (c_5, c_7) the intersection has **exactly 6 points**, i.e. density 6/144 = **1/24**.

Independent check straight from the definition, with no parametrisation: (k,l) ↦ (2^k 3^l mod 5, mod 7) hits all 24 residue pairs, each exactly 6 times.

**Proved:** every pair of cosets intersects, and the intersection has density exactly 1/24.

## 5. Exact maximum density of the union (`maxunion.py`; independent re-check `maxunion_direct.py`)

| Block | Torus | Choices enumerated | Max covered | **Max density** | Min density | Σ 1/e_p |
|---|---|---|---|---|---|---|
| {5,7,11,13} | (Z/60)², 3600 pts | 2880 (all) | 1765 | **353/720** ≈ 0.490278 | 17/36 | 3/5 |
| {5,7,11,13,17} | (Z/240)², 57600 pts | 46080 (all; also 11520 with c_5 = 0, same max) | 30580 | **1529/2880** ≈ 0.530903 | 143/288 | 53/80 |

- One maximiser: (c_5, c_7, c_11, c_13, c_17) = (0, 0, 0, 1, 3) in the linear forms above. 720 of the 2880 choices attain the 4-prime maximum; 2880 of the 46080 attain the 5-prime maximum.
- `maxunion_direct.py` recomputes both maxima without the discrete-log forms, enumerating the target residues r_p ∈ H_p directly. It agrees.
- Translation acts on all cosets at once, which justifies fixing c_5 = 0. The full 46080-choice run confirms it.
- For comparison, the fully-independent value would be 31/64 for B4 and 529/1024 for B5. The true maxima exceed it because 11 and 13 are dependent (item 3).

## 6. The strongest statement these numbers support

Let P be a finite set of primes with chosen cosets C_p whose union covers Z², and let N = lcm_{p ∈ P} e_p. (Periodic sets cover {k,l ≥ 0} iff they cover Z².)

Then P ⊆ pool(N), and for any block B ⊆ pool(N):

    1 = dens(∪ C_p) ≤ dens(∪_{p∈P∩B} C_p) + Σ_{p∈P\B} 1/e_p ≤ maxunion(B) + Σ_{p∈pool(N)\B} 1/e_p.

**Theorem (unconditional, no bound on the size of p).** No covering system of primes for #203 has lcm_{p∈P} e_p ≤ 5040.

- If N ≤ 5040 and N ≠ 5040: Σ_{pool(N)} 1/e_p ≤ 739/792 < 1 (item 2). The plain density condition suffices.
- If N = 5040: here Σ = 143/140 > 1, so the plain density condition fails, but the block bound closes it:
  - with B4: 353/720 + (143/140 − 3/5) = **919/1008 ≈ 0.9117 < 1**;
  - with B5: 1529/2880 + (143/140 − 53/80) = **17939/20160 ≈ 0.8898 < 1**.

**Extra beyond the brief (`bound.py`; only the "lcm divides N" form, not "≤ N").** The same B5 inequality excludes coverings with lcm(e_p) dividing each of these N:

| N | bound |
|---|---|
| 10080 | 2593/2880 ≈ 0.9003 |
| 15120 | 55369/60480 ≈ 0.9155 |
| 20160 | 3041/3360 ≈ 0.9051 |
| 25200 | 94147/100800 ≈ 0.9340 |
| 27720 | 3499/3696 ≈ 0.9467 (B4, since 17 ∉ pool) |
| 30240 | 56029/60480 ≈ 0.9264 |
| 45360 | 168547/181440 ≈ 0.9289 |
| 50400 | 95257/100800 ≈ 0.9450 |

**At N = 55440 this inequality does not settle anything:** B4 gives 14599/13860 ≈ 1.0533 and B5 gives 228733/221760 ≈ 1.0314. Both exceed 1, which says nothing either way about whether a covering exists.

**Scope.** This covers pure prime covering systems only. If m is a perfect power, the algebraic factorisations (X^q + 1; 4Y^4 + 1) give "free" cells that add density, so the inequality would have to be re-run with those cells included. It is not a statement about #203 itself.

## 7. Novelty against the README (veljjanoski repo, last commit 2026-09-28) and the forum snapshot

**Limit on what I could read:** the forum HTML shows only 10 of its 15 comments ("Show 5 more comments"). Any absence claim about the forum covers those 10 comments only.

**Already present:**
- e_p = lcm(ord_p 2, ord_p 3); cosets of an index-e_p lattice of the form {ak + bl ≡ c (mod e_p)}; and Σ 1/e_p ≥ 1 as a necessary condition. Sources: AnimishSharma, 21 Jun 2026, and the README Setup section.
- Complete pools via gcd(Φ_a(2), Φ_b(3)) (README; veljjanoski comment, 15 Sep 2026):
  - 5040: 31 primes, density "1.021";
  - 55440: 55 primes, "1.163", stated complete;
  - e_p ≤ 2000: 442 primes, Σ ≈ 1.97;
  - e_p ≤ 5000: 1006 primes, Σ ≈ 2.15.
  - All four match my numbers exactly. Their published `primes_full_N5040.json` and `primes_full_N55440.json`, read as data, equal my sets, with the same (a, b, h) for 5, 7, 11, 13, 17.
- AnimishSharma: "among primes p ≤ 50,000,000, no covering set P with lcm(|H_p|) < 5040", stated as conditional on the prime bound. This is item 2 restricted to N < 5040.
- Heuristic searches at N = 5040 reaching 71.7% coverage (both sources) and AnimishSharma's 5040/10080 family checks. Both are explicitly "evidence, not proof".
- The README's rigorous result is about **strip** coverings at N = 720720 with d < 720. It is a different family.

**Not present in the README or the visible comments:**
- The exact fractions 641/720, 143/140, 21493/18480 (they give decimals), the N = 720 pool, and the ranked near-1 list in item 2 (3960: 739/792, …). These are minor.
- That AnimishSharma's p ≤ 5·10^7 caveat is **vacuous**. The largest prime with e_p ≤ 5040 is 11,321,831, so the "< 5040" exclusion is unconditional. This is derivable from the README's complete-pool method, but nobody states it, and the README's complete data stops at e ≤ 5000.
- **e_35 = 24, e_91 = 72, e_55 = 40 (pairwise independence), and the 1/24 intersection for 5 and 7.** README item 4 discusses only nesting (K_q ⊂ K_p, 77 pairs), which is the opposite relation. Also absent: e_143 = 60.
- **The exact block maxima 353/720 and 1529/2880.**
- **The block inequality and its consequence:** no prime covering with lcm(e_p) = 5040, hence none with lcm ≤ 5040, even though Σ = 143/140 > 1 there. The same goes for the | N exclusions at 10080 … 50400.

Honest size of the increment: the forum already had "< 5040", with a removable caveat. The new content is the step to "= 5040", where the plain density condition fails, plus the method that achieves it, which reaches up to 50400 and stops at 55440.

## Files

- `scripts/pool.py`, `all_e_upto.py`, `densities.py`, `xcheck.gp`, `xcheck2.gp`, `composite.py`, `cosets.py`, `maxunion.py`, `maxunion_direct.py`, `bound.py`
- Data: `pool_{720,5040,55440}.json`, `all_e_le_5040.json`, `dens_le_5040.json`, `gp_set.txt`, `forum/forum.txt` (tag-stripped)
