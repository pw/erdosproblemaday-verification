# Blind consistency read: erdosproblemaday.com entry #160 (`160-shidong-itabe-upper-bounds-refereed`)

Reader: blind seat, 2026-10-13 ~18:45Z. I read the rendered body (`render_160.txt`), the HTML, the summary (it ships as `<meta name="description">` and `og:description` on the day page, and as the write-up blurb on `/problem/160`), and the HEADLINES card (`title`, `tag`, `line` in `apply160.py`; the title and tag render on the home page). I checked every number and attribution against the files on disk, not against memory. Witnesses and small thresholds were re-checked by my own script (`/tmp/blindread160/wit.py`).

Labels: **SUBSTANTIVE** means the finding changes a claim, a number, an attribution or a verdict. **MINOR** means wording, typography or redundancy.

---

## SUBSTANTIVE

**1. The Python checker never ran at p = 11 or 13, so "two implementations for p ≤ 13" is false. The same claim appears in four places.**
- Body (ii): *"A Python checker (…) and a C checker (…) each build Shi–Dong's colouring of ℤ/p⁴ℤ and test every pair (a, d), d ≠ 0: for p = 5, 7, 11, 13"*
- "What is ours": *"the two independent exhaustive verifications of the 27p-colouring for p ≤ 13"*
- Summary: *"re-implemented Shi–Dong's colouring twice (…) and enumerated every 4-AP in ℤ/p⁴ℤ for p = 5, 7, 11, 13"*
- Card line: *"enumerated Shi–Dong's 27p-colouring of ℤ/p⁴ℤ for p ≤ 13 in two implementations"*

Problem:
- The only Python log is `shidong/check_shidong_k4_py_p5_7.log`, which covers p = 5 and 7. The bundle README says the same thing.
- At p = 11 the second implementation is seat B's numpy checker (`check_k4_cyclic.py`, p = 5, 7, 11).
- At p = 13 (the 8.2·10⁸ case) only the C checker ran.

Fix: "a Python checker (p = 5, 7) and a C checker (p = 5, 7, 11, 13), with seat B's third implementation at p = 5, 7, 11. So p ≤ 11 has at least two independent implementations, and p = 13 has the C checker alone." Carry the same correction into "What is ours", the summary and the card line. Alternatively, run `check_shidong_k4.py 11 13` before shipping, which makes the sentence true.

**2. "Palette exactly 27p" is false at p = 7 in our own Python run, and false at p = 5 in the summary and card wording.**
- Body: *"the palette exactly 27p for p ≥ 7 (123–125 of 135 at p = 5)"*
- Summary: *"palette exactly 27p"*
- Card line: *"palette exactly 27p"*

Problem: the Python log reads `p=7 … palette=187 (<=27p=189)`, and seat B's run also gives 187 at p = 7. The C checker gives 123, 189, 297, 351. So the attained palette depends on the cubic. The summary and card versions drop even the p = 5 exception.

Fix: "palette ≤ 27p throughout, attained exactly at p = 11, 13 and by the C checker at p = 7 (187 of 189 with the Python checker's cubic; 123–125 of 135 at p = 5)." In the summary and card, write "palette within 27p".

**3. LeechLattice's construction is misdescribed.**
> *"(LeechLattice on MathOverflow, December 2021: partition F_p³ into the 8p² translates of a twisted cubic)"*

Problem: the MO answer partitions F_p³ into the **p²** sets Y_ij = {(t, t²+i, t³+j)}. The figure 8p² is the number of classes on [0, 8p³) after projecting to ℤ (4ap² + 2bp + c) and taking 8 shifted copies.

Fix: "partition F_p³ into the p² translates of a twisted cubic, then project to ℤ and shift, which covers [0, 8p³) with 8p² classes."

**4. The page misstates what the forum comment quotes.**
> *"its abstract states the slightly weaker /log log N form, which is what the forum comment quotes"*

Problem: ruizshi's comment (15:45, 4 Aug 2026) says *"a better lower bound h(N) ≫ exp(c(log N)^{1/6−o(1)}) follows from the result in https://arxiv.org/abs/2603.27045"*. That is the 1/6 − o(1) form, the first form of Theorem 1.4. The comment never writes /log log N. The page's own item (3) correctly reports it as exp(c(log N)^{1/6−o(1)}), so the two passages contradict each other.

