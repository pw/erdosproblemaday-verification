# Referee report — seat `energy`: §5.4–5.8 (PDF pp. 39–45), the local Fourier energy bound (5.11)

Paper: OpenAI, "Weighted dilation graphs, smooth shifted primes and totient fibers" (24 Sept 2026), /tmp/oaimath/011/paper.pdf.
Read from the rendered PDF pages 35–45 (all of §5), plus pp. 4–10 (Convention 2.1, Lemmas 2.5–2.8, Lemma 2.9/Cor 2.10) and pp. 27–34 (Theorem 4.1, Lemma 4.2, Lemma 4.3, §4.4) for interface facts.
Toy checks: `/tmp/energy_checks/check512.py` (run `nice -n 19 python3 -I`).

## Bottom line

I did not find a sentence in §5.4–5.8 where the argument fails. I re-derived every displayed step, and every inequality points the way it is used. What remains is cosmetic: wrong "Theorem" labels on lemmas, one sentence describing steps out of order, and overloaded notation. The section proves (5.11) **assuming** (a) its inputs from §5.2–5.3 (the shape of the endpoint sequence U in (5.9), the arc set with H = H′/L^{C_arc}, H′ ≥ exp(L^c)), and (b) the discrepancy hypothesis (5.4) for the first endpoint's α. Whether §6–7 actually deliver (5.4) with the B chosen last is outside this seat.

**The seat's main question, answered:**
1. **(i) A small-group prime p_s ∈ [exp(L^a), exp(L^b)] is forced.** It is forced by the mark weight W_t^b, not by (5.3). On the comparison-pattern endpoints t_g = ℓ + c_g. Theorem 4.1 gives C_g = ∅ for every small group g ∈ S (p. 27: "C_g = ∅ (g ∈ S)"), so t_{g_s} = ℓ ≥ 1. The raw pattern has t_g = ℓ too. W_t^b(w) contains the factor (ω_{g_s}(w))_ℓ, which vanishes unless ω_{g_s}(w) ≥ ℓ ≥ 1. The mark function b depends only on big labels: Theorem 4.1, (4.2): "These coefficients use no shared labels and none of the last ℓ labels", with X_A, X_B, D_A, D_B big-group products, and p. 38: "The additional mark function uses only big labels".
2. **(ii) The long W-rough factor p ∈ I_p ⊂ [x^τ, x^η] is forced** by (5.3). F_0 is the Dirichlet convolution (α χ_0 m^{iσ0}) * (1_{I_p, P⁻>W} p^{iσ1}) * c evaluated at n_*, so every term carries such a p.
3. **(5.12) is an exact identity for ordered distinct lists** whenever p_s ∤ w/p_s, and in particular whenever no prime of P_{g_s} divides w squared. Proof:
   - Fix the designated slot. List ↦ (p_s = entry in that slot, the remaining (t−1)-list) is a bijection onto pairs (p_s | w, list of t−1 distinct primes of P_{g_s} dividing w/p_s). Every prime ≠ p_s dividing w divides w/p_s. Conversely, no prime dividing w/p_s equals p_s when p_s ∥ w.
   - The q-exponent is unchanged: ω drops by one and Σ t_g drops by one.
   - The factor V_{g_s}^{−1} is split off, and b is unchanged because it ignores small labels.
   - Toy check (small group {11,13,17,19,23}, a big group carrying a nonconstant b, t_s = 2, t_b = 1, exact rational arithmetic): 0 mismatches on 57,143 integers with no p_s² factor. All 28 mismatches occur on square multiples, which is exactly the error set the paper bounds.
4. **No step of §5.5–5.8 uses the second endpoint's structure.** V enters only through ‖V‖₂² ≪ Y L^{C8} ((5.10)), via Cauchy–Schwarz on each major arc (p. 39) and via Parseval on the minor arcs. The argument is symmetric, so either endpoint could carry the structure, which is consistent with the "conjugated" clause of Theorem 5.1.
5. **N_E is compatible with Lemma 5.3.** I recomputed log N_E ≤ log(2P) + O(j_0) + j_0 log j_0 + 2A_s j_0 log L + O(log L) with j_0 = ⌊log Y/log 2P⌋ ≤ (1+o(1))L^{1−a}. So N_E = exp(O_{A_s}(L^b + L^{1−a} log L)) = Y^{o(1)} because 0 < a and b < 1. Lemma 5.3 needs R·Y^{1/2} ≪ U log 2Y with U ≍ Y/(PP′) ≥ Y^{1−η−o(1)} ≥ Y^{3/4−o(1)} (using P ≤ x^{o(1)}, P′ ≤ x^η, η < 1/4, Y ≥ x). R ≤ Y^{0.05} suffices, so the requirement holds with a wide margin. The only proviso is x ≥ x_0(A_s), which is legitimate because A_s is fixed before x → ∞.

