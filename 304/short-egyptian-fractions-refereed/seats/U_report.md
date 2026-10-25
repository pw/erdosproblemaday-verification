# Seat U: hostile referee report on the upper bound of Theorem 1.1 (N(b) ≤ c2 log log b)

Scope: printed §2 (Prop 2.1, Lemma 2.2, Lemma 2.3, proof of Thm 1.1), §3 (Lemma 3.1, (3.1)–(3.13)),
§4 (Lemmas 4.1–4.5, (4.1)–(4.15), §4.4 selection proof), §5 (proof of Prop 2.1, (5.1)–(5.10)); pp. 5–22.
I read the LaTeX source line by line and checked it against paper.txt for printed numbering. Every inequality
in the chain was re-derived by hand. The explicit numerical claims were then checked by script
(`/tmp/oaimath/025/seats/U_checks/check{1,2,3}.py`, `negctl.py`; outputs reproduced below).

Context worth knowing: Bloom–van Doorn (§6 of their note) say they "have not yet read those sections [3–5] in
detail". They also point out that the paper's §8 gives an independent, more elementary proof of the upper bound.
So §§3–5 are logically redundant for Theorem 1.1, and no human expert has vouched for them. I treated them as
unverified. OpenAI's Lean development follows this same §2–5 route (DivisorMoments, Holder, MomentRecurrence,
RecurrenceUnrolling, ... feeding `Main.lean: main_upper_expansions`). The kernel replay is the coordinator's
job, not mine.

---

## 1. Order of constants and uniformity (brief item 1)

The fixing order, as actually used:

1. (4.2): K=100, R=1000, D0=10^5, η=10^-4, D_M=(2R+2)(K+2)=204204, D_X=D_M+2=204206, D_C=4D_X=816824.
   These are numbers and depend on nothing.
2. §5 opening: K_d=3D_X/η (≈6.13·10^9), D_*=2D_C+D_M+1, r ≥ max{2, 8K_d}, α=1−1/r. These depend only on step 1.
3. Thresholds:
   - Lemma 3.1 S0(D_*, r).
   - Lemma 4.2 (w large; absolute Erdős–Turán constant).
   - Lemma 4.3 with B=3D_C (A_B, δ_B, U large).
   - Lemma 4.5 (absolute).
   - The o(1) failure probabilities in §4.4 (depend on K_d and D0 only).
   - §5's "S sufficiently large" (depends on r, K_d, c_*=0.001).
4. B0 (terminal length constant) depends on η and D0. L = B0 + K_d.

Nothing chosen later feeds back into an earlier choice. C enters in three places only:
- the range e^{D_C S} ≤ C ≤ e^{2D_C S};
- Lemma 4.4, uniform in C through |Z| ∈ [e^{D_C S}, e^{(2D_C+K+2)S}];
- the shift bound N = C_j t ≤ CM < e^{D_* S}.

The random part of Lemma 4.1 (middle and terminal levels) uses Q=1 and never sees C. So the threshold of
Prop 2.1 is independent of C, as claimed.

Final length:
- 1 + ⌈log2(D_C S/log 2)⌉ greedy terms (Lemma 2.3), plus 2L log S (two members of G);
- Lemma 2.2 does not change the count.

So c2 is absolute (about 2(B0+K_d) ≈ 1.2·10^10), independent of a and b. **Holds.**

Observation, not an error: b0 is astronomically large. Lemma 4.3 with B=3D_C gives Q_B=2,450,473 and
δ_B=(10Q_B 2^{Q_B})^{-1} ≈ 10^{-737,673}. Lemma 4.4 needs e^{-0.8δ_B S} ≤ e^{-0.01m}, i.e. log S ≳ 10^{737,671}.
The recurrence (5.10) alone needs S ≳ 10^{32}. The theorem asserts only the existence of b0, so this is
harmless. But c2 being "absolute" here is an existence statement whose threshold has no numerical use.

## 2. §2: dense family to every numerator (brief item 2)

