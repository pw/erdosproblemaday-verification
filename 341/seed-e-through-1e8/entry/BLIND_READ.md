# Blind consistency read: Erdős #341 entry ("the last seed in [12]")

What I read: only `render_page.txt` (the whole entry) and the #341 headline card in `render_home.txt`. I did not read code, logs or any other repo file. I did not judge whether the mathematics is true. Where I recomputed something, I used only numbers printed on the page; those checks are marked [arith].

Locations: **Title** is the page `<title>` and the H1 (identical). **Chips** are the status line under the H1. **Card** is the home-page headline card. **URL** is the visible slug. Body paragraphs:
- **P1** "The problem (…)"
- **P2** "The wall, moved."
- **P3** "What the sequence does instead…"
- **P4** "The rotation is not a metaphor…" (runs through the five other seeds)
- **P5** "Why Li's method cannot be the proof…" (heading plus the two ingredients)
- **P6** "E has no shield…" (the SAT census)
- **P7** "One step up."
- **P8** "Controls and what is not claimed."

The most serious findings are **1, 2, 3, 4, 5, 9, 14, 21, 24 and 27**.

---

## A. Arithmetic and numbers that disagree

**1. P7: the census total is off by one.** [arith]
- Phrase: "Together with July's [12] that is 16,377 of 16,383 nonempty seeds inside [14] with an all-future certificate … and six distinct resisting sequences".
- Problem: certified seeds are 4,094 ([12], July) + 4,094 (max 13) + 8,188 (max 14) = **16,376**. Resisting seeds are 1 + 2 + 4 = **7** rows (E, two with max 13, four with max 14), and 16,376 + 7 = 16,383. The 16,377 comes from subtracting the 6 distinct *sequences* instead of the 7 resisting *seeds*. {3,5,8,10,13,14} is uncertified even though it duplicates a sequence.
- Fix: "16,376 of 16,383 nonempty seeds … certify; the other seven, which generate six distinct sequences, resist."

**2. P3: 889, 9,547 and 27,875 are not intermediate fractions of the page's own g.** [arith]
- Phrase: "(889, 9,547 and 27,875 are intermediate fractions)".
- Problem: from the page's partial quotients [0; 3,1,1,17,1,1,1,1,2,1,2,1,2,1,12,…], the intermediate-fraction denominators are 11, 18, …, 116 (step 7), 1,019, 3,946, 14,765, 23,293+k·31,821… None of them is 889, 9,547 or 27,875. Instead 889 = 636 + 253 and 7,892 = 8,528 − 636, which are sums and differences of convergent denominators. On the page's g: ‖889g‖ ≈ 0.00223, ‖9,547g‖ ≈ 0.00078, ‖27,875g‖ ≈ 0.00022. These are worse than the unlisted convergent or intermediate denominators near them: ‖1,019g‖ ≈ 0.00082, ‖2,291g‖ ≈ 0.00013, ‖6,237g‖ ≈ 0.00009, ‖8,528g‖ ≈ 0.00003, ‖23,293g‖ ≈ 0.00003.
- Fix: drop "intermediate fractions". Say what they are, for example "889 = 636 + 253, 9,547 and 27,875 are not best approximations of g", or explain them.

**3. P3: the record ladder does not track ‖qg‖ on the page's own g, yet the page says it is "the shadow of" the rotation.** [arith]
- Phrase: "What these numbers are the shadow of is the Fourier transform" and "The near-periods are the continued fraction of g".
- Problem: if the indicator were a rotation coding, agreement at shift q should rise as ‖qg‖ falls. On the page's g:
  - 383 (‖·‖ ≈ 0.0013) beats 253 (≈ 0.0018), but 383 is not a record.
  - 2,291 (≈ 0.00013) and 6,237 (≈ 0.00009) beat 1,655 (≈ 0.00035), but neither is a record.
  - 889 (≈ 0.0022) is a record ahead of 636 (≈ 0.00047), at 97.8% against 97.1%.
  - A careful reader who computes ‖qg‖ will notice all of this.
- Fix: say that the ladder is only partly explained by the convergents and that the agreement metric is not monotone in ‖qg‖ (for example because of the edge-zone residual), or recheck the ladder.

