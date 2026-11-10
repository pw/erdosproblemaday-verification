# Blind read: Erdős #912 page ("why h(n)/(n/log n)^{1/2} is 2.57 and not 2.51")

Reader: cold, independent. I read the page, the bundle `~/ErdosProblemADay-1110-0900/verification/912/cramer-at-1e18/` (README, code/, out/, controls/; no referee_*.md), gi.txt, hm.txt, f912.html, the problem page, Montgomery–Soundararajan (arXiv math/0409258), MathOverflow 413332 (API), OEIS A357385/A357391 (via Hetzner) and Kruis's GitHub package. I also read the paragraph added mid-read ("Eldar's second conjecture looks false…").

My own scripts are in `/tmp/br912/`:
- `num.py`: constants, Bernstein bounds, coefficients.
- `lemma.c`: the Lemma for every prime q, not only divisors.
- `lrange.c`: how far the Lemma's range really goes.
- `moves.py`: exact recount of moves to 10^7.
- `moves9.py`: real versus model move shares near 10^9.
- `md2.py`: Poisson versus Bernoulli move density.
- `pc/`: sensitivity of the pair term to how it is resummed.

## What checks out (so the objections are read in proportion)

- **Every h(n) value and ratio in table 1.** All trace to `out/hfast_*.out` and `hfast_small.log`. The GMP agreements at 10^9 and 10^12–10^15 trace to `href.log` and `href_1e15.log`. The boundary-moved reruns at 10^15–10^18 trace to `xcheck.log`.
- **Every entry of table 2.** All trace to `summary_*.txt`, `model_*.out` and `bernstein.txt`. The empty, one-prime and two-prime class counts trace to `hfast_1e18.out` and `model_1e18.out`. The pair shares 0.8137, 0.8232, 0.8308 and 0.8396 trace to `pair_check.log`. F19 = 1.18–1.21 and the calibrated 0.9875–0.9904 trace to `pair_calib.log`. The c_r values trace to `cr_check.txt`.
- **The mutant counts.** 1,165,588, 1,167,674 and 150,403 match `ctl_bf_mut_*.log`. The 242,570,204 isolation pairs match `bf_1e8.log`, and 2,549,489,372 matches `bf_1e9.log`. The figures 4,003 and 2,000 match `hfast_vs_bf.log`.
- **The b-file.** I diffed the MathDyad copies of `bf_small.txt` against the OEIS b-file: identical, 10,000 rows.
- **Bernstein bounds.** Recomputed: 10^−6683.7 and 10^−149168.9.
- **Heuristic coefficients.** The coefficients 0.93, 0.90 and 0.87 recompute. So do Cramér's +0.17 and −0.03, (γ + log 2π − 1)/2 = 0.70755, and D(H) = −½H log H − 0.20755H.
- **G–I's Theorem 1.2.** The constant (1+γ+log 8)/(2 log n) is verbatim. The quoted sentence is verbatim; the ellipsis cuts "such as the Cramér–Granville model (see, e.g., [13, Chapter 17])".
- **The log log n cancellation.** It is right as algebra. The pair shift is √(π/2)·(log log n − (2 − log(π/4)))/log n · L, and √(π/2) = √(2π)/2.
- **The Lemma proof is complete.** Each case checks. Independently, I tested isolation for every prime q with q² ≤ x+1 (not only divisors) for x ≤ 3·10^6: 566,156,105 checks, 0 failures.
- **The Theorem proof is complete.** My separate recount of up and down steps to 10^7 via the jump rule and prime counts gives 283,888 up (+1 at m = 4 makes 283,889) and 281,802 down. That matches bf and Eldar's table.
- **Attributions that check.**
  - Sawin's answer: 7 Jan 2022, the interval reduction, √(2π).
  - Tao's comment: 31 Aug 2025; the problem page credits him.
  - Owmire: 24 Jun 2026, to 10^8, "a proof seems intractable to me".
  - Eldar: A357385, Sep 2022, table to 10^7. His formula reads "a(p) = 0 for an odd prime p", with a(n) = h(n+1) − h(n). That is indeed off by one: a(5) = h(6) − h(5) = 1. The page is right.
  - Kruis: exhaustive to 165,493,254,314.
  - July report: its square case does say "0 or 1".
