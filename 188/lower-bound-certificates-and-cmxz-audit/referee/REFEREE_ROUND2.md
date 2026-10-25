# Erdős #188, round-2 blind consistency read (report only, no files edited)

Read: `verification/188/lower-bound-certificates-and-cmxz-audit/README.md`, `entry_body.html`, `entry_summary.txt`, `entry_title.txt`, every log in the bundle (`cores/*.describe.json`, `logs/*`, `controls/controls.log`), plus the live job state (ps at 2026-10-14T01:18Z, `~/MathDyad/erdos188/runs/`) and the source PDFs (Tsaturian 1703.10723v2, CMXZ 2606.17194v2, Conlon–Fox 1705.02166v4, EGMRSS 1975 II).

Recomputed and found to agree: 15/69/111 point counts. Pairs and runs 11/4, 63/16, 95/29. Radii √7, 5.2074, 6.0200. Minimality 16/16, 126/126, 81/81. Negative controls 1/11, 29/95, 19/63. CNF headers match pairs + runs + units: 5,791 / 746,909 / 302,135 clauses. DRAT 252/2,459/4,654 bytes. All solver times in the tables. Every core generator has d² = 3, so θ₃ is never used. The 7 rotated points of the 15-point core are ρ(the 7 nonzero lattice points), and its structure is exactly the one the prose describes. `config188.py` regenerates `egmrss_k4` and `ts3_c6_k5` byte-identically. Crossovers: 6330 with the rounded exponent, 6329 unrounded, 4917 (g(4916) = +0.0054, g(4917) = −0.0089), 4840 with 69.28m lines. The values 3.16·10⁹ and 2.15·10⁹ are right; Conlon–Fox state "log denotes log base 2" and diam ≤ R−1 gives R = m. CMXZ quotes check out: 10¹⁰, Thm 1.2, Thm 2.5 = (50DM/N)^N, −0.01557. EGMRSS's own Fig. 2 argument and Tsaturian's Lemma 2.2 erratum match the README. W2 logic is sound: a red P forces both ρP and ρ⁻¹P blue, so either composition convention works.

## Findings

### FIX-FIRST

1. **Non-existence asserted for unresolved instances.** README §1c: "The precise statement is: no certificate exists among the configurations listed, and the instances that could decide the matched question are open at these time limits." Entry: "So: no certificate of *k* ≥ 7 among these configurations".
   → Only one ℓ₆ instance resolved (SAT). The other four are unresolved, so a certificate may well exist among them. The "precise statement" contradicts its own second clause.
   → Fix: "no certificate was **found** among the configurations listed: one is SAT, the rest are unresolved at these limits". In the entry: "no certificate of k ≥ 7 found among these configurations".

2. **The relaunched and "informative" instances are misidentified.** Entry: "The informative instances — centre radius 4 with (5,0) blue, where ℓ₅ is UNSAT in 0.3 s, and centre radius 6 with (6,0) blue — had not returned at 1200 s and were relaunched with three-hour caps".
   → (a) The c6/(6,0) ℓ₅ twin is SAT 0.70 s (`controls5.log`), so it is not informative by the README's own criterion.
   → (b) c6/(6,0) never ran at 1200 s; there is no c6 row in `probe6.log`. It is `ladder3.sh`'s run with `timeout 3600`, at 2,535 s elapsed at 01:18Z.
   → (c) The two jobs actually running with `timeout 10800` are `l6_c3_b6` and `l6_c4_b5` (ps). The c3/(6,0) ℓ₅ twin is also SAT (0.37 s).
   → README has the same problem: "the informative instances — where ℓ₅ is UNSAT in a third of a second — … (two were relaunched with 3-hour caps …)". Only one ℓ₆ run (c4/(5,0)) has an UNSAT ℓ₅ twin. The ℓ₆ twin of the 69-point instance (`l6_c6_b5`) is queued in `ladder3.sh` behind c6/(6,0) and is mentioned nowhere.
   → Fix: name the 10800 s pair (c3/(6,0), c4/(5,0)) in the table rows. Call only c4/(5,0) informative. Add a row "6 | (5,0) | UNSAT 0.4 s (the 69-point instance) | queued (3600 s cap)". In the entry, replace "and centre radius 6 with (6,0) blue" with the true set.

3. **An informative ℓ₆ result is missing, the bundle log is stale, and "uncapped" is false.** README: "Earlier, uncapped runs (`logs/ladder1.log`: rotations about centres within radius 1 and 2, R = 10, no W2) are SAT for both k = 5 and k = 6".
   → `ladder1.sh` runs with `timeout 1800`.
   → The live `runs/ladder1.log` (01:10) now ends with "runs/c3_k6 … Command exited with non-zero status 124 1800.05s". That is the ℓ₆ twin of `c3_k5`, which is UNSAT in 7.9 s with no W2 unit. The bundle copy (00:37) lacks this line and its DONE.
   → Fix: say "capped at 1800 s". Refresh `logs/ladder1.log`. Add the pair (centres ≤ 3, d ∈ {√3, 3, 5}, R = 10, no W2: ℓ₅ UNSAT 7.9 s / ℓ₆ unresolved at 1800 s) to §1c and to the entry's ℓ₆ paragraph.