## Objections (numbered)

None of these is FATAL or a GAP.

**E1 — COSMETIC (wrong cross-reference labels).** These statements are cited as "Theorem" but are Lemmas or a Corollary:
- p. 41: "By Theorem 2.6, for any dyadic time scale T′ ≥ 1," — this is Lemma 2.6.
- p. 41: "A fixed number of convolution factors and Theorem 2.5 give" — Lemma 2.5.
- p. 42: "In the last step use Theorem 2.6" — Lemma 2.6.
- p. 43: "For the occupied unit intervals I_j in Theorem 5.2," — Lemma 5.2.
- p. 43: "Theorem 2.7 gives O(U/|z|)" — Lemma 2.7(i).
- p. 43: "By Theorem 2.10, there is a polynomial" — Corollary 2.10.
- p. 45: "Theorem 5.4 gives an arbitrarily strong uniform bound" — Lemma 5.4.
- p. 45: "and Theorem 5.3 gives" — Lemma 5.3.

In each case I checked that the intended statement is the one used and that its hypotheses hold. Same pattern just before §5.4: "Theorem 4.2" = Lemma 4.2, "Theorem 3.11" = Cor 3.11. Fix: relabel.

**E2 — UNCLEAR, exposition only, harmless (order of operations in §5.5, p. 41).** "For the remaining portion split the four factor variables in Equation (5.13) into dyads. There are O(L⁴) boxes and only boxes whose joint size is comparable to Y contribute. … Fourier-separate the parenthesized cutoff in logarithmic coordinates. … truncate at a fixed log-power frequency with arbitrary saving."
- Once (w/Y)Ψ₁(w/Y) is Fourier-separated, the cutoff no longer kills boxes whose product range misses its support, so the box selection must happen first.
- The correct order is available: before separation such boxes contribute exactly 0.
- The rest is right as written. Cauchy–Schwarz over O(L⁴) boxes and over the L^{O(1)}-mass Fourier integral costs L^{O(1)}. The truncated tail is bounded by the mean value ∫_{|t|≤L/h}|Q|² ≪ (LY/H + Y log Y)·L^{O(1)}/Y = L^{O(1)} times an arbitrarily small tail mass (Lemma 2.8). The shifts move [−L/h, L/h] into [−2L/h, 2L/h].
- Fix: one sentence fixing the order.

**E3 — COSMETIC (overloaded notation).**
- u is the arc numerator in §5.4, the log-variable in v = Ye^u in §5.5, and u = t+σ in Lemma 5.4.
- v is the unit m p_s p (r/d_0) in §5.4, the Plancherel variable in (5.14), and a Mellin frequency in w^{iv}.
- B_0 is both the dyadic exponent of Lemma 4.3 ((4.20)) and the threshold of Lemma 5.4.
- H is both the arc scale and the H of Lemma 2.7(ii).
- I tracked each use; no step mixes them.

**E4 — UNCLEAR (hidden x-threshold in Lemmas 5.2/5.3).** Lemma 5.2: "The set E meets at most exp(O(L^b + L^{1−a} log L)) = Y^{o(1)} intervals". The implied O-constant contains 2A_s (from j_0·log(CL^{2A_s})). Lemma 5.3 needs "R = Y^{o(1)}" only in the form R ≤ Y^{0.1}, which holds for x ≥ x_0(A_s). The bound L^{C12} itself is independent of A_s (verified: the row sum is ≪ U log 2Y once RY^{1/2} ≤ U, and Σ|c_n|² ≪ L^{C10}/U). This is correct under Convention 2.1 ("Every constant is fixed before x → ∞") and is consistent with §5.8's order (A_s, then the Lemma 5.4 accuracy A, then B_0, then B). It is worth stating explicitly because C12 must not depend on A_s, and it does not.

**E5 — COSMETIC.** §5.8 (p. 45): "Its range condition holds since 2L/h = o(Y) = x^{1+o(1)} < x²/2". This abuses o(·); the intended statement is 2L/h ≤ Y = x^{1+o(1)} < x²/2. True.

