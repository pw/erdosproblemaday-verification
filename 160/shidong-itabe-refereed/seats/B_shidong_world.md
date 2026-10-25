# Seat B: Shi–Dong arXiv:2607.20752v2, consequences (§6), novelty and priority

Referee seat B, 2026-10-13. Sources I read directly: the Shi–Dong v2 text and PDF (page 6 rendered so the brackets in the Cor 1.5 display could be checked), Shi–Dong v1 (arXiv, diffed against v2), DTZ arXiv:2307.06914v2, Führer arXiv:2403.18611 v1 and v2, Gowers arXiv:2004.07598, Raghavan arXiv:2603.27045v3, Itabe's manuscript plus his git repo and the GitHub release API, the erdosproblems.com pages /160, /forum/thread/160 and /forum/thread/160/proof-claims, and both proof-claim comment threads (fetched through the Hetzner box, because exe.dev gets a CF challenge). I also read teorth/erdosproblems `data/problems.yaml` and the OAI catalogue. Scripts and downloads are in `/tmp/erdos160/seats/B_work/`.

## VERDICT on §6: HOLDS AS READ

- Display (1) matches DTZ Theorem 1.8 exactly.
- Display (2) matches DTZ Proposition 2.4 combined with Theorem 2.8 exactly.
- The exponent arithmetic in Corollaries 1.4 and 1.5 is correct.
- A bound ρ_k(α) ≤ Cα^{k+δ} does refute Conjecture 1.10 as DTZ state it, with the quantifiers in their order.
- The hypothesis DTZ need (a colouring of the cyclic group Z/MZ with no symmetrically coloured k-AP for any d ≢ 0 mod M) is exactly what Theorem 1.1 provides.

I checked the k = 4 case of that hypothesis exhaustively by computer (p = 5, 7, 11, all a and all d ≠ 0 mod p⁴), with negative controls that do find violations.

One thing I could not check: the primary text of [Gow01, Conjecture 4.2]. The published GAFA version is behind a paywall. The preprint on Gowers' site (`sz898.dvi`, TeX-dated 2000-03-27) has a §4 "Two motivating examples" but no numbered conjectures, and it lacks the p. 488 "length five" sentence that DTZ quote. I therefore relied on DTZ's statement of it as their Conjecture 1.10 (DTZ is refereed: Math. Proc. Camb. Phil. Soc. 179 (2025)).

### Checks that passed (no objection)

- **(1) against DTZ Thm 1.8.** DTZ: "Suppose there exists an r-coloring of Z/NZ avoiding symmetrically colored 4-APs. Then there exists a constant C (depending on r, N), such that for all 0 < α < 1/2, ρ4(α) ≤ Cα^{3+(1/2) log_r N}." Shi–Dong (1), "ρ4(α) = O_{r,M}(α^{3+½ log_r M}) for 0 < α < 1/2", is the same statement: same exponent, same range, constant depending on (r, M).
  - I also re-derived the proof of Theorem 2.7 (r^ℓ-colouring of Z/N^ℓZ, then Lemma 4.3, Lemma 3.6 with m = O(r^{2ℓ}), Lemma 4.2, then ℓ = ½ log_r(1/α)). It gives α^3 · N^{−ℓ} = α^{3+½ log_r N}, so the statement is internally consistent.
- **(2) against DTZ Thm 2.8 + Prop 2.4.** DTZ: "For every ε > 0, there exists a constant C (depending on k, r, N, ε), such that for all 0 < α < 1, ρ̃k(α) ≤ Cα^{k−1+(log_r N)/(k−1)−ε}", together with "Proposition 2.4. ρk(α) ≤ ρ̃k(α) for all k and α." Shi–Dong (2), "O_{r,M,k,ε}(α^{k−1+(log_r M)/(k−1)−ε}) … for even k ≥ 4 and 0 < α < 1", matches in exponent, range, the role of ε, and constant dependence.
- **Corollary 1.4 arithmetic.** With r = 27p and M = p⁴: ½ log_{27p} p⁴ = 2 log p / (log p + log 27), which tends to 2 as p → ∞, so the exponent 3 + … tends to 5. To get ≥ 5 − ε, choose p ≥ 27^{(2−ε)/ε}. Sample values: e(10⁴) = 4.473, e(10⁸) = 4.697, e(10³⁰) = 4.909.
  - The old value 4.406 = 3 + ½ log₃ 22 (DTZ Cor 1.9) is quoted correctly.
