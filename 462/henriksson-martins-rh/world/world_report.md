I found an earlier RH-conditional solution of the composite reading, posted before either submission and cited by neither. One more fell between Henriksson and Martins on 20 Nov. Ryota Mori posted the first on Zenodo on 14 Nov 2026, a week before Henriksson; the second is a GitHub prize submission by "lixiang90" on 20 Nov. Henriksson and Martins do not cite each other either. Separately, an RH proof was announced on 20 Nov and is being checked; it changes what "RH-conditional" means here.

Work is in /tmp/e1122/seatW/. erdosproblems.com not read, by any route. I also avoided erdosproblems.ai in case it mirrors that site.

## 1. Zhang, arXiv:2608.24930

**Versions.**
- v1: 22 Aug 2026, 10:13 UTC.
- v2: 21 Oct 2026, 08:06 UTC.
- No v3: `/abs/2608.24930v3` and `/pdf/...v3` both return 404 as of 22 Nov, about 09:07 UTC.

**Neither version mentions the Riemann hypothesis.** The word does not appear in either text, so Zhang does not prove the composite reading under RH. His results are:
- the constant c = 8;
- the window mean 4C + O_C(1/log X);
- a second moment;
- one conditional uniform theorem.

**v1 abstract (iii):** "Under a weak Cramér-type hypothesis on primes in intervals of length (log y)^{2+o(1)}, the estimate μ_C(x)=4C+O_C(1/log x) holds uniformly in x."
- v1 also claimed a second moment of O_C((log X)^{-2}) and Corollary 1.5, "μ_C(x)=4C+o(1) for almost all x". Both are gone in v2, where the second moment is O_C(1).
- v1's Hypothesis 1.6 was: "For every fixed C0 > 0 and A ≥ 1 there is a constant C_A > 0 such that for all y ≥ 2 and all h with C0(log y)^2 ≤ h ≤ y, |π(y+h) − π(y) − h/log y| ≤ C_A h/(log y)^A."
- v2 Remark 1.6 itself says this form "is false" by Maier's theorem. That makes v1's Theorem 1.8 vacuous.

**v2, verbatim:**
- **Hypothesis 1.5 (Bounded fluctuations), Martins's "Hypothesis Z":** "For every fixed C0 > 0 there are constants 0 < c1 ≤ 1 ≤ c2 such that for all y ≥ 2 and all h with C0(log y)^2 ≤ h ≤ y, c1 h/log y ≤ π(y+h) − π(y) ≤ c2 h/log y."
- **Theorem 1.7 (Uniform boundedness under Hypothesis 1.5):** "Assume Hypothesis 1.5. Then for every fixed C > 0, there exists X0(C) > 0 such that for all x ≥ X0(C), μC(x) = 4C + OC(1), uniformly in x; in particular μC(x) is bounded between two positive constants depending on C. Consequently the question of Erdős and Graham has an affirmative answer (for the sums over composites; including primes only increases the sum)."
- **Conjecture 1.8:** "For every fixed C > 0, μC(x) = 4C + o(1) uniformly in x → ∞."
- **Proof scope:** the proof (§5) applies the hypothesis with "C0 := 4C (or any fixed C0 ≤ 4C)".

Hypothesis 1.5 is pointwise. For small C0 it forces prime gaps of size o((log p)^2), which is expected to be false; Martins §1.3 argues this from Granville's prediction and Banks–Ford–Tao.

Zhang also writes that the problem is "open, with no claimed proofs". He cites Zeraoulia (ResearchGate 400404179), Chojecki's agentic-erdos repository, and Matomäki 2017 (an almost-all result).

**Before 21 Nov, did anyone prove the composite reading under RH alone? Yes, twice. Neither is refereed.**

- **(C) Ryota Mori, "A remark on Erdős Problem #462: the Riemann Hypothesis suffices."**
  - Zenodo 10.5281/zenodo.24210937, created 2026-11-14 02:22:44 UTC (DataCite registration 02:22:46). Code is in 24210939.
  - Theorem 1: "Assume the Riemann Hypothesis. There are absolute constants C0 > 0 and c > 0 such that for every C ≥ C0 there is an x0(C) with μC(x) ≥ cC (x ≥ x0(C)). More precisely, for x ≥ x0(C) the interval (x, x + L) contains at least cCx^{1/2} integers n = pq with p, q primes in (½x^{1/2}, 2x^{1/2})."
  - The proof is about a page and a half: smoothed explicit formula in both variables, with the main term κ·L against an error of O(x^{1/2}(log x)^2).
  - It covers only C ≥ C0, and C0 is effective but not computed.
  - The note says it was written with extensive generative-AI help and was not formalized.
  - I read it once and saw no error.
