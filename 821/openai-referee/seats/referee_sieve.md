# Referee report — seat `sieve` — §7 (pp. 53–65), §8 (pp. 65–66), and Theorem 1.2 ⇒ Theorem 1.1

Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026), /tmp/oaimath/011/paper.pdf.
Read from the rendered PDF pages 53–66 (all displayed formulas checked against the images, not the text extraction), plus the inputs §7 calls: Lemma 2.5, Theorem 2.2, Theorem 2.3, Corollary 2.4, Lemma 2.9 (with proof), Definition 3.1, the §4/§5 group preambles, the §6.1 hypotheses and statement of Theorem 6.1, Remark 6.2.

**Bottom line for this seat.** I could not find a sentence in §7–§8 where the argument fails. Assuming Theorem 6.1 (Type II), and taking Lemma 2.9 and Theorems 2.2/2.3 as inputs (I checked all three; see below), §7 is a correct Harman/Friedlander–Iwaniec-style extraction of primes, and §8 is a correct Erdős–Pomerance product-and-pigeonhole step. Every quantity that gets subtracted is bounded in the right direction. The Buchstab identity (7.18) is exact (re-derived, and checked numerically to 1e-16). The order of choices in §7.7 has no cycle. All the parity-breaking content of Theorem 1.2 sits in Theorem 6.1, which is outside my scope. §7 is a pure deduction from it and adds no risk of its own. All objections below are COSMETIC or UNCLEAR. None is a FATAL or a GAP.

---

## 1. Objections

**O1 — §7.7(ii), p. 64. COSMETIC (exposition).**
> "(ii) Fix κ ∈ (0, 1/50) so small that C_bal κ < 𝔖/4. This is possible because the constant in (7.31) is independent of the gap."

In §7.6, "the gap" is the θ-gap of (7.24) ("Choose a fixed large index j′ and then θ in the gap …"). The paper says C_bal depends on exactly that: "The constant C_bal depends only on δ, r0, Ψ, j′, θ and the fixed P-group geometry" (p. 64). So read literally, the sentence contradicts (7.31). What is meant, and what is true, is "independent of κ". Since θ is fixed in step (i), before κ, the order is fine. Fix: replace "the gap" with "κ".

**O2 — §1 p. 2 and §8 p. 65, citation of Pomerance [19, Theorem B]. COSMETIC (exposition, not load-bearing).**
> "Pomerance states the relevant transfer explicitly in [19, Theorem B]."

Pomerance's Theorem B (quoted in the citation table) assumes a *positive proportion*, Π(x, x^u) > επ(x), and concludes N(m) > m^{1−u}. Theorem 1.2 supplies only x^{1−o(1)}, so Theorem B does not apply as stated. This does not matter, because §8 gives its own proof, which needs only "more than X^{1−δ} primes". I checked that proof line by line (§3 below). It loses 3δ+o(1) < ε in the exponent, where Erdős's argument loses δ. Fix: say "compare [19, Theorem B]", or note that its hypothesis is stronger than what is available.

**O3 — cross-reference labels throughout §7–8. COSMETIC.**
Lemma 2.9 is cited as "Theorem 2.9" (pp. 56, 58, 60, 61, 63). Proposition 7.1 appears as "Theorem 7.1" (p. 56), Proposition 7.2 as "Theorem 7.2" (p. 56), Lemma 2.5 as "Theorem 2.5" (p. 56), Lemma 7.3 as "Theorem 7.3" (pp. 58, 61, 62), Lemma 7.4 as "Theorem 7.4" (p. 61), and Lemma 8.1 as "Theorem 8.1" (p. 66). These are hyperref artefacts. Each target exists and says what the citing sentence needs.

**O4 — Lemma 7.3 proof, p. 58. COSMETIC.**
> "Intersecting the test interval in (5.4) with K leaves at most two partial cells; their combined harmonic mass is O(L^{−S} + x^{−b1/4})."

By (7.13), a cell's W-rough count carries O(D_W) with D_W = x^{o(1)}. The partial-cell mass is therefore O(L^{−S} + x^{−b1/4+o(1)}). This is harmless, since the bound only needs to be ≪ L^{−B}.

**O5 — symbol reuse in §7. COSMETIC.**
- "a" means the Prop 7.2 exponent ("x^a ≪ P, U ≪ x^{1−a}") and also the group exponent a = 1/10.
- "h" means the modulus cofactor (d = hf) and also the sieve parameter in the same subsection.
- "D" means the Type I saving exponent in (7.8), the sieve level D = x^{10θ} in (7.28), and the §3 shift product.
- "θ" means the §7.6 gap value and also §6.2's θ = L^{−d}.
- "C" is overloaded throughout.

I traced each use and found no place where two meanings get confused.

**O6 — §7.5, p. 61. UNCLEAR, resolvable.**
> "Apply Theorem 6.1 with α = I_γ − B_γ restricted to each actual cofactor range, and β the prime indicator restricted to its bin and dyad."

