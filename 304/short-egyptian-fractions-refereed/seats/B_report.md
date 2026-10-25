# Seat B: blind consistency read of the #304/#148/#293 entry (family 25), pre-publication

Read: `/tmp/oaimath/025/entry/entry_rendered_preblind.txt`, plus the summary/READSUMMARY/LEANLABEL/HEADLINE strings in
`entry_draft.js` and `mkvalues.py`. The renderer that made the preblind text dropped the whole summary: the `<` in "1 ≤ a < b"
opened a fake tag. The site escapes `summary` (`index.js:11273`, `escapeHtml`), so production should be fine, but nobody has
read the rendered summary. I read it from the JS source. The coordinator added the "Sources and the world" paragraph
(`world_rendered.txt`); its items are W1–W10 at the end.

Evidence I checked myself: tex + `paper.txt` (printed numbers), BvD text, the live pages (p/t/c 304, 148, 293, c18), the
U/P/L/W reports, every replay log named in the brief, both bridges and their mutants, the FC copies, the Lean sources, our
empirical logs and scripts, and `ledger_data.js`. Things that check out (abridged):
- 15 min 55 s (18:08:35→18:24:30Z); 348/348 rc=0; peak `maxrss_kb` 7,020,264 (6.70 GiB); 8,140 and 36,061 lines.
- 24/24 pp.all blocks; sorryAx on the comparators; 233/57 from `deps_summary.txt`.
- `upperConstant` at `UpperAssembly.lean:52` ≈ 1.2254·10¹⁰ (recomputed from `dimX`, `terminalConstant`, `greedyConstant`); c₁ = 1/2.
- Both docstring quotes are verbatim.
- All printed lemma and equation numbers are right; 257/log 2 = 370.77.
- PDF md5 = openai/math `adc7f124` (2026-10-06); 33 pages; family 025 in `CONTENTS.md`.
- July ledger: N(b) ≤ 7 for b ≤ 1000, 733…907, 2307 ≤ v(8) ≤ 27539.
- Empirical logs (F, |D_k|, v, s_k − 1, N(b) list, 11/17/79, 11/17/103/733).
- FC verbatim check and its two mutations.
- The 681943 arithmetic: the PR tuple's deficit is exactly 131225/8053056, and the forum tuple sums to exactly 1.

---

## Main body

1. **MUST-FIX.** "Taken literally that is 1 for every k ≥ 2, and the page reads it, after a December 2025 comment on its thread, as the least such integer above 1."
   - **Wrong:** the page does not read it that way. The fetched #293 statement still says "the minimal integer which does not appear as some n_i", with no "> 1". The page also carries "The original source is ambiguous as to what the problem is — please add a comment".
   - Woett's 8 Dec 2025 comment ("smallest integer larger than 1 … (The site has been updated to address this comment.)") changed the commentary (e.g. v(k) ≤ kF(k)+2), not the statement.
   - The sentence also contradicts the new world paragraph ("the site's wording drops … '> 1'"), and W_report §3 says "The site text is still unfixed".
   - Evidence: `live/p293.html.txt`; `grep 'minimal integer' p293.html`; `t293.txt` (Woett, 22:34 on 08 Dec 2025).
   - **Replace:** "Taken literally that is 1 for every k ≥ 2. Erdős and Graham's own wording is 'the least integer v(n) > 1' (p. 35), and a December 2025 comment on the thread says that is what is meant, but the page's statement still omits '> 1' and is flagged as ambiguous."

2. **MUST-FIX.** "The Lean proves its own versions of what the paper cites, including a three-primes theorem, so the formal statements depend on nothing beyond Mathlib."
   - **False, and it contradicts the §8.1 paragraph** of this same page. The Lean proves no three-primes theorem. Its major-arc main term is only a hypothesis ("no Vinogradov theorem is asserted"), and every three-primes module is unused. Prop 8.1 is proved by the composite cube-free route instead.
   - What the Lean does replace with its own proofs: the Erdős–Turán inequality (a finite cyclic discrepancy lemma) and the PNT (Chebyshev bounds).
   - Evidence: `ThreePrimeSingularSeries.lean:103`; `logs/deps_summary.txt`; L_report §2 "Three-prime material" and §3 items 4–5.
   - **Replace:** "Where the paper cites an outside result, the Lean either proves its own version (the Erdős–Turán inequality as a finite cyclic discrepancy lemma, the prime number theorem as Chebyshev bounds) or avoids it (the three-primes theorem, see above), so the formal statements depend on nothing beyond Mathlib."

