# Seat W: world, novelty and priority report for OpenAI's Heilbronn claim (family 191, Erdős #507)

Seat W, fetched 2026-10-22 between 15:10Z and 16:10Z. Scratch and downloaded copies are in `/tmp/oaimath/191/seats/W_work/`. I quote sources and do not paraphrase them. When a negative comes from a search, I say so: a search that finds nothing tells you about that search's coverage, not that the thing is absent.

**Dating, which matters for "prior".** The paper is dated 25 Sep 2026, but its first public appearance was OpenAI's repository `openai/math`. Commit `adc7f1241` ("Initial commit") is dated 2026-10-06 14:58:50 −0700. The bigospeedrun board says the same: "OpenAI baseline: ≈3.18·10^−236, released Oct 6, 2:58 PM PT". The Heilbronn Lean files and `lean/docs/191.md` are byte-identical across `adc7f124`, `fd4aeeb2` and the current HEAD `1581d4c`: `git diff --stat` over those paths is empty, and HEAD only adds `.github/workflows/lock-prs.yml`.

---

## 1. Prior lower bounds and earlier claims

**Best published lower bound before the release: Komlós–Pintz–Szemerédi 1982, (log n)/n².**
- KPS 1982 is Free to Read on Wiley, so I read it through the epdf reader. Source: https://londmathsoc.onlinelibrary.wiley.com/doi/epdf/10.1112/jlms/s2-25.1.13. The theorem, p.14: "THEOREM. There exists a configuration of N points in the unit disc that contains no triangle of area less than C₁ (log N)/N²." It is stated for the **unit disc**, which is the Erdős #507 setting.
- Zakharov's survey (published 3 Mar 2026; see §2) gives KPS 1982 as the lower bound: "in 1982, Komós, Pintz and Szemerédi [13] showed that there exists a collection of N points in [0,1]² with all triangles having area at least Δ(N) ⩾ c log N / N²." The survey mentions no later improvement.
- Ben Green's open problems list (PDF CreationDate 30 Jan 2026), https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf, Problem 77: "Komlós, Pintz and Szemerédi [197] showed that the o(1)-term is necessary". The updates for 2023 and 2025 cover only the upper bound (CPZ).
- The live erdosproblems.com/507 page (saved 2026-10-22 15:03Z; "last edited 30 December 2025"): "The current best bounds are \[\frac{\log n}{n^2}\ll \alpha(n) \ll \frac{1}{n^{7/6+o(1)}}.\] The lower bound is due to Komlós, Pintz, and Szemerédi [KPS82]."
- Wikipedia "Heilbronn triangle problem", current revision 1381407762 of 2026-10-22: "Their construction shows that Δ(n)=Ω(log n / n²)". The article does not mention OpenAI.
- **Improving the log factor:** none found. My coverage was the sources above plus an arXiv `all:Heilbronn` search, newest first, back to Feb 2024, with every abstract containing "lower bound" checked. The only lower-bound improvements on the (log n)/n² scale since 1982 are deterministic, polynomial-time versions of KPS (Bertram-Kretzberg–Hofmeister–Lefmann). Those are the same bound, not a better one; this is from memory and Wikipedia's "The proof can be derandomized", and I did not re-fetch it.

**Ellmann, arXiv:1703.03297.** The current version **is v12**, 12 Nov 2025 (abs page history: "[v12] Wed, 12 Nov 2025 12:33:48 UTC (374 KB)"; v3 was a withdrawal stub). Source: https://arxiv.org/abs/1703.03297v12, PDF read in full, 8 pages. What it claims: c n^{−3/2} log^{−7/2} n for the unit circle (disk).
- p.1: "In this paper we are going to use a heuristic method to prove the following: Theorem 1: … Au ≥ c n0^{-3/2} log^{-7/2} n0 if n0 > n1."
- p.3: "In fact, we assume that the hit points are uniformly distributed on the r circle, also between neighbouring R vertices. This assumption makes the article heuristic."
- p.3: "Although we cannot prove that the hit points (of any possible P and Q) are uniformly distributed in the 2π long arc between neighbouring R vertices, it may still be assumed."
- Theorem 4 is stated on p.5 ("Theorem 4: If the Δ's three vertices are elements of the Set and they fall on two or three polygons, then max(Z) = c N^{–1}/√log N"). Its proof runs over pp.5–6 and uses the assumption. p.5: "The heuristic assumption was that the probability of the hit point falling into the exclusion zone around the nearest R is less than Z/π". p.6: "… points that will be deleted with Z/π probability."
- **Verdict: the paper's description is ACCURATE** ("acknowledges an unproved local uniformity assumption and describes the argument as heuristic [p.3]; the deletion estimate uses this assumption [Theorem 4, pp.5–6]"). Note that the arXiv **abstract** does not say "heuristic"; only the PDF does.