Fix: "its abstract states the slightly weaker /log log N form; the forum comment quotes the (log N)^{1/6−o(1)} form."

**5. Seat D's coverage of Itabe's Lemma 4.1 is overstated.**
> *"brute-forced Lemma 4.1 for every P ≤ 121"*

Problem: seat D's report and `D_scratch/lemmas.py` (line 77: `for P in [25,49,73,97,121]`) test P = 24B + 1 for B = 1…5, plus generalised moduli (mod 4: P = 5, 9, 13; mod 6: P = 7, 13; mod 3: P = 7, 10). They do not test every P ≤ 121. The error comes from the internal log draft ("exhaustive to P = 121").

Fix: "brute-forced Lemma 4.1 for P = 25, 49, 73, 97, 121 (every P = 24B + 1 up to 121), and for the modulus-4/6/3 variants".

**6. Shi–Dong's Remark 4.2 is reported as a theorem in two places, while elsewhere the page correctly calls it a heuristic.**
- *"their Remark 4.2 notes that Chevalley–Warning caps what any constant-degree polynomial can add to k²/4 at O_k(1)"*
- *"Shi–Dong's Remark 4.2 says the polynomial method as used here cannot get there."*

Problem:
- The Remark says *"one should not expect to gain more than O_k(1) dimensions over k²/4 by using another polynomial of degree O_k(1) within the same framework."*
- Seat A classifies it as an unproved heuristic, and the page itself says *"Remark 4.2 is a heuristic"*.
- "caps" and "says … cannot" attribute a proved bound the authors did not claim. Seat A notes that only the layered-design version follows from Chevalley–Warning.

Fix:
- First sentence: "their Remark 4.2 suggests, by Chevalley–Warning, that a constant-degree polynomial in this framework should not gain more than O_k(1) dimensions over k²/4 (a heuristic; the precise version holds for the layered design)".
- Last paragraph: "…and Shi–Dong's Remark 4.2 suggests the polynomial method as used here will not get there."

**7. The label for Corollary 1.3 says we re-read DTZ Lemmas 3.2 and 7.11. Lemma 3.2 was not re-proved.**
> *"(b) rigorous modulo Deng–Tidor–Zhao's Lemmas 3.2 and 7.11 (… both are standard Behrend-type colourings and we re-read them)"*

Problem: seat A says *"I did not re-prove DTZ Lemma 3.2. DTZ only sketches it via Ruzsa [9, Thm 2.3] and random translates."* Seat A did re-check Lemma 7.11's proof for a = (1,2,3,4). A label that rests on 3.2 should say that 3.2 is a sketch in a refereed paper and is classical.

Fix: "(… peer-reviewed; 7.11 we re-checked for a = (1, 2, 3, 4); 3.2 is a sketch in DTZ, a Behrend-type pattern-free set plus random translates citing Ruzsa, which we did not re-prove; it is classical)".

**8. The mod-24 control did not fire on two of its three horizons, and our checker exits 2 ("cannot see"). The page does not say so.**
> *"his mod-24 label (… P = 25 and 49, up to 15,625 residues): no three-equal pattern and no ABAB, and with the digit labels removed ABAB appears on every horizon"*

Problem:
- `check_itabe.log` shows the three-equal control at `(P,L)=(25,1)` → 0 and `(49,1)` → 0. It fires only at (25,2).
- The script ends `RC 2` / `itabe rc=2`, its own CANNOT SEE code.
- The bundle README discloses this. The page mentions only the ABAB control, which did fire, and the item's other controls ("controls fire") are all green.
- An instrument that reports "cannot see" must not read as a pass.

Fix: after "…ABAB appears on every horizon", add "; the three-equal control fires only at L = 2 (at L = 1 the square norm alone produces no three-equal pattern), so the checker reports 'cannot see' on that row — the modulus-4 rerun below is the evidence that counts."

**9. Exact table: double-solver coverage is overstated, and the run status is stale.**
> *"each threshold UNSAT re-proved on a second solver (Glucose 4) under a second encoding … (the solver is still running past 51; … Glucose's second-encoding run at (36, 5) had not finished when this went live — the two lower thresholds it has re-proved)"*

