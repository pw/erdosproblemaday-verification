# Referee report — seat `prediction` — §3 "Prediction from short histories" (PDF pp. 11–16)
Paper: OpenAI, "A power saving for planar unit distances", 23 Sep 2026 (local copy /tmp/oaimath/167/paper/paper.pdf; every formula below was read from the rendered PDF, not from paper.txt).
Seat date: 2026-10-14. Also read for interfaces: §1.2 (pp. 2–4), §2.3–§2.5 (pp. 6–11, Prop 2.4, Lemmas 2.5–2.7), the Prop 4.4 paragraph that applies Cor 3.2 (p. 20), and §5.1 (Lemma 5.1, (5.7)–(5.9), Lemma 5.3; pp. 23–24) where Cor 3.3 / (3.17) are applied.

## Verdict for this scope
**HOLDS AS READ.** Every step of §3 (laws (3.1)–(3.6), Lemma 3.1, the remark after it, Cor 3.2, (3.13)–(3.14) and the union-bound / equivalent-draw remarks, Cor 3.3, (3.17), §3.4) was checked line by line and found correct. No FATAL, no GAP. Objections below are COSMETIC / UNCLEAR only. The constant in (3.7) is even better than stated (2^{5/4}BB' ≈ 2.38BB', not 4BB'). A numerical simulation on explicit finite laws reproduces every identity exactly (to 1e-16) and the inequalities with large slack, and six deliberately broken variants (controls) each FAIL in the predicted way — which shows the lemma's hypotheses (conditioning on the history; the fresh test having the same law as the history tests; the product reference law; the −2 coefficient; uniform independent hashing; a hash-free prediction) all actually matter, so the lemma is not vacuously true.

§3 contains nothing Euclidean: it is a statement about an arbitrary finite law ω on P×Q (brief item (i): confirmed). Its only input from the geometry is D = o(log t) (Lemma 2.7), and its outputs are used in exactly two places — Prop 4.4 (Cor 3.2 with a FIXED alphabet M = M(B,τ)) and (5.7) (Cor 3.3 via (3.17), feature norms √3, √6). I checked that the √M feature-norm cost of Cor 3.2 never meets a growing alphabet: the template count M ≤ L^{2Kk} of (5.8) is used only as a collision count (Lemma 5.3, M/d(p)), never as a feature dimension in Lemma 3.1.

## Status per item (the deliverable)
| Item | Status |
|---|---|
| (3.1) wedge law, point-pair marginal π, both marginals μ | VERIFIED LINE BY LINE (also numerically exact) |
| (3.2) D finite ("π(p,r)>0 implies µ(p)µ(r)>0") | VERIFIED |
| (3.3) chain rule; data-processing derivation from it | VERIFIED; citation MATCH (see table) |
| (3.4) Pinsker 2TV² ≤ D in nats | VERIFIED; citation MATCH (natural-log constant correct) |
| (3.5) | VERIFIED |
| (3.6) µ_h | VERIFIED |
| Lemma 3.1 statement | VERIFIED |
| Lemma 3.1 proof: freezing, data processing on the PAIR transcript | VERIFIED LINE BY LINE |
| — reference law b_{j,h,h'} = (c_{T_j})_*µ_h ⊗ (c_{T_j})_*µ_{h'} | VERIFIED LINE BY LINE |
| — (3.8) iterated chain rule over the pair transcript | VERIFIED LINE BY LINE (numerically: chain sum == transcript KL ≤ D, every run) |
| — (3.9) | VERIFIED |
| — residuals U_j centred and independent under the reference product; (3.10) | VERIFIED LINE BY LINE |
| — (3.11) exact identity | VERIFIED LINE BY LINE (numerically max error 8.3e-17) |
| — Cauchy–Schwarz chain to 4BB'(D/K)^{1/4} | VERIFIED (true constant 2^{5/4}) |
| — "replace T_j by a fresh test after that prefix" | VERIFIED |
| — fixing a prefix, M^{j−1} ≤ M^{K−1} | VERIFIED |
| Remark on two different histories (p. 13) | VERIFIED (accurate description of the proof) |
| Cor 3.2 (feature e_c, coefficient 1_{A_T(q)}, √M) | VERIFIED LINE BY LINE (numerically: identity ⟨f−m,g⟩ = s_pred − s_act to 3e-16) |
| (3.13) sampling law and its marginals | VERIFIED LINE BY LINE (numerically exact) |
| (3.14) collision bound | VERIFIED LINE BY LINE (numerically) |
| union-bound remark | VERIFIED |
| "equivalent way to draw the point pair" | VERIFIED (numerically: identical pair law) |
| coordinate-quantization paragraph (p. 14) + its use in Prop 4.4 (p. 20) | VERIFIED as an interface (the rest of Prop 4.4 is another seat's scope: SKIMMED) |
| Cor 3.3: inner product = hashed strict-cross indicator | VERIFIED (exhaustive over [L]²×[L]², L=2,3,4) |
| Cor 3.3: 2/L per comparison, 4/L total, "no current hash" | VERIFIED LINE BY LINE (+ exact enumeration + MC) |
| Cor 3.3: 4√18 < 18, history count (L²)^{K−1} ≤ L^{2K} | VERIFIED |
| (3.17) integrated form; W = 0 case; "consistency implies strict cross" | VERIFIED |
| §3.4 K, L, k and every consequence | VERIFIED LINE BY LINE |
| Lemma 5.1 / (5.7) as consumers of §3.4 and (3.17) | VERIFIED as an interface |
| Lemma 2.7 (input D = o(log t)) | arithmetic re-done as an interface check (other seat's scope) |

## Line-by-line notes (what was checked, and how)

**(3.1)–(3.2).** Ω(p,q,r) = κ(q)ω(p|q)ω(r|q); π(p,r) = Σ_q Ω. Row sum: Σ_r π(p,r) = Σ_q κ(q)ω(p|q) = Σ_q ω(p,q) = µ(p). D finite because π(p,r) ≤ Σ_q ω(p,q) = µ(p) and likewise ≤ µ(r).

**Data processing (p. 12).** "adjoin the map to the outcome and then discard the nonnegative conditional term": KL(a_X‖b_X) = KL(a_{X,φ(X)}‖b_{X,φ(X)}) = KL(a_φ‖b_φ) + E KL(a_{X|φ}‖b_{X|φ}) ≥ KL(a_φ‖b_φ). Correct.

**Lemma 3.1 proof.** Freeze T_1..T_K; τ(p) := (c_{T_1}(p),…,c_{T_K}(p)). Map (p,r) ↦ (τ(p),τ(r)): image of π vs image of µ⊗µ = τ_*µ ⊗ τ_*µ, KL ≤ D. The pair transcript is the sequence Z_j = (c_{T_j}(p), c_{T_j}(r)); its prefix is the PAIR (H_j(p), H_j(r)). Under the reference µ⊗µ, conditioning on (H_j(p),H_j(r)) = (h,h') leaves p ~ µ_h and r ~ µ_{h'} independent, so the next pair has law (c_{T_j})_*µ_h ⊗ (c_{T_j})_*µ_{h'} = b_{j,h,h'} exactly (µ_h "formed with H_j", as the paper says). Positivity: an actual prefix pair of positive π-image probability is attained by some (p,r) with π(p,r) > 0, hence µ(p)µ(r) > 0, hence positive reference probability — so every a_{j,h,h'} that appears has a defined b_{j,h,h'}, and (Cover–Thomas chain rule, iterated) Σ_j E_π KL(a_{j,H_j(p),H_j(r)} ‖ b_{j,H_j(p),H_j(r)}) = KL(transcript images) ≤ D. That is (3.8), with equality in the middle step.
(3.9): Pinsker termwise, TV ≤ √(KL/2), then Jensen over (j, prefix pair): (1/K)Σ_j E TV ≤ √((1/K)Σ_j E KL/2) ≤ √(D/(2K)).
Residual U_j(x) = f_{T_j}(c_{T_j}(x)) − m_{T_j,H_j(x)} is ONE function applied to both endpoints; given the prefix pair (h,h'), U_j(p) is a function of c_{T_j}(p) alone (h fixed) and U_j(r) of c_{T_j}(r) alone. Under b_{j,h,h'}: E U_j(p) = Σ_x µ_h(x) f(c(x)) − m_{T_j,h} = 0, likewise for r with h', and the two are independent, so E_b⟨U_j(p),U_j(r)⟩ = 0. F_{h,h'}(c,c') := ⟨f(c)−m_h, f(c')−m_{h'}⟩ has ‖F‖_∞ ≤ (2B)² = 4B², so by (3.5) |E_a F| ≤ 8B² TV(a,b). Summing gives (3.10) (in fact with absolute values).
(3.11): under the wedge law, p and r are i.i.d. ω(·|q) given q, and U_j is a fixed function of a single point (tests frozen), so E[⟨U_j(p),U_j(r)⟩ | q] = ‖E_{p∼ω(·|q)}U_j(p)‖². Exact. Hence every summand of (3.10) is ≥ 0 — this nonnegativity is what turns the AVERAGE bound (3.10) into control of each X_j := E_q‖E_{p|q}U_j‖² on average.
Target with T_j in place of T: E_{(p,q)∼ω}⟨U_j(p), g_{T_j}(q)⟩ = E_{q∼κ}⟨E_{p|q}U_j(p), g(q)⟩ (since ω(p,q) = κ(q)ω(p|q)), so |·| ≤ B' E_q‖E_{p|q}U_j‖ ≤ B'√X_j. Then (1/K)Σ_j B'√X_j ≤ B'√((1/K)Σ_j X_j) ≤ B'(8B²√(D/(2K)))^{1/2} = 2^{3/2}·2^{−1/4} BB'(D/K)^{1/4} = 2^{5/4}BB'(D/K)^{1/4} ≤ 4BB'(D/K)^{1/4}. Note this holds for EVERY frozen sequence, not only on average; my simulation checks that stronger statement (0 violations in 1,400 frozen sequences).
Fresh-test step: the step-j quantity Φ_j = |E_{(p,q)}⟨f_{T_j}(c_{T_j}(p)) − m_{T_j,H_j(p)}, g_{T_j}(q)⟩| is a function of (T_1,…,T_{j−1},T_j) only; by i.i.d., (T_1,…,T_{j−1},T_j) has the same joint law as (T_1,…,T_{j−1},T) with T fresh, and J is independent of the tests, so E_J E Φ_J(T_1..T_{J−1},T_J) = LHS of (3.7). Correct. The direct fresh-test Monte Carlo in the simulation agrees with the frozen-sequence average to within MC error at every K (e.g. K=16: 0.0231±0.0008 vs 0.0222).
Fixing a prefix: some (j, t_1..t_{j−1}) has E_T|…| ≤ the average (measurability assumed in the text, p. 12, "all maps and integrands below are assumed measurable"); its history map takes ≤ M^{j−1} ≤ M^{K−1} values; the fresh T is independent of a deterministic map. Correct.

**Remark after the proof (p. 13).** "The reference law uses the first endpoint's prediction at the first coordinate and the second endpoint's prediction at the second. No independence of the actual endpoints after their histories have been specified is asserted. Their independence is used only conditional on the center, in (3.11)." Accurate: the actual conditionals a_{j,h,h'} are never assumed to be products. (FAIL control 3 shows that the "same-history" reference (c)_*µ_h ⊗ (c)_*µ_h would break (3.8): its chain sum is +∞ on law A.)

**Cor 3.2.** f_T(c) = e_c (norm 1, B = 1), g_T(q) = 1_{A_T(q)} ∈ {0,1}^M (norm ≤ √M = B'). ⟨f(c(p)), g(q)⟩ = 1{c(p) ∈ A(q)}; ⟨m_{T,H(p)}, g(q)⟩ = Σ_x µ_{H(p)}(x)1{c(x) ∈ A(q)}; the edge-average of the difference is (1−s_act) − (1−s_pred) = s_pred − s_act ("differ by the negative of their acceptance probabilities"). Since s_0 = E_T s_act does not depend on the history, averaging (3.7) gives E_{prefix}E_T s_pred ≤ s_0 + 4√M(D/K)^{1/4}; fix a prefix at or below the average → (3.12). Correct.

**(3.13)–(3.14), union bound, equivalent draw.** p̂-marginal: Σ_p µ(p)µ_{H(p)}(x) = Σ_h µ(H=h)µ_h(x) = µ(x). (p,q_j) has law µ(p)ω(q_j|p) = ω(p,q_j); q_j has marginal κ. Law of (p̂, q_j) = Σ_p ω(p,q_j)µ_{H(p)}(p̂) — exactly the weight in the LHS of (3.12), so P(c_T(p̂) ∉ A_T(q_j)) for a fresh T equals the LHS of (3.12) for each j, and the union bound over j = 1..r needs no independence (as stated). (3.14): Σ_h Σ_{p∈h} µ(p)²/µ(H=h) ≤ Σ_h max_p µ(p) = |H(P)| max µ. Equivalent draw: µ(p)µ_{H(p)}(p̂) = µ(H=h)µ_h(p)µ_h(p̂) with h = H(p) = H(p̂) — identical (numerically confirmed). "If K = o(log t), D/K = o(1), and max_p µ(p) ≤ t^{−1+o(1)}, then the prediction failure and the collision probability both tend to zero": with M fixed, r(0 + 4√M(D/K)^{1/4}) → 0 and M^{K−1}t^{−1+o(1)} = t^{−1+o(1)} → 0. Correct. Interface with Prop 4.4 (p. 20): M = M(B,τ) "independent of t and of the field degree", acceptance = "point code is attained by some actual neighbor of q" (so s_0 = 0, and acceptance of p̂ at q_j does hand an actual neighbour of q_j with the same code as p̂ — brief item (iv), first question: yes, by definition of A_T), history chosen "after averaging the prediction failure over that fresh embedding; the embedding itself is not fixed" — consistent with Cor 3.2 (the tuple (p,p̂,q_1,q_2,q_3) of (3.13) is drawn independently of the fresh σ for the fixed deterministic H, which is what (4.5)/(4.6) need).

**Cor 3.3.** Feature f(a,b) = (e_a, e_b, e_{(a,b)}), ‖f‖ = √3; coefficient g(q) = (e_{a_q}, e_{b_q}, −2e_{(a_q,b_q)}), ‖g‖ = √6; ⟨f,g⟩ = 1{a=a_q} + 1{b=b_q} − 2·1{(a,b)=(a_q,b_q)} ∈ {1 (exactly one agrees), 0 (both or neither)} — EXACTLY the hashed strict-cross indicator (exhaustively confirmed; the −1 coefficient fails 29 cases). Lemma 3.1 with B = √3, B' = √6 gives 4√18(D/K)^{1/4}; d = 2L + L² is irrelevant (the bound is dimension-free). Hash accounting: conditional on the true test T, the hash values of distinct attained labels are i.i.d. uniform on [L], same map for points and centres in each coordinate, independent across coordinates and tests. For two FIXED true states the hashed and true strict-cross indicators can differ only through a collision of truly unequal labels: probability max(2c(1−c), c) with c = 1/L, ≤ 2/L (exact enumeration agrees). Actual pair: (p,q) ∼ ω is independent of the current hashes. Predicted pair: x ∼ µ_{H(p)}, where H is built from EARLIER augmented tests (earlier hashes) — "the predicted point is sampled by (3.6) using no current hash" is literally true, so the current hash is independent of (x,q). Chain actual-true → actual-hashed (2/L) → predicted-hashed (Lemma 3.1) → predicted-true (2/L): 4/L + 4√18(D/K)^{1/4}, and 4√18 = 16.97 < 18. The predicted-true quantity does not involve the current hashes, so averaging over them before fixing the prefix is legitimate. History values ≤ (L²)^{K−1} ≤ L^{2K}. FAIL control 6 shows "no current hash" is load-bearing: drawing the prediction from p's CURRENT hashed fibre gives flip rate 0.69 (L=4) and 0.60 (L=8) against 2/L = 0.5, 0.25.

**(3.17).** With tests τ ∼ dτ/W, multiply (3.16) by W: W·E_T[…] = ∫_T […]dτ, W·s_0 = ∫ P(strict-cross fails at τ)dτ ≤ ∫ m(τ)dτ. Correct. "Consistency implies the strict-cross relation": consistent = (Y=1 and exactly A agrees) or (Y=0 and exactly B1 agrees), both of which are "exactly one coordinate agrees"; so strict-cross failure ≤ inconsistency, i.e. m may be the inconsistency probability. Correct. Consumer (5.7): k³(∫_C m + W_c(4/L + 18(D/K)^{1/4})) ≤ k³·O(1) + k^{3+1/16}·S·O(e_t) = o(S) using ∫m = O(1), W_c ≤ S/ε, ε = k^{−1/16}, k³/S → 0, k^{20}e_t → 0 (Lemma 5.1). Correct.

**§3.4.** T_0 = log t, D = o(T_0). K = ⌈√((D+1)T_0)⌉ → ∞; K/T_0 ≤ √((D+1)/T_0) + 1/T_0 → 0; D/K ≤ D/√((D+1)T_0) ≤ √(D/T_0) → 0 (true whether D stays bounded or diverges — and D may diverge: Lemma 2.7's own bound is D ≤ (a+o(a)) log t + O(1) with a log t → ∞, so no step may assume D bounded, and none does). Fixed M: M^K = e^{K log M} = t^{o(1)}. L = ⌊exp√(T_0/K)⌋ → ∞ (T_0/K → ∞), eventually ≥ 2; K log L ≤ √(KT_0) = T_0√(K/T_0) = o(T_0), so L^{2K} = t^{o(1)}. k = ⌊min{(T_0/(K log L))^{1/2}, η_t^{−1/40}}⌋: kK log L ≤ √(T_0 K log L) = o(T_0); k^{20}η_t ≤ η_t^{1/2} → 0; k → ∞ since both arguments diverge (η_t positive, → 0). "Further finitely many slow-growth requirements": all requirements in use (kK log L = o(T_0), k^{20}(…) → 0, k³/S → 0) are monotone in k, so shrinking k preserves them. No circularity: η_t = (D/K)^{1/4} + 1/L + 1/S + 1/d_{Q,min} is determined before k (S is a property of the configuration, not of the tests). Correct.

**Lemma 2.7 interface (other seat's scope; arithmetic only).** H(p,r) ≥ (1−P(p=r))log(1/M_t), log(1/M_t) = (2+3a+o(a))log t − log 2; H(p) ≤ (1+2a+o(a))log t; so D ≤ (a + o(a) + O(t^{−a+o(a)}))log t + O(1) = o(log t). Matches (2.18).

## Objections (all minor)
1. **COSMETIC — constant.** p. 12/13, (3.7) "≤ 4BB′(D/K)^{1/4}" and the last display of the proof "B′(8B²√(D/(2K)))^{1/2} ≤ 4BB′(D/K)^{1/4}". The left side equals 2^{5/4}BB′(D/K)^{1/4} ≈ 2.378·BB′(D/K)^{1/4}; the stated 4 is valid but loose. Downstream "4√18 < 18" and "4√M" inherit valid but loose constants. No fix needed.
2. **COSMETIC — cross-reference labels.** p. 13 "In the setting of Theorem 3.1" (Corollary 3.2), p. 15 "Therefore Theorem 3.1 compares its actual and predicted probabilities" and "One form of Theorem 3.3 that will be convenient", p. 20 "By Theorem 2.7, D = o(log t)… Apply Theorem 3.2", p. 23 "use Theorem 3.3". The objects are labelled Lemma 3.1, Corollary 3.2, Corollary 3.3, Lemma 2.7. Each points to the intended result.
3. **COSMETIC — symbol clash s_0.** Lemma 2.5 (p. 8) uses s_0 for an absolute threshold constant ("there are absolute constants s_0 > 0, C"); Cor 3.2 (p. 13) and Cor 3.3 (p. 15) reuse s_0 for the actual acceptance / strict-cross failure probability ("s_0 = E_T P_{(p,q)∼ω}{c_T(p) ∉ A_T(q)}"). The meanings never interact inside §3, but a reader of §5 (which uses both Lemma 2.5 and (3.16)) must keep them apart.
4. **UNCLEAR (exposition) — p. 14:** "Geometric estimates valid for all couplings with these marginals remain valid for each fixed history." The sentence does not say which marginals. The correct and sufficient reading is: any estimate that uses only (a) the one-point law µ of p and of p̂, (b) the edge law of each (p,q_j), and (c) the independence of the fresh test from the whole tuple (3.13), holds for every fixed H. That is exactly what Prop 4.4 uses (tails (4.5)/(4.6) at a fresh σ applied to height functions of p, p̂, q_j, and of differences, bounded via (4.4) by marginal heights). No gap; a one-line clarification would suffice.
5. **COSMETIC — p. 14:** "additional nonnegative error quantities can be averaged together with the prediction error before choosing a prefix; this always leaves the test fresh." True, but the selected prefix bounds each quantity only by the SUM of the averages, not by its own average. Every application uses o(1)+o(1) or o(S)+o(S), so harmless.
6. **COSMETIC — p. 12:** "Every realized history has at most M^{K−1} values." For prefix length J−1 the count is M^{J−1}; the stated bound is the maximum, as used. Fine.
(No objection to the measurability conventions: in the two applications the test spaces are the finite set of field embeddings (Prop 4.4) and the level space with step-function state maps (§4.4, "All class comparisons are threshold comparisons and all cell indices are measurable functions of s", p. 22).)

## Answers to brief item (iii)
- (3.8) is a correct use of the chain rule: the conditioning variable is the PAIR of prefixes (H_j(p),H_j(r)), the actual conditional law a_{j,h,h'} is arbitrary (not assumed product), and the reference conditional law under µ⊗µ is exactly the product of the two conditional pushforwards (c_{T_j})_*µ_h ⊗ (c_{T_j})_*µ_{h'}. Confirmed algebraically and numerically (chain sum = transcript KL ≤ D in every frozen sequence tested).
- (3.11) is exact: it uses only that p, r are i.i.d. ω(·|q) given q under the wedge law and that U_j is one fixed function of one point. Numerically exact to 8e-17.
- Replacing T_j by a fresh test preserves the joint law with the strict prefix: yes, by i.i.d. tests and independence of J.
- Cor 3.3: the inner product is exactly the hashed strict-cross indicator; the 4/L accounting is right (2/L actual + 2/L predicted); the predicted point is sampled from µ_{H(p)} with H built from earlier augmented tests only, so it uses no current hash. All three confirmed exhaustively / by enumeration, with failing controls for each.

## Finite check (script VERBATIM, output, controls)
Script: /tmp/oaimath/167/checks/prediction_sim.py (sha256 e500527feefd5380daef344d2b8d1852c0ad7c35670621f1a34ac33b845bf9b8), run as `nice -n 19 python3 -P prediction_sim.py` (3 min 27 s; `-I` could not be used because numpy lives in the user site-packages — the script reads no downloaded file). Output: /tmp/oaimath/167/checks/prediction_sim.out.

What it does:
- **A.** Random unbalanced bipartite graph, |P| = 30, |Q| = 200, centre degrees uniform in {2..8}, ω = uniform edge law; D computed EXACTLY (0.266591 nats). Tests: random code P→[3], random features on the radius-1 sphere in R², coefficients g(q) ADVERSARIALLY ALIGNED with E_{p|q}f(c(p)) − E_µ f(c(p)) (legal: g may depend arbitrarily on the test), B = B' = 1. For K ∈ {1,…,64}: 200 frozen sequences each — exact Φ_j, exact (3.11) identity, (3.10) and nonnegativity, chain-rule sum vs transcript KL vs D; plus a direct fresh-test Monte Carlo of the LHS of (3.7) (3,000 draws of J, prefix, independent fresh T).
- **A'.** Cor 3.2 with A_T(q) = codes of actual neighbours (s_0 = 0): identity ⟨f−m,g⟩ = s_pred − s_act; per-sequence average vs 2^{5/4}√M(D/K)^{1/4}; (3.13) marginals, (3.14), equivalent draw — all exact.
- **B.** Planted two-block law (two complete bipartite blocks, D = log 2 exactly) with the "half test" (code = block, f = ±1, g = ±1), K = 10,000, bound 4(D/K)^{1/4} = 0.365.
- **C.** Cor 3.3 pieces: exhaustive inner-product identity; exact hash-flip enumeration; MC of the "no current hash" property.

FAIL controls (each must and does violate the corresponding bound/identity):
1. Prediction from µ (history ignored): discrepancy 1.0000 > 0.3650. (Correct conditioning: 0.0001 = 1/K.)
2. Fresh test NOT identically distributed with the history tests (prefix tests trivial, fresh = half test): 1.0000 > 0.3650. This is precisely the "replace T_j by a fresh test" step failing when its hypothesis fails.
3. Wrong reference law in (3.8) (first endpoint's history used for both coordinates): chain sum = +∞ > D (correct reference: 0.266591 = transcript KL ≤ D).
4. Coefficient −1 instead of −2 in g: 29 mismatches with the strict-cross indicator (paper's −2: 0 mismatches).
5. Non-uniform hash (value 0 w.p. 1/2+1/(2L)): worst flip 0.4512 > 2/L = 0.25 at L = 8; 0.4175 > 0.125 at L = 16 (uniform hash: 0.2188 and 0.1172, within 2/L).
6. Prediction drawn from p's CURRENT hashed fibre: flip 0.6932 > 0.5 (L=4), 0.6025 > 0.25 (L=8); hash-free prediction 0.3705 and 0.2161, within 2/L.

Honest limits of the check: in experiment A the bound 4BB'(D/K)^{1/4} exceeds the trivial bound 2BB' for K ≤ 4, so the comparison is non-vacuous only for K ≥ 8; observed per-sequence discrepancies are at least 14.6× below the bound (worst ratio 0.0685), mean discrepancies 27× (K=1) to 185× (K=64) below it, i.e. random instances are far from extremal, and experiment B is what shows the history mechanism doing real work. With |P| = 30, long histories separate all points (µ_h = δ_p), so I did not run an end-to-end (3.16) experiment at the K needed to make 18(D/K)^{1/4} < 1 (that needs D/K < 1e-5); instead each link of the Cor 3.3 chain was checked separately. A finite check cannot test the asymptotic §3.4 claims; those were done algebraically above.

### Output (VERBATIM)
```
=== A. random unbalanced bipartite graph, |P|=30, |Q|=200, center degrees uniform in {2..8}
|P|=30 |Q|=200 |E|=988  D=KL(pi||mu x mu)=0.266591 nats
marginal check: pi rows sum to mu: True, cols: True
tests: c uniform random P->[3], f random on sphere radius B=1.0 in R^2, g aligned with neighbourhood mean, |g|<=B'=1.0
K=  1: per-frozen-sequence max avg_j Phi_j=0.1884  mean=0.1062 | fresh-test MC (3.7) LHS=0.1057+-0.0007 | 2^(5/4)BB'(D/K)^(1/4)=1.7090  4BB'(D/K)^(1/4)=2.8742 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
K=  2: per-frozen-sequence max avg_j Phi_j=0.1656  mean=0.1013 | fresh-test MC (3.7) LHS=0.1014+-0.0006 | 2^(5/4)BB'(D/K)^(1/4)=1.4371  4BB'(D/K)^(1/4)=2.4169 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
K=  4: per-frozen-sequence max avg_j Phi_j=0.1161  mean=0.0808 | fresh-test MC (3.7) LHS=0.0797+-0.0007 | 2^(5/4)BB'(D/K)^(1/4)=1.2085  4BB'(D/K)^(1/4)=2.0324 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=8.3e-17 | (3.10)&nonneg: True
K=  8: per-frozen-sequence max avg_j Phi_j=0.0610  mean=0.0431 | fresh-test MC (3.7) LHS=0.0437+-0.0009 | 2^(5/4)BB'(D/K)^(1/4)=1.0162  4BB'(D/K)^(1/4)=1.7090 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
K= 16: per-frozen-sequence max avg_j Phi_j=0.0320  mean=0.0222 | fresh-test MC (3.7) LHS=0.0231+-0.0008 | 2^(5/4)BB'(D/K)^(1/4)=0.8545  4BB'(D/K)^(1/4)=1.4371 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
K= 32: per-frozen-sequence max avg_j Phi_j=0.0161  mean=0.0107 | fresh-test MC (3.7) LHS=0.0107+-0.0006 | 2^(5/4)BB'(D/K)^(1/4)=0.7186  4BB'(D/K)^(1/4)=1.2085 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
K= 64: per-frozen-sequence max avg_j Phi_j=0.0082  mean=0.0055 | fresh-test MC (3.7) LHS=0.0055+-0.0004 | 2^(5/4)BB'(D/K)^(1/4)=0.6042  4BB'(D/K)^(1/4)=1.0162 | seq>sharp: 0/200 | (3.8)chain==transcriptKL<=D: True | (3.11) max|diff|=5.6e-17 | (3.10)&nonneg: True
worst observed (per-sequence average)/(4BB'(D/K)^(1/4)) over all K: 0.0685

=== A'. Cor 3.2 acceptance (A_T(q) = codes of actual neighbours of q, so s0 = 0), M=3
K=  4: per-sequence avg_j s_pred,j : max=0.0951 mean=0.0849  <= 2^(5/4) sqrt(M)(D/K)^(1/4)=2.0931 [paper 4 sqrt(M)(D/K)^(1/4)=3.5202] : True; identity <f-m,g> == s_pred - s_act : max err 3.3e-16
K= 16: per-sequence avg_j s_pred,j : max=0.0256 mean=0.0230  <= 2^(5/4) sqrt(M)(D/K)^(1/4)=1.4801 [paper 4 sqrt(M)(D/K)^(1/4)=2.4892] : True; identity <f-m,g> == s_pred - s_act : max err 3.1e-16
K= 64: per-sequence avg_j s_pred,j : max=0.0064 mean=0.0057  <= 2^(5/4) sqrt(M)(D/K)^(1/4)=1.0466 [paper 4 sqrt(M)(D/K)^(1/4)=1.7601] : True; identity <f-m,g> == s_pred - s_act : max err 2.8e-16
(3.13) marginals: p-marginal==mu True, phat-marginal==mu True; (3.14) P(p=phat)=0.6408 <= |H(P)| max mu = 0.9808
'equivalent way to draw the pair' (h~mu(H=h), then two iid from mu_h) equals (3.13) pair law: True

=== B. planted two-block law (D = log 2 exactly) and FAIL controls
D = 0.693147, log 2 = 0.693147
K=10000: correct conditioning  avg_j Phi_j = 0.000100  (expect 1/K = 0.0001)  <= 4BB'(D/K)^(1/4) = 0.3650: True
FAIL control 1 (prediction from mu, history ignored): avg Phi = 1.0000 > bound 0.3650: VIOLATES = True
FAIL control 2 (fresh test NOT identically distributed with the prefix tests: prefix trivial, fresh = half test): Phi at the fresh test = 1.0000 > bound 0.3650: VIOLATES = True
FAIL control 3 (law A, K=8): chain sum with correct b = 0.266591 (== transcript KL 0.266591 <= D=0.266591); with WRONG reference b=(c)_*mu_h x (c)_*mu_h : inf -> exceeds D: True

=== C. Cor 3.3: feature/coefficient inner product == hashed strict-cross indicator (exhaustive)
paper (-2): mismatches over all L in {2,3,4} = 0; norms (|f|,|g|) = [(1.732051, 2.44949)] (paper: sqrt3=1.732051, sqrt6=2.449490)
FAIL control 4 (coef -1): mismatches over all L in {2,3,4} = 29; norms (|f|,|g|) = [(1.732051, 1.732051)] (paper: sqrt3=1.732051, sqrt6=2.449490)

=== C'. hashing: P(true strict cross != hashed strict cross) <= 2/L for any two fixed true states (exact enumeration)
L=2: uniform independent hash worst flip prob (enumeration) = 0.5000, formula max(2c(1-c),c) = 0.5000, <= 2/L = 1.0000: True;  non-uniform hash: enumeration 0.6250, formula 0.6250
L=3: uniform independent hash worst flip prob (enumeration) = 0.4444, formula max(2c(1-c),c) = 0.4444, <= 2/L = 0.6667: True;  non-uniform hash: enumeration 0.5000, formula 0.5000
L=8: uniform hash worst flip = 0.2188 <= 2/L=0.2500: True;  FAIL control 5 (hash value 0 w.p. 1/2+1/(2L)): worst flip = 0.4512 > 2/L: True
L=16: uniform hash worst flip = 0.1172 <= 2/L=0.1250: True;  FAIL control 5 (hash value 0 w.p. 1/2+1/(2L)): worst flip = 0.4175 > 2/L: True

=== C''. 'predicted point sampled using no current hash' is load-bearing (MC)
L=4: predicted-pair E|true - hashed|: hash-free prediction (mu) 0.3705 <= 2/L=0.5: True;  FAIL control 6 (prediction drawn from p's CURRENT hashed fibre): 0.6932 > 2/L: True
L=8: predicted-pair E|true - hashed|: hash-free prediction (mu) 0.2161 <= 2/L=0.25: True;  FAIL control 6 (prediction drawn from p's CURRENT hashed fibre): 0.6025 > 2/L: True
```

### Script (VERBATIM)
```python
#!/usr/bin/env python3
"""Numerical check of Lemma 3.1 / Cor 3.2 / Cor 3.3 of the OpenAI unit-distance preprint (Sec. 3).
Seat `prediction`.  Everything finite and exact except where marked MC (Monte Carlo over tests).
Run: nice -n 19 python3 -I prediction_sim.py
"""
import numpy as np, math, itertools, sys
rng = np.random.default_rng(20261014)

# ---------------------------------------------------------------- the law
def law_from_adj(adj):
    adj = adj[adj.sum(1) > 0][:, adj.sum(0) > 0]          # "delete atoms of zero marginal mass"
    E = adj.sum()
    omega = adj / E                                       # uniform edge law
    mu = omega.sum(1); kappa = omega.sum(0)
    w_p_given_q = omega / kappa                           # columns sum to 1
    # wedge law (3.1): pi(p,r) = sum_q kappa(q) w(p|q) w(r|q)
    pi = (w_p_given_q * kappa) @ w_p_given_q.T
    ref = np.outer(mu, mu)
    m = pi > 0
    D = float((pi[m] * np.log(pi[m] / ref[m])).sum())
    return dict(adj=adj, omega=omega, mu=mu, kappa=kappa, wpq=w_p_given_q, pi=pi, D=D)

def random_unbalanced(nP=30, nQ=200, dlo=2, dhi=8):
    adj = np.zeros((nP, nQ))
    for q in range(nQ):
        d = rng.integers(dlo, dhi + 1)
        adj[rng.choice(nP, d, replace=False), q] = 1
    return adj

# ---------------------------------------------------------------- tests
# a test = (c : P->[M] int array, F : M x d feature matrix, G : Q x d coefficient matrix)
def random_test(law, M, d, B, Bp, aligned=True):
    nP = law['mu'].size
    c = rng.integers(0, M, nP)
    F = rng.normal(size=(M, d)); F *= B / np.maximum(np.linalg.norm(F, axis=1, keepdims=True), 1e-12)
    if aligned:   # adversarial-but-legal: g(q) aligned with E_{p|q} f(c(p)) - E_mu f(c(p))
        fc = F[c]
        v = law['wpq'].T @ fc - law['mu'] @ fc
        nv = np.linalg.norm(v, axis=1).max()
        G = Bp * v / nv if nv > 0 else np.zeros_like(v)
    else:
        G = rng.normal(size=(law['kappa'].size, d)); G *= Bp / np.linalg.norm(G, axis=1, keepdims=True)
    return (c, F, G)

def refine(labels, c):
    """history partition after appending code c: returns new integer labels"""
    key = labels * (c.max() + 1) + c
    _, new = np.unique(key, return_inverse=True)
    return new

def residual(law, labels, test, cond=True):
    """U(x) = f(c(x)) - m_{T,H(x)} with m_{T,h} = sum_x mu_h(x) f(c(x))   (cond=False: wrong, uses mu)"""
    c, F, G = test
    mu = law['mu']; fc = F[c]
    if not cond:
        return fc - mu @ fc
    U = np.empty_like(fc)
    for h in np.unique(labels):
        idx = labels == h
        muh = mu[idx] / mu[idx].sum()
        U[idx] = fc[idx] - muh @ fc[idx]
    return U

def phi(law, U, G):
    """|E_{(p,q)~omega} <U(p), g(q)>|"""
    return abs(float((law['omega'] * (U @ G.T)).sum()))

def frozen_sequence_stats(law, tests, cond=True, check_chain=False, wrong_ref=False):
    K = len(tests); nP = law['mu'].size
    labels = np.zeros(nP, dtype=np.int64)
    phis, Xs, inner, chain = [], [], [], 0.0
    for j, t in enumerate(tests):
        c, F, G = t
        U = residual(law, labels, t, cond)
        phis.append(phi(law, U, G))
        EU = law['wpq'].T @ U                          # E_{p~w(.|q)} U(p), shape Q x d
        X = float((law['kappa'] * (EU ** 2).sum(1)).sum())
        I = float((law['pi'] * (U @ U.T)).sum())
        Xs.append(X); inner.append(I)
        if check_chain:
            chain += chain_term(law, labels, c, wrong_ref)
        labels = refine(labels, c)
    return np.array(phis), np.array(Xs), np.array(inner), chain, labels

def chain_term(law, labels, c, wrong_ref=False):
    """E_{(p,r)~pi} KL(a_{j,H(p),H(r)} || b_{j,H(p),H(r)})  with b = (c)_*mu_h (x) (c)_*mu_h'.
    wrong_ref=True uses the WRONG reference (c)_*mu_h (x) (c)_*mu_h (first endpoint's history twice)."""
    pi, mu = law['pi'], law['mu']; M = c.max() + 1
    tot = 0.0
    H = np.unique(labels)
    push = {h: np.bincount(c[labels == h], weights=mu[labels == h], minlength=M) / mu[labels == h].sum() for h in H}
    for h in H:
        for hp in H:
            blk = pi[np.ix_(labels == h, labels == hp)]
            w = blk.sum()
            if w <= 0: continue
            a = np.zeros((M, M))
            np.add.at(a, (c[labels == h][:, None].repeat(blk.shape[1], 1), c[labels == hp][None, :].repeat(blk.shape[0], 0)), blk)
            a /= w
            b = np.outer(push[h], push[h] if wrong_ref else push[hp])
            m = a > 0
            if np.any(b[m] == 0):
                return math.inf
            tot += w * float((a[m] * np.log(a[m] / b[m])).sum())
    return tot

def transcript_KL(law, labels):
    """KL of the image of pi under (tau(p),tau(r)) vs image of mu x mu   (data processing: <= D)"""
    pi, mu = law['pi'], law['mu']
    H = np.unique(labels)
    A = np.array([[pi[np.ix_(labels == h, labels == g)].sum() for g in H] for h in H])
    m = np.array([mu[labels == h].sum() for h in H]); Bm = np.outer(m, m)
    k = A > 0
    return float((A[k] * np.log(A[k] / Bm[k])).sum())

def bound(B, Bp, D, K):  return 4 * B * Bp * (D / K) ** 0.25
def sharp(B, Bp, D, K):  return 2 ** 1.25 * B * Bp * (D / K) ** 0.25

out = print
# =============================================================== Experiment A: random unbalanced graph
out("=== A. random unbalanced bipartite graph, |P|=30, |Q|=200, center degrees uniform in {2..8}")
law = law_from_adj(random_unbalanced())
out(f"|P|={law['mu'].size} |Q|={law['kappa'].size} |E|={int(law['adj'].sum())}  D=KL(pi||mu x mu)={law['D']:.6f} nats")
out(f"marginal check: pi rows sum to mu: {np.allclose(law['pi'].sum(1), law['mu'])}, cols: {np.allclose(law['pi'].sum(0), law['mu'])}")
M, d, B, Bp = 3, 2, 1.0, 1.0
out(f"tests: c uniform random P->[{M}], f random on sphere radius B={B} in R^{d}, g aligned with neighbourhood mean, |g|<=B'={Bp}")
worst_ratio = 0.0
for K in [1, 2, 4, 8, 16, 32, 64]:
    seq_avgs = []; viol = 0; chain_ok = True; id_err = 0.0; c310_ok = True
    for rep in range(200):
        tests = [random_test(law, M, d, B, Bp) for _ in range(K)]
        ph, Xs, inner, chain, labels = frozen_sequence_stats(law, tests, check_chain=(rep < 20))
        id_err = max(id_err, float(np.max(np.abs(Xs - inner))))          # (3.11) exact identity
        if (inner < -1e-12).any(): c310_ok = False
        if inner.mean() > 8 * B * B * math.sqrt(law['D'] / (2 * K)) + 1e-12: c310_ok = False   # (3.10)
        if rep < 20:
            tk = transcript_KL(law, labels)
            if not (abs(chain - tk) < 1e-9 and tk <= law['D'] + 1e-12): chain_ok = False      # (3.8) chain rule + DP
        a = ph.mean(); seq_avgs.append(a)
        if a > sharp(B, Bp, law['D'], K) + 1e-12: viol += 1
        worst_ratio = max(worst_ratio, a / bound(B, Bp, law['D'], K))
    # direct fresh-test MC of (3.7): J uniform, prefix T_1..T_{J-1}, independent fresh T
    fresh = []
    for s in range(3000):
        J = rng.integers(1, K + 1)
        labels = np.zeros(law['mu'].size, dtype=np.int64)
        for _ in range(J - 1):
            labels = refine(labels, random_test(law, M, d, B, Bp)[0])
        T = random_test(law, M, d, B, Bp)
        fresh.append(phi(law, residual(law, labels, T), T[2]))
    fresh = np.array(fresh)
    out(f"K={K:3d}: per-frozen-sequence max avg_j Phi_j={max(seq_avgs):.4f}  mean={np.mean(seq_avgs):.4f} | fresh-test MC (3.7) LHS={fresh.mean():.4f}+-{fresh.std()/math.sqrt(len(fresh)):.4f} | "
        f"2^(5/4)BB'(D/K)^(1/4)={sharp(B,Bp,law['D'],K):.4f}  4BB'(D/K)^(1/4)={bound(B,Bp,law['D'],K):.4f} | seq>sharp: {viol}/200 | "
        f"(3.8)chain==transcriptKL<=D: {chain_ok} | (3.11) max|diff|={id_err:.1e} | (3.10)&nonneg: {c310_ok}")
out(f"worst observed (per-sequence average)/(4BB'(D/K)^(1/4)) over all K: {worst_ratio:.4f}")

# ---------------------------------------------------------------- Cor 3.2 on the same law
out("\n=== A'. Cor 3.2 acceptance (A_T(q) = codes of actual neighbours of q, so s0 = 0), M=3")
def acc_test(law, M):
    c = rng.integers(0, M, law['mu'].size)
    A = np.zeros((law['kappa'].size, M), bool)
    pp, qq = np.nonzero(law['adj']); A[qq, c[pp]] = True
    F = np.eye(M); G = A.astype(float)                       # f = e_c (|f|=1), g = indicator vector (|g|<=sqrt M)
    return (c, F, G), A
def s_pred(law, labels, c, A):
    fail = 0.0
    for h in np.unique(labels):
        idx = labels == h; muh = law['mu'][idx] / law['mu'][idx].sum()
        fail += float((law['omega'][idx].sum(0) * ((~A[:, c[idx]]) @ muh)).sum())
    return fail
for K in [4, 16, 64]:
    per_seq = []; ident = 0.0; coll = []
    for rep in range(200):
        labels = np.zeros(law['mu'].size, dtype=np.int64); vals = []
        for j in range(K):
            t, A = acc_test(law, M)
            sp = s_pred(law, labels, t[0], A)
            U = residual(law, labels, t)
            # identity: E<f(c(p)) - m, g(q)> = (1 - s_act) - (1 - s_pred) = s_pred - s_act, s_act = 0
            ident = max(ident, abs(float((law['omega'] * (U @ t[2].T)).sum()) - sp))
            vals.append(sp); labels = refine(labels, t[0])
        per_seq.append(np.mean(vals))
    b = 2 ** 1.25 * math.sqrt(M) * (law['D'] / K) ** 0.25
    out(f"K={K:3d}: per-sequence avg_j s_pred,j : max={max(per_seq):.4f} mean={np.mean(per_seq):.4f}  <= 2^(5/4) sqrt(M)(D/K)^(1/4)={b:.4f} [paper 4 sqrt(M)(D/K)^(1/4)={4*math.sqrt(M)*(law['D']/K)**0.25:.4f}] : {max(per_seq) <= b}; "
        f"identity <f-m,g> == s_pred - s_act : max err {ident:.1e}")
# a fixed history for the exact (3.13)/(3.14) checks: prefix of 3 acceptance tests
labels = np.zeros(law['mu'].size, dtype=np.int64)
for _ in range(3): labels = refine(labels, acc_test(law, M)[0][0])
best = (None, labels, 4)
# (3.13)/(3.14) exact checks for this fixed history
labels = best[1]; mu = law['mu']
joint = np.zeros((mu.size, mu.size))
for p in range(mu.size):
    idx = labels == labels[p]; joint[p, idx] = mu[p] * mu[idx] / mu[idx].sum()
out(f"(3.13) marginals: p-marginal==mu {np.allclose(joint.sum(1), mu)}, phat-marginal==mu {np.allclose(joint.sum(0), mu)}; "
    f"(3.14) P(p=phat)={np.trace(joint):.4f} <= |H(P)| max mu = {len(np.unique(labels))*mu.max():.4f}")
eq = np.zeros_like(joint)
for h in np.unique(labels):
    idx = labels == h; muh = mu[idx] / mu[idx].sum()
    eq[np.ix_(idx, idx)] += mu[idx].sum() * np.outer(muh, muh)
out(f"'equivalent way to draw the pair' (h~mu(H=h), then two iid from mu_h) equals (3.13) pair law: {np.allclose(eq, joint)}")

# =============================================================== Experiment B: planted two-block law, D = log 2; FAIL controls
out("\n=== B. planted two-block law (D = log 2 exactly) and FAIL controls")
nP, nQ = 30, 200
adj = np.zeros((nP, nQ)); adj[:15, :100] = 1; adj[15:, 100:] = 1
lawB = law_from_adj(adj)
out(f"D = {lawB['D']:.6f}, log 2 = {math.log(2):.6f}")
blk = (np.arange(nP) >= 15).astype(int)
half = (blk, np.array([[1.0], [-1.0]]), np.where(np.arange(nQ) >= 100, -1.0, 1.0)[:, None])   # B = B' = 1, d = 1
trivial = (np.zeros(nP, dtype=int), np.array([[1.0]]), np.zeros((nQ, 1)))
K = 10000
bB = bound(1, 1, lawB['D'], K)
ph, _, _, _, _ = frozen_sequence_stats(lawB, [half] * K)
out(f"K={K}: correct conditioning  avg_j Phi_j = {ph.mean():.6f}  (expect 1/K = {1/K})  <= 4BB'(D/K)^(1/4) = {bB:.4f}: {ph.mean() <= bB}")
ph, _, _, _, _ = frozen_sequence_stats(lawB, [half] * K, cond=False)
out(f"FAIL control 1 (prediction from mu, history ignored): avg Phi = {ph.mean():.4f} > bound {bB:.4f}: VIOLATES = {ph.mean() > bB}")
ph, _, _, _, _ = frozen_sequence_stats(lawB, [trivial] * (K - 1) + [half])
out(f"FAIL control 2 (fresh test NOT identically distributed with the prefix tests: prefix trivial, fresh = half test): Phi at the fresh test = {ph[-1]:.4f} > bound {bB:.4f}: VIOLATES = {ph[-1] > bB}")
# FAIL control 3: wrong reference law in (3.8)
tests = [random_test(law, M, d, B, Bp) for _ in range(8)]
_, _, _, ch_ok, labels = frozen_sequence_stats(law, tests, check_chain=True)
_, _, _, ch_bad, _ = frozen_sequence_stats(law, tests, check_chain=True, wrong_ref=True)
out(f"FAIL control 3 (law A, K=8): chain sum with correct b = {ch_ok:.6f} (== transcript KL {transcript_KL(law, labels):.6f} <= D={law['D']:.6f}); "
    f"with WRONG reference b=(c)_*mu_h x (c)_*mu_h : {ch_bad:.6f} -> exceeds D: {ch_bad > law['D']}")

# =============================================================== Experiment C: Cor 3.3 pieces
out("\n=== C. Cor 3.3: feature/coefficient inner product == hashed strict-cross indicator (exhaustive)")
def ip(a, b, aq, bq, L, coef=-2.0):
    f = np.concatenate([np.eye(L)[a], np.eye(L)[b], np.eye(L * L)[a * L + b]])
    g = np.concatenate([np.eye(L)[aq], np.eye(L)[bq], coef * np.eye(L * L)[aq * L + bq]])
    return float(f @ g), float(np.linalg.norm(f)), float(np.linalg.norm(g))
for coef, tag in [(-2.0, 'paper (-2)'), (-1.0, 'FAIL control 4 (coef -1)')]:
    bad = 0; norms = set()
    for L in [2, 3, 4]:
        for a, b, aq, bq in itertools.product(range(L), repeat=4):
            v, nf, ng = ip(a, b, aq, bq, L, coef); norms.add((round(nf, 6), round(ng, 6)))
            sc = float((a == aq) != (b == bq))
            if abs(v - sc) > 1e-12: bad += 1
    out(f"{tag}: mismatches over all L in {{2,3,4}} = {bad}; norms (|f|,|g|) = {sorted(norms)} (paper: sqrt3={math.sqrt(3):.6f}, sqrt6={math.sqrt(6):.6f})")

out("\n=== C'. hashing: P(true strict cross != hashed strict cross) <= 2/L for any two fixed true states (exact enumeration)")
def sc(y, z): return (y[0] == z[0]) != (y[1] == z[1])
for L in [2, 3]:
    labsA = range(3); labsB = range(3)
    worst = 0.0; worst_bad = 0.0
    states = list(itertools.product(labsA, labsB))
    hashes = list(itertools.product(range(L), repeat=3))
    # biased hash for the control: all labels mapped to 0 w.p. 1/2, else uniform
    for y in states:
        for z in states:
            cnt = 0
            for hA in hashes:
                for hB in hashes:
                    if sc(y, z) != sc((hA[y[0]], hB[y[1]]), (hA[z[0]], hB[z[1]])): cnt += 1
            worst = max(worst, cnt / len(hashes) ** 2)
            # non-uniform hash (FAIL control 5): each label hashed to value 0 with prob 1/2, else uniform on [L]
            pv = np.full(L, 0.5 / L); pv[0] += 0.5
            P = 0.0
            for hA in hashes:
                for hB in hashes:
                    w = np.prod([pv[x] for x in hA]) * np.prod([pv[x] for x in hB])
                    if sc(y, z) != sc((hA[y[0]], hB[y[1]]), (hA[z[0]], hB[z[1]])): P += w
            worst_bad = max(worst_bad, P)
    cu = 1 / L; cb = 0.25 * (1 + 1 / L) ** 2 + (L - 1) / (4 * L * L)
    fu = max(2 * cu * (1 - cu), cu); fb = max(2 * cb * (1 - cb), cb)
    out(f"L={L}: uniform independent hash worst flip prob (enumeration) = {worst:.4f}, formula max(2c(1-c),c) = {fu:.4f}, <= 2/L = {2/L:.4f}: {worst <= 2/L + 1e-12};  "
        f"non-uniform hash: enumeration {worst_bad:.4f}, formula {fb:.4f}")
for L in [8, 16]:
    cu = 1 / L; cb = 0.25 * (1 + 1 / L) ** 2 + (L - 1) / (4 * L * L)
    fu = max(2 * cu * (1 - cu), cu); fb = max(2 * cb * (1 - cb), cb)
    out(f"L={L}: uniform hash worst flip = {fu:.4f} <= 2/L={2/L:.4f}: {fu <= 2/L};  FAIL control 5 (hash value 0 w.p. 1/2+1/(2L)): worst flip = {fb:.4f} > 2/L: {fb > 2/L}")

out("\n=== C''. 'predicted point sampled using no current hash' is load-bearing (MC)")
# law: 200 points in 100 groups of 2; 300 centres, each adjacent to both points of one group.
# states: A_p = group(p), B_p = p (distinct); A_q = group of its neighbours, B_q = -1.  Every edge is a TRUE strict cross (s0 = 0).
nG = 100; nPc = 2 * nG; nQc = 300
adjc = np.zeros((nPc, nQc)); gq = np.concatenate([np.arange(nG), rng.integers(0, nG, nQc - nG)])  # every group has a centre
for q in range(nQc): adjc[2 * gq[q], q] = adjc[2 * gq[q] + 1, q] = 1
lawC = law_from_adj(adjc)
Ap = np.arange(nPc) // 2; Bpl = np.arange(nPc); Aq = gq; Bq = np.full(nQc, -1)
pp, qq = np.nonzero(lawC['adj'])
def flip_rate(cheat, Lh, reps):
    tot = 0.0
    for _ in range(reps):
        hA = rng.integers(0, Lh, nG); hB = rng.integers(0, Lh, nPc + 1)    # hB[-1] is the hash of label -1
        hp = hA[Ap] * Lh + hB[Bpl]
        diff = 0.0
        for p, q in zip(pp, qq):
            if cheat: xs = np.nonzero(hp == hp[p])[0]
            else:     xs = np.arange(nPc)
            muh = lawC['mu'][xs] / lawC['mu'][xs].sum()
            tru = ((Ap[xs] == Aq[q]) != (Bpl[xs] == Bq[q])).astype(float)
            hsh = ((hA[Ap[xs]] == hA[Aq[q]]) != (hB[Bpl[xs]] == hB[-1])).astype(float)
            diff += lawC['omega'][p, q] * float(muh @ np.abs(tru - hsh))
        tot += diff
    return tot / reps
for Lh in [4, 8]:
    r_ok = flip_rate(False, Lh, 40); r_ch = flip_rate(True, Lh, 40)
    out(f"L={Lh}: predicted-pair E|true - hashed|: hash-free prediction (mu) {r_ok:.4f} <= 2/L={2/Lh}: {r_ok <= 2/Lh};  "
        f"FAIL control 6 (prediction drawn from p's CURRENT hashed fibre): {r_ch:.4f} > 2/L: {r_ch > 2/Lh}")
```

## Citation table (this scope)
| Cited | Paper's claim | Source (version read) | Verdict |
|---|---|---|---|
| [8] Cover–Thomas, Thm 2.5.3 | (3.3) D_KL(a_XY‖b_XY) = D_KL(a_X‖b_X) + Σ_x a_X(x) D_KL(a_{Y\|x}‖b_{Y\|x}) | 1st ed. (Wiley 1991), p. 23, read from a course-hosted scan (users.itk.ppke.hu); saved in refs/covthomas/full.pdf p. 45: "Theorem 2.5.3 (Chain rule for relative entropy): D(p(x,y)‖q(x,y)) = D(p(x)‖q(x)) + D(p(y\|x)‖q(y\|x))", with (2.65) "D(p(y\|x)‖q(y\|x)) = Σ_x p(x) Σ_y p(y\|x) log p(y\|x)/q(y\|x)". The paper cites the 2nd ed. (2006); its ToC (Wiley reading sample, refs/covthomas/sample.pdf) keeps §2.5 "Chain Rules for Entropy, Relative Entropy, and Mutual Information"; 2nd-ed. body text not opened. | MATCH (statement); theorem number checked in 1st ed., consistent with 2nd-ed. ToC |
| [8] Cover–Thomas, Lemma 11.6.1 | Pinsker in nats: 2TV(a,b)² ≤ D_KL(a‖b) | 1st ed. p. 300 (refs/covthomas/full.pdf p. 322): "Lemma 12.6.1: D(P₁‖P₂) ≥ (1/(2 ln 2)) ‖P₁ − P₂‖₁²" (C&T's log is base 2). In nats: D ≥ ½‖·‖₁² = ½(2TV)² = 2TV². 1st-ed. §12.6 is the conditional-limit-theorem section (Thm 12.6.1 Pythagorean theorem on the same page); 2nd-ed. ToC lists "11.6 Conditional Limit Theorem 366" — so 11.6.1 is the 2nd-ed. number of the same lemma (chapter shift 12→11). | MATCH (content and natural-log constant); 2nd-ed. numbering inferred from ToC, body not opened |
| [16] Katz–Tardos 2004, §2 proof of Lemma 1 | "Sampling a second object from the first object's fiber also appears in [16, Section 2, proof of Lemma 1]"; §1.1: "the conditional-copy argument of Katz–Tardos retains the marginal law when resampling within a class" | Author's copy, renyi.hu/~tardos/katz.pdf (Contemp. Math. template; refs/katztardos/katz.pdf pp. 3–4): "Consider the following distribution [R, S] on pairs of rows of A: select R uniformly randomly from the n rows of A and then select S uniformly randomly among those rows of A satisfying p_{U∅}(R) = p_{U∅}(S). … Notice that S is also distributed uniformly among the n rows" | MATCH |
| [2] Ahlswede 1982, §4 Lemma 3 | "Related short conditioning arguments occur in Ahlswede's wringing method [2, Section 4, Lemma 3]" (attribution only, not used in any proof) | COULD NOT FETCH the 1982 paper (Bielefeld PUB record 1913152 sits behind an Anubis JavaScript proof-of-work wall; no other copy found). Secondary only: Ahlswede–Cai (Bielefeld homepage public/188.pdf) restate "Lemma A. (Wringing Technique [3]) Let P and Q be probability distributions over a Cartesian power Z^n … P(z^n) ≤ (1+c)Q(z^n) … then for any 0 < γ < c, 0 ≤ ε < 1 there exist t_1,…,t_k ∈ {1,2,…,n}, where 0 ≤ k ≤ c/γ such that for some z̄_{t1},…,z̄_{tk}, P(z_t \| z̄_{t1},…,z̄_{tk}) ≤ max[(1+γ)Q(z_t \| z̄_{t1},…,z̄_{tk}), ε] and P(z̄_{t1},…,z̄_{tk}) ≥ ε^k" (pp. 467–468, read from the rendered PDF), [3] = the 1982 paper. Consistent with "short conditioning arguments"; the "§4 Lemma 3" location is unverified. Non-load-bearing. | COULD NOT FETCH (secondary consistent) |

## Prove-too-much / brief cross-items touching §3
- (i) Valtr: nothing in §3 uses the Euclidean metric or even geometry; it is a statement about any finite bipartite law. Its only geometric input, D = o(log t), comes from Lemma 2.7, which uses only the pair-codegree bound (two points lie on ≤ 2 unit circles) and the unbalanced degrees — properties that also hold for Valtr-type strictly convex unit curves. So §3 cannot be where the Euclidean feature enters (as the brief expects); it must enter in §4–§8.
- (viii)(c): §3 is insensitive to the number field and its degree; nothing in §3 depends on d_N.
- (viii)(a): §3 is entirely asymptotic (rates (D/K)^{1/4}, 1/L with no quantitative rate for D/T_0, "These statements require no quantitative rate for D/T_0", p. 16) — consistent with the paper giving no effective δ.
