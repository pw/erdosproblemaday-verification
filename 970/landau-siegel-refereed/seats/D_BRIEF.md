# Seat D — definitions audit of the Lean + a Mathlib-only statement bridge (read COMMON.md first)

Question you answer: does the Lean theorem our pages rest on SAY what the paper's Theorem 1 says, in Mathlib's own definitions, with
nothing in OpenAI's code able to change the meaning — and does its proof formalize THIS paper's argument?

Known (2026-10-23, verification/431/.../deps/): `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound` was kernel-accepted
against `ours_no_landau_siegel_zeros` (SiegelStmt.lean), std axioms; two mutants rejected; a comment-stripped scan of all 7,582
sources found `sorry` only in comparator files and no `axiom`/`admit`. THE LOOPHOLE that check left open: our statement was
elaborated in a file that ALSO imported OpenAI's modules, so an OpenAI instance / notation / macro / default_instance could in
principle have changed what `≤`, `*`, `Real.log`, coercions, `IsPrimitive`, `χ ≠ 1`, `.im`, `LFunction` elaborate to.

Tasks, in order:
(1) Textual scan of the 67-module closure (/tmp/oaimath/003/lean/closure_DRZB.txt; sources under /tmp/oaimath/013/repo/lean and
    /tmp/oaimath/013/ext/PrimeNumberTheoremAnd) — comment-stripped — for: `instance`, `attribute [instance`, `default_instance`,
    `macro`, `macro_rules`, `syntax`, `notation`, `infix`/`infixl`/`infixr`/`prefix`/`postfix`, `elab`, `unif_hint`, `@[simp]`-free
    is fine; and for soundness escapes: `axiom`, `sorry`, `admit`, `opaque`, `implemented_by`, `extern`, `unsafe`, `native_decide`,
    `ofReduceBool`, `decide := true`-style kernel bypasses, `set_option debug.skipKernelTC`. For every instance/notation hit: is it
    `local`/`scoped` (cannot leak) or global, and could it apply to any type in the statement (ℕ, ℝ, ℂ, ZMod q, DirichletCharacter ℂ q
    = MulChar (ZMod q) ℂ)? Save hits to D_work/scan.txt.
(2) Rebuild just enough to run Lean against the closure. Toolchain leanprover/lean4:v4.34.1 (NOT installed now — ~/.elan has 4.32.1
    and 4.33.0-rc1); Mathlib d13f23b checkout at /tmp/erdos0300/lean/mathlib4 (its .lake build was deleted — `lake exe cache get`);
    the 10-23 recipe and scripts are in /tmp/oaimath/013/lean-build/ (cacheget.sh, drive.py, lean_path.txt, statement_match.py) and
    the bundle README "Reproduce" section; patched PNT+ under /tmp/oaimath/013/ext. Compile ONLY the 67 closure modules (topological
    order = the closure file order) with plain `lean -o`, LEAN_NUM_THREADS ≤ 2, at most TWO lean processes at once, each under an RSS
    watchdog (copy /tmp/oaimath/191/bridge/rsscap.sh; `ulimit -v` breaks Lean's olean mmaps, do not use it for lean). GUARDS: before
    `cache get` or a toolchain install `df -h /` must show ≥ 30 GB free; before each lean launch `free -g` must show ≥ 20 GB available
    after ~8 GB for it. Keep build trees under /tmp/oaimath/003/lean/ (or reuse the erdos0300 mathlib checkout's .lake); log every step.
(3) THE BRIDGE (the deliverable): write `NoLSStatement.lean` that imports ONLY Mathlib and defines
      `def NoLandauSiegel : Prop := ∃ c : ℝ, 0 < c ∧ ∀ (q : ℕ) [NeZero q], 3 ≤ q → ∀ χ : DirichletCharacter ℂ q, χ.IsPrimitive →
        χ ≠ 1 → (∀ a : ZMod q, (χ a).im = 0) → ∀ β : ℝ, (0 < β ∧ β < 1 ∧ χ.LFunction (β : ℂ) = 0) → c ≤ (1 - β) * Real.log q`
    written by you FROM THE PAPER's Theorem 1 (state in the report how each clause maps: "primitive" = IsPrimitive, "nonprincipal"
    = χ ≠ 1, "real" = im = 0, "real zero β ∈ (0,1)", "conductor q" = modulus of a primitive χ, natural log). Compile it to an .olean
    BEFORE anything of OpenAI's is on the path. Then `Bridge.lean` importing NoLSStatement + OAI.NumberTheory.Jacobsthal.Siegel.
    DirichletRealZeroBound: `theorem bridge : NoLandauSiegel := OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound`
    + `#print axioms bridge`. Because NoLandauSiegel's body was elaborated in a Mathlib-only environment, no OpenAI declaration can
    have touched its meaning; the kernel then checks OpenAI's term against it. Also print `pp.all` of NoLandauSiegel's value from the
    Mathlib-only side and confirm every constant in it is Mathlib's (list them).
    Mutation controls (must be REJECTED, each in its own file, logs kept): e.g. (i) β < 1 replaced by β ≤ 2 (claims more zeros
    bounded — must fail to typecheck against the term); (ii) c ≤ … replaced by c ≤ (1-β) (drop the log — a stronger statement);
    (iii) drop `χ ≠ 1`. A mutant that typechecks means the bridge is not discriminating — say so loudly.
(4) Non-vacuity + meaning of LFunction (kernel-checked, Mathlib-only file): (a) exhibit q ≥ 3 and χ : DirichletCharacter ℂ q with
    IsPrimitive, χ ≠ 1, all values real (e.g. the quadratic character mod 3 or mod 4 — `quadraticChar`, `ZMod.χ₄` + ringHomComp to ℂ;
    any route). (b) `#check` the Mathlib theorems that pin `DirichletCharacter.LFunction` to the true L-function: equality with the
    Dirichlet series LSeries for re s > 1, and differentiability/entireness for χ ≠ 1 (find the exact names; quote their types). By
    uniqueness of analytic continuation these two make LFunction χ β the analytic continuation at β ∈ (0,1) — no junk value.
(5) Paper ↔ Lean map: for Lemma 2, Lemma 3, Corollary 4, Lemma 6, Lemma 7 and §6, name the Lean module(s)/theorem(s) that prove
    the corresponding statement, and say whether the Lean follows the PAPER's proof or a different one (e.g. is Lemma 3 proved by the
    nearest-point/face argument, or via Hilbert series / zero schemes / derivations?). Is the Lean's analytic input
    (HadamardSupport) a proof or an imported assumption? Also: what are the 39 Jacobsthal/Siegel files OUTSIDE the closure?
Leave the built .lake trees in place at the end (the main seat deletes them after banking) but record their paths and sizes.
Report: /tmp/oaimath/003/seats/D_report.md (verdict per task; exact file paths of every .lean/.log you made).
