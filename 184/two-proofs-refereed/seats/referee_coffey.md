# Hostile referee report: Proof B (Ryan Coffey, "A proof of the Erdős–Gallai cycle decomposition conjecture", 152 pp)

**Seat.** Coffey, load-bearing chain. 2026-10-20.

**What I read as text** (no lean, lake or leanchecker was run):
- the final paper: `coffey/repo/paper/src/{s1,s2,s5,s6,s7,formalization}.tex`, with s3 and s4 read only for the statements of TPV, PV and Theorem 16\*;
- manuscript v6.1, which the Lean quotes: `proofs/manuscript/*.tex`, diffed against the final paper section by section;
- `ERRATA_v6.1.md`, `v61/PATCHES.md`, `v61/FIXES.md`, `formal/work/p4/DEVIATIONS.md`, `README.md`, `CORRESPONDENCE.md`;
- `formal/comparator/Challenge.lean` (sha256 9f36e4e0…, matching the brief) and `formal/STATEMENT.md`;
- Bucić–Montgomery arXiv 2211.07689 **v2** (14 Nov 2023, still the current version), fetched to `/tmp/oaimath/181/refs/bm_2211.07689.pdf` and `bm.txt`.

**Companion files.** Two helper passes of this seat wrote companion files:
- `referee_coffey_BMtable.md`: the full citation table, with BM pages rendered where pdftotext garbles formulas;
- `referee_coffey_LEANmap.md`: the paper-to-Lean statement map.

I re-checked their load-bearing claims as follows.
- **Citations:** I compared BM Lemma 14, Lemma 25 and Corollary 22 against bm.txt myself.
- **Lean:** I read `formal/EG/Proof/Todo/JVps.lean`, the `UHsplitThetaStatement` spec, and DEVIATIONS D26–D34 myself.
- Everything else from those passes is marked [helper].

---

## Verdict

**For the scope of this seat: HOLDS AS READ on the load-bearing chain.** The pieces covered are:
- the induction and its constants (Section 7, final part);
- the cost line (`s7:propCost`) and the quotient-size bound (`s7:lemUHsplit`, θ_Q = ε₂(D\*));
- the lift (`s7:lemLift`);
- the per-round cost accounting that replaces BM's log\* n;
- the τ-modification of BM's Lemma 14.

I found **no FATAL** objection and **no GAP**. I looked specifically for a per-round cost of order Θ(n) and found none (§2 below).

**HOLDS WITH FIXES (exposition)** for the citation layer and the status/formalization prose (objections 3–8).

**COULD NOT CHECK** line by line:
- the device lemmas of s3–s5: Lemma 15⁺, Theorem 16\*, Lemma 17\*, TPV, the four-phase P-vortex, VX⁺, zones, and the parent-side chaining;
- the HCC-P/PAR internals of s6.

For these I only checked how their statements are used. The Lean is the evidence for their truth. Note that for two of them the Lean does not follow the paper's proof (objections 1 and 2).

---

## 1. The induction and the constants: recomputed

- **`s7:thmHI` (Theorem HI″).** Take a minimal counterexample G.
  - If G has an isolated vertex, delete it.
  - If n < N₀, then f ≤ n(n−1)/2 < (N₀/2)n.
  - If d₁ = 2|E|/n < D\*, then f ≤ |E| < (D\*/2)n ≤ Cn.
  - Otherwise, JV⁺\* gives f(G) ≤ C₀n + 2Σf(Q_l) with Σ|V(Q_l)| ≤ θ_Q n < n. Minimality applies to each Q_l, giving f(G) ≤ C₀n + 2cθ_Q n ≤ cn exactly when c ≥ C₀/(1−2θ_Q).

  With θ_Q ≤ 1/4 (Γ4), c_EG = max{C₀/(1−2θ_Q), N₀/2} ≤ max{2C₀, N₀/2}, and C₀ ≤ D\*/2 + 1091. The quotients are strictly smaller graphs, since their **total** order is ≤ n/4. They are simple: they are vertex-disjoint unions of rank-split sub-layers (`s7:lemSimple`). The minimality argument is not circular. C₀ and θ_Q are fixed functions of D\*, chosen before any graph is considered (`s7:remNonCirc`). The induction is applied only to graphs with fewer vertices. **Correct.**
