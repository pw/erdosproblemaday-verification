# Seat L report — §9 (pp. 74–79) + global assembly; Part B: the Lean's literature inputs (both Lean routes)

STATUS: FINAL (Part A complete; Part B complete incl. route M dependency trace, B.4)

## 1. VERDICT
- **Part A (§9 and the deduction of Thm 1.1): HOLDS AS READ.** Every display (9.1)–(9.21) re-derived by hand; every earlier
  result §9 invokes is used inside the range and with the parameter order in which it is stated. No objection above EXPOSITION.
  (Conditional, as §9 itself is, on Prop. 7.1 = (7.17)/(7.18), on (7.6), (7.13) and Lemma 8.1 = (8.8), which are other seats' scope;
  I checked only that their *statements* match their use.)
- **Part B (Lean inputs): route C (`OAI.NumberTheory.Ostmann.Complete`) formalizes every analytic input the paper cites, in the
  paper's own form**, each as an explicit hypothesis later discharged by a proved `theorem`/`def`; 0 axioms/sorry in either route.
  **Route M (`OAI.NumberTheory.Ostmann.Main`, comparator `OstmannPrimes`) is a different proof that is NOT a formalization of the
  paper's analytic inputs: it imports a formalized "no Landau–Siegel zeros" theorem**
  (`WeightedTorusJets.dirichlet_real_zero_bound`: `c ≤ (1-β)·log q` for every real zero of every primitive real character),
  which the paper never uses (its Remark 5.4 explicitly declines the companion QRH result). See B.4 — this matters for the public page.

## 2. Objections
None at FATAL / GAP / FIXABLE level in §9. EXPOSITION only:

E1 (EXPOSITION, p. 74, (9.1)). "There are only exp(O_k(1)) ways to choose and pair the two partitions of the leaf sets into these
components." True (r ≤ 2^k), but the displayed bound (9.1) then reads as if the factor (m!)^r e^{(¼log r+C)rm} alone bounds N_bad;
for tiny m it does not (r=4, m=1: N_bad = 24 > 10.9), the e^{O_k(1)} pairing factor is what carries it. The proof is right; the
sentence order makes the O_k(1) look cosmetic. Brute-force check below.

E2 (EXPOSITION, p. 76, (9.6)/(9.8)). "for every sufficiently large fixed k and then sufficiently large L" — the reason k must be
large here is only that the constant C of (9.4) is asserted uniform "once k and then L are sufficiently large" (§7.1, p. 54); worth
one clause, since the reader otherwise looks for a k-dependence in (9.7) and finds none.

E3 (EXPOSITION, Remark 5.4 vs Lean). The paper says the proof "uses the classical estimate of Lemma 5.3, not this zero-free theorem"
— true of the paper and of Lean route C, false of Lean route M (B.4). A public page should not cite route M as "the paper, formalized".

## 3. What I checked and how

