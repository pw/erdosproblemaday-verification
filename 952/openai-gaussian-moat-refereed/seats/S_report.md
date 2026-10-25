# Seat S report: printed §5 (Lemma 5.1, Theorem 5.2) and printed §6 (§6.1–§6.4, Lemma 6.1, Prop 6.2)

Paper: OpenAI, "Bounded-Step Walks on Gaussian Primes" (26 Sep 2026). I read `coverage-transfer.tex` and `schedule.tex`
line by line against `paper.txt`, together with `preliminaries.tex`, `geometry.tex` and `information.tex` for what §5–6
consume and what consumes them. Printed numbering is used throughout: (5.1)–(5.9) and (6.1)–(6.17). Scripts and outputs are
in `seats/S_work/`, each run under `ulimit -v 4000000; timeout 900`.

## 0. Bottom line

I tried to refute §5 and §6 and could not.

- **Lemma 5.1 and Theorem 5.2** hold as stated. I re-derived every inequality, including the Chernoff constant, the
  averaging over deficient coordinates, and the strictness of the final contradiction.
- **The §6 schedule** holds:
  - Lemma 6.1 and the band arithmetic;
  - the iteration (6.3) and its preservation;
  - (6.4) and (6.5);
  - the checkpoint ladder (6.6)–(6.11);
  - every invocation of Theorem 5.2 inside Prop 6.2, i.e. every i < J and the base case at i = J.
- **The quantifier order** D → (e₀, a₀, l₀) → g₀ → c₀ → B → M → (schedule, batches, J, ladder) → walk → exact start
  is respected. No "sufficiently large M" depends on the walk, the batch, the exact start, i, or a constant fixed later.
  §1 gives the full order.
- **Seat I's conditional imports.** All five statements that seat I's §7–8 verdict depends on hold in exactly the form
  §7–8 use them. §2 gives the row-by-row ruling.
- **Objections.** I raise only EXPOSITION items (§5 below). None is GAP or FATAL.
- **The inherited helper script was wrong in a reassuring-for-a-refuter direction.** `checks3.py` "found" (5.4)/(6.16)
  budget failures and a band failure at every M. These are 30-digit cancellation artefacts: it subtracted r_i log T −
  r_{i+1} log T with log T ≈ 10^{2M}. I rewrote it (`S_params.py`) to take that difference symbolically as 2β_i log T.
  With that fix every printed inequality holds from M = 84 (g₀ = 10⁻³). Four negative controls each trip the intended
  check.

## 1. Order of quantifiers (written out, then checked against every use)

| # | Object | Depends on | Where fixed |
|---|---|---|---|
| 1 | D ≥ 1 | — | §6.1 |
| 2 | β₀ = 1/200, e₀ = β₀/50 = 10⁻⁴ | absolute | §6.1 |
| 3 | a₀ (any a₀ < 1/2; a₀ = 1/4 works) | absolute (needs k_T L_* / T → 1/2, (3.1)) | §6.2 |
| 4 | l₀ with 2^{−l₀} < e₀/3 (l₀ = 15) | e₀ only, so absolute | §6.2 |
| 5 | g₀ < 10⁻² with 2C_D g₀ + 8g₀ < 2e₀/3 | D, through the constant of Lemma 4.3. That constant is independent of g, U, T (seat G, item G1, agrees). | §6.2 |
| 6 | c₀ < a₀ g₀^{2(l₀+1)} | a₀, g₀, l₀ | §6.2, (6.4) |
| 7 | C (k_T log 2T ≤ CT for T ≥ T₀) | absolute | §6.2, (6.5) |
| 8 | B > max(2, 1 + C/(e₀c₀)) | c₀, e₀, C | §6.2, (6.5) |
| 9 | (§7) K₀, c₁ = β₀c₀/(12K₀), K_D | absolute / c₀ / D | §7 |
| 10 | M ≥ M₀(D, g₀, l₀, a₀, c₀, B, C_D) | all of the above | everywhere "sufficiently large M" |
| 11 | X_m, windows, batches T = B^j, T₊, N = ⌈T₊^{10}⌉, g₁ = e^{−M³}, g₂ = e^{−100M^{20}}, the schedule | B, M | §6.1 |
| 12 | Per batch: q_T, A_i(T), J(T), β_i, r_i, τ_i, δ_i, η_i (absolute sequences cut at J), s_i, n_i | T, M | §6.2–6.4 |
| 13 | The walk; then exact starts a ≥ 0 | after everything | §6, §7 |

