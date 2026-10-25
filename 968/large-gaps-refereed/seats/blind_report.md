# Blind read: #968 /day/ entry (entry_rendered.txt), 2026-10-21

I am the blind seat. I checked the text against the printed paper (TeX plus O_work/paper_layout.txt), the bundle README and its files, the O/T/L/W reports, main_reading.md, the live pages, the two Erdős scans, the Lean source and the entry tooling. Each item gives the quote, what is wrong, a suggested fix and a tag.

**Totals: FACT 22 · OVERCLAIM 4 · CONSISTENCY 6 · STYLE 8 (40 items).** The items are ordered by importance.

---

1. **CONSISTENCY (ships broken).** Homepage card tag: "… STATEMENT MATCHED · @@HEADREAD@@ · OURS: …"
   - **Problem.** The placeholder is in the rendered card, and the splice script will publish it as is.
     - `apply968.py` replaces `@@…@@` tokens only in the entry string `e`. It then pastes `vals['HEADLINE']` into `HEADLINES` raw (`once('const HEADLINES = [\n', … + vals['HEADLINE'])`).
     - Its leftover-token assert checks only `e`.
     - `smoke968.mjs` checks `/` only for the slug, so it passes with `@@HEADREAD@@` on the homepage.
   - **Fix.** Inline the text (`READ LINE BY LINE + THREE HOSTILE AI SEATS: HOLDS AS READ`, but see item 5), or run the substitution loop over `HEADLINE` too. Then assert `'@@' not in s` before writing, and add a smoke check that `/` does not contain `@@`.

2. **FACT (our checks).** "The proof is 56 modules (22,533 lines, 1,238 theorems and lemmas) …"
   - **Problem.** No source supports 1,238.
     - Seat L counts 1,118 `theorem` + 175 `lemma` = 1,293 ("~1,290 lemma proofs").
     - A grep of the 56 files confirms 1,293: 1,062 plain `theorem`, 55 `@[simp] theorem`, 1 `private theorem`, and 175 `lemma`.
     - A column-0 grep that drops the attributed and private declarations gives 1,237, which is probably where the near-miss came from.
   - **Fix.** "(22,533 lines; 1,118 theorems and 175 lemmas)", or "1,293 theorems and lemmas".

3. **FACT (our checks).** T paragraph: "OpenAI's Lean has the same constant."
   - **Problem.** The Lean's constant is not the same.
     - T finding 10: `unorderedWeight_detector_bound` concludes `≤ (lam + lam^2 * l2Mass g^2 + 1) * familyW`.
     - L finding 6: D = λ + λ²(∫g²)² + 1 and ε = λ²/(16D).
     - So the Lean has the same squared c_G but a different constant (K_λ + 1) and a different ε.
   - **Fix.** "OpenAI's Lean has the same squared c_G; its detector constant is λ + λ²c_G² + 1, and it takes the smaller ε = λ²/(16(λ + λ²c_G² + 1))."

4. **FACT (primary source).** "… proves it for the decreases on the spot, and ends: "Es scheint schwierig zu sein, …""
   - **Problem.** That sentence is not the end of the paper. The p. 256 scan (ep-6.png) continues after it:
     - "Eine andere Frage wäre, ob es unendlich oft vorkommen kann, daß p_k/k > p_{k+1}/(k+1) > p_{k+2}/(k+2)";
     - a "Schließlich bemerken wir …" paragraph on Satz 2;
     - then "Eingegangen am 9. 1. 1961".
   - **Fix.** "…, proves it for the decreases on the spot, and then says: …"

5. **OVERCLAIM (could read as human verification).** Summary: "We read all five sections line by line, and three hostile AI referee seats, two on the mathematics and one on the sources, found no gap either." Card title: "…read line by line here". HEADREAD: "READ LINE BY LINE + THREE HOSTILE AI SEATS".
   - **Problem.** The "we" who read line by line is the main seat (Claude Opus 5.5, per main_reading.md and the receipts). Set against "AI referee seats … either", the summary invites the reader to take "we" as human. The body says otherwise only in the last paragraph. This matters on a site whose readers apply erdosproblems.com's human-verification bar.
   - **Fix.** Summary: "Our main reading seat (Claude Opus 5.5) read all five sections line by line and found no gap; three further hostile AI seats, two on the mathematics and one on the sources, found none either." Card: "READ LINE BY LINE BY AN AI SEAT + THREE HOSTILE AI SEATS: HOLDS AS READ".

