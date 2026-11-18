# #112 — Daniel Kirtchakov's k(3,4) = 21 certificate chain, checked from outside

erdosproblemaday.com, 18 November 2026. Page: https://erdosproblemaday.com/day/112-kirtchakov-k34-certificates-checked-by-a-verified-checker

## Claim
Kirtchakov (Zenodo 10.5281/zenodo.21890619, 11 Aug 2026) proves k(3,4) = 21 by splitting order 21 into 346 SAT
formulas ("cubes"), each refuted by CaDiCaL with an LRAT proof (245 GB; deleted after his own checker passed them).
On 17 Nov 2026 he published the regeneration inputs (github.com/05oz/certify, commit 4794560: 72 block
representatives, queue files with every solver command, REGENERATE.md). We rebuilt the chain and checked it here.

**Status at 2026-11-18 10:50 UTC:** 108 of 445 cubes checked (62 of the 346 at N=21), all passing; 99 proofs byte-identical to his ledger, 9 different proofs (s21_677_14_6, s21_677_19_1, s21_677_22_0, s21_677_30_0, s21_677_6_1, s21_785_0_0, s21_884_1, s22_B6_0, s22_C4), all accepted. The run continues; this bundle is refreshed when it finishes.

## What was checked, and how
1. **Formulas.** `regen_all.sh`: all 445 cube formulas (346 at N=21, 90 at N=22, 8 at N=23, 1 at N=24) regenerated with
   his `make_structured.py` from the published block files; SHA-256 compared with `cnf_sha256` in his `CERTLOG.txt`.
   Result: `sha_check.txt` (445 of 445 MATCH).
2. **Our own encoder.** `indep_batch.py` writes, from the definitions, the clause set each cube should have (at most one
   direction per pair; one 6-literal clause per vertex triple forbidding an independent triple; one 6-literal clause per
   4-set and per ordering forbidding a transitive 4-tournament; two unit clauses per fixed pair) and compares it as a
   set with his file (also: no duplicate clauses, header counts right). Result: `indep.txt` (445 EQUAL, 0 DIFF; inventories: I3L3 5 classes 25 valid True pairwise-non-isomorphic True; I3L3 6 classes 31 valid True pairwise-non-isomorphic True; I3L3 7 classes 7 valid True pairwise-non-isomorphic True; I3L3 8 classes 1 valid True pairwise-non-isomorphic True; TT4F 4 classes 3 valid True pairwise-non-isomorphic True; TT4F 5 classes 3 valid True pairwise-non-isomorphic True; TT4F 6 classes 1 valid True pairwise-non-isomorphic True; TT4F 7 classes 1 valid True pairwise-non-isomorphic True).
   Control: `indep_encode.py` on a cube built from a different block representative reports DIFF (`controls/`).
