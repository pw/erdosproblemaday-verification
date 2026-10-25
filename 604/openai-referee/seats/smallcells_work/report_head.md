# Referee report — seat `smallcells` — §4 "Small cells and fiber mass" (PDF pp. 12–14)

Paper: OpenAI, "The weak pinned planar distance theorem" (23 Sep 2026), local copy /tmp/oaimath/604/paper.pdf.
Read for this seat: PDF pp. 3–15 rendered (§1.2, §2 incl. Prop 2.2 and (2.2)–(2.4), §3 incl. (3.1)–(3.7), all of §4, first page of §5),
plus p. 18 (the one downstream re-use of Lemma 4.1 in §6.1, hypotheses only). Lean read AS TEXT only (never run):
`OAI/Geometry/PinnedDistances/SmallCells.lean`, parts of `ArithmeticGraphs.lean`, `OverlapRates.lean`, `Hierarchy.lean`.
Every formula below was read off the rendered PDF; paper.txt was used only to copy prose verbatim.

## Verdict for this scope

**HOLDS AS READ.** The setup (4.1), the definition and finiteness of T(λ), Lemma 4.1 with all three branches and all three
cases, (4.3), (4.4), the level changes r′ = h_e − r ∓ H_v, N_j(y), the Tonelli claims, the parameter choice τ = λ_n^{1/3},
H = λ_n^{−1/2}, and the derivation of (4.5) W_{2,sm} = o(W+1) from (2.4) and (4.1) all check line by line. I found no FATAL
and no GAP. The objections below are COSMETIC (wording that is vacuous, implicit, or stronger than needed). An exact
rational toy computation of the whole three-case accounting on random nested hierarchies (397 instances, all three cases
exercised, the Figure-1 multiset duplication present in 608/800 hierarchies) closes with zero discrepancy in every exact
identity of the proof; two input-level controls (a non-fiber, a non-nested "hierarchy") and five code mutants all fail as they
should.

Conditional inputs (owned by other seats, used here as stated): (2.2) and (2.4) from Prop 2.2 [extremal seat]; (3.3), Lemma
3.1's tail (3.4) and finiteness, Lemma 3.2's finiteness bounds, and the additive identity (3.6) [arithmetic seat]. §4 adds no
new Euclidean / characteristic-zero input of its own (see "Note for the whole/(i) seat" at the end).

## Objections (numbered)

**1. COSMETIC (exposition) — Case 3, p. 14: vacuous "empty union" provision.**
> "These cells form a nested chain of subsets of the finite set P, so |N_j(y)| < τn (with empty union allowed)."
and the displayed sum's index condition "N_j(y) ≠ ∅".
N_j(y) is never empty: the hypothesis τ ≥ 2/n gives τn ≥ 2 > 1, and every distinct-pair depth is finite (Lemma 3.1), so
above d₊ the singleton {y} is an actual j-cell of size 1 < τn. The provision and the index restriction are vacuous; harmless
(when N_j(y) = ∅ the term |N_j(y)| − 1 = −1 would only help). Fix: delete both, or say "N_j(y) ∋ y".

**2. COSMETIC (exposition) — Case 3, p. 14: right side undefined off the giant ray.**
> "≤ B0/(n(n−1)) Σ_{y∉G_{j′}(r′), N_j(y)≠∅} (|N_j(y)| − 1) ≤ B0 τ α(P \ G_{j′}(r′))." … "Integrating, summing coordinates and averaging gives B0τA."
G_{j′}(r′) is defined only where a giant exists. The bound is used only at levels where some fiber is in Case 3, i.e. where
V₊ = Π_{j′}(r′)(x_e) is giant, so G_{j′}(r′) exists; elsewhere the Case-3 integrand is 0. Integrating B0τα(P∖G_{j′}(r′)) over
{r′ : G_{j′}(r′) exists} is exactly B0τ E_α S_{j′} by the definition of S_j on p. 10, which gives B0τA after summing j and ⟨·⟩.
The proof is right; the restriction to {G exists} is implicit. Fix: write the bound as B0τα(P∖G_{j′}(r′))1{G_{j′}(r′) exists}.

