# Blind hostile proofread — /day/551-openai-cycle-clique-ramsey-refereed (page551.txt / page551.html), 2026-10-20 ~23:05Z

Scope: every sentence of the entry (summary/meta description, title, "Newer public claim" box, body, sources list) and the
HEADLINES card (src/index.js line 10751), checked against the paper .tex, lean-build/, bridge/, finite/, seats/*, live/raw.html,
the openai/math git history and the bundle under ~/ErdosProblemADay-main/verification/551/cycle-clique-refereed/.
Categories: WRONG · OVERCLAIM · UNSUPPORTED · UNCLEAR · INCONSISTENCY. Severity H/M/L.
Scratch files only in seats/blind_work/.

**Counts (43 findings, primary category):** WRONG 9 (#1–5, 14, 28–30) · OVERCLAIM 7 (#7–9, 12, 19, 22, 41) · UNSUPPORTED 6 (#10, 11, 17, 20, 23, 42) · UNCLEAR 17 (#15, 18, 24–27, 31–40, 43) · INCONSISTENCY 4 (#6, 13, 16, 21; #5 is also one). Nothing found that touches the mathematics of the claim itself; every error is in how our own checks are described.

## A. High-severity findings

1. **WRONG (H)** — "What catches it is the comparison of the regenerated traces with the shipped file, which verify.py also performs and which our run passed."
   The degree-test deletion (seat F mutation S6) was made in a copy of `original_checker.py`, which writes no trace at all.
   verify.py's only trace check is `sha(independent/certificates.jsonl) == sha(data/certificates.jsonl)` — the INDEPENDENT
   program re-producing its own shipped output. Seat F says so explicitly ("verify.py's 'trace equals supplied data' is a
   self-consistency check of the independent program against its own earlier output, not a third opinion") and lists what
   actually certifies the rule: (a) line reading, (b) seat F's own check that the original's `initial()` matrices equal the
   trace's `initial` flags for all 3,099, (c) seat F's explicit-construction derivation. The page attributes the catch to the one
   check that cannot see this mutation, and contradicts seat F's recommendation that verify.py *should* check the matrices.
   Replace: "What catches it is a check of the matrices themselves: our finite-stage seat confirmed that the original checker's
   initial matrices equal those in the shipped trace for all 3,099 patterns, and that both equal an independent explicit-construction
   derivation. verify.py compares only the independent checker's regenerated trace with the shipped file; that would catch this
   change in the independent program, not in the original."

2. **WRONG (H)** — "the finite stage is (d) computer-assisted, by three implementations that share the pattern definition and nothing else"
   seatF_finite.md §3 "Shared (non-independent) elements": the two Python programs share (i) the labelling convention,
   (ii) the ball-bound arithmetic (`ball_options` is "a line-for-line transliteration of (9.8)–(9.11) incl. the exception test"),
   (iii) the procedure skeleton and the (visited, end) state-merging idea. The Lean uses "same patterns, same labelling"
   (patternChoices = the same recursion as `forests`). Seat F's third validator re-checks the witnesses recorded in the SHIPPED
   trace, so it shares the trace data. Replace: "by two released Python programs (which share the labelling and the ball-bound
   arithmetic), a Lean proof that re-checks explicit witness certificates in the kernel, and our seat's validator of the shipped
   traces; the inference rules themselves were re-derived by hand, since an unsound rule would be replicated in both programs."

3. **WRONG (H)** — "each reproduces the published output byte for byte, "Verified 3099 patterns in all 42 parameter pairs; zero unresolved", in 197 s."
   The published output (`data/expected-output.txt`, 130 bytes) is the 13 rows of Table 2 ("5 0 4 3" … "17 0 878 1"). The quoted
   sentence is printed once, by verify.py, after both runs. 197 s is verify.py's total wall time (finite/verify1.log: wall 197.03 s);
   the checkers took 50.5 s and 146.0 s (run1/run.json). Replace: "each prints the published Table 2 rows byte for byte, and verify.py
   ends 'Verified 3099 patterns in all 42 parameter pairs; zero unresolved' (both checkers together: 197 s, 51 s and 146 s)."

4. **WRONG (H)** — "We mutation-tested the matcher three ways: a changed numeral in a definition, a challenge without sorryAx, and a solution with an extra axiom."
   lean-build/mut: M1 changes `Fin N` to `Fim N` inside RamseyProperty (cmp_M1.log vs cmp.log) — an identifier, not a numeral.
   All three mutations are edits of the printed logs fed to statement_match.py (cmp_M1.log, cmp_M2.log, ax_M3.log with
   `Lean.ofReduceBool` added), not of Lean sources; a reader will assume Lean files were mutated. Replace: "We mutation-tested the
   matcher on edited copies of the printouts: one character changed inside RamseyProperty's body (Fin → Fim), sorryAx deleted from the
   challenge's axiom list, and Lean.ofReduceBool added to the solution's. It flagged each one."

5. **WRONG + INCONSISTENCY (H)** — summary / meta description / og:description: "Erdős, Faudree, Rousseau and Schelp conjectured in 1978 that R(C_m, K_n) = (m−1)(n−1)+1 whenever m ≥ n ≥ 3, with (3,3) excepted."
   The body (and seat W §3, EFRS p. 64 rendered) says the opposite: "the 1978 paper's own sentence, 'It is conjectured that this formula
   holds for all m ≥ n', has no (3,3) exception". The summary is the text that goes to search engines and link previews.
   Replace: "Erdős, Faudree, Rousseau and Schelp conjectured in 1978 that R(C_m, K_n) = (m−1)(n−1)+1 for all m ≥ n; in its standard form
   (n ≥ 3, (3,3) excepted, as stated by Keevash, Long and Skokan) it is Erdős problem #551."

6. **INCONSISTENCY (H)** — body "Two hostile AI referee seats then read separately." vs summary "three hostile AI referee seats (on the large-clique
   argument, on the finite stage and its code, and on the sources) agreed" vs card "THREE AI REFEREE SEATS: NO GAP".
   The body later cites "Seat W re-checked it…" without ever introducing a Seat W. Replace in the body: "Three hostile AI referee seats
   then read separately: a proof seat (§§5–8), a finite-stage seat (§9 and Appendix A) and a sources seat, Seat W (§1 and the literature)."
   (Card: "TWO AI REFEREE SEATS ON THE MATHEMATICS + ONE ON THE SOURCES" if you want to keep the distinction.)

7. **OVERCLAIM (H)** — "Labels: the structural argument (§§2–8) is (a) elementary, read line by line by us and by a separate seat"
   §§2–4 had ONE reader. COMMON.md told every seat "The main seat has ALREADY read §2, §3 and §4 line by line … you need not repeat
   that"; seat P's scope is §5–§8 and it took Theorem 3.1 and Lemma 2.2 as quoted statements. Replace: "§§2–4 read line by line by the
   main seat; §§5–8 by the main seat and again by a separate proof seat".

8. **OVERCLAIM (M-H)** — "model-checked Lemmas 7.1 and 8.1–8.3 and the separation and counting in the final packings over all weighted path systems for t = 9 to 12"
   seatP_proof.md "Limits": "The model check works at the path-system level only … The graph-level steps — ball growth (7.1)/(7.2),
   Lemma 7.3's clique case, Lemma 8.3's |B_1| ≥ t+1 and |B_2| ≥ k+1, the per-ball triples via Lemma 5.3, Lemma 6.4's separation — are
   checked by hand only … The per-ball independence values the model check adds up … are the paper's". For Lemma 8.3 the program checks only
   the "≥ 2 nonsingleton chains" clause. Replace: "model-checked, at the level of path systems (forest plus amounts), the replacement
   arguments of Lemmas 7.1, 8.1 and 8.2, Lemma 8.3's two-chain claim, and, for every final packing, that each required pair of bases has
   its whole parameter range forbidden and that the paper's per-ball independence values sum to more than k: about 79 million replacement
   systems for t = 9 to 12 and every k from t to 2t+1, no violation. The graph-level steps it took from the paper were checked by hand."

9. **OVERCLAIM (M-H)** — "Every prior-result sentence in §1.1 says what its source says."
   Seat W verdict line: "COULD NOT CHECK full texts of Chartrand–Schuster 1971 (AMS bot-wall), Schiermeyer 2003, Zhang–Zhang 2009,
   Bataineh et al. 2011, Nikiforov CPC published version … verified via abstracts/titles + independent secondary sources instead."
   Replace: "Every prior-result sentence in §1.1 agrees with its source; we read the primary text for all but five (Chartrand–Schuster,
   Schiermeyer, Zhang–Zhang, Bataineh–Jaradat–Al-Zaleq, and the journal version of Nikiforov), which we checked through abstracts,
   titles and later citations."

10. **UNSUPPORTED (H)** — "Every referee seat was served by Claude Opus 5.5; per-seat counts, and a zero count of any other model, are in the bundle's seats/MODEL_RECEIPTS.txt."
    No MODEL_RECEIPTS.txt exists in /tmp/oaimath/189/seats/ or in the bundle (verification/551/cycle-clique-refereed/seats/). Only
    main_reading.md self-identifies its model. Generate the receipts (transcript `message.model` grep per seat) before publishing, or cut the sentence.

11. **UNSUPPORTED (H, site-wide)** — "our notes are in the bundle as seats/main_reading.md" and the Sources link "Our bundle — …"
    point to github.com/pw/ErdosProblemADay.com, which is PRIVATE (`gh api repos/pw/ErdosProblemADay.com` → private; anonymous GET of
    …/tree/main/verification/505 → 404). Every "in the bundle" claim is unverifiable by a reader. Same convention on 68 links site-wide —
    either publish the verification tree (or a public mirror) or stop citing it as the reader's evidence.

12. **OVERCLAIM (M)** — "Ours is a second one on different hardware, plus the from-scratch check and the bridge below."
    The from-scratch check has not happened: leanchecker --fresh began 22:58:34Z, its log is empty, the process is still running.
    Replace: "…plus a from-scratch check, still running, and the bridge below." (Also: MathVet ran OpenAI's comparator tool; ours is our own
    pp.all statement match, not the comparator — say which.)

13. **INCONSISTENCY / OVERCLAIM (M)** — card title "the cycle–clique Ramsey conjecture of 1978 now has a complete proof" and the page banner
    "CLOSED OCT 20, 2026" vs body "if the proof stands it is closed" / "No human has refereed this proof" / entry status `proof_claimed`.
    Pick one stance. Either the kernel-checked Lean (statement matched) is the warrant — then say so in the body ("the Lean proof, kernel-checked
    here, closes it whatever a human referee finds in the prose") — or the title should read "now has a complete claimed proof".

## B. Medium findings

14. **WRONG (M)** — "A second route in Construction/ (261 further modules, 194 MB, per-k certificates) proves the same statement as cycle_clique_main_unconditional ; we did not replay it."
    Construction/ holds 259 modules; 261 = those 259 + `CycleClique/Main.lean` + `CycleClique/RamseyNumbers.lean` (the two top-level files
    outside thm_main's 182-module closure; checked by diffing the closure against the directory). `cycle_clique_main_unconditional` states
    `IsRamseyNumber m n ((m−1)(n−1)+1)` for (m,n) ≠ (3,3) — a different predicate, without the (3,3) value; the cycleCliqueRamsey form is
    `cycleCliqueRamsey_unconditional`. And since it was not replayed, "proves" is unsupported. Replace: "A second route — the 259 modules of
    Construction/ plus Main.lean and RamseyNumbers.lean, 261 modules and 194 MB outside the comparator's closure, with per-k certificates —
    states the theorem as cycle_clique_main_unconditional (via an IsRamseyNumber predicate) and cycleCliqueRamsey_unconditional; we did not replay it."

15. **UNCLEAR (M)** — notation collision on k, worst in the bridge paragraph: "a shifted cycle length, C k+1 , fails at rfl".
    The problem quote uses k for the cycle length; "The argument" redefines k = m − 1 so that C_{k+1} is the TARGET cycle; the bridge
    paragraph silently returns to FC's k = cycle length. Read with the page's own notation, "a shifted cycle length, C_{k+1}" names the
    correct statement. Replace: "a shifted cycle length (cycleGraph (k+1) in place of FC's cycleGraph k, where FC's k is the cycle length m)
    fails at rfl". Also add one line after the problem quote: "Below we write m for the cycle length, as OpenAI does."

16. **INCONSISTENCY (M)** — "for n = 8 only 8 ≤ m ≤ 15 and, through Nikiforov, m ≥ 34 were settled" and "Schiermeyer's 2003 range …, which Nikiforov's
    supersedes for n ≥ 7" vs the same page: "the published proof of Nikiforov's range m ≥ 4n + 2 has a step in Case 4.1 that does not follow as printed".
    Either qualify ("through Nikiforov's theorem, whose printed proof has the Case 4.1 problem noted below, m ≥ 34; unconditionally m ≥ 48
    (Schiermeyer) and m ≥ 62 (Bondy–Erdős)") or forward-reference the note.

17. **UNSUPPORTED (M)** — "Our July report on this problem said that the published proof of Nikiforov's range … Seat W re-checked it against the rendered arXiv pages (the only version)"
    Seat W: "Published CPC 14(3) 349–370 text NOT seen (paywalled)"; "the only version" is the only ARXIV version. Replace: "…that the printed proof
    (arXiv v1, the only arXiv version; we have not seen the journal text) of Nikiforov's range…". The July report (ledger, wave 5z, 26 July) is not linked — link it.

18. **UNCLEAR (M)** — "the displayed chain needs 2(r 1 + r 2 ) ≤ r + 1, where only r 1 + r 2 ≤ r + 1 and r 1 ≤ (r + 1)/2 are established; r = 6, p = 29, r 1 = 2, r 2 = 5 makes the step read 37 ≤ 30."
    r, p, r1, r2 are Nikiforov's, never defined here. Add: "(Nikiforov proves r(K_{r+1}, C_{p+1}) = pr + 1 for p ≥ 4r + 5, so r = n − 1 and p = m − 1;
    r1 = α of an end block B of G − S and r2 = α of the rest; the second inequality of his chain, p + 2r1 + 2r2 − (p−r−1)/2 + 5 ≤ p + r − (p−r−1)/2 + 6,
    becomes 37 ≤ 30.)"

19. **OVERCLAIM (M)** — "We read §§2–9 line by line ourselves, re-deriving every inequality, vertex count and case split, and found nothing above exposition"
    "Ourselves" on a Patrick White + Claude page reads as if a human read it; it was the main Claude seat (main_reading.md line 2). Its notes
    (written by 21:24Z; COMMON.md at 21:09Z already says §§2–4 were done) record re-derivations for §§2–8 in detail, but for §9.8 say only
    "Lemma 9.8 packing + the radius-pruning argument + the branch-and-bound search: correct." Replace: "The main seat (Claude) read §§2–9 line by line
    and found nothing above exposition; the steps it re-derived are recorded in seats/main_reading.md."

20. **UNSUPPORTED (M)** — "and Faudree and Schelp's statement of the same conjecture in their 1976 Kalamazoo paper (published 1978)"
    Seat W saw only secondary sources: DS1.18's citation "[FS4, EFRS2]" and Yang–Huang–Zhang's paraphrase ("stated the following problem: …
    does the equality hold for n ≥ m?") — a question, from a paper we did not read. Replace: "and Faudree and Schelp's 1976 Kalamazoo paper
    (LNM 642, 1978), which the survey literature credits with first asking the same question (we have not seen its text)."

21. **INCONSISTENCY (M)** — how many implementations exclude the 3,099 patterns: card "twice in Python and, by a different encoding, in Lean";
    summary "two Python programs and a Lean proof each exclude"; body heading "re-run three ways" (= two Python re-runs + seat F's trace validator);
    labels "three implementations". Say once, everywhere: two Python searches (released) + a kernel-checked Lean certificate check (released) +
    our validator of the shipped traces. The third "way" in the heading is a re-check of recorded witnesses, not a re-run of the search.

22. **OVERCLAIM (M)** — summary: "but the constant C was never computed, so finitely many pairs stayed open"
    KLS's concluding remarks say THEY did not compute C ("less than 20" only suggested; July report wave 5z §1) — "never" is a universal
    nobody checked. And the "so" is a non sequitur: an explicit C would still leave finitely many pairs to check. Replace: "Keevash, Long and
    Skokan proved it in 2021 for m ≥ C log n / log log n, which settles every large n but leaves finitely many pairs — and their C is not explicit,
    so not even the list of open pairs was known."

23. **UNSUPPORTED (L-M)** — "The same program at t = 8 … reports 169 violations" and "changes 2,471 of the 3,099 initial matrices"
    No artifact: seatP_work has model_t10/11/12.out and altcount_t9.out but no t = 8 output; no file in F_work contains 2471 (only the reports
    say so). Save both outputs into the bundle before citing the numbers.

24. **UNCLEAR (M)** — the "Newer public claim" box (line 41) is two notes concatenated: "…bridged to a verbatim copy of Formal Conjectures' erdos_551 — see
    /day/551-openai-cycle-clique-ramsey-refereed — family 189 at github.com/openai/math , OpenAI's own Lean proves Theorem 1.1 — …kernel-replayed on our
    machine on 20 Oct 2026 (…) ; a kernel-checked bridge of ours derives a verbatim copy … — see our /day entry." The replay, statement match and bridge
    are each said twice, and the /day path is plain text, not a link. Collapse to one sentence with one link.

25. **UNCLEAR (M)** — §§5–8 sketch: "a short outside path between two representatives would be such an improvement unless the system has one of exactly
    three shapes, and in each shape the neighbourhood balls of the representatives are pairwise separated …"
    Omits Lemma 7.4 (some pair of representatives MUST have a short outside path, of parameter 1..6, else the radius-2 balls are already
    separated and give more than k independent vertices), so the reader cannot see where the no-short-path case goes. Also the balls are around
    chosen BASES, not all representatives. Suggest: "If no two representatives were joined by a short outside path, their radius-2 balls would be
    separated and hold more than k independent vertices (Lemma 7.4); so some short path exists, and it would be such an improvement unless the system
    has one of exactly three shapes (Lemma 8.2). In each shape, balls around suitably chosen representatives are again separated and carry more than
    k independent vertices (Prop. 8.4)."

26. **UNCLEAR (M)** — "Fix a maximum clique Q and a system of internally disjoint paths between its vertices, with interiors outside Q"
    Leaves out that the paths' endpoint pairs must form a linear forest on Q (disjoint chains) — the property that lets the system be closed into
    one cycle through edges of Q, and the "chain" the next paragraph refers to ("along each chain of paths"). Add "whose endpoint pairs form disjoint
    chains (a linear forest) on Q". Further undefined on the page: "budget" (B = k − t, the allowed total interior), "admissible pairs (k, t)"
    (5 ≤ k ≤ 17, max{3,⌊k/2⌋} ≤ t ≤ min{8,k}), "representative", "the set E in Lemma 9.4", "the degree test", "(9.11)", "route A".

27. **UNCLEAR (M)** — "large-clique argument" (summary: "three hostile AI referee seats (on the large-clique argument, …)"; Lean paragraph:
    "clique number ≥ 9 to the large-clique argument") while §3 is headed "A large clique (§3)" on the same page. Use "the t ≥ 9 argument" for §§5–8.

## C. Low-severity findings

28. **WRONG (L)** — "#print axioms gives exactly … for main (the range m ≥ n ≥ 3)". `main` assumes (m, n) ≠ (3, 3) (MainTheorem/FiniteRange: `hne : (m, n) ≠ (3, 3)`).
    Replace "(the range m ≥ n ≥ 3, (m,n) ≠ (3,3))".

29. **WRONG (L)** — "Every pattern ends in a contradiction: 3,049 at the first packing test and 50 after strengthening."
    Paper §9.6: output 2 = "after adding required-path constraints or strengthening the matrix"; seat F's W7 shows 4 of the 50 close at the
    required-path step with no strengthening round. Replace "…and 50 after the required-path rule or strengthening."

30. **WRONG (L)** — "The same 1978 page asks two more questions, which the problem page repeats: the smallest m …, and which m minimises R(C_m, K_n) for fixed n."
    The problem page asks "what is the minimum value of R(C_k,K_n)" — the value, not the minimiser (seat W §3: "Bloom paraphrases loosely").
    Replace "which the problem page repeats (the second as 'the minimum value of R(C_k, K_n)')".

31. **UNCLEAR (L)** — "about 43,000 kernel-evaluated decide calls": this is a grep count of the token `decide` in the 182 source files (43,320;
    43,243 as `by decide`), not a kernel count. Say "about 43,000 `decide` proofs in the source".

32. **UNCLEAR (L)** — "is rejected with a type mismatch against 10": Lean prints the term's type as `(4 - 1) * (4 - 1) + 1` (logs/typectl.log).
    "…rejected: the term has type R(C_4,K_4) = (4−1)(4−1)+1, not = 9".

33. **UNCLEAR (L)** — "does not list this paper, although its scope note lean/docs/189.md and the comparator are in the same commit."
    Same commit as what? All three files date from the initial commit, and formalization.yaml was revised again on 7 October (3014888) still
    without it. Replace: "…although the scope note and the comparator have been in the repository since the initial commit, and the catalogue was
    revised on 7 October without adding it."

34. **UNCLEAR (L)** — "(a mutated enumerator fails on 38 of the 42 pairs; the other 4 have zero budget either way)" and "Raising every budget by one gives
    5,735 instead, so the count is not insensitive." The mutation is unnamed (lean_pattern_lists_MUT.py lowers every budget by one, clamped at 0, so the
    four t = k pairs are unchanged); "not insensitive" is a double negative. Replace: "(lowering every budget by one breaks 38 of the 42 pairs; the other
    four, t = k, have budget 0 either way)" and "…gives 5,735 instead, so an off-by-one in the budget would have shown."

35. **UNCLEAR (L)** — "with minimum degree ⌊k/2⌋" → "with minimum degree at least ⌊k/2⌋"; and "If not" applies only for k ≥ 8 (for k ≤ 7 the triangle
    of Lemma 3.2 already gives t ≥ max{3, ⌊k/2⌋}).

36. **UNCLEAR (L)** — §4 sketch "every short connection … closes a C 4 or C 5 , so those neighbourhoods are separated, and expansion makes them too big."
    Fits k = 4 with a K_4; for k = 3 (and k = 4, ω = 3) the last step is a further C_4/C_5 through vertices outside the neighbourhoods or an
    overlapping-triangle case analysis (main_reading.md §4), not a size count. Add "mostly" or "and a short case analysis finishes".

37. **UNCLEAR (L)** — "We copied … verbatim (…; only the enclosing namespace renamed)". The copy keeps FC's namespaces SimpleGraph and Erdos551 but
    wraps them in a new outer namespace Bridge551, and drops FC's `@[category …]` attributes and docstrings. Say "wrapped in an outer namespace,
    attributes and docstrings dropped; definitions and statements character-identical."

38. **UNCLEAR (L)** — "its author replied that he had not yet checked the proof's axiom closure": author's gender not established; "the author replied that the
    formal_proof link was pending because they had not yet checked…".

39. **UNCLEAR (L)** — "The theorem and both of its proofs are OpenAI's" — both = the paper's proof and the Lean, or the two Lean routes? Say which.

40. **UNCLEAR (L)** — card line: "every independent set I sees at least k|I|+1 vertices" → "every nonempty independent set I has a closed neighbourhood of at least
    k|I|+1 vertices"; "That forces a clique of order ⌊k/2⌋" → "of order at least max{3, ⌊k/2⌋}".

41. **OVERCLAIM (L)** — card tag / title "41 PAGES READ LINE BY LINE HERE": the main seat read §§2–9; §1 and the bibliography were checked by the sources seat,
    Appendix A by the finite-stage seat. Defensible as a union, but "§§2–9 READ LINE BY LINE HERE" is the accurate version.

42. **UNSUPPORTED (L)** — bundle link label "…the replay (driver, per-module log, probes, statement match, leanchecker)…": the bundle's replay/logs has no
    leanchecker log yet (it is still running). Fine once the update lands; until then drop "leanchecker" from the label.

43. **UNCLEAR (L)** — labels "(a) elementary", "(d) computer-assisted" and "route A" are the site's private scheme; one parenthetical gloss
    ("our labels: (a) proved in the text by elementary means … (d) computer-assisted") and naming route A where the two routes are introduced.

## D. Checked and correct (no action)
Problem-page quotes (statement, Bondy–Erdős k > n²−2, Nikiforov k ≥ 4n+2, KLS, Tao 01 Sep 2025, 0 proof claims, DECIDABLE 2025-08-31);
Bondy–Erdős Theorem 4 is ⩾ (seat W rendered); 41 pp., dated 25 Sep 2026; initial commit adc7f12 = 2026-10-06 14:58:50 −07:00 = 21:58:50Z;
preprint dir, comparator, Lean dir and docs/189.md untouched since; HEAD 1581d4c; formalization.yaml omits the paper; 182-module closure,
28,344,292 bytes; 443 modules; source audit (only "axiom" hit is a docstring in Construction/PublishedInputs.lean); build 21:06:15→22:57:23Z
= 1 h 51 min, W = 3, 0 errors on 182/182, max RSS 8,211,088 KiB = 7.83 GiB; axioms of thm_main/main/exceptional/ramsey_upper/
finite_range_verified/ramsey_lower_counterexample = {propext, Classical.choice, Quot.sound}; pp.all match of thm_main + both defs
(lens 1182/641/191); planted sorry → sorryAx; Pos44 elaborates; reduced_counterexample_impossible's split (k ≤ 4 / ω ≥ 9 / clique bound →
finite_verification) as described; 42 pairs, Table 1 rows, 3,099, budget+1 → 5,735; Lean lists = our enumeration on all 42; patterns_k_t_coverage by
`decide +kernel`; both checkers' stdout = expected-output.txt; trace sha matches; Table 2 = 3,049 + 50; seat P's t ≤ 70 arithmetic, 78.9 M Lemma-7.1
systems (+3.2 M step-detours) for t = 9..12, Lemma 5.3 over α ≤ 2 graphs on 6–11 vertices, E2/E3 notes; seat F's 3,099/3,099, 5 negative controls,
W10 = 4 all-singleton t = k patterns, S6 table byte-identical, E1 (E as any subset); bridge: verbatim statements vs world/FC_551.lean and
FC_SimpleGraph_Ramsey.lean, rw + rfl, threshold 4, standard axioms, wrong-value control fails at rw, cycleGraph (k+1) control fails at rfl;
FC toolchain v4.33.1 vs OAI v4.34.1; FC tag research open, PR #6992 state; MathVet 19 Oct pass; Bloom 8 Oct post; EFRS "for all m ≥ n" with no
(3,3) exception; R(C5,K8) = 29 = 4·7+1; DS1.18 Table Vb R(C8,K9) = 56 < 57 and the 8·K7 witness; Nikiforov 37 vs 30 arithmetic (p = 29, r = 6:
(p−r−1)/2 = 11, 29+4+10−11+5 = 37, 29+6−11+6 = 30); leanchecker --fresh started 22:58:34Z and is running.

## E. Is the mathematics explained well enough for a combinatorialist who has not read the paper?
Mostly yes for §§2–4 and §9: the minimal-counterexample/expansion step, the BFS-layer clique bound with the 2p + (k+1−2p) cycle count, and the
"pattern = weighted linear forest up to isomorphism" reduction are stated crisply and correctly. Three things stop a careful reader:
(i) the letter k means the cycle length in the problem quote and the bridge, but m − 1 in the argument (finding 15);
(ii) the §§5–8 paragraph skips the linear-forest condition, never says why a short path between representatives must exist (Lemma 7.4), and uses
"chain", "representative", "balls", "separated" without definitions (findings 25–26) — as written it reads as a gesture, not an outline;
(iii) the finite-stage and Lean paragraphs lean on undefined internals (budget, E, the degree test, (9.11), pp.all, sorryAx, route A).
A five-line glossary (Q, h = k+1−t, amount, chain, representative, B_r(x), "parameter d of an outside path") would fix most of it.