**4. P3: the five arcs add up to 11% before the fifth arc is counted.** [arith]
- Phrase: "five flat arcs (0.139–0.173, 0.367–0.403, 0.599–0.637, 0.832–0.834 and a narrow one near 0.94; 11% of the circle)".
- Problem: the four stated arcs measure 0.034 + 0.036 + 0.038 + 0.002 = 0.110, which leaves zero width for the arc "near 0.94". The fourth arc, 0.832–0.834, is 2 bins wide at the stated 1,000-bin resolution. That is no wider than the arc called "narrow", and an arc 2 bins wide cannot have a core "away from the edges". 0.834 looks like a typo. The 11% is independently consistent with density, since 0.11 + 0.095 × 0.487 ≈ 0.156, so the endpoints are probably what is wrong.
- Fix: give exact endpoints for all five arcs, including the one near 0.94, so that they sum to the stated 11%. Check 0.832–0.834.

**5. P3: "every integer … — 34 exceptions" contradicts itself, and so does "exact" in the Title and Card.**
- Phrases:
  - P3: "on which every integer is in S — 34 exceptions among 110,000" and "on which no integer is in S — 42 exceptions among 795,003".
  - P3: "the greedy arithmetic decides membership only inside the edge zones".
  - Title: "exact away from the arcs' edges".
  - Card: "exact except on the arcs' edges".
  - P4: "a rotation coding in the exact sense E is on its cores".
  - (c) reading: "a residual confined to the arcs' edges".
- Problem: the page's own data has 76 integers outside the edge zones that break the coding. "Exact", "every" and "confined" all overstate what was measured.
- Fix: "all but 34 of the 110,000 integers on the arcs are in S, and all but 42 of the 795,003 in the deep complement are out". Replace "exact" in the Title and Card with "exact on all but 76 of ~900,000 core integers", "almost exact", or "exact up to ~10⁻⁴". In the (c) reading say "a residual concentrated on the arcs' edges".

**6. P3: the 59%/41% split does not fit the claim that the arcs are sum-free.** [arith]
- Phrase: "the sumset of the cores covers only 59% of the circle, and it is the edge elements … that cover the remaining 41%".
- Problem: S + S must cover the non-members (79.5% deep complement plus about half of the 9.5% edge zones) and must *avoid* the 11% of arcs. 59% + 41% = 100% of the circle, so "the remaining 41%" includes the arcs, which the previous clause says no sum reaches. The next phrase, "the phases of S + S fill the complement of the arcs at uniform density", also cannot hold literally inside the edge zones, where about half the integers are members and so are *not* in S + S.
- Fix: give the percentages relative to what must be covered, for example "the cores' sumset covers X% of the complement of the arcs and the edge elements cover the remaining Y%". Write "the deep complement" where that is what is meant.

**7. P2 and Title: onset bounds are rounded up, which strengthens the claim.**
- Phrases:
  - Title and Card: "beginning before 5·10⁷".
  - P2: "onset before 50.0·10⁶".
  - P2: "every membership period up to about 25·10⁶".
- Problem:
  - The proved scope is onset ≤ a_7,810,617 = 49,993,396. "Before 5·10⁷" and "before 50.0·10⁶" also claim onsets in (49,993,396, 5·10⁷), which the test does not cover. "50.0" also signals three significant figures.
  - The membership bound computes to (3,905,308 − 3,072)/0.1563 ≈ 24.97·10⁶. "About 25·10⁶" rounds up in the claim direction.
  - By contrast, "3.9·10⁶" for 3,905,308 correctly rounds down.
- Fix: "beginning at or before 49,993,396 (just under 5·10⁷)". In P2 write "up to 24.9·10⁶ with onset at or before 49,993,396".

**8. Title and Card: "5·10⁷" does not say what it measures.**
- Phrase: "no gap period of up to 3.9·10⁶ terms beginning before 5·10⁷".
- Problem: the period is counted in *terms*, so a reader will take 5·10⁷ as a term index. It is an integer position, roughly term 7.8·10⁶. Read the first way, the claim is about 6.4× stronger than the body's.
- Fix: "…beginning below the integer 5·10⁷ (term 7.8·10⁶)", or "…beginning by term 7.8·10⁶".

