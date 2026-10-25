# Referee report — seat `lowmodes`
Scope: §16 (pp.132–138), §17 (pp.139–145), §18 (pp.146–165), §1.3 phase 4 (p.4), Appendix A rows Bounded / Low direct / Low cluster (p.168–169).
Read from the rendered PDF pages (all of 132–165, 166–169, plus 11–14, 106–124, 128–131 for the statements I depend on); pdftotext used only to grep and to get verbatim quotes.
Method: a hostile line-by-line re-derivation of every inequality I list as "verified" below. No Lean was run. Downloaded references are in `refs/lm_*`.

---------------------------------------------------------------------

## 0. Bottom line

I found **no mathematical gap** in §§16–18 as I read them. I found **one exposition gap** in the proof of Lemma 18.1. It is the step the Lean seat pointed me to, and I reached the same conclusion independently: the step is true but not justified as written. I also found a handful of UNCLEAR/COSMETIC points. The bounded regime closes with **C_n → ∞ at no rate**. I traced every occurrence of C_n in §§16–18 (list in §4). The only quantitative facts about C_n used are C_n → ∞, C_n ≥ 1 (i.e. N ≥ 2^n) and C_n ≤ n (i.e. N ≤ n2^n). The last two are both supplied by Lemma 2.1.

Parts that rest on internals of §14 and §15.2 I could not check line by line (listed in §5). Those are other seats' territory.

---------------------------------------------------------------------

## 1. Objections

### Objection 1 — Lemma 18.1, "Broad prefixes and deletion kernels" (p.148–149). Severity: **GAP — EXPOSITION** (the statement is true, but the justification as written omits a premise). Flagged by the Lean seat; I verified it independently.

Lemma 18.1 as stated (p.148), verbatim:
> "Fix an entering history satisfying the prerequisite gate, and use the product reference transition at b. … If the first two requirements hold, every tested prefix is broad, the specified deletion comparisons hold, and the full conditional label kernel satisfies (18.3)."

Proof step (p.149), verbatim:
> "Suppose Requirements 1 and 2 hold. For a target sketch, its empirical hit fraction H(y) = m^{-1} Σ_a I_{X_a}(y), with y ∼ U, has mean .5 + O(b_*). In its second moment, nonconflicting pairs contribute .25 + O(b_*) by (18.2), and conflicting pairs have total fraction at most 2e^4_{w,j}. Hence Var_U H = O(b_* + e^4_{w,j}), U{H < .5 − e_{w,j}} ≤ O((b_* + e^4_{w,j})/e^2_{w,j}) = O(e^2_{w,j})."

Requirement 2 (p.148), verbatim:
> "For each even role v in the current batch require ∫ I_x dU = .5 ± 10b_*, ∫ I_x I_z dU = .25 ± 10b_* (18.2) for all x ∈ D_v^0 and all nonconflicting pairs there."

**What is wrong.** Both the "mean .5 + O(b_*)" and the "nonconflicting pairs contribute .25 + O(b_*) by (18.2)" apply (18.2) to the sketch entries X_a. But (18.2) only controls labels in D_v^0 = supp τ_v^r. Nothing in "Requirements 1 and 2 hold" says the sketch entries lie in D_v^0. As a statement about arbitrary side data (mask plus sketches), the implication "R1 ∧ R2 ⇒ every tested prefix is broad" is false. The Lean seat's finite model (`HypercubeRamsey/S18/Nodes_sol_s18_1b.lean`, namespace `Obstruction`, theorem `local_obstruction`) shows this. In that model, distinct sketch labels outside the initial support conflict only on the diagonal, so R1 holds with conflict fraction 1/m ≤ 2e^4. The supported labels have the exact R2 moments 1/2 and 1/4. Yet the sketch hit fraction is identically 0 under the mask, so the first test retains zero mass. I checked that model against the paper's definitions and agree it is a faithful counterexample to the implication as worded.

**Why the conclusion is still true.** The missing premise is: every sketch entry X_a at a tested site w lies in D_w^0. This premise holds for every side datum of positive reference probability once the entering history satisfies the gate G_b:
(i) The sketch at w is iid from τ_w^j. τ_w^j is τ_w^r conditioned on previously imposed late hits, so supp τ_w^j ⊆ supp τ_w^r = D_w^0, unless a fallback point mass is used.
(ii) The fallback ("an invalid initial list or a zero normalizer is replaced by the point mass at that label", p.147) is excluded on G_b. G_b requires initial validity within radius 6r and the true-hit conclusions at earlier late roles, so every imposed hit keeps mass ≥ .5 − 3e > 0. Independently, a fallback sketch is constant, so its ordered conflict fraction is 1 > 2e^4 and R1 itself fails.
(iii) The actual late sampler has a joint upper comparison with the reference kernel (clock lemma, Prop 18.4), so it never outputs reference-null side data.

The paper states the needed restriction only after the proof, as a parenthetical:
> "(our stage assignments with joint upper comparison will indeed use only values in reference support given history)"