- **`s7:propCost`.** I re-added Table `s7:tabCost`:
  - K-RED: (D\*/2 + 745 + ε_K)n;
  - TPV: 169·(2 + ε_A)n;
  - JS-LC: 252n/D\* + 1.5ε_CONC n;
  - unpaired fresh legs: 2n;
  - SDR failures and loops: 9n/D\*;
  - lift: 2Σf(Q_l);
  - the bracketed stage-1 terms 80 dem + 369 lp + Σ(169 + M_l − 1)|Lost_l| + X_pool ≤ X_U + X_pool ≤ X′ ≤ 3E X′ ≤ 3ε_X n.

  The constant is 745 + 338 + 2 = 1085, and ε₁ = ε_K + 169ε_A + 252/D\* + 1.5ε_CONC + 3ε_X + 9/D\*. **Correct.** The Lean `C0`/`eps1` agree formula by formula [helper; I spot-read `JVps.lean`].
- **`s7:lemUHsplit`.** At each round the quotient has four kinds of vertices: PAR copies (`s7:lemCC`), copies of non-ultra hubs, junction copies in HUB layers (`s7:lemMULT`), and copies of ultra hubs (`s7:lemUltra`). Its order is copies_l ≤ 4E[copies_l | Past_l] ≤ 4(X_{V,l} + det_l), using Markov's inequality at step (f).
  - E X_{V,l} ≤ (6 log₂M_l + 12)n/M_l. This uses E|Pool_l| ≤ n/M_l² and Σ_w mult_r(w) ≤ 1.37n (F11).
  - det_l consists of 3|D_l| and terms decaying like nM_l³ log λ/λ_{l−2}^{95}.
  - Σ_l 3|D_l| ≤ 1.5ε_A n by (K2) and Lemma Tower(e).
  - The decaying terms sum to at most 2F(log₂D\*)n < 2^{−1000}n (F(2^25) ≤ 2^20·2^{−2255}). The tower-lacunary step λ_{l−2} ≥ 2λ_{l−1} is valid because λ ≥ 2^25.

  I re-derived every numerical constant (44.7, 29.8, 32.9 ≤ 78; 312.36 + 7.5 < 320; 3184 = 624 + 320·8; 30400 = 320·95). **Correct.**
- **The lift (`s7:lemLift`).** I checked both cycle types.
  - PAR sub-layer cycle [w₀]…[w_{m−1}]: the lift is w₀ p₀ (x₀) q₀ w₁ … Its vertices are pairwise distinct, for these reasons:
    - one colour per port and per middle (the greedy colouring, `s7:lemWellDef`(i));
    - p_i ≠ q_i;
    - ports lie in Qs_Z and middles in F_Z, which are disjoint by (J3);
    - junctions are pooled, and live vertices are never pooled by rule (a2).
  - HUB sub-layer cycle: the lift is h₀ u₀ w₀ u′₀ h₁ … Its vertices are distinct because the SDR gives distinct colours at a port, and hubs and ports are live while junctions are pooled.
  - Edge-disjointness: each item lies in exactly one edge of Q_l, and the junction edge uw determines the end at u, because junctions at u are injective in (e1) and (e2). The edge uw cannot also be an end at w, since w is pooled and every item at w was paid.
  - Junction edges lie in E_r(Y) with r ≤ l−2, items lie in E_l(Z), and these are disjoint. The colour class LJV_{Y,l} is indexed by l, so distinct rounds use disjoint classes. Unused junction edges stay with their owner as junk, and the owner's device holds on its good event for **every** admissible edge set (`s6:lemLent`(iii), `s6:thmMIXC`(a)).
  - The order R, R−1, …, 1 makes Lent(Y) final before Y is processed.

  Together these give JC2: Obj_l partitions J_l ⊔ LentJV_l, and every edge of G is covered exactly once (`s6:thmMIXC`(b)). **Correct.**
- **(J1), the "most delicate point" behind Lemma MULT.** I verified it at its source, `s6:lemJSLC` Step 2(b). The parity moves are made once per pair (centre h, class Y), on R⁰_Y aggregated over **all** Z ∈ Std_l. So there is at most one J_hub edge of class Y at h per round. That is what makes m_κ(h,w) ≤ mult_r(w) in `s7:lemMULT`.

## 2. The hunt for a per-round Θ(n) cost (the place where BM's log\* n lives)

BM's Lemma 26 pays ≤ 6Σ|G_i| ≤ 12n cycles in every one of ≤ log\* n rounds (Theorem 24 applied to every small expander). I checked that this is the BM mechanism (bm.txt l. 1517–1580). Here every cost term charged at round l is one of the following.

