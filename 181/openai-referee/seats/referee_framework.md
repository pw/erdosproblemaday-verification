# Referee report, YOURTAG = framework
## Scope: §2 (Lemma 2.1), §3 (Def 3.1 – Lemma 3.10, pp. 10–26), plus §1.3–1.4, Fig. 1 (pp. 3–7) and App. A (pp. 166–169)

Source read: /tmp/oaimath/171/paper.pdf. Pages 1–33, 79–80, 111–114, 123 and 166–172 were read as rendered images. paper_plain.txt was used for grep and for invocation contexts.

**Bottom line.** I found no mathematical gap in §2–§3, including Lemma 3.9 checked against the false decomposition recorded in the Lean design note (item 12). Every lemma in scope is correct as stated, once the proofs are re-derived. In several places the exposition is compressed. Items 1–11 below are all graded COSMETIC or UNCLEAR, and none of them is FATAL or a GAP.

I also spot-checked invocations of Lemmas 3.2, 3.3 and 3.5–3.10 in §§4, 6–11 and 13–16, at least three per lemma (35+ sites in total). Every hypothesis I checked is satisfied. The one exception is a reading point: Lemma 3.8 is stated in the variable n but is applied on Q_h with h possibly bounded (item 1).

---

## 1. Objections

### 1. Lemma 3.8 is invoked with the internal dimension h in place of n, and h may stay bounded. UNCLEAR, exposition.

**Location.** Lemma 3.8, p. 15: "*R₀ = ⌈log² n⌉, Rᵢ = MRᵢ₋₁, M = ⌈n^σ⌉ … (i) Except on an event of probability at most exp(−n^{1+c}) … (ii) … at most exp(−n^c)*". The setup on p. 14 reads "*S of Q_d, where d = Θ(n) … λ = n^{J₀}*".

**The invocation.** §14.1, p. 119: "*Use the geometric height device on Q_h with step bound 6, radius ⌊ρh⌋, λ = h¹⁰ …*". p. 120: "*asymptotic slack in powers of h itself need only hold for q ≥ Q₀*". p. 123: "*positive-height bound is e^{−h^{Ω(1)}} … These are precisely the bounds of Lemma 3.8*".

**Why it matters.** Table 1 (p. 169, low cluster) says "*The scales q, hᵢ, dᵢ may stay fixed*". So the lemma is used with n := h fixed. Its "for large n" thresholds then become "h ≥ h₀". Its global bound (i), exp(−h^{1+c}), is then a fixed small number, not o(1).

**Assessment.** The proof does deliver an explicit n₀ that depends only on the fixed parameters (J₀, b₀, b, ρ, D, σ, ζ, θ, a and the Θ-constant). Every comparison in Steps 2–5 is an explicit power inequality, for example "*n^a (R′)^θ / (Rᵢ log n) ≥ n^{a−σ−(1−θ)+o(1)} / log n*". The paper also fixes all the geometric constants before Q₀: p. 113, item 3, reads "*Fix all the small-surplus geometric and probability constants before taking a large scale threshold Q₀*". On p. 123 the paper uses only per-slice failure, exp(−h_i^{1+Ω(1)}), and never the global o(1).

So this is not a gap. **Fix:** state Lemma 3.8 for a free parameter n ≥ n₀(params), instead of tying it to the cube dimension.

The same reading applies to Lemma 3.9 with d = dᵢ fixed (Prop. 16.4, p. 137). Its threshold "sufficiently large d" is absolute, and the comparison factor becomes a fixed exp(dᵢ^{−.04} l) rather than 1 + o(1). The paper states exactly that factor, as exp(dᵢ^{−.01} l). COSMETIC.

### 2. The finite-union clause of Lemma 3.2 is phrased so that one reading fails. COSMETIC, exposition.

**Location.** p. 11: "*For an available union of k families with tolerance κ, use κ/k as the removal tolerance for each member. If no member were available on a subsequence, we could combine their eliminating sets and eliminate the union within its tolerance.*"

**The issue.** The sentence is correct only if read as "no member is available along **any** subsequence".
- Under that reading, each member's elimination number τᵢ(n) is o(N) along the **whole** sequence. Summing the k removal sets then eliminates the union with o(N) labels, which contradicts tolerance κ.
- Under the weaker reading ("along the given subsequence no member is available"), non-availability gives only liminf τᵢ/N = 0 for each member separately. That is an "infinitely often" statement, and it gives no common n at which all members are cheap. The combination step would then fail.

**Clean proof.** τ_U ≤ Σᵢ τᵢ, so maxᵢ τᵢ(n) > κN/k eventually. By pigeonhole, some i attains the maximum infinitely often, and that member is available with tolerance κ/k along that subsequence.

Every invocation I found applies the clause to members that are already stabilized, so each member is either absent or available and the point is moot. These are: two colours in Lemma 4.1 (p. 27) and in (7.1) (p. 64), Cor. 7.2 (p. 69), Cor. 8.2 (p. 79), §9 (p. 81) and §11 (p. 97).

