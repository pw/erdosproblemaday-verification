
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
