# Hostile referee report — seat `whole`
**Paper:** OpenAI, "The weak pinned planar distance theorem", 23 Sep 2026, 27 pp. (local `/tmp/oaimath/604/paper.pdf`; every quote below is
from the rendered PDF pages, not from `paper.txt`). Erdős problem #604.
**Scope:** (1) the whole paper as a dependency graph (hypotheses → where supplied; subsequence bookkeeping §2/§6/§7; the two-regime
split; anything used before it is proved); (2) brief item (i), the characteristic-zero input, in full, with a literature search for
anything that would refute the generalized statement the argument proves; the F_q(T) sanity test; (3) brief items (ix) and (x);
(4) the Lean statement reading (`Model.lean`, `Main.lean`, `Pins.lean`, the comparator), read as text only.
**Seat:** Opus 5.5, tool-equipped, 2026-10-14 ~15:3x–16:0xZ. No lean/lake was run.

---

## VERDICT FOR THIS SCOPE: HOLDS AS READ.

- **Dependency graph.** Every lemma, proposition and equation gets its hypotheses from an earlier, proved statement. Nothing is
  used before it is proved. The subsequence bookkeeping is clean: (2.2)–(2.4), (4.5) and (5.2) are proved along the full
  Proposition 2.2 sequence and survive any subsequence; §6 and §7 then take nested subsequences and never drop an earlier one.
  The two-regime split (W → ∞ / W bounded) is exhaustive, and the closing paragraph applies it correctly.
- **Characteristic-zero input (brief (i)).** The argument proves, verbatim, a strictly more general **Theorem G**: any finite set
  with two injective coordinate maps Z₁, Z₂ into Q̄, with "distance" (Z₁(y)−Z₁(x))(Z₂(y)−Z₂(x)). By transfer this includes:
  - the real Minkowski plane with no two points on a light-like line;
  - C² with the complex bilinear distance and no two points on an isotropic line.

  The Lean core says the same thing: `arithmetic_sequence_impossible` is stated for abstract vertex types and arbitrary injective
  maps into number fields. I found no counterexample to Theorem G anywhere: not in Roche-Newton–Rudnev, Sheffer–Zahl, Dewar et
  al. §1.3.2/§4, or Lee–Pohoata–Zhu arXiv:2607.05374. The 2026 "vertical amplification" number-field constructions also do not
  give one: they enlarge the space of possible distance values relative to n, by (2√D)^d. **Not FATAL.**
- **F_q sanity test.** There are two cases:
  - q ≡ 1 (mod 4): the proof breaks at §3.1, because Z₁ is not injective and t vanishes on distinct pairs.
  - q ≡ 3 (mod 4): every §3.1 hypothesis holds in F_{q²}, and §3–§5 hold trivially in F_{q²}(T) with W = 0. The proof breaks
    exactly at §7.1, which needs an archimedean place and one fixed compact target space, the Riemann sphere, for every
    configuration.

  So the decisive characteristic-zero input is §7. It is used correctly.
- **(ix).** No circularity, no limit taken before a sup, no configuration-dependent o(1). The proof is ineffective, and the paper
  says so. The paper claims exactly what it proves.
- **(x).** Corollary 1.2's half-page proof checks line by line, and so does the Lean's `bad_fraction_bound`. A finite exact check
  agrees with both, and its deliberately wrong control fails.
- **Lean statements.** `main`, `pins`, `pinsStatement` and `exists_pin_eventually` say exactly Theorem 1.1, Corollary 1.2, and
  "eventually some pin has ≥ n^{1−ε} distinct nonzero distances". The last is logically equivalent to the first question of #604
  but not verbatim: the page counts the zero distance, and its "≫ n^{1−o(1)}" is unpacked as ∀ε eventually. No definition weakens
  the statement or makes it vacuous. The choice `EuclideanSpace ℝ (Fin 2)` matters: with `Fin 2 → ℝ` the metric would be ℓ∞, and
  the statement would be false.

Objections: 6, all COSMETIC (plus 2 remarks). No FATAL, no GAP, in either proof or exposition.

---

## 1. Dependency graph (every numbered item: needs → supplied by; status)

Status key: **VLL** = verified line by line by me; **SK** = skimmed, i.e. read and logic checked, but constants or algebra not redone
(a sibling seat redid them, and its verdict is noted); **NR** = not read.