| Term (source) | Per-round size | Sum over rounds |
|---|---|---|
| Long cycles 𝒞yc_l (R1) | ≤ n/(2 log² d_l) | ≤ n (`s2:propStructure`(iii)) |
| TPV hubs Σ_Z\|A_Z\| (K2) | ≤ 15.2εn/log P_l | ≤ ε_A n (Tower(e)) |
| TPV fresh ports | x is fresh only at rounds j₀(x), j₀(x)+1 (`s2:propParentless`(i); I checked the proof) | ≤ 2n, **once per vertex** |
| TPV lost ports | E\|Lost_l\| ≤ 2n/M_l² | ≤ 5.5n/D\* (in X_U) |
| Child vortex, parentless pairs | at rounds j₁(v), j₁(v)+1, plus Bad parts | ≤ 2n + lp, **once per vertex** |
| U-chaining (`s5:lemParent`(ii)) | ≤ 56(J̄+1)M_l(M_l+1)ν_l + cap_l, with ν_l ≤ 2.74n/P_{l−2} and P_{l−2} ≥ M_l^{13} | ≤ ε_Chain(D\*)n |
| JS-LC cycles | ≤ 126n/M_l + 1.5Σ_giant m_{Y,l} | ≤ 252n/D\* + 1.5ε_CONC n |
| Hub concentration Σm_{Y,l} (CONC-L(iv)) | the τ-term per ancestor, carrying a factor R−r ≤ log λ_r | ≤ ε_CONC(D\*)n, uniform in R |
| Demoted parts, lp | E ≤ |Y|^{−1}·O(log λ_r) per light part | ≤ ε_U n |
| Paid J-items (a1)–(a3), SDR, loops | O(n/M_l) in expectation or on the Markov event | O(n/D\*) |
| Unpaired fresh legs | ≤ \|F_Z\| | ≤ 2n, **once per vertex** |
| Quotient order \|V(Q_l)\| | ≤ 4(X_{V,l} + det_l) = O(n log M_l/M_l) + 12\|D_l\| + o | ≤ θ_Q n ≤ n/4 |

The novelty that removes the per-round Θ(n) is visible in the last row. Up to |J_l| ≤ n(M_l − 1) parity-leftover edges per round are compressed into a quotient with only O(n log M_l/M_l) vertices: pooled junctions have density M_l^{−2}, and the rank split creates few copies. That quotient is then paid for by the induction (cost 2c·|V(Q_l)|), not round by round. Each per-ancestor factor R−r is beaten by decay in λ_r. So Remark `s1:remStatus`(ii)(4) is true as far as I can verify: **no Θ(n)-per-round term exists apart from the once-per-vertex charges.**

The weight now rests on the device lemmas that produce the decaying bounds: TPV's 169|Ret_Z|, the P-vortex's 369|Pl|, JS-LC's 126n/M_l, Lemma Parent's chaining count, and CONC-L(i) from the τ-rules. Of these I checked only the τ-rule mechanism (§3). The others are statements whose truth I take from the Lean.

## 3. Lemma 14^τ against BM's Lemma 14

- `s1:citLem14` quotes BM Lemma 14 (v2 p. 12) **exactly**. The deleted edges number ≤ 4sn log n, the expanders satisfy Σ|G_i| ≤ 2n, and the proof uses the induction under 2n − 2n/(2+log n) with (6)–(9). Coffey re-derives (9) separately for n ≥ 3 and n = 2. BM's chain gives (9) only for log n > 1.094. That is erratum L14-INEQ9, fixed in v6.1; the re-derivation is correct.
- `s2:lem14tau` is a **new lemma with a full proof** in the paper and a Lean statement (L14Split/Term/Global/OV/Thin). It is not used as a black box.
  - The τ-rules (`s2:defTauRules`) move the vertices of U with ≥ τ deleted edges into the separator (H_out). They then move the outside vertices with ≥ τ edges into U′ (H_in).
  - The cost is |H_out| + |H_in| ≤ |F₀|/τ, because |F₁| ≤ |F₀| − τ|H_out|. This is ≤ |U|/(128 log² m) and is absorbed as a 1.6ε overlap constant.
  - Lemma SEP(iii) puts all deleted edges h–(Leaf∖Dup) at one node. This gives (c): ≤ ⌈τ⌉ − 1.
  - Overlap: Δ_{≥M} ≤ 1.6ε(1 + 1/c_OV)S/log M, by the geometric descent of log m.

  I find the modification sound. As stated in v6.1, (c) fails at τ = 0 (erratum L14-C-TAU0); the final paper adds τ > 0. Both the paper and the Lean route ORIGIN(b) through the thin-cut lemma, so 14^τ(c) itself has no consumer [helper].

