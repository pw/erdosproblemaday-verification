# Referee report — scope `algebra`: §3 in full (PDF pp. 14–26)
Paper: /tmp/oaimath/166/paper.pdf (sha256 37f63553…bf). Read: §1.2–1.3 and §2 (pp. 2–13) for the architecture, then §3 (pp. 14–26) line by line in the text extraction, with PDF pp. 18–24 rendered to confirm every displayed formula ((3.5)–(3.17)). Downstream call sites of every §3 result were located by grep and form-checked (statement used = statement proved); the surrounding §4–6/App. A arguments are other referees' scope.

**Bottom line: §3 HOLDS AS READ.** I found no mathematical gap. Every statement in §3 is a finite, effective inequality whose constants depend only on the ambient dimension. None of them is asymptotic, uses a rate, or depends on N, M, δ, the sequence or a window. The engine inequality (3.7) is true as stated, with an explicit uniform constant, and I checked it on the three toys the brief names. The objections below are exposition and cosmetic issues, plus cross-scope flags. The one thing I could not check is the text of Fulton [14], a paywalled book (COULD NOT FETCH). The §3 steps that cite it are standard, and I verified them independently. The only Fulton-dependent statement I could not close is used in Appendix A, not in §3 (Objection 1).

---

## 1. Sources fetched (each in its own dir under /tmp/oaimath/166/refs/)

| id | what | version read |
|---|---|---|
| `chardin1989/chardin1989.pdf` | Chardin, Bull. SMF 117 (1989) 305–318 | Numdam scan of the published article |
| `chardin_philippon1999/RI.pdf` | Chardin–Philippon, “Régularité et interpolation”, JAG 8 (1999) 471–481 | author-hosted copy from Chardin's IMJ page, listed there as the JAG 1999 paper (webusers.imj-prg.fr/~marc.chardin/publications/textes/11.RI.pdf). Not on arXiv; publisher PDF not fetched. The erratum's internal references (Definition 1, Prop. 2, Cor. 2, Remark A) agree with this copy's numbering. |
| `chardin_philippon_erratum2002/Err.pdf` | Erratum, JAG 11 (2002) 599–600 | author-hosted (…/11.Err.pdf) |
| `stacks/*.html` | Tags 00OQ, 00NQ, 02JN, 062F, 0578 | live site, 2026-10-11 |
| `1811.07865v2`, `1906.05843v2`, `2608.14454v1` | Walsh [27], Walsh [28], TYZ [26] | current arXiv versions (v2, v2, v1, confirmed via the arXiv API today). These dirs had already been downloaded by another seat; I read them. |
| Fulton [14], Hartshorne [17] | books | **COULD NOT FETCH** (no free or author copy; two web searches) |

Scratch: `/tmp/oaimath/166/algebra_scratch/toys.py` (exact rank computations mod 1000003).

---

## 2. Objections

### Objection 1 — UNCLEAR (exposition). §3 preamble, p. 14: the multiplicity form of refined Bézout
> “More generally, the degrees, with local intersection multiplicities, of isolated components of an intersection are at most the Bézout product, even if the same equations have larger components elsewhere. One obtains this latter form by taking generic linear combinations locally at the isolated components, perturbing to proper intersections, and specializing: the isolated intersection multiplicities are positive and persist in the specialization, whereas intersections on other components can only add to the total.”

**Problem 1 — undefined quantities.** When the system has s > codim equations, “local intersection multiplicity” and “the Bézout product” are not defined: multiplicity of which c-element subsystem, and the product of which degrees? Generic linear combinations of equations of unequal degrees all have the maximal degree, so the product the sketch actually controls is L^c, not d₁⋯d_c.

**Problem 2 — the justification is a sketch.** “Perturb and specialize” is a dynamic-intersection heuristic, not a proof. The rigorous route is Fulton's positivity / refined Bézout ([14, Thm 12.2–12.3]), which I could not fetch.

**Effect on §3: none.** No §3 proof uses the version with multiplicities. Lemma 3.1, Lemma 3.9, Lemma 3.12(ii) and Cor. 3.14 use only:
- the multiplicity-free bound “Σ deg(components of a proper section) ≤ a·q”, which is classical. Walsh [27, Lemma 2.1] states it verbatim (quoted in the citation table);
- or, in Cor. 3.14, “local intersection number of a curve with a hyperplane ≤ deg C”, which is elementary.

