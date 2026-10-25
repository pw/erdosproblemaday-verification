# Blind read: Erdős #51 entry (rendered_page.txt), 2026-10-21

I read only the page text. I recomputed everything I could cheaply (scripts in /tmp/blind51/: an inverse-totient least-preimage routine, an exact-integer DP over the 3-smooth box, a float DP over the 5-smooth box and the other diagonals, and a φ-sieve to n ≤ 5·10⁷).

## 1. FALSE

**1a. Title and H1: "so bounded least-preimage ratios would give infinitely many Pierpont primes".** This doesn't follow. If sup R = B < ∞, the theorem gives infinitely many primes q with q−1 y-smooth, where y is the first prime with ∏_{p≤y} p/(p−1) > B. You only get Pierpont primes (y = 3) when B < 3. Since lim sup R ≥ 2.04 is all anyone knows, bounded ratios could sit at, say, 3.2, and then you'd get Q_{2,3,5} infinite, not Pierpont. The body has it right ("Below 3 means infinitely many Pierpont primes. If ℓ(a) < 3a for every totient a…"). The title is the most-read line and it's the one that's wrong. **Fix:** "so least-preimage ratios bounded below 3 would give infinitely many Pierpont primes".

**1b. "Every ratio record has T = 255/128 (3·5·17) and W ≤ 1.0258".** The six records (my sieve reproduces the first five: a = 2, 8, 128, 5888, 2,037,248, then 387,383,296) include a = 2 (ℓ = 3, T = 3/2) and a = 8 (ℓ = 15, T = 15/8). Only the last four have T = 255/128. **Fix:** "Every record from a = 128 on has T = 255/128…"

## 2. Overclaims, unclear scope, things that are incomplete

**2a. "The maximum, 2 + 9.04·10⁻²¹, is at a = 2⁹⁸·3".** The value is right, but it isn't attained at just that one point. My exact DP finds it at all 23 cells a = 3·2^X with 98 ≤ X ≤ 120, with ℓ = 2^(X−65)·(3·2⁶⁶+1). This is because no prime 3·2^j+1 exists for 67 ≤ j ≤ 188. The "27 points within 0.01 of 2" count checks out: those 23 cells plus X = 73, 81, 89, 97 (all with Y = 1). **Fix:** "is attained at a = 3·2^X for every 98 ≤ X ≤ 120 (first at 2⁹⁸·3, ℓ = 2³³·(3·2⁶⁶+1))".

**2b. Title: "every 3-smooth totient up to 2¹²⁰·3⁸⁰".** That reads as a size bound. What was computed is an exponent box, X ≤ 120 and 1 ≤ Y ≤ 80. For example 3·2¹⁵⁰ < 2¹²⁰·3⁸⁰ but it wasn't computed. **Fix:** "every 3-smooth totient 2^X·3^Y with X ≤ 120, 1 ≤ Y ≤ 80", as the body says.

**2c. Lim sup understated.** "Ford's propagation lemma … turns any single ratio into infinitely many, so lim sup R ≥ 2.043447". The page then establishes R = 2.0449753841 at a = 17,776,474,638,307,328 (I confirmed this is the exact least preimage). If the lemma applies to any single ratio, then lim sup R ≥ 2.044975, and the page never says so. Either state it, or explain why the lemma can't be applied to that a.

**2d. Ambiguous superscripts (check the live HTML).** In the text extraction, several formulas read as false statements:
- "(2^X3^Y+1 is always a preimage)" reads as 2^X·3^Y + 1, which is a preimage only when it's prime. The intended cover is 2^X·3^(Y+1), which has ratio 3.
- "ℓ(2^k) = 2^k+1" (twice) should be 2^(k+1).
- "ℓ = 2^9+j·257²" should be 2^(9+j)·257².
- "2^e+2^s" should be 2^(e+2^s).

If the HTML uses `<sup>`, these are fine on the page, but they'll be wrong in any plain-text copy (og:description, feeds, quotes). The 2^X·3^(Y+1) one is worth rewriting regardless.

