# #970 (+ #687) — OpenAI's Jacobsthal bound, refereed; Lean replayed; FC bridges

erdosproblemaday.com, /day/970-openai-jacobsthal-quadratic-refereed, 2026-10-23 (00:00Z seat began; 03:00Z seat finished after the
first seat hit a subscription session limit at ~00:20Z).

## Claim (OpenAI's, not ours)
OpenAI, "A quadratic bound for Jacobsthal's function", dated 25 Sep 2026, 83 pp., github.com/openai/math family 021
(`paper/SOURCE.txt`: commit and SHA-256 of every source file; the paper is not redistributed here).
Theorem 1.1: h(k) ≤ C·k²/(log log 3k)² for every k ≥ 1. Theorem 1.2: for large z and any classes a_p (p ≤ z),
#{n ≤ Y : n ≢ a_p ∀p ≤ z} ≥ c·Y·V0/B², Y = ⌊z²/L²⌋, L = log z, w = L/(log L)², B = L/log w, V0 = ∏_{p≤w}(1−1/p).

## What is ours
1. A kernel replay of OpenAI's Lean (`replay/`) — not the first (cert-machine, nealmcb ran Comparator earlier; see the page).
2. `bridge970/Bridge970.lean` — Formal Conjectures' `erdos_970` and `erdos_970.variants.iterated_log` (verbatim) from OpenAI's
   theorems. `erdos_970` was already done by 30k30/scholia (11 Oct); the iterated_log variant is new here (one step).
3. `bridge687/Bridge687.lean` — Y(x) ≪ x²/(log x · log log x)² for FC's Erdős 687 `Y` (verbatim defs), from OpenAI's
   `erdos_970_iterated_log` + Mathlib's Chebyshev bound; FC's `erdos_687.parts.ii` (also by 30k30) and
   `erdos_687.variants.iwaniec` (no linked proof in FC) as corollaries; `Bridge687b.lean` proves draft PR #7442's
   proposed `erdos_687.variants.quadratic_log` (Y ≪ (x/log x)²).
4. The reading (`seats/`) and the sanity check against Banks–Ford–Tao's exceptional-zero obstruction (on the page).

## Chain and controls
- replay/: `driver.log`, `modules.tsv` (850 modules, rc/errors/maxrss/wall/sha each), `steps.tsv`, `post.log`.
  850/850, 0 errors, largest single module 7.35 GiB, Lean v4.34.1, Mathlib d13f23b7. `#print axioms` (--trust=0) = [propext, Classical.choice,
  Quot.sound] for both comparator theorems (`logs/ax_*.log`). pp.all statement match 3/3 + 3/3 (`statement_match.txt`);
  `matcher_mutations.py` → `matcher_mutations.out`: 7/7 mutants caught. Planted sorry → sorryAx (`probe/Neg.lean`).
  `leanchecker --fresh` (over Bridge970 = Mathlib + 850 + bridge) rc 0, 3,703 s, peak 8.6 GiB; missing-module control rc 1.
- scan/: `holes_out.txt` — 0 sorry/admit/axiom/native_decide/implemented_by/extern/unsafe/opaque/set_option over 850 files;
  1 `partial def` + 1 `syntax` + 1 `elab_rules` (PrimeNumberTheoremAnd's additive_combination tactic), 1 scoped `attribute … in`.
- bridge970/: verbatim (FC 93e94653; unchanged at c83a94d7) MATCH, mutated copy MISMATCH; axioms std; BridgeMutSorry →
  sorryAx; BridgeMutExp / BridgeMutK0 fail to compile.
- bridge687/: verbatim vs FC c83a94d7 (`GreensOpenProblems/46.lean`, `ErdosProblems/687.lean`) MATCH 4/4, mutated copy rc 1;
  `Ax687.log` std axioms on all four theorems; `Mut_sorry` → sorryAx on all four; `Mut_strong` (asks for an extra log log x)
  and `Mut_cheb` (Chebyshev 2x/log x → x/log x) fail; `lc.log`: leanchecker --fresh over Bridge687 (Mathlib + OpenAI's 850 + bridge) rc 0, 3,753 s, peak 8.6 GiB; missing-module control rc 1. `Bridge687b.lean` (PR #7442's quadratic_log, verbatim vs FC_PR7442.diff @ ecd8e11c) compiled + std axioms (`Ax687b.log`), not in the leanchecker pass.
- compute/: `loss_terms.py` (first-omission loss terms of Prop 6.3, quadrature + MC + perturbed control; tail line overflows),
  `jprim.c` (j(P_k), k ≤ 9). Small-value table on the page from Ziller 2019 Table 2 + Hajdu–Saradha 2012.
- seats/: brief, addendum, the four reports (R1 §§2–6, R2 §§7–9, R3 §§10–11 + appendices + statement, W world/citations),
  and the blind read (`B_report.md`; its MUST/SHOULD fixes are applied on the page; `page_text_as_read_by_B.txt` is the pre-fix text).

## Reproduce
`replay/drive.py` (module-by-module build against `lean_path.txt` paths), then `post.sh`; `bridge970/bridge.sh`;
in `bridge687/`: `source lean_env.sh; lean Bridge687.lean -o out/Bridge687.olean; lean --trust=0 Ax687.lean;
python3 verbatim_check.py; python3 verbatim_check.py --mutate`. Paths are this machine's; adjust LEAN_PATH.
