# #505 — OpenAI family 156, "A nine-dimensional counterexample to Borsuk's covering assertion": refereed + replayed (erdosproblemaday.com, 2026-10-20)

Page: https://erdosproblemaday.com/day/505-openai-borsuk-fails-in-dimension-nine-refereed

**Claim (OpenAI, 23 Sep 2026; public 6 Oct 2026, openai/math adc7f12, unchanged at 1581d4c):** X = {uuᵀ : u ∈ ℝ⁴, ‖u‖=1} in the 9-dim
trace-one symmetric 4×4 matrices (Frobenius metric) has diameter √2 and cannot be covered by ten sets of diameter < √2 ⇒ Borsuk fails in ℝ⁹.
Paper: see `paper/SOURCE.txt` (sha256 e7ffa6f8…; not redistributed here).

## replay/ — OpenAI's Lean, kernel-replayed
- Source: openai/math @ 1581d4cb, `lean/OAI/Geometry/Borsuk/` (269 modules, 78,964 lines; Lean 4.34.1, Mathlib d13f23b7; imports only Mathlib + itself).
  Source audit (grep): 0 axiom / sorry / native_decide / set_option / macro / elab / syntax / unsafe / implemented_by / extern / opaque / #eval / IO /
  Lean.Meta / ofReduceBool / maxHeartbeats; 19,594 `by decide` calls on 13,197 lines (19,574 in FiniteCases/; 4,093 case lemmas).
- `ESTIMATE.md` written before CPU. `drive.py` = lake-free DAG-parallel driver (≤ 4 lean at once, nice 19, LEAN_NUM_THREADS=1, launch gate
  MemAvailable ≥ 26 GB); `order.txt` = closure of OAI.Geometry.Borsuk.Main; `modules.tsv` = per-module rc / errors / max RSS / wall / olean sha.
  Result: 269/269 rc 0, 0 errors, 18:07:59Z → 18:36:48Z (28 min 49 s wall; Σ module wall 4,137 s; peak RSS 7,031,564 KiB ≈ 6.7 GiB).
- `post.sh` probes (`probe/`, logs in `logs/`): comparator module compiled; `Cmp.lean`/`Ax.lean` print pp.all of the theorem + the 6 definitions
  in the challenge and in the solution; `statement_match.py` → `statement_match.txt`: MATCH (main_theorem + projector, projectorSet,
  traceOneSymmetric, HasTenSmallCover, Vector4, Matrix4), solution axioms exactly {propext, Classical.choice, Quot.sound} for main_theorem,
  euclidean_nine_counterexample, no_admissible_ten, cover_to_admissible, FiniteObstruction.no_ten_system; comparator carries sorryAx.
  `mut/MUTATION_RESULTS.txt`: the matcher flags a changed numeral in HasTenSmallCover (MISMATCH), a challenge without sorryAx (CMP_SORRY_NOT_SEEN),
  a solution with an extra axiom (NONSTD). Controls: `Neg.lean` planted sorry → sorryAx; `TypeCtl.lean` (theorem re-typed as an 11-set
  statement) fails to elaborate (rc 1, Type mismatch at the expected term).
- leanchecker --fresh OAI.Geometry.Borsuk.Main: see `steps.tsv` row `leanchecker_fresh` + `logs/leanchecker_fresh.log` — rc 0 after 3587 s (Mathlib included, from scratch); missing-module control rc 1.

## bridge/ — Formal Conjectures' statements from OpenAI's theorem (ours)
`Bridge505.lean`: FC's `HasBorsukCover` / `BorsukConjecture` copied verbatim (FC @ 14c30813, `FormalConjectures/Wikipedia/BorsukConjecture.lean`,
notation from `FormalConjecturesForMathlib/Geometry/Euclidean.lean`), proves `borsuk_conjecture.not_nine`, `.not_forall` (= type of
`Erdos505.erdos_505`) and `borsuk_conjecture` (fails in 4..62) from `OAI.BorsukNine.euclidean_nine_counterexample`; compiled in OpenAI's env
(rc 0; `bridge.log`: all three on propext/Classical.choice/Quot.sound). Controls (`bridge_mut.log`, `bridge_wrongshape.log`): FC def mutated
< → ≤ fails at the strict-inequality step (`hsmall i` has type ≤); an 11-piece target fails on Fin 10 vs Fin 11. Not compiled in FC's own
environment (Lean 4.33.1, Mathlib 0df444a3).