| Item (PDF p.) | Needs (hypotheses) | Supplied by | Status |
|---|---|---|---|
| Def. of D_x(P), k_P, F_n(s); Thm 1.1 (p.2) | — | — | VLL. k_P counts y itself; F_n is a sup over |P| = n, so the convergence is uniform. |
| Cor. 1.2 + proof (p.2) | F_n(ε/2) → 0 | Thm 1.1 | VLL + finite check (§5 below) |
| Θ, s*, (2.1) (p.5) | Θ nonincreasing; F_n(t) = 0 for t ≥ 1 | definitions | VLL. 0 < s* ≤ 1, θ = Θ(s) > 0 because s < s*. The factor 1/3 in c < s*/3 is never used (Obj. 1). |
| Lemma 2.1 (p.5) | Θ continuous at s (left-continuity suffices) | choice of s in (2.1) | VLL |
| Prop 2.2, transfer paragraph (p.6) | finitely many values ⇒ maximum attained; RCF transfer [9] | finiteness; Kuhlmann (not fetched by me; `sources` seat) | VLL (logic). The Lean uses a specialization theorem instead (§4 R2). |
| Prop 2.2, deletion + contradiction + (2.5) (pp.6–7) | Lemma 2.1 with r_N = f_N → s, M_N = m₀ → ∞; at most N(N−1)/N^s initial fibers | Lemma 2.1 | VLL. Excess = η_N A_N(1 − B_N/A_N − η_N) > 0; a fiber never splits because its key is (source, squared distance). |
| (2.2), (2.3) (p.7) | d_n → θ; degree lower bound | (2.5) | VLL. B₀ = 2/θ; q_Y{d⁻ < n^γ} ≤ n^{1+γ}/|E|. |
| (2.4), both regimes (p.8) | Lemma 2.1 with r = s − δ_n, M = n^{1−c}; Θ(s′) = 0 for s* < s′ < s/(1−c); counted pairs have k_C(x_e,y) ≥ |F_e ∩ C| ≥ T_n | (2.1), Lemma 2.1, definition of s* | VLL. Uses k_C (fibers restricted to C), so applying F_m to subsets is legitimate (brief (ii)). |
| §3.1: Z₁, Z₂, (3.1), (3.3) (p.9) | real u, b ⇒ injective; t ≠ 0 | Prop 2.2 (real algebraic points) | VLL |
| (3.2) normalized product formula (p.9) | K a number field, i ∈ K ⇒ all archimedean places complex | Prop 2.2 | VLL against the standard normalized product formula Π_v‖z‖_v = 1 (‖·‖ = |·|² at complex places, |N_{K_v/Q_p}(·)|_p at finite places). Dividing the logarithm by [K:Q] gives exactly σ_v = [K_v:Q_p]/[K:Q] with |p|_v = p⁻¹, σ_v = 2/[K:Q] at complex places, and Σ_{v∣∞}σ_v = 1. I did not fetch Milne's theorem numbers (`arithmetic`/`sources` seats did). |
| §3.2 grids; Lemma 3.1, (3.4) (pp.9–10) | — | construction | SK. I checked the pair-independence logic: {Δ ≥ u} = {share at the largest side ≤ Re^{−u}}, whose law depends only on the log-uniform phase, the direction and the shift. `arithmetic` seat: HOLDS, KS + quadrature. |
| §3.3, Lemma 3.2, (3.5) (pp.10–11) | Lemma 3.1 for integrability | Lemma 3.1 | VLL for the pointwise identity o − g = t − 1{G, x∉G} − 1{G, y∉G}, all four cases by hand. Integrability: SK. |
| §3.4, ⟨d₁+d₂⟩ = 2κ, (3.6), (3.7) (pp.11–12) | (3.2), Lemma 3.1 (E Δ = κ at every complex place), Σ_{v∣∞}σ_v = 1, (3.5), finiteness (Lemma 3.2 + finitely many non-unit places) | §3.1–3.3 | VLL. b* = 2κ − ⟨M₁+M₂⟩. |
| (4.1) (p.12) | (3.6), (q_X+q_Y)/2 ≥ (1−ε_n)α, q ≤ B₀π, S* ≥ 0, L* ≥ 0 | (2.2), (3.6) | VLL. E_q L* = W₂ + Σ_x(q_X+q_Y−2α)S*. |
| Lemma 4.1, (4.2)–(4.4) (pp.12–14) | (3.3), (3.4), q ≤ B₀π, nesting, Σ_{v∣∞}σ_v = 1; 0<λ<1/2, 2/n ≤ τ ≤ 1, H ≥ 1 | §2, §3 | SK. `smallcells` seat: HOLDS, exact rational toy check. |
| T(λ_n) = o(W+1) and (4.5) (p.14) | Lemma 4.1 with λ = 1/log n, τ = λ^{1/3}, H = λ^{−1/2} (hypotheses met for n ≥ 8); (2.4) uniform in C; (4.1) | Lemma 4.1, (2.4), (4.1) | VLL. W_{2,sm}(1 − o(1)) ≤ o(1)A + o(1)W₂ + o(W+1). |
| Lemma 5.1, (5.1)–(5.7) (pp.15–16) | uniform laws on B with k ≥ n^γ; weights independent of places/grids, total ≤ 1; E_Fν ≤ Mα; (3.6); W₂ < ∞; (4.5); c < γ | (3.6), (4.5), (2.1) | Hypotheses and logic of (5.3): VLL. I checked the m ∈ {0,1} cancellation of (5.4) by hand (p = 0 and p = 1/k both give 0). The algebra of (5.4)–(5.7): SK. `variance` seat: HOLDS, exact rational check with 6 failing controls. |
| Applications + (5.8) (p.17) | k_e ≥ n^{s−o(1)} ≥ n^γ (γ < s); E_eμ_e = q_Y ≤ B₀α; Σ_y q_Y(y)ρ_y = q_X ≤ B₀α; d_y ≥ n^γ | Prop 2.2 | VLL |
| W ∈ [0,∞), split (p.17) | finiteness of W | §3.4 | VLL |
| (6.1)–(6.4) (pp.17–18) | (3.5), (3.3), (3.4), (4.1), (6.2) [averaging (3.6) over y ≠ x, n > 2], conditional independence of Y, Y′, (5.2) for fibers, E_e p = q_Y(C) ≤ B₀a | §3–§5 | VLL. min{a₁+a₂, b₁+b₂} ≤ Σ min{a_i,b_j}; coefficient 2 checked. |
| (6.5) (p.18) | Lemma 4.1 with λ = 2δ < 1/2 (δ < 1/4), τ = λ^{1/3}, H fixed; (5.2) both terms; p ≥ 2δ ≥ 2/k_e eventually | Lemma 4.1, (5.2) | VLL |
| w, ℓ_j, (6.6), (6.7) (p.19) | (6.5); symmetry w(u) = w(1−u); Lipschitz w; Cauchy–Schwarz; (5.2) for both families | (6.5), (5.2) | VLL |
| (6.8), (6.9) (p.19) | nested (ultrametric) partitions | §3.2 | VLL. Ultrametric argument: for d(a₁,z) > d₀, d(a₀,z) = d₀. |
| (6.10), U/V, (6.11) (p.20) | (3.1) on the fiber; (3.4) first moment; (6.7) first term (fiber family) | §3, (6.7) | VLL. I derived (6.10) myself: Z_{j′}(z) − Z_{j′}(y) = t_e(Z_j(y)−Z_j(z))/((Z_j(z)−Z_j(x))(Z_j(y)−Z_j(x))). |
| Tree, (6.12) (pp.20–21) | finite nested partition | §3 | SK (standard). `transport` seat: HOLDS numerically. |
| (6.13), coupling, (6.14) (p.21) | q_Y = E_eμ_e, convexity; (6.7) second term for both families; (5.8); T_j ≤ ℓ_j; (6.6); (6.11); triangle inequality for D_j | §5, §6 | VLL |
| Lemma 6.1 + application (p.22) | each positive edge separates α-mass ≥ δ/2 on both sides | w = 0 off (δ/2, 1−δ/2) | VLL: E d(X,y) ≥ δL/2; Pr ≥ δ/4; M = ⌈16/δ⌉+1 walk pieces; Σα(C_r)² ≥ 1/M; product δ/(4M)·δL/8. Then (6.6) + (6.14) give W ≪ o(W). |
| §7.1 place selection, (7.1)–(7.3), β_j (pp.22–23) | W ≤ C; Σ_{v∣∞}σ_vV_v = o(1) [(5.2) with W bounded]; Markov over archimedean weights summing to 1; (3.5), (3.4) | §3, §5 | VLL. (7.1) has the outer absolute value in the PDF ("E_π|log|U_j(x) − U_j(y)|| ≤ C₁"). |
| (7.4), (7.5) (pp.23–24) | V_v ≤ 2η_n at the selected place; ≤ N(R,ε) squares; (7.2); α_n^j ⇒ β_j | §7.1 | VLL (logic); N(R,ε) bookkeeping SK |
| §7.3 joint limit, independence, (7.6) (pp.24–25) | (7.4) for both families; q ≤ B₀π ≤ 2B₀α⊗α; nonatomic β_j; closedness of the pushforward graph on the open domain; zero prelimit mass (U_j injective, exact Möbius relation) | §7.1–7.2 | VLL (logic) |
| Lemma 7.1, (7.7), (7.8) (pp.25–26) | nonatomic β₁, β₂; a ⊥ (a′,b′); a′ ∈ supp β₁, b′ ∈ supp β₂ | §7.3 | VLL. Includes the choice of l with 1/l ≤ min(p,q), giving RHS ≥ log(r₀/r) > 0, and the existence of a_k → a′ inside the full-measure set. |
| Closing paragraph (p.26) | both regimes excluded; every nonnegative sequence has a bounded or → ∞ subsequence | §6, §7 | VLL |

