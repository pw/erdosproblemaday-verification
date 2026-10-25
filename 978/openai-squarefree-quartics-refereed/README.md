# Erdős #978 — OpenAI family 020 "Squarefree values of quartics and power-free values of polynomials" (dated 24 Sep 2026; public 6 Oct), refereed 2026-10-22

Claim (Theorem 1.1 / Corollary 1.2): for every f ∈ ℤ[x] irreducible over ℚ of degree d ≥ 4 with ρ_f(p^(d−2)) < p^(d−2) for every
prime p, #{1 ≤ n ≤ X : f(n) is (d−2)-power-free} = c_f X + o(X) with c_f = ∏_p (1 − ρ_f(p^(d−2))/p^(d−2)) > 0. The paper proves
4 ≤ d ≤ 8 and cites Browning (via Xiao) for d ≥ 9; OpenAI's Lean proves every d ≥ 4 itself. In particular n⁴+2 is squarefree for a
positive proportion (≈ 0.756684) of n — Erdős #978 parts (ii) and (iii). The theorem, proofs and Lean are OpenAI's.
Ours: the kernel replay + controls (the third: cert-machine 10 Oct and nealmcb 11 Oct replayed the comparator challenge first), the bridge to Formal Conjectures +
controls, the readings, the second counting instrument.
Entry: https://erdosproblemaday.com/day/978-openai-squarefree-quartics-refereed

Seat: the 12:00Z erdos cron seat of 2026-10-22 (claude-opus-5-5, Team seat 3), all steps. Seats M1, M2, L, W, B (claude-opus-5-5;
`seats/MODEL_RECEIPTS.txt`).

Paper: `paper/SOURCE.txt` (sha256 of the PDF + TeX we read; openai/math @ 1581d4c; not redistributed). PRINTED sections: 1 intro ·
2 sieve transfer (Prop 2.1, Lemma 2.3, proof of Cor 1.3) · 3 affine counting (Thm 3.1) · 4 factorisation, paired boxes (Lemmas 4.1–4.2) ·
5 determinant cuts · 6 lattice coordinates · 7 weighted Hilbert bounds · 8 quartic geometry (Props 8.1, 8.2) · 9 curves · 10 parameters
(Prop 10.1, Table 1) · 11 the large-prime estimate (Prop 1.4) · 12 the cyclotomic example · Appendix A the exact certificate.
(TeX files: 12-certificate.tex is Appendix A, 13-cyclotomic.tex is §12.)

## replay/ — kernel replay of OpenAI's Lean (openai/math @ 1581d4c lean/, Lean v4.34.1, Mathlib d13f23b7)
- Closure `all_order.txt`: 63 modules under OAI/NumberTheory/PowerFree (23,269 lines), external = Mathlib only (computed by
  `closure.py`, which scans every line of every file for imports). The directory's git tree is da55b200 at adc7f12 (FC's pin) and at
  1581d4c; Main.lean blob 4f47d76e and the manuscript blob 67d63397 are the same at both.
- `drive.py` (lake-free, DAG-parallel, W=4): 63/63, 0 errors, 0 warnings, wall 12:05:12–12:22:34Z (17 min 22 s; 981 s summed over
  modules), peak RSS 6.8 GiB; `modules.tsv`, `driver.log`, per-module logs `logs/module_logs.tar.xz`. Mathlib oleans from
  `lake exe cache get` (`cacheget.sh`, `cacheget.out`).
- `post.sh`: comparator module compiled; probes `probe/Cmp_PowerFreeValues.lean` (imports the challenge) and
  `probe/Ax_PowerFreeValues.lean` (imports the solution, `--trust=0`), printing `pp.all` blocks for `allDegrees` and its seven
  definitions (`probes.json`). `statement_match.py` → `statement_match.txt`: ALL_MATCH_STD_SORRYSEEN, 8 MATCH / 0 MISMATCH;
  `allDegrees` on exactly [propext, Classical.choice, Quot.sound]; sorryAx seen on the challenge theorem. `probe/Neg.lean`: planted
  sorry → sorryAx (`logs/neg.log`).
- Matcher mutation test `mutate_matcher.sh` → `mut/MUTATIONS.txt`: unmodified 0; def_powerfree_dvd, count_Icc, density_littleO,
  thm_degree, extra_axiom, cmp_no_sorry → 1; missing_block, missing_log → 2 (a mutation that does not change its input is refused).
- `bridge.sh` (after the bridge steps) runs `leanchecker --fresh Bridge978` (Mathlib + the 63-module closure + our bridge, re-checked from
  stored terms): rc 0 after 3,502 s, peak RSS 8.2 GiB (`logs/leanchecker_fresh.log`); missing-module control rc 1
  (`logs/leanchecker_missing.log`). `steps.tsv` = every step's rc and seconds. Two earlier third-party Comparator replays accepted the same
  challenge (carlostoledo1891/cert-machine, 10 Oct, Lean kernel + nanoda; nealmcb/openai-math-lean-tooling, 11 Oct) — ours is the third.
- Source scan (seat L + ours): the only `sorry` is the challenge's; no axiom/opaque/implemented_by/extern/unsafe/native_decide/meta
  code; zero `set_option` in the closure; five `decide +kernel` (QuarticComponents, ∀ j : Fin 100 over ℚ). The lakefile's top-level
  `run_cmd` (git clone + patch of 24 dependencies) touches no package in this closure.