- **Corollary 1.5 arithmetic.** log_r M = (k²/4) log p / ((k²/4 − 1) log(k−1) + log p). This tends to k²/4, so the exponent tends to k − 1 + k²/(4(k−1)) = k + (k−2)²/(4(k−1)).
  - Limits: k = 6 gives 6.8, k = 8 gives 9.2857, k = 10 gives 11.7778.
  - The rendered PDF display has the brackets right, with (k−1) multiplying the whole bracket. The pdftotext output loses them.
- **Does "exponent > k" contradict Conjecture 1.10?** Yes.
  - Conjecture 1.10 (∀ even k, ∀ ε ∃ η: ‖1_A − α‖_{U^{k−2}} ≤ η with α = |A|/N ⇒ Λ_k(1_A) ≥ α^k − ε) implies ρ_k(α) ≥ α^k for every α.
  - Proof of that implication. If ‖1_A − α‖_{U^{k−2}} ≤ η, then |α' − α| ≤ η, where α' = |A|/N, because U^d norms dominate |E f|. Hence ‖1_A − α'‖ ≤ 2η, and the conjecture gives Λ_k ≥ α'^k − ε/2 ≥ α^k − ε. Definition 1.11's ρ_k is a supremum that is attained (a limit of valid values is valid), so ρ_k(α) ≥ α^k.
  - Contrapositive: ρ_k(α) ≤ C_p α^{e−ε} with e − ε > k gives ρ_k(α) < α^k for all α < C_p^{−1/(e−ε−k)}. Then there are ε₀ > 0, arbitrarily large N, and U^{k−2}-close sets with Λ_k < α^k − ε₀ ≤ α'^k − ε₀/2. That falsifies Conj 1.10 for that ε₀, whatever η is. The quantifier order (ε before η) causes no problem, and the "liminf" nature of ρ_k only helps.
- **Cyclic hypothesis.** DTZ need cyclic Z/NZ: Lemma 5.1's tensor power reads the lowest differing base-N digit modulo N. Theorem 1.1 is stated for Z/p^{k²/4}Z, and Lemma 2.2 handles wrap-around at the top digit (the top digit is taken mod p, with no τ label). Nontriviality is d ≢ 0 mod M (Lemma 2.2: "if d ≠ 0 in Z/p^L Z, then h ≠ 0"). Since p > k, the k terms are distinct.
  - Exhaustive check (`B_work/scripts/check_k4_cyclic.py`), k = 4, over all a ∈ Z/p⁴Z and all d ≠ 0:
    - p = 5: **0 violations**, 125 colours used (bound 27p = 135).
    - p = 7: **0 violations**, 187 colours used (bound 189).
    - p = 11: **0 violations**, 297 colours used (bound 297).
  - Negative controls, to show the check can fail:
    - Dropping the τ label on digit 0: 168 / 890 / 15,700 violations.
    - Dropping the linear layer: 5,324 violations at p = 11. It shows 0 at p = 5 and 7, because there the thirds have at most 3 elements and τ alone blocks the step-1 progressions.
- **Prior bounds through (1)/(2) for comparison.**
  - Itabe's 9p-colouring of Z/p³Z gives 3 + 3/2 = 4.5 through (1) (see N6).
  - DTZ's Z/22 3-colouring gives 3.938, 5.563 and 7.402 through (2) for k = 4, 6, 8.

## Findings

