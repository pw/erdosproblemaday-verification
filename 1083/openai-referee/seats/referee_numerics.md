# Referee report — seat `numerics`

Paper: OpenAI, "The higher-dimensional Erdős distinct-distances conjecture" (23 Sept 2026), /tmp/oaimath/166/paper.pdf (sha256 37f6355365a18510e75d897dc9ab6d29305d7ff132cf148845b6f16d080ee1bf).
Scope: exact identities and small-case checks (a)–(i) of the numerics brief. Every script is in `/tmp/oaimath/166/numerics_scripts/`. Every output quoted below was re-run by this seat on 2026-10-12, at `nice -n 19`, each run under 35 s. The verbatim outputs are also stored in `numerics_scripts/outputs/<script>.txt`. Scripts left by a previous seat were re-read before reuse. `b_sv.py` was rewritten. `h_hilbert.py` (84 s, over the time budget) was superseded by `h3_hilbert.py` and is not reported. Six scripts are new: `c2_extra.py`, `d3_exact.py`, `f2_all_isometries.py`, `h3_hilbert.py`, `i_sec56.py`, and the rewritten `b_sv.py`.

**Verdict for scope: HOLDS AS READ.** None of the identities or inequalities on the brief's list failed, at any instance tested. That includes the explicit constants and exponent inequalities I recomputed in §5–6. Every inequality that pushes against a divergent quantity has a strict positive margin, and the margin does not depend on δ. The only failures produced are deliberate: Lemma 3.6 toys built to violate its hypothesis. Those show the hypothesis is needed, and the paper's two uses, (2.3) and (2.9), satisfy it. Limits: small-case checks cannot certify the qualitative (algebraic-geometric) steps. Those are listed under "skimmed" below.

## Pass/fail table

| Item | Claim tested (paper location) | Instances | Result |
|---|---|---|---|
| (a) | Grid {1..t}^d has squared distances in [1, d(t−1)²] (p. 1). Ratio \|Δ\|/n^{2/d} | d=3,4; t=2..6, all pairs enumerated | PASS (ratios 0.75–2.03; ≤ d always) |
| (b) | §1.1 (p. 2): GK+SV Thm 2.1 ⇒ n^{3/5}/(log n)^{2/5} (d=3); TYZ+SV Cor 2.3 ⇒ 8/17 (d=4); TYZ+SV Cor 2.6 ⇒ 3/8 (d=5); SV Thm 1.1: n^{.5643}, n^{2/d−2/(d(d+2))} | exact rationals + asymptotics | PASS (all MATCH SV) |
| (c) | N=A^{d/2}, N²=A^d, N≤A^{d−1}, A^{d/2}≤A^{d−2} (d≥4), M^{2+(d−ℓ)/2}=O(M^{d/2}) ⟺ ℓ≥4, δ(H)/A^{d−1}=c₃A/M, C(D+s₀,s₀)≤C₄A^{s₀}, exponent of A^{d−1} in N | d=3..8 symbolic | PASS |
| (c′) | Lemma 2.1 rows and c₀=1/2; Prop 2.2 dyadic sum; (2.3) c₁; (2.9) c₄, θ; Chernoff/union bound | numeric + symbolic | PASS |
| (d) | (2.6)–(2.8) and the p. 11 matrix identity (v₀·Zv₀=0); F_{p,q} distinct; {Z: Z(u+w)=u−w} ≠ ∅ ⟺ \|u\|=\|w\| (u+w≠0), codim d−1; both polarization identities (pp. 12–13); Prop 2.2 radius-class identity | d=3,4: sympy-symbolic, exact rational (40 trials each, three cases), float (200 trials) | PASS |
| (e) | Lemma 2.5: equal Gram matrices ⇒ u_i↦w_i extends to S∈O(d) | d=3; k=1..5; dependent, collinear and planar sets; both orientations; negative control | PASS |
| (f) | Theorem 7.1 scale Σ_{k_g≥C_rich A} k_g² vs N⁴/A = N^{10/3} | lattice motions t=3..7; ALL isometries of R³ for t=3 (13 392 linear parts) | sanity: ratio 1.5–4.3 at C_rich=1–2, decreasing in t (not a proof) |
| (g) | Lemma 2.1: a circle holds ≤ 2M points; a line ≤ 2M | regular n-gons n≤24, + centre, all subsets of the 12- and 13-gon, subsets of lattice circles | PASS. Proof gives 2M−1, sharp (regular odd polygons); 2M never attained |
| (h) | Lemma 3.6: H_V(L) ≥ c_{n,k} a L^k at the defining degree, c_{n,k}=1/((n−k+1)^n k!); (3.5); the shift q ≤ (n−k)(L−1); (3.8) | 100 toys (62 satisfy the hypothesis) | PASS: 0/62 violations, min ratio 2.30·c_{n,k}. Shift q tight for CI points. 4/38 hypothesis-violating toys fall below, as expected |
| (i) | §5.1 thresholds (5.3)–(5.5), lower-boundary ratio, E L² = o(N); (5.6)–(5.7); Prop 5.5 nonreal-line fraction; (6.5)–(6.7) margins; (6.9); (6.10), Lemma 6.4 margins; k≥2 deletion exponent; (6.19)–(6.20); r vs q; (6.26) case analysis; (6.25)/(6.27); §6.5 identities RD_d=A, e_{d−1}/R=N/A, (6.29) | exact + 100 000 random admissible profiles, d=3..7 | PASS. The only zero-margin case is exactly the one the paper names (narrower centres, l=1, b_d>0 → §6.5) |

## Objections (all in this scope)

None is FATAL or GAP. Recorded so the next reader does not re-derive them.

1. **Lemma 2.1, p. 7 (rows u=1 and "A circle contains at most 2M points").** COSMETIC. The proof on p. 8 ("any positive distance has at most two realizations… These observations include the sample point itself") gives 1+2(M−1) = 2M−1. The paper itself states the sharper form at (7.2), p. 61: "Thus the sharper bound 1 + 2(M − 1) also holds." For circles 2M−1 is sharp. The regular (2k+1)-gon has |Δ|=k and n = 2k+1 = 2M−1 (`g_circle.py`). An exhaustive search over all subsets of the regular 12- and 13-gon gives max(n − (2M−1)) = 0, so 2M is never attained. For lines the true bound is M (n collinear points determine ≥ n−1 distances). The stated bounds are valid upper bounds and are used only as upper bounds. Harmless.

2. **(6.9), p. 47: "Balance gives 1 ≤ k < d − 1, e_j = B^{d−2k}, N/e_j = A^k."** COSMETIC. With s = log B every D_i = B^{1+b_i} ≥ 1 (b_i ≥ −1), so e_j = B^{d−2k} forces k ≤ d/2. Enumeration (`i_sec56.py`) gives the feasible k: d=3: {1}; d=4: {1,2}; d=5: {1,2}; d=6: {1,2,3}; d=8: {1,2,3,4}. So the stated range 1 ≤ k < d−1 is correct but loose. The equalities also hold only up to exp(o(s)) = B^{o(1)}. The argument that follows treats every k ≥ 2 uniformly, so nothing depends on this. The k ≥ 2 deletion exponent (d−2k)+(k+1) = d−k+1 < d checks for every k ≥ 2.

3. **§5.1, p. 36: "If a residual survives at step i, every later terminal piece inside it has size at least m exp(−a_i/2 − Σ_{r>i} a_r)."** COSMETIC (unexplained factor, but a weaker-than-true bound). The construction gives the stronger m·exp(−Σ_{r>i} a_r), because every later operation keeps ≥ λ_r of the original mass of the node it acts on. So (5.4) holds a fortiori. The exact arithmetic of (5.4) was checked for K ≤ 39 indices: Σ_{r>i} a_r < a_i/9 exactly, and −1/2+1/9 = −7/18 exactly.

4. **§5.1, p. 36: "Σ_i a_i = s^{1/10+o(1)} = o(s^{1/3})".** Not an error, an observation. With K = O(1+√log s) indices, Σ a_i = s^{1/10}(10^K−1)/9 and 10^K = exp(O(√log s)) = s^{o(1)}. The output table shows Σa_i / s^{1/3} < 1 only between s = 10^{32} and 10^{64}. Only the limit is used and no rate is claimed, so this is harmless. The summability claims (5.5) also check: 2^{m/10} ≥ 1+cm with c = log2/10, and √log(2^m u) ≤ √log u + √(m log 2), with 0 violations over m < 400. The resulting sums tend to 0 as u → ∞.

5. **§1.1, p. 2, the d=3 log bound.** No objection; precision note. "Combining the Guth–Katz planar bound with the first Solymosi–Vu recurrence gives Ω(n^{3/5}/(log n)^{2/5})" is right, with the correct citation [21, Theorem 2.1]: Corollary 2.3 only takes pure powers. The exact optimum is min_m max(n m^{−2/3}, m/ln m) ∼ (5/3)^{2/5} n^{3/5}/(ln n)^{2/5}. Numerically the ratio to n^{3/5}/(ln n)^{2/5} rises 1.154 (n=10⁶) → 1.2224 (n=10³⁰⁰) → 1.2267.

6. **The brief's framing of the "general d" state of the art (not the paper).** The paper says "Their original theorem gives … Ω_d(n^{2/d−2/(d(d+2))}) for every fixed d ≥ 4 [21, Theorem 1.1]", which MATCHES SV. Note, though, that SV's own Fact 2.8 fed with the Guth–Katz and TYZ inputs gives strictly larger exponents for every d ≥ 4: 2(d+1)/(d²+2d−2) for even d, 2(d+1)/(d²+2d−3) for odd d. Examples: d=6: 9/29 ≈ 0.3103 vs 7/24 ≈ 0.2917; d=7: 4/15 vs 16/63. All stay below 2/d. This affects no claim in the paper.

7. **Theorem 7.1 sanity check (f) and its hypothesis.** Observation. The grids {0..t−1}³ violate the literal hypothesis M ≤ A, since |Δ| ≈ 2.5A (t=6: |Δ|=44 > A=36). They do satisfy the line cap ≤ 2A, and that cap is what the proof uses (p. 62: "We shall prove the same assertion for two clouds X, Y … whenever every line contains at most 2A points of either cloud"). Results: lattice motions give Σ_{k≥A} k² / N^{10/3} = 3.97, 3.28, 2.58, 2.27, 1.94 for t=3..7. All isometries of R³ at t=3 give 4.24 for C_rich=1, 2.17 for C_rich=2 and 9.82 for C_rich=1/2. Grids are far from extremal: Σ over all lattice motions ≈ 14.7 N³. This is consistent with (7.1) but proves nothing about K_rich.

## Citation table (this scope)

| Cited result | Paper's claim (p. 1–2) | Source (quote) | Verdict |
|---|---|---|---|
| Solymosi–Vu [21] — Combinatorica 28(1) (2008) 113–125. Journal PDF at refs/solymosi-vu/sv_combinatorica2008.pdf (sha256 36fc0ed5…ec78; byte-identical to refs/SV/sv.pdf). **Not on arXiv:** arXiv title search "Near optimal bounds distinct distances high dimensions" and author search both return nothing. Read the journal version. | "Solymosi and Vu developed two recursive inequalities connecting distance bounds in lower and higher dimensions [21, Theorems 2.1–2.2]" | Thm 2.1: "Let A be a set of n points in R^d (d ≥ 3) and m be the maximum cardinality of the intersection of A with a hyperplane of co-dimension 1. Then t(A) = Ω(max(n/m^{(d−1)/d}, t_{d−1}(m)))." Thm 2.2: "… co-dimension 2. Then t(A) = Ω(max(n^{(d+1)/2d}/m^{(d−1)/2d}, t_{d−2}(m)))." | MATCH |
| [21] §2 | "The recurrences have separate forms for the total number of distances and for the maximum number measured from one point… We use the forms for total distances" | "Instead of lower bounding g_d(n), we are going to bound t_d(n) from below. All theorems and corollaries in this section hold, with the same proofs, if we replace t_d(n) by g_d(n)." | MATCH |
| [21, Thm 1.1] | "Their original theorem gives Ω(n^{0.5643}) distances in dimension three and Ω_d(n^{2/d−2/(d(d+2))}) for every fixed d ≥ 4" | "Theorem 1.1. (a) g₃(n) = Ω(n^{.5643}). (b) For any d ≥ 4, g_d(n) = Ω(n^{2/d − 2/(d(d+2))})." (from α₂ = .8635 via (1) with d₀=2, d=3: 3·.8635/(3·.8635+2) = 0.564318) | MATCH |
| [21, Thm 2.1] with Guth–Katz [16, Thm 1.1] | "Combining the Guth–Katz planar bound with the first Solymosi–Vu recurrence gives Ω(n^{3/5}/(log n)^{2/5}) distances in dimension three [21, Theorem 2.1]" | GK (refs/1011.4105v3, current v3): "Theorem 1.1. A set of N points in the plane determines ≳ N/log N distinct distances." Thm 2.1 (above), optimised over m: (5/3)^{2/5}(1+o(1)) n^{3/5}/(log n)^{2/5} | MATCH |
| [21, Cors 2.3, 2.6] with TYZ [26, Thm 1.1] | "Inserting their three-dimensional distance bound into the Solymosi–Vu recurrences gives n^{8/17−o(1)} in dimension four and n^{3/8−o(1)} in dimension five [21, Corollaries 2.3 and 2.6]" | Cor 2.3: "Let α be a positive constant such that t_{d−1}(n) = Ω(n^α), then t_d(n) = Ω(n^{dα/(dα+(d−1))})". Cor 2.6: "… t_{d−2}(n) = Ω(n^α), then t_d(n) = Ω(n^{(d+1)α/(2dα+(d−1))})". TYZ (refs/2608.14454v1; arXiv abs page shows only v1, 14 Aug 2026): "Theorem 1.1. There exists a function ε = ε(N) satisfying ε(N) ≲ log log N/ log N so that any set of N points in R³ determines at least N^{2/3−ε} distinct distances." 4·(2/3)/(4·(2/3)+3) = 8/17; 6·(2/3)/(10·(2/3)+4) = 3/8. The corollaries need a constant α; use α = 2/3−ε' for each ε'>0. | MATCH |

## Constant-dependency table (this scope)

