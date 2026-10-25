# Blind read 2 — #508 entry after corrections (rendered 22:19Z; re-rendered from src 14 Oct for HTML/home-card checks)

Checked against: rendered_508.txt, a fresh render of /day/508 and / from `src/index.js` (the shipped rendered_home_card.txt is a 2,800-char slice that cuts the card off mid-title), title/summary/headline_card/claim line/lean label/entry508.js/extra_links.js, apply_blind_read.py (to tell new sentences from old), and the sources named in the brief. Kernel status unchanged: `leanchecker --fresh` (pid 2679499) still running, no `leanchecker_fresh` row in steps.tsv, so the page's "running as this is written" sentence is still true.

## Part 1 — the 48 items

| # | Status | New wording (quoted) / note |
|---|---|---|
| 1 | FIXED | Title: "…and χ equals the weak-measurable chromatic number of the plane". Body: "the first answers, in its weak form, a question open since Falconer". |
| 2 | FIXED | Falconer → `10.1016/0097-3165(81)90014-5`. Crossref: "The realization of distances in measurable subsets covering Rn", JCTA 31(2):184–189, Falconer, 1981. |
| 3 | FIXED (title nit, N7) | "Soifer, Chromatic number of the plane & its relatives (Mathematics Competitions 16(1), 2003) — the Nelson/Isbell history the paper cites at pp. 15–19" → wfnmc PDF. Right document, but the label truncates the article's title (see N7). |
| 4 | FIXED | "(1581d4c of 12 October; the build was launched at fd4aeeb, the 8 October merge, and every closure file is byte-identical between the two — the sources seat finds these files have exactly one commit, adc7f124 of 6 October)". Checked: fd4aeeb = 2026-10-07T22:20−07:00 (8 Oct 05:20Z); 1581d4c = 12 Oct 14:55−07:00; `git diff fd4aeeb 1581d4c` is empty on all three closure dirs and the challenge file; driver.log launched at fd4aeeb. bundle README l.11/30 agrees. |
| 5 | FIXED (minor, N10) | "(Proposition 4.2's first paragraph — a Følner sequence and a weakly convergent subsequence, a textbook construction; the axiom of choice enters elsewhere, through the invariant mean on F/ℤ of §2.2 and the compactness arguments)". Matches paper l.1486–1490 ("finite-set Følner sequence … a weakly convergent subsequence") and l.366–368 (the invariant mean on F/ℤ, Bekka G.2.1). "the compactness arguments" is vague (N10). |
| 6 | FIXED (nuance, N9) | "one comment (BorisAlexeev, October 2025, asking whether Erdős's 1975 "F(2) ≤ 6" was a slip for 7)". Author and date (27 Oct 2025) are right; for the framing see N9. |
| 7 | FIXED | "with the tightest margin at vertex B, P′ − P ≈ 7·10⁻⁴ (certified ≥ 6.96·10⁻⁴)". moser_cert.log: P′ − P = 0.000698320 − 0.000001690 = 6.966·10⁻⁴. |
| 8 | FIXED | "seven corruptions rejected". |
| 9 | FIXED | "found the most material of the citations the paper is missing (the others being Székely 1984 and Shelah–Soifer on whether χ and χ_m can differ)". Matches sources §1 "Omitted references" and S7. |
| 10 | FIXED | World: "Five third parties record machine checks: plasma-ai's claim card …; Sergi Galán's repository …; cert-machine's comparator run …; AI-hard's Comparator run at fd4aeeb (10–11 October, pass); and Li–Su …, who rebuild the transfer half". Summary: "Five other parties record machine checks of the Lean". Labels: "…accepted by cert-machine on two kernels, with four other parties recording machine checks". Every element checks against its source (§3 below). |
| 11 | FIXED | "that had been out of date for a week". plasma-ai card created 2026-10-07T07:46Z; brief dated 14 Oct. |
| 12 | FIXED (wording, N13) | "What no one has published in eight days is a referee reading of the human-readable argument; the one public engagement with Payne's obstruction is Galán's field notes, which list the same uses of square roots our seats found and re-run the Lean over smaller fields." Galán's notes never name Payne (N13). |
| 13 | PARTLY | Galán is now credited: "a consequence Sergi Galán had already drawn publicly on 9–10 October ("This is OpenAI's transfer, run with several distances": for every set D of algebraic distances, χ(ℝ², D) ≥ 1/m_D(ℝ²))". But that sentence says Galán drew the Soifer/Kahle consequence, which he did not, and the date is off (N1). |
| 14 | FIXED | Title: "the page's lower bound compiled from scratch". Summary: "the page's lower-bound statement closes from it in three forms". Tag: "THE PAGE'S LOWER BOUND COMPILED AS A PROBE". Line, lean label and body: "lower-bound statement". No "page's (own) question" is left anywhere. |
| 15 | FIXED | Card title: "…and no human has publicly refereed the 62 pages". |
| 16 | FIXED | `kind: "bound"`. |
| 17 | NOT FIXED | Labels still read "(d) computer-assisted : OpenAI's own Lean, kernel-replayed here …" with no qualifier. build.sh's gate requires `leanchecker_fresh 0` for (d) and that row has not landed. The sibling #90 entry wrote "leanchecker pending" until its row landed. The card title's "kernel-checked on our box" has the same gap. Fix: "(d) for the 70 OpenAI modules; Mathlib from cache, leanchecker --fresh pending", or hold (d) until the row is 0. |
| 18 | FIXED | "That is where square roots in F do their work — they make the ring generated by K all of E; density of the directions is not it (the rational directions are dense too), nor is divisibility of K on its own". |
| 19 | PARTLY | Added: "— #print axioms is transitive, so the first line already covers everything the theorem rests on". This is correct, and axioms.log does hold four `#print axioms` lines under `lean --trust=0`. Still present: "Under --trust=0 the kernel printed exactly …" (body) and "under --trust=0 the kernel printed only propext, Classical.choice and Quot.sound for the theorem and, transitively, everything it rests on" (summary). `#print axioms` is a frontend command, not the kernel, and `--trust=0` does not re-check imported (cached Mathlib) .oleans. Fix: "`#print axioms` (run under `lean --trust=0`) reports only …". |
| 20 | FIXED | "c x ≠ c(x + e^{it}) for (volume ⊗ Haar)-almost every (x, t) on ℂ × AddCircle(2π)". Matches Coloring.lean (`∀ᵐ p ∂volume.prod angularMeasure, c p.1 ≠ c (p.1+direction p.2)`, with angularMeasure = haarAddCircle on AddCircle(2π)). |
| 21 | FIXED (attribution, N5) | "the only Fact instances are 0 < 2π and 2 ≠ ⊤ in ℝ≥0∞, both true". A grep of all 70 modules finds Coloring:15 (0 < 2π), Compactness:135 and :250 and Factors:570 (all `(2 : ENNReal) ≠ ⊤`), and nothing else. The sentence is now credited to the whole seat, which wrote the opposite (N5). |
| 22 | FIXED | "…finite case splits on Fin 5 and Fin 6 data, plus a few numeral side conditions". |
| 23 | FIXED | "@[extern]". |
| 24 | FIXED | "BorelTransfer.lean, 451 lines, and the chain behind it: the label model and the invariant law in PlaneSpectrum/Representations, …, residual_fourier in PlaneSpectrum/Ergodicity, …". Checked: `LabelModel`, and `measure k ω` = StationaryMean.measure at Representations.lean:52/116; `residual_fourier` at Ergodicity.lean:403; BorelTransfer.lean is 451 lines. |
| 25 | FIXED (provenance, N12) | "("totally unbelievable alien math?", 260,000 views, and in the follow-up post "ridiculous human-developed machinery — amenable groups, Pontryagin duality, Furstenberg–Zimmer towers")". The 1/2 post matches the captured JSON (views 260,063). For the 2/2 post see N12. |
| 26 | FIXED | "…that the prior lit used to my knowledge". Verbatim (Bluesky, 2026-10-06T23:03Z). |
| 27 | FIXED | "with his caveat that he has "not yet looked at in any serious way" any of the proofs". Verbatim. |
| 28 | PARTLY | "proves by a different lattice method that χ(ℝ⁴) = χ_m(ℝ⁴) and, for d ≥ 5 and finite distance sets with rational squares, χ(ℚ^d) = χ(ℝ^d) = χ_m(ℝ^d) — the full measurable coincidence in high dimension, stronger than Theorem 1.3's weak-measurable one — …; so Theorem 1.3 is new in the plane, with Davies's as the concurrent high-dimensional statement." The "χ_m(ℚ^d)" error and the "concurrent" mis-framing are gone. The qualifier is now attached to the wrong clause (N3). |
| 29 | FIXED | "clear of Bukh's conjecture on algebraically independent distances". |
| 30 | FIXED | "Croft's upper bound 4.359". |
| 31 | FIXED | "(1,581 vertices, later cut to 553 by Heule and 509 by Parts, per the paper's introduction)". |
| 32 | PARTLY | Summary fixed: "transfers any colouring at all to a weak measurable one, for every number of colours (through a new rigidity theorem …)" and "excludes five weak-measurable labels". Left over: the headline card `line` says "Theorem 1.4 kills five measurable labels", and the claim line and banner say "a measurable obstruction to five labels (Theorem 1.4)" (N11). |
| 33 | FIXED | Summary, seats paragraph and Labels: "between them covered all 62 pages …, each scoped seat line by line through its stretch". |
| 34 | FIXED | Link: "two-colourable, measurably at least five". Claim: "it cites Payne's example of the graph on ℝ² whose edges join points whose displacement is a unit vector with rational coordinates". |
| 35 | FIXED | Separate links for "/day/90-…" and "/day/604-openai-weak-pinned-distances-refereed" (the smoke test returns 200 for #604). |
| 36 | FIXED | "No Lean rebuild performed here … ; kernel correctness assumed". |
| 37 | FIXED | "gets a jointly measurable version correct at every point x rather than almost every x". Matches the transfer seat T4 ("its version is correct at every x (`exists_measurable_field`)"). |
| 38 | FIXED | "five because six equal steps around a rotation orbit cannot close modulo five (Proposition 8.2), four by the parity of the six-position angular words of Lemma 8.3 together with the arc geometry of Lemma 8.4 (Proposition 8.5)". Matches paper l.3162–3169 ("six equal steps do not close modulo five") and l.3259–3273 (parity h(t) of X positions plus the Lemma 8.4 arcs). The paper's own intro (l.180) also calls the five-cycle words "six-position angular words", so the old wording was defensible too. |
| 39 | FIXED | "remainder/d² at 0.70–0.72", "an improper colouring overlaps 2.9–4.2%", "bounded, ≈ 1.15". Matches the palettes report (0.7027–0.7197; 4.19%/2.85%; 1.1536). |
| 40 | FIXED | "(our own check now carries that literal reading as a logged control: it puts exactly those three vertices, 0, uB and uT, outside the region)". moser_cert.log 22:15: "CONTROL literal rotate·g+shift reading: vertices outside the region = ['0', 'uB', 'uT']". (That control is not in the script's final `ctrl1 and ctrl2` conjunction. This is cosmetic: the log line prints its own pass/fail.) |
| 41 | FIXED, but introduced a typo (N4) | "we found no mention of it in Tao's or Aaronson's posts on the release" starts a sentence in lowercase. |
| 42 | PARTLY | The "written before that release" boilerplate is gone (0 occurrences in the HTML). The " , " was a render artifact of the tag-stripper (the HTML has "openai/math</a>, OpenAI's own Lean…"). The comma splice is still there: "…the exact value, 6 or 7, stays open — family 158 at github.com/openai/math, OpenAI's own Lean proves Theorem 1.1 — …". Fix: a full stop or semicolon before "OpenAI's own Lean". |
| 43 | FIXED (exactness, N14) | "What the kernel certifies is Theorem 1.1, Theorem 1.4 for Borel colourings (no_measurable_weak_five_coloring; the step from Lebesgue to Borel, modifying on a null set, is a one-liner not formalised) and the forward half of Theorem 1.3". This is right in substance; for the exact statement see N14. |
| 44 | FIXED | "the rational-field counterexamples to Theorem 2.3's analogue are hand arguments about infinite objects, supported by finite checks". |
| 45 | FIXED | "a closed square of side ten has no relatively open cover of mesh at most two and multiplicity at most two". Matches paper l.2882–2884. The new Lean clause is also right: `compact_open_cover_impossible` takes any compact `Q ⊇ ball 0 5`, relatively open `U i : Set Q`, no point in three, ‖x−y‖ ≤ 2. Its proof is partition of unity → `hit_center`, a complex-log lift around a circle (a winding argument), where the paper uses Brouwer (l.2899–2902). |
| 46 | FIXED | "The proof has two parts, and the first answers, in its weak form, a question open since Falconer." Davies's abstract calls the question Székely's 1984 conjecture; "open since Falconer" is fair. |
| 47 | FIXED | "checked 24 of the 33 references … (Falconer, Hadwiger and Woodall through secondary sources behind publisher walls, Zimmer's two by abstract, three by metadata only, Furstenberg 1977 closed access and not load-bearing)". 24+3+2+3+1 = 33, matching sources §0 item 1. Hadwiger was behind a CAPTCHA rather than a publisher paywall, which is close enough. |
| 48 | NOT FIXED | Title still 70 words (76 in `<title>`/og:title) and still telegraphic ("with its Lean kernel-replayed here"). |

Tally: 41 FIXED (eight of them with a nit or a new defect: 3, 5, 6, 12, 21, 25, 41, 43), 5 PARTLY (13, 19, 28, 32, 42), 2 NOT FIXED (17, 48).

## Part 2 — new findings (introduced or exposed by the corrections)

**N1 — Seats ¶, whole-seat flag. UNSUPPORTED (attribution) + date. Medium.**
Quote: "it would settle Soifer's 2ⁿ-distance problem and Kahle's n!-distance problem, which Davies–McCarty–Pilipczuk listed as open in 2023 — a consequence Sergi Galán had already drawn publicly on 9–10 October ("This is OpenAI's transfer, run with several distances": for every set D of algebraic distances, χ(ℝ², D) ≥ 1/m_D(ℝ²))".
What is wrong:
- (a) "a consequence … drawn" grammatically attaches to settling Soifer's and Kahle's problems. Galán never mentions either problem: grep of decalion89_chromatic-number-of-the-plane_README.md, decalion_notes_six_over_fields.md and decalion_openai-five_README.md finds no "Kahle", and "Soifer" only as the 2024 book. What he states is the distance-set transfer. The Soifer/Kahle answers follow from it by FKW, but that step is the whole seat's, not his.
- (b) The README dates the distance-set work "(papers/forbidden-distances/, 10 October 2026)". 9 October is his Lean rebuild.
- (c) The quote is cut mid-sentence with no ellipsis. The source reads "This is OpenAI's transfer, run with several distances and for fractional colourings."

Correction: "— the distance-set transfer itself Sergi Galán had already stated publicly on 10 October ("This is OpenAI's transfer, run with several distances and for fractional colourings": for every set D of algebraic distances, χ(ℝ², D) ≥ 1/m_D(ℝ²)), from which the Soifer and Kahle answers follow by FKW —".

**N2 — Link label (new, extra_links.js). INCONSISTENT/UNSUPPORTED priority claim. Medium.**
Quote: "Li–Su (arXiv:2610.15424, 11 Oct 2026) — the first theorem built on the transfer; rebuilt its Lean half".
What is wrong:
- The page's own world ¶ and N1 sentence put Galán's distance-set transfer on 9–10 October. Galán's README marks it "Proved, using OpenAI's rigidity theorem" and gives it a Lean transfer layer. So by the page's own account it predates Li–Su (11 Oct).
- Galán's README row also lists Li–Su's result: "the least independence ratio of an n-point unit-distance graph tends to m₁(ℝ²) (half of a conjecture of Dúcz and Varga)". The row is undated in a 14 Oct capture, so priority between the two cannot be settled from our files either way.
- The sources seat wrote "the first downstream theorem … already exists", not "the first theorem".

Correction: drop "first": "Li–Su — the first half of the Dúcz–Varga conjecture (#1070) from a single-class transfer; rebuilt its Lean half". Optionally note in the world ¶ that Galán's README lists the same consequence.

**N3 — World ¶, Davies. INCONSISTENT with the source. Low–medium.**
Quote: "χ(ℝ⁴) = χ_m(ℝ⁴) and, for d ≥ 5 and finite distance sets with rational squares, χ(ℚ^d) = χ(ℝ^d) = χ_m(ℝ^d)".
What is wrong: in Davies's Theorem 1.1 (sources §5, verbatim) the hypothesis "D finite and nonempty with d_i² ∈ ℚ" governs both conclusions, ℝ⁴ as well as d ≥ 5. The page writes the unit-distance χ, for which the hypothesis holds automatically. Hanging it on the d ≥ 5 clause alone suggests the high-dimensional unit-distance statement needs it and the ℝ⁴ one does not.
Correction: "proves χ(ℝ⁴) = χ_m(ℝ⁴) and, for d ≥ 5, χ(ℚ^d) = χ(ℝ^d) = χ_m(ℝ^d) (indeed for every finite distance set with rational squares)".

**N4 — World ¶. TYPO (introduced by the item-41 fix).**
Quote: "…the smallest known non-4-colourable graph has 509 vertices). we found no mention of it in Tao's or Aaronson's posts…".
Correction: "We found…".

**N5 — Seats ¶, whole seat. Attribution drift. Low.**
Quote: "The whole-paper seat … confirmed that nothing in the 70 modules weakens the statement (…; the only Fact instances are 0 < 2π and 2 ≠ ⊤ in ℝ≥0∞, both true; …)".
What is wrong: the seat wrote "the only `Fact` is 0 < 2π" (referee_whole.md l.19, l.52). The corrected fact is true (my grep agrees), but it is now credited to a seat that got it wrong.
Correction: "(the Fact instances — 0 < 2π, and 2 ≠ ⊤ in ℝ≥0∞, which the seat missed — are both true)", or move the clause out of the seat's report.

**N6 — World ¶, Galán. STYLE/imprecise. Low.**
Quote: "patches that run the same proof over the constructible, origami and other countable subfields".
What is wrong: the three patches are constructible, origami and **radicals** (`solvableByRad ℚ ℂ`; decalion_lean_external_openai-five_fields_README.md l.8–10).
Correction: "over the constructible, origami and radical fields".

**N7 — Link label, Soifer. STYLE. Low.**
Quote: "Soifer, Chromatic number of the plane & its relatives (Mathematics Competitions 16(1), 2003)".
What is wrong: the paper's [24] and the PDF title read "The 50th Anniversary of One Problem: The Chromatic Number of the Plane & Its Relatives, Part 1", Mathematics Competitions 16(1):9–41.
Correction: use the full title and the pages.

**N8** is folded into N1(c).

**N9 — Problem ¶, BorisAlexeev. STYLE (softened). Low.**
Quote: "asking whether Erdős's 1975 "F(2) ≤ 6" was a slip for 7".
What is wrong: the comment asserts "almost certainly this last equation F(2)≤6 is an error and should have said ≤7. ... But what if it wasn't an error?"
Correction: "noting that Erdős's 1975 "F(2) ≤ 6" is almost certainly a slip for 7".

**N10 — Architecture, choice. Imprecise. Low.**
Quote: "the axiom of choice enters elsewhere, through the invariant mean on F/ℤ of §2.2 and the compactness arguments".
What is wrong: Prop 4.2's own compactness is choice-free: {1,…,k}^E with E countable is compact metrizable in ZF. The choice-using compactness is in the converse, the product {1..k}^{ℝ²}, and in de Bruijn–Erdős for Corollary 1.5 (whole seat l.67, 71, 111; that list also has "the colouring itself").
Correction: "…through the invariant mean on F/ℤ of §2.2 (and, in the converse and Corollary 1.5, through product compactness and de Bruijn–Erdős)".

**N11 — Headline `line` and claim line/banner. Residue of item 32. Low.**
Quotes: "Theorem 1.4 kills five measurable labels" (headline_card.js); "a measurable obstruction to five labels (Theorem 1.4)" (oai_claim_line.txt, rendered in the banner).
What is wrong: Theorem 1.4 excludes *weak* measurable five-colourings. The text understates it and is inconsistent with the summary.
Correction: "kills five weak-measurable labels" / "an obstruction to weak measurable five-colourings (Theorem 1.4)".

**N12 — World ¶, Rybin 2/2. Provenance. Low.**
Quote: "and in the follow-up post "ridiculous human-developed machinery — amenable groups, Pontryagin duality, Furstenberg–Zimmer towers"".
What is wrong: only the 1/2 post is captured (rybin_…json). The 2/2 text comes from a web-search snippet (webfetch_captures #6: "ridiculous human-developed machinery - amenable groups, …"), and the page normalises "-" to "—"/"–". The words match the snippet, so nothing is false. But it is a quote of a fragment we never captured, and the snippet may be cut at the front.
Correction: capture the 2/2 post, or keep its punctuation as captured.

**N13 — World ¶, "the one public engagement with Payne's obstruction is Galán's field notes". Gloss + under-credit. Low–medium.**
What is wrong:
- Galán's notes and README never mention Payne. Payne appears only in the README bibliography (l.606), and the notes have no "rational direction" discussion. So "engagement with Payne's obstruction" is our gloss on what the notes do.
- The notes do engage the rational field directly, and this is the bigger point. decalion_notes_six_over_fields.md l.217–220 (a referee caveat): "A p-adic version of the construction makes the analogue fail over F(i) for every number field F, ℚ(i) included (for ℚ(i) and p = 3: the image of Haar measure on ℤ₃[i] …)". That is the same 3-adic ℚ(i) counterexample our §2–3 seat built, which the page reports as the seat's own construction with no mention that it is already public.

Correction: "the one public engagement with the rational-field question behind Payne's obstruction is Galán's field notes, which list the same uses of square roots our seats found, record the same 3-adic failure of Theorem 2.3 over ℚ(i), and re-run the Lean over smaller fields."

**N14 — Labels, "Theorem 1.4 for Borel colourings": what is exact. Low (precision).**
The kernel-checked statement is `no_measurable_weak_five_coloring : Measurable c → WeakColoring 5 c → False`, where:
- `Measurable` is Borel (ℂ's Borel σ-algebra);
- `WeakColoring 5 c` := `AEMeasurable c volume ∧ ∀ᵐ (x,t) ∂ volume.prod (haarAddCircle on AddCircle 2π), c x ≠ c (x + e^{it})` (Coloring.lean; axioms.log `#print`).

So "Theorem 1.4 for Borel colourings" is the right description. It is not "for measurable colourings satisfying the weak condition" (Lebesgue), since the hypothesis is `Measurable`, i.e. Borel. Exactly: Theorem 1.4 for Borel colourings, with Definition 1.2 in its product-null form. Two hand steps sit outside the kernel:
- that product-null form ≡ Def. 1.2's vanishing integrals (σ-finiteness and completion; whole seat l.41–43: "equivalent, not verbatim");
- Lebesgue → Borel by modifying on a null set (per-t translation invariance plus Tonelli; a one-liner, unformalised, as the page says).

Suggested: "Theorem 1.4 for Borel colourings (in the product-null form of Definition 1.2, equivalent by hand; the Lebesgue-to-Borel step … not formalised)".

**N15 — Home card title. STYLE + item-17 tie-in. Low.**
Quote: "OpenAI's proof, kernel-checked on our box, where de Grey's five stood since 2018 and no human has publicly refereed the 62 pages".
What is wrong: "where" dangles; it reads as modifying "our box". "kernel-checked" carries the same leanchecker caveat as item 17.
Correction: "…: OpenAI's proof, kernel-replayed on our box (leanchecker pending). De Grey's five had stood since 2018; no human has publicly refereed the 62 pages".

**N16 — Summary. STYLE. Low.**
Quote: "covered all 62 pages — each scoped seat line by line through its stretch — and found no gap — only exposition notes, …".
What is wrong: three dashes in one clause chain.
Correction: "…covered all 62 pages, each scoped seat line by line through its stretch, and found no gap: only exposition notes, …".

## Part 3 — the new sentences checked against their sources and found correct

- **plasma-ai:** "kernel-checked Lean proofs were built and axiom-audited here" is verbatim; created 2026-10-07T07:46Z.
- **Galán:** "70 modules … (18 minutes, no errors)", `#print axioms` standard, research log 9 Oct. The notes' "four places" (Lemma 2.7, L = √(AB), t + i√(1−t²), |z| ∈ F) match our pp. 13/19/21/18. Divisibility: Lemma 2.4 and Lemma 3.2.
- **cert-machine:** run 38019899278 shows both kernels "accepts the solution" and strict mode okay. The red control (forge → "Type mismatch") is in run 38050007619. Dated 10 Oct per the sources seat.
- **AI-hard:** fd4aeeb, "2026-10-10 to 2026-10-11", EuclideanFiveColor "pass", nanoda not used.
- **Li–Su:** "Its only non-classical input is the Haar rigidity theorem…", 11 Oct, leanchecker over the BorelTransfer closure.
- **Bloom, Zelinsky:** both verbatim.
- **Falconer DOI** correct. **Lemma 7.5** wording, the **Lean PlanarCover statement**, **winding vs Brouwer**, the **§8 wording** and the **Fact list** are all correct.
- **Axiom transitivity sentence:** correct as Lean semantics (only the "kernel"/`--trust=0` framing remains, item 19).
- **Følner/subsequence** matches the paper.
- **FC PR #6898** merged 2026-10-11T08:10Z. **MO 516012** created 2026-10-13. **Davies** title and date correct.

## Summary (≤200 words)

Of 48 items: 41 fixed, 5 partly, 2 not. Not fixed:
- the "(d) computer-assisted" label, given while leanchecker --fresh still runs (the build gate and #90 convention say qualify or hold);
- the 70-word title.

Partial fixes leave the "kernel printed under --trust=0" framing and some "measurable" (not weak) wording in the card and claim lines.

The corrections brought in two medium errors:
- The seats paragraph says Galán "had already drawn" the Soifer/Kahle consequence. He stated only the distance-set transfer, on 10 October (not 9–10), and the quote is cut without an ellipsis.
- The new Li–Su link calls it "the first theorem built on the transfer". The page's own Galán sentence dates his distance-set theorems earlier, and his README lists the same Dúcz–Varga half.

Smaller new issues:
- Davies's rational-squares qualifier is attached only to the d ≥ 5 clause.
- A sentence starts with lowercase "we".
- The whole seat is credited with a Fact count it got wrong.
- "Other countable subfields" should say "radical".
- The Soifer link title is truncated.
- Galán's notes already publish the same 3-adic ℚ(i) counterexample our seat built.

Every other new sentence checks out.
