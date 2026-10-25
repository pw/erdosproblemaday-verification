# Erdős #203 — the cosets of 5 and 7 always overlap; no covering system has period ≤ 65,520

Problem (erdosproblems.com/203): is there m ≥ 1, (m,6)=1, such that 2^k 3^ℓ m + 1 is composite for all k, ℓ ≥ 0?
The only known mechanism for such an m (as for Sierpiński numbers) is a finite **covering system of primes**, possibly
combined with the algebraic factorisations available when m is a perfect power. This bundle proves that no such
covering system exists at any small period, by an argument that is elementary at its core.

## Setup (all elementary)
For a prime p ≥ 5 let H_p = ⟨2,3⟩ ≤ (ℤ/p)^×, e_p = |H_p| = lcm(ord_p 2, ord_p 3), and
L_p = {(k,ℓ) ∈ ℤ² : 2^k 3^ℓ ≡ 1 (mod p)} — the kernel of the surjection ℤ² → H_p, so a sublattice of index e_p.
For m coprime to p, {(k,ℓ) : p | 2^k 3^ℓ m + 1} is empty (if −m^{-1} ∉ H_p) or a single coset C_p of L_p.

**Lemma 1 (ℕ² vs ℤ²).** If a finite set P of primes ≥ 5, plus the primes 2 and 3, plus the algebraic free sets below,
certify compositeness for all k, ℓ ≥ 0 (or merely for all k ≥ K, ℓ ≥ L), then the cosets C_p (p ∈ P) together with the
free sets cover all of ℤ². Proof: 2 | 2^k 3^ℓ m + 1 exactly when k = 0 (m odd), and 3 | 2^k 3^ℓ m + 1 forces ℓ = 0; the
union U of the cosets and free sets is invariant under Λ = ∩ L_p ∩ (periods of the free sets) ⊇ Nℤ², and
U ⊇ {k ≥ max(K,1), ℓ ≥ max(L,1)}; every point of ℤ² is Λ-congruent to one of those. So the primes 2 and 3 never help,
and we may study coverings of ℤ².

**Lemma 2 (two primes).** For p ≠ q ≥ 5, the kernel of (k,ℓ) ↦ 2^k 3^ℓ mod pq is L_p ∩ L_q, so
[ℤ² : L_p ∩ L_q] = e_{pq} := |⟨2,3⟩ ≤ (ℤ/pq)^×|. Hence C_p ∩ C_q is empty or a coset of L_p ∩ L_q, of density 1/e_{pq};
and if e_{pq} = e_p e_q the map ℤ² → H_p × H_q is onto, so C_p ∩ C_q ≠ ∅ for **every** choice of the two cosets.

**Theorem A (elementary).** e_35 = 24 = e_5 · e_7 (2 has order 12 mod 35, and 3 is not a power of 2 mod 35:
the powers of 2 are 1,2,4,8,16,32,29,23,11,22,9,18 — so ⟨2,3⟩ is all of (ℤ/35)^×). Therefore, whatever cosets are
chosen, C_5 ∩ C_7 has density exactly 1/24, and any covering system containing 5 and 7 satisfies
    Σ_{p∈P} 1/e_p ≥ 1 + 1/24.
(density(∪C_p) ≤ density(C_5 ∪ C_7) + Σ_{p≠5,7} 1/e_p = 1/4 + 1/6 − 1/24 + Σ_{p≠5,7} 1/e_p.)

**Complete pools.** A covering has a period N = lcm(e_p), and every usable prime divides G_N = gcd(2^N−1, 3^N−1).
`pool.py`/`pool2.py` compute the COMPLETE pool of primes with e_p | N (every prime factor of G_N, split by cyclotomic
pairs gcd(Φ_a(2),Φ_b(3)); certificate: the product of the found prime powers equals G_N exactly) with their
characters (u,v): L_p = {uk + vℓ ≡ 0 mod e_p}. Densities (exact fractions in `pool_N.json`):
  N=720: 15 primes, 641/720 = 0.8903 · 2520: 23, 0.9171 · **5040: 31 primes, 143/140 = 1.021429** · 10080: 1.0319 ·
  15120: 1.0471 · 20160: 1.0367 · 25200: 1.0656 · 27720: 1.0564 · 30240: 1.0580 · 40320: 1.0411 · 45360: 1.0605 ·
  50400: 1.0766 · 55440: 55 primes, 1.163041 · 60480: 1.0633 · 65520: 1.1035 · 110880: 1.1777 · 166320: 1.1913 ·
  221760: 1.1826 · 332640: 1.2064 · 720720: 99 primes, 1.248958.  (These agree with veljjanoski's independent
  computation posted 15 Sep 2026 where both exist: 31/1.021, 55/1.163, 99/1.249.)
