# R1 report — printed §§2–6 (sieve inputs, decreasing-prime tree, delay functions/path process, harmonic→prime, reference tree)

STATUS: COMPLETE (2026-10-23). Work dir: /tmp/oaimath/021/seats/R1_work/ (all scripts + outputs there).

## 1. VERDICT for my scope

**HOLDS AS READ.** I found no FATAL and no GAP in printed §§2–6 (pp. 6–36). Two EXPOSITION points, below; neither touches
a load-bearing inequality. The four priority items:

1. **Comparison identity / lower-bound expansion (§3, Lemma 3.1, (3.2), (3.7), pp. 9–11).** Exact, and uniform in the classes
   a_p: the sign induction uses only the partition identity (3.2) and nonnegativity of the counts S_{dp}; nothing averages
   over classes. (3.7) is a purely algebraic unrolling of (3.5) to the same stops (the reference tree's inclusion rule depends
   only on exponents, never on classes). Confirmed by brute force on toy parameters with random AND greedy-adversarial
   classes, with a control that breaks it (below).
2. **Positive reference margin (Prop 6.3, (6.20), p. 34).** Every sign-carrying constant recomputed by a route different
   from the paper's; all hold, with large slack. True values: **I = 0.359344** (paper proves I > 0.14, Remark 6.4 > 0.2230),
   **M_g = 4.56459** (paper uses M_g ≤ 4e^γ = 7.124), so the limit is **−a⋆ + 2I/M_g = 0.1474** (paper claims > 0.02).
   Also checked end-to-end in the continuous model: B²·Φ_e(sB,B)·s²/φ_e(s) → 2I/M_g, by direct solution of the
   propagation recursion with no renewal theory used.
3. **§4 renewal/occupation limits.** Each limit is for a FIXED admissible test as r_in → ∞, uniform only in the start ratio
   s_in ∈ [1.99, 2.3] and ℓ ∈ {1,2}; that is exactly what §§5–6 and the later uses I traced (assembly, boxes, stops) invoke.
   ξ does not occur in §§3–6; the only ξ-statement in scope (end of §2, p. 8) puts the ξ-dependence in the threshold, not
   the constant, as it should. Lemma 4.8's C_ε is independent of b₀ as stated; b₀, b₁ are fixed before r_in → ∞.
4. **§5 transfer errors vs §6 needs.** Coupling failure exp(−c₃√log w), log-gap drift CNh, horizon N = O((log B)³), and
   the 1/φ tail control via Lemma 5.4 + Lemma 4.6 are each smaller than what Lemma 6.1, (6.10)–(6.11) and the assembly
   tail (11.2) consume. Key comparison: (log B)^C·E(2) with E(2) = exp(−c√(2 log w)), log w ~ log B, is o(1) — fine.

## 2. Objections