"Actual cofactor range" is never defined. It has to be an interval inside one dyad, because that is what Lemma 7.3 covers ("uniformly for every interval K inside a dyad in the stated factor ranges"). The dyad m ∈ [U, 2U) is enough here. With N_u ∈ [2x, 4x+1] and p ∈ bin ∩ [V, 2V), no further restriction on m is needed, so the hypotheses match exactly. Theorem 6.1 states the matching requirement: "the sequence to which the discrepancy hypothesis is applied includes the actual restriction m ≍ U and any additional interval restriction on m." Fix: write "restricted to m ∈ [U, 2U)".

**O7 — pointer for the typeII/whole seats, not an objection in my scope.**
§7 uses Theorem 6.1 at its most unbalanced end. In §7.5 the *arbitrary* coefficient β sits on primes p as small as x^{b1}, and the discrepancy coefficient α sits on cofactors as large as 5x^{1−b1}. Here b* = b1/3, and b1 has to be very small. (7.22) needs O(b1^{−1}e^{−c/b1}) < 2/5, and h = 2⌊1/(40b1)⌋ gives c ≈ 1/20, so, with an unknown implied constant, b1 is plausibly of order 1/100–1/200, i.e. b* ≈ 0.002–0.003. The exceptional slot then has η* < b*/4 ≈ 0.0005–0.0008 ((7.10)). Theorem 6.1 claims every fixed b* > 0 ("Fix D*, b* > 0, and C > 0, and require η* < b*/4"), so §7 is consistent with its statement. Anyone checking Theorem 6.1 should test it in exactly this regime.

I found nothing else. In particular, none of the brief's direction-sensitive items is reversed, and I found no parameter cycle (§4 below).

---

## 2. The most important question: the subtraction (§7.5–§7.6), re-derived

Notation: S_0 := Σ_{P⁻(N_u)>x^{b1}} A(u)Ψ(u/x). Every N_u counted in S_0 is (i) prime, (ii) composite with least prime p ∈ (x^{b1}, x^{1/2−κ}], or (iii) composite with P⁻(N_u) > x^{1/2−κ}.

**Lower bound for S_0 — (7.11) is a LOWER bound. ✓**
- Lemma 2.9 applies with objects u, weight A(u)Ψ(u/x), and bad events p | N_u for odd p ≤ z = x^{b1}. The weight on {d | N_u} is X_A g(d) + r(d), with g = 1/φ multiplicative, g(p) = 1/(p−1) ≤ 1/2, and Σ_{w<p≤w²} g(p) bounded.
- (2.5) is two-sided. Its lower side gives S_0 ≥ X_A V_1(x^{b1})(1 − O(e^{−h})) − O(Σ_{d≤z^{4h+2}}|r(d)|).
- With h = 2⌊1/(40b1)⌋: 4h+2 ≤ 1/(5b1) + 2, so b1(4h+2) ≤ 1/5 + 2b1 < 0.49 < ϑ = 1/2 − κ/2 for κ < 1/50 and b1 < 0.145.
- (7.8) bounds the remainder by xL^{−D} + X_A L^{−18}. This is o(X_A/L) because X_A ≫ xL^{−C_A} and D > C_A + 10.
- V_1(x^{b1}) ~ 𝔖V(x^{b1}) ~ 𝔖e^{−γ}/(b1 L) by (7.9). I re-derived V_1/V = 2Π_{3≤p≤y}(1 − 1/(p−1)²) → 𝔖.
- e^{−h} ≤ e²·e^{−1/(20b1)}.
- So (7.11) holds as a lower bound, with error 𝔖X_A/L · O(b1^{−1}e^{−c/b1}).