**Lemma 2.3 (greedy preparation).** The facts used are:
- z=⌈C/A⌉ ≤ C because A ≥ 1.
- C' ≤ C².
- 0 ≤ A' < A.
- z ≥ 2 because A/C < 1.
- The first crossing of T comes from a denominator below T (the start is b < T), so the result is < T².
- x − 1/⌈1/x⌉ ≤ x²/(1+x), x1 < 1/2, x_j ≤ 2^{-2^{j-1}}, and x_j ≥ 1/C_j > 1/T before stopping.

These give at most 1+⌈log2(log T/log 2)⌉ steps. Checked on 20,000 random (a, b, T) with b up to 10^30:
0 failures of the step bound, of 1 ≤ A ≤ a, of T ≤ C < T², of z ≥ 2, or of exact reconstruction.
Negative control: lowering the bound by 2 is violated 537 times, so the check can fail.

**Lemma 2.2 (removing repetitions).**
- The finiteness induction is correct: the smallest denominator is ≤ k/x.
- The identities 2/(2p) = 1/(p+1)+1/(p(p+1)) and 2/(2p+1) = 1/(p+1)+1/((p+1)(2p+1)) are correct.
- Total < 1 excludes a denominator of 1 and a double 2.
- The increases (p−1)² and 2p² are correct and positive.
- Termination holds because every list visited is distinct, by strictly increasing denominator sum.

Simulated on 5,000 random lists with forced repeats (sum < 1): 0 failures. Every run terminated with k
distinct denominators ≥ 2 and the same sum.

**Proof of Thm 1.1 (upper half).**
- A < b = e^S and M ≤ e^{D_M S}, so AM < e^{(D_M+1)S} < X = e^{(D_M+2)S}.
- g = ⌊X/(AM)⌋ ≥ 1 and n = gAM ∈ [X/2, X].
- Each element of H kills at most two of the n−1 splits u + (n−u), so at most 2|H| ≤ X/4 < X/2 − 1 ≤ n − 1
  splits are bad. A good split exists.
- n/(MC) = gA/C. Multiplying every denominator by g yields A/C with ≤ 2L log S terms.

Distinctness (brief item 2): multiplying by g is injective, so distinctness of each piece would survive. The
union of the two expansions with the greedy prefix may still collide, and Lemma 2.2 at total a/b < 1 removes
all collisions without changing the count. So length stays O(log S). The 1/8 exceptional proportion is more
than enough. **Holds.**

