# Hostile referee report: Erdős #51, CLAIMS_v1 + v1.1 addendum

Referee: claude-opus-5-5, 2026-10-21. My scripts are in `/tmp/ref51/scripts/` (`dp23.py`, `brute.py`). Nothing in `~/MathDyad/erdos51` was touched except this file.

**Bottom line.** I could not refute any theorem. Every step checks at the level of valuations, and Theorem 1 is actually *sharper* than stated: ℓ(a_K) = n_K exactly. The defects are all in the surrounding prose:

- one false inequality about an infinite product;
- one false justification in the notation line;
- a misleading Fermat parenthetical in C1;
- an overclaim about what a YES answer "needs";
- a C6 conclusion that is weaker than it reads;
- a gloss attributed to Tao.

The y = 2 case of Theorem 1 is Carmichael's 1907 result, so Theorem 1 generalises a classical observation rather than being wholly new.

---

## 0. Notation line: HOLDS WITH FIXES

> "an infinite set A with n_a/a → ∞ exists iff sup R = ∞, since each value is attained finitely often"

The equivalence is true, but the stated reason is false. R-values *are* attained infinitely often. For example, ℓ(2·3^j) = 3^{j+1}, so R = 3/2, whenever 2·3^j + 1 is composite (j = 3, 7, 8, 10, …).

**Fix:** use the correct reason. Each R(a) is finite, so sup R = ∞ gives a sequence of *distinct* a with R → ∞.

I verified the 2-seed ℓ(5888) = 11985 by a φ-sieve.

## 1. Lemma 0 and the decomposition: HOLDS WITH FIXES

**Lemma 0 is correct.** ℓ(a) ≤ n_0 gives R(a) ≤ n_0/φ(n_0). The hypothesis on the shape of a is redundant. The identity φ(2^X 3^{Y+1}) = 2^X 3^Y holds for X ≥ 1.

**The swap is correct.** φ(2^e F_s) = 2^{e−1+2^s} = φ(2^{e+2^s}), and 2^{e+2^s} < 2^e F_s. This works for every e ≥ 1.

**Objection A.**

> "(< 2, since ∏_s (1 + 2^{−2^s}) < 2)"

This is false as written. ∏_{s≥0}(1 + x^{2^s}) = 1/(1−x), so the full product equals **exactly 2**.

**Fix:** ℓ has finitely many prime factors, so T ≤ ∏_{s≤S}(1 + 2^{−2^s}) = 2(1 − 2^{−2^{S+1}}) < 2. Alternatively, use the fact that F_5 through F_32 are composite.

**Objection B.**

> "T = 2 if 4 | ℓ, else ∏ over Fermat primes…"

The "else" branch silently contains the case 2 ∥ ℓ, where this formula would lose the factor 2.

**Fix:** state that ℓ(a) ≢ 2 (mod 4) for a ≥ 2, because φ(n/2) = φ(n) when n ≡ 2 (mod 4). I checked this: there are 0 exceptions for a ≤ 10^6, and 0 in the 2^X 3^Y DP.

## 2. Theorem 1: HOLDS, and is sharper than stated

**Every step checks:**

- r | m implies r − 1 | φ(m) = a_K. Since a_K is y-smooth, r ≤ y or r ∈ Q_y.
- **Prime powers.** If r > y then r ∥ m; otherwise r | a_K, which is impossible. So no r^f issue arises.
- If p ∤ m, every r | m has r ≠ p, so v_p(φ(m)) = Σ_{r|m} v_p(r−1).
- The case **p = 2** goes through unchanged (m is odd).
- **No off-by-one:** v_p(a_K) = K − 1 + Σ_{r≤y} v_p(r−1) exactly.

**Improvements:**

**(i) Tighter threshold.** The Σ_{r≤y} terms cancel exactly, so the threshold can be K − 1 > Σ_{q∈Q_y} v_p(q−1).

**(ii) Resolve the garbled clause.**

> "(and by Lemma 0, = it... ≤ it)"

n_K is a y-smooth preimage, so R(a_K) ≤ ∏_{p≤y} p/(p−1). But every extra prime q ∈ Q_y dividing m multiplies R by q/(q−1) > 1. So R(a_K) equals the product, m has no Q_y factor, and matching valuations forces m = n_K.

**State it as:** *if Q_y is finite, then ℓ(a_K) = n_K for all large K.*

**Sanity check at y = 2.** The known Fermat primes give Σ v_2(q−1) = 1+2+4+8+16 = 31. The theorem then gives ℓ(2^k) = 2^{k+1} for all k ≥ 32. That is exactly Carmichael's threshold, and it is sharp: at k = 31 the odd number 3·5·17·257·65537 is the smaller preimage. It also matches OEIS A387221 (ℓ(2^k) = 2^{k+1} for k = 32…36). There is no off-by-one.

## 3. Corollaries C1–C4

**C1: HOLDS WITH FIXES.**

