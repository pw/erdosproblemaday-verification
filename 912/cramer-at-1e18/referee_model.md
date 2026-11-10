# Referee report: Claims 3–5 (model comparison), Erdős #912

Hostile referee, 2026-11-10. Scope: CLAIMS.md Claims 3, 4 and 5, plus hfast.c, model.c, mc_control.py, summary.py and their outputs. I edited no file except this one. My scratch scripts and outputs are in `/tmp/ref912/` (`indep.py`, `pair.py`, `pair_asym.py`, `owmire_ur.py`, `tabcheck.py`, `table.py`, `*.out`).

## Verdict: HOLDS WITH FIXES

**The numbers hold.** model.c computes what it says it computes. My own per-integer computation, with no midpoint approximation and coprimality tested by direct modulus, reproduces its E[J], sd, sieve-model values and u_0/u_1/u_2 to ≤ 0.01 at n = 10^6, 10^12 and 10^13. The region definition is the same set as hfast's J. The variance formula is right, and the Z-scores convert to legitimate Bernstein tail bounds. h(10^15) is now also independently confirmed by href.py: 13,837,595, |A∩B| = 0.

**The interpretation needs fixes.** I found five problems:
1. The "sieve model z closes the gap monotonically" story fails once z is pushed past 19. At 10^12 and 10^13 the family plateaus and then overshoots the actual J.
2. The "≈ 0.64 · loglog n/log n" description has the wrong functional form.
3. The mechanism is cited to the wrong literature.
4. The Z-score headline is true but uninformative.
5. Claim 5 omits the π(√n) term. That term is why Owmire's constant matches small-n data.

**A stronger replacement exists, and I computed it.** It is a parameter-free Hardy–Littlewood pair-correlation correction, built from the exact singular series. That term alone accounts for 78–84% of the gap at every n from 10^12 to 10^18. With the higher-order factor calibrated on the z = 19 model, it accounts for 98.7–99.1%. Asymptotically it cancels the negative loglog n term in G–I's Theorem 1.2 exactly. This is a heuristic, but it is the right one to put on the page instead of the z-fit.

---

## 0. Own numbers: model.c vs an independent exact computation

