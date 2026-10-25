# Hostile referee report — check778c.cpp (Erdős #778, (1:2) clique game, K_9 certificate)

_Status: IN PROGRESS (written incrementally)._

## what you ran (log, appended as I go)
- Read check778c.cpp (144 lines) and nautytest.cpp (56 lines) in full.
- nauty build: header `nauty.h` unconditionally `#define USE_TLS` -> `TLS_ATTR _Thread_local`, `HAVE_TLS 1`; `readelf -s libnauty.a` shows 488 TLS symbols incl. `workperm`, `canonlab`, `workspace`. The only non-TLS *mutable* statics are in gtnauty.o / naugroup.o / nautycliquer.o (not on densenauty's path); nauty.o / naugraph.o / nautil.o have only const tables + `labelorg`/`nauty_kill_request` globals (never written by densenauty). Thread safety of `canon()` holds as built.
- Process table at start: no check778c running; `solve778 --n 9 --mode clique --nocut` running (not touched).
- `nautytest`: "all good: 2000 transports verified / oracle: 400/400 pairs agree (key-equal 102, isomorphic 102)".
- Reproduced the stated controls: n6 ACCEPT (70 nodes), n7 ACCEPT (2068), n7_triangle ACCEPT, n7_nocut --no-cutoff ACCEPT (2195), n3_fake REJECT "terminal lost at R=1 B=6", n7_del REJECT "no Bob reply recorded", n7_flip CANNOT SEE, n7_swap ACCEPT, n7_swap30 REJECT **"no Bob reply recorded for R=36867 B=84368"** (i.e. the 30-swap control is killed by a MISSING ENTRY, not by a lost game).
- `referee_scratch/keytest.cpp`: check778c's `canon()` included VERBATIM (sed lines 40-59) vs a nauty-free brute-force canonical form (lex-min over all n! permutations). Results (key-equal&non-iso = soundness failures; iso&key-differ = canonicity failures):
  - n=4, all 3^6 colourings: 66 keys = 66 classes, 0 / 0. Old no-fold key: 36 collisions.
  - n=5, all 3^10 = 59,049 colourings: 792 = 792, 0 / 0. Old key: 6,260 collisions.
  - n=6, ALL 1,724,284 game-shaped positions (|B| in {2|R|, 2|R|-2}): 2,990 = 2,990, 0 / 0. Old key: 371,160 collisions.
  - n=7, all 853,882 game-shaped positions with |R| <= 2: 329 = 329, 0 / 0. Old key: 216,090 collisions.
- `referee_scratch/ref778.cpp`: independent reference solver (nauty-free: memo keyed by brute-force lex-min canonical form; own recursive max-clique routine; NO cutoffs, every line played to the full board). Root values: n=3 ALICE, n=4 BOB, n=5 BOB, n=6 BOB, n=7 BOB (1,598 / 2,388 memo classes).
- Cutoff soundness, exhaustive over every game-shaped position (checker's `bob_cutoff`/`alice_cutoff` included verbatim, sed lines 31-38): n=4, 5, 6 (n=6: 722,086 Alice-to-move + 999,195 Bob-to-move positions; 80,040 + 137,880 Bob-cut; 9,900 + 54,720 Alice-cut): **0** Bob-cut positions where Bob fails to win under ALL continuations; **0** Alice-cut positions where Bob wins under ANY continuation.
- Independent certificates (`ref778 n cert`, different coordinates/strategy from solve778): ref_n4/n5/n6 ACCEPT both with and without cutoffs; ref_n5 exercises the `free2==0` (Alice takes the last edge, m=10≡1 mod 3) branch: 5 terminal leaves. ref_n3 (complete but losing) REJECT "terminal lost".
- **Q8 negative tests (losing reply at a deep position, subtree fully covered):** for a Bob-to-move position P, a reply (x,y) that LOSES per ref778 (valB(P)=1, valA(P+x+y)=0, and NOT "Bob loses under every continuation" — Alice must find the line), plus one row per class for the ENTIRE subtree after it (Bob plays a winning reply where one exists), all PREPENDED (duplicates keep the first) to a complete certificate. The checker can therefore not reject on a missing entry.
  | file | base | depth | --no-cutoff | default |
  |---|---|---|---|---|
  | NEG_A_n6_R4 | ref_n6 | P=(1545,246), reply (8,11) | REJECT terminal lost R=5641 B=27126 | REJECT terminal lost R=5641 B=27126 |
  | NEG_B_n6_R3 | ref_n6 | P=(1537,30), reply (5,6) | REJECT terminal lost R=7681 B=25086 | REJECT alice cutoff R=5633 B=510 |
  | NEG_C_n6_R2 | ref_n6 | P=(9,6), reply (4,5) | REJECT terminal lost R=4745 B=28022 | REJECT alice cutoff R=649 B=3446 |
  | NEG_D_solver_n6_R4 | certs/n6_clique | P=(39,17240) looked up by the walk, reply (7,10) | - | REJECT terminal lost R=4135 B=28632 |
  | NEG_E_solver_n6_R3 | certs/n6_clique | P=(35,16712), reply (2,4) | - | REJECT alice cutoff R=4131 B=17372 |
  | NEG_F_solver_n7_R5 | certs/n7_clique | P=(65611,1192244), reply (7,9) | - | REJECT alice cutoff R=589899 B=1195956 (same with --threads 4) |
  | NEG_G_solver_n7_R4 | certs/n7_clique | P=(32835,20788), reply (3,7) | - | REJECT alice cutoff R=1081411 B=22460 |
  Every rejecting position re-checked with ref778: all are genuinely lost for Bob (valA=0). None of the 11 rejections is "no Bob reply recorded".
- **Exhaustive injection sweeps** (every losing alternative reply, per ref778, at every looked-up / emitted Bob position; subtree fully covered and prepended):
  - n6 solver cert (`certs/n6_clique`), 588 losing replies at 55 looked-up positions (|R|=2:84, 3:261, 4:243): original default **588/588 REJECT** (321 alice-cutoff, 267 terminal-lost). (--no-cutoff column uninformative: base is a cutoff cert -> "no Bob reply".)
  - n6 complete cert (`ref_n6`), 147 losing replies: original **147/147 REJECT** default (63 alice-cutoff, 84 terminal-lost) and **147/147 REJECT** --no-cutoff (all terminal-lost).
  - n5 complete cert (`ref_n5`, m=10 ≡ 1 mod 3, exercises line 118), 24 losing replies: original **24/24 REJECT** default (20 alice-cutoff, 4 terminal-lost) and **24/24** --no-cutoff (all terminal-lost).
- **Mutation testing of the instrument** (`referee_scratch/mutants/`, each a one-line sed of check778c.cpp; "killed" = some negative certificate the original REJECTs is ACCEPTed by the mutant, or a good certificate is rejected):
  | mutant | line | killed by |
  |---|---|---|
  | M1 terminal ties to Bob (`>=`) | 36 | NEG_A/B/C/D, ref_n3, n3_fake |
  | M2 bob_cutoff `>=` | 37 | NEG_A/D/E/F, n7_del |
  | M3 kA = A-|R|-1 | 37 | NEG_A, NEG_D |
  | M4 Alice never plays edge m-1 | 117 | **survived the 7 hand-built negatives**; killed by the n6 sweeps (6/588 and 24/147 ACCEPTed) |
  | M5 old no-fold key | 57 | rejects every GOOD cert (transport lands on occupied edges) — caught by positives only |
  | M6 alice cutoff counted as a leaf | 115 | NEG_E, NEG_F |
  | M7 no terminal check when Alice takes the last edge | 118 | **survived everything at n=6/7** (branch unreachable when m≡0); killed by the n5 sweep (4/24 default, 24/24 --no-cutoff) |
  | M8 dedup by red graph only | 133 | NEG_A/B, n7_swap30, n7_del |
  | M9 budget `<k` | 34 | NEG_A, NEG_D |
  | M10 transport via pos instead of lab | 128 | rejects every GOOD cert — caught by positives only |
  | M11 no terminal check after Bob fills the board | 109 | NEG_A/B/C/D, ref_n3, n3_fake |
  | M12 alpha+1 | 33 | all 12 negatives |
