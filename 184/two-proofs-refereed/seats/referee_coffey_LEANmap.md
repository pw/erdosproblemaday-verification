# Hostile referee map: Coffey paper vs Lean formalization (load-bearing statements)

Repo: `/tmp/oaimath/181/coffey/repo`. I read the Lean as text only. Nothing was built or run: no lean, lake or leanchecker.
Paths are relative to the repo root. "Paper" means `paper/src/*.tex` (final). "v6.1" means `proofs/manuscript/*.tex`.
I diffed v6.1 against the final paper for s2, s5, s6 and s7. For every statement compared below, the
statement text is identical except for the errata noted, which are 14^τ(b) wording and 14^τ(c) `τ>0`.

Helper scripts (mine, read-only on the repo) are in `/tmp/oaimath/181/seats/coffey_scripts/`:
`closure.py` computes the module import closure of `EG.Proof.Main` (481 modules, 98 of them `EG.Spec.*`);
`strip_scan.py` strips comments and strings and scans for `sorry/admit/axiom/opaque/extern/implemented_by/unsafe`.
It found **0 hits** in `formal/EG` and `formal/EGCheck`, so the textual "no axiom / no sorry" claim holds.

## Bottom line

* I found **no FATAL and no GAP for the formal theorem.** The chain from `EG.Proof.mainInternal` to `erdos_184` is
  closed. Every hypothesis of every Spec on the route is discharged by a proved theorem, and none is a
  structure field or argument that is left assumed (§7, §8).
* Statement-level fidelity is good. JV⁺*, HI″, CONC-L(iv), propOV(K2), K-RED's bound and 14^τ(b) agree
  with the paper in meaning. The constants agree **formula by formula**: C₀, ε₁, ε₂ = θ_Q, F, det_l, ε_X, ε_U, ε_K, ε_A,
  ε_CONC, ε_M, c_EG.
* The real differences sit at the **MIX-C / K-RED / Lift(iii) assembly layer**. There the Lean statements are
  deliberately weaker or restructured (Option B′, ORDER-DECOUPLE, stage 3 made deterministic). The paper's own
  interleaved assembly argument is therefore **not machine-checked**. Only its conclusions are, by a different route.
  This matters if someone claims "the paper's proof is formally verified". It does not matter for the truth of the Lean theorem.

---

## 0. Is the main route really using these statements?

`formal/EG/Proof/Main.lean`:
* `hiHyp_of_gammaCond` (l.57) calls `EG.Todo.ExistsRun` (l.60, with `hΓ.gamma1core` only),
  `exists_isDesignation` (l.62), and `EG.Todo.JVps V G N0 D run δ hN hΓ hn hd1 hrun hδ` (l.65). It also converts
  `D ≤ 2|E|/n` to `D ≤ run.d G 1` by `simpa [Run.d, Run.graph_one, Round.d]` (l.63-64).
* `mainInternal` (l.74) uses `EG.exists_gammaCond` and then `mainInternal_of_hiHyp` (`Proof/Quot/HIMain.lean:55`), which
  calls `EG.hi : HIStatement` (`HIMain.lean:33`).

The constant-level references I traced by grep:

| Spec compared | Theorem on route | How it is reached |
|---|---|---|
| `JVpsStatement` | `EG.Todo.JVps` | direct (Main.lean:65) |
| `HIStatement` | `EG.hi` | HIMain.lean:33 |
| `CostStatement` | `EG.Todo.Cost` | Proof/Todo/JVps.lean:39 |
| `OneOutcomeStage1Statement` | `EG.Todo.OneOutcomeStage1` | JVps.lean:37 |
| `UHsplitThetaStatement` | `EG.Todo.UHsplitTheta` | JVps.lean:50 |
| `MixCStatement` | `EG.Todo.MixC` | Proof/Todo/Cost.lean:54 |
| `MixCConcStatement` → `ConcLSumStatement` | `EG.Todo.MixCConc` → `EG.concLSum` | Cost.lean:64; MixCConc.lean:23 |
| `LemKREDStatement` | `EG.Todo.LemKRED` | argument of `mixc_of_specs` (Proof/Todo/MixC.lean:37) |
| `OVRunStatement` (K2) | `EG.Todo.OVRun` | via `EG.Todo.TowerE` (Proof/Todo/TowerE.lean:77, used in MixC.lean:37) and Vstar.lean:69 |
| `L14OVStatement` (14^τ(b)) | `EG.l14OV` | via `EG.Todo.OVRound` → `OVRun` |
| `LiftJConsumerRunStatement` | **not the Spec theorem** `EG.liftJConsumerRun`; a verbatim `Type u` copy `EG.liftJConsumerRun_univ` | `Lib/Quot/LiftUniv.lean:108`, used in Cost.lean:48,51 and Lib/Quot/CostRound.lean:61 |
| `LiftDecompStatement` | **not** `EG.liftDecomp`; the identical Lib lemma `Quot.Rules.liftDecomp_core` | `LiftUniv.lean:33`; `EG.liftDecomp` is literally `liftDecomp_core` (Proof/Quot/Lift.lean:159-161) |
| `LiftAccountingStatement` (Lift(iii)) | **no consumer** (`EG.liftAccounting` is referenced nowhere) | — |
| `L14ThinStatement` (14^τ(c),(d)) | **no consumer** (`EG.l14Thin` is referenced nowhere outside its own file) | ORIGIN(b) instead uses `STree.thinCut_lt` (`Lib/HB/SEP.lean:230`) |

