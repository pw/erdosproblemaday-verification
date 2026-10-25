# Seat B — blind read of the #174 entry page against the files (2026-10-21, ~21:45–22:10Z)

Read: `entry/entry_rendered.txt` and `entry/entry174.js` (21:40Z versions; tokens filled from `entry/vals.json`), against
`src/`, `refs/palv_v1.txt`, `live/`, `lean-build/`, `bridge/`, `compute/`, and the seat reports. My own scripts are in
`seats/B_work/` (`sqrect_cert.py`, `lemmaA1_census.py`, `sqrect_reduced.py`, a copy of O's `checkA2.py`), each run under
`ulimit -v 4000000; timeout 600`. Model receipt (`receipts.sh`, run by me): every seat and the main session served
`claude-opus-5-5`. The two "still running" leanchecker sentences are not flagged, as instructed.

**Bottom line.** The replay, the bridges, the census numbers and the attributions for the paper, Pálvölgyi and the
algebraic-coordinates corollary check out. But the page's headline new finding is false: the square-plus-rectangle (and
every one of the five failing eight-point orbits) **does** have a first-order derivation certificate, of exactly the kind
in Pálvölgyi's own Lemma A.1. Our `derivation_cert.py` tested a stronger condition (mixed moment = 0) than the method
needs (mixed moment symmetric). Separately, the one-transcendental decision procedure has prior public work the page does
not credit, the second instrument is a check at two rational values of τ rather than a second exact decision, and the
label for the seat-read proofs is (b) where the site's convention and the facts give (c).

---

## MUST-FIX

### M1. "No derivation certificate can see it" is false (title, summary, eight-point bullet, labels, headline)

Sentences:
- Title: *"and an eight-point square-plus-rectangle that fails the test while no derivation certificate can see it"*
- Summary: *"…fails the test, although the derivation method behind Pálvölgyi's and OpenAI's examples cannot detect it."*
- Bullet: *"For this set the moment identities that Pálvölgyi's and Prop 7.7's derivation certificates need have only the zero
  solution, so no first-order derivation certificate exists. … The classification's colouring, a ℚ-linear functional,
  sees an obstruction that the derivation method cannot."*
- Labels: *"…the square-plus-rectangle example and its missing derivation certificate are (d) computations…"*
- Also `apply174.py` HEADLINES tag: *"AN EIGHT-POINT SQUARE-PLUS-RECTANGLE THAT THE DERIVATION METHOD CANNOT SEE"*.

What the files say. Pálvölgyi's Appendix, Lemma A.1 (`refs/palv_v1.txt` l. 204–222) — the general first-order
derivation certificate — requires Σλ = 0, Σλp = 0, Σλppᵀ = 0, ΣλD(p) = 0, and that **M = ΣλD(p)pᵀ be symmetric**, not
zero; then Σλ‖D(p′)‖² = E for every copy, because the cross term is 2·tr(D(A)ᵀA·M) with D(A)ᵀA skew. (The appendix is
labelled unchecked by its author; I re-derived this four-line proof: AᵀA = I gives D(A)ᵀA + AᵀD(A) = 0, and the trace of
skew × symmetric is 0. Every other term dies by the listed moments.) His Theorem 1 and
OpenAI's (31) happen to use M = 0, but that is a special case. `compute/derivation_cert.py` imposes the full
Σλ(Dp)pᵀ = 0 (all nine augmented entries), i.e. the special case, and from its "only λ = 0" the page concludes that no
first-order certificate exists.

What I computed (`B_work/sqrect_cert.py`, D = d/dτ on ℚ(τ)):
- With M only required symmetric, the square + rectangle has a 1-dimensional solution space:
  λ = −2u² on (±1,0), −2v² on (0,±1), 1 on each rectangle point (u = (1−τ²)/(1+τ²), v = 2τ/(1+τ²)).
  Energy E = Σλ‖D(p)‖² = 16/(1+τ²)² ≠ 0; M = diag(κ, −κ) with κ = 16τ(τ²−1)/(τ²+1)³ (symmetric, nonzero — which is
  exactly why `derivation_cert.py` missed it). With M = 0 imposed, the script reproduces `derivation_cert.log` (only λ = 0).
