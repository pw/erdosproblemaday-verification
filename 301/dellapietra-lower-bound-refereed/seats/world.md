I found no referee report, replay or criticism of Della Pietra's lower bound by anyone else. His repository has no issues, pull requests, forks or stars, and his last commit is still `789c6f0` from 30 Jul. The claim does have one downstream user: Dmitry Khanukov builds a Problem 302 result on it, and Khanukov's CI re-runs Della Pietra's Lean proof terms through Lean's kernel. That checks the Lean; it is not a mathematical review. No other claim of f(N) ≥ (1/2+ε)N, and no proof of the conjecture, turned up anywhere. The trackers that have picked up his lower bound list it as an unverified claim; the others still list 301 as open.

**Wall:** I fetched nothing from erdosproblems.com. I also skipped two copies of its content: `erichou1/erdos-open-problems/forum_threads/301.html` and the unsolvedmath.com mirror. Anything below about that site's forum or proof-claims tab comes from the third-party plasma-ai wiki's paraphrase or from teorth's post counts. I did not read it myself.

## 1. Refereeing, replays, citations and building on the lower bound

**Built on it: Khanukov, Problem 302** (github.com/khanukov/erdos302, created 2026-08-14)
- His lower bound f₃₀₂(N) ≥ (5/8+δ)N takes Della Pietra's 301 witness and adds a padding lemma. The 301 Lean is pinned at `789c6f0`, the 327 Lean at `a720144`, and Tao's Mathlib fork at `da1f94df`. The bookkeeping is in `docs/LOWER_BOUND_PROVENANCE.md`, which assumes the witness satisfies |C_N| ≥ (1/2+ρ_L/24)N.
- Zenodo versions: v0.1.0 on 2026-08-16 (10.5281/zenodo.21966591), v0.1.1 on 08-18 (21989077), v0.2.0 on 09-13 (22737316).
- A version from 2026-09-21 makes the constant explicit, δ = 1/(86400·commonL), where commonL is astronomically large.
- v0.3.0 (2026-11-23, 10.5281/zenodo.24457000) contains only an upper bound for 302.
- **Closest thing to a replay:** CI run 45080234162 on 2026-11-22, job `lower-lean`, passed `leanchecker --fresh`. This kernel-checks Della Pietra's proof terms, including `roughThirdSet_admissible` and `roughThirdSet_card_lower_bound`. It does so on a pre-release Lean (v4.33.0-rc1) with Tao's unmerged Mertens fork, and it trusts the compiled Lean library files as given. Khanukov calls the result unrefereed.

**Cited it**
- Hexagon 2611.00752 (Howe, Huffman, Kohlmeyer, Kruer; 2026-11-20). This is a Problem 302 paper ("f₃₀₂ = CN + o(N)", entered for Justin Sun Prize as JSP-000254). It cites the Della Pietra 301 manuscript only as the source of the prime-factor-regularity idea. The authors declare that no human has checked the paper.
- Orakwue, Zenodo 10.5281/zenodo.24413618 (2026-11-21). An upper bound of 2233/2808 ≈ 0.795228; it also reproduces Della Pietra's 15437/19344 and claims A390394(73)=54 and A390394(74)=55. It cites the repo for upper bounds only, says nothing about the lower bound, and calls 301 OPEN.

**Trackers that have the lower bound**
- plasma-ai/erdos wiki, `E0301` (claim page created 2026-10-07, edited to 10-17). Records it as a pending, AI-assisted claim (the claim names "GPT 5.6 Sol") with no acceptance. Secondhand, it reports:
  - the claim was filed on erdosproblems.com as proof-claim #169 on 2026-07-30;
  - two comments sit under it: one says a GPT review found no fatal issue but wants Prop 4.1 expanded; the other credits Sawin's 327 framework.
- techno-optimist/erdos-frontier-atlas strike board (2026-09-27): "uncertain… reported, unverified".