CORRESPONDENCE.md's "in closure" (no ○) is a **module-level** import closure. The file says so at CORRESPONDENCE.md:111-121
("only means the final theorem *can* use them"). So `L14Thin`, `LiftAccounting`, and the Spec-level `liftDecomp` /
`liftJConsumerRun` carry no ○ even though no constant on the route references them. Their content either enters
through a Lib duplicate with the same type (Lift(ii), (iv)) or is not needed at all (Lift(iii), 14^τ(c)).

---

## 1. Theorem JV⁺* (s7:thmJVps)

**Paper** (`paper/src/s7.tex:1350-1362`; v6.1 `s7.tex:1366`): "Assume that D_* satisfies Γ1–Γ4. Let G be a graph
with n ≥ N_0 vertices and d_1 ≥ D_*. Take any valid HB^{τ+} run on G, any designation δ, and no VX-parts. Then
there are simple graphs Q_3,…,Q_R without isolated vertices such that (1) f(G) ≤ C_0 n + 2Σ_{l=3}^R f(Q_l), where
C_0 := D_*/2+1085+ε_1(D_*); (2) Σ_{l=3}^R |V(Q_l)| ≤ θ_Q n, where θ_Q = ε_2(D_*) ≤ 1/4."

**Lean** (`formal/EG/Spec/Quot/JVps.lean:56-66`):
```
∀ V [DecidableEq V] (G : FGraph V) (N0 Dstar : ℝ) (run : Run V) (δ : Designation V),
  N0Cond N0 → GammaCond N0 Dstar → N0 ≤ G.card → Dstar ≤ run.d G 1 →
  run.Valid G Dstar → IsDesignation run G δ →
  ∃ W Q, (∀ l ∈ Icc 3 run.R, ∀ v ∈ (Q l).verts, ∃ e ∈ (Q l).edges, v ∈ e) ∧
    fnum G.edges ≤ C0 Dstar * G.card + 2 * Σ_{l∈Icc 3 R} fnum (Q l).edges ∧
    Σ_{l∈Icc 3 R} (Q l).card ≤ thetaQ Dstar * G.card
```

**Classification: SAME** (the hypothesis packaging is ENCODING-ONLY).
* `f` is `EG.fnum` (`Defs/Fnum.lean:58`). It is a genuine minimum over decompositions of the loopless part, and
  `FGraph.edges` is loopless by construction (`Defs/Graph.lean:39-48`).
* `n = G.card = |verts|`. `d_1 = run.d G 1 = Round.d (run.graph G 1) = 2|E(G)|/|V(G)|` (`Defs/HB/Run.lean:81`,
  `Round.lean:111`, `Lib/HB/Run.lean:346` `graph_one`).
* "Simple" is enforced by the type `FGraph` (Finset of `Sym2`, no loops). The paper's Lemma 7.8 (`QuotSimpleStatement`)
  is ○ (unused). It is not vacuous by encoding, though. Collapsed parallel edges would leave items uncovered,
  and that cannot happen because JC2 is proved. The "no parallel edges" content lives in `Rules.rank_inj`
  (`Lib/Quot/Quotient.lean:101`), which is used by `layerOf_eq` (`:154`).
* "Any valid run, any designation" is `∀ run δ` together with `run.Valid` and `IsDesignation`. `Run.Valid`
  (`Defs/HB/Run.lean:257`) and `Round.Valid` (`Round.lean:320`) are purely deterministic encodings of (R0)–(R5)
  with arbitrary witnesses. They contain no probabilistic or "good" content.
* Γ1–Γ4 is `GammaCond` (`Defs/Main/GammaCond.lean:34`): Γ1 ∧ Γ2(a) ∧ Γ3 ∧ Γ4. Γ2(b),(c) are lemmas, not
  hypotheses, which matches the paper's "implied by Γ1". N_0 appears as an arbitrary `N0` with `N0Cond`
  (`Defs/Gamma/Full.lean:83`) rather than a fixed constant. "θ_Q ≤ 1/4" is Γ4 (`Defs/Main/Gamma.lean:29`)
  and is not restated.
* "No VX-parts" and the two sentences about ultra hubs have no Lean content. They are commentary (COSMETIC).
* The proof (Proof/Todo/JVps.lean:33-55) builds the Q_l as `roundQuotient … (Js l)` on the Js returned by
  `Cost`. The **same** Q are used for (1) and (2).

**Constants are the same explicit functions** (`Defs/Quot/Constants.lean`, `Defs/Chain/Constants.lean`, `Defs/HB/Run.lean:371`):

