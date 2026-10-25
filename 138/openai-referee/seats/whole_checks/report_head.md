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