**Trackers that list 301 as open without the claim**
- Formal Conjectures issue #477 is still open. PR #7918 (tombudd, opened 2026-11-12, approved by bocowgill 2026-11-15, not merged) marks both parts open. It records only the 1/2 lower and 25/28 upper bounds.
- teorth/erdosproblems `data/problems.yaml`: 301 is open, `last_update 2025-08-31`. A forum block added 2026-11-04 shows posts 6, proof_claims 2. That count is unchanged at HEAD `8e3d61b` (2026-11-22).
- grandchallenge/MATH-PROGRAMME `editorial/0301.md` (2026-10-13/14): open, no mention of Della Pietra.
- Justin Sun Prize: JSP-000253 is Problem 301, "Current status: Open". Three partial Lean PRs were closed (#530, #3508, #4584). There is no Della Pietra submission.
- plby/lean-proofs (2026-08-28): 301 open.

**Sister-proof audits (Problem 327)**
- The 301 Lean imports about ten modules from his 327 repo (e.g. `ThreeFormBoxBounds`, `MixedFinalSummation`, `Regularity`, `RoughCount`).
- The paper says no 327 theorem is used. The README says no theorem *about Problem 327* is a mathematical input. Both are true, but the Lean's trust base includes the 327 repo.
- On that repo, hhe48203-ctrl opened two PRs. PR #1 (2026-08-09, still open, no reply) fixes a wrongly stated identity in the 327 manuscript; the Lean is unaffected. PR #2 (closed unmerged 2026-08-10) made ε explicit for 327 and "found no mathematical or paper-statement error".

## 2. Della Pietra himself
- Four public repos:
  - `erdos-883-proof` (07-27, releases v1 and v2);
  - `erdos-327-proof` (07-29, release `proof-claim-v1`, last commit 07-30);
  - `erdos-301-proof` (07-30; no release or tag, CI green on all four commits);
  - `meter-beater` (Aug–Sep, unrelated).
- No commit, correction or reply since 30 Jul. His recent public activity (2026-11-16) is in `deepdotspace/deepspace`, which is unrelated.
- No arXiv, Hexagon or Zenodo paper by him.
- The lower-bound claim appears only in his repo, the erdosproblems.com claims tab (secondhand), and the downstream items above.

## 3. de la Bretèche–Tenenbaum ("BretecheTenenbaum2026")
- The citation is correct: "Mean values of arithmetic functions and application to sums of powers", Math. Proc. Camb. Phil. Soc. 180(1) (2026) 1–13. It was online 2025-08-08, DOI 10.1017/S0305004125101382 (checked on Crossref).
- arXiv:2403.19320 has versions from v1 (2024-03-28) to v6 (2025-08-04); v6 carries the journal reference.
- Theorem 3.1 is a multivariable mean-value upper bound for F(|Q₁(n)|,…,|Q_k(n)|) over boxes, for F in their function class M_k(A,B,ε).
- The numbering moved: in v1 this result is Theorem 1.2, and it becomes 3.1 by v3 (2025-01-28). Della Pietra cites the journal, so his "Theorem 3.1" matches.
- His paper says the Lean does not formalize Theorem 3.1 itself but proves substitute bounds that are enough for his use.

## 4. Mathlib Mertens
Not merged.
- PR #41394 (head `teorth:mertens-second-theorem`, opened 2026-07-06) is open and labelled `blocked-by-other-PR`.
- It was split into #44061 and #44062, both opened 2026-09-22 and still open.
- `Mathlib/NumberTheory/Mertens.lean` does not exist on master.
- The pinned commit `da1f94df` (2026-07-17) is no longer on Tao's branch, which was rewritten and now has head `4d8a5a87` (2026-10-01). It can still be fetched by SHA; Khanukov's CI had to switch to that on 2026-11-21 (commit `4871d6a`). This is a reproducibility risk for anyone rebuilding the 301 Lean.

## 5. Other claims of f(N) ≥ (1/2+ε)N or f = (1/2+o(1))N
- **Chen, Wang, Zhan, Tang (Shanghai DianJi University).** Zenodo supporting materials for "Residual Dilations and Isolated Semiprimes in Erdős Problem 301": v1.0.0 on 2026-07-25 (10.5281/zenodo.21559561) through v1.2.9 on 08-13 (21911627).
  - The manuscript itself is not public.
  - Their claim map lists a "lower-order improvement above N/2" from isolated semiprimes, proved in prose only. That means N/2 + o(N), not positive density.
  - It also lists upper bounds 17339219/20976956 ≈ 0.826584 and 64374043/77878944 ≈ 0.826591.
  - Their own scope note says 301 stays open. They do not mention Della Pietra.
- Nothing else for 301. The 302 lower bounds (Cambie 5/8, Khanukov 5/8+δ, JSP-000254 PR #5077 at 17/32) say nothing about 301, because a 301-free set is also 302-free, so f₃₀₁ ≤ f₃₀₂.
- **Other new upper bounds:**
  - Wang 667/806 (Zenodo 2026-05-26/27);
  - leon2k2k2k 0.8436 (June);
  - Della Pietra 15437/19344 ≈ 0.79803;
  - Orakwue 2233/2808 ≈ 0.795228;
  - rickyc 319/390 (forum, secondhand).

  A van Doorn–Tang paper below 0.8 was announced on the forum (secondhand) but is not on arXiv; I checked both authors' listings. Our 0.787738 is still the lowest I saw.

## 6. Standing of the literature
- **Erdős–Graham 1980, p. 37.** I have only plasma-ai's transcription, not the book. It shows the top half gives more than cn with c = 1/2, and asks whether c > 1/2 is possible. Della Pietra's claim would answer that question "yes".
- I found no published, refereed lower bound beyond N/2.
- The nearest published results are on neighbouring problems, not 301:
  - Bloom, arXiv:2112.03726: positive upper density forces a subset with reciprocal sum 1;
  - Liu–Sawhney, arXiv:2404.07113: Problem 300, threshold 1−1/e is sharp;
  - Sawin, arXiv:2607.15419 (2026-07-16): a 327-type question; it does not mention 301.
- Graham's survey "Paul Erdős and Egyptian Fractions" (2013, Bolyai Society Mathematical Studies 25, pp. 289–309) exists, but it is paywalled and I did not read it.

## Where I looked and found nothing more
- **arXiv API**, title/abstract only, not full text. Terms: "Erdos problem 301", "#301", "unit fraction(s)", "Egyptian fraction", "isolated semiprimes", "residual dilations", "unit-fraction-free", and author searches for Della Pietra, Khanukov, van Doorn and Quanyu Tang.
- **MathOverflow** search API (five queries) and the unit-fractions / egyptian-fractions tags.
- **terrytao.wordpress.com** site search for "erdos 301", "Della Pietra", "unit fraction free" and "mertens second theorem".
- **Hexagon** query API for unit fraction, reciprocal, Erdős, Della Pietra and "limiting density".
- **DataCite** queries for erdos 301, "Problem 301", unit-fraction-free, Della Pietra, Khanukov, Wang, Chen and Orakwue.
- **GitHub code and repo search** for Erdos301, erdos-301, erdos_301, erdos301Conclusion, roughThirdSet, donalddellapietra, erdos-301-proof, unit-fraction-free, reciprocal-sum-free and JSP-000253.
- **Specific repos:** openai/math `CONTENTS.md` (its item 301 is a C*-algebra result), carlostoledo1891/cert-machine, the nealmcb repos, the Nervous-Machine DEBRIEF series, TheJustinSunPrize/awards, uclanlp/continual-graph-memory, and vibemathing (an empty scaffold).
- **Web search:** three queries.
- **Blocked:** oeis.org and the Zenodo API returned 403 from both this box and Hetzner. I got the Zenodo files through WebFetch and extracted them in `/tmp/e301lit/`.