- **(D) lixiang90 on GitHub, "jsp-375-selberg-semiprimes".**
  - Justin Sun Prize awards PR #5616 opened 2026-11-20 19:41 UTC. The repository was created 20:28 UTC, with commits at 20:28:53Z and 21:07:16Z.
  - Claim: under RH, with A = 1+640K, C = A and c = A/1920, for every large real x.
  - Method: disjoint grid bins near √x/2 and their reciprocals x/u, plus Selberg's mean square, and it explicitly says "The input from prime distribution is classical".
  - The README claims a Lean derivation from Mathlib's RiemannHypothesis via Steve Hubbard's LeanLab Selberg theorem. I did not build it.
  - It was developed with Codex and leans on Alpöge's announced RH proof (see "Where things stand").

## 2. Literature, last 90 days and classical

**Zeraoulia, "Toward Erdős–Graham Problem 462 (composite-only)…"**
- Records: ResearchGate 400404179, DOI 10.13140/rg.2.2.35272.99847/2 (DataCite created 2026-02-04; page says "On Feb 3, 2026"). OpenAlex also lists a /1 version.
- ResearchGate returned 403. I read the full text in the Wayback snapshot of 2026-08-28.
- It contains no RH result; "Riemann" appears only in a book blurb.
- Proposition 4 assumes a uniform pointwise lower bound for primes in every interval of length (log Y)^B with B > 2, and concludes only for windows of length C√x(log x)^B.
- Lemma 5 is vacuous as stated: with p, q ∈ [√x, 2√x] and pq ≤ x+H, only O((log x)^4) pairs exist. Henriksson's criticism of it is correct.

**gpt-erdos `data/solutions/462/candidate_solution.md`** (neelsomani/gpt-erdos, commit 7f633835, 2026-01-20)
- A status note, not a solution.
- It records that RH prime gaps settle the version that includes primes.
- On the composite version: "Proving a uniform lower bound for every large x, however, is not currently known."

**Other searches**
- **przchojecki/agentic-erdos `notes/ep462.md`** (accessed by its author 2026-05-08): numerics only. It quotes Tao's 28 Sep 2025 comment, which I am seeing only secondhand from GitHub.
- **Michael Ross, Zenodo (July/Sept 2026), "Exact Semiprimes in Short Intervals":** heuristic framework, no RH theorem.
- **Hexagon works API** (queries "least prime factor", "semiprimes", "products of two primes"): only Henriksson 2611.00808.
- **arXiv API** (all-fields searches): only Zhang plus unrelated items. 2611.05000 (Baluyot–Conrey–Irfan) is about variance asymptotics for Λ*k under RH plus a shifted-moments conjecture; it does not give every-interval lower bounds.
- **openai/math** (751 preprints released 6 Oct): nothing on semiprimes in short intervals or #462.
- **MathOverflow and Math.SE API:** nothing.
- **Tao's blog** (feed and search): no post on 462.
- **MathHelm search:** "Nothing here yet" for 462 and semiprimes.

**Classical prior art.** I found no pre-2026 paper stating "under RH, every interval of length C√x(log x)^2 contains ≫√x balanced semiprimes".
- The argument is the multiplicative counterpart of the RH result on Goldbach numbers in intervals of length C log² N. Chirre–Hagen's introduction credits that to Linnik (log^{3+ε}), then Kátai (1967) and Montgomery–Vaughan (1975) at log².
- Mori calls his proof "standard methods", and lixiang90 says the input is "classical".
- Almost-all results (Selberg 1943; Teräväinen 2016; Matomäki–Radziwiłł; Matomäki–Teräväinen 2022, (log x)^{2.1}) do not give every interval or balanced factors, so none implies the statement directly.
- My read: no old theorem implies it immediately, but it is about a page from Selberg's 1943 mean square. Novelty is modest, and priority for the headline belongs to Mori.

## 3. teorth and Formal Conjectures

**teorth `data/problems.yaml`** (fetched at commit 8e3d61bf, 2026-11-22 07:26Z). The #462 row:

```
status: open, last_update 2025-08-31
informal_status: open, 2025-08-31
formal_status: unformalized
formalized: yes, 2026-09-02
forum: posts: 2
oeis: A032742 possible
tags: number theory, primes
```

- The row is unchanged since 2026-05-01 except for forum counts.
- The `forum` field was introduced for all problems on 2026-11-06 (commit 0d7b6c8), already showing 2 posts. The second post is not read.
- No teorth issues or PRs concern 462; PR #462 there is about problem 379.

**Formal Conjectures**
- Issue #743 (opened 2025-10-05) was closed by PR #4074, "Add Erdős problem 462", merged 2026-09-02.
- The later commits are chores: tagging (6740), modulizing (4688), removing answer() (6762).
- No other issues or open PRs on 462.
- The formal statement is the literal reading: the sum over all n in Icc x ⌊x + C√x(log x)²⌋₊ of n.minFac/n, primes included.

