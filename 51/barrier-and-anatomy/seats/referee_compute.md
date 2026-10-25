# Erdős #51 — hostile COMPUTE referee (2026-10-21, Opus 5.5)

Scratch, my implementations and all mutants: `/tmp/refc51/` (`knap.c`, `exactdp.py`, `cmp_omega.py`, `cmp_bnb.py`, `cmp_sdp.py`, `mut/*`).
Originals were not modified. Every run was `ulimit -v 4000000; nice -n 19; timeout`, one heavy process at a time, omega never above NMAX = 1e8.

## Verdicts

| program | verdict |
|---|---|
| omega.c | **HOLDS.** Every 1e9 number reproduced by a decorrelated algorithm, per-a identity to 4e7. |
| bnb.py | **HOLDS.** One latent misuse hazard (objection 3, in `diag.py`). |
| smoothdp.py | **HOLDS for the two runs reported.** One latent bug for non-consecutive bases (objection 1). |
| the 5-smooth claim "odd part > 1 ⇒ R ≤ 1.875" | **FALSE as stated, by 1.04·10⁻¹⁷** (objection 2). The float DP cannot see the gap. |

## Independent implementations (decorrelated)

**A. `knap.c`: a multiplicative 0/1 group knapsack over primes, not a scan over n.**
- `best[a]` is the least n with φ(n) = a using the primes processed so far. For each prime p ≤ A+1 and each k ≥ 1, every a is extended by φ(p^k), processing a in descending order and updating in place.
- There is no NMAX: it gets ℓ(a) for every a ≤ A directly. Only even a are stored, as uint32, with saturation detected.
- **A = 10⁹, 59 s.** Every number matches omega's 1e9 output:
  - V = 139,847,905;
  - max R = 2.043447080 at a = 387,383,296 (ℓ = 791,597,265);
  - max W = 1.583664159 at a = 559,789,704 (ℓ = 886,518,891 = 3³·19³·4787, T = 1);
  - 0 violations, 0 saturated;
  - all 17 W-histogram bins identical, under both exact integer binning and omega's float binning.
- The ℓ-ordered record list rebuilt from knap's output is **byte-identical** to `run1e9/records.tsv`.
- knap gives max ℓ(a)/a over a ≤ 10⁹ as 2.0434 < 2.5. So every ℓ(a) ≤ NMAX, and omega's completeness follows **without** relying on V_table.
- **Per-a check:** an instrumented copy of omega (`omega_dump`) and knap agree on ℓ(a) for **every a ≤ 4·10⁷** (20,000,001 entries, 0 mismatches; omega hit no odd a except a = 1).
- A side fact this exposed: only **6** least preimages ≤ 10⁹ are even (a = 2¹⁶·257·2^j, j = 0..5, ℓ = 2^{9+j}·257²). All other least preimages are odd.

**B. `exactdp.py`: an exact-integer lattice DP (Python ints for n, no logs, no floats).**
- Each free prime q = d+1 is proved prime by a **Lucas/Pocklington certificate** from the known factorization of q−1, not by BPSW.
- All **402** free primes in the (2,3) lattice and all **2,914** in the (2,3,5) lattice are certified.
- Against `R23.npy` and `R235.npy`: 0 disagreements in which cells are totients, and maximum relative difference 4.4e−16 / 3.6e−16 (float noise). So the float DP never picked a materially wrong cover.
- Confirms exactly:
  - max over Y ≥ 1 in the (120, 80) lattice = 2 + 9.03502·10⁻²¹ at 2⁹⁸·3, with ℓ = 2³³·(3·2⁶⁶+1);
  - diagonal S = {2,3}, K ≤ 40: max 13/12;
  - diagonal S = {2,3,5}, K ≤ 20: max 1.0240278 (K = 3).

## Objections

**1. smoothdp.py, `if q <= P[-1]: continue` — latent bug, BUG FOUND (outside the reported scope).**
- This line drops every prime ≤ y, which is right only if the base P contains *all* primes ≤ y. Nothing checks that; the `assert` only checks that p−1 is smooth.
- `smoothdp.py 2,5 6,3` returns R(2) = 2.0 (true ℓ(2) = 3, so 1.5) and R(8) = 2.0 (true ℓ(8) = 15, so 1.875), because 3 is never offered.
- The reported runs (2,3 and 2,3,5) are consecutive bases and are unaffected.
- Fix: `assert P == list(primerange(2, P[-1]+1))`, or exclude only `q in P`.

**2. Claim "(d) 5-smooth, exponents ≤ (60,30,20), odd part > 1: max R 1.875" — FALSE as an inequality.**
- The exact maximum is **15/8 + 3·2⁻⁵⁸ ≈ 1.875 + 1.04·10⁻¹⁷**, at a = 2⁵⁸·5 with ℓ = 3·5·(5·2⁵⁵+1). Confirmed independently by bnb.
- It is the only cell above 15/8, and no cell equals 15/8 exactly. The next value is 1.6000000092.
- The float DP prints 1.875000000 because the relative gap (5.6·10⁻¹⁸) is below one ulp. There is no `exact_top`-style exact pass for this lattice; the 3-smooth lattice got one.
- Replace "max R 1.875" / "R ≤ 1.875" with "max R = 15/8 + 3·2⁻⁵⁸ (single cell 2⁵⁸·5); R ≤ 1.6000000092 elsewhere".