**"Clearly / it follows / similarly / the same argument / standard / directly" census (whole paper).** I checked all 7:
- "it follows" (p.12, (4.1)): verified.
- "The same argument will apply to the conditional law of sources" (p.15): it is actually carried out in (5.8)/§7.2.
- "standard" ×3 (pp.4, 21): (6.12) is proved in place.
- "Directly from the cell definition" ((6.9), p.19): verified.
- "a similar use of (7.1)" ((7.3), p.23): the argument is written out in the next sentence.

None of these phrases hides a step.

---

## 2. Subsequence bookkeeping and the two regimes (brief (ix), part)

1. **§2.** A sequence N_k → ∞ with F_{N_k}(s) → θ exists by the definition of limsup. The deletion output n_k ∈ (N_k/2, N_k], so
   n_k → ∞. Every o(1) in (2.2)–(2.5) is a function of the sequence index only. This is because b_N, t_N, η_N, K_N, T_n are
   built from F_m, θ, log N, log n, never from the configuration. ✓
2. **§4–§5.** (4.5) and (5.2) are proved along the full sequence. The paper says explicitly: "This estimate holds before passing
   to either a bounded or an unbounded subsequence of W" (p.14). ✓
3. **§6.** A subsequence with W → ∞. The cutoff δ is fixed once, before n → ∞, and the O(δ^{1/3}W) constant does not depend on
   δ (p.18). ✓
4. **§7.** A subsequence with W ≤ C. A place is selected per n, then a common subsequence makes α_n^1, α_n^2 converge. (7.4)
   holds along it. A further subsequence gives Q, and (7.4) and the independence estimate pass to it. ✓ No later step needs a
   property of a discarded index.
5. **Closing.** "Every sequence of nonnegative real numbers has a bounded subsequence or a subsequence tending to infinity"
   (p.26). This is true and correctly applied: W is finite and nonnegative for every configuration, by §3.4. ✓

---

## 3. Brief item (i): THE CHARACTERISTIC-ZERO INPUT

### 3.1 Every step that uses the reals, the number field, or an archimedean place

| # | Location | What is used | Role |
|---|---|---|---|
| R1 | §2 transfer (p.6) | real closed field transfer: "Their existential sentence holds over R and therefore over the real algebraic numbers, by transfer for real closed fields [9, Theorems 3.1 and 4.1]" | puts the configuration in a number field; "Require D_ij > 0 for i < j" encodes distinctness |
| R2 | §3.1 (p.9) | "Both maps are injective, because u, b are real in the given embedding." | injectivity of Z₁, Z₂ ⇒ t(x,y) ≠ 0, raw depths finite on distinct pairs, h_e finite. In the Euclidean case this is the only use of reality: no two real points lie on a common isotropic line u ± ib = const. |
| N1 | (3.2) (p.9) | normalized product formula of a number field | gives ⟨i₁+i₂⟩ = 0 on every distinct pair, hence the additive identity (3.6). (The `arithmetic` seat notes ⟨i_j⟩ = 0 holds for each j separately.) |
| A1 | §3.2, Lemma 3.1 (pp.9–10) | random rotated, log-uniformly scaled square grids in C at each complex place; Euclidean geometry of C | nested partitions with a pair-independent depth error Δ of mean κ. At finite places Δ = 0. |
| A2 | §3.4 (p.12), (4.4) (p.13), (6.1) (p.17), (6.11) (p.20), (7.1) (p.23) | Σ_{v∣∞}σ_v = 1 | makes every grid-error bound absolute and uniform in the varying field: "Every absolute grid-error bound remains uniform in K, since its archimedean weights sum to one." |
| A3 | §7.1 (pp.22–23) | choosing an archimedean place with T_v ≤ 2C+1, V_v ≤ 2η_n (Markov over archimedean weights summing to 1); normalizing U_j = e^{m_j}Z_j + b_j in C; tightness and nonatomicity on the Riemann sphere Ĉ [14] | **the decisive use**: one fixed compact space receives the normalized coordinates of every configuration, whatever its number field |
| A4 | §7.3–7.4 (pp.24–26) | Möbius maps on Ĉ, weak limits, Portmanteau; Lemma 7.1 on nonatomic laws on C | the final obstruction |

A1/A2 are bookkeeping. In a field with no archimedean place they would just disappear (Δ ≡ 0, κ term absent). **A3 is the only
step that has no non-archimedean replacement** (§3.3 below).

### 3.2 The generalized theorem the argument proves verbatim

> **Theorem G (implicit in §§2–7).** Call (P, Z₁, Z₂) *admissible* if P is a finite set with n = |P| ≥ 2 and Z₁, Z₂ : P → Q̄ are
> injective. For distinct x, y ∈ P put t(x,y) = (Z₁(y) − Z₁(x))(Z₂(y) − Z₂(x)) (≠ 0) and
> k(x,y) = #{z ∈ P∖{x} : t(x,z) = t(x,y)}. Let F^G_n(s) be the sup over admissible triples with |P| = n of
> #{(x,y) : x ≠ y, k(x,y) ≥ n^s}/(n(n−1)). Then F^G_n(s) → 0 for every fixed s > 0. Consequently, for every ε > 0, all but o(n)
> points x of every admissible triple see at least n^{1−ε} distinct values t(x,·), uniformly in the triple.

**Why the argument proves this verbatim.**
- **§2** uses only three facts (the `extremal` seat reached the same conclusion independently):
  - F_m is a sup over a class closed under taking subsets;
  - the (source, value) classes at a pin partition the other points;
  - the counting is finite.
- **The transfer step.** Theorem G needs ACF₀ transfer (Q̄ ≺ C, so any complex triple has an algebraic copy with the same
  equality/inequality pattern), with "t_ij ≠ 0" in place of "D_ij > 0".
- **§§3–7** never use Z₂ = conj(Z₁). The paper says so itself (p.3): "At other complex embeddings the two maps need not be
  conjugates; the algebraic factorization remains valid." Section 3.1 (p.9) adds: "their injectivity and the algebraic
  factorization below are the properties we use."

**Incarnations of Theorem G (all by transfer):**
- (a) the Euclidean plane: Z₂ = conj Z₁ at the identity embedding, with injectivity automatic (R2);
- (b) the real Minkowski plane: (u−u′)² − (v−v′)² = (Δ(u+v))(Δ(u−v)), with no two points on a common light-like line;
- (c) C² with the complex *bilinear* distance (z₁−w₁)² + (z₂−w₂)², with no two points on a common isotropic line of slope ±i;
- (d) any field of characteristic 0: a finitely generated subfield embeds in C.

**The Lean confirms the generality.** The formal core contradiction is stated at exactly this level
(`ArithmeticContradiction.lean`, lines 37–45, verbatim):
```
theorem arithmetic_sequence_impossible
    (G : ∀ j,Core.Fibers (V j) (I j)) (θ γ c : ℝ) (η : ℕ → ℝ)
    (Z₁ Z₂ : ∀ j,V j → K j) (h₁ : ∀ j,Function.Injective (Z₁ j)) (h₂ : ∀ j,Function.Injective (Z₂ j))
    ...
    (hG : ∀ j,PreparedGraph (V j) (I j) (G j) θ γ c (η j))
    (t : ∀ j,I j → K j) (ht : ∀ j e y,y∈(G j).targets e →
      (Z₁ j ((G j).source e)-Z₁ j y)*(Z₂ j ((G j).source e)-Z₂ j y)=t j e) : False
```
Here `K j` carries a `NumberField` instance, V j is an abstract finite type, and `PreparedGraph` (`IncomingFibers.lean`, lines
333–342) is purely combinatorial: density, degree, fiber size > n^γ, and the two subset bounds. No plane, no reals, no conjugation.