**E6 — COSMETIC (normalization wording of (5.15)).** p. 40: "the squared norm of the error in Equation (5.14) is ≪ (H/Y)² Σ_w |a_w|²". This is H^{−2} times the squared L²(dv) norm of the kernel-replacement error. Recomputation:
- The arguments (w−v)/H and v log(w/v)/H differ by O(H/Y) on |w−v| ≪ H.
- Cauchy–Schwarz over O(H) values of w gives |E(v)|² ≪ H (H/Y)² Σ_{|w−v|≪H}|a_w|².
- Integrating over v gives ≪ H²(H/Y)²Σ|a_w|². Multiplying by H^{−2} gives (H/Y)²Σ|a_w|².
- This is ≪ H² L^{O(1)}/Y = x^{−1+o(1)}. Correct.

**E7 — Interface note (not an error in this scope).** (5.4) quantifies over all intervals I ⊂ [1, x²], including unit intervals. Taken literally, it forces |α_m| ≤ m L^{−B} for every single m. That is vacuous for m ≥ L^{B+C} and restrictive only for small m. In §5.8 only dyads [M_0, 2M_0) ∩ supp α are used, so a weaker hypothesis (dyadic intervals intersected with the support) would suffice for this section. Whether §6–7 verify (5.4) for the α actually used, with B chosen after B_0(C, C_arc, A, τ, η), belongs to the §6/§7 seats. This seat only confirms that §5.8 asks for no more than (5.4) as stated.

## Line-by-line verification record (§5.4–5.8)

### §5.4
- **(5.12)** exact, as in "main question" item 3. Error set = integers with p_s² | w for some p_s ∈ P_{g_s}.
  - Both sides are ≤ L^{O(1)}: (5.2) with t_max ≤ ℓ + m_probe, which is J-independent, and ω_{g_s}(w) ≤ L^{1−a}(1+o(1)).
  - |F_0(n)| ≤ L^{2C} τ_3(n_*) ≤ L^{2C} τ(n_*)², and w_* | w/p_s².
  - Σ_{p_s} Σ_{w≍Y, p_s²|w} τ(w_*)⁴ ≪ Y L^{O(1)} Σ p_s^{−2} ≪ Y L^{O(1)} e^{−L^a}. Here Y/p_s² = x^{1+o(1)} because p_s ≤ exp(L^b) = x^{o(1)}.
  - Parseval over the arc (length < 1) bounds the error energy by Σ|e_w|². Verified.
- **The factorization w = m p_s p r.** Set r := w/(m p_s p), so r_* = the original residual (m, p are P-free since W > exp(L^d) ≥ every group prime). Then (p_s, m, p, r′) ↔ (m, p_s, p, r) is a bijection and W^b_{t−e}(w/p_s) = W^b_{t−e}(r) because m, p carry no group primes. The residual coefficient c_{r_*}W^b_{t−e}(r) is ≤ L^{C + C(t_max)}. Verified.
- **Units mod q_0.**
  - m: P⁻(m) > W > L^{C_arc} (or m = 1). p_s ≥ exp(L^a) > L^{C_arc}. p: P⁻(p) > W. So all three are units mod r_0.
  - r itself need not be coprime to r_0, since r contains the arbitrary residual of (5.3). With d_0 = (r, r_0) and q_0 = r_0/d_0, gcd(r/d_0, q_0) = 1 always (elementary; also checked for all r < 3000, r_0 < 300: 0 violations). So v = m p_s p (r/d_0) is a unit mod q_0 in every case.
  - e(uw/r_0) = e(uv/q_0). Verified.
- **Character expansion.** Σ_χ c(χ)χ(v) = e(uv/q_0) by orthogonality, and |c(χ)| ≤ φ(q_0)^{−1}·φ(q_0) = 1. The sum runs over all characters mod q_0, including principal and imprimitive ones. Number of pairs (d_0, χ) = Σ_{d_0|r_0} φ(r_0/d_0) = r_0 ≤ L^{C_arc}, so Cauchy–Schwarz costs L^{C_arc}. χ_m = χχ_0 has modulus ≤ L^{C+C_arc}, and χ_p = χ has modulus ≤ L^{C_arc}. Verified.
- **(5.13).** Coefficients factor as a product of functions of m, p_s, p, r. The constraint (r, r_0) = d_0 involves r only. Σ|a_w|² ≪ Y L^{O(1)} by a fixed divisor moment (τ_4 ≤ τ³). Verified.

