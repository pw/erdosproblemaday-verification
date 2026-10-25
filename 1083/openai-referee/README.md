# Erdős 1083 — audit of OpenAI's "The higher-dimensional Erdős distinct-distances conjecture" (dated 23 Sept 2026; public 6 Oct 2026)

**Claim under audit (theirs, not ours):** for every integer d ≥ 3 there is c_d > 0 such that every set of n ≥ 2 points in ℝ^d
determines at least c_d·n^{2/d} distinct distances — the higher-dimensional Erdős conjecture WITH the constant factor (the
problem page asks for n^{2/d−o(1)}). Paper: openai/math, family 166, 103 pages; SHA-256 in `paper.sha256`. State of the art
before it: n^{2/3−o(1)} in ℝ³ (Tidor–Yu–Zakharov, arXiv:2608.14454v1, Aug 2026); Solymosi–Vu's n^{2/d − 2/(d(d+2))} in general.
**Nothing mathematical in this directory is ours.**

## The chain of evidence, strongest first

1. **Third-party Lean 4 formalization** — github.com/cadamcat/distinct-distances-lean4 (Yao Xu; v1.0.0 10 Oct, HEAD `88919b8`
   11 Oct 02:42Z). Target `DistinctDistances.jsp_000900` = Theorem 1.1 (constant factor, every d ≥ 3, every set of ≥ 2 points, L²
   metric, real exponent) plus the grid upper bound; strictly implies Formal Conjectures' `erdos_1083` right-hand side (short step,
   not formalized there). Source audit `seats/referee_lean.md` (+ `lean/audit_scripts/`): across the 757-file project, the 503-module
   OpenAI closure and the one patch-injected third-party file in the import cone, zero `sorry`/`admit`/`axiom`/`native_decide`/
   `implemented_by`/`extern`/`unsafe`/`opaque`/`debug.*`/`addDecl`, no metaprogramming in the cone; Mathlib pinned upstream
   `d13f23b`, unpatched. ⚠ It does NOT "follow the paper" where the plane is concerned: Theorem B.12 / Cor. B.13 / B.7–B.11 have no
   counterpart; the Lean uses a Pach–Sharir-type |Δ| ≥ c n^{3/4}, plane occupancy ≤ C M^{4/3}, c₀ = 1/3. Provenance: one squashed
   211,476-line commit (2026-10-10T18:52Z) + 5 comment commits, development history private, written by AI agents, "agent-reviewed,
   reviewers: []", Comparator run not sandboxed (author's own docs), `Challenge.json` has `enable_nanoda: false`. Built by nobody but
   the author. OpenAI's own library supplies 503 modules / 130,917 lines (degree, dimension, Hilbert–Serre/Lech, local Bézout,
   Bertini, Borsuk–Ulam), far more than the "polynomial isolation interface" its README names. Copies of the repo's top-level
   files in `lean/`.
