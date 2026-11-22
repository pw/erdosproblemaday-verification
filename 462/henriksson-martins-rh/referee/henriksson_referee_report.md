I found no mathematical error and no gap between the Lean inputs and the published theorems. My recommendation is **VERIFIED, as a result conditional on RH**. The implications from RH to the Chirre–Hagen and Cully-Hugill–Dudek estimates are cited from their papers, not formalized. Siebert's original 1976 paper is paywalled, so I could not read his exact wording.

## Verdict per item

| Item | Verdict | Basis |
|---|---|---|
| Thm 1.1 (§2) | **HOLDS** | Rests on Chirre–Hagen Thm 3 under RH. Lean-checked from that exact published statement. Your hand check agrees with mine. |
| Lemma 3.1 (§3) | **HOLDS** | Every constant recomputed. Lean `fixed_length_supply` proves S/320. |
| Thm 1.2 lower (§3) | **HOLDS** | Rests on Cully-Hugill–Dudek Thm 1 under RH, Siebert, and PNT. Lean-checked. |
| Thm 1.2 upper (§4) | **HOLDS** | Unconditional: Siebert plus Mathlib's Chebyshev bound. Lean-checked. |
| A.2 (Grenié–Molteni–Perelli route) | **HOLDS** | Not formalized. The cited Prop 1 matches. |
| A.3 | **HOLDS** | Lean-checked (`cully_dudek_wide_interval`). |

## Constants recomputed (exact rationals, `scripts/consts.py`)

**Lemma 3.1**
- (9/4)·log 4 = 3.119 < 4.
- Diagonal: 4Sh/log S ≤ 2Sh²/(log S)², using h ≥ 2 log S.
- Expanding g(2k) = Σ_{m|k} a_m and Σ_j (h−2mj)_+ ≤ h²/(4m) gives h²/(4ω), because 1 + 1/(ℓ(ℓ−2)) = (ℓ−1)²/(ℓ(ℓ−2)) = 1/(1−(ℓ−1)^−2).
- Off-diagonal: 2·16ω·h²/(4ω)·y/log²y = 8yh²/log²y. At y = 9S/4 this is ≤ 18Sh²/log²S, so the total is 20.
- First moment: for p ∈ (5S/4, 2S] and h ≤ S/4, the interval [p−h, p) lies inside [S, 2S]. PNT gives (3/4)S/log S ≥ S/(2 log S).
- Cauchy–Schwarz: (1/4)²/20 = 1/320 > 1/2500.

**Thm 1.2 lower**
- 808·16 = 12928. Since x/T² = 1/r², the excluded s-measure is 12928N/(Cr²) = 25856S/(Cr). This is ≤ bS/2 exactly when r ≥ 51712/(bC).
- q ≤ 9S/4 = 9N/(8r) < N < T < p ≤ (1+η)2T < 3T.
- Count: (bS/2)(h/4L)(ηT/4L)/h with ST = N²/2 gives bCN/64.
- Window: 3ηx = 3CNL² ≤ 4CNL² = H_C(x). Weight bound bC/(192r).
- The variant using (1) instead: 48L²/η, 96S/(Cr), r ≥ 192/(bC). Correct, but not formalized.

**§4 upper**
- dy = 4L. Small primes: 2(4L + 1/(C²L²))/(L/2) = 16 + o(1) ≤ 20.
- Since y³ > x + H, every remaining composite is pq with y < p ≤ q.
- The starts p/(1+d) < t < p lie in [S/2, 2S] and have length ≥ dS/2.
- v ∈ [T/4, 2T], |dt/dv| ≤ 16S/T.
- dS ≥ 4L and dT ≥ 2CL². With d ≤ 1/96 and 3CL ≥ 1, both window lengths lie in [2 log U, U/4] on every dyadic piece.
- Second moments: 80·(3/2)·4 = 480 and 16·80·(7/4)·36 = 80640, summing to 81120.
- M_S ≤ 81120·dST/L². Weight per product ≤ 2S/x, which gives 162240·dS/L².
- ΣS ≤ 4N, so the total is 648960·dN/L² = 2595840C. Final bound 20 + 2595840C.

**A.2**
- 4D(h + log²Y)log²Y/h² ≤ 8DY/K. Exceptions: 8 + 4·4 = 24, so K ≥ 192D gives ≤ N/8 and |G| ≥ 3N/8 ≥ N/4.
- Consecutive a-th powers are ≥ (N/2)^{(a−1)/a} ≥ √(N/2) apart (confirmed against preprint.tex).
- Prime powers contribute O(log N log log N) = o(h).
- Count Nh/(64 log²3N). On [3N/2, 2N], t + x/t ≤ 5N/2 ≤ 8N/3. Weight ≥ K/768, and 4Nh = K√x(log x)².

