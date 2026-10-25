# Seat LEAN: source audit of the Lean package for Sarid's 131/5000 claim (Erdős #128)

I read the source only. I did not run lake or lean: the kernel replay belongs to the host. Package root:
`/tmp/erdos1800/claim/erdos-128-sparse-halves/lean/` (paths below are relative to it). All of my logs and scripts are in
`/tmp/erdos1800/seats/lean/`.

## 1. VERDICT
HOLDS AS READ at source level, pending the host's kernel replay. The endpoint's type faithfully states
"BCL Theorem 2(a), exactly as published ⇒ every finite triangle-free graph has ⌊n/2⌋ vertices spanning ≤ (131/5000)n² edges".
It has no hidden hypothesis, no shadowed definition and no cheating construct. I found nothing FATAL and nothing at
GAP level. Everything below is EXPOSITION.

## 2. Findings, most severe first (none FATAL, none GAP)

### 2.0 What the endpoint says (the item-1 unfolding). Verdict: HOLDS AS READ. Label (a).
- `Erdos128/ModuloBCL.lean:50-55`
  ```lean
  theorem sparse_half_131_5000 (hBCL : BCLEventual) (V : Type) [Fintype V] [DecidableEq V]
      (G : SimpleGraph V) [DecidableRel G.Adj] (htri : G.CliqueFree 3) :
      HasSparseHalf G ((131 / 5000 : ℚ) * (Fintype.card V : ℚ) ^ 2)
  ```
  Unfolded, with `GraphBasics.lean:62-64` and `:24-25`, this reads: for every finite V : Type and every
  simple graph G on V with no 3-clique,
  `∃ S : Finset V, S.card = Fintype.card V / 2 ∧ ((G.edgeFinset ∩ S.sym2).card : ℚ) ≤ (131/5000)·|V|²`.
  - (i) CONFIRMED. `/` is `Nat` division between two `ℕ` terms, so the size is ⌊n/2⌋. The bound is the rational
    `(131/5000)·n²`, with no truncation, and the comparison is `≤`.
  - (ii) CONFIRMED. Mathlib's `Finset.sym2 S` is every unordered pair from S, diagonal `s(a,a)` included. The diagonal
    does not matter, because `G.edgeFinset` never contains a diagonal element (a simple graph is irreflexive). So
    `edgeCountOn G S` is exactly the number of edges with both ends in S. The package also proves that this count
    equals the upstream count: `DeepMindTarget.lean:42-61` `edgeSet_ncard_induce_finset :
    (G.induce (S : Set V)).edgeSet.ncard = edgeCountOn G S`.
- `ModuloBCL.lean:30-34`
  ```lean
  def BCLEventual : Prop := ∃ N : ℕ, ∀ (W : Type) [Fintype W] [DecidableEq W] (H : SimpleGraph W) [DecidableRel H.Adj],
      N ≤ Fintype.card W → H.CliqueFree 3 → BCLCutCertificate H
  ```
  with `ExternalInputs.lean:25-28`
  `BCLCutCertificate G := ∃ X : Finset V, ((edgeCountOn G X + edgeCountOn G Xᶜ : ℕ) : ℚ) ≤ (2/47 : ℚ) * (Fintype.card V : ℚ)^2`.
  - (iii) CONFIRMED: this is exactly BCL Theorem 2(a). The source, `papers/bcl.txt:71-75`, reads: "Theorem 2. Let G be a
    triangle-free graph on n vertices. Then, for n large enough, (a) D₂(G) ≤ n²/23.5". Here 1/23.5 = 2/47 exactly.
    D₂ = min over bipartitions (X, Xᶜ) of e(X) + e(Xᶜ), since deleting a set of edges leaves a bipartite graph iff that
    set contains all internal edges of some bipartition (a). "For n large enough" is `∃ N, N ≤ card W`. The
    hypothesis is neither weaker nor stronger. The package then proves (Bridge.lean:60-93) that it is equivalent to
    the all-n form, which is the same remark BCL themselves make (bcl.txt:235-247).
  - Universe: `W : Type` means universe 0. As a hypothesis this makes the condition easier to discharge (BCL is only
    asked for Type-0 graphs), and the conclusion is also Type-0 only. The upstream Formal Conjectures (FC) statement
    has the same `V : Type`. Every finite graph is isomorphic to one on `Fin n : Type`, so this is no mathematical
    restriction. (a), EXPOSITION.
