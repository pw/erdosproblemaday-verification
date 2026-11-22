# Erdős #112 — Tyler Satchel Orden's 30 ≤ k(6,3) ≤ 32 (submission qrhaen, 21 Nov 2026)

k(n,m) = r(I_n, L_m): least k such that every oriented graph on k vertices has n independent vertices or a transitive
m-tournament. Before: 29 ≤ k(6,3) (Kirtchakov, Zenodo 21890619, 11 Aug 2026) and k(6,3) ≤ 33 (Ihringer–Rajendraprasad–
Weinert, Discrete Math. 344 (2021) 112268, arXiv 1707.09556).

**Claim:** 30 ≤ k(6,3) ≤ 32 (Zenodo concept 10.5281/zenodo.24064870: v1 24064871 of 9 Nov, v2 24272287 of 16 Nov; Lean
record 10.5281/zenodo.24237180, latest 24272901). Files as downloaded: `submitter/`.

**Verdict: VERIFIED** (22 Nov 2026).

**Lower bound.** `check_k63_witness.py witness_n29_m6_anneal.txt` → `check_k63_witness.out` (our checker, reusing the
search in `check_orden.py`): 29 vertices, 140 arcs, no loops/2-cycles, no transitive triangle, no independent 6-set;
negative controls (asked for no independent 5-set; one arc reversed) fail as they must. SHA-256 of the witness =
5c1cc09c…cb3fa, as in his record. The referee's own checker (`referee/wit/`) agrees and finds the independence number
exactly 5 and a trivial automorphism group; 137 of 140 single-arc deletions create an independent 6-set.
A different, non-isomorphic 29-vertex witness appeared on GitHub on 11 Nov (rsvaultpudgy-create/erdos-112-lower-bounds),
two days after Orden's v1; the referee verified it too.

**Upper bound.** Hostile referee (`referee/referee_report.md`): every line checked against IRW (arXiv 1707.09556v3) —
F1 (Cor 2.2), F2 (Lemma 2.1), F3 (k(2,3)=4, k(3,3)=9 Bermond, k(4,3)=15, k(5,3)=23 IRW Thm 1.1), F4 (IRW Lemma 3.3; its
hypothesis |N±(v)| = m−1 holds at all three uses), Lemma A both cases, the Theorem (Case A 212 > 210; Case B 207 > 198).
HOLDS. No slack in two places, so all rests on Lemma B.

**Lemma B, reproduced from scratch** (referee; `referee/lemmaB*.py`, `referee/bt/`, `referee/cnf/`, `referee/proofs/`):
- SAT (pysat) with I(0) fixed to Bermond's graph (unique: SAT enumeration finds exactly 5,040 labelled {I_3,L_3}-free
  8-vertex graphs = the S8-orbit of Bermond's Z8 graph, |Aut| = 8): UNSAT for (out,in) = (3,2) and (2,3) under cadical195,
  glucose4 and kissat; kissat's proofs pass drat-trim (`s VERIFIED`) and cake_lpr on the LRAT (`s VERIFIED UNSAT`)
  (`proofs/certify.log`). Checker controls: `proofs/neg1.out` (`s NOT VERIFIED` on a satisfiable formula), rejected
  unrelated/truncated LRAT.
- (3,2) with I(0) free (no uniqueness used): UNSAT, cadical195, 291 s (not proof-checked).
- Separate C backtracker: 0 completions for (3,2) and (2,3) with Bermond glued; positive controls on 13 vertices
  23,104 / 3,216 / 3,216 completions, matched exactly by SAT enumeration; n=8 count 5040, n=9 count 0.
- Also: k(4,3) = 15 (framed cases), Lemma A cross-check gluing IRW's 14-vertex graph UNSAT for (3,3) and (4,2).

**Objections (none breaks the proof):** the record's "no 21-vertex {I_5,L_3}-free graph has a vertex of degree 6 at all"
assumes IRW's 14-vertex graph is unique (the record calls that uncertified; the hand proof does not need it); "5040 =
8!/|Aut|" alone does not prove uniqueness (IRW Lemma 3.1 and the orbit check do); the README says "directed graph" where
the Lean file means oriented (equivalent, not formalized).

**Lean:** not built by us. The referee read it: faithful definitions, statement literally `30 ≤ k3 6 ∧ k3 6 ≤ 32`,
no sorry/axiom/native_decide in proofs (`decide +kernel`). Orden reports Palomar registry PALOMAR-2026-11-15-000004,
three kernels.

`submission_qrhaen_frozen.json` is the submission as received (contact details removed).
