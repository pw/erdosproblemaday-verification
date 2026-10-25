# Referee report — seat `construct` — sib1 §3 (pp. 5–9) + §4 (pp. 9–14)
Paper: "Asymptotically minimal maxima of real Littlewood polynomials" (sib1, 23 Sept 2026, /tmp/oaimath/076/sib1/paper.pdf)
Seat started 2026-10-12. Status: COMPLETE.

## Scope read (pages)
sib1 pp. 5–14 in full from the PDF render (§3: preamble, Lemma 3.1, Theorem 3.2, proof of Lemma 3.1 incl. geometry;
§4: Prop 4.1, Lemma 4.2 and proof, proof of Prop 4.1 through "These are all the assertions" and the closing paragraph on
p. 14). For the interfaces only: p. 4–5 (Prop 2.1, K_δ, proof of Thm 1.1 — not audited), p. 15 Lemma 5.1's use of Lemma 4.2,
p. 16 the application of Lemma 3.1/Prop 4.1 ((32)–(35)), p. 18 line using (1−3δ)².

## Method
Read pp. 4–14 from the PDF render (displayed math) cross-checked against layout text; re-derive each inequality; fetch Alon–Yuster
2005 for the quoted Pippenger–Spencer form.

## Findings (running)

### [partial, ~T+12min] External input fetched
- Alon–Yuster, "On a hypergraph matching problem", Graphs Combin. 21 (2005) 377–384 — FETCHED as the author's PDF
  https://web.math.princeton.edu/~nalon/PDFS/ayhyper2.pdf (linked from Alon's publication list; 6 pp; sha256 39adbd2b…;
  saved refs/alon_yuster_2005/paper.pdf + .txt). This is the author manuscript, not the journal typeset version.
  Their Lemma 2.1 verbatim: "For an integer r ≥ 2 and a real γ > 0 there exists a real β = β(r, γ) so that the following holds:
  If an r-uniform hypergraph S has the following properties for some t: (i) (1 − β)t < d(x) < (1 + β)t holds for all vertices,
  (ii) d(x, y) < βt for all distinct x and y, then q(S) ≤ (1 + γ)t." (q(S) = chromatic index = least number of matchings
  partitioning the edges.) sib1 Theorem 3.2 (p. 6) matches this statement (strict inequalities both sides, codegree < βt,
  conclusion "at most (1+γ)t matchings"). The paper adds "β > 0" and "t > 0" — harmless. Note: the 1989 Pippenger–Spencer
  original (paywalled, NOT fetched) carries a D ≥ D₀ hypothesis; AY's form drops it. It can be absorbed by shrinking β (codegree
  < βt with any two intersecting edges forces t > 1/β), and in sib1's application t = D_q → ∞ anyway, so this is immaterial.
  The proof of Lemma 3.1 in fact only uses the corollary "some colour class has ≥ (1−o(1))|E|/D_q edges", i.e. a near-perfect
  matching (Frankl–Rödl/Pippenger level), weaker than the colouring statement.

### [partial, ~T+35min] Lemma 3.1 (pp. 5–9) — read line by line; HOLDS
Re-derived every step; notes per step (all checks passed unless flagged):
- Slot lengths (p.6, (4)): α_i>2w_i, Σα_i=1 possible since 2Σw_i<1; odd L_i≈Tα_i give L_i/(2L)→α_i/2>w_i. OK.
- Ranks: b=rank_Q≥2 (two nonparallel nonzero rows); for q not dividing one nonzero b×b minor and one nonzero 2×2 minor per pair,
  rank_Fq = b (cannot exceed b) and every pair has rank 2 (so also every a_i ≢ 0). OK.
- p=1/(2L) exact for interior folded sites (6): exactly one shift mod L puts a type-j middle site at c; L_j<L so the slot lies
  in the chunk when c is ≥L from both ends; orientation 1/2. OK.
- Simple r-uniform hypergraph: vertices are typed slots, so the tuple ↔ r-set map is injective; each compatible tuple has
  exactly q^{m−b} solutions (kernel of the rank-b map). Degree (7) d=q^{b−1}Z_{i,s}: y ↦ tuple is well defined because a
  type-j oriented centre determines its slot uniquely, and each tuple has exactly q^{m−b} preimages in the fibre. OK.
  Codegree (8) ≤ q^{m−2}/q^{m−b}=q^{b−2} by pair rank 2. OK. q^{b−2}/D_q = 1/(p^{r−1}q) → 0. OK.
