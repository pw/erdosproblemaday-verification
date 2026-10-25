# Seat A report: §1.2, §2, §3, §4

Referee: Seat A (hostile). Scope: printed §1.2 (Method), §2 (Large-prime labels and their short averages), §3 (Arithmetic preliminaries at an auxiliary log scale) and §4 (Amplifying a mixed correlation). I read every lemma and proof line by line in the TeX (introduction/labels/arithmetic/amplification.tex) and cross-checked numbering against paper.txt. External sources fetched, current versions:

- MR arXiv:1501.04585v4
- MRT arXiv:1503.05121v3
- Ford, zeta zero-free regions, arXiv:1910.08205v5
- Ford, Sieve Methods Lecture Notes 2023 (sieve2023.pdf)
- Koukoulopoulos, *The Distribution of Prime Numbers*, preliminary version (primes.pdf)
- Granville–Koukoulopoulos, LSD paper

Scratch work is in `seats/A_work/`.

**Bottom line:** I found no FATAL objection and no GAP in §§1.2–4. Every external input is cited for what the source actually says, with hypotheses that the paper's inputs satisfy. The order of limits inside these sections is correct. All objections below are EXPOSITION or minor. The dependency notes in Part B are things §§5–11 must respect; I spot-checked that §10 does respect them.

---

## A. Objections

### A1. Symbols are overloaded in ways that invite a wrong order-of-choice reading (EXPOSITION)

- **`C_0` has three meanings.**
  1. Lemma 3.2: "absolute constant `C_0` such that |C_{j,z}(P_0)| ≪_j (log P_0)^{C_0+j}".
  2. Lemma 4.1: "There exist C_0 > 0 and d_0 > 0 such that, for each fixed C_* ≥ C_0 …". This threshold may depend on the grid and τ, through the constant C in (3.11).
  3. §10: "Here C_0 can be chosen independently of C_*, η and C_6".

  Meanings 2 and 3 are different constants.
- **`H` has five meanings:** the expansion order (Lemmas 3.1–3.2), H_B = (log P_0)R^{1/2} (Lemma 3.5), H_B = L_B/d (§2.5), the window length (Lemma 4.3), and H(t,w) = φW (Lemma 4.4).
- **`L`** is used both for the grid size and for log P_0 (Lemma 4.3).
- **`X` and `c`** are reused freely.

None of this causes an error. But a reader auditing whether "C_0 independent of C_*" is checking the right constant has to disambiguate by hand. Suggested fix: rename Lemma 4.1's threshold to something like C_*^{min}.

### A2. The no-change term converges absurdly slowly; correct but wasteful (EXPOSITION)

§4.4, second moment (printed p. 33):

> "B R^{−α0} = B^{1−α0}(1000 log B)^{α0} → 0."

This is true, but with α_0 − 1 = 0.109 it is a very weak limit. Numerically, B·R^{−α_0} ≈ 8.7·10^3 at B = 10^6. The argument is qualitative (B → ∞), so this is not an error.

A cleaner bound uses the g = 1 total-count cutoff already imposed. All four first-split sets have ≥ (1/2 − τ)ℓ primes, so the no-change probability is at most 2^{−2(1−2τ)ℓ} = R^{−1.386+O(τ)}, which is ≪ B^{−1.38}.

### A3. The sieve citation is stated in a weaker, re-parametrised form (EXPOSITION)

§3.2 says the upper sieve with "weights … supported on squarefree d ≤ D … when Z ≤ D^{1/s_k}" is "the bounded-dimension upper-sieve statement of [Ford, Theorems 2.4 and 3.6]".

Ford's Thm 2.4 gives S(A,z) ≤ O_{κ0,B0}(XV(z)) + Σ_{d≤z, μ²(d)=1} |r_d|, assuming (Ω). Hypothesis (Ω) follows from θ_p ≤ k/p with p > P_k > 2k (Ford's (Ω_0)). So the paper's version is implied, with s_k = 1. The citation is accurate, just re-parametrised.

### A4. Bibliographic nit (EXPOSITION)

The bib key `FordZeta2022` refers to a 2002 article; the corrected arXiv v5 is dated 2025. The cited (1.2) is the Richert-type bound |ζ(σ+it)| ≤ A|t|^{B(1−σ)^{3/2}} log^{2/3}|t| for 1/2 ≤ σ ≤ 1, |t| ≥ 3. At σ = 1 it gives the (log)^{2/3} that the paper weakens to (log)^{3/4}. Fine.

No other objection survived checking.

---

## B. Dependencies that §§5–11 must respect

