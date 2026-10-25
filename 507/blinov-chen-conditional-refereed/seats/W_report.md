VERDICT: HOLDS WITH FIXES. Scope: world, priority and prior art only, not the mathematics. What our 22 Oct page says about the outside world is accurate: both claims are unchecked, there is no complete Lean proof, and BOS marks every row "Claimed". The new page still needs four credit and quotation fixes (F6, F8, F3-NIT, F4), and it should report the 3-AP-free finding in F9.

Seat W, 2026-10-22. Every fetch was made on 2026-10-22 between 21:11:25Z and 21:37:23Z unless a time is given. Raw pages, API JSON and scripts are in /tmp/oaimath/191b/seats/W_work/ (raw data in raw/). File names are given in [brackets].

---

## Findings

### F1. Nobody has checked, refereed, refuted or replicated either claim (SHOULD-FIX: say exactly this, with the evidence)
Every place I looked, and what it showed:

- **Blinov's repo**, https://api.github.com/repos/littleBro/heilbronn-triangle-bounds [gh_blinov_repo.json]: `"has_issues": false, "has_discussions": false, "forks_count": 0, "stargazers_count": 0`. All 13 PRs (#1–#13) have 0 comments, 0 reviews and 0 review comments. Commit comments: 0 [gh_blinov_pulls_all.json, gh_blinov_pr*_reviews.json, gh_blinov_issue_comments.json, gh_blinov_pr_review_comments.json, gh_blinov_commit_comments.json]. **The 1/50,893,237 claim is the head of PR #13, which is still open and not merged.** PR #13 is titled "Reserve tag words inside the packing for a 2.85x exponent gain", created 2026-10-15T21:07:25Z, head e29a291 on branch research/five-packing-compression. `main` is at 4573878 and carries 1/145,278,430.
- **Chen's repo**, https://api.github.com/repos/canghaimeng/openai-math-improvement [gh_chen_*.json]: one commit, b3c7abe (2026-10-19T11:43:27Z, "Qiuyu Chen <canghaimeng@sjtu.edu.cn>"). 0 issues, 0 PRs, 0 comments, 0 forks, 0 stars, 0 releases.
- **BOS race page**, https://bigospeedrun.com/other/heilbronn-triangle [bos_other_heilbronn-triangle.html; byte-identical to live/bos.html], "Data updated Oct 22, 1:17 PM PT":
  - The page says: "These results are Claimed: their authors published them, and we have not checked them."
  - The proof scope in Chen's row: "No Lean proof is supplied for this result. The proof is the PDF paper in the repository; no independent check."
  - Its structured data [board_bigospeedrun_com_chat-knowledge_json.raw] gives `"claimCount": 9, "relevantRepos": []`.
- **BOS race board**, https://board.bigospeedrun.com/api/posts?board=other-heilbronn-triangle&format=md [board_heilbronn_feed.md/.json]: "No posts yet."; JSON `"posts":[]`.
  - Positive control: the matrix-multiplication board feed has posts (12,100 bytes).
  - Negative control: an unknown board name returns 404 `unknown_board`.
- **BOS verifier**, github.com/bigospeedrun/verifier [gh_bosv_*.json, bosv_*]:
  - Only a *statement* exists. PR #20 by Joshua Cortez added `BigOSpeedrun.HeilbronnTriangle.Bound η`; it was merged as 079ac7b4 on 2026-10-21T18:30:36Z.
  - Maintainer comment on PR #20, 2026-10-21T18:37:04Z: "Enabling Lean submissions for the Heilbronn row is a separate step that we announce later."
  - challenges/heilbronn-triangle/README.md: "Merging the statement alone would not make any saving Lean Verified, and no current board record has a complete Lean proof." The README's own example is `Bound (1 / 50893237 : ℚ) := by sorry -- placeholder`.
  - None of the verifier's 42 issues/PRs is a Heilbronn proof. Chen's only submission there is #16, for DFT.
- **erdosproblems.com/507**, the forum thread and the proof-claims tab, fetched via Hetzner [erdos_507*.html/.txt]:
  - All three pages show "Comments (0)" and "Proof claims (0)". The claims tab says "No proof claims have been submitted yet." The thread says "The ability to post new comments has been suspended."
  - The page is "last edited 30 December 2025". It still gives (log n)/n² ≪ α(n) (Komlós–Pintz–Szemerédi 1982) and does not mention OpenAI.
  - Positive control: forum/thread/1 shows "Comments (6)" and "Proof claims (2)" [erdos_control_*].
