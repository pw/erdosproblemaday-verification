# Erdős #203 — hostile referee report (JUDGMENT seat)

Reviewed: `README.md` (both the 12:27Z and the 12:36Z versions; the theorem text is the same in both), the code
listed in the brief, the saved forum thread `/tmp/erdos203_forum.html` (all 15 comments), and veljjanoski's linked
repository github.com/veljjanoski/erdos203 (README at commits of 2026-09-15 and 2026-09-28).
Referee scratch code: `/tmp/ref203/` (`myU.py`, `quot.py`, `quot7.py`, `alg.py`, `alg2.py`, `lb.py`, `algscan.py`,
`fr5.py`).

## What I re-derived independently (all agree with the README)

- e_35 = 24, e_55 = 40, e_91 = 72, e_143 = 60 by group closure; the powers of 2 mod 35 as listed; 3 is not among them.
- Characters from scratch (my own generator search and discrete logs, not the pool file). For p = 13: 2 has order 12,
  so h = 2, u = 1, and 2^4 = 16 ≡ 3, so v = 4. This matches pool_5040.json's (1,4). The other six characters agree
  with the pool file up to a unit multiple, so they have the same kernel.
- U({5,7}) = 3/8. U({5,7,11,13}) = **1765/3600** over a FULL enumeration of all 2880 choices (no translation trick):
  720 optimal choices, i.e. 4 × 180. U({5,7,11,13,17}) = 30580/57600.
- U(S6) = 983/1728 = 294900/518400, computed by a different representation: the quotient group ℤ²/∩L_p, which has
  8,640 points, instead of the 518,400-point torus. 4320 optimal choices; 2.5 s.
- U(S7) = 4213/7200 = **303336/518400**, by exact search on the 43,200-point quotient. The search is pruned: an S6
  configuration is expanded only if |U6| + 1/30 can reach the known witness, which is valid. 64,800 optimal choices,
  the same count as maxunion.c. So loss(S7) = 541/720 − 4213/7200 = **133/800 = 0.16625 exactly**.
- 55440: the density is exactly 21493/18480 = 1.163041, below 933/800 = 1.16625. Excluded, with a margin of 0.0032.
- Algebraic sweep, S6. I recomputed U_d for d ∈ {2,3,4,5,9,10,12,15,20,30,45,60,720}. I decided admissibility by a
  different route: take a representative (k,ℓ) of the coset, set a = 2^k 3^ℓ, set m = −a^{−1}, and test
  m^{(p−1)/g} ≡ 1. This does not use h. The free sets were rebuilt independently. Every value matches, and the
  maximum is **1583/2700 = 0.586296** at d = 15.
- Algebraic sweep for the block {5,7,11,13,19,31}: max_d U_d = 382/675 = 0.565926, which matches
  algsweep_5_7_11_13_19_31.json.
- Σ_{odd prime q ≥ 7} 1/q² = 0.0511363.
- Every pool density quoted in "Complete pools" matches the exact fraction in pool_N.json. 40320 is 1.041121, below
  25/24 = 1.041667, which is correct.
- scanN.tsv and scanN2.tsv: every N from 1 to 30000 has status `complete`. Below 5040 only N = 5040 reaches 1. The
  runners-up are 3960 at 0.933 and 3600 at 0.930.
- Pure exclusion holds for every N ≤ 30000. That includes the 53 multiples of 720 which frontier.py silently skipped
  (see finding 7): all have S7 ⊆ pool, and the largest density among them is 1.0656, below 1.16625.
- Algebraic exclusion holds for every N ≤ 30000 only once the block containing 31 is used for 27720 (finding 4).

## Findings

**1. OVERCLAIM.** Quoted: "So any covering system for #203 has Σ 1/e_p ≥ 1.16625 and lcm(e_p) > 65520 (and > every
scanned N)." The same claim appears in the scope section: "nor with Σ 1/e_p < 1.16625 (pure)".
Theorem B actually gives Σ_{p∈P} 1/e_p ≥ 1 + loss(P ∩ S7). The bound is 1.16625 only when P ⊇ S7. Smaller cases:
- If the covering omits 31: Σ ≥ 1 + loss(S6) = 1.1492.
- If it omits 5: Σ ≥ 1 + loss({7,11,13,17,19,31}) = 1.0696.
- If it uses none of S7: only Σ ≥ 1.

Nothing proven here forces a covering at large period to use 5, 7, 11, 13, 17, 19 and 31; the primes with e_p ≤ 2000
already carry density 1.97 (veljjanoski). The correct statement is "Σ ≥ 1 + loss(P ∩ S7); in particular ≥ 1.16625
when P ⊇ S7".

