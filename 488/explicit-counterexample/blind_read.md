# Blind cold read: /day/488-gessel-counterexample-refereed-and-made-explicit

Reader: a fresh seat that had not seen how the page was made, reading as a skeptical number theorist. Date 2026-11-11.
Read: page_render.txt and page.html, the whole bundle (README, lean/, referee/, world/, explicit/, routeC/), Liu v2, Gessel's note, the parsed forum thread, the saved Jig pages, erdosproblems.com/488 and its history page, and the July search report (`~/MathDyad/runs/erdos488_divisor_closed_density.md`).
Ran: small exact Python checks of every derived number, and one small run of `brackets.c` (y = 251, T = 10^4, 10^6, 10^8, K = 2.6·10^7, about 420 MB). That run was needed because the bundle has no output for these containment points.

## Verdict: SHIP WITH FIXES

The mathematics holds.
- The band identity is Liu's Lemma 12. I re-derived it, including the need for y ≤ Λ (strip primes p ≤ y ≤ Λ) and Λ ≤ q (a cofactor below Λ is smooth).
- `bracketsW.c` does what the page says. Ψ_up is the count with Ld ≤ ⌊R ln x⌋. Ψ_lo is the count with Ld·(1+1/w₂) ≤ R ln x. Then |A|_up = Ψ_up(ΛT) − Ψ_lo(T) and M_lo = Σ_u max(0, Ψ_lo(⌊WT/u⌋) − Ψ_up(T)). The sum runs over u = 1 and the primes in [q, W). The program refuses to run unless W < q² and y ≤ Λ ≤ q. The test n·M_lo > 2m·|A|_up is done in u128, and the products (≤ 6·10^35) do not overflow.
- In every row, n = ΛT ≥ max A and m > n.

Every number traces, with three exceptions:
- "9 test points": the README lists 8.
- Cambie's "November 2025": his remark was already on the page in the 2025-10-20 revision.
- "Smallest we certified": the bundle holds a smaller certified n.

Two items are MUST. One is a priority claim stated as fact. The other is a row label that our own bundle contradicts.

## MUST

**M1. Priority stated as fact.**
- Page: "No explicit counterexample below n ≈ 10^118 had been published."
- The same claim is in the entry summary (`src/index.js` line 38): "the only explicit counterexample published before had n ≈ 10¹¹⁸".
- The HEADLINES ticker carries it as "(BEFORE: 10¹¹⁸)". The title implies it with "come down from n ≈ 10¹¹⁸".
- world_W.md (e) forbids "priority as settled fact … rather than 'earliest we found'". Its own search was bounded: it could not check Guy E5 3rd ed., Hall–Tenenbaum, Hall 1996 or Ruzsa.
- Fix: "As far as we found, no explicit counterexample below n ≈ 10^118 had been published (Toledo's search of smooth bands up to 10^7 found none; Liu's n = 6.7·10^13 band reaches 1.447)." In the summary: "the only explicit one we found published before had n ≈ 10¹¹⁸".

**M2. The row "Smallest we certified (ours)" is not the smallest we certified.**
- The row gives T = 1.1·10^12 and n = 1,114,300,000,000,000.
- `explicit/out/scanW3*_out.txt` certifies a smaller pair: y = 1009, T = 1,096,478,196,143, n = 1,110,732,412,692,859, W = 251,224, ratio_lo = 2.000284478, certified=1.
- The page's own by-y list ("1009: 1.1·10^12") is that scan point.
- Fix, either of:
  - (a) Relabel the row "Round T just above our smallest (both programs)", and add one line: "the smallest on our grid is T = 1,096,478,196,143, n ≈ 1.111·10^15, ratio ≥ 2.00028, certified by our program only".
  - (b) Put the true smallest in the row, with "—" in the second-program column.
- Related: the title says "n ≈ 1.2·10¹⁵ overall" while the table says 1.1·10^15. Either say "≈ 1.1·10¹⁵ overall", or say the headline is the round case both programs certify.

## SHOULD

