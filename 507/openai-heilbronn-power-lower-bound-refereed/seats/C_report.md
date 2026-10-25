# Seat C (compute) — hostile referee report
## OpenAI, "A power improvement in the Heilbronn triangle lower bound" (25 Sep 2026), Erdős #507

Role: decorrelated second instrument. Every finite, checkable claim listed in my brief was tested by exact
computation on scaled-down instances, each with a **positive control** (the checker passes on the true
statement) and a **mutation control** (a deliberately broken statement or input the checker must reject).
Both outcomes are printed for every check below.

All code and raw output: `/tmp/oaimath/191/seats/C_work/` (`checkN_*.py` → `checkN_*out.txt`). Every script
was run as `bash -c 'ulimit -v 4000000; exec timeout 900 python3 <script>'`. Arithmetic is exact throughout:
Python big integers, finite-field tables, or numpy int64 with magnitudes bounded well below 2^63 (one
int64 overflow in a random-GL3 sampler in check 4 was caught by the runtime warning, fixed to exact Python
ints, and the check re-run; the figures below come from the corrected run). No instrument is shared between
checks. Checks 5 and 8 first borrowed check 2's determinantal-divisor routine; I replaced it with local
brute-force index computations and re-ran both, with identical results.

What compute cannot settle: asymptotic "≪" constants, the regime q ≈ h^100, and the real parameters
(d = 41; k has 232 digits). For "≪" claims I report the normalised ratio across a range of sizes and show
it does not grow, and I show that a mutated normalisation does grow. That is evidence, not proof.

---

### Summary table

| # | Paper claim (printed numbering) | Positive control | Mutation control |
|---|---|---|---|
| 1a | (3.5)–(3.11), Lemma 3.3, d = 1 full digit encoding | 0 failures; obstruction holds on 7,630 distinct-label triples | position break → identity fails on every distinct-label triple, 5 obstruction counterexamples; small base → 89–394 counterexamples |
| 1b | (3.6)/(3.7) matching with T > 1 (synthetic T = 4, k = 17) | 0 failures (identity, coefficient bound, obstruction) | ℓ_a = T²−Ta → identity fails 453–825×/run; small base → 20–59 obstruction counterexamples |
| 1c | Lemma 3.1 + (3.2)/(3.4), d = 3 over F_{r³}, r = 3,5,7 | full 165³ tensor in F_r, antisymmetric, zero on repeats; T-sum = N at 180/180 points per r | d = 2 (even): fails; perturbed slot: fails; no Frobenius: leaves F_r |
| 2 | Lemmas 4.1–4.2, h = 4 (all 4⁹), 8, 9, 25, 27 | index = DE, EZ³ ⊆ Λ, b-characterisation, elimination: 0 failures; worst \|O_C\|D³E²/h⁸ = 0.65625 ≥ 21/64 | D²E² bound violated; bound without det-image factor violated |
| 3 | Lemma 4.3, (4.5)–(4.6), exact | 0 violations over all r⁹ prescriptions at j = 1; bound **attained exactly** in one case | shared digits for repeated labels → Pr = 1; hypothesis L < B dropped → violated |
| 4 | Lemma 5.1, Lemma 5.2 | Γ cap for q ≤ 17; paper constants for H = 1,2,3; dense stress H = 2,3: 0 violations | split quadric → collinear; a ∉ A → short relations / 0 ∈ V |
| 5 | Lemma 7.3 (7.4), R ≥ h | max Σg³/(R³I) = 25.98 over h ≤ 32; pointwise (7.2) and density formula exact | drop I → ratio ∝ I (up to 25,000); R < h → ratio up to 2,048 |
| 6 | Lemma 2.4 | ratio to (R₁R₂R₃)²(log 2R₁)² ≤ 53.3, no growth to R = 8 | one fewer power of R₃ → ratio grows linearly in R₃ |
| 7 | §8 arithmetic (8.1)–(8.8) | α = 45435k+16, β = (3029k+1)/2, η = 2/α reproduced symbolically and on exact toys | wrong β fails 18/18 toy instances |
| 8 | (extra) Prop 2.5 I² saving; Lemma 6.1 | count·I²/(X⁶log²) ≤ 39 and *decreasing* in I; pairs/N³ → 1.15 | I³ saving rejected (ratio ∝ I); N^2.5 rejected |
| 9 | (extra) App. A threshold; §8 every-n interpolation | Bertrand verified n ≤ 2·10⁵; interpolation 0 violations | C_k with 2^α instead of 4^α violated 1,463× |

