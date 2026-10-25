# Hostile referee report: Erdős #188 bundle (`lower-bound-certificates-and-cmxz-audit/README.md`), 2026-10-14

**Verdict.** I could not break either finite certificate, and the CMXZ audit stands. The README cannot be published as written:
§1c is an unfilled placeholder, and §3 makes a claim that depends on it. Three statements about the literature are wrong. Two
of them are the "distinguishing" claims the README makes about its own certificates. The verifier has two coverage holes. The
shipped data happens to pass through both of them cleanly.

---

## FATAL

**F1. §1c is empty, but the title and §3 both rely on it.**
- Title: *"… an audit of the 2026 upper bound, and a negative search at ℓ₆"*
- §1c: *"L6_SECTION_PLACEHOLDER"*
- §3: *"Lower side: the ℓ₆ analogue of Tsaturian's lattice rigidity does not hold — see §1c — so k₁₈₈ ≥ 7 is not reachable by
  the lattice + rotation family at the sizes searched."*

Why this is fatal:
1. The bundle has no ℓ₆ result. `logs/ladder3.log` has only the ℓ₅ line and no `DONE`. The `l6_*` runs in `ladder3.sh` have
   not finished: at 00:55Z, `cadical runs/l6_c6_b6.cnf` had used about 19 CPU-min and `runs/c3_k6.cnf` about 14 CPU-min, with
   empty `.sol` files. `l6_c3_b6` and `l6_c4_*` had also just started.
2. Two ℓ₆ runs did finish: `c1_k6` and `c2_k6` in `ladder1.log`, both SAT. They have no discriminating power, because the ℓ₅
   instances at the same parameters are SAT too (`c1_k5` and `c2_k5`). The apparatus only becomes UNSAT for ℓ₅ at `centers 3`.
   The matched ℓ₆ instance at that size (`c3_k6`) is unresolved, and it is not an easy SAT.
3. A SAT finite instance does not show that "lattice rigidity does not hold". Tsaturian's Lemmas 2.5 and 2.6 say the colouring
   of the lattice is unique. Refuting the ℓ₆ analogue requires exhibiting two inequivalent forced patterns, or a colouring of the
   full lattice. A satisfying assignment of a finite patch does neither.

Fix: either drop the ℓ₆ material (title phrase, §1c, last §3 bullet), or fill §1c with finished runs. Each ℓ₆ run needs its
same-parameter ℓ₅ control, which must be UNSAT for the ℓ₆ SAT to mean anything. Restate the conclusion as "no certificate within
parameters X". Do not call it a failure of rigidity.

---

## GAP

**G1. The "different proof" claim misreads Tsaturian.** The README says the 111-point certificate *"is a different proof of
Tsaturian's theorem — it never uses his Lemma 2.3 rotation (θ₃, cos = 17/18), only the Moser angle"*.

- Tsaturian's Lemma 2.3 rotation is the Moser angle, not θ₃. In that lemma A, F and X are at distance √3 from B; the T₇ cell
  is a √3-lattice and X is the reflection of F in BC. The rotation about B has XX′ = AA′ = FF′ = 1, and the paper says
  X′A′F′ is *"a blue equilateral triangle with side length 3 and red center B"*. Circumradius √3 means the angle is θ_√3, with
  cos 5/6.
- Lemma 2.2 also rotates points at the circumradius √3 of a side-3 triangle, so it is θ_√3 too.
- His only other rotation is the distance-5 step in the proof of Theorem 1.1. That is exactly W2.
- θ₃ (cos 17/18) appears nowhere in the paper; `grep` finds no `17/18`. `ladder2.sh` labels its run *"Tsaturian control: …
  theta_sqrt3, theta_3"*, so the misreading is already in the setup.