**S1. Credit for statement 41.**
- Page: "an explicit instance with T = 2^384 (so n ≈ 10^118) was certified by a Python checker (statement 41)."
- The author is unnamed. Jig and Liu's reference [10] both name **woshuajolk** (made with Fable 5.1 / Claude Code, 6 Sep 05:59Z). The table row says "not ours" but never says whose.
- Fix: "…was certified by a Python checker (statement 41, woshuajolk)." In the table: "Explicit instance on Jig (woshuajolk, statement 41, Python checker)". Optionally give its in-lane floor: certified ratio ≥ 2.0013 (floor 1.000634 on the halved ratio at S = 8000).

**S2. Credit Liu for the band family behind the headline row.**
- "Headline band (ours) | 1009, 1013" reads as if the band were ours.
- The bands A_{T,Λ} and the finite-m formula are Liu's §4. His Table 1 lists p = 1009, p′ = 1013, with limiting ratio 14.47 as T → ∞.
- What is ours: picking a finite T and m, and certifying the inequality there.
- Fix: rename the row "Liu's 1009-band at finite T (certificate ours)". Add a sentence: "Liu's Table 1 gives this band's limiting ratio as 14.47; at T = 1.2·10^12 it is only just above 2, which is why the certificate needs exact counts."

**S3. Independence of the second program is overstated.**
- Page: "A separate seat wrote its own certifier from the definitions alone, without seeing ours".
- routeC/README.md §1 says it used "the fact supplied by the coordinator", which is Liu's Lemma 12(iii). It was also given the target parameters, exact control values and our lower bounds: "Both bounds exceed the coordinator-supplied lower bounds (2.003562825 and 2.000402962)".
- So both programs share the identity as a dependency. Each checked it by brute force on tiny cases, which is fine, but it is not "the definitions alone".
- Fix: "…wrote its own certifier without seeing our code, from the definitions and Liu's identity (which it re-checked by brute force on small cases)…".

**S4. The title overclaims the Formal Conjectures replay; the entry summary does too.**
- Title: "its Lean replays against Formal Conjectures as it reads today". Summary: "his statement is provably identical to Formal Conjectures' erdos_488 as it reads today".
- Referee O3: the bridge was elaborated in the standalone file's 13-module import context, not under `FormalConjecturesUtil`, and no artifact compiles `refutation` against FC's own elaborated term. The body states this caveat; the title and summary do not.
- Fix: title "…its Lean replays, and refutes Formal Conjectures' current statement pasted verbatim…". Summary: "his adapter's statement is textually identical to Formal Conjectures' erdos_488 as it reads today, and equal to it by Iff.rfl in a standalone file".

**S5. "No tracker records it yet" is inaccurate.**
- Page: '"closed" means closed on Jig; no tracker records it yet.'
- Jig itself records the problem as Refuted.
- The plasma-ai/erdos wiki says "status: claimed, claim: disproved".
- FC carries the label "solution found", which the page reports two paragraphs earlier.
- Fix: "…closed on Jig; erdosproblems.com, the community database and Formal Conjectures do not yet record it."
- Also make clear these are fixes to Gessel's note. Our own badge says CLOSED, so write: "Two wording fixes to the note. … the note's 'the problem is closed' means closed on Jig."

**S6. Say that the referee pass is an AI pass.**
- "Our referee pass" and "A separately briefed seat tried to break every step". A number theorist will not know what a "seat" is and may read this as a human referee.
- world_W (e) forbids implying the result is "refereed … or confirmed by mathematicians".
- Fix: "A separate Claude instance, briefed only with Gessel's note and told to act as a hostile referee, tried to break every step…". Elsewhere use "a separate Claude instance" instead of "seat". The summary's "our hostile seat" has the same problem.

**S7. "These are not the smallest counterexamples" is unproven.**
- Page: "These are not the smallest counterexamples: Liu's Problem 18 stays open…"
- We do not know that. No smaller counterexample is known, and the page says the least one is open.
- Fix: "We do not claim these are the smallest: Liu's Problem 18 stays open…".

