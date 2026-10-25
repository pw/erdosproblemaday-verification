# Seat CERT — hostile referee report on Proposition 3.1 (the C₄ flag-algebra certificate)
Claim: A. Sarid, "Sparse halves in triangle-free graphs: a bound of 131/5000" (4 Aug 2026), Prop. 3.1:
every triangle-free graph (graphon) satisfies t(C₄) ≥ ρ³ − γρ, γ = 3/64 + 1/(5·10¹⁰).
Seat scratch: /tmp/erdos1800/seats/cert/ (every number below is printed by a script there; logs alongside).

## 1. VERDICT
**HOLDS AS READ** — Prop. 3.1 is re-established by an independent exact verifier (label d); no FATAL, no GAP; exposition only.

Detail: every one of the 38 hosts dominates in exact rational arithmetic; my verifier, two families of controls, the
author's code (per host and per term) and the Lean's literal data and moment tables agree to the last digit; no probe
(14,651 graphs exact, 356 graphs × 16–61 weighted multistarts, 7 SRGs exact, 12 named graphs weighted) finds a violation.
Exposition defects: two false/unproved sentences outside the paper (README l.65, F4; verifier docstring l.35–37, F5), one
imprecise sentence in the paper (l.179, F6), and one omission (the paper never states its sampling semantics, §5).

## 2. Findings, most severe first

No FATAL, no GAP. What I attacked and what came back:

**F1 — the certificate semantics (the thing a hand check cannot see). HOLDS AS READ.**
Quoted: claim.txt l.184–190, "At level six, the expression t(C₄,W) − ρ³ + γρ has one rational coefficient for each of the
38 triangle-free unlabelled graphs on six vertices … checks that the coefficient of every one of the 38 hosts dominates
the sum of the corresponding square coefficients."
The paper never says which sampling semantics the coefficients use. I fixed one and checked it is the one the
certificate is written in: **injective sampling inside the host** (coefficient = probability under a uniformly random
bijection [6]→V(H)), applied to the **step graphon** of G (six points sampled *with* repetition from V(G)).
In that semantics c_H(C₄) = #C₄-subgraphs/45, c_H(ρ³) = #perfect matchings/15, c_H(ρ) = e(H)/15 (a, elementary).
Established by `controls.py` part (ii): on seven step graphons (C5, Petersen, Clebsch, four random weighted
triangle-free graphs on 5–6 vertices) I computed the 38 induced densities p(H;W) exactly by enumerating all n⁶ maps
(16⁶ = 16.8M for Clebsch) and checked Σ_H p(H;W)·c_H against *direct* counting: t(C₄) = tr((AD)⁴), ρ = wᵀAw, ρ³ —
**exact equality 7/7 graphons, all three densities** (C5: t(C₄) = 6/125; Clebsch: t(C₄) = 65/4096, ρ = 5/16).
Every one of the 34 averaged squares was also evaluated *directly from its graphon definition*
(E over the root of (Σᵢ vᵢ P(flagᵢ | root))², conditional laws enumerated over the leaves) and compared with its
host expansion: **34/34 exact equality on all 7 graphons, all direct values ≥ 0**. So the host-level coefficients are
the right linear functionals, the squares are genuinely averaged squares, and ρ³ really is t(3K₂).

**F2 — the u4 tie-break. HOLDS AS READ (a).** verify_clebsch_tangent_certificate.py l.224 ff. (`canonical_four_root` docstring):
"pick the ordering minimizing the root's induced mask (ties broken by the ordering, to keep the choice deterministic)".
When the 4-vertex root type has automorphisms the profile coordinates depend on the tie-break, and the tie-break
depends on the *sampled order* of the root vertices — a possible semantics slip. It is harmless: for g ∈ Aut(G[R]),
τ ↦ g∘τ is a bijection of the orderings of R preserving the induced labelled graph, so the lexicographic tie-break's
canonical assignment is *uniformly distributed* over all canonical assignments of R; hence each host coefficient equals
the average over ALL canonical assignments, and the graphon value E[f²] is unchanged (and each summand is still a square,
since the choice depends on the root only). My verifier uses the averaging rule (no tie-break at all); it agrees with the
author's per-term host coefficients on **all 34×38 (term, host) pairs** (`compare_author.py`, printed "38/38 … and per
term on all 34x38 pairs"); entrywise against the Lean's literal moment tables, 0 mismatches in 42,142 entries. The Lean uses the same tie-break as the Python (`canonicalRootCode`, Defs.lean) and its
nonnegativity proof only needs the code to depend on the four roots (`canonicalRootCode_induced_eq`), which it does.