So the stated distinguishing feature is false: the certificate uses the same angles as Tsaturian. Fix: say *"uses only θ_√3
(as Tsaturian's Lemmas 2.2–2.3 do) plus the W2 step (his final step); the θ₃ generator we also supplied is never used"*.
Describe whatever genuinely differs, such as the 111-point size and radius 5.21, without the θ₃ contrast.

**G2. The 15-point core is not EGMRSS's figure.** The README says *"The 15-point certificate is EGMRSS's own figure made
explicit"*.

- EGMRSS's proof of Theorem 1′ (egmrss_1975_II.txt around lines 117–132) uses an equilateral triangle a, b, c on C₂ (radius √3),
  with ℓ₄'s *along its sides* (a–d–e–b, where d and e are on C₁). It then rotates a and b, and argues by cases over pairs.
  It has no points at distance √7.
- The core (from `describe_core` plus my dump) uses origin red, which makes 8 unit-circle points blue. It has one √3-point,
  (2,1) = (1.5, 0.866), lying on two ℓ₄'s:
  - [(0,−1), (1,0), (2,1), (3,2)]
  - [(0,1), (1,1), (2,1), (3,1)]
  Each of these ends at a √7-point, and (3,1)–(3,2) is a unit pair. That forces (2,1) red. Its θ_√3-image about 0 is forced red
  the same way, and the two are at distance 1.
- This is a different (and shorter) argument. Fix: describe it as above, without attributing it to EGMRSS.

**G3. The Conlon–Fox number is wrong.** The README says *"Before that: 2.15·10⁹ from Conlon–Fox 2019 Thm 1.1"*.

- CF Theorem 1.1 says: R > 2, K is 1-separated with diameter ≤ R−1, and |K| > 10^{4n} log R. CF state *"we use log to denote
  log base 2"*. CMXZ v2 restates it as *"10^{4n} log₂ R"* and says CF *"implies E² ↛ (ℓ₂, ℓ_{10^{10}})"*.
- With n = 2, K = ℓ_m and R = m, the condition m > 10⁸·log₂ m first holds at **m ≈ 3.1555·10⁹**. At m = 2.15·10⁹,
  10⁸·log₂ m = 3.10·10⁹, which is larger than m, so the condition fails.
- 2.15·10⁹ is the crossover for m > 10⁸·ln m (2.1488·10⁹). Sagdeev's forum figure therefore reads CF's log as natural log.

Fix: *"≈ 3.16·10⁹ from CF Thm 1.1 as stated (log₂); the forum's 2.15·10⁹ reads log as ln; CMXZ quote 10¹⁰"*. Optionally
add that CF's proof inequality gives far better without changing the argument, as CMXZ remark.

**G4. Three cited pieces of evidence are not in the bundle.**
- *"The full ℓ₅ instance was also closed by minisat22 and glucose4 (`logs/`)"*: there is no such log in `logs/`.
- *"cadical's DRAT proof … was checked by drat-trim (`s VERIFIED`)"*: `logs/ts_c3_k5.drat.time` is the proof-generation timing.
  No drat-trim output is shipped.
- *"Negative controls …: … (`lat_k5`); … (`t0_*`); … (`noT3_R8`)"*: none of these CNFs or logs are in the bundle, and
  `config188.py` has no T₃ option, so the noT3 generator is missing.

I re-ran all of them, and every claim reproduces:
- pysat minisat22 and glucose4 both return UNSAT on `ts_c3_k5.cnf` (746,909 clauses), in 1.3 s and 1.2 s.
- `~/.local/bin/drat-trim ts_c3_k5.cnf logs/ts_c3_k5.drat` gives **s VERIFIED** (0.84 s; 244 core clauses, 21 of 194 lemmas).
- `lat_k5` is SAT. `t0_k5` and `t0_k6` are SAT, and so are their `_o` origin-red variants. `t0_k4_o` is UNSAT, as it should
  be. `noT3_R8`, `noT3_R10` and `noT3_R12` are all UNSAT.

So the claims are true but undocumented. Fix: ship these logs and the noT3 generator. Also note that "the lattice alone is SAT
for every k" rests on one file (k = 5). A one-line argument covers all k ≥ 3: red is one class of the proper 3-colouring of
ℤ[ω], so no blue ℓ₃ lies along any lattice line.

**G5. `verify_core.py` does not fully check what it prints.**
- (a) It prints *"runs exact (collinear, unit-spaced, length {k})"* but never asserts `len(ch) == k`. A shorter all-positive
  clause, for example an ℓ₄ clause in a k = 5 core, would be unsound and would still PASS.
- (b) The geometric checks run over `core["pairs"]`, `core["runs"]` and `core["units"]`. The SAT, minimality and UNSAT checks
  run over `core["core_clauses"]`. Nothing asserts that these are the same multiset of clauses. A clause that `mus188.py`
  misclassifies, or a mixed-sign clause, would be solved but never checked geometrically.

My independent checks show both properties hold on the shipped cores: every run has length k, and coverage is equal (16/16 and
126/126). So the certificates are fine, but the verifier as an instrument could pass an unsound core. Fix: add those two
assertions.

**G6. The ≤ 4920 remark has a one-sentence hole at θ = π.** The remark parametrises *"(x₁, y₁, t = tan(θ/2))"*. That misses
θ = π, and the remark is labelled "rigorous (b)".

The polynomials are right. With F(x,y) = ax + by + c and q_j = (x₁ + (j−1)(1−t²)/(1+t²), y₁ + (j−1)·2t/(1+t²)):

  (1+t²)·F(q_j) = (1+t²)(a x₁ + b y₁ + c) + (j−1)(a(1−t²) + 2bt).

This is degree 3 because of the t²x₁ and t²y₁ terms. Its sign equals the sign of F(q_j). With M = s·m ≤ 100m² ≥ N = 3,
Theorem 2.5 applies and gives (50·3·M/3)³ = (5000m²)³.

The progressions with θ = π are missing. Any such progression, read backwards, is a θ = 0 progression, and the all-blue event
depends only on the *set* of cells. So the union bound over the (x₁, y₁, t)-realisable ordered collections already covers every
event, and nothing is lost. But the remark must say so. Fix: add that sentence.

---

## NOTE

- **N1. The field is misstated.** *"Field of all coordinates: ℚ(√−3, √11)"* and *"rebuilds every core point exactly in
  ℚ(√−3, √11)"* are wrong under both readings.
  - The rotation e^{iθ_√3} = (5+√−11)/6 has minimal polynomial 3x²−5x+3.
  - So the complex coordinates lie in ℚ(√−3, √−11). The real coordinates x and y lie in ℚ(√3, √11).
  - ℚ(√−3, √11) contains neither √−11 nor √33. The compositum ℚ(√−3, √11, √−11) has degree 8, checked with sympy.
  - `describe_core.py`'s string "Q(sqrt(-3), sqrt(4d^2-1))" has the same slip; it should be √(1−4d²).
- **N2. "One-off" mischaracterises the paper.** The README says *"(the paper says 6330 — a one-off in the safe direction)"*,
  and the log says *"the proof as written gives every m ≥ 6329"*.
  - The paper's Lemma 3.2 is stated as exp(−0.01557m). With that constant, ln E(6329) = **+0.0042** and ln E(6330) = −0.0101,
    so 6330 is exactly right for the lemma as printed.
  - 6329 needs the unrounded rate −0.0155711263…·m.
  - Fix: *"with the unrounded Janson exponent the crossover is 6329; the paper rounds the exponent to 0.01557, from which 6330
    is exact"*.
- **N3. The remark's numbers can be sharpened.**
  - The exact crossover of 3 ln(5000m²) − 0.0155711m < 0 is **4917**: +0.0054 at 4916 and −0.0089 at 4917. It is also 4917 with
    the rounded rate. So ≤ 4920 is safe but not sharp.
  - With 69.28m lines the crossover is **4840**, not "≈ 4850".
  - Not an error, but p = 1/19 is not the optimal p for the full exponent: p ≈ 0.0416 gives −0.016068 per point, a further free
    gain.
  - On CMXZ's original 4-variable count, the exact 69.28m lines alone give 6227.
- **N4. `verify_core.py` uses the wrong norm formula.** Line 91 uses `d2 = a*a + a*b + b*b`. For ω = e^{2πi/3} the norm is
  |a+bω|² = a² − ab + b². This is harmless for (5,0), but the printed "|P|^2" would be wrong whenever ab ≠ 0. The check is also
  vacuous by design: W2 holds for any point with |P| ≥ 1/2, which is fine, but say so.
- **N5. The negative control is weak.** It perturbs by (1,0) and asks whether the result is still unit. That only tests a gross
  error, and it would misfire if the first pair's difference vector had x-component −1/2, since then |u + (1,0)| = 1. It does
  not test the real risk, which is float-screened near-unit pairs. Fix: perturb one centre or θ by a tiny exact rational and
  require FAIL.
- **N6. `ts3_c6_k5` is float-screened only.** *"… is UNSAT as well"*: there is no core, no exact check and no DRAT for that run.
  Label it as corroboration from a 1e-9-screened instance.
- **N7. The periodic-construction sentences contradict each other as written.** §3 says *"a periodic construction makes
  [the covering statement] finite"* and then *"Lattice-periodic red sets fail outright …"*.
  - The second claim is true for a red set with **one piece per period**: then h = det Λ/|λ_min| ≥ (√3/2)|λ_min| > piece width.
  - It does not exclude periodic sets with several pieces per period, which is presumably what the first sentence intends.
  - "(piece width)" is undefined. State the hypothesis.
- **N8. The m⁵ count is unsupported.** *"a direct count … should be ~m⁵·C"*: label it as a conjecture or heuristic.
- **N9. Several state-of-problem claims are not evidenced in the bundle.**
  - *"The main page still says 10⁷"*: the snapshot captures comments only, not the statement text. It does show "last edited
    14 October 2025".
  - *"teorth database: `open`"*: not in the snapshot.
  - *"Not in the OpenAI 2026-10-06 catalogue"*: no source given.
  - *"10⁷ more or less"*: no source in hand. CMXZ quote Erdős–Graham as *"at most 10000000"*; quote that instead.
  - Separately, Alfaiz's comment says *"4 ≤ k ≤ 6330"*, a stale lower bound. The README is right not to repeat it.
- **N10. Tsaturian's Lemma 2.2 typo is real, and the forum fix is incomplete.**
  - The statement should say side length 3, not √3. With side √3 the circumradius is 1, which makes the statement vacuous.
  - The proof's opening *"Suppose that blue points A, B and C"* must also read **red**. Otherwise *"Then A′, B′, C′ are blue"*
    does not follow.
  - The README does not depend on this. It is noted for completeness.
- **N11. Wording on d².** *"with d² a norm in ℤ[ω] (so that the rotation sends lattice points at distance d to unit-distance
  partners)"*: θ_d does that for every d > 1/2. The norm condition only ensures lattice points exist at distance d.
