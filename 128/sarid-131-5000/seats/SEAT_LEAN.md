# Seat LEAN — source audit of the formalization (no build needed; the host may run a kernel replay separately)
Read COMMON.md first, then lean/README.md, Erdos128/ModuloBCL.lean, Erdos128/ExternalInputs.lean,
Erdos128/DeepMindTarget.lean, Erdos128/GraphBasics.lean, AxiomAudit.lean, lakefile.toml, lean-toolchain.

1. State, in plain words, the exact TYPE of `Erdos128.ModuloBCL.sparse_half_131_5000` and
   `formalConjectures_131_5000`, unfolding `HasSparseHalf`, `edgeCountOn`, `BCLEventual`, `BCLCutCertificate`,
   `FormalConjecturesStatement`. Confirm or refute: (i) the conclusion is "∃ S, |S| = ⌊n/2⌋ ∧ e(S) ≤ (131/5000)n²"
   with Nat floor division; (ii) `edgeCountOn G S` counts exactly the edges with both ends in S
   (`G.edgeFinset ∩ S.sym2` — is `S.sym2` the set of unordered pairs from S incl. diagonal? does the diagonal
   matter?); (iii) `BCLEventual` is EXACTLY BCL Thm 2(a) and not weaker/stronger (∃N ∀ graphs with ≥ N vertices,
   triangle-free → ∃ bipartition with ≤ (2/47)n² internal edges) — note it quantifies over `Type` (universe 0):
   is that a restriction vs the paper? (iv) `FormalConjecturesStatement 1 50` vs the upstream FC body: the upstream
   has `50 * … > Fintype.card V ^ 2`, Sarid's has `denominator * … > numerator * Fintype.card V ^ 2` — with
   numerator 1 that is `1 * n^2`; is "definitionally the body" true (`Iff.rfl`-level) or only up to `one_mul`?
   Quote both.
2. Hunt for cheating constructs across all 683 files: sorry, admit, axiom, native_decide, implemented_by, extern,
   unsafe, opaque, partial, `decide := true` configs, `Lean.ofReduceBool`, `trust`, custom `instance : Decidable`
   that could be wrong (a wrong Decidable instance can't make the kernel accept a false theorem, but a wrong
   DEFINITION can make a true theorem say nothing — so audit the DEFINITIONS: `c4Hom`, `edgeDensityQ`,
   `c4DensityQ`, `C4FlagCertificate`, `IsFractionalHalf`, `edgeCost`, the balanced blow-up, `cliqueFree`).
   Report the grep counts and the one `opaque` mention (C4Certificate/Defs.lean:214 is a comment — confirm).
3. The C4 certificate route in Lean: read C4Certificate/{Defs,Semantics,Soundness,Provider,GlobalBridge}.lean.
   What is `certificate_all_triangleFree_masks` (type)? How does the development go from a check over 6-vertex
   masks to `C4FlagCertificate G` for an arbitrary finite triangle-free G (sampling with repetition? a counting
   identity over 6-tuples of vertices?). Is there any `n ≥ 6` or `n ≥ 1` side condition that leaks into the
   endpoint? What do `maxHeartbeats 0`/`maxRecDepth 1000000` protect (how big is the finite check — 2^15 masks?).
4. The BCL bridge: BCLCertificate/{Semantics,Bridge}.lean — how `bclCutCertificate_all_of_eventually` removes "n large"
   (balanced blow-up by k ≥ N/n); check the blow-up is defined so that D₂ scales by k² and triangle-freeness is
   preserved (`cliqueFree_balancedBlowup`).
5. The 11 edited files (README "Provenance"): verify the constants in LowDensity.lean and SimpleBound.lean are
   7/22, 131/5000, 88/417, 1/100, M0 = 7/44 as the README says, and that nothing else differs from the paper's
   constants (γ = 3/64 + 1/5e10, I₀ = 2/47). Compute the README's SHA-256 of the 680 files and compare.
6. Could the package be built here? Report lean-toolchain (v4.30.0) and the mathlib rev; the host has elan toolchains
   incl. v4.30.0 under /tmp/oaimath/166/lean-build/home/.elan but NO mathlib cache for v4.30.0 and ~6 GB free disk.
   Estimate (do NOT run): size of `lake exe cache get` for mathlib at that rev, and the build cost of these 683 files
   (count `decide`/`maxHeartbeats 0` modules). Do not build.
Write REPORT.md as specified.