- Exceptional set (9)–(10): c is unique (a_i≢0) and nonzero (pair rank 2); |E_i| ≤ 2·C(r−1,2)·2R = O(R). OK.
- Collision logic (p.7–8): two residues folding into one chunk ⇒ |u|_q−|u'|_q ∈ (−R,R) ⇒ u+u' or u−u' has folded value ≤ R
  (the text says "at most R"; it is < R — immaterial). (a_j±a_l)·y on the fibre is uniform unless a_j±a_l ∈ span_Fq(a_i), in
  which case it is the constant cs with |cs|_q>R for s∉E_i. Relations among ≥3 forms other than a_j±a_l=c·a_i are irrelevant
  because only sums/differences decide a chunk collision. This is exactly the "pairwise nonparallel suffices" claim: VERIFIED.
- τ_q=(1+4LK+2R)/q: ≤2L noninterior sites per chunk (≤2L also for the short chunk), ×2 for negatives, +0, +2R for Q_s. OK.
  (11): u(r−1)τ_q + 2·C(u(r−1),2)(2R+1)/q; cross-copy pairs (incl. j=l) are sums/differences of independent uniforms. OK.
- (12)–(13): on the good event the r−1 (resp. 2(r−1)) indicators live in distinct chunks ≠ Q_s, each exactly p, independent
  of each other and of V_{i,s}; bad event contributes in [0,1]. Hence E[(Z−p^{r−1})²|V]=O(q^{−1/2}). OK.
- Chebyshev with ε_q=q^{−1/8}: O(q^{−1/2})/(ε_q²p^{2(r−1)}) = O(q^{−1/4}); expected atypical ≤ r(q−1)·O(q^{−1/4}) = O(q^{3/4});
  exceptional O(q^{1/2}) deterministically; Markov ⇒ a realization with ≤ q^{7/8} bad vertices. Deleting them costs any
  survivor ≤ q^{7/8}·q^{b−2} = O(q^{−1/8}D_q) edges. All survivors then satisfy Thm 3.2's two-sided degree condition with
  t=D_q and codegree o(D_q) — every vertex, as AY's Lemma 2.1 requires (no exceptional-vertex allowance needed). OK.
- Matching size (14): |E|=(1/r)Σd(v)=(1+o(1))v_qD_q/r, ≤(1+γ)D_q colours ⇒ a class with ≥(1−o(1))q/(2L) edges; upper bound
  by #type-1 vertices. Only the LOWER bound matters for w_i/H<L_i/q, and it holds for large q by the strict inequality (4). OK.
- Geometry (p.9): θ_h=y_h/q ⇒ a_i·θ_h ≡ ±c/q (mod 1), c∈[1,n], so both signed centres are c/q and −c/q regardless of
  orientation, never equal (2c≢0 mod q) — the ±a degenerate case (centre 0 or 1/2) cannot occur. Positive slot intervals
  ⊂[1/(2q),1/2], reflections ⊂[1/2,1−1/(2q)]; interiors pairwise disjoint (slots are disjoint site sets; distinct matching
  edges use distinct slots; different types are different slots). Closed interval of length w_i/H < L_i/q centred at c/q lies
  in the open interior. Disjointness is EXACT, not asymptotic, including at 1/2 and across 0. OK.
- H and θ_h depend only on (a_i, w_i) (via q); nothing involves N. The interface p.16 (34) uses I_{a,h} = a·θ_h ± |λ_a|/(2H)
  for all a∈A = {±a_i}, which is precisely Lemma 3.1's conclusion with w_i=|λ_{a_i}|. OK.

### [~T+55min] §4 — Lemma 4.2 (pp. 10–11) — HOLDS
- Completing the square (x0=u/(Tβ)) checked; Gaussian ∫exp(−πa y²+2πiξy)dy = a^{−1/2}exp(−πξ²/a), Re a>0, principal branch;
  limit (−iTβ)^{−1/2} = (T|β|)^{−1/2}e(sgnβ/8) and exp(−πξ²/(−iTβ)) = e(−ξ²/(2Tβ)) checked. Re(1/(ρ−iTβ))=ρ/(ρ²+T²β²)>0 so
  the multiplier has modulus ≤1; Fubini under the damping and both dominated-convergence passages are legitimate (ĝ Schwartz,
  g compactly supported). Error: |e(θ)−1| ≤ 2π|θ| gives exactly π(T|β|)^{−1}∫ξ²|ĝ|.
