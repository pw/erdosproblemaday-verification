# Referee report — seat `sample` — sib1 §5 (pp. 14–18)
Paper: "Asymptotically minimal maxima of real Littlewood polynomials" (sib1, 23 Sept 2026, /tmp/oaimath/076/sib1/paper.pdf)
Seat started 2026-10-12 ~09:18Z. Status: COMPLETE (~25 min of work; running notes first, final classified findings + verdict at the END of the file).

## Scope read (pages)
pp. 14–18 (§5: intro p.14, §5.1 Lemma 5.1 + proof p.15, §5.2 proof of Prop 2.1 pp.16–18) line by line from the PDF render; plus, as INPUTS consumed by §5, p.4 (Prop 2.1 statement, K_δ, 1−7δ), p.5 (Lemma 3.1 statement and the §3 heuristic), pp.9–14 (Prop 4.1 statement (15)–(16); Lemma 4.2 statement AND proof, because Lemma 5.1 rests on it). Status: COMPLETE.

## Method
Read the PDF render of pp. 4–18 (displayed math) cross-checked against layout text; re-derive each estimate in §5; check
uniformity of every O(·) in N, t, block centre; check every-N delivery.

## Findings (running)

### Running notes (first pass, ~10 min in)
- Read PDF render of pp. 4–19 (Prop 2.1 statement p.4; §3 statement of Lemma 3.1 p.5; §4 Prop 4.1 + Lemma 4.2 pp. 9–14 as
  INPUTS only; §5 pp. 14–18 line by line). Quotes below use the per-page layout files sib1/pages/pNNN.txt (line numbers = `cat -n`).