- `ModuloBCL.lean:62-63`: `theorem formalConjectures_131_5000 (hBCL : BCLEventual) : FormalConjecturesStatement131_5000`.
  It unfolds (`DeepMindTarget.lean:24-29,33-34`) to
  `∀ (V : Type) [Fintype V] (G : SimpleGraph V), (∀ V' : Set V, 2 * V'.ncard + 1 ≥ Fintype.card V →
     5000 * (G.induce V').edgeSet.ncard > 131 * Fintype.card V ^ 2) → ¬ G.CliqueFree 3`.
  The proof (`DeepMindTarget.lean:65-86`) instantiates V' := S with |S| = ⌊n/2⌋ (so 2|S| + 1 ≥ n) and finishes with
  `omega`. HOLDS AS READ.

### 2.1 (iv) "definitionally the body" is true only up to `one_mul`. EXPOSITION. Label (a) by reading; not kernel-tested.
- Quote, `DeepMindTarget.lean:22-23`: "For `numerator = 1` and `denominator = 50`, this is definitionally the body in
  the upstream Erdős 128 declaration."
- Upstream (FC checkout bdda9748, shallow), `FormalConjectures/ErdosProblems/128.lean:38-40`:
  `∀ (V : Type) [Fintype V] (G : SimpleGraph V), (∀ V' : Set V, 2 * V'.ncard + 1 ≥ Fintype.card V →
     50 * (G.induce V').edgeSet.ncard > Fintype.card V ^ 2) → ¬ G.CliqueFree 3`
- Sarid's version with numerator 1 has `1 * Fintype.card V ^ 2` in place of `Fintype.card V ^ 2`. `Nat.mul` recurses on
  its second argument. Here that argument is `Fintype.card V ^ 2`, which is stuck on the free `Fintype` instance, so
  `1 * x` does not reduce to `x`. They are equal only through the induction lemma `Nat.one_mul`, so the two bodies
  agree by `simp only [one_mul]`, not by `Iff.rfl`.