**Where the multiplicity version is used.** Appendix A, `paper_plain.txt` l. 5163–5165 (“…affect their isolated Bézout bound [14, Theorem 12.3 and Example 12.3.1]… complete-intersection multiplicity equals the quotient length…”). The concentration referee should check that use.

**The statement is true** in the form needed there: for c hypersurfaces of degree ≤ L, Σ e_Z deg Z ≤ L^c over isolated components Z. Positivity of the distinguished-variety contributions in Pⁿ gives it.

**Fix:** state precisely “for c generic linear combinations of the equations, of degree ≤ L, Σ_Z e_Z deg Z ≤ L^c, e_Z = length of the local quotient” and cite Fulton Thm 12.3 with Example 12.3.1 instead of the sketch.

### Objection 2 — COSMETIC. §3.3, p. 17: attribution of the lower estimate to Chardin–Philippon
> “For components of a single equation system, the shifted lower estimate follows from the isolated-component bound of Chardin–Philippon [7, Corollary 3]”

- C–P's Corollaire 3 holds for ν > d₁+⋯+d_r − r (strict inequality).
- (3.6) is stated for D ≥ q.
- So the citation covers (3.6) except at D = q.

The paper's own proof gives D ≥ q correctly. At D = q it gives H ≥ a; for a complete intersection of n forms of degree L, at D = n(L−1), this is exactly tight. Nothing depends on the citation. **Fix:** none needed; optionally say “for D > q”.

### Objection 3 — COSMETIC. Symbol overloading in §3
Several letters are reused with different meanings, sometimes inside one lemma:
- **q:** Lemma 3.6's shift; Lemma 3.10's ⌊(n+1)E/r⌋; Lemma 3.11's minor size.
- **b:** the scaling integer in (3.8); the failing degree in Lemma 3.8; the forced degree in Lemma 3.9; the number of tᵢ in Lemma 3.10.
- **a:** total degree; also the inverted integer in Lemma 3.10.
- **c:** the number of variables in Lemmas 3.2, 3.3 and 3.5; also the constants c_n.
- **regular:** “regular local ring”, “regular sequence” and “regular equations” (= Jacobian rank n−k, Lemma 3.8). Castelnuovo–Mumford regularity, the subject of C–P [7], is never used by the paper.

Each use is locally defined and I found no place where the overloading causes an error. **Fix:** rename.

### Objection 4 — COSMETIC. Lemma 3.1, p. 15
> “Moreover, P is precisely the common zero set of a system of polynomials of degree at most 2M + 1.”

The equations (3.3) have degree ≤ 2(M−1)+1 = 2M−1. The stated bound is loose but true. The OAI Lean file `oai_lean/PolynomialIsolation.lean` proves `degree_isolationPolynomials : totalDegree ≤ 2*(distances P).card + 1`, i.e. 2M−1, and `isolation_zero_iff`, which is exactly the zero-set claim. No fix needed.

### Objection 5 — UNCLEAR (cross-scope flag, not a defect of §3). The hypothesis “D ≥ C_n L” of Lemmas 3.8 and 3.9 at their uses
Lemma 3.8 (“If D ≥ C_n L…”) and Lemma 3.9 (“If D ≥ C_n max{L, L′}…”) have a fixed dimensional constant C_n in the hypothesis. In my reconstruction C_n ≈ 2(n−k), enough to force D ≥ 2q.

They are applied at D/L = exp((b′−β−o(1))s) (l. 2530–2540), T₁/T₀ = exp((t₁−t₀)s) (l. 3116) and T₁/T₀ (l. 3838). Each application is legitimate only once that ratio exceeds the fixed C_n, i.e. for window widths s ≥ s₀(n, margin).

§3 is correct as stated. The §5–6 referees should confirm that s → ∞ (or a fixed margin) is in force at every application. A bounded-s regime would make the hypothesis fail rather than merely weaken the conclusion.

### Objection 6 — UNCLEAR (cross-scope flag for the `lean` seat)
The brief describes OpenAI's library as supplying “only the polynomial isolation interface”. The third-party repo's `lakefile.lean` instead has
`require OAI from git "https://github.com/openai/math" @ "adc7f1241b42e322a6451854ab7e4b4c146bf78a" / "lean"`.

It imports multiplicity modules from that library, e.g. `DistinctDistances/Foundations/ALocaldimAux.lean: import OAI.RingTheory.Multiplicity.LechHilbertSerre`, `…LechLengthLe`, and `OAIInterface/FiniteGradedQuotient.lean: import OAI.RingTheory.Multiplicity.LechBoundedEquiv`.

