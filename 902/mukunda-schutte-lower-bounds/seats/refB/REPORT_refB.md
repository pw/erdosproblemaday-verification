# Referee B (Opus 5.5 seat), Erdős #902 Mukunda schutte-paper-v1 (1eed1fd), §§3–6 + §10 claims — 2026-11-26 ~09:40Z
erdosproblems.com not read. Their verify_proof.py read only after own code.
VERDICTS
- Lemma 3.1 (p.4) VERIFIED: hand + brute force on QR7, QR19, QR67, N70 (all A,|A|<=n-1, all k; 429,440 identity instances, 0 failures); QR331 orbit reps (271,440 checks). Mutations (h+1; nu_k+1) violated 115,039 / 100,368 times on QR67 (checker can go red).
- Thm 1.2 VERIFIED (n>=5 two-case proof; Lambda(5)=858/7, Lambda(4)=165/4, cubic identity =30 at n=5, Lambda>P for 5..3000; n=4 bound 51 = Thm 6.4).
- Thm 1.3 / c* VERIFIED: Lemma 4.3 limit step rigorous (n0 depends only on (i,eps)); c* = 0.769503219150489432699065268309823134676652788 by closed form+Newton, mpmath quadrature+bisection (agree 3e-40), asymptotic series (2e-60). a2..a6 match.
- Thm 1.4 / Lemma 4.5 / Table 1 VERIFIED: own exact-integer recursion -> 7,19,49,121,281,665,1485,3388,7398,16569,35655 (n=2..12); every N in 300 below each threshold ruled out; L_s(N) <= nu_s(T) on QR7,QR19,QR67,N70,QR331; mutated recursion violated (can go red).
- Lemma 5.1 VERIFIED (3000 random bipartite tournaments, LP game value, 0 violations; v^2 control fails 976x).
- Thm 1.5 VERIFIED WITH FIXES — FALSE AS LITERALLY STATED: |A|=n,|B|=1 with b beating A has S_{n,n} on n+1 vertices (n=2: 3<12); |A|=|B|=1 vacuous; proof p.7 "extend it to an n-set" needs both sides >= n. Fix: require |A|,|B| >= n. Then correct. Brute force: no S_{2,2} with |A|+|B|<=11 and both sides >=2 (2,959,499 families); 6+6 example of Remark 5.2 has S_{2,2}, v=1/2. Thm 1.5 should say equality for n=1,2.
- §6 (Lemmas 6.1–6.3, Thm 6.4 f(4)>=51) VERIFIED (needs N>=3 in statement).
- Prop 10.1 VERIFIED WITH FIXES (v>=t; t=1 separately); Lemma 10.2 VERIFIED; 70-vertex S4 tournament VERIFIED (QR67 + 3 vertices, nu3=5).
- Remark 4.4 "a_j - 2a_{j-1} decreases to 1/2": not proved (limit 1/2 easy; monotonicity numerical only, j=2..~130).
- verify_proof.py reproduces verify_proof.out exactly (timings aside, Failures: 0); needs mpmath (README omits it). It does not check Lemma 4.3's induction, §5, §10; V2 never exercises Lemma 6.1 (0 tight pairs).
- Novelty of Thm 1.5 vs Borowiecki–Grytczuk–Hałuszczak–Tuza 2003: NOT CHECKED (paywalled; abstract gives no bounds).
MUST-FIX: S_{n,n} definition needs |A|,|B| >= n.
SHOULD-FIX: S_n defined only for N>=n; Thm 6.4/1.1 need N>=3; Thm 1.2 proof should cite Thm 6.4 for n=4 (then no dependence on §§7–8); Lemma 4.1 strictly decreasing needs b>0; Remark 4.4 wording; Prop 10.1 v>=t; §10 sentence misapplies Prop 10.1 (conclusion true: explicit covering on F_2^n x {0,1} with 2^{n+1}-2 lifted hyperplanes); README omits mpmath; ATTRIBUTION: proof/ERDOS902_PROOF.md credits f(4)>=48 to Reid–McRae–Hedetniemi–Hedetniemi 2004 and f(4)>=49 to J. Wilder, but the paper cites [8] only generically and calls Thm 1.1 "the next small case beyond the classical one".
Scripts/logs: this directory (check_lemma31.py, cstar.py, recursion.py, check_qr331_and_recursion_soundness.py, check_bip*.py, check_thm12_and_chain.py, check_n70_structure.py, verify_proof.rerun*.out).
