# Seat P — the algebra, the packing and the fresh-digit lemma (Blinov §§3–4; Chen §2)
Read /tmp/oaimath/191b/seats/BRIEF_common.md first. Your report: /tmp/oaimath/191b/seats/P_report.md; work dir P_work/.

Referee these steps of Blinov's written transfer (patches/reserved-tags.patch, the §3 and §4 hunks) and Chen's §2,
and RECOMPUTE the finite facts by your own code (decorrelated from the authors' checkers — do not import or copy them):

1. The 18-form identity 3·det A·det C = Σ_{t=1}^{18} Π_{j=1}^{3} h_t(A_{·j}, C_{·j}) over Z[u]/(u²−u+1), with the
   table printed in the patch (Lemma norm:decomposition) and in Chen (3). Verify symbolically (all 3×3 matrices of
   indeterminates). Do the two tables agree? Mutation control: flip one coefficient; the identity must fail.
2. The degree-five norm identity end to end, NUMERICALLY over a real finite field: r = 37 (and one more prime
   r ≡ 1 mod 3, e.g. 43), K = F_{r^5} built from an irreducible quintic, power basis 1,θ,…,θ⁴. For random variable
   groups X^(1),X^(2),X^(3) ∈ F_r^15 compute N = Nm_{K/F_r} det(Z(X^(1)),Z(X^(2)),Z(X^(3))) directly, and compute the
   2,916-term sum Σ det(f_{ia}(X^(j))) by following the patch's construction literally (pairs (σZ,σ²Z),(σ³Z,σ⁴Z);
   F_{iw} = Z_i·H_w; normalisation 3^{−2}; constant-coordinate functional ℓ; 9 interpolation nodes). Equal for ≥ 50
   random inputs? Controls: drop one node / omit 3^{−2} / use a non-split prime (r ≡ 2 mod 3, no root u) must fail or be
   impossible. Also confirm distinct Vandermonde labels give N ≠ 0 and equal labels give 0.
3. The packing: twelve-digit {0,1}-words in base 3; exactly 5 below 10 (0,1,3,4,9) and 2,921 below 204,391; norm
   words = [10,204391); k = 408,781; positions i_a=j_a=c(x_a), ℓ_a=k−1−2c(x_a) in [0,k); the matching property
   i_a+j_a'+ℓ_a''=k−1 ⟺ a=a'=a''; tag exclusion (no position-triple with sum k−1 that uses a tag in row 1 and/or
   row 2). Check EXHAUSTIVELY (all pairs x,y in the 2,921-set: is (x+y)/2 in the set only when x=y?).
4. Lemma orb:tagged-moment (the patch's new lemma; Chen §2.4): this is the crux. Read the proof line by line.
   (a) Is F(Y) = U(Y)(Z1(Y)−Z2(Y)) right for labels (λ,λ,μ) with deterministic top rows? (b) Below position 10, are
   the row-1 and row-2 digits exactly as claimed (1 then r's; tag representatives at 0,1,3,4,9, r elsewhere)? Is U_a
   the first nonzero coefficient with 0<|U_a|<r, so v_B(U(B)) = a and b ≤ a? Are ALL coefficients of U below B
   (needed for exact valuation)? (c) J ⇒ F_{k−1} = 0 over the integers: check the carry bounds with
   A0 = 6k²P, P = L1L2L3, B−1 ≥ 100k²P. (d) The joint conditioning: P(b ≥ j and J | labels) ≤ M^{−(2j+1)} for
   1 ≤ j ≤ a — is the digit at v = k−1−a really untouched by the Schur-congruence exposure and does F_{k−1} depend on
   it with coefficient exactly −U_a? (e) θ = B/M² ≤ 1/2 with the stated B interval. (f) the three-label-pattern sum
   E[D·1_J] ≤ 6/(M r^5) + 2/r^10, and the claim E[D | labels] ≤ 2 for EVERY label triple under L1 = L2 = r (the
   generalised orb:conditional with p* = (r/L2)²(r/L3)²).
   Then build an INDEPENDENT small-model exact computation of the lemma's mechanism (your own toy: small prime B,
   small r, short digit strings, a tag layout with the same structure, the fresh-digit position beyond the low prefix)
   that computes P(b ≥ j ∧ F_{k−1}=0 | labels) exactly by enumeration and compares to M^{−(2j+1)}; and a negative
   control where the "fresh" digit lies INSIDE the low prefix (the bound must then fail).
5. Distinct labels ⇒ not J, with the tags present: γ_{k−1} ≡ N(ξ1,ξ2,ξ3) (mod r).
6. Lean (read only; do not build): for FiveTagged.tagged_small_residue_moment, FiveFiniteTheorem.total_small_residue_moment,
   FiveNorm.finite_field_norm, ReservedPacking.reserved_packing, FiveScales: quote the theorem statements; do their
   hypotheses match what the written transfer uses? grep the lean/ dir for sorry, admit, axiom, native_decide, implemented_by.