Problem:
- **(a)** The main clause says every threshold was re-proved. `verify_unsat_glucose4.log` re-proves only (13,3) and (23,4). The (36,5) Glucose run (pid 669792, 1 h cap) is still running, so (36,5) currently rests on CaDiCaL alone.
- **(b)** `exact_h.log` now ends `N=52 k=6: TIMEOUT/UNKNOWN after 900s — stopping` (file mtime 18:41:28Z). "Still running past 51" is no longer true.

Fix:
- "…each SAT witness re-verified; the thresholds (13,3) and (23,4) re-proved UNSAT on a second solver (Glucose 4) under a second encoding; (36,5) rests on CaDiCaL alone (764 s) until Glucose's run lands."
- "The search stopped at (52, 6) on its 900 s cap, so h(52) ∈ {6, 7} is undecided."
- Re-check the Glucose (36,5) outcome before ship. If it times out, say so.

**10. The priority paragraph quotes ruizshi selectively and leaves out the sentence that matters most for fairness.**
> *"ruizshi's own comment under Itabe's claim (24 July) says their 1/4 construction was inspired by "a 1/3 bound suggested by GPT-5.6 Sol" and that he is "not entirely sure whether our result may have been indirectly influenced by this comment"."*

Problem: the comment (01:38, 24 Jul) opens *"it was not until I posted our latest 1/4 result … that I realized there was already a 1/3 argument in this comment"*. It also adds *"(it's pretty hard to precisely attribute the idea suggested by LLM). We will make sure to cite this comment in a future version of the preprint"*, and v2 did cite it four days later.

- The page omits both the statement of non-awareness and the promise to cite, which they then kept.
- What is left reads as an admission.
- "their 1/4 construction was inspired" also paraphrases "while developing our result, we were inspired".

Fix: quote the opening sentence and the promise to cite, and use the comment's own words ("while developing our result, we were inspired by a 1/3 bound suggested by GPT-5.6 Sol").

**11. The summary and the card line editorialise on priority and misname what coincides.**
- Summary / meta description: *"a priority story their 'concurrent' understates — Itabe was public eight days before their v1, and his colouring is exactly their k = 4 colouring restricted to the subgroup pℤ/p⁴ℤ."*
- Card line: *"a priority story the paper calls 'concurrent' that the dates do not support — Itabe's colouring is their k = 4 colouring restricted to pℤ/p⁴ℤ."*

Problem:
- "understates" and "the dates do not support" are verdicts on the authors, not facts. The brief requires facts and quotes only, and the body does that.
- It is Itabe's **cubic factor**, not "his colouring", that coincides with the restricted k = 4 colouring. His full colouring is the product with the mod-24 and dyadic labels.
- The body correctly says "up to the choice of F_p-basis"; the summary's "exactly" drops that.

Fix (both places): "…Itabe's manuscript was public eight days before Shi–Dong's v1, which did not cite it; v2 cites it as 'a concurrent result'. Itabe's cubic factor is, up to the choice of basis, their k = 4 colouring restricted to pℤ/p⁴ℤ."

**12. The card title over-claims twice, and the summary repeats the second over-claim.**
- Card title: *"the exponent falls from 0.355 to 1/4 — a cubic field norm kills the one pattern Behrend sets never could"*
- Summary: *"…which kills the one two-colour pattern (ABBA) that Behrend-style colourings cannot."*

Problem:
- **(a)** "The exponent falls" states an unrefereed preprint's bound as established. The body says *"Nothing in 2026 is refereed"*, and the card is read without the body.
- **(b)** "never could" and "cannot" assert an impossibility nobody has proved. DTZ say only *"it seems difficult to avoid symmetrically colored 4-APs by using Behrend-like sets as color classes."*

Fix:
- Card: "…the claimed exponent falls from 0.355 to 1/4 (two preprints, refereed here) — a cubic field norm handles the one pattern Behrend-type colourings had not".
- Summary: "…that Behrend-style colourings are not known to handle."

**13. "First exact values" drops the body's hedge, and the card line drops the last range.**
- Summary: *"Ours: … the first exact values"*
- Card line: *"Also the first exact values: h(N) = 3, 4, 5 on 4–12, 13–22, 23–35."*

Problem:
- The body says *"Nobody seems to have written down h(N) for small N"*, and the only evidence is an OEIS terms search with no artifact in the bundle. "the first" is a priority claim stronger than the evidence.
- The card line also omits h = 6 on 36–51, while the title and tag say N ≤ 51.

