# Blind read: /day/505 entry draft (entry_rendered.js + headline_rendered.js), 2026-10-20 ~18:50Z

Reader: hostile copy-editor and fact-checker (Claude Opus 5.5). Every factual sentence was checked against the files named in BLIND_BRIEF.md. Nothing was edited. One check was re-run: cake_lpr on the two mutated certificates, because no log of it exists. It ran under ulimit -v 8000000 with --CML_HEAP_SIZE=3000 --CML_STACK_SIZE=2000.

**Counts:** 6 WRONG · 13 OVERCLAIM · 8 UNSUPPORTED (one of them PENDING) · 13 UNCLEAR. Everything else is SUPPORTED (ledger at the end).

**Deploy blockers, in my judgement:** items 1, 2, 7, 8 and 20. Item 23 (leanchecker) has to be resolved whenever it lands.

---

## WRONG

**1. The decide count is a line count.**
- Page: "There are 13,197 kernel `decide`s; 13,170 of them are in the finite-case directory."
- Fact: 13,197 is the number of *lines* that contain `decide` (`grep -rw decide | wc -l`). The source has **19,594 `by decide` calls**, 19,574 of them in `FiniteCases/` (13,170 lines). The other 13 matches use `decide` as a function, as in `decide (y … < 0)`, and are not tactic calls. Seat F's report says it correctly: "13,170 `decide` lines". The error also appears in ESTIMATE.md and the bundle README.
- Fix: "There are 19,594 kernel-evaluated `by decide` calls (on 13,197 lines); 19,574 of them are in the finite-case directory."

**2. Not all of §6 is replaced.**
- Page: "*All of §6* is replaced by a machine-generated refutation: 4,093 case lemmas over 66,297 lines on 330 Boolean unknowns."
- Fact: seat F's map lists Lemma 6.1 as "**Same route**": `facet_six_properties`, `facet_complement_exclusion`, `Projectors/Within.lean`. The machine refutation replaces only **Lemmas 6.2–6.4 and Theorem 6.5**. The `complementary` and `pair_count` fields of `TenSystem` are *proved* from Lemma 6.1's geometry; they are not refuted cases.
- Fix: "Lemmas 6.2–6.4 and Theorem 6.5 are replaced by …"

**3. The 41.3852° bound is rounded the wrong way.**
- Page: "Every line through the origin is within 41.3852° of one of the eleven, and that is the exact covering radius."
- Fact: the exact radius is arccos√(1/(2M)) = **41.385231°** (`cover/verify_runs_seatW.log`: "rho <= 41.385231 deg"). Lines at the deep hole are 41.38523° from every centre, so they are *not* within 41.3852°.
- Fix: "within 41.38524°", or "the exact covering radius is 41.38523…°".

**4. The interval endpoint is rounded the wrong way.**
- Page: "The true minimum therefore lies in [45°, 45.3320°]."
- Fact: the three exact certificates give 45.332011°, 45.332012° and 45.332013° (`verify_runs_seatW.log`). The certified upper end is above 45.3320°.
- Fix: "[45°, 45.33202°]". The sentence "The best ten lines known reach 45.3320°" is fine as a rounded value.

**5. Kalai's post title is misquoted.**
- Page link label: "Kalai, Test Your Intuition 60: the finite and infinite Borsuk's conjecture (11 Oct 2026)". The body says "(Test Your Intuition 60)".
- Fact: `w_dl/kalai_blog_1011.html` has the title "**Test Your Human Intuition 60: The Finite and Infinite Borsuk's Problem**". The URL slug on the page is correct.
- Fix: use the real title.

**6. The label for b(X) ≤ 11 contradicts the page's own scheme.**
- Page (Labels): "*b*(*X*) ≤ 11: **(a) elementary**, given an exact rational vertex enumeration."
- Fact: the bound rests on 330 × 8 = 2,640 exact 4×4 rational solves by `verify_cover.py`. The same page labels the SAT core "(d) computer-assisted" for the same kind of reason.
- Fix: "**(d) computer-assisted** (exact rational vertex enumeration; the reduction from it is elementary)."

---

## OVERCLAIM

