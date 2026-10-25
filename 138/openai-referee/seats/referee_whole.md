# Hostile referee report — seat `whole`

Paper: OpenAI, "Quantitative Superexponential Bounds for van der Waerden Numbers" (23 Sep 2026, 25 pp; sha256 042acea3…, `/tmp/oaimath/160/paper.pdf`).
Source read: the paper's own LaTeX, `build/sections/01–08*.tex` (all 1,810 lines, every line read), `paper.tex`, `preamble.tex`.
Lean read as text only (never ran lean/lake): `lean/ComparatorChallenges/QuantitativeVanDerWaerden.lean`, `lean/OAI/Combinatorics/ProgressionColoring/{Model,Main,UniformTransfer,CyclicWitness,LargeColorConsequences,CyclicBasic,DigitProduct,DigitProductBounds,Basic,UpperBound(§F, finite_ramsey),GrowthConsequences(statements),LargeColorGrowth(exp_bound)}.lean`.
Scripts: `/tmp/oaimath/160/seats/whole_checks/` (all runs < 7 s, < 100 MB).

Label → printed number → printed page (from the PDF): setup:dilation = Lemma 2.1 p.4 · setup:prime = Lemma 2.2 p.4 · mesh:width = Lemma 2.3 p.5 · mesh:neighbors = Lemma 2.4 p.6 · mesh:truncated = Lemma 2.5 p.6 · count:arrangement = Lemma 3.1 p.7 · count:global = Lemma 3.2 p.7 · count:eligible = Definition 3.3 p.8 · count:local = Lemma 3.4 p.8 · outer:lll = Lemma 4.1 p.10 · outer:coloring = Proposition 4.2 p.10 · dichotomy:affinity = Lemma 5.1 p.12 · dichotomy:drift = Lemma 5.2 p.12 · dichotomy:path = Lemma 5.3 p.13 · dichotomy:heavy-width = Lemma 5.4 p.14 · dichotomy:main = Theorem 5.5 p.14 · perturb:multiplicity = Lemma 6.1 p.16 · perturb:signatures = Lemma 6.2 p.17 · perturb:cyclic = Theorem 6.3 p.18 · transfer:product = Proposition 7.1 p.20 · transfer:large-r = Theorem 7.2 p.20 · transfer:limits = Corollary 7.3 p.21–22 · upper:finite = Theorem A.1 p.22–23. Equations: (transfer:division) = (7.1), (transfer:norm-color) = (7.2), (transfer:color-count) = (7.3), (transfer:midpoint) = (7.4), (upper:recursion) = (A.1), (upper:matching-blocks) = (A.2), (upper:next-block) = (A.3). Introduction display on p.2.

## 1. Verdict (whole paper, my scope)

**HOLDS AS READ.** I found no FATAL objection and no GAP in the proof of Theorem 1.1 (main:intro). Every "for sufficiently large k" inequality in §2–§6 holds for all large k with the stated parameters; there are finitely many (≈30), none depends on r, on the progression, or on the choice of the prime P (§4 table). The binding one, under the paper's own explicit constants, is the uniform sup bound in (outer:second-weight), which needs D ≥ 29,210, i.e. k ≳ 10^44.65; so the absolute K_0 exists and is ≈ 10^45 by the paper's route. §7 and the Appendix check line by line, and brute-force checks with failing controls agree with them. Formally, `uniform_lower_bound` is exactly Theorem 1.1 (no weakening). `kthRoot_tendsto` at r = 2 is exactly erdosproblems.com/138's question. `W` cannot be vacuous: with an empty set, sInf = 0 would make the theorem FALSE. The objections below are COSMETIC or UNCLEAR (attribution/exposition).

## 2. Objections (numbered)

**Objection 1. COSMETIC (gap in EXPOSITION, not in the proof). §7, Prop transfer:product (7.1, p.20), Thm transfer:large-r (7.2, p.21), proof of Thm 1.1.**
Quoted: "Translation by one now gives a coloring of $[N^m]$ with $2^m$ colors and no monochromatic $k$-term progression. This proves the first assertion." and "After translating the interval by one and using Equation~\eqref{transfer:color-count}, we obtain $W_r(k)>b^s$."
Going from "some colouring of [N^m] avoids" to "W > N^m" silently uses two facts. (a) W_r(k) exists. This is Theorem A.1, which §7 never cites, and the Introduction's "least positive integer N such that…" presupposes it. (b) The Ramsey property is monotone in N, by restriction of colourings. Both are trivial. The Lean states both explicitly: `lt_W_of_not_isRamsey` needs `hfinite`, and its docstring says "Monotonicity is used: failure at one size alone is not minimality". In `DigitProductBounds.lean` the finiteness comes from `finite_ramsey`.
Fix: add one sentence: "W is finite by Theorem A.1, and the Ramsey property passes to longer intervals by restriction."

**Objection 2. COSMETIC. Printed cross-references throughout the PDF.**
cleveref is used with lemma/proposition/definition sharing the `theorem` counter (`\newtheorem{lemma}[theorem]{Lemma}` in preamble.tex) and no `\crefname` set. The result is that **34 printed references call a Lemma, Definition or Proposition a "Theorem"**. Examples:
- p.12: "whose coordinate widths are at most 2H by Theorem 2.3. By Theorem 5.1" (these are Lemma 2.3 and Lemma 5.1).
- p.10: "In every eligible recorded pattern of Theorem 3.3" (this is Definition 3.3).
- p.14: "Theorem 4.2(i) supplies" (this is Proposition 4.2).
- p.18: "By Theorem 6.1, these positions specify at least γk/4" (this is Lemma 6.1).

Counted in paper.txt: 2.1×1, 2.2×1, 2.3×4, 2.4×2, 2.5×1, 3.1×3, 3.2×4, 3.3×2, 3.4×1, 4.1×2, 4.2×4, 5.1×2, 5.2×1, 5.3×2, 6.1×3, 6.2×1. No mathematical effect: the numbers are right, only the type names are wrong.
Fix: `\crefname{lemma}{Lemma}{Lemmas}` etc.

**Objection 3. UNCLEAR (dependency on an unrefereed companion; not a proof here). 01-introduction.tex lines 87–104, p.2.**
Quoted: "Combining it with the coloring upper bound in the companion paper~\cite[Equation~(1.3)]{openaiArithmeticProgressions2026} gives, for each integer $k\ge3$, a constant $A_k\ge1$ such that for every integer $r\ge256$, $\exp(\frac{(\log r)^2}{64\log2})<W_r(k)\le\lceil\exp(A_k(2+\log r)^{A_k})\rceil$. Thus, for every fixed progression length $k\ge3$, as integer $r$ tends to infinity, growth in the number of colors is superpolynomial but at most quasipolynomial".
- The **lower** half is this paper's Theorem 7.2. I verified it line by line and by brute force (§9.3).
- The **upper** half is the companion's (1.3). I fetched it from github.com/openai/math main (sha256 481eaf77…): "W_r(k) ≤ ⌈exp(A_k(2 + log r)^{A_k})⌉ (r ≥ 1), (1.3)". It is derived there from the companion's own Theorem 1.1, a ~160-page claim that r_k(N) ≤ C_k N exp(−c_k(log N)^{ε_k}). The citation MATCHES. The companion in turn cites "[37, Theorem 7.2]", which is this paper's Thm 7.2.
- For k = 3 the quasipolynomial upper bound is classical (Kelley–Meka). For **k ≥ 4** no published density bound gives it. Green–Tao's r_4(N) ≪ N(log N)^{−c} gives only W_r(4) ≤ exp(r^{O(1)}). Leng–Sah–Sawhney's r_k(N) ≤ N exp(−(log log N)^{c_k}) gives only W_r(k) ≤ exp exp((log r)^{O_k(1)}).
- So the clause "at most quasipolynomial" for k ≥ 4 is exactly as strong as the companion's unrefereed main theorem. The paper attributes it correctly, and it is not part of Theorem 1.1 or of the Lean formalised here (`LargeColorConsequences.lean` formalises only the lower half, via `LargeColor.exp_bound`).
Fix: say "conditional on [companion, Thm 1.1]" or confine "at most quasipolynomial" to k = 3.

**Objection 4. COSMETIC (context; nothing false). Abstract/Intro "quantitative".**
Quoted: "It is stronger than the assertion that $W_2(k)/2^k$ tends to infinity." This is true as an asymptotic implication. Numerically, though, k^{ck} with c = 10^{-5} exceeds the previous two-colour bounds (Kozik–Shabanov β·2^{k−1}; Campos–Fox–Schildkraut (1−o(1))k2^{k−1}) only once c·log k > log 2 + o(1), i.e. **k ≳ e^{69,315} ≈ 10^{30,103}**. The paper's own explicit chain also needs k ≳ 10^{44.65} (§4). The paper never states K_0 and never claims numerical superiority, so this is not an error. Recorded so that nobody quotes Theorem 1.1 as beating CFS at any feasible k.

**Objection 5. COSMETIC. Appendix notation clash (08-upper.tex lines 70–106, pp.22–23).**
"$q=b+(k-1)\Delta$" (A.3), "$B=F(r^m,k-1)$" and the block index "$b$" reuse q (the prime power of §2), B (the affine slope of §5–6) and b (the base of Thm 7.2). The Appendix is self-contained, so nothing breaks.

**Objection 6. COSMETIC. Intro line 180: "We prove all geometric, counting, and probabilistic ingredients needed here, including the finite local lemma."**
Lemma count:arrangement (3.1) proves the zero-sign reduction and the (e+1)²(s+1)^e simplification. The strict-region bound Σ_{j≤e} C(s,j) itself is only sketched ("Induction on $s$ and $e$, followed by Pascal's identity, gives the stated bound") and is cited to Stanley. It is the classical Buck/Zaslavsky count and the sketch is the standard one; the counting seat owns the detail.

**Objection 7. COSMETIC (world/formal bookkeeping, not this paper). Formal Conjectures `erdos_138` (saved `/tmp/oaimath/160/world/formal_conjectures_138.lean`).**
FC tags `erdos_138` "research solved" and links `Main.lean#L12`. That line is `uniform_lower_bound`, not `kthRoot_tendsto` (L35). It is stated for OAI's `W` (sInf over 0-based colourings ℕ → Fin r), not FC's `monoAPNumber 2` (colourings of `Finset.Icc 1 N`). The bridge from FC's W to OAI's W at r = 2, and from the uniform bound to the k-th-root limit, is mathematically immediate but is not in the linked artefact. Also, the comparator manifest (`QuantitativeVanDerWaerden.json`) checks only `uniform_lower_bound`. `kthRoot_tendsto` compiles in the same module (Main.lean), but no independent challenge file checks its statement. I read that statement and it is exactly #138 at r = 2 (§8).