**Agama, arXiv:2006.05269.** The current version **is v13**, 6 May 2026 (history: "[v13] Wed, 6 May 2026 17:31:57 UTC (11 KB)"). Source: https://arxiv.org/abs/2006.05269v13, PDF read, 13 pages. What it claims: Δ(s) ≫ (log s)/(s√s) on the unit disk. Theorem 4.1 runs over pp.12–13.
- p.12, proof of Theorem 4.1: "In this circle locate (s − 3) admissible points so that the chord joining each pair of adjacent (s − 1) admissible points including ⃗x and V_m[⃗x] is equidistant. We join each of the (s − 1) admissible points considered to the center of the circle … We join all pairs of adjacent admissible points considered by a chord and produce (s−1) triangles of equal area."
- **Verdict: the paper's description is ACCURATE but incomplete, and understated.** The configuration is a regular (s−1)-gon plus its centre. A diameter's endpoints and the centre are collinear **only when s−1 is even**. My check (`W_work/scripts/agama_check.py`): s=9 gives minimum area 1.5e−17, s=21 and s=41 give 0, while s=10, 22 and 42 have no collinear triple. The stronger objection is the one the paper does not make: with or without the centre, three consecutive vertices of a regular m-gon of radius R span area 2R² sin²(π/m) sin(2π/m) ≈ 4π³R²/m³. That is **Θ(s^{−3})**, so the construction contradicts its own claimed (log s)/s^{3/2} for every large s. Numbers at R=½: s=42 gives 4.47e−4 against a claimed 1.37e−2. Our own report/507 already proves this boundary formula (β(n)=2 sin²(π/n) sin(2π/n)). The paper's sentence "Omitting the center leaves the every-triple estimate unproved" is true but too weak: the omitted case is not merely unproved, it is false for this configuration. Classification: EXPOSITION / ERROR-NONFATAL. It has no bearing on Theorem 1.1.
- Agama's claim also appears on academia.edu as "AN IMPROVED LOWER BOUND OF HEILBRONN'S TRIANGLE PROBLEM", 13 pp., same bound (https://www.academia.edu/116435929/; read through a browser).

**Other power-lower-bound claims, 2024–2026.** All the new ones are later than the OpenAI release and conditional on it:
- **Ivan Blinov (@littleBro)**, https://github.com/littleBro/heilbronn-triangle-bounds, repository created 2026-10-08. README: "A conditional research draft by Ivan Blinov (@littleBro), extending OpenAI math family 191 … The claim is for every sufficiently large n, conditional on the pinned manuscript's geometric estimates and the written transfer." Its η runs from 1/145,278,430 up to 1/50,893,237 on the board. Its own review guide says "Slab, lattice, orbit, weighted count and deletion | Pinned manuscript and written transfer | No complete independent upstream audit". So the repository **assumes** OpenAI's §§2, 4–8; it does not check them.
- **Qiuyu Chen (Euler)**, https://github.com/canghaimeng/openai-math-improvement/blob/b3c7abea0d5e392777498816ca837eded8b85669/problems/bound-191/README.md, repository created 2026-10-19. Claims η = 2/100866719 "using Blinov's degree-five norm decomposition, reserved labels and slab estimate". The board says: "No Lean proof is supplied for this result … no independent check."
- These are collected on https://bigospeedrun.com/other/heilbronn-triangle, where every entry is labelled "Claimed: their authors published them, and we have not checked them."
- No independent (non-OpenAI-derived) power-lower-bound claims from 2024–2026 turned up beyond the Ellmann v6–v12 and Agama v9–v13 revisions. Coverage: arXiv `all:Heilbronn` back to Feb 2024, WebSearch, Hacker News, Reddit. viXra, ResearchGate and X were not directly searchable (see §7).
- **Do not conflate:** Logunov–Zakharov, arXiv:2511.10509 (13 Nov 2025), gives a human **power improvement for the point–line minimal-distance problem**: "the distance from p_i to any other line ℓ_j is at least c n^{γ−1} … better than a trivial construction by a polynomial factor." That is not a Heilbronn lower bound. Zakharov's survey uses it to bound what the incidence method can reach.