- No harm: nothing in the package ever instantiates `FormalConjecturesStatement 1 50` (grep: 0 hits), and the endpoint
  is the 131/5000 instance, honestly labelled. The phrase in `C4Certificate/Provider.lean:29-31` ("definitionally the
  upstream … with only the numerical threshold changed") is fair.

### 2.2 Stale "trust boundary" comment, and dead code inside the import closure. EXPOSITION.
- Quote, `SimpleBound.lean:81`: "`SimplifiedCertificate` is the precise trust boundary of this formalization."
  The endpoint does not use it. `IntegratedBound.lean:29-98` goes straight through
  `C4Certificate.exists_highDensity_profile` and `exists_lowDensity_profile` → `LowDensity.calculus_bound`.
  `SimplifiedCertificate`, `SimplifiedGraphCertificate` (`GraphCertificate.lean:42`) and
  `sparse_half_131_5000_of_certificate` are referenced only in SimpleBound.lean and GraphCertificate.lean. The real
  trust boundary is `BCLEventual`.
- `BCLCertificate/Semantics.lean` (rooted-cut semantics) and `Bridge.lean:26`
  `bclCutCertificate_of_rootedCutCost_le` are also unused by the endpoint. They look like residue of a BCL
  reconstruction: the generated files cite `bcl_reconstruction/generate_host_classification.py` and
  `F_edges2__n8_unlabeled.txt`, neither of which is shipped. That is harmless, because the kernel re-checks the
  generated data, not the generator.

### 2.3 "Exhaustive check over every triangle-free mask" describes the coverage, not the method. EXPOSITION. Label (a).
- Quote, README.md:50-51: "proved here, by an exhaustive check over every triangle-free mask on six vertices". The
  same phrase is in claim.txt:549.
- The kernel never enumerates the 2¹⁵ = 32,768 masks or the 5,789 triangle-free ones. The method is:
  - an orbit classification by vertex extension, orders 0→6 (`FiniteHostData/Order6.lean:39`
    `covers_order6_checked : Covers 6 order6Codes`; definition `FiniteHostClassification.lean:525`). The last step
    has 14 parents × 32 neighbourhood profiles: 235 transitions checked by `rfl` on a Boolean `validAtCheck`, and 213
    non-independent profiles dismissed by `decide`;
  - relabelling invariance (`Relabel.lean:135,230`);
  - 38 representative evaluations (`C4Certificate/HostData.lean:44`), each a 720-order moment table checkpointed
    in 8 files per host, followed by a `norm_num` comparison.
- The theorem nevertheless covers every mask. `certificate_all_triangleFree_masks (m : Mask)
  (htriangle : IsTriangleFreeMask m) : sosCoefficient m ≤ targetCoefficient m` (`FiniteCertificate.lean:26-30`)
  quantifies over all `m : Fin 15 → Bool`. I independently rechecked the cover (§3).

### 2.4 The paper's Theorem 1.1 omits the BCL condition that the Lean statement carries. EXPOSITION (framing).
- Quote, claim.txt:62: "Theorem 1.1. Every finite triangle-free graph G on n ≥ 1 vertices satisfies β(G) ≤ 131/5000."
- The Lean theorem is conditional on `BCLEventual`, which is honest and disclosed in the abstract and §5
  (claim.txt:546). The paper's theorem is as strong as BCL Thm 2(a), which is a EuroComb extended abstract with a
  proof sketch. Whether BCL is proved is for SOURCES, not this seat.

### 2.5 Cheating-construct grep: clean. HOLDS AS READ. Logs: `grep_cheats.log`, `grep_details.log`, `grep_extra.log`, `grep_shadow.log`.
- Run over all 683 `.lean` files:
  - 0 hits for each of: `sorry` · `admit` · `axiom` (as a declaration) · `native_decide` · `implemented_by` ·
    `@[extern` · `unsafe` · `partial` · `decide := true` · `ofReduceBool` · `trustCompiler` · `debug.skipKernelTC` ·
    `macro`/`elab`/`syntax`/`notation`/`infix` · `run_cmd`/`#eval` · `csimp` · `include` · `Fact` ·
    `attribute [...]` changes.
- The few hits are all prose:
  - `extern` (6 hits): all are the words "external"/"externally".
  - `opaque` (1 hit): `C4Certificate/Defs.lean:214`. It is inside the docstring of `keyIndex` ("…instead of an
    optimized opaque search routine"), not an `opaque` declaration. CONFIRMED.
  - `trust` (1 hit): the SimpleBound comment in §2.2.
  - `Lean.` (257 hits): all are the comment "checked by Lean."
- `set_option` values used:
  - linters;
  - `maxHeartbeats 0` (582 hits in 506 files: 228 HostCheckpoints + 240 FiniteHostData + 38 HostChecks, and nowhere
    else);
  - `maxRecDepth 1000000` (633 hits) and `maxRecDepth 100000` (7 hits).
  These only lift elaborator limits. They cannot make the kernel accept a false term.
- Decidable instances: 9 hand-written (`Defs.lean:81`, `FiniteHostClassification.lean:44,48,53,336,516`,
  `BCLCertificate/Semantics.lean:41`, `BalancedBlowup.lean:35`, plus local instances `LowDensityConstruction.lean:227,231`).
  Each is built from `infer_instance` or from `if h : check = true then isTrue (proof) else isFalse …`, so each
  carries a proof.
- No shadowing:
  - no declaration named `SimpleGraph.*`, `Finset.*`, `Nat.*`, `Set.*` or `Matrix.*`;
  - each endpoint-type name (`HasSparseHalf`, `edgeCountOn`, `BCLEventual`, `BCLCutCertificate`,
    `FormalConjecturesStatement`, `…131_5000`) is defined exactly once;
  - every `variable` line binds only `V`, the instances and `G`;
  - no auto-bound identifiers appear in the endpoint definitions.
- Internal definitions audited (item 2). They cannot weaken the endpoint, because each one is either proved inside the
  package or occurs only inside proofs. They matter only for the paper↔Lean correspondence claims, and all match the
  paper:
  - `c4Hom := trace (adjMatrix ^ 4)` = hom(C₄,G), with the explicit fourfold sum proved at
    `C4Certificate/Soundness.lean:31-38`;
  - `edgeDensityQ = 2e/n²`, `c4DensityQ = hom/n⁴`;
  - `C4FlagCertificate := n²·hom ≥ 8m³ − 2γmn⁴`, which is t(C₄) ≥ ρ³ − γρ after dividing by n⁶
    (`ExternalInputs.lean:62-73` proves that);
  - `IsFractionalHalf`: 0 ≤ x ≤ 1 and Σx = n/2 (`GraphBasics.lean:51-53`);
  - `edgeCost` = Σ over edges of x_u·x_v (`GraphBasics.lean:37-48`);
  - `balancedBlowup := G.comap Prod.fst` (`BalancedBlowup.lean:25-26`);
  - triangle-free means mathlib's `CliqueFree 3`.
  - The definition is not vacuous: it fails on K₃ and K₄ and is exactly tight at γ = 3/64 on the Clebsch graph (§3).

### 2.6 How the C₄ route reaches an arbitrary finite G (item 3). HOLDS AS READ. Label (a), with (d) for the finite part.
- `GlobalBridge.lean:25-53`, `c4FlagCertificate_of_mask_bound`, sums the pointwise mask inequality over all
  `x : Fin 6 → V`. That is sampling with replacement, n⁶ tuples. Repeated vertices give non-adjacent twin positions,
  which are still triangle-free masks (`Soundness.lean:228` `inducedMask_isTriangleFree`).
- Two identities close the argument:
  - `TargetAveraging.lean:34`: `Σₓ targetCoefficient (inducedMask G x) = 720 · (n²·c4Hom G − 8m³ + 2γ·m·n⁴)`. This is
    exact: the C₄ term leaves two coordinates free (n²), three disjoint edge indicators give (2m)³, and the γ term
    gives 2m·n⁴.
  - `ConditionalSquares.lean:37`: `0 ≤ Σₓ sosCoefficient (inducedMask G x)`. Each rank-one term is a weighted
    conditional square over its roots (`ConditionalSquaresCore.lean:173`), and all weights are positive
    (`Data.lean`, `certificateTerms_weight_pos`).
- There is no `n ≥ 6` and no `n ≥ 1` side condition. Empty sums handle n = 0. The finite check is 38 host evaluations
  plus the order-6 cover, not 2¹⁵ masks. `maxHeartbeats 0`/`maxRecDepth` guard those `rfl`/`norm_num` reductions.
- The type of `certificate_all_triangleFree_masks` is given in §2.3.

### 2.7 BCL bridge (item 4). HOLDS AS READ. Label (a).
- `Bridge.lean:60-93`. Given N, take k := N + 1 (line 70), independent of n, which is simpler than the paper's
  k ≥ n₀/n. Then |W × Fin k| = n(N+1) ≥ N (lines 74-81).
- The blow-up stays triangle-free (`cliqueFree_balancedBlowup`, `BalancedBlowup.lean:121-131`: a 3-clique
  {a,b,c} maps to {a.1,b.1,c.1}).
- D₂ scales by k²:
  - `card_edgeFinset_balancedBlowup : (balancedBlowup G k).edgeFinset.card = k ^ 2 * G.edgeFinset.card` (:179-182);
  - `hasNormalizedInternalCutBoundQ_balancedBlowup_iff` (:677) shows the normalized internal-cut bound is invariant
    under blow-up. The descent direction averages the indicator per clone class and rounds it to an integral cut.
- n = 0 is handled separately in `provider_of_eventual` (`ModuloBCL.lean:41-44`), with X = ∅.

### 2.8 Constants and provenance hash (item 5). HOLDS AS READ. Log: `constants.log`, `sha256.log`.
- `LowDensity.lean` has `M0 = 7/44` (:23), `I0 = 2/47` (:24), the junction 88/417 (e.g. :71, :135, :184) and the
  derivative threshold `1/100` (:110, :178).
- `SimpleBound.lean:21-27` has `target = 131/5000`, `densitySplit = 7/22`, `M0 = 7/44`, `I0 = 2/47`,
  `gamma = 3/64 + 1/50000000000` and `aStar = 88/417`.
- `ExternalInputs.lean:31-32` has `c4FlagGamma = 3/64 + 1/50000000000`, and `:28` has the BCL constant 2/47.
- `LowDensityConstruction.lean:26-31` writes `lowFQ` with the literals 7/44 and 2/47. The split `7/22` appears at
  `IntegratedBound.lean:36`, `Soundness.lean:205`, `HighDensity.lean:491` and `LowDensityConstruction.lean:701,758,850`.
  `HighDensity.lean:525-526` proves `(c4FlagGamma : ℝ) = gamma`.
- These all agree with the paper: γ = 3/64 + 1/(5·10¹⁰) (claim.txt:162-168), I₀ = 2/47. No stale 8/25 or 21/800 is
  left anywhere (0 grep hits).
- SHA-256 of the 680 files (excluding ModuloBCL), concatenated in `LC_ALL=C` sorted order:
  `a2f966e79e4b4c7839566eb558ecd5e2f7bace4439f155bb6498bb0ab731265a`, which matches the README byte for byte.
  This only shows the files are the ones the README describes. It is not independent provenance.
- Import closure (`scripts/imports.py` → `imports.log`): 681 files under `Erdos128/`. The closure of
  `Erdos128.ModuloBCL` is all 681, none unreached, and the only external imports are `Mathlib` and
  `Mathlib.Data.Fintype.Basic`. 681 + `Erdos128.lean` + `AxiomAudit.lean` = 683 files, so the README claim
  "680 + ModuloBCL are exactly the transitive imports" is CONFIRMED.

### 2.9 Build feasibility (item 6). Observed, not run.
- Pins: `lean-toolchain` = `leanprover/lean4:v4.30.0`. Mathlib rev `c5ea00351c28e24afc9f0f84379aa41082b1188f`
  (inputRev v4.30.0). Other deps: batteries 32dc18c, aesop 558915a, Qq a6e6c34, plausible a456461,
  proofwidgets a84b3e2 (v0.0.99), importGraph 515cf9d, LeanSearchClient c5d5b8f, Cli 6b907cf.
- The brief's environment facts are off:
  - `/tmp/oaimath/166/lean-build/home/.elan` holds only v4.34.1. v4.30.0 is at `~/.elan/toolchains/leanprover--lean4---v4.30.0`.
  - `df` shows 39 GB free on `/`, not ~6 GB.
- The host's own replay is already running in `/tmp/erdos1800/lean-build/erdos128/`. I only took read-only `du`
  measurements there and touched nothing:
  - Mathlib at this rev takes 6.7 GB on disk (8,101 `.olean`); the other deps take about 380 MB.
  - Lake's job total is 9157, which matches the README.
  - Package modules start near job 8475.
  - The latest log lines show 33–52 s per OrderFactsLight chunk.
- Estimate (c): 681 package modules, 506 of them with `maxHeartbeats 0`. At roughly 20–60 CPU-s each that is about
  4–11 CPU-hours, i.e. about 1–3 h wall at 4 threads. The compressed `lake exe cache get` download was not measured;
  I would guess 1–1.5 GB.

## 3. What I recomputed, and by which route (citable as second instruments)
- **SHA-256** (`sha256sum`, LC_ALL=C and default sort): matches the README (§2.8). (d)
- **Import closure** (`scripts/imports.py`): 681/681 reached (§2.8). (d)
- **Orbit cover**, independent of Lean (`scripts/count_masks.py` → `count_masks.log`, networkx isomorphism, my own
  decoding of the Defs.lean bit order):
  - 32,768 masks, of which 5,789 labelled triangle-free;
  - the 38 `hostMasks` are distinct, triangle-free and pairwise non-isomorphic;
  - every one of the 5,789 matches exactly one host.
  nauty separately: `geng -t 5` = 14 (the 14 parents) and `geng -t 6` = 38 (`nauty_count.log`). (d)
- **Lean certificate = JSON certificate** (`scripts/cmp_terms.py` → `cmp_terms.log`): 34 terms parsed from
  `C4Certificate/Data.lean`, 34 in `clebsch_tangent_certificate.json`, 0 weight or vector mismatches in exact
  rationals, block names in 1-1 correspondence. The Lean proof does not depend on the JSON; this only ties the
  paper's Python route to the same object. (d)
- **The `C4FlagCertificate` definition is non-vacuous** (`scripts/c4def_check.py` → `c4def_check.log`, exact rationals):
  - slack is ≥ 0 on K₂, C₅, Petersen and K₅,₅;
  - on Clebsch the slack is 0.000104858, exactly 2·(1/5e10)·40·16⁴, so it is tight at γ = 3/64 as the paper says
    (claim.txt:176);
  - it fails on K₃ (slack −31.2) and K₄ (−240), so the triangle-free hypothesis is load-bearing. (d)
- **Non-vacuity of the hypothesis** (`scripts/small_n_bcl.py` → `small_n_bcl.log`): Lean proves that BCLEventual
  implies D₂(H) ≤ (2/47)|H|² at every order, so one small violator would make BCLEventual false and the theorem
  vacuous. Exact D₂ over all triangle-free graphs with 2 ≤ n ≤ 10 (14,650 graphs): max D₂/n² = 1/25 (C₅ at n=5, the C₅
  2-blow-up at n=10) < 2/47. Consistent. (d)
- **Endpoint at small n** (`scripts/small_n_endpoint.py` → `small_n_endpoint.log`): all triangle-free graphs with
  n ≤ 11 (119,722 graphs). The worst min over ⌊n/2⌋-sets of e(S) is 2 at n=10 (bound 2.62) and 1 at n=11 (bound
  3.17). There is no small counterexample to the endpoint statement. This is a weak test: the bound is slack at
  small n. (d)

## 4. Exposition notes (short)
- DeepMindTarget.lean:22-23: "definitionally" should read "up to `one_mul`" (§2.1).
- SimpleBound.lean:81: stale "trust boundary" sentence. GraphCertificate's `SimplifiedGraphCertificate` and
  BCLCertificate/Semantics are unused by the endpoint (§2.2).
- README.md:50-51 and claim.txt:549: "exhaustive check" should say orbit classification plus 38 evaluations (§2.3).
- claim.txt:62: Theorem 1.1 is stated without the BCL condition (§2.4).
- The README's Lemma 2.2 ↔ Lean table entries all exist as declared (`readme_table.log`: all 20 names found at the
  listed modules).
- Brief vs reality: there is no `C4Certificate/Semantics.lean` (the semantics live in Defs/TargetAveraging/
  ConditionalSquares). The v4.30.0 toolchain location and the free-disk figure are also off (§2.9).

## 5. What I could not check, and why
- **Kernel replay / `#print axioms`.** Excluded by brief (the host runs it). Every "HOLDS" above is a source-level
  statement about what the declared types say, conditional on the build succeeding with the three standard axioms.
- **`1 * n^2` not being defeq to `n^2`.** Established by reasoning about `Nat.mul` reduction, not by running Lean.
- **README Provenance**, "669 copied unchanged from the development in which they were written". There is no access to
  that development. The generator scripts (`bcl_reconstruction/…`) are not shipped either; this is irrelevant to
  soundness, since the kernel re-checks the data.
- **Whether BCL Theorem 2(a) is actually established.** It is an extended abstract with a proof sketch: SOURCES seat.
- **Whether the Lean `blockKeys`/flag canonicalization agree with the Python verifier's.** Irrelevant to the Lean
  theorem, which checks its own copy: CERT seat.
- **Download size of `lake exe cache get`.** Not measured.
