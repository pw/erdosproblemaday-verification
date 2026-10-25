# Referee report — seat "heights": Section 4 (PDF pp. 16–22) + brief item (iv)

Paper: OpenAI, "A power saving for planar unit distances", 23 Sep 2026, local copy /tmp/oaimath/167/paper/paper.pdf
(formulas read from the rendered PDF pages 16–22, not from the mangled pdftotext).
Primary source fetched: Milne, *Algebraic Number Theory*, **v3.08 (July 19, 2020)**, https://www.jmilne.org/math/CourseNotes/ANTc.pdf,
saved to /tmp/oaimath/167/refs/milne_ant/ANTc.pdf (md5 6fadc1eaf22c51b8855b9f1d9f4d2fe9), read via pdftotext.
Scripts (mine, not from the paper): /tmp/oaimath/167/checks/heights/ (*.py, *.gp, outputs *.out). gp = PARI/GP at /usr/bin/gp.

## VERDICT FOR THIS SCOPE: **HOLDS AS READ.**

Every displayed equation and every constant in §4 was re-derived; (4.9) and (4.15) were checked exactly; the weighted-place
normalisation of Lemma 4.1 was checked in PARI against the Mahler-measure height (an independent characterisation)
on Q(i), Q(√2), Q(ζ8) to 1e-76, and fails as it should under two wrong normalisations. I found **no FATAL and no GAP**.
The objections below are COSMETIC/exposition only (an omitted derivation I supply, mislabelled cross-references,
one citation that needs a one-line dimension count). Brief item (iv) (Prop 4.4) is answered point by point in §C.

---------------------------------------------------------------------------------------------------------------------

## A. Status of each result in scope

| Result | Status |
|---|---|
| (4.1) and the three sentences after it (p.16) | VERIFIED LINE BY LINE |
| Lemma 4.1 (weighted absolute values) + proof (p.17) | VERIFIED LINE BY LINE (+ PARI check, + all four Milne citations fetched and quoted) |
| Definition of h; Lemma 4.2 (4.3), (4.4), (4.5), (4.6) + proof (pp.17–18) | VERIFIED LINE BY LINE (+ PARI checks with failing controls) |
| §4.2: n_e(v), I_v, (4.7), level space, (4.8), S, "enlarging I_v does not change S", (4.9) (p.18) | VERIFIED LINE BY LINE ((4.9) checked exactly in PARI on a toy law) |
| Lemma 4.3 (transferring edge heights) + proof (p.19) | VERIFIED LINE BY LINE |
| Proposition 4.4 + proof (pp.19–21) | VERIFIED LINE BY LINE (sympy for (4.15)/elimination/Cramer; numerical Cramer + 8Bτ checks with failing controls) |
| §4.4: states, fractional shifts, (4.16), consistency, (4.17) (p.21) | VERIFIED LINE BY LINE |
| Lemma 4.5 (state consistency) + proof (p.22) | VERIFIED LINE BY LINE (+ Monte Carlo of the archimedean bound; control with a non-reciprocal jump) |
| Downstream use of (4.7) in Lemma 6.4 (p.33, out of scope) | SKIMMED — checked only the one sentence that consumes (4.7); it is consistent |
| Inputs used from §2–§3 (Prop 2.4 statement, Lemma 2.5, Lemma 2.7, Lemma 3.1/Cor 3.2 statements, (3.13)–(3.14)) | SKIMMED — read statements and checked that §4 applies them inside their hypotheses; their proofs are other seats' scope |

---------------------------------------------------------------------------------------------------------------------

## B. Objections (numbered)

