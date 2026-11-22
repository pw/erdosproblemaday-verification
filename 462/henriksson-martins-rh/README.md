# Erdős #462 — two RH-conditional answers to the composite reading, refereed (22 Nov 2026)

p(n) = least prime factor. #462 (Erdős–Graham 1980, p. 92): is the sum of p(n)/n over x ≤ n ≤ x + C√x(log x)² bounded
below for some C > 0 and all large x? Literal reading = all integers (Formal Conjectures `erdos_462`); composite reading
= primes excluded (Zhang, arXiv:2608.24930).

## Submissions
- **qkev6e — Adam Henriksson**, "A solution to the composite form of Erdős problem 462 under the Riemann hypothesis",
  Zenodo 24422158 (v3, 21 Nov 2026 15:59 UTC; v1 06:27 UTC). **Verdict: VERIFIED as an RH-conditional result.**
  Thm 1.1 (C = 384, x ≥ 9.6·10³⁷, ≥ (14/3)√x balanced products, weight ≥ 14/9, from Chirre–Hagen Thm 3), Thm 1.2
  (positive lower bound for every fixed C under RH; unconditional upper bound 20 + 2595840C).
- **pzkv8q — Pedro Martins** (duplicate row m5f5bt), "Least prime factors in short intervals under the Riemann
  Hypothesis", Zenodo 24431352 (22 Nov 2026 03:13 UTC). **Verdict: PARTIAL** (all three theorems hold under their
  hypotheses; the submission's "solved" does not, since nothing is unconditional). Thm 1.3 S_C ≥ min{C/54, C²/K}
  (RH); Thm 1.5 |S_C − 4C| ≤ K′√C (RH); Thm 1.6 S_C = 4C + o(1) under Hypothesis PC. One harmless slip: Prop 5.5
  Step 6 "(9/8)δ" needs ε ≤ 1/24 (constant 61 → ~74 for ε ≤ 1/8). Lean file: uncompiled, 19 `sorry`s.

## What is here
- `referee/henriksson_referee_report.md`, `referee/martins_referee_report.md` — the two hostile referee reports
  (separate Claude instances, told to refute), verbatim. `referee/henriksson_consts.py` recomputes Henriksson's
  constants in exact rationals; `referee/siebert_check.py` tests the Siebert bound numerically; `referee/martins_table1_rerun.py`
  re-runs Martins's Table 1.
- `lean-replay/` — our build of Henriksson's Lean project (Lean v4.33.1, Mathlib 0df444a = v4.33.1 release, cache):
  `build.log` (3,193 jobs, exit 0, no warnings), `audit.log` (105 declarations, each `[propext, Classical.choice,
  Quot.sound]`), `replay.log` (author's ReplayProofs.lean via Lean.Replay: 54,397 declarations, "Fresh kernel replay
  passed."), `leanchecker.log` (non-fresh, 25 project modules, exit 0), `MyAxioms.lean` + `myaxioms.log` (our own
  `#print axioms` and full types for the seven headline theorems; `Iff.rfl` checks that the input Props unfold to the
  published statements). Not run: `leanchecker --fresh`, Lean4Lean.
- `world/world_report.md` — the world seat's report: Zhang v1/v2, Mori (Zenodo 24210937, 14 Nov), lixiang90 (GitHub,
  20 Nov), version timeline, the four cited analytic inputs quoted from their sources, Erdős–Graham's printed wording,
  teorth row, and where it could not look. erdosproblems.com not read.
- `submission_*_frozen.json` — the submissions as received (contact details removed).

## Lead seat's own checks
Henriksson §2 (Thm 1.1) re-derived by hand: |B_I|, |B_J| ≤ N/24, |G| ≥ 7N/24, per-pair measure ≤ 2δN, count
7·512/768·N = 14N/3, window 3δx = 1536L²N = 384√x(log x)², weight ≥ 14/9. Lean logs grepped for error/sorry/
mismatch/kernel: none.

## Context (not a result)
On 20 Nov 2026 Levent Alpöge announced an AI-generated, Lean-only proof of the Generalized Riemann Hypothesis (Tao's
blog, 20 Nov: "an (enormous) Lean-only proof"); verification is under way. Until it is accepted, everything here is
conditional on RH.