- **teorth/erdosproblems** [teorth_problems.yaml]: #507 is `state: "open"`, `last_update: "2025-08-31"`. Issue/PR search for "507" and for "heilbronn" returns 0 (control: "477" returns 3).
- **mahrud/openai-math-comments PR #191**, "A power improvement in the Heilbronn triangle lower bound" [mahrud_pr191*.json]: 0 comments, 0 reviews, 0 review comments, 0 commit comments. Control: 12 other PRs in that repo have comments. Its README forbids LLM comments.
- **google-deepmind/formal-conjectures**: no issue or PR about 507, Heilbronn or Green 77 created after 2026-10-05. Earlier items: #1948/#1951 (Jan 2026), #2169, #2674, #3196, #5520, #760.
- **plasma-ai/erdos wiki** [misc/plasma_E0507_*.md]: E0507/claims has a single entry for OpenAI (`status: claimed`, updated 2026-10-17T21:49:34Z). There is nothing on Blinov or Chen.
- **arXiv API** (all:heilbronn; abs:heilbronn AND abs:triangle; sorted by date) [arxiv_api_*.xml]:
  - The newest Heilbronn-triangle preprint is 2609.25035 (published 2026-08-24). There is nothing after 6 Oct.
  - The author queries "au:Blinov" and "au:Chen_Qiuyu" return no Heilbronn paper. Chen's Euler report, 2610.19864 (14 Oct), predates the result and its abstract does not mention it.
- **Hacker News** (Algolia, from 2025-10-05) [hn_*.json]: no story or comment mentions OpenAI's Heilbronn result, Blinov or Chen. The query "openai heilbronn" returns 0.
  - The "OpenAI withdraws three mathematical results" thread (item 50002650, 575 nodes) never mentions Heilbronn or 191 [hn_item_50002650.json].
- **MathOverflow and Math.SE** (StackExchange API, "heilbronn", sorted by date): nothing about this since 6 Oct [se_*.json].
- **Tao's blog**, search "heilbronn" [tao_search_heilbronn.html]: only Deuring–Heilbronn posts, including 2026/10/20. Nothing on the triangle problem.
- **Wikipedia, "Heilbronn triangle problem"** (raw text and revision history) [wiki_heilbronn_*]: no mention of OpenAI, Blinov or Chen. The last edit is 2026-10-22T07:18:30Z ("References").
- **Mathstodon #heilbronn tag timeline**: only posts about the German city.
- **Web search** (6 queries, see "Searches"): finds no check, comment or refutation. Every hit for Blinov goes back to his own repo.
- **The closest thing to a replication is Chen's paper itself.**
  - It is not independent. It was produced with an AI agent system (F4) on top of Blinov's pinned checkpoint, and nobody has checked it.
  - Its own words (p.1, §1): "Blinov's pinned checkpoint [2] supplies the degree-five decomposition, reserved tag words, fresh-digit collision argument, and slab refinement." Also: "The remaining estimates are proved here with the constants of the recorded proof." Its reference [2] is "Pinned checkpoint e29a2912; retrieved October 17, 2026."

### F2. OpenAI has not updated the family-191 preprint (NIT: our page can say so)
- `gh api repos/openai/math/commits?path=preprints/A-power-improvement-…-2026` returns one commit only: adc7f12, "Initial commit", 2026-10-06T21:58:50Z [gh_openai_heilbronn_commits.json].
- The tree SHA of that directory is the same, 68d19fc2…, at adc7f12, fd4aeeb, 1581d4c and main. So the 10-08 "Update manuscripts and Lean formalizations" commit did not touch it.
- openai/math has issues disabled. Commit 2710f99 ("Lock pull request conversations when opened") closes the PR route. The repo has only 2 PRs in total, both internal [gh_openai_*.json].

### F3. The BOS board as of 2026-10-22 13:17 PT, and nothing newer than Chen (SHOULD-FIX on use; NIT on BOS)
All 9 rows are Claimed. Ranks, dates in PT, and the source each row links:

| # | η | Author | Date (BOS) | Linked source |
|---|---|---|---|---|
|1|2/100866719 ≈1.98e-8|Qiuyu Chen (Euler)|Oct 19 4:44 AM|canghaimeng/openai-math-improvement b3c7abe bound-191/README.md|
|2|1/50,893,237 ≈1.96e-8|Ivan Blinov|Oct 15 2:07 PM|README @e29a291; PR #13|
|3|1/145,278,430 ≈6.88e-9|Blinov|Oct 13 1:11 PM|README @4573878; commit 840a550|
|4|1/15,789,789,943 ≈6.33e-11|Blinov|Oct 13 12:15 PM|README @ac09885; commit 2d1bd79|
|5|1/10,819,299,076,922,581 ≈9.24e-17|Blinov|Oct 13 8:01 AM|5a73067|
|6|1/(498·15⁷·19⁴+7) ≈9.02e-17|Blinov|Oct 12 10:03 PM|README @448db91; efe6be2|
|7|1/(498·27·23⁹+7) ≈4.13e-17|Blinov|Oct 12 8:51 PM|README @fdf0603; a9f9bfd|
|8|1/(498·39·35⁸+7) ≈2.29e-17|Blinov|Oct 8 5:23 PM|README @f4c2a16; c57cd75|
|9|1/(498·379¹⁷+7) ≈2.92e-47|Blinov|Oct 8 1:04 PM|README @2259fc0; 9891f18|

Evidence level for every row: "Claimed". Baseline row: "OpenAI baseline: ≈3.18·10⁻²³⁶, released Oct 6, 2:58 PM PT". The JSON gives `η>3.17·10^{-236}`. My exact value is 3.1757·10⁻²³⁶, so 3.18 is the rounding and 3.17 is the floor; both are consistent [arith_check_output.txt].

**There is no later checkpoint from either author:**
- Blinov's 11 branches top out at e29a291. The repo was last pushed at `pushed_at 2026-10-15T21:06:51Z` [gh_blinov_branches.json, gh_blinov_repo.json].
- Blinov's public GitHub events from 18 to 20 Oct are all on littleBro/BendKV; none touch the Heilbronn repo [gh_littleBro_events.json].
- Chen's only later events are two Euler README commits (19 and 20 Oct).
- BOS site commit df652e8e (2026-10-19T13:13:39Z) added Chen's row: "Heilbronn (bound-191): eta = 2/100866719 = 1.9828e-8, above littleBro's 1/50893237 = 1.9649e-8" [gh_bos_site_commits.json].

**Blinov's full checkpoint history**, from the README's boxed η at each commit in the local clone. The clone's refs match the live branch list.
- 8 Oct, 14:43 −0300 (7a895cd, the first commit): 1/(1074·403¹⁷+7) ≈ 4.77e-48.
- 8 Oct, 16:18 (a84a29b, slab cap): 1/(498·403¹⁷+7) ≈ 1.03e-47.
- 8 Oct, 17:04 (9891f18): 1/(498·379¹⁷+7).
- 8 Oct, 17:31 / 19:18 / 20:28 (e3ca52e / 2fa58c9 / 5860029): 47¹⁰ / 27¹¹ / 27¹⁰.
- 8 Oct, 21:23 (c57cd75): 39·35⁸.
- 13 Oct, 00:51 (a9f9bfd): 27·23⁹.
- 13 Oct, 02:03 (efe6be2, first use of CGLV): 15⁷·19⁴.
- 13 Oct, 11:32 (a3dbb1e): 1/10,819,300,749,604,981.
- 13 Oct, 12:01 (5a73067): 1/10,819,299,076,922,581.
- 13 Oct, 16:15 (2d1bd79, degree 7): 1/15,789,789,943.
- 13 Oct, 17:11 (840a550, degree 5, label tags plus fresh digit): 1/145,278,430.
- 15 Oct, 18:06 (e29a291, reserved tags): 1/50,893,237.

BOS does not list the 1074·403¹⁷, 403¹⁷-slab, 47¹⁰, 27¹¹ and 27¹⁰ checkpoints.

**NIT, a BOS transcription error.** BOS shows Chen's threshold as "n≥2^{100866718·250}"; the KaTeX source is `n\ge2^{100866718\cdot250}`. Chen's paper (Theorem 1, rendered p.1 checked [W_work/chen_p1-01.png]) has N₀ = 2^{100866718·2^{50}}: BOS dropped the superscript. **Our page must quote the threshold from the paper, not from BOS.**

