# World search on Li's disproof of Erdős #341 (Dickson greedy problem)

Compiled 2026-10-13 (UTC) by seat A. Read-only reconnaissance; nothing compiled or re-proved here. Raw fetches are in `/tmp/erdos2100/seats/A/raw/`.

Access notes:
- erdosproblems.com returns Cloudflare 403 to the datacenter IP. I read it through the home-IP Chrome on the old Mac (CDP, new tabs only, closed afterwards).
- Not retrievable, so unread: Guy UPINT (archive.org borrow-only), Finch 1992 Monthly (T&F Cloudflare challenge, not bypassed), Queneau 1972 (ScienceDirect challenge, not bypassed), OEIS (403 from datacenter).
- Not searchable from here: X/Twitter, Reddit, Lean Zulip, Telegram/Discord.

---------------------------------------------------------------------------------------------------

## TL;DR

1. **Nobody has disputed or found an error in Li's claim, anywhere I could look. Nobody authoritative has accepted it either.**
   - erdosproblems.com still shows #341 as open. It lists Li's proof claim with the standard "no guarantee of correctness" disclaimer, and the claim has 0 comments. Comments and proof claims are paused site-wide.
   - The teorth database still says `open` (last_update 2025-08-31).
   - Ben Green's list is a Jan-2026 PDF that predates the claim.
   - The only institutional uptake is google-deepmind/formal-conjectures (merged 2026-09-18, approved by `mo271`). It relies on an independent Lean rebuild by the PR author.
2. **Prior literature has no earlier proof or counterexample.** The nearest items are computational evidence only: Calkin–Finch 1996 Table 3 and Calkin–Finch–Flowers 2005. They all concern *sum-free-base* (Cameron) sets, and none was proved aperiodic.
3. **Dickson 1934 never states the periodicity question.** I read all four pages. Calkin–Erdős 1996 footnotes the same thing. The question is attributed to Dickson only via Erdős–Graham 1980 p.53 and Guy.
4. **Seed caveat for the referee.** Li's seed is *not* sum-free (12 internal relations x+y=z, e.g. 1+1=2, 1+2=3). #341 as posed (Erdős–Graham, erdosproblems, Green) allows arbitrary seeds, so this is legitimate for #341. The older Cameron/Calkin–Finch literature frames the question with sum-free bases, and Li's example does not obviously answer that narrower question. Calkin–Finch Conjecture 4.2 is the exact statement.
5. Provenance nits are listed in §1.8. None is a soundness defect.

---------------------------------------------------------------------------------------------------

## 1. Has anyone accepted, disputed, or found an error?

### 1.1 erdosproblems.com (read 2026-10-13 via home-IP Chrome)

Raw text is in `raw/mac/`.

- Problem page https://www.erdosproblems.com/341
  - Status: no "solved/disproved" marker.
  - Statement: "Let A={a_1<⋯<a_k} be a finite set of positive integers … least integer exceeding a_n which is not of the form a_i+a_j with i,j≤n. Is it true that the sequence of differences a_{m+1}−a_m is eventually periodic?"
  - Note: "An old problem of Dickson. Even a starting set as small as {1,4,9,16,25} requires thousands of terms before periodicity occurs." / "discussed under Problem 7 on Green's open problems list."
  - "This page was last edited 20 January 2026."
  - Tabs: Comments (1), Proof claims (1), Proof expositions (0).
- History page https://www.erdosproblems.com/history/341
  - Only two revisions: current, and 2025-10-20. The 2025-10-20 revision is the version without the Green's-list sentence, hence the `{P}` marker. Nothing since 2026-01-20.
- Forum thread https://www.erdosproblems.com/forum/thread/341
  - One comment, by **KentaKitamura, 13:15 on 08 Jul 2026**. It says that for {1,4,9,16,25} with i=j allowed, "I seem to get a period of length only 224 … a_{n+224}=a_n+1176 for n≥87." It cites a Colab link and discloses Codex 5.5 / ChatGPT 5.5 Pro.
  - This is about the page's side-remark, not about Li. It is the only comment ever posted, and nobody has replied.
  - Footer: "The ability to post new comments has been suspended."