- Positive control: on an explicit congruent copy in ℝ³ whose entries are rational functions of τ and a second parameter
  (so D acts on the copy as well), Σλ‖D(p′)‖² − E simplifies to **0**.
- By hand it is two lines: on the rectangle D(p) = b·Jp with b ∝ xy (b = 2D(τ)/(1+τ²)·sign(xy)), on the square D(p) = 0;
  so the derivative conditions reduce to Σλx²y = Σλxy² = 0 (odd), and the quadric conditions fix λ as above.
- `B_work/lemmaA1_census.py`: **all five** failing eight-point orbits have such a certificate (1-dim solution space,
  energy a nonzero rational function of τ, e.g. −2λ₇/τ² for (0,2,4,6,8,9,10,11)); the passing controls
  (0,…,7), (0,1,2,3,8,…,11), (0,2,5,7,8,…,11) and a 7-subset have none (dimension 0). So, for the twelve points, the test
  and first-order derivation certificates agree on every orbit I tried.
- The classification-level functional Φ(a⊗b) = (∂a)(∂b) of (32) also works with a symmetric (not zero) mixed moment and
  needs only the trace of Σβ(∂p)(∂p)ᵀ, so even "the classification's colouring" for this set can be a derivation one.
- Prior public claim, in our own bundle (`seats/W_src/wstrinz/spherical-ramsey_FRONTIER.md` l. 47–49, 129–131): "at
  quadric corank one the two coincide … The two counts first separate on S² at (κ, k) = (3, 4); **on the circle they never
  do**." The page's claim contradicts it; my computation agrees with wstrinz.

Consequence: the eight-point non-Ramseyness is **elementary** (Lemma A.1 + EGMRSS Lemma 15 / Rado), independent of
Theorem 1.1. Corrected text, e.g.:
- Title: "…and an eight-point square-plus-rectangle inside OpenAI's twelve points that is already not Ramsey" (or drop).
- Bullet: "Each half is transitive, but the union is not Ramsey. Our computation says it fails the test (its reduced
  kernel has an antisymmetric spatial block, so never I). It also has an elementary first-order certificate in the sense
  of Pálvölgyi's Lemma A.1: weights −2u² on (±1,0), −2v² on (0,±1) and 1 on the rectangle, with symmetric but nonzero mixed
  moment and energy 16D(τ)²/(1+τ²)² ≠ 0. The zero-mixed-moment certificates of Pálvölgyi's Theorem 1 and Prop 7.7 do not
  exist for it. All five failing eight-point orbits have Lemma A.1 certificates."
- Labels: the eight-point non-Ramseyness becomes (a)+(d) (an explicit certificate, verified exactly); the eight-point
  *minimum* stays (b) modulo Theorem 1.1, since it uses the sufficiency half for the 7-point subsets.
- "Where to look for the hole" should now say that this error was found and where (`derivation_cert.py` tested the
  special case M = 0).

### M2. The one-transcendental decision procedure is not first: credit the prior public procedure

Sentences: *"Deciding the test with one transcendental (ours; computation, label (d))."*; summary *"We also built an exact
procedure that decides the test when the coordinates involve one transcendental number."*; *"Ours: … and the decision
procedure with what it found."*

The bundle's own copy of wstrinz/spherical-ramsey (14 Oct 2026; v1.1.1 on Zenodo) lists, in its README results table:
*"An exact decision procedure for one-parameter cyclic sets; it reproduces the known exact verdicts | [CERT] per instance
(`exact_circle_cert.py`)"*, and FRONTIER F7: *"The one-parameter circle case is implemented with 5/5 exact controls"*, with
the local form *"exact algebra over ℚ(T)[U] localized at U = T"* and *"the criterion is a lifting problem over the local
ring of F ⊗ F at the diagonal"* (SR-C33(a)). That is the same localisation at the diagonal that our DVR procedure uses. It is
AI-generated and unreviewed, like ours, but it is earlier and public, and it is in `seats/W_src/wstrinz/`.