**F1 — EXPOSITION.** Proof of Cor 1.5: *"Choosing ε < (k−2)²/(4(k−1)) makes the exponent larger than the random exponent k."*
- This is true only after p has been taken large, and the sentence does not say so. At finite p the exponent is e_k(p) − ε, and e_k(p) > k requires log p > (k−1)(k²/4 − 1) log(k−1) / ((k−2)²/4):
  - k = 4: p > 3⁹ = 19,683 (through (2)).
  - k = 6: p > 5¹⁰ ≈ 9.77·10⁶. For example e_6(7) = 5.236 and e_6(10⁶) = 5.932, both below 6.
  - k = 8: p > 7.2·10⁹.
  - k = 10: p > 7.6·10¹².
- The correct order is: fix p with e_k(p) > k, then take ε < e_k(p) − k. This is harmless, since the conjecture is qualitative, but the displayed sentence is false as written for small p.
- The counterexamples are also purely qualitative. C = C(k, r, M, ε) is unspecified, so ρ_k(α) < α^k holds only for α below an inexplicit threshold.

**F2 — EXPOSITION.** Intro: *"Gowers [Gow01, Conjecture 4.2] conjectured that ρk(α) is lower bounded by the random baseline α^k for every even k ≥ 4."*
- This paraphrases Gowers through DTZ's later Definition 1.11. Conj 1.10 ⇒ ρ_k ≥ α^k is valid (shown above), and it is the only direction the paper uses. The converse is not obvious (Conj 1.10's η is uniform in α and has no N₀).
- I could not compare the paraphrase with Gowers' own wording (see the verdict). Gowers 2020 paraphrases the k = 4 case as: *"if A is a set of density δ that is c-uniform, then the number of quadruples … is at least (δ⁴ − c′)N² … It is this conjecture that we shall disprove here."* This is consistent with DTZ's restatement at k = 4.

