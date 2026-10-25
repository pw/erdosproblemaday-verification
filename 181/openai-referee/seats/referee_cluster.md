# Referee report, seat "cluster": §10 (pp. 89–97), §11 (pp. 97–106), §12 (pp. 106–111), plus §1.3, Fig. 1, App. A rows "Full-dimensional clusters", "Linear-budget jump", "Deep discrepancy" and "Exhaustion and boundary conventions" (pp. 168–169)

Read from the PDF page images (paper.pdf, pp. 3–7, 10–26, 69, 79–80, 89–111, 112 (Def. 13.1 and Lemma 13.2, for the second use of Cor. 10.2), 166–169). I took the statements of §3 (Def. 3.1, Lemmas 3.2, 3.3, 3.5–3.10), Cor. 7.2, Cor. 8.2, Def. 9.1 and Prop. 9.2 as given; other seats are refereeing those. I re-derived every displayed inequality in pp. 89–111 by hand, and checked the borderline numerics numerically: the gain coefficient .02 − .01 log 2 + .0002a = .0131 > 0; log(1/.99) = .01005 < .1; 2·√(4η) = 4·10⁻⁴ < 1; log(1/.24) = 1.427 < 2; −log(1/2+2g) + .2g ≤ log 2 − 2g for g ≤ 10⁻²; and the external tilt tail exponent −2.4 + 2 = −.4.

**Bottom line: I found no FATAL error and no mathematical GAP in §10–12.** Every quantitative claim I re-derived is correct, usually with room to spare. The objections below are exposition-level: ambiguous definitions that hold under the reading the surrounding text forces, verifications left implicit, citation hygiene, and notation clashes. The real limitation of this report is the measure-theoretic "locality" bookkeeping (objection 11 and the skimmed list). I checked it at the level the paper states it and did not reconstruct it formally.

---

## 1. Objections

**1. Prop. 10.1, hypothesis (p. 89). COSMETIC.**
> "Assume (7.2) on the retained sets in both orientations."

Only one orientation is used. That is the first-side law μ_{i_z} (or μ conditioned on an exception set) tested against D̄_J on the second side (p. 91). The "both orientations" form is needed only so that Cor. 10.2 can be stated for both orientations, which follows by symmetry. Harmless over-hypothesis.

**2. Lemma 3.8 parameter check left implicit (p. 90). COSMETIC (exposition).**
> "For the height lemma's parameters ζ, σ, 1 − θ, a, unrelated to the cluster parameters here, take 8δ, σg, δ, 20δ, with 0 < σg ≪ δ. The sublinear-radius condition is satisfied …"

The paper does not display the required inequalities. I checked them all:
- Lemma 3.8 requires b₀ > a > ζ + σ + (1 − θ). Here 50δ > 20δ > 9δ + σ_g.
- It requires b > a + 4σ. Here 140δ > 20δ + 4σ_g.
- With ρ = 10δ and step bound D = 6, the sublinear-radius condition is b > b₀ + (D+1)ρ. Here 140δ > 50δ + 70δ = 120δ.
- 0 < b₀ < b < 1 (since δ < 1/2000), θ = 1 − δ > .9, and λ = n^{10} (J₀ = 10 > 2).
- H ≤ n^{1−8δ+σ_g}, so r + H = O(n^{1−7δ}).
- The fan bound uses 2n^b = 2n^{140δ} ≤ T = n^{141δ}.

Everything holds; the proof should simply say so.

**3. Selection weight w_{ℓ,c} in "From a prescribed list to the actual selection" (p. 93). UNCLEAR (exposition), but load-bearing.**
> "let w_{ℓ,c}(P_{z′}) be the supremum, over fixed legal eligibility sets, of the conditional activation-and-tie probability that this ID is selected on the queried slice's size and height gates. … At level 0 uniform eligible-active selection gives the pointwise bound w_{0,c} ≤ 1/(.99λ)."

"Legal eligibility set" can mean two things:
- Lemma 3.8's "required size" |E| ≥ λ/3. Under this reading the bound is 3/λ, the per-slice sum is ≤ 3 + o(1), and the product over m external slices is 3^m. That destroys the claim N max p̂_b ≤ e^{.1m}, which needs (1/.99 + o(1))^m.
- Sets meeting the ".99λ" size gate built into V_g (p. 92). Under this reading 1/(.99λ) is correct.

The paper's wording ("selected on the … size … gates", and V_g contains the .99λ condition) supports the second reading, and with it the claim holds:
- Σ_c Pr(c present) = λ exactly, so level 0 contributes 1/.99.
- Higher levels contribute Hλe^{−n^{c0}} by Lemma 3.8(ii), forced-center and sup-over-eligibility form.

**Fix:** define w as the supremum over eligibility assignments in which every consulted set has size ≥ .99λ. The constant .99 is load-bearing here (it is not slack), and the text should flag that.

**4. The mask bound carries a factor T+1, not O(1) (p. 93). COSMETIC.**
> "Choose a distribution of masks so these hypothetical means, for all t, are each bounded by O(T + 1)ν_{i_z} pointwise."

The separation argument proves exactly this:
- For prices c_t(y), discard labels with Σ_t c_t(y) > 10S. The cheap set has ν-mass ≥ .9.
- Clusters with cheap mass < 1/2 then have λ-mass ≤ .2, so the mask is legal.
- The cost is ≤ 10(T+1)S.

The factor T+1 = n^{141δ} is absorbed later as O(log(T+1)) in the e^{.1m} cap. Correct; noted only because a reader might expect an O(1)ν bound.