### 3a. Earlier results §9 invokes — statement vs. use
| §9 use | invoked result (printed) | hypotheses at point of use |
|---|---|---|
| (9.3) bad diagonal matchings | (7.17) one-assignment bound, diagonal environment, l=j−1, r=r_j | 𝒢 = (7.14) with v=s ✓; K_ar dropped (single assignment) ✓; external measure (7.16) bounded mass ✓ |
| (9.3) point-probability extraction | (7.15) C_H ≤ L^{−r_jm}e^{Cr_jm+O_k(1)}; (7.7) T_H = G + r_jw_j + Δ_j | on simultaneous support only ✓ (used after the |A1 Ā2| ≤ (|A1|²+|A2|²)/2 split, both squares) |
| (9.4) good matchings | (7.18), diagonal environment, l=j−1≥2, ≤3r_j/4 components, with K_ar | exactly the factor K_ar of §7.4 arises from exact extraction ✓; count (r_jm)!L^{−r_jm} = e^{O_k(m)} ✓ |
| (9.8)–(9.11) transfers | (7.13) e^{−c_g}|η_{j−1}|² ≤ D_j + η_j, η_j real | ✓ |
| (9.11) start | (7.6) |η_0| ≥ e^{−B_*m}, B_* independent of B_D,B_z,k and valid for all large B_s | order B_s → B_* → B=B_*+3 → B_z≥9 → B_D → k → L ✓ |
| (9.15) | Lemma 8.1 (8.8), giant row (a0,a1,μ,δ')=(.049,.95,.012,.018) | log p ∈ [e^{.05L},e^{.9L}] ⊂ [e^{.049L},e^{.95L}] ✓; log C = O_k(h+m e^{.006L}) ≤ e^{.012L}=e^{μL} ✓; a ∈ U_C ✓; ε_L = exp(−c e^{.018L}) matches δ' ✓; exceptional term kept, multiplier in [0,2] ✓ |
| (9.13)–(9.14) | g_ℓ(0)=0, ℓ^{−1}Σ|g_ℓ|²=1 (Cor. 4.2 def. of F_p,g_p, p. 34; restated end of §6) | F_p centred and L²-normalised ⇒ both identities hold exactly ✓ |
| (9.19) | (7.17),(7.18) final environment, l=k, 𝒢=1, K_ar=1 | pairs differ only by bulk permutation, nonbulk and d common ✓; (7.18) "uniform in permutations" ✓ |
| (9.17) | exchangeability of iid bulk priors (§7.2: identical priors, same deletion ℰ_L) and invariance of G_R | ✓ (G_R depends only on the set of prime values) |

### 3b. Line-by-line re-derivations (all correct)
- (9.1): a log a ≤ (a−1)(log r+1) for 1≤a≤r (uses log a ≤ a−1 and a ≤ r); (am)! ≤ (m!)^a a^{am} (multinomial); Σ(a_i−1)=r−t<r/4.
- (9.2): (m!)^r/(rm)! ≤ m^{rm}e^{rm}/(rm)^{rm} = e^{rm}r^{−rm} ⇒ exp((−¾log r + C+1)rm + O_k(1)).
- (9.3): (m!)^{r_j}L^{−r_jm} ≤ (m/L)^{r_jm} ≤ z^{r_jm} since m=2⌊zL/2⌋ ≤ zL.
- (9.7): −Δ_j/(r_jm) + Δ_0/m + log z + ¼log r_j = B_s−B_D+(9−B_z)log z −(3/20)log r_j. With (9.6) this is ≤ −(2B+6)+C−C ⇒ (9.8).
- (9.9): c_g ≤ .91L, m = k⁴L+O(1) ⇒ (c_g+log2)/m ≤ 2/k⁴ for large L.
- (9.10)/(9.11): hypothesis |η_{j−1}| ≥ e^{−Br_jm} ⇒ ½e^{−c_g}|η_{j−1}|² ≥ e^{−(2B+3)r_jm} ≥ D_j iff 3r_jm ≥ c_g+log2 ✓; recursion
  −log|η_j| ≤ c_g+log2 + 2(−log|η_{j−1}|) gives 2^jB_*m + (2^j−1)(c_g+log2) < (B_*+3)2^jm ✓; sharper bound at j−1 supplies the coarse
  hypothesis at j ✓ (no "reserve spent per step").
- (9.12)–(9.16): Σ_{a∈U_C}F(a) = Π_ℓ(ℓ−|g_ℓ(0)|²) = C; C/φ(C)=1+o_k(1) (O_k(m) primes ≥ exp(exp(.004L))); summed progression error
  O(Z_G^{−1}Cε_L) with Z_G^{−1}=e^{O(L)}, log C ≤ e^{.012L}, ε_L = exp(−ce^{.018L}) ⇒ o(1); a_ℓ units since 0<|s|≤V_k < every slot prime.
  Pointwise use of the [0,2] multiplier makes any χ_*–F correlation harmless ✓.
- (9.20): Σ_{j≤k} r_j log r_j = log2·((k−2)2^k+2) = r log r −2r log 2 + 2 log 2 ✓; Δ_0/(rm) ≤ B_s+8log z (deliberate weakening).
- (9.21): −¾ + 2/5 = −7/20; log z coefficient (B_z+8)+8 = B_z+16; B_s coefficient 2 ✓. k chosen last among constants
  (log r = k log 2 vs log z = 4 log k) ✓; second term e^{E_k−ω_k(m)} → 0 faster than any e^{−Cm} since E_k = O_k(m) ✓.
- Contradiction: |η_k|² ≤ e^{−(2B+1)rm} vs (9.11) |η_k|² ≥ e^{−2Brm} ✓.
- "For most p" → "for all p": none in §9. The only average over primes ((9.16)) is used as an average (Cauchy–Schwarz input (9.18)),
  never pointwise. The spectator "most primes" restriction was built into the prior in §7 (Cor. 4.2 subset), not passed through §9.
- Deduction of Thm 1.1: Lemma 2.2 (finite summand ⇒ B(Y) ≪ Y/(log Y)² by Lemma 2.1 with the two shifts from A, contradicting
  π(Y) ≤ |A|B(Y)+O(1)) + Thm 2.3 ⇒ Thm 1.1 ✓. Lemma 2.1's Markov step (E log u = (1/10+o(1))log Q ⇒ ≥9/10 of weight has u ≤ Q) ✓.
  Lean: route C `PaperMain.lean` derives both statements; comparator challenge statements (`ComparatorChallenges/OstmannComplete.lean`,
  `OstmannPrimes.lean`) are faithful: ℕ = N₀, `Nat.Prime` = positive primes, `EventuallyPrimeSumset` ⇔ finite symmetric difference.

### 3c. Numerics (script `L_work/checks.py`, `L_work/checks2.py`; each with a control that fails)
- Σ r_j log r_j identity, k=1..14: exact; perturbed constant (log 2 instead of 2 log 2) fails.
- a log a ≤ (a−1)(log r+1), all 1≤a≤r<300: holds; weaker (a−1)log r: 1,593 violations (control).
- (am)! ≤ (m!)^a a^{am}: holds a≤7, m≤14; (am)! ≤ (m!)^a fails for a>1 (control).
- Brute-force N_bad vs the structure sum Σ_{t>3r/4}Π(a_im)! of the (9.1) proof: r=4,m=1: 24 ≤ 24; r=4,m=2: 384 ≤ 384 (tight);
  r=8,m=1: 40,320 ≤ 1,169,280. Control: total arrangements 40,320 > 384 for r=4,m=2 (the bound is specific to bad pairs).
- CRT identity (9.14) with centred, L²-normalised random F_ℓ (ℓ=5,7,11, C=385): Σ_{a∈U_C}F(a) = 385.000000; control with an
  un-centred (g(0)≠0) test: 72.0 ≠ 385.

## 4. What I could NOT check
- Prop. 7.1 (§8), (7.6), (7.13) and Lemma 8.1 themselves (other seats). Montgomery 1969 / Inoue 2021 Lemma 1, FGKMT Lemma 7.1,
  Heath-Brown 1995 Thm 1, MV Cor. 11.20 were not opened (no source access here); their *Lean* versions are proved (Part B), so the
  question "does the cited source say this" is moot for route C's correctness, but I did not verify the citations' theorem numbers.
- Route M was not checked against the paper beyond module/statement level; I did not verify that the Lean's no-Siegel-zero proof is
  sound mathematics (it is kernel-checked per the brief; that is all I can say).

## 5. Where a hole is most likely to hide in my scope
The parameter order: B_D must beat the constant C of (9.4), which must not depend on k, B_D, B_z, B_s, yet the bad-diagonal bound
(9.3) carries C_H's cell normalisations e^{O(kr_jL)} and the r_j-dependence of (7.17). Both are absorbed into e^{Cr_jm} only because
m ≍ k⁴L (kL ≤ m/k³), and the ¼log r_j from counting is beaten by the .4 log r_j built into Δ_j, leaving −(3/20)log r_j ≤ 0. I
re-derived each absorption and found them consistent; the hole would have to be in §8's proof that Prop. 7.1's C is k-uniform,
which is outside §9. Within §9 I believe it holds.

---

# PART B — the Lean's literature inputs

## B.1 Route C chain (comparator `OstmannComplete`, solution `OAI.NumberTheory.Ostmann.Complete`)
`Complete.twoInfiniteSummandsImpossible / inverseGoldbach`
→ `MainWithoutQuadraticSieve` (`publishedComplexZeroDensity`) → `MainWithoutSiegel` (`publishedQuadraticLargeSieve`)
→ `MainWithoutSummandSize` (`publishedSiegelBound`) → `MainWithoutAdditiveSieve` (`publishedSummandSizeBound`)
→ `MainWithoutProgression` (`publishedAdditiveLargeSieve`) → `MainActualProgression` (`actualProgressionTheta`)
→ `Preliminaries/ReducedPublishedInputs.…_without_real_zero_input` (`progressionInput_of_actual_theta`, `actualComplexZeroRegion`,
`exists_actual_real_low_height_region`, `actualPublishedRealZeroInput`, `faithfulCharacterZeroEquiv`, `actualSmoothExplicitFormula`,
`P0.mertens`, `P0.smoothPrincipalPNT`, `publishedBonamiBound`)
→ `Construction/ConditionalMain.twoInfiniteSummandsImpossible_of_published` (the paper's argument, hypotheses = the 12 inputs below).
`MainWithoutPage.lean` / `PublishedProgressionEstimate` is imported but NOT on this path (a side variant).

## B.2 Token audit
Over all modules in both closures (route C 3,242; route M 4,385; incl. PNT+, StrongPNT, AINTLIB sources), comment-stripped grep for
`axiom`, `sorry`, `admit`, `native_decide`, `implemented_by`, `@[extern`, `unsafe`, `csimp`, `opaque`, `ofReduceBool`: **0 hits**
(the only textual matches are two docstrings saying "not a global axiom"). Positive control: a planted file with `sorry`, `axiom`,
`@[implemented_by]` → all three caught. Whole trees Ostmann (7,716 files) + Jacobsthal (819) + PrimeGaps (56): 0 hits as well.
Every discharging term below is a `theorem` or a `noncomputable def` with a body. The comparator JSONs permit only
`propext, Quot.sound, Classical.choice`, which is the stronger guarantee; my grep is corroboration.

## B.3 Route C input table
| # | Lean input (file) | Plain statement | Literature / strength | Paper cites? | Discharged by |
|---|---|---|---|---|---|
| 1 | `PublishedProgressionInput` (ZeroDensity/PublishedProgressionInputs) | data κ,c>0, C≥0, a choice of ≤1 primitive real zero (χ_e,β) per modulus with cond(χ_e)|q; *complete*: any such zero with β ≥ 1−κ/log 4q is the chosen one; *unique*: for Q≥2 at most one primitive real zero with cond ≤Q, β ≥ 1−κ/log 4Q; *theta*: ∀q≥1, (a,q)=1, x≥2: \|θ(x;q,a) − (x − χ_e(a)x^β/β)/φ(q)\| ≤ C x exp(−c√log x) | MV Thm 11.3 + Cor 11.10 (Page) + Cor 11.20 (11.32/11.34): de la Vallée-Poussin error, exceptional term retained, no Siegel; uniform in all q (trivial beyond e^{c√log x}) | Yes: Lemma 8.1 (p. 66) cites MV 11.3, 11.10, 11.16, 11.17/11.20 — paper derives (8.8) via zero-free region+explicit formula; Lean takes Cor 11.20 directly. Sufficient for both rows of (8.7) (μ < a0/2, δ' < a0/2) | `progressionInput_of_actual_theta actualProgressionTheta` (ActualProgressionInput def; ActualThetaEstimate thm), `actualLocalZero_complete`, `actualPage_unique` |
| 2 | `PublishedSmoothExplicitFormula Z` | for ONE fixed test φ=`primeMeanTest` (supp [5/8,7/8]): Mellin decay ≤C(1+\|t\|)^{−8} on −½≤σ≤2; Σ_{χ∈F}N_χ(0,T) ≤ C Q²(T+1)log(Q(T+2)) for any finite family of primitive nonprincipal χ, cond ≤Q; Σ_n Λχφ(n/X) + Σ_ρ X^ρΦ(ρ) + [χ even]Φ(0) = O(log(2q)/√X) | MV Ch. 10 / Helfgott §3.7.1, 3.7.3; special form (single fixed test) | Yes, Lemma 5.3 proof, eq. (5.x) "supply-smoothed-explicit" — same form | `actualSmoothExplicitFormula faithfulCharacterZeroEquiv` (SmoothActualExplicitFormula) |
| 3 | `PublishedComplexZeroDensity Z` | ∃C ∀Q≥1,T≥2,½≤σ≤1, finite F of primitive nonprincipal χ, cond ≤Q: Σ_{χ∈F}N_χ(σ,T) ≤ C(Q²T)^{3(1−σ)/(2−σ)}(log QT)^{13} | Montgomery 1969 Thm 1 as in Inoue 2021 Lemma 1: Ingham–Montgomery exponent 3(1−σ)/(2−σ), **not log-free**, log-power 13 | Yes, Lemma 5.3, identical form | `publishedComplexZeroDensity` (ComplexDensityProof thm; actually proves (log)^{10} for σ ≥ ½+1/log Q²T, trivial count below) |
| 4 | `PublishedComplexZeroRegion Z` | ∃c ∀Q≥101,T≥2 ∃ at most one exceptional primitive character, all other zeros (cond ≤Q, \|γ\|≤T) have 1−β ≥ c/log(2QT) | Landau–Page at bounded height, FGKMT Lemma 7.1 (whole exceptional character deleted) | Yes, Lemma 5.3, same form | `actualComplexZeroRegion` (via `exists_actual_page_uniqueness`, `complexZeroRegion_of_page`) |
| 5 | `PublishedSmoothPrincipalPNT` | ∃C,c: \|Σ_nΛ(n)φ(n/X) − X∫φ\| ≤ CX exp(−c√log X), φ = the fixed test | classical PNT with dlVP error, q=1 of MV Cor 11.20, smoothed | Yes ("classical PNT with its zero-free-region error", Lemma 5.3), no citation | `P0.smoothPrincipalPNT` (ProgressionPrincipalPNT thm) — derived from input 1 |
| 6 | `PublishedRealZeroInput P` | per primitive real χ: a multiplicity enumeration of zeros with Hadamard identity \|Σ_ρ Re 1/(s−ρ) − Re L′/L(s,χ) − ½log q\| ≤ C on 1<s≤2; low-height region: ≤1 real zero with β ≥ 1−κ/log 4Q, all others with \|γ\|<1 have β ≤ 1−κ/log 4Q | Helfgott §3.7.4 (3.97)–(3.102) + MV 11.3/11.10 | Yes, §3 (Lemma on (3.x) "quad-log-derivative") cites exactly these | `actualPublishedRealZeroInput P (exists_actual_real_low_height_region …)` |
| 7 | `PublishedSiegelBound` | ∀ε>0 ∃C: every real zero β∈(0,1) of a primitive nonprincipal real χ mod q has (1−β)^{−1} ≤ Cq^ε | **Siegel's theorem, full ineffective form** (MV Cor 11.15) | Yes, §3 cites MV Cor 11.15 | `publishedSiegelBound` (SiegelBoundProof) ← `LargePrimeGaps.quadratic_siegel` (PrimeGaps/SiegelBounds: L(1,χ) ≥ c_ε(q+1)^{−ε}) |
| 8 | `PublishedBonamiBound` | finite P, l≥1, real a_Q: E_ε\|Σ_Q a_QΠ_{p∈Q}ε_p\|^{2l} ≤ (Σ_Q(2l−1)^{\|Q\|}a_Q²)^l | Bonami 1970 Ch. III Thms 2–3, (2,2l) hypercontractivity on the cube, full strength for these exponents | Yes; paper also proves it inline | `publishedBonamiBound` (Characters/BonamiInput) |
| 9 | `PublishedSummandSizeBound` | for infinite A,B with A+B eventually = primes: ∃a,C,N₀: a√N/(log N)³ ≤ \|A∩[0,N]\|,\|B∩[0,N]\| ≤ C√N(log N)² | Elsholtz 2006 Thm 1.9 consequence — exactly Lemma 2.4 | Yes, cited and reproved (Lemma 2.4) | `publishedSummandSizeBound` (Preliminaries/SummandSizeProof) |
| 10 | `PublishedAdditiveLargeSieve` | M consecutive integers, Q≥1: Σ_{q≤Q}Σ_{(h,q)=1}\|Σc_n e(hn/q)\|² ≤ (M+Q²)Σ\|c_n\|² | Montgomery–Vaughan 1973 Thm 1 (M−1+Q² weakened to M+Q²; constant 1, stronger than paper's ≪) | Yes, (2.1) | `publishedAdditiveLargeSieve` ← `separated_additive_sieve` (Preliminaries/SeparatedAdditiveSieve) |
| 11 | `PublishedQuadraticLargeSieve` | ∀ε ∃C ∀M,N≥1, b: Σ_{m≤M odd sqfree}\|Σ_{n≤N odd sqfree}b_n(n/m)\|² ≤ C(MN)^ε(M+N)Σ\|b_n\|² | **Heath-Brown 1995 Thm 1, full statement** | Yes, §3 (3.x) "quad-heath-brown", same form + paper's signed extension | `publishedQuadraticLargeSieve` (Quadratic/QuadraticSieveProof, exponent descent 1+1/(r+1)) |
| 12 | Mertens `MertensEstimate`/`MertensHarmonicEstimate` | classical Mertens | — | used throughout | `P0.mertens` (MertensFromProgression) — derived from input 1 |

Paper black-box citations that are NOT inputs (so proved inline or avoided): MV Appendix D.2 (periodic Poisson — Lean Poisson
modules), Rota 1964 (partition Möbius inversion), MV Thms 9.6–9.7 (|τ(χ)|=√q — Lean Gauss-sum modules + AINTLIB
BernoulliRegular.GaussSum), Green–Harper (2.1)/Lemma 2.4/Lemmas 6.1–6.2/Prop 3.1 (motivational), Gallagher's larger sieve (inline in
both), Kneser 1953 / DeVos Thm 1 (§4: **not formalized anywhere**; route M replaces it by an elementary doubling-cover lemma
`Characters/DenseAdditiveCoverage.exists_ordered_sum_cover`; route C's closure contains neither, so route C's §4 avoids this step —
location not traced), Gowers / Babai–Nikolov–Pyber / Gill (§6, comparison only; the paper proves its operator bound directly),
Schwartz–Zippel–DeMillo–Lipton (§8, paper proves its nonuniform variant), Laffer–Mann Thm 12 (Lemma 2.2 reproved), MV Thm 11.16
(subsumed by input 1), OpenAIQRH2026 (Remark 5.4, optional — not used by the paper or route C).

## B.4 Route M (comparator `OstmannPrimes`, `Ostmann.Main → Corollaries → Result.lean`)
- `Result.main := assemble_from_infinite_case Conclusion.actual_no_decomposition`. `assemble_from_infinite_case` takes one
  hypothesis (∀ d : Decomposition, False), discharged by `actual_no_decomposition`, which is `∀ _d : Decomposition, False` with
  NO hypotheses (`no_decomposition_of_actual_four_comparison_providers 17 17` applied to four `theorem` providers). Clean.
- Structure: its `Conclusion/` directory (71 modules) mirrors §9 file by file (BadArrangementCount, BadFraction, ComponentFactorials,
  OverlapComponents, TransferRecurrence, RegularNorm*, PermutationSymmetrization, FinalRateAbsorption, ParameterChoice), so route M
  follows the paper's §§2–9 architecture, but with **different analytic inputs**, all proved inline: its own Heath-Brown sieve
  (`Ostmann/QuadraticSieve*`), Siegel (`PrimeGaps/SiegelBounds`, `Reuse/SiegelNearOne`), Strong PNT (StrongPNT `PNT5_Strong`),
  Mertens (PNT+ `Erdos970.MertensClassical`), a smoothed explicit formula (`Ostmann/Dirichlet/SmoothedExplicit*`), and a **weaker**
  zero-density estimate (`ZeroDensity/Density.exists_actual_zero_density_constant`: (Q²H)^{10(1−σ)}(1+log QH)^{11}), plus
- **the decisive difference**: `Jacobsthal/Siegel/DirichletRealZeroBound.dirichlet_real_zero_bound` (105 `Jacobsthal.Siegel` modules,
  namespace `WeightedTorusJets`): ∃c>0 ∀q≥3, primitive real χ mod q, real zero β∈(0,1): c ≤ (1−β)·log q — i.e. **no Landau–Siegel
  zeros**, a famous open problem in the published literature (cf. the paper's bib entry OpenAIQRH2026, "The Quasi-Riemann
  Hypothesis: a zero-free half-plane Re s > 7/8", OpenAI preprint 30 Sep 2026). It feeds `Jacobsthal/Estimates/PrimitiveTransfer`
  (zero-free disk |s−1| ≤ c/log q, no exception) → `Primes/DirichletZeroFree` (1−c/(log q+log(|t|+6))² region for ALL nonprincipal
  χ) → `Sieve/LargeModulusSiegelWalfisz.large_modulus_siegel_walfisz` (π(X;q,r) = Li(X)/φ(q) + O(X e^{−c(log X)^{1/3}}) for
  q ≤ e^{c(log X)^{1/3}}, **no exceptional term**) → `Ostmann/PrimeProgression/CountToHarmonic` → `Arithmetic/PrimeCellReplacement`
  → `Conclusion/RegularNormAP` (route M's version of (9.15)); also `Ostmann/Reuse/SiegelGap`, `Dirichlet/QuadraticZeroFreeSharp`,
  `Dirichlet/LogZeroFree`. Sanity argument (mine) that this input is genuinely stronger than anything classical: the large-modulus SW
  statement with absolute error, applied at log X = (2u/c)³ with q₁=e^u carrying a real zero, forces 1−β ≫ (log q₁)^{−2} for all large
  q₁ — beyond Siegel (≫_ε q^{−ε}). Route C (0 Jacobsthal / 0 Erdos970 modules in its closure) does not depend on any of this.
- **The no-Siegel-zero theorem is on route M's proof path, not merely imported.** Textual reference-graph BFS over the 22,139
  declarations of route M's closure (`L_work/path.py`, output `L_work/path_M.txt`), every link then confirmed by hand (each caller's
  body names the callee): `actual_no_decomposition` → `no_decomposition_of_actual_four_comparison_providers` →
  `false_of_actual_four_comparison_providers` → `exists_actual_comparison_obstruction(_interface)` →
  `initial_amplitude_construction(_actual/_interface)` → `initial_source_construction(_separated)` → `actual_positive_giant_prior`
  (Construction/GiantSourceProducer) → `nonsparse_supply` (Supply/NonsparseSupply = route M's Prop. 5.1) →
  `eventually_actualPrime_weight_large` → `ZeroDensity/SupplyPrimeError.eventually_totalPrimitivePrimeError_supply` (route M's
  Lemma 5.3: note its argument `totalPrimitivePrimeError Q none …` — exception = `none`, i.e. ALL primitive characters of conductor
  ≤ Q, no exceptional character deleted) → `…SupplyErrorAssembly` → `…LiteralSupplyZeros` → `…SupplyZeroDecay` →
  `ZeroDensity/WeightedPowers.exists_unconditional_zero_power_constants` → `ZeroFreeWeights.exists_unconditional_weighted_zero_constants`
  → `exists_actual_zero_gap_constant` → `Dirichlet/LogZeroFree.exists_nonprincipal_log_zero_free_region` (1−β ≥ c/(log q+log(|t|+6))
  for EVERY nonprincipal χ, no exception) → `Dirichlet/QuadraticZeroFreeSharp.exists_primitive_quadratic_log_zero_free_region` →
  `Jacobsthal/Estimates/PrimitiveTransfer.exists_primitive_real_zero_free_disk` → `Jacobsthal/Siegel/DirichletRealZeroBoundProof.
  WeightedTorusJets.dirichletRealZeroBound_proof`. So in route M the paper's §5 step (Lemma 5.3 omitting the Landau–Page character,
  then the one-prime deletion after it, p. 42) is replaced by a sum over all characters using an exception-free zero-free region
  — the shape of the paper's own Remark 5.4, but powered by no-Siegel-zeros rather than QRH. Caveat: the BFS is a textual
  over-approximation (short-name matching); the 25 links listed were each checked by reading the caller.
- One-sentence answer to the coordinator: route M follows the paper's §§2–9 architecture (its `Conclusion/` mirrors §9 file by file),
  but not the paper's analytic inputs: it uses an exception-free Dirichlet zero-free region derived from a formalized proof that
  Landau–Siegel zeros do not exist, a weaker (exponent 10(1−σ)) zero-density estimate proved inline, and a "large-modulus
  Siegel–Walfisz" with no exceptional term for (9.15); its final theorem `Conclusion.actual_no_decomposition` carries no hypotheses.

## B.5 Paragraph for the public page (proposed wording)
"Every analytic input the paper cites is formalized and proved in Lean in the solution module `OAI.NumberTheory.Ostmann.Complete`
(comparator *OstmannComplete*). The formalization was first built with these results as explicit hypotheses and each was then
discharged by a proof: the prime number theorem in progressions with Page's exceptional zero retained (Montgomery–Vaughan Cor.
11.20, with Theorem 11.3 and Page's Corollary 11.10), Siegel's theorem in its full ineffective form (Cor. 11.15), Montgomery's
zero-density estimate in the non-log-free form N(σ,T) ≪ (Q²T)^{3(1−σ)/(2−σ)}(log QT)^{13} summed over primitive characters
(Montgomery 1969 / Inoue Lemma 1), the bounded-height Landau–Page zero-free region (Ford–Green–Konyagin–Maynard–Tao Lemma 7.1),
a smoothed explicit formula and zero count for one fixed test function, the real-character Hadamard identity, Heath-Brown's
quadratic large sieve (1995, Thm 1, full statement), the Montgomery–Vaughan additive large sieve with constant M+Q², Bonami's
hypercontractive inequality, and Elsholtz's square-root size bounds; no axiom beyond Lean's standard three is used. Kneser's
theorem, cited in §4, is not formalized in either Lean route (the second route replaces that step by an elementary
doubling-cover lemma). A second, largely independent Lean proof (`OAI.NumberTheory.Ostmann.Main`,
comparator *OstmannPrimes*) follows the same architecture but replaces the exceptional-zero bookkeeping with a separately
formalized theorem that real primitive characters have no zero β with (1−β)log q < c (no Landau–Siegel zeros) — a result the paper
does not use; the first route does not depend on it."
