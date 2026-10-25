# Referee report — seat `transference` — Section 3 (PDF pp. 10–26)

Paper: "Weighted dilation graphs, smooth shifted primes and totient fibers" (OpenAI, 24 Sept 2026), /tmp/oaimath/011/paper.pdf (sha in paper.sha256).
Scope: Definitions 3.1–3.3, Lemma 3.4, Theorem 3.5, Lemmas 3.6–3.10, (3.37)–(3.47), "Completion of Theorem 3.5", Corollary 3.11.
Method: read every page of §3 from the rendered PDF (pp. 10–27); re-derived every displayed identity and inequality by hand; checked the memory identity (Lemma 3.7) exactly by computer on 13 toy instances, with mutation controls and a negative control on the hypothesis "group primes > |k|" (scripts in /tmp/transference_toy/, outputs quoted in §D below).

**Bottom line for this seat: I could not refute Section 3.** Theorem 3.5 and Corollary 3.11 follow from hypothesis (3.6) as written. I found no hidden loss exponential in N. The only cost paid on every visit or edge is the ghost cost L^{C_v} and the projection cost L^{C_s}; both are independent of m, C_1, J and both are paid by (3.37). Every other per-edge cost either goes to zero by the choice of J (dirty part), or is additive and of size exp(−L^c+O(T)) (density change, free/active ban), or is paid on only o(N) edges (equality-rank phases), or is a tail of size exp(−Ω(L²)) (memory truncation). The memory identity is exact on every toy I ran. The objections below are cosmetic or expository. **§3 proves nothing about whether (3.6) holds; that is Theorem 4.1, which is outside this seat.**

---

## A. Objections (numbered)

**1. Cross-references point to "Theorem" for objects that are Definitions, Lemmas or a Corollary.** COSMETIC.
- p.12, Lemma 3.4: "C_abs may depend on m, C_1 and the fixed data in Theorem 3.1". Same in Theorem 3.5 ("the fixed data in Theorem 3.1") and Lemma 3.10 ("depending only on the fixed data in Theorem 3.1"). There is no Theorem 3.1; this is **Definition 3.1**.
- p.13: "Theorem 3.11 will turn precisely this estimate into cancellation". This is **Corollary 3.11**.
- p.14: "By Theorem 3.4, the absolute mass of all length N paths … is L^{O(N)}"; "Taking A sufficiently large in Theorem 3.6". These are **Lemma 3.4** and **Lemma 3.6**.
- p.20 ("by the proof of Theorem 3.8"), p.24 ("In the proof of Theorem 3.8"), p.25 ("Theorem 3.8 bounds its new norm by L^{C_a}"). This is **Lemma 3.8**.
- p.25: "which is the expression required by Theorem 3.7". This is **Lemma 3.7**.
- Fix: renumber. Every target is unambiguous, so no mathematical consequence.

**2. "ℓ ∈ N" in Definition 3.1, but Lemma 3.9 and the choice of J in (3.37) need ℓ ≥ 1 (and J ≥ 1).** UNCLEAR (exposition). True as used: §5–§7 fix ℓ ≥ 1, and the application uses ℓ = 1, q = 1/2.
- Quote, p.10: "0 < q < 1, ℓ ∈ N." Quote, (3.29): "𝒟 = (M choose ℓ)^{|S|}". Quote, (3.37): "it suffices that (c_0/2) log (J+ℓ choose ℓ) > C_a + G + 3."
- If ℓ = 0 then 𝒟 = 1, the rare-transfer bound (3.30) gives no saving, and the condition on J cannot be met. Theorem 3.5 as stated (fixed data includes "ℓ ∈ N") would then be unproved. The paper states "ℓ ≥ 1" only later (p.33: "it is possible because ℓ ≥ 1"; §5: "t_{g_s} = ℓ ≥ 1"; §6).
- Fix: write ℓ ≥ 1 in Definition 3.1.

**3. Edge step (i) does not name the law of the auxiliary free draws.** UNCLEAR (exposition); the intended reading is correct.
- Quote, p.16: "(i) Form D from shared source labels and the independent free draws." The memory identity holds only if the free draws keep the physical law μ_g (not μ̃_g). That is implicit in Def 3.3 ("independent labels of law μ_g") and in Lemma 3.10 ("the measures of active labels and fresh target integrations are μ̃_g in place of μ_g", so free draws stay μ_g).
- My toy check (§D) uses μ_g for free draws on both sides and matches exactly.
- Fix: write "law μ_g".