4. **The "orders of magnitude" figure is too small.** README: "two to three orders of magnitude harder for cadical"; README §1c header area and entry: "The ℓ₆ instances are two to three orders of magnitude harder for the solver"; summary: "two to three orders of magnitude harder and still running".
   → The data say 981.35 s vs 0.39 s = 2,516× (10^3.4) for the one that resolved. For the informative one it is 1200 s vs 0.28 s = >4,286× (>10^3.6), still running.
   → Fix: "more than three orders of magnitude (≥ 2,500×)" in all three places.

5. **The ℓ₆ patch statistics are wrong, and no shipped log supports them.** README: "the k = 6 colourings found there have red density 0.24 on the lattice, longest blue run 5 in each direction, 150 red T₃'s and no period ≤ 12". Entry: "red density 0.24 … 150 red √3-triangles and no period up to 12".
   → Recounted from `runs/c1_k6.sol` / `runs/c2_k6.sol` on the base lattice copy:
     - density 0.219 (c1) and 0.239 (c2), so "0.24" is c2 only;
     - longest blue run 5 in every direction, both ✓;
     - no period 1–12 along the three unit directions, both ✓;
     - distinct red side-√3 triangles: **31 (c1) and 50 (c2)**. 150 = 3 × 50, i.e. each triangle counted once per vertex.
   → `analyze_sol.py` computes neither the T₃ count nor the longest run, and its output is not in the bundle.
   → Fix: "one of them (centres ≤ 2) has red density 0.24, 50 red T₃'s, …", and ship the analysis script and its output.

6. **The bundle's CMXZ log contradicts both artefacts.** `logs/cmxz_audit.log` ends "=> the same proof gives E^2 not-> (l_2, l_4920) with their line count (100m), ~4850 with the exact 69.3m." The README says "**E² ↛ (ℓ₂, ℓ₄₉₁₇)** … ≈ 4840 with the exact line count 69.3m" (the entry and title say 4917). The README also attributes to this log a rounded-exponent crossover ("with the exponent rounded to 0.01557 … exactly from m = 6330") that the log never prints.
   → The README numbers are right (recomputed above). The log is the 10-step-grid draft.
   → Fix: in `cmxz_audit.py`, scan in unit steps and print g(4916)/g(4917), the 69.3m variant and the rounded-exponent 6329/6330 lines. Regenerate the log.

7. **A bound below 4917 is implied without a label.** README: "≈ 4840 with the exact line count 69.3m; further free gain from optimising p against the full exponent rather than against p(1−p)¹⁸".
   → This reads as a bound below 4917 obtainable from the same proof, but no claim label is attached (rule b). The entry is clean on this.
   → Fix: append "(estimate only, not claimed)" or delete the clause.

8. **The Lemma 2.6 attribution is wrong, and the W2 unit in the noT3 control goes unmentioned.** Entry: "the no-red-*T*₃ branch of Tsaturian's proof is UNSAT on the bare lattice at radius 8, as his Lemma 2.6 says". README: "the no-red-T₃ branch of Tsaturian's proof is UNSAT on the bare lattice already at R = 8". The `noT3.py` docstring says the same.
   → Lemma 2.6 (Tsaturian p. 7) says that with no red T₃ the colouring of L **exists and is unique** (Fig. 9). The UNSAT comes from the extra units in `noT3.py` (origin red **and (5,0) blue**) plus his final step: Fig. 9 has no two points of different colour at distance 5.
   → As written, a reader checking Lemma 2.6 sees a contradiction.
   → Fix: "with the origin red and (5,0) blue, the no-red-T₃ branch is UNSAT on the bare lattice at R = 8 — Lemma 2.6's unique colouring (Fig. 9) has no two points of different colour at distance 5, which is his final step."

### Smaller (fix in the same pass)

9. **Summary.** "15 and 69 points … with a red origin and one WLOG blue point".
   → The 15-point core has only the origin unit (`units [[183]]`, and no blue line in `verify_egmrss_k4.log`).
   → Fix: "a red origin (and, for ℓ₅, one WLOG blue point)".

10. **Entry W2.** "And for any *d*, the rotation about the origin by the angle with 2*d*·sin(θ/2) = 1 …"
    → The README and the verify log both say d > 1/2.
    → Fix: "for any d > 1/2".

11. **Entry W1.** "A valid colouring has a red point (else any ℓ*k* is blue), so *the origin is red*."
    → The translation step is dropped; the README has it.
    → Fix: "so, after a translation, the origin is red".