**3. diag.py, `fac` built only from primes in P — silent wrong answers when S is not φ-closed.**
- `bnb.ell` uses `_divs(fac)` when a ≥ 10¹² and trusts the caller's factorization completely.
- `diag.py 2,3,11 7` has 5 | 11−1, and 5 is not in P. It prints R = 1.250044 with cover (2898919)(28513)(5²). The true value is ℓ = 1317691·1254529, R = 1.0000016.
- Every S the README actually runs is φ-closed, so the published numbers are unaffected. Add `assert` that the product of p^fac[p] equals a, in `ell()` or in `diag.py`.

**4. Primality "conservative" wording points the wrong way for the (d) claims.**
- The smoothdp docstring ("conservative for a seed claim") and the README ("conservative for every ≥ and record claim") are true as worded. But the lattice claims in (d) are **≤** claims ("ℓ(a) < (2+10⁻²⁰)a for every …").
- For a ≤ claim, a BPSW pseudoprime is *anti*-conservative: it would add a fake cheaper cover.
- The claims are now safe because of the certificates in B. The README should say that, or cite B.

**5. omega's own control (count = V(10⁹)) certifies coverage, not ℓ.**
- The logic is sound: if φ is correct, count = V means complete, and the first hit in an increasing scan is the least preimage.
- But mutations M1, M3 and M5 below corrupt ℓ while the count stays exactly V. Before this seat, the ℓ-derived statistics rested on that count plus "8 record values checked by bnb".
- They are now independently confirmed (knap: full aggregates at 1e9, per-a identity to 4e7).
- "0 violations of the T-lemma" was exercised on only 6 even ℓ. It is true, but it is near-vacuous as evidence; the swap proof carries it.

**6. xcheck.py is thin.**
- It samples 300 points per lattice: 3.1% of R23's 9,721 totient cells and 0.8% of R235's 38,519.
- Cells above the cap are never sampled (log₁₀ a > 45 / > 30: 32% / 21% of totient cells).
- Its tolerance is relative 1e−9, so it cannot speak to any claim at the 10⁻¹⁷–10⁻²¹ level. Mutant S2 below passed it.

**7. Housekeeping.** `erdos51/records.tsv` (563 B, 15:16:36) is a stale partial record list from an earlier launch; it stops at a = 2,037,248. The authoritative file is `run1e9/records.tsv`. Delete the stale one or label it.

### Lines attacked that hold
- **bnb pruning:** `n*(rem+1) >= best[0]` is valid. φ(m) = rem > 1 implies m ≥ rem+1 whatever primes remain. Completions drawn from `cand[i:]` are coprime to n. Pruning on `>=` loses only ties.
- **bnb skipping (2,1)** is lossless: if 2 ‖ n then n/2 is smaller with the same φ.
- **bnb candidate set** `d%2==0 or d==1` is complete: a prime q is either 2 (d = 1) or has q−1 even.
- **smoothdp groups** read `old`, so at most one power per base prime is used. `f==1` is skipped for p = 2. `shifted()` is correct at the boundaries: vᵢ = 0 is the identity, and vᵢ ≥ s gives INF through the `all(...)` guard. The full-lattice exact match confirms this.
- **omega's loop break** `p*p>hi && p>hi` means effectively `p>hi`, so all primes ≤ PL are sieved in every segment: slower, but correct.
- **omega's leftover factor:** after dividing by all primes ≤ PL > √NMAX, the leftover is 1 or a single prime to the first power. 65537 can only appear as a leftover with exponent 1 (65537² > 2.5·10⁹).
- **omega's T/W split:** 3² goes to W (`isfermat && e==1` is false). n ≡ 2 mod 4 gets T·W ≠ R, but such n never occurs as a first hit (0 at 1e9), and R itself is computed as n/a.
- **omega's integers:** uint64 φ and the `seen` bitmap cannot overflow.

## Mutation tests

**omega** (AMAX = 4e7, NMAX = 1e8; the authors' check is count = V; mine are per-a ℓ against knap plus aggregates):

| mutant | count = V | my check |
|---|---|---|
| M1: scan each segment in reverse | passes | **caught** (1,859,330 ℓ mismatches) |
| M2: 257 not treated as Fermat | passes | **caught by the histogram only** (ℓ unchanged) |
| M3: sieve start skips n = lo when p \| lo | passes | **caught** (11) |
| M5: first n of each segment skipped | passes | **caught** (2) |
| M4: last n of each segment skipped | passes | passes |

M4 is harmless at this scale: those n are k·2²², and none of them is a least preimage ≤ 10⁸.

**bnb** (their xcheck; my per-a check against knap on 10,305 values):

| mutant | xcheck | my check |
|---|---|---|
| B1: prune at n·2·rem | **caught** (272 + 271) | **caught** (805) |
| B2: same prime reusable | **caught** (26 + 3) | **caught** (42) |
| B3: q = 2 never a candidate | **caught** (crashes with TypeError) | **missed** |
| B4: 2² forbidden | passes | passes |

B3 is a gap in *my* check: even ℓ are so rare that my sample hit none. B4 is empirically equivalent: v₂(ℓ) = 2 occurs 0 times in 6.2M ℓ ≤ 4e7 and 0 times in both lattices.

**smoothdp** (their xcheck; my full-lattice exact comparison):

| mutant | xcheck | my check |
|---|---|---|
| S1: several powers of one base prime allowed | passes | passes (equivalent on these lattices: 0 cells differ) |
| S2: base primes also usable as free primes | **missed** | **caught** (R235 cell 2³², 1.667 vs 2) |
| S3: top power dropped | caught 1 (R23) + 0 | **caught** (2 + 2) |
| S4: free primes usable twice | **caught** (23 + 3) | **caught** (498 + 643) |

**Not checked (out of brief):** `chain.py` / `chain_safe.py` and the July safe-marker chain claim (ℓ(17,776,474,638,307,328), and "beats every value below 1.2·10¹¹").