### F4. Who the authors are and what they disclose (SHOULD-FIX: quote, and note that Chen's PDF is unsigned)
- **Blinov.** GitHub user littleBro, name "Ivan", bio "Playing with computers", X handle ivanBcde, account created 2013 [gh_user_littleBro.json].
  - README l.3: "A conditional research draft by **Ivan Blinov (@littleBro)**, extending OpenAI math family 191, with OpenAI Codex assistance."
  - README l.391: "Research, implementation and drafting used substantial OpenAI Codex assistance."
  - README l.395: "This draft has no independent peer review, priority claim or OpenAI endorsement."
  - CITATION.cff: "Research, implementation and drafting used OpenAI Codex assistance."
  - The pinned commit e29a291 is authored "Ivan <your-email@example.com>", a placeholder. Earlier commits are "Ivan Blinov <3585850+littleBro@users.noreply.github.com>".
- **Chen.**
  - **The PDF has no author line and no AI disclosure.** Page 1 shows the title, abstract and "Date: October 18, 2026" (rendered and checked). The PDF metadata `Author:` field is empty. The only external credits in the text are OpenAI, Blinov, CGLV and Bennett–Martin–O'Bryant–Rechnitzer.
  - Disclosure is in the repo README instead: bound-191/README.md says "Developed with [Euler], a mathematical research system for collaborative reasoning and human-guided exploration." The top README says "We tested Euler on 20 problems from OpenAI's mathematics release. Teams of publicly accessible models obtained results that improve the original published bounds on 8 problems." Its table gives the Heilbronn reasoning time as "38 min".
  - **Chen's own README does not star the Heilbronn result as "community-leading".** Only DFT, the cylinder cover and Laughlin are starred.
- **Euler**, github.com/canghaimeng/Euler [gh_euler_README.md; euler_site_en.txt]:
  - The README says: "Euler is a mathematical research agent system built to help researchers follow and understand the entire reasoning process."
  - It names the models: "Working through Euler, Astra and GPT-6.1 Sol improved the original results on 8 problems". The project site says the same: "Astra and GPT-6.1 Sol worked through Euler".
  - On the CLIs: "Combine Codex, Claude Code, Gemini CLI, Grok, and Cursor Agent".
  - Authors: Qiuyu Chen (Shanghai Jiao Tong University), Qi Wang, Liang Xu, Xin Jin, Baao Xie, Wenjun Zeng. Tech report arXiv:2610.19864. License: PolyForm Noncommercial.
  - BOS credits the result as "Qiuyu Chen (Euler)".

### F5. Lean: no formalization of an every-n bound at either exponent, and no copy of the tagged-moment lemma outside Blinov's repo (SHOULD-FIX: word the coverage honestly)
- Blinov's README: "The full Heilbronn theorem is not formalized." It also lists as written-only: "Instantiating its tag and distinct-label interfaces from the norm packing, identifying the minor exponent with the manuscript's Smith divisor, and the slab, lattice, orbit, deletion and prime-progression arguments."
- Chen supplies no Lean for bound-191; BOS says the same.
- The BOS verifier has the target statement only (F1).
- The only Lean proof of `Bound η` for a positive η that I know of is ours, at OpenAI's exponent (our 22 Oct page).
- GitHub code search, logged in [gh_code_search_log.tsv]:
  - "tagged_small_residue_moment", "total_small_residue_moment" and "reserved_packing" return 0.
  - "HeilbronnTriangle" returns 365. Paging through gives openai/math, its mirrors, BOS, nealmcb, ours, plus AlphaEvolve-style small-n benchmark repos. None is at Blinov's or Chen's exponent.
  - "Problem355" hits are openai/math and LeetCode noise. "FiveTagged" and "FiveTags" hits are unrelated.
  - "50893237" returns noise only. "100866719" and "145278430" timed out (HTTP 408) and were re-run at the end: 8 and 10 hits, all noise (numeric data files). None is Heilbronn-related, and none is Chen's repo, even though Chen's README contains 100866719. So these numeric searches are also coverage-limited.
- **Coverage caveat, measured:** GitHub code search does not index Blinov's repo at all. `repo:littleBro/heilbronn-triangle-bounds Heilbronn` returns 0, while `repo:openai/math almost_n_minus_two_refuted` returns 3 and `repo:canghaimeng/openai-math-improvement Heilbronn` returns 3.
  - So zero code-search hits cannot rule out copies. Blinov has 0 forks.
  - A tree scan of 129 openai-math-related and Heilbronn repos found no file mentioning Blinov, 50893237 or tagged_small_residue outside Chen's repo [scan_out/scan_results.json, scan_log.txt]. That scan read root READMEs plus path-matched files only.