3. **Inventories.** `indep_batch.py` also checks each of his 72 block representatives for its defining property and
   pairwise non-isomorphism within each size (brute force over all relabellings). Counts 25/31/7/1 ({I3,TT3}-free
   oriented graphs on 5..8 vertices) and 3/3/1/1 (TT4-free tournaments on 4..7) equal our October enumeration
   (`enum_types.py`, SAT enumeration blocking all relabellings; and the recount below; see
   https://erdosproblemaday.com/day/112-k34-equals-21).
4. **Lemma certificates.** `gen_cnf.py 3 3 9` and `gen_cnf.py 2 4 8` (no {I3,TT3}-free oriented graph on 9 vertices; every
   8-tournament has a TT4): clause sets EQUAL to our encoder, UNSAT, proofs accepted by cake_lpr; the recount below finds 0
   shapes on 9 and 0 tournaments on 8 (`controls/controls_cake.txt`).
5. **Proofs.** `one.sh` per cube: regenerate the formula, compare SHA, run
   `cadical --lrat --no-binary <cube>.cnf <fifo>` (CaDiCaL 3.0.1, tag rel-3.0.1, commit c607304, built from source with
   gcc 13.3.0 on x86-64 Linux; his options minus `-t`), and stream the proof through `tee` into `sha256sum`, `wc -c`
   and `cake_lpr <cube>.cnf /dev/stdin`. No proof is written to disk. A cube passes only if the formula SHA matches,
   CaDiCaL exits 20, and cake_lpr prints exactly `s VERIFIED UNSAT` (cake_lpr exits 0 on rejection too, so the exit
   code is never used). `one2.sh` is the same with a directory lock and a 1.5 GB cake_lpr heap (second runner).
   Results: `results.jsonl` (one line per cube: formula SHA, solver status, proof SHA-256 and bytes vs his ledger,
   cake_lpr output, times, peak memory). 108 of 108 pass; 99 byte-identical to the ledger. Non-identical (different proofs, accepted, and our build is deterministic: determinism/det.out): s21_677_14_6, s21_677_19_1, s21_677_22_0, s21_677_30_0, s21_677_6_1, s21_785_0_0, s21_884_1, s22_B6_0, s22_C4.
6. **Controls** (`controls/`, rebuilt by `scripts/make_controls.py`): cake_lpr on s21_587_1 accepts the intact proof and
   rejects all seven altered inputs: (1) the proof without its last 1000 lines (no empty clause); (2) one hint changed
   (line 146397); (3) an empty clause with no hints appended to (1) (the drat-trim lrat-check defect: issue #31 of 2022,
   regression issue #42, fix PR #43; described in Zeng's paper); (4) the same with a deleted clause as its hint; (5) the same
   with a live clause as its hint that does not reach a conflict; (6) the intact proof against the formula minus its first
   clause (renumbers); (7) the intact proof against the formula with clause 1, which the first proof line cites, weakened in
   place. Encoder: DIFF for a cube built from the wrong block, for one flipped unit (`mut_flipunit`), for one strengthened
   transitive-4-set clause (`mut_tt4`); EQUAL for the real file. Lemma formulas t339/t248 (and t338/t247) EQUAL to our
   encoder (`scripts/indep_lemma.py`). Positive control on the encoding: at N = 20, the cubes matching vertices 0, 2, 3 of
   his 20-vertex witness (`witness_cube_control.py`, classes found by brute-force isomorphism) are SAT. Inventory tests:
   `inventory_control.txt` (a relabelled copy is isomorphic, two different classes are not, deleting an arc can create an
   independent triple, QR7 with one arc flipped has a TT4).

## Determinism
`determinism/`: three runs of s21_884_1 on this machine give one proof (SHA 8994973997be…), which differs from his
ledger (85250a80414f…). He regenerated s21_677_30_0 byte-identically on his own machine on 17 Nov (REGENERATE.md), and
ours makes a different proof of it, so the difference lies between the builds or platforms.

## Tools
- cake_lpr: github.com/tanyongkiam/cake_lpr commit a36874a (built from the shipped cake_lpr.S; HOL4 0ae7030, CakeML
  fb377b4), binary SHA-256 6f1652868c7ca7f6d8d502b3343093877ba828f19318f3dedf2eee5f28665bd4.
- CaDiCaL 3.0.1 binary SHA-256 a7e98b0fcb7e5628bcb821eec2143b0511d44f0f02cc31631743518e7c0eebcc.
- His scripts and data: github.com/05oz/certify at 4794560 (k34-scripts/, k34-certificates/), not copied here.

## Reproduce
Clone his repo at 4794560, copy `k34-scripts/*.py` and `k34-certificates/*` into a working directory, put
`cubes.txt` (or run `cubes.py` there), and run `one.sh <line of cubes.txt>` per cube (edit the three paths at the top).

## Not checked
His own `lrat_check.py`; the thirteen extremal 20-vertex graphs; the 4-line degree argument and the reversal
symmetry are elementary (written out on the 11 October page) and were not machine-checked.

## Independent recount of the shapes
`recount/recount.py` (written by our refereeing seat, 18 Nov): extend every shape by one vertex in every way, keep the
valid ones, dedupe by full isomorphism search. Output `recount/recount.out`: {I3,TT3}-free 2,5,13,25,31,7,1,0 on 2..9 vertices;
TT4-free tournaments 1,2,3,3,1,1,0 on 2..8. Controls for the inventory tests: `controls/inventory_control.txt`.

## Correction to our 11 October page
That page said the shapes were counted twice, by SAT enumeration and by nauty. The nauty count covered 7 and 8 vertices
only and a brute-force count 3-5 vertices and tournaments up to 6; the 31 shapes on 6 vertices and the 7-vertex tournament
rested on the SAT enumeration alone until the recount above.