Every "sufficiently large M" in §6 resolves to one of the following:

- (i) The regime of Lemma 4.3 (q ≤ k_T and g⁵U/log T ≥ Λ_D) over all (U, g, T) used. The minimum over all tuples is
  ≥ exp(0.05·10^M − 500M^{20} − O(M)). This depends on D only.
- (ii) Lemma 6.1, which depends on g₀ through the number of operations.
- (iii) Explicit inequalities in M alone. They hold uniformly because log T ∈ [10^M, 1.05·100^M] for every batch.
- (iv) T ≥ T₀ for (3.1).

None of these mentions the walk, an exact start, i, or a batch beyond that range. In particular:

- c₀ is independent of B and M.
- B is chosen after c₀ and before M.
- The only threshold that involves B is "each window contains ≥ 2 batches" (0.05·X_{⌈M/2⌉} > 2 log B). It is legitimate
  because B precedes M.

## 2. The five §6 statements imported by §7–§8 (seat I's table), adjudicated

| Row | Form used in §7–§8 | Ruling |
|---|---|---|
| (6.4) at A₀(T) | From time 0: f_{z_{A₀}}(q_T) ≥ (1−e₀) q_T L_* and q_T L_* ≥ c₀T. Here f averages over uniform q_T-subsets of B_T with fair signs. | **HOLDS.** See note 2.1. |
| (6.5) | Σ_{used T'<T} k_{T'} log(2T') ≤ e₀c₀T for every used T. | **HOLDS.** See note 2.2. |
| (6.9) at i = 0 | H(z_{t_*} − z_{A₀}) ≤ C_D T^{1/4}, unconditional from time 0, with t_* counted as a checkpoint. | **HOLDS.** See note 2.3. |
| Prop 6.2 at i = 0 | For every exact start a at A₀(T), at most a fraction η₀ = 1/100 of the 2k_T signed primes fail (τ₀, β₀) = (1/4, 1/200) coverage. This must hold for every batch at once, with an M-threshold uniform over walks. | **HOLDS.** See note 2.4. |
| (6.2) | TV(L(t_*), L(t_*+a)) ≤ T₊^{−9} for 0 ≤ a ≤ T₊, both from an exact start at A₀(T) and from time 0. | **HOLDS.** See note 2.5. |

**2.1 (6.4).**
- A₀(T) lies in the middle band of window m, strictly after the top-band recording checkpoint, so it is a "later
  checkpoint" in the sense of (6.4).
- Preservation runs through Lemma 6.1 and Lemma 3.1 at the recording scale V. The loss is ≤ (4g₀V + O_D(1))/(V/2) =
  8g₀ + o(1).
- The iteration is uniform over initial laws, and time 0 is a deterministic start.
- q_T ≤ a₀T/L_* ≤ k_T, so the q_T-subsets exist. The law of C_T is exactly the law in f's definition (printed §4.3).
- V > a₀ g₀^{2(l₀+1)} T, because the first top-band scale ≤ a₀T exceeds g₀²a₀T; it cannot be the band's top edge, since
  log T ≤ 1.05X_m < 1.3X_m. Hence q_T L_* ≥ c₀T.

**2.2 (6.5).**
- Every used T' satisfies log T' ≥ X_{⌈M/2⌉}, so k_{T'} log 2T' ≤ CT'.
- The used batches are a subsequence of B^j, so the sum is ≤ CT/(B−1) ≤ e₀c₀T by item 8.
- §7 bounds log|alphabet(O)| by Σ q_{T'} log 2T' ≤ Σ k_{T'} log 2T' over exactly this set (all used batches below T,
  across all windows).
- Real-prime check: C ≈ 0.51 for T ≤ 10⁷.

**2.3 (6.9) at i = 0.**
- The definition reads "A checkpoint is a stage just before a specified transition, or the terminal stage."
- S₀ includes N − 1, and the support D₀ does not depend on the start. So the unconditional entropy is
  ≤ log|D₀| ≤ 4g₁T^{1/4} + O_D(1), which is sharper than printed.

**2.4 Prop 6.2 at i = 0.**
- All thresholds in the base case and the induction step are of types (i)–(iv) in §1, so they are uniform over walks,
  starts, i and batches.
- For each M there are finitely many batches, each above the same threshold, so "every batch at once" is immediate.
- "Fraction" means equal weight on the 2k_T signed primes, which is exactly what §7's count E|bad ∩ C_T| ≤ η₀q uses.

**2.5 (6.2).**
- t_* = t̃ + U_N, with U_N uniform on {0, …, N−1} and independent of everything before it.
- TV(U_N, U_N + a) = a/N ≤ T₊/T₊^{10}. Mixing over t̃ for any start preserves the bound.
- §7 and §8 apply it to deterministic functions of the time (hit events; block/residue-vector pairs), and TV contracts
  under such maps.

Seat I's verdict on §7–8 is therefore unconditional with respect to §6.

## 3. Printed §5

### Lemma 5.1. HOLDS.

For each fixed S: H(F_S(Y)) − H(𝓗) ≤ H(F_S(Y) | 𝓗) ≤ Σ_{c∈S} H(φ_c(Y) | 𝓗).

Averaging over S uses P(c ∈ S) = (s/k)·(1/2) = s/(2k), so E_S Σ_{c∈S} u_c = s·av_c u_c. Also av_c log p_c = L̄. This
gives (5.1).

No independence of Y and 𝓗 is used, as claimed. Exact check (`S_lemma51.py`) on 10 split primes in [101, 202], with
Y spread over up to 120 lattice points and data 𝓗 correlated with Y in three ways, s ∈ {1, 2, 3}, 120 laws:
- max[E_S H(F_S Y) − H(𝓗) − s·av H(φ|𝓗)] = −1.08 ≤ 0;
- max[(5.1) LHS − (ε+κ)L̄] = −0.78 ≤ 0;
- **negative control**: dropping the −H(𝓗) term gives +2.46 > 0. So the shared-cost term is load-bearing, and the test
  can fail.

### Theorem 5.2. HOLDS.

**Existence of K_c.** "Deficient" means #{u : P < τ/p} ≥ p^{1−β}. That count is an integer, so it is ≥ ⌈p^{1−β}⌉ = u_p.

**(5.8).**
- E[count at x = φ_c(Y)] = n·P(φ_c(Z) ∈ K_c) < nτu_p/p, because (Y, h_ℓ) has the law of (Y, h₁) for each ℓ.
- Markov then gives P(in list) ≥ δ/(τ+δ) ≥ δ, using τ + δ ≤ 1.
- As the paper says, only the one-trial marginal is used here.

**Small list (5.9).**
- Σ_x |(K−x) ∩ E| = u_p|E|. So fewer than |E|/δ candidates x have overlap > δu_p (the set is empty, or the inequality
  is strict).
- Every other x has hit probability ≥ τ'(1−δ)u_p/p ≥ (τ+2δ)u_p/p. The identity (τ+4δ)(1−δ) − (τ+2δ) = δ(2−τ−4δ) is
  ≥ 1.5625δ on the allowed range.
- Stochastic domination by Bin(n, λ) holds because the trials are i.i.d. given A = a.
- The inline Chernoff proof is correct: with t = −log(1−v), the exponent is −nλ[v + (1−v)log(1−v)] ≤ −nλv²/2. With
  v = δ/(τ+2δ) one gets nλv²/2 = nδ²(u_p/p)/(2(τ+2δ)) ≥ δ²np^{−β}/2.
- A union bound over ≤ p candidates and (5.5) give |L| < p^{1−β'}/δ < p^{1−β'/2} with conditional probability
  ≥ 1 − δ/100.
- The citation [Lugosi, Ex. 8, p. 13] is not load-bearing, because the bound is proved inline. I did not check that
  exercise number.

**Averaging.**
- Fix a. For each a, uncovered coordinates number ≤ η'·2k.
- So, averaged over the θ·2k deficient ones, P(c uncovered at A) ≤ η'/θ < η'/η ≤ δ/100.
- Then ā ≥ δ − δ/100 − δ/100 ≥ δ/2.

**Lemma 3.3** applies with b = p^{1−β'/2} (1 ≤ b ≤ p; a non-integer b is fine). Jensen gives av h(a_c) ≤ h(ā), and
h(ā) ≤ ā log(e/ā) ≤ ā log(2e/δ). With log p_c ≥ log T and (5.6), the deficient mean is ≥ (ā β'/4) log T ≥ (δβ'/8) log T.

**Contradiction.** The overall mean is ≥ θ(δβ'/8) log T, which is **strictly** > η(δβ'/8) log T ≥ (ηδβ'/16) L̄, using
θ > η and L̄ ≤ log 2T ≤ 2 log T. This contradicts (5.1) and (5.4).

**Numerical checks.**
- Inner inequalities (`checks1.py`, re-run): min[(τ+4δ)(1−δ) − (τ+2δ)]/δ = 1.5626. v + (1−v)log(1−v) − v²/2 ≥ 0.
  No exact-binomial lower-tail violation of the stated bound in 3000 random cases. Σ_x|(K−x)∩E| = |K||E| in 500/500
  cases. h(u) ≤ u log(e/u).
- Mechanism check of (5.9) (`S_list.py`, FFT, p = 4001, n from (5.5) = 8.84·10⁶, β' = 0.25):
  - with independent trials, the list lay inside the exceptional-candidate set in 40/40 runs (it was in fact empty);
  - **negative control**, all n trials equal (dependent): the list had ≈ p − u_p ≈ 3937 elements and lay outside the
    exceptional set in 40/40 runs.
  - So conditional independence given A = a is load-bearing, and the walk application supplies it ("Conditional on this
    exact time A, repeat … independently").
  - Caveat: at testable p, (5.5b) cannot hold (it needs p^{β'/2} > 64), so this tests the mechanism, not the printed
    constants. The constants are checked in §4.

## 4. Printed §6

### Lemma 6.1. HOLDS.

**Scales and shifts.** Scales are logarithms of time lengths: a transition at U shifts time by ≤ ⌊e^{gU}⌋. So
S_V = N − 1 + Σ ⌊e^{g_U U}⌋ is deterministic and bounds the advance from every start.

**Band domination** (`S_params.py`, all ordered pairs of bands, all windows):
- Within a band, later g_U U = g·g^{2j}V ≤ gV.
- The scale drops between bands are e^{0.5X_m} (top→middle), e^{0.1X_m} (middle→bottom), and e^{0.037X_m}
  (bottom m → top m−1; 0.05 − 1.3/100 = 0.037).
- Each drop beats the parameter ratio ≤ e^{100M^{20}}.
- Checked from M = 34 (fails at M = 30).

**log(1+S_V) ≤ 2gV.**
- min log(gV) ≥ 0.05·10^M − 100M^{20}, which beats log(log N + log #ops + log 2) with log N = 10.5·100^M.
- Checked from M = 34 (fails at M = 30).

**Smoothing (6.2).** TV(U_N, U_N + a) = a/N. Mixtures preserve this bound.

### §6.2 (6.3)–(6.5). HOLD.

**Exact chaining.** The transition at U' = g²U has input size ⌊U'/L_*⌋ = ⌊g²U/L_*⌋, which equals the previous output b
exactly.

**Iteration and preservation.**
- d_{j+1} ≤ d_j/2 + C_D g gives d_l ≤ 2^{−l} + 2C_D g.
- Preservation costs 8g + o(1).
- **This requires Lemma 4.3's error constant to be independent of g.** It is: the g-proportional losses are
  log A/(rL_*) ≥ 1 − 10g − o(g), b/r = O(g), and 4 log(n+1)/((q−b)L_*) ≈ 4g. All others are o(g). This matches seat G's
  item G1.

**Top-band placement.**
- l₀ + 1 steps below a₀T stay above 0.8X_m once 0.2X_m > log(1/a₀) + 2(l₀+2)log(1/g₀).
- The top band contains a scale ≤ a₀T, since 1.3X_m > 1.05X_m.

### §6.3 (6.6)–(6.11). HOLD.

**Recursions and closed forms.** Checked exactly in rationals for i < 1500 (`S_recursions.py`):
- τ_i = 3/8 − 2^{−i−3};
- η_i = 100^{−(i+1)} 2^{−i(i−1)/2−6i};
- r_i = 1/4 − 4β₀(1 − 2^{−i}) ∈ (0.23, 0.25].

A deliberately wrong τ closed form is rejected 50/50.

**J.** J is the least index with β_J log T ≤ M^{20}. J ≥ 1 once β₀·10^M > M^{20} (M = 34 suffices; M = 30 fails). Minimality gives
M^{20}/2 < β_J log T. Observed max J = 423, 436 and 461 at M = 84, 86 and 90, against (log₂ 100)·M ≈ 6.64M; so J = O(M).

**A_i in the middle band.**
- r_i log T ∈ (0.23X_m, 0.2625X_m], strictly inside [0.20X_m + 2M³, 0.30X_m].
- So the first operation with U ≤ T^{r_i} is a middle-band operation with log U ∈ (r_i log T − 2M³, r_i log T].

**(6.8)/(6.9).** Lemma 6.1 gives log|D_i| ≤ 2 log(1 + S_i) + O_D(1) ≤ 4g₁T^{r_i} + O_D(1) ≤ C_D T^{r_i}. The support
does not depend on the start.

**(6.10).**
- ⌈M³⌉ iterations at g₁ starting at A_i give deficit ≤ 2^{−⌈M³⌉} + (2C_D + 8)e^{−M³} ≤ e^{−cM³} (any c < log 2).
- They use 2M³(⌈M³⌉+1) of log-scale, which fits in 2β_i log T > 2M^{20}.
- log(s_i L_*) ≥ r_i log T − 2M³(⌈M³⌉+1) − log 2.
- The start q ≤ T^{1/4}/L_* ≤ k_T.
- s_i depends on the batch and the schedule only.

**(6.11).**
- Bottom band: ⌈200M^{20}⌉ steps of 200M^{20} log-scale fit in the bottom band (width 0.05X_m) once M ≥ 84. This is the
  binding numerical constraint.
- Deficit: 2^{−⌈200M^{20}⌉} + (2C_D + 8)e^{−100M^{20}} ≤ e^{−90M^{20}}.
- Concavity of f with f(0) = 0 gives f(1) ≥ f(s)/s.

### §6.4 Prop 6.2. HOLDS, including every invocation of Theorem 5.2.

**Base (i = J).**
- A failing prime has TV ≥ (1−τ_J)p^{−β_J} ≥ (5/8)e^{−M^{20}}·2^{−β_J}.
- Pinsker gives a deficit ≥ 2TV² for each failing prime.
- So the failing fraction is ≤ e^{−90M^{20}}L_*/(2TV²) = exp(−88M^{20} + O(M)), which is < η_J ≥ exp(−O(M²)).

**Step (i < J).** Hypotheses of Theorem 5.2 with (τ, δ, τ', β, β', η, η') = (τ_i, δ_i, τ_{i+1}, β_i, β_{i+1}, η_i, η_{i+1}):

| Hypothesis | Verification | Status |
|---|---|---|
| τ ≤ 3/8 | τ_i < 3/8 | ✓ |
| δ ≤ 1/64 | δ₀ = 1/64 | ✓ |
| τ' = τ + 4δ | by (6.12) | ✓ |
| β' ≤ β | β_{i+1} = β_i/2 | ✓ |
| 0 < η ≤ 1 | — | ✓ |
| Coverage at every a in supp A | induction hypothesis at i+1, which is stated for **all** exact starts | ✓ |
| A, Y = y(A), h_ℓ i.i.d. ν_A given A | Markov property of the schedule ("fresh conditional on the current exact walk time") | ✓ |
| Z = Y + h₁ has the terminal law from A_i = a | Markov property | ✓ |
| (5.3) joint entropy | (6.10) with ε_i = e^{−cM³}, s = s_i ∈ [1, k_T] | ✓ |
| (5.3) data cost | H(𝓗) ≤ n_i log\|D_{i+1}\|, support bound, no independence needed. log κ_i ≤ log C_D + 2log 2 − (4/5)β_i log T + 2M³(⌈M³⌉+1) ≤ −M³ | ✓ |
| (5.4) η' ≤ ηδ/100 | equality by (6.13) | ✓ |
| (5.4) ε + κ ≤ ηδβ'/16 | e^{−cM³} vs exp(−O(M²)) | ✓ |
| (5.5a) | δ_i²n_i p^{−β_i}/2 ≥ exp(β_i log T/5 − O(M)) ≫ log(100p/δ_i) | ✓ |
| (5.5b) | 2^{i+6} < e^{β_{i+1} log T/2}, with β_{i+1} log T > M^{20}/2 | ✓ |
| (5.6) | log(2e/δ_i) = O(M) ≤ M^{20}/8 | ✓ |

All of these were checked with explicit stand-ins for every hidden constant (`S_params.py`), at seven values of log T
across each window [X_m, 1.05X_m], every window m ∈ [⌈M/2⌉, M], and every i ≤ J:

| Setting | Result |
|---|---|
| g₀ = 10⁻³, l₀ = 15, a₀ = 1/4, C_{4.3} = 100, C_D = 10³ | **no failures at M = 84, 86, 90**. M ≤ 80 fails only the bottom-band capacity (and, at M ≤ 34, the J ≥ 1 / Lemma 4.3-regime / Lemma 6.1 checks). |
| Heavier constants C_{4.3} = 10⁶, C_D = 10⁹, g₀ = 10⁻⁶ | no failures at M = 90 and M = 120 |
| NC1: n_i = ⌈T^{β_i}⌉ (drop the 6/5) | fails (5.5a) only |
| NC2: r_i − r_{i+1} = β_i (gap halved) | fails (5.4) and (6.16) |
| NC3: g₁ = e^{−M} | fails (5.4) |
| NC4: g₂ = e^{−M³} | fails (6.11) (bottom deficit ≤ e^{−90M^{20}}) |

So the checks can fail, and the printed choices (6/5, gap 2β_i, M³, 100M^{20}) are each load-bearing.

## 5. Objections (classified)

All five are EXPOSITION. None propagates.

**S1 (EXPOSITION), §6.1 and §6.2.** The paper states: *"This completes the fixed-constant choices in the order D, e₀,
then l₀, g₀, c₀, then B, and finally M."*
- The list omits a₀, which is introduced mid-§6.2 ("Choose a small absolute a₀ > 0"), and the PNT constant C of (6.5).
  Both are absolute, so the order is unaffected.
- l₀ depends on e₀ alone (l₀ = 15), not on D as §6.1 suggests ("depending only on D, e₀").
- A complete statement would be D, (e₀, a₀, l₀, C absolute), g₀(D), c₀(a₀, g₀, l₀), B(c₀), M. The table in §1 is that
  statement.

**S2 (EXPOSITION), §6.2.** The paper states: *"In particular g^C U/log T → ∞ for every fixed C > 0."*
- Lemma 4.3 is phrased for an "asymptotic family". §6 applies it to many (U, g, T) tuples for each M, with g → 0 in the
  middle and bottom bands.
- What is needed is the threshold form that seat G extracted: g⁵U ≥ Λ_D log T ⇒ error ≤ C_D g with C_D independent
  of g.
- The three displayed uniform bounds do give min over tuples of g⁵U/log T ≥ exp(0.05·10^M − 500M^{20} − O(M)) → ∞.
  Checked (with a margin of e^{50}) from M = 36; fails at M = 34.
- So the application is valid, but this should be said explicitly, together with the fact that the O_D(g) constant does
  not depend on g. Choosing g₀ in item 5 relies on that fact.

**S3 (EXPOSITION), (6.8).** The paper states: *"Since the scale at A_i is at most T^{r_i}, lattice-point counting gives
log|D_i| ≤ C_D T^{r_i}."*
- The scale alone gives nothing. The step goes through Lemma 6.1 (log(1+S_i) ≤ 2g₁V ≤ 2T^{r_i}) and then lattice
  counting, which gives the sharper 4g₁T^{r_i} + O_D(1).
- Correct as stated, but the dependence on Lemma 6.1 is left implicit.

**S4 (EXPOSITION), (6.17).** The paper states: *"E_{p,π}[log p − H(Y mod π | 𝓗)] ≤ (e^{−cM³} + κ_i)L_*."*
- The notation E_{p,π} is undefined; it means the equal-weight average over signed primes, as in (5.1).
- The display is never used: Theorem 5.2 calls Lemma 5.1 internally from (5.3).

**S5 (EXPOSITION), Lemma 6.1 proof.** The paper states: *"The number of operations is O_{g₀}(X_M) = exp(O_{g₀}(M))."*
The g₀-dependence is a multiplicative constant, so the count is exp(O(M)). Harmless notation.

**Not objections, but worth recording:**
- The margin in (6.7)'s 0.23 < r_i is only 0.02·2^{−i} (about 10^{−152} at i ≈ 500). The band containment needs only
  r_i log T > 0.20X_m + 2M³, which has margin ≈ 0.03X_m.
- The paper's ladder is heavier than necessary. Seat L reports that the Lean reaches τ₀ = 1/4, η₀ = 1/100 at A₀ with a
  constant-fraction base and a single transfer step. That is a statement about economy, not correctness.

## 6. Seat L's finding: the Lean does not follow the printed §6.3–6.4 ladder

**No gap was found in the printed ladder**, so nothing here needs to be rescued by the Lean's alternative route.

For the record, I read `EntropyBand.lean:240`:
- `CoverageDerivation` is a general inductive ladder (`base | step`).
- Its `step` constructor carries Theorem 5.2's hypotheses in generalized form: τ ≤ 3/8, δ ≤ 1/64, next level at τ + 4δ,
  conditional i.i.d. trials, and a data-cost-plus-deficit gap.
- So the mechanism of Theorem 5.2 is formalized, through `backward_coverage_step` and `lowResidues_backward`. Only the
  printed instantiation (β_i, r_i, τ_i, η_i, J = O(M)) is not. Per seat L, `one_step_coverage` uses one step.

The Lean's step requires η' + ε ≤ ηδ/2, where ε is the union-bound error. That is a stronger requirement than the
paper's. The paper needs only the union-bound error ≤ δ/100 per covered coordinate, because it averages over deficient
coordinates. The difference is conservative and consistent with §5.

If a gap had existed only in §6.3–6.4, it would be an exposition defect: the Lean's route (if the kernel replay is
green) proves the same §7 input at A₀.

## 7. Scripts (`seats/S_work/`)

| Script | Content | Result |
|---|---|---|
| `S_recursions.py` | Exact rational check of (6.6), (6.12), (6.13) closed forms and ranges, i < 1500, plus a negative control | 0 mismatches; control 50/50 |
| `S_params.py` / `S_params.out` | Precision-safe check of every explicit inequality in Lemma 6.1, (6.4), (6.7), (6.10), (6.11), (6.14)–(6.16), (5.4)–(5.6) at every i ≤ J, all windows, 7 points per window. Full output: M = 84, 86, 90 clean. | M = 84, 86, 90 clean |
| `S_params_nc.py`, `S_params_nc2.py` / `.out` | Heavier hidden constants plus four negative controls (M = 90; two independent runs agree) | baseline clean; each control trips exactly its intended check; heavy constants clean at M = 90 and 120 |
| `S_lemma51.py` | Exact Lemma 5.1 test in Z[i]/(π), with a negative control | as in §3 |
| `S_list.py` | FFT Monte Carlo of the (5.9) mechanism, with a dependent-trials negative control | as in §3 |
| `S_batches.py` | Real-prime check of a₀ (min k_T L_*/T = 0.48) and C (max k_T log 2T/T = 0.516), T ≤ 10⁷, plus the geometric sum for B = 3 | as stated |
| `checks1.py`, `checks2.py` (inherited) | Re-run | correct |
| `checks3.py` (inherited) | **Wrong**: 30-digit cancellation produced false (5.4)/(6.16)/band failures. Superseded by `S_params.py`. Its run was stopped at the 15-min background limit after M = 120. | — |

Scope of this verdict: printed §5 and §6, and the five §6 statements imported by §7–§8.

VERDICT: HOLDS AS READ