- **New paragraph.**
  - 5.66% (10^7), 4.84% (10^8) and 4.48% (10^9) recompute from `bf_1e9.log`. So do the decade shares 6.40, 5.54, 5.66, 4.74 and 4.44%.
  - Eldar's up and down counts match.
  - The Frullani limit 2 log 2/log n is right: the sum is ≈ (4/log n)∫ e^{−u}(1−e^{−u}) du/(2u).

## Objections

1. **MUST — wrong unit.**
   - Quoted: "It is 2.6% of L at 10¹⁵ and 2.3% at 10¹⁸. The model's own spread is about 0.04% of L."
   - Why: the gap divided by L is 0.0649 at 10^15 and 0.0579 at 10^18 (`summary_*.txt`: (J−E_C)/scale), i.e. 6.5% and 5.8% of L. The 2.6% and 2.3% are fractions of the model mean E[h]: 348,987/13,488,974 and 9,000,142/388,502,991. The sd is 0.036% of L at 10^15 but 0.0069% at 10^18.
   - Fix: "The gap is 0.065·L at 10^15 and 0.058·L at 10^18, i.e. 2.6% and 2.3% of the model's mean; the model's sd is 0.036% of L at 10^15 and 0.007% at 10^18."

2. **MUST — false at half the n computed.**
   - Quoted: "At the n we computed, the positive third term outweighs the negative second. Their expansion therefore sits slightly above √(2π) (2.511 at 10¹⁵), but well below the data."
   - Why: the bracket coefficient (1+γ+log 8 − log log n)/2 changes sign at log log n = 3.6567, i.e. n ≈ 6.6·10^16.
     - At 10^17 and 10^18 the negative term wins. The page's own table gives 2.5063 and 2.5046, both below √(2π) = 2.50663. The page itself later says "−0.03 at 10¹⁸".
     - The exact model mean is below √(2π) from 10^16 on (2.5046, 2.5027, 2.5012).
   - Fix: "At 10^15 the positive third term outweighs the negative second, so their expansion gives 2.511. It crosses √(2π) near n ≈ 7·10^16 and is 2.505 at 10^18. The data stay at 2.56–2.57."

3. **MUST — the "independent second implementation" is not in the bundle.**
   - Quoted: "Two independent implementations agree to the unit: 283,973, 845,454, 2,524,290 and 7,556,372." Also: "The Hardy–Littlewood sums were computed twice, by separately written code, and agree to the unit."
   - Why: the only two pair-sum outputs in the bundle share code. `code/pair_calib.py` starts with `exec(open('pair_check.py').read().split("def pair_delta")[0]…)`, so it reuses pair_check's 𝔖 and C2 arrays. Its `pair()` is a line-for-line copy of `pair_delta` (same midpoint, same lp0 > −80 cut, same exponentiation). The "separately written" (referee) implementation and its output are not in code/, out/ or controls/. A reader who sees `pair_check.log` and `pair_calib.log` agree will wrongly take that as the independent check.
     - Also, the logs say 7,556,372.9 and 7,556,373; the page prints 7,556,372, a truncation.
   - Fix: put the referee's pair-term code and log in controls/, or say "computed once (pair_check.py); pair_calib.py reuses it". Print 7,556,373.

4. **MUST — the 98.8–99.0% has precision the method doesn't have.**
   - Quoted: "Scaling the true pair term by that factor accounts for 98.8–99.0% of the gap."
   - Why: the calibration factor depends on which sieve depth you pick.
     - With F5 from the same log (1.1788 … 1.1485), pair share × F5 = 95.9%, 96.1%, 96.2%, 96.4%.
     - With F19 the result is 98.8–99.0%.
     - The page says deeper sieves "overshoot", so larger z would presumably push the number past 100%.
     - Nothing makes F_19 the right transfer factor for the true primes; the sieve model's higher correlations come from a truncated singular series.
     - "Past depth ≈ 40 it stops improving, and past ≈ 100 it overshoots" (and "depth 139") cannot be traced to any file in out/ or controls/; model.c only runs z ≤ 19.
   - Fix: "Scaling by the sieve models' ratio (1.15–1.21 for depths 5–19) brings the total to roughly 96–99%; this depends on the depth chosen and is a calibration, not a derivation." Add the depth-139 run's output to out/. Better still, see objection 5.