**9. P2: the gap-to-membership bound rests on the constant "2·1536", which appears nowhere else.**
- Phrase: "|S ∩ [x₀, x₀+q)| ≤ 0.1563 q + 2·1536 terms".
- Problems:
  - (a) 1,536 is not defined anywhere. The only discrepancies the page reports are 215 on [2·10⁶,10⁷] and 1,064 on [2·10⁷,10⁸], so a reader cannot connect 1,536 to them.
  - (b) Those discrepancies were measured "after the transient with the density refitted". The bound needs a deviation from the line 0.1563·x valid for *every* x₀ ≤ 5·10⁷, including the transient.
  - (c) The slope 0.1563 differs from the stated density 0.1562.
- Fix: one clause such as "where 1,536 bounds |S∩[1,x]| − 0.1563x … over all x ≤ 10⁸ (measured)", and explain why 0.1563 rather than 0.1562.

**10. P2: off-by-one or unstated indexing for the gap-word suffix.** [arith]
- Phrase: "the suffix of the gap word from term 7,810,617 (its last 7,810,617 terms)".
- Problem: 15,621,235 elements give 15,621,234 gaps. With 1-indexing, terms 7,810,617 through 15,621,234 are 7,810,618 terms. The parenthesis is only right with 0-indexing, but "a_7,810,617" reads as 1-indexed. P2 also says "at or before term 7,810,617" and then "i.e. before a_7,810,617", which mixes inclusive and exclusive.
- Fix: state the indexing convention once (for example "gap i = a_{i+1} − a_i, i ≥ 1") and use "at or before" in both places.

**11. P3: three window sizes are mixed in one sentence, and the bound does not fit its window.**
- Phrase: "The autocorrelation of the indicator on [2·10⁶, 10⁷] has record peaks … and no shift up to 40·10⁶ agrees better than 98.9%".
- Problem: [2·10⁶, 10⁷] is only 8·10⁶ long, so shifts up to 40·10⁶ cannot be measured on it. On [2·10⁷, 10⁸], where they can, the stated records only reach 95.8%, so "98.9%" does not belong to that window either.
- Fix: name the window and data for the 40·10⁶ statement, for example "on the full 10⁸ output, no shift up to 4·10⁷ agrees better than …".

**12. P3: agreement drops about 10 points between the two windows with no comment.**
- Phrase: "130 (86.3%) … 27,875 (95.8%)" on [2·10⁷, 10⁸] against "96.2% … 98.8%" on [2·10⁶, 10⁷].
- Problem: shift 130 goes from 96.2% to 86.3% and shift 27,875 from 98.8% to 95.8%. For a stationary rotation coding (and P3 stresses "the same arcs" on two windows) agreement at a fixed shift should not fall by 10 points. Either the metric changed between the two chains or the later window is markedly less rotation-like. The page says neither. 7,892 appears only in the second chain and is never explained.
- Fix: say whether "exact agreement" means the same thing in both chains, and comment on the drop and on 7,892.

**13. P3: 110,000 is a round number next to an exact one.**
- Phrase: "34 exceptions among 110,000 … 42 exceptions among 795,003".
- Problem: the integer count on arcs covering "11% of the circle" will not be exactly 110,000, while the next count is exact (795,003). A reader will ask whether 110,000 is rounded and whether 34 is then exact.
- Fix: give the exact count, or write "≈110,000".

**14. P6: the 94 doubling cycles are not fully accounted for, and "the fourteen four- and six-cycles" misleads.** [arith]
- Phrase: "50 because a mixed rail sum already lands on a rail (every cycle of length 8 or more — 36 of them — and the fourteen four- and six-cycles at M = 5, 9, …, 45), 29 by the solver — including all twelve three-rail cycles … and all six five-rail cycles".
- Problem: the named groups add up to 36 + 14 + 12 + 6 + 16 two-rail = 84 of 94. "The fourteen four- and six-cycles" reads as if there were only fourteen. Enumerating x, 2x, 4x, … mod M for M < 49 gives **24** four- and six-cycles: 15 four-cycles and 9 six-cycles. Ten of them go to the solver: M = 15 (two), 21 (two six-cycles), 30 (two), 42 (two six-cycles), 45 (two). The 29 solver cases are therefore 12 + 6 + 10 + the M = 3 two-cycle. None of this is visible on the page.
- Fix: "fourteen of the twenty-four four- and six-cycles", and "29 by the solver: the twelve three-rail cycles, the six five-rail cycles, the other ten four- and six-cycles (M = 15, 21, 30, 42, 45) and the two-rail cycle at M = 3".