### B1. Lemma 2.3 (2.12) has no rate in B

Lemma 2.3 is a pure lim_B limsup_x = 0 statement for FIXED s_0, s_1, D, r, v, with arbitrary sequences T(B), L_B → ∞ and a_B. Any downstream use must therefore:

- (i) fix D, r, v, s_0, s_1 before B grows;
- (ii) multiply the block averages only by coefficients bounded uniformly in B;
- (iii) use finitely many such averages, fixed before B grows.

I checked §10 (printed (10.4)–(10.5), "It remains to show that the fully factored expression tends to zero"):

- D is the period of the fixed S_{P_1}.
- The v's are fixed polynomial monomials.
- The blocks J_a have L_a ≥ c_{δ,C_6}T → ∞ and B-dependent origins, which Lemma 2.3 allows via a_B.
- There are R_0 blocks, a fixed number.
- The coefficients L_aL_b/(MT), w, k_B and h_l are asserted uniformly bounded.

So the use matches the lemma as stated. Seat B should verify that k_B and the h_l really are bounded uniformly in B; that is outside my scope.

### B2. Order of parameter choices around c_5

c_5 = (d_0β_*)²/C_4 depends only on (ρ_0, ψ, φ, W) and on a sieve constant C_4. It is independent of C_*, the grid, τ, η, C_6 and the partition. Lemma 4.1's threshold for C_* may depend on (grid, τ).

§10 chooses in the order: grid and τ (absolute, §6 "impose no condition on C_*"), then C_*, then η and C_6, then the partition. There is no cycle.

---

## C. Steps checked and found sound

### §2 (labels and short averages)

- **Lemma 2.1 (bin-count law).**
  - The factorial moments are computed correctly.
  - Selections with d ≤ βx number O(x/log x), so the O(1) progression errors sum to o(x).
  - Squares of bin primes, repeated selections and the moving boundary Σv ≤ 1 + log β/log x all cost o(1).
  - Falling-factorial monomials with r_k ≤ J span the functions on the finite count set, so moments determine the law.
  - The limit is independent of α, β, q, a because log β/log x → 0.
  - The multiplier invariance (2.6) holds because f_x(u) = g_x(u) = 1 once P^+(u) ≤ x^{1/J}.
- **Theorem 2.4 (real short intervals).** It does follow from MR Thm 1 (v4). The exceptional set there is ≤ CX((log h)^{1/3}δ^{−2}h^{−δ/25} + δ^{−2}(log X)^{−1/50}), uniform in all f: N → [−1,1]. Since X ≥ h, take δ = (log h)^{−1/200} and bound the exceptional set trivially by 4. This gives r(H) → 0, and moving from integer to real origins costs O(1/H). The paper's claim "terms depending on X can be absorbed because X ≥ H" is exactly right.
- **Theorem 2.5 (complex).** MRT Thm A.1 (v3) gives ≪ e^{−M}M + (loglog h/log h)² + (log X)^{−1/50}. The Remark after A.1/A.3 says the published proof was wrong for slowly growing M and that the corrected proof gives e^{−M}. The paper's (1+M)e^{−M} is weaker than both, hence valid. M(f;X) = inf_{|t|≤X} D² as in MRT (1.6).
- **Lemma 2.6 (non-pretentiousness).** The lower bound is D² ≥ (1/(4m²))·loglog x − O_{J,c,C,χ,E}(1), uniformly for |t| ≤ CX.
  - For |t| ≤ 1: log|L(σ+it,χ)| ≤ C (nonprincipal L is entire, compact region).
  - For |t| > 1: 1 − Re z^m ≤ m²(1 − Re z) (checked numerically, max violation 1.7e−15), plus log|ζ(σ+imt)| ≤ (3/4)·loglog x + O(1).
  - The comparison between p ≤ y with weight 1/p and all p with p^{−σ} is O_J(1); I verified the substitution ∫_{1/J}^∞ e^{−v}/v dv.
  - The Phragmén–Lindelöf extension is valid: finite order, and the log branch is analytic since Re(s+3) ≥ 4.
  - Uniformity over all h_x with this prime agreement is genuine; E = P_B is finite at fixed B.
