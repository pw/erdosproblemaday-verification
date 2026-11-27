# Erdős #36 (minimum overlap): reader "Hallllllll"'s 9,408-step upper bound, checked — 27 November 2026

Claim checked: the step function h in inputs/construction_v1.0.0.json (9,408 equal cells on [0,2), heights a_i/D,
D = 52428700000000) has largest overlap max_s ∫ h(x) g(x−s) dx (g = 1 − h on [0,2), 0 elsewhere) exactly
U = 2462273619527794579322422405079 / 6465103708838880000000000000000 ≈ 0.38085601258978, attained only at s = −571/1176.
By the upper half of Swinnerton-Dyer's theorem (proof in Haugland 1996) U bounds the minimum overlap constant. Label (d) for U,
(b) for the bound on Erdős's constant. Reader's repository: github.com/Hallllllll/erdos36-minimum-overlap-lean4, tag v1.0.0
(commit 045d628a3db3becc39671bd18af68f91ad6931c8); Zenodo 10.5281/zenodo.24575270.

Chain
- scripts/overlap_eval.py + run_main.py (referee seat): all 18,817 grid-shift values T_k exactly (20-bit split convolution);
  logs/run_main.log. Float FFT third route in the same log (max diff 2.2e-16).
- scripts/kronecker.py (main seat): the same values by one big-integer product; logs/main_seat_kronecker.log.
- Both: max at k = −2284 only; second best k = −3052 lower by 2.7e-13; side conditions exact.
- scripts/controls.py, logs/controls.log: Haugland 2016 (19- and 51-step), AlphaEvolve 95-step, negative controls.
- scripts/parse_data_lean.py, logs/lean_data_crosscheck.log: the heights and 18,815 certificate values inside the reader's
  Lean source (Overlap/Data.lean) equal the JSON and our T_k.
- scripts/parent.py, logs/parent.log, inputs/compute_substrate_parent_2026-11-25.txt: the Commonplace parent (4,704 cells over
  524287, 0.380856013736) exactly; gain P − U = 1.1453e-9 exactly; 5,396 cells differ from the parent doubled.
- inputs/willk30_pr419_C1b_trackA_18816_record.json (teorth/optimizationproblems #419): scored by scripts/kronecker.py
  (logs/willk30_18816_kronecker.log) and by the world seat's scripts/c1b_exact.py: exactly
  270730612195671389820648367/710848381933401954727231488 ≈ 0.3808556355.
- logs/ci_api.log (reader's CI on 045d628) and logs/reader_ci_31ded31_full.log (+ excerpt) for the later commit 31ded31:
  the READER'S instrument, read not rebuilt. We have NOT built either commit.
- referee_report.md: the hostile referee seat's report. submission/44a4n7.json: the submission (contact fields removed).
Scripts hard-code /home/exedev/MathDyad/subs-1127/36 paths; point them at this folder's inputs/ to re-run.