**S8. H(k) is undefined.**
- Page: "the bound |A| ≤ 8H(k+1); the injection that gives M(m) ≥ H(k)·φ(Q)…", and later "2H(k+1) ≤ 3H(k)".
- Fix: at first use, "H(j) = the number of odd 251-smooth integers up to 256^j".

**S9. The whole-period row is not certified "as exact integers".**
- Method paragraph: "A pair is certified when n · (lower bound on M(m)) > 2m · (upper bound on |A|), compared as exact integers."
- That is true for the finite-m rows (`bracketsW.c`).
- The row "Gessel's set, whole period … lcm A … 2.0467" comes from `bracketsL.c`. That program bounds the density with a long-double tail sum Σ e^{−Ld(1+1/w₂)/R} and a 10⁻⁹ allowance. It is rigorous given the floating-point analysis, but it is not an integer comparison.
- Fix: one clause, "(for the whole-period row M(m)/m is the density of B, bounded below by a tail sum in extended precision with a rounding allowance; see the README)".

**S10. The k = 6 sentence is more precise than its evidence.**
- Page: "For Gessel's set at k = 6 (T = 2^48) the best m we tried gives at most 1.9947, just short; we have not ruled out every m."
- Later: "It also gives an upper bound of 1.99472…"
- The upper bound exists for one m only, W = 24,415, the one with our best lower bound. Route C puts it in [1.994680, 1.994695] at R = 1,985,362, or [1.994659, 1.994715] at R = 10^6.
- The two numbers on the page come from different resolutions, so they read as inconsistent.
- The W grid tried for k = 6 is not recorded: `gessel_family_W.txt` prints only bestW.
- Fix: "For Gessel's set at k = 6 (T = 2^48), the m with our best lower bound, 24,415·2^48, has ratio in [1.99468, 1.99470] (second program), just short; other m we tried score lower, and we have not ruled out every m." Use 1.99470 in the second-implementation paragraph too, and record the W range in the bundle.

**S11. The by-y list sorts by the wrong quantity and stops where T keeps falling.**
- Page: "Where the best T falls, by y … 887: 1.3·10^12; 1009: 1.1·10^12."
- Problem 18 asks for the least n (or least max A). These are T values, and n = qT.
- The scans also certify y = 1129 (T = 1.05·10^12, n = 1.205·10^15) and y = 1499 (T = 1.0·10^12, n = 1.51·10^15). So T keeps falling past 1009, while n is smallest at y = 1009 on our grid.
- Fix: list n, or both. For example: "smallest certified n by y: 199: 5.9·10^17; 251: 8.1·10^16; 307: 2.0·10^16; 401: 5.0·10^15; 449: 4.1·10^15; 523: 1.9·10^15; 887: 1.20·10^15; 1009: 1.11·10^15; 1129: 1.21·10^15". Drop "best T".

**S12. The exact-count test points don't match the README and lack outputs.**
- Page: "At 9 test points (y = 61, 251, 509; T up to 10^12), every exact value lies inside our bounds…"
- The README lists 8: y = 251 at 10^4, 10^6, 10^8; y = 509 at 10^10, 10^12; y = 61 at 10^5, 10^6, 10^12.
- The bundle holds our bracket output for only the three y = 61 points (`tiny_W_brackets.out`, `liu_control_brackets.txt`).
- For y = 251 and y = 509 it has only the exact values. The only y = 509 bracket output is the rounded-up negative control.
- I re-ran `brackets.c` at y = 251. Containment holds at all three points:
  - Ψ(10^4) ∈ [5507, 5508] against exact 5508, and Ψ(qT) ≤ 315875 against exact 315875.
  - Ψ(10^8) ∈ [3400971, 3401031] against exact 3401025.
  - Every ratio_lo is below the exact ratio.
