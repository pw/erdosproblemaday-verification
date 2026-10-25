# Referee report — tag `deduction`
Scope: Section 2 (PDF pp. 5–10): Def. 2.1–2.2, Principle 2.3 and 2.4 *as stated*, Lemma 2.5 + proof, §2.5 deduction of Thm 1.1 (incl. separation (1.1)), Cor. 1.2, Cor. 2.6; parameter order asserted in Fig. 1 / §1.2.
Sources read: paper.pdf pp. 1–11 rendered (formulas checked on the page images, not only the text extraction); §5.1 (5.1), §5.4 proof of Principle 2.3, Lemma 5.4, §8 opening, Lemma 8.1, §8.2 (8.9)–(8.10), §8.5 + proof of Principle 2.4 (read only to confirm the quantifiers Section 2 relies on, not to verify them).
Primary sources fetched: Alweiss arXiv:2307.08901 (abs page + v6 PDF + v5 PDF) in /tmp/oaimath/refs/2307.08901/; Sanders arXiv:1712.03620v1 in /tmp/oaimath/refs/1712.03620/. Hindman 1974 (JCTA) not fetchable (ScienceDirect returns HTML).
Scratch checks: /tmp/oaimath/scripts_deduction/check.py (index combinatorics only; see §D).

**Bottom line for this scope: I did not find the failing sentence in Section 2.** The deduction of Theorem 1.1 from Principles 2.3 and 2.4, exactly as those principles are worded, is valid; the parameter graph is acyclic; Lemma 2.5, Cor. 1.2 and Cor. 2.6 are correct. Everything that could still be wrong lives inside the two principles, i.e. in Sections 3–8, which I did not verify. Below: what I checked and how, then the only objections I can sustain (all COSMETIC/UNCLEAR), then the citation table.

---

## A. Dependency graph (item a) — verified, no cycle

Quantifier structure, quoted:

- Principle 2.3: "For every m ≥ 2 there is an integer s = s(m) with the following property. Given n, r, χ, finite lists satisfying (2.6), and tolerances 0 < τ < 1/4, η > 0, there are admissible parameters and step-at-most-s models such that the following conclusions hold along the fixed ultrafilter U in w."
  Form: ∀m ∃s ∀(n,r,χ,𝓑,𝓐,τ,η) ∃(admissible family, models). The output may depend on everything before it, χ and the lists included. The text after the principle repeats this: "The step bound depends only on the requested chain length m. The complexity bound may depend on all the fixed data and tolerances."
- Principle 2.4: "For every n, r, s there are finite lists 𝓑, 𝓐 satisfying (2.6) and a constant δ > 0, depending only on n, r, s, such that the following holds. For any admissible family, any system of step-at-most-s models, and any fixed τ > 0, define A_w … Then lim inf_{w→∞} P(A_w) ≥ δ. In particular, δ is independent of τ and of the model complexity bound."
  Form: ∀(n,r,s) ∃(𝓑,𝓐,δ) ∀(admissible family, step-≤s system, τ). This is uniform over every admissible family (Def. 2.1 for that n) and every step-≤s system relative to that 𝓐 (Def. 2.2). A_w does not involve χ at all. δ comes before τ and before any model.
- Order in §2.5 (p. 9): m → s = s(m) (Pr. 2.3) → n = n(m,r) (Lemma 2.5; depends only on m, r) → (𝓑 ⊂ ℚⁿ_{>0}, 𝓐, δ) = Pr. 2.4(n,r,s) → C = #(B,a,c), K = #(b, chain, c) (functions of n, m, r, |𝓐|, |𝓑|) → τ, then η via (2.14) → Pr. 2.3(n,r,χ,𝓑,𝓐,τ,η) → admissible family and models of step ≤ s(m) → Pr. 2.4's universal quantifier instantiated on that output with the same τ.
  - n is fixed before 𝓑 ⊂ ℚⁿ is chosen. (2.6) "b_B ∈ 𝓐 for all b ∈ 𝓑 and all blocks B" is a constraint on Alignment's own output, and Alignment receives n. Consistent.
  - The s that Prediction delivers is the same s that Alignment was called with. The models are indexed by the 𝓐 that Alignment chose (Def. 2.2 "Fix finite sets 𝓐 ⊂ ℚ_{>0} and [r], and an admissible family"). A_w uses S_{B,b_B,c}, which is legal by (2.6).
  - The only edge that could close a cycle is s depending on 𝓑, 𝓐, δ, τ or η. Pr. 2.3 says it does not. Its proof fixes s by (5.1): "Choose an integer s ≥ 3 such that s + 1 ≥ 2(2^d) − 1 for every cube order d occurring in Proposition 4.5. The order bound in that Proposition makes this a choice depending only on m." I did not verify Prop. 4.5's order bound (outside scope).
