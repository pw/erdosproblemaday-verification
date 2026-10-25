# Seat D — hostile referee, human-readable proofs: Itabe, "A candidate N^{1/3+o(1)} upper bound for Erdős Problem 160" (14 July 2026)

Read against: `/tmp/erdos160/itabe/itabe.txt` and `repo/paper/main.tex` (the TeX was used to settle every symbol the text extraction garbled). The Lean sources were consulted only to check that the prose and the code describe the same objects.
Scratch instruments: `/tmp/erdos160/seats/D_scratch/{lemmas.py, labels.py, params.py, nu_small.py, bridge.py}`. Each run took under 15 s at `nice -n 19`.

## VERDICT: HOLDS AS READ

Every lemma's proof was read line by line. Every algebraic identity, case split and inequality chain the checklist names was recomputed. Each residue lemma was brute-forced exhaustively over all inputs it quantifies over, for a range of parameters, with controls that make the lemma fail when exactly the hypothesis the proof uses is removed. Nothing FATAL and no GAP was found. All findings below are EXPOSITION: the prose is terse or loose in places where a reader has to supply a step, but each such step is true and checked.

One instrument caveat the caller should know about: the existing `check_itabe.py` **exits 2, not 0** (its mod-24 rows are close to vacuous). Details are in "What I verified, §(ii)" below.

---

## Objections

**1. EXPOSITION (§2, product step).**
> "More explicitly, an at-most-two tuple of product colours projects to an at-most-two tuple in each factor. The first two labels then form a proper-ABBA filter by the classification above."

Classifying each factor *separately* does not close the argument. If λ has shape AABB (λ0=λ1≠λ2=λ3), nothing about μ by itself rules this out. What rules it out is that the *product* takes at most two values: that forces μ0=μ1 and μ2=μ3, and μ's AABB-freeness then gives the contradiction. The working argument is to classify the product tuple itself:
- three equal product colours ⇒ three equal λ;
- product ABAB ⇒ λ-ABAB equalities;
- product AABB ⇒ μ-AABB equalities;
- what remains is product-proper ABBA ⇒ ν-ABBA equalities.

The conclusion is correct. As phrased, the sentence points at the wrong mechanism. Lean does it correctly (`sharedNoThreeABAB_aabb_isProperABBAFilter` acts on the pair `(sharedColour x, aabbColour x)`).

**2. EXPOSITION ("X-free" is never defined).** The paper never defines "excluding ABAB", "AABB-free" or "ABBA-free". The §2 argument needs the *equality* reading (no nontrivial AP satisfies the equalities of the pattern, with A = B allowed, so AAAA counts):
> "contradicting its ABBA-free property"

This step fails under a "distinct A ≠ B" reading whenever ν is constant on the AP. μ likewise has to exclude AAAA. The proofs establish exactly the equality versions: (4.13), (5.6) and §7.2 never assume A ≠ B. The Lean predicates are also equality versions (e.g. `horizonCubicColour_abba_free`: `c n0 ≠ c n3 ∨ c n1 ≠ c n2`). Add a one-line definition.

**3. EXPOSITION (§3, quotient descent).**
> "dividing by P shows that the quotients q_j form the same integer progression."

Precisely: the quotients satisfy the same homogeneous linear identities. They form an integer progression, usually with a different step and possibly step 0. In §4.2 the identity being carried is a single weighted relation, not a progression. The descent itself is valid for any homogeneous integer-coefficient identity, signed or not. (Checklist item 2: valid.)

**4. EXPOSITION (§4.3, (4.10)).**
> "The progression relation before taking residues implies δ0 = δ1 + uP, δ2 = δ1 + vP, u, v ∈ {−1, 0, 1}."

The reason u, v ∈ {−1,0,1} (each |δ_i| < P, so |δ0−δ1| < 2P) is only stated later, in Lemma 7.1's proof. Fine, but it belongs here.

