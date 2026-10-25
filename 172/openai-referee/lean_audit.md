# Third-party Lean 4 formalization of the #172 theorem — audit (2026-10-11, erdos tick)

**Repo:** github.com/cadamcat/hindman-sums-products-lean4 — author Yao Xu (@cadamcat); created 2026-10-07T22:52Z,
tag `v1.0.0` (tree `1d77b968…`), HEAD at audit time `3064cac5f9133a968482886ab1c7a1d69c16207f`
(2026-10-11 01:37 +0200, "Derive Formal Conjectures' Erdős 172 statement"). Description: "A Lean 4 formalization of
Hindman's finite sums and products conjecture, following OpenAI's proof". AUTHORS.md: planned/dispatched/reviewed by
the author; written with Claude Opus 5.5 (Claude Code) and GPT-6 Luna / GPT-6.1 Sol (Codex); "all proofs are verified
by the Lean 4 kernel".

**Size:** 84 `.lean` files, 5,993,300 bytes of Lean in `HindmanSumsProducts/` (not counting dependencies).

**Statement** (`HindmanSumsProducts/Main.lean`, identical text in `Challenge.lean`, which is Mathlib-only):
```lean
theorem hindman_finite_sums_products (r : ℕ) (χ : ℕ → Fin r) (m : ℕ) :
    ∃ (A : Finset ℕ) (c : Fin r), A.card = m ∧ (∀ a ∈ A, 0 < a) ∧
      ∀ B ⊆ A, B.Nonempty → χ (∑ b ∈ B, b) = c ∧ χ (∏ b ∈ B, b) = c
```
This is exactly Hindman's finite conjecture (Theorem 1.1 of the paper WITHOUT the separation clause (1.1) and without
Corollary 1.2). `audit/Erdos172.lean` (HEAD commit) derives from it, verbatim, the right-hand side of Formal
Conjectures' `Erdos172.erdos_172` (commit `9d259649…`: `∀ n color m, ∃ A, A.card ≥ m ∧ ∃ c, ∀ S : Finset A, S.Nonempty →
color (∑ x ∈ S, x) = c ∧ color (∏ x ∈ S, x) = c`) — i.e. the statement erdosproblems.com/172 and our /problem/172 page
show. Under the pairwise reading of "sums and products of distinct elements" (our August report's Φ(A)) the theorem is
stronger still, since pairwise sums/products are 2-subset sums/products.

**Open proofs / axioms in source:** `grep -rn '\bsorry\b\|^\s*axiom '` over the project's `.lean` files finds exactly ONE
hit — `Challenge.lean:21: sorry`, the Comparator challenge placeholder by design (the solution module proves the same
name). `HindmanSumsProducts/Arithmetic/RoughCoprimality/Axioms.lean` contains only `#print axioms` commands (no axioms).
No `native_decide`, `implemented_by`, or `@[extern]`.

**What is formalized where (per `docs/mathematics.md` + `THIRD_PARTY.md`):**
- §2 deduction + chain selection: `Framework.lean` (`main_of_principles`), `ChainSelection/`.
- §3 arithmetic (master scales, rough coprimality, sampling, product law, linear forms): `Arithmetic/` (own).
- §4 correlation (mask removal, additive elimination, correlation test): `Correlation/` (own).
- §5 Prediction Principle: `Prediction/` (own), with TWO deliberate substitutions: Tao–Ziegler concatenation → Kravitz–Kuca–Leng
  subgroup box-norm concatenation (arXiv:2407.08636 §6, proved in `Concatenation.lean`); GTZ inverse theorem → OpenAI's
  cyclic inverse theorem `OAI.Erdos3.exists_cyclicNativeInverse_positive` (from openai/math, family 159), transferred in
  `InverseBridge/`. So the formal proof of the Prediction half does NOT certify the paper's §5 text as written; it
  certifies the Principle by a different route.
- §6–§8 Alignment Principle: NOT re-proved here — imported unchanged from OpenAI's own library:
  `OAI.SourceMenuLiteral.charted_finite_menu_alignment` (openai/math `lean/OAI/Combinatorics/SumProduct/Alignment/
  MenuLiteral01.lean:130`, commit `adc7f124`; 259 files in that directory + `OAI/Geometry/NilpotentCharts`), via
  `OAI.raw_alignment_reference`. We sparse-checked those OpenAI subtrees (1,929 files, 28.7 MB): ZERO `sorry`/`axiom`
  hits. OpenAI's CONTENTS.md lists family 164 with no Lean link and its `lean/formalization.yaml` does not list the
  Hindman paper — i.e. OpenAI formalized the Alignment half but not the whole theorem; the third party closed the gap.
- Brun–Titchmarsh: `OAI.NumberTheory.Jacobsthal.Sieve.PrimeFibreBrunBound`; PNT in APs: PrimeNumberTheoremAnd (Wiener).

**Author's verification claim** (`docs/verification.md`): on 7–8 Oct 2026 a fresh clone of v1.0.0 on a 32-core GCP VM:
`lake build` exit 0 (11,472 jobs, 34 min, no sorry); `scripts/verify.sh` exit 0 — `#print axioms` gives exactly
`propext, Classical.choice, Quot.sound`; `lake env leanchecker --fresh HindmanSumsProducts.Main` exit 0 (30 min kernel
replay of the main module and everything it imports, including cached dependency artifacts); Comparator (leanprover/
comparator `ca04cfc`) statement match exit 0. On 10 Oct a second machine repeated it with `enable_nanoda` — the
independent Rust type checker nanoda also accepted the export, and rejected a sorryAx export and an altered-numeral
export as controls. Caveats they state themselves: `lake exe cache get` means Mathlib was NOT rebuilt from source
(leanchecker/nanoda re-check the declarations anyway); Comparator ran with its development stand-in for the sandbox.

**Dependency patching:** `scripts/apply-oai-patches.sh` applies OpenAI's `*-lean4341.patch` files to 23 pinned packages
(Lean 4.34.1 compatibility). A patch cannot smuggle a false theorem past the kernel; it could only add an axiom — which
`#print axioms` on the final theorem would show. Mathlib pinned `d13f23b7…`, openai/math pinned `adc7f124…`.

**Our independent replay (decorrelated instrument):** launched 2026-10-11 06:45Z on exe.dev (16 cores, box at load ~24
from the #112 SAT sweep), `nice -n 19`, `LEAN_NUM_THREADS=4`, `lake build -j 4`, scrubbed environment and scratch
HOME (`/tmp/oai-math/lean-build/run.sh`, log `build.log`, per-step `steps.tsv`); steps: clone HEAD → elan 4.34.1 →
`lake update` → OpenAI patches → `cache get` → `lake build` → `scripts/verify.sh` (prints `#print axioms` under
`--trust=0`) → `audit/NonVacuity.lean`. Result goes in `replay/` when it lands (expected hours; the next tick picks it up).
Until then the kernel-level claim is the AUTHOR'S, reproduced by us only at the source level (no sorry, standard
axioms declared, statement fidelity read by eye and derived to the FC statement in Lean).