**5. Lemma 11.2: Kakutani applied directly, not through Lemma 3.3 (pp. 99–101). COSMETIC (exposition).**
> "Require it supported only on tags compatible with the input as listed. These responses are convex and have closed graph (cliques used strict inequalities), so Kakutani proves the claim."

Lemma 3.3's second assertion assumes output rules "fixed … independently of the profiles". Here the feasible output set depends on the input profile through a support restriction, so Lemma 3.3 does not apply verbatim. The direct Kakutani argument is correct:
- Each tag's compatibility set C_i = {p : tag i compatible with p} is closed. The conditions |m_x| ≤ 4b* and p{i′ : d_G(x; π_{i′}) > .8} ≤ η are linear in p and non-strict. "No s_c-clique with K_π > 8n^{−δ}" is a finite union, over the pairs of each candidate clique, of closed sets {K_π ≤ 8n^{−δ}}.
- So incompatibility is open, and if (p_n, q_n) → (p, q) with q_n ∈ R(p_n), then q_i = 0 for every i incompatible with p.
- Values are convex.
- Values are nonempty because the compatibility discards are uniformly small in p (< N e^{−n^{1−υ/4}}, N e^{−n^δ}, N e^{−n^δ}; all three bounds derived from (11.1) and Cor. 10.2 with p-independent thresholds). That leaves availability slack for price separation, with K fixed beforehand, as the last paragraph of p. 100 says.

Citation [24] is not repeated at this use.

**6. Lemma 3.3's first assertion applied to a subprobability (p. 99). COSMETIC.**
> "It is nonempty by availability and price separation."

The laws are (π_i, α_i), and α_i is a subprobability. Lemma 3.3 is stated for patch laws, which are probability laws. The price proof goes through verbatim for mass ≤ 1.

**7. §11 menu construction (p. 97). UNCLEAR, verified.**
> "Choose an available exponent h₀ < .01. Its surplus n^{−h₀} is much larger than g. After fixing a color along a subsequence, the columns of degree at least 1/2 + 2g have second-law mass at least cn^{−h₀}."

Implicit steps, all correct:
- H_L(.01,.01) = 0 holds because H_L† is a supremum of a nonnegative function that is nonincreasing in (x, α).
- The bias witness is absolute; take the color G in which d_G(μ,ν) − 1/2 ≥ n^{−h₀}.
- Since d_G(μ,y) ≤ 1, ν{d_G(μ,y) ≥ 1/2 + 2g} ≥ 2(n^{−h₀} − 2g) ≥ n^{−h₀}, so c = 1 works.
- Conditioning adds h₀ log n to the width, and .01n + h₀ log n + O(1) ≤ .011n.
- The color choice is a 2-member finite union (Lemma 3.2, "after passing to a subsequence"). This is legitimate inside a proof by contradiction.

**8. Lemma 12.3, first bullet (p. 107). COSMETIC.**
> "With one free label and the other labels fixed, the magnitude of any interaction involving it exceeds O_u(b*) with probability at most e^{−αn/3}."

This is a per-interaction bound. "Any" invites a reading over all interactions simultaneously, which would need an extra factor O_u(n). Lemma 12.4 does take that union explicitly ("The union over the O_u(n) interactions and Lemma 12.3 …"), so nothing breaks.

**9. Hamming citation (p. 89). COSMETIC.**
> "This uses the binary syndrome correction rule of Hamming's parity-check construction [21, Sections 3–4]. The index 0 is also a bit position, so exactly one bit is always flipped."

Hamming §3 gives the checking-number rule, where checking number 0 means "no error". The paper's variant, with index 0 a real coordinate that always gets flipped, is not in Hamming. Hamming §4 adds an overall parity position, which is a different device. The facts actually used are elementary and I verified them directly:
- u(s ⊕ e_l) = u(s) + l, so the projected syndrome is 0.
- The preimages of a zero-syndrome word c are exactly {c ⊕ e_l} (H′ of them).
- Across a residual edge one chunk changes in ≤ 3 coordinates, and that chunk always changes.
- Multiplicities are 2 (u ≠ 0), H′ (u = 0), or 1 (unit chunk).

**10. Uncited standard tools in scope. COSMETIC.**
- **Azuma–Hoeffding for bounded supermartingale increments**, p. 91: "their deviation below (−log 4 + .4a)k has probability exp(−Ω(a²k))". The increments are not independent, because q depends on the prefix J, so the martingale form is needed. It is valid: increments lie in [log .24, 0], conditional means are ≥ −log 4 + .7a, and the deviation is .3ak, giving exp(−2(.3ak)²/(k·1.43²)).
- **Chernoff bound** for position counts, p. 91.
- **Exponential Markov with e^x ≤ 1+(e−1)x**, p. 96.
- **Ramsey/Erdős–Szekeres bound** R(s,t) ≤ C(s+t−2, t−1), pp. 100, 103, 110.
- **Kakutani**, p. 100.
- **Jensen, Cauchy–Schwarz, Fubini.**

All are used correctly.

**11. Locality / primitive-domain bookkeeping (pp. 92, 96). UNCLEAR (not a found error).**
> "Thus a group calculation reads only tags, tuple and position fields, masks, activations and ties within special-coordinate distance 3 and residual distance r + 12H + 9. … Replacing a tuple only reevaluates the same list, marking, height and kernel functions on this fixed primitive domain; it does not initiate a recursive search through other eligibility rules."

