# Erdős #371 (+ #928) — OpenAI family 012 "The joint Dickman law for consecutive integers" (dated 24 Sep 2026; public 6 Oct), refereed 2026-10-22

Claim (Theorem 1.1): for every fixed a, b ∈ (0,1), (1/X)·#{2 ≤ n ≤ X : P⁺(n) ≤ n^a, P⁺(n+1) ≤ n^b} → ρ(1/a)ρ(1/b) through all real X
(ordinary natural density). Corollary 1.2: P⁺(n) < P⁺(n+1) has natural density 1/2, and so does the reverse ordering (Erdős #371,
Erdős–Pomerance 1978). Prior: Teräväinen 2018 (log density), Tao–Teräväinen 2019/2026 (almost all scales), Wang 2021 (conditional on EH
for friable integers). The theorem, proofs and Lean are OpenAI's. Others built the Lean first (plasma-ai wiki, 7 Oct, self-reported).
Ours: the replay + controls (a replication), the dependency walk, the readings, the FC bridge (erdos_371 verbatim) and #928 as posed
in Lean (jbaelaw/Erdos928 formalized the implication from a hypothesis first, 9–10 Oct), the α-question remark, the counts.
Entry: https://erdosproblemaday.com/day/371-openai-joint-dickman-law-refereed

Seat: the 06:00Z erdos cron seat (2026-10-22, Opus 5.5, Team seat 3/yt3). Referee seats A (§1.2, §§2–4), R (§§5–11), L (Lean vs paper),
W (world), all Opus 5.5 (seats/MODEL_RECEIPTS.txt); blind read B on the rendered page.
The 06:00Z seat hit the Team-seat session limit at 07:22Z before its blind read reported. The 09:00Z erdos cron seat (same model, same
seat) closed the leanchecker sentence when the run landed (08:07Z), re-ran blind read B, applied its fixes and shipped.

Paper: `paper/SOURCE.txt` (sha256 of the PDF + TeX we read; not redistributed). PRINTED sections: 1 intro (Thm 1.1, Cor 1.2) · 2 labels
and short averages (Lemmas 2.1, 2.3, Thms 2.4–2.5, Lemma 2.6) · 3 arithmetic preliminaries · 4 amplification · 5 independent-site kernel
· 6 second moment · 7 channels · 8 endpoint features · 9 sampling · 10 vanishing of the main energy · 11 marginals, joint law, ordering.

## replay/ — kernel replay of OpenAI's Lean (openai/math @ 1581d4c lean/, Lean v4.34.1, Mathlib d13f23b7)
- Closure `all_order.txt`: 1,837 modules = PaperMain's closure (1,836 modules / 221,509 lines; OAI 1,792 incl. 1,456 under JointDickman)
  + the one-line umbrella `OAI.NumberTheory.JointDickman` that imports it (seat B, `seats/B_work/closure_check.py`; PrimeNumberTheoremAnd @c39a751 +
  OpenAI patch 28; StrongPNT @2f5835c + OpenAI patch 7; LeanArchitect @468e8f5 9). `SOURCES.sha256` = sha256 of every OAI source file.
  `ESTIMATE.md` = the estimate written before spending CPU.
- `drive.py` (lake-free, DAG-parallel, W=5): 1,837/1,837, 0 errors, ≈4.0 CPU-h, peak 7.35 GiB/process; `modules.tsv`, `driver.log`,
  per-module logs `logs/module_logs.tar.xz`. ⚠ The first run (`build 1` in steps.tsv) stopped at 1,576/1,834 on
  PrimeNumberTheoremAnd.Fourier: OUR closure script (`scripts/closure.py`/`closure2.py` v1) stopped parsing a patched file's imports at
  its leading comment block and missed 3 modules (Sobolev, SmoothExistence, Mathlib.Analysis.Asymptotics.Asymptotics; the v1 list is
  `all_order_v1_parser_bug.txt`). Parser fixed (strip nested block comments), closure regenerated, `drive.py` resumed (`after2.sh`).
- `post.sh`: comparator module compiled; probes `probe/Cmp_JointDickman.lean` (imports the challenge) and `probe/Ax_JointDickman.lean`
  (imports the solution, `--trust=0`) print pp.all blocks for 3 theorems + 7 definitions (`probes.json`). `statement_match.txt`:
  ALL_MATCH_STD_SORRYSEEN, 10 MATCH / 0 MISMATCH; solution axioms exactly [propext, Classical.choice, Quot.sound]; sorryAx on the
  challenge theorems. `probe/Neg.lean`: planted sorry → sorryAx.
