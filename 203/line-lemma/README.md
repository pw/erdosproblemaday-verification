# Erdős #203 — the Quotient Lemma on lines: every period ≤ 65,520 excluded a second way; the five open pools closed

Companion to `verification/203/covering-forced-loss/` (12 Oct: Theorem A forced overlap, Theorem B block maxima,
Theorem C perfect powers; every period ≤ 65,520 excluded; pools 110880, 166320, 221760, 332640, 720720 left open).
Entry: `/day/203-the-quotient-lemma-lines-close-the-open-pools`.

## The claim
No #203 covering system (a finite set of primes p ≥ 5 with one coset C_p of L_p = {uk+vℓ ≡ 0 mod e_p} each, ∪C_p = ℤ²)
has period N for any N ≤ 65,520, nor for any divisor of 110880, 166320, 221760, 332640 or 720720 (17 periods above
65,520). PURE covering systems only; the perfect-power variant is a separate run (`results/pp_*.jsonl`, see the entry).

## The proof (two layers)
1. **Theorem D (elementary, no solver)** — `scripts/LEMMA.md` § Theorem D, `scripts/fivesevencut.py`: in direction (1,1)
   the prime 5 covers whole lines (one class mod 4) and 7 has intensity 1/2 on one class mod 3; on the 30 of every 60 line
   classes neither touches, the average intensity of the other primes is at most the closed-form sum B(pool); B < 1 for
   every pool in the claim (≤ 3965/4752 = 0.8344 for the 26 periods ≤ 65,520 with density ≥ 1; 720720: 11255/12012 = 0.9370).
   Found by the hostile referee (`referee/REPORT.md` finding 5), recomputed by us from the pool files; the two programs
   share no code. Its output for all 33 pools is `results/fivesevencut.out`.
2. **Exact solver values** — `scripts/linelemma.py`: V = max over coset classes of min over line classes, per direction,
   as a CP-SAT max–min program (a proven BestObjectiveBound < 1 excludes; OPTIMAL values are exact) and as a feasibility
   program (every line ≥ 1 hard; INFEASIBLE from CP-SAT or HiGHS excludes). One JSON line per (period, direction) with
   E, Λ, M, status, V, bound, witness and its exact re-count: `results/ll_<N>.jsonl` (+ `ll_<N>_rerun.jsonl` for
   directions rerun at 900 s), `results/feas_<N>.jsonl` (+ `feas_<N>_undecided.jsonl`). `results/TABLE.md` is generated
   from these by `scripts/table.py`; the numbers on the page come from it, not from memory.

## What the Quotient Lemma is
For a subgroup Λ ≤ ℤ² and G = ℤ²/Λ, a coset of L_p meets a cell of G either not at all or in a coset of L_p ∩ Λ, hence
with density w_p = [G : S_p]/e_p (S_p = image of L_p), and the cells it meets form a coset of S_p; so a covering forces
every cell to receive intensity Σ w_p ≥ 1. Lines: Λ = ℤ(a,b); i_p = gcd(a·u_p + b·v_p, e_p) = [⟨2,3⟩ : ⟨2^a 3^b⟩],
w_p = i_p/e_p = 1/ord_p(2^a 3^b); C_p meets the lines τ ≡ t_p (mod i_p) only. Coarsening to a modulus M: i_p ↦ gcd(i_p,M),
w_p ↦ gcd(i_p,M)/e_p (still necessary; exact iff lcm i_p | M). The lemma itself is the classical restriction of a coset
cover to the cosets of a subgroup (Neumann 1954; Tomkinson; Z.-W. Sun, arXiv:math/0501451); what is ours is the weighted
line condition over the whole pool, its two integer-program forms, Theorem D (with the referee), and the exclusions (as far as we and the referee found, the first for the five
open pools). Antecedents on the thread: AnimishSharma's ℓ = 0 remark (one line, unweighted); veljjanoski's shear/strip family.

## Scope of the solver runs (exactly what ran)
- 26 periods ≤ 65,520 with density ≥ 1 (the others fail the density condition): 16 directions each, CP-SAT max–min at a
  60 s cap (5040–30240 at 300 s in the first batch). Directions left undecided by that cap are being decided by a
  feasibility run (CP-SAT 300 s + HiGHS 300 s, `feas_<N>_undecided.jsonl`) and by a 900 s max–min rerun
  (`ll_<N>_rerun.jsonl`); the feasibility program (CP-SAT 120 s + HiGHS 120 s) is also being run on every direction of
  every period as the second instrument (`feas_<N>.jsonl`). `TABLE.md` (regenerated at bundling) says exactly which
  period × direction pairs each run had reached and refuted at the time of the bundle; its last column counts the
  feasibility refutations per solver. NOT every direction excludes every period (55440 has three directions with
  re-counted witnesses ≥ 1 — (1,0), (0,1), (2,3) — and 65520 one, (2,−3)); direction (1,1) excludes every period (exact
  value at 22 of the 26, a proven bound at 27720, 41580, 55440, 65520).