- Fig. 1 caption: "Alignment fixes a positive mass before Prediction fixes model complexity". §1.2 says Alignment's "success probability is bounded below independently of the complexity of the nilsequence models. This uniformity permits the final choice of small calibration errors." Both match the order above.
- §8.5 closes with "The lists and δ depend only on n, r, s, whereas the rate of convergence may depend on the fixed threshold and model family. These are exactly the quantifiers of Principle 2.4." δ is defined in (8.26) as ∏ 1/(3Q_iV_i) from Lemma 8.1 budgets "before the choice of admissible parameters, models, and τ". That is consistent with the statement. I did not verify the proof.

## B. Arithmetic of §2.5 (items b, c, h) — verified line by line

1. "The union bound and (2.7) give lim_U P(G_w^c) ≤ C(3τ+η) < δ/2". This uses (2.14): 3Cτ < δ/4 and Cη < δ/4, so the sum is < δ/2. Ultrafilter limits are additive on bounded sequences. ✓
2. (2.15): P(A∩G) ≥ P(A) − P(G^c). For nonprincipal U, lim_U a_w ≥ lim inf a_w. So lim_U P(A∩G) ≥ δ − lim_U P(G^c) > δ/2 (the paper writes ≥, which is weaker and still correct). ✓
3. Witness logic on A_w ∩ G_w, for w large:
   - x_i = h_i b_i t_i ∈ ℕ (Def. 2.1(1): h_i is a multiple of W^w, which absorbs the fixed denominators of b_i).
   - Lemma 2.5 gives a chain and a colour c with χ(∏_{k∈J} x_{B_k}) = c for all J ≠ ∅. Since ∏_{k∈J} c_k z_k(t) = ∏_{k∈J} h_{B_k} b_{B_k} t_{B_k} = x_{∪B_k}, this gives U(z(t)) = 1.
   - Singleton masks give χ(h_{B_d} b_{B_d} t_{B_d}) = c with b_{B_d} ∈ 𝓐. So G_w (no calibration failure at (B_d, b_{B_d}, c)) forces S_d(t_{B_d}) > 2τ.
   - For |J| ≥ 2 with d = max J, D := {B_k : k ∈ J∖{d}} ⊆ E_{B_d}. Then L_J(z(t)) = t_{B_d} + Σ_{A∈D} (h_A b_A/(h_{B_d} b_{B_d})) t_A, which is exactly the argument in (2.12) with B = B_d. The chain c is admissible because A_w quantifies over every colour.
   - So each of the q = 2^m − m − 1 factors is > τ, the product is > τ^q ≥ τ^{2^m} (since 0 < τ < 1 and q < 2^m), and the model integrand of that triple is > τ^{2^m}. ✓