- `mutate_matcher.sh` → `mut/MUTATIONS.txt`: unmodified 0; rho_sign, icc_start, threshold_base, extra_axiom, cmp_no_sorry → 1;
  missing_block, missing_log → 2. All as wanted.
- `probe/Deps.lean` → `logs/deps.log`: kernel walk (types + values, opaque included) from the three theorems: ~10.5k non-Mathlib constants
  in 1,626–1,627 modules; none of RealShortIntervalInput / ComplexShortIntervalInput / MultiplicativeExponentialInput /
  CharacterDistanceInput / MRTShortExponentialInput / MRTLiouvilleShortInput; the PublishedInputs props reached are each instantiated
  by a proof (Ford-type sieve, Selberg–Delange, Siegel–Walfisz-type, 2× Mertens, McDiarmid, Chebyshev, finite-bin distribution).
- `leanchecker.sh`: `leanchecker --fresh Bridge371` (whole closure + our bridge) — exit 0 after 3,629 s, peak RSS 8.9 GiB
  (`logs/leanchecker_fresh.log`, steps.tsv row `leanchecker_fresh`); missing-module control rc 1 (`logs/leanchecker_missing_control.log`).

## bridge/
- `BridgeCore.lean`: verbatim FC `Set.partialDensity` / `Set.HasDensity` (FC @ 3b7c94ec, FC_Density.lean) + transfer lemma
  (|FC partial density − OpenAI realDensity| ≤ 2/b) + #928 sandwich, all CONDITIONAL on OpenAI's JointDickmanLaw / IncreasingOrderLaw
  (compiled first against the 5-module Ordering slice; `AxCore.lean`: standard axioms).
- Re-checked 09:3xZ: FC head a9326184 (22 Oct 08:27Z) differs from 3b7c94ec only in ErdosProblems/1212.lean; 371.lean byte-identical, no 928.lean.
- `Bridge371.lean` (generated by `make_final.py`): the same + `Erdos371.erdos_371` (verbatim FC statement) and `EPAD371.erdos_928`
  (+ `_exists`) instantiated with OpenAI's unconditional theorems. `AxBridge.log`: standard axioms. Mutants `BridgeMut{Value,Strict928,
  DensityDef}` fail (logs). `verbatim_check.py` → `verbatim_check.log`: 3 MATCH, rc 0; each targeted one-token mutation rc 1.

## compute/
- `lpf_count.c` (segmented sieve, division) → `out_1e10.txt` (583 s, 6 threads): inc 4,999,983,166, dec 5,000,016,833 for 2 ≤ n ≤ 1e10;
  checkpoints {1,2,5}·10^k; `hist_1e10.bin.xz` = 101×101 histogram of (⌈100u⌉,⌈100v⌉) per decade (`readhist.py`).
- `lpf_numpy.py` (ascending-prime overwrite, no division) → `out_numpy_1e8.txt`, `out_numpy_1e7.txt`: identical checkpoints to 1e8;
  16 joint counts identical at 1e7. Third instrument: our July `runs/erdos371_wave8y.md` census (A(X) = ours + 1, counts n = 1).
  OEIS A070089 b-file (1,000 terms) identical.
- `rho_check2.py`: OpenAI's `rho` definition (grid Picard + mpmath) vs Heun ODE vs literature (ρ(2), ρ(3), ρ(4), ρ(5)): ~1e-9.
- `alpha_count.c` → `out_alpha_1e9.txt` (Erdős's α-question counts, α = k/20, margin 1e-9, NEAR_TIES 0); predictions from the product
  law by `alpha_predict.py` → `out_alpha_predict.txt`; table in `entry/alpha_table.html`. `indep_ratio.py` reproduces `indep_ratio_1e10.txt`.
- `joint_table_1e10.txt`, `indep_ratio_1e10.txt`.

## seats/ — BRIEF.md (+ B_BRIEF.md), main_reading.md (coordinator: §1, §11), A/R/L/W/B reports, receipts.
- B (blind read, 09:0xZ seat): 6 MUST-FIX + 13 SHOULD-FIX + 15 NIT; every MUST-FIX and SHOULD-FIX applied, and all NITs except N4 (the
  banner's 'family 12' is the site-wide format), N10 and N14/N15 (bundle-side notes; the 11,804 instances were unseeded, harmless since the
  identity is algebraic; lpf_numpy MemoryError came after its last checkpoint; rho_check2's one-short control cannot fail) — `entry/fixB/apply_B.py`.
  B's scripts in `seats/B_work/` include the exact-integer α recount at 10^6 (the table's 10^6 column had no output file before).