3. **MUST-FIX.** "In our labels, the paper's proof is (b), rigorous modulo the cited prime-number-theorem estimates."
   - **Incomplete label.** The paper's text also rests, without proof, on the Erdős–Turán inequality (4.8) in Lemma 4.2, cited as [9, Part I Thm III]. For the explicit slope it rests on Vinogradov's quantitative three-primes theorem (Lemma 8.2). Neither is a PNT estimate.
   - Evidence: `residues.tex` ("We use the Erdős–Turán discrepancy inequality …"); `prescribed.tex` ("We use the quantitative form of Vinogradov's three-prime theorem …"); U_report §6; W_report table.
   - **Replace:** "In our labels, the paper's proof is (b): rigorous modulo the prime number theorem, the Erdős–Turán discrepancy inequality and, for the explicit slope log 2/257 only, Vinogradov's three-primes theorem."

4. **MUST-FIX.** "The one place where the Lean leaves the paper is §8.1."
   - **False.** Seat L lists further departures:
     - Lemma 4.2's Erdős–Turán input is replaced by a self-contained cyclic discrepancy lemma in both developments.
     - PNT is replaced by Chebyshev or central-binomial bounds.
     - Lemma 6.1 is proved in a different, exact-length form (`marked_cleanup_exact_length`).
     - Lemma 3.1 is proved for real r ≥ 0 in EgyptianFractions.
     - c₁ = 1/2.
   - Evidence: L_report §3 items 1, 3, 4, 5, 6.
   - **Replace:** "The one place where the Lean takes a different mathematical route is §8.1. Elsewhere it follows the paper and swaps cited inputs for self-contained ones (a finite discrepancy lemma for Erdős–Turán, Chebyshev bounds for the PNT)."

5. **MUST-FIX.** Two sentences with the same error:
   - "… but not the paper's own §8.1 argument, which rests on Kumchev's three-primes count …"
   - "It read Kumchev's 1997 three-primes count …"

   **Wrong attribution.** The asymptotic is Vinogradov's 1937 theorem (Hardy–Littlewood singular series). Kumchev 1997 is a paper on Piatetski-Shapiro primes that restates it as displays (1)–(2) in its introduction. The paper itself says "the quantitative form of Vinogradov's three-prime theorem … see the statement in [15, (1)–(2)]".
   - Evidence: `P_dl/…jtnb.186.pdf.txt` ("In 1937 I. M. Vinogradov [15] solved the Goldbach ternary problem. He proved that …"); `prescribed.tex`.
   - **Replace:** "… which rests on Vinogradov's quantitative three-primes theorem (in the form stated in Kumchev 1997, (1)–(2))". And: "It read the statement of Vinogradov's three-primes asymptotic in Kumchev 1997, (1)–(2), and Glibichuk and Konyagin's bilinear bound …"

