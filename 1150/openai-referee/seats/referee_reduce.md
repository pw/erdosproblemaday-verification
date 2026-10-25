# Referee report — seat `reduce` (family 076, sib1 "Asymptotically minimal maxima of real Littlewood polynomials")

Scope (verbatim): sib1 §1–§2 (pp. 1–4), §7 (p. 21), Appendix A (pp. 23–24), and the three contrary preprints
(refs/2504.21499, refs/2509.04212, refs/1609.03435v2) + Bonami–Révész refs/0707.3023; §1.1 prior-work sentences
(Erdélyi refs/2608.00744 Thm 2.1); Bloom's live-thread quantifier objection.

Status: COMPLETE (09:26Z). Verdict: HOLDS AS READ IN SCOPE (3 EXPOSITION notes, no FATAL/GAP).

## Scope read (pages)
sib1 pp.1–5 in full (pp.2–5 also as rendered PDF for every displayed formula: m_N, Thm 1.1, Prop 2.1 (1)–(2) with K_δ,
Lemma 2.2 (3), the proof of Thm 1.1 at the top of p.5); p.21 (§7, Cor 7.1 + proof) and pp.23–24 (Appendix A) rendered and read
line by line; pp.25–26 bibliography (version locators [6],[8],[9],[10],[11]). Spot-reads in §5 only to match the constants
(paper_plain l.1219–1264, 1438, 1560, 1636–1650) and the first lines of §6 (µ = 0 case, l.1765).
Contrary preprints read against their own text: 2504.21499v1 pp.1–9 (whole argument, Lemma 5, Eq. (27), final step);
2509.04212v1 pp.5–11 (definitions, Theorem 1, Cors 1–3 rendered, Lemma 1–5, start of proof); 1609.03435v2 §1, §2 (Eq. (2.1)),
§3 (definitions, Props 3.1–3.2, Theorem 3.3), first lines of the proof of Thm 3.3. Bonami–Révész 0707.3023v2 pp.1–6 (Defs 1–6,
Thms 5, 7, 8, Props 9, 10). Live thread /tmp/oaimath/076/live/thread1150.html (all 5 comments). Comparator
lean/AsymptoticallyMinimalLittlewood.lean + .json.