**5. EXPOSITION ((5.2)).**
> "Equality of buckets implies y + 1 < 2(x + 1), x + 1 < 2(y + 1)."

x and y are never introduced. It should read "if β(x) = β(y) then …". The inequality itself is correct, and so is its integer form (5.5), r1 ≤ 2r0 etc.

**6. EXPOSITION ((6.5), second inequality unproved in prose).**
> "With r = ⌈log2(m+1)⌉, elementary estimates give D_N ≤ 2^{mr+2m+1} ≤ 2^{5m√m}."

The second inequality has no argument in the paper. The Lean route is ⌈log2(m+1)⌉ ≤ 2⌊√m⌋ (`clog_two_succ_le_two_mul_sqrt`), then mr + 2m + 1 ≤ 5m⌊√m⌋. Lean uses `Nat.sqrt`. The paper's real-√ bound is weaker, so it follows. I verified both versions for every m ≤ 3000. The floor version is tight at m = 1, 2, 3 (4 ≤ 5, 9 ≤ 10, 13 ≤ 15). One sentence would fix this.

**7. EXPOSITION ((6.6) compressed).**
> "The threshold gives s ≥ T, while m = s+1 ≤ 2s, so (Am + B0)K ≤ s² ≤ q − 1."

The skipped chain is (Am+B0)K ≤ (2A+B0)sK ≤ 2(A+B0)K·s ≤ T·s ≤ s². It uses s ≥ 1 and A, B0 ≥ 0. It is correct.

**8. EXPOSITION (Theorem 1.2 / (1.3): redundant max).**
> "N > max{2^{(76k)²}, 2^{(40k)⁴}}"

(40k)⁴ = 2,560,000 k⁴ > 5,776 k² = (76k)² for every k ≥ 1 (checked k < 1000, and it is obvious). The first entry never binds, so the hypothesis is just N > 2^{(40k)⁴}. This is harmless, but it suggests two competing regimes that do not exist. Lean's `explicitUnifiedOneThirdThreshold` keeps the same redundant max.

**9. EXPOSITION (why 24?).** The proof uses only two properties of the modulus M:
- (a) if E ≠ 0 and |E| ≤ 3(P−1), then MP ∤ E. This needs M ≥ 3 (Lemma 4.1: "|E| < 3P < 24P").
- (b) M is even and P is odd (the parity step (4.11)).

M = 4 with P = 4B+1 satisfies both, and the proof goes through word for word. A reader looking for where 24 is actually used will find nothing. This is not an error ("no optimization … is intended"), but one sentence would help. I tested the generalisation; see "What I verified, §(ii)".

**10. EXPOSITION (notation collisions in the same few paragraphs).**
- u: wrap index in (4.10) and Lemma 7.1, but the high digit in (7.2) and in "q_j = s_j + p u_j".
- d: AP step (1.1), region difference b − a (Lemma 7.1), and constant coefficient of f (7.8).
- a, b: outer/inner regions in Lemma 7.1, then cubic coefficients with a = N(R) in (7.8).
- D: ‖R‖² in (4.13)/(5.6), D(B,L) in (5.7), D_N, and the digit vector D̄_p.
- q: palette size in Definition 1.1, and clog2 N in §6/§7.3.
- β: weight in Lemma 4.1, and bucket in (5.1).

None of these causes an error, but each costs a careful reader a re-read.

**11. EXPOSITION (edge horizons).** (6.1) at N = 1 has q = 0 and √(q−1) undefined over ℝ (Lean uses truncated subtraction). (7.13) is stated "If N > 1", yet (7.14) is then used without that condition. At N = 1, (7.14) holds anyway (p = 5: (45)³ = 91,125 < 2,985,984). None of this matters for Theorem 1.2, where N > 2^{2,560,000}.

