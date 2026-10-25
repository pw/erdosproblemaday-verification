# Seat C (judgment) — Didin & Pimenov, (1:2)-biased clique game

**VERDICT: SOUND AS READ.** The theorem is the asymptotic (1:2) case only. With the paper's own constants it holds from n_0 ≈ 3^148.5 ≈ 10^70.9 (Lean certifies n ≥ 3^158 ≈ 10^75.4). No variant of the method can certify any n below about 10^16. Erdős #778 Q2 ("for all n > 3") stays **OPEN** for 8 ≤ n < n_0. The citation of [2] (1:4) is **accurate** for the version cited (v2); the live-page comment refers to v1.

Scripts and outputs are in this folder: `threshold.py/.out`, `verify_points.py/.out`, `family.py/.out` (UP block only), `down2.py/.out`, `verify_t06.py/.out`, `ms_v2/` (MS v1 and v2 PDFs and text).

---

## 1. Read as a whole

**Soundness.** Every step checks:
- **Q-weights.** A Bella edge triples Q_A, so the increase is 2·Q_A. A Chingiz edge kills Q_A, so the decrease is Q_A.
- **P-weights.** A Bella edge multiplies P_U by 6/5, so the increase is P_U/5. A Chingiz edge multiplies P_U by (3/4)(6/5) = 9/10, or zeroes it at the threshold, so the decrease is at least P_U/10.
- **Danger.** With danger = ΣQ + ΣP/10, each Chingiz edge lowers Φ by at least its danger. Weights only fall during Chingiz's moves, so z's danger is non-increasing and both greedy picks cost at least d*(z). Bella's increase is then exactly 2·d*(z).
- **Initial bounds.** Correct, including the opening-edge factors 3 and 6/5.
- **Terminal properties (1).** f = 0 at the end, so any violation makes a single weight ≥ 1, contradicting Φ < 1.
- **Averaging identity.** e_C(S)·C(s−2, ℓ−2) = Σ_U e_C(U). Correct.
- **Lemma 2 recurrence.** m+3/2 → (3/5)(m+3/2), because (3/5)(3/2) = 9/10 = 3/2 − 3/5. Correct.

**The one idea.** It is a single greedy danger function that adds two potentials at the same 2:1 exchange rate:
- an Erdős–Selfridge blocker, Q = 3^(−f), with base 1 + bias;
- a Chernoff-type density forcer, P = (4/3)^(3H/5 − x)·(5/6)^f.

So every Chingiz edge blocks and builds at once. Malekshahian–Spiro instead split Chingiz's q edges into blockers and builders, which needs q ≥ 4 when Bella plays one edge.

The P-family forces Chingiz density ≥ 3/5 on every ℓ-set with ℓ = Θ(log n). Greedy extraction then gives log_{5/3} n against the blocker's 2·log_3 n, and the comparison is (5/3)² = 25/9 < 3 = 27/9.

**What "sufficiently large" hides.** Nothing load-bearing. It covers three explicit numerical conditions:
- ℓ ≤ n;
- Φ_init < 1, which is never binding near the threshold (ΣQ ≤ 10^−71, ln ΣP ≈ −1900);
- R(n) ≥ a, which is the binding condition.

The O(log log n) error is explicitly log_{5/3}(ℓ + 3/2) + O(1).

Two harmless undercounts:
- Lemma 2 throws away V_R, which has at least (3/5)(ℓ − 1) vertices, all adjacent to v_0, …, v_{R−1}. So ω(G_C) ≥ R + 1.
- Since |V_R| ≥ a, (1) puts a Chingiz edge inside V_R, giving ω(G_C) ≥ R + 2.

**What the result is.** It is exactly Cambie–Provoost Conjecture 17 for p = 1, and the (1,2) case of Malekshahian–Spiro v2 Conjecture 1. The paper credits neither. Our computation covers n = 4..7. The range 8 ≤ n < 3^158 is not certified by anything.

## 2. Explicit n_0 from the paper's own constants

θ = (4/3)^(3/5)·(5/6) = 0.9903346989. η = −ln θ = 0.0097123133, so 2/η = 205.924. θ^5 = 6250/6561 was checked.

Leading constants:

| | value |
|---|---|
| 1/ln(5/3) | 1.957615 |
| 2/ln 3 | 1.820478 |
| gap per unit of ln n | 0.137137 |
| same gap in log_3 units, κ = log_3(27/25) | 0.070053 |

**Conditions used.** The paper's literal bounds:
- a = ⌈2·log_3 n⌉ + 2;
- ℓ = ⌈C·ln n⌉;
- ΣQ ≤ 3^(1−a/2);
- ΣP ≤ (6/5)·(n·θ^((ℓ−1)/2))^ℓ;
- R(n) = 1 + ⌊log_{5/3}((n + 3/2)/(ℓ + 3/2))⌋;
- require ΣQ + ΣP < 1 and R ≥ a.

I scanned ln n ∈ [20, 400] at step 2·10^−5 (`threshold.py`). Independently, I checked every half-integer block start 3^(k/2) for k = 250..359 with exact integers in mpmath (`verify_points.py`).

**Result.**

| setting | last failure |
|---|---|
| best admissible C (any C ∈ (205.92, 210], equivalently least admissible ℓ per n) | ln n = 163.16, so n_0 ≈ 10^70.86 ≈ 3^148.51 |

- The first success is at ln n = 155.45 (≈ 10^67.5). Between 10^67.5 and 10^70.9, wins and losses alternate because a and R are step functions.
- At the threshold: a = 300, ℓ = 33,612, R = 300.
- The last failing block is n just above 3^148.5. There a = 300 and R = 299, and R steps to 300 at ln n = 163.159.

Sensitivity:

| variation | n_0 |
|---|---|
| C = 227.6 (Lean's ℓ ≈ 250·log_3 n) | 3^150.0 |
| C = 300 | 3^154.0 |
| C(n,ℓ) ≤ n^ℓ/ℓ! instead of n^ℓ | 3^147.5 (negligible) |

**Lean comparison.** 3^158 ≈ 10^75.39, about 3^9.5 ≈ 3×10^4 times the paper-constant n_0. Lean's sufficient inequality, 125·25^k·(500k + 505) ≤ 2·27^(k+1), fails at k = 157 and holds at k = 158. So 158 is tight for Lean's own parametrization; "deliberately unoptimized" overstates the slack. The gap to 3^148.5 has two sources:
- Lean uses a = 2⌊log_3 n⌋ + 4, which is effectively one more unit of a at the worst point. Each unit of a costs 1/0.137 ≈ 7.3 in ln n, about 6.6 in log_3 n.
- Lean's C ≈ 227.6 adds about 1.5 in log_3 n.

**Why the threshold is so large.**
1. The win is a first-order race whose margin is only 0.137·ln n (27 vs 25). That margin must pay for log_{5/3} ℓ ≈ 20.4 plus about 2–3 units of rounding in a, so ln n ≈ 22.5/0.137 ≈ 163.
2. ℓ ≈ 206·ln n ≈ 3.4×10^4 because the Chernoff exponent is quadratic in the density gap. The target 3/5 sits only 1/15 below Chingiz's 2/3 share, so η = D(3/5 ‖ 2/3) ≈ (9/4)(1/15)² ≈ 0.0097, and θ is barely below 1.

## 3. Where the loss sits

**General family.** Take P_U = λ^(tH − x_U)·μ^(f_U). Write u = 1/μ for Bella's multiplier and r = 1/(λμ) for Chingiz's. The danger weight on P_U is 1 − r.
- Exact Lemma-1 accounting requires u − 1 = 2(1 − r).
- The per-set initial weight is θ^H with θ = λ^t·μ = u^(t−1)·r^(−t).
- Minimising over u gives **u = 3(1 − t), r = 3t/2** (needs t < 2/3), and

  −ln θ = t·ln(3t/2) + (1 − t)·ln(3(1 − t)) = **D(t ‖ 2/3)**, the Kullback–Leibler divergence (Chernoff exponent).
- At t = 3/5 this gives u = 6/5, r = 9/10. **The paper's multipliers are already the optimum.** Any other legal pair has a smaller η. Only t and the crude a/binomial bookkeeping are tunable.

**Leading constants.**
- Chingiz: ω_C ≥ ln n/ln(1/t) − log_{1/t} ℓ − O(1), with ℓ ≈ 2·ln n/D(t ‖ 2/3).
- Bella: ω_B ≤ 2·ln n/ln 3 + O(1).
- First-order win iff t > 3^(−1/2) = 0.57735. So the usable window is t ∈ (0.5774, 0.6667).
- The margin in log_3 units is κ(t) = log_3(3t²) ∈ (0, log_3(4/3) = 0.262).
- The best asymptotic constant is t → 2/3, giving 1/ln(3/2) = 2.466 vs 1.820. But D(t ‖ 2/3) ≈ (9/4)(2/3 − t)² → 0, so ℓ blows up.

| t | u | r | η = D | 2/η | 1/ln(1/t) | κ |
|---|---|---|---|---|---|---|
| 0.58 | 1.26 | 0.870 | 0.01630 | 123 | 1.836 | 0.008 |
| **0.60** | **1.20** | **0.900** | **0.00971** | **206** | **1.958** | **0.070** |
| 0.62 | 1.14 | 0.930 | 0.00480 | 417 | 2.092 | 0.130 |
| 0.64 | 1.08 | 0.960 | 0.00158 | 1266 | 2.241 | 0.188 |
| 0.65 | 1.05 | 0.975 | 0.00062 | 3226 | 2.321 | 0.216 |
| 0.66 | 1.02 | 0.990 | 0.00010 | 20066 | 2.407 | 0.244 |

**Tuned thresholds** (`family.py` UP block; sufficient conditions). These use the least a with 3·C(n,a)·3^(−C(a,2)) ≤ 1/2, the least ℓ with u·C(n,ℓ)·θ^(C(ℓ,2)) ≤ 1/2, and C(n,k) ≤ n^k/k!. They reduce the paper-constant n_0 as follows:

| change | n_0 | ln n_0 |
|---|---|---|
| paper's constants, t = 3/5 | 10^70.9 | 163.2 |
| same t and weights, sharp a and ℓ! | 10^40.0 | 92.0 |
| t ≈ 0.65 | 10^18.9 | 43.4 |
| plus the free extra vertex | 10^17.9 | 41.2 |

The 10^40.0 row was spot-checked exactly in mpmath (`verify_t06.py`). The least a is 8–9 below the paper's ⌈2·log_3 n⌉ + 2, and each unit of a is worth about 7.3 in ln n. So most of the paper's excess is bookkeeping in a, not the method. The asymptotic constant improves from 1.958 to 2.32 at the optimal finite-n t.

**Cannot reach small n — necessary conditions** (`down2.py`). The check allows:
- any t ∈ [0.30, 2/3) and any legal multipliers (η ≤ D);
- the least a with C(n,a) < 3^(C(a,2));
- the least ℓ with C(n,ℓ) < e^(D·C(ℓ,2)), using exact log-binomials;
- Lemma 2 plus both free vertices.

Result: **no integer 8 ≤ n ≤ 2·10^4 passes**, and the log grid first passes at ln n = 37.2 (n ≈ 1.4×10^16, t = 0.645, a = 63). The whole family is useless below about 10^16.

**The elementary reason, worked at n = 100.**
1. The least a is 8, so Chingiz needs a K_8.
2. Lemma 2 plus two free vertices therefore needs R ≥ 6. That requires n/ℓ ≳ (1/t)^5 ≥ (3/2)^5 ≈ 7.6, so ℓ ≤ 13.
3. But C(100,13) < e^(78η) forces η > 0.47, i.e. t < 0.2. That contradicts (1/t)^5 ≤ 100/ℓ.

In general, each extracted vertex costs a factor 1/t ≥ 3/2 in set size, while Bella's certified bound grows like log_{√3} n. Since (3/2)² < 3 only barely, a win needs n^κ ≳ ℓ/t with κ ≤ 0.262. Meanwhile ℓ ≳ 2·ln(n/ℓ)/D(t ‖ 2/3) is in the thousands on the usable range of t, so n ≳ ℓ^(1/κ) ≥ 10^12 or more.

## 4. Transfer

**General (1:q).**
- The Q-base becomes q + 1, so Bella ≤ 2·ln n/ln(q+1).
- For P, u − 1 = q(1 − r), with optimum u = (q+1)(1−t), r = (q+1)t/q and η = D(t ‖ q/(q+1)).
- The usable window is (1/√(q+1), q/(q+1)). It is nonempty iff q² > q + 1, i.e. **q ≥ 2**.

So (1:2) is the smallest bias the method handles, and the tightest one. (1:q) for q ≥ 3 also follows asymptotically, which is weaker than CP's (1:3) result for all n ≥ 4.

**Unbiased game (#778 Q1, Erdős's conjecture; ties go to Bob).**
- q = 1: the window (0.707, 0.5) is empty.
- With t < 1/2, Bob's certificate gives ω ≥ ln n/ln(1/t) < log_2 n. In the hint's notation, with s = 1 − t, that is ln n/ln(1/(1−s)) < 1/ln 2, while the a-set bound is 2/ln 2.
- Alice, as Maker, can force (2 − o(1))·log_2 n (Beck, f_N(1,1) ∼ 2·log_2 N, as cited in CP25 §3).
- So the certificate is off by a factor of 2, and no tuning repairs it.
- Even an ideal extraction (2·log_{1/t} n, the random-graph value, with t ≤ 1/2) would only tie at first order. Q1 lives in lower-order terms, which this first-order method cannot see.

**(p:p+1) for p ≥ 2 (CP Conjecture 17).** Chingiz's share is (p+1)/(2p+1), so t < (p+1)/(2p+1) and his certified constant is at most 1/ln((2p+1)/(p+1)). Bella's p edges per turn compound on sets containing several of them, which breaks the linear 2:1 exchange.

| constant (coefficient of ln n) | p = 2 | p = 3 | p = 4 | p → ∞ |
|---|---|---|---|---|
| Chingiz certified (max) | 1.958 | 1.787 | 1.701 | 1.443 |
| Bella, Beck biased Erdős–Selfridge certificate, 2p/ln(p+2) | 2.885 | — | — | — |
| Bella, random-graph benchmark, 2/ln((2p+1)/p) | 2.183 | — | — | — |
| Bella as Maker can force, p/ln(p+2) (Gebauer, as cited in CP25) | 1.443 | 1.864 | 2.232 | — |

- **p ≥ 3: impossible in principle.** Bella can force more than Chingiz can certify, and the gap widens with p.
- **p = 2:** it would need a Bella certificate below her random-play clique number. Even the random benchmark (2.183) beats Chingiz's 1.958.

The method does not touch Conjecture 17 beyond p = 1.

## 5. Citation check

**[2] "Malekshahian and Spiro proved the corresponding asymptotic result for bias 1:4" — ACCURATE as cited.**
- The paper cites arXiv:2410.18304**v2** (2026). v2 was revised 2026-05-05 and accepted at J. Graph Theory.
- v2 Theorem 3 at p = 1 gives q ≥ 4. The text states: "In particular, for all sufficiently large n, the game Clique(1,4)(n) is a Player 2 win." Corollary 14 (q ≥ 3p + 1) gives the same at p = 1.
- v2 says this refinement came from a referee after submission.
- The live-page comment ("15:1 (14:1 with improved Ramsey bound)") describes **v1** (Oct 2024). v1 Theorem 3 reads "q+1 > 3.999^(2p) … Clique(1,15)", via Campos–Griffiths–Morris–Sahasrabudhe. A base-3.8 Ramsey bound gives 3.8² = 14.44, hence q ≥ 14.
- CP25's "(Notice that in [11], it is proved with q = 15)" also refers to v1, since CP25 v2 (2025) predates MS v2.
- **The comment is stale, not the paper.**

**[3] Cambie–Provoost — understated.** The paper files CP under "the corresponding asymptotic result … for bias 1:3". CP Theorem 8 proves (1:3) for **every n ≥ 4** (Theorem 18 for even n, Theorem 19 for odd n). The paper also does not mention that its Theorem 1 is CP Conjecture 17 at p = 1.

**Guy 1983 / Erdős attribution.** Consistent with MS and CP.

**Provenance (GPT-5.6 Pro).** Irrelevant to correctness.