Four steps rest on this "every rule is local" claim:
- independence of separated odd rows in Lemma 3.6 (p. 96);
- factorization of the even product means (p. 97);
- w-independence of the reference Q (p. 94);
- the recomputation of gates in L_w (p. 94).

I checked the distance arithmetic: 3 + 12H + 3 + 3 + r residual; 1 + 1 + 1 special. Lemma 3.8(i) says a long height reads bad statuses within 2DH = 12H, and a bad status reads the r-ball eligible set and the (r+D)-ball crowd. The maximal disjoint failed-list family at a group reads only that group's lists, its mask, and positions.

I did not formalize that the full pre-cluster history restricted to a domain is a measurable function of the primitive fields in that domain. The paper asserts this and does not prove it. It is plausible and consistent everywhere I checked, but it is the one structural claim in §10 that I verified only at the level of the paper's own description.

**12. Notation collisions. COSMETIC.** These are dangerous for a reader cross-referencing §3 and §9:
- **h**: internal dimension ⌊n^{.1}⌋ in §11, versus the bias exponents h, h₀, H in Def. 9.1 and the start of §11.
- **D**: step bound in Lemma 3.8, list 𝒟, cluster D, and D_x = d_G(x;π).
- **T**: fan bound in §10, T = S − E_πS in Lemma 11.3, T₀ on p. 99.
- **d**: n − m in §10, n − h in §11.
- **a**: codegree surplus n^{−δ}, a parameter in Lemma 3.8, and the functions a_x(y).
- **θ**: Lemma 3.8, §12 θ, clock θ₀.
- **m**: special bits, versus m_x.
- **ζ**: cluster atom exponent and Lemma 3.8's ζ (the paper flags this one).

**13. Appendix A, "Linear-budget jump" row (p. 168). COSMETIC.**
> "Reverse-orientation discrepancy n^{−.95} at widths (n^{1−υ/4}, n^{x₀})."

The row does not say which side carries which width. Against (11.1) it is: first side X width n^{1−υ/4}, second side Y width n^{x₀}. Consistent.

**No other inconsistency** between the text and App. A rows or Fig. 1 in my scope:
- δ < min(η₀, ζ, 1)/2000 and k(T+m) = O(n^{500δ}) match the text.
- The even bound e^{(log 2 − .01n^{−δ})n} matches.
- The available widths (n^{.01}, .011n), column surplus 2n^{−.01}, gain n^{.09} versus O(n^{.05}) + n^{.03} all match.
- For deep discrepancy: widths (αn, n^{x*}) in either order, α, x* < .01, b* = n^{−.96}, one-free tail e^{−αn/3}, two-free threshold n^{−1.03} with tail e^{−n^{.4}}, small width ≤ n^{x*/4} all match.

---

## 2. What each item in scope delivers, and the brief's questions (a)–(g)

**(a) Proposition 10.1 and Corollary 10.2.**

*Hypotheses, all used:*
- (7.2) is used for q(x) ≥ 1/4 − O(n^{−η₀}). The widths fit: D̄_J has width ≤ n^δ + O(1) + 2k(T+m) = o(n^{η₀}), and μ conditioned on an exception of mass ≥ e^{−n^{η₀}/2} has width ≤ n^δ + n^{η₀}/2.
- width(μ_i), width(ν_i) ≤ n^δ is used in the posterior cap (kn^δ = o(akn)), in the D̄_J width, and in N p̂_b ≤ e^{.1m}.
- Atoms ≤ e^{−n^ζ} are used in column-sum concentration (L* = n^{O(log n)}·2e^{−n^ζ+1.5k(T+m)} = e^{−Ω(n^ζ)}) and in the clock atom bound.
- Codegree ≥ 1/4 + a is used in E_x q(x) ≥ 1/4 + a, including the diagonal y = y′.

*Constants:* δ < min(η₀, ζ, 1)/2000 gives 500δ < η₀ and 500δ < ζ (both needed), and also m = o(an) and 140δ < 1. The exponents are m = n^{200δ}, k = n^{300δ}, T = n^{141δ}, a²k = n^{298δ} ≫ (m+T) log n, ak = n^{299δ}.

*§10.1 list test, re-derived:*
- A(J ∩ N(x)) = A(J)·q(x).
- D̄_J ≤ 4ν/A(J).
- Jensen gives q ≥ d_G(x; D̄_J)².
- With u₀ = 1/4 − Cn^{−η₀} and log v − log u₀ ≥ v − u₀, the clipped mean increment is ≥ −log 4 − O(n^{−η₀}) + a − O(e^{−n^{η₀}/2}) ≥ −log 4 + .7a.
- Azuma gives exp(−Ω(a²k)). External ratio: (1/4 − o(1))^k ≥ e^{−2k}. Absolute: .24^{k|𝒟|} ≥ e^{−2k|𝒟|}.

*§10.1 eligibility:*
- Maximal disjoint failed family ⇒ actual lists pass.
- L_n^n p_n^n = exp(−Ω(na²k)) beats the union over ≤ 2^n groups.
- Forbidden IDs per site: O(n³)·n·(T+m) = o(n^{10}).
- Fan ≤ 2n^b ≤ T.

*§10.2:*
- Pr_tilt{D(F)/D(F_{−c}) < t} ≤ t²A(F_{−c})/A(F), giving e^{−.24ak} (own), e^{−.4k} (external), e^{−k|𝒟|} (absolute), so h_F ≥ 1/2.
- p_𝒟 ≤ 2·4ν·e^{2k|𝒟|}.
- Masks: objection 4.
- N p̂_b ≤ n^{O(T)}(1/.99+o(1))^m O(T+1)e^{n^δ} < e^{.1m}; see objection 3.