**7. Kalai did not propose this set; he proposed the family.**
- Summary: "Kalai proposed this same set as a candidate counterexample in 2015, for dimensions above about 70."
- Body: "had already proposed this very set as a Borsuk counterexample, conditional on the double-cap conjecture and 'for *d* > 70 or so'".
- Whose: "The candidate set is Kalai's (2015)".
- Fact: Kalai's C₃ (`w_dl/kalai1505.txt` §2.3–2.4; 2011 blog "Construction 3") is the projector set of ℝⁿ *in general*. He proposed it for n large enough that d > 70, i.e. n ≥ 12. The ℝ⁴ member lives in dimension 9, so "this same set … for dimensions above about 70" contradicts itself. Seat W: "Nowhere does he ask about n = 4." Separately, "Kalai's (2015)" conflicts with the body's own 2011 blog date.
- Fix: "Kalai proposed this construction (the projector set of ℝⁿ) as a candidate counterexample, for n large enough that d > 70 (blog 2011, survey 2015 §2.4)." In Whose: "The construction is Kalai's (2011/2015)."

**8. The cap case is not "Walkup's"; it is our derivation from Walkup.**
- Tag: "CAP CASE ALREADY IN WALKUP 1970".
- Heading: "The cap case is 1970 mathematics".
- Whose: "the cap case is Walkup's (1970)".
- Fact: Walkup states (8.1) and Theorem 3 (`w_dl/walkup1970.txt`, l. 60ff and 730ff). He never states the covering-radius corollary. The six-step argument is the world seat's (`seatW_world.md` §(c)), and the page's own body says "Our world seat found that …". Attributing an unstated result to a 1970 author is the misattribution the brief warns about.
- Fix:
  - Tag: "CAP CASE FOLLOWS FROM WALKUP 1970".
  - Heading: "The cap case follows from 1970 mathematics".
  - Whose: "the cap case follows from Walkup's (1970) Prop. 8.1 + Thm 3 (derivation: our world seat)".

**9. Our certificate is not "that certificate" for acprk's cells.**
- Page: "The notes said the cells still had to be certified, and this is that certificate."
- Fact: acprk's claim (`world/acprk_03-borsuk.md`) is about *their* 11 optimized lines and *Voronoi cells*, valid if no cell contains an orthogonal pair (margin 0.036). We certify a *different* configuration (the world seat's) by a *stronger* criterion (covering radius < 45°, closed caps). Seat W: "the criteria differ."
- Fix: "The notes said the cells still had to be certified. We certify the statement instead, for a different eleven-line configuration and by a stronger criterion (caps of radius < 45°)."

**10. The minimal finite core rests on our hand-written encoding; the checker verifies only the CNF.**
- Page: "an independent SAT proof of the finite step with a verified certificate, which shows the step needs less than the paper uses"
- Labels: "The minimal finite core … **(d) computer-assisted**, by a verified-checker certificate".
- Fact: cake_lpr certifies that `cnf/core_min.cnf` is UNSAT. That this CNF says "pure + pair_count + nonempty" rests on reading `tensystem_cnf.py`. I read it, and the encoding is right as far as I can see. Its controls are three things: the full ten_lean variant UNSAT (the Lean already proves `no_ten_system`), each drop-one SAT result, and a set-logic model checker in the same file. None of these formally links the core to `TenSystem`. The "needs less" claim is exactly the part with no Lean or second-encoding cross-check.
- Fix: say "relative to our CNF encoding (checked by code reading and by drop-one controls)". Better: state the core in Lean as a 3-field structure; `no_ten_system`'s style of proof would decide it.

**11. "Not formalized by anyone" is too strong.**
- Page: "Corollary 7.1 (every *d* ≥ 9) is not formalized by anyone."
- Fact: Formal Conjectures PR #7312 (open) states it, with `sorry` (seat W). We cannot rule out formalizations we did not find.
- Fix: "Corollary 7.1 has no formal proof that we found (OpenAI's Lean stops at d = 9; FC PR #7312 states it with `sorry`)."

**12. "First reported" is a "first" claim we did not establish.**
- Page (Whose): "*b*(*X*) = 11 was first reported numerically by the acprk notes."
- Fact: seat W only says it found nothing before 6 Oct.
- Fix: "was reported numerically by the acprk notes (10 Oct; nothing earlier found)."

**13. "Uses only" overstates the Lean's purity step.**
- Page: "The proof uses only the fact that lower-dimensional smooth images are Lebesgue-null: no Sard on the level map and no Stiefel–Whitney classes."
- Fact: per seat F, the null-image fact is the step's only *Sard-type* input. The proof also uses sign chambers, smooth approximation, compact local homotopy and `traceHomotopy_ray`.
- Fix: "Its only Sard-type input is that lower-dimensional smooth images are Lebesgue-null …"