### F6. CGLV arXiv:1909.04785 Theorem 4.1 says less than "rank 18 for det⊗det" (SHOULD-FIX: credit precisely)
Fetched v1 and v2 PDFs [raw/cglv/]. The abs page lists v1 (10 Sep 2019) and v2 (27 Dec 2021), and the journal reference "computational complexity, 31 (1), 2022".

- **The statement (v2, §4.1):** "Theorem 4.1. The Waring rank of det3 is at most 18: R_S(det3) ≤ 18."
- **The proof:** "We give the rank 18 decomposition for det3 explicitly, as a collection of 18 linear forms on C⁹ = C³⊗C³ whose cubes add up to det3 … Let ϑ = exp(2πi/6) …", giving det3 = Σ_{i=1}^{18} L_i³. The coefficients include ±1/3 and ±ϑ.
- **Field:** ℂ.
- **The root:** ϑ = e^{2πi/6}, which satisfies ϑ² − ϑ + 1 = 0. This is exactly Blinov's u and Chen's ℤ[u]/(u²−u+1).
- **"det⊗det" holds only through Lemma 2.4:** "T_skewcw,2^{⊠2} ≅ det3", where T_skewcw,2 = a₀∧a₁∧a₂ (the 3×3 determinant tensor). So Theorem 4.1 is a *symmetric (Waring) decomposition of one 3×3 determinant polynomial*. That polynomial is isomorphic to the Kronecker square of the determinant tensor.
- **The identity actually used is a reformulation.** "3 det A det B = Σ_{t=1}^{18} Π_j h_t(A_{·j},B_{·j})" over any commutative ring with a root of u²−u+1 is Blinov's (notes/sphere-packing.tex §eighteen: "with the second coefficient column multiplied by three"). Blinov proves it in Lean.
- **Chen says this correctly:** "Their theorem states a complex Waring decomposition; the precise finite-field identity needed here is verified coefficientwise below."
- **Numbering:** "Theorem 4.1" is right for v2 and the journal version. In v1 the same result is Theorem 2.11 ("RS(det3) ≤ 18"). Chen pins v2; Blinov cites the bare arXiv number.
- CGLV also note: "The Waring decomposition of 4.1 was generalized in [JT20]" (Johns–Teitler, arXiv:2004.06158). Blinov first used CGLV in efe6be2, 13 Oct, 02:03 −0300.

### F7. The slab cap is Blinov's, first seen 8 Oct 2026 (NIT: date the credit)
- **OpenAI's version.** §5 Lemma `aux:cap` takes "a set S ⊂ {0,…,w−1}³ … with |S| ≥ w³/q", a translate of Γ = {(x,y,x²−νy²)} cut by the full cube. This gives (aux:cap-size) "s ≥ w³/q ≥ q²/(2000³H⁶)".
  - OpenAI's Lean does the same: CapInBox.lean `residueBox q w := Fintype.piFinset (fun _ => residueInterval q w)`, i.e. all three coordinates.
  - "slab" does not occur in sections 01–09 of OpenAI's TeX.
- **Blinov's version** is S = {(x, y, x²−νy²): 0≤x<w, y∈F_q}, with |S| = wq. It first appears in commit a84a29b (2026-10-08 16:18:23 −0300 = 19:18:23Z), with PR #5 opened at 19:18:50Z and merged at 19:43:12Z.
  - His rationale (README at a84a29b): "The short-relation exclusion in upstream Section 5 only bounds the first coordinate."
  - The same README: "Thus s >= q²/(2000 H²), improving the previous q²/(2000³ H⁶) bound." It also says "The cap geometry itself is a written proof".
- I found no earlier source for it.
- BOS's first Heilbronn row (9891f18, 379¹⁷) already includes the slab, but BOS never listed the 403¹⁷ slab-only checkpoint.
- Chen credits the "slab refinement" to Blinov.