In the analogous place in Lemma 18.2 it does state the support condition explicitly:
> "Thus the initial masked-list requirement and the supported current lists on the original gate imply these retained conditions" (p.151).

**Fix.** In Lemma 18.1's conditional assertion, replace "If the first two requirements hold" with "If the first two requirements hold and the side data lie in the support of the product reference transition (equivalently, every sketch entry at w lies in D_w^0)". Add one sentence: on G_b the sketch law τ_w^j is not a fallback, so its support is contained in D_w^0. All downstream uses (Prop 18.4, Prop 18.5, Fig. 2) integrate against the reference kernel or a sampler dominated by it, so they are unaffected. **Not a mathematical gap.**

### Objection 2 — Prop 18.4 uses Lemma 3.10 with its scale replaced by n_clock (p.158). Severity: **COSMETIC / UNCLEAR (exposition)**.
Lemma 3.10 (p.21) is stated in the cube dimension n:
> "Let there be g labels, with log g = O(n) … Suppose Σ_a p_a(y) ≤ θ_0, p_a(y) ≤ n^{−A_*} … at most n^{−P_*} … at most n^B rows".

Prop 18.4 applies it as
> "apply the clock lemma with parameter n_clock = ⌊e^{n^{δ'}}⌋ … log M_late = O(n) ≪ n_clock, 2e^{g_0 n}/M_late ≪ n_clock^{−A_*}, n^{O(r)} ≪ n_clock^5, e^{−n^δ/(2r)} ≪ n_clock^{−P_*}".

The proof of Lemma 3.10 uses n only as a scale parameter (T_0 = K_0 log n, L = ⌈n^{.1K_0}⌉, ε = n^{B−P_*/2}), so the reparametrization is legitimate. I checked all four displayed comparisons: g_0 = α/100 ≪ log 2; δ' ≪ δ; r = O(log n). The statement should say that n there is an arbitrary large parameter.

### Objection 3 — Prop 16.3, column bound by "the capacity subset certificates of Section 15.2" (p.137). Severity: **UNCLEAR (exposition); COULD NOT CHECK in full.**
Verbatim:
> "Enforce the column bound by the capacity subset certificates of Section 15.2, using the present nominal loads and the target .2. … The same factorial calculation, inflating each certificate probability by 2 per participating group, bounds the sum touching any specified group by d_i exp(−Ω(d_i^{.4})) … Star charges ε_i^{1/16} together with these certificate charges have total at most d_i^{−10} per group."

In §15.2 (p.129) the certificate errors are made "smaller than every inverse polynomial in n" using q > (log n)^{c_q}. In low cluster mode only smallness in the fixed scale d_i is available. The low-mode version (target .2 instead of θ_0, the bucket constants K', c', the bound z ≤ 2m_j/λ_j) is not written out.

What I could check:
- d·exp(−Ω(d^{.4})) + O(h^2)ε^{1/16} ≤ d^{−10} holds for d ≥ e^{Q_0/2} with Q_0 large.
- ε_i = e^{−.001 a k_i h_i}, k_i = ⌈h_i^{3ω}⌉, h_i ≥ q^{M_lo}, d_i = ⌊e^{q/2}⌋, so ε_i ≤ exp(−c q^{M_lo(1+3ω)}), which is superpolynomially small in d_i.
- h_i = o(d_i^{.01}).

The re-run of the bucket arithmetic at target .2 is asserted, not shown. I believe it goes through (the structure is identical), but I did not verify the constants.

### Objection 4 — Lemma 18.6, "Geometric averaging" (p.164). Severity: **COSMETIC**.
> "For a uniformly chosen distinct p-set of positions, p ≤ t_0, … Its average is bounded by a convergent geometric sum with ratio e^{−(log 2)n/2 + o(n)}."

The later sum "Equation (18.5), geometric averaging and C(L,p) ≤ L^p/p! bound the expected number…" silently relies on one fact: the structure sum 4^{p−1}p^{p−1}·2M(K/M)^p is a bound uniform in the p-set, using H_v = M^{−2} on nonisolates. Only then is Σ_S[corr(S)·structure-sum(S)] ≤ C(L,p)·avg corr·(uniform bound). This is true (both H bounds hold for every p-set), but the order of summation is left implicit.

### Objection 5 — §16 opening: "M_i = Nn^{−o(1)} … ℓ_i = o(log n)" "uniformly in the present cases" (p.132). Severity: **COSMETIC**.
Low direct only gives ℓ_i ≤ s_i/(1000u) = O(log n) from the common budget. ℓ_i = o(log n) needs the other inequality of Prop 13.3's proof: ℓ_i ≤ log_2(S/M_i)+1 together with log(N/M_i) ≤ g^{a_B}+O(1) = o(log n). True; not cited at the point of use.