- **Lemma 2.3 (2.12): the key §2 input.**
  - The interpolation by finitely many completely multiplicative h_{ℓ,x} with values in [0,1] uses tensor Vandermonde on {0..J}^{J−1}. It is valid because each bin count is ≤ J on m ≤ C_B x for x large. I checked it numerically for J = 3: residual 3e−12. The coefficients depend only on J and the phases.
  - The reduction m = dk, with k in a unit class mod q = D/d, is correct.
  - G_{B,v}(dk) = G_{B,v}(k) once min P_B > D.
  - Principal character: the h_ℓ G χ_0 are real in [0,1] and multiplicative, so Thm 2.4 applies uniformly. Σ_ℓ c_ℓ L_X(h_ℓ G χ_0) = L_X(F G χ_0) → 0 by Lemma 2.1 in classes modulo the fixed period q·∏_{P_B} p. The constant is (Σ|c_ℓ|)², independent of B.
  - Nonprincipal characters: Lemma 2.6 with E = P_B gives M → ∞ at fixed B. Theorem 2.5 then leaves C(loglog H_B/log H_B)².
  - Dyadic covering: O(log(s_1/s_0)) intervals, scales comparable to Tx/d, origin flooring at multiplicity ≤ d+1, all fixed at fixed B.
  - Conclusion: the centred function is handled via a FIXED finite multiplicative family, uniformly in x at fixed B, as the paper claims.
- **Profile W (§2.6).**
  - λ_x → dt dw by progression counting plus Stone–Weierstrass, since products φ(t)·(locally constant in w) are dense in C_c.
  - |ν_x| ≤ 2λ_x gives local uniform variation bounds. C_c((0,∞)×Ẑ) is separable, so a diagonal weak-* extraction works.
  - |∫Φdν| ≤ 2∫|Φ| for all Φ gives |ν| ≤ 2 dt dw by duality/outer regularity, then Radon–Nikodym gives |W| ≤ 2.
  - Passing to 1_{(0,1)} costs O(ε) at both ends.
  - The subsequence depends only on J, the phases and the bad sequence. It is chosen once, and the convergence then holds for EVERY test, hence for every B simultaneously. There is no B-dependent subsequence.

### §3 (arithmetic preliminaries)

- **Lemma 3.1.** Standard Selberg–Delange.
  - Twisted case: zero-free region (Koukoulopoulos Thm 12.3) plus Siegel (Thm 12.10, quoted correctly). ε < 1/(2C) gives 1 − β ≫ L^{−Cε} ≫ L^{−1/2} for d ≤ L^C.
  - The polynomial bound for L on the rectangle and the Perron shift are correct.
  - The citations (GK Thm 1; Koukoulopoulos Thm 13.2) are for the classical expansion only, which is what is used.
- **Lemma 3.2.**
  - h_z(p^e) = (−z)^e for p ≤ P_0 gives g_{z,P0} = g_z * h_z; I verified the Euler factors.
  - The Rankin bound is (log P_0)^{C_0}.
  - The tail v > √Y is exp(−L_Y/(2 log P_0)), negligible since L_Y ≥ B^{0.89}.
  - The C_{0,z} formula and its Mertens asymptotics are right.
  - Character range: B^{15} ≤ (B^{0.89}/2)^{18}.
- **m_B and f_{z,B} limits.** These are consistent with the generalised-Dickman law: the Lévy measure z·dv/v on (0,4] has density e^{−γz}s^{z−1}/(4^zΓ(z)) = c_z s^{z−1} exactly on (0,4]. Also c_{1/2} = c_A/2, consistent with (3.5) giving the ratio 1/2.
- **Proposition 3.3.**
  - (3.2): Ramanujan sum c_q(u) = μ(q) for (u,q) = 1. Error budget: q·(1+|ξ|)·B·B^{−200} ≤ B^{−170}. The ranges q ≤ B^{15}, |ξ| ≤ B^{14} cover the §8 major-arc use (q ≤ B^{10}, |ξ| ≤ B^{13}).
  - (3.3): the exact ν_z(n) formula, B^{−199} from partial summation, B/P_0 correction.
  - (3.4): the two regimes δ < 1/R (empty product) and δ ≥ 1/R (Mertens) are correct.
  - (3.5): the ratio → Q R^{1/2} → 1/2.
- **Lemma 3.4.**
  - The fundamental-lemma remainders are as stated. In the rectangle: (N_1+N_2)N_*^{1/2+o(1)} + N_*^{1+o(1)} ≪ N_1N_2N_*^{−0.4}, checked.
  - The small-prime restoration factor is bounded (surviving fraction ≥ 1/p or 1/p²).
  - The weighted version via independent random forbidding is exact.
