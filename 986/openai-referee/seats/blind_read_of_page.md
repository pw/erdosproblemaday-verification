# Blind pre-publication read — /day/986-openai-sharp-log-exponent (family 170)
Reader: hostile blind seat, 2026-10-20. Appended incrementally.

## Checked and holding (no action)
- Module/line counts: 858 modules, 123,565 lines; 450 RamseyFive + 408 SharpRamsey; R5 closure 482 = 450 + 32 shared (recomputed from import lines). Lean 4.34.1, Mathlib d13f23b7.
- Replay: 858/858 rc 0, 0 errors (modules.tsv); wall 12:08:55Z→13:04:17Z = 55 min 22 s; Σ wall_s = 8,644.7 ≈ 8,645 module-seconds; three workers, nice 19.
- leanchecker --fresh: SL 13:05:26→14:03:44 = 3,498 s rc 0; R5 → 15:03:23 = 3,579 s rc 0; missing-module control rc 1 (post.log, steps.tsv).
- Axioms: both mains [propext, Classical.choice, Quot.sound] (axSL.log, axR5.log); statement_match MATCH ×2 incl. 4 defs each; mutation test (nat_lit 6→5 ⇒ SL MISMATCH; sorryAx injected ⇒ R5 NONSTD).
- Probe Extra_S4: `main_of_primeConstruction4` is byte-identical to OpenAI's FromConstruction.lean l.62–74 except the name and `6 ≤ s`→`4 ≤ s` (diff); main4/main5/main_ge4 on standard axioms; `actual_prime_construction (i) : PrimeConstruction (i+3)` has no hypothesis; wrapper uses `hd` only for `d-3+3=d`; `all_epsilon_lower` needs `1 ≤ d`, `ramsey_upper` needs `3 ≤ s`.
- MainBounds: ∃ C>0, ∀ ε>0, ∃ t₀, ∀ t≥t₀: t^(s−1)/rpow(log t)((s−2)+ε) ≤ ramsey s t ≤ C t^(s−1)/(log t)^(s−2); C before ε; lower coefficient 1; Real.log natural (axSL.log pp.all).
- Bridge: Bridge986Main proves erdos986At_ge_four_sharpLogOnly (c=(s−2)+1=s−1, C=1, ε=1), erdos986_iff_three : Erdos986Statement ↔ Erdos986At 3, classicalRamsey_eq_{sharpLog,five}; all standard axioms (logs_Bridge986Main.log).
- Dates/commits: adc7f12 2026-10-06T21:58:50Z; family-170 paths empty diff adc7f12..1581d4c; PDFs 41 pp / 53 pp (pdfinfo).
- Chen (2610.15293, 11 Oct; AEKS via OpenAI preprints [9],[10]) and Lin–Zhang (2610.17891, 13 Oct; Shearer 1995, "We take as an external input") — both derive r(4,t) by one-step neighbourhood descent; grep: neither mentions Lean or a d=3 construction.
- Bradač v3 (16 Jun) declaration quote verbatim; OpenAI papers never mention the OpenAI origin of §2.5 (grep).
- Paper A seat read §§1–3, 5–6 (+7–8, 11) in PRINTED numbering; §§9–10 (score, completion) unread — page correct for Paper A.

## Findings
1. **WRONG — Paper B section numbers are off by one throughout (file index, not the printed paper).**
   Quoted: "Paper B fixes "an integer d ≥ 5" where its construction is introduced (Theorem 1.2, §1, §6)"; "*Paper B, §§1–3* (foundations, the description and validation theorems, the projection, the polynomial-method rich-line bounds, the learning step)"; "*Paper B, §§4–6 and the entropy lower bound*: holds as read, given §§2–3"; "our referee seat on its §§4–6".
   Evidence: Paper B PDF TOC (pdftotext) — §1 Introduction, §2 Flags, incidence, and selected-tuple entropy, §3 Describing sparse pairs, §4 Learning, §5 Marking, §6 Replacing the context, §7 Completion. "Fix an integer d ≥ 5" occurs in Theorem 1.2 (§1), at the opening of §2 (01-foundations.tex l.4) and "Fix d ≥ 5" in the proof of Theorem 1.2 in §7 (06-conclusion.tex l.16; PDF line "Proof of Theorem 1.2. Fix d ≥ 5"). The seats (referee_s6_geometry.md "§1 foundations (01-foundations.tex)", referee_s6_compression.md "§4 (marking), §5 (compression), §6 (iteration…)") numbered by TeX FILE name 00–06; the page copied that. Paper A's numbering on the same page ("§§1–3 and 5–6") IS the printed one, so the paragraph mixes two conventions. A reader opening the PDF finds §1 = Introduction and §6 = compression.
   Fix: Paper B → "(Theorem 1.2 in §1, §2, and its proof in §7)"; "Paper B, §§2–4 (foundations, …, the learning step)"; "Paper B, §§5–7 and the entropy lower bound (§2): holds as read, given §§3–4"; "our referee seat on its §§5–7". Same fix in bundle README ("Paper B §§1–3 … §§4–6 … given §§2–3").

