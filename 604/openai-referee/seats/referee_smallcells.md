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
| Lemma 4.1 statement (4.2) (p. 12) | VERIFIED LINE BY LINE | Explicit form: T(λ) ≤ 2λW2/τ² + B0τA [large, complements] + 2B0λW2 [Case 1] + 4λH [Case 2] + B0τA [Case 3] + 2·(4C0/b0)e^{−b0H/2} [errors, two coordinates]; depends only on B0, C0, b0 as claimed. |
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
`cd /tmp && python3 -I /tmp/oaimath/604/seats/smallcells_work/lemma41_toy.py 400` — 39 s wall; peak RSS 13.8 MB (measured on a 30-seed run).

### Script (verbatim)
```python
#!/usr/bin/env python3
"""Exact toy check of Lemma 4.1 (paper pp. 12-14) and its three-case split.

One place (weight 1), two coordinates j=1,2, each with a FIXED realized nested
hierarchy given by an ultrametric 'sharing depth' d_j (Pi_j(r) = classes of
d_j >= r).  Fibers e = (source x_e, target set F_e, constant h_e); the raw-depth
sum i_j+i_j' = h_e on the fiber is (3.3), so Delta_j+Delta_j' = d_j+d_j'-h_e.
All arithmetic is Fraction (exact).  Every level integral is computed exactly as
sum over the open intervals between breakpoints of (value at midpoint)*(length);
on the two unbounded intervals every integrand is asserted to be exactly 0.
"""
from fractions import Fraction as Fr
import random, sys

def ultrametric(n, rng, maxlev=12, den=2):
    cl = [[i] for i in range(n)]
    ts = sorted((Fr(rng.randint(0, maxlev*den), den) for _ in range(n-1)), reverse=True)
    d = {}
    for t in ts:                       # merges at non-increasing depth => ultrametric
        a, b = rng.sample(range(len(cl)), 2)
        for x in cl[a]:
            for y in cl[b]:
                d[(x, y)] = d[(y, x)] = t
        cl = [c for k, c in enumerate(cl) if k not in (a, b)] + [cl[a] + cl[b]]
    return d

def is_ultra(d, n):
    return all(d[(x, z)] >= min(d[(x, y)], d[(y, z)])
               for x in range(n) for y in range(n) for z in range(n)
               if len({x, y, z}) == 3)

def cell(d, n, r, x):
    return frozenset([x] + [z for z in range(n) if z != x and d[(x, z)] >= r])

def partition(d, n, r, strict=True):
    cells = {cell(d, n, r, x) for x in range(n)}
    if strict:  # cells must be disjoint (genuine partition)
        assert sum(len(c) for c in cells) == n, "NOT A PARTITION (hierarchy not nested)"
    return cells

def giant(C, n): return 2*len(C) > n

def family(d, n, r):
    """Transformed multiset C_j(r): actual nongiant cells + complement of giant."""
    P = frozenset(range(n)); fam = []; G = None
    for C in partition(d, n, r):
        if giant(C, n): G = C
        else: fam.append((C, 'act'))
    if G is not None: fam.append((P - G, 'comp'))
    return fam, G

def integrate(fn, bps):
    """Exact integral over R of a piecewise-constant dict-valued fn."""
    b = sorted(set(bps)); tot = {}
    for v in fn(b[0] - 1).values(): assert v == 0, "nonzero on (-inf,b0)"
    for v in fn(b[-1] + 1).values(): assert v == 0, "nonzero on (bK,inf)"
    for lo, hi in zip(b, b[1:]):
        for k, v in fn((lo + hi) / 2).items():
            tot[k] = tot.get(k, 0) + v * (hi - lo)
    return tot

def pos(t): return t if t > 0 else Fr(0)

class Toy:
    def __init__(s, n, d, fibers, lam, tau, H):
        s.n, s.d, s.fib, s.lam, s.tau, s.H = n, d, fibers, lam, tau, H
        s.E = [(x, y) for (x, F, h) in fibers for y in F]
        assert len(set(s.E)) == len(s.E)
        s.q = Fr(1, len(s.E)); s.B0 = Fr(n*(n-1), len(s.E))   # q <= B0*pi exactly
        s.w = [Fr(len(F), len(s.E)) for (x, F, h) in fibers]
        s.P = frozenset(range(n))
    def mu(s, F, C): return Fr(len(F & C), len(F))

    # ---------- global (occurrence-level) quantities for coordinate j ----------
    def glob(s, j):
        n, d, lam, tau = s.n, s.d[j], s.lam, s.tau
        Gl = {}  # giant at midpoint levels, for S_j
        def fn(r):
            fam, G = family(d, n, r)
            o = dict(W2=0, Acomp=0, EqL=0, EqLng=0, Tlarge=0, Tcomp=0, Tact=0,
                     comp_a_small=0, large_bound=0, S=[0]*n)
            for C, kind in fam:
                m = len(C); a = Fr(m, n); pi = Fr(m*(m-1), n*(n-1))
                qC = s.q * sum(1 for (x, y) in s.E if x in C and y in C)
                t = sum(wi*s.mu(F, C) for wi, (x, F, h) in zip(s.w, s.fib)
                        if x in C and s.mu(F, C) < lam)
                o['W2'] += pi; o['EqL'] += qC
                if kind == 'act': o['EqLng'] += qC
                else: o['Acomp'] += a
                if a >= tau:
                    o['Tlarge'] += t; o['large_bound'] += 2*lam*pi/tau**2
                    assert m >= 2 and t <= lam <= 2*lam*pi/tau**2   # (4.3) step
                elif kind == 'comp':
                    o['Tcomp'] += t; o['comp_a_small'] += a
                    assert t <= qC <= s.B0*pi <= s.B0*tau*a
                else:
                    o['Tact'] += t
            S = [Fr(1) if (G is not None and z not in G) else Fr(0) for z in range(n)]
            o['S'] = 0; o.update({('S', z): S[z] for z in range(n)})
            return o
        bps = list(d.values())
        res = integrate(fn, bps)
        res['A'] = sum(res[('S', z)] for z in range(n)) / n
        return res

    def Lng(self, j, x, y):
        """int 1{x,y share a NONGIANT actual j-cell at level r} dr."""
        n, d = self.n, self.d[j]
        def fn(r):
            C = cell(d, n, r, x)
            return {'L': Fr(1) if (y in C and not giant(C, n)) else Fr(0)}
        return integrate(fn, list(d.values())).get('L', 0)

    # ---------- per-fiber three-case split for coordinate j ----------
    def fiber(s, j, e, stats):
        n, lam, tau, H = s.n, s.lam, s.tau, s.H
        dj, dk = s.d[j], s.d[3 - j]
        x, F, h = s.fib[e]
        def fn(r):
            U = cell(dj, n, r, x); p = s.mu(F, U)
            Vm = cell(dk, n, h - r - H, x); Vp = cell(dk, n, h - r + H, x)
            assert Vp <= Vm                                   # V+ subset V-
            Dm = s.mu(F, s.P - (U | Vm)); Dp = s.mu(F, U & Vp)
            ret = (not giant(U, n)) and Fr(len(U), n) < tau and p < lam
            case = 1 if not giant(Vm, n) else (2 if not giant(Vp, n) else 3)
            o = dict(tot=p if ret else 0, c1=0, c2=0, c3=0, Dm=Dm, Dp=Dp,
                     Vm_ng=(s.mu(F, Vm) if not giant(Vm, n) else 0),
                     c1_Dm=0, c3_Dp=0, c3_rest=0, c2_raw=Fr(1) if case == 2 else 0)
            if ret:
                o['c%d' % case] = p
                if case == 1:
                    assert 1 - p <= s.mu(F, Vm) + Dm                 # cover
                    assert p <= 2*lam*(s.mu(F, Vm) + Dm)            # Case 1
                    o['c1_Dm'] = Dm
                    if not p <= lam*(s.mu(F, Vm) + Dm): stats['C3viol'] += 1
                    stats['n1'] += 1
                elif case == 2: stats['n2'] += 1
                else:
                    assert p == Dp + s.mu(F, U - Vp)                # Case 3 identity
                    o['c3_Dp'] = Dp; o['c3_rest'] = s.mu(F, U - Vp)
                    if p > 0: stats['n3'] += 1
            return o
        bps = []
        for z in range(n):
            if z != x:
                bps += [dj[(x, z)], h - H - dk[(x, z)], h + H - dk[(x, z)]]
        I = integrate(fn, bps)
        # exact identities of the proof
        Ey = lambda f: sum(f(y) for y in F) / len(F)
        S = lambda y: dj[(x, y)] + dk[(x, y)] - h                  # = Delta_j + Delta_j'
        assert I['Dm'] == Ey(lambda y: pos(h - dj[(x, y)] - dk[(x, y)] - H))
        assert I['Dp'] == Ey(lambda y: pos(dj[(x, y)] + dk[(x, y)] - h - H))
        assert I['Dm'] + I['Dp'] == Ey(lambda y: pos(abs(S(y)) - H))   # (4.4) integrand
        assert I['c2_raw'] == 2*H          # straddle set has length EXACTLY 2H
        assert I['c2'] <= 2*lam*H          # Case 2 bound
        assert I['tot'] == I['c1'] + I['c2'] + I['c3']
        assert I['c3'] == I['c3_Dp'] + I['c3_rest']
        # level change r' = h - r - H: int mu(V-)1{V- nongiant} dr = E_y L^ng_{j'}(x,y)
        assert I['Vm_ng'] == Ey(lambda y: s.Lng(3 - j, x, y))
        return I

    def Nj(s, j, y):
        n, d = s.n, s.d[j]
        vals = sorted({d[(y, z)] for z in range(n) if z != y})
        cells = [cell(d, n, v, y) for v in vals] + [frozenset([y])]
        small = [C for C in cells if len(C) < s.tau*n]
        for A in small:
            for B in small: assert A <= B or B <= A          # nested chain
        N = frozenset().union(*small)
        assert len(N) < s.tau*n
        return N

    def case3_levelchange(s, j, Igl):
        """Pointwise in r' = h_e - r + H: fiber-summed Case-3 mass <= the
        N_j(y) double sum <= B0*tau*alpha(P minus G_j'(r'))."""
        n, H, dk = s.n, s.H, s.d[3 - j]
        N = {y: s.Nj(j, y) for y in range(n)}
        def fn(rp):
            lhs = 0
            for e, (x, F, h) in enumerate(s.fib):
                r = h - rp + H
                U = cell(s.d[j], n, r, x); p = s.mu(F, U)
                Vm = cell(dk, n, h - r - H, x); Vp = cell(dk, n, h - r + H, x)
                ret = (not giant(U, n)) and Fr(len(U), n) < s.tau and p < s.lam
                if ret and giant(Vp, n):
                    lhs += s.w[e]*s.mu(F, U - Vp)
            fam, G = family(dk, n, rp)
            if G is None: r1 = r2 = Fr(0)
            else:
                r1 = sum(s.q for (x, y) in s.E if y not in G and x in N[y] and x != y)
                r2 = s.B0*s.tau*Fr(n - len(G), n)
            assert lhs <= r1 <= r2, (lhs, r1, r2)
            return dict(lhs=lhs, r1=r1, r2=r2)
        bps = list(dk.values())
        for e, (x, F, h) in enumerate(s.fib):
            for z in range(n):
                if z != x:
                    for b in (s.d[j][(x, z)], h - H - dk[(x, z)], h + H - dk[(x, z)]):
                        bps.append(h - b + H)
        return integrate(fn, bps)

def run_instance(seed, stats):
    rng = random.Random(seed)
    n = rng.randint(9, 15)
    d = {1: ultrametric(n, rng), 2: ultrametric(n, rng)}
    assert is_ultra(d[1], n) and is_ultra(d[2], n)
    fibers = []
    for x in rng.sample(range(n), rng.randint(3, n)):
        others = [z for z in range(n) if z != x]; rng.shuffle(others)
        k = 0
        while k < len(others) - 3 and rng.random() < 0.7:
            sz = rng.randint(3, min(9, len(others) - k)); F = frozenset(others[k:k+sz]); k += sz
            sums = sorted(d[1][(x, y)] + d[2][(x, y)] for y in F)
            h = sums[len(sums)//2] + Fr(rng.randint(-4, 4), 2)
            fibers.append((x, F, h))
    if not fibers: return None
    lam = rng.choice([Fr(1, 5), Fr(1, 3), Fr(2, 5), Fr(49, 100)])
    tau = max(Fr(2, n), rng.choice([Fr(2, n), Fr(1, 4), Fr(3, 8), Fr(1, 2), Fr(1)]))
    H = rng.choice([Fr(0), Fr(1, 2), Fr(1), Fr(2)])
    t = Toy(n, d, fibers, lam, tau, H)
    G = {j: t.glob(j) for j in (1, 2)}
    T = W2 = A = EqL = 0; act_fiber = 0; ERRm = ERRp = ERR44 = 0
    c = dict(c1=0, c2=0, c3=0, c1main=0, c1err=0, c3err=0, c3rest=0)
    for j in (1, 2):
        g = G[j]; k = 3 - j
        assert g['Acomp'] == g['A']                 # int of a over complements = A
        assert g['Tlarge'] <= g['large_bound']
        assert g['Tcomp'] <= t.B0*t.tau*g['comp_a_small'] <= t.B0*t.tau*g['A']
        T += g['Tlarge'] + g['Tcomp'] + g['Tact']; W2 += g['W2']; A += g['A']; EqL += g['EqL']
        for e in range(len(fibers)):
            I = t.fiber(j, e, stats); we = t.w[e]
            act_fiber += we*I['tot']
            for key in ('c1', 'c2', 'c3'): c[key] += we*I[key]
            c['c1main'] += we*2*t.lam*I['Vm_ng']; c['c1err'] += we*2*t.lam*I['c1_Dm']
            c['c3err'] += we*I['c3_Dp']; c['c3rest'] += we*I['c3_rest']
            ERRm += we*I['Dm']; ERRp += we*I['Dp']
            x, F, h = fibers[e]
            ERR44 += we*sum(pos(abs(d[j][(x, y)] + d[k][(x, y)] - h) - H) for y in F)/len(F)
        L3 = t.case3_levelchange(j, g)
        c3j = sum(t.w[e]*t.fiber(j, e, {'C3viol':0,'n1':0,'n2':0,'n3':0})['c3_rest'] for e in range(len(fibers)))
        assert L3['lhs'] == c3j                     # level change r'=h-r+H preserves the integral
        assert L3['r2'] == t.B0*t.tau*G[k]['A']     # integrates to B0 tau A_{j'}
        if L3['r2'] > 0: stats['c3ratio'] = max(stats['c3ratio'], float(L3['lhs']/L3['r2']))
    assert act_fiber == G[1]['Tact'] + G[2]['Tact']   # occurrence sum == per-fiber sum
    assert ERRm + ERRp == ERR44
    assert EqL <= t.B0*W2                           # q <= B0 pi
    assert c['c1'] <= c['c1main'] + c['c1err']
    assert c['c1main'] <= 2*t.lam*EqL
    assert c['c2'] <= 4*t.lam*t.H
    if c['c1main'] + c['c1err'] > 0: stats['c1ratio'] = max(stats['c1ratio'], float(c['c1']/(c['c1main'] + c['c1err'])))
    if t.H > 0: stats['c2ratio'] = max(stats['c2ratio'], float(c['c2']/(4*t.lam*t.H)))
    assert c['c3'] == c['c3err'] + c['c3rest']
    bound = (2*t.lam*W2/t.tau**2 + t.B0*t.tau*A                 # large + complements
             + 2*t.lam*t.B0*W2 + 2*t.lam*ERRm                    # Case 1
             + 4*t.lam*t.H                                       # Case 2
             + ERRp + t.B0*t.tau*A)                              # Case 3
    assert T <= bound, (T, bound)
    stats['inst'] += 1
    stats['ratio'] = max(stats['ratio'], float(T/bound) if bound else 0)
    for key in ('c1', 'c2', 'c3'):
        if c[key] > 0: stats['pos_' + key] += 1
    return True

def control_C1():
    """Fake fiber violating (3.3): targets have DIFFERENT raw sums h_y."""
    n = 9; rng = random.Random(7)
    d = {1: ultrametric(n, rng), 2: ultrametric(n, rng)}
    x = 0; F = frozenset(range(1, 9)); H = Fr(1)
    hy = {y: d[1][(x, y)] + d[2][(x, y)] + Fr(rng.choice([-3, 3]), 1) for y in F}  # true i1+i2
    he = sorted(hy.values())[len(hy)//2]       # the single level-change constant
    t = Toy(n, d, [(x, F, he)], Fr(2, 5), Fr(1, 2), H)
    I = t.fiber(1, 0, {'C3viol':0,'n1':0,'n2':0,'n3':0})
    true = sum(pos(abs(d[1][(x, y)] + d[2][(x, y)] - hy[y]) - H) for y in F) / len(F)
    return I['Dm'] + I['Dp'], true

def control_C2():
    """Coordinate j NOT nested (balls of a non-ultrametric d): N_j(y0) is large."""
    n = 20; dj = {}; dk = {}
    for a in range(n):
        for b in range(n):
            if a != b:
                dj[(a, b)] = Fr(5) if (0 in (a, b) and 1 <= a + b <= 12) else Fr(0)
                dk[(a, b)] = Fr(10) if (a and b) else Fr(0)
    ultra_j = is_ultra(dj, n)
    fibers = [(k, frozenset(range(n)) - {k}, Fr(5)) for k in range(1, 13)]
    lam, tau, H = Fr(1, 5), Fr(3, 20), Fr(1)
    t = Toy(n, {1: dj, 2: dk}, fibers, lam, tau, H)
    try:
        partition(dj, n, Fr(3)); part_ok = True
    except AssertionError: part_ok = False
    # Case-3 mass with U := ball, bypassing the partition requirement
    lhs = 0
    for e, (x, F, h) in enumerate(fibers):
        def fn(r):
            U = cell(dj, n, r, x); p = t.mu(F, U)
            Vp = cell(dk, n, h - r + H, x)
            ret = (not giant(U, n)) and Fr(len(U), n) < tau and p < lam
            return {'m': t.mu(F, U - Vp) if (ret and giant(Vp, n)) else Fr(0)}
        bps = [Fr(0), Fr(5), h + H - Fr(10), h + H]
        lhs += t.w[e]*integrate(fn, bps).get('m', 0)
    Ak = t.glob(2)['A']
    N0 = frozenset([0] + [k for k in range(1, 13)])   # union of the 'cells' {k,0}
    return ultra_j, part_ok, len(N0), tau*n, lhs, t.B0*tau*Ak

def show_example():
    for seed in range(17750, 20000):
        rng = random.Random(10_000 + seed)
        n = 8
        d = {1: ultrametric(n, rng, maxlev=6), 2: ultrametric(n, rng, maxlev=6)}
        x = 0; F = frozenset(rng.sample(range(1, n), 6))
        sums = sorted(d[1][(x, y)] + d[2][(x, y)] for y in F)
        h = sums[len(sums)//2] + Fr(rng.randint(-2, 2), 2)
        t = Toy(n, d, [(x, F, h)], Fr(2, 5), Fr(1, 2), Fr(1, 2))
        I = t.fiber(1, 0, {'C3viol':0,'n1':0,'n2':0,'n3':0})
        if not (I['c1'] > 0 and I['c2'] > 0 and I['c3_rest'] > 0 and I['Vm_ng'] > 0): continue
        if max(abs(d[1][(x, y)] + d[2][(x, y)] - h) for y in F) > 1: continue
        print("WORKED EXAMPLE (seed %d): n=8, source x=0, F=%s, h_e=%s, lam=2/5, tau=1/2, H=1/2, j=1" % (10_000+seed, sorted(F), h))
        print("  d_1(0,y):", {y: str(d[1][(0, y)]) for y in range(1, n)})
        print("  d_2(0,y):", {y: str(d[2][(0, y)]) for y in range(1, n)})
        print("  Delta_1+Delta_2 on F:", {y: str(d[1][(0, y)] + d[2][(0, y)] - h) for y in sorted(F)})
        bps = sorted(set(sum(([d[1][(0, z)], h - t.H - d[2][(0, z)], h + t.H - d[2][(0, z)]] for z in range(1, n)), [])))
        print("  %-13s %-16s %-6s %-6s %-6s %-5s %-5s %-4s" % ("r-interval", "U", "p", "D-", "D+", "case", "kept", "V+gt"))
        for lo, hi in zip(bps, bps[1:]):
            r = (lo + hi)/2
            U = cell(d[1], n, r, 0); p = t.mu(F, U)
            Vm = cell(d[2], n, h - r - t.H, 0); Vp = cell(d[2], n, h - r + t.H, 0)
            case = 1 if not giant(Vm, n) else (2 if not giant(Vp, n) else 3)
            kept = (not giant(U, n)) and Fr(len(U), n) < t.tau and p < t.lam
            print("  (%5s,%5s) %-16s %-6s %-6s %-6s %-5d %-5s %-4s" % (lo, hi, sorted(U), p, t.mu(F, t.P-(U|Vm)), t.mu(F, U & Vp), case, kept, giant(Vp, n)))
        print("  integrals: total kept p =", I['tot'], "= c1+c2+c3 =", I['c1'], "+", I['c2'], "+", I['c3'])
        print("  Case1 bound 2lam*int mu(V-)1{ng} + 2lam*int_{C1} D- =", 2*t.lam*I['Vm_ng'], "+", 2*t.lam*I['c1_Dm'])
        print("  Case2 bound 2*lam*H =", 2*t.lam*t.H, " (raw straddle length =", I['c2_raw'], "= 2H)")
        print("  Case3: c3 = int_{C3} D+ + int_{C3} mu(U\\V+) =", I['c3_Dp'], "+", I['c3_rest'])
        print("  int D- =", I['Dm'], " int D+ =", I['Dp'], " E(|Delta+Delta'|-H)+ =", I['Dm'] + I['Dp'])
        return
    print("no example found")

if __name__ == '__main__':
    show_example()
    stats = dict(inst=0, C3viol=0, n1=0, n2=0, n3=0, ratio=0.0, c3ratio=0.0, c1ratio=0.0, c2ratio=0.0,
                 pos_c1=0, pos_c2=0, pos_c3=0)
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 40)
    for sd in seeds: run_instance(sd, stats)
    print("instances passed (all exact assertions):", stats['inst'])
    print("instances with positive Case-1/2/3 mass:", stats['pos_c1'], stats['pos_c2'], stats['pos_c3'])
    print("retained level-intervals hit, cases 1/2/3:", stats['n1'], stats['n2'], stats['n3'])
    print("max T(lambda)/bound over instances: %.4f" % stats['ratio'])
    print("max Case-3 ratio (level-changed mass / B0 tau A_j'): %.4f" % stats['c3ratio'])
    print("max Case-1 ratio (actual / (2 lam E_q L^ng + 2 lam D-)): %.4f" % stats['c1ratio'])
    print("max Case-2 ratio (actual / 4 lam H): %.4f" % stats['c2ratio'])
    print("SHARPNESS: Case-1 levels violating p <= lam*(mu(V-)+D-) [factor 2 dropped]:", stats['C3viol'])
    a, b = control_C1()
    print("CONTROL C1 (fiber with non-constant i1+i2): int(D-+D+) = %s  vs  E(|Delta+Delta'|-H)+ = %s  -> %s"
          % (a, b, "MATCH (control did not fail!)" if a == b else "MISMATCH: identity rejects a non-fiber"))
    u, po, N, tn, lhs, rhs = control_C2()
    print("CONTROL C2 (non-nested j-'hierarchy'): ultrametric=%s partition=%s |N_j(y0)|=%d vs tau*n=%s;"
          " Case-3 mass %s (=%.4f) vs B0*tau*A_j' %s (=%.4f) -> %s"
          % (u, po, N, tn, lhs, float(lhs), rhs, float(rhs), "BOUND FAILS" if lhs > rhs else "bound holds (control did not fail!)"))
```