### F8. Credit for the base-3 {0,1} set: Erdős–Turán 1936, not Salem–Spencer (SHOULD-FIX if our page says "Salem–Spencer")
- **Erdős–Turán**, "On some sequences of integers", J. London Math. Soc. 11 (1936), p.263 footnote [raw/r3lit/et36.txt, from users.renyi.hu/~p_erdos/1936-05.pdf]: "It is easily seen that r{½(3^k + 1)} ≥ 2^k; for, if u < ½(3^k−1) is any integer not containing the digit 2 in the ternary scale, then the integers u+1 form an A sequence." The text adds: "G. Szekeres has conjectured that r{½(3^k+1)} = 2^k."
- **"Salem–Spencer set" is the generic name for any 3-AP-free set.** Salem and Spencer's 1942 contribution was the nearly-linear construction, which disproved the Erdős–Turán conjecture (Wikipedia, "Salem–Spencer set" [wiki_salem_spencer_raw.txt]). The {0,1} ternary set is OEIS A005836, the lexicographically first such sequence.
- **How the two authors credit it:**
  - Blinov's README: "The ternary progression-free construction is classical ([Moy and Rolnick, Section 4])". Moy–Rolnick is arXiv:1502.06013, "Novel structures in Stanley sequences". He also cites Behrend for the sphere variants.
  - Chen's §2.2 proves 3-AP-freeness inline with no citation: "Let C consist of the integers with twelve ternary digits, each zero or one. If x + y = 2z in C, neither side has ternary carries…"

### F9. A 2,921-element 3-AP-free set fits in [0, 137,692], two-thirds of Blinov's [0, 204,390] (SHOULD-FIX: report it, and hand it to the P and G seats)
- **Blinov's set.** His positions are the first 2,921 base-3 {0,1} words, numbered 0…2920. Word 2920 is 1011011010000₂ read in base 3, which equals 204,390. So his positions fill [0, 204390] and k − 1 = 2·204,390, giving k = 408,781 (checked [arith_check_output.txt]).
- **Wróblewski's table.** J. Wróblewski's "Nonaveraging sets" pages (http://www.math.uni.wroc.pl/~jwr/non-ave/) define a(n) as the least k with an n-element 3-AP-free subset of {1..k}. The same function is OEIS A065825.
  - log50k.txt, line 2921 [raw/oeis/jwr_log50k.txt; identical in log30k.txt]: `2921 137693 1.4828639641 Theorem 216`.
  - methods.htm defines "Theorem N": a(N(q−1)+r) ≤ P(a(q)−1)+k_r, built from a modular solution mod P.
  - DATABASE.TXT gives the witness: `m(216)<=3889 1 8 12 18 …`. The method note says this is the 216-th roots of unity mod 3889.
- **I rebuilt and checked the set independently** [W_work/ap3_check.py, ap3_check_output.txt]:
  - K is exactly {x : x²¹⁶ ≡ 1 mod 3889}, it is 3-AP-free mod 3889, and 3889 is prime.
  - The a(14)=36 witness {1 2 4 8 9 13 21 23 26 27 30 32 35 36} is 3-AP-free.
  - q=14, r=113. The best affine image c·K+d is c=1331, d=640, giving k_r=1578, so the bound is 3889·35+1578 = 137,693.
  - The constructed set has |A|=2921, min 1, max 137,693, and is **3-AP-free**. The witness is saved [W_work/witness_2921_in_1_137693.txt].
  - Negative controls, all rejected as they should be: {1,2,3}; K with an AP completion mod P; A plus an AP completion; an interval used as the modular set; the ternary set plus an AP completion.
- **What this means for Blinov's k.** In [0,X] form, X = 137,692, against 204,390, a ratio of 0.674. If the 2,921 positions need *only* 3-AP-freeness (the matching property reduces to u(a)+u(a') = 2u(a'')), then k = 2X+1 = 275,385 instead of 408,781. With Blinov's formula η = 2/(249k+5), that would give 1/34,285,435.
  - **I have NOT checked that only 3-AP-freeness is needed.** Blinov's tag lemma uses "tag span ten": tags 0,1,3,4,9 lie below 10. In this set the five smallest elements, shifted to start at 0, are 0, 15, 16, 21, 22 (span 22). That question belongs to the P/G seats.
- **Other numbers from the same table:**
  - The same table puts a 3,680-element 3-AP-free set inside Blinov's own interval: a(3680) = 201,215 ≤ 204,391.
  - It gives 2,340 elements below 100,000. GGK's 2025 survey [raw/r3lit/2501.01634.txt, Table 8] gives 2,048 at n=10⁵ for base 3, the best of their methods there.
