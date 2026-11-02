# Seat C — Section 8 tables (snapshot taken by the host at 2026-11-02 ~10:20Z, while the seat's last runs were still going)

Reproduced (our code; two programs where noted):
- F(x) = 0 for x <= 11, 24 for 12 <= x <= 23, 216 at x = 24, with the paper's five moduli sets at 24:
  bf.c (plain enumeration of all 3,968,055,000 assignments on the sqrt(x)-smooth moduli, bf_x24.out) and the
  Python route B (Bpy_*), re-verified by verify_systems.py (verify_bf_x24.out: 216 distinct, 0 failing).
- Unpruned over ALL moduli in [2, x]: dfsA.c (A_unpruned_x2..x12.out) and routeB (B_unpruned_*, Bc_unpruned_x5..x13.out):
  0 for x <= 11, 24 at x = 12 and x = 13. "Near-unpruned" x = 16 (all moduli <= 16 except 13): 24 (Bc_near_x16.out).
- Checker controls: controls.out (classical system accepted; +3 mod 8, each single deletion, and {0 mod 2, 1 mod 2} rejected).
- k(x): kenc.py (CNF + kissat) k(12) = 5, k(24) = 6, k(30) = 10 (SAT at k, UNSAT at k+1; k_sat.log), and CP-SAT
  cpsat_witness.py: x = 30 k >= 11 INFEASIBLE (cpsat_ub30.out); witnesses k(36) >= 14, k(40) >= 15 (cpsat_w36/40.out).
  Paper's printed 18-class system with moduli <= 48 and the 14-class system on the divisors of 216 check (controls.out).
NOT reproduced at snapshot time: optimality of k(36) = 14, k(40) = 15, k(48) = 18 (upper-bound runs in progress; k_ub.log).
The seat's own REPORT, if it lands, supersedes this file.