### Output (verbatim, 400 seeds; 3 seeds produced no fiber and were skipped)
```
WORKED EXAMPLE (seed 27750): n=8, source x=0, F=[1, 2, 3, 4, 5, 6], h_e=4, lam=2/5, tau=1/2, H=1/2, j=1
  d_1(0,y): {1: '1', 2: '1', 3: '1', 4: '1', 5: '7/2', 6: '1', 7: '1'}
  d_2(0,y): {1: '2', 2: '7/2', 3: '2', 4: '2', 5: '1/2', 6: '2', 7: '2'}
  Delta_1+Delta_2 on F: {1: '-1', 2: '1/2', 3: '-1', 4: '-1', 5: '0', 6: '-1'}
  r-interval    U                p      D-     D+     case  kept  V+gt
  (    0,    1) [0, 1, 2, 3, 4, 5, 6, 7] 1      0      0      1     False False
  (    1,  3/2) [0, 5]           1/6    2/3    0      1     True  False
  (  3/2,  5/2) [0, 5]           1/6    0      0      2     True  False
  (  5/2,    3) [0, 5]           1/6    0      0      3     True  True
  (    3,  7/2) [0, 5]           1/6    0      0      3     True  True
  (  7/2,    4) [0]              0      0      0      3     True  True
  integrals: total kept p = 5/12 = c1+c2+c3 = 1/12 + 1/6 + 1/6
  Case1 bound 2lam*int mu(V-)1{ng} + 2lam*int_{C1} D- = 1/5 + 4/15
  Case2 bound 2*lam*H = 2/5  (raw straddle length = 1 = 2H)
  Case3: c3 = int_{C3} D+ + int_{C3} mu(U\V+) = 0 + 1/6
  int D- = 1/3  int D+ = 0  E(|Delta+Delta'|-H)+ = 1/3
instances passed (all exact assertions): 397
instances with positive Case-1/2/3 mass: 217 221 307
retained level-intervals hit, cases 1/2/3: 2311 3968 3779
max T(lambda)/bound over instances: 0.1652
max Case-3 ratio (level-changed mass / B0 tau A_j'): 0.4286
max Case-1 ratio (actual / (2 lam E_q L^ng + 2 lam D-)): 0.3041
max Case-2 ratio (actual / 4 lam H): 0.5402
SHARPNESS: Case-1 levels violating p <= lam*(mu(V-)+D-) [factor 2 dropped]: 286
CONTROL C1 (fiber with non-constant i1+i2): int(D-+D+) = 23/8  vs  E(|Delta+Delta'|-H)+ = 2  -> MISMATCH: identity rejects a non-fiber
CONTROL C2 (non-nested j-'hierarchy'): ultrametric=False partition=False |N_j(y0)|=13 vs tau*n=3; Case-3 mass 5/19 (=0.2632) vs B0*tau*A_j' 1/8 (=0.1250) -> BOUND FAILS

real	0m39.140s
user	0m39.002s
sys	0m0.024s
```

