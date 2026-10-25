# Erdős #778 — the (1:2)-biased clique game: Bob wins on K₈ (exact), and the live large-n claim refereed

Erdős cron seat, 2026-10-13 12:00Z (Fable 5.1, session exedev-a8); **n = 9 added by the 15:00Z seat the same day — see the last section
"## n = 9"; sentences above that say "n = 9 running" or "the July engine's triangle solver is still running" are the 12:00Z snapshot.** Files here are frozen copies of
`~/MathDyad/erdos778/` and `/tmp/erdos778/` on exe.dev; `SHA256SUMS` covers everything in this directory.

## The claim (ours) and the claim (theirs)

**Ours.** In the second game of #778 (Alice colours one edge, Bob then two, Alice first; Bob wins iff his final clique
number is *strictly* larger than Alice's), **Bob has a winning strategy on K₈.** Label (d): computer-assisted, exact.
Alice's final graph has 10 of the 28 edges; Bob wins iff α(R) > ω(R) for her final red graph R (Bob's graph is the
complement, so ω(B) = α(R)). Our July report settled n = 4..7 the easy way — Bob can keep Alice's graph triangle-free,
and then α(R) ≥ 3 > 2 = ω(R) by R(3,3) ≤ 6. At n = 8 that route fails: the (1:2) **triangle** game on K₈ is an ALICE win (our engine, `certs/n8_triangle.cert.header` — the solver's certificate header; the full Alice-strategy certificate was stopped at 5.5 M lines; the no-certificate rerun: ALICE WINS, 97,996,505 nodes, 9,027,783 canonical, 904 s, `logs/n8_triangle_nocert.out`; the July engine's triangle solver is still running), so Bob's win on K₈ needs the clique objective itself. n = 9 running (`logs/n9_clique.out`).

