# Erdős #301 — divisor-block upper bounds: N. T. Nhan's 61487/77376 checked, and exact profiles pushed further

Problem: f(N) = max |A|, A ⊆ {1..N}, with no 1/a = 1/b_1 + … + 1/b_k (a, b_i distinct in A). f(N) ≥ N/2; conjecture f(N) = (1/2+o(1))N.

## Method (Della Pietra, github.com/donalddellapietra/erdos-301-proof, 30 Jul 2026)
n = m·d uniquely with d | M and v_p(m) ≡ 0 mod (v_p(M)+1) for p | M. A solution-free A meets block m·D(M) in a scaled
solution-free subset of D(M) ∩ [1, N/m]. With F_M(t) = largest solution-free subset of D(M) ∩ [1,t], h_M = count − F_M:
f(N) ≤ (1 − δ_M W_M + o(1))N, δ_M = Π (1−1/p)/(1−p^{−(e+1)}), W_M = Σ_{d: F_M does not step at d} 1/d.
Equivalently C_M = δ_M Σ_{d: F_M steps at d} 1/d (because δ_M σ(M)/M = 1).
Refinements used for lower bounds past the exact range (all disjoint unions of divisor sets):
D(pM) = D(M) ⊔ p·D(M) for p ∤ M  ⇒ h_{pM}(t) ≥ h_M(t) + h_M(t/p);   D(2^5 m) = D(2^4 m) ⊔ 32·D(m), m odd.

## Files
- `dfs/prof.c` (v2: split-point bound), `dfs/prof_v1.c` (v1), `dfs/prof_mut.c` (mutant control) — exact depth-first
  search, decreasing order, exact subset-sum bitset of the chosen reciprocals scaled by M. Outputs `dfs/p<M>_*.out`
  (per divisor: grow/jump, F, h, node count, the witness set for every grow).
- `profile/profile.py`, `profile2.py` (dumps), `profile3.py` (seeded from a previous run's cuts) — CP-SAT with lazy
  constraints; `profile/partial_<M>_<T>.json` = every cut (each a genuine equation, re-checked in Fractions) + witnesses.
- `profile/scip_recheck.py` — SCIP (pyscipopt) re-solves every CP-SAT "jump" (no larger free set) from the dumped cuts.
- `analysis/bound.py`, `analysis/final2.py` — certified lower bound on W (step function on the divisor grid, running
  max, h_M(t/p) evaluated at the largest divisor ≤ t/p), the bound chains, cross-checks, the reader's intervals.
- `analysis/reader_arith.py` — the submission's arithmetic in exact fractions.
- `controls/` — OEIS A390394 n ≤ 22 (DFS on {1..22} via M = lcm(1..22)), mutant, Della Pietra's 1680/2520/5040 constants.
- `referee/` — the hostile referee's report and its own solver.

## Reproduce
gcc -O2 -o prof dfs/prof.c && ./prof 5040 0          # full 5040 profile, ~11 min on one core
python3 profile/profile2.py 720720 300 4               # CP-SAT, dumps partial_720720_300.json
~/.venv/bin/python profile/scip_recheck.py profile/partial_720720_300.json
python3 analysis/final2.py

## Final numbers (analysis/final2_run_final.txt, 21 Nov 2026 ~11:40Z)
- Version A (every value confirmed a second way: the two programs agree, or SCIP re-solved CP-SAT's "no larger set" problem from
  the same cuts, or our search reproduces an independent published constant): best f(N) ≤ (743221/943488 + o(1))N ≈ 0.787738N
  (M = 1441440; confirmed through 55440:132, 720720:130, 10080:1008, 110880:112, 1441440:88, odd parts 315/3465 full, 45045:2145).
- Version B (also single-program values: 55440 to 168, 1441440 to 91, 45045 in full): 2599157/3302208 ≈ 0.787097.
- External matches: 5040 full = 15437/19344 (Della Pietra), 2520 = 839/1040, 1680 = 4865/5952 (Della Pietra), 10080 prefix to
  504 = 3481/4368 and to 1008 = 2233/2808 (Orakwue). Cuts: 27,061 distinct (30,669 saved), all genuine (analysis/check_cuts.py).
  SCIP: 99 jumps re-solved (57 where CP-SAT was the only program), 0 disagreements. Witness sets re-checked by final2: 285.
- Paths: the analysis scripts read and write ~/MathDyad/erdos301/ (the scratch layout this bundle copies); to rerun here,
  set B in final2.py to the bundle root.
