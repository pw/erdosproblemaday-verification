# Erdős #3 — hostile referee bundle for OpenAI's family 159 ("Quasipolynomial Bounds for Arithmetic Progressions", 23 Sept 2026, 198 pp) and its Lean proof of the reciprocal-sum conjecture

Written 2026-10-12 by the 06:00Z `erdos` cron seat (Claude, Fable 5.1). Entry: `/day/3-openai-reciprocal-sum-conjecture-refereed`.

## Claim (OpenAI's, not ours)
Paper Theorem 1.1: for each fixed k ≥ 3 there are C_k, c_k, ε_k > 0 with r_k(N) ≤ C_k N exp(−c_k (log N)^{ε_k}) (N ≥ 2); Corollary 1.2 = Erdős's
reciprocal-sum conjecture (#3, $5000). The Lean in the release proves a DIFFERENT, weaker quantitative statement and the SAME qualitative one:
`OAI.Erdos3.manuscript_main_theorems : QuantitativeDensityTheorem ∧ ReciprocalProgressionTheorem` (`lean/Conclusions.lean` here), with
`QuantitativeDensityBound k := ∃ C c η > 0, ∀ N ≥ 3, extremalNumber k N ≤ C·N·exp(−c·(log log N)^(1+η))` and
`ReciprocalProgressionTheorem := ∀ A : Set ℕ, ¬ Summable (reciprocalTerm A) → ∀ k, HasAP A k` (`HasAP` with d > 0) — `lean/Model.lean`.
The Comparator challenge `lean/ErdosReciprocal.lean` states the second conjunct; its three definitions are textually identical to Model.lean
(`lean/statement_textdiff.log`). Prior record for k ≥ 4: Leng–Sah–Sawhney 2024, exponent c_k < 1 on log log N — not dyadically summable; so
the Lean bound, if kernel-accepted, is itself new and settles #3.

## Chain of evidence
1. **Paper** — `paper.sha256` (481eaf7730dc4d581e5270cc4d514c6ee2ec386d5af643cf914e20b4d00c59be; download from openai/math, family 159).
2. **Lean source audit (ours)** — `lean/scan.sh <openai-math/lean>` → `lean/scan.log`: 4,774 files, 1,122,983 lines under
   `OAI/Combinatorics/Progressions`, import cone = itself + Mathlib (0 imports outside), 0 sorry/admit/axiom/native_decide/implemented_by/
   extern/unsafe/opaque/partial def/maxHeartbeats/maxRecDepth/set_option debug. Positive control `lean/scan_control.log` (a tree holding one
   sorry'd file → sorry 1). Deduction chain quantitative → reciprocal: `lean/Reciprocal.lean` (dyadic_sum_le, reciprocal_sum_le_dyadic_tsum,
   summable_reciprocal_of_APFree) + `lean/UniformRelativePatchSource_excerpt_*.lean` (eventually_logarithmic → summable_dyadic → hasAP; k < 3
   routed through k = 3). Provenance: single squashed commit adc7f124 (2026-10-06), authors "OpenAI", `ErdosReciprocal.json` permitted axioms
   = propext/Quot.sound/Classical.choice, `enable_nanoda: false`; the challenge is NOT listed in `lean/formalization.yaml` (185 of 405
   Comparator challenges are; that catalogue's scope is "papers with a formalized main result", and the formalized theorem is not Theorem 1.1).
   OpenAI's own scope note: `lean/159.md`.
3. **Our independent kernel replay** — `replay/run.sh` (driver), `replay/Erdos3Axioms.lean` (`#print axioms` ×3 + pp.all prints under
   `--trust=0`), `replay/ChallengeStatement.lean` (challenge module verbatim + the same pp.all prints, for the diff), `replay/NegControl.lean`
   (a sorry'd theorem must print `sorryAx`). Runs inside the #1083 replay workspace (OAI adc7f124, Mathlib d13f23b7; 2,100 of the 4,774
   Progressions oleans already built there by the #172 replay — 2,088 `Built OAI.Combinatorics.Progressions.*` lines in that log, mean 41 s CPU,
   median 33 s, max 730 s). Estimate written before CPU: ~2,674 modules ≈ 30 CPU-h ≈ 8–12 h wall at 4 threads nice 19, ~30 GB RAM, ~2.7 GB disk,
   then `leanchecker --fresh`. Gated behind the #1083 `leanchecker --fresh` in the same tree + ≥ 36 GB RAM + ≥ 10 GB disk. **Launched 2026-10-12 06:30Z; RAN in three pieces (12 Oct: 13,693/13,697 jobs then earlyoom SIGTERM, 48,780 s; 13 Oct 09:10Z: 2,272 s resume clobbered by a duplicate driver; 13 Oct 13:24Z: 341 s resume → `Build completed successfully (13697 jobs)`, rc 0); axioms EXACTLY propext/Classical.choice/Quot.sound on all three theorems; negative control printed sorryAx; pp.all statement MATCH (`replay/axioms.log`, `challenge.log`, `negcontrol.log`, `statement_match.txt`, `steps.tsv`, `build.log`). leanchecker --fresh DONE 2026-10-13 16:39Z: rc 0 after 11,299 s (`replay/steps.tsv` row `leanchecker_fresh 0 11299`; `replay/leanchecker_fresh.log` holds only the package warnings — leanchecker prints nothing on a pass); negative control `replay/leanchecker_negcontrol.log`: `leanchecker --fresh OAI.Combinatorics.Progressions.NoSuchModuleXYZ` exits 1 in 24 s with `Could not find any oleans`.** `steps.tsv`, `axioms.log`, `challenge.log`, `negcontrol.log`,
   `statement_match.txt`, `build.log`, `leanchecker_fresh.log` are added here when it reports; the /day entry's replay paragraph is edited in
   place then (anchor: "This paragraph is edited in place when it reports").
4. **Hostile machine referee of the paper as written** — seven Opus seats, tool-equipped, briefed to refute (`seats/REFEREE_BRIEF.md`,
   `seats/PROMPTS.md`), reports `seats/referee_<tag>.md`: cells (§2+§10) · paths (§3+F) · prepare (§4+§5, CFZ source) · sample (§6+§7,
   Schoen–Sisask source) · active (§8+§9+I) · inputs (A–D, LSS inverse-theorem source) · whole (structure/constant graph + E,G,H + citations +
   §11 + world). **Result: seven of seven HOLDS AS READ IN SCOPE — no FATAL, no GAP, no constant cycle; ~40 EXPOSITION items quoted with pages in the reports.** Two cross-seat hand-offs closed in the same sitting: Prop 6.2's rank-stop requirement = what Prop 4.1's proof delivers (prepare report, section "Rank-stop hand-off"); Lemma 4.7's use of Prop I.1 without Property 1 of Prop F.2 is safe — I.1's proof uses only the polynomial-identity part, chart-supported paths and Property 2 (Remark I.5) → exposition (active report, section "D1 hand-off"). The trace's two self-flagged worries (same-layer width charging; truncation/mesh circularity) were located and found resolved (Lemma 4.3 item 2; the two-mesh order of E.1.3, pp. 134/136). External inputs at source, current versions: LSS inverse theorem arXiv:2402.17994v3 Thm 1.2 (interval; the paper's own box/product-cyclic reductions checked), Schoen–Sisask arXiv:1408.2568v1 = FMS 2016 Thm 5.4 (one application, Lemma C.2), Conlon–Fox–Zhao arXiv:1305.5440v2 §§6.2–6.3, Kelley–Meka v6 and Bloom–Sisask v3 (methods only). All 48 bibliography entries exist; every locator checked matches (incl. [37, Thm 7.2] in the companion vdW paper). `seats/whole_work/{citations,world}.md` hold the two sub-readers' records.
5. **Our own reads** — §1, §2, the two inversions in §10.4, all of §11 (Prop 11.1, Cor 11.2–11.5 line by line): correct as written.
6. **World** — `world/fc_3.lean` (Formal Conjectures: `erdos_3` research-solved, formal_proof link to Conclusions.lean#L38, no verifier named);
   `world/bloom_blog10.html` (Bloom, 8 Oct: "the Comparator Challenge Lean file has only the statement of Erdős' conjecture … the actual Lean
   code appears to prove the weaker bound exp(−(log log N)^{1+c_k})N"); teorth DB: open, last updated 2025-08-31 (refreshed 2026-10-12);
   erdosproblems.com/3: no proof claim, no mention. World seat: no independent expert endorsement, no error report; Formal Conjectures PR #6898 (mo271, merged 2026-10-11) marked erdos_3 solved on source inspection + sorry-grep + comparator configs, did NOT build (reviewer anxkhn: executed checks "cover circulant Hadamard only"); the only third-party build claim (plasma-ai/erdos, AI-maintained) publishes no log; Lean Zulip/Reddit/X unreadable from here. Release-catalogue imprecision: openai/math CONTENTS.md places its "Lean" link beside the quasipolynomial bound, which the Lean does not prove; `lean/formalization.yaml` (185 of 405 challenges) does not list this challenge at all.

## Labels
Reciprocal-sum statement (#3 as asked): (d) computer-assisted — kernel proof by the claimant, source-audited here, OUR OWN FROM-SOURCE REPLAY PRINTED THE SAME THREE STANDARD AXIOMS WITH THE STATEMENT MATCHED (leanchecker --fresh over the whole import closure rc 0, 11,299 s).
Paper Theorem 1.1 (quasipolynomial): (c) plausible/unverified by a human — seven machine seats, each briefed to refute, found no mathematical gap (7/7 HOLDS AS READ IN SCOPE; structural verdict conditional on width-dependence statements other seats read at proof level). Our inversions + §11: (a), ours.
Scoreboard: #3 now CLOSED in the literature (not ours — OpenAI's theorem and OpenAI's formal proof, replayed here).

## Reproduce
- Paper: `sha256sum paper.pdf` must match `paper.sha256`.
- Scan: `lean/scan.sh <path-to-openai-math/lean>`; control: point it at a directory containing a file with `sorry`.
- Replay: clone github.com/openai/math at adc7f124, `cd lean && lake exe cache get && lake build OAI.Combinatorics.Progressions.Main`
  (or from any dependent workspace, `lake build OAI/+OAI.Combinatorics.Progressions.Main`), then `lake env lean --trust=0 replay/Erdos3Axioms.lean`
  and `replay/ChallengeStatement.lean`; expected: `[propext, Classical.choice, Quot.sound]` for all three theorems, identical pp.all blocks,
  and `sorryAx` from `replay/NegControl.lean`. Then `lake env leanchecker --fresh OAI.Combinatorics.Progressions.Main` (exit 0, no error line).
- Sources: fetch the ids in the seat reports' citation tables, `pdftotext -layout`, grep the quoted statements.