- **The site warns about its own reliability** (index.htm): "Therefore the results published on this website are not reliable. I apologize for that." The warning concerns "Search" rows; the n=2921 row is "Theorem 216", and I reproduced it independently.
- **Bounds on the smallest X:**
  - Exact r₃ is known only up to N=211: OEIS A003002 b-file (Cariboni), r₃(211)=43 [raw/oeis/b003002.txt].
  - By subadditivity r₃(N) ≤ ⌈N/211⌉·43, so any 2,921-element 3-AP-free interval has more than 14,137 integers.
  - **Best known (that I found): 14,137 ≤ X ≤ 137,692.** Nobody publishes an optimum at this size.
  - The NrootN page states a(n) ≤ n√n "is true for n<=1,408,000". For n = 2921 that is ≈157,868, weaker than 137,693.

### F10. Chen's comparisons check out (NIT, confirmation only)
- 249·408781+5 = 101,786,474, so Blinov's η is 1/50,893,237. With k = 1,166,895 the same formula gives 1/145,278,430.
- 2/100866719 > 1/50893237; the ratio is 1.00912, a 0.91% gain [arith_check_output.txt].
- Negative controls: k=408,780 does not reproduce 1/50,893,237, and 2/101,786,476 < 1/50,893,237.

---

## What I checked and how
- **GitHub, read-only via `gh api`:**
  - repos, branches, commits, issues, PRs, reviews, comments, forks, releases and events for littleBro/heilbronn-triangle-bounds, canghaimeng/openai-math-improvement, canghaimeng/Euler, openai/math (path-filtered commits, directory tree SHAs), bigospeedrun/{verifier,site,watch,board}, mahrud/openai-math-comments, teorth/erdosproblems, google-deepmind/formal-conjectures, plasma-ai/erdos, korbonits/korbonits.github.io, tejstead/heilbronn-site;
  - search/code and search/repositories, with the queries listed below;
  - a scan of 129 repos with W_work/scan_repos.py (scan_log.txt).
- **BOS:** curl with a Chrome UA for the race page, about page, llms.txt, chat-knowledge.json and the board HTML and feeds. Feed controls on two other boards; parsed with Python.
- **erdosproblems.com:** fetched via `ssh deploy@100.103.211.37 curl` with a Chrome UA (/507, /forum/thread/507, /forum/thread/507/proof-claims, plus control threads).
- **arXiv:** export API (HTTPS) and abs/PDF pages. CGLV v1 and v2 PDFs converted with pdftotext.
- **Other sources:** HN via the Algolia API; StackExchange API; Wikipedia raw text and revision API; Tao's blog search; Mathstodon tag timeline; OEIS via Hetzner (exe.dev gets Cloudflare 403); Wróblewski's pages and logs.
- **Chen PDF:** page 1 rendered with pdftoppm and inspected; pdfinfo; pdfdetach -list shows an attached mathematical-supplement.zip, which I did not open.
- **Computation:** ap3_check.py and arith_check.py, both run under `ulimit -v 8000000` and timeout. Each has negative controls, and all of them reject.