**F3 — EXPOSITION, about DTZ rather than Shi–Dong (so a reader isn't tripped up).** DTZ's proof of Theorem 2.8 writes *"m = (k²u)^{1/β_k+o(1)}"*, a marginal *"r^{−ℓ/β_k}"*, *"ℓ = β_k log_r(1/α)"*, and finally *"Λ̃k(1_A) ≲ α^{(k−1+log_r N)/β_k − o(1)}"*.
- Under Definition 3.4 (largest solution-free set ≥ N^{1/β_k}), the correct values are m = (k²u)^{β_k+o(1)} and ℓ = log_r(1/α)/β_k. That gives Λ̃ ≲ α^{k−1+(log_r N)/β_k − o(1)}, and β_k ≤ k−1 then yields exactly the stated exponent k − 1 + (log_r N)/(k−1) − ε. The Behrend factor e^{O(√(ℓ log N))} is absorbed in the o(1).
- So the theorem statement, which is what Shi–Dong quote as (2), is correct, and the proof's last display has β_k inverted.
- Shi–Dong could cite the statement and add one line noting that β_k ≤ k − 1 is the only input used.

**F4 — NOVELTY-NOTE: "the first counterexample … for every even k ≥ 6" holds up under everything I could check.** The claim is *"Our result provides, to the best of our knowledge, the first counterexample to this conjecture for every even k ≥ 6"*, with *"This provides the first counterexamples … for every even k ≥ 6"* in §6.
- **(a) DTZ itself** gives nothing for even k ≥ 6. Their remark after Conj 1.14, *"an application of the Lovász local lemma implies that there is an O(N^{2/k})-coloring of [N] avoiding symmetrically colored k-APs"*, has log_r M → k/2. Through (2) that gives k − 1 + k/(2(k−1)) − ε: 3.667, 5.6 and 7.571 for k = 4, 6, 8, always below k. Their explicit Z/22 colouring gives 5.563 for k = 6. DTZ also say outright: *"this conjecture has been disproved for k = 4. In light of this, it is reasonable to believe that it is false for all k ≥ 4."*
- **(b) The k = 4 colouring does not already settle k ≥ 6.** DTZ observe *"each symmetrically colored k-AP contains a symmetrically colored 4-AP"* (take the middle four terms), so any k = 4 colouring is also a symmetric-k-AP-free colouring. Through (2), Shi–Dong's own 27p-colouring of Z/p⁴Z gives k − 1 + 4/(k−1) − ε: 5.8 for k = 6 and 7.571 for k = 8. Both are below k.
  - The general criterion through (2) is a colouring with r = M^θ and θ < 1/(k−1). Shi–Dong have θ = 4/k², and 4/k² < 1/(k−1) ⟺ (k−2)² > 0. The k = 4 colouring (θ = 1/4) fails this for every k ≥ 6. So the layered general-k construction really is needed.
  - Conditional caveat: if DTZ's conjecture β_k = k/2 held at k = 6, the proof of Thm 2.8 would give k − 1 + (log_r M)/β_k ≈ 5 + 4/3 = 6.33 > 6 from the k = 4 colouring alone. But β_6 = 3 is not known; DTZ prove β_k = k/2 only for k = 4.
- **(c) Literature.**
  - Gowers 2020 (arXiv:2004.07598; Acta Math. Hungar. 161) covers only k = 4 and only Fourier uniformity ("It is this conjecture that we shall disprove here"; Theorem 6).
  - Its closing sentence, *"This question is open only for progressions of length 4: for longer progressions, Ruzsa has constructed a counterexample (see Theorem 2.4 of [1])"*, is about Ruzsa's α^C question for **Fourier-uniform** sets. That is the BHK appendix example, Fourier-uniform with few 5-APs (per DTZ). It does not meet the U^{k−2} hypothesis of Conj 4.2 for k ≥ 6, and a reader should not take it as an earlier refutation.
  - DTZ Thm 1.13 (odd k′) cannot be transferred to even k. With k′ = k − 1, the sets are only U^{k−3}-uniform, which is too weak. With k′ = k + 1, they are U^{k−1}-uniform, which forces Λ_k ≈ α^k.
  - Web and arXiv searches (Oct 2026) for U^{k−2}-uniform sets with fewer than α^k k-APs for even k ≥ 6 turned up nothing other than Shi–Dong. This is a coverage statement about my search, not proof that nothing exists.

**F5 — NOVELTY-NOTE on FT24.** The sentence at issue: *"A closely related polynomial construction appears in [FT24] for producing large line-evasive sets, where norm layers of both odd and even degrees are used."* It is accurate but understates the overlap. Shi–Dong's result is **not** a corollary of FT24.
- **What FT24 contains.**
  - v1 (Führer alone, *"More on maximal line-free sets in F_p^n"*, 27 Mar 2024) proves Theorem 1.1: P = Σ_{i=1}^{k−1} P_i, with P_i homogeneous of degree i in i variables with only the trivial zero, on F_q^{(k²−k)/2}. Its zero set has no k points on a line. The proof is exactly the descending induction "coefficient of Y^l in Q is P_l(b_l), so b_l = 0", "inspired by Lin and Wolf [Proposition 3]".
  - Theorem 1.4 of v1 gives the q-colouring by translates: no monochromatic full line.
  - v2 (Führer–Taranchuk, retitled, 10 Feb 2026) uses norms N_i for every i = 1..t on F_q^{t(t+1)/2}. It partitions into level sets of P_{t,q} that are t-line evasive (any line meets a colour class in at most t points). It adds vector-space Ramsey numbers and Turán numbers, plus a §6 Chevalley–Warning minimality remark.
  - Neither version mentions symmetric colourings, colourings of Z/NZ, digit or carry structure, or uniform sets.
- **Why it is not a corollary.**
  1. The property is different. Avoiding symmetric k-APs is stronger than avoiding monochromatic k collinear points.
  2. FT's all-layer colouring is **not** symmetric-free. Take h = (0, v₂, 0) and u₂ = −(3/2)v₂ in F_p × F_{p²} × F_{p³} (t = 3). Then Q(y₀ + th) = const + (t − 3/2)² N₂(v₂), which is symmetric about 3/2, giving a symmetrically coloured 4-AP with h ≠ 0.
  3. Shi–Dong's real algebraic idea is the parity step: symmetry forces g(t+a) to be even, so only odd layers are needed. That gives dimension k²/4 instead of k(k−1)/2, together with the carry-control lift to Z/p^L Z.
- That said, Lemma 4.1's proof is the FT/Lin–Wolf top-coefficient induction, and Shi–Dong's Remark 4.2 (Chevalley–Warning) parallels FT v2 §6.
- Citation precision: [FT24] is listed as "Führer and Taranchuk, *Large line-free sets and their applications*, 2024". The 2024 version is single-author with a different title. The layered polynomial dates from March 2024 (Führer), building on Lin–Wolf 2010.

**F6 — NOVELTY-NOTE on priority and the [Ita26] characterisation.** Shi–Dong v2 §3: *"The cubic norm construction P3 is also used in a concurrent result [Ita26] to claim an intermediate O(N^{1/3}) upper bound."* Intro: *"To the best of our knowledge, this [O(N^{log_22 3})] is the strongest previously known upper bound for this problem."*
- **Dates** (server-side timestamps where available):

  | Event | Date |
  |---|---|
  | Itabe repo created | 2026-07-14 05:19:20Z |
  | Itabe release v0.2.0-review-candidate published (GitHub API) | 2026-07-14 05:26:34Z |
  | Itabe release v0.2.1 published | 2026-07-14 06:49:39Z |
  | Itabe proof claim on erdosproblems #160 | 2026-07-15 00:32:16 |
  | Shi–Dong v1 on arXiv (no citation of Itabe or FT24) | 2026-07-22 22:06:35Z |
  | Shi–Dong proof claim | 2026-07-24 01:29 |
  | ruizshi's comment on Itabe's claim | 2026-07-24 01:38 |
  | Shi–Dong v2 adds [Ita26] and [FT24] | 2026-07-28 18:31:55Z |

  - Itabe's tag objects are dated 05:22:52Z and 06:45:08Z.
  - v0.2.0 already contains the cubic §7. The diff to v0.2.1 changes only the Definition 1.1 wording and the Lean `siteH 0` note.
- **ruizshi's own comment** (proof-claim 14 comments, 01:38, 24 Jul 2026): *"it was not until I posted our latest 1/4 result … that I realized there was already a 1/3 argument in this comment. To be honest, while developing our result, we were inspired by a 1/3 bound suggested by GPT-5.6 Sol. Therefore, I am not entirely sure whether our result may have been indirectly influenced by this comment."* Together with the acknowledgement *"The key construction idea for 4-APs was suggested during an interaction with OpenAI's GPT-5.6 Sol"*, this makes "concurrent" generous: Itabe's work was public 8 days before v1.
- **Exact relation (confirmed).** Itabe §7 colours n = r + p(w + pu) by (τ_p(r), τ_p(w), N_{F_{p³}/F_p}(ι_p(r, w, u))), with 9p colours on [0, p³). This is, up to the choice of F_p-basis, **Shi–Dong's k = 4 colouring restricted to the subgroup pZ/p⁴Z ≅ Z/p³Z** (the slice x₀ = 0): there τ(x₀) = 0 and Q = 0 + N₃(x₁, x₂, x₃).
  - So it is the "cubic layer alone" case. Note that Theorem 1.1 has no free L, so "the L = 3 case of Theorem 1.1" is only informally right.
  - Shi–Dong's additions over Itabe: the degree-1 layer plus one more digit (1/3 → 1/4), the odd-layer generalisation to all even k, the general-k carry lemma (Itabe's Lemma 7.1 is the k = 4 thirds version), and the cyclic formulation feeding DTZ.
  - Restriction to a subgroup preserves symmetric-freeness, and I checked independently that Itabe's colouring is symmetric-free on **cyclic** Z/p³Z: exhaustive, p = 5, 7, 11, 13, 17, 0 violations (`check_itabe_cyclic.py`). So through DTZ Thm 1.8 it would already have given ρ₄(α) ≤ α^{4.5−ε}. Nobody claimed this.