### 3. Lemma 3.3's constant K = 4/κ depends on the counterexample sequence. UNCLEAR; no circularity found.

**Location.** p. 12: "*Thus K = 4/κ suffices.*" App. A, p. 166: "*Every constant and exponent is fixed before n → ∞*".

**The issue.** The availability tolerance κ exists only along the stabilized sequence. It is halved at each later o(N) discard stage (Lemma 3.2: "*persists with half that tolerance*") and divided by k at each finite union. So K, and the downstream constants K′, depend on the sequence and on the stage. This would be fatal only if some exponent or threshold fixed before the sequence had to dominate K.

**What I checked.** p. 28 (K/N tag balance); p. 32 (K′ = 2·(3 + o(1))); p. 65 ("*If α(H_τ) ≥ K′n^{−D₀}*"); pp. 66–67 (Markov threshold against the means K′); pp. 99–100 (Lemma 11.2, "*increasing their fixed K at the outset as needed for discard slack*"); p. 126 and p. 132 ("*N(K′/C_n)^n = o(1)*").

In every case K enters only as a multiplicative constant. It is set against a negative power of n, against e^{−Ω(n)}, or against C_n → ∞, and all of these beat any fixed K. The Markov thresholds of Lemma 3.6 are chosen after K. I found no cycle.

**Fix (wording).** App. A should say "fixed before n → ∞, possibly depending on the counterexample sequence".

### 4. Lemma 3.5 is ambiguous about the neighbour product. COSMETIC.

**Location.** p. 12: "*Suppose that, whenever defined, the probability of Eᵢ conditioned on avoidance of any subset of its nonneighbors other than itself is at most pᵢ … pᵢ ≤ xᵢ ∏_{j∼i}(1 − xⱼ)*".

**The issue.** It is not said whether i ∼ i. If ∼ is reflexive, the hypothesis is strictly stronger, so the proof is unaffected either way. The proof I re-derived uses only j ∈ S ∩ Γ(i) with j ≠ i.

### 5. Lemma 3.6 asks for K^n rather than K^ℓ for sequences of length ℓ ≤ n. COSMETIC.

**Location.** p. 13: "*for any sequence of at most n indices … the joint product expectation with the success indicator is at most K^n times the product*".

**Assessment.** This is a weaker hypothesis than K^ℓ (because K ≥ 1), and the proof still yields K^n(|U|^{−1}Σ d + nfL)^n. Invocations that verify C^ℓ (pp. 67 and 78) satisfy it with K = max(C, 1). There is no error.

### 6. Lemma 3.10's discretization limit is only asserted. UNCLEAR, exposition.

**Location.** p. 26: "*Choose the time mesh sufficiently fine for this bound to persist. Continuous arrival times are distinct almost surely; matching decisions and truncated explorations therefore converge almost surely as the mesh is refined.*"

**Re-derivation.** Almost surely there are finitely many arrivals on [0, T₀] over the finitely many edges, with distinct times. For a mesh finer than the minimum gap, the binned process makes the same decisions, so every test's indicator converges almost surely. The incidence sums and the joint target probabilities are finite sums of such probabilities, and they converge by dominated convergence. Step 8 gives "*Every contribution has a fixed power of slack below n^{−.6K₀}*", so the strict slack survives a fine enough mesh. The argument is correct; it is just terse.

### 7. Lemma 3.8, Step 3: the sublinear-radius ball-intersection bound is only sketched. UNCLEAR, exposition.

**Location.** p. 17: "*For sublinear radius, the enlarged ball has radius at most n^{1−c″}; layer ratios and a subset union bound for the differing coordinates improve both exponents to Ω(s log n).*"

**What I checked.**
- **Linear case.** A point x with d(x, c₁) ≥ r′ − s/10 and d(x, c₂) ≤ r′ must flip at least 0.45s of the s differing coordinates. The paper states .44s, which is safe. The hypergeometric mean is at most (1/4 + o(1))s, so the tail is e^{−Ω(s)}. The ball-enlargement cost is e^{O(R′)}. With s ≥ KR′ the result is V·e^{−Ω(R′)}, as claimed.
- **Sublinear case.** I checked the exponents only heuristically: layer ratio about d/r′ ≈ n^ρ, and C(s, .45s)·(r′/d)^{.45s} = e^{−Ω(s log n)}, against an enlargement cost of e^{O(R′ log n)}.

I did not write out the sublinear case in full.

### 8. §9 re-runs Steps 2–4 of Lemma 3.8 "by the same induction". UNCLEAR; the invocation is outside scope, but it rests on in-scope work.

**Location.** pp. 81–82: "*We adapt Steps 2–4 of the proof of Lemma 3.8, using paths with step bound 2 in the full cube … The base bound, the overlap bound and independence on private regions now give the same scale induction as in Lemma 3.8.*"