### Objection 6 — Lemma 16.1 proof (p.133). Severity: **COSMETIC**.
> "Each class has size 2^{n−1}/H_*: the joint map recording syndrome and parity has full rank, since the IDs include zero and span H."

"The IDs span H" needs at least one ID outside the hyperplane H_0. That follows from n > H_*/2 = |H_0|, i.e. from H_* < 2n, but this is not said. Verified (see §3).

No further objections. In particular I found no FATAL or mathematical gap in §§16–18.

---------------------------------------------------------------------

## 2. Specific checks requested in the brief

### (a) Lemma 16.1 — explicit construction and verification (line by line)
- **Setup.** H = F_2^m with H_* = 2^m ∈ [n, 2n).
- **IDs.** Coordinates k get distinct IDs a_k ∈ H, with H_0 ⊆ {a_k} for a fixed linear hyperplane H_0 (|H_0| = H_*/2 ≤ n). The remaining n − H_*/2 IDs lie outside H_0; this is possible because n − H_*/2 ≤ H_*/2 iff n ≤ H_*.
- **Syndrome map.** s(z) = Σ_k a_k z_k. This is the syndrome of a shortened Hamming-type parity-check matrix whose columns are the a_k. It is not a distance-3 code, since one column is 0. The paper does not cite [21] here, and needs no code property.
- **Class sizes.** z ↦ (s(z), parity(z)) is surjective onto H × F_2:
  - a_k = 0 for some k (0 ∈ H_0), giving (0,1);
  - each (a_k, 1) is in the image, so (a_k, 0) is in the image;
  - the a_k span H, because more than H_*/2 distinct vectors cannot lie in a proper subspace.
  So each odd syndrome class has exactly 2^{n−1}/H_* roles. There are H_* odd classes in total. The late classes are the r with t ∈ L, a subspace with A_0 log n ≤ r = |L| < 2A_0 log n; a power of two exists in that range.
- **At most one neighbour per class (in fact per any class).** v+e_k is in class t iff a_k = s(v)+t. The IDs are distinct, so this happens for at most one k. It is the brief's criterion L(e_i) = L(e_j) iff i = j.
- **Between ⌊j/2⌋ and j neighbours in the last j classes.**
  - If s(v) ∈ H_0, then for t ∈ L∩H_0 the required ID s(v)+t lies in H_0 ⊆ IDs.
  - If s(v) ∉ H_0, then for t ∈ L∖H_0 the required ID s(v)+t lies in H_0.
  - |L∩H_0| = |L∖H_0| = r/2 because L ⊄ H_0.
  - The ordering in which every suffix splits evenly then gives ≥ ⌊j/2⌋. Hence r/2 ≤ p(v) ≤ r.
- **At most one late internal neighbour.** The eligible late flips have a_k ∈ s(v)+L (one coset). The internal axes are nested across patches, so their union has size max_i h_i ≤ (log n)^{.1}, and they get IDs in H_0 in distinct cosets of H_0∩L. There are H_*/r ≍ n/log n such cosets. Distinct cosets of H_0∩L inside H_0 are distinct cosets of L. So at most one internal ID lies in s(v)+L.
- **No edges inside late classes.** Late roles are odd, and Q_n is bipartite, so there are no cube edges among them (trivial). The paper never uses this.
- **Sizes.** L_late = 2^{n−1}/H_* ≤ 2^{n−1}/n. M_late ≍ N/(3r) (from the ⌊N/3⌋ Y-reserve of §13.1). L_late/M_late ≍ (log n)/(n C_n) → 0.

### (b) §16.1–16.3 (line by line except where noted)
- **Slot fitting.** "The patch counts and C_n → ∞ ensure that all cells' slots fit disjointly among these bins" (p.133–134). Total slots ≲ (2·2^{n−ℓ_i}/n^{A_c} + e^{O(log^4 n)})·⌈K_cell n^{A_c}/d_i⌉. B_i = M_i/d_i. With 2^{−ℓ_i} < 2M_i/S, this needs S ≥ (4+o(1))K_cell 2^n, i.e. C_n ≥ O(K_cell)/c'. A fixed constant: only C_n → ∞ is used. ✓
- **Permutation vs iid slots.** For k = exp(polylog) slots, B^{−k}(1−k/B)^{−k} = B^{−k}(1+o(1)) since B_i ≥ 2^{n−o(n)}. ✓
- **(16.1) permission trim.** For fixed σ_v of width ≤ h_i log 2, take a one-sign exceptional y-set of uniform Y_{i(b)}-mass ≥ e^{−3cn}. It has width ≤ log(N/M_{i(b)}) + 3cn < αn for c < α/3, so (12.1) contradicts deviation > 2b_* > b_*. Averaged bound 2e^{−3cn}; Markov plus group/bin multiplicities give an e^{−Ω(n)} removed fraction. ✓
- **Lemma 16.2, normalizers.** Expectation 1. Bounded differences with per-slot change exp(O(kT))/L^slot = n^{−A_c+o(1)}: deviation n^{−4} has exponent ≥ n^{−8}·L^slot/exp(O(kT)) = n^{192−o(1)}. The union over exp(n^{1+o(1)}) histories survives. ✓
- **Lemma 16.2, empirical failure.** Integral ≤ 2√ε + n^{−A_c+o(1)}, bounded-differences deviation ε^{1/4}/4 ≥ n^{−o(1)}, exponent n^{A_c−o(1)}. ✓ (The 2√ε input from (14.3) and the pretrim was only skimmed.)
- **Load gate.** Slices contribute ≤ n^{−A_c+o(1)} each; there are ≤ n^{A_c} slices; mean O(1/K_cell) ≤ θ_*/2. Hoeffding plus a union over n^{A_c+o(1)} pool labels gives δ(P) ≤ e^{−n^{c0}}. E[F|P, gate] ≤ E[F|P]/(1−δ). ✓
- **Prop 16.3.** C is compact and convex: a support condition plus finitely many linear inequalities. The separation argument checks out:
  - centered-price gain ≥ ½d^{−.1}Σ|c−c̄|q̃;
  - singleton error ≤ d^{−2}Σ|c−c̄|q̂ (center using Σ_D(μ_g−q̂_g) = 0);
  - star failure 2ε^{1/8} by Markov from ε^{1/4};
  - Lemma 3.5's final assertion gives the exp(d^{−.05}l) joint factor (charges ≤ d^{−10} per group).
  Certificate constants: see Objection 3.