- **Two wording problems.**
  - Itabe's headline claim is H(N) ≤ N^{1/3+o(1)} for #160. "O(N^{1/3})" is correct only for his ABBA factor (9p with p³ < 4096N).
  - The intro's "strongest previously known upper bound" sentence was left unchanged in v2 while §3 now cites an earlier N^{1/3} claim. It should say "strongest previously known *published* bound" or mention [Ita26] there.

**F7 — NOVELTY-NOTE on the lower bound and Raghavan.**
- **Raghavan, arXiv:2603.27045.** "Improved Bounds for 3-Progressions", math.NT, single author (UCLA). Three versions: v1 27 Mar 2026, v2 1 May 2026, v3 15 May 2026 ("Revised to fix a couple of typos"). No journal-ref or DOI on arXiv and none found by search; treat it as an unrefereed preprint.
- **Main theorem (Thm 1.4):** *"|A| ≤ exp(−log(N)^{1/6−o(1)})N. More specifically, |A| ≤ exp(−Ω(log(N)^{1/6} log log(N)^{−1/6}))N."*
  - Internal inconsistency: the abstract states the weaker *"exp(−c log(N)^{1/6} log log(N)^{−1})N"*.
  - The final step of the proof ("N ≤ exp(O(L(α)⁶ log L(α)))") gives the Thm 1.4 form, so the abstract is merely weaker.