**15. P6: the jump from 17 to 21 elements is not explained.**
- Phrase: "both three-cycles need |D| + 2|B| ≥ 17 — Li's own 7 + 2·5 — so within the model seed = D ∪ B ∪ (M + B) ∪ rails, his 21 elements are the fewest the architecture can produce".
- Problem: 7 + 5 + 5 = 17, so the rails must contribute 4 elements. With three rails a reader would expect 3, making 20. The minimum rail contribution that the conclusion needs is never stated or shown.
- Fix: say how many rail elements are needed and why (for example "plus at least four rail elements, the fewest that start an aperiodic controller"), or drop "the fewest".

**16. P6 and P8: "23 of 27 initial contents" does not fit the counting used two lines earlier.**
- Phrases: "aperiodic from 23 of 27 initial contents" against "q ≤ 1, 2 and 3 (16, 64 and 256 contents…)".
- Problem: two-rail contents are counted as 2^(rails·(q+1)), a power of 2. 27 = 3³ cannot arise that way for three rails. The reader cannot tell what the 27 initial contents are.
- Fix: one clause defining the 27, for example "the 27 Lemma-5 initial contents" if that is what they are.

## B. Labels, hedges, and title, URL or card promising more than the body

**17. URL: the slug claims more than the body.**
- Phrase: `/day/341-the-last-seed-in-12-is-not-periodic-through-1e8`.
- Problem: P2 states the exact scope (gap periods ≤ 3,905,308 terms with onset by term 7,810,617) and adds that "it says nothing about longer periods or later onsets". "Not periodic through 1e8" also suggests periods with later onsets or longer lengths within 10⁸ are excluded, and they are not.
- Fix: a slug such as `341-the-last-seed-in-12-no-short-period-through-1e8`, or `…-a-rotation-with-fuzzy-edges`.

**18. Card: "runs to 10⁸ without repeating" overclaims in the same way.**
- Phrase: "The six-element seed {1,4,8,10,11,12} runs to 10⁸ without repeating".
- Problem: same as 17. The card's own tag says "NO GAP PERIOD ≤ 3.9·10⁶ TERMS BEFORE 5·10⁷", which is much narrower.
- Fix: "is computed to 10⁸ and has no gap period of up to 3.9·10⁶ terms starting before 5·10⁷", or "shows no short period through 10⁸".

**19. Card: "a shape Li's counterexample machinery cannot produce" is stronger than anything in the body.**
- Problem: the body shows two things. First, E has no shield at m ≤ 400, which is a measurement. Second, a diagonal-gate shield with three or more rails needs M ≥ 49, which is a finite census labelled (d) of one mechanism. Neither says Li's machinery cannot produce a rotation-coding shape. P6's own label says "not a theorem about all mechanisms".
- Fix: "a shape unlike Li's shield-and-rails", which matches the Title's "nothing like".

**20. Title: things the body labels (c) or (d) are stated as plain fact.**
- Phrases: "what it does instead is a coding of a single rotation by a five-arc window, exact away from the arcs' edges" and "which a SAT census shows cannot exist for any cycle of three or more rails at any modulus below 49".
- Problem: the body gives the rotation coding as "Our reading, label (c)" (and see 5 on "exact"). The SAT result carries "Label (d): a finite census of one mechanism (diagonal-only gates)". The title drops both hedges and the restriction to diagonal-only gates.
- Fix: "…looks like a coding of a single rotation…" and "…which a SAT census of the diagonal-gate design rules out for three or more rails below modulus 49".

**21. P4: "reading", "conjecture" and the label are used inconsistently.**
- Phrases: "Our reading, label (c): … it is not eventually periodic." and then "If the conjecture is true…". P8: "Not claimed: that E is aperiodic (conjectured, (c))".
- Problem: the same statement is called a "reading" and a "conjecture". The brief treats these as different label words. The page never says what (a), (b), (c) and (d) mean, so a first-time reader cannot decode "(c)" or "(d)".
- Fix: pick one word, "Our conjecture, label (c)" or "Our reading", and use it throughout. Add a one-line key, or link to where the labels are defined.