> "for y = 2 this is the Fermat-prime question"

This case can never arise. C1 needs ∏_{p≤y} p/(p−1) > sup R ≥ 11985/5888 = 2.0355 (2.0434 using OEIS A393265). For y = 2 the product is exactly 2.

Worse, Q_2 is heuristically *finite*, so listing it among the "open infinitude" statements misleads. Drop it.

The first relevant y is 3, and only if sup R < 3. The honest conclusion of a NO answer is "Q_y is infinite for some y", i.e. lim inf_p P(p−1) < ∞.

**C2: HOLDS.** 2 · 3/2 · 5/4 = 15/4 ✓. If Q_5 is finite, then R(a_K) = 15/4 > 3, which gives a 3-seed. The conclusion allows γ = 0, so it is implied by Pierpont-infinitude. That is fine, but say so.

**C3: HOLDS.** The "infinitely many K" version is just the contrapositive of Theorem 1 (Q_3 finite ⇒ R(a_K) = 3 for all large K). The bracketed O(1) sketch is unnecessary.

I reproduced the DP independently:

- 402 Pierpont primes 2^α 3^β + 1 > 3 with α ≤ 120 and β ≤ 80.
- An exact 0/1 knapsack over integers.
- A brute-force sieve agrees on all 129 values a = 2^X 3^Y ≤ 10^6.

Results:

- **Maximum:** R − 2 = 9.04·10^{−21}, attained at (X, Y) = (98, 1).
- **Above 2:** 23 cells have R > 2, and none reach 2 + 10^{−19}.
- **Diagonal** 2^K 3^{K−1} (K ≤ 81): max R = 1.5, at K = 1.

**Claim confirmed.**

**C4: HOLDS.** The products 3.75, 4.375, 4.8125 and 5.21354 are correct. Remove the "?": y = 13 is right for k = 5. Strictness was handled correctly (y = 3 gives exactly 3, which is not > 3).

## 3b. Addendum: Theorem 1S, C5, C6: HOLDS WITH FIXES

**Theorem 1S** is valid by the same proof, and gets the same sharpening: ℓ(a_K) = n_K.

**Is φ-closedness exactly what the proof needs? No.** It is used exactly once: to make a_K S-smooth, so that r − 1 | a_K forces r ∈ S ∪ Q_S. It is sufficient but not necessary.

For a non-closed S, write a_K = D · (S-unit), where D is the S-free part of ∏_{p∈S}(p−1) and does not depend on K. The proof goes through verbatim with Q_S replaced by {primes r ∉ S : r − 1 ∈ d·⟨S⟩ for some d | D}. φ-closedness is the case D = 1. The statement "(this forces 2 ∈ S …)" is correct.

**C5 numerics are correct:**

| S | ∏ p/(p−1) | φ-closed? |
|---|---|---|
| {2, 3} | 3 | yes |
| {2, 5} | 2.5 | yes |
| {2, 17} | 2.125 | yes (16 is a power of 2) |

All three exceed 2.0355, so none of the hypotheses is already refuted by data. {2, 257} gives 2.0078 and {2, 65537} gives less, so both are vacuous: the list of Fermat cases is complete. Note that "sup R < 3" cannot be relaxed to "≤ 3".

**C6: arithmetic correct.** 3q/(q−1) > 3. S = {2, 3, q} is φ-closed because q − 1 is 3-smooth. The listed q are correct; the next ones are 109, 163, 193. But:

> "for EVERY prime q ≥ 5 … infinitely many primes of the form 2^α 3^β q^γ + 1"

Here γ = 0 is allowed, so every instance is implied by "infinitely many Pierpont primes". The "for EVERY" ranges over an infinite set only if Pierpont primes are infinite, and then every instance is trivial.

**Honest form:** no 3-seed ⇒ either infinitely many Pierpont primes, or, for each of the finitely many Pierpont q ≥ 5, infinitely many primes 2^α 3^β q^γ + 1 with **γ ≥ 1**. C6 at q = 5 is exactly C2, since Q_5 = Q_{{2,3,5}}.

## 4. "Open for every fixed y": HOLDS

I found no fixed y for which Q_y is proved infinite, and no citation that states the general fixed-y question verbatim. I did find an a-fortiori citation [LMP13]:

- "Q_y is infinite for some fixed y" implies "for every ε there are infinitely many p with P(p−1) < p^ε".
- [LMP13] says the latter was unknown in 2013.

Everything since then is for y growing with p, so none of it counts:

- Baker–Harman (exponent 0.2961);
- Lichtman (β > 0.2843);
- OpenAI's unrefereed September 2026 preprint (every ε, i.e. P(p−1) ≤ p^ε).

For y = 3 there is also #1055 / Guy A18 (the p−1 variant).

**Fix the wording:**

> "open for every fixed y"

should become: "no fixed y is known; NO ⇒ ∃y with Q_y infinite, which is open (a fortiori from [LMP13])". Also note that y = 2 is open but conjecturally false.

