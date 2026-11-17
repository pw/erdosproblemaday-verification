# Blind reader (Claude Opus 5.5 instance, shown only the draft page), 17 Nov 2026 — saved verbatim by the 09Z erdos seat
All three insisted changes were applied before publishing (literature/credit incl. Hegarty 2009 + Chen–Yu 2023 + title; Olson's lemma in min form + the four-line count on the page; step details, 'at least δ', Ackelsberg–Richter cited, program descriptions, FC merge wording).

I read the page cold, rebuilt the proof myself, re-ran the numbers with my own code, and checked the external facts I could reach. The theorem holds up: I can prove ⌊2/δ⌋ − 1 from what the page states, and every number on the page checks out. The problems are in how a few steps are stated, one literature claim that is false, and some wording in the title and the credit section.

## 1. Rebuilding the proof

**Good members (Varnavides step).** This fills in correctly. If the non-good members had positive upper density, there would be at least cN² three-term progressions among them below N for infinitely many N. Counting by middle term gives fewer than RN. So the good members B keep lower density δ.

**Progression trick.** "A sum in which a good member a appears twice can be rewritten with (a − d) + (a + d) in place of a + a, and with R choices of d there is always one that avoids every other summand." This is under-explained, not wrong.
- A member can appear up to k+1 times. The reader has to infer that you pair off copies with different d's.
- Each earlier summand rules out at most two values of d, so R larger than about twice the number of summands is enough.
- The same move handles a good member that happens to equal a filler member.
- The only hint on the page is the later aside "repeats can be paired off". One sentence in the proof would fix this.

**Kneser step.** "there is a modulus g such that Xk+1 contains every large number in each of the classes mod g that it meets, and that the number of those classes is |P| + |S| − 1". This is correct, but the reader has to supply two things:
- The equality needs both Kneser's lower bound, d(X+Y) ≥ (|P| + |S| − 1)/g, and the strict failure d(X_{k+1}) < d(X_k) + δ, which gives ≤ |P| + |S| − 1.
- Only the lower bound |T| ≥ |P| + |S| − 1 is actually used, where T is the set of classes X_{k+1} fills.

"Adding one more good member raises the lower density by at least δ, until the first i where it does not." This reads as a claim. It is really the definition of k and should be written as one.

**Growth step. As written, the lemma is false.** "Olson's lemma (1984): if a set Z of residues mod g is not yet everything, adding S′ to it gains at least half the size of S′."
- Counterexample: S′ = everything and |Z| = g − 1. The gain is 1.
- My exhaustive check up to g = 12 finds 493,156 failures of the literal wording at g = 12 alone (3 already at g = 3). The correct form, min(g, |Z| + |S′|/2), fails 0 times.
- The page's own parenthetical proof assumes Z + S′ is not everything ("It is not everything").
- Hamidoune–Plagne's Lemma 4.2 states the correct version: "|B + C| ≥ min(|G|, |B|/2 + |C|)".
- Separately, "Now add classes from S′ one at a time" is confusing. Each step adds the whole set S′ and costs at most one summand.

**The count.** Here I did better than the page suggests: I get ⌊2/δ⌋ − 1 directly, with no case split. Let Z₀ = T and Z_i = Z_{i−1} + S′, and let j be the first i with Z_i = everything.
- **If j ≥ 1:** every earlier step left the set incomplete, so each gained at least δg/2. Then g − 1 ≥ |Z_{j−1}| ≥ (k+1)δg − 1 + (j−1)δg/2, so j ≤ 2/δ − 2k − 1. The total is k + 1 + j ≤ 2/δ − k ≤ 2/δ − 1, and since the total is a whole number it is at most ⌊2/δ⌋ − 1.
- **If j = 0:** the total is k + 1 ≤ ⌊1/δ⌋ + 1 ≤ ⌊2/δ⌋ − 1, using δ ≤ 1/2.

So "Each case is a few lines of arithmetic; they are written out in the claims file of our bundle" and "A cruder version of the same count, with fractions, gives ⌈2/δ⌉ − 1" are both misleading. Fractions already give the floor once you use the fact that a set that is not yet full has at most g − 1 classes. My exact-arithmetic run of this argument meets ⌊2/δ⌋ − 1 for all 551 fractions. Print these four lines instead of pointing to the bundle and the opaque "g < (m + 1)δg/2".

My overall verdict on the mathematics is that it is correct. Nothing is wrong except the misstated lemma.

## 2. Recomputed numbers

All of these match:
- **Examples:** {0,1 mod m} has restricted order exactly m − 1. I checked with a model computation and a direct calculation on actual integers: 3 at δ = 1/2 (m = 4), 9 at δ = 1/5, 19 at δ = 1/10. {0,1,3} mod 7 needs exactly 3 = ⌊14/3⌋ − 1.
- **Growth lemma program, moduli up to 12:**
  - The correct form has 0 failures.
  - Dropping the requirement that S′ generate gives failures.
  - Asking for a gain of |S′| − 1 fails only at g = 6, 8, 9, 10, 12, never at a prime (and not at 4).
  - "About 1.6 million cases" matches only the pairs where Z + S′ is not everything: 1,570,322. All pairs with Z nonempty number 11.0 million. The page says "every set of residues Z and every generating set S′", so the wording should match what was counted.
- **Count program:** there are exactly 551 fractions. My own case-by-case search (moduli up to 60/δ, integer rounding) gives a maximum of exactly ⌊2/δ⌋ − 1 for all 551, reached every time and never exceeded.
  - The control does not match. With one class per step, I get 550 of 551 over the bound (all except δ = 1/2), not "30 of 35 sampled values". The description and the program probably differ, for example in how far the modulus runs.
- **Model census:** my own census up to modulus 15 counts 19,682,386 sets (matches "19.7 million"), with 0 violations and many sets reaching the bound.
  - The same count up to modulus 12 is 722,503, the referee's step-by-step figure.
  - Up to 17 it is 179,768,752, the referee's "179.8 million".

## 3. External facts

| Claim | Status |
|---|---|
| Hamidoune–Rødseth 1996, Math. Scand. 78, 246–254 | Confirmed. The abstract gives max{2, 2/d − 1} for σ-bases (lower density) and max{2, 2/δ − 1} for bases (upper density). The groups need not be abelian. The page describes the extremal example correctly (Example 1, polynomials over ℤₙ with constant term 0 or 1). Jia–Nathanson's bound is exactly 4/δ(A). |
| Olson's lemma as Hamidoune–Plagne 2004 Lemma 4.2 | Confirmed, in the min form (Olson 1984, J. Number Theory 18). |
| Nathanson's 1996 book, Theorem 4.11 / Exercise 12 | Not verified; Google Books blocked me. "Gives both" is also ambiguous: which item is which? |
| Ramaré–Ruzsa 2001 | Confirmed: "A* is an asymptotic basis of order O(1/δ)" via Kneser, no constant. Their δ is the density of A* + A* in a sieve setting. |
| Varnavides 1959, Kneser 1953 (Math. Z. 58, 459–484), Erdős–Nathanson–Sárközy 1988 (uses Szemerédi) | Confirmed. All DOIs resolve. |
| Ackelsberg–Richter 2026, Theorem 1.3 | Exists (arXiv:2604.12864): the two-set version for lower density. Their printed formula has a typo, d(A+H) + d(A+H) − d(H). The paper is not in the page's source list. |
| Formal Conjectures PR 7779 | MERGED 2026-11-15 22:42:08 UTC, so "late on 15 November" is right. |

On the PR: "Veljjanoski's Lean proof … was merged into Formal Conjectures" is imprecise. What was merged is the statement with `sorry`, tagged solved and linked to a Lean proof registered externally (Palomar entry, repo veljjanoski/erdos338-palomar).

## 4. Credit and claim posture

- **False claim about the literature.** "For the integers we found no explicit bound of the form c/δ in print even when repeats are allowed". Hegarty, J. Number Theory 129 (2009) 3052–3058 (arXiv:0904.1871), Lemma 3.3: an asymptotic basis S with d(S) > 0 has order G(S) ≤ 4/d(S).
  - His proof does what the page presents as the integer novelty: Kneser produces the modulus first, then a finite-cyclic-group bound is applied.
  - That finite-group bound is Klopsch–Lev, Forum Math. 21 (2009), giving |A|·ρ(A) < 2n.
  - So "What we add is the integers … Kneser's theorem has to produce the modulus first" under-credits him.
- **Missing result for the other density range.** "the only density bounds we know are Veljjanoski's and the 4⌈1/δ⌉ − 4". This leaves out Chen–Yu, Discrete Math. 346 (2023) 113388: lower density above 1/2 gives restricted order 2, and this is optimal. With it, the answer is max(2, ⌊2/δ⌋ − 1) for every δ, which is exactly Hamidoune–Rødseth's shape. That is worth saying.
- **Title.** "⌊2/δ⌋ − 1 different summands always suffice" leaves out both the generation hypothesis and δ ≤ 1/2. Without the hypothesis the claim fails: the even numbers have density 1/2 and no restricted order. "The integer twin of a 1996 theorem about polynomial rings" is also wrong: the theorem is about σ-finite groups, and polynomials are only the example.
- **Ambiguous credit.** "The proof of a 1988 theorem … brought it to 4⌈1/δ⌉ − 4" reads as if Erdős–Nathanson–Sárközy improved Veljjanoski's bound. It was this site's adaptation two days ago. (The figure is consistent with their proof, which gives about 4k − 4.)
- **What is fairly credited.** The counting is credited to Hamidoune–Rødseth, the filling step and the sharp example to Veljjanoski, and the tools to Erdős–Nathanson–Sárközy. The honest novelty claim is narrower than the page's: the sharp constant for different summands under the Erdős–Graham hypothesis, made from known parts.

## 5. Readability

- **"Label (b) means the proof is complete apart from two named theorems".** The proof also uses Olson's lemma and Kneser's theorem for finite groups (I believe that version is in the same 1953 paper, but the page should say so).
- **"Let A be a set of positive integers with lower density δ".** The example has density 2/m ≥ δ, so the statement should say "at least δ" (or the example should be thinned to density exactly δ).
- **"The question … Erdős and Graham asked whether…".** This is one of several parts of #338; the main question asks for necessary and sufficient conditions.
- **"for sets whose finite deletions all have the same order h, is the restricted order bounded in terms of h alone?"** The Erdős–Graham question asks whether a restricted order exists at all, not whether it is bounded in terms of h.
- **"checked every step by hand".** Odd wording for an AI referee.
- **"two of the three sources our draft cited…".** Internal draft history that readers don't need.
- **"Today's answer: exactly ⌊2/δ⌋ − 1."** Placed right after the problem statement, a non-specialist may read this as answering #338 itself.

## The three changes I would insist on before publishing

1. **Fix the literature and credit claims.** Withdraw "no explicit bound of the form c/δ in print". Cite Hegarty 2009 Lemma 3.3 (4/d, built as Kneser then Klopsch–Lev) and Chen–Yu 2023 (δ > 1/2 gives 2). Reword "What we add" to the sharp constant for different summands. Fix the title: state the hypothesis and δ ≤ 1/2, and say σ-finite groups, not polynomial rings.
2. **State Olson's lemma correctly and put the four-line count on the page.** Use the form "|Z + S′| ≥ min(g, |Z| + |S′|/2)", which is how Hamidoune–Plagne state it. Replace the deferred case split and the "cruder … ⌈2/δ⌉ − 1" sentence with the short argument from section 1, and fix "add classes one at a time".
3. **Make the remaining steps checkable on the page.** Handle members repeated more than twice, define k as a definition, say "lower density at least δ", and add Ackelsberg–Richter to the sources. Describe the 1.6 million cases as pairs where Z + S′ is not everything, reconcile the "30 of 35" control, and describe the Formal Conjectures merge accurately (the statement plus a link to Veljjanoski's Lean proof registered with Palomar).

My scratch code and outputs are in /tmp/blind338/; downloaded papers are in /tmp/blind338/dl/.

Sources: [Hamidoune–Rødseth PDF](https://journals.msp.org/mscand/article/view/1041), [Hamidoune–Plagne PDF](https://www.cmls.polytechnique.fr/perso/plagne/2004-079-001-08.pdf), [Erdős–Nathanson–Sárközy reprint](https://static.renyi.hu/~p_erdos/1988-33.pdf), [Hegarty arXiv:0904.1871](https://arxiv.org/pdf/0904.1871), [Ackelsberg–Richter arXiv:2604.12864](https://arxiv.org/pdf/2604.12864), [Ramaré–Ruzsa](http://www.numdam.org/item/JTNB_2001__13_2_559_0.pdf), [Hegyvári–Hennecart–Plagne 2007](https://www.cmls.polytechnique.fr/perso/plagne/Erdos-Burr.pdf), [zbMATH/MaRDI entry for Chen–Yu, "On the restricted order of two"](https://portal.mardi4nfdi.de/wiki/Item:Q6046163), [Bienvenu–Hennecart arXiv:1911.07745](https://arxiv.org/pdf/1911.07745), [Chalmers record for Hegarty](https://research.chalmers.se/en/publication/?id=94784).