2. **UNSUPPORTED — "with three of the four helper passes".**
   Quoted: "That seat, the seat on the s = 5 Lean and the formal-statement seat were all cut off by a session limit at 12:31 UTC before finishing, with three of the four helper passes".
   Evidence: none of the four helper files carries a completion marker. r5lean_sub_high.md is 276 bytes, header only ("Status: IN PROGRESS"); r5lean_sub_decouple.md stops at N2 with no verdict; r5lean_sub_predictor.md stops mid-section ("Lean passes τ itself … — CHECK below"); r5lean_sub_tree.md covers only §1a–1b of lem:fresh-test. Original mtimes (/tmp/oaimath/170/seats/) 12:29:34–12:31:16Z, i.e. all four died in the same window. README repeats "(three cut off)" with no evidence which one finished.
   Fix: "with all four helper passes" — or name the one that finished and point to its verdict line.

3. **OVERSTATED — "OpenAI's own assembly" is said to yield s = 4; as written it cannot.**
   Quoted (summary/meta/og): "OpenAI's own ten-line assembly fed d = 3 gives r(4,t) = t³/(log t)^(2+o(1))"; card line: "at d = 3 OpenAI's own assembly yields r(4,t) ≥ t³/(log t)^(2+ε)"; strip: "fed to OpenAI's own assembly it proves the s = 4 case too".
   Evidence: `main_of_primeConstruction (s) (hs : 6 ≤ s)` (FromConstruction.lean l.62) cannot be applied at s = 4 — that is exactly the page's own TypeSL-style control. What yields s = 4 is OUR copy with `6 ≤ s` replaced by `4 ≤ s` (diff of Extra_S4.lean vs l.62–74: only the name and that hypothesis differ). The body says this correctly ("that assembly copied verbatim with 4 ≤ s"); the three short forms do not.
   Fix: "a verbatim copy of OpenAI's assembly with 6 ≤ s relaxed to 4 ≤ s (the hypothesis is used only for side conditions)".

4. **WRONG (minor) — "not the papers' d ≥ 5".**
   Quoted (summary/meta): "The library states its construction for every dimension d ≥ 3, not the papers' d ≥ 5".
   Evidence: only Paper B fixes d ≥ 5; Paper A works in PG(4,q) only (r5 Lean `Space K = Fin 5 → K`, referee_r5_lean.md §2g; Paper A Theorem on K₅-free graphs on ⌊q⁴ log q⌋ vertices).
   Fix: "not Paper B's d ≥ 5 (Paper A is the single case d = 4)".

5. **UNCLEAR / internally inconsistent — the citations sentence.**
   Quoted: "every pin-cite the world seat could reach matches its source — all four to Bradač's v3, Mubayi–Verstraëte, …, Alon–Rödl — with two exceptions: … and Paper B calls its i.i.d. stream Bradač's §2.5 construction".
   Evidence (referee_world.md header + T1b/T4): (a) §2.5 is one of the "four Bradač pin-cites" the sentence first says MATCH, then lists as an exception; the seat graded it "MATCH with an EXPOSITION caveat", not a mismatch — the only MISMATCH is Kollár. (b) The seat checked five Bradač cites (Thm 1.1, §2.5, Claim 2.13, proof of Lemma 2.12, and Lemma 2.1) plus Ellenberg–Oberlin–Tao Thm 4.6, which the list drops. (c) "could reach" misdescribes the rest: the seat's own line is "Not checked (outside brief / not load-bearing): Dvir 2009, Guth–Katz 2010, Elekes–Kaplan–Sharir, Raghavendra–Tan, Shearer 1983, Alon 1996, Kim 1995, Spencer 1977, Codenotti–Pudlák–Resta, Kostochka–Pudlák–Rödl" — not checked is not unreachable. (d) "calls its i.i.d. stream Bradač's §2.5 construction" is stronger than the text: B 01-foundations l.81–84 says "We use Bradač's ordered flag construction [§2.5]. … Sample an ordered stream of N independent uniform flags" — the attribution is of the ordered flag graph; the sampling is stated as B's own step. Also omitted: the geometry seat's cosmetic note that B's GuthKatz2010 is the joints paper, not the distinct-distances paper (referee_s6_geometry.md obj. 9).
   Fix: "Of the pin-cites the world seat checked — five to Bradač's v3, Mubayi–Verstraëte, Mattheus–Verstraëte, Bohman–Keevash, Nie–Wang, Ellenberg–Hablicsek, Ellenberg–Oberlin–Tao, Alon–Rödl — all match except Kollár (Theorem 2 should be Theorem 4); one wording note: B attributes the ordered flag graph to Bradač §2.5, where flags are randomly ordered, while the i.i.d. stream is OpenAI's variant. Classical motivational cites (Dvir, Guth–Katz, Kim, Spencer, …) were not checked."