5. **MUST — false statement, and it is the reason given for using a calibration.**
   - Quoted: "The rest is plausibly higher-order correlations. We cannot compute those for the true primes."
   - Why: under the same Hardy–Littlewood heuristic they are computable.
     - The third and fourth factorial cumulants of an interval's count are q³R₃(H) and q⁴(R₄ − 3R₂²-type) sums of explicit k-tuple singular series over the H integers of the interval.
     - The intervals that matter have H ≲ 200. That is about 1.3M triples and about 70M quadruples, each singular series a rapidly convergent product. This is a few CPU-minutes in C.
     - Montgomery–Soundararajan's Theorem 2 also gives the order of R_k(h), which is how you know these terms are lower order asymptotically.
   - Fix: say "we did not compute". Or compute the third-order term (and the fourth if cheap). That would turn the 99% from a calibration into a heuristic derivation, at the same level as the 81–84%.

6. **MUST — misstates Kruis.**
   - Quoted: "It reproduces all six exhaustive values Kruis published, at 1.78·10⁹ and 1.65·10¹¹."
   - Why: Kruis's AUDIT_SUMMARY.txt (github Xer0H3r0-87/a357391) publishes 19 values: n = 1784800611..19 (9 values) and 165493254305..14 (10 values). `kruis_control.log` checks 6 of them, the endpoints and starts.
   - Fix: "It reproduces six of the 19 values Kruis lists (…)". Better: run hfast at all 19, which is cheap, and say "all 19".

7. **MUST — misattributes a theorem's content.**
   - Quoted: "Heyman and Miraj (arXiv 2309.16072, Theorem 2) proved h(n) = #{⌊n/p⌋ : p ≤ n} exactly."
   - Why: hm.txt's Theorem 2 states only the two-sided bound c₁(X/log X)^{1/2} ≤ |S_p(X)| ≤ c₂(X/log X)^{1/2}. The identity |S_p(X)| = |α(X!)| is proved inside its proof (§3: "We will show that |S_p(X)| = |α(X!)|"). A reader who opens Theorem 2 will not find it.
   - Fix: "Heyman and Miraj (arXiv 2309.16072, in the proof of their Theorem 2) proved …". The Sources line needs the same fix.

8. **MUST (new paragraph) — the last sentence is false; the conjecture can be refuted unconditionally.**
   - Quoted: "A proof that the share tends to 0 would need short-interval information about primes that nobody has."
   - Why: as I read it, moves in (N, 2N] number ≪ N/log N with no hypothesis. Sketch:
     - By the jump rule, a move needs m = n+1 = kQ with Q > √m, k ≥ 2, and exactly one of two events. A_k: class k (the primes in (⌊n/(k+1)⌋, Q−1]) is empty. B_k: class k−1 (the primes in [Q, ⌊n/(k−1)⌋]) is {Q}. Note that Q sits at the left edge of class k−1, because ⌊n/k⌋ = Q−1.
     - **k ≤ L.** A_k forces the gap before Q to exceed H ≍ N/k², and B_k forces the gap after Q to exceed H. Among the primes Q in an interval of length N/k, at most N/(kH) + 1 ≪ k have such a gap, because the gaps are disjoint. Summing over k ≤ L gives ≪ L² = N/log N.
     - **k > L.** A move needs ¬A_k or ¬B_k, i.e. another prime within D ≍ N/k² of Q. The Selberg/Brun upper-bound sieve gives #{Q ≤ X : Q, Q±d prime} ≪ 𝔖(d)X/log²X, uniformly in d. Summing over d ≤ D gives ≪ N²/(k³ log²N) + N/(k log²N). Summing over L < k ≤ √(2N) gives ≪ N/log N.
     - Edge cases check out. A small prime cannot sit in class k−1, because its exponent exceeds Q's. It cannot sit in class k for k < √m either.
     - So the share of moving steps is O(1/log n), matching the heuristic 2 log 2/log n. The density of 0 tends to 1, so Eldar's second conjecture (0.943) is false. I checked the bound numerically near 10^9: the per-k count of A is at most 0.35 of the gap bound.
   - Fix: write the proof, have the proof referee check it, and relabel the paragraph "(a/b)" with the heading "Eldar's second conjecture is false". Keep the Cramér/Frullani computation as the heuristic for the constant 2 log 2.