4. Summing over the K triples handles the fact that the chain, b and c depend on the sample t. All model integrands are ≥ 0 (U ∈ {0,1}, S ∈ [0,1]). So Σ_triples E_t g ≥ τ^{2^m} P(A_w ∩ G_w) for all large w, and lim_U ≥ δτ^{2^m}/2. ✓
5. (2.16): lim_U Σ I ≥ lim_U Σ E g − Σ lim_U |I − E g| ≥ δτ^{2^m}/2 − Kη > δτ^{2^m}/2 − δτ^{2^m}/4 = δτ^{2^m}/4 > 0. The inequality directions are right, and the 1/2 vs 1/4 bookkeeping is right. ✓ (See Obj. 1 on the boundedness of I.)
6. Positivity ⇒ configuration (item c):
   - I is a finite average: μ_i is supported on [X_i, X_i²), and ν_B is an expectation over finitely supported tail laws.
   - All factors are ≥ 0: ν_B(y) = E σ 1_{σ|y} ≥ 0, f ∈ {0,1}, U ∈ {0,1}. A positive product therefore forces U(z) = 1 and f_{d(J)}(L_J(z)) = 1 for every |J| ≥ 2.
   - For large w the coefficients c_k/c_d (k < d) are positive integers and z_k ∈ ℕ, so L_J(z) ∈ ℕ. The zero extension of f off ℕ can therefore only kill terms, never create them.
   - f_{d(J)}(L_J(z)) = 1 means χ(c_{d(J)} L_J(z)) = χ(Σ_{k∈J} a_k) = c, with c_d ∈ ℕ for large w.
   - "The extra divisor factors cannot create a false positive" is correct.
7. Integrality (item d).
   - Def. 2.1(1): "For every A ∈ E_B, the ratio h_A/h_B is an integer multiple of W^w." For a chain and k < d: B_k = T_k ∪ {i_k} with T_k < T_d (by (2.2)), T_d < i_k (all tails precede all pivots), and i_k < i_d. So B_k ∈ E_{B_d} = {P ∪ {j} : ∅ ≠ P < T_d < j < i_d}.
   - Fixed rationals have bounded denominator primes and valuations, so W^w absorbs them once w ≥ max(prime, valuation). Hence h_{B_k} b_{B_k}/(h_{B_d} b_{B_d}) ∈ ℕ eventually, and so are c_d and every colour argument.
   - Checked mechanically on 2,000 random chains: 0 violations of B_k ∈ E_{B_d}. Negative control: Alweiss-style anti-ordered tails give 2,396 violations out of 2,396.
8. Separation (1.1) (p. 9–10):
   - c_d ≤ C_0 M (Def. 2.1(1): h_B ≤ M; C_0 = max b_B). z_d ∈ [X_{i_d}, X_{i_d}²) gives a_d < C_0 M X_{i_d}², and a_e ≥ X_{i_e} because c_e ≥ 1.
   - For d < e: M ≤ V_e and X_{i_d} ≤ ∏_{j<i_e} X_j ≤ V_e, so a_d < C_0 V_e³. Then Σ + ∏ ≤ (m−1)C_0V_e³ + C_0^{m−1}V_e^{3(m−1)} ≤ C_1 V_e^{3m}.
   - Def. 2.1(2) says H_{i_e} dominates powers of V_e (it is literally 2 + M + ∏_{ℓ<i_e} X_ℓ) and log X_{i_e} dominates powers of H_{i_e}. So X_{i_e} > R C_1^D V_e^{3mD} eventually, uniformly over the finitely many chains.
   - a_1 ≥ X_{i_1} ≥ exp(H_{i_1}) → ∞, because H_i ≥ M ≥ W^w.
   - Finally, choose w in (U-set of (2.16)) ∩ (a cofinite set). That is two sets, so the intersection is nonempty. ✓
9. Item b, the specific question: q = 2^m − m − 1 ≤ 2^m and τ < 1, so τ^q ≥ τ^{2^m}. Kη < δτ^{2^m}/4 suffices. ✓
10. Item h: exactly as the paper says. ✓
11. Definition 2.1 is satisfiable, so Pr. 2.4 is not vacuous. Take h_i = W^{w·2^{n−i}} and M = W^{w·2^n}. The exponent gap e_P + e_j − e_T − e_i is ≥ 5 (in units of w) over all P < T < j < i for n = 7, and max h_B ≤ W^{w(2^n−1)} ≤ M (script, §D). With H_i and X_i chosen by the domination rules, every condition of Def. 2.1 holds.

## C. Lemma 2.5 (item e) — verified line by line