**22. P4 and P8: irrationality of g is conjectured in one place and disowned in another.**
- Phrases:
  - (c) reading: "the greedy from E is an **irrational** rotation coding".
  - P8: "Not claimed: … that g is irrational".
  - P4: "The periodicity question and the irrationality of g are the same question".
- Problem: the (c) reading builds irrationality in, but the Not-claimed list gives it no "(conjectured, (c))" tag, unlike aperiodicity. "Are the same question" is stated as unlabelled fact, though it holds only under the (c) model.
- Fix: in P8, "that g is irrational (conjectured as part of (c); …)". In P4, "Under this reading, the periodicity question and the irrationality of g are the same question".

**23. P4: the "smallest counterexample" sentence relies on things outside the conjecture.**
- Phrase: "If the conjecture is true, the smallest counterexample seed by largest element drops from Li's [97] to [12]; by number of elements {3, 5, 8, 10, 13} below has five to E's six."
- Problems:
  - (a) The conjecture as stated is only about E, so it says nothing about {3,5,8,10,13}.
  - (b) "Smallest by number of elements" is checked only inside [14]. Seeds with ≤ 4 elements and a larger maximum were never censused.
  - (c) The second clause is grammatically broken.
- Fix: "If it is true, E would be the smallest counterexample by largest element (every seed inside [11] certifies). If {3,5,8,10,13} is also aperiodic, it would be the smallest found by number of elements among seeds inside [14]: five against E's six."

**24. P4: "None of the six" contradicts the page's own description of E.**
- Phrase: "None of the six is a rotation coding in the exact sense E is on its cores".
- Problem: P7's "six distinct resisting sequences" include E, and the paragraph has just named five others ({3,5,8,10,13} plus "Four more"). "None of the six … in the sense E is" either includes E, which is self-contradictory, or miscounts the others.
- Fix: "None of the other five…".

**25. P4: Calkin–Erdős is credited with more than the page quotes.**
- Phrase: "Calkin and Erdős proved exactly why a clean coding cannot do this alone: the interval codings {n : {nα} ∈ (1/3, 2/3)} are … never complete".
- Problem: as quoted, the result covers one family of interval codings. It is not a proof about clean codings in general, and E's window is five arcs, not (1/3, 2/3).
- Fix: "Calkin and Erdős showed the simplest instance of why a clean coding cannot do this alone: …".

**26. P5 heading: a firm claim on a (d) basis, and a broken construction.**
- Phrase: "Why Li's method cannot be the proof, and that no smaller Li-type seed exists."
- Problems:
  - (a) "Cannot be the proof" rests on measuring m ≤ 400 plus a census below 49 labelled (d). The body itself says "not a theorem about all mechanisms".
  - (b) "Why X, and that Y" is not parallel.
  - (c) "No smaller Li-type seed exists" is supported only by a MaxSAT run *at M = 49* (element count) and M ≥ 49 for three or more cycles. It says nothing about fewer elements at M > 49, or about a smaller largest element than 97 for other B at M = 49.
- Fix: "Why Li's shield is not what E is doing, and why no Li-type seed is smaller (within the diagonal-gate model at M = 49)".

**27. P6: the "[13]" bound does not match the rest of the page.**
- Phrase: "So for every cycle of length three or more, 49 is the least modulus; a seed inside [13] is out of Li's reach."
- Problem: no reason is given for 13. The page's own census goes to [14]. A Li-type seed needs M ≥ 49 with B nonempty (|D| + 2|B| ≥ 17), so its M + B elements exceed 49, which implies a much larger bound. A reader cannot tell where [13] comes from.
- Fix: state the bound that follows and why (for example "no seed inside [49] can be Li-type"), or explain 13. Possibly [12] (E) or [14] (the census) was meant.

**28. Chips against P8: the status chip says OPEN, the body says Li settled the problem.**
- Phrases: "Community database OPEN as of 2025-08-31" and P8 "anything about the problem's status, which Li settled". P1 also has "Zhiheng Li answered no in August 2026".
- Problem: a reader sees "OPEN" dated a year before Li's disproof, next to text saying the problem is settled.
- Fix: annotate the chip, for example "database still says OPEN (last updated 2025-08-31); disproved by Li, August 2026, see our 13 October referee entry".

