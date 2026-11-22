I tried to refute the upper bound and could not. Both bounds hold, so 30 ≤ k(6,3) ≤ 32 stands as claimed.

## Verdicts
- **Upper bound k(6,3) ≤ 32: HOLDS.** I checked the proof line by line against the arXiv version of IRW (1707.09556v3). Everything except Lemma B is a correct hand argument. Two inequalities have no slack. Lemma A Case (3,3) needs e(J) ≥ 42 exactly (IRW only prove 38). Theorem Case A ends at 212 > 210. So any error in Lemma B would break the proof. I reproduced Lemma B three ways with my own code, and the key run is proof-checked.
- **Lower bound k(6,3) ≥ 30: HOLDS.** My own checker passes the witness. A second, independent 29-vertex witness also exists and passes (see the world check).

## Task 1: the proof, line by line
- **F1** = IRW Cor 2.2. It is stated for {I_m, L_3}-free graphs, but the independence part only needs L_3-free. Correct.
- **F2** = IRW Lemma 2.1(2). Correct.
- **F3** is right: r(I_2,L_3)=4 (IRW credit Erdős–Rado [9]), r(I_3,L_3)=9 (Bermond), r(I_4,L_3)=15 and r(I_5,L_3)=23 (IRW Theorem 1.1). I re-checked IRW's own steps: Prop 3.4 Case (a) gives 20 vs 16, Case (b) gives 40 vs 36. Their Lemma 3.2 (at least 38 edges) also holds.
- **F4** is quoted exactly as IRW Lemma 3.3. It assumes d⁻(v) = m−1 (or d⁺(w) = m−1) in an {I_m, L_3}-free graph. That hypothesis is met at every use: Lemma A Case (4,2) with m=5 and |P|=4; Theorem Case A with m=6 and |N±|=5; Theorem Case B with m=6 and |N⁺|=5. Their private-neighbour proof is sound.
- **Lemma A**, all correct:
  - Degree ≥ 6 and out/in-degree ≤ 4.
  - All degrees ≥ 7 gives at least 147/2 edges, so at least 74.
  - The edge decomposition e(H) = 6 + t + e(P∪Q, J) + e(J), and the degree sum 6 + 2t + e(P∪Q, J) ≥ 36.
  - Case (3,3): "at most 3 vertices of J with no neighbour in P" holds, because two non-adjacent such vertices plus P give 5 independent vertices, and an L_3-free tournament has at most 3 vertices. Then the minimum of t + max(22, 30−2t) is 26, so e(H) ≥ 74.
  - Case (4,2): F4 gives at least 20; "at most 8 with no neighbour in Q" holds via r(I_3,L_3)=9; the minimum is 28, so e(H) ≥ 76.
- **Theorem**, all correct:
  - Degrees are 9 or 10.
  - Case A: 32 + 32 + 2·74 = 212 > 210.
  - Case B: the out-degree sum equals the in-degree sum, so a (5,4) vertex exists. Inside C every degree is ≥ 7, so e(C) ≥ 77. Then e(N⁺(v), C) ≥ 34 and e(N⁻(v), C) ≥ 19, giving 207 > 198. (This is a balance argument, not parity; the text says it correctly.)

**Objections** (none breaks the proof):
1. "A SAT cross-check is stronger: gluing on IRW's 14-vertex graph shows that no 21-vertex {I_5, L_3}-free graph has a vertex of degree 6 at all." This overstates it. Gluing on one fixed 14-vertex graph covers all cases only if that graph is the unique {I_4, L_3}-free graph on 14 vertices, and the record's own "Side facts" call that "uncertified". The hand proof of Lemma A does not depend on it.
2. "That graph is Bermond's: there are exactly 5040 = 8!/|Aut| labelled ones, with |Aut| = 8." A count plus |Aut| does not by itself prove there is only one graph up to isomorphism (for example, two classes with |Aut| = 16 also give 5040). Uniqueness is IRW Lemma 3.1, and my orbit check (below) closes it independently. Wording only.
3. "the bounds before this record were 29 <= k(6,3) <= 33" is correct. But the record does not mention a second, non-isomorphic 29-vertex witness posted on GitHub two days after its first version (details in Task 5).
4. The README's problem statement says "every directed graph", while the Lean file formalizes oriented graphs. They are equivalent (delete one arc of each 2-cycle), but that step is not formalized. Minor.