- **The reduction holds.** If x, x+d, x+2d ⊂ [N/4, 3N/4] are monochromatic (d > 0), then 2d ≤ N/2, so x + 3d ≤ 3N/4 + N/4 = N. The 4-AP (x, …, x+3d) therefore lies in [N] and has three equal colours, contradicting goodness.
  - So each colour class meets that interval in a 3-AP-free set, and h(N) ≥ (N/2)/r₃(N/2) ≫ exp(c (log N)^{1/6} (log log N)^{−1/6}).
- **The forum comment** (ruizshi, 15:45, 4 Aug 2026) actually says *"h(N) ≫ exp(c(log N)^{1/6−o(1)})"*. That is correct given Thm 1.4, and also holds in the /log log N form.
- **Context.** The page still records exp(c(log N)^{1/9}) from Bloom–Sisask arXiv:2309.02353 (a single v1, no journal-ref on arXiv). The OAI catalogue's result 159 (quasipolynomial r_k bounds for all k ≥ 3, unrefereed, Sept 2026) is tangential. It would improve DTZ's monochromatic-k-AP colour lower bound Ω(exp((log log N)^{c_k})) to exp(c(log N)^{ε_k}) if correct, but it does not beat the 3-AP route for #160.

**F8 — NOVELTY-NOTE on database status.**
- **teorth/erdosproblems** `data/problems.yaml` (repo HEAD 0ac519b6, 2026-10-13): #160 has `status: open`, `last_update: 2025-08-31`, `formalized: yes`, `formal_status: unformalized`. Neither 2026 claim is reflected.
- **erdosproblems.com/160** (fetched 2026-10-13):
  - "This page was last edited 02 December 2025". It still states h(N) ≪ N^{log 3/log 22 + o(1)} (Hunter, comment of 18 Oct 2025) and h(N) ≫ exp(c(log N)^{1/9}).
  - "Comments (2)": Hunter 18 Oct 2025 and ruizshi 4 Aug 2026. "Proof claims (2)": Itabe and Shi–Dong. "The ability to post new comments has been suspended."
  - The only comment on Shi–Dong's claim (Xiao Hu, 24 Jul 2026) is a favourable summary, not a check.