- `post.log` records one void pass: the first bridge compile failed (two small errors), so that pass's mutants and leanchecker ran
  against a missing olean; the steps were removed from `steps.tsv`, the bridge fixed, and every bridge step re-run.

## bridge/ — ours
- `Bridge978.lean` (imports Mathlib + OpenAI's Main; 330 lines): helper lemmas (PowerFree ⇔ FC's Powerfree on ℤ; FC's local condition
  ⇒ LocallyAdmissible; Gauss; density ⇒ infinite; X⁴+2 irreducible by Eisenstein at 2), then FC's `erdos_978.variants.sub_two`,
  `erdos_978.parts.ii`, `erdos_978.parts.iii` VERBATIM from `FC_978.lean` (google-deepmind/formal-conjectures @ a7b87c8d; `FC_SHA.txt`),
  plus `erdos_978.parts.ii_density` (FC's own `Set.HasDensity` with OpenAI's Euler product, hence `HasPosDensity`; definitions copied
  verbatim from `FC_Density.lean`) and `parts_ii_without_extra_hypotheses` (no k ≠ 2^l, no sign condition). `Powerfree` copied verbatim
  from `FC_Powerfree.lean`. `verbatim_check.py`: `verbatim.log` 7/7 MATCH rc 0; `verbatim_mut.log` (n⁴+2 → n⁴+1) rc 1.
- `AxBridge.log` (`--trust=0`): [propext, Classical.choice, Quot.sound] on all seven bridge theorems. Controls: `BridgeMutSorry` (sorry in
  the density ⇒ infinite lemma) → `AxMutSorry.log` sorryAx on all three FC theorems; `BridgeMutExp` (conclusion exponent d−3) fails at the
  step that uses the exponent; `BridgeMutNoLocal` (local hypothesis dropped — false, by DeepMind's degree-6 polynomial) fails where local
  admissibility is supplied. Elaborated under OpenAI's toolchain (Lean 4.34.1), not FC's pin (4.33.1).

## compute/ — ours (label (d); illustrations, they test nothing about the theorem)
- `euler.gp` → `euler.out`: ρ(p²) by brute force mod p² for p < 2000, #roots mod p beyond; c(x⁴+2) = 0.756684002977… and
  c(x⁴+1) = 0.980817474478… truncated at p ≤ 2·10⁷ (true values lie below these by a few 10⁻⁹); direct counts by full factorisation
  to 2·10⁵: 151,346 and 196,180.
- `tail.gp` → `tail.out`: n ≤ 10⁵ with p² | f(n) for a prime p > n: x⁴+2 → n = 2 (p = 3), n = 97 (p = 179); x⁴+1 → none.
  Seat M2's run to 10⁶ (`seats/M2_work/out_w*_c*.txt`, `sqf.gp`) finds the same two and none else; its counts: 756,674 and 980,831.
- `count1e5.gp` → `count1e5.out`: factoring counts to 10⁵ for both polynomials (75,670 / 98,090; fills the n⁴+1 cell the July run lacked).
- `sieve_count.py` → `sieve_count.out` (second instrument, no factoring: sieve by every p ≤ 10⁶ on Hensel-lifted roots mod p²):
  S(10⁵) = 75,670 / 98,090, S(2·10⁵) = 151,346 / 196,180, S(10⁶) = 756,674 / 980,831 — equal to every factorisation count (ours, M2's,
  and our July report's certified 75,670). Exact only together with the tail census (a prime p > 10⁶ with p² | f(n), n ≤ 10⁶, would have
  p > n). Mutation `sieve_count_mut_nolift.py` (no lift) → 65,353 / 84,624 at 10⁵: the agreement is not automatic.

## seats/
- `BRIEF.md` (M1, M2, L, W), `B_BRIEF.md` (blind read). Reports: `M1_report.md` (§§2–4, 10, App. A, 11; exact certificate recomputation
  + 6 mutations — HOLDS AS READ), `M2_report.md` (§§5–9, 12; evaluation-rank checks of every Hilbert claim, the 25 quintics, counts to
  10⁶ — HOLDS AS READ), `L_report.md` (the Lean as source: statement fidelity, architecture, the shorter route — HOLDS AS READ),
  `W_report.md` (Erdős's three sources, priority, ZCJ withdrawn 15 Oct, Carella's constants, the status record — GAP at Cor 1.3 d = k+1,
  minor, fillable; HOLDS on the rest), `B_report.md` (blind read of the page: 6 MUST-FIX incl. a false "first replay" claim, 10 SHOULD-FIX, NITs — all MUST-FIX and SHOULD-FIX applied; `entry/entry978.js.pre-blind` is the version it read). Third-party downloads are not redistributed
  (`THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256`).

## live/
- The problem page, forum thread, claims tab and LaTeX view fetched 22 Oct 2026 through our Hetzner box; teorth DB extract.

## entry/
- `body.html`, `reading.html`, `m2_items.html`, `numbers.html`, `mkentry.py` → `entry978.js`; `apply978.py` (splices the entry,
  OAI_CLAIMS[978], LEAN_LABEL own978, CLOSED_BY_LITERATURE, HEADLINES; each anchor asserted once), `smoke978.mjs`, `render.mjs`,
  `entry_rendered.txt`; `fc_issue_title.txt`, `fc_issue_body.md` (staged on Handoff, not posted).
