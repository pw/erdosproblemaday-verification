# Hostile referee report — seat `initial_a`

**Paper:** OpenAI, "The hypercube Ramsey number has linear order" (23 Sept 2026), paper.pdf in /tmp/oaimath/171 (PDF page = printed page).
**Scope:** §4 (Lemma 4.1, pp. 26–34), §5 (Lemma 5.1, pp. 34–50); orientation from §1.3, Fig. 1, App. A Table 1 rows "Power-width bias versus purity" and "Constant broad side" (pp. 166–167). §3 statements read (pp. 11–25) only as interfaces; §3 proofs NOT refereed here.
**Method:** every displayed formula in scope was read from the rendered PDF pages (not the text dump); every inequality in §4 was re-derived by hand; the §5 estimate chain was re-derived as described in Part D. No code from the downloaded files was run.

**Bottom line:** I found **no FATAL objection and no GAP** (mathematical or expository) in §4 or §5. §4 holds as read, line by line. §5 holds as read for every displayed estimate I re-derived. A few combinatorial sub-claims in §5 I checked only to order of magnitude against slack that is large (Part D lists them). The objections below are UNCLEAR/COSMETIC. One of them (Obj. 4) is a justification that is literally inadequate as written but is rescued by slack that is never stated.

---

## Part A — Objections

### Obj. 1 — Lemma 4.1 statement: undefined terms and an unstated quantifier on (ii). Severity: UNCLEAR (exposition only)
Location: Lemma 4.1, p. 26.
> "the following two hypotheses cannot both hold along a bad sequence: (i) Pairs of laws at widths ≤ n^β, n^γ on X, Y respectively with absolute bias ≥ n^{−h} from half are available; (ii) On the current sets there is no pair at respective widths ≤ 2n^β, 2n^γ having defect ≤ exp(−n^h) in either color."

The paper never defines "bad sequence" (the term recurs in Cor. 7.2 and Cor. 8.2). "Current sets" is also undefined. (ii) carries no "eventually"/"for all large n". The proof uses (ii) at every large n of the (sub)sequence on which it builds the cube: Step 3, p. 29, "contrary to hypothesis (ii)". Read the statement as follows. "Bad sequence" is the counterexample sequence of Lemma 2.1 after stabilization. "Current sets" are the retained sides. (ii) holds for all sufficiently large n. That reading matches how the lemma is used: Cor. 7.2, p. 69, "Stabilization therefore makes this purity property absent", where "absent" means eventually absent in the sense of Lemma 3.2. Under that reading the proof is complete. It would also survive (ii) holding only on an infinite subsequence: pass to that subsequence first, since availability in (i) survives restriction to a subsequence.
Fix: write "(ii) eventually, on the retained sides, there is no pair …" and define "bad sequence := counterexample sequence of Lemma 2.1".

### Obj. 2 — Step 1 of Lemma 4.1: "supported in this patch" is ambiguous. Severity: COSMETIC
Location: p. 27.
> "We also retain the following upper density bound: any laws supported in this patch with respective widths at most s_X + ½n^{β−ω/2}, s_Y + ½n^{γ−ω/2} have G-density at most p + n^{−ω/3}. Both laws fit the next budget pair, which proves this bound independently of the trimming."

The bound is derived for all laws on the residual sets: ≤ P_{j+1} < P_j + n^{−ω/3} = p + n^{−ω/3}. It is used (Step 3, p. 29: "The intrinsic upper density bound from Step 1 also gives Pr{q(x) > p+n^{−ω/3}} ≤ exp(−n^{β−ω/2}/4)") only for laws supported in supp μ_i × supp ν_i: μ_i^M conditioned on an exceptional set, and η ⊂ supp ν_i^M. Under the reading "supported in supp μ_i, supp ν_i" the patch property is intrinsic to its supports, as Lemma 3.2 requires. Under the other reading it is still monotone under removals. Either way the Lemma 3.2/3.3 steps ("This construction works after every removal allowed by hypothesis (i), so the resulting patches are available. Lemmas 3.2 and 3.3 allow us to pass to a subsequence, fix one available color G …") are legitimate. Fix: say "supported in supp μ_i × supp ν_i".

### Obj. 3 — §4 Step 3, own-key fractions: an unproved elementary inequality. Severity: COSMETIC (true)
Location: p. 30.
> "at every other own-key entry, log q ≥ −log 2 + .7a_i"

A non-dip entry has q ≥ p − a_i/4 = ½ + ¾a_i. So one needs log(1 + 1.5a) ≥ 0.7a for all a ∈ (0, ½], not just small a: a_i is only bounded below by a_* and may be of order 1. The inequality does hold on all of [0, ½]. The left side is concave, the two sides agree at 0, and at ½ we have log 1.75 = 0.5596 ≥ 0.35. The ensuing "for sufficiently small c_1" is satisfied by any c_1 ≤ 0.65: the dip loss is ≤ (a_*k/(20L))·L = a_*k/20, so the log-ratio is ≥ k(−log 2 + .7a_i) − a_*k/20 ≥ k(−log 2 + .65a_*). No issue, but the paper gives no justification.

