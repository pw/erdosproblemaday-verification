# Hostile referee report — PROOF A (OpenAI, "A linear cycle-and-edge decomposition of every graph", 24 Sep 2026)

Seat: Proof A, whole argument from TeX (preprints/.../build/{main.tex, sections/*.tex, figures/lifting.tex}), cited inputs, paper-vs-Lean.
Written 2026-10-20. No `lean`/`lake` run; Lean read as text only.

## VERDICT: HOLDS WITH FIXES (expository only) — no FATAL, no GAP found
Fixes: (A.3) state the size of C (≈2^{7.6·10^{12}}); (A.4) note the greedy routing proof / that AH is avoidable; (A.5) label
Cor. 1.2(ii) as resting on GGKO Prop 6.3 and as not formalized; (A.10) fix cleveref so lemmas are not printed as "Theorem";
(B, FC) the FC `formal_proof` link points at a theorem with a different (equivalent) statement; minor cosmetics A.6–A.9.

Fixes requested are all EXPOSITION/COSMETIC. Every inequality the induction uses was recomputed and holds
with the stated constants; the order of constant choices is non-circular; every recursive call is on a strictly smaller graph;
the lifting argument is correct and its three routing guarantees are each necessary (negative controls) and jointly sufficient
(randomised end-to-end simulation). The one piece of Theorem 1.1's proof that rests on an external theorem in the paper
(Aharoni–Haxell, inside lem:routing) is proved in the Lean by a different, elementary greedy argument for the *same* statement,
and Lovász 1968 is proved from scratch in the Lean — so the formal proof of Theorem 1.1 has no external mathematical input.
Corollary 1.2 is paper-only (not in the Lean); its second assertion rests on GGKO2021 Prop. 6.3, whose (⇐) proof is a sketch
(COULD NOT CHECK in depth — out of this seat's budget).


---

## A. Objections (paper)

### 1. [none FATAL / none GAP]

I looked specifically for the three classic holes:
- *Lemma assuming the conclusion's strength*: the only appeals to the induction hypothesis are (a) the quotients Q_W, order
  q_W ≤ B_0 = D^{0.30} ≤ n^{0.30} < n (eq:individual-quotient-order, induction.tex l.348–351), and (b) the small-residue residual
  graphs, each of order < r ≤ n (lem:small-residue; induction.tex l.168–171, 369–371). Both strictly smaller. The strengthened
  hypothesis C·φ(n)·n is used on the quotients only through φ(q_W) ≤ φ(B_0) (monotonicity) and on residuals only through φ ≤ 1.
- *Citation that does not say what is claimed*: every cited statement checked against its source (§C). All say what is claimed.
- *"Clearly/standard" at the hard step*: none. The hard steps (vertex sampling without a union bound over all subsets,
  routing with team constraints, the switch/lifting simplicity, the load injection, the order-saving ledger) are all proved
  in full in the paper.
- *Accumulating per-scale cost*: none. Per-scale costs are long cycles Σ_l N_{l−1}/(2D_l^{0.01}) ≤ 20n/log D_t (geometric in
  1/log D_l, dominated by the last term — eq:prefix-cycle-cost) and the box-overlap factor ∏(1+C_0/log D_l) ≤ 1+C_2/log D_t
  (eq:layer-order); piece processing is charged to S_i via lem:prefix-choice (Σ_{j≤i+K} S_j ≤ P_0 S_i). The O(n/log D) residue
  is absorbed by the φ-gain δ/√log D on the D^{0.30}-order quotients. Checked numerically (§D).

### 2. Points I attacked hardest and that survived (recorded so the next reader need not redo them)

2a. **Order of constants / circularity** (preliminaries.tex l.41–43; proof of Proposition 7.2, induction.tex l.62–66, 439–462; parameters (7.1)). θ, K, P_0, η, C_0=2, hence
    C_2=80, H=C_2θ^{−K}≈2.28·10^6, A_1=H+4/3, A_2=max{9P_0+8, 9H}≈2.05·10^7, δ=1/√0.3−1 are fixed first; D_* is then chosen
    subject only to lemma thresholds (which depend on η, c∈{1,1/4}, absolute exponents) and to log D_* ≥ max{C_2, 40/3,
    ((A_1+1)/δ)^2}; only then C ≥ max{7A_2, 4T(D_*)}, T(D_*)=20+D_*+18P_0. No constant used before C depends on C. The
    coefficient-of-S_i step needs C ≥ (300/47)A_2 and uses C ≥ 7A_2; the absorption step needs only w ≥ ((A_1+1)/δ)^2 and
    C ≥ 7A_2 (to bound A_2 n/w by C n/w). Both checked exactly.

2b. **The φ-gain (7.20) really dominates the overlap cost, uniformly in which layer i is selected.** The overhead is (A_1+1)Cn/w with
    w = log D_i, and the gain is C n(φ(n)−φ(D_i^{0.30})) ≥ Cnδ/√w with the *same* w (because H/w = C_2/log D_t exactly, the
    θ^{−K} gap factor being absorbed into H). Verified on a grid w ∈ [40/3, 10^{13}], log n ∈ [w, w+10^{15}], S_i/n ∈ [0,2]:
    min gain/(δ/√w) = 1.000000 (equality at log n = w, i.e. i=0), inductive-cost ≤ Cφ(n)n at w ≥ w_* for C∈{7A_2, 70A_2}.

2c. **Quotient-order ledger** (eq:active-order (7.14), eq:total-quotient-order (7.17)). Σ_W q_W ≤ N_t − Σ/3, N_t ≤ (1+H/w)n,
    Σ ≥ S_i − 4n/w (non-good vertices ≤ y/w per box from eq:descendant-degree with exponent θ^{K+1}−0.01 ≤ −0.009; skipped
    occurrences ≤ L_0(1+4y/B_0)y/σ ≤ y(D^{−0.87}+4D^{−0.15}) ≤ y/w). Exponent arithmetic checked exactly. Note the paper
    correctly allows Σ_W q_W > n (l.435–437); the φ-gain pays for it.

2d. **Lifting: does every quotient cycle lift to ONE simple cycle?** (proof of Lemma 6.2, folding.tex l.297–420; Figure 1 = figures/lifting.tex). Yes. Fibers
    of z_1..z_s are disjoint; switch u_j≠v_j only inside a folded pair of one active set X_{W,R}; each switch path lies in
    V(R), its interior avoids Z_C = ⋃V(ê_j) (all representative endpoints of the whole cycle), interiors of switches of one
    cycle in one router are disjoint by the team constraint, switches in different routers lie in disjoint pieces (pieces in
    one box are vertex-disjoint). The "unused twin" case (u_j=v_j at a paired fiber) is handled explicitly (l.407–414).
    Randomised end-to-end simulation (§D, lifting_sim.py): 200,092 lifted quotient cycles incl. 24,426 switch paths, all simple,
    all parts pairwise edge-disjoint, union = E(F) ∪ ⋃U_R exactly, per-vertex demand load ≤ d_F(x) ≤ a. **Negative controls:**
    dropping Z_C-avoidance → "repeated vertex in lifted cycle"; dropping team-disjointness → "repeated vertex"; dropping router
    edge-disjointness → "edge used twice". So each guarantee of lem:routing is load-bearing and the three together suffice.

2e. **Edge-disjointness across ALL lifted cycles and from all other parts.** Route edges ⊆ E(P_R) ⊆ E(R), and E(R) ∩ E(F(Y)) = ∅
    because pieces are removed at stage i and F(Y) is the stage-t remainder (eq:global-edge-ledger); routers of different
    pieces are edge-disjoint (pieces in different boxes carry disjoint assigned edges even when vertex sets overlap); one
    routing application per router covers all batches and both demand types (l.376–382). Every original edge lands in exactly
    one of: long cycle / piece (router-used, small-residue part, or residual H') / batch edge (trimmed single, remnant cycle,
    folding error single, or quotient representative) — eq:global-edge-ledger + l.373–385 + l.422–452. (My first simulation
    run modelled the router as K_{V(R)} without removing F-edges and "found" a double use; that was my model, not the paper:
    G simple ⇒ E(R) ∩ E(F) = ∅. Recorded so nobody re-files it.)

2f. **Load bound across batches** (eq:batch-global-load, in the proof of Lemma 6.2). The injection from demand-end occurrences at x into F(Y)-edges at x is
    correct: remnant ends ↦ terminal E_X-edge; switch ends ↦ ê_{j−1} (at u_j) / ê_j (at v_j); an edge ê_j is associated at most
    once per endpoint because its two endpoints lie in different fibers z_j ≠ z_{j+1}; designated E_X edges were removed before
    folding; batches have disjoint J_W. Hence k = a = D^{0.01} is valid with b = B_0, z = 2B_0, and ℓ²(a+B_0)+2B_0 =
    O(D^{0.54}log⁴D) = o(σ/256).

2g. **Small residue** (lem:small-residue = Lemma 4.3; lem:vertex-sampling = Lemma 4.2): three disjoint reservoirs, every non-reserved edge avoids some reservoir, representative
    capacity k_0 = ⌈8r/(ph)⌉, routing margin ℓ_i²(k_0+1) = O(D^{0.68}log⁴D) = o(τ=D^{0.74}); counts 3r cycles + 6r singles = 9r;
    residual order ≤ 6pr ≤ ηr with each < r. Correct. The vertex-sampling lemma's "approximate a failing cut by a union of
    ≤ s neighbourhoods" argument is correct, exponents 0.12 < 0.78, −0.16, −0.04 checked.

2h. **Splitting** (lem:scale-split = Lemma 5.1, lem:split-vertex-expansion = Lemma 5.2): DFS balance (unexplored − finished passes through 0), the
    X/J/Z segment argument, the potential f with f(u)−f(u_1) ≥ log(4/3)/log²u and εf ≤ 1/16 < log₂(4/3) — all correct. C_0 = 2
    via 1/(1.02 log D − 1) ≤ 2/log D for log D ≥ 2.

2i. **Pair folding** (lem:pair-folding = Lemma 6.1): exact pairing probabilities incl. the dummy-vertex odd case; the three collision classes
    exhaust distinct-edge pairs in a simple graph; 4/7+16/35+16/49 = 332/245 < 2 (exact). Simulation max |E_err|/Σm_i = 0.33.

### 3. [EXPOSITION] The constant is astronomically large and the paper never says so
induction.tex \label{eq:cutoff-absorption}, printed (7.21), in the proof of Proposition 7.2 (l.432–434): `\log D_*\ge\left(\frac{A_1+1}{\delta}\right)^2`.
With the paper's own values A_1 = H + 4/3, H = C_2θ^{−K} = 80·0.95^{−200} ≈ 2.28·10^6, δ ≈ 0.8257, this forces
log₂ D_* ≥ 7.64·10^{12}, and C ≥ 4T(D_*) > 4D_* ≥ 2^{7.6·10^{12}}. Nothing is wrong — "absolute constant" is literally true and
explicit — but the abstract/Theorem 1.1 reader should be told C is of order 2^{10^{12.9}} (compare BM's O(n log* n) with small
constants for all practical n). Fix: one sentence after Prop. induction-bound stating the size of C.

### 4. [EXPOSITION] lem:routing (printed Lemma 3.1) proof uses Aharoni–Haxell (Theorem 2.3); an elementary greedy proof of the same statement exists (it is the Lean's)
routing.tex l.7–9 "Its proof uses the hypergraph formulation and expansion-to-connectivity method of Bucić and Montgomery";
l.231–233 "Applying \Cref{thm:aharoni-haxell} gives disjoint hypergraph representatives".
The Lean `routing` (Routing.lean l.874–1030) proves the identical conclusion under the identical hypothesis
`64 * (routingLength^2 * (k + b) + z) ≤ h` by routing demands one at a time, keeping every vertex's used-edge degree
≤ h/8 + 2 + (endpoint load) and forbidding "saturated" vertices (≥ h/8 used edges, at most h/8 of them since 128|F| ≤ h²)
internally. This removes AH from the trusted mathematical base. Not an error in the paper; worth a remark (and it makes
thm:aharoni-haxell unnecessary for Theorem 1.1).

### 5. [EXPOSITION] Corollary 1.2(ii) is paper-only and rests on a sketched proposition
main.tex, proof of \label{cor:eulerian-cycles} (printed Corollary 1.2): "Their Proposition~6.3 proves that Conjecture~1.14 ... is equivalent to their
Erd\H{o}s--Gallai Conjecture~1.4, supplied by \Cref{thm:main}."
Checked against GGKO arXiv 1911.05501v2: Prop. 6.3 is stated exactly so, Conjecture 1.14's quantifiers ("For any δ, p > 0,
there exist ε, n_0 > 0 ... Eulerian weakly-(ε,p)-quasirandom ... at most Δ(G)/2 + δn cycles") match the corollary, and the
weak-quasirandom definition (§1.2) matches the cut condition. But the (⇐) direction is a one-paragraph sketch ("apply the
arguments of Step 1 of the proof Theorem 1.10(ii) ...", "by similar arguments as in the proof of Theorem 1.11"). The
corollary inherits that. Not formalized (no Eulerian/quasirandom content anywhere in the Lean tree). COULD NOT CHECK the GGKO
sketch in depth. Fix: label Cor. 1.2(ii) as conditional on GGKO's published argument (it is), and say it is not in the Lean.
Cor. 1.2(i) is a correct two-line deduction (parity + greedy cycle removal, ≤ s/3 ≤ s cycles).

### 6. [COSMETIC] induction.tex l.111–112 (proof of Proposition 7.2, just before (7.5)) "Increase the absolute constant C_0 ... if necessary so that C_0 ≥ 1"
Redundant: lem:scale-split already fixes C_0 = 2 (splitting.tex l.19, l.293). Harmless.

### 7. [COSMETIC] routing.tex l.67–68 (proof of Lemma 3.1, before (3.3)) "Each matching member uses at most ℓ graph edges and at most ℓ tokens"
At most ℓ−1 tokens; the bound used is weaker and fine.

### 8. [COSMETIC] residue.tex l.95 / l.191–192 (proof of Lemma 4.2) "Here the chosen value of C_p is more than sufficient"
pM/4 = 4 log₂ r, so r·e^{−pM/4} = r^{1−4/ln2} ≈ r^{−4.77}; claim r^{−3} < 1/4 for r ≥ 2 checked. Fine; could just say so.

### 9. [COSMETIC] main.tex §1 (introduction) vs AABC2025 Thm 1.7 wording
main.tex: "improved this covering bound to n−2 for graphs containing a cycle." AABC v2 Thm 1.7 is stated for graphs "that are
not a tree" (abstract: "containing a cycle"). The paper's form is implied (a graph with a cycle is not a tree). Intro only.

### 10. [COSMETIC — but it misleads a PDF reader] every internal cross-reference to a lemma/corollary/proposition prints as "Theorem"
The PDF (sha256 4aa44187…) renders every `\Cref{lem:…}`, `\Cref{cor:…}`, `\Cref{prop:…}` as "Theorem X.Y": pdftotext counts
"Theorem 2.2" ×2 (= Corollary 2.2), "Theorem 2.4" ×2 (= Lemma 2.4), "Theorem 3.1" ×4 (= Lemma 3.1), "Theorem 4.1/4.2/4.3"
(= Lemmas 4.1–4.3), "Theorem 5.1/5.2", "Theorem 6.1/6.2", "Theorem 7.1" (= Lemma 7.1), "Theorem 7.2" (= Proposition 7.2),
"Theorems 5.1", "Theorems 6.1". Example: induction.tex l.373 `\Cref{lem:batch-resolution} resolves exactly the batch category`
prints as "Within each Y, Theorem 6.2 resolves exactly the batch category in (7.12)". Only Theorems 1.1, 2.1, 2.3 are actually
theorems. Likely cause (inferred, not tested): cleveref with `\newtheorem{lemma}[theorem]` (shared counter) — the counter-type lookup returns "theorem".
Fix: `\crefname{lemma}{Lemma}{Lemmas}` etc. plus defining the theorem environments so cleveref sees the type (or use
`\newtheorem` via `aliascnt`/`thmtools`). No mathematical consequence; it does make "Theorem 4.3" etc. unfindable in the PDF.

---

## B. Paper vs Lean (Lean read as text; nothing run)

Lean tree: /tmp/oaimath/604/lean-build/repo/lean/OAI/Combinatorics/CycleDecomposition/ (34 files, linear import chain,
only Sampling.lean imports Mathlib). Grep audit over all 34 files: no `sorry`, `axiom`, `admit`, `opaque`, `implemented_by`,
`extern`, `native_decide`, `unsafe`, `ofReduceBool`, custom `macro/elab/syntax`, `set_option`. The only `Missing*` names
(`MissingLovaszTheorem`, `MissingEndpointTheorem`, PathDeletion.lean:66,80) are Prop-valued `def`s that are *proved*
(EndpointPartition.lean:258,265) and never used as hypotheses. `main_cost_bound` / `erdos_gallai` (Main.lean:91,207) carry
no hypotheses. Comparator JSON permits only propext / Quot.sound / Classical.choice. (Kernel replay is a separate gated step.)

**What the Lean proves.**
- **Theorem 1.1: YES**, as `OAI.ErdosGallai.erdos_gallai : MainStatement` (Main.lean:207), MainStatement =
  `∃ C : ℝ, 0 < C ∧ ∀ (n : ℕ) (G : SimpleGraph (Fin n)), ∃ k : ℕ, EdgeDecomposition G k ∧ (k : ℝ) ≤ C * n`
  (PrefixSelection.lean:104, text-identical to ComparatorChallenges/CycleDecomposition.lean), with parts
  `Fin k → Set (Sym2 V)`, each `(∃ v (p : G.Walk v v), p.IsCycle ∧ s = p.edgeSet) ∨ ∃ e ∈ G.edgeSet, s = {e}`, pairwise
  disjoint, union = `G.edgeSet`. Mathlib `IsCycle` = simple closed walk of length ≥ 3, so this is exactly Theorem 1.1 and
  exactly Erdős's question. It actually proves the stronger `decompositionCost G ≤ C·φ(|V|)·|V|` for every Fintype V
  (Main.lean:91), i.e. Prop. induction-bound itself.
- **Corollary 1.2: NO.** No Eulerian / quasirandom / Δ(G)/2 content anywhere in the tree. Both assertions are paper-only;
  (i) is a trivial deduction, (ii) rests on GGKO Prop 6.3 (§A.5).
- **External inputs:** Lovász 1968 is *proved* (Lovasz.lean:1574 `path_cycle_partition : HasPartition G` with
  `2 * k ≤ activeOrder G` — the number of non-isolated vertices, STRONGER than ⌊n/2⌋); cor:endpoint-paths is proved
  (EndpointPartition.lean:261, endpoint load ≤ 2, k ≤ |V|). Aharoni–Haxell does not occur at all (§B.1). So the formal proof
  of Theorem 1.1 has no external mathematical input beyond Mathlib.

**Where the Lean proves a different / weaker form (ranked by what a referee should care about):**

B.1 [paper-only argument] **lem:routing**: same statement, different proof. Lean `routing` (Routing.lean:874; Batch copy
BatchRouting.lean:934) has hypothesis `hbudget : 64 * ((routingLength (Fintype.card V) h : ℝ) ^ 2 * (k + b) + z) ≤ h` with
`routingLength = 2·⌈8(r/h)log₂(2r)⌉·(1+⌈log₂ r⌉)` — exactly eq:routing-condition and eq:routing-radii — and conclusions
(i)–(iii) verbatim. The proof is a greedy one-demand-at-a-time induction (`PartialRoutes`, l.864) keeping used-edge degree
≤ h/8 + 2 + endpoint load and forbidding saturated vertices; *no hypergraph, no Aharoni–Haxell*. The paper's ball-union
halving argument is formalized (`rootBallUnion_*`, `routing_large_root_ball` l.425) but **has no callers** (dead code;
verified by grep). Consequence: the AH-based proof in routing.tex is not machine-checked (I checked it by hand in this report: correct), but the
lemma it proves is, so the formal proof of Theorem 1.1 does not depend on AH. (Objection §A.4.)

B.2 [repackaging] **lem:batch-resolution** has no single Lean counterpart. The lifting is `uniform_batch_resolution`
(BatchResolution.lean:342: parts ≤ Σk_b + 8ΣΣ|X_{b,i}|, all `CycleOrSingleEdge G`, `Disjoint F.edgeSet used`,
union = `F.edgeSet ∪ used`); the P/T router split and the induction on quotients are folded into
`uniform_coupled_resolution_cost` (CoupledResolution.lean:738), which outputs `H r ≤ R r` with
`CutExpansionOn (H r) (U r) (D^(9/10)/4)` and cost ≤ t·(Σ|W_b| − ΣΣ⌊|X|/2⌋) + 8ΣΣ|X| + Σ cost(H r) — the paper's accounting.
The single-cycle lift is `complete_batch_cycle` (CycleLifting.lean:797): hypotheses = switch paths `IsPath`, interiors in
pairwise-disjoint router vertex sets, team-disjoint within a router, interiors avoid every representative endpoint;
conclusion `∃ v (c : G.Walk v v), c.IsCycle ∧ c.edgeSet = {representatives} ∪ ⋃ routes`. This is the paper's lifting
argument, with a Mathlib `IsCycle` (not a circuit) as the output — answers "one simple cycle, not a closed walk". Lean teams
are coarser (one team per template across routers, `team := Sigma.fst`, Templates.lean:714–744, forbidden set = all template
vertices); still within b = B₀, z = 2B₀, so valid and only stronger.

B.3 [weaker form, harmless] **lem:small-residue** = `small_residue` (Decomposition.lean:119): 9r parts, each residual order
< r, Σ orders ≤ ηr, σ = D^{9/10}, r ∈ [D^{9/10}, D^{51/50}], τ = D^{37/50}. It does **not** export pairwise vertex-disjointness
of the three residual vertex sets (residuals are `H b ≤ G` with support ⊆ W b). Downstream (`uniform_piece_cost_on`,
Decomposition.lean:487) needs only Σ|W b| ≤ ηr, so nothing depends on the omitted clause. The Lean packages it with the
induction: `cost G ≤ (9 + Cη)|A|` under the hypothesis "every smaller graph costs ≤ C·card" — matches the paper's use
(φ ≤ 1 on residuals).

B.4 [different, harmless] **Gap condition**: paper's nonterminal case is `i+K < m−1` (induction.tex l.183–184); Lean's is
`i+200 < H.count` (Main.lean:164), which also includes i+K = m−1 (paper puts it in the terminal case). Lean's terminal case is
`m ≤ i+200`. The Lean gap-case lemma (`uniform_gap_prefix_cost`, LayerCosts.lean:177) only needs stage i+200 to exist, so both
splittings are valid; the paper's is merely conservative.

B.5 [internal constants differ, no effect] vertex-sampling witness parameter M = D^{1/100} (Lean) vs C_p log r (paper);
pair-folding cross-collision constant 32/49 (Lean, BatchPreparation.lean:434,480; total 412/245) vs 16/49 (paper; total
332/245) — both < 2, the paper's is the sharper and also correct (it halves for unordered pairs); edge-split failure bound
l(e^{r e^{−h/(8l)}}−1) vs 2lΣ(·)^u; long-cycle lemma generic in α (STRONGER); active-set hypothesis `8 ≤ |X| ∧ a² ≤ |X|`
instead of |X| ≥ D^{0.03} (STRONGER, since L₀ ≥ max{8,a²}); `uniform_layers` needs only 2e/|V| ≤ |V| (weaker than paper's n−1).

B.6 [constants identical] θ = 19/20, K = 200, mainP = 804 = 4(200+1), mainEta = 1/(100·mainP), mainH = 80/θ^200 (C₀=2,
C₂=80), mainA₁ = mainH + 4/3, mainA₂ = max(9·mainP+8, 9·mainH), inductionDelta = 1/√(3/10) − 1, inductionPhi as in
eq:induction-potential on [1,∞) (CoupledResolution.lean:403; value 1 off [1,∞), unused), C = max(4(20+D*+18·mainP), 7·mainA₂)
(Main.lean:105), wmin = max 80 ((mainA₁+1)/δ)² (Main.lean:94; paper: log D* ≥ max{C₂=80, 40/3, ((A₁+1)/δ)²}), and
`MainScaleReady` (CostRegrouping.lean:162) = the paper's four displayed eventual inequalities + 8 ≤ D^{3/100}.
`induction_cost_absorbed` (CoupledResolution.lean:483) is eq:inductive-cost ≤ Cφ(n)n verbatim (C·ηP₀ = C/100).

B.7 [readability] namespace duplication: Lovász, path deletion, endpoint partition, reservoir cycles, edge splitting and
`decompositionCost` each exist in 2–3 namespaces (ErdosGallai / .Scale / .Batch), bridged by `rfl` (Main.lean:86–89).
Any manual audit has to track which copy is in the chain.

**Statement fidelity w.r.t. Formal Conjectures.** The FC file (main, fetched 2026-10-20) tags `Erdos184.erdos_184` as
`formal_proof using lean4 at ".../Main.lean#L207"`, but that line proves OpenAI's `MainStatement` (Fin n, parts as
`Set (Sym2 V)`, k ≤ Cn), not FC's `erdos_184` (`∃ f =O[atTop] n, ∀ {V : Type*} [Fintype V] [DecidableEq V] G,
∃ D : Finset G.Subgraph, (∀ H ∈ D, IsCycleOrEdge H.coe) ∧ IsDecomposition G D ∧ D.card ≤ f |V|`). The two are mathematically
equivalent (transport along V ≃ Fin |V|, universe-polymorphic V, `Subgraph.fromEdgeSet` of a cycle's edge set is connected
2-regular on its vertex set), but that bridge is not formalized in the OpenAI repo. [EXPOSITION / FC metadata, not a math gap.]

---

## C. Cited inputs — checked against sources

| Cited | Source checked | Verdict |
|---|---|---|
| thm:lovasz — "at most ⌊n/2⌋ paths and cycles", edge-disjoint (Lovász 1968 Thm 1) | Primary not fetched (Academic Press proceedings). Secondary: BM arXiv v2 Thm 21 ("at most n/2 paths and cycles"), CFS arXiv Thm 1.1. **Also proved from scratch in the Lean** (Lovasz.lean `path_cycle_partition`, `2 * k ≤ activeOrder G`) | SAYS WHAT IS CLAIMED |
| cor:endpoint-paths = BM Cor 22 | BM v2 §5.2, Cor 22 + proof (same v_0 augmentation) | SAME; paper's deduction re-proved, correct |
| thm:aharoni-haxell bounded-rank form = BM Thm 6 | BM v2 §2.5 Thm 6 verbatim ("at most ℓ vertices in each edge … matching … more than ℓ(|I|−1) edges"), stated there as a consequence of AH2000 Cor 1.2 via padding with new unique vertices — same padding remark as preliminaries.tex l.118–123. AH2000 primary (JGT 35) not fetched (paywalled) | SAYS WHAT IS CLAIMED; and not needed by the Lean (§A.4) |
| BM Prop 8 / Lemma 9 (routing method) | BM v2 §2.6 | attribution of method only; paper proves its own lemma |
| BM Lemma 14 (overlapping split, Σ|G_i| ≤ 2n) | BM v2 §3.3 | attribution; paper proves its own (1+2/log D) version |
| BM §2.2, Lemma 23 (three classes, close paths) | BM v2 §2.2 proof sketch; §5.3 Lemma 23 (three expanders, three vertex classes, Cor 22, close through V_i) | attribution matches |
| BM Lemma 25 (DFS long cycle) | BM v2 §5.5 Lemma 25 | attribution matches; paper re-proves with its constants |
| BM §4 (sampling) | BM v2 §4 "Finding edge disjoint paths through random vertex sets" | attribution matches |
| BM §6 lower bound (3/2−o(1))n | BM v2 §6: K_{2k+1,n−2k−1} gives (3/2 − 1/(4k+2) − o(1))n | matches (k→∞) |
| CFS Lemma 3.1 (sparse-cut removal), Lemma 6.3 (bipartite path trimming), §3, Thms 1.3/1.4 | CFS arXiv 1310.0632v2 | all match as attributions |
| GGKO Thm 1.10(iii), §1.1 equivalence, §1.2 weak quasirandomness, Conj 1.14, Prop 6.3 | GGKO arXiv 1911.05501v2 | statements match; Prop 6.3 (⇐) proof is a sketch (§A.5) |
| AABC Thms 1.3, 1.7 | arXiv 2509.01901v2 | match (1.7 slightly stronger than quoted) |

Versions: BM = arXiv 2211.07689**v2** (14 Nov 2023, current; the bib note pins numbering to v2). GGKO = 1911.05501v2 (current).
CFS = 1310.0632v2 (current). Files in /tmp/oaimath/181/refs/{bm,ggko,cfs,aabc}/.

---

## D. Numeric checks run (all under /tmp/oaimath/181/seats/openai_checks/)

`induction_checks.py` — 64 checks, **0 FAIL** (output in induction_checks_results.txt). Covers: eq:scale-window (θ^K = 3.505e−5 ≤ e^{−10}; 1.02θ^K, θ^{K+1} < 0.001);
Σθ^t = 20; e^x ≤ 1+2x on [0,½]; the layer-order product bound ∏(1+C_0/log D_l) ≤ 1+C_2/log D_j for every j with log D_j ≥ C_2
(max ratio 0.999999); Σ1/log D_l ≤ 20/log D_j; H/w = C_2/log D_t identity; lem:prefix-choice on 20,000 random sequences and on
geometric sequences with K up to 200; ηP_0 = 1/100 exactly; A_2 + C/100 − C/6 ≤ 0 at C=7A_2 (value −0.0967A_2); 300/47 < 7;
φ(B_0) non-constant iff w ≥ 40/3; eq:potential-gain on a grid (min ratio 1.000000); absorption threshold
log₂D_* ≥ ((A_1+1)/δ)² = 7.6392·10^{12}; the full eq:inductive-cost ≤ Cφ(n)n at and above threshold for S_i/n ∈ [0,2];
terminal/base inequalities; all exponent identities (−0.87, −0.15, −0.009, 0.54<0.90, 0.68<0.74, 0.12<0.78, −0.16, −0.04,
0.01>0); greedy batching ≤ 1+2T_Y/B_0 (5,000 random trials); ⌊m/2⌋ ≥ m/3; eq:routing-length-bound ℓ ≤ 108(r/h)log²r
(max ratio 0.629 over r ∈ [2, 10^{12}], h ∈ (0,r)); log₂(1+x) ≥ x/2; routing budget ratios; Chernoff constants
(1−ln2)/2 = 0.153 ≥ 1/8, 2ln2−1 = 0.386 ≥ 1/3; r·e^{−4log₂r} ≤ r^{−3} < 1/4; representative-capacity saturation;
p = min{η/12,1/12}; 3r+6r = 9r; 332/245 < 2 exact; m/(m−1) ≤ 8/7, m/(m−3) ≤ 8/5 for m ≥ 8; C(d,2) ≤ (a−1)d/2; 6+2 = 8.

`lifting_sim.py` — randomised end-to-end simulation of heavy-neighbour trimming → random pair folding → loop/parallel cleanup →
an arbitrary cycle-and-edge partition of each quotient → switch demands → routes honouring exactly the three lem:routing
guarantees → lifting, with global edge accounting. Runs (seed, instances, a, density): (7,3000,2,2), (11,3000,2,2), (3,2000,3,1), (5,2000,4,2), (9,1500,5,2), (13,1500,3,3),
(21,3000,3,1): 16,000/16,000 instances complete, all assertions pass — 200,092 lifted quotient cycles, 24,426 switch paths,
max |E_err|/Σm_i = 0.333 (bound 2). Output saved in lifting_sim_results.txt. Negative controls (mutation arg 5): `noZ` → AssertionError repeated vertex;
`noteam` → repeated vertex; `noedge` → edge used twice. (Route *existence* is lem:routing's job and is not simulated; this
checks that the routing lemma's guaranteed properties suffice for the lifting and the ledger.)