### §5.5
- **K and (5.14).** For K ≥ 0 with ∫K = 1 and supp K ⊂ [−1/6, 1/6]: Re K̂(ξ) ≥ cos(2π/6) = 1/2 for |ξ| ≤ 1.
  - With f(v) = Σ a_w K((w−v)/H): f̂(ξ) = H K̂(−Hξ) â(−ξ).
  - Hence ∫_{|β|≤1/H}|â(β)|² ≤ 4H^{−2}∫_R|f|².
  - The direction is the one used (an upper bound for the energy). Verified.
- **Kernel replacement and (5.15):** see E6. Verified.
- **Logarithmic Fourier inversion.** With y = v log(w/v)/H = e^u log(w/v)/h and ξ = h e^{−u} t/(2π), the displayed formula follows exactly. Verified.
- **|A(s,t)| ≪_j (1+|s|)^{−2}(1+|ht|)^{−j}.**
  - Two u-derivatives of ρ(u)e^{−u}K̂(c e^{−u}) stay bounded uniformly in c because ξ^k K̂^{(k)}(ξ) is Schwartz.
  - The decay in c = ht/(2π) comes from the same fact. Verified.
- **(5.16).** Minkowski in s, then Plancherel in u for each s: ‖ρg‖_{L²(du)} ≪ h(∫(1+|ht|)^{−2j}|P|²)^{1/2}. With dv ≤ O(Y)du: H^{−2}·Y·h² = Y^{−1}. Verified.
- **Dyadic tail.**
  - Lemma 2.6 on two intervals of length T′ with polynomial length ≍ Y and Σ|a_w|² ≪ Y L^{O(1)} gives Y^{−2}∫_{T′≤|t|≤2T′}|P|² ≪ (T′/Y + log Y)L^{O(1)} ≪ (1+T′/Y)L^{C9}. Verified.
  - Summing over T′ = 2^k L/h: Y L^{C9} Σ_k (2^k L)^{−j}(1 + 2^k L/H) ≪ Y L^{C9+1−j}. So the portion |t| > L/h is O(YL^{−A}) for j ≥ A + C9 + 1. Verified.
- **Reduction to (5.17).**
  - There are O(L⁴) boxes, since each variable has O(L) dyads, including p_s ≤ exp(L^b).
  - P(t)/Y factors exactly through 1/w = (1/m)(1/p_s)(1/p)(1/r).
  - Order of operations: see E2.
  - (5.17) is needed with A′ ≥ A + 4 + C_arc + O(1). Verified.
- **(5.18).** p_s ∈ [exp(L^a), exp(L^b)] gives e^{L^a}/2 ≤ P ≤ e^{L^b}. I_p ⊂ [x^τ, x^η] gives x^τ/2 ≤ P′ ≤ x^η. Verified.
- **(5.19).** Collapsed coefficients are (1/n)·(product of L^{O(1)} coefficients) times the ordered-factorization count ≤ τ(n)^{b−1}, so Σ_{n≍U}|c_n|² ≪ L^{O(1)}/U. The exponent is independent of J and A_s. Verified.

