# Seat W — the world, Erdős #684 / arXiv 2604.23784v3 (checked 2026-10-31 UTC)
(Saved by the main seat from the seat's final message; the harness blocked the subagent from writing this file. Raw pages/JSON in `evidence/`.)

## Q1. Replays / audits of jidodat/erdos684-lean
- Repo created 2026-09-03T11:36Z, last push 18:40Z; 0 issues, 0 PRs; only fork = Palomar's preservation copy `PalomarArchive/jidodat--erdos684-lean--b4c193c90ac2`.
- Tag `v3-arxiv` = `49ee38c` (Lean 4.32.2, Mathlib 905b958). **Palomar registered the later commit `4543ff7`** (Lean 4.32.0, Mathlib 81a5d257; adds Challenge, Solution, comparator.json, formalization.yaml). `git diff v3-arxiv 4543ff7 -- Erdos684Lean` is EMPTY ⇒ proof sources identical.
- formalization.yaml @4543ff7: "No external or independent human review of the Lean development has been performed." (review status: self-assessed).
- **Palomar PALOMAR-2026-09-03-000006 v1** (record https://data.palomar-registry.org/entries/PALOMAR-2026-09-03-000006-v1.json): mechanical check Actions run https://github.com/PalomarRegistry/PalomarSubmission/actions/runs/33787783004, success 2026-09-03T18:11Z, log tail "nanoda kernel accepts the solution … Lean default kernel accepts the solution / Your solution is okay!"; compared `Erdos684.Palomar.{main_theorem, main_theorem_limsup, unbounded, lt_f_iff, u_mul_eq_choose}` allowing only propext/Quot.sound/Classical.choice. Review by `codex:gpt-5.6-sol` 18:22Z, outcome "neutral", no findings ("Mechanical verification succeeded, and the editorial checks identified no blocking problem…"); schema: "neutral" = "no blocking problems were identified". (evidence/pal_*.json)
- Palomar statement (18 Aug 2026; Avigad, Ballard, De Dios, Guillen, Kra, Morrison, Tao, Vakil, Venkatesh): "the appearance of a work in the registry does not constitute a certificate of novelty, nor a certification of relevance, nor a certification that the verified statement matches the informal statement." · "Palomar also replays every exported proof through a second, independently implemented kernel (nanoda) as well as Lean's own". About page: "Palomar adds no human editorial step: no one here reads the mathematics the way a referee would." · "It does not accept, approve, or endorse a result." "Trust level: high" describes the Challenge file (112 lines, imports Mathlib only).
- No replay/audit found at: AItoBit/erdos-684-elementary-bounds (18 Oct; Palomar 2026-10-18-000007; APSSV-strength bounds only; SOURCES.md: "This is a check of the registry record, not an independent audit…"); plasma-ai/erdos wiki E0684 (8 Oct: "Bae's Lean 4 development, not built or audited here"); cert-machine (12,261-file tree incl. corpus/openai-math/kernel-runs/); nealmcb/openai-math-lean-tooling; mathvet/mathvet; GitHub code search (hits = Bae's jbaelaw/erdos457-lean reuse, index/RSS mirrors, our repo); GitHub issues/PRs (only dzackgarza/formalization-corpus#9, 28 Oct, a to-do list); Lean Zulip web-public (684, erdos684, jidodat, 2604.23784, "Ji Ho Bae", the Palomar ID, "shifted carry").

## Q2. Literature since 1 Sep 2026
- arXiv export API `abs:"problem 684"` → only Li 2606.08216v1 and Bae v3; Sept–Oct sweep of 201 "Erdős" + 209 "binomial" abstracts: none on #684. APSSV 2603.29961 last v2 (2 Apr); Li only v1 (6 Jun), doesn't cite Bae; Bae v1 26 Apr, v2 28 Apr, v3 3 Sep (comment: "v1-v2 argument, which relied on an unjustified weighted extension of Timofeev's method, is withdrawn").
- Citations of 2604.23784: zero (Semantic Scholar, OpenAlex).
- Zenodo: Bae 19807164 (27 Apr, v1 argument; abstract "refute the widely expected upper bound f(n) ≪ log n") and 22264212 (3 Sep, v3). **Sayantan Roy, Zenodo 23183198 (DOI 10.5281/zenodo.23182889, 6 Oct)** claims "f(n) ≤ C log n + O(log log n)" for all n (contradicts v3; doesn't cite Bae). Key step ends "log u ≥ 3/4 k + O(k) ≥ 1/4 k" (does not follow); its every-n bound is incompatible with the APSSV construction it restates (u(n_K,k)=1 for all k ≤ K); the text contains "hmm, that's not right either". No responses found.
- Tao's blog, MathOverflow, X (last 7 days): nothing.
- Verdict: no improvement, no proof of f(n) ≫ (log n)² i.o., no reported error in v3.

## Q3. erdosproblems.com/684
- **No status shown** (`<div class="problem-text" id=neutral>`), per Bloom's 6 Oct "Changes" post (https://www.erdosproblems.com/forum/thread/blog:9): "The site will not display the statuses of any problems". Page last edited 1 Apr 2026 (/history: 2025-10-20, 2026-04-01). Remarks credit Tang+ChatGPT, Sothanaphan heuristic, OpenAI model (APSSV26); no Bae, Li or Palomar.
- Thread (27 comments, post IDs 3477–6535): Bloom #post-3521 (20 Jan) "perhaps for infinitely many n we have f(n)≫(log n)^2, say." · Sothanaphan #post-3554 (20 Jan) "Further computation supports f(n) is possibly Θ(log n)." · #post-3637 (22 Jan) "limsup f(n)/log n ≈ 8" · Tao #post-5186 (1 Apr) on APSSV getting "a log² n type bound on f rather than the conjectural log^{1+o(1)} n bound" · jidodae (Bae) #post-5958 (27 Apr) v1 Zenodo link, no replies · **Oliveira e Silva #post-6535 (20 May): "not enough to give us a clear indication if f(n)/log n is bounded or not."** (last comment).
- Proof claim 247 (2026-09-04 01:05): tab disclaimer "no guarantee of proof correctness, and does not mean that anyone associated with this site has examined any part of the proof." Bloom #post-8733 (4 Sep): "I have edited this to a partial proof claim, since … there is still some uncertainty about how fast f(n) actually grows." Woett #post-8742: "this result disproves the possibility of an asymptotic." Bloom #post-8746: "I'd like to know whether e.g. f(n)≫(log n)^2 infinitely often." Commenting suspended. Block reads "A proof claimed by Ji Ho Bae."; "partial" appears only in Bloom's comment. Bloom's 6 Oct post: will "link to correct Lean formalisations (if verified on Palomar) quickly"; 684 page not updated.

## Q4. teorth database, Formal Conjectures
- teorth/erdosproblems data/problems.yaml (HEAD bcd2fbd, 29 Oct), 684: status open (2025-08-31); formalized yes (2026-10-19, bot, FC PR #7438). Nothing about Bae.
- Tao's AI-contributions wiki (last commit 30 Jun): three 684 rows, all "Partial result" (OpenAI model, Tang, Sothanaphan); no Bae row.
- FC 684.lean: PR #7438 by AItoBit, merged 19 Oct, closes #877; 29 Oct touch (Palomar linter off). States `erdos_684.upper_bound` (514) and `erdos_684.lower_bound` (1/8, u = 1), both research solved → AItoBit's Lean. PR body: "Bae's separate registered development proves a stronger lower bound". No open issue/PR on 684 or Bae.

## Q5. OpenAI math catalogue
CONTENTS.md (721 manuscripts, 373 families): no #684, no 2603.29961, no binomial smooth-part result; no #684 Lean. Only public #684 Lean: Bae's and AItoBit's (gotrevor/binomial-thresholds is a sorry scaffold).

## Q6. Objections to v1/v2 before v3
- v3 Remark 1.1 (Relation to v1–v2): "Versions 1 and 2 used a weighted extension of Timofeev's mean-in-progressions method … not justified by the cited theorem; those arguments are withdrawn … No Timofeev, Burgess, or Fourier-sieve input is used". No mention of Lemma 18 or an outside report.
- v2: Theorem 6 "Weighted squarefree transfer of Timofeev's method" = the withdrawn step. Lemma 18 "Non-prefix Fourier tails" = ours. v1 has no such lemma ⇒ Lemma 18 entered in v2.
- Ours: erdosproblemaday.com/report/684 (access 27 Jul; site commit 4d84aa8, 2026-07-27T21:54Z), Wayback http://web.archive.org/web/20260729215733/https://erdosproblemaday.com/report/684 (contains the Lemma 18 text). Never sent to Bae or the site.
- VibeMathed (vibemathed.com/problem/erdos-684, repo 68ec269, 30 Jul): "Retracted / Contested" because "a deterministic audit later found a counterexample to its key Lemma 18" — names no auditor (consistent with relaying ours; not established). VibeMath (12 Sep) mirrors it. Both stale vs v3.
- Nobody publicly reported the Timofeev flaw before Bae's 3 Sep comment.

## Sentences safe to write
1. Palomar registered Bae's Lean on 3 Sep 2026; its pipeline checked commit 4543ff7 with Comparator, Lean's kernel and the independent nanoda kernel, and an automated LLM review found no blocking problem.
2. Palomar says it adds no human referee and certifies neither novelty nor that the formal statement matches the informal one.
3. The registered commit is not the arXiv tag v3-arxiv, but the Erdos684Lean/ proof files are identical.
4. Apart from Palomar's registration run we found no public replay or audit; Bae's metadata says no independent human review; AItoBit and plasma-ai say they did not build or audit it.
5. We found no work after 3 Sep 2026 that improves the bound, proves f(n) ≫ (log n)² i.o., or reports an error in v3 (scope stated).
6. erdosproblems.com/684 last edited 1 Apr 2026, doesn't mention Bae or Li; the site has shown no statuses since 6 Oct; teorth/erdosproblems lists it open.
7. Bloom relabelled the claim partial on 4 Sep because the growth rate is still uncertain, and asked whether f(n) ≫ (log n)² i.o.
8. The forum explicitly asked whether f(n)/log n is bounded (Oliveira e Silva, 20 May); if v3 is correct, no.
9. FC 684.lean states only APSSV-type bounds (514, 1/8), not Bae's result.
10. The OpenAI catalogue has no #684 entry and no #684 Lean.
11. We published a counterexample to v2's Lemma 18 on 27 Jul 2026 (archived 29 Jul), found no earlier public report of it, and did not send it to the author.
12. v3 withdraws v1–v2 for a different step (v2's Theorem 6, Timofeev) and does not mention Lemma 18; Lemma 18 first appears in v2.
13. Bae's bound is still log^{1+o(1)} n: it rules out f(n) = O(log n) but is consistent with Tao's remark about a conjectural log^{1+o(1)} n bound.

## Sentences NOT safe to write
"Nobody has checked this proof/the Lean" · "We are the first to verify/replay it" · "The arXiv tag was Palomar-verified" · "Palomar certifies/approves/endorses" · "Bae withdrew v1–v2 because of us" · "We were the only ones to flag v1/v2" · "erdosproblems.com lists #684 as OPEN" · "Bloom marked it partial because he doubted correctness" · "erdosproblems.com accepted/acknowledged Bae's result" · "Bae refutes Tao's conjecture / Sothanaphan / Li density-one" · "#684 is solved" · "v3 is refereed/published" · "No one disputes v3" (Roy, 6 Oct — describe it as broken) · "FC formalizes Bae's theorem / marks the problem solved" · "OpenAI formalized #684" · "VibeMathed/VibeMath describe the current state".

Scope limits: X ~last 7 days; Zulip web-public only; GitHub search index only; Google Scholar unreachable. Contacted no one, posted nothing.
