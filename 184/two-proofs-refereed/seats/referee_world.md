# Referee seat: WORLD, PRIORITY, COMPARISON — Erdős #184

Seat: world / priority / comparison. Written 2026-10-20 ~03:30Z. Hostile brief: /tmp/oaimath/181/seats/REFEREE_BRIEF.md.
Raw evidence I fetched for this seat is under /tmp/oaimath/181/world/ (Wayback captures, Kim PDFs, boonsuan files, teorth yaml, Palomar queries).

## Verdict header

- **Priority (public record): HOLDS AS READ, with one major correction to the brief's framing.** Coffey went public first (1 Oct 2026). OpenAI's public release (6 Oct) came about 5¾ days later. **But there are THREE claimed proofs, not two.** Jaehoon Kim (KAIST) submitted *A proof of the Erdős–Gallai cycle decomposition conjecture*, arXiv:2610.07840, on 6 Oct 2026 at 06:42:42 UTC. That is about 15 h before OpenAI's repo existed and 5¼ days after Coffey. Kim's proof takes a different, short route, and the author states that he checked it himself. The brief doesn't mention it.
- **Comparison: COULD NOT CHECK correctness (other seats' scope).** The structural comparison is below. OpenAI and Coffey share the quotient-induction-and-lift skeleton on top of Bucić–Montgomery (BM) expanders. They differ in the scale and round schedule, in what is identified, in the accounting (≈n−S/3 with φ(n) versus ≤n/4 with a ×2 lift), and in the constants. Kim shares neither skeleton.
- **Lower-bound check: HOLDS AS READ.** OpenAI's "(3/2−o(1))n from complete bipartite examples, see BM §6" is what BM §6 says. erdosproblems' K_{3,n−3} ⇒ (1+c)n is the k=1 case of the same construction, c = 1/3.
- **Human verification anywhere: none of the three proofs has an independent human check on record.** The only human verification claim is Kim's own statement about his own paper.

---

## 1. Timeline

All times UTC unless marked. "Server" means set by GitHub, arXiv or Wayback. "Author" means a self-asserted date (commit author date, a \date line, a PDF CreationDate).

| # | When (UTC) | Event | Kind | Source |
|---|---|---|---|---|
| 0 | 2022-11-14 / 2023-11-14 | BM arXiv:2211.07689 v1 / v2 ("Final version, accepted"); Adv. Math. 437 (2024) 109434 | server | https://arxiv.org/abs/2211.07689 |
| 1 | 2026-03-16 06:38Z | FC `ErdosProblems/184.lean` added by Daniel Chin, `research open` ("Assisted by Gemini/Antigravity") | server | FC commit cba707c6db, https://github.com/google-deepmind/formal-conjectures/commit/cba707c6db |
| 2 | 2026-04-01 | erdosproblems.com/184 "last edited 01 April 2026" (state seen 7 Oct) | site | Wayback capture 20261007155228 of /forum/thread/184/proof-claims |
| 3 | 2026-09-24 | OpenAI preprint's own date "September 24, 2026" (`\date` in main.tex; directory name). **Self-asserted. The repo has one squashed "Initial commit" by "Anonymous", so no history backs it.** | author | openai/math preprints/A-linear-cycle-and-edge-decomposition-of-every-graph-September-24-2026/build/main.tex:42 |
| 4 | 2026-09-24 19:42:19Z | FC commit 2424bb48 (an unrelated "Mark five problems solved"). Coffey pins his challenge statement here, so his Lean target was fixed after this moment | server | `gh api repos/google-deepmind/formal-conjectures/commits/2424bb48…` |
| 5 | 2026-09-25 / 26 | Coffey's own dated record: proofs/manuscript/preamble.tex `\date{25 September 2026}`; PLAN_FORMALIZATION.md "Decisions … (2026-09-25)"; manuscript v6.1 `\date{Version 6.1, 26 September 2026}`; TRUST.md "version of 2026-09-25 was rejected by two trust audits". Private development repo steelwheel01/Erdos-Proof returns 404 | author | coffey/repo files cited |
| 6 | 2026-09-30 | Coffey's ERRATA/CORRESPONDENCE cite "release run 36767721300, 2026-09-30", which is in the private repo and cannot be checked | author | proofs/manuscript/ERRATA_v6.1.md:3; CORRESPONDENCE.md:3 |
| 7 | 2026-09-30 12:15Z | FC: `erdos_184.variants.covering` set true (Pyber 1985). Unrelated to the main statement | server | FC commit 473f47c113 (PR #6745) |
| 8 | **2026-10-01 00:12:30Z** | **github.com/steelwheel01/erdos-gallai-lean created public** (PublicEvent at creation). Account created 2026-01-27, 1 public repo, no name or affiliation on the profile | server | `gh api repos/steelwheel01/erdos-gallai-lean` (created_at), repo events API (PublicEvent) |
| 9 | 2026-10-01 00:15:28Z | Commit a11bb45 "Initial public snapshot of the Lean formalization (from steelwheel01/Erdos-Proof bb4d878…)"; tag `release-2026-10-01` → a11bb45; branch push 00:18:44Z | author+server | commits API; git/refs/tags API; events API |
| 10 | 2026-10-01 00:19:40Z → 02:25:32Z | Actions run **36795612102 `formal-release`, conclusion success**: jobs comparator (00:19:43–00:55:49), build, verify (leanchecker --fresh 01:51:49–02:25:08). The two `formal-ci` runs on a11bb45 FAILED at the "Gate red-team (fixtures N1–N3)" step, before any Lean ran. The fixture placeholder was added in 570205a, and later formal-ci runs (570205a, 660ae11, weekly schedule to 2026-10-19) all succeed | server | https://github.com/steelwheel01/erdos-gallai-lean/actions/runs/36795612102 ; runs list API |
| 11 | 2026-10-01 02:42:23Z | Commit 570205a "Record public release run 36795612102 …" | author | commits API |
| 12 | 2026-10-01 03:20:49Z | Coffey PDF CreationDate (152 pp, letter, pdfTeX); paper `\date{1 October 2026}` | author | `pdfinfo paper/erdos-gallai-proof.pdf`; paper/src/ms.tex:235 |
| 13 | 2026-10-01 03:21:06Z (pushed 03:22:30Z) | Commit 660ae11 adds paper PDF + LaTeX, CITATION.cff (`date-released: "2026-10-01"`, `commit: a11bb45…`, affiliation "Yale University", which I could not verify) | author / server push | commits API; events API PushEvent 03:22:30Z; CITATION.cff |
| 14 | **2026-10-01 03:29:21 (site clock)** | erdosproblems.com proof claim #379 "by Ryan Coffey (using Claude Opus 5.5)", posted by user American-Pharaoh. **Site timezone: not stated. I infer UTC** from two anchors. This claim comes 7 min after the PDF push at 03:22:30Z. ho boon suan's comment "16:05 on 01 Oct" comes 4 min after his repo's commit 93f11f0 at 16:01:22Z. Under UK time (BST = UTC+1), both posts would link files that did not yet exist | site (inferred UTC) | live/claims184.txt; boonsuan commits API |
| 15 | 2026-10-01 11:02 (site) | StijnC on claim: "150+ pages … Took responsibility; read&understood all yourself?" | site | live/c379.html |
| 16 | 2026-10-01 14:13:29Z → 16:01Z | github.com/boonsuan/cycles created; commits 154b4a6 (15:42Z) "Rewrite … as a readable expository paper", 060dbc6, 93f11f0 (16:01Z) | server/author | commits API |
| 17 | 2026-10-01 16:05 (site) | ho boon suan comment: "I asked GPT-6 Pro and Opus 5.5 to simplify … fully AI generated … no human has read and understood it yet" | site | live/c379.html |
| 18 | 2026-10-02 09:10–09:52Z | boonsuan restructures (5 commits). Final PDF CreationDate 2026-10-02 09:51:38Z, 35 pp | author | commits API; pdfinfo |
| 19 | 2026-10-03 11:57Z (merged 10-08 10:07Z) | FC PR #6819 (anatoliiohorodnyk) links a Lean proof of `erdos_184.variants.lower_bound` (K_{3,n−3}, c = 1/4, n ≥ 48). Not the main statement | server | FC commit 99111aa0bc |
| 20 | 2026-10-06 ~12:5xZ (HN 12:53:58Z) | **erdosproblems.com policy change** (blog:9; crossposted on Tao's blog dated 6 Oct). It **freezes new problem comments AND proof claims**, stops displaying statuses, and adopts "no credit/ownership language to describe future solutions". It says it will link Lean formalisations "if verified on Palomar" | site/blog | https://terrytao.wordpress.com/2026/10/06/changes-to-the-erdos-problems-web-site/ ; HN item 49977689 |
| 21 | **2026-10-06 06:42:42Z** | **Kim, arXiv:2610.07840v1 submitted** (32 pp, 42 KB), "Department of Mathematical Sciences, KAIST". "Use of AI tools: The author made extensive use of ChatGPT (OpenAI) and Claude (Anthropic) … The author has verified all results" | server | https://arxiv.org/abs/2610.07840 (submission history) |
| 22 | **2026-10-06 21:47:02Z** (initial commit authored 21:58:50Z) | **github.com/openai/math created; adc7f12 "Initial commit" (author "Anonymous")**. 719 manuscripts / 372 families. Family 181 = this paper (32 pp). Creation is not necessarily the moment it went public. The first HN post ("Read the 722 new OpenAI math papers") is at 23:15:35Z, an upper bound on public availability | server | `gh api repos/openai/math` created_at; local `git log` adc7f12; HN item 49985531 |
| 23 | 2026-10-07 ~00:00Z (20:00 ET Oct 6) | Kim's v1 appears in the arXiv listing "new listings for Wednesday, 7 October 2026". It is absent from the Oct 8 and Oct 9 listings. So Kim became public about 2–2.5 h after OpenAI's repo. His v2 confirms the order: "After the first version … was submitted to arXiv, and before it appeared, OpenAI announced an independent proof" | server | Wayback 20261007022423 of arxiv.org/list/math/new (contains 2610.07840) |
| 24 | 2026-10-07 05:03Z (22:03:50 −07:00 on 10-07) | OpenAI commit 3014888 "Update manuscripts and Lean formalizations". **It did not touch #184.** `git show --name-only 3014888 \| grep -i 'CycleDecomposition\|A-linear'` → none. The "cycle" hits are two unrelated Kähler-MMP `06-cycles.tex` files. Trees at adc7f12 and 1581d4c are identical for lean/OAI/Combinatorics/CycleDecomposition (tree 53e54cb9), the challenge file (blob aebc8e97) and preprint main.tex/main.pdf | author | local repo /tmp/oaimath/604/lean-build/repo |
| 25 | 2026-10-07 10:16Z → merged 10-11 07:51:35Z | **FC PR #6898 (mo271) marks `erdos_184` `research solved`**, approved by Paul-Lez 10-10 and reviewed by anxkhn. It gives `formal_proof using lean4 at ".../openai/math/blob/adc7f124.../CycleDecomposition/Main.lean#L207"` and a docstring "This was proved by an internal OpenAI model in September 2026 [OAI26a]" | server | FC commit 3dfd999dfe |
| 26 | 2026-10-07 15:52Z | erdosproblems /184 still "last edited 01 April 2026", 1 proof claim (Coffey), no formal-proof sentence | site | Wayback 20261007155228 |
| 27 | 2026-10-08 (blog dated) | Bloom, "Erdős problems in the OpenAI proofs": lists [184] ("This PDF claims to prove … This proof has been formalised. The PDF is 32 pages long"). Disclaimers: "I have not yet looked at in any serious way any of the proofs … nor … checked … that the formalisation compiles or that the statement … accurately captures the problem"; "There have been some accusations of plagiarism, and some of the proofs below have appeared online in some form before the 6th October release" | site/blog | Wayback 20261019093239 of /forum/thread/blog:10 |
| 28 | 2026-10-08 22:41 (site) | Comment by efiebig on blog:10: "for problem 184 … at least two claimed solutions before OpenAI's announcement: the first … on this same website on October 1st by Ryan Coffey … The second one appeared on arxiv almost at the same time of the announcement, by Jaehoon Kim [arXiv 2610.07840]" (1 "needs update" reaction) | site | same capture |
| 29 | 2026-10-09 04:08:00Z | Kim v2 (22 pp, 32 KB). Simplified: heavy cycles defined by degrees; a deterministic routing lemma replaces random colouring. Adds a "Note added" describing OpenAI's proof as independent with a different strategy, and cites it as [18]. **Neither Kim version cites Coffey** | server | arXiv abs; kim_v2.txt §7 |
| 30 | 2026-10-14 | plasma-ai/erdos (erdosproblems.ai, an AI-run record) records 3 claims for E0184: OpenAI "accepted" (formalized only; dated by them **2026-09-24**, i.e. by the preprint's self-date), Coffey "claimed", Kim "claimed". It states: "No outside reviewer is recorded." | server | https://github.com/plasma-ai/erdos/pull/46 ; https://erdosproblems.ai/184 |
| 31 | **2026-10-16** | erdosproblems /184 edited. Adds "A formal proof of the main conjecture, that O(n) edge-disjoint cycles and edges suffice, is available here", where **"here" = github.com/openai/math/blob/main/lean/ComparatorChallenges/CycleDecomposition.lean**. That is the comparator **challenge** file, which ends `theorem erdos_gallai : MainStatement := by sorry`; it is not the proof and not a Palomar entry. The BM sentence is reworded ("Bucić and Montgomery [BM22] proved…"). No mention of Coffey or Kim in the remarks; credit-neutral, per the 6 Oct policy | site | diff of Wayback 20261007 vs live/claims184.txt (computed) |
| 32 | 2026-10-19 21:27:17Z | teorth/erdosproblems `data/problems.yaml` (latest commit 49e0238b7e): 184 = `status: open` (last_update 2025-08-31), `formal_status: unformalized`, `formalized: yes` (2026-03-16). **Stale.** Our erdosproblemaday tracker (HEAD data from 2026-10-10/11) consequently shows #184 "open", with FC category "research open" | server | raw.githubusercontent.com/teorth/erdosproblems/main/data/problems.yaml ; ~/ErdosProblemADay/src/{tracker,statements}_data.js at HEAD |
| 33 | 2026-10-20 | Palomar registry (palomar-registry.org, the verifier Bloom names): **no #184 entry** for either repo (`/repositories/steelwheel01/erdos-gallai-lean.json` and `/openai/math.json` → 404; text searches "Erdos Gallai", "cycle decomposition", "erdos_184", "CycleDecomposition", "Erdos 184", "Coffey" → no #184 hit) | server | https://data.palomar-registry.org/api/v1/results |

**Who was publicly first, and by how much**
- Coffey's Lean was public at 2026-10-01 00:12:30Z and his paper at 03:22:30Z.
- Kim's arXiv submission was 5 d 6 h 30 m after Coffey's Lean went public. Kim was publicly listed at about 00:00Z on 7 Oct.
- OpenAI's repo was created at 2026-10-06 21:47:02Z (public by 23:15Z at the latest). That is **5 d 21 h 34 m after Coffey's Lean** and 5 d 18 h after Coffey's paper.
- So the public order is Coffey (1 Oct) → OpenAI (6 Oct, evening UTC) → Kim's listing (7 Oct, about 2 h later).
- By submission/internal timestamps the order is OpenAI's self-date 24 Sep → Coffey's self-dated record 25–30 Sep → Coffey public 1 Oct → Kim submitted 6 Oct 06:42Z → OpenAI public 6 Oct 21:47Z.
- **OpenAI's preprint carries an internal date (Sept 24) that precedes Coffey's public release (Oct 1). OpenAI's public release (Oct 6) follows it.** Neither the 24 Sep date nor Coffey's 25–30 Sep dates can be checked against any third-party timestamp.

## 2. Credit lines as they stand

- **Formal Conjectures** (main, 184.lean): `@[category research solved, AMS 5, formal_proof using lean4 at "…openai/math/blob/adc7f124…/lean/OAI/Combinatorics/CycleDecomposition/Main.lean#L207"]`, docstring "This was proved by an internal OpenAI model in September 2026 [OAI26a]; see the linked Lean proof." (PR #6898, merged 2026-10-11).
  - Searching FC issues and PRs for "Coffey" and "steelwheel01" returns 0 hits; the repo name surfaces nothing relevant. Coffey appears nowhere in FC.
  - **World-level fidelity point (flag to the Lean seat).** FC links a proof of `OAI.ErdosGallai.MainStatement`: `Fin n`, `Set (Sym2 (Fin n))` parts, `Walk.IsCycle` edge sets, `k ≤ C·n`. That is **not** FC's own `erdos_184`: arbitrary `Fintype V`, `Finset G.Subgraph`, `IsCycleOrEdge H.coe`, `f =O[atTop] n`.
  - PR #6898's "Reviewer notes" list the statements whose link "differ[s] … by a routine transport that is not in the linked proof" (Borsuk, Green 42, Erdős 371, 952, 1150, circulant Hadamard). **#184 is not on that list**, although the same kind of transport is needed.
  - Coffey's repo, by contrast, claims a comparator proof of FC's `erdos_184` with the statement byte-identical (FC pin 2424bb48). FC adopted neither it nor a note about it.
- **erdosproblems.com**: credit-neutral by policy since 6 Oct. The only remark is the 16 Oct sentence linking OpenAI's challenge file. The proof-claims tab holds only Coffey's claim (#379) **because claims were frozen on 6 Oct**, before OpenAI's and Kim's proofs went public. "One claim" says nothing about who else claimed.
- **teorth DB**: open / unformalized (stale).
- **OpenAI preprint**: cites BM, CFS, EGP, Lovász, Krivelevich, BKS, Pyber, KKS, GGKO, AH2000 and AABC2025. **It does not cite Coffey or Kim.** Its outline credits "the expansion, hypergraph matching and path-closing methods of Bucić and Montgomery … with earlier reservoir and sparse-cut methods of Conlon, Fox and Sudakov".
- **Kim v2** cites OpenAI as "independent"; neither version cites Coffey.
- **boonsuan exposition** cites Coffey as the source of the thin-cut rule, lending/anchors, cherries and quotient ideas; BM for the rounds.

## 3. Human responses found

| Who | What | Where |
|---|---|---|
| Thomas Bloom (site owner) | Lists the OpenAI #184 claim and says explicitly that he has neither read the proofs nor checked the formalisation or statement. Says AI-release papers are "at a glance, very poorly written … I expect that the vast majority of them are (a) correct yet (b) capable of being substantially simplified". Notes "accusations of plagiarism" generally, not for #184 | blog:10 (8 Oct) |
| efiebig | The Coffey / Kim priority comment quoted in timeline row 28 | blog:10 comment, 22:41 on 8 Oct |
| StijnC | Asks Coffey whether he "read&understood all yourself" | claim #379 comments, 1 Oct |
| ho boon suan (boonsuan) | Posted an AI-generated (GPT-6 Pro + Opus 5.5) exposition of **Coffey's** proof. The title page says "Claude Opus 5.5 — An AI-generated exposition of the proof claimed by Ryan Coffey", and the README says "no human has read or understood this proof". It is **not a third derivation**: it reorganises Coffey's argument (one kind of piece, a single clearing lemma, greedy cherry grouping, a simplified quotient, an extended BM Theorem-16 linking lemma) and credits Coffey for the key ideas. The earlier draft archive/astra-draft.tex ("A shorter route…", "Working reconstruction of the proof claim by Ryan Coffey", "a new mathematical draft, checked by static reasoning but not formally verified") is kept in the repo | github.com/boonsuan/cycles, branch claude/loving-allen-lml6o8 (35 pp, PDF 2 Oct 09:51Z) |
| Jaehoon Kim | Author of the third proof. Self-verification statement: "The author has verified all results and takes full responsibility" | arXiv:2610.07840 |
| Bucić, Montgomery | **No public response found.** WebSearch (extended) and HN Algolia searches turned up nothing. That is a coverage statement, not proof that none exists | — |
| HN / press | No HN thread on #184 specifically. Release-wide threads exist: "Association for Human Mathematics's Statement …" (49999159), The Verge "'Pure insanity'…" (50041162), SciAm on Navier–Stokes (50144760), Gizmodo (50117849), "Erdosproblems.com Succumbs to the AI Onslaught" (49977689). My grep of those threads' comment text found no 184 / Gallai / Coffey / Kim mentions. OfficeChai (9 Oct) lists 184 among the 23 problems | HN Algolia API; officechai.com |
| Mathstodon / X | Nothing found by WebSearch. Coverage only | — |
| arXiv | arXiv search "cycle decomposition Erdős Gallai" (sorted by announcement), "decomposed into O(n) cycles and edges" and "Hajós conjecture cycle decomposition": only Kim's paper is new. **No arXiv posting by Coffey** (author search "Coffey, Ryan": no results), even though CORRESPONDENCE.md:12–13 calls manuscript v6.2 "the arXiv version". **OpenAI's preprint is not on arXiv either** | arxiv.org/search |

## 4. Comparison of the arguments (OpenAI A vs Coffey B, plus Kim K)

What I read: OpenAI main.tex (intro and "Outline of the proof"), induction.tex (Lemma prefix-choice, Proposition induction-bound and its closing cost estimate), folding.tex opening (Lemma pair-folding), the routing/residue/splitting lemma list. Coffey s1.tex "Overview: the architecture, and where the log* disappears" and s7.tex §§ intro, round-split pools, "The quotient is simple, and every decomposition lifts" (Lemmas MULT, Simple, JV-L). Kim v2 §1.1 and §7.

**Shared between A and B (mechanisms, not provenance):**
1. Both are built on BM's toolkit: robust sublinear expanders, long cycles in expanders, Lovász's path decomposition, and a Haxell-type hypergraph matching theorem (A uses Aharoni–Haxell 2000; B uses Haxell 1995 in a q²-form).
2. Both turn the leftover edges that BM could not afford into **smaller simple quotient graphs**. Both decompose the quotients **by strong induction on the number of vertices**. Both **lift** each quotient cycle back to a cycle of G through edges **reserved inside earlier expanders**. A reserves routing paths in an "expanding piece" (lem:routing). B lends random colour classes of ancestors at least 2 rounds back, plus private junction edges (Lemma JV-L).
3. Both pay explicitly to make the quotient simple. A sets aside loops and all but one edge per parallel class via E_err (lem:pair-folding, |E_err| ≤ 2Σm_i). B's sub-layers are simple by rank construction; looped PAR objects are "paid" (Lemma Simple).
4. Both must make a per-scale or per-round cost summable, uniformly in the number of scales or rounds. That is exactly the BM §6 "bottleneck" which both, and Kim, name.

**Where A and B differ:**

| Aspect | OpenAI (A) | Coffey (B) |
|---|---|---|
| Scale schedule | Scales D_j = n^{0.95^j}: polynomial decay, so about log log n scales (CFS-like rather than BM-like). One layer i is **selected** by a prefix-charging lemma (Σ_{j≤i+K} S_j ≤ P_0 S_i, K = 200); only that layer's pieces are processed, after a fixed gap of K scales | BM's rounds kept: R = O(log* n), degree d → polylog d, tower-type parameters. **All rounds are processed.** Per-round costs are made to decay (tower-lacunary sums), charged once per vertex, or offset by a factor R−r that is outweighed |
| Expanders | Vertex-disjoint pieces of cut expansion D^{0.90} inside boxes of order ≤ D^{1.02}; total box order ×(1+O(1/log D)) | Hierarchy HB_tp built from Lemma 14^τ (τ-rules inside BM Lemma 14) + rule GC (guest-degree cap) ⇒ hub concentration ≤ ε_CONC(D_*)·n |
| What is identified | **Pairs of low-degree vertices** in batch∩piece intersections are paired at random and identified 2-to-1 (lem:pair-folding, lem:batch-resolution). A quotient edge = one original edge | Each **end** of a leftover J-item gets a **private junction edge** to a junction vertex in a sparse random pool (density M_l^{-2}) inside its ancestor's expander. Quotient vertices are junction copies [w] and hubs. A lifted single edge = "one or two single edges of G" |
| Other closing devices | Edges between a folding set and over-neighbours are first split into paths; reserved routes close the trimmed remnants | Standalone parts are chained into cycles via junction paths in lent colour classes ≥ 2 rounds back (TPV vortex, JS-LC); cherry systems; K-RED |
| Inductive hypothesis / accounting | f ≤ C·φ(n)·n with φ(n) = max{1/2, 1−1/√log n}. Quotient orders sum to ≤ n − S_i/3 + A_1 n/w; the text says explicitly "No choice made here requires the total quotient order … to be at most n; the potential gain pays for its possible excess". Quotients have order ≤ about D^{0.30}, and φ's gain ≈ δ/√w absorbs the O(n/log D) overlap | f(G) ≤ (D_*/2 + c_KRED + c_Fresh + 2 + ε_1)·n + **2**Σ_l f(Q_l), with Σ|Q_l| ≤ θ_Q·n ≤ n/4 ⇒ f ≤ C_0 n + 2c_EG·n/4 ≤ c_EG·n (layered induction HI″) |
| Constants | Auxiliary numerals explicit (θ = 0.95, K = 200, P_0 = 804, η = 1/(100P_0)). D_* "large enough" for a finite list of eventual inequalities, then C ≥ max{7A_2, 4T(D_*)}. Not computed numerically, but plainly elementary-sized | Galactic: D_* of tower type (log₂log₂D_* ≥ 2^8 per brief), c_EG = ⌈c_EG⌉ not computed |
| Size | 32 pp; Lean 34 files / 21,451 lines | 152 pp (+ v6.1 manuscript, errata with 31 items); Lean 601 files / about 93k lines |
| Lean target | OpenAI's own `MainStatement` (Fin n) | FC's `Erdos184.erdos_184`, verbatim, by comparator |

**Kim (K), for contrast. It shares neither skeleton:**
- No rounds and no quotient induction.
- A single greedy procedure charged against two budgets. The first is a degree potential Φ(G) = Σ_v f(d(v)) < n with f(d) = 1 − 1/√(d+1). Each removed "heavy" cycle drops Φ by ≥ 1. The second is the vertex count, since each vertex is deleted once.
- Theorem 1.3 ("light" graphs contain a near-closed induced subgraph of minimum degree ≥ |S|^{1/1000}) is elementary and uses no expanders.
- Theorem 1.4 extends CFS from linear to polynomial minimum degree using BM's expanders.
- 32 pp (v1), 22 pp (v2); no Lean.

**Neutral statement of the date/mechanism facts:**
- OpenAI's preprint's internal date (24 Sept) precedes Coffey's public release (1 Oct). OpenAI's public release (6 Oct) follows it by about 5¾ days.
- Coffey's own self-dated record begins 25 Sept, and his FC pin was created 24 Sept 19:42Z.
- The two A/B arguments share the quotient-induction-plus-expander-lifting idea on a BM base, and differ in essentially every implementation choice above.
- Kim's argument is mechanically distinct from both.
- I make no inference about copying in any direction. No third-party timestamp exists for anyone's pre-1-October work.

## 5. Lower-bound check (BM §6, arXiv:2211.07689v2, current version, 14 Nov 2023)

What BM §6 actually says (bm.txt l.1597–1615):
- "It is known that only (3/2+o(1))n cycles and edges are needed … with linear minimum degree (GGKO), and also that 3/2 is best possible here. This latter fact was observed by Erdős [17] in 1983 who remarked that there are graphs requiring (3/2−o(1))n cycles and edges, **likely referring to** the following generalisation of an example of Gallai."
- The construction: take K_{A,B} with |A| = 2k+1 and |B| = n−2k−1. Each B-vertex has odd degree and B is independent, so there are ≥ |B| single edges. Every cycle has length ≤ 2|A|. Hence there are at least |B| + (|A||B|−|B|)/(2|A|) = (3/2 − 1/(2|A|))|B| = (3/2 − 1/(4k+2) − o(1))n parts.

Checks:
- **The argument is correct.** The count s + (|A||B|−s)/(2|A|) increases in s, so it is minimised at s = |B|.
- **erdosproblems** "K_{3,n−3} ⇒ (1+c)n": the k=1 case gives ≥ (4/3)(n−3), so c = 1/3 − o(1). Consistent. The FC `variants.lower_bound` proof uses the weaker c = 1/4, n ≥ 48, which is fine for ∃c.
- **OpenAI** main.tex:85–87, "complete bipartite examples require (3/2−o(1))n parts; see [BM2024, §6] for this lower bound and its history": **accurate.** It needs k = k(n) → ∞ with k = o(n); BM's display, read with k fixed, gives 3/2 − 1/(4k+2). EXPOSITION-level nuance only.
- **Kim** states it as Erdős's observation without BM's "likely referring to" hedge ("Erdős [6] observed that (3/2−o(1))n …"; v2 "at least 3/2 by the example of Erdős [5]"). COSMETIC.

## 6. Flags for the other seats and for the cron

1. **[Most important] A third claimed proof exists:** Kim, arXiv:2610.07840 (v1 6 Oct 06:42:42Z, v2 9 Oct), by a KAIST combinatorialist, by a different short route, with the author's own verification statement and declared heavy ChatGPT/Claude use. Any write-up that says "two proofs" or "OpenAI and Coffey" is incomplete.
2. erdosproblems' single proof claim reflects the **6 Oct freeze on proof claims**, not the field of claimants.
3. erdosproblems' "formal proof … available here" links **OpenAI's comparator challenge file (a `sorry` statement)**, not a proof file or a Palomar entry. **Neither formalization is on Palomar**, the registry Bloom's policy names.
4. FC credits OpenAI with a `formal_proof` link to a theorem of a **different, non-identical statement** (routine transport, not in the linked proof, not listed in the PR's reviewer notes). Coffey's verbatim proof of FC's statement (public 5¾ days earlier) is mentioned nowhere in FC.
5. **Naming hazard:** OpenAI "family 181" = Erdős **#184**, while Erdős **#181** (hypercube Ramsey) is OpenAI family **171**. Our working dir /tmp/oaimath/181 is the family number.
6. **Our own surface is stale:** erdosproblemaday's tracker data at HEAD shows #184 `"s":"open"` (teorth status, last_update 2025-08-31) and FC `"c":"research open"` (statements from FC 4c40439d, 2026-10-10, the day before FC flipped to solved). **Housekeeping note:** while checking how the tracker reads teorth, `python3 scripts/gen_tracker.py --help` *ran the generator* (the script ignores `--help`) and rewrote src/tracker_data.js and src/statements_data.js. I restored both with `git checkout --`, and `git status` is back to only the two pre-existing untracked verification/112 files. Nothing in our repo is left modified by this seat.
7. No independent human verification of any of the three proofs is on record anywhere I could reach. The plasma-ai record "accepts" OpenAI on its own (AI corpus) build and audit and itself says "No outside reviewer is recorded".

## Sources

- erdosproblems.com (saved 2026-10-20): /tmp/oaimath/181/live/{p184,claims184,thread184}.txt, c379.html
- Wayback: https://web.archive.org/web/20261007155228/https://www.erdosproblems.com/forum/thread/184/proof-claims ; https://web.archive.org/web/20261019093239/https://www.erdosproblems.com/forum/thread/blog:10
- Bloom guest post (6 Oct): https://terrytao.wordpress.com/2026/10/06/changes-to-the-erdos-problems-web-site/
- Coffey: https://github.com/steelwheel01/erdos-gallai-lean ; https://github.com/steelwheel01/erdos-gallai-lean/actions/runs/36795612102 ; local clone /tmp/oaimath/181/coffey/repo (README, CITATION.cff, CORRESPONDENCE.md, ERRATA_v6.1.md, PLAN_FORMALIZATION.md, paper/src)
- OpenAI: https://github.com/openai/math (adc7f12, 3014888, 1581d4c); local /tmp/oaimath/604/lean-build/repo
- Kim: https://arxiv.org/abs/2610.07840 (v1, v2 PDFs in /tmp/oaimath/181/world/kim/); arXiv listing capture https://web.archive.org/web/20261007022423/https://arxiv.org/list/math/new
- BM: https://arxiv.org/abs/2211.07689 (v2), local /tmp/oaimath/181/refs/bm.txt §6
- Formal Conjectures: commits cba707c6db, 473f47c113, 99111aa0bc, 3dfd999dfe (PR #6898), 2424bb48; current https://raw.githubusercontent.com/google-deepmind/formal-conjectures/main/FormalConjectures/ErdosProblems/184.lean
- teorth: https://github.com/teorth/erdosproblems data/problems.yaml @ 49e0238b7e
- boonsuan: https://github.com/boonsuan/cycles/tree/claude/loving-allen-lml6o8
- plasma-ai / erdosproblems.ai: https://github.com/plasma-ai/erdos/pull/46 ; https://erdosproblems.ai/184
- Palomar: https://palomar-registry.org/ ; https://data.palomar-registry.org/api/v1/results
- HN (Algolia API): items 49977689, 49979215, 49985531, 49999159, 50041162, 50117849, 50144760
- OfficeChai (9 Oct): https://officechai.com/ai/openai-has-also-included-proofs-for-23-erdos-problems-in-its-latest-math-proof-drop/
