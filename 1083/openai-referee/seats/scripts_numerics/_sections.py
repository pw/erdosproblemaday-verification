import os
D = '/tmp/oaimath/166/numerics_scripts'
O = os.path.join(D, 'outputs')
def out(name): return open(os.path.join(O, name + '.txt')).read().rstrip()
sec = []
def add(title, text, names):
    s = f"## {title}\n\n{text.strip()}\n\n"
    for n in names:
        s += f"Script `numerics_scripts/{n}.py` — verbatim output:\n\n```\n{out(n)}\n```\n\n"
    sec.append(s)
add("(a) The grid {1..t}^d", """
Enumerate {1..t}^d. Collect the squared distances of all point pairs exactly (integers), and cross-check against the set of squared lengths of difference vectors. The paper claims (p. 1) "its squared distances are integers between 1 and d(t − 1)²". This holds in all 10 instances. The ratio |Δ|/n^{2/d} = |Δ|/t² stays bounded: it lies in [0.75, 2.03] and tends to (5/6)·3 for d=3 (Legendre's three-square theorem) and to 4 for d=4. This is the matching upper bound O(n^{2/d}).""", ['a_grid'])
add("(b) Solymosi–Vu recurrences applied by hand", """
Recurrences, quoted from the journal text in refs/solymosi-vu/sv.txt:
- Thm 2.1: t(A) = Ω(max(n/m^{(d−1)/d}, t_{d−1}(m))).
- Cor 2.3: α ↦ dα/(dα+d−1).
- Cor 2.6: α ↦ (d+1)α/(2dα+d−1).
- "All theorems and corollaries in this section hold … if we replace t_d(n) by g_d(n)."

Arithmetic:
- (i) d=3 with Guth–Katz g₂(m) ≳ m/log m. Corollary 2.3 does not apply (it needs a constant power α), so Theorem 2.1 is used directly: min_m max(n m^{−2/3}, m/ln m). The minimum sits at the crossing n = m^{5/3}/ln m, where ln m ∼ (3/5) ln n, so the value is ∼ (5/3)^{2/5} n^{3/5}/(ln n)^{2/5}. Answer: **3/5, with (log n)^{2/5}**.
- (ii) d=4 with α₃ = 2/3: Cor 2.3 gives (8/3)/(8/3+3) = **8/17**. The alternative, Cor 2.6 from the plane, gives 5/11 < 8/17.
- d=5 with α₃ = 2/3: Cor 2.6 gives 4/(20/3+4) = **3/8**. Cor 2.3 from 8/17 gives 10/27 < 3/8.
- TYZ's ε(N) ≲ log log N/log N passes through both maps continuously, so the results are n^{8/17−o(1)} and n^{3/8−o(1)}.
- The general **2/d − 2/(d(d+2)) = 2(d+1)/(d(d+2))** is SV's own Theorem 1.1(b). It comes from Cor 1.3 with Tardos's α₂ = .8635 and α₃ = .5643. The script confirms that SV's Cor 1.3 exponents exceed it for d = 4..10, and that Cor 1.3 equals Fact 2.8 with d₀ = 2, 3.

All of this agrees with the paper's §1.1 (pp. 1–2). See the citation table.""", ['b_sv'])
add("(c) Exponent bookkeeping of §2", """
Tabulated for d = 3..8 in base-A exponents:
- N = A^{d/2} and N² = A^d.
- N ≤ A^{d−1} ⟺ d ≥ 2.
- A^{d/2} ≤ A^{d−2} ⟺ d ≥ 4. This is the isotropic cap of Lemma 2.5; d=3 uses the C_rich A deletion instead.
- Prop 2.2, ℓ ≥ 4 branch: 2 + (d−ℓ)/2 ≤ d/2 ⟺ ℓ ≥ 4, checked in each fibre case. The circle case has exponent 1 and the ≤2-point case exponent 0, both dominated.
- δ(H)/A^{d−1} = c₃ A^d/(M A^{d−1}) = c₃A/M → ∞, with no rate used.
- C(D+s₀,s₀) ≤ C₄A^{s₀}.
- A^{d−1} = N^{2(d−1)/d}: N^{4/3}, N^{3/2}, N^{8/5} for d = 3, 4, 5. This is "the fixed positive power of N" behind the union bound over N² vertices.
- Excess h = d−2 = r−1; ambient dimension s₀ + d = d(d+1)/2.

The table rows marked "FAILS (branch NOT used)" are the ℓ ≤ 3 cases. The paper does not use the fibre count there; it uses Lemma 2.1, the greedy curve bound, the light-line bound, and N = A^{3/2} when d=3 and the span is the whole space. Those bounds are A², KA·deg Y and H·deg Y respectively, each of which is ≤ C deg(Y)A^a. `c2_extra.py` adds:
- the Lemma 2.1 inversions;
- the Prop 2.2 dyadic sum, whose ratio to N²/H + N·L_max is ≤ 8;
- c₁ and c₄;
- the sizes in the Chernoff/union bound.""", ['c_exponents', 'c2_extra'])
add("(d) Skew-form identities (2.6)–(2.8) and polarization (pp. 11–13)", """
The p. 11 matrix identity was checked in three ways:
- symbolically (sympy, generic p, q, Z): Ωv − y ≡ 0 on F_{p,q}, using v₀·Zv₀ ≡ 0;
- with random reals (200 trials, d = 3, 4);
- with exact rationals.

Distinct pairs give distinct flats. The map v ↦ (Zv)_Z has rank d, so equality "for every skew Z then recovers v₀" holds; and (p,q) vs (p,q′) gives different flats.

dim F_{p,q} = s₀.

{Z skew : Z(u+w) = u−w}, tested exactly over 40 rational trials per d, with |w| = |u| produced by a rational Cayley rotation:
- nonempty, of codimension exactly d−1 (rank of Z ↦ Zx equals d−1), whenever |u| = |w|;
- empty when |w| = 1.5|u|;
- empty when u + w = 0. This is why R must be generic: "The rotation R may be chosen to ensure u+w ≠ 0".

Global polarization: B(X,X′) = −(v₀−v₀′)·(y₀−y₀′) = −(|p−p′|²−|q−q′|²)/4, symbolically, so (v₀−v₀′)·(y₀−y₀′) = 0 ⟺ |p−p′|² = |q−q′|².

Local polarization: (u_i−w_i)·(u_j+w_j) + (u_j−w_j)·(u_i+w_i) = 2(u_i·u_j − w_i·w_j), symbolically.

Also checked: the identity (Zv₀−y₀) − (Zv₀′−y₀′) = −½(Z(u+w)−(u−w)), which is (2.8); and the Prop 2.2 radius-class identity.""", ['d_skew', 'd2_symbolic', 'd3_exact'])
add("(e) Lemma 2.5: equal Gram matrices ⇒ isometry (d = 3)", """
Built S ∈ O(3) with SU = W from orthonormal bases of span U and span W. Cases:
- generic k = 1..5 vectors;
- a dependent set (u₃ = u₁ + 2u₂);
- a collinear set;
- 4 vectors in a plane;
- W built directly from the Gram matrix (Cholesky), not from any S₀.

Well-definedness was checked as kernel preservation, |W·ker U| ≈ 1e-16. That is the paper's "every linear relation is preserved by equality of the Gram matrices". Both orientations of S₀ were tested. Negative control: unequal Gram matrices are rejected. The match check x ↦ q + S(x−p) sends p+u_i to q+w_i.""", ['e_gram'])
add("(f) d = 3 rich motions on small grids (sanity of Theorem 7.1's scale)", """
`f_motions.py` uses lattice isometries: 48 signed permutations times all integer translations, t = 3..7. For t = 3, 4 it adds rational rotations from integer quaternions of bounded norm (a partial enumeration).

`f2_all_isometries.py` is exhaustive over **all** isometries of R³ with a non-collinear match set, for t = 3. Such a g maps two independent difference vectors of P to difference vectors with the same Gram matrix. All 721 152 candidate linear parts were generated and deduplicated to 13 392 orthogonal S; the 48 lattice ones serve as a positive control. Collinear match sets have k ≤ 3 < A.

Σ_{k≥C_rich A} k² / N^{10/3} comes out between 1.5 and 4.3 for C_rich ∈ {1, 2}, decreasing in t. The non-lattice motions add exactly the 192 motions with k = 9 = A that the partial rational enumeration also found. Caveat (objection 7): the grid violates M ≤ A but satisfies the line cap that the proof actually uses. This is a scale sanity check, not a test of K_rich.""", ['f_motions', 'f2_all_isometries'])
add("(g) Lemma 2.1 circle and line rows", """
"A circle contains at most 2M points", with M = 1 + |Δ|. Findings:
- The proof gives 2M − 1.
- Regular odd polygons attain 2M − 1 exactly: the extremal configuration is the regular (2k+1)-gon, with |Δ| = k.
- Regular even polygons, with or without the centre, do not attain it.
- Exhaustive subsets of the regular 12- and 13-gons never exceed 2M − 1.
- Subsets of the integer points on x²+y² = 25 and = 65 stay strictly below it.

Line row: n collinear points have M ≥ n, so "2M" is loose by a factor 2. See objection 1.""", ['g_circle'])
add("(h) Hilbert-function toys for Lemma 3.6", """
Each toy records n (ambient projective dimension), k, a, L (the defining degree) and the exact H. The tester c_{n,k} = 1/((n−k+1)^n k!) is the algebra seat's value: q = (n−k)(L−1) and b = n−k+1 in (3.8). H was computed as an exact evaluation rank mod two primes, and cross-checked with closed forms and with sympy Gröbner standard-monomial counts.

Results (asymptotic values of H/(a L^k)):

| Toy | n, k | H/(a L^k) | c_{n,k} |
|---|---|---|---|
| D′ ≤ D concurrent lines in P² | 2, 1 | (2D−D′+3)/(2D) ≥ 1/2 | 1/4 |
| D′ > D concurrent lines in P² (not components of Env_D) | 2, 1 | can fall below c_{2,1}; at their own defining degree L = D′: (C(D′+2,2)−1)/D′² → 1/2 | 1/4 |
| CI of two degree-D surfaces in P³ (degree D² = D^{codim}) | 3, 1 | (C(D+3,3)−2)/D³ → 1/6 | 1/27 |
| general points in P² | 2, 0 | 1 | 1/9 |
| collinear points in P², a ≤ D | 2, 0 | 1 | 1/9 |
| collinear points in P², a ≥ D+1 (the line enters Env_D) | 2, 0 | hypothesis fails | — |
| D² CI points in P² | 2, 0 | → 1/2 | 1/9 |
| D³ CI points in P³ | 3, 0 | → 1/6 | 1/64 |
| isolated points of a system with an extra 1-dimensional component | 2, 0 | 0.83–1 | 1/9 |

For D′ > D concurrent lines: degree-D forms vanishing on D′ > D concurrent lines vanish identically, so these lines are not components of Env_D. There H_Y(D) = C(D+2,2) < c_{2,1}·D′·D once D′ > 2(D+1)(D+2)/D. Example: 16 lines at D = 3 give H = 10 < 12.

Summary:
- **0 of 62 hypothesis-satisfying toys violate the lower bound.** The minimum of (H/(aL^k))/c_{n,k} is 2.30.
- **4 of 38 hypothesis-violating toys fall below it**, all of them concurrent-line toys: so the component-of-the-envelope hypothesis is necessary. The paper's uses satisfy it. (2.3) takes "the projective envelope of those directions at degree D", and (2.9) takes "the envelope of their union" at degree D, i.e. components of a degree-D locus.
- The shift (3.6) holds with q ≤ (n−k)(L−1) and is **tight** for CI points in P²: H first reaches a at m = 2(L−1). For the CI curve in P³ the minimal q is L−1 ≤ 2(L−1).
- (3.5) H ≤ a·C(D+k,k) holds in all 100 toys.
- (3.8) H(bL) ≤ b^n H(L) holds in all 36 instances.

In (2.3) the components live in P^{d−1} and can have degree up to D^{codim}. The toys with a = D² and a = D³ cover that regime: they still sit far above c_{n,k}.""", ['h3_hilbert', 'h2_lemma36'])
add("(i) Explicit constants and exponent inequalities in §5–6", """
Recomputed every displayed numerical claim found in §5–6, symbolically or exactly where possible, and over 100 000 random admissible limiting profiles (−1 ≤ b₁ ≤ … ≤ b_d ≤ 1, Σb_i = 0, max|b_i| ≥ 1/2). Margin statements are written in normalised logarithms (units of s), the same convention as the paper.

- §5.1: Σ_{r>i}a_r < a_i/9 and the 7/18 of (5.4), exactly; Σa_i = s^{1/10+o(1)} (see objection 4); the summability inequalities of (5.5) with c = log 2/10 and the vanishing sums; the lower-boundary exponent −(√2−1)√s; E L²/N = δ e^{6s_*} → 0; width halving.
- (5.6)–(5.7): the σ plateau identity; b₁+b₂ < 0, with 0 violations over 80 000 profiles; Figure 2's profile.
- Prop 5.5: e_{d−1}/N = e^{−b_d s}/B.
- (6.5)–(6.7): the initial interval T^{2d−1} ≥ σ²T/(D₁D₂); the k = d−1 inequality, which reduces to T ≤ D₂; non-outermost margins ≥ min(1, −(b₁+b₂)) > 0, observed minimum 0.256; outermost margin 1 − b_d.
- (6.9): see objection 2.
- (6.10) and Lemma 6.4: margins t₀−β, t₀−(1+b₁+b₂), t₁−t₀−ε; the k≥2 deletion exponent d−k+1 < d; T_s(t₂) = B^{1+t₂} = B^{2−(1−t₂)}; the outermost Bézout fraction √δ·B^{−c+o(1)}; the final row EM/n ≤ √δ·M/A → 0 with no rate.
- (6.20): e_j B^{l+1}/N = B e^{s Σ_{i≤j} b_i} = B e^{−s Σ_{i>j} b_i} = R; the B-exponent is 1 for every (d, j).
- Wider windows: q = B^{1/2} = o(r), r = B^{1−o(1)}.
- (6.26): exhaustive over all plateaux j = 1..d−1 of every profile. A strictly negative margin exists in every case **except** narrower centres with l = 1 and b_{j+1} = b_d > 0, which is exactly the zero-margin case the paper names and treats in §6.5. Wider centres never lack a margin.
- (6.25)/(6.27) ≥ δ^{−1} e^{cs/3}.
- §6.5: R·D_d = B² = A; e_{d−1}/R = B^{d−2} = N/A; exceptional degree over projected degree = δ e^{(ε−η)s} → 0, with the δ factor only helping. This matches the paper's warning "One must not instead compare (N/A) exp(−o(s)) directly with δN/A".

No inequality in §5–6 compares δ with an uncontrolled exp(o(s)) factor. Every contradiction rests on a fixed positive multiple of s.""", ['i_sec56'])
open(os.path.join(D, '_sections.md'), 'w').write("\n".join(sec))
# appendix: scripts verbatim
names = ['a_grid', 'b_sv', 'c_exponents', 'c2_extra', 'd_skew', 'd2_symbolic', 'd3_exact', 'e_gram', 'f_motions', 'f2_all_isometries', 'g_circle', 'h3_hilbert', 'h2_lemma36', 'i_sec56']
app = "## Appendix — scripts, verbatim\n\nRun as `nice -n 19 python3 <script>.py` (f2_all_isometries.py with argument `3`) from /tmp/oaimath/166/numerics_scripts/.\n\n"
for n in names:
    app += f"### `{n}.py`\n\n```python\n{open(os.path.join(D, n + '.py')).read().rstrip()}\n```\n\n"
open(os.path.join(D, '_appendix.md'), 'w').write(app)
print("ok")