**Upper bound for (ii) — every step is an UPPER bound or a two-sided equality. ✓**
- (a) Σ_{mp=N_u, p∈bin} AΨ I_γ(m) ≥ the mass of (ii) in that bin. Each such N_u is counted at least once, with p = P⁻(N_u), since P⁻(m) ≥ p > x^γ. Prime N_u are never counted, because m ≥ x^{1/2+κ} > 1. Everything counted lies in S_0, because P⁻(N_u) > x^γ ≥ x^{b1}. Overcounting is harmless.
- (b) The replacement I_γ → B_γ is a two-sided equality up to O(#dyads · xL^{−D*}) by Theorem 6.1. The ranges fit: p ∈ (x^{b1}, x^{1/2−κ}] and m ∈ [x^{1/2+κ}, 5x^{1−b1}] both lie in [x^{b*}, x^{1−b*}] with b* = b1/3, and UV ≍ x since N_u ∈ [2x, 4x+1]. α is W-rough, |α| ≤ 1, |β| ≤ 1. The discrepancy hypothesis comes from Lemma 7.3 for the same interval restriction (O6). There are O(L) dyad pairs per bin and finitely many bins, so the cost is o(X_A/L) once D* > C_A + 2.
- (c) B_γ ≥ 0, and c_γ(C_Y) ≤ (sup_{γ≤a≤γ′} D_γ(1−a) + o(1))/(LV(W)) by (7.17). This rests on (7.20), which is an upper count: the last prime's lower cutoff is dropped, and repeated primes are bounded by Yx^{−b1}. The inequality direction is correct.
- (d) Σ_{p∈bin} Σ_{p|N_u, P⁻(N_u)>W} AΨ comes from Lemma 2.9 per p, with X = X_A/(p−1), g(l) = 1/(l−1), remainders r(pd), and h = 2⌈T²⌉, i.e. level W^{4h+2} = x^{o(1)}. The upper side of (2.5) is used. The products pd ≤ x^{1/2−κ+o(1)} < x^ϑ are distinct (p > W is their only prime factor above W), squarefree and odd. So Σ|r(pd)| ≤ xL^{−D} + X_A L^{−18} = o(X_A V(W)), using V(W) ≍ L^{−1/2}.
- (e) Multiplying (c) by (d) and using V_1(W)/V(W) → 𝔖 and Σ_{bin} 1/(p−1) → log(γ′/γ) gives (7.21), as an upper bound.
- (f) D is jointly continuous on the compact set {b1 ≤ γ ≤ a ≤ 1/2−κ}, where w − γ = 1 − a − γ ≥ 2κ. So a fixed fine mesh gives Σ_bins ≤ ∫_{b1}^{1/2−κ} D_α(1−α)dα/α + 1/10. The integrand is ≥ 0, so this is ≤ ∫_{b1}^{1/2} = D_{b1}(1) − 1 by (7.18).

**Combining with (7.19) — the direction needed. ✓**
(7.19) is an UPPER bound on D_{b1}(1), which is the subtracted quantity. Hence:

mass(i) + mass(iii) ≥ (𝔖X_A/L)[e^{−γ}/b1 − O(b1^{−1}e^{−c/b1}) − (D_{b1}(1) − 1) − 1/10 + o(1)] ≥ (𝔖X_A/L)[1 − 1/10 − O(b1^{−1}e^{−c/b1}) + o(1)] ≥ 𝔖X_A/(2L).

This is (7.22). The Buchstab accounting leaves exactly the one-prime term "1". The losses are 1/10 (mesh slack), O(b1^{−1}e^{−c/b1}) (from (7.11) and (7.19)), and o(1).

**Upper bound for (iii) — (7.31) is an UPPER bound. ✓**
- Since N_u ≤ 4x+1 < x^{3(1/2−κ)}, N_u = mn with exactly two primes, both in B_κ. Ordered pairs count each such N_u once or twice, which overcounts.
- Two two-sided Theorem 6.1 replacements follow. The second takes α = (I_pr − B_pr)(n)1_K and β = B_pr(m), with |β| ≤ 1.
- Then B_pr ≥ 0 and B_pr ≤ C/(LV(W)) by (7.16): cells with w ∈ [0.46, 0.54], #primes/#W-rough ≈ 1/(wLV(W)). This gives (7.23).
- (7.30) per dyad pair, and O(κL + 1) dyad pairs, give C_bal(κ + L^{−1})X_A/L + o(X_A/L).
- Final count: Σ_{prime} ≥ 𝔖X_A/(2L) − C_bal κ X_A/L − o(X_A/L) ≥ 𝔖X_A/(4L) for large x, since C_bal κ < 𝔖/4.

**(7.30) line by line. ✓**
- Majorant (7.27). Expand a_Q into lists and W_1 into one mark per group. For a genuine decomposition, D1 | u. Every non-P prime l ≤ x^θ dividing u is a micro-band or rough-slot entry: the macro bands j < j′ have log p ≥ c1 s′2^{−j′+1}L > θL, and the rough slot has j** ≥ j0 ≥ j′. So such l is never banned. D1's P-part is exactly one prime per group, so the mask expectation is q^{ω(u)−s} = the W_1 damping. The normalized macro count is ≤ Π 1/a_p! ≤ 1.
- Sieve set-up. Residue counts: mn ≡ 0 (mod l) has 2l−1 pairs; mn ≡ 1 has l−1. g(l) ≤ 3/l, and g(3) ≤ 7/9 < 1. The CRT count φ(D1)ν(d) is right even when D1 has prime powers.
- Lattice error. Each class pair contributes O(1 + (M1+M2)/(D1d)). The remainders total ≪ L^{O(1)}((M1+M2)D + D1D²), with D = x^{10θ} ≤ x^{1/20}.
- Euler factors.
  - Banned l ≤ W: 1 − 3/l + 2/l² ≤ (1−1/l)³(1+O(l^{−2})).
  - Allowed P prime: (1−1/l)², which needs one compensating factor.
  - Banned l > W: 1 − 1/l + 1/l² ≤ (1−1/l)(1+O(l^{−2})).
  - There is no unbanned l > W, because all P primes are < W.
  - Primes dividing D1 need at most three compensating factors. These have product ≤ (1−L^{−20})^{−3L} = O(1), since D1 ≤ x^{1/20} and every p | D1 is ≥ L^{20}.
- E_mask Π_{allowed}(1−1/p)^{−1} = Π(1+q/(p−1)) ≤ H_P by (7.6).
- Σ_assgn λ/D1 = H_Q^{mic} exactly, because each group's normalized mark mass is V_g^{−1}Σ1/p = 1.
- Main term ≪ xV(W)²V(x^θ)H_Q^{mic}H_P ≪ X_A V(W)², using (7.3), (7.25) and V(x^θ) ≍ 1/(θL).
- Error ≪ x^{0.54+0.05+0.05}L^{O(1)}H_Q^{mic} = x^{0.64}L^{O(1)}H_Q^{mic} = o(xH_QH_P/L²).
- Constants: absolute sieve constants for h = 2 (η0 = 2/9 and Σ_{w<l≤w²} g(l) ≤ 3 log 2 + o(1)); (7.3)/(7.25) constants that depend on δ, r0, Ψ, j′ but not on j**; 1/θ.
- So C_bal is independent of κ, b1, j**, D*, B and S, as claimed.

---

## 3. Other re-derivations (all ✓)

**§7.1 geometry (c1, c2, c3, c4) = (1, 6/5, 3/2, 9/5).**
- Q_j ∪ P_j ∪ Q_{j−1} sit at [1, 1.2]s_j, [1.5, 1.8]s_j and [2, 2.4]s_j, so they are disjoint (c2 < c3 and c4 < 2c1). P_j and P_{j−1} = [3, 3.6]s_j are disjoint too.
- V_g = log(1.8/1.5) + o(1) = log 1.2 + o(1) ≈ 0.182, by PNT, since s_j ≥ L^{1/10}/1.5.
- Each kind has (1/10)log_2 L + O(1) ≍ T groups.
- Def 3.1 needs 0 < a < b < c < d < 0.47: (1/10, 1/5, 3/10, 2/5) ✓.
- §4 needs big groups to be intervals of primes inside [e^{L^c}, e^{L^d}] ✓.
- §3 uses 0.52 + d = 0.92 < 1 ✓, exp(L^{2/5}) < W ✓, and b < c (line "exp(ℓ|S|L^b) < exp(L^c)") ✓. §6.2 uses 1 − d = 0.6 > 1/2 ✓.
- §6.1 needs:
  - c2s′ < 1/4: 6/(11r0) < δ < 1/4 ✓;
  - λ = 2 and (6.1) = (7.1) ✓;
  - c_−T ≤ s_{jx} ≤ c_+T with c_∓ = 20, 40 ✓;
  - bands disjoint from each other and from the groups ✓;
  - η* < b*/4 = (7.10) ✓.
- (7.1) needs r0 ≥ 6 and r0 > 6/(11δ).

**Prop 7.1.**
- a_Q ≤ τ: fix the rough divisor; the band assignment is then forced; each band's normalized count is ≤ 1.
- A ≤ exp(C√L): ≤ 2^{log(2x)/log W} rough divisors, and W_1 ≤ C^{O(T)} = L^{O(1)}.
- (7.5): with F_g(y) = Π(1 + y/(p−1)), the group factor is F′_g(q)/V_g = F_g(q)V_g^{−1}Σ1/(p−1+q).
- (7.6): exact, since p−1+q ≤ p.
- (7.7): with ξ = L^{−2/5}, p^ξ ≤ e for all P primes (small ones too), so each tilted factor is ≤ e^{2eqV_g}·2e and Σ_{r>x^σ} ≤ e^{−σL^{3/5}}L^{O(1)}.
- Midpoint sum: Σ_j r0(c1+c2)/2·s′2^{−j}L = r0(c1+c2)s′L = L exactly.
- ∆ = (c2−c1)s′L = L/(11r0).
- Write log U = L − m_f + E′ + (free slot), with E′ ∈ (−∆/6, ∆/12) from:
  - prefix deviation ±∆/24;
  - tail midpoints [0, ∆/24) (this covers missing bands j > j_x);
  - actual tail values [0, ∆/24) (the rough slot included);
  - P-part [0, ∆/12].
- So the target for the free slot lies at distance ≥ ∆/3 − O(1) ≥ ∆/4 from [m_f ± ∆/2]. Conditional probability ≍ 1/L; upper bound O(1/L).
- The constants do not depend on j**, and r0, the prefix and the masses are fixed early.
- Prime-factor range [L^{20}, x^δ]: smallest band c1s_{jx} ≥ 20T; P primes ≤ e^{L^{2/5}}; rough slot ≤ x^{c2s′2^{−j**}} < x^δ.

**Prop 7.2.**
- 2u+1 ≡ 0 (mod d) is a unit class for u.
- (u, d) > 1 correction: (L/(20 log L))·L^{−20}·O(L) = O(L^{−18}/log L) per u ✓.
- Exact extraction A(u) = Σ_{pr=u, p∈Q_0} b(r), with b ≤ L^{O(1)}τ: since j** ≥ 1, Q_0 has only prime slots, and W_1(pr) = W_1(r).
- Large sieve bound: Theorem 2.3 with 1/φ(f) ≤ (f/φ(f))/R, then Cauchy–Schwarz, gives (1/R)√((P+R²)(U+R²)PU)·L^{O(1)}. Expanding √(PU)(√P+R)(√U+R)/R with PU ≍ x gives x(R^{−1} + U^{−1/2} + P^{−1/2} + R/√x) exactly as displayed.
- ϑ < 1/2 makes R/√x a power saving; P, U ≥ x^a with a = s′/2.
- Small conductors: Siegel–Walfisz (modulus ≤ 2L^{C′} ≤ (log P)^{O(1)}).
- p | h: ≤ ϑ/a terms, costing x^{1−a}L^{O(1)}.
- The L^{O(1)} exponent does not depend on C′, so choosing C′ and then A is legitimate.

**Lemma 7.3.**
- (7.13): Lemma 2.9 with g = 1/p (g(2) = 1/2), h = 2⌈T²⌉, D_W = W^{4h+2} = x^{o(1)} ≪ ∆_L Y.
- 0 ≤ c_I ≤ 1: tests select W-rough integers, since x^γ > W and primes ≥ x^{b1/4} > W.
- Principal case: χ ≡ 1 on W-rough m (r ≤ L^B < W). Full cells have zero unweighted sum. The variation of t^{iv−1} on a cell is O((1+|v|)∆_L/Y), so full cells give O((1+|v|)∆_L·harmonic mass) = O(L^{B−S}). Two partial cells add O(L^{−S} + x^{−b1/4+o(1)}).
- Nonprincipal test:
  - unique nondecreasing list of l ≤ 2/b1 primes > x^γ;
  - the last prime ranges over one interval in [x^γ, x²] (order ∧ cutoff ∧ the interval for Qp_l);
  - Corollary 2.4 gives O(L^{−A}) uniformly in r ≤ L^B and |v| ≤ L^B;
  - the remaining factors cost (Σ_{x^γ<p≤x²}1/p)^{l−1} = O_{b1}(1);
  - imprimitive characters are fine (primes ≥ x^γ do not divide r).
- Nonprincipal proxy: (7.14), from the CRT in a unit class with primes p | r omitted. The main term cancels over χ. The errors are O(|J′|V(W)e^{−T²} + φ(r)D_W). After partial summation and summing O(L^{S}) cells this gives O(e^{−T²}) + x^{−b1/4+o(1)}L^{O(1)}.
- |B_I| ≤ 1 for every S, so the Theorem 6.1 coefficient bound is independent of S. The order coefficient bound → B → S is non-circular.

**Lemma 7.4.**
- (7.16): w ∈ [0.46, 0.54] for κ < 1/50 gives C ≈ 1/0.46.
- (7.20) and (7.17): checked as above. Short-interval PNT on (y, e^{L^{−S}}y] with y ≥ x^γ/2 needs accuracy (log y)^{−A} with A > S+1, and the paper takes A > S+3. The w − γ ≥ 2κ uniformity is used correctly.
- (7.18) re-derived:
  - the l-th term of D_{b1}(1) is (1/l!)·dt_1…dt_{l−1}/(t_1⋯t_l) on {Σt_i = 1, t_i ≥ b1}, which is symmetric;
  - selecting the minimum α gives factor l and measure dα/α;
  - the rest is the (l−1)-term of D_α(1−α), with coefficient l/l! = 1/(l−1)!;
  - α ≤ 1/l ≤ 1/2;
  - the l = 1 term is 1.
- (7.19): the liminf lower density ≥ D_{b1}(1) (lists weighted 1/l! put ≤ 1 on each integer) is compared with the Lemma 2.9 upper bound xV(x^{b1})(1+O(e^{−c/b1})) + O(x^{0.49}).

**Numerical check of (7.18)** (`/tmp/sieve_scripts/buchstab.py`, run under `nice -n 19`):
- D_γ(w) is computed directly from definition (7.15) by nested adaptive quadrature, not via the Buchstab recursion.
- It is compared with Buchstab's ω from its delay differential equation, and with e^{−γ}/b1.
- Negative controls (`negctl.py`) with perturbed identities must fail, and they do.

Verbatim output:
```
b1=0.300000: D_b1(1)=1.8699640129  D_b1(1)-1=0.8699640129  int_b1^1/2 D_a(1-a)da/a=0.8699640129  diff=2.22e-16 (quad err 9.7e-15)
           omega(1/b1)/b1=1.8699640135   e^-gamma/b1=1.8715316119   D_b1(1)-e^-g/b1=-1.568e-03
b1=0.250000: D_b1(1)=2.2458329656  D_b1(1)-1=1.2458329656  int_b1^1/2 D_a(1-a)da/a=1.2458329656  diff=0.00e+00 (quad err 1.4e-14)
           omega(1/b1)/b1=2.2458329662   e^-gamma/b1=2.2458379343   D_b1(1)-e^-g/b1=-4.969e-06
b1=0.200000: D_b1(1)=2.8072723413  D_b1(1)-1=1.8072723413  int_b1^1/2 D_a(1-a)da/a=1.8072723413  diff=-4.44e-16 (quad err 2.0e-14)
           omega(1/b1)/b1=2.8072723421   e^-gamma/b1=2.8072974178   D_b1(1)-e^-g/b1=-2.508e-05
b1=0.170000: D_b1(1)=3.3027045981  D_b1(1)-1=2.3027045981  int_b1^1/2 D_a(1-a)da/a=2.3027045972  diff=-8.95e-10 (quad err 2.9e-09)
           omega(1/b1)/b1=3.3027045989   e^-gamma/b1=3.3027028445   D_b1(1)-e^-g/b1=1.754e-06
negative controls (b1=0.2): target D_b1(1)-1 = 1.8072723413; (a) D_{0.9a}(1-a): 1.9514708651  (b) da instead of da/a: 0.5715740276  (c) wrong coefficient 1/(l·l!): 1.5943022934
```
- For b1 = 1/5: D_{1/5}(1) − 1 = 1.8072723413 and ∫_{1/5}^{1/2} D_α(1−α)dα/α = 1.8072723413.
- D_{b1}(1) agrees with ω(1/b1)/b1, as the Buchstab interpretation predicts.
- D_{b1}(1) − e^{−γ}/b1 takes both signs (negative at 0.3/0.25/0.2, positive at 0.17). That is consistent with (7.19), whose (1+O(e^{−c/b1})) factor allows either sign, so a one-sided "D ≤ e^{−γ}/b1" would be false. The paper never claims that.

**Final count and Theorem 1.2.**
- Σ_{2u+1 prime} AΨ ≫ X_A/L.
- Each summand is ≤ ‖Ψ‖ exp(C√L), and X_A ≫ xL^{−C_A}.
- u ↦ 2u+1 is injective, so there are ≥ xL^{−C_A−1}e^{−O(√L)} = x^{1−o(1)} distinct primes. This is an honest x^{1−o(1)}.
- Range: u ∈ [x, 2x] gives p ∈ [2x+1, 4x+1] ⊂ (2x, 5x].
- P⁺(p−1) = max(2, P⁺(u)) ≤ x^δ. The exceptional slot is W-rough, not prime, but its prime factors are ≤ its value ≤ x^{η*} < x^δ.

**§8, line by line.**
- Lemma 8.1:
  - p^a ∥ m implies p^{a−1}(p−1) | φ(m), so fibers are finite.
  - φ(m) ≥ c_θ m^{1−θ}: use 1 − 1/p ≥ p^{−θ} for large p, put the small primes into c_θ, and use p^{−θ} ≤ 1.
- Theorem 1.1:
  - Take x = X/5. This gives > X^{1−δ} primes ≤ X with X^δ-smooth p−1.
  - k = ⌊X^{2δ}⌋ ≤ M since 3δ < 1.
  - (8.1): C(M,k) ≥ (M/k)^k, since each factor (M−j)/(k−j) ≥ M/k ⇔ M ≥ k. And M/k > X^{1−3δ}.
  - φ(Π_{p∈Q} p) = Π(p−1) ≤ X^k is X^δ-smooth.
  - (8.2): exponents are ≤ k log X/log 2 and there are ≤ X^δ primes. Then log[(1 + k log X/log 2)^{X^δ}]/(k log X) = O(X^δ log X)/(X^{2δ} log X) = O(X^{−δ}) → 0.
  - Pigeonhole gives n ≤ X^k with g(n) ≥ X^{(1−3δ−o(1))k} > n^{1−ε}, since 3δ + o(1) < ε, which follows from 4δ < ε.
  - g(n) → ∞ and fibers are finite, so infinitely many such n exist.
  - The case ε ≥ 1 is trivial.

---

## 4. Parameter-dependency table (§7–8)

| constant | fixed where | depends on | used where | claimed independent of (verified?) |
|---|---|---|---|---|
| δ ∈ (0,1/4) | input | — | (7.1), final range | — |
| Ψ | §7.1, step (i) | — | X_A, Thm 6.1 data | — |
| q = 1/2, ℓ = 1 | §7.1 | — | W_1, Def 3.1 | — |
| c1, c2, c3, c4 = 1, 6/5, 3/2, 9/5 | §7.1 | absolute | geometry | — |
| r0 | §7.1 (i) | δ (r0 > 6/(11δ), r0 ≥ 6) | (7.1), (6.1) | — |
| s′ = 1/(r0(c1+c2)) | §7.1 | r0 | s_j, ∆ | — |
| a, b, c, d = 1/10, 1/5, 3/10, 2/5; c0, C0, v_± | §7.1 | absolute (v_± ≈ log 1.2) | §3–6 hypotheses | — |
| j_x, s_j | x-dependent | x, s′ | bands | — |
| prefix length j_p | §7.1 (i) | r0, c's | lower bound in (7.3) | — |
| j′, θ | §7.6 (i) | r0, c's, s′ | (7.24)–(7.30) | — |
| j0 | (i) | j_p, j′ | j** ≥ j0 | — |
| C, C_A (Prop 7.1) | (i) | early data | (7.2), (7.3), D, D* | j** (✓) |
| C_bal | after (i) | δ, r0, Ψ, j′, θ, P-geometry | (7.31), (ii) | κ, b1, j**, S, D*, B (✓) |
| κ | (ii) | C_bal, 𝔖; κ < 1/50 | ϑ, B_κ, (7.16), (7.31) | — |
| b1 | (iii) | absolute constants of (7.11)/(7.19)/(7.22); κ only through ϑ | sieve, bins, b* | — |
| h = 2⌊1/(40b1)⌋ | (iii) | b1 | (7.11), (7.19) | — |
| ϑ = 1/2 − κ/2 | (iii) | κ | (7.8) level | — |
| b* = b1/3 | (iii) | b1 | Thm 6.1 | — |
| j**, τ*, η* | (iii) | b*, r0, j0 ((7.10)) | A(u), Thm 6.1 | C_A, C_bal, (7.3) constants (✓) |
| bin mesh | (iii) | b1, κ (uniform continuity of D) | (7.21) | — |
| D (Type I saving) | free | > C_A + 10 | (7.8), (7.11), §7.5 | — |
| D* | (iv) | C_A (+ dyad count) | Thm 6.1 errors | — |
| coefficient bound C (Thm 6.1) | (iv) | |α|, |β| ≤ 1 ⇒ fixed | Thm 6.1 | S (✓, |B_I| ≤ 1) |
| B (discrepancy exponent) | (iv), output of Thm 6.1 | D*, b*, C, Ψ, group/band constants incl. j** | Lemma 7.3 | S (✓) |
| S (cell precision) | (v) | B (S > 2B+3) | proxies | — |
| PNT/SW accuracies | (v) | S (A > S+3), B | (7.16), (7.20), Lemma 7.3 | — |
| h_W = 2⌈T²⌉, D_W | x-dependent | x | (7.13), (7.14), §7.5 | uniformity in h in Lemma 2.9 (✓) |
| ξ = L^{−2/5}, σ = ∆/(12L) | Prop 7.1 | s′, r0 | (7.7) | — |
| ε, δ (§8), 4δ < ε | §8 | ε | (8.1)–(8.2) | — |
| X, x = X/5, k = ⌊X^{2δ}⌋, M | §8 | X | pigeonhole | — |

No cycle. B depends on j**, b*, D* and C, but not on S, κ-proxies or the mesh. S is chosen last, and nothing upstream depends on S.

---

## 5. Citation table (results used in §7–8)

| cited | paper says | source says (quote) | verdict |
|---|---|---|---|
| Thm 2.3 ← MV [15] Thm 19.16 (author-hosted draft, refs/MV_energy/mv2.pdf) | Σ_{r≤R}(r/φ(r))Σ*|Σ a_nχ(n)|² ≪ (H + 1 + R²)Σ|a_n|² for a_n on an interval of length H | "Theorem 19.16 … for any integer Q ≥ 1, Σ_{q≤Q} q/φ(q) Σ★ |S(χ)|² ≤ (N + Q²) Σ_{n=M+1}^{M+N} |c_n|² for arbitrary complex numbers c_n." | MATCH (N ≤ H+1) |
| Thm 2.2 (SW) ← Tao 254A notes 2, Ex. 64 | π(y; r, a) = Li(y)/φ(r) + O_{A,C}(y/(log y)^A), uniformly for r ≤ (log y)^C | "Exercise 64 (Siegel–Walfisz theorem) … Σ_{n≤x, n=a (q)} Λ(n) = x/φ(q) + O(x exp(−c_A √log x)) … with q ≤ log^A x" | MATCH (partial summation) |
| PNT ← Tao notes 2, Cor. 39 / Ex. 40 | PNT with error below any fixed log power | "Σ_{n≤x} Λ(n) = x + O_A(x log^{−A} x)"; "π(x) = li(x) + O(x exp(−c√log x))" | MATCH |
| Mertens (2.2) ← Tao 254A notes 1, Thms 15, 26 (fetched to refs/Tao254A1_sieve/) | Σ1/p = log log y + O(1); Π(1−1/p) ∼ e^{−γ}/log y | Thm 15: "Σ_{p≤x} 1/p = log log x + c_1 + O(1/log x)"; Thm 26: "Π_{p≤x}(1−1/p) = (e^{−γ}+O(1/log x))/log x" | MATCH |
| Lemma 2.9 ← Ford–Halberstam [8] §1 Lemma 1 (refs/FH) | the block product / one-block correction inequalities | "Lemma 1. Suppose that 0 ≤ x_j ≤ y_j (j = 1,…,r). Then x_1⋯x_r ≥ y_1⋯y_r − Σ_ℓ (y_ℓ − x_ℓ) Π_{j≠ℓ} y_j." | MATCH. The paper proves Lemma 2.9 in full; I re-checked the proof: U_j ≥ I_j for even h_j, U_j − I_j ≤ E_j, level Σ(j+1)h2^{−j} = 4h (+1), and R_h ≪ e^{−h} |
| Pomerance [19] Thm B (refs/Pom/popular.pdf) | "Pomerance states the relevant transfer explicitly" | "THEOREM B (Erdős [3]). Suppose that there is an ε > 0 such that Π(x, x^u) > επ(x) for all large x. Let m_1 < m_2 < … be the values of m where N(m) > m^{1−u}. Then there are infinitely many m_i …" | MISMATCH IN STRENGTH (positive-proportion hypothesis). Not load-bearing; §8 is self-contained (O2) |
| Pomerance [19] p. 84, C = 1 attributed to Erdős | Erdős conjectured C = 1 | "Erdos [4] has conjectured that C = 1." | MATCH as to Pomerance's text (the identity of his [4] belongs to the citations seat) |
| Buchstab [4] | the identity (7.18) is "the corresponding Buchstab identity" | — | COULD NOT FETCH (Mat. Sbornik 1937, no open copy found). Not load-bearing: re-derived exactly and checked numerically |
| Friedlander–Iwaniec [9] §1 | "compare" only | — | not load-bearing; not checked by this seat |

---

## 6. Verified line by line vs only skimmed

**Verified line by line** (rendered PDF):
- §7 opening paragraph.
- §7.1: definitions, (7.1), P/Q disjointness, group counts and masses, the designated slot.
- Prop 7.1: (7.2), (7.4), (7.5), (7.6), (7.7), the upper and lower localisation, uniformity in j**, the prime-factor range.
- §7.2: r(d); Prop 7.2 in full (unit class, L^{−18} correction, Q_0 extraction, h–f decomposition, the four-term large-sieve bound recomputed, small conductors, p | h terms); V, V_1, 𝔖, (7.9); κ, b*, (7.10), h, ϑ, b1(4h+2) < ϑ, D > C_A+10, (7.11) and its direction.
- §7.3: (7.12); Lemma 7.3 statement and proof (both cases, test and proxy), the cell count, the order coefficient → B → S.
- §7.4: (7.15); joint continuity; Lemma 7.4 (7.16), (7.17), (7.20) incl. repeated primes and PNT accuracy, (7.18) re-derived and checked numerically, (7.19).
- §7.5: in full, including the overcount, Theorem 6.1's hypotheses, the per-p sieve, distinctness of the pd, (7.21), the mesh, (7.22).
- §7.6: in full — 3(1/2−κ) > 1, B_κ, double replacement, (7.23), (7.24)–(7.26), (7.27) incl. the mask expectation and macro normalisation, residue counts, ν, g, base mass, CRT count, lattice error, (7.28), Euler factors, (7.29), the H_P bound, main term, error term, (7.30), (7.31), C_bal independence.
- §7.7 (i)–(v), the final count, the range, P⁺(p−1).
- §8: Lemma 8.1 and the proof of Theorem 1.1.
- Inputs used by §7: Theorem 2.3 statement, Corollary 2.4 proof, Lemma 2.5, Lemma 2.9 proof, Theorem 2.2 statement, the Def 3.1 / §4 / §5 / §6.1 hypotheses on groups and bands, the statement of Theorem 6.1, Remark 6.2.

**Skimmed or not checked:**
- Theorem 6.1's proof (§6), Theorem 5.1 (§5), Theorems 3.5 and 4.1 (§3–4) — other seats.
- Whether hypotheses *hidden inside* the §3–5 proofs (as opposed to the stated hypotheses I checked) are met by the §7 geometry.
- The plausibility of Theorem 6.1 in the very unbalanced regime V ≈ x^{b1} with b1 of order 1/100–1/200 that §7 needs (O7).
- Buchstab 1937 (not fetched).

---

## 7. Verdict for this seat

**HOLDS AS READ — §7 (pp. 53–65), §8 (pp. 65–66), and Theorem 1.2 ⇒ Theorem 1.1, conditional on Theorem 6.1.**

The sieve lower bound (7.11) and the composite upper bounds (7.21) and (7.31) are each proved in the direction the subtraction needs. The Buchstab bookkeeping (7.18)–(7.19) leaves exactly the one-prime term, with losses 1/10 + O(b1^{−1}e^{−c/b1}) + C_bal κ + o(1). Theorem 6.1 is applied with the discrepancy hypothesis that Lemma 7.3 actually provides: same interval restriction (one dyad), coefficient bound 1 for every S, and S fixed after B. The order of choices is acyclic. The count x^{1−o(1)} is honest. §8 is correct and self-contained.

**COULD NOT CHECK** (outside scope): whether Theorem 6.1 is true, particularly at b* ≈ b1/3 → 0. Theorem 1.2 stands or falls with it.