## Searches run (including those that found nothing)
- **GitHub code search:**
  - HeilbronnTriangle: 365 (pages 1–4 read).
  - heilbronn language:Lean: 34, none relevant beyond FC, ours and Davenport–Heilbronn.
  - Problem355: 407 (openai/math plus noise).
  - reserved_packing: 0. tagged_small_residue_moment: 0. total_small_residue_moment: 0.
  - FiveTagged: 5, noise. FiveTags: 778, noise. 50893237: 1,475, noise.
  - 100866719: first run 408 timeout; re-run gives 8 hits, all noise (Chen's repo absent). 145278430: first run 408 timeout; re-run gives 10 hits, all noise.
  - Controls: repo:littleBro/heilbronn-triangle-bounds with "tagged_small_residue_moment", "Heilbronn" and "theorem" each return 0 (not indexed). repo:canghaimeng/openai-math-improvement Heilbronn returns 3. repo:openai/math almost_n_minus_two_refuted returns 3.
- **GitHub repo search:** heilbronn (486); heilbronn created:>2026-09-30 (16); heilbronn in:readme created:>2026-09-30 (75); heilbronn pushed:>2026-10-06 (23); "openai math 191" (0); openai-math in:name (119, two pages); "erdos 507" (1, vibemathing, unrelated); heilbronn-triangle (12).
- **GitHub issue search:**
  - repo:teorth/erdosproblems: 507 (0), heilbronn (0), triangle (14), 477 (3, control).
  - repo:google-deepmind/formal-conjectures: heilbronn (2, Jan 2026), 507 (14), green_77 (0), openai (479), 507 created:>2026-10-05 (0), triangle created:>2026-10-05 (26, none relevant), "Green 77" created:>2026-10-05 (0).
- **arXiv API:** all:heilbronn (125); abs:heilbronn AND abs:triangle (19); au:Blinov (352, none relevant); au:Chen_Qiuyu (24; Euler 2610.19864); ti:"small triangles" (2); abs:"smallest triangle" AND abs:points (4); id_list=2610.19864.
  - Two later Waring-rank queries ("Waring rank of the determinant") returned empty feeds, probably rate-limited. Not evidence.
- **HN Algolia** (since 2025-10-05): heilbronn (21; the "Heilbronn Problem" small-n site plus city noise); "heilbronn triangle" (2); blinov (5, noise); "openai heilbronn" (0); 50893237 (1, noise); control "openai math" (1,604). Item 50002650 read in full (575 nodes, no Heilbronn).
- **StackExchange:** mathoverflow and math.SE, "heilbronn", sorted by date: nothing on the OpenAI result, Blinov or Chen.
- **Reddit:** search.json for "heilbronn" and "heilbronn triangle" returned **403 from both exe.dev and Hetzner. Not checked.**
- **Mathstodon:** v2 search for "heilbronn" returned empty (unauthenticated full-text search is not supported; not evidence). The #heilbronn tag timeline had 40 posts from 19 Sep to 20 Oct, all about the city.
- **Tao's blog:** ?s=heilbronn (Deuring–Heilbronn only); ?s=openai (Oct 2026 posts, none on Heilbronn).
- **Wikipedia:** Heilbronn triangle problem (raw text and last 15 revisions); Salem–Spencer set (raw text).
- **WebSearch:**
  1. "Blinov Heilbronn triangle lower bound exponent"
  2. "Heilbronn" OpenAI "power improvement" … verified OR refuted OR error
  3. Euler Qiuyu Chen Heilbronn "100866719"
  4. "heilbronn-triangle-bounds" OR "50,893,237" OR "50893237" Heilbronn
  5. Heilbronn OpenAI n^(-2+eta) … comment mathematician
  6. bigospeedrun Heilbronn Blinov Chen Euler claimed
  7. leanprover zulip Heilbronn OpenAI formalization
  8. Gasarch Glenn Kruskal "Finding large 3-free sets" …
  9. large 3-AP-free sets … r_3(N) N=10^5 record table

  None found any check of either claim. Hits I followed up: Kingy blog (an index only); arXiv 2608.14673 (predates the release, no Heilbronn).
- **3-AP literature:** OEIS A003002, A065825 and the b003002 b-file; Wróblewski's index.htm, nrootn.htm, methods.htm, DATABASE.TXT, BEST.TXT, BESTMOD.TXT, log30k.txt, log50k.txt; GGK survey II (arXiv 2501.01634); Ergezer 2606.04016 (upper-bound searches at N ≤ 211, not used); Erdős–Turán 1936; Moy–Rolnick 1502.06013 abs page.

## What I did NOT check
- **Places I could not read:** BOS Discord (needs joining); X/Twitter (bot wall), including Blinov's @ivanBcde; Reddit (403); Lean Zulip archive (web search only); Mathstodon full-text search (needs auth); Chinese-language forums (Zhihu, WeChat group in Euler's README).
- **Chen's embedded ZIP supplement:** not opened.
- **Whether the 137,692 set can replace Blinov's ternary positions:** I did not check this inside his tag/fresh-digit argument (F9). That question is for the P/G seats.
- **Better 3-AP-free sets:** I did not search for any beyond Wróblewski's tables, and did not look for a set whose five smallest elements are small.
- **Other Waring decompositions of det3:** I did not check whether any later paper gives one with fewer than 18 terms, which would shrink T = 9·18² (the arXiv query failed).
- **Mirror and audit repos:** I did not open every one in full. The scan read root READMEs plus files whose path matched heilbronn, 191, triangle, blinov or euler.
- **Code search:** the two numeric queries that first timed out were re-run (noise only); their coverage limits are noted in F5.