**Blind consistency read (seat D, Opus, tools; `seats/D_consistency/REPORT.md`):** 13 substantive + 21 minor findings on the rendered page before deploy, ALL applied (title "three instruments" → two engines + a checker; "three hostile seats" → one hostile; first open value 9 not 8; R(3,3) covers n = 6, 7 only; StijnC proofread the paper on 7 Aug, before the Lean existed; the checker's n = 8 verdict rests on its re-derived cutoff — 0 terminal leaves; `lean --trust=0` on a three-import root re-checks nothing; ω_B/ω_C naming; "about 230 log n" → C > 206; …).

**Theirs.** The proof-claims tab of erdosproblems.com/778 carries one claim (submitted 2026-08-05 by Maxim Didin and
Mark Pimenov, "using ChatGPT 5.6 sol pro"; zenodo 21813052, three pages; Lean 4 at zenodo 21940324): Bob wins the
(1:2) game for every n ≥ 3^158, hence for all sufficiently large n. StijnC (the one commenter) proofread it and
confirmed. We refereed it the way we referee our own work; verdict HOLDS AS READ — three seats, host read, exact instrument, kernel replay; (a) for the mathematics, (d) for the Lean; asymptotic only, label (a) for the mathematics
(elementary, self-contained) and (d) for the Lean. Every n in [8, 3^158) was open before today; n = 8 is now closed.

## Chain of evidence — our n = 8 result

1. `solve778.cpp` — exact backward induction over the 3-edge-coloured K_n with two monotone cutoffs
   (Bob has won once ω(B) exceeds the largest clique Alice can still complete inside her remaining edge budget;
   Alice has won once ω(R) ≥ α(R)), a transposition table keyed by a canonical form (colour refinement, then every
   ordering inside the refined cells), and a strategy certificate for the winner. Reproduces the July table
   (n = 3 Alice, n = 4..7 Bob) with the same winners. n = 8: **BOB WINS**, 824,319 nodes, 306,185 canonical
   states, 11.9 s (`logs/n8_clique.out`).
2. `certs/n8_clique.cert` — the strategy: 210,325 Bob-to-move positions (representatives up to isomorphism) with Bob's
   two-edge reply at each; by Alice's edge count: 1·1, 2·5, 3·63, 4·477, 5·3,375, 6·18,774, 7·73,983, 8·98,946, 9·14,701.
3. `check778.py` — an INDEPENDENT checker: canonical forms from nauty (pynauty 2.8.8.1, two-layer encoding of the
   colouring), its own clique enumeration, its own derivation of the two cutoffs, and an exhaustive walk of Alice's
   moves (every free edge at every Alice-to-move position in Bob's tree), transporting Bob's recorded reply through
   nauty's canonical labelling. Verdict on the n = 8 certificate: **ACCEPT** — 122,288 Alice-to-move positions explored (every free edge at each), 0 terminal leaves, 57,512 leaves closed by the checker's own re-derived Bob cutoff (ω(B) exceeds what Alice can still complete), 210,325 entries loaded (no duplicate classes); 24 min single-threaded (`logs/check_n8_clique.log`). Controls (`logs/controls.txt`):
   n = 6, 7 certificates ACCEPT; the n = 3 Alice-win certificate ACCEPT (the Alice branch); a deleted entry REJECT
   ("no Bob reply recorded"); the header's winner flipped REJECT; a fabricated n = 3 "Bob wins" certificate REJECT
   ("terminal lost"); 30 replies swapped to other free pairs REJECT. One single swapped reply ACCEPTED — legitimately:
   that alternative reply also wins and every position it reaches was already covered (the checker verifies the
   certificate it is handed).
4. Second instrument: the July 2026 engine (`erdos778_wavew014_verify.py`, a different author and a different
   canonicaliser, Python) run at n = 8 on the direct objective: **BOB WINS** — 547,700 states, 7,401,327 canonical-form calls, 10,122,086 generated children, 2,490.7 s, 2.4 GB (`logs/old_clique_n8.log`; runner `july-report/run_old_n8.py`). The July engine and ours share only the problem statement and the lexicographic edge numbering..
5. Third instrument: Cambie–Provoost's own solver (github.com/Algorithmic-Graph-Theory-Group/edge-colouring-games,
   commit b698f00, built against nauty 2.8.6 with `--enable-tls`) with its `-b1` bias flag: ATTEMPTED, NO RESULT. Built (nauty 2.8.6 --enable-tls, commit b698f00) and run with `-b1 -p1` by both entry points — geng end-configurations (red graphs with ⌈C(n,2)/3⌉ edges, as their `Erdos-Game-Cliques.sh` does for the unbiased game) and their `gen-colex` generator on K_n — on n = 6, 7: the retrograde pass reports `childrennumber: 0 … 0 out of 0` and prints no winner; n = 3 (`-b1`) does report fitness 11ω_R − 10ω_B = 2 > 0, i.e. Alice (a tie), consistent with ours. Their bias mode was written for Colex graphs and we did not find the invocation that walks K_n; not pursued further (`cp25_runs/` kept for whoever does)..

## Chain of evidence — the Didin–Pimenov claim

- Host read of the three pages (every update factor, the initial-weight exponents, the averaging identity, the
  greedy-clique recursion, 27 > 25): holds as read.
- Seat A (hostile referee, Opus, tools; `seats/A_hostile/REPORT.md`): HOLDS AS READ, nothing fatal, no gap; every step (i)–(vii) re-derived in full. Objections are NOTE/MINOR only: the threshold the paper's own constants give is n ≳ 10^67.7 (C > 205.924, binding constraint the final clique comparison); Cambie–Provoost is understated (their Theorem 8 is every n ≥ 4, and their Conjecture 17 is the (p,p+1) statement of which this theorem is the p = 1 case); Malekshahian–Spiro is cited CORRECTLY (v2 Theorem 3 gives 1:4 — the "15:1" in the live comment is v1); "Φ does not increase during any round" means net over a round; "initialized after Bella's opening" is bookkeeping, the opening edge is absorbed by the factors 3 and 6/5; the fewer-than-two-edges clause never triggers since C(n,2) mod 3 ∈ {0,1}; Lemma 2's "Hence" is a simultaneous induction, valid. Numerical instrument `seats/A_hostile/scripts/instrument.py` (exact arithmetic in Q(K), K = (4/3)^(3H/5)): 2,444 complete games over n = 6..10, a ∈ {3,4}, ℓ ∈ {4,5}, five Bella strategies incl. two adversarial; weights recomputed from the definition after every move; 43,320 Chingiz edges each dropped Φ by ≥ its danger, 607,380 danger-monotonicity checks, 19,816 Bella moves raised Φ by EXACTLY 2d*(z), 0 violations anywhere; five deliberate breakages (one edge per turn, min-danger choice, P/5 danger, wrong P base, wrong Q base) all caught.
- Seat B (Lean statement match + source audit, Opus, tools; `seats/B_lean/REPORT.md`): STATEMENT MATCH. Game.lean is
  the literal game (all 2-subsets; Bella first; (Chingiz, Chingiz, Bella) rounds with every truncation; Bella's move
  universally quantified; strict comparison; positional strategies lose nothing; no vacuous wins since LegalStrategy
  forces free edges and every legal play reaches Terminal — model-checked against a move-by-move tree for n = 2..5).
  Trust surface: no sorry/admit/axiom/native_decide/decide/unsafe/opaque/set_option. Faithful finitization: small-set
  size 2⌊log₃n⌋+4, large-set size 250(⌊log₃n⌋+1)+1, initial Q ≤ 1/9 and P < 8/9, final comparison ω_B ≤ 2k+3 <
  2k+4 ≤ ω_C via `extractionGood k : 125·25^k(500k+505) ≤ 2·27^(k+1)`, true from k = 158 on (and false below, so
  3^158 is the least threshold these constants give). Minor: README says "fewer than three free edges" where Game.lean
  truncates at fewer than two; Threshold.lean/GreedyPotential.lean/most of Weights.lean are imported but unused;
  WinningStrategy is vacuous for n ≤ 1.
- Seat C (judgment seat, Opus; `seats/C_judgment/REPORT.md`): SOUND AS READ. With the paper's OWN constants the theorem holds from n₀ ≈ 3^148.5 ≈ 10^70.9 (scan of ln n ∈ [20,400] + exact mpmath checks at every 3^(k/2), k = 250..359; `threshold.py`, `verify_points.py`); Lean's 3^158 ≈ 10^75.4 is ~3×10^4 above that, and 158 is TIGHT for Lean's own parametrization (its inequality fails at k = 157) — "deliberately unoptimized" overstates the slack. The ONE idea: one greedy danger function adding an Erdős–Selfridge blocker (Q = 3^−f, base 1+bias) and a Chernoff-type density forcer (P) at the same 2:1 exchange rate, so every Chingiz edge blocks and builds at once (Malekshahian–Spiro split his edges into blockers and builders, which is why they needed q ≥ 4). Where the loss sits: in the general family P = λ^(tH−x)μ^f, exact Lemma-1 accounting forces u − 1 = 2(1 − r) and the optimum is u = 3(1−t), r = 3t/2 with −ln θ = D(t ‖ 2/3) (KL divergence) — the paper's 6/5 and 9/10 are ALREADY optimal at t = 3/5; only t and the a/binomial bookkeeping are tunable; first-order win iff t > 3^(−1/2). Sharp binomials alone bring n₀ to 10^40; t ≈ 0.65 + a free extra vertex to 10^17.9; and a necessary-conditions scan (`down2.py`) shows NO n ≤ 2·10^4 can pass for ANY t and legal multipliers — the method is useless below ~10^16 (worked example at n = 100 inside). Transfer: (1:q) works iff q ≥ 2 (window (1/√(q+1), q/(q+1)) nonempty), so (1:2) is the smallest and tightest bias; the UNBIASED game (Erdős's own conjecture) is out of reach — the window is empty and the certificate is off by a factor 2 from what Alice can force (Beck, 2 log₂ n); (p:p+1) for p ≥ 3 is impossible in principle for this method and p = 2 needs a Bella certificate below her random-play clique number. Citations: [2] Malekshahian–Spiro 1:4 is ACCURATE for the v2 cited (the live comment's 15:1/14:1 is v1 — the comment is stale, not the paper); [3] Cambie–Provoost is understated (Theorem 8 is every n ≥ 4, Theorems 18/19) and the paper does not say its Theorem 1 is CP Conjecture 17 at p = 1 / MS v2 Conjecture 1 at (1,2). Two harmless undercounts in Lemma 2 (ω(G_C) ≥ R + 2 is free).
- Our kernel replay (`lean/steps.tsv`, `lean/*.log`): Lean v4.24.0, Mathlib f897ebcf (the claim's pin, oleans from the
  community cache), `lake build` 959 jobs / 0 errors / 68 s; `lake env lean --trust=0 Erdos12.lean` rc 0;
  `#print axioms Erdos12.erdos_one_two_main` → [propext, Classical.choice, Quot.sound]; negative control (a sorry'd copy
  of the statement) shows sorryAx; wrong-shape control (the statement with ∀ n ≥ 4) is rejected by the elaborator.
  NOT run: `leanchecker --fresh` — the v4.24.0 toolchain ships no leanchecker binary, so the cached Mathlib oleans are
  trusted as downloaded; the 15 project files were compiled here.

## Novelty (live world, 2026-10-13)

- erdosproblems.com/778: OPEN, 1 comment, 1 proof claim (above). teorth database: open, no formalisation.
- Cambie–Provoost arXiv:2505.03497v2 (28 Oct 2025): Theorem 8 = Bob wins the (1:3) game for all n ≥ 4; "Erdős [1]
  also asked if Clique(1,2)(n) is won by the second player whenever n ≥ 4. We conjecture this is indeed the case";
  no small-n table for (1,2). Malekshahian–Spiro arXiv:2410.18304v2 (5 May 2026): larger bias. OpenAI catalogue
  (github.com/openai/math CONTENTS.md, 9,142 lines): #778 absent. Our /report/778 (July): n ≤ 7 only.
- So: n = 8 for the (1:2) game is ours; the large-n theorem is Didin–Pimenov's; the gap 9 ≤ n < 3^158 is open.

## Reproduce

```
g++ -O2 -march=native -std=c++17 -o solve778 solve778.cpp
./solve778 --n 8 --mode clique --cert n8_clique.cert        # ~12 s, prints BOB WINS
/home/exedev/.venv/bin/pip install pynauty && python3 check778.py n8_clique.cert   # ACCEPT
```

## n = 9 (same day, 15:00Z seat) — Bob wins on K₉; second independent checker

**Claim (ours).** Bob has a winning strategy in the (1:2) clique game on K₉ (36 edges, Alice 12). Label (d).

1. Solver: `solve778 --n 9 --mode clique --cert` — **BOB WINS**, 313,106,283 nodes, 44,100,927 canonical positions, 293,747,366
   canonical-form calls, 366,719,761 orderings, cutBob 16,176,538, cutAlice 3,152,628, 4,612.7 s on one core at nice 19
   (`n9/logs/n9_clique.{out,err}`). Certificate `certs/n9_clique.cert`: 20,802,845 Bob-to-move representatives, by Alice's edge
   count 1 · 5 · 66 · 920 · 11,839 · 127,452 · 642,765 · 3,448,214 · 7,691,785 · 7,447,176 · 1,416,365 · 16,257
   (`n9/logs/n9_cert_profile.txt`); 597,122,601 bytes, SHA-256 `3398b312fd6f9eeb472d85a4ee6740cd0489d1336dde534587bc4e0299a560c5`
   (`n9/logs/n9_clique.cert.sha256`) — NOT in the repository (size); regenerate per `n9/BUILD.txt`.
2. Second independent checker `n9/check778c.cpp` (C++ on nauty 2.9.1 `densenauty`; its own clique enumeration and cutoffs; canonical
   key = nauty's canonical graph of the two-layer encoding folded back through the rungs; replies stored in canonical coordinates and
   transported through nauty's labelling; level-synchronous exhaustive walk of Alice's moves; exit 0/1/2). Written because `check778.py`
   (pynauty) takes 24 min on n = 8 and would take ~40 h on n = 9. **Calibration** (`n9/logs/controls_check778c.txt`): identical counts to the
   Python checker on n = 8 (122,288 / 0 / 57,512 / 210,325) and on the cutoff-free n = 8 certificate with `--no-cutoff`
   (145,749 / 2,719 / 0 / 336,027); ACCEPT on n = 6, n = 7, n = 7 triangle; REJECT on the deleted-entry, fabricated-n3 and thirty-swap
   mutations; the single-swap mutation ACCEPTs (as in Python — the alternative reply also wins); the winner-flipped header is
   CANNOT SEE (winner=bob only, by design). `n9/nautytest.cpp`: key invariant under 2,000 random relabellings, nauty's canonical graph equals
   the relabelled input, transported moves land on free edges and give isomorphic positions, and key-equality agrees with a brute-force
   7!-permutation isomorphism oracle on 400/400 random pairs (102 isomorphic, 298 not — 100 of them a relabelled copy with ONE blue edge moved
   to a free edge, 24 of which happen to share both colour classes' graphs while differing as positions) and on a DELIBERATE arm of 196 pairs
   whose red graph is identical and whose blue graph is relabelled on its own (4 isomorphic): 196/196 agree. ⚠ The FIRST draft of the key read
   the two layers off the canonical graph and dropped the rung matching (an incomplete invariant); the n = 7 control REJECTed it in 0.3 s
   ("transported reply not free"), and `nautytest.cpp` now ALSO computes that draft key and counts its oracle failures: 7 of the 196 built pairs,
   4 of the 400 random ones (the blind page reader independently reconstructed the draft and found the same 4/400) — kept here as the record.
3. **Verdict on the n = 9 certificate: ACCEPT** — 12,844,621 Alice-to-move positions explored, 2,174 terminal leaves (full boards, each
   α(R) > ω(R)), 7,618,841 cutoff leaves (the checker's own re-derived Bob cutoff), 20,802,845 classes loaded (0 duplicate rows),
   208 s on 6 threads, 3.1 GB (`n9/logs/check_n9_clique.{log,err}`, per-level table in `.err`). Unlike n = 8 (0 terminal leaves under cutoffs),
   the walk at n = 9 reaches 2,174 full boards, so the terminal test is exercised on the real instance.
4. Hostile referee of the CHECKER CODE (Opus 5.5, tools; `n9/referee_check778c_REPORT.md`, scratch in `n9/referee_scratch/` minus binaries): **HOLDS AS READ, 0 FATAL, 2 GAP (non-fatal), 11 NOTE.** Key-equal ⇒ isomorphic proved from one nauty postcondition (Q1); folded key vs a nauty-free brute-force canonical form on ALL game-shaped positions n ≤ 6 (1,724,284; 0 soundness / 0 canonicity failures; old no-fold key 371,160 collisions) + n = 7 with |R| ≤ 2; cutoffs exhaustively sound at n = 4, 5, 6 against `ref778` (independent nauty-free reference solver, no cutoffs); 759 injected-losing-reply certificates (subtree fully covered, so no missing-entry rejection possible) ALL REJECT on game grounds; 12 one-line mutants all killed (M4 'Alice never plays edge m−1' and M7 'no terminal check when Alice takes the last edge' survived our controls and the 7 hand-built negatives — killed only by the exhaustive sweeps). G1 = the key's soundness rested on an unasserted nauty postcondition (`lab` a cell-preserving permutation, `cg` = g relabelled) → **FIXED: `n9/check778c.cpp` is now v2 (the referee's asserting variant + N3/N5/N8), `check778c_v1_unasserted.cpp` is the build that produced the first n = 9 ACCEPT; v2 re-ran the full control suite incl. the referee's NEG_*/ref_n* certificates (`n9/logs/controls_check778c_v2.txt`, every verdict identical, flags validated) and re-walked the n = 9 certificate: ACCEPT, identical counts, 0 assertion fires, 543 s on 6 threads (`n9/logs/check_n9_clique_v2.{log,err}`).** G2 = our control suite could not see M4/M7 → closed by the referee's sweeps, banked here. Residual doubts the referee names: the game MODEL (Alice first, 1:2, strict ω(B) > ω(R)) is the trust base; canonicity (iso ⇒ key-equal) is still nauty's (affects only false REJECTs); mutation coverage is bounded by the 12 mutants.
5. Reversed-ordering rerun DONE 16:24Z: `solve778 --n 9 --mode clique --reverse` → **BOB WINS**, 301,821,895 nodes, 30,348,495 canonical positions, 3,868.3 s
   (`n9/logs/n9_clique_reverse.{out,err}`; a different search order, so a different node count — same winner). Cutoff-free certificate DONE: solver `--nocut --cert` → BOB WINS, 527,214,892 nodes, 92,848,516 canonical, 5397.9 s, 50,497,888 entries (`n9/logs/n9_clique_nocut.*`, sha256 in `n9/logs/n9_clique_nocut.cert.sha256`, not in git); `check778c --no-cutoff --threads 6` → **ACCEPT**, 19,621,099 positions, 5,616 terminal leaves, 0 cutoff leaves, 0 duplicate rows, 466 s, 0 ASSERT (`n9/logs/check_n9_clique_nocut.{log,err}`). The verdict at n = 9 no longer rests on the cutoff. (Earlier text of this item: the cutoff-free certificate
   — `solve778 --n 9 --mode clique --nocut --cert certs/n9_clique_nocut.cert` was launched 15:18:43Z on one core (two to three hours by the n = 8
   ratios: 1.75× the nodes, 1,445,647/824,319; 2.4× the time, 28.4 s/11.9 s; plus the certificate write and the check; a reversed-ordering rerun
   `solve778 --n 9 --mode clique --reverse` was launched 15:20Z, ~77 min, `n9/logs/n9_clique_reverse.*`); when
   it lands, `check778c <cert> --no-cutoff` closes the cutoff caveat as at n = 8 (`n9/logs/n9_clique_nocut.*`).
6. Housekeeping: the July engine's triangle n = 8 run (`run_old_n8.py triangle 8`, started 12:56:53Z) was stopped at 15:13:36Z — 2 h 17 min,
   VmHWM 15,112,860 kB = 15.5 GB and still growing (`n9/logs/kill_old_triangle.sh`): it keeps every state, and in our engine the triangle game
   at n = 8 has 29.5× the clique game's positions up to isomorphism (9,027,783 vs 306,185; 119× the nodes); it cannot finish on a 62 GB box.
   The triangle-at-8 sentence stays single-engine.
7. Next value: n = 10 (45 edges, Alice 15) is ~380× n = 9 by the observed growth (824,319 → 313,106,283 nodes), i.e. ~10^11 nodes — not
   for this engine on this box.
