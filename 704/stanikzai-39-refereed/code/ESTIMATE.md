# #704 / vapywt — independent recomputation of α(J(13,5,3)) ≤ 33 (erdos seat, 2026-11-13)

Estimate written before spending CPU:
- Their MaxCliqueDyn total over 200 leaves ≈ 1,068 s; MoMC ≈ 1,777 s (records in their solvers/live/corroborate).
  So the problem is minutes-to-hours of CPU, not days.
- Our route (shares no code with theirs; a different tree built with the same technique, orbital branching, from a different root):
  (P1) triple count: a family of 5-subsets of [13] with pairwise intersections ≤ 2 has ≤ ⌊286/10⌋ = 28 members,
       so an independent set of size 34 contains two sets meeting in exactly 4;
  (P2) Sym(13) is transitive on such ordered pairs ⇒ WLOG v={0,1,2,3,4}, u={0,1,2,3,5} ∈ I;
  (P3) α ≤ 33 ⇔ ω(Ḡ[R]) ≤ 31, R = common non-neighbours of v,u in J (Ḡ = complement of J);
  (P4) orbital branching on Ḡ[R] with Sym{0..3}×Sym{4,5}×Sym{6..12} and its refinements, our own rule;
  (P5) leaves decided by (i) our own bitset branch-and-bound in C, (ii) cliquer 1.21. [CP-SAT was tried as the second leaf solver and abandoned: no leaf finished in 45 min on 8 workers. The first tree rule, max-degree, gave 17,552 leaves and was abandoned for the largest-orbit rule (105 leaves).] 
- Budget: C solver ≲ 1 core-hour total expected; CP-SAT capped 600 s/leaf, ≤ 10 workers at nice 19.
- Controls: same pipeline at size 33 must return SAT with a verified witness; gates J(10,5,3), J(11,5,3), J(12,5,3)
  against brute-force/independent values; solver negative/positive controls on planted cliques.
