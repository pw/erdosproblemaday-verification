**Referee report: Erdős #700(b), Tresmontant's proof and the lead's corollaries C1 and C2**

## Verdicts
| Item | Verdict |
|---|---|
| Step 1 (reduction and the three pair cases) | **HOLDS** (a few steps are asserted without derivation, but each is true) |
| Step 2 (Lemma, Chebyshev, infinitude) | **HOLDS** |
| C1 (f(n) = pq exactly) | **HOLDS** |
| C2 (count ≫ X^{1/3}/log X) | **HOLDS** (true, but a weak bound) |
| Novelty as an answer to (b) | **NOT NEW.** Earlier three-prime proofs exist (see section 4). The Maynard-free Step 2 may be new. |

I could not refute any line of the mathematics. The serious finding is about priority, not correctness.

## 1. Line-by-line check

**Background facts.** All of these check out:
- e ≥ 6 is forced. All three primes are odd (p > 2e² ≥ 72), so d ≥ 2 and h ≥ d+2.
- d+2e < p holds because 3e ≤ e² for e ≥ 3.
- r < 2p holds because e < √(p/2) < p. Then r < 2p ≤ pq, so r² < n.
- "Small k" never matters: if neither prime divides C(n,k), then k = s·t·j and j ≤ u/2.

**Digit identities.** I checked all eight expansions symbolically with sympy, and every one is exact. Where a digit range is asserted, it holds.

**Quoted sentences I object to.** None of these is a gap of substance:
1. *"We show that for each pair one of them fails."* This is only literally true for the pair (p,q). For (p,r) and (q,r), the base-p or base-q condition first bounds j (j ≤ d, or j < e), and only then does the base-r condition fail. So the honest wording is "the two conditions cannot both hold".
2. *"Write dj=cq+x, 0<x<q."* x ≠ 0 needs q ∤ j. That is true because j ≤ r/2 < q, but the reason only appears in the next sentence.
3. *"with j-c-1 a single digit (j<=r/2<q)"* also needs j−c−1 ≥ 0. That holds because c < dj/q < j, but it is unstated.
4. *"(ej=cp+x', j+c<p)"* is asserted without derivation. It follows from j ≤ (q−1)/2, c < e and d+2e < p, which is where "d+2e<p" gets used. The same applies to *"j+c<q"* in the pair (q,r): use c < h/2 and p/2 + h/2 < q.
5. *"pj=(j-1)r+(r-ej)"* needs ej < r. That uses j ≤ d from the base-p step (ej ≤ ed < p < r), which is not said.

**Your specific questions:**
- *"r<=e(j+h)" direction:* correct. The base-r digit needs r − ej ≤ eh, i.e. r ≤ e(j+h). Then e(j+h) ≤ e(d+h) = e² < p < r, a contradiction. The (q,r) analogue h(j+e) < e·2e = 2e² < p < r is also right.
- *Lemma:* the index range is 1 ≤ i ≤ M−2. Any i satisfying the inequality is automatically ≤ M−2, since for i = M−1 the left side is 0. M ≥ 3 follows from M > 2 + log₂L with L ≥ 1. The proof S_i ≥ 2S_{i+1} ⇒ L ≥ S₁ ≥ 2^{M−2} is correct, using S_{M−1} ≥ 1.
- *Chebyshev step:* π(2x) − π(x) ≫ x/log x is enough. The average count per window is about x^{1/3}/log x, which exceeds 2 + log₂ x^{1/3} for large x. Also e < x^{1/3} ≤ p^{1/3} gives 2e² < p once p > 8.

**C1.** The lower bound follows from the theorem, since pq is the smallest product of two of the primes. For the upper bound with k = r:
- pq in base r is (eh, r−e−h), and 1 ≤ eh, so r ∤ C(n,r).
- r mod p = e ≠ 0 and r mod q = h ≠ 0, so p and q both divide C(n,r).
- This is the Erdős–Szekeres bound f ≤ n/P(n), attained.