9. **MUST (new paragraph) — the stated cause is backwards for the events that matter.**
   - Quoted: "The real share runs lower for the same reason as above: fewer intervals are empty."
   - Why: the two intervals that decide a move flank a prime Q, and next to a prime the real data leave more of them empty, not fewer. In the window m ∈ [10^9, 10^9 + 4·10^6] (`moves9.py`):
     - The real local move share is 4.26%. Cramér, on the same (k, Q) events, gives 5.28%.
     - P(A) is 0.265 for real primes versus 0.2435 for Cramér; P(B) is the same, 0.265 versus 0.2435. That the two are equal is forced by up ≈ down.
     - Independence using the real marginals gives 4.01%. The real A and B are slightly negatively correlated (P(A∧B) is 0.2076 against 0.2110), which lifts the share back to 4.26%.
     - The mechanism is the first-order HL effect of conditioning on Q being prime: Σ_{d≤H}(𝔖(d) − 1) ≈ −½ log H, so the H integers beside a prime hold fewer primes than average. "Both flanks empty" (no move) becomes commoner. It comes from the same less-clumped structure, but it shows up as more empty intervals here, not fewer.
   - Fix: replace the sentence with the measured decomposition, or with "Conditioned on Q being prime, its neighbouring intervals are empty more often than in the model (26.5% versus 24.4% near 10^9), so both events happen together more often." Put the window script and its output in the bundle.

10. **MUST (new paragraph) — wrong model, and not like for like.**
    - Quoted: "In Cramér's model the share … The model gives 6.9%, 6.2% and 5.6% at 10⁷, 10⁸ and 10⁹."
    - Why: `move_density.py` uses the Poisson form p0 = exp(−λ), with real-valued lengths and no √n cut. Cramér's model as defined (G–I (1.8), Bernoulli 1/log l, integer lengths) gives 6.5%, 5.8% and 5.3% (`md2.py`). Also, these are local shares at n, but the data quoted next to them are cumulative or decade averages.
    - Fix: say "Poisson approximation", or recompute with Bernoulli. Compare local with local: real 4.26% against Cramér 5.3% near 10^9.

11. **SHOULD — "therefore" outruns the evidence.**
    - Quoted: "The 2.57 is therefore no evidence against c = √(2π)."
    - Why: it rests on a (c) heuristic that supplies 81–84%, or 96–99% after a depth-dependent calibration.
      - Note also that the pair-corrected finite-n model is already at its asymptotic coefficient: (E_C[h]+pair)/L gives 2.5596 → 2.5498, coefficient 0.73 → 0.71, at 10^15 → 10^18.
      - So "drifting down towards 0.71" is not a finite-n effect of the pair model. The 0.16 residual is the unexplained higher-order part.
    - Fix: "So the 2.57 is consistent with c = √(2π): at the pair level the next term is +0.71/log n. The data's 0.87 at 10^18 exceeds this; the difference is the higher-order part we only calibrated." Also soften "That is why the ratio sits above √(2π)" to "This is consistent with the ratio sitting above …".

12. **SHOULD — a resummation choice hides behind "nothing fitted".**
    - Quoted: "We summed that shift over every interval, with nothing fitted. It supplies 81%, 82%, 83% and 84% of the gap."
    - Why: the code exponentiates, ΔE = Σ p₀(1 − e^{q²D}). The equally second-order linear form Σ p₀(−q²D) gives 84.9% at 10^15 instead of 81.4% (`/tmp/br912/pc`). That 3.5-point spread is larger than the 81→84% "rise with n".
    - Fix: state the choice ("factorial-cumulant expansion truncated at second order and exponentiated; linearising gives 85% at 10^15"). The title's "supplies 84% … with nothing fitted" should read "a second-order Hardy–Littlewood correction accounts for about 84%".

13. **SHOULD — wrong rounding of a closed-form constant.**
    - Quoted: "√(π/2)·(log log n − 2.2417)/log n."
    - Why: the constant is exactly 2 − log(π/4) = 2.24156. Showing the closed form also makes the next line (γ + log 2π − 1) transparent: (1+γ+log 8) − 2 + log(π/4).
    - Fix: "(log log n − 2 + log(π/4))", ≈ 2.2416.