*§10.3:*
- Likelihood ratio h_F^{−1}(A(F_{−c})/A(F))(D(F)/D(F_{−c}))^{2−j}.
- j ≥ 2 case: 2e^{k(j log 2 − .08aj − .24a)}. Singletons: ≤ 2e^{2k}, at most m+1 of them (m special plus ≤ 1 unit chunk).
- log(L_w/Q) ≤ (log 2 − .06a)kn.
- Lemma 3.7 with ε = e^{−.01akn} gives posterior ≤ N^{−k}e^{(log 2 − .04a)kn}.
- |B|/N ≤ e^{−(log 2 − .02a)n}.
- Pr(#heavy ≥ q) ≤ 2^k e^{(log 2−.04a)kn}(|B|/N)^q, with exponent gain akn·(.02 − .01 log 2 + .0002a) > 0.
- Light mass ≥ c₆a, so N max p_v^X ≤ e^{(log 2 − .01a)n}.
- The mean identity ∫Z·(posterior) = μ^{⊗k}·(gate prob) ≤ μ^{⊗k} gives N p̂_v^X ≤ poly(n)e^{n^δ}/(c₆a) < e^{.1m}.
- Tag profiles: Lemma 3.3, second assertion; the hypotheses hold because the mask lookups are fixed before the profiles and rows are supported in their own patch.
- Tag-level Lemma 3.6: f = m^{O(1)}2^{−m}, L = e^{.1m}.
- Pre-cluster odd rows: f_res ≤ 2^{−n}e^{o(an)}, L = e^{o(n)}.
- Cluster column sums ≤ θ₀ via exponential Markov.
- Clock lemma with B = 2: atoms e^{−Ω(n^ζ)} ≤ n^{−A*}, columns ≤ θ₀, log g = O(n), no predicates.
- Transfer: clock comparison at fixed clusters, then drop the nonlocal cluster indicator, then integrate clusters. This is the reference law of L_w, so the predictive failures union to 2^n·poly·e^{−.01akn} = o(1).
- Even column sums: f_res·n·e^{(log 2−.01a)n} = o(1).
- Embedding: Hall's condition holds and every edge is in G, since the posterior is supported on tuples whose entries hit all n odd neighbours, including special ones (v's center is in every neighbour group's list).

*Cor. 10.2:*
- The list is countable: rational (ζ, δ) with δ < min(η₀, ζ, 1)/2000, × 2 orientations × 2 colors.
- The witness is intrinsic to its supports (widths are normalized by the original N; codegree depends only on μ and G).
- "Available" yields a cube by Prop. 10.1; (7.2) persists under further discards. So each property is eventually absent, and absence persists under every further removal.
- **Second use (Lemma 13.2, p. 112), checked against Cor. 10.2's hypotheses.** The paper needs γ′a_C < δ < min(η₀, ζ, 1)/2000 with 0 < ζ < γ′, using a_C < min(η₀,1)/10⁶. A rational δ exists: take ζ = γ′/2; then γ′min(η₀,1)/10⁶ < min(η₀, γ′/2)/2000. Bins of size ≥ e^{n^{γ′−o(1)}} meet the atom cap e^{−n^ζ}. ζ and δ are fixed rationals chosen after the limit point γ′, so countability is respected. The arrow is consistent.

**(b) Proposition 11.1.**

*Where (11.1) comes from.* It is **not** from Cor. 8.2 or Cor. 12.1. It comes from the case hypothesis "H† ≥ 1 in the reversed orientation", via Def. 9.1:
- G(x) := lim_{y↑1} H_rev(x,y) = inf_y H_rev(x,y) is nonincreasing in x, and sup_x G = H†_rev ≥ 1.
- So there is a rational x₀ with H_rev(x₀, y) > .95 for all y < 1, in particular at the rational 1 − υ/4.
- .95 < H_rev means the bias property at rational exponent .95 is not available, so it is stabilized-absent.
- Orientation: π on Y with width n^{x₀}, σ on X with width n^{1−υ/4}.

This is not circular. Prop. 10.1 uses only (7.2); §11 uses Def. 9.1 plus Cor. 10.2 at the fixed rational pair ζ = 1/100, δ < min(η₀, .01)/2000. Prop. 9.2 is used only in Cor. 11.4. The order matches Fig. 1.

*Slice experiment, re-derived:*
- Row tests via Lemma 3.7: Pr ≤ e^{−kh} + h e^{−.2gk}.
- Passing rows have width ≤ .011n + n^{.3}(1 − log(1/2+2g)) ≤ .02n.
- Fixing y₀ by averaging is justified by translation symmetry.
- σ_v has mass 1 except with probability exp(−Ω(gk)), from:
  - the neighbour ratio (1/2+2g)^{−k}e^{.2gk} ≤ e^{(log 2 − 2g)k};
  - Lemma 3.7 with ε = e^{−.5gkh};
  - posterior cap N^{−k}e^{(log 2 − g)kh}, using n^{.01} = o(gh);
  - hence T₀ ≥ N e^{−(log 2−g)h}, which exceeds the cutoff N e^{−(log 2−.5g)h}.
- The hidden W_v influences the neighbours' tests, and the paper does recompute them ("Recompute both rows and tests at (W_{−v}, w)").

*Lemma 11.2, all three discards re-derived:*
1. **|m_x| > 4b*:** < N e^{−n^{1−υ/4}} by (11.1) against π, which has width ≤ log K.
2. **Clique union V:** a reversed-orientation cluster witness with first law π, clusters uniform on cliques, codegree (1 + m_x + m_{x′} + K)/4 ≥ 1/4 + 2n^{−δ} − 2b* ≥ 1/4 + n^{−δ}, and atom 1/s_c ≤ e^{−n^ζ}.
3. **Set U of η-violators:**
   - E_i D_i(x)² ≥ 1/4 + cη (c ≈ .08).
   - A p-fraction ≥ cη/1.5 of tags has ‖v_i‖² ≥ 1/4 + cη/2.
   - Each such tag has a projection mass ≥ c′.
   - Independence number < t₀ when c‴ < c″ + c″².
   - Collision bound r₀²e^{.02n}/N ≤ e^{.08n}2^{−n} → 0.
   - Ramsey packing leaves ≤ s_c^{O(1)} = e^{O(n^{.01})} ≪ r₀ = e^{.03n}.
   - The aggregate is ≤ (2C(1+o(1))/p(S))π, so its width is O(1).
   - This gives an original-orientation cluster witness.
4. **Kakutani:** objection 5.

*Lemma 11.3, all steps re-derived:*
- **Identity:** E(Z−1)^u = ∫Σ_I(−1)^{u−|I|}(∫∏_{I}(1+a)dπ)^d.
- **One-free:** M_J = ⟨f_x, H₀ − E H₀⟩/(1+m_x), with the offset-test reduction to (11.1) and conditioned width ≤ O(h) + n^{1−υ/4}/2.
- **Two-free:**
  - ρ_x has width O(h + n^{.4}) and ‖E_{ρ_x}a_z‖ = O(b*).
  - E‖S‖² = O(t + t²b*²), with t = n^{.25}.
  - Fubini gives a set q of width O(n^{.65}) < n^{1−υ/4}.
  - The identity E_q⟨a_x, S⟩ = c_q E_{q̃}⟨f_x, T⟩ holds (checked: ⟨a_x, S⟩ = r_x⟨f_x, S − E S⟩).
  - The π_± with equal normalizers give O(b*√t) = O(n^{−.825}) < n^{−.78}.
- **Mean:** E M_J² ≤ (C b*)^{r} + C e^{−Ω(n^{x₀})}, and .95/2 > .4.
- **Counting:** t₀ = O(n^{2υ}) since δ = 4υ; log C(s_c + t₀, t₀) = O(n^{.01+2υ}) < n^{.03}.
- **Exponential weights:** 2^u n^{.06} ≪ n^{.4} and 2^u n^{1−υ} ≪ n^{1−υ/4}.
- **Expansion:** coefficients vanish unless the selected interactions cover [u]; the tail is (2^u n^{−.03})^L; the main term is O(n^{L − .4u/L}).
- **Peeling:** |B_R|·max σ·max D^{−d} ≤ (2^n/N)e^{−.5gh + O(n^{.05}) + n^{.03}}, with gh = n^{.09}.

*§11.3:*
- Tag conditions: Markov on Lemma 11.3 with 4P. The union N(4η)^{(n−h)/2} uses N ≤ n2^n.
- Lemma 3.5 at the tag stage (dependency O(n²)) and the tuple stage (O(n⁴)), with charges n^{−2P} and n^{−P}.
- A_s cap e^{.02n}. B_s ≤ 2^h·.8^{d/2}·2^d e^{O(n^{.05})} = 2^n e^{−Ω(n)}.
- E B_s ≤ K: each neighbour ratio integrates to 1, and Σ p_i Nα_i ≤ K.
- Clock lemma with B = 4: atoms e^{.02n}/N < n^{−A*}; predicates read n rows and each row is in n predicates.
- Even cap N M_v ≤ 2^n e^{−.5gh + O(n^{.05})} ≤ 2^n e^{−.4gh}.
- Product means = B_s, because σ_v (internal) is independent of the outer labels (distinct slices, raw law π_{i(s^j)}).
- Normalizing (mass ≥ 1/2) at most doubles column sums. Hall's condition holds.

*Cor. 11.4:* H_L† ∈ {0} is excluded by Prop. 11.1 and (0,1) by Prop. 9.2, so H_L† ≥ 1. Take rational h₀ ∈ (1−ε, 1); since H_L† is a supremum there are rational (x, α) with H_L(x,α) > h₀; stabilized absence gives the bound. Correct.

**(c) Corollary 12.1, exact quantifiers.**

For the fixed stabilized sequence there are constants 0 < x* < .01 and 0 < α < .01, depending on the sequence but not on n, and an n₀, such that for all n ≥ n₀ along the subsequence, every pair of laws on the retained sides, with the first side's law of width ≤ αn and the other's ≤ n^{x*} (either side), and either color, satisfies |d_G − 1/2| ≤ n^{−.96}.

It follows from Cor. 11.4 with ε = .04, taking the minimum over the two orientations (monotonicity) and shrinking below .01. "Taking strictly smaller error exponents" in App. A means you get n^{−h₀} for every h₀ < 1, never n^{−1}. Consistent: no conclusion at the infimum is used. Persistence under later discards and subsequences holds because widths are normalized by the original N.

**(d) What Lemmas 12.2–12.6 deliver.** Setting: d ≤ n, π_l of width ≤ n^{x*/4}, τ of width ≤ n^{x*/4}, |D_{π_l} − 1/2| = O(b*) on supp τ.
- **12.2:** the identity (12.2), with singleton interactions zero. Correct.
- **12.3, for fixed u:**
  - (i) per (l, J), with the others fixed: Pr_x(|M_{l,J}| > C_u b*) ≤ e^{−αn/3}. Also a gated version, with the mass of (gate ∩ exception) bounded, never divided.
  - (ii) Pr_{x,z}(|M_{l,J}| > n^{−1.03}) ≤ e^{−n^{.4}}.
  - (i) and (ii) also hold for K_{π_l}(x,z) without the degree assumption.
  - (iii) E|M_{l,J}| ≤ n^{−.4|J|}.
  - Re-derived: widths n^{x*/4} + αn/3 < αn; ρ_x width O(n^{.4}) < αn; the q-set has width O(n^{.65}); Cauchy–Schwarz gives O(b*√t) = n^{−.835} < n^{−.78}; .96/2 > .4.
- **12.4:** with R = P², L = ⌈500R⌉, even u > 10L², ξ < α2^{−10u−100}: |∫_{w≤2ξ}Φ_u dτ^{⊗u}| ≤ n^{−3R}, and each positive product term, for every subtuple, has bounded integral on {w ≤ 2ξ}. Re-derived:
  - O_u(n)e^{2^u n^{.06} − n^{.4}};
  - O_u(n)e^{2^{u+1}ξn − αn/3};
  - tail (2^u n^{−.03})^{L} ≤ n^{−15R+o(1)};
  - main term n^{L − .4u/L} ≤ n^{−3L}.
- **12.5 (homogeneous π):**
  - If there is no ⌈e^Q⌉-clique with K_π > 3θ, then the number of extensions to an interaction > ξ is ≤ e^{C*Q}, and #{z : |K_π(x,z)| > ξ} ≤ e^{C*Q}, with t₀ = t₀(ξ,u) and C* chosen after (u, ξ, θ).
  - If in addition max τ D^{−d} e^{C*Q} ≤ Γ < 1, the large-interaction contribution is O_u(Γ), and Pr(Z < 1/2) ≤ 2^u(n^{−3R} + C_uΓ).
  - The hypothesis (no e^Q-clique) is *not* supplied by Cor. 10.2 when Q is a fixed constant. It must come from the residual-scale argument in §13 (out of my scope).
- **12.6:** for a uniform small-width first set and ≤ exp(o(n^{.2})) small-width second laws, removing an o(1) fraction gives (12.3) for every kept x. The interpolated version uses thresholds n^{−1.02}, 2ξ, weight 100n and e^{−n^{.19}}, under an ℓ¹-mesh of n^{−3}.
  - Re-derived: |K_π − K_π′| ≤ ‖π − π′‖₁, e^{100n·n^{−3}} = e^{100n^{−2}}, 100 ≤ 150, and the union e^{o(n^{.2})}·e^{−cn^{.4}+n^{.2}} = o(1).
  - Note: later sections must keep the mesh-point count ≤ exp(o(n^{.2})). Not checked here.

**(e) Applications of the §3 lemmas in scope.**

| Lemma | Page | Use | Hypotheses |
|---|---|---|---|
| 3.2 | 89 | finite menu | ✓ |
| 3.2 | 97 | color fixing (2-member union) | ✓ |
| 3.2 | 97 | Cor. 10.2, countable rational list | ✓ |
| 3.3 (2nd) | 95–96 | tag profiles: players = 2^m slices, finite actions, output rule fixed (mask lookups fixed first), one-slice feasibility by price separation since rows are supported on own patch | ✓ |
| 3.3 (1st) | 99 | nonemptiness, with a subprobability | ✓ (obj. 6) |
| Kakutani (direct) | 100 | Lemma 11.2 | ✓ (obj. 5) |
| 3.5 | 105 | tag stage: iid tags, dependency O(n²), charges n^{−2P} | ✓ |
| 3.5 | 105 | tuple stage: independent W, scope full-cube distance 2, O(n⁴), charges n^{−P} | ✓ |
| 3.5 comparison | 105–106 | removing O(n³), O(n⁵) constraints touching ≤ n scopes, cost (1 − 2n^{−P})^{−O(n⁵)} = 1 + o(1) | ✓ |
| 3.6 | 96 | tag level: L = e^{.1m}, f = m^{O(1)}2^{−m}, K = 1 | ✓ |
| 3.6 | 96 | pre-cluster odd: L = e^{o(n)}, f_res | ✓ |
| 3.6 | 97 | even: L = e^{(log 2−.01a)n}, f_res, K = 1+o(1) | ✓ |
| 3.6 | 105 | outer words: L = 2^n e^{−cn}, f = n^{O(1)}2^{−(n−h)} | ✓ |
| 3.6 | 105 | odd: L = e^{.02n}, f = n^{O(1)}2^{−n} | ✓ |
| 3.6 | 106 | even: L = 2^n e^{−.4gh} | ✓ |
| 3.7 | 95 | predictive test; Q a probability independent of w; gate recomputed with w | ✓ |
| 3.7 | 98 | row tests: reference μ^{⊗kh}, deletion with posterior as prior | ✓ |
| 3.7 | 98–99 | σ_v common neighbours: Q = product of deletion posteriors; recomputation done | ✓ |
| 3.8 | 90 | parameter constraints | ✓ (obj. 2) |
| 3.8 | 92 | (i) on eligibility sizes ≥ .99λ ≥ λ/3; eligibility independent of activations | ✓ |
| 3.8 | 93 | (ii) forced-center plus sup-over-eligibility form, and the 3/λ level-0 selection bound sharpened to 1/(.99λ) | ✓ (obj. 3) |
| 3.10 | 96 | B = 2, no predicates | ✓ |
| 3.10 | 106 | B = 4 | ✓ |

Lemma 3.9 is not used in scope. The hidden tuple's influence on selection is explicitly recomputed in L_w (p. 94) and in F_w (p. 98), as §1.3 promises.

**Phrases "same / similarly / again" in scope.** A grep for same / similarly / as before / as in / again / analogous gives about 25 hits in pp. 89–111. I checked each one; none hides a hard step, and most are wording (e.g. "the same cap holds"). "The same two assertions hold for K_{π_l}" (p. 107) is proved on p. 108. "At retained separated rows, first make the same clock comparison" (p. 96) names the order of operations.

**(f) Rates.**

*N/2^n → ∞ enters* only as o(1) column sums:
- Lemma 3.6 thresholds give Σ ≤ M·2^{n−1}/N;
- the clock condition columns ≤ θ₀;
- 2^n/N ≤ 1 in Lemma 11.3;
- e^{.02n}/N < n^{−A*};
- e^{.08n}/N → 0 in Lemma 11.2.

**No rate is used anywhere in scope.** Every cap L, near fraction f and Markov threshold is independent of C_n.

*N ≤ n2^n (equivalently log N = O(n)) enters* in:
- every Lemma 3.6 "union over labels" (pp. 96, 97, 105, 106);
- the clock lemma's log g = O(n) (pp. 96, 106);
- the second tag condition, where N(4η)^{(n−h)/2} needs N ≤ e^{cn} with c < log(1/(2·10⁻⁴)), which is satisfied.

*Sharpest budgets.*
- **Width .011n:** the real constraint is e^{.02n} ≪ 2^n (log 2 ≈ .69), so there is huge slack (r₀ = e^{.03n}, collisions e^{.08n}/N).
- **Deep error n^{−.96}** needs b* = o(n^{−.94}) (one-free threshold below n^{−1+.06}), b*√t < t n^{−1.03} (that is, b* < n^{−.905}), and √b* ≤ n^{−.4}. All hold with margin.
- **§11 error n^{−.95}:** the binding constraint is n·b* = n^{.05} ≪ gh = n^{.09} (and the extension count n^{.03} ≪ n^{.09}). It holds.

**(g) Citations:** see §3 below.

---

## 3. Citation table (scope)

| Cited result | What the paper says it gives | Source (version read), quote | Verdict |
|---|---|---|---|
| Hamming [21, §§3–4] (BSTJ 29 (1950) 147–160; read the scanned journal copy via archive.org, bstj29-2-147) | Syndrome u(s) = Σ l·s_l; s ↦ s ⊕ e_{u(s)} lands on syndrome 0; a zero-syndrome word has exactly H′ preimages; index 0 also a bit position | §3: "We shall require that this checking number give the position of any single error, with the zero value meaning no error in the symbol"; Table II: first check over positions 1, 3, 5, 7, …. §4 adds "one more position" (overall parity). | MATCH for the syndrome rule. The index-0-as-flipped-bit variant is the paper's own, verified directly (obj. 9). |
| Kakutani [24] (Duke Math. J. 8 (1941)), used directly in Lemma 11.2 without the number | Fixed point for a closed-graph, nonempty, convex-valued correspondence on a compact convex set in finite dimension | COULD NOT FETCH (Project Euclid paywall; the file left in refs/kakutani by another seat is JavaScript, not the paper). Standard statement: an upper-semicontinuous map from a closed simplex to its nonempty closed convex subsets has a fixed point; the corollary extends to bounded closed convex subsets of Euclidean space. | COULD NOT FETCH (statement standard; usage matches it) |
| Uncited: Azuma–Hoeffding (bounded martingale differences), p. 91 | exp(−Ω(a²k)) deviation for clipped log increments | Azuma 1967 (Tohoku Math. J. 19, J-STAGE PDF, read from page images), Remark 1: "If (x_n) is a sequence of martingale differences such that \|x_n\| ≤ K_n a.s. for all n, then … E{exp(tx_n) \| 𝔄_{n−1}} ≤ cosh(tK_n) ≤ exp(t²K_n²/2)"; iterating as in (2.4) gives the Chernoff bound. Applied to X_j − E[X_j \| past], with \|·\| ≤ 1.43. | MATCH (uncited at this use) |
| Uncited: Erdős–Szekeres Ramsey bound, pp. 100, 103, 110 | R(s,t) ≤ C(s+t−2, t−1) | Standard | MATCH |
| Finner [11] | Not used in §10–12 (cited on p. 87, §9) | n/a | out of scope |

---

## 4. Parameter-dependency table (scope)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| η₀ | Cor. 7.2 | sequence | δ bound; (7.2) in §10.1, §13 |
| ζ, δ (rational) | Prop. 10.1 / Cor. 10.2 (countable list); §11: ζ = 1/100 | η₀ | m, k, T, a = n^{−δ}; Lemma 3.8 parameters |
| m = n^{200δ}, k = n^{300δ}, T = n^{141δ} | p. 89 | δ (n-dependent sizes, fixed exponents) | all of §10 |
| Lemma 3.8: ζ_h = 8δ, σ_g ≪ δ, 1−θ = δ, a_h = 20δ, b₀ = 50δ, b = 140δ, ρ = 10δ, D = 6, λ = n^{10} | p. 90 | δ | heights, fan, c₀ |
| c₅ (absolute) | p. 90 | — | list-failure tail |
| c₆ (absolute) | p. 95 | — | light mass |
| κ (menu tolerance) | Lemma 3.2 menu | sequence | K = 4/κ (tag balance), then Lemma 3.6 threshold M |
| θ₀, A*, P* | Lemma 3.10 with B = 2 (§10), B = 4 (§11) | B | clock |
| x₀ (rational) | p. 97, from H†_rev ≥ 1 | sequence, δ (through υ = δ/4) | (11.1) |
| h₀ < .01 (rational) | p. 97, from H_L(.01, .01) = 0 | sequence | color/menu |
| g = n^{−.01}, h = n^{.1}, k = n^{.2}, b* = n^{−.95}, s_c = e^{n^{.01}}, υ = δ/4 | p. 97–98 | fixed exponents; δ | §11 |
| y₀(i) | p. 98 | tag i (deterministic choice per n) | slice law |
| η = 10⁻⁸, c, c′, c″, c‴, t₀, C | Lemma 11.2 | absolute (c′… from η) | compatibility |
| K (balance, §11) | Lemma 11.2, fixed before the profile domain | κ, compatibility slack | (11.2), E A_s, E B_s ≤ K |
| P | §11.3, p. 104 | Lemma 3.10 (B = 4) and dependency exponents | tag/tuple avoidance, Lemma 11.3 with 4P |
| u, L | Lemma 11.3 | P | moment |
| x*, α | Cor. 12.1 | sequence (H_L), ε = .04 | (12.1); ξ |
| A_c = 200, then P ≥ (clock, B = 5), then R = P², L = ⌈500R⌉, u > 10L², ξ < α2^{−10u−100}, θ(ξ,u), t₀(ξ,u), C*(u,ξ,θ) | p. 107, 109, 111 | in that order | Lemmas 12.4–12.6 and later sections |

No cycle. No constant depends on n, the removed sets or the witness where uniformity is claimed. Several constants (x₀, h₀, x*, α, ξ) depend on the fixed counterexample sequence; that is legitimate, since the sequence is fixed once (p. 10) and these are fixed before n → ∞.

---

## 5. Verified line by line vs. skimmed

**Verified line by line (re-derived, including arithmetic):**
- Prop. 10.1:
  - Hamming projection facts and multiplicities; distance ≤ 6; fiber n^{O(log n)}.
  - Lemma 3.8 parameter constraints; fan ≤ T.
  - The whole list-test argument (10.1); eligibility and maximal-family logic; L_n^n p_n^n; o(λ) forbidden.
  - Tilt tail and h_F ≥ 1/2; p_𝒟 ≤ 8e^{2k(T+m)}ν; mask separation; external-selection sum; e^{.1m} cap.
  - Likelihood-ratio formula and the (10.2) arithmetic; Lemma 3.7 predictive step; posterior cap.
  - B and light-coordinate exponent; even cap; mean identity for p̂_v^X.
  - Exponential-Markov column bound; clock hypotheses; all near-fraction × cap products.
  - The edge/Hall conclusion.
- Cor. 10.2, including its second use in Lemma 13.2.
- (11.1) derivation from Def. 9.1; H_L(.01,.01) = 0; the menu.
- The slice experiment (row tests, widths, σ_v common-neighbour claim).
- Lemma 11.2: all three discard arguments and the Kakutani closed graph.
- Lemma 11.3: every paragraph.
- §11.3: tag and tuple conditions, A_s/B_s caps and means, clock hypotheses, even cap, product means, normalization.
- Cor. 11.4 and Cor. 12.1 quantifiers.
- Lemmas 12.2–12.6: every inequality.
- App. A rows and the exhaustion paragraph against the text; Fig. 1 arrows (10 → 11, 10 → 13, 8–9 → 11–12).

**Only checked at the level the paper states it (skimmed in the formal sense):**
- That every pre-cluster rule is a measurable function of the primitive fields in the declared domain (obj. 11), and hence the exact independence used in Lemma 3.6 at separated roles. Distance arithmetic checked; formal measurability not reconstructed.
- The "stop and continue with fixed good increments" construction in the list test (standard stopping; accepted).
- Translation-symmetry claims in §11 (easy; accepted).
- Internal proofs of the §3 lemmas (other seats).
- The precise definition of "reference sampling law" at invalid groups ("independent local defaults"). Only its monotone use (upper bounds) is needed, and I checked that.

---

## 6. Verdict for scope

**HOLDS AS READ** for §10 (Prop. 10.1, Cor. 10.2), §11 (Prop. 11.1, Lemmas 11.2–11.3, Cor. 11.4) and §12 (Cor. 12.1, Lemmas 12.2–12.6), and for the App. A rows, the exhaustion paragraph and the Fig. 1 dependencies in scope.

There is no mathematical gap. The exposition issues are objections 1–13. Two need attention:
- **Objection 3:** the w_{ℓ,c} supremum must be read with the .99λ size gate, or the e^{.1m} cap fails.
- **Objection 11:** the locality and measurability of the pre-cluster history is asserted, not proved. It is the structural claim most worth checking in the Lean.

**COULD NOT CHECK:** the Kakutani 1941 source text (paywalled; standard statement used).