**14. The replay leaves more of the printed proof unchecked than §§4 and 6.**
- Page: "So a green replay certifies Theorem 1.1, not §§4 and 6 as printed, and those had to be read separately."
- Fact: seat F also lists these as not certified as printed:
  - Lemma 3.1(2)–(3) and the smoothness claims of Lemma 3.2 (§3);
  - Lemma 5.3 (absorbed into FiniteCases);
  - Corollary 7.1.

  A reader will take §§2, 3, 5 and 7 as kernel-certified.
- Fix: "certifies Theorem 1.1, not the printed arguments of Lemma 3.1(2)–(3), the smoothness in Lemma 3.2, Lemma 4.2 and the degree/Stiefel–Whitney steps of §4, Lemma 5.3, Lemmas 6.2–6.4/Theorem 6.5, or Corollary 7.1".

**15. The upstream caveat names only one of the inputs still needed.**
- Page: "('At least two' is still needed in dimension three, inside Lemma 5.2, to produce the designs.)"
- Fact: getting `pair_count` (exactly two triangles of *K* per pair) upstream also needs:
  - Lemma 5.2's complementary-triple exclusion in ℝ³ (the "at most ten" half);
  - Lemma 6.1's "no additional triangles" step in ℝ⁴ (three witness lines).

  Dropping the *field* `complementary` from the finite problem does not make the geometric complementarity unnecessary.
- Fix: "(Upstream, the designs still need Lemma 5.2's 'at least two' and its complementary-triple exclusion in ℝ³, and Lemma 6.1's 'no additional triangles' step.)"

**16. "Borsuk number exactly 11" is credited to us without its condition.**
- Heading: "Eleven pieces suffice: *b*(*X*) = 11, certified here."
- Summary: "an exact certificate that eleven sets do cover *X*, so its Borsuk number is exactly 11".
- Tag: "OURS: … BORSUK NUMBER EXACTLY 11".
- Fact: only b(X) ≤ 11 is certified here. The equality needs OpenAI's Theorem 1.1, which the Labels section says correctly ("(b) rigorous modulo Theorem 1.1").
- Fix: "… so, with OpenAI's theorem, its Borsuk number is exactly 11"; heading "*b*(*X*) ≤ 11 certified here, so *b*(*X*) = 11".

**17. The hemi-icosahedron is credited to the paper.**
- Page: "In ℝ³ this forces the triangles on six labels to be the six-vertex ℝP² (the hemi-icosahedron), with exactly one triangle from each complementary pair (§5)."
- Fact: §5 defines "six-label triangle systems" and never names ℝP²₆ or the hemi-icosahedron. Xie notes it is "unnamed in the paper". The identification comes from our enumeration (`finite/triangle_systems.out`: 12 systems, one orbit, the hemi-icosahedron is one of them).
- Fix: "… forces a 'six-label triangle system' (§5), which by our enumeration is always the six-vertex ℝP² (the hemi-icosahedron) …"

**18. The eleven-set retyping "control" is weak.**
- Page: "Two controls also behaved: … re-typing the theorem as an eleven-set statement fails to elaborate."
- Fact: `TypeCtl.lean` fails because `HasElevenSmallCover` is a different constant (`typectl.log`: "Type mismatch"). It would fail even if the eleven-set statement were true, so it tests only that the type checker compares types.
- Fix: describe it as a sanity check of the probe harness, or drop it. The planted-sorry control is the meaningful one.

**19. The world seat did not read every history source in the primary.**
- Page: "The world seat checked every dimension in the paper's history paragraph against its source, and all are correct."
- Fact: Nilli's 946 was checked through secondary sources (Kalai's survey reference list, Bondarenko p. 2, Grey–Weißbach), not Nilli's paper (seat W table).
- Fix: "against its source or a citing source".

---

## UNSUPPORTED