**E1 — EXPOSITION, p. 34, proof of (6.18).** Quoted: "From $0.69<\lambda<0.70$, the expression in braces for $m\geq4$ is at
most $3/(4(0.69)^2)+3/(8(0.69))<2.14$." The braces are $\lambda^{-2}+\frac1m(\frac3{2\lambda}-\lambda^{-2})$; the displayed
number is their value at m = 4. It is the maximum over m ≥ 4 only because $\frac3{2\lambda}-\lambda^{-2}=(3\lambda-2)/(2\lambda^2)>0$
for λ > 2/3 (= 0.0827 at λ = log 2), so the braces decrease in m. Unstated but true; one clause fixes it. Numerically:
braces(m=4) = 2.1188 < 2.14; series = 0.30971 < 0.313; exact majorant (6.18) = 0.312123 < 0.34 (mpmath, 40 digits; the
earlier panel's float overflow in /tmp/oaimath/021/compute/loss_terms.py does not affect this).

**E2 — EXPOSITION, p. 34, proof of Prop 6.3.** Quoted: "$r_0=2B-a_\star+2-\frac{2\log L}{\log w}+o(1)=2B-a_\star+o(1)$."
The o(1) is $-4\log\log L/\log L\,(1+o(1))$, i.e. negative and decaying only like log log L / log L, so the effective
displacement below ratio 2 at finite z is $a_\star+4\log\log L/\log L$, which is ≫ 0.01 for any z one could name.
Harmless for the stated limit (margin 0.147 in the limit) and the constants are declared ineffective, but worth a sentence,
since it is the slowest-converging term in the root benchmark.

No other objection. Items I specifically tried and could not break: the "clearly" steps in Lemma 3.1's size claim
(J_d ≥ w^{a⋆}), the omission-window derivation (6.14) (thresholds increase within parity: A_m − A_{m−2} =
x_{m−1}+2x_m−x_{m−2} ≥ 3−2 > 0), the identification a°=a, c°=c via the no-jump argument in Lemma 4.1, both
invariance equations for π_e, π_o (Lemma 4.4), β = 4A/3, the M_g ≤ 2A bound (pieces A−3, 4, A−1), the extended derivative
weight on [1.98,2) (it is exactly ∫_{s−1}^∞ W₀φ_o with φ_o = A below 1), the three-step domination (4.31) in
Lemma 4.6, the marginal majorants of Lemma 5.4 (induction constant 1+O(δ_w+poly(S)h) per step over N steps), the K_B split in
Prop 5.5(iii), and the Q = (log B)√(log log B) split in (6.8).

## 3. What I checked and how

Read in full, line by line (TeX source of printed §2–§6): §2 (Lemmas 2.1–2.3), §3 ((3.1)–(3.7), Lemma 3.1, §3.1–3.2),
§4 (Lemmas 4.1–4.4, Prop 4.5, Lemma 4.6, Remark 4.7, Lemma 4.8), §5 (Lemmas 5.1, 5.2,
Prop 5.3, Lemma 5.4, Prop 5.5), §6 ((6.1)–(6.22), Lemmas 6.1, 6.2, Prop 6.3, Remark 6.4, Lemma 6.5). Traced
the downstream uses in printed (11.1)–(11.3) and (7.2)–(7.4) and the "Length"/"isolated position" steps of the regular-box proposition (§7).

Hand verifications (all reconstructed, not taken on trust): (3.2) partition; Lemma 3.1 induction incl. stops; (3.7);
r₀ = 2B − a⋆ + o(1); (4.2) from the delay equations; F − f = c₀, F + f = Aω; future integrals (4.4)-(4.5) via derivatives +
decay; auxiliary-chain normalization ∫_{s−1}^∞ c₀ = Aρ(s−1); drift E e^{s_next} ≤ (2/e)e^s at λ = 2; Dickman ratio bounds;
(4.11) deficit forms of φ; φ_e' = −sφ_o(s−1)/(s−1)², φ_o' = −sφ_e(s−1)/(s−1)² (direct differentiation); kernel
normalization; path-weight telescoping (4.17)/(5.5); invariance + β; cycle occupation; renewal limit constant 1/E G =
β/M_g; band bounds; Remark 4.7; Lemma 4.8 geometry (x ∈ [3.19b₀, 0.324b₁], r' > 6.76b₀); Lemma 5.1–5.4; Prop 5.5(i)–(iv);
(6.2) Buchstab product identity; residual cancellation (6.4); the structure of (6.10) (anomaly + residual propagated through
x > 2); (6.11) → (6.12) change of variables (inner integrals y−1 and y²/(y+1), r dr = 4(y+1)dy); I_full = 8/3 (6.13);
loss series (6.15) with windows (6.14); L₁ = 1; tail majorant; e^γ < 1.95; final inequality −0.01 + 0.28/7.8 = 0.0259 > 0.02.

Numerics (all under `ulimit -v 8000000`, nice 19; each with a control that fails):
- `sieve_fns.py`: f, F, ρ from the delay equations by cumulative trapezoid (step 1/20000). Matches closed forms on [2,4],
  ρ on [1,2] to 2e-10; F − f = Aρ(s−1)/s checked. 
- `boundary_I.py` (the independent route for I): solves the cutoff-2 boundary recursion for Q_e(r,2), Q_o(r,2) on a 2-D
  (gap × cutoff) grid with the true admission r − x ≥ x + 2, then integrates (6.12) directly — never uses the first-omission
  series. h = 1/200…1/1600, Richardson: **I = 0.3593435** (stable to 4e-6 across mesh pairs). Paper's route with exact L₂,L₃
  and the earlier seat's MC tail gives 8/3 − ΣL_m = 0.359348: agreement 4e-6. Controls: admission threshold x+2 ± 0.05 →
  I = 0.2638 / 0.4544 (moves by ≫ error). `full_control.py`: admission off (negative gaps allowed) → 2Q ≡ 1 to 1e-6 and
  I_full = 2.666680 vs 8/3 (confirms (6.13) numerically; my first version of this control failed because it truncated
  negative gaps — the true-rule computation never visits negative gaps, which I verified from the admission inequalities).
- `L23_mp.py`: L₂, L₃ by mpmath tanh-sinh nested quadrature on the original integrands: equal to the closed forms (6.16),
  (6.17) to 25 digits; perturbed integrand (A_m + x_m) gives 1.809 / 0.659 (fails, as it must).
- `mg_and_tail.py`: M_g = 4.56458616 (direct integral of π_i g; φ by two routes — finite differences of f,F and the deficit
  formulas — agreeing to 1e-8); ∫₁^∞c = 2, ∫₁^∞a = A−2 confirmed; both invariance balances confirmed at sample points, and
  the control (drop the 1 − s^{−2} factor) fails by 20–45%; tail majorant and coarse bounds as in E1.
- `occupation_check.py` (end-to-end check of Prop 4.5 + 5.5(iv) + (6.10)–(6.12) in the continuous model, no renewal theory):
  (a) propagate the anomalies δ_i through x > 2 by solving Φ_e(r,b) = δ_e(r) − ∫₂^b Φ_o(r−x,x)dx/x,
  Φ_o(r,b) = δ_o(r) − ∫₂^b 1{r−x≥2x}Φ_e(r−x,x)dx/x on a grid; T(s,B) = (s²B²/φ_e(s))Φ_e(sB,B) at s = 2.0:
  0.1977 (B=10), 0.1714 (20), 0.1616 (40), 0.1584 (80); error shrinks ≈4× per doubling; B⁻²-extrapolation 0.15735 vs
  predicted 2I/M_g = 0.15745. s ∈ {1.995, 2.05, 2.1, 2.2, 2.3} converge to the same value (slower at 2.2–2.3:
  0.1592/0.1586 at B=80), consistent with the s-independence the occupation limit predicts after the φ_e(s)/s² normalization.
  (b) decomposition check: the FULL continuous reference recursion Q_e(r,b) (exponents in (1,b], H(x) = max(2x,x+2)) solved
  directly; Q_e(sB,B) − f_i(s)/B extrapolates (h = 1/100, 1/200) to Φ_e(sB,B) at B = 8, 12, s ∈ {1.995 (root-type, uses
  f_ext), 2.0, 2.1, 2.2} — e.g. B=8, s=2: 4.162e-3, 4.092e-3 → 4.02e-3 vs Φ_e = 4.021e-3. So the "continuous residual is
  identically zero" claim and the root decomposition (6.10) hold, including the starting extension. Combined: in the
  continuous model B²Q_e(r₀,B)/e^γ → −a⋆ + 2I/M_g = 0.147 > 0.
- `tree_toy.py` (priority 1): brute force with w ∈ {3,5,7}, z ∈ {40,60,90}, Y ∈ {1500,3000,6000}, a⋆ ∈ {0.01, 0.5, 1.5};
  40 random class choices + 3 greedy-adversarial (each big prime's class chosen to hit the most current survivors) per setting,
  each with no stops and with random prefix-free lower stops: 0 failures of alternating-sum ≤ S₁(B) (min slack 17); size claim
  min J_d ≥ w^{a⋆} held in every case; (3.2) exact at random nodes; (3.7) exact to 2e-13 with random stops. Controls:
  moving the admission test from upper to lower nodes breaks the lower bound in 80/80 trials; a perturbed reference
  recursion breaks (3.7) by 4–34 (units of counts).
- `ratio_checks.py`: a/c₀ ∈ [0.281, 0.562], c/c₀ ∈ [0.438, 0.719] on [1,8] (compact in (0,1), as (4.3) claims); φ_e, φ_o
  positive and nonincreasing; uρ(u)/ρ(u−1) ∈ [0.29, 0.62] ⊂ [1/(4u), 1].

## 4. What I could NOT check

- The prime transfer (§5) numerically: w, B are asymptotic (z = 10^100 gives w ≈ 7.8, B ≈ 112), so no finite-prime
  experiment is meaningful. §5 was checked by hand only.
- Cited inputs not re-derived: the dimension-2 fundamental lemma in the τ(l)^C-weighted form (Lemma 2.1, citing Sofos 2023
  Lemma 2.8 / Friedlander–Iwaniec Cor. 6.10 — sources not opened; the stated form is weaker than the standard one, so I accept
  it), Siegel–Walfisz/Brun–Titchmarsh (Lemma 2.2(ii),(iii)), Heath-Brown 1982 Theorem p. 1365 for 2.2(iv) (only the tiling
  reduction was checked), the key renewal theorem as stated in Serfozo §2.7 Thm 35, and the Kloosterman/large-sieve inputs
  (used outside my scope).
- The numerical I and M_g are floating-point (mesh-extrapolated) values, not interval arithmetic; they are used only to
  confirm the paper's rigorous bounds with ~2.5× (I) and ~7× (margin) slack, so this does not matter.
- Lemma 6.5's discrete half (6.22) relies on the same compact-convergence argument as Lemma 6.2; not tested numerically.

## 5. Where a hole would most likely hide in this scope

The likeliest place was Prop 6.3's sign: a B^{-2} quantity extracted from an alternating tree of harmonic mass ~B, whose value
depends on (i) the residual of the benchmark being exactly zero in the continuous model (including the f_ext / F = A/s
continuations at the root), (ii) the renewal normalization 1/E G = β/M_g, and (iii) the loss series with its windows. Any
sign or factor-2 slip in (6.10)–(6.15) would flip or shrink the margin, and the paper's own check (I > 0.14 vs the needed
0.0356) is only 4× above the threshold. I believe there is no hole there: the three ingredients were checked by three
independent numerical routes (direct boundary recursion for I; direct M_g; direct propagation and full-recursion solves that
reproduce the predicted limit 0.1574 to 0.1%), and the true margin 0.147 is seven times the claimed 0.02. The remaining
risk in my scope is in the analytic §5 transfer, which is standard (PNT with de la Vallée Poussin error against a
(log B)^{O(1)} horizon) and which I could only read, not test.

---
Receipts: every script's stdout is saved beside it in R1_work/*.out. Label note: script printouts that say "(3.5)" or
"(3.2)" use the TeX source order; the comparison identity is printed (3.7), the tree identity printed (3.2), the tail
majorant printed (6.18), the M_g bound printed (4.22), the margin printed (6.20).