Corrected: "(an independent implementation; wstrinz/spherical-ramsey released an exact decision procedure for
one-parameter cyclic sets on 14 Oct, `exact_circle_cert.py`, built on the same localisation at the diagonal; ours is written
for any dimension with one transcendental, though every set we ran is on a circle)". Fix the same in the summary and in
"What this entry is". (Whether our script was written before anyone here read theirs, the files do not say; the page should
not imply priority either way.)

### M3. The second instrument is a check at two rational values of τ, not a second exact decision

Sentences: *"A second, separately written instrument uses exact rational arithmetic and no computer algebra: it takes the
limit of the kernel as y → x through its Plücker coordinates…"* and *"The two instruments agree on every one of the 304
orbits at six, seven and eight points."*

`plucker_check.py` and `crosscheck8.py` fix x = x0 ∈ {2/7, −5/3} (and `minor_check8.py` x0 ∈ {2/7, −5/3, 11/13}) and take
the limit h → 0 at that x0; the docstring itself says "Exact for generic x0". Specialising first and then taking the
limit agrees with the generic reduction for all but finitely many x0, so two agreeing values are strong evidence, not a
proof over ℚ(τ). Both instruments also share the reduction theorem (m_F(K) = reduction of the saturated kernel), the
parametrisation and the labels (`minor_check.point` vs `census.X`, which I checked agree). So:
- "for any transcendental" rests on instrument 1 alone (sympy, symbolic over ℚ(x, y), τ an indeterminate) plus
  ℚ(τ) ≅ ℚ(x). That inference is correct; I re-ran instrument 1 on the square + rectangle and got the reduced spatial
  block [[0, −x(x−1)(x+1)], [x(x−1)(x+1), 0]] symbolically (`B_work/sqrect_reduced.py`), nonzero for transcendental x.
  (The bundle logs the antisymmetric block only at three x0, in `minor_check8.log`; log the symbolic one too.)
- Corrected: "A second, separately written instrument (exact rationals, no computer algebra) evaluates at fixed rational
  τ = 2/7 and −5/3 and takes the limit y → x there through Plücker coordinates. It is a spot check of the generic
  computation at two specialisations, not a second proof; both rest on the same reduction to the DVR."
- The 12-point rank claim is different and fine: rank 9 at one rational point does prove rank 9 over ℚ(x, y).

### M4. Label (b) for the AI-read proofs, and "by hand"

Sentences: *"…with the paper's own proofs of Lemmas 3.1 and 4.2 read by hand as (b)."*; *"Seats O and T read those proofs
by hand."*

The readers were AI seats (O; the main seat), not humans; the page's own summary says "None of this has been reviewed by a
human expert". (b) means "rigorous modulo a named theorem"; sibling entries label seat-read proofs **(c) plausible,
unverified by a human** (e.g. the entry at `src/index.js` offset ~952k: "The paper as written: (c) plausible/unverified by
a human — four tool-equipped machine seats…"). Corrected: "…with the paper's own proofs of Prop 2.1's descent and Lemmas
3.1, 4.2 and 5.2 — which the kernel does not check — (c): read line by line by AI seats O and T and the main seat, no gap
found, not human-reviewed." And "Seats O and T read those proofs line by line (machine seats)".

### M5. The page is marked CLOSED but never says that "characterise" is a judgment

The rendered page shows **CLOSED OCT 21, 2026**. `apply174.py`'s CLOSED_BY_LITERATURE comment says *"whether that is the
characterisation Erdős wanted is a judgment, said so on the page"* — the page does not say it anywhere (grep for
judg/characteris/decid: only the problem statement and the ALS quote). L flagged it (L3: nothing formal says the criterion is
decidable or effective; whether an existential criterion "characterises" is a judgment). Add, e.g. to "The claim":
"Theorem 1.1 is an existential algebraic criterion. Whether it is the characterisation Erdős asked for is a judgment; we
mark the problem closed on that reading. The paper proves no effective procedure (Remark 2.2 shows only that the kernel is
finitely generated)."

### M6. The bundle the page sends readers to is private