`scanN.py`: for EVERY N ≤ 5040 the complete pool density (G_N fully factored, 5040/5040 complete); only N = 5040
reaches 1 (next: 3960 at 0.933, 3600 at 0.930). `scanN2` extends this N by N above 5040 to 30,000; `scanN3` (`scan/scanN3.tsv`, 30,001..65,520, 0 UNFACTORED,
landed 2026-10-12 13:25Z) to 65,520; `scripts/frontier3.py` = `frontier.py` reading all three, output `frontier3.out`.

**Corollary of Theorem A.** The pool for N = 5040 has density 143/140 < 1 + 1/24 = 25/24, so a covering with lcm | 5040
cannot use both 5 and 7; one that omits 7 has density ≤ 143/140 − 1/6 < 1, one that omits 5 has ≤ 143/140 − 1/4 < 1.
So no covering system has lcm(e_p) | 5040; with the scan (density < 1 for every other N ≤ 5040), none has
lcm(e_p) ≤ 5040 at all; and the pools for 10080, 20160, 40320 (1.0319, 1.0367, 1.0411 < 1.04167, all containing 5 and 7)
are excluded by the same line. (Monotonicity: a period N excluded by any of these bounds excludes every divisor of N,
since pool(d) ⊆ pool(N).)

## Theorem B (computer-assisted, three independent implementations)
For a block B of primes let U(B) = max over all coset choices of the density of ∪_{p∈B} C_p (an exact maximum over a
finite set, computed by brute force on the torus (ℤ/T)², T = lcm e_p). Since U is monotone and the union of a covering
P is at most U(P∩B) + Σ_{p∈P∖B} 1/e_p, a covering with lcm(e_p) = N needs
    U(B ∩ pool(N)) + density(N) − Σ_{p∈B∩pool(N)} 1/e_p ≥ 1.
Exact values (`maxunion.c` bitset brute force; `maxunion_np.py` numpy brute force; `cpsat_maxcover.py` OR-tools CP-SAT
max-cover — all agree where all ran):
  {5,7}: U = 9/24 (loss 1/24, = Theorem A) · {5,7,11,13}: 1765/3600, loss 0.1097 · +17: 30580/57600, loss 0.1316 ·
  +19 (= S6): 294900/518400, loss 0.1492 · +31 (= S7): 303336/518400, **loss 0.166250**.
  All 2^7 subsets of S7 in `subsets_S7.json` (so the bound applies to every N, whichever of these primes its pool has).
Consequences: no covering with lcm(e_p) = N for any N whose pool density is below 1 + loss(S7 ∩ pool N); in
particular the complete pools for 55440 (1.163041 < 1.166250), 60480, 65520 and EVERY N ≤ 65,520 (`frontier.py` / `frontier3.py`, each N
with its own sub-block; the script refuses to print a frontier if any subset value is missing) are excluded. Of the larger
pools computed, the ones NOT excluded by this block are 110880 (1.1777), 166320, 221760, 332640, 720720 (1.249); periods
between 65,520 and 110,880 were not computed (`frontier3.out`: "pure: every N <= 65520 excluded"). The general inequality is Σ_P 1/e_p ≥ 1 + loss(P ∩ S7); so any covering whose period is a multiple of 720
(⇔ its pool contains all seven primes) needs Σ 1/e_p ≥ 1.16625 — NOT every covering (one using none of the seven is
bound only by Σ ≥ 1).