**12. EXPOSITION ((8.5) framing, minor).** "Even this fixed specialization improves the exponent recorded" is correct as an O-statement (H(N) = O(N^{7/20})). For k = 60, though, the explicit inequality only applies for N > 2^{(2400)⁴} ≈ 2^{3.3·10¹³}. A reader may want that caveat next to the sentence.

Out of scope, flagged only: the docstring of our own `check_itabe.py` says that Shi–Dong's Theorem 1.1 (L=3, one norm layer) "predicts the same" ABBA-freeness for the cubic norm factor. The paper cites no Shi–Dong and says a non-exhaustive search found no prior source. I did not check this; the novelty seat should.

---

## What I verified (checklist)

**1. §2 classification** — complete. With at most two values and no value three times, there are exactly two values, each used twice; with the first position named A, the only shapes are AABB, ABAB, ABBA. ABBB/BAAA/AAAA etc. are three-equal and handled by λ.
Exhaustive check over {0..3}⁴: tuples with ≤2 values, no three-equal, not ABAB, not AABB, and not proper ABBA → **0**.

**2. Quotient descent** — valid for any homogeneous linear identity Σc_j n_j = 0 with integer c_j (signed). Subtract the exact residue identity and divide by P. The relations used are:
- n0 − 2n1 + n2 = 0 and n1 − 2n2 + n3 = 0 (ABAB, AABB, ABBA);
- αx + βy − (α+β)z = 0 (three-equal).
The top digit equals the final quotient because Q_L(n) < P.

**3. Lemma 4.1** — α+β ≤ 3 gives |E| ≤ (α+β)(P−1) ≤ 3(P−1) < 3P < 24P. gcd(24B+1, 24) = 1. The needed (α,β) are (1,1), (2,1), (1,2).
- 013: 2x0 + x3 = 3a + 3d = 3x1 ✓.
- 023: x0 + 2x3 = 3a + 6d = 3x2 ✓.

Exhaustive over all residue triples, all three weight pairs:
- P = 25, 49, 73, 97, 121 at mod 24: **0 violations**.
- Generalised moduli: mod 4 (P = 5, 9, 13), mod 6 (P = 7, 13), mod 3 (P = 7, 10): 0 violations.
- Control mod 2 (P = 5, 9, 7): **4, 16, 8 violations**, as the 2P ≤ 3(P−1) bound predicts.

**4. Norm step (4.9)** — the expansion gives αX² + βY² + (α+β)Z² − 2Z(αX+βY). With αX + βY = (α+β)Z this becomes αX² + βY² − (α+β)Z² ✓; it does need the coordinatewise relation, which (4.8) supplies. Summing and using equal norms gives 0, so X = Y = Z. The vectors are full fixed-length vectors including the top digit, so the integers are equal, which is impossible for a nontrivial AP.

**5. ABAB** — (4.11): 2r1 − r0 − r2 is even (r0 ≡ r2 mod 24 ⇒ mod 2) and P is odd, so u = 0. Likewise r3 + r1 − 2r2 is even, so v = 0. In (4.13):
- ‖X+2R‖² − ‖X‖² = 4A + 4D ✓;
- ‖X+3R‖² − ‖X+R‖² = (6A+9D) − (2A+D) = 4A + 8D ✓.
Hence 4D = 0.

Exhaustive residue check (congruent steps, ABAB congruences ⇒ exact AP):
- P = 25, 49, 73 at mod 24: **0 violations**.
- mod 4 (P = 5, 9), mod 6 (P = 7), mod 2 (P = 5): 0.
- Control: odd modulus 3 (P = 7, 10, 4, 9): **4, 14, 4, 18 violations**, as predicted by the parity step.

**6. Lemma 5.1** — I re-derived every case (u = −1; u = 1 with v ∈ {−1,0,1}; u = 0 with v = ±1), and each inequality follows as written. Exhaustive over **all bases B = 1..72 and B = 128**, all r0, r1, r2 (r3 is determined): **0 violations**. The lemma holds for every base, not only powers of 2. Control (floor(log3(r+1)) buckets, ratio 3 instead of 2): violations for B = 2, 4, 5, ….

