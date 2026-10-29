# Erdős #85 — reader submission jhpvtq (f(48) = 8, f(49) = 7) — our verification bundle

Submission: Robb Walters with AI co-authors (Lean Genius / 2AM Logic), Zenodo 23325806, repository
lean-genius @ 2029149d7e42. Claim: every 49-vertex graph with minimum degree ≥ 7 contains a 4-cycle (f(49) ≤ 7), with
explicit graphs for the lower sides — so f(48) = 8 > f(49) = 7, equivalently R(C₄, K₁,₄₂) = 49 (Boza's table left
{49, 50}). Verdict: PARTIAL (2026-10-20) → **VERIFIED (2026-10-29)**, after our H1 campaign closed all 13,351 cells (item 8, h1m/README.md §6); see the review on /submission/jhpvtq.

Everything here is OUR code and OUR output. Nothing in fs/ or h9/ reads the authors' Lean, emitters, CNFs or
certificates; h1sample/ and h7check/ deliberately run THEIR emitters on OUR build and compare to their receipts.

## Chain
1. **Lower sides** (`lower/`): check_witness.py (edge-list codegree) and witness_matrix.py (A² off-diagonal ≤ 1) on
   Boza's 48-vertex graph (7-regular, C₄-free) and the 49-vertex graph (δ = 6, C₄-free); both reject an added edge.
2. **Case split by hand** (`split/`): degrees 7/8; highs pairwise non-adjacent with one common neighbour;
   h = #high ∈ {1,3,5,7,9}; H7 splits as (7−t, 14+3t, 21−3t). sample_h1.py recounts the H1 orbit inventory.
3. **From-scratch encoding** (`fs/`, `h9/`; README in fs/): exact low degrees + codegree ≤ 1 (h9/c4cnf.py) +
   R1/R1b (every vertex ≠ x has EXACTLY one neighbour in N(x) for each high x — the 48 two-walks saturate) + lex-leader
   symmetry breaking on interchangeable lows (+ high-permutation SB for H7 t = 0). Table: fs/RESULTS.md. Every H3, H5,
   H7 and H9 cell UNSAT under Kissat 4.0.4; CaDiCaL 1.7.3 DRAT proofs checked by drat-trim (19/19 + 20/20).
   H1 is re-proved by its own route (item 8, the miss-matrix cube; all 13,351 cells DRAT-checked 2026-10-27), not by this encoder.
4. **Their artefacts on our build**: H7 t = 0 — 28 base cubes = inputs.json, 28 covers = receipts + UNSAT, leaves
   (h7check/leaves.tsv); H1 — 12 random orbits (seed 20261019, h1sample/sample.json) emitted by their emitter: hash =
   receipt, UNSAT under the other solver family (h1sample/results.tsv). INSTRUMENT_NOTE.txt: `lean --run` prints 340
   bytes of compile warnings ahead of the DIMACS; stripped, hashes match (first reading said MISMATCH).