*"…written up with both instruments in the bundle"* and the link *"Our bundle — …"* point to
github.com/pw/ErdosProblemADay.com, which is **PRIVATE** (`gh repo view` → visibility PRIVATE; `mkpage.py` says so too).
Every reader gets a 404, and the "where to look for the hole" sentence depends on it. Sibling entries add "(repository
private at the time of writing — files available on request)". Add that, or publish the bundle.

---

## SHOULD-FIX

S1. *"T wrote out the ultrafilter realisation for a two-point set (30 realisations) and an equilateral triangle (27)…"*
T's (A)/(B) replace Lemma 5.5's output by arbitrary strings in the common columns ("simulating Lemma 5.5's output"), and the
triangle paths are synthetic; T says "Not checked computationally: the ultrafilter choices themselves". Corrected: "T
simulated the string realisation of §5.3 for a two-point set (30 line realisations, from a genuine equal-endpoint pair) and
for an equilateral triangle (27, synthetic paths), with arbitrary common strings in place of the non-constructive
ultrafilter choices; distances came out exactly A's." Also "checked Lemma 6.3's averaging with Fox derivatives" → "(the first
derived step, which is all s = 3 needs)".

S2. *"…with K = 2 or 3 the same search does find them."* False for K = 3. I re-ran O's `checkA2.py` unchanged
(`B_work/O_checkA2_copy.py`): K = 2 → 436 monochromatic (100,046 proof-relevant coincidences); **K = 3 → 0 monochromatic**,
354 proof-relevant coincidences; K = 4…7 → 0; wrong weights → 48,018. Corrected: "with K = 2 the same search finds 436
monochromatic copies, and with K = 3 it finds the near-misses the proof's bound rules out (354)". Also "searched 769,470
copies": these are 769,470 copy *parameters* (x, y) = (|t|², t·u), each standing for every copy with those squared norms.

S3. *"Seat W read the primary text of nearly every citation, and all were accurate: … Hindman–Strauss (second edition)…"*
vs T's note *"the citation for the product rule (20) points to the wrong Hindman–Strauss results"*. The page says both. The
paper cites the 1998 first edition; W and T checked the 2012 second edition; T's point is that the cited Thm 2.5, Cor 2.6,
Thm 1.42 are the semigroup facts, while the convention (20) is Thm 4.12(b) (2nd ed.), uncited. Reconcile: "accurate, with
H–S numbering checked only against the 2nd edition; the convention (20) itself is H–S Thm 4.12(b), which is not cited (T)".
"Wrong" is too strong for T's note.

S4. A third bridge now exists and the page does not mention it. `bridge/Bridge174Main.lean` (21:42Z, after the page),
`AxBridgeMain.log`, two `BridgeMainMut*` mutants, `verbatim_check.py` (now reads it; the page's "checked by a script" run is
the 21:43 one), `make_bundle.sh` (copies it) and the FC issue draft ("three bridges", `erdos_174_criterion`) all have it. The
page says "the two bridges". Either describe it (FC's `erdos_174` with an explicit `criterionAnswer`, axioms, mutants, and
that the FC leanchecker run covers only `Bridge174FC`) or keep it out of the bundle and the issue.

S5. The seven-point paragraph ignores the most relevant prior (AI) claims, which are in the bundle: wstrinz B(a) "any at
most six distinct points on a circle are Ramsey" ([LEAN], unconditional), "7 is the minimum size of a non-Ramsey cyclic
set", the rank criterion SR-C24 for one-parameter cyclic sets with 5 ≤ n ≤ 8, the radian 8-gon (Ramsey for every θ), and
the conjectured one-parameter threshold "Ramsey iff fewer than 9 points in general position". Cite them next to JD-Jones;
the square + rectangle (8 one-parameter points, not Ramsey) is a non-general-position case worth saying so. Also: *"…is no
counterexample to it"* — "it" has no clear antecedent (JD-Jones' claim is about six points); and "is not of the form ℚ(τ)"
needs its reason (the field is the function field of a genus-1 curve, a (ℤ/2)³ cover of the r-line branched at 1/2, 3/2, 2,
∞, so it is not purely transcendental). Pálvölgyi's Theorem A.3 (generic seven points not Ramsey) belongs here as context.

