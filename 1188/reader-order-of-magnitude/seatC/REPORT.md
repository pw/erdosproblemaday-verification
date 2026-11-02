# Referee seat C — Erdős #1188, submission 8gfcew, Section 8 (Computations)
(Opus seat, 2026-11-02 ~09:03–11:05Z. Saved by the host from the seat's final message; harness blocked .md writes.
Code/logs referee/C/scratch/; rendered pp. 28, 31, 32 in referee/C/pages/. All jobs finished or killed by PID at 11:00Z.)

VERDICT: HOLDS WITH NOTES. Everything recomputed matches the paper digit for digit: Table 1 (every cell), §8.1 structure
(24 = orbit of (1) under z → ±z + b; 216 = 24/48/48/48/48 over the five sets; 3,968,055,000 assignments at x = 24), Table 6
(|S_x|, x/log x, and the k values settled), Table 7, both printed example systems, Tables 2 and 3. Nothing wrong in scope.

N1 (exposition) §8.6 p.31 "for 30 ≤ x ≤ 48 the solver proved optimality" — Table 6 has only x = 30, 36, 40, 48; S_x also
   changes at 32 and 45 with no k value; should read "at the tabulated x".
N2 (slip, not load-bearing) k(x) upper bounds for 30 ≤ x ≤ 48 rest on CP-SAT "optimal" (no checkable certificate).
   Reproduced: k(30) ≤ 10 with two solvers/encodings (kissat UNSAT k≥11 637.6 s; CP-SAT infeasible 29.8 s / 9.8 s);
   k(36) ≤ 14 with CP-SAT only (own model, own symmetry breaking): `cpsat_witness.py --x 36 --k 15 --workers 2 --time 1750
   --sym --sym2` → "M [...36] k>= 15 status INFEASIBLE wall 601.2s" (cpsat_ub_sym2.out). Control on the same flags: x = 30
   --k 11 infeasible (9.8 s, agrees with kissat on a different encoding); every known witness still found with --sym2 on
   (k = 6 @24, 10 @30, 14 @36, 15 @40, 18 @48). --sym2 validity: z → uz + b (u unit mod L) preserves moduli, covering,
   minimality ⇒ largest-modulus class residue 0, second-largest residue 0 or a proper divisor of n. Translation-only model:
   UNKNOWN at 1700 s. k(40) ≤ 15 and k(48) ≤ 18 NOT reproduced (CP-SAT k≥16 @40 killed 11:00Z; k≥19 @48 never started).
   No proof uses Table 6 (Thm 1.7 asymptotic).
N3 (note) for x ≥ 13 Table 1 rests on Cor 1.4; paper's own unrestricted test reaches x = 12. Seat proved the needed lemma
   itself (Lemma W, = Thm 1.3/Cor 1.4); unrestricted search to x = 13, near-unrestricted (drop primes > x/2) to x = 16;
   pruned and unpruned agree wherever both ran.
N4 (definitions) [2,x] vs page's [1,x] with 1 < n₁ agree; allowing modulus 1 would add exactly 1 to each F(x).

Table 1: x = 2..11 → 0 (all moduli, routes A+B, Python and C); 12 → 24 (all moduli A+B; hand count 2×2×3! = 24; brute);
13 → 24 (all moduli, route B, 5,907,103 nodes, 383.5 s); 14, 15, 16 → 24 (all moduli except 13; 16: 229,266,410 nodes,
1096.7 s); 17..23 → 24 (3-smooth by Lemma W, four implementations); 24 → 216 (3-smooth; brute force 3,968,055,000
assignments, 20,697,840 coverings, 216 minimal, 312 s; 24 with 5 classes + 192 with 6; three dumped lists identical; all pass
both minimality tests).
Table 6: |S_x| 7/10/17/19/20/22 and x/log x match. k(12) = 5, k(24) = 6, k(30) = 10 reproduced; k(36) = 14 reproduced
(CP-SAT only); k(40) ≥ 15 and k(48) ≥ 18 by verified witnesses (x=30: 1/2 2/4 3/5 0/8 2/10 4/12 6/15 4/20 20/24 0/30;
x=36: 0/3 3/4 0/5 2/6 4/8 7/9 4/10 5/12 1/15 13/18 2/20 16/24 28/30 1/36; x=40: 0/3 2/4 2/5 2/6 3/8 1/9 1/10 1/12 8/15
16/18 5/20 7/24 29/30 4/36 15/40; x=48: paper's system + a second 18-class CP-SAT system).
Table 2 (sieve to 10^8): Λ/x 0.2825 0.4022 0.4398 0.4538 0.4617 (P = 97, 997, 9973, 99991, 999983); |S_x|/x 0.4330 0.3715
0.3582 0.3443 0.3327; Υ/(x log x) 0.3500 0.3180 0.3185 0.3135 0.3114. Table 3: |U_x| 299, 1,742, 12,495, 91,157, 714,810;
normalised columns match; smallest balanced integer 30. Table 7: L = 36 → 7, 216 → 14, 1296 → 23 (≥ +1 infeasible; witnesses
use every divisor except 1 and 2).
Controls: checker (classical accepted; +3 mod 8 rejected; each single deletion rejected 5/5; {0 mod 2, 1 mod 2} rejected);
private-point ⇔ subfamily minimality agreed 3000/3000 random coverings; SAT encoder forced (1) SAT, (1)+3 mod 8 UNSAT,
(1) − 7 mod 12 UNSAT, paper's 18-class SAT (as printed and translated by −33).
Implementations: Route A dfsA.c (modulus-by-modulus bitset DFS), Route B routeB.py + routeB.c (least uncovered point,
canonical branching, identical node counts), Route C bf.c (plain enumeration).
Not checked by this seat: Tables 4, 5, §8.2, §8.5 certificates, §8.7 (seats A/B did those).