**29. P3 and P6: shield-looking census at "the convergent denominators" contradicts the m ≤ 400 measurement.**
- Phrases: "At those moduli the residue census of course looks like a shield" (P3) and "at the moduli where its census looks shielded (the convergent denominators of g)" (P6).
- Problem: the convergent denominators include 3, 4, 7, 123, 130, 253 and 383, all ≤ 400. At those moduli P3 says every class holds 0.83–1.18 of the mean. At 8,528, also a convergent, the classes range from 0.44 to 1.67 with none empty. Only at 31,821 is anything empty.
- Fix: "at the large convergent denominators (31,821 in our range)…".

**30. P6 against P3: the shield bound ≤ 400 is weaker than what P3 measured.**
- Phrase: "E has no shield at any modulus ≤ 400 by measurement".
- Problem: P3 also reports that over [10⁷, 10⁸] no class mod any m ≤ 10,000 is empty and the fullest is 1.67× the mean. That rules out both permanently-out and permanently-in classes up to 10,000. Citing only 400 leaves the reader wondering why the stronger number was dropped.
- Fix: "no shield at any modulus ≤ 10,000 (no empty class; none above 1.67× the mean) on [10⁷, 10⁸]", or explain why only 400 counts.

**31. P8: "Not claimed: that no mechanism other than Li's could prove it" says something else.**
- Problem: read literally, it disclaims "only Li's mechanism could prove it". The page has just argued Li's mechanism *cannot* apply, so this is confusing or inverted. The intended disclaimer, matching P6's "a controller fed by mixed rail sums is an architecture nobody has tried", seems to be that no *other* mechanism could prove aperiodicity, or produce E.
- Fix: "Not claimed: that no other mechanism (for example a controller fed by mixed rail sums) could produce or prove E's behaviour."

**32. P7: "zero tool errors" against the crash reported in P8.**
- Phrases: P7 "with an all-future certificate, zero tool errors" against P8 "a seed whose certificate fell inside its own range crashed certify.py, and the first census driver read the crash as 'unresolved' … a false survivor for twenty minutes".
- Fix: "zero tool errors in the final (fixed) run".

**33. Card: "GAP FOUND IN A FIRST DRAFT" is ambiguous and undercounts.**
- Phrase: "HOSTILE REFEREE: GAP FOUND IN A FIRST DRAFT, FIXED; HOLDS WITH FIXES".
- Problems:
  - (a) On a page where "gap" means a difference of consecutive terms (as in "NO GAP PERIOD" in the same card), "GAP FOUND" can be misread as a term gap.
  - (b) The body lists several referee catches: the 4f₁ + 9f₂ relation, the f₁ + 2f₂ − 2f₄ relation for {3,5,8,10,13}, the census-driver crash fix, and the independent encoder.
- Fix: "HOSTILE REFEREE: THREE ERRORS IN A FIRST DRAFT (A MISSED FREQUENCY RELATION, …), FIXED".

**34. Unlabelled claims of different kinds.**
- Problem: "All of this is computation, label (d)" covers P2 only. Three other blocks carry no label:
  - P3's spectrum and phase measurements;
  - P7's census, which contains actual proofs (finite certificates for 16,376 seeds) and so differs in kind from the (d) measurements;
  - the P4 sentences "E is a greedy extension that is a rotation coding except on edge zones … the price of completeness" and the random-walk explanation of discrepancy growth, which are interpretation.
- Labels (a) and (b) never appear, although the certificates are proofs.
- Fix: label P3 and P7 explicitly. Give the certified-periodic results their proof label. Mark interpretive sentences "(our reading)".

## C. Notation, definitions, cross-references