- Finite sums, finite form: "every coloring of [F] with r colors contains positive integers u_1,…,u_m whose nonempty subset sums all lie in [F] and have one color". This is exactly Sanders Thm 2 (sums lie in A_ℓ ⊆ S = [J(t,n)]; "not necessarily distinct"). The König/compactness derivation from Hindman's theorem is correct as written: badness is closed under restriction, and an infinite branch gives a colouring of ℕ in which any FS-configuration lies in some [F'], a contradiction.
- Ramsey by cardinality: n_0 = 2F. Set N_{n_0} = n_0 and N_{q−1} = R^{(q)}(N_q; r) backwards, with n = N_0. Pass successively to homogeneous sets for sizes 1, …, n_0. A subset of the final n_0-set has size ≤ n_0, so all of them are covered. This is Sanders' Lemma 1 with k = r = n_0, which the paper paraphrases without citing (Obj. 3). ✓
- κ(2a) is defined because 2a ≤ 2F = n_0. Σ_d u_d is itself a nonempty subset sum, so it lies in [F], which gives Σ q_d = 2Σ u_d ≤ n_0. Also q_d = 2u_d ≥ 2, so each tail has size q_d − 1 ≥ 1 and is nonempty. ✓
- Taking consecutive tail groups and then m pivots realises (2.2) using Σ q_d indices. Blocks are disjoint, so ∏_{d∈J} x_{B_d} = x_{∪_{d∈J} B_d} with |∪| = Σ_{d∈J} q_d = 2Σ_{d∈J} u_d. Its colour is κ(2Σ_J u_d), which is the common FS-colour. ✓
- x_i need not be distinct; the Ramsey argument runs on index sets. ✓

## D. Corollaries (item g) — verified line by line

- Cor. 1.2 (R = 2, D = 1): a_1 > 2 and a_d > 2(Σ_{k<d} a_k + ∏_{k<d} a_k).
  - Sums: cancel, then the top index beats the whole other side. Products: cancel, then the top factor beats the product of all smaller ones, and an empty side equals 1 < every remaining factor.
  - Sum vs product with different top index: the larger top index wins. With the same top index j: the sum lies in [a_j, a_j + Σ_{k<j} a_k) ⊂ [a_j, 2a_j), because Σ_{k<j} a_k < a_j/2. A nonsingleton product is ≥ 2a_j (the other factor is ≥ 3). A singleton product equals a sum only for S = {j}.
  - Counts: |FS| = |FP| = 2^m − 1, |FS ∪ FP| = 2(2^m − 1) − m. ✓
  - The same holds for any R ≥ 2, D ≥ 1, since Σ + ∏ ≥ 1, which is what the "distinctness properties" sentence of Cor. 2.6 uses.
- Cor. 2.6:
  - Refine χ by the residue mod q, giving rq colours, and take max(m,2) elements. Then a_1 ≡ a_2 ≡ a_1 + a_2 ≡ v, so 2v ≡ v and v ≡ 0 (mod q). ✓
  - The first m elements inherit (1.1) (a prefix condition) and monochromaticity (FS/FP of a subset). ✓
  - The compactness tree is closed under restriction, and König applies. ✓

## E. Comparison with Alweiss (item f)

- Current arXiv version: **v6, submitted Sun 12 Jul 2026 03:14 UTC** (the PDF title page reads "July 14, 2026"; comment "v6, accepted in Duke Math Journal"). This is the version the paper cites. v1–v5 are 2023; v5 (17 Nov 2023) was also downloaded.
- Thm 1.3 (v6, verbatim): "For any n ≥ 2, if ℚ is colored in finitely many colors, we can find some x_1, ⋯, x_n ≠ 0 such that all the numbers Σ_{i∈S} x_i and ∏_{i∈S} x_i, for nonempty S ⊂ [n] are the same color." Calling this "the full finite sums and products theorem over ℚ" is fair. Note the x_i are only required to be nonzero; distinctness is not part of the statement (Alweiss remarks x_n ≫ ⋯ ≫ x_1 can be arranged).
- §5 Steps II–IV:
  - Step II: "By Ramsey's theorem, we can pass to a subset of the x_i so that the color of x_{i1}x_{i2}⋯x_{ik} depends only on k". This is Lemma 2.5's Ramsey-by-cardinality.
  - Step III: Folkman on the degree colouring. This is Lemma 2.5's finite-sums step.
  - Step IV: "pick (possibly empty) sets S_i of size a_r − 1 [sic; a_i − 1 intended] … so that S_{i+1} > S_i and {N/2} > S_r … X_i = x_{N−i} ∏_{j∈S_i} x_j." The pivot index N−i *decreases* as the tail S_i *increases*, so tails and pivots are anti-ordered. The paper co-orders them (T_1 < ⋯ < T_m < i_1 < ⋯ < i_m) and doubles sizes (q_d = 2u_d) to force nonempty tails.
  - My script confirms the anti-ordered Alweiss arrangement violates (2.1) in every pair. The paper's phrase "the ordered tails and pivots are chosen to match the additive shifts in (2.1)" acknowledges the adaptation. So "follows … [1, Section 5, Steps II–IV]" is accurate as a description of borrowed ideas, with Step IV modified.