## Method
Read each sentence in scope against the rendered PDF; re-derived every inequality in the proof of Thm 1.1 and Cor 7.1 by
hand; quoted each contrary preprint's statement and the exact step OpenAI attacks from the preprint's own PDF/text (never from
sib1's paraphrase); re-checked Appendix A's three computations numerically (nice -n 19 python3 -I, exact rationals for the
2^{j²} example; script in /tmp/reduce_scratch/chk.py, outside the refs tree); fetched Erdős 1957 to settle the Problem 22
locator.

## Running notes

### [09:21Z] First pass: §2 proof of Theorem 1.1 and the comparator statement — no objection yet
- Theorem 1.1 (p.2) vs comparator `MainStatement` (lean/AsymptoticallyMinimalLittlewood.lean): the comparator is exactly the
  printed "Equivalently" form: ∀η>0 ∃N₀ (≥1) ∀N≥N₀ ∃ε:Fin N→ℝ, every ε k ∈ {−1,1}, ∀z with ‖z‖=1,
  ‖Σ_{k:Fin N} ε_k z^k‖ ≤ (1+η)·Real.sqrt N. "Length N" = N coefficients = degree N−1; √N is √(length). The `1 ≤ N₀`
  clause is harmless (N₀ can always be increased). Equivalence with lim m_N = 1: (⇒) minimum over the finite set {±1}^N is
  attained, so m_N ≤ 1+η gives a witness; (⇐) uses m_N ≥ 1 (Parseval). Correct.
- Lean statement ⇒ NO to #1150 (degree n, √n, "for all large n"): take N = n+1, η = c/2; (1+c/2)√(n+1) ≤ (1+c)√n once
  (n+1)/n ≤ ((1+c)/(1+c/2))². Every coefficient incl. both endpoints ε_0, ε_{N−1} is ±1, so the degree is exactly n and the
  constant term is nonzero. Lean gives ALL large n, stronger than the "infinitely many n" the negation needs. Correct.
- Proof of Thm 1.1 (p.5) line by line: liminf ≥ 1−7δ ⇒ eventually ≥ 1−8δ (δ>0) ✓; 1−|x| ≤ 1−x² on [−1,1] ⇒
  µ ≤ ½(N − ΣX²) ≤ 4δN ✓; d/du[u log(80N/u)] = log(80N/u) − 1 > 0 iff u < 80N/e ≈ 29.4N, so increasing on (0,N/2] ✓ (and
  µ ≤ N/2 always, 4δN < N/5); hence √(µ log(80N/µ)) ≤ 2√(δ log(20/δ))·√N ✓; triangle inequality
  P_ε(e(t)) = Q_X(t) + Σ(ε_k−X_k)e(kt) ⇒ m_N ≤ ‖Q_X‖∞/√N + C/√N + 2C√(δ log(20/δ)) ✓; limsup m_N is δ-independent, so
  bounding it by f(δ) for every δ∈(0,1/20) gives limsup ≤ inf f = 1 (K_δ→1, δ log(1/δ)→0) ✓. The "N→∞ then δ↓0" order is
  legitimate exactly because the left side does not depend on δ. µ=0 case: bound is C, consistent ✓.
- Constants as printed vs delivered: K_δ = √((1+δ)³/(1−δ)) (p.4, rendered PDF) is the same K_δ² = (1+δ)³/(1−δ) that §5
  closes with (paper_plain l.1219–1264, 1438, 1560); 1−7δ is delivered as (1−δ)(1−3δ)² = 1−7δ+15δ²−9δ³ ≥ 1−7δ (l.1646, arithmetic
  checked). Whether §§3–5 really deliver these is OTHER seats' scope; the reduction consumes exactly what is printed.

### [09:24Z] §7, Appendix A vs the preprints themselves, Bloom — checks done, no FATAL/GAP
- Cor 7.1 (p.21) line by line: f_N = |P_N(e(t))|/√N with P_N a minimiser; ∫f_N² = 1 (Parseval, probability Haar);
  1 = (∫f²)² ≤ ∫f⁴ ≤ ‖f‖∞²∫f² = m_N² → 1 ✓; ∫(f²−1)² = ∫f⁴ − 1 → 0 ✓; for u ≥ 0, |u−1|⁴ ≤ |u²−1|² since u+1 ≥ |u−1| ✓;
  p ≤ 4: Jensen/Hölder on a probability space, ∫|f−1|^p ≤ (∫|f−1|⁴)^{p/4} ✓ (incl. 0<p<1); p > 4: f ≥ 0 and f ≤ m_N give
  |f−1| ≤ max(1, m_N−1) = 1 eventually, so ∫|f−1|^p ≤ ∫|f−1|⁴ ✓. One family serves every p (minimisers do not depend on p).
  So YES: a one-sided sup bound (1+o(1))√N plus exact L² mass forces L^p-flatness for EVERY finite p>0 (and nothing at p=∞:
  no lower bound). Cor 7.1 is not used anywhere in §§2–6.
- Appendix A is independent of the proof of Thm 1.1 — CONFIRMED by grep of sib1/paper_plain.txt: refs [6],[8],[9],[10],
  eqs (45),(46) and Cor 7.1 are cited only on p.3 (§1.1, two sentences) and in App. A itself. Appendix A could be deleted
  without touching Theorem 1.1.
- A, opening para vs refs/1609.03435 (v2, 11 Jan 2017 — the version cited): Theorem 3.3 verbatim "There are no square
  L2-flat polynomials sequence from the class of Littlewood polynomials"; Eq. (2.1) class L = q^{-1/2}(ε0+…+ε_{q−1}z^{q−1})
  "where ǫ0 = ǫq−1 = 1" ✓ both endpoints +1; "square Lα-flat" = |Pn|² → 1 in L^α (§3) ✓. Fixing ≤2 endpoint signs changes the
  sup by ≤ 4, i.e. ≤ 4/√N normalised, L² mass unchanged, so the Cor 7.1 computation ∫(f²−1)² ≤ m_N² − 1 → 0 applies ✓.
  NOTE (not a defect): App. A does not locate the error in [8]'s proof; the conflict with [8] rests on Thm 1.1 alone.
- A.1 vs refs/2504.21499 (v1, only version) — read the whole proof (pp.6–9 of the preprint): Theorem 1 verbatim "There is
  no sequence from the class L which is L2p-flat, for any positive integer p > 1" ✓ (class L is q^{-1/2}-normalised ±1).
  Eq. (27): ∫_{(−δ,δ)}|2Q_q/√q|^α dx / ‖2Q_q/√q‖_α^α → 1 (Q_q the 0/1 polynomial), then "by taking α = 2p … and applying
  Lemma 5, we get a contradiction." Lemma 5 = Bonami–Révész c_{2k} ≤ 1/2. Against refs/0707.3023v2 itself: Def. 2 defines
  c_p as the sup of c such that FOR ANY symmetric nonempty open E SOME idempotent f has ∫_E|f|^p ≥ c∫_T|f|^p; just after,
  "c_p = inf_{a∈T} c_p(a)"; Theorem 7 gives 0.495 < c4 ≤ 1/2, 0.483 < c2k ≤ 1/2; after Proposition 9: "using the Dirichlet
  kernel that peaks at 0, we find full p-concentration at 0 for p > 1"; Proposition 10: c_{2k}(1/2) = 1/2 (the obstruction
  sits at 1/2, not 0). So (27) — concentration at neighbourhoods of 0 only — is a statement B–R already prove is TRUE for
  the Dirichlet kernel; it cannot contradict an upper bound on an infimum over all symmetric open E. OpenAI's (45) is a
  correct rewriting of Def. 2 (sup{c: ∀E ∃f ratio ≥ c} = inf_E sup_f ratio). The Dirichlet computation (|D_q| ≤ 1/sin(πd)
  off (−d,d); |D_q| ≥ 2q/π on |t| ≤ 1/(2q); ratio of tails ≤ sin(πd)^{-α}(π/2)^α q^{1−α} → 0 for α > 1) is correct, and the
  D_{⌊q/2⌋} remark answers (19) (density 1/2). Numerics (q=1000, d=.05, α=4): concentration ratio 0.99999997.
  DIAGNOSIS CORRECT. It is the same objection as Bloom's (live thread, 04 Feb 2026, "the final step of the proof on page 9
  does not contradict Lemma 5, since the latter is just about the existence of one function with concentration, rather than
  proving concentration for all functions"): page 9 of 2504.21499 is exactly (27)+"applying Lemma 5". el Abdalaoui's own
  16 Aug 2026 reply restates c_p with "for any symmetric non empty open set E" — which is precisely why (27) cannot reach it;
  the reply does not address the objection. OpenAI's version is the sharper one (explicit witness that the cited sets have
  B = 1).
