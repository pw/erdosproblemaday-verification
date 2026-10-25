# Hostile referee report — `check778c.cpp` (Erdős #778, (1:2) clique game; K_9 certificate)

Referee: Claude (Opus 5.5), 2026-10-13. Source reviewed: `~/MathDyad/erdos778/cpp/check778c.cpp`, md5 `5096a269d13a64e2c11edac628ab30cd` (144 lines). The installed binary `cpp/check778c` (md5 `40504f77…`) is **byte-identical to a fresh rebuild of this source**, so the logged n=9 ACCEPT (`logs/check_n9_clique.log`: 12,844,621 Alice-to-move positions / 2,174 terminal / 7,618,841 cutoff / 20,802,845 entries / 0 duplicate rows, threads 6, 208 s) was produced by exactly the code refereed here. `certs/n9_clique.cert` sha256 = `3398b312…a560c5`, matching `logs/n9_clique.cert.sha256`. I did not run the checker or the solver on n=9.

## VERDICT

**HOLDS AS READ.** I found no way for this code to ACCEPT a certificate that is not a Bob win in the game as modelled (Alice 1 edge, Bob 2, Alice first, play to the full board, Bob wins iff α(R) > ω(R)). ACCEPT is a self-contained proof in the checker's own coordinates. Its soundness rests on four things, each argued below and each tested: (a) key-equal ⇒ isomorphic; (b) the Bob cutoff is a valid "Bob has already won"; (c) the terminal test; (d) no enqueued child is dropped. Canonicity (iso ⇒ key-equal), the transport convention, the Alice cutoff and the load-time checks can only cause false REJECTs, never false ACCEPTs.

There are two GAPs, both non-fatal: one unasserted library postcondition carries soundness, and the original control suite was too weak to see two classes of checker bug. Neither changes the n=9 verdict.

**Update 16:03Z:** while this review was running, the author shipped `check778c.cpp` **v2** (md5 `01536e5b…`; v1 kept as `check778c_v1_unasserted.cpp`, md5 = the reviewed `5096a269…`). v2 adopts the G1 fix, N3, N5 and N8; see the v2 addendum. G1 is closed for n=9 once the in-progress v2 n=9 run (`logs/check_n9_clique_v2.err`) ends in ACCEPT with no `ASSERT:` line on stderr. At last read it was at level 8 of 12, with counts so far identical to v1.

## FATAL

None.

## GAP

**G1. Soundness of the dedup rests on an unasserted nauty postcondition.** The only nauty property soundness needs is that `cg` is exactly the input graph relabelled by a cell-preserving *permutation* `lab`. Given that, the folded key equals σ(R,B) for a vertex permutation σ, so equal keys imply isomorphic positions (proof in Q1). The runtime checks are necessary but not sufficient:
- line 50 `for(int p=0;p<n;p++) if(lab[p]>=n){ ... exit(2); }` checks cell membership, not that `lab` is a permutation;
- line 55 `... for(int q=n;q<nv;q++) if(ISELEMENT(row,q)){ tau[q-n]=p; cnt++; } if(cnt!=1) ...` counts rungs per **layer-0 position p** only. If two positions p shared one layer-1 partner, both would pass `cnt==1`, one `tau[]` slot would never be written, and line 57 `Bc|=1ULL<<eidx[tau[q1]][tau[q2]]` would read an uninitialised `tau` (UB) and build a key that is not σ(position). A colliding key at line 135 `if(seen.insert(x.first).second) nxt.push_back(x.second);` silently drops a subtree. That is the one route to a false ACCEPT in this design.