**What changes.** Three crowd tests replace the single (r + D)-ball test, and paths cross slices.

**What I checked.** The restated constraints play exactly the roles of b₀ and b in Lemma 3.8, with χ/2 as the minimum crowd exponent:
- "*0 < σ_h < ζ, b₀ > a > ζ + σ_h + (1−θ), χ/2 > a + 4σ_h*"
- the overlap exception "*exp(−Ω(n^{χ/2} R′/q))*"

I did not re-verify the cross-slice overlap geometry (p. 81, "*either the consulted slice ranges are disjoint or the residual separation is Ω(KR′)*").

### 9. Lemma 2.1 and the bipartite reduction. No objection, recorded for completeness.

- N = min(⌊(R(Q_n)−1)/2⌋, n2^n) gives 2N ≤ R(Q_n) − 1.
- C_n = min(⌊(R−1)/2⌋/2^n, n) → ∞ along the subsequence on which R/2^n → ∞. Such a subsequence exists because each R(Q_n) is finite, so an unbounded ratio must be unbounded along n → ∞.
- Any copy of Q_n that uses only cross edges is a copy in K_{R−1}.
- I grepped the whole paper for intra-side adjacency ("same side", "inside a side", "edges within", …) and found none. Every cube edge joins an even role to an odd one, so the embedding sends A to one side and B to the other. Codegrees are cross-edge counts into the other side.

So "no monochromatic Q_n across the two sides" is all the proof needs.

**Where N ≤ n2^n is used:**
- union over exp(O(n)) labels after Lemma 3.6 (p. 13);
- log g = O(n) in Lemma 3.10;
- "*2N = exp(O(n)) label coordinates*" (p. 28);
- "*the union is legitimate because N ≤ n2^n*" (p. 67);
- N(K′/C_n)^n → 0 (pp. 126 and 132).

**Where N ≥ C_n 2^n is used:** n² ≤ N^{.025} (pp. 32, 62), and column sums O(2^n/N) = O(1/C_n). None of these needs a rate.

### 10. Selection inside the likelihood (§1.3 "The probability comparisons"). No objection.

Lemma 3.7 (p. 14) builds the gate into F_z: "*The gate and every selection rule in F_z must be recomputed as z varies*".

I checked the first application line by line, pp. 30–31:
- "*F_z(y) = 1_E ∏_{u∼v} p_u(y_u) … Selection, validity, and all other local rules in this formula are recomputed for each replacement of z*".
- Q omits the whole tuple W_{c,g(v)}, and the mixture over ID sets is drawn from present IDs only. Neither depends on z.
- On E, F_z ≤ exp((log 2 − c₂a_*)kn)·Q, by the Step 3 mass ratios with n − m matching neighbours.
- Transfer to the injective law (p. 33) is done by applying the Lemma 3.9 joint bound to Φ = 1_E 1_{D_c} with 1_{S_pre} retained, then dropping 1_{S_pre}, then integrating z under its raw prior.

Every step is legitimate. The other applications on pp. 62, 87, 98 and 123 have the same structure, and I checked them at the level of hypotheses: Q independent of the candidate, fallback independent of the candidate, and ε·(number of candidates) = o(1).

### 11. Lemma 3.3 (second part, Kakutani): profile-independence of the output rules at each invocation. No objection.

The hypothesis is "*Conditional on the realized actions, fix each player's output-vector rule independently of the profiles*".