## Theorem C (perfect-power m: the algebraic free sets)
The setup is veljjanoski's (repository README, Sept 2026) and is restated here: if m = t^{N0} with N0 maximal, the
factorisations X^q + 1 (q odd prime, q | N0) and 4Y^4 + 1 (4 | N0) make the sets qℤ² and {k ≡ 2 (4), ℓ ≡ 0 (4)} free;
by Capelli's theorem (applied to 2^k 3^ℓ t^{N0} + 1 as a polynomial in t) these are the only such factorisations. The
price: m ≡ −h^{−c} (mod p) must be an N0-th power residue, i.e. a gcd(N0, p−1)-th power residue, which removes cosets.
What is ours is the exact computation below.
`algsweep.py` computes, for the block S6 and every d = gcd(N0, 720) (720 = lcm(p−1 : p ∈ S6)), the exact maximum
U_d of |∪ admissible cosets ∪ F_d| / T² with F_d = ∪_{odd q | d} qℤ² ∪ ([4|d] Aurifeuillean set): max_d U_d = 0.586296
(attained at d = 15, 30, …; the unconstrained value is 0.568866 — the residue condition eats almost all of the free
sets' nominal 0.147 and leaves a net gain of 0.017). Free sets of odd primes q not dividing lcm(p−1 : p ∈ block) are
credited as a density allowance Σ 1/q² (= 0.051136 over q ≥ 7 for S6, whose lcm is 720; `frontier.py` computes it per
block, so a block without 11 is also charged 1/25 — a first version omitted that; no verdict changed) — their residue
constraints are ignored, which only weakens the bound. So a covering with a perfect-power m and lcm(e_p) = N needs
density(N) ≥ 1 − allowance − U_max(block) + Σ_{block} 1/e_p (= 1.08062 when the pool contains S6). Periods whose pool
lacks 11, 17 or 19 were run with their own sub-block (`algsweep_<block>.json`; 27720, lacking 17, needed the block
{5,7,11,13,19,31}: max U_d = 0.565926 = 382/675, which excludes it — the S6-only bound would not): excluded for every
N ≤ 65,520 except 55440 and 65520 (`frontier3.out`: "alg : every N <= 65520 EXCEPT [55440, 65520]"); 40320, 45360, 50400,
60480 excluded; NOT excluded (by these blocks) for 55440, 65520 and above.

## Controls
- `maxunion.c` checks every coset bitset has exactly T²/e_p points (fails loudly otherwise); `maxunion_np.py` rebuilds
  the masks from a meshgrid and re-counts a given witness literally (S4, S5, S6); `maxunion_int.py` is a third
  implementation (Python big-int bitsets; S4, S5, S6 and S7: 303336, 64,800 optimal, 1,527 s — `bigint.log`); CP-SAT reproduces 1765 and 30580 with
  proof of optimality (`cpsat_S4.log`, `cpsat_S5.log`; the S6/S7 CP-SAT runs hit their time limits). The S7 value 303336
  and its 64,800 optimal configurations were ALSO reproduced by the judgment referee's own pruned exact search on the
  43,200-point quotient group (`referee/ref203_scratch/`). Numbers of optimal configurations scale by e_5 = 4 between
  the c_5-fixed and the full enumeration (6→24, 180→720, 720→2880), as translation invariance predicts.
- e_p recomputed by sympy `n_order` (lcm) for all 31 primes of the 5040 pool: 0 mismatches. e_35 = 24 three ways
  (group closure, powers of 2 mod 35, kernel determinant on [0,12)²).
- Pool completeness: ∏ p^{v_p(G_N)} == G_N asserted for every N listed.
- A second positive instance of Theorem A's mechanism: (7,13) has e_{91} = 72 = e_7 e_13 → forced overlap 1/72; and the
  discriminating negative: (11,13) has e_{143} = 60 ≠ 120, so those cosets CAN be chosen disjoint (194 of the 465 pairs in
  the 5040 pool are non-transversal) — Theorem A uses only transversal pairs.
- The all-N scan (`scanN.py`, `scanN_range.py`) factors G_N = gcd(2^N−1, 3^N−1) completely with sympy and sums 1/e_p over
  its prime factors (status `complete` on every row means no composite cofactor was left); the cyclotomic split with the
  product certificate is used for the named pools (`pool.py`/`pool2.py`). The two agree on every N where both exist.
- The densities 1.021 / 1.163 / 1.249 we compare against are from veljjanoski's repository (the 720720 pool was certified
  complete there in its 28 Sep revision), not from the forum text.

## Second seats (both Opus, separately briefed, reports in `referee/`)
- EVIDENCE seat (recomputed from scratch, own code + PARI/GP cross-checks, before reading our argument): pools
  641/720, 143/140, 21493/18480 with completeness; only N = 5040 reaches density 1 below 5040 (runners-up 739/792 at
  3960, 3349/3600 at 3600); every prime with e_p ≤ 5040 is below 11.4 M (so AnimishSharma's p ≤ 5·10^7 cap was never
  binding); e_35 = 24, e_91 = 72, e_55 = 40 (all = e_p e_q) while e_143 = 60 ≠ 120 (11 and 13 can be disjoint);
  the 1/24 intersection on (ℤ/12)² for all 24 coset pairs; block maxima 353/720 and 1529/2880 over ALL 46,080
  five-prime choices (not only c_5 = 0). Verdict: agrees on every number.
- JUDGMENT seat: hostile read of the lemmas, the inequality, Capelli/residue logic, the frontier sentences; see
  `referee/referee_judgment.md` and the entry's record of what was changed.
- All 15 comments of the live thread were read (the page collapses the five oldest; the saved HTML holds all 15):
  Dogmachine ×5, uona ×2, Bloom ×2, Tao ×2, Woett, emil467q, AnimishSharma, veljjanoski. None states a forced-overlap
  or block bound.

## What this does and does not say
It says: the covering-system mechanism (with or without perfect-power factorisations) cannot produce a #203 witness
with period ≤ 5040, nor with Σ 1/e_p < 1.16625 (pure) / and the perfect-power variant fails for every pool of density
< 1.08066. It does NOT say that no m exists, and it does not touch mechanisms that are not covering systems
(none are known; cf. Filaseta–Finch–Kozek's conjecture that Sierpiński numbers are coverings or perfect powers).