- Lemma 5.1 (p.15): re-derived. Poisson summation with f(y)=χ(y/N)e(by+(Nλ/2)(y/N−x*)²): f̂(ℓ)=N∫χ(x)e(Nφ_{b,ℓ}(x))dx — matches (31).
  Two integrations by parts: ((χ/φ')'/φ')' = χ''/φ'² − 3λχ'/φ'³ + 3λ²χ/φ'⁴ — matches the displayed integrand exactly (sign +, since
  (−1)²). Tail |ℓ|>L: φ' ≥ |ℓ|/2 because |λ(x−x*)+b| is bounded on supp χ × J; integrals O(N⁻²ℓ⁻²), sum ×√N = O(N^{-3/2}), uniform in b.
  Head |ℓ|≤L: phase expansion checked; u/(Tβ) = x*+(ℓ−b)/λ = x_{b,ℓ}; −u²/(2Nλ)+Nλx*²/2 = N[(b−ℓ)x*−(b−ℓ)²/(2λ)] = Nω_{b,ℓ} ✓.
  Lemma 4.2's error (π/(T|β|))∫ξ²|ĝ| is independent of u ⇒ uniform in b ✓. "Increasing L" so χ(x_{b,ℓ})=0 for |ℓ|>L ✓ (ℓ ∈ b+λ(suppχ−x*)).
  No defect found in Lemma 5.1.
- §5.2 (pp.16–17) maximum: b = t + a·θ_h, J = [min a·θ_h, max a·θ_h + 1] suffices since Q_X is 1-periodic; finitely many (a,h) ⇒
  finitely many applications of Lemma 5.1, each with its own fixed (χ_h, x*_h, λ_a, J) ⇒ the O(N⁻¹) constants are independent of N and t.
  Stationary contribution nonzero ⇒ x_{b,ℓ} ∈ supp χ_h ⊂ OPEN block ⇒ |ℓ−t−a·θ_h| < |λ_a|/(2H) STRICT ⇒ −t ∈ interior of I_{a,h}.
  Lemma 3.1 (as stated p.5) gives disjointness of all 2rH CLOSED intervals for σ = ±1, i.e. of I_{a,h} and I_{−a,h} too, and the
  widths w_i/H = |λ_{a_i}|/H coincide with (34)'s. So: ≤ 1 pair (a,h), and since the open ℓ-window has length |λ_a|/H < 1, ≤ 1 ℓ.
  Endpoints and ±a pairs are covered; closedness is not even needed (strict inequality). Main term ≤ |c_a|/√|λ_a|·‖χ_h‖∞ ≤ K_δ by (33).
  ⇒ (37) with error O(1/N) uniform in t. Delivers (1) with K_δ exactly as printed in Prop 2.1 (same K_δ = √((1+δ)³/(1−δ)) as (16)).
- Mean square (pp.17–18): X real ⇒ X² = χ_h²|F|², cross-block products vanish (disjoint supports), |F|² = Σ c_a conj(c_{a'}) e((a−a')·y)
  ⇒ (38) ✓. Three cases checked: a=a' Riemann sum → ∫χ_h²; κ≠0: Lemma 5.1 with amplitude χ_h², J={β} ⇒ N^{-1/2}·O(1) → 0;
  a≠a', κ=0: centers of disjoint closed intervals are distinct mod 1 ⇒ β∉Z; Abel summation with |Σe(kβ)| ≤ 2/|1−e(β)| and discrete
  variation ≤ ∫|ψ'| ⇒ O(1)/N → 0. Parseval (probability Haar, as declared p.9) ⇒ lim = (Σ∫χ_h²)‖F‖₂².
  (1−δ)(1−3δ)² = 1−7δ+15δ²−9δ³ ✓ (expanded by hand), ≥ 1−7δ since δ²(15−9δ)>0 ✓. The LIMIT exists, so liminf ≥ 1−7δ ✓.
- Every N ≥ 1: (35) is defined for every N with k/N against fixed real block endpoints (h−1)/H, h/H; no N/H rounding, no divisibility.
  Small N: |X_{N,k}| ≤ 1 still holds (at most one cutoff nonzero, |F| ≤ 1). Prop 2.1 only asserts limsup/liminf, so every-N is delivered.
  (k=0 gives X_{N,0}=0 since suppχ_1 ⊂ (0,1/H) compact; harmless.)
- Status after first pass: no FATAL/GAP yet. Next: numeric positive control of Lemma 5.1 and of the whole §5 mechanism on a toy F.

### Running notes (second pass: numerics, ~20 min in)
- Script dir /tmp/sample_seat_scripts/ (mine; nothing executed from the paper bundle).
- lemma51.py / lemma51b.py: Lemma 5.1 LHS vs RHS for χ = smooth bump on (0.2,0.6), x* = 0.31 (deliberately off-centre),
  λ ∈ {0.37, −0.23} (both signs, so e(sgnλ/8) and ω_{b,ℓ} are exercised), b over a grid of [−1,2]:
  λ=0.37: max_b|err|·N = 86.9, 132, 170, 183.8, 184.06, 184.08 at N = 500, 2k, 8k, 32k, 128k, 512k (saturates ⇒ O(1/N), uniform on the grid).
  λ=−0.23: N·err → 74.0 (same at 128k and 512k). Pre-asymptotic growth at small N is the bump's large ∫ξ²|ĝ|, as Lemma 4.2's
  error constant predicts. Phase conventions and the ω formula confirmed numerically.
- toy5.py: the full §5 mechanism (eq. (35)) on a hand-packed toy F = (cos2πy₁+cos2πy₂)/2 (c_{±e_i}=1/4, ‖F‖∞=1), H=2:
  PACKED, distinct curvatures v=(0.1,0.15): max|Q|/√N = 0.9085, 0.8646, 0.8117, 0.7954 (N=2k..128k) → predicted K = max|c_a|/√|λ_a| = 0.7906;
     mean X² = 0.22423 = predicted (Σ∫χ_h²)·‖F‖₂² exactly.
  PACKED, equal curvatures v=(0.1,0.1) (the a≠a', κ=0 case): same convergence, mean X² = prediction.
  NEGATIVE CONTROL 1 (intervals overlap, θ₁=(0.05,0.05)): max|Q|/√N → 1.4408 ≈ 0.7906+0.6455 (two stationary contributions add) — fires.
  NEGATIVE CONTROL 2 (κ=0 AND β∈Z): mean X² = 0.44846 = 2× prediction — fires (this is exactly why the paper needs distinct centres).
  So the instrument can fail, and on correctly packed data it agrees with the paper's (37) and (39).
- Cross-read (not a substitute for the kernel replay): OpenAI's Lean `almost_sign_sampler` (AlmostSign.lean l.12–20) states the §5
  output in the STRONGER finite-N form ∀N≥1 ∀t∈[0,1]: ‖N^{-1/2}Σ X_{N,k} e(kt)‖ ≤ √((1+δ)³/(1−δ)) + C/N, |X N k| ≤ 1, and
  (1/N)ΣX² → L ≥ 1−7δ, with δ ∈ (0,1/20) — the same constants and the same O(1/N) uniformity I derived from the paper.

## Findings (final, classified)

No FATAL. No GAP. Item-by-item against the seat's checklist:

1. Lemma 5.1 uniformity (p.15). Uniform in b ∈ J: tail |ℓ|>L by two integrations by parts with |φ'_{b,ℓ}| ≥ |ℓ|/2 on supp χ × J
   ("Choose a fixed integer L so large that, for |ℓ| > L, |ϕ′b,ℓ(x)| … ≥ |ℓ|/2 on supp χ, uniformly in b ∈ J", p015 l.72–79);
   head |ℓ|≤L by Lemma 4.2, whose error π/(T|β|)∫ξ²|ĝ| is independent of u (p.11, proved, I re-derived the Gaussian identity (18),
   the branch, |(ρ−iTβ)^{-1/2}| ≤ (T|β|)^{-1/2}, and both dominated-convergence steps). The block centre x* and λ are FIXED data of
   each application, not varying parameters; the paper never needs uniformity in x* because there are finitely many blocks (H fixed).
   Constants depend on (χ, x*, λ, J) only, as stated (p015 l.44). HOLDS.
2. "At most one stationary contribution per angle" (p016 l.112–119, p017 l.1–3). Nonzero leading term ⇒ x_{b,ℓ} ∈ supp χ_h, a compact
   subset of the OPEN block ⇒ strict inequality |ℓ−t−a·θ_h| < |λ_a|/(2H) ⇒ −t in the interior of I_{a,h}. Lemma 3.1 as stated (p.5)
   makes all 2rH closed intervals pairwise disjoint over σ ∈ {±1}, so I_{a,h} ∩ I_{−a,h} = ∅ (the ±a pair of a real F) and intervals of
   different blocks are disjoint too; widths match ((34) length |λ_a|/H = w_i/H). Interval length < 1 ⇒ ≤ 1 integer ℓ. Endpoints: the
   strict inequality means closedness is never even used. HOLDS for every t, including endpoints and ±a. (Correctness of Lemma 3.1
   itself is the `construct` seat's.)
3. Poisson summation and integer-frequency shifts (p015 (31)): f(y)=χ(y/N)e(by+(Nλ/2)(y/N−x*)²) is C_c^∞, f̂(ℓ)=N∫χ e(Nφ_{b,ℓ}) with
   φ_{b,ℓ} = λ(x−x*)²/2 + (b−ℓ)x ✓; phase expansion and stationary point x_{b,ℓ}, value ω_{b,ℓ} re-derived ✓. HOLDS.
4. Non-stationary contributions: there is no separate "non-stationary blocks" argument — every (a,h) goes through Lemma 5.1, whose main
   term simply vanishes when −t ∉ I_{a,h}, leaving O(N^{-1}). The integrations by parts (tail ℓ) use 2 derivatives of χ; the integrand
   ((χ/φ')'/φ')' = χ''/φ'² − 3λχ'/φ'³ + 3λ²χ/φ'⁴ matches p015 l.84–100 exactly; no boundary terms (compact support in R; cutoffs
   χ_h ∈ C_c^∞((h−1)/H, h/H) strictly inside the block, p016 l.61). HOLDS.
5. Mean-square recovery (p017 l.40–80, p018 (39)): three cases a=a' / κ≠0 / (a≠a', κ=0) each re-derived; the third uses "The centers of
   I_{a,h} and I_{a′,h} are distinct modulo one, so β ∉ Z" (p017 l.62–63) — follows from disjointness of the closed intervals. Abel
   summation constant 2/|1−e(β)| · (‖ψ‖∞ + ∫|ψ'|) is fixed. Parseval with probability Haar (declared p.9). (1−δ)(1−3δ)² =
   1−7δ+15δ²−9δ³ ≥ 1−7δ for 0<δ<5/3 ✓. The limit EXISTS, stronger than the liminf claimed. HOLDS.
6. Delivery of (1) with K_δ exactly: main term modulus ≤ |c_a|·‖χ_h‖∞/√|λ_a| ≤ K_δ by (33), K_δ in (16), (33) and p.4's (1) are the same
   √((1+δ)³/(1−δ)) ✓; error Σ_{(a,h)} |c_a|·C_{a,h}/N, finitely many pairs ⇒ (37) as K_δ + O(1/N) uniformly in t. HOLDS.
7. Every O(·): all constants depend on (F, v, a_i, H, θ_h, χ_h), all fixed by δ before N; none on N or t. Quantifier order:
   δ → Prop 4.1 data → Lemma 3.1 (H, θ_h) → cutoffs χ_h → (per Lemma 5.1 application) L, error constant → N. No cycle. HOLDS.
8. Every integer N ≥ 1 (p016 l.74, p018 l.39–41): (35) is defined for every N; blocks are fixed real intervals sampled at k/N; no N/H
   rounding, no H | N, no prime condition; |X_{N,k}| ≤ 1 for every N (at most one χ_h nonzero at k/N, |F| ≤ 1). Prop 2.1 asserts only
   limsup/liminf, so small N needs nothing more. HOLDS. (Side remark: X_{N,0} = 0 always, since supp χ_1 ⊂ (0,1/H) is compact; harmless.)

EXPOSITION (repairable, none affects the proof):
- E1. Overloaded symbols across sections: β is Theorem 3.2's degree tolerance (p.6), Lemma 4.2's curvature (p.10), and (38)'s
  (a−a′)·θ_h (p017 l.52); L is §3's total slot length ΣL_i (p.6) and Lemma 5.1's tail cutoff (p015 l.72); J is §3's slot interval (p.9)
  and Lemma 5.1's compact b-set (p015 l.8). Each is locally unambiguous.
- E2. p017 l.58–59 "Lemma 5.1, now with amplitude χ_h², shows that the sum with normalization N^{−1/2} is bounded" leaves implicit that
  the compact set is J = {β} and λ = κ; trivial to supply.
- E3. p016 l.119 "−t (mod 1) lies in I_{a,h}" — the argument actually gives the INTERIOR of I_{a,h}; stating it that way would make the
  endpoint remark (p017 l.2–3) unnecessary. Cosmetic.

## External inputs checked
- None outside the paper are logically used in §5. "Bombieri and Bourgain [5, Section 7] use Poisson summation …" (p015 l.5–7) is an
  attribution only; Lemma 5.1 is proved from scratch from Poisson summation + the paper's own Lemma 4.2. I did NOT fetch [5]
  (not load-bearing). Internal inputs consumed: Prop 4.1's (15)–(16) (statement), Lemma 3.1 (statement), Lemma 4.2 (statement + proof,
  re-derived). Their proofs (other than Lemma 4.2) belong to the `construct` seat.
- Numeric positive + negative controls (see running notes): Lemma 5.1 error is O(1/N) uniformly on a b-grid for both signs of λ with
  an off-centre x*; the §5 mechanism on a packed toy reproduces (37)'s constant and (39)'s mean square; both negative controls (overlap;
  κ=0 with β∈Z) fire.
- OpenAI Lean `almost_sign_sampler` statement (AlmostSign.lean l.12–20, read-only): same constants, finite-N form K_δ + C/N for all
  N ≥ 1 and t ∈ [0,1]. Read as corroboration of the paper's quantitative shape, NOT as a kernel check (that replay is queued separately).

## What I skimmed / did not check
- Did not check Lemma 3.1's proof (§3 pp.5–9) or Prop 4.1's proof beyond Lemma 4.2 (pp.11–14) — `construct` seat. §5's correctness is
  conditional on Lemma 3.1 delivering EXACT (not asymptotic) disjointness of all 2rH closed intervals for a fixed H, which is what its
  statement says.
- Did not read the Lean sampling modules (BlockSampling / ModeSampling / SamplingEnergy / SamplingTail / QuadraticTail) beyond the
  AlmostSign statement; did not run lake/lean.
- Did not fetch Bombieri–Bourgain [5].
- §6 / Theorem 1.1's use of (2) (1−8δ ⇒ µ ≤ 4δN) only glanced at (p.5): consistent, but it is the `reduce`/`round` seats' scope.

## Verdict
HOLDS AS READ IN SCOPE — sib1 §5 (Lemma 5.1, §5.2) proves Prop 2.1 as stated (K_δ exactly, 1−7δ, every N ≥ 1, errors O(1/N) uniform
in t with constants fixed by δ before N), conditional on Lemma 3.1 and Prop 4.1 as stated; three EXPOSITION nits only.