- Proof-claims tab https://www.erdosproblems.com/forum/thread/341/proof-claims
  - "There is 1 proof claim (partial or full)". The claim is `proof-claim-200`: "claimed by Zhiheng Li (using GPT-5.6 Sol)", **Submitted 2026-08-09 15:32:18 by Z_Li**.
  - Summary quoted from the page: "We construct an explicit finite set of positive integers whose greedy pair-sum-avoiding extension has a non-eventually periodic sequence of consecutive gaps … nonperiodic scale-eight sumset controller embedded in three residue classes modulo 49, together with a finite modular shield … The exact recurrence verifies the least-admissible-next-term rule, with equal summands allowed."
  - Links: proof = `…/Erdos-341/blob/main/paper/Erdos341.pdf`; formalisation = `…/LeanProject/Erdos341.lean`.
  - Site disclaimer: "Appearing on this page is no guarantee of proof correctness, and does not mean that anyone associated with this site has examined any part of the proof."
  - Claim comments: https://www.erdosproblems.com/forum/proof-claims/200/comments returns "No comments yet. The ability to post new comments has been suspended."
- Z_Li profile https://www.erdosproblems.com/forum/user/Z_Li
  - No posts, no bio, exactly 1 proof claim (this one).
- Forum index https://www.erdosproblems.com/forum/
  - Banner: "The ability to post proof claims and comment on individual problems has been paused. Comments on general threads, blog posts, and the direct messaging system work as before."
  - So the absence of discussion on #341 is partly structural. I could not date the pause.
  - Grep of the forum index for "341" found only Z_Li's claim and KentaKitamura's comment.
- Problem 342 (Ulam) https://www.erdosproblems.com/342 and its thread
  - Last edited 30 Sep 2025; latest comment 23:54 on 16 Sep 2026 (Woett, about 1,2,3 vs 1,2,5 starts).
  - Nothing about Li or 341.
- Not found: any Bloom/Tao comment on #341. A Tao blog search for "erdős 341" (https://terrytao.wordpress.com/?s=erd%C5%91s+341, 2026-10-13) returned no results.

### 1.2 teorth/erdosproblems database and wiki

- https://github.com/teorth/erdosproblems/blob/main/data/problems.yaml, read at HEAD `0ac519b69b` (2026-10-13T17:12:52Z, a github-actions bot commit). Entry for #341:
  ```
  - number: "341"
    informal_status: state "open", last_update "2025-08-31"
    formal_status:   state "unformalized"
    status:          state "open", last_update "2025-08-31"
    formalized:      state "yes", last_update "2026-01-22"
  ```
  The `formalized` field only means the *statement* is in formal-conjectures; the update script only checks for the existence of .lean files.
- The AI-contributions wiki says "The wiki is no longer updated. The latest data is as of Jun 30, 2026." It has no 341 row (before the claim): https://raw.githubusercontent.com/wiki/teorth/erdosproblems/AI-contributions-to-Erd%C5%91s-problems.md
- GitHub issue/PR search in teorth/erdosproblems for "341" returns only unrelated issues #341 and #342.
- GitHub search for "Zhiheng", "LiAlreadyExists", "Li26", "erdos_341" and "Erdos341 not_erdos_341" finds only the two formal-conjectures items below.

### 1.3 google-deepmind/formal-conjectures (the only institutional uptake)

- Issue https://github.com/google-deepmind/formal-conjectures/issues/6069 opened 2026-09-18T13:36Z by `Konamiu` (liudongdong). Closed 19:43Z.
  - Says the Lean statement "(an ℕ-valued strictly increasing a satisfying the greedy rule from some index on, with n ↦ a(n+1)−a(n) not eventually periodic) implies the negation of our ℤ-valued IsLeast formulation".