- **N12. One run is unreported.** `ladder1` `c3_k5` (ds √3, 3, 5; centres within 3; origin red; **no** W2 unit) is UNSAT. The θ₅
  generator effectively internalises W2. This is harmless, and arguably worth a line.

---

## HOLDS AS READ: what I checked

**1. W1 and W2 are sound.**
- W1: a colouring with no blue ℓ_k has a red point, so translate it to 0.
- W2: if P is red, then ρ_d(P) is blue, with |P − ρ_d P| = 2d·sin(θ_d/2) = 1. Replace c by c∘ρ_d. This fixes 0, is an isometry,
  and makes P blue.
- Only one rotation freedom is used. The lattice and its rotated patches are fixed point sets, and only the colouring is moved.
- cos θ = 1 − 2sin²(θ/2) = 1 − 1/(2d²), and sin θ = √(4d²−1)/(2d²). Both signs of the rotation are sound, because each rotated
  point is just a fixed point whose constraints are checked exactly.
- Restricting a plane colouring to P satisfies every pair clause and every run clause, so the certificates prove the statement
  for **all** plane colourings, not just lattice ones.

**2. Exact re-check, independent of sympy.** I wrote my own checker using Fraction arithmetic on the basis {1, √3, √11, √33}.
It rebuilds every point from (a, b) and the rotation word, matches the floats to 1e-9, and parses `core_clauses` directly.
- EGMRSS core: 11/11 pairs have squared distance exactly 1. All 4 runs are exactly unit-spaced and collinear with length 4.
  The only unit clause is the origin, positive. Max radius √7.