No check produced a counterexample to any statement as the paper writes it.

---

### Check 1 — the determinant obstruction (§3)

**1a. d = 1 end to end** (`check1_encoding.py` → `check1_out.txt`). K = F_r, M = 3, T = 1, k = 2; label
coordinates X(ξ) = (1, ξ, ξ²); N = the Vandermonde determinant; (f₁₀, f₂₀, f₃₀) = (1·X₁, X₂, X₃); positions
(i₀, j₀, ℓ₀) = (0, 0, 1) as in (3.6). **Changed from the paper:** L = r² instead of r¹⁰ (so L/r = r digit
choices per residue). The base is B = nextprime(100k²L³), so B − 1 ≥ 100k²L³, L < B and r | L all still
hold. Every sampled triple has fresh digits per column, as in (3.8).

For each triple I computed γ(Y) exactly (polynomial determinant), S_C, and det C mod h = B^k. Then I checked:
- (I1) γ_{k−1} ≡ N(labels) (mod r);
- (I2) |γ_u| ≤ 6k²L³ (3.9);
- (I3) S_C ≡ det C (mod h);
- (OB) labels distinct ⇒ no representative of det C in [−τ, τ].

| r | L | B | samples | I1/I2/I3 fail | distinct-label triples | OB fail | repeated-label triples with a rep in [−τ,τ] |
|---|---|---|---|---|---|---|---|
| 3 | 9 | 291619 | 20000 | 0/0/0 | 2253 | **0** | 237 / 17747 |
| 5 | 25 | 6250009 | 12000 | 0/0/0 | 2930 | **0** | 8 / 9070 |
| 7 | 49 | 47059613 | 8000 | 0/0/0 | 2447 | **0** | 0 / 5553 |

**Repeated-label examples, as the brief asked: they exist.**
- r = 3, labels (0,2,0): γ₁ = 0 and det C ≡ 0 (mod h), i.e. a genuinely zero determinant residue.
- r = 5, labels (2,4,4): centred determinant 145.

So the obstruction really does need distinct labels, and the r^(−d) accounting for collisions (end of §3,
(4.8), Cor 6.4) is doing real work rather than covering an empty case.

**Mutations (all rejected):**
- **M1, row-3 position moved 1→0** (the designated triple no longer sums to k−1). I1 fails on every
  distinct-label triple (2163, 2851 and 2480 failures). At r = 3 the obstruction itself fails 5 times, e.g.
  labels (0,2,1), γ₁ = 0, centred determinant −83.
- **M2, base inequality dropped** (B = nextprime(L) = 11, 29, 53). OB fails 394, 194 and 89 times, e.g.
  labels (0,2,1) with det C ≡ −1.

**1b. Matching with T > 1** (same script). Synthetic T = 4, k = 17: label coordinates y(ξ) = (1, ξ, ξ², ξ³);
the four monomial triples p<q<s with scalars c_a; P = Σ c_a det[y_p; y_q; y_s]. Two coefficient choices:
- c = (1,0,0,0): P = Vandermonde, and three slots carry scalar 0 but nonzero rows 2 and 3, exactly the
  situation Lemma 3.1 allows;
- c random.

Positive controls, r = 3, 5, 7, 2000–3000 triples each: 0 failures of I1, I2, I3 and OB.

**Mutations (rejected):**
- **M3, ℓ_a = T² − Ta** (drops the "+1"). Unmatched triples (0, a′, a′) now hit k−1, and I1 fails 453–825
  times per run. The obstruction itself was never observed to fail under M3, because that needs
  γ_{k−1} = 0 exactly, which is rare. The identity failure is the operative rejection.
- **M4, small base.** OB fails 20–59 times per run.

**Matching (3.7), exhaustive** for T ∈ {1,2,3,4,5,7,10,20}: exactly T solutions, all matched, and 0
unmatched. The M3 positions give T − 1 unmatched solutions.

**1c. Lemma 3.1 for d = 3** (`check1_norm.py` → `check1_norm_out.txt`). K = F_{r³} (irreducible cubic,
polynomial basis β_ν = ω^ν), 9 variables per group, M = C(11,3) = 165. I computed the **full coefficient
tensor** c[p,q,s] (165³ entries in K) by expanding the three trilinear factors σ^j(D), j = 0, 1, 2. This
uses nothing from the paper's argument.