- PR https://github.com/google-deepmind/formal-conjectures/pull/6070
  - Merged 2026-09-18 as commit https://github.com/google-deepmind/formal-conjectures/commit/a8d29337adec1b1c9057e0c94cae509a36b986ce
  - Reviewed and approved by **mo271** (Moritz Firsching) 2026-09-18T19:24:43Z: "Thanks, LGTM!" No other discussion.
  - PR body, "How checked": "Rebuilt plby's three files (`Erdos341/Shield.lean`, `Erdos341/Proof.lean`, `Erdos341.lean`, Mathlib-only imports) against this repo's Mathlib: `#print axioms Erdos341.not_erdos_341` → `[propext, Classical.choice, Quot.sound]`, no sorry/native_decide." It also gives a "bridge" theorem `erdos_341_false`, "verified locally, not part of this PR".
  - PR body, on status: "proof claim on erdosproblems.com is listed as under review, but the Lean proof is complete."
  - PR comment (Konamiu, 2026-09-18T18:02Z): erdosproblems.com and teorth's problems.yaml "still record this problem as `open` while the proof claim is under human review".
  - Net effect on `FormalConjectures/ErdosProblems/341.lean`: `answer(sorry)`→`answer(False)`, `research open`→`research solved`, added `formal_proof using lean4 at …plby/lean-proofs/blob/8822f7dd…/Erdos341.lean#L12`, added [Li26] reference. The theorem body is still `by sorry`; the linkage is by the external proof.
  - File history for 341.lean: #1778 (formalized, merged 2026-01-22, danielchin) → modulization commits → #6070 (2026-09-18).
- Earlier PR #2885 (2026-03-03, closed unmerged, an AI-generated "formally solved `erdos_341.variants.known_result`") is unrelated to Li.
- Issue #1546 "Green's Open Problems #7" is open. The Green 7.lean file covers only the Ulam positive-density part.

### 1.4 plby/lean-proofs (Boris Alexeev's collection)

- Commit https://github.com/plby/lean-proofs/commit/faeedb63f1c9d991c943baf17304e48daa111d19 "Add proof claim for Erdos341." (2026-08-26T03:43Z, Boris Alexeev, committer email `balexeev@openai.com`).
- It adds `src/latest/ErdosProblems/Erdos341.lean`, `…/Erdos341/Proof.lean` (847 lines), `…/Shield.lean` (651 lines), a Comparator challenge (`ComparatorChallenges/ErdosProblems/Erdos341.{lean,json}`, permitted axioms propext / Quot.sound / Classical.choice), and a `data/sources.yaml` entry.
- The `sources.yaml` entry credits Li (human) + GPT-5.6 Sol (AI) for both informal and formal parts. Version "4.33.0-rc1". Source repo pinned at Li's commit `c1d912189983…`.
- The pinned file at `8822f7dd…` states:
  ```lean
  theorem not_erdos_341 :
    ∃ a : ℕ → ℕ, StrictMono a ∧ (∀ n, 0 < a n) ∧
      (∃ k, ∀ n, k ≤ n → (¬ ∃ i ≤ n, ∃ j ≤ n, a i + a j = a (n+1)) ∧
          ∀ t, a n < t → t < a (n+1) → ∃ i ≤ n, ∃ j ≤ n, a i + a j = t) ∧
      ¬ ∃ N p, 0 < p ∧ ∀ n, N ≤ n → a (n+p+1) - a (n+p) = a (n+1) - a n
  ```
- My grep of `Proof.lean`, `Shield.lean` and `Erdos341.lean` for `sorry|admit|axiom|native_decide|unsafe|implemented_by|extern|opaque|ofReduceBool` found only `#print axioms` lines. The set_options are `maxRecDepth 10000` and `maxHeartbeats 2000000`.
- This is a grep, not a compile.
- Li's files are byte-identical to plby's except for the import line:
  - `LeanProject/Erdos341.lean` = plby `Erdos341/Proof.lean` (import path differs).
  - `Erdos341Shield.lean` = plby `Shield.lean` (identical).

### 1.5 Li's own repo, Zenodo, paper

- https://github.com/LiAlreadyExists/Erdos-341 was created 2026-08-09T11:56Z. It has 1 star, 0 forks, 0 issues, 0 PRs, and no license file. The account has 1 repo and was created 2025-01-12.
- 8 tags/releases, v1.0.0 (2026-08-10) → **v2.1.0 (2026-08-20T14:03Z)**. The cited Zenodo DOI 10.5281/zenodo.22030511 is **v2.0.1**, not the latest.
  - Zenodo record: https://zenodo.org/records/22030511 (cc-by-4.0, created 2026-08-20T13:58Z, 55 views).
  - Concept DOI 10.5281/zenodo.21880071.
  - Later version v2.1.0 = record 22030579 (14:03Z, "add lean").
  - Descriptions: v1.1.0 "Only Lean files included"; v1.3.0 "Adding generalized version"; v2.0.0 "add generalization section, add lean verification of section 5".