**35. Notation overloads: N, q, m, f₁ and f₂.**
- N is the certificate onset in P1 ("2N + q − 2") and the run length in P2 ("truncated at N − t").
- q is a period (P1, P2), a denominator ("p/q", P4), and a rail position ("Y_i[q]", "content on q ≤ 1, 2, 3", P5–P6).
- m is a census modulus ("m ≤ 400") and a multiplier ("m·g, |m| ≤ 82").
- f₁ and f₂ are E's top two frequencies (P3), then reused for {3,5,8,10,13}'s generators in "f₁ + 2f₂ − 2f₄ … among a first draft's three". That phrase names three generators f₁, f₂, f₄ with no f₃, and t is never defined.
- Fix: define N at first use ("onset N") and use L for the run length. Use another letter for rail positions (for example Y_i[k]). Rename the other seed's frequencies (h₁, h₂, h₃) and explain or remove the "f₄".

**36. P1 and P2: "both rules" is used before it is defined.**
- Phrase: "on Li's seed to 10⁷ under both rules".
- Problem: the problem statement defines only the equal-indices rule. "Both rules" (equal vs distinct, Dickson vs Queneau) is decoded only later via "the equal/distinct flag". More importantly, the page never says **which rule E's 10⁸ run, spectrum and census use**, or whether the [13]/[14] census was run under one rule or both.
- Fix: "under both rules (equal indices allowed, as in the statement, and distinct indices, Queneau's variant)". State once that E's results are for the equal-indices rule, if so.

**37. P7 and P8: the positive control's period is quoted two ways.**
- Phrases: P7 "{1, 2, 7, 8, 10, 11, 12} (period 2,039 from 95,787)" against P8 "(the July-certified {1, 2, 7, 8, 10, 11, 12}, gap period 204)".
- Problem: P7's "period" is unqualified, so a reader sees 2,039 and 204 for the same seed.
- Fix: "membership period 2,039 (204 gaps) from 95,787" in P7, and "gap period 204 (membership period 2,039)" in P8.

**38. P3 against P8: sidelobes are "excluded" but still appear among the 40 largest peaks.**
- Phrases: P3 "36 of the 40 largest … the other four are three window sidelobes and one stray" against P8 "Spectrum: … sidelobes excluded".
- Fix: say which statement applies where, for example "sidelobes excluded from the generator search; three remain among the 40 largest raw peaks".

**39. P3 against P8: multipliers go up to 82, but the relation search stops at 50.**
- Phrases: "integer multiple m·g mod 1 (|m| ≤ 82 …)" against "integer relations among candidate generators searched to coefficients 50".
- Problem: a peak at, say, 82g amounts to a relation with coefficient 82, beyond the stated search bound. A reader will ask whether the ≤ 50 search could have found it.
- Fix: say the |m| ≤ 82 identification was a separate one-generator fit, or raise the stated bound.

**40. P3: g has more digits than the formula that defines it.** [arith]
- Phrase: "g = −f₁ − 2f₂ = 0.28459193622".
- Problem: with the printed 9-decimal f₁ and f₂, −f₁ − 2f₂ = 0.284591936. The trailing "22" cannot come from the displayed formula. Separately, ‖31,821g‖ on this g is about 2.5·10⁻⁶, which the page gives as "≈ 2·10⁻⁶".
- Fix: "g ≈ −f₁ − 2f₂, refined to 0.28459193622 by …". Optionally write ‖31,821g‖ ≈ 2.5·10⁻⁶.

**41. P8 against P6: Li's lemma numbering is inconsistent.**
- Phrases: "his Lemma 3.1 conditions" (P6 and Sources) against "Lemma-5 seeds" (P8).
- Problem: the two numbering styles do not match and "Lemma-5 seeds" is never defined.
- Fix: one clause defining "Lemma-5 seeds", with the matching numbering style.

**42. P2 against P8: the number of byte-identical runs is unclear.**
- Phrases: P2 "byte-identical to the old one on E to 2·10⁶ and 10⁷ and on Li's seed to 10⁷ under both rules" against P8 "four byte-identical runs".
- Problem: if "under both rules" applies to every item there are 6 runs; if only to Li's seed, 4.
- Fix: list the four runs explicitly in one place.

**43. P4: a measurement scope is unclear.**
- Phrases: "agreement never above 98.5% through 10⁷" and "never higher through 3.3·10⁶" (for {4,6,8,9,10,13,14}).
- Problem: it is unclear whether "through" refers to shifts or data range. The 3.3·10⁶ also departs from the "through 10⁷" scope used for the other five, with no reason given.
- Fix: "for shifts up to …, on data through …", and explain the shorter scope for {4,6,8,9,10,13,14}.

