# Referee report, seat "allocation": §13 (pp. 111–118), §14 (pp. 118–125), §15 (pp. 125–132), plus §1.3 phase 3, Figure 1, Appendix A (pp. 166–169)

Paper: OpenAI, "The hypercube Ramsey number has linear order" (23 Sept 2026), /tmp/oaimath/171/paper.pdf.
How I read it: every page in scope was read in the PDF render (pp. 1–8, 10–25, 106–133, 166–169). Every exponent I quote was checked against the `pdftotext -layout` text. The render makes superscripts easy to misread: I first read Lemma 12.6's "exp(o(n^{.2}))" as "exp(o(n^2))", and the text settled it. I read §3 (Lemmas 3.2–3.10), §12 (Cor 12.1, Lemmas 12.2–12.6) and Prop 10.1 / Cor 10.2 only as statements this scope depends on. Other seats referee their proofs.

Bottom line: I found **no FATAL objection and no mathematical GAP** in §13–15 as written. The objections below are UNCLEAR (compressed exposition I could not check line by line) or COSMETIC. The "verified vs skimmed" list is the real deliverable.

---

## 1. Objections

**O1. UNCLEAR (exposition, not a mathematical gap). Prop 15.4, small-bin repeat handling and the ordering of the comparisons. pp. 130–132.**
Quoted: "At this point the bin variables have their independent raw laws given W. Integrate removed variables in reverse order. Earlier removed choices can be held fixed while charging the necessary repeat of a later one; the surviving label integral does not read that later variable." Also: "Reverse integration has therefore used independence only after both the label and bin comparisons, not under the avoidance-conditioned bin law."
What I checked:
- Every cost exponent in this proof:
  - core-near fraction 2^{−n}e^{.01 s_i} times cap 2^n e^{−200 s_i};
  - core-bin repeat cost n^{O(1)}·4e^{2kT}d_i/M_i ≤ 2^{−n}e^{o(s_i)}. This uses d_i/M_i ≤ 2^{−n}e^{q/2+q^{a_C}}/c and q = o(s_i), because s_i ≥ a q^{M_hi}/10^6;
  - crossing-repeat cost 2^{−n+o(n)};
  - crossing-graph cost (n²2^{−n+o(n)})^j·3^{2jℓ_i} → 0.

  All are correct.
- That (15.3) holds on J_v.

What I could not check: the claim that, after the label-stage comparison ((3.2) / clock) and then the bin-stage comparison (Lemma 3.5), the integrand really is "a nonnegative function only of the kept bin choices and local W, multiplied by the repeat indicators". The argument is stated rather than derived.
- Severity: UNCLEAR.
- What would settle it: write out the n-th moment as an explicit sum over (position tuple, removal mask). Then show for each term that the order label-comparison → bin-comparison → reverse integration of removed variables only ever integrates a function of variables not yet conditioned.

The Lean formalisation is the natural cross-check for this step.

**O2. UNCLEAR (exposition). Prop 15.3, "Capacity certificates" plus the LLL charge accounting. p. 129.**
Quoted: "For a certificate involving l groups, the reciprocal neighbor product is at most exp(O(lδ_n)) ≤ 2^l, which is paid by its chosen charge inflation."
Verified:
- a_g(y) = h_i U_g^W(D)(y) ≤ d^{−1/2};
- the bucket/l_j arithmetic: (l_j−1)λ_j ≤ K'm_j + c'2^{−j/2}, l_j−1 ≥ 20z, l_j − 1 ≳ d^{1/2}2^{j/2};
- the subset sum 2^{l}z^{l−1}/(l−1)! ≤ 2(2e/20)^{l−1};
- Σ_j(K'm_j + c'2^{−j/2}) ≤ K'θ_* + c'/(1−2^{−1/2}) ≤ θ_0;
- δ_n = o(n^{−4P}).

So the hypothesis p ≤ x∏(1−x_j) of Lemma 3.5 is met, with x = 2^l·p for certificates and x = n^{−5P} for star constraints, given R = P².

Not checked: that the neighbour relation used here (events joined when their bin-choice variable scopes overlap) is exactly the one for which "independent underlying variables … satisfy this hypothesis with p_i = Pr(E_i)" (Lemma 3.5, p. 12).
- Severity: UNCLEAR. I believe it.

**O3. COSMETIC (exposition). §14.1, use of Lemma 3.8 on Q_h. p. 119.**
Quoted: "Use the geometric height device on Q_h with step bound 6, radius ⌊ρh⌋, λ = h^{10}, activation and crowd exponents b_0 = ω/8, b = ω/2, height-proof exponents a_g = ω/12, ζ_g = 1 − θ_g = ω/30, 0 < σ_g ≪ ω".

The problem: Lemma 3.8 (p. 15) is stated on "Q_d, where d = Θ(n)", with λ = n^{J_0} and every asymptotic in n. Here it is applied with h in the role of n. In low cluster mode h can stay bounded, so h ≥ Q_0^{M_lo} only.

The transfer is legitimate. The lemma's proof uses n only as the dimension parameter, and "sufficiently large n" becomes "h above a fixed threshold", which Q_0 supplies. I checked the lemma's parameter constraints for the stated choices:
- b_0 > a > ζ+σ+(1−θ): .125ω > .0833ω > .0667ω + σ_g, which needs σ_g < ω/60;
- b > a + 4σ;
- θ = 1 − ω/30 > .9 for (iii);
- radius ⌊ρh⌋ ≤ (1/4+o(1))h;
- 2DH + O(ρh+1) < 10ρh, since H = O(h^{1−ω/30+σ_g}) = o(h).