**20. No record exists of "our own reading" of §§5–6.**
- Page: "Our own line-by-line reading of §§5–6 also found HOLDS AS READ: the block invariance in Lemma 6.4, the count forcing block sizes 3, 2, 2, and the last step through {r, s, z}."
- Summary: "Three AI referee seats and our own reading found only exposition problems in the paper."
- Fact: there is no written report, notes file or log of this reading anywhere: not in `seats/`, the bundle, `~/MathDyad/erdos505`, `~/MathDyad/notes`, or today's autonomous log. Only the bundle README asserts it. Each seat claim on the page has a report behind it; this one has none. Lemma 5.3 is backed (`triangle_systems.out`); Lemmas 6.2–6.4 and Theorem 6.5 are not.
- Fix: bank a short `seats/main_reading_s5-6.md` (step list plus verdict) before deploy, or cut the sentence and its share of the summary claim.

**21. The cake_lpr rejection controls have no log.**
- Page: "cake_lpr rejects the Lean-variant certificate when one hint is removed from its empty-clause step, and when it is checked against a satisfiable variant of the formula with the clause numbering kept."
- Fact: the mutated inputs exist (`runs/ten_lean.MUT_dropemptyhint.lrat`, `cnf/ten_lean.MUT_nonempty_taut.cnf`), but no output was saved. The bundle README says "REJECTS" with no file behind it.
- I re-ran both now:
  - positive: `s VERIFIED UNSAT`;
  - dropped hint: "c Checking failed at line: 1098. Reason: pivot must be non-zero" (the empty-clause line, 0-indexed);
  - neutralised unit: "c Checking failed at line: 1. Reason: clause not empty or singleton after reduction".

  So the claim is TRUE. Bank these outputs.
- ⚠ Instrument note: **cake_lpr exits 0 on rejection**. Any gate on its return code is blind; grep for `s VERIFIED UNSAT` instead.

**22. "Compiled first try" has no evidence.**
- Page: "It compiled first try"
- Fact: `bridge.log` shows only the final successful compile. Nothing records the number of attempts, and the boast adds nothing.
- Fix: cut it.

**23. PENDING: leanchecker has not finished.**
- Page: "`leanchecker --fresh` over the whole closure of `OAI.Geometry.Borsuk.Main` started at 18:38 UTC; this sentence is updated when it lands."
- Fact: `steps.tsv` has no `leanchecker_fresh` row. `logs/leanchecker_fresh.log` is 0 bytes, and the process (pid 3388680) was still running at 18:51Z.
- Until it lands, "kernel-replayed" and "kernel-checked" (title, tag, Labels) mean only this: each of the 269 OAI modules was elaborated and kernel-checked on our box. **Mathlib's .oleans came from `lake exe cache get` and were not re-checked.** That is standard, but say it if the page ships before leanchecker finishes.
- Also: `post.sh` runs a missing-module control after leanchecker. Report its result next to the leanchecker verdict, because an empty or failed leanchecker log is not a pass.

**24. Two details of the release history are not in any file.**
- Page: "(adc7f12, 6 October 2026, 21:58:50 UTC), and every family-156 file is unchanged at today's head, 1581d4c."
- Fact:
  - Our clone is shallow (`git rev-parse --is-shallow-repository` = true; only 1581d4c, dated 2026-10-12). Seat W gives "2026-10-06T21:58Z". The seconds ":50" appear nowhere.
  - Seat W checked only the paper directory and `lean/OAI/Geometry/Borsuk/`. `ComparatorChallenges/BorsukNine.lean`, `docs/156.md` and the comparator JSON are not covered by any check on disk.
- Fix: "21:58 UTC", and "the paper and its Lean directory are unchanged at …". Or fetch history and check all family-156 paths.

**25. The model receipts file is stale.**
- Page: "Every referee seat was served by Claude Opus 5.5 (the counts are in the bundle's `seats/MODEL_RECEIPTS.txt`)."
- Fact: the claim is TRUE. I grepped all three seat transcripts: T 68, F 163, W **386** `"model":"claude-opus-5-5"`, and no other model string. But `MODEL_RECEIPTS.txt` (written 18:26Z) still shows W as "305 … (snapshot; seat still running)", and it counts only opus occurrences, so it cannot show the *absence* of a fallback model.
- Fix: refresh the file with final counts plus "other models: 0" per seat.

**26. The "seven-item list" is not in the bundle.**
- Page: "It checked every step on a seven-item list, including the regularity computation (4.6), …"
- Fact: seat T's report has seven numbered sections, but the list itself (a brief) is not in the bundle. Low.
- Fix: "It checked §§2–4 in seven sections, including …"