It cannot happen with a correct nauty, so this is a GAP, not FATAL:
- `updatecan` builds `cg` from `lab`;
- the library is genuinely TLS-built (488 TLS symbols, incl. `workperm`, `canonlab`, `workspace`; no mutable non-TLS state on densenauty's path);
- my assert variant (below) never fired on any canon call over full n=6, n=7 and both n=8 runs, or on 759 negative certificates.

Both checkers (C++ and pynauty) share nauty, so their n=8 agreement does not discharge G1. It is discharged for n ≤ 6 by brute force, not for n=9. **Fix (verified):** `referee_scratch/check778c_assert.cpp` adds about 8 lines after line 58. They check that `lab` is a cell-preserving permutation, that `cg` equals g relabelled by `pos`, and that `(Rc,Bc)` equals σ(R,B). Cost: about +20% wall time on n=8 (1.84 → 2.22 s). With it, soundness no longer depends on nauty at all; nauty can then only cause REJECTs. Recommend one re-run of n=9 with it (~250 s, 6 threads).

**G2. The stated control suite could not see two classes of checker bug, and its "30 swaps" control does not test the win condition.**
- `mut/n7_swap30` is rejected with **"no Bob reply recorded for R=36867 B=84368"**: a missing entry, not a lost game.
- Before this review, the only control exercising the win condition was `n3_fake`: n=3, one level.
- Mutation testing (table below) showed a checker where Alice never plays edge index m−1 (M4, line 117) survives every stated control and all 7 of my hand-built deep negatives. So does a checker that skips the terminal test when Alice takes the last edge (M7, line 118).

Both are absent from the reviewed code: line 117 is `for(int e=0;e<m;e++){ if(!(freeM>>e&1)) continue;`, and line 118 is unreachable at n=9 since m=36 ≡ 0. **Closed by this review:** exhaustive injected-loss sweeps (759 certificates, all REJECT on game grounds, none via a missing entry) kill all 12 mutants, M4 and M7 included. Recommend banking `referee_scratch/sweep*` plus `ref778` as a standing control.

## NOTE

- **N1 (Q4, line 132)** `u64 B2 = (pc(free2)==1) ? (B|(1ULL<<a)) : ...` is dead for every n. C(n,2) mod 3 ∈ {0,1} (n≡2 mod 3 gives 1, otherwise 0), so Bob never faces a single free edge. If it were reached, line 129 `if(a==b2 || ((R2|B)>>a&1) || ((R2|B)>>b2&1))` would REJECT first, since two distinct free edges cannot exist; load line 85 also rejects `e==fe`. It fails toward REJECT.
- **N2 (Q4, line 118)** The `free2==0` branch (Alice takes the last edge, m ≡ 1 mod 3) never runs at n=9. It is exercised and correct at n=5 (independent cert: 5 terminal leaves; 24/24 injected losses REJECT) and at n=8 nocut (2,719 terminal leaves).
- **N3 (Q6, line 90)** `if(it==table.end()) table.emplace(...); else { dups++; if(it->second!=rep[i]) inconsistent++; }` keeps the first row. `inconsistent` is printed only to stderr (line 96), not in the ACCEPT line (line 142). Soundness is unaffected: only replies actually used are trusted, and they are verified. n=9 has 0 duplicates. Suggest printing `inconsistent` in the ACCEPT line.
- **N4** The ACCEPT line's "certificate entries" is `table.size()`, not the number of entries used. Rows never looked up are unverified (and unneeded). The accurate statement is: "the strategy given by the first row of each canonical class, on the positions reached, is a Bob win".
- **N5 (line 64)** `else if(a=="--threads") NT=atoi(argv[++i]);`:
  - `--threads` as the last argument reads `argv[argc]==NULL` and segfaults;
  - `--threads 0` or a negative value gives non-conforming `omp_set_num_threads` and a size-0 `loc(NT)` indexed by `loc[t]` (UB);
  - unknown flags are silently ignored, so the typo `--nocutoff` runs *with* cutoffs (sound).
  
  Crash-class, not a realistic false ACCEPT. Suggest validating `NT>=1`.
- **N6 (line 92)** Rows with trailing junk parse (`sscanf(...)!=4`), and lines over 255 chars are split by `fgets` into fragments that may parse as rows. Harmless: extra entries are re-verified at line 129 and their children explored.
- **N7** The header's `edgeorder=` is never checked, and need not be. ACCEPT proves the theorem in the checker's own lex coordinates, and a mismatched order can only produce missing entries. The "shared edge numbering" is therefore not a trusted component.
- **N8 (nauty usage, Q7)** `#define MAXN 32` in the program, linked against `libnauty.a` built with MAXN=0 (dynamic). No exported struct or signature depends on MAXN, and nautytest plus the exhaustive tests confirm it works, but `nauty_check(WORDSIZE,mm,nv,NAUTYVERSIONID)` is never called. Suggest calling it once at startup.
  - The rest checks out: `defaultptn=FALSE`; `ptn` marks two cells (`ptn[n-1]=0; ptn[nv-1]=0`); `lab` starts as the identity; `getcanon=TRUE`; options, stats and graphs are stack locals; TLS confirmed.
- **N9** nautytest's t%4==1 arm, as first read, claimed "same red graph, same blue graph". Moving a blue edge to the first free slot generally changes the blue graph, so it did not build the rung-matching adversary. The author has since corrected the comment and added a "blue layer permuted alone" arm. My exhaustive test supersedes both.
- **N10** The solver uses no nauty (`#include <bits/stdc++.h>` only). The C++/Python agreement at n=8 is independent of the solver but not of nauty; see G1.
- **N11 (Q3)** The Alice cutoff is exact, not over-strict: ω(R) ≥ α(R) means Bob loses under every continuation (proof below; exhaustively confirmed at n ≤ 6). It is checked only at popped Alice-to-move positions, but it depends on R alone. So if it holds at a Bob-to-move node, it holds at that node's child, or the terminal test fires there. A lost line cannot slip through between the two checks.

## Proofs for the attacked questions

**Q1, key completeness.** Let G(R,B) be the 2-layer graph. A colour-class-preserving isomorphism G(R1,B1) → G(R2,B2) maps rungs to rungs, since rungs are the only cross-layer edges. It therefore has the form (v,0)↦(σv,0), (v,1)↦(σv,1) with σ an isomorphism of positions; the converse is immediate. So cg1 = cg2 ⟺ the positions are isomorphic.

Now write cg = g relabelled by `pos` (vertex v → `pos[v]`, `pos[lab[p]]=p`) with `lab` cell-preserving. Then rung i–(n+i) goes to `pos[i]`–`pos[n+i]`, so `tau[pos[n+i]-n] = pos[i]`. Red edge (i,j) is read at line 56 as (pos i, pos j). Blue edge (i,j) sits at (pos[n+i], pos[n+j]) and line 57 folds it to (tau[pos[n+i]-n], tau[pos[n+j]-n]) = (pos i, pos j). Hence **key = σ(R,B) as masks, with σ = pos restricted to layer 0**.
- Key-equal ⇒ σ1(P1) = σ2(P2) ⇒ P1 ≅ P2 (soundness: needs only the G1 postcondition).
- Isomorphic ⇒ cg1 = cg2 ⇒ key-equal (canonicity: needs nauty's canonical-form guarantee, and affects completeness only).
- The old no-fold key reads layer 1 in its own positions, which drops `tau`. It collided 371,160 times on n=6.

Automorphisms are irrelevant: the key is a function of `cg` alone.

**Q2, transport.** Load: row (R0,B0,e,f) gives σ0 and stores σ0(e), σ0(f). Lookup at (R2,B) gives σ1, and line 128 computes `a = eidx[lab[ea[ec]]][lab[eb[ec]]]` = σ1⁻¹σ0(e) =: π(e). Equal keys mean σ1(R2,B) = σ0(R0,B0), so π maps (R0,B0) onto (R2,B) exactly. The transported pair is therefore free, distinct, and leads to π(R0, B0+e+f).

A different labelling gives π' with π'π⁻¹ ∈ Aut(R2,B), so the resulting positions are isomorphic. And the walk never assumes the reply wins: it explores the child.

**Q3, cutoffs.**
- Bob cutoff: B only grows, so ω(B_final) ≥ ω(B). Any final red clique S has no blue edge inside, and each of its currently non-red edges must be among Alice's kA = A−|R| remaining edges. So ω(R_final) ≤ `omega_budget(R,B,kA)`. At the end α(R_final) = ω(B_final) > ω(R_final), a Bob win under every continuation.
- Alice cutoff: R only grows, so ω(R_final) ≥ ω(R) ≥ α(R) ≥ α(R_final), a Bob loss under every continuation.

Both are confirmed exhaustively at n=4, 5, 6 against exact game values, in the strong "every continuation" form.

**Q5, walk completeness.** Each explored Alice-to-move position P and each free e ends in exactly one of:
- a verified terminal (lines 109 / 118);
- a sound Bob cutoff (lines 116 / 122);
- a found, free reply (lines 123–129) whose child is keyed at line 133 and offered to `seen` at line 135.

If the key is new, the child is pushed and explored next level. If it is not new, a key-equal (hence isomorphic) child was pushed earlier in the same level: keys encode |R|, so no cross-level match is possible. Induction on free edges from the leaves gives a Bob win from every explored position, the root included.

On the bookkeeping:
- every `lerr` write is inside `#pragma omp critical` and is never cleared;
- the chunk loop stops on error, and line 138 REJECTs;
- the counters (`nodes`, `leaves`, `cutoffs`, `gen`) feed no decision;
- `table.find` from many threads is a const-for-races call.

The multi-chunk (`CH=400000`) and multi-flush (`1<<20`) paths are untested at n ≤ 8 but run at n=9. I re-ran them with chunk = 7 and flush = 1024: identical counts and verdicts on n7, n8, n8-nocut and three negatives, at 1 and 5 threads.

## Residual doubts (strongest first)

1. **G1 at n=9 specifically:** the logged n=9 ACCEPT is v1 (unasserted). The postcondition has been verified on every canon call only for n ≤ 8 and the test certificates. The v2 n=9 run will close it; read its stderr for `ASSERT:` and its stdout for the `v2 asserted` ACCEPT line.
2. **The game model itself is the trust base.** Alice first, 1:2, play to a full board, strict ω(B) > ω(R). I refereed the code against the rules as stated in the brief, not against erdosproblems.com #778's wording (tie rule, whether Bob must take exactly two edges).
3. **Canonicity at n=9** (iso ⇒ key-equal) is trusted to nauty. It affects only false REJECTs and node counts, not soundness.
4. **Mutation coverage is bounded by the mutants I thought of.** 12 one-line mutants, all killed by the extended suite. A two-site bug that both drops children and suppresses its own symptom is not ruled out by testing, only by the reading above.
5. **The n=8 cross-check with check778.py shares nauty** (G1 / N10).

## v2 addendum (author's post-review revision, 16:03Z)

`diff check778c_v1_unasserted.cpp check778c.cpp` shows four changes:
- after line 58: the referee assert block, verbatim from `referee_scratch/check778c_assert.cpp` (closes G1 once n=9 is re-run);
- line 64 → 73: `--threads` requires a value in 1..64, and unknown flags give CANNOT SEE (closes N5);
- new line 84: `nauty_check(WORDSIZE,SETWORDSNEEDED(2*n),2*n,NAUTYVERSIONID);` (closes N8);
- the ACCEPT line prints `inconsistent` (closes N3).

Hostile read of v2:
- **N12 (new, my own residue):** v2 inherits a dead line from my variant: `for(int i=0;i<n;i++) if(pos[n+i]!=n+(pos[i])&&false){}`. Delete it. If anyone "fixes" it by removing `&&false`, it will false-REJECT, because the canonical rung matching `tau` is generally not the identity. Harmless as written.
- **N13 (new):** `nauty_check` reports a mismatch by calling `exit(1)`, which this checker's convention reads as **REJECT**, not CANNOT SEE. It fails toward rejection, so it is safe, but a library mismatch would be mislabelled as a refutation of the certificate.
- **Soundness under v2:** the final assert, `if(Rs!=Rc||Bs!=Bc){ ... exit(3);}`, checks key == σ(R,B) directly, with σ = `pos` on layer 0 a permutation (just asserted). That alone makes key-equal ⇒ isomorphic hold without trusting nauty. Even the line-57 `tau` UB from G1 is now caught: a garbage `Bc` fails the compare, and a garbage `Bc` that happens to equal σ(B) is the correct key anyway.

v2 evidence:
- The installed v2 binary is byte-identical to a rebuild of `cpp/check778c.cpp` (built from the same path; a rebuild from a renamed copy differs only in the STT_FILE symbol name).
- v1 (rebuilt) vs v2 over all 773 test certificates × {default, --no-cutoff} = 1,546 runs: **0 verdict differences, 0 assertion fires**.
  - (An earlier sweep reported 11 "diffs". All were artifacts of the binary being swapped mid-run: 10 ACCEPT lines whose format changed, plus 1 empty read during the swap. Re-run, the case agrees.)
- v2 on n8_clique: identical counts.
- `--threads` with no value, `--threads 0` and the typo `--nocutoff` each give CANNOT SEE.

## What you ran


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
- n=8 thread determinism: `check778c n8_clique.cert` at --threads 1 (5.1 s) and 6 (1.8 s): identical 122,288 / 0 / 57,512 / 210,325 (= the Python figures). n8_clique_nocut --no-cutoff at 6 threads: 145,749 / 2,719 / 0 / 336,027.
- `referee_scratch/check778c_assert.cpp` (G1 fix): n8_clique and n8_clique_nocut give identical verdicts and counts with zero assertion fires (2.22 s vs 1.84 s; 3.17 s vs 2.71 s).
- `referee_scratch/check778c_smallchunk.cpp` (`CH=7`, flush every 1024 rows): n7, n8, n8-nocut, NEG_F, NEG_G, n7_swap30 at 1 and 5 threads give identical counts and verdicts to the shipped build.
- Provenance: rebuilt check778c from the reviewed source and `cmp` reports it byte-identical to the installed binary; `sha256sum certs/n9_clique.cert` matches the logged hash; `wc -l` = 20,802,846 (1 header + 20,802,845 rows).
- Read-only: `logs/check_n9_clique.{log,err}` (n=9 ACCEPT, load line "0 duplicate rows, 0 with a different reply"), `logs/n9_clique.out` (solver: BOB WINS, 4,612.7 s), `logs/controls_check778c.txt`, `solve778.cpp` includes (no nauty), `check778.py` imports (pynauty).
- All scratch artifacts are under `/tmp/erdos778/referee_scratch/`: keytest.cpp, ref778.cpp, mutants/, sweep5/, sweep6/, sweep6ref/, NEG_*.cert, ref_n*.cert, check778c_assert.cpp, check778c_smallchunk.cpp, check778c_log.cpp.
- Parallel sweeps (`referee_scratch/assertsweep/`): (1) shipped binary vs assert variant over 773 certs × 2 options, 0 fires; the 1 diff was transient during the v2 binary swap. (2) Rebuilt v1 vs v2 over the same 1,546 runs: 0 fires, 0 diffs. Verdict mix: 10 ACCEPT (good certs), 409 REJECT alice-cutoff, 533 REJECT terminal-lost, 594 REJECT missing entry (cutoff bases run with --no-cutoff, plus the stated mutants).