**A.3**
- 64·808/9; 1/2 − 320·808/(9·131072) = 647/2304 ≈ 0.2808 > 1/4.
- δN²/(128L²) = 1024N; 3·131072 = 393216 = 98304·4.

**§2 threshold**
- B¹⁵ < (1359/500)⁶⁵⁶ holds by exact integer comparison, but the margin is only 0.00286 in log. log B = 43.72861 against 656/15 = 43.73333.
- δ at B is 9.9954·10⁻¹⁴ < 10⁻¹³. B² = 9.598·10³⁷ < 9.6·10³⁷.

## Objections (none fatal)

1. **Siebert fidelity (§3, the displayed bound before "where g(d) = …").** The sentence is "For every even integer d > 0 and every real y > 1, Siebert's sieve bound [10, p. 327], with a = 1 and b = d, gives #{p ≤ y : p, p + d prime} ≤ 16ω g(d) y/(log y)²."
   - Springer gives only the abstract of the original.
   - Ramaré's TME-EMT explicit-estimates database quotes it without a limit on p + d ("a, b coprime, 2|ab, x > 1"). This matches the Lean Prop exactly.
   - Tao (arXiv 1201.6656, p. 22) quotes the limited form {p ≤ x : p+h−h′ prime, p+h−h′ ≤ x}.
   - If the original only had the limited form, `SiebertBound` would assume more than Siebert proved. Every use only needs pairs with q = p + d ≤ y = 9S/4, so this would be a fixable fidelity point, not an error.
   - Numerically the Prop holds comfortably: count/bound ≤ 0.21 over y ≤ 2·10⁵ and even d ≤ 600.
2. **Lemma 3.1 states "b = 1/2500"** while the proof gives 1/320. Harmless slack.
3. **Not formalized:** A.2, and the "Using (1) instead …" variant of the Thm 1.2 lower bound. Lean's `theorem_1_2_lower` takes the Cully-Hugill–Dudek bound. Both pass my hand check.
4. **Cosmetic:** A.2 uses "a" both for the grid shift and for the exponent.
5. **Errata hunt.** Lee (arXiv 2403.11814, footnote 1) reports a typo affecting constants in a *different* Cully-Hugill–Dudek paper (Res. Number Theory 8 (2022), Paper 61). I found no erratum for the J. Aust. Math. Soc. 117 paper.

## The input Props against the published statements

**Chirre–Hagen Thm 3.** Checked against arXiv 2512.23534v1 *and* the published Res. Number Theory 12, art. 82 (14 Aug 2026), read through the Mac Chrome.
- Published: "Assume RH. Then, for x ⩾ 10^13 and δ ∈ (0,10^−13] we have J_θ(x,δ) ⩽ 2.5571·δ log²(2.0001/δ) x²". Here J_θ(x,δ) = ∫_1^x (θ((1+δ)y) − θ(y) − δy)² dy, from (1.1).
- Lean `SelbergBound`, which `Iff.rfl` confirms is identical to theorem_1_1's inline hypothesis: `∀ Y d : ℝ, 10^13 ≤ Y → 0 < d → d ≤ 1/10^13 → ∫ v in 1..Y, (Chebyshev.theta ((1+d)*v) - Chebyshev.theta v - d*v)^2 ≤ (25571/10000)*d*Y^2*Real.log ((20001/10000)/d)^2`.
- Mathlib's θ is Σ_{p ≤ ⌊x⌋} log p. Every quantifier, the range [1, Y], θ (not ψ), the log argument, and ≤ match. Only RH is assumed.

**Chirre–Hagen Thm 2** (used for the ψ-route variant). Journal text is identical to arXiv: x ≥ 10^13, δ ∈ (0, 10^−13], J_ψ ≤ 2.2258·δ log²(2.0001/δ) x². `PsiAtFactors` asks for this only at Y ∈ {2N, 2N/3}, δ = 512L²/N, which is weaker than the theorem.

**Cully-Hugill–Dudek Thm 1.** Checked against arXiv 2206.00433v2 (Aug 2023, before the 19 Sep 2023 online publication). Chirre–Hagen restate it the same way. The journal full text is paywalled; its abstract matches.
- Published: "Assuming RH, for all x ≥ 10^8 and any δ ∈ (0, 10^−8] we have ∫_1^x |θ(y+δy) − θ(y) − δy|² dy < 202δx² log² x".
- Lean `CullyDudekBound`: `∀ Y d, 10^8 ≤ Y → 0 < d → d ≤ 1/10^8 → Jtheta Y d < 202*d*Y^2*(Real.log Y)^2`. Exact match, strict inequality included. Only RH is assumed.