6. **OVERSTATED — absence stated as fact.**
   Quoted: "No public referee report, reproduction or rebuttal of the s − 2 + o(1) exponent exists — and two notes already build on it."
   Evidence: referee_world.md: "no third-party verification/refutation FOUND"; "the coverage claim rests on title/abstract sweeps + reading"; "HN/MO/Tao/press coverage is a search-coverage claim, not proof of absence". The arXiv API full-text index "does not yet carry the 11/13 Oct notes either". The page phrases the two neighbouring claims correctly ("We found no other published replay", "As far as the world seat's search reached") but this one as existence.
   Fix: "We found no public referee report, reproduction or rebuttal (arXiv title/abstract sweeps, the problem page and forum, FC, teorth, Palomar, HN, MO) — and two notes already build on it."

7. **WRONG (minor) — RSS unit.**
   Quoted: "no process above 7.2 GB".
   Evidence: drive.py l.27 `/usr/bin/time -f 'maxrss_kb=%M'`; GNU time %M is KiB; modules.tsv max 7,171,604 KiB = 7.34 GB = 6.84 GiB. 7.2 comes from reading KiB as 10³ bytes. (README repeats "max RSS 7.2 GB".)
   Fix: "no process above 6.9 GiB".

8. **OVERSTATED (minor) — what `--trust=0` contributes.**
   Quoted: "With --trust=0, both main theorems depend only on propext, Classical.choice and Quot.sound."; bridge: "Everything is on the standard axioms under --trust=0."
   Evidence: `#print axioms` output does not depend on the trust level; the 858 modules were compiled at default trust (drive.py l.27 has no --trust); the --trust=0 axioms runs took 6–7 s (steps.tsv `axSL 0 6`, `axR5 0 7`), so they re-checked no imported module. Bridge986.lean was compiled WITHOUT --trust=0 (bridge/run.sh: only Bridge986Main gets it), so the bridge sentence is literally false for the file that proves classicalRamsey_eq_*. The real independent kernel re-check is leanchecker --fresh (which did not cover the probe or bridge files — their own few declarations were kernel-checked at elaboration only).
   Fix: drop "--trust=0" as assurance, or say "#print axioms (on the compiled library) shows only …; leanchecker --fresh then re-checked …; the probe and bridge declarations were kernel-checked when compiled, not re-checked by leanchecker".

9. **OVERSTATED (minor) — vacuous negative controls presented as evidence.**
   Quoted: "It stops at 4: asking it for PrimeConstruction 2 is a type error"; "applying the s ≥ 6 theorem at s = 5 is a type error"; "s = 3 through the library fails".
   Evidence: Extra_S4neg.log: `PrimeConstruction (0 + 3)` vs `PrimeConstruction 2` — a numeral mismatch; typeSL.log: `5 ≤ s` vs `6 ≤ s`; Neg_s3.lean fails because `norm_num` cannot prove `4 ≤ 3` (log: "unsolved goals ⊢ False"). Each fails by construction from the hypothesis text and could not have passed; none tests mathematics. "It stops at 4" reads as a mathematical limit of the method; the library simply never states a d = 2 instance (and one would give only r(3,t) ≥ t²/(log t)^(1+ε), weaker than Kim, so nothing is missing).
   Fix: "The library's construction starts at d = 3, so this route gives nothing at s = 3 (which is classical anyway)"; call the three controls "hypothesis sanity checks", not evidence of scope.

