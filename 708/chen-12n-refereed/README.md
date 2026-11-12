# Erdős #708 — Chen's g(n) ≤ 12n refereed and replayed; the K_{2,t} window at every size (2026-11-12)

Page: https://erdosproblemaday.com/day/708-chen-12n-refereed-and-a-k2t-window-at-every-size

## Claims and labels
1. **Statement audit (a).** `Erdos708Statement.g_le 12` (chy4pro/erdos-708-explicit-upper-bounds, lean/Erdos708/Statement.lean,
   commit dc150fd) is g(n) ≤ 12n for the problem as posed, under the "at most g(n)" reading.
2. **Kernel replay (d).** See lean-replay/ (steps.tsv, logs, scripts). Mathlib de5ce8a9 oleans came from the Mathlib cache;
   every Erdos708 module was compiled here from source (so its proofs were kernel-checked here); `leanchecker --fresh` was not run.
3. **Referee (Claude seat).** referee_claims/REPORT.md: long-interval theorem, §17 arithmetic, statement — hold; barrier
   (Prop 18.9) holds in the atom form but its 21-prime instance does not refute the w_z form the reduction uses; a 60-prime
   cluster (1049..1483) does (182.9 > 145). Recomputed independently by ours/barrier/wz_barrier.py (23 ≤ 46; 1829/10 > 145).
4. **Ours: the K_{2,t} placement for every t (a)(b)(d).** ours/LEMMA.md. g(2t) ≥ 3t−1 and g(2t+1) ≥ 3t, i.e.
   g(n) ≥ ⌊3n/2⌋ − 1 for every n ≥ 4 (primes from the prime number theorem); explicit instances for t ≤ 14 in ours/certs.json,
   each solved exactly. Referee: referee_lemma/REPORT.md (HOLDS WITH FIXES, all applied).

## Controls
- ours/exact.py vs plain subset enumeration: 0 mismatches on 400 random instances; mutation_test.py: two planted bugs caught
  258/400 and 392/400.
- referee_lemma/refsolve.py: separate DP + HiGHS integer programme, 0 mismatches vs brute force on 600 instances; agrees on
  every certificate.
- Red control: ours/k2t.py (naive centring) at t = 9, where q_u² − m = 36 < q_u, lets a q_u² multiple into the window and
  gives 25 < 26 (ours/k2t_run.log).
- Chen's printed instances reproduced: {10,12,15,20}@50 → 5; {5,10,12,15,20}@50 → 6; K_{2,2} (59,61;71,73)@18652287 → 5;
  K_{2,3} (67,73,79;97,101)@3785449127 → 8.

## Reproduce
    cd ours && python3 exact.py && python3 k2t2.py 14 && python3 certs.py && python3 mutation_test.py
    cd ours/barrier && python3 wz_barrier.py
Lean: clone chy4pro/erdos-708-explicit-upper-bounds at dc150fd; cd lean; lake exe cache get; build per lean-replay/coord.py
(certificate modules one owner each, ≤ 3 at a time), then `lake build Erdos708.FinalCheck` and
`lake env lean Erdos708/FinalCheck.lean` (success = no output).

## Not ours
The 12n theorem, its proofs and Lean (H. Chen with GPT-5.6 / GPT-6 / Qwen, Claude orchestrator and referees); the K_{2,t}
family and its count (Chen §19, repo version); the 1959 construction and count (Erdős–Surányi); the "for every θ < 1"
assertion (referee in Chen's pipeline, run37, unproved there).