- A.2 vs refs/2509.04212 (v1, only version), rendered PDF pp.6–7: Theorem 1 hypothesis verbatim
  Σ_{m≤n} a_m² ≤ (K/n²) Σ_{m≤n} m² a_m² "for some absolute constant K", (a_j)_{j≥1} ONE fixed real sequence, (c_j) unimodular,
  P_n = Σ_{j=1}^n a_j c_j z^j / (Σ a_j²)^{1/2}, conclusion "is not Lp-flat, for any p > 0" ✓ = (46). Counterexample
  a_j = 2^{j²}, c_j = 1: checked exactly in rationals for n ≤ 13 (Σ_{j<n}a_j²/a_n² ≤ (n−1)2^{−4n+2} ≤ 1, (46) with K = 2,
  Σ_{j<n}a_j/a_n ≤ (n−1)2^{−2n+1}); sampled sup||P_n|−1| = 3e−5 at n=8 → P_n is ultraflat hence L^p-flat for every p.
  Theorem 1 of [9] is FALSE as stated. Corollary 3's proof verbatim: "Littlewood's argument |Pn(z) − Pn(z′)| =
  ±{|Pn(z)|} ± {|Pn(z)|}, z, z′ ∈ S1, can be applied [28, p.307]" ✓ (second argument repeated, as OpenAI says); with z′
  restored, P=1+z, z=1, z′=i: LHS √2, candidates ±2±√2 = {3.41, 0.59, −0.59, −3.41} ✓ false. DIAGNOSIS CORRECT. Extra point
  OpenAI did not make: Cor 3 has an n-dependent array ε_n(k), so Theorem 1 (one fixed sequence (a_j),(c_j)) does not even
  apply to it; the corollary rests on the false identity alone.
