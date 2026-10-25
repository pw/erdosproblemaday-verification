# Blind consistency read — /day/138-openai-superexponential-van-der-waerden-refereed

Page read: /tmp/oaimath/160/entry/rendered_138.txt (HTML-unescaped; quotes below are verbatim from it, spacing artefacts of the
HTML strip included). Every artefact named below was read; nothing was run except read-only counts (python/grep/git log), no lean/lake.

## Own counts (not taken from the page)

| What | Count | Source |
|---|---|---|
| Referee reports | 7 (setup, counting, outer, dichotomy, perturbation, whole, sources) | seats/referee_*.md |
| Numbered objections | **45** = setup 9 · counting 6 · outer 4 · dichotomy 5 · perturbation 6 · whole 7 · sources 8 | objection headers in each report |
| …by severity | **36 COSMETIC**, 1 COSMETIC/UNCLEAR (sources S6), **5 UNCLEAR** (counting #6, outer O2, perturbation #4, whole #3, sources S7), **1 GAP in the EXPOSITION** (sources S2), 1 provenance note (counting #5), 1 correction to the brief (sources S8); 0 FATAL, 0 GAP in the proof | same |
| Modules / files / lines | 115 / 115 / 14,837 | modules.tsv (115 × `rc=0 errors=0 lines=0`), `ls`, `cat *.lean \| wc -l` |
| Build time | 430 s | steps.tsv `build 0 430` |
| References | 25 bib entries | refs/references.bib (`grep -c '^@'`) |
| Comments on erdosproblems.com/138 | 8; only one after 2 June (24 Aug 2026) | world/e138_thread_text.txt |
| Paper / CFS / companion pages | 25 / 5 / 198 | pdfinfo |
| "Theorem x.y" printed for a non-theorem | 34 single references + 1 range ("Theorems 5.2 to 5.4", paper.txt l.783) | grep of paper.txt |
| Separation pairs in the §6 seat's seven cyclic models | 13,845,248 (largest single model 5,762,400) | seats/perturbation_checks/out_cyclic.txt |
| Raw statement-match blocks | byte-identical; raw lengths 1,592 / 324 / 187 / 792 / 405 (the page's 1,238 / 304 / 187 / 664 / 355 are whitespace-collapsed) | logs/axioms.log vs logs/comparator.log, re-split with statement_match.py's head regex |

## Findings

1. **Title (and H1):** "and seven hostile seats read all 25 pages: no gap"
   - Artefact: seats/referee_sources.md §0: "One substantive exposition GAP in scope (S2)"; S2: "Severity: GAP in the EXPOSITION (an attribution/conditionality gap), not in the proof of Theorem 1.1". (Also referee_whole.md Objection 1: "COSMETIC (gap in EXPOSITION, not in the proof)".)
   - Severity: **OVERCLAIM** (a seat wrote GAP).
   - Replace with: "and seven hostile seats read all 25 pages: no gap in the proof of Theorem 1.1"

2. **Title (and H1):** "where the two-colour record was exponential since 1968"
   - Artefact: referee_sources.md citation table, Erdős–Rado 1952: "W(k,l) > (2lk^l)^{1/2}" (k classes, (l+1)-term APs) — at two colours (2l·2^l)^{1/2}, already exponential in 1952; Schmidt 1962 likewise (Berlekamp p. 409 quote in the same table). Nothing in the artefacts makes 1968 the start of exponential bounds; 1968 is only Berlekamp's prime-case construction.
   - Severity: **WRONG**.
   - Replace with: "where every earlier two-colour lower bound, from Erdős–Rado (1952) to Campos–Fox–Schildkraut (August 2026), was exponential"

3. **What the seats found:** "and every one returned HOLDS AS READ : no FATAL, no GAP in the proof of Theorem 1.1, some forty cosmetic notes"
   - Artefacts: my count above — 45 numbered objections, of which 36 COSMETIC, 5 UNCLEAR (referee_counting.md #6 "UNCLEAR-but-harmless"; referee_outer.md "O2 — UNCLEAR"; referee_perturbation.md "4. UNCLEAR"; referee_whole.md "Objection 3. UNCLEAR"; referee_sources.md S7 "Severity: UNCLEAR"), 1 GAP (S2), plus counting #5 "Provenance note" and S8 "correction to the BRIEF". The sources verdict is qualified: "HOLDS AS READ for every citation I could fetch". The page itself later says "Three findings are more than cosmetic", so calling everything cosmetic here is internally inconsistent.
   - Severity: **INCONSISTENT / OVERCLAIM**.
   - Replace with: "and every one returned HOLDS AS READ (the sources seat: "for every citation I could fetch"): no FATAL and no GAP in the proof of Theorem 1.1; 45 numbered objections — 36 cosmetic, six unclear (exposition or paper-vs-Lean correspondence), one exposition GAP outside Theorem 1.1's proof (the quasipolynomial aside below), a provenance note and one correction to our brief"

4. **What the seats found:** "a Behrend-type constant quoted from memory"
   - Artefact: no report contains such an objection (grep of all seven reports for "memory", "recall", "quoted" near Behrend/Rankin finds nothing). The only Behrend items are: sources S5 ("Theorem 7.2's uniformity in k is automatic; only the explicit constant is new" — COSMETIC novelty note) and the Behrend 1946 citation "COULD NOT FETCH … attribution only" (referee_perturbation.md citation table; referee_sources.md table rows [1]).
   - Severity: **UNSUPPORTED**.
   - Replace with: "an unverifiable theorem number (Szabó's "Theorem 2")" (sources S1) — or delete the item.

5. **What the seats found:** "read the paper's own LaTeX line by line, and every one returned"
   - Artefact: referee_sources.md §2 status table: "Lemma outer:lll: NOT READ (outer seat)", "Prop transfer:product and Thm transfer:large-r: NOT READ line by line (whole seat)", "Thm upper:finite: NOT READ", "Lemma count:arrangement itself: SKIMMED"; its scope was the citing sentences and the world.
   - Severity: **OVERCLAIM** (minor).
   - Replace with: "— the six mathematical seats read their sections of the paper's own LaTeX line by line, the sources seat every citing sentence against its source — and every one returned"

6. **What the seats found / world:** "The sources seat fetched or otherwise confirmed all 25 references (Szabó's "Theorem 2" label and Behrend's 1946 paper sat behind walls on every route and were confirmed through Green–Wolf, Kelley–Meka and the publisher abstracts) and found no mismatch"
   - Artefact: referee_sources.md S1: "the locator "Theorem 2" COULD NOT be verified"; table row [23]: "Content MATCH (abstract); theorem NUMBER "Theorem 2" COULD NOT VERIFY". §0: "COULD NOT CHECK at the primary source: Szabó 1990 …, Behrend 1946 …, Schmidt 1962, Shelah 1988, Rankin 1961 full text (verified via secondary sources / publisher synopsis / title)"; row [20] "Shelah by title + Gowers' account"; row "[1] Behrend (digits+sphere)": "not checkable here".
   - Severity: **WRONG** (Szabó's label was not confirmed) and **OVERCLAIM** (three further references were confirmed only secondarily or by title).
   - Replace with: "The sources seat checked all 25 references against Crossref/arXiv and found no mismatch; five could not be read at the primary source — Szabó 1990 (content matches the publisher abstract; the "Theorem 2" locator is unverified), Behrend 1946 and Rankin 1961 (confirmed through Green–Wolf, Kelley–Meka and the publisher synopsis), Schmidt 1962 (through Berlekamp) and Shelah 1988 (by title and Gowers's account)"

7. **Labels:** "seven hostile machine seats found no gap and quote nothing they could not check"
   - Artefact: referee_sources.md S2 "GAP in the EXPOSITION"; the seats mark unchecked material explicitly — referee_sources.md §0 "COULD NOT CHECK …"; referee_perturbation.md "Lemma 6.2 … (Lemma 3.1 imported, SKIMMED)"; referee_outer.md "Lemma 3.2 …, Lemma 3.4 (inputs) | SKIMMED".
   - Severity: **OVERCLAIM**.
   - Replace with: "seven hostile machine seats found no gap in the proof of Theorem 1.1 and mark what they could not check"

8. **More than cosmetic, First:** "the kernel certifies the theorem, the seats' hand reading certifies the paper's sharper lemmas, and they are two different arguments."
   - Artefact: referee_counting.md #5: "Lemma 3.1 as printed, and the exponents 2 (Lemma 3.2) and 6D (Lemma 3.4), are human-proof-only. My hand check and finite checks A–D support them."
   - Severity: **OVERCLAIM** ("certifies" where only a hand reading exists).
   - Replace with: "the kernel certifies the theorem; the paper's sharper lemmas rest only on the seats' hand reading and finite checks, and they are two different arguments."

9. **More than cosmetic, First:** "and the prime lemma is Mathlib's Bertrand — all weaker forms that still clear §4 and §6"
   - Artefact: referee_setup.md Objection 2: "The lemma is strictly weaker than Bertrand's postulate (which gives P ≤ 2k for k ≥ 1), and the Lean replaces this proof by Mathlib's Bertrand"; PrimeScale.lean l.32 `Nat.exists_prime_lt_and_le_two_mul`. Bertrand (P ≤ 2k) is stronger than the paper's P ≤ 2k², not a weaker form.
   - Severity: **WRONG**.
   - Replace with: "… the affine-signature count with exponent 8 for 3 — weaker forms that still clear §4 and §6 — while the prime lemma is replaced by Mathlib's Bertrand (P ≤ 2k, stronger than the paper's P ≤ 2k², by a different proof)"

10. **More than cosmetic, First:** "which is exactly what OpenAI's own scope note means by"
    - Artefact: world/openai_lean_docs_160.md says only: "The sharper intermediate estimates used in the paper are not part of the described formalization." Nothing saved says which estimates OpenAI meant.
    - Severity: **UNSUPPORTED** (attributes intent).
    - Replace with: "which is consistent with OpenAI's own scope note,"

11. **What the seats found (whole seat):** "kthRoot_tendsto at r = 2 is the problem page's sentence word for word"
    - Artefact: referee_whole.md §8: "Is `kthRoot_tendsto` erdosproblems.com/138's question at r = 2? Yes. … By monotonicity (`IsRamsey.mono`), "least N such that all N' ≥ N are Ramsey" equals "least N Ramsey", which is W 2 k." — an equivalence via monotonicity and the 0/1-based shift, not a verbatim match (the page defines W(k) by "whenever N ≥ W(k)", the Lean by an sInf over 0-based intervals).
    - Severity: **OVERCLAIM**.
    - Replace with: "kthRoot_tendsto at r = 2 is exactly the problem page's statement (up to the shift by one and monotonicity)"

12. **§3 seat:** "The §3 seat checked the arrangement lemma against Fourier–Motzkin, exact face enumeration and Zaslavsky's count on 690 random degenerate arrangements"
    - Artefact: seats/counting_checks/check_arrangement.out l.1: "random arrangements tested: 690  (FM oracle; e=2 also vs face-enumeration and Zaslavsky; e=1 vs 2r+1)".
    - Severity: **OVERCLAIM** (two of the three methods ran only on the e = 2 cases).
    - Replace with: "The §3 seat checked the arrangement lemma on 690 random degenerate arrangements by exact Fourier–Motzkin, the e = 2 cases also by face enumeration and Zaslavsky's count"

13. **§2 seat:** "The §2 seat built the adaptive mesh exactly as defined for every k ≤ 32 and in windows up to k = 10 12 : the width bounds hold with the measured constants 4, 4000 D +1 and ≈1 where the paper proves 49, 16004 D and ¼…2"
    - Artefact: referee_setup.md: checks run "every cell k=3..32"; Objection 7: "Lemma 2.4's "at most 49" has true maximum 4; Lemma 2.5's 16004D has true maximum 4000D+1 …; Lemma 2.3's [1/4, 2] has true range 1 ± O(H)". 49 is an endpoint count and 16004D a breakpoint count, not width bounds; k = 1, 2 were not built.
    - Severity: **INCONSISTENT** (mislabels two of three constants) / COSMETIC (k range).
    - Replace with: "The §2 seat built the adaptive mesh exactly as defined for every k from 3 to 32 and in windows up to k = 10^12: the paper's bounds hold with measured values 4 (mesh endpoints near a cell, Lemma 2.4), 4000D+1 (breakpoints on a 4H arc, Lemma 2.5) and ≈1 (width ratio, Lemma 2.3) where the paper proves 49, 16004D and ¼…2"

14. **§5 seat:** "(no dilation: 425 of 1528 progressions lose the affine lift"
    - Artefact: seats/dichotomy_checks/out_A_ctrl_lam1.txt: "progressions checked= 3000", "heavy case (< delta k light) checked= 1212", "SHORT-PERIOD CONCLUSION (ii) … checked= 1528 FAIL=425"; referee_dichotomy.md §6: checks are "per progression and per choice of heavy label. Every heavy label is tried". 1,528 > 1,212 heavy progressions, so the unit is (progression, heavy label) cases.
    - Severity: **WRONG** (unit).
    - Replace with: "(no dilation: 425 of 1,528 short-period (progression, heavy-label) cases lose the affine lift"

15. **§5 seat:** "then ran a toy cyclic model with the paper's formulas at k = 12, 100 and 1056 (52,388 block checks, no failure)"
    - Artefact: referee_dichotomy.md §6: "Only q is chosen freely: a prime > k, large enough that labels actually repeat"; table: "C | none | … longer: 52,388 block checks" — the 52,388 are model C (k = 1056) only; "In models A and B … the longer case is skipped".
    - Severity: **OVERCLAIM** (minor).
    - Replace with: "then ran a toy cyclic model with the paper's formulas (q chosen freely so that labels repeat) at k = 12, 100 and 1056 (52,388 long-period block checks at k = 1056; no failure in any base run)"

16. **§5 seat:** "Lemma 5.4 is essentially sharp (observed ratio 2.072 against the proof's 2)"
    - Artefact: dichotomy_checks/out_C.txt l.57: "min over heavy indices of (2M/k)|V|/|v_i| (lemma says >= 1): 2.072"; referee_dichotomy.md: "The lemma guarantees ≥ 1; the proof actually gives ≥ (2M/k)(m'−1) ≥ 66·32/1056 = 2." The stated lemma has a factor ≈2 slack; it is the proof's intermediate bound, at k = 1056, that is nearly attained.
    - Severity: **COSMETIC** (imprecise).
    - Replace with: "the proof of Lemma 5.4 is essentially sharp at k = 1056 (observed ratio 2.072 against the proof's floor of 2; the lemma as stated claims only 1)"

17. **§6 seat:** "(5.76 million pairs; a non-unit λ fails on 14,406)"
    - Artefact: perturbation_checks/out_cyclic.txt, the seven non-control models: 14,520 + 28,392 + 5,762,400 + 5,762,400 + 390,000 + 117,306 + 1,770,230 = 13,845,248 pairs; referee_perturbation.md: "in seven models (up to 5,762,400 pairs)". The control figure is right ("ctl_nonunit … failures=14406").
    - Severity: **INCONSISTENT** (a per-model maximum printed as the total).
    - Replace with: "(13.8 million pairs in all, up to 5.76 million in one model; a non-unit λ fails on 14,406)"

18. **§6 seat:** "and both union bounds below ½ at every k from 2 20 to 10 18 including every jump of D"
    - Artefact: perturbation_checks/out_thresholds.txt: "scanned 745 values of k in [2^20, 1e18]: max log R_k bound = -1241.4, max log A_k bound = -128365.3"; referee_perturbation.md: "over 745 scanned k ∈ [2^20, 10^18] incl. every D-jump".
    - Severity: **OVERCLAIM** (a 745-point scan, not every k).
    - Replace with: "and both union bounds below ½ at 745 scanned values of k from 2^20 to 10^18, every jump of D included"

19. **Architecture (§4):** "criterion 1/8 − 1/32 − 2/500 > 0 at l ≥ 100"
    - Artefact: 04-outer.tex l.175–176: "For the second inequality, the positive difference $1/8-1/32-2/500$ multiplied by $100$ exceeds $\log2$." Positivity alone is not the criterion; the page's own seats paragraph states it correctly ("(1/8 − 1/32 − 2/500)·100 = 359/40 with e^{359/40} > 2").
    - Severity: **WRONG / INCONSISTENT**.
    - Replace with: "criterion (1/8 − 1/32 − 2/500)·l ≥ log 2 for l ≥ 100"

20. **Architecture (§6):** "probability ≤ (1 − p ) k /4 = exp(− k 19/20 /4)"
    - Artefact: 06-perturbation.tex (perturb:affine-bound) l.266–271: "A_k ≤ 2T_aff(1−p)^{k/4} ≤ 2max{1,T_aff}exp(−pk/4) … using … $1-p\le e^{-p}$." (1 − p)^{k/4} is strictly less than exp(−pk/4), not equal.
    - Severity: **WRONG** (an equality where the paper has an inequality).
    - Replace with: "probability ≤ (1 − p)^{k/4} ≤ exp(−k^{19/20}/4)"

21. **Architecture:** "The exponent 10 −5 is where the two unions are made to clear"
    - Artefact: referee_whole.md §5: "The only inequality that caps c is the rich-case union bound … The affine case does not cap c"; referee_perturbation.md: "The only place `c` enters §6 is the rich union bound". The page's next clause ("2c must sit below γ/80") is the rich-case condition only.
    - Severity: **INCONSISTENT**.
    - Replace with: "The exponent 10^−5 is where the rich-case union is made to clear (the affine union clears for any fixed c)"

22. **Architecture (§3):** "the number of label words along a k -term progression is exp( O ( k 3/10 log k ))"
    - Artefact: 03-counting.tex Lemma count:global / referee_counting.md: "T_glob counts full-label words of all progressions" (one word per progression; the bound is on how many distinct words all progressions realize).
    - Severity: **COSMETIC** (misdescribes the counted object).
    - Replace with: "the number of distinct label words realized by k-term progressions is exp(O(k^{3/10} log k))"

23. **The Lean:** "The definitions are four lines ( Model.lean )"
    - Artefact: lean/OAI/Combinatorics/ProgressionColoring/Model.lean: `MonoAP`, `HasMonoAP`, `IsRamsey`, `W` — four definitions of two lines each (plus a docstring on `W`).
    - Severity: **WRONG** (minor).
    - Replace with: "The definitions are four short ones (Model.lean)"

24. **The replay:** "Under --trust=0 the kernel reports that"
    - Artefact: probe/Axioms138.lean is `import …Main` + `#print axioms …`; logs/axioms.log is that command's output. `#print axioms` is a traversal of the compiled declarations, and a file that only imports and prints re-checks nothing already compiled — the re-check of the whole closure is the separate `leanchecker --fresh` step (build.sh; driver.log "BEGIN leanchecker_fresh", log still empty). The declarations were kernel-checked when each module compiled (modules.tsv), but the axiom list is not a kernel report.
    - Severity: **OVERCLAIM** (minor, technical).
    - Replace with: "`#print axioms` (in a probe run with --trust=0 over the compiled modules) reports that"

25. **The replay:** "1,238, 304, 187, 664 and 355 characters"
    - Artefact: statement_match.py: blocks are compared after `re.sub(r"\s+"," ",seg)`; the raw blocks in logs/axioms.log and logs/comparator.log are byte-identical (my re-split) at 1,592 / 324 / 187 / 792 / 405 characters.
    - Severity: **COSMETIC** (the byte-identity claim holds; the lengths are of whitespace-collapsed text).
    - Replace with: "1,238, 304, 187, 664 and 355 characters with whitespace collapsed"

26. **The replay:** "The estimate was written before the first core was spent."
    - Artefact: ESTIMATE.md itself: "cache get relaunched 06:08:42Z" and header "06:1xZ"; logs/cache_get.log: "Decompressed 8907 already-cached file(s) … Completed successfully in 49415 ms!" (file mtime 06:10:09). Mathlib's cache had already been fetched and decompressed when the estimate was written; what it preceded was the build (driver_attempt1 06:15:51, "build launched 2026-10-15T06:15:53Z").
    - Severity: **UNSUPPORTED** (minor).
    - Replace with: "The estimate was written before the build started."

27. **The replay:** "every step waiting for 28 GB of free memory"
    - Artefact: build.sh: `waitmem 28` before `smoke`, before each module in the build loop, before `axioms`, and before `leanchecker_fresh`; `comparator_module`, `comparator`, `rightshape`, `wrongshape`, `negcontrol` have no wait of their own.
    - Severity: **COSMETIC / OVERCLAIM**.
    - Replace with: "every module build waiting for 28 GB of free memory"

28. **The world:** "— the file we replayed, at the commit it links —"
    - Artefact: world/formal_conjectures_138.lean links `openai/math/blob/adc7f1241b…/ProgressionColoring/Main.lean#L12`; driver.log: "openai/math rev: 1581d4cbdd69…" (the page's own replay paragraph says 1581d4c). `git log` shows the ProgressionColoring path touched only by adc7f12, so the file is identical, but it was not replayed at that commit.
    - Severity: **INCONSISTENT** (minor).
    - Replace with: "— the file we replayed (at 1581d4c, unchanged since the commit adc7f124 that it links) —"

29. **The world:** "Its priority search (arXiv, the forum, Bloom's blog, MathOverflow, GitHub; X, Reddit and Zulip were blocked)"
    - Artefact: referee_sources.md §5.3: coverage = "23 web queries …, the arXiv API queries above, HN, MathOverflow, erdosproblems.com. Not covered: X, Reddit, Zulip, Google Scholar, non-English venues"; "the Lean Zulip live API (401; public archive ends 28 Feb 2026)". GitHub was searched for rebuilds and follow-ups (§5.4–5.5), not listed for priority; Hacker News and the web queries are omitted on the page.
    - Severity: **INCONSISTENT** (minor).
    - Replace with: "Its priority search (23 web queries, arXiv, Hacker News, MathOverflow, erdosproblems.com, Bloom's blog; X, Reddit, the live Zulip, Google Scholar and non-English venues not covered)"

30. **The world:** "so the claim is first, and positive"
    - Artefact: referee_sources.md §5.3: "This is a COVERAGE claim"; §0: "no human-authored claim … (a coverage claim; queries listed in §5.3)".
    - Severity: **OVERCLAIM** (absence stated as fact).
    - Replace with: "so, as far as that search reaches, the claim is first, and positive"

31. **The world:** "puts the threshold K 0 beyond 10 41"
    - Artefact: referee_outer.md O4: "So the proof's K_0 is at least of order 10^41 from §4 alone." A threshold for the proof's route, not the least valid K_0.
    - Severity: **OVERCLAIM** (minor).
    - Replace with: "puts the proof's threshold K_0 beyond 10^41"

32. **The problem:** "The two-colour case — the case Erdős priced — is open on the page."
    - Artefact: referee_sources.md §5.1: "No status word on the page: the problem box carries `id=neutral`, which is the site-wide policy announced 6 Oct"; world/e138_text.txt shows no status, only remarks that do not mention a two-colour resolution.
    - Severity: **UNSUPPORTED** (the page shows no status at all).
    - Replace with: "The two-colour case — the case Erdős priced — is unresolved in the page's text (the site has displayed no statuses since 6 October)."

33. **The problem:** "and the Erdős–Graham books"
    - Artefact: world/e138_text.txt lists only the tags "[ErGr79]" and "[ErGr80]"; nothing saved identifies them, and nothing establishes that both are books.
    - Severity: **UNSUPPORTED** (cosmetic).
    - Replace with: "and Erdős–Graham 1979 and 1980"

34. **The world:** "Bloom's post lists #138 with the rest and reads none of them."
    - Artefact: world/bloom_blog10_text.txt l.34: "I have not yet looked at in any serious way any of the proofs in this release"; his #138 entry nonetheless remarks "It appears to use similar methods to [FoHu26]".
    - Severity: **OVERCLAIM** (minor paraphrase).
    - Replace with: "Bloom's post lists #138 with the rest and says he has not yet looked at any of them in any serious way."

35. **The claim:** ""including the two-color case""
    - Artefact: the phrase is in the abstract (build/paper.tex l.12–13: "giving a quantitative positive resolution of Erdős's superexponential-growth question, including the two-color case."), not in Theorem 1.1 or the sentence after it (01-introduction.tex l.28–33).
    - Severity: **COSMETIC** (attribution).
    - Replace with: "hence W_r(k)^{1/k} → ∞ for each fixed r ≥ 2 — in the abstract's words, "including the two-color case"."

36. **What the seats found:** "the compiled PDF prints 34 cross-references to lemmas, definitions and the proposition as "Theorem""
    - Artefact: paper.txt: 34 single "Theorem x.y" with x.y ∈ {2.1–2.5, 3.1–3.4, 4.1, 4.2, 5.1–5.3, 6.1, 6.2} (my count matches referee_setup.md Obj. 1 and referee_whole.md Obj. 2), plus one range at l.783: "Theorems 5.2 to 5.4" (Lemmas).
    - Severity: **COSMETIC**.
    - Replace with: "the compiled PDF prints 34 cross-references (and one range, "Theorems 5.2 to 5.4") to lemmas, definitions and the proposition as "Theorem""

## Checked and found consistent (no change needed)

115 modules / 115 files / 14,837 lines; imports only Mathlib + `Lean.Elab.Tactic.Omega`; ProgressionColoring and the preprint touched only by
adc7f12 (6 Oct); Mathlib pin d13f23b7 and toolchain v4.34.1 (lakefile.lean, lean-toolchain); build 430 s, 0 errors; six declarations on
{propext, Classical.choice, Quot.sound}; comparator with sorryAx; statement_match v1 MISMATCH / v2 MATCH and the stated causes (statement_match.py
header); RightShape v1 failure on `simpa` (logs/rightshape_v1.log) and v2 pass; WrongShape type mismatch; NegControl `[sorryAx]`; leanchecker
started 06:26:51Z and unfinished. Theorem 1.1, Theorem 7.2, the boundary values, c = 10^−5, parameters, γ/80 arithmetic (−21/200000).
Comparator JSON fields, docs/160.md quotes, formalization.yaml entry. Seat figures: 226 LLL instances, tail ratio 0.567, 359/40, log T_glob ≤
√k/320 and exp(D²/65), fourteen §5 inequalities, k ≥ 1056, 2M/k ≤ 1/16, cut failures on ~nine tenths (615/682, 625/682), 48,910 identity
instances, multiplicity 2 not 4, c < 1/16000, C = 1322, 335 → 557 → 889 vs 3, ℤ/3, ℤ/4, ℤ/11, ten r values, sweep to 2·10⁶, ≈30 thresholds,
D ≥ 29,210 / 10^44.7, three threshold estimates 10^41.4–10^44.7, the Lean weaker forms ((e+2)²(s+1)^{2(e+1)}, 16(·)⁶, (16005Dh)^{14D},
exponent 8), the companion's 198 pages and its scope note, Kelley–Meka k = 3. World: 8 comments, one after 2 June (24 Aug, CFS), CFS 5 pages
and abstract, proof claims 0, comments frozen, teorth open 2025-08-31, Bloom's 25 and 12, FC commit 3dfd999d on 11 Oct with `sorry`, the FC
docstring quote, DeepMind April and Atlas variants, mathvet 8 Oct and nealmcb 11 Oct, first public 6 Oct, FH and CFS calling it open, S8 as
the brief's only flagged error.