6. **CONSISTENCY / FACT (numbers).** Card line: "Up to 10⁹ the share of increases stays between 39.7% and 42.1%."
   - **Problem.** This is false below 10⁶. In run_2.3e10.log, N = 10³ gives 47.5%, 10⁴ gives 44.6% and 5·10⁴ gives 43.6%. The summary correctly says "at every checkpoint from 10⁶ to 10⁹".
   - **Fix.** "At ten checkpoints from N = 10⁶ to 10⁹ the share of increases stays between 39.7% and 42.1%."

7. **OVERCLAIM.** Card: "(THE BEST KNOWN THRESHOLD WAS 0.579)". World paragraph: "The strongest earlier unconditional result is the one the paper names, Theorem 5 of Bazzanella, Languasco and Zaccagnini …"
   - **Problem.** Seat W left this open. It did not check whether a later twin-prime sieve constant (Wu 2004), if uniform in the shift, would give about 2/3.3996 ≈ 0.588 by BLZ's argument. W also notes that "The paper itself never claims 0.579 is the best known; COMMON.md does." The summary hedges ("we know of"); the card and the world paragraph do not, and the latter attributes a "strongest" claim to the paper.
   - **Fix.** Card: "(THE BEST THRESHOLD WE KNOW OF WAS 0.579)". World: "The strongest earlier unconditional result we found is the one the paper cites, …; we did not check whether later sieve constants push BLZ's 0.579 slightly higher (W: perhaps ≈ 0.588)."

8. **FACT (paper) / CONSISTENCY.** Lean label: "…and on the way proves the Siegel–Walfisz and Bombieri–Vinogradov theorems, which the paper assumes and Mathlib lacks".
   - **Problem.** The paper never mentions Siegel–Walfisz: there are zero hits for "Walfisz" or "Siegel" in the TeX and the layout. Its only quoted input is BV (Lemma 5.2). The summary has this right ("the paper assumes Bombieri–Vinogradov").
   - **Fix.** "…and on the way proves Bombieri–Vinogradov (which the paper assumes) from a proof of Siegel–Walfisz; Mathlib has neither."

9. **CONSISTENCY.** The body contradicts itself on the number of prime number theorem uses.
   - The Lean section says: "The Lean replaces both of the paper's uses of the prime number theorem with Chebyshev's bounds from Mathlib".
   - The reading section says: "All three uses of the prime number theorem (the corollary, the passage from X to N, and Q ≤ h^1/2 in Lemma 5.4) need only Chebyshev's bounds, which is what the Lean uses."
   - **Problem.** It is three uses. The third is in Lemma 5.4's proof: "The prime number theorem gives Q ≤ h^{1/2}". The Lean covers that one with `primorial_le_four_pow` (BoxMeans.lean:269).
   - **Fix.** "The Lean replaces all three of the paper's uses of the prime number theorem with Chebyshev-type bounds from Mathlib; in particular its corollary takes C = 2/log 2 …"

10. **FACT (paper).** "Cauchy–Schwarz gives a weighted proportion of starts with a prime in J, and almost all of that weight has no prime in I."
    - **Problem.** The paper chooses ε = λ²/(2K_λ) against a lower bound λ²/K_λ, so Δ = λ²/(2K_λ). At least half of the weight survives, not "almost all".
    - **Fix.** "…, and at least half of that weight has no prime in I (the paper takes ε = λ²/(2K_λ))."

11. **OVERCLAIM (number theory; a universal).** "its N_0(C) is also ineffective, as for any argument through Bombieri–Vinogradov, which rests on Siegel's theorem."
    - **Problem.** This is not true of every argument through BV. GPY/Maynard-type sieve arguments are routinely made effective by using an effective BV that excludes the multiples of at most one exceptional modulus (Landau–Page). Ineffectivity belongs to this proof as written, which quotes BV with arbitrary log-power savings. The paper says nothing about effectivity.
    - **Fix.** "As written, the proof gives an ineffective N_0(C): it quotes Bombieri–Vinogradov with arbitrary log-power savings, whose standard proof uses Siegel's ineffective theorem. Whether an effective variant suffices here, we did not check."