Fix: "exact values we could not find written down anywhere: h(N) = 3, 4, 5, 6 on 4–12, 13–22, 23–35, 36–51".

**14. The novelty of the parity step is attributed to Shi–Dong in a way that erases Itabe's earlier single-layer use of it.**
> *"Shi–Dong's parity step — symmetry forces an even polynomial, so only odd layers are needed — is the new algebraic idea"*

Problem: the page's own mechanism paragraph says both papers kill ABBA by *"g(3/2 + t) is even, so the t³ coefficient vanishes"*. Itabe's §7.2 does exactly this for the cubic layer, by direct elimination (27a + 9b + 3c = 0, 7a + 3b + c = 0 ⇒ 6a = 0), eight days earlier. What is new to Shi–Dong is using evenness to kill **several** odd layers at once (and the observation that even layers are therefore unnecessary). That is new relative to FT24's all-degree layering.

Fix: "Shi–Dong's parity step, run across every odd layer (symmetry forces an even polynomial, so only odd layers are needed), is what is new relative to FT24, and it is what gets k²/4 dimensions instead of k(k−1)/2. Itabe's §7.2 uses the same symmetry for the single cubic layer."

**15. The lower-bound reduction is not attributed to Hunter.**
> *"h(N) ≫ exp(c(log N)^{1/9}) from the Bloom–Sisask 3-AP bound — because a colour class restricted to [N/4, 3N/4] must be 3-AP-free …"*

Problem: erdosproblems.com/160 credits this to *"the observation of Zach Hunter in that question"*. Hunter's December 2021 MO question contains the reduction, with the interval [1, 2n/3]. The entry presents the reduction with no author. It also calls it "the same reduction" in (3), and later "the elementary lower-bound reduction (3) we checked ourselves".

Fix: "…from the Bloom–Sisask 3-AP bound via Hunter's observation (MO 410808, 2021): a colour class restricted to [N/4, 3N/4] must be 3-AP-free…".

---

## MINOR

**16. The axiom sentence contradicts itself.**
> *"all nine audited endpoints depend on exactly [propext, Classical.choice, Quot.sound] (the displayed-threshold identity needs only propext, Quot.sound)"*

The threshold identity is one of the nine (`their_axioms.log`). Fix: "eight of the nine depend on exactly [propext, Classical.choice, Quot.sound]; the ninth, the displayed-threshold identity, needs only propext and Quot.sound."

**17. Replay timings, and what `--trust=0` actually did.**
> *"the Mathlib cache downloads in three minutes — then lake build of all 21 first-party modules (174 s), his AxiomAudit.lean under --trust=0"*

- `driver.log` says *"No files to download … Decompressed 8283 already-cached file(s)"*. The 183 s step was cloning dependency repos and decompressing a local cache, not a download.
- The 174 s is the whole `check_release.sh` step (build + axiom audit + source scan + manifests). The driver's own `lake build -j2` failed instantly, and `build2` took 11 s.
- `AxiomAudit.lean` is imports plus `#print axioms`, so `--trust=0` re-checks nothing there. The kernel check of the 21 modules is the from-source build. Mathlib's oleans stay trusted until `leanchecker --fresh` (pid 663468, still running) lands.

Fix: "the cache step took three minutes (the oleans were already local); his check_release.sh built all 21 first-party modules from source and ran his audit (174 s in total)". Drop or explain the `--trust=0`.

**18. The paper contains no case analysis for Corollary 1.3, though the page says it does.**
> *"and the eight-pattern case analysis in the proof of Corollary 1.3 is complete."*

The paper writes no case analysis; seat A supplied one. The page later says *"the product step of Corollary 1.3 wants the eight-pattern case analysis made explicit"*. Fix: "and the eight-pattern case analysis that the proof of Corollary 1.3 leaves implicit goes through".

**19. Miscount of the symmetry conditions.**
> *"so that the k symmetry conditions give a degree-(k−1) polynomial k distinct roots"*

There are k/2 conditions (∀ i ∈ [k/2]), each giving two roots ±t. Fix: "the k/2 symmetry conditions give … k distinct roots".