- Conflict check: Cor 7.1 does contradict all three as printed: [10] Thm 1/Cor 1 (L^{2p}, L^α α≥4), [9] Cor 3 (L^α, every
  α>0, read with the L²-normalisation of its own intro), [8] Thm 3.3 (square-L², endpoint convention). [10] Cor 2 ("no
  ultraflat") is NOT contradicted by sib1 (no lower bound) — sib1 correctly does not claim it (p.23 "even though our maximum
  estimate supplies no uniform lower bound").

### [09:25Z] §1.1 prior-work sentences
- Erdélyi refs/2608.00744v1 Theorem 2.1 verbatim: "max_{t∈R} |Pn(e^{it})|² ≥ n + 1 + (1/38) n^{1/3} for every polynomial
  Pn ∈ Ln" (Ln = degree n, coefficients ±1). With N = n+1 this is sib1's ‖P‖∞² ≥ N + (N−1)^{1/3}/38 ✓ exactly; compatibility
  remark ✓ (extra term/N → 0). (His Thms 2.2–2.3 are also compatible with a one-sided (1+o(1))√N maximum.)
- Balister refs/1909.08777v1 Theorem 1: "|P<n(z)| ≤ √(6n−2) − 1 for all n ≥ 1 and |z| = 1", P<n = first n terms ✓
  (radical extent confirmed by the stated sharp case n = 3, z = 1: P<3(1) = 3 = √16 − 1). sib1's "√(6N−2) − 1 for its
  initial segments" ✓.
- Rudin–Shapiro √(2N) at dyadic lengths: mathematically standard (|P_t|²+|Q_t|² = 2^{t+1}); locator "[22, Theorem I and
  its proof]" COULD NOT FETCH Rudin 1959 (ams.org served a Cloudflare challenge; refs/rudin1959/NOTE.txt) — world seat.