- §4 compensating scalings (v6 p. 11, verbatim): "perform the shift x_n ← x_n + Σ u_{S,T} … and then the scaling operations x_j ← x_j k^{y_j} for j < n. Lastly, performing the scaling operation x_n ← x_n / k^{Σ_{j∈T′} y_j}." and "For T_1 ∈ T that have been previously M-handled … the terms … will still be handled after these operations". This matches the paper's "compensating scale updates in [1, Section 4], which fix the current target product while retaining the requirements secured at earlier targets", and §8.1 (8.1)–(8.2).
- Context worth recording: Alweiss v6 §6 names the exact obstruction over ℕ: "we cannot simply 'shift' ac by b; this is because b generally will not be divisible by c". The paper's ordering puts the added tail P *below* the anchor tail T, so the added block product is not a multiple of t_T. That obstruction is therefore not removed by the Section 2 combinatorics. It is pushed into Alignment (§8.2: "an integer displacement q need not be divisible by t … choose an integer ρ with tρ ≡ q (mod M)"). Section 2 is correct *because* it delegates this. Whether §8 overcomes it is not checked here.

---

## Objections

**1. §2.3 (2.11) and §2.5 (2.16), p. 7 and p. 9 — COSMETIC.**
Quoted: (2.11) "lim_U |I_{b,c,𝐁} − E_t U(z(t)) ∏ S_{d(J)}(L_J(z(t)))| ≤ η" and "It follows from (2.11) and (2.14) that lim_U Σ I_{b,c,𝐁} > 0." versus p. 6: "Every bounded real sequence has such a limit".
Problem: I_{b,c,𝐁} contains unbounded divisor weights ν_B(y) = E σ1_{σ|y} (pointwise up to the tail product). No bound on I uniform in w is stated in Section 2, so lim_U is applied outside the class the paper declared.
Harmless, for two reasons. All terms are ≥ 0, so lim_U exists in [0, ∞] and is additive there. And (2.11) itself, if true, forces |I| ≤ 1 + η + ε on a U-set.
Fix: one sentence ("limits of nonnegative sequences taken in [0,∞]").

**2. Def. 2.1 remark, (2.7), (2.12), (2.10), p. 6–7 — COSMETIC.**
Quoted: "every color argument used below is eventually a positive integer."
Problem: for the finitely many small w where h_B a ∉ ℕ or h_A b_A/(h_B b_B) ∉ ℕ, the probabilities in (2.7), the event A_w and the count I are undefined. Only lim_U (nonprincipal) and lim inf are ever used, so they are insensitive to finitely many w.
Fix: define them arbitrarily for those w.

**3. Lemma 2.5 proof, p. 8 — COSMETIC.**
Quoted: "Repeated finite Ramsey gives an n such that every coloring of the nonempty index subsets of [n] has an n_0-element subset on which the color depends only on cardinality … apply the finite Ramsey theorem successively to the subset sizes 1, …, n_0, choosing the successive ambient bounds backward."
The proof is correct but given only in prose. It is precisely Sanders [30] Lemma 1 ("there exists a number N(k,r,t) such that if all the non-empty subsets of a set S of order n ≥ N(k,r,t) are divided into t classes … all the j-subsets of K are contained in A_{i_j} for j = 1,…,r") with k = r = n_0. The paper cites [30] only for the finite sums theorem.
Fix: cite it.