| Paper | Lean | Match |
|---|---|---|
| C_0 = D_*/2+1085+ε_1 (s7.tex:1272, s1 defConstants(v)) | `C0` Constants.lean:63 | exact |
| ε_1 = ε_K+169ε_A+252/D_*+1.5ε_CONC+3ε_X+9/D_* (s7.tex:1267-1268) | `eps1` :58-60 | exact |
| θ_Q = ε_2 = 12ε_X+4(3ε_A+60/D_*+2F(log₂D_*)) (s7.tex:1110-1112) | `eps2` :50-51, `thetaQ` :54 | exact |
| F(x) = (3184+30400 log₂x) x^{-90.2} | `FQ` :46 | exact |
| det_l = 3\|D_l\|+78nM_l/Hcd_l+30n/M_l+320nM_l³(log₂θ^ult_l+8)/λ_{l-2}^{95} | `detl` :38-42 | exact |
| ε_X = ε_U+10.3/D_*+2.1(6log₂D_*+12)/D_* | `epsX` :30-31 | exact |
| ε_U = 2462 (log₂D_*)^{-205} (s5.tex:138) | `Light.epsU` (Defs/Light/Constants.lean:31) | exact |
| ε_K = ε_ch = 614/D_*+log₂(2A log₂(A log₂log₂D_*))/(371(log₂log₂D_*)²) (s5.tex:223) | `Chain.epsK` :40-43 | exact |
| ε_A = 31ε/(C' log log D_*) | `HB.epsA` Run.lean:371 | exact |
| ε_CONC (s6.tex:339-352) | `Chain.epsCONC` :33-36 | exact (σ=100, ε=2^{-5}, C'=103 as in s1:defConstants(i)) |
| ε_M = ε_K+169ε_A+252/D_* | `Chain.epsM` :47-48 | exact |
| c_EG = max(C_0/(1−2θ_Q), N_0/2) | `cEG` Defs/Main/Gamma.lean:33 | exact |

---

## 2. Theorem HI″ (s7:thmHI) and Corollary 7.22 (s7:thmMainProof)

**Paper** (`s7.tex:1386-1397`): "Let C ≥ D_*/2 and ϑ ∈ [0,1/2) be constants with the following property. Every graph G
without isolated vertices, with n ≥ N_0 vertices and d_1 = 2|E(G)|/n ≥ D_*, admits finitely many simple graphs
Q_1,…,Q_k (k≥0) such that f(G) ≤ Cn+2Σf(Q_i) and Σ|V(Q_i)| ≤ ϑn. Then f(G) ≤ c|V(G)| for every graph G, where
c := max(C/(1−2ϑ), N_0/2)."

**Lean** (`formal/EG/Spec/Quot/HI.lean:54-71`):
```
HIHyp Dstar N₀ C ϑ := ∀ (V : Type) (G : FGraph V), (∀ v ∈ G.verts, ∃ e ∈ G.edges, v ∈ e) →
   N₀ ≤ G.card → Dstar ≤ 2 * G.edges.card / G.card →
   ∃ (k : ℕ) (W : Fin k → Type) (Q : (i : Fin k) → FGraph (W i)),
     fnum G.edges ≤ C * G.card + 2 * Σ_i fnum (Q i).edges ∧ Σ_i (Q i).card ≤ ϑ * G.card
HIStatement := ∀ Dstar N₀ C ϑ : ℝ, Dstar/2 ≤ C → 0 ≤ ϑ → ϑ < 1/2 → HIHyp … →
   ∀ (V : Type) (G : FGraph V), fnum G.edges ≤ max (C/(1-2ϑ)) (N₀/2) * G.card
```

**Classification: SAME for HIHyp. LEAN STRONGER for HIStatement**, which carries no sign condition on D_*, N_0 or C.
* Q_i are **not required to have fewer vertices than G**. The paper does not require it either; both derive it from
  Σ|V(Q_i)| ≤ ϑn < n. Q_i are **simple** because they have type `FGraph`. **d_1 is written literally as 2|E|/n**
  in ℝ, with `x/0 = 0` at n = 0, a case the paper never considers.
* At negative parameters the statement stays true. I checked a case by hand: if c < 0 then N_0 < 0, so HIHyp
  applies to K₂ and is false there, which makes the implication vacuous. It is kernel-checked anyway.
* JVps does not need "without isolated vertices". `hiHyp_of_gammaCond` drops `_hiso` (Main.lean:60) and also discards
  JVps's no-isolated conclusion (Main.lean:65). This is harmless and documented as D1.
* Corollary 7.22. The route to `erdos_184` uses `c = ⌈max(C₀/(1−2θ_Q), N₀/2)⌉₊` (HIMain.lean:55-57) with
  C := C₀ and ϑ := θ_Q, which is exactly the paper's application. `half_le_C0`, `thetaQ_nonneg` and `thetaQ_lt_half`
  come from Γ2(a) and Γ4 (Main.lean:76-78). The explicit-constant form `CorJVpsEGStatement`
  (`Spec/Main/CorJVpsEG.lean:46-48`: f(G) ≤ cEG N0 D·n) is proved but marked ○, so it is not on the route (ENCODING-ONLY).
* `mainInternal_iff_exists_hiHyp` (HIMain.lean:69) shows that HIHyp with k = 0 is equivalent to the main
  theorem. All the weight is therefore on JV⁺*, which is as it should be.

---

## 3. Lemma JV-L (s7:lemLift), parts (ii)–(iv)

**Paper** (`s7.tex:619-635`):
* (ii) "For every decomposition Dec of E(Q_l) into cycles and single edges, the lift of each cycle of Dec is a cycle of
  G, and the lift of each single edge of Dec consists of one or two single edges of G. The lifts of distinct members of
  Dec are pairwise edge-disjoint. Hence … at most 2|Dec| pairwise edge-disjoint objects of G."
* (iii) items are paid or lie in exactly one Q_l-edge; junction-edge uniqueness and orientation; "exactly one lent class,
  namely LJV_{Y(u),l} … the only consumer of this class is the round-l step"; the disjointness of E_r(Y) and E_l(Z).
* (iv) "…is a J-consumer: Obj_l and LentJV_l satisfy (JC1)–(JC3)… The objects of Obj_l other than paid single edges
  number at most 2|Dec_l| = 2f(Q_l)."

**Lean** (`formal/EG/Spec/Quot/Lift.lean`):
* (ii) `LiftDecompStatement` (:150-162). It holds for every valid abstract round input `I` and valid rules `R`, every
  ξ and every `Dec` with `IsDecomp (R.Q ξ).edges Dec`. Each cycle lifts to `[Obj.cycle c']` with `(Obj.cycle c').WF`
  (Nodup and length ≥ 3, `Defs/Objects.lean`) and edges in `I.G.edges`. Each single edge lifts to 1–2 WF single edges
  of G. The flattened edge list of all lifts is `Nodup`, and the total length is ≤ 2|Dec|.
* (iii) `LiftAccountingStatement` (:175-200).
* (iv) `LiftJConsumerStatement` (:202-207) and `LiftJConsumerRunStatement` (:221-233). The run-level form is
  `JC1 … ∧ JC2 J LentJV Obj ∧ |⋃lifts(dec)| ≤ 2·fnum(Q_l)`, where `JC2 = IsDecomp (J ∪ L) Obj`
  (`Defs/Chain/JConsumer.lean:50`). That is: well-formed objects, pairwise edge-disjoint, **union exactly J_l ∪ LentJV_l**.
  It assumes `JPlusProps` and `(RoundInput.ofPast …).Valid`.

**Classification:**
* (ii) **SAME**. Lean is somewhat more general, since it covers every valid abstract past.
  "Cycle of G" means distinct vertices, length ≥ 3, consecutive pairs adjacent in G.
* (iii) **LEAN WEAKER**, and this is acknowledged in the file (:166-174).
  - "Exactly one lent class" is checked only among the `LJV_{Y,l}` of the past.
  - COL(g) "only consumer" is not formalized.
  - E_r(Y) / E_l(Z) membership is replaced by the consequence `Disjoint junctionEdges J`.
  - It has **no consumer on the route** (§0).
* (iv) **SAME**, conditional on validity of the past. On the route that validity is discharged by
  `EG.Quot.ofPast_valid` (`Lib/Quot/OfPastValid.lean:74`), called at Proof/Todo/Cost.lean:43. The Lean obligation
  holds for **every** J with `JPlusProps`, not only the chain's J_l, so Lean is stronger here. The bound
  "≤ 2f(Q_l)" relies on `Rules.Valid.dec`: `R.dec ξ` is an optimal decomposition, length = fnum
  (`Defs/Quot/Round.lean:777`). That holds for the chosen rules, whose existence is proved by
  `Rules.std_valid`, so it is not an assumption.

**Stale text (EXPOSITION).** The protected docstring of `LiftJConsumerRunStatement` (Lift.lean:214-220) still says that
`ofPast_valid` "is an open obligation … that no Spec states yet, and the hypotheses … have not been shown satisfiable".
That is out of date: it is proved and used. The bundle it discharges, `RoundInput.Valid` with 18 fields
(Defs/Quot/Round.lean:150-197), covers J⁺(J1–J3), lemCand(iv) (`good_cand`, `Hcd_ge`), propStructure(iii)
(`ljv_disj`, `ljv_J`), designation typing, and more. It is load-bearing, yet it exists only as a Lib theorem with
**no Spec-level statement and no CORRESPONDENCE row of its own**.

---

## 4. CONC-L(iv) (s6:thmCONCL) and propOV (K2) (s2:propOV): the log* n killers

**Paper, CONC-L(iv)** (`s6.tex:339-352`; v6.1 `s6.tex:335`): "For every valid run and every designation, summing over
*all* ancestors…, Σ_{(Y,l)} m_{Y,l} ≤ ε_CONC(D_*) n, where ε_CONC(D_*) := 2^{σ+15} log*D_*/log D_* + 200ε log*D_*/(C' log
log D_*) + 4(2log*D_*+2)/(log D_*)^{1/2}."

**Lean** `ConcLSumStatement` (`Spec/Chain/CONCL.lean:148-153`):
`∀ V G Dstar run, Gamma1core Dstar → run.Valid G Dstar → ∀ δ, IsDesignation run G δ →
 Σ_{l∈Icc 1 R} Σ_{Y∈run.ancestors G} mY run G δ Y l ≤ epsCONC Dstar * G.card`.

**Classification: SAME.** Lean is marginally stronger: it needs only Γ1(a)–(e) (`Defs/Gamma/Core.lean:89`), with
no n ≥ N_0 and no Γ1(f), Γ3 or Γ4.
* The quantifiers are "for every valid run and every designation", exactly as in the paper.
* The constant is a function of D_* alone, so there is **no n-dependence and no log* n**.
* `mY = max_{h∈V(G)} d_{Y,l}(h)` (`Defs/Chain/Design.lean:66-72`) matches the paper's definition.
* Lean sums over l ∈ [1,R] and all ancestors, the paper over "all (Y,l)". The two agree because m_{Y,l} = 0
  elsewhere: Std_l = ∅ outside [1,R], there are no classed ports for l ≤ 2, and δ is forced into anc_l.
* `logStar` (`Defs/Log.lean`) is the paper's log*.
* On the route via `MixCConc` (MixCConc.lean:23) → Cost.lean:64.

**Paper, (K2)** (`s2.tex:851-853`): "|D_r| ≤ dup_r ≤ 7.6 εn/log P_r, and Σ_{Z∈Std_r}|A_Z| ≤ Σ|Z^0∩D_r| ≤ 2dup_r ≤ 15.2
εn/log P_r", for a fixed valid run and a round r ≤ R.

**Lean** `OVRunStatement` (`Spec/HB/OVRun.lean:128-158`): `Gamma2a Dstar → run.Valid G Dstar → ∀ r ∈ Icc 1 R, … (run.D G r).card ≤ run.dup G r ∧ dup ≤ 7.6 ε n / log₂ P_r ∧ Σ_{a∈Std}|hubs| ≤ Σ_{a∈prePart}|Z0∩D| ≤ 2 dup ∧ 2dup ≤ 15.2 ε n / log₂ P_r ∧ …`.
Here `hubs = Z0 ∩ D` (`Run.lean:324`), `D = {μ ≥ 2}` (`Round.lean:194`) and `dup = Σ_w (μ_w − 1)^+` (`Run.lean:342`).

**Classification: SAME.** The Γ2(a) hypothesis is implicit in the paper's proof, through Lemma Cap(ii). It does not
involve the designation. The **summation over rounds**, which is where log* n is actually killed, is
`TowerEStatement` (`Spec/HB/Tower.lean:101-107`). It matches the paper's lemTower(e) (`s2.tex:1174ff`):
Σ_l 15.2ε/log P_l ≤ ε_A, Σ_l|D_l| ≤ ε_A n, and Σ_lΣ_Z|A_Z| ≤ ε_A n. Its proof uses OVRun(K2) and `LacunaryRun`
(TowerE.lean:44-90). It is on the route as an argument of `mixc_of_specs`.

---

## 5. Theorem MIX-C (s6:thmMIXC), cost line (c), and Lemma K-RED (s5:lemKRED)

**Paper, MIX-C(c)** (`s6.tex:771-775`): "The number of output objects is at most (D_*/2+c_KRED+c_Fresh)n + ε_M(D_*)n +
[80 dem + 369 lp + 169Σ_l|Lost_l|] + 1.5Σ_{(Y,l)} m_{Y,l} + Σ_l|Obj_l| … Moreover 1.5Σm ≤ 1.5ε_CONC(D_*)n." This holds
for any stage-1 outcome, stage-3 outcomes in the good events, and *any* J-consumer, with the run's own J_l.

**Lean** `MixCStatement` (`Spec/Chain/MixC.lean:118-134`): `RunHyp → IsDesignation → ∀ ω ∈ (Stage1.law G run).supp, ∀ (C : JConsumer run G δ (stageOf ω)) (b), (∀ l J, 3≤l≤R → JPlusProps … l J → |(C.out l J).1| ≤ b l J) → ∃ Js, (∀ l ∈ [3,R], JPlusProps … (Js l)) ∧ ∃ D, IsDecomp E(G) D ∧ |D| ≤ (D_*/2+745+338)n + ε_M n + (80dem+369lp+169Σ_{l∈[1,R]}|Lost_l|) + 1.5Σ_{l∈[1,R]}Σ_{Y}m_{Y,l} + Σ_{l=3}^R b l (Js l)`.
`MixCConcStatement` (:138-143) is the last sentence of (c).

**Classification: DIFFERENT, Lean strictly weaker in shape but sufficient for its consumer.**
* The numbers and constants are **SAME**: c_KRED = 745, c_Fresh = 338 = 169·2, ε_M exact.
* *Option B′*: `Js` is existential and constrained only by `JPlusProps` (∅ qualifies). So Lean does **not** say that the
  bound holds for the chain's own J_l. This is acknowledged at MixC.lean:69-82 (D34). The consumer obligation
  ("bounds uniform over all JPlusProps sets") is met. `UHsplitThetaStatement` (`Spec/Quot/UHsplit.lean:104-118`)
  quantifies over **every** JPlusProps family `Js`, every valid rule family and every Markov-event ξ family, and
  `CostStatement` (`Spec/Quot/Cost.lean:58-70`) has the same existential shape. So JV⁺*(1) and (2) are read off the
  **same** Js and the same Q_l. The chain is consistent.
* Consumers are restricted to functions of (l, J) in a fixed context, and outcomes to the positive-weight support.
  Lean is weaker than the paper's "any", which is immaterial.
* The stage-3 good-event hypothesis is **removed**: the Lean statement is unconditional in stage 3. That direction
  is stronger.
* MIX-C (a) "Order" and the five detailed bullets of (b) are not stated. Only `IsDecomp E(G) D` is.
  The TPV bullet of (a) is a separate proved Spec, `MixCTPVApplicableStatement` (:151-163).

**Paper, K-RED** (`s5.tex:332-356`): for a fixed valid run, a fixed stage-1 outcome, stage-3 outcomes in all light-part
good events, and *any* family Lent_ext with Lent_ext(Y) ⊆ ∪LJS ∪ ∪LJV and Lent_ext(Y) = ∅ for demoted Y, the
round-by-round procedure yields a decomposition of E(G)∖K_std∖∪_Y Lent_ext(Y) into ≤ (D_*/2+745+ε_K)n + 80 dem + 369 lp
objects, plus a causality clause ("objects produced at round l depend only on …").

**Lean** `LemKREDStatement` (`Spec/Light/KRED.lean:59-67`): `RunHyp → ∀ ω ∈ supp, ∀ Lext, LentExtHyp ω Lext → ∃ D, IsDecomp ((E(G) \ Kstd) \ ⋃_{Y∈lightParts} Lext Y) D ∧ |D| ≤ (D_*/2+745+ε_K)n + 80·dem ω + 369·lp ω`.
`Kstd`, `LentExtHyp` (`Defs/Probe/S5/KRED.lean`) and `dem`, `lp` (`Defs/Light/Stages.lean:167-173`) match
s5:defStages (s5.tex:98).

**Classification: SAME for the conclusion and the bound** (existence form). The good-event hypothesis is removed,
which is stronger. The causality clause is **dropped**, so Lean is weaker on that clause (D28). In the paper that
clause is load-bearing for the interleaved Construction 6.17. Lean does not need it, because it decouples the
assembly: it builds the standalone chain R..1 first and then applies K-RED once with the final Lent_ext
(Lib/Chain/MixCAssembly.lean, D33).

---

## 6. Lemma 14^τ (s2:lem14tau), parts (b) and (c)

**Paper (b)** (`s2.tex:396-401`): at every split |N″| ≤ 1.6ε|U′|/log²m, U′ goes only to G_1, |G_1| ≤ ¾m; hence S ≤
n_0/(1−5.5ε) ≤ 1.21 n_0, and for M ≥ 2, Δ_{≥M} ≤ 5.46 εS/log M.

**Lean** `L14OVStatement` (`Spec/HB/Lemma14Tau.lean:146-160`): the same four per-split facts plus
`2 ≤ |node|`, plus `t.OVHyp epsC 1.6 H`, leafMass ≤ n_0/(1−5.5ε), n_0/(1−5.5ε) ≤ 1.21 n_0, and ∀ M ≥ 2,
DeltaGe ≤ 5.46 ε·leafMass/log₂M. The hypotheses are 1 ≤ s, 128 s log² n_0 ≤ τ, and `IsTauRun`.

**Classification: SAME.** Lean is slightly stronger because it adds explicit conjuncts. It is on the route through
OVRound → OVRun(K2).

**Paper (c)** (`s2.tex:402-404`, final): "for every leaf and every vertex h, if τ>0 then #{deleted hu : u∈V(Leaf)∖Dup}
≤ ⌈τ⌉−1 (= τ−1 for integer τ); the number is 0 if h ∈ V(Leaf)". In v6.1 (`s2.tex:403-404`) the clause "if τ > 0"
is absent.

**Lean** `L14ThinStatement` (:166-183): both bounds carry `0 < τ`; the h ∈ V(Leaf) clause and (d) are unconditional.

**Classification: SAME as the final paper. LEAN WEAKER than the v6.1 literal text, which is false at τ = 0**
(`EGTest.ProbeP3A.lem14tau_c_literal_false`; erratum L14-C-TAU0). (c) is **off-route in both texts**.
* In the paper, no later statement cites 14^τ(c). ORIGIN(b) uses Lemma thin cut (`s2.tex`, proof of propOrigin(b),
  deps line).
* In Lean, `EG.l14Thin` has no reference. ORIGIN(b) uses `STree.thinCut_lt` (`Lib/HB/SEP.lean:230`), which needs only
  `0 < τ` and the τ-labels (not τ ≥ 128 s log²n_0).
* The erratum therefore cannot touch the main chain. CORRESPONDENCE does not ○ it, because its "closure" is module-level.

---

## 7. Probabilistic statements made deterministic: what replaced the probability?

* **Stage 3** (TPV, PV/lemChild, VX⁺/lemDemoted, K-RED, and MIX-C's "stage-3 outcomes in the good events"): replaced by
  **deterministic existence**, "∀ admissible E (or H₀), ∃ partition/decomposition with the bound". Examples:
  `TPVStatement` (`Spec/Vortex/TPV.lean:73-76`), Child.lean:62, Demoted.lean:45, KRED.lean:59.
  - The good event is **not assumed**. Its non-emptiness is **proved** inside Lib with explicit probability bounds:
    `TPVProb.exists_good` (`Lib/Vortex/TPVProb.lean:105`, P ≥ 1/2 − η > 0), `PVProb.exists_good`
    (`Lib/Vortex/PVProb.lean:32`), and `VXProb.exists_good`. The TPV proof consumes it at Proof/Todo/TPV.lean:25.
  - The paper's claim is stronger in quantifier order: "one stage-3 outcome works for every admissible E/H₀"
    (OneOutcome(2), s7.tex:1189-1194 and its proof). Lean only proves ∀E ∃ (D27). This is sufficient, because
    every device is applied once, to the final E.
* **Stage 1** (COL, E1, Expect, Lost, EXprime) **remains genuinely probabilistic**. It is a product law
  `Stage1.law = (FinDist.pi coordLaw).map ofCoords` (`Defs/Stage1/Law.lean:132`), with independent coordinates
  per H_Y edge, vertex, JS site and pool label. Expectations and probabilities are real sums, for example
  `LostStatement` (Spec/Chain/Lost.lean:61) and `EXprimeStatement` (Spec/Quot/EXprime.lean:46).
* **Round randomness ξ_l remains probabilistic**.
  - `MarkovEvent` (`Defs/Quot/Round.lean:669`) is the paper's event (f).
  - `xiChosen` (:678) picks a positive-weight point of the event if one exists, else an arbitrary one.
  - Non-emptiness is **proved** by Markov, P ≥ 1/2 (`Lib/Quot/RoundExist.lean:35-50`), so the fallback is never taken.
  - The stage-1 Markov choice X′ ≤ 3E X′ is `OneOutcomeStage1` (Spec/Quot/OneOutcome.lean:65), discharged on the route
    at JVps.lean:37.
* The good-event **hypotheses** on the route are `X′(ω) ≤ 3E X′` in Cost and UHsplitTheta, and `MarkovEvent (ξs l)` in
  UHsplitTheta. Both are discharged on the route (JVps.lean:37, 48-50; Cost.lean:92-97). **None is left as an
  undischarged assumption.**

## 8. Hypotheses added in Lean, and "assumed-property" fields on the route

* **Added hypotheses vs. the stated paper text, all discharged on the route:**
  - Γ1core in `ExistsRunStatement` (`Spec/HB/Exists.lean:166-168`). The paper's Prop 2.15 says "For every graph G a
    valid run exists" with no Γ. CORRESPONDENCE notes that it is false without a condition on D_* (EXPOSITION; covered
    by the paper's standing assumption).
  - Γ2(a) in OVRun.
  - Γ1core in ConcLSum.
  - `0 < τ` in 14^τ(c).
  - `(ofPast …).Valid` in the Lift run-level form.
  - `ω ∈ supp` in the stage-1 Specs.
* **Structures and fields that could hide assumptions:**
  - `JConsumer.jc1/jc2`: supplied from `liftJConsumerRun_univ` (Cost.lean:44-52).
  - `RoundInput.Valid`: proved by `ofPast_valid`.
  - `Rules.Valid`: only says the fixed rules are well-formed choices (permutations, an SDR when one exists, an
    optimal `dec`). It is proved for `Rules.std` (`RoundExist.lean:59-64`).
  - `StageData.Coherent`: `coherent_ofOutcome` (Cost.lean:40).
  - `mixc_of_specs` takes **proved theorems** as arguments (MixC.lean:36-37).
  - No `axiom`, `opaque` or `sorry` token appears in code (my scan).

## 9. Paper-only claims on the load-bearing route, and Lean-only claims

**Claimed by the paper but not established by Lean as stated.** In every case the downstream conclusion *is* established, by another route.
1. Construction 6.17 (interleaved processing R..1) and Lemma 6.18 (Lent sets). CORRESPONDENCE marks them P,
   proof-internal. Lean uses ORDER-DECOUPLE (D33). The paper's own ordering and finality argument is uncertified.
2. MIX-C (a) "Order" and the detailed (b) bullets; the cost bound with the chain's own J_l (Lean: existential Js).
3. K-RED's causality clause (dropped, D28).
4. Lift (iii): global exclusivity of the lent class and COL(g) "only consumer" (not formalized; Lift(iii) is unused).
5. OneOutcome (2): uniformity of a single stage-3 outcome over all admissible edge sets (D27).
6. The JS-LC routing engine as written. Per D29 and the CORRESPONDENCE ○ on `MedStatement` and `EqLpt*`, Lean
   proves JS-LC's stated bound (126n/M_l + 1.5Σ_giant m) by a simpler first-fit cherry grouping with no S₀,
   MED, EQ-LPT or padding. The paper lists this engine as "weakest link (a)". It is **not** what was machine-checked.
   I did not re-read the JS-LC Lean proof myself; this item rests on D29 and the ○ marks.
7. 14^τ(c) in its v6.1 wording (false at τ = 0; fixed in the final paper; unused in both).

**Established by Lean but not stated by the paper (Lean stronger):**
* HI″ for all real D_*, N_0, C, ϑ.
* The J-consumer obligations and UHsplit (iii)/(iv) for **every** JPlusProps J and every valid rule family, not only
  the run's.
* Lift (ii)/(iv) for every valid abstract round input.
* CONC-L(iv) needs only Γ1(a)–(e).
* The thin cut needs only τ > 0 and τ-labels.
* Internal sharper constants (D26, D28, D29): K-RED 739; JS-LC ≈ 11.96 n/M_l; PV 296. TPV is the exception:
  Lean gets 144|P| where the paper gets 132, still within the stated 169.

---

## 10. Ranked discrepancies

| # | Severity | Item | What |
|---|---|---|---|
| 1 | UNCLEAR | s6:consOrder, s6:lemLent, MIX-C(a)/(b), K-RED causality, Lift(iii) exclusivity/COL(g), OneOutcome(2) uniformity | The paper's interleaved assembly argument is not machine-checked. Lean proves the same conclusions (IsDecomp E(G) plus the cost line) by a different decoupled route. Nothing contradicts the paper's argument, but "paper proof verified" is overstated for §6's assembly. |
| 2 | UNCLEAR | JS-LC routing engine (MED, EQ-LPT, S₀; the paper's weakest link (a)) | Bypassed in Lean (D29; MED and EQ-LPT are ○). The stated JS-LC bound is certified; the paper's proof of it is not. Not independently re-read here. |
| 3 | EXPOSITION | MIX-C / propCost (Option B′) | Lean `MixCStatement` and `CostStatement` are strictly weaker than the TeX: the J_l are existential and may differ from the chain's. This is consistent because UHsplit is uniform over JPlusProps sets. A reader of the Spec cannot recover "the decomposition given by MIX-C on the run's J_l". |
| 4 | EXPOSITION | Correspondence "in closure" | The closure is module-level. `L14ThinStatement`, `LiftAccountingStatement`, and the Spec theorems `EG.liftDecomp` / `EG.liftJConsumerRun` carry no ○ but are referenced by no constant. The route uses `liftDecomp_core` and `liftJConsumerRun_univ`; I checked that these have the same statements. |
| 5 | EXPOSITION | `Spec/Quot/Lift.lean:214-220` | A stale protected docstring says `ofPast_valid` is open and its hypotheses not shown satisfiable. In fact it is proved (`Lib/Quot/OfPastValid.lean:74`) and on the route. The load-bearing bundle it proves (J⁺, lemCand(iv), propStructure(iii)) has no Spec statement and no correspondence row. |
| 6 | EXPOSITION | s2:propExists | The paper's statement omits the Γ condition that Lean shows necessary (covered only by the standing assumption). |
| 7 | EXPOSITION | Stage-3 lemmas (TPV, PV, VX⁺, Child, Demoted, K-RED) | Deterministic ∀E∃ form, weaker in quantifier order than the TeX's uniform good event. Good-event non-emptiness is proved in Lib, not assumed. |
| 8 | COSMETIC | s2:lem14tau(c) | v6.1 is literally false at τ = 0. The final paper and Lean add τ > 0. It is unused by anything in either text. |
| 9 | COSMETIC | s7:thmJVps | "No VX-parts" and the ultra-hub sentences have no Lean content. Lemma 7.8 (Q_l simple) is ○; simplicity is by type, backed by `rank_inj`. |
| 10 | COSMETIC | MIX-C / K-RED | Restricted to ω ∈ supp and to consumers that are functions of (l, J). Immaterial. |
| 11 | COSMETIC | Stale "P3 stub … replace `by sorry`" headers | For example Proof/Todo/JVps.lean:10. Historical, and acknowledged in the README. The code contains no `sorry`. |

**FATAL: none. GAP: none** for the formal theorem. Every statement I compared that lies on the constant-level
route (JV⁺*, HI″, Cost, UHsplitTheta, OneOutcome, MIX-C, MIX-C-Conc → CONC-L(iv), K-RED, OVRun(K2) via TowerE,
14^τ(b) via OVRound, Lift(ii)/(iv) via the Lib duplicates) is proved, and its hypotheses are discharged on the route.