- Tsaturian core: 95/95 pairs and 29/29 runs pass. The units are origin (+) and (5,0) (−), the latter a base-lattice point
  with empty rotation word. No duplicate points. Max radius **5.2074**.
- The only generator used is θ_√3, at 9 centres with the signs listed. That gives 46 Eisenstein points plus 65 rotated points.
  "θ₃ never used" is true.

**3. Propositional checks.**
- Both cores are subsets of the bundled instances: 16/16 and 126/126 clauses.
- The cadical binary returns UNSAT on both cores. Brute force on the 15-variable core finds 0 of 32,768 assignments satisfying.
- `verify_core.py` gives PASS on both cores, with minimality 16/16 and 126/126.

**4. Reproducibility.** `config188.py` with the README flags regenerates **byte-identical** `egmrss_k4.cnf` (1099 / 3108 / 2682)
and `ts_c3_k5.cnf` (76,861 / 519,756 / 227,151). drat-trim returns VERIFIED, and minisat22 and glucose4 return UNSAT, on the
full instance.

**5. CMXZ §3.1, recomputed.** The audit's "HOLDS AS READ" is correct, apart from the N2 wording.
- v₂ = (3/4, √3/4) gives a hexagonal lattice with spacing √3/2, circumradius 1/2 and diameter 1−ε.
- |z(D)| = 18: rings at 0.866 (gap 0), 1.5 (gap 0.5) and 1.732 (gap 0.866). The √7 ring has gap 1.32, and the 3s ring has gap
  1.73.