**4. The proof of Lemma 3.7 is a two-paragraph sketch of a bijection.** GAP (exposition only). I checked the statement and it is correct.
- Quote, p.17: "Conversely, fix an original compatible path and a chosen lifespan term for every represented big prime. … Thus these constructions are mutually inverse and preserve all coefficients."
- The reader must supply three things the sketch leaves out:
  - (a) Under distinct-birth plus the free-label ban, the rules "Require p ∤ D for every stored or promoted particle" and "Newly stored particles cannot be promoted across this edge" are automatic: a stored prime is an unshared source label, so it is neither a shared label nor a free label. My mutations deleting either rule leave the identity unchanged. The rules are needed only for the evolution without distinct-birth used in Lemma 3.9, which the paper says on p.20: "The exclusion p ∤ D is retained under reversal, even when numerical coincidences have been allowed".
  - (b) A stored particle never terminated, or a ghost born at visit N, gives zero because the final memory must be empty. This is what reproduces the "1" (dropped) term of (3.13) and the strict inequalities j < i in (3.14).
  - (c) Free labels are not births, so a free label may equal a pending or later-active prime. This matches the physical ban, which applies only to the two endpoint lists of that edge.
- I verified exactness by computer (§D). No fix needed beyond writing the bijection out.

**5. Notation collisions make the section hard to verify.** COSMETIC.
- B is both the big-group index set and the memory cap ⌈L²⌉ in (3.27).
- h is the Bonferroni degree (Lemma 3.6), the offsets h_i, the block size in (3.46), and the ghost-batch index in (3.16).
- A is the residue precision, A_i = q_i/ρ² in (3.19), the terminated subset A in (3.16), and the free probe set in §4.
- D_i = −η_i/ρ in (3.19) clashes with the shift D_i of §3.2. 𝒟 in (3.29) is another object again.
- C_i = V_gD_i, alongside many constants named C.
- No mathematical consequence. Each overloading resolves from context.

**6. The step "exp(−ANT) = L^{−AN}" is never stated.** COSMETIC.
- p.14: "Taking A sufficiently large … makes the summed error smaller than L^{−A′N}". This needs exp(−ANT) = L^{−AN} (T = log L) against the absolute path mass L^{C_abs N}. Correct, and the needed order is A > A′ + C_abs. The paper leaves it implicit.

**7. Corollary 3.11 only helps if E > 2C_3.** COSMETIC for §3; a note for the global-order seats.
- Quote, (3.48): "|⟨f, 𝒜g⟩| ≪ XL^{−E+2C_3}". So C_3 (the endpoint norm exponent, C_6 in §5) must be fixed before E, and hence before E_id, m, C_1, J. §3 correctly takes C_3 as given.
- The other seats must confirm that §5's C_6 is independent of E, E_id, J. The paper claims it is independent of J.
- Also, the final sentence "the extra factor L^{−C_3/R} is bounded for fixed C_3" is trivially true: the factor is ≤ 1.

**8. Theorem 3.5 is stated for one real ζ ("No bound on ζ is needed apart from the assumed ideal estimate"), but Theorem 4.1 gives (4.1) only for |ζ| ≤ L^{C_4}.** Not an error in §3; a note for the `lift` / `energy` seats.
- Within §3 the claim is correct: ζ enters only through multipliers D^{iζ} of modulus 1, and through the hypothesis.
- The application must keep |ζ| ≤ L^{C_4} with C_4 fixed before E_id. This is outside my scope.

No FATAL objection. No mathematical GAP found in §3.

---

## B. Verification record (what I checked and how)

### B1. Definitions 3.1–3.3, the adjoint claim and (3.4) — verified
- Joint weight of an edge in group g: source mass V_g^{−M} times target coefficient V_g^{−t_g}, which equals V_g^{−M−t_g} in either direction. Free-label law is the same both ways. D is unchanged on reversal because shared labels are copied slot to slot. The damping q^{(ω(n)−Ms)/2}q^{(ω(n′)−Ms)/2} is symmetric.
- Hence, with equal mass at every state, the adjoint is the reversed operation: shift −kD, labels swapped, multiplier conjugated. ✓

### B2. Lemma 3.4 and (3.5) — verified
- Ordered unshared target lists: (y−M+t_g)_{t_g}, with z = y−M.
- sup_z V_g^{−t_g}(z+t_g)_{t_g}q^{z/2} < ∞ depends only on q, v_−, and t_g ≤ ℓ+m. Hence independent of J.
- Product over s ≍ T groups gives C^{O(T)} = L^{O(1)}. Times Σ sup|K_ν| ≤ L^{C_1}. Columns by (3.4).
- The residue-model version is identical, since the sup over z covers any number of zero coordinates. ✓ C_abs = C_abs(m, C_1, fixed data).

### B3. Theorem 3.5 quantifiers against the proof — verified
- E_id is fixed by (3.37) from E, C_v, C_s only. C_v depends on (v, ρ, q, v_+, C_0); C_s on (q, ℓ, v_−, C_0). So E_id is independent of m, C_1, J, as claimed.
- J is chosen after C_a = C_a(m, C_1, …), G and c_0.
- The x-threshold depends on J, m, C_1, C_2, γ, A, C″. It is uniform in ζ, Θ, k (given |k| ≤ L^{C_2}), the K_ν beyond (3.2), and X ∈ [x^γ, x^{1/γ}].
- No cycle (see table C).