- **p. 32 (§4).** "*The output rules for fixed masks do not depend on their profile probabilities: in particular, the posterior computations condition on the realized masks.*" I checked this: M_c and Q use the realized masks of the tuple and the odd roles. The experiment is the raw one, "*without conditioning on geometric success*", so there is no profile-dependent normalization. The odd-mask player's bound, 2ν (masks of mass ≥ ½ on cheap labels), and the (c, g) player's bound, 2n_{c,g}w_cμ (w_c from Lemma 3.8's 3/λ and e^{−n^{c₃}}, uniform over legal eligibilities), are profile-free. Separation makes each response set nonempty.
- **pp. 95–96 (§10).** "*The mask lookups and all other rules conditional on realized tags have already been fixed, independently of profile probabilities.*" Consistent.
- **pp. 100 and 124.** These are direct Kakutani applications. On p. 124 the paper asserts "*each posterior retains its realized corner law as prior*". I skimmed these.

### 12. Lemma 3.9 checked against the trap recorded in the Lean design note. Checked; no defect.

This item was added at the coordinator's request.

**What the note says.** /tmp/oaimath/171/lean/repo/HypercubeRamsey/S03/Injection/DESIGN.md ("Why the former split failed") records that the formalizers' first breakdown of Lemma 3.9 contained two false intermediate statements:

- **(a) L3.9a `balanced_completion_good_order`.** It asserted "*Real atoms ≤ d^(-.95), but every completed atom ≤ 10/d*". This is false. The note's counterexample is one row with q(0) = 11/d and d = 11^{20}: the row satisfies the atom bound d^{−.95} = 11/d, so preserving it contradicts "≤ 10/d". Only the **dummy** atoms are O(1/d).
- **(b) L3.9b `tracking_label_sampler`.** It asserted "*Some injection law has additive singleton error ≤ d^(-.1)*". This is an existential statement about marginals only. It cannot feed the joint bound. The note's example: for uniform rows, uniform cyclic shifts have exact marginals 1/d, yet two consecutive prescribed labels occur with probability 1/d rather than about 1/d². This violates (3.2), since exp(2d^{−.04}) < d. The note adds that an *additive* singleton error lets a zero-probability target receive positive mass, which a relative error does not.

The note's fix: the joint bound must be proved for the **specific** sequential sampler, conditioned on the tracking event, with relative errors throughout. It also cuts the horizon to t ≤ 3d/4, because "*permitting t=d would destroy*" the denominator lower bound. The note explicitly does **not** claim the paper is wrong.

**Lemma 3.9 as written (pp. 18–21) avoids both traps.**

1. **Atoms (trap a).** Step 1, p. 19: "*First allow label atoms O(d^{−.95}) and column sums at most 1/2. … Add t − m identical dummy rows with law p_dum(y) = (t/d − c_y)/(t − m). The numerator is nonnegative and sums to t − m, so this is a probability law. Its atoms are O(1/d), and every completed column sums to t/d.*"
   - "Its" refers to p_dum only. Real atoms stay O(d^{−.95}).
   - The martingale step correctly uses "*increments bounded by the column atom range*" in Step 1, and "*Its martingale increments are O(d^{−.95})*" in Step 2, so it never needs a 1/d bound on real atoms.
   - "O(d^{−.95})" rather than "≤ d^{−.95}" is exactly the slack that the Step 4 perturbation needs: atoms grow by at most (1+δ)/(1−δ). The paper says "*The perturbed rows satisfy the relaxed hypotheses of Step 1*".
2. **Horizon.** t = ⌈2d/3⌉ ≤ 3d/4. "*Before stopping, all sampling denominators are bounded away from zero*": 1 − D_j^j ≥ 1 − (t−1)/d − 1/20 > 0.28. This matches the note's corrected horizon.
3. **Joint bound and marginals for one specific process (trap b).**
   - Step 2 defines a concrete sequential process: "*At step j, sample row j's law conditional on its label still being free … Call this successful tracking event G, and condition the sampler on G.*"
   - Step 3 compares that same process with an explicit forcing sampler. The likelihood ratio is "*p_i(y_i)/(1 − D_i^i) (i queried), 1 − Σ_{i>j, i queried} p_j(y_i)/(1 − D_j^j) (j ordinary)*".
   - The comparison is relative: "*Integrating this ratio under the forcing law, and dividing by Pr(G) = 1 − exp(−d^{Ω(1)}), gives the joint upper comparison exp(O(d^{−.09}l)) ∏_i p_i(y_i).*" Here **J (|J| ≤ d^{.025}) ranges over every query set**, so a cyclic-shift law would fail it.
   - The singleton lower bound is also relative: "*(1 − O(d^{−.09}))p_i(y_i)*". The paper itself guards the zero-atom and tiny-atom point: "*The target mass was extracted before this tracking exception was bounded; no absolute error is divided by a tiny atom.*" A zero atom gives zero joint mass because ∏p_i(y_i) = 0.
4. **Exact marginals obtained without losing the joint bound.**
   - Step 4, p. 21: "*Let C be the set of all laws on injections of the real rows satisfying the joint upper inequalities relative to those original inputs. These are linear inequalities on a finite probability simplex, so C is compact and convex. Every price-dependent construction just made belongs to this same set, and its marginal vector has price at least that of the original marginal vector. If the original vector were outside the marginal image of C, a separating linear functional would contradict that property.*"
   - The exact-marginal law is therefore a point of C, so it **inherits (3.2) by definition of C**. The marginals come from separation, and no "near-marginal" law is post-processed.
   - The price-directed members of C are the Step 2–3 sampler run on the perturbed rows p′_i ∝ p_i(1 + δ·sign(c_i − c̄_i)) with δ = d^{−.05}.
   - Their joint bound relative to the original p costs "*exp(O(d^{−.05}l + d^{−.09}l)), which fits (3.2)*". I re-derived this: p′ ≤ e^{3δ}p, and O(d^{−.05}) ≤ d^{−.04} for large d.
   - Their centred-price gain ≥ ½δΣ_y p_i\|c_i − c̄_i\| dominates the relative singleton error O(d^{−.09})Σ_y p_i\|c_i − c̄_i\|. So Σ_y q_i c_i ≥ c̄_i holds row by row.
5. **Full outputs.** "*It suffices to construct the labels: the independent conditional draws then give both assertions for full outputs.*" The side data are drawn independently given the labels, so the label bound multiplied by ∏ p̂_i(o_i)/p_i(y_i) gives (3.2) for full outputs. The marginals stay exact.

**Verdict on item 12.** The statement of Lemma 3.9 is not the false intermediate form. It asserts joint relative bounds for every J with |J| ≤ d^{.025}, plus exact marginals, both for one law. The proof establishes both, in the order the Lean redesign adopted: completion with dummy-only O(1/d) atoms, then tracking of the concrete process, then forcing comparison, then perturbation, then separation inside C. The Lean note's table maps each node to TeX lines 627–768, which correspond to these steps.

**Minor exposition point (COSMETIC).** Step 2 says "*no stop and D^a_j = s_j ± d^{−.1}*" and Step 3 then says "*Tracking permits replacement of s_j by D^j_j at error O(d^{−.1})*". The tracking event G is defined by the stop rule plus the d^{−.1} accuracy. The paper never names G's defining inequalities separately, and the Lean `Good` predicate makes them explicit.

A side note for the Lean seat, not my scope: the DESIGN.md text says its analytic nodes "*contain intentional `sorry` placeholders*". The current files contain no `sorry` (grep count 0 in all six Injection/*.lean files), so the note describes an earlier state.

---

## 2. Citation table (scope only)

| Cited result | What the paper claims | What the source says | Verdict |
|---|---|---|---|
| [30] Ramsey 1930 | Each R(Q_n) is finite. | Standard finite Ramsey theorem (not fetched). | MATCH (trivial) |
| [9] Erdős–Lovász 1975, §2 | "*The local lemma and its conditional induction go back to Erdős and Lovász [9, Section 2]*" (p. 13) | Fetched users.renyi.hu/~p_erdos/1975-34.pdf (OCR text). §2, p. 616: "*Lemma. Let G be a (finite) graph with maximum degree d … suppose that A_i is independent of the set {A_j : (v_i, v_j) ∉ E(G)}. Also suppose (3) P(A_i) ≤ 1/(4d). Then (4) P(Ā₁…Ā_n) > 0. Proof. We prove more, namely that (5) P(A₁ \| Ā₂…Ā_n) ≤ 1/(2d)* … by induction". | MATCH (symmetric version, with the conditional induction) |
| [10] Erdős–Spencer 1991, §1 | "*introduced the lopsided nonneighbor condition*" | COULD NOT FETCH: Elsevier, not on the Rényi archive under 1990–92 numbers in OCR-searchable form. Secondary source, Lu–Székely p. 2: "*(in [10], the terminology was lopsidependency graph) … [10] described the proof of Lemma 3 in this special setting*". | COULD NOT FETCH; secondary MATCH |
| [27] Lu–Székely 2007, Lemma 3 | "*see Lu and Székely [27, Lemma 3] for the asymmetric formulation used here*" | Fetched (EJC R63). "*Lemma 3 Lovász Local Lemma (third version) [10] … Let A₁,…,A_n be events with a negative dependency graph G. If there exist x₁,…,x_n ∈ [0,1) with Pr(A_i) ≤ x_i ∏_{ij∈E(G)}(1−x_j) for all i, then Pr(∧Ā_i) ≥ ∏(1−x_i) > 0.*" Here (1) is Pr(A_i \| ∧_{j∈S}Ā_j) ≤ Pr(A_i) for S ⊂ non-neighbours. | MATCH. The paper's Lemma 3.5 replaces Pr(E_i) by a bound p_i and adds Pr(E_i \| A_S) ≤ x_i, the E[W \| ·] comparison and the extra-event F bound. It proves these in-text, and I re-derived them correctly. |
| [24] Kakutani 1941 | Fixed point for the product response correspondence. | COULD NOT FETCH (Project Euclid script wall). Standard: an upper-semicontinuous (closed-graph) correspondence with nonempty closed convex values on a compact convex subset of ℝ^d has a fixed point. A product of finitely many simplices qualifies. | COULD NOT FETCH; statement standard, application correct |
| [20] Hall 1935 | Distinct representatives from Σ_v p_v(y) ≤ 1. | COULD NOT FETCH (Wiley). Standard; the in-text derivation \|S\| = Σ_y Σ_{v∈S} p_v(y) ≤ \|∪ supp p_v\| is correct. | COULD NOT FETCH; trivial use |
| [8] Dirr–Dondl–Grimmett–Holroyd–Scheutzow, §§4–5 | "*Its path-maximum rule is related to the admissible-path construction of Lipschitz percolation*" | Fetched arXiv:0911.3384v2. "*Such paths will be allowed to move downwards … with or without a simultaneous horizontal move, but whenever they move upwards, they must do so to a closed site.*" Lemma 3 path count; 1st proof of Thm 1: G = sites reachable from T₋, F(x) = min{t > 0 : (x,t) ∉ G}, Lipschitz via the diagonal extension. | MATCH ("related to" only; Lemma 3.8's proof is self-contained and does not use [8]). Convention difference: the paper's up-step is *from* a bad site-level, Dirr's is *to* a closed site. Immaterial. |
| [16] Gandhi–Khuller–Parthasarathy–Srinivasan, (P1)–(P3) | "*Preserving individual marginals while choosing distinct representatives … Their negative-correlation guarantee concerns edges incident to a common vertex*" | Fetched (author copy cs.umd.edu/~samir/grant/jacm06.pdf). "*(P1): Marginal distribution. For every edge (i,j), Pr[X_{i,j} = 1] = x_{i,j}. (P2): Degree-preservation … (P3): Negative correlation … For any vertex i and any subset S of the edges incident on i: ∀b, Pr[∧_{f∈S}(X_f = b)] ≤ ∏ Pr[X_f = b]*" | MATCH. Context only; not used in any proof. |
| [23] Hoeffding 1963 | Bounded-difference concentration; the prefix of a random order is sampling without replacement (Lemma 3.9, Step 1). | Fetched (scanned; abstract page read): "*These results are then used to obtain analogous inequalities for certain sums of dependent random variables such as U statistics and the sum of a random sample without replacement from a finite population.*" | MATCH (did not read §6 in detail) |
| [1] Azuma 1967 | Bounded-increment martingale concentration (Lemma 3.9, Steps 1–2; §4 p. 30 "*The bounded-increment inequality [1]*") | Fetched (J-STAGE scan, OCR). Lemma 1 / Theorem 1: for martingale differences with \|x_n\| ≤ K_n, an exponential moment bound E exp(tΣb_k x_k) ≤ ∏cosh(t b_k)-type, giving Gaussian tails. | MATCH |
| [15] Freedman 1975 | "*This is the bounded-jump exponential estimate used here; compare [15]*" (Lemma 3.10, Step 6) | Fetched (JSTOR scan). (1.1) \|X_n\| ≤ 1; "*(1.3) LEMMA (a) E{exp(λX)} ≤ exp[V e(λ)]*" with e(λ) = e^λ − 1 − λ; "*(1.6) THEOREM … P{S_n ≥ a and T_n ≤ b for some n} ≤ exp[−a²/(2(a+b))]*". | MATCH as an analogue. The paper uses the continuous-time pure-jump version (jumps ≤ λ_*, v² × variance-rate compensation) and derives it in-text. I re-checked the arithmetic: v = n^{−A_*/4}/(2T₀λ_*) gives exp(−n^{A_*/2−o(1)}). |

Results cited elsewhere in the paper but not used in §2–3: Moser–Tardos [28], Harris–Srinivasan [22] and Haeupler–Saha–Srinivasan [19] (only §17.3, p. 144); Finner [11] (§9, p. 87); Hamming [21] (§10, p. 89).

---

## 3. Parameter-dependency table (scope)

| Constant | Fixed where | Depends on | Used where / constraint |
|---|---|---|---|
| C_n = N/2^n | Lemma 2.1 | the counterexample sequence | → ∞ at no rate; only "C_n > fixed constant eventually" is used (pp. 13, 33, 126, 132) |
| N ≤ n2^n | Lemma 2.1 | — | unions over N = e^{O(n)} labels (pp. 13, 28, 67, 126); log g = O(n) in Lemma 3.10 |
| κ | Def. 3.1 / Lemma 3.2, per property | the property **and the stabilized sequence**; halved per later discard stage; ÷k per finite union | Lemma 3.3 (K = 4/κ); not uniform over properties; never needs to be |
| K = 4/κ, K′ | Lemma 3.3; §4 Step 6 | κ (hence the sequence) | only as a multiplicative constant against n^{−c}, e^{−Ω(n)} or C_n → ∞ (item 3) |
| x_i, p_i | Lemma 3.5, per application | the application | needs p_i ≤ x_i ∏(1 − x_j) |
| K, f, L, d_v, Markov threshold T | Lemma 3.6, per application | the application; T chosen after K and the mean of d | nfL = o(1); T > 2eK·(mean d) for the union over N ≤ n2^n labels |
| ε, s | Lemma 3.7, per application | the application | ε·#candidates = o(1) (e.g. p. 33: exp(O(n)) vs e^{−c₂a_*kn/4}) |
| D, J₀ > 2, 0 < b₀ < b < 1 | Lemma 3.8 input | — | crowd and hole tails |
| ρ (sublinear case) | Lemma 3.8 | b, b₀, D: b > b₀ + (D+1)ρ | crowd mean n^{b₀+Dρ} < threshold n^b |
| 0 < σ < ζ < 1, θ, a | Lemma 3.8 | b₀ > a > ζ + σ + (1−θ), b > a + 4σ; for (iii) θ > .9 | Step 4 exponent comparisons; top scale a + (1−ζ)θ > 1 |
| R₀, M, Rᵢ, H, h | Lemma 3.8 | n, σ, ζ; h ≈ (1−ζ)/σ bounded | scale induction |
| ηᵢ ∈ [¼,½], sᵢ ∈ [⅛,¼], tᵢ ∈ [⅓,¾] | Lemma 3.8, Step 1 | fixed gaps | child thresholds |
| K (separation), c′ | Lemma 3.8, Step 3 | K large absolute; c′ small relative to (ηᵢ₋₁ − ηᵢ)/K | covering argument |
| ε (overlap) | Lemma 3.8, Step 4 | below all gaps sᵢ − sᵢ₋₁, tᵢ − tᵢ₋₁ | private-region transfer |
| c in exp(−n^{1+c}), exp(−n^c) | Lemma 3.8 conclusion | all of the above | §4 p. 32 c₃; §10 p. 93 c₀; §14 with n := h |
| n₀ of Lemma 3.8 | implicit | all of the above | must precede Q₀ in §14 (item 1); p. 113 item 3 does this |
| .95, .4, .025, .04, δ = d^{−.05}, t = ⌈2d/3⌉ | Lemma 3.9 | absolute | d₀ absolute; §16 needs d_i ≥ d₀, ensured by Q₀ |
| B | Lemma 3.10 input | the application (3, 3, 4, 5 at pp. 68, 78, 104, 126) | — |
| K₀ | Lemma 3.10 | B: (.1 − 2√θ)K₀ > B and B < (.4 − θ − √θ)K₀ | giant tail; incidence n^{−.6K₀} |
| A_*, P_* | Lemma 3.10 | K₀, B: A_*/4 > 2K₀ + 3B, P_* > 4B and large | tracking; trimming (1−ε)^{−n^B} = 1 + o(1) |
| θ₀ = 10^{−8}, θ ≈ 10^{−6} | Lemma 3.10 | absolute, chosen before K₀ (needs 2√θ < .01) | branching moments |
| T₀ = K₀ log n, L = ⌈n^{.1K₀}⌉, δ = n^{−.01K₀}, λ_* = O(n^{−A_*}) | Lemma 3.10 proof | K₀, A_* | Steps 4–8 |
| implied constant in log g ≤ Cn | Lemma 3.10 | given | only the Step 6 union e^{Cn − n^{A_*/2−o(1)}}; A_* does not depend on C |

There are no cycles inside §3. Lemma 3.10's ordering is θ₀ → K₀(B) → A_*, P_*(K₀, B), and it is consistent.

---

## 4. What I verified line by line vs what I only skimmed

**Verified line by line, with every inequality re-derived:**
- **Lemma 2.1:** N, cross-edge restriction, C_n → ∞, both sides of N.
- **Definition 3.1 and Lemma 3.2.**
  - Negation of "available": ∀κ > 0, infinitely often τ_n ≤ κN, i.e. liminf τ_n/N = 0, which is equivalent to "o(N) removals along a subsequence eliminate the property". So the dichotomy is exact, on the current sequence at each stage.
  - Both alternatives survive passing to subsequences; the non-available alternative never needs to.
  - Diagonalization: choose n_j ∈ S_j with ε^{(i)}_{n_j} < j^{−2} for all i ≤ j. Total removals ≤ N/j. An earlier available property loses ≤ N/j < κ/2·N. An absent property stays absent.
  - Finite union (item 2); finite menu.
- **Lemma 3.3, part 1:** price threshold 2P/(κN), fewer than κN/2 expensive labels, separation from the downward-closed box with c ≥ 0 forced, K = 4/κ.
- **Lemma 3.3, part 2:** response sets nonempty, closed and convex; multilinear expectations give closed graph; Kakutani.
- The Hall paragraph (p. 12).
- **Lemma 3.5:** all four assertions, via the induction split S = (S ∩ Γ(i)) ∪ (S \ Γ(i)), the chain rule for Pr(A_T \| A_S), the W-comparison and the F-bound. Also: independent variables imply the hypothesis.
- **Lemma 3.6:** removal-pattern expansion, reverse-order summation, total (d̄ + nfL)^n; the remark's union and column-sum conversion.
- **Lemma 3.7:** exception mass ≤ ε∫Q, posterior density ≤ e^s/ε, disintegration identity.
- **Lemma 3.9, Steps 1–4** (re-checked against the DESIGN.md trap, item 12):
  - dummy rows: law, O(1/d) atoms, column sums t/d;
  - random-order prefix concentration exp(−d^{.65});
  - drift formula; both summations by parts; Grönwall e_b = O(d^{−1/8});
  - likelihood ratio orig/forcing: cancellation to O(l d^{−.1} + l² d^{−.95}) in the log;
  - lower singleton bound via Pr_forcing(G);
  - centred-price gain ≥ ½δΣp\|c − c̄\| beats the O(d^{−.09}) error;
  - perturbation cost e^{O(d^{−.05})l} ≤ e^{d^{−.04}l};
  - compact convex C and separation giving exact marginals.
- **Lemma 3.10, Steps 1–8 bookkeeping and logic:**
  - trimming; dummy rows; Poisson greedy matching; first-arrival principle;
  - leaf rectangles and the forcing coupling (hit edges of E are never inspected by a disjoint-active F; shared edges are absence-absence, and the monotone coupling preserves them), giving Pr(E \| A) ≤ Pr(E);
  - LLL charge 2Pr(E) with neighbour sum 2Ln^{−.6K₀};
  - Mecke-insertion walk sum cosh(√θT₀) + θ^{−1/2} sinh(√θT₀);
  - branching moment bounds (4δe^{2√θt}/√θ and 4δe^{2√θt}, with e^x − 1 ≤ 2x) and the giant tail;
  - ODE z′ = −qz, q′ = −θzq, q = 1 − θ + θz, (log zq)′ = −(q + θz), ∫zq = 1 − z(T₀);
  - Freedman-type tail; Grönwall; the background/outside-process identity in Step 7;
  - final exponent conditions in Step 8; the joint-target partition into product rectangles.
- **Lemma 3.8.**
  - Step 2: hole e^{−s₀n^{b₀}}; crowd binomial tail; count exp(O(R₀ log n)).
  - Step 3: covering argument and rise count −η_{i−1}MR′ + O((q+1)KR′); linear-case intersection.
  - Step 4: overlap tails; transfer of holes and crowds to private regions; Pr(C \| P,E) ≤ 1_{B_pos} + Pr(B_act \| P) + ∏b_ℓ; independence of P_ℓ; exponent comparisons including b > a + 4σ.
  - Step 5: a + (1−ζ)θ > 1; good maximizing site-level; Lipschitz by one; (ii) and (iii) exponents; the 3/λ tie bound; the forced-center variant.
- **Parameter verification of the Lemma 3.8 invocations** at p. 28 (§4: D=2, b=ω/30, b₀=b/4, ρ=b₀/10, λ=n¹⁰, ζ=b₀/20, σ=ζ/10), p. 71 (linear, r = ⌊.01n⌋), p. 90 (D=6, ρ=10δ, b₀=50δ, b=140δ, ζ=8δ, 1−θ=δ, a=20δ: 120δ < 140δ, 50δ > 20δ > 9δ + σ_g) and p. 119 (ω/8 > ω/12 > ω/15 + σ_g, ω/2 > ω/12 + 4σ_g).
- **Application of Lemmas 3.6–3.9 in §4,** pp. 28–33, line by line.

**Spot-checked at the hypothesis level** (statement vs. invocation, without re-proving the surrounding section):

| Lemma | Invocations checked |
|---|---|
| 3.2 | p. 27, p. 64, p. 69, p. 79 (×2), p. 97 (×2), p. 111; countability: rational parameters throughout |
| 3.3 | p. 27, p. 32, p. 65, p. 81, p. 96; p. 100 and p. 124 skimmed |
| 3.5 | p. 58, p. 66, p. 67, p. 83, p. 105, p. 137 |
| 3.6 | p. 33, p. 60, p. 63, p. 66, p. 76, p. 96, p. 126, p. 128 |
| 3.7 | p. 31, p. 62, p. 87, p. 98, p. 123 |
| 3.8 | p. 28–32, p. 71/73, p. 90–93 (\|E\| ≥ .99λ ≥ λ/3, tie 1/(.99λ)), p. 119–123 |
| 3.9 | p. 32, p. 62, p. 137–138 |
| 3.10 | p. 68 (q = ⌈n^{4d}⌉ so e^{−.02q} ≪ n^{−P_*}), p. 78, p. 88, p. 96, p. 126 |

All of these satisfy the lemma's hypotheses as stated.

**Skimmed, not fully verified:**
- Lemma 3.8, Step 3: the sublinear-radius intersection estimate (item 7).
- Lemma 3.10, Step 5: the deferred-construction domination ("*attach its sole processing to the node making its highest request*"). The logic is plausible, since horizons are processed in decreasing order, but I did not formalize it.
- Lemma 3.10: the mesh limit (item 6).
- The §9 adaptation of Lemma 3.8 (item 8).
- The direct Kakutani uses on pp. 100 and 124.
- Hoeffding §6 and Kakutani 1941 themselves (not read or not fetched).

---

## 5. Verdict for scope

**§2 and §3: HOLDS AS READ.** I found no mathematical gap.

The remaining items are exposition or unchecked detail:
- Lemma 3.8 should be stated for a free parameter, because §14 uses it with the bounded internal dimension h (item 1).
- The finite-union sentence of Lemma 3.2 should be read with "any subsequence" (item 2).
- κ and K depend on the sequence; I verified this is benign (item 3).

**COULD NOT CHECK:** Erdős–Spencer [10], Kakutani [24] and Hall [20] as primary sources (paywalled or script-walled); their content is standard, and the paper's uses match the standard statements. I also did not fully re-derive the sublinear ball-intersection exponent in Lemma 3.8, Step 3, or the Step 5 branching domination in Lemma 3.10.