- Hayman–Lingham refs/1809.07200: Problem 4.13 is the real-sign question (P = Σ_{k=1}^n ε_k z^k, ε_k = ∓1, "Is it
  necessarily true that C1 > 1 + A"); Problem 4.31 is the Erdős–Newman unimodular question and says "The weaker form of our
  conjecture stated that (4.6) holds if we assume ak = ±1 (Problem 4.13)" ✓ — supports "[15, Problems 4.13 and 4.31]" and
  "the distinction … is also explicit in [15, Problem 4.31]".
- Erdős 1957 (Michigan Math. J. 4, 291–300) — fetched the scan (refs/erdos1957/wfnmc.pdf, Project-Euclid id 1028997963,
  rendered p.297). Problem 22 verbatim: "If P(z) = Σ_1^n a_k z^k, where |a_k| = 1 for all k, then max_{|z|=1}|P(z)| ≥ √n, by
  Parseval's Theorem. Does there exist a universal constant c > 0 such that, for n ≥ 2, the maximum is at least (1+c)√n? I
  have an unpublished proof that if P(θ) = Σ_{k=1}^n ε_k cos kθ (ε_k = ±1), then max |P(θ)| > (1+c)√(n/2)." So Problem 22 is
  the UNIMODULAR question (= erdosproblems #230, as DanielChin said on the thread); its only ±1 content is about real cosine
  sums, a different object (real-valued, normalised by √(n/2)), not Σ ε_k z^k. → EXPOSITION finding E1 below.
- Georgiev–Gómez-Serrano–Tao–Wagner refs/2511.02864 §6.13 Problem 6.28: C⁺_{6.28}(n) = min_{p∈U_n} max_{|z|=1}|p(z)|/√(n+1)
  = m_{n+1}; AlphaEvolve "for n ≤ 100" ✓; "does not imply a definitive convergence" ✓. Context the paper does not mention
  (not a defect): GGTW report Odlyzko's 30 CPU-year numerics (n ≤ 100) "suggested that lim C⁺_{6.28}(n) ≈ 1.27" — Theorem
  1.1 says the limit is 1; consistent only with very slow, non-effective convergence, which is all the paper claims ("no
  useful convergence rate"). Side note: GGTW print the JKS constant as "6.340261…"; sib1's 6.342061… matches the largest
  root of 29x³−249x²+417x−27 (6.3420617…) — the cubic is from my memory of JKS, NOT checked against JKS (world seat).
- Downarowicz–Lacroix manuscript p.3 (cited for the naming): "the hypothesis on boundedness is called the Turyn's conjecture,
  or, equivalently, the Erdös L4-norm conjecture" ✓.

## Findings
No FATAL. No GAP. The reduction (§2) is a complete, correct deduction of Theorem 1.1 from Prop 2.1 + Lemma 2.2 AS PRINTED;
Theorem 1.1 is exactly the comparator's MainStatement and does negate #1150; Cor 7.1 is correct for every 0 < p < ∞;
all three Appendix A diagnoses are correct against the preprints themselves; Appendix A and §7 are not used by Thm 1.1.
The weight of Theorem 1.1 therefore sits ENTIRELY on Prop 2.1 (§§3–5: K_δ and 1−7δ for EVERY large N, not a subsequence)
and on Lemma 2.2 with an ABSOLUTE C (§6) — other seats' scopes.

E1 EXPOSITION (attribution), p.2, §1, lines 7–9 after the m_N display: "Erdős's original question allowed complex unimodular
coefficients and was refuted in that class by Kahane; the restriction to real signs is the question addressed here [12,
Problem 22]; see also [17] and [15, Problems 4.13 and 4.31]." Erdős 1957 Problem 22 (scan, p.297) is the |a_k| = 1 question;
its only ±1 statement is about real cosine sums Σε_k cos kθ normalised by √(n/2) (where Erdős claims the AFFIRMATIVE) — not the
analytic real-sign question. The locator is attached to the wrong clause; the real-sign question is Hayman–Lingham Problem
4.13 (already cited). Repair: move "[12, Problem 22]" to "Erdős's original question". No mathematical consequence.

E2 EXPOSITION (minor), p.4, §1.3: "A dyadic rounding procedure keeps the defect mass from increasing, which makes its total
loss o(√N) as the target error decreases." For fixed δ, Lemma 2.2 with µ ≤ 4δN bounds the loss by C + 2C√(δ log(20/δ))·√N —
a small MULTIPLE of √N, not o(√N); it is o(√N) only in the iterated limit (N→∞, then δ↓0). The formal proof on p.5 does this
correctly; only the overview sentence is loose.

E3 EXPOSITION (minor), p.3: "Appendix A examines specific issues in the contrary arguments." For [8] (1609.03435v2) Appendix A
examines no step of the argument — it only reconciles the endpoint convention (ε_0 = ε_{q−1} = 1) and lets Thm 1.1 + Cor 7.1
carry the conflict. Accurate as far as it goes; the sentence slightly oversells. (Optional strengthening for A.2: [9] Cor 3
concerns an n-dependent array ε_n(k), outside [9] Thm 1's single-fixed-sequence hypothesis, so Cor 3 rests on the false
identity alone.)

## External inputs checked (source, version, exact statement vs use)
- Comparator lean/AsymptoticallyMinimalLittlewood.lean: MainStatement = ∀η>0 ∃N₀, 1≤N₀ ∧ ∀N≥N₀ ∃ε:Fin N→ℝ, IsRealSigning ε ∧
  ∀z:ℂ, ‖z‖=1 → ‖Σ_{k:Fin N} (ε k:ℂ) z^k‖ ≤ (1+η)·Real.sqrt N — identical in content to the "Equivalently" form of Thm 1.1
  (length N, √length). (Textual identity with OAI's Model.lean and the kernel replay: lean seat / lean-build, not checked here.)
- 2504.21499v1 Thm 1, Lemma 5, Eq. (27), p.9 final step — quoted above; diagnosis correct; = Bloom's objection.
- 0707.3023v2 Defs 1–2, "c_p = inf_a c_p(a)", Thm 7, Prop 9 (+ the Dirichlet-kernel remark after it), Prop 10 — quoted
  above; (45) is a faithful rewriting of Def. 2; "full concentration at 0 vs uniform level" is in the source.
- 2509.04212v1 Thm 1 hypothesis = (46) verbatim; Cor 3's identity verbatim with repeated argument; both diagnoses correct.
- 1609.03435v2 Thm 3.3 verbatim; Eq. (2.1) fixes ε_0 = ε_{q−1} = 1 verbatim; "square Lα-flat" definition; fix correct.
- 2608.00744v1 Thm 2.1 verbatim; conversion n+1 = N exact.
- 1909.08777v1 Thm 1 verbatim (√(6n−2) − 1, all n ≥ 1).
- 1809.07200 Problems 4.13, 4.31 verbatim (support §1's citations).
- Erdős 1957 Problem 22 verbatim (scan) → E1.
- 2511.02864 §6.13 Problem 6.28: n ≤ 100 ✓; Odlyzko's ≈1.27 extrapolation noted as context.
- Downarowicz–Lacroix manuscript p.3: Turyn ⇔ Erdős L⁴ naming ✓.
- Rudin 1959 Theorem I: COULD NOT FETCH (Cloudflare challenge at ams.org).

## What I skimmed / did not check
- §§3–6 proofs (Prop 2.1, Lemma 2.2) — other seats; I only matched the constants K_δ, 1−7δ and the µ = 0 convention between
  statement and proof endpoints. If §5 delivers (1)–(2) only along a subsequence, or §6's C depends on N or X, Thm 1.1 falls —
  nothing in my pages can detect that.
- §8 / Cor 8.1–8.2, the merit-factor normalisation vs D–L Def. 2/Lemma 0/Thm 2 (round seat); JKS 6.342061… (world seat;
  only the cubic-root sanity check from memory).
- The earlier steps of 2504.21499 (Vitali, (19) density-½ via Lemma 3, (20)–(26)) — not needed: the final inference fails even
  granting them; I did not audit 1508.06439 / 2210.15480 (el Abdalaoui's reply cites them for other steps).
- Where in 1609.03435's 2,766-line proof of Thm 3.3 the error lies (sib1 does not claim to locate it either).
- Rudin 1959 (could not fetch). Formal Conjectures erdos_1150 and the Lean source (lean seat).

## Verdict
HOLDS AS READ IN SCOPE — Theorem 1.1 = comparator statement = a NO to #1150; the §2 reduction, Cor 7.1 (all 0<p<∞) and all
three Appendix A diagnoses (incl. Bloom's quantifier objection, which is the same point) are correct against the sources;
Appendix A and §7 are independent of the proof. Three EXPOSITION notes (E1 Erdős-1957 Problem 22 locator on the wrong clause;
E2 "o(√N)" overview sentence; E3 "examines specific issues" oversells for [8]).