- **OAI catalogue** (`oai_contents.md`, 719 manuscripts / 372 families): its item **"160. Superexponential van der Waerden numbers"** (W_r(k) > k^{ck⌊log₂ r⌋}) is its own internal index, not erdosproblems #160.
  - A grep for h(N), three colours, symmetric colourings, uniform sets, Ruzsa, Gowers or 4-AP colourings finds nothing. **Erdős #160 (4-APs with at least 3 colours) is not in that catalogue.**

## State of the problem (Erdős #160, h(N) = least number of colours of [N] such that every nontrivial 4-AP gets at least 3 colours), as of 2026-10-13

**Upper bounds**

| Bound | Source | Date | Status |
|---|---|---|---|
| **h(N) ≤ N^{1/4+o(1)}** (best claimed) | Shi–Dong, arXiv:2607.20752 (https://arxiv.org/abs/2607.20752); proof claim on https://www.erdosproblems.com/forum/thread/160/proof-claims | v1 22 Jul 2026, v2 28 Jul 2026; claim 24 Jul 2026 | Preprint, not refereed |
| N^{1/3+o(1)} | Itabe, https://github.com/ritabe-dev/ErdosProblem160-OneThirdUpper/releases/tag/v0.2.1-review-candidate (manuscript plus Lean 4 per author; seat B did not check the Lean) | First public 14 Jul 2026 05:26Z; forum claim 15 Jul 2026 | Unrefereed |
| N^{log 3/log 22 + o(1)} ≈ N^{0.355} (the bound recorded on the page) | Hunter, forum comment 18 Oct 2025, combining DTZ's Z/22 colouring and tensor power (https://arxiv.org/abs/2307.06914) with Behrend-type product colourings | Comment 2025; DTZ 2025 | DTZ is peer-reviewed (Math. Proc. Camb. Phil. Soc. 179 (2025) 79–103); the deduction is a forum comment |
| N^{2/3} | LeechLattice, MathOverflow | — | — |

- For the non-ABBA patterns, Shi–Dong rely on DTZ's refereed Lemmas 3.2 and 7.11 plus their own Lemma 5.3 (AABB). Itabe uses his own mod-24 and dyadic filters (§§4–5 of his manuscript).

**Lower bounds**

| Bound | Source | Date | Status |
|---|---|---|---|
| **h(N) ≫ exp(c (log N)^{1/6} (log log N)^{−1/6})** (best claimed) | Raghavan's r₃ bound, arXiv:2603.27045 (https://arxiv.org/abs/2603.27045), plus the elementary reduction above; posted as a comment by ruizshi | Paper v1–v3 Mar–May 2026; comment 4 Aug 2026 | Preprint, not refereed |
| exp(c(log N)^{1/9}) (the bound recorded on the page) | Bloom–Sisask, arXiv:2309.02353 | 2023 | No journal-ref on arXiv |
| exp(c(log N)^{1/12}) | Kelley–Meka bound; the Bloom–Sisask exposition of it is Essential Number Theory 2 (2023), refereed | 2023 | Refereed |

**Net position**
- Nothing in 2026 is refereed.
- The problem is listed **open** on both erdosproblems.com and the teorth database. Neither has been updated for the 2026 claims.
- The gap remains exp((log N)^{1/6−o(1)}) ≤ h(N) ≤ N^{1/4+o(1)}, both preprint-level.

**Side consequences of Shi–Dong** (both preprint, both resting on refereed DTZ reductions, and §6 holds as read):
- ρ₄(α) = O_ε(α^{5−ε}), against the refereed α^{4.406} (DTZ Cor 1.9).
- The first counterexamples to Gowers' Conj. 4.2 for even k ≥ 6, with exponent k + (k−2)²/(4(k−1)) − ε. These are qualitative and need p > 5¹⁰ already for k = 6.
