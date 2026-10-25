# Seat T — printed §5 "Analytic estimates for the square" (TeX file 03-moments.tex), and its use in proving the moment proposition of §3.
Read COMMON.md first. Your scope:
1. Proposition 5.1 (uniform mixed moments): hypotheses (support budgets Σρ_r < 1 unmarked, < 1/2 marked; shifts |a_i| ≤ D L^B),
   the main term L^{-t}(𝔖(H) 𝒞 + O(L^{-1/2}(log L)^A)), uniformity in the shifts, the additive error when 𝔖 = 0, and formula for 𝒞
   when fibers have size ≤ 2.
2. The weighted Bombieri–Vinogradov lemma: endpoints, prime powers, translation by |a| ≤ H_X, the Cauchy–Schwarz trick with
   K^{ω(q)} weights, the bound q/φ(q) ≤ 2^{ω(q)}, the Mertens-type bound via ζ(1+u) ≤ 1+1/u. Is BV quoted in a correct form and range
   (q ≤ x^{1/2}(log x)^{−b(A)} vs the range q ≤ X^σ, σ < 1/2 used)?
3. The exact density-sum lemma: compatibility, the marked case (non-reduced classes contribute exactly zero because n > q), the count
   (2^M − 1)^{ω(q)} of assignments, and the unmarked O(1) error.
4. The Fourier evaluation: the transform Φ_r with the e^{Σv} factor, inversion valid on the orthant, the interchange bound,
   the Euler factor P_p, the zeta-pole factors B_p and the claim H_p = 1 + O(p^{-2}) for p > Y, H_p(0) = local factor of 𝔖, the
   additive telescoping comparison that "never divides by a zero local factor", the pole expansion and the kernel K_i, and the final
   derivative formula for fibers of size ≤ 2 (the identity w w'/(w+w') = w w' ∫ e^{−(w+w')y} dy and Fubini).
5. Lemma 5.? (singular series in boxes, Gallagher-type): truncation at y = (1/4) log h, Q ≤ h^{1/2}, mean exactly one on complete
   residue tuples, the tail T_y bound, the claimed error terms.
6. The evaluation of the square (proof of the moment proposition): the matching rule (unmatched shift ⇒ face vanishing ⇒ zero main
   term), the limits C(h,j)/L^j → α_j, h C(h−1,j)/L^{j+1} → λα_j, E Z^4 = O(1), and especially the DETECTOR bound: the pointwise
   inequalities θ(m+b)/L ≤ q_X D_G(m;b)² and (θ/L)² ≤ q_X θ/L, the six-factor off-diagonal term with budget 6τ < 1 (unmarked), why
   the two subsets from Z² must be identical there, the coefficient c_G²‖f_j‖² — note c_G = ∫|G'|² is used SQUARED in C_*; is that
   right? — and why C_* is independent of k and the family. Also: is "(−1)^j ∂...F = f_j vanishes on every coordinate face" enough to
   kill every off-diagonal main term in Z², Z²V_B and the detector term, including fibers that mix a Z-shift with b or c?
Numerics welcome where they test a claimed identity (e.g. singular-series box means for s = 2, 3 at moderate h).
Out of scope: printed §§2–4 except where §5 is applied.