**1. Prop 4.4, p.21 — the constant 8Bτ is asserted without derivation. COSMETIC (exposition; the statement is true).**
Quoted: *"Since the latter has coordinates bounded by B, this is a nonoverflow code, and the two complex coordinate errors are at most
√2τ. Comparing with that neighbor's exact edge equation gives |(Z_p̂ − Z_qj)(W_p̂ − W_qj) − 1| ≤ 8Bτ."*
Derivation (supplied): let p′ be the accepted neighbour of q_j, a = σ(Z_p̂−Z_qj), b = σ(W_p̂−W_qj), a′ = σ(Z_p′−Z_qj), b′ = σ(W_p′−W_qj).
Same non-overflow code ⇒ real and imaginary parts differ by < τ ⇒ |a−a′|, |b−b′| < √2τ. The edge (p′,q_j) gives a′b′ = 1 exactly
(an identity in N, preserved by σ). |a| ≤ |σZ_p̂|+|σZ_qj| ≤ 2B and |b| ≤ 2B (both W's are in the B-bounded list). Hence
|ab−1| = |(a−a′)b + a′(b−b′)| ≤ √2τ·2B + (2B+√2τ)·√2τ = 4√2Bτ + 2τ² ≤ (4√2+1)Bτ < 8Bτ, using τ < 1 ≤ B/2.
Numerically the worst sampled ratio |ab−1|/(Bτ) is 2.95 (cramer.py). Note the list "Z_p, W_p, Z_p̂, W_p̂, (Z_qj, W_qj, D_j, D_j^{−1})" contains
exactly what this needs (|σW_qj| ≤ B is used; |σZ_p|,|σW_p| ≤ B are never used — harmless).

**2. Lemma 4.2 proof, p.18 — citation of [19, Prop 8.2] for a degree identity it does not literally state. COSMETIC.**
Quoted: *"For a finite extension L/N, the decomposition into completions [19, Proposition 8.2] gives Σ_{q|p}[L_q : N_p] = [L : N]."*
Milne Prop 8.2 states L ⊗_K K̂ ≅ ∏_{i=1}^g L_i (quoted in §E). The degree identity is the K̂-dimension count of that isomorphism
(one line). True; the citation is to the right result.

**3. Cross-references throughout §4 name Lemmas/Propositions/Corollaries as "Theorem". COSMETIC.** Each points where intended:
"Theorem 2.4" (= Prop 2.4, pp.16, 20, 21), "Theorem 4.1" (= Lemma 4.1, pp.17, 18), "Theorem 2.5" (= Lemma 2.5, p.19),
"Theorem 4.3" (= Lemma 4.3, p.19), "Theorem 4.2" (= Lemma 4.2, p.19), "Theorem 2.7" (= Lemma 2.7, p.20), "Theorem 3.2"
(= Corollary 3.2, p.20), "Theorem 4.4" (= Prop 4.4, pp.21, 22), "Theorem 4.5" (= Lemma 4.5, p.22). Checked each: no
mis-targeted reference.

**4. Lemma 4.5 proof, p.22 — strictness. COSMETIC.** *"it cannot lie in the same cell once r ≥ log √2, by the diameter of a half-open square"*
— correct because two points of a half-open square of side ℓ are at distance < √2ℓ; the displayed bound uses 1{|s−n_e| ≤ log√2},
which is ≥ the needed 1{|s−n_e| < log√2}. Fine as written.

**5. A note on the brief's paraphrase (not an objection to the paper).** The brief says the ΔZΔW term "is absorbed into E_j". It is
not: the paper keeps ΔZΔW on the left of *"ΔZ/D_j + ΔW D_j + ΔZΔW = E_j"*, and the term is the same in all three equations, so it
cancels EXACTLY on subtracting j=1 from j=2,3 (sympy-verified). That is precisely why three neighbours are used: three quadratic
equations → two exactly linear equations in (ΔZ, ΔW). E_j is defined as (Z_p̂−Z_qj)(W_p̂−W_qj) − 1, bounded by Objection 1.

No GAP or FATAL objection in this scope.

---------------------------------------------------------------------------------------------------------------------

## C. Line-by-line notes (what was checked, and how)

### C.1 (4.1), p.16
‖p−q‖² = (x1−y1)²+(x2−y2)² = (z_p−z_q)(w_p−w_q) for real points, so a unit edge gives w_p − w_q = d_e^{−1}, d_e ≠ 0. For REAL points z
(resp. w) determines (x1,x2), so distinct real points have distinct z and distinct w; embeddings are injective so the differences stay
nonzero. Checked that §4 never assumes a point–center difference is nonzero off an edge (P and Q are separate copies, so a point and a
center may coincide as real points): the only nonzero claims used are z_p ≠ z_{p′} / w_p ≠ w_{p′} within P ((4.7), Prop 4.4's p̂ ≠ p),
within Q (Prop 4.4's D_j − D_l = Z_{q_l} − Z_{q_j}), and d_e ≠ 0 on edges. Reality is used here — a complex configuration on the
graph of zw = 1 could have distinct points sharing z (brief viii(d)).

### C.2 Lemma 4.1, p.17
Milne normalises: finite p: |a|_p = (1/Np)^{ord_p a}; real σ: |σa|; complex pair: |σa|² (quoted in §E); Lemma 8.6: normalised value on a
local extension L/K is |·|^{[L:K]}. With K = Q_ℓ, L = N_p, the paper's |·|_p (|ℓ|_p = ℓ^{−1}) gives Milne's value |·|_p^{n_p}, n_p = [N_p:Q_ℓ].
Since i ∈ N, every embedding is complex; |σa|² = |σa|·|σ̄a|, so taking ordinary modulus once per embedding (d_N of them) reproduces the
complex places. Product formula ⇒ Σ_p n_p log|u|_p + Σ_σ log|σu| = 0; ÷ d_N gives (4.2). Archimedean weight = d_N·(1/d_N) = 1.
Finitely many nonarch entries with |u|_v ≠ 1: Milne Thm 3.20 (free abelian group on primes) + finitely many copies per prime. **Answer to the
brief: yes, "n_p copies of weight 1/d_N" is the correct normalisation; Σ* log|u|_v = 0 and the archimedean weight is exactly one.**
h(u) = Σ* log⁺|u|_v is then the absolute logarithmic Weil height — confirmed numerically against log M(f_u)/deg f_u (PARI, §D.3).

### C.3 Lemma 4.2, pp.17–18
- Field independence: [L_q:Q_ℓ] = [L_q:N_p][N_p:Q_ℓ], Σ_{q|p}[L_q:N_p] = [L:N] ⇒ Σ_{q|p}[L_q:Q_ℓ]/[L:Q] = [N_p:Q_ℓ]/[N:Q] ✓; restriction
  of |·|_q (|ℓ| = ℓ^{−1}) to N is |·|_p ✓; each embedding of N has [L:N] extensions, weight [L:N]/[L:Q] = 1/[N:Q] ✓. Checked
  numerically (h(1+2i) in Q(i) vs Q(ζ8), h(1+√2) in Q(√2) vs Q(ζ8): differences ≤ 3e-77).
- (4.3): product formula ⇒ Σ*log⁺ = Σ*log⁻ (finite sums) ⇒ h(u^{−1}) = h(u), Σ*|log|u|_v| = 2h(u) ✓ (PARI to 1e-76).
- (4.4): log⁺(ab) ≤ log⁺a + log⁺b termwise; |u+v|_v ≤ 2max at infinity (cost log 2 × total archimedean weight 1), ultrametric elsewhere;
  zero cases by h(0) = 0 ✓. Equality case u = v = 1 (h(2) = log 2) shows the log 2 is sharp; control without log 2 fails by log 2.
- (4.5): for fixed X, P_σ(|σX|>B) ≤ (1/d_N)Σ_σ log⁺|σX| / log B ≤ h(X)/log B (Markov; nonarch terms ≥ 0) ✓; then average over X, which is
  legitimate because X is independent of σ. (4.6): same with X^{−1} and h(X^{−1}) = h(X), X ≠ 0 ✓.

### C.4 §4.2, p.18
- I_v = [0,0] at all but finitely many entries: finitely many nonzero elements (d_e, z_p−z_{p′}, w_p−w_{p′}) are units at all but finitely
  many places ✓.
- "Enlarging any I_v further does not change S": outside [min_e n_e(v), max_e n_e(v)] all bits agree, f = 0 ✓. (Also ∫m in Lemma 4.5 is
  bounded by a full-line integral, so it too is insensitive to the enlargement ✓.)
- (4.9): for fixed v, |n_e − n_{e′}| = ∫_R |1{n_e>s} − 1{n_{e′}>s}| ds and I_v contains both values; Tonelli ⇒ E_{e,e′}|n_e−n_{e′}| =
  ∫_{I_v} P(Y_e ≠ Y_{e′}) = ∫ 2π(1−π). n_e − n_{e′} = −log|d_e/d_{e′}|_v, so Σ*|n_e−n_{e′}| = 2h(d_e/d_{e′}) by (4.3). π(1−π) ≤ min(π,1−π) = f.
  So 2E h(d_e/d_{e′}) = E Σ*|n_e−n_{e′}| = 2∫π(1−π) ≤ 2S **exactly as the brief requested**; checked exactly in PARI (all three = 3.51716467083…;
  2S = 4.5039…; §D.4).
- Role of (4.7) (checked in its only consumer, Lemma 6.4, p.33): with a = −log|Z|_v, b = log|W|_v and l ≤ a, u ≥ b,
  ∫_l^u (1{s≤a} + 1{s≥b} − 1) ds ≤ a − b; Σ*(a−b) = −Σ*log|ZW|_v = 0. Without (4.7) the left side could exceed a − b. Consistent.

### C.5 Lemma 4.3, p.19 (VERIFIED LINE BY LINE)
- Nonarch labels: |U_x−U_y|_v ≤ e^s is an equivalence relation (ultrametric) ✓; point mismatch ⇔ |U_p−U_{p′}|_v > e^s exactly ✓;
  edge mismatch integral over s ≥ 0 is exactly log⁺|U_p−U_q|_v ✓.
- Arch labels: uniform shift ⇒ per-coordinate mismatch probability = min(1, |Δx|/ℓ); |Δx|+|Δy| ≤ √2a ⇒ P ≤ min(1, √2ae^{−s}) ✓
  (exact value 1 − (1−|Δx|/ℓ)⁺(1−|Δy|/ℓ)⁺; max ratio to the bound = 1.0000 in grids.py).
  ∫_0^∞ min(1,√2ae^{−s})ds = √2a if √2a ≤ 1, else 1 + log(√2a); ≤ (1+log√2)(1+log⁺a) ✓.
- Edge side summed with weights: ≤ C(1 + E h(U_p−U_q)) ✓ (direction: upper bound on edge mismatch — correct direction).
- Hypothesis applied per (level, shift) — it is exactly (2.10) of Lemma 2.5, "uniformly for every pair of label maps", with the same rule on
  P and Q and only finitely many labels attained ✓.
- Point side: distance ≥ √2e^s forces different cells for every shift ✓; log⁺a ≤ ∫_0^∞ 1{a > √2e^s}ds + log√2 (equality for a ≥ √2) ✓
  (direction: lower bound on point mismatch — correct direction). Sum with total archimedean weight 1 gives the extra log√2 ✓.
  Conclusion E h(U_p−U_{p′}) ≤ C_0 C (E h(U_p−U_q)+1) + log√2 ≤ C_1(…) with C_1 depending only on C_0 ✓.

### C.6 Proposition 4.4, pp.19–21 (VERIFIED LINE BY LINE) — brief item (iv)
1. **d_0 from (4.9):** E_{e,e′}h(d_e/d_{e′}) = ∫π(1−π) ≤ S ≤ S_0 ⇒ some e′ with E_e h(d_e/d_{e′}) ≤ S_0 ✓.
2. **Rescaling:** z/d_0 has jump D_e = d_e/d_0; d_0w has jump d_0/d_e = D_e^{−1}; product still 1 ✓; E h(D_e^{−1}) = E h(D_e) ≤ S_0 by (4.3) ✓.
3. **(4.10):** Lemma 4.3 with C_0 from (2.10) on U = z/d_0 and U = d_0w gives E_{p,p′}[h((z_p−z_{p′})/d_0) + h(d_0(w_p−w_{p′}))] ≤ 2C_1(S_0+1);
   some p′ = p_0 attains ≤ the average ✓. Centers: Z_q = Z_p − D_pq ⇒ E_κh(Z_q) = E_ω h(Z_p − D_e) ≤ E_µh(Z) + E h(D) + log 2 ✓ (κ is the
   center marginal of ω). C_h depends only on S_0 and absolute constants ✓.
4. **(4.11):** identical to (3.13) with r = 3; p, p̂ ~ µ, q_j ~ κ, (p,q_j) ~ ω; given p, p̂ and the q_j are independent, so each (p̂,q_j) has
   law ω(p,q)µ_{H(p)}(p̂) — exactly the law inside (3.12) ✓.
5. **Heights uniform in H:** E h(Z_p̂ − Z_p) ≤ 2E_µh(Z)+log 2, E h(D_j − D_l) ≤ 2E_E h(D)+log 2 by (4.4), using marginals only ✓.
6. **(4.5)/(4.6) applicability (brief iv):** for each fixed H, the tuple is drawn from (4.11) independently of σ; (4.5)/(4.6) need only that.
   The bounds use only marginals, so the choice of B (16 quantities, each E h ≤ C_h: need 16C_h/log B < 1/100) and of r (four
   difference events) is made BEFORE and uniformly over H. The later choice of H "after averaging over σ" (Cor 3.2) does not fix σ and does
   not interact with these bounds. ✓ Order of constants: S_0 → C_h → B → r → τ (4.12) → M = M(B,τ) → K → H ✓ (none depends on t or d_N).
7. **Codes:** Re/Im of σZ_p, σW_p in [−B−1,B+1] in half-open intervals of length ≤ τ, plus overflow; M = M(B,τ) independent of t and d_N ✓.
   A_σ(q) = codes attained by actual neighbours of q ⇒ s_0 = 0 ✓.
8. **Cor 3.2:** K → ∞, K = o(log t), D/K → 0 (possible since D = o(log t), Lemma 2.7) ⇒ failure ≤ 4√M(D/K)^{1/4} = o(1), |H(P)| ≤ M^{K−1} = t^{o(1)} ✓.
   The three acceptances are at the SAME fresh σ; union bound needs no independence ✓.
9. **(4.13):** P(p̂ = p) = Σ_h Σ_{H(p)=h} µ(p)²/µ(H=h) ≤ |H(P)| max µ ✓; max µ(p) = d(p)/|E| = t^{−1−2a+o(a)} ⇒ o(1) ✓.
10. **P(q_j = q_l):** given p, the q_j are iid uniform on the d(p) neighbours (ω(q|p) = 1/d(p)), so P = E[1/d(p)] ≤ 1/min d(p) = t^{−1+o(a)} ✓.
11. **Good event:** P(fail) ≤ 3·o(1) + 1/100 + 1/100 + o(1) + o(1) < 1 ⇒ positive probability that all three accept, all 16 quantities are
    ≤ B, p̂ ≠ p, q's distinct; then distinctness + not-small events give (4.14) ✓.
12. **Acceptance ⇒ genuine neighbour:** by definition of A_σ(q_j), some p′ with (p′,q_j) ∈ E has c_σ(p′) = c_σ(p̂) ✓; non-overflow because
    |σZ_p̂|,|σW_p̂| ≤ B ✓. **8Bτ:** Objection 1 (true, constant derived).
13. **Equation:** (D_j+ΔZ)(D_j^{−1}+ΔW) − 1 = ΔZ/D_j + D_jΔW + ΔZΔW ✓ (sympy). Subtraction kills ΔZΔW exactly ✓ (sympy);
    RHS |E_j − E_1| ≤ 16Bτ ✓.
14. **(4.15):** det = (D_1−D_2)(D_1−D_3)(D_2−D_3)/(D_1D_2D_3) ✓ (sympy: difference simplifies to 0; sign-flipped control does not).
    |det| ≥ r³/B³ from |σ(D_j−D_l)| ≥ r and |σD_j| ≤ B ✓. Entries ≤ 2B (needs |σD_j^{−1}| ≤ B — in the list) ✓.
15. **Cramer:** |ΔZ| ≤ |b_1a_22 − a_12b_2|/|det| ≤ (2·16Bτ·2B)/(r³/B³) = 64B⁵τ/r³ < r/2 ⇔ τ < r⁴/(128B⁵) = (4.12) ✓. (Sharper exact form:
    ΔZ = D_1D_2D_3[E_1(D_2−D_3)+E_2(D_3−D_1)+E_3(D_1−D_2)]/[(D_1−D_2)(D_1−D_3)(D_2−D_3)], sympy-verified; gives |ΔZ| ≤ 3B³max|E_j|/r².)
    Numerically: 96,000 adversarial/random systems, 0 violations, max |ΔZ|/(64B⁵τ/r³) = 0.059.
16. **Contradiction:** |σ(Z_p̂−Z_p)| < r/2 vs ≥ r ✓. Hence no bounded subsequence; S → ∞ ✓.
**Brief iv answers:** acceptance at σ does hand a genuine neighbour of q_j with p̂'s code (item 12); (4.5)/(4.6) apply (item 6); (4.15) and
8Bτ/16Bτ/64B⁵τ/r³ and (4.12) are right (items 12–15); three neighbours suffice because ΔZΔW is common and cancels exactly (Obj. 5);
the neighbours are distinct w.p. 1 − O(1/min d(p)) and q_j ≠ q_l ⇒ D_j ≠ D_l ⇒ (by (4.6) with E h(D_j−D_l) ≤ 2C_h + log 2)
|σ(D_j−D_l)| ≥ r outside the 1/100 budget (items 10–11).

### C.7 §4.4 and Lemma 4.5, pp.21–22 (VERIFIED LINE BY LINE)
- Nonarch: n_e > s ⇔ |d_e|_v < e^{−s} ⇒ A agrees; then |d_e^{−1}|_v > e^s ⇒ B1 disagrees ✓; n_e < s reverses ✓; s = n_e (both agree) is a
  single point per edge per entry ✓ ⇒ "consistent outside finitely many threshold levels" ✓.
- Arch: at entry σ, |σd_e| = e^{−n_e} and |σd_e^{−1}| = e^{n_e} (σ is a field map). With r = |s−n_e|, the jump/scale ratios are e^{−r} (the
  coordinate that SHOULD agree) and e^{r} (the one that should not) ✓. Smaller: mismatch ≤ √2e^{−r} (Lemma 4.3's grid bound) ✓; larger:
  forced mismatch for r ≥ log√2 ✓. Bound 1{|s−n_e| ≤ log√2} + √2e^{−|s−n_e|}, integral over R = log 2 + 2√2 ≈ 3.52 ✓.
- Same fractional shift at every level: for each FIXED s the scaled shift is uniform on the cell, which is all the per-level bound uses; Tonelli
  then averages ∫m over the finitely many (2 per embedding) shifts and some choice attains ≤ the mean ✓. Monte Carlo (grids.py): mean
  per-edge ∫ inconsistency 2.21 ≤ 3.52; pointwise max excess over the bound 0.005 is MC noise (the exact probability is ≤ √2e^{−r} by
  the formula in C.5).
- Match implications: c_v = 1 (equivalence classes), c_v = √2 (half-open square diameter) ✓. Measurability: floor functions of s ✓.

### C.8 Euclidean input in §4 (brief item i)
- Lemmas 4.1–4.3 are metric-free (number-field heights and label transfer).
- Prop 4.4 uses the specific identity (Z_p−Z_q)(W_p−W_q) = 1, but **is not Euclidean-essential**: for a parabola-type unit "circle"
  (jumps D, D², as on the arc used in Valtr-type constructions) the analogous argument (my sketch, not in the paper) works with two neighbours
  (2D_jΔX + ΔX² − ΔY = E_j; subtracting gives 2(D_j−D_1)ΔX = E_j − E_1). So the bounded-S case would be excluded for such metrics too; this
  is NOT a problem for the paper (Valtr-type configurations have S → ∞), it just locates the Euclidean input elsewhere.
- **Lemma 4.5 is Euclidean-essential** (needs the reciprocal jumps d, d^{−1}). Control (parabola_ctrl.py): replacing the w-jump 1/d by d²,
  the per-edge inconsistency integral is no longer O(1) but grows like ≈3|n_e| (n_e = 0,1,2,4,8 → 1.9, 2.2, 4.6, 10.9, 22.9; reciprocal
  stays ≈2). At a nonarchimedean entry one computes exactly: the edge is inconsistent on an interval of length 3|n_e(v)|, so the
  nonarchimedean part of ∫m is 3·E Σ*_{v finite}|n_e(v)| (≤ 6·E h(d_e)) — the size of the heights, not O(1). With jumps (d, d^k) and the
  paper's B1-scale e^{s}, that length is |1+k|·|n_e(v)|, zero only for k = −1; rescaling the B1-threshold rescues any k < 0 but no k > 0
  (for k > 0, {n_e > s} is an up-set in n_e while {B1 disagrees} is a down-set, so 'exactly one agrees' fails on a half-line of n_e at every
  level). This confirms the brief's reading: the "exactly one coordinate agrees" structure of §4.4 is where zw = 1 enters §4.
- Brief viii(b),(c): §4 uses near-4/3 density only through §2's outputs (Lemma 2.5 expansion, D = o(log t), max µ → 0, min d(p) → ∞).
  d_N is irrelevant in §4: weights are 1/d_N, the tests are uniform embeddings, M = M(B,τ) and all constants are independent of d_N.

---------------------------------------------------------------------------------------------------------------------

## D. Finite checks run (scripts verbatim, outputs, failing controls)

All run with `nice -n 19`, seconds each. Directory /tmp/oaimath/167/checks/heights/.

### D.1 det415.py — (4.15), the elimination of ΔZΔW, the exact Cramer formula
```python
# Check (4.15), the elimination of Delta Z * Delta W, the Cramer constant, and the 8B*tau bound.
import sympy as sp, random, cmath, math

D1, D2, D3, dZ, dW = sp.symbols('D1 D2 D3 dZ dW')
# (i) the j-th equation: (D_j + dZ)(1/D_j + dW) - 1 == dZ/D_j + D_j dW + dZ dW
for D in (D1, D2, D3):
    assert sp.simplify(sp.expand((D + dZ)*(1/D + dW) - 1) - (dZ/D + D*dW + dZ*dW)) == 0
# (ii) subtracting j=1 from j=2,3 kills dZ*dW exactly
Ej = lambda D: dZ/D + D*dW + dZ*dW
for D in (D2, D3):
    diff = sp.expand(Ej(D) - Ej(D1))
    assert sp.expand(diff - (dZ*(1/D - 1/D1) + dW*(D - D1))) == 0
    assert sp.Poly(sp.together(diff).as_numer_denom()[0], dZ, dW).coeff_monomial(dZ*dW) == 0
# (iii) the determinant (4.15)
M = sp.Matrix([[1/D2 - 1/D1, D2 - D1], [1/D3 - 1/D1, D3 - D1]])
claim = (D1 - D2)*(D1 - D3)*(D2 - D3)/(D1*D2*D3)
print("(4.15) det - claim simplifies to:", sp.simplify(M.det() - claim))
# control: a wrong sign must NOT simplify to 0
print("control (sign flipped) simplifies to:", sp.simplify(M.det() + claim))
# (iv) exact Cramer formula for dZ in terms of E's
E1, E2, E3 = sp.symbols('E1 E2 E3')
sol = sp.solve([dZ*(1/D2 - 1/D1) + dW*(D2 - D1) - (E2 - E1),
                dZ*(1/D3 - 1/D1) + dW*(D3 - D1) - (E3 - E1)], [dZ, dW], dict=True)[0]
dZsol = sp.simplify(sol[dZ])
target = (E1*(D2 - D3) + E2*(D3 - D1) + E3*(D1 - D2))*D1*D2*D3/((D1 - D2)*(D1 - D3)*(D2 - D3))
print("Cramer dZ - closed form:", sp.simplify(dZsol - target))
```
Output:
```
(4.15) det - claim simplifies to: 0
control (sign flipped) simplifies to: 2*D1/D3 - 2*D1/D2 - 2*D2/D3 + 2*D3/D2 + 2*D2/D1 - 2*D3/D1
Cramer dZ - closed form: 0
```
Control: the sign-flipped determinant does NOT simplify to 0 (printed above); the asserts on the j-th equation and on the vanishing ΔZΔW coefficient passed.

### D.2 cramer.py — Cramer bound and 8Bτ, with two failing controls
```python
# Numerical check of the Cramer step in Prop 4.4 and of |ab-1| <= 8*B*tau, with failing controls.
import random, cmath, math
random.seed(167)

def solve_dZ(D, E):
    D1, D2, D3 = D; E1, E2, E3 = E
    a11, a12, b1 = 1/D2 - 1/D1, D2 - D1, E2 - E1
    a21, a22, b2 = 1/D3 - 1/D1, D3 - D1, E3 - E1
    det = a11*a22 - a12*a21
    dZ = (b1*a22 - a12*b2)/det
    dW = (a11*b2 - b1*a21)/det
    return dZ, dW, det

def rand_D(B, r):
    while True:
        D = [cmath.rect(math.exp(random.uniform(-math.log(B), math.log(B))), random.uniform(0, 2*math.pi)) for _ in range(3)]
        if all(abs(D[i]-D[j]) >= r for i in range(3) for j in range(i+1, 3)):
            return D

def worst_E(D, eps):
    # |dZ| is linear in E: dZ = (E1(D2-D3)+E2(D3-D1)+E3(D1-D2))/det ; align phases to maximise
    D1, D2, D3 = D
    co = [D2 - D3, D3 - D1, D1 - D2]
    return [eps*cmath.exp(-1j*cmath.phase(c)) for c in co]

worst_ratio = 0.0; n = 0; viol = 0
for B in (2.0, 3.0, 5.0):
    for r in (0.9, 0.5, 0.2, 0.05):
        tau = 0.999*min(1.0, r**4/(128*B**5))
        eps = 8*B*tau
        for _ in range(4000):
            D = rand_D(B, r)
            for E in (worst_E(D, eps), [eps*cmath.exp(1j*random.uniform(0, 6.3))*random.random() for _ in range(3)]):
                dZ, dW, det = solve_dZ(D, E)
                n += 1
                assert abs(det) >= r**3/B**3 - 1e-12
                bound = 64*B**5*tau/r**3
                worst_ratio = max(worst_ratio, abs(dZ)/bound)
                if not (abs(dZ) <= bound + 1e-12 and abs(dZ) < r/2):
                    viol += 1
print(f"Cramer: {n} systems, violations={viol}, max |dZ|/(64B^5tau/r^3) = {worst_ratio:.4f}")

# full three-equation check: random (dZ,dW,D), E_j computed exactly; ratio |dZ| r^3 / (B^4 max|E|) must be <= 8
worst = 0.0
for _ in range(200000):
    B = random.choice([2.0, 3.0, 5.0])
    D = [cmath.rect(math.exp(random.uniform(-math.log(B), math.log(B))), random.uniform(0, 2*math.pi)) for _ in range(3)]
    r = min(abs(D[i]-D[j]) for i in range(3) for j in range(i+1, 3))
    dZ = cmath.rect(10**random.uniform(-6, 0), random.uniform(0, 6.3)); dW = cmath.rect(10**random.uniform(-6, 0), random.uniform(0, 6.3))
    E = [dZ/d + d*dW + dZ*dW for d in D]
    worst = max(worst, abs(dZ)*r**3/(B**4*max(abs(e) for e in E)))
print(f"three-equation: max |dZ| r^3/(B^4 max|E_j|) = {worst:.4f}  (paper's implication needs <= 8)")

# 8 B tau: |a|,|b| <= 2B, a'b'=1, |a-a'|,|b-b'| <= sqrt2*tau  =>  |ab-1| <= 8 B tau   (B>=2, tau<1)
worst8 = 0.0
for _ in range(300000):
    B = random.uniform(2, 6); tau = random.uniform(0, 1)
    a = cmath.rect(random.uniform(0, 2*B), random.uniform(0, 6.3))
    d1 = cmath.rect(math.sqrt(2)*tau*random.random()**0.1, random.uniform(0, 6.3))
    ap = a + d1
    if ap == 0: continue
    bp = 1/ap
    d2 = cmath.rect(math.sqrt(2)*tau*random.random()**0.1, random.uniform(0, 6.3))
    b = bp + d2
    if abs(b) > 2*B: continue
    worst8 = max(worst8, abs(a*b - 1)/(B*tau))
print(f"8B*tau: max |ab-1|/(B tau) = {worst8:.4f} (needs <= 8; analytic sup 4*sqrt2 + 2tau/B <= 6.66)")

# ---- CONTROLS (must FAIL) ----
# (a) violate (4.12): tau = 50 * r^4/(128 B^5); worst-case E gives |dZ| > r/2
B, r = 2.0, 0.5
tau_bad = 50*r**4/(128*B**5); eps = 8*B*tau_bad
best = 0.0
for _ in range(20000):
    D = rand_D(B, r)
    dZ, dW, det = solve_dZ(D, worst_E(D, eps))
    best = max(best, abs(dZ))
print(f"CONTROL (4.12) violated (tau=50x limit): max |dZ| = {best:.4f}  vs r/2 = {r/2}  -> exceeds: {best > r/2}")
# (b) violate (4.14): D's almost collide; exact solution with |dZ| = r and tiny E_j
B, r = 2.0, 0.5
Dc = [1.0, 1.0 + 1e-4, 1.0 + 2e-4j]
dZ = r
# choose dW minimising max|E_j| (approximately) : make E_1 = 0
dW = -(dZ/Dc[0])/(Dc[0] + dZ)
E = [dZ/d + d*dW + dZ*dW for d in Dc]
print(f"CONTROL (4.14) violated (|D_j-D_l|~1e-4): |dZ| = {dZ}, max|E_j| = {max(abs(e) for e in E):.3e}"
      f" -> an |E|<=8B*tau configuration with |dZ|>=r exists for tau = {max(abs(e) for e in E)/(8*B):.2e}"
      f" < r^4/(128B^5) = {r**4/(128*B**5):.2e}: {max(abs(e) for e in E)/(8*B) < r**4/(128*B**5)}")
```
Output:
```
Cramer: 96000 systems, violations=0, max |dZ|/(64B^5tau/r^3) = 0.0589
three-equation: max |dZ| r^3/(B^4 max|E_j|) = 2.3603  (paper's implication needs <= 8)
8B*tau: max |ab-1|/(B tau) = 2.9534 (needs <= 8; analytic sup 4*sqrt2 + 2tau/B <= 6.66)
CONTROL (4.12) violated (tau=50x limit): max |dZ| = 0.3634  vs r/2 = 0.25  -> exceeds: True
CONTROL (4.14) violated (|D_j-D_l|~1e-4): |dZ| = 0.5, max|E_j| = 1.667e-04 -> an |E|<=8B*tau configuration with |dZ|>=r exists for tau = 1.04e-05 < r^4/(128B^5) = 1.53e-05: True
```
Controls FAIL as they must: (a) with τ = 50× the (4.12) limit, worst-case E_j give |ΔZ| = 0.363 > r/2 = 0.25; (b) with (4.14) violated (|D_j−D_l| ~ 1e-4) there is an EXACT solution of all three equations with |ΔZ| = r and max|E_j| = 1.7e-4, i.e. admissible for a τ below the (4.12) limit — so the separation (4.14) is what drives the contradiction.

### D.3 heights.gp — Lemma 4.1 normalisation, Lemma 4.2 (4.3)–(4.6), field independence (PARI/GP)
```
\\ Lemma 4.1 / 4.2 checks: weighted places (n_p copies of weight 1/d) and the absolute height.
default(realprecision, 60);
nrm(nf, u) = lift(Mod(numerator(u), nf.pol) / Mod(denominator(u), nf.pol));
\\ weighted sum of log|u|_v ; mode 0 = paper's normalisation,
\\ mode 1 = CONTROL (genuine |.|_p once per prime, weight 1/d), mode 2 = CONTROL (squared modulus at every embedding)
wsum(nf, u, mode) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, if(mode == 2, 2, 1) * log(abs(c[k]))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += if(mode == 1, 1, pr.e*pr.f) * (-ord/pr.e) * log(pr.p) / d);
  s
}
hplaces(nf, u) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); if(u == 0, return(0));
  c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, max(0, log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += pr.e*pr.f * max(0, (-ord/pr.e) * log(pr.p)) / d);
  s
}
habs(nf, u) =
{
  my(d = poldegree(nf.pol), c, s, fa, pr, ord);
  u = nrm(nf, u); c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, abs(log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; ord = fa[k,2]; s += pr.e*pr.f * abs((-ord/pr.e) * log(pr.p)) / d);
  s
}
\\ independent height: log Mahler measure of primitive integer minimal polynomial / degree
hmahler(nf, u) =
{
  my(f, g, r);
  u = nrm(nf, u); f = minpoly(Mod(u, nf.pol));
  g = f * denominator(content(f)); g = g / content(g); r = polroots(g);
  (log(abs(pollead(g))) + sum(k = 1, #r, max(0, log(abs(r[k]))))) / poldegree(g)
}
report(name, nf, L) =
{
  print("== ", name, "   pol = ", nf.pol, "   d_N = ", poldegree(nf.pol));
  for(k = 1, #L,
    my(u = L[k], ui = 1/L[k]);
    printf("u=%-18s sum*log|u|_v=% .1e | CTRL once/prime=% .4f CTRL sq.mod=% .4f | h_places=%.10f h_Mahler=%.10f diff=% .0e | h(1/u)-h(u)=% .0e | sum*|log|u|_v|-2h=% .0e\n",
      Str(u), wsum(nf,u,0), wsum(nf,u,1), wsum(nf,u,2), hplaces(nf,u), hmahler(nf,u),
      hplaces(nf,u)-hmahler(nf,u), hplaces(nf,ui)-hplaces(nf,u), habs(nf,u)-2*hplaces(nf,u)));
}
QI = nfinit(x^2 + 1);
report("Q(i)", QI, [1 + 2*x, 3, (1 + x)/3, 5/(2 + x), 7, (3 + 4*x)/5, 2, 1 + x, 12/(5 + 12*x), 13*x/(4 - x)]);
QS = nfinit(x^2 - 2);
report("Q(sqrt2)", QS, [1 + x, 3 + 2*x, (1 + x)/7, x/3, 5, (x - 1)/(x + 3)]);
Q8 = nfinit(x^4 + 1);
\\ in Q(zeta8): i = x^2, sqrt2 = x - x^3
report("Q(zeta8)", Q8, [1 + 2*x^2, 3, 7, (3 + 4*x^2)/5, 1 + x - x^3, 3 + 2*(x - x^3), (1 + x - x^3)/7]);
print("field independence: h(1+2i): Q(i) - Q(zeta8) = ", hplaces(QI, 1 + 2*x) - hplaces(Q8, 1 + 2*x^2), ";   h(1+sqrt2): Q(sqrt2) - Q(zeta8) = ", hplaces(QS, 1 + x) - hplaces(Q8, 1 + x - x^3));
rnd(nf) =
{
  my(d = poldegree(nf.pol), w = 0);
  while(w == 0, w = sum(k = 0, d - 1, (random(21) - 10) * x^k) / (1 + random(9)));
  w
}
{
  my(ok = 1, wa = -1e9, wm = -1e9);
  setrand(167);
  for(it = 1, 300,
    my(nf = if(it % 2, QI, Q8), a = rnd(nf), b = rnd(nf), ha, hb, m, s);
    ha = hplaces(nf, a); hb = hplaces(nf, b);
    m = hplaces(nf, a*b) - ha - hb;
    s = hplaces(nf, a + b) - ha - hb - log(2);
    wm = max(wm, m); wa = max(wa, s);
    if(m > 1e-40 || s > 1e-40, ok = 0));
  print("(4.4) 300 random pairs: max[h(uv)-h(u)-h(v)] = ", wm, "   max[h(u+v)-h(u)-h(v)-log2] = ", wa, "   all ok: ", ok);
}
print("(4.4) equality case u=v=1: h(2)-2h(1)-log2 = ", hplaces(QI, 2) - 2*hplaces(QI, 1) - log(2), ";  CONTROL without log2: h(2)-2h(1) = ", hplaces(QI, 2) - 2*hplaces(QI, 1), "  (>0: the log 2 is needed)");
{
  my(XL = [1 + 2*x^2, (3 + 4*x^2)/5, 1 + x - x^3, (1 + x - x^3)/7, 3 + 2*(x - x^3), 5/(2 + x^2), 12*x], Eh, B, r, pB, pr, c);
  Eh = sum(k = 1, #XL, hplaces(Q8, XL[k])) / #XL;
  for(j = 1, 3,
    B = [3/2, 2, 4][j]; r = [1/2, 3/10, 1/10][j]; pB = 0; pr = 0;
    for(k = 1, #XL, c = conjvec(Mod(nrm(Q8, XL[k]), Q8.pol)); for(m = 1, #c, pB += (abs(c[m]) > B); pr += (abs(c[m]) < r)));
    pB /= (#XL * 4); pr /= (#XL * 4);
    printf("(4.5) B=%.1f: P(|sX|>B)=%.4f <= Eh/logB=%.4f : %d     (4.6) r=%.2f: P(X!=0,|sX|<r)=%.4f <= Eh/log(1/r)=%.4f : %d\n",
      B, pB, Eh/log(B), pB <= Eh/log(B), r, pr, Eh/log(1/r), pr <= Eh/log(1/r)));
}
{
  my(X = 1/7, c = conjvec(Mod(1/7, QI.pol)));
  printf("CONTROL (4.6) with archimedean-only height: X=1/7, P_sigma(|sX|<1/2)=1 but arch log+ part = %.3f (bound 0 fails); true bound h(1/7)/log 2 = %.3f\n",
    sum(k = 1, 2, max(0, log(abs(c[k])))) / 2, hplaces(QI, X) / log(2));
}
```
Output:
```
== Q(i)   pol = x^2 + 1   d_N = 2
u=2*x + 1            sum*log|u|_v= 8.6 e-78 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.8047 | h_places=0.8047189562 h_Mahler=0.8047189562 diff= 0.e-77 | h(1/u)-h(u)=-9. e-78 | sum*|log|u|_v|-2h=-2. e-77
u=3                  sum*log|u|_v= 0.e-76 | CTRL once/prime= 0.5493 CTRL sq.mod= 1.0986 | h_places=1.0986122887 h_Mahler=1.0986122887 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=1/3*x + 1/3        sum*log|u|_v= 0.e-76 | CTRL once/prime=-0.3760 CTRL sq.mod=-0.7520 | h_places=1.0986122887 h_Mahler=1.0986122887 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=5/(x + 2)          sum*log|u|_v= 8.6 e-78 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.8047 | h_places=0.8047189562 h_Mahler=0.8047189562 diff= 0.e-77 | h(1/u)-h(u)=-9. e-78 | sum*|log|u|_v|-2h=-2. e-77
u=7                  sum*log|u|_v= 0.e-76 | CTRL once/prime= 0.9730 CTRL sq.mod= 1.9459 | h_places=1.9459101491 h_Mahler=1.9459101491 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=4/5*x + 3/5        sum*log|u|_v= 0.e-77 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.0000 | h_places=0.8047189562 h_Mahler=0.8047189562 diff= 0.e-77 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h= 0.e-76
u=2                  sum*log|u|_v= 0.e-77 | CTRL once/prime= 0.3466 CTRL sq.mod= 0.6931 | h_places=0.6931471806 h_Mahler=0.6931471806 diff= 0.e-77 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h= 0.e-76
u=x + 1              sum*log|u|_v=-4.3 e-78 | CTRL once/prime= 0.1733 CTRL sq.mod= 0.3466 | h_places=0.3465735903 h_Mahler=0.3465735903 diff= 0.e-77 | h(1/u)-h(u)= 4. e-78 | sum*|log|u|_v|-2h= 0.e-77
u=12/(12*x + 5)      sum*log|u|_v= 0.e-76 | CTRL once/prime= 1.2425 CTRL sq.mod=-0.0800 | h_places=2.5649493575 h_Mahler=2.5649493575 diff= 0.e-76 | h(1/u)-h(u)=-3. e-77 | sum*|log|u|_v|-2h= 0.e-76
u=13*x/(-x + 4)      sum*log|u|_v= 0.e-76 | CTRL once/prime= 0.0000 CTRL sq.mod= 1.1483 | h_places=2.5649493575 h_Mahler=2.5649493575 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h=-7. e-77
== Q(sqrt2)   pol = x^2 - 2   d_N = 2
u=x + 1              sum*log|u|_v=-8.6 e-78 | CTRL once/prime=-0.0000 CTRL sq.mod=-0.0000 | h_places=0.4406867935 h_Mahler=0.4406867935 diff=-4. e-78 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h= 9. e-78
u=2*x + 3            sum*log|u|_v= 2.6 e-77 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.0000 | h_places=0.8813735870 h_Mahler=0.8813735870 diff=-9. e-78 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h=-3. e-77
u=1/7*x + 1/7        sum*log|u|_v=-2.6 e-77 | CTRL once/prime=-0.0000 CTRL sq.mod=-1.9459 | h_places=1.9459101491 h_Mahler=1.9459101491 diff= 0.e-76 | h(1/u)-h(u)=-2. e-77 | sum*|log|u|_v|-2h= 0.e-76
u=1/3*x              sum*log|u|_v= 0.e-76 | CTRL once/prime=-0.3760 CTRL sq.mod=-0.7520 | h_places=1.0986122887 h_Mahler=1.0986122887 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=5                  sum*log|u|_v= 0.e-76 | CTRL once/prime= 0.8047 CTRL sq.mod= 1.6094 | h_places=1.6094379124 h_Mahler=1.6094379124 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=(x - 1)/(x + 3)    sum*log|u|_v=-2.6 e-77 | CTRL once/prime=-0.0000 CTRL sq.mod=-0.9730 | h_places=1.1831016383 h_Mahler=1.1831016383 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
== Q(zeta8)   pol = x^4 + 1   d_N = 4
u=2*x^2 + 1          sum*log|u|_v=-1.7 e-77 | CTRL once/prime= 0.4024 CTRL sq.mod= 0.8047 | h_places=0.8047189562 h_Mahler=0.8047189562 diff=-3. e-77 | h(1/u)-h(u)= 2. e-77 | sum*|log|u|_v|-2h= 2. e-77
u=3                  sum*log|u|_v= 0.e-77 | CTRL once/prime= 0.5493 CTRL sq.mod= 1.0986 | h_places=1.0986122887 h_Mahler=1.0986122887 diff= 0.e-76 | h(1/u)-h(u)= 0.e-76 | sum*|log|u|_v|-2h= 0.e-76
u=7                  sum*log|u|_v=-8.6 e-78 | CTRL once/prime= 0.9730 CTRL sq.mod= 1.9459 | h_places=1.9459101491 h_Mahler=1.9459101491 diff=-2. e-77 | h(1/u)-h(u)= 2. e-77 | sum*|log|u|_v|-2h= 0.e-76
u=4/5*x^2 + 3/5      sum*log|u|_v= 0.e-77 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.0000 | h_places=0.8047189562 h_Mahler=0.8047189562 diff= 0.e-77 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h= 0.e-76
u=-x^3 + x + 1       sum*log|u|_v=-3.0 e-77 | CTRL once/prime=-0.0000 CTRL sq.mod=-0.0000 | h_places=0.4406867935 h_Mahler=0.4406867935 diff=-4. e-78 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h= 3. e-77
u=-2*x^3 + 2*x + 3   sum*log|u|_v= 1.2 e-76 | CTRL once/prime= 0.0000 CTRL sq.mod= 0.0000 | h_places=0.8813735870 h_Mahler=0.8813735870 diff=-9. e-78 | h(1/u)-h(u)= 0.e-77 | sum*|log|u|_v|-2h=-1. e-76
u=-1/7*x^3 + 1/7*x + 1/7 sum*log|u|_v=-2.6 e-77 | CTRL once/prime=-0.9730 CTRL sq.mod=-1.9459 | h_places=1.9459101491 h_Mahler=1.9459101491 diff= 0.e-76 | h(1/u)-h(u)=-5. e-77 | sum*|log|u|_v|-2h= 0.e-76
field independence: h(1+2i): Q(i) - Q(zeta8) = 2.5908505665283333876 E-77;   h(1+sqrt2): Q(sqrt2) - Q(zeta8) = 0.E-77
(4.4) 300 random pairs: max[h(uv)-h(u)-h(v)] = 1.3817869688151111401 E-76   max[h(u+v)-h(u)-h(v)-log2] = -0.103819682389122250807720522133693833748366296340406950031837   all ok: 1
(4.4) equality case u=v=1: h(2)-2h(1)-log2 = 0.E-77;  CONTROL without log2: h(2)-2h(1) = 0.693147180559945309417232121458176568075500134360255254120680  (>0: the log 2 is needed)
(4.5) B=1.5: P(|sX|>B)=0.5714 <= Eh/logB=2.8775 : 1     (4.6) r=0.50: P(X!=0,|sX|<r)=0.2857 <= Eh/log(1/r)=1.6832 : 1
(4.5) B=2.0: P(|sX|>B)=0.5714 <= Eh/logB=1.6832 : 1     (4.6) r=0.30: P(X!=0,|sX|<r)=0.1429 <= Eh/log(1/r)=0.9691 : 1
(4.5) B=4.0: P(|sX|>B)=0.2143 <= Eh/logB=0.8416 : 1     (4.6) r=0.10: P(X!=0,|sX|<r)=0.0714 <= Eh/log(1/r)=0.5067 : 1
CONTROL (4.6) with archimedean-only height: X=1/7, P_sigma(|sX|<1/2)=1 but arch log+ part = 0.000 (bound 0 fails); true bound h(1/7)/log 2 = 2.807
```
Reading: with the paper's normalisation Σ* log|u|_v is 0 to 1e-76 for every element and h_places = h_Mahler to 1e-76 (independent characterisation of the absolute Weil height). Controls FAIL: "once per prime" (dropping the n_p copies) gives nonzero sums exactly when an inert/ramified prime (n_p = 2) divides u (u = 3, 7, 2, 1+i, (1+i)/3, …; it is 0 when only split primes occur, as it must be); "squared modulus at each embedding" (archimedean weight 2) gives nonzero sums whenever the archimedean part is nonzero. (4.4): equality at u = v = 1, and dropping the log 2 fails by log 2. (4.6): the bound genuinely needs the nonarchimedean part of h (X = 1/7).

### D.4 eq49.gp — (4.9) exactly on a toy edge-jump law in Q(i)
```
\\ (4.9): 2 E h(d_e/d_e') = E sum* |n_e - n_e'| = 2 int pi(1-pi)  (<= 2S), on a toy edge-jump law in Q(i).
default(realprecision, 50);
nf = nfinit(x^2 + 1); d = 2;
nrm(u) = lift(Mod(numerator(u), nf.pol) / Mod(denominator(u), nf.pol));
hpl(u) =
{
  my(c, s, fa, pr);
  u = nrm(u); if(u == 0, return(0));
  c = conjvec(Mod(u, nf.pol)); fa = idealfactor(nf, u);
  s = sum(k = 1, #c, max(0, log(abs(c[k])))) / d;
  for(k = 1, #fa~, pr = fa[k,1]; s += pr.e*pr.f * max(0, -fa[k,2]/pr.e * log(pr.p)) / d);
  s
}
J = [1 + 2*x, (3 + 4*x)/5, 2, 1/(1 + x), 7*x/(2 - x), 3, (1 - x)/5, 11 + 0*x];
J = vector(#J, k, nrm(J[k])); m = #J;
\\ places: 2 embeddings (weight 1/2 each) + primes dividing some d_e (weight e*f/2)
P = []; { for(k = 1, m, my(fa = idealfactor(nf, J[k])); for(j = 1, #fa~, my(pr = fa[j,1], new = 1);
      for(i = 1, #P, if(P[i].p == pr.p && idealval(nf, pr.gen[2], P[i]) > 0 && P[i].e == pr.e && P[i].f == pr.f && idealhnf(nf, P[i]) == idealhnf(nf, pr), new = 0));
      if(new, P = concat(P, [pr])))); }
\\ n_e(v) table
nv(k, v) = if(v <= 2, -log(abs(conjvec(Mod(J[k], nf.pol))[v])), my(pr = P[v - 2]); idealval(nf, J[k], pr) * log(pr.p) / pr.e);
wt(v) = if(v <= 2, 1/d, my(pr = P[v - 2]); pr.e*pr.f/d);
\\ exact integral of pi(1-pi) over s, pi(s) = #{n_e > s}/m, piecewise constant between sorted values
ipi(vals) = { my(sv = vecsort(vals), tot = 0, cnt); for(j = 1, #sv - 1, cnt = #select(t -> t > sv[j], sv); tot += (cnt/m)*(1 - cnt/m)*(sv[j+1] - sv[j])); tot };
ifm(vals) = { my(sv = vecsort(vals), tot = 0, cnt); for(j = 1, #sv - 1, cnt = #select(t -> t > sv[j], sv); tot += min(cnt/m, 1 - cnt/m)*(sv[j+1] - sv[j])); tot };
{
  my(nV = 2 + #P, lhs, mid, rhs, S);
  lhs = 2 * sum(a = 1, m, sum(b = 1, m, hpl(J[a]/J[b]))) / m^2;
  mid = sum(a = 1, m, sum(b = 1, m, sum(v = 1, nV, wt(v) * abs(nv(a, v) - nv(b, v))))) / m^2;
  rhs = 2 * sum(v = 1, nV, wt(v) * ipi(vector(m, k, nv(k, v))));
  S = sum(v = 1, nV, wt(v) * ifm(vector(m, k, nv(k, v))));
  print("primes used: ", vector(#P, i, [P[i].p, P[i].e, P[i].f]));
  print("2E h(d/d')            = ", lhs);
  print("E sum*|n_e - n_e'|     = ", mid);
  print("2 int pi(1-pi)        = ", rhs);
  print("2S                    = ", 2*S, "   (4.9) chain holds: ", abs(lhs-mid) < 1e-30 && abs(mid-rhs) < 1e-30 && rhs <= 2*S + 1e-30);
  print("CONTROL: 2 int min(pi,1-pi) = 2S differs from 2E h: ", 2*S - lhs, "  (the equality is with pi(1-pi), only an inequality with f)");
}
```
Output:
```
primes used: [[5, 1, 1], [5, 1, 1], [2, 2, 1], [7, 1, 2], [3, 1, 2], [11, 1, 2]]
2E h(d/d')            = 3.5171646708333047253590910431967963111732234660773
E sum*|n_e - n_e'|     = 3.5171646708333047253590910431967963111732234660773
2 int pi(1-pi)        = 3.5171646708333047253590910431967963111732234660773
2S                    = 4.5039335628349834722363381427561491485976174585296   (4.9) chain holds: 1
CONTROL: 2 int min(pi,1-pi) = 2S differs from 2E h: 0.98676889200167874687724709955935283742439399245233  (the equality is with pi(1-pi), only an inequality with f)
```

### D.5 grids.py — Lemma 4.3 grid bound, Lemma 4.5 archimedean bound
```python
# Lemma 4.3 grid mismatch bound and Lemma 4.5 archimedean inconsistency bound (same fractional shift at every level).
import random, math, cmath
random.seed(45)
SQ2 = math.sqrt(2)
def cell(z, side, phi):
    return (math.floor(z.real/side - phi[0]), math.floor(z.imag/side - phi[1]))

# Lemma 4.3: P(different cells) <= min(1, sqrt2 * a / side); exact value 1-(1-|dx|/l)+(1-|dy|/l)+
worst = 0.0
for _ in range(2000):
    a = 10**random.uniform(-2, 1); th = random.uniform(0, 2*math.pi); side = 1.0
    d = cmath.rect(a, th)
    exact = 1 - max(0, 1 - abs(d.real)/side)*max(0, 1 - abs(d.imag)/side)
    worst = max(worst, exact/min(1, SQ2*a/side))
print(f"L4.3: max exact P(diff cell)/min(1,sqrt2 a e^-s) = {worst:.4f} (<=1 required)")
# integral over s>=0 of min(1, sqrt2 a e^-s) vs C(1+log+ a) with C = 1+log sqrt2
for a in (0.01, 0.5, 1/SQ2, 1.0, 10.0, 1e6):
    I = SQ2*a if SQ2*a <= 1 else 1 + math.log(SQ2*a)
    print(f"  a={a:g}: int = {I:.4f} <= (1+log sqrt2)(1+log+ a) = {(1+math.log(SQ2))*(1+max(0,math.log(a))):.4f}")
# point-pair side: log+ a <= int_0^inf 1{a > sqrt2 e^s} ds + log sqrt2  (equality for a >= sqrt2)
for a in (0.3, 1.0, SQ2, 5.0, 1e5):
    lhs = max(0, math.log(a)); rhs = max(0, math.log(a/SQ2)) + math.log(SQ2)
    print(f"  point pair a={a:g}: log+a={lhs:.4f} <= {rhs:.4f}: {lhs <= rhs + 1e-12}")

# Lemma 4.5 at infinity. Edge: z-jump delta, w-jump 1/delta ; n_e = -log|delta|.
def inconsistent(zq, wq, delta, s, phiA, phiB):
    zp, wp = zq + delta, wq + 1/delta
    Aagree = cell(zp, math.exp(-s), phiA) == cell(zq, math.exp(-s), phiA)
    Bagree = cell(wp, math.exp(s), phiB) == cell(wq, math.exp(s), phiB)
    n = -math.log(abs(delta))
    if n > s:  return not (Aagree and not Bagree)
    else:      return not (Bagree and not Aagree)
viol = 0; tot = 0; Iacc = 0.0; ntr = 300
grid = [x/20 for x in range(-200, 201)]  # s in [-10,10], ds = 0.05
for tr in range(ntr):
    n = random.uniform(-3, 3); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
    zq = complex(random.uniform(-50, 50), random.uniform(-50, 50)); wq = complex(random.uniform(-50, 50), random.uniform(-50, 50))
    phiA = (random.random(), random.random()); phiB = (random.random(), random.random())   # ONE shift per grid, all levels
    for s in grid:
        tot += 1
        Iacc += inconsistent(zq, wq, delta, s, phiA, phiB) * 0.05
I_avg = Iacc/ntr
# pointwise bound check: average over shifts at fixed (delta, s)
worst = 0.0
for _ in range(60):
    n = random.uniform(-2, 2); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi)); s = n + random.uniform(-3, 3)
    m = sum(inconsistent(0j, 0j, delta, s, (random.random(), random.random()), (random.random(), random.random())) for _ in range(3000))/3000
    b = (1 if abs(s-n) <= math.log(SQ2) else 0) + SQ2*math.exp(-abs(s-n))
    worst = max(worst, m - b)
print(f"L4.5: mean over edges/shifts of int_R inconsistency = {I_avg:.3f} <= log2 + 2sqrt2 = {math.log(2)+2*SQ2:.3f}; "
      f"max(MC P(incons) - pointwise bound) = {worst:.4f} (<= ~0 up to MC noise)")
# CONTROL: replace the w-jump 1/delta by delta^2 (parabola-type 'unit circle' Y = X^2): consistency integral is NOT bounded
def inconsistent_par(zq, wq, delta, s, phiA, phiB):
    zp, wp = zq + delta, wq + delta**2
    Aagree = cell(zp, math.exp(-s), phiA) == cell(zq, math.exp(-s), phiA)
    Bagree = cell(wp, math.exp(s), phiB) == cell(wq, math.exp(s), phiB)
    n = -math.log(abs(delta))
    return (not (Aagree and not Bagree)) if n > s else (not (Bagree and not Aagree))
Iacc = 0.0; big = [x/20 for x in range(-400, 401)]
for tr in range(100):
    n = random.uniform(-3, 3); delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
    phiA = (random.random(), random.random()); phiB = (random.random(), random.random())
    Iacc += sum(inconsistent_par(0j, 0j, delta, s, phiA, phiB) for s in big)*0.05
print(f"CONTROL (jumps d, d^2 instead of d, 1/d): mean int over s in [-20,20] of inconsistency = {Iacc/100:.2f} (per-edge value grows linearly in |n_e|, see parabola_ctrl.py; random n_e in [-3,3] here)")
```
Output:
```
L4.3: max exact P(diff cell)/min(1,sqrt2 a e^-s) = 1.0000 (<=1 required)
  a=0.01: int = 0.0141 <= (1+log sqrt2)(1+log+ a) = 1.3466
  a=0.5: int = 0.7071 <= (1+log sqrt2)(1+log+ a) = 1.3466
  a=0.707107: int = 1.0000 <= (1+log sqrt2)(1+log+ a) = 1.3466
  a=1: int = 1.3466 <= (1+log sqrt2)(1+log+ a) = 1.3466
  a=10: int = 3.6492 <= (1+log sqrt2)(1+log+ a) = 4.4472
  a=1e+06: int = 15.1621 <= (1+log sqrt2)(1+log+ a) = 19.9502
  point pair a=0.3: log+a=0.0000 <= 0.3466: True
  point pair a=1: log+a=0.0000 <= 0.3466: True
  point pair a=1.41421: log+a=0.3466 <= 0.3466: True
  point pair a=5: log+a=1.6094 <= 1.6094: True
  point pair a=100000: log+a=11.5129 <= 11.5129: True
L4.5: mean over edges/shifts of int_R inconsistency = 2.214 <= log2 + 2sqrt2 = 3.522; max(MC P(incons) - pointwise bound) = 0.0051 (<= ~0 up to MC noise)
CONTROL (jumps d, d^2 instead of d, 1/d): mean int over s in [-20,20] of inconsistency = 5.20 (per-edge value grows linearly in |n_e|, see parabola_ctrl.py; random n_e in [-3,3] here)
```

### D.6 parabola_ctrl.py — control: Lemma 4.5 needs reciprocal jumps
```python
# CONTROL for Lemma 4.5: replace the reciprocal w-jump 1/d (Euclidean, zw=1) by d^2 (parabola Y=X^2, Valtr-type arc).
# With 1/d the per-edge inconsistency integral is O(1) uniformly in n_e; with d^2 it grows linearly in |n_e|.
import random, math, cmath
random.seed(7)
def cell(z, side, phi): return (math.floor(z.real/side - phi[0]), math.floor(z.imag/side - phi[1]))
def incons(delta, wjump, s, phiA, phiB):
    Aagree = cell(delta, math.exp(-s), phiA) == cell(0j, math.exp(-s), phiA)
    Bagree = cell(wjump, math.exp(s), phiB) == cell(0j, math.exp(s), phiB)
    n = -math.log(abs(delta))
    return (not (Aagree and not Bagree)) if n > s else (not (Bagree and not Aagree))
S = [x/20 for x in range(-1000, 1001)]
for n in (0.0, 1.0, 2.0, 4.0, 8.0, -4.0, -8.0):
    Ir, Ip = 0.0, 0.0
    for _ in range(40):
        delta = cmath.rect(math.exp(-n), random.uniform(0, 2*math.pi))
        phiA = (random.random(), random.random()); phiB = (random.random(), random.random())
        Ir += sum(incons(delta, 1/delta, s, phiA, phiB) for s in S)*0.05
        Ip += sum(incons(delta, delta**2, s, phiA, phiB) for s in S)*0.05
    print(f"n_e={n:+.0f}: int inconsistency  reciprocal(1/d)={Ir/40:.2f}   parabola(d^2)={Ip/40:.2f}")
```
Output:
```
n_e=+0: int inconsistency  reciprocal(1/d)=2.24   parabola(d^2)=1.86
n_e=+1: int inconsistency  reciprocal(1/d)=2.02   parabola(d^2)=2.19
n_e=+2: int inconsistency  reciprocal(1/d)=2.66   parabola(d^2)=4.63
n_e=+4: int inconsistency  reciprocal(1/d)=2.27   parabola(d^2)=10.89
n_e=+8: int inconsistency  reciprocal(1/d)=1.94   parabola(d^2)=22.93
n_e=-4: int inconsistency  reciprocal(1/d)=2.72   parabola(d^2)=14.72
n_e=-8: int inconsistency  reciprocal(1/d)=1.94   parabola(d^2)=25.98
```

---------------------------------------------------------------------------------------------------------------------

## E. Citation table (Milne, *Algebraic Number Theory* v3.08, 19 July 2020 — the version the paper cites as [19])

| Cited | Paper's claim | Source text (quoted from pdftotext of ANTc.pdf v3.08) | Verdict |
|---|---|---|---|
| [19, Thm 7.14] | classification of places of a number field | "THEOREM 7.14 Let K be an algebraic number field. There exists exactly one prime of K (a) for each prime ideal p; (b) for each real embedding; (c) for each conjugate pair of complex embeddings." | MATCH |
| [19, Thm 7.15] | product formula for normalised absolute values; complex place = squared modulus | "THEOREM 7.15 (PRODUCT FORMULA) For each prime v, let \| \|_v be the normalized absolute value. For every nonzero α ∈ K, ∏ \|α\|_v = 1 (product over all primes of K)." Normalisations (p.112): "for a prime ideal p of O_K, \|a\|_p = (1/Np)^{ord_p(a)} …; for a real embedding σ: K ↪ R, \|a\| = \|σa\|; for a nonreal complex embedding σ: K ↪ C, \|a\| = \|σa\|²." | MATCH (paper's "His complex-place value is squared modulus" is exactly this) |
| [19, Lemma 8.6] | Milne's finite-place value equals \|·\|_p^{n_p} | "LEMMA 8.6 In the above situation, ‖a‖ = \|a\|^n, where n = [L:K]." Situation: "Let K be a local field with normalized absolute value \| \| … Let L be a finite separable extension of K, and let \| \| be the unique extension of \| \| to L. Let ‖ ‖ be the normalized absolute value on L". Applied with K = Q_ℓ, L = N_p. | MATCH |
| [19, Thm 3.20] | a principal fractional ideal has finitely many prime factors | "THEOREM 3.20 Let A be a Dedekind domain. The set Id(A) of fractional ideals is a group; in fact, it is the free abelian group on the set of nonzero prime ideals." | MATCH |
| [19, Prop 8.2] | Σ_{q\|p}[L_q:N_p] = [L:N] | "PROPOSITION 8.2 Let \| \| be a absolute value on K (archimedean or discrete nonarchimedean) and let L be a finite separable extension of K. Let K̂ be the completion of K with respect to \| \|. Then \| \| has finitely many extensions \| \|_1, …, \| \|_g to L; if L_i denotes the completion of L with respect to the absolute value \| \|_i, then L ⊗_K K̂ ≅ ∏_{i=1}^g L_i." | MATCH up to a one-line K̂-dimension count (Objection 2) |

Not in my scope but encountered: the paper's [17] (real-closed transfer, Lemma 2.1) and [20] (Kummer, §8.5) were not fetched.

---------------------------------------------------------------------------------------------------------------------

## F. Verdict for scope

**HOLDS AS READ** for all of Section 4 (pp.16–22): (4.1); Lemma 4.1; Lemma 4.2 incl. (4.3)–(4.6); §4.2 incl. (4.7)–(4.9);
Lemma 4.3; Proposition 4.4 (brief item (iv)); §4.4 incl. (4.16)–(4.17); Lemma 4.5 incl. (4.18). Only COSMETIC objections
(1: 8Bτ derivation omitted but correct, true constant ≤ (4√2+1)Bτ; 2: Prop 8.2 citation needs a dimension count;
3: "Theorem" labels for Lemmas/Props, all correctly targeted; 4: harmless ≤/< at log√2).
Section 4 is not where the 4/3 barrier is broken: Prop 4.4 (bounded S) would go through for a parabola-type metric too;
the Euclidean input that §4 contributes to the S → ∞ branch is Lemma 4.5's O(1) consistency, which provably needs the
reciprocal jumps d, d^{−1} (control: with d² its nonarchimedean part becomes 3·E Σ*_{finite}|n_e(v)|, of the order of the heights). Whether §5–§8 use that
consistency correctly is other seats' scope.

STATUS: COMPLETE.
