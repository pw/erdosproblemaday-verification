HOLDS AS READ

Seat T — printed §5 "Analytic estimates for the square" (TeX 03-moments.tex) and its use in the proof of Proposition 3.1.
Referee: hostile seat T (rerun; previous seat died before reporting). Paper rendered via pdftotext -layout
(/tmp/oaimath/026/seats/T_work/paper_layout.txt); all locations below are PRINTED numbers. Work dir: /tmp/oaimath/026/seats/T_work/.

Bottom line: I read every step of Proposition 5.1, Lemmas 5.2–5.4, the §5.3 pattern-summation remark and the proof of
Proposition 3.1 (§5.4) line by line, re-derived each inequality, and found no false step and no unjustified step. The
printed rate O(L^{-1/2}(log L)^A), uniform in the shifts, IS proved by the printed argument (it is not just o(1)). The
c_G^2 in C_* is correct, not a slip. Findings below are verifications plus two exposition-level remarks.

## Findings

1. Prop 5.1, eq. (13) — statement, rate and uniformity. VERIFIED.
   Quote: "the implied constant may depend on all the fixed data, but is uniform in the actual shifts. In particular the
   error is additive when S(H) = 0."
   Checked every error source in the proof: (i) arithmetic error O(L^{-N}) from Lemma 5.3; (ii) frequency tail
   max|u_γ| > √L: integrand ≤ |Φ| · L^{C_M} by (26), Φ Schwartz ⇒ O(L^{-N}); (iii) telescoping for p ≤ Y:
   |H_p(z)−H_p(0)| ≪ L^{-1/2}(log p)/p on |u| ≤ √L (|p^{-z_S}−1| ≤ |z_S| log p, denominators ≥ 1/2), partial products
   ≤ exp(C Σ_{p≤Y}1/p) ≪ (log Y)^{C'}, Σ (log p)/p ≪ (log Y)^2 ⇒ O(L^{-1/2}(log L)^A); (iv) tails p > Y: no collisions
   since Y = max(2, 2DL^B) exceeds every difference of shifts (incl. a_0), H_p = 1+O(p^{-2}) ⇒ 1+O(1/Y) = 1+O(L^{-B}),
   and B ≥ 1 makes this ≤ L^{-1/2} (the hypothesis B ≥ 1 is genuinely used here; B < 1/2 would break it);
   (v) pole expansion ζ(1+z) = z^{-1}(1+O(|z|)) with |z_S| ≪ L^{-1/2}, multiplicative error times polynomial-growth
   ∏K_i integrated against |Φ|. Nothing depends on the shifts except through H_X and Y. Additivity when S(H)=0 is
   correct because (28) is an additive comparison (telescoping never divides by a local factor). Severity: none.

2. Prop 5.1 — Euler factor, B_p, H_p(0) = local factor of S(H). VERIFIED (algebra + exact numerics).
   Quote: "At z = 0, summing signs over the nonempty subsets of each occupied allowed residue class gives
   P_p(0) = (p − ν_p(H))/(p − δ), B_p(0) = (1 − 1/p)^t."
   Re-derived both cases: unmarked, #allowed classes = ν_p(H); marked, allowed classes exclude a_0's residue, count =
   ν_p(H)−1 whether or not a_0 collides with some a_i, giving 1−(ν_p−1)/(p−1) = (p−ν_p)/(p−1). B_p(0) exponent
   Σ_i Σ_{∅≠S⊂M_i} −(−1)^{|S|} = t. Ratio equals (1−ν_p/p)(1−1/p)^{−(t+δ)}. fourier_check.py: max |H_p(0) − local factor|
   over 400 random patterns (p ≤ 7, fibers ≤ 3, marked and unmarked, with collisions) = 3.6e-15. (27) re-derived:
   P_p and B_p agree to order p^{-1} when residues are distinct; 1/(p−δ) − 1/p = O(p^{-2}). ∏_p B_p = ∏ζ(1+z_S)^{(−1)^{|S|}}
   sign checked (|S| = 1 gives 1/ζ ≈ z). (29): Σ_{∅≠S⊂M_i}(−1)^{|S|} = −1 gives exactly L^{-1} per fiber. Severity: none.

3. Prop 5.1, eq. (14) — constant for fibers of size ≤ 2. VERIFIED (analytically and numerically).
   Quote: "a double fiber contributes w_γ w_γ′/(w_γ + w_γ′) = w_γ w_γ′ ∫_0^∞ e^{−(w_γ+w_γ′)y_i} dy_i."
   Re(w+w') = 2 so the integral converges; Fubini justified as stated; differentiating (25) gives
   (−1)^j ∂_1⋯∂_j F_r(v) = ∫Φ_r ∏w_ℓ e^{−Σ w_ℓ v_ℓ}, so (14) follows with singleton coordinates at 0. Numerics
   (fourier_check.py, rerun today): inversion (25) to ~1e-5; double fiber ∫∫Φ1Φ2 w1w2/(w1+w2) = 0.00409942 vs
   ∫_0^∞ψ1'ψ2' = 0.00409951; singleton ∫Φw = −0.11004 vs −ψ1'(0) = −0.11036 (gap = truncation |u| ≤ 80). The convention
   of Φ_r with the e^{Σv} factor and the sign of the exponent in (25) are consistent. Reality of C (u ↦ −u) correct. None.

4. Prop 5.1 — "a real constant C, depending only on the functions and κ". EXPOSITION.
   Quote: "Then there is a real constant C, depending only on the functions and κ, such that ..."
   In the proof C := ∫Φ∏K_i, and Φ is built from an arbitrarily chosen smooth compact extension F̃_r. For fibers of size
   ≤ 2, (14) shows C depends only on orthant data. For larger fibers (used only for Z^4) independence of the extension is
   not stated or argued. It does follow (apply (13) to a fixed admissible shift set, e.g. a_i = i·N! with N ≥ t+1, so
   S(H) > 0 and L^t·LHS → S(H)C with LHS extension-free), and Z^4 only needs finiteness anyway. Severity: exposition.

5. Lemma 5.2 — weighted BV with shifted endpoints. VERIFIED.
   Quote: "At either endpoint x = X, 2X, the range q ≤ X^σ is contained in the range of (15) for every fixed logarithmic
   saving once X is sufficiently large."
   True for σ < 1/2: X^σ ≤ x^{1/2}(log x)^{−b(A)} at x = X, 2X for large X. Main terms 2X/φ(q) − X/φ(q) = X/φ(q).
   Prime-power removal Σ_{p^j≤3X, j≥2} log p ≪ X^{1/2}L^2 (crude but true); endpoint translation O((H_X+1)L) per class,
   uniform in a, so (17) holds with no union bound; Q·X^{1/2}L^2 and Q·H_X·L are ≪ X L^{−A_0} because σ < 1/2. (18):
   (X/q+1)L + X/φ(q) with q/φ(q) ≤ 2^{ω(q)} ≤ d(q). (19): ∏(1+T/p) ≤ exp(TΣ1/p) and the elementary Σ_{p≤y}1/p bound via
   1/p ≤ e·p^{−1−1/log y} (p ≤ y), Σ_p p^{−s} ≤ log ζ(s), ζ(1+u) ≤ 1+1/u — all correct. Cauchy–Schwarz with K^{2ω(q)}
   weights correct (first factor sums E_X over all q ≤ Q, fine). BV is quoted in the endpoint form (weaker than the usual
   max_{y≤x} form, so implied by it). Severity: none. (Page/equation of the BFI citation NOT checked — see below.)

6. Lemma 5.3 — exact density sum. VERIFIED.
   Quote: "The marked sum on a nonreduced class is therefore exactly zero, not an unestimated exceptional term."
   Correct: residue of n = m + a_0 at p | d_γ is a_0 − b_γ, so the class is reduced iff the mark-exclusion holds; a prime in
   a nonreduced class equals a prime divisor of q ≤ X^σ < X − H_X < n. Reduced-class sum X/φ(q) + O(E_X(q)) with the
   window (X+a_0, 2X+a_0] matching the definition of E_X. ρ_1 = ∏(p−1)^{-1} = 1/φ(q). Assignment count (2^M−1)^{ω(q)}
   correct (each prime of q goes to a nonempty set of coordinates). Unmarked: count X/q + O(1), (24) correct, error
   X^{σ−1}(1+log X)^{M−1} needs σ < 1, as assumed. (23) correct from the per-factor budgets. Severity: none.

7. Lemma 5.4 — singular series in boxes. VERIFIED (proof + numerics).
   Quote: "The Chinese remainder theorem therefore shows that S_y has exactly mean one on complete residue tuples modulo Q."
   E(1−ν_p/p) = (1−1/p)^s holds including collisions; CRT gives exact mean 1; TV of the box tuple mod Q is O_s(Q/h);
   tail: |log T_y| ≪ 1/y + log Δ/(y log y), log Δ ≤ C(s,2) log(Kh) (printed "\binom s2", garbled in text extraction)
   ⇒ O(1/log log h); errors as stated. Minor: "The prime number theorem gives Q ≤ h^{1/2}" — Chebyshev suffices (PNT
   gives Q = h^{1/4+o(1)}); true as written. Numerics (ss_box.py, rerun today, output byte-identical to the dead seat's):
   normalized ordered-distinct sums s=2: 0.9815 (I,I) / 0.9983 (J,I) at h=400; s=3: 0.875 / 0.948 at h=150, approaching 1
   at the expected Gallagher secondary rate ≈ C(s,2)(log h)/h. Consistent with the o(1) claim. Severity: none.

8. §5.3 closing remark and the pattern summation in the proof of Prop 3.1. VERIFIED.
   Quote: "Thus the uniform error in Proposition 5.1, summed over that pattern, is O(L^{−1/2}(log L)^A) = o(1)."
   O(h^t) assignments × L^{−t−1/2}(log L)^A; marked: O(h^{t+1}) × L^{−1} × same. Finitely many patterns because k and
   the family are frozen before X → ∞ (the proof of Prop 2.1 freezes a single k). Severity: none.

9. Proof of Prop 3.1 — matching rule and limits (5), (6). VERIFIED.
   Quote: "Any shift in S △ T occurs once and sets a coordinate of one of the functions in (4) to zero. Its main coefficient
   is therefore zero."
   In Z^2, Z^2V_J and the detector term every fiber has size ≤ 2, so (14) applies; a singleton fiber puts y = 0 in
   (−1)^j∂⋯F_j = f_j, which vanishes on faces (f_j ∈ C_c^∞ of the OPEN orthant). No fiber mixes a Z-shift with b or c:
   b, c ∈ J and Z-shifts ∈ I are disjoint; for the internal mark a ∈ I, identity (8) (re-derived: log(m+a)/L > 1 > τ kills
   the d_a = m+a term) removes a from every subset, so Prop 5.1 is applied with a_0 = a distinct from U ∪ U'. (−1)^j∂F̃_j =
   f_j + Tf_{j+1} since F_{j+1}(v,0) = ∫_{s≥v} Tf_{j+1}; Tf_{j+1} is supported away from faces. Counts C(h,j)/L^j → α_j,
   hC(h,j)/L^{j+1} → λα_j, hC(h−1,j)/L^{j+1} → λα_j are the right ones (Lemma 5.4 with s = j, j+1, j+1, ordered→unordered
   by 1/j!). Budgets: 2τ = 1/4 < 1/2 marked, 4τ = 1/2 < 1 for Z^4, 6τ = 3/4 < 1 detector. Z^4 = O(1) needs only finiteness
   of the pattern constants and |C|·L^{−t}Σ S(H) = O(1). Severity: none.

10. Proof of Prop 3.1 — detector bound (7) and the SQUARED c_G. VERIFIED; c_G^2 is correct.
   Quote: "For their common size j, the coefficient is c_G^2 ‖f_j‖_2^2." and "C_* = λ + λ^2 c_G^2".
   The pointwise inequalities hold (D_G(m;b) = 1 at prime m+b because G(u) = 0 for u ≥ τ and log(m+b)/L > 1;
   θ(m+b)/L ≤ log(2X+h)/L ≤ q_X). The off-diagonal term replaces BOTH primes b ≠ c by D_G(·)^2, so there are two double
   fibers {G at b, G at b} and {G at c, G at c}, each contributing ∫_0^∞ G'^2 = c_G by (14): hence c_G^2, not c_G. This is
   exactly why the term has six factors. Diagonal: (θ/L)^2 ≤ q_X θ/L gives q_X E(Z^2 V_J) → λw. Off-diagonal ordered
   count h(h−1)C(h,j)/L^{j+2} → λ^2α_j. Total limit λw + λ^2c_G^2 w = C_* w. Cross-check: OpenAI's Lean
   (DetectorMoments.lean, `unorderedWeight_detector_bound`) concludes ≤ (lam + lam^2 * l2Mass g^2 + 1) * familyW with
   `l2Mass g = ∫ g^2` (LevelMoments.lean:63), i.e. the same c_G^2, via `tensorProfile g g` and budget `2*(tau+(tau+tau))<1`.
   C_* depends only on λ and G, which is fixed before k and the family. Observation (harmless): by Cauchy–Schwarz
   c_G ≥ 1/τ = 8, so C_* ≥ λ + 64λ^2; only finiteness and family-independence are used. Severity: none.

11. Prop 3.1 setup — extensions. VERIFIED.
   Quote: "multiplication by smooth coordinate cutoffs that equal one near [0, ∞) and vanish below −1 makes it compactly
   supported without changing its orthant values or derivatives."
   Correct; F_j already vanishes when any coordinate exceeds the support bound of f_j; same for F̃_j and for G|[0,∞).
   Severity: none.

## What I did NOT check
- The Bombieri–Friedlander–Iwaniec citation "[3, p. 206, equation (1.4)]" and "ψ notation ... p. 204": no access to the
  source offline. If (1.4) is stated with main term ψ(x)/φ(q) or with max_{y≤x}, the passage to (15) is a one-line
  standard reduction; not a mathematical risk.
- Gallagher [8, p. 5, eq. (3)] and Maynard [13, §6, p. 404] citations (motivational only; Lemma 5.4 is proved in full).
- Printed §§2–4 (Prop 2.1, Lemma 2.2, §4 cancellation), including whether (5)–(7) are exactly what §2 consumes and the
  choice ε = λ^2/(2K_λ) — out of scope for seat T.
- Lean ↔ paper correspondence beyond the detector constant (one theorem read, not a statement audit).
- I did not run new large numerics: density_sum.out (dead seat's run of exact A_δ vs (13)/(14) in 1-D) was inspected,
  not rerun; its trends (main term →1 at rate ~1/ℓ; unmatched/face-vanishing cross terms ≈ 0; marked S({0,2}) =
  1.3203 approached as 1.3054 at ℓ = 15.2) are consistent with Prop 5.1 but are weak evidence at ℓ ≤ 15.
- Time spent ≈ 60 min, single seat, no sub-agents.