The paper never says "apply Lemma 3.8 with n := h", and "0 < σ_g ≪ ω" is the only place the needed σ_g < ω/60 is implied. Fix: one sentence.

**O4. COSMETIC. Prop 13.3 proof, p. 116.**
Quoted: "ℓ_i ≤ log_2(S/M_i) + 1." Since r_i ≥ p_i, i.e. 2^{−ℓ_i} ≥ M_i/S, in fact ℓ_i ≤ log_2(S/M_i). The weaker bound is harmless.

**O5. COSMETIC (exposition). §14.2, p. 120.**
Quoted: "As in the proof of (10.1), clip log ratios below at log(.24). Their conditional means are at least −log 4 + .7a."

This does not follow from E[ratio] ≥ 1/4 + a and ratio ∈ [.24, 1] alone. The chord bound on [.24, 1] gives only −log 4 + 1.88a − .022, which is worse than −log 4 + .7a for a = θ/100 small.

It is true because, by Jensen and (7.2), the ratio is ≥ (1/2 − n^{−η_0})² outside an e^{−Ω(n^{η_0})} event. The chord from 1/4 − ε to 1 then gives −log 4 + 1.84a − O(ε). The text does say "Jensen and (7.2) then bound the probability of a ratio below 1/4 − O(n^{−η_0}) by e^{−Ω(n^{η_0})}" one sentence earlier, so the ingredient is there. I verified the bound. It is merely implicit.

**O6. COSMETIC. Lemma 13.2 proof, p. 112.**
Quoted: "Here we can take deviation 2n^{−η_0} = o(1) … Here |m(y)|, |m(y′)| ≤ 4n^{−η_0}". Consistent, since m = 2D − 1. The real content is that the first-set width q^{a_C} ≤ n^{a_C} ≪ n^{η_0}, so (7.2) applies. Recorded only because the "o(1)" is weaker than what is used.

No other "clearly / similarly / by symmetry / as before" occurs at a hard step in §13–15. A grep of the extracted §13–15 text finds only:
- "as in Lemma 13.2" (p. 115) — checked, same outlier removal;
- "as in the cube tilings of [6, Section 2.2]" (p. 115) — checked against the source;
- "As in Section 10.1" (p. 119), the site-distance-6 / O(h³) incidence — re-derived independently for the §14 syndrome map, see V14.1;
- "As in the proof of (10.1)" (p. 120) — see O5;
- "likewise" (pp. 115, 129) — both checked.

---

## 2. Brief items (a)–(h): findings

**(a) Def 13.1, Lemma 13.2, and the "second use" of Cor 10.2.**

*g-bound.* A bias witness consists of two uniform sets of size ≥ Ne^{−g^{a_B}}, so both widths are ≤ g^{a_B} ≤ n^{a_B}, using bias ≤ 1/2 ⇒ g ≤ n. Corollary 12.1 / Cor 11.4 with error slack ι/2 holds at budgets (n^{x(ι/2)}, αn), and a_B < x(ι/2) is chosen. Then g/n ≤ n^{−1+ι/2}. ✓