**Siebert.** Lean: `∀ (y:ℝ) (d:ℕ), 1 < y → 0 < d → Even d → #{p ∈ primesLE ⌊y⌋ | (p+d).Prime} ≤ 16*(∏' p, twinFactor p)*y/(log y)^2 * ∏_{p ∈ d.primeFactors, 2<p} (p−1)/(p−2)`, where twinFactor p = 1 − 1/(p−1)² on odd primes and 1 otherwise. This matches TME-EMT with a = 1, b = d. The project proves `HasProd twinFactor (⨅ partial products)`, and the infinite product is only ever used through its bound by a partial product.

**PNT.** Lean: `Tendsto (fun y => #primesLE ⌊y⌋ * log y / y) atTop (𝓝 1)`. This is the true prime number theorem, so it costs nothing.

**FC check.** The project's `Catalog` is exactly the Formal Conjectures statement `erdos_462` (natural x, all integers). `catalog_of_selberg : SelbergBound → Catalog` passes the axiom audit.

## Lean replay

Toolchain v4.33.1. Mathlib 0df444a is the tagged release v4.33.1, so the cache was used. Builds ran under nice with 4 threads.

| Step | Exit | Result | Log greps (error / sorry / declaration uses / kernel / mismatch) |
|---|---|---|---|
| `sha256sum -c SHA256SUMS` | 0 | 34/34 OK (checks the package against itself only) | — |
| elan install | 0 | — | — |
| targeted `lake exe cache get` | 0 | 3152 files | — |
| `lake build` | 0 | 3193 jobs; only the 25 `Erdos462.*` modules compiled; 3:26, peak 3.6 GB | 0 hits, no warnings |
| `lake env lean Audit.lean` | 0 | 105 lines, every one exactly `[propext, Classical.choice, Quot.sound]`, no other output | only false hits on the identifier `squareError` |
| `lake env lean --run ReplayProofs.lean` | 0 | "Project declarations: 361 / Transitive declarations: 54397 (including 41661 theorem bodies) / Fresh kernel replay passed." 5:52, 3.7 GB | 0 hits |
| My `MyAxioms.lean` | 0 | see below | 0 hits |
| `LEAN_NUM_THREADS=1 lake env leanchecker --verbose Erdos462` (not fresh) | 0 | 25 "replaying Erdos462.*" lines | 0 hits |

My file printed `#print axioms` for theorem_1_1, composite_sum_384, cully_dudek_wide_interval, theorem_1_2_lower, theorem_1_2_upper, erdos_462_composites and erdos_462_as_printed. All seven give exactly [propext, Classical.choice, Quot.sound]. The full types are printed in `myaxioms.log`:
- theorem_1_1: hypothesis ⇒ ∀ x ≥ 96·10^36, ∃ S, every n ∈ S is pq with x < n < x + 384√x(log x)² and √x/2 < q < √x < p < 3√x, |S| ≥ (14/3)√x, and Σ minFac/n ≥ 14/9.
- theorem_1_2_upper: SiebertBound ⇒ ∀ C > 0, eventually composite sum ≤ 20 + 2595840C.
- theorem_1_2_lower: CullyDudekBound → SiebertBound → PrimeNumberTheorem → ∀ C > 0, ∃ c > 0, eventually c ≤ composite sum.
- The two `Iff.rfl` examples compiled, confirming the input Props unfold to the published forms quoted above.

Cleanup: `.lake` deleted (3.6 GB); logs kept in /tmp/e1122/seatH/. The toolchain stays installed because 8 other workspaces pin v4.33.1, including ~/.cache/erdos-sources/formal-conjectures.

The author's `verify.py`: full mode exits 1 because z3 is not installed. `--incidences-only` exits 0 and its output matches the expected lines. This is the author's own tool, not an independent check.

## Not checked

- Siebert 1976 in the original (paywalled).
- The full journal text of Cully-Hugill–Dudek (paywalled); I used arXiv v2.
- The correctness of the published Chirre–Hagen and Cully-Hugill–Dudek proofs themselves; they are taken as given.
- `leanchecker --fresh` and `verify-lean4lean.sh` (not run). Non-fresh leanchecker re-checks only the project's modules; the Mathlib .oleans are trusted. `ReplayProofs.lean` is the author's script, though it uses Lean's stock `Lean.Replay`.
- Intro attributions (Tao's comment, Zeraoulia, the Erdős–Graham wording) were not checked, because checking them would mean fetching erdosproblems.com (the wall).
- Prior art: Zhang (arXiv 2608.24930v2) gets the answer only under a stronger "bounded-fluctuation" hypothesis, and his mean of 4C sits between the paper's bounds. That fits this being new under RH alone, but I did not run a full novelty search.