2. **Our independent replay** — `replay/` (driver `run.sh`, `steps.tsv`, `build.log`, `axioms.log`, `verify_and_audits_excerpt.log`;
   `flip1083.py` is the anchored script that edited the /day entry). The driver waited behind the #181 replay whose built packages it
   reuses (both manifests pin OAI `adc7f124` + Mathlib `d13f23b7`; asserted), opened its gates 2026-10-12T01:37Z (39 GB free, load 15),
   checked out `88919b8`, ran `scripts/apply-oai-patches.sh`, `lake exe cache get` (180 s). **Result (2026-10-12):** `lake build
   DistinctDistances.Main` — 10,172 jobs, 13,960 s (3 h 53 min) at nice 19, four threads, `Build completed successfully`, zero `error`
   lines. `scripts/verify.sh` rc=0 in 153 s: Challenge.lean matches its frozen blob; `definitions block identical: True`; `challenge exit 0,
   main exit 0, pp.all outputs identical: True`; `'DistinctDistances.jsp_000900' depends on axioms: [propext, Classical.choice,
   Quot.sound]`; `PASS: all axioms are in the permitted set.`; `scanned 756 files: PASS: no forbidden constructs`. `Audit/TargetProbes.lean`,
   `Audit/IndependentRestatement.lean`, `Audit/NonVacuity.lean` compiled under `--trust=0` on the same build (rc=0; 14 s / 14 s / 30 s),
   probes carrying the same three axioms (e.g. `'NonVacuity.g_unbounded' depends on axioms: [propext, Classical.choice, Quot.sound]`).
   Mathlib's object files came from the official cache, which `--trust=0` does not re-check in Lean 4.34; the `leanchecker --fresh
   DistinctDistances.Main` pass over the whole import closure started 2026-10-12T05:43:04Z and EXITED 0 at 07:55:03Z after 7,919 s
   (`replay/steps.tsv` row `leanchecker_fresh 0 7919`; `replay/leanchecker_fresh.log` = 23 Lake "has local changes" warnings, no
   error line). Controls on the same build (`replay/leanchecker_controls.{sh,log}`): NEG `leanchecker DistinctDistances.DoesNotExist`
   → "Could not find any oleans", rc=1; POS `leanchecker DistinctDistances.Framework` (non-fresh) → silent, rc=0. The Mathlib cache is
   therefore kernel-checked too; nothing in the import closure was rejected.
3. **Hostile machine referee of the paper as written** — TWELVE Opus seats, tool-equipped, briefed to refute
   (`seats/REFEREE_BRIEF.md`, `seats/PROMPTS.md`), reports `seats/referee_<tag>.md`: reduction (§1–2) · algebra (§3) · secants
   (§4–5) · sparse_a (§6 preamble, 6.1–6.2) · sparse_b (§6.3–6.5) · motions (§7) · concentration (App. A) · incidence (App. B) ·
   citations (+ world) · whole (whole paper + global constant graph) · lean (source audit) · numerics. Nine were written by the
   2026-10-11 21:00Z cron seat (which hit its session limit); secants, whole and numerics were re-run from scratch by the 00:00Z seat.
   Verdict: **HOLDS AS READ, twelve of twelve; no FATAL, no GAP; ~90 exposition notes (UNCLEAR/COSMETIC), every one with its quote.**
   Findings worth knowing: no hidden rate on δ or M/A anywhere (28 asymptotic steps classified by the whole seat); no cycle in the
   constant graph (H, K, c, C, c₁, c′, c₂, c₃ are "fixed along the subsequence" ⇒ c_d is ineffective); the planar input needed is
   any exponent > 2/3, NOT Guth–Katz n/log n (lean, incidence, secants, whole — independently) — but Guth–Katz's k ≥ 3 incidence
   theorem B.5 IS consumed at full k⁻² strength via Cor. B.6 → Lemma 7.4 → Thm 7.1 at d = 3, hence on the critical path for every d;
   the lower-dimensional theorem is needed at full constant strength only in Prop 2.2, case ℓ = 4 (d ≥ 7); Theorem 7.1 proves what
   TYZ state as Conjecture 7.13 ("out of reach"); Lemma 3.6 holds with explicit c_{n,k} = 1/((n−k+1)^n k!), uniform in component
   degree, and its hypothesis is load-bearing (4 of 38 hypothesis-breaking toys fall below the bound); Appendix A proves only the
   containment (i = 0) concentration TYZ call within reach; Lemma 2.1's circle row is really 2M−1 (sharp) and line row M; Prop 5.5's
   pool-mass sentence names the wrong operative bound (sparse_a, secants, whole agree on the repair); s_* depends on δ, unstated,
   legitimately; the text was finalised 1–6 Oct under a 23 Sept title date (Stacks "consulted … October 1, 2026"; one repo commit).
   Scripts behind the numeric checks: `seats/scripts_*/`.
4. **Our own reads** (in the /day entry): §2 exponent bookkeeping; Prop 2.6's rank contradiction; the proof of Lemma 3.6
   (Lemma 3.3's divided-difference separators + the standard-monomial scaling (3.8)); Prop 4.3 in full (line case incl. the Hölder
   step, d ≥ 4 stabilizer argument, d = 3 valid-triple count); statements of Thms 7.1, A.1, B.2, B.12.
5. **Primary-source checks** — `seats/referee_citations.md`: 24 of 28 references read at source (Fulton, Hartshorne: books, could not
   fetch; Beck, Elekes–Tóth: attribution only); every theorem-number citation in §1–2 matches verbatim; per-scope citation tables in
   each report (Chardin, Chardin–Philippon + erratum, Walsh ×2, TYZ, Guth–Katz ×2, Elekes–Kaplan–Sharir, KKT, Bardwell-Evans–Sheffer,
   Solymosi–Vu, Hatcher, 11 Stacks tags). No fabricated detail; no black box on the main chain beyond standard algebra + Borsuk–Ulam.
6. **World state** — `world/WORLD_FINDINGS.md` (+ raw fetches in `world/mine/`): teorth DB OPEN (lu 2025-10-17, statement
   formalized 2026-09-07); erdosproblems.com/1083 no status, no mention of OpenAI/TYZ; Bloom 8 Oct: listed, "not formalised";
   Formal Conjectures: issue #6905 open, no PR; JSP-000900 "Solved … independent mathematical review pending", not claimable,
   formalizer's PR #4994 open ("Independent verifier(s), if any: none"); Palsson–Wang arXiv 7 Oct still cites Solymosi–Vu for d ≥ 4;
   no arXiv/MO/Zulip/blog discussion of the mathematics by any named expert; the two earlier arXiv claims (Aksoy Yazici 2020,
   withdrawn; Agama) are not proofs.

## Labels
Theorem: (d) computer-assisted — a Lean 4 kernel proof exists (third party, different planar route), author-reported replays, and OUR
OWN FROM-SOURCE REPLAY PRINTED THE SAME THREE STANDARD AXIOMS (verify.sh PASS 2026-10-12 05:42Z; leanchecker --fresh over the whole
import closure, Mathlib's cache included, exited 0 at 07:55Z). Paper as written: (c) plausible/unverified by a human — twelve machine seats, each briefed to refute,
found no mathematical gap. Citation checks, numerics and our own reads: (a)/(b), ours. Scoreboard: #1083 now CLOSED in the literature (not ours — OpenAI's theorem,
Yao Xu's formal proof, replayed here); nothing pending.

## Reproduce
- Paper: `sha256sum paper.pdf` must match `paper.sha256` (download from openai/math, family 166).
- Replay: `git clone https://github.com/cadamcat/distinct-distances-lean4 && cd distinct-distances-lean4 && git checkout 88919b8 &&
  lake update; scripts/apply-oai-patches.sh && lake exe cache get && lake build DistinctDistances.Main && LEAN_NUM_THREADS=4
  scripts/verify.sh && lake env lean --trust=0 Audit/*.lean && lake env leanchecker --fresh DistinctDistances.Main` (our exact driver:
  `replay/run.sh`). Expected: axioms exactly propext, Classical.choice, Quot.sound; leanchecker exit 0.
- Numerics: `python3 seats/scripts_numerics/<script>.py` (outputs in `seats/scripts_numerics/outputs/`); `seats/scripts_secants/checks.py`;
  `seats/scripts_incidence/`, `seats/scripts_motions/`.
- Sources: fetch the ids in the citation tables, `pdftotext -layout`, grep the quoted statements.
