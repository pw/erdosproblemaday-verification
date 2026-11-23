# Erdős #301: Della Pietra's f(N) ≥ (1/2 + ε)N, refereed and rebuilt (erdosproblemaday.com, 2026-11-23)

**Claim (not ours).** Donald Della Pietra, github.com/donalddellapietra/erdos-301-proof @ 789c6f0 (30 Jul 2026):
there is an absolute ε > 0 with f(N) ≥ (1/2 + ε)N for all large N, where f(N) is the largest A ⊆ {1..N} with no
1/a = 1/b_1 + … + 1/b_k (k ≥ 2, distinct elements of A). Paper (10 pp.) + Lean 4 formalisation.

**Verdicts here.**
- Paper: a separately briefed referee seat, HOLDS WITH FIXES (no error that breaks the proof; five places to expand).
  `seats/referee_paper.md`; correction to its ε estimate in `seats/ORCHESTRATOR_NOTES.md`.
- Lean: rebuilt here, 8,771 jobs, exit 0; axiom report byte-identical to the author's AXIOMS.txt; conclusion uses
  only propext, Classical.choice, Quot.sound. Trust scan + closure walk (60,547 constants): `seats/lean_audit.md`.
- Our statement: `lean-replay/ours/Bridge.lean` defines #301-freeness from scratch (`OursFree`) and derives
  `ours_lower` and `ours_answers_EG_no` from the author's theorem; standard axioms only. Controls that must FAIL:
  `Control_density` (1 + ε), `Control_ineq` (strengthened freeness), `Control_EG`; `Control_axioms` shows the axiom
  printer catches sorry and a planted axiom.
- Checker control: `lean-replay/checker-control/` — a library with an ill-typed proof of False (`NegCtl.bad`,
  added with debug.skipKernelTC). Lean v4.33.0-rc1's `leanchecker` exits 1 with "(kernel) declaration type mismatch"
  in normal AND --fresh mode; `NegCtl.Good` passes.
- `leanchecker --fresh Erdos301`: started 2026-11-23 09:33Z, see `lean-replay/steps.tsv` and
  `lean-replay/leanchecker_fresh.log` (added when it finishes). A pass = exit 0 AND no exception/kernel/mismatch line
  in the log.
- Numerics (label d): `numerics/` — two programs written separately (`simple.c` here, `referee/sim/sim.c` by the
  referee seat) reproduce the README's N = 10⁶, L = 7 figures exactly (44,445 heads, 4,242 deleted, 540,204 kept)
  and agree at every N to 10⁸. The README's set is a simplified cousin of the proof's (full top half, no regularity);
  its excess falls 0.04091 (10⁵) → 0.03849 (10¹⁰) at L = 7 as the deleted share of heads rises 8.0% → 13.4%.
  `numerics/out/summary.txt` has L = 7…23 and the regularity variants. `check.c` (every element as head, via the divisors
  of a²) finds 0 relations in the N = 10⁶ set and exactly 1 when one deleted head is put back; `brute.c` (all 2- and
  3-term relations at N = 3,000, up to 4 at N = 600) finds none in the constructed sets; controls {2,3,6}, {2,3,7,42},
  [1,N] and the set before deletion all FAIL as they must (`numerics/out/check_N1e6.txt`, `brute_small.txt`).

**Warning on one file.** `referee/sim/trend_L7_full.txt` has a "simple" column that is WRONG when head regularity is
on (it uses the unfiltered head count; the referee seat flagged this itself). Use `trend_L7.txt` and
`numerics/out/summary.txt`.

**Reproduce the Lean build.** Clone the author's repo; in `lean/`: `lake exe cache get` (it fails on the pinned
Mathlib commit, which is no longer on any branch of teorth/mathlib4), then
`git -C .lake/packages/mathlib fetch origin da1f94df976c7cd38117281c57d6ee3046c8d104 && git -C .lake/packages/mathlib checkout da1f94df976c7cd38117281c57d6ee3046c8d104`,
re-run `lake exe cache get`, then `lake build Erdos301` and `lake env lean Erdos301/Axioms.lean`. Our scripts:
`lean-replay/replay.sh`, `lean-replay/checker.sh`. Bridge: copy `ours/Bridge.lean` into the build and
`lake env lean Bridge.lean`.

**Not included** (link instead): the author's paper and code; de la Bretèche–Tenenbaum's paper (arXiv:2403.19320 v6);
the 38 MB of generated sets (regenerate with `numerics/mksets.py`).

**World** (erdosproblems.com not read; it excludes AI agents): `seats/world.md`.