- **Prop 16.4.** Hypotheses of Lemma 3.9 checked:
  - cluster: atoms ≤ 2e^{1.5kT}/d ≤ d^{−.95} by (14.1) since kT ≪ log d; column ≤ .2(1+O(d^{−.02})) ≤ .4; ≤ h_i ≤ d^{.025} queries per bin;
  - direct: d = L^slot = n^{200+o(1)}, atoms O(1/L), column ≤ 1/(2K_cell) ≤ .4, l ≤ L^{.025} = n^{5+o(1)} ≥ n^3.
  ✓ (Role-label pin O(dε^{1/8}): skimmed.)
- **Lemma 16.6.** Chain of factors (1+e^{−n^{c0}})·(B/L)(1+O(n^{−4}))·(1+e^{−Ω(n)}), with E_W[q^{in,W}U^W] = π_i^out = π_i at the fixed point. Averaging over iid pools: Pr(bin ∈ P) ≤ L/B. ✓
- **Lemma 16.7.** Containment of m distinct target bins in an iid pool ≤ (L/B)^m cancels the m factors B/L. The remaining costs h^{O(1)}√ε and h d^{−.01} are bounded. ✓

### (c) §17 (line by line)
- **Lemma 17.1, mass.**
  - s + c' + d ≤ n − h_i − p(v) + 1, because only one late neighbour can be internal. ✓
  - Pins: σ_v-mass ≥ .9·2^{−s} times (2−o(1))^s from denominators .5+o(1) (bulk O(log n/n), crossings ≤ 3b_* by Lemma 13.4) gives ≥ .9−o(1). ✓
  - Crossings: (12.1) at small first width / linear second width; per-step factor 1 ± O(b_*); c'b_* = o(1) since c' ≤ ℓ_i = o(log n). Mass > .8. ✓
  - τ ≤ K2^s4^{c'}σ_v. ✓
- **Lemma 17.1, Γ.** Recomputed in each mode.
  - Cluster: Δ_i ≤ e^{s}, N‖σ‖ ≤ 2^{h}e^{−500s}, D^{−d} ≤ 2^d e^{s/(50u)}, 2^{c'} ≤ e^{s}, 2^{h+s+d} ≤ 2^{n−c'−p(v)+1}, N ≥ 2^n. Result Γ ≤ 2Ke^{−497s}2^{−p(v)}.
  - Direct: D^{−d} ≤ 2^d e^{−500s(1−o(1))}, N/M_i ≤ e^{s/(1000u)}, same result.
  - Bounded: all factors fixed (Δ_i ≤ K, N/M_i = O(1), D^{−d} ≤ 2^d e^{2K}); Γ ≤ K2^{−p(v)}.
  - Then p(v) ≥ A_0 log n/2 with A_0 ln2/2 > 3R gives Γ ≤ n^{−3R}. ✓
- **Lemma 17.1, moment step.** Pr(Z < 3/4) ≤ 4^u(n^{−3R}+C_uΓ) ≤ n^{−2R}/2. This uses Lemmas 12.2/12.4/12.5. Their hypotheses (small width, |D−.5| ≤ O(b_*), no ⌈e^Q⌉-clique on the cleaned support, the Γ condition) were all checked against pp.107–110 and Lemma 13.4. ✓
- **Lemma 17.1, support size.** E|L_v(J)| ≤ N·2^{−(d−|J|)}·e^{O(log n)} ≤ exp(O((log n)^4)), using N ≤ n2^n. C(n,(log n)^4) ≤ exp((log n)^5). Markov at exp((log n)^8). ✓
- **Lemma 17.2.** Per occurrence: bin-label weight B·d·(11/M) = 11. Overlap-rank fraction (2nT_s)^{3j}L^{−j}. Pinned trials ≤ 2j/s_0. The bracket [(2nT_s)^3·11^2·n^{2R/s_0}/min L] = n^{3.1−200+o(1)} → 0. Pr(p_S > n^{−P}) ≤ n^{−(R−P)T_s} ≤ n^{−RT_s/2} since R = P^2, P ≥ 2. A_v: Markov plus a union over n^{O(s_0(A_c+1))} choices. ✓
- **Lemma 17.3.**
  - GV-type map with χ_i ≤ e^{s_i}, using log Vol(h, 1000ρh) < (a/10^9)h.
  - Equal colour classes among even roles (free outer bit, surjective map).
  - Palette concentration: exponent ≥ cC_ne^{199s}2^{p(v)} ≥ n^{A_0 ln2/2} ≫ n^{2+o(1)} histories.
  - (17.2): typical pairs give a ratio product 1+o(1). Exceptional nonconflicting pairs: R^d ≤ e^{100n|K|}O(1) is controlled by the relaxed weighted row tail e^{−n^{.19}}; σ_v vs uniform costs e^{O(log n)}. ✓
- **What survives the initial assignment for each even v** (answer to (c)), all on S_fin under terminal conditioning:
  - σ_v valid: a probability on one cleaned corner support, on common neighbours of all internal odd labels, including the dummy at the ≤1 late internal neighbour, with cap N max σ_v ≤ 2^{h_i}e^{−500s_i};
  - M_v^0 ≥ 1/2 with all external early hits (bulk + crossing) imposed and no external late hit imposed;
  - masked-list bound max_{|J| ≤ (log n)^4}|L_v(J)| ≤ exp((log n)^8);
  - palette mass ≥ 1/(4χ_i);
  - deterministic cap max τ_v^r ≤ 4KC_n^{−1}e^{−199s_i}2^{−p(v)};
  - plus pool typicality, (17.1) and p_F ≤ e^{−n^δ} for every late bad event F.
- **Prop 17.4.** The MT witness argument was checked:
  - A component has a true site at every round start (outside executions adjacent to the component would belong to it).
  - The least-numbered true site executes, so M ≥ T_s.
  - Listed tests read disjoint (cell, index) entries, giving joint ≤ n^{−P(M+J)}.
  - Backward closure: terminal entries are untouched by listed tests, which yields the multiplicative comparison.
  ✓ The citation of [28] is background only; the paper proves its own fixed-priority version.

### (d) §18 — injectivity, adjacency, distinctness, and the final Hall estimate
- **Injectivity of all odd roles.** All of the following combine to global injectivity on Y:
  - early labels: injective within a cell (Prop 16.4), cells on disjoint bins (permutation of bins), patches disjoint (Prop 13.3), all inside Y_i's outside the ⌊N/3⌋ reserve;
  - late labels: each class drawn from its own late pool (pools disjoint, inside the reserve), injective within the class (clock lemma: "distinct labels");
  - dummy labels are discarded.
  ✓
- **Adjacency of each even role's candidates to ALL its odd neighbours.**
  - supp q_v ⊆ supp σ_v ∩ {x : I_x(y_b) = 1 ∀ b ∈ B_v^e} ∩ {hits every replaced late label}.
  - Internal neighbours are covered by σ_v. External early neighbours (bulk and crossing, i.e. across patches) are covered by U_v^0. All late neighbours, including the ≤1 internal late one after replacement, are covered by the τ conditioning (Req. 3 guarantees positive mass).
  - The extra hit on the internal dummy is harmless.
  ✓
- **Distinct candidates, never colliding with odd labels.** Nonconflict excludes the diagonal (K(x,x) = 1 > ξ), so each pair has distinct labels. Even labels lie in X and odd labels in Y, which are disjoint. Palettes are disjoint within a patch, and patches are disjoint. ✓
- **Lemma 18.6, Hall for 2-element sets.** Hall fails iff some connected component of the label multigraph (one edge per even row) has more edges than vertices. The paper's enumeration:
  - Connected p-row sets: row-tree diagrams ≤ 4^{p−1}p^{p−1}. I checked that the p−1 identifications give exactly p+1 classes: the identification graph on 2p slots is a forest, since a cycle would need a closed walk using each row-tree edge once. The rows then form a tree on those classes. Leaf-peeling gives ≤ 2M(K/M)^p.
  - Violators: a connected violator with p ≥ 3 has ≤ p−1 labels, so ≥ 2 further merges, O(p^4) choices. That leaves p edges on p−1 vertices, no loops (distinct endpoints); spanning tree p−2 edges plus 2 edges at max-weight M^{−2}e^{.01n}. Total ≤ K^pM^{−p−1}e^{.02n}.
  - Large sets: every component with ≥ t_0 edges contains a connected t_0-row set. Expected number ≤ e^{O(r)}M(4eK^2L/M)^{t_0} with L ≤ KM/C_n, so ≤ e^{O(r)}M(K/C_n)^{t_0}, whose log is n log 2 + o(n) + ηn log(K/C_n) → −∞ linearly. This only uses C_n → ∞.
  - Small sets: e^{O(r)}p^4M^{−1}e^{.02n}(K/C_n)^p, with M^{−1} ≤ 2^{−n+O(log n)}.
  - Summing over e^{o(n)} patches and palettes: o(1).
  Everything checks.
- **Geometric averaging.** Pr(rank ≥ j) ≤ p^{2j}(n^{A_c+O(1)}/L)^j with L = 2^{n−O(log n)}. The correction e^{(.02+C'η)nj} has ratio ≤ e^{−(log2−.02−C'η)n+o(n)} ≤ e^{−(log 2)n/2}. ✓

### (e) Bounded regime (one patch, M_i ≍ N, ℓ_i = h_i = s_i = 0, |D−½| ≤ K/n, Δ_i ≤ K, χ_i = 1)
Where the slack comes from:
1. Deferring p(v) ≥ A_0 log n/2 late hits makes Γ ≤ K2^{−p(v)} ≤ n^{−3R} (Lemma 17.1). Only N ≥ 2^n is used. Without the deferral Γ ≍ K/C_n, which is only o(1).
2. This polynomial slack carries Lemma 17.2/Prop 17.4 (n^{−P} truth tests, LLL charges vs D_n = n^{O(T_s)}) and the palette step (trivial here, χ_i = 1).
3. The late process restores the 2^{−p(v)} one class at a time:
   - error e_{w,j} = C_n^{−β}2^{−βj}, with Σ_j e = O(C_n^{−β}) = o(1) (C_n → ∞) and min e ≥ n^{−.02} (C_n ≤ n);
   - sketch concentration needs 8K^2C_n^{−1}2^{−p_w(j)} ≤ C_n^{−4β}2^{−4βj}/2, true for C_n ≥ const (β ≤ 1/16);
   - retention needs (1−O(e^2))^n ≥ e^{−g_0 n}, true for C_n ≥ const.
4. The final lists have cap 8KC_n^{−1}, so Z_v ≥ 1/2 needs C_n ≥ 16K^2, and Hall needs K/C_n < 1 and log(K/C_n) → −∞.

I hunted for any e^{−cn}·2^n, n^{−k}·(#roles) or (list size)^{−1} comparison that needs C_n ≥ n^c: **there is none**. Every C_n-dependent inequality in §§16–18 is of the form "C_n ≥ fixed constant" or "C_n^{−β} → 0".

### (f) "same/similarly" phrases in scope (all checked)
- p.134 "The same comparison holds after fixing any one global slot" — ✓ trivial.
- p.136 "In direct modes typicality itself gives the same load slack" — ✓ (load ≤ 1/(2K_cell)).
- p.137 "The same factorial calculation, inflating each certificate probability by 2" — Objection 3.
- p.138 "The same pinned argument as for group bins" — ✓ structure.
- p.139 "The same proof can retain the true internal-validity indicator" — ✓.
- p.140 "the cleaned crossing denominators have the same estimate" — ✓ Lemma 13.4 (3b_*).
- p.140 "the same inequality holds with a fixed K and s_i = 0" (bounded) — ✓ recomputed.
- p.141 "the same argument uses entirely unforced selected data" — ✓.
- p.144 "the same estimate" for pair integral — ✓.
- p.149 "similarly for forward influences" — ✓ (radius O(r)).
- p.154 "apply the same estimate to the normalized restriction for z" — ✓ (bounded width increase).
- p.157 "The same argument compares tests supported on a polynomial union of these local regions" — ✓ (sum of touching charges n^{O(1)}D_n n^{−PT_s/3} = o(1)).

### (h) Final contradiction
On a full run with no Hall obstruction (probability ≥ 1 − o(1) − o(1) > 0 for large n along the stabilized subsequence) the construction gives:
- an injective odd assignment into Y and an injective even assignment into X;
- every cube edge an edge of the single colour G chosen in §13 (every even label is in N_G of every odd neighbour's final label).

This is a monochromatic Q_n across the two sides, contradicting the defining property in Lemma 2.1 ("red-blue colorings between disjoint sets X, Y, each of size N, with no monochromatic Q_n across the two sides"). The hypotheses of Lemma 2.1 used in §§16–18 are C_n → ∞, N ≤ n2^n (support size in Lemma 17.1; polynomial factor in Lemma 18.2; label union in Prop 18.4; e_{w,j} ≥ n^{−.02}) and N ≥ 2^n.

---------------------------------------------------------------------

## 3. Citation table (scope)

| Cited | Paper's claim | Source (version read) and quote | Verdict |
|---|---|---|---|
| [28] Moser–Tardos | "The parallel-round theorem of Moser and Tardos uses a maximal independent set in each round" (p.144) | arXiv:0903.0544v2: "in every step we select a maximal independent set S in the subgraph of the dependency graph G spanned by the violated events and resample all the variables these events depend on in parallel" | MATCH (background; Prop 17.4 is proved directly) |
| [19, Thm 2.2] Haeupler–Saha–Srinivasan | "established multiplicative comparisons for fixed events determined by the current assignment during a resampling execution" (p.144) | arXiv:1001.1231v4, Thm 2.2: "Let B be any event that is determined by P. Then, the probability that B was true at least once during the execution of the MT algorithm … is at most Pr{B}·(∏_{C∈Γ(B)}(1−x_C))^{−1}" | MATCH |
| [22] Harris–Srinivasan | "developed this distributional analysis further" (p.144) | arXiv:1507.02674v1 (preprint of the TALG paper): "We examine the distributions on these variables which arise during intermediate stages of MT … building further on the 'MT-distribution' concept of Haeupler et al." | MATCH |
| [27, Thm 1] Lu–Székely | "the negative-dependency precedent for partial mappings in a uniform injection" (p.157) | EJC 14 (2007) R63: "Let A_1,…,A_n be canonical events in I(U,V). Let G be the graph … E(G) = {ij \| A_i and A_j conflict}. Then G is a negative dependency graph" | MATCH (precedent only; §18.3 gives its own swap coupling incl. tapes and image collisions; I checked that the coupling preserves nonneighbour leaves) |
| [27, Lemma 3] (via Lemma 3.5, used in Props 16.3, 16.4, 18.3) | "asymmetric formulation used here" | "If there exist x_i ∈ [0,1) with Pr(A_i) ≤ x_i ∏_{ij∈E(G)}(1−x_j) for all i, then Pr(∧Ā_i) ≥ ∏(1−x_i) > 0" | MATCH in substance; the paper's Lemma 3.5 is the conditional form with general p_i and is proved in-text |
| [20] Hall | Hall's theorem for distinct representatives (Lemma 18.6) | COULD NOT FETCH (Wiley/Cloudflare challenge). Used only in its textbook form (SDR iff every k sets have union ≥ k). | COULD NOT FETCH (standard) |
| [21] Hamming | — | Not cited in §§16–18; Lemma 16.1's syndrome map is self-contained (verified above) | n/a |
| [1],[15],[23] martingales | "bounded differences" used without citation (Lemma 16.2, Lemma 18.1) | Standard McDiarmid consequence of Azuma–Hoeffding; Lemma 18.2's martingale step is a self-contained second-moment computation, no Freedman bound used | not separately compared |
| [9],[10],[16],[8] | Not invoked in §§16–18 (enter only through Lemmas 3.5, 3.9, §3.1) | — | out of scope |

---------------------------------------------------------------------

## 4. Parameter-dependency table (scope)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| A_c = 200 | §12 (p.107) | — | cell size n^{A_c}, L^slot, all n^{−A_c+o(1)} repeat costs |
| P, R = P^2 | §12 | A_c, clock constants at B=5 | (17.1) n^{−P}; n^{−2R}, n^{−RT_s/2}; LLL in 18.3 (P ≫ C(A_c+4)) |
| u, L=⌈500R⌉, ξ, θ, C_* | §12 (p.109) | R; then u; then ξ | Lemma 17.1 moment; nonconflict cutoff ξ; Δ_i = e^{C_*Q_i} |
| α, x_*, b_* = n^{−.96} | Cor 12.1 | earlier sections | (16.1), Lemma 17.1–17.2, 18.2; g_0 = α/100 |
| M_1, C_b, M_lo, c_q, M_hi, ω, a=θ/100, ρ | §13.2 items 1–2 | C_*, a_B, a_C | mode split; h_i, d_i, s_i; palette map |
| K_B, A_0 ≫ 10^6 R | §13.2 item 3 | R | r ≍ A_0 log n late classes; Γ ≤ n^{−3R}; palette concentration |
| Q_0 (scale threshold) | §13.2 item 3, "increased as needed" incl. Prop 18.5 (δ_cal ≤ .005) | all small-surplus constants, ξ, ε=10^{−5} | low-cluster d_i, h_i, ε_i inequalities; bounded-case K and Δ_i |
| K (bounded-case degree/conflict constant) | Lemma 13.4 | M_1Q_0, a | Lemma 17.1 Γ, (18.1), Z_v; absorbed by "large n" and "C_n large" (no A_0 ≥ f(K) requirement, so no cycle) |
| K_cell | §16 | θ_* (≪ θ_0 clock) | slot count; load gate; column ≤ .4 |
| c (16.1), c_0 | §16 | α | permission trim, pool typicality |
| s_0 = ⌈20R⌉ | Lemma 17.1 | R | pins; 2R/s_0 ≤ .1 |
| T_s = ⌈log^2 n⌉ | §17 | n | rounds; n^{−PT_s/2} |
| β (late error) | §18.1, "after the low-mode constants" | A_0, K_B, a | e_{w,j}; needs β(1+10^{−3}K_B+2A_0 ln2) ≤ .02 and β ≤ 1/16 |
| m = ⌈n^{.25}⌉, g_0 = α/100 | §18.1 | α | sketches, broad threshold e^{−g_0 n} |
| c, c_1, c_2, c_3; δ < c_1; δ' ≪ min(δ,1) | Lemmas 18.1–18.2, §18.3, Prop 18.4 | x_*, α | alarms a_q, n_clock = ⌊e^{n^{δ'}}⌋, B=5, A_*, P_*, θ_0 |
| C', η (.02+C'η < log2/2), t_0 = ⌊ηn⌋ | Prop 18.5, Lemma 18.6 | absolute; ξ, δ_cal give the .01n margin | Hall estimate |