10. **UNCLEAR — "mutation-tested in both directions".**
   Quoted: "an instrument we mutation-tested in both directions (one token of a hypothesis changed ⇒ MISMATCH; sorryAx added to an axiom list ⇒ flagged)".
   Evidence: statement_match_mutation_README.txt / _result.txt: both mutations exercise the must-FLAG direction, on two different checks (statement, axioms). Nothing tests the other direction (that a genuinely equal statement printed differently still reads MATCH).
   Fix: "mutation-tested on both of its checks".

11. **UNCLEAR — "2s − 4 below, s − 2 above" without its range.**
   Quoted: "So after June the live question was the power of the logarithm: 2s − 4 below, s − 2 above."
   Evidence: at s = 3 the log power was settled (Kim 1995 lower t²/log t vs AKS); at s = 3, 2s − 4 = 2 is not "the best below". A Ramsey theorist will object.
   Fix: "for s ≥ 4: 2s − 4 below (Mattheus–Verstraëte's 4 at s = 4), s − 2 above."

12. **OVERSTATED (register) — the s = 4 clause in the title and card.**
   Quoted: title "and the same Lean library proves the s = 4 case, r(4,t) = t³/(log t)^(2+o(1)), which neither paper states"; card "the Lean library under them proves r(4,t) = t³/(log t)^(2+o(1)) too, a case neither paper states"; tag "THE SAME LIBRARY ALSO PROVES s = 4, KERNEL-CHECKED".
   Evidence: true as stated, but the statement was published on paper on 11 Oct (Chen) and 13 Oct (Lin–Zhang); the page says "The r(4,t) statement itself is not new" only mid-paragraph. A reader of the title/og:title alone (which is all a feed shows) will take r(4,t) = t³/(log t)^(2+o(1)) as news found here.
   Fix: title/og: "…proves the s = 4 case directly — r(4,t) = t³/(log t)^(2+o(1)), derived on paper by Chen and by Lin–Zhang the week before; neither paper states it". Card tag: "…ALSO PROVES s = 4 (ALREADY DERIVED ON PAPER BY CHEN, LIN–ZHANG), KERNEL-CHECKED".

13. **MINOR — "OpenAI's two proofs, kernel-checked on our machine" (card title).**
   Evidence: what was kernel-checked are the two Lean proofs; the papers' arguments are labelled (c) on the page itself.
   Fix: "OpenAI's two Lean proofs, kernel-checked on our machine".

14. **MINOR — argument paragraph and card line compress the contradiction inaccurately; two symbols undefined.**
   Quoted: "But a decoder can rebuild it from dσℓ + O(k)"; card: "a long independent set would carry entropy dσℓ + ηℓ log σ (σ = log q) but compresses to dσℓ + O(k)"; card: "polynomial-method descriptions of sparse incidence structures kept below the characteristic".
   Evidence: B §§5–7 (referee_s6_compression.md pass 1/2): the first description costs dσℓ + Λ + O(k) + O(Δqσ) with Δ = (d−1)σ, i.e. Θ(qσ²) ≫ the surplus; only after T = ⌈8/η⌉ rounds of shorter subsequences does a Θ(k)-long F_* get dσℓ_* + O(k). The card drops "at least … − O(k)". It is the polynomial DEGREES that are kept below the characteristic. On the page ℓ (the deterministic length Θ(k)) and ⊥ (point lies on hyperplane / covector vanishes) are never defined.
   Fix: "…after a bounded number of rounds, a decoder rebuilds a Θ(k)-long subsequence from dσℓ + O(k)"; define ℓ and ⊥; "…descriptions whose polynomial degrees stay below the characteristic".