**3. COSMETIC — Lemma 4.1 hypothesis "H ≥ 1" is never used.**
> "if 0 < λ < 1/2, 2/n ≤ τ ≤ 1, and H ≥ 1, then T(λ) ≪ (λ/τ² + λ)W2 + τA + λH + e^{−b1H}"
Every step needs only H ≥ 0 (the tail integral ∫_H^∞ needs H ≥ 0 so that (3.4)'s "u ≥ 0" applies; Case 2 needs H_v ≥ 0 so that
V₊ ⊆ V₋). The Lean (`SmallCells.active_integral`, hypothesis `hH : 0 ≤ H`) uses H ≥ 0. Harmless.

**4. COSMETIC — p. 12: a hypothesis attached to an unconditional identity.**
> "If (qX + qY)/2 ≥ (1 − ϵn)α, where ϵn → 0, then E_q L*(x,y) = W2 + Σ_{x∈P} (qX(x) + qY(x) − 2α(x)) S*(x)."
The displayed identity is unconditional (it is (3.6) integrated against q, minus W2 = b* + 2A); the marginal hypothesis is
needed only for the next inequality W2 − o(1)A ≤ E_qL*. Harmless. (Exact form: E_qL* ≥ W2 − 2ε_n A.)

**5. COSMETIC — (4.4) suppresses the coordinate and the constant b1.**
(4.4) "⟨E_e ∫(D⁻ + D⁺) dr⟩ ≪ e^{−b1H}" is for one fixed coordinate j (D± depend on j); the proof of (4.2) uses it summed over
j = 1, 2, a factor 2 absorbed in ≪. The value b1 = b0/2 (from Pr(|Δ_j + Δ_{j′}| > u) ≤ 2C0e^{−b0u/2}, so
E(|Δ_j+Δ_{j′}| − H)₊ ≤ (4C0/b0)e^{−b0H/2}) is not stated; the lemma only claims "b1 > 0 is absolute", which is true.

**6. COSMETIC — Case 1, p. 14: the main-term step is compressed.**
> "After discarding the other restrictions, change levels to r′ = he − r − Hv. Sharing a nongiant cell in the j′-hierarchy contributes to Lj′, so the main term is bounded by 2λEqLj′."
The three facts behind the sentence, all true: (a) for a fixed fiber r ↦ h_e − r − H_v is a measure-preserving bijection of ℝ,
so ∫µ_e(V₋)1{V₋ nongiant}dr = E_{y∼µ_e}∫1{y ∈ Π_{j′}(r′)(x_e), nongiant}dr′; (b) E_e E_{y∼µ_e} = E_q (the sampling rule on
p. 6); (c) a nongiant actual cell is a member of C_{j′}(r′), so the indicator is ≤ Σ_{C∈C_{j′}(r′)} 1_C(x)1_C(y), whose integral
is L_{j′}(x,y). (a) is checked exactly in the toy (assertion `I['Vm_ng'] == Ey(L^ng)`).

No FATAL. No GAP. No UNCLEAR.

## What each piece of §4 says, and status (the deliverable)

