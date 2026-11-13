# Erdős #704 submission (Stanikzai, χ(R^12) ≥ 39 via J(13,5,3)): world / literature referee seat

Seat: hostile literature referee. Date of checks: 13 Nov 2026.
Scope: every claim the submission makes about the state of the world, plus anything that would make its framing wrong.
The math (is α(J(13,5,3)) really 33, do the VeriPB logs check) is NOT this seat's job and was not checked here.
Raw downloads: `/tmp/ws704/` (arXiv PDFs + pdftotext in `pdf/`, web pages in `web/`, erdosproblems pages in `ep/`, Davies's arXiv source in `eprint/x/`).

Labels: CONFIRMED = primary source quoted. WRONG = primary source contradicts. UNVERIFIABLE = could not be settled from reachable sources (an absence claim, or a source behind a wall).

---

## 1. Davies, "Measurable obstructions for unmeasurable colourings", arXiv:2610.12301

**1a. Exists; version; date.** CONFIRMED.
arXiv abs page (https://arxiv.org/abs/2610.12301): "Submission history From: James Davies [v1] Thu, 8 Oct 2026 16:50:24 UTC (78 KB)". Comments field: "47 pages, 1 table". No journal-ref. Only v1 exists as of 13 Nov 2026. Affiliation on the PDF: Leipzig University.

**1b. What it proves.** CONFIRMED that the submission describes it correctly.
Theorem 1.1 (PDF p. 3): "Let D = {d1, ..., dt} ⊂ (0,∞) be finite and nonempty with d1², ..., dt² ∈ Q. Then αD(R⁴) = mD(R⁴) and χD(R⁴) = χD^(m)(R⁴), furthermore, for d ⩾ 5, αD(Q^d) = αD(R^d) = mD(R^d) and χD(Q^d) = χD(R^d) = χD^(m)(R^d)."
With D = {1} this is "χ(R^n) equals the measurable chromatic number for n ≥ 4", as the submission says.

Table 1 (PDF p. 4), the d = 12 row, verbatim:
"12 | 0.02680653 [29] | 0.00611112 [4] | 37 [12] | 164 [4] | 3.9758787 × 10−4 | 2,516"
(columns: previous α(R^d) upper, previous m1 upper, previous χ(R^d) lower, previous χ^(m) lower, new α = m1 upper, new χ = χ^(m) lower; [4] = Bachoc–Passuello–Thiery, [12] = Cherkashin–Kulikov–Raigorodskii, [29] = Exoo–Ismailescu).
Rows 13 and 14: new χ lower bounds "5,616" and "12,688". So the submission's "χ(R^12) ≥ 164 via Bachoc et al." and "2516, 5616 and 12 688 for n = 12, 13, 14" are CONFIRMED.
Theorem 9.1: "For 5 ⩽ d ⩽ 24, the upper bounds for m1(R^d) and the lower bounds for χ^(m)(R^d) are those in the new columns of Table 1. The same bounds hold for α(R^d) and χ(R^d), respectively."
BPT's own Table 3 (arXiv:1401.6140v2, p. 18) row: "12 | 129 [20] | 164" — the 164 is BPT's, refereed (DCG 53 (2015) 783–808, Crossref-confirmed).

Asymptotics (relevant to #704's actual question): Theorem 1.4 "m1(R^d) ⩽ (2 + o(1))^−d and therefore χ(R^d) ⩾ (2 + o(1))^d"; Theorem 1.5 "χ(R^d) ⩽ (3√3/2 + o(1))^d". Davies: "We boldly conjecture that one of these two bases is tight and cowardly do not specify which one."
**WARNING — typo in Davies's abstract** (both the arXiv abstract and PDF p. 1): it prints the upper bound as "(3√3/4 + o(1))^d" ≈ 1.299^d, which is below the lower bound 2^d. The body (Theorem 1.5, p. 4) says 3√3/2 ≈ 2.598, and Bikeev–Voronov–Raigorodskii (arXiv:2610.32408v2) quote it as 3√3/2. Never quote the abstract's constant.

**1c. Refereed?** No evidence of refereeing. UNVERIFIABLE whether submitted to a journal. Treat as an unrefereed 5-week-old preprint.
Davies's own "Statement of AI use" (p. 37): "Since early September we started using ChatGPT more and were able to use ChatGPT 5.6 Sol to complete the proof of Theorem 1.1. Its contribution here was the initial proof of the full converse of Theorem 2.1, and the initial statements and proofs of Theorems 2.2 and 3.5. ... More recently we then used ChatGPT 6.1 Sol to improve the χ(R^d) lower bound applications in Sections 8 and 9." And: "Due to the very recent release of [53] by OpenAI, we have posted this paper slightly earlier than we would have liked. We apologize for this."

**1d. Public reaction (last ~30 days).** No critique found anywhere. Reception so far is citation-as-proven by experts in the area:
- Polymath16 thread 18 (https://dustingmixon.wordpress.com/2026/01/17/polymath16-eighteenth-thread-back-with-a-new-conjecture/), Vsevolod Voronov, 9 Oct 2026: "Since James Davies improved all bounds on chromatic numbers starting from R^4 https://arxiv.org/abs/2610.12301 and a few days ago another paper appeared ... the only open question remains \chi(R^3) \geq 7." Carson Crocker, 10 Oct: "Davies's paper from 8 Oct does R^4 and up but not R^3."
- Koshelev–Kupavskii–Voronov, arXiv:2610.18907v1 (11 Oct 2026): "Davies [6, Theorem 1.1] proves that ordinary and measurable chromatic numbers agree in every dimension at least four." Their AI statement says they independently "were able to produce the (2 + o(1))^n lower bound" before Davies posted.
- Bikeev–Voronov–Raigorodskii, arXiv:2610.32408v2 (23 Oct 2026): "A recent paper by Davies [3] gives (2 + o(1))^n ⩽ χ(R^n) ⩽ (3√3/2 + o(1))^n."
- Henry Bass, GitHub `outsidetext/euclidean-chromatic-transfer` (Oct 2026, unrefereed, Claude-assisted): claims an independent transfer "χ(ℝⁿ) = χ_m(ℝⁿ) for every n ≥ 2" (Lean, conditional on OpenAI's planar rigidity theorem; literature density bounds enter as hypotheses), and credits "J. Davies (arXiv:2610.12301) proved χ = χ_m and α₁ = m₁ in dimensions n ≥ 4 by a different method". Its own caveat: "Nothing here has been refereed."
- Not found: any Tao blog post (search of terrytao.wordpress.com for "chromatic number": newest relevant post is Polymath16 2018), any Kalai post (his 7 Oct 2026 "Sharing AI progress" post predates Davies and does not mention him), any MathOverflow question (StackExchange API, 2025–), any Quanta article, any erdosproblems.com forum comment (see §4).

**1e. Our own spot-check of Davies's d = 12 density certificate** (this goes slightly beyond the brief; it bears on the "2516" number we might quote).
Davies's arXiv source ships `verify_section9_derivatives.py` + `section9_derivative_certificates.json` (stdlib-only). Run here with `python3 -I ... 12`: exit 0, `"chi_lower": 2516`, `"density_upper_exact": "198873/500198873"`, `"min_margin": 1.8456738970097378e-09`.
Positive control (instrument can go red): lowering B from 0.000397746 to 0.000397000 or 0.0003 → `ArithmeticError: (12, 'failed', ...)`, exit 1.
Decorrelated re-evaluation (mpmath, our code `/tmp/ws704/h12.py`, h0 matched Ω_12 to 40 digits): min of H(s)+B over a 0.01-step grid on (0, 200] is +4.78e-9 (equioscillating minima at s ≈ 9.94, 13.59, 30.03). So H ≥ −B holds for d = 12 by two independent evaluations.
This corroborates only the measurable bound m1(R^12) ≤ 3.976e-4 GIVEN Davies's Theorem 8.1 (radial-derivative trick: compact approximation leaves a distance gap around 1, so the smoothed autocorrelation vanishes on an annulus and all its radial derivatives vanish at r = 1). The ordinary bound additionally needs Theorem 1.1. Neither theorem was audited here. The 164 needs only Theorem 1.1 + refereed BPT.

**Consequence.** If Davies stands, the best known lower bound for χ(R^12) is 2516 (164 from Theorem 1.1 + BPT alone), and 39 is the best bound from an EXHIBITED finite graph, nowhere near the best bound overall. The submission says exactly this ("If these bounds stand, the contribution of Theorem 1.1 is the exact value of α(J(13,5,3)) and an explicit 1287-vertex unit-distance graph of chromatic number at least 39"). Framing: CONFIRMED honest.
"none has been exhibited": UNVERIFIABLE as an absence claim, but supported: Davies's paper never claims to exhibit a finite graph (grep for "explicit/exhibit/constructive" finds only "explicit bounds"/"explicit derivative family"), and nothing else we found exhibits one.

---

## 2. Explicit-graph record for χ(R^12) before this paper

**2a. Kahle–Taha, arXiv:1409.1278 → χ(R^12) ≥ 32.** CONFIRMED.
PDF p. 1, Theorem 1.1: "χ(R^8) ≥ 19, χ(R^9) ≥ 21, χ(R^10) ≥ 26, χ(R^11) ≥ 32, and χ(R^12) ≥ 32." p. 3: "the half-cube H(11, 4) has independence number ... 32. There are 1024 vertices ... χ(R^11) ≥ 1024/32 = 32. This last example also gives a new record lower bound χ(R^12) ≥ 32."
Nuance: their 32 for R^12 comes from an 11-dimensional graph by monotonicity. arXiv v1 only (3 Sep 2014); journal version Geombinatorics 24(3) (2015) 109–116 is corroborated only secondarily (Parts's bibliography in arXiv:2603.14581 gives the same reference).

**2b. Exoo–Ismailescu, arXiv:1408.2002 → α(J(13,6,4)) = 46, stated as χ(R^12) ≥ 36.** CONFIRMED (see §5 for the quotes). arXiv v1 only (9 Aug 2014), never revised, no journal-ref.

**2c. Cherkashin–Kulikov–Raigorodskii, arXiv:1512.03472 (DAM 243 (2018) 125–131) → 37 from a closed form.** CONFIRMED.
PDF p. 2, Theorem 1: "α(Gn) = max{6n − 28, 4n − 4c(n)}" (Gn = {−1,0,1}^n vectors of norm √3, edges at scalar product 1, i.e. distance 2). p. 2: "for small values of n, the theorem gives the best known bounds, namely: χ(R^9) ⩾ χ(Q^9) ⩾ 21, χ(R^10) ⩾ χ(Q^10) ⩾ 30, χ(R^11) ⩾ χ(Q^11) ⩾ 35, χ(R^12) ⩾ χ(Q^12) ⩾ 37." Arithmetic: |V12| = 8·C(12,3) = 1760, α = max{44, 48} = 48, ⌈1760/48⌉ = 37. Crossref confirms DAM 243, pp. 125–131, 2018, doi 10.1016/j.dam.2018.02.005. arXiv v2 dated 30 Aug 2016.
Also (p. 1): "Recently further improvements were announced: χ(R^8) ⩾ 19 [10], χ(R^10) ⩾ 26 [7], [10], χ(R^11) ⩾ 32 [10], χ(R^12) ⩾ 36 [7]." with [7] = Exoo–Ismailescu arXiv 1408.2002v1. So the submission's "The introduction of [7] lists χ(R^12) ≥ 36 as an announced improvement" is CONFIRMED.
Dimensions 13, 14 (submission: "the theorems of [7] give 46 and 52"): CONFIRMED by our arithmetic (2288/50 → 46; 2912/56 = 52) and by Davies Table 1 ("13 ... 46 [12]", "14 ... 52 [12]").

**2d. Any later explicit graph with χ(R^12) ≥ 38?** NONE FOUND. Strong negative evidence from three independent expert snapshots:
- Jaan Parts, Polymath16 thread 18, 25 Jan 2026: "From my notes, the published record lower bounds for the chromatic number in spaces of dimensions from 4 to 12 are as follows: 9, 9, 12, 16, 19, 22, 30, 35, 37. Can anyone confirm or correct these values?" (n = 12 → 37.)
- Vsevolod Voronov, same thread, 26 Jan 2026: "I think the other estimates remained unchanged. Certainly, no one in the MIPT community did this, nor did anyone who referred to earlier articles."
- Davies, Table 1, Oct 2026: previous χ(R^12) lower bound "37 [12]".
Parts's 2026 explicit-graph improvements are for d = 6, 7, 8, 9, 10 only (χ(R^6) ≥ 14, χ(R^7) ≥ 18, χ(R^8) ≥ 25 [arXiv:2603.14581], χ(R^9) ≥ 30, χ(R^10) ≥ 33 [thread comments 20 May–6 Jul 2026]). No d = 12 work.
arXiv API searches run (2016–2026): title "chromatic" with Euclidean/small dimension/unit distance; abstract "chromatic number" AND Euclidean; "generalized Johnson graph"; "Johnson graph" AND "independence number"; "unit distance graph"; "measurable chromatic"; "Hadwiger-Nelson"; "forbidden intersection"; authors Raigorodskii, Cherkashin, Bobu, Voronov, Prosanov, Exoo, Kahle, Parts. The only R^12-relevant hits were the papers above plus Davies. Raigorodskii–Sinelnikov-Murylev's 2025 survey (Russ. Math. Surveys 80:3, mathnet PDF) declines to tabulate specific small parameters ("нет никакой возможности (а кажется, и большого смысла) сделать сколько-нибудь исчерпывающий обзор").

**2e. A detail the submission does not mention but should be on our page.** The E–I value 46 had **not** been independently reproduced before this submission, and two experts tried in 2026:
- Parts, arXiv:2603.14581 (15 Mar 2026), footnote 2: "By the way, we haven't got a solution for the 1716-vertex graph mentioned in [4] when estimating the lower bound of χ(R^12), although the mcqd solver was running for over a month."
- Parts, Polymath16, 1 Apr 2026: after orbit-splitting, "taking an average of 4 hours per subgraph yields an estimate of five years for the original 1716-vertex graph"; Voronov, 3 Apr 2026: "Yes, I got about the same results. Apparently, without other ideas, it will not be possible to find the exact value if we use mcqd."
- Davies's Table 1 α column for d = 12, "0.02680653 [29]", equals 46/1716 = 0.0268065…, i.e. Davies takes E–I's 46 at face value, yet his χ column still says 37, not ⌈1/0.02680653⌉ = 38.
So: "earlier bounds from explicit finite graphs give at most 38" is CONFIRMED as written (stated record 37; 38 is implied by E–I's reported but, until now, unreproduced value). The submission's own reproduction of 46 is uncertified (its own words), so 46 should still be described as reported-and-reproduced-uncertified, not certified.

---

## 3. Has α(J(13,5,3)) been published before?

NO PRIOR VALUE FOUND. UNVERIFIABLE as a universal absence.

- **Bachoc–Passuello–Thiery (arXiv:1401.6140v2), Table 1** "Bounds for the independence number of J(n, w, i)": rows include "(12, 5, 2) 57 66 72 57", "(13, 5, 2) — 78 109 72", "(13, 6, 2) — — 191 148"; no row for (13,5,3) or (13,6,4); last exact α entry is (12,5,2) = 57. CONFIRMED. Notation check (no trap): Definition 3.3 "edges connecting pairs of n-tuples having exactly i coordinates in common equal to 1", so their i is the intersection size, same as the submission's t.
- **Brouwer's constant-weight tables** tabulate A(n,d,w) (all distances below d forbidden), a different quantity; not fetched live, by definition only. Note A(13,6,5) ≤ α(J(13,5,3)), since a distance-≥6 code avoids distance 4.
- **Raigorodskii–Sinelnikov-Murylev 2025 survey**: no table of small values (quote in 2d). The submission's "Frankl–Wilson-type inequality stated in the survey gives α(J(13,5,3)) ≤ 93" is CONFIRMED by recomputing the survey's Theorem 6 (r = 5, s = 3, r − s = 2 prime, d = 2s − r + 1 = 2): with (d1, d2) = (0, 2) we get t = 0, n2 = 11, bound C(13,2)/C(5,2) · (1 + 11) = 7.8 · 12 = 93.6, so 93. The splits (1,1) and (2,0) admit no t.
- **Balogh–Chen–Li (arXiv:2604.05607v1, 7 Apr 2026)**: asymptotic only, whole cube; they name the constant-weight quantity: "m(n, k, ℓ) := m2(n, k, ℓ), which denotes the maximum size of a k-uniform family with no two sets intersecting in exactly ℓ elements", and their Lemma 2.5 ties layers to the cube. The submission's description is CONFIRMED; no n = 13 value.
- **Jiang–Yang, "Binary Codes with a Forbidden Distance" (arXiv:2611.04523v1, 3 Nov 2026)**, posted after the submission's October search: whole binary cube, "for all t ≥ 3 and n ≥ (t + 1)²"; no constant-weight value at n = 13.
- **OEIS** (JSON search via Hetzner): no sequence for generalized-Johnson independence numbers, "intersect in exactly", or Euclidean chromatic lower bounds.
- **Classical name the submission does not use:** α(J(13,5,3)) = m(13,5,3) (also written N(n,k,ℓ)), the Erdős/Frankl–Füredi "forbidding just one intersection" number. Here k = 5, ℓ = 3 lies outside the solved regime k ≥ 2ℓ + 2. A web search for small exact values found none.
- **Passuello's 2013 thesis** (source of BPT's tables): UNVERIFIABLE (HAL is behind a bot wall from both exe.dev and Hetzner).
- **Polymath16 2026 discussion** covered only J(13,6,4) (Voronov, 28 Mar 2026: "the original graph is the Johnson graph G(13,6,4). Sadly, the general theory doesn't provide the exact value of the independence number in this case."). Nobody there mentions J(13,5,3).

---

## 4. The submission elsewhere; what Hexagon is

- **Hexagon record** https://hexagonmath.org/2611.00358: CONFIRMED live. Title "The independence number of the generalized Johnson graph J(13,5,3)", "Contributed by Mustafa Stanikzai", "Version 2 / Nov 12, 2026 / CC BY 4.0"; v1 shown as "Superseded Nov 12, 2026". Badges: "A mix of human-written and AI-generated text", "Human understanding: all parts". The v2 change note says only cross-reference names changed ("Statements, proofs, results and bibliography are unchanged"). Our local copy (`paper.txt`) is dated "November 11, 2026", so presumably v1. Provenance statement: "I used Claude Code (Anthropic) with the Claude Fable 5, Fable 5.1, Fable 5.2 and Opus 5.5 models to plan, draft, revise and review the paper and to write its code ... I used OpenAI Codex with the GPT-5.6 Sol model to evaluate plans". Its own limits line: "VeriPB, the encoding checker and the programs that check the decomposition are not formally verified."
- **What Hexagon is** (https://hexagonmath.org/about, /who): "a repository for research works in the mathematical sciences and theoretical computer science, administered by the Hexagon Mathematics Foundation ... created in response to the staggering changes that artificial intelligence has induced in the mathematics research landscape." "Acceptance of a work represents a decision to disseminate and preserve the work, and is not a judgment about its correctness, quality, or novelty." "Hexagon does not perform peer-review." In public beta; moderation is an automated screen plus a human check. Executive Director Benjamin Antieau, board president Mohammed Abouzaid, advisory board includes Kevin Buzzard, Akhil Mathew, Johannes Schmitt, Nikhil Srivastava, Ravi Vakil. In short, an arXiv-like, AI-era-friendly, non-refereed repository with a provenance page.
- **Zenodo 10.5281/zenodo.24145863**: CONFIRMED (API JSON fetched with Accept: application/json; the HTML page 403s from exe.dev). Created 2026-11-11T23:44Z, version 1.0.0, creator "Stanikzai, Mustafa", open access, `isSupplementTo` the Hexagon URL. 18 files, including tarballs of about 10.6 GB and 29.7 GB of proof logs. Stats at check time: 32 downloads, 13 unique views.
- **erdosproblems.com forum thread 704** (fetched through Hetzner): 5 comments (29 Sep 2025 – 22 Jul 2026), all about Raigorodskii's constant 1.2395667…; nothing on R^12, Davies or this submission. "The ability to post new comments has been suspended." Problem page "last edited 10 April 2026"; it still lists only Frankl–Wilson, Raigorodskii (1.239…)^n, Larman–Rogers (3+o(1))^n, the Larman–Rogers guess (2^{3/2}+o(1))^n and Prosanov. It does NOT mention Davies.
  Side note for our page (UNVERIFIED against LaRo72 itself): Davies's claimed upper base 3√3/2 ≈ 2.598 is below 2^{3/2} ≈ 2.828, so if Theorem 1.5 holds, the "truth may be (2^{3/2}+o(1))^n" guess quoted on erdosproblems is false.
  Threads 705, 706, 508: no mention of Davies, R^12 or the submission. The #508 page (edited 16 Oct 2026) now reads "The best bounds currently known are 6 ≤ χ ≤ 7", with a formalised proof that χ ≥ 6 (the OpenAI result).
- **teorth/erdosproblems**: `data/problems.yaml` has 704 at "open", last_update 2025-08-31. GitHub issue search for 704, Davies, J(13,5,3) and Stanikzai found nothing relevant (the Stanikzai hits are unrelated people).
- **Polymath16 thread 18** (newest comment 5 Nov 2026) and **MathOverflow**: no mention of the submission.
- **Web search** for "Stanikzai" + J(13,5,3): nothing beyond Hexagon and Zenodo.

---

## 5. The Exoo–Ismailescu arithmetic

CONFIRMED that E–I wrote 36 where their value gives 38.
arXiv:1408.2002v1, §5 "χ(R^12)" (PDF p. 5): "For this case, computing the independence number is a much harder computation. But again, both mcqd and our specialized program were able to determine that the independence number is 46. Hence the chromatic number is at least ⌈1716/46⌉ = 36". Then "Theorem 5.1. χ(R^n) ≥ 36, for n = 12, 13, 14." Their Table 1 lists "12 | 24 [11] | 36", "13 | 31 [19] | 36", "14 | 35 [19] | 36".
1716/46 = 37.30…, so the ceiling is 38 (46·37 = 1702 < 1716 ≤ 1748 = 46·38). Their 36 is a valid but weaker bound, a slip and not an invalid claim. The submission's quote of E–I ("both mcqd and our specialized program were able to determine that the independence number is 46") is verbatim-correct.

---

## Extra world context a #704 page should carry (not claims of the submission)

- The fixed-dimension bound does not touch #704's questions. Exponential growth was settled by Frankl–Wilson. Whether lim χ(R^n)^{1/n} exists is open. The bounds now claimed (preprint) are (2+o(1))^n ≤ χ(R^n) ≤ (3√3/2+o(1))^n (Davies, Theorems 1.4–1.5); Koshelev–Kupavskii–Voronov say they independently obtained the (2+o(1))^n lower bound.
- The flood of transfer results in Oct 2026 (Davies n ≥ 4; Koshelev–Kupavskii–Voronov n = 3, χ(R^3) ≥ 7; the Bass/Crocker transfer for all n conditional on OpenAI's planar theorem) all rest on preprints from the last 6 weeks, much of it AI-assisted, and none refereed.

---

## Sentences we CAN safely put on a public page

1. "Before this submission, the largest lower bound for χ(R^12) stated in print from an explicit finite unit-distance graph was 37 (Cherkashin, Kulikov and Raigorodskii, Discrete Applied Mathematics 2018), from a 1760-vertex graph whose independence number they determined exactly."
2. "Exoo and Ismailescu (arXiv 2014) reported α(J(13,6,4)) = 46 by computer and stated χ(R^12) ≥ 36; the value they report actually gives ⌈1716/46⌉ = 38."
3. "That value of 46 had not been independently reproduced in print. In 2026 Jaan Parts and Vsevolod Voronov reported that a standard clique solver had not finished after more than a month, and estimated years of computation."
4. "The submission gives an explicit 1287-vertex unit-distance graph in R^12, J(13,5,3), and proves its independence number is 33, so χ(R^12) ≥ 39. This is the largest lower bound from an exhibited finite graph that we know of." (Add "with certified proof logs" only if our math seats have checked the VeriPB logs.)
5. "We found no earlier published value of α(J(13,5,3)), the largest family of 5-subsets of a 13-set with no two sharing exactly 3 elements, in the tables of Bachoc–Passuello–Thiery, the 2025 Raigorodskii–Sinelnikov-Murylev survey, the OEIS, or recent work on forbidden distances."
6. "A preprint by James Davies (arXiv:2610.12301, October 2026, not yet refereed) proves that for n ≥ 4 the chromatic number of R^n equals its measurable chromatic number. Combined with Bachoc–Passuello–Thiery (2015) this gives χ(R^12) ≥ 164, and Davies's own density certificates give χ(R^12) ≥ 2516. If Davies's theorem stands, 39 is far below the best known lower bound; what 39 adds is a graph you can write down and check."
7. "By the de Bruijn–Erdős theorem, Davies's bounds imply that finite unit-distance graphs in R^12 with chromatic number at least 2516 exist, but none has been exhibited as far as we know."
8. "None of this addresses #704's headline question, whether lim χ(R^n)^{1/n} exists. That remains open; the best asymptotic bounds now claimed (in preprints) are (2+o(1))^n ≤ χ(R^n) ≤ (3√3/2+o(1))^n."
9. "The paper is posted on Hexagon, a moderated but not peer-reviewed mathematics repository, with an AI-use provenance statement; the data are on Zenodo."
10. "Exoo and Ismailescu's stated bound of 36 is correct as a bound; it is two weaker than their reported value supports."

## Sentences we must NOT write

- "New record lower bound for χ(R^12)" / "best known lower bound for χ(R^12)" without the qualifier "from an explicit finite graph". Davies (preprint) gives 164 and 2516.
- Anything implying 39 competes with or improves on Davies.
- "χ(R^12) ≥ 38 was known." It was implied by a reported value; nobody stated it in print. Say "implied by Exoo–Ismailescu's reported value".
- "The previous explicit-graph record was 38." The stated record was 37.
- "Exoo and Ismailescu made an error that invalidates their result." Their 36 is valid; it is a weaker-than-possible ceiling.
- "This paper certifies / independently verifies α(J(13,6,4)) = 46." Its 46 is explicitly uncertified (its own words). At most: "reproduces, uncertified".
- "Davies proved χ(R^12) ≥ 2516" without "in a preprint, not yet refereed".
- Davies's upper bound as "(3√3/4)^n" (typo in his abstract); use 3√3/2 from Theorem 1.5.
- "Hexagon accepted / reviewed / vetted the paper." Its own terms: acceptance "is not a judgment about its correctness, quality, or novelty"; "does not perform peer-review."
- "Nobody has ever computed α(J(13,5,3))" or "first ever": a universal absence we cannot verify. Say "we found no earlier published value".
- "This resolves / advances Erdős #704." A fixed-dimension bound does not touch any of the problem's three questions.
- "The first finite unit-distance graph in R^12 with chromatic number ≥ 39." De Bruijn–Erdős plus Davies imply such graphs exist; say "first exhibited".
- "Kahle and Taha found a 12-dimensional graph." Their χ(R^12) ≥ 32 comes from an 11-dimensional half-cube by monotonicity.
- "The erdosproblems.com page records the current state." It was last edited 10 Apr 2026, predates Davies, and its forum is closed to new comments.
