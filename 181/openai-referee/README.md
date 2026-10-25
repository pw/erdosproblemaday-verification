# Erdős 181 — audit of OpenAI's "The hypercube Ramsey number has linear order" (23 Sept 2026)

**Claim under audit (theirs, not ours):** R(Q_n) ≤ C·2^n for an absolute constant C — the Burr–Erdős hypercube Ramsey
conjecture, i.e. the headline question of erdosproblems.com/181. Paper: openai/math, family 171, 172 pages; SHA-256 in
`paper.sha256`. **Nothing mathematical in this directory is ours.**

## The chain of evidence, strongest first

1. **Kernel-checked formalization by a third party** — github.com/cadamcat/hypercube-ramsey-lean4 (Yao Xu; v1.0.0 8 Oct,
   audited at HEAD `35fa134` 11 Oct). Statement and definitions = Formal Conjectures' `Erdos181.erdos_181` verbatim at FC commit
   9d259649 (diffed); `Bridge.lean` equates FC's Ramsey number with OpenAI's as sets, both directions, closing the `sInf ∅ = 0`
   trap; `Audit/IndependentRestatement.lean` proves an elementary restatement equivalent. Source audit in `seats/referee_lean.md`:
   no axiom, live `sorry`, `native_decide` or environment edit reaches the proof; Mathlib/Batteries/core pristine. 752 files,
   ~532k lines, written by AI agent lanes in ~32 h (1,922 commits), "agent-reviewed", reviewers: none. OpenAI's library supplies
   only the cube, the Ramsey number, elementary bounds and Lemma 2.1 (287 lines). Author's report: `#print axioms` = propext,
   Classical.choice, Quot.sound; a second-kernel check; his own bounty claim (JSP-000175) says "Independent verifier(s), if any:
   none" and "the raw logs are not published". Formal Conjectures marked it solved 11 Oct via the author's own PR #7128,
   approved in 32 minutes in a batch of ~20, merged 09:08Z, no rebuild (FC's CI cannot build a linked external proof).
2. **Our independent replay** — `replay/` (driver `run.sh`, `steps.tsv`, build log, `#print axioms` output, and a
   `leanchecker --fresh` log over the whole import closure, Mathlib included), produced on exe.dev from the pinned sources in a
   scrubbed environment. **Result (2026-10-11, driver relaunched 18:02Z after a first attempt died on a missing `lake` launcher in the scrubbed toolchain copy; `build.log.{first,second,third}-attempt` are those false starts):** `lake build HypercubeRamsey.Main` — 9,650 jobs, 18,514 s (5 h 08 min) at nice 19, four threads, `Build completed successfully`, zero `error` lines (the `ring`/`ring_nf` lines in the log are Lean `info: Try this` suggestions). `scripts/verify.sh` rc=0 in 129 s: `challenge exit 0, main exit 0, pp.all outputs identical: True`; `'Erdos181.erdos_181' depends on axioms: [propext, Classical.choice, Quot.sound]`; `PASS: all axioms are in the permitted set.` `Audit/TargetProbes.lean` and `Audit/IndependentRestatement.lean` both compiled under `--trust=0` (rc=0, 27 s / 28 s), their probes carrying the same three axioms (`axioms.log`). Mathlib's object files came from the official cache (`lake exe cache get`, 196 s), which `--trust=0` does not re-check in Lean 4.34; the `leanchecker --fresh HypercubeRamsey.Main` pass over the whole import closure started 2026-10-11T23:26Z and exited 0 after 7,773 s (`replay/leanchecker_fresh.log`: Lake "has local changes" warnings only, no error line; `replay/steps.tsv` row `leanchecker_fresh 0 7773`). Controls for reading that silence as a pass, run 2026-10-12 on the same build (`replay/leanchecker_controls.{sh,log}`): a non-existent module exits 1 with "Could not find any oleans"; a real module (non-fresh) exits 0 printing nothing. The driver's final step, the #172 project's own `leanchecker --fresh`, died with rc=127 (`lake: command not found` — the copied `.elan` has no `bin/` proxies) and was relaunched 2026-10-12T03:05Z with the toolchain `bin` on PATH; its result belongs to the #172 bundle.
3. **Hostile machine referee of the paper as written** — nine Opus seats, tool-equipped, briefed to refute (`seats/REFEREE_BRIEF.md`,
   `seats/PROMPTS.md`), reports `seats/referee_<tag>.md`: framework (§2–3) · initial_a (§4–5) · initial_b (§6–7) · asymmetric
   (§8–9) · cluster (§10–12) · allocation (§13–15) · lowmodes (§16–18) · citations (bibliography + world) · lean (source audit).
   Verdict: **HOLDS AS READ, nine of nine; no mathematical gap.** Found: one exposition gap (Lemma 18.1, p. 149 — the second-moment
   step needs every sketch entry in D⁰_w, unstated but forced by the gate; found independently by lowmodes and, via the
   formalizers' notes, by lean); one step taken on trust (§9.1's center map "adapting Steps 2–4 of Lemma 3.8" outside that lemma's
   hypotheses; every exponent condition checks); one load-bearing reading (p. 93, supremum over ≥ .99λ eligibility sets); one
   asserted measurability (pp. 92, 96); compressed orderings in Prop. 15.3–15.4; a "(1+o(1)) per variable" in §5.4; cosmetic notes.
   No hidden rate on N/2^n → ∞ anywhere (nine independent traces).
4. **Primary-source checks** — in `seats/referee_citations.md`: all 34 references resolved (31 DOIs via Crossref/zbMATH, two
   renyi.hu scans); every theorem-number citation in §1.1–1.2 quoted beside the paper's paraphrase; per-scope citation tables in
   each seat report (Azuma, Freedman, Hoeffding, Finner, Lu–Székely, Erdős–Lovász, Moser–Tardos, HSS, Harris–Srinivasan, dependent
   rounding, Lipschitz percolation, Hamming, CFLS Prop 2.2, FGMSS §2). Hall 1935 and Kakutani 1941 could not be fetched (publisher
   bot walls); used in their textbook form.
5. **World state** — `world/`: FC `181.lean` at main (11 Oct) + its history; the cadamcat commit log (last 100), repo metadata,
   lake-manifest; `WORLD_FINDINGS.md` (search log). erdosproblems.com/181 shows no status; Bloom's 8 Oct post: "not formalised";
   teorth DB: open, unformalized; no human proof, no improvement on Tikhomirov, no expert comment found.

## Labels
Theorem: (d) computer-assisted — a Lean 4 kernel proof exists, author-reported replays, and our own from-source replay printed the same three standard axioms (verify.sh PASS; leanchecker --fresh over the whole import closure, Mathlib's cache included, exited 0 on 2026-10-12 ~01:35Z). Paper as written: (c) plausible/unverified by a
human — nine machine seats, each briefed to refute, found no mathematical gap. Citation checks and our own spot reads
(Lemma 3.2, 3.7, §13.2, Lemma 16.1, §18.5): (a)/(b), ours.

## Reproduce
- Replay: `git clone https://github.com/cadamcat/hypercube-ramsey-lean4 && cd hypercube-ramsey-lean4 && lake update;
  scripts/apply-oai-patches.sh && lake exe cache get && lake build HypercubeRamsey.Main && LEAN_NUM_THREADS=4 scripts/verify.sh
  && lake env leanchecker --fresh HypercubeRamsey.Main` (our exact driver: `replay/run.sh`). Expected: `PASS` from
  `scripts/check_axioms.py` with exactly propext, Classical.choice, Quot.sound; leanchecker exits 0.
- Sources: fetch the ids in the seat reports' citation tables, `pdftotext -layout`, grep the quoted statements.
- Paper: `sha256sum paper.pdf` must match `paper.sha256`.

## World state at audit time (2026-10-11)
teorth DB: 181 OPEN (lu 2025-08-31), fz 1. OpenAI CONTENTS.md: family 171, PDF only. Formal Conjectures: research solved
(PR #7128, the formalizer's own). Bloom's 8 Oct post: listed, "not formalised". No independent build reported anywhere; ours is the first.