### Obj. 4 — §5.4 Stage 4: "density multiplier 1+o(1) per variable" does not by itself control products over J→∞ variables. Severity: UNCLEAR (exposition gap; the statement is true)
Location: p. 43.
> "Their probabilities from Stage 3 are o(1), so the low variables remain independent with a density multiplier 1 + o(1) per variable. A regular Step 2 pattern uses O(j + 1) low keys, so its probability multiplies by (1 + o(1))^{O(j+1)} and remains at most e^{−δu_j/16}. A high Step 3 pattern reads only O(J) low keys: the possible low tuple's S-list and the optional keys named in the record. Its bound remains e^{−c_{H0}s/3}."

Where the o(1) comes from: Stage 3 restricts small-prefix (optional-key) tests to conditional failure ≤ e^{−δL/8} with L = u_* = ⌈η log m⌉. So the per-variable pretrim loss is O(m^{−δη/8}), and δη is very small (δ ≪ gaps between the a_i; K_hη < .025). For a high pattern the multiplier over O(J) = O(m^{1/20}) variables is therefore exp(O(m^{1/20 − δη/8})). That tends to ∞, so "(1+o(1)) per variable" does not by itself give "remains e^{−c_{H0}s/3}". What rescues the claim, unstated in the paper: s = ⌈K_sJ log m⌉, so exp(O(J·m^{−δη/8})) = e^{o(s)}, and the stated bound follows. For the regular Step 2 pattern, (1+o(1))^{O(j+1)} = e^{o(j+1)} ≤ e^{δu_j/16} since u_j = ⌈K_1(j+4)log m⌉. So the claim is mathematically correct; the reason given is not the operative one.
Fix: one sentence. "The multiplier is exp(O(J m^{−δη/8})) = e^{o(s)} at high patterns and e^{o(j+1)} at regular ones."

### Obj. 5 — Constants declared but unused, and symbol collisions. Severity: COSMETIC
- p. 34: "Fix constants a0 = 1/3 < a1 < · · · < a8 < τ0 < τ1 < log 2". a_7 and a_8 never appear: a_6 is the last used (p. 49), and "the other exponents fit the gap below τ0" (p. 50) covers a_6 + δ < τ0.
- Symbol reuse inside the scope:
  - η: mass threshold exp(−n^{γ−ω/2}/2) in §4 Step 1, the law on Y in §4 Step 3, and the high block-length constant in §5.
  - m: number of gadget bits Θ(n^{γ+13ω}) in §4; ⌈n^α⌉ in §5.
  - b: Lemma 3.8 crowd exponent; odd state b in §5; stream lengths b_j (the paper flags this one itself, p. 38: "These height exponents are unrelated to the stream lengths b_j").
  - L: n^h in §4; cap in Lemma 3.6; test scale in §5.4.
  - K′: Step 6 constant in §4; Step 1 cap in §5.
  - θ: Lemma 3.8; hidden target ϑ; θ_0 of Lemma 3.10.
  - D: Lemma 3.8; D_c; ID sets 𝒟.
  - a: Lemma 3.8's a vs the a_i chain.

None of these collisions creates a wrong inference that I could find.

### Obj. 6 — §5.3/§5.5: record and configuration counts asserted, not derived. Severity: UNCLEAR (not refuted; large slack)
Location: p. 39.
> "Choosing their lists and assigning the exceptional states gives logarithmic record counts at most O(T log n + (j + 1) log T + k∗1_{j=J}), b low, O(T log n + (J + 1) log T), b high."
> "There are O(T + j) low tuples around a low state."

These counts feed three places:
- the "n disjoint failures" union in §5.5 ("bound the probability of n disjoint failures by exp(−Ω(nk′_j)) at a low star and exp(−Ω(ns)) at a high star, including the union over their records");
- the Q_b mixtures in §5.6 ("The low record count, including a mask if needed, fits the reserved margin because k′_j ≤ k");
- the Stage-5 group probabilities (p. 44).

I reconstructed the count only roughly:
- choose ≤ T IDs out of poly(n) present IDs: T log n;
- one ID-subset per boundedly many generic type variant: O(T);
- ≤ O(j) exceptional neighbor states (sign/F changes from chunks within distance 1.5 of mid-weight, at most j such chunks), each assigned one ID: (j+1) log T;
- the mask: log C(M_*/u_*, k_*/u_*) = O(k_*).

Each required margin is enormous compared with these counts:
- k′_j ≥ K_2 m^{.02} versus T log n = m^{.001} log n and k_* = m^{.005};
- s = K_s J log m versus J log m and T log T.