5. **Cold Lean replay** (`replay/`): 893 project modules + 1 Archive into an empty root with our own scheduler
   (drive.py, then drive2.py from 15:0xZ 10-19 — see its docstring), Mathlib from the pinned cache; steps.tsv has every
   module's rc, seconds, source sha256, max RSS, olean sha256. Result: 883 of the 893 project modules rc 0 with olean sha256 = the authors' RUN.json object_sha256 (replay/olean_match.out; + the Archive module, not in their RUN.json). Two rows are OURS, not findings: the `-15` T1Rep0Certificate row (stopped by the 21Z seat, Lean's --memory cap) and the `1` T0CanonicalCnfSatisfaction row (our --memory=16000; passed uncapped, 22.8 GB). The final `143` T1Rep0Certificate row is earlyoom (SIGTERM at VmRSS 28,180 MiB, 10,579 s, 2026-10-20 03:40Z) on our shared 62 GB box; its 9 dependents (the capstones) never ran here — see 9 for how both were covered.
6. **Referees**: referee/REPORT.md (the submission: HOLDS WITH GAPS), fs/referee/REPORT.md (our encoding: SOUND AS READ).
7. **H1 by hand** (`h1k/`, README there): reduction of H1 to a 6-regular C₄-free graph on 40 vertices with 8 paired
   blocks; Lemma D (codegree-0 counts between blocks) ⇒ e(X) + e(X') ≥ 3 ⇒ five cases with every block's internal
   matching fixed; k = 3 and k = 5 analogues UNSAT; hostile referee h1k/referee/REPORT.md HOLDS AS READ. The k = 7 cases
   did not fall as single SAT calls in the time we gave them (h1k/README.md RESULTS) — superseded by the miss-matrix route (8).

8. **H1 miss-matrix cube** (`h1m/`, README there): every far vertex misses exactly one available block; M[X][Y] =
   #vertices of X missing Y gives edges(X,Y) = 5 − M[X][Y], M symmetric, row sums 2e(X), and Lemma D ⇔
   M[X'][Y] + M[X][Y'] ≤ 5. Enumerated by menum.py + mcount.c (+ the h1m referee's own enumerator): 13,351 classes,
   which the referee matched ROW BY ROW to the submission's kept H1 inventory (their highBranchMissCount = M, their
   capacity filter = M4; 190 removed rows = the M4 failures). Cell encoder h1mcell.py; random sample 26/26 UNSAT under
   Kissat (19–167 s/cell); no-C4 and mutation controls in runs/ and referee/. Hostile referee HOLDS WITH FIXES (all
   applied). **The full 13,351-cell pass RAN (2026-10-25 → 10-27, Patrick's go):** all 13,351 UNSAT under Kissat (206.9 CPU-h, one pass) and all 13,351 again under CaDiCaL with binary DRAT proofs verified by drat-trim (280.1 h, one pass); proofs (253.7 GB) checked, then deleted; every cell's row, formula hash and proof size in h1m/runs/campaign_{kissat,drat}.tsv; reproduce recipe, tools and file hashes in h1m/README.md §6. Post-run checks h1m/flipcheck/ (ALL PASS) and hostile referee h1m/referee_flip/REPORT.md (HOLDS WITH FIXES, all applied). With item 3, every stratum is now re-proved from scratch with checked proofs. (The 10-20 text said this pass had not been run; it is superseded.)

9. **T1Rep0Certificate, checked outside Lean, and the capstones over a one-axiom stub** (`t1rep0/`, README there).
   EmitT1Rep0.lean renders `orderFortyNineGeneratedH7SatCnf (representativeMasks t r)` as DIMACS and checks at run time
   that the rendered clause array maps clause for clause onto the Lean CNF; unpack_lrat.c (ours) decodes the packed
   certificate to text LRAT whose sha256 = the module header's `compact_lrat_sha256` (t1r0, t7r0). **cake_lpr**
   (CakeML-verified, @ a36874a, the commit the authors' kit pins) accepts all 13 H7 t ≥ 1 certificates (cake13.tsv),
   and the referee's independent strict RUP checker accepts t1r0 (referee/t1r0.out). Controls: a hint dropped deep in the
   proof, the final empty clause's last hint dropped, and a literal flipped in a clause the first step cites are all
   rejected; an uncited unit clause flipped is still accepted (expected, uninformative). ⚠ drat-trim's `lrat-check` was
   our first checker and is NOT evidence: it accepts a final empty clause that never reaches a conflict (referee; e.g.
   VERIFIED on the satisfiable `1 2 0` with proof `2 0 0`, and on t7r0 with the empty clause's last hint dropped —
   `t7r0_droplast_empty.lrat`). (⚠ → CLOSED 2026-10-21, see `gap6/README.md`: first-use renaming of our rendering reproduces every header hash, 13/13.) ⚠ Our rendered CNFs do NOT have the headers' `source_cnf_sha256` (rendered_cnf.sha256),
   and six formatting variants don't reproduce it — unexplained; the generator is not in the deposit. stub/: the T1Rep0
   module replaced by a stub exporting `sevenHighT1Rep0_excluded` from ONE axiom
   (`erdos85_t1rep0_cnf_unsat_checked_externally`, the CNF's `Unsat`), the 9 downstream modules built on our replay
   oleans, `#print axioms` on the three headline theorems: 601 / 607 / 604 (the authors' audit counts), set difference
   vs RUN.json's recorded lists exactly one swap each (stub/axiom_counts.out). The headline theorems are CONDITIONAL on
   `hOne` (H1) and `hSeven` (H7 t = 0), as the authors state. Hostile referee: t1rep0/referee/REPORT.md (HOLDS WITH FIXES,
   all applied).

10. **v1.1's `InventoryNonzero` (gap 2), built** (`v11nonzero/`, README there): the module and its 190-module cone at tag erdos85-paper-v1.1, all rc 0; its theorems use only propext / Quot.sound / Classical.choice. So `hOne` reduces to bare unsatisfiability of the inventory's formulas.

## Controls
sbtest/sbtest2 (brute-force SB soundness + mutations) · er7ctl (R1/R1b on ER(7), secant mutation UNSAT) · erqctl
(ER(3) exhaustive) · erdescend_hsb (ER(5)/ER(7) lex-descent at production scale) · h1norm_erctl · h9 mutctl · DRAT
negative controls (fs/out/dratneg.out, last row of h9/drat.tsv) · replay drive2 adoption judge vs GNU time's failure
lines.

## Reproduce
Lower sides: `python3 lower/check_witness.py`. A stratum cell: `python3 fs/fsrun.py <args as in fs/RESULTS.md>` then
`cadical --no-binary cell.cnf cell.drat && drat-trim cell.cnf cell.drat`. Replay: clone lean-genius at 2029149d7e42,
`lake exe cache get` in proofs/, fetch the 13 H7 certificates (their scripts/fetch-h7-certificates.sh, requester-pays),
`python3 replay/drive2.py <proofs> <out> 6`.

## Not checked
The H1 LRAT as a whole (~28 TB, not repeatable on one box), the bank proofs themselves, cake_lpr itself, and the T1Rep0Certificate module inside Lean on our machine (checked outside Lean instead, 9).