The paper's text never invokes Lech's inequality or the Hilbert–Serre theorem: `grep -i "lech\|serre"` on paper_plain.txt finds 0 hits.
- §3.5 (Lemma 3.10) is a self-contained Frobenius argument.
- §3.6 uses only the definition of Hilbert–Samuel multiplicity, blow-up intersection numbers, Artin–Rees and Nakayama.

So whatever the Lean development takes from those OAI modules is not something the paper cites. The `lean` seat should check what is proved there versus assumed.

No further objections. In particular I found none against Lemma 3.6, the engine of (2.3) and (2.9).

---

## 3. Lemma 3.6 — the engine: exact statement, hypotheses, uniformity, toys

**Statement (p. 18, rendered PDF):**

> Let V ⊂ ℂⁿ be a finite union of distinct irreducible varieties of pure dimension k and total degree a. For every D ≥ 0, H_V(D) ≤ a·C(D+k,k). (3.5)
>
> Suppose in addition that every member of this family is an irreducible component of a common locus defined by equations of degree at most L ≥ 1. Other components of that locus may have any dimension. There is an integer q ≤ C_nL such that, for D ≥ q, H_V(D) ≥ a·C(D−q+k,k). (3.6)
>
> In particular, H_V(L) ≥ c_n a L^k. (3.7)
>
> The same assertions hold for projective varieties, with homogeneous restriction rank.
>
> [Union of lists: L ↦ L_* = Σ_ν L_ν.]

**What it assumes about a versus D.** Nothing. There is no hypothesis relating a to L or D, so components of degree up to L^{n−k} (the refined-Bézout maximum) are allowed. The only hypothesis is that every member is an irreducible component (isolated, i.e. not contained in a larger component) of a locus cut out by equations of degree ≤ L.

**Is the constant uniform? Yes.** It is c_{n,k} = 1/((n−k+1)ⁿ·k!), independent of a, L, D, the number of components, and the other components of the locus. Derivation:
- Lemma 3.3, applied on the geometric generic fibre in F^{n−k}, gives q = (n−k)(L−1). In the union-of-lists case, Lemma 3.5 gives q ≤ (n−k)L_*.
- b = n−k+1 gives bL − q ≥ L.
- By (3.8), H_V(L) ≥ b^{−n} H_V(bL) ≥ b^{−n} a·C(L+k,k) ≥ a L^k / (bⁿ k!).

**Proof, verified line by line:**
- **Upper bound (3.5).** Hyperplane-restriction induction on h⁰(O_V(D)), with base h⁰(O_V) ≤ #components ≤ a and hockey-stick summation. It needs a general hyperplane section of a reduced variety to be reduced. The paper gets this from openness of geometrically reduced fibres (Stacks 0578, statement checked) applied to the incidence correspondence. This is an independent proof of Chardin's theorem (Kollár's route, which Chardin's own closing Note mentions).
- **Lower bound (3.6).**
  - Generic linear normalization: finite of degree deg Vᵢ, because the centre at infinity misses V̄ᵢ ∩ H_∞ for dimension reasons ((k−1)+(n−k−1) < n−1).
  - The a sheets of the geometric generic fibre are distinct; different Vᵢ have disjoint generic fibres since Vᵢ ∩ Vⱼ does not dominate.
  - They are isolated in the generic fibre of the whole system, since Vᵢ ∩ W is non-dominant for every other component W, including higher-dimensional ones.
  - Lemma 3.3 applies over F = algebraic closure of ℂ(t); the fibre equations have y-degree ≤ L.
  - Choose a monomials with independent evaluation columns. A ℂ-relation among the products t^α mᵢ becomes an F-relation with polynomial coefficients in t, which forces every c_{i,α} = 0.
- **(3.8) H_V(bL) ≤ bⁿ H_V(L).** Standard monomials for a degree-compatible order form an order ideal and, in degree ≤ D, a basis of ℂ[x]_{≤D}/I_{≤D}. x^α ↦ x^{⌊α/b⌋} maps standard to standard (it divides x^α), with ≤ bⁿ preimages. Correct.

This sharpens Walsh [27, Thm 2.6], which gets the same bound from C–P Cor. 3 only for m ≥ 2(n−d)δ(V). The (3.8) trick brings it down to the defining degree m = δ at a constant-factor cost. Correct.