## 4. Priority and dates (all UTC)

| Date / time | Event |
|---|---|
| 2026-08-22 | Zhang v1 |
| 2026-10-21 | Zhang v2 |
| 2026-11-14 02:22 | Mori, Zenodo 24210937 |
| 2026-11-20 19:41 | lixiang90, JSP PR #5616 (repository 20:28) |
| 2026-11-21 06:27:50 | Henriksson Zenodo v1, 24412768, "462 v1" (says "v1 AI-generated draft"; theorem: x ≥ 10^42, ≥ 4√x products, weight ≥ 4/3) |
| 2026-11-21 08:02 | Henriksson companion Lean record, 24414348 |
| 2026-11-21 08:30:20 | Henriksson Zenodo v2, 24414763, "Balanced semiprimes…" |
| 2026-11-21 09:43–09:44 | Henriksson TauCeti roadmap commits (fork created 09:41) |
| 2026-11-21 09:45:59 | TauCetiRoadmap PR #2865 opened |
| 2026-11-21 10:08:34 | Commit 37a574a1, "Correct the source of the semiprime interpretation" |
| 2026-11-21 10:32:34 | Hexagon 2611.00808v1 created |
| 2026-11-21 10:41 | Henriksson "Revised proof package", Zenodo 24416597 |
| 2026-11-21 11:53:43 | Commit 35753e0c by ad-he-nx, "Fix the Lean roadmap targets…"; AI reviewer approved at 12:37 |
| 2026-11-21 15:59:03 | Henriksson Zenodo v3, 24422158 (concept 24412767; 3 versions) |
| 2026-11-21 17:50:35 | Hexagon 2611.00808v1 published |
| 2026-11-22 03:13:14 | Martins, Zenodo 24431352 (concept 24431351; 1 version) |

**Henriksson record details**
- The commit you named, 35753e0c, is in ad-he-nx/TauCetiRoadmap; Hexagon links its parent 37a574a1 instead. That commit dropped the false claim that Erdős–Graham "then ask" for ≫√x balanced products; v2 had it, v3 does not.
- Hexagon's 2611.00808v1 is an intermediate version: v2's title and abstract, 6 pages, and it says Theorem 1.2 "has not been formalized in Lean". v3 claims Lean for Theorem 1.2 as well.
- Hexagon labels it "Primarily AI-generated", "Human understanding: no parts", tool ChatGPT 6.2 Astra.

**Cross-citation.** Neither submission cites the other, and neither cites Mori or lixiang90.
- Martins cites only Zhang and writes: "As far as we are aware, no solution of Problem 1.2 conditional on the Riemann Hypothesis … has appeared in the literature." That is false as of his posting (Mori, lixiang90 and Henriksson preceded him).
- Henriksson cites our 26 July working report as [7].
- Martins's record also contains `LeastPrimeFactorRH.lean` (54 KB), which his paper never mentions.

**What each one adds beyond Mori's 14 Nov headline**
- **Henriksson:**
  - the only explicit theorem: C = 384, x ≥ 9.6·10^37, ≥ (14/3)√x products, weight ≥ 14/9, given Chirre–Hagen;
  - a lower bound for every C > 0 (≍ C² for small C);
  - an unconditional upper bound μ_C ≤ K(1+C), which I did not find in any source checked;
  - a Lean check of the deduction, taking the Chirre–Hagen inequality as hypothesis.
- **Martins:**
  - S_C ≥ min{C/54, C²/K} for every C;
  - |S_C − 4C| ≤ K′√C under RH;
  - Zhang's Conjecture C under a pair-correlation-type variance hypothesis.
  - The last two appear in none of the others.

## 5. The cited analytic inputs

The subagent read these; I spot-checked each statement against its extracted text. All four match what the papers use.

- **Chirre & Hagen, Res. Number Theory (2026) 12:82**
  - DOI 10.1007/s40993-026-00767-6, published online 14 Aug 2026; also arXiv:2512.23534 v1, 29 Dec 2025, identical statements. Journal PDF fetched through the Mac Chrome because Springer blocked curl.
  - Definition: Jθ(x,δ) = ∫_1^x (θ((1+δ)y) − θ(y) − δy)² dy.
  - Theorem 3: "Assume RH. Then, for x ⩾ 10^13 and δ ∈ (0, 10^−13] we have that Jθ(x, δ) ⩽ 2.5571 · δ log²(2.0001/δ) x²."
  - Theorem 2: the same statement for Jψ with constant 2.2258.
  - MATCH.