| Item (PDF page) | Status | Notes |
|---|---|---|
| W2 = b* + 2A (p. 12) | VERIFIED LINE BY LINE | E_π[b*+S*(x)+S*(y)], both π-marginals are α. |
| E_qL* = W2 + Σ(q_X+q_Y−2α)S* (p. 12) | VERIFIED LINE BY LINE | (3.6) integrated against q (q lives on distinct pairs, E ⊂ {x≠y}). |
| (4.1) W2 − o(1)A ≤ I(q(C²)) = E_qL* ≤ B0W2 (p. 12) | VERIFIED LINE BY LINE | Lower: q_X+q_Y−2α ≥ −2ε_nα and S* ≥ 0 ⇒ ≥ W2 − 2ε_nA. Upper: L* ≥ 0 (integral of nonneg. indicators) and q ≤ B0π. I(q(C²)) = E_qL* by Tonelli. ε_n is (2.2)'s, uniform in vertices. |
| T(λ) definition and finiteness (p. 12) | VERIFIED | Integrand ≤ E_e1_C(x_e)µ_e(C) = q(C²) (fiber sampling), and I(q(C²)) ≤ B0W2 < ∞. |
| Lemma 4.1 statement (4.2) (p. 12) | VERIFIED LINE BY LINE | Constants: 2/τ² (large) + B0 (complements) + 2B0 (Case 1) + 4 (Case 2) + B0 (Case 3) + 2·(4C0/b0)·(1+1) errors; depends only on B0, C0, b0 as claimed. |
| (4.3) α(C)²/2 ≤ π(C²) = m(m−1)/(n(n−1)) ≤ α(C)² for m ≥ 2 (p. 13) | VERIFIED | Upper ⇔ m ≤ n; lower ⇔ n(m−2) + m ≥ 0. |
| Large-cell branch a ≥ τ (p. 13) | VERIFIED | m = an ≥ τn ≥ 2 uses τ ≥ 2/n; integrand ≤ λE_e1_C(x_e) ≤ λ ≤ 2λπ(C²)/τ² by (4.3); integrates to ≤ 2λW2/τ². Covers actual AND complement occurrences with a ≥ τ. |
| Giant-complement branch a < τ (p. 13) | VERIFIED | Integrand ≤ q(C²) ≤ B0π(C²) ≤ B0a² < B0τa. "The integral of a over the giant-complement occurrences is A": ⟨Σ_j∫_{G_j(r) exists} α(P∖G_j(r)) dr⟩ = ⟨Σ_j E_αS_j⟩ = A — exact (toy assertion `Acomp == A`). Multiplicity: a complement equal to an actual cell is counted once here and once as an actual cell below; both occurrences are covered. |
| Reduction of actual nongiant cells with a < τ to a per-fiber level integral (p. 13) | VERIFIED | For fixed r and e exactly one actual cell contains x_e, namely U = Π_j(r)(x_e), and it is a member of C_j(r) iff it is nongiant; so Σ_{C actual}1_C(x_e)f(C) = f(U)1{U nongiant}. Toy: occurrence-level sum == per-fiber sum, exactly. |
| V± and V₊ ⊆ V₋ (p. 13) | VERIFIED | Π increases in fineness with level; h_e − r + H_v ≥ h_e − r − H_v since H_v ≥ 0. |
| ∫D⁻dr = E(h_e − d − d′ − H_v)₊, ∫D⁺dr = E(d + d′ − h_e − H_v)₊ (p. 13) | VERIFIED LINE BY LINE | y ∉ U ⇔ d < r; y ∉ V₋ ⇔ r < h_e − H_v − d′; y ∈ U∩V₊ ⇔ h_e + H_v − d′ ≤ r ≤ d. Toy: exact. |
| Sum = E(|Δ_j + Δ_{j′}| − H_v)₊ (p. 13) | VERIFIED | d + d′ − h_e = Δ_j + Δ_{j′} by (3.3); (−a−H)₊ + (a−H)₊ = (|a|−H)₊ for H ≥ 0. Zero at finite places since Δ = 0 and H_v = 0. |
| Tail Pr(|Δ_j+Δ_{j′}| > u) ≤ 2C0e^{−b0u/2} and (4.4) (p. 13) | VERIFIED given (3.4) | Union bound on marginal tails, no joint law needed ("No independence of the two errors is required" — correct). (3.4) itself = Lemma 3.1, arithmetic seat. |
| Case 1: V₋ nongiant (pp. 13–14) | VERIFIED LINE BY LINE | P∖U ⊆ V₋ ∪ (P∖(U∪V₋)) ⇒ µ_e(V₋) + D⁻ ≥ 1 − p > 1/2 ⇒ p < λ ≤ 2λ(µ_e(V₋)+D⁻). Main term → 2λE_qL_{j′} (Objection 6), then Σ_j,⟨·⟩, (4.1) upper ⇒ 2B0λW2. Error ≤ ∫D⁻ since 2λ < 1. The factor 2 is needed: dropping it is violated on 286 retained level-intervals in the toy. |
| Case 2: V₋ giant, V₊ not (p. 14) | VERIFIED LINE BY LINE | Giant levels of x's j′-cell form a proper initial ray (P is giant; singletons are not, as n ≥ 2), endpoint t₀ finite. V₋ giant & V₊ not ⇔ h_e − r − H_v ≤ t₀ < h_e − r + H_v (up to endpoints) ⇒ r in an interval of length EXACTLY 2H_v (toy: raw straddle length == 2H in every fiber; Lean `straddle_integral` proves = 2H). Integrand ≤ λ ⇒ 2λH_v per fiber ⇒ 4λH after Σ_j and Σ_{v|∞}σ_v = 1. Empty at finite places (H_v = 0 ⇒ V₋ = V₊). |
| Case 3: V₊ giant (p. 14) | VERIFIED LINE BY LINE | Exhaustive since V₊ ⊆ V₋ (giant V₊ ⇒ giant V₋). p = µ_e(U∩V₊) + µ_e(U∖V₊) = D⁺ + µ_e(U∖V₊) (toy: exact). After r′ = h_e − r + H_v (per-fiber bijection), V₊ = G_{j′}(r′), so a counted target has y ∉ G_{j′}(r′). |
| N_j(y), "|N_j(y)| < τn", "all possible sources lie in N_j(y)∖{y}" (p. 14) | VERIFIED | Cells containing y in a nested hierarchy are totally ordered; finitely many distinct ones, so the union of those of size < τn is the largest, size < τn. A counted source x_e lies in U = Π_j(r)(x_e) ∋ y with |U| = α(U)n < τn, so U ⊆ N_j(y) and x_e ∈ N_j(y)∖{y} (x_e ≠ y: distinct pairs). "Each edge belongs to exactly one fiber" (a fiber is (source, squared distance)), and r ↔ r′ is a bijection per fiber, so each edge is counted at most once at each r′. |
| Case-3 bound q ≤ B0/(n(n−1)); |N_j(y)| − 1 ≤ τ(n−1) (p. 14) | VERIFIED | |N_j(y)| − 1 < τn − 1 ≤ τn − τ as τ ≤ 1. ⇒ B0τ α(P∖G_{j′}(r′)) ⇒ B0τA (Objection 2). Toy: checked POINTWISE in r′ (fiber-summed Case-3 mass ≤ the N_j double sum ≤ B0τα(P∖G)), and the integrated level-changed mass equals the per-fiber Case-3 mass exactly. |
| "Threshold ties … Tonelli's theorem applies" (p. 14) | VERIFIED | All integrands piecewise constant in r with finitely many breakpoints per place/grid; nonnegative; ⟨·⟩ is a nonnegative sum over places of grid expectations, with only finitely many nonunit places contributing (at unit places every term — T, L, S, D± — is 0). Joint measurability in (grid, r) is Lemma 3.1's last sentence (arithmetic seat). |
| (4.5) parameters (p. 14) | VERIFIED | λ_n = 1/log n < 1/2 for n ≥ 8; τ = (log n)^{−1/3} ∈ [2/n, 1] for n ≥ 3; H = (log n)^{1/2} ≥ 1 for n ≥ 3. (λ/τ²+λ)W2 + τA ≤ 2λ^{1/3}W, λH = λ^{1/2}; so T(λ_n) ≤ K(2λ_n^{1/3}W + λ_n^{1/2} + e^{−b1λ_n^{−1/2}}) = o(W+1) with a configuration-independent o(1). |
| (4.5) W_{2,sm} = o(W+1) from (2.4) and (4.1) (p. 14) | VERIFIED LINE BY LINE | See derivation below. |
| Inputs (2.2), (2.4) (pp. 6–8) | VERIFIED at the level used | B0 = 2/θ since q/π = 1/d_n; marginal lower bound from the degree bound; (2.4) both regimes re-derived (count of edges (x_e,y) ∈ C² with |F_e∩C| ≥ λ_nk_e, k_C(x_e,y) ≥ |F_e∩C| ≥ T_n, Lemma 2.1 / Θ(s′)=0). Its left side depends only on the finite graph and the subset C — never on the place, grid or level — so the o(1)'s are uniform over all occurrences, as (4.5) needs. Full audit = extremal seat. |
| Inputs (3.3), (3.4), (3.6), Lemma 3.2 bounds (pp. 9–12) | (3.3) VERIFIED; others SKIMMED | (3.3): t(x,y) factors in K, |·|_v multiplicative. (3.4)/(3.6)/Lemma 3.2: arithmetic seat. |
| §6.1 re-use of Lemma 4.1 (p. 18) | hypotheses VERIFIED; rest NOT READ | "For a fixed 0 < δ < 1/4 … apply Lemma 4.1 with λ = 2δ, τ = λ^{1/3} and any fixed H ≥ 1": λ = 2δ < 1/2 ✓, τ ≥ 2/n eventually ✓, (λ/τ²+λ)W2 + τA ≪ δ^{1/3}W ✓, λH + e^{−b1H} = O_δ(1) ✓. |