So even a constant-factor error in the counts would be absorbed. I did not verify the exact combinatorics of "generic variants" line by line.

### Obj. 7 — The brief's question on §5.4 ("a Kakutani/Lemma 3.3 application?"): No. Severity: none (clarification)
§5.4 uses Markov's inequality plus the conditional-avoidance Lemma 3.5 (independent-variable local lemma), in five stages. It does not use Kakutani or Lemma 3.3. The hypotheses check out stage by stage:
- **Stage 2:** the bin variables (A_w, W_w) are independent given V_0, and events are grouped per bin with scope equal to the bins of a bounded C_i-neighbourhood. The grid is 300-dimensional with O(n^{.04}) bins per axis, so the degree is bounded. Per-bin pattern sums are o(1) because the conditional failure functions are sign-invariant: π_ℓ depends on (i, j), not on t, so no 2^m union arises.
- **Stage 3:** the high U_ℓ are independent given the base. The bounded-degree local lemma applies with o(1) charges.
- **Stage 4:** a separate per-variable restriction, so independence is preserved.
- **Stage 5:** independent trimmed low keys. Dependency degree and groups-per-variable are m^{O(1)}, and group probabilities are ≤ m^{−K_deg}.

The only minimax in §5 is the separating-hyperplane construction of the common high-row law 𝓡 (p. 41). It is valid: 𝔉 is a compact convex set of laws on a finite set, the costs E^c_h are finite (Q̃ is smoothed by a uniform component), and the grid ξ̂ satisfies ξ_c ≤ (1+ε_g)ξ̂_c. Kakutani, via Lemma 3.3, is used in my scope only in §4 Step 1 (balanced mixture) and §4 Step 6 (mask profiles). There, all hypotheses hold:
- players: 2^{n−1} odd roles and the (ID, key) pairs, all finite;
- action sets: masks, finite;
- output rules do not depend on profile probabilities ("the posterior computations condition on the realized masks", p. 32);
- each player's bound is achievable against arbitrary opponents' profiles: the price-≤-2×mean mask, by separation.

### Obj. 8 — On item (d) of the brief: τ1 < log 2 is necessary, but the operative condition is τ1 < log 2 − H_bin(2ρ), and it enters through the repeat term, not the column sum. Severity: none (the paper is correct; this corrects the brief's framing)
p. 50: "its repeat cost is at most n exp{−n(log 2 − H_bin(2ρ)) + o(n)}O(e^{τ1 n}) = o(1)."
p. 38: "Choose ρ > 0 so small that the binary ball entropy at 2ρ, in natural logs, is less than log 2 − τ1."
The even column sum equals (|A|/N)·(normalized average load) = O(1)/(2C_n). The O(1) is the scattered-moment bound of Lemma 3.6. That bound needs nfL → 0, with cap L = O(e^{τ1 n}) and near fraction f = e^{−n(log 2 − H_bin(2ρ)) + o(n)}: the near set is linear-radius 2r + o(n) with r = ⌊ρn⌋, measured in residual coordinates. ρ is chosen after τ1, so there is no cycle.

---

## Part B — Citation table (in-scope citations and tools invoked in scope)