## 4. Numbered objections

1. **UNCLEAR. The JS-LC routing engine, the author's own "weakest link (a)", is not what was machine-checked.**
   - TeX `s6:lemJSLC` Steps 4–5 (s6.tex ~l. 498–543) build the non-giant system 𝒮₀(Y,l), "oriented by MED, layered by EQ-LPT and padded", using HCC-P at junction multiplicity 2M_l − 2.
   - v6.1 listed this as "(a) The routing engine inside JS-LC … it remains listed first despite the two AI audits" (v6.1 s7.tex, *What is not established* (2)(a)).
   - The final paper still names it first among its new ingredients (`s1:remStatus`(i)(a)).
   - DEVIATIONS **D29**: the Lean proves the **stated** bound 126n/M_l + 1.5Σ_giant m by splitting **every** component into cherries and grouping them first-fit (`formal/EG/Proof/Chain/JSLCGroups.lean`, `JSLCBound.lean:49,94,123`). It uses m_{Y,l} ≤ 2γ_l on non-giant pairs. "S₀, MED, EQ-LPT and the padding are never built", and `MedStatement` and `EqLpt*` are off the route (○).
   - So the statement is kernel-certified (pending our replays), but **the paper's proof of it has been checked only by AI referees**. That is a fact about the paper, not about the theorem.
   - **Fix:** replace Steps 4–5 with the Lean's argument. It is shorter and gives the sharper 11.96n/M_l + Σm. This removes the riskiest part of the text.
2. **UNCLEAR (paper level only). The interleaved assembly is not machine-checked.**
   - TeX: `s6:consOrder` ("For l = R, R−1, …, 1, in this order, do: (1) … (4)"), `s6:lemLent`, `s6:thmMIXC`(a)/(b), the causality clause of `s5:lemKRED`, `s7:lemLift`(iii) (class exclusivity / COL(g)), and `s7:lemOneOutcome`(2) (one stage-3 outcome for all admissible edge sets).
   - The Lean instead:
     - builds the standalone chain R..1 first and applies K-RED once (D33, ORDER-DECOUPLE);
     - states MIX-C with an **existential** family J_l constrained only by `JPlusProps` (D34, Option B′);
     - drops the K-RED causality clause (D28);
     - makes stage 3 "∀E ∃ decomposition" rather than a single uniform good event (D27);
     - leaves `LiftAccountingStatement` without a consumer [helper].
   - I read the paper's own argument for these steps (Lent finality, the four-family coverage in MIX-C(b), the junk tolerance) and found it consistent. So this is not a GAP. I checked that the Lean composition is coherent: `JVps.lean` takes the Js returned by `Cost`, and `UHsplitThetaStatement` quantifies over **every** JPlusProps family, rule family and Markov-event ξ family. So bounds (1) and (2) of JV⁺\* are read off the same Q_l.
3. **EXPOSITION. The formalization paragraph overstates correspondence.**
   - TeX (`formalization.tex` l. 50–52): "The formalization follows this paper section by section; a table matching every numbered statement … is given in CORRESPONDENCE.md".
   - In fact the repo's own DEVIATIONS.md records **36 route differences** (D1–D36). Among them are the two of objections 1–2, and the TPV accounting: Lean gets 144|P|, while the paper claims 132|P| and states 169|P| (D26).
   - **Fix:** cite DEVIATIONS.md and say which paper proofs are not the checked ones.
4. **EXPOSITION. The status disclaimers were deleted.** The final paper removes several v6.1 passages:
   - the subsection *What is not established* (v6.1 s7.tex l. 1562–1665);
   - its "Refutation targets";
   - "The Erdős–Gallai conjecture must not be recorded as proved on the basis of this text";
   - the AI-review history, which includes one **major gap** (PV-ARC-END) found by clean-room AI review and repaired as CR1-PV.

   In their place it says "We prove this conjecture" (abstract) and "This completes the proof" (s7 l. 1519). The README still says "No human review … of the mathematics". With a Lean proof the theorem's status is a kernel question, but the **paper's** status has not changed. **Fix:** keep a short status paragraph: AI-generated, no human review, Lean route deviates per DEVIATIONS.md.