**C2.** Each run of the Lemma needs at least m points of spread ≤ L, and stays valid as primes are removed. The process gives at least (M−m)/3 disjoint triples per window. Windows with M < m only lower the sum, so summing (M−m)/3 over all windows is a valid bound. W·m ≈ x^{2/3} log x = o(x/log x). Distinct prime triples give distinct n by unique factorisation, so disjointness isn't even needed for that. Taking x = (X/8)^{1/3} gives the bound.

The bound is weak: triples alone heuristically give about X^{2/3}/log³X. Also, 60 composites up to 1200 already have f > √n (30, 70, 84, 105, …), and most are not of this shape.

## 2. My program
Everything is in `/tmp/e1122/seat700/`, written from scratch: `ref700.py` plus the stage scripts. I compute f three independent ways:
- **literal:** gcd with `math.comb`;
- **Legendre:** valuations over every k up to n/2;
- **Lucas-set:** enumerate the k that each prime fails to divide and intersect the sets. This does not use the proof's reduction.

**Cross-validation:**
- Literal vs Legendre for every n from 4 to 1200: 0 mismatches.
- Lucas-set vs literal on all 533 squarefree composites up to 1200: 0 mismatches.
- Legendre vs both Lucas methods on 6,618 prime triples: 0 mismatches. This covers all triples with n ≤ 2·10⁴, 1/15 of those up to 3·10⁵ and 1/120 of those up to 2·10⁶; 407 have f > √n, and both r < pq and r > pq occur.
- The original `validate.py` timed out (exit 124) after these checks; `validate2.py` replaced its triple-comparison stage.

**Theorem and C1, exhaustive** (`b1_*.out`):
- My own enumerator finds exactly **2,952** hypothesis triples with p ≤ 6000 and **24,601** with p ≤ 20000, matching both the submitter and the lead.
- I computed f exactly for all 24,601: **f = pq in every case**, so none has f ≤ √n. This includes 1,550 triples with e within 1 of the largest allowed value and 1,959 with d = 2.
- The smallest admissible triple is (101,103,107).

**Large-p edge cases** (Lucas-set): f = pq for all of these.
- d=2, h=4: p = 51131, 100517, 300317, 1001087, 2000387 (n ≈ 8·10¹⁸).
- Largest allowed e near p ≈ 3·10⁴, 6·10⁴ and 10⁵, with d = 2 and d ≈ e/2, e.g. (100391,100393,100613) and (100169,100279,100391).

**Pure Legendre brute force over every k**, up to n = 1.3·10⁹: f = pq in all seven cases.
- (101,103,107)
- (419,421,433) and (443,449,457): e = 14 at the smallest p allowed
- (809,811,829) and (1013,1021,1033): e = 20
- (1009,1019,1031): e = 22, the largest allowed
- (1091,1093,1097)

The control 103·107·113 gives f = 107 < √n (√n ≈ 1115), as the submitter says.

**Sharpness:**
- Among triples with p ≤ 3000 and e² < 2p, f = p in all 4,349 with h ≤ d, in every size band. This is consistent with our July page's "f = p if the gaps do not increase".
- With h > d but p/2 ≤ e² < p, 570 of 1,053 fail. The smallest failure is (41,43,47).
- With h > d and p ≤ e² < 2p, only 39 of 2,254 have f > √n.
- **The constant is asymptotically sharp:** failures occur at 2e²/p = 1.069, for example (11969,11971,12049) with f = p, and the closest failures all have d = 2. The argument predicts this: in the pair (q,r), h(j+e) ≈ 2e² − O(e).

## 3. The lead's `check700.py`
**It can go red.** I loaded only its function definitions and tested them:
- `small_gcd_exists` returns True on 103·107·113, 457·461·463, 101·107·109 and 1009·1019·1021.
- On 1,472 random triples with r < pq it agreed with my exact f every time, in both directions (11 had f > √n).
- On 568 triples with p = 2 it also agreed. The lead never tests p = 2, because `primerange` starts at 3.
- **Mutation test:** I loosened the hypothesis to 2e² < 2p (p ≤ 2000). The lead's exhaustive logic then flags 270 triples, each confirmed f < √n by my code. At 2e² < 3p it flags 799.
- Its two-sided validation set is real: 4,634 triples with f ≤ √n and 527 with f > √n.

