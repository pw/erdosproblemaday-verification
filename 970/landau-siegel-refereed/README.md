# OpenAI family 003, "Uniform exclusion of Landau–Siegel zeros" (dated 1 Oct 2026, 9 pp.): referee read + definitions audit

Erdős-problem-a-day erdos cron, 09:00Z seat of 2026-10-26 (Claude Opus 5.5). Requested by Patrick (Handoff ask 8f242353,
answered "Full read + definitions audit", 2026-10-25). Not an Erdős problem: it is filed under #970 because both of OpenAI's
#970 Lean theorems (and our #687 bridge) reach `OAI.Erdos970.WeightedTorusJets.dirichlet_real_zero_bound`, and route M of #431
does too (see verification/431/openai-ostmann-inverse-goldbach-refereed/deps/).

## Claim (OpenAI's, not ours)
Theorem 1: there is an absolute c > 0 such that every real zero β ∈ (0,1) of every primitive nonprincipal real Dirichlet
L-function of conductor q ≥ 3 satisfies (1 − β) log q ≥ c. Source pinned in `paper/SOURCE.txt` (openai/math @1581d4c; not
redistributed here).

## Verdicts
| seat | scope | verdict | file |
|---|---|---|---|
| R0 (main seat) | whole paper, own read, written before any report came back | HOLDS AS READ | seats/R0_main_seat_read.md |
| R1 (Opus 5.5) | whole paper, hostile | HOLDS AS READ; 3 exposition notes | seats/R1_report.md |
| C (Opus 5.5) | exact small-case computation of Lemmas 3, 6, 7 | CONSISTENT, 0 counterexamples; controls fail where they should | seats/C_report.md, compute/ |
| D (Opus 5.5) | Lean definitions audit, Mathlib-only statement bridge, mutants, non-vacuity, paper↔Lean map | HOLDS AS READ; the Lean proves Cor. 4 by a different zero estimate than §3 | seats/D_report.md, lean/ |
| W (Sonnet) | world: reception, third-party replays, citations | no reported gap anywhere; we were late (Banks 11 Oct, Kerr 15 Oct, Green 17 Oct, Tao 19 Oct; replays from 9 Oct) | seats/W_report.md, world/ |
| W (2nd pass) | fact-check of the page text | see seats/W_factcheck.md | |

## The chain
1. Paper read twice independently (R0, R1), every step of §§1–6. Both found the same sanity test unprompted (and C a third
   time): the divisibility step applies to primes whose Frobenius is one of the three conjugations used as variables
   {1, σ, στ}; for a fixed field that bounds their log-density by 3/4 + ε, which Chebotarev says is exactly the truth — the
   method is saturated by equidistribution and proves nothing false; only a bias to χ(p) = −1 (what a Siegel zero forces)
   breaks it.
2. Decorrelated computation (C): Δ built exactly in ℤ[√d,√2] (multimodular CRT, exact rank certification), 7 fields,
   N = 2, 3 (and 4 for d = −1), H = 1..8, two tie-breaks: Lemma 7 holds in 188/188 admissible cases, equality in 91.
   Controls: τ-class primes fail 84/93, p ≤ H fails 56/84, wrong-conjugate constructions fail; Lemma 3 certified for every
   (3.1)-box at N = 2, 3 (corner-box + monotonicity); a ℚ-dependent kernel loses rank (75 < 81) on a (3.1)-box.
3. Lean (D): toolchain v4.34.1 + Mathlib d13f23b (cache); the 67-module closure of `dirichlet_real_zero_bound` compiled from
   source (0 errors). `lean/bridge/SeatD003/NoLSStatement.lean` (imports Mathlib only) compiled BEFORE any OpenAI file was on
   the path; `Bridge.lean` has the kernel accept OpenAI's term against it, axioms [propext, Classical.choice, Quot.sound].
   Six mutants rejected (Type mismatch). Constant-provenance audit: statement uses only Mathlib/Init(/Batteries) constants
   (positive and negative controls). NonVacuity.lean: hypotheses satisfiable (real character mod 3), trivial character not
   primitive, LFunction = unique entire continuation of the L-series, and the "bare L-series" reading proved FALSE.
   `leanchecker --fresh` over the whole import closure: see "Fresh replay" below.
4. Paper ↔ Lean (D): Lemma 2, Lemma 6, Lemma 7, §6 follow the paper (same constants, H ≥ 86,713,344); Corollary 4 is proved
   by a multiplicity estimate (37 modules used only there); the nearest-point proof of Lemma 3 is not in the 105 files.
   Reilly (jmreilly1113) formalized Lemma 3 separately and rerouted the comparator through it (W).

## Fresh replay
`leanchecker --fresh SeatD003.Bridge` (replays every declaration of the bridge's whole import closure, Mathlib included, in a fresh kernel): exit 0, wall 7,238.8 s, maxrss 8,612,588 kB (`lean/logs/leanchecker_fresh.log`; GNU time prints `Command exited with non-zero status` on failure and leanchecker prints `leanchecker found a problem` — neither appears). Controls (`lean/lcctl/`): an olean proving False with the kernel off is rejected (`LcBad.leanchecker.log`), a good one passes, a missing module exits 1. Note: seat D's wrapper had a 7,200 s cap that would have killed the run 39 s before it finished; at 11:3xZ the main seat killed only the wrapper and put an RSS-only watchdog over the same PID (`lean/logs/lc_watch.sh`, `lc_watch.log`).

## Not done
The 199-page quasi-RH paper (out of scope). An independent kernel (nanoda/lean4lean) is not installed here; third parties
ran nanoda on the comparator copy (W). The paper's analytic constants were checked by hand only; computations are small (M ≤ 256).

## Layout
paper/ (SOURCE.txt) · seats/ (briefs, all reports) · compute/ (seat C scripts + outputs; compute/R1_numerics = seat R1's quick checks, which its report cites as R1_work/) · lean/ (seat D sources, logs, scan;
no .olean) · world/ (seat W notes and search logs; third-party PDFs, the Formal Conjectures clone, press pages and paper texts
were not copied — they stay in the scratch dir /tmp/oaimath/003/seats/W_work/ and are listed in world/NOT_COPIED.txt).