5. **EXPOSITION. BM Lemma 25 "explicit form" is filed as a published result** (`s1:citLem25`, `\deps{none (published)}`; s1 l. ~406 "All items of this subsection are published results").
   - BM v2 p. 22 states only "a cycle of length Ω(n/log⁴ n)" for n ≥ 2^{30}/ε².
   - The constant ε²m/(18 log⁴m) and the hypothesis m ≥ 2 are derived from BM's DFS proof. I checked this myself: |Y| ≥ ε²n/(18 log⁴n), and the cycle contains Y.
   - The derivation is correct and load-bearing: `s2:lemCap`(ii), the M_l size cap.
   - The paper gives only a sketch. The full proof is the Lean `EG.bmLemma25` (D9).
   - **Fix:** relabel it "derived from the proof of [BM, Lemma 25]" and write out the roughly 8-line proof.
6. **EXPOSITION. Minor citation slips** [helper, see the BM table].
   - The overview (s1 l. 171) says BM's iteration "costs Θ(n) objects, charged to all vertices that are active in it". BM prove an O(n) upper bound; the charging is Coffey's own reading.
   - Prop 12 is described as "modified in `s3:propP13s`", but it is applied there verbatim as a black box.
   - Prop 18 is quoted with BM's s ≥ log²⁴n while Coffey's own remark says BM's proof needs s ≥ θ+1. This is harmless.
   - Def 7's "multiset clause, quoted in substance" adds an interpretation ("t counts occurrences").
7. **EXPOSITION. `s2:propExists` reads "For every graph G a valid HB^{τ+} run exists, and every sequence of admissible choices terminates".** Termination needs Γ1 on D\*. The Lean `ExistsRunStatement` carries `Gamma1core` (D17), and CORRESPONDENCE says "the statement is false without a condition on D\*". The paper covers this only by the s2 "standing assumption" paragraph. **Fix:** put "if D\* satisfies Γ1" in the statement.
8. **COSMETIC. Commentary inside a theorem statement.** `s7:thmJVps` ends with commentary ("Items at ultra hubs cost no collision payments …") that is not part of the statement and has no Lean content. `s7:lemSimple` is not on the Lean route; simplicity holds by the type `FGraph`, backed by `Rules.rank_inj` [helper].
9. **COSMETIC. Stale Lean docstrings.**
   - `Spec/Quot/Lift.lean:214-220` still calls `ofPast_valid` "an open obligation". It is proved (`Lib/Quot/OfPastValid.lean:74`) and on the route.
   - `Spec/Ext/BMLemma25.lean` still says "at present with sorry".
   - "P3 stub … replace by sorry" headers remain.
   - A comment-stripped scan found 0 `sorry`/`axiom`/`opaque` tokens in `formal/EG` and `formal/EGCheck` [helper].

## 5. BM quotation checks (arXiv 2211.07689v2; numbering is pinned to v2 in s1 l. 403–404; the bibliography cites Adv. Math. 437 (2024) 109434)

The rows marked ✓ I compared against bm.txt myself. All other rows are [helper], done with page renders.