**The "reduced" test is only valid when r < pq.** That is correct: when r > pq, the single-prime gcd pq is already below √n and the test ignores it. The 70 disagreements in the first version were all r > pq cases. The hypothesis forces r < 2p ≤ pq, so the test is valid where it is used.

**Defects to fix:**
- (a) `check700_6000.out` is stale. It is timestamped 09:11, before the script was edited at 09:17. It holds 70 DISAGREE lines and ends "SOMETHING UNEXPECTED", yet the README cites it. Rerun it.
- (b) The README says "all 5,161 prime triples with r < pq and n ≤ 3·10⁶". In fact it is only primes from 3 to 139. The full set of odd-prime triples with r < pq and n ≤ 3·10⁶ has 107,741 members.
- (c) The script runs its controls through `f_brute` only, not through the detector the exhaustive loop uses. My probes cover that gap.
- (d) The `isprime(471)` construct is dead code: 471 = 3·157, so it always falls back to (457,461,463).

## 4. Novelty: the main finding
- **Our own page [/day/700-gcd-binomial](https://erdosproblemaday.com/day/700-gcd-binomial) (24 Jul 2026)** already states the three-prime theorem plus Maynard: p > 10D², f = pq if the gaps increase, f = p otherwise. The lead's update already links it.
- **FC issue [#6704](https://github.com/google-deepmind/formal-conjectures/issues/6704)** (opened 30 Sep, citing that page). A contributor declined to retag it as solved on 21 Nov because there was no rigorous write-up. Tresmontant's proof could now be that write-up.
- **[aichiwuhuarou/jsp-000570-lean](https://github.com/aichiwuhuarou/jsp-000570-lean) README (20 Sep)** and Justin Sun Prize PR #657 (17 Sep) say that erdosproblems.com/700 credits the "three-prime / 2/3-exponent result" to **"GPT 5.6 Sol Pro prompted by Liam Price"**. They cite an Overleaf manuscript using a "Lucas–Maynard strategy" and call (b) "the already answered square-root infinitude question".
  - That repo also Lean-verifies a **four-prime** criterion: f(P(P+a)(P+b)(P+c)) = P(P+a)(P+b), given 1 ≤ a, 3a ≤ b, 3b−a+1 ≤ c and 12c³ ≤ P. That is an exponent-3/4 family (its infinitude step uses Maynard and is not formalized).
  - It also has a Lean counterexample at c = 3b−a, with P = 25480409371. The work is mirrored in competemath/tengoku.
  - **I could not confirm the credit line first-hand.** The Overleaf link renders only with JavaScript, and erdosproblems.com is behind the wall. Someone (Patrick) should check the problem page.
- **What may still be new in Tresmontant's proof:** the Maynard-free infinitude step (Chebyshev plus the doubling lemma), and the explicit, essentially sharp hypothesis 2e² < p. C1 matches the July page's dichotomy and, presumably, the predecessor. C2 is probably new but trivial.
- **Where I looked:**
  - arXiv API: several queries. Nearest hits are 2611.25794 (Cui–Yang on the distribution of gcd(n, C(n,k))), 2606.22997, 2606.20940, 2609.37754 and 2610.01328. All are different questions.
  - MathOverflow and the web: nothing besides our page.
  - GitHub: code and issue search, including FC, teorth (still "open", last updated 2025-08-31), lean-genius (stale), tengoku and jsp570.
  - OEIS A091963: blocked by Cloudflare.

## What I could not check
- The Liam Price / GPT manuscript, its date and its exact hypotheses.
- The current erdosproblems.com/700 text.
- OEIS A091963's comments.

**Process notes:**
- My first `tests.py` B1 run timed out (exit 124); I reran it as three p-ranges, all complete.
- One run was started with `timeout 3000` by mistake. I stopped it and restarted it with `timeout 1800` as instructed.