**20. Several quotations are not verbatim.**
- *"interval i − 1 or i + 1"*: the paper says "interval i or i − 1 … interval i or i + 1".
- *"a carry … would place the pair on opposite sides of M/2, so τ differs"*: the paper says "the corresponding pair … so τ(y0) ≠ τ(y1) or τ(y2) ≠ τ(y3)".
- *"makes the exponent larger than k"*: the paper says "larger than the random exponent k".
- *DTZ Conjecture 1.6 ("N^{o(1)} colours suffice?")*: DTZ state it as an affirmative conjecture, "For all N, there exists an N^{o(1)}-coloring of [N] without symmetrically colored 4-APs".

Fix: quote exactly, or drop the quotation marks.

**21. A general-k lemma is described in k = 4 language.**
> *"a wrap would move a digit from the top third to the bottom third"*

Lemma 2.1 is for general k with k − 1 intervals. Fix: "from the top interval to the bottom one".

**22. The k = 6 sample does not add the first layered polynomial.**
> *"This exercises the layered polynomial, which k = 4 does not"*

The k = 4 Q = x₀ + N₃ is already two-layer. Fix: "This exercises a third layer (a degree-5 norm), which k = 4 does not".

**23. Three random cubics do not test basis-independence.**
> *"(the result is basis-independent, and this tests that)"*

Three random power bases, one per p, sample basis-independence; they do not test it. Basis-independence is immediate anyway (norm ∘ linear isomorphism). Fix: "with a randomly chosen irreducible cubic each time".

**24. τ is not recorded on every digit.**
> *"write n in base p and record, for each digit, which third of [0, p) it lies in"*

τ is recorded on every digit except the top one (Shi–Dong: digits 0…L−2; Itabe: the two low digits). Fix: "for each digit but the top one".

**25. The control drops more than the norm.**
> *"drop the norm coordinate"*

The control drops the whole Q coordinate (linear layer + norm). Fix: "drop the Q coordinate".

**26. Small inaccuracies in the seat D summary.**
- "+1 bridge against brute force for N ≤ 7" should be 4 ≤ N ≤ 7.
- "tight at m = 1–3" is about Lean's floor version (mr + 2m + 1 ≤ 5m⌊√m⌋), not the paper's inequality.
- "any even modulus ≥ 3" should be "≥ 4".
- "the modulus 24 is never motivated" is unfair as worded. 24 = a! with a = 4 is DTZ Lemma 7.11's χ modulus, and Itabe's Lean module is named `DTZABABExplicit`. Suggest: "the modulus 24 (DTZ 7.11's 4!) is not explained in the text; any even modulus ≥ 4 works".

**27. Two things that bear on the label for Corollaries 1.4–1.5 are not mentioned.**
- Seat B's report says the two displays match DTZ "exactly" (exponent, range and constant dependence agree); "word for word" overstates this, since the notation differs.
- Seat B's F3 found that DTZ's own proof of Theorem 2.8 has β_k inverted in its last display. The statement is correct.
- Seat B could not read Gowers's primary Conjecture 4.2 and relied on DTZ's Conjecture 1.10 restatement.

The label rests on both. Add one clause each.

**28. Itabe statement precision.**
- "Itabe proves the shift in Lean" holds for N ≥ 4.
- "explicitly h(N)^{3k} < 2,985,984^k N^{k+3} for N > max(…)" needs "for every integer k ≥ 1".

**29. "What no instrument here reaches" leaves out the case that matters for #160.**

It names k ≥ 8 and non-degenerate k = 6, but not k = 4 at p ≥ 17. Those are exactly the primes the h(N) ≤ N^{1/4+o(1)} corollary uses. Add "and the k = 4 colouring itself beyond p = 13".

**30. Tone toward DTZ.**
> *"which they could only attack with the ℤ/22ℤ tensor construction"*

DTZ also gave the local-lemma O(N^{2/k}) bound, and wrote "we were unable to resolve Conjecture 1.6 despite some effort". Fix: "for which their best construction was the ℤ/22ℤ tensor power".

**31. The shared-idea paragraph attributes Itabe's filters to DTZ.**
> *"…which a sphere-of-digits colouring avoids (Deng–Tidor–Zhao Lemma 3.2) … (DTZ Lemma 7.11 for ABAB; …)"*

- DTZ 3.2's colouring is random translates of a Behrend-type set.
- Itabe handles three-equal and ABAB with his own single mod-24 label (§4), not with DTZ 3.2 or 7.11.

Add "(Itabe's §4 does both with one mod-24 label)".