### (4.5), written out with explicit error sequences
Let ε₁ → 0 with I(q(C²)) ≥ W2 − ε₁A ((4.1)); let ε₂, ε₃ ≥ 0, → 0, with E_e1_C(x_e)p1{p≥λ_n} ≤ (1+ε₂)π(C²) for |C| > n^{1−c} and
≤ ε₃π(C²) for |C| ≤ n^{1−c}, uniformly in C ((2.4)); let ε₄ → 0 with T(λ_n) ≤ ε₄(W+1) (Lemma 4.1 at τ = λ_n^{1/3}, H = λ_n^{−1/2}).
Splitting E_e1_C(x_e)p = (…)1{p<λ_n} + (…)1{p≥λ_n} inside I and integrating occurrence by occurrence:

W2 − ε₁A ≤ I(q(C²)) ≤ ε₄(W+1) + (1+ε₂)(W2 − W_{2,sm}) + ε₃W_{2,sm},

hence W_{2,sm}(1 + ε₂ − ε₃) ≤ ε₁A + ε₂W2 + ε₄(W+1), so W_{2,sm} ≤ (ε₁ + ε₂ + ε₄)(W+1)/(1 − ε₃) = o(W+1). Directions are right: the
LOWER bound of (4.1) (arithmetic: (3.6) + the marginal bound) is played against the UPPER bound from (2.4) (combinatorics) plus
Lemma 4.1. Nothing is circular: Lemma 4.1 uses only the UPPER half of (4.1) (via q ≤ B0π), never (4.5). The paper's closing
remark "This estimate holds before passing to either a bounded or an unbounded subsequence of W" is correct: every ε_i is a
fixed sequence independent of the configuration's coordinates and of W.

