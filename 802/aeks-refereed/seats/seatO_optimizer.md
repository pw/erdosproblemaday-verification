# Seat O — §2 (the extremal weight, random multipliers, cross-mass bound) + §6 (independent-set induction, Theorem 1.1)
Read /tmp/oaimath/184/seats/COMMON.md first. Report: /tmp/oaimath/184/seats/O_report.md. Work dir: /tmp/oaimath/184/seats/O_work/.
1. Lemma 2.1 and identity (2.2): re-derive. Existence/positivity of maximizers; note F_G is NOT concave (M_G indefinite) — does anything later assume
   uniqueness or concavity? Is "w_v ≤ 1" correctly derived?
2. Lemma 2.2 (random multipliers): the greedy neighbourhood removal, the induction on r, the bound b_r(ε) = 2^{r(r−2)} ε^{−(r−2)}, Em_v = 1, and
   E M_G((w_v m_v)_v) ≤ ε s². Re-derive the final display (the PDF text is garbled there; use optimizer.tex). Check that the induction hypothesis is applied
   with the right total weight (s_i, not s) and precision ε/4, and that p_i > ε/8 really holds. IMPLEMENT the construction exactly for small weighted K_4-
   and K_5-free graphs (random graphs, random positive weights, a few ε), enumerate its finite law, and check all three properties of (2.3) exactly
   (fractions or high precision). A construction that fails on some graph is the most valuable thing you can find.
3. Lemma 2.3 (cross-mass bound, C_r = 16r²): every step incl. the choice ε = e^{−8x}, k = e^{4x}, the bound on log(1 + k b_r), the vertex-term bound
   (1+y)log(1+y) − y ≤ y log(1+y), (2.6), the case 0 < s < e^{−x}, the random-partition step for overlapping S, D, and A_r + 3 ≤ 4r². NUMERICS: for small
   K_4-free graphs compute a maximizer of F_G (several starts; check (2.1) to 1e-10) and test (2.5) by brute force over ALL pairs S, D (x = 1, 2, 3, also
   x large); report the worst ratio e_w(S,D)/g_x(w(S)) found (the claim is ≤ 16r²; the truth is probably far smaller — record it).
4. §6: Proposition 6.1 (the deletion-cost identity (6.2), the averaging (6.3) incl. the claim that an edge ab lies in G[A_v] exactly when v = a, v = b or v is
   a common neighbour, (6.4), (6.5), the constant test vector, the induction on n with Δ FIXED) and the proof of Theorem 1.1 (deleting degree > 2d;
   Δ = 2d ≥ 4 ≥ 3; |V(H)| ≥ n/2; log(2d) ≥ log d). Numerically confirm (6.2) exactly on small graphs.
5. Does anything in §2 or §6 use more than "K_r-free" — e.g. a property of the maximizer that is lost after deleting A_v (the induction re-maximizes on
   G − A_v: is that legitimate)? Does any constant depend on n, d or Δ?