14. **SHOULD — G–I's theorem is restated without its error term.**
    - Quoted: "Theorem 1.2: Cramér's model gives h = √(2π)(n/log n)^{1/2}(1 − log log n/(2 log n) + (1+γ+log 8)/(2 log n) + …)."
    - Why: G–I state it "with probability 1", for h_C(n!), with error O(log log n/(log n)^{3/2}). At 10^15 that scale is about 0.017 relative, comparable to the effects being compared. That is exactly why the exact finite-n model values matter.
    - Fix: give the O-term and "with probability 1". Then say that table 2's exact model column is what makes the expansion comparison meaningful.

15. **SHOULD — misquoted error term and the less direct equation.**
    - Quoted: "D(H) = … + O(√H) … the k = 2 case of Montgomery and Soundararajan's … eq. (17)."
    - Why: M–S (16) states R₂(h) = −h log h + Ah + O(h^{1/2+ε}) with A = 2 − γ − log 2π. Since R₂ = 2D, that is the direct statement. Eq. (17) is the Gallagher-moment form, which gives the same thing at k = 2. M–S prove O(h^{1/2+ε}), not O(√H).
    - Fix: "M–S (16) (equivalently (17) with k = 2), error O(H^{1/2+ε}); numerically (D − main)/√H stays below 0.2 up to H = 20,000."

16. **SHOULD — say these are the models G–I asked for, and name Gallagher.**
    - Quoted: "We can compute them for a fixed-depth Granville sieve model…" and "Every model here has the same leading constant √(2π)."
    - Why: G–I explicitly suggested the Cramér–Granville model; the sieve family is a fixed-depth version of exactly that. Readers will also want Gallagher's theorem: uniform HL ⇒ Poisson counts in intervals of length λ log x ⇒ √(2π). That is why every model shares the constant. (Gallagher averages over x, not over the grid n/k; that caveat belongs in "What this does not do".)
    - Fix: one sentence each.

17. **SHOULD — the title.** About 50 words, and it frames 2.57 versus 2.51 (10^15 data versus the 10^15 expansion). The body frames 2.56 versus 2.50 (10^18 data versus the exact model). It also states the heuristic as fact. Suggested: "#912: exact h(n) to 10¹⁸, and why the ratio is 2.56, not the Cramér model's 2.50".

18. **SHOULD — the per-t excess.**
    - Quoted: "The excess reaches 3.4% of all intervals near t ≈ 1.25, where the average count is about 1.3."
    - Why: from `model_1e18.out` the peak is 3.41% in the bin t ∈ [1.15, 1.20), where 2/t² ≈ 1.45. The excess is a plateau of about 3.4% over 1.15–1.30.
    - Fix: "about 3.4% for t ≈ 1.15–1.3, where the average count is 1.2–1.5".

19. **SHOULD — K0 is never explained.**
    - Quoted: "Take the intervals with k ≥ K₀ = 32,167,776 at n = 10¹⁸."
    - Why: K0 is hfast's internal sieve/Miller–Rabin boundary, where an interval holds about 40 expected primes. A reader can't tell why that cut.
    - Fix: "(below K0 every interval holds about 40 or more primes and none is empty, in fact or in the model)".

20. **SHOULD — process notes and untraceable numbers.**
    - Quoted: "Our proof referee caught this step missing from our first draft. The bound is attained, 2,013 times below 2·10⁵."
    - Why: process narrative inside a proof. 2,013 is not in any bundle log, though I reproduce it: e_n(q) = m/q = Q happens 2,013 times for m ≤ 2·10^5. It is also ambiguous which bound is meant. What the proof needs is e_n(q) > k, and that has slack in every case but one (m = 6, where e = k+1).
    - Fix: cut both sentences, or say "e_n(q) = Q occurs (2,013 times below 2·10^5); e_n(q) = k+1 only at m = 6". Add the log.

21. **SHOULD — small proof gaps** (each one line). In the Theorem, write "q | k, so k ≥ q; Q > √m ≥ q; hence m ≥ q(q+1) and n ≥ q²". In "Small factors", note that the Lemma's exception (q, x) = (2, 3) is exactly m = 4. In the Lemma, note that q = 2 has no q−, and in the case q² ≤ x < q+² that the first term does not increase.