- **Cully-Hugill & Dudek, Theorem 1** (arXiv:2206.00433 v2, 21 Aug 2023, marked accepted at J. Aust. Math. Soc.)
  - "Assuming RH, for all x ≥ 10^8 and any δ ∈ (0, 10^−8] we have ∫_1^x |θ(y + δy) − θ(y) − δy|² dy < 202δx² log² x."
  - MATCH with v2. arXiv v1 (25 May 2022) states a different theorem: x ≥ e^12 with constant 18.
  - The journal text is paywalled. Its abstract's constants match v2, as does Chirre–Hagen's restatement.
- **Grenié–Molteni–Perelli, Proposition 1** (arXiv:1602.02906 v2; unchanged from v1; journal paywalled)
  - "Assume DRH for the number field K. Then there exist absolute constants c, X0 > 0 such that for X ≥ X0 and 2 ≤ h ≤ X we have ∫_X^{2X} |ΔK(x,h)|² dx ≤ cX(h + L²)(nK L + log dK)²."
  - With K = Q this is the form both papers use. MATCH.
  - The Saffari–Vaughan (6.20) misprint is noted in the paper.
- **Carneiro–Milinovich–Soundararajan, Theorem 5** (arXiv:1708.04122 v2; same in v1)
  - "Assume the Riemann hypothesis. Then, for x ≥ 4, there is always a prime number in the interval [x, x + (22/25)√x log x]."
  - It holds for all x ≥ 4, not just large x. MATCH.

## The original text and the two readings

I read Erdős–Graham 1980, printed p. 92, from Graham's UCSD scan. It says:

> "With p(n) denoting the least prime factor of n, it is easy to see that Σ_{n<x, n≠prime} p(n)/n = (c+o(1)) x^{1/2}/(log x)². Is it true that Σ p(n)/n > c′, where n ranges over all integers in [x, x+cx^{1/2}(log x)²]?"

- The next sentence is an unrelated question about composites m with m − p(m) < n.
- So the literal reading includes primes, and the FC statement matches it. Under RH, Carneiro–Milinovich–Soundararajan Theorem 5 settles that reading for every C.
- The interval coefficient is printed as the same lowercase c as the asymptotic constant, which Zhang shows is 8. If that is meant literally, only results valid for every C (Henriksson's Theorem 1.2, Martins's Theorem 1.3) cover it. Mori (C ≥ C0), lixiang90 (C = 1+640K) and Henriksson's Theorem 1.1 (C = 384) would not.

## Where things stand (needs care)

On 20 Nov 2026 Levent Alpöge announced a Lean-only proof of RH and of GRH for Dirichlet L-functions, found with Claude.
- Announcement: alpo.ge/remark.pdf (PDF created 2026-11-20 12:52 UTC). Mirror: CocoSgt/riemann-hypothesis-lean, created 14:59 UTC.
- Tao's blog (20 Nov) points to the Lean Zulip thread where verification is under way. His 21 Nov link post lists an "AHM Statement on the Announced Proof of the Riemann Hypothesis".
- One independent kernel check is reported: user sbp, with the con-ron checker, gist dated 21 Nov, "successfully completed".
- An open GitHub issue questions some trivial-looking predicates.
- Hexagon has three items on it (2611.00799, .00809, .00812), which I did not read.

If the proof stands, all four RH-conditional results become unconditional, and #462 is settled in both readings. Henriksson's explicit theorem would then hold unconditionally for x ≥ 9.6·10^37. lixiang90's PR already depends on this. For now it is an announced claim under verification, not an accepted theorem.

## Where I looked and could not see

- **erdosproblems.com: not read.** That covers the problem page, the forum thread (Tao's comment seen only secondhand), the second forum post, and the proof-claims tab.
- **erdosproblems.ai:** not fetched, because it may mirror erdosproblems.com.
- **ResearchGate:** 403 directly. I read Zeraoulia only in the 2026-08-28 Wayback snapshot; DataCite returns 404 for the /1 version (OpenAlex still lists it).
- **Journal full texts** of Cully-Hugill–Dudek, Grenié–Molteni–Perelli and Carneiro–Milinovich–Soundararajan: paywalled, so I used the arXiv versions.
- **Semantic Scholar:** 429 (rate-limited). Google Scholar: not used.
- **arXiv:** no full-text search exists; I used API all-fields searches and web search.
- **Lean Zulip and the AHM statement text:** not read.
- **Lean builds:** I did not build lixiang90's, Martins's or Henriksson's Lean.

Applying the "no X found in <sources>" rule:
- No other RH-conditional or unconditional claimed solution of #462 found in Zenodo, DataCite, OpenAlex, the arXiv API, the Hexagon API, GitHub (code, repos, FC/teorth issues and PRs, JSP awards), MathOverflow, Math.SE, Tao's blog or MathHelm, as of 2026-11-22 about 09:30 UTC, beyond Mori, lixiang90, Henriksson and Martins.
- No pre-2026 statement of the RH balanced-semiprime result found in the same sources plus two web searches.