No other objections. In particular, I checked brief items (a)–(j) at the level of the whole-paper interfaces:
- **(a)** count:local's constant is C = (9·16005²)^{1/3} ≈ 1321, independent of q, λ, β, D and the anchor width.
- **(b)** There is one (h,t,u,v) per progression. Every block uses that same v, and Lemma 5.4 is proved for that v at every heavy index. So the stationary-coordinate verification is right even when j_* carries a different heavy label from the one that chose h.
- **(c)** Half-open boxes are fine for Lemma 5.1, which only needs representatives in a box of side ≤ 2H.
- **(d)** Identical signatures prescribe identical events. A key carrying both outer colours makes the rich event empty.
- **(f)** The events are functions of the ξ_β alone, the dependency graph is valid, and Σ_{F∈Γ(E)} z_F ≤ l(E)/500 follows by summing over the l(E) labels (an over-count, so the direction is right).
- **(g)** The convex-combination step needs half-open product boxes and j'+h/e < j'+h ≤ k−1. Both hold.
- **(h)** Checked separately (§7, §9.2).
- **(e), (i), (j)**: §4, §5.

## 3. Dependency graph (every lemma: hypotheses needed → where supplied → consumers)

| Statement | Needs | Supplied by | Used by |
|---|---|---|---|
| (setup:parameters) (2.1) | h_0 < 2M < k | k ≥ 7 (§4 S1) | everything |
| Lemma 2.1 setup:dilation | definition of λ only | — | (setup:orders) via log λ ≤ h_0 log 2M; Def 3.3/count:coordinate-periods (rotating ⇒ s_i > h_0); Thm 5.5 short case (h ≤ h_0 ⇒ h \| λ); Thm 5.5 long case (s_i > h_0) |
| Lemma 2.2 setup:prime | k² log 4 − log(2k²+1) > k log(2k²) | k ≥ 3 (S2) | choice of q; gcd(λ,q)=1 (needs h_0 < k < P, S3); distinct terms in (setup:cyclic) (order ≥ P > k); Lemma 6.1 separation |
| (setup:q-bounds) (2.3/2.4) | P ≤ 2k², minimality of q | Lemma 2.2 | Lemma 2.3 (R ≤ (D+1)log q); (setup:orders); Lemma 6.2 (log q); Thm 6.3 (q^{2D}, N ≥ k^{ck}) |
| Lemma 2.3 mesh:width | α ≤ 1/4, R ≥ 1, θ ≤ 1 | S4 | Lemma 2.4; Lemma 2.5; Lemma 3.2 (\|V\|); Lemma 3.4 rotating case (anchor width ≤ 2H); Lemma 5.2 (box ≤ 2H); Lemma 5.4 (L_i ≤ 2H); Thm 5.5 short case (\|V\| ≤ 2H(ρ+α)); Lemma 6.1 (box ≤ 2H) |
| Lemma 2.4 mesh:neighbors | Lemma 2.3, H ≤ 1/8, 3w < 1 | S6 | Lemma 3.4 stationary case (49 endpoints); Thm 5.5 long case (\|J\| ≥ L_*/16) |
| Lemma 2.5 mesh:truncated | Lemma 2.3, arc ≤ 4H | C2 | Lemma 3.4 rotating case (16004D) |
| Lemma 3.1 count:arrangement | none (classical strict count, sketched) | Stanley | Lemma 3.2 (e=2), Lemma 3.4 (e=2), Lemma 6.2 (e=3) |
| Lemma 3.2 count:global | Lemma 3.1, (setup:orders), \|V\| from 2.3 | — | Prop 4.2 first family; Lemma 6.2 |
| Def 3.3 count:eligible | s_i from Lemma 2.1, η, V | — | Lemma 3.4; Prop 4.2(ii); Thm 5.5 long case |
| Lemma 3.4 count:local | Lemmas 3.1, 2.3, 2.4, 2.5; eligibility (ii), (iii) at the anchor; 6H < 1 | C2, C3 | Prop 4.2 (outer:second-weight) |
| Lemma 4.1 outer:lll | finite family, dependency graph | — | Prop 4.2 |
| Prop 4.2 outer:coloring | Lemma 4.1, Lemma 3.2, Lemma 3.4, cosh ≤ e^{t²/2}, O1–O6 | §4 table | Thm 5.5 light case (i) and long case (ii) |
| Lemma 5.1 dichotomy:affinity | 2kH < 1 | D1 | Lemma 5.2, Lemma 6.1 |
| Lemma 5.2 dichotomy:drift | heavy label (m_* > k/M), Lemma 2.3, Lemma 5.1, λH_x = H, k ≥ 2M, 6MH/k < 1 | D2, D3 | Lemmas 5.3, 5.4; Thm 5.5 |
| Lemma 5.3 dichotomy:path | Lemma 5.2 (v = λu, minimal h, \|u\| bound), half-open product box, 4MH < 1 | D4 | Lemma 5.4 (a integral); Thm 5.5 long case (labels distinct in a block; block = form (count:local-paths)) |
| Lemma 5.4 dichotomy:heavy-width | Lemma 5.3, Lemma 5.2 bounds, L_i ≤ 2H, 2H + 4MH/h < 1 | D5 | Thm 5.5 long case (iii) |
| Thm 5.5 dichotomy:main | Prop 4.2(i),(ii); Lemmas 5.2–5.4; Lemma 2.1; Lemma 2.3; Lemma 2.4; (dichotomy:step-lattice); D6–D15 | §4 table | Thm 6.3 |
| Lemma 6.1 perturb:multiplicity | Lemma 5.1; box ≤ 2H; λ unit mod q^D (P > h_0); distinct terms | Lemma 2.2, 2.3 | Thm 6.3 rich and affine cases |
| Lemma 6.2 perturb:signatures | Thm 5.5(ii) affine form; Lemma 3.1 (e=3); Lemma 3.2; (setup:q-bounds) | — | Thm 6.3 affine case |
| Thm 6.3 perturb:cyclic | Thm 5.5; Lemmas 6.1, 6.2; p < 1/2; R_k + A_k < 1 | P1–P4 | Thm 1.1 (via Prop 7.1) |
| Prop 7.1 transfer:product | cyclic avoidance for every d ≠ 0 incl. wrapping; N, k ≥ 2; [implicit: finiteness + monotonicity of W, Obj. 1] | Thm 6.3; App. A.1 | Thm 1.1 |
| Thm 1.1 main:intro | Thm 6.3 + Prop 7.1 with N = q^D ≥ k^{ck} | — | Cor 7.3 |
| Thm 7.2 transfer:large-r | r ≥ 256, k ≥ 3; [implicit finiteness] | self-contained | Cor 7.3; intro display (lower half) |
| Cor 7.3 transfer:limits | Thm 1.1, Thm 7.2, finiteness (log W finite) | App. A.1 | — |
| Thm A.1 upper:finite | self-contained induction | — | finiteness (implicitly everywhere W is named); Lean `finite_ramsey` |

All interfaces match. The objects passed are: the recorded word of a block = an eligible pattern for the same (h, t); "events using ξ_β" = the patterns that count:local counts; Theorem 5.5(i)/(ii) = the rich/affine split of Theorem 6.3; and Theorem 6.3's "every d ≠ 0 in Z/NZ" = the hypothesis of Proposition 7.1.

## 4. Single table of every "for sufficiently large k" inequality (brief items e, i)

Computed by `thresholds.py` (§9.1) with the paper's OWN explicit bounds:
- log λ ≤ h_0 log 2M;
- q ≤ 2k²·k^{ck/D};
- R ≤ (D+1) log q;
- T_glob ≤ [9(3k²F+1)²]^{2D} with F = k²λ + 2m;
- count:local constant C = (9·16005²)^{1/3} ≈ 1321 (from 9(16004Dh+1)² ≤ 9·16005²(Dh)² and C_0^{2D}D^{4D}h^{5D+1} ≤ (CDh)^{6D});
- arrangement constant in dimension 3: 16(s+1)³ ≤ 128s³.

Thresholds below k = 2×10^4 are exact (every integer checked). Above that the check runs on a grid k = 10^x, x step 0.01, up to 10^300, and each inequality was checked to hold at every grid point beyond its threshold. Asymptotically every one compares a larger power of k with a smaller power or with log factors.