**32. Wording nits.**
- Summary: "N^{log 3/log 22} ≈ N^{0.355} above" is missing "+o(1)".
- "Nothing in 2026 is refereed" is ambiguous on a page titled "refereed". Say "has been through a journal".
- "unfolds siteH to the infimum over k of colourings" should be "to the least k for which there is a colouring".
- In the sources list, give Raghavan's title ("Improved Bounds for 3-Progressions").

**33. Artifacts.**
- The OEIS terms search has no artifact in the bundle. Save the query and the empty response.
- The bundle link points at a private repo, so it will 404 for readers. The body discloses this; consider dropping the link or marking it.

**Out of scope, noted.** `/problem/160` shows the Formal Conjectures statement with *"their label: research solved"*. That tag belongs to `erdos_160.known_upper` (the n^{2/3} variant), which the board template picks as "the statement". On an OPEN problem it reads as if the problem were solved. This is a board-template issue, not this entry.

---

## Checked and consistent (no change needed)

- 28,561 × 28,560 ≈ 8.2·10⁸; 7⁹ = 40,353,607; 5⁸·7 = 2,734,375; T³+2 and T⁵+T+3 (log); 10⁸ random + 121,060,818 = 3·(7⁹−1); no-Q control 13.
- 5¹⁰ ≈ 9.77·10⁶; e₆(7) = 5.236.
- (40k)⁴ > (76k)²; 2,985,984 = 729·4096; log 3/log 22 = 0.3554.
- 8,788; 119,277; 5,762,400 / 5,764,800; 3,107 / 6,561; palettes 35, 55, 91; 9 endpoints; 21 modules (20 E160 + root); 764 s.
- Witnesses: [12] = `0 0 1 2 1 0 2 1 0 1 2 2` and [22] = `0 0 2 3 1 3 0 1 0 2 2 1 3 0 1 0 2 2 1 3 0 3` match `exact_h.tsv` and are good colourings (my script).
- All 48 `exact_h.tsv` witnesses verify. My own backtracking confirms (12,3) SAT, (13,3) UNSAT, (22,4) SAT and (23,4) UNSAT.
- Thresholds 12/13, 22/23, 35/36 and N ≤ 51 match the table, the title, the tag and the summary.
- The eight-pattern list is complete (1 + S(4,2) = 8).
- The carry/norm mechanism is faithful to both papers. "Itabe's cubic factor = Shi–Dong's k = 4 colouring on pℤ/p⁴ℤ (x₀ = 0), same τ = ⌊3x/p⌋, up to basis" checks against Itabe (7.1)–(7.10) and Shi–Dong's proof of Theorem 1.1.
- Lower-bound reduction (x+3d ≤ 3N/4 + N/4) is correct.
- "Roots distinct because p > k" is fine: for prime p and even k ≥ 4, p ≥ k ⇔ p > k, so this agrees with seat A's p > k−1.
- The pp.all statement and siteH unfolding match `axioms.log`. The negative control shows sorryAx. `source_scan.log` is empty, with stderr captured.
- Dates and attributions check out: Hunter 18 Oct 2025 07:23; LeechLattice 15 Dec 2021; Itabe 14 Jul (release 05:26Z) and claim 15 Jul 00:32; Shi–Dong v1 22 Jul 22:06Z, claim 24 Jul 01:29, ruizshi comment 24 Jul 01:38, v2 28 Jul; ruizshi 4 Aug 15:45; page edited 2 Dec 2025; DTZ MPCPS 179 (2025) 79–103 (per Shi–Dong's reference); Raghavan v1 27 Mar, v3 15 May; "using GPT-5.6" and "using GPT 5.6 Sol" verbatim; v1 cites neither Itabe nor FT24; "strongest previously known" unchanged in v2.
- Every other seat number the page cites matches the seat reports (except item 5).
- "Unreviewed by humans" is present in the body and the tag. Nothing claims the problem is closed or a bound is ours.

---

**Overall verdict: FIX THEN SHIP.** The core verdicts hold and are faithfully reported: Shi–Dong holds as read, Itabe replays green, and the exact table is correct. But the bar paragraph overstates our own instruments: the Python coverage, "palette exactly 27p", the silent mod-24 control, and the Glucose (36,5) re-proof. One source is misquoted (the forum comment) and one construction misdescribed (LeechLattice's twisted cubic). The summary and card editorialise on priority and over-claim the result (items 1–15).