- **Lemmas 3.5 and 3.6.**
  - Local densities (log P_0)^{−1}R^{t−1} with t = 1/2, 1/4 give 1 and B^{1/4+o(1)}.
  - In (3.7) and (3.8), p | j forces p < P_0 because |j| ≤ T < P_0. The loss 1 + O(1/p) is absorbed by Σ(j).
  - p | b forces p > P_0, with total cost O(B/P_0).
  - Odd j with odd b kills the count entirely, and the sieve lemma covers this ("whole residue space forbidden ⇒ zero").
- **Definition 3.7, (3.9) and (3.10).**
  - A, K ≤ B^{h_0+τ log 2+o(1)} from the g = 1 lower cutoff.
  - Numerics: 2h_0 = 0.30685, 1 − 6h_0 = 0.07944, 1 − 5h_0 = 0.23287. All three strict inequalities hold for τ < 0.001116, so they are compatible.
- **Lemma 3.8 (regularity loss).**
  - Exponential-Markov tilts inside the weighted sieve are valid, because the tilted weights stay in [0,1] and dropping primes above Z is in the upper-bound direction for both tilts. Primes above Z number ≤ 4/c, which shifts the g = 1 count by O(1).
  - The prefix brackets are ≤ −sτ/2.
  - The tail bracket is −0.1s + O(s²) with a_s > 0. For example, at s = 0.1: 0.04 − 0.0476 < 0.
  - The geometric sum over dyadic Y is dominated by its top term, which gives c_3 = s absolute.
  - The probability version with λ_p = 1/(2p) + O(p^{−2}) and an omitted set E_B is correct.

### §4 (amplification)

- **D_B on Ẑ (4.1).**
  - D_B is determined by w mod ∏_{p∈P} p², hence locally constant.
  - φ(t)D_B(w) is an admissible test, so (4.3) holds along the FIXED subsequence for each B.
  - Fair-split identity (3.1): A_0(a_U)K_0(S∖U) = B·2^{−|S|}, checked. A numerical check of E_split e^{−v log b/B} = ∏(1+p^{−v/B})/2 gave agreement to 1e−15.
- **Lemma 4.2.**
  - Per-prime total variation is O(1/p²). Residues at distinct primes are independent under Haar measure.
  - On the success event, D_B = D̃_B exactly.
  - sup D_B ≪ B^{1+O(τ)}, since ≤ 2^{2(1+2τ)ℓ} representations each have weight ≤ B^{4(h_0+τlog2)−1}. This is well under the paper's B^4, so the error is O(B^8/P_0).
- **First moment.**
  - a and c are independent with law ν_{1/2}.
  - B·E_aψ(a/(Tc)) → f(s)∫ψ dr/r. The window has width O(1/B) and the (3.3) error is O(B^{−80}) absolute.
  - d_* = (∫ρ_0 f²)(∫ψ dr/r) > 0.
  - Coefficient-regularity loss: O(B) dyadic boxes, each ≪ TX²(ε_B + e^{−c_3C_*})/(B²TX²). After the outer factor B this gives o(1) + O(e^{−c_3C_*}).
  - Remaining-set loss: conditional remaining probabilities are 1/(2p−1). The coefficient primes form an omitted set with Σ1/p ≪ B/P_0.
  - Hence d_0 = d_*/2 for C_* ≥ C_0. d_0 is independent of C_* and B.
- **Second moment, P(E_1∩E_2) ≪_{C_*} B^{−2}.**
  - The orientation symmetry under swapping the two splits is valid in the original law, applied before coupling.
  - The coupling to four independent Bernoulli(1/(2p)) processes costs O(1/P_0), which is ≪ B^{−2}.
  - The conditioning order is correct: Q_ν (recipient additions below Y, independent Bernoulli(1/(4p))) is independent of F, J(F) is F-measurable, and G_Y, H_Y are in F.
  - P(H_Y | high sets) = 2^{−Σ(N_C+N_R)(>Y)} ≤ 2^{−4q(Y)} = 2^{4C_*}(Y/B)^{α_0}.
  - α_0 = 1.6 log 2 = 1.1090 > 1. So Σ_Y (Y/B)^{α_0}/Y ≪ 1/B, dominated by the largest Y < 8B. The case q(Y) < 0 is harmless.
  - The no-change term is o(1/B); see A2.
  - Total: (1/B)·O_{C_*}(1/B).
- **Lemma 4.3 (small ball).**
  - The exact law P(Q=n) = q_Y w_Y(n)/n holds, and w_Y ≤ w majorisation is valid.
  - The sieve level Z = e^{cY} ≤ X^{c_s} because X ≥ e^{Y/2} and 2c < c_s.
  - q_Y·𝒟 ≪ (L/Y)^{1/4}·(1/L)(L/Y)^{3/4} = 1/Y. The case Z < P_0 also gives ≪ 1/Y.
  - The remainder q_Y X^{−0.2} ≤ e^{−Y/10}.
  - The result is uniform in the location of the interval.