- "Uniform in what": uniform in every real u (the bound does not see x0). The O_{g,β}(T^{−1}) is honest and in fact explicit:
  π‖ξ²ĝ‖₁/(T|β|); it is valid for every T>0, not only asymptotically. Its uses — §4 with T=B, β=β_{s,j} (finitely many) and
  §5 Lemma 5.1 with T=N, β=λ_a, u=N(ℓ−b+λx*) (finitely many, uniformity in u is what makes Lemma 5.1 uniform in t) — need
  exactly this. Numeric sanity (nice python, bump g on (−.45,.45)): max over u of |error| = 8.9e-2/3.3e-2 at T=50/200, β=1
  (bound 0.24/0.061); 0.11/0.044 at β=−0.7 (bound 0.35/0.087). Consistent.

### §4 — Proposition 4.1 (pp. 9–14) — HOLDS
- (19)–(20): |p_j| ≤ |p_{j−1}| + 1−|p_{j−1}| ≤ 1; mean zero by integrating y_j; M_j = M_{j−1} + (1/8)∫(1−p²_{j−1})² ≥ M_{j−1} +
  (1−M_{j−1})²/8 by Jensen; M_j ↑ 1. Numerically M_1=1/8, coefficient of e(y_2) in p_2 = 7/32 (exact), M_2=0.22168 ≥ 0.22070.
- Support structure: new frequencies have coordinate j equal to ±1, old ones have it 0 ⇒ last nonzero coordinate ±1 ⇒ parallel
  elements of S are equal or opposite; S = {±s_1..±s_D}, D ≥ 2 (e_1 coefficient 1/4 from p_1, e_2 coefficient 7/32, persisting). OK.
- Curvatures: b_j^0 ∈ s_j^⊥ avoiding the proper subspaces s_j^⊥∩s_l^⊥ (proper because s_l,s_j independent; d ≥ D ≥ 2); denominators
  s_j·b_l^0 ≠ 0; Δ_{s_j}/τ = (s_j·b_j^1)Π_{l≠j}|s_j·b_l^0+τ s_j·b_l^1| → |c_{s_j}|²/ρ_{s_j}; same for −s_j (Δ, |c|, ρ even).
  (21) with positive lower bound forces every β_{s,j} ≠ 0. OK.
- Spreading (22)–(24): G real, smooth on T^{d+D} (g compactly supported in (−1/2,1/2)), |G| ≤ 1, ‖G‖²₂ = M_d(∫g²)^D ≥ (1−δ)²;
  Ĝ(s,u) = c_s Π_j I_{s,j}(u_j) with β_{s,j}=s·b_j — recomputed. (25) from Lemma 4.2 with |g| ≤ 1: (1+O(1/B))^D ≤ 1+δ. OK.
- Boxes (26): |U_s| = Π(2⌊B|β|/2⌋+1) ≤ Π(B|β|+1) ≤ (1+δ)B^DΔ_s. U_{−s} = U_s = −U_s since β_{−s,j} = −β_{s,j}. OK.
- Tail (27)–(29): for |w| > B|β|/2, |Bβx−w| ≥ (1−2α)|w| ≥ c(B+|w|) with c = (1−2α)|β|/(2+|β|); l integrations by parts give
  terms (Bβ)^h g^{(k)}/φ'^{l+h}, bounded by C_l(B+|w|)^{−l}; outside sum O(B^{1−l}), full sum O(B); union over the D coordinate
  complements gives O(B^{D−l}) → 0 for l > D. G smooth ⇒ absolutely convergent Fourier series ⇒ ‖G−T_B‖_∞ ≤ discarded mass ≤ δ.
- Budgets (p.14): ‖F‖_∞ ≤ (1+δ)/(1+δ) = 1; ‖F‖₂ ≥ (1−δ−δ)/(1+δ) ≥ 1−3δ (since (1−3δ)(1+δ) = 1−2δ−3δ²). F real (symmetric retained
  set + G real). A symmetric, nonzero, pairs equal-or-opposite (projection to first d coords), r ≥ D ≥ 2. λ_a = ρ_s/(τB^D(1+δ)³) > 0;
  Σ_A|λ_a| ≤ Σ_s(1+δ)B^DΔ_sρ_s/(τB^D(1+δ)³) ≤ Σ_s|c_s|²/(1+δ) = M_d/(1+δ) < 1; |F̂(a)|²/|λ_a| ≤ |c_s|²τ(1+δ)³/(Δ_sρ_s) ≤
  (1+δ)³/(1−δ) = K_δ². All re-derived; K_δ = sqrt((1+δ)³/(1−δ)) as printed in (16) and in Prop 2.1.