**Uses checked against the statement:**
- **(2.3), p. 10:** projective version, n = d−1, L = D = ⌊A⌋. The envelope is a locus of degree-D forms; any subfamily of its j-dimensional components qualifies; H_S(D) = H_{Env}(D) ≥ H_{V_j}(D) by (3.1) and monotonicity.
- **(2.9), p. 13:** affine skew-form space, n = s₀+d, L = D. Same reasoning; the envelope = whole space case is the k = n case, q = 0.
- **(A.6)/(A.7), p. 76–77:** single component, L = m. Form matches.

**Toys** (brief's list; exact rank computations mod 1000003 in toys.py, plus hand computation):
1. **Complete-intersection curve of degree D² in P³ (n = 3, k = 1, L = D).** H_Y(D) = C(D+3,3) − 2 ≈ D³/6. The lemma requires ≥ c·D²·D with c = 1/(3³·1!) = 1/27. Holds; the scaling is the right order (D³ on both sides). Numerically, on the degenerate complete intersection {∏(x−αᵢ) = ∏(y−βⱼ) = 0} (D² lines), H(D) = 2, 8, 18, 33, 54 for D = 1..5, exactly C(D+3,3) − 2, against bounds 0.04…4.63.
2. **a ≤ D concurrent lines in P² (affine chart, n = 2, k = 1, L = D, envelope = the lines).** Computed H(D) = a(2D+3−a)/2 exactly for all 1 ≤ a ≤ D ≤ 7. The lemma requires ≥ aD/4. Holds.
3. **Mixed dimensions.**
   - Plane {x = 0} ∪ CI curve V(f, g) in P³, f, g of degree D−1: Env_D = this union, I_D = x·⟨f, g⟩, so H = C(D+3,3) − 2. This beats the Cor. 3.7 bound c(D² + (D−1)²D).
   - (L−1)² grid points as the isolated points of {x·f, x·g} beside the line {x = 0}: computed H(L) = 1, 4, 9, 15, 22, 30, 39 for L = 2..8, against a/9 = 0.11…5.44.
   - Also checked (3.8) on random point sets in ℂ²: no violation.

**Verdict on the brief's concern (ii): (3.7) HOLDS at the defining degree, uniformly in the component degrees.**

---

## 4. The rest of §3, item by item

- **Lemma 3.1 (p. 15).**
  - s_p = ∏_{ρ∈Δ(P)} (Σ(xⱼ−pⱼ)² − ρ²)/(−ρ²) has degree 2|Δ(P)| = 2(M−1). Its values on the real sample are 1/0 (distance set positive; checked; also formalized in the OAI Lean file: `eval_physicalSeparator`, `degree_physicalSeparator`).
  - (3.2): induction on dimension, using that s_p is nonzero at p ∈ V so its section is proper, of degree ≤ 2Ma. This gives C_u = 1 + 2C_{u−1}, i.e. C_u = 2^{u+1}−1.
  - Exact isolation (3.3) is correct over ℂ.
  - In Lemma 2.4 the product of separators for p and for q, written in (v₀, y₀), has degree 4(M−1) = O(M) ≤ O(A). Correct.
  - Real/complex: s_p is real; counting real points on complex V needs only s_p(p) ≠ 0. Correct.
- **Lemma 3.2 (Koszul / Ext).**
  - The chain map K(f) → K(Z) is ∧Q, so its top degree is det Q.
  - Ext^{c−1}_R(K, R) = 0 for finite length K (depth c), hence Ext^c(F, R) ↪ Ext^c(R/(f), R), sending 1 ↦ det Q.
  - Correct; this is Wiebe's socle theorem in disguise.
- **Lemma 3.3.**
  - Prime avoidance gives c combinations, each of degree ≤ L.
  - The divided-difference matrix has entries of y-degree ≤ L−1.
  - The vanishing argument for y ≠ z: the adjugate times a unit coordinate of y − Z.
  - Setting Y = z gives f(Z) = Q(z,Z)(Z−z).
  - The functional λ commutes with evaluation.
  - The jets u = 3s²−2s³ and v = (Yⱼ−zⱼ)s² have the right values and first derivatives.
  - Exact isolation in degree c(L−1)+1.
  - All correct. **“Isolated”** means a 0-dimensional irreducible component of the common zero set; other components of any dimension are allowed. **Degree** c(L−1), independent of |S|.
- **Lemma 3.5.** Product of the separator in the list containing z and an exact-isolation equation for each other list, normalized at z. Degree ≤ Σ(c(L_ν−1)+1) ≤ cL_*. Correct.
- **Cor. 3.7.** Max over k loses n+1. Upper bound by injecting into ⊕_k restrictions. Correct.
- **Lemma 3.8 (pp. 20–21).**
  - J annihilates ker E_D = I(V)_{≤D}, so rank(E_D, J) = H_V(D).
  - First-order interpolation (Lemma 3.3/3.5) gives (a+b) independent augmented columns. ∂_y commutes with t^α since vᵢ is vertical, so (a+b)·C(D−q+k,k) ≤ a·C(D+k,k).
  - For D ≥ 2q, the ratio ∏(D+i)/(D−q+i) ≤ 1 + C q/D, so b ≤ C_n aL/D.
  - Minors have degree ≤ (n−k)(D−1).
  - The analytic-germ argument (smooth k-germ ⊇ pure k-dimensional V forces equality, so two components cannot share it) is correct.
- **Lemma 3.9.**
  - deg C ≤ aL′ in dimension k−1, so (3.5) gives H_C(D) ≤ aL′·C(D+k−1,k−1).
  - I(C)_{≤D} ⊂ I(forced)_{≤D} gives H_forced ≤ H_C.
  - Lower bound (3.6) on the forced subfamily, so b ≤ C_n aL′/D.
  - g is chosen outside finitely many proper subspaces.
  - Correct.
- **Lemma 3.10.**
  - m = ⌈np/r⌉ and the digit decomposition (3.13); deg hᵢ ≤ mE/p ≤ (n+1)E/r for p ≥ r.
  - f^m ∈ ((Xⱼ−zⱼ)^p) because n(p−1) < np.
  - hᵢ(X)^p ≡ hᵢ(z)^p mod J_z, and the digit monomials form a basis.
  - The specialization to char p ≥ r is legitimate: R finitely generated, f(x*)^{-1} adjoined, Noether normalization plus lying-over.
  - Correct. Sanity check n = 1: the bound gives 2|S|; the truth is |S|.
- **Lemma 3.11.** Multilinear column expansion of det(A(p) + (A(x) − A(p))). Correct.
- **Lemma 3.12.**
  - (i) Blow-up at p: f*O(1) = O(H−E); H^{k−j}E^j = 0 for 0 < j < k; E^k = (−1)^{k−1} mult_p X; hence (H−E)^k = a − mult_p X. Checked on the nodal cubic projected from its node (3 − 2 = 1·1).
  - (ii) Dimension counts on the Grassmannian. Join avoidance gives singleton fibres; avoiding T_{q₀}X gives an unramified point, hence birationality by Nakayama on the finite module. The Artin–Rees and conductor argument gives e(m_A) = e(m_A B) ≥ e(n_B).
  - Correct.
- **Cor. 3.13.**
  - G∘π has order ≥ mult_{π(p)} π(X) ≥ mult_p X > a/2.
  - x* ∉ Λ because x* ∈ J(x*, X), so the value at x* is defined.
  - Lemma 3.10 with E = a and r = ⌊a/2⌋+1 gives degree < 2(n+1).
  - Correct.
- **Cor. 3.14.** ℓ ∈ m²_{X,p} needs X smooth at p (assumed). R = O_{C,p} is a 1-dimensional domain, so length(R/ℓʲ) = j·length(R/ℓ) ≥ 2j·mult − O(1); the local intersection number is ≤ deg C. Correct.
- **Lemma 3.15.** The generic polar has no common component with F (char 0). The dehomogenized partials have order ≥ m−1; I_q ≥ m(m−1); Bézout total a(a−1); and m² ≤ 2m(m−1) for m ≥ 2. Correct. (Its only use, the inline restatement (4.3) at l. 1996, agrees.)

**Hedge-word census in §3 (case-insensitive):** “clearly/similarly/obvious/easily/the same argument/routine/well known” 0; “standard” 3 (all “standard monomials”, technical); “it follows” 1 (Lemma 3.10, checked); “usual” 2 (generic linear normalization — checked; usual basis — trivial); “directly” 2 (both trivial); “generic” 33. Every “generic” is a finite union of proper Zariski-closed conditions: coordinates, hyperplane, linear combinations, projection centre, polar coefficients, minors combination, chart. I checked each such condition is proper.

**Real versus complex inside §3:** the only crossings are in Lemma 3.1 (real separators; counting real points on complex V). Both are fine. Everything else is purely complex algebraic geometry.

---

## 5. Citation table (§3 scope, plus the Walsh citations in §1.1 that the brief asked for)

| Cited | Paper claims | Source says (quote) | Verdict |
|---|---|---|---|
| Chardin [6] | p. 17: “The upper estimate below is Chardin's Hilbert-function bound [6]” = (3.5) | p. 306: “THÉORÈME. — Soient k un corps et R = k[X₀,…,Xₙ]. Soient I un idéal homogène E.G.R. de R, de dimension D ≥ 0 et H_I la fonction de Hilbert de I. On a alors : H_I(ν) ≤ C(ν+D, D) deg I ∀ν ∈ ℕ.” (E.G.R. = équidimensionnel et géométriquement réduit) | **MATCH.** Radical equidimensional I(V) over ℂ; the paper also proves it independently. |
| C–P [7, Cor. 3] | p. 17: “the shifted lower estimate follows from the isolated-component bound of Chardin–Philippon [7, Corollary 3]” | p. 7: “Corollaire 3. Soit I un idéal homogène, engendré par des polynômes de degrés d₁ ⩾ d₂ ⩾ ⋯ ⩾ d_m. Si J ⊇ I^{<r>} est un idéal de codimension r, on a, pour tout ν > d₁+⋯+d_r − r, H(A/J,ν) ⩾ deg J·C(ν+n−(d₁+⋯+d_r), n−r).” with “I^{<r>} l'intersection des idéaux primaires correspondant aux premiers isolés de codimension r de I” | **MATCH** for a single system: q = Σd − r ≤ (n−k)(L−1), k = n−r. The range differs at D = q only (Objection 2); the paper does not rely on the citation. |
| C–P erratum [8] | p. 17: “see also their erratum [8]” | “the proof of the equivalence in the definition of (m,b)-regularity is not correct: there is a gap in the proof of (∗∗)′ ⇒ (∗)′; and this implication is indeed false (unless b = A)… Nevertheless, it does not affect the other results of the article since we only use the definition (∗)′, except at one point where it can be easily repaired as explained in Remark A” (Remark A: “The only change to be made in the sequel of the article concerns the proof of Proposition 2…”) | **MATCH / not affected.** The erratum withdraws one implication in Definition 1 and repairs the proof of Prop. 2. Cor. 3 (via Thm 1, Prop. 1, Cor. 1/Prop. 2 and Prop. 4) stands as corrected. The paper uses only the statement of Cor. 3, which is unchanged, and re-proves it anyway. |
| Stacks 00OQ | p. 16: R = F[Z]_{(Z)} is regular local | “Proposition 10.114.2. A polynomial algebra in n variables over a field is a regular ring. … All localizations at maximal ideals are regular local rings of dimension n.” | MATCH |
| Stacks 00NQ | regular local ⇒ CM; coordinates form a regular sequence | “Lemma 10.106.3. Let R be a regular local ring and let x₁,…,x_d be a minimal set of generators for the maximal ideal 𝔪. Then x₁,…,x_d is a regular sequence… In particular R is Cohen-Macaulay.” | MATCH |
| Stacks 02JN | a system of parameters in a CM local ring is a regular sequence | “Lemma 10.104.2. Let R be a Noetherian local Cohen-Macaulay ring… x₁,…,x_c is a regular sequence ⇔ dim(R/(x₁,…,x_c)) = dim(R) − c” | MATCH |
| Stacks 062F | Koszul complexes of the two regular sequences are free resolutions | “Lemma 15.31.2. … an M-regular sequence is M-Koszul-regular and any regular sequence is Koszul-regular.” | MATCH (Koszul-regular = higher Koszul homology vanishes, so the Koszul complex resolves R/(f)) |
| Stacks 0578 | p. 18: “The openness of reduced fibers [25, Tag 0578] gives the assertion for a general hyperplane” | “Lemma 37.26.4. Let f : X → Y be a morphism of schemes. Assume Y is irreducible with generic point η, X_η is geometrically reduced, and f is of finite type. Then there exists a nonempty open subscheme V ⊂ Y such that X_V → V has geometrically reduced fibres.” | MATCH. The paper supplies the hypothesis: the incidence is a projective bundle over a reduced V, the generic fibre is reduced, hence geometrically reduced in char 0. |
| Fulton [14, Thm 12.3 & Ex. 12.3.1] | p. 14: componentwise refined Bézout, including the multiplicity form | — | **COULD NOT FETCH.** The multiplicity-free form used in §3 is confirmed independently: Walsh [27, Lemma 2.1]: “Let W ⊆ ℂⁿ be an irreducible variety and f₁,…,f_s … polynomials. Write Z₁,…,Z_r for the irreducible components of Z(f₁,…,f_s) ∩ W. Then Σ deg(Zᵢ) ≤ deg(W) ∏ deg(fⱼ).” (Walsh attributes it to Hartshorne, “[24, Theorem 7.7]”.) |
| Fulton [14, Ex. 12.3.7(ii)–(iii)] | p. 14: isolated CI multiplicity = local length (CM) | — | **COULD NOT FETCH.** The fact (Serre's formula, CM case) is standard; not used in §3. |
| Fulton [14, App. B.6, Prop. 4.4] | p. 24: blow-up and degree formula for a linear system with base locus | — | **COULD NOT FETCH.** The paper computes (3.15) directly from intersection numbers on the blow-up; I verified that computation independently. |
| TYZ [26, Thm 4.1] | p. 20: “Tidor, Yu, and Zakharov formulate regular approximate complete intersections whose Jacobian recovers the tangent space generically” | 2608.14454v1 p. 28–29: “Theorem 4.1. Let V ⊆ ℂⁿ be a codimension-r irreducible variety. Then there exist polynomials f₁,…,f_r … such that: (1) V is an irreducible component of Z(f₁,…,f_r); (2) ∏ deg fᵢ ≲ₙ deg V; and (3) the Jacobian of f₁,…,f_r has full rank (that is, rank r) on a Zariski-dense open subset of V.” They add: “In Section 4.2 we prove (3) for varieties of codimension at most 2. The full proof … we defer it to a companion paper [56].” | **MATCH.** It is not used: Lemma 3.8 is the paper's own, weaker-degree, family-level substitute, proved in full. |
| Walsh [27] (§1.1, App. A) | “approximate complete intersections” | 1811.07865v2: “Theorem 1.3. Let V ⊆ ℂⁿ be an irreducible variety of dimension d. Then V is an irreducible component of Z(f₁,…,f_{n−d}) for some polynomials fᵢ with ∏ deg(fᵢ) ≲ₙ deg(V).” Also, not cited by the paper but the closest prior form of (3.7): “Theorem 2.6. Let V ⊆ ℂⁿ be an algebraic set of dimension d. Then, there exists some constant c₀ ≳ₙ 1 such that, for every m ≥ 2(n−d)δ(V), we have the bound H_{I(V)}(m) ≥ c₀ m^d deg(V). Proof. This follows from [11, Corollaire 3].” | MATCH (§1.1 description). (3.7) is a correct strengthening of Thm 2.6 down to m = δ(V). |
| Walsh [28] (§1.1, App. A l. 4924) | “Walsh's concentration parameters [28, Section 1.1, definition of D_m]” | 1906.05843v2 §1.1: “D_m(T) = max{deg(T_W)/deg(W) : dim(W) = m}, where the maximum goes along all m-dimensional varieties.” | MATCH |
| Hartshorne [17] | not cited in §3 (only “[14, 17]” at App. A l. 5102) | — | COULD NOT FETCH; nothing in §3 depends on it |

---

## 6. Constant-dependency table (§3)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | OK? |
|---|---|---|---|---|---|
| deg s_p = 2(M−1) | Lemma 3.1 | M = 1+\|Δ(P)\| (a degree, not a constant) | Lemma 2.4 separators (product 4(M−1) = O(A)); (5.2) initial isolation degree | — | yes |
| C_u in (3.2) | Lemma 3.1 induction | u only (C₀ = 1, C_u = 1+2C_{u−1}) | (4.3.1) l. 1812; l. 3228 (u = 1) | P, V, a, M | yes |
| exact-isolation degree ≤ 2M+1 | Lemma 3.1 | M (true value ≤ 2M−1) | (5.2) l. 2192 | — | yes |
| separator degree c(L−1); jet degree ≤ 3c(L−1) ∨ 2c(L−1)+1; isolation degree c(L−1)+1 | Lemma 3.3 | number of variables c, L | Lemmas 3.5, 3.6, 3.8; l. 2205 | \|S\|, other components | yes |
| C_c L_* | Lemma 3.5 | c | Lemma 3.6 (union version), 3.8; l. 2551 | number of lists, \|S\| | yes |
| q = (n−k)(L−1) (or ≤ (n−k)L_*) | Lemma 3.6 | n, k, L | (3.6), (3.8), Lemmas 3.8, 3.9 | a, components | yes |
| c_{n,k} = 1/((n−k+1)ⁿ k!) | Lemma 3.6 via b = n−k+1 in (3.8) | n, k | (3.7) → (2.3), (2.9), (A.7), Lemma 3.9 | a, L, D, number and type of other components | yes (brief's concern ii: uniform) |
| upper constant C(D+k,k) | (3.5) | exact | (2.9) sample rank; Lemma 3.9; (A.6) | — | yes |
| c_n/(n+1) | Cor. 3.7 | n | Env applications | — | yes |
| C_n in “D ≥ C_n L” | Lemma 3.8 | n (≈ 2(n−k) suffices) | l. 2538, 3116, 3838 | — | yes, but see Objection 5 |
| C_n in exceptional degree C_n aL/D | Lemma 3.8 | n | same | a, D, L | yes |
| C_n in D ≥ C_n max{L, L′}, C_n aL′/D | Lemma 3.9 | n (via c_{n,k}, (3.5)) | l. 2530 | — | yes |
| (n+1) | Lemma 3.10 | n | Lemma 3.11, Cor. 3.13, l. 3638 | \|S\| | yes |
| 2(n+1) | Cor. 3.13 | n | l. 3366 | a, \|S\| | yes |
| 1/2 | Cor. 3.14 | — | l. 3222 | — | yes |
| 1, 2 in (3.17) | Lemma 3.15 | — | (4.3) l. 1996 | — | yes |

**No §3 constant depends on N, the sequence, δ, M/A, a window or a scale. §3 contains no asymptotic statement, so it cannot be the source of a hidden rate. There is no cycle: §3 imports nothing from §§2, 4–7 or the appendices.**

---

## 7. Verified line by line versus skimmed

**Verified line by line:**
- Lemma 3.1 (construction, degree, (3.2) induction, exact isolation, real/complex)
- Lemma 3.2 (Koszul chain map, Ext injectivity)
- Lemma 3.3 (all steps)
- Lemma 3.5
- Lemma 3.6 (upper bound induction and hockey stick; lower bound normalization, isolation, independence, count; (3.8) monomial map; choice of b; union version)
- Cor. 3.7
- Lemma 3.8 (rank identity (3.10), augmented interpolation, (3.11), binomial ratio, minors and germs)
- Lemma 3.9
- Lemma 3.10 (char p, specialization)
- Lemma 3.11
- Lemma 3.12 (i) intersection computation and (ii) dimension counts, birationality, multiplicity comparison
- Cor. 3.13, Cor. 3.14, Lemma 3.15
- The applications of Lemma 3.6 in (2.3) and (2.9), including H_S(D) = H_{Env}(D) and subfamily monotonicity
- Toys run numerically

**Checked at the level of “the statement used matches the statement proved” only:**
- the §4–6 and App. A call sites (l. 1812, 1996, 2192, 2205, 2530–2551, 3116, 3228, 3366, 3638, 3838, 4936–5019)

**Accepted as standard without line-by-line reproof:**
- existence of the generic Noether normalization of the stated degree
- “reduced by localization” for the generic fibre of the incidence correspondence
- Artin–Rees
- the classical inequality I_q(F,G) ≥ m_q(F)·m_q(G)
- that the degree of E with respect to O_E(1) is the Hilbert–Samuel multiplicity

**Not checked:**
- Fulton [14]'s text (COULD NOT FETCH)
- the “perturb and specialize” multiplicity sketch (Objection 1), which §3 does not use
- the JAG publisher PDF of [7] (author copy read)

---

## 8. Verdict for scope `algebra`
**HOLDS AS READ.** Lemma 3.6, the engine of (2.3) and (2.9), is correct as stated: H_V(L) ≥ c_{n,k}·a·L^k at the defining degree, with c_{n,k} = 1/((n−k+1)ⁿ k!) uniform over all families. It makes no assumption on component degree versus L, and it needs only that the members are irreducible components of a degree-≤ L locus, with other components of any dimension allowed. Lemmas 3.1–3.15 are proved correctly, with constants depending only on the ambient dimension.

**COULD NOT CHECK:** Fulton's text (book). The one Fulton-backed claim I did not prove myself, the multiplicity form of refined Bézout (Objection 1), is not used in §3. It is used in Appendix A and should be checked there.

**Cross-scope flags:**
- Objection 5: “D ≥ C_n L” at the §5–6 applications needs s large.
- Objection 6: the Lean development depends on OAI multiplicity modules the paper never cites.
