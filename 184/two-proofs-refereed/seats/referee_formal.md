# Referee report — FORMAL side (statements, trusted base, source audit) — Erdős #184, family 181

Seat: hostile formal referee, 2026-10-20. Scope: statement fidelity of both Lean targets vs Erdős's problem, the
equivalence of the two targets, a draft bridge, and a text audit of both Lean trees. No `lean`/`lake`/`leanchecker`
was run (per brief); every Lean claim below is from reading source text. Kernel replays and the bridge compile are
separate, gated steps.

## VERDICT

**HOLDS WITH FIXES (1) · COULD NOT CHECK (kernel replays; bridge compile).**

* Both formal targets mean what Erdős asked (finite simple graph; partition of E(G) into edge sets of cycles of
  length ≥ 3 and single edges; at most C·n parts, C absolute). No loophole, no vacuity, found in either.
* The two targets are **equivalent** (on-paper proof, §3, both directions).
* **Fix needed (formal chain, not mathematics):** nothing anywhere kernel-checks that OpenAI's
  `OAI.ErdosGallai.MainStatement` implies FC's `Erdos184.erdos_184`, yet FC main (commit `3dfd999dfe`,
  2026-10-11) marks `erdos_184` `research solved` with `formal_proof … openai/math/…/Main.lean#L207` — a proof of a
  *different, equivalent* statement, on a *different toolchain* (Lean v4.34.1 / Mathlib d13f23b7 vs FC's v4.33.1 /
  Mathlib 0df444a3). A draft bridge is written: `/tmp/oaimath/181/seats/bridge_draft/Bridge.lean` (not compiled).
* Source audit: **both trees are clean** of sorry/admit/axiom/native_decide/implemented_by/extern/unsafe/csimp/
  opaque/partial/macro/elab/syntax/initialize/notation/run_cmd/#eval/addDecl/Lean-meta imports in proof code.
  Only benign hits (table §4).
* Coffey's tree proves FC's statement **verbatim**: `formal/comparator/Challenge.lean` is byte-identical to FC
  `184.lean` at `2424bb48` (sha256 `9f36e4e0…20d6`, git blob `36cc140c…`), and FC main's `erdos_184` statement
  is textually unchanged since then (only attributes/docstrings), same Mathlib pin, same toolchain.

## Findings by severity

**GAP (formal chain; fixable; does not touch the mathematics)**
- G1. *FC main cites a Lean proof that does not prove FC's statement.* FC main 184.lean:
  `@[category research solved, AMS 5, formal_proof using lean4 at "https://github.com/openai/math/blob/adc7f124…/lean/OAI/Combinatorics/CycleDecomposition/Main.lean#L207"]`
  on `theorem erdos_184 : ∃ f : ℕ → ℝ, (f =O[atTop] …) ∧ ∀ {V : Type*} … ∃ (D : Finset G.Subgraph), …`.
  Main.lean:207 is `theorem erdos_gallai : MainStatement := by`, whose statement is
  `∃ C : ℝ, 0 < C ∧ ∀ (n : ℕ) (G : SimpleGraph (Fin n)), ∃ k : ℕ, EdgeDecomposition G k ∧ (k : ℝ) ≤ C * n`.
  Different statement, different encoding of "cycle" (Walk.IsCycle edge set vs connected 2-regular subgraph),
  different vertex types (Fin n vs any Fintype in any universe), different toolchains — so the two cannot even be
  imported into one environment. Why it matters: until a bridge is compiled, "FC's erdos_184 is formally proved"
  rests on OpenAI's proof + an *unchecked* equivalence. Fix: compile `Bridge.lean` (draft provided) in the OpenAI
  environment; it copies FC's two definitions + statement verbatim (only namespace changed) and proves
  `theorem bridge : OAI.ErdosGallai.MainStatement → <FC statement>` and `Bridge184.erdos_184 := bridge erdos_gallai`.
  Residual after the fix: the copy-vs-original identity is textual + Mathlib-definitional (§2), not `Expr.equal`
  across environments (impossible across toolchains).