- **Lemma 4.4 (preservation).**
  - H = φW ∈ L². The conditional-expectation approximation H_q (w mod q, q = N!) preserves both the integral and the t-support.
  - D_B is independent of w mod q once P ∩ {p | q} = ∅.
  - The Cauchy–Schwarz error is ε·√|supp φ|·‖D_B‖_2 ≪_{C_*} ε, uniform in B.
  - Then (4.8): liminf_B lim_x |I_{1,x}|/B ≥ d_0β_*. This order is legitimate: ε → q → B, then B → ∞.
- **(4.9), Cauchy–Schwarz and Proposition 4.5.**
  - The reindexing n = am is exact. g_x(am) = g_x(m) holds simultaneously for the finite coefficient list at fixed B.
  - Cauchy–Schwarz with the nonnegative weights x^{−1}ρ_0A(c)K(m) on I_{c,x} gives |I_1|² ≤ V·I_2.
  - limsup_x V ≤ C_4B/T, from K ≤ K_0 (periodic, mean ~1/2) and Σ_c ρ_0A_0(c)/c ≪ B over O(B) dyadic boxes via (3.6).
  - Hence liminf_B liminf_x I_2/(BT) ≥ (d_0β_*)²/C_4 = c_5. c_5 is independent of C_*, η, C_6, the partition, the grid and τ.
  - Diagonal: Q_B ≤ B^{2(h_0+τlog2)+o(1)} = o(T = B^{0.32}), and 𝒥_{B,x} = (B/x)Σφ(n/x)D_B(n) → B∫φ∫D_B ≪ B. So the diagonal vanishes in lim_B limsup_x.
  - The off-diagonal coefficient windows give 0 < |j| < T. I verified the substitution n' = b·l_a, n'+j = a·l_b algebraically: a·l_b − b·l_a = (a−b)/c = j.
- **Order of limits (§§2–4).**
  - x → ∞ is always along the single subsequence fixed in §2.6, at fixed B (and fixed C_*, grid, τ).
  - Quantities chosen after the subsequence (φ, β_*, d_0, C_4, c_5) are used only as fixed constants or B-independent lower bounds.
  - Nothing in §§3–4 needs uniformity in x across B. Every "for x sufficiently large" (multiplier invariance, interpolation identity, Lemma 2.6 threshold, progression counting) is at fixed B.

---

## D. Numerics run

Scripts are in `seats/A_work/scripts/`.

- **Elementary progression count.** #{αx<n≤βx : n≡a (q), d|n} − (β−α)x/(qd) was checked over 2·10^4 random cases (gcd(q,d) = 1). The maximum absolute deviation was 0.994 ≤ 1, as claimed.
- **Constants.**
  - α_0 = 1.1090354889 > 1.
  - 2h_0 = 0.3068528; 1 − 6h_0 = 0.0794415; 1 − 5h_0 = 0.2328680. These match the printed values.
  - τ < 0.001116 suffices for all of (3.10).
- **Interpolation (2.18), J = 3.** The tensor Vandermonde solve is exact (residual 3e−12).
- **Fair-split identity.** Verified to machine precision.
- **Lemma 2.1, J = 3, x = 3·10^6.**
  - Limit law: P(0,1) = log(3/2) = .4055, P(2,0) = M_2/2 = .1472, P(1,0) = .3987, P(0,0) = .0486.
  - Empirical laws for (0.2x,0.5x] ≡ 3 (mod 4): within ~0.01–0.02 of the limit.
  - For (x,2x]: moderate deviations.
  - For (5x,6x] ≡ 2 (mod 7): visibly off, e.g. (1,1) mass .048, which the limit forbids.
  - This shows the convergence is only at rate ~log β/log x. That is consistent with the lemma as an asymptotic statement and harmless in the iterated limit, since β ≍ T(B) is fixed while x → ∞. It is not an objection.

---

## Summary

Within §§1.2–4, the short-average theorem is a correct consequence of MR Thm 1 and MRT Thm A.1 (corrected), applied to a fixed finite family of multiplicative interpolants with the right uniformity. The divisor weight has positive Haar mean and bounded L² norm, and the profile, Cauchy–Schwarz, energy and diagonal steps are correct in the stated iterated limit along a single fixed subsequence. Only exposition issues were found.

VERDICT: HOLDS AS READ