| r | coeffs in F_r | zero when two indices coincide | antisymmetric | tensor = Nm(det) (instrument control) | T-sum = N, random points | T-sum = N, label points | nonzero slots of T = 735130 | (3.4) on distinct label triples |
|---|---|---|---|---|---|---|---|---|
| 3 | yes | yes | yes | 15/15 | 120/120 | 60/60 | 29985 | all 17550: det = Vandermonde, Nm ≠ 0 |
| 5 | yes | yes | yes | 15/15 | 120/120 | 60/60 | 40187 | 20000 sampled: same |
| 7 | yes | yes | yes | 15/15 | 120/120 | 60/60 | 42995 | 20000 sampled: same |

**Mutations (rejected):**
- **d = 2 (even), r = 3, 5, 7.** The tensor is not zero on repeats and not antisymmetric, and the T-term sum
  matches N at only 8, 5 and 5 of 40 random points.
- **One nonzero slot perturbed by +1.** Mismatches at 6, 23 and 22 of 40 points.
- **No Frobenius (N′ = D³).** The coefficients leave F_r, and check (a) fails.

The r = 3 case confirms the paper's remark that no division by 3! is needed.

### Check 2 — Lemmas 4.1–4.2, residue orbits (`check2_orbits.py` → `check2_out.txt`)

D and E come from the **determinantal divisors** of the integer matrix [C̃; hI]. The index comes from brute
force, h³/|{x·C}|, and E·Z³ ⊆ Λ_C from brute-force membership. The paper's own elimination (proof of
Lemma 4.1) is implemented literally and checked: C = P·diag(1, B^b, B^e)·Q with P and Q invertible, and
(b, e) equal to the divisors.

Orbits are computed two ways:
- **h = 4, exact:** a union-find partition of all 4⁹ = 262144 matrices under the generators E_ij(1). The
  positive control is that |orbit(I)| = 43008 equals the brute-force count of det ≡ 1.
- **h ≥ 8:** |SL₃(Z/h)| / |Stab_SL(C)|, with the stabiliser counted by brute force over (Ann_left C)³. This
  route was cross-checked against the exact h = 4 partition (400/400 agree). For 4 top-class matrices
  (h = 25, 27) it was replaced by the diagonal-form count, itself cross-checked against brute force
  wherever both run (0 mismatches).

|SL₃(Z/8)| = 11,010,048 and |SL₃(Z/9)| = 36,846,576 by brute force.

| h | matrices | index = DE / EZ³⊆Λ / b ⇔ minors / elimination | worst \|O_C\|D³E²/h⁸ (claim ≥ 0.328125) | D²E² mutation violations | no-det-image mutation violations |
|---|---|---|---|---|---|
| 4 | all 261632 with a unit entry | 0 / 0 / 0 / 0 (3000 sampled) | 0.656250 | 1568 | 86016 |
| 8 | 640 (600 random + 4 per class, all 10 classes) | 0 / 0 / 0 / 0 | 0.656250 | 13 | 417 |
| 9 | 624 (all 6 classes) | 0 / 0 / 0 / 0 | 0.855967 | 25 | 511 |
| 25 | 262 (all 6 classes) | 0 / 0 / 0 / 0 | 0.952320 | 6 | 244 |
| 27 | 170 (all 10 classes) | 0 / 0 / 0 / 0 | 0.855967 | 12 | 156 |

The exact worst ratio is (1−B⁻²)(1−B⁻³) in every class except D = E = h, where it is 1−B⁻³. That is
≥ 2 × (21/64) for every B, so (4.2) holds with c₀ = 21/64 and room to spare.

Both mutations are rejected:
- (4.2) with D²E² in place of D³E² is false (e.g. the D = E = h classes).
- Dropping the det-image factor (4.4) is false already at C = I.

The factor E/h in (4.4) is load-bearing and the paper includes it.

### Check 3 — Lemma 4.3, conditional digit estimate (`check3_tail.py`, `check3_control.py` → `*_out.txt`)

The event b ≥ j depends only on digits at positions u < j, so Pr(b ≥ j | prescription) is computed
**exactly** by enumerating all (L/r)^{9j} digit choices.

- **j = 1, every prescription.** For P1 (B=5, r=2, L=4): all 512, max Pr = 0.02734 ≤ (r/L)⁴ = 0.0625.
  For P2 (B=7, r=3, L=6): all 19683, max Pr = **0.0625 = (r/L)⁴ exactly**, attained by the all-residue-2
  prescription (32/512). For P3 (B=11, r=2, L=8): max 7.5·10⁻⁴ ≤ 3.9·10⁻³. **(4.5) is sharp**: there is
  no slack anywhere in it, and it is not violated.