`indep.py` works as follows:
- For every integer l in (s, n//k_c], it sums log1p(−p_l) exactly into its k = n//l.
- For k < k_c, P(empty) < e^{−60}. This is checked by assertion: min len/log b is 97 at 10^6, 110 at 10^12 and 112 at 10^13.
- The sieve models use direct `l % p` tests and never touch model.c's prefix tables.
- u_r is the exact Poisson-binomial, not the binomial at the midpoint.

| n | quantity | model.c | referee (exact, per integer) |
|---|---|---|---|
| 10^6 | E_C[J] / sd | 526.12 / 12.17 | 526.120 / 12.172 |
| 10^6 | E_z5[J] | 554.03 | 554.034 |
| 10^12 | E_C[J] / sd | 400,378.95 / 359.44 | 400,378.954 / 359.444 |
| 10^12 | E_z19[J] / sd | 413,875.88 / 314.55 | 413,875.882 / 314.553 |
| 10^12 | u_0, u_1, u_2 (k ≥ K0, Cramér) | 599,620.0, 175,791.5, 56,888.8 | 599,620.05, 175,791.49, 56,888.80 |
| 10^13 | E_C[J] / sd | 1,224,843.30 / 632.39 | 1,224,843.302 / 632.392 |
| 10^13 | E_z19[J] | 1,263,770.41 | 1,263,770.411 |
| 10^13 | u_0, u_1, u_2 | 1,937,433.7, 540,325.9, 173,183.4 | 1,937,433.70, 540,325.88, 173,183.44 |

Actual values: J(10^12) = 414,491 and J(10^13) = 1,265,488 (hfast). h(10^12) = 492,989 and h(10^13) = 1,493,135 agree with href.log. At 10^12, every z from 2 to 19 agrees with model.c to < 0.01 (`indep_1e12.out`).

## 1. Code checks (task item 1): all PASS

- **Region.** For integer l, ⌊n/l⌋ = k ⇔ n/(k+1) < l ≤ n/k ⇔ ⌊n/(k+1)⌋ < l ≤ ⌊n/k⌋. So (a, b] with integer endpoints is exact; there is no off-by-one between n/(k+1) and ⌊n/(k+1)⌋. The clip `a = max(a, s)` gives exactly l > s, which is hfast's "prime p > s". Both programs use kmax = ⌊n/(s+1)⌋, and k = kmax+1 has b ≤ s. hfast's region M (k < K0, intervals (⌊n/(k+1)⌋, ⌊n/k⌋]) and region S (p ≤ ⌊n/K0⌋ ⇔ k ≥ K0) partition k = 1..kmax with no overlap. `mid = (a+b)/2 + 1/2` is the mean of the integers a+1..b, so the linear Taylor term cancels exactly.
- **Midpoint error, analytic bound.** f(l) = log(1 − 1/log l) has |f''(l)| ≲ 1/(l² log² l). The per-interval error in log P0 is ≤ max|f''|·len³/24 ≈ len/(24 k² log² l), since len/l ≈ 1/k. Weighted by P0 ≤ e^{−len/log}, each k contributes ≤ 1/(24 e k² log l). Summed over k ≥ k_c that is ≲ 10^{−6}. At sd ~ 10^3–10^4 this is irrelevant, and the empirical difference is < 0.01 (table above).
- **Variance.** The I_k are disjoint, and the model draws each integer independently, so the A_k are independent. Var J = Σ p_k(1−p_k) is exact. This holds in the z-models too: given the fixed coprimality pattern, the draws are still independent across integers.
- **Z as a probability.** Bernstein for a sum of independent centred variables bounded by 1 gives P(J − EJ ≥ t) ≤ exp(−t²/(2σ² + 2t/3)).

  | n | Z | bound |
  |---|---|---|
  | 10^12 | +39 | e^{−744} |
  | 10^13 | +64 | e^{−1998} |
  | 10^15 | +178 | e^{−15,390} |
  | 10^16 | +298 | e^{−43,020} |
  | 10^17 | +500 | e^{−121,500} |
  | 10^18 | +840 | e^{−343,500} ≈ 10^{−149,200} |

  Since t ≪ 3σ², this is essentially the Gaussian Z²/2. **The Z-scores are legitimate tail statements within the model.** For the z = 19 residual: Z = +9.6 → e^{−46}, and +47.0 → e^{−1105}. At 10^12 and 10^13 the z = 19 residual is Z = +2.0 and +3.1, which is not significant.
- **Coprime prefix tables.** I rebuilt them by the same construction and compared F(b) − F(a) against a direct count. For every z ≤ 19 there were 0 mismatches in 300 random intervals in [10^6, 10^12], and tab[P] = φ(P) each time (`tabcheck.py`). Stronger: model.c's z-model E[J] matches my direct-modulus computation to < 0.01 for every z ≤ 19 at 10^12 and 10^13. uint32 holds φ(P_19) = 1,658,880, and (b/P)·φ ≤ 1.7·10^17 fits in uint64.
- **u_r recurrence.** P(r+1) = P(r)·(N−r)/(r+1)·q/(1−q), started at (1−q)^N, is the binomial pmf. With mean ≈ 40 at K0, p0 ≈ e^{−40} does not underflow. It agrees with the exact Poisson-binomial to 0.01 (table).
- **mc_control (n = 10^6, 3,000 draws).** Correct as far as it goes, but weak: se 0.22 on sd 12, and at the smallest n. It is now superseded by the exact cross-check. Say so in CLAIMS.

**Fix 1 (wording).** Objected sentence: *"Exact Cramér expectation E_C[J] (sum over k of 1 − Π…, log l at the interval midpoint)"*. "Exact" sits next to "midpoint" in the same sentence. Write instead: "finite-n Cramér expectation (midpoint log l; agrees with the per-integer sum to < 0.01 at 10^6, 10^12, 10^13)".

## 2. The headline (task item 5)

Objected sentence: *"The Cramér model's finite-n prediction is wrong by hundreds of its own SDs"*.

This is true, but it is not informative. Any bias of size ≍ scale·loglog n/log n grows like n^{1/4}·(loglog n)/(log n)^{3/4} relative to the model sd (≍ n^{1/4}/(log n)^{3/4}·const). So Z must reach the hundreds at these n for any model that misses a second-order term. A skeptic will read the headline as "Cramér is wrong", which says nothing about c.

The informative quantity is the bias in units of the scale: 0.0649 → 0.0579, i.e. 2.6% → 2.3% of h/scale. The point that matters is that this is a **bias of the model mean, not model noise**: sd/scale ≈ 4·10^{−4} at 10^15. Suggested headline: "At 10^15–10^18 the Cramér model's finite-n mean is low by 2.3–2.6% of scale; model noise is 10^{−4} of scale, so 2.57 is a model bias, not a fluctuation."

## 3. The "0.63–0.645 · loglog n/log n" description (task item 3)

Objected sentence: *"The gap (J − E_C[J])/scale = 0.0649, 0.0623, 0.0601, 0.0579, i.e. ≈ 0.63–0.645 · loglog n / log n at all four n."*

The four numbers are right. The "i.e." suggests a fitted coefficient of loglog n/log n, and that reading is wrong. The coefficient drifts upward monotonically (0.6324, 0.6368, 0.6417, 0.6448). My HL computation (§5) gives, at the pair level, **gap/scale → √(π/2)·(loglog n − 2.2417)/log n**. That is a loglog n/log n coefficient of √(π/2) ≈ 1.253, together with a large negative 1/log n term.

The derivation sketch:

    gap/scale ≈ (1/L)∫e^{−2/t²}(2/t²)(log H + 0.4151)dt,  with H = L/t²
              = √(π/2)[LL − log 2 + 0.4151 + ψ(1/2)]/L

Here 0.4151 = γ + log 2π − 2 comes from the numerically confirmed Σ_{d<H}(H−d)(𝔖(d)−1) = −½H log H − 0.2075H + O(√H). I checked D(1000) = −3658.8 against the formula's −3661.4.

The continuous-t numerics converge to this: gap·L = 5.7549 vs 5.7449 at n = 10^400, and 4.0302 vs 4.0075 at 10^100 (`pair_asym.py`). They also reproduce the discrete pair sums at 10^12–10^15 to 0.3%.

So "0.64" is a pre-asymptotic blend of two terms, not a coefficient. **Fix:** report the four numbers and say "of order loglog n/log n". Drop "≈ 0.63–0.645 · loglog n/log n", or label it explicitly as a numerical description over 10^15–10^18 only.

## 4. The sieve-model-z narrative and over-fitting (task item 3)

Objected sentence: *"Sieve model z … closes the gap monotonically in z; z = 19 leaves ~5% of it (Z = +10, +16, +28, +47)."*

The numbers are correct, and so is monotonicity for z ≤ 19 at n ≥ 10^12. But z is a free knob, and the family does **not** converge to the actual value. I extended it to z = 139 (exact per integer; `indep_1e12.out`, `indep_1e13.out`):

| n | actual J | z = 19 | z ≈ 37–97 (plateau) | turns non-monotone at | crosses actual J | z = 139 |
|---|---|---|---|---|---|---|
| 10^12 | 414,491 | 413,876 | 414,137–414,502 | z = 43 (414,166 < 414,176 at z = 41) | between z = 89 and 97 | 415,439 (+3.7 sd over) |
| 10^13 | 1,265,488 | 1,263,770 | 1,264,642–1,264,956 | z = 61–83 (dips) | between z = 113 and 127 | 1,265,962 (+1.0 sd over) |

At 10^6 the family is already non-monotone at z = 17 and 19 (558.2 → 557.5 → 553.8; actual 555), because θ_z/log l ≈ 0.8 there.

**Why it overshoots.** For large z, the model's per-integer probability θ_z/log l is not small: θ_19/log l is 0.31 at 10^15 and 0.26 at 10^18 in the critical range. More importantly, P_z dwarfs the range of l, so position averages of r-tuple coprimality leave the fundamental-lemma regime. Fixed-z models then stop representing Hardy–Littlewood. "z → ∞ closes the gap" is false at fixed n, and "z = 19 leaves 5%" is one point on a curve that crosses the target. That is a fit-shaped statement even though z was never tuned.

**Fix:** state the z ≤ 19 numbers, and add: "the family is non-monotone beyond z ≈ 40 and overshoots for z ≳ 100 at 10^12–10^13, so it is a diagnostic of direction, not a prediction." Better still, replace it with the parameter-free HL computation in §5.

**Is "sieve model z" a legitimate Cramér–Granville-type model?** Yes in form: integers coprime to P_z are "prime" with probability (P_z/φ(P_z))/log l, which is Granville's normalisation. But Granville lets z grow with x (z → ∞, log z = o(log x)), and here z is fixed. Call it a "fixed-z Granville-type sieve model". Do not imply it answers G–I's remark ("It would be interesting to apply other models … such as the Cramér–Granville model …, but this seems to be more difficult"). They meant proving the expansion; these are finite-n numerics.

**Does each fixed-z model have limit √(2π)?** Yes. For k = t·scale with t in a compact set, H_k ≍ log n → ∞. The number of z-rough integers in I_k is H_k/θ_z + O_z(1), and θ_z q → 0. So log P(empty) = −(2/t²)(1 + o(1)), and E A_k → 1 − e^{−2/t²}. The tails are bounded exactly as in G–I §3.2. So "every sieve model here has the same limit √(2π)" holds for fixed z. Put this one-line reason in.

## 5. Mechanism and attribution, with the parameter-free replacement (task item 3)

Objected sentence: *"Reading: the 2.57 at 10^15 is the Cramér model's known blindness to small-prime divisibility (Granville 1995) acting at second order — not evidence against c = √(2π)"*.

**Attribution.** Granville 1995 is mainly about Maier's theorem and large gaps, which are first-order failures for extreme statistics. The second-order effect here, on counts in typical intervals of length ≍ log x, is the Hardy–Littlewood pair correlation. Gallagher (1976) showed under HL that the counts are Poisson to first order, which is why c is unchanged. Montgomery–Soundararajan (2004) showed the variance is h log(x/h) rather than Cramér's h log x. That is a relative correction of log h/log x, which with h ≍ log n is exactly loglog n/log n. Cite these.

**The parameter-free test (referee's computation, `pair.py`).**
- Take an interval of H integers at height x, with q = 1/log x.
- HL changes the second factorial cumulant by 2q²D(H), where D(H) = Σ_{d<H}(H−d)(𝔖(d) − 1) and 𝔖 is the full singular series.
- To second order, log P0_true = log P0_Cramér + q²D(H).
- The same formula with the truncated 𝔖_19 is *exactly* the pair correlation of model.c's z = 19 model. Comparing it with model.c's exact z = 19 value therefore calibrates the neglected higher orders.

| n | gap = J − E_C | HL pair-only | pair-only / gap | z19 exact / z19 pair | z5 exact / z5 pair | HL pair × (z19 factor) / gap |
|---|---|---|---|---|---|---|
| 10^12 | 14,112 | 10,981 | **0.778** | 1.269 | 1.226 | **0.987** |
| 10^13 | 40,645 | 32,352 | **0.796** | 1.245 | 1.207 | **0.991** |
| 10^15 | 348,987 | 283,973 | **0.814** | 1.214 | 1.179 | **0.988** |
| 10^16 | 1,026,994 | 845,454 | **0.823** | 1.201 | 1.168 | **0.989** |
| 10^17 | 3,038,563 | 2,524,290 | **0.831** | 1.190 | 1.157 | **0.988** |
| 10^18 | 9,000,142 | 7,556,372 | **0.840** | 1.180 | 1.149 | **0.990** |

The part of the gap above z = 19 (J − E_z19) is predicted at 71–82% of its actual size by (pair_full − pair_19) × factor (434 vs 615 … 382,568 vs 469,419). The higher-order factor for the full 𝔖 is evidently a little larger than the z = 19 factor.

How to read the table:
- With no free parameter, the singular-series pair term explains 78–84% of the gap, and the share rises with n, as it should once the higher-order terms (O((loglog n/log n)²)) fade.
- With the higher-order inflation measured on the truncated model, it explains ~99% at every n. That calibration step is a heuristic: the factor rises with z (z5 < z19), so the full-𝔖 factor is plausibly a bit larger, i.e. ≥ 99%.
- The z-family plateau at 10^12 and 10^13 sits 2.3% and 1.4% of the gap below the actual value. That agrees with the ~99% figure.

**The answer to G–I's actual worry.** They wrote *"Since the second term in h_C(n!) turns out to be negative, it is not clear to us whether the Cramér model gives the correct prediction"*. The pair-level HL correction is +√(π/2)(LL − 2.2417)/L·scale = √(2π)·scale·(LL/(2L) − 1.121/L). Its loglog term **exactly cancels** G–I's −LL/(2L), because √(π/2) = √(2π)/2. The heuristic HL expansion is then

h(n) ≈ √(2π)(n/log n)^{1/2}·(1 + (γ + log 2π − 1)/(2 log n) + o(1/log n)), with (γ + log 2π − 1)/2 = 0.7075.

The data's (h/(√(2π)·scale) − 1)·log n is 0.934, 0.916, 0.896, 0.885, 0.877 and 0.867 at 10^12 … 10^18. It decreases slowly toward the pair-level 0.71, and the excess (0.16–0.22) is about the size of the (loglog n)²/log n-type higher-order terms (≈ 0.34–0.36/L·const). The Cramér expansion's own coefficient is −LL/2 + 1.83, which is +0.06 to −0.03 here and nowhere near the data.

This is a heuristic: second-order factorial-cumulant truncation plus HL. It still needs an independent derivation and a cold check before it goes on any public page. But it replaces "a free-parameter family gets within 5%" with "the standard second-order prime-correlation term predicts the excess, and its sign and loglog cancellation explain why 2.57 > √(2π)".

## 6. "Not evidence against c = √(2π)" (task item 3)

This is justified as a *negative* statement. A model family with limit √(2π) reproduces ~95–99% of the excess, so the excess carries no information against √(2π). It must not slide into a positive statement. The corrections are ≍ loglog n/log n, still 2–3% at 10^18 and decaying logarithmically, so no reachable n distinguishes c = √(2π) from a nearby constant without the second-order theory. c = √(2π) remains conditional on prime-tuple-type heuristics, exactly as before.

## 7. Claim 5: Owmire's c_r (task item 4)

**Re-derivation.** Put k = t·(n/log n)^{1/2}. The interval length is ≈ log n/t², at height ≈ √(n log n) where the density is ≈ 2/log n, so the count is ≈ Poisson(2/t²). With u = 2/t² and dt = (√2/2)u^{−3/2}du:

∫_0^∞ P(Poi(2/t²) = r) dt = (√2/2)∫e^{−u}u^{r−3/2}/r! du = (√2/2)Γ(r − 1/2)/r!

Next, Π_{j<r}(1/2 − j) = ½(−1)^{r−1}Γ(r − 1/2)/Γ(1/2). Hence √(2π)(−1)^{r+1}C(½, r) = √2·Γ(r − ½)/(2·r!), which is the same expression. This gives c_1 = √(π/2) = 1.25331 and c_2 = √(2π)/8 = 0.31333. cr_check.txt agrees to 12 digits. Σ_{r≥1}(−1)^{r+1}C(a, r) = 1 − (1−1)^a = 1 for a > 0 (the binomial series converges at x = −1 for a > 0). Both families sum to √(2π). **Correct.**

**Fairness.** Owmire (forum, 24 Jun 2026) claims c_r = √(2π)(−1)^{r+1}C(2−√2, r) "by the same Cramer model as Tao". His u_r counts *all* exponents. The p ≤ √n exponents are isolated, so they add π(√n) ≈ 2√n/log n to u_1, which is o(scale). The Cramér limit is therefore (√2/2)Γ(r−½)/r!, and c_1 = 1.2533 ≠ 1.4683. "Owmire's c_r is not the Cramér limit" is fair.

**Missing caveat (fix).** u_1/scale is 1.5065 at 10^8 and 1.4754 at 10^9, against Owmire's 1.4683 (`owmire_ur.py`). The match comes from π(√n)/scale = 0.53 and 0.49, which decays only like 2/√(log n) and is still 0.33 at 10^17 (u_1/scale ≈ 1.377 there). Without π(√n), u_1/scale is 0.979 and 0.986. Owmire's c_1 is consistent with reachable data for this reason, so a skeptic would ask why the claimed "wrong" formula fits the data better than the "right" one. Add one sentence: "Owmire's c_1 happens to match u_1/scale at n ≤ 10^9 because u_1 includes the π(√n) ≍ 2/√(log n)·scale small-prime exponents; subtract them and compare at k ≥ K0, where the Cramér/HL picture applies."

## 8. Claim 3: independence of the exact values

- h(10^15) = 13,837,595 is now confirmed by a genuinely independent route: href.py (GMP next_prime, Heyman–Miraj union, no isolation lemma, |A∩B| = 0; `href_1e15.log`).
- 10^16–10^18 rest on hfast alone. The xcheck.log K0×2 / K0×0.5 reruns (all identical: 42,289,684, 129,533,241, 397,503,133) only move the sieve/MR boundary inside one implementation. That is an internal-consistency check, not an independent route.
- Fix: say so, or run href at 10^16. It is ~3× the 10^15 run, roughly an hour, but the B set may need a bitset rather than a Python set to stay under 4 GB.

## 9. Smaller points

- *"G–I's expansion gives 2.5108, … (consistent within its O(loglog/log^{3/2}) error)"*. "Consistent with an O(·) of unknown constant" says nothing. Report instead the normalised residual (E_C[h] − GI)/(√(2π)·scale·LL/L^{3/2}) = −0.090, −0.093, −0.096, −0.098: stable, O(1), consistent with a next term of that shape.
- *"Per class … u_1 = 52,507,646 vs Cramér 48,972,543"*. Correct. Say what it means: actual u_0 and u_2 are below Cramér while u_1 is above it. That is a sub-Poisson (less clumped) count distribution, which is the Montgomery–Soundararajan variance deficit, the same mechanism as §5.
- summary.py counts the prime 2 as certain while G–I's model starts at 3. This is a +1 offset and irrelevant, but say it.

## Weakest honest phrasing (suggested replacement for the "Reading" line of Claim 4)

> At 10^15–10^18 the exact h(n) exceeds the Cramér model's finite-n mean by 0.065–0.058·(n/log n)^{1/2} (2.6–2.3%). That is a bias of the model mean, far outside model noise. The second-order Hardy–Littlewood pair correlation, computed from the singular series with no free parameter, accounts for ~80% of the excess at every n from 10^12 to 10^18; it is the Montgomery–Soundararajan h log(x/h) variance deficit. With higher-order terms calibrated on a fixed-z (z = 19) Granville-type sieve model it accounts for ~99%. At the pair level this term cancels the negative loglog n/(2 log n) term of G–I's Theorem 1.2. Every model used has leading constant √(2π). So the observed 2.57 gives no reason to doubt c = √(2π), but it cannot confirm it either: the corrections decay only like 1/log n, and the limit remains a prime-tuples heuristic. (Fixed-z sieve models are a directional diagnostic only: for z ≫ log n they overshoot.)

## Files

- `/tmp/ref912/indep.py`, `indep_1e12.out`, `indep_1e13.out`: exact per-integer E[J], sd and u_r, Cramér plus z = 2…139.
- `/tmp/ref912/model_1e12.out`, `model_1e13.out`, `hfast_1e1{2,3}.out`: model.c and hfast at 10^12 and 10^13 (bitsets in /tmp/ref912).
- `/tmp/ref912/pair.py`, `pair_a.out`, `pair_b.out`: the HL pair-only prediction (full and truncated 𝔖). `pair_asym.py`: asymptotics to 10^400.
- `/tmp/ref912/owmire_ur.py`: u_r at 10^8 and 10^9. `tabcheck.py`: prefix-table brute force. `table.py`: summary of §5.