**2. OVERCLAIM (title).** Quoted: "every covering system wastes at least 1/24 of its density". Theorem A proves this
only for coverings that contain both 5 and 7. A covering that avoids 5 or 7 has no proven lower bound on waste. That
lower bound would need some pair of transversal primes; whether an exact cover by distinct lattices is impossible in
2D is not addressed. Retitle to "…every covering that uses 5 and 7 wastes ≥ 1/24…" or similar.

**3. OVERCLAIM.** Quoted: "lcm(e_p) > 65520" and "the first pools NOT excluded by this block are 110880 …".
What the computations establish:
- every N ≤ 30000, from the complete scan;
- the listed pools 30240, 40320, 45360, 50400, 55440, 60480, 65520;
- the divisors of those listed pools.

The divisor step is valid but the README never states it. It needs a one-line lemma: f(N) = density(N) −
loss(S7 ∩ pool N) is monotone under N | M, because loss(B) − loss(B′) ≤ Σ_{B∖B′} 1/e_p.

Thousands of N in (30000, 65520] are neither scanned nor divisors of a listed pool, for example 30030, 31680, 36960,
39600, 41580, 47520, 51480, 59400 and 63360. I computed three of them with `pool2.py`, all complete: 39600 = 1.0662,
47520 = 1.0634, 36960 = 1.0300. All three are excluded, so the claim is very likely true, but it is not established.
Either extend scanN2 to 65520, or restate as "lcm(e_p) > 30000, and ∉ {listed} ∪ divisors up to 65520". "The first
pools NOT excluded" should read "among the pools computed". The same gap exists for (65520, 110880).

**4. GAP / WRONG (Theorem C coverage).** Quoted: "excluded for every N ≤ 5040 and for 10080, 15120, 20160, 25200,
27720, 30240, …" and "the perfect-power variant fails for every pool of density < 1.08066".
The pool for 27720 lacks 17, because 16 ∤ 27720. The S6-block computation that the README describes gives:

0.586296 + 0.051136 + 1.056421 − Σ_{5,7,11,13,19} (= 0.655556) = **1.0383 ≥ 1**, so 27720 is NOT excluded.

The sub-block {5,7,11,13,19} (maxU 0.552593) still gives **1.0046 ≥ 1**. Only the block {5,7,11,13,19,31} gives
0.565926 + 0.051136 + 1.056421 − 0.688889 = **0.98459 < 1**. That file, algsweep_5_7_11_13_19_31.json, was created at
12:31Z, after the README text, and the README nowhere describes it. I reproduced 382/675 independently, so the
exclusion of 27720 is TRUE, but the README must describe the 31-including block.

The sentence "fails for every pool of density < 1.08066" is FALSE as stated. 27720 has density 1.0564 < 1.0806, and
the described S6 computation does not exclude it. The correct statement is "every pool ⊇ S6 with density < 1.08062",
plus the specific sub-block results. Every other listed N contains S6 and is fine. Every N ≤ 30000 other than 27720
is excluded by the S6 bound alone (scan: `algscan.py`).

**5. WRONG NUMBER.** Quoted: "(= 1.08066 when the pool contains S6)", and "< 1.08066" in the scope section.
The correct value is 1 − 0.0511363 − 1583/2700 + 517/720 = **1.080623**, which frontier.py itself prints as
1.08062. No verdict changes, because no pool density lies in [1.08062, 1.08066). Fix both occurrences.

**6. WRONG (sentence).** Quoted: "the unconstrained value is 0.568866 — the free sets gain less than the residue
constraints cost". The numbers say the opposite: max_d U_d = 0.586296 > U(S6) = 0.568866, so the free sets gain more
than the constraints cost, a net gain of +0.0174 at d = 15. What is true is that the residue constraints cancel most
of the free sets' nominal density: 0.1467 nominal at d = 15, against a net gain of 0.0174. Reword.

**7. WRONG (state at writing) and a TOOL that only reports passes.** Quoted: "All 2^7 subsets of S7 in
`subsets_S7.json`". At 12:27–12:35Z the file held 127 entries; the full S7 job (`maxunion sub_5_7_11_13_17_19_31.txt`)
was still running, and the file reached 128 only at 12:36Z.
In the meantime frontier.py put the 53 N whose key was missing (every multiple of 720, including 55440, 60480 and
65520) into `pending`, `continue`d past both the pure and the algebraic checks, and still printed "PURE covering NOT
excluded: []" and "pure: every N <= 30000 excluded". For those 53 N it had not checked anything.
The README's conclusions for those N are true (I checked them with loss(S7) = 133/800), but the instrument must
treat `pending` as fatal (non-zero exit), not report it as clean.