- Lean content has been **byte-identical since the first upload** (11:59Z on 2026-08-09): `Erdos341.lean` sha256 `75c56c1e…` (28,728 bytes), `Erdos341Shield.lean` sha256 `8f2f6ed7…` (23,028 bytes). I verified this across tags v2.0.1 and v2.1.0 and the early commits. The 08-12 "Pure Lean" commit only removed the paper. `Erdos341g.lean` (the 7p family) is identical at v2.0.1 and v2.1.0.
- The deleted BUILD_VERIFIED.md (first commit) recorded: "Lean v4.33.0-rc1, Mathlib 79d0395a…, `lake build` successful (8662 jobs), axioms [propext, Classical.choice, Quot.sound], no sorry/admit/axiom/native_decide".
- The paper (https://github.com/LiAlreadyExists/Erdos-341/blob/main/paper/Erdos341.pdf, tex at `paper/Erdos341.tex`) carries the "AI-use disclosure" ("developed with assistance from OpenAI's GPT-5.6 Sol. All arguments were checked and verified by the author") and "Formal verification" paragraphs.
  - Bibliography: Erdős–Graham 1980, Bloom's database ("accessed 11 August 2026"), Calkin–Finch 1996, Calkin–Erdős 1996.
  - It does **not** cite Dickson 1934, Cameron 1987, Queneau, Finch 1992, or Guy.
  - It says: "Related periodicity criteria are due to Calkin and Finch, while Calkin and Erdős proved that a natural class of aperiodic sum-free sets is incomplete."
  - The main theorem is stated for "a nonempty finite set A ⊆ ℕ" with `t > a_n, t ∉ A_n + A_n`, i.e. arbitrary seed, equal summands allowed.

### 1.6 arXiv, MathOverflow, other searches (nothing disputing, nothing supporting)

- arXiv API (export.arxiv.org, 2026-10-13), 0 hits for each of: `all:"Erdős Problem 341"`, `all:"Erdos Problem 341"`, `all:"Erdos 341"`, `all:Dickson AND greedy AND sum`, `au:"Zhiheng Li" AND all:Erdos`, `all:"sum-free" AND all:"eventually periodic" AND all:greedy`, `all:"GPT-5.6" AND all:Erdos`.
  - Positive control: `all:Erdos AND all:greedy` returned 13 results, so the API works.
  - **Li's paper is not on arXiv.**
- OpenAlex search "Erdős problem 341 Dickson greedy sum" (from 2026-01-01): 0 hits.
- Zenodo: only Li's own record.
- MathOverflow / Math.SE via Stack Exchange API: nothing on #341 or Dickson greedy sums.
  - Only relevant MO item: https://mathoverflow.net/questions/470827/on-s-additive-sequences (2024-05-08, 0 answers). It summarises Finch 1992 and Queneau's explicit periods for 0-additive bases, and says "Finch also remarks that from 'the sheer magnitude of' Queneau's computations, it can be conjectured that all 0-additive sequences are regular."
- Hacker News (Algolia): nothing on #341.
- Mathstodon public hashtag timelines (`#erdosproblems`, `#erdos`): shallow, nothing on 341.
- Other GitHub items mentioning 341:
  - **grandchallenge/MATH-PROGRAMME#1611** (https://github.com/grandchallenge/MATH-PROGRAMME/issues/1611), an automated source-audit task. Its result comment (fyremael, 2026-10-13T06:50Z) is built on stale pins (teorth commit 536408716, FC commit 85f863718). It does **not** mention Li's claim, the proof-claims tab, or the merged FC change, and concludes "The universal question remains open on the checked evidence." This is stale-snapshot noise, not a dispute.
  - **TheJustinSunPrize/awards PR #4260** ("JSP-000341: register Lean formalization (plby/lean-proofs)", 2026-09-23, dcdreamy-code), closed 2026-09-24 with the boilerplate "Submissions that provide only partial progress … do not meet these requirements."
    - The PR names no defect.
    - It is mis-mapped: that catalog's JSP-000341 is a *different* problem ("trajectories obtained by repeatedly adding an integer's divisor count"; `problems/catalog-0301-0400.md`), and I found no JSP entry for the Dickson problem.
    - So its closure is not a verdict on Li.
  - thisisanameforsure/open_proof_network_graph#54 (2026-09-14): "Admission failed at witness: the hypotheses need an integer sequence that is eventually the greedy sum-avoiding sequence. That is a real construction to write and check." Pre-dates plby's formalisation reaching their tool.
  - rjwalters/lean-genius: several AI-generated "erdos-341" audit/enrichment PRs from Jan–Jul 2026, before the claim.
- The Patrick-owned "Erdős Problem a Day" working report https://www.erdosproblemaday.com/report/341 (dated 2026-07-28, pre-Li) says the same as the site and has no knowledge of Li's claim.
  - Its content: a finite periodicity-certificate lemma; {1,4,9,16,25} has minimal period 1176 / 224 selected residues from onset 426 (so the page's "thousands of terms" remark is overstated, consistent with KentaKitamura's comment); all nonempty seeds in [12] except {1,4,8,10,11,12} certified periodic; and the observation that Calkin–Finch "normally starts with a sum-free base. The live problem … permits an arbitrary finite set".

### 1.7 Ben Green's list

- https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf: `Last-Modified: Fri, 30 Jan 2026 14:15:00 GMT`, PDF CreationDate 2026-01-30, 62 pp. **It predates Li's claim, so it cannot mention a resolution.**
- Problem 7 text (comment section): "A (somewhat) related class of sequence may be defined as follows. Start with some 'seed' set of values u_1<⋯<u_m. For n⩾m, define u_{n+1} to be the smallest integer greater than u_n not of the form u_i+u_j for i,j⩽n. This construction was considered by Dickson. A variant construction considered by Queneau is to define u_{n+1} to be the smallest integer greater than u_n and not of the form u_i+u_j with i<j⩽n. For both variants, the following question appears to be open: is u_{n+1}−u_n eventually periodic? For references and computations showing that periodicity (if present) can be very slow to appear, see [119, 164], and see also erdosproblems.com/341 and /342."
- [119] = Finch, "Are 0-additive sequences always regular?", Amer. Math. Monthly 99 (1992) 671–673. [164] = Guy, Unsolved Problems in Number Theory (2nd ed. 1994).
- Note: Green's text allows an arbitrary "seed" with no sum-free requirement, and both variants (i≤j and i<j) are posed.

### 1.8 Provenance nits (not soundness defects)

- The paper's Zenodo DOI is the v2.0.1 snapshot, not v2.1.0 (Lean files identical).
- BUILD_VERIFIED.md recorded sha256 `e95e8a49…` for `LeanProject/Erdos341.lean`. The committed file hashes to `75c56c1e…` and has been unchanged since the first commit. The Shield hash matches (`8f2f6ed7…`). I could not reproduce the recorded hash with simple variants (CRLF, trailing newline, import-path swap). The build record is self-reported, and independent rebuilds exist (FC PR author, Alexeev's repo), so I note it only for completeness.
- The Lean statement and the faithful-formalisation bridge to formal-conjectures' ℤ/IsLeast form were checked only by the FC PR author (`Konamiu`), locally.

---------------------------------------------------------------------------------------------------

## 2. Prior literature

### 2.1 Dickson 1934: what he actually wrote

- L. E. Dickson, "The converse of Waring's problem", Bull. AMS 40 (1934) 711–714, DOI 10.1090/S0002-9904-1934-05951-2. PDF fetched from https://www.ams.org/journals/bull/1934-40-10/S0002-9904-1934-05951-2/S0002-9904-1934-05951-2.pdf (saved at `raw/lit/dickson1934.pdf`, text layer in `dickson1934.txt`). Read all 4 pages.
- It is about **universal k-sets** (additive bases): "In the converse problem, k is given and we seek all k-sets." Sets include **0**, and integers are ≥ 0.
- The greedy rule appears as construction I, verbatim: "I. As the nth element of the set choose the least integer which is not a sum of any two of the first n − 1 elements. The set is composed of 0 and all positive odd integers."
- **Equal summands are allowed** (forced by the outcome: if 1+1 were excluded the set would not be 0 + odds). There is no sum-free requirement on the start, which includes 0.
- Constructions II–V:
  - II: "The set with 0, 1, 2 and later elements chosen as in I is composed of 0, 1, 2+3x."
  - III–IV: variants "subtract 1 from the least".
  - V is a "bizarre 2-set" with blocks, of which Dickson says "there is apparently no simple independent definition of this 2-set… [differences] a highly irregular sequence."
- **Dickson never asks whether the gap sequence is eventually periodic.** The 4 pages contain no such question. This matches the footnote in Calkin–Erdős 1996 (see §2.3): "It seems that the problem as stated by Guy doesn't appear in the reference cited."
- van Berkel–Bosma 2026-09-15 (§2.6) agree: "Apparently (cf. Guy, Problem E32) Dickson [7] was the first to coin questions about sumfree sequences; however, his main focus was on constructing sequences with the property that every positive integer is the sum of (at most) t elements in the sequence (allowing repetitions)."

### 2.2 Erdős–Graham 1980, p.53 (checked against the scanned page image `/tmp/erdos2100/live/pg-049.png`)

Exact text: "The following old problem of Dickson [Dic (34)] is still wide open. Given a set of integers A_k = {a_1 < … < a_k}, extend it to the infinite sequence A = {a_1 < … < a_k < …} by defining a_{n+1} for n ⩾ k to be the least integer exceeding a_n which is **not** of the form a_i + a_j, **i, j ⩽ n**. Is it true that the sequence of differences a_{m+1} − a_m is eventually periodic? Even a starting set as small as {1, 4, 9, 16, 25} requires thousands of terms before periodicity eventually occurs."
- It says "a set of integers", not necessarily positive. i,j ≤ n (equal allowed). There is no sum-free requirement. It follows with the Ulam problem (i≠j, unique representation).

### 2.3 Guy, Cameron, Calkin–Finch, Calkin–Erdős (the 1987–1996 line)

- **Guy**, Unsolved Problems in Number Theory ("Sequences of Integers" chapter): Calkin–Finch cite "Dickson's problem [Dickson 1934; Guy 1980, Problem E32]"; Calkin–Erdős cite "Problem C9". I could not read Guy (borrow-only).
- **Cameron 1987**, "Portrait of a typical sum-free set" (Surveys in Combinatorics 1987, LMS Lecture Notes 123, pp. 13–42): the bijection between binary decision sequences σ and sum-free sets θ(σ). Not read; described via Calkin–Finch.
- **Calkin & Finch, "Conditions on Periodicity for Sum-Free Sets", Experiment. Math. 5 (1996) no. 2, 131–137** (copy at https://emis.de/ft/51959, saved as `raw/lit/calkin_finch.pdf`).
  - Setting: S sum-free (no x+y=z, x=y allowed), S = θ(σ). "S is ultimately complete if, for all sufficiently large n, either n∈S or there exist x,y∈S such that x+y=n." Prop 3.1: S ultimately complete ⇔ σ has finitely many zeros.
  - **Conjecture 4.2** (Cameron, personal communication): "A binary string σ has only finitely many zeros iff θ(σ) is ultimately periodic and ultimately complete (… this is the same as saying that any ultimately complete sum-free set is ultimately periodic)." The text says: "Cameron [1987] has found evidence that 4.2 may also be false."
  - "Cameron [1987] found the first potentially aperiodic complete sum-free set … The existence of such a set suggests that Dickson's problem [Dickson 1934; Guy 1980, Problem E32] may have a negative solution. Queneau [1972] and Finch [1992] have studied a variation of this problem involving what are known as 0-additive sequences."
  - Section 5 computations: all 76,080 sum-free bases with max ≤ 27 (and all bases of ≤3 elements up to 35) tested to 10^7.
  - **Table 3, "Apparently aperiodic complete sum-free sets listed by base (checked up to 10^7)"**: {8,18,30}, {8,27,32}, {9,16,29}, {9,26,32}, {9,28,35}, {10,18,34}, {11,26,35}, {12,21,35}, {9,21,24,27}, {11,16,17,26}, {1,3,8,20,26}, {2,15,16,23,27}, {5,6,14,23,27}, {3,12,17,19,21,27}, {10,13,15,16,17,24}, {10,15,16,18,22,27}, {12,15,17,18,19,25}, {14,16,17,18,21,27}, {6,14,17,18,22,25,27}.
  - Table 4 ("tentatively periodic") includes Cameron's example {3,4,13,18,24} with estimated period ~3.27 million.
  - They stress "periodicity need not arrive quickly" (e.g. base {10,14,15,17,22}: minimal period 2,875,722 after ~584,000 terms).
  - **No aperiodicity is proved**: "no method is known that will show that a sum-free set is not ultimately periodic from a consideration of only finitely many elements."
  - All of these are **sum-free bases** (Cameron's setting).
- **Calkin & Erdős, "On a class of aperiodic sum-free sets", Math. Proc. Camb. Phil. Soc. 120 (1996) 1–5** (https://www.math.clemson.edu/~calkin/Papers/calkin_erdos.pdf; fetched with `curl -k`, expired or mismatched cert on the Clemson host).
  - Quote: "An old question (ascribed to Dickson by Guy [6] and rediscovered in a more general setting by Cameron [4]) asks whether a sum-free set constructed in a greedy fashion from a finite initial set will be ultimately periodic. Cameron, Calkin and Finch have investigated this question, and it seems that the answer may be 'no': in particular, the sum-free sets {1,3,8,20,26,…} and {2,15,16,23,27,…} are not known to be ultimately periodic … Unfortunately there is currently no way to show that these sets are aperiodic (though there is good evidence [2,3] to suggest that they are)."
  - Footnote 1: "It seems that the problem as stated by Guy doesn't appear in the reference cited."
  - It proves S_α = {n : {nα} ∈ (1/3,2/3)} (aperiodic, sum-free) is **incomplete** for every irrational α, so that route cannot yield a counterexample. Its definitions: "S is complete … Equivalently, S is complete if and only if it is constructed greedily from a finite set."
- **Calkin–Finch–Flowers, "Difference density and aperiodic sum-free sets", INTEGERS 5(2) (2005) A03** (https://www.math.clemson.edu/~calkin/Papers/calkin_finch_flowers.pdf; published 9/1/05).
  - Abstract: "…These tests produce further evidence of a positive nature that certain sets are, in fact, not ultimately periodic."
  - "However, since we cannot show d(m) < 1 for all m, we cannot prove any of θ(0̇1001̇), θ(0̇1010̇), or θ(1̇0010̇) to be aperiodic." Those are non-greedy decision sequences (they contain zeros).
- **Finch, Errata and Addenda to Mathematical Constants** (arXiv 2001.00578, Jan 2020), §2.25: "Further evidence for the existence of complete aperiodic sum-free sets is given in [CFF 2005, Wen et al.]." That is still only "evidence", as of 2020.
- **Wen–Zhang–Wu, "On the regular sum-free sets"** (arXiv 1405.6493, Eur. J. Combin. 2015): "This question is still open."
- OpenAlex forward citations of Calkin–Finch 1996 (2026-10-13) list only: Calkin–Cameron 1998, CFF 2005, Wen et al. 2015, Finch's addenda/book chapters, a period-k-folding/Sturmian paper (2019/2020), and a few others. **Nothing before 2026 resolves it.**
- **Conclusion for task 2:** no earlier counterexample or proof for Dickson's problem. The earlier "counterexamples" were only numerical evidence, for sum-free bases.

### 2.4 Queneau 1972, Finch 1992 (the i<j variant)

- Queneau, "Sur les suites s-additives", J. Combin. Theory A 12 (1972) 31–71, DOI 10.1016/0097-3165(72)90083-0. I could not retrieve the text (ScienceDirect challenge, not bypassed).
- Secondary descriptions:
  - Green: Queneau's variant uses u_i+u_j with **i<j**.
  - van Berkel–Bosma 2026: "Queneau [11] defined s-additive sequences, which consist, after an initial segment, of those positive integers that can be expressed in exactly s ways as the sum of two different previous entries. For s = 0 this is the same as our 2-sumfree sequences. His Section 4 concerns this case (he calls those sequences non-additive). He considered many explicit cases S_{f,g}, and formulates several conjectures …"
  - MO #470827: Queneau's explicit periods for 0-additive bases {1,k}, {2,k}.
- Finch, "Are 0-additive sequences always regular?", Amer. Math. Monthly 99 (1992) 671–673: not retrievable. Per the MO summary and Green, it concerns the **strict (i<j)** 0-additive case with 2-term bases and conjectures regularity. (Also Finch, "Patterns in 1-additive sequences", Exp. Math. 1 (1992), not looked at.)
- **None of Dickson / Queneau / Finch states a sum-free requirement on the seed in the Dickson (i≤j) rule.** The sum-free-base requirement is Cameron's, from his bijection.

### 2.5 Seed caveat (sum-free vs arbitrary)

- Li's seed A = {1,2,3,5,7,13,22,27,28,32,36,40,47,48,52,63,71,77,81,89,97}: I counted **12 internal triples x+y=z** (e.g. 1+1=2, 1+2=3, 1+27=28, 1+47=48, 2+3=5, 2+5=7, 5+22=27, 5+27=32, 5+47=52, 7+40=47, 13+27=40, 27+36=63). So **A is not sum-free**.
- #341 as stated (Erdős–Graham "set of integers", erdosproblems "finite set of positive integers", Green "seed set") allows this. Dickson's own seeds {0,1,2} are not sum-free either.
- Li's S satisfies t∈S ⇔ t∉S+S only for t>97. S is not itself sum-free, so it is not a "complete aperiodic sum-free set" in the Cameron/Calkin–Finch sense.
- So the Cameron / Calkin–Finch **Conjecture 4.2** (every ultimately complete **sum-free** set is ultimately periodic) is, as far as I can tell, not addressed by Li. The paper does not claim to address it. A hostile referee should check whether the tail could be re-seeded from a sum-free base. No source I found does this.

### 2.6 2026 work on the strict (Queneau / "0-additive") variant, and #342

All of these post-date Li's claim (or nearly) and **none mentions Li or #341**.
- van Berkel & Bosma, "On t-sumfree sequences", arXiv:2609.16843 (2026-09-15).
  - t-sumfree = least integer exceeding the last that is not the sum of t *distinct* earlier values (t=2 is Queneau's s=0). "The main open problem concerns the question of the conjectured ultimate periodicity of these sequences."
  - Conjecture 2: every 2-sumfree S_{f,g} is ultimately periodic. Conjecture 4 (folklore): every 3-sumfree sequence is. Theorem 5: "at most 12 exceptions" among f≤25, d≤25.
  - "Note that a similar criterion for deciding non-periodicity based on a finite initial segment is lacking."
  - Related-work section describes the **non-strict** greedy 2-sumfree case, notes Cameron's bijection, and says: "Calkin and Finch did extensive calculations which left several periodic candidates for σ that seem to give aperiodic S."
- van Berkel & Bosma, "Periodicity conjectures for all 2-sumfree sequences", arXiv:2609.18522 (2026-09-16): precise conjectures that would imply every strict 2-sumfree sequence (2-term starts) is ultimately periodic.
- O. Shtrezi, "The greedy 3-sumfree sequence S_{1,g,g+1}", arXiv:2606.17447 (2026-06-13): explicit eventual periodic description.
- #342 (Ulam, unique sums): comments through 2026-09-16, no connection to Li. Li's controller is built for the non-strict (i≤j) rule. Nothing I found says it applies to the Queneau i<j variant or to Ulam.

---------------------------------------------------------------------------------------------------

## 3. Dated source list

| Date | Source |
|---|---|
| 1934-10 | Dickson, Bull. AMS 40:711–714 |
| 1972 | Queneau, JCTA 12:31–71 |
| 1980 | Erdős–Graham, p.53 |
| 1987 | Cameron, LMS LN 123 |
| 1992-08 | Finch, Monthly 99:671–673 |
| 1996 | Calkin–Finch (Exp. Math. 5:2); Calkin–Erdős (MPCPS 120:1, 1996-07) |
| 2005-09-01 | CFF, Integers 5(2) A03 |
| 2015 | Wen–Zhang–Wu (EJC) |
| 2020-01 | Finch addenda (arXiv 2001.00578) |
| 2026-01-20/22 | erdosproblems.com/341 last edit; FC #1778 merged |
| 2026-01-30 | Green's list PDF |
| 2026-07-08 | KentaKitamura comment |
| 2026-07-28 | EPAD working report |
| 2026-08-09 | Li repo created 11:56Z; claim submitted 15:32:18 |
| 2026-08-10→20 | Zenodo v1.0.0→v2.1.0 |
| 2026-08-26 | plby commit (Alexeev) |
| 2026-09-15/16 | van Berkel–Bosma arXiv |
| 2026-09-18 | FC #6069/#6070 merged |
| 2026-09-23/24 | JSP PR (mis-mapped, closed) |
| 2026-10-13 | GCL result (stale); erdosproblems and teorth still "open" |