12. **CONSISTENCY.** Card: "ERDŐS AND PRACHAR, 1961–62: DOES p_n/n INCREASE ON A SET OF POSITIVE DENSITY?" Body: "The page reads "positive density" as positive lower density, as Erdős most likely meant."
    - **Problem.** The entry's own world section says Erdős and Prachar asked "explicitly for lower density" (untere Dichte, p. 256), so the hedge is settled. The card asks a different question from the one in the 1961 paper, and the body repeats the hedge before refuting it.
    - **Fix.** Card: "…ON A SET OF POSITIVE LOWER DENSITY?" Body: "The page reads "positive density" as positive lower density; the 1961 paper asks for exactly that (below)."

13. **CONSISTENCY (bundle claims).** The entry promises bundle contents that are not there yet.
    - "its step-by-step notes are in the bundle"
    - "The seat's table, mapping each printed statement to its declaration, is in the bundle."
    - "…are in the bundle's seats/MODEL_RECEIPTS.txt"
    - The bundle link label: "…the paper-to-Lean table, referee reports, and the model receipts".
    - **Problem.**
      - `verification/968/large-gaps-refereed/seats/` and `entry/` are currently empty.
      - The README still contains the literal `@@SEATS_README@@`.
      - I ran `receipts.sh`: 11 rows, 0 other-model strings, so the claim itself holds. But the file it names does not exist yet.
    - **Fix.** Before publishing:
      - copy main_reading.md, the O/T/L/W reports and briefs, and the receipts output (as MODEL_RECEIPTS.txt) into `seats/`;
      - copy the entry files into `entry/`;
      - fill `@@SEATS_README@@`;
      - grep the bundle for `@@`.

14. **FACT (our checks).** Two checks are described as exact when they were floating-point.
    - O: "It checked the prime-deletion identity (8) in exact integer arithmetic … the two sides agree to 2·10⁻¹⁶". `v2_identity8.py` uses `random.uniform` coefficients for F_j. The divisors and Möbius values are exact; the test functions are floats. A 2·10⁻¹⁶ residual is itself evidence that this is not exact arithmetic.
    - T: "exact numerics on 400 random patterns, collisions included, agree to 4·10⁻¹⁵". `fourier_check.py` is numpy floating point.
    - **Fix.** O: "…checked (8) directly from the definition of the divisor sums (exact divisors and Möbius values, random real test functions), at twelve events…" T: "floating-point numerics on 400 random patterns … agree to 4·10⁻¹⁵."

15. **FACT (our checks).** "The hypothesis B ≥ 1 is genuinely needed, for the tail of the Euler product beyond the largest shift difference."
    - **Problem.** T's finding is weaker. T says it is "genuinely used here; B < 1/2 would break it": the tail is 1 + O(L^{-B}), which needs B ≥ 1/2 to beat L^{-1/2}. Lemmas 5.2–5.3 allow B ≥ 0. Nothing shows B ≥ 1 is necessary.
    - **Fix.** "The hypothesis B ≥ 1 is really used: the Euler-product tail beyond the largest shift difference is O(L^{-B}), and B < 1/2 would lose the printed rate."

16. **FACT (our checks).** "Otherwise the Lean follows the printed construction parameter for parameter: τ = 1/8, λ = C + 1, …" and "The differences are of exposition."
    - **Problem.** L's own map shows three more differences:
      - ε = λ²/(16D) rather than λ²/(2K_λ);
      - the detector constant has an extra +1;
      - W = Z² is not normalised by w.
      These are harmless, but "parameter for parameter" is contradicted by the seat's own table.
    - **Fix.** "Otherwise the Lean follows the printed construction: τ = 1/8, λ = C + 1, …; it takes a smaller ε and a detector constant one larger, and does not normalise W. These and the following differences are of exposition."

17. **FACT (number theory).** "It never proves a zero-free region. It proves lower bounds |L(σ + it, χ)| ≥ c·((q + 2)(|t| + 2))^−ε for 1 ≤ σ ≤ 2, …"
    - **Problem.** A lower bound on Re s ≥ 1 is non-vanishing there, which is the trivial zero-free region; the Lean file is even named ZeroFreeBounds.lean. What the proof avoids is a de la Vallée Poussin region to the left of Re s = 1. The constant c depends on ε, which the sentence omits.
    - **Fix.** "It proves no zero-free region to the left of Re s = 1. Instead, for every ε > 0 it proves lower bounds |L(σ + it, χ)| ≥ c(ε)·((q + 2)(|t| + 2))^−ε on 1 ≤ σ ≤ 2, …"