| # | Location (TeX line, printed page) | Inequality needed | Holds for | Depends on r? | on progression? | on P? |
|---|---|---|---|---|---|---|
| S1 | 02 l.21, p.4 | h_0 < 2M < k | k ≥ 7 | no | no | no |
| S2 | setup:prime l.77–79, p.4 | k² log 4 − log(2k²+1) > k log(2k²) | k ≥ 3 | no | no | no |
| S3 | 02 l.91, p.4 | h_0 < k (< P) ⇒ gcd(λ,q)=1 | k ≥ 5 | no | no | no |
| S4 | mesh:width l.185, p.5 | α ≤ 1/4, R ≥ 1, θ = R/m ≤ 1 | k ≥ 3 | no | no | uniform |
| S5 | mesh:width l.200 | R ≤ (D+1) log q (q^{D+1} ≥ 2) | always | no | no | no |
| S6 | mesh:neighbors l.221, 226 | H ≤ 1/8; 3w ≤ 6H < 1 | k ≥ 3 | no | no | no |
| S7 | mesh:truncated l.260 | 16000D + 4 ≤ 16004D | D ≥ 1 | no | no | no |
| C1 | count:global (3.2) | log T_glob = O(k^{3/10} log k) = o(M) | absorbed in O1 | no | no | uniform |
| C2 | count:local l.176–183, p.9 | 3\|I\| ≤ 6H < 1; target range 4H < 1 | k ≥ 3 | no | no | no |
| C3 | count:local l.213–217 | h^{D+1}[C_0(Dh)²]^{2D} ≤ (CDh)^{6D} | always (C = C_0^{1/3}) | no | no | no |
| O1 | (outer:first-weight) l.131, p.11 | kT_glob e^{−(δM−1)/32} ≤ 10^{−3} | k ≳ 10^{22.70} | no | no | uniform |
| O2 | outer l.140 | log(CDh)/h decreasing on h ≥ D² (CD³ > e) | always | no | no | no |
| **O3** | outer l.143–147, p.11 | 6 log(CD³)/D ≤ 1/128, so that each summand ≤ e^{−h/128} | **k ≳ 10^{44.655} (D ≥ 29,210): BINDING** | no | no | no |
| O4 | outer l.148 | Σ_{h>D²} e^{−h/128} ≤ 10^{−3} | k ≳ 10^{15.78} | no | no | no |
| O1+O4 | (outer:incident-weight) l.152 | per-label weight ≤ 1/500 | k ≳ 10^{44.65} | no | no | uniform |
| O5 | outer l.164–166 | l(E) ≥ 100: δM−1 ≥ 100 and (D²+1)/2 ≥ 100 | k > 14^{10} ≈ 2.9×10^{11} | no | no | no |
| O6 | (outer:criterion) l.176 | 100(1/8 − 1/32 − 2/500) = 8.975 > log 2; log(1−z) ≥ −2z on [0,1/2] | always | no | no | no |
| D1 | dichotomy:affinity l.15, 26, p.12 | 2kH < 1 | k ≥ 3 | no | no | no |
| D2 | dichotomy:drift l.59, p.12 | m_*−1 ≥ k/(2M) (needs k ≥ 2M) | k ≥ 6 | no | no | no |
| D3 | dichotomy:drift l.77 | 6MH/k < 1 | k ≥ 3 | no | no | no |
| D4 | dichotomy:path l.132, p.13 | (1−2MH)/(2M) > H ⇔ 4MH < 1 | k ≥ 3 | no | no | no |
| D5 | dichotomy:heavy-width l.163, p.14 | 2H + 4MH/h < 1 | k ≥ 4 | no | no | no |
| D6 | dichotomy:main l.191 | δk/4 ≥ γk (1/40 ≥ 1/100) | numeric | no | no | no |
| D7 | (dichotomy:short-motion) l.202, p.15 | k\|w_i\| ≤ 4MH/h < 1/2 | k ≥ 5 | no | no | no |
| D8 | dichotomy:main l.226 | 2H(k+1)\|w_i\| < \|w_i\| | k ≥ 3 | no | no | no |
| D9 | (dichotomy:step-lattice) l.210 | q^{−D} ≥ α = q^{−(D+1)} | always | no | no | no |
| D10 | dichotomy:main l.253 | \|v_i\| ≤ 4MH/k < η | k ≥ 39 | no | no | no |
| D11 | (dichotomy:regular-fraction) l.262 | D(4η + 1/h_0) = 4/1000 + 1/D < 1/2 | k ≥ 1025 (D ≥ 3) | no | no | no |
| D12 | l.268–269 | \|u_i\| ≤ 2MH_x/k ≤ H_x; \|v_i\| ≤ 4MH/k ≤ H | k ≥ 20 | no | no | no |
| D13 | l.280, 287 | (2M/k)L_* ≤ L_*; 2M/k ≤ 1/16 | k ≥ 1056 | no | no | no |
| D14 | l.302–305 | k − h − δk ≥ 4k/5 (2M ≤ k/10) | k ≥ 420 | no | no | no |
| D15 | l.306 | k/10 ≥ γk | numeric | no | no | no |
| P1 | perturb:cyclic l.206, p.18 | p = k^{−1/20} < 1/2 | k > 2^{20} = 1,048,576 | no | no | no |
| P2 | (perturb:negative-coefficient) l.237–240 | 2c − γ/80 = −21/200000 < 0 | exact (Fraction) | no | no | no |
| P3 | (perturb:rich-bound) l.228–243 | R_k ≤ 2q^{2D}p^{γk/4} < 1/2 | k ≳ 1.55–1.58×10^5 | no | no | uniform (q ≤ 2k²k^{ck/D}) |
| P4 | (perturb:entropy), (perturb:affine-bound) l.130–133, 264–268 | A_k ≤ 2T_aff(1−p)^{k/4} < 1/2 | k ≥ 7,239 | no | no | uniform |
| P5 | perturb:multiplicity l.37 | 2kH < 1 (Lemma 5.1) | k ≥ 3 | no | no | no |

**(i) Quantifiers.** There are finitely many thresholds (the table is complete for §2–§6; §7 and the Appendix carry none on k beyond k ≥ 2 or k ≥ 3). Every one is a condition on k alone. P enters only through q, and the paper's bounds are uniform over every prime P ∈ (k, 2k²], as stated at 06 l.281–283. r first appears in §7. So K_0 ≈ 10^{44.7} under the paper's own constants, and it is absolute. The Lean mirrors this: `exists_cyclic_coloring` is ∃K ∀k≥K ∃N …, with no r anywhere, and `uniform_lower_of_cyclicLowerBound` takes `max K 2` before introducing r. **No reversed inequality was found.** Each line in the brief's list (e) is in the table and holds for all large k.

## 5. Prove-too-much (brief item j)

The only inequality that caps c is the rich-case union bound: 2q^{2D}p^{γk/4} needs 2c < γ/80, i.e. **c < γ/160 = 1/16000 = 6.25×10^{−5}**. The paper's c = 10^{−5} leaves a 6.25× margin.
- The affine case does not cap c. Its c-dependent term is 6 log q ≈ 6(ck/D) log k = o(pk) for every fixed c, because D ≈ k^{1/10} beats k^{1/20}.
- `cap_check.py` (§9.4) confirms this. With c = 7×10^{−5} (control), log R_k > 0 at every k from 10^6 to 10^300. With c = 6×10^{−5} or 6.2×10^{−5}, log R_k < 0 from k = 10^{10} on. The affine main term is negative for every c tried, up to 10^{−3}.