**8. OVERCLAIM (provenance).** Quoted: "Theorem B (computer-assisted, three independent implementations)" and "all
agree where all ran". When the README was written:
- The headline S7 value (0.16625) had been computed by ONE implementation, maxunion.c.
- S6 had one; numpy S6 finished 12:35Z and bigint S6 12:33Z, and both agree.
- `cpsat_S6.log` and `cpsat_S7.log` are empty (0 bytes).
- The Controls claim "CP-SAT reproduces 1765 and 30580 with proof of optimality (1.2 s, 32 s)" has no log in the
  directory or the bundle list.

The numbers are right (finding list above: S7 reproduced by me on the quotient group). Still, state exactly which
implementation reproduced which value. Add the CP-SAT logs, or drop the CP-SAT claim.

**9. OVERCLAIM (attribution / novelty). This is the most important fix for a public page.** The README's Setup and
the whole framing of Theorem C appear without credit, yet several pieces were already public.

On 2026-09-15 (commit bed197d), veljjanoski's repository README, linked from the forum post, already contained:
- the m = t^{N0} free sets: cells k ≡ ℓ ≡ 0 (mod q) for odd q | N0, and cells (2,0) mod 4 for 4 | N0, citing Izotov;
- "By Capelli's theorem these are the only factorisations of 2^k 3^l t^{N0} + 1 as a polynomial in t";
- "Using them restricts the admissible cosets: m ≡ −h^{−c} (mod p) must be an N0-th power residue". This is almost
  verbatim our Theorem C preamble.

The forum post itself contains:
- one coset per prime, with index e_p;
- covering ℤ² ⟺ covering the problem;
- complete pools via gcd(Φ_a(2), Φ_b(3));
- 31 primes at 5040 and 55 at 55440.

AnimishSharma (21 Jun) proved |H_p| = lcm(ord_p 2, ord_p 3) and the necessary condition Σ 1/e_p ≥ 1, and excluded
lcm < 5040 for p ≤ 5·10^7.

None of these is credited where it is used. The "Second seats" note "None states a forced-overlap or block bound" is
true, and it is exactly the right boundary for what we may claim (see (g)).

**10. NIT (misdated attribution).** Quoted: "(These agree with veljjanoski's independent computation posted 15 Sep 2026
where both exist: 31/1.021, 55/1.163, 99/1.249.)" The densities 1.021, 1.163 and 1.249 are not in the 15 Sep forum
text, which gives only the counts 31, 55 and "99 primes p ≤ 10^7". They are in the linked repository. On 15 Sep the
720720 pool there was "primes p ≤ 10^7" and not certified complete. Completeness came in the 28 Sep revision (commit
f77420a), which also records that earlier "complete" files had 91 and 127 primes. Say "veljjanoski's repository
(15 Sep; 720720 pool certified complete 28 Sep)".

**11. GAP (minor).** Quoted: "The pool for N = 5040 has density 143/140 < 1 + 1/24 = 25/24, so no covering system has
lcm(e_p) | 5040". The missing case is a covering that does not contain both 5 and 7. Then Σ_P ≤ 143/140 − 1/6 =
0.855 < 1 (or 143/140 − 1/4 = 0.771). It is one line, but the corollary is false without it. Theorem A also excludes
7920 (1.0255), 15840 (1.0400) and 18480 (1.0158) by the same line; listing them is optional.

**12. NIT (Lemma 1: the prime 2).** Quoted: "If a finite set P of primes ≥ 5, plus the prime 3, plus the algebraic free
sets below, certify compositeness for all k, ℓ ≥ 0 … U ⊇ {k ≥ K, ℓ ≥ max(L,1)}". For k = 0, 3^ℓ m + 1 is always even,
so every real witness's k = 0 column is certified by the prime 2, which is not in the list. The quadrant must be
{k ≥ max(K,1), ℓ ≥ max(L,1)}, and "So the prime 3 never helps" should read "the primes 2 and 3 never help".
Also "Λ ⊇ Nℤ²" should be N′ = lcm(N, periods of the free sets) when free sets are present.
The core argument is correct:
- U is Λ-periodic;
- U contains the shifted quadrant;
- the quadrant meets every Λ-class.
Each prime p ≥ 5 contributes at most one coset, or none when −m^{−1} ∉ H_p or p | m. Dropping such primes only
lowers Σ, so every bound survives.

**13. NIT (Theorem C hygiene).**
- Say "take N0 maximal (t not a perfect power)". With t a perfect power the free-set list belongs to the true
  exponent. This is harmless here, because the maximum over all d covers it.
- Say "as a polynomial in t (k, ℓ fixed)" where Capelli is invoked, as veljjanoski does. The application itself is
  right. With c = −2^{−k}3^{−ℓ}:
  - c ∈ ℚ^q for odd q ⟺ q | k, ℓ;
  - c ∉ ℚ² because c < 0;
  - c ∈ −4ℚ^4 ⟺ k ≡ 2, ℓ ≡ 0 (mod 4).
