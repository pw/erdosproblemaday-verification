GAP — every cited source I checked says what the paper says it does. The novelty framing leaves out a public prior: a certified, publicly posted Lean proof of the c = 2 case (erdosproblems #416(i)), accepted 14 Sep 2026. That is 11 days before the paper's date and 22 days before the public release. Nothing I found refutes the paper's literature claims. Its own claim to novelty is the asymptotic formula and general c > 0.

Seat W (world and sources), Erdős #416, OpenAI "An asymptotic formula for the number of totients" (25 Sep 2026; local repo at commit 1581d4cb).
Working files are in /tmp/oaimath/024/seats/W_work/ (subdirectories ford/, src/, cio_dl/, zer/, fc/, teorth/, scripts/).

## Findings

### 1. Priority: a conjectures.io Lean proof of V(2x)/V(x) → 2 predates the paper, and the paper does not mention it
- **Severity:** exposition / attribution. It is not a mathematical defect, but it does qualify the paper's novelty framing.
- **Paper, printed §1, p. 2:**
  - "We obtain an explicit asymptotic equivalent and prove the fixed-scale limit, thereby answering this question of Erdős and Hall positively."
  - Neither conjectures.io, JenW1N, nor Zeraoulia appears anywhere in paper.txt (checked with grep).
- **Dates, from the saved page /tmp/oaimath/024/live/cio_result.html, re-fetched live today with the same content:**
  - "Verified 14 Sept 2026"
  - "Approved · decided 15 Sept 2026"
  - "Certified 16 Sept 2026, published by conjectures.io."
  - Review text: "The submission was accepted on 14 September 2026 at 04:31:57.787556 UTC."
  - Solver: "JenW1N".
  - "Axioms permitted: propext, Quot.sound, Classical.choice"
  - "Checked in 16 min 37 s"
  - Proof SHA-256: af5e0facfbfca599610dc80e9c1a484c5fa50c8ce23a7aef409ff6ff32e751a1.
- **Source I downloaded:**
  - Today's download of `.../results/51923647-.../solution/download` hashes to that same SHA. It is 64,775 lines and saved as W_work/cio_dl/solution_Main.lean.
  - Target: `Bounty.target : fcTypeOfName% "Erdos416.erdos_416.parts.i"`, proved by `exact Erdos416Proof.Simplified.doubling_limit` (lines 64567–64568).
  - The proof covers the case c = 2 only.
- **The reviewer's own caveat:** "No fresh Lean replay, separate complete axiom export, exhaustive line-by-line audit of the 64,775-line proof or proof of originality is claimed." I did not replay it either.
- **Public on erdosproblems.com:**
  - The #416 proof-claims tab (/tmp/oaimath/024/live/part1.txt) shows "A proof claimed by conjectures.io … Submitted 2026-09-27 13:20:29 by Thomas Bloom".
  - Bloom wrote: "I have not verified the proof yet, and do not claim that the formalisation is correct … It is also not transparent (e.g. of who is running these through the AI, how long for, and which AI)."
- **Timeline of the OpenAI paper (GitHub API):**
  - The openai/math repo was created 2026-10-06T21:47Z.
  - The paper's first public commit is adc7f124 at 2026-10-06T21:58:50Z.
  - `git diff --stat adc7f124 1581d4cb` over the preprint directory is empty, so the reviewed text is the text released on 6 Oct.
  - So the cio proof was public about 3 weeks before the release. It predates the paper's internal date (25 Sep) as well.
- **What the paper still has first, as far as I can find:**
  - all c > 0;
  - the explicit equivalent V(x) ∼ (x/log x) G_m A(1;θ);
  - the N_k companion.
  - Erdős–Hall's question is "for every c > 1", and cio proves only c = 2.

### 2. Route of the conjectures.io proof
- **Severity:** information.
- **The exposition PDF is gone.** `https://conjectures.io/papers/erdos416i.pdf` returns HTTP 404 live (a "Not found · Conjectures.io" page of 38,159 bytes). The saved copy /tmp/oaimath/024/live/erdos416i.pdf is that same 404 page.
  - Positive control: the problem page on the same host returns 200, so this is a real 404, not a block.
  - Wayback has no snapshot: availability API returns `"archived_snapshots": {}`. The Wayback CDX service was "Temporarily Offline".
  - So the prose route cannot be read anywhere I could reach.
- **The route, as read from the Lean docstrings (not audited):**
  - It covers totients by "core pairs" (b, p) with value (p − 1)·b, where b = φ(a) and P⁺(a) < p (`corePairValue`, line 730; `corePairValue_is_totient`, line 778). In other words it counts via the largest prime.
  - It proves three things:
    - coverage of all but εV(y) values;
    - collisions o(V);
    - a "prime-counting imbalance" (`(Q y).card − 2·#{f ≤ y/2}` = o(card)) that halves the count when y is halved.
  - Theorems used: `doubling_of_power_raw_counting_contracts` and `doubling_limit`, at lines 64484–64563.
  - Inputs:
    - Ford's S-normal primes: "Ford's normality predicate", line 682.
    - Ford's polytope and Lemma 3.2 / Corollary 3.3 / (3.3) / (3.6): lines 36012–37439.
    - A multi-form collision sieve: "two-form Selberg sieve", line 22431; "collision-class sieve", line 33807.
    - The PNT project.
  - This is the same Ford-based skeleton as OpenAI's printed §6 ("Counting the largest prime with common endpoint parameters first gives regular variation"). Unlike OpenAI's paper, it does not identify a limiting coefficient.
- **Who did it first internally cannot be determined** from public data.
- **Side finding about Ford.** The cio source contains (line 38755): "The unnormalized all-index inequality printed on Ford page 15 fails at i=1; the volume ratio actually requires A_i>4*g_i". I checked this; see finding 7.

### 3. Rafik Zeraoulia's claim (29 Jul 2026): what it proves, and its table
- **Severity:** information. The paper does not cite it; the result is subsumed if OpenAI's theorem holds.
- **Repository:** github.com/rafikmath15/fixed-scale-totient-limit-points. It was created 2026-07-29T06:11Z with a single commit, daf7c87969 (2026-07-29T06:12:40Z).
- **Main result**, quoted from the PDF (zer.txt), Theorem 1.1:
  > "For every fixed real c > 1, lim inf_{n→∞} |V(cn)/V(n) − c| = 0. More precisely, for every function L(X) → ∞, a near-hit occurs at an integer n ∈ [X, cXL(X)]. The complete cluster set of V(cx)/V(x) is a closed interval containing c."
- **The author's own scope statements:**
  - "This is partial progress … It is **not** a proof that V(cx)/V(x)→c" (README).
  - "no estimate in this paper controls the width of the cluster interval".
- **Method:** Ford's bounded-factor estimate, plus exact telescoping over the scales c^j, plus the unit jumps of V.
- **Table**, copied verbatim with sources:
  - From `data/selected_values_1e10.csv`, lines 2–5 and 7, plus `data/selected_values.csv`, lines 2–4; the same values appear in `data/totient_ratio_grid_1e10.csv` at lines 2/11/101/1001/5001 and in PDF Table 1:

| x | V(x) | V(2x) | V(2x)/V(x) | source |
|---|---|---|---|---|
| 10^3 | 291 | 543 | 1.8659793814433 | selected_values.csv:2 |
| 10^4 | 2374 | 4486 | 1.88963774220725 | selected_values.csv:3 |
| 10^5 | 20254 | 38992 | 1.92515058753826 | selected_values.csv:4 |
| 10^6 | 180184 | 349297 | 1.9385572525862451 | selected_values_1e10.csv:2 |
| 10^7 | 1634372 | 3183543 | 1.9478692733355687 | selected_values_1e10.csv:3 |
| 10^8 | 15037909 | 29395153 | 1.9547367256977017 | selected_values_1e10.csv:4 |
| 10^9 | 139847905 | 274107751 | 1.9600418826438624 | selected_values_1e10.csv:5 |
| 5·10^9 | 667935656 | 1311179363 | 1.9630324436520274 | selected_values_1e10.csv:7 |
| 10^10 | 1,311,179,363 | — | — | PDF eq. (20); COMPUTATION_CERTIFICATE.txt:9 "V(10^10) = 1,311,179,363." |

  - Notes on the table:
    - V(10^10) appears as V(2x) at x = 5·10^9.
    - V(10) and V(10^2) are not in his files.
    - The scaled deficit (2 − R_2(x))·log x drifts from 0.849 (10^6) to 0.826 (5·10^9).
- **My independent check:**
  - Script: W_work/scripts/vcheck.py, a numpy φ-sieve up to 1.22·10^8.
  - Completeness argument: n/φ(n) ≤ 5.847 for n < 23# = 223092870; for n ≥ 23#, φ(n) ≥ 2.23·10^8/6.12 > 2·10^7. (The script's printed "tail-min" diagnostic is a bad test and should be ignored; this argument is the actual completeness proof.)
  - Results: V(10)=6, V(20)=10, V(100)=38, V(200)=72.
  - It reproduces his values exactly for k = 3…7, and for 2·10^k, k ≤ 7.
  - V(10^6) = 180,184 and V(10^7) = 1,634,372 also match Ford's arXiv Table 1, p. 3 (positive control).
  - I did not independently check his values above 2·10^7.
- **Conjectures.io's assessment of his claim:** "They explicitly leave the interval's width uncontrolled … They do not establish convergence for the exact submitted target."

### 4. Other proofs or criticism (arXiv / web, 2025 to Oct 2026)
- **Severity:** information. This is a coverage claim, not an existence claim.
- **What I searched:**
  - The arXiv API, which was rate-limited mid-run.
  - The arXiv web search UI with six queries, including "number of totients", "distinct values Euler function", "distribution of totients", "Erdos problem 416" and "V(cx)/V(x) totient". Two of these returned empty pages, probably because of the rate limit.
  - WebSearch with four queries.
- **What I found:**
  - No other proof of V(cx)/V(x) → c and no other asymptotic formula for V(x).
  - No public mathematical criticism of the OpenAI totient paper.
  - Press coverage (officechai, 9 Oct 2026) lists only "results on totient values (416 and 821)".
  - Press reports of 3 manuscripts withdrawn on 7 Oct concern other papers. This preprint is byte-identical between adc7f124 and 1581d4cb.
- **Survey prior:** Tenenbaum's survey (Erdős Centennial volume 2013; arXiv 1908.00488v1, final section) mentions only Ford's order result for Φ(x). That is consistent with the question having been open.

### 5. Formal Conjectures, FormalConjectures/ErdosProblems/416.lean
- **Severity:** information, plus one attribution point.
- **History** (GitHub API, path filter): 11 commits.
  - Statement added in 5ff9bc0374b7 (2025-07-29, PR #352).
  - Both `parts.i` and `variants.regularly_varying` were marked solved in 3dfd999dfe5a (2026-10-11, PR #6898, by mo271, "closes #6897").
- **What PR #6898 says:**
  - Commit message: "Newly solved … Erdős … 416 (parts i)", and "New solved variants with proof links: Erdős 416 regular variation".
  - Docstring: "Yes. This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked Lean proof, which gives `V(cx)/V(x)→c` for every fixed `c>0`."
  - Link target: openai/math@adc7f124 …/UnconditionalMain.lean#L12.
  - It does **not** mention the conjectures.io proof, even though that proof was certified on 16 Sep against this very FC statement.
  - A search of FC issues and PRs for "conjectures.io" returns total 0.
- **Why parts.ii stays open:**
  - PR #6898: "Left open on purpose: … Erdős 416 parts ii (the main term needs many auxiliary definitions)".
  - Issue #6907 (open, 2026-10-07, labels `erdos-problems`, `solution found`): "PR #6898 marks `parts.i` solved but leaves `parts.ii` open because stating `mainTerm` needs about 25 auxiliary definitions".
  - So parts.ii is open for formalization overhead, not because of any doubt about the mathematics.
- **Remark on the FC statement:**
  - `erdos_416.parts.ii` is `Tendsto (V x / answer x) → 1`. As a bare formal statement it is satisfied by answer := V.
  - It is a `@[question value]` item, so humans judge the answer. It is not a meaningful machine target.
- **External database:** teorth/erdosproblems data/problems.yaml (repo last commit 2026-10-21T10:30Z) still lists #416 `state: "open"` with `last_update: "2025-08-31"`. It lags, so I treat it as uninformative.

### 6. Cited sources: each place says what the paper claims
- **Severity:** checked; all HOLD unless noted.
- **Ford, arXiv 1104.3264v2:**
  - The arXiv abs page says "[Submitted on 16 Apr 2011 (v1), last revised 14 Jul 2013 (this version, v2)]", and v2 is current.
  - **Theorem 1 (p. 2):** "V(x) = x/log x exp{C(log3 x − log4 x)² + D log3 x − (D + 1/2 − 2C) log4 x + O(1)}". This matches paper (1.1).
    - My recomputation (W_work/scripts/consts.py, mpmath at 30 digits): ρ = 0.542598586098471021959, F′(ρ) = 5.697758934230192675, C0 = 1/(2λ) = 0.8178146400836, D0 = 2.1769687435594.
    - The paper's D0 formula, (1+log(λ/γ))/λ − 1/2 with γ = 1/(ρF′(ρ)), equals Ford's (1.6) D = 2C(1+log F′(ρ) − log 2C) − 3/2 to all 30 digits.
    - λ = 0.61139 (so 30λ = 18.34) and 1.1ρ = 0.597, consistent with the paper's (3.3) remarks.
  - **Theorem 2 (p. 2):** "V_k(x) ≫_ε d^{−1−ε} V(x)". Its proof is in §5.
  - **Theorem 4 (p. 3):** "Consequently, for every fixed c > 1, V(cx) − V(x) ≍_c V(x)."
  - **p. 3:** "Erdős has asked if V(cx) ∼ cV(x) for each fixed c > 1, which would follow from an asymptotic formula for V(x). The method of proof of Theorem 1, however, falls short of answering Erdős' question."
  - **Theorem 10 (p. 5):**
    - (a) holds for 0 < ε ≤ i/(3L0) with the bound V(x) exp{−L0(L0−i)ε²/(4i) + log(i/(εL0))}.
    - (b) holds for i/(3L0) ≤ ε ≤ 1/8 with the bound V(x) exp{−L0 ε/13}.
    - Convention: "we write V(x; C) for the number of totients m ≤ x which have a pre-image n satisfying condition C".
    - The paper's summation for (3.7) applies (a) and (b) in exactly these ranges.
  - **Theorem 16 (p. 29):** ξ_i = 1 + (1/10000)e^{−(L0−i)/40}. The exceptional set "(x_1,…,x_L) ∉ S_L(ξ) or x_L(n;x) ≤ 2/log2 x" is "≪ V(x) exp{−Ψ²/4}".
    - This matches the paper's ξ_i = 1 + 10^{−4}e^{−h_i/40} and its claim at P = Ψ.
    - Ford's (I_{L−1}) is 0 ≤ x_L ≤ ξ_{L−1}x_{L−1}, with coefficient 1. So the paper's "coefficient 1 in place of a1 < 1; weakening that inequality gives (3.8)" is correct.
    - Ford's convention that q_i(n) = 1 for i ≥ Ω(n) (p. 17) makes a missing p_L land in the exceptional set (x_L = 0), as the paper says.
  - **Lemmas and corollaries (pp. 11–13):**
    - Lemma 3.2 and Corollary 3.3 are the ξ-scaling results.
    - Lemma 3.4 and Corollary 3.5 give T_L ≍ ρ^{L(L+3)/2}F′(ρ)^L/L!.
    - Lemma 3.7: "|g_i − λρ^{−i}| ≤ 5, where λ = 1/(ρF′(ρ))". This is the paper's γ, as the paper states.
    - Remark 1: "The above proof is based on [24]". Ford's [24] is "K.-W. Lau, … Solution of Problem 10682, Amer. Math. Monthly 107 (2009)". Ford's year is a typo; Crossref lists 10.2307/2589199 as AMM 107(4):374, April 2000, by Ford and Lau. The paper's [9], dated 2000, is correct.
  - **Definition 1 and Lemma 2.6 (pp. 8–9):** match the paper's Definition 3.1 and (3.9).
  - **Lemma 5.1:** exists, at p. 21.
  - **(5.10)–(5.19):** on pp. 24–25, as cited.
    - The paragraph after (5.18) ends: "In particular, for such n we have φ(n′) ≠ φ(n) for n′ ≠ n and n′ ∈ B."
    - p. 26 has "V_κ(x) ≥ |B|/2 ≫_ε d^{−1−ε} V(x)".
  - **§7.3, p. 39:**
    - "for at least half of the numbers b ∈ B, the totient φ(b)d has only the pre-images bm_i"
    - "For k ∈ {2, 4, 8}, take d = 2^18 · 257"
  - **My check of that example** (scripts/invphi.py, with positive controls φ^{-1}(2) = {3,4,6}, φ^{-1}(4) = {5,8,10,12}, φ^{-1}(6) = {7,9,14,18}, φ^{-1}(54) = {81,162}):
    - φ^{-1}(2^18·257) has 8 preimages, all divisible by 8, none odd.
    - ℓ(d) = 135,268,352, so ℓ(d)/d = 2.0078 > 2.
    - Remark 7.4's k = 2 seed HOLDS.
- **Erdős–Hall, Mathematika 23 (1976), 1–3** (renyi 1976-11.pdf):
  - Title: "Distinct values of Euler's φ-function". The paper's title is right; COMMON.md's "On the values …" is a different paper, Acta Arith. 22 (1973).
  - p. 3, final paragraph: "Finally, we would like to ask the following question: is it true that, for every c > 1, lim V(cx)/V(x) = c?"
  - The theorem holds "for every A < 1/log 16". HOLDS.
- **Erdős [4], Astérisque 61 (1979):**
  - I rendered numdam PDF page 9 and confirmed it is p. 80 from the printed folio.
  - "It is not certain that there is a genuine asymptotic formula for Φ(X) but perhaps Φ(CX)/Φ(X) → C holds for every C > 0."
  - Same page: "estimate the number of integers n < X for which the smallest solution of φ(m) = n satisfies kX < m ≤ (k+1)X. I can at the moment say nothing interesting about this problem."
  - HOLDS for both of the paper's uses.
- **Erdős [5], Resenhas 2(2) (1995), 165–186, §I.9, p. 171:**
  - "Is there an infinite sequence of integers a_1 < a_2 < ... so that φ(n) = a_i is solvable but if n_i is the smallest integer for which φ(n_i) = a_i then n_i/a_i → ∞?" HOLDS.
  - Bibliographic defect: the cited DOI 10.11606/resimeusp.v2i2.74798 does not resolve. doi.org returns 404, the handle API returns `responseCode 100` (not found), and Crossref has no record. The USP journal page prints it anyway. The working URL is revistas.usp.br/resenhasimeusp/article/view/74798. Severity: typo-level.
- **Erdős [1] 1935, §2:** "THEOREM. N(M, n) = o(n(log n)^{ε−1}) for all positive ε". HOLDS.
- **Erdős [2] 1945:**
  - Lemma 1 (p. 540) bounds the solutions of (p−1)a = (q−1)b.
  - The theorem on p. 542 says the number of distinct φ(pr), pr ≤ n, is n(log log n)(log n)^{−1}(1+o(1)), with the proof finishing on p. 543. HOLDS.
- **Erdős [3] 1958, Theorem 4:** "If there exists an integer n with A(n) = k then there exist infinitely many such integers"; the proof works via the "trivial solutions y = pb". HOLDS for the "inverse-fiber preservation" attribution.
- **Maier–Pomerance [10] (scan, OCR'd p. 264):**
  - Equation (1.3) defines a_n = (n+1)log(n+1) − n log n − 1, and (1.4) is F(ρ) = 1.
  - "(1.5) C = 1/(2|log ρ|) = 0.81781465…"
  - "Theorem. V(x) = x/log x exp{(C+o(1))(log log log x)²}". HOLDS.
- **Pomerance [14] 1986, (1.4):** "For every C > … = 1.175018095…, V(x) = O(x/log x exp{C(log log log x)²})". HOLDS.
- **Pollack–Pomerance–Treviño (author version, 17 pp.), Lemma 4.1:**
  - "Fix natural numbers d1, d2 ∈ V … there are ≫_D Z(x) numbers n which satisfy … (ii) n is convenient for both d1 and d2 …"
  - Proof: "a simple adaptation of the lower-bound argument of Ford [8, §5]".
  - Crossref confirms Ramanujan J. 30(3):379–398 (2013). HOLDS.
- **Ford, sieve notes [8], Spring 2023, Theorem 2.5:** a uniform ≪_k bound (x/log^k x)(∆/φ(∆))^k with ∆ = ∏a_i ∏(a_i b_j − a_j b_i). HOLDS.

### 7. Source erratum in Ford (it does not affect the paper as cited)
- **Severity:** information.
- **Ford p. 15**, proof of Lemma 3.4: "Using Lemma 3.7, plus explicit computation of g_i for small i, gives A_i > 4 for all i".
- **This is false as printed at i = 1.** With A_i = g_i + g_{i+1}/(1−a1), I get A_1 = 2.1115 (scripts/ford_p15.py).
- **The normalized version A_i/g_i > 4 holds**, with minimum 4.0030 (at i = 48) and limit 1 + ρ^{−1}/(1−a1) ≈ 4.003. Presumably that is what was meant. The conjectures.io Lean independently flagged the same line.
- **Effect on the paper:** it cites only the conclusion of Lemma 3.4 (for its (3.4)) and derives its own simplex volume. The margin is thin (4.003 vs 4), so a reader re-deriving Ford's 0.61 bound should use the normalized form.
- **Separately,** Ford's Remark 1 says the gap sum is "−0.2938…", but −1 + γ/(1−ρ) computes to −0.29284. This is a Ford typo and the paper does not use it.

### 8. Is "ℓ(d)/d unbounded" known?
- **Severity:** information. The paper's "remains unresolved here" is accurate.
- **This is exactly Erdős problem #51.** FC 51.lean at main: "@[category research open, question, AMS 11] theorem erdos_51 : ∃ A … A.Infinite ∧ (∀ a, IsLeast (φ⁻¹' {a}) (n a)) ∧ Tendsto (n a / a) atTop atTop".
  - Its remarks point to #694.
  - teorth DB: #51 `state: "open"`.
  - Web search snippets say the erdosproblems #51 page is discussed in Guy B36/B39. I could not load it live (403).
- **The paper does not cite #51 by number.** It cites [5, §I.9], which is the same question. Its equivalence statement in Theorem 2.2 and Remark 7.4 is correct by definition.
- **Erdős 1958 [3]** does not pose the question (checked by grep plus reading Theorem 4).
- **Ford p. 39** knows only small-k divisibility seeds, and "It appears that there might not be any totient, all of whose pre-images are divisible by 6, but I cannot prove this."
- **Other problems the brief asked about are different questions:**
  - #417 is lim V(x)/V′(x) (FC 417.lean).
  - #418 is the non-cototients question (FC 418.lean).
  - #821 is #φ^{-1}(n) > n^{1−ε} infinitely often. The paper cites its companion OpenAI preprint [11, Theorem 1.1] for this as an established fact. That claim is unrefereed and not an input to the proof; FC PRs #7314/#7316 to mark #821 solved are open.
  - #694 (max/min preimage ratio, solved, Lean) is different again.
- **Numerical probe for k ≥ 2** (scripts/ellratio.py, totients ≤ 2·10^7; output in W_work/ellratio_result.txt):
  - The run counts 3,183,543 totients ≤ 2·10^7. That equals my V(2·10^7) and Zeraoulia's, which is the positive control.
  - **k = 2:** 19 totients have ℓ(v) > 2v.
    - The smallest is v = 5888, with ℓ = 11985 (odd), giving ratio 2.0355.
    - So the k = 2 seed is far smaller than Ford's 2^18·257.
    - Cross-checked with the separate inverse-φ routine (9 preimages, min 11985).
  - **k = 3:** no totient ≤ 2·10^7 has ℓ(v) > 3v.
    - The maximum of ℓ(v)/v is 2.0414, at v = 2,037,248 (ℓ = 4,158,795, cross-checked).
  - So the k = 3 alternative of Theorem 2.2 is not settled by any small seed. This is consistent with the paper's "We do not determine which other integers k satisfy this seed condition", and with #51 being open.

## What I did NOT check
- I did not replay the conjectures.io Lean proof, and did not audit it beyond docstrings. Its prose exposition is unavailable (404, no archive).
- I did not replay or audit OpenAI's Lean. That belongs to the other seats.
- Guy, Unsolved Problems, B36/B39 (book not online).
- Pillai 1929 (relied on Ford's p. 2 account).
- Erdős–Hall 1973.
- Maier–Pomerance §§2–3 content. I checked only §1 and the constant.
- Bloom's 8 Oct 2026 blog post "Erdős problems in the OpenAI proofs" and the forum thread blog:10 (erdosproblems.com is 403 from here and via WebFetch).
- Zeraoulia's Zenodo record, and his values above 2·10^7.
- Companion preprint [11].
- arXiv coverage is partial: the API was rate-limited and some UI queries came back empty.
- I did not check the mathematical correctness of any step in the paper.