15. **MINOR — "(r(3,t) ≍ t²/log t, Kim 1995)".**
   Evidence: Kim 1995 is the lower bound; the upper bound is AKS 1980 (Shearer's constant). Fix: "(r(3,t) ≍ t²/log t: AKS 1980 above, Kim 1995 below)".

16. **MINOR — credit for the s = 4 observation.**
   Quoted: "the observation that the library proves s = 4 directly (found by our formal referee seat)".
   Evidence: referee_s6_compression.md objection 1 ("!! Lean `actual_prime_construction (i : ℕ) : PrimeConstruction (i+3)` — EVERY d ≥ 3") found it independently; referee_formal.md "KEY FORMAL FINDING". Fix: "found independently by two of our seats (formal; Paper B §§5–7)".

17. **MINOR — "every one served by Claude Opus 5.5 (checked in the transcripts)" is not checkable from the bundle.**
   Evidence: only referee_formal, referee_s6_geometry and referee_world self-identify ("Opus 5.5"); the transcripts are not in the bundle. Fix: add a receipt file (per-seat `message.model` counts from the transcript JSONL) or say "per the session transcripts (not in the bundle)".

18. **WRONG (ship-blocking for the evidence chain) — the bundle link is dead for every reader.**
   Quoted: source link "Our bundle — the replay (…), the bridge and its controls, ten referee reports …" → https://github.com/pw/ErdosProblemADay.com/tree/main/verification/986/openai-referee.
   Evidence: `gh api repos/pw/ErdosProblemADay.com` → private: true / visibility: private; and `git status` in the worktree shows `?? verification/986/` (not yet committed). Project CLAUDE.md: "those links only resolve if the repo is public." Every "the bundle" / "in the bundle as they stand" sentence on the page points a cold reader at a 404.
   Fix: commit + push the bundle, and either make the repo (or a mirror of verification/) public or host the bundle elsewhere before shipping; otherwise remove "in the bundle" phrasing.

19. **MINOR — "copies FC's two definitions and its statement verbatim, changing only the namespace".**
   Evidence: Bridge986.lean adds `open SimpleGraph` (README says so) and renames the binder `hs` → `_hs` in `Erdos986Statement`, and turns the theorem into a `def … : Prop`. All harmless, but "only the namespace" is not literal. Also "What it checks is that OpenAI's ramsey is the Ramsey number Formal Conjectures means" holds as both are read in Mathlib d13f23b7, not FC's pin (said one sentence earlier — keep the qualifier attached).
   Fix: "verbatim up to the namespace, an `open SimpleGraph`, and an unused binder name".

20. **UNCLEAR — "CLOSED OCT 20, 2026" badge.**
   Evidence: the page's own strip says the community database has #986 PROVED as of 2026-06-21 (Bradač); the Oct 20 entry closes nothing of Erdős's question and the result is OpenAI's. A cold reader will read the badge as "#986 closed on 20 Oct (here)". Site convention (STATUS.proof_claimed → "CLOSED"), but it collides with this page's history.
   Fix: a qualifier on this entry (e.g. "REFEREED", or "CLOSED (JUNE, BRADAČ) · SHARPENED (OCT, OPENAI)").

21. **MINOR — relative dates in evergreen text.** "Two notes derived that r(4,t) statement on paper last week" (summary/meta/og, card) — will be wrong in a week. Fix: "on 11 and 13 October".

22. **MINOR — "the ten-line assembly".** FromConstruction.lean l.62–74 is 13 lines (11-line body). Fix: "the short assembly" or "thirteen-line".

23. **MINOR — Chen's route.** "Chen through the recent proof of the Ajtai–Erdős–Komlós–Szemerédi bound, itself another OpenAI preprint": Chen cites two OpenAI preprints for it ([9] "A logarithmic independence bound for clique-free graphs" as Lemma 1.3, [10] correspondence colouring which implies it). Fix: "itself from two further OpenAI preprints".

## Items checked and NOT objected to (for the shipping seat)
- "we found no public statement of that (same search as above)" — correctly a coverage claim; no sentence makes the r(4,t) statement ours or new (body: "The r(4,t) statement itself is not new"; "What we add is that the statement is a kernel-checked theorem of OpenAI's library").
- Statement-fidelity sentences (C before ε, coefficient 1, natural log, sInf junk makes the lower bound false, limit is a corollary) match referee_formal.md §1 and the pp.all print.
- Bridge: "FC's whole statement is equivalent to its s = 3 instance" is exactly `erdos986_iff_three : FC.Erdos986Statement ↔ FC.Erdos986At 3`; "c = s − 1 and C = 1, from ε = 1" matches `erdos986At_of_mainBounds`.
- Seat attributions for Paper B (projection orientation, high-moment sketch reconstructed, prime hypothesis / q^{41/80} / E–H, z = x⁷ flatness check, Claim 2.13 modification with PG(3,5), PG(3,7), PG(2,11) simulation, conditioning robustness, log σ ledger, d ≥ 5 unused) all quote-match the two reports (modulo the section-number item 1).
- Kollár Theorem 2 vs 4 matches referee_world.md T4 exactly. Paper A coverage and the "read by no one" sentence match referee_r5.md.
- Provenance paragraph matches Bradač v3 and the grep of both OpenAI TeX trees.

VERDICT: SHIP WITH FIXES — the mathematics, numbers and Lean claims hold; must-fix before ship: 1 (Paper B section numbers), 2 (helper-pass count), 3 (assembly overclaim in summary/card/strip), 6 (absence as fact), 18 (private/uncommitted bundle link); the rest are minor.