Structurally the method cannot approach k^k:
- (count:global) needs D³ log k = o(k^{1/2}), so D ≪ k^{1/6};
- log T_aff ≈ 6(ck/D) log k = o(pk) forces p = k^{−ε} with ε < 1/6;
- the rich bound needs 2c < εγ/4, with γ ≤ 1/40 from the light case δ/4.
- So the best constant is c = O(10^{−3}). The bound W ≥ k^{ck} is far below every known upper bound (Gowers' tower) and below the folklore guess 2^{k²}.

Nothing proves too much. The paper says nothing about W(k) ≥ k^{(1−o(1))k}.

Corollary transfer:limits claims nothing extra:
- the first infimum is over integers r ≥ 2 at fixed k, and the bound log W_r(k)/(k log r) ≥ (c/(2 log 2)) log k holds for all r simultaneously once k ≥ K_0, so the k-threshold ordering is correct;
- the second infimum, over k ≥ 3, uses Thm 7.2, which has no k-threshold.

## 6. Introduction claims vs what is proved (01-introduction.tex, pp.1–3)

| Claim (quoted) | Proved where | Status |
|---|---|---|
| Abstract: "absolute constants $c>0$ and $K_0$ such that $W_r(k)>k^{ck\lfloor\log_2 r\rfloor}$ for every $k\ge K_0$ and $r\ge2$" | Thm 1.1 = Thm 6.3 + Prop 7.1, c = 10^{−5} | proved |
| "Consequently $W_r(k)^{1/k}\to\infty$ for each fixed $r\ge2$ … including the two-color case" | Cor 7.3 | proved |
| "Erd\H{o}s explicitly asked for this full limit in the two-color case [p.~90, (2)]" | Erdős 1980 p.90: "I offer 500 dollars for the proof or disproof of lim f(n)^{1/n} = ∞ (2)" | MATCH (§10) |
| "It is stronger than the assertion that $W_2(k)/2^k$ tends to infinity." | k^{ck}/2^k → ∞ | true asymptotically; numerically only for k ≳ e^{69,315} (Obj. 4) |
| Fox–Hunter Thm 1 / Thm 2 / pp.2–3 paraphrases | — | MATCH (§10) |
| "For example, taking $\varepsilon=1/2$ gives a stronger lower bound when $r\ge(\log k)^6$" | r^{k log k/2} = exp(½ k log k log r) vs this paper's ≤ exp((c/log 2) k log k log r), and c/log 2 ≈ 1.44×10^{−5} < ½ | correct |
| CFS: "$W_2(k)\ge(1-o(1))k2^{k-1}$ … credit ChatGPT 5.6 Sol Pro with the coloring and an initial proof" | CFS abstract, AI-use paragraph | MATCH |
| Display $\exp((\log r)^2/(64\log2))<W_r(k)\le\lceil\exp(A_k(2+\log r)^{A_k})\rceil$, $r\ge256$, $k\ge3$ | lower half = Thm 7.2 (verified); upper half = companion (1.3) | lower: proved; upper: cited, conditional on the companion's main theorem (Obj. 3) |
| "The boundary cases are $W_1(k)=k$, $W_r(1)=1$, and $W_r(2)=r+1$." | Thm A.1 | proved + brute force (§9.5) |
| Construction paragraph: q a power of a prime > k; λ holds the full primary part at primes ≤ D² of every h ≤ 2⌈k^{1/2}⌉; periods 1 or > D²; (CDh)^{6D} independent of q, λ, anchor width; flips p = k^{−1/20} on keys (V-box, ⌊‖qỹ‖²⌋); ≤ 4 occurrences; log count O(k^{9/10} log k) = o(pk) | §2–§6 | consistent with the body, line for line |
| "We prove all … ingredients needed here, including the finite local lemma." | Lemma 4.1 proved; Lemma 3.1 strict-region count sketched | essentially true (Obj. 6) |

## 7. §7 (07-transfers.tex) line by line

**Prop 7.1 transfer:product: VERIFIED LINE BY LINE.**
- Colour n ∈ [0, N^m) by (C(n_0), …, C(n_{m−1})).
- A progression with d > 0 inside the interval has a + d ≤ a + (k−1)d ≤ N^m − 1 (uses k ≥ 2), so 0 < d < N^m.
- {i ≤ m−1 : N^i | d} contains 0. Its largest element i gives e = d/N^i with N ∤ e: for i < m−1 this is maximality; for i = m−1 it holds because N^m ∤ d, since 0 < d < N^m. "There is therefore" carries exactly this.
- (7.1) ⌊(a+jd)/N^i⌋ = ⌊a/N^i + je⌋ = ⌊a/N^i⌋ + je holds because je ∈ Z. Reducing mod N, the i-th digits are A + je mod N with e ≢ 0 mod N.
- Monochromatic tuples ⇒ C constant on that cyclic progression ⇒ contradiction. This needs the hypothesis for EVERY d ≠ 0 in Z/NZ, including wrapping and repeated-term progressions. Theorem 6.3 supplies exactly that ("no progression … with $d\ne0$ in $\Z/N\Z$"). The control in §9.2 shows the hypothesis cannot be weakened to non-wrapping progressions.
- "Translation by one" (n ↦ n+1) maps [0,N^m) progressions with d > 0 bijectively onto [N^m] progressions with a, d ≥ 1. The conclusion W > N^m uses monotonicity and finiteness (Obj. 1).
- m = ⌊log₂ r⌋ ≥ 1 and 2^m ≤ r; inject the tuples into [r]. Fewer than r colours are allowed. ✓

**Proof of Theorem 1.1: VERIFIED.** N = q^D ≥ P > k ≥ 2 (unstated but immediate). W_r(k) > N^{⌊log₂ r⌋} ≥ k^{ck⌊log₂ r⌋}. "The threshold on $k$ was fixed before $r$ was introduced": ✓.

**Thm 7.2 transfer:large-r: VERIFIED LINE BY LINE.**
- r ≥ 256 gives b = ⌊r^{1/4}⌋ ≥ 4 (paper says ≥ 2; true) and s = ⌊log₂ r/4⌋ ≥ 2.
- H_0 = {0..⌈b/2⌉−1} and H_1 = {⌈b/2⌉..b−1} partition the digits, with diameters ⌈b/2⌉−1 and ⌊b/2⌋−1.
- Colours: 2^s(1+s(b−1)²) of them.
- (7.3): 1+sb² ≤ (s+1)b² (since b ≥ 1, unstated) ≤ (s+1)r^{1/2}; s+1 ≤ 2^s ≤ r^{1/4}; product ≤ r. ✓
- (7.4): the midpoint relation Σ(x_i − 2y_i + z_i)b^i = 0 with |x_i − 2y_i + z_i| ≤ 2(⌈b/2⌉−1) ≤ b−1 < b, so the carry-free induction gives x + z = 2y.
- Parallelogram: ‖x−z‖² = 2‖x‖² + 2‖z‖² − ‖x+z‖² = 0. So x = z, y = x, and the integers are equal. Every k ≥ 3 progression contains a 3-AP.
- L = log r ≥ 8 log 2. ⌊u⌋ ≥ u/2 at u = L/(4 log 2) ≥ 2 and at u = r^{1/4} ≥ 4. So s ≥ L/(8 log 2) and log b ≥ L/4 − log 2 ≥ L/8 (⇔ L ≥ 8 log 2). Then log b^s ≥ L²/(64 log 2), and W > b^s gives the strict inequality.
- `behrend_check.py` (§9.3) brute-forces 10 values of r and sweeps every integer r ∈ [256, 2×10^6] plus the jump points exactly, with three failing controls.

**Cor 7.3 transfer:limits: VERIFIED LINE BY LINE.**
- ⌊log₂ r⌋ ≥ log₂ r/2 for r ≥ 2. log W_r(k) > ck⌊log₂ r⌋ log k ≥ (c/(2 log 2)) k log k log r. Infimum ≥ (c/(2 log 2)) log k → ∞.
- log W_r(k)/log r > log r/(64 log 2) uniformly over k ≥ 3.
- W_r(k)^{1/k} > k^{c⌊log₂ r⌋}.
- log(W_r(k)/r^A) > L²/(64 log 2) − AL → ∞.
- "The restrictions on the parameters are necessary": k ∈ {1,2} gives ratio 0 or → 1, and r = 1 gives log r = 0. ✓

## 7A. Appendix (08-upper.tex) line by line: Thm A.1 upper:finite — VERIFIED LINE BY LINE

- **Recursion and well-foundedness.** F(·,k) uses only F(·,k−1), and m_t is a finite positive integer.
- **Boundary values.** W_r(1) = 1 (a singleton is a 1-term progression). W_r(2) = r+1 (pigeonhole on r+1 points gives two equal colours at distance d ≥ 1; the injective colouring of [r] avoids). W_1(k) = k ([k] contains 1..k; [k−1] has no k-term AP since a+(k−1)d ≥ k).
- **Focus.** In an avoiding colouring the focus colour differs from every arm colour, since the arm f−(k−1)d_i, …, f−d_i together with f is a k-AP of difference d_i > 0.
- **Inner step.**
  - Set m = m_t and B = F(r^m, k−1). Split [2mB] into 2B blocks and colour each block by its word (≤ r^m words).
  - The outer induction at length k−1, applied to blocks 1..B, gives b, Δ ≥ 1 with b + (k−2)Δ ≤ B.
  - Since k−2 ≥ 1, Δ ≤ B−1 (because b ≥ 1). So q = b + (k−1)Δ ≤ 2B−1 < 2B, and the block exists.
  - The common word avoids, being a translate of a sub-interval, so the inner hypothesis gives a focus f with t arms and colour a_0 ≠ a_i.
  - New focus f' = (q−1)m + f. Check: f' − s(mΔ + d_i) = (b + (k−1−s)Δ − 1)m + (f − sd_i), for s = 1..k−1. These sit in matching blocks b, …, b+(k−2)Δ at offsets in [m], with colour a_i. The new arm f' − smΔ has colour a_0.
  - All t+1 colours are distinct, all differences are positive, and all points lie in [1, Bm]. Since f' ≤ 2mB, f' is a focus with t+1 colours.
- **Conclusion.** At t = r an r-colouring cannot give the focus a colour outside r distinct arm colours, so F(r,k) = m_r is Ramsey. ✓
- **Lean.** `UpperBound.lean` defines `focusSize previous r (t+1) = 2 * focusSize … t * previous (r ^ focusSize … t)` and `Fcore (k+3) r = focusSize (Fcore (k+2)) r r`, the identical recursion. `finite_ramsey` supplies the nonemptiness `W` needs (§8 below).
- **Brute force.** `upper_check.py` (§9.5) checks the boundary values and W_2(3) = 9 ≤ F(2,3) = 780.

## 8. Lean statement reading (plain words; no lean run)

The definitions in `ComparatorChallenges/QuantitativeVanDerWaerden.lean` are byte-identical to `Model.lean` (diff, lines 1–21), and the theorem statement is byte-identical to `Main.lean` lines 11–14 (diff). The comparator manifest checks `OAI.QuantitativeVanDerWaerden.uniform_lower_bound` with axioms {propext, Quot.sound, Classical.choice}. Grep found no `sorry`, `axiom`, `admit` or `native_decide` in `ProgressionColoring/`.

- **`MonoAP c k a d`** — for every j < k, c(a + j·d) = c(a). The k terms a, a+d, …, a+(k−1)d all share a's colour.
- **`HasMonoAP c k N`** — there are naturals a ≥ 0 and d > 0 with a + (k−1)d < N and MonoAP c k a d. That is, c restricted to {0,…,N−1} has a monochromatic k-term AP with positive difference. (With natural subtraction at k = 0 this degenerates to "N ≥ 1".)
- **`IsRamsey α k N`** — every colouring c : ℕ → α has HasMonoAP c k N. Only the values on {0,…,N−1} matter; `isRamsey_iff_finite` proves the equivalence with colourings Fin N → α.
- **`W r k`** — sInf {N : 0 < N ∧ IsRamsey (Fin r) k N}. This is the least positive N such that every colouring of {0,…,N−1} by elements of Fin r (r colours, not all required) has a monochromatic k-AP. It is 0 if no such N exists.
- **`uniform_lower_bound`** — there is a natural K such that for every k ≥ K and every r ≥ 2, the real number k^{(1/100000)·k·Nat.log 2 r} is strictly less than W r k.
- **`kthRoot_tendsto`** (hr : 2 ≤ r) — the real sequence (W r k)^{1/k} tends to +∞ as k → ∞ over ℕ.
- **`CyclicLowerBound c`** (UniformTransfer.lean) — there is K such that for every k ≥ K there are a natural N ≥ 2 with k^{ck} ≤ N and a Boolean colouring C of ZMod N satisfying `CyclicAvoids C k`. That predicate is: for all a and all d ≠ 0, it is not the case that C(a + j·d) = C(a) for all j < k (wrapping and repeated terms included).
- **`exists_cyclic_coloring`** — CyclicLowerBound (1/100000), unfolded.

**Is `W r k` the paper's W_r(k)?** Yes, for r ≥ 1 and k ≥ 1.
- 0-based vs 1-based: n ↦ n+1 carries {0..N−1} with a ≥ 0, a+(k−1)d < N onto [N] with a ≥ 1, a+(k−1)d ≤ N.
- ℕ → Fin r vs [N] → [r]: restriction and extension, Fin r nonempty.
- "Fewer than r colours allowed": neither side demands surjectivity.
- k = 0 or r = 0 cases (W r 0 = 1, W 0 k = 1) are never reached.

**Can the theorem be vacuous?** No. If the set were empty, W r k = sInf ∅ = 0, and the conclusion k^{…} < 0 would be FALSE, because a real power of k ≥ 2 is positive. So proving it forces nonemptiness, i.e. van der Waerden's theorem for (r,k). The Lean gets this from `finite_ramsey` (UpperBound.lean, the twin of Thm A.1), consumed by `cyclic_binary_color_lower` through `lt_W_of_not_isRamsey`. This is exactly where the Appendix's finiteness enters.

**Could the formal statement be weaker than Thm 1.1?** No.
- `Nat.log 2 r` = ⌊log₂ r⌋ (proved in Growth.lean `natLog_two_eq_floor_log`; Main.lean also restates it with the real floor as `uniform_lower_bound_floor`).
- c = 1/100000 = 10^{−5} exactly (real division).
- The quantifier order ∃K ∀k ≥ K ∀r ≥ 2 is the paper's order.
- Real powers at k = 0, 1 are irrelevant: K is existential, and at k = 1 the inequality 1 < W r 1 = 1 is false anyway, so every valid K is ≥ 2 (the proof takes `max K 2`). For k ≥ 2 rpow is the ordinary power.
- Strict < matches ">".

**Is `kthRoot_tendsto` erdosproblems.com/138's question at r = 2?** Yes. The page says: "Let the van der Waerden number $W(k)$ be such that whenever $N\geq W(k)$ and $\{1,\ldots,N\}$ is $2$-coloured there must exist a monochromatic $k$-term arithmetic progression. … prove that $W(k)^{1/k}\to \infty$." By monotonicity (`IsRamsey.mono`), "least N such that all N' ≥ N are Ramsey" equals "least N Ramsey", which is W 2 k. The Lean gives the full limit, which is stronger than Fox–Hunter's paraphrase "lim sup … = ∞".

**Is `exists_cyclic_coloring` Theorem perturb:cyclic?** Yes, as the conclusion with N existentially quantified: the Lean witness is `ConstructionModel.groupSize s` = q^D (CyclicWitness.lean l.103–104). The internal budget (l.95–98) is literally the paper's R_k + A_k < 1:
`2·N²·p^{⌈k/400⌉} + 2·|affine signatures|·(1−p)^{⌈k/4⌉} < 1`
Here ⌈k/400⌉ = ⌈γk/4⌉, the rich condition `k ≤ 100·|opposite positions|` is "≥ γk positions of colour 1−b", and key multiplicity ≤ 4 is `construction_key_fiber_card_le_four`.

**Digit product in the Lean** (`DigitProduct.lean`) mirrors Prop 7.1 exactly: `exists_base_factor` is the largest i with N^i | d and N ∤ e; `div_ap_of_base_factor` is (7.1); `digitColor` is n ↦ (C(⌊n/N^i⌋ mod N))_i.

## 9. Finite checks (scripts VERBATIM, outputs, failing controls)

All under `/tmp/oaimath/160/seats/whole_checks/`. Run with `python3 -I`. Each takes under 7 s and under 100 MB.

### 9.1 thresholds.py — every large-k inequality with the paper's explicit constants (feeds §4)

```python
#!/usr/bin/env python3
"""Every 'for sufficiently large k' inequality of the paper, evaluated with the
paper's own explicit bounds (log lambda <= h0 log 2M; q <= 2k^2 k^{ck/D};
R <= (D+1) log q; T_glob <= [9(3k^2F+1)^2]^{2D}; C_0 = 9*16005^2, C = C_0^{1/3};
arrangement constant in dim 3: 16(s+1)^3 <= 128 s^3).
Reports, for each inequality, the last k (on a grid) at which it FAILS and
checks it holds on the whole grid beyond that, up to k = 10^300.
No quantity depends on r or on the progression: r never appears below."""
import math, sys

def iroot_floor(n, e):
    # integer Newton: largest x with x**e <= n
    if n < 2: return n
    x = 1 << ((n.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + n // x ** (e - 1)) // e
        if y >= x: break
        x = y
    while x ** e > n: x -= 1
    while (x + 1) ** e <= n: x += 1
    return x

def iroot_ceil(n, e):
    # smallest x with x**e >= n
    x = iroot_floor(n, e)
    return x if x ** e == n else x + 1

c, delta, gamma = 1e-5, 0.1, 0.01
C0 = 9 * 16005 ** 2
Ccl = C0 ** (1 / 3)          # count:local constant
LN2 = math.log(2)

def logaddexp(a, b):
    m = max(a, b); return m + math.log(math.exp(a - m) + math.exp(b - m))

def params(k):
    D = iroot_ceil(k, 10); M = iroot_ceil(k, 2); h0 = D * D
    lk = math.log(k)
    loglam = h0 * math.log(2 * M)                    # setup:dilation bound
    logq = (c * k / D) * lk + math.log(2 * k * k)    # setup:q-bounds upper
    R = (D + 1) * logq                               # mesh:width
    logm = logaddexp(2 * lk + math.log(R), 0.0)      # m <= k^2 R + 1
    logF = logaddexp(2 * lk + loglam, math.log(2) + logm)
    log3k2F1 = logaddexp(math.log(3) + 2 * lk + logF, 0.0)
    logTglob = 2 * D * (math.log(9) + 2 * log3k2F1)  # count:global
    return D, M, h0, lk, loglam, logq, logTglob

def ineqs(k):
    D, M, h0, lk, loglam, logq, logTglob = params(k)
    H = 1.0 / k ** 2 if k < 10 ** 150 else 0.0
    eta = 1 / (1000 * D)
    out = {}
    out['S1 h0<2M<k (sec2 l.21)'] = h0 < 2 * M < k
    out['S2 prime: k^2 log4 - log(2k^2+1) > k log(2k^2)'] = (k * k * math.log(4) - math.log(2 * k * k + 1) > k * math.log(2 * k * k)) if k < 10**100 else (math.exp(lk) * math.log(4) - (math.log(3) + 2 * lk) / math.exp(lk) > LN2 + 2 * lk)
    out['S3 h0<k (gcd(lambda,q)=1)'] = h0 < k
    out['S4 alpha<=1/4, R>=1, H<=1 (mesh:width)'] = (logq > 0) and k >= 1
    out['S6 H<=1/8 and 3w<=6H<1 (mesh:neighbors)'] = k * k >= 8
    out['C2 6H<1, 4H<1 (count:local ranges)'] = k * k > 6
    out['O1+O4 incident weight <= 1/500'] = None   # filled below
    first_log = lk + logTglob - (delta * float(M) - 1) / 32
    out['O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000'] = first_log < math.log(1 / 1000)
    out['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})'] = 6 * math.log(Ccl * D ** 3) / D <= 1 / 128
    sec_log = -(h0 + 1) / 128 - math.log(1 - math.exp(-1 / 128))
    out['O4 sum_{h>D^2} e^{-h/128} <= 1/1000'] = sec_log < math.log(1 / 1000)
    out['O1+O4 incident weight <= 1/500'] = out['O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000'] and out['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})'] and out['O4 sum_{h>D^2} e^{-h/128} <= 1/1000']
    out['O5 l(E)>=100: dM-1>=100 and (D^2+1)/2>=100'] = (delta * M - 1 >= 100) and ((h0 + 1) / 2 >= 100)
    out['O2 log(CDh)/h decreasing for h>=D^2 (CD^3>e)'] = Ccl * D ** 3 > math.e
    out['D1 2kH<1 (affinity)'] = 2 * k < k * k
    out['D2 m*-1>=k/(2M) (needs k>=2M)'] = k >= 2 * M
    out['D3 6MH/k<1 (v=lambda u)'] = 6 * M < k ** 3
    out['D4 4MH<1 ((1-2MH)/2M > H)'] = 4 * M < k * k
    out['D5 2H+4MH<1 (heavy-width)'] = 2 + 4 * M < k * k
    out['D7 4MH < 1/2 (short-motion, h>=1)'] = 8 * M < k * k
    out['D8 2H(k+1)<1 (short width)'] = 2 * (k + 1) < k * k
    out['D10 4MH/k < eta (long, drift<eta)'] = 4 * M * 1000 * D < k ** 3
    out['D11 D(4eta+1/h0)<1/2'] = 4 / 1000 + 1 / D < 0.5
    out['D12 2M<=k and 4M<=k (|u|<=Hx,|v|<=H)'] = 4 * M <= k
    out['D13 2M/k<=1/16'] = 32 * M <= k
    out['D14 k-h-dk>=4k/5 (h<=2M<=k/10)'] = 20 * M <= k
    out['P1 p<1/2 (k^{1/20}>2)'] = k > 2 ** 20
    logR = LN2 + 2 * D * logq - (gamma / 80) * math.exp(lk) * lk
    logA = LN2 + math.log(128) + logTglob + 3 * (lk + math.log(3 * D) + 2 * logq) - math.exp(0.95 * lk) / 4
    out['P2r rich: log R_k < log(1/2)'] = logR < -LN2
    out['P2a affine: log A_k < log(1/2)'] = logA < -LN2
    return out

# exact scan for small k, grid scan beyond
names = list(ineqs(10 ** 7).keys())
last_fail = {n: None for n in names}
for k in range(3, 20001):
    for n, v in ineqs(k).items():
        if not v: last_fail[n] = k
x = 4.30
while x <= 300:
    k = int(10 ** x) if x < 15 else int(round(10 ** (x - 15))) * 10 ** 15
    for n, v in ineqs(k).items():
        if not v: last_fail[n] = k
    x += 0.01
w = max(len(n) for n in names)
print(f"{'inequality':<{w}}  last failing k on grid (k=3..2e4 exact, then 10^4.3..10^300 step 10^0.01)")
for n in names:
    lf = last_fail[n]
    s = 'never fails (k>=3)' if lf is None else (f'{lf}' if lf < 10 ** 7 else f'~10^{math.log10(lf):.2f}')
    print(f"{n:<{w}}  {s}")
# the binding constraint, located more finely
lo, hi = 40.0, 46.0
for _ in range(60):
    mid = (lo + hi) / 2
    k = int(round(10 ** (mid - 15))) * 10 ** 15
    if ineqs(k)['O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})']: hi = mid
    else: lo = mid
k = int(round(10 ** (hi - 15))) * 10 ** 15
print(f"O3 threshold: k ~ 10^{hi:.3f}, D = {params(k)[0]}, C = {Ccl:.1f}")
```

Output:
```
inequality                                             last failing k on grid (k=3..2e4 exact, then 10^4.3..10^300 step 10^0.01)
S1 h0<2M<k (sec2 l.21)                                 6
S2 prime: k^2 log4 - log(2k^2+1) > k log(2k^2)         never fails (k>=3)
S3 h0<k (gcd(lambda,q)=1)                              4
S4 alpha<=1/4, R>=1, H<=1 (mesh:width)                 never fails (k>=3)
S6 H<=1/8 and 3w<=6H<1 (mesh:neighbors)                never fails (k>=3)
C2 6H<1, 4H<1 (count:local ranges)                     never fails (k>=3)
O1+O4 incident weight <= 1/500                         ~10^44.65
O1 first-family total kTglob e^{-(dM-1)/32} <= 1/1000  ~10^22.70
O3 6 log(C D^3)/D <= 1/128 (summand <= e^{-h/128})     ~10^44.65
O4 sum_{h>D^2} e^{-h/128} <= 1/1000                    ~10^15.78
O5 l(E)>=100: dM-1>=100 and (D^2+1)/2>=100             ~10^11.46
O2 log(CDh)/h decreasing for h>=D^2 (CD^3>e)           never fails (k>=3)
D1 2kH<1 (affinity)                                    never fails (k>=3)
D2 m*-1>=k/(2M) (needs k>=2M)                          5
D3 6MH/k<1 (v=lambda u)                                never fails (k>=3)
D4 4MH<1 ((1-2MH)/2M > H)                              never fails (k>=3)
D5 2H+4MH<1 (heavy-width)                              3
D7 4MH < 1/2 (short-motion, h>=1)                      4
D8 2H(k+1)<1 (short width)                             never fails (k>=3)
D10 4MH/k < eta (long, drift<eta)                      38
D11 D(4eta+1/h0)<1/2                                   1024
D12 2M<=k and 4M<=k (|u|<=Hx,|v|<=H)                   19
D13 2M/k<=1/16                                         1055
D14 k-h-dk>=4k/5 (h<=2M<=k/10)                         419
P1 p<1/2 (k^{1/20}>2)                                  1047128
P2r rich: log R_k < log(1/2)                           154881
P2a affine: log A_k < log(1/2)                         7238
O3 threshold: k ~ 10^44.655, D = 29210, C = 1321.0
```

Control: `cap_check.py` (§9.4) is the failing control for this machinery. With c = 7×10⁻⁵ the rich inequality P3 fails at every k. Within this run, S1/S3/D2/D5/D7/D10–D14/P1–P4 visibly FAIL below their thresholds, so the predicates can fail.

### 9.2 digit_product_check.py — Prop transfer:product (7.1) by brute force

```python
#!/usr/bin/env python3
"""Brute-force check of Prop transfer:product (07-transfers.tex) on tiny cyclic colourings.
(1) find 2-colourings C of Z/NZ with no monochromatic a, a+d, ..., a+(k-1)d (d != 0 mod N,
    wrap-around allowed, repeated terms allowed) -- the hypothesis of the proposition;
(2) build the digit-product colouring n -> (C(floor(n/N^i) mod N))_{i<m} of [0, N^m) and
    brute-force every progression a, a+d, ..., a+(k-1)d with d >= 1 inside [0, N^m);
CONTROL A (must FAIL): a colouring of Z/NZ that avoids every NON-wrapping k-AP in {0..N-1}
    but has a wrapping cyclic mono k-AP; its digit product must contain a mono k-AP.
CONTROL B (must FAIL): identity (transfer:division) with N^i NOT dividing d.
EXTERNAL CONTROL: W_2(3) = 9, so no cyclic 3-AP-free 2-colouring of Z/9Z ... Z/12Z may exist."""
import itertools, random, sys

def cyclic_avoids(C, N, k):
    for a in range(N):
        for d in range(1, N):
            c0 = C[a]
            if all(C[(a + j * d) % N] == c0 for j in range(1, k)):
                return False
    return True

def interval_avoids(col, L, k):
    for a in range(L):
        for d in range(1, (L - 1 - a) // (k - 1) + 1 if k > 1 else 1):
            c0 = col[a]
            if all(col[a + j * d] == c0 for j in range(1, k)):
                return (a, d)
    return None

def digit_colour(C, N, m):
    out = []
    for n in range(N ** m):
        out.append(tuple(C[(n // N ** i) % N] for i in range(m)))
    return out

def search(N, k, limit=4):
    found = []
    for bits in range(1 << (N - 1)):          # fix C[0]=0 (colour swap symmetry)
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if cyclic_avoids(C, N, k):
            found.append(C)
            if len(found) >= limit: break
    return found

print("EXTERNAL CONTROL (W_2(3)=9): cyclic 3-AP-free 2-colourings of Z/NZ, N=3..12:")
for N in range(3, 13):
    print(f"  N={N}: {'some' if search(N, 3, 1) else 'none'}")

for (N, k, ms) in [(3, 3, (1, 2, 3, 4, 5)), (4, 3, (1, 2, 3, 4)), (11, 4, (1, 2, 3))]:
    cols = search(N, k, 2)
    if not cols:
        print(f"N={N},k={k}: no cyclic avoiding colouring found"); continue
    C = cols[0]
    for m in ms:
        bad = interval_avoids(digit_colour(C, N, m), N ** m, k)
        print(f"N={N},k={k},C={''.join(map(str,C))},m={m}: interval [0,{N**m}) with 2^{m} colours: "
              f"{'NO mono k-AP (W_{2^m}(k) > N^m)' if bad is None else 'MONO AP FOUND ' + str(bad)}")

print("\nCONTROL A: colourings avoiding all NON-wrapping k-APs on {0..N-1} but not cyclically:")
for (N, k) in [(8, 3), (16, 4)]:
    ctrl = None
    for bits in range(1 << (N - 1)):
        C = [0] + [(bits >> i) & 1 for i in range(N - 1)]
        if interval_avoids(C, N, k) is None and not cyclic_avoids(C, N, k):
            ctrl = C; break
    if ctrl is None:
        print(f"  N={N},k={k}: none found"); continue
    for m in (2,):
        bad = interval_avoids(digit_colour(ctrl, N, m), N ** m, k)
        print(f"  N={N},k={k},C={''.join(map(str,ctrl))},m={m}: digit product "
              f"{'has NO mono AP (control did not fail!)' if bad is None else 'has mono k-AP (a,d)=' + str(bad) + '  [control FAILS as it must]'}")

print("\nIdentity (transfer:division): floor((a+jd)/N^i) == floor(a/N^i) + j*d/N^i")
random.seed(1)
ok = bad = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(0, 3); e = random.randint(1, 50)
    d = N ** i * e; a = random.randint(0, 10 ** 6); j = random.randint(0, 40)
    ok += ((a + j * d) // N ** i == a // N ** i + j * e)
print(f"  N^i | d: {ok}/20000 hold")
fails = 0
for _ in range(20000):
    N = random.randint(2, 12); i = random.randint(1, 3); d = random.randint(1, 10 ** 4)
    if d % N ** i == 0: continue
    a = random.randint(0, 10 ** 6); j = random.randint(1, 40)
    # with N^i not dividing d, j*d/N^i is not an integer for j=1: the identity cannot hold
    if (a + j * d) // N ** i * N ** i != (a // N ** i) * N ** i + j * d: fails += 1
print(f"  CONTROL B (N^i does not divide d): identity fails in {fails} random cases [must be > 0]")
```

Output:
```
EXTERNAL CONTROL (W_2(3)=9): cyclic 3-AP-free 2-colourings of Z/NZ, N=3..12:
  N=3: some
  N=4: some
  N=5: none
  N=6: none
  N=7: none
  N=8: none
  N=9: none
  N=10: none
  N=11: none
  N=12: none
N=3,k=3,C=010,m=1: interval [0,3) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=2: interval [0,9) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=3: interval [0,27) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=4: interval [0,81) with 2^4 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=3,k=3,C=010,m=5: interval [0,243) with 2^5 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=1: interval [0,4) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=2: interval [0,16) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=3: interval [0,64) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=4,k=3,C=0110,m=4: interval [0,256) with 2^4 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=1: interval [0,11) with 2^1 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=2: interval [0,121) with 2^2 colours: NO mono k-AP (W_{2^m}(k) > N^m)
N=11,k=4,C=01110100100,m=3: interval [0,1331) with 2^3 colours: NO mono k-AP (W_{2^m}(k) > N^m)

CONTROL A: colourings avoiding all NON-wrapping k-APs on {0..N-1} but not cyclically:
  N=8,k=3,C=01011010,m=2: digit product has mono k-AP (a,d)=(0, 21)  [control FAILS as it must]
  N=16,k=4,C=0010110101001000,m=2: digit product has mono k-AP (a,d)=(0, 8)  [control FAILS as it must]

Identity (transfer:division): floor((a+jd)/N^i) == floor(a/N^i) + j*d/N^i
  N^i | d: 20000/20000 hold
  CONTROL B (N^i does not divide d): identity fails in 16340 random cases [must be > 0]
```

Controls: (A) colourings avoiding every NON-wrapping k-AP in {0..N−1} but not cyclically produce a monochromatic k-AP in the digit product. For example, N = 16, k = 4: (a,d) = (0,8), whose lowest digits 0,8,0,8 form a wrapping, repeated-term cyclic progression with step 8. This shows the cyclic hypothesis must cover every d ≠ 0, which Theorem 6.3 provides. (B) Identity (7.1) fails whenever N^i ∤ d. External control: W_2(3) = 9 forbids cyclic 3-AP-free 2-colourings of Z/NZ for N ≥ 9, and the search finds none.

### 9.3 behrend_check.py — Thm transfer:large-r (7.2) by brute force + exact sweep

```python
#!/usr/bin/env python3
"""Brute-force + exact checks of Theorem transfer:large-r (07-transfers.tex, printed Thm 7.2).
(1) For r in a list: b = floor(r^{1/4}), s = floor(log r / (4 log 2)); colour n in [0, b^s) by
    (h(x_0),...,h(x_{s-1}), sum x_i^2); check #colours used <= 2^s(1+s(b-1)^2) <= r and that NO
    colour class contains a 3-AP n, n+d, n+2d (d >= 1).
CONTROL 1 (must FAIL): halves H_0 = {0..ceil(b/2)} (diameter one larger) -> mono 3-AP expected.
CONTROL 2 (must FAIL): drop the squared-norm entry -> mono 3-AP expected.
(2) Exact arithmetic of (transfer:color-count), s >= L/(8 log 2), log b >= L/8 and
    b^s > exp(L^2/(64 log 2)) for EVERY integer r in [256, 2*10^6] and for r = 2^j, 2^j - 1,
    j <= 400 (where floors jump)."""
import math

def iroot_floor(n, e):
    if n < 2: return n
    x = 1 << ((n.bit_length() + e - 1) // e)
    while True:
        y = ((e - 1) * x + n // x ** (e - 1)) // e
        if y >= x: break
        x = y
    while x ** e > n: x -= 1
    while (x + 1) ** e <= n: x += 1
    return x

def params(r):
    b = iroot_floor(r, 4)
    s = (r.bit_length() - 1) // 4          # floor(floor(log2 r)/4) = floor(log r/(4 log 2))
    return b, s

def colouring(b, s, half_cut, with_norm=True):
    cols = []
    for n in range(b ** s):
        x, t = [], n
        for _ in range(s):
            x.append(t % b); t //= b
        hv = tuple(int(xi >= half_cut) for xi in x)
        cols.append(hv + ((sum(xi * xi for xi in x),) if with_norm else ()))
    return cols

def mono_3ap(cols):
    classes = {}
    for n, c in enumerate(cols): classes.setdefault(c, []).append(n)
    for c, mem in classes.items():
        S = set(mem)
        for i in range(len(mem)):
            for j in range(i + 1, len(mem)):
                a, z = mem[i], mem[j]
                if (a + z) % 2 == 0 and (a + z) // 2 in S:
                    return (a, (a + z) // 2, z), len(classes)
    return None, len(classes)

for r in [256, 400, 625, 1296, 2401, 4096, 6561, 10000, 65536, 100000]:
    b, s = params(r)
    hc = (b + 1) // 2                      # ceil(b/2): H_0 = {0..ceil(b/2)-1}
    bound = 2 ** s * (1 + s * (b - 1) ** 2)
    if b ** s > 300000:
        print(f"r={r}: b={b}, s={s}, b^s={b**s} too large to brute force here"); continue
    w, ncol = mono_3ap(colouring(b, s, hc))
    w1, _ = mono_3ap(colouring(b, s, hc + 1))
    w2, _ = mono_3ap(colouring(b, s, hc, with_norm=False))
    lb = math.exp(math.log(r) ** 2 / (64 * math.log(2)))
    print(f"r={r}: b={b}, s={s}, interval [0,{b**s}), colours used {ncol} <= {bound} <= r: {ncol <= bound <= r}; "
          f"mono 3-AP: {w}; claimed bound exp(L^2/64log2)={lb:.3f} < b^s: {lb < b**s} | "
          f"CONTROL1 wide halves -> {w1} | CONTROL2 no norm -> {w2}")

# (2) exact arithmetic over all r in a range and at the jump points
bad = []
def check(r):
    b, s = params(r)
    L = math.log(r)
    ok = (2 ** s * (1 + s * b * b) <= r and s >= L / (8 * math.log(2)) - 1e-12
          and math.log(b) >= L / 8 - 1e-12 and s * math.log(b) >= L * L / (64 * math.log(2)) - 1e-9
          and b >= 2 and s >= 1)
    if not ok: bad.append(r)
for r in range(256, 2_000_001):
    check(r)
for j in range(8, 401):
    for r in (2 ** j - 1, 2 ** j, 2 ** j + 1):
        if r >= 256: check(r)
for t in range(4, 10 ** 4):
    for r in (t ** 4 - 1, t ** 4):
        if r >= 256: check(r)
print(f"\nexact-arithmetic sweep r in [256, 2e6] plus jump points: failures = {bad[:10]} (count {len(bad)})")
# CONTROL 3a (must FAIL): claim the stronger constant 16 log 2 instead of 64 log 2
f3a = [r for r in range(256, 200001) if params(r)[1] * math.log(params(r)[0]) < math.log(r) ** 2 / (16 * math.log(2))]
print(f"CONTROL3a (b^s >= exp(L^2/(16 log 2)) claimed): fails at {len(f3a)} r in [256,2e5], first {f3a[:3]}")
# CONTROL 3b (must FAIL): b = floor(r^{1/3}) instead of r^{1/4} breaks (transfer:color-count)
f3b = [r for r in range(256, 200001) if 2 ** ((r.bit_length()-1)//4) * (1 + ((r.bit_length()-1)//4) * iroot_floor(r, 3) ** 2) > r]
print(f"CONTROL3b (b = floor(r^(1/3))): colour count exceeds r at {len(f3b)} r in [256,2e5], first {f3b[:3]}")
```

Output:
```
r=256: b=4, s=2, interval [0,16), colours used 14 <= 76 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.000 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> None
r=400: b=4, s=2, interval [0,16), colours used 14 <= 76 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.246 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> None
r=625: b=5, s=2, interval [0,25), colours used 21 <= 132 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=2.545 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=1296: b=6, s=2, interval [0,36), colours used 30 <= 204 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=3.183 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=2401: b=7, s=2, interval [0,49), colours used 38 <= 292 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=3.919 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=4096: b=8, s=3, interval [0,512), colours used 243 <= 1184 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=4.757 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=6561: b=9, s=3, interval [0,729), colours used 322 <= 1544 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=5.705 < b^s: True | CONTROL1 wide halves -> (46, 86, 126) | CONTROL2 no norm -> (0, 1, 2)
r=10000: b=10, s=3, interval [0,1000), colours used 435 <= 1952 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=6.768 < b^s: True | CONTROL1 wide halves -> None | CONTROL2 no norm -> (0, 1, 2)
r=65536: b=16, s=4, interval [0,65536), colours used 5124 <= 14416 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=16.000 < b^s: True | CONTROL1 wide halves -> (24, 2064, 4104) | CONTROL2 no norm -> (0, 1, 2)
r=100000: b=17, s=4, interval [0,83521), colours used 5853 <= 16400 <= r: True; mono 3-AP: None; claimed bound exp(L^2/64log2)=19.844 < b^s: True | CONTROL1 wide halves -> (154, 298, 442) | CONTROL2 no norm -> (0, 1, 2)

exact-arithmetic sweep r in [256, 2e6] plus jump points: failures = [] (count 0)
CONTROL3a (b^s >= exp(L^2/(16 log 2)) claimed): fails at 199742 r in [256,2e5], first [257, 258, 259]
CONTROL3b (b = floor(r^(1/3))): colour count exceeds r at 142575 r in [256,2e5], first [256, 257, 258]
```

Controls: CONTROL1 (halves widened by one digit) produces a monochromatic 3-AP at r = 6561, 65536 and 100000. CONTROL2 (norm entry dropped) produces one at every tested r with b ≥ 5; at b = 4 the halves {0,1} and {2,3} happen to be 3-AP-free. CONTROL3a (claiming exp(L²/(16 log 2))) fails at 199,742 values of r. CONTROL3b (b = ⌊r^{1/3}⌋) breaks (7.3) at 142,575 values of r. The true chain has 0 failures over r ∈ [256, 2×10⁶] plus all jump points.

### 9.4 cap_check.py — which inequality caps c (brief item j)

```python
#!/usr/bin/env python3
"""Which inequality caps c (brief item j)?  Rich case: log R_k <= log2 + 2D log q - (gamma/80) k log k
with D log q <= c k log k + D log(2k^2)  =>  needs 2c < gamma/80, i.e. c < gamma/160 = 6.25e-5.
Affine case: log T_aff ~ 6 log q ~ 6 (c k/D) log k = o(p k) for EVERY fixed c (D ~ k^{1/10} > k^{1/20}).
CONTROL (must FAIL): c = 7e-5 > gamma/160 -> rich bound positive at every large k."""
import math
gamma = 0.01
def logR(k_log10, c):
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return math.log(2) + 2 * D * logq - (gamma / 80) * k * lk
def logAff_main(k_log10, c):   # 6 log q - pk/4 (dominant c-dependent part of log A_k)
    lk = k_log10 * math.log(10); k = math.exp(lk)
    D = math.ceil(math.exp(lk / 10))
    logq = (c * k / D) * lk + math.log(2) + 2 * lk
    return 6 * logq - math.exp(0.95 * lk) / 4
for c in (1e-5, 6e-5, 6.2e-5, 7e-5, 1e-3):
    row = [f"{logR(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    aff = [f"{logAff_main(x, c):+.3e}" for x in (6, 10, 50, 100, 300)]
    print(f"c={c:g}: 2c-gamma/80={2*c-gamma/80:+.3e}; log R_k at k=10^6,10^10,10^50,10^100,10^300: {row}")
    print(f"        affine main term 6log q - pk/4 at same k: {aff}")
```

Output:
```
c=1e-05: 2c-gamma/80=-1.050e-04; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['-1.223e+03', '-2.418e+07', '-1.209e+48', '-2.418e+98', '-7.253e+298']
        affine main term 6log q - pk/4 at same k: ['-1.249e+05', '-7.893e+08', '-7.905e+46', '-2.500e+94', '-2.500e+284']
c=6e-05: 2c-gamma/80=-5.000e-06; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+1.582e+02', '-1.150e+06', '-5.756e+46', '-1.151e+97', '-3.454e+297']
        affine main term 6log q - pk/4 at same k: ['-1.239e+05', '-7.830e+08', '-7.902e+46', '-2.500e+94', '-2.500e+284']
c=6.2e-05: 2c-gamma/80=-1.000e-06; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+2.135e+02', '-2.292e+05', '-1.151e+46', '-2.303e+96', '-6.908e+296']
        affine main term 6log q - pk/4 at same k: ['-1.238e+05', '-7.828e+08', '-7.901e+46', '-2.500e+94', '-2.500e+284']
c=7e-05: 2c-gamma/80=+1.500e-05; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+4.345e+02', '+3.455e+06', '+1.727e+47', '+3.454e+97', '+1.036e+298']
        affine main term 6log q - pk/4 at same k: ['-1.237e+05', '-7.818e+08', '-7.901e+46', '-2.500e+94', '-2.500e+284']
c=0.001: 2c-gamma/80=+1.875e-03; log R_k at k=10^6,10^10,10^50,10^100,10^300: ['+2.613e+04', '+4.317e+08', '+2.159e+49', '+4.317e+99', '+1.295e+300']
        affine main term 6log q - pk/4 at same k: ['-1.044e+05', '-6.650e+08', '-7.837e+46', '-2.500e+94', '-2.500e+284']
```

Control: c = 7e-5 and c = 1e-3 give log R_k > 0 at every k shown (the rich bound FAILS as it must). The affine term stays negative for every c, so the cap 2c < γ/80 is the only one.

### 9.5 upper_check.py — Thm A.1 boundary values and W ≤ F

```python
#!/usr/bin/env python3
"""Theorem upper:finite (printed Thm A.1): compute F(r,k) from (A.1) literally and compare with
brute-force W_r(k) on tiny cases; check the boundary values W_r(1)=1, W_r(2)=r+1, W_1(k)=k.
W uses the paper's 1-based definition: least N such that every map [N]->[r] is constant on
some a, a+d, ..., a+(k-1)d with a,d >= 1, a+(k-1)d <= N.
CONTROL (must FAIL): the claim W_r(2) = r is rejected by the same brute force."""
import itertools
from functools import lru_cache

@lru_cache(None)
def F(r, k):
    if k == 1: return 1
    if k == 2: return r + 1
    m = 1
    for _ in range(r):
        m = 2 * m * F(r ** m, k - 1)
    return m

def has_mono(col, k):            # col: tuple indexed 1..N via col[n-1]
    N = len(col)
    for a in range(1, N + 1):
        for d in range(1, N + 1):
            if a + (k - 1) * d > N: break
            if all(col[a + j * d - 1] == col[a - 1] for j in range(k)): return True
    return False

def ramsey(N, r, k):
    return all(has_mono(col, k) for col in itertools.product(range(r), repeat=N))

def W(r, k, cap=12):
    for N in range(1, cap + 1):
        if ramsey(N, r, k): return N
    return None

print("F(r,k) small values:", {(r, k): F(r, k) for r in (1, 2) for k in (1, 2, 3)}, " F(1,4) =", F(1, 4))
res = []
for r in (1, 2, 3, 4):
    res.append((f"W_{r}(1)", W(r, 1), 1)); res.append((f"W_{r}(2)", W(r, 2), r + 1))
for k in (1, 2, 3, 4, 5):
    res.append((f"W_1({k})", W(1, k), k))
res.append(("W_2(3)", W(2, 3), 9))
for name, got, claim in res:
    print(f"{name}: brute force {got}, paper {claim}, {'OK' if got == claim else 'MISMATCH'}")
print("W_r(k) <= F(r,k):", all(W(r, k) <= F(r, k) for r, k in [(1, 3), (1, 4), (2, 3), (3, 2), (4, 2)]),
      "(W_2(3)=9 <= F(2,3)=%d)" % F(2, 3))
print("CONTROL claim W_r(2)=r:", ["rejected" if W(r, 2) != r else "ACCEPTED (bad)" for r in (1, 2, 3, 4)])
```

Output:
```
F(r,k) small values: {(1, 1): 1, (1, 2): 2, (1, 3): 4, (2, 1): 1, (2, 2): 3, (2, 3): 780}  F(1,4) = 8
W_1(1): brute force 1, paper 1, OK
W_1(2): brute force 2, paper 2, OK
W_2(1): brute force 1, paper 1, OK
W_2(2): brute force 3, paper 3, OK
W_3(1): brute force 1, paper 1, OK
W_3(2): brute force 4, paper 4, OK
W_4(1): brute force 1, paper 1, OK
W_4(2): brute force 5, paper 5, OK
W_1(1): brute force 1, paper 1, OK
W_1(2): brute force 2, paper 2, OK
W_1(3): brute force 3, paper 3, OK
W_1(4): brute force 4, paper 4, OK
W_1(5): brute force 5, paper 5, OK
W_2(3): brute force 9, paper 9, OK
W_r(k) <= F(r,k): True (W_2(3)=9 <= F(2,3)=780)
CONTROL claim W_r(2)=r: ['rejected', 'rejected', 'rejected', 'rejected']
```

Control: the false claim W_r(2) = r is rejected for r = 1..4.

Exact arithmetic (Fraction): 2c − γ/80 = −21/200000; 100·(1/8 − 1/32 − 2/500) = 100·359/4000 = 8.975 > log 2 = 0.693; γ/160 = 1/16000.

## 10. Citation table (my scope)

| Cited result | What the paper says it says | What the source says (quote) | Verdict |
|---|---|---|---|
| Fox–Hunter arXiv 2606.02541v1, Thm 1 | "$W_3(k)>2^{k\log^*k/4}$ for all sufficiently large $k$, where $\log^*k$ counts the iterations of the natural logarithm" | "Theorem 1. For k sufficiently large, w(k; 3) > 2^{k(log∗ k)/4}." log∗ = "the number of times the logarithm function must be iteratively applied to k before the result is at most 1" | MATCH ("natural" is the paper's gloss) |
| Fox–Hunter Thm 2 | "$W_r(k)\ge r^{(1-\varepsilon)k\log k}$ when $k$ is sufficiently large in terms of $\varepsilon$ and $r\ge(\log k)^{3/\varepsilon}$" | "Theorem 2. For each ε ∈ (0, 1) there exists k0(ε) so that the following holds. Suppose k ≥ k0(ε) and r ≥ (log k)^{3/ε}, then w(k; r) ≥ r^{(1−ε)k(log k)}." | MATCH |
| Fox–Hunter pp.2–3 | "covering an interval by translates of such sets already gives superpolynomial growth in the number of colors" | "if there is a set S ⊂ [N] with |S| ≥ εN with no k-term arithmetic progression, then we can use r = (3/ε) log2 N random translates of S to cover [N] … that there is c_k > 0 such that w(k; r) ≥ 2^{c_k (log r)^{⌈log k⌉}}" | MATCH |
| Fox–Hunter Section 2 (Erdős–Turán via least nonzero digit) | 07 l.7–9: "recalled, with the least-nonzero-digit argument, by Fox and Hunter [Section 2]" | "Erdős and Turán [16] gave the following simple construction … consider the position i of the least nonzero digit in base p of the common difference d." | MATCH |
| Fox–Hunter lcm dilations | "Least-common-multiple dilations in cyclic groups appear in Fox and Hunter" | Proof of Lemma 2.10: "Let ℓ = lcm(1, 2, …, ⌈1/ε⌉) … ℓ is invertible in Z_N … ℓ · I be the dilation of I by ℓ" | MATCH |
| Campos–Fox–Schildkraut arXiv 2608.20824v1, Thm 1 | "$W_2(k)\ge(1-o(1))k2^{k-1}$. They credit ChatGPT 5.6 Sol Pro with the coloring and an initial proof." | "Theorem 1. For every positive integer k we have w(k) ≥ (1 − o(1))k2^{k−1}." "The coloring used to prove Theorem 1, as well as a proof of Theorem 1, were generated by a query to ChatGPT 5.6 Sol Pro. The proof we present, while drawing somewhat on the proof given by ChatGPT, was produced by the authors." | MATCH |
| CFS settles W_2(k)/2^k | "Their result settles the question about $W_2(k)/2^k$" | "This verifies a conjecture of Erdős" (lim w(k)/2^k = ∞) | MATCH |
| Companion "Quasipolynomial Bounds for Arithmetic Progressions", Eq. (1.3) (fetched from github.com/openai/math main, sha256 481eaf7730dc…) | upper half of the intro display, r ≥ 256, A_k ≥ 1 | "Wr (k) ≤ ⌈exp(Ak (2 + log r)^{Ak})⌉ (r ≥ 1), (1.3) after increasing Ak … The companion paper [37, Theorem 7.2] gives the complementary lower bound Wr (k) > exp((log r)²/(64 log 2)) for all integers r ≥ 256 and k ≥ 3." | MATCH as a citation; content unrefereed (Obj. 3) |
| Erdős 1980 survey, p.90 (2) | "Erdős explicitly asked for this full limit in the two-color case" | "I offer 500 dollars for the proof or disproof of lim f(n)^{1/n} = ∞ (2)", with f(n) defined for "divide the integers 1 ≤ t ≤ f(n) into two classes" | MATCH |

(The remaining bib entries — Berlekamp, Szabó, Kozik–Shabanov, Hunter, Kelley–Meka, Leng–Sah–Sawhney, Stanley, Behrend, Rankin, Green–Wolf, Green, Shi–Dong, Shelah, Gowers, van der Waerden 1998 — belong to the `sources` seat. I did not check them.)

## 11. Status per lemma / proposition / equation

| Item | Status |
|---|---|
| 01-introduction.tex (all claims) | VERIFIED LINE BY LINE against the body and cited sources (§6, §10) |
| (setup:parameters), (setup:dilation-definition), Lemma 2.1 setup:dilation | VERIFIED LINE BY LINE |
| Lemma 2.2 setup:prime | VERIFIED LINE BY LINE (holds from k = 3; §4 S2) |
| (setup:q-bounds), gcd(λ,q)=1, (setup:orders), (setup:coordinates), U-partition, (mesh:definition), (mesh:intervals) | VERIFIED LINE BY LINE |
| Lemma 2.3 mesh:width, Lemma 2.4 mesh:neighbors, (mesh:truncation-definition), Lemma 2.5 mesh:truncated | VERIFIED LINE BY LINE (no numeric mesh build: that is the `setup` seat's job) |
| Lemma 3.1 count:arrangement | zero-sign reduction and final simplification VERIFIED; strict-region bound SKIMMED (classical, cited to Stanley, sketched) |
| Lemma 3.2 count:global | VERIFIED LINE BY LINE |
| Def 3.3 count:eligible, Lemma 3.4 count:local | VERIFIED LINE BY LINE (three cases, lift uniqueness, arithmetic h^{D+1}[C_0(Dh)²]^{2D} ≤ (CDh)^{6D} with C = C_0^{1/3}) |
| Lemma 4.1 outer:lll | VERIFIED LINE BY LINE |
| Prop 4.2 outer:coloring, (outer:row-size), (outer:tail), (outer:first-weight), (outer:second-weight), (outer:incident-weight), (outer:criterion) | VERIFIED LINE BY LINE (thresholds in §4) |
| Lemmas 5.1–5.4, Thm 5.5 (short and long cases) | VERIFIED LINE BY LINE (no small-model simulation: that is the `dichotomy` seat's job) |
| Lemma 6.1 perturb:multiplicity, (perturb:signature), Lemma 6.2 perturb:signatures, Thm 6.3 perturb:cyclic, (perturb:rich-bound), (perturb:negative-coefficient), (perturb:affine-bound) | VERIFIED LINE BY LINE (−21/200000 exact) |
| Prop 7.1 transfer:product, (7.1), proof of Thm 1.1 | VERIFIED LINE BY LINE + brute force with failing controls |
| Thm 7.2 transfer:large-r, (7.2)–(7.4) | VERIFIED LINE BY LINE + brute force + exact sweep with failing controls |
| Cor 7.3 transfer:limits | VERIFIED LINE BY LINE |
| Thm A.1 upper:finite, (A.1)–(A.3) | VERIFIED LINE BY LINE + brute force of boundary values |
| figures/norm-band.tex | NOT READ (illustration only) |
| Lean: Model, Main, UniformTransfer, CyclicWitness, LargeColorConsequences, CyclicBasic, DigitProduct, DigitProductBounds, Basic, UpperBound (F, finite_ramsey, W_two), comparator | statements READ and compared (§8); proofs not kernel-checked by me (replay running elsewhere; never ran lean/lake) |
| Lean: the remaining ~100 ProgressionColoring files | NOT READ |

## 12. Verdict for my scope

**HOLDS AS READ.**
- Theorem 1.1 follows from §2–§6 and Prop 7.1 through a dependency graph whose interfaces all match (§3).
- Every "sufficiently large k" inequality holds for all large k, and none is reversed (§4). K_0 is absolute and uniform in r, P and the progression. Under the paper's own constants K_0 ≈ 10^{44.7}, set by the outer:second-weight sup bound.
- The constant is capped only by 2c < γ/80 (§5). Nothing proves too much.
- §7 and the Appendix are correct.
- The Lean statement `uniform_lower_bound` is exactly Theorem 1.1, with no vacuity and no weakening.
- `kthRoot_tendsto` at r = 2 is exactly erdosproblems.com/138.
- The remaining issues are expository:
  - finiteness and monotonicity are unstated in §7;
  - 34 mislabelled "Theorem" cross-references;
  - the intro's "at most quasipolynomial" for k ≥ 4 rests on the unrefereed companion paper.