**F3 — margin and fragility. HOLDS AS READ; worth knowing.** claim.txt l.171–172: "The verifier reports that the exact
slack its own square coefficients require is 1.9911·10⁻¹¹ < ε". Reproduced exactly, same 100-digit fraction
(`myverify.log`: ε needed = 1.991010996973144e-11). ε is used at 99.55% — the binding host is #23 = 3K₂ (perfect
matching on six vertices), slack 1.8·10⁻¹⁴. Consequently the certificate fails under ANY small perturbation:
weight ×1.01 → 34/34 terms FAIL; weight ×0.99 → 34/34 FAIL (host coefficients of a square can be negative, so the check is
not monotone in the weights); one vector entry ×1.001 → 34/34 FAIL; ε = 0 FAIL (host 23, −3.98·10⁻¹²);
ε = 1.9910·10⁻¹¹ FAIL (−2.2·10⁻¹⁷); ε = 1.9911·10⁻¹¹ passes; γ = 3/64 − 10⁻⁶ FAIL (host 37 = K₃,₃). This is not a defect
(all arithmetic is exact), but it means no decimal/float transcription of the certificate is valid — so I checked the Lean
copy is the JSON digit for digit: `lean_data_vs_json.py` prints "term-by-term identical (block, weight, full vector):
34 / 34", c4FlagGamma = 3/64 + 1/50000000000, and Lean `blockKeys` = my first-principles coordinate keys in all 10 blocks.

**F4 — README.md l.65 (EXPOSITION, false sentence):** "The minimum slack is exactly zero because the inequality is tight at
the Clebsch graph, which is why γ carries the small 1/(5·10¹⁰) term." WRONG as stated: the zero is at host 0 = the empty
graph E??? (target and every square coefficient vanish identically there; HOSTS.tsv row 0). The Clebsch graph is not a host;
at the Clebsch graphon the certificate leaves slack g − Σw·E[f²] = 5.996·10⁻¹² (`controls.log`). Does not affect validity.

**F5 — verifier docstring l.35–37 (EXPOSITION, unproved claim):** "an inequality tight at an interior point cannot be a
positive combination of squares, so a strictly positive ``epsilon`` is unavoidable for a certificate of this shape."
As a general statement this is false (exact certificates for tight inequalities exist when every square vanishes at the
extremal point — the paper itself says so at claim.txt l.169–171). For THIS certificate: at the Clebsch graphon the 34
squares sum to 2.54·10⁻¹³ > 0 (they do not all vanish), consistent with the paper's careful wording "no such certificate was
found". Nothing depends on it.

**F6 — claim.txt l.179 (EXPOSITION):** "a finite identity exhibiting the difference between the two sides of (2) as a
nonnegative rational combination of averaged squares". It is a host-wise *domination*, not an identity: the difference is
Σ squares + Σ_H p(H;W)·slack_H with slack_H ≥ 0, and two hosts carry large slack (host 24, 6.43·10⁻³; host 29,
5.60·10⁻²). Harmless.

## 3. What I recomputed and by which route (citable as a second instrument)
- **Hosts (d):** geng -t 6 → 38; brute force over all 2¹⁵ labelled graphs on [6] (orbit sweep) → 5789 labelled
  triangle-free graphs in 38 classes; the two class sets are identical (canonical form = lexicographically least sorted
  edge list over 720 relabellings). The Lean's 38 `classificationHostMasks` decode to exactly the same 38 classes
  (`lean_hosts_check.py`), and my verifier run on the Lean's labellings gives the same ε-needed (relabelling control).
- **Coordinates (d):** re-derived from first principles (s0: 3-vertex graphs by edge count; s2: labelled triangle-free
  4-vertex flags, key = min over the leaf swap; u4: the 7 triangle-free root types, coordinates = independent sets of the
  root) → dimensions 3/15/10/16/12/10/9/9/8/7 = the JSON's; key lists = Lean `blockKeys` in all 10 blocks.