### B4. (3.8) — verified
- An interior visit is the target of one edge and the source of the next: q^{(ω−Ms)/2} twice gives q^{#\{p∉Λ_i : p | n+h_i\}}. Endpoint visits get one half, so q_0 = q_N = √q. ✓

### B5. Lemma 3.6 — verified line by line
- (3.9): log Q_act ≤ (N+1)Ms·L^d = O_J(L^{0.52+d}T) = o(L). This uses d < 0.47.
- X_p ∈ [0,1] with c_{p,r} = 1 − Π_{i: h_i ≡ −r} q_i ∈ [0,1].
- λ ≤ (N+1)Σ_{group p} 1/p ≤ (N+1)v_+s = O(NT).
- Bonferroni for numbers in [0,1] is the inclusion–exclusion for independent events, so it is valid. The independent expectation of e_{h+1} is e_{h+1}(EX) ≤ λ^{h+1}/(h+1)!.
- h = K_A·NT with K_A large gives (eλ/h)^h ≤ exp(−(A+C)NT).
- CRT: #{n ∈ I : n ≡ a mod Q} = |I|/Q + O(1).
- Number of terms ≤ (π(exp(L^d))(N+1))^{h} = exp(O(hL^d + h log N)) = exp(O_A(L^{0.52+d}T)) = exp(o(L)). Coefficients are ≤ 1. Total error exp(o(L))/|I| ≤ exp(−γL+o(L)), negligible against Q_act^{−1}·q^{O_J(NT)} = exp(−o(L)).
- Summation over paths: Σ_paths |coef|·E_res ≤ (initial mass ≤ 1 by (3.10)) × (residue-model row bound)^N = L^{C_abs N}. Relative error exp(−ANT) = L^{−AN}, so the summed error is ≤ L^{−(A−C_abs)N}. ✓

### B6. (3.11)–(3.14) and the "exactly one lifespan" claim — verified
- (3.13) checked by direct expansion: Π_{i<a}(1−x_i) = 1 − Σ_{j<a} x_j Π_{j<i<a}(1−x_i).
- (3.14) checked by splitting residues r into classes S_r = {i : h_i ≡ −r} and using Π_{S}(1−x_i) = 1 − Σx_i + Σ_{j<i∈S} x_jx_i Π_{j<t<i,t∈S}(1−x_t). Summing over r gives b_p + (1/p)Σ_{j<i, h_j≡h_i} η_jη_i Π(…). ✓
- Hand check, M = 1, D = 1, h = (0,k,0): a generic prime's factor is 1 − 2(1−q)/p = b_p + η_0η_2/p. ✓
- The two compatibility consequences need only "group primes > |k|" plus the distinctness/ban rules. ✓ Negative control in §D.
- Baseline: Σ_i η_i ≤ N+1 < P_*, so 0 < b_p ≤ 1. It is common to all paths and multiplies the signed sum, so dropping it is legitimate. ✓

### B7. §3.4 ρ-accounting — verified for every event
- Ghost birth: (−η_jV_g/ρ)·μ̃(p)·ρ = −η_j/(pb_p).
- Internal hit: ρ·(q_i/ρ²)·ρ = q_i.
- Ghost termination: ρ·(−η_i/ρ) = −η_i.
- A stored particle sits at residue Δ ≢ 0 after its edge (p ∤ D, p > |k|), so it pays no ρ and cannot be promoted across that edge.
- A promoted particle is removed before step (iv).
- Lifespan cost V_g^{−r}/(pb_p) for both birth types. ✓
- "Termination precedes birth" reproduces j < i in (3.14).
- Boundary: memory is empty at visit 0, and must be empty at visit N, so continuing zeros and births at N contribute 0. ✓

### B8. Lemma 3.7 — exact on all computer toys (§D)

### B9. §3.5 — verified
- (3.18): weighted Schur test, standard. ✓
- (3.19): (1/(k+t)!)·C(k+t,t) = 1/(k!t!). ✓
- Adjoint swap: conjugating and exchanging (t,α) ↔ (b,β) gives birth coefficient D_i and termination coefficient C_i. ✓
- (3.20): |G|w(z) = v^j(A_i+|D_i|/v)^{z}·exp(|C_i|vν(P_g)), recomputed. ✓
- (3.21) implies A_i + |D_i|/v < 1 (row) and A_i + |C_i|/v < 1 (column, since |C_i| ≤ v_+|D_i|), also with doubled ghost births. That is enough, because the z-dependent factor is then ≤ 1 for every z.
- The exponential factor per group is exp(η_iV_gvν/ρ) ≤ exp(2v_+v/ρ). Over |B| ≤ C_0T groups this gives L^{O(C_0v_+v/ρ)} = L^{C_v}. Bounded per group, yes.
- (3.23)–(3.25): (j)_a/j! = 1/(j−a)! = (j−a+b)_b/(j−a+b)!. ✓ Counting measure on the forced residues gives one point. ✓
- Reversal factor V_g^{b−a} ≤ max(V,V^{−1})^{ℓ+m} per group. ✓

### B10. Lemma 3.8 — row verified line by line; column verified at the level of the argument
- Row: (Z′)_aρ^{Z′−a} ≤ sup_z(z)_aρ^{z−a}; v^{b−a}; V^{−a}; μ̃(P_g)^{t−a} ≤ 2^{t}; 4^{t} transfer subsets. All bounded per group in terms of ℓ, m, ρ, v, v_±. So C_a = C_a(m, C_1, fixed data), independent of J. ✓
- Column: same form after reversal, with the step-(ii) ρ factors controlling retrievals. ✓

### B11. (3.27)–(3.28) — verified
- Stores supply ≤ (ℓ+m)|B|N particles, so a violating path has ≥ L² − O(L^{0.52}T) ghost births.
- The 2^{−#births} trick with the doubled-ghost absolute bounds gives exp(−(log 2)L² + O(NT)), which is ≤ L^{−AN} = exp(−AL^{0.52}T) for every fixed A. ✓

### B12. Lemma 3.9 — verified
- D_S = F/U, where U is the product of the ℓ omitted labels per small group. The small labels are distinct (small states are physical), so the 𝒟 = C(M,ℓ)^{|S|} values of U are distinct integers.
- U ≤ exp(ℓC_0TL^b) < exp(L^c) ≤ p, so they are distinct mod p.
- F, k, D_B are units mod p: F has small primes only, |k| < p, p ∤ D.
- r + σkD_BF/U ≡ 0 fixes U mod p, and r = 0 is impossible. So at most one omission choice per pending particle, at most B in total.
- Promotion part: row (B/𝒟)L^{C_a}, column L^{C_a}. Store-only part: the same with rows and columns exchanged, using the target symmetrization. Schur gives 2L^{C_a}(B/𝒟)^{1/2}. ✓
- "Does not bias": K_ν depends on big labels only, and D^{iζ}, e(θσkD) have modulus 1. ✓
- (3.32): √B = L and 𝒟^{−1/2} ≤ L^{−(c_0/2)log C(J+ℓ,ℓ)}. ✓

### B13. Lemma 3.10 — derivation of (3.34)–(3.36) verified
- The two P_d's carry V^{−J/2−ℓ} each, i.e. V^{−J−2ℓ} = V^{−M−ℓ} in total, the physical joint normalization.
- Cauchy in R gives the multiplier sup_{z≥M} q^{z−M}(z−M+ℓ)_ℓ/V^ℓ. This depends on q, ℓ, v_− only, so C_s is independent of J, m, C_1. ✓
- Fourier on (small torus) × (pending residues, counting measure) is unitary and diagonalizes translation by Δ = σkd′D_B. At frequency (ξ, r̂) the phase is e(σΘD_B) with Θ = kd′(θ + Σξ_p/p + Σr̂_h/p_h) (sign conventions aside). This is independent of the big active labels.
- The ρ factors are multiplication operators on the source and target memories (contractions), so absorbing them into the test vectors is legitimate.
- The density change and the free/active ban are ADDITIVE perturbations of size O_{J,m}(L^{C_1}sN/P_*) = exp(−L^c+O(T)). ✓

### B14. (3.37)–(3.38) — verified
- Clean part 2L^{−E_id+C_s} < 2L^{−G−2}; dirty part ≤ L^{C_a+1−(c_0/2)log C(J+ℓ,ℓ)} < L^{−G−2}. Sum ≤ L^{−G} for large x. ✓

### B15. §3.8 — every exponent recomputed
- (3.39): A_* ≤ (J+ℓ)C_0T(N+1) + (N+1)C_0T·L² = L^{2.52+o(1)}, so C′ can be taken independent of J once x ≥ x_0(J).
- (3.41): sign-sum over value-preserving permutations, standard Möbius inversion on set partitions. ✓
- (3.42): coefficient of t^r in Π_{j<A}(1+jt) = number of permutations with A − #cycles = r ≤ e_r(0,…,A−1) ≤ (A²/2)^r/r! ≤ A^{2r}. ✓
- (3.43): μ̃_g(p) ≤ 1/(v_−P_*b_p) ≪ 1/P_*. ✓
- Large rank: Σ_{r≥r_0} L^{C′r}·L^{C_h(N+1)}(C/P_*)^r ≤ L^{C_h(N+1)}·exp(−r_0(L^c − O(T))). With r_0 = ⌈C″NT/L^c⌉, which tends to ∞ because c < 0.47 < 0.52, this is L^{C_h(N+1) − C″N(1−o(1))} = o(L^{−EN}) for C″ > C_h + E + 1. ✓
- (3.46): equality of integers as ∫_{[0,1]^{h−1}} e(Σ τ_j(p_{β_j} − p_{β_0})) dτ. ✓
- Small rank: affected operations ≤ #addresses ≤ 2r(π), since each block has size ≥ 2 and |B′| ≤ 2(|B′|−1).
- (3.47): N − 2r unaffected edges at L^{−G}, 2r affected edges at L^{C_a}, N+1 ghost operations at L^{C_v}. Exponent (−G+C_v)N + C_v + 2r(G+C_a). ✓ recomputed.
- Display after (3.47): Σ_{r<r_0} L^{C′r}·L^{(−G+C_v)N+C_v+2r(G+C_a)} ≤ L^{(−G+C_v)N + C_v + r_0(C′+2G+2C_a) + log r_0/T}. With r_0/N = C″T/L^c + 1/N → 0 this is L^{(−G+C_v+o(1))N}. Since G − C_v > E + 3, it is o(L^{−EN}). ✓
- The ghost-batch multiplier symmetrization is legitimate: everything after the batch is permutation-equivariant on existing memory particles, because later phases attach only to later births. ✓

### B16. "Completion of Theorem 3.5" — order verified
physical average = residue model + O(L^{−A′N})
= ∫_0^1 Π b_p·[untruncated memory expression with distinct-birth] dθ
= ∫ Π b_p·([truncated, distinct] + o(L^{−AN})) dθ
[truncated, distinct] = Σ_π μ(π)[…] = o(L^{−EN}) uniformly in θ
Π b_p ≤ 1; take A, A′ > E.
All choices are made in a valid order. ✓

### B17. Corollary 3.11 — verified line by line
- Blocks of length ⌈H⌉ with log H = O_J(TL^d), (3.49). Neighborhoods have bounded overlap.
- ‖A*f_j‖ ≤ ‖f_j‖^{1−1/R}⟨f_j, B_0^R f_j⟩^{1/(2R)} (spectral Hölder for B_0 ≥ 0).
- Gram matrix PSD, largest eigenvalue ≤ trace = d_j.
- (O(H)sup|f|²)^{1/(2R)} = exp(O_J(TL^d + √L)/L^{0.52}) = O(1). This uses d < 0.52 and 1/2 < 0.52; it is where 0.52 > 1/2 is needed.
- Hölder exponents 2, 2R/(R−1), 2R sum to 1.
- Σd_j ≤ XL^{−2RE}.
- Result: X^{1/2}L^{C_3}·(X^{1/2}L^{C_3})^{1−1/R}·X^{1/(2R)}L^{−E} = XL^{−E+2C_3−C_3/R}. ✓

### B18. Answer to the seat's central question (hidden loss exponential in N?)
Complete ledger of every factor in the length-N path sum after the reduction:

| item | cost | per | where paid |
|---|---|---|---|
| residue replacement (Lemma 3.6) | relative L^{−AN} × absolute mass L^{C_abs N} | whole sum | A > A′ + C_abs |
| baseline Π b_p | ≤ 1 (a gain) | whole sum | dropped |
| ghost operation G_i | L^{C_v} | each of N+1 visits | (3.37): G > E + C_v + 3 |
| projection P_d (small groups) | L^{C_s} | each edge (inside the clean norm) | (3.37): E_id > G + C_s + 2 |
| clean edge | L^{−E_id} | each edge | hypothesis (3.6) |
| μ̃ vs μ density | additive O_J(L^{C_1}sN/P_*) | each edge | negligible vs L^{−E_id} |
| free/active ban | additive O_{J,m}(L^{C_1}s/P_*) | each edge | negligible |
| dirty (store/promote) | 2L^{C_a}√(B/𝒟) | each edge | J large (3.37) |
| memory truncation | exp(−Ω(L²)) | whole sum | tail (3.28) |
| equality rank, small r | L^{(2G+2C_a+C′)r}, r < r_0 = o(N) | ≤ 2r edges | o(N) in the exponent |
| equality rank, large r | (CL^{C′}/P_*)^r × L^{C_h(N+1)} | whole sum | C″ > C_h + E |
| θ-integral (3.11) | sup over θ | whole sum | uniform in θ |
| boundary vector | ‖1_∅‖² = 1 + O_J(sN/P_*) | once | — |

Every cost that applies on every visit or edge (C_v, C_s) is independent of m, C_1, J, and both are inside (3.37). The constant C_a, which depends on m and C_1, appears on only o(N) edges, or is killed by J. **Nothing else costs L^c per visit.**

---

## C. Parameter-dependency table for §3

| constant | fixed where | depends on | used where | claimed independent of (status) |
|---|---|---|---|---|
| a<b<c<d<0.47 | Def 3.1 | fixed data | (3.1); exp(L^a) > \|k\|; U < exp(L^c) (L3.9); 0.52+d < 1 (L3.6); P_* = exp(L^c); (3.49) | x |
| c_0, C_0 | Def 3.1 | fixed data | \|S\|,\|B\| ≍ T; all products over groups; c_0 in (3.32), (3.37) | x |
| v_−, v_+ | Def 3.1 | fixed data | (3.5), (3.21), C_s, C_a | x |
| q ∈ (0,1) | Def 3.1 | fixed data | damping; ρ; (3.21); C_s | — |
| ℓ (must be ≥ 1, Obj. 2) | Def 3.1 | fixed data | t_g, 𝒟, C_s, C_abs | — |
| m, C_1 | external (Thm 4.1; depend on E_id, C_4) | E_id, C_4, ℓ, group bounds | (3.2), C_abs, C_a, C_h | J (needed and used: yes) |
| C_2 | Def 3.3 | external | x-threshold (exp(L^a) > L^{C_2}); log H | — |
| ζ, Θ | Def 3.2/3.3 | free | multipliers only | the bound is uniform in both (verified) |
| E | input to Thm 3.5 | — | (3.7), (3.37), C″ | — |
| ρ | §3.4 | q (ρ² > √q) | splitting; C_v, C_a | m, C_1, J ✓ |
| v | (3.21) | q, ρ, v_+ | Schur weight; C_v, C_a | m, C_1, J ✓ |
| C_v | (3.22) | v, ρ, q, v_+, C_0 | (3.22), (3.37), (3.47) | m, C_1, J ✓ verified |
| C_s | Lemma 3.10 | q, ℓ, v_−, C_0 | (3.33), (3.37) | m, C_1, J ✓ verified |
| G | (3.37) | E, C_v | (3.38), (3.47) | m, C_1, J ✓ |
| E_id | (3.37) | E, C_v, C_s | hypothesis (3.6) | m, C_1, J ✓ verified (statement of Thm 3.5) |
| C_abs | Lemma 3.4 | m, C_1, fixed data | absolute path mass L^{O(N)} | J ✓ verified |
| C_a | Lemma 3.8 (enlarged in 3.9) | m, C_1, ℓ, ρ, v, v_±, C_0 | (3.30), J-choice, (3.47) | J ✓ verified |
| J | (3.37) | E (via G), C_a (so m, C_1), c_0, ℓ | 𝒟, (3.32) | chosen last among the constants ✓ |
| M = J+ℓ | — | J | lists, Q_act, A_* | — |
| R = ⌈L^{0.52}⌉, N = 2R | Thm 3.5 | x | everywhere | — |
| γ | Thm 3.5 | external | CRT error exp(−γL+o(L)) | — |
| A′ | §3.2 | > E | summed residue error | — |
| A | Lemma 3.6 | A′, C_abs | relative error exp(−ANT) = L^{−AN} | — |
| h (Bonferroni) | Lemma 3.6 | A (h = K_A NT) | e_h truncation | — |
| P_* = exp(L^c) | (3.12) | x | μ̃/μ, (3.43), (3.45) | — |
| B = ⌈L²⌉ | (3.27) | x | Lemma 3.9 (√B = L), A_* | — |
| 𝒟 = C(M,ℓ)^{\|S\|} | (3.29) | J, ℓ, \|S\| | (3.30) | — |
| A_*, C′ | (3.39), (3.42) | x; C′ ≈ 5.1 for x ≥ x_0(J) | (3.42), (3.47), large rank | J ✓ (once x large) |
| C_h, C | (3.44) | m, C_1, v, ρ, … | large rank | J |
| C″ | (3.45) | C_h, C, C′, E | r_0 | — |
| r_0 | (3.45) | C″, N, T, L^c | split small/large rank | r_0/N → 0 ✓ |
| C_3 | Cor 3.11 input | external (§5's C_6) | (3.48) | must be fixed before E (Obj. 7; global order) |
| H | (3.49) | J, C_2 | Cor 3.11 blocks | — |
| x-threshold | — | J, m, C_1, C_2, γ, A, C″, G, … | — | uniform in ζ, Θ, k, X, K_ν beyond (3.2) ✓ |

No cycle inside §3. The order is E → (C_v, C_s fixed data) → G → E_id → [Thm 4.1: m, C_1] → C_a, C_h → J → x.
Numerically, at the paper's q = 1/2, ℓ = 1: ρ > 0.841 is required, and (3.21) then needs v ≳ 5·max(1, v_+). So C_v ≈ O(C_0 v_+ v/ρ) is a fixed but possibly large number (tens). Theorem 4.1 must deliver E_id > E + C_v + C_s + 5. The paper's quantifiers allow this (E_id is an arbitrary input to Theorem 4.1), but it is the `ideal` seat's burden.

---

## D. Computer check of Lemma 3.7 (exact memory identity)

Script: /tmp/transference_toy/memtoy2.py (and the earlier memtoy.py).
- One big group (primes P), no small groups, identity permutations, generic random complex coefficients κ_i (pattern, source list, target list, free labels), phase e(θσ_ikD_i), q = 0.6, ρ = 0.95, θ = 0.137.
- **Physical side:** sums over all ordered distinct lists, patterns C ⊆ {0..J−1} with |C| ≤ m, free labels of law μ_g banned from both endpoint lists. Weight V^{−M}·ΠV^{−t}·Πμ(f)·κ·e(…) times E_residue[(3.8)], computed prime by prime.
- **Memory side:** Π_p b_p × the sum over histories built exactly from the rules: (3.16) ghost operation (terminate −η/ρ, continue q/ρ², batch births (−ηV/ρ)μ̃ as sets of unborn primes); edge steps (i)–(iv) (ρ per old zero; store/drop; translate; promote old zeros with p ∤ D at V^{−1}; fresh μ̃); distinct-birth; empty final memory.
- The two sides are coded independently.

Results (relative difference |phys − mem|/|phys|; args = primes N k M J m):
```
3,5,7,11   2 1 1 0 0   rel 9.5e-16
3,5,7,11   4 1 1 0 0   rel 3.7e-15   (term 2904, promo 16680, store 9972 histories exercised)
3,5,7,11,13 4 2 1 0 0  rel 1.4e-13
3,5,7,11   5 1 1 0 0   rel 6.5e-15
3,5,7,11   3 1 2 1 1   rel 1.7e-16
5,7,11,13  3 2 2 1 1   rel 6.6e-16
3,5,7,11,13 3 1 2 1 1  rel 4.3e-15
3,5,7,11   4 1 2 1 1   rel 7.6e-16
3,5,7,11,13 3 1 2 2 1  rel 1.4e-14   (composite D = product of two shared labels)
(memtoy.py, M=2,J=1,m=1, P∈{5,7,11},{3,5,7},{3,5,7,11}, N=2..5, k=1,2): all rel ≤ 2.1e-15
```
Mutation controls on (3,5,7,11 4 1 1 0 0) and (3,5,7,11,13 3 1 2 1 1):
```
termination coefficient +η/ρ instead of −η/ρ : rel 0.289 / 0.182   (FAILS, as it should)
ghost birth without the factor V_g            : rel 0.029 / 0.019   (FAILS)
no ρ in step (ii)                             : rel 0.0049 / 0.0054 (FAILS)
distinct-birth rule removed                   : rel 15.0            (FAILS)
allow store with p | D                        : rel 3.7e-15         (vacuous: automatic from ban + distinct-birth)
allow promotion of newly stored particles     : rel 3.7e-15         (vacuous: residue Δ ≢ 0)
```
Negative control on the hypothesis "group primes exceed |k|":
```
3,5,7,11  4 k=3 :  rel 0.868  (3 | k: identity FAILS)
5,7,11,13 3 k=5 :  rel 0.900  (5 | k: FAILS)
5,7,11,13 3 k=4 :  rel 1.3e-15 (no group prime divides k: holds)
```
(An earlier 3-prime/M=2 instance agreed but exercised zero ghost terminations, so it could not have caught a ghost-rule error. I discarded it as evidence and re-ran with more primes than slots.)

Not covered by the computer toy:
- small groups (they are physical Haar coordinates, identical on both sides by construction);
- several big groups (the lifespan expansion is prime by prime, so groups only partition the primes and enter D multiplicatively);
- non-identity symmetrizing permutations (the identity is claimed for each fixed choice of permutations).
I checked these by hand.

---

## E. Citation table for §3

§3 uses no external theorem as an input. Its only tools are standard: Bonferroni inequalities, Stirling, CRT, the weighted Schur test (proved in the text as (3.18)), and spectral Hölder. The two external citations are context only.

| cited | paper says | source says (quote) | verdict |
|---|---|---|---|
| Helfgott–Radziwiłł [11, §1.5] (arXiv:2103.06853v2, read from /tmp/oaimath/011/refs/HR) | "Signed closed walks and repeated prime labels also occur in the divisibility-graph arguments of Helfgott and Radziwiłł [11, Section 1.5]" (p.10) | §1.5 "Strategy of proof": "Tr(A\|X)^{2k} can also be expressed as a sum over closed walks of length 2k in the graph (Γ ∪ Γ′)\|X … edges of Γ∪Γ′ have the weight 1−1/p (if they are edges of both Γ and Γ′) or −1/p … in Tr A^{2k}, we can consider only walks where every edge length p that appears, appears at least twice" | MATCH (context) |
| Pilatte [18, §§3, 5] (arXiv:2310.19357v3, refs/Pilatte) | same sentence, "[18, Sections 3 and 5]" | §3 "Reformulations of the main theorem": "the divisibility term 1_{p1\|n}⋯1_{pJ\|n} is replaced by the 'centred' product (1_{p1\|n} − 1/p1)⋯"; §5 "High trace bound for the non-backtracking operator" | MATCH (context) |
| (internal) "Theorem 3.1/3.4/3.6/3.7/3.8/3.11" | — | Definition 3.1 / Lemmas 3.4, 3.6, 3.7, 3.8 / Corollary 3.11 | misnumbered, COSMETIC (Obj. 1) |

Hedge-word count in §3: 30 matching lines for the pattern clearly|similarly|standard|same argument|same estimate|same bound|for completeness|it follows|uniformly|obvious|routine|easily|negligible|exactly|immediate|in particular (grep of paper_plain.txt lines 812–2303). There are 0 occurrences of "clearly", "obvious", "routine", "easily", "standard" or "the same argument". Hard-step instances:
- "Both changes are negligible" (L3.10): checked, additive exp(−L^c+O(T)).
- "It follows uniformly in d" (L3.10): checked.
- "For completeness, these conditional row bounds can be iterated" (§3.8): checked at the argument level.
- "the remaining weighted row costs are uniformly bounded" (L3.9): checked.
- "exactly the form in (3.26)" (L3.8, column): checked at the argument level.
- "similarly split" (ρ-splitting): checked.
None hides a gap.

---

## F. Verified line by line vs only skimmed

Verified line by line:
- Def 3.1–3.3, (3.3), the adjoint paragraph and (3.4).
- Lemma 3.4 and (3.5).
- The quantifiers of Theorem 3.5 against the proof.
- (3.8). Lemma 3.6 incl. (3.9), the Bonferroni degree, Stirling, the CRT count, the term count, the relative error. (3.10) and the summation over paths. (3.11).
- (3.12)–(3.14) by hand, incl. a numeric hand example. Both compatibility consequences. The baseline.
- §3.4: every ρ/η/V/μ̃ factor for every event type. (3.15)–(3.16).
- Lemma 3.7: exact on 13 computer instances with 6 mutations and 3 negative controls, plus two hand toys (N = 1 and N = 2, M = 1).
- (3.18)–(3.25). Lemma 3.8 row bound. (3.27)–(3.28).
- Lemma 3.9 incl. (3.31), (3.32).
- Lemma 3.10: the P_d normalization, (3.35)'s multiplier, the Fourier reduction and Θ.
- (3.37)–(3.38). (3.39)–(3.43), (3.45)–(3.47) and the display after (3.47).
- The Completion paragraph. Corollary 3.11 and (3.49).

Verified only at the level of the argument (I did not recompute the constants):
- Lemma 3.8 column bound (reversal of (3.23)–(3.26)).
- Lemma 3.10 density-perturbation and ban-removal bounds.
- §3.8 large rank: the backward induction with retained pivots, and pivots/dependents inside one operation "handled in their prescribed integration order".
- The ghost-batch multiplier symmetrization.
- The multi-group, small-group and permutation aspects of Lemma 3.7 (by hand, not by computer).

Skimmed: Figure 2 (illustrative only).

Not in scope and not checked: whether hypothesis (3.6) holds (Theorem 4.1); whether §5's lift reproduces exactly the operator 𝒜 of Def 3.3 (incl. Ψ(n/(ZD)), the 1/n weights, and |ζ| ≤ L^{C_4}); the global order involving C_3/C_6 and C_4.

---

## G. Verdict for §3

**HOLDS AS READ.** Theorem 3.5, conditional on (3.6), and Corollary 3.11 are proved with the asserted quantifiers (E_id depends only on E and Definition 3.1's data; J depends on E, m, C_1). The memory identity (Lemma 3.7) is exact; I confirmed it by computer, and the computer check can fail. The length-N path sum has no hidden per-visit loss beyond L^{C_v} (ghosts) and L^{C_s} (projection), both paid by (3.37). Remaining defects are cosmetic or expository: misnumbered cross-references, ℓ ≥ 1 left implicit, the free-draw law left implicit, and a sketched bijection. Section 3 does not establish (3.6) itself; any refutation of the paper must come from Theorem 4.1, the §5 lift (does it produce exactly the Def 3.3 operator, and is |ζ| ≤ L^{C_4}?), Theorem 5.1, or §6–§7.