- Wall-line spacing is √3/4 ≈ 0.433 ≥ 1/3. The line count 90m + 3 ≤ 100m.
- |P₀| radius 3.44m ≤ 7m/2, and L‖u‖ = 3m·0.866 > m + 4.
- (1250m²)⁴ = 2⁴5¹⁶m⁸.
- Janson's form with unordered-pair Δ: E[X_iX_{i+1}] = 0, which is forced because q_i and q_{i+1} are at distance 1. There are
  at most 3m pairs with 2 ≤ |i−j| ≤ 4, each with E ≤ p²(1−p)¹⁸ because |z(D_i) ∪ z(D_j)| ≥ 18. Each index has at most 8
  neighbours, so δ ≤ 8p(1−p)¹⁸. The dependency graph is valid by Lemma 2.7, since |i−j| ≥ 5 implies distance ≥ 5.
- The resulting rate is −0.0155711263·m. The crossover function is concave and decreasing past m ≈ 514, so "every m ≥" is
  legitimate.
- The proof is purely probabilistic, as the README says.
- Source PDFs match `sources_sha256.txt`.

**6. The remark (≤ 4920).** The degree-3, 3-variable polynomials are written out in G6. Theorem 2.5's hypotheses (M ≥ N ≥ 2)
hold, and Lemma 3.2 is unchanged. The remark is valid once the θ = π sentence is added, and the true threshold is 4917 (N3).

**7. Literature.**
- EGMRSS Theorem 1′ = E² → (ℓ₂, ℓ₄). Confirmed.
- Tsaturian Theorem 1.1 = E² → (ℓ₂, ℓ₅). Confirmed, and his final step is W2 with d = 5.
- CMXZ v1 dated 15 Jun 2026, v2 dated 31 Aug 2026, both stating 6330. Confirmed.
- The CF number is wrong (G3), and the EGMRSS-figure and Tsaturian-θ₃ claims are wrong (G1, G2).

Scratch work (my checkers, regenerated instances): `/tmp/ref188/`. No bundle file was edited.