- **j ≤ k.** Construction-induced prescriptions (all label triples, repeats included) plus random and
  structured ones: 0 violations, max Pr/bound = 0.4375.
- **P4 (k=3), j = 3.** 0/134,217,728 for one prescription.
- **(4.6).** Max exact E[D] is 1.1188 (P1) against the bound 1.4102 ≤ 1/(1−θ) = 1.4545, and 1.1839 (P2)
  against 1.6289 ≤ 1.7778.
- **Instrument control (`check3_control.py`).** Exact against 3·10⁶-sample Monte Carlo on nonzero cases:
  all within 1.3 standard errors. The first control in `check3_tail.py` happened to hit a zero-probability
  prescription, so it was replaced.

**Mutations:**
- **Three repeated labels sharing one digit draw** (the paper prescribes fresh digits). Pr(b ≥ j) = 1 for
  every j: rejected.
- **Two columns sharing a draw.** Pr = 0.156 against a bound of 0.0625 (P1, j=1): rejected.
- **Hypothesis L < B dropped** (B=3, L=4). Violated (0.0977 > 0.0625).
- **Exponent 5j in place of 4j.** Rejected on P2.

Conclusion: "fresh independent digits even when their labels coincide" (end of (3.8)) and L < B are both
load-bearing, and both are in the paper.

### Check 4 — §5 cap and shifts (`check4_cap.py`, `check4b_literal.py` → `check4*_out.txt`)

**Γ, exhaustive, q = 5, 7, 11, 13, 17 with ν a nonsquare:** 0 lines carry three points.
- Mutation ν = 1 (split quadric): 10/14/22/26/34 rich lines, up to q points each.
- Mutation ν = 0: q rich lines.

**Paper constants** (q ≥ 2000H², w = ⌊q/(1000H²)⌋), shift chosen with |S| ≥ w³/q:

| H | q | w | \|S\| (w³/q) | rich lines in S | Pr(a₁ ∉ A) vs union bound | \|A\|/q³ | \|V\|=\|S\|, 0∉V, rich lines in V | short relations, \|x\| ≤ H, exhaustive |
|---|---|---|---|---|---|---|---|---|
| 1 | 2003 | 2 | max over all q³ shifts = 4 (0.004) | 0 | — | 0.9865 | yes, yes, 0 | 0 |
| 1 | 1000003 | 1000 | 1048 (1000.0) | 0 | 0.0130 ≤ 0.0180 | 0.9870 | yes, yes, 0 | trivial (x = ±e_i) |
| 2 | 4000037 | 1000 | 260 (250.0) | 0 | 0.0114 ≤ 0.0180 | 0.9886 | yes, yes, 0 | 0 (16 vectors up to sign) |
| 3 | 9000011 | 1000 | 121 (111.1) | 0 | 0.0117 ≤ 0.0180 | 0.9884 | yes, yes, 0 | 0 (61 vectors up to sign) |

At q = 2003 the exact average |S| over all q³ shifts equals w³/q to six digits, which is the averaging
step of Lemma 5.1 checked directly.

**Stress test.** Same logic, but with a dense cap that keeps 3Hw < q/2: H=2 with q=20011, w=250, |S|=801;
H=3 with q=60013, w=300, |S|=455.
- Positive control: 0 short relations, 0 rich lines, 0 ∉ V.
- Mutation a = 0 (∉ A): 6 forbidden relations at H=2 (e.g. x = (−1,−1,1), Σx = −1). It found 0 at H=3; a
  bad shift does not always manufacture one.
- Mutation a = −v: 0 ∈ V and 21 relations at both H.
- Mutation split quadric: 241 and 60 rich lines.
- Mutation random points with no cap property: 21 relations at H=3, but 0 at H=2. The 0 is correct
  mathematics, not instrument blindness: for H < √6 every x with Σx = 0 and |x| ≤ H has the shape (t,−t,0),
  so that branch of Lemma 5.2 is vacuous on distinct triples. The cap property first bites at H ≥ √6
  through midpoint relations (1,−2,1).

### Check 5 — Lemma 7.3 (7.4) (`check5_moment.py`, `check5_mutR.py` → `*_out.txt`)

Setup:
- g(x) = gcd(C̃x, h).
- I = DE, computed with this check's own brute-force index (independent of check 2).
- h ∈ {4, 8, 16, 32, 3, 9, 27, 5, 25}; for each, 6 random unit-entry C plus one P·diag(1,B^b,B^e)·Q
  representative of every class.