**2e. Labels.** "What is ours" puts all the corollaries under (a). But "a positive proportion of totients v have ℓ(v) > 3v" rests on the preprint's Theorem 2.2, which makes it (b) by the page's own scheme. The heading "((d), two instruments)" introduces a section that then describes three instruments (the referee's certified DP is the third).

**2f. "Powers of 2 alone give exactly 2 from 2³² onwards".** This is unconditional only for 32 ≤ k < 2³³, as the parenthesis right after it says. The lead clause shouldn't say "onwards".

**2g. "The theorem cannot give a yes answer".** This is conditional on beliefs. It's fine as hedged by the next clause, but "cannot" would be cleaner as "is not expected to".

## 3. Internal inconsistencies

- **Guy A18:** it's cited as the authority that the Pierpont question is open ("Guy A18; erdosproblems.com/1055"), but later the page says the searches "did not reach Guy's B36/B39/A18". Either mark it as a second-hand citation or drop it.
- **Diagonal summary:** "On the diagonal the theorem uses, the least preimage is one to three huge primes from Q_S" conflicts with the {2,17} case. I get ℓ = 5·17³ there at K = 3, so 17 ∈ S stays in, as the page itself notes. In the {2,3} case the least preimage at K = 2 is just 13. Suggest "typically one to three large primes from Q_S".
- **Trivial covers:** "The trivial covers are worth 3, 3.75, 3.5, 3.25 and 2.5" lists five values for six sets. {2,17}'s value of 2.125 is missing, and that's the set whose 1.328 is the outlier.
- **July chain:** "appending primes whose p−1 brings a new large prime factor: 3, 5, 17, 47, …". That doesn't hold for 3, 5 and 17 (their p−1 is a power of 2). The text later says "After 17…". Rephrase as "starting from 3·5·17, appending…".

## 4. Attributions and quotes

- **Tao quote.** The second use, "very difficult with our current analytic number theory technology", drops "to prove this rigorously" without an ellipsis. Since it's in quotation marks and attributed to Tao, either quote it exactly or add "…".
- **"an unrefereed OpenAI preprint of September 2026".** Is this the same paper as "OpenAI's totient preprint" (Lemma 7.2, Theorem 2.2)? A general reader can't tell. Say "the same preprint" or name it.
- **"refereed here today".** This reads as formal peer review. Suggest "reviewed in our #416 entry".
- **Erdős remark marked "our remark".** The page quotes p. 80 directly, so please confirm that the surrounding text there doesn't already draw the "this would give n_a/a → ∞" consequence. Erdős often did.
- **Luca–Menares–Pizarro-Madariaga "in 2013".** I couldn't check the year. If the source is the journal version, it may be later than the arXiv date.

## 5. Hard to parse

- "caught, with at least one check, every one of its thirteen planted bugs that changes any output (three change nothing on our data)". Is it 13 bugs total with 10 detectable, or 13 detectable plus 3 inert? State the numbers plainly.
- "a reason given for an equivalence that was false". Was the reason false, or the equivalence? Suggest "a false justification for the (true) equivalence with sup R = ∞".
- "If the theorem has a hole, it would be in the step … (true for any preimage: …)". This both invites and dismisses the check. The second candidate ("reading … 'infinitely many K' off a statement about every a") is a trivially valid direction, so it's unclear what the worry is.
- "A reader who knows the barrier from somewhere else will find this sentence already saying where we did not look." This is awkward. Try "If you know an earlier statement, it is probably in one of these."
- Jargon for a general reader: "#416 tick", "seats", "hostile … referee", and the undefined ⟨S⟩ (say "the products of primes in S").
- "still with a bound that grows with p" is clearer as "i.e. P(p−1) = p^o(1), not a fixed y".

## 6. Clearly fine (checked)

- **Barrier theorem proof, line by line.** r−1 | φ(m) = a_K, which is S-smooth. r ∉ S ⇒ r ∤ a_K ⇒ r ∥ m. Missing p ⇒ v_p(a_K) = Σ_{r|m} v_p(r−1) ≤ Σ_S + Σ_Q. v_p(a_K) = (K−1) + Σ_S. That gives the contradiction, and then m/φ(m) ≥ n_K/φ(n_K) together with m ≤ n_K gives m = n_K. The proof is correct (and the last step is even shorter than written). The widened-Q remark for non-φ-closed S also checks out.
- **Carmichael case.** Σv₂ = 31. For k ≥ 32 the formula holds, and it's sharp at 31 because 3·5·17·257·65537 = 2³²−1 < 2³². The unconditional range k < 2³³ (F₅–F₃₂ composite) is correct.
- **Products and thresholds.** 15/4, 2·17/16 = 2.125, 2·5/4 = 2.5, 3, 2·257/256 = 2.0078. The y thresholds 5/7/13 for k = 3/4/5 (3.75, 4.375, 5.2135 vs 3, 3.75, 4.8125). y ≥ 3 since sup R > 2. The {2,3,q} disjunction (∀q(P ∨ A_q) ≡ P ∨ ∀q A_q). The "read the other way" seed statement.
- **Erdős-hope implication.** m_X ≫ X log log X and m′_X = max_{a≤X} ℓ(a), so ℓ(a)/a ≥ m′_X/X → ∞ (given the stated reading of m_X and m′_X).
- **Anatomy.** ℓ is never ≡ 2 mod 4. The Fermat swap 2^e·F_s → 2^(e+2^s). ∏(1+2^(−2^s)) = 2. T ≤ 2. A 3-seed needs W > 3/2.
- **Recomputed and matching:**
  - 402 Pierpont primes (excluding 2 and 3) and 2,914 free primes in the 5-smooth box.
  - No 3-smooth cell reaches 2+10⁻²⁰ (exact).
  - 27 cells within 0.01 of 2.
  - {2,3} diagonal max 13/12 at K = 2, and the K = 18 single prime 33,853,318,889,473.
  - {2,3,5} max 1.0240; {2,5} 1.025; {2,3,7} 1.0933; {2,3,13} 1.0075; {2,17} 1.328.
  - 5-smooth max 15/8 + 3·2⁻⁵⁸ at 2⁵⁸·5 with the stated ℓ; next cell 1.6000000092.
- **The July chain.** All eight stages are the exact least preimages. a = 2¹²·23·173·593·683·2693 = 17,776,474,638,307,328, R = 2.0449753841. Stage 7: a = 3,300,496,590,848, R = 2.0445958. The appended primes 47 through 5387 are safe primes. The p = 5399 cheaper preimage is exactly as stated (ratio 1.50028). In a sample of 65 safe primes in (5387, 6·10⁶], none keeps the appended product.
- **Records and preimages.** Records up to 2·10⁷ match. ℓ(387,383,296) = 3·5·17·47·257², R = 2.043447. ℓ(559,789,704) = 3³·19³·4787, R = 1.583664, with 2³ ∥ a. The six even least preimages 2^(9+j)·257² (j ≤ 5, j = 6 exceeds 10⁹) are least, and the first even ℓ is at 2¹⁶·257 = 16,842,752.
- **The sieve-to-2.5·10⁹ logic.** Coverage certified by the count, plus an upward scan, gives least preimages. That reasoning is sound.
- **Not checked:** V(10⁹) = 139,847,905 and the OEIS/forum/quote contents.