**27. Bundle hygiene: seat W's header carries a future timestamp.**
- This is not on the page, but the bundle is linked from it.
- Fact: `seatW_world.md` says "Checked 2026-10-20, ~18:00–19:10 UTC", but the file was last written at **18:35:51Z**, and it is 18:51Z now.
- Fix: correct the header before it ships in the bundle.

---

## UNCLEAR (prose a mathematician would misread)

**28. Headline quantifier.** "Eleven lines within 41.39° of every line (exact rational certificate) give the matching cover." As written, the eleven lines are each near every line.
- Fix: "Every line is within 41.39° of one of eleven fixed lines (exact rational certificate), which gives the matching cover."

**29. Headline ending.** "… forces every tetrahedron's six-label complement to be the six-vertex ℝP², which ten labels cannot fit." Ten labels can carry six-vertex ℝP²s. The contradiction is that no ten-label complex has this structure on *every* facet complement at once.
- Fix: "… and no complex on ten labels can have that on every facet complement."

**30. Tag order.** "… CAP CASE ALREADY IN WALKUP 1970 · NOT OURS · UNREVIEWED BY HUMANS". Placed there, "NOT OURS" reads as being about the cap case, whose derivation *is* ours.
- Fix: "THE THEOREM IS NOT OURS", placed right after "OPENAI'S CLAIM".

**31. The homotopy sentence is backwards.** "… is proved by showing that a homotopy of the odd map would have to miss a ray, which it cannot."
- Fix: "… by showing that a smaller facet would let the odd map be homotoped to one that misses a ray, which no map homotopic to it can do."

**32. "Dimension four" clashes with "dimension nine".** "In dimension four the finite step needs neither …". Everywhere else the page says "dimension nine".
- Fix: "For lines in ℝ⁴ (ten labels) the finite step needs neither …"

**33. "All three printed VERIFIED" is ambiguous.** It reads as the three tools, and CaDiCaL prints `s UNSATISFIABLE`, not VERIFIED.
- Fix: "drat-trim and cake_lpr both printed VERIFIED for the Lean variant, the paper variant and the minimal core."

**34. The environment parenthetical is misplaced.** "We compiled it in OpenAI's environment, not FC's (Lean 4.33.1, Mathlib 0df444a3)." The versions are FC's (`world/fc/lean-toolchain`, `lake-manifest.json`), but the sentence order invites reading them as OpenAI's (which are 4.34.1 / d13f23b7).
- Fix: "We compiled it in OpenAI's environment (Lean 4.34.1, Mathlib d13f23b7), not in FC's own (Lean 4.33.1, Mathlib 0df444a3). FC's definitions are textually identical but elaborate against OpenAI's Mathlib."

**35. "Each" implies every process peaked.** "a peak of 6.7 GiB each". `modules.tsv` max RSS is 7,031,564 KiB = 6.71 GiB, the maximum over modules.
- Fix: "a peak of 6.7 GiB per process".

**36. The perturbation must preserve symmetry.** "Take the convex hull of their twenty unit vectors, perturbed slightly so that it is simplicial." The perturbation must stay centrally symmetric.
- Fix: "perturb the ten lines slightly so that the hull of their twenty unit vectors is simplicial".

**37. The D₄ control was a rounding of D₄.** "The same verifier rejects the twelve lines of the D₄ root system (covering radius exactly 45°)". The verifier checked a rational rounding of D₄ (`verify_runs.log`: M = 1.000001494, not 1).
- Fix: "rejects a rational rounding of the twelve D₄ lines (exact radius 45°; rounded M = 1.0000015)". The minus-one-root control (M = 2.0000006) is clean.

**38. The Wikipedia motive is our inference.** "… mentions the nine-dimensional claim in a new 'Variations' section, because it concerns an infinite set."
- Fix: "… in a new 'Variations' section, noting that the construction is infinite and so does not settle the finite version."

**39. "Exactly the dropped field" needs a qualifier.** "separate code re-checked each model, and each violates exactly the dropped field."
- Fact: `finite/check_models.out` shows the CaDiCaL drop-`pair_count` model violating `['parity', 'pair_count']`. Parity is not a Lean field, so the statement holds only among the Lean's fields. The "separate code" is `check()` in the same `tensystem_cnf.py`, independent only in reusing no clauses.
- Fix: "a separate set-logic checker (no clause reuse) re-checked each model; among the Lean's fields each violates only the dropped one."