**UNCLEAR (trusted base — instructions for our own replay, not defects found)**
- U1. Coffey's load-bearing acceptance check is a **self-patched comparator**: `comparator fd5d5bcf` +
  `patches/comparator-fd5d5bcf-lean-v4.33.1.patch`, which (README) replaces `Kernel.Environment.replay` and
  back-ports a *soundness* fix (`Expr.getUsedConstants` skipping `Expr.proj` structure names; "Unpatched on v4.33.1,
  comparator **accepts** `proj_trick` (measured)"). We should not inherit that patch as trusted: replay with the stock
  v4.33.1 kernel checker on a fresh clone and do our own `pp.all`/`Expr.equal` of `EGCheck.erdos_184` (or the
  Solution's `Erdos184.erdos_184`) against `Erdos184.erdos_184` built from a fresh FC clone at 2424bb48.
  (Coffey's own `scripts/FinalCheck.lean` does exactly this check — `a.type.equal bty` and axioms exactly
  `{propext, Classical.choice, Quot.sound}` with sorryAx a FAIL — and reads like it does what the README says;
  it is still the author's tool.)
- U2. OpenAI's `lakefile.lean` requires ~30 third-party packages (iut, gromov, carleson, …) none of which is in the
  import closure of `OAI.Combinatorics.CycleDecomposition.Main` (closure = 34 family files + `import Mathlib`, in
  `Sampling.lean`). Their lakefiles still execute at configure time. A kernel replay neutralises this for proof
  validity; statement identity must be read off `pp.all` of the replayed constant, not off build logs.
- U3. OpenAI defines **three** textually identical copies of the target notions —
  `OAI.ErdosGallai.{CycleOrSingleEdge,EdgeDecomposition,decompositionCost}` (Decomposition.lean:13–22, 276),
  `OAI.ErdosGallai.Scale.*` (ScaleDecomposition.lean:222–231, 328), `OAI.ErdosGallai.Batch.*` (Templates.lean:102–111, 208)
  — glued in Main.lean by `main_cost_eq_scale … := by rfl` / `main_cost_eq_batch … := by rfl`. Harmless (rfl is
  kernel-checked), but the `pp.all` check must confirm `MainStatement` (PrefixSelection.lean:104–106, inside
  `namespace ErdosGallai`, only `open Finset`) mentions `OAI.ErdosGallai.EdgeDecomposition` — the comparator's name —
  and not the Scale/Batch copy. By source reading it does.

**COSMETIC / EXPOSITION**
- C1. FC `IsCycleOrEdge`'s right disjunct `H.edgeFinset.card = 1` admits a one-edge subgraph **with extra isolated
  vertices** (H.verts ⊋ ends of the edge). Harmless: decomposition is at edge-set level, and two members with the
  same nonempty edge set would violate `Set.PairwiseDisjoint`, so no double counting; padding only increases |D|.
  The left disjunct is strict (a cycle plus an isolated vertex fails both disjuncts) — also harmless.
- C2. FC's statement is universe-polymorphic (`erdos_184.{u_1}`, the `Type*` inside the theorem type), so `f` is
  chosen per universe. Harmless (both proofs give the uniform `f n = C·n`; every finite type in any universe is
  equivalent to some `Fin n`).
- C3. FC docstring now says "proved by an internal OpenAI model in September 2026 … see the linked Lean proof";
  the only artefact that proves FC's statement *verbatim* is Coffey's (submitted to the proof-claims tab
  2026-10-01 03:29Z, repo HEAD 660ae11 2026-10-01 03:21Z), pending our replay. Record-keeping, not a formal defect.
- C4. Coffey's public repo is a 3-commit snapshot of a private repo (`steelwheel01/Erdos-Proof bb4d8781…`); the
  development history (e.g. what `EG/Proof/Todo/*` — "Generated at the P2→P3 transition … replace `by sorry`" —
  looked like with sorries) is not inspectable. Trust does not depend on it (no sorry remains in code, §4).
- C5. Coffey's `EGCheck/Final.lean` uses `open Lean Elab Command in run_cmd do …` (a meta-check). It is advisory,
  not imported by `comparator/Solution.lean`, and only reads the environment. Benign.

## 1. Statement fidelity

### 1(a) FC `Erdos184.erdos_184` (2424bb48 = Coffey's target) and FC main (`c6f4b4bd`, 2026-10-19)

Fetched raw: `seats/fc/184_2424bb48.lean` (sha256 `9f36e4e0…20d6` = Coffey's Challenge.lean),
`seats/fc/184_main.lean` (`2ad4b57d…`), `seats/fc/Decomp_{2424bb48,main}.lean` (both `86bf339a…` — identical).
`diff 184_2424bb48 184_main`: only (i) two added references [OAI26a], [Py85]; (ii) docstring sentence crediting
OpenAI; (iii) attributes on `erdos_184` (open → solved + formal_proof link) and on `variants.lower_bound`
(formal_proof link); (iv) `variants.covering` rewritten from `answer(sorry) ↔ …` to the bare statement (marked
solved via Pyber); (v) BM docstring tense. **The `erdos_184` statement and `IsCycleOrEdge` are textually identical;
`SimpleGraph.IsDecomposition` is byte-identical; FC main still pins Lean v4.33.1 and Mathlib `0df444a3` (v4.33.1),
same as 2424bb48 and Coffey's lake-manifest.** History of 184.lean: 473f47c1 (09-30, covering fix), 99111aa0 (10-08,
lower-bound link), 3dfd999d (10-11, OpenAI link), 75a6d3d5/7db2ea3b (10-14, question tag/answer removal).

Elaborated form (Coffey's generated `formal/STATEMENT.md`, `pp.all`; consistent with my reading): the Fintype
instance on `↥H.verts` is `Subtype.fintype … (fun a => Classical.propDecidable (a ∈ H.verts)) inst`; membership
in `D` via `Finset.instSetLike`; 31 constants.

What `IsCycleOrEdge H.coe` admits (H : G.Subgraph, H.coe : SimpleGraph ↥H.verts, V finite):
- Left `H.coe.Connected ∧ H.coe.IsRegularOfDegree 2`: `Connected` = preconnected + `Nonempty ↥H.verts`. A finite
  connected simple graph with every degree exactly 2 is a cycle C_k, k ≥ 3, with vertex set exactly H.verts.
  Disjoint unions of cycles: excluded by connectivity. Extra isolated vertices: excluded (degree 0 ≠ 2).
  Empty subgraph: excluded (no Nonempty; and degree). Single vertex: degree 0. So left ⇔ "H is a cycle".
- Right `H.coe.edgeFinset.card = 1`: H has exactly one edge (edges of `H.coe` biject with `H.edgeSet` via
  `Sym2.map Subtype.val`, `Subgraph.image_coe_edgeSet_coe`), vertices arbitrary ⊇ its ends (C1).
- `IsDecomposition G D` = edge sets of distinct members pairwise disjoint ∧ ⋃ = G.edgeSet. Members are subgraphs of
  G so their edges are G-edges. Every member has ≥ 1 edge, so this is an honest edge partition with |D| parts.
- `∃ f, f =O[atTop] (n ↦ n) ∧ … (D.card : ℝ) ≤ f (card V)`: exactly O(n). (⇐ of "∃ C ∀ n ≥ 1 …" is trivial with
  f = C·n; the converse needs only that for the finitely many n below the IsBigO threshold N, |E| ≤ n(n−1)/2 ≤ N·n,
  see §3.) `[DecidableEq V]` is an extra hypothesis — harmless (it only weakens what must be proved, and every type
  has one classically).
- Vacuity: none. The bound must hold for every finite simple graph; complete graphs force real content.
- Universe: C2.

### 1(b) OpenAI `OAI.ErdosGallai.MainStatement`

`ComparatorChallenges/CycleDecomposition.lean` (39 lines; json: theorem `OAI.ErdosGallai.erdos_gallai`,
permitted axioms propext/Quot.sound/Classical.choice, `definition_names: []`, nanoda off). The solution-side
definitions are **textually identical** (Decomposition.lean:13–22 vs Challenge:15–25; PrefixSelection.lean:104–106
vs Challenge:28–30; same `namespace OAI … namespace ErdosGallai`, same `open Filter Asymptotics Real`,
`open scoped Topology`, `open MeasureTheory ProbabilityTheory Finset` context). Main.lean:207
`theorem erdos_gallai : MainStatement` in `namespace OAI … namespace ErdosGallai` — the comparator's exact type by
source reading (to be confirmed by `pp.all` after replay; U3).
- `CycleOrSingleEdge G s := (∃ v (p : G.Walk v v), p.IsCycle ∧ s = p.edgeSet) ∨ ∃ e ∈ G.edgeSet, s = {e}`.
  Mathlib `Walk.IsCycle` = trail (edges nodup) ∧ `p ≠ nil` ∧ `support.tail.Nodup` (Paths.lean:69–85) — a simple
  cycle; length ≥ 3 is forced (a closed walk of length 2 in a simple graph repeats its edge). `p` is a G-walk, so
  `p.edgeSet ⊆ G.edgeSet`. No loophole.
- `EdgeDecomposition G k := ∃ parts : Fin k → Set (Sym2 V), (∀ i, CycleOrSingleEdge G (parts i)) ∧
  Pairwise (Disjoint on parts) ∧ ⋃ parts = G.edgeSet`. Parts are nonempty, so pairwise disjointness forces them
  distinct; k is exactly the number of parts. Repeated/empty parts could only *raise* k.
- `MainStatement := ∃ C : ℝ, 0 < C ∧ ∀ n (G : SimpleGraph (Fin n)), ∃ k, EdgeDecomposition G k ∧ (k:ℝ) ≤ C * n`.
  C before n; only `Fin n` — enough, since decompositions transport along graph isomorphisms (§3). n = 0 forces
  k = 0 (fine: no edges). `{V : Type}` in the defs (Type 0 only) — irrelevant for Fin n, but it means the OpenAI
  predicate cannot be *stated* on `V : Type u`; the bridge therefore transports at the `Fin n` side (§5).
- Faithful to Erdős's problem. No vacuity.

### 2. Mathlib definitional stability between the two pins (0df444a3 ↔ d13f23b7)

The bridge lives in the OpenAI environment (d13f23b7) while FC's meaning is fixed in 0df444a3. I fetched the
relevant Mathlib files at 0df444a3 from upstream (`seats/mlcmp/v4331/`) and compared with d13f23b7
(`seats/mlcmp/d13f/`; d13f23b7 confirmed an upstream mathlib4 commit, "chore: bump toolchain to v4.34.1",
2026-09-24; local file hashes equal upstream). **Textually identical definitions** (modulo position):
`Subgraph` (structure), `Subgraph.coe`, `Subgraph.edgeSet`, `Subgraph.Connected`, `SimpleGraph.Connected`,
`Preconnected`, `Reachable`, `Walk.darts/edges/edgeSet`, `Walk.IsTrail/IsCircuit/IsCycle`, `neighborSet`,
`neighborFinset`, `degree`, `IsRegularOfDegree`, `edgeFinset`, `neighborSetFintype`, `fintypeEdgeSet`.
Diffs in these files are lemmas, deprecations, new instances on `incidenceSet` (unused here), and a
`Connected.connected_delete_edge_of_not_isBridge` reproof. Not checked: `Asymptotics.IsBigO`, `Finset`/`Fintype`
core, `Sym2` quotient core (Sym2.lean diff = 23 lines, deprecations + two simp lemmas) — standard, low risk.

## 3. On-paper proof: MainStatement ⇔ erdos_184

Notation: for `V` finite, `n = |V|`, `e : V ≃ Fin n` (`Fintype.equivFin`), `G' := G.comap e.symm` on `Fin n`
(`G'.Adj a b ↔ G.Adj (e⁻¹a) (e⁻¹b)`), `φ := Hom.comap e⁻¹ G : G' →g G`, injective.

**(⇒) MainStatement → erdos_184 (every universe).** Take C from MainStatement, f(n) := C·n; f =O n trivially.
Given V, G: apply MainStatement to (n, G'): parts P_1..P_k of E(G'), k ≤ Cn. For each i define H_i ≤ G:
- if P_i = p.edgeSet for a cycle p of G' at v: q := p.map φ is a cycle of G (injective maps preserve IsCycle);
  H_i := q.toSubgraph. Then E(H_i) = q.edgeSet = φ_*(P_i). H_i.coe is connected (Walk.toSubgraph_connected) and
  every vertex w of H_i has |N_{H_i}(w)| = 2 (IsCycle.ncard_neighborSet_toSubgraph_eq_two, w ∈ q.support), and
  N_{H_i.coe}(w) ≃ N_{H_i}(w) — so 2-regular. Left disjunct.
- if P_i = {s(a,b)} with G'.Adj a b: H_i := G.subgraphOfAdj (φ.map_adj): E(H_i) = {s(φa,φb)} = φ_*(P_i), one edge,
  so |E(H_i.coe)| = 1. Right disjunct.
D := {H_1,…,H_k} (Finset image), |D| ≤ k ≤ C·n = f(n). Disjoint: distinct members H_i ≠ H_j have i ≠ j, so
P_i ∩ P_j = ∅, and Sym2.map φ is injective, so E(H_i) ∩ E(H_j) = ∅. Union: ⋃ E(H_i) = φ_*(⋃P_i) = φ_*(E(G')) = E(G)
(⊆: E(H_i) ⊆ E(G); ⊇: x ∈ E(G) ⇒ Sym2.map e x ∈ E(G') and φ_*(Sym2.map e x) = x). ∎
(Universe: e : V ≃ Fin n is a heterogeneous-universe Equiv; nothing else depends on the universe.)

**(⇐) erdos_184 (at universe 0) → MainStatement.** f =O n gives c, N with |f(n)| ≤ c·n for n ≥ N. Put
C := max(c,0) + N + 1 > 0. Fix n, G on Fin n.
- n ≥ N: take D from erdos_184; enumerate D (Finset.equivFin) as H_1..H_k, k = |D| ≤ f(n) ≤ c·n ≤ C·n; parts
  P_j := E(H_j). Pairwise disjoint and covering by IsDecomposition (distinct indices ⇒ distinct members). Each P_j:
  if H_j.coe is connected 2-regular, it is a finite connected 2-regular simple graph, hence a single cycle through
  all its vertices and edges (walk from a vertex always leaving by the unused edge; finiteness closes it; the first
  repeated vertex is the start, else some vertex has degree ≥ 3; the closed cycle's vertices already have degree 2
  inside it, so it is a whole component = everything by connectivity). Its image under the injective inclusion
  H_j.coe →g G (Subgraph.hom) is a cycle walk p of G with p.edgeSet = Sym2.map val '' E(H_j.coe) = E(H_j). If
  instead |E(H_j.coe)| = 1 then |E(H_j)| = 1, E(H_j) = {e}, e ∈ E(G). So EdgeDecomposition G k.
- n < N: the single-edge decomposition (OAI's `edgeDecomposition_singleEdges`) has k = |E(G)| ≤ n(n−1)/2 ≤ N·n ≤ C·n.
  (n = 0: k = 0 ≤ 0.) ∎
(Mathlib for the cycle extraction: `SimpleGraph.IsCycles` Matching.lean:375 and
`IsCycles.exists_cycle_toSubgraph_verts_eq_connectedComponentSupp` Matching.lean:526; then equality of edge sets from
verts = univ and both sides 2-regular.)

So the two formal targets are equivalent; either Lean proof, if it replays, settles the other's statement modulo
a bridge, and the bridge needed for OpenAI→FC is the easy (⇒) direction.

## 4. Source audit

Method: Python scanner (`seats/tools/scan.py`, run with `python3 -I`) that blanks nested `/- -/` comments, `--`
comments and string literals, then counts word-bounded patterns: `sorry admit axiom native_decide ofReduceBool
decide:=true implemented_by extern unsafe csimp opaque partial macro(_rules) elab(_rules) syntax (builtin_)initialize
notation/infix/prefix/postfix set_option debug.*/skipKernelTC "import Lean…" run_cmd/run_tac/run_elab/run_meta
#eval addDecl/addAndCompile non-local attribute[…] instance(priority) export "open Lean" #exit Classical.choice`.
Positive controls: a synthetic file (sorry/axiom in code, in a comment, in a nested comment, in a string,
implemented_by, unsafe, set_option debug.skipKernelTC) scored exactly the code hits; Coffey's `formal/redteam/`
(41 attack files) lit up sorry 3, axiom 4, native_decide 1, implemented_by 1, extern 2, csimp 1, macro 3, elab 3,
initialize 2, skipKernelTC 3, Lean imports 16, #eval 5, addDecl 7. Raw JSON: `seats/tools/scan_{oai,coffey}.json`.

### OpenAI — `lean/OAI/Combinatorics/CycleDecomposition/*.lean` (34 files, 21,451 lines) + challenge

Repo HEAD 1581d4c (2026-10-12); `git diff adc7f124 HEAD` over these paths, the challenge, lakefile, manifest and
toolchain: **empty**; worktree clean. No comments or string literals at all in the 34 files. Imports: only
`import Mathlib` (Sampling.lean) and intra-family imports.

| file | lines | hits (code only) |
|---|---:|---|
| ComparatorChallenges/CycleDecomposition.lean | 39 | sorry 1 (the challenge placeholder, by design) |
| BatchEndpoints | 276 | — |
| BatchIndexing | 499 | `attribute [instance]` ×2 (309 `GraphBatches.finite`, 428 `ActiveFamily.finite`) |
| BatchLovasz | 1607 | — |
| BatchPathDeletion | 736 | — |
| BatchPreparation | 1035 | — |
| BatchResolution | 468 | `attribute [instance]` 230 `BatchTemplateFamily.finiteIndex`; `Classical.choice` 378 |
| BatchRouting | 1101 | — |
| CollisionEstimates | 549 | — |
| CostRegrouping | 405 | — |
| CoupledResolution | 818 | `Classical.choice` 784 |
| CycleLifting | 836 | — |
| Decomposition | 515 | — |
| DepthFirstSearch | 198 | — |
| EdgeSplitting | 404 | — |
| EndpointPartition | 276 | — |
| ExpansionBoxes | 659 | — |
| LayerCosts | 345 | — |
| Lovasz | 1606 | — |
| Main | 227 | — |
| Pairing | 836 | — |
| PathDeletion | 736 | — |
| PrefixSelection | 112 | — |
| Representatives | 265 | `Classical.choice` 26, 216 |
| ReservoirCycles | 776 | `Classical.choice` 391 |
| ReservoirRemainder | 742 | — |
| ReservoirSampling | 399 | — |
| Routing | 1041 | — |
| Sampling | 389 | — (holds `import Mathlib`) |
| SamplingCuts | 714 | — |
| ScaleDecomposition | 633 | — |
| ScaleExtraction | 623 | — |
| ScaleHierarchy | 576 | — |
| Templates | 785 | `attribute [instance]` ×2 (431 `CycleOutline.finiteW`, 608 `RoutingTemplate.finiteArity`) |
| UniformLayers | 298 | — |

All hits benign: global `attribute [instance]` on `Finite`-valued structure fields (typeclass resolution only;
cannot touch the kernel); `Classical.choice` term uses are a permitted axiom. Zero `set_option`, zero `sorry`
outside the challenge. `attribute [local instance] Classical.propDecidable` occurrences are `local` (excluded).

### Coffey — `formal/{EG,EGTest,EGCheck}/**`, `formal/comparator/*.lean`, roots, `lakefile.toml` (647 files, 105,221 lines)

Worktree clean at 660ae11. EG = 601 files (Defs 53 / Lib 183 / Proof 243 / Spec 122), all `module`s.
Imports: EG imports only `Mathlib.*` and `EG.*`; only EGCheck (and comparator/*) import FormalConjectures*;
no `import Lean`/`Lean.Elab`/`Lean.Meta` anywhere in proof code.

| path | files | lines | hits (code only) |
|---|---:|---:|---|
| EG.lean | 1 | 606 | — |
| EG/Defs | 53 | 7,242 | — |
| EG/Spec | 122 | 11,318 | — |
| EG/Lib | 183 | 50,953 | set_option ×14: `linter.unusedSimpArgs false` ×4 (Chain/CherrySystem 85–97), `linter.unusedSectionVars/unusedVariables false` ×4 (Ext/LovaszCons 31–32, Ext/LovaszThm 25–26), `maxHeartbeats 1000000` ×6 (Vortex/PVProb 28, PVRunStep 92, TPVProb 101, TPVStepMain 32, VXProb 176, VXStepMain 29) |
| EG/Proof | 243 | 24,283 | set_option `maxHeartbeats 1000000` ×1 (Todo/CCPartner 41) |
| EGTest + root | 38 | 10,062 | — |
| EGCheck + root | 5 | 539 | `open Lean Elab Command in` + `run_cmd do` (Final.lean 44–45; advisory read-only meta-check, C5) |
| comparator (Challenge, Solution) | 2 | 218 | sorry ×7 — all in Challenge.lean = the upstream FC file's own sorries (erdos_184 + 5 variants + `answer(sorry)`), by design |
| lakefile.toml | — | — | leanOptions `pp.unicode.fun`, `autoImplicit=false`, `relaxedAutoImplicit=false`, `maxSynthPendingDepth=3`; no moreLeanArgs/plugins; FC pinned 2424bb48, Mathlib v4.33.1 (manifest 0df444a3) |

Raw-text `sorry` appears in 122 files of EG/EGTest/EGCheck, but only inside comments ("No `sorry`.", "replace `by sorry` with
the proof" in the `EG/Proof/Todo/*` generated headers) — zero in code. Zero `axiom`, `admit`, `native_decide`,
`implemented_by`, `extern`, `unsafe`, `opaque`, `partial`, `macro`, `elab`, `syntax`, `initialize`, notation, `#eval`,
`addDecl`, `debug.*`.

Coffey's checks, read against their claims:
- `comparator/Challenge.lean`: sha256 `9f36e4e053285cd8b886042eb609ace5f21f49bd81903eebca8000ff03e020d6` (computed)
  = FC 2424bb48 raw (computed); git blob `36cc140cb3d8e60b08a842f1691fe9b73602f92b` (computed) = README.
- `comparator/Solution.lean` vs Challenge: diff = an added modification notice, two private imports
  (`EG.Proof.Main`, `EGCheck.BridgeCore`), the `erdos_184` proof (`obtain … := EGCheck.Bridge.of_mainInternal_unfolded
  EG.Proof.mainInternal; exact ⟨f, hf, fun G => (hD G).imp fun _ hD => ⟨fun H hH => hD.1 H hH _ _, hD.2⟩⟩`), and the
  five `variants` removed. `IsCycleOrEdge` and the statement verbatim.
- `EGCheck/Final.lean`: `theorem EGCheck.erdos_184.{u} : type_of% @_root_.Erdos184.erdos_184.{u} := EGCheck.Bridge.solution`,
  `#guard_msgs` on `#print axioms` = `[propext, Classical.choice, Quot.sound]`, and a `run_cmd` checking module
  origin of the upstream constants, kinds, universe count, and `a.type.equal bty`. Advisory (in-band), as it says.
- `scripts/FinalCheck.lean` (1025 lines, `importModules … loadExts := false`): `checkStatement` = universe-count
  equality + `a.type.equal (b.type.instantiateLevelParams …)`; `checkAxioms` = own traversal, passes iff the
  non-sorry axiom set is exactly the three, sorryAx a FAIL unless `--allow-sorry`, cross-checked with
  `collectAxioms`; plus `replay` (kernel re-check of every project constant), `origin`/duplicate-merge defence,
  `policy`, `meta`, closure `pin`. **It checks what the README says.** (Still the author's tool — U1.)
- Coffey's bridge (`EGCheck/BridgeLemmas.lean`, `BridgeCore.lean`) uses the same instance-generic trick as my draft:
  prove the `IsCycleOrEdge` body for arbitrary `i₁ : H.coe.LocallyFinite`, `i₂ : Fintype H.coe.edgeSet`, transport
  along `Fintype.equivFin` via `G.comap e.symm`. Its correctness is kernel-checked against FC's constant, so its
  internal `EG.Spec.MainInternal` encoding does not need a separate fidelity review for the *theorem's* truth.

## 5. Lean plan for MainStatement → erdos_184, and the draft

File: **`/tmp/oaimath/181/seats/bridge_draft/Bridge.lean`** (≈190 lines; imports `Mathlib` +
`OAI.Combinatorics.CycleDecomposition.Main`; namespace `Bridge184`). Contents:
1. `Bridge184.IsDecomposition` — verbatim body of FC `SimpleGraph.IsDecomposition`.
2. `Bridge184.IsCycleOrEdge` — verbatim FC def (incl. `open scoped Classical in`).
3. `degree_eq_ncard`, `card_edgeFinset_eq_ncard` — instance-generic counts (ported from Coffey, Mathlib names
   checked in d13f23b7); `mem_edgeSet_comap`.
4. `exists_sub` — one OpenAI part on `G'` pushed along an injective `φ : G' →g G` is `H.edgeSet` of an
   `H : G.Subgraph` satisfying the `IsCycleOrEdge` body for all instances (cycle: `(p.map φ).toSubgraph`;
   edge: `G.subgraphOfAdj (φ.map_adj hx)`).
5. `per_graph_aux` (any `e : V ≃ Fin m`) and `per_graph` (`e := Fintype.equivFin V`, `V : Type u`).
6. `theorem bridge : OAI.ErdosGallai.MainStatement → <FC erdos_184 statement verbatim>` with `f n = C * n`,
   closing `IsCycleOrEdge H.coe` by `hcyc H hH _ _` (kernel unfolds the def, instantiates the classical instances).
7. `theorem Bridge184.erdos_184 : <verbatim> := bridge OAI.ErdosGallai.erdos_gallai` and `#print axioms` (expect
   exactly propext, Classical.choice, Quot.sound).

Mathlib (d13f23b7) names used, with locations (all under `Mathlib/`):
- `SimpleGraph.Walk.IsCycle.map` (alias of `isCycle_map_iff_of_injective`.mpr) — Combinatorics/SimpleGraph/Paths.lean:1126–1132
- `SimpleGraph.Walk.edgeSet_map` — Combinatorics/SimpleGraph/Walk/Maps.lean:107
- `SimpleGraph.Walk.edgeSet_toSubgraph` — Combinatorics/SimpleGraph/Connectivity/Subgraph.lean:215
- `SimpleGraph.Walk.toSubgraph_connected` — Connectivity/Subgraph.lean:507; field `Subgraph.Connected.coe` — :48–49
- `SimpleGraph.Walk.IsCycle.ncard_neighborSet_toSubgraph_eq_two` — Connectivity/Subgraph.lean:438
- `SimpleGraph.Walk.mem_verts_toSubgraph` — Connectivity/Subgraph.lean:188
- `SimpleGraph.Subgraph.coeNeighborSetEquiv` — Combinatorics/SimpleGraph/Subgraph.lean:244
- `SimpleGraph.Subgraph.image_coe_edgeSet_coe` — Subgraph.lean:261; `Subgraph.edgeSet_subset` — :252
- `SimpleGraph.subgraphOfAdj` — Subgraph.lean:86; `SimpleGraph.edgeSet_subgraphOfAdj` — Subgraph.lean:963
- `SimpleGraph.card_neighborSet_eq_degree` — Combinatorics/SimpleGraph/Finite.lean:247; `coe_edgeFinset` — Finite.lean:63
- `SimpleGraph.Hom.comap` (`@[simps]`) — Combinatorics/SimpleGraph/Maps.lean:412; `Hom.map_adj` — Maps.lean:338;
  `comap_adj` — Maps.lean:130 (alt.: `Iso.comap` — Maps.lean:704)
- `Fintype.equivFin` — Data/Fintype/EquivFin.lean:80 (noncomputable, no DecidableEq needed)
- `Nat.card_eq_fintype_card`, `Nat.card_congr` — SetTheory/Cardinal/Finite.lean:45, 91; `Nat.card_coe_set_eq` —
  Data/Set/Card.lean:627 (rfl); `Set.ncard_coe_finset` :666; `Set.ncard_singleton` :694; `Set.ncard_image_of_injective` :826
- `Sym2.map_mk` (rfl) — Data/Sym/Sym2.lean:267; `Sym2.map.injective` :269; `Sym2.map_map` :263; `Sym2.map_id` :255
- `Set.disjoint_image_of_injective` — Data/Set/Image.lean:1358; `Set.image_singleton` — :275
- `Finset.card_image_le` — Data/Finset/Card.lean:233; `Finset.mem_image`, `Set.mem_iUnion₂`, `Set.mem_iUnion`
- `Asymptotics.isBigO_refl` — Analysis/Asymptotics/Basic.lean:372; `Asymptotics.IsBigO.const_mul_left` — Analysis/Asymptotics/Ring.lean:46

Patterns copied from code that already compiles on d13f23b7 (OAI Decomposition.lean): `rcases hs with
⟨v,p,hp,rfl⟩ | ⟨e,he,rfl⟩` on `CycleOrSingleEdge`; `hp.map hf`; `induction e using Sym2.ind with | _ x y =>
… f.map_adj he`; `obtain ⟨parts, …⟩ := (h : EdgeDecomposition …)`. Patterns copied from Coffey (compiled on
0df444a3): the degree/edge-count rewrites, `mem_edgeSet_comap`, the `isBigO_refl … const_mul_left` term, the
`Set.PairwiseDisjoint` intro shape.

Compile-risk points for the main seat (most likely edits if it fails):
1. `have hφ : Function.Injective φ := e.symm.injective` and `have hHe' … := hHe` rely on `⇑(Hom.comap ⇑e.symm G)`
   being defeq to `⇑e.symm` (true by `@[simps]`/rfl; if `exact` balks, use `by intro a b h; simpa [φ] using h`
   and `fun i => by simpa [φ] using hHe i`).
2. `rw [Walk.edgeSet_toSubgraph, Walk.edgeSet_map]` and `rw [edgeSet_subgraphOfAdj, Set.image_singleton, Sym2.map_mk]`
   are expected to close by `rfl`; if a goal survives add `rfl`.
3. `unfold OAI.ErdosGallai.MainStatement at h` — if `unfold` complains, `obtain ⟨C, -, hmain⟩ := h` directly
   (rcases unfolds defs).
4. Name resolution: helper names were grepped against Mathlib d13f23b7 — no `SimpleGraph.degree_eq_ncard`,
   `card_edgeFinset_eq_ncard`, `mem_edgeSet_comap`, `IsDecomposition`, `IsCycleOrEdge` exist, so `open SimpleGraph`
   creates no ambiguity.
5. After it compiles, the meaningful check is a textual diff of the copied defs/statement against FC 2424bb48
   (only the namespace prefix may differ) plus `#print axioms Bridge184.erdos_184`.

## What I could not check

- Any kernel replay (OpenAI 34-file closure; Coffey 601+ modules), any `pp.all` of the replayed constants, the
  bridge compile. All gated to the main seat.
- `Expr.equal` of the bridge's copied statement with FC's constant (impossible across toolchains; mitigated by §2).
- Mathlib definitional identity for `Asymptotics.IsBigO`, Finset/Fintype/Sym2 core between the two pins (not
  diffed; standard and low risk).