**7. (5.6)** — Q(0) = Q(1) ⇒ 2A + D = 0. Q(2) = Q(3): (4A+4D) − (6A+9D) = −2A − 5D = 0, i.e. 2A + 5D = 0, as printed ✓. Subtracting gives 4D = 0.

**8. §6 arithmetic** (exact big-int):
- q ≤ m² for every q ≤ 4000.
- S_N ≤ 2^{8m+11} for every m ≤ 3000; the sub-steps 24^{m−1} ≤ 2^{5m}, P ≤ 2^{m+5}, mP²+1 ≤ 2^{3m+11} all check.
- D_N ≤ 2^{mr+2m+1} ≤ 2^{5m√m} (both floor and real √) for every m ≤ 3000.

Thresholds at the smallest admissible q:

| k | (6.7): (8m+11)·2k vs q−1 | (6.8)/(6.9): 5(s+1)⌊√(s+1)⌋·2k vs s² | exact 2k·log2 D_N vs q−1 |
|---|---|---|---|
| 1 | 1254 ≤ 5776 | 640,400 ≤ 2,560,000 | 40,491 < 2,560,000 |
| 2 | 4940 ≤ 23,104 | 10,241,600 ≤ 40,960,000 | 374,953 < 40,960,000 |
| 3 | holds | holds | holds |

For (6.8)/(6.9) the real-√ value is 640,600 for k = 1, also ≤ 2,560,000. The "(6.8) D_N^K < N" claim at the K = 2 threshold is correct, with large slack.

Whole theorem in log₂ at N = 2^{(40k)⁴} (+), with p at the Bertrand upper end 2y:
- k = 1: 3k·log2(S·D·U) = 2.65·10⁶ vs log2(C^k N^{k+3}) ≥ 1.02·10⁷.
- k = 2: 8.27·10⁷ vs 2.05·10⁸.

**9. Lemma 7.1** — (7.5) re-derived: 2(bp+e1) − (ap+e0) − (bp+e2) = 3up gives (d−3u)p = e0+e2−2e1 ✓, and the second identity likewise. The right-hand sides lie in [−2(p−1), 2(p−1)] ⊂ (−2p, 2p) ✓. The (d, u, v) table is exactly right. The d = ±2 rows are killed by e0+e3−e1−e2 < 2p (resp. e1+e2−e0−e3 < 2p) ✓.

Exhaustive over **all integers p = 2..60** (primality is not used): **0 violations**. Controls:
- halves instead of thirds: violations for p = 3, 4, 5, …;
- outer equality only, p = 11: 26 violations.

**10. §7.2** — f(3) − f(0) = 27a + 9b + 3c; f(2) − f(1) = 7a + 3b + c; first − 3·second = 6a ✓. p > 3 ⇒ 6 ≠ 0 ⇒ N(R) = 0 ⇒ R = 0. Reduction mod p keeps R ≠ 0 because each coordinate of the integer step has |·| < p ✓. The leading coefficient is det(M_R) = N(R) ✓.

Full ν_p (thirds of the two low digits + F_{p³}/F_p norm under a random F_p-linear ι, random irreducible cubic):
- p = 13 on [0, 2197): palette 109 ≤ 117, **0** ABBA-equality APs.
- p = 17 on [0, 4913): palette 145 ≤ 153, **0**.
- `check_itabe.py` adds p = 5, 7, 11, interval and cyclic: 0, with the no-norm and isotropic controls firing.
- p = 2, 3: also 0, but uninformative — no no-wrap integer 4-AP of digit vectors exists for p ≤ 3, so that control cannot fire.

