# #787, k = 6: a second route to n+(6) = 21 (so n_max(6) = 43), 27 November 2026

Claim: no 22 positive reals have answer 6 (every 7 of them contain a pair whose sum is in the set fails), so
n_max(6) <= 2*21 + 1 = 43 and, with the reader's 43- and 59-element examples, g(n) = 7 for 44 <= n <= 59.
Label (d). The SAT side is NOT proof-logged.

Inputs from the reader (skaya), repository tag v1.1.1, commit d2bb472:
data/k6_farkas_certs.jsonl.gz, SHA-256 b0f821b1b823df9275606bdfe6f5657636f5aa9cf028c34ac1da0ebed4bd4e82, 1,645,192 certificates.

Chain
1. check_certs.py (ours) certifies every certificate exactly in integers: check_certs.log (1,645,192 certified, 0 not; 165 s).
   Its controls: controls_certify.py / controls_certify.log (CONTROLS PASS). The reader's own verifier also passes: their_verifier.log.
   The certified certificates, renumbered to our triple ids, are cores_ourids.txt (40 MB, not committed; sha in cores_ourids.sha256).
2. Encoding (ours, written 25 Nov before the archive existed): sat_close.py base_clauses() + write_cnf.py order_atoms().
   Variables s(i,j,l) <=> x_i + x_j = x_l (i<j<l) over 22 increasing positive reals; AMO per pair; AMO per (a,l); ORDER2;
   order atoms (x_i + x_j > x_l, closed upward); edge e(i,j) -> OR_l s(i,j,l); every 7-subset of the 22 indices contains an edge;
   one blocking clause per certified certificate.
3. Split: the reader's 21 cases on the unique j with x_j + x_20 = x_21 (or none) and 4,010 (u_low, u_high) subcases
   (sat_tasks.py tasks_for_case); exhaustiveness of the subcases checked per case by SAT using only the always-true clauses
   (sat_tasks.py split_exhaustive): cases_hybrid.jsonl split_exhaustive = true for all 21.
4. Solving: sat_hybrid.py (incremental CaDiCaL 1.9.5 via pysat with a conflict budget; overflow to kissat on the same clauses).
   tasks_hybrid.jsonl: 3,926 subcases UNSAT (CaDiCaL 3,678, kissat 237, propagation 11); tasks_oa.jsonl: 84 earlier UNSAT
   on the same formula; 3,926 + 84 = 4,010. sat_hybrid.log ends "done, total 23434.6s". No SAT answer appeared, so the
   CEGAR step (exact Farkas certificate for any proposed pattern) never fired: extra cores 0.
5. Controls (controls_sat.py, controls_sat.log, CONTROLS_SAT PASS, 88 s; the s-part is taken from base_clauses() itself):
   C1 124 real 22-element positive sets entered as their exact sum patterns are SAT with every core (no core excludes a real
   configuration); mutation (core ids shifted by one) blocks 115 of 124. C2 a real set P+{100} with alpha = 7: the full
   encoding allowing 7 is SAT, allowing 6 is UNSAT. C3 the kissat path agrees on both.

Reproduce: python3 check_certs.py <archive>; python3 controls_certify.py; python3 sat_hybrid.py <budget> all; python3 controls_sat.py
(paths inside the scripts point to /home/exedev/MathDyad/subs-1126/787/check; adjust D).