| Cited result | What the paper claims / uses | What the source says (quote) | Verdict |
|---|---|---|---|
| [1] Azuma 1967, Tohoku Math. J. 19, 357–367. Read: J-STAGE scan, refs/azuma1967/azuma.pdf, pp. 1–3. | p. 30: "The bounded-increment inequality [1] shows that an own-key last tuple has at most a∗k/(20L) dips, except with probability exp(−Ω(ka∗²/L²))." Applied to X_j = I_j − Pr(I_j \| 𝓕_{j−1}), with \|X_j\| ≤ 1 and Pr(I_j \| ·) ≤ o(a_*/L). | Remark 1: "If (x_n) is a sequence of martingale differences such that \|x_n\| ≤ K_n a.s. for all n, then … E{exp(tx_n)\|𝔄_{n−1}} ≤ cosh(tK_n) ≤ exp(t²K_n²/2)". Lemma 2: "E{exp(tS*_n)} ≤ 8 exp((t²/2)Σ b_k²)". | MATCH. The tail form follows by Markov, one standard step left implicit: Pr(Σ X_j ≥ t) ≤ exp(−t²/(2k)) with t ≍ a_*k/L. |
| [14, Lemma 2.1] Fox–Sudakov 2009. Read: arXiv:0707.4159v1. | p. 29: "These filters use the common-neighborhood sampling operation of dependent random choice [14, Lemma 2.1]." Attribution only, not load-bearing. | "If ε > 0 and G = (V1,V2;E) is a bipartite graph with \|V1\| = \|V2\| = N and at least εN² edges, then for all positive integers a, d, t, x, there is a subset A ⊂ V2 with \|A\| ≥ 2^{−1/a}ε^t N such that for all but at most 2ε^{−ta}(x/N)^t·C(\|A\|, d) d-sets S in A, we have \|N(S)\| ≥ x." Proof: "Let T be a subset of t random vertices of V1, chosen uniformly with repetitions. Set A = N(T)". | MATCH (attribution) |
| [20] Hall 1935. | p. 34: "Hall's theorem [20] assigns them distinct representatives". Hall's condition is supplied by p. 12: \|S\| = ΣΣ p_v(y) ≤ \|∪ supp p_v\|. | — | COULD NOT FETCH (Wiley returned HTML; other seats' copies are HTML stubs). The statement is the textbook marriage theorem and the condition supplied is exactly Hall's. |
| [24] Kakutani 1941, via Lemma 3.3 (§4 Steps 1 and 6). | Fixed point of a closed-graph, nonempty-convex-valued correspondence on a product of simplices. | — | COULD NOT FETCH (Project Euclid returned HTML). Textbook statement; application hypotheses verified in Obj. 7. |
| [23] Hoeffding 1963. Uncited at point of use: "Bounded-summand concentration", §4 Step 2 (p. 28) and §5.6 (p. 48). Read: refs/hoeffding/h.pdf (another seat's download), JASA pp. 13–16. | §4: deviation of Σ_g α_g Nμ_{i_g}(x) bounded by exp(−Ω(exp(cn^{γ+ω}))). §5.6: exponent nk_*²/(D_H+O(1))². | Theorem 2: "If X_1, …, X_n are independent and a_i ≤ X_i ≤ b_i (i = 1, 2, …, n), then for t > 0, Pr{X̄ − μ ≥ t} ≤ e^{−2n²t²/Σ(b_i−a_i)²}." | MATCH. §4: Σ_g ε_g² ≤ (max ε_g)(Σ ε_g) ≤ e^{−cn^{γ+ω}+4n^γ}, giving a doubly exponential tail. §5.6: exp(−2(a_5−a_4)²k_*²n/(D_H+O(1))²). |
| Lemma 3.5 sources [9, 10, 27] (used in §5.4 and inside 3.10). | Independent-variable conditional avoidance. | Not fetched by me; §3 seat's scope. | Application checked against Lemma 3.5 as stated (p. 12): see Obj. 7. |
| Lemma 3.9 (d = N), §4 Step 7. | Hypotheses: atoms ≤ d^{−.95}, column sums ≤ .4, l ≤ d^{.025}. | Paper's statement, p. 19. | Interface MATCH: atoms N^{−1}e^{O(n^γ)} ≤ N^{−.95} since N ≥ 2^n; column sums ≤ 1/10; n² ≤ N^{.025}. |
| Lemma 3.10 (B = 2), §5.6. | Hypotheses: log g = O(n); Σ_a p_a(y) ≤ θ_0; p_a(y) ≤ n^{−A_*}; predicates ≤ n^{−P_*}; ≤ n^B rows per predicate and ≤ n^B predicates per row. | Paper's statement, p. 21. | Interface MATCH: g = N ≤ n2^n; column sums ≤ θ_0 from §5.5; atoms e^{o(n)}/N (D_L = m^{.15}, D_H = O(m^{.05} log m)); predicate failure e^{−n^{1−.09α+o(1)}}; n rows per predicate and n predicates per row. |
| Lemma 3.8, §4 Step 3 and §5.3. | Sublinear radius in §4, linear radius in §5. | Paper's statement, p. 15. | Interface MATCH. §4: b = ω/30, b_0 = b/4, ρ = b_0/10 give b_0 + 3ρ = 0.325b < b; ζ = b_0/20, σ = ζ/10; e.g. θ = 1 − b_0/4, a = b_0/2 give ζ+σ+(1−θ) = 0.305b_0 < a < b_0 and a+4σ = 0.52b_0 < b. §5: r = ⌊ρn⌋ ≤ (1/4+o(1))d; θ > 1 − .001α > .9; √m ≤ H. |
| Lemmas 3.6 and 3.7. | Scattered moments; gated posterior. | Paper's statements, pp. 13–14. | Interface MATCH at every in-scope use (Part D). |

---

## Part C — Parameter-dependency table

### Lemma 4.1 (§4)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| β ≤ γ | lemma input (rational in Cor 7.2/8.2) | — | widths |
| ω = min(β, 1−γ)/1000 | Step 1 | β, γ | everything below |
| h = ω/10⁶ | Step 1 | ω | (i), (ii), a_* = n^{−h}, L = n^h |
| k = ⌈n^{ω/3}⌉ | Step 1 | ω (sequence in n) | tuple length |
| plateau mesh: j ≤ ⌊n^{ω/2}/2⌋; step n^{−ω/3}; trim n^{−ω/5} | Step 1 | ω | plateau, trimming |
| κ (tolerance of (i)), then κ/2 after the color choice | stabilization; finite-union clause of Lemma 3.2 | the fixed subsequence only, not n | menus, K |
| K = 4/κ′, doubled after drawing the i_g | Lemma 3.3; Step 2 | κ | balanced loads |
| p_i = ½ + a_i, j_i, s_X, s_Y | per patch | n, removal, witness | **only through bounds uniform in them** (a_i ≥ a_*, s_X ≤ 1.5n^β, s_Y ≤ 1.5n^γ) — OK |
| s′ ≍ n^{2ω}, S = s′+1, ⌊n^{γ−ω}⌋ gadgets, m = Θ(n^{γ+13ω}) | Step 2 | γ, ω | keys, \|Z_u\| |
| D = 2; b = ω/30; b_0 = b/4; ρ = b_0/10; ζ = b_0/20; σ = ζ/10; θ, a | Step 3 | ω | Lemma 3.8, H |
| T = ⌈3n^b⌉, λ = n^{10}, r = ⌊n^{1−ρ}⌋ | Step 3 | b, ρ | validity, eligibility |
| c_1 ≤ 0.65 (absolute) | Step 3 | — | own-key ratio |
| c_2 ∈ (0, c_1) | Step 5 | c_1 | gain |
| c_3 | Lemma 3.8(ii) | Lemma 3.8 parameters | w_c |
| K′ ≈ 2(3+o(1)) | Step 6 | — | even loads |
| Markov thresholds in Step 7 | Step 7 | K, K′ | column sums |

**No cycle.** h depends only on (β, γ), not on κ, which is what Cor. 7.2's stabilization needs. Nothing depends on removed sets or witnesses except through uniform bounds.

### Lemma 5.1 (§5)

| Constant | Fixed where | Depends on | Used where |
|---|---|---|---|
| γ, K_0′, χ | input | — | — |
| q_0 | §5.1 | χ (needs log(2/χ²)/q_0 + log(1/.9) ≤ 1/3) | segment density e^{a_0q_0} |
| a_0 = 1/3 < … < a_6 (< a_8) < τ0 < τ1 < log 2 | §5.1 | absolute | likelihood chain |
| δ | §5.1 | gaps between the a_i | all denominator tests |
| K′ (cap), K″ (A_K) | §5.2 | a_0, a_1, δ, χ; \|C_i\| ≤ 601 | caps, A_K |
| K_h, then η | Order of constants, p. 44 | a_1 + δ < K_h; K_hη + .005 < .03 | high pools |
| K_1 → K_2 → K_0 → K_D → K_s | Order of constants | earlier constants (K_0 depends on K_1, K_2; K_D on K_0) | u_j, k_j, high cap, D_H, s |
| c_{L0}, c_{H0}, c′ (clip rate), L_0, ε_g, δ′, ε′, η_D | §5.3 | a_3, δ; **independent of K_s** (claimed and verified: the martingale constants depend on L_0, δ′ only) | Step 3 / high rows |
| c_L = c_{L0}/4, c_H = c_{H0}/6 | Stage 5 | c_{L0}, c_{H0} | history bounds |
| K_deg | Stage 5 | arbitrary | local lemma |
| υ_0 (υ_0 + τ0/τ1 < 1), υ_1 ∈ (τ0/τ1, 1−υ_0) | p. 44, p. 50 | τ0, τ1 | even row |
| K_B | p. 44 | q_0, υ_0, K_0′, K″, K_h | prior-heavy |
| ρ | p. 38 | τ1 (H_bin(2ρ) < log 2 − τ1) | r, near set |
| α | **last** among likelihood constants | everything above | m, J, T, k_*, s, rarity |
| b > b_0, σ, ζ, θ, a (height) | after α | b < .001α | Lemma 3.8 |
| T = ⌈m^{.001}⌉, λ = n^{10}, D = 8 | §5.3 | α | IDs |
| D_L = m^{.15}, D_H = K_DJ log m | §5.3 | α, K_D | caps |
| θ_0, A_*, P_* | Lemma 3.10 with B = 2 | B | odd injection |

**No cycle.** The scale relations TM_* = o(J), T log n = o(k_*), T log n = o(m^{.02}), and T + J = o(s) hold for every fixed α. The α-dependent requirements, with α chosen last:
- K′K_1·5α ≤ .02;
- rarity n^{−.13J} beating e^{O(K_BK″K_sαJ log n)};
- D_H = o(J log n·.13);
- α < .02, needed for the tail Pr(j ≥ h) ≤ n^{−.13h};
- α < .1, needed for O(mn^{.3}) = o(n^{.4}).

---

## Part D — What I verified line by line vs what I skimmed

### §4 (Lemma 4.1) — verified line by line
- **Step 1.** Plateau existence: ⌊n^{ω/2}/2⌋·n^{−ω/3} > 1. Trimming inequality t(n^{−ω/5} + n^{−ω/3}) ≤ n^{−ω/3} + η, re-derived from the mean decomposition. Width budgets: s_X ≤ 1.5n^β, and the doubled budgets accommodate the mask, conditioning and filter costs. Upper density bound via P_{j+1}. Availability across removals. Finite-union (color) and finite-menu use of Lemma 3.2. Lemma 3.3.
- **Step 2.** Gadget invariant t_(a) ≤ aS ≤ bS ≤ t_(b). O(log n) outputs under one-bit changes, including the tie argument (S ≥ 4, integer midpoints never hit at a leaf). Output probability (2/3)^{s′}. Bit count m = n^{γ+13ω} = o(n). \|Z_u\| ≤ n^{γ−ω+o(1)}. Key-probability bound exp(−Ω(n^{γ+ω})). Balanced tag assignment via Hoeffding.
- **Step 3.**
  - Validity definition; width cost of the prefix O(kT\|Z_u\|L) = n^{γ−0.633ω+h+o(1)} = o(n^{γ−ω/2}).
  - The e^{−L} hit bound from (ii), with widths ≤ 1.5n^β + log 2 + n^{β−ω/2}/4 < 2n^β.
  - Upper tail via the intrinsic bound; mean bound E q ≥ p − 3n^{−ω/5}; dip probability O(n^{−ω/5}/a_i) = o(a_*/L), which needs ω/5 > 3h.
  - Dip count via Azuma; own-key ratio with c_1 ≤ .65; cross-key ratio; R_u lower bound.
  - Union: k a_*²/L² = n^{ω/3−4h}, giving exp(−n^{ω/5}).
  - log Vol(O(r+H)) = n^{1−3.75·10⁻⁴ω+o(1)} = o(a_*n).
- **Step 4.** n-disjoint-family union exp(n[O(T log n) − n^{ω/5}]) against exp(O(n)) roles × levels. O(n²T) = o(λ) marks. Two consecutive levels (distance-2 neighbours, Lemma 3.8(i)). Crowd bound 2n^b < T. Validity of the actual set by maximality. Cap Np_u ≤ e^{O(n^γ)}.
- **Step 5.**
  - E and its recomputation under z.
  - Q independent of z.
  - p_u ≤ (R^-/R)·#terms·Q_u, with c ∈ D_u on E and g(v) ∈ Z_u.
  - Cost exp((n−m)k(log 2 − c_1a_*) + mkL + O(nT log n)), with T log n = o(ka_*) and mL = o(a_*n) because γ + 13ω + 2h < 1.
  - Posterior density e^{(log 2 − c_2a_*/2)kn} (prior width 1.5n^β = o(a_*n) because β < 1 − h).
  - Deterministic consequence \|S\| ≥ Ne^{−(log 2 − c_2a_*/2)n} ≥ C_n e^{c_2a_*n/2} ≥ 1.
- **Step 6.** Players, w_c = (λ/V)(3/λ) at level 0 and (λ/V)e^{−n^{c_3}} above. Σ_c w_c ≤ 3 + Hλe^{−n^{c_3}}. Separation for both player types; Kakutani hypotheses.
- **Step 7.**
  - Odd loads: Lemma 3.6 with L = e^{O(n^γ)}, f = e^{−n log 2+o(a_*n)}, d_u ≤ 2Nν; union over ≤ n2^n labels; \|B\|/N = 1/(2C_n).
  - Lemma 3.9 hypotheses; injection comparison.
  - Predictive threshold: Σ_{y∈D_c}M_c ≤ ε, using that z ∼ π is independent of the rest and D_c does not depend on z; ε = e^{−c_2a_*kn/4} against exp(O(n)) pairs, with a_*kn = n^{1+ω/3−h}.
  - Even loads: 1_{S_good} ≤ 1_{S_pre} order of operations; factorization in the raw experiment; cap times near fraction = o(1).
  - Hall; colors; disjoint sides.

### §5 (Lemma 5.1) — verified line by line
- **§5.1.**
  - H has density ≥ χ²/2 and V_0/A_w atoms are O(1)/N (requires \|Y\| ≥ χN, given).
  - Segment density (2/χ²)(.9)^{−q_0} ≤ e^{q_0/3}; R[u] marginals ≤ K_0′/N and joint density ≤ e^{un^γ}.
  - Bins: probability ≤ 2n^{−.04}, O(n^{.04}) endpoints; Pr(boundary) ≤ n^{−.05}; Pr(j ≥ h) ≤ (O(n^{α−.15}))^h ≤ n^{−.13h}.
  - Coverage of all neighbour keys by S (coarse / F-sign / j±1 / residual cases; the J+1 high replacement; the optional key) and w ∈ C_i.
- **§5.2 Step 1.** Prefix-deletion test (likelihood ≤ e^{a_0u}, small-denominator set of mass ≤ e^{−δu}) and the cap N max π_ℓ ≤ e^{K′b_j} at interior and boundary keys.
- **§5.2 Step 2.** G_K is sign-free and true-block gated. Ratio tests have raw probability ≤ threshold, via ∫m_{S−ℓ} ≤ 1. dP_K/dP_{K,−ℓ} ≤ e^{(a_1+δ)us_ℓ} and dP_K/dR[u] ≤ A_K^u. Support enforces adjacency. Optional-hit mass ≥ e^{−(a_1+δ)u_*}, and pools of size m^{K_hη}k_*/u_* suffice.
- **§5.3.**
  - State embedding into Q_d with d = (1+o(1))n; one-hot distance ≤ 4 per flip, so D = 8; all low neighbours of a high even state form one state (merging 5.5/6.5).
  - Step 3 low: P ≤ e^{(a_2+δ)k_c}Q_c ≤ e^{a_3k_c}Q_c; selection multiplier e^{δk′_j} with k′_j ≤ k_c; cap D_L = m^{.15} ≥ (T+j)·max k_l·O(1) = m^{.1+o(1)}.
  - Step 3 high: log(N^s max P) ≤ K_0sJ log m (TM_* = m^{.031} = o(J)).
  - High-row law 𝓡:
    - negative-part exponential moment ≤ 2;
    - chain rule giving the average E^c ≤ a_3 + o(1), using unsmoothed logs for the negative parts and Q̃ ≥ (1−ε)Q;
    - Azuma for D^ξ_h;
    - grid count exp(O_{ε_g}(r_ref)) with r_ref = O(T+J) = o(s);
    - restriction mass β; set 𝔉; separation;
    - bounds R ≤ 2e^{D_H}/(sN) and E_R[cost] ≤ a_4k_c.
- **§5.4.** Stage structure; Markov alarms; the sign-translation and bin symmetry that avoids a 2^m union (π_ℓ is a function of (i, j) only); local-lemma hypotheses (Obj. 7); pretrim multipliers against exponents (Obj. 4); K_1/K_2/K_s pattern unions.
- **Prior-heavy bound.** 2^{k_c}A_K^{k_c}(q_0K_0′/B_K)^{υ_0k_c/q_0}; rarity sums E_vB_K e^{O(k_*1_{j>J})} = O(1) and Pr(j > J)e^{D_H} = o(1).
- **§5.5.**
  - Singleton removals and binomial tails.
  - n-disjoint-failure bound exp(−Ω(nk′_j)), summable over e^{O(n)} stars since k′_j → ∞.
  - Every actual mapping passes Step 3, by maximality.
  - Selection correction: P_y(presentation, O ∈ do) = F_y a_y Q_𝔡(do); adjusted posterior ≤ ε^{−1}P; cancellation E[p^{pr}1_adj] ≤ π_ℓ(x) by disjoint presentation events; fallback ≤ ε·#records·π_ℓ(x) with #records < ε^{−1}.
  - Long/short mismatch: O(n)·o(e^{−2m^{1/5}})·e^{D_L} = o(1), since .15 < .2.
  - Three-level odd column sums:
    - bin level: same-bin repeat n(2n^{−.04})^{300}n^{.02} → 0; boundary/j ≥ 1 rarity; Step-1 caps ≤ .02(j+1) log n;
    - low-key level: near fraction 2^{−m+o(m)};
    - center level: residual-ball rarity × ne^{D_L} → 0;
    - \|B\|/N → 0.
- **§5.6.**
  - Predicate concentration exponent n^{1−.09α+o(1)} and clock-lemma interface.
  - Q independent of z. F_z ≤ e^{a_6kn}Q, covering low same-mode, high same-mode and opposite-mode neighbours, with O(mn^{.3}) = o(n^{.4}) and O(D_L + D_H) each.
  - Gated posterior exception e^{−δkn} against exp(O(n)+O(k_*)).
  - Posterior density e^{τ0kn}, with prior (A_Ke^{n^γ})^k = e^{o(kn)}.
  - H_1 mass bound 2^ke^{τ0kn−υ_1kτ1n}; μ̄ restriction mass ≥ 1 − υ_0 − υ_1 − o(1); cap O(e^{τ1n}); support on common neighbours, checked case by case across all four low/high pairings.
  - Even comparison mean via cancellation and the forced-centre height bound: d_v = O(B_K e^{O(k_*)}).
  - Even scattered moments: repeat term needs τ1 < log 2 − H_bin(2ρ).
  - \|A\|/N → 0; Hall.

### Skimmed (not verified line by line)
1. The exact observation-record and abstract-pattern counts, p. 38 last paragraph – p. 39 first half (Obj. 6). Only checked to order of magnitude against slack that is at least polynomial in m.
2. "Local validity under replacement" (pp. 45–46): the claim that long and short truncations "really use the same eligible sets and that unconsulted keys remain unobserved". I accepted the design statement and checked only the displayed mismatch estimate.
3. p. 41: "integrating against the gated data subdensity and adding the earlier denominator exceptions gives the same form of bound for each mapping". Accepted.
4. The parity-bookkeeping paragraph for merged counts (p. 38: "A state determines parity despite the merged counts …"). Read, plausible, not re-derived symbol by symbol.
5. All §3 tool proofs (Lemmas 3.3, 3.5, 3.6, 3.7, 3.8, 3.9, 3.10). Used only through their statements; the §3 seat is responsible.

---

## Part E — Direct answers to the brief's items (a)–(g)

- **(a)** Parameter chain re-derived (Part C).
  - **(i) used:** at Step 1 only (P_0 ≥ ½ + a_*, availability).
  - **(ii) used:** at Step 3 only (the hit fraction q ≥ e^{−L} except with probability exp(−n^{β−ω/2}/4)).
  - **Conclusion:** a G-cube at every large n of the subsequence.
  - **Atom bound:** N max p_v ≤ e^{(log 2 − (c_2/2)n^{−h})n}, matching Table 1.
  - **C_n → ∞ (no rate) enters at:** odd column sums 1/(2C_n)·O(1) ≤ 1/10, and even column sums ≤ 1.
  - **N ≥ 2^n enters at:** the Lemma 3.9 atom/query hypotheses and \|S\| ≥ 1.
  - **N ≤ n2^n enters at:** the Markov + label-union steps (Step 7) and the Step 2 assignment union (where even a much larger N would be tolerated).
  - **No rate of C_n is used anywhere in §4.**
- **(b)** Lemma 3.7 in §4: yes, the selection event is recomputed. p. 31: "Selection, validity, and all other local rules in this formula are recomputed for each replacement of z." E is a function of the preparatory data only (positions, activations, ties, masks, tuples including z). Q is built with W_{c,g(v)} deleted and without requiring selection or tests. The predictive-failure bound uses only that z ∼ π independently of the rest and that D_c is z-free. Correct.
- **(c)** Lemma 5.1: see Part D. The final Hall step is correct:
  - odd labels are injective (clock lemma);
  - even rows are probabilities supported on ∩_b N(y_b), because every posterior tuple coordinate is adjacent to every neighbour label in all four low/high pairings;
  - column sums are ≤ O(1)/(2C_n) ≤ 1.
- **(d)** Re-derived; see Obj. 8 for the precise role of τ1.
- **(e)** Every "the same / similarly / likewise / analogous" in pp. 26–50 was checked:
  - p. 28 "The same bound holds on the odd side" ✓
  - p. 30 "The same bound on all entries gives the lower bound for R_u(D)" ✓
  - p. 32 "this player can likewise choose a mask" ✓
  - p. 33 "With the same near fraction as above" ✓
  - p. 37 "the same small-denominator estimate give the asserted cap" ✓
  - p. 37 "gives the analogous test m_{S+ℓ}/m_S ≥ e^{−δu∗}, with the same probability bound" ✓
  - p. 40 "This is the subdensity calculation of Step 2, now using ∫M_{−c} ≤ 1" ✓
  - p. 40 "The same argument against uniform measure gives …[log(NP_h)]_+/D_H ≤ K_0/K_D + o(1)" ✓ (negative-part moment ≤ 1 + Σ_y√(P_h(y)/N) ≤ 2 by Cauchy–Schwarz)
  - p. 41 "gives the same form of bound for each mapping" — skimmed (Part D item 3)
  - p. 43 "Likewise translating all signs does not change a raw failure probability" ✓
  - p. 48 "The additive comparison above gives the same conclusion for the long means" ✓
- **(f)** Part B.
- **(g)** Part C. No constant depends on n, the subsequence (beyond the fixed κ), the witness, or the removed sets, except per-patch quantities that enter only through uniform bounds. No cycles.

---

## Verdict for scope
- **§4, Lemma 4.1: HOLDS AS READ** (verified line by line). Only UNCLEAR/COSMETIC objections (Obj. 1–3, 5).
- **§5, Lemma 5.1: HOLDS AS READ** for the full chain of displayed estimates, including the gated posterior with selection recomputed, the selection-corrected low rows, the common high-row law, the posterior density e^{τ0kn}, the cap O(e^{τ1n}), the column sums, and Hall.
- **COULD NOT CHECK** line by line: the exact record and pattern counts (pp. 38–39, 42–44), and the long/short "local validity under replacement" design claims (pp. 45–46). Both are protected by large slack; I found no inconsistency.
- One exposition gap with a true statement (Obj. 4). No mathematical gap found.