### §5.6
- **Ordinary times.** P_lR has length ≍ Y/P and coefficient-square sum ≪ L^{C10}P/Y. Lemma 2.6 on |t| ≤ 2L/h gives ≪ (LP/H + log Y)L^{C10}. Since LP/H ≤ L^{1+C_arc} e^{L^b − 2L^c} → 0 (b < c, and H′ ≥ exp(2L^c) because both free products contain a big prime), the portion is ≪ L^{−2A_s+C11}. The paper's ratio (Y/P)/(2L/h) = H/(2LP) is correct. Verified.
- **Lemma 5.2.**
  - j_0: (2P)^{j_0} ≤ Y, so P_s^{j_0} has indices < Y.
  - Coefficient squares: |c_n|² ≤ (#ordered reps)·Σ_reps Π|b|²p^{−2}, and the number of ordered representations of n as a product of j_0 primes is a multinomial coefficient ≤ j_0!, repeated primes included. So Σ|c_n|² ≤ j_0!(Σ_{p≍P}|b|²p^{−2})^{j_0} ≤ j_0!(2/P)^{j_0}.
  - Sobolev: |Q(t_0)|² ≪ ∫_{|t−t_0|≤1/2}(|Q|²+|Q′|²). Lemma 2.6 on an interval of length O(Y) for Q and for Q′ (coefficients multiplied by i log n) gives Σ_j|Q(t_j)|² ≪ Y(log 2Y)³Σ|c_n|². The constants are absolute, which is essential because j_0 → ∞.
  - Markov: N·L^{−2A_s j_0} ≤ Σ_j|P_s(t_j)|^{2j_0}. Three residue classes.
  - Exponent: see "main question" item 5. Verified.
- **Lemma 5.3.**
  - U ≍ Y/(PP′) ≥ Y^{1−η−o(1)} > Y^{0.6}, using Y ≥ x. Σ|c_n|² ≪ L^{O(1)}/U.
  - (5.20), first range 1 ≤ |z| ≤ cU: f′(n) = z/(2πn) is monotone, |f′| ≍ |z|/U, and f′ ⊂ [λ, 1−λ] (or [−1+λ, −λ]) with λ ≍ |z|/U. Lemma 2.7(i) gives ≪ U/|z|.
  - (5.20), second range cU < |z| ≪ Y: |f″| ≍ |z|/U² with a bounded ratio on n ≍ U. Lemma 2.7(ii) gives ≪ |z|^{1/2} + U|z|^{−1/2} ≪ Y^{1/2}.
  - |t_j − t_k| ≤ 4L/h + 2 ≪ Y, so (5.20) applies to every pair.
  - Gram row sums: Σ_k U/(1+|t_j−t_k|) ≪ U log 2Y for unit-separated points, plus RY^{1/2}.
  - Schur on ΦΦ* (with (ΦΦ*)_{jk} = Σ_n n^{i(t_j−t_k)}) gives Σ_j|R(t_j)|² ≪ U log(2Y)·Σ|c_n|² ≪ L^{O(1)}.
  - Maxima taken over closed unit intervals; three classes. Verified.

### §5.7 (Lemma 5.4)
- **Sieve setup.**
  - h_s = 2⌈T²⌉ is even and → ∞, so e^{−h_s} ≤ L^{−2T}. D = W^{4h_s+2} = exp(O(√L T²)) = x^{o(1)}.
  - Cor 2.10 gives U ≥ 1_{P⁻>W}, |λ_d| ≤ 1, d ≤ D squarefree with primes ≤ W, and Σ_{[P′,2P′]}(U − 1_{rough}) ≪ P′e^{−h_s} + D.
  - Nonnegativity of U − 1_{rough} gives |Σ_{J′}χ(n)n^{−1+iu}(U−1)| ≤ P′^{−1}Σ(U−1). Verified.
- **(5.21).** Σ|λ_d|/d ≤ Π_{p≤W}(1+1/p) ≪ log W. Verified.
- **Splitting n.** (d, q′) > 1 kills the term. n = dv with v = q′y + a, χ constant on classes, N = P′/(dq′) ≥ x^{τ−o(1)} ≥ x^{τ/2}. B_0 > C+1 gives |u| ≥ L^{B_0}/2. Verified.
- **(5.22), Kusmin–Landau regime |u| ≤ cN.** f(y) = (u/2π)log(q′y+a) and f′ = uq′/(2π(q′y+a)) ≍ u/N, monotone, inside (0, 1/2) or (−1/2, 0) for small c. Lemma 2.7(i) gives ≪ N/|u|. Verified.
- **(5.22), van der Corput regime.**
  - The ranges [N^{k−2+ε_0}, N^{k−ε_0}] for 2 ≤ k ≤ K = ⌈4/τ⌉+3 overlap and cover (cN, x²], because N^{K−ε_0} ≥ x^{(K−0.1)τ/2} ≥ x².
  - f^{(k)} = (u/2π)(−1)^{k−1}(k−1)! q′^k/(q′y+a)^k has constant sign and |f^{(k)}| ≍_k |u|N^{−k}.
  - After positive shifts h_1, …, h_{k−2} ≤ H_0 = ⌊N^{ε_0/(2k)}⌋: g″ is an iterated integral of f^{(k)}, so |g″| ≍ |u|N^{−k}Πh_i ∈ [c_kN^{−2+ε_0}, C_kN^{−ε_0/2}], since Πh_i ≤ N^{(k−2)ε_0/(2k)} < N^{ε_0/2}.
  - Second-derivative test on length ≤ CN: ≪ N·N^{−ε_0/4} + N^{1−ε_0/2}.
  - Weyl–van der Corput in normalized form: B_j² ≪ H_0^{−1} + B_{j+1}, with h = 0 giving H_0^{−1}, negative h giving conjugates, and shifts = o(N) keeping v ≍ P′/d.
  - Recursion recomputed exactly (Fractions, k = 3..11): starting from ε_0/4 and halving min(ε_0/(2k), ·) k−2 times gives exactly δ_k = ε_0/(k 2^{k−1}). δ = ε_0/(K2^{K−1}) depends only on τ.
  - Verified.
- **Partial summation and the class sum.** The weight 1/n ≤ 1/P′ is monotone. With the subinterval-uniform bound from (5.22), the q′ classes give (1/d)(|u|^{−1} + N^{−δ}) and N^{−δ} ≤ x^{−τδ/2}. Verified.
- **Final bound.** Total ≪ e^{−h_s} + D/P′ + √L(2L^{−B_0} + x^{−τδ/2}) ≪ L^{−A} for B_0 > A + 2. B_0 depends on (C, A); τ and η affect only the x-threshold and the implied constant. Verified.

### §5.8
- **Ordinary times.** O(L^{−2A_s+C11}). Verified.
- **Exceptional times with |t| ≥ L^{B_0}.**
  - ≤ sup|P_s|²·sup_{|t|≥L^{B_0}}|P_l|²·Σ_j sup_{I_j}|R|² ≪ L^{O(1)+C12−2A_{5.4}}.
  - Lemma 5.4 applies with its C = max(C, C_arc) (χ_p mod q_0, σ = σ_1) and |t + σ_1| ≤ 2L/h + L^{O(1)} < x².
  - Verified.
- **|t| ≤ L^{B_0}.**
  - The m-polynomial is Σ_{m∈[M_0,2M_0)∩supp} α_m (χ_0χ)(m) m^{−1+i(σ_0+t)}.
  - Interval ⊂ [1, x²] because M_0 ≪ Y = x^{1+o(1)}. Modulus ≤ L^{C+C_arc}. Frequency |σ_0 + t| ≤ L^C + L^{B_0}, where t is the already-shifted (5.17) variable, so the Mellin shifts v_1 and v are included.
  - So (5.4) applies once B ≥ max(C + C_arc, B_0) + 1.
  - The other factors are L^{O(1)} (harmonic sums). The integral is ≪ L^{−2B+B_0+O(1)}, with O(1) independent of B. Verified.
- **Order of choices.** Theorem 5.1 data (C, τ, η, Ψ bounds, D_0) → C_7, hence C_4 → probe count m and kernels (Q, h, ξ, C_1; Theorem 4.1/Lemma 4.3) → J (Theorem 3.5) → D_2, C_arc, the (5.11) target A, Lemma 2.8 tails → A′ → A_s → A_{5.4} → B_0 → B → x → ∞.
  - Every constant in §5.4–5.8 (C_8, …, C_12) depends only on C, ℓ, m (through t_max in (5.2)) and fixed divisor moments. None depends on J, A_s, A, B_0 or B.
  - The ideal frequency range is |ζ| ≤ 2L^C + L^{C_7}. It is fixed by the Theorem 5.1 bounds and by C_7, and C_7 is fixed by Lemma 2.8 before any accuracy ("C′ … may be fixed before the desired A", p. 7; tail exponent C(j+1) − C′(j−b) → −∞ as j grows once C′ > C). So C_4 is fixed before J and is not enlarged by later tail accuracies. The paper's claim "no enlargement of the already fixed ideal frequency range" holds.
  - **No cycle in this scope.**

## Citation table (scope §5.4–5.8 and the lemmas it invokes)

| Cited result | Paper's claim | Source (version read) and quote | Verdict |
|---|---|---|---|
| [15] MV draft, Cor 16.6 → Lemma 2.7(i) (used in (5.20), (5.22)) | "If f′ is monotone and stays in [j+λ, j+1−λ] … then Σ e(f(n)) ≪ λ^{−1}." | Author-hosted draft (472 pp., pdf CreationDate 2024-10-09), downloaded to refs/MV_energy/mv2.pdf: "Corollary 16.6 Let f(x) be a real valued function continuous on [a, b], with a continuous derivative on (a, b), and such that f′(x) is increasing. Suppose further that M₁ is a positive real number such that ∥f′(x)∥ ≥ M₁ for all x ∈ (a, b). Then \|Σ_{a≤n≤b} e(f(n))\| ≤ 2/(πM₁)." Decreasing f′ follows by conjugation. | MATCH |
| [15] MV draft, Thm 16.7 → Lemma 2.7(ii) (used in (5.20), (5.22)) | "If f is C² and λ ≤ \|f″\| ≤ Cλ … Σ e(f(n)) ≪_C Hλ^{1/2} + λ^{−1/2}." | "Theorem 16.7 Let N be a positive integer with a ≤ b ≤ a + N and suppose that f is twice differentiable on [a, b] and that 0 < M₂ ≤ f″(x) ≤ AM₂ when a ≤ x ≤ b. Then Σ_{a≤n≤b} e(f(n)) ≪_A M₂^{1/2}N + M₂^{−1/2}. If instead we have −AM₂ ≤ f″(x) ≤ −M₂, then the same bound applies". Continuity of f″ with \|f″\| ≥ λ > 0 forces constant sign. | MATCH |
| [16] MV 1974, Thm 2/Cor 3 → Lemma 2.6 ("compare") | Weaker elementary mean value. | Not fetched (paywalled). Lemma 2.6 is proved in full in the text; I re-derived it (off-diagonal 2/\|log(n/m)\| ≤ 2Y/\|n−m\|, Σ1/\|n−m\| ≪ log 2Y; Sobolev for (2.3)). | NOT LOAD-BEARING (proof verified) |
| [13] MR arXiv:1501.04585v4, §2.1, §4 Lemmas 8–9 ("compare", §5.6) | Ordinary/exceptional split, prime-polynomial moments, sparse mean square. | refs/MR/paper.pdf (v4, 15 Oct 2017). Lemma 8: "Let k = ⌈log T/log P⌉ … ≤ (1/P^k) k! (Σ 1/p)^k … \|T\| ≪ T^{2 log V/log P} V² exp(2 (log T/log P) log log T)". Lemma 9 (Halász for integers): "Σ_{t∈T}\|A(it)\|² ≪ (N + \|T\|√T) log 2T Σ\|a_n\|²". The paper explicitly does not invoke MR's theorems and reproves analogues: Lemma 5.2 takes j_0 from the length Y rather than from the time range (equally valid), and Lemma 5.3 is Halász–Montgomery with √T ≤ Y^{1/2}. | MATCH (compare-citation; analogues proved in text) |
| [20] Soundararajan 2009, Lemma 3 ("compare", Lemma 5.2) | Factorial coefficient estimate for prime-polynomial moments. | refs/Sound/paper.pdf (arXiv math/0612106v2): "Lemma 3. … ∫_T^{2T} \|Σ_{p≤x} a(p)/p^{1/2+it}\|^{2k} dt ≪ T k! (Σ_{p≤x} \|a(p)\|²/p)^k", with a_{k,x}(n) the multinomial. The paper's j_0! bound is the same mechanism. | MATCH (compare) |
| Cor 2.10 / Lemma 2.9 (internal, Brun–Hooley; Ford–Halberstam [8] cited there) → Lemma 5.4 | U ≥ 1_{P⁻>W}, \|λ_d\| ≤ 1, d ≤ z^{4h+2}, overcount ≪ \|I\|e^{−h} + D, Σ\|λ_d\|/d ≪ log 2z. | Internal proof (pp. 8–10) skimmed: block degrees h_j = (j+1)h, level Σh(j+1)2^{−j} = 4h, e_j ≤ C^{h_j+1}/(h_j+1)!, R_h ≪ e^{−h}. Ford–Halberstam not fetched by this seat (another seat's scope). | Internal; main lines checked |
| Lemma 2.8 (internal) → §5.5 cutoff separation, §5.2 ideal frequency range | C′ fixed before A; L^{O(1)} coefficient mass. | Proof checked: tail L^{C(j+1)−C′(j−b)} → any negative power once C′ > C; mass from b+1 derivatives. | Internal; checked |

## Parameter-dependency table (§5.4–5.8)

| Constant | Fixed where | Depends on | Used where | Claimed independent of / verified |
|---|---|---|---|---|
| a < b < c < d < 0.47 | Def 3.1 | — | (5.18), Lemma 5.2 exponent, b < c in §5.6 | x; ✓ |
| ℓ ≥ 1, q | Def 3.1 | — | t_{g_s} = ℓ ≥ 1 in (5.12); damping | J; ✓ |
| C (endpoint bounds: \|α\|, \|c_r\|, χ_0 modulus, σ_0, σ_1, a_i, k, Z) | Thm 5.1 hypotheses | — | everywhere | ✓ |
| τ, η (η < 1/4) | (5.3) | — | Lemma 5.3 (U > Y^{0.6}), Lemma 5.4 (N ≥ x^{τ/2}, K, δ) | ✓ |
| C_7 (Mellin cutoff of Ψ) | §5.2 | Ψ derivative bounds (Lemma 2.8) | ideal frequency range | later accuracies; ✓ |
| C_4 (ideal frequency exponent) | input to Thm 4.1 | C, C_7 | (4.1) | J and all later choices; ✓ |
| m_probe, Q, h, ξ, C_1 | Thm 4.1 / (4.20) | E_id, C_4, ℓ | H′ ≤ exp(O(m T L^d)) (5.8); pattern costs | J; ✓ (outside scope, as stated) |
| J | after kernels | E, E_id | not used in §5.4–5.8 constants | — ✓ (t_max = ℓ + m) |
| C_8 ((5.10)) | §5.3 | C, ℓ, m (via (5.2)), divisor moments | arc Cauchy–Schwarz | J, A, B; ✓ |
| D_2, C_arc | §5.3 | pattern costs, κ, C′ | arcs; r_0 ≤ L^{C_arc} | — ✓ |
| A ((5.11) target) | §5.3 | C_arc, C_8, D_2 | (5.11) | — ✓ |
| K (kernel), j (decay order) | §5.5 | absolute; j after A, C_9 | (5.14)–(5.16) | ✓ |
| C_9, C_10, C_11 | §5.5–5.6 | C, t_max, divisor moments | tails, (5.19), ordinary times | A_s; ✓ |
| A′ ((5.17) target) | §5.5 | A, C_arc, boxes L⁴, separation cost | (5.17) | ✓ |
| A_s | §5.6 | A′, C_11 | E, Lemma 5.2 | ✓ |
| j_0, N_E | Lemma 5.2 | x, P, A_s | Lemma 5.3 | N_E ≤ Y^{0.05} for x ≥ x_0(A_s); ✓ |
| C_12 | Lemma 5.3 | C, t_max, divisor moments, η < 0.4 | §5.8 | A_s; ✓ |
| A_{5.4} (accuracy in Lemma 5.4) | §5.8 | A′, C_12 | exceptional times | ✓ |
| h_s, D | Lemma 5.4 | T, W (x-dependent) | sieve | ✓ |
| ε_0 = 1/10, K = ⌈4/τ⌉+3, H_0, δ = ε_0/(K2^{K−1}) | Lemma 5.4 | τ | (5.22) | C, A; ✓ |
| B_0 (Lemma 5.4) | §5.8 | max(C, C_arc) + 1, A_{5.4} + 2 | Lemma 5.4; low-time regime | ✓ |
| B ((5.4)) | last | C + C_arc, B_0, A′ | m-polynomial at \|t\| ≤ L^{B_0} | chosen after everything; no feedback ✓ |

## Steps verified line by line vs skimmed

**Verified line by line (re-derived):**
- §5.4 in full: (5.12) (proof plus toy check), the error bound, the factorization and residual, the unit claims including gcd(r/d_0, q_0) = 1, the character expansion and |c| ≤ 1, (5.13).
- §5.5 in full: K and the direction of (5.14), (5.15), logarithmic Fourier inversion, A(s,t), (5.16), the dyadic tail via Lemma 2.6, boxes and separation, (5.17)–(5.19).
- §5.6 in full: the ordinary-times bound and ratio, Lemma 5.2 (every line), Lemma 5.3 (every line, both ranges of (5.20), Gram/Schur).
- §5.7 Lemma 5.4 (every line, the δ_k recursion computed exactly).
- §5.8 (all three regimes; the order paragraph).
- The lemmas these invoke: Lemmas 2.5, 2.6, 2.7 (against MV), 2.8.
- The major-arc use of (5.11) on p. 39 (Cauchy–Schwarz, |M| ≤ 1, arc count).

**Skimmed or taken as input (not verified here):**
- Lemma 2.9/Cor 2.10: main lines only.
- The minor-arc claim and Dirichlet approximation in §5.3 (lift seat).
- §5.2's lift to (5.7) and the claim that U in (5.9) has the stated form. I confirmed only the interface facts C_g = ∅ on small groups, A and B nonempty, and coefficients using only big labels, from Theorem 4.1 as stated.
- Theorems 3.5 and 4.1 themselves.
- Whether §6–7 produce α satisfying (5.4).

## Verdict for scope §5.4–5.8

**HOLDS AS READ.** The local Fourier energy bound (5.11) follows from (5.4) for the first endpoint, the shape (5.3), and t_{g_s} = ℓ ≥ 1 with small-label-free marks, by the argument written. Objections E1–E7 are cosmetic, exposition-order, or interface notes; none is a mathematical gap. I could not check anything that lies outside the scope: §5.3's minor arcs, §5.2's lift, and §6–7's verification of (5.4) at the B chosen last.