**40. The ℝ⁹ form is not comparator-matched.** The paragraph "It also proves the ℝ⁹ form, `…euclidean_nine_counterexample`, through the isometry (2.2)" should add that this theorem is **not** in the comparator's `theorem_names` (seat F §1d), so only `main_theorem` is statement-matched. The bridge, which copies FC's statement verbatim, is what pins the ℝ⁹ form, and it is worth saying so.

---

## SUPPORTED (ledger; evidence file in brackets)

**Summary**
- Borsuk's 1933 question and the Erdős #505 statement [`live/ep505.html`].
- Kahn–Kalai 1993 for n > 2014 [same].
- 64, Jenrich–Brouwer 2014, still on the problem page [same].
- 63, Grinsztajn 2026, finite set [seatW §3].
- 6 Oct release [`w_dl/blog10.txt`, seatW].
- X ⊂ trace-one symmetric matrices, no ten sets of diameter < √2 [`paper.txt` Thm 1.1].
- 269 modules, standard axioms, statement matched [`modules.tsv`, `statement_match.txt`].
- Proof differs in degree theory and the finite step [seatF §2].
- Kahn–Kalai answered the problem in 1993 [`ep505.html`].

**The problem**
- Quote and refs [Er46b], [Er61], [Er75f, p. 102], [Er81b, p. 28].
- n ≤ 3, with Eggleston for n = 3.
- "last edited 30 December 2025"; gives 64; "Proof claims (0)"; "The ability to post new comments has been suspended" [`live/*.html`].

**The claim**
- 18 pp., dated 23 Sep 2026; family 156; Theorem 1.1 text; Remark 2.2 isometry; Corollary 7.1 for d ≥ 9 [`paper.txt` pp. 1–4, 17].
- "does not determine the smallest dimension … or the exact value of b(X)" [p. 2].
- Initial commit adc7f12 on 6 Oct [seatW; seconds unsupported, see item 24].
- Head 1581d4c [`repo/.git`].

**The argument**
- (2.1) orthogonal ⇔ distance √2 [Lemma 2.1].
- Thickening plus partition of unity [Lemma 2.4].
- Averaging, positive minus negative, odd map S⁹ → S⁹ [§3, (3.3), (3.6)].
- ≥ k(k+1)/2 labels and degree 1 at equality [Prop 4.1].
- Facets have k vertices; ridges lie in a positive even number of facets [Thm 4.3].
- One triangle per complementary pair [Lemma 5.2]; the hemi-icosahedron part is item 17.
- Ten-label block argument [§6].
- Walkup "cannot be applied directly" [p. 2].

**The Lean and the replay**
- `main_theorem` and the comparator file [`repo/lean/ComparatorChallenges/BorsukNine.lean`].
- ℝ⁹ form via `coordinates9` = (2.2) [`Main.lean` l. 117, seatF §1d].
- 269 modules, 78,964 lines, Lean 4.34.1, Mathlib d13f23b7, imports only Mathlib plus itself [`find`/`wc`/`grep` on the repo, `lean-toolchain`, `lake-manifest.json`].
- Source audit: zero hits for each listed keyword [`grep -rw`, re-run].
- 269/269 built, 0 errors, 18:07:59 → 18:36:48 = 28 min 49 s, W = 4 [`driver.log`, `modules.tsv`].
- Five-declaration axiom set exactly {propext, Classical.choice, Quot.sound} [`logs/ax.log`].
- Theorem plus six definitions MATCH under pp.all [`logs/statement_match.log`].
- Three matcher mutations each flagged [`mut/MUTATION_RESULTS.txt`].
- Planted sorry → sorryAx [`logs/neg.log`].
- Eleven-set retype fails [`logs/typectl.log`; but see item 18].
- leanchecker started 18:38 UTC [`post.log` 18:38:11Z].

**Two routes**
- Combinatorial Tucker / Smith-theory degree; purity via a homotopy that misses a ray; `no_free_ridge` (≥ 2) in place of the F₂ cycle, which is all §§5–6 use [seatF §2–3].
- 4,093 case lemmas (named `c####`), 66,297 lines, ≤ 330 variables [`grep`/`wc` on FiniteCases; seatF].
- Seat T: HOLDS AS READ; (4.6), (4.8) and the facet-coefficient count checked; icosahedral positive control [`seatT_topology.md`].
- Lemma 5.3: 12 systems, one orbit, |Aut| = 60, no transposition [`triangle_systems.out`].
- Reversed Hatcher citations and compact steps as the only findings [seatT EXPOSITION 1–6; seatW: all EXPOSITION].