**"Where this sits": two more objections.**

**(a) Gloss attributed to Tao.**

> "the precise form of Tao's 'very difficult with current technology'"

Tao said nothing about smooth-shifted primes. This is our gloss. Write "consistent with", and credit Kovač's comment (quoted below) as the nearest forum precursor.

**(b) Overclaim about YES.**

> "YES direction needs, for each y, exponent vectors where every cover by smooth-shifted primes is blocked"

This is an overclaim. A YES witness need not be y-smooth, or of the a_K shape. Large R only needs Σ_{r|ℓ} 1/r to be large, and that could come from a non-smooth a. Rewrite as "one route to YES".

## 5. Novelty: PARTIAL PRIOR ART

- **y = 2 is classical (Carmichael 1907).** I have it second-hand, via the zbMATH review of Gupta 1981 and OEIS A002181. I did not read Carmichael's original.
- **The swap mechanism linked to smooth-shifted primes is already on the forum** (Kovač, 28 Aug 2025).
- **The general Theorem 1, or its contrapositive** ("bounded ⇒ infinitely many smooth-shifted primes"), **was not found** in anything I searched. That is a coverage statement, not proof that it does not exist.

**Verdict:** present Theorem 1 as an elementary generalisation of Carmichael's Fermat-prime observation, credit Kovač for the heuristic, and do not call it a new theorem.

**Searched:**

- erdosproblems.com #51, #694, #1055 and #203 (pages and threads, fetched via Hetzner because exe.dev gets a 403);
- the OpenAI preprints 024 ("number of totients", by grep for Fermat/Pierpont/smooth/seed) and "Weighted dilation graphs, smooth shifted primes and totient fibers" (abstract, introduction and references);
- Granville's *Smooth numbers* survey §5.3;
- arXiv 1311.2527;
- Wikipedia and OEIS A005109;
- web searches on Pierpont / S-smooth p−1 / least inverse totient;
- `world.md`'s earlier zbMATH, arXiv and MathOverflow sweep.

**Not read:** Guy B36, B39 and A18 (no copy available), and Carmichael 1907 in the original.

---

## Citations (verbatim quotes)

1. **Luca, Menares, Pizarro-Madariaga, "On shifted primes with large prime factors and their products", arXiv:1311.2527 (2013), p. 1:**

   > "The extreme cases P(p − 1) = 2 and P(p − 1) = (p − 1)/2 correspond to Fermat primes and Sophie-Germain primes, respectively. Not only do we not know if there are infinitely many primes of these kinds, but we do not know whether for each ε > 0 arbitrarily small there exist infinitely many primes p with P(p − 1) < p^ε or P(p − 1) > p^{1−ε}."

   This establishes, a fortiori, that the fixed-y question was open as of 2013.

2. **erdosproblems.com/1055 (Erdős–Selfridge classes; [Er77]; Guy A18; OPEN):**

   > "Are there infinitely many primes in each class? … A similar question can be asked replacing p+1 with p−1. This is problem A18 in Guy's collection."

   Class 1 of the p−1 variant is exactly the Pierpont primes (OEIS A005109: "Class 1- (or Pierpont) primes").

3. **Wikipedia, "Pierpont prime":**

   > "It has been conjectured that there are infinitely many Pierpont primes, but this remains unproven."

   The conjecture is due to Gleason, Amer. Math. Monthly 95 (1988) 185–194.

4. **OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sep 2026, unrefereed):**

   > "for every ε > 0 there are infinitely many primes p with P+(p − 1) ≤ p^ε."

   It also says "These results concern fixed positive exponents" (about the prior literature). Its smoothness bound grows with p; it says nothing about fixed y.

5. **Kovač, #51 forum, 28 Aug 2025:**

   > "the possibility of such swapping procedure is related to questions like #203, where one would use such prime p to replace some powers of 2 and 3 from a. But already these questions seem to be too difficult."

   This is the closest precursor to the barrier. In the same thread on the same day (00:31): "if there were infinitely many Fermat primes, then their products … would be good examples."

6. **Tao, #51 forum, 10 Aug 2025:**

   > "Most likely the answer is negative … Intuitively, if n has too many prime factors, it should be possible to swap out some prime factors for others … But it looks very difficult to prove this rigorously with our current analytic number theory technology!"

   He makes no mention of smooth-shifted primes.

7. **Gupta 1981, zbMATH review (second-hand, via `world.md`):**

   > "Assuming that 2^k+1 is composite for k>16 it is shown that v_o(2^k)=1 if 0≤k≤31 and v_o(2^k)=0 if k≥32. This was first proved by R. D. Carmichael [Bull. AMS 13 (1907)]."

   This is Theorem 1 at y = 2, with the same threshold.

8. **OEIS A002181 (T. D. Noe):**

   > "If there are only five Fermat primes, then terms will be even for 2m = 2^r for all r > 31."
