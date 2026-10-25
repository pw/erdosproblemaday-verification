# Erdős #952 — OpenAI family 28 "Bounded-Step Walks on Gaussian Primes" (dated 26 Sep 2026; public 6 Oct), refereed 2026-10-22

Claim (Theorem 1.1): for every finite real D there is a finite B_D such that every connected component of G_D (Gaussian primes,
edges at distance ≤ D, axis primes included) has at most B_D vertices; hence no infinite walk through distinct Gaussian primes has
bounded steps (the Gaussian moat problem; Gordon 1962 per Gethner–Stark; Erdős #952). Reduced (Prop 2.1, periodicity) to Theorem 1.2:
a finite set P_D of split primes p ≡ 1 (mod 4) such that A(P_D) (Gaussian integers divisible by neither factor of any p ∈ P_D) has
no infinite D-walk; proved by an entropy/information argument (§§3–8). B_D is not explicit. The theorem, proofs and Lean are OpenAI's.
The uniform form is Gethner–Stark's 1997 conjecture and Vardi's 1998 Conjecture 1.2. Others built the Lean before us (plasma-ai 7 Oct,
cert-machine 10 Oct, RichardGeorgeDavis 12 Oct). Ours: the replay + controls (a replication), the bridge to Formal Conjectures + controls,
the readings, the miniature computation (its first case reproduces Vardi 1998 §7: 580).
Entry: https://erdosproblemaday.com/day/952-openai-gaussian-moat-refereed

Seats: the 00:00Z erdos seat (2026-10-22) ran the replay, the bridge, seats G/I/L and the miniature, then died on the Team-seat session
limit at ~00:24Z; the 03:00Z seat re-ran seats S and W, ran the blind read B, the second-instrument BFS over all 154 sets, and shipped.

Paper: `paper/SOURCE.txt` (sha256 of the PDF + TeX we read; openai/math @ 1581d4c; not redistributed). PRINTED sections: 1 problem ·
2 periodicity (Prop 2.1) · 3 arithmetic/entropy (3.1, Lemmas 3.1–3.3) · 4 enrichment (Lemmas 4.1–4.3) · 5 coverage transfer (Lemma 5.1,
Thm 5.2) · 6 schedule (Lemma 6.1, Prop 6.2) · 7 zero avoidance (Prop 7.1) · 8 budget (Lemma 8.1, proof of Thm 1.2).

## replay/ — kernel replay of OpenAI's Lean (openai/math @ 1581d4c lean/, Lean v4.34.1, Mathlib d13f23b7)
- Closure `all_order.txt`: 41 modules under OAI/NumberTheory/GaussianMoat (12,703 lines), external = Mathlib only. The directory's git
  tree is c84262a9 at adc7f12 (FC's pin), fd4aeeb and 1581d4c; comparator .lean/.json, docs/028.md, the preprint, toolchain and
  manifest are unchanged across them. `ESTIMATE.md` = the estimate written before spending CPU.
- `drive.py` (lake-free, DAG-parallel, W=4): 41/41, 0 errors, 7 min 39 s; `modules.tsv`, `driver.log`, per-module logs
  `logs/module_logs.tar.xz`. Mathlib oleans from `lake exe cache get` (`cacheget.sh`, `cacheget.out`).
- `post.sh`: comparator module compiled; probes `probe/Cmp_GaussianMoat.lean` (imports the challenge) and `probe/Ax_GaussianMoat.lean`
  (imports the solution, `--trust=0`), printing `pp.all` blocks for the theorem and its five definitions (`probes.json`).
  `statement_match.py` → `statement_match.txt`: ALL_MATCH_STD_SORRYSEEN, 6 MATCH / 0 MISMATCH; `fullMain` on exactly [propext,
  Classical.choice, Quot.sound]; sorryAx seen on the challenge theorem. `probe/Neg.lean`: planted sorry → sorryAx (`logs/neg.log`).
- Matcher mutation test `mutate_matcher.sh` → `mut/MUTATIONS.txt`: unmodified 0; def_irreducible, dist_token, uniform_token,
  extra_axiom, cmp_no_sorry → 1; missing_block, missing_log → 2 (a mutation that does not change its input is refused).
- `post.sh` also runs `leanchecker --fresh Bridge952` (the 41-module closure + Mathlib + our bridge): rc 0 after 3,480 s, peak RSS
  8.2 GiB (`logs/leanchecker_fresh.log`); missing-module control rc 1 (`logs/leanchecker_missing.log`). `steps.tsv` = every step's rc
  and seconds (the bridge steps are in `bridge/bridge.sh`).

## bridge/ — ours
- `Bridge952.lean` (imports Mathlib + OpenAI's Main): `dist_toComplex_eq_sqrt_norm`; `erdos_952` with FC's statement VERBATIM from
  `FC_952.lean` (google-deepmind/formal-conjectures @ 3b7c94ec; sha256 in `FC_SHA.txt`; last change to the file 7db2ea3, 14 Oct),
  proved from `OAI.GaussianMoat.fullMain.1` with D = √C; `erdos_952_uniform` from `fullMain.2`. `verbatim_check.py` (whitespace-
  normalised source text, not elaborated terms): `verbatim.log` rc 0, `verbatim_mut.log` (Prime→Irreducible) rc 1. `AxBridge.log`:
  standard axioms on all three theorems. Controls: `BridgeMutSorry` (fullMain's use replaced by sorry) → `AxMutSorry.log` sorryAx;
  `BridgeMutStep` (step bound < C + N(x n), true of the increasing rational primes ≡ 3 mod 4 for large C) fails at the inequality step;
  `BridgeMutNoInj` (injectivity dropped; a constant sequence satisfies it) fails at the injectivity step. Elaborated under OpenAI's
  toolchain (Lean 4.34.1), not FC's pin (4.33.1). FC's PR #6898 reviewer notes list "Erdős 952 (norm vs distance)" as a routine transport
  not in the linked proof; this file is that transport. No other public proof of FC's statement found (seat W §5b).

## compute/ — ours (exact; label (d); a sanity check)
- `sieve_perc.c` (first instrument: union-find on the torus (ℤ/Qℤ)² with lift offsets; INFINITE iff a cycle lifts to a nonzero
  translation) and `bfs_check.py` (second instrument: BFS with lift positions; independent code). `scan.py` → `scan_R1.log`
  (D=1: first blocking set by increasing Q is P={5,13}, Q=65, max component 580), `singles_R1.log` (no single split prime < 65 blocks),
  `scan_R2_R4.log` (D=√2, 2: none of 154 sets with Q ≤ 4000), `spotcheck.log` (both programs on five sets).
- Seat B (blind read) found the scan's "154 sets with Q ≤ 4000" were only those built from split primes < 400; there are 416.
  `scan_all416.py` → `scan_all416.log`: sieve_perc over all 416 sets: D=√2 and D=2 none finite (min density 0.4831); D=1, 10 finite
  (each contains 5 and 13 or 17).
- The second instrument over the whole 154-set population at D ∈ {√2, 2}: `bfs_all.py` → `bfs_all.log` (stopped by hand at Q = 2465 for
  speed), `bfs_one.py`/`bfs_slice.py` → `bfs_R4.log`, `bfs_R2_s*.log`, `bfs_R4_s*.log` (three of the D=√2 slices hit their 4 GB cap —
  MemoryError in the log), `bfs_sets.py` → `bfs_R2_rest_{a,b}.log` (the five unfinished sets, 8 GB cap). `bfs_summary.py` →
  `BFS_SUMMARY.txt`: 154/154 covered at both D, 0 finite, 0 disagreements with sieve_perc; it exits 1 on a flipped line (tested).
- `spotcheck_R1.log`: both programs at D=1 on {5,13} (580) and {5,13,17} (80). `vardi130.py` → `vardi130.log` (seat W's script):
  Z[i] prime to 130 at step ≤ √2 and A({5,13}) at step 1 both have largest component 580.
- The D=1, P={5,13} case is NOT new: under z ↦ (1+i)z + 1 it is Gethner–Stark's 1997 √2 moat sieved by 65+65i, and Vardi 1998 §7
  counts its largest component as 580. Seat W's `seats/W_work/scripts/vardi130.py` checks the correspondence (580 both ways).
- `july_checker_rerun.log`: our July report's checker re-run 2026-10-22 (G_√2 maximum component 100; Vardi's 71 for numbers prime
  to 390 reproduced on the way).

## seats/
`BRIEF.md` (one brief, printed numbering); `G_report.md` (§§1–4), `S_report.md` (§§5–6, incl. seat I's five imports from §6, the
quantifier order, explicit-inequality checks with negative controls), `I_report.md` (§§7–8), `L_report.md` (Lean vs paper),
`W_report.md` (sources, priority, live states, what is ours) — all HOLDS AS READ; `main_reading.md` (the 00:00Z seat's own read);
`B_BRIEF.md` + `B_report.md` (blind read of the entry page against these files: 4 MUST-FIX, all applied — Jordan–Rabung's 48 is an admissible-set bound, not a walk bound for G_√2 (B_work/jr48b.py: a 60-step walk on distinct Gaussian primes through 1+i, re-checked independently; our July report corrected in runs/erdos952_wavew024.md); 154 vs 416 sets; the hole/label lists unified; PR #6898's notes are its author's, not reviewers'). Work dirs `G_work/`, `I_work/`, `S_work/`
(S_work/checks3.py is WRONG — 30-digit cancellation — superseded by S_params.py), `B_work/`; W's small text extracts in `W_src/`;
third-party downloads listed by hash only (`THIRD_PARTY_DOWNLOADS_NOT_REDISTRIBUTED.sha256`). `MODEL_RECEIPTS.txt`: served-model
fields per seat transcript where the transcript survives.

## live/
erdosproblems.com/952 + forum thread + proof-claims tab (00:1xZ and 03:0xZ, 22 Oct, via the Hetzner box; "Proof claims (0)", last
edited 8 Apr 2026, no status label rendered) and the teorth database extract (952: open, last_update 2025-08-31).

## entry/
`entry952.js` (the entry as spliced), `apply952.py` (splice; refuses placeholders), `headline.js`, `lean_label.txt`, `closed_by.txt`,
`smoke952.mjs`, `render.mjs`, `make_bundle.sh`, `fc_issue_title.txt` + `fc_issue_body.md` (staged on Handoff, not posted).
