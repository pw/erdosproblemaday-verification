Full notes with every query and URL: `/tmp/erdos2100/seats/A/world_search.md`. Raw fetches: `/tmp/erdos2100/seats/A/raw/`. All read 2026-10-13.

**Nobody has disputed it, nobody found an error, and nobody authoritative has accepted it.**

**erdosproblems.com/341** (https://www.erdosproblems.com/341; history https://www.erdosproblems.com/history/341)
- The page was last edited 2026-01-20 and shows no solved/disproved marker.
- Proof-claims tab (https://www.erdosproblems.com/forum/thread/341/proof-claims): one claim (#200) by Z_Li, submitted 2026-08-09 15:32:18. It carries the disclaimer "Appearing on this page is no guarantee of proof correctness…" and has 0 comments.
- Posting comments and proof claims is paused site-wide, so the silence is partly structural.
- The only thread comment (https://www.erdosproblems.com/forum/thread/341) is KentaKitamura, 2026-07-08. It concerns the {1,4,9,16,25} side remark (period 224 from a_87), not Li.

**teorth/erdosproblems** (https://github.com/teorth/erdosproblems/blob/main/data/problems.yaml at HEAD 2026-10-13): #341 is still `status: open`, last_update 2025-08-31.

**Formal Conjectures** — the only institutional uptake.
- Issue https://github.com/google-deepmind/formal-conjectures/issues/6069 and PR https://github.com/google-deepmind/formal-conjectures/pull/6070 were merged 2026-09-18 (commit a8d29337). The PR was approved by mo271 with "Thanks, LGTM!" and no other discussion.
- The merge set `answer(False)` and `research solved` and linked plby's wrapper.
- The FC theorem body is still `sorry`. The PR's ℕ→ℤ/IsLeast bridge was "verified locally, not part of this PR". My `Bridge.lean` is an independent machine check of exactly that bridge.

**plby/lean-proofs** (https://github.com/plby/lean-proofs/commit/faeedb63f1c9d991c943baf17304e48daa111d19, 2026-08-26, Boris Alexeev)
- It re-hosts Li's Lean files byte-identically (import paths aside), adds `not_erdos_341`, and adds a Comparator challenge. It is a re-host, not an independent proof.

**Ben Green's list** (https://people.maths.ox.ac.uk/greenbj/papers/open-problems.pdf): the PDF is dated 2026-01-30, before the claim. Problem 7 poses both the Dickson (i,j ≤ n) and Queneau (i<j) variants as open.

**Searched, nothing about Li's claim found:**
- arXiv API, 7 queries; the positive control returned hits. Li's paper is not on arXiv.
- OpenAlex.
- MathOverflow / Math.SE.
- Tao's blog (search "erdős 341").
- Hacker News.
- Mathstodon (#erdosproblems, #erdos).
- GitHub code/issue search for "Zhiheng", "LiAlreadyExists", "erdos_341".

**Not searchable:** X/Twitter, Reddit, Lean Zulip, Discord.

**Two closed or stale items that are NOT verdicts:**
- TheJustinSunPrize/awards PR #4260 was closed with boilerplate and is mis-mapped: its JSP-000341 is a different problem.
- grandchallenge/MATH-PROGRAMME#1611 is an automated audit built on stale pins and never saw the claim.

**Li's repo and Zenodo** (https://github.com/LiAlreadyExists/Erdos-341, https://zenodo.org/records/22030511)
- The repo has 1 star and 0 issues.
- The DOI cited in the paper is the **v2.0.1** snapshot. The latest is v2.1.0 (record 22030579). Lean files are byte-identical across versions and since the first upload; `Erdos341g.lean` is identical at v2.0.1 and v2.1.0.
- Provenance nit: the since-deleted `BUILD_VERIFIED.md` recorded a sha256 for `Erdos341.lean` (`e95e8a49…`) that does not match the committed file (`75c56c1e…`). That is a self-reported record. Our replay built the committed file, so this is not a soundness issue.

**Prior literature: no earlier proof or counterexample.**
- **Dickson 1934**, Bull. AMS 40, 711–714 (https://www.ams.org/journals/bull/1934-40-10/S0002-9904-1934-05951-2/), read in full.
  - It concerns additive bases ("universal k-sets", containing 0). Construction I is the greedy rule with **equal summands allowed**: "least integer which is not a sum of any two of the first n−1 elements … 0 and all positive odd integers".
  - It **never asks the periodicity question**. Calkin–Erdős 1996, footnote 1: "the problem as stated by Guy doesn't appear in the reference cited."
  - Dickson's seeds contain 0. Adding 0 to Li's seed changes nothing, because x+0 ≤ a_n < t.
  - So there is no reading of Dickson under which Li's example fails, beyond the i<j and sum-free variants discussed above.
- **Calkin–Finch 1996** (Exp. Math. 5, 131–137; https://emis.de/ft/51959): Table 3 lists 19 "apparently aperiodic" complete sum-free sets, all from **sum-free bases** and checked to 10^7. They state "no method is known that will show that a sum-free set is not ultimately periodic from … finitely many elements." Their Conjecture 4.2 (Cameron) concerns sum-free sets.
- **Calkin–Erdős 1996** (https://www.math.clemson.edu/~calkin/Papers/calkin_erdos.pdf): {1,3,8,20,26,…} and {2,15,16,23,27,…} are "not known to be ultimately periodic … no way to show that these sets are aperiodic".
- **Calkin–Finch–Flowers 2005** (INTEGERS 5(2) A03): more evidence, no proof.
- **Finch's 2020 addenda** (arXiv 2001.00578) and **Wen–Zhang–Wu 2015** (arXiv 1405.6493, "This question is still open"): no resolution.
- So Li's is, to everything found, the **first proved** aperiodic example. It is for arbitrary seeds; the sum-free-base version remains open (objection 3).
- **2026 work on the strict i<j variant**: van Berkel–Bosma arXiv:2609.16843 and 2609.18522 conjecture ultimate periodicity there, which is consistent with my period-693 observation for Li's seed under i<j. Shtrezi arXiv:2606.17447. None mentions Li.

**Erdős–Graham p.53, checked against the page image `pg-049.png`:** "for n ⩾ k" (not "n > k" as in the OCR), and "a_i + a_j, i, j ⩽ n". This confirms the statement-match table.