- So the claim is true where I checked, but the receipts are missing.
- Fix: put the y = 251 and y = 509 bracket outputs in `explicit/controls/`, and either state 8 or say what the ninth point is.
- On the same paragraph: "for the finite-m certificate behind our headline the gap is about 4 parts in 10^5" reads as if exact counts were done at y = 1009. They were not. The 4.4·10⁻⁵ is the y = 61 Liu control (1.524123 vs 1.524190), and at the headline the comparable figure is route C's 3.8·10⁻⁵.
- Fix: "for the finite-m certifier (tested on Liu's y = 61 band) the gap is about 4 parts in 10^5".

**S13. The bundle README contradicts the page on k = 111.**
- README: "Smallest slow k = 111 (float DP with a rigorous error envelope, R = 32768); k = 112 by exact integers (R = 2048)."
- The page says k = 111 in exact integers. That is supported: `referee/slowk_crt_32768.out` gives exact CRT certificates at k = 111 and k = 112, with fast steps exact up to 110, and referee_R.md says the same.
- The README is stale. Fix it, because it is the public receipt.

## NIT

- **Cambie date.** Page: "(Alexeev, Aristotle, Cambie, November 2025)". Cambie's remark is already in the earliest erdosproblems.com/history/488 revision (2025-10-20). Alexeev and Aristotle are 27 Nov 2025. Fix: "(Cambie; Alexeev and Aristotle, November 2025)".
- **Identity check only at Λ = q.** "We re-checked both formulas … in 62 small cases" is followed by "Gessel's construction is the case y = 251, Λ = 256". All 62 cases in `identity_check.py` have Λ = q; none has Λ < q. Add a few Λ < q cases, or say "(all with Λ = q)".
- **Liu frames Gessel's case differently.** Liu writes it as "p = 257, Λ = 256 (so Λ < p)", outside his Lemma 12. The page's y = 251 is correct, because the primes are those below 257. A reader holding Liu will notice the clash. Add: "(Liu writes p = 257; with Gessel's primes below 257 it is y = 251, inside the lemma)."
- **Lower bound wording.** "Rounding each weight down can only overcount, and the loss is at most one unit per prime factor, so both bounds are one-sided" leaves the lower bound implicit. Add: "so shrinking the threshold by the factor w₂/(w₂+1), w₂ = ⌊2^20 ln 2⌋, gives a lower bound".
- **How the u-sum is evaluated.** Say once that W < q², so the rough u < W are 1 and the primes in [q, W). Also "M(WT)" never says m = WT.
- **"A planted error. The same program…"** "Same program" grammatically points at the exact counter in the paragraph before. Fix: "Our certifier, with every weight rounded up…". It was run on `brackets.c`, which shares the Ψ machinery with `bracketsW.c`.
- **Size of counts.** "a Lean version would need the 10^12–10^13-sized counts formalised". The counts are Ψ(T) ≈ 7·10^9, |A| ≈ 5.7·10^11 and M(m) ≈ 2.8·10^14. Fix: "counts up to about 3·10^14 (smooth numbers up to 3·10^17)".
- **"a few hundred times qT".** W/q is 80–110 for y ≤ 307 and 141–248 for y = 449–1009. Fix: "about 80 to 250 times qT".
- **"Wider prime gaps after y help".** y = 1009 (gap 4) beats y = 887 (gap 20), and y = 557 (gap 6) beats y = 523 (gap 18). Either drop it or say "at comparable y, a larger q − y helps".
- **"Erdős's inequality says it is always below 2".** Fix: "Erdős asked whether it is always below 2".
- **"proved it equal … by Iff.rfl".** Fix: "proved it equivalent (definitionally) by Iff.rfl". Also "fetched today" should read "fetched 11 November", and "14 October rewrite" should be "14 October change (prop-valued answer removed)".
- **"Each lemma has a positive control … and a negative control".** The pigeonhole has no negative control (referee: "No negative control exists for endpoint_gap's decide"). The far-injection positive control uses a truncated residue set. Fix: "Each counting lemma has…".
- **Table header.** "second program" should be "second program, certified ratio ≥". "It certifies every row in the last column" should be "every row with an entry in the last column". "Gessel's set at k = 7 (ours)" should be "(certificate ours)".
- **Liu comparison.** "his search over m was presumably narrower" is fine as hedged. Better: "m = 2876·T may lie outside the range he searched". Our own full-period ratio for that band is 1.4438 (`liu_control_exact.txt`), close to his 1.447, which may explain his number.
- **Bundle README operator details.** The first line names seats and the 5-hour cap. `mirror_classify.py` withholds files with operator details, which could withhold the README from the public mirror. Strip that line, then run `scripts/mirror_verification.sh` and check that the README and `lean/proof-note.md` (Gessel's third-party note) are handled as intended.
- **Stale comment.** The header comment in `scanW4.sh` (W in [32q, 320q], T 10^11..10^17) does not match its code (W in [64q, 1000q] step 2q, T = 10^(j/50), j = 550..620).

## Numbers traced

| Number on page | Source / derivation |
|---|---|
| 2 − 1/a (A={a}, n=2a−1, m=2a) | derived; Liu §1; erdosproblems.com/488 |
| Erdős 1961, 1966 p.150, 1980 p.112; Guy E5 | erdosproblems.com/488 ([Er61,p.236][Er66,p.150][Er80,p.112], Gu04 E5); Liu refs [3–5,8] |
| "two printings say non-multiples" | Liu §1 ("In [3, 5]"); forum post on the Er80 typo |
| Alexeev, Aristotle Nov 2025 | thread_parsed.txt posts 1860/1862/1865 (27 Nov 2025) |
| Cambie Nov 2025 | **NOT TRACED.** Remark present in the 2025-10-20 history revision |
| 5 Sep 2026, GPT-6 Astra, k < 4096, T = 256^k, n = 256T, m = 2TQ | Gessel proof-note.md; world_W timeline |
| Jig problem 398, statement 40; PR #5297; claim #266 | world_W; jig398_s40.html |
| Statements 42–43 Benefield; 41 Python checker, T = 2^384 | world_W (c); jig398_s41.html; Liu ref [10] |
| n = 2^392 ≈ 1.0·10^118; m = 2^385·Q | Python: 2^392 = 1.0087e118; Jig s41 (m = 2·2^384·Q) |
| Liu 17 Oct 2026, Zenodo, not peer-reviewed | world_W; liu_v2.txt |
| "solution found", reviewer replay | world_W (b) (mo271 18 Sep; Deicyde) |
| Toledo 7 Nov | world_W |
| no statuses since 6 Oct; remarks last edited 8 Apr; claim no comments | world_W (a), (b); 488.html footer |
| "falsifiable" = open; 2026-03-29 | world_W (teorth problems.yaml, CONTRIBUTING.md) |
| FC research open; PR unmerged, needs rebase | world_W (d) |
| Problem 18 | liu_v2.txt line 391 |
| n = 6.7·10^13, 1.447 | liu_v2.txt §6 (p=61, Λ=67, T=10^12) |
| July search: max A ≤ 28, m ≤ 10^6 | ~/MathDyad/runs/erdos488_divisor_closed_density.md (2026-07-25); erdos488_search.py "report" tier |
| \|A\| ≤ 8H(k+1); M(m) ≥ H(k)φ(Q); 3Q < 16φ(Q) | Gessel note eq. (7), (10), (1); referee_R.md (a)–(e) |
| φ/Q = 0.2007 | referee/constants table (0.20070659…); my Python 0.2007066 |
| Lean 4.33.0, Mathlib db584cd; axioms | lean/lean_out.log, steps.tsv, lake-manifest |
| Three planted errors | lean/ctl2_NegConst.log (rc 1), ctl2_NegSorry.log (sorryAx), ctl2_NegBridge.log (Iff.rfl mismatch) |
| 14 October rewrite | world_W (FC #6762, #6740) |
| k = 111 smallest; k = 110 fails; exact integers | referee/slowk_crt_32768.out (exact, fast 0..110, slow 111, 112); referee_R.md. README is stale (S13) |
| numbers near 10^49 | H(111) ∈ [1.31540·10^49, 1.31573·10^49] (slowk_crt_32768.out) |
| T = 2^888, n = 2^896, m = 2^889·Q | derived from k = 111 (T = 256^111) |
| 2.14 (Gessel row) | (32/3)·φ/Q = 2.14087 (referee constants); with exact H brackets ≥ 2.1437 |
| 62 small cases | identity_check.out: 17 + 45 = 62, 0 failures; negatives break |
| Λ, q, y triples (251/256/257; 1009/1013; 61/67) | bracketsW.c guard; Python next prime |
| ⌊2^20 ln p⌋ | weights.py / weights_20.txt (2 → 726817) |
| 2^64 ≈ 1.8·10^19; 2^72 ≈ 4.7·10^21 | Python 1.8447e19, 4.7224e21 |
| 2.0467 (whole period, T = 2^64) | out/gessel_family_k.txt ratio_lo 2.046671428 certified=1 (bracketsL) |
| k = 7: 22,616·2^56, 2.1253 / 2.1254 | out/gessel_family_W.txt (2.125275056); routeC README §4 #2 (2.125364 at R=1e6; 2.125388 at R=1,985,362); my exact recomputation 2.125275 |
| headline: T = 1.2·10^12, n = 1,215,600,000,000,000, m = 250,347·T ≈ 3.0·10^17, 2.0036 | out/headline_y1009.txt (2.003562825); Python m = 3.0042e17 |
| 2.00364, [2.00364, 2.00366] | routeC README §6 #5 R=1,985,362: [2.003640247, 2.003653193] (rounded outward) |
| "smallest": T = 1.1·10^12, n = 1,114,300,000,000,000, 2.0004 / 2.00048 | out/headline_y1009.txt (2.000402962); routeC §6 #6 (2.000480050). **Not the smallest certified; see M2** |
| 5.7·10^11 elements | \|A\| ≤ 570,685,479,308 (headline_y1009.txt) |
| 4.7·10^−4, 9.4·10^−4 | Python: 570685479308/1.2156e15 = 4.6947e−4; 282574347563735/3.00416e17 = 9.4061e−4 |
| by-y T: 199 2.8e15, 251 3.2e14, 307 6.3e13, 401 1.2e13, 449 8.9e12, 523 3.5e12, 887 1.3e12, 1009 1.1e12 | scanW3*/scanW4* first certified (2.818e15, 3.162e14, 6.310e13, —, 8.913e12, 3.548e12, 1.318e12, 1.096e12); refine_y401.txt (1.2303e13) |
| "a few hundred times qT" | scans: W/q = 80–248; **loose** (NIT) |
| k = 6: 1.9947; 1.99472; 24,415·2^48 | gessel_family_W.txt (ours ≥ 1.994588, W = 24415); routeC §4 #3: upper 1.994715 (R=1e6), 1.994695 (R=1,985,362) |
| 9 test points | **NOT TRACED.** README lists 8; our bracket outputs in bundle for 3 only (S12) |
| y = 61, 251, 509; T up to 10^12 | controls/exact_routeA_y251.txt, exact_routeA_y509.txt, liu_control_*.txt, tiny_W_*.out |
| 4 parts in 10^5 | liu_control_brackets.txt 1.524123288 vs exact 1.524190400 → 4.4e−5 (y = 61, not the headline) |
| \|A\| = 64,844,856 | controls/liu_control_exact.txt; liu_v2.txt §6 |
| m = 2876·T, 1.5242 | README item 4; routeC check_m_control (exact M = 4,242,568,187); Python 1.52419040 |
| planted error (round up) | controls/negcontrol_ceil.txt: Ψ_up(qT) 6,657,973,823 < exact 6,657,989,227 (w₂ = 726818) |
| second implementation: two resolutions, uint64 | routeC/README.md (R = 10^6, 1,985,362; uint64 with overflow guards) |
| dates 11 Nov, 6 Oct, 8 Apr, 17 Oct, 7 Nov, 14 Oct, 5 Sep | world_W timeline |
| Mat. Lapok 17 (1966) 135–155 | Liu ref [4] |