## Task 2: Lemma B, reproduced with my own code (timings at nice 19 on a loaded box)
I wrote my own SAT encoding (pysat) and, separately, my own C backtracker, without reusing verify_small.c's logic.

**Controls for the SAT encoding**
- Known values: n=4, k=2 UNSAT; n=9, k=3 UNSAT; n=8, k=3 SAT; n=14, k=4 SAT (finds a 42-arc, 6-regular graph, confirmed by brute force).
- Bermond's graph is unique: SAT enumeration finds exactly **5040** labelled {I_3, L_3}-free graphs on 8 vertices (cadical195 and glucose4). That set is exactly the S8-orbit of Bermond's Z8 graph, and |Aut| = 8.

**Lemma B results**
- **Vertex 0 has (out, in) = (3,2), with I(0) fixed to Bermond's graph:** UNSAT under cadical195, glucose4 and kissat.
  - The kissat proof passes drat-trim ("s VERIFIED").
  - The LRAT version passes cake_lpr ("s VERIFIED UNSAT").
  - (2,3) gives the same result.
- **(3,2) with I(0) completely free** (does not use Bermond's uniqueness at all): UNSAT in 291 s with cadical195. This run is not proof-checked; glucose4 timed out at 900 s. I killed the (2,3) free run after about 20 min; it is equivalent to (3,2) by reversing all arcs.
- Degree(0) ≥ 7 is UNSAT. Degree(0) ≤ 5 with no labels fixed was too slow, and I killed it after about 7 min.

**Positive controls and mutations**
- Degree(0) = 6 on 14 vertices: SAT.
- On 13 vertices, degree(0) ≤ 4 is SAT. This is a near-miss: a vertex with 8 non-neighbours exists there.
- The 13-vertex (2,2) frame with Bermond glued in: SAT.
- Dropping the transitive-triangle clauses, or loosening to k=5: SAT.
- The proof checkers reject when they should: drat-trim says "s NOT VERIFIED" on a satisfiable formula with an unrelated proof; cake_lpr rejects an unrelated LRAT, a truncated LRAT, and a mismatched case.

**My C backtracker (bt.c)**
- Exact known counts: n=3 gives 2, n=4 gives 0, **n=8, k=3 gives 5040** (1.2 s), n=9 gives 0 (19.7 s).
- Lemma B with Bermond glued in: **(3,2) has 0 completions** (0.3 s), **(2,3) has 0** (1.7 s).
- Positive controls on 13 vertices: 23,104 completions for (2,2), 3,216 for (3,1), and 3,216 for (1,3); the last two must match by reversal, and do.
- **Cross-check between the two methods:** SAT enumeration on the same 13-vertex frames gives exactly 23,104 / 3,216 / 3,216.

**Extras**
- r(I_4, L_3) = 15: no 15-vertex graph. With a (3,3) frame and Bermond fixed, UNSAT in 0.2 s; with I(0) free, UNSAT in 133 s. I killed the frameless run for time.
- Lemma A cross-check, gluing on IRW's 14-vertex graph: UNSAT for (3,3) in 4.3 s and for (4,2) in 1.0 s, matching lemmaA_nodeg6.log.
  - Controls: the same glue on 20 vertices with (3,2) is SAT, and the k=6 mutation is SAT.
  - **With I(0) free plus a 6-regularity constraint, both cases timed out at 900 s**, so I could not confirm objection 1's "at all".
- IRW's two graphs, built from their own definitions, check out: the 14-vertex one is {I_4, L_3}-free and 6-regular; the Z_22 one is {I_5, L_3}-free and 8-regular.

## Task 3: the lower-bound witness
My checker (bitmask recursion plus a separate itertools brute force) confirms:
- 29 vertices, 140 arcs; no loops, duplicate arcs or 2-cycles; 0 transitive triangles; 0 independent 6-sets by both methods.
- Out- and in-degrees are 4 or 5; the independence number is exactly 5 (760 independent 5-sets); the automorphism group is trivial.
- SHA-256 matches 5c1cc09c…cb3fa.

Controls:
- Both forms of Kirtchakov's Z_28 circulant pass, and the x → 5x relabelling claim checks out.
- Circulant plus an isolated vertex fails (252 independent 6-sets); adding a chord fails (transitive triangle); adding a reverse arc fails (2-cycle).
- 137 of 140 single-arc deletions create an independent 6-set, and the checker catches each one.

## Task 4: Lean
- **The definitions are faithful:**
  - `OGraph.asymm` rules out loops and 2-cycles.
  - The independence and transitive-triangle definitions are correct (asymmetry forces the three vertices to be distinct).
  - `Free n` means "no independent set of exactly n", which is equivalent to "no independent set of at least n".
  - `k3 n = sInf {k | ∀ D : OGraph (Fin k), ¬D.Free n}`.
- **The statement is literally `30 ≤ k3 6 ∧ k3 6 ≤ 32`.** The usual trap (an empty set making sInf return 0) is closed: the lower bound gets non-emptiness from `bound_6_36`, and the upper bound proves 32 is in the set via `Nat.sInf_le`.
- **The grep is clean:** no sorry, admit, axiom declarations, implemented_by, extern, opaque, unsafe, set_option, or notation/instance overrides. `native_decide` appears only in comments. All computation uses `decide +kernel`.
- `rows29` is identical to the witness file, and Defs and Main are identical to the GitHub copies.
- The Lean proof of Lemma B does not assume Bermond's uniqueness, so it is a different decomposition from the paper's.
- **Not verified by me:** I did not build it (as instructed), so I have not seen `#print axioms` output. The GitHub repo has no CI runs.

## Task 5: world check
- **arXiv:** only IRW. Nobody else states k(6,3) ≤ 32 or better, or a different value of r(I_5, L_3).
- **Zenodo:**
  - Kirtchakov 21890619 (2026-08-11) confirmed: k(3,4) = 21 and 29 ≤ k(6,3) ≤ 33.
  - Orden v1 24064871 is dated **2026-11-09**, v2 24272287 is dated 2026-11-16, and the Lean record is 24272901.
  - Orden also posted 24390891 (2026-11-20, other small bounds).
- **GitHub:**
  - `rsvaultpudgy-create/erdos-112-lower-bounds` (single commit, **2026-11-11**) independently claims k(6,3) ≥ 30 with a different 29-vertex graph.
    - I verified it passes and is **not isomorphic** to Orden's.
    - Orden is earlier by 2 days.
    - His Nov 20 record cites this repo for other bounds, but the k(6,3) record does not mention it.
  - teorth/erdosproblems lists #112 as open and unformalized. formal-conjectures PR #6648 (open) states the problem only, with no proof.

## What I could not check
- The Lean build and its axioms.
- The erdosproblems.com forum, which the GitHub repo cites (hard wall).
- Lemma A's SAT cross-check without assuming IRW's 14-vertex graph is unique.
- Uniqueness of IRW's 14- and 22-vertex graphs.
- The claim that no circulant witness exists on 29–32 vertices.
- The McKay-data claims.
- Frameless r(I_4, L_3) = 15, and r(I_5, L_3) = 23 by SAT.

## Process note
I once used `pkill -P <my shell> -f certify.sh` instead of killing by PID. It matched only my own script. Every other kill was by PID, and the two 68-day cadical runs (PIDs 3026833/3026834) were not touched.

Files are in /tmp/e1122/seatO/: `enc.py`, `check.py`, `lemmaB.py`, `lemmaB2.py`, `enum8.py`, `crosscount.py`, `lemmaA.py`, `bt/bt.c`, `bt/mkin.py`, `wit/mycheck.py`, the formulas in `cnf/`, the proofs in `proofs/`, and the run logs (`*.log`, `bt/glue.log`, `wit/wit.log`, `proofs/certify.log`).