**Consequence.** If the kernel replay holds, the core of Theorem G is formally true. Our replay so far shows: all 48 modules
built (rc 0); `main`/`pins`/`pinsStatement`/`exists_pin_eventually` depend on [propext, Classical.choice, Quot.sound];
`statement_match_v3` = MATCH; `leanchecker --fresh` was still running at 15:46Z (empty log). A counterexample to Theorem G of the
PreparedGraph form would therefore contradict a kernel-checked theorem. The paper does not state Theorem G. Its incarnations
(b) and (c), pinned Minkowski and pinned complex distances, appear to be **new by-products**: I found no prior statement of either
(see 3.4). This is not an objection. It is the honest scope of the method, and it makes the characteristic-zero input transparent
(Remark R1).

### 3.3 The finite-field sanity test: where exactly does the proof break?

Script `fq_sanity.py` (§6 below), output verbatim:
```
q= 3 (q mod 4 = 3) n=   9 Z1 injective=True Z2 injective=True distinct pairs with t=0:     0 MIN over pins of #distinct nonzero t = 2 (sqrt n = 3); fiber sizes over ordered pairs: {4: 72}
q= 7 (q mod 4 = 3) n=  49 Z1 injective=True Z2 injective=True distinct pairs with t=0:     0 MIN over pins of #distinct nonzero t = 6 (sqrt n = 7); fiber sizes over ordered pairs: {8: 2352}
q=11 (q mod 4 = 3) n= 121 Z1 injective=True Z2 injective=True distinct pairs with t=0:     0 MIN over pins of #distinct nonzero t = 10 (sqrt n = 11); fiber sizes over ordered pairs: {12: 14520}
q=19 (q mod 4 = 3) n= 361 Z1 injective=True Z2 injective=True distinct pairs with t=0:     0 MIN over pins of #distinct nonzero t = 18 (sqrt n = 19); fiber sizes over ordered pairs: {20: 129960}
q=23 (q mod 4 = 3) n= 529 Z1 injective=True Z2 injective=True distinct pairs with t=0:     0 MIN over pins of #distinct nonzero t = 22 (sqrt n = 23); fiber sizes over ordered pairs: {24: 279312}
q= 5 (q mod 4 = 1) n=  25 Z1 injective=False Z2 injective=False distinct pairs with t=0:   200 MIN over pins of #distinct nonzero t = 4 (sqrt n = 5); fiber sizes over ordered pairs: {4: 400}
q=13 (q mod 4 = 1) n= 169 Z1 injective=False Z2 injective=False distinct pairs with t=0:  4056 MIN over pins of #distinct nonzero t = 12 (sqrt n = 13); fiber sizes over ordered pairs: {12: 24336}
```
**Reading.**
- **q ≡ 1 (mod 4)** (this is the control that must fail §3.1's hypotheses, and it does): i ∈ F_q, Z₁ = u + iv is not injective,
  and t vanishes on 200 / 4,056 ordered distinct pairs, namely those on isotropic lines. Raw depths would be +∞ on distinct pairs.
  **The proof breaks at R2/§3.1.**
- **q ≡ 3 (mod 4)**: every hypothesis the paper takes from the reals holds inside F_{q²} = F_q(i). Z₁ and Z₂ are injective,
  t ≠ 0 on distinct pairs, and t ∈ F_q^×. Yet every pin sees only q − 1 = √n − 1 values, and every ordered pair lies in a fiber
  of size q + 1 ≈ √n. So F^G_n(s) = 1 for s ≤ log(q+1)/log(q²) → 1/2, and Theorem G **fails over F_{q²}**. Now place
  P = F_q² ⊂ F_{q²}(T)² (constant coordinates):
  - Every difference is a nonzero constant, hence a unit at every place, so i_j ≡ 0 everywhere.
  - Each hierarchy is {P} for r ≤ 0 (a giant, replaced by ∅) and singletons for r > 0, so M = S = L = 0 and W = 0.
  - The product formula holds in the global function field with no archimedean term, so (3.6) holds trivially. T(λ), W_{2,sm}
    and the Lemma 5.1 integrals all vanish.
  - §6 is never entered. The family is in the **bounded-W regime**, and §7.1 begins "At an archimedean place v …". F_{q²}(T) has
    none.

  More fundamentally, §7 needs a single compact space where the normalized coordinates of all configurations live. Here the
  residue fields F_{q²} change with n. In any fixed non-archimedean local field with residue field of size Q, at most Q points
  can be pairwise at distance 1, so no tight, nonatomic limit (the analogue of (7.2)–(7.3)) can exist. **The proof breaks at
  A3 (§7.1), and only there.**

The argument therefore does use something false over F_q, in the right place: the archimedean compactness of §7. The
characteristic-zero input is real, located, and used correctly.

**Rank control (why the factorization (3.1) is load-bearing).** A quadratic form splits into two linear forms over Q̄ iff its rank
is ≤ 2. For rank ≥ 3, few pinned distances do happen. Script `rank_control.py`, output verbatim:
```
R^3 grid k= 6 n=  216: distinct sq-distances per pin in [18,44]  vs n^(2/3)=36  n^0.9=126
R^3 grid k=10 n= 1000: distinct sq-distances per pin in [44,144]  vs n^(2/3)=100  n^0.9=501
R^3 grid k=14 n= 2744: distinct sq-distances per pin in [87,299]  vs n^(2/3)=196  n^0.9=1243
R^2 grid k=20 n=  400: distinct sq-distances per pin in [60,179]  vs n/sqrt(log n)=163
R^2 grid k=40 n= 1600: distinct sq-distances per pin in [197,652]  vs n/sqrt(log n)=589
R^2 grid k=60 n= 3600: distinct sq-distances per pin in [407,1396]  vs n/sqrt(log n)=1258
```
In R³ every pin of the grid sees O(n^{2/3}) distances, so the weak pinned statement is false there. The paper's method cannot run
there because (3.1) does not exist. The same holds for C² with the *Hermitian* distance (= R⁴, rank 4). The method applies exactly
to the rank-2 forms: Euclidean plane, Minkowski plane, complex bilinear plane. Those are the settings where n^{1−o(1)} is expected.
Consistent.

### 3.4 Literature search for anything refuting or supporting Theorem G

Searched with WebSearch (standard + extended), arXiv abstract and PDF fetches, and the saved Dewar et al. text. Findings:

| Source | What it says (quote) | Bearing on G |
|---|---|---|
| Roche-Newton–Rudnev, arXiv:1203.6237 (Israel J. Math. 2015), fetched | Abstract: "We prove that N > 1 points in the Minkowski plane R^{1,1} generate Ω(N/log N) distinct distances, or all the distances are zero." Intro p.2: "Stronger versions of the conjecture in R² (e.g. the pinned one – proving the lower bound for the size of the set of distances from a 'typical' point of P) remain open". | Global Minkowski analog of (b) is proved. Pinned: nothing. Supports, does not decide. |
| Sheffer–Zahl, arXiv:2006.08886 (Trans. AMS 2021), abstract fetched | "We prove that if P is a set of n points in C², then either the points in P determine Ω(n^{1−ε}) complex distances, or P is contained in a line with slope ±i." | Global complex analog of (c) is proved. Pinned: nothing. Supports. |
| Dewar–Frankl–Mansfield–Nixon–Passant–Warren, arXiv:2505.06590v1 (local `refs/dewar.txt`) §1.3.2, Cor. 1.9, §4 | pseudo-Euclidean treatment is global only (rigid-graph realization counts, via [33] = Roche-Newton–Rudnev). §4 Thm 4.1 is pinned, but only "for most d-norms" (n/log²n). Conj. 4.7 = Euclidean weak pinned; Thm 4.10: weak UDC ⇒ weak pinned. | No pinned pseudo-Euclidean result, positive or negative. |
| Lee–Pohoata–Zhu, arXiv:2607.05374v1 (6 Jul 2026), fetched in full | Thm 2: "for every subset A ⊆ P of size at least 2, we have µ(A) ≳ |A|²/n^{1−δ}". The set is "a two-dimensional Minkowski grid obtained from a symmetric box in the ring of integers of a high-degree totally real number field". | Not a counterexample. Its most repeated distance has n^{1+δ} ordered pairs, an n^{δ−1} → 0 fraction of all pairs, consistent with Thm 1.1. The paper says nothing about pinned or distinct-distance counts. ("Minkowski grid" = Minkowski *embedding*, not the Minkowski metric.) |
| OpenAI unit-distance disproof (May 2026), Sawin arXiv:2605.20579, Alon et al. arXiv:2605.20695, Pohoata arXiv:2606.13619 (Elekes–Rónyai: f = x+y+(x−y)², |f(A,A)| ≤ |A|^{2−c}), Bloom–Sawin–Schildkraut–Zhelezov arXiv:2605.28781 (sum-product false over R), Tao's 3 Jul 2026 "digestion" post | The 2026 "vertical amplification" family. Tao's post and comments never mention distinct or pinned distances (WebFetch check). | No pinned counterexample claimed anywhere (searches for "weak pinned distance conjecture counterexample 2026" etc. returned none). |

**Structural reasons why no cheap counterexample exists (not a proof).**
1. If P is an orbit of a finite group of isometries, every pin sees the *same* distance set, which then equals the global
   distance set. Guth–Katz, Roche-Newton–Rudnev and Sheffer–Zahl then give n^{1−o(1)} at *every* pin. A counterexample to G must
   be inhomogeneous: different pins must see different small sets.
2. The 2026 number-field grids P = σ₁(B_K(X))² (K totally real, degree d, root discriminant ≤ D) multiply the space of available
   values. From any pin, the squared distances lie among the totally positive elements of O_K in Π_j[0, 8X²]. There are about
   (8X²)^d/√Δ_K = n·(2√D)^d of them, against n points. By contrast, in the Z² grid the values fill [0, 2n], which forces average
   multiplicity ≥ √log n. This is why amplification helps for one special value (unit distances) and hurts for "all distances
   at a pin".

   Heuristic, not made rigorous: the typical representation count 2^{ω_split} is beaten by the relative class number
   h⁻ ≈ (√D/π)^d L(1,χ). This uses the Tsfasman–Vlăduţ bound Σ_{p split} log p/(p−1) ≤ log D − O(1) and D ≥ 60.8 for totally real
   towers.
3. For integer configurations with polynomially bounded coordinates, Theorem 1.1 (and G) is trivial by the divisor bound
   (r₂(N) = N^{o(1)}). Any counterexample needs super-polynomial heights or growing degree. That is exactly the territory the
   product-formula/compactness machinery is built for.

**Verdict on (i):** No known configuration with injective coordinates, nonzero products, and a positive fraction of pins seeing
≤ n^{1−c} distinct products was found, over a number field, C, or the Minkowski plane. **No FATAL finding.** Absence is not a
proof, but here the Lean core is itself stated at the generality of G (3.2), so a refutation of G would contradict a kernel-checked
theorem, if the replay holds.

---

## 4. Brief items (ix) and (x)

**(ix) Quantifiers / prove-too-much.**
- **No circularity.** Θ and s* depend on nothing but the F_n. c, s, γ, θ are then fixed from s* and the continuity of Θ (2.1).
  B₀ = 2/θ. Every o(1) is in the sequence index (§2 above). The 1/3 in c < s*/3 is unused (Obj. 1).
- **No limit before a sup.** F_n is a sup over configurations (maximum attained); Θ is the limsup of the sups. ✓
- **No configuration-dependent o(1).** Prop 2.2: "All the errors are uniform in vertices, fibers, and subsets wherever these
  occur." §3: the field-dependence is killed by Σ_{v∣∞}σ_v = 1 (A2). §7: the constant B in E_Fν ≤ Bα is B₀ for both families;
  C₁ depends only on the W-bound C and absolute constants. ✓
- **Rate.** The proof is ineffective in three places:
  - the choice of a continuity point s of Θ;
  - the compactness extractions in §7.1/§7.3;
  - the overall proof by contradiction. The Lean uses `Classical.choice`.

  The paper says: "Its exponent s is fixed; the theorem supplies no explicit rate of decay." ✓ Nothing in the paper claims or
  implies a rate.
- **n/√log n.** Not claimed. The paper correctly calls it "the sharper pinned conjecture" (p.3). Corollary 1.2 is exactly n^{1−ε}.
  ✓
- **Claims vs. proof.**
  - Abstract: "all but o(n) points of any n-point planar set determine at least n^{1−ε} distinct nonzero distances" = Cor. 1.2. ✓
  - "The convergence is uniform over all configurations" holds because F_n is a sup. ✓
  - "An exceptional set is necessary: … the center sees just one nonzero distance": true (circle + centre). ✓
  - For erdosproblems.com/604, Cor. 1.2 gives: YES to the first question, (1−o(1))n good pins (the "≫ n many such points" variant
    on the page), and Σ_x d(x) ≥ (1−o(1))n^{2−ε}, the n^{2−o(1)} form of Erdős's averaged conjecture, not n²/√log n. It says
    nothing about n/√log n. The paper does not claim any of these extras.
- **Prove-too-much.** It proves *more* than stated: Theorem G, §3. It does not prove anything known false: not ℓ∞ (no
  factorization), not R³/R⁴ (rank ≥ 3, see the rank control), not F_q (breaks at §3.1 or §7.1).

**(x) Corollary 1.2's half-page proof — VLL.**
- "At a pin with fewer than n^{1−ε} distance classes, fewer than n^{1−ε+s} neighbors lie in classes of size less than n^s":
  there are at most #classes < n^{1−ε} small classes, each of size < n^s, so the total is < n^{1−ε+s} (and 0 if there are none).
  Classes are the distance classes at the pin, so a class of size ≥ n^s means k_P(x,y) ≥ n^s. ✓
- "Each such pin therefore contributes at least n − 1 − n^{1−ε/2} pairs counted by F_n(s)". ✓
- b(n−1−n^{1−ε/2}) ≤ n(n−1)F_n(ε/2), so b/n ≤ (n−1)F_n(ε/2)/(n−1−n^{1−ε/2}) → 0 once n−1 > n^{1−ε/2}. The bound does not depend
  on P because F_n is a sup. ✓
- The ε ≥ 1 remark: n^{1−ε} ≤ 1, while every pin has |D_x| ≥ 1 when n ≥ 2. ✓
- **Lean `bad_fraction_bound`** (Pins.lean) proves badPinFraction ≤ 2·pairFraction(ε/2) + 2·n^{1−ε/2}/n. It derives
  |bad|(n−1) ≤ |richPairs(ε/2)| + n·n^{1−ε/2}, then uses n^{1−ε/2}/(n−1) ≤ 2n^{1−ε/2}/n (n ≥ 2) and a lazy pairFraction ≤
  2·pairFraction. The factor 2 is harmless slack, and this form needs no case split on ε ≥ 1 (n^{−ε/2} → 0 for every ε > 0).
- Finite check: §6, `cor12.py`. Paper and Lean inequalities hold on 32 (configuration, ε) instances. The deliberately wrong
  control "b(n−1) ≤ R" (it drops the light-target term) is rejected on circle+centre+5far at ε = 0.4, 0.6.

---

## 5. Lean statement reading (read as text; files: `lean/OAI/Geometry/PinnedDistances/{Model,Main,Pins}.lean`, `lean/ComparatorChallenges/PinnedDistances.lean`)

The definitions `Plane`, `distanceFiber`, `k`, `richPairs`, `pairFraction`, `F` in `Model.lean` are **byte-identical** to the
comparator's (`diff` of the two blocks: IDENTICAL_DEFS).

In plain words:
- **`main (s) (hs : 0<s) : Tendsto (fun n => F n s) atTop (𝓝 0)`.**
  - `F n s` = for n ≥ 2, the supremum, over all n-point finite subsets P of the Euclidean plane, of
    #{(x,y) ∈ P×P : x ≠ y, n^s ≤ #{z ∈ P∖{x} : |z−x| = |y−x|}} / (n(n−1)). It is 0 for n < 2.
  - `main` says this tends to 0 for every s > 0. This is **Theorem 1.1 verbatim**: same k (counts y itself), same normalisation,
    same sup.
- **`pins (ε) (hε : 0<ε) : Tendsto (fun n => B n ε) atTop (𝓝 0)`.** `B n ε` = for n > 0, the supremum over n-point sets of
  (#{x ∈ P : #(distinct values of |y−x|, y ∈ P∖{x}) < n^{1−ε}})/n. `pins` says this tends to 0 for every ε > 0. This is
  **Corollary 1.2 verbatim**.
- **`pinsStatement : PinsStatement`** is the same as `pins`, packaged as the Prop `∀ ε>0, Tendsto (B · ε) atTop (𝓝 0)`.
- **`exists_pin_eventually (ε) (hε : 0<ε) : ∀ᶠ n in atTop, ∀ P, P.card = n → ∃ x ∈ P, n^{1−ε} ≤ #distances P x`.** For every
  ε > 0 there is n₀ such that every planar set of n ≥ n₀ points has a point with at least n^{1−ε} distinct nonzero distances to
  the others. This is Cor. 1.2's "In particular" sentence.

**Is `exists_pin_eventually` the problem page's first question verbatim?** No, but it is logically equivalent. The page asks
"must there be a point x ∈ A such that #{d(x,y) : y ∈ A} ≫ n^{1−o(1)}?". Two differences:
1. The page's set includes y = x, so it counts the distance 0. The Lean counts only nonzero distances (one fewer), which is
   immaterial.
2. "≫ n^{1−o(1)}" means: there is g(n) → 0 with every n-point set having a pin with ≥ n^{1−g(n)} distances. The Lean's form is
   "for all ε > 0, eventually ≥ n^{1−ε}". The two are equivalent by the standard diagonal choice of g.

The replay's `RightShape.lean` probe derives the from-scratch statement (no OAI definitions) from `exists_pin_eventually`, and
`WrongShape.lean` (exponent 1+ε) fails as it must (steps.tsv: rightshape 0, wrongshape 1).

**Could any definition make the formal statement weaker or vacuous?** I checked each:
- `dist` on `EuclideanSpace ℝ (Fin 2)` is the L² metric. The elaborated term in the replay's `comparator.log` goes through
  `PiLp.innerProductSpace`. With plain `Fin 2 → ℝ` it would be the sup metric, where the k×k grid has ≤ k distinct ℓ∞ distances
  at every pin and the statement would be FALSE. So this choice is load-bearing, and it is correct.
- `distances P x = (P.erase x).image (dist · x)` is a `Finset ℝ`. Repeated distances count once; 0 is excluded because x is
  erased (`distances_pos` proves every element > 0). Same as the paper's D_x(P).
- `k` counts y itself: y ∈ P.erase x and dist y x = dist y x. Same as the paper.
- `sSup`: the sets are nonempty (`Finset.exists_card_eq` on an infinite type) and bounded above by 1 (`bad_values_bddAbove`;
  for F, richPairs ⊆ the off-diagonal pairs). So `sSup` is a genuine supremum, and `le_csSup` gives pairFraction P s ≤ F n s for
  every P. The junk value sSup = 0 for unbounded sets never arises.
- Real power `(P.card : ℝ)^s` is `Real.rpow` on a positive base for n ≥ 1, monotone in the exponent. Fine.
- `if 2 ≤ n` / `if 0 < n` only change F, B for n ≤ 1, which is irrelevant to the limits.
- `Finset Plane`: points are distinct by construction.
- `pairFraction` divides by n(n−1) over ℝ, which is positive for n ≥ 2.

**Verdict on the Lean reading:** the formal statements are exactly the paper's, and non-vacuous. `exists_pin_eventually` is #604's
first question up to the immaterial zero-distance count.

**R2 (architecture difference, not an error).** The paper transfers *before* deletion, by real-closed transfer. The Lean
(`ArithmeticSequence.lean`, `core_arithmetic_model`, lines 237–249) extracts the graph on the real points first. It then uses a
"proved finite specialization theorem" (`Transfer.planar_factor_model`) to produce K ⊂ Q̄ with injective Z₁, Z₂ preserving the
full product/distance pattern (`… ↔ dist a b = dist c d`). These coordinates need *not* be real. This is a second, independent
confirmation that the core uses only injectivity plus the factorization.

---

## 6. Objections (numbered)

**1. (2.1), p.5 — COSMETIC (exposition).** "Fix 0 < c < s∗/3, max{c, (1 − c)s∗} < s < s∗, c < γ < s, (2.1)". The factor 1/3 is
never used. Later uses of c need only 0 < c < γ (n^{c−γ} in (5.1)), (1−c)s* < s (to choose s′ in (2.4)), and c < 1. Fix: drop
"/3". (The `extremal` seat found the same.)

**2. Prop. 2.2 / (2.4), pp.6–8 — COSMETIC (exposition).** The sequence is indexed by N ("Choose a sequence N → ∞ on which
F_N(s) → θ"), but Prop 2.2 and (2.4) speak of "n = |P| → ∞" and apply "By Lemma 2.1, F_m(s − δ_n) ≤ θ + o(1)" with index n.
Lemma 2.1 is stated with index N ("If r_N → s and M_N → ∞ …"). Since n(N) ∈ (N/2, N] and Lemma 2.1 holds for any sequences, the
readings agree. Fix: say every o(1) is in the sequence index.

**3. Notation collisions — COSMETIC.**
- η_N = √t_N (p.7) vs "Σ_{v|∞}σ_vV_v = η_n → 0" (p.22).
- N, the pre-deletion size, vs "At most N = N(R, ε) squares" (p.24).
- B₀ vs "E_Fν ≤ Bα for a fixed B" (p.24) vs B a subset (§5) or a cell (§6).

No step is affected.

**4. §7.1, p.22 — COSMETIC (mis-attribution).** "Since W is bounded, Lemma 5.1 gives Σ_{v|∞}σ_vT_v ≤ C, Σ_{v|∞}σ_vV_v = η_n → 0."
The first inequality is the bound W ≤ C itself (Σ_v σ_v T_v ≤ W₂ + A); only the second uses Lemma 5.1, via (5.2) with W bounded.
True as stated.

**5. §3.2, p.9 — COSMETIC (unstated convention).** "At a complex place we obtain the same nesting property from square grids." A
complex place is a conjugate pair {σ, σ̄}, and the paper never says which embedding carries the grid. It is immaterial: the grid
law (uniform orientation, log-uniform scale, uniform nested shifts) is invariant under reflection, so the law of the hierarchy and
|·|_v are the same either way. Fix: "use either embedding of the pair".

**6. §1.2 / §3.1 — COSMETIC (scope not stated; see Remark R1).** The paper says (p.3) "At other complex embeddings the two maps
need not be conjugates; the algebraic factorization remains valid", but it never states the general theorem this implies
(Theorem G). In particular it does not state the pinned Minkowski and pinned complex-bilinear analogues, which its proof (and the
Lean core `arithmetic_sequence_impossible`) establish. A referee would ask for this: it is the clearest way to show the reader
exactly which characteristic-zero input does the work (§7's archimedean compactness, §3.3 here). Not an error.

**Remarks (not objections).**
- **R1.** Theorem G (§3.2) is what the argument proves. The literature search (§3.4) found no counterexample, and the F_q test
  (§3.3) locates the decisive input at §7.1.
- **R2.** The Lean replaces real-closed transfer by a specialization theorem (§5).

No FATAL. No GAP. No objection rises above COSMETIC, in proof or exposition.

---

## 7. Finite checks (scripts verbatim, outputs, failing controls)

All scripts are in `/tmp/oaimath/604/seats/whole_checks/`. Each ran with `python3 -I` from /tmp, in under 60 s and under 100 MB.

### 7.1 `cor12.py` — Corollary 1.2 counting + Lean bound, with a control that fails
```python
# Finite check of Corollary 1.2's counting step (paper p.2) and of the Lean bound (Pins.lean, bad_fraction_bound).
# Exact: integer coordinates, squared distances as Python ints; n^x as floats only in the threshold comparisons.
import itertools, math, random, sys
from collections import Counter

def stats(P, eps):
    n = len(P); s = eps/2
    rich = 0; bad = 0; worst = None
    for x in P:
        cls = Counter((y[0]-x[0])**2 + (y[1]-x[1])**2 for y in P if y != x)
        nd = len(cls)                                   # |D_x(P)| : distinct nonzero distances at pin x
        r_x = sum(c for c in cls.values() if c >= n**s) # targets y with k_P(x,y) >= n^s
        rich += r_x
        if nd < n**(1-eps): bad += 1
    return n, rich, bad

def configs():
    for k in (5, 8, 12, 16):
        yield f"grid{k}x{k}", [(i,j) for i in range(k) for j in range(k)]
    # circle of radius^2 = 5^2*13^2*17^2 lattice points + centre (many lattice points on one circle)
    R2 = (5*13*17)**2
    r = math.isqrt(R2); circ = set()
    for a in range(-r, r+1):
        b = math.isqrt(R2-a*a)
        if a*a+b*b == R2: circ |= {(a,b),(a,-b)}
    circ = sorted(circ); yield f"circle({len(circ)})+centre", circ+[(0,0)]
    yield f"circle+centre+5far", circ+[(0,0)]+[(10**7+3*i*i+i, 7*i+11) for i in range(5)]
    random.seed(1)
    yield "random60", list({(random.randrange(10**6), random.randrange(10**6)) for _ in range(60)})
    yield "grid10+line", [(i,j) for i in range(10) for j in range(10)] + [(i, 100) for i in range(30)]

ok_paper = ok_lean = True; control_fail = False
for name, P in configs():
    for eps in (0.2, 0.4, 0.6, 0.9):
        n, R, b = stats(P, eps)
        # paper: b*(n-1-n^{1-eps/2}) <= R   (when the bracket is positive)
        lhs = b*(n-1-n**(1-eps/2)); paper = (lhs <= R + 1e-9)
        # Lean: b/n <= 2*R/(n(n-1)) + 2*n^{1-eps/2}/n
        lean = (b/n <= 2*R/(n*(n-1)) + 2*n**(1-eps/2)/n + 1e-12)
        # CONTROL (deliberately wrong): drop the light-target term, i.e. claim every bad pin's n-1 targets are rich: b*(n-1) <= R
        ctrl = (b*(n-1) <= R)
        ok_paper &= paper; ok_lean &= lean
        if b > 0 and not ctrl: control_fail = True
        print(f"{name:18s} n={n:4d} eps={eps:.1f} bad={b:4d} richpairs(eps/2)={R:6d} paper_ineq={paper} lean_ineq={lean} WRONG_control_holds={ctrl}")
print("PAPER INEQUALITY HOLDS ON ALL:", ok_paper, "| LEAN INEQUALITY HOLDS ON ALL:", ok_lean, "| wrong control rejected somewhere:", control_fail)
```
Output (selected lines; full output in `cor12.out`):
```
grid16x16          n= 256 eps=0.2 bad= 116 richpairs(eps/2)= 61404 paper_ineq=True lean_ineq=True WRONG_control_holds=True
circle(108)+centre n= 109 eps=0.4 bad=   1 richpairs(eps/2)=   108 paper_ineq=True lean_ineq=True WRONG_control_holds=True
circle+centre+5far n= 114 eps=0.4 bad=   1 richpairs(eps/2)=   108 paper_ineq=True lean_ineq=True WRONG_control_holds=False
circle+centre+5far n= 114 eps=0.6 bad=   1 richpairs(eps/2)=   108 paper_ineq=True lean_ineq=True WRONG_control_holds=False
grid10+line        n= 130 eps=0.2 bad=   6 richpairs(eps/2)= 10872 paper_ineq=True lean_ineq=True WRONG_control_holds=True
PAPER INEQUALITY HOLDS ON ALL: True | LEAN INEQUALITY HOLDS ON ALL: True | wrong control rejected somewhere: True
```
**Control.** In circle+centre+5far the centre is bad: it sees 6 < n^{1−ε} distances, 5 of whose classes are light. The wrong
inequality b(n−1) ≤ R reads 113 ≤ 108 and fails. The correct inequality b(n−1−n^{1−ε/2}) ≤ R holds.

### 7.2 `fq_sanity.py` — F_q² sanity test with the q ≡ 1 (mod 4) control
Script verbatim:
```python
# Sanity test (brief item (i)): P = F_q^2 inside the field F_{q^2} = F_q(i).
# For q = 3 mod 4: Z1(u,v) = u + i v, Z2(u,v) = u - i v are INJECTIVE on P and t(x,y) = dZ1*dZ2 = du^2+dv^2 is NONZERO
# for distinct points -- i.e. every hypothesis of Sec.3.1 that the paper takes from the reals holds -- yet every pin sees
# only q-1 = sqrt(n)-1 distinct values and every pair lies in a fiber of size q+1 ~ sqrt(n): F_n(s) = 1 for s <= log(q+1)/log(q^2).
# CONTROL that must FAIL the hypotheses: q = 1 mod 4 (i in F_q): Z1 not injective and t vanishes on distinct pairs (isotropic lines).
from collections import Counter
def run(q):
    # F_{q^2} for q = 3 mod 4 as pairs (a,b) = a + b*i with i^2 = -1; for q = 1 mod 4 take i = a square root of -1 in F_q
    pts = [(u,v) for u in range(q) for v in range(q)]
    n = len(pts)
    if q % 4 == 3:
        Z1 = lambda p: (p[0] % q, p[1] % q)          # u + i v  as an element of F_q(i)
        Z2 = lambda p: (p[0] % q, (-p[1]) % q)       # u - i v
    else:
        I = next(x for x in range(q) if (x*x+1) % q == 0)
        Z1 = lambda p: (p[0] + I*p[1]) % q
        Z2 = lambda p: (p[0] - I*p[1]) % q
    inj1 = len({Z1(p) for p in pts}) == n; inj2 = len({Z2(p) for p in pts}) == n
    zero_t = 0; minvals = n; maxfib_min = n; fibsizes = Counter()
    for x in pts:
        vals = Counter()
        for y in pts:
            if y == x: continue
            t = ((y[0]-x[0])**2 + (y[1]-x[1])**2) % q    # = (Z1(y)-Z1(x))(Z2(y)-Z2(x)) in F_{q^2}; lies in F_q
            if t == 0: zero_t += 1; continue
            vals[t] += 1
        minvals = min(minvals, len(vals))
        for y in pts:
            if y == x: continue
            t = ((y[0]-x[0])**2 + (y[1]-x[1])**2) % q
            if t: fibsizes[vals[t]] += 1
    return n, inj1, inj2, zero_t, minvals, dict(fibsizes)
for q in (3, 7, 11, 19, 23, 5, 13):
    n, i1, i2, z, mv, fs = run(q)
    print(f"q={q:2d} (q mod 4 = {q%4}) n={n:4d} Z1 injective={i1} Z2 injective={i2} distinct pairs with t=0: {z:5d} "
          f"MIN over pins of #distinct nonzero t = {mv} (sqrt n = {n**.5:.0f}); fiber sizes over ordered pairs: {fs}")
```
Output: verbatim in §3.3 above. **Control:** q = 5 and q = 13 fail injectivity, with 200 and 4,056 isotropic ordered pairs, as
they must.

### 7.3 `rank_control.py` — rank ≥ 3 control
```python
import math
def pinned_counts(pts):
    out = []
    for x in pts:
        out.append(len({sum((a-b)**2 for a,b in zip(x,y)) for y in pts if y != x}))
    return min(out), max(out)
for k in (6, 10, 14):
    P3 = [(i,j,l) for i in range(k) for j in range(k) for l in range(k)]; n3 = len(P3)
    mn, mx = pinned_counts(P3)
    print(f"R^3 grid k={k:2d} n={n3:5d}: distinct sq-distances per pin in [{mn},{mx}]  vs n^(2/3)={n3**(2/3):.0f}  n^0.9={n3**0.9:.0f}")
for k in (20, 40, 60):
    P2 = [(i,j) for i in range(k) for j in range(k)]; n2 = len(P2)
    mn, mx = pinned_counts(P2)
    print(f"R^2 grid k={k:2d} n={n2:5d}: distinct sq-distances per pin in [{mn},{mx}]  vs n/sqrt(log n)={n2/math.sqrt(math.log(n2)):.0f}")
```
(Header comment lines omitted here; the file has them.) Output: verbatim in §3.3. Here the "control" is the setting where the
statement is false (R³) and the method's (3.1) does not exist.

---

## 8. Citation table (my scope)

| Cited result | Paper claims | Source says | Status |
|---|---|---|---|
| [2] Dewar et al., arXiv:2505.06590v1, Conj. 4.7 | "the modern terminology appears, for example, in [2, Conjecture 4.7]" | "Conjecture 4.7 (Weak pinned distance conjecture). For any ε > 0, there exists a constant Cε > 0 such that … there exists a point q ∈ P, which determines at least Cε|P|^{1−ε} distances" (refs/dewar.txt l.1792) | MATCH. Cor. 1.2 ⇒ Conj. 4.7 (take C_ε small for n < n₀). |
| [9] Kuhlmann, Thms 3.1, 4.1 | RCF transfer | — | COULD NOT FETCH in my slot (`sources` seat). The Lean does not depend on it (R2). |
| [11] Milne v3.08, Thms 7.14–7.15, Lemma 8.6 | normalized product formula (3.2) | normalization checked against the standard product formula (§1 table) | normalization MATCH by derivation; theorem numbers not fetched by me (`arithmetic`/`sources` seats) |
| [14] van Gaans | compactness of P(S), Portmanteau | — | not fetched by me (`sources`/`limits` seats) |
| (uncited, for (i)) Roche-Newton–Rudnev 1203.6237 | — | quoted in §3.4 | fetched (PDF, v2) |
| (uncited) Sheffer–Zahl 2006.08886 | — | quoted in §3.4 | abstract fetched |
| (uncited) Lee–Pohoata–Zhu 2607.05374 | — | quoted in §3.4 | fetched (PDF, v1, 7 pp.) |

---

## 9. Verdict for scope `whole`

**HOLDS AS READ.** The dependency graph closes, the subsequence bookkeeping is clean, and the two regimes are exhaustive.
Corollary 1.2 and its Lean counterpart check, with a failing control. The Lean statements are faithful and non-vacuous.

The characteristic-zero input is genuinely used, at §7.1 (archimedean place ⇒ one fixed compact space, the Riemann sphere), plus
the realness that gives injectivity at §3.1. The F_q² family satisfies every other hypothesis and breaks exactly there.

The argument proves a more general Theorem G (two injective coordinate maps into Q̄). This includes pinned Minkowski and pinned
complex-bilinear analogues the paper does not state. The literature search found no counterexample to G, and the Lean core is
itself stated at G's generality.

COULD NOT CHECK: the cited theorem numbers in [9], [11], [14] (other seats). `leanchecker --fresh` was still running when I wrote
this.