**4. §1.1 / §2.4 attribution to Alweiss [1, §5 Steps II–IV], p. 3 and p. 8 — COSMETIC.**
Quoted: "The ordered-block selection in our proof follows the Ramsey and finite-sums argument in [1, Section 5]."
Alweiss's Step IV anti-orders tails and pivots and allows empty tails (see §E). The paper's chain (2.2) reverses the tail order and forces |T_d| ≥ 1. This change is necessary for B_k ∈ E_{B_d} (my control: the Alweiss ordering fails 100% of pairs). The paper's own clause "the ordered tails and pivots are chosen to match the additive shifts in (2.1)" discloses this, so it is not a misattribution.
Fix: say "adapts" rather than "follows".

**5. Notation, pp. 2–10 — COSMETIC.**
D is both the exponent in (1.1) and the subset D ⊆ E_B in (2.12). q is used for 2^m − m − 1 (§2.5), for the block sizes q_d (Lemma 2.5), and for the modulus (Cor. 2.6). C is both the calibration count and, in §8, the tail C. No ambiguity affects any step I checked.

**6. Principle 2.4 and Principle 2.3 as stated — UNCLEAR (scope boundary, not a defect of Section 2).**
The deduction is valid only because of three uniformity assertions, which Section 2 states but does not prove.
- (i) Pr. 2.3: "s = s(m)", proved via (5.1) from Prop. 4.5's order bound. If s had to depend on 𝓑, 𝓐 or n-dependent block sizes, the order s → 𝓑 → s would be a cycle.
- (ii) Pr. 2.4: δ "independent of τ and of the model complexity bound". Def. 2.2's "bounded complexity" is only per-system ("its nilmanifolds belong to a fixed finite list"). So Pr. 2.4 asserts a lower bound uniform over nilmanifolds of *every* dimension and over every Lipschitz constant. §8.1 obtains it by compactness over colourings of the free step-s nilpotent group on finitely many generators, using [37, Cor. 3.7].
- (iii) Pr. 2.4 holds "for any … system of step-at-most-s models". Def. 2.2 lets a model be an *arbitrary* function of y mod M: a constant nilsequence on each residue class is a step-0 piece of complexity O(1). Def. 2.1 does not force M | h_A/h_B. For example, h_i = W^{w2^{n−i}} and M = W^{w2^n} are admissible, and then the shifts Σ (h_A b_A/(h_B b_B)) t_A move the residue class mod M. So Alignment must defeat arbitrary residue colourings mod M with M → ∞. §8.2 claims to do this by moving the raw pivot p ↦ p + r_e with t r_e ≡ q_e (mod MW^w), together with translation invariance (8.25) of μ_i. That is plausible in architecture, but whether the shifted states for different residue classes live on "one common state" is the content of §§6–7 (Prop. 7.5 / Lemma 7.7).
None of (i)–(iii) is contradicted by anything in Section 2. A referee of §§4–5 and §§6–8 must verify them; a failure of any one breaks the deduction. I have not verified them.

No FATAL and no GAP objection in scope.

---

## Citation table (scope: §1.1 attributions used in §2, §2.4)