### Hand-wave phrases in §4 (all checked)
pdftotext of §4 contains exactly five: "it follows that" ((4.1), checked), "Thus V₊ ⊆ V₋" (checked), "Hence ∫D⁻ … ∫D⁺" (checked,
exact in toy), "Thus all the possible sources of this target lie in N_j(y)∖{y}" (checked), "The mass at r′ is therefore at most"
(checked, pointwise in toy). No "clearly", "similarly", "the same argument".

## Citation table for this scope
§4 (pp. 12–14) cites no external source. The only named tool is Tonelli's theorem (nonnegative integrands; correctly invoked).
Internal dependencies: (2.2), (2.4), (3.3), (3.4), (3.6), Lemma 3.2 — all as listed above.

## Lean cross-reference (read as text; not run by this seat)
Per /tmp/oaimath/604/lean-build/modules.tsv (the replay's own record, read only): `SmallCells`, `ArithmeticGraphs`,
`OverlapRates` built rc=0, errors=0. The formal proof of Lemma 4.1 has the SAME four-term per-fiber shape as the paper:
`SmallCells.active_pointwise` (l. 551): activeMass ≤ 2λ·nongiantMass(h−r−H) + λ·straddle + minusError + plusError +
neighborMass(h−r+H); `active_integral` (l. 726) integrates it; `straddle_integral` (l. 131) proves the Case-2 set has length
exactly 2H; `smallNeighbors_card` (l. 163) is |N_j(y)| < τn; `source_mem_smallNeighbors` (l. 186) is "every counted source lies in
N_j(y)"; `case_three_bound` (l. 528) and `fiber_neighbor_bound` (l. 772) are Case 3; `errors_integral`/`two_truncations`
(ll. 478–484) are the D± integrals; `small_case_one` (l. 303) is Case 1 (with hypotheses mass ≤ λ ≤ 1/2). (4.5) is
`PreparedGraph.small_overlap` (ArithmeticGraphs l. 251) + `small_overlap_rate` (OverlapRates l. 36), which uses FIXED τ, H and
an ε-argument instead of τ = λ_n^{1/3}, H = λ_n^{−1/2}, with explicit error term 32·exp(−H/2). The Lean's `Depth` (Hierarchy.lean
l. 21) is exactly an ultrametric sharing depth — the same abstraction my toy uses. Minor differences (λ ≤ 1/2 vs < 1/2, H ≥ 0
vs ≥ 1, Case-1 error coefficient 1 vs 2λ) are all in the harmless direction.