*q-bound.* Argue by contradiction along a subsequence with log_n q → γ' ∈ [γ, 1].
- Column-degree outliers number < 2Ne^{−n^{η_0}}, by (7.2) applied to their uniform sets. The first set has width q^{a_C} ≤ n^{a_C} ≪ n^{η_0}.
- The red codegree equals (1+m+m'+K)/4 with f = 2·1_G − 1. Blue flips the signs of m and m' and keeps K. So both colours give ≥ 1/4 + θ/8, and the diagonal is ≈ 1/2. ✓
- Witness for Prop 10.1:
  - μ uniform on the first set, width ≤ q^{a_C}+O(1) < n^δ;
  - λ is the size-weighted mixture of uniform half-mass bins, so ν is uniform on their union, width ≤ q^{a_C}+O(1);
  - atoms ≤ 2e^{−q} ≤ e^{−n^ζ};
  - codegree ≥ 1/4 + n^{−δ}.
- ζ < γ' and γ'a_C < δ < min(η_0, ζ, 1)/2000 are compatible, since a_C < min(η_0,1)/10^6.
- ζ and δ depend on γ', i.e. on the subsequence. This is legitimate: Cor 10.2 (p. 101) gives eventual absence "for every fixed rational admissible parameter choice, in both orientations and both colors", which is countably many properties stabilised by Lemma 3.2. Eventual absence persists to all subsets of the retained sides, so it holds uniformly on residual sets. ✓

**(b) Prop 13.3.**
- *Trichotomy, boundary conventions, termination* (the "bounded test first" convention is App. A p. 169).
  - If max(g,q) ≥ M_1Q_0 and g ≤ M_1q, then q ≥ Q_0, both when q ≥ M_1Q_0 and when g ≥ M_1Q_0.
  - Direct mode forces g ≥ M_1Q_0.
  - Each pass either extracts a patch of size ≥ cNe^{−n^{o(1)}} or stops in the bounded case. Residual sides stay ≥ N − o(N) − ⌊N/3⌋ − .1N ≥ cN. ✓
- *Direct extraction.*
  - |U_1| ≥ |U|/8 ≥ Ne^{−(2g)^{a_B}} needs g^{a_B}(2^{a_B}−1) ≥ log 8, given by Q_0.
  - The absent 2g budget gives d(U_1,V) < 1/2 + 2g/n. The 1/8·(1/2+2g/n) + 7/8·(1/2+g/(2n)) = 1/2 + 11g/(16n) arithmetic is correct and contradicts the witness ≥ 1/2 + g/n, so |U^+| ≥ |U|/8 and c = 1/8.
  - Random M_i-subsets preserve degrees to o(1/n) (Hoeffding, M_i = e^{Ω(n)}, union over ≤ N rows). ✓
- *Cluster extraction.*
  - Outlier removal leaves |m| ≤ 4n^{−η_0}.
  - Half-mass bins are cut into blocks of size d_i ≤ e^{q/2}, losing ≤ 2e^{−q/2}.
  - The common size is a multiple of d_i, at least ~ Ne^{−q^{a_C}}/2 ≫ d_i.
  - The codegree is ≥ 1/4 + θ/4 − 2n^{−η_0} > 1/4 + 3a, since a = θ/100.
  - c does not depend on Q_0, which matters for (b′) below. ✓
- *One colour, one orientation.*
  - The selection is a pigeonhole over finitely many types at each n: 5 modes × 2 orientations × 2 colours, so S ≥ (.1/20)N. No subsequence is needed, because each mode's argument holds "for all sufficiently large n" with thresholds fixed before n.
  - The selection is not just legitimate but necessary. The host is bipartite (only X×Y edges are coloured, Lemma 2.1), so every patch must send odd roles to the same host side, or crossing edges would land inside one side.
  - Every downstream input is symmetric under swapping orientation or colour: (12.1) "in either order … for either color", Cor 10.2 "both orientations and both colors", the color-free inner product of Def 13.1, and Lemma 12.6. ✓
- *Dyadic rounding and leftover.*
  - r_i = 2^{−ℓ_i} ∈ [p_i, 2p_i), so Σ_I r_i ≥ 1.
  - In the decreasing order, the first prefix J whose sum reaches 1 sums to exactly 1: all terms and 1 are multiples of the last term, and the previous partial sum was < 1.
  - Σ_J M_i > S/2.
  - Patches in I \ J are simply unused, as are the surplus labels inside a used patch (M_i/#roles ≥ S/2^n ≥ c'C_n → ∞).
  - By Kraft equality, a complete prefix code with lengths ℓ_i exists, and leaf i has 2^{n−ℓ_i−1} ∈ [2^{n−1}M_i/S, 2^nM_i/S) roles of each parity. ✓
- *Crossing edges.*
  - For v in leaf i, flipping coordinate j ≤ ℓ_i lands in a leaf whose codeword agrees with w on [j−1] and differs at j. Its length is ≥ j, or it would be a prefix of w, contradicting prefix-freeness. So the flips go to distinct leaves, and the edge is a leading flip for both endpoints. This matches CFLS Prop 2.2(ii), see the citation table.
  - Every cube edge joins an even role (label in X_i) to an odd role (label in Y_j). It constrains only the even row Z_v, through the factor I_x(y_b)/D_{i(b)}(x) for bulk/crossing neighbours, or through supp σ_v for internal ones.
  - Labels in different patches are distinct because the X_i are pairwise disjoint and the Y_i are pairwise disjoint.
  - The ⌊N/3⌋ reserve (p. 112) is removed before g and q are ever measured, so it is disjoint from every patch. It is used only by the low modes (p. 133, "Split the reserved Y-labels into disjoint late pools"). In §13–15 no reserve label is used; §16–18 must keep late-pool labels distinct (other seat).
- *(b′) Allocation budget ℓ_i, log(N/M_i) ≤ s_i/(1000u).*
  - Direct: log(N/M_i) ≤ g^{a_B}+log 8 and ℓ_i ≤ log_2(N/M_i), against s_i/(1000u) = 10^{−6}g/u.
  - Cluster: q^{a_C} + O(1) against a q^{M_lo}/(10^9 u).
  - Both hold above a Q_0 chosen after u, a_B, a_C, a, M_lo, c. Achievable for every i ∈ J. ✓
- *Bounded branch.* One patch with M_i ≥ cN, J = {i}, ℓ_i = 0. K comes from a fixed dyadic budget b ≥ M_1Q_0 with Ne^{−b^{a_B}} < aM_i/10. ✓

**(c) Lemma 13.4.**
- Direct.
  - The lower bound is preserved because only rows are removed and π_i is fixed.
  - Upper trimming: rows with D > 1/2 + 4g/n number < Ne^{−(2g)^{a_B}}, which is a fraction e^{−(2^{a_B}−1)g^{a_B}}/c of M_i.
- Cluster.
  - The bias budget b' ∈ [q^{C_b}, 4q^{C_b}] exceeds g ≤ M_1q.
  - Outlier rows (> 8q^{C_b}/n) together with a uniform approximant V of π_i (|V| ≥ Ne^{−b'^{a_B}}) would witness bias ≥ b'/n. The width separation q^{C_ba_B} ≫ q^{a_C} + q^{4ωM} holds since C_b a_B > 100a_C and 4ωM < a_C/125. ✓
- Bounded. ✓
- Clique exclusion.
  - Greedy disjoint 2θ-cliques of size ⌈e^{Q_i}⌉ with union ≥ Ne^{−Q_i^{a_C}} would form a reverse-orientation q-witness of budget Q_i > q (Q_i ≥ q², or Q_i > √M_1·q/2).
  - Δ_i = e^{C_*Q_i} ≤ e^{s_i}, since 2C_*q² ≤ a q^{M_lo}/10^6 and 2C_*/√M_1 ≤ 10^{−3}. ✓
- Other patches. (12.1) with the first law conditioned on mass e^{−cn} (width ≤ n^{ι/2} + cn < αn) and π_j of width ≤ n^{x_*/4} gives outliers ≤ e^{−cn} per j. With #I ≤ e^{n^{2ι}}, the union is negligible. Lemma 12.6 allows exp(o(n^{.2})) laws, and 2ι < .2. ✓
- Codegree after removal: (1/4+3a−r)/(1−r) ≥ 1/4+a for r < a. ✓
- Stability. An ℓ¹ mesh of diameter n^{−3} preserves: own-degree margin 8→10 (with 2q^{C_b}/n ≫ n^{−3}), 2b_* → 3b_*, 2θ → 3θ (|K_π − K_{π'}| ≤ ‖π−π'‖₁), and the relaxed (12.3). ✓

**(d) §14.**

*(14.1).*
- p_g^W(y) ≤ (2/A(F))Σ_D r_g(D)D(F)D(y)1_F ≤ (2/A(F))·4/M_i ≤ 8e^{2kT}/M_i.
- The masked bin prior is ≤ (1/0.8B_i) = 1.25d_i/M_i ≤ 2d_i/M_i. This uses that at most M_i/10 labels are expensive ⇒ ≤ B_i/5 bins dropped.
- |supp U| ≥ D(F)|D| ≥ e^{−1.5kT}d_i/2. ✓

*Likelihood bound L_w ≤ e^{(log2−.06a)kh}𝒬.*
- Per group, the termwise ratio 2(A(F_{−c})/A(F))(D(F)/D(F_{−c}))^{2−j} ≤ 2e^{(log4−.4a)k+(log2−.08a)k(j−2)} ≤ 2e^{(log2−.08a)kj} needs j ≥ 2.
- The syndrome map gives j ≥ 2. I re-derived it: s(ψ(z)) = 0, the fibres are {w⊕e_l} of size h, ψ(v⊕e_l) = v⊕e_l⊕e_{s(v)+l}, so the multiplicities are 2 (h/2 groups) or h.
- The mixture cost |ℒ_g| = e^{O(T log h)} = e^{o(ak)}.
- The reference 𝒬 does not depend on w, and selections and validity are recomputed at w. This matches the requirement of Lemma 3.7 ("The gate and every selection rule in F_z must be recomputed as z varies"). ✓

*(14.2).*
- Posterior density e^{(log2−.05a)kh}; joint cap (2N/M_i)^k e^{(log2−.05a)kh} ≤ e^{(log2−.04a)kh}, using log(N/M_i) ≤ ah/(10^9u).
- |B|/N ≤ 2^{−h}e^{.02ah}.
- P(r fixed coordinates in B) ≤ exp(kh[−.04a+.01a log2+.02a]) = e^{−.013akh}.
- P̄(B^c) ≥ .01a(1−o(1)), so N max σ_v ≤ 2^he^{−.02ah}/(ca) ≤ 2^he^{−500s_i} (500s_i = .0005ah).
- Mean bound:
  - the cancellation Σ_y Z(y)P̄_{c,y}(x) = ∫(1/k)Σ_r 1{w_r=x}·1_gate dμ^{⊗k};
  - level 0 contributes λ·(3/λ)·(2/M_i), and Lemma 3.8's 3/λ bound is uniform over fixed eligibilities E, so the dependence of selection on W_c is harmless;
  - higher levels contribute poly(h)·λ·e^{−h^{Ω(1)}}·(2/M_i);
  - K = O(1/a). ✓

*(14.3).* Markov at ε_i gives h^{O(1)}e^{−.009akh}, and the union over 2^{h−1} roles is exp(−h^{1+Ω(1)}), since k = h^{3ω}. ✓

*Support of σ_v.* σ_v is nonzero only on V_v, which requires validity of the neighbouring groups. The selected center c at ψ(v) lies in every neighbouring group's list, so each internal y_b ∈ F ⊂ common neighbourhood of W_c's entries, and the posterior support consists of such tuples. ✓

*Prop 14.2 (Kakutani).*
- The domain ∏_i{π_i: M_i max π_i ≤ e^{10k_iT_i}} × Δ(Y_i) is a nonempty compact convex polytope.
- π^out is single-valued and continuous: barycentric hat functions are continuous, and every realisation's output is fixed. In low mode it is a ratio with denominator ≥ 1 − exp(−h^{1+Ω(1)}), and the pretrim normaliser is ≥ 1 − h²√ε.
- π^out lands in the cap: 32e^{2kT} ≤ e^{10kT}.
- The argmax of a linear functional over a simplex is a nonempty convex face, and the correspondence has closed graph (Berge).
- Fixed-point bound: max π_i = z_i·π_i ≤ (10/M_i + o(1/M_i)) = 11/M_i, because every label in supp π^out is retained by some mask with vertex price ≤ 10/M_i and the vertex prices are within o(1/M_i) of z_i. ✓
- Lemma 3.3 is not used here; Kakutani is applied directly.

*Fixed scales (Appendix "The scales q, h_i, d_i may stay fixed").*
- Inside §13–14, every estimate is of the form "for h (or q) above a threshold". Q_0 is fixed after all small constants and supplies it. No estimate inside §13–14 needs q → ∞.
- The losses that are fixed in low mode:
  - e^{O(q^{C_b})} from the bulk degree error 10q^{C_b}/n over n edges;
  - Δ_i;
  - (N/M_i)·2^{ℓ_i}.

  These are beaten by e^{−500s_i}, because M_lo > C_b+100 and q^{a_C}, C_*q² ≪ q^{M_lo}.
- Several failure probabilities in low mode are fixed small constants rather than o(1): exp(−h^{1+Ω(1)}), ε_i, and h²√ε_i. Their absorption ("late classes supply polynomial slack") is §16–18 business. I checked only that §14 claims nothing stronger (Prop 14.2: "they do not require a low-mode scale to tend to infinity").
- Lemma 14.3: h ≤ (log n)^{.1} ⇒ 2^h = n^{o(1)}; k log N = n^{1+o(1)} uses N ≤ n2^n. ✓

**(e) §15.**
- *Lemma 15.1 (high direct).*
  - Crossing filters: τ ≤ (2(1+O(b_*)))^{ℓ}σ_v ≤ 4^ℓσ_v. The deep discrepancy (12.1) bounds each step's exceptional y-set by e^{−n^{x_*}/2} (first law width ≤ log(N/M_i)+2ℓ_i < αn).
  - D_i^{−|L_v|} ≤ 2^{|L_v|}e^{−.4g}, from (1+g/(2n))^{n−o(n)} ≥ e^{.49g}.
  - Δ_i max τ D^{−|L_v|} ≤ e^{s_i}·2^{n+ℓ_i}e^{−.4g}/((1−a)M_i) ≤ e^{s_i}(N/M_i)2^{ℓ_i}·2e^{−400s_i} ≤ e^{−200s_i}. This uses 2^n ≤ N.
  - Lemma 12.2's hypotheses hold: the width of τ is ≤ n^{ι} ≤ n^{x_*/4}; |D − 1/2| ≤ 4g/n ≤ 4n^{−1+ι/2} ≤ b_*; and the bulk inputs are i.i.d. π_i.
  - Lemma 12.5's hypotheses hold: no ⌈e^{Q_i}⌉-clique on supp τ ⊂ cleaned X_i; homogeneous π = π_i; d = |L_v|. So P(Z < 1/2) ≤ 2^u(n^{−3R} + C_u n^{−0.2K_B}) ≤ n^{−R}.
  - Lemma 3.10 with B = 5:
    - predicates ≤ n^{−R} ≤ n^{−P_*};
    - n rows per predicate and n predicates per row;
    - atoms 1/M_i = e^{−Ω(n)};
    - column sums ≤ 2^n/S = O(1/C_n) ≤ θ_0;
    - log(#labels) ≤ log(n2^n) = O(n).
  - Lemma 3.6:
    - L = 2^ne^{−200s_i};
    - near set = distance ≤ 2, f|U| = O(n²);
    - nfL = O(n³)2^{ℓ_i+1}e^{−200s_i} → 0;
    - the joint product over disjoint stars is ≤ (1+o(1))∏M_iσ_v(x) by the clock bound on ≤ n² ≤ n^5 queried rows.
  - Column sum = (|E_i|/M_i)A_x ≤ (2^n/S)A_x. Union: N(K'/C_n)^n ≤ n(2K'/C_n)^n → 0. ✓
- *§15.1.*
  - Product test: E[mass of (J_v^0)^c] ≤ e^{−Ω(n)} + e^{−n^{.5}}. The true Hoeffding rate is e^{−Ω(n^{.92})}, since each term is O(b_*). Markov at e^{−n^{.2}} gives ≤ e^{−n^{.2}}.
  - Large-interaction test: E T_v ≤ e^{−450s_i}·O_u(1) + e^{2^uξn−αn/4}·poly ≤ e^{−300s_i}, with Γ = Δ_i max σ_v D_i^{−|L_v|} ≤ e^{s+20q^{C_b}}2^{h+|L_v|}e^{−500s}/N ≤ e^{−450s}.
  - LLL: degree ≤ n^{O(1)}e^{(a/10^9)h} and charge e^{−s_i} with s_i = ah/10^6 and s_i/log n → ∞ (h > (log n)^5), so ∏(1−x_j) → 1. ✓
- *Lemma 15.2.*
  - J_v-removed mass ≤ (M_i/N)2^{h}e^{−500s}(e^{−n^{.2}}+e^{−Ω(n)}) = o(1), since ι < .2.
  - Lemma 12.2 (heterogeneous): denominators D_b^W match 1+a_{l,x} = 1_G/D_{π_l} with π_l = p^W_{g(b)}; |D_b^W − .5| ≤ 2b_* on J_v; small widths.
  - The 2^u conversion via the ∏D_b^W/D_i ≥ 1/2 gate.
  - 5^{u(ℓ+1)}e^{−100s} ≤ n^{−3R}. ✓
- *§15.2 load success H.* Lemma 3.6 with the near relation "same slice": nfL = n2^{h+ℓ+1−n}·8e^{2kT} → 0, and means M_iπ_i(y) ≤ 11 by (14.4). ✓
- *Prop 15.3.*
  - Small bins: (log n)^{c_q} < q ≤ (log n)², h_i < 2q^{M_hi}, d_i^{.025} ≥ min(e^{.0125q}, e^{.025√log n}), so h_i = o(d_i^{.025}). h_i > (log n)^5 since c_qM_hi > 5.
  - Lemma 3.9: atoms ≤ 2e^{1.5kT}/d_i ≤ d^{−.95}, column ≤ θ_0 ≤ .4, ≤ h_i ≤ d^{.025} queried rows per bin, d → ∞.
  - Large bins: k_iT_i = O(q^{4ωM_hi}), with 4ωM_hi < a_C/125 < a_C/2 and ≪ log d_i = q/2. Atoms 2e^{1.5kT}/d_i ≤ e^{−(log n)²/3}, superpolynomial ⇒ ≤ n^{−A_*}.
  - Clock predicates n^{−R/2} ≤ n^{−P_*}. ✓
- *Prop 15.4 and Hall.*
  - Odd labels are injective across patches (disjoint Y_i) and within a patch (disjoint physical bins, plus the clock lemma or Lemma 3.9 inside each bin).
  - Z_v in (15.1) carries ∏ over b ∈ L_v ∪ H'_v, i.e. bulk and crossing neighbours in other patches. Internal neighbours are covered by supp σ_v. So supp Z_v ⊆ X_i ∩ common neighbourhood of all n odd neighbours.
  - Rows of patch i live in X_i, which is disjoint across patches, so global Hall reduces to per-patch Hall.
  - Row mass ≥ 1/2 ⇒ normalising multiplies each row by ≤ 2 ⇒ column sums ≤ 1. Then |S| = ΣΣp_v ≤ |∪supp| (p. 12) gives Hall.
  - Joint existence: P(H) = 1−o(1), P(H ∩ some column > 1/2) = o(1), and the mass gates are enforced surely on passing histories. ✓
  - The moment bound itself is O1.

**(f) Applications of Lemmas 3.x and 12.x in scope; hypotheses checked (page of use).**
- Lemma 3.2 / Cor 10.2: p. 112 ✓.
- Lemma 3.5: p. 127 (W-LLL) ✓; p. 129 (bins) ✓, see O2; p. 129 (small-bin labels) ✓ (degree n^{2+o(1)}, charge n^{−5P}); pp. 130–132 comparisons, see O1.
- Lemma 3.6: p. 126 ✓; p. 128 ✓; p. 132 ✓.
- Lemma 3.7: p. 123 ✓ (gate recomputed at w; 𝒬 independent of w).
- Lemma 3.8: pp. 119–123 ✓, see O3.
- Lemma 3.9 / (3.2): p. 129 ✓; p. 131 ✓.
- Lemma 3.10: p. 126 ✓; p. 129 ✓.
- Lemma 12.2: p. 128 ✓.
- Lemma 12.3: p. 127 ✓ (one-free gated, σ_v width ≤ n^ι).
- Lemma 12.4: pp. 125, 128 ✓.
- Lemma 12.5: pp. 116, 125, 127 ✓.
- Lemma 12.6: p. 117 ✓ (#I ≤ e^{n^{2ι}} = e^{o(n^{.2})}, uniform first law of width ≤ n^{ι/2}).
- (12.1): pp. 112, 117, 125, 126, 128 ✓.
- (7.2): pp. 112, 120 ✓.
- (10.1): pp. 120–121 ✓ (with O5).

**(g) Where N/2^n → ∞ and N ≤ n2^n enter.**
- C_n → ∞, with no rate:
  - odd column sums O(1/C_n) ≤ θ_0 (pp. 126, 128);
  - even column sums O(A_x/C_n) (pp. 126, 132);
  - the union bounds N(K'/C_n)^n ≤ n(2K'/C_n)^n → 0 as soon as C_n > 4K' (pp. 126, 132).

  In fact the high modes need only C_n ≥ an absolute constant.
- N ≥ 2^n: the caps 2^n/N ≤ 1 (pp. 125, 127, 130).
- N ≤ n2^n:
  - the label unions above;
  - log N = O(n) in Lemma 14.3 and in the clock lemma's "log g = O(n)".
- I found no step needing a rate, i.e. no N ≥ n^c2^n or N ≥ (log n)2^n.
- The §1.3 gain heuristic (M/N)(1+2δ)^n with δ = g/(4n) is exactly the inverse of the Lemma 15.1 cap, (N/M_i)2^{ℓ_i}e^{−g/2}·e^{s_i}.

**(h) Citations: see the table in §3.**

---

## 3. Citation table (scope §13–15)

| Cited result | What the paper claims | Source says (quote; version read) | Verdict |
|---|---|---|---|
| [6] CFLS, *Ramsey numbers of cubes versus cliques*, §2.2 (cited p. 115) | "The allocation uses subcubes obtained by fixing initial coordinates, as in the cube tilings of Conlon, Fox, Lee and Sudakov [6, Section 2.2]" | arXiv:1208.1732v2, §2.2 "Tiling the cube": "a tiling … uses only cubes that have all their fixed coordinates at the start of the vector. That is, they are of the form C = (a1, …, ad, ∗, …, ∗) … We will call such a cube special". Prop 2.2(ii): "Two disjoint cubes C = (a1,…,ad,∗,…) and C′ = (b1,…,bd′,∗,…) for d′ ≤ d are adjacent if and only if (a1,…,ad′) and (b1,…,bd′) differ in exactly one coordinate"; (iii) "there are at most d other special cubes C′ … of codimension d(C′) ≤ d which are adjacent to C." | MATCH. The paper uses only the geometry: complete prefix code, ℓ_i crossings to distinct leaves. I re-derived that independently. |
| [13] FGMSS, *On the Ramsey number of the triangle and the cube*, §2 (cited p. 115) | "their adaptation by Fiz Pontiveros, Griffiths, Morris, Saxton and Skokan [13, Section 2]" | arXiv:1302.3840v1, §2: "Q_x = {(y1,…,yn): yi = xi for each 1 ⩽ i ⩽ d} denote the subcube of Qn consisting of points whose initial coordinates agree with x … if Qx has co-dimension d, then every vertex v ∈ V(Qx) has exactly d neighbours in V(Qn) \ V(Qx) … Qx and Qz are disjoint if and only if d(x,z) > 0, and are adjacent if and only if d(x,z) = 1." | MATCH. |
| [24] Kakutani 1941 (used directly in Prop 14.2, p. 124; also via Lemma 3.3) | Nonempty convex-valued correspondence with closed graph on the compact convex parameter polytope has a fixed point | COULD NOT FETCH. The Duke Math. J. DOI returns an Incapsula bot page; see /tmp/oaimath/171/refs/initial_b_kakutani/k.pdf, an HTML stub. Standard statement (from memory, not fetched): if S ⊂ ℝⁿ is nonempty compact convex and Φ: S → 2^S is upper semicontinuous with nonempty closed convex values, then x₀ ∈ Φ(x₀) for some x₀. A closed graph into a compact range is equivalent to usc with closed values. | COULD NOT FETCH; the use matches the standard statement. Hypotheses checked: finite-dimensional compact convex domain; π^out continuous and single-valued; argmax over the simplex is a nonempty convex face with closed graph. |
| [20] Hall 1935 (used via the p. 12 paragraph in Lemma 15.1, Prop 15.4) | Distinct representatives exist when \|S\| ≤ \|∪_{v∈S} supp p_v\| for all S | COULD NOT FETCH. The LMS/Wiley DOI returns a Cloudflare challenge; see refs/hall1935/hall.pdf, an HTML stub. Standard: a family of finite sets has an SDR iff every k of them have union ≥ k. | COULD NOT FETCH; the use is standard and the counting step on p. 12 is correct. |
| Hamming [21] (cited in §10.1; the same syndrome projection is reused in §14.1 without citation) | ψ(z) = z⊕e_{s(z)} has syndrome-zero image and fibres of size h | Not fetched (another seat's citation). I re-derived it directly: s(z⊕e_{s(z)}) = 0; ψ^{−1}(w) = {w⊕e_l : l ∈ ℤ₂^m}; this needs h to be a power of two, and h_i = q^M is one because q is dyadic. | Self-contained; correct. |

No other external result is invoked inside §13–15. Azuma / Hoeffding / "bounded-increment concentration" appear only as names on p. 120, applied to O(1)-bounded log increments, and they apply.

---

## 4. Parameter-dependency table (scope §13–15)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| A_c=200, P, R=P² | §12 (p. 111) | clock constants for B=5 | n^{−R} mass failures; P ≥ P_*(B=5) |
| u, L=⌈500R⌉, ξ, θ, C_* | §12 (pp. 109–111) | R; ξ<α2^{−10u−100}; θ(ξ,u); C_*(u,ξ,θ) | moments, clique count Δ_i = e^{C_*Q_i} |
| η_0, x_*, α, b_*=n^{−.96} | Cor 7.2, Cor 12.1 | earlier sections | (7.2), (12.1) |
| ι | p. 112 | ι < min(x_*,η_0,.01)/1000 | g ≤ n^{ι/2}; h_i, ℓ_i < n^ι |
| a_C | p. 112 | a_C < min(η_0,1)/10^6 | cluster size threshold Ne^{−q^{a_C}} |
| a_B | p. 112 | a_B ≪ a_C; a_B < x(ι/2), the (12.1) budget for slack ι/2 | bias size threshold Ne^{−g^{a_B}} |
| M_1 | p. 113 | 2C_*/√M_1 ≪ 10^{−3} | direct/cluster split; Δ_i ≤ e^{s_i} in direct mode |
| C_b | p. 113 | C_b > 100a_C/a_B + 100 | own-degree budget q^{C_b} |
| M_lo, c_q, M_hi | p. 113 | M_lo > C_b+100; c_q < 1/(20M_lo); M_hi ≫ M_lo+10/c_q | h_i ∈ [q^M, 2q^M); low/high split |
| ω | p. 113 | 5ωM_hi < a_C/100 | k_i, T_i |
| γ (Lemma 13.2) | p. 116 | γ < ι/(2M_hi) | h_i < n^ι |
| a | p. 113 | a = θ/100 | codegree 1/4+3a, s_i = ah_i/10^6 |
| ρ | p. 113 | log Vol(1000ρh) < (a/10^9)h | radii in §14–15 |
| K_B, A_0 | p. 113 | ≫ 10^6 R | high/low direct split; late classes |
| geometric b_0, b, a_g, ζ_g, θ_g, σ_g; λ=h^{10}; D=6 | p. 119 | ω (σ_g < ω/60 needed, see O3) | Lemma 3.8 on Q_h |
| K (bounded), Q_i (bounded) | p. 117 | M_1Q_0, a, c, a_B, a_C | bounded patch |
| Q_0 | p. 113, last | everything above, including u (allocation budget), a_B (log 8 slack), C_*, a | all "above threshold" estimates |
| c, c' | pp. 114–115 | structural (1/8; ≈1/2; .1/20); **independent of Q_0** (checked) | M_i lower bounds, S ≥ c'N |
| g, q, h_i, d_i, k_i, T_i, s_i, ℓ_i, Q_i (direct/cluster), mode/orientation/colour, mesh | per n, per patch | the residual pair at extraction | allowed to depend on n; all bounds on them hold uniformly in residual sets |

No cycle found. The constants ζ, δ in Lemma 13.2 depend on the subsequence limit γ', but only inside a contradiction argument against Cor 10.2, which is stated for every fixed rational choice. This is legitimate.

---

## 5. Verified line by line vs skimmed

**Verified line by line (arithmetic, inequality and hypothesis checks reproduced):**
- V13.1: Def 13.1; Lemma 13.2, both bounds, including the codegree formula, the Cor 10.2 witness parameters, and the legitimacy of the subsequence and rational choice.
- V13.2: the §13.2 parameter order; the trichotomy and boundary conventions (App. A p. 169).
- V13.3: Prop 13.3 in full:
  - direct extraction, including the 11/16 arithmetic and the size bound;
  - cluster extraction;
  - type selection;
  - dyadic rounding with the exact-sum argument;
  - prefix leaves (Kraft) and leaf role counts;
  - crossing-flip geometry, distinct leaves, and symmetry of crossing edges;
  - internal/bulk coordinate fitting;
  - the allocation budget.
- V13.4: Lemma 13.4 in full: approximant, own-degree trimming in all three modes, clique exclusion and Δ_i ≤ e^{s_i}, other-patch rows, codegree retention, ℓ¹-stability.
- V14.1: the syndrome geometry (fibres, multiplicity ≥ 2, site distance ≤ 6, O(h³) incidence).
- V14.2: (14.1) all three bounds; the masked-prior bound.
- V14.3: the likelihood ratio L_w ≤ e^{(log2−.06a)kh}𝒬; the posterior density; the joint cap; the B-set computation; the N max σ_v bound; the mean bound E σ_v ≤ K/M_i; the (14.3) union.
- V14.4: Prop 14.2, Kakutani hypotheses, cap preservation, the max π_i ≤ 11/M_i argument, the TV bound (structure only); Lemma 14.3.
- V14.5: the list-test mean −log4 + .7a (with O5).
- V15.1: Lemma 15.1 in full.
- V15.2: §15.1: both alarms' exponents, the LLL charges and degree.
- V15.3: Lemma 15.2.
- V15.4: §15.2, the H moment.
- V15.5: Prop 15.3: scale relations, capacity-certificate arithmetic, clock and Lemma 3.9 hypotheses.
- V15.6: Prop 15.4: caps (15.3), all repeat-cost exponents, the final union bound, normalisation and Hall, and that the embedding is complete. Every edge type (internal, bulk, crossing) is constrained, and labels are distinct across and within patches.
- App. A: the six rows Bounded / Low direct / High direct / Low cluster / High-small / High-large, and the "last six rows" paragraph, against the body. **No mismatches.**

**Skimmed or accepted on the paper's word (not reproduced):**
- S1: Prop 15.4's order of integration and comparison in the small-bin case: "Small-bin removal patterns", "Restoring the reference product" (O1).
- S2: Prop 15.3: that the certificate and star-constraint family satisfies Lemma 3.5's neighbour hypothesis exactly as joined (O2).
- S3: §14.2's eligibility, marking, search and union details ("each search has fewer than h of them except with probability exp(−h^{1+Ω(1)})"). The exponent count was checked: (#lists)^h·e^{−Ω(a²kh)}, with T log h = o(a²k). The marking and validity logic was not re-derived.
- S4: §14.2 "Local validity and fallback rules" and the translation-invariance of tie rules under syndrome-zero shifts. I checked only that the primitive experiment is invariant, giving the group-independence of π_i^0.
- S5: the proofs of Lemmas 3.5–3.10 and 12.2–12.6 themselves (other seats). I checked statements and hypotheses only.
- S6: everything in §16–18 that the low and bounded rows hand off to: late classes, fixed-constant failure absorption, and late-pool distinctness.

---

## 6. Verdict for this scope

- **§13: HOLDS AS READ.** Checked in full, including both items the brief flagged: one colour and one orientation chosen by pigeonhole (legitimate and in fact necessary), and power-of-two rounding (exact dyadic sum on a subcollection carrying > S/2, surplus unused).
- **§14: HOLDS AS READ** at the level of every stated inequality and hypothesis. The S3/S4 bookkeeping was not re-derived.
- **§15: HOLDS AS READ, with UNCLEAR at Prop 15.4's small-bin repeat-handling order (O1) and Prop 15.3's certificate LLL bookkeeping (O2).** These are compressed exposition, not demonstrated gaps; every exponent in them checks.
- **COULD NOT CHECK:** the primary sources of Kakutani [24] and Hall [20], which are behind publisher bot walls. Both are used in their standard forms.
- No step in scope uses a rate for C_n → ∞. The high modes use only C_n ≥ an absolute constant, plus N ≤ n2^n for union bounds and log N = O(n).