| Cited | Paper says | Source says (quoted) | Verdict |
|---|---|---|---|
| [1] Alweiss arXiv:2307.08901, cited as v6 (12 Jul 2026) | "Alweiss proved the full finite sums and products theorem over ℚ [1, Theorem 1.3]" | v6 Thm 1.3: "For any n ≥ 2, if ℚ is colored in finitely many colors, we can find some x_1, ⋯, x_n ≠ 0 such that all the numbers Σ_{i∈S} x_i and ∏_{i∈S} x_i, for nonempty S ⊂ [n] are the same color." Current version is v6 = cited version. | MATCH (x_i only nonzero; no distinctness in the statement) |
| [1, §5 Steps II–IV] | "The following selection uses the Ramsey-by-cardinality and finite-sums argument of [1, Section 5, Steps II–IV]; the ordered tails and pivots are chosen to match the additive shifts in (2.1)." | Step II: "By Ramsey's theorem, we can pass to a subset of the x_i so that the color of x_{i1}⋯x_{ik} depends only on k". Step III: "Applying Folkman's theorem to this coloring". Step IV: "pick (possibly empty) sets S_i … so that S_{i+1} > S_i … X_i = x_{N−i}∏_{j∈S_i}x_j" | MATCH for II–III. Step IV adapted, with order reversed and tails nonempty; the adaptation is disclosed |
| [1, §4] | "compensating scale updates … which fix the current target product while retaining the requirements secured at earlier targets" | "x_n ← x_n + Σ u_{S,T}… then the scaling operations x_j ← x_j k^{y_j} for j < n … x_n ← x_n/k^{Σ_{j∈T′} y_j}"; "previously M-handled … will still be handled after these operations" | MATCH |
| [30] Sanders, arXiv:1712.03620v1 | finite form of finite sums: "[30, Theorem 2 and Corollary 1.1]" | Thm 2: "Given numbers t, n there exists a number J(t, n) such that if the set S = {1,…,J(t,n)} is divided into t classes … there exists a sequence of (not necessarily distinct) numbers a_1,…,a_n and a number ℓ … such that Σ_{i∈I} a_i ∈ A_ℓ for all I ⊆ {1,…,n}." Cor 1.1: "The a_i may be assumed distinct in the above theorem." | MATCH (Lemma 1 there is also the Ramsey-by-cardinality step, uncited) |
| [19] Hindman 1974 + [23] compactness | "it also follows from Hindman's finite sums theorem and compactness" | Not fetched (ScienceDirect returns HTML). The infinite finite-sums theorem is textbook-standard, and the compactness argument is written out in the paper and is correct. | COULD NOT FETCH (statement not in doubt) |
| [37] Zorin-Kranich Cor. 3.7; [17, 18, 34, 12, 13] | used in §§5–8 | outside this scope | NOT CHECKED (other referees) |

---

## Steps verified line by line vs skimmed

**Verified line by line, with quantifiers, inequalities and integrality redone:**
- Def. 2.1 (all three items) and the remark on rational factors. Shown satisfiable with an explicit family, exponent gaps checked by script.
- Chain property: B_k ∈ E_{B_d} for k < d (by hand and by script with a negative control).
- Statements of Pr. 2.3 and Pr. 2.4: quantifier order and what each output may depend on.
- Lemma 2.5 statement and proof: finite Ramsey bookkeeping, Σ q_d ≤ n_0, nonempty tails, index count, colour of the union.
- Finite sums finite form and its compactness proof.
- All of §2.5:
  - parameter order;
  - (2.14) → G_w bound → (2.15);
  - witness/chain/calibration logic;
  - q = 2^m − m − 1 and τ^q ≥ τ^{2^m};
  - the sum over K triples;
  - (2.16) with its constants;
  - positivity ⇒ configuration (nonnegativity of ν, f, U; integrality of L_J(z); zero extension);
  - separation (C_0, V_e, C_1, domination chain from Def. 2.1(2));
  - the final choice of w (intersection of finitely many U-sets).
- Cor. 1.2 and Cor. 2.6 in full.
- Alweiss v6 Thm 1.3, §4 and §5 against the paper's descriptions. Sanders Thm 2, Cor 1.1 and Lemma 1.

**Read for the quantifiers Section 2 relies on, not verified:**
- §5 (5.1) (s depends only on m); proof of Pr. 2.3 in §5.4 (calibration via ψ, telescoping); Lemma 5.4.
- §8 opening; Lemma 8.1 and the "uniform finite version" compactness paragraph; §8.2 (8.9)–(8.10); §8.5 (8.25)–(8.28) and the proof of Pr. 2.4.

**Not read:** §§3–4, 5.1–5.3, 6–7, 8.3–8.4.

## Verdict for scope

**HOLDS AS READ.** Theorem 1.1, Cor. 1.2 and Cor. 2.6 follow correctly from Principles 2.3 and 2.4 as stated, and the parameter graph is acyclic.

**COULD NOT CHECK** the three uniformity claims on which acyclicity and the final inequality depend (Obj. 6: s = s(m) only; δ uniform over all nilmanifold dimensions and Lipschitz constants; Alignment against arbitrary residue-mod-M model pieces). They are asserted in Section 2 and proved, if at all, in §§4–5 and §§6–8, which are outside this scope.