## Note for the whole/(i) seat: what §4 uses that is not pure combinatorics
Lemma 4.1 is a deterministic statement about two nested hierarchies on a finite set, one constant h_e per fiber with
i_j + i_{j′} = h_e ((3.3)), and the grid-error tail (3.4) at archimedean places, plus Δ = 0 at finite places and
Σ_{v|∞}σ_v = 1. (3.3) comes from the factorization (3.1), valid in any field, and multiplicativity of |·|_v. (4.5) adds (2.4) and
(4.1), the latter resting on (3.6) (product formula). So §4 introduces NO new real/Euclidean input beyond §3's; it would hold
verbatim for any two injective coordinates with nonzero products of differences (the pseudo-Euclidean/complex generalization
in brief item (i)). Whatever separates ℝ² from F_q² must therefore live in §3 or §7, not here.

## Finite check: exact toy computation of Lemma 4.1's accounting

What it does. One place of weight 1; two coordinates; each realized hierarchy is a random ultrametric sharing depth d_j with
half-integer values (Π_j(r) = classes of d_j ≥ r; nested by construction, asserted ultrametric); random fibers (source, disjoint
target sets, a constant h_e near the median of d_1+d_2 on the fiber, so Δ_1+Δ_2 = d_1+d_2−h_e is a genuine nonzero "grid error");
q uniform on edges, B0 = n(n−1)/|E| = max q/π exactly; random λ ∈ {1/5,1/3,2/5,49/100}, τ ∈ [2/n,1], H ∈ {0,1/2,1,2}. All
arithmetic in Fraction; level integrals are exact sums over the intervals between breakpoints; every integrand is asserted to
be exactly 0 on the two unbounded intervals. Asserted EXACTLY (==) or as inequalities, per instance: the occurrence-level split
T = T_large + T_comp + T_act; T_large ≤ 2λW2/τ²; T_comp ≤ B0τ∫a ≤ B0τA and ∫Σ_{complements} a dr == A; occurrence-level T_act ==
the per-fiber level integral; per fiber: ∫D⁻ == E(h−d−d′−H)₊, ∫D⁺ == E(d+d′−h−H)₊, sum == E(|Δ+Δ′|−H)₊; total kept mass ==
Case1+Case2+Case3; Case 1 pointwise cover and p ≤ 2λ(µ(V₋)+D⁻); ∫µ(V₋)1{ng}dr == E_y L^{ng}_{j′} (the level change r′ = h−r−H);
raw straddle length == 2H and Case-2 mass ≤ 2λH; Case 3 pointwise identity p == D⁺ + µ(U∖V₊); |N_j(y)| < τn with the chain
nested; POINTWISE in r′ = h_e − r + H: fiber-summed Case-3 mass ≤ Σ_{y∉G}Σ_{x∈N_j(y)∖y}q(x,y) ≤ B0τα(P∖G); its r′-integral ==
the per-fiber Case-3 mass and the right side integrates == B0τA_{j′}; E_qL ≤ B0W2; and the assembled Lemma 4.1 bound with
explicit constants T ≤ 2λW2/τ² + B0τA + 2λB0W2 + 2λ·ERR⁻ + 4λH + ERR⁺ + B0τA.

Controls that FAIL (deliberately wrong inputs the checker rejects):
- C1 — a fake "fiber" whose targets have DIFFERENT raw sums i_1+i_2 (violates (3.3)): ∫(D⁻+D⁺) = 23/8 ≠ E(|Δ+Δ′|−H)₊ = 2.
  The D± accounting closes only because h_e is constant on a fiber.
