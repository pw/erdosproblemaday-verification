# #85 `jhpvtq` — the H7 t=1 rep 0 certificate, checked outside Lean (erdos cron seat, 2026-10-20 06Z)

**★ READ FIRST (after the hostile referee, 06:4xZ): drat-trim `lrat-check` is NOT evidence here.** It prints `c VERIFIED`
for a final empty clause whose hints never reach a conflict (the empty clause has pivot 0 and falls through to a RAT
test that passes vacuously) — VERIFIED on the satisfiable `p cnf 2 1 / 1 2 0` with proof `2 0 0`, and on t7r0 with the
empty clause's last hint dropped (`t7r0_droplast_empty.lrat`; cake_lpr rejects it). The result rests on **cake_lpr**
(CakeML-verified, github.com/tanyongkiam/cake_lpr @ a36874a = the commit the authors' kit pins; `.S` sha256 = the repo's
`cake_lpr.sha256`; built `gcc basis_ffi.c cake_lpr.S`) — `run_cake_all.sh` → `cake13.tsv` — and the referee's strict
RUP checker (`referee/src/rupcheck.c`, own unpacker + zstd LZ4; `referee/t1r0.out` RUP-VERIFIED (strict), 72 s).
RESULTS (06:5xZ): cake_lpr on t1r0 **s VERIFIED UNSAT, 759 s** (16 GB heap); all 13 reps under cake_lpr in `cake13.tsv`
(+ the cited-clause CNF flip on t1r0, which must FAIL, as its last row); strict checker on t1r0 (`t1_strict_controls.out`):
unmutated RUP-VERIFIED; final empty clause's last hint dropped -> FAIL at id 10,975,255; first hint of the 4,000,000th
multi-hint addition dropped -> FAIL at id 5,331,022; cited clause 1,302,103 flipped -> FAIL at the first lemma. cake_lpr on
t1r0 with the empty clause's last hint dropped: `cake_droplast.tsv` (must FAIL). t7 controls under both trusted checkers +
the lrat-check exploit: `t7_controls.out`. `unpack_lrat2` (= current unpack_lrat.c; v1 kept as unpack_lrat.v1.c) adds
`--binary` (re-encoding verified byte-identical to the referee's zstd decode on t7r0) and `--mutate-last-empty`.
Byte-identity: our decoder's text output hashes to the module header's `compact_lrat_sha256` (t1r0 e8334179…, t7r0
3d9940e3…), so the checked proof IS the authors' certificate. The lrat-check rows below are kept as history.


Why: the authors' module `Proofs/Erdos85OrderFortyNineSevenHighT1Rep0Certificate.lean` (include_str of a 1.6 GB packed
LRAT, checked by `native_decide`) cannot be built on our shared 62 GB box — the cold replay's lone, uncapped attempt was
earlyoom-SIGTERMed at 03:40Z 10-20 (VmRSS 28,180 MiB, 10,579 s ≈ 40% of the ~27,000 s our 3.5× slowdown predicts; the
authors built it in 7,831 s in a 110 GiB container). Its nine dependents (the capstones) therefore never built.

What we did instead:
1. `EmitT1Rep0.lean <blocks> <index> <out>` (`lean --run` on our cold-replayed oleans): renders the DIMACS of
   `orderFortyNineH7FixedClauses ++ orderFortyNineC4Clauses ++ (orderFortyNineDegreeBlocks 7).clauses ++
   orderFortyNineH7PartitionClauses` for `representativeMasks blocks index` and asserts AT RUN TIME
   `dimacsFormulaToSatClauses arr == (orderFortyNineGeneratedH7SatCnf masks).clauses` (prints `same_as_lean_cnf=true`,
   exits 2 otherwise). Header `p cnf 29764 1329041`. ⚠ The rendered file's sha256 does NOT equal the module header's
   `source_cnf_sha256` for ANY representative (t1r0 4fc61de9… vs 6699c73d…; all 13 differ) — the certificates check against
   our rendering clause for clause, so we read it as DIMACS formatting of their Python generator (not in the deposit).
2. `unpack_lrat.c` (ours, from `Erdos85OrderFortyNineLratCertificateBase.lean` + Std's binary LRAT parser): 7-bit unpack →
   LZ4 frame → binary LRAT → text LRAT on stdout. Action counts equal every module header's `lrat_actions`.
   Soundness of an UNSAT verdict does not depend on the decoder (any proof lrat-check accepts proves UNSAT); the decoder
   only matters for "it is THEIR certificate".
3. drat-trim `lrat-check` (`~/.local/bin/lrat-check`, src `~/.local/src/drat-trim/lrat-check.c`; VERIFIED requires an
   empty-clause addition and every addition checked): `run_t1rep0.sh` → `lratcheck_t1r0.out` **c VERIFIED**, 279.98 s,
   117 MB, 14,332,419 actions (9,646,214 adds / 4,686,205 deletes, 0 RAT, 1 empty clause).
   All 13 H7 t≥1 certificates: `all13.tsv` (+ t7/t6/t5 in this README's session log) — 13/13 VERIFIED.
4. Controls: `--mutate 4000000` (drop one hint deep in the proof) → NOT VERIFIED at exactly the mutated clause id
   5,331,022 (`ctl_mut.out`); a CNF clause the first lemma cites (1,302,103, sign of one literal flipped) → FAILED at the
   first lemma (`ctl_cnf2.out`); an UNCITED unit clause flipped (clause 1, `ctl_cnf.out`) → still VERIFIED — expected,
   a proof of UNSAT of a sub-formula is still a proof; recorded as an uninformative control, not a pass. Small reps
   t7r0 with two hint drops + one cited-clause flip all rejected.
5. Composition (`stub/`): a stub of the T1Rep0 module exporting `sevenHighT1Rep0_excluded` from ONE axiom
   `erdos85_t1rep0_cnf_unsat_checked_externally : (orderFortyNineGeneratedH7SatCnf (representativeMasks 1 0)).Unsat`
   (exactly what 1+3 establish), derived through the authors' own `orderFortyNineH7CnfSegments_satisfied` /
   `sat_of_…_covered` / `orderFortyNineGeneratedH7SatCnf_covered`; `build_stub.sh` builds it + the 9 capstone modules over
   our replay oleans (merged LEAN_PATH dir of symlinks — Lean resolves a package root to ONE search-path entry) and
   prints axioms: **601 / 607 / 604** for the three headline theorems = the authors' audit counts, and the set
   difference against RUN.json's recorded lists is exactly one swap each: theirs
   `Erdos85.sevenHighT1Rep0_check._native.native_decide.ax_1_1` ↔ ours `Erdos85.erdos85_t1rep0_cnf_unsat_checked_externally`.
   No sorryAx. (`stub/stub_v1_exists_lrat.lean.txt` = an earlier variant whose axiom asserted ∃ proof with Std's
   LRAT.check — replaced because Std's checker is not what we ran.)
