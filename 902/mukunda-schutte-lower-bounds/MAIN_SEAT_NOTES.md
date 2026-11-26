# Main seat (Claude Opus 5.5, erdos cron 2026-11-26 ~09:15–09:30Z): hand read of §§2, 3 (Thm 1.2), 6, 7, 8
Read from paper.txt (pdftotext of the tagged PDF); no code. Each item: what was re-derived, and the result.
- Lemmas 2.2, 2.3, (F1)–(F3): (F1) = Lemma 2.2 at n = 4 (nu_3 >= 5); (F2), (F3) from (2): in-degree of y in T[D(P)] = |D(P ∪ {y})| >= 5,
  in-degree of a in T[N^-(v)] = |D({a,v})| >= 11. OK.
- Thm 1.2: Case 1 is Lemma 3.1 with s = n-2, m = 2n+3, h = n+1, k = n-1 (LHS >= (n+1)C(2n+3,n-1), RHS (N-n+2)C(n+2,3)); Case 2 is (3) with j = 2
  (N+1 >= 2^(n-2)(2n+5)); dichotomy from Lemma 2.3 (|R| >= 2(n+1)+1). OK.
- Lemma 6.1: 45 triples through r, 225 incidences; 5 in-neighbours in R give C(4,2) = 6 each; others beaten by >= 5 of R, so <= C(5,2) = 10 each;
  P never dominates (R beats P). d^-(r) >= 24.5. OK.
- Lemma 6.2: C(23,2) = 23·11 forces T[A] 11-regular, all {a,v} tight; 11(N-24) <= 23(N-38) gives 12N >= 610. OK.
- Lemma 6.3: sum f_x = 12 (C(24,2) = 264 + 12); (a) a in L beats Z_v \ {a}; (b) 12 >= q(l-11) + C(q,2) + (24-l-q) <=> (q-1)(l-12) + C(q,2) <= 0,
  so q <= 1, |Z_v| <= 2, C(|Z|,2) <= 2|Z| gives |Z| <= 5. OK.
- Thm 6.4: no in-degree 23 below 51; C(N,2) >= 24N gives N >= 49; sum(d^- - 24) = N(N-49)/2 = 0 or 25; contradicts |Z| <= 5. OK.
- §7: (6) D(U) for U ⊆ R (P beaten by R); (I1) 25 - j_r - 7 = 18 - j_r; (I2) 198 - J and 8 - J; (I3) 5·4 = 20, c <= 4; (*) 195 <= 200 + 10 j_r - sum lambda;
  lambda(5..9) = 0,4,7,9,10. Structure when J <= 2: q = 7 forces J >= 4, q = 8 forces J >= 3; triple count 110 + 20(38-m9-n6) + 10 n6 >= 825;
  cases m9 = 0, >= 2 excluded; m9 = 1, n6 <= 2. (R1) 3c + 4k + 3m - 45 (contributions 3/4/3, y* none); (R2) 10 + 20j - 8beta - 20gamma using
  sum k = 5 alpha, sum m = 4 beta; (R3) s ≡ 3 - c - m (mod 4), c + m <= 6, so s >= 3-c-m and >= 7-c-m when c+m >= 4; rounding lemma
  5j >= beta + 5gamma + N4. Conclusion: no 6-vertex, q_{y*} = 13 - J <= 11 so J = 2, Q_{y*} = R; s(u,v) = 3 - c, k = 12 - c, |D({u,v})| = 12 on V0;
  sum_v |D({s,v})| = 120 + 5 j_s; j_s = 2 gives 120 != 130; j = 1,1 gives |D({s1,s2})| = 125 - 108 = 17, s(s1,s2) = 23 - c >= 19 > 15 = ½·30. OK.
- Cor 7.2: in-degree 23: 27·11 = 297 <= 299 - sum_A e, so J({a,v}) <= 2, contra Thm 7.1. In-degree 24: Gram matrix of the 50 sets D_z ⊆ A
  (|A| = 24), G_zz' = |D({v,z,z'})| >= 5; M = G - 5J ⪯ G has >= 26 non-positive eigenvalues; sum h_z = 1176 - 550 - sum_A d^- <= 28 - W;
  a tight row of M has off-diagonal sum 8 - J <= 5 < 6, so the tight block is positive definite, so at most 24 tight, so >= 26 non-tight,
  so W <= 2; a tight {a,v} from Lemma 6.3 then has J <= W <= 2, contra Thm 7.1. Regular; J = 0 excluded, so every pair >= 12; 51·C(25,2) = 12·C(51,2). OK.
- §8: (M1) inclusion–exclusion 48 - 72 + (36 - sigma) - k; (M2) T[N^+(w)] 12-regular on 25, 1650/650 per w, 84150/33150; (M3) 51·... = C(51,2)·C(12,3) = 280500;
  (M4) double count of (Y,W) with W => Y; C(k,3) - C(L-k,3) = (u^3 + (3a^2-1)u)/3 checked by expanding f(x) = x^3 - x; the sign of
  u^3 - u/4 needs u >= -1/2, i.e. k >= 5 (used); 7650·25 + 82875 + p = 280500 gives p = 6375 > 2762.5. OK.
Not read by the main seat: §§4, 5, 9 (referee B: §§3–6; referee A: §9 certificates).