No cycle found. The only "increase X later" instance is Q_0. I checked that every later requirement on Q_0 involves only quantities fixed before Q_0 (ξ, ε, a, M_lo, ω, C_b). β is chosen after Q_0, and nothing about Q_0 involves β.

**All C_n occurrences in §§16–18:**
- p.133 slot fitting (C_n ≥ const);
- p.140 N ≥ 2^n;
- p.141 N ≤ n2^n;
- p.143 cap K C_n^{−1}…;
- p.147 e_{w,j} = C_n^{−β}… (C_n ≤ n; C_n^{−β} → 0);
- p.147 (18.1);
- p.149 sketch concentration (C_n ≥ const);
- p.155 M_i ≤ n2^n;
- p.159 Z_v (C_n ≥ const), L ≤ KM/C_n;
- p.165 (K/C_n)^{t_0}, (K/C_n)^p.

None requires a rate.

---------------------------------------------------------------------

## 5. Verified line by line vs only skimmed

**Verified line by line (inequalities re-derived):**
- Lemma 16.1 (entire).
- §16 slot fitting, permutation/iid comparison, (16.1).
- Lemma 16.2 (normalizer and load-gate concentration).
- Prop 16.3 separation logic and star-charge arithmetic.
- Prop 16.4 Lemma 3.9 hypotheses.
- Lemmas 16.6, 16.7.
- Lemma 17.1 (all three parts, all three modes).
- Lemma 17.2.
- Lemma 17.3 (map, colouring concentration, (17.2), the uniform integral).
- Prop 17.4 (witness and terminal-entry arguments).
- §18.1: e_{w,j} bounds, (18.1), Lemma 18.1 (all three paragraphs; Objection 1).
- §18.2 geometry: parity vector P, (18.4), V_0 analysis, one-block locality and affected-site counts.
- §18.2 survival-under-cylinder arithmetic, likelihood-ratio second moment, final Cauchy–Schwarz count.
- Prop 18.3 replay argument and leaf-coupling (lopsided) step.
- Prop 18.4 mask balance (minimax), alarm thresholds, clock-lemma comparisons, column-load moment and union.
- Prop 18.5 bookkeeping (late factors, shared-incidence removal O(t'j), isolated-row H_v bounds, nonisolate reduction, repeated-bin cost, the δ_cal ≤ .005 budget).
- Lemma 18.6 (entire).
- Conclusion of Theorem 1.1.

**Only skimmed / taken on trust (COULD NOT CHECK fully):**
- The low-mode capacity-certificate constants imported from §15.2 into Prop 16.3 (Objection 3).
- The 2√ε_i input in Lemma 16.2 from (14.3) and the pretrim (§14 internals).
- Prop 16.4's role-label pin bound O(d_iε_i^{1/8}).
- Lemma 18.2's block-protocol bookkeeping at the level of exact exponents (response log-range n^{.4}, n polylog updates). I checked the orders of magnitude, not every constant.
- The LLL charge arithmetic over permutation leaves in Prop 18.3 (D_n = n^{C(A_c+4)T_s+O(r)} vs n^{−PT_s/3}): checked as stated, with C not traced.
- Lemma 3.10's proof itself (outside scope).

---------------------------------------------------------------------

## 6. Verdict for scope

- **HOLDS AS READ** for §16, §17, §18, §1.3 phase 4 and Appendix A rows Bounded / Low direct / Low cluster. No mathematical gap; the bounded regime closes using only C_n → ∞, N ≥ 2^n and N ≤ n2^n.
- **GAP (exposition) at Lemma 18.1**, "Broad prefixes and deletion kernels" (p.149). The step applies (18.2) to sketch entries without the premise that they lie in D_w^0. The premise holds automatically for reference-supported side data on the gate G_b (and fallback sketches already violate R1), so the conclusion is true.
- **COULD NOT CHECK:** the §15.2-derived certificate constants in low mode (Prop 16.3), the §14 inputs, and the exact exponents in Lemma 18.2's protocol counts.