| Constant | Fixed where | Depends on | Used where | Claimed independent of | Check |
|---|---|---|---|---|---|
| c₀ = 1/2 | Lemma 2.1 proof, p. 8 | nothing (d ≥ 3) | flat caps, p. 7 and later | sequence | worst flat B^{max(2,d−1)+o(1)} < B^{d−1/2} for d=3..7 (`c2_extra.py`) |
| C_u (flat rows) | Lemma 2.1 | u, and c_u of dimension u (minimality) | Prop 2.2 fibres; Lemma 2.1 | sequence | inversion m/ln m ≤ X ⇒ m ≤ 2X ln X checked |
| c₁ = c_d/(d·C·2^{d−1}) | (2.3), p. 10 | d; Lemma 3.6's c_d; Prop 2.2's C | Prop 2.3 positive density (2/c₁ factor) | subset S, sequence | `c2_extra.py` |
| c₂, c₃ | (2.4), (2.5), p. 10–11 | c′ of Prop 2.3; for d=3 also K_rich/A·M → 0 | Prop 2.6 | sequence | δ(H)/A^{d−1} = c₃A/M → ∞, no rate |
| C₄ = 2^{s₀+1}/s₀! | Prop 2.6, p. 13 | d (s₀ = d(d−1)/2) | sampled rank | A, sequence | max_{A≥s₀} C(A+s₀,s₀)/A^{s₀} = 0.7407, 0.0198, 1.85e-5 (at A = s₀) ≤ 2^{s₀}/s₀! for d=3,4,5 |
| c₄ = c/(C(d+1)2^{s₀+d}) | (2.9) | d; Lemma 3.6 c; Lemma 2.4 C | Prop 2.6 | sequence | arithmetic in `c2_extra.py` |
| θ < c₄/C₄ | Prop 2.6 | c₄, C₄ only | sampling | sequence, δ(H) | fixed before N → ∞ |
| c_{n,k} = 1/((n−k+1)^n k!) | Lemma 3.6 (algebra seat's explicit value) | n, k | (2.3), (2.9) | a, L, D, other components | toys: 0/62 violations, min ratio 2.30·c_{n,k} |
| s_* | §5.1, p. 35 | δ (chosen slowly: δ e^{6s_*} → 0, s_* ≤ ¼ log B) | core: E L² = δ N e^{6s_*} = o(N) | — (sequence-dependent by design; used only qualitatively) | `i_sec56.py` |
| a_K = s^{1/10}, a_i = 10a_{i+1}, K = O(1+√log s) | (5.3) | s | (5.4), (5.5) | — | exact; 7/18; summable |
| ε < ¼(t₁−t₀), ξ, η, t₀…t₂ | (6.10), Lemma 6.4, §6.5 | limiting profile (b_i) | margins | δ | all margins strictly positive from (5.7) |
| r = ⌈B e^{−2s}⌉, q = B^{1/2} | §6.3, p. 55 | B, s | depth bound | — | q/r = B^{−1/2+o(1)} → 0 |

## What I verified line by line vs skimmed

**Verified line by line, arithmetic and identities, all re-run:**
- p. 1 grid upper bound.
- §1.1 pp. 1–2: every exponent quoted, against the SV source.
- §2 pp. 7–13:
  - Lemma 2.1: rows, c₀, circle and line rows.
  - Prop 2.2: rich-line dyadic sum; greedy degree budget N/(KA); the L²/M − L ≥ L²/(2M) count; the radius-class identity |q−z_i|²−|q−z_j|² = −2(q−p)·(z_i−z_j); the ℓ ≥ 4 fibre bookkeeping for d=3..8 in every case d−ℓ ∈ {0,1,2,≥3}.
  - (2.3) constant; (2.4) Cauchy–Schwarz; d=3 deletion o(N⁴/M); pruning bound; (2.5).
  - (2.6)–(2.8) symbolically and exactly, including dimension s₀, distinctness, nonemptiness iff |u|=|w|, codimension d−1, excess h = d−2 = r−1, u+w=0 empty.
  - Both polarization identities; Gram-to-isometry.
  - Isotropic caps: N ≤ A^{d−1}; N = A^{d/2} ≤ A^{d−2} iff d ≥ 4.
  - (2.9), C₄, θ, Markov/Chernoff/union bound.
- §5.1 p. 35–36: every displayed number. §5.2 (5.6)–(5.7) deduction including b₁+b₂<0 and Figure 2's profile (sum 0, b₁+b₂ = −6/5). Prop 5.3 exceptional-mass exponent. Prop 5.5 nonreal-line fraction e_{d−1}/n = e^{o(s)}/D_d.
- §6: (6.5) initial-interval and k=d−1 comparisons; (6.6); (6.7) margins; (6.9); (6.10)–(6.11); Lemma 6.4 margins t₀−β, t₀−(1+b₁+b₂), t₁−t₀−ε; the k≥2 deletion; B^{2−c}; the √δ B^{−c} and √δ M/A ratios; lift-degree ≤ 2 deg γ; (6.18)–(6.20), including R = B e^{−sΣ_{i>j}b_i}; q = o(r); (6.21)–(6.26) case analysis, exhaustive over plateaux of 100 000 random admissible profiles; (6.25)/(6.27) ≥ δ^{−1}e^{cs/3}; §6.5 RD_d = A, e_{d−1}/R = N/A, (6.28)–(6.29) ratio δ e^{−(η−ε)s}.

**Only skimmed. Not certifiable by numerics:**
- The algebraic-geometric content of Prop 2.2's hyperplane-section induction and of Lemmas 2.4/2.5, i.e. Theorem A.1 itself.
- The proof of Lemma 3.6, beyond the toys.
- §5.2's envelope propagation for (5.9).
- §5.3–5.4 (regularity, product testing, window selection), beyond their displayed arithmetic.
- §6's geometric arguments: Lemma 6.2's flatness and fibre identification, Lemma 6.4's regularity, §6.3's Sylvester-matrix/DVR specialisation and multiplicity compression, §6.5's identification of covering curves.
- §4 (Prop 4.3, Lemma 4.2), §7 (Theorem 7.1 proof) and Appendices A, B. Other seats own these.

---
## (a) The grid {1..t}^d

Enumerate {1..t}^d. Collect the squared distances of all point pairs exactly (integers), and cross-check against the set of squared lengths of difference vectors. The paper claims (p. 1) "its squared distances are integers between 1 and d(t − 1)²". This holds in all 10 instances. The ratio |Δ|/n^{2/d} = |Δ|/t² lies in [0.75, 2.03]. By the stated bound it is always < d(t−1)²/t² < d, which is the matching upper bound |Δ| < d·n^{2/d}.

Script `numerics_scripts/a_grid.py` — verbatim output:

```
d=3 t=2 n=    8 |Delta|=  3 <= d(t-1)^2=  3: True  ratio |Delta|/n^(2/d) = 0.7500  (pairs-checked)
d=3 t=3 n=   27 |Delta|=  9 <= d(t-1)^2= 12: True  ratio |Delta|/n^(2/d) = 1.0000  (pairs-checked)
d=3 t=4 n=   64 |Delta|= 18 <= d(t-1)^2= 27: True  ratio |Delta|/n^(2/d) = 1.1250  (pairs-checked)
d=3 t=5 n=  125 |Delta|= 31 <= d(t-1)^2= 48: True  ratio |Delta|/n^(2/d) = 1.2400  (pairs-checked)
d=3 t=6 n=  216 |Delta|= 44 <= d(t-1)^2= 75: True  ratio |Delta|/n^(2/d) = 1.2222  (pairs-checked)
d=4 t=2 n=   16 |Delta|=  4 <= d(t-1)^2=  4: True  ratio |Delta|/n^(2/d) = 1.0000  (pairs-checked)
d=4 t=3 n=   81 |Delta|= 13 <= d(t-1)^2= 16: True  ratio |Delta|/n^(2/d) = 1.4444  (pairs-checked)
d=4 t=4 n=  256 |Delta|= 28 <= d(t-1)^2= 36: True  ratio |Delta|/n^(2/d) = 1.7500  (pairs-checked)
d=4 t=5 n=  625 |Delta|= 49 <= d(t-1)^2= 64: True  ratio |Delta|/n^(2/d) = 1.9600  (pairs-checked)
d=4 t=6 n= 1296 |Delta|= 73 <= d(t-1)^2=100: True  ratio |Delta|/n^(2/d) = 2.0278  (pairs-checked)
```


## (b) Solymosi–Vu recurrences applied by hand

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

All of this agrees with the paper's §1.1 (pp. 1–2). See the citation table.

Script `numerics_scripts/b_sv.py` — verbatim output:

```
== consistency of SV's own statements ==
  Thm 1.1(a): Cor 2.3 at d=3 with Tardos a2=.8635:  3a2/(3a2+2) = 0.564318  (SV: .5643)
  Cor 1.3 d=4: 0.43576 > 2/d-2/(d(d+2)) = 0.41667: True
  Cor 1.3 d=5: 0.35111 > 2/d-2/(d(d+2)) = 0.34286: True
  Cor 1.3 d=6: 0.29820 > 2/d-2/(d(d+2)) = 0.29167: True
  Cor 1.3 d=7: 0.25733 > 2/d-2/(d(d+2)) = 0.25397: True
  Cor 1.3 d=8: 0.22800 > 2/d-2/(d(d+2)) = 0.22500: True
  Cor 1.3 d=9: 0.20371 > 2/d-2/(d(d+2)) = 0.20202: True
  Cor 1.3 d=10: 0.18495 > 2/d-2/(d(d+2)) = 0.18333: True
  Fact 2.8 with d0=2 equals Cor 1.3(3): True ; with d0=3 equals Cor 1.3(4): True
== (i) Guth-Katz g_2(m) >= c m/log m into Thm 2.1 at d=3 (the log form; Cor 2.3 needs a pure power) ==
  pure-power shadow: Cor 2.3 with a=1 at d=3: 3/5
  exact asymptotics: minimise max(n m^(-2/3), m/ln m) over m; the minimum is at the crossing n = m^(5/3)/ln m,
  value V = m/ln m;  ln m ~ (3/5) ln n  =>  V ~ n^(3/5) ((3/5) ln n)^(-2/5) = (5/3)^(2/5) n^(3/5)/(ln n)^(2/5); (5/3)^(2/5) = 1.226703
    n=1e6: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.15437
    n=1e12: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.17857
    n=1e24: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.19642
    n=1e50: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.20896
    n=1e100: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.21631
    n=1e200: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.22075
    n=1e300: min max(...) / (n^(3/5)/(ln n)^(2/5)) = 1.22244
  => Theta(n^(3/5)/(log n)^(2/5)): exponent 3/5, log power 2/5 (paper Sec. 1.1: Omega(n^{3/5}/(log n)^{2/5}) [21, Theorem 2.1])
== (ii) Tidor-Yu-Zakharov g_3(n) >= n^{2/3-o(1)} ==
  d=4 via Cor 2.3 (from d=3): 8/17  (paper: 8/17)   [Fact 2.5 d0=3: 8/17 ]
  d=4 via Cor 2.6 (from d=2, Guth-Katz a=1): 5/11 =  0.45454545454545453 < 8/17
  d=5 via Cor 2.6 (from d=3): 3/8  (paper: 3/8)   [Fact 2.8 d0=3: 3/8 ]
  d=5 via Cor 2.3 (from d=4 = 8/17): 10/27 = 0.37037037037037035 < 3/8
  o(1) bookkeeping: inputs 2/3-eps give d=4: 0.47058786159143173  d=5: 0.37499978906230225 (continuous in a; -> 8/17, 3/8)
== general d: best of the two recurrences from (Guth-Katz a2 = 1-o(1), TYZ a3 = 2/3-o(1)) vs SV's general 2/d - 2/(d(d+2)) ==
  d=4: via Cor2.3 8/17 (0.4706), via Cor2.6 5/11 (0.4545); Fact 2.8 closed form 5/11 (0.4545); 2/d-2/(d(d+2)) = 5/12 (0.4167); 2/d = 0.5000
  d=5: via Cor2.3 10/27 (0.3704), via Cor2.6 3/8 (0.3750); Fact 2.8 closed form 3/8 (0.3750); 2/d-2/(d(d+2)) = 12/35 (0.3429); 2/d = 0.4000
  d=6: via Cor2.3 9/29 (0.3103), via Cor2.6 56/181 (0.3094); Fact 2.8 closed form 7/23 (0.3043); 2/d-2/(d(d+2)) = 7/24 (0.2917); 2/d = 0.3333
  d=7: via Cor2.3 21/79 (0.2658), via Cor2.6 4/15 (0.2667); Fact 2.8 closed form 4/15 (0.2667); 2/d-2/(d(d+2)) = 16/63 (0.2540); 2/d = 0.2857
  d=8: via Cor2.3 32/137 (0.2336), via Cor2.6 81/347 (0.2334); Fact 2.8 closed form 3/13 (0.2308); 2/d-2/(d(d+2)) = 9/40 (0.2250); 2/d = 0.2500
  d=9: via Cor2.3 36/173 (0.2081), via Cor2.6 5/24 (0.2083); Fact 2.8 closed form 5/24 (0.2083); 2/d-2/(d(d+2)) = 20/99 (0.2020); 2/d = 0.2222
  d=10: via Cor2.3 25/133 (0.1880), via Cor2.6 352/1873 (0.1879); Fact 2.8 closed form 11/59 (0.1864); 2/d-2/(d(d+2)) = 11/60 (0.1833); 2/d = 0.2000
  identity 2/d - 2/(d(d+2)) = 2(d+1)/(d(d+2)): True
```


## (c) Exponent bookkeeping of §2

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
- the sizes in the Chernoff/union bound.

Script `numerics_scripts/c_exponents.py` — verbatim output:

```
d | N=A^e  | N^2=A^e | N<=A^(d-1)? | A^(d/2)<=A^(d-2)? (local iso cap, needs d>=4) | s0=d(d-1)/2 | A^(d-1)=N^e | delta(H)/A^(d-1)
3 | 3/2    | 3       | True (3/2<= 2) | False (3/2 <= 1) | 3 | N^4/3 | c3*N^2/(M*A^(d-1)) = c3*A^3/(M*A^2) = c3*A/M -> oo
4 | 2    | 4       | True (2<= 3) | True (2 <= 2) | 6 | N^3/2 | c3*N^2/(M*A^(d-1)) = c3*A^4/(M*A^3) = c3*A/M -> oo
5 | 5/2    | 5       | True (5/2<= 4) | True (5/2 <= 3) | 10 | N^8/5 | c3*N^2/(M*A^(d-1)) = c3*A^5/(M*A^4) = c3*A/M -> oo
6 | 3    | 6       | True (3<= 5) | True (3 <= 4) | 15 | N^5/3 | c3*N^2/(M*A^(d-1)) = c3*A^6/(M*A^5) = c3*A/M -> oo

Prop 2.2, l>=4 branch: fibres O(M^2) many, each bounded by f(d-l); total exponent 2+f vs d/2
  d=3 l=1 d-l=2: fibre circle: 2M             total M^3 vs M^3/2: FAILS (branch NOT used: l<=3 handled separately)
  d=3 l=2 d-l=1: fibre <=2 points             total M^2 vs M^3/2: FAILS (branch NOT used: l<=3 handled separately)
  d=3 l=3 d-l=0: fibre <=2 points             total M^2 vs M^3/2: FAILS (branch NOT used: l<=3 handled separately)
  d=4 l=1 d-l=3: fibre flat u=3: C M^(u/2)    total M^7/2 vs M^2: FAILS (branch NOT used: l<=3 handled separately)
  d=4 l=2 d-l=2: fibre circle: 2M             total M^3 vs M^2: FAILS (branch NOT used: l<=3 handled separately)
  d=4 l=3 d-l=1: fibre <=2 points             total M^2 vs M^2: OK (branch NOT used: l<=3 handled separately)
  d=4 l=4 d-l=0: fibre <=2 points             total M^2 vs M^2: OK (branch used)
  d=5 l=1 d-l=4: fibre flat u=4: C M^(u/2)    total M^4 vs M^5/2: FAILS (branch NOT used: l<=3 handled separately)
  d=5 l=2 d-l=3: fibre flat u=3: C M^(u/2)    total M^7/2 vs M^5/2: FAILS (branch NOT used: l<=3 handled separately)
  d=5 l=3 d-l=2: fibre circle: 2M             total M^3 vs M^5/2: FAILS (branch NOT used: l<=3 handled separately)
  d=5 l=4 d-l=1: fibre <=2 points             total M^2 vs M^5/2: OK (branch used)
  d=5 l=5 d-l=0: fibre <=2 points             total M^2 vs M^5/2: OK (branch used)
  d=6 l=1 d-l=5: fibre flat u=5: C M^(u/2)    total M^9/2 vs M^3: FAILS (branch NOT used: l<=3 handled separately)
  d=6 l=2 d-l=4: fibre flat u=4: C M^(u/2)    total M^4 vs M^3: FAILS (branch NOT used: l<=3 handled separately)
  d=6 l=3 d-l=3: fibre flat u=3: C M^(u/2)    total M^7/2 vs M^3: FAILS (branch NOT used: l<=3 handled separately)
  d=6 l=4 d-l=2: fibre circle: 2M             total M^3 vs M^3: OK (branch used)
  d=6 l=5 d-l=1: fibre <=2 points             total M^2 vs M^3: OK (branch used)
  d=6 l=6 d-l=0: fibre <=2 points             total M^2 vs M^3: OK (branch used)
  d=7 l=1 d-l=6: fibre flat u=6: C M^(u/2)    total M^5 vs M^7/2: FAILS (branch NOT used: l<=3 handled separately)
  d=7 l=2 d-l=5: fibre flat u=5: C M^(u/2)    total M^9/2 vs M^7/2: FAILS (branch NOT used: l<=3 handled separately)
  d=7 l=3 d-l=4: fibre flat u=4: C M^(u/2)    total M^4 vs M^7/2: FAILS (branch NOT used: l<=3 handled separately)
  d=7 l=4 d-l=3: fibre flat u=3: C M^(u/2)    total M^7/2 vs M^7/2: OK (branch used)
  d=7 l=5 d-l=2: fibre circle: 2M             total M^3 vs M^7/2: OK (branch used)
  d=7 l=6 d-l=1: fibre <=2 points             total M^2 vs M^7/2: OK (branch used)
  d=7 l=7 d-l=0: fibre <=2 points             total M^2 vs M^7/2: OK (branch used)
  d=8 l=1 d-l=7: fibre flat u=7: C M^(u/2)    total M^11/2 vs M^4: FAILS (branch NOT used: l<=3 handled separately)
  d=8 l=2 d-l=6: fibre flat u=6: C M^(u/2)    total M^5 vs M^4: FAILS (branch NOT used: l<=3 handled separately)
  d=8 l=3 d-l=5: fibre flat u=5: C M^(u/2)    total M^9/2 vs M^4: FAILS (branch NOT used: l<=3 handled separately)
  d=8 l=4 d-l=4: fibre flat u=4: C M^(u/2)    total M^4 vs M^4: OK (branch used)
  d=8 l=5 d-l=3: fibre flat u=3: C M^(u/2)    total M^7/2 vs M^4: OK (branch used)
  d=8 l=6 d-l=2: fibre circle: 2M             total M^3 vs M^4: OK (branch used)
  d=8 l=7 d-l=1: fibre <=2 points             total M^2 vs M^4: OK (branch used)
  d=8 l=8 d-l=0: fibre <=2 points             total M^2 vs M^4: OK (branch used)
  generic identity: 2+(d-l)/2 <= d/2  <=>  l >= 4 : 2 - l/2 <= 0

Lemma 2.1 rows (M<=A=B^2): u=1: 2M<=2B^2; u=2: C M log 2M <= C B^2 log(2B^2) = B^{2+o(1)}; u>=3: C M^(u/2) <= C B^u
  d=3: worst proper flat ~ B^2 (u=2 if >=3 else plane B^{2+o(1)}); N B^(-1/2) = B^5/2 -> c0=1/2 works: True
  d=4: worst proper flat ~ B^3 (u=3 if >=3 else plane B^{2+o(1)}); N B^(-1/2) = B^7/2 -> c0=1/2 works: True
  d=5: worst proper flat ~ B^4 (u=4 if >=3 else plane B^{2+o(1)}); N B^(-1/2) = B^9/2 -> c0=1/2 works: True

C(D+s0,s0) vs A^{s0} with D=floor(A): ratio C(D+s0,s0)/A^{s0}
  d=3 s0=3: A=10,100,1e3,1e5 -> ['0.286', '0.1769', '0.1677', '0.1667']  limit 1/s0! = 0.1667  (so C4 = 2^3/s0! suffices for A>=s0)
  d=4 s0=6: A=10,100,1e3,1e5 -> ['0.008008', '0.001706', '0.001418', '0.001389']  limit 1/s0! = 0.001389  (so C4 = 2^6/s0! suffices for A>=s0)
  d=5 s0=10: A=10,100,1e3,1e5 -> ['1.848e-05', '4.69e-07', '2.911e-07', '2.757e-07']  limit 1/s0! = 2.756e-07  (so C4 = 2^10/s0! suffices for A>=s0)

Lemma 2.5 excess dimension: Z-space dim s0, neighbour flat codim d-1, hypersurface dim s0-1 => h = (s0-1)-(s0-d+1) = d-2 = r-1 with r=d-1
  d=3: s0=3, neighbour flat dim 1, hypersurface dim 2, h=1, r-1=1; bound C*deg*A^(d-2) summed over deg<=A: C*A^2
  d=4: s0=6, neighbour flat dim 3, hypersurface dim 5, h=2, r-1=2; bound C*deg*A^(d-2) summed over deg<=A: C*A^3
  d=5: s0=10, neighbour flat dim 6, hypersurface dim 9, h=3, r-1=3; bound C*deg*A^(d-2) summed over deg<=A: C*A^4

Global ambient: skew forms on C^(d+1) = (Z,c): dim s0+d = d(d+1)/2; Lemma 2.4 h ranges 0..d
  d=3: s0+d=6 = d(d+1)/2=6; total params N^2=A^3, iso cap N=A^3/2 <= A^2
  d=4: s0+d=10 = d(d+1)/2=10; total params N^2=A^4, iso cap N=A^2 <= A^3
  d=5: s0+d=15 = d(d+1)/2=15; total params N^2=A^5, iso cap N=A^5/2 <= A^4

(2.4)-(2.5): edges 2*sum s_rho^2 >= 2|S|^2/(M-1) >= 2|S|^2/M; prune threshold E0/(2N^2) >= c2 N^2/(2M)
d=3 deletion: sum C(k,2) <= (1/2) sum k^2 <= (K/2) N^4/A ; ratio to N^4/M = (K/2) M/A -> 0
Chernoff: P(Bin < mean/2) <= exp(-mean/8); union over N^2 vertices: N^2 exp(-theta*delta(H)/8) <= N^2 exp(-theta*A^(d-1)/8) -> 0 since A^(d-1)=N^(2(d-1)/d) >> log N
```

Script `numerics_scripts/c2_extra.py` — verbatim output:

```
== Lemma 2.1 u=2 row: planar bound g_2(m) >= c m/log m and <= M-1 distances  =>  m <= C M log(2M) ==
  min_{X>0} (X - 2 ln X) = 0.613706 > 0, so m = 2X ln X has m/ln m >= X; brute check:
  violations of (largest m with m/ln m <= X) <= 2 X ln X over 200 X in [1.5, 2.8e8]: 0
== Lemma 2.1 u>=3 rows: c_u m^(2/u) <= M  =>  m <= (M/c_u)^(u/2) = C_u M^(u/2);  c0 = 1/2 ==
  d=3: proper u-flats hold at most u=1: B^2, u=2: B^2+o(1); N B^(-1/2) = B^5/2; worst exponent 2 < 5/2
  d=4: proper u-flats hold at most u=1: B^2, u=2: B^2+o(1), u=3: B^3; N B^(-1/2) = B^7/2; worst exponent 3 < 7/2
  d=5: proper u-flats hold at most u=1: B^2, u=2: B^2+o(1), u=3: B^3, u=4: B^4; N B^(-1/2) = B^9/2; worst exponent 4 < 9/2
  d=6: proper u-flats hold at most u=1: B^2, u=2: B^2+o(1), u=3: B^3, u=4: B^4, u=5: B^5; N B^(-1/2) = B^11/2; worst exponent 5 < 11/2
  d=7: proper u-flats hold at most u=1: B^2, u=2: B^2+o(1), u=3: B^3, u=4: B^4, u=5: B^5, u=6: B^6; N B^(-1/2) = B^13/2; worst exponent 6 < 13/2
== Prop 2.2 rich-line discard: sum over dyadic t = 2^j H <= L_max of C(N^2/t^3 + N/t)(2t)^2 <= 8C(N^2/H + N L_max) ==
  N=1e+06 H=10 L_max=1000: dyadic sum / (N^2/H + N L_max) = 7.909 (<= 8)
  N=1e+09 H=50 L_max=100000: dyadic sum / (N^2/H + N L_max) = 7.977 (<= 8)
  N=1e+12 H=1000 L_max=1000000: dyadic sum / (N^2/H + N L_max) = 7.988 (<= 8)
== Prop 2.2 greedy: removed curves Y carry > K A deg(Y) disjoint partners  =>  sum deg Y < N/(KA) = o(N/A) when K -> oo ==
== (2.3): |S| = sum_j #partners_j <= sum_j C a_j A^j,  H_S(D) >= c_d a_j D^j,  D = floor(A) >= A/2 (A >= 2) ==
  d=3: |S| <= d * C * 2^(d-1) * max_j a_j D^j <= (d C 2^(d-1)/c_d) H_S(D)  =>  c1 = c_d/(d C 2^(d-1)) = c_d/(C*12)
  d=4: |S| <= d * C * 2^(d-1) * max_j a_j D^j <= (d C 2^(d-1)/c_d) H_S(D)  =>  c1 = c_d/(d C 2^(d-1)) = c_d/(C*32)
  d=5: |S| <= d * C * 2^(d-1) * max_j a_j D^j <= (d C 2^(d-1)/c_d) H_S(D)  =>  c1 = c_d/(d C 2^(d-1)) = c_d/(C*80)
== (2.9) and the sample: H_{S_F}(D) >= max_h c a_h D^(s0+h) >= (c/C) max_h m_h A^(s0)(D/A)^(s0+h) >= c4 m A^s0 with c4 = c/(C (d+1) 2^(s0+d)) ==
  d=3, s0=3: max_(A>=s0) C(A+s0,s0)/A^s0 = 0.7407 <= 2^s0/s0! = 1.3333: True;  theta < c4/C4 suffices (fixed: depends on d and the constants of Lemmas 2.4 and 3.6 only)
  d=4, s0=6: max_(A>=s0) C(A+s0,s0)/A^s0 = 0.0198 <= 2^s0/s0! = 0.0889: True;  theta < c4/C4 suffices (fixed: depends on d and the constants of Lemmas 2.4 and 3.6 only)
  d=5, s0=10: max_(A>=s0) C(A+s0,s0)/A^s0 = 0.0000 <= 2^s0/s0! = 0.0003: True;  theta < c4/C4 suffices (fixed: depends on d and the constants of Lemmas 2.4 and 3.6 only)
== Chernoff + union bound: P(Bin(n,theta) < n theta/2) <= exp(-n theta/8); need N^2 exp(-theta delta(H)/8) -> 0 with delta(H) >> A^(d-1) ==
  d=3 N=1e+03: A^(d-1) = N^1.333 = 1.000e+04; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: 1.257e+01
  d=3 N=1e+06: A^(d-1) = N^1.333 = 1.000e+08; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -1.247e+04
  d=3 N=1e+09: A^(d-1) = N^1.333 = 1.000e+12; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -1.250e+08
  d=4 N=1e+03: A^(d-1) = N^1.500 = 3.162e+04; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: 9.863e+00
  d=4 N=1e+06: A^(d-1) = N^1.500 = 1.000e+09; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -1.250e+05
  d=4 N=1e+09: A^(d-1) = N^1.500 = 3.162e+13; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -3.953e+09
  d=5 N=1e+03: A^(d-1) = N^1.600 = 6.310e+04; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: 5.929e+00
  d=5 N=1e+06: A^(d-1) = N^1.600 = 3.981e+09; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -4.976e+05
  d=5 N=1e+09: A^(d-1) = N^1.600 = 2.512e+14; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: -3.140e+10
```


## (d) Skew-form identities (2.6)–(2.8) and polarization (pp. 11–13)

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

Also checked: the identity (Zv₀−y₀) − (Zv₀′−y₀′) = −½(Z(u+w)−(u−w)), which is (2.8); and the Prop 2.2 radius-class identity.

Script `numerics_scripts/d_skew.py` — verbatim output:

```
===== d=3, s0=3 (d(d-1)/2=3), ambient skew forms on C^4: dim 6 = d(d+1)/2 = 6
  (2.7) Omega v == y on F_pq: max residual over 200 random points 8.88e-16;  v0.Z v0 = 0: max 5.28e-16
  evaluation system Omega v = y: rank of all d+1 rows = 3, rank of first d rows = 3 -> flat dim = 3 (claimed s0=3)
  last (d+1)-th coordinate equation implied by first d: True  (uses v.Omega v = 0 and v.y = 0: v.y = 0.00e+00)
  distinct random pairs give distinct flats (200 trials): True;  (p,q) vs (p,q') same flat? False
  (2.8) intersection of neighbouring flats satisfies Z(u+w)=u-w: max residual 1.06e-13; intersection dim = 1 = s0-(d-1) = 1
  {Z skew: Z x = y}, x=u+w, y=u-w:
    |u|=|w|  : rank[Z->Zx] = 2, rank augmented = 2 -> NONEMPTY, codim in Z-space = 2  (x.y = |u|^2-|w|^2 = +1.783e-18)
    |u|!=|w| : rank[Z->Zx] = 2, rank augmented = 3 -> EMPTY, codim in Z-space = -  (x.y = |u|^2-|w|^2 = -9.440e-01)
    u+w=0    : rank[Z->Zx] = 0, rank augmented = 1 -> EMPTY, codim in Z-space = -  (x.y = |u|^2-|w|^2 = +0.000e+00)
  exact rank of Z->Zx for x=[1, 2, -3]: 2 (claimed d-1=2)
  non-proportional x give different direction spaces (200 trials): True; proportional x give same: True
  global polarization: B(X,X') = -(v0-v0').(y0-y0') = -(|p-p'|^2-|q-q'|^2)/4 : max err 1.11e-15
  local polarization: (ui-wi).(uj+wj)+(uj-wj).(ui+wi) = 2(ui.uj - wi.wj) = B([ui+wi:ui-wi],[uj+wj:uj-wj]): max err 3.55e-15
  Prop 2.2 identity |q-z_i|^2-|q-z_j|^2 = -2(q-p).(z_i-z_j) on a radius class: max err 1.42e-14
===== d=4, s0=6 (d(d-1)/2=6), ambient skew forms on C^5: dim 10 = d(d+1)/2 = 10
  (2.7) Omega v == y on F_pq: max residual over 200 random points 8.88e-16;  v0.Z v0 = 0: max 7.49e-16
  evaluation system Omega v = y: rank of all d+1 rows = 4, rank of first d rows = 4 -> flat dim = 6 (claimed s0=6)
  last (d+1)-th coordinate equation implied by first d: True  (uses v.Omega v = 0 and v.y = 0: v.y = 0.00e+00)
  distinct random pairs give distinct flats (200 trials): True;  (p,q) vs (p,q') same flat? False
  (2.8) intersection of neighbouring flats satisfies Z(u+w)=u-w: max residual 3.42e-14; intersection dim = 3 = s0-(d-1) = 3
  {Z skew: Z x = y}, x=u+w, y=u-w:
    |u|=|w|  : rank[Z->Zx] = 3, rank augmented = 3 -> NONEMPTY, codim in Z-space = 3  (x.y = |u|^2-|w|^2 = -6.342e-17)
    |u|!=|w| : rank[Z->Zx] = 3, rank augmented = 4 -> EMPTY, codim in Z-space = -  (x.y = |u|^2-|w|^2 = -6.797e-01)
    u+w=0    : rank[Z->Zx] = 0, rank augmented = 1 -> EMPTY, codim in Z-space = -  (x.y = |u|^2-|w|^2 = +0.000e+00)
  exact rank of Z->Zx for x=[1, 2, -3, 5]: 3 (claimed d-1=3)
  non-proportional x give different direction spaces (200 trials): True; proportional x give same: True
  global polarization: B(X,X') = -(v0-v0').(y0-y0') = -(|p-p'|^2-|q-q'|^2)/4 : max err 1.78e-15
  local polarization: (ui-wi).(uj+wj)+(uj-wj).(ui+wi) = 2(ui.uj - wi.wj) = B([ui+wi:ui-wi],[uj+wj:uj-wj]): max err 3.55e-15
  Prop 2.2 identity |q-z_i|^2-|q-z_j|^2 = -2(q-p).(z_i-z_j) on a radius class: max err 1.42e-14
```

Script `numerics_scripts/d2_symbolic.py` — verbatim output:

```
d=3: Omega v - y on F_pq  == [0, 0, 0, 0]  ; v0.Z v0 = 0
  B(X,X') + (v0-v0').(y0-y0') = 0;  (v0-v0').(y0-y0') - (|p-p'|^2-|q-q'|^2)/4 = 0
  (Zv0 - y0) - (Zv0' - y0') + (1/2)(Z(u+w) - (u-w)) = [0, 0, 0]
  local: L - 2(ui.uj - wi.wj) = 0;  x.Zx for skew Z: 0
d=4: Omega v - y on F_pq  == [0, 0, 0, 0, 0]  ; v0.Z v0 = 0
  B(X,X') + (v0-v0').(y0-y0') = 0;  (v0-v0').(y0-y0') - (|p-p'|^2-|q-q'|^2)/4 = 0
  (Zv0 - y0) - (Zv0' - y0') + (1/2)(Z(u+w) - (u-w)) = [0, 0, 0, 0]
  local: L - 2(ui.uj - wi.wj) = 0;  x.Zx for skew Z: 0
```

Script `numerics_scripts/d3_exact.py` — verbatim output:

```
d=3 (s0=3): {'eq_norm_nonempty_codim_d-1': 40, 'neq_norm_empty': 40, 'u+w=0_empty': 40, 'trials': 40}
   rank of v |-> (E v)_E over all skew basis E: 3 (= d -> Z v0 = Z v0' for all skew Z forces v0 = v0')
   F_pq: rank of (Z,c)-system = 3, dim = s0 + d - rank = 3 (claimed s0 = 3)
   excess dimension of a hypersurface component over a neighbour flat: 1 (claimed d-2 = 1 = r-1, r = d-1)
d=4 (s0=6): {'eq_norm_nonempty_codim_d-1': 40, 'neq_norm_empty': 40, 'u+w=0_empty': 40, 'trials': 40}
   rank of v |-> (E v)_E over all skew basis E: 4 (= d -> Z v0 = Z v0' for all skew Z forces v0 = v0')
   F_pq: rank of (Z,c)-system = 4, dim = s0 + d - rank = 6 (claimed s0 = 6)
   excess dimension of a hypersurface component over a neighbour flat: 2 (claimed d-2 = 2 = r-1, r = d-1)
```


## (e) Lemma 2.5: equal Gram matrices ⇒ isometry (d = 3)

Built S ∈ O(3) with SU = W from orthonormal bases of span U and span W. Cases:
- generic k = 1..5 vectors;
- a dependent set (u₃ = u₁ + 2u₂);
- a collinear set;
- 4 vectors in a plane;
- W built directly from the Gram matrix (Cholesky), not from any S₀.

Well-definedness was checked as kernel preservation, |W·ker U| ≈ 1e-16. That is the paper's "every linear relation is preserved by equality of the Gram matrices". Both orientations of S₀ were tested. Negative control: unequal Gram matrices are rejected. The match check x ↦ q + S(x−p) sends p+u_i to q+w_i.

Script `numerics_scripts/e_gram.py` — verbatim output:

```
generic k=1                      det(S0)=+1: kernel-preserved err 0.0e+00, image basis orthonormal err 4.4e-16, |S U - W| = 2.2e-16, |S^T S - I| = 3.3e-16, det S = -1.000
generic k=1                      det(S0)=-1: kernel-preserved err 0.0e+00, image basis orthonormal err 5.6e-16, |S U - W| = 4.4e-16, |S^T S - I| = 2.2e-16, det S = +1.000
generic k=2                      det(S0)=+1: kernel-preserved err 0.0e+00, image basis orthonormal err 4.4e-16, |S U - W| = 6.7e-16, |S^T S - I| = 7.8e-16, det S = +1.000
generic k=2                      det(S0)=-1: kernel-preserved err 0.0e+00, image basis orthonormal err 2.2e-16, |S U - W| = 6.7e-16, |S^T S - I| = 6.7e-16, det S = +1.000
generic k=3                      det(S0)=+1: kernel-preserved err 0.0e+00, image basis orthonormal err 1.6e-15, |S U - W| = 8.9e-16, |S^T S - I| = 2.9e-15, det S = +1.000
generic k=3                      det(S0)=-1: kernel-preserved err 0.0e+00, image basis orthonormal err 1.3e-15, |S U - W| = 1.3e-15, |S^T S - I| = 2.0e-15, det S = -1.000
generic k=4                      det(S0)=+1: kernel-preserved err 1.1e-16, image basis orthonormal err 2.4e-15, |S U - W| = 1.9e-15, |S^T S - I| = 2.0e-15, det S = +1.000
generic k=4                      det(S0)=-1: kernel-preserved err 1.1e-16, image basis orthonormal err 2.7e-15, |S U - W| = 2.0e-15, |S^T S - I| = 1.8e-15, det S = -1.000
generic k=5                      det(S0)=+1: kernel-preserved err 3.9e-16, image basis orthonormal err 6.7e-16, |S U - W| = 6.7e-16, |S^T S - I| = 6.7e-16, det S = +1.000
generic k=5                      det(S0)=-1: kernel-preserved err 5.0e-16, image basis orthonormal err 6.7e-16, |S U - W| = 6.7e-16, |S^T S - I| = 6.7e-16, det S = -1.000
dependent: u3=u1+2u2             det(S0)=+1: kernel-preserved err 5.4e-16, image basis orthonormal err 8.9e-16, |S U - W| = 1.3e-15, |S^T S - I| = 6.7e-16, det S = +1.000
dependent: u3=u1+2u2             det(S0)=-1: kernel-preserved err 4.5e-16, image basis orthonormal err 8.9e-16, |S U - W| = 1.3e-15, |S^T S - I| = 6.7e-16, det S = +1.000
collinear: u2=-1.5u1, u3=3u1     det(S0)=+1: kernel-preserved err 6.5e-16, image basis orthonormal err 3.3e-16, |S U - W| = 1.3e-15, |S^T S - I| = 4.4e-16, det S = -1.000
collinear: u2=-1.5u1, u3=3u1     det(S0)=-1: kernel-preserved err 7.6e-16, image basis orthonormal err 6.7e-16, |S U - W| = 1.2e-15, |S^T S - I| = 1.1e-16, det S = -1.000
planar 4 vectors                 det(S0)=+1: kernel-preserved err 1.3e-16, image basis orthonormal err 8.9e-16, |S U - W| = 4.4e-16, |S^T S - I| = 6.7e-16, det S = +1.000
planar 4 vectors                 det(S0)=-1: kernel-preserved err 1.7e-16, image basis orthonormal err 4.4e-16, |S U - W| = 6.7e-16, |S^T S - I| = 4.4e-16, det S = -1.000
Gram-built W, k=2: |S U - W| = 2.2e-16, |S^T S - I| = 5.9e-16
Gram-built W, k=3: |S U - W| = 8.9e-16, |S^T S - I| = 2.6e-15
negative control: unequal Gram matrices correctly rejected
match check: max |q + S((p+u_i)-p) - (q+w_i)| = 6.661338147750939e-16
```


## (f) d = 3 rich motions on small grids (sanity of Theorem 7.1's scale)

`f_motions.py` uses lattice isometries: 48 signed permutations times all integer translations, t = 3..7. For t = 3, 4 it adds rational rotations from integer quaternions of bounded norm (a partial enumeration).

`f2_all_isometries.py` is exhaustive over **all** isometries of R³ with a non-collinear match set, for t = 3. Such a g maps two independent difference vectors of P to difference vectors with the same Gram matrix. All 721 152 candidate linear parts were generated and deduplicated to 13 392 orthogonal S; the 48 lattice ones serve as a positive control. Collinear match sets have k ≤ 3 < A.

Σ_{k≥C_rich A} k² / N^{10/3} comes out between 1.5 and 4.3 for C_rich ∈ {1, 2}, decreasing in t. The non-lattice motions add exactly the 192 motions with k = 9 = A that the partial rational enumeration also found. Caveat (objection 7): the grid violates M ≤ A but satisfies the line cap that the proof actually uses. This is a scale sanity check, not a test of K_rich.

Script `numerics_scripts/f_motions.py` — verbatim output:

```
t=3 N= 27 A=  9.0 N^(10/3)=5.905e+04 | lattice: max k=27 | C_rich=1: #motions=1200, sum k^2=234576, /N^(10/3)=3.9726 | C_rich=2: #motions=336, sum k^2=128304, /N^(10/3)=2.1728
      + 11600 rational-rotation motions (quaternion norm <= 50): max k = 9, #with k>=A: 192, #with k>=4: 24000
t=4 N= 64 A= 16.0 N^(10/3)=1.049e+06 | lattice: max k=64 | C_rich=1: #motions=4752, sum k^2=3439488, /N^(10/3)=3.2802 | C_rich=2: #motions=1200, sum k^2=1901568, /N^(10/3)=1.8135
      + 4368 rational-rotation motions (quaternion norm <= 30): max k = 18, #with k>=A: 2016, #with k>=4: 657408
t=5 N=125 A= 25.0 N^(10/3)=9.766e+06 | lattice: max k=125 | C_rich=1: #motions=10032, sum k^2=25209648, /N^(10/3)=2.5815 | C_rich=2: #motions=3024, sum k^2=15376464, /N^(10/3)=1.5745
t=6 N=216 A= 36.0 N^(10/3)=6.047e+07 | lattice: max k=216 | C_rich=1: #motions=23568, sum k^2=137188992, /N^(10/3)=2.2689 | C_rich=2: #motions=9648, sum k^2=103928064, /N^(10/3)=1.7188
t=7 N=343 A= 49.0 N^(10/3)=2.825e+08 | lattice: max k=343 | C_rich=1: #motions=39792, sum k^2=549335184, /N^(10/3)=1.9447 | C_rich=2: #motions=17808, sum k^2=435394224, /N^(10/3)=1.5414
t=3: sum over all lattice motions of k^2 = 329232;  /N^3 = 16.73;  /N^(10/3) = 5.5756
t=4: sum over all lattice motions of k^2 = 4088832;  /N^3 = 15.60;  /N^(10/3) = 3.8994
t=5: sum over all lattice motions of k^2 = 29478000;  /N^3 = 15.09;  /N^(10/3) = 3.0185
t=6: sum over all lattice motions of k^2 = 149382528;  /N^3 = 14.82;  /N^(10/3) = 2.4705
t=7: sum over all lattice motions of k^2 = 591666768;  /N^3 = 14.66;  /N^(10/3) = 2.0946
```

Script `numerics_scripts/f2_all_isometries.py` — verbatim output:

```
  raw (u1,u2,w1,w2,sign) candidates: 721152
t=3: N=27, A=9.00; distinct orthogonal S mapping two independent difference vectors to difference vectors: 13392
  of which signed permutations (lattice S): 48 (expected 48)
  match-count distribution over all (S,h) with k>=4: {4: 17280, 5: 1152, 6: 7680, 8: 384, 9: 480, 12: 576, 18: 288, 27: 48}
  C_rich=0.5: #motions with k >= 4.5: 10608, sum k^2 = 579984, / N^(10/3) = 9.8221
  C_rich=1.0: #motions with k >= 9.0: 1392, sum k^2 = 250128, / N^(10/3) = 4.2359
  C_rich=2.0: #motions with k >= 18.0: 336, sum k^2 = 128304, / N^(10/3) = 2.1728
```


## (g) Lemma 2.1 circle and line rows

"A circle contains at most 2M points", with M = 1 + |Δ|. Findings:
- The proof gives 2M − 1.
- Regular odd polygons attain 2M − 1 exactly: the extremal configuration is the regular (2k+1)-gon, with |Δ| = k.
- Regular even polygons, with or without the centre, do not attain it.
- Exhaustive subsets of the regular 12- and 13-gons never exceed 2M − 1.
- Subsets of the integer points on x²+y² = 25 and = 65 stay strictly below it.

Line row: n collinear points have M ≥ n, so "2M" is loose by a factor 2. See objection 1.

Script `numerics_scripts/g_circle.py` — verbatim output:

```
== regular n-gon (all vertices on the circle): |Delta| = #distinct chords, M = 1+|Delta|; claim n <= 2M (proof gives n <= 2M-1) ==
  n= 3: |Delta|=1, M=2, 2M=4, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n= 4: |Delta|=2, M=3, 2M=6, n<=2M: True, n<=2M-1: True
  n= 5: |Delta|=2, M=3, 2M=6, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n= 6: |Delta|=3, M=4, 2M=8, n<=2M: True, n<=2M-1: True
  n= 7: |Delta|=3, M=4, 2M=8, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n= 8: |Delta|=4, M=5, 2M=10, n<=2M: True, n<=2M-1: True
  n= 9: |Delta|=4, M=5, 2M=10, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=10: |Delta|=5, M=6, 2M=12, n<=2M: True, n<=2M-1: True
  n=11: |Delta|=5, M=6, 2M=12, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=12: |Delta|=6, M=7, 2M=14, n<=2M: True, n<=2M-1: True
  n=13: |Delta|=6, M=7, 2M=14, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=14: |Delta|=7, M=8, 2M=16, n<=2M: True, n<=2M-1: True
  n=15: |Delta|=7, M=8, 2M=16, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=16: |Delta|=8, M=9, 2M=18, n<=2M: True, n<=2M-1: True
  n=17: |Delta|=8, M=9, 2M=18, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=18: |Delta|=9, M=10, 2M=20, n<=2M: True, n<=2M-1: True
  n=19: |Delta|=9, M=10, 2M=20, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=20: |Delta|=10, M=11, 2M=22, n<=2M: True, n<=2M-1: True
  n=21: |Delta|=10, M=11, 2M=22, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=22: |Delta|=11, M=12, 2M=24, n<=2M: True, n<=2M-1: True
  n=23: |Delta|=11, M=12, 2M=24, n<=2M: True, n<=2M-1: True  <-- equality n=2M-1
  n=24: |Delta|=12, M=13, 2M=26, n<=2M: True, n<=2M-1: True
== regular 2k-gon + centre (centre is off the circle, so the circle still carries 2k points; M can only grow) ==
  2k= 4+centre: |Delta|=3, M=4, circle points 4 <= 2M=8: True
  2k= 6+centre: |Delta|=3, M=4, circle points 6 <= 2M=8: True
  2k= 8+centre: |Delta|=5, M=6, circle points 8 <= 2M=12: True
  2k=10+centre: |Delta|=6, M=7, circle points 10 <= 2M=14: True
  2k=12+centre: |Delta|=6, M=7, circle points 12 <= 2M=14: True
  2k=14+centre: |Delta|=8, M=9, circle points 14 <= 2M=18: True
  2k=16+centre: |Delta|=9, M=10, circle points 16 <= 2M=20: True
== exhaustive: every subset (|S|>=2) of vertices of the regular 12-gon and 13-gon; max over subsets of |S| - (2M-1) ==
  n=12: max (|S| - (2M-1)) = 0 attained e.g. by |S|=3, M=2, S=(0, 4, 8)
  n=13: max (|S| - (2M-1)) = 0 attained e.g. by |S|=13, M=7, S=(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
== exhaustive subsets of the 12 integer points on x^2+y^2=25 and the 16 on x^2+y^2=65 (exact integer squared distances) ==
  R^2=25: 12 lattice points; max (|S|-(2M-1)) over subsets of size<=12 = -1 (|S|=2, M=2)
  R^2=65: 16 lattice points; max (|S|-(2M-1)) over subsets of size<=12 = -1 (|S|=2, M=2)
== line row: n collinear points, from an endpoint all distances distinct => n <= M (paper states 2M) ==
  arithmetic progression n=2: M=2, n<=M: True, n<=2M: True
  arithmetic progression n=3: M=3, n<=M: True, n<=2M: True
  arithmetic progression n=4: M=4, n<=M: True, n<=2M: True
  arithmetic progression n=5: M=5, n<=M: True, n<=2M: True
  arithmetic progression n=6: M=6, n<=M: True, n<=2M: True
  arithmetic progression n=7: M=7, n<=M: True, n<=2M: True
  arithmetic progression n=8: M=8, n<=M: True, n<=2M: True
  arithmetic progression n=9: M=9, n<=M: True, n<=2M: True
  arithmetic progression n=10: M=10, n<=M: True, n<=2M: True
  arithmetic progression n=11: M=11, n<=M: True, n<=2M: True
```


## (h) Hilbert-function toys for Lemma 3.6

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

In (2.3) the components live in P^{d−1} and can have degree up to D^{codim}. The toys with a = D² and a = D³ cover that regime: they still sit far above c_{n,k}.

Script `numerics_scripts/h3_hilbert.py` — verbatim output:

```
== T1: D' concurrent lines through [0:0:1] in P^2 (n=2,k=1), tested at degree D ==
  1 concurrent lines @deg D=1                    n=2 k=1 a=   1 L= 1: H=    2  H/(aL^k)= 2.000  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 concurrent lines @deg D=1                    n=2 k=1 a=   2 L= 1: H=    3  H/(aL^k)= 1.500  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  4 concurrent lines @deg D=1                    n=2 k=1 a=   4 L= 1: H=    3  H/(aL^k)= 0.750  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  8 concurrent lines @deg D=1                    n=2 k=1 a=   8 L= 1: H=    3  H/(aL^k)= 0.375  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  1 concurrent lines @deg D=2                    n=2 k=1 a=   1 L= 2: H=    3  H/(aL^k)= 1.500  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 concurrent lines @deg D=2                    n=2 k=1 a=   2 L= 2: H=    5  H/(aL^k)= 1.250  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 concurrent lines @deg D=2                    n=2 k=1 a=   3 L= 2: H=    6  H/(aL^k)= 1.000  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  6 concurrent lines @deg D=2                    n=2 k=1 a=   6 L= 2: H=    6  H/(aL^k)= 0.500  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  12 concurrent lines @deg D=2                   n=2 k=1 a=  12 L= 2: H=    6  H/(aL^k)= 0.250  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  1 concurrent lines @deg D=3                    n=2 k=1 a=   1 L= 3: H=    4  H/(aL^k)= 1.333  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 concurrent lines @deg D=3                    n=2 k=1 a=   3 L= 3: H=    9  H/(aL^k)= 1.000  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 concurrent lines @deg D=3                    n=2 k=1 a=   4 L= 3: H=   10  H/(aL^k)= 0.833  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  8 concurrent lines @deg D=3                    n=2 k=1 a=   8 L= 3: H=   10  H/(aL^k)= 0.417  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  16 concurrent lines @deg D=3                   n=2 k=1 a=  16 L= 3: H=   10  H/(aL^k)= 0.208  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  1 concurrent lines @deg D=4                    n=2 k=1 a=   1 L= 4: H=    5  H/(aL^k)= 1.250  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 concurrent lines @deg D=4                    n=2 k=1 a=   2 L= 4: H=    9  H/(aL^k)= 1.125  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 concurrent lines @deg D=4                    n=2 k=1 a=   4 L= 4: H=   14  H/(aL^k)= 0.875  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  5 concurrent lines @deg D=4                    n=2 k=1 a=   5 L= 4: H=   15  H/(aL^k)= 0.750  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  10 concurrent lines @deg D=4                   n=2 k=1 a=  10 L= 4: H=   15  H/(aL^k)= 0.375  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  20 concurrent lines @deg D=4                   n=2 k=1 a=  20 L= 4: H=   15  H/(aL^k)= 0.188  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  1 concurrent lines @deg D=5                    n=2 k=1 a=   1 L= 5: H=    6  H/(aL^k)= 1.200  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 concurrent lines @deg D=5                    n=2 k=1 a=   2 L= 5: H=   11  H/(aL^k)= 1.100  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  5 concurrent lines @deg D=5                    n=2 k=1 a=   5 L= 5: H=   20  H/(aL^k)= 0.800  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  6 concurrent lines @deg D=5                    n=2 k=1 a=   6 L= 5: H=   21  H/(aL^k)= 0.700  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  12 concurrent lines @deg D=5                   n=2 k=1 a=  12 L= 5: H=   21  H/(aL^k)= 0.350  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  24 concurrent lines @deg D=5                   n=2 k=1 a=  24 L= 5: H=   21  H/(aL^k)= 0.175  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  1 concurrent lines @deg D=6                    n=2 k=1 a=   1 L= 6: H=    7  H/(aL^k)= 1.167  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 concurrent lines @deg D=6                    n=2 k=1 a=   3 L= 6: H=   18  H/(aL^k)= 1.000  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  6 concurrent lines @deg D=6                    n=2 k=1 a=   6 L= 6: H=   27  H/(aL^k)= 0.750  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  7 concurrent lines @deg D=6                    n=2 k=1 a=   7 L= 6: H=   28  H/(aL^k)= 0.667  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  14 concurrent lines @deg D=6                   n=2 k=1 a=  14 L= 6: H=   28  H/(aL^k)= 0.333  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  28 concurrent lines @deg D=6                   n=2 k=1 a=  28 L= 6: H=   28  H/(aL^k)= 0.167  c_nk=0.2500  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  same lines at their defining degree L = D' (one equation: product of D' linear forms):
  2 concurrent lines @deg L=D'=2                 n=2 k=1 a=   2 L= 2: H=    5  H/(aL^k)= 1.250  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 concurrent lines @deg L=D'=4                 n=2 k=1 a=   4 L= 4: H=   14  H/(aL^k)= 0.875  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  8 concurrent lines @deg L=D'=8                 n=2 k=1 a=   8 L= 8: H=   44  H/(aL^k)= 0.688  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  12 concurrent lines @deg L=D'=12               n=2 k=1 a=  12 L=12: H=   90  H/(aL^k)= 0.625  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  20 concurrent lines @deg L=D'=20               n=2 k=1 a=  20 L=20: H=  230  H/(aL^k)= 0.575  c_nk=0.2500  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  failure threshold when the hypothesis is dropped: H(D) = C(D+2,2) < c*D'*D  iff  D' > C(D+2,2)/(c D); c=1/4, D=3: D' > 13.333333333333334
== T2: complete intersection of two degree-D surfaces in P^3 (curve, degree D^2), at L = D ==
  product CI (D^2 lines), D=1                    n=3 k=1 a=   1 L= 1: H=    2  H/(aL^k)= 2.000  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  product CI (D^2 lines), D=2                    n=3 k=1 a=   4 L= 2: H=    8  H/(aL^k)= 1.000  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  product CI (D^2 lines), D=3                    n=3 k=1 a=   9 L= 3: H=   18  H/(aL^k)= 0.667  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  product CI (D^2 lines), D=4                    n=3 k=1 a=  16 L= 4: H=   33  H/(aL^k)= 0.516  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  product CI (D^2 lines), D=5                    n=3 k=1 a=  25 L= 5: H=   54  H/(aL^k)= 0.432  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  random CI (smooth, reduced: I(Y)=(f,g)), D=1   n=3 k=1 a=   1 L= 1: H=    2  H/(aL^k)= 2.000  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: minimal q = 0  vs (n-k)(L-1) = 0: True
  random CI (smooth, reduced: I(Y)=(f,g)), D=2   n=3 k=1 a=   4 L= 2: H=    8  H/(aL^k)= 1.000  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: minimal q = 1  vs (n-k)(L-1) = 2: True
  random CI (smooth, reduced: I(Y)=(f,g)), D=3   n=3 k=1 a=   9 L= 3: H=   18  H/(aL^k)= 0.667  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: minimal q = 2  vs (n-k)(L-1) = 4: True
  random CI (smooth, reduced: I(Y)=(f,g)), D=4   n=3 k=1 a=  16 L= 4: H=   33  H/(aL^k)= 0.516  c_nk=0.0370  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: minimal q = 3  vs (n-k)(L-1) = 6: True
== T3: a points in P^2 (n=2,k=0): general position vs collinear, at degree D ==
  2 general points @D=2                          n=2 k=0 a=   2 L= 2: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 collinear points @D=2                        n=2 k=0 a=   2 L= 2: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 general points @D=2                          n=2 k=0 a=   3 L= 2: H=    3  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 collinear points @D=2                        n=2 k=0 a=   3 L= 2: H=    3  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  4 general points @D=2                          n=2 k=0 a=   4 L= 2: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 collinear points @D=2                        n=2 k=0 a=   4 L= 2: H=    3  H/(aL^k)= 0.750  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  6 general points @D=2                          n=2 k=0 a=   6 L= 2: H=    6  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  6 collinear points @D=2                        n=2 k=0 a=   6 L= 2: H=    3  H/(aL^k)= 0.500  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  12 general points @D=2                         n=2 k=0 a=  12 L= 2: H=    6  H/(aL^k)= 0.500  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  12 collinear points @D=2                       n=2 k=0 a=  12 L= 2: H=    3  H/(aL^k)= 0.250  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  2 general points @D=3                          n=2 k=0 a=   2 L= 3: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 collinear points @D=3                        n=2 k=0 a=   2 L= 3: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 general points @D=3                          n=2 k=0 a=   3 L= 3: H=    3  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  3 collinear points @D=3                        n=2 k=0 a=   3 L= 3: H=    3  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 general points @D=3                          n=2 k=0 a=   4 L= 3: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 collinear points @D=3                        n=2 k=0 a=   4 L= 3: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  5 general points @D=3                          n=2 k=0 a=   5 L= 3: H=    5  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  5 collinear points @D=3                        n=2 k=0 a=   5 L= 3: H=    4  H/(aL^k)= 0.800  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  8 general points @D=3                          n=2 k=0 a=   8 L= 3: H=    8  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  8 collinear points @D=3                        n=2 k=0 a=   8 L= 3: H=    4  H/(aL^k)= 0.500  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  10 general points @D=3                         n=2 k=0 a=  10 L= 3: H=   10  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  10 collinear points @D=3                       n=2 k=0 a=  10 L= 3: H=    4  H/(aL^k)= 0.400  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  20 general points @D=3                         n=2 k=0 a=  20 L= 3: H=   10  H/(aL^k)= 0.500  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  20 collinear points @D=3                       n=2 k=0 a=  20 L= 3: H=    4  H/(aL^k)= 0.200  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  2 general points @D=4                          n=2 k=0 a=   2 L= 4: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  2 collinear points @D=4                        n=2 k=0 a=   2 L= 4: H=    2  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 general points @D=4                          n=2 k=0 a=   4 L= 4: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  4 collinear points @D=4                        n=2 k=0 a=   4 L= 4: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  5 general points @D=4                          n=2 k=0 a=   5 L= 4: H=    5  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  5 collinear points @D=4                        n=2 k=0 a=   5 L= 4: H=    5  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  6 general points @D=4                          n=2 k=0 a=   6 L= 4: H=    6  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  6 collinear points @D=4                        n=2 k=0 a=   6 L= 4: H=    5  H/(aL^k)= 0.833  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  13 general points @D=4                         n=2 k=0 a=  13 L= 4: H=   13  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  13 collinear points @D=4                       n=2 k=0 a=  13 L= 4: H=    5  H/(aL^k)= 0.385  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  15 general points @D=4                         n=2 k=0 a=  15 L= 4: H=   15  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  15 collinear points @D=4                       n=2 k=0 a=  15 L= 4: H=    5  H/(aL^k)= 0.333  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  30 general points @D=4                         n=2 k=0 a=  30 L= 4: H=   15  H/(aL^k)= 0.500  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  30 collinear points @D=4                       n=2 k=0 a=  30 L= 4: H=    5  H/(aL^k)= 0.167  c_nk=0.1111  hyp(components of degree-L locus)=False  lower-ok=None  (3.5) H<=aC(L+k,k)=True
  collinear points at their defining degree L = a (line + one degree-a form): H(a) = a, ratio 1
== T4: 0-dimensional complete intersections (all D^n points are components), at L = D ==
  CI of two degree-1 curves in P^2 (grid)        n=2 k=0 a=   1 L= 1: H=    1  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 0  vs (n-k)(L-1) = 0: q = 0 <= 0: True
  CI of two degree-2 curves in P^2 (grid)        n=2 k=0 a=   4 L= 2: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 2  vs (n-k)(L-1) = 2: q = 2 <= 2: True
  CI of two degree-3 curves in P^2 (grid)        n=2 k=0 a=   9 L= 3: H=    8  H/(aL^k)= 0.889  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 4  vs (n-k)(L-1) = 4: q = 4 <= 4: True
  CI of two degree-4 curves in P^2 (grid)        n=2 k=0 a=  16 L= 4: H=   13  H/(aL^k)= 0.812  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 6  vs (n-k)(L-1) = 6: q = 6 <= 6: True
  CI of two degree-5 curves in P^2 (grid)        n=2 k=0 a=  25 L= 5: H=   19  H/(aL^k)= 0.760  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 8  vs (n-k)(L-1) = 8: q = 8 <= 8: True
  CI of two degree-6 curves in P^2 (grid)        n=2 k=0 a=  36 L= 6: H=   26  H/(aL^k)= 0.722  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
      (3.6) shift: H(m) = a first at m = 10  vs (n-k)(L-1) = 10: q = 10 <= 10: True
  CI of three degree-1 surfaces in P^3 (grid)    n=3 k=0 a=   1 L= 1: H=    1  H/(aL^k)= 1.000  c_nk=0.0156  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  CI of three degree-2 surfaces in P^3 (grid)    n=3 k=0 a=   8 L= 2: H=    7  H/(aL^k)= 0.875  c_nk=0.0156  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  CI of three degree-3 surfaces in P^3 (grid)    n=3 k=0 a=  27 L= 3: H=   17  H/(aL^k)= 0.630  c_nk=0.0156  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  CI of three degree-4 surfaces in P^3 (grid)    n=3 k=0 a=  64 L= 4: H=   32  H/(aL^k)= 0.500  c_nk=0.0156  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
== T5: isolated points of {l f = l g = 0} (extra 1-dim component l), f=prod(x-i), g=prod(y-j), deg L-1, at L ==
  isolated grid of 1 pts (+ a line), L=2         n=2 k=0 a=   1 L= 2: H=    1  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  isolated grid of 4 pts (+ a line), L=3         n=2 k=0 a=   4 L= 3: H=    4  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  isolated grid of 9 pts (+ a line), L=4         n=2 k=0 a=   9 L= 4: H=    9  H/(aL^k)= 1.000  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  isolated grid of 16 pts (+ a line), L=5        n=2 k=0 a=  16 L= 5: H=   15  H/(aL^k)= 0.938  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  isolated grid of 25 pts (+ a line), L=6        n=2 k=0 a=  25 L= 6: H=   22  H/(aL^k)= 0.880  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
  isolated grid of 36 pts (+ a line), L=7        n=2 k=0 a=  36 L= 7: H=   30  H/(aL^k)= 0.833  c_nk=0.1111  hyp(components of degree-L locus)=True  lower-ok=True  (3.5) H<=aC(L+k,k)=True
== summary ==
  toys satisfying the hypothesis: 62; lower bound H >= c_nk a L^k violated in: 0
  min over hypothesis-satisfying toys of (H/(aL^k))/c_nk = 2.300
  toys violating the hypothesis: 38; of these, H < c_nk a L^k in 4  (hypothesis is needed)
  upper bound (3.5) violated in: 0 of 100
```

Script `numerics_scripts/h2_lemma36.py` — verbatim output:

```
== (3.8) H_V(bL) <= b^n H_V(L), n=2, on k x k grids and on random point sets ==
  grid   k=3 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  grid   k=3 L=1 b=3: H(L)=  3 H(bL)=  8 b^2 H(L)= 27 ok=True
  grid   k=3 L=2 b=2: H(L)=  6 H(bL)=  9 b^2 H(L)= 24 ok=True
  grid   k=3 L=2 b=3: H(L)=  6 H(bL)=  9 b^2 H(L)= 54 ok=True
  grid   k=3 L=3 b=2: H(L)=  8 H(bL)=  9 b^2 H(L)= 32 ok=True
  grid   k=3 L=3 b=3: H(L)=  8 H(bL)=  9 b^2 H(L)= 72 ok=True
  random k=3 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  random k=3 L=1 b=3: H(L)=  3 H(bL)=  9 b^2 H(L)= 27 ok=True
  random k=3 L=2 b=2: H(L)=  6 H(bL)=  9 b^2 H(L)= 24 ok=True
  random k=3 L=2 b=3: H(L)=  6 H(bL)=  9 b^2 H(L)= 54 ok=True
  random k=3 L=3 b=2: H(L)=  9 H(bL)=  9 b^2 H(L)= 36 ok=True
  random k=3 L=3 b=3: H(L)=  9 H(bL)=  9 b^2 H(L)= 81 ok=True
  grid   k=5 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  grid   k=5 L=1 b=3: H(L)=  3 H(bL)= 10 b^2 H(L)= 27 ok=True
  grid   k=5 L=2 b=2: H(L)=  6 H(bL)= 15 b^2 H(L)= 24 ok=True
  grid   k=5 L=2 b=3: H(L)=  6 H(bL)= 22 b^2 H(L)= 54 ok=True
  grid   k=5 L=3 b=2: H(L)= 10 H(bL)= 22 b^2 H(L)= 40 ok=True
  grid   k=5 L=3 b=3: H(L)= 10 H(bL)= 25 b^2 H(L)= 90 ok=True
  random k=5 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  random k=5 L=1 b=3: H(L)=  3 H(bL)= 10 b^2 H(L)= 27 ok=True
  random k=5 L=2 b=2: H(L)=  6 H(bL)= 15 b^2 H(L)= 24 ok=True
  random k=5 L=2 b=3: H(L)=  6 H(bL)= 25 b^2 H(L)= 54 ok=True
  random k=5 L=3 b=2: H(L)= 10 H(bL)= 25 b^2 H(L)= 40 ok=True
  random k=5 L=3 b=3: H(L)= 10 H(bL)= 25 b^2 H(L)= 90 ok=True
  grid   k=7 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  grid   k=7 L=1 b=3: H(L)=  3 H(bL)= 10 b^2 H(L)= 27 ok=True
  grid   k=7 L=2 b=2: H(L)=  6 H(bL)= 15 b^2 H(L)= 24 ok=True
  grid   k=7 L=2 b=3: H(L)=  6 H(bL)= 28 b^2 H(L)= 54 ok=True
  grid   k=7 L=3 b=2: H(L)= 10 H(bL)= 28 b^2 H(L)= 40 ok=True
  grid   k=7 L=3 b=3: H(L)= 10 H(bL)= 43 b^2 H(L)= 90 ok=True
  random k=7 L=1 b=2: H(L)=  3 H(bL)=  6 b^2 H(L)= 12 ok=True
  random k=7 L=1 b=3: H(L)=  3 H(bL)= 10 b^2 H(L)= 27 ok=True
  random k=7 L=2 b=2: H(L)=  6 H(bL)= 15 b^2 H(L)= 24 ok=True
  random k=7 L=2 b=3: H(L)=  6 H(bL)= 28 b^2 H(L)= 54 ok=True
  random k=7 L=3 b=2: H(L)= 10 H(bL)= 28 b^2 H(L)= 40 ok=True
  random k=7 L=3 b=3: H(L)= 10 H(bL)= 49 b^2 H(L)= 90 ok=True
  violations: 0
== isolated points of {l*f = l*g = 0}: l a line (1-dim component), f=prod(x-i), g=prod(y-j) of degree L-1 ==
  L=2: a=1 isolated points, surjectivity degree q=0 (<= 2L=4: True), H_V(L)=1, H_V(L)/a=1.000
  L=3: a=4 isolated points, surjectivity degree q=2 (<= 2L=6: True), H_V(L)=4, H_V(L)/a=1.000
  L=4: a=9 isolated points, surjectivity degree q=4 (<= 2L=8: True), H_V(L)=9, H_V(L)/a=1.000
  L=5: a=16 isolated points, surjectivity degree q=6 (<= 2L=10: True), H_V(L)=15, H_V(L)/a=0.938
  L=6: a=25 isolated points, surjectivity degree q=8 (<= 2L=12: True), H_V(L)=22, H_V(L)/a=0.880
  L=7: a=36 isolated points, surjectivity degree q=10 (<= 2L=14: True), H_V(L)=30, H_V(L)/a=0.833
```


## (i) Explicit constants and exponent inequalities in §5–6

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

No inequality in §5–6 compares δ with an uncontrolled exp(o(s)) factor. Every contradiction rests on a fixed positive multiple of s.

Script `numerics_scripts/i_sec56.py` — verbatim output:

```
== 5.1 thresholds (5.3): a_K = s^(1/10), a_i = 10 a_{i+1}; claims sum_{r>i} a_r < a_i/9, (5.4) exponent -a_i/2+sum_{r>i}a_r <= -7a_i/18 ==
  max over K<=39, i of (-a_i/2 + sum_(r>i) a_r)/a_i = -38888888888888888888888888888888888889/100000000000000000000000000000000000000 = -0.388889  vs claimed <= -7/18 = -0.388889: True
  exact: sum_{r>i} a_r / a_i -> sum_{m>=1} 10^-m = 1/9 (strict for finite K); 1/2 - 1/9 = 7/18 = 7/18
  sum_i a_i = s^(1/10) (10^K - 1)/9 with K = O(1+sqrt(log s)): log_s of 10^K factor -> 0, so sum = s^(1/10+o(1)):
    s=1e+02: K=4, sum a_i = 1.761e+03, log(sum)/log(s) = 1.623, sum/s^(1/3) = 3.794e+02
    s=1e+04: K=5, sum a_i = 2.791e+04, log(sum)/log(s) = 1.111, sum/s^(1/3) = 1.295e+03
    s=1e+08: K=6, sum a_i = 7.011e+05, log(sum)/log(s) = 0.731, sum/s^(1/3) = 1.510e+03
    s=1e+16: K=8, sum a_i = 4.423e+08, log(sum)/log(s) = 0.540, sum/s^(1/3) = 2.053e+03
    s=1e+32: K=10, sum a_i = 1.761e+12, log(sum)/log(s) = 0.383, sum/s^(1/3) = 3.794e+01
    s=1e+64: K=14, sum a_i = 2.791e+19, log(sum)/log(s) = 0.304, sum/s^(1/3) = 1.295e-02
  NOTE: o(s^(1/3)) holds asymptotically, but sum/s^(1/3) < 1 only for astronomically large s with this K (between 1e32 and 1e64 above) -- harmless: only the limit is used, no rate is claimed.
== (5.5) summability over dyadic widths 2^m u, u >= s_*: claims 2^(m/10) >= 1+cm (c = log2/10) and sqrt(log(2^m u)) <= sqrt(log u)+sqrt(m log 2) ==
  violations over m<400, u in {2,10,1e3,1e9}: 0
    u=1e+02: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = 1.911e+01;  sum_m exp(-(2^m u)^(1/3)) = 1.326e-02  (both -> 0 as u -> oo)
    u=1e+04: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = 1.020e+01;  sum_m exp(-(2^m u)^(1/3)) = 4.416e-10  (both -> 0 as u -> oo)
    u=1e+06: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = 3.961e+00;  sum_m exp(-(2^m u)^(1/3)) = 3.720e-44  (both -> 0 as u -> oo)
    u=1e+10: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = 1.192e-01;  sum_m exp(-(2^m u)^(1/3)) = 0.000e+00  (both -> 0 as u -> oo)
    u=1e+20: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = 1.544e-21;  sum_m exp(-(2^m u)^(1/3)) = 0.000e+00  (both -> 0 as u -> oo)
== 5.1 lower boundary: N exp(-sqrt(2s)) / (N exp(-sqrt(s) - o(s^(1/3)))) = exp(-(sqrt2-1)sqrt(s)+o(s^(1/3))) ==
  exponent difference -sqrt(2s)+sqrt(s) = sqrt(s)*(1 - sqrt(2)) ; coefficient sqrt2-1 = 0.41421356237309503 > 0, and s^(1/3) = o(sqrt s)
== 5.1 core: on entry to the last width s_f in [s_*, 2 s_*], degree B exp((1+o(1)) s_f) <= B exp(3 s_*);  E L^2 = (delta N/A) B^2 exp(6 s_*) ==
  E*L^2 / N = delta*exp(6*s_star)  -> 0 by the choice delta*exp(6 s_*) -> 0
  width halving: batches <= exp(sqrt s); union degree exp(sqrt s)*O(B e^{s/2}) = B exp(s/2 + O(sqrt s)) = B exp((1+o(1)) s/2): relative error O(sqrt(s))/(s/2) -> 0
== (5.6)-(5.7) profiles: sigma(b) = prod_i min(T,D_i) = e_j T^(d-j) on plateau j; b1+b2<0 from sum=0, b1<0<bd, d>=3 ==
  80000 random admissible profiles (d=3..6): violations of b1+b2<0 or of the sigma plateau identity: 0
  Figure 2 profile (-0.8,-0.4,0.3,0.9): sum = 0 , b1+b2 = -6/5 , max|b| = 9/10
== Prop 5.5: omitted nonreal-line fraction e_{d-1} exp(o(s))/n = exp(o(s))/D_d, D_d = B e^{b_d s} >= B since b_d > 0 ==
  with s <= log B: exp(o(s))/B <= B^{-1+o(1)} -> 0  (exact: e_{d-1}/N = prod_{i<d} D_i / B^d = exp(s*sum_{i<d} b_i)/B = exp(-b_d s)/B)
== (6.5)-(6.7) common window: initial interval rank T^(2d-1) vs sigma^2 * T/(D1 D2) with sigma = T^d and D1 D2 >= T^2 ==
  violations of T^(2d-1) >= T^(2d+1)/(D1 D2) on t < b1 (5000 profiles x d=3..5): 0
  k = d-1 plateau: D1^2 T^(2d-2) min(1, T/(D1 D2)) <= D1 T^(2d-2)  <=>  min(D1, T/D2) <= 1 (true as T <= D2): checked symbolically below
   D1^2 T^(2d-2) * T/(D1 D2) / (D1 T^(2d-2)) = T/D2  <= 1 iff T <= D2
  (6.7) margins at T = D_d, sigma = N: log(A/D_d)/s = (log B)/s - b_d; log(A/(D1 D2))/s = -(b1+b2)
    d=3: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = 0.2559 (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)
    d=4: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = 0.3590 (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)
    d=5: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = 0.2979 (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)
    d=6: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = 0.3680 (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)
  outermost s = log B: margin1 = 1 - b_d, zero iff b_d = 1 (the Sec. 6.2 case)
== (6.9) outermost endpoint: s = log B, b_d = 1, final open plateau of dim k after j = d-k cuts, cuts j+1..d at time 1 ==
  d=3: feasible k = [1]; paper's range 1 <= k < d-1 = [1]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1]
  d=4: feasible k = [1, 2]; paper's range 1 <= k < d-1 = [1, 2]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1, 2]
  d=5: feasible k = [1, 2]; paper's range 1 <= k < d-1 = [1, 2, 3]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1, 2]
  d=6: feasible k = [1, 2, 3]; paper's range 1 <= k < d-1 = [1, 2, 3, 4]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1, 2, 3]
  d=7: feasible k = [1, 2, 3]; paper's range 1 <= k < d-1 = [1, 2, 3, 4, 5]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1, 2, 3]
  d=8: feasible k = [1, 2, 3, 4]; paper's range 1 <= k < d-1 = [1, 2, 3, 4, 5, 6]; e_j = B^(d-2k) >= 1 forces k <= d/2: [1, 2, 3, 4]
  identities: e_j * (B^2)^k = B^d  =>  e_j = B^(d-2k), N/e_j = B^(2k) = A^k
== (6.10)-(6.11), Lemma 6.4 at the outermost endpoint ==
  t0 > 1+b1+b2 is possible below 1 since b1+b2 < 0; normalized logs of T0/T_s(beta) and T0/(D1 D2): t0-beta and t0-(1+b1+b2):
    log(T0/(D1 D2))/s = -b1 - b2 + t0 - 1 = t0 - (1+b1+b2)
    d=4, k=2: deletion mass exponent (d-2k)+(k+1) = 3 < d: True;
    d=5, k=2: deletion mass exponent (d-2k)+(k+1) = 4 < d: True;    d=5, k=3: deletion mass exponent (d-2k)+(k+1) = 3 < d: True;
    d=6, k=2: deletion mass exponent (d-2k)+(k+1) = 5 < d: True;    d=6, k=3: deletion mass exponent (d-2k)+(k+1) = 4 < d: True;    d=6, k=4: deletion mass exponent (d-2k)+(k+1) = 3 < d: True;
    d=7, k=2: deletion mass exponent (d-2k)+(k+1) = 6 < d: True;    d=7, k=3: deletion mass exponent (d-2k)+(k+1) = 5 < d: True;    d=7, k=4: deletion mass exponent (d-2k)+(k+1) = 4 < d: True;    d=7, k=5: deletion mass exponent (d-2k)+(k+1) = 3 < d: True;
    d=8, k=2: deletion mass exponent (d-2k)+(k+1) = 7 < d: True;    d=8, k=3: deletion mass exponent (d-2k)+(k+1) = 6 < d: True;    d=8, k=4: deletion mass exponent (d-2k)+(k+1) = 5 < d: True;    d=8, k=5: deletion mass exponent (d-2k)+(k+1) = 4 < d: True;    d=8, k=6: deletion mass exponent (d-2k)+(k+1) = 3 < d: True;
  test degrees T_s(t2) = B^(1+t2) = B^(2-(1-t2)) with t2 < 1: c = (1-t2)/2 works after constants
  Bezout direction count: C E B^(2-c+o(1))/n with E = delta N/A, n >= N sqrt(delta): = sqrt(delta) * B^(-c+o(1))
  final row count: E M / n <= sqrt(delta)/B**2 * M  = sqrt(delta) M / A -> 0 (no rate needed)
  lift degree: deg(gamma)deg(C->gamma) = deg C - mult_p C >= deg C/2 and sum deg(C->gamma) <= 1  =>  sum deg C <= 2 deg(gamma)
== 6.3 (6.18)-(6.20) and the depth denominators ==
  (6.19): groups of depth <= R e^{eta s}, t_p deg pi_p Y >= deg Y/2  =>  sum_Z deg Z >= a/(2R e^{eta s})
  (6.20)/|P_x|: e_j B^(l+1)/N with e_j = B^j exp(s sum_{i<=j} b_i), l = d-j:
    d=3 j=1: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=3 j=2: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0
    d=4 j=1: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=4 j=2: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=4 j=3: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0
    d=5 j=1: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=5 j=2: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=5 j=3: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=5 j=4: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0
    d=6 j=1: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=6 j=2: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=6 j=3: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=6 j=4: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0;    d=6 j=5: B-exponent j+(l+1)-d = 1 (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0
    wider window: B=1e+06, s=0.05*log B: q=B^(1/2)=1.000e+03, r=ceil(B e^(-2s))=2.512e+05, q/r=3.981e-03, r >= ... B^0.900
    wider window: B=1e+06, s=0.01*log B: q=B^(1/2)=1.000e+03, r=ceil(B e^(-2s))=7.586e+05, q/r=1.318e-03, r >= ... B^0.980
    wider window: B=1e+12, s=0.05*log B: q=B^(1/2)=1.000e+06, r=ceil(B e^(-2s))=6.310e+10, q/r=1.585e-05, r >= ... B^0.900
    wider window: B=1e+12, s=0.01*log B: q=B^(1/2)=1.000e+06, r=ceil(B e^(-2s))=5.754e+11, q/r=1.738e-06, r >= ... B^0.980
    wider window: B=1e+30, s=0.05*log B: q=B^(1/2)=1.000e+15, r=ceil(B e^(-2s))=1.000e+27, q/r=1.000e-12, r >= ... B^0.900
    wider window: B=1e+30, s=0.01*log B: q=B^(1/2)=1.000e+15, r=ceil(B e^(-2s))=2.512e+29, q/r=3.981e-15, r >= ... B^0.980
    wider window: B=1e+100, s=0.05*log B: q=B^(1/2)=1.000e+50, r=ceil(B e^(-2s))=1.000e+90, q/r=1.000e-40, r >= ... B^0.900
    wider window: B=1e+100, s=0.01*log B: q=B^(1/2)=1.000e+50, r=ceil(B e^(-2s))=1.000e+98, q/r=1.000e-48, r >= ... B^0.980
  r - q - O(1) >= r/2 for large B since q = o(r) (q/r = B^(-1/2+o(1)))
  multiplicity compression degree O(L^2/r) with L = B e^{O(s)}, r = B^(1+o(1)): = B e^{O(s)}
== (6.26) strict margins on target plateaux (separated windows), all plateaux j=1..d-1 of random profiles ==
  NO strict negative margin: d=3 narrow case l=1,b_{j+1}>0 : 9974 plateau instances
  NO strict negative margin: d=4 narrow case l=1,b_{j+1}>0 : 10022 plateau instances
  NO strict negative margin: d=5 narrow case l=1,b_{j+1}>0 : 9982 plateau instances
  NO strict negative margin: d=6 narrow case l=1,b_{j+1}>0 : 9975 plateau instances
  NO strict negative margin: d=7 narrow case l=1,b_{j+1}>0 : 10109 plateau instances
  (paper: the only zero-margin case is narrower centres, final one-dimensional plateau l = 1 with b_{j+1} = b_d > 0, handled in 6.5)
  initial interval ratio A/T^2 = exp(-2 b s): positive margin near b1 < 0
  (6.25)/(6.27) at the last endpoint: sigma T e^{cs}/A / (C E T) = sigma e^{cs}/(C delta N) >= e^{cs/2 - o(s)}/(C delta) >= delta^-1 e^{cs/3}
== 6.5: identities on the final narrow curve plateau (j = d-1, R = B exp(-b_d s)) ==
  R*D_d = B**2 = A ;  e_{d-1}/R = B**(d - 2) = N/A
  exceptional degree / projected degree: (delta (N/A) e^{-eta s}) / ((N/A) e^{-eps s}) = delta*exp(s*(epsilon - eta))  -> 0 for 0 < eps < eta
```

## Appendix — scripts, verbatim

Run as `nice -n 19 python3 <script>.py` (f2_all_isometries.py with argument `3`) from /tmp/oaimath/166/numerics_scripts/.

### `a_grid.py`

```python
# (a) grid {1..t}^d: count distinct squared distances exactly; compare with d(t-1)^2 and n^{2/d}=t^2
import itertools
for d in (3, 4):
    for t in range(2, 7):
        # squared distance between two grid points = sum of d squares of coordinate differences in {0..t-1}
        diffs = range(0, t)
        sq = set()
        for v in itertools.product(diffs, repeat=d):
            s = sum(x*x for x in v)
            if s > 0:
                sq.add(s)
        n = t**d
        D = len(sq)
        bound = d*(t-1)**2
        # brute-force cross-check on actual point pairs for small cases
        if n <= 1296:
            pts = list(itertools.product(range(1, t+1), repeat=d))
            sq2 = set()
            for i in range(len(pts)):
                pi = pts[i]
                for j in range(i+1, len(pts)):
                    pj = pts[j]
                    sq2.add(sum((a-b)**2 for a, b in zip(pi, pj)))
            assert sq2 == sq, (d, t)
            chk = "pairs-checked"
        else:
            chk = "diff-vectors"
        print(f"d={d} t={t} n={n:5d} |Delta|={D:3d} <= d(t-1)^2={bound:3d}: {D<=bound}  ratio |Delta|/n^(2/d) = {D/t**2:.4f}  ({chk})")
```

### `b_sv.py`

```python
# (b) Solymosi-Vu recurrences, applied by hand.  Source read: refs/solymosi-vu/sv_combinatorica2008.pdf
# (Combinatorica 28 (1) (2008) 113-125, journal PDF, 13 pp; not on arXiv -- arXiv title/author searches return nothing),
# text: refs/solymosi-vu/sv.txt (pdftotext -layout).  Statements used (verbatim in the report):
#  Thm 2.1: t(A) = Omega(max(n/m^{(d-1)/d}, t_{d-1}(m))), m = max |A cap hyperplane|
#  Thm 2.2: t(A) = Omega(max(n^{(d+1)/2d}/m^{(d-1)/2d}, t_{d-2}(m))), m = max |A cap codim-2 flat|
#  Cor 2.3: t_{d-1}(n)=Omega(n^a) => t_d(n)=Omega(n^{d a/(d a + d-1)});  Cor 2.6: t_{d-2}(n)=Omega(n^a) => t_d(n)=Omega(n^{(d+1)a/(2 d a + d-1)})
#  Fact 2.5 / 2.8 closed forms; sec. 2: "All theorems and corollaries in this section hold ... if we replace t_d(n) by g_d(n)."
from sympy import Rational as R, Symbol, solve, nsolve, log as slog, simplify
import math
def c23(d, a): return d*a/(d*a + d - 1)
def c26(d, a): return (d+1)*a/(2*d*a + d - 1)
def f25(d, d0, a0): return R(2*d)/((d+d0+1)*(d-d0) + 2*d0/a0)
def f28(d, d0, a0): return R(2*(d+1))/((d+d0+2)*(d-d0) + 2*(d0+1)/a0)

print("== consistency of SV's own statements ==")
a2 = 0.8635
print("  Thm 1.1(a): Cor 2.3 at d=3 with Tardos a2=.8635:  3a2/(3a2+2) =", round(3*a2/(3*a2+2), 6), " (SV: .5643)")
for d in range(4, 11):
    e = 2*(d+1)/(d*d + 2*d - 8 + 6/a2) if d % 2 == 0 else 2*(d+1)/(d*d + 2*d - 15 + 8/0.5643)
    print(f"  Cor 1.3 d={d}: {e:.5f} > 2/d-2/(d(d+2)) = {2/d-2/(d*(d+2)):.5f}: {e > 2/d-2/(d*(d+2))}")
print("  Fact 2.8 with d0=2 equals Cor 1.3(3):", all(simplify(f28(d, 2, Symbol('a')) - 2*(d+1)/(d*d+2*d-8+6/Symbol('a'))) == 0 for d in (4, 6, 8)),
      "; with d0=3 equals Cor 1.3(4):", all(simplify(f28(d, 3, Symbol('a')) - 2*(d+1)/(d*d+2*d-15+8/Symbol('a'))) == 0 for d in (5, 7, 9)))

print("== (i) Guth-Katz g_2(m) >= c m/log m into Thm 2.1 at d=3 (the log form; Cor 2.3 needs a pure power) ==")
print("  pure-power shadow: Cor 2.3 with a=1 at d=3:", c23(3, R(1)))
print("  exact asymptotics: minimise max(n m^(-2/3), m/ln m) over m; the minimum is at the crossing n = m^(5/3)/ln m,")
print("  value V = m/ln m;  ln m ~ (3/5) ln n  =>  V ~ n^(3/5) ((3/5) ln n)^(-2/5) = (5/3)^(2/5) n^(3/5)/(ln n)^(2/5); (5/3)^(2/5) =", round((5/3)**0.4, 6))
for k in (6, 12, 24, 50, 100, 200, 300):
    lnn = k*math.log(10)
    # solve (5/3) ln m - ln ln m = ln n for x = ln m by Newton
    x = 0.6*lnn
    for _ in range(100):
        F = (5/3)*x - math.log(x) - lnn; x -= F/((5/3) - 1/x)
    lnV = x - math.log(x)
    ratio = math.exp(lnV - (0.6*lnn - 0.4*math.log(lnn)))
    print(f"    n=1e{k}: min max(...) / (n^(3/5)/(ln n)^(2/5)) = {ratio:.5f}")
print("  => Theta(n^(3/5)/(log n)^(2/5)): exponent 3/5, log power 2/5 (paper Sec. 1.1: Omega(n^{3/5}/(log n)^{2/5}) [21, Theorem 2.1])")

print("== (ii) Tidor-Yu-Zakharov g_3(n) >= n^{2/3-o(1)} ==")
a3 = R(2, 3)
print("  d=4 via Cor 2.3 (from d=3):", c23(4, a3), " (paper: 8/17)   [Fact 2.5 d0=3:", f25(4, 3, a3), "]")
print("  d=4 via Cor 2.6 (from d=2, Guth-Katz a=1):", c26(4, R(1)), "= ", float(c26(4, R(1))), "< 8/17")
print("  d=5 via Cor 2.6 (from d=3):", c26(5, a3), " (paper: 3/8)   [Fact 2.8 d0=3:", f28(5, 3, a3), "]")
print("  d=5 via Cor 2.3 (from d=4 = 8/17):", c23(5, c23(4, a3)), "=", float(c23(5, c23(4, a3))), "< 3/8")
eps = R(1, 10**6)
print("  o(1) bookkeeping: inputs 2/3-eps give d=4:", float(c23(4, a3-eps)), " d=5:", float(c26(5, a3-eps)), "(continuous in a; -> 8/17, 3/8)")
print("== general d: best of the two recurrences from (Guth-Katz a2 = 1-o(1), TYZ a3 = 2/3-o(1)) vs SV's general 2/d - 2/(d(d+2)) ==")
best = {2: R(1), 3: R(2, 3)}
for d in range(4, 11):
    cand = [c23(d, best[d-1]), c26(d, best[d-2])]
    best[d] = max(cand)
    closed = f28(d, 2, R(1)) if d % 2 == 0 else f28(d, 3, R(2, 3))
    sv = R(2, d) - R(2, d*(d+2))
    print(f"  d={d}: via Cor2.3 {cand[0]} ({float(cand[0]):.4f}), via Cor2.6 {cand[1]} ({float(cand[1]):.4f}); Fact 2.8 closed form {closed} ({float(closed):.4f}); 2/d-2/(d(d+2)) = {sv} ({float(sv):.4f}); 2/d = {float(R(2,d)):.4f}")
print("  identity 2/d - 2/(d(d+2)) = 2(d+1)/(d(d+2)):", simplify(R(2,1)/Symbol('d') - 2/(Symbol('d')*(Symbol('d')+2)) - 2*(Symbol('d')+1)/(Symbol('d')*(Symbol('d')+2))) == 0)
```

### `c_exponents.py`

```python
# (c) exponent bookkeeping of Section 2, in base-A exponents (A = N^{2/d} = B^2; N = A^{d/2})
from sympy import Rational as R, symbols, binomial, limit, oo, factorial, simplify, floor
print("d | N=A^e  | N^2=A^e | N<=A^(d-1)? | A^(d/2)<=A^(d-2)? (local iso cap, needs d>=4) | s0=d(d-1)/2 | A^(d-1)=N^e | delta(H)/A^(d-1)")
for d in (3, 4, 5, 6):
    eN = R(d, 2)
    print(f"{d} | {eN}    | {2*eN}       | {eN <= d-1} ({eN}<= {d-1}) | {eN <= d-2} ({eN} <= {d-2}) | {R(d*(d-1),2)} | N^{R(2*(d-1),d)} | c3*N^2/(M*A^(d-1)) = c3*A^{d}/(M*A^{d-1}) = c3*A/M -> oo")
print()
print("Prop 2.2, l>=4 branch: fibres O(M^2) many, each bounded by f(d-l); total exponent 2+f vs d/2")
for d in range(3, 9):
    rows = []
    for l in range(1, d+1):
        u = d - l
        if u >= 3: f, why = R(u, 2), f"flat u={u}: C M^(u/2)"
        elif u == 2: f, why = R(1), "circle: 2M"
        else: f, why = R(0), "<=2 points"
        tot = 2 + f
        ok = tot <= R(d, 2)
        rows.append((l, u, why, tot, ok))
    for (l, u, why, tot, ok) in rows:
        tag = "(branch used)" if l >= 4 else "(branch NOT used: l<=3 handled separately)"
        print(f"  d={d} l={l} d-l={u}: fibre {why:22s} total M^{tot} vs M^{R(d,2)}: {'OK' if ok else 'FAILS'} {tag}")
print("  generic identity: 2+(d-l)/2 <= d/2  <=>  l >= 4 :", simplify((2+(symbols('d')-symbols('l'))/2 - symbols('d')/2)), "<= 0")
print()
print("Lemma 2.1 rows (M<=A=B^2): u=1: 2M<=2B^2; u=2: C M log 2M <= C B^2 log(2B^2) = B^{2+o(1)}; u>=3: C M^(u/2) <= C B^u")
for d in (3, 4, 5):
    worst = max(2, d-1)
    print(f"  d={d}: worst proper flat ~ B^{worst} (u={d-1} if >=3 else plane B^{{2+o(1)}}); N B^(-1/2) = B^{R(2*d-1,2)} -> c0=1/2 works: {worst < R(2*d-1,2)}")
print()
print("C(D+s0,s0) vs A^{s0} with D=floor(A): ratio C(D+s0,s0)/A^{s0}")
for d in (3, 4, 5):
    s0 = d*(d-1)//2
    vals = []
    for Aval in (10, 100, 1000, 10**5):
        D = Aval
        vals.append(float(binomial(D+s0, s0))/Aval**s0)
    print(f"  d={d} s0={s0}: A=10,100,1e3,1e5 -> {['%.4g'%v for v in vals]}  limit 1/s0! = {float(1/factorial(s0)):.4g}  (so C4 = 2^{s0}/s0! suffices for A>=s0)")
print()
print("Lemma 2.5 excess dimension: Z-space dim s0, neighbour flat codim d-1, hypersurface dim s0-1 => h = (s0-1)-(s0-d+1) = d-2 = r-1 with r=d-1")
for d in (3,4,5):
    s0 = d*(d-1)//2
    print(f"  d={d}: s0={s0}, neighbour flat dim {s0-(d-1)}, hypersurface dim {s0-1}, h={s0-1-(s0-(d-1))}, r-1={d-2}; bound C*deg*A^(d-2) summed over deg<=A: C*A^{d-1}")
print()
print("Global ambient: skew forms on C^(d+1) = (Z,c): dim s0+d = d(d+1)/2; Lemma 2.4 h ranges 0..d")
for d in (3,4,5):
    print(f"  d={d}: s0+d={d*(d-1)//2+d} = d(d+1)/2={d*(d+1)//2}; total params N^2=A^{d}, iso cap N=A^{R(d,2)} <= A^{d-1}")
print()
print("(2.4)-(2.5): edges 2*sum s_rho^2 >= 2|S|^2/(M-1) >= 2|S|^2/M; prune threshold E0/(2N^2) >= c2 N^2/(2M)")
print("d=3 deletion: sum C(k,2) <= (1/2) sum k^2 <= (K/2) N^4/A ; ratio to N^4/M = (K/2) M/A -> 0")
print("Chernoff: P(Bin < mean/2) <= exp(-mean/8); union over N^2 vertices: N^2 exp(-theta*delta(H)/8) <= N^2 exp(-theta*A^(d-1)/8) -> 0 since A^(d-1)=N^(2(d-1)/d) >> log N")
```

### `c2_extra.py`

```python
# (c') further Section-2 bookkeeping: Lemma 2.1 rows, Prop 2.2 sums, constants c1 (2.3) and c4/C4/theta (2.9), Chernoff.
import math
from math import comb, factorial
from sympy import Rational as R
print("== Lemma 2.1 u=2 row: planar bound g_2(m) >= c m/log m and <= M-1 distances  =>  m <= C M log(2M) ==")
# claim used: m/ln m <= X (X >= 1)  =>  m <= max(e, 2 X ln X) ; check: X >= 2 ln X for all X > 0
print("  min_{X>0} (X - 2 ln X) =", round(2 - 2*math.log(2), 6), "> 0, so m = 2X ln X has m/ln m >= X; brute check:")
bad = 0
for X in [1.5*1.1**i for i in range(200)]:
    m = 3
    while m/math.log(m) <= X: m += max(1, m//1000)
    if m - 1 > max(math.e, 2*X*math.log(X)) + 1: bad += 1
print("  violations of (largest m with m/ln m <= X) <= 2 X ln X over 200 X in [1.5, 2.8e8]:", bad)
print("== Lemma 2.1 u>=3 rows: c_u m^(2/u) <= M  =>  m <= (M/c_u)^(u/2) = C_u M^(u/2);  c0 = 1/2 ==")
for d in range(3, 8):
    rows = []
    for u in range(1, d):
        e = 1 if u == 1 else (1 if u == 2 else R(u, 2))   # exponent of M (u=2: M^{1+o(1)})
        rows.append(f"u={u}: B^{2*e}{'+o(1)' if u == 2 else ''}")
    print(f"  d={d}: proper u-flats hold at most " + ", ".join(rows) + f"; N B^(-1/2) = B^{R(2*d-1,2)}; worst exponent {max(2, d-1)} < {R(2*d-1,2)}")
print("== Prop 2.2 rich-line discard: sum over dyadic t = 2^j H <= L_max of C(N^2/t^3 + N/t)(2t)^2 <= 8C(N^2/H + N L_max) ==")
for N, H, L in ((10**6, 10, 1000), (10**9, 50, 10**5), (10**12, 1000, 10**6)):
    s = 0.0; t = H
    while t <= L: s += (N**2/t**3 + N/t)*(2*t)**2; t *= 2
    print(f"  N={N:.0e} H={H} L_max={L}: dyadic sum / (N^2/H + N L_max) = {s/(N**2/H + N*L):.3f} (<= 8)")
print("== Prop 2.2 greedy: removed curves Y carry > K A deg(Y) disjoint partners  =>  sum deg Y < N/(KA) = o(N/A) when K -> oo ==")
print("== (2.3): |S| = sum_j #partners_j <= sum_j C a_j A^j,  H_S(D) >= c_d a_j D^j,  D = floor(A) >= A/2 (A >= 2) ==")
for d in (3, 4, 5):
    print(f"  d={d}: |S| <= d * C * 2^(d-1) * max_j a_j D^j <= (d C 2^(d-1)/c_d) H_S(D)  =>  c1 = c_d/(d C 2^(d-1)) = c_d/(C*{d*2**(d-1)})")
print("== (2.9) and the sample: H_{S_F}(D) >= max_h c a_h D^(s0+h) >= (c/C) max_h m_h A^(s0)(D/A)^(s0+h) >= c4 m A^s0 with c4 = c/(C (d+1) 2^(s0+d)) ==")
for d in (3, 4, 5):
    s0 = d*(d-1)//2
    C4 = 2*2**s0/factorial(s0)          # 2 * C(D+s0,s0) <= 2 (2A)^s0/s0!  for A >= s0
    worst = max(comb(A+s0, s0)/A**s0 for A in range(s0, 5000))
    print(f"  d={d}, s0={s0}: max_(A>=s0) C(A+s0,s0)/A^s0 = {worst:.4f} <= 2^s0/s0! = {2**s0/factorial(s0):.4f}: {worst <= 2**s0/factorial(s0)};  "
          f"theta < c4/C4 suffices (fixed: depends on d and the constants of Lemmas 2.4 and 3.6 only)")
print("== Chernoff + union bound: P(Bin(n,theta) < n theta/2) <= exp(-n theta/8); need N^2 exp(-theta delta(H)/8) -> 0 with delta(H) >> A^(d-1) ==")
for d in (3, 4, 5):
    for N in (10**3, 10**6, 10**9):
        A = N**(2/d); theta = 1e-3
        lg = 2*math.log(N) - theta*A**(d-1)/8
        print(f"  d={d} N={N:.0e}: A^(d-1) = N^{2*(d-1)/d:.3f} = {A**(d-1):.3e}; log(N^2 exp(-theta A^(d-1)/8)) with theta=1e-3: {lg:.3e}")
```

### `d_skew.py`

```python
# (d) skew-form identities (2.6)-(2.8) and the polarization identities, pp. 11-13.
import numpy as np, itertools
from sympy import Matrix, Rational, symbols, zeros, eye
rng = np.random.default_rng(166)

def skew_basis(d):
    B = []
    for i in range(d):
        for j in range(i+1, d):
            E = np.zeros((d, d)); E[i, j] = 1; E[j, i] = -1; B.append(E)
    return B

def flat_system(p, q):
    """Linear system on unknowns (z_ij (i<j), c) for F_{p,q}: Z v0 + c = y0."""
    d = len(p); B = skew_basis(d); s0 = len(B)
    v0 = (p+q)/2; y0 = (p-q)/2
    Mz = np.column_stack([E @ v0 for E in B])        # d x s0
    M = np.hstack([Mz, np.eye(d)])                    # d x (s0+d)
    return M, y0

def omega(Z, c):
    d = len(c)
    O = np.zeros((d+1, d+1)); O[:d, :d] = Z; O[:d, d] = c; O[d, :d] = -c
    return O

for d in (3, 4):
    B = skew_basis(d); s0 = len(B)
    print(f"===== d={d}, s0={s0} (d(d-1)/2={d*(d-1)//2}), ambient skew forms on C^{d+1}: dim {s0+d} = d(d+1)/2 = {d*(d+1)//2}")
    worst_eval = 0.0; worst_quad = 0.0
    for trial in range(200):
        p, q = rng.normal(size=d), rng.normal(size=d)
        v0, y0 = (p+q)/2, (p-q)/2
        # random point of F_{p,q}: choose Z skew, set c = y0 - Z v0
        z = rng.normal(size=s0); Z = sum(zz*E for zz, E in zip(z, B)); c = y0 - Z @ v0
        O = omega(Z, c)
        v = np.append(v0, 1.0); y = np.append(y0, -v0 @ y0)
        worst_eval = max(worst_eval, np.abs(O @ v - y).max())
        worst_quad = max(worst_quad, abs(v0 @ Z @ v0))
    print(f"  (2.7) Omega v == y on F_pq: max residual over 200 random points {worst_eval:.2e};  v0.Z v0 = 0: max {worst_quad:.2e}")
    # converse + dimension: evaluation equation Omega v = y as a linear system in (Z,c) has rank d (last row dependent)
    p, q = rng.normal(size=d), rng.normal(size=d); v0, y0 = (p+q)/2, (p-q)/2
    v = np.append(v0, 1.0)
    rows = []
    basis_full = [omega(E, np.zeros(d)) for E in B] + [omega(np.zeros((d, d)), e) for e in np.eye(d)]
    Mfull = np.column_stack([Ob @ v for Ob in basis_full])      # (d+1) x (s0+d)
    rk_full = np.linalg.matrix_rank(Mfull); rk_first = np.linalg.matrix_rank(Mfull[:d])
    print(f"  evaluation system Omega v = y: rank of all d+1 rows = {rk_full}, rank of first d rows = {rk_first} -> flat dim = {s0+d-rk_full} (claimed s0={s0})")
    # last row is v^T Omega v - v.y == 0 identically? check: last row coefficient vector = -(first d rows)^T v0 combination
    lastrow_dep = np.linalg.matrix_rank(np.vstack([Mfull[:d], Mfull[d:]])) == rk_first
    print(f"  last (d+1)-th coordinate equation implied by first d: {lastrow_dep}  (uses v.Omega v = 0 and v.y = 0: v.y = {v @ np.append(y0, -v0@y0):.2e})")
    # distinct pairs -> distinct flats
    distinct_ok = True
    for trial in range(200):
        p, q, p2, q2 = (rng.normal(size=d) for _ in range(4))
        M1, y1 = flat_system(p, q); M2, y2 = flat_system(p2, q2)
        # same flat iff same row space AND consistent: stacked system rank == individual rank and solvable
        st = np.vstack([np.hstack([M1, y1[:, None]]), np.hstack([M2, y2[:, None]])])
        same = np.linalg.matrix_rank(st) == np.linalg.matrix_rank(M1) == np.linalg.matrix_rank(M2)
        if same: distinct_ok = False
    # also degenerate: pairs sharing p or sharing q
    p, q, q2 = rng.normal(size=d), rng.normal(size=d), rng.normal(size=d)
    M1, y1 = flat_system(p, q); M2, y2 = flat_system(p, q2)
    st = np.vstack([np.hstack([M1, y1[:, None]]), np.hstack([M2, y2[:, None]])])
    same2 = np.linalg.matrix_rank(st) == d
    print(f"  distinct random pairs give distinct flats (200 trials): {distinct_ok};  (p,q) vs (p,q') same flat? {same2}")
    # recover (p,q) from flat: Z=0 -> c=y0; then Z v0 = y0 - c for all Z determines v0
    # (2.8): F_pq cap F_p'q' = {Z : Z(u+w) = u - w}
    worst = 0.0
    for trial in range(100):
        p, q = rng.normal(size=d), rng.normal(size=d)
        u = rng.normal(size=d)
        # make |w| = |u| with w random direction
        w = rng.normal(size=d); w *= np.linalg.norm(u)/np.linalg.norm(w)
        p2, q2 = p+u, q+w
        M1, y1 = flat_system(p, q); M2, y2 = flat_system(p2, q2)
        # solve intersection, then check every solution satisfies Z(u+w)=u-w and dimension
        Mst = np.vstack([M1, M2]); yst = np.concatenate([y1, y2])
        sol, res, rk, _ = np.linalg.lstsq(Mst, yst, rcond=None)
        Zs = sum(zz*E for zz, E in zip(sol[:s0], B))
        worst = max(worst, np.abs(Zs @ (u+w) - (u-w)).max(), np.abs(Mst @ sol - yst).max())
        dim_int = s0 + d - rk
    print(f"  (2.8) intersection of neighbouring flats satisfies Z(u+w)=u-w: max residual {worst:.2e}; intersection dim = {dim_int} = s0-(d-1) = {s0-(d-1)}")
    # nonempty iff |u|=|w| (u+w != 0); codim exactly d-1 inside Z-space
    print("  {Z skew: Z x = y}, x=u+w, y=u-w:")
    for label, u, w in [("|u|=|w|", rng.normal(size=d), None), ("|u|!=|w|", rng.normal(size=d), "neq"), ("u+w=0", rng.normal(size=d), "neg")]:
        if w is None:
            w = rng.normal(size=d); w *= np.linalg.norm(u)/np.linalg.norm(w)
        elif w == "neq":
            w = rng.normal(size=d); w *= 1.3*np.linalg.norm(u)/np.linalg.norm(w)
        else:
            w = -u
        x, y = u+w, u-w
        A = np.column_stack([E @ x for E in B])   # d x s0
        rkA = np.linalg.matrix_rank(A, tol=1e-9); rkAug = np.linalg.matrix_rank(np.hstack([A, y[:, None]]), tol=1e-9)
        print(f"    {label:9s}: rank[Z->Zx] = {rkA}, rank augmented = {rkAug} -> {'NONEMPTY' if rkA==rkAug else 'EMPTY'}, codim in Z-space = {rkA if rkA==rkAug else '-'}  (x.y = |u|^2-|w|^2 = {x@y:+.3e})")
    # exact rational check of rank d-1 for a rational example
    xs = [Rational(1), Rational(2), Rational(-3), Rational(5)][:d]
    Mx = Matrix([[ (E @ np.array([float(t) for t in xs]))[i] for E in B] for i in range(d)])
    print(f"  exact rank of Z->Zx for x={xs}: {Matrix(Mx).applyfunc(lambda t: Rational(t).limit_denominator(1000)).rank()} (claimed d-1={d-1})")
    # distinct local parameters -> distinct neighbour flats  (flat {Zx=y} determines [x:y] for d>=3)
    okloc = True
    for trial in range(200):
        x1, x2 = rng.normal(size=d), rng.normal(size=d)
        A1 = np.column_stack([E @ x1 for E in B]); A2 = np.column_stack([E @ x2 for E in B])
        # direction spaces ker(A1), ker(A2) equal?
        if np.linalg.matrix_rank(np.vstack([A1, A2])) == np.linalg.matrix_rank(A1): okloc = False
    x1 = rng.normal(size=d); A1 = np.column_stack([E @ x1 for E in B]); A2 = np.column_stack([E @ (2.5*x1) for E in B])
    print(f"  non-proportional x give different direction spaces (200 trials): {okloc}; proportional x give same: {np.linalg.matrix_rank(np.vstack([A1,A2]))==np.linalg.matrix_rank(A1)}")
    # polarization identities
    wg = 0.0; wl = 0.0
    for trial in range(200):
        p, q, p2, q2 = (rng.normal(size=d) for _ in range(4))
        v0, y0, v1, y1_ = (p+q)/2, (p-q)/2, (p2+q2)/2, (p2-q2)/2
        X1 = np.concatenate([v0, [1.0], y0, [-v0 @ y0]]); X2 = np.concatenate([v1, [1.0], y1_, [-v1 @ y1_]])
        Bform = lambda X, Y: X[:d+1] @ Y[d+1:] + Y[:d+1] @ X[d+1:]
        lhs = Bform(X1, X2); rhs = -(v0-v1) @ (y0-y1_); phys = -(np.sum((p-p2)**2) - np.sum((q-q2)**2))/4
        wg = max(wg, abs(lhs-rhs), abs(rhs-phys))
        ui, wi, uj, wj = (rng.normal(size=d) for _ in range(4))
        L = (ui-wi) @ (uj+wj) + (uj-wj) @ (ui+wi); Rr = 2*(ui @ uj - wi @ wj)
        Bloc = (ui+wi) @ (uj-wj) + (uj+wj) @ (ui-wi)
        wl = max(wl, abs(L-Rr), abs(Bloc-L))
    print(f"  global polarization: B(X,X') = -(v0-v0').(y0-y0') = -(|p-p'|^2-|q-q'|^2)/4 : max err {wg:.2e}")
    print(f"  local polarization: (ui-wi).(uj+wj)+(uj-wj).(ui+wi) = 2(ui.uj - wi.wj) = B([ui+wi:ui-wi],[uj+wj:uj-wj]): max err {wl:.2e}")
    # Prop 2.2 radius-class identity: |z_i-p|=|z_j-p| => (|q-z_i|=|q-z_j| <=> (q-p).(z_i-z_j)=0)
    werr = 0.0
    for trial in range(200):
        pp, qq, zi = rng.normal(size=d), rng.normal(size=d), rng.normal(size=d)
        r = np.linalg.norm(zi-pp); zj = rng.normal(size=d); zj = pp + r*(zj/np.linalg.norm(zj))
        lhs = np.sum((qq-zi)**2) - np.sum((qq-zj)**2); rhs = -2*(qq-pp) @ (zi-zj)
        werr = max(werr, abs(lhs-rhs))
    print(f"  Prop 2.2 identity |q-z_i|^2-|q-z_j|^2 = -2(q-p).(z_i-z_j) on a radius class: max err {werr:.2e}")
```

### `d2_symbolic.py`

```python
# (d') exact symbolic versions of the identities on pp. 11-13 (sympy), d = 3 and 4
from sympy import symbols, Matrix, expand, simplify, zeros
for d in (3, 4):
    p = Matrix(symbols(f'p1:{d+1}')); q = Matrix(symbols(f'q1:{d+1}'))
    p2 = Matrix(symbols(f'P1:{d+1}')); q2 = Matrix(symbols(f'Q1:{d+1}'))
    zs = symbols(f'z1:{d*(d-1)//2+1}')
    Z = zeros(d, d); k = 0
    for i in range(d):
        for j in range(i+1, d):
            Z[i, j] = zs[k]; Z[j, i] = -zs[k]; k += 1
    v0 = (p+q)/2; y0 = (p-q)/2
    c = y0 - Z*v0                      # generic point of F_{p,q}
    Om = zeros(d+1, d+1); Om[:d, :d] = Z; Om[:d, d] = c; Om[d, :d] = -c.T
    v = Matrix.vstack(v0, Matrix([1])); y = Matrix.vstack(y0, Matrix([-(v0.T*y0)[0]]))
    r1 = (Om*v - y).applyfunc(expand)
    print(f"d={d}: Omega v - y on F_pq  ==", list(r1), " ; v0.Z v0 =", expand((v0.T*Z*v0)[0]))
    # global polarization
    v1 = (p2+q2)/2; y1 = (p2-q2)/2
    X1 = list(v0)+[1]+list(y0)+[-(v0.T*y0)[0]]; X2 = list(v1)+[1]+list(y1)+[-(v1.T*y1)[0]]
    Bf = sum(X1[i]*X2[d+1+i] + X2[i]*X1[d+1+i] for i in range(d+1))
    phys = -(((p-p2).T*(p-p2))[0] - ((q-q2).T*(q-q2))[0])/4
    print(f"  B(X,X') + (v0-v0').(y0-y0') = {expand(Bf + ((v0-v1).T*(y0-y1))[0])};  (v0-v0').(y0-y0') - (|p-p'|^2-|q-q'|^2)/4 = {expand(((v0-v1).T*(y0-y1))[0] - (((p-p2).T*(p-p2))[0] - ((q-q2).T*(q-q2))[0])/4)}")
    # (2.8): subtracting the two flat equations
    c2 = None
    diff = (Z*v0 - y0) - (Z*v1 - y1)        # (c cancels)
    u = p2 - p; w = q2 - q
    print(f"  (Zv0 - y0) - (Zv0' - y0') + (1/2)(Z(u+w) - (u-w)) = {list((diff + (Z*(u+w) - (u-w))/2).applyfunc(expand))}")
    # local polarization
    ui = Matrix(symbols(f'a1:{d+1}')); wi = Matrix(symbols(f'b1:{d+1}')); uj = Matrix(symbols(f'c1:{d+1}')); wj = Matrix(symbols(f'e1:{d+1}'))
    L = ((ui-wi).T*(uj+wj))[0] + ((uj-wj).T*(ui+wi))[0]
    print(f"  local: L - 2(ui.uj - wi.wj) = {expand(L - 2*((ui.T*uj)[0] - (wi.T*wj)[0]))};  x.Zx for skew Z: {expand(((ui).T*Z*ui)[0])}")
```

### `d3_exact.py`

```python
# (d'') exact rational versions (sympy) of the rank/codimension/nonemptiness claims around (2.6)-(2.8), d = 3, 4.
# Equal-norm rational pairs are produced exactly by a rational orthogonal Q (Cayley transform of a rational skew K).
import random
from sympy import Matrix, Rational as R, eye, zeros
random.seed(20261012)
def rr(): return R(random.randint(-9, 9), random.randint(1, 5))
def skew_basis(d):
    B = []
    for i in range(d):
        for j in range(i+1, d):
            E = zeros(d, d); E[i, j] = 1; E[j, i] = -1; B.append(E)
    return B
def cayley(d):
    K = zeros(d, d)
    for i in range(d):
        for j in range(i+1, d):
            x = rr(); K[i, j] = x; K[j, i] = -x
    return (eye(d) - K).inv()*(eye(d) + K)
for d in (3, 4):
    Bs = skew_basis(d); s0 = len(Bs)
    tallies = {"eq_norm_nonempty_codim_d-1": 0, "neq_norm_empty": 0, "u+w=0_empty": 0, "trials": 0}
    for _ in range(40):
        u = Matrix([rr() for _ in range(d)])
        if u.norm() == 0: continue
        Q = cayley(d); assert Q.T*Q == eye(d)
        w = Q*u                                   # |w| = |u| exactly
        if (u + w).norm() == 0: continue
        x, y = u + w, u - w
        Ax = Matrix.hstack(*[E*x for E in Bs])     # d x s0 : Z -> Z x in the skew basis
        rk, rka = Ax.rank(), Matrix.hstack(Ax, y).rank()
        tallies["trials"] += 1
        if rk == d-1 and rka == d-1: tallies["eq_norm_nonempty_codim_d-1"] += 1
        w2 = R(3, 2)*w; x2, y2 = u + w2, u - w2      # |w2| != |u|
        A2 = Matrix.hstack(*[E*x2 for E in Bs])
        if A2.rank() == d-1 and Matrix.hstack(A2, y2).rank() == d: tallies["neq_norm_empty"] += 1
        A3 = Matrix.hstack(*[E*zeros(d, 1) for E in Bs]); y3 = 2*u      # w = -u: Z*0 = 2u impossible
        if Matrix.hstack(A3, y3).rank() > A3.rank(): tallies["u+w=0_empty"] += 1
    print(f"d={d} (s0={s0}): {tallies}")
    # distinct pairs give distinct flats: v -> (Z -> Z v) is injective (stacked d*s0 x d matrix has rank d)
    M = Matrix.vstack(*[E for E in Bs])            # rows: E v for each basis E, as a (d*s0) x d linear map in v
    print(f"   rank of v |-> (E v)_E over all skew basis E: {M.rank()} (= d -> Z v0 = Z v0' for all skew Z forces v0 = v0')")
    # flat F_{p,q} dimension: unknowns (z, c) in C^(s0+d), equations Z v0 + c = y0 (d independent equations, c-block = I)
    v0 = Matrix([rr() for _ in range(d)])
    Mflat = Matrix.hstack(Matrix.hstack(*[E*v0 for E in Bs]), eye(d))
    print(f"   F_pq: rank of (Z,c)-system = {Mflat.rank()}, dim = s0 + d - rank = {s0 + d - Mflat.rank()} (claimed s0 = {s0})")
    # neighbour flat inside F_pq: Z(u+w) = u-w has codim d-1, so a hypersurface of F has excess h = (s0-1)-(s0-(d-1)) = d-2
    print(f"   excess dimension of a hypersurface component over a neighbour flat: {(s0-1)-(s0-(d-1))} (claimed d-2 = {d-2} = r-1, r = d-1)")
```

### `e_gram.py`

```python
# (e) Lemma 2.5: equal Gram matrices (u_i.u_j = w_i.w_j) => u_i -> w_i extends to S in O(d)
import numpy as np
rng = np.random.default_rng(2025)
d = 3
def random_O(d, det=None):
    Q, R = np.linalg.qr(rng.normal(size=(d, d))); Q = Q @ np.diag(np.sign(np.diag(R)))
    if det is not None and np.sign(np.linalg.det(Q)) != det: Q[:, 0] *= -1
    return Q
def extend_isometry(U, W, tol=1e-9):
    """U, W: d x k with U^T U == W^T W. Build S in O(d) with S U = W (via orthonormal bases of spans)."""
    G = U.T @ U
    assert np.allclose(G, W.T @ W, atol=1e-9)
    # well-definedness: kernel of U equals kernel of W
    nU = np.linalg.svd(U)[2]; r = np.linalg.matrix_rank(U, tol)
    ker = nU[r:].T                       # k x (k-r)
    welldef = np.abs(W @ ker).max() if ker.size else 0.0
    # orthonormal basis of span(U) and corresponding images
    Uu, s, Vt = np.linalg.svd(U, full_matrices=True)
    E = Uu[:, :r]                          # orthonormal basis of span U
    # E = U V_r diag(1/s); image F = W V_r diag(1/s)
    F = W @ Vt[:r].T @ np.diag(1/s[:r])
    orthoF = np.abs(F.T @ F - np.eye(r)).max()
    # complete both to orthonormal bases of R^d
    def complete(X):
        Qf, _ = np.linalg.qr(np.hstack([X, rng.normal(size=(d, d-X.shape[1]))]))
        Qf[:, :X.shape[1]] = X
        # re-orthonormalise the completion against X
        for j in range(X.shape[1], d):
            v = Qf[:, j] - Qf[:, :j] @ (Qf[:, :j].T @ Qf[:, j]); Qf[:, j] = v/np.linalg.norm(v)
        return Qf
    Ef, Ff = complete(E), complete(F)
    S = Ff @ Ef.T
    return S, welldef, orthoF
cases = []
for k in (1, 2, 3, 4, 5):
    U = rng.normal(size=(d, k)); cases.append((f"generic k={k}", U))
U = rng.normal(size=(d, 2)); cases.append(("dependent: u3=u1+2u2", np.column_stack([U, U[:, 0]+2*U[:, 1]])))
u1 = rng.normal(size=d); cases.append(("collinear: u2=-1.5u1, u3=3u1", np.column_stack([u1, -1.5*u1, 3*u1])))
U = rng.normal(size=(d, 2)); cases.append(("planar 4 vectors", np.column_stack([U, U @ rng.normal(size=(2, 2))])))
for name, U in cases:
    for det in (+1, -1):
        S0 = random_O(d, det)
        W = S0 @ U
        S, wd, oF = extend_isometry(U, W)
        print(f"{name:32s} det(S0)={det:+d}: kernel-preserved err {wd:.1e}, image basis orthonormal err {oF:.1e}, |S U - W| = {np.abs(S@U-W).max():.1e}, |S^T S - I| = {np.abs(S.T@S-np.eye(d)).max():.1e}, det S = {np.linalg.det(S):+.3f}")
# Gram-equal pairs NOT produced from an S0: construct W from the Gram matrix directly (Cholesky-type), check extension still exists
for k in (2, 3):
    U = rng.normal(size=(d, k)); G = U.T @ U
    L = np.linalg.cholesky(G)                       # G = L L^T, L k x k
    W = np.zeros((d, k)); W[:k, :] = L.T
    S, wd, oF = extend_isometry(U, W)
    print(f"Gram-built W, k={k}: |S U - W| = {np.abs(S@U-W).max():.1e}, |S^T S - I| = {np.abs(S.T@S-np.eye(d)).max():.1e}")
# negative control: unequal Gram => no isometry (assert fires)
U = rng.normal(size=(d, 2)); W = U.copy(); W[:, 1] *= 1.01
try:
    extend_isometry(U, W); print("NEGATIVE CONTROL FAILED")
except AssertionError:
    print("negative control: unequal Gram matrices correctly rejected")
# matches: x -> q + S(x - p) maps p -> q and p+u_i -> q+w_i
p, q = rng.normal(size=d), rng.normal(size=d); U = rng.normal(size=(d, 3)); S0 = random_O(d, -1); W = S0 @ U
S, _, _ = extend_isometry(U, W)
print("match check: max |q + S((p+u_i)-p) - (q+w_i)| =", np.abs((q[:, None] + S @ U) - (q[:, None] + W)).max())
```

### `f_motions.py`

```python
# (f) d=3 rich motions on a small grid P = {0..t-1}^3 (self-motions, both orientations).
# Lattice part: all 48 signed permutation matrices x integer translations (exhaustive for these S).
# Rational part (t<=4): rotations R(q)/|q|^2 from integer quaternions with |q|^2 <= QMAX, plus improper -S; deduplicated.
import numpy as np, itertools, math, sys
QMAX = int(sys.argv[1]) if len(sys.argv) > 1 else 50
def signed_perms():
    out = []
    for perm in itertools.permutations(range(3)):
        for signs in itertools.product((1, -1), repeat=3):
            M = np.zeros((3, 3), dtype=np.int64)
            for i in range(3): M[i, perm[i]] = signs[i]
            out.append((M, 1))
    return out
def quat_rot(a, b, c, d):
    n = a*a+b*b+c*c+d*d
    M = np.array([[a*a+b*b-c*c-d*d, 2*(b*c-a*d), 2*(b*d+a*c)],
                  [2*(b*c+a*d), a*a-b*b+c*c-d*d, 2*(c*d-a*b)],
                  [2*(b*d-a*c), 2*(c*d+a*b), a*a-b*b-c*c+d*d]], dtype=np.int64)
    g = math.gcd(n, *[int(x) for x in M.flatten()])
    return M//g, n//g
def rational_motions(qmax):
    seen = set(); out = []
    r = math.isqrt(qmax)
    for a, b, c, d in itertools.product(range(-r, r+1), repeat=4):
        n = a*a+b*b+c*c+d*d
        if n == 0 or n > qmax: continue
        M, m = quat_rot(a, b, c, d)
        if m == 1: continue
        for sgn in (1, -1):
            key = (m,) + tuple(int(x) for x in (sgn*M).flatten())
            if key not in seen:
                seen.add(key); out.append((sgn*M, m))
    return out
def match_counts(Pm, motions):
    ks = []
    for M, m in motions:
        img = Pm @ M.T
        H = (m*Pm[None, :, :] - img[:, None, :]).reshape(-1, 3)
        off = H.min(axis=0); span = H.max(axis=0) - off + 1
        key = ((H[:, 0]-off[0])*span[1] + (H[:, 1]-off[1]))*span[2] + (H[:, 2]-off[2])
        _, cnt = np.unique(key, return_counts=True)
        ks.append(cnt)
    return np.concatenate(ks)
lat = signed_perms()
for t in range(3, 8):
    Pm = np.array(list(itertools.product(range(t), repeat=3)), dtype=np.int64); N = len(Pm); A = N**(2/3)
    kl = match_counts(Pm, lat)
    line = f"t={t} N={N:3d} A={A:5.1f} N^(10/3)={N**(10/3):.3e} | lattice: max k={kl.max()}"
    for C in (1, 2):
        S = int((kl[kl >= C*A].astype(np.int64)**2).sum())
        line += f" | C_rich={C}: #motions={(kl>=C*A).sum()}, sum k^2={S}, /N^(10/3)={S/N**(10/3):.4f}"
    print(line)
    if t <= 4:
        q = QMAX if t == 3 else 30
        rat = rational_motions(q)
        kr = match_counts(Pm, rat)
        print(f"      + {len(rat)} rational-rotation motions (quaternion norm <= {q}): max k = {kr.max()}, #with k>=A: {(kr>=A).sum()}, #with k>=4: {(kr>=4).sum()}")
for t in (3, 4, 5, 6, 7):
    Pm = np.array(list(itertools.product(range(t), repeat=3)), dtype=np.int64); N = len(Pm)
    kl = match_counts(Pm, lat).astype(np.int64)
    tot = int((kl**2).sum())
    print(f"t={t}: sum over all lattice motions of k^2 = {tot};  /N^3 = {tot/N**3:.2f};  /N^(10/3) = {tot/N**(10/3):.4f}")
```

### `f2_all_isometries.py`

```python
# (f') EXHAUSTIVE over ALL isometries of R^3 (not only lattice ones) for the grid P = {0..t-1}^3 (t=3).
# An isometry g = (S,h) with a NON-collinear match set maps two independent difference vectors u1,u2 of P to
# difference vectors w1,w2 of P with the same Gram matrix; S is then [w1 w2 +-w1xw2][u1 u2 u1xu2]^-1.
# We enumerate every such S (deduplicated), then count matches k(S,h) for every translation h at once
# (histogram of y - S x over x,y in P).  Collinear match sets have k <= t < A and are irrelevant for k >= C*A.
import itertools, sys, numpy as np
t = int(sys.argv[1]) if len(sys.argv) > 1 else 3
P = np.array(list(itertools.product(range(t), repeat=3)), dtype=float); N = len(P); A = N**(2/3)
V = np.array([v for v in itertools.product(range(-(t-1), t), repeat=3) if any(v)], dtype=float)   # difference vectors
nrm = (V**2).sum(1).round().astype(int)
chunks = []
for a in range(len(V)):
    u1 = V[a]; W1 = V[nrm == nrm[a]]
    for b in range(a+1, len(V)):
        u2 = V[b]; cr = np.cross(u1, u2)
        if not cr.any(): continue
        Finv = np.linalg.inv(np.column_stack([u1, u2, cr]))
        W2 = V[nrm == nrm[b]]
        ii, jj = np.nonzero(np.abs(W1 @ W2.T - u1 @ u2) < 1e-9)
        w1, w2 = W1[ii], W2[jj]; wc = np.cross(w1, w2)
        for sgn in (1, -1):
            G = np.stack([w1, w2, sgn*wc], axis=2)            # columns w1, w2, +-w1xw2
            chunks.append((G @ Finv).reshape(-1, 9))
allS = np.concatenate(chunks)
_, first = np.unique(np.round(allS, 9), axis=0, return_index=True)
Ss = {i: allS[i].reshape(3, 3) for i in first}
print(f"  raw (u1,u2,w1,w2,sign) candidates: {len(allS)}")
print(f"t={t}: N={N}, A={A:.2f}; distinct orthogonal S mapping two independent difference vectors to difference vectors: {len(Ss)}")
assert all(np.allclose(S @ S.T, np.eye(3), atol=1e-9) for S in Ss.values())
ks = []; nlat = 0
for S in Ss.values():
    if np.allclose(S, np.round(S)): nlat += 1
    H = (P[None, :, :] - (P @ S.T)[:, None, :]).reshape(-1, 3)        # y - S x
    keys = np.round(H, 6)
    _, cnt = np.unique(keys, axis=0, return_counts=True)
    ks.append(cnt)
ks = np.concatenate(ks)
print(f"  of which signed permutations (lattice S): {nlat} (expected 48)")
print("  match-count distribution over all (S,h) with k>=4:", {int(k): int((ks == k).sum()) for k in np.unique(ks) if k >= 4})
for C in (0.5, 1.0, 2.0):
    sel = ks[ks >= C*A].astype(np.int64)
    print(f"  C_rich={C}: #motions with k >= {C*A:.1f}: {len(sel)}, sum k^2 = {int((sel**2).sum())}, / N^(10/3) = {(sel**2).sum()/N**(10/3):.4f}")
```

### `g_circle.py`

```python
# (g) Lemma 2.1 circle row "a circle contains at most 2M points", M = 1 + |Delta(P)|; and the line row 2M.
# Exact arithmetic: points with exact squared distances via sympy for polygons; integer points for Pythagorean circles.
import itertools, math
from sympy import cos, pi, Rational, nsimplify, simplify, sqrt, S as SS, minimal_polynomial, Symbol
from fractions import Fraction
x = Symbol('x')
def chord_sq(n, k):   # squared chord between vertices k apart on unit circle: 2-2cos(2 pi k/n)
    return simplify(2 - 2*cos(2*pi*Rational(k, n)))
print("== regular n-gon (all vertices on the circle): |Delta| = #distinct chords, M = 1+|Delta|; claim n <= 2M (proof gives n <= 2M-1) ==")
for n in range(3, 25):
    chords = set()
    for k in range(1, n//2+1):
        chords.add(minimal_polynomial(chord_sq(n, k), x))   # exact distinctness via minimal polynomials + numeric
    numvals = sorted(set(round(float(chord_sq(n, k)), 12) for k in range(1, n//2+1)))
    D = len(numvals); M = 1 + D
    print(f"  n={n:2d}: |Delta|={D}, M={M}, 2M={2*M}, n<=2M: {n<=2*M}, n<=2M-1: {n<=2*M-1}{'  <-- equality n=2M-1' if n==2*M-1 else ''}")
print("== regular 2k-gon + centre (centre is off the circle, so the circle still carries 2k points; M can only grow) ==")
for k in range(2, 9):
    n = 2*k
    vals = set(round(float(chord_sq(n, j)), 12) for j in range(1, k+1)); vals.add(1.0)   # radius 1
    M = 1 + len(vals)
    print(f"  2k={n:2d}+centre: |Delta|={len(vals)}, M={M}, circle points {n} <= 2M={2*M}: {n<=2*M}")
print("== exhaustive: every subset (|S|>=2) of vertices of the regular 12-gon and 13-gon; max over subsets of |S| - (2M-1) ==")
for n in (12, 13):
    pts = list(range(n)); best = None
    sqd = {k: round(float(chord_sq(n, k)), 12) for k in range(0, n)}
    for r in range(2, n+1):
        for sub in itertools.combinations(pts, r):
            ds = set(sqd[(b-a) % n] for a, b in itertools.combinations(sub, 2))
            M = 1 + len(ds); excess = r - (2*M - 1)
            if best is None or excess > best[0]: best = (excess, r, M, sub)
    print(f"  n={n}: max (|S| - (2M-1)) = {best[0]} attained e.g. by |S|={best[1]}, M={best[2]}, S={best[3]}")
print("== exhaustive subsets of the 12 integer points on x^2+y^2=25 and the 16 on x^2+y^2=65 (exact integer squared distances) ==")
for R2 in (25, 65):
    P = [(a, b) for a in range(-9, 10) for b in range(-9, 10) if a*a+b*b == R2]
    best = None
    for r in range(2, min(len(P), 12)+1):
        for sub in itertools.combinations(P, r):
            ds = set((a[0]-b[0])**2+(a[1]-b[1])**2 for a, b in itertools.combinations(sub, 2))
            M = 1 + len(ds); excess = r - (2*M-1)
            if best is None or excess > best[0]: best = (excess, r, M, sub)
    print(f"  R^2={R2}: {len(P)} lattice points; max (|S|-(2M-1)) over subsets of size<=12 = {best[0]} (|S|={best[1]}, M={best[2]})")
print("== line row: n collinear points, from an endpoint all distances distinct => n <= M (paper states 2M) ==")
for n in range(2, 12):
    D = len(set(range(1, n))); M = 1 + D
    print(f"  arithmetic progression n={n}: M={M}, n<=M: {n<=M}, n<=2M: {n<=2*M}")
```

### `h3_hilbert.py`

```python
# (h) Hilbert-function toys for Lemma 3.6 (pp. 18-19):  H_V(L) >= c_n a L^k  at the DEFINING degree L, for V a union
# of k-dimensional irreducible components (total degree a) of a locus cut out by equations of degree <= L.
# Constant under test (algebra seat): c_{n,k} = 1/((n-k+1)^n k!).  Also (3.5) H_V(D) <= a C(D+k,k) and the shift
# (3.6) H_V(D) >= a C(D-q+k,k) for D >= q with q <= (n-k)(L-1).
# H is computed as an exact rank (mod two large primes) of evaluation of all degree-D forms on explicit points,
# and cross-checked with closed forms / sympy Groebner standard-monomial counts.
import itertools, math, random
from math import comb
from sympy import symbols, groebner, Poly
random.seed(166)
PR = (1000000007, 998244353)
def rank_mod(rows, p):
    rows = [[x % p for x in r] for r in rows]; rk = 0
    for c in range(len(rows[0]) if rows else 0):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [x*inv % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a - f*b) % p for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def monos(nv, D): return [e for e in itertools.product(range(D+1), repeat=nv) if sum(e) == D]
def H(pts, D):   # homogeneous degree-D restriction rank on projective points given by integer reps
    ms = monos(len(pts[0]), D)
    rows = [[math.prod(pt[i]**e[i] for i in range(len(pt))) for e in ms] for pt in pts]
    return max(rank_mod(rows, p) for p in PR)
def c_nk(n, k): return 1/((n-k+1)**n * math.factorial(k))
out = []
def row(name, n, k, a, L, h, hyp):
    ratio = h/(a*L**k); c = c_nk(n, k); up = a*comb(L+k, k)
    ok = (ratio >= c) if hyp else None
    out.append((name, n, k, a, L, h, ratio, c, ok, h <= up))
    print(f"  {name:46s} n={n} k={k} a={a:4d} L={L:2d}: H={h:5d}  H/(aL^k)={ratio:6.3f}  c_nk={c:.4f}  hyp(components of degree-L locus)={hyp}  lower-ok={ok}  (3.5) H<=aC(L+k,k)={h<=up}")

print("== T1: D' concurrent lines through [0:0:1] in P^2 (n=2,k=1), tested at degree D ==")
for D in range(1, 7):
    for Dp in sorted(set((1, max(1, D//2), D, D+1, 2*D+2, 4*D+4))):
        pts = [(1, i, z) for i in range(1, Dp+1) for z in range(D+1)]       # D+1 points on each line {y = i x}
        h = H(pts, D) if Dp*(D+1) <= 300 else None
        closed = comb(D+2, 2) - (comb(D-Dp+2, 2) if Dp <= D else 0)
        if h is not None: assert h == closed, (D, Dp, h, closed)
        # lines are components of Env_D(Y) iff Dp <= D (for Dp > D every degree-D form vanishing on them is 0)
        row(f"{Dp} concurrent lines @deg D={D}", 2, 1, Dp, D, closed, Dp <= D)
print("  same lines at their defining degree L = D' (one equation: product of D' linear forms):")
for Dp in (2, 4, 8, 12, 20):
    row(f"{Dp} concurrent lines @deg L=D'={Dp}", 2, 1, Dp, Dp, comb(Dp+2, 2) - 1, True)
print("  failure threshold when the hypothesis is dropped: H(D) = C(D+2,2) < c*D'*D  iff  D' > C(D+2,2)/(c D); c=1/4, D=3: D' >", comb(5,2)/(0.25*3))

print("== T2: complete intersection of two degree-D surfaces in P^3 (curve, degree D^2), at L = D ==")
X, Y, Z, W = symbols('x y z w')
for D in range(1, 6):
    # (a) product CI: {prod_i (x - i w) = 0, prod_j (y - j w) = 0} = D^2 lines {x=i, y=j}; D+1 points per line
    pts = [(i, j, z, 1) for i in range(D) for j in range(D) for z in range(D+1)]
    h = H(pts, D) if D <= 4 else comb(D+3, 3) - 2
    assert D > 4 or h == comb(D+3, 3) - 2
    row(f"product CI (D^2 lines), D={D}", 3, 1, D*D, D, h, True)
for D in range(1, 5):
    rp = lambda: sum(random.randint(-5, 5)*X**e[0]*Y**e[1]*Z**e[2]*W**e[3] for e in monos(4, D))
    G = groebner([rp(), rp()], X, Y, Z, W, order='grevlex')
    lead = [Poly(g, X, Y, Z, W).monoms(order='grevlex')[0] for g in G.exprs]
    std = lambda m: sum(1 for e in monos(4, m) if not any(all(e[i] >= l[i] for i in range(4)) for l in lead))
    h = std(D)
    row(f"random CI (smooth, reduced: I(Y)=(f,g)), D={D}", 3, 1, D*D, D, h, True)
    # shift (3.6): smallest q with H(m) >= a (m - q + 1) for all m in [q, 4D+4]
    Hm = {m: std(m) for m in range(0, 4*D+5)}
    q = next(q for q in range(0, 4*D+5) if all(Hm[m] >= D*D*(m-q+1) for m in range(q, 4*D+5)))
    print(f"      (3.6) shift: minimal q = {q}  vs (n-k)(L-1) = {2*(D-1)}: {q <= 2*(D-1)}")

print("== T3: a points in P^2 (n=2,k=0): general position vs collinear, at degree D ==")
for D in (2, 3, 4):
    for a in sorted(set((2, D, D+1, D+2, comb(D+2, 2)-2, comb(D+2, 2), 2*comb(D+2, 2)))):
        gen = [(random.randint(-10**6, 10**6), random.randint(-10**6, 10**6), 1) for _ in range(a)]
        col = [(i, 2*i+3, 1) for i in range(1, a+1)]
        hg, hc = H(gen, D), H(col, D)
        # components of Env_D: general points iff the degree-D system through them has only them as base locus;
        # sufficient: a <= C(D+2,2)-2 (at least a pencil, 0-dim base locus); collinear points iff a <= D (a degree-D form
        # vanishing at D+1 points of a line vanishes on the line, so for a >= D+1 the line lies in Env_D)
        row(f"{a} general points @D={D}", 2, 0, a, D, hg, a <= comb(D+2, 2) - 2)
        row(f"{a} collinear points @D={D}", 2, 0, a, D, hc, a <= D)
print("  collinear points at their defining degree L = a (line + one degree-a form): H(a) = a, ratio 1")

print("== T4: 0-dimensional complete intersections (all D^n points are components), at L = D ==")
for D in range(1, 7):
    pts2 = [(i, j, 1) for i in range(D) for j in range(D)]
    h2 = H(pts2, D)
    row(f"CI of two degree-{D} curves in P^2 (grid)", 2, 0, D*D, D, h2, True)
    m = next(m for m in range(0, 4*D) if H(pts2, m) == D*D)
    print(f"      (3.6) shift: H(m) = a first at m = {m}  vs (n-k)(L-1) = {2*(D-1)}: q = {m} <= {2*(D-1)}: {m <= 2*(D-1)}")
for D in range(1, 5):
    pts3 = [(i, j, l, 1) for i in range(D) for j in range(D) for l in range(D)]
    h3 = H(pts3, D)
    row(f"CI of three degree-{D} surfaces in P^3 (grid)", 3, 0, D**3, D, h3, True)

print("== T5: isolated points of {l f = l g = 0} (extra 1-dim component l), f=prod(x-i), g=prod(y-j), deg L-1, at L ==")
for L in range(2, 8):
    k_ = L - 1; iso = [(i, j, 1) for i in range(k_) for j in range(k_)]
    row(f"isolated grid of {k_*k_} pts (+ a line), L={L}", 2, 0, k_*k_, L, H(iso, L), True)

print("== summary ==")
hyp = [r for r in out if r[8] is not None]
print(f"  toys satisfying the hypothesis: {len(hyp)}; lower bound H >= c_nk a L^k violated in: {sum(1 for r in hyp if not r[8])}")
print(f"  min over hypothesis-satisfying toys of (H/(aL^k))/c_nk = {min(r[6]/r[7] for r in hyp):.3f}")
nohyp = [r for r in out if r[8] is None]
print(f"  toys violating the hypothesis: {len(nohyp)}; of these, H < c_nk a L^k in {sum(1 for r in nohyp if r[6] < r[7])}  (hypothesis is needed)")
print(f"  upper bound (3.5) violated in: {sum(1 for r in out if not r[9])} of {len(out)}")
```

### `h2_lemma36.py`

```python
# (h') two further toys for Lemma 3.6: (3.8) H_V(bL) <= b^n H_V(L) on affine point sets, and isolated points of a
# system that also has a 1-dimensional component (the "other components of any dimension" clause).
import itertools, math, random
random.seed(7)
P = 1000000007
def rank_mod(rows, p=P):
    rows = [[x % p for x in r] for r in rows]; rk = 0
    for c in range(len(rows[0])):
        piv = next((i for i in range(rk, len(rows)) if rows[i][c]), None)
        if piv is None: continue
        rows[rk], rows[piv] = rows[piv], rows[rk]; inv = pow(rows[rk][c], p-2, p)
        rows[rk] = [x*inv % p for x in rows[rk]]
        for i in range(len(rows)):
            if i != rk and rows[i][c]:
                f = rows[i][c]; rows[i] = [(a-f*b) % p for a, b in zip(rows[i], rows[rk])]
        rk += 1
    return rk
def H_aff(pts, D):      # affine restriction rank of polynomials of degree <= D
    ms = [e for e in itertools.product(range(D+1), repeat=len(pts[0])) if sum(e) <= D]
    return rank_mod([[math.prod(pow(x, ei, P) for x, ei in zip(pt, e)) for e in ms] for pt in pts])
print("== (3.8) H_V(bL) <= b^n H_V(L), n=2, on k x k grids and on random point sets ==")
viol = 0
for k in (3, 5, 7):
    grid = [(i, j) for i in range(k) for j in range(k)]
    rnd = [(random.randint(1, 10**6), random.randint(1, 10**6)) for _ in range(k*k)]
    for name, pts in (("grid", grid), ("random", rnd)):
        for L in (1, 2, 3):
            for b in (2, 3):
                h1, h2 = H_aff(pts, L), H_aff(pts, b*L)
                ok = h2 <= b**2*h1; viol += (not ok)
                print(f"  {name:6s} k={k} L={L} b={b}: H(L)={h1:3d} H(bL)={h2:3d} b^2 H(L)={b*b*h1:3d} ok={ok}")
print("  violations:", viol)
print("== isolated points of {l*f = l*g = 0}: l a line (1-dim component), f=prod(x-i), g=prod(y-j) of degree L-1 ==")
for L in range(2, 8):
    k = L - 1
    iso = [(i, j) for i in range(k) for j in range(k)]       # the line l: x + 2y = -7 misses all of them
    a = len(iso)
    q = next(q for q in range(0, 4*L) if H_aff(iso, q) == a)   # interpolation degree on the isolated points
    HL = H_aff(iso, L)
    print(f"  L={L}: a={a} isolated points, surjectivity degree q={q} (<= 2L={2*L}: {q<=2*L}), H_V(L)={HL}, H_V(L)/a={HL/a:.3f}")
```

### `i_sec56.py`

```python
# (i) explicit numerical constants / exponent inequalities in Sections 5-6, recomputed.
# Exact (sympy) where symbolic; random profiles for the case analyses (seeded).
import math, random, itertools
from sympy import symbols, Rational as R, simplify, sqrt, log, exp, limit, oo, nsimplify, Sum, expand
random.seed(1662)

print("== 5.1 thresholds (5.3): a_K = s^(1/10), a_i = 10 a_{i+1}; claims sum_{r>i} a_r < a_i/9, (5.4) exponent -a_i/2+sum_{r>i}a_r <= -7a_i/18 ==")
worst = -1
for K in range(1, 40):
    a = [10**(K-1-i) for i in range(K)]            # exact integers; a_K normalised to 1, a[0] largest
    for i in range(K):
        tail = sum(a[i+1:])
        assert 9*tail < a[i], (K, i)                # exact: sum_{r>i} a_r < a_i/9
        worst = max(worst, R(-a[i], 2*a[i]) + R(tail, a[i]))
print(f"  max over K<=39, i of (-a_i/2 + sum_(r>i) a_r)/a_i = {worst} = {float(worst):.6f}  vs claimed <= -7/18 = {-7/18:.6f}: {worst <= R(-7,18)}")
print("  exact: sum_{r>i} a_r / a_i -> sum_{m>=1} 10^-m = 1/9 (strict for finite K); 1/2 - 1/9 =", R(1,2)-R(1,9), "= 7/18")
print("  sum_i a_i = s^(1/10) (10^K - 1)/9 with K = O(1+sqrt(log s)): log_s of 10^K factor -> 0, so sum = s^(1/10+o(1)):")
for s in (1e2, 1e4, 1e8, 1e16, 1e32, 1e64):
    K = 1 + math.ceil(math.sqrt(math.log(s)))   # one admissible choice of K = O(1+sqrt(log s))
    tot = s**0.1 * (10**K - 1)/9
    print(f"    s={s:.0e}: K={K}, sum a_i = {tot:.3e}, log(sum)/log(s) = {math.log(tot)/math.log(s):.3f}, sum/s^(1/3) = {tot/s**(1/3):.3e}")
print("  NOTE: o(s^(1/3)) holds asymptotically, but sum/s^(1/3) < 1 only for astronomically large s with this K (between 1e32 and 1e64 above) -- harmless: only the limit is used, no rate is claimed.")

print("== (5.5) summability over dyadic widths 2^m u, u >= s_*: claims 2^(m/10) >= 1+cm (c = log2/10) and sqrt(log(2^m u)) <= sqrt(log u)+sqrt(m log 2) ==")
c = math.log(2)/10; bad = 0
for m in range(0, 400):
    if 2**(m/10) < 1 + c*m - 1e-12: bad += 1
    for u in (2.0, 10.0, 1e3, 1e9):
        if math.sqrt(math.log(2**m*u)) > math.sqrt(math.log(u)) + math.sqrt(m*math.log(2)) + 1e-12: bad += 1
print(f"  violations over m<400, u in {{2,10,1e3,1e9}}: {bad}")
for u in (1e2, 1e4, 1e6, 1e10, 1e20):
    S = sum((1+math.sqrt(math.log(2**m*u)))*math.exp(-(2**m*u)**0.1/2) for m in range(0, 400))
    S3 = sum(math.exp(-(2**m*u)**(1/3)) for m in range(0, 400))
    print(f"    u={u:.0e}: sum_m (1+sqrt(log 2^m u)) exp(-(2^m u)^(1/10)/2) = {S:.3e};  sum_m exp(-(2^m u)^(1/3)) = {S3:.3e}  (both -> 0 as u -> oo)")

print("== 5.1 lower boundary: N exp(-sqrt(2s)) / (N exp(-sqrt(s) - o(s^(1/3)))) = exp(-(sqrt2-1)sqrt(s)+o(s^(1/3))) ==")
s_ = symbols('s', positive=True)
print("  exponent difference -sqrt(2s)+sqrt(s) =", simplify(-sqrt(2*s_)+sqrt(s_)), "; coefficient sqrt2-1 =", float(sqrt(2)-1), "> 0, and s^(1/3) = o(sqrt s)")
print("== 5.1 core: on entry to the last width s_f in [s_*, 2 s_*], degree B exp((1+o(1)) s_f) <= B exp(3 s_*);  E L^2 = (delta N/A) B^2 exp(6 s_*) ==")
B_, N_, d_, delta, sst = symbols('B N d delta s_star', positive=True)
A_ = B_**2
print("  E*L^2 / N =", simplify((delta*N_/A_)*(B_*exp(3*sst))**2/N_), " -> 0 by the choice delta*exp(6 s_*) -> 0")
print("  width halving: batches <= exp(sqrt s); union degree exp(sqrt s)*O(B e^{s/2}) = B exp(s/2 + O(sqrt s)) = B exp((1+o(1)) s/2): relative error O(sqrt(s))/(s/2) -> 0")

print("== (5.6)-(5.7) profiles: sigma(b) = prod_i min(T,D_i) = e_j T^(d-j) on plateau j; b1+b2<0 from sum=0, b1<0<bd, d>=3 ==")
def rand_profile(d):
    while True:
        b = sorted(random.uniform(-1, 1) for _ in range(d - 1))
        last = -sum(b)
        if -1 <= last <= 1:
            b = sorted(b + [last])
            if max(abs(x) for x in b) >= 0.5 and abs(sum(b)) < 1e-12 and b[0] < 0 < b[-1]:
                return b
viol = 0; cnt = 0
for d in (3, 4, 5, 6):
    for _ in range(20000):
        b = rand_profile(d); cnt += 1
        if not (b[0] + b[1] < 0): viol += 1
        # sigma identity in log-scale (B = e^1, s = 1): log T = 1 + t, log D_i = 1 + b_i
        for j in range(d):
            lo = -1 if j == 0 else b[j-1]; hi = b[j] if j < d else 1
            if hi - lo < 1e-9: continue
            t = random.uniform(lo, hi)
            lhs = sum(min(1+t, 1+bi) for bi in b); rhs = sum(1+bi for bi in b[:j]) + (d-j)*(1+t)
            if abs(lhs-rhs) > 1e-9: viol += 1
print(f"  {cnt} random admissible profiles (d=3..6): violations of b1+b2<0 or of the sigma plateau identity: {viol}")
fig2 = [R(-8,10), R(-4,10), R(3,10), R(9,10)]
print("  Figure 2 profile (-0.8,-0.4,0.3,0.9): sum =", sum(fig2), ", b1+b2 =", fig2[0]+fig2[1], ", max|b| =", max(abs(x) for x in fig2))

print("== Prop 5.5: omitted nonreal-line fraction e_{d-1} exp(o(s))/n = exp(o(s))/D_d, D_d = B e^{b_d s} >= B since b_d > 0 ==")
print("  with s <= log B: exp(o(s))/B <= B^{-1+o(1)} -> 0  (exact: e_{d-1}/N = prod_{i<d} D_i / B^d = exp(s*sum_{i<d} b_i)/B = exp(-b_d s)/B)")

print("== (6.5)-(6.7) common window: initial interval rank T^(2d-1) vs sigma^2 * T/(D1 D2) with sigma = T^d and D1 D2 >= T^2 ==")
bad = 0
for d in (3, 4, 5):
    for _ in range(5000):
        b = rand_profile(d); t = random.uniform(-1, b[0])
        # log-scale with log B = 1/s normalisation: logs in units of s, B = e^{beta*s}; use beta = log B / s >= 1
        lhs = (2*d - 1)*t; rhs = 2*d*t + t - (b[0] + b[1])      # log(T^(2d-1)) vs log(sigma^2 T/(D1D2)) relative to B-powers (B-exponents cancel: (2d-1) vs 2d+1-2)
        if lhs < rhs - 1e-12: bad += 1
print(f"  violations of T^(2d-1) >= T^(2d+1)/(D1 D2) on t < b1 (5000 profiles x d=3..5): {bad}")
print("  k = d-1 plateau: D1^2 T^(2d-2) min(1, T/(D1 D2)) <= D1 T^(2d-2)  <=>  min(D1, T/D2) <= 1 (true as T <= D2): checked symbolically below")
D1, D2, T = symbols('D1 D2 T', positive=True)
print("   D1^2 T^(2d-2) * T/(D1 D2) / (D1 T^(2d-2)) =", simplify(D1**2*T/(D1*D2)/D1), " <= 1 iff T <= D2")
print("  (6.7) margins at T = D_d, sigma = N: log(A/D_d)/s = (log B)/s - b_d; log(A/(D1 D2))/s = -(b1+b2)")
for d in (3, 4, 5, 6):
    mins = []
    for _ in range(20000):
        b = rand_profile(d)
        for ratio in (1.0, 2.0, 4.0):         # (log B)/s : 1 = outermost, >= 2 otherwise (dyadic widths)
            m1 = ratio - b[-1]; m2 = -(b[0] + b[1])
            if ratio >= 2: mins.append(min(m1, m2))
    print(f"    d={d}: non-outermost windows, min over 20000 profiles of min(margin1, margin2) = {min(mins):.4f} (> 0 required; margin1 >= 1 always, margin2 = -(b1+b2) > 0)")
print("  outermost s = log B: margin1 = 1 - b_d, zero iff b_d = 1 (the Sec. 6.2 case)")

print("== (6.9) outermost endpoint: s = log B, b_d = 1, final open plateau of dim k after j = d-k cuts, cuts j+1..d at time 1 ==")
for d in range(3, 9):
    feas = []
    for k in range(0, d+1):
        j = d - k
        # need j values in [-1, 1) summing to -k (cuts at time 1 contribute k), and b1 + b2 < 0, plateau positive-dim (k >= 1)
        if k == 0: continue
        if j == 0: continue
        if -j <= -k < j: feas.append(k)   # sum of j values in [-1,1) can be -k iff -j <= -k < j
    print(f"  d={d}: feasible k = {feas}; paper's range 1 <= k < d-1 = {list(range(1, d-1))}; e_j = B^(d-2k) >= 1 forces k <= d/2: {[k for k in feas if 2*k <= d]}")
print("  identities: e_j * (B^2)^k = B^d  =>  e_j = B^(d-2k), N/e_j = B^(2k) = A^k")
print("== (6.10)-(6.11), Lemma 6.4 at the outermost endpoint ==")
print("  t0 > 1+b1+b2 is possible below 1 since b1+b2 < 0; normalized logs of T0/T_s(beta) and T0/(D1 D2): t0-beta and t0-(1+b1+b2):")
t0, beta, b1, b2 = symbols('t0 beta b1 b2', real=True)
Bs = symbols('Bs', positive=True)   # B = e^{s} at s = log B
print("    log(T0/(D1 D2))/s =", simplify((1 + t0) - (1 + b1) - (1 + b2)), "= t0 - (1+b1+b2)")
for d in (4, 5, 6, 7, 8):
    for k in range(2, d-1):
        print(f"    d={d}, k={k}: deletion mass exponent (d-2k)+(k+1) = {d-k+1} < d: {d-k+1 < d}", end=";")
    print()
print("  test degrees T_s(t2) = B^(1+t2) = B^(2-(1-t2)) with t2 < 1: c = (1-t2)/2 works after constants")
print("  Bezout direction count: C E B^(2-c+o(1))/n with E = delta N/A, n >= N sqrt(delta): =", simplify((delta*N_/B_**2)*B_**2/(N_*sqrt(delta))), "* B^(-c+o(1))")
print("  final row count: E M / n <=", simplify((delta*N_/B_**2)/(N_*sqrt(delta))), "* M  = sqrt(delta) M / A -> 0 (no rate needed)")
print("  lift degree: deg(gamma)deg(C->gamma) = deg C - mult_p C >= deg C/2 and sum deg(C->gamma) <= 1  =>  sum deg C <= 2 deg(gamma)")

print("== 6.3 (6.18)-(6.20) and the depth denominators ==")
print("  (6.19): groups of depth <= R e^{eta s}, t_p deg pi_p Y >= deg Y/2  =>  sum_Z deg Z >= a/(2R e^{eta s})")
print("  (6.20)/|P_x|: e_j B^(l+1)/N with e_j = B^j exp(s sum_{i<=j} b_i), l = d-j:")
for d in (3, 4, 5, 6):
    for j in range(1, d):
        l = d - j
        expo_B = j + (l + 1) - d
        print(f"    d={d} j={j}: B-exponent j+(l+1)-d = {expo_B} (claim 1); s-exponent sum_(i<=j) b_i = -sum_(i>j) b_i by sum b = 0", end="\n" if j == d-1 else ";")
for B in (1e6, 1e12, 1e30, 1e100):
    for frac in (0.05, 0.01):
        s = frac*math.log(B); q = B**0.5; r = math.ceil(B*math.exp(-2*s))
        print(f"    wider window: B={B:.0e}, s={frac}*log B: q=B^(1/2)={q:.3e}, r=ceil(B e^(-2s))={r:.3e}, q/r={q/r:.3e}, r >= ... B^{math.log(r)/math.log(B):.3f}")
print("  r - q - O(1) >= r/2 for large B since q = o(r) (q/r = B^(-1/2+o(1)))")
print("  multiplicity compression degree O(L^2/r) with L = B e^{O(s)}, r = B^(1+o(1)): = B e^{O(s)}")

print("== (6.26) strict margins on target plateaux (separated windows), all plateaux j=1..d-1 of random profiles ==")
fails = {}
for d in (3, 4, 5, 6, 7):
    for _ in range(20000):
        b = rand_profile(d)
        for j in range(1, d):           # plateau after j cuts, l = d - j, next cut b_{j+1} = b[j]
            l = d - j; bn = b[j]
            m1 = b[0] + bn                      # R = D1 (always)
            m2 = -sum(b[j+1:])                  # R = B exp(-s sum_{i>j} b_i) (narrower centres)
            m3 = bn - 2                         # R = B exp(-2s) (wider centres, b_{j+1} > 0, l < d-1)
            for side in ("narrow", "wide"):
                opts = [m1]
                if side == "narrow": opts.append(m2)
                if side == "wide" and bn > 0 and l < d - 1: opts.append(m3)
                best = min(opts)
                key = (d, side, "l=1,b_{j+1}>0" if (l == 1 and bn > 0) else "other")
                if best >= -1e-12:
                    fails.setdefault(key, 0); fails[key] += 1
for key in sorted(fails):
    print(f"  NO strict negative margin: d={key[0]} {key[1]:6s} case {key[2]:14s}: {fails[key]} plateau instances")
print("  (paper: the only zero-margin case is narrower centres, final one-dimensional plateau l = 1 with b_{j+1} = b_d > 0, handled in 6.5)")
print("  initial interval ratio A/T^2 = exp(-2 b s): positive margin near b1 < 0")
print("  (6.25)/(6.27) at the last endpoint: sigma T e^{cs}/A / (C E T) = sigma e^{cs}/(C delta N) >= e^{cs/2 - o(s)}/(C delta) >= delta^-1 e^{cs/3}")

print("== 6.5: identities on the final narrow curve plateau (j = d-1, R = B exp(-b_d s)) ==")
bd, s = symbols('b_d s', real=True)
Dd = B_*exp(bd*s); Rr = B_*exp(-bd*s); e_dm1 = B_**d_/Dd   # prod_{i<d} D_i = N/D_d with N = B^d (sum b = 0)
print("  R*D_d =", simplify(Rr*Dd), "= A ;  e_{d-1}/R =", simplify(e_dm1/Rr), "= N/A")
eta, eps = symbols('eta epsilon', positive=True)
print("  exceptional degree / projected degree: (delta (N/A) e^{-eta s}) / ((N/A) e^{-eps s}) =", simplify((delta*exp(-eta*s))/exp(-eps*s)), " -> 0 for 0 < eps < eta")
```