S6. *"We have not seen this eight-point example stated elsewhere."* Nobody searched for it: W's report (21:26Z) predates the
k = 8 census and does not look for it; the bundle holds only wstrinz's README/FRONTIER, not the note or ledger that treat
one-parameter 7- and 8-point circle sets. State the coverage: "not in the paper, Pálvölgyi's appendix, or the
READMEs/FRONTIER of the four repositories; we did not read wstrinz's note or ledger."

S7. Twelve-point rank observation: wstrinz FRONTIER F5 already reports nonzero 9 × 9 evaluation determinants over ℚ(T, U)
for 176 one-parameter non-two-group nine-point cyclic samples (SR-C6). Our "220 of 220 nine-point subsets full rank" is an
instance of a pattern stated there; say so.

S8. *"We derived it, seat L derived it independently…"* L's §4 heading quotes the exact statement as a question ("'Every
spherical configuration with algebraic coordinates is Ramsey'?"), which suggests it was put to L; the per-seat prompts are
not in the bundle, so independence cannot be checked. Safer: "seat L, asked whether the Lean contains it, gave the same proof
(étale idempotent)".

S9. Mutant hygiene. Every bridge mutant renames the namespace (`Bridge174M1`, `Erdos174MA`, …) but keeps the original
`end …`, so each has an incidental "Invalid name after `end`" error and would exit 1 even if the mutation changed nothing. I
read the logs: each also has genuine errors at the mutated site, so all six controls stand. Fix the harness (match the
`end`, or assert the error line).

S10. Bundle leftovers: `entry/README.md` (copied to the bundle root by `make_bundle.sh`) still contains the tokens
`LEANCHECKER_README` and `RANDOM_README`. `MODEL_RECEIPTS.txt` does not exist yet (receipts.sh has to be run into it; my run:
all six transcripts `claude-opus-5-5`).

S11. Pálvölgyi paragraph: *"…moments Σλ, Σλp, Σλppᵀ and Σλ·D(p)pᵀ vanish…"* omits ΣλD(p) = 0 (needed for the translation
term with his unaugmented p), and *"F(q) = R·Σ D(qi)²"* never defines R (= (2r−1)(2r−3)(2r−4)); a reader will take R for ℝ.
Either define R or write F(q) = Σ D(q_i)² (the constant only normalises the sum to −24).

---

## NIT