22. **SHOULD — the mutant list.**
    - Quoted: "Four mutants fail as they should. … so the Lemma's range is real."
    - Why: only three are listed. The fourth (STEPBOUND=0, 565,691 step failures) is missing. The mutants ran at N = 10^7, not 10^8 or 10^9. And the stated range is not sharp: isolation holds for every q² ≤ 1.5x for x ≤ 10^6, all 269 cases q² = x+2 hold, and the first failure is at q²/x = 1.8 (x = 5, q = 3). The mutant only shows 4m is too far.
    - Fix: list the fourth, give N = 10^7, and say "the range cannot be pushed to q² ≤ 4m (it does hold empirically to q² ≤ 1.5x)".

23. **SHOULD — other untraceable numbers.** Add the logs or cut the claims.
    - "a referee's per-integer computation, to within 0.01 at 10⁶, 10¹² and 10¹³": no log, and no unit. Is 0.01 in J or in h/L?
    - model.c's 10^6 value (526.12), which the Monte Carlo compares against: no `model_1e6.out`.
    - The b-file match: neither `bf_small.txt` nor the b-file is in the bundle. I diffed the MathDyad copies; they match.
    - The Seats paragraph's "every n ≤ 2·10⁵ … 801 targeted steps up to 5·10⁶" and "depth 139".

24. **SHOULD — href.py's independence.**
    - Quoted: "href.py is a separate route … without assuming the Lemma."
    - Why: it relies on Heyman–Miraj's identity instead. Its set A is the set of first Legendre terms ⌊n/p⌋, not exponents.
    - Fix: say so. It is still a genuinely different route.

25. **SHOULD — "Pairs at short distances are rarer than chance."** 𝔖(2) = 2C₂ ≈ 1.32 > 1. What is below 1 is the average of 𝔖(d) over d < H, by about ½ log H/H. Rephrase: "averaged over the distances inside an interval, pairs are slightly rarer than chance".

26. **SHOULD — small citation and number fixes.**
    - Sawin's answer is MO 413344; 413332 is the question.
    - Erdős: "pp. 25–27" in the text against "25–45" in Sources. Write "Congr. Numer. 34 (1982), 25–45; the quote is on p. 27".
    - "Owmire repeated the observation": nothing shows he knew of A357385. Write "made the same observation".
    - "That report also computed h up to 10⁹": it computed h at powers of ten up to 10^9.
    - "0.33 at 10¹⁷": π(√n)/L = 0.338 → 0.34. The 2/√log n approximation gives 0.32.
    - "using the mean of log l over each interval": the code uses log at the interval midpoint.
    - The labels list (a), (c), (d) with no (b). Say why.

27. **SHOULD — the Bernstein probabilities.** Arithmetic correct, as recomputed above. But the next paragraph already concedes the sd count is uninformative, and these are the same fact in a louder unit. Cut them, or keep one sentence.

28. **SHOULD — structure.**
    - "Why this split is exact is shown below" forces the reader to accept the key identity on credit through two tables. Either move the Lemma and Theorem before "Ours: exact values", or give the two-line separation argument inline.
    - The Seats paragraph is process. Move it to a footer.
    - "(4) A blind reader read this page cold" should go in only once it is true.

29. **SHOULD (new paragraph) — "near L" and Eldar's constants.**
    - Quoted: "So moves come only from k near L."
    - Why: near 10^9, 91% of moves have k > L (0.40% of steps from k ≤ L, 3.86% from k > L). The integrand peaks where p₀ = ½, at t ≈ 1.7.
    - Fix: say "k of order L, mostly L < k < 4L". Also note that Eldar's 0.028 and 0.943 are simply his observed shares at 10^7 (283,889/10^7 and 9,434,309/10^7). That makes the "fixed share" reading visibly an extrapolation.

## What I would cut

- The Bernstein probabilities (objection 27).
- The Seats paragraph from the body (objection 28).
- "Our proof referee caught…" and "2,013 times" (objection 20).
- The 98.8–99.0% decimals (objection 4).
- The title down to one clause (objection 17).

Lead the heuristic section with the 81–84% pair term, its resummation caveat (objection 12) and the log log n cancellation. That is the page's real contribution, and it stands.