- R ∈ {h, 2h}, summed over all primitive x with R ≤ |x| < 2R.

Results:
- **Positive:** max Σg³/(R³I) = **25.98** across all h, C and R ≥ h. The ratio is stable at about 24–26,
  close to the count of primitive points per R³ (24.4 at R=16).
- **Pointwise:** g(x) | E (7.2), and B^j | g ⇔ Cx ≡ 0 (mod B^j), with 0 failures. The residue-class density
  B^(−j−max(j−b,0)) for j ≤ e is exact, with 0 failures.

**Mutations:**
- **Drop I.** Max Σg³/R³ grows in proportion to I (25.8 at I=1, 783 at I=32, 25,000 at I=1024): rejected.
- **R < h** (sharpened in `check5_mutR.py` with unconjugated diag(1, B^b, B^e)). Σg³/(R³I) reaches
  **2048.75 at R = 1** (h=32, (b,e) = (0,5)), 1025 at (1,5), 256 at (5,5), and 1459 at h=27. It returns to
  about 24 as soon as R ≥ h.

So the hypothesis R ≥ h is **load-bearing**. The paper meets it only because Lemma 5.2 excludes relations
with |x| ≤ H = h² in the affine case (R > H/2 = h²/2 ≥ h), and that exclusion is checked in check 4. The
equal-pair cases use the pointwise g³ ≤ Ih² plus the q-savings instead, which needs no R ≥ h. This is the
coherent reading, and it holds.

### Check 6 — Lemma 2.4 (`check6_lattice.py` → `check6_out.txt`)

Exact counts of (u₁,u₂,u₃) with |u_j| ≤ R_j and det = t, via det = u₁·(u₂×u₃) grouped by cross product.
Instrument control: identical to direct triple enumeration for (2,2,2), (3,2,1) and (3,3,3).

Configurations: isotropic R = 2…8; anisotropic (8,8,1), (8,8,2), (8,8,4), (8,4,1), (8,4,2), (8,2,1),
(8,1,1), (6,6,3), (8,6,3), (8,8,6); t ∈ {1,2,3,5,6,12,30,60}.

- **Positive:** count/((R₁R₂R₃)²(log 2R₁)²) ≤ **53.26** (max at (3,3,3)), with no upward trend: 35.8 at
  (8,8,8) and 9–37 on the anisotropic boxes. At t = 1 the ratio decreases with R (28.3 → 12.3).
- **Mutation, bound with (R₁R₂)²R₃:** at R₁ = R₂ = 8 the ratio rises linearly with R₃ (13.9, 22.6, 48.8,
  75.7, 98.4 for R₃ = 1, 2, 4, 6, 8), while the paper-normalised ratio stays flat (13.9, 11.3, 12.2, 12.6,
  12.3): rejected.
- **t = 0 contrast:** 58–184, larger, as expected for the excluded case.

### Check 7 — §8 arithmetic (`check7_arith.py` → `check7_out.txt`)

**Symbolic, k free (sympy).** From B ~ r³⁰, h = B^k, q ~ h¹⁰⁰, N = (hq)¹⁰, τ ~ B^{k−1}: the exponent of r
in a_r = r√(N³/τ) is **45435k + 16**. Also:
- β = 15·101k − (k−1)/2 = (3029k+1)/2, matching the paper;
- 1 + 30β = α;
- the second term of (8.2) carries r^{30+2−d} = r^{−9} with d = 41;
- (a_r/2)²·τ/(16N³) = r²/64 exactly, which is (8.5).

**Exact integers:**
- M = C(163,41) = 606759748397114245242771031375422128400 (39 digits).
- T = C(M,3) has 116 digits; T = M(M−1)(M−2)/6 checked.
- k = T²+1 has **232 digits**.
- log₁₀ η = log₁₀(2/(45435k+16)) = **−249.4982**.
- The Lean exponent 1/(100000k) has log₁₀ = **−250.1418**.
- η / (Lean exponent) = 4.40189 = 200000k/(45435k+16).
- **1/(100000k) < 2/(45435k+16): True.** The reversed claim is rejected.

**Toy (8.6), exact big integers** (k = 2,3,4; r = 101, 1009; B uniform in (100k²r³⁰, 200k²r³⁰]; q uniform
in (h¹⁰⁰, 2h¹⁰⁰]): √2·rB^β < a_r ≤ 2¹⁵√3·rB^β held in 18/18 instances. The mutation β = 1515k (forgetting
τ) violates it in 18/18.