- **Target (d):** by subgraph counting (#C₄/45 − #pm/15 + γ·e/15), not by a 720-ordering loop. Equal to the author's
  per-host value on 38/38 hosts.
- **Squares (d):** by subset sums — s0: (1/20)Σ_{3-sets}; s2: (1/180)Σ_{ordered root pairs}Σ_{leaf-pair splits};
  u4: (1/15)Σ_{4-sets} average over ALL canonical assignments. Equal to the author's on all 34×38 (term, host) pairs.
- **Domination (d):** `myverify.py` → "ALL HOSTS DOMINATE: True", minimum slack 0 (host 0), smallest positive slack
  1.798·10⁻¹⁴ (host 23 = 3K₂), ε needed = 37066776…901207/1861706…632000 ≈ 1.991010996973144·10⁻¹¹ < 2·10⁻¹¹.
  Per-host table: HOSTS.tsv (exact fractions + floats).
- **Graph level (d):** g(G) = t(C₄,G) − ρ³ + γρ with hom densities, exact, on the step graphons above, and the
  probes below.
- **Lean data (d):** Data.lean literal = JSON (34/34), γ literal correct. The Lean's 38 literal per-host moment tables
  (`HostChecks/Host{k}.lean`, `hostTables{k}`, which the Lean states equal to its own `momentTables (maskOfNat m)`)
  equal 720 × my symmetrised Gram matrices entrywise: 42,142 entries compared (2,894 nonzero), **0 mismatches**
  (`lean_moments_vs_mine.py`). Entrywise u4 agreement is a direct confirmation of the tie-break-uniformity argument (F2).

## 3b. Numeric probes (necessary conditions; a negative value would refute; exact parts are (d), SLSQP parts are (c))
All three probe families are necessary conditions; none can refute unless a value goes negative (beyond 1e-9).
Notation: g = t(C₄) − ρ³ + γρ (claim: g ≥ 0); h = t(C₄)/ρ − ρ² (claim, for ρ > 0: h ≥ −γ = −0.046875000…).
- **(a) all triangle-free graphs on n ≤ 10 vertices, uniform weights, exact rationals** (`probes.log`, geng -t):
  1+2+3+7+14+38+107+410+1897+12172 = 14,651 graphs, **0 negative g**. Smallest h per order: n=5 −0.040000 (C5),
  n=6 −0.028219, n=7 −0.030092, n=8 −0.041667 (GCrb`o, = Andrásfai(3)), n=9 −0.040129, n=10 −0.040000.
- **(b) the seven triangle-free SRGs, parameters verified from the adjacency matrix, exact** (adjacency matrices built in my own code;
  the S(3,6,22) blocks re-coded after reading the census construction and re-checked: 1540 triples each covered once):
  C5 g = 343750001/125000000000 (2.75e-3); Petersen 2.0625e-3; **Clebsch g = 1/160000000000 = 6.25e-12 = ε·ρ exactly**
  (t(C₄) = 65/4096, ρ = 5/16, h = −3/64); Hoffman–Singleton 4.5465e-3; Gewirtz 4.2707e-3; M22 3.4318e-3;
  Higman–Sims 2.9205e-3. All positive.
- **(c) weighted blow-ups, all connected triangle-free graphs on 2…8 vertices** (1+1+3+6+19+59+267 = 356 graphs;
  61 SLSQP starts each for n ≤ 7, 16 for n = 8, minimising both g and h on the simplex, analytic gradients):
  min g = 0 (attained only at ρ = 0, i.e. weight on an independent set), **min h = −0.041666667** (n = 8,
  GCrb`o uniform; n ≤ 7: −0.040022167 at FCpv? with weights (0.1997, 0.1822, 0.0188, 0.1985, 0.0188, 0.1997, 0.1822)).
  Margin to −γ: 5.21e-3. No negative value. (Clebsch is not in this range — 16 vertices — so (c) cannot see the tight point.)
- **(d) weighted local probes on 14 named graphs, 12 completed** (uniform start + 12 multiplicative perturbations of size 1%/5%/20% +
  random Dirichlet starts): **Clebsch: min h found = −0.046875000 at the uniform weighting (max |w − u| = 3.6e-9),
  margin to −γ = 2.000e-11 = ε** — no reweighting of Clebsch goes below 3/64, consistent with the certificate.
  Petersen, C5: −0.040 at uniform. Grötzsch: −0.044679 (closest non-Clebsch value, margin 2.2e-3, non-uniform).
  Andrásfai(3,4,5): −1/24. Möbius–Kantor: −0.027778. Kneser(7,3): −0.013968. Kneser(8,3), Hoffman–Singleton, Gewirtz:
  −0.040 (the optimiser collapses onto a C5/Petersen-type sub-blow-up). The weighted M22 and Higman–Sims probes did NOT complete (stopped at the
  time wall; their exact uniform values are in (b)).
  Nothing below −γ; min g over all (d) runs ≥ 0 up to float noise (largest magnitude printed 7.6e-18, all positive).

## 4. Lean side of Prop 3.1 (read, not built — building is the LEAN seat's job)
`certificate_all_triangleFree_masks : ∀ (m : Mask), IsTriangleFreeMask m → sosCoefficient m ≤ targetCoefficient m`
(FiniteCertificate.lean), where `Mask = Fin 15 → Bool` is a *labelled* graph on Fin 6 with bit e ↔ `edgeEnds e`
(lexicographic pairs, the Python's order), `targetCoefficient m = Σ over the 720 label orders p of targetAt m p`
(targetAt = adj p0p1·p1p2·p2p3·p3p0 − p0p1·p2p3·p4p5 + c4FlagGamma·p0p1, i.e. the Python target ×720) and
`sosCoefficient m = Σ_p Σ_t weight·feature(left)·feature(right)` over the literal 34 `certificateTerms`. It is proved for
all 2¹⁵ masks by a checked orbit cover of the 38 representatives plus relabel-invariance of both coefficients
(`certificate_of_cover`), with the 38 representative inequalities discharged in `HostChecks/Host{k}.lean` from literal moment tables
(`momentTables_host{k}`; I did not build these proofs — LEAN seat). Host-level semantics:
**injective** (all 720 orderings of the six labelled positions), exactly the Python's.
`checkedC4FlagCertificateProvider : C4FlagCertificateProvider`, i.e. `∀ (V : Type) [Fintype V] [DecidableEq V]
(G : SimpleGraph V) [DecidableRel G.Adj], G.CliqueFree 3 → C4FlagCertificate G` (IntegratedBound.lean l.109), and
`C4FlagCertificate G` (ExternalInputs.lean) is `n²·tr(A⁴) ≥ 8m³ − 2·c4FlagGamma·m·n⁴` with n = |V|, m = |E|, which for
n > 0 is exactly t(C₄,G) ≥ ρ³ − γρ with hom densities (`c4DensityQ_ge_of_C4FlagCertificate`). The step from six vertices
to an arbitrary finite G (GlobalBridge.lean) sums over **all maps x : Fin 6 → V, with repetition** (`inducedMask`
docstring: "Sampling is with replacement") — the discrete step-graphon argument: (i) Σ_x targetCoefficient(inducedMask G x)
= 720·(n²·hom(C₄) − 8m³ + 2γmn⁴) (`sum_targetCoefficient_inducedMask`, via order reindexing + the identity-order sum);
(ii) Σ_x sosCoefficient(...) ≥ 0 because, at the identity order, each term factors as weight × Σ_root(Σ_leaf F)²
(`sum_termAt_identityOrder_nonneg`, using that the u4 canonical code depends only on the four roots); (iii) inducedMask of
a CliqueFree-3 graph is a triangle-free mask (`inducedMask_isTriangleFree`: a mask triangle forces three pairwise adjacent,
hence distinct, vertices), so the pointwise bound applies to every summand. So the statement proved is exactly
`C4FlagCertificate G` for every finite triangle-free G with V : Type (the universe-polymorphic
`c4FlagCertificate_of_mask_bound` gives it in every universe), with no hypothesis beyond `G.CliqueFree 3`; it does not
mention BCL. Note: the brief's `Semantics.lean` does not exist; the semantics lives in `C4Certificate/Defs.lean`
("Exact finite semantics for the six-vertex C₄ flag certificate").

## 5. Exposition notes (short; never change a verdict)
- Paper l.182–190 should say in one sentence: coefficients are injective-sampling densities inside the host, applied to the
  step graphon (with-repetition sampling from G); and should state the coordinate convention or point to the docstring.
- Paper l.179 "finite identity" → "finite domination" (F6). README l.65 explanation is wrong (F4). Docstring l.35–37
  overclaims (F5).
- It would help to state the binding host (3K₂) and that ε is used at 99.55%.

## 6. Could not check
- I did not build the Lean package (no `lake build` run by this seat); I read the statements and proof skeletons of
  Defs, FiniteCertificate, ClassificationSoundness, GlobalBridge, TargetAveraging(Core), ConditionalSquares(Core),
  Provider, ExternalInputs, IntegratedBound. Kernel-checking the 38 host computations and the orbit cover is the LEAN seat's.
- Numerical probes are necessary conditions only; SLSQP minima are local and float-valued (labelled c). The weighted
  probes on M22 (77 v.) and Higman–Sims (100 v.) did not finish inside the time wall (exact uniform values do: (b)).
- Nothing in this seat touches BCL Theorem 2(a), Lemma 3.2, or Section 4.

## Files (all in /tmp/erdos1800/seats/cert/)
`myverify.py` (+ `myverify.log`, writes `HOSTS.tsv`) — independent verifier · `controls.py` / `controls.log` — mutation
and graphon-expansion controls · `probes.py` / `probes.log`, `probes_d2.py` / `probes_d2.log` — numeric probes ·
`compare_author.py` / `.log` — per-host/per-term agreement with the author's functions (run with `python -I`) ·
`lean_data_vs_json.py`, `lean_hosts_check.py`, `lean_moments_vs_mine.py` (+ logs) — Lean literal data vs JSON and vs mine.