## 2. Zakharov, "Small triangles", J. London Math. Soc. 113(3) (2026) e70447

DOI 10.1112/jlms.70447, online 3 Mar 2026. Crossref gives the licence as **CC-BY 4.0** (open access). curl, Bright Data and Hetzner all hit Cloudflare 403, so I read it through a real browser: https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70447. The math below comes from the MathML alttext. I found no arXiv version (arXiv API title and author search; OpenAlex reports "any_repository_has_fulltext: False").

- **§3 ("3 DENSITY INCREMENT ARGUMENT"), its first sentence:** "Even though Heilbronn's conjecture turned out false, many believe (including Szemerédi [1, 7]) that it is ‘almost’ true: Δ(N) ⩽ C_ε N^{−2+ε} for any ε>0." Here [1] is Brass–Moser–Pach, *Research problems in discrete geometry* (2005), and [7] is Erdős, *Problems and results in combinatorial geometry*, Ann. NY Acad. Sci. 440 (1985).
- **§6 ("6 FURTHER DEVELOPMENTS"):** "any improvement would be very interesting — despite major progress, we are still very far from the conjectured Δ(N) ≲ N^{−2+o(1)}."
- **§6 table of upper bounds, last row:** "Best possible | Δ ≲ N^{−2+ε}".
- **Status:** in §3 it is a **belief** attributed to "many … including Szemerédi". In §6 it is called "the conjectured" bound. The survey does not pose it as a question. The paper says "The almost n^{−2} formulation, discussed in Zakharov's survey [Section 3], asks whether, for every ε>0 … Δ(n) ≤ C_ε n^{−2+ε}". The section reference and the formula are correct, and "discussed" is fair. "Asks whether" is the paper's own framing; the survey states a belief and a conjecture. Classification: EXPOSITION. The cleaner citation is §3 together with §6 ("the conjectured Δ(N) ≲ N^{−2+o(1)}").
- **A source the paper does not cite:** Green's open problems list, Problem 77, asks exactly this as a question: "Given n points in the unit disc, must there be a triangle of area at most n^{−2+o(1)} determined by them?" erdosproblems.com/507 cross-links it ("This problem is Problem 77 on Green's open problems list"). Formal Conjectures has it as `green_77`, still `@[category research open, question …]` (§6 below).

## 3. Cohen–Pohoata–Zakharov citations

- **arXiv:2305.18253: v1 is the only version** (abs history: "[v1] Mon, 29 May 2023 17:20:57 UTC"). Theorem 1.1, p.2: "For sufficiently large n, any set of n points in the unit square contains three points forming a triangle of area at most ∆ ⩽ n^{−8/7−1/2000}." **Matches the paper.**
- **arXiv:2409.07658: v2 is current** (18 Mar 2025, "To appear in Inventiones Mathematicae"). Theorem 1.8: "For any ε > 0, every set of n points in the unit square contains a triangle of area ∆ ≲_ε n^{−7/6+ε}." **Matches.** The published Invent. Math. 240(3), 1045–1118 (online 14 Mar 2025, CC-BY) also numbers it "Theorem 1.8"; I checked this on the Springer page through a browser. The bibliographic details in `references.bib` match Crossref.