- Interface: §5 (32)–(33) quotes exactly (15)–(16); p.18 uses ‖F‖₂² ≥ (1−3δ)² (the L² NORM bound is squared correctly there:
  (1−δ)(1−3δ)² ≥ 1−7δ). 2Σw_i = Σ_A|λ_a| < 1 is exactly Lemma 3.1's hypothesis.

### Constant-dependency chain (tested for cycles)
δ → d (M_d ≥ 1−δ) → S, c_s, D → γ → b_j^0, b_j^1 → τ (21) → g (needs D, δ) → l > D, B (needs g, all β_{s,j}, D, l, δ) → F, A, m, r, v
→ [Lemma 3.1] α_i, L_i, L → γ_PS, β_PS(r,γ_PS) → prime q (needs forms, L_i, β_PS) → H, θ_h → [§5] cutoffs χ_h → N. Each object is
chosen after everything it depends on; nothing in §3–§4 depends on N, and H is fixed before N (no divisibility H | N is used in
(35): blocks are [(h−1)/H, h/H) in x = k/N). No cycle found. Large r (≈ B^D-many modes) only makes p^{r−1} astronomically
small but FIXED; all O(·) in Lemma 3.1 are as q → ∞ with that data fixed, which the proof states ("All constants implicit …
may depend on the fixed forms and the fixed slot lengths").

## Findings
FATAL: none. GAP: none.
EXPOSITION (all harmless, repairable in one line):
- E1 (p.7, last paragraph): "If two residues fold into one chunk, the difference of their folded sites has absolute value at most
  R." — it is at most R−1 (chunks have ≤ R sites); the subsequent "(2R+1)/q" bound is then slightly generous. No effect.
- E2 (p.10, Lemma 4.2): stated "As T → ∞ … + O_{g,β}(T^{−1})", but the proof gives an exact, explicit bound π‖ξ²ĝ‖₁/(T|β|) valid
  for every T > 0. Stating it that way would make the uniformity claim self-evidently non-circular. No effect.
- E3 (p.6, Theorem 3.2): Pippenger–Spencer's original carries a D ≥ D₀ hypothesis that the quoted (AY) form omits; this is
  harmless (absorbable by shrinking β, and t = D_q → ∞ in the application) but the paper does not remark on it.
- E4 (p.8): "The vertices with centers in some E_i number O(q^{1/2})" means type-i vertices whose centre lies in E_i (a
  vertex is typed); wording only.
- E5 (p.5, §3 preamble): the "asymptotic bound |c|/√|λ|" and the width |λ|/H are heuristic here; their rigorous form is
  Lemma 5.1 + (36) on pp. 15–16 (outside my scope). The preamble is consistent with what §5 later uses.

## External inputs checked (source, version, exact statement vs use)
- Alon–Yuster 2005, Lemma 2.1 — FETCHED (author PDF ayhyper2.pdf from Alon's Princeton publication list; not the journal
  typeset copy). Statement quoted above; sib1's Theorem 3.2 matches it (same strict two-sided degree window, codegree < βt,
  ≤ (1+γ)t matchings). Applied with t = D_q to a hypergraph in which EVERY vertex satisfies the window (after deletion) — the
  hypotheses are met at the exact point of use. sib1 only needs the weaker consequence "a matching of ≥ (1−o(1))|E|/D_q edges".
- Pippenger–Spencer 1989 (JCTA 51, 24–42) — NOT FETCHED (paywalled); not needed given AY's statement.
- Bombieri–Bourgain [5, §2, Eq. (2.2)] — NOT CHECKED; cited only as "also appears", Lemma 4.2 carries a complete
  self-contained proof, so the citation is not load-bearing.
- Frankl–Rödl [13] — cited for lineage only; not load-bearing; not checked.

## What I skimmed / did not check
- §5 beyond the interface lines listed (Lemma 5.1's proof, (36)'s endpoint analysis, the non-stationary blocks, the
  mean-square recovery) — that is the `sample` seat's scope. I only confirmed §5 consumes Lemma 3.1/Prop 4.1 with matching
  hypotheses and constants.
- I did not construct a concrete instance of Lemma 3.1 numerically (q would have to be astronomically large for r ≈ |A|/2
  modes); the proof was checked by hand only. Numerics done: Lemma 4.2 error vs its bound; M_1, M_2 and the 7/32 coefficient.
- The Lean formalization of §3–§4 (lean seat).

## Verdict
HOLDS AS READ IN SCOPE (sib1 §3 Lemma 3.1 incl. its use of Alon–Yuster Lemma 2.1, and §4 Prop 4.1 + Lemma 4.2; five
EXPOSITION notes, no GAP, no FATAL).