## Summary (≤400 words)

Scope: §4 (pp. 12–14) — the setup (4.1), T(λ), Lemma 4.1 with its three branches (large cells, giant complements, actual
small cells) and three cases, the errors D± and (4.4), the per-fiber level changes r′ = h_e − r ∓ H_v, N_j(y), Tonelli, and
(4.5) W_{2,sm} = o(W+1); brief item (v).

Verdict: HOLDS AS READ. Every line checks. (4.1) is (3.6) integrated against q plus the marginal lower bound (2.2) and q ≤ B0π.
Giant-complement multiplicity is respected. The ∫D±
formulas are exact consequences of the fiber identity (3.3); (4.4) needs only the marginal tails (3.4) and a union bound. Case 1:
µ_e(V₋)+D⁻ ≥ 1−p > 1/2 ⇒ p ≤ 2λ(µ_e(V₋)+D⁻), then the per-fiber reflection r′ = h_e − r − H_v turns the main term into 2λE_qL_{j′}.
Case 2: the straddle set has length exactly 2H_v (empty at finite places). Case 3: p = D⁺ + µ_e(U∖V₊), V₊ = G_{j′}(r′) after
r′ = h_e − r + H_v, every counted source lies in N_j(y) (it shares U ∋ y with |U| < τn), and |N_j(y)| < τn because cells
containing y are a finite nested chain. (4.5) follows with explicit error sequences; directions are right and nothing is
circular (Lemma 4.1 uses only the upper half of (4.1)).

Objections: six, all COSMETIC — a vacuous "empty union allowed"/"N_j(y) ≠ ∅" (singletons always qualify since τn ≥ 2); the
Case-3 right side written without its implicit 1{giant exists}; an unused hypothesis H ≥ 1 (H ≥ 0 suffices; the Lean uses
0 ≤ H); a hypothesis attached to an unconditional identity before (4.1); (4.4) suppresses j and b1 = b0/2; Case 1's main-term
step compresses three true facts into one sentence. No FATAL, no GAP, no UNCLEAR.

Finite check: exact rational computation (Fraction) on 397 random instances with two ultrametric hierarchies and genuine
nonzero depth errors; all three cases exercised (positive mass in 217/221/307 instances); every exact identity of the proof holds
with zero discrepancy, including the r′-pointwise Case-3 inequality and the level-change integrals. Controls fail as they
should: a fiber violating (3.3) breaks the D± identity (23/8 vs 2); a non-nested "hierarchy" gives |N_j(y₀)| = 13 > τn = 3 and
Case-3 mass 5/19 > B0τA_{j′} = 1/8; five code mutants each trip an assertion.

§4 adds no Euclidean/characteristic-zero input beyond §3's (3.3), (3.4), (3.6).