**11. §7.3** — for q = 1..399: y > 3, N ≤ y³, 3e ≤ q+8, y³ ≤ 2^{q+8} < 512N, (2y)³ < 4096N at the worst N = 2^{q−1}+1 ✓. With the actual Bertrand prime (`nextprime(y)`) for q ≤ 120: p ≤ 2y, p > 3, N ≤ p³, (9p)³ < C·N ✓. **729·4096 = 2,985,984** ✓.

**12. §8, §9** —
- (8.2) holds: the product of available codomains is S_N·D_N·U_N.
- (8.3): (S D)^k < N cubed gives N³, and U³ < CN raised to the k gives (CN)^k ✓.
- (8.4) (k+3)/(3k) = 1/3 + 1/k ✓. 63/180 = 7/20 ✓. 22⁷ = 2,494,357,888 < 3²⁰ = 3,486,784,401 ✓.
- §9: compressing a good colouring to its image, splitting a fibre of size ≥ 2 into a fresh colour (keeps goodness and surjectivity), minimality, and H ≥ 3 for N ≥ 4 all check. The literal "two distinct nonempty parts" equivalence also checks (k ≥ 2 and surjectivity supply the second part).
- Brute force N = 4..7: H = 3, h_E = 2 under both the at-most-two and the literal readings, so H = h_E + 1 ✓. (H = 3 throughout; `exact_h.tsv` independently has H(13) = 4 with 3 colours UNSAT.)

**Prose ↔ Lean correspondence (spot-checked):**
- The "shared" label is genuinely one function: `horizonNoThree_eq_horizonABAB : … := by rfl`.
- The final palette is `NoThreeMod24Palette × DyadicSquarePalette × ((Fin 3 × Fin 3) × ZMod p)`, with card = S_N·D_N·9p, matching (8.2) — no double-counted mod-24 factor.
- Parameters match (6.1): `aabbDigitCount N = Nat.sqrt (clog 2 N − 1) + 1`, base 2^m, P = 24·2^m + 1.
- `dyadicBucket r = Nat.log 2 (r+1)` and the thirds regions match (5.1)/(7.1).
- The cubic prime comes from Bertrand with p ≤ 2·cubicScale.

### What I verified, §(ii) — note on the existing instrument

`~/MathDyad/erdos160/check_itabe.py` currently ends **`RC 2`** (its own "cannot see" code). The cause is its mod-24 control (the label with the mod-24 digits removed): it produces **0 three-equal APs** at P = 25 and 49 with L = 1, so the control never fires there.

Those mod-24 rows are also close to vacuous. At brute-forceable horizons the real λ label is almost injective: palette 624/625 (P=25, L=1), 2321/2401 (P=49, L=1), 15552/15625 (P=25, L=2). This is structural: with P = 24B+1, λ_{P,L} only stops being near-injective once P^{L−1} ≳ 24^L(L+1), i.e. at horizons like 49¹⁰.

The non-vacuous evidence for λ's proof logic is the generalised-modulus run in `labels.py`. It is the same proof with 24 replaced by M:

| M | P | L | N | palette | three-equal | ABAB |
|---|---|---|---|---|---|---|
| 4 | 5 | 4 | 3125 | 2304 | 0 | 0 |
| 6 | 7 | 3 | 2401 | 2160 | 0 | 0 |
| 4 | 9 | 3 | 6561 | **3107** | 0 | 0 |
| control 2 | 5 | 3 | 625 | 187 | **22** | 0 |
| control 3 | 7 | 3 | 2401 | 1126 | 0 | **138** |

Each control breaks exactly the step the proof predicts: M < 3 breaks Lemma 4.1, and an odd M breaks the parity step.

The μ label in the non-injective regime: B = 4 with L = 4 and 5, B = 16 with L = 2, B = 32 with L = 1, plus non-power-of-2 bases B = 6 with L = 3 and B = 12 with L = 2. Palettes run ~50–75 % of N (e.g. 2124/4096). **0 AABB** (equality version, AAAA included).