- The five open pools: direction (1,1) at the exact modulus (720720: coarsened to 55440 → effective M = 27720, after the
  exact M = 360360 attempt returned UNKNOWN in 180 s) — CP-SAT bounds < 1 (`ll_<N>.jsonl`; none of the five optima
  closed); the feasibility program (`feas_<N>.jsonl`: at bundling time 166320 CP-SAT INFEASIBLE 24 s + HiGHS infeasible;
  221760 CP-SAT INFEASIBLE 28 s, HiGHS at its time limit; 332640 / 720720 / 110880 as recorded there, or pending — the
  entry's pending sentence says which); HiGHS max–min on 110880 and 166320 (`milp_<N>.jsonl`: 110880 dual bound 0.9165
  < 1; 166320's HiGHS bound did NOT get below 1 in 1500 s — a failure of the second solver on that form, recorded); plus
  the referee's M = 60 certificates (`referee/scratch/coarse_run.out`, `bnb60.out`, `indep_milp60.out`) and Theorem D.
- `ll_110880.jsonl` = three directions at a 300 s cap ((1,0), (0,1) feasible; (1,1) bound 0.8086); `ll_720720_exact_attempt.jsonl`
  = the UNKNOWN exact-modulus run.
- Brute force (`--brute`) ran only on the controls and, in `torus.py --selftest`, on the first seven primes of the 720 pool
  at T = 12: every published row has ∏ i_p above the 3·10⁶ limit. HiGHS max–min receipts: `milp_720.jsonl` (three
  directions, agreeing) and `milp_5040.jsonl` (= `run_5040.jsonl`: 15 of 16 directions to optimality agreeing, (2,3) agreeing
  at its time limit).
- Coarse torus (`scripts/torus.py`), (ℤ/60)² with all 99 primes of 720720: `results/torus_720720_T60_feas.jsonl` UNKNOWN
  after 1500 s (max–min form: best 0.3549, bound 1.0052 after 600 s). Theorem D shows the instance is infeasible; the
  solver did not. Recorded as the stronger instrument that did not decide.
- `results/S8.{txt,log}`: the eight-prime block maximum (S7 + 37) the previous entry queued — still running at bundling
  time (single core, nice 19, ~5 h from 09:11Z); its result is for the previous entry's Theorem B, not for this one, and is
  reported there when it lands.

Pools: `pools/pool_<N>.json` (the named ones are the 12 Oct bundle's; 7920, 15840, 18480, 23760, 31680, 35280, 36960,
39600, 41580, 46800, 47520, 51480, 63360 regenerated by the same `pool2.py` with the completeness certificate
∏ p^{v_p} = gcd(2^N−1, 3^N−1); log `logs/pool2_scan.log`). The referee re-derived all 33 pools from scratch (orders,
characters against an explicit generator, completeness by division): 0 errors.

## Controls (`results/controls.log`, `results/selftest_torus.log`)
- Classical covering 0(2) 0(3) 1(4) 3(8) 7(12) 23(24) as full-weight classes ⇒ V = 1 (CP-SAT, brute force, HiGHS agree);
  {2,3,4,8} leaves a point bare ⇒ V = 0; shifting the constant part by 1/7 shifts V by exactly 1/7.
- The four cosets of L_5 entered as four 'primes' ⇒ V = 1 in all 17 directions (fractional weights and 1 < i < e are
  exercised); plus the six cosets of L_7 ⇒ V = 2; dropping one L_7 coset in direction (0,1) ⇒ exactly 11/6.
- Torus: lattice-image claim by enumeration (T = 10, 12), synthetic cover/non-cover, brute force = CP-SAT on 7 primes at
  T = 12, torus ≤ line projection.
- Every witness a solver returns is re-counted exactly (`recount_ok`: = at OPTIMAL, ≥ on time-limited runs — a free z
  can sit below the true minimum of a non-optimal solution).
- The referee's independent checks: 448 direct enumerations of the line formulas and the coarsening rule; torus image at
  T ∈ {8, 9, 15, 20, 24, 36}; a 2-D brute force on (ℤ/60)² with real primes against CP-SAT (31 instances, 0 mismatches);
  its own exhaustive enumerator on 5040 (0,1) = 529/630, 7920 (1,1) = 4459/7920, 7920 (1,−3) = 123/176 (all match);
  its own branch-and-bound refuting the five open pools at M = 60.

## Second seats
`referee/REPORT.md` — hostile Opus seat with tools (brief `scripts/REFEREE_BRIEF.md`): HOLDS WITH FIXES; every FIX applied
(the "every direction" claim, controls, re-count test, overstated checks, scope, attribution, table); its finding 5 is
Theorem D. `referee/consistency/` — the blind consistency read of the page before deploy (Opus, cold): FIX-FIRST with 30 findings
(every number on the page matched the files; the card and summary still carried the sentence the referee had ruled
false; several 'what ran' claims outran the files; the 'constant part diverges' remark was unproven; the solver bounds are
not uniformly sharper than Theorem D) — all applied before deploy; its scratch scripts are alongside.

## What this does not say
Nothing about whether an m exists. For a fixed direction the constant part (primes for which 2^a3^b generates ⟨2,3⟩)
diverges with the pool, so no single direction excludes every N; the exact covering problem is Λ = ∩ L_p. Next: the pool
of lcm(1..17) = 12252240 (uncomputed), and whether a 5–7-type cut keeps B < 1 for every period.