- C2 — coordinate j given by a NON-ultrametric depth (balls, not a partition): the partition assertion fails, |N_j(y₀)| = 13 vs
  τn = 3, and the Case-3 mass 5/19 ≈ 0.263 EXCEEDS B0τA_{j′} = 1/8. Nesting is load-bearing in Case 3.
- Sharpness: dropping the factor 2 in Case 1 (p ≤ λ(µ(V₋)+D⁻)) is violated on 286 kept level-intervals.
- Mutants of the checker itself (each must trip an assertion; all do): M1 wrong sign in V₋'s level (h+r−H) → integrand not
  compactly supported; M2 D⁻ forgets U → same; M3 Case-3 identity without D⁺ → "Case 3 identity" assertion; M4 claim Case-2
  length ≤ H → fails (it is exactly 2H); M5 D⁻ built with V₊ instead of V₋ (compact support kept) → the exact ∫D⁻ identity
  assertion fails. Mutant command and outcome:
```
for f in mut/*.py; do printf '%s -> ' "$(basename $f)"; timeout 60 python3 -I "$f" 30 2>&1 | grep -B2 -E "^AssertionError" | head -1 | sed 's/^ *//'; done
M1_Vminus_level_sign.py -> for v in fn(b[0] - 1).values(): assert v == 0, "nonzero on (-inf,b0)"
M2_Dminus_forgets_U.py -> for v in fn(b[0] - 1).values(): assert v == 0, "nonzero on (-inf,b0)"
M3_case3_drops_Dplus.py -> assert p == s.mu(F, U - Vp)                # Case 3 identity
M4_case2_length_H.py -> assert I['c2_raw'] <= H
M5_Dminus_uses_Vplus.py -> assert I['Dm'] == Ey(lambda y: pos(h - dj[(x, y)] - dk[(x, y)] - H))
```
Mutant diffs vs the script below (`show_example()` replaced by `pass` in all mutants):
```
M1: Vm = cell(dk, n, h - r - H, x) -> Vm = cell(dk, n, h + r - H, x)   (and the V+ ⊆ V- assert disabled)
M2: Dm = s.mu(F, s.P - (U | Vm))  -> Dm = s.mu(F, s.P - Vm)
M3: assert p == Dp + s.mu(F, U - Vp) -> assert p == s.mu(F, U - Vp)
M4: assert I['c2'] <= 2*lam*H     -> assert I['c2_raw'] <= H
M5: Dm = s.mu(F, s.P - (U | Vm))  -> Dm = s.mu(F, s.P - (U | Vp))
```
Also counted (same hierarchies as the 400 seeds): the Figure-1 multiset duplication (giant complement equal to an actual
cell) occurs on some level interval in 608 of 800 hierarchies, so the multiplicity bookkeeping is genuinely exercised.

Worked example (printed by the script; hand-checked): n = 8, x = 0, F = {1,…,6}, h_e = 4, λ = 2/5, τ = 1/2, H = 1/2, j = 1. On
(1, 3/2): U = {0,5}, V₋ = Π₂(3.5−r)(0) = {0,2} nongiant ⇒ Case 1, p = 1/6, D⁻ = µ({1,3,4,6}) = 2/3, and
p ≤ 2λ(µ(V₋)+D⁻) = (4/5)(5/6). On (3/2, 5/2) (length 1 = 2H): V₋ = {0,1,2,3,4,6,7} giant, V₊ = {0,2} not ⇒ Case 2. On
(5/2, 7/2): V₊ giant ⇒ Case 3, p = D⁺ + µ(U∖V₊) = 0 + µ({5}) = 1/6 — the target y = 5 has Δ₁+Δ₂ = 0, yet it is in U and outside
the giant V₊: exactly the "rest" term charged to N_1(5) and to S_2. Totals: kept mass 5/12 = 1/12 + 1/6 + 1/6.

Script: /tmp/oaimath/604/seats/smallcells_work/lemma41_toy.py (sha256 b68489e4…fcf), run as
`cd /tmp && python3 -I /tmp/oaimath/604/seats/smallcells_work/lemma41_toy.py 400` — 39 s wall, < 50 MB.

### Script (verbatim)
```python