6. **MUST-FIX.** "FC's #148 is still a research-open value question (…), so there is no FC statement to prove verbatim."
   - **False.** FC_148 also has `erdos_148.variants.lower_bound`, tagged research solved and still `sorry`. It states exp(exp((log 2·log 3/3 + o(1))·k/log k)) ≤ F k (Konyagin's form). That follows at once from Corollary 1.2: take o := 0, since c′k/log k ≤ ck eventually. Seat L said so.
   - Evidence: `bridge/FC_148.lean` lines 190–193; L_report §4b ("FC's `erdos_148.variants.lower_bound` … follows from the OpenAI lower bound with o := 0").
   - **Replace:** "FC's headline `erdos_148` is a research-open value question (…, answer sorried), which log log F ≍ k does not settle. FC's `erdos_148.variants.lower_bound` (Konyagin's form) does follow from Corollary 1.2, but we have not bridged it." Alternatively, bridge it, which is a few lines on top of `F_eq_oai`.

7. **MUST-FIX.** "Every junk-value trap is closed by a proved conjunct, among them sInf of an empty set, the if inside Finset.sup, ncard, log log of small arguments and the real liminf of a sequence that might be unbounded."
   - **Misreports seat L.** L says each trap "is either excluded by a proved conjunct or can only make the statement false, never vacuous".
   - The `if` inside `Finset.sup` is harmless by construction (the a = 0 term contributes 0). log log of small arguments is irrelevant because b₀ is existential. Neither is closed by a conjunct.
   - Evidence: L_report §0 L1 and §1a–1b.
   - **Replace:** "Every junk-value trap is either closed by a proved conjunct (sInf of an empty set, ncard of an infinite set, the real liminf/limsup) or harmless by construction (the `if` inside `Finset.sup`, log log at small arguments)."

8. **MUST-FIX.** Seat counts disagree across the page.
   - Summary (READSUMMARY): "Three hostile AI seats (the upper bound in §§2–5, the corollaries in §§6–8, and the Lean against the paper and the problems) found no gap."
   - Body: "Three hostile seats with tools and one Lean seat, all Claude Opus 5.5 …"
   - The summary counts L as one of the three hostile seats. The body counts three hostile seats plus L. The world paragraph adds seat W, and the body never names the third hostile seat.
   - Evidence: `mkvalues.py` READSUMMARY; `seats/` has U, P, L, W reports; `receipts.sh` lists U, P, L, W, B.
   - **Replace** (both places): "Four AI seats, all Claude Opus 5.5: three hostile referees with tools (U: §§2–5; P: §§6–8; W: sources and the world) and one Lean seat (L) …". Also put the same count in the summary.

9. **MUST-FIX.** "… per-seat counts, and a zero count of any other model, are in the bundle's seats/MODEL_RECEIPTS.txt."
   - **The file does not exist.** The bundle `seats/` has `receipts.sh` but no `MODEL_RECEIPTS.txt`. The "zero count of any other model" is therefore unverified.
   - The script reads transcripts under `/tmp/claude-1000/…`, which do not persist. Run it before publishing and bank the output.
   - Evidence: `ls ~/ErdosProblemADay-main/verification/304/short-egyptian-fractions-refereed/seats`.
   - **Fix:** generate the file (after the last seat, including this one, is done), check it says what the sentence says, then publish.

10. **MUST-FIX.** "So the bound n_k ≤ s_k − 1 that Quanyu Tang gives on the #293 thread is sharp in that range."
    - **Attribution.** The bound is classical: Curtiss 1922, Kellogg's problem; Soundararajan for the underapproximation. Tang's comment itself says "It is well known that Sylvester's sequence gives the best n-term Egyptian underapproximation of 1".
    - **Sharpness.** "Sharp in that range" understates it. The Sylvester expansion attains the bound by an identity for every k ≠ 2, so our computation is a consistency check, not evidence.
    - Evidence: `live/t293.txt` (Tang, 16:53 on 08 Dec 2025); BvD ref [7] (Curtiss 1922).
    - **Replace:** "This is the classical bound n_k ≤ s_k − 1 (Curtiss 1922; recalled by Quanyu Tang on the #293 thread), which the Sylvester expansion attains for every k ≠ 2; our search simply agrees with it."

11. **MUST-FIX** (headline string in `mkvalues.py`, published on the homepage). "OURS: KERNEL-CHECKED BRIDGES TO FORMAL CONJECTURES' #304 AND #148, …"
    - **Overstates #148.** For #148 we proved no FC statement. We proved that FC's `F` equals OpenAI's `F`, plus a statement of our own.
    - Evidence: `Bridge148_293.lean` docstring ("`erdos_148.variants.double_log_order` below is OUR statement").
    - **Replace:** "OURS: KERNEL-CHECKED BRIDGES TO FORMAL CONJECTURES' #304 STATEMENTS AND TO FC'S #148 COUNTING FUNCTION, A FORMAL STATEMENT FOR #293, …"

12. **OPTIONAL.** "The descent runs through levels X_j = X·e^{−10⁻⁴mj}, at most 3D_X·10⁴·log S of them (about 6·10⁹·log S with the paper's constants)."
    - That number is the bound K_d·log S. The actual depth is d = ⌈(D_X S − m)/(ηm)⌉ ≈ D_X·10⁴·log S ≈ 2.0·10⁹·log S, so "about" overstates the count threefold. The levels are j = 0…d, i.e. d+1 of them.
    - **Replace:** "… d ≈ D_X·10⁴·log S ≈ 2·10⁹·log S of them (the paper bounds d by 3D_X·10⁴·log S)".

13. **OPTIONAL.** "The danger is that h lands on an earlier failure."
    - Ambiguous: "earlier" reads as a higher level. The risk is H_{j+1}, the failure set one level down, which is built first because the sets are constructed from the bottom up.
    - **Replace:** "The danger is that h lands in the failure set of the next level down."

14. **OPTIONAL.** "Section 2 reduces everything to one proposition."
    - It reduces the upper bound of Theorem 1.1, not the corollaries. **Replace:** "Section 2 reduces the upper bound to one proposition."

15. **OPTIONAL.** "For #148 (Section 6), apply the theorem to (Q−1)/Q …, append 1/Q, and split the denominator n that Q divides …"
    - This skips Lemma 6.1. Appending 1/Q can duplicate a denominator, and the cleanup that removes repetitions at total one while keeping a multiple of odd Q is what produces n (a multiple of Q, not Q itself).
    - **Insert:** "… append 1/Q, remove repetitions while keeping a multiple n of Q (Lemma 6.1), and split n as …".

16. **OPTIONAL.** "§8 uses nothing from §§3–5, so Corollary 1.3, the lower bound of Corollary 1.2 (through v(k) ≤ kF(k) + 2) and Theorem 1.1 itself all survive any defect there; Bloom and van Doorn make the same observation."
    - For Theorem 1.1 this needs §8's machinery restarted at q₀ = b. That adaptation is in P's O1 and in BvD's Theorem 1, not in the paper's text.
    - **Replace the end:** "… and, by the adaptation Bloom and van Doorn write out (restart §8's greedy at b), Theorem 1.1's upper bound as well."

17. **OPTIONAL.** "It ran the reduction identity on 200,000 random inputs in exact rational arithmetic, alongside two negative controls."
    - U's two negative controls were for (3.3) and for Lemma 2.3's step bound, not for the identity. **Replace:** "…; two other checks, of (3.3) and of Lemma 2.3's step bound, carried negative controls that do fail."

18. **OPTIONAL.** "(3.7) reuses the symbol C_r for a different exponent."
    - In (3.5), C_r is a multiplier. In (3.7) it is used as an exponent, and the proof actually gives e·C_r (U_report). **Replace:** "(3.7) uses C_r, the multiplier of (3.5), as an exponent (the proof gives e·C_r)."

19. **OPTIONAL.** "All ten theorems depend on exactly the standard axioms …, checked with --trust=0."
    - `--trust=0` on a probe that only imports compiled `.olean`s re-checks nothing. The axiom lists come from `#print axioms`. The from-scratch re-check is `leanchecker --fresh`, still running.
    - Evidence: `post.sh` (`lean --trust=0 … AxSE.lean`); `probe/AxSE.lean`.
    - **Replace:** "… as reported by `#print axioms` on the replayed environment."

20. **OPTIONAL.** "… asking exact_marker_padding to pad a length-2 expansion, when it requires length at least 3, fails to elaborate."
    - The probe supplies no expansion. It passes r = 2 with `le_refl 2 : 2 ≤ 2` where `3 ≤ 2` is required (`probe/TypeCtl.lean`). **Replace:** "… and feeding `exact_marker_padding` the length r = 2, below its hypothesis r ≥ 3, fails to elaborate."

21. **OPTIONAL.** "…, with a peak of 6.7 GiB."
    - That is the peak RSS of a single `lean` process (7,020,264 kB in `modules.tsv`), with four running at once. **Replace:** "peak 6.7 GiB per process".

22. **OPTIONAL.** "Four mutants must fail, and do: FC's definition with n > 0, which admits 1/1; …"
    - With n > 0, FC's `upper_bound` and `lower_1950` stay true, because 1/1 cannot occur in an expansion of a/b < 1. That mutant fails only because the bridge lemma is stated for every a, b, and is false at a = b.
    - All four fail at the first tactic that meets the changed token (omega / rewrite / type mismatch, see the `*.log`s). They show the proofs are not insensitive to those tokens. They do not show the mutated statements are false.
    - **Replace:** "Four mutated copies make the unchanged proofs fail: FC's definition with n > 0 (which breaks the for-all-a,b bridge lemma at a = b); upper_bound with log log log b; F with 1 ∉ S; and log log v(k) ≍ k²."

23. **OPTIONAL.** "All eight bridge theorems depend on exactly the standard axioms."
    - The two files contain 13 theorems and lemmas. `AxBridge.lean` prints eight. **Replace:** "The eight headline bridge theorems (and so every lemma they use) depend …"

24. **OPTIONAL.** "This proves FC's statements in OpenAI's environment (Lean 4.34.1, Mathlib d13f23b7), not FC's own constants."
    - "constants" is opaque. **Replace:** "… not in FC's repository: our copies are fresh declarations compiled against OpenAI's Mathlib pin, not FC's Mathlib or `FormalConjecturesUtil`."

25. **OPTIONAL.** "… derives verbatim copies of upper_bound and of erdos_304.variants.lower_1950, Erdős's lower bound, which FC lists separately."
    - FC already links a third-party formal proof for `lower_1950` (`thepriceisright/publications …/Lower1950.lean`). Say so, so it does not read as a first.

26. **OPTIONAL.** "Route A gives F(7) = 245,765, |D7| = 83,231 and v(7) = 733. Seat P's enumeration, a third program, agrees through k = 7, …"
    - P's program (`egy_enum.py`) uses the same divisors-of-q² two-term tail as route A, so it is not decorrelated. P reports F and v, not |D_7|. So |D_7| = 83,231 rests on route A alone, and route B ran only to k ≤ 6.
    - **Replace:** "Seat P's enumeration (same two-term method) agrees on F(7) and v(7) …"

27. **OPTIONAL.** "Every expansion satisfies the Lean's bounds n_i ≤ k^{2^{i−1}}, F(k) ≤ k^{2^k−1} and v(k) ≤ 1 + k^{2^{k−1}}."
    - Add "for k ≤ 7". Also, F(k) and v(k) are not properties of an expansion. **Replace:** "For k ≤ 7 every expansion satisfies n_i ≤ k^{2^{i−1}}, and F(k) ≤ k^{2^k−1}, v(k) ≤ 1 + k^{2^{k−1}} (the bounds the paper and the Lean prove)."

28. **OPTIONAL.** "An exact search gives N(b) for b ≤ 60 … The first b with N(b) = 4, 5 and 6 is 11, 17 and 79."
    - 79 > 60. That value came from a separate search to b ≤ 110 (`nab2.py`). **Add:** "(a search to b ≤ 110; N(b) = 7 first occurs at 733, from our July search)".

29. **OPTIONAL.** "… and the Elsholtz–Planitzer upper bound F(k) ≤ c0^{(1/5+o(1))2^k} [ElPl21]."
    - The page gives c₀ = 1.26408 (Vardi). Elsholtz–Planitzer's Remark 3 constant is 1.5979 = Vardi², per W_report and FC_148's own docstring. As the page writes it, the bound appears to be stronger than the published one.
    - Either say "the page gives (with c₀ the Vardi constant)" and add "(Elsholtz–Planitzer's own constant is its square)", or drop the constant.

30. **OPTIONAL.** Three places present √log b and exp(ck²) as the prior state:
    - "The new content is the uniform upper bound for N(b), the lower bound log log F(k) ≫ k, which improves Konyagin's k/log k, and the lower bound for v(k), which improves van Doorn and Tang's exp(ck²)."
    - the summary's "Vose improved the upper bound to √(log b) in 1985";
    - the headline's "(VOSE 1985: √log b)".

    As the world paragraph now says, the best bounds before the paper were van Doorn–GPT-6 Astra Pro's (16 Sep): N(b) ≤ 2c₀(log log b)² and v(k) ≥ exp(exp(√(k/(2c₀)))). Align "The claim" with them: "… the lower bound for v(k), which improves van Doorn and Tang's exp(ck²) and van Doorn–GPT-6 Astra Pro's exp(exp(√(k/(2c₀)))) (16 Sep)."

31. **OPTIONAL.** "They include every three-primes, Vaughan and arc module."
    - `PrimeTripleAsymptotics` is in the used set (`deps.log:425`, used by `quantitative_marked_length`). Its docstring says it is "purely an asymptotic comparison, not a three-prime theorem". A reader grepping `deps.log` will find it. The deps filter was by name (ThreePrime*/Vaughan*/MinorArc*/MajorArc*/Mangoldt*).
    - **Add:** "(the one used module with 'PrimeTriple' in its name, `PrimeTripleAsymptotics`, only compares growth rates)".

32. **OPTIONAL** (LEANLABEL in `mkvalues.py`). "… (those 57 modules are imported but unused)."
    - Not all 57 unused modules are three-primes ones (e.g. `CountingFromMarkers`, `MarkedGroupingFin`, `FejerExponentialBudget`). **Replace:** "(its three-primes modules are among 57 that are imported but unused)".

33. **OPTIONAL.** "… OAI/NumberTheory/EgyptianFractions (290 modules) …" (link label).
    - The directory holds 366 files; 290 is the import closure of `Main`, and 76 more are not imported (L_report §2). **Replace:** "(290-module closure of Main)".

34. **OPTIONAL.** "… proves nine statements in the namespace OAI.Problem337 …"
    - Add "(OpenAI's internal label, unrelated to Erdős #337)". L flags this as a naming hazard.

35. **OPTIONAL.** "… against FC's text at commit 2a315101 (21 October) …" and the link label "at commit 2a315101 (21 Oct 2026)".
    - `FC_SHA.txt` records that 2a315101 was `refs/heads/main` when fetched. 21 Oct is the fetch date, not necessarily the commit date. **Replace:** "(FC main as fetched 21 October)".

36. **OPTIONAL.** "Ours: the replay and its controls, the three bridges and their controls, the readings, and the small-case computations."
    - The headline and README also claim the kernel dependency walk, which is the page's main new finding about the Lean. Add it.

37. **OPTIONAL** (READSUMMARY). "… write that they had not read §§3–5 in detail".
    - BvD's words are "have not yet read those sections in detail". Keep "yet".

38. **OPTIONAL.** "Its one caveat, on §8.1, is the dependency finding above, which our walk over the kernel terms confirmed."
    - L's import-closure argument gave 234 used / 56 unused. The kernel walk gives 233 / 57. **Replace:** "… confirmed (one module finer)".

39. **OPTIONAL** (link). "Thomas Bloom, Erdős problems in the OpenAI proofs (8 Oct 2026)".
    - There is no local copy of this page in the bundle. Fetch it and check the title and date before publishing.

## Sources and the world (W items)

W1. **MUST-FIX.** "Its history skips two public intermediate results. Liam Price's 24 July proof claim on #18 gives h(n) ≪ (log log n)² for infinitely many practical n. … Both are strictly weaker than the paper's theorems, so this is a gap in its exposition, not a priority question."
- Price's item is an unverified proof claim on #18. It concerns h(n) for practical numbers, which the paper never addresses, so "strictly weaker than the paper's theorems" does not apply to it.
- It is not itself a result on #304/#148/#293. Van Doorn's note says ChatGPT had to "slightly amend the proof … so that it can again be used to obtain analogous bounds on N(b) and v(k)". Woett's claim summary says the same.
- "gives" also asserts correctness, which the site disclaims ("Appearing on this page is no guarantee of proof correctness").
- Evidence: `live/c18.html.txt`; `seats/W_src/vdgpt.tex` line 85.
- **Replace:** "Its history skips one public intermediate result, which grew out of Liam Price's 24 July proof claim on #18 (h(n) ≪ (log log n)² for infinitely many practical n). Van Doorn and GPT-6 Astra Pro amended that argument … and posted 'Practical numbers and Egyptian fractions' on 16 September … with N(b) ≤ 2c₀(log log b)² and v(k) ≥ …. That result is strictly weaker than the paper's theorems, so this is a gap in its exposition, not a priority question."

W2. **OPTIONAL.** "… which makes the literal reading v(k) = 1." For k = 1 the literal value is 2, since 1 = 1/1. **Replace:** "v(k) = 1 for every k ≥ 2". This also matches the body.

W3. **OPTIONAL.** "… and the other natural readings (length at most k; repetitions allowed) get the same order."
- This is seat W's own short argument, not the paper's. Say so and give the one-line reasons:
  - lengths at most k: D₁ = D₂ = ∅ and D_k ⊆ D_{k+1}, so nothing changes;
  - repetitions allowed: D_k ⊆ D′_k gives the lower bound, and n_i ≤ k^{2^{i−1}} also holds for nondecreasing tuples.

W4. **OPTIONAL.** "… so §§3–5 have, as far as we know, no human reading; they rely on the Lean, as this page does for every step it checks only by machine."
- The antecedent of "they" is unclear (BvD, or §§3–5?). BvD do not say they rely on the Lean for §§3–5; they say the proofs "were formalised in Lean, and hence one can verify their correctness mechanically".
- The sentence also omits that this page's seat U, an AI, read §§3–5 line by line.
- **Replace:** "… so §§3–5 have, as far as we know, no human reading: apart from our AI seat U, their check is the Lean, as it is for every step this page checks only by machine."

W5. **OPTIONAL.** "The community database (teorth/erdosproblems at 302a00e) still lists all three as open, last updated 31 August 2025."
- 31 August 2025 is the date in the `status` field. The #293 record also carries `comments: "ambiguous statement"`, added 2026-08-28 per W_report.
- The hash 302a00e appears nowhere in W_report or W_src (`problems.yaml` is banked without it).
- **Replace:** "… lists all three as open (status fields dated 31 August 2025)". Record the hash in the bundle.

W6. **OPTIONAL.** "That PR 'rejects the proposed tuple containing 681943 …'. Its tuple, however, has 144 and 1984 where the forum certificate (14 September) has 44 and 984, apparently '1/44 + 1/984' misread."
- Accurate: I recomputed the PR tuple's deficit as exactly 131225/8053056, and the forum tuple, which has 9 distinct terms, as summing to 1.
- Two additions would make it fair to the PR:
  - its arithmetic on its own tuple is right; the error is in the transcription;
  - the PR itself says "Rejecting that tuple does not prove that 681943 cannot occur in another decomposition" (`W_src/fcissue_6842.json`).
- The PR's tuple came via the coordinator. Bank the PR diff in the bundle.

W7. **OPTIONAL.** "Konyagin's own known errata (his equation (4), and a missing 'm odd' in his Lemma 1, both confirmed by him to Wouter van Doorn per the #148 thread) …"
- Credit the finder: Quanyu Tang raised the equation (4) error on 5 Sep 2025. Konyagin's confirmation to van Doorn (Woett) came on 29 Dec 2025 (`live/t148.txt`).

W8. **OPTIONAL.** "Vose 1985 and Tenenbaum–Yokota were checked only through their zbMATH reviews, Konyagin 2014 only through two secondary sources …, and Graham–Kolesnik not at all."
- The list of sources not read in primary omits Gallagher 1971, which was checked by Crossref metadata only (W_report table). Add it.

W9. **OPTIONAL.** "… because the paper's own §7–8 method gives Theorem 1.1 more simply."
- The body says "the shorter route through §8". BvD say Sections 7 and 8 prove Theorem 3 by a method that offers a simpler route to Theorem 1. Use one phrasing on both sides, e.g. "the §§7–8 method (Lemma 7.1's greedy plus §8)".

W10. Checked and correct, no change needed:
- the 6 Oct release / byte-identical PDF;
- vDT v2 dated 24 May 2026;
- the Erdős–Graham p.32 and p.35 quotes (scans `W_src/eg/r-028.png`, `r-031.png`);
- 61/log 2 (BvD §5);
- the quotes "occupying 15 pages, out of 33 total", "entirely redundant" and "Strangely, nowhere in the paper is this oddity mentioned";
- v(k) ≤ kF(k)+2;
- Hart–Iosevich and base-B (BvD Lemma 4, Lemma 7);
- "formalised by Aristotle" (`vdgpt.tex` line 85);
- c₀ = 14/log 2 and both vDT–Astra bounds (`c18`);
- PR #6842 open since 2026-10-04, with no growth theorem;
- issue #476 open;
- FC: #304 research solved, #148 research open, no #293 file.

---

Counts: main body 11 MUST-FIX, 28 OPTIONAL; world paragraph 1 MUST-FIX, 8 OPTIONAL (W10 is a no-change list). Total 12 MUST-FIX, 36 OPTIONAL.