**Eleven pieces**
- acprk "b(X) = 11 numerically", needs certification, 10 Oct [`world/acprk_03-borsuk.md`, seatW].
- Eleven lines from the world seat's search, rounded to exact rational unit vectors [`verify_cover.py`, `seatW_best_K11_s11_vp.*`].
- 330 four-subsets × 8 signs [code].
- M = 0.888221984… < 1, exact fraction in the bundle [`verify_runs_seatW.log`, `.cert.json`].
- ⟨u,cᵢ⟩² ≥ 1/(2M) and exactness at the argmax vertex [code logic, checked].
- Closed sets Aᵢ cover X; 2 − 2(1/M − 1)² = 1.968326 < 2 [log].
- 41.7107° and 41.9385° [`verify_runs.log`].
- Hull deep hole equal to 10 printed digits; 10⁷ samples never below the bound [`verify_runs_seatW.log`].
- D₄ and D₄-minus-one rejected [`verify_runs.log`; see item 37].

**Cap case**
- The argument itself is correct as written. I checked Walkup's (8.1) and Theorem 3 verbatim in `w_dl/walkup1970.txt`.
- Four world-seat runs converge to 45.3320, three exact-certified [`w_scripts/vpolish_K10_*.log`, `verify_runs_seatW.log`].
- A set of diameter < √2 need not lie in a 45° cap (the near-orthonormal-frame example).
- The paper cites only Kalai §2.3 [`paper.txt` p. 2].

**Finite step**
- 330 variables; Lean variant and paper variant UNSAT [`runs/*`].
- CaDiCaL 0.04–0.05 s, Kissat about 1.1 s [`*.time`].
- Drop pure / pair_count / nonempty gives SAT (exit 10).
- Dropping no_boundary, complementary and down together stays UNSAT (`core_min`).
- drat-trim VERIFIED and cake_lpr `s VERIFIED UNSAT` for ten_lean, ten_paper and core_min [`runs/*.dratrim.out`, `*.cakelpr.out`].
- The encoding matches the Lean's `TenSystem` fields as I read them [`tensystem_cnf.py` vs `TenLabels/Labels.lean`].

**Bridge**
- FC `not_nine` is research solved, links OpenAI `Main.lean#L117`, which is `euclidean_nine_counterexample` [`world/FC_BorsukConjecture.lean`].
- Statement differences: inside X with `diam` < √2, versus arbitrary pieces with `ediam` < `ediam s`.
- FC definitions verbatim [diff against `world/fc` HEAD 14c30813, which matches `FC_BorsukConjecture.lean`].
- Three theorems proved, `erdos_505 : type_of% borsuk_conjecture.not_forall`, standard axioms [`bridge.log`, `FC_505.lean`].
- `<` → `≤` mutant fails at `hsmall i` [`bridge_mut.log`].
- Fin 10 vs Fin 11 control fails [`bridge_wrongshape.log`].
- FC environment is 4.33.1 / 0df444a3 [`world/fc`].

**World**
- Page unchanged; Bloom's 8 Oct post lists 25 problems, no 505, no "Borsuk" [`w_dl/blog10.txt`].
- FC PR #6898 on 11 Oct (build only, no axioms check, no Comparator); PR #7312 open.
- Wikipedia still says 63, with a Variations section [`w_dl/wiki_borsuk_raw.txt`].
- Tao's 28a page says 63; PR #217 says "I did not independently check the Lean".
- Kalai's posts of 7 and 11 Oct; earlier records all finite sets; Grinsztajn verifier re-run clean [seatW, `w_grin`].
- Xie: "combination leaning new", no compilation [`w_dl/xie2610.txt` l. 476, 965].
- No dispute and no public replay found; 903 / Magdeburg 97-25 [seatW].

**Whose and links**
- "internal OpenAI model" [`w_dl/oai_readme.md`].
- Every seat on Opus 5.5 (transcripts; see item 25).
- DOIs 10.37236/4069 → EJC v21i4p29 and 10.1007/BF02392331 → Acta Math (both resolved).
- Kalai arXiv 1505.04952, §2.3–2.4.
- The TYI URL slug is correct.