## D. Grammar, typos, broken constructions

**44. P2: the appositive is attached to the wrong noun.**
- Phrase: "reproduces the July report's SHA-256 of the membership bits through 500,000 (3a045efe…, a pure-Python big-integer generator)".
- Problem: the parenthesis calls the hash a generator.
- Fix: "(3a045efe…, computed by the July report's pure-Python big-integer generator)".

**45. P4: "26 of its 40 largest peaks and 67% of its variance" has no verb.**
- Problem: the sibling items say "holding 36 of its 40 largest peaks and 75% of the variance".
- Fix: insert "holding" before "26".

**46. P7: word choice.**
- "the slowest with membership period 743" should read "the longest membership period, 743".
- "four rows resist" should read "four seeds resist". "Rows" is spreadsheet jargon and is mixed with "seeds" in the same sentence.

**47. P1: "no modulus q ≤ 20,000 is a period".**
- Problem: calling a period a "modulus" collides with the residue-class moduli (M, m) used later.
- Fix: "no period q ≤ 20,000 begins at or before 479,993".

**48. P8: number disagreement in "are detected from the right suffixes and not from the wrong one".**
- Fix: "not from the wrong ones".

**49. P8: "Spectrum: peaks located exactly on the element set (no interpolation)" is unclear.**
- Fix: "peak frequencies evaluated exactly (direct sums over the elements, no FFT interpolation)", or whatever is meant.

**50. P3: the near-periods are not "the continued fraction".**
- Phrase: "The near-periods are the continued fraction of g".
- Problem: they are the convergent denominators of g's continued fraction, and given 2 and 3 above, only some of them.
- Fix: "The near-periods include the convergent denominators of g = [0; 3, 1, 1, 17, …]".

**51. P4: "Four more … with the same signature" is unclear.**
- Problem: it follows straight after {3,5,8,10,13} was called "a different animal" from E, so the reader cannot tell which signature is meant: E's, or {3,5,8,10,13}'s rank-two one.
- Fix: "with the same coarse signature (no rail, sharp spectrum, an unclosed ladder)".

**52. P4: "a third of random" is generous.** [arith]
- Phrase: "1,064 … where random sets give 2,174–3,482 — a third of random".
- Problem: the ratio is 0.31–0.49, and 0.20–0.45 on the earlier window.
- Fix: "a third to a half of random".

**53. P4, low priority: "gaps mostly 1 and 3" sits oddly with the stated density.**
- Phrase: "{2, 6, 8, 9, 10, 11, 14} (gaps mostly 1 and 3, density 0.1646".
- Problem: density 0.1646 means a mean gap of about 6.1, so if most gaps are 1 or 3 the rest must average well above 10. A reader may suspect a typo. Same pattern, more mildly, for "gaps mostly 11" with density 0.1189 (mean gap ≈ 8.4).
- Fix: give shares (for example "41% ones, 22% threes"), as P3 does for E.

**Checks that came out consistent:**
- 4f₁ + 9f₂ ≈ 3; f₁ ≡ −9g and f₂ ≡ 4g.
- The convergent-denominator list matches the stated partial quotients.
- 4,095 = 2¹² − 1; 4,096 and 8,192 seed counts.
- 50 + 29 + 15 = 94; 316 + 4 = 320.
- 7 + 2·5 = 17; 16, 64, 256 contents.
- 2·677,409 + 87,921 − 2 = 1,442,737 < 2·10⁶.
- p(100) share ≈ 8.07%.
- 11% + 79.5% + 9.5% = 100%; 0.11 + 0.095·0.487 ≈ 0.156, the density.
- The near-period sums for the other seeds (110 + 1,393, 145 + 560, 705 + 1,934).
- 297,128 = 594,256/2; 3,905,308 = ⌊7,810,617/2⌋.
- The SHA is 64 hex digits.
- 3,905,308 and 7,810,617 are quoted identically throughout.
- "20,000 and 479,993" match P1.
- 23-of-27 is quoted identically twice.
- The HTML entities (&#39;, &middot;, &quot;) are single-escaped and render correctly in a browser. The literal "&#39;" in render_*.txt is only an artefact of the text extraction.
