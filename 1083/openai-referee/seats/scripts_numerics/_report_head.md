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