## Ours (erdosproblemaday.com, 2026-10-20, 18:00Z erdos seat)

### finite/ — an independent encoding of the finite obstruction (paper §6; the Lean's `TenSystem`)
`tensystem_cnf.py` writes a CNF over 330 variables (210 tetrahedra q[S], 120 triangles t[U] on labels 0..9) for the six `TenSystem`
fields (down, pure, no_boundary, complementary, pair_count) + nonempty (q[{0,1,2,3}], WLOG by relabelling), or the paper's version
(no_boundary replaced by "every triangle in an EVEN number of tetrahedra"), with any field droppable. Written from the field
definitions, not from OpenAI's case files. `check_models.py` re-checks every SAT model with plain set logic (no clause reuse).
Results (CaDiCaL 2.x and Kissat, both): Lean variant UNSAT, paper variant UNSAT, both UNSAT; dropping pure / pair_count / nonempty
→ SAT (models re-checked: each violates exactly the dropped field); dropping no_boundary, complementary or down — singly or all three
together — stays UNSAT. So the minimal core is **pure + pair_count + nonempty**: once a tetrahedron exists, purity and the six-label
designs on facet complements already contradict; the "≥ 2 tetrahedra per triangle" property (and with it the paper's Lemmas 6.2–6.4) is
not needed at dimension 4 (it is still needed at dimension 3, inside Lemma 5.2, to get the designs).
All outputs incl. both rejection controls: `finite/cakelpr_runs.log` (⚠ cake_lpr exits 0 even when it REJECTS — read the printed verdict line).
Scope: the minimal-core claim is relative to OUR encoding (checked by reading it against `TenLabels/Labels.lean` + the drop-one controls); `finite/core_locality.py`
shows the contradiction needs designs on tetrahedra meeting S0 in 1 point (with down: sizes {4,3,1} or {4,2,1} suffice).
Certificates: CaDiCaL DRAT → drat-trim (VERIFIED, emits LRAT) → **cake_lpr** (CakeML-verified checker; `s VERIFIED UNSAT`) for
`ten_lean`, `ten_paper`, `core_min`. Controls: LRAT with the empty-clause step's last hint dropped → cake_lpr REJECTS at that step;
the ten_lean certificate against the same CNF with the nonempty unit neutralised (index-preserving, now SAT) → REJECTS.
`triangle_systems.py`: exactly 12 six-label triangle systems (Def 5.1), one S6-orbit, |Aut| = 60 with no transposition; Lemma 5.3
(1)–(4) hold on all 12; the hemi-icosahedron's 10 triangles are one of them.

### cover/ — eleven pieces suffice: b(X) = 11
`verify_cover.py` turns 11 float centres into EXACT rational unit vectors (inverse stereographic projection, denominators 10^6) and
enumerates every vertex of P = {x ∈ ℝ⁴ : ⟨x,c_i⟩² ≤ 1/2 ∀i} in Fractions (C(11,4) × 8 sign patterns): M = max |v|² = 0.903616716779…
(exact fraction in `cover/cover_n11_seed99.cert.json`; that was our first configuration — the page uses the world seat's 41.3852° one, below) < 1. Hence every unit x has max_i ⟨x,c_i⟩² ≥ 1/(2M) = 0.5533…, i.e. every line is within
41.9385° of one of the 11 lines (and this bound is attained: it is the exact covering radius). The sets A_i = {uuᵀ : ⟨u,c_i⟩² ≥ 1/(2M)}
are closed, cover X, and two lines in one A_i meet at angle ≤ 2·41.94° < 90°, so ‖uuᵀ − vvᵀ‖² = 2 − 2⟨u,v⟩² ≤ 2 − 2(1/M − 1)² =
1.97725 < 2. With OpenAI's Theorem 1.1: **b(X) = 11** (stated numerically, uncertified, by acprk/openai-math-followups on 10 Oct 2026; this is the certificate) (the paper: "does not determine … the exact value of b(X)").
Second and third instruments: float convex hull of {±c_i} (deep hole at 41.9385°, the same number to 1e-10); 10⁷ random lines + the
hull's deep holes — none below the certified bound. Controls: the D4 root system (12 lines, covering radius exactly 45°) and D4 minus
a root are REJECTED by the same verifier.
The 10-line statement (every 10 lines through the origin in ℝ⁴ leave a line at angle ≥ 45° from all of them) is the CAP case of Theorem 1.1
and already follows from Walkup 1970 (world seat; see below) — our searches never went below 45° (best 45.65°), consistent with it, not a test of OpenAI.

Best configurations (all exact-certified with `verify_cover.py` / `exact_radius.py`; logs `cover/verify_runs*.log`):
- 11 lines, covering radius 41.3852° (M = 0.888221984160505…): world seat's minimax search (`seats/w_scripts/`), `cover/seatW_best_K11_s11_vp.*` — the page's certificate;
  ours: 41.7107° (`cover_n11_seed11.*`), 41.9385° (`cover_n11_seed99.*`).
- 10 lines: 45.3320° (world seat, three of its four runs: `cover/seatW_best_K10_s20[123]_vp.*`); ours 45.6508° (`cover_n10_seed10.*`). Lower bound 45° = Walkup 1970
  (Prop. 8.1 + Thm 3; argument in `seats/seatW_world.md`), NOT a test of OpenAI's theorem.
- `search_n9.log` / `search_n12.log` are partial (stopped early by hand to lower box load).

## seats/
Three AI referee seats (Claude Opus 5.5, receipts in `MODEL_RECEIPTS.txt`), brief `COMMON.md`:
- `seatT_topology.md` — §§2–4, Lemma 5.2, Lemma 6.1: HOLDS AS READ (exposition only); `T_scripts/` incl. an explicit admissible ℝP² → Δ⁵ (positive control).
- `seatF_formal.md` — statement faithfulness + paper→Lean architecture map: HOLDS AS READ; the kernel route differs from the printed one (combinatorial
  Borsuk–Ulam/Smith-theory degree, homotopy-misses-a-ray purity, `no_free_ridge` instead of the F₂ cycle, §6 = 4,093 machine case lemmas).
- `seatW_world.md` — world/sources/novelty: HOLDS WITH FIXES (exposition): cap case follows from Walkup 1970; Kalai 2015 §2.4 proposed this set;
  b(X) = 11 stated numerically (uncertified) by acprk/openai-math-followups on 10 Oct; Grey–Weißbach 903 has Magdeburg preprint 97-25.
- Main seat's own reading of §§5–6 (Lemmas 5.3, 6.1–6.4, Theorem 6.5): HOLDS AS READ; Lemma 5.3 exhaustive in `finite/triangle_systems.py`.
- `blind_read.md` — blind read of the page before deploy (40 findings: 6 WRONG, 13 OVERCLAIM, 8 UNSUPPORTED, 13 UNCLEAR — all applied or banked); `main_reading_s5-6.md` — the main seat's own reading of §§5–6; `MODEL_RECEIPTS.txt` — per-seat model counts incl. zero other models.

## world/
Live captures of erdosproblems.com/505 (+ forum, proof-claims tab) fetched 2026-10-20 via our box; FC files @ 14c30813; acprk note @ 884a3637.

Reproduce: `python3 finite/tensystem_cnf.py out.cnf --variant lean` then cadical/kissat; `python3 cover/verify_cover.py cover/seatW_best_K11_s11_vp.json`
(exit 0 iff certified); replay: see `replay/drive.py` + `replay/post.sh` (paths are this machine's).
