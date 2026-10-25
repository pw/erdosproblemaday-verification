# Hostile referee brief — OpenAI preprint "The weak pinned planar distance theorem" (23 Sep 2026, 27 pp), family 167, Erdős problem #604

ONE paper, anonymous author ("OpenAI"), github.com/openai/math `preprints/The-weak-pinned-planar-distance-theorem-September-23-2026/paper.pdf`
(sha256 6350959d…). Local copies: /tmp/oaimath/604/paper.pdf (PDF page number = printed page number) and /tmp/oaimath/604/paper.txt
(pdftotext -layout; displayed math is MANGLED — absolute-value bars, overlines, subscripts and fraction bars are often lost; when a
formula matters, Read the .pdf itself with `pages=` (it renders) and quote from the PDF). A Lean 4 formalization EXISTS and is catalogued:
/tmp/oaimath/604/lean-build/repo/lean/OAI/Geometry/PinnedDistances/ (48 files, 14,207 lines; Main.lean proves `OAI.WeakPinned.main`
= Theorem 1.1 with the comparator's statement, /tmp/oaimath/604/lean-build/repo/lean/ComparatorChallenges/PinnedDistances.lean;
Pins.lean proves `pins` (Corollary 1.2 as B n ε → 0) and `exists_pin_eventually` = the problem page's first question). Our kernel
replay is running in /tmp/oaimath/604/lean-build (steps.tsv) — do NOT run lean/lake yourselves (memory guard on this box); read the
Lean sources as text if your scope needs them.

THEOREM 1.1. For n ≥ 2, s > 0: F_n(s) = sup over n-point P ⊂ ℝ² of #{(x,y) ∈ P², x ≠ y, k_P(x,y) ≥ n^s} / (n(n−1)), where
k_P(x,y) = #{z ∈ P∖{x} : ‖z−x‖ = ‖y−x‖} (counts y itself). Claim: for every fixed s > 0, F_n(s) → 0. No rate.
COROLLARY 1.2 (half-page proof on p. 2): for every fixed ε > 0, sup_P #{x ∈ P : |D_x(P)| < n^{1−ε}}/n → 0, where D_x(P) is the set of
distinct nonzero distances from x. In particular every sufficiently large n-point planar set has a pin with ≥ n^{1−ε} distinct distances.

WHY THIS MATTERS. erdosproblems.com/604 ($500; page text saved at /tmp/oaimath/604/live_604.html): "Given n distinct points A ⊂ ℝ²
must there be a point x ∈ A such that #{d(x,y) : y ∈ A} ≫ n^{1−o(1)}? Or even ≫ n/√log n?" — the page's best known bound is
Katz–Tardos 2004, ≫ n^{c−o(1)} with c = (48−14e)/(55−16e) = 0.864137…; 0 proof claims; 1 comment (Hunter: one pin ⇒ ≫ n pins greedily);
last edited 23 March 2026. Corollary 1.2, if it holds, ANSWERS the first question YES (ineffectively) and says nothing about n/√log n.
Bloom's 8 Oct 2026 blog post lists #604 among 25 problems the release touches ("This proof has been formalised. The PDF is 27 pages long.")
with his standing caveat that he has read none of them. The "weak pinned distance conjecture" name is from Dewar–Frankl–Mansfield–Nixon–
Passant–Warren, arXiv:2505.06590v1, Conjecture 4.7 (saved at /tmp/oaimath/604/refs/dewar.txt): "For any ε > 0, there exists C_ε > 0 such
that for any finite P ⊆ ℝ² there exists q ∈ P which determines at least C_ε|P|^{1−ε} distances" — their Theorem 4.10 says the WEAK UNIT
DISTANCE conjecture implies it, and that hypothesis is now FALSE (OpenAI's n^{1+c} unit-distance construction, Lean-verified, May 2026), so
no implication route exists; this paper claims a direct proof.

ARCHITECTURE (read §1.2 first whatever your scope). Contrapositive + compactness. Suppose Θ(t) := limsup F_n(t) is positive somewhere;
s* = sup{t : Θ(t) > 0} ∈ (0,1]; fix 0 < c < s*/3, max{c,(1−c)s*} < s < s*, c < γ < s, s a continuity point of Θ (monotone ⇒ countably
many discontinuities), θ = Θ(s) > 0; everything below is along a sequence of configurations.
§2 Prop 2.2: configurations attaining F_N(s) (finite set of values ⇒ attained), transferred to REAL ALGEBRAIC coordinates keeping every
distance equality/disequality (transfer for real closed fields, [9] Kuhlmann notes Thms 3.1, 4.1); then a deletion process (discard fibers
< K_N = N^s/log N; delete vertices with in+out degree < 2(θ−η_N)(m−1); repeat) which cannot reach m₀ = ⌈N/2⌉ vertices (edge count vs
F_{m₀}(f_N) ≤ θ + b_N, Lemma 2.1 uniformity) ⇒ stops at n > N/2 with density d_n → θ, every fiber ≥ n^{s−o(1)}; (2.2) q ≤ B₀π,
q_X, q_Y ≤ B₀α, (q_X+q_Y)/2 ≥ (1−o(1))α pointwise; (2.3) targets of in-degree < n^γ have q_Y-mass O(n^{γ−1}); (2.4) the SUBSET ESTIMATE:
for every C ⊂ P with m = |C|, p_e = µ_e(C): E_e 1_C(x_e) p_e 1{p_e ≥ λ_n} ≤ (1+o(1))π(C²) if m > n^{1−c}, ≤ o(1)π(C²) if m ≤ n^{1−c},
uniformly in C (λ_n = 1/log n; uses T_n = λ_n K_N ≥ n^{s−δ_n}, Lemma 2.1, and Θ(s′) = 0 for s* < s′ < s/(1−c)).
§3 Z₁ = u+ib, Z₂ = u−ib on real points (injective); t(x,y) = (Z₁(y)−Z₁(x))(Z₂(y)−Z₂(x)) (3.1); number field K ∋ i containing all coordinates;
normalized product formula (3.2) Σ_v σ_v log|z|_v = 0, Σ_{v|∞} σ_v = 1 (Milne ANT Thms 7.14–7.15, Lemma 8.6); raw depths
i_j(x,y) = −log|Z_j(x)−Z_j(y)|_v; fiber identity (3.3) i₁+i₂ = h_e on a fiber. §3.2 nested partitions: ultrametric at finite places;
at complex places random square grids (random orientation, side e^ξ 2^m with ξ uniform on [0, log 2), uniform shifts, nested by adding 0 or
l_m); d_j = sharing depth; Lemma 3.1: Δ_j = d_j − i_j has a law independent of the pair/place/configuration, mean κ, tails
Pr(|Δ| > u) ≤ C₀e^{−b₀u} (3.4). §3.3 giant replacement (a cell of size > n/2 replaced by its complement, multiset); M_j, S_j(x),
L_j(x,y); Lemma 3.2 identity (3.5) d_j(x,y) = M_j + L_j(x,y) − S_j(x) − S_j(y). §3.4 ⟨·⟩ = Σ_v σ_v E_grids; product formula + Lemma 3.1 ⇒
⟨d₁+d₂⟩ = 2κ ⇒ the ADDITIVE IDENTITY (3.6) L*(x,y) = b* + S*(x) + S*(y) ⇒ any signed pair law with zero mass and zero marginal sum
integrates to 0 against L*. Scales W₂ = E_π L*, A = E_α S*, W = W₂ + A.
§4 Lemma 4.1: T(λ) = I(E_e 1_C(x_e) p 1{p<λ}) ≪ (λ/τ² + λ)W₂ + τA + λH + e^{−b₁H}; proof separates large cells / giant complements / actual
small cells, the last via the COMPLEMENTARY coordinate: V± = cells of x in Π_{j′}(h_e − r ∓ H_v); errors D± with ∫(D₋+D₊)dr =
E_{y∼µ_e}(|Δ_j+Δ_{j′}| − H_v)₊ (4.4); three cases (V₋ nongiant / V₋ giant V₊ not / V₊ giant), the last using N_j(y) = union of small
actual j-cells containing y, |N_j(y)| < τn. Then (4.5) W_{2,sm} := I(π(C²)1{|C| ≤ n^{1−c}}) = o(W+1) via (2.4) and (4.1).
§5 Lemma 5.1 (VARIANCE): for a weighted family of uniform laws ν on subsets B of size k ≥ n^γ with E_F ν ≤ Mα:
I[E_F (p−a)² 1{m>n^{1−c}} + p² 1{m≤n^{1−c}, p≥2/k}] ≤ C_M n^{c−γ} W₂ + W_{2,sm} = o(W+1). Exact signed identity P_B − 2R_B + π
(R_B: X∼ν, then Y ∈ B∖{X} w.p. k/n else uniform outside B; marginals ν and α) ⇒ (5.3) I(P_B(C²) − 2R_B(C²) + π(C²)) = 0; (5.4)
H_B(C) = (p−a)² + (2k/n − 1)p(1−p)/(k−1) − a(1−a)/(n−1); cases m > n^{1−c} (5.6), 2 ≤ m ≤ n^{1−c} (5.7), m ∈ {0,1} exact zero.
Applied to fibers (weights k_e/|E|, E_e µ_e = q_Y) and to incoming laws ρ_y (targets with d_y ≥ n^γ, weights q_Y(y)), (5.8).
§6 W → ∞: (6.1) W₂ ≥ c₁W (via (6.2) S*(x) ≥ A − 2W₂ and (6.3)/(6.4)); (6.5) cells with α-mass in (δ, 1−δ) carry ≫ W; Lipschitz
weight w; ℓ_j = ∫Σ_B w(α(B)) dr; (6.6) W ≪ ⟨ℓ₁+ℓ₂⟩ ≪_δ W; (6.7) weight-swap and imbalance = o(W); cut distances D_j^ν(a₀,a₁), (6.8),
(6.9) with the formal endpoint ∞; FIBER EQUATION (6.10) i_{j′}(y,z) = i_j(y,z) − i_j(x,z) + h_e − i_j(x,y) for z in the fiber of (x,y)
⇒ (6.11) E_q|D_j(x,y) − D_{j′}(∞,y)| = o(W); §6.3 D_j is a path metric on the cell tree; tree transport formula (6.12) [5]; (6.13);
coupling argument ⇒ (6.14) E_{x,x′,y iid α}|D_j(x,y) − D_j(x′,y)| = o(W); Lemma 6.1: on a tree of total length L with every positive
edge separating α-mass ≥ δ/2 on both sides, E|d(X,Y) − d(X′,Y)| ≥ δ²L/(32(⌈16/δ⌉+1)) ⇒ W ≪ o(W), contradiction.
§7 W bounded: pick an archimedean place with T_v ≤ 2C+1 and V_v ≤ 2η_n (Markov on the weights); normalize U_j = e^{m_j}Z_j + b_j
with m_j = E_π i_j; (7.1) E_π log|U_j(x)−U_j(y)| bounded (CHECK IN THE PDF whether it is |log| — (7.3) needs the NEGATIVE part of log,
(7.2) the positive part); (7.2) tails, (7.3) small balls ⇒ subsequential weak limits β_j on the Riemann sphere are NONATOMIC with no
mass at ∞ (Portmanteau, [14]); §7.2 (7.4)–(7.5): fiber laws and incoming laws converge to the same β_j in family mean; §7.3 joint limit Q
of (U₁(x),U₂(x),U₁(y),U₂(y),(U₁)_*µ_e,(U₂)_*µ_e): a ∼ β₁ INDEPENDENT of (a′,b′); a ≠ a′, b ≠ b′, a′ ∈ supp β₁, b′ ∈ supp β₂ a.s.;
(7.6) β₂ = Φ_*β₁ with Φ(z) = b + t′/(z−a), t′ = (a′−a)(b′−b) (Möbius, det −t′ ≠ 0, closed-graph + Portmanteau); Lemma 7.1: no such
law exists — J_w(X) = ∫ w(Pr(X ≥ u)) du is translation invariant and → 0 under convergence in probability (7.7); −log|Φ(z)−b′| =
log(|z−a|/|z−a′|) − log|b′−b| ⇒ (7.8); independence + Fubini ⇒ for a.e. (a′,b′) the identity holds for β₁-a.e. a; a_k → a′ in supp β₁
⇒ LHS → 0 while RHS is a fixed positive number.

WHERE THE PROOF GOES BEYOND THE STATE OF THE ART (test these hardest):
(i) THE CHARACTERISTIC-ZERO / EUCLIDEAN INPUT. Over F_q, P = F_q² has q = √n distances at EVERY pin, so a correct proof must use something
false there. Name every step that uses: the reals (Z₁, Z₂ injective; t ≠ 0 for distinct points), the number field (product formula), the
ARCHIMEDEAN place (§3.2 grids; §7's normalization, Σ_{v|∞}σ_v = 1). Then ask what the argument proves VERBATIM for any finite P ⊂ K²
(K a number field) with two injective coordinate maps Z₁, Z₂ and all products (Z₁-difference)(Z₂-difference) nonzero — e.g. the
Minkowski form u² − b² on real sets with no two points on a common isotropic line, or complex "distances" in ℂ². Is THAT statement
known to be true, open, or FALSE anywhere in the literature (pseudo-Euclidean pinned distances; Dewar et al. treat pseudo-Euclidean
metrics; "Minkowski grid" arXiv:2607.05374)? A known counterexample to the generalized statement would be FATAL; its absence is not a proof.
(ii) PROP 2.2's deletion process and the SUBSET ESTIMATE (2.4): redo the edge-count contradiction with the constants (A_N, B_N, t_N, η_N);
is Lemma 2.1 used with the right quantifiers (uniform in m ≥ M_N); is "a restricting vertices never splits a fiber" right (same source AND
same squared distance); in (2.4) for m ≤ n^{1−c}, is Θ(s′) = 0 with s′ > s* legitimately applied to SUBSETS C of a configuration (F_m is a sup
over all m-point sets, so yes — but check the pair count counts pairs IN C with k_C ≥ T_n, i.e. fibers restricted to C, vs k_P).
(iii) LEMMA 3.1 and the GRID ERROR: is the law of Δ really pair-independent (random orientation + log-uniform scale + uniform shifts +
the nested-shift rule); is (3.4) two-sided; mean κ finite; is Lemma 3.2's (3.5) right on the ray where the giant exists (sign of S, the
multiset doubling of a cell equal to a giant's complement, Figure 1); is the "giant exists on an initial ray" claim right (nested ⇒ yes).
(iv) THE ADDITIVE IDENTITY (3.6): it needs ⟨i₁+i₂⟩ = 0 on every distinct pair (product formula on t(x,y) ≠ 0) and E Δ_j = κ at every
complex place with Σσ_v = 1. Check the normalization of |·|_v and σ_v against Milne (finite places: |p|_p = p^{−1} extended, σ_v =
[K_v:Q_p]/[K:Q]; complex: ordinary modulus, σ_v = 2/[K:Q]) — the paper says "the weights convert the norm-based absolute values and
squared complex moduli"; verify that Σ_v σ_v log|z|_v = 0 is exactly Milne's product formula divided by [K:Q], including the factor 2 at
complex places.
(v) LEMMA 4.1's three cases: the level change r′ = h_e − r ∓ H_v per fiber and Tonelli; Case 2's "length at most 2H_v"; Case 3's
|N_j(y)| < τn (nested chain of cells of size < τn — the union of a nested chain is its largest member, fine — but is every counted
source really in N_j(y)?); the claim that giant complements are handled by the a < τ branch with multiplicity; then (4.5) from (2.4)+(4.1).
(vi) LEMMA 5.1: verify (5.4) EXACTLY (algebra), (5.6), (5.7), the singleton tails, and that the integrability/Tonelli claims hold; then the
two applications (5.8). A finite exact check of (5.3)/(5.4) on small explicit instances is cheap — do it with a control that fails.
(vii) §6: (6.2)–(6.5) with their constants; (6.7) both terms; (6.8)/(6.9) the cut formula incl. the endpoint ∞; (6.10) the fiber equation
(derive it from (3.1) yourself); (6.11)'s error accounting; the transport formula (6.12) and the coupling chain to (6.14); Lemma 6.1's
constant (verify on random trees numerically with a failing control) and whether its hypothesis ("every positive edge separates α-mass ≥
δ/2 on both sides") really holds for the w-weighted tree (w = 0 below δ/2).
(viii) §7: (7.1)–(7.3) (absolute values!); the selected-place Markov argument; (7.4)–(7.5) uniformity N(R,ε) and the giant-complement
occurrence; §7.3 independence of a from the PAIR (a′,b′) (why the pair and not just a′); the passage of the Möbius identity to the limit
(is the equality graph closed on the open domain; is the complement open; zero prelimit mass); Lemma 7.1 line by line incl. (7.7) and the
existence of a_k → a′ inside the full-measure set.
(ix) PROVE-TOO-MUCH / QUANTIFIERS: Theorem 1.1 is "for each fixed s"; Θ and s* are defined without any other parameter — check nothing
circular; the contradiction kills every subsequence (bounded or → ∞) — is "every sequence has a bounded or divergent subsequence" applied
to W ≥ 0 correctly; could the argument prove a RATE (it says not) or n/√log n (it must not — the lattice shows n^{1−o(1)} is the ceiling
of this method's shape? no: the lattice has n/√log n at every pin; ask only whether the paper CLAIMS more than it proves).
(x) COROLLARY 1.2's half-page proof: redo the counting; "fewer than n^{1−ε+s} neighbors lie in classes of size < n^s" (classes counted at
the pin); the bound b/n ≤ (n−1)F_n(ε/2)/(n−1−n^{1−ε/2}); the ε ≥ 1 remark. And the Lean's version (Pins.lean, bad_fraction_bound: factor 2).

Classic holes to hunt: quantifier/parameter order; "clearly"/"it follows"/"similarly"/"the same argument" at a hard step (count them in your
scope and check each); inequalities used in the wrong direction; a probability called EXACT that is approximate; an o(1) that depends on the
configuration; a limit taken before a sup; a "subsequence" that forgets a previously fixed subsequence; a lemma applied outside its
hypotheses (sizes k ≥ n^γ, m thresholds, λ < 1/2, τ ≥ 2/n).

OUTPUT — write /tmp/oaimath/604/seats/referee_<YOURTAG>.md containing:
- Objections, numbered. Each: location (section / lemma / equation / PDF page), the quoted sentence(s) VERBATIM (from the PDF), what is
  wrong or unverifiable, severity FATAL / GAP / UNCLEAR / COSMETIC, what would fix it. For FATAL/GAP say whether it is a gap in the PROOF
  or in the EXPOSITION (the Lean, if it compiles, settles the theorem regardless — your job on the paper is the human-readable proof).
- For each lemma/proposition/equation in your scope: VERIFIED LINE BY LINE / SKIMMED / NOT READ. This distinction is the deliverable.
- Any finite check you ran: the script VERBATIM, its output, and a control that FAILS (a deliberately wrong input the check rejects).
  Python is fine; keep every run under a minute and under 1 GB (the box carries live solvers); never run lean/lake.
- Citation table for your scope (if any): cited result → what the paper claims it says → what the source actually says (quote) →
  MATCH / MISMATCH / COULD NOT FETCH. Fetch primary sources with curl/pdftotext (arXiv current version) or WebFetch.
- Verdict for your scope: HOLDS AS READ / GAP AT <location> / COULD NOT CHECK <what, why>.
Be concrete, quote, no "the authors should clarify". A machine wrote this; it will not be clarifying. Finish with a ≤400-word summary in
your final message (the file is the full report).