- d = gcd(N0, 720) is the right parameter, because p − 1 | 720 for all of S6 and so gcd(N0, p−1) = gcd(d, p−1).
- q ≥ 7 never divides p − 1 for p ∈ S6, so the allowance primes impose no constraint inside the block.
- Ignoring their constraints outside the block only enlarges the maximum. This is the safe direction.
- Σ_{q≥7} 1/q² is a valid upper bound for the union of those free sets.
- Monotonicity in the block holds: every S6 prime has H_p = (ℤ/p)^×, so each has ≥ 1 admissible coset for every d.

**14. NIT (latent tool bug, no current consequence).** The new sub-block sweeps whose lcm(p−1) is not divisible by 5
are `algsweep_5_7_13*.json`, with LCM 12, 36 and 144. They omit the 5ℤ² free set (density 1/25): it is neither in
F_d, because 5 ∤ LCM, nor in the q ≥ 7 allowance. frontier.py uses these files. I added 1/25 to every such case:
no verdict for N ≤ 30000 changes (`fr5.py`). Fix the allowance to Σ over odd primes q not dividing LCM.

**15. NIT (provenance of the scan).** Quoted: "`scanN2` extends this N by N above 5040 (range stated in the entry)".
The range (5041..30000) is not stated in the README. There is no scanN2 script in the directory: scanN.py
hard-codes `scanN.tsv`. "Every N in the scanned range" is therefore undefined on the page. Commit the script or the
command line, and state the range.

**16. NIT (wording).** Quoted: "Negative control for Theorem A's mechanism: the pair (7,13) has e_{91} = 72". (7,13) is
transversal, so it is a positive instance and not a negative control. The negative control is the 194 non-transversal
pairs, and that count is correct (194 of 465). The numbers e_91 = 72 and 194/465 check out.

**17. NIT (primality).** Pool completeness rests on sympy `isprime` (BPSW). That test is deterministic below 2^64, so
every prime in the listed pools is proven prime; the largest is 7,983,361. Any scan cofactor above 2^64 would be only
BPSW-probable. Say so, or certify those.

## (g) What the page may claim as ours

The following was public before us:
- the coset/lattice formulation and the reduction to covering ℤ² (veljjanoski);
- complete pools via gcd(Φ_a(2), Φ_b(3)), and the counts 31/55/99 (veljjanoski);
- the perfect-power free-set model with Capelli and the N0-th-power residue condition (veljjanoski's repository,
  15 Sep);
- |H_p| = lcm and the density condition Σ 1/e_p ≥ 1 (AnimishSharma);
- exclusion of lcm < 5040 for primes ≤ 5·10^7 (AnimishSharma);
- heuristic searches showing 71.7% coverage at 5040 and 76% at 55440, and ~70–74% for perfect powers (veljjanoski).

What is new and may be claimed:
- (i) the forced-overlap lemma for transversal pairs (Lemma 2 + Theorem A). It is the 2D analogue of the classical
  CRT remark that coprime moduli always meet, and it upgrades the density condition to Σ ≥ 25/24 for coverings
  through 5 and 7. It thereby rigorously excludes N = 5040, where Σ = 143/140 > 1 and the density condition fails to
  decide, along with 7920, 10080, 15840, 18480, 20160 and 40320.
- (ii) removing the prime cap: every N ≤ 30000 is handled by complete pools, unconditionally.
- (iii) exact block maxima (Theorem B), computer-assisted and now reproduced by an independent method for S6 and S7.
  They exclude every lcm ≤ 30000 and the listed pools up to 65520, including 55440, where veljjanoski's search was
  only heuristic.
- (iv) the first rigorous exclusion of the perfect-power variant (Theorem C) for every lcm ≤ 30000 and the listed
  N ≤ 60480, using the 31-including block for 27720. The setup must be credited to veljjanoski.

The page may NOT claim a universal 1/24 waste, a universal Σ ≥ 1.16625, or lcm > 65520.

## Verdict

**HOLDS WITH FIXES.** None of the findings is fatal, and every number I recomputed is right. The fixes:
- 1 and 2: restrict the 1.16625 and 1/24 claims to coverings containing S7, respectively {5,7};
- 3: restate the frontier as lcm > 30000 plus the listed N, or extend the scan to 65520;
- 4: describe the {5,7,11,13,19,31} algebraic block that 27720 needs, and restrict "every pool of density < 1.08066"
  to pools ⊇ S6;
- 5: 1.08066 → 1.08062;
- 6: reword the "free sets gain less" sentence;
- 7 and 8: correct the implementation and provenance statements, and make frontier.py fail on `pending`;
- 9 and 10: credit veljjanoski (repository, including the Theorem C setup) and AnimishSharma;
- 11 and 12: add the "5 or 7 absent" line, and the prime 2 in Lemma 1;
- 13–17: hygiene.
