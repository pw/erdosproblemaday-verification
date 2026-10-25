# Hostile referee report — h1k §1–§3 + h1cube.py (Opus seat, 2026-10-19 ~15:35–16:02Z)
(Saved verbatim-in-substance by the 15Z erdos seat; the seat's harness blocked its own write. Scripts/outputs it wrote
are beside this file.)

**VERDICT: HOLDS AS READ.** Re-derived §1 reduction, Lemma D (steps 1–5) and the §3 case split, and audited h1cube.py
with independent code; no FATAL or SUBSTANTIVE defect. The encoder encodes exactly the block-form problem restricted
to case j + Lemma D's cross constraints + sound residual lex-leader clauses, nothing more. Only substantive item:
status — no k=7 case result yet, nothing certified.

Re-derived (agrees): §1 forward (2-walk saturation ⇒ perfect matching + exactly-one; |F| = (k+1)(k−2), H-degree k−1);
§1 converse (4-cycles of G classified by #N(x)-vertices; given the skeleton, C4-free ⇔ (i)+(ii)+(iii), nothing else
forced or forgotten); Lemma D counts (miss exactly one of d+1 available blocks incl. own; each block missed by exactly
d−1 = 2e(Y) outside + (d−1)−2e(Y) inside; step 3 bijection handles common neighbours inside X or Y; steps 4–5 handle
Y = X' / Y' = X; μ consistent); e(X) ≤ 2 and e+e' ≥ 3; 5 cases exhaustive; pair-swap + pair-permutation + fixed
internal matchings + residual within-block transpositions jointly WLOG, all one row-major order; row-lex unfolding
X ≤lex πX ⇔ row_i ≤lex row_j re-derived; constant positions harmless since each transposition preserves every fixed edge.

Objections (all MINOR except 8):
1. MINOR — §1 converse parenthetical incomplete ("a 4-cycle through x needs a far vertex with two N(x)-neighbours"):
   the middle vertex can also lie in N(x) — excluded by the matching property. Conclusion unaffected (0 mismatches /
   900 mutated structures).
2. MINOR — Lemma D proof uses (ii) silently in step 2 and "X's missers all lie outside X'" silently in step 4. Both true.
3. MINOR — "24 non-paired (X,Y)" / "24 cross constraints": the identity (X,Y)~(X',Y') pairs them up — 12 distinct
   constraints; the encoder adds each twice (harmless).
4. MINOR (efficiency) — residual symmetry left unbroken: swap of the two matched edges in a 2-edge block,
   permutations of same-type pairs, block swap inside a (2,2) pair. Sound, just more solver work. (Transposition list
   matches its brute force: 24/22/20/18/16 for j = 0..4.)
5. MINOR — at k = 5 the Lemma D cross constraints never bind (e ≡ 1 + counting already force sum ≥ 4), so k = 5 runs
   never exercise that cardinality encoding; at k = 7 they do bind and the audit covers them.
6. MINOR (evidence gap, CLOSED by the referee): nothing in the package could catch over-strong C4 clauses. Closed by
   (a) clause audit: 0 of 209k–214k edge-only clauses per case not implied; C4 clauses exactly = independently enumerated
   potential 4-cycles (103,458–105,942 per case), 0 missing / 0 extra; (b) positive control WITH C4 on, via a 3-line
   block-size-parameter patch (h1cube_gen.py): CNF accepted every normalised real solution — (d,s)=(2,2) 56/56 with an
   exhaustive full-group orbit check, (2,3) 3,000/3,000, (4,5) 25/25, and 30/30 at real k=7 with C4 off on their actual
   case CNFs; (c) mutations: each detected.
7. MINOR — cosmetic: --drop-c4 recheck does not check Lemma D on the model; SB assert has a dead disjunct
   `(i, jj) in [(min(i, c), max(i, c))]`; --emit still launches the solver.
8. SUBSTANTIVE (status, not a flaw) — README §4 RESULTS empty; h1cube.py takes verdicts from `kissat -q` with no proof
   log. Each of the 5 case CNFs needs DRAT/LRAT certification; soundness of SB/case fixing then rests on the hand
   argument (now checked). Path works: the k=5 case CNF certified by CaDiCaL + drat-trim → s VERIFIED (drat_k5.out).

What it ran (each < 2 min, niced, ulimit -v 6e6): lemmaD_test.py (identity on C4-free generalised instances, q from
the full G, (2,2),(2,3),(2,4),(4,4),(4,5),(4,6): 0 failures with internal edges present; steps 1/2/4/5 + counting form
of 3 at real k=5,7 with C4 dropped: 0 failures; wrong-pairing negative control: 272 and 224 failures) · audit_cnf.py
(all 5 cases + k=5: 0 not implied, 0 missing, 0 extra; semantic equivalence incl. Lemma D boundary assignments: 0
mismatches; mutations flipped-lex / extra clause / dropped C4: each detected) · descent_test.py + h1cube_gen.py
(0 rejections; lex-ascend mutation 25/25 rejected; exhaustive d=2,s=3 orbit check did not finish in 2 min (27,648
labelled), replaced by the 3,000-sample run) · own_block_enc.py / own_k5.py (independent k=5 encoder: e ≡ 1 UNSAT
0.7 s; free internal edges UNKNOWN at 110 s — as README) · their_k5_controls.out · drat_k5.out (VERIFIED) · cnf/.