EXPOSITION (introduction, outline): "Adding their expansions and dividing by g represents A/C". The operation
is multiplying each denominator by g. The proof of Thm 1.1 says this correctly ("Multiplying every
denominator by the integer g").

## 3. §3: the uniform divisor moment, Lemma 3.1 (brief item 3)

This is the step I expected to break: a Shiu-type r-th moment in intervals of length Y ≥ X^{1/2} that can be
N^{o(1)} (N up to e^{DS}, Y possibly only exp(S/(4 log S))). That is well below Shiu's Y ≥ N^ε. It survives
because divisors are truncated at X ≤ Y² and the target is only exp(S^{1/4}), not polylog. I re-derived
every display.

- **(3.3).** Σ_{j≤J} C(L,j) ≤ q^{-J}(1+q)^L ≤ exp(BJ), with:
  - L = ⌊ES/log z⌋ (at most that many prime factors ≥ z, since n ≤ e^{ES});
  - J = v/log z;
  - q = v/(ES) ∈ (0,1);
  - qL ≤ J.

  Correct. Checked on 1,200 parameter sets: 0 failures, max log-gap −0.64. Negative control (B → 0.3B):
  720/720 violations, so the instrument can fail.
- **(3.4).** Small primes below S^{1/2} give at most (1+ES/log 2)^{S^{1/2}} exponent choices. Large primes
  give exp(2Bv/log S). The bound v ≥ S/(2 log S) turns both into ε_D(S)v with ε_D → 0. Correct.
- **Prefix inequality d_X(n) ≤ τ(d) d_X(n/d).** The map a ↦ (gcd(a,d), a/gcd(a,d)) is valid: for every prime,
  v_p(a/gcd(a,d)) = max(0, v_p(a)−v_p(d)) ≤ v_p(n/d). This holds for any d | n, coprime or not. Checked on
  3,000 random n ≤ 10^15 with random X and Y: 0 failures, including d ≤ √Y < dp, primes of d ≤ p, and primes
  of n/d ≥ p.
- **(3.5)–(3.7).**
  - (3.6) holds: e·Σp^{-s} with s = 1+1/log T, and ζ(s) ≤ 1+1/(s−1). Numerically to 10^7, the ratio is ≤ 0.414.
  - (3.7) holds, but the constant is mislabelled (EXPOSITION). The proof gives (1+log T)^{e·C_r}, while the
    display writes (log 2T)^{C_r}, reusing the symbol C_r from (3.5). It is harmless: only a polylog factor is
    used.
- **Case log p ≥ v^{15/16}, and n ≤ √Y.** (3.10) holds: e^{rBv^{1/16}} (log Y)^{O_r(1)} = exp(O(S^{1/16} log log S + log S)).
- **(3.11).** log d > ½ log Y − log p ≥ v/4 − v^{15/16} > v/5. Holds.
- **p < S^4 (Rankin with exponent 1/10), (3.12).** The prefix d is S^4-smooth. Σ_{d>e^{v/5}} 1/d ≤ e^{-v/50}·exp(O(S^{2/5})).
  The pointwise r-th power gives exp(rε_D v) = exp(o(v)). Holds.
- **Intermediate bands [t, 2t), (3.13).**
  - Q = v/t ≥ v^{1/16}, λ = log Q/(10t) < 1/4, so (3.5) applies with σ = 1−λ ≥ 3/4.
  - Σ_{ℓ≤e^{2t}} ℓ^{-1+λ} ≤ Q^{1/5}·e·log(1+2t).
  - λv/5 = Q log Q/50.
  - rB/log Q ≪ log log S/log S and Q^{1/5}log(2t)/(Q log Q) ≪ v^{-1/20}.
  - There are O(log S) bands.

  Holds.
- **Every n is in exactly one case**, and each case counts n through its unique prefix d using
  #{multiples of d in (N, N+Y]} ≤ 2Y/d (d ≤ √Y ≤ Y). No n is double-counted or missed.
  - The case split is log p ≥ v^{15/16}; p < S^4; 4 log S ≤ log p < v^{15/16}; n ≤ √Y.
  - The bound is uniform in N and in the shift. Thresholds depend only on (D, r).

EXPOSITION: "order its prime factors with multiplicity" does not say *nondecreasing*. The next sentence's
consequences ("all prime factors of d are at most p, and all those of n/d are at least p") require that order.

Citation: Erdős 1952 (JLMS 27) is cited for the method only; the lemma is proved in full, so the citation is
not load-bearing. Hildebrand–Tenenbaum is cited only for Rankin's trick, which is carried out explicitly.

Toy sanity check (not a test of the asymptotic statement, which no feasible computation reaches). X=10^6,
Y=10^3, N ≈ 10^12–10^13 including N = lcm(1..29), r=3: (1/Y)Σ d_X(N+h)^3 ≈ 3·10^4–10^5, against (log X)^7 ≈ 10^8.
Consistent with a polylog-size moment, far below exp(S^{1/4})-type slack.

**Lemma 3.1 holds.**

## 4. §4: divisors with small residues (brief item 4)

**Identity (4.1) / introduction display / (5.2) / (5.4).** Checked with exact rationals on 200,000 random
(M/t, t, Q, u):
- u/(MQ) = 1/((M/t)z) + (1/z)(h/(MQ)) with z = ⌈Qt/u⌉ and h = uz − Qt;
- the rescaled form (5.4) with C_{j+1} | C_j;
- h ≡ −Qt (mod u) and 0 ≤ h < u.

0 failures.

**Lemma 4.1 construction.**
- log M ≥ Km log S ≥ K(S − log S) > S.
- log M ≤ D0 log S + log 2 + (2R+1)m(K log S + log 2) ≤ D_M S, since (2R+1)K = 200100 < 204204.
- t ≤ e^{(K+1)S}, which is (4.6).
- The T_0 entries are distinct by unique factorization. This is used for the diagonal and for Z ≠ 0 in
  Lemma 4.4.
- (4.7) holds: the formula for d, d ≤ K_d log S, e^{(1−η)m} < X_d ≤ e^m, X_{j+1} ≥ √X_j, C_d = 1, and C_{j+1} | C_j.

**Lemma 4.2 (Erdős–Turán).**
- The discrepancy is O(e^{-4ηw} + (1+4ηw)e^{-3ηw}) = o(e^{-ηw}).
- {−Qt/u} = (u⌈Qt/u⌉ − Qt)/u.
- The rotation remark correctly handles the half-open endpoint.

The cited inequality (Erdős–Turán 1948) is the standard one with absolute constants, valid for finite lists
with multiplicity. **Holds.**

**Lemma 4.3 (reciprocal phase, van der Corput).**
- k = nearest integer to log|Z|/log U gives |Z|U^{-k-1} ∈ [U^{-3/2}, U^{-1/2}].
- There are k−2 differencings with L = ⌊U^{1/(10k)}⌋.
- g'' is an integral of f^{(k)} of constant sign, so (k!/2^{k+1})Λ ≤ |g''| ≤ k!Λ, and U^{-3/2} ≤ Λ ≤ U^{-2/5}.
- The second-derivative test (4.10) is sketched correctly (Kusmin–Landau on the β-separated pieces) and gives
  O_k(U^{4/5}).
- The recursion σ_j² ≪ L^{-1} + σ_{j+1} gives σ_0 ≪ U^{-1/(10k 2^{k-2})}.

Standard and correct. Toy numerics (U = 500, 2000, 8000; Z ∈ [U^4, U^6]): |Σ e(Z/n)|/U = 0.06, 0.04, 0.025,
decreasing.

**Lemma 4.4 (deterministic mean square).**
- The diagonal gives ≤ 2^{-m}.
- Off-diagonal pairs have Z = ℓC(t−t') with e^{D_C S} ≤ |Z| ≤ e^{(2D_C+K+2)S}, and U ∈ [e^{0.8S}, e^{D_X S}].
- U^4 ≤ e^{4D_X S} = e^{D_C S} ≤ |Z|. This is exactly why D_C = 4D_X.
- U^{3D_C} ≥ |Z| needs 0.4D_C ≥ K+2; true.
- The dyadic U's sum to O(X).

Uniform in C. **Holds.**

**Lemma 4.5 (random products).** This is the probabilistic heart. I checked the conditioning carefully.
- For a pair (I, J) with Hamming distance ≥ m/4 ≥ 2s, the 2s I-selected samples at differing coordinates are
  variables distinct from the J-selected ones. t_J and U_0 are functions of the exposed variables, and U_1, U_2
  are independent products of s fresh i.i.d. samples. Correct.
- gcd event: gcd(lU_0, u) ≤ l·gcd(U_0, u) and l ≤ u^{0.005}. Failure needs ≥ k_0 hits, where each sample hits
  with probability ≤ S/P ≤ S^{-(K-2)} (at most S primes ≥ S^K divide u ≤ e^S). The union bound gives
  ≤ S^{-(K-3)k_0} ≤ u^{-0.0768} ≤ u^{-0.05}.
- Fresh-product values ≤ u^{0.7575} < u^{0.8} ≤ q, so reduction mod q is injective. Atoms ≤ s!/P^s ≤ u^{-0.7252}.
  Orthogonality with gcd(c, q) = 1 and Cauchy–Schwarz gives √q·‖α‖‖β‖ ≤ u^{1/2−0.7} = u^{-0.2}.
- The Hamming tail P(Bin(m, ½) < m/4) ≤ e^{-m/16} was checked exactly for m = 4..3000: 0 failures.
- The other numerical constants (0.74V/(K log S) ≤ s, 2s ≤ m/4, 3e^{-0.05w} ≤ e^{-0.01w} for w ≥ 28) all check.

Monte Carlo sanity check of the mechanism (outside the lemma's range): subset products of 10–12 random primes
in [1000, 2000] modulo u ≈ 10^6–10^7, including u = 2^23. The mean |avg|² is 1.10–1.26 × 2^{-m}, i.e.
essentially diagonal.

**Holds**, including for composite u, prime powers and repeated samples, as the text says.

**§4.4 (simultaneous choice).**
- High levels: Markov plus a union over ℓ ≤ H gives X_j·e^{(10η−0.01)m} = X_j e^{-0.009m} exceptions.
  This is deterministic.
- Middle levels: w ≥ (1−η)m and 4η ≤ 0.005(1−η). The per-u failure probability is e^{-0.008999m}. Then
  E B_j ≤ X_j e^{-0.005m}, and P(B_j > X_j e^{-0.001m}) ≤ e^{-0.004m}. The union over d = O(log S) levels is o(1).
- Terminal: per-block failure is u^{-0.009}. R = 1000 independent blocks give u^{-5}, and Σ_{u>S^{D0}} u^{-5} = o(1).
- No independence across u or levels is needed. One realization serves everything.
- Lemma 4.2 with w = m (or w = log u) converts the Fourier bounds into ρ|T|/2 entries with h < ρu ≤ X_{j+1}
  (or h < u^{1−η}).

**Holds.**

## 5. §5: propagation of exceptional sets (brief item 5)

**Terminal level.**
- Binary: every bit 2^k ≤ u ≤ S^{D0} ≤ 2^a divides M. That is ≤ 1 + D0 log S/log 2 terms.
- Terminal reduction: log h ≤ (1−η) log u, so ≤ 1 + ⌈log S/(−log(1−η))⌉ steps.
- B0 is absolute.
- Denominators are ≥ 2 because the totals are < 1, which holds since u ≤ e^S < M, and X_0 < MC at high levels.

**Backward sets (5.3), (5.4).**
- Inheritance multiplies denominators by C_j/C_{j+1} (an integer).
- The residue step uses (5.4), verified above.
- The length bound (5.5) B0 log S + d − j follows by induction.

**Double count (5.6).**
- H_j ∩ [1, Y] ⊆ H_{j+1}.
- Each non-exceptional u ∈ H_j ∩ (Y, X] has ≥ ρ|I_j|/2 indices whose residue lies in [1, Y]. These residues
  lie in H_{j+1}, since 0 or a member of G_{j+1} would put u in G_j.
- For fixed (h, i) we have u | C_j t_i + h and u ≤ X, so the number of predecessors is ≤ d_X(C_j t_i + h).
- Indices are retained on both sides.

Correct.

**Lemma 3.1 hypotheses.**
- S/(2 log S) ≤ m < log X_j ≤ D_X S ≤ D_* S.
- √X ≤ Y = X^{1−η·m/log X} ≤ X.
- N = C_j t_i ≤ CM < e^{D_* S}.

All hold.

**Hölder (5.7) and recurrence (5.8).**
- |H_{j+1}|^α (Y e^{S^{1/4}})^{1/r} = Y δ^α e^{S^{1/4}/r}.
- Dividing by X, the factor 2/(ρ|I_j|)·|I_j|·Y/X = 2. The inherited term becomes ρδ_{j+1}.
- Hence δ_j ≤ ε + Aδ_{j+1}^α with A = e^{2S^{1/4}} and ε = e^{-c_* m}.

**Do the losses accumulate fatally?** No. Unrolling with (a+b)^α ≤ a^α + b^α gives
Σ_i A^{(1−α^i)/(1−α)} ε^{α^i}.
- The A-exponents are bounded by 1/(1−α) = r, a geometric sum, not linear in d.
- The Hölder loss α^i is bounded below by α^d ≥ e^{-2d/r} ≥ S^{-2K_d/r} ≥ S^{-1/4}, using r ≥ 8K_d.
- So δ_0 ≤ d·exp(2rS^{1/4} − c_* m S^{-1/4}). This tends to 0 because m S^{-1/4} ≍ S^{3/4}/log S.

The mechanism works only because ε = exp(−c_* S/log S) is tiny enough to survive being raised to the power
S^{-1/4}. That is exactly what (5.9) arranges.

I checked the unrolled bound against the worst-case iteration δ_j = min(1, ε + Aδ_{j+1}^α) for 20,000 random
(r, d, ε, A): 0 violations.

**Holds.**

## 6. Does anything assume what it should prove? (brief item 6)

No. Every external input is standard and is used within its hypotheses:
- Erdős–Turán (absolute constant, finite lists with multiplicity).
- van der Corput differencing and the second-derivative test (proved in the text).
- PNT or Chebyshev for P ≥ S^{K−1} (Selberg 1949 is more than is needed).
- Rankin's trick (carried out).
- Erdős's 1952 splitting (method only; proved in full).
- Takenouchi (reproved).

No lemma is invoked with a stronger uniformity than it proves:
- Lemma 3.1 is applied with fixed (D_*, r), uniformly in N and in subsets of the interval.
- Lemma 4.3 with fixed B = 3D_C.
- Lemma 4.5 uniformly in u, l, P.

## Findings

| # | Location | Quote / point | Class |
|---|---|---|---|
| 1 | §3, proof of Lemma 3.1, "A prefix of the prime factorization" | "order its prime factors with multiplicity": nondecreasing order is needed for the next sentence | EXPOSITION |
| 2 | (3.7) | "≪_r (log(2T))^{C_r}": the exponent is e·C_r, reusing the symbol C_r from (3.5); only a polylog is needed | EXPOSITION |
| 3 | §1 outline | "Adding their expansions and dividing by g represents A/C": the operation is multiplying denominators by g (the §2 proof states it correctly) | EXPOSITION |
| 4 | Lemma 4.3 with B = 3D_C feeding Lemma 4.4 | δ_B ≈ 10^{-737,673}, so S0 ≳ exp(10^{737,671}). Absolute and finite, but numerically meaningless; not claimed otherwise | (observation) |
| 5 | §§3–5 as a whole | logically redundant for Thm 1.1 (§8 also proves the upper bound, per Bloom–van Doorn §6) | (observation) |

No FATAL, GAP, or ERROR-NONFATAL item found in printed §§2–5, Lemma 2.2, or Lemma 2.3.

## Numerical check log (all scripts in U_checks/, run under `ulimit -v 4000000; timeout 600`)

```
identity checks ((4.1), (5.4), intro display, h = (-Qt) mod u), 200k random:  failures = 0
Lemma 2.3 greedy, 20k random (a, b, T), b ≤ 1e30:                              failures = 0
Lemma 2.2 Takenouchi, 5000 lists with forced repeats:                          failures = 0
x - 1/ceil(1/x) ≤ x²/(1+x), 100k:                                              failures = 0
(3.3) binomial bound, 1200 cases:                                              failures = 0 (max log-gap -0.639)
prefix inequality d_X(n) ≤ τ(d) d_X(n/d) and prime-side facts, 3000 n ≤ 1e15:  failures = 0
(3.6) Σ_{p≤T} 1/p ≤ e log(1+log T), T ≤ 1e7:                                   failures = 0 (max ratio 0.414)
Hamming tail P(Bin(m,½) < m/4) ≤ e^{-m/16}, m = 4..3000:                       failures = 0
(5.8)→(5.10) unrolling vs worst-case iteration, 20k:                           failures = 0
constants: (2R+1)K = 200100 < D_M = 204204; 4D_X = D_C; 10η − 0.01(1−η) = −0.008999; 4η ≤ 0.005(1−η);
           0.08(K−3)/(K+1) = 0.0768; 0.75(K+1)/K = 0.7575; 0.74(K−2)/K = 0.7252; R·0.005 = 5      all as claimed
negative controls: (3.3) with 0.3B → 720/720 violations; greedy bound − 2 → 537 violations (instruments can fail)
```

VERDICT: HOLDS AS READ