| Coffey (label) | Coffey's statement | BM v2 actual statement | Match? |
|---|---|---|---|
| `s1:citLem14` ✓ | delete ≤ 4sn log n edges; rest partitioned into (ε,s)-expanders with Σ\|G_i\| ≤ 2n, ε ≤ 2^{−5}; proof by induction on 2n − 2n/(2+log n), (6)–(9) | Lemma 14 p. 12: identical, same proof | EXACT; the (9) sub-case n = 2 is correctly patched |
| `s1:citLem25` ✓ | ε ≥ 2^{−5}, m ≥ max(2, 2^{30}/ε²) ⇒ cycle of length ≥ ε²m/(18 log⁴m) | Lemma 25 p. 22: Ω(n/log⁴n) for n ≥ 2^{30}/ε²; the proof gives ε²n/(18 log⁴n) ≤ \|Y\| and a cycle containing Y | DERIVED-EXPLICIT-FORM (sound; objection 5) |
| `s1:citCor22` ✓ | every graph decomposes into paths, each vertex an end of ≤ 2; consequence: edges inside W ⇒ ≤ \|W\| paths | Corollary 22 p. 21: identical | EXACT; the consequence is correctly derived |
| `s1:citProp8` | 1 ≤ ℓ,t ≤ n, \|V\| ≥ 4t−2, ball condition ⇒ some x_jy_j-path of length ≤ 4ℓ log n | Prop 8 p. 8: identical | EXACT (black box; Lean-proved) |
| `s1:citProp12` | expander, 1 ≤ \|U\| ≤ 2n/3, \|F\| ≤ s\|U\|/2, 0 < d ≤ s ⇒ (a) or (b) | Prop 12 p. 11: no lower bound on \|U\| | FAITHFUL (Coffey's version is slightly weaker; black box) |
| `s1:citThm16` | 1 ≥ ε ≥ 2^{−7}, s ≥ log^{135}n, V a 1/3-random set ⇒ whp (4 log⁵n, 2^8 log⁵n)-path connected | Thm 16 p. 14; proof §4.3 | EXACT (structure only; `s3:thmT16s` is proved in full) |
| `s1:citLem17` | ball > \|V\|/2 with probability 1 − e^{−Ω(\|U\|log²n)} | Lemma 17 p. 16 (exponent checked by render) | EXACT (structure only) |
| `s1:citProp18` | s ≥ log²⁴n ⇒ U′ with \|N(U′)\| ≥ \|U′\|log²⁴n, \|U′\| ≥ ε\|U\|/(3 log²⁶n) | Prop 18 p. 18: identical; proof needs s ≥ θ+1 | EXACT, plus a correct erratum on BM's proof (E2) |
| `s1:citLem19` | for every **non-empty** U … | Lemma 19 p. 18: "every U" (false at U = ∅) | FAITHFUL (corrects BM) |
| `s1:citLem9` | (4ℓ log n, k)-path connected under the ball condition | Lemma 9 p. 8: identical; Coffey's "⌈n/8⌉+1" silently fixes BM's n/8+1, which fails at n = 34 | EXACT |
| `s1:citDef7` / `s1:citDef11` | path connectivity / (ε,s)-expander | Def 7 p. 7 / Def 11 p. 10 | EXACT; the multiset gloss in Def 7 is Coffey's (E4) |
| `s1:citProp13`, `s1:citThm4`, `s1:citThm21`, `s1:citLem15` | — | Prop 13 p. 11, Thm 4 p. 7, Thm 21 p. 21, Lemma 15 p. 13 | EXACT (Lemma 15 is unused; its k ≥ 1 is an erratum) |
| Overview, s1 l. 166–172 | BM iterate Lemma 26 ≤ log\* n times (Lemma 14 at s = 0, Lemma 25, Theorem 24) | BM §5.6 pp. 23–24 | accurate, except "Θ(n)" should be O(n) (objection 6) |

Every number refers to the right result. No quoted conclusion is stronger than what BM prove, and no hypothesis is weaker. The one item stronger than BM's **statement**, Lemma 25, is implied by BM's proof.

## 6. Errata found by the formalization (`ERRATA_v6.1.md`, `v61/PATCHES.md`, `v61/FIXES.md`)

**Counts.** There are **31 confirmed errata** against v6.1: 21 open in v6.1 and 10 already fixed there.
- Repo class **T1** ("statement true as used; proof, wording or constant has a gap"): **18** (12 open, 6 fixed).
- Repo class **T0** (formalization detail or editorial): **13** (9 open, 4 fixed).
- **T2/T3** (false statement): **0**.

In this brief's vocabulary all of these are EXPOSITION or COSMETIC, with three exceptions:
- **Literally false in a degenerate case** (statement false as written, true as used):
  - quoted BM Lemma 15 at k = 0 (unused);
  - Lemma 14^τ(c) at n₀ = 1, τ = 0 (unused);
  - BM Lemma 25 at m = 1 (fixed in v6; `bmLemma25_literal_false`).
- **GAP-grade in v6, fixed in v6.1 by the P2 triage of the formalization:**
  - **ROUND-RULES**: the "fixed rules" of the round step had no declared arguments. PATCHES.md: "without it, adversarial rules falsify the claims: a grouping that reads η_h makes SDR failure almost sure; an (e2) order that reads ≺_u steers junctions".
  - **M-INTEGER**: M_l was defined as a real number but used as a count (palettes [3M_l], K^JS = M_l², binomials).

  The repo grades both T1. I would grade them GAP in v6: each made a stated round-step claim false under a literal reading.
- **Earlier, before the Lean.** Clean-room AI review found one **major gap**, PV-ARC-END: the arc-end bound of Lemma PV(c) missed arcs created by stripping in the finish. It was repaired as CR1-PV.

**Data point on reliability.** An unformalized AI-written proof of 150+ pages, after six rounds of AI review, still contained, in the text the Lean was written against:
- 2 GAP-grade issues (ROUND-RULES, M-INTEGER), both caught by formalization triage;
- about 16 minor T1 slips and 13 cosmetic T0 slips;
- 3 statements literally false at degenerate parameters.

None was fatal or reached a theorem as used. In addition, the Lean found the paper's most intricate proof (JS-LC Steps 4–5) unnecessary (D29).

**Did the final paper apply them?** Yes. I spot-checked 14 errata in `paper/src`, all applied:
- Lemma 14^τ(c) "if τ > 0";
- 1 + 1/c_OV = 3.4094…;
- OV-546 (5.455… ≤ 5.46);
- BM Lemma 15 "k ≥ 1";
- Γ1(d) "follows from (a)";
- (R5)(3) "in the home order";
- propDegRec(b) leaves non-empty;
- JS-LC "If R_Y has no non-giant component, 𝒮₀ is empty";
- JS-LC claim (c) "the equality uses M_l ≥ 2";
- (J2) without the 1.37 factor, with s7's consumer rewritten;
- the ⌈N₀⌉ ≥ 2^{1024} parenthetical;
- the lemParent(i) connector clause restated;
- Lent-set disjointness for Y ≠ Y′ via (F-c);
- lemLost(i) sharpened to |V(Y)|^{−2}/2 + |Y|^{−2}/2.

The only other changes from v6.1 to the final paper are removed `\fixes`/red-team tags and the removed status text (objection 4). No statement content changed beyond the errata.

## 7. Paper vs Lean on the five most load-bearing statements [helper map; spot-read by me]

| Paper statement | Lean | Verdict |
|---|---|---|
| `s7:thmJVps` (Thm 7.19) | `JVpsStatement` (`Spec/Quot/JVps.lean:56-66`), called directly at `Proof/Main.lean:64`; C0/eps1/eps2/FQ/detl match formula by formula | SAME |
| `s7:thmHI` + `s7:thmMainProof` | `HIHyp`/`HIStatement` (`Spec/Quot/HI.lean:54-71`); c = ⌈max(C₀/(1−2θ_Q), N₀/2)⌉₊ | SAME (Lean stronger: no sign conditions) |
| `s7:lemLift`(ii),(iv) | used via identical library copies `liftDecomp_core` and `liftJConsumerRun_univ`; JC2 = IsDecomp(J ∪ LentJV) | SAME; (iii) WEAKER and unused |
| `s6:thmCONCL`(iv) + `s2:propOV`(K2) + Tower(e) | `ConcLSumStatement`, `OVRunStatement`, `TowerEStatement` (needs only Γ1(a)–(e) or Γ2(a)) | SAME |
| `s6:thmMIXC`(c), `s7:propCost` | `MixCStatement`/`CostStatement`: existential J_l (Option B′) | WEAKER in shape, sufficient (objection 2) |

Probabilistic steps. Stage 3 is made deterministic (∀ admissible E ∃ decomposition), and the non-emptiness of each good event is **proved** (`TPVProb.exists_good`, etc.), not assumed. Stage 1 and the per-round ξ_l stay genuinely probabilistic, with Markov existence proved. No undischarged hypothesis or assuming structure field remains on the route [helper].

## 8. Bottom line for the cron

Within my scope I found nothing that breaks Proof B. The induction closes with the stated constants. The quotients are strictly smaller simple graphs, and their lifts partition E(G) exactly once, with junction edges private to one end and one object. No per-round Θ(n) cost survives. The BM citations are faithful.

The honest residuals are about the paper's **proofs** of JS-LC and of the MIX-C assembly, not about the theorem: in both places the Lean proves the same statements by different, simpler routes. The truth of the theorem then reduces to our kernel replay and to statement fidelity. The fidelity of FC `erdos_184` looked right to me: IsCycleOrEdge on `H.coe`, IsDecomposition = PairwiseDisjoint edge sets with union E(G), and f fixed before V. That check is another seat's lane.