18. **FACT (number theory; a seat's heuristic stated as fact).** "So the argument would run for any such set with that level of distribution, and it meets no parity obstruction."
    - **Problem.** This is seat O's heuristic, and as stated it is too broad. The marked moment (Lemma 5.3) uses moduli q ≤ X^{1/4} and needs the marked integer to avoid 0 mod p for every p | q. An X^{1/8}-rough set does not do that for p in (X^{1/8}, X^{1/4}], so the local factors change and the run is not verbatim. "level 1/4 (Bombieri–Vinogradov)" can also be misread as BV's level being 1/4.
    - **Fix.** "Seat O's heuristic: the prime input is used only at level 1/4, half the Bombieri–Vinogradov range, and only through upper-bound-type suppression plus one asymptotic. So a suitably rough set with prime-like local densities and that level of distribution should behave the same way, and the method should not meet the parity barrier. We have not checked this."

19. **FACT (our numbers; interpretation unsupported).** "It moves in steps rather than drifting, which is what one expects when the threshold p_n/n passes an even number, …"
    - **Problem.** Ten cumulative checkpoints cannot show steps. Of the four even crossings in range, two coincide with a rise in the cumulative share:
      - 16, crossed between 10⁶ and 2.5·10⁶ (p_n/n 15.49 → 16.46): share 40.61% → 40.87%;
      - 22, crossed between 2.5·10⁸ and 5·10⁸ (21.35 → 22.07): share 39.67% → 40.19%.
      The 18 example is real.
    - **Fix.** "Since every gap after the first is even, the local rate of increases drops each time p_n/n passes an even number. The cumulative share responds slowly; it falls from 42.13% to 40.03% as p_n/n passes 18 between N = 10⁷ and 2.5·10⁷."

20. **FACT (our checks).** Summary: "Our own sieve to 2.3·10¹⁰, checked by a second implementation, finds p_n/n increasing at between 39.7% and 42.1% of indices at every checkpoint from 10⁶ to 10⁹."
    - **Problem.** CROSSCHECK.txt compares the two implementations at 4 of the 10 checkpoints (10⁶, 10⁷, 10⁸, 10⁹). The minimum, 39.67%, is at 2.5·10⁸, which only the first sieve reports.
    - **Fix.** "Our own sieve to 2.3·10¹⁰ (matched exactly by a second implementation at N = 10⁶, 10⁷, 10⁸, 10⁹) finds p_n/n increasing at between 39.7% and 42.1% of indices at all ten checkpoints from 10⁶ to 10⁹."

21. **FACT (sources).** "They are not the first in Lean: a public repository, kimihiro64/bombieri-vinogradov …"
    - **Problem.** "They" covers five results: the large sieve, Pólya–Vinogradov, Siegel's bound, SW and BV. agentA documents prior Lean BV, SW, the large sieve and a Siegel gap, but not Pólya–Vinogradov. kimihiro's BV (π-form, moduli ≤ x^θ, θ < 1/2) is also weaker than OpenAI's endpoint range x^{1/2}(log x)^{-b}.
    - **Fix.** "Bombieri–Vinogradov (in the range x^θ, θ < 1/2), Siegel–Walfisz and the large sieve are not new to Lean: …"

22. **FACT (our checks).** "Our Lean seat checked that both definitions are the standard statements and are not vacuous."
    - **Problem.** L calls the BV definition "the standard endpoint BV … It has no max over y ≤ x, so it is weaker than the textbook statement".
    - **Fix.** "…checked that both definitions are faithful (BV in its endpoint form, the one the paper cites) and are not vacuous."

23. **FACT (attribution).** "Rosser's bound p_n < n(log n + log log n) covers n ≥ 6"
    - **Problem.** That upper bound is Rosser–Schoenfeld (1962), as main_reading.md says. Rosser (1938) is the lower bound p_n > n log n.
    - **Fix.** "the Rosser–Schoenfeld bound p_n < n(log n + log log n) covers n ≥ 6".

24. **FACT (paper).** "The letter B names three different things."
    - **Problem.** Seat O counted only §§2–4: V_B and B_X, B_R in Lemma 4.1, and g's support endpoint in Prop 4.2. §5 adds the shift exponent "|a_i| ≤ DL^B, where D > 0 and B ≥ 1". The entry itself discusses that B two sentences earlier.
    - **Fix.** "The letter B names at least four different things (an interval label, B_R in Lemma 4.1, an endpoint of supp g, and the shift exponent in Proposition 5.1)."

25. **CONSISTENCY.** "The theorem's type and all six definitions it unfolds through (the prime indexing Nat.nth Nat.Prime (n − 1), the set of large-gap indices, the counting function, the lower density, the set of ratio increases) …"
    - **Problem.** It says six but lists five. The README's six are prime, largeGapIndices, primeAt, initialCount, lowerAsymptoticDensity and ratioIncreaseIndices; `primeAt` is missing.
    - **Fix.** Add `primeAt` with a gloss, or say "the six definitions it unfolds through (prime, primeAt, largeGapIndices, initialCount, lowerAsymptoticDensity, ratioIncreaseIndices)".

26. **FACT (paper).** "It takes f_j = … on the r = ⌊√k⌋ levels just below a large k"
    - **Problem.** The active levels are a = k − r + 1 ≤ j ≤ k, which includes k itself.
    - **Fix.** "on the r = ⌊√k⌋ levels k − r + 1, …, k".

27. **FACT (paper).** "…a one-dimensional profile g with ∫g² = 1, ∫g = √λ and a small first moment"
    - **Problem.** Lemma 4.1's small quantity is μ_g = ∫u·g(u)² du, the mean of the density g². It is not the first moment of g.
    - **Fix.** "…and a small mean μ_g = ∫u·g(u)² du".

28. **FACT (statement).** Lean label: "OpenAI's own Lean proves Theorem 1.1 (for every C > 0, at least c(C)·N of the indices n ≤ N have p_{n+1} − p_n > C·log p_n) …"
    - **Problem.** It drops "for every N ≥ N_0(C)". The bound is not claimed for small N.
    - **Fix.** "(for every C > 0 there is c(C) > 0 with at least c(C)·N of the indices n ≤ N having p_{n+1} − p_n > C·log p_n, for every large N)".

29. **FACT (paper).** "…while a detector bound E(Z²V_J²) ≤ (λ + λ²c_G²)·w holds with a constant independent of k."
    - **Problem.** Display (7) is a lim sup as X → ∞, not an inequality at each X.
    - **Fix.** "…while a detector bound lim sup E(Z²V_J²) ≤ (λ + λ²c_G²)·w holds …"

30. **FACT (our checks).** "The seat searched arXiv math.NT from January 2025 to 21 October 2026 (8,279 records), …; it could not search the Lean Zulip."
    - **Problem.** The 8,279-record listing ends on 20 October; 21 October was covered by the HTML new-listing page only. W also lists X/Twitter, Reddit and Chinese-language forums as not searched.
    - **Fix.** "…arXiv math.NT from January 2025 to 20 October 2026 (8,279 records) plus the 21 October new listing, …; it could not search the Lean Zulip, X or Reddit."

31. **FACT (our checks).** "T's one remark: Proposition 5.1 says …"
    - **Problem.** T reports "two exposition-level remarks". The second, that Chebyshev suffices for Q ≤ h^{1/2}, appears later under "Exposition notes".
    - **Fix.** "T's main remark: …"

32. **OVERCLAIM (minor).** Card: "OURS: A KERNEL-CHECKED BRIDGE TO FORMAL CONJECTURES' erdos_968"
    - **Problem.** The bridge proves a verbatim copy in OpenAI's environment (Lean 4.34.1), not FC's own constant. The body says so; the card does not.
    - **Fix.** "OURS: A KERNEL-CHECKED BRIDGE TO A VERBATIM COPY OF FORMAL CONJECTURES' erdos_968".

33. **STYLE (ambiguous "it").** "…never argues that the choice does not matter. It does not: apply (13) to one fixed admissible set of shifts."
    - **Problem.** "It does not" can be read as "the proof does not argue it".
    - **Fix.** "The choice does not in fact matter: apply (13) to one fixed admissible set of shifts."

34. **STYLE.** "The paper quotes the Bombieri–Vinogradov theorem, in the endpoint form recorded by Bombieri, Friedlander and Iwaniec, and proves everything after it. The Lean proves it."
    - **Problem.** "Everything after it" is vague. The paper also quotes standard facts such as PNT and Chebyshev. The two "it"s have different referents.
    - **Fix.** "The paper's one non-elementary input is the Bombieri–Vinogradov theorem, quoted in the endpoint form recorded by Bombieri, Friedlander and Iwaniec. The Lean proves that theorem too."

35. **STYLE / precision.** "(quadratic_siegel, through the product of three L-functions)"
    - **Problem.** The auxiliary series is ζ(s)L(s,χ)L(s,ψ)L(s,χψ): `biquadraticCoefficients = zeta * χ * ψ * (χ.pmul ψ)`. The lower bound is on the product of the three L-values at s = 1.
    - **Fix.** "(quadratic_siegel, via the classical product ζ(s)L(s,χ)L(s,ψ)L(s,χψ))".

36. **STYLE.** "a subset count printed as "2MR − 1" in (26)"
    - **Problem.** The garbled count is in the sentence justifying (26) ("there are at most 2^M − 1 subsets"), not in display (26).
    - **Fix.** "a subset count printed as "2MR − 1" in the justification of (26)".

37. **STYLE (completeness).** "This is Erdős problem #968." The card has kind: "solved".
    - **Problem.** erdosproblems.com/968, and FC's file, also carry Erdős's side question: are u_n < u_{n+1} < u_{n+2} and u_n > u_{n+1} > u_{n+2} infinitely often? FC marks both solved from the literature (Ford–Maynard–Tao 2018; Maynard 2015). The entry never mentions this, so a reader of the page may ask "what about the rest?".
    - **Fix.** Add one sentence to "The problem": "The page also asks whether u_n < u_{n+1} < u_{n+2} and u_n > u_{n+1} > u_{n+2} hold infinitely often; FC records both as already settled (Ford–Maynard–Tao's chains of large gaps; Maynard's bounded gaps), and neither the paper nor its Lean addresses them."

38. **STYLE.** "This bounded multiplicity is what rules out Tao's obstacle: …"
    - **Problem.** Multiplicity does not rule out the scenario; it makes the count immune to it. The theorem is what rules the scenario out.
    - **Fix.** "This bounded multiplicity is what defeats Tao's obstacle: …"

39. **STYLE (length).** 41 sentences run past 35 words. The worst:
    - **Title, about 58 words.** Suggest: "#968: for every fixed C, a positive proportion of prime gaps exceed C·log p, so p_n/n increases on a set of positive lower density — OpenAI's proof, read and replayed here".
    - **Lean label, about 100 words in one sentence.** Split after "Mathlib lacks" and after "under pp.all".
    - **"Ten were checked at the cited place, …" (about 78 words).** End the sentence after "say what the paper says." and list the ten in a second sentence.
    - **"Erdős and Prachar's paper (…) asks explicitly …" (about 72 words).** Split before the quotation.
    - **"The predicate reproduces all 10,000 terms …" (about 71 words).** Make three sentences: the reproduction, the two failing mutants, and the equivalent mutant with its one-line reason.
    - **Others over 55 words.**
      - "In 1965 Erdős wrote: …" (61 words).
      - "A second implementation, written separately in numpy …" (59 words): move the 10⁹ counts to their own sentence.
      - "The theorem's type and all six definitions …" (56 words).
      - "The strongest earlier unconditional result …" (56 words).

40. **STYLE (jargon without a gloss).** Several terms appear unexplained, and some readers will stop at each. Suggested glosses:
    - "comparator challenge": OpenAI's file stating the theorem with `sorry`, which the solution must match;
    - "fibres": groups of divisor coordinates that share one shift;
    - "prime mark" / "marked": one factor weighted by whether m + a is prime;
    - "singular series";
    - "level of distribution": how large the moduli can be, relative to X, in a Bombieri–Vinogradov-type bound;
    - "parity obstruction";
    - "Riesz mean";
    - "Vaughan's identity";
    - "box version of Gallagher's singular-series average";
    - "dot notation";
    - "leanchecker --fresh": re-checks every declaration from source, without trusting compiled files.

---

**What I did not check:**
- the mathematics of §5 beyond spot-reading;
- FC commit dates;
- the content of the kimihiro repository;
- Heath-Brown 1982;
- the live arXiv state.

On the source commit: FC links adc7f12 and we replayed 1581d4c. I confirmed that `git diff` between them is empty for the PrimeGaps Lean, the comparator and the preprint directory, so FC's link and our replay concern the same files.