12. **Entry, Milnor–Thom.** "(Milnor–Thom on 100*m*² wall lines in the four coordinates of two points)"
    → The README and log say ≤ 100m wall lines; M = 100m² is lines × points (sign conditions).
    → Fix: "100m wall lines (100m² sign conditions)".

13. **README, unit clauses.** "the unit clauses are the origin (positive) and one lattice point ≠ 0 (negative)"
    → The second unit exists for the ℓ₅ cores only.
    → Fix: add "(the ℓ₄ core has only the origin)".

14. **README, field of coordinates.** "all real coordinates of rotated points lie in ℚ(√3, √11)."
    → This is false for the θ₃ images present in both full ℓ₅ instances (sin θ₃ = √35/18).
    → Fix: "of θ_{√3}-rotated points, hence of every core point".

15. **Entry controls.** "the bare lattice is SAT for every *k*"
    → The README has k ≥ 3, and k = 2 fails.
    → Fix: "every k ≥ 3".

16. **Unit-circle points.** README: "the eight unit-circle points of the two lattice copies"; entry: "the eight unit-circle points of both copies".
    → Each copy has six unit-circle points; the core uses four from each.
    → Fix: "the eight unit-circle points in the core (four per copy)".

17. **Dangling references.**
    - (a) Both artefacts cite the referee seat's "Fraction-arithmetic checker on the basis {1, √3, √11, √33}". Neither its code nor its output is in the bundle. Ship both, or drop the sentence.
    - (b) The 10800 s relaunch has no script or log in the bundle.
    - (c) The entry's only artefact link (`github.com/pw/ErdosProblemADay.com/tree/main/verification/188/…`) returns **404 publicly**: the repo's `visibility` is `private`, and `verification/188/` is still untracked in worktree `seat-0014`.
      - The entry's stated value is "third-party-checkable certificates", so this matters here, even though it is site-wide (51 such links).
      - At minimum, commit and push before shipping. Better, make the bundle reachable: the cores are 2/35/81 KB.
    - (d) `$P noT3.py` in "Reproduce" writes `runs/noT3_R*.cnf` and needs cwd = the bundle. It fails from a fresh bundle, which has no `runs/`. `controls5.sh`, `probe6.sh` and `ladder*.sh` all `cd ~/MathDyad/erdos188`.

18. **README §3.** "Nothing here changes the headline: 6 ≤ k₁₈₈ ≤ 6330 in print, ≤ 4917 by the remark above."
    → This clashes with a title that headlines 4917.
    → Fix: "Nothing here changes the published bounds; the remark (label b) gives ≤ 4917."

19. **Entry, universal claim.** "nobody has moved the lower bound since Tsaturian's *k* ≥ 6 in 2017"
    → This is a universal claim, and its only sources are the page/forum snapshots.
    → Fix: "the page and forum record nothing beyond Tsaturian's k ≥ 6 (2017)".

20. **README, θ₅.** "the θ₅ generator internalises W2"
    → No core was extracted from `c3_k5` to show the θ₅ copies are used.
    → Fix: "presumably internalises".

21. **README, (6,0) explanation.** "(6,0) blue stays SAT at centre radius 6 — the 5-periodic lattice patterns of Tsaturian's Lemmas 2.5/2.6 allow it."
    → Tsaturian only says Figs. 7/9 have no two points of different colour at distance 5. "5-periodic" and "allow it" are unverified explanation.
    → Fix: "consistent with Tsaturian's Figs. 7/9 (unchecked)", or cut.

22. **README, DRAT scope.** "with its UNSAT proof checked by a third party"
    → drat-trim checked the full-instance proofs; the 69-point core was re-solved by minisat22, with no DRAT.
    → Fix: "with a drat-trim-checked UNSAT proof of the instance that contains it".

23. **Optional.** Entry: "E² → (ℓ₂, ℓ*k*) holds iff some finite point set has no colouring …"
    → The "only if" direction is compactness (de Bruijn–Erdős), not elementary, and it is never used.
    → Fix: say "if", or cite compactness.

**(f) future-update phrasing.** The update promises are acceptably phrased: "this row is updated when it lands", "the rows are updated when they land", "this paragraph is updated when they land". No TODO or placeholder text was found. Timing note: `l6_c6_b6` hits its 3600 s cap at about 01:35Z, then `ladder3.sh` starts `l6_c6_b5`.

## Verdict: FIX-FIRST

The theorem side is clean: certificates, WLOG logic, CMXZ audit arithmetic, and the literature numbers all agree.

The ℓ₆ section is not. It asserts a non-existence it did not establish (#1). It names the wrong relaunched/informative instances (#2). It omits an informative timeout (#3). It understates the hardness gap (#4). It carries a 3×-inflated T₃ count (#5).

The bundle's own CMXZ log contradicts the 4917/4840 in the text (#6). The Lemma 2.6 attribution misreads the source (#8). 1–8 must be fixed before shipping; 9–23 can go in the same edit.
