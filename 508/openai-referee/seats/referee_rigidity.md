# Referee report — seat `rigidity`
Paper: OpenAI, "The Euclidean plane is not five-colorable" (23 Sep 2026), /tmp/oaimath/158/paper/paper.pdf (PDF page = printed page).
Scope: §2 in full (Defs 2.1–2.2, Thm 2.3, Lemmas 2.4–2.7), §3 in full (Lemmas 3.1–3.5, proof of Thm 2.3), test (A) (Payne's rational graph),
the ergodic-decomposition question. Read from the rendered PDF pp. 3–4 (overview) and pp. 5–23. Finite checks in
/tmp/oaimath/158/seats/rigidity_checks/ (scripts + outputs reproduced at the end). Referee: Claude (Opus 5.5), 14 Oct 2026.

## 0. Verdict for this scope
**HOLDS AS READ.** I found no FATAL and no GAP in §2–3. Every lemma in scope was checked line by line. The objections below are
COSMETIC or exposition-only. Theorem 2.3 (every K-invariant probability ν on D with ν(C)=0 is Haar) is proved for ergodic ν
(pp. 18–22) and then for general ν by ergodic decomposition (p. 22). The proof is correct as written.

**Test (A) has a definite answer.** The step that uses something Payne's rational graph lacks is real and can be named exactly:
p. 13, in the proof of Lemma 2.7, *"Each |x_j| < 1 is a sum of two elements of K … The square roots belong to F"*. For the rational
graph, both Lemma 2.7 and Theorem 2.3 are actually FALSE: I give an explicit counterexample, ν₃, in §2 below. So for the rational
graph the method proves nothing, and the paper's argument does not "prove too much" there. See §2.

## 1. Line-by-line status
| Item (page) | Status | Notes |
|---|---|---|
| Def 2.1 + following paragraph (p. 6): divisibility of K, metrizability of D, j continuous injective, C Borel, j⁻¹ Borel, a·C = C | VERIFIED LINE BY LINE | Divisibility is correct ("complex nth root of an algebraic number of modulus one is again algebraic and has modulus one"). |
| Def 2.2, Thm 2.3 statement (p. 6) | VERIFIED | Section 4 only needs f_ν(z)=0 for z≠0. The Lean `wild_fourier` states exactly that. |
| Classical-analogue paragraph [3, 11] (pp. 6–7) | SKIMMED | Background only, never used. Sources paywalled (not fetched). |
| Lemma 2.4 (p. 7) | VERIFIED LINE BY LINE | Divisibility is used but not needed (Obj. 1). |
| §2.2: invariant mean on F/ℤ, (2.3), I(φ\|_F)=∫φ, weak integral and ‖I(V)‖ ≤ I(‖V‖) (pp. 7–8) | VERIFIED LINE BY LINE | Used only as a positive translation-invariant functional. No limit is ever taken along a "sequence" defined by the mean. |
| Lemma 2.5 (p. 8) | VERIFIED LINE BY LINE | Bochner on ℝ after continuous extension, pushforward to F̂_disc, Fourier uniqueness by Stone–Weierstrass, ν(L_a)=0, then strong continuity of V_φ. |
| Lemma 2.6 (p. 9) | VERIFIED LINE BY LINE | |difference| ≤ \|s\|, strict convexity, coercivity bound (2p−1)\|s\|−p(R+√(1+R²)), Borel selection, both equivariances. Translation identity also checked numerically, with a failing control. |
| §2.4 disintegration paragraph (p. 9) | VERIFIED | Tao [26] Thm 4 / Remark 5 match. |
| Tower definition, (2.6) (p. 10) | VERIFIED | |
| Lemma 2.7 (pp. 10–14) | VERIFIED LINE BY LINE | Universal transfinite induction; base = Lemma 2.4; constant mass a via ergodicity; m cosets; Lemma 2.6 centres; factor Z, map b, uniform β_y; phase encoding; (2.7); (2.8); return to an earlier factor (successor and limit cases); induction hypothesis in Z; p(a) ≥ 0 (2.10); choice of t via I; (2.11); x_j = k_j + k'_j; bins, J, Chebyshev, q(y), (2.12); collision count; final contradiction. All constants rechecked exactly. Parameter order checked: m → ρ → (N,c) → s → τ → γ → (H_r,q,B,W) → L → M → t → x_j, k_j → w → J. Nothing is chosen before what it depends on. |
| Lemma 3.1 (pp. 14–16) | VERIFIED LINE BY LINE | Kernel centring, Hilbert–Schmidt bound, rank constant by ergodicity of Y, (3.1), strict extension, (2.6) for Y′→Y with Y-measurable coefficients bounded uniformly in k, termination by separability. The measurability paragraph is compressed but sufficient. |
| §3.2 every-Følner mean ergodic theorem (p. 16) | VERIFIED | |
| Lemma 3.2 (pp. 16–18) | VERIFIED LINE BY LINE | Pair criterion (3.3)/(3.4) on X; transfer to ℛ over Y; van der Corput induction (3.5)–(3.8); expansion (3.9). |
| §3.3 setup (3.10)–(3.11), radiality (p. 18) | VERIFIED | |
| Lemma 3.3 (pp. 18–19) | VERIFIED LINE BY LINE + exact sympy check | Both identities of (3.14), the factorisation, u−u⁻¹ = 2i Im u, and ru + rū = 2r Re u all hold. Controls fail as they should. |
| Lemma 3.4 (pp. 19–20) | VERIFIED LINE BY LINE + exact example | Series u(ha) = 1+2iha−2h²a²+…; ℚ-spans of squares; avoiding finitely many proper subspaces. |
| Lemma 3.5 (p. 20) | VERIFIED LINE BY LINE + grid test on the maximal admissible w | |
| Proof of Thm 2.3 (pp. 21–22): syndeticity (3.16), selections, (3.17), (3.18), (3.19), m ≥ e^{−4M₀H} on F∩(0,2rc₀), contradiction with (2.4), Fourier uniqueness, ergodic decomposition | VERIFIED LINE BY LINE | |

## 2. Test (A) — Payne's rational graph

### 2.1 The exact step
Replace F by ℚ, E by ℚ(i), and K by K_ℚ = {u ∈ ℚ(i) : |u| = 1}. Then the following parts still go through verbatim (modulo trivial edits):
- Lemma 2.4. The divisibility is unnecessary (Obj. 1).
- Lemmas 2.5 and 2.6.
- Lemma 2.7 up to and including the choice of t ∈ ℚ and (2.11).
- Lemma 3.1.
- Lemma 3.4. The ℚ(i), d₀=2 version holds; I checked it exactly (script 2).
- Lemma 3.5, which is pure arithmetic on nonnegative reals.

The first step that fails is p. 13, proof of Lemma 2.7, paragraph "A common coefficient bin on a good fiber", quoted from the PDF:

> "Each |x_j| < 1 is a sum of two elements of K. One explicit choice is k_j = x_j/2 + i√(1 − x_j²/4), k'_j = x_j/2 − i√(1 − x_j²/4).
> The square roots belong to F, and x_j = k_j + k'_j."

This sentence uses the fact that F is real closed: positive elements have square roots in F. Over ℚ the step is not merely unproved, it is false:
- For real x ≠ 0, the equation x = k + k' with |k| = |k'| = 1 forces Re k = x/2 and (Im k)² = 1 − x²/4 (because |x−k|² = 1 gives 2Re(x k̄) = x²).
  - Of the 1,101 reduced rationals in (0,1) with denominator ≤ 60, exactly 5 are sums of two rational unit vectors. Examples that fail: 1/2, 1/3, 1/5, 2/3, 3/4.
  - For every t = n/d with d < 400, at most M = 1 consecutive multiples jt are decomposable. The proof needs 0.9M/L > 10m².
- Worse, no decomposition of any length exists. Every rational unit vector is (a/c, b/c) with every prime factor of c ≡ 1 mod 4 (all 1,632 primitive triples with m < 90 checked; this is the classical fact). Hence K_ℚ ⊂ ℤ[i][1/p : p ≡ 1 mod 4]. Bezout gives the reverse inclusion, so ℤ[K_ℚ] = ℤ[i][1/p : p≡1 (4)]. No integer combination of rational unit vectors has 2 or 3 in its denominator, so x = 1/3 is not a ℤ-combination of elements of K_ℚ at all.

Over E = F(i) the opposite holds. Every real algebraic a ∈ [−2, 2] equals u + ū with u = a/2 + i√(1−a²/4) ∈ K, so ℤ[K] = E. This is the property the proof actually consumes: E has no proper nonzero K-invariant subgroup. The paper never states it.

Two further uses of real-closedness occur in my scope. They are not reached in the rational case, because the argument has already failed at p. 13:
- p. 18, "Equal nonzero moduli in E differ by an element of K. Thus m is radial; its radii lie in F_{≥0}." For example |1+i| = √2 ∉ ℚ.
- p. 19, "First take A, B > 0 and put L = √(AB) ∈ F". For example A=1, B=2 gives L ∉ ℚ.
- p. 21, "Every t ∈ F ∩ [−1, 1] is the real part of an element of K, namely t + i√(1−t²)". For example t = 1/2 fails over ℚ.

Divisibility of K (stressed in Def. 2.1) is used non-trivially only in two places:
- p. 16: "the representation u ↦ U_{u^d} … has the same invariant vectors as U, because the power map u ↦ u^d is onto".
- Lemma 3.3: the maps u ↦ u² and u ↦ u⁻². Over ℚ, K_ℚ^d has infinite index in K_ℚ.

### 2.2 The rational analogues of Theorem 2.3 and Lemma 2.7 are false: explicit counterexample ν₃
- **Construction.** 3 is inert in ℤ[i], so |u|₃ = 1 for every u ∈ K_ℚ: the rational rotations act isometrically on ℚ₃(i). Let R = ℤ₍₃₎[i]. It is K_ℚ-invariant, and R^⊥ ⊂ D_ℚ = (ℚ(i)_disc)^ is the compact group dual to ℚ(i)/R ≅ ℚ₃(i)/ℤ₃[i], i.e. R^⊥ ≅ ℤ₃[i]. Under the trace pairing, K_ℚ acts on it by multiplication. Let G₃ be the closure of the K_ℚ-orbit of 1, an infinite compact subgroup of the norm-one units. Script 3 shows the image of K_ℚ mod 3ⁿ growing as 4, 12, 36, 104, 304 for a finite sample; the full norm-one counts are 4·3^{n−1}. Let ν₃ be Haar measure on G₃, viewed as a measure on D_ℚ.
- **ν₃ is K_ℚ-invariant and ergodic.** It is a minimal isometric rotation, hence uniquely ergodic.
- **ν₃ is wild.** A continuous character trivial on the dense set R is trivial, so C ∩ R^⊥ = {0}, and 0 ∉ G₃.
- **ν₃ is not Haar.** Its Fourier coefficient at 1 is f(1) = 1, because 1 ∈ R.

So the rational Theorem 2.3 is false. ν₃ is also a compact (isometric) system, so the tower Y₀ → Y₁ = X satisfies (2.6), and at Y₁ the conditional difference law is δ₀ ∈ C. So the rational Lemma 2.7 is false at its first successor stage.

Tracing the proof of Lemma 2.7 on ν₃ (m=1, W trivial):
- p(a) = |f(a)|² = 1 for every a ∈ R.
- Hence the t produced by Lemma 2.5 must have 3 in its denominator.
- Hence x_j = jt ∉ R ⊇ ℤ[K_ℚ], so x_j is not a sum of elements of K_ℚ.

The proof breaks at exactly the quoted sentence and nowhere earlier.

### 2.3 Why the rational graph needs exactly this exclusion
Payne's 2-colouring of the rational-unit graph is a 2-adic object. Colour ℤ₍₂₎² by (x+y) mod 2. Every rational unit step (a/c, b/c) has (a+b)/c a 2-adic unit, so the colour flips on every edge (checked on 1,260 rational unit vectors, with a failing control). Colour the other cosets of ℤ₍₂₎² independently.

The averaged law of such a colouring has its label spectral measures on the 2-adic part of D_ℚ, where K_ℚ acts isometrically: a wild, non-Haar law of the ν₃ type. Theorem 2.3 says no such law exists over F(i), and p. 13 is the step that makes it true there.

My own (unchecked-in-literature) gloss on why: complex conjugation lies in no p-adic decomposition group, because Gal(ℚ̄_p/ℚ_p) is torsion-free (Artin–Schreier). So for every finite place v of ℚ̄ some u ∈ K has |u|_v ≠ 1, whereas K_ℚ is bounded at 2 and at every p ≡ 3 mod 4.

### 2.4 What the method proves for the rational graph
Nothing. Its central statement (Thm 2.3) is false there. The paper's p. 1 caveat ("measurable and unrestricted colorings cannot be identified merely because their distance constraints look the same") is therefore answered by the paper's own proof. The paper just never says so (Obj. 2).

### 2.5 Lean corroboration (read as text, not run)
- `OAI/Analysis/PlaneSpectrum/ConditionalSpectrum.lean` l. 116: `theorem real_algebraic_sum_two_rotations (x : F) (hx : |(x : ℝ)| < 2) : ∃ u v : K, ofF x = kCoeff u + kCoeff v`. Its proof builds `s := Real.sqrt (1-r^2)` and proves `IsAlgebraic ℚ s`. This is the p. 13 step.
- `RadialEnergy.lean` l. 9: `lemma equal_moduli_quadratic (A B L : ℝ) (hL : L^2 = A*B) (u : Circle)`. This is (3.14).

## 3. The ergodic-decomposition question
Ergodicity is assumed in Lemma 2.7 (X ergodic), Lemma 3.1, Lemma 3.2 and §3.3 ("Fix an ergodic wild K-invariant probability µ on D"). It is supplied wherever these lemmas are used:
- Inside Lemma 2.7, the induction hypothesis is applied to Z, "a standard ergodic factor" (p. 11). A factor of an ergodic system is ergodic.
- §3.3 applies Lemmas 3.1 and 2.7 to (D, µ) with µ ergodic.
- Lemmas 2.4 and 2.5 need only invariance and wildness. Lemma 2.5 is applied to the conditional difference laws, which are invariant and wild but not necessarily ergodic. That is fine.

The reduction from a general wild ν to ergodic components is explicit, p. 22, last paragraph of the proof of Thm 2.3:

> "Finally, an arbitrary wild invariant probability has an ergodic decomposition for the countable group K on the standard compact
> space D. Since C is invariant Borel and has measure zero, almost every ergodic component also gives C measure zero. The ergodic
> case just proved makes each such component Haar probability. Their integral is therefore Haar probability as well."

Wildness survives the decomposition: ν(C) = ∫ν_ω(C) dP(ω) = 0 with ν_ω(C) ≥ 0, and C is Borel (p. 6). There is no hole. The Lean mirrors this. `Ergodicity.lean` l. 335, `wild_fourier`: "The arbitrary invariant wild case, obtained from actual conditional ergodic fibers". It uses `InvariantDecomposition.code`, `fiber_ergodic` and `ConditionalFiber.ae_fiber_of_ae` for the C-null fibres, then applies `ergodic_wild_fourier`. The paper gives no citation for the ergodic decomposition (Obj. 3).

## 4. Objections (all non-fatal)
1. **Lemma 2.4, p. 7 — COSMETIC (exposition).** "The action on this finite orbit gives a finite image of the divisible abelian group K. Such an image is trivial: a finite abelian group cannot be divisible unless it is trivial."
   - Correct, but divisibility is not needed. The stabilizer of the coset has finite index in the infinite group K, so it contains some u ≠ 1, and "(u − 1)d ∈ C … d ∈ C" follows.
   - This matters for reading test (A): divisibility is not what separates F(i) from ℚ(i) here.
   - Fix: replace by "pick u ≠ 1 in the finite-index stabilizer".
2. **The paper never says which step uses the arithmetic of E — COSMETIC (exposition gap, not a proof gap).**
   - p. 1 raises Payne's graph as a warning, and p. 6 emphasises "Thus K is divisible". The decisive property is that F is real closed, so ℤ[K] = E. It is used on p. 13 ("The square roots belong to F"), p. 18 (radii in F), p. 19 (L = √(AB) ∈ F) and p. 21 (t + i√(1−t²)).
   - A reader checking the transfer against Payne has to find this alone.
   - Fix: one sentence after Theorem 2.3 noting that the rational analogue fails (ν₃ above) and naming p. 13.
3. **p. 22, ergodic decomposition — COSMETIC.** No reference is given for the ergodic decomposition of a countable-group action on a standard Borel space (e.g. Varadarajan 1963). The statement is standard and correctly applied. The Lean constructs it.
4. **p. 10, "We use transfinite induction in its universal form: at each ordinal the assertion ranges over all ambient ergodic standard systems…" — COSMETIC.** This is legitimate: induction on α of a statement that quantifies over all systems. The induction step (p. 12) uses it only at the ordinal of W, which is strictly smaller. The statement of Lemma 2.7 itself says nothing about the induction being universal; the proof supplies it.
5. **p. 10, "None is C almost surely, because the original marginal law gives C measure zero." — COSMETIC.** True (∫κ_y(C) = ν(C) = 0), but never used afterwards.
6. **Lemma 3.2 statement vs (3.5), pp. 16–18 — COSMETIC.**
   - (3.2) allows an exponent 0. (3.5) is proved only for nonzero exponents. The final paragraph bridges this by shifting all exponents by a common integer inside the scalar integral (3.9). That is correct.
   - The shift is needed because Lemma 3.3 uses exponents (0,2) and (0,1,2).
7. **Lemma 3.1 measurability paragraph, p. 15 — not an objection, a note.**
   - It is compressed: dense countable family, bounded polynomials → 1_{(δ,∞)} via spectral calculus, a.e.-fibre subsequence, then first-available independent sections and Gram–Schmidt.
   - I accept it. Q_y has finite rank d and is applied to a family dense in each fibre, so the projected family spans range Q_y on a.e. fibre, and rank tests are measurable.

## 5. Citation table (scope §2–3)
| Cited | Claimed | Source says | Verdict |
|---|---|---|---|
| [1] Bekka–de la Harpe–Valette, Thm G.2.1 (p. 7) | Invariant mean on the discrete abelian group F/ℤ exists | "Theorem G.2.1 (Markov-Kakutani) Every abelian topological group G is amenable." Amenable = invariant mean on UCB(G) (G.1, Thm G.1.7); for a discrete G, UCB = ℓ^∞ | MATCH (2007 manuscript, the paper's stated version, fetched from the cited ncatlab URL) |
| [1] Thm D.2.2 (p. 8) | Bochner on ℝ | "Theorem D.2.2 (Bochner) Let ϕ be a continuous function of positive type on Ĝ. There exists a finite positive Borel measure µ on G such that µ̂ = ϕ." | MATCH |
| [26] Tao 254A lecture 9, Thm 4 + Remark 5 (p. 9) | Disintegration kernel exists, a.e. unique, for standard spaces | "Theorem 4 (Disintegration theorem) … there exists a probability kernel … this probability kernel is unique up to -almost everywhere equivalence"; Remark 5: regular spaces = standard Borel | MATCH |
| [10] Furstenberg 1977, Lemmas 6.6, 7.2 (p. 14) | Invariant HS kernels → finite-rank modules; bounded bases | — | COULD NOT FETCH (Springer paywall). Not load-bearing: the paper re-proves what it uses (Lemma 3.1, verified). |
| [3] Crum 1956; [11] Gneiting–Sasvári 1999 (pp. 6–7) | Measurable radial positive-definite on ℝ² = continuous + c·1_{0} | — | COULD NOT FETCH (paywalled). Background only, not used. |
| [16, 17] Jamneshan; [32, 33] Zimmer; [9] Følner; [29] von Neumann | Context/history | — | Not fetched; not load-bearing |

Saved copies: /tmp/oaimath/158/world/rigidity_src/{bhv.pdf, bhv.txt, tao254a9.html, furst77_paywall.html}.

## 6. Finite checks (scripts verbatim, outputs, failing controls)
All are run with `python3 <script>` from /tmp/oaimath/158/seats/rigidity_checks/. Each takes under 10 s and uses little memory.
Summary:
- **Script 1 (Lemma 3.3).** Both identities of (3.14), the factorisation, u − u⁻¹ = 2i Im u, and ru + rū = 2r Re u hold symbolically for u = (1+it)/(1−it) and for u = e^{iθ}, and on an exact algebraic instance (A=2, B=3, u=(1+i√2)/√3: all three sides equal 17). Controls that FAIL: L→2L, L→(A+B)/2, u→2u.
- **Script 2 (Lemmas 3.4, 3.5).** Lemma 3.4 exactly over ℚ(√2, i) (9 elements, all 126 4-subsets ℚ-bases), with a failing control (adding −S[0]). The rational analogue (ℚ(i), d₀=2) also holds. Lemma 3.5 is tested on the maximal w satisfying w(0)=0, w(p_j) ≤ 1 and (3.12) on a grid. All 596 cases satisfy w(z) ≤ 4M (max ratio 2.0). The failing control: the stronger bound w(z) ≤ M fails in 109 cases.
- **Script 3 (test A).** Covers the p. 13 decomposition over ℚ, ℤ[K_ℚ], the ν₃ counterexample data, Payne's 2-adic colouring (with a failing control), and the other real-closedness uses.
- **Script 4.** Exact arithmetic of every constant in Lemma 2.7. Numeric check of Lemma 2.6's translation identity, with one far atom so there is no moment assumption; error 2e-11, and the wrong-sign control has error 1.38.


### check_lemma33.py
```python
# Lemma 3.3 (p.18-19): exact verification of the two unit-direction identities and the
# auxiliary algebraic facts used in Lemma 2.7 (p.13) and Sec 3.5 (p.21). With FAILING controls.
import sympy as sp
A,B,t,x,r,th = sp.symbols('A B t x r theta', positive=True)
I = sp.I
def absq(z):  # |z|^2 for z built from real symbols
    z = sp.expand(z); return sp.simplify(sp.expand(z*sp.conjugate(z)))
# u on the unit circle: rational parametrization u(t)=(1+it)/(1-it) (all of S^1 except -1), and u = e^{i theta}
u_par = (1+I*t)/(1-I*t)
u_tri = sp.cos(th)+I*sp.sin(th)
L = sp.sqrt(A*B)
ok = True
for name,u in [('u(t)=(1+it)/(1-it)',u_par),('u=e^{i theta}',u_tri)]:
    imu = sp.im(sp.expand_complex(u))
    rhs = (A-B)**2 + 4*A*B*imu**2
    e1 = sp.simplify(sp.expand_complex(absq(A-B*u**2) - rhs))
    e2 = sp.simplify(sp.expand_complex(absq(-L+(A-B)*u+L*u**2) - rhs))
    e3 = sp.simplify(sp.expand_complex((-L+(A-B)*u+L*u**2) - u*((A-B)+L*(u-1/u))))
    e4 = sp.simplify(sp.expand_complex((u-1/u) - 2*I*imu))
    e5 = sp.simplify(sp.expand_complex(r*u + r*sp.conjugate(u) - 2*r*sp.re(sp.expand_complex(u))))
    print(name, '(3.14) first =', e1, '| second =', e2, '| factorization =', e3, '| u-1/u-2iIm u =', e4, '| ru+r ubar-2rRe u =', e5)
    ok &= all(e==0 for e in (e1,e2,e3,e4,e5))
    # FAILING controls: replace L by 2L, and by (A+B)/2 ; drop |u|=1 (u -> 2u)
    c1 = sp.simplify(sp.expand_complex(absq(-2*L+(A-B)*u+2*L*u**2) - rhs))
    c2 = sp.simplify(sp.expand_complex(absq(-(A+B)/2+(A-B)*u+(A+B)/2*u**2) - rhs))
    c3 = sp.simplify(sp.expand_complex(absq(A-B*(2*u)**2) - ((A-B)**2 + 4*A*B*sp.im(sp.expand_complex(2*u))**2)))
    print('   controls (must be NONZERO): L->2L:', sp.factor(c1), '| L->(A+B)/2:', sp.factor(c2), '| u->2u:', sp.factor(c3))
    ok &= all(c!=0 for c in (c1,c2,c3))
# exact numeric instance with algebraic numbers (F = real algebraic numbers): A=2, B=3, u=(1+i*sqrt(2))/sqrt(3)
uu = (1+I*sp.sqrt(2))/sp.sqrt(3)
assert sp.simplify(uu*sp.conjugate(uu)) == 1
Ln = sp.sqrt(6)
lhs = sp.nsimplify(sp.simplify(sp.expand(sp.Abs(2-3*uu**2)**2)))
mid = (2-3)**2 + 4*6*sp.im(uu)**2
rhs2 = sp.simplify(sp.expand(sp.Abs(-Ln+(2-3)*uu+Ln*uu**2)**2))
print('exact instance A=2,B=3,u=(1+i sqrt2)/sqrt3: |A-Bu^2|^2 =', sp.simplify(lhs), ' (A-B)^2+4AB Im^2 =', sp.simplify(mid), ' |-L+(A-B)u+Lu^2|^2 =', sp.simplify(rhs2))
ok &= sp.simplify(lhs-mid)==0 and sp.simplify(rhs2-mid)==0
# p.13: every real x with |x|<2 is k+k' with k,k' in K: k = x/2 + i sqrt(1-x^2/4)
k = x/2 + I*sp.sqrt(1-x**2/4); kp = x/2 - I*sp.sqrt(1-x**2/4)
print('p.13 decomposition: |k|^2-1 =', sp.simplify(sp.expand_complex(k*sp.conjugate(k)).subs(x,sp.Rational(1,3))-1),
      '(at x=1/3), k+k\'-x =', sp.simplify(k+kp-x), ', k(1/3)=', k.subs(x,sp.Rational(1,3)))
# p.19 Lemma 3.4: formal expansion u(ha) = 1 + 2iha - 2h^2a^2 + ...
h,a = sp.symbols('h a')
ser = sp.series((1+I*h*a)/(1-I*h*a), h, 0, 4).removeO()
print('Lemma 3.4 series u(ha) =', sp.expand(ser))
ok &= sp.expand(ser - (1+2*I*h*a-2*h**2*a**2-2*I*h**3*a**3))==0
print('Lemma 3.4: 4a = (a+1)^2-(a-1)^2 :', sp.expand((a+1)**2-(a-1)**2))
print('ALL IDENTITIES OK' if ok else 'FAILURE')
```
Output:
```
u(t)=(1+it)/(1-it) (3.14) first = 0 | second = 0 | factorization = 0 | u-1/u-2iIm u = 0 | ru+r ubar-2rRe u = 0
   controls (must be NONZERO): L->2L: 48*A*B*t**2/(t**2 + 1)**2 | L->(A+B)/2: 4*t**2*(A - B)**2/(t**2 + 1)**2 | u->2u: -3*B*(2*A - 5*B)
u=e^{i theta} (3.14) first = 0 | second = 0 | factorization = 0 | u-1/u-2iIm u = 0 | ru+r ubar-2rRe u = 0
   controls (must be NONZERO): L->2L: 12*A*B*sin(theta)**2 | L->(A+B)/2: (A - B)**2*sin(theta)**2 | u->2u: -3*B*(2*A - 5*B)
exact instance A=2,B=3,u=(1+i sqrt2)/sqrt3: |A-Bu^2|^2 = 17  (A-B)^2+4AB Im^2 = 17  |-L+(A-B)u+Lu^2|^2 = 17
p.13 decomposition: |k|^2-1 = 0 (at x=1/3), k+k'-x = 0 , k(1/3)= 1/6 + sqrt(35)*I/6
Lemma 3.4 series u(ha) = -2*I*a**3*h**3 - 2*a**2*h**2 + 2*I*a*h + 1
Lemma 3.4: 4a = (a+1)^2-(a-1)^2 : 4*a
ALL IDENTITIES OK
```

### check_lemma34_35.py
```python
# Lemma 3.4 (general position, p.19-20) exact over N = Q(sqrt2)(i) and over N = Q(i) (rational analogue);
# Lemma 3.5 (addition under a cap, p.20) tested on the MAXIMAL function satisfying (3.12) on a grid.
from fractions import Fraction as Fr
from itertools import combinations
import random, numpy as np
random.seed(158)
# ---- arithmetic in Q(sqrt2)(i): element = (a,b,c,d) meaning a+b*s + i(c+d*s), s=sqrt2
def r2mul(x,y): return (x[0]*y[0]+2*x[1]*y[1], x[0]*y[1]+x[1]*y[0])
def r2inv(x):
    n = x[0]*x[0]-2*x[1]*x[1]; return (x[0]/n, -x[1]/n)
def cmul(z,w):
    zr,zi=(z[0],z[1]),(z[2],z[3]); wr,wi=(w[0],w[1]),(w[2],w[3])
    rr = tuple(p-q for p,q in zip(r2mul(zr,wr),r2mul(zi,wi))); ii = tuple(p+q for p,q in zip(r2mul(zr,wi),r2mul(zi,wr)))
    return (rr[0],rr[1],ii[0],ii[1])
def conj(z): return (z[0],z[1],-z[2],-z[3])
def u_of_t(t):  # t=(p,q) in Q(sqrt2): u=(1+it)^2/(1+t^2)
    one_it = (Fr(1),Fr(0),t[0],t[1]); num = cmul(one_it,one_it)
    den = r2inv((Fr(1)+r2mul(t,t)[0], r2mul(t,t)[1]))
    return cmul(num,(den[0],den[1],Fr(0),Fr(0)))
def rank(vecs):
    M=[list(v) for v in vecs]; rk=0; ncol=len(M[0]) if M else 0
    for c in range(ncol):
        piv=next((i for i in range(rk,len(M)) if M[i][c]!=0),None)
        if piv is None: continue
        M[rk],M[piv]=M[piv],M[rk]
        for i in range(len(M)):
            if i!=rk and M[i][c]!=0:
                f=M[i][c]/M[rk][c]; M[i]=[a-f*b for a,b in zip(M[i],M[rk])]
        rk+=1
    return rk
def build_S(size, d0, gen):
    S=[]
    while len(S)<size:
        u=gen()
        if all(rank(list(sub)+[u])==len(sub)+1 for k in range(0,d0) for sub in combinations(S,k)):
            S.append(u)
    return S
one=(Fr(1),Fr(0),Fr(0),Fr(0))
gen=lambda: u_of_t((Fr(random.randint(-9,9),random.randint(1,9)),Fr(random.randint(-9,9),random.randint(1,9))))
S=build_S(9,4,gen)
assert all(cmul(u,conj(u))==one for u in S), 'not unit modulus'
allind = all(rank(sub)==4 for sub in combinations(S,4))
print('Lemma 3.4, N=Q(sqrt2,i), d0=4: |S|=%d, all elements in K (u*ubar=1): True, every 4-subset a Q-basis: %s (%d subsets)'%(len(S),allind,len(list(combinations(S,4)))))
# FAILING control: replace one element by -S[0] (still in K and N): some 4-subset must be dependent
Sc=S[:-1]+[tuple(-c for c in S[0])]
print('  control (S with -S[0] added): every 4-subset a Q-basis:', all(rank(sub)==4 for sub in combinations(Sc,4)), '(expected False)')
# rational analogue: N0=Q, N=Q(i), d0=2
genQ=lambda: u_of_t((Fr(random.randint(-30,30),random.randint(1,30)),Fr(0)))
SQ=build_S(12,2,genQ)
print('Lemma 3.4 rational analogue N=Q(i), d0=2: |S|=%d, every 2-subset a Q-basis: %s  -> Lemma 3.4 itself does NOT separate F(i) from Q(i)'%(len(SQ),all(rank(sub)==2 for sub in combinations(SQ,2))))
# ---- Lemma 3.5 on the maximal w satisfying w(0)=0, w(p_j)<=H=1, (3.12) for args in [0,P]
def maximal_w(P, inputs):
    INF=10**9; w=np.full(P+1,INF,dtype=np.int64); w[0]=0
    for pj in inputs: w[pj]=min(w[pj],1)
    idx_all=np.arange(P+1)
    while True:
        old=w.copy()
        for A in range(P+1):
            if w[A]>=INF: continue
            vals=w[A]+w; idx=np.abs(A-idx_all); m=vals<INF
            np.minimum.at(w, idx[m], vals[m])
        if np.array_equal(old,w): return w
worst=0.0; worst_case=None; tested=0; ctrl_fail=0
for trial in range(6):
    P=600; q=random.choice([2,3]); inputs=sorted(set([P]+[random.randint(1,P-1) for _ in range(q-1)]))
    w=maximal_w(P,inputs)
    for M in range(1,7):
        # all integer vectors a with sum|a|<=M
        vecs=[()]
        for _ in inputs: vecs=[v+(a,) for v in vecs for a in range(-M,M+1)]
        for a in vecs:
            if sum(map(abs,a))>M or sum(map(abs,a))==0: continue
            z=sum(ai*pi for ai,pi in zip(a,inputs))
            if 0<=z<P:
                tested+=1; ratio=w[z]/(M*1.0)
                assert w[z]<=4*M, ('LEMMA 3.5 VIOLATED',inputs,a,z,w[z])
                if ratio>worst: worst=ratio; worst_case=(inputs,a,z,int(w[z]),M)
                if w[z]>1*M: ctrl_fail+=1
print('Lemma 3.5: %d (inputs, combination) cases, all satisfy w(z)<=4MH; max w(z)/(MH)=%.3f at %s'%(tested,worst,worst_case))
print('  control: the stronger claim w(z)<=1*MH FAILS in %d cases (so the check can fail; constant >1 is needed)'%ctrl_fail)
```
Output:
```
Lemma 3.4, N=Q(sqrt2,i), d0=4: |S|=9, all elements in K (u*ubar=1): True, every 4-subset a Q-basis: True (126 subsets)
  control (S with -S[0] added): every 4-subset a Q-basis: False (expected False)
Lemma 3.4 rational analogue N=Q(i), d0=2: |S|=12, every 2-subset a Q-basis: True  -> Lemma 3.4 itself does NOT separate F(i) from Q(i)
Lemma 3.5: 596 (inputs, combination) cases, all satisfy w(z)<=4MH; max w(z)/(MH)=2.000 at ([166, 193, 600], (0, 2, 0), 386, 4, 2)
  control: the stronger claim w(z)<=1*MH FAILS in 109 cases (so the check can fail; constant >1 is needed)
```

### check_testA_rational.py
```python
# Test (A): run the arithmetic steps of Sec 2-3 with E=Q(i), K_Q={u in Q(i): |u|=1}.
from fractions import Fraction as Fr
from math import isqrt, gcd
from itertools import product
def is_sq(q):
    q=Fr(q)
    if q<0: return False
    n,d=q.numerator,q.denominator; return isqrt(n)**2==n and isqrt(d)**2==d
def prime_factors(n):
    f=set(); p=2
    while p*p<=n:
        while n%p==0: f.add(p); n//=p
        p+=1
    if n>1: f.add(n)
    return f
# (1) p.13 step: "Each |x_j|<1 is a sum of two elements of K."  For real x != 0, k+k'=x with |k|=|k'|=1 forces
#     Re k = x/2 and (Im k)^2 = 1-x^2/4  (from |x-k|^2=1 => 2Re(x k-bar)=x^2).  Over Q this needs 1-x^2/4 to be a rational square.
def sum_of_two_rational_units(x):
    x=Fr(x); return x==0 or is_sq(1-x*x/4)
tests=[Fr(1,2),Fr(1,3),Fr(1,5),Fr(2,3),Fr(3,4),Fr(1,7),Fr(6,5),Fr(8,5),Fr(24,25)]
print('(1) x in Q, is x = k+k\' with k,k\' in K_Q ?', {str(x):sum_of_two_rational_units(x) for x in tests})
H=60; cnt=tot=0
for d in range(1,H+1):
    for n in range(1,d):
        if gcd(n,d)==1:
            tot+=1; cnt+=sum_of_two_rational_units(Fr(n,d))
print('    among the %d reduced rationals in (0,1) with denominator <= %d, only %d are sums of two rational unit vectors'%(tot,H,cnt))
# the proof needs x_j = j t for j=1..M ALL decomposable, t chosen by an invariant mean (no arithmetic control).
best=0
for d in range(1,400):
    for n in range(1,d):
        if gcd(n,d)!=1: continue
        t=Fr(n,d); M=0
        while abs((M+1)*t)<1 and sum_of_two_rational_units((M+1)*t): M+=1
        best=max(best,M)
print('    largest M with jt decomposable for all j=1..M (t=n/d, d<400, |Mt|<1):',best,' (the proof needs M >= 2 with 0.9M/L > 10m^2, i.e. M huge)')
# (2) Stronger: Z[K_Q] avoids 1/3 and 1/2: every rational unit vector (a/c,b/c) (primitive triple) has c with prime factors = 1 mod 4.
bad=0; seen=0
for m in range(1,90):
    for n in range(1,m):
        if (m-n)%2==1 and gcd(m,n)==1:
            a,b,c=m*m-n*n,2*m*n,m*m+n*n; seen+=1
            if any(p%4!=1 for p in prime_factors(c)): bad+=1
print('(2) %d primitive Pythagorean triples: hypotenuses with a prime factor not = 1 mod 4: %d'%(seen,bad))
print('    => K_Q subset Z[i][1/p : p=1 mod 4]; so EVERY integer combination of elements of K_Q has no 2 or 3 in its denominator;')
print('       x=1/3 or 1/2 is not a Z-combination of rational unit vectors of ANY length.')
# control: the algebraic field passes: x=1/3 = k+k' with k = 1/6 + i sqrt(35)/6 (in K, algebraic) -- see check_lemma33.py
# (3) 3-adic counterexample to the rational Theorem 2.3 / Lemma 2.7: K_Q acts ISOMETRICALLY on Q_3(i) (3 inert).
def v_p(q,p):
    q=Fr(q)
    if q==0: return 99
    n,d=q.numerator,q.denominator; v=0
    while n%p==0: n//=p; v+=1
    while d%p==0: d//=p; v-=1
    return v
units=[]
for m in range(1,40):
    for n in range(-39,40):
        if n!=0 and gcd(m,abs(n))==1 and (m-n)%2==1:
            c=m*m+n*n; units.append((Fr(m*m-n*n,c),Fr(2*m*n,c)))
print('(3) sample |K_Q| =',len(units),'; min 3-adic valuation of coordinates:',min(min(v_p(x,3),v_p(y,3)) for x,y in units),
      '; min 2-adic:',min(min(v_p(x,2),v_p(y,2)) for x,y in units))
# image of K_Q in (Z/3^n)[i]^x grows with n => orbit closure G_3 in Z_3[i]^x is infinite => Haar(G_3) nonatomic.
for n in range(1,6):
    mod=3**n; img=set()
    for x,y in units:
        inv=pow(x.denominator,-1,mod)  # denominators prime to 3
        img.add(((x.numerator*inv)%mod,(y.numerator*pow(y.denominator,-1,mod))%mod))
    print('    |image of sample of K_Q in (Z/3^%d)[i]| = %d'%(n,len(img)))
print('    => nu_3 := Haar on G_3 = closure of K_Q.1 in Z_3[i]^x (embedded in D_Q as characters trivial on Z_(3)[i]) is K_Q-invariant,')
print('       ergodic (minimal isometric rotation), gives C measure 0 (C meets that compact subgroup only in 0, and 0 is not in G_3),')
print('       and has Fourier coefficient f(1)=1 (1 in Z_(3)[i]); it is NOT Haar on D_Q.  Rational Theorem 2.3 is FALSE.')
# (4) Payne's 2-colouring lives on the 2-adic isometric place: colour Z_(2)^2 by (x+y) mod 2; a rational unit step flips it.
flips=all(((x+y).numerator%2==1 and (x+y).denominator%2==1) for x,y in units)
print('(4) every sampled rational unit vector (x,y) has x+y a 2-adic UNIT (odd/odd):',flips,' => colour(x,y)=(x+y mod 2) flips on every rational unit step')
ctrl=(Fr(3,5),Fr(1,5)); print('    control: non-unit step (3/5,1/5): x+y = 4/5 odd/odd?',(ctrl[0]+ctrl[1]).numerator%2==1,'(expected False -> the test can fail)')
# (5) the other two real-closedness uses, rational analogues
print('(5) Lemma 3.3 needs L=sqrt(AB) in the base field: A=1,B=2 -> AB square in Q?',is_sq(Fr(2)),
      '; p.21 "every t in [-1,1] is Re of an element of K": t=1/2 -> 1-t^2 square in Q?',is_sq(Fr(3,4)))
print('    p.18 "radii lie in F_{>=0}": |1+i| = sqrt2 rational?',is_sq(Fr(2)))
```
Output:
```
(1) x in Q, is x = k+k' with k,k' in K_Q ? {'1/2': False, '1/3': False, '1/5': False, '2/3': False, '3/4': False, '1/7': False, '6/5': True, '8/5': True, '24/25': False}
    among the 1101 reduced rationals in (0,1) with denominator <= 60, only 5 are sums of two rational unit vectors
    largest M with jt decomposable for all j=1..M (t=n/d, d<400, |Mt|<1): 1  (the proof needs M >= 2 with 0.9M/L > 10m^2, i.e. M huge)
(2) 1632 primitive Pythagorean triples: hypotenuses with a prime factor not = 1 mod 4: 0
    => K_Q subset Z[i][1/p : p=1 mod 4]; so EVERY integer combination of elements of K_Q has no 2 or 3 in its denominator;
       x=1/3 or 1/2 is not a Z-combination of rational unit vectors of ANY length.
(3) sample |K_Q| = 1260 ; min 3-adic valuation of coordinates: 0 ; min 2-adic: 0
    |image of sample of K_Q in (Z/3^1)[i]| = 4
    |image of sample of K_Q in (Z/3^2)[i]| = 12
    |image of sample of K_Q in (Z/3^3)[i]| = 36
    |image of sample of K_Q in (Z/3^4)[i]| = 104
    |image of sample of K_Q in (Z/3^5)[i]| = 304
    => nu_3 := Haar on G_3 = closure of K_Q.1 in Z_3[i]^x (embedded in D_Q as characters trivial on Z_(3)[i]) is K_Q-invariant,
       ergodic (minimal isometric rotation), gives C measure 0 (C meets that compact subgroup only in 0, and 0 is not in G_3),
       and has Fourier coefficient f(1)=1 (1 in Z_(3)[i]); it is NOT Haar on D_Q.  Rational Theorem 2.3 is FALSE.
(4) every sampled rational unit vector (x,y) has x+y a 2-adic UNIT (odd/odd): True  => colour(x,y)=(x+y mod 2) flips on every rational unit step
    control: non-unit step (3/5,1/5): x+y = 4/5 odd/odd? False (expected False -> the test can fail)
(5) Lemma 3.3 needs L=sqrt(AB) in the base field: A=1,B=2 -> AB square in Q? False ; p.21 "every t in [-1,1] is Re of an element of K": t=1/2 -> 1-t^2 square in Q? False
    p.18 "radii lie in F_{>=0}": |1+i| = sqrt2 rational? False
```

### check_constants_l26.py
```python
# Arithmetic of the constants in the proof of Lemma 2.7 (pp.11-14) and a numeric check of Lemma 2.6 (p.9).
from fractions import Fraction as Fr
import random, math
ok=True
for m in range(1,50):
    m2=Fr(m*m)
    # (2.7) majorant budget: arc mass < 1/(16m^2), approx error 1/(64m^2) twice, nonconstant part < 1/(32m^2)
    budget = Fr(1,16)/m2 + Fr(1,64)/m2 + Fr(1,32)/m2 + Fr(1,64)/m2
    ok &= budget == Fr(1,8)/m2 and budget < Fr(1,4)/m2
    # final collision bounds: lower > (0.95^2-0.1)/m^2 > 1/(4m^2) ; uses |J| > 10 m^2
    ok &= (Fr(95,100)**2 - Fr(1,10))/m2 > Fr(1,4)/m2
# Markov: 2g^2/t^2 < 1e-4  =>  (2 g^2)/(0.1 t^2) = 20 g^2/t^2 < 1e-3
ok &= Fr(20,2)*Fr(1,10**4) <= Fr(1,1000)
# Chebyshev: tau = s/100, distance <= 3 tau, two encodings: 2*9 tau^2/s^2
ok &= 2*9*Fr(1,100)**2 == Fr(18,10**4) and 1-Fr(18,10**4) > Fr(95,100)
# good-fiber sets: P(W-good for 2.11) > 0.99 and P(>0.9M good indices) > 0.999 => intersection > 0.989 > 0
ok &= Fr(99,100)+Fr(999,1000)-1 > 0
print('Lemma 2.7 constant arithmetic OK' if ok else 'CONSTANT FAILURE')
# Lemma 2.6: J_lambda(s) = sum_t w_t (sqrt(1+|s-t|^2)-sqrt(1+|t|^2)); |difference| <= |s|; J_{lambda'}(s)=J(s+r)-J(r) for lambda' = law(t-r)
random.seed(26)
pts=[(random.gauss(0,3),random.gauss(0,3)) for _ in range(40)]+[(1e6,-2e6)]  # one far atom: no moment assumption
wts=[random.random() for _ in pts]; Z=sum(wts); wts=[w/Z for w in wts]
def J(s,P):
    return sum(w*(math.hypot(1,math.hypot(s[0]-t[0],s[1]-t[1]))-math.hypot(1,math.hypot(t[0],t[1]))) for w,t in zip(wts,P))
r=(0.7,-1.3); Pp=[(t[0]-r[0],t[1]-r[1]) for t in pts]
errmax=0; bndok=True
for _ in range(200):
    s=(random.uniform(-9,9),random.uniform(-9,9))
    errmax=max(errmax,abs(J(s,Pp)-(J((s[0]+r[0],s[1]+r[1]),pts)-J(r,pts))))
    for t in pts[:5]:
        bndok &= abs(math.hypot(1,math.hypot(s[0]-t[0],s[1]-t[1]))-math.hypot(1,math.hypot(t[0],t[1])))<=math.hypot(*s)+1e-9
print('Lemma 2.6 translation identity max error %.2e ; |integrand|<=|s| : %s'%(errmax,bndok))
# control (must FAIL): the identity with the wrong sign J(s-r)-J(-r)
ctrl=max(abs(J(s,Pp)-(J((s[0]-r[0],s[1]-r[1]),pts)-J((-r[0],-r[1]),pts))) for s in [(1,2),(3,-1),(-2,0.5)])
print('  control J(s-r)-J(-r): max error %.3f (expected clearly nonzero)'%ctrl)
```
Output:
```
Lemma 2.7 constant arithmetic OK
Lemma 2.6 translation identity max error 2.12e-11 ; |integrand|<=|s| : True
  control J(s-r)-J(-r): max error 1.382 (expected clearly nonzero)
```

## 7. Summary
§2–3 HOLD AS READ. Theorem 2.3 (wild ⇒ Haar) is proved correctly: Lemmas 2.4–2.7 and 3.1–3.5 were checked line by line, the two
unit-direction identities and all constants were checked exactly, and the ergodic reduction is explicit on p. 22 and mirrored in Lean.
Test (A): the transfer uses that F is real closed, i.e. ℤ[K] = E. The exact step is p. 13: "Each |x_j| < 1 is a sum of two elements of K … The
square roots belong to F". Over ℚ(i) this fails, and the rational Theorem 2.3 and Lemma 2.7 are false (ν₃ = Haar on the
3-adic orbit closure of K_ℚ). So the method proves nothing for Payne's graph, consistent with Payne. Objections: cosmetic/exposition
only (unneeded divisibility in Lemma 2.4; the paper never names the step that separates F(i) from ℚ(i); no citation for ergodic decomposition).