N1. *"peak 6.7 GiB"* is the largest single-module RSS (7,020,712 kB = 6.70 GiB, `modules.tsv`) with four modules running
in parallel; say "peak per-module RSS 6.7 GiB".
N2. *"two parts that share no imports"* — both import Mathlib; "neither imports the other" (verified by grep, both ways).
N3. *"EuclideanRamsey (47 modules) proves the classification and the consequences"* — except Prop 7.7 (SphericalRamsey) and
Cor 7.5's citation half.
N4. *"Applying mF to the first condition gives an ordinary sphere through the points"* — a quadric; with the second
condition (spatial block I) it is a sphere.
N5. *"at an arbitrarily small scale q"* — q multiplies squared distances.
N6. *"Sufficiency (§§3–6) is the new part."* Necessity for this criterion is new too (EGMRSS's strategy, a new invariant);
"the harder part".
N7. *"merged this morning"* → "merged on 21 October (10:05Z)"; a /day page is permanent.
N8. *"A fifth, blind seat checked this page… All four returned HOLDS AS READ"* — "All four" right after the fifth seat reads
oddly; move the fifth-seat sentence after the verdict.
N9. The page uses "(d)", "(b)", "(c)" without defining them (siblings say "Labels, as on every entry here: (a) elementary
proof · (b) rigorous modulo a named theorem · (c) plausible, unverified · (d) computer-assisted"), and "label (d)" appears in
a heading before any definition.
N10. *"we kernel-checked it … (Bridge174.lean …)"* — the Lean statement assumes full affine span (and s ≥ 2, d ≥ 1); say
"for configurations with full affine span" (wstrinz's Theorem A has no span hypothesis).
N11. *"Theorem 1.1 and its consequences are (d)"* — Cor 7.5's non-subtransitivity half is (b) modulo LRW 2011 Cor 2.
N12. Labels mention only Lemmas 3.1 and 4.2, while the Lean paragraph lists four sub-lemmas proved differently (Prop 2.1's
descent and Lemma 5.2 too).
N13. *"Bloom calls these claims, not endorsements"* (site banner template) — nothing in this bundle supports it; check the
template's source.
N14. `apply174.py` HEADLINE says "READ BY AI SEATS (THREE HOSTILE + ONE LEAN)"; all four seats had the same hostile brief
(`BRIEF.md`) and the page says four were briefed to refute.
N15. *"The paper notes the test is a finite computation…"* — Remark 2.2 says the kernel is finitely generated and its image
is the span of finitely many blocks; "finite computation" is our paraphrase.

---

## Checked and correct

- Replay: 65 modules = 47 + 18 (`all_order.txt`); 9,589 lines (summed from the source at 1581d4c; L's 8,620 + 982 includes
  the 13-line `Result.lean`, outside the closure); Mathlib d13f23b7, Lean v4.34.1; 65/65, 0 errors, 21:05:07 → 21:11:14 =
  6 min 7 s; Σ per-module wall 608 s; `statement_match.txt` 11+13+4+5+8+4+4 = 49 blocks, ALL_MATCH_STD_SORRYSEEN; seven
  solution theorems on [propext, Classical.choice, Quot.sound], sorryAx on every comparator; `MUTATIONS.txt` seven mutants
  + unmodified, all as wanted; `neg.log` planted sorry → sorryAx.
- SphericalRamsey: D(t) = (1+t²)/2, energy Σ D(y_j)², weights (if square = 2 then −2 else 1), weighted sum 8, colour
  ⌊3e⌋ mod 50, for every n (`Main.lean`, `Coloring.lean`, `EnergyIdentity.lean`); no import from EuclideanRamsey.
- FC: 174.lean as described (graham and LRW `research open`; spherical `research solved` with `sorry`), PR #7469 on 20 Oct;
  PR #6980 merged 21 Oct; verbatim check MATCH, mutated run MISMATCH rc 1; bridges on the three standard axioms; the
  ℝ⁰ step is `dim_pos_of_congruent`; mutants fail with genuine errors.
- Bridge174: P = (1−e)(h⊗1) with e generating the Kähler ideal; standard axioms; three mutants fail genuinely. The four
  repositories, dates and the shared theorem name are as W reports.
- Paper: Theorem 1.1, Cor 7.1–7.5, Props 7.3, 7.6, 7.7 as summarised; the necessity paragraph (functional, (5)–(7), 2s+1
  intervals, (2s+1)^s colours) and the sufficiency outline (Lemma 3.1, 4.1–4.3, §§5–6, t·(1/t) = 1) match the text.
- Pálvölgyi: date, v1, ChatGPT disclosure, the seven points and circle, D(r) = 1, integer weights, forum post 23 Sep 09:20.
- Live: page last edited 16 Oct 2025, no status shown, OpenAI not mentioned; teorth `open` (2025-08-31).
- Compute: criterion.py's math is right (B_p = ℚ[x,y]_(x−y) is a DVR, residue field ℚ(x); a basis whose reductions are
  independent spans V ∩ B_p^N; replacement step uses a unit coefficient; constant row/column free). Controls as listed.
  Orbit counts 128/104/72 (and 304) recomputed by Burnside-free enumeration; 67 + 5 at k = 8; the failing orbit
  (0,2,4,6,8,9,10,11) is exactly square ∪ {(±u,±v)}; group of order 8 is a symmetry group of X. Rank 9 at one rational point
  proves rank 9 over ℚ(x, y), so the 12-point and 220 nine-point claims stand. nine_det 64 / nonzero / 0. Random 40/40
  and 40/40. O's 1/21 and 769,470; T's 30 and 27. "For any transcendental" follows from instrument 1 (symbolic) and the
  invariance of the criterion under ℚ(τ) ≅ ℚ(x) and under enlarging F (Prop 2.1's descent), as M3 says.