### Extras

**Prop 2.5, the I² saving** (`check8_extra.py` → `check8_out.txt`). This is the quantity that Cor 6.4 trades
against |O_C| ≫ h⁸/(D³E²), and an I^1.5 would break the argument. Setup: exact counts of matrices with rows
in Λ_C, lengths ≤ X and det = t·I, over every (D,E) class for h = 4, 8, 9; X ∈ [6,18] with λ₃ ≤ E ≤ X.
- **Positive:** max count·I²/(X⁶ log²2X) by I = 38.7 (I=1), 39.0 (2), 26.4 (3), 25.8 (4), 24.3 (8),
  25.4 (9), 21.3 (16), 18.9 (27), 17.0 (32), 16.4 (64), 14.8 (81). It is bounded and *decreasing* in I.
- **Mutation, an I³ saving:** the ratio grows about linearly in I (38.7 → 1196): rejected.

**Lemma 6.1.** Ordered proportional pairs (equal pairs included) in [0,N)²×[N,2N), divided by N³: 1.226,
1.200, 1.175, 1.161, 1.153 for N = 10, 20, 40, 80, 160. That is ≪ N³. Under the mutated normaliser N^2.5
the ratio grows (3.9 → 14.6).

**Appendix A / §8 interpolation** (`check9_interp.py` → `check9_out.txt`).
- The closing inequality (n/3)log4 > √(2n)·log(2n) + log(2n+1) fails last at n = 467. Bertrand verified
  directly for n ≤ 2·10⁵.
- The every-n step n ≤ n_r ≤ C_k·n with C_k = max(1, 4^α D_k/A_k), using real primes r ∈ (m, 2m] and both
  extreme admissible n_r: 0 violations in 54,030 cases.
- Mutation C_k = 2^α D_k/A_k: 1,463 violations.

So the every-n deduction of Theorem 1.1 (which the Lean does not cover) is arithmetically sound as written.

---

### Objections from the compute seat

No FATAL, no GAP. Classified observations:
1. **EXPOSITION, (4.5).** The tail bound is attained with equality: B=7, r=3, L=6, every digit residue 2,
   Pr(b ≥ 1) = 1/16 = (r/L)⁴. Nothing breaks, but there is no slack in (4.5).
2. **EXPOSITION, Lemma 7.3.** "For R ≥ h" is a genuinely necessary hypothesis. For R < h the moment sum
   can exceed R³I by a factor of order h/R or more: 256 at R = 1 for diag(1,0,0) mod 32, and 2048 for
   diag(1,1,0) mod 32, where the whole plane x₃ = 0 has g = h. The text could say explicitly that the
   auxiliary prime exists to put the affine case in this range. As written it is correct, because the
   affine case only meets R > H/2 = h²/2 ≥ h.
3. **EXPOSITION, Lemma 5.2.** For H < √6 the Σx = 0 branch is vacuous on distinct triples. For the paper's
   H = h² ≥ 4 it is not vacuous, and it held exhaustively at H = 3 under stress.

### Three places I was most suspicious of, and what settled each

1. **Lemma 4.2's constant with the det-image factor in singular classes (e = k).** Settled by exact orbit
   sizes (full partition at h = 4; stabiliser counts at 8, 9, 25, 27, cross-validated). The worst ratio is
   ≥ 2× the claimed 21/64 in every class, and both natural mis-statements (D²E², no det-image factor) are
   false.
2. **Whether Lemma 7.3's moment bound really covers the affine zero-determinant case.** Settled. The bound
   holds at about 26·R³I for R ≥ h, fails by up to 2048× for R < h, and the R ≥ h regime is exactly what
   Lemma 5.2's exhaustively verified short-relation exclusion (|x| ≤ H = h²) delivers.
3. **Repeated labels: Lemma 4.3's (r/L)^{4j} and the obstruction's dependence on distinct labels.** Settled.
   The obstruction is never violated for distinct labels, and repeated labels do produce small or zero
   determinants, so the collision accounting is necessary. (4.5) holds over every prescription at j = 1, is
   attained with equality in one case, and fails as soon as repeated labels share digits, which the paper
   forbids.

VERDICT: HOLDS AS READ. Every finite, checkable claim in §§2–5, 7, 8 and Appendix A that I tested held,
with positive and mutation controls; this is not a proof of the asymptotic ≪ constants.
