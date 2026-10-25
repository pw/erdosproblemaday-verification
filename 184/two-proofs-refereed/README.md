# Erdős #184 — three claimed proofs refereed, both Lean proofs kernel-replayed, and a bridge to Formal Conjectures' statement

erdosproblemaday.com entry: `/day/184-erdos-gallai-three-proofs-two-lean-replays-and-a-bridge` (2026-10-20).

**The problem.** "Any graph on n vertices can be decomposed into O(n) many edge-disjoint cycles and edges" (Erdős–Gallai;
erdosproblems.com/184). Record before October 2026: O(n log* n) (Bucić–Montgomery).

**The claims under review.**
- Ryan Coffey (github.com/steelwheel01/erdos-gallai-lean, public 2026-10-01 00:12:30Z; paper 152 pp, sha256 3bc03240…;
  Lean: 601 files, Lean 4.33.1 / Mathlib 0df444a3; proves Formal Conjectures' `Erdos184.erdos_184` verbatim). `papers/coffey_sha256_and_log.txt`.
- Jaehoon Kim, arXiv:2610.07840 (v1 2026-10-06 06:42:42Z, v2 2026-10-09; no Lean).
- OpenAI, "A linear cycle-and-edge decomposition of every graph" (family 181 of github.com/openai/math, repo created
  2026-10-06 21:47:02Z; preprint self-dated 24 Sep; main.pdf sha256 4aa44187…; Lean: 34 files / 21,451 lines,
  Lean 4.34.1 / Mathlib d13f23b7; proves `OAI.ErdosGallai.MainStatement`, NOT FC's statement). `papers/openai_paper_sha256_and_rev.txt`.

## What is here

| path | what |
|---|---|
| `replay/openai/` | Lake-free kernel replay of OpenAI's 34 modules (`build.sh`, `ESTIMATE.md` written before CPU, `steps.tsv`, `modules.tsv`, per-module logs, probes, `statement_match.{py,txt}`, `leanchecker --fresh` log) |
| `replay/coffey/` | `lake build` of Coffey's tree at a11bb45 (Lean sources identical to HEAD 660ae11: `git diff --stat a11bb45 660ae11 -- formal/` = two .md files), our own check file `probe/OurCheck.lean`, controls, `leanchecker --fresh` log |
| `bridge/` | **Ours.** `Bridge.lean`: FC's `erdos_184` (definitions copied verbatim, namespace renamed) proved from OpenAI's `erdos_gallai` inside OpenAI's environment; controls; `pp_compare.py` + `InstDefeq.lean` (copy-vs-original checks across the two toolchains) |
| `seats/` | Referee brief + reports: `referee_openai.md`, `referee_coffey.md` (+ `_BMtable`, `_LEANmap` helper passes), `referee_formal.md`, `referee_world.md`, `referee_kim.md`; their check scripts (`openai_checks/`, `kim_checks/` (the 03:00Z seat's first Kim scripts), `referee_kim_checks/` (the Kim seat's re-runs and its own §6 checks), `coffey_scripts/`, `tools/scan.py` source scanner with its JSON output, `fc/` FC sources at 2424bb48 and main) |
| `world/` | Captures: erdosproblems.com/184 page, proof-claims tab, comment thread; FC 184.lean at the pin and at main + diff; teorth DB row |
| `papers/` | sha256 + commit logs of the reviewed artefacts |

## Results

Both replays compile the project's own modules (and, for Coffey, Formal Conjectures' modules) from source against Mathlib's
published build cache (`lake exe cache get`; OpenAI: 8,529 Mathlib oleans present before the build, `replay/openai/driver.log`);
`leanchecker --fresh` then re-checks every declaration in each import closure, Mathlib included.

**OpenAI replay** (`replay/openai/steps.tsv`): 34/34 modules rc 0 in 493 s, one thread, nice 19, against the pinned Mathlib
(openai/math 1581d4c; `git diff adc7f124 1581d4c` over the family, the challenge, toolchain and manifest is empty).
`#print axioms OAI.ErdosGallai.erdos_gallai` = [propext, Classical.choice, Quot.sound]. `statement_match.txt` = MATCH /
STD_AXIOMS / CMP_SORRY_SEEN: the pp.all of `MainStatement`, `EdgeDecomposition`, `CycleOrSingleEdge` in the solution
environment equals that of the comparator challenge module elaborated on its own (which shows `sorryAx`, as a challenge must).
Negative control on that instrument (09:00Z seat): one token of the solution-side `MainStatement` print changed (`Nat.cast` →
`Int.cast`, `logs/axioms_mutated_for_negcontrol.log`) → `MainStatement MISMATCH` (`logs/statement_match_negcontrol_mutated.log`).
WrongShape (k ≤ C, constant bound) rc 1 with "Type mismatch … erdos_gallai has type MainStatement"; NegControl (planted sorry)
shows sorryAx. `leanchecker --fresh OAI.Combinatorics.CycleDecomposition.Main` rc 0 after 3,680 s; missing-module control rc 1.

**Coffey replay** (`replay/coffey/steps.tsv`): `lake build EG EGTest EGCheck EGCheck.Final` — 9,574 jobs, 1,755 s, toolchain
v4.33.1 (scratch elan, sha verified), Formal Conjectures fetched by lake at 2424bb48 and `FormalConjectures.ErdosProblems.«184»`
built from that source. `probe/OurCheck.lean`: `theorem ours184.{u} : type_of% @_root_.Erdos184.erdos_184.{u} := @EGCheck.erdos_184.{u}`
— the TYPE comes from FC's own module, the term from Coffey's — elaborates; axioms [propext, Classical.choice, Quot.sound].
We did NOT use Coffey's comparator (he runs it with his own patch, `comparator/patches/…`, which back-ports a soundness fix).
Controls: `probe/WrongShape2.lean` (constant bound, same binders, `open scoped Classical`) rc 1 with "Type mismatch
EGCheck.erdos_184 has type ∃ f, …"; its positive twin `probe/RightShape2.lean` (FC's bound) rc 0, standard axioms;
NegControl (planted sorry on FC's type) shows sorryAx. `leanchecker --fresh EGCheck.Final` rc 0 after 3,673 s; missing-module
control rc 1. ⚠ The first constant-bound control (`probe/WrongShape.lean`, 03:00Z seat) failed for the WRONG reason — "failed to
synthesize Fintype ↑H.verts" (no classical instance in scope) — so it tested nothing; it is kept, superseded by WrongShape2/RightShape2.

**The bridge (ours)** (`bridge/`): `Bridge.lean` compiled unchanged from the formal seat's 03:19Z draft
(`Bridge_draft_0319Z.lean`, byte-identical) with `lean --trust=0` in OpenAI's environment (LEAN_PATH in
`replay/openai/lean_path.txt`): rc 0 (100 s cold / 11 s warm, 6.8 GB); `Bridge184.erdos_184` depends on [propext, Classical.choice,
Quot.sound]. The header comment of `Bridge.lean` was then rewritten (DRAFT note removed; Apache-2.0 attribution to Coffey's
`EGCheck/BridgeLemmas.lean` + `BridgeCore.lean` added; code below `namespace Bridge184` byte-identical to the draft) and the file
and all controls were re-run: `logs/*_v2.log`, `logs/bridge_controls_v2.tsv` (first run's logs in `logs/v1_draft_header/`).
Controls (`logs/bridge_controls_v2.tsv`): `BridgeWrong.lean` (FC statement with O(1) in place of O(n)) rc 1 type mismatch;
`BridgeEdgesOnly.lean` (copied IsCycleOrEdge reduced to "exactly one edge") rc 1 type mismatch; `BridgeSorry.lean` → sorryAx.
Copy vs original — the two cannot share an environment (Lean 4.33.1/Mathlib 0df444a3 vs 4.34.1/d13f23b7):
- `pp_compare.py replay/coffey/logs/ourcheck.log logs/BridgePP.log` → `pp_compare.out`: FC's `erdos_184` statement (1,460 chars)
  and `IsCycleOrEdge` (930 chars) IDENTICAL to our copies after renaming the namespace; `IsDecomposition` differs only in the
  instance path to `PartialOrder`/`OrderBot` on `Set (Sym2 V)` (Mathlib's lattice hierarchy changed between the pins). Controls:
  a one-token mutation (`Finset.card` → `Finset.sum`) → MISMATCH exit 1 (`pp_compare_mutated.out`); empty input → CANNOT SEE exit 2.
- `InstDefeq.lean`: both instance paths written out explicitly; the two `Set.PairwiseDisjoint` propositions proved equal by
  `Iff.rfl` — rc 0 in OpenAI's environment (`logs/instdefeq_oai.log`) AND in Coffey's/FC's (`logs/instdefeq_coffey.log`);
  `InstDefeqNeg.lean` (one side's function complemented) rc 1.
- Residual: textual + definitional identity across two toolchains, not one `Expr.equal`; the Mathlib definitions the statement
  unfolds to were compared file by file between the pins by the formal seat (`seats/referee_formal.md` §2).
- Attribution: `degree_eq_ncard`, `card_edgeFinset_eq_ncard`, `mem_edgeSet_comap`, the instance-generic strategy and the
  `isBigO_refl … const_mul_left` term are taken from Coffey's `formal/EGCheck/BridgeLemmas.lean` / `BridgeCore.lean` (Apache-2.0);
  the transport from OpenAI's `MainStatement` (`exists_sub`, `per_graph_aux`, `per_graph`, `bridge`) is ours.
- `pp_compare.py` stops a block at a `/usr/bin/time` line (`maxrss_kb=`): the v2 log carries one, and before that fix the script
  reported MISMATCH on it (the instrument failing as it should); re-controlled after the fix: real 0, mutated 1, empty 2.

**Referee seats** (all briefed to refute, quote, and not to run Lean; every seat — the 03:00Z seat's five and the 09:00Z seat's
Kim seat and blind page reader — was served by `claude-opus-5-5`, read from the transcripts' `model` field; the same model Coffey's
proof claim names, so these readers are not independent of his tooling): OpenAI paper HOLDS WITH FIXES (expository only; 64
numeric checks 0 FAIL; lifting simulation 16,000 instances / 200,092 lifted cycles, three negative controls each break it).
Coffey HOLDS AS READ on the load-bearing chain, HOLDS WITH FIXES on citations/status prose, COULD NOT CHECK the §3–§5 device
lemmas line by line (the Lean is the evidence there); paper and Lean diverge at JS-LC Steps 4–5 and the MIX-C assembly
(DEVIATIONS.md D1–D36). Formal seat: both statements faithful, equivalent (proof on paper both ways), trees clean of
sorry/axiom/native_decide/etc. (scanner with positive controls). World seat: timeline, credit lines, no human verification on
record. Kim seat (09:07–09:24Z, v2 TeX line by line): HOLDS AS READ, nothing above EXPOSITION; citations (BM Def 11, Lemma 14, Cor 22,
Thm 24; CFS Cor 4.3, Lemma 4.4) checked in source; BM Lemma 14 / Thm 24 not re-proved; numerics in `seats/referee_kim_checks/`
(104/104 PASS on the constants; Lemmas 3.1/3.2/6.5/6.7/6.8 on small instances, each with a failing negative control).

## Reproduce
1. OpenAI: clone github.com/openai/math at 1581d4c (or adc7f124), `lake exe cache get` for Mathlib d13f23b7 in a mathlib4
   checkout, then `replay/openai/build.sh` (edit the paths at its top; it builds `order.txt` one module at a time).
2. Coffey: clone github.com/steelwheel01/erdos-gallai-lean, `cd formal && lake exe cache get && lake build EG EGTest EGCheck
   EGCheck.Final`, then `lake env lean --trust=0 replay/coffey/probe/OurCheck.lean` and the probes.
3. Bridge: with OpenAI's LEAN_PATH, `lean --trust=0 bridge/Bridge.lean` (and the four control files); `lean bridge/InstDefeq.lean`
   in both environments; `python3 bridge/pp_compare.py <ourcheck.log> <BridgePP.log>`.

`SHA256SUMS` covers every file in this directory.