## 4. KPS 1982 §2 and Roth 1951's appendix

- **KPS 1982 §2 ("2. The proof of the theorem"), pp.15–16, read in full.** "We define a 3-graph G on these n points (as vertices) by {a,b,c} ∈ G if the points a, b, c form a triangle of area less than A." … "Now we show that, with large probability, only o(n) short cycles occur in this 3-graph." … "Thus deleting all vertices in 2-3-4-cycles, we get a 3-graph with girth greater than 4. Hence, by Lemma 1, it contains at least c₂(n/t)(log t)^{1/2} = N independent vertices." Lemma 1 is the independence bound for 3-graphs of girth >4. The paper describes this as "edges of a hypergraph, removes short cycles, and uses a stronger independence bound … [Section 2]". **ACCURATE.** Strictly, Lemma 1 is stated in §1 and proved in §§3–4; §2 applies it, which is how the paper words it.
- **Roth 1951** is Free to Read on Wiley (epdf viewer; the OCR is poor). p.198: "Erdős has proved‡ that … ‡ His proof of this result is given in the appendix." Appendix, p.204: "In order to prove that … it clearly suffices … to construct p distinct points (u_ν/p, v_ν/p), where u_ν and v_ν are non-negative integers less than the prime number p, such that no three of the points P_ν are collinear. The construction given below is due to Erdős: x_ν = ν/p, y_ν = (1/p)(ν² − p[ν²/p]), ν = 0,1,2,…,p−1. Then no three P_ν are collinear." These are the parabola's residues mod p. The paper's "Erdős's finite-field parabola, recorded in Roth [Appendix]" and "see Roth [p.198]" for Heilbronn's conjecture are both **ACCURATE**.

## 5. Replays and checks of OpenAI's Lean for this family by others

Search used: `gh search code HeilbronnTriangle` / `heilbronn_power_lower_bound` / `almost_n_minus_two_refuted`. **At least three independent kernel replays predate today, so our replay is NOT the first.** All three ran on `fd4aeeb2` or the identical-content files. Ordered by date:

| Who | When | What ran | Result |
|---|---|---|---|
| **mathvet/mathvet**, `reviews/openai-math/evidence/cloud/HeilbronnTriangle.comparator.txt` (https://github.com/mathvet/mathvet) | run 2026-10-08 15:13:51Z–15:21:03Z, committed 15:33:30Z | Comparator in a landrun sandbox, **Lean default kernel only** (OpenAI's config has `"enable_nanoda": false`) | "Lean default kernel accepts the solution / Your solution is okay! / == comparator exit=0". Fidelity table, family 191: verdict **"weaker-statement"**, note "`heilbronn_power_lower_bound` only yields an unbounded sequence of sizes … not 'for every sufficiently large n'". |
| **carlostoledo1891/cert-machine**, `corpus/openai-math/kernel-runs/38019899278/HeilbronnTriangle.json` (https://github.com/carlostoledo1891/cert-machine; there is no `cert-machine` org, `gh api users/cert-machine` returns 404) | run B1, recorded in commit d93dd5b 2026-10-10T08:34:51Z | Comparator d03acab1 (v4.34.0), Lean 4.34.1, lean4export 076e8e57, **nanoda enabled by them** | `"okay": true`, `"kernels": ["Lean default kernel accepts the solution", "nanoda kernel accepts the solution"]`, 701 s, 9,118 build jobs. Their reading file (2026-10-10, `readings/first/batch4.json`) labels 191 **"NARROWER — DECLARED"**, with the gap "Only an unbounded sequence of sizes n_j is stated, not every sufficiently large n." |
| **nealmcb/openai-math-lean-tooling** (https://github.com/nealmcb/openai-math-lean-tooling) | `results/cmp-all/configs.csv`: started 2026-10-11T10:10:02Z; `results/kernel-pair-sweep.jsonl`: 2026-10-15T03:57:24Z | Comparator (nanoda False), then a separate export with both kernels | configs.csv: "HeilbronnTriangle,accepted,…,nanoda False". Kernel sweep: "lean_verdict": "Lean kernel accepts; replay 87733 ms", "nanoda_rc": 0, "nanoda_decls": 72308, export 587,366,573 bytes. |

Side note from nealmcb's REPORT.md §3h, a sweep of modules no Comparator config imports. A Heilbronn-family declaration, `OAI.Problem355.MainDigitLaw.sampled_orbit_det_gt` in `MainDigitBadTripleBound.lean`, "fails in the pinned nanoda (it passes in 8.9 s with upstream master …) … Lean's kernel accepts it in the build". That module is **not** in the Main closure: it is absent from `/tmp/oaimath/191/closure_order.txt`. The failure is a nanoda stack limit on an orphan module and does not affect the two theorems.

Other non-replay mentions: `bigospeedrun/verifier` (statement contribution, accepted 2026-10-21), `plasma-ai/erdos` (claim card, created 2026-10-07), `anantgupta2/AI-hard` (classification dataset: "lean_vs_headline": "weaker"), `dwootton/openai-math-explorer`, `TimeLordRaps/lean4-explainer`, `aikjx/openmath` (mirrors).

## 6. Formal Conjectures and the teorth database

- **FC `FormalConjectures/ErdosProblems/507.lean`, current main** (identical to the saved `/tmp/oaimath/191/paper/fc_507.lean`; last commit 32ac619 2026-10-15, a style change). `erdos_507.equivalent`, `erdos_507.lower` and `erdos_507.upper` are all `@[category research open, question value, AMS 51]`, with `answer := sorry`. `erdos_507.lower` asks for `(lowerBest =o[atTop] answer) ∧ (answer ≪ α)` with `lowerBest n = log n / n²`. The paper's every-n theorem, transferred to the disk, would answer it. The sequence-only Lean does not literally fit `≪ α`, because `α` must dominate the answer for all large n. Variants are `research solved`: `upper_trivial`, `lower_erdos`, `lower_kps82`, `upper_cpz24`.
- **FC `GreensOpenProblems/77.lean`:** `@[category research open, question, AMS 5 52] theorem green_77 : ∃ (o : ℕ → ℝ), Tendsto o atTop (𝓝 0) ∧ α ≪ fun n ↦ n ^ (-2 + o n)`. This is exactly the almost-n^{−2} statement for the disk, and it is still open in FC. Even OpenAI's **sequence** theorem would refute it, after the square-to-disk transfer, because a sequence with α(n_j) ≥ c n_j^{−2+η} contradicts α ≪ n^{−2+o(1)}. Nobody has filed this.
- **Issues and PRs:** searches for "Heilbronn", "507 in:title", "erdos_507", "Erdős 507", "Erdos 507", "OpenAI Heilbronn" and "power improvement Heilbronn" in google-deepmind/formal-conjectures found **no** issue or PR about OpenAI's proof. Hits were #760 (closed 2025-10-06), #1948/#1951 (closed 2026-01-31), #2169 (merged 2026-02-05), #2674/#3196 (closed 2026-03-03) and #5520 (merged 2026-09-10, "fix(ErdosProblems/507): minTriangleArea uses unsigned areas of all triples"). All predate the release.
- **teorth/erdosproblems `data/problems.yaml`** (main HEAD bfa61c4, 2026-10-22T14:34Z), entry 507: `status: state: "open", last_update: "2025-08-31"`; `informal_status: "open"`; `formalized: state: "yes", last_update: "2026-02-10"`; `comments: "Heilbronn's triangle problem"`. It has not changed since the release.

## 7. Public discussion

- **erdosproblems.com/507** (saved 15:03Z): "Comments (0) Proof claims (0)", "No proof claims have been submitted yet", and "The ability to post new comments has been suspended."
- **Bloom's blog post "Erdős problems in the OpenAI proofs"** (8 Oct 2026), re-fetched today in a browser from https://www.erdosproblems.com/forum/thread/blog:10: "There are significant claims relevant to 25 Erdős problems. The relevant problem numbers are: [3], [90], [120], … [1150]." **#507 is not in the list.** Today's copy and the 11 Oct snapshot agree, and no comment mentions Heilbronn. His general disclaimer reads: "all of these should be read as 'claims' … This post should not be read as any kind of endorsement".
- **Tao.** WordPress post search for "Heilbronn" returned only the 2026-10-20 Siegel-zero post (about Heilbronn–Linfoot), none on the triangle problem. Of the 45 posts since 2026-09-20, none is on Heilbronn. Mathstodon @tao, every status since 2026-09-03, searched for "Heilbronn|triangle": 0 hits. I could not search the blog comments; the WP API ignores the search parameter for comments.
- **MathOverflow / Math.SE** (SE API, since Sep 2025): no Heilbronn-triangle questions or answers.
- **Hacker News** (Algolia): no item mentioning "Heilbronn" after 2026-10-05. The Oct 2–5 items are about a "Heilbronn Problem" small-n records site.
- **Reddit:** the only relevant result is r/LLMmathematics, "Open Math Courses + Audit/Lessons on (some of) the new OpenAI results" (u/lepthymo, ~11 Oct). It lists "Heilbronn's triangle problem 8 [lessons] 191, the Heilbronn triangle lower bound", AI-written ("getting Opus 5.5 (Max) to work through some of the new Proofs by OpenAI"). It is not an expert review.
- **Quanta:** no article found (WebSearch). **X/Twitter: COULD NOT CHECK.** A logged-in browser search hit a Cloudflare "Performing security verification" challenge at x.com/account/access, and web search does not index X.
- **Expert endorsement or dispute:** none found in any of the sources above. Zakharov, Pohoata, Cohen, Sawhney and Bloom have said nothing on this claim that I could find; that is a statement about the sources I covered, not proof of absence.
- **Has anyone noticed that the Lean proves only an unbounded sequence?** Yes, several, starting with OpenAI's own scope note (`lean/docs/191.md`): "The linked construction is for an unbounded sequence of sizes; the paper's statement for every sufficiently large n is broader." The others:
  - mathvet, 2026-10-08: "weaker-statement".
  - cert-machine, 2026-10-10: "NARROWER — DECLARED".
  - littleBro README, quoted by bigospeedrun: "The original upstream Lean comparator uses a different exponent and a subsequence statement."
  - bigospeedrun statement PR, 2026-10-19/21: "Subsequence instead of every large n. … sparse good n do not give every large n, since Δ is only monotone."
  - AI-hard dataset: "lean_vs_headline": "weaker".

## 8. Our own site: https://erdosproblemaday.com/report/507

HTTP 200, 62,519 bytes, fetched via curl. What it states:
- **Header:** "ERDőS #507 · PARTIAL | Community database OPEN as of 2025-08-31".
- **Banner:** "Newer public claim (6 Oct 2026): OpenAI's internal-model release claims, for this problem, Heilbronn: α(n) ≥ n^(−2+η), improving Komlós–Pintz–Szemerédi — family 191 at github.com/openai/math, a Lean file is linked. Bloom calls these claims, not endorsements; anything on this page that says the question is open was written before that release and has not re-checked it."
- **Body (wave w041, 2026-07-31), stating the best bounds:** "the current bounds \[\frac{\log n}{n^2}\ll \alpha(n) \ll \frac1{n^{7/6+o(1)}}.\]". Later: "The asymptotic problem remains open at the live-page gap \[\frac{\log n}{n^2}\ll\alpha(n)\ll n^{-7/6+o(1)}.\]". The finite results α(3)=3√3/4, α(4)=1, α(5)=√(5(5−√5)/32), and β(n)=2 sin²(π/n) sin(2π/n) for all-on-circle sets.
- **Problems with the banner:**
  1. "Bloom calls these claims" suggests Bloom covered this family, but his post does not list #507.
  2. "α(n) ≥ n^(−2+η)" leaves out the constant c₁, the threshold n ≥ n₀, and the fact that the paper is stated for the unit square; the move to the disk is a trivial translation.
  3. It says "a Lean file is linked" without saying the Lean covers only an unbounded sequence.

---

## Safe to say on our page vs do not say

**Safe to say (with the cited sources):**
- Before OpenAI's 6 Oct 2026 release, the best lower bound was KPS 1982, (log n)/n² (stated in the unit disc). erdosproblems.com/507, teorth (open, 2025-08-31) and FC (`research open`) still list it as of 2026-10-22.
- OpenAI's paper (dated 25 Sep 2026, published 6 Oct 2026) claims Δ(n) ≥ c₁n^{−2+η} for every n ≥ n₀, with η = 2/(45435k+16) ≈ 3·10^{−236}.
- OpenAI's Lean, by its own scope note, proves only an unbounded sequence of n, with η = 1/(100000·k). That is enough to refute the almost-n^{−2} statement.
- Independent Comparator replays already exist: mathvet (2026-10-08, Lean kernel), cert-machine (2026-10-10, Lean kernel and nanoda) and nealmcb (2026-10-11 Comparator; 2026-10-15 Lean kernel and nanoda). All accept. Ours is at best a further replay.
- The almost-n^{−2} statement is a belief/conjecture in Zakharov's survey (§3 "many believe (including Szemerédi)"; §6 "the conjectured Δ(N) ≲ N^{−2+o(1)}"). It is a question as Green's Problem 77 and FC `green_77`, both still open in FC.
- Ellmann v12 is self-described as heuristic. Agama v13's Theorem 4.1 construction is a regular polygon (plus centre) and has triangles of area Θ(s^{−3}).
- No expert endorsement or dispute was found as of 2026-10-22 on erdosproblems (0 comments, 0 proof claims), Bloom's blog (which does not list #507), Tao's blog or Mathstodon, MathOverflow, Hacker News, Reddit or Quanta. X was not checked.
- Later follow-ups (Blinov; Chen/Euler) claim larger η, conditional on OpenAI's manuscript. They are unchecked.

**Do not say:**
- That ours is the "first" replay or check of the Lean. It is not.
- That the Lean proves the every-n Theorem 1.1, or "α(n) ≥ n^{−2+η}" without c₁, n₀ and "(paper; Lean: along a sequence)".
- That Bloom, Tao, Zakharov or any expert has endorsed, examined or disputed this claim, or that Bloom listed #507.
- That Zakharov's survey "asks" or "poses" the question. It reports a belief and a conjecture; the question form is Green's Problem 77.
- That Agama's bound fails *only* because of the centre, or that the collinear triple occurs for every s. It occurs only for s odd.
- That there were no earlier power-lower-bound claims. There were two, both flawed: Ellmann is heuristic and Agama's construction is broken.
- That the Blinov or Chen improvements are established, or independent of OpenAI's §§2–8.
- That #507 is "solved". Even the paper's claim leaves the true order open: n^{−2+η} ≪ α(n) ≪ n^{−7/6+o(1)}.

---

VERDICT (world and priority only, not the mathematics): HOLDS AS READ for the paper's citations and its descriptions of prior work, with two EXPOSITION notes. First, Zakharov's text is a belief/conjecture, not a question. Second, the Agama objection is accurate but understated (the collinear triple needs s odd; the stronger defect is Θ(s^{−3}) triangles). Green's Problem 77 is the uncited source of the question form.

Three places I was most suspicious of, and what settled each:
1. **Whether Zakharov's §3 really states the almost-n^{−2} formulation.** Settled by reading the CC-BY full text in a real browser: §3, first sentence, quoted above, together with the §6 "conjectured" sentence.
2. **Whether our Lean replay could be called "first".** Settled against it: three dated third-party Comparator/kernel replays (mathvet 10-08, cert-machine 10-10, nealmcb 10-11/10-15), all on content identical to HEAD.
3. **Whether the paper's Agama objection is fair.** Settled by reading v13 pp.12–13 and running the configuration numerically. The objection is accurate for odd s; the construction fails more basically for all large s.
