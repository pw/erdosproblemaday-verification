HOLDS AS READ

Main seat (09:00Z erdos cron seat, 2026-10-21, opus 5.5, Team seat 3/yt3): my own reading of the printed paper,
§§1–5, from the pdftotext -layout rendering (seats/O_work/paper_layout.txt), with the TeX consulted wherever the
rendering was ambiguous. Printed numbering throughout.

What I checked, step by step (every step re-derived on paper, not skimmed):
1. Cor 1.2: p_n/n < p_{n+1}/(n+1) ⇔ p_{n+1} − p_n > p_n/n; p_n/n ~ log p_n; C = 2 then discard finitely many n.
   Numerically p_n/n < 2 log p_n for every 2 ≤ n ≤ 10⁶ (n = 1 the only exception), and Rosser–Schoenfeld
   p_n < n(log n + log log n) (n ≥ 6) covers the rest since log log n < log n < log p_n.
2. §2: V_B ≥ 1 when V_B > 0 (all prime arguments exceed X); Lemma 2.2 (p(m)+ > m+2h ≥ p(m)+h, multiplicity ≤ h);
   proof of Thm 1.1: first weighted Cauchy–Schwarz (W V_J = W V_J 1_A), lim inf ≥ λ²/K_λ, 1_B ≤ V_I, ε = λ²/(2K_λ)
   ⇒ Δ = λ²/(2K_λ); second Cauchy–Schwarz (E(W1_{A∖B})² ≤ E W² · |A∖B|/X) with E(W1_{A∖B}) ≥ Δ/2 eventually ⇒ δ = Δ²/(4M);
   h > C log p from λ > C; X = ⌊p_N/3⌋ ⇒ 2X + h < p_N; X/log X ~ N/3. Quantifier order (K_λ before ε, M after) correct.
   E_X W_X → 1 in Prop 2.1(1) is never used (seat L found the same in the Lean).
   Consistency check: the first CS forces λ²/K_λ ≤ lim E W = 1; indeed c_G ≥ 1/τ = 8 by Cauchy–Schwarz on
   1 = |∫_0^τ G'|², so K_λ = λ + λ²c_G² ≥ 64λ² — no contradiction.
3. §3: prime deletion (8) — the a-coordinate divisor of a prime m+a is 1 or m+a, log(m+a)/L > 1 > τ kills the latter;
   subsets containing a map bijectively to U = S∖{a}; F̃_j = F_j + F_{j+1}(·,0) needs symmetry (given);
   (−1)^j ∂_1…∂_j F_{j+1}(v,0) = ∫_0^∞ f_{j+1}(v,u) du = T f_{j+1}(v). α_j = λ^j/j! from C(h,j)/L^j.
4. §4: Lemma 4.1 — A_R ≥ log R, B_R ≤ log 4R, 1/2 ≤ N_R² ≤ 2, and the three scaling identities ∫g² = 1, ∫g = √λ,
   μ_g = λB_R/A_R² re-derived. Prop 4.2 — ‖Q_j‖ = 1, TQ_{j+1} = √(λ/k) Q_j, (10), (11) (sign and the factor
   √((j+1)/(λk))), the event S_j ≤ β − B/k with Chebyshev at deviation d/2 (k ≥ 2B/d) ⇒ 4s²/(kd²), the bracket
   1 − √((j+1)/k) ≤ r/k for j ≥ k − r + 1, |bracket| ≤ 1, the two endpoint terms ≤ 1/r each ⇒ (12).
   Support: f_j ∈ C_c^∞ of the open simplex (coordinates ≥ (inf supp g)/k > 0, S_j ≤ γ < τ).
5. §5: Lemma 5.2 — endpoint BV at x = X, 2X, prime powers O(X^{1/2}L²) per class, endpoint translation O((H_X+1)L),
   Q·X^{1/2}L² absorbed because σ < 1/2, (18), (19) via ζ(1+u) ≤ 1+1/u, Cauchy–Schwarz with K^{2ω}. Lemma 5.3 —
   CRT compatibility, marked non-reduced class empty because a prime n ≡ 0 (mod p | q) would be ≤ q ≤ X^σ < X − H_X,
   (2^M − 1)^{ω(q)} assignments, (24). Prop 5.1 — Fourier inversion (25) with the e^{Σv} factor, (26) [the layout
   rendering reads "2MR − 1"; the TeX says 2^M − 1], P_p(0) = (p − ν_p(H))/(p − δ) (allowed occupied classes number
   ν_p(H) − δ), B_p(0) = (1 − 1/p)^t, H_p(0) = local factor of S(H) in both cases, H_p = 1 + O(p^{-2}) without
   collisions, telescoping on p ≤ Y = max(2, 2DL^B) (needs B ≥ 1 so that 1/Y ≤ L^{-1}), Π ζ(1+z_S)^{(−1)^{|S|}}
   ⇒ L^{-t} Π K_i, (14) via w w'/(w+w') = w w' ∫e^{-(w+w')y}dy. Lemma 5.4 — S_y has mean one on complete residue
   tuples (E(1 − ν_p/p) = (1 − 1/p)^s), TV O(Q/h), Q ≤ h^{1/2}; tail T_y with log Δ ≤ C(s,2) log(Kh) [the layout
   rendering reads "2s log(Kh)"; the TeX says binom(s,2) — an extraction artefact, not a typo].
   §5.4 — support table; Z² matching (unmatched shift ⇒ coordinate face ⇒ zero); counts C(h,j)/L^j → α_j,
   h C(h,j)/L^{j+1} → λα_j, h C(h−1,j)/L^{j+1} → λα_j; detector: D_G(m;b) = 1 at a prime m+b (G(0) = 1, G = 0 past τ),
   ϑ/L ≤ q_X D_G², (ϑ/L)² ≤ q_X ϑ/L, six factors 6τ < 1, each D_G² pair is a fibre of size 2 contributing ∫G'² = c_G,
   so c_G² is correct; h(h−1)C(h,j)/L^{j+2} → λ²α_j ⇒ lim sup ≤ (λ + λ²c_G²) w.

Findings (all exposition; nothing fatal, no gap):
F1 (exposition, §1 and §2): both uses of the prime number theorem can be replaced by Chebyshev's bounds (the Lean does).
F2 (exposition, Prop 2.1(1)): "E_X W_X −→ 1" is stated and never used.
F3 (exposition, (7)): the detector bound is stated as a lim sup over X for each fixed family; the family-independence
   of C_* is the point and is correctly argued, but the convergence rate is family-dependent (the paper says so).
F4 (exposition, §5.1): Lemma 5.2 assumes BV; the paper is therefore rigorous modulo BV (label (b)); the Lean proves BV.
Not checked by me: the cited sources at their cited places (seat W), numerics of Lemma 4.1/Prop 4.2 (seat O), Lemma 5.4
numerics